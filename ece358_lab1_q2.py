import math
import random
import matplotlib.pyplot as plt
import sys
import time
import threading


def exponential_random_var(lambd):
    uniform_random_var = random.random()
    return -1 * (1 / lambd) * math.log(1 - uniform_random_var)


class Queue:
    def __init__(self, simulation_time, packet_rate_lambd, size_lambd, transmission_rate):
        self.packet_rate_lambd = packet_rate_lambd
        self.size_lambd = size_lambd
        self.simulation_time = simulation_time

        simulation_duration = 0
        departure_time = 0
        link_number = 0
        queue = []

        # Generate arrival and departure events.
        while simulation_duration < simulation_time:
            # Generate random variables of inter-arrival times and sizes of packets.
            event_time = exponential_random_var(packet_rate_lambd)
            packet_size = exponential_random_var(size_lambd)

            # Sum the total arrival time so it halts once it is equal to or greater
            # than the provided simulation time.
            simulation_duration += event_time

            # Calculate the service time.
            service_time = packet_size / transmission_rate

            # If statements to check if there is anything being serviced right now.
            # If there is, the departure time is the departure time of the previous
            # packet, plus the service time of the current packet.
            if simulation_duration < departure_time:
                departure_time = departure_time + service_time
            else:
                departure_time = simulation_duration + service_time

            # Append the arrival and departure events to the Queue list.
            queue.append(Event("Arrival", simulation_duration, link_number))
            queue.append(Event("Departure", departure_time, link_number))

            # Append an integer to link the departure and arrival events
            # the finite buffer case.
            link_number += 1

        # Generate observer events at 5 times the rate of arrival/departure events.
        simulation_duration = 0
        while simulation_duration < simulation_time:
            event_time = exponential_random_var(packet_rate_lambd * 5)
            simulation_duration += event_time
            queue.append(Event("Observer", simulation_duration, -1))

        # Sort queue based on occurrence time.
        queue.sort(key=Event.get_occurrence_time, reverse=True)

        self.queue = queue

    def output_queue(self):
        return self.queue.pop(len(self.queue) - 1)

    def remove_departure(self, link_number):
        for i in reversed(range(len(self.queue))):
            if self.queue[i].get_link_number() == link_number:
                self.queue[i].set_event_type("Deprecated")
                return

    def size(self):
        return len(self.queue)


class Event:
    def __init__(self, event_type, occurrence_time, link_number):
        self.event_type = event_type
        self.occurrence_time = occurrence_time
        self.link_number = link_number

    def get_event_type(self):
        return self.event_type

    def get_occurrence_time(self):
        return self.occurrence_time

    def insert_service_time(self, service_time):
        self.service_time = service_time

    def insert_departure_time(self, departure_time):
        self.departure_time = departure_time

    def get_link_number(self):
        return self.link_number

    def set_event_type(self, event):
        self.event_type = event


def startSimulation(simulation_duration, packet_rate_lambd, size_lambd, transmission_rate, buffer_size):
    queue = Queue(simulation_duration, packet_rate_lambd, size_lambd, transmission_rate)

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
        if event.get_event_type() == "Arrival":
            # Buffer is full and need to drop arrival and respective departure packet.
            if (buffer_size >= 0) and (packets_in_buffer + 1 >= buffer_size):
                link_number = event.get_link_number()
                queue.remove_departure(link_number)
                packets_loss += 1
            else:
                packets_in_buffer += 1
            total_packets_arrival += 1

        elif event.get_event_type() == "Departure":
            packets_in_buffer -= 1

        elif event.get_event_type() == "Observer":
            observer_count += 1
            number_of_packets += packets_in_buffer
            if packets_in_buffer == 0:
                no_packets += 1
        i += 1

    # Calculate performance metrics.
    packets_average = number_of_packets / observer_count
    packets_idle = no_packets / observer_count
    packets_loss = packets_loss / total_packets_arrival

    return {"packets_average": packets_average, "packets_idle": packets_idle, "packets_loss": packets_loss}


