"""
functions for simulation study
"""


import numpy as np
import time
import copy
import pickle

from model_and_sampler.changepoint_model import ChangepointModel
from model_and_sampler.mcmc_sampler import MCMCsampler


def run_experiment_star_structure(file_name_output, theta_1_2_s):


    # experiment options
    L = 30
    T = 300
    tau = 200
    distr = ['Poisson'] * L
    hyper = [[100, 0.1]] * L
    theta_base = 1000
    theta_large = 1150
    C2_card_s = [0, 9, 18, 27]
    logit_p_s = [-i for i in range(60, 140, 10)]
    lambdas_s = [0, 0.2, 0.4, 0.6, 0.8]
    nrep = 10
    seed = 267

    time_begin_all = time.time()

    np.random.seed(seed)

    num_simulations = 0

    # store results
    res_table = {}
    for theta_1_2 in theta_1_2_s:
        res_table[theta_1_2] = {}
        for C2_card in C2_card_s:
            res_table[theta_1_2][C2_card] = {}
            for logit_p in logit_p_s:
                res_table[theta_1_2][C2_card][logit_p] = {}
                for lambdas in lambdas_s:
                    res_table[theta_1_2][C2_card][logit_p][lambdas] = {0: 0.,  # post prob 0 for main
                                                                       1: 0.,  # post prob 1 for main
                                                                       2: 0,  # post prob 1 for secondary
                                                                       3: 0   # post prob 0 for N
                                                                       }
    # run simulations
    for rep in range(nrep):
        for theta_1_2 in theta_1_2_s:
            cp_1 = ChangepointModel(x_distr=distr[:1], x_hyper=hyper[:1], ltau=[[tau]], L=1, T=T)
            cp_1.sample_data([[theta_base, theta_1_2]])   # for more accurate comparisons, sample first time series here
            for C2_card in C2_card_s:
                C_1 = [0]
                C_2 = np.random.choice(range(1, L), C2_card, replace=False).tolist()
                C_2.sort()

                ltau = [[tau] if i in C_1 + C_2 else [] for i in range(L)]
                d = [[0] if len(ltau[i]) > 0 else [] for i in range(L)]
                theta = [[theta_base, theta_1_2] if i in C_1 else [theta_base, theta_large] if i in C_2 else [theta_base] for i in range(L)]

                cp = ChangepointModel(x_distr=distr, x_hyper=hyper, ltau=ltau, d=d, L=L, T=T)
                cp.sample_data(theta)
                cp.x[0] = copy.copy(cp_1.x[0])

                for logit_p in logit_p_s:
                    for lambdas in lambdas_s:
                        delta_hyper = None  # if lambdas == 0 else [0.5, 1, 50]
                        cp.interaction_parameters('star', -logit_p * lambdas / (L-1) if lambdas > 0 else None, hyper_param=None, zeta=None)
                        lambdas_ = cp.lambdas

                        mcmc = MCMCsampler(x=cp.x, x_distr=distr, x_hyper=hyper, logit_p=logit_p, lambdas=lambdas_, delta_hyper=delta_hyper)
                        time_begin_sample = time.time()
                        mcmc.run(num_iter=50000, burn_in=20000, thinning=10, move_prob=None)
                        #mcmc.run(num_iter=50, burn_in=10, thinning=1, move_prob=None)
                        time_end_sample = time.time()
                        print(num_simulations, ' in ', time_end_sample-time_begin_sample)

                        num_simulations += 1
                        mcmc.post_distr()

                        res_table[theta_1_2][C2_card][logit_p][lambdas][0] += mcmc.post_distr_k[0][0]/nrep if 0 in mcmc.post_distr_k[0].keys() else 0
                        res_table[theta_1_2][C2_card][logit_p][lambdas][1] += mcmc.post_distr_k[0][1]/nrep if 1 in mcmc.post_distr_k[0].keys() else 0
                        if len(C_2) > 0:
                            res_table[theta_1_2][C2_card][logit_p][lambdas][2] += np.average([mcmc.post_distr_k[i][1] if 1 in mcmc.post_distr_k[i].keys() else 0 for i in C_2])/nrep
                        res_table[theta_1_2][C2_card][logit_p][lambdas][3] += np.average([mcmc.post_distr_k[i][0] if 0 in mcmc.post_distr_k[i].keys() else 0 for i in np.setdiff1d(range(L), C_1 + C_2)])/nrep

    # print results
    time_end_all = time.time()
    print(num_simulations, ' simulations in ', (time_end_all - time_begin_all)/60)
    dump_file = open('simulation_study/simulations_star_results/' + file_name_output, "wb")
    pickle.dump(res_table, dump_file)
    dump_file.close()

    return res_table


