import warnings
import numpy as np
from Grouping import Proposal, Comparison
from DE import DE
import matplotlib.pyplot as plt
from os import path
from cec2013lsgo.cec2013 import Benchmark


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
    Gene_len = 8
    Dim = 1000
    this_path = path.realpath(__file__)
    '''
    DE parameter initialization
    '''
    NIND = 30
    FEs = 3000000
    trail = 5
    '''
    Benchmark initialization
    '''

    for func_num in range(1, 16):

        bench = Benchmark()
        func = bench.get_function(func_num)
        info = bench.get_info(func_num)
        scale_range = [info["lower"], info["upper"]]

        intercept = func(np.zeros(Dim)) * (1 + np.random.normal(loc=0, scale=0.01, size=None))
        #
        # CCVIL_obj_path = path.dirname(this_path) + "/Data/obj/CCVIL/f" + str(func_num)
        # D_obj_path = path.dirname(this_path) + "/Data/obj/D/f" + str(func_num)
        # DG_obj_path = path.dirname(this_path) + "/Data/obj/DG/f" + str(func_num)
        # G_obj_path = path.dirname(this_path) + "/Data/obj/G/f" + str(func_num)
        GA_obj_path = path.dirname(this_path) + "/Data/obj/p/f" + str(func_num)

        for i in range(trail):
            # CCVIL_groups, CCVIL_cost = Comparison.CCVIl(Dim, func)
            # D_groups = Comparison.DECC_D(Dim, func, scale_range, groups_num=20, max_number=50)
            # DG_groups, DG_cost = Comparison.DECC_DG(Dim, func)
            # G_groups = Comparison.DECC_G(Dim, groups_num=20, max_number=50)
            GA_groups, GA_cost = Proposal.GALINC_Rmin(Dim, Gene_len, func, 5, scale_range, 0, intercept)

            # CCVIL_Max_iter = int((FEs - CCVIL_cost) / NIND / Dim) - 10
            # CCVIL_obj_trace = DE.CC(Dim, NIND, CCVIL_Max_iter, func, scale_range, CCVIL_groups)
            # write_obj(CCVIL_obj_trace, CCVIL_obj_path)

            # D_Max_iter = int((FEs - 30000) / NIND / Dim) - 10
            # D_obj_trace = DE.CC(Dim, NIND, D_Max_iter, func, scale_range, D_groups)
            # write_obj(D_obj_trace, D_obj_path)

            # DG_Max_iter = int((FEs - DG_cost) / NIND / Dim) - 10
            # DG_obj_trace = DE.CC(Dim, NIND, DG_Max_iter, func, scale_range, DG_groups)
            # write_obj(DG_obj_trace, DG_obj_path)
            #
            # G_Max_iter = int((FEs) / NIND / Dim) - 10
            # G_obj_trace = DE.CC(Dim, NIND, G_Max_iter, func, scale_range, G_groups)
            # write_obj(G_obj_trace, G_obj_path)
            #
            GA_Max_iter = int((FEs - GA_cost) / NIND / Dim) - 2
            GA_obj_trace = DE.CC(Dim, NIND, GA_Max_iter, func, scale_range, GA_groups)
            write_obj(GA_obj_trace, GA_obj_path)





