import matplotlib.pyplot as plt

NODE_NUM = [20, 40, 60, 80, 100]
PACKET_RATE = [7, 10, 20]

# Convert throughput from bps to Mbps
input_throughput_list = [[204765.0, 398337.0, 572977.5, 724710.0, 839008.5], [290764.5, 551665.5, 767617.5, 906853.5, 943146.0], [558072.0, 946434.0, 941695.5, 941799.0, 943824.0]]

output_throughput_list = [[], [], []]
counter = 0

for list1 in input_throughput_list:
    for value in list1:
        output_throughput_list[counter].append(value/1e6)
    print(output_throughput_list[counter])
    counter += 1

# Throughput 2000T, non-persistent (in Mbps)
tp_2000_7 = [0.204765, 0.398337, 0.5729775, 0.72471, 0.8390085]
tp_2000_10 = [0.2907645, 0.5516655, 0.7676175, 0.9068535, 0.943146]
tp_2000_20 = [0.558072, 0.946434, 0.9416955, 0.941799, 0.943824]

# Efficiency 2000T, non-persistent
eff_2000_7 = [0.9950361175295755, 0.9757924055470225, 0.9338207971524681, 0.857651567733953, 0.7549993453439104]
eff_2000_10 = [0.9855454887485637, 0.9296453578018756, 0.8079308243422029, 0.641577772212294, 0.5269123664731136]
eff_2000_20 = [0.9040231127914916, 0.6712726344234738, 0.5996208177728536, 0.5553043770507752, 0.5247984306490504]

plt.plot(NODE_NUM, tp_2000_7)  # 7 packets/sec
plt.plot(NODE_NUM, tp_2000_10)  # 10 packets/sec
plt.plot(NODE_NUM, tp_2000_20)  # 20 packets/sec

plt.legend(["7", "10", "20"], title='Arrival rate')
plt.ylabel("Throughput (Mbps)")
plt.xlabel("Number of nodes")
plt.title('Number of nodes vs. throughput (2000T)')
plt.show()

plt.plot(NODE_NUM, eff_2000_7)  # 7 packets/sec
plt.plot(NODE_NUM, eff_2000_10)  # 10 packets/sec
plt.plot(NODE_NUM, eff_2000_20)  # 20 packets/sec

plt.legend(["7", "10", "20"], title='Arrival rate')
plt.ylabel("Efficiency")
plt.xlabel("Number of nodes")
plt.title('Number of nodes vs. efficiency (2000T)')
plt.show()