def run_experiment_cluster_detection(file_name_output, seed, theta_1_2_s, graph_type, lag_mode, window_type, nrep, fixed_lag=None, delta_on=1):
    # parameters for the experiment
    L = 30
    T = 300
    tau = 200
    distr = ['Poisson'] * L
    hyper = [[100, 0.1]] * L
    theta_base = 1000
    logit_p_s = [-i for i in range(60, 140, 10)]
    lambdas_s = [0, 0.2, 0.4, 0.6, 0.8]
    cluster_s = [list(range(6)), [16, 17, 22, 23, 28, 29], [12]]


    # initialise
    time_begin_all = time.time()

    #np.random.seed(seed)

    num_simulations = 0

    if cluster_s is None:
        C_1 = list(range(6))
        C_2 = [15, 16, 17, 21, 22, 23]
        C_3 = [12, 26]
        N = np.setdiff1d(range(L), C_1 + C_2 + C_3)
    else:
        C_1 = cluster_s[0]
        C_2 = cluster_s[1]
        C_3 = cluster_s[2]
        N = np.setdiff1d(range(L), C_1 + C_2 + C_3)

    print(C_2)
    # store results
    res_table = {}
    for theta_1_2 in theta_1_2_s:
        res_table[theta_1_2] = {}
        for lag in lag_mode:
            res_table[theta_1_2][lag] = {}
            for graph in graph_type:
                res_table[theta_1_2][lag][graph] = {}
                for window in window_type:
                    res_table[theta_1_2][lag][graph][window] = {}
                    for logit_p in logit_p_s:
                        res_table[theta_1_2][lag][graph][window][logit_p] = {}
                        for lambdas in lambdas_s:
                            res_table[theta_1_2][lag][graph][window][logit_p][lambdas] = {}
                            for cluster in range(4):    # C1, C2, C3, N
                                res_table[theta_1_2][lag][graph][window][logit_p][lambdas][cluster] = {0: 0.0,  # post prob k = 0
                                                                                                       1: 0.0,  # post prob k = 1
                                                                                                       'loss': {0: 0.0,     # expected loss
                                                                                                                1: []      # bayes estimate
                                                                                                                }
                                                                                                       }

    # run simulations
    for theta_1_2 in theta_1_2_s:
        for lag in lag_mode:
            ltau = [[tau] if i in C_1 + C_2 + C_3 else [] for i in range(L)]
            d = [[0] if i in C_1 + C_2 + C_3 else [] for i in range(L)]
            if lag:
                for i in range(len(C_1)):
                    d[C_1[i]][0] = [-fixed_lag, 0, fixed_lag, -fixed_lag, 0, fixed_lag][i]
                for i in range(len(C_2)):
                    d[C_2[i]][0] = [-fixed_lag, fixed_lag, 0, -fixed_lag, -fixed_lag, fixed_lag][i]
            theta = [[theta_base] if len(ltau[i]) == 0 else [theta_base, theta_1_2] for i in range(L)]

            for rep in range(nrep):
                np.random.seed(seed+rep)
                cp = ChangepointModel(x_distr=distr, x_hyper=hyper, ltau=ltau, d=d, L=L, T=T)
                cp.sample_data(theta)

                for i in range(6):      # for more accurate comparisons
                    cp.x[C_1[i]] = copy.deepcopy(cp.x[C_2[i]])

                for window in window_type:
                    for graph in graph_type:
                        for logit_p in logit_p_s:
                            for lambdas in lambdas_s:

                                if window == 'no':
                                    w = None
                                    w_hyper = None
                                elif window == 'fixed':
                                    #w = [fixed_lag*2] * L if lambdas > 0. else None
                                    w = [30] * L if lambdas > 0. else None
                                    w_hyper = None
                                else:
                                    w = [fixed_lag] * L if lambdas > 0. else None
                                    w_hyper = [[0.8, 0.90]] * L if lambdas > 0. else None  #[0.8, 0.95]

                                if delta_on:
                                    delta_hyper = None if lambdas == 0.0 else [0.5, 1, 30]
                                else:
                                    delta_hyper = None

                                cp.interaction_parameters(graph, -lambdas * logit_p / 4. if lambdas > 0 else None, hyper_param=[2 if graph == 'rchain' else 6], zeta=None)
                                lambdas_ = cp.lambdas

                                time_begin_sample = time.time()
                                mcmc = MCMCsampler(x=cp.x, x_distr=distr, x_hyper=hyper, logit_p=logit_p,
                                                   lambdas=lambdas_, w_hyper=w_hyper, delta_hyper=delta_hyper, w=w)
                                mcmc.run(num_iter=50000, burn_in=20000, thinning=10, move_prob=None)
                                #mcmc.run(num_iter=50, burn_in=10, thinning=1, move_prob=None)
                                time_end_sample = time.time()
                                print(num_simulations, ' in ', time_end_sample - time_begin_sample)

                                num_simulations += 1

                                mcmc.post_distr()

                                for cluster_index in range(4):
                                    cluster = [C_1, C_2, C_3, N][cluster_index]

                                    for i in cluster:
                                        res_table[theta_1_2][lag][graph][window][logit_p][lambdas][cluster_index][0] += \
                                            mcmc.post_distr_k[i][0] / (nrep*len(cluster)) if 0 in mcmc.post_distr_k[i].keys() else 0

                                        res_table[theta_1_2][lag][graph][window][logit_p][lambdas][cluster_index][1] += \
                                            mcmc.post_distr_k[i][1] / (nrep*len(cluster)) if 1 in mcmc.post_distr_k[i].keys() else 0

                                        res_table[theta_1_2][lag][graph][window][logit_p][lambdas][cluster_index]['loss'][0] += \
                                            mcmc.expected_loss_i(i, a=40, b=1, upper_bound=40, threshold=50, action='derive',
                                             tau_i=[cp.ltau[i][j] + cp.d[i][j] for j in range(1, len(cp.ltau[i]) - 1)])/(nrep*len(cluster))

    # print results
    time_end_all = time.time()
    print(num_simulations, ' simulations in ', (time_end_all - time_begin_all)/60)
    dump_file = open('simulation_study/simulations_cluster_results/' +file_name_output, "wb")
    pickle.dump(res_table, dump_file)
    dump_file.close()


