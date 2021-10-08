import matplotlib.pyplot as plt
import threading
import time
import math
import heapq

from ece358_lab1_functions import simulate_thread


# For question 3
def simulate_question_3():
    print("----- Q3 Simulation Initiated -----")
    start_time = time.time()

    packet_rates = {"init" : 25, "end" : 105, "increment" : 10}
    parameters = {"packet_rates" : packet_rates, "packet_size" : 2000, "transmission_rate" : 1e6}
    buffer_size = -1
    simulation_time = 1000

    # List of p steps
    list_x = []
    thread_list = []
    list_counter = 0
    final_average = []
    final_idle = []
    for packet_rate in range(packet_rates["init"], packet_rates["end"], packet_rates["increment"]):
        packet_rate = packet_rate / 100
        list_x.append(packet_rate)
        t = threading.Thread(target=simulate_thread, args=(parameters, packet_rate, buffer_size, simulation_time, final_average, final_idle, []))
        thread_list.append(t)
        list_counter += 1

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    heapq.heapify(final_average)
    heapq.heapify(final_idle)

    final_average_list = []
    final_idle_list = []

    for _ in range(len(final_average)):
        average = heapq.heappop(final_average)
        idle = heapq.heappop(final_idle)
        final_average_list.append(average[1])
        final_idle_list.append(idle[1])

    # Plot the graphs
    plt.plot(list_x, final_average_list)
    plt.xlabel("Traffic intensity, p")
    plt.ylabel("Average number of packets, E[N]")
    plt.title(f'Average # of Packets vs Traffic Intensity')
    plt.show()

    plt.plot(list_x, final_idle_list)
    plt.xlabel("p")
    plt.ylabel("P_idle")
    plt.title("P_idle vs Traffic Intensity")
    plt.show()
    current_time = time.time() - start_time
    minutes = math.floor(current_time / 60)
    seconds = current_time % 60

    print(f'It has been {minutes}m {seconds}s')
    print("----- Q3 Simulation Terminated -----")


simulate_question_3()
