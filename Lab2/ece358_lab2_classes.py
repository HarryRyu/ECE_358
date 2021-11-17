import math
import random

KMAX = 10
LAN_SPEED = 1e6
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
        self.bus_counter = 0

        simulation_duration = 0
        queue = []
        # Generate arrival events.
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
        self.collision_counter = 0
        return self.queue.pop()

    def exponential_wait(self, current_time):
        # Check if there is more than 1 item in the queue. If so, it means collision, so increment counter.
        if len(self.queue) > 0:
            self.collision_counter += 1

            # If the the number of collisions is greater than or equal to the maximum allowed (10),
            # drop the packet.
            if self.collision_counter >= KMAX:
                self.pop_queue()

            # If the collision counter isn't at 10 yet, back off based on the collision formula.
            else:
                exp_random = random.randrange(0, 2 ** self.collision_counter)
                self.queue[-1] = current_time + exp_random * TP / LAN_SPEED

    def test_size(self):
        return len(self.queue)

    def exponential_bus_wait(self, current_time, packet_size, transmission_speed, propagation_duration):
        # Check if there is more than 1 item in the queue. If so, get the arrival time of that event.
        if len(self.queue) > 0:
            next_arrival_time = self.queue[-1]

            # Check if the next event time will try to send when there is already a packet sending.
            # That is, check if the medium is busy. If it is, increment busy bus counter.
            if next_arrival_time < current_time + propagation_duration + packet_size / transmission_speed:
                self.bus_counter += 1

                # If busy bus counter is equal to or greater than allowed maximum (10),
                # drop packet and reset counter.
                if self.bus_counter >= KMAX:
                    self.queue.pop()
                    self.bus_counter = 0

                # If busy bus counter is not at 10 yet, back off based on exponential formula.
                else:
                    exp_random = random.randrange(0, 2 ** self.bus_counter)
                    self.queue[-1] = next_arrival_time + exp_random * TP / LAN_SPEED
