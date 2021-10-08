# Store data into file as backup
average = open(f'ECE356_Q6_Average_Output_3', "r")
for item in average:
    # print(len(average))
    print(len(item[1]))

loss = open(f'ECE3568_Q6_Loss_Output_3', "r")

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