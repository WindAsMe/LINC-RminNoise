import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu


def Normalization(Matrix):
    max_len = 0
    for v in Matrix:
        max_len = max(max_len, len(v))
    for v in Matrix:
        while len(v) < max_len:
            value = v[0]
            v.insert(0, value)
    return Matrix


def draw_convergence(x_CCVIL, CCVIL_obj, x_D, D_obj, x_G, G_obj, x_DG, DG_obj, x_Proposal, Proposal_obj, f, p_value, move):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.semilogy(x_D, D_obj, label='DECC-D', linestyle=':', color='plum')
    plt.semilogy(x_CCVIL, CCVIL_obj, label='DECCVIL', linestyle=':', color='lightgreen')
    plt.semilogy(x_G, G_obj, label='DECC-G', linestyle=':', color='aqua')
    plt.semilogy(x_DG, DG_obj, label='DECC-DG', linestyle=':', color='grey')
    plt.semilogy(x_Proposal, Proposal_obj, label='DECC-LINC-Rmin', color='red')

    # plt.plot(x_D, D_obj, label='DECC-D', linestyle=':', color='plum')
    # plt.plot(x_CCVIL, CCVIL_obj, label='CCVIL', linestyle=':', color='lightgreen')
    # plt.plot(x_G, G_obj, label='DECC-G', linestyle=':', color='aqua')
    # plt.plot(x_DG, DG_obj, label='DECC-DG', linestyle=':', color='grey')
    # plt.plot(x_Proposal, Proposal_obj, label='Proposal', color='red')
    font_title = {'size': 18}
    font = {'size': 16}
    plt.title('$f_' + '{' + str(f) + '}$', font_title)
    plt.xlabel('Fitness evaluation times', font)
    plt.ylabel('Fitness', font)
    plt.legend()
    if p_value < 0.05:
        if p_value < 0.01:
            plt.text(FEs, move, "**", fontdict={'size': 14, 'color': 'red'})
        else:
            plt.text(FEs, 5 * move, "*", fontdict={'size': 14, 'color': 'red'})
    plt.savefig('/Users/ISDL/PycharmProjects/MALINC-RminNoise/Data/pic/' + 'f' + str(f))
    plt.show()


def ave(array):
    result = []
    for i in range(len(array[0])):
        result.append(np.mean(array[:, i]))
    return result


def Holm(CCVIL_obj, D_obj, G_obj, DG_obj, proposal_obj, test):
    result = {'CCVIL_D': test(D_obj, CCVIL_obj)[1], 'CCVIL_G': test(CCVIL_obj, G_obj)[1], 'CCVIL_DG': test(DG_obj, CCVIL_obj)[1],
              'CCVIL_P': test(CCVIL_obj, proposal_obj)[1], 'D_G': test(D_obj, G_obj)[1], 'D_DG': test(D_obj, DG_obj)[1],
              'D_P': test(D_obj, proposal_obj)[1], 'G_DG': test(G_obj, DG_obj)[1], 'G_P': test(G_obj, proposal_obj)[1],
              'DG_P': test(DG_obj, proposal_obj)[1]}
    result = dict(sorted(result.items(), key=lambda d: d[1]))
    flag = len(result)
    for (k, v) in result.items():
        result[k] = v * flag
        flag -= 1
    return result


def final(CCVIL_obj, D_obj, G_obj, DG_obj, Proposal_obj):
    CCVIL_final = CCVIL_obj[:, len(CCVIL_obj[0]) - 1]
    D_final = D_obj[:, len(D_obj[0]) - 1]
    G_final = G_obj[:, len(G_obj[0]) - 1]
    DG_final = DG_obj[:, len(DG_obj[0]) - 1]
    Proposal_final = Proposal_obj[:, len(Proposal_obj[0])-1]
    print('CCVIL final: ', '%e' % np.mean(CCVIL_final), '±', '%e' % np.std(CCVIL_final, ddof=1))
    print('D final: ', '%e' % np.mean(D_final), '±', '%e' % np.std(D_final, ddof=1))
    print('G final: ', '%e' % np.mean(G_final), '±', '%e' % np.std(G_final, ddof=1))
    print('DG final: ', '%e' % np.mean(DG_final), '±', '%e' % np.std(DG_final, ddof=1))
    print('Proposal final: ', '%e' % np.mean(Proposal_final), '±', '%e' % np.std(Proposal_final, ddof=1))
    return CCVIL_final, D_final, G_final, DG_final, Proposal_final


if __name__ == '__main__':
    f = 1
    FEs = 3000000
    CCVIL_cost = [4104, 4480, 4188, 4574, 4524, 4580, 4618, 4230, 4330, 4106, 4462, 4944, 4516, 4240, 4114]
    DG_cost = [3972, 3972, 3974, 3972, 3972, 3972, 3972, 3972, 3972, 3972, 3972, 3972, 3972, 3972, 3972]

    Proposal_cost = [470995, 480525, 475520, 477400, 478255, 478380, 483555, 479285, 478945, 476705, 482410, 482540,
                     484530, 480280, 483140]

    move = 0.5 * 10e11

    CCVIL_obj = []
    D_obj = []
    DG_obj = []
    G_obj = []
    Proposal_obj = []

    CCVIL_obj = np.array(Normalization(CCVIL_obj))
    D_obj = np.array(Normalization(D_obj))
    DG_obj = np.array(Normalization(DG_obj))
    G_obj = np.array(Normalization(G_obj))
    Proposal_obj = np.array(Normalization(Proposal_obj))

    CCVIL_obj_ave = ave(CCVIL_obj)
    D_obj_ave = ave(D_obj)
    G_obj_ave = ave(G_obj)
    DG_obj_ave = ave(DG_obj)
    Proposal_obj_ave = ave(Proposal_obj)

    CCVIL_final, D_final, G_final, DG_final, Proposal_final = final(CCVIL_obj, D_obj, G_obj, DG_obj, Proposal_obj)
    result = Holm(CCVIL_final, D_final, G_final, DG_final, Proposal_final, mannwhitneyu)

    x_CCVIL = np.linspace(CCVIL_cost[f-1], FEs, len(CCVIL_obj_ave))
    x_D = np.linspace(30000, FEs, len(D_obj_ave))
    x_G = np.linspace(0, FEs, len(G_obj_ave))
    x_DG = np.linspace(DG_cost[f-1], FEs, len(DG_obj_ave))
    x_Proposal = np.linspace(Proposal_cost[f-1], FEs, len(Proposal_obj_ave))

    print(result)
    p_value = 0.001
    draw_convergence(x_CCVIL, CCVIL_obj_ave, x_D, D_obj_ave, x_G, G_obj_ave, x_DG, DG_obj_ave, x_Proposal,
                     Proposal_obj_ave, f, p_value, move)
