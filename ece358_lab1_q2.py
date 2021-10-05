import math
import random
import matplotlib.pyplot as plt


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
        queue = []

        # Generate arrival and departure events.
        while (1):
            time = exponential_random_var(packet_rate_lambd)
            packet_size = exponential_random_var(size_lambd)

            simulation_duration += time
            queue.append(Event("Arrival", simulation_duration))

            service_time = packet_size / transmission_rate

            if simulation_duration < departure_time:
                departure_time = departure_time + service_time
            else:
                departure_time = simulation_duration + service_time

            if departure_time < simulation_time:
                queue.append(Event("Departure", departure_time))

            if simulation_duration > simulation_time:
                break

        # Generate observer events.
        simulation_duration = 0
        while (1):
            time = exponential_random_var(packet_rate_lambd * 5)
            simulation_duration += time
            queue.append(Event("Observer", simulation_duration))

            if simulation_duration > simulation_time:
                break

        queue.sort(key=Event.get_occurrence_time)

        # for item in queue:
        #     print(item.get_event_type())
        #     print(item.get_occurrence_time())

        self.queue = queue

    def output_queue(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)


class Event:
    def __init__(self, event_type, occurrence_time):
        self.event_type = event_type
        self.occurrence_time = occurrence_time

    def get_event_type(self):
        return self.event_type

    def get_occurrence_time(self):
        return self.occurrence_time

    def insert_service_time(self, service_time):
        self.service_time = service_time

    def insert_departure_time(self, departure_time):
        self.departure_time = departure_time        


def startSimulation(simulation_duration, packet_rate_lambd, size_lambd, transmission_rate):
    queue = Queue(simulation_duration, packet_rate_lambd, size_lambd, transmission_rate)

    output_list = []

    packets_in_buffer = 0
    i = 0

    while (queue.size() != 0):
        print(i)
        event = queue.output_queue()

        if (event.get_event_type() == "Arrival"):
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

    
    return {"packets_average": packets_average, "packets_idle" : packets_idle}


TRANSMISSION_TIME = 1000000
PACKET_SIZE = 2000
SIMULATION_TIME = 100

average_list_y = []
idle_list_y = []
list_x = []

for i in range(25, 95, 10):
    p = i * TRANSMISSION_TIME / 2000 / 100
    simulation_result = startSimulation(SIMULATION_TIME, p , 1 / PACKET_SIZE, TRANSMISSION_TIME)
    average_list_y.append(simulation_result["packets_average"])
    idle_list_y.append(simulation_result["packets_idle"])
    list_x.append(i / 100)

plt.plot(list_x, average_list_y)
plt.xlabel("p")
plt.ylabel("E[N]")
plt.title("Average # of Packets vs Utilization of Queue")
plt.show()

plt.plot(list_x, idle_list_y)
plt.xlabel("p")
plt.ylabel("P_idle")
plt.title("P_idle vs Utilization of Queue")
plt.show()


