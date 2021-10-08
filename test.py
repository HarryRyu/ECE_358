import matplotlib.pyplot as plt
# Store data into file as backup
# average = open(f'ECE356_Q6_Average_Output_3', "r")
# for item in average:
    # print(len(average))
    # print(average)

# loss = open(f'ECE3568_Q6_Loss_Output_3', "r")
data = [[[[(0.5, 1.0330545599362804)], [(0.6, 1.4510693454309787)], [(0.7, 2.056437389770723)], [(0.8, 2.8134457950880676)], [(0.9, 3.720157411456056)], [(1.0, 4.542520803734524)], [(1.1, 5.273367015517864)], [(1.2, 5.894361525704809)], [(1.3, 6.454251883745964)], [(1.4, 6.793406593406593)], [(1.5, 7.160755537437152)]], [[(0.5, 1.0021713383339914)], [(0.6, 1.4668014829794405)], [(0.7, 2.0946302206188427)], [(0.8, 2.8122624778312644)], [(0.9, 3.731573649479924)], [(1.0, 4.57488986784141)], [(1.1, 5.263138883872133)], [(1.2, 5.916139110416838)], [(1.3, 6.469740189653844)], [(1.4, 6.862881283116139)], [(1.5, 7.182040151926207)]]], [[[(0.5, 1.0003987240829346)], [(0.6, 1.4871967654986522)], [(0.7, 2.358474082702388)], [(0.8, 3.7986610463674686)], [(0.9, 7.021705766279324)], [(1.0, 11.87280163599182)], [(1.1, 16.58529465426017)], [(1.2, 19.20976821192053)], [(1.3, 20.72732852539512)], [(1.4, 21.493917963224895)], [(1.5, 22.048194388508524)]], [[(0.5, 0.9896414342629483)], [(0.6, 1.4861456777833084)], [(0.7, 2.28809961794255)], [(0.8, 3.88222884090345)], [(0.9, 7.019458264234384)], [(1.0, 11.82921974522293)], [(1.1, 16.66958404764053)], [(1.2, 19.347464042392126)], [(1.3, 20.700382555470544)], [(1.4, 21.480138668207424)], [(1.5, 22.016631044616616)]]], [[[(0.5, 0.9823805794831637)], [(0.6, 1.5349148012028067)], [(0.7, 2.351290684624018)], [(0.8, 3.9952020202020204)], [(0.9, 8.516509949704789)], [(1.0, 24.50946468552819)], [(1.1, 39.63641294521786)], [(1.2, 43.91921542553192)], [(1.3, 45.73920945024989)], [(1.4, 46.46568487274807)], [(1.5, 47.011678257446526)]], [[(0.5, 0.9851720047449585)], [(0.6, 1.479026845637584)], [(0.7, 2.3348074179743223)], [(0.8, 4.01988812927284)], [(0.9, 8.690852437124416)], [(1.0, 24.77091811414392)], [(1.1, 39.13656267104543)], [(1.2, 44.092916283348664)], [(1.3, 45.68793235972329)], [(1.4, 46.549594069890574)], [(1.5, 47.01062195203421)]]]]
buffer10 = data[0]
buffer10_avg_1000 = buffer10[0]
buffer10_avg_2000 = buffer10[1]

# buffer10[0][0]
x_axis = []
y_value_dict = {}
y_val_list = []

i = 1000

for simulation_time in buffer10:
    for xvalue in simulation_time:
        x_axis.append(xvalue[0][0])
        y_val_list.append(xvalue[0][1])
    y_value_dict = {f"simulation_time_{i}": i, 'y_list': y_val_list}
    i += 1000
print('y dict is: ')
print(y_value_dict)

buffer25 = data[1]
buffer25_avg = buffer25[0]
buffer25_loss = buffer25[1]

buffer50 = data[1]
buffer50_avg = buffer50[0]
buffer150_loss = buffer50[1]

print(buffer10_avg_2000[0][0][0])
x_axis = []
buffer10_avg_y = []

for x_value in buffer10_avg_1000:
    x_axis.append(x_value[0][0])
    buffer10_avg_y.append(x_value[0][1])

buffer50_avg_y = []
for x_value in buffer50_avg:
    # x_axis.append(x_value[0][0])
    buffer50_avg_y.append(x_value[0][1])

buffer25_avg_y = []
for x_value in buffer25_avg:
    buffer25_avg_y.append(x_value[0][1])

plt.plot(x_axis, buffer10_avg_y)
plt.plot(x_axis, buffer50_avg_y)
plt.plot(x_axis, buffer25_avg_y)


plt.show()

# for i in range(len(final_average)):
#     for _ in range(len(final_average[i][0])):
#         average = heapq.heappop(final_average[i][0])[0][0]
#         idle = heapq.heappop(final_loss[i][0])[0][0]
#         average_2 = heapq.heappop(final_average[i][1])[0][0]
#         idle_2 = heapq.heappop(final_loss[i][1])[0][0]

#         final_average_list_1[i].append(average[1])
#         final_loss_list_1[i].append(idle[1])
#         final_average_list_2[i].append(average_2[1])
#         final_loss_list_2[i].append(idle_2[1])

# # Store data into file as backup
# f = open(f'ECE356_Q6_Average_Output', "w")
# string1 = repr(final_average_list_1)
# f.write(string1)
# f.close()

# f = open(f'ECE3568_Q6_Loss_Output', "w")
# string1 = repr(final_loss_list_1)
# f.write(string1)
# f.close()

# # Store data into file as backup
# f = open(f'ECE356_Q6_Average_Output_2', "w")
# string1 = repr(final_average_list_2)
# f.write(string1)
# f.close()

# f = open(f'ECE3568_Q6_Loss_Output_2', "w")
# string1 = repr(final_loss_list_2)
# f.write(string1)
# f.close()

# # Plot the graphs
# plt.plot(list_x, final_average_list_1[0])
# plt.plot(list_x, final_average_list_1[1])
# plt.plot(list_x, final_average_list_1[2])
# plt.plot(list_x, final_average_list_2[0])
# plt.plot(list_x, final_average_list_2[1])
# plt.plot(list_x, final_average_list_2[2])
# plt.xlabel("Traffic intensity, p")
# plt.ylabel("Average number of packets, E[N]")
# plt.title(f'Average # of Packets vs Traffic Intensity')
# plt.legend(buffer_size)
# plt.show()

# plt.plot(list_x, final_loss_list_1[0])
# plt.plot(list_x, final_loss_list_1[1])
# plt.plot(list_x, final_loss_list_1[2])
# plt.plot(list_x, final_loss_list_2[0])
# plt.plot(list_x, final_loss_list_2[1])
# plt.plot(list_x, final_loss_list_2[2])
# plt.xlabel("Traffic intensity, p")
# plt.ylabel("Amount of packets lost, P_loss")
# plt.title("P_loss vs Traffic Intensity")
# plt.legend(buffer_size)
# plt.show()
# current_time = time.time() - start_time
# minutes = math.floor(current_time / 60)
# seconds = current_time % 60