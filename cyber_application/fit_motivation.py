
import sys
import os
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from model_and_sampler.mcmc_sampler import MCMCsampler

import numpy as np
import pandas as pd
import copy

path = 'cyber_application/'

nodes = ['U342@DOM1', 'U86@DOM1']

# import data
data = []
for v in nodes:
    try:
        data_v = pd.read_csv(path + 'data/tseries/x_' + str(v) + '.csv')
        data_v = data_v.values.tolist()
        data += [copy.deepcopy(data_v)]
    except:
        pass

data = [np.array(data[i][:720]) for i in range(len(data))]

# set parameters
L = len(data)
T = len(data[0])

logit_p_s = [-10, -30, -50, -70, -90, -110, -130, -150, -170]
pd.Series(logit_p_s).to_csv(path + 'results/motivation_logit_p.csv', index=False)


# fit data
np.random.seed(707)
for i in range(len(nodes)):

    hyper = [[1] * len(data[i][0])]
    distr = 'Multinomial'

    post_k = []
    post_tau = []
    bayes_estim = []
    map_tau = []
    tau_bayes = []

    print(i)

    for logit_p in logit_p_s:
        print(logit_p)
        mcmc = MCMCsampler(x=np.array([data[i]]), x_distr=[distr], x_hyper=[hyper], logit_p=logit_p)
        mcmc.run(num_iter=15000, burn_in=5000, thinning=1, move_prob=None)
        mcmc.post_distr()
        post_k += [mcmc.post_distr_k[0]]

        mcmc.expected_loss_i(0, a=24*2, b=1, upper_bound=24*2, threshold=50, action='argmin')
        bayes_estim += [copy.copy(mcmc.tau_Bayes_estimate[0])]

    post_k = pd.DataFrame(post_k).fillna(0)
    post_k = post_k.reindex(range(min(post_k.columns), max(post_k.columns) + 1), axis='columns')
    post_k = post_k.fillna(0)
    bayes_estim = pd.DataFrame(bayes_estim).fillna(0)

    post_k.to_csv(path + 'results/motivation_post_k_' + str(nodes[i])+'.csv', index=False)
    bayes_estim.to_csv(path + 'results/motivation_bayes_tau_' + str(nodes[i]) + '.csv', index=False)


