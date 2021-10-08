import math
import matplotlib.pyplot as plt
import time
import threading
import heapq

from ece358_lab1_functions import simlutate_buffer

# For question 6
def simulate_question_6():
    print("----- Q6 Simulation Initiated -----")
    start_time = time.time()

    packet_rates = {"init" : 50, "end" : 160, "increment" : 10}
    parameters = {"simulation_time" : 1000, "packet_rates" : packet_rates, "packet_size" : 2000, "transmission_rate" : 1e6}
    buffer_size = [10, 25, 50]

    final_average = []
    final_loss = []

    for _ in buffer_size:
        # List to store # of packets in buffer
        final_average.append([])
        # List to store percentage of idle time for buffer
        final_loss.append([])

    # List of p steps
    list_x = []
    for packet_rate in range(packet_rates["init"], packet_rates["end"], packet_rates["increment"]):
        list_x.append(packet_rate / 100)

    thread_list = []
    for j in range(len(buffer_size)):
        thread_list.append(threading.Thread(target=simlutate_buffer, args=(final_average[j], final_loss[j], parameters, buffer_size[j])))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
    
    for i in range(len(final_average)):
        heapq.heapify(final_average[i])
        heapq.heapify(final_loss[i])

    final_average_list = []
    final_loss_list = []
    for _ in buffer_size:
        final_average_list.append([])
        final_loss_list.append([])

    for i in range(len(final_average)):
        for _ in range(len(final_average[i][0])):
            average = heapq.heappop(final_average[i][0])
            idle = heapq.heappop(final_loss[i][0])
            print(final_average_list, average)
            final_average_list[i].append(average[0][1])
            final_loss_list[i].append(idle[0][1])

    # Store data into file as backup
    f = open(f'ECE318_Q6_Average_Output', "w")
    string1 = repr(final_average_list)
    f.write(string1)
    f.close()

    f = open(f'ECE318_Q6_Loss_Output', "w")
    string1 = repr(final_loss_list)
    f.write(string1)
    f.close()
        

    # Plot the graphs
    plt.plot(list_x, final_average_list[0])
    plt.plot(list_x, final_average_list[1])
    plt.plot(list_x, final_average_list[2])
    plt.xlabel("p")
    plt.ylabel("E[N]")
    plt.title(f'Average # of Packets vs Utilization of Queue')
    plt.legend(buffer_size)
    plt.show()

    plt.plot(list_x, final_loss_list[0])
    plt.plot(list_x, final_loss_list[1])
    plt.plot(list_x, final_loss_list[2])
    plt.xlabel("p")
    plt.ylabel("P_loss")
    plt.title(f'P_loss vs Utilization of Queue')
    plt.legend(buffer_size)
    plt.show()
    current_time = time.time() - start_time
    minutes = math.floor(current_time / 60)
    seconds = current_time % 60

    print(f'It has been {minutes}m {seconds}s')
    print("----- Q6 Simulation Terminated -----")

simulate_question_6()
