import math
import random

def exponential_random_var(lambd):
    uniform_random_var = random.random()
    return -1 * (1/lambd) * math.log(1 - uniform_random_var)

class Queue:
    def __init__(self, simulation_time, lambd):
        self.lambd = lambd
        self.simulation_time = simulation_time

        simulation_duration = 0
        queue = []

        while (1):
            time = exponential_random_var(lambd)
            packet_size = exponential_random_var(lambd)

            simulation_duration += time
            queue.append(Event(packet_size, simulation_duration))

            if (simulation_duration > simulation_time):
                break

        self.queue = queue

    def output_queue(self):
        return self.queue.pop(0)
    
    def size(self):
        return len(self.queue)


class Event:
    def __init__(self, packet_size, arrive_time):
        self.packet_size = packet_size
        self.arrive_time = arrive_time
    
    def get_arrival_time(self):
        return self.arrive_time

    def get_packet_size(self):
        return self.packet_size

    def insert_service_time(self, service_time):
        self.service_time = service_time
    
    def insert_departure_time(self, departure_time):
        self.departure_time = departure_time

class EventList:
    def __init__(self, arrival_time, packet_size, service_time, departure_time):
        self.packet_size = packet_size
        self.arrive_time = arrival_time
        self.service_time = service_time
        self.departure_time = departure_time


def calculateDeparture(arrivalEvent, transmission_rate):
    service_time = arrivalEvent.get_packet_size() / transmission_rate
    departure_time = arrivalEvent.get_arrival_time() + service_time
    arrivalEvent.insert_service_time(service_time)
    arrivalEvent.insert_departure_time(departure_time)

        


def startSimulation(simulation_time, lambd, transmission_rate):
    queue = Queue(simulation_time, lambd)

    output_list = []

    while (queue.size != 0):
        arrival_event = queue.output_queue()
        
        calculateDeparture(arrival_event, transmission_rate)

        output_list.append(arrival_event)
    
    print(output_list)

startSimulation(10, 50, 0.01)


