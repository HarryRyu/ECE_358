import math
import random
from statistics import mean, variance

exponential_random_var_list = []
simulation_time = 1000
for x in range(simulation_time):
    uniform_random_var = random.random()
    lambd = 75
    exponential_random_var_list.append(-1 * (1/lambd) * math.log(1 - uniform_random_var))
mean_random_var = mean(exponential_random_var_list)
variance_random_var = variance(exponential_random_var_list)
print(f'Mean: {mean_random_var}')
print(f'Variance: {variance_random_var}')

print('hi')
