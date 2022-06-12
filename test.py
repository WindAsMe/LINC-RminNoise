import numpy as np
from bench import benchmark
import random


def CCDE(N):
    groups = []
    for i in range(N):
        groups.append([i])
    return groups


def DECC_G(Dim, groups_num=20, max_number=50):
    return k_s(Dim, groups_num, max_number)


def k_s(Dim, groups_num=20, max_number=50):
    groups = []
    groups_index = list(range(Dim))
    random.shuffle(groups_index)
    for i in range(groups_num):
        group = groups_index[i * max_number: (i+1) * max_number]
        groups.append(group)
    return groups


def ObjFunc(Dim, groups, func):
    intercept = func(np.zeros(Dim))
    base = func(np.ones(Dim))
    bias = (len(groups) - 1) * intercept
    total = 0
    for group in groups:
        total += Difference(Dim, group, func)
    print(np.abs(base - total + bias))


def Difference(Dim, group, func):
    index = np.zeros(Dim)
    for var in group:
        index[var] = 1
    return np.abs(func(index))


Dim = 1000
bench = benchmark.Function(1)
func = bench.get_func()
intercept = func(np.zeros(Dim))
groups_CC = CCDE(Dim)
groups_G = DECC_G(Dim, 20, 50)
ObjFunc(Dim, groups_CC, func)
ObjFunc(Dim, groups_G, func)
