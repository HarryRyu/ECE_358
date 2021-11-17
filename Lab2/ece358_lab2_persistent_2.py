from ece358_lab2_classes import Queue
import matplotlib.pyplot as plt

# Final copy of persistent simulation (Question 1).
def start_persistent_simulation(node_total, packet_rate, lan_speed, packet_size, node_distance, propagation_speed):
    # Initial simulation time
    simulation_time = 1000
    node_list = []

    attempted_transmission = 0
    successful_transmission = 0

    # Generate list of nodes with packet arrival times
    for _ in range(node_total):
        node_list.append(Queue(packet_size, packet_rate, simulation_time))

    # Start of iteration
    current_time = 0
    while current_time <= simulation_time:
        min_packet_arrival_time, node_num = get_arrival_time(node_list, current_time)
        
        current_time = min_packet_arrival_time
        attempted_transmission += 1

        collision_detected = False

        # Decide whether or not there is a collision.
        if len(node_num) == 1:
            if node_list[node_num[0]].check_queue() < current_time:
                collision_detected, node_num = False, node_num[0]
            else:
                collision_detected, node_num = check_collision(node_list, current_time, node_num[0],
                                                               node_distance / propagation_speed)
        else:
            collision_detected, node_num = True, node_num

        # If there is collision, back off appropriately.
        if collision_detected:
            exponential_backoff(node_list, node_num, current_time)

        # If not, attempt to transmit (but check the medium at an exponential wait time).
        else:
            time = node_list[node_num].pop_queue()

            if time < current_time:
                current_time += packet_size / lan_speed
            else:
                current_time = time + packet_size / lan_speed

            successful_transmission += 1

    # Calculate metrics.
    efficiency_value = successful_transmission / attempted_transmission
    throughput_value = successful_transmission * packet_size / simulation_time

    return efficiency_value, throughput_value


# Exponential back off for collisions.
def exponential_backoff(node_list, node, current_time):
    for i in range(len(node)):
        node_list[node[i]].exponential_wait(current_time)


# Iteratively check all nodes to see if there is a collision.
def check_collision(node_list, time, node, propagation_time):
    for i in range(len(node_list)):
        if i != node:
            propagation_time_final = abs(node - i) * propagation_time
            output_time = node_list[i].check_queue()
            if time + propagation_time_final > output_time > 0:
                return True, [node, i]
    return False, node


# Get the earliest time in all nodes that will act as the "sender".
def get_arrival_time(node_list, current_time):
    min_time = 99999999
    end_after = False
    node_num = []

    output_time_list = []
    for i in range(len(node_list)):
        output_time_list.append(node_list[i].check_queue())

    for i in range(len(output_time_list)):
        if current_time >= output_time_list[i] > 0:
            node_num.append(i)
            end_after = True

    if end_after:
        return current_time, node_num

    for i in range(len(output_time_list)):
        if current_time < output_time_list[i] <= min_time:
            node_num = [i]
            min_time = output_time_list[i]

    return min_time, node_num

# Define some constants in a list to iterate simulation through.
NODE_NUM = [20, 40, 60, 80, 100]
PACKET_RATE = [7, 10, 20]
LAN_SPEED = 1e6
PACKET_SIZE = 1500
NODE_DISTANCE = 10
PROPAGATION_SPEED = (2 / 3) * 3e8

efficiency = [[], [], []]
throughput = [[], [], []]


# Run simulation through all packets rates, for each number of nodes.
for i in NODE_NUM:
    for j in range(len(PACKET_RATE)):
        print(f'Starting Simulation with NODE_NUM: {i} and PACKET_RATE: {PACKET_RATE[j]}')
        efficiency_output, throughput_output = start_persistent_simulation(i, PACKET_RATE[j], LAN_SPEED, PACKET_SIZE, NODE_DISTANCE, PROPAGATION_SPEED)
        efficiency[j].append(efficiency_output)
        throughput[j].append(throughput_output)

# Store data into file as backup.
f = open("q1_eff_1000", "w")
string1 = repr(efficiency)
f.write(string1)
f.close()

f = open("q1_throughput_1000", "w")
string1 = repr(throughput)
f.write(string1)
f.close()

# Plot the data.
plt.plot(NODE_NUM, throughput[0])  # 7 packets/sec
plt.plot(NODE_NUM, throughput[1])  # 10 packets/sec
plt.plot(NODE_NUM, throughput[2])  # 20 packets/sec

plt.legend(["7", "10", "20"], title='Arrival rate')
plt.ylabel("Throughput (bps)")
plt.xlabel("Number of nodes")
plt.title('Number of nodes vs. throughput (1000T) ')
plt.show()

plt.plot(NODE_NUM, efficiency[0]) # 7 packets/sec
plt.plot(NODE_NUM, efficiency[1]) # 10 packets/sec
plt.plot(NODE_NUM, efficiency[2]) # 20 packets/sec

plt.legend(["7", "10", "20"], title='Arrival rate')
plt.ylabel("Efficiency")
plt.xlabel("Number of nodes")
plt.title('Number of nodes vs. efficiency (1000T) ')
plt.show()
