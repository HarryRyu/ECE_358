from statistics import mean, variance

from ece358_lab1_functions import exponential_random_var


# Create list to append all generated variables.
exponential_random_var_list = []

# Define constants.
SIMULATION_TIME = 1000
LAMBD = 75

# Iteratively call the formula, and append to list.
for x in range(SIMULATION_TIME):
    exponential_random_var_list.append(exponential_random_var(LAMBD))

# Calculate mean and variance of all elements in the list.
mean_random_var = mean(exponential_random_var_list)
variance_random_var = variance(exponential_random_var_list)

# Calculate expected mean and variance for comparison.
mean_expected = 1 / LAMBD
variance_expected = 1 / LAMBD ** 2

print(f'Calculated Mean: {mean_random_var}, Expected Mean: {mean_expected}')
print(f'Calculated Variance: {variance_random_var}, Expected Variance: {variance_expected}')
