import warnings
import numpy as np
from Grouping import Proposal, Comparison
from DE import DE
from cec2013lsgo.cec2013 import Benchmark
from util.help_Proposal import random_Population
from util import help_Proposal
import matplotlib.pyplot as plt
from os import path


warnings.filterwarnings("ignore")


def write_obj(data, path):
    with open(path, 'a+') as f:
        f.write(str(data) + ', ')
        f.write('\n')
        f.close()


def draw_curve(x, data, title):
    plt.plot(x, data)
    plt.title(title)
    plt.show()


if __name__ == '__main__':

    Dim = 1000
    this_path = path.realpath(__file__)
    '''
    DE parameter initialization
    '''
    NIND = 30
    FEs = 3000000
    trail = 25
    '''
    Benchmark initialization
    '''

    for func_num in range(1, 16):
        bench = Benchmark()
        info = bench.get_info(func_num)
        scale_range = [info['lower'], info['upper']]
        func = bench.get_function(func_num)
        intercept = func(np.zeros(Dim))
        CCVIL_groups, CCVIL_cost = Comparison.CCVIl(Dim, func)
        CCVIL_cost_path = path.dirname(this_path) + "/Data/cost/CCVIL/f" + str(func_num)
        write_obj(CCVIL_cost, CCVIL_cost_path)
        for i in range(trail):

            Max_iter = int((FEs - CCVIL_cost) / NIND / Dim) - 2
            var_trace, obj_trace = DE.CC(Dim, NIND, Max_iter, func, scale_range, CCVIL_groups)
            CCVIL_obj_path = path.dirname(this_path) + "/Data/obj/CCVIL/f" + str(func_num)
            write_obj(obj_trace, CCVIL_obj_path)

