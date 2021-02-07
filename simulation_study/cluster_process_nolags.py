#!/usr/bin/env python3

"""
process output from simulations with cluster structures with no lags
"""


# import relevant modules and functions

import pickle
import pandas as pd


folder = 'simulation_study/simulations_cluster_results/'

theta_1_2_s = [1040, 1045, 1050, 1055, 1060]
res_table = {}
for j in range(len(theta_1_2_s)):
    source_file = open(folder+"simulation_cluster_part0" + str(j) + "_results.pkl", "rb")
    res_table_ = pickle.load(source_file)
    source_file.close()
    res_table[theta_1_2_s[j]] = res_table_[theta_1_2_s[j]]


logit_p_s = [-i for i in range(60, 140, 10)]
lambdas_s = [0, 0.2, 0.4, 0.6, 0.8]

graph_type = ['rchain', 'lattice']

theta_1_2_s = [1040, 1045, 1050, 1055, 1060]


# print for plot in R...

pd.Series(graph_type).to_csv(folder+'simulation_clust_graph_type.csv')
pd.Series(theta_1_2_s).to_csv(folder+'simulation_clust_thetas.csv')
pd.Series(logit_p_s).to_csv(folder+'simulation_clust_logits.csv')
pd.Series(lambdas_s).to_csv(folder+'simulation_clust_lambdas.csv')


# print for R plotting..
for theta_1_2 in theta_1_2_s:
    for graph in graph_type:
        for cluster in range(4):
            to_print = pd.DataFrame([[ res_table[theta_1_2][0][graph]['no'][logit_p][lambdas][cluster][1] for lambdas in lambdas_s] for logit_p in logit_p_s])
            to_print.to_csv(folder+'simulation_cluster_res_' + str(theta_1_2) + '_graph_'+ graph + '_cluster_'+ str(cluster) + '.csv')




theta_1_2_s = [1050]
res_table = {}

source_file = open(folder+"simulation_cluster_part11_results.pkl", "rb")
res_table_ = pickle.load(source_file)
source_file.close()
res_table[theta_1_2_s[0]] = res_table_[theta_1_2_s[0]]

# print for R plotting..
for theta_1_2 in theta_1_2_s:
    for graph in graph_type:
        for cluster in range(4):
            to_print = pd.DataFrame([[ res_table[theta_1_2][0][graph]['no'][logit_p][lambdas][cluster][1] for lambdas in lambdas_s] for logit_p in logit_p_s])
            to_print.to_csv(folder+'simulation_cluster_res_' + str(theta_1_2) + '_graph_'+ graph + '_cluster_'+ str(cluster) + '_no_delta.csv')




