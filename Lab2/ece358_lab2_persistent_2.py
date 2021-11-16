from ece358_lab2_classes import Queue, Queue_2
import matplotlib.pyplot as plt


def start_persistent_simulation(node_total, packet_rate, lan_speed, packet_size, node_distance, propagation_speed, simulation_time):

    current_time = 0
    attempted_transmission = 0
    successful_transmission = 0

    # Generate list of nodes with packet arrival times
    node_list = generate_nodes(node_total, packet_size, packet_rate, simulation_time)

    # Start of iteration
    while simulationNotOver(current_time, simulation_time):
        current_time, transmitting_nodes = get_arrival_time(node_list)
        collision_detected, collision_list = check_collision(node_list, current_time, transmitting_nodes, node_distance / propagation_speed)
        attempted_transmission += 1
        if collision_detected:
            current_time = time_after_collision(collision_list, current_time, node_distance / propagation_speed)
            exponential_backoff(node_list, collision_list, current_time)
        else:
            node = collision_list[0]
            time = node_list[node].pop_queue()
            current_time = time + packet_size / lan_speed
            successful_transmission += 1

        update_queue_time(node_list, current_time)

    efficiency = successful_transmission / attempted_transmission
    throughput = successful_transmission * packet_size / simulation_time
    print(efficiency, throughput, successful_transmission)

    return efficiency, throughput
  




def exponential_backoff(node_list, collision_list, current_time):
    for node in collision_list:
        node_list[node].exponential_wait(current_time)

# @param
# node_list: 
def check_collision(node_list, current_time, transmitting_nodes, propagation_time):
    if len(transmitting_nodes) > 1:
        return True, transmitting_nodes
        
    node = transmitting_nodes[0]
    collision_list = [node]
    for i in range(len(node_list)):
        if (i != node):
            propagation_time_final = abs(node - i) * propagation_time
            output_time = node_list[i].check_queue()
            if current_time + propagation_time_final > output_time:
                collision_list.append(i)

    if len(collision_list) > 1:
        return True, collision_list
    return False, collision_list


def get_arrival_time(node_list):
    min_time = 99999999
    node_num = []

    for i in range(len(node_list)):
        if node_list[i].check_queue() < min_time:
            node_num = [i]
            min_time = node_list[i].check_queue()
        elif node_list[i].check_queue() == min_time:
            node_num.append(i)
       
    return min_time, node_num

def generate_nodes(node_total, packet_size, packet_rate, simulation_time):
    node_list = []
    for _ in range(node_total):
        node_list.append(Queue_2(packet_size, packet_rate, simulation_time))
    return node_list

def simulationNotOver(current_time, simulation_time):
    return current_time <= simulation_time

def update_queue_time(node_list, current_time):
    for node in node_list:
        node.update_queue_time(current_time)

def time_after_collision(collision_list, current_time, propagation_time):
    max_propagation_time = 0
    for node in collision_list:
        for node_2 in collision_list:
            max(abs(node - node_2) * propagation_time, max_propagation_time)
    return current_time + max_propagation_time

NODE_NUM = [20,40,60,80,100]
PACKET_RATE = [5, 7, 10, 12 ,20]
LAN_SPEED = 1e6
PACKET_SIZE = 1500
NODE_DISTANCE = 10
PROPAGATION_SPEED = (2/3) * 3e8

efficiency = [[],[],[], [], []]
throughput = [[],[],[], [], []]

for i in NODE_NUM:
    for j in range(len(PACKET_RATE)):
        print(f'Starting Simulation with NODE_NUM: {i} and PACKET_RATE: {PACKET_RATE[j]}')
        efficiency_output, throughput_output = start_persistent_simulation(i, PACKET_RATE[j], LAN_SPEED, PACKET_SIZE, NODE_DISTANCE, PROPAGATION_SPEED, 1000)
        efficiency[j].append(efficiency_output)
        throughput[j].append(throughput_output)

# Store data into file as backup
f = open("efficiency", "w")
string1 = repr(efficiency)
f.write(string1)
f.close()

f = open("throughput", "w")
string1 = repr(throughput)
f.write(string1)
f.close()

plt.plot(NODE_NUM, efficiency[0])
plt.plot(NODE_NUM, efficiency[1])
plt.plot(NODE_NUM, efficiency[2])
plt.plot(NODE_NUM, throughput[0])
plt.plot(NODE_NUM, throughput[1])
plt.plot(NODE_NUM, throughput[2])

# plt.xlabel("Traffic intensity, p")
# plt.ylabel("Fraction of packets loss, p_loss")
# plt.title(f'Packets Loss vs Traffic Intensity')
# plt.legend(["10 - 1000T","25 - 1000T","50 - 1000T", "10 - 2000T","25 - 2000T","50 - 2000T"])

plt.show()
