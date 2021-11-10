import math
import random
import heapq

KMAX = 10
TP = 512


# Formula to calculate an exponential random variable, with a given lambda.
def exponential_random_var(lambd):
    uniform_random_var = random.random()
    return -1 * (1/lambd) * math.log(1 - uniform_random_var)


class Queue:
    def __init__(self, packet_size, packet_rate, simulation_time):
        self.packet_size = packet_size
        self.packet_rate = packet_rate
        self.simulation_time = simulation_time
        self.collision_counter = 0
        self.wait_time = 0

        simulation_duration = 0
        queue = []
        # Generate arrival and departure events.
        while simulation_duration < self.simulation_time:
            # Generate random variables of inter-arrival times and sizes of packets.
            event_time = exponential_random_var(self.packet_rate)

            # Sum the total arrival time so it halts once it is equal to or greater
            # than the provided simulation time.
            simulation_duration += event_time

            # Append packet arrival time to the list.
            queue.append(simulation_duration)

        # Sort queue based on occurrence time.
        queue.sort(reverse=True)

        self.queue = queue

    def check_queue(self):
        if len(self.queue) > 0:
            return self.queue[-1]
        else: 
            return -1

    def pop_queue(self):
        self.queue.pop()

    def exponential_wait(self, current_time):
        if len(self.queue) > 0:
            self.collision_counter += 1

            if self.collision_counter >= KMAX:
                self.collision_counter = 0
                self.pop_queue()
            else:
                exp_random = random.randrange(0, 2 ** self.collision_counter - 1)
                self.queue[-1] = current_time + exp_random * TP




