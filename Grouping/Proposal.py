from bench import benchmark
from util import help_Proposal
from Grouping import optimizer, Comparison


def GALINC_Rmin(Dim, Gene_len, func, pop_size, scale_range, cost, intercept):
    """
    Algorithm initialization
    """
    stop_threshold = 0.1
    NIND = 20
    Max_iter = 20
    initial_groups = Comparison.CCDE(Dim)
    random_Pop = help_Proposal.random_Population(scale_range, Dim, pop_size)
    final_groups = initial_groups

    base_fitness = benchmark.base_fitness(random_Pop, func, intercept)
    cost += len(random_Pop)
    groups_fitness, cost = benchmark.groups_fitness(initial_groups, random_Pop, func, cost, intercept)
    current_best_obj = benchmark.object_function(base_fitness, groups_fitness)

    """
    Apply GA
    """
    if current_best_obj > stop_threshold:
        Groups, obj, temp_cost = optimizer.GA_optmize(Dim, Gene_len, func, random_Pop, NIND, Max_iter, intercept)
        cost += temp_cost
        if obj < current_best_obj:
            final_groups = Groups
    return final_groups, cost
