from ece358_lab2_classes import Queue


def start_persistent_simulation(node_num, packet_rate, lan_speed, packet_size, node_distance, propagation_speed):
    # Initial simulation time
    simulation_time = 100000
    node_list = []

    attempted_transmission = 0
    successful_transmission = 0

    # Generate list of nodes with packet arrival times
    for _ in range(node_num):
        node_list.append(Queue(packet_size, packet_rate, simulation_time))


    # Start of iteration
    current_time = 0
    while (current_time <= simulation_time):
        min_packet_arrival_time, node_num = get_arrival_time(node_list, current_time)
        current_time = min_packet_arrival_time
        attempted_transmission += 1

        collision_detected = False

        if len(node_num) == 1:
            collision_detected, node_num = check_collision(node_list, current_time, node_num[0], node_distance / propagation_speed)
        else:
            collision_detected, node_num = True, node_num
        

        if collision_detected:
            exponential_backoff(node_list, node_num, current_time)
        else:
            node_list[node_num].pop_queue()
            current_time += packet_size / lan_speed
            successful_transmission += 1

    efficiency = successful_transmission / attempted_transmission
    throughput = successful_transmission * packet_size / simulation_time
    print(efficiency, throughput)

    return efficiency, throughput




        



        




def exponential_backoff(node_list, node, current_time):
    for i in range(len(node)):
        node_list[node[i]].exponential_wait(current_time)


def check_collision(node_list, time, node, propagation_time):
    for i in range(len(node_list)):
        if (i != node):
            propagation_time = abs(node - i) * propagation_time
            output_time = node_list[i].check_queue()
            if (time + propagation_time > output_time):
                return True, [node, i]
    return False, 0




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

NODE_NUM = 18
PACKET_RATE = 7
LAN_SPEED = 1e6
PACKET_SIZE = 1500
NODE_DISTANCE = 10
PROPAGATION_SPEED = (2/3) * 3e8

start_persistent_simulation(NODE_NUM, PACKET_RATE, LAN_SPEED, PACKET_SIZE, NODE_DISTANCE, PROPAGATION_SPEED)





