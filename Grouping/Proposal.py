
from util import help_Proposal
from Grouping import optimizer, Comparison


def GALINC_Rmin(Dim, Gene_len, func, pop_size, scale_range, cost, intercept):
    """
    Algorithm initialization
    """
    NIND = 20
    Max_iter = 20
    random_Pop = help_Proposal.random_Population(scale_range, Dim, pop_size)

    """
    Apply GA
    """
    Groups, obj, temp_cost = optimizer.GA_optmize(Dim, Gene_len, func, random_Pop, NIND, Max_iter, intercept)
    cost += temp_cost
    return Groups, cost
