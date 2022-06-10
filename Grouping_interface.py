from os import path
from Grouping import Proposal, Comparison
from bench import benchmark
import numpy as np
import copy


this_path = path.realpath(__file__)
Dim = 2000
trail = 1

Gene_len = 9
pop_size = 5

for func_num in [5]:
    print("In function: " + str(func_num))
    bench = benchmark.Function(func_num)
    func = bench.get_func()
    scale_range = bench.get_info()

    intercept = func(np.zeros(Dim))

    DG_file_path = path.dirname(this_path) + '/Data/Groups/DG/f' + str(func_num) + '.txt'
    DG_cost_path = path.dirname(this_path) + '/Data/cost/DG/f' + str(func_num) + '.txt'

    for t in range(trail):
        print('    In trail: ', t)
        DG_groups, DG_cost = Comparison.DECC_DG(func, Dim)

        with open(DG_file_path, 'a+') as f:
            f.write(str(DG_groups) + ', \n')
            f.close()

        with open(DG_cost_path, 'a+') as f:
            f.write(str(DG_cost) + ', \n')
            f.close()