# For question 3
def simulate_question_3():
    start_time = time.time()

    # Define constant and assign variables.
    TRANSMISSION_TIME = 1000000
    PACKET_SIZE = 2000
    simulation_time = 0

    # List to store # of packets in buffer.
    prev_average_list_y = []

    # List to store percentage of idle time for buffer.
    prev_idle_list_y = []

    # List of p steps.
    list_x = []

    # For stability testing.
    test_pass = False

    # Run until margin is less than 5%
    while not test_pass:
        current_time = time.time() - start_time
        minutes = math.floor(current_time / 60)
        seconds = current_time % 60

        print(f'It has been {minutes}m {seconds}s')
        simulation_time += 1000
        print(f'Running simulation with time: {simulation_time}')
        # Run with different values of p, step size of 0.1
        for i in range(25, 35, 10):
            print(f'Initiating rho of: {i/100}')
            average_list_y = []
            idle_list_y = []
            p = i * TRANSMISSION_TIME / 2000 / 100
            simulation_result = startSimulation(simulation_time, p, 1 / PACKET_SIZE, TRANSMISSION_TIME, 10)
            average_list_y.append(simulation_result["packets_average"])
            idle_list_y.append(simulation_result["packets_idle"])
            list_x.append(i / 100)

        if len(prev_average_list_y) != 0:
            for i in range(len(prev_average_list_y)):
                margin = abs((prev_average_list_y[i] - average_list_y[i]) / prev_average_list_y[i])
                margin2 = abs((prev_idle_list_y[i] - idle_list_y[i]) / prev_idle_list_y[i])
                if margin > 0.05 and margin2 > 0.05:
                    test_pass = False
                    break
                else:
                    test_pass = True

        prev_average_list_y = average_list_y
        prev_idle_list_y = idle_list_y

    # Plot the graphs
    plt.plot(list_x, prev_average_list_y)
    plt.xlabel("p")
    plt.ylabel("E[N]")
    plt.title(f'Average # of Packets vs Utilization of Queue with Simulation Time: {simulation_time}')
    plt.show()

    plt.plot(list_x, prev_idle_list_y)
    plt.xlabel("p")
    plt.ylabel("P_idle")
    plt.title(f'P_idle vs Utilization of Queue with Simulation Time: {simulation_time}')
    plt.show()


# Constant variables
TRANSMISSION_TIME = 1000000
PACKET_SIZE = 2000

# List to store # of packets in buffer
final_average_list_y = [[], [], []]
# List to store percentage of idle time for buffer
final_loss_list_y = [[], [], []]


# For question 6
def simulate_question_6():
    print("----- Q6 Simulation Initiated -----")
    start_time = time.time()
    packet_rate_init = 50
    packet_rate_end = 150
    buffer_size = [10, 25, 50]

    # List of p steps
    list_x = []
    for packet_rate in range(packet_rate_init, packet_rate_end, 10):
        list_x.append(packet_rate)
    # For stability testing

    thread_list = []
    for j in range(len(buffer_size)):
        thread_list.append(threading.Thread(target=simlutate_finite_buffer,
                                            args=(j, buffer_size[j], packet_rate_init, packet_rate_end)))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    # Plot the graphs
    plt.plot(list_x, final_average_list_y[0])
    plt.plot(list_x, final_average_list_y[1])
    plt.plot(list_x, final_average_list_y[2])
    plt.xlabel("p")
    plt.ylabel("E[N]")
    plt.title(f'Average # of Packets vs Utilization of Queue')
    plt.legend(buffer_size)
    plt.show()

    plt.plot(list_x, final_loss_list_y[0])
    plt.plot(list_x, final_loss_list_y[1])
    plt.plot(list_x, final_loss_list_y[2])
    plt.xlabel("p")
    plt.ylabel("P_idle")
    plt.title(f'P_idle vs Utilization of Queue')
    plt.legend(buffer_size)
    plt.show()
    current_time = time.time() - start_time
    minutes = math.floor(current_time / 60)
    seconds = current_time % 60

    print(f'It has been {minutes}m {seconds}s')
    print("----- Q6 Simulation Terminated -----")


