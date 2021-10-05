import math
import random
import matplotlib.pyplot as plt
import sys
import time


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
        while (1):
            time = exponential_random_var(packet_rate_lambd)
            packet_size = exponential_random_var(size_lambd)

            simulation_duration += time
            queue.append(Event("Arrival", simulation_duration, link_number))

            service_time = packet_size / transmission_rate

            if simulation_duration < departure_time:
                departure_time = departure_time + service_time
            else:
                departure_time = simulation_duration + service_time

            if departure_time < simulation_time:
                queue.append(Event("Departure", departure_time, link_number))

            if simulation_duration > simulation_time:
                break
            link_number += 1

        # Generate observer events.
        simulation_duration = 0
        while (1):
            time = exponential_random_var(packet_rate_lambd * 5)
            simulation_duration += time
            queue.append(Event("Observer", simulation_duration, -1))

            if simulation_duration > simulation_time:
                break

        queue.sort(key=Event.get_occurrence_time)

        self.queue = queue

    def output_queue(self):
        return self.queue.pop(0)

    def remove_departure(self, link_number):
        for i in range(len(self.queue)):
            if (self.queue[i].get_link_number() == link_number):
                self.queue.pop(i)
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



def startSimulation(simulation_duration, packet_rate_lambd, size_lambd, transmission_rate, buffer_size):
    queue = Queue(simulation_duration, packet_rate_lambd, size_lambd, transmission_rate)

    output_list = []
    

    packets_in_buffer = 0
    packets_loss = 0
    i = 0
    queue_size = queue.size()
    while (queue.size() != 0):
        
        print(f'At queue {i} of {queue_size}')
        sys.stdout.write("\033[F")
        event = queue.output_queue()

        if (event.get_event_type() == "Arrival"):
            if ((buffer_size >= 0) and (packets_in_buffer + 1 >= buffer_size)):
                link_number = event.get_link_number()
                queue.remove_departure(link_number)
                packets_loss += 1
            else:
                packets_in_buffer += 1   
        elif (event.get_event_type() == "Departure"):
            packets_in_buffer -= 1
        elif (event.get_event_type() == "Observer"):
            output_list.append({'time': event.get_occurrence_time(), 'packets': packets_in_buffer})
        i += 1

    packets_average = 0
    packets_idle = 0
    for i in output_list:
        packets_average += i["packets"]
        if (i["packets"] == 0): 
            packets_idle += 1


    packets_average = packets_average / len(output_list)
    packets_idle = packets_idle / len(output_list)
    packets_loss = packets_loss / len(output_list)

    
    return {"packets_average": packets_average, "packets_idle" : packets_idle, "packets_loss" : packets_loss}

# For question 3
def simulate_question_3():
    start_time = time.time()
    # Constant variables
    TRANSMISSION_TIME = 1000000
    PACKET_SIZE = 2000


    simulation_time = 0

    # List to store # of packets in buffer
    prev_average_list_y = []
    # List to store percentage of idle time for buffer
    prev_idle_list_y = []
    # List of p steps
    list_x = []
    # For stability testing
    test_pass = False

    # Run until margin is less than 5%
    while (not test_pass):
        current_time = time.time() - start_time
        minutes = math.floor(current_time / 60)
        seconds = current_time % 60
        
        print(f'It has been {minutes}m {seconds}s')
        simulation_time += 1000
        print(f'Running simulation with time: {simulation_time}')
        # Run with different values of p, step size of 0.1
        for i in range(25, 95, 10):
            print(f'Initiating row of: {i}')
            average_list_y = []
            idle_list_y = []
            p = i * TRANSMISSION_TIME / 2000 / 100
            simulation_result = startSimulation(simulation_time, p , 1 / PACKET_SIZE, TRANSMISSION_TIME, 10)
            average_list_y.append(simulation_result["packets_average"])
            idle_list_y.append(simulation_result["packets_idle"])
            list_x.append(i / 100)

        if (len(prev_average_list_y) != 0):
            for i in range(len(prev_average_list_y)):
                margin = math.abs((prev_average_list_y[i] - average_list_y[i]) / prev_average_list_y[i])
                margin2 = math.abs((prev_idle_list_y[i] - idle_list_y[i]) / prev_idle_list_y[i])
                if (margin > 0.05 and margin2 > 0.05):
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


# For question 6
def simulate_question_6():
    start_time = time.time()
    # Constant variables
    TRANSMISSION_TIME = 1000000
    PACKET_SIZE = 2000
    buffer_size = [10,25,50]


    simulation_time = 0

    # List to store # of packets in buffer
    prev_average_list_y = [[],[],[]]
    # List to store percentage of idle time for buffer
    prev_idle_list_y = [[],[],[]]
    # List of p steps
    list_x = []
    # For stability testing
    test_pass = False

    for j in range(len(buffer_size)):
        # Run until margin is less than 5%
        while (not test_pass):
            current_time = time.time() - start_time
            minutes = math.floor(current_time / 60)
            seconds = current_time % 60
            
            print(f'It has been {minutes}m {seconds}s')
            simulation_time += 1000
            print(f'Running simulation with time: {simulation_time}')
            # Run with different values of p, step size of 0.1
            for i in range(50, 150, 10):
                print(f'Initiating row of: {i}')
                average_list_y = []
                idle_list_y = []
                p = i * TRANSMISSION_TIME / 2000 / 100
                simulation_result = startSimulation(simulation_time, p , 1 / PACKET_SIZE, TRANSMISSION_TIME, buffer_size[j])
                average_list_y[j].append(simulation_result["packets_average"])
                idle_list_y[j].append(simulation_result["packets_idle"])
                if (j==0):
                    list_x.append(i / 100)

            if (len(prev_average_list_y) != 0):
                for i in range(len(prev_average_list_y)):
                    margin = math.abs((prev_average_list_y[i] - average_list_y[i]) / prev_average_list_y[i])
                    margin2 = math.abs((prev_idle_list_y[i] - idle_list_y[i]) / prev_idle_list_y[i])
                    if (margin > 0.05 and margin2 > 0.05):
                        test_pass = False
                        break
                    else:
                        test_pass = True
            
            prev_average_list_y = average_list_y
            prev_idle_list_y = idle_list_y

    # Plot the graphs
    plt.plot(list_x, prev_average_list_y[0])
    plt.plot(list_x, prev_average_list_y[1])
    plt.plot(list_x, prev_average_list_y[2])
    plt.xlabel("p")
    plt.ylabel("E[N]")
    plt.title(f'Average # of Packets vs Utilization of Queue with Simulation Time: {simulation_time}')
    plt.show()

    plt.plot(list_x, prev_idle_list_y[0])
    plt.plot(list_x, prev_idle_list_y[1])
    plt.plot(list_x, prev_idle_list_y[2])
    plt.xlabel("p")
    plt.ylabel("P_idle")
    plt.title(f'P_idle vs Utilization of Queue with Simulation Time: {simulation_time}')
    plt.show()

simulate_question_3()

