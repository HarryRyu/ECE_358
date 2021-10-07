import heapq
import math
import random
import matplotlib.pyplot as plt
import statistics
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
        link_number = 0
        queue = []

        # Generate arrival and departure events.
        while simulation_duration < simulation_time:
            # Generate random variables of inter-arrival times and sizes of packets.
            event_time = exponential_random_var(packet_rate_lambd)

            # Sum the total arrival time so it halts once it is equal to or greater
            # than the provided simulation time.
            simulation_duration += event_time

            # Append the arrival events to the Queue list. Will be tuple.
            queue.append((simulation_duration, "Arrival"))

        # Generate observer events at 5 times the rate of arrival/departure events.
        simulation_duration = 0
        while simulation_duration < simulation_time:
            event_time = exponential_random_var(packet_rate_lambd * 5)
            simulation_duration += event_time
            queue.append((simulation_duration, "Observer"))

        # Make it a heapq by
        heapq.heapify(queue)
        self.queue = queue
        # Generate random variable for departure event
        # exponential_var = exponential_random_var(packet_rate_lambd)

        # Insert departure event
        # departure_time = simulation_duration + exponential_var
        # heap_departure = (departure_time, "Departure")
        # heapq.heappush(heap_queue, heap_departure)
        # self.queue = heap_queue

    def pop_event_from_queue(self):
        return heapq.heappop(self.queue)

    def size(self):
        return len(self.queue)


def create_queue(simulation_time, packet_rate_lambd, size_lambd):
    simulation_duration = 0
    queue = []

    # Generate arrival and departure events.
    while simulation_duration < simulation_time:
        # Generate random variables of inter-arrival times and sizes of packets.
        event_time = exponential_random_var(packet_rate_lambd)

        # Sum the total arrival time so it halts once it is equal to or greater
        # than the provided simulation time.
        simulation_duration += event_time

        # Append the arrival events to the Queue list. Will be tuple.
        queue.append((simulation_duration, "Arrival"))

    # Generate observer events at 5 times the rate of arrival/departure events.
    simulation_duration = 0
    while simulation_duration < simulation_time:
        event_time = exponential_random_var(packet_rate_lambd * 5)
        simulation_duration += event_time
        queue.append((simulation_duration, "Observer"))
    # Make it a heapq and return

    return queue


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

    def get_link_number(self):
        return self.link_number

    def set_event_type(self, event):
        self.event_type = event


def start_simulation(simulation_duration, packet_rate_lambd, size_lambd, buffer_size):
    queue = create_queue(simulation_duration, packet_rate_lambd, size_lambd)

    # Make it a heapq
    heapq.heapify(queue)

    # Define variables and assign starting values.
    number_of_packets = 0  # Used for counting how many packets in buffer.
    no_packets = 0  # Used for counting how many times there are no packets in buffer.
    packets_in_buffer = 0  # Used for counting total number of packets in buffer.
    packets_loss = 0  # Used for counting if packets are dropped due to buffer overflow.
    observer_count = 0  # Used for counting total number of observer events.
    total_packets_arrival = 0  # Used for counting total number of arrived packets.
    i = 0
    queue_size = len(queue)
    while len(queue) != 0:
        percentage = math.floor((i / queue_size * 100))
        if percentage % 10 == 0:
            print(f'{percentage}% done')
            sys.stdout.write("\033[F")

        event = heapq.heappop(queue)
        # Depending on the type of the event, modify the buffer and increment
        # respective counters.
        if event[1] == "Arrival":
            # Buffer is full and need to drop arrival and respective departure packet.
            if (buffer_size >= 0) and (packets_in_buffer + 1 >= buffer_size):
                packets_loss += 1
            else:
                packets_in_buffer += 1
                # Generate random variable for departure event
                exponential_var = exponential_random_var(packet_rate_lambd)

                # Insert departure event
                departure_time = event[0] + exponential_var
                heap_departure = (departure_time, "Departure")
                heapq.heappush(queue, heap_departure)
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
    packets_average = number_of_packets / observer_count
    packets_idle = no_packets / observer_count
    packets_loss = packets_loss / total_packets_arrival

    return {"packets_average": packets_average, "packets_idle": packets_idle, "packets_loss": packets_loss}


def percent_difference(value1, value2):
    return (abs(value1-value2))/(statistics.mean([value1, value2]))


# Testing question 6
def simulate_question_6():
    start_time = time.time()

    # Define constant and assign variables.
    transmission_time = 1e6
    packet_size = 2000
    simulation_time = 0
    max_iteration = 10  # Used to ensure that we don't get stuck in an infinite loop.
    difference_counter = 0

    # List to store # of packets in buffer.
    prev_average_list_y = []

    # List to store percentage of idle time for buffer.
    prev_idle_list_y = []

    # List of p steps.
    start_rho = 50
    end_rho = 150
    step_rho = 10

    # Use list comprehension to create list of rho's.
    list_x = list(value / 100 for value in range(start_rho, end_rho, step_rho))

    # For stability testing. This will get updated if the percent difference is < 5%.
    test_pass = False
    final_graph_values = []

    # Run until margin is less than 5%
    while not test_pass:
        current_time = time.time() - start_time
        minutes = math.floor(current_time / 60)
        seconds = current_time % 60

        print(f'It has been {minutes}m {seconds}s')
        simulation_time += 1000
        # Run with different values of p, step size of 0.1.
        # Create lists to store calculated values.
        average_list_y = []
        idle_list_y = []
        # List of p steps.
        for rho in list_x:
            print(f'Initiating rho of: {rho} and simulation time: {simulation_time}')
            p = rho * transmission_time / 2000
            simulation_result = start_simulation(simulation_time, p, 1 / packet_size, 10)
            average_list_y.append(simulation_result["packets_average"])
            idle_list_y.append(simulation_result["packets_idle"])

        graph_values = {'simulation_time': simulation_time,
                        'average_list_y': average_list_y,
                        'idle_list_y': idle_list_y}
        final_graph_values.append(graph_values)

        if len(prev_average_list_y) != 0:
            for i in range(len(prev_average_list_y)):
                margin = percent_difference(prev_average_list_y[i], average_list_y[i])
                margin2 = percent_difference(prev_idle_list_y[i], idle_list_y[i])
                if margin > 0.05 and margin2 > 0.05:
                    test_pass = False
                    break
                else:
                    test_pass = True

        test_pass = True  # FOR TESTING 1 iteration

        prev_average_list_y = average_list_y
        prev_idle_list_y = idle_list_y
        if difference_counter > max_iteration:
            print('Maximum iteration reached! Code did not converge.')
            break
    # Create legend list for graph.
    legend = []

    # Iteratively plot the graphs.
    for graph_value in final_graph_values:
        plt.plot(list_x, graph_value['average_list_y'])
        legend.append(graph_value['simulation_time'])
    plt.legend(legend)
    plt.xlabel("Traffic intensity, p")
    plt.ylabel("Average number of packets, E[N]")
    plt.title(f'Average # of Packets vs Traffic Intensity with varying simulation times')
    plt.show()

    for graph_value in final_graph_values:
        plt.plot(list_x, graph_value['idle_list_y'])
    plt.legend(legend)
    plt.xlabel("Traffic intensity, p")
    plt.ylabel("Fraction of time that buffer is empty, P_idle")
    plt.title(f'P_idle vs Traffic intensity with varying simulation times')
    plt.show()


simulate_question_6()
