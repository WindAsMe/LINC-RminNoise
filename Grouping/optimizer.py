import copy
import random
import numpy as np

from util import help_Proposal
from Grouping import DProblem
import geatpy as ea
from bench import benchmark
from Grouping.soea_EGA_templet import soea_EGA_templet


def MA_optmize(Dim, gene_len, func, random_Pop, NIND, Max_iter, intercept):
    i = 0
    cost = 0
    base_fitness = benchmark.base_fitness(random_Pop, func, intercept)
    problem = DProblem.MyProblem(Dim, gene_len, func, random_Pop, intercept, base_fitness)
    Encoding = 'BG'  # 编码方式
    NIND = NIND  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)
    population = ea.Population(Encoding, Field, NIND)
    population.initChrom()
    population.Phen = population.decoding()
    problem.aimFunc(population)
    current_best_Phen = None
    current_best_Obj = 0
    while i < Max_iter:
        # GA
        algorithm = soea_EGA_templet(problem, population, MAXGEN=2, logTras=0)
        solution = ea.optimize(algorithm, drawing=0, outputMsg=False, drawLog=False, saveFlag=False)
        population, best_obj, best_indi = solution['lastPop'], solution['ObjV'], solution['optPop']

        cost += problem.cost
        # Local Search
        current_best_indi, current_best_obj, LS_cost = LS(best_indi, best_obj, 5, 0.1, gene_len, random_Pop, func, intercept, base_fitness)
        cost += LS_cost

        index = np.argmin(population.ObjV)
        population.Chrom[index] = current_best_indi.Chrom[0]
        population.Phen[index] = current_best_indi.Phen[0]
        population.ObjV[index] = current_best_obj
        current_best_Phen = current_best_indi.Phen[0]
        current_best_Obj = current_best_obj
        i += 1
    MA_groups = help_Proposal.Phen_Groups(current_best_Phen, help_Proposal.empty_groups(2 ** gene_len))
    # return so_Groups, obj, cost
    return MA_groups, current_best_Obj[0], cost


def LS(best_indi, best_obj, Max_iter, rate, Gene_len, random_Pop, func, intercept, base_fitness):

    current_best_indi = best_indi.copy()
    current_best_obj = best_obj[0]
    LS_cost = 0
    for i in range(Max_iter):
        copy_best_indi = copy.deepcopy(current_best_indi)
        for index in range(len(copy_best_indi.Chrom[0])):
            if random.random() < rate:
                if copy_best_indi.Chrom[0][i] == 1:
                    copy_best_indi.Chrom[0][i] = 0
                else:
                    copy_best_indi.Chrom[0][i] = 1
        copy_best_indi.Phen = copy_best_indi.decoding()
        Empty_groups = help_Proposal.Phen_Groups(copy_best_indi.Phen[0], help_Proposal.empty_groups(2 ** Gene_len))

        groups_fitness, cost = benchmark.groups_fitness(Empty_groups, random_Pop, func, 0, intercept)
        LS_cost += cost
        obj = benchmark.object_function(base_fitness, groups_fitness)
        if obj < current_best_obj:
            current_best_indi = copy_best_indi.copy()
            current_best_obj = obj
    return current_best_indi, [current_best_obj], LS_cost














