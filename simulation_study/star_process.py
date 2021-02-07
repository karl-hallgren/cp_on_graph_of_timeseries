#!/usr/bin/env python3

"""
process output from simulations with star structure
"""


# import relevant modules and functions

import pickle
import pandas as pd

folder = 'simulation_study/simulations_star_results/'

theta_1_2_s = [1030, 1040, 1050, 1060, 1070]
res_table = {}
for j in range(len(theta_1_2_s)):
    source_file = open(folder+"simulation_star_part0" + str(j) + "_results.pkl", "rb")
    res_table_ = pickle.load(source_file)
    source_file.close()
    res_table[theta_1_2_s[j]] = res_table_[theta_1_2_s[j]]


C2_card_s = [0, 9, 18, 27]
theta_1_2_s = [1030, 1040, 1050, 1060, 1070]

logit_p_s = [-i for i in range(60, 140, 10)]
lambdas_s = [0, 0.2, 0.4, 0.6, 0.8]

pd.Series(C2_card_s).to_csv(folder + 'simulation_star_C2card.csv')
pd.Series(theta_1_2_s).to_csv(folder + 'simulation_star_thetas.csv')
pd.Series(logit_p_s).to_csv(folder + 'simulation_star_logits.csv')
pd.Series(lambdas_s).to_csv(folder + 'simulation_star_lambdas.csv')

# print for R plotting..
for theta_1_2 in theta_1_2_s:
    for card in C2_card_s:
        to_print = pd.DataFrame([[res_table[theta_1_2][card][logit_p][lambdas][1] for lambdas in lambdas_s] for logit_p in logit_p_s])
        to_print.to_csv(folder + 'simulation_star_res_' + str(theta_1_2) + '_card_' + str(card) + '.csv')


