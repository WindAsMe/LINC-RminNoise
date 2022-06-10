from util import help_Proposal
from Grouping import DProblem
import geatpy as ea


def GA_optmize(Dim, gene_len, func, random_Pop, NIND, Max_iter, intercept):
    problem = DProblem.MyProblem(Dim, gene_len, func, random_Pop, intercept)
    algorithm = ea.soea_EGA_templet(problem, ea.Population(Encoding='BG', NIND=NIND), MAXGEN=Max_iter, logTras=0)
    solution = ea.optimize(algorithm, drawing=0, outputMsg=False, drawLog=False, saveFlag=False)
    Groups, obj = solution['Vars'][0], solution['ObjV']
    so_Groups = help_Proposal.Phen_Groups(Groups, help_Proposal.empty_groups(2 ** gene_len))

    return so_Groups, obj, problem.cost








