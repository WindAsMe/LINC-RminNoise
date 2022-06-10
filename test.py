import copy


proposal_groups = [[1,2,3], [4,5]]
second_proposal_groups = copy.deepcopy(proposal_groups)
for group in second_proposal_groups:
    for i in range(len(group)):
        group[i] += 1000
proposal_groups.append(second_proposal_groups)