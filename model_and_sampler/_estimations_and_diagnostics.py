"""
methods related to estimations of posterior distribution of the changepoints and diagnostics of sampler
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
import pandas as pd
import matplotlib.pyplot as plt
import copy
from model_and_sampler._segment import L_

def trace_plot(self, param=None, sub=None):
    if sub is None:
        sub = range(self.L)

    if param is None:
        param = ['tau'] * len(sub)
    elif not isinstance(param, list):
        param = [param] * len(sub)

    plt.figure()
    for i in range(len(sub)):
        plt.subplot(len(sub), 1, i + 1)
        if param[i] == 'k':
            k_i_sample = [iteration[sub[i]] for iteration in self.sample_k]
            plt.xlim(0, len(self.sample_k))
            plt.plot(k_i_sample)
        elif param[i] == 'ltau':
            ltau_i_sample = pd.DataFrame([t[sub[i]] for t in self.sample_ltau])
            # plt.ylim(0, self.T)
            plt.xlim(0, len(self.sample_ltau))
            if ltau_i_sample.shape[1] > 0:
                plt.plot(ltau_i_sample, 's', marker='+', markersize=3, color='k')
            else:
                plt.plot([])
        elif param[i] == 'tau':
            tau_i_sample = pd.DataFrame([t[sub[i]] for t in self.sample_tau])
            # plt.ylim(0, self.T)
            plt.xlim(0, len(self.sample_tau))
            if tau_i_sample.shape[1] > 0:
                plt.plot(tau_i_sample, 's', marker='+', markersize=3, color='k')
            else:
                plt.plot([])
        elif param[i] == 'w':
            w_i_sample = [iteration[sub[i]] for iteration in self.sample_w]
            plt.xlim(0, len(self.sample_w))
            plt.plot(w_i_sample)
        elif param[i] == 'd':
            pass
        else:
            pass
    plt.show()


def post_distr(self, param=None, sub=None, param_cond=None):
    if param is None:
        param = ['k', 'tau']
    if 'tau' in param:
        param += ['k']

    if sub is None:
        sub = range(self.L)

    for i in sub:
        if 'k' in param:
            post_distr_i_k = pd.Series([iteration[sub[i]] for iteration in self.sample_k]).value_counts()
            post_distr_i_k = post_distr_i_k / post_distr_i_k.sum()
            self.post_distr_k[sub[i]] = post_distr_i_k.copy()

        if 'tau' in param:
            if param_cond is not None:
                k_cond = param_cond[sub[i]]
            else:
                k_cond = self.post_distr_k[sub[i]].index[0]  # MAP k_i
            post_dist_tau_i = [iteration[sub[i]] for iteration in self.sample_tau if len(iteration[sub[i]]) == k_cond]
            num_iter_k_cond = len(post_dist_tau_i)
            if num_iter_k_cond > 0 and k_cond > 0:
                post_dist_tau_i = pd.DataFrame(post_dist_tau_i)
                post_dist_tau_i = post_dist_tau_i.apply(pd.value_counts).fillna(0).sum(axis=1)
                post_dist_tau_i = post_dist_tau_i / num_iter_k_cond
                self.post_distr_tau[sub[i]] = [k_cond, post_dist_tau_i.copy()]
            else:
                self.post_distr_tau[sub[i]] = [k_cond, 0]  # 0 to indicate prob 0 for this k_cond

        if 'w' in param:
            post_distr_w_i = pd.Series([iteration[sub[i]] for iteration in self.sample_w]).value_counts()
            post_distr_w_i = post_distr_w_i / post_distr_w_i.sum()
            self.post_distr_w[sub[i]] = post_distr_w_i.copy()


def post_distr_plot(self, param=None, param_cond=None, sub=None, options=None):
    self.post_distr(param=[param], sub=sub, param_cond=param_cond)

    if sub is None:
        sub = range(self.L)

    plt.figure()
    for i in range(len(sub)):
        plt.subplot(len(sub), 1, i + 1)
        plt.ylim(0, 1)
        if param == 'k':
            post_distr_k_i = self.post_distr_k[sub[i]]
            post_distr_k_i.reindex(list(range(min(post_distr_k_i.index), max(post_distr_k_i.index) + 1)),
                                   fill_value=0)
            plt.bar(post_distr_k_i.index, post_distr_k_i.values, color='darkslategray')
            plt.xticks(post_distr_k_i.index)

        elif param == 'tau':
            post_distr_tau_i = self.post_distr_tau[sub[i]][1]
            if not isinstance(post_distr_tau_i, int):
                # post_distr_tau_i.reindex(list(range(min(post_distr_tau_i.index), max(post_distr_tau_i.index) + 1)),
                post_distr_tau_i.reindex(list(range(1, self.T + 1)), fill_value=0)
                plt.bar(post_distr_tau_i.index, post_distr_tau_i.values, color='black')
            else:
                plt.plot([])

        elif param == 'w':
            post_distr_w_i = self.post_distr_w[sub[i]]
            post_distr_w_i.reindex(list(range(min(post_distr_w_i.index), max(post_distr_w_i.index) + 1)),
                                   fill_value=0)
            plt.bar(post_distr_w_i.index, post_distr_w_i.values, color='darkslateblue')

        else:
            pass
    plt.show()


def post_MAP(self):
    self.k_MAP = []
    self.tau_MAP = []
    for i in range(self.L):
        k_i_sample = pd.Series([iteration[i] for iteration in self.sample_k])
        self.k_MAP += [k_i_sample.mode()[0]]

        if self.k_MAP[-1] == 0:
            self.tau_MAP += [[]]
        else:
            tau_i_sample = pd.DataFrame([iteration[i] for iteration in self.sample_tau])
            tau_i_sample_cond = tau_i_sample.loc[k_i_sample == self.k_MAP[-1], range(0, self.k_MAP[-1])]
            tau_MAP_i = \
            tau_i_sample_cond.groupby(list(range(self.k_MAP[-1]))).size().sort_values(ascending=False).index[0]
            if not isinstance(tau_MAP_i, tuple):
                tau_MAP_i = [tau_MAP_i]
            self.tau_MAP += [list(tau_MAP_i)]

def get_post_bayes_factors(self, mode='bayes'):
    self.post_bayes_factors = []

    if mode == 'bayes':
        tau_post = [[int(t) for t in self.tau_Bayes_estimate[i]] for i in range(self.L)] #copy.deepcopy(self.tau_Bayes_estimate)
    elif mode == 'map':
        tau_post = [[int(t) for t in self.tau_MAP[i]] for i in range(self.L)] #copy.deepcopy(self.tau_MAP)
    else:
        tau_post = [[] for i in range(self.L)]

    tau_post = [[1] + tau_post[i][:] + [self.T+1] for i in range(self.L)]

    for i in range(self.L):
        out_i = []
        for j in range(1, len(tau_post[i])-1):
            tau_beg = tau_post[i][j-1] - 1
            tau_p = tau_post[i][j] - 1
            tau_end = tau_post[i][j+1] - 1
            out = self.L_(i, [tau_beg, tau_p]) + self.L_(i, [tau_p, tau_end]) - self.L_(i, [tau_beg, tau_end])
            out_i += [out]

        self.post_bayes_factors += [out_i[:]]


def loss_function(tau, tau_h, a, b, upper_bound):
    if len(tau)*len(tau_h) == 0:
        return np.abs((len(tau) - len(tau_h)))*a
    else:
        if len(tau) >= len(tau_h):
            tau_r = tau[:]
            tau_c = tau_h[:]
        else:
            tau_r = tau_h[:]
            tau_c = tau[:]

        cost = []
        for t_r in tau_r:
            cost += [[b * np.abs(t_c - t_r) if np.abs(t_c - t_r) <= upper_bound else a for t_c in tau_c]]
        cost = np.array(cost)
        row_ind, col_ind = linear_sum_assignment(np.array(cost))

        return cost[row_ind, col_ind].sum() + (len(tau_r) - len(tau_c)) * a


def expected_loss_i(self, i, a, b, upper_bound, threshold=100, action='argmin', tau_i=None):

    # a = 40
    # b = 1
    # upper_bound = 40

    tau_i_sample = pd.DataFrame([t[i] for t in self.sample_tau])
    tau_i_sample = tau_i_sample.fillna(0)
    if tau_i_sample.shape[1] > 0:
        tau_i_table = tau_i_sample.groupby(list(range(tau_i_sample.shape[1]))).size().sort_values(ascending=False) / tau_i_sample.shape[0]
        tau_i_table = pd.DataFrame(tau_i_table, columns=[tau_i_sample.shape[1]])
        tau_i_table = tau_i_table.reset_index()

        if threshold is not None:
            tau_i_table = tau_i_table[:threshold]

        if action == 'derive':
            if tau_i is None:
                tau_i = []
                print('expected loss of []')
            tau_i_table[tau_i_sample.shape[1] + 1] = tau_i_table.apply(lambda row: loss_function([r for r in row[:-1] if r > 0],
                                                           tau_i, a=a, b=b, upper_bound=upper_bound), axis=1)
            return np.sum(tau_i_table[tau_i_sample.shape[1]] * tau_i_table[tau_i_sample.shape[1] + 1])

        elif action == 'argmin':
            expected_loss_tau = []
            for j in range(tau_i_table.shape[0]):
                tau_i_table[tau_i_sample.shape[1] + 1] = tau_i_table.apply(lambda row: loss_function([r for r in row[:-1] if r > 0],
                                                                                                     [t for t in tau_i_table.iloc[j][:tau_i_sample.shape[1]] if t > 0],
                                                                                                     a=a, b=b, upper_bound=upper_bound), axis=1)
                expected_loss_tau += [np.sum(tau_i_table[tau_i_sample.shape[1]] * tau_i_table[tau_i_sample.shape[1] + 1])]
            argmin = expected_loss_tau.index(min(expected_loss_tau))
            self.tau_Bayes_estimate[i] = [t for t in tau_i_table.iloc[argmin][:tau_i_sample.shape[1]] if t > 0]
            return expected_loss_tau[argmin]
        else:
            print('action is None')

    else:
        if action == 'derive':
            if tau_i is None:
                tau_i = []
                print('expected loss of []')
            return loss_function([], tau_i, a=a, b=b, upper_bound=upper_bound)
        elif action == 'argmin':
            self.tau_Bayes_estimate[i] = []
            return 0
        else:
            print('action is None')



