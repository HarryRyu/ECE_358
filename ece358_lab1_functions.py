import math
import random
import threading
import sys

from ece358_lab1_classes import Queue


# Formula to calculate an exponential random variable, with a given lambda.
def exponential_random_var(lambd):
    uniform_random_var = random.random()
    return -1 * (1/lambd) * math.log(1 - uniform_random_var)


def startSimulation(parameters, packet_rate, buffer_size, simulation_time):

    queue = Queue(parameters, packet_rate, simulation_time)

    # Define variables and assign starting values.
    number_of_packets = 0  # Used for counting how many packets in buffer.
    no_packets = 0  # Used for counting how many times there are no packets in buffer.
    packets_in_buffer = 0  # Used for counting total number of packets in buffer.
    packets_loss = 0  # Used for counting if packets are dropped due to buffer overflow.
    observer_count = 0  # Used for counting total number of observer events.
    total_packets_arrival = 0  # Used for counting total number of arrived packets.
    i = 0
    queue_size = queue.size()

    while queue.size() != 0:
        percentage = math.floor((i / queue_size * 100))
        if percentage % 10 == 0:
            print(f'{percentage}% done')
            sys.stdout.write("\033[F")

        event = queue.output_queue()

        # Depending on the type of the event, modify the buffer and increment
        # respective counters.
        if event[1] == "Arrival":
            # Buffer is full and need to drop arrival and respective departure packet.
            if (buffer_size >= 0) and (packets_in_buffer + 1 >= buffer_size):
                packets_loss += 1
            else:
                packets_in_buffer += 1
                queue.generate_departure(event[0])

            total_packets_arrival += 1

        elif event[1] == "Departure":
            packets_in_buffer -= 1

        elif event[1] == "Observer":
            observer_count += 1
            number_of_packets += packets_in_buffer
            if packets_in_buffer == 0:
                no_packets += 1
        i += 1

    # Calculate performance metrics.
    average = (packet_rate, number_of_packets / observer_count)
    p_idle = (packet_rate, no_packets / observer_count)
    p_loss = (packet_rate, packets_loss / total_packets_arrival)

    return [average, p_idle, p_loss]


# Each function runs a simulation
def simulate_thread(parameters, packet_rate, buffer_size, simulation_time, average_list, p_idle_list, loss_list):

    print(
        f'Simulation with packet rate {packet_rate} and buffer size {buffer_size} '
        f'and simulation time {simulation_time} started')

    # Run the simulation.
    [average, p_idle, p_loss] = startSimulation(parameters, packet_rate, buffer_size, simulation_time)

    # Store into central list.
    average_list.append(average)
    p_idle_list.append(p_idle)
    loss_list.append(p_loss)

    print(f'Simulation with packet rate {packet_rate} and buffer size {buffer_size} '
          f'and simulation time {simulation_time} ended')


def simulate_buffer(final_average, final_loss, parameters, buffer_size):
    simulation_time = parameters["simulation_time"] 
    packet_rates = parameters["packet_rates"]

    print(f'Finite Buffer Thread with Buffer Size {buffer_size} Started')

    # List for storing output. It will be a 3D list: 2nd dimension for storing different simulation time,
    # 3rd dimension for storing different packet rates.
    final_results = {
        "average": [[], []],
        "p_loss": [[], []]
    }

    # ---------- GENERATING FIRST SET OF DATA -----------

    # Generate the first set of simulation data at 1000s simulation time
    list_counter = 0
    thread_list = []

    for packet_rate in range(packet_rates["init"], packet_rates["end"], packet_rates["increment"]):
        final_results["average"][0].append([])
        final_results["p_loss"][0].append([])
        final_results["average"][1].append([])
        final_results["p_loss"][1].append([])
        
        average = final_results["average"][0][list_counter]
        p_loss = final_results["p_loss"][0][list_counter]
        p_idle = []

        packet_rate = packet_rate / 100
        t = threading.Thread(target=simulate_thread, args=(parameters, packet_rate, buffer_size, simulation_time, average, p_idle, p_loss))

        thread_list.append(t)
        list_counter += 1

    # Start running the threads
    for thread in thread_list:
        thread.start()

    # ---------- GENERATING SECOND SET OF DATA -----------

    # Stop the function if test passes. Test will pass if the margin is less than 5%
    test_pass = False
    list_ptr = 0

    while not test_pass:
        # Increment the simulation time by 1000s.
        # It should start at 2000s and continue until margin requirements are met.
        simulation_time += parameters["simulation_time"] 
        list_ptr = list_ptr ^ 1

        # Create threads to run simulation at different packet rates.
        list_counter = 0
        thread_list_next = []
        for packet_rate in range(packet_rates["init"], packet_rates["end"], packet_rates["increment"]):

            final_results["average"][list_ptr][list_counter] = []
            final_results["p_loss"][list_ptr][list_counter] = []

            average = final_results["average"][list_ptr][list_counter]
            p_loss = final_results["p_loss"][list_ptr][list_counter]
            p_idle = []
            packet_rate = packet_rate / 100
            t = threading.Thread(target=simulate_thread, args=(parameters, packet_rate, buffer_size, simulation_time, average, p_idle, p_loss))
            thread_list_next.append(t)
            list_counter += 1

        # Start running the threads
        for thread in thread_list_next:
            thread.start()

        # Wait for the threads to stop running
        if simulation_time == parameters["simulation_time"] * 2:
            for thread in thread_list:
                thread.join()

        for thread in thread_list_next:
            thread.join()

        # Check if margin is within 5%
        for i in range(len(final_results["average"][0])):

            old_average = final_results["average"][0][i][0][1]
            new_average = final_results["average"][1][i][0][1]
            old_loss = final_results["p_loss"][0][i][0][1]
            new_loss = final_results["p_loss"][1][i][0][1]

            # Margin value of average # of packet in buffer
            margin_packet = abs((old_average - new_average) / old_average)

            if (old_loss) != 0:
                margin_loss = abs((old_loss - new_loss) / old_loss)
            else:
                margin_loss = abs((old_loss - new_loss))

            if margin_packet > 0.05 or margin_loss > 0.05:
                test_pass = False
                break
            else:
                test_pass = True

    # Insert the values into the list
    final_average.append(final_results["average"][list_ptr])
    final_loss.append(final_results["p_loss"][list_ptr])

    # # Store data into file as backup
    # f = open(f'ECE318_Q6_Buffer_Size_{buffer_size}_Average_Output', "w")
    # string1 = repr(average_list_y[list_ptr])
    # f.write(string1)
    # f.close()

    # f = open(f'ECE318_Q6_Buffer_Size_{buffer_size}_Loss_Output', "w")
    # string1 = repr(loss_list_y[list_ptr])
    # f.write(string1)
    # f.close()

    print(f'Finite Buffer Thread with Buffer Size {buffer_size} ended')
