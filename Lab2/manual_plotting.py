import matplotlib.pyplot as plt

NODE_NUM = [20, 40, 60, 80, 100]
PACKET_RATE = [7, 10, 20]

# Convert throughput from bps to Mbps
input_throughput_list = [[205047.0, 398994.75, 574416.0, 724161.75, 839378.25], [290451.75, 552635.25, 768842.25, 906786.75, 943417.5], [557603.25, 947273.25, 941876.25, 941692.5, 943925.25]]

output_throughput_list = [[], [], []]
counter = 0

for list1 in input_throughput_list:
    for value in list1:
        output_throughput_list[counter].append(value/1e6)
    print(output_throughput_list[counter])
    counter += 1

# Throughput 1000T, non-persistent (in Mbps)
tp_1000_7 = [0.204765, 0.398337, 0.5729775, 0.72471, 0.8390085]
tp_1000_10 = [0.2907645, 0.5516655, 0.7676175, 0.9068535, 0.943146]
tp_1000_20 = [0.558072, 0.946434, 0.9416955, 0.941799, 0.943824]

# Throughput 2000T, non-persistent (in Mbps)
tp_2000_7 = [0.205047, 0.39899475, 0.574416, 0.72416175, 0.83937825]
tp_2000_10 = [0.29045175, 0.55263525, 0.76884225, 0.90678675, 0.9434175]
tp_2000_20 = [0.55760325, 0.94727325, 0.94187625, 0.9416925, 0.94392525]

# Efficiency 1000T, non-persistent
eff_1000_7 = [0.9950361175295755, 0.9757924055470225, 0.9338207971524681, 0.857651567733953, 0.7549993453439104]
eff_1000_10 = [0.9855454887485637, 0.9296453578018756, 0.8079308243422029, 0.641577772212294, 0.5269123664731136]
eff_1000_20 = [0.9040231127914916, 0.6712726344234738, 0.5996208177728536, 0.5553043770507752, 0.5247984306490504]

# Efficiency 2000T, non-persistent
eff_2000_7 = [0.9949487597531151, 0.9752267156975071, 0.9329402879625794, 0.8584664681610011, 0.7551633744370034]
eff_2000_10 = [0.9860721751595843, 0.9279896728692422, 0.8067007145330354, 0.6419481513810618, 0.5258763839952374]
eff_2000_20 = [0.9031968462804697, 0.671319011149575, 0.59978259800164, 0.5547389335196027, 0.5250511360483797]

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
