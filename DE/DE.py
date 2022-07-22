import geatpy as ea
import numpy as np
from util import help_DE
from DE import MyProblem, templet
from sklearn.preprocessing import MinMaxScaler


def CC(Dim, NIND, MAX_iteration, func, scale_range, groups):
    var_traces = np.zeros((MAX_iteration, Dim))
    based_population = np.zeros(Dim)
    initial_Population = help_DE.initial_population(Dim, NIND, func, groups, scale_range)
    real_iteration = 0

    while real_iteration < MAX_iteration:
        for i in range(len(groups)):
            solution = CC_Opt(func, scale_range, groups[i], based_population, initial_Population[i])

            # Dynamic Average
            # solution['lastPop'].ObjV = DynamicAverage(groups[i], based_population, solution['lastPop'].Phen,
            #                                             solution['lastPop'].ObjV, func, NIND * len(groups[i]) / 10)
            # solution['lastPop'].FitnV = ea.scaling(solution['lastPop'].ObjV)
            initial_Population[i] = solution['lastPop']
            best_index = np.argmin(solution['lastPop'].ObjV)
            best_indi = solution['lastPop'].Phen[best_index]
            for element in groups[i]:
                var_traces[real_iteration][element] = best_indi[groups[i].index(element)]
                based_population[element] = best_indi[groups[i].index(element)]
        real_iteration += 1

    obj_traces = []
    for var in var_traces:
        obj_traces.append(func(var) * (1 + np.random.normal(loc=0, scale=0.01, size=None)))

    for i in range(1, len(obj_traces)):
        if obj_traces[i] > obj_traces[i-1]:
            obj_traces[i] = obj_traces[i-1]
    return obj_traces


def CC_Opt(benchmark, scale_range, group, based_population, population):
    problem = MyProblem.CC_Problem(group, benchmark, scale_range, based_population)  # 实例化问题对象

    """===========================算法参数设置=========================="""
    myAlgorithm = templet.soea_DE_currentToBest_1_L_templet(problem, population)
    myAlgorithm.MAXGEN = 2
    myAlgorithm.drawing = 0
    """=====================调用算法模板进行种群进化====================="""
    solution = ea.optimize(myAlgorithm, verbose=False, outputMsg=False, drawLog=False, saveFlag=False)
    return solution


def DynamicAverage(group, base_pop, Phen, ObjV, func, computation):

    best_index, best_ObjV = elite_extract(ObjV, max(1, int(len(ObjV) * 0.05)))
    scaler = MinMaxScaler()
    FitV = ea.scaling(best_ObjV)
    trans_FitV = scaler.fit_transform(FitV)
    amp_FitV = amplify(trans_FitV)
    reevaluation = resourceAssign(amp_FitV, computation)

    for i in range(len(best_index)):
        obj = 0
        for time in range(int(reevaluation[i])):
            obj += func(extend(Phen[best_index[i]], base_pop, group)) * (1 + np.random.normal(loc=0, scale=0.01, size=None))
        ObjV[best_index[i]][0] = ((obj + ObjV[best_index[i]][0]) / (reevaluation[i] + 1))
    return ObjV


def elite_extract(ObjV, elite_len):
    ObjV = ObjV[:, 0]
    elite_index = np.argsort(ObjV)[0:elite_len]
    best_ObjV = []
    for i in elite_index:
        best_ObjV.append([ObjV[i]])
    return elite_index, np.array(best_ObjV)


def extend(x, base_pop, group):
    for i in range(len(group)):
        base_pop[group[i]] = x[i]
    return base_pop


def amplify(FitV):
    amp_FitV = []
    nomi = 0
    for fit in FitV:
        nomi += fit
    for fit in FitV:
        amp_FitV.append(fit / nomi)
    return amp_FitV


# Roulette allocate
def resourceAssign(amp_FitV, computational):
    allocation = [0] * len(amp_FitV)
    accumulative_P = [0]
    for i in range(1, len(amp_FitV)):
        accumulative_P.append(accumulative_P[i-1] + amp_FitV[i-1])
    i = 0
    while i < computational:
        r = np.random.rand()
        ind = locate(accumulative_P, r)
        allocation[ind] += 1
        i += 1
    return allocation


def locate(P, r):
    for i in range(len(P) - 1):
        if P[i] <= r <= P[i+1]:
            return i
    return len(P) - 1