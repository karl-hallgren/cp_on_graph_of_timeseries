#!/usr/bin/env python3

import pandas as pd
import pickle


path = 'cyber_application/'

red_users = pd.read_csv(path+'data/red_users.csv')
red_users = red_users['0'].values.tolist()


files = []

for wind in ['nw', 'uw']:
    files += ['auth_weekly_' + wind + '_part' + str(i).zfill(2) for i in range(0, 7)]

results = {}

for file in files:
    source_file = open(path+'results/' + file, "rb")
    res = pickle.load(source_file)
    source_file.close()
    window = [k for k in res.keys() if k not in ['nodes', 'edges']][0] #   list(res.keys())[-1]
    if window not in results.keys():
        results[window] = {}
    logit_p_s = list(res[window].keys())
    lambdas_s = list(res[window][logit_p_s[0]].keys())
    for logit_p in logit_p_s:
        if logit_p not in results.keys():
            results[window][logit_p] = {}
        for lambdas in lambdas_s:
            if lambdas not in results[window][logit_p].keys():
                results[window][logit_p][lambdas] = {}
            results[window][logit_p][lambdas] = res[window][logit_p][lambdas]

source_file = open(path+'results/' + files[0], "rb")
res = pickle.load(source_file)
source_file.close()
E = res['edges']
nodes = res['nodes']


windows = list(results.keys())
logit_p_s = list(results[windows[0]].keys())
lambdas_s = list(results[windows[0]][logit_p_s[0]].keys())
lambdas_s.sort()
L = len(results[windows[0]][logit_p_s[0]][lambdas_s[0]])


pd.Series(logit_p_s).to_csv(path + 'results/logit_p_s.csv', index=False)



# average number of changepoints

for window in windows:

    num_cp = {'red': [], 'notred': [], 'all': []}

    for logit_p in logit_p_s:
        num_cp['red'] += [[]]
        num_cp['notred'] += [[]]
        num_cp['all'] += [[]]
        for lambdas in lambdas_s:
            num_cp['red'][-1] += [[]]
            num_cp['notred'][-1] += [[]]
            num_cp['all'][-1] += [[]]

            num_cp['all'][-1][-1] = [len(results[window][logit_p][lambdas][i]) for i in range(L)]
            num_cp['all'][-1][-1] = sum(num_cp['all'][-1][-1]) / len(num_cp['all'][-1][-1])

            num_cp['red'][-1][-1] = [len(results[window][logit_p][lambdas][i]) for i in range(L) if nodes[i] in red_users]
            num_cp['red'][-1][-1] = sum(num_cp['red'][-1][-1]) / len(num_cp['red'][-1][-1])

            num_cp['notred'][-1][-1] = [len(results[window][logit_p][lambdas][i]) for i in range(L) if nodes[i] not in red_users]
            num_cp['notred'][-1][-1] = sum(num_cp['notred'][-1][-1]) / len(num_cp['notred'][-1][-1])

    if window is None:
        wind = 'nw'
    elif window < 0:
        wind = 'uw'
    else:
        wind = 'fw' + str(window)

    for type_i in ['all', 'red', 'notred']:
        pd.DataFrame(num_cp[type_i]).to_csv(path+'results/num_cp_' + type_i + '_' + wind + '.csv', index=False)


# degrees

E = set([tuple(e) for e in E])

degree_all = []
for i in range(len(nodes)):
    degree_all += [0]
    for j in range(len(nodes)):
        if i != j:
            if (i, j) in E or (j, i) in E:
                degree_all[-1] += 1


pd.DataFrame([[nodes[i], nodes[i] in red_users, degree_all[i]] for i in range(len(nodes.tolist()))]).to_csv(path + 'results/nodes.csv', index=False)



# n_i


ni_d = {window: [] for window in windows}

for window in windows:
    for logit_p in logit_p_s[:]:
        ni_d[window] += [[]]
        for lambdas in lambdas_s[:]:
            ni_d[window][-1] += [[]]
            for i in range(L):
                print(i)
                ni_i = []
                for tau in results[window][logit_p][lambdas][i]:
                    ni_i_t = 0
                    for j in range(L):
                        if j != i:
                            if (i, j) in E or (j, i) in E:
                                tau_j = set(results[window][logit_p][lambdas][j])
                                tau_i = set([tau + w for w in range(-12, 13)])
                                if len(tau_i.intersection(tau_j)) > 0:
                                    ni_i_t += 1
                    ni_i += [ni_i_t]
                ni_d[window][-1][-1] += [ni_i[:]]



# sum ni deg d

for window in windows:

    sum_ni_d = {'red': [], 'notred': [], 'all': []}

    for p in range(len(logit_p_s[:])):
        sum_ni_d['red'] += [[]]
        sum_ni_d['notred'] += [[]]
        sum_ni_d['all'] += [[]]
        for la in range(len(lambdas_s[:])):
            sum_ni_d['red'][-1] += [[]]
            sum_ni_d['notred'][-1] += [[]]
            sum_ni_d['all'][-1] += [[]]

            sum_ni_all = [(sum(ni_d[window][p][la][i])+1)/(degree_all[i]+1) for i in range(L) if len(ni_d[window][p][la][i]) > 0]
            sum_ni_d['all'][-1][-1] = sum(sum_ni_all) / len(sum_ni_all)

            sum_ni_red = [(sum(ni_d[window][p][la][i])+1) / (degree_all[i]+1) for i in range(L) if len(ni_d[window][p][la][i]) > 0 and nodes[i] in red_users]
            sum_ni_d['red'][-1][-1] = sum(sum_ni_red) / len(sum_ni_red)

            sum_ni_nred = [(sum(ni_d[window][p][la][i])+1) / (degree_all[i]+1) for i in range(L) if len(ni_d[window][p][la][i]) > 0 and nodes[i] not in red_users]
            sum_ni_d['notred'][-1][-1] = sum(sum_ni_nred) / len(sum_ni_nred)


    if window is None:
        wind = 'nw'
    elif window < 0:
        wind = 'uw'
    else:
        wind = 'fw' + str(window)

    for type_i in ['all', 'red', 'notred']:
        pd.DataFrame(sum_ni_d[type_i]).to_csv(path+'results/sum_ni_dd_' + type_i + '_' + wind + '.csv', index = False)



