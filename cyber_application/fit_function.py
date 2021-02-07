# import relevant modules and functions

import sys
import os
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from model_and_sampler.mcmc_sampler import MCMCsampler

import numpy as np
import pandas as pd
import time
import copy

import networkx as nx


def run_fit_lanl(logit_p_s, window=None):

    path = 'cyber_application/data/'
    nodes_file = 'nodes_subnetwork.csv'
    graph_type = 'edgeset_subnetwork.csv'
    lambdas_s = [0, 0.5, 0.6, 0.7, 0.8]

    beg = time.time()

    """
    store results
    """
    results = {}
    results['nodes'] = []
    results['edges'] = []
    results[window] = {}
    for logit_p in logit_p_s:
        results[window][logit_p] = {}
        for lambdas in lambdas_s:
            results[window][logit_p][lambdas] = []
        if 0 not in lambdas_s:
            results[window][logit_p][0] = []

    # import nodes
    nodes = pd.read_csv(path + nodes_file)
    nodes = list(nodes['0'].values)
    nodes = np.array(nodes)
    results['nodes'] = nodes

    nodes_i = {nodes[i]: i for i in range(len(nodes))}

    # import data
    data = []

    for v in nodes:
        data_v = pd.read_csv(path + 'tseries/x_' + str(v) + '.csv')
        data_v = data_v.values.tolist()
        data += [copy.deepcopy(data_v)]

    data = [np.array(data[i][:720]) for i in range(len(data))]


    # edge set
    if graph_type != '':
        E = pd.read_csv(path + graph_type)
        E = E.values.tolist()

        E_sub = [[nodes_i[e[0]], nodes_i[e[1]]] for e in E if e[0] in nodes and e[1] in nodes]
        for e in E_sub:
            e.sort()

        results['edges'] = E_sub

        G = nx.Graph()
        for v in range(len(nodes)):
            G.add_node(v)
        for e in E_sub:
            G.add_edge(e[0], e[1])
        degree_average = sum([d[1] for d in G.degree]) / len([d[1] for d in G.degree])
        #degree_max = max([d[1] for d in G.degree])


    L = len(data)
    T = len(data[0])
    hyper = [[[1] * len(i[0])] for i in data]
    distr = ['Multinomial'] * L

    if window is None:
        w = None
        w_hyper = None
    elif window < 0:
        w = [5] * L
        w_hyper = [[0.8, 0.95]] * L
    else:
        w = [window] * L
        w_hyper = None


    for logit_p in logit_p_s:
        for lambda_ in lambdas_s:
            print('lambda ', lambda_)

            bayes_estim_i = []

            if lambda_ == 0:
                if len(results[window][logit_p][0]) == 0:
                    for i in range(len(data)):
                        mcmc = MCMCsampler(x=np.array([data[i]]), x_distr=[distr[i]], x_hyper=[hyper[i]], logit_p=logit_p)
                        mcmc.run(num_iter=10000, burn_in=2000, thinning=2, move_prob=None)

                        mcmc.expected_loss_i(0, a=24 * 2, b=1, upper_bound=24 * 2, threshold=50, action='argmin')
                        bayes_estim_i += [copy.copy(mcmc.tau_Bayes_estimate[0])]

                    results[window][logit_p][0] = copy.deepcopy(bayes_estim_i)


            if lambda_ > 0:

                mcmc = MCMCsampler(x=data, x_distr=distr, x_hyper=hyper, logit_p=logit_p, w=w, w_hyper=w_hyper)

                mcmc.interaction_parameters('edge_set', -lambda_ * logit_p / degree_average, hyper_param=E_sub)

                la = -lambda_ * logit_p / degree_average
                mcmc.delta_hyper = None if lambda_ == 0.0 else [0.1, -np.log(1 - 0.03) / la]
                mcmc.delta = 0.0

                # run sampler
                mcmc.run(num_iter=1000000, burn_in=300000, thinning=100, move_prob=None)

                for i in range(len(data)):
                    mcmc.expected_loss_i(i, a=24 * 2, b=1, upper_bound=24 * 2, threshold=50, action='argmin')
                results[window][logit_p][lambda_] = copy.copy(mcmc.tau_Bayes_estimate)

    end = time.time()
    print('ran in ', end - beg)
    return results
