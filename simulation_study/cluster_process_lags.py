#!/usr/bin/env python3

"""
process output from simulations with cluster structures with no lags
"""


# import relevant modules and functions

import numpy as np
import time
import copy
import pickle
import pandas as pd


folder = 'simulation_study/simulations_cluster_results/'


lags = [5, 10, 15]


theta_1_2 = 1050
res_table = {theta_1_2: {}}

for lag in lags:
    res_table[theta_1_2][lag] = {}


for j in range(5, 11):
    j_text = str(j).zfill(2)
    source_file = open(folder+"simulation_cluster_part" + j_text + "_results.pkl", "rb")
    res_table_ = pickle.load(source_file)
    source_file.close()
    graph = 'rchain' if j % 2 else 'lattice'
    lag = lags[2] if j < 7 else lags[1] if j > 8 else lags[0]
    res_table[theta_1_2][lag][graph] = res_table_[theta_1_2][1][graph]




windows = ['no', 'fixed', 'unknown']

logit_p_s = [-i for i in range(60, 140, 10)]
lambdas_s = [0, 0.2, 0.4, 0.6, 0.8]

graph_type = ['rchain', 'lattice']


# print for plot in R...

pd.Series(windows).to_csv(folder+'simulation_clust_windows.csv')

# print for R plotting..
for window in windows:
    for graph in graph_type:
        for lag in lags:
            for cluster in range(4):
                to_print = pd.DataFrame([[ res_table[theta_1_2][lag][graph][window][logit_p][lambdas][cluster][1] for lambdas in lambdas_s] for logit_p in logit_p_s])
                to_print.to_csv(folder+'simulation_clusterlagged_prob1_' + window + '_graph_' + graph + '_cluster_'+ str(cluster) + '_lag_' + str(lag) + '.csv')

                to_print = pd.DataFrame([[res_table[theta_1_2][lag][graph][window][logit_p][lambdas][cluster]['loss'][0] for lambdas in lambdas_s] for logit_p in logit_p_s])
                to_print.to_csv(folder+'simulation_clusterlagged_loss_' + window + '_graph_' + graph + '_cluster_'+ str(cluster) + '_lag_' + str(lag) + '.csv')