def simlutate_finite_buffer(j, buffer_size, packet_rate_init, packet_rate_end):
    print(f'Finite Buffer Thread with Buffer Size {buffer_size} Started')
    simulation_start_constant = 500
    # List for storing output. It will be a 3D list: 2nd dimension for storing different simulation time,
    # 3rd dimension for storing different packet rates.
    average_list_y = [[], []]
    loss_list_y = [[], []]
    for packet_rate in range(packet_rate_init, packet_rate_end, 10):
        average_list_y[0].append([])
        average_list_y[1].append([])
        loss_list_y[0].append([])
        loss_list_y[1].append([])
    list_ptr = 0

    # Increment simulation_time until margin of output is less than 5%
    simulation_time = simulation_start_constant

    # ---------- GENERATING FIRST SET OF DATA -----------

    # Generate the first set of simulation data at 1000s simulation time
    list_counter = 0
    thread_list = []
    for packet_rate in range(packet_rate_init, packet_rate_end, 10):
        thread_list.append(threading.Thread(target=simulate_thread, args=(
            simulation_time, packet_rate, buffer_size, average_list_y[0][list_counter], [],
            loss_list_y[0][list_counter])))
        list_counter += 1

    # Start running the threads
    for thread in thread_list:
        thread.start()

    # ---------- GENERATING SECOND SET OF DATA -----------

    # Stop the function if test passes. Test will pass if the margin is less than 5%
    test_pass = False

    while not test_pass:
        # Increment the simulation time by 1000s.
        # It should start at 2000s and continue until margin requirements are met.
        simulation_time += simulation_start_constant
        list_ptr = list_ptr ^ 1

        # Create threads to run simulation at different packet rates.
        list_counter = 0
        thread_list_next = []
        for packet_rate in range(packet_rate_init, packet_rate_end, 10):
            thread_list_next.append(threading.Thread(target=simulate_thread, args=(
                simulation_time, packet_rate, buffer_size, average_list_y[list_ptr][list_counter], [],
                loss_list_y[list_ptr][list_counter])))
            list_counter += 1

        # Start running the threads
        for thread in thread_list_next:
            thread.start()

        # Wait for the threads to stop running
        if simulation_time == simulation_start_constant * 2:
            for thread in thread_list:
                thread.join()

        for thread in thread_list_next:
            thread.join()

        # Check if margin is within 5%
        for i in range(len(average_list_y[0])):
            # Margin value of average # of packet in buffer
            margin_packet = abs((average_list_y[0][i][0] - average_list_y[1][i][0]) / average_list_y[0][i][0])
            if (loss_list_y[0][i][0]) != 0:
                margin_loss = abs((loss_list_y[0][i][0] - loss_list_y[1][i][0]) / loss_list_y[0][i][0])
            else:
                margin_loss = abs((loss_list_y[0][i][0] - loss_list_y[1][i][0]))
            if margin_packet > 0.05 or margin_loss > 0.05:
                test_pass = False
                break
            else:
                test_pass = True

    # Insert the values into the list
    final_average_list_y[j] = average_list_y[list_ptr]
    final_loss_list_y[j] = loss_list_y[list_ptr]

    # Store data into file as backup
    f = open(f'ECE318_Q6_Buffer_Size_{buffer_size}_Average_Output', "w")
    string1 = repr(average_list_y[list_ptr])
    f.write(string1)
    f.close()

    f = open(f'ECE318_Q6_Buffer_Size_{buffer_size}_Loss_Output', "w")
    string1 = repr(loss_list_y[list_ptr])
    f.write(string1)
    f.close()

    print(f'Finite Buffer Thread with Buffer Size {buffer_size} ended')


# Each function runs a simulation
def simulate_thread(simulation_time, packet_rate, buffer_size, average_list_y, idle_list_y, loss_list_y):
    print(
        f'Simulation with packet rate {packet_rate} and buffer size {buffer_size} '
        f'and simulation time {simulation_time} started')
    # Calculate packet_rate.
    p = packet_rate * TRANSMISSION_TIME / 2000 / 100

    # Run the simulation.
    simulation_result = startSimulation(simulation_time, p, packet_rate / PACKET_SIZE, TRANSMISSION_TIME, buffer_size)

    # Store into central list.
    average_list_y.append(simulation_result["packets_average"])
    idle_list_y.append(simulation_result["packets_idle"])
    loss_list_y.append(simulation_result["packets_loss"])

    print(f'Simulation with packet rate {packet_rate} and buffer size {buffer_size} '
          f'and simulation time {simulation_time} ended')

# current_time = time.time() - start_time
# minutes = math.floor(current_time / 60)
# seconds = current_time % 60

# print(f'It has been {minutes}m {seconds}s')
simulate_question_3()
