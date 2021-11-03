import math
import random
import heapq


# Formula to calculate an exponential random variable, with a given lambda.
def exponential_random_var(lambd):
    uniform_random_var = random.random()
    return -1 * (1/lambd) * math.log(1 - uniform_random_var)


class Queue:
    def __init__(self, parameters, packet_rate, simulation_time):
        self.simulation_time = simulation_time
        self.packet_rate = packet_rate
        self.packet_size = parameters["packet_size"]
        self.transmission_rate = parameters["transmission_rate"]
        self.departure_time = 0

        actual_packet_rate = self.packet_rate * self.transmission_rate / self.packet_size

        simulation_duration = 0
        queue = []

        # Generate arrival and departure events.
        while simulation_duration < self.simulation_time:
            # Generate random variables of inter-arrival times and sizes of packets.
            event_time = exponential_random_var(actual_packet_rate)

            # Sum the total arrival time so it halts once it is equal to or greater
            # than the provided simulation time.
            simulation_duration += event_time

            # Append the arrival and departure events to the Queue list.
            queue.append((simulation_duration, "Arrival"))

        # Sort queue based on occurrence time.
        heapq.heapify(queue)

        self.queue = queue
