from ece358_lab1_functions import startSimulation

def simulate_question_4():
    packet_rate = 1.2
    buffer_size = -1
    simulation_time = 1000
    parameters = {"packet_size" : 2000, "transmission_rate" : 1e6}

    [average, p_idle, p_loss] = startSimulation(parameters, packet_rate, buffer_size, simulation_time)

    print(f'E[N]: {average}\n'
          f'P_idle: {p_idle}')

simulate_question_4()