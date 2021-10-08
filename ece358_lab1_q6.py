import math
import matplotlib.pyplot as plt
import time
import threading
import heapq

from ece358_lab1_functions import simulate_buffer


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
        thread_list.append(threading.Thread(target=simulate_buffer, args=(final_average[j], final_loss[j], parameters, buffer_size[j])))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
    
    for i in range(len(final_average)):
        heapq.heapify(final_average[i][0])
        heapq.heapify(final_loss[i][0])
        heapq.heapify(final_average[i][1])
        heapq.heapify(final_loss[i][1])

    final_average_list_1 = []
    final_loss_list_1 = []
    final_average_list_2 = []
    final_loss_list_2 = []
    for _ in buffer_size:
        final_average_list_1.append([])
        final_loss_list_1.append([])
        final_average_list_2.append([])
        final_loss_list_2.append([])

    
    # Store data into file as backup
    f = open(f'ECE356_Q6_Average_Output', "w")
    string1 = repr(final_average)
    f.write(string1)
    f.close()

    f = open(f'ECE3568_Q6_Loss_Output', "w")
    string1 = repr(final_loss)
    f.write(string1)
    f.close()

    Average_Output_Plot(final_average)
    Loss_Output_Plot(final_loss)

    current_time = time.time() - start_time
    minutes = math.floor(current_time / 60)
    seconds = current_time % 60

    print(f'It has been {minutes}m {seconds}s')
    print("----- Q6 Simulation Terminated -----")

def Average_Output_Plot(average_data):
    simulation_1000_10_data = []
    simulation_1000_25_data = []
    simulation_1000_50_data = []
    simulation_2000_10_data = []
    simulation_2000_25_data = []
    simulation_2000_50_data = []

    heapq.heapify(average_data[0][0])
    heapq.heapify(average_data[0][1])
    heapq.heapify(average_data[1][0])
    heapq.heapify(average_data[1][1])
    heapq.heapify(average_data[2][0])
    heapq.heapify(average_data[2][1])


    size = len(average_data[0][0])

    for _ in range(size):
        simulation_1000_10_data.append(heapq.heappop(average_data[0][0])[0][1])
        simulation_1000_25_data.append(heapq.heappop(average_data[1][0])[0][1])
        simulation_1000_50_data.append(heapq.heappop(average_data[2][0])[0][1])
        simulation_2000_10_data.append(heapq.heappop(average_data[0][1])[0][1])
        simulation_2000_25_data.append(heapq.heappop(average_data[1][1])[0][1])
        simulation_2000_50_data.append(heapq.heappop(average_data[2][1])[0][1])
        

    list_x = []
    for packet_rate in range(50, 160, 10):
        list_x.append(packet_rate / 100)

    # Plot the graphs
    plt.plot(list_x, simulation_1000_10_data)
    plt.plot(list_x, simulation_1000_25_data)
    plt.plot(list_x, simulation_1000_50_data)
    plt.plot(list_x, simulation_2000_10_data)
    plt.plot(list_x, simulation_2000_25_data)
    plt.plot(list_x, simulation_2000_50_data)
    plt.xlabel("Traffic intensity, p")
    plt.ylabel("Average number of packets, E[N]")
    plt.title(f'Average # of Packets vs Traffic Intensity')
    plt.legend(["10 - 1000T","25 - 1000T","50 - 1000T", "10 - 2000T","25 - 2000T","50 - 2000T"])

    plt.show()

def Loss_Output_Plot(average_data):
    simulation_1000_10_data = []
    simulation_1000_25_data = []
    simulation_1000_50_data = []
    simulation_2000_10_data = []
    simulation_2000_25_data = []
    simulation_2000_50_data = []

    heapq.heapify(average_data[0][0])
    heapq.heapify(average_data[0][1])
    heapq.heapify(average_data[1][0])
    heapq.heapify(average_data[1][1])
    heapq.heapify(average_data[2][0])
    heapq.heapify(average_data[2][1])


    size = len(average_data[0][0])

    for _ in range(size):
        simulation_1000_10_data.append(heapq.heappop(average_data[0][0])[0][1])
        simulation_1000_25_data.append(heapq.heappop(average_data[1][0])[0][1])
        simulation_1000_50_data.append(heapq.heappop(average_data[2][0])[0][1])
        simulation_2000_10_data.append(heapq.heappop(average_data[0][1])[0][1])
        simulation_2000_25_data.append(heapq.heappop(average_data[1][1])[0][1])
        simulation_2000_50_data.append(heapq.heappop(average_data[2][1])[0][1])
        

    list_x = []
    for packet_rate in range(50, 160, 10):
        list_x.append(packet_rate / 100)

    # Plot the graphs
    plt.plot(list_x, simulation_1000_10_data)
    plt.plot(list_x, simulation_1000_25_data)
    plt.plot(list_x, simulation_1000_50_data)
    plt.plot(list_x, simulation_2000_10_data)
    plt.plot(list_x, simulation_2000_25_data)
    plt.plot(list_x, simulation_2000_50_data)
    plt.xlabel("Traffic intensity, p")
    plt.ylabel("Fraction of packets loss, p_loss")
    plt.title(f'Packets Loss vs Traffic Intensity')
    plt.legend(["10 - 1000T","25 - 1000T","50 - 1000T", "10 - 2000T","25 - 2000T","50 - 2000T"])

    plt.show()

simulate_question_6()
