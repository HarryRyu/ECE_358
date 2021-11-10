from ece358_lab2_classes import Queue
import matplotlib.pyplot as plt


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
    while (current_time <= simulation_time):


        
        min_packet_arrival_time, node_num = get_arrival_time(node_list, current_time)
        # print(f'Current Time: {current_time}, Min Arrival Time: { min_packet_arrival_time}')
        # for i in range(len(node_list)):
        #     x = node_list[i].check_queue()
        #     y = min_packet_arrival_time + abs(node_num[0] - i) * node_distance / propagation_speed
        #     print(f'{i}. {x}, {y}')
        
        current_time = min_packet_arrival_time
        attempted_transmission += 1

        collision_detected = False

        if len(node_num) == 1:
            if node_list[node_num[0]].check_queue() < current_time:
                collision_detected, node_num = False, node_num[0]
            else:
                # print("HELLO")
                collision_detected, node_num = check_collision(node_list, current_time, node_num[0], node_distance / propagation_speed)
        else:
            collision_detected, node_num = True, node_num
        

        if collision_detected:
            exponential_backoff(node_list, node_num, current_time)
        else:
            time = node_list[node_num].pop_queue()

            if time < current_time:
                current_time += packet_size / lan_speed
            else:
                current_time = time + packet_size / lan_speed

            successful_transmission += 1

    efficiency = successful_transmission / attempted_transmission
    throughput = successful_transmission * packet_size / simulation_time
    ##print(efficiency, throughput, successful_transmission)

    return efficiency, throughput




        



        




def exponential_backoff(node_list, node, current_time):
    for i in range(len(node)):
        node_list[node[i]].exponential_wait(current_time)


def check_collision(node_list, time, node, propagation_time):
    for i in range(len(node_list)):
        if (i != node):
            propagation_time_final = abs(node - i) * propagation_time
            output_time = node_list[i].check_queue()
            if (time + propagation_time_final > output_time and output_time > 0):
                return True, [node, i]
    return False, node



def get_arrival_time(node_list, current_time):
    min_time = 99999999
    end_after = False
    node_num = []

    output_time_list = []
    for i in range(len(node_list)):
        output_time_list.append(node_list[i].check_queue())

    for i in range(len(output_time_list)):
        if output_time_list[i] <= current_time and output_time_list[i] > 0:
            node_num.append(i)
            end_after = True
    
    if end_after:
        return current_time, node_num

    for i in range(len(output_time_list)):
        if output_time_list[i] > current_time and output_time_list[i] <= min_time:
            node_num = [i]
            min_time = output_time_list[i]

    return min_time, node_num

NODE_NUM = [20,40,60,80,100]
PACKET_RATE = [5, 7, 10, 12 ,20]
LAN_SPEED = 1e6
PACKET_SIZE = 1500
NODE_DISTANCE = 10
PROPAGATION_SPEED = (2/3) * 3e8

efficiency = [[],[],[]]
throughput = [[],[],[]]

# for i in NODE_NUM:
#     for j in range(len(PACKET_RATE)):
#         print(f'Starting Simulation with NODE_NUM: {i} and PACKET_RATE: {PACKET_RATE[j]}')
#         efficiency_output, throughput_output = start_persistent_simulation(i, PACKET_RATE[j], LAN_SPEED, PACKET_SIZE, NODE_DISTANCE, PROPAGATION_SPEED)
#         efficiency[j].append(efficiency_output)
#         throughput[j].append(throughput_output)

# # Store data into file as backup
# f = open("efficiency", "w")
# string1 = repr(efficiency)
# f.write(string1)
# f.close()

# f = open("throughput", "w")
# string1 = repr(throughput)
# f.write(string1)
# f.close()

# plt.plot(NODE_NUM, efficiency[0])
# plt.plot(NODE_NUM, efficiency[1])
# plt.plot(NODE_NUM, efficiency[2])
# plt.plot(NODE_NUM, throughput[0])
# plt.plot(NODE_NUM, throughput[1])
# plt.plot(NODE_NUM, throughput[2])

# # plt.xlabel("Traffic intensity, p")
# # plt.ylabel("Fraction of packets loss, p_loss")
# # plt.title(f'Packets Loss vs Traffic Intensity')
# # plt.legend(["10 - 1000T","25 - 1000T","50 - 1000T", "10 - 2000T","25 - 2000T","50 - 2000T"])

# plt.show()


y_1 = [0.9646866552656259, 0.8632075617164973, 0.7181624959966021, 0.5537502131992552, 0.45454243224332486]
y_2 = [0.9282148799619682, 0.7412752007989264, 0.5109828145690546, 0.4217890611926145, 0.39324446266913204]
y_3 = [0.7416175397122414, 0.4552744829683698, 0.42597158459212914, 0.4073203632368688, 0.3929417984867151]

plt.plot(NODE_NUM, y_1)
plt.plot(NODE_NUM, y_2)
plt.plot(NODE_NUM, y_3)

plt.show()


 







