import math
import random
from statistics import mean, variance

def exponential_random_var(lambd):
    uniform_random_var = random.random()
    return -1 * (1/lambd) * math.log(1 - uniform_random_var)

exponential_random_var_list = []
simulation_time = 1000
lambd = 75
for x in range(simulation_time):
    exponential_random_var_list.append(exponential_random_var(lambd))
mean_random_var = mean(exponential_random_var_list)
variance_random_var = variance(exponential_random_var_list)
mean_expected = 1 / lambd
variance_expected = 1 / lambd ** 2
print(f'Calculated Mean: {mean_random_var}, Expected Mean: {mean_expected}')
print(f'Calculated Variance: {variance_random_var}, Expected Variance: {variance_expected}')