import numpy as np


def base_fitness(Population, func, intercept):
    fitness = []
    for indi in Population:
        fitness.append(func(indi) * (1 + np.random.normal(loc=0, scale=0.01, size=None)) - intercept)
    return fitness


def group_individual(group, individual):
    part_individual = np.zeros(len(individual))
    for element in group:
        part_individual[element] = individual[element]
    return part_individual


def groups_fitness(groups, Population, func, cost, intercept):
    fitness = []
    for indi in Population:
        indi_fitness = 0
        for group in groups:
            indi_fitness += (func(group_individual(group, indi)) * (1 + np.random.normal(loc=0, scale=0.01, size=None)) -
                             intercept)
            cost += 1
        fitness.append(indi_fitness)
    return fitness, cost


# outer interface
# opt_fitness is calculated by groups_fitness
def object_function(base_fitness, opt_fitness, group_size, epsilon=0.01):
    error = 0
    for i in range(len(base_fitness)):
        # error += (epsilon * (1 - opt_fitness[i] / base_fitness[i]) ** 2 + (1 - epsilon) / group_size)
        error += (opt_fitness[i] - base_fitness[i]) ** 2

    return error

















