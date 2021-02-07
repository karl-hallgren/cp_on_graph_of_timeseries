"""
Markov chain Monte Carlo sampler for the graphical changepoint model
"""


import sys
import os
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import copy
import time
import numpy as np


from model_and_sampler.changepoint_model import ChangepointModel


class MCMCsampler(ChangepointModel):

    from model_and_sampler._estimations_and_diagnostics import trace_plot, post_distr, post_distr_plot, post_MAP, get_post_bayes_factors
    from model_and_sampler._estimations_and_diagnostics import loss_function, expected_loss_i

    def __init__(self, x, x_distr, x_hyper, logit_p=None, lambdas=None, w_hyper=None, delta_hyper=None, ltau=None,
                 d=None, w=None, delta=None, prop_t_uniform=None):

        ChangepointModel.__init__(self, x_distr, x_hyper, x, logit_p, lambdas, w_hyper, delta_hyper, ltau, d, w, delta)

        # storage for the sampler
        self.sample_ltau = []
        self.sample_d = []
        self.sample_tau = []
        self.sample_k = []
        self.sample_w = []
        self.accept_prob = 0.0
        self.accept_count = 0

        # full conditional (1) or uniform (0) proposal for lags for [birth-mv, shift-mv, lag-mv, w-mv]
        self.lag_full_cond = [1, 0, 0, 1]
        self.prop_t_uniform = 0 if prop_t_uniform is None else prop_t_uniform     # for the birth/death move

        # estimation
        self.post_distr_k = {}
        self.post_distr_ltau = {}
        self.post_distr_tau = {}
        self.post_distr_w = {}
        self.k_MAP = []
        self.tau_MAP = []
        self.tau_Bayes_estimate = {}
        self.post_bayes_factors = []

    def propose(self, move_type):

        self.accept_prob = 0.0

        if move_type == 'auxi':
            # sample delta and auxiliary variables
            self.sample_delta()
            self.u_full_conditional()
            self.accept_count += 1

        elif move_type == 'birth_death':

            # select a time point t_
            if self.prop_t_uniform:
                t_ = np.random.choice(range(2, self.T + 1))
            else:
                existing_ltau = list(set(x for l_ in self.ltau for x in l_))
                existing_ltau.sort()
                k_ = len(existing_ltau) - 2
                if k_ == 0:
                    sample_from = range(2, self.T)
                    t_ = np.random.choice(sample_from)
                elif k_ == self.T-1:
                    t_ = np.random.choice(existing_ltau[1:-1])
                else:
                    if np.random.uniform(0.0, 1.0) < 0.5:
                        sample_from = np.setdiff1d(range(2, self.T+1), existing_ltau)
                        t_ = np.random.choice(sample_from)
                    else:
                        t_ = np.random.choice(existing_ltau[1:-1])

            # if u_t needs to be updated then do it, and sample a cluster of time series indices
            self.u_t_full_conditional(t_)
            clusters_t = self.get_induced_clusters(t_)
            cluster_t = clusters_t[np.random.choice(len(clusters_t))]

            # adapt to birth or death
            valid_move = 1
            move_death = 0
            add_indices = {}
            if t_ in self.ltau[cluster_t[0]]:   # death
                move_death += 1
                for i in cluster_t:
                    add_indices[i] = self.ltau[i].index(t_)
            else:  # birth
                for i in cluster_t:
                    self.ltau[i].append(t_)
                    self.ltau[i].sort()
                    add_indices[i] = self.ltau[i].index(t_)
                    self.d[i].insert(add_indices[i], None)
                    # check if birth is valid
                    valid_move *= 1 if len(self.conditional_D_j(i, add_indices[i])) > 0 else 0

            #print(len(cluster_t))
            # derive acceptance ratio for adding changepoint at t_ for i \in cluster_t
            if valid_move:
                for i in cluster_t:

                    # prior ratio for adding changepoints
                    self.accept_prob += self.cp_prior_ratio(i, t_, cond=1)

                    # propose lags for added changepoints
                    self.accept_prob -= self.proposal_lag(i, add_indices[i], sample=1 - move_death,
                                                          full_cond=self.lag_full_cond[0])

                    # change of normalising constant for the lags
                    self.accept_prob += self.norm_const_lag_birth(i, add_indices[i])

                    # likelihood ratio
                    self.accept_prob += self.llikelihood_ratio_birth(i, add_indices[i])

                # update accept_prob with proposal for t_ if needed
                if not self.prop_t_uniform:
                    existing_ltau_p = list(set(x for l_ in self.ltau for x in l_))
                    k_p = len(existing_ltau_p) - 2
                    diff_k = k_p - k_
                    if diff_k > 0:
                        self.accept_prob += np.log(self.T - 1 - k_) - np.log(k_p)
                        if k_p == self.T - 1:
                            self.accept_prob -= np.log(0.5)
                        elif k_p == 1:
                            self.accept_prob += np.log(0.5)
                    elif diff_k < 0:
                        self.accept_prob += np.log(k_) - np.log(self.T - 1 + k_p)
                        if k_p == self.T - 2:
                            self.accept_prob += np.log(0.5)
                        elif k_p == 0:
                            self.accept_prob -= np.log(0.5)

            else:
                self.accept_prob = -np.infty

            # accept or reject the move
            if move_death:
                if np.random.uniform(0.0, 1.0) <= min(1, np.exp(-self.accept_prob)):    # death move accepted
                    for i in cluster_t:
                        self.ltau[i].pop(add_indices[i])
                        self.d[i].pop(add_indices[i])
                    self.accept_count += 1
            else:
                if np.random.uniform(0.0, 1.0) > min(1, np.exp(self.accept_prob) if self.accept_prob < 0 else 1):      # birth move rejected
                    for i in cluster_t:
                        self.ltau[i].pop(add_indices[i])
                        self.d[i].pop(add_indices[i])
                else:
                    self.accept_count += 1

        elif move_type == 'shift':

            # pick t_
            existing_ltau = list(set(x for l_ in self.ltau for x in l_))
            existing_ltau.sort()
            if len(existing_ltau) > 2:      # else no changepoint to shift
                t_ = np.random.choice(existing_ltau[1:-1])

                # if u_t needs to be updated then do it; sample a cluster of time series indices impacted by a change
                self.u_t_full_conditional(t_)
                clusters_t = self.get_induced_clusters(t_)
                clusters_t_1 = [cluster for cluster in clusters_t if t_ in self.ltau[cluster[0]]]
                cluster_t = clusters_t_1[np.random.choice(len(clusters_t_1))]
                cluster_t.sort()
                self.accept_prob += np.log(len(clusters_t))

                # propose t_p as a new value for t_
                shift_indices = {}
                cluster_t_lags = {}
                possible_t_p = np.arange(2, self.T + 1)
                for i in cluster_t:
                    shift_indices[i] = self.ltau[i].index(t_)
                    cluster_t_lags[i] = self.d[i][shift_indices[i]]
                    positions_i = np.arange(self.ltau[i][shift_indices[i]-1] + 1, self.ltau[i][shift_indices[i]+1])
                    possible_t_p = np.intersect1d(positions_i, possible_t_p)
                t_p = np.random.choice(possible_t_p)

                # if u_t_p needs to be updated then do it
                self.u_t_full_conditional(t_p)

                #print(len(cluster_t))
                for i in cluster_t:

                    # likelihood of proposing current lags at t_
                    self.accept_prob += self.proposal_lag(i, shift_indices[i], sample=0, full_cond=self.lag_full_cond[1])

                    # log likelihood of data given t_
                    self.accept_prob -= self.llikelihood_adjacent_segments(i, shift_indices[i])

                    # change of normalising constant for the lags
                    self.accept_prob += self.norm_const_lag_birth(i, shift_indices[i])

                    # shift changepoint t_ to t_pself.ltau
                    self.ltau[i][shift_indices[i]] = t_p

                    # change of normalising constant for the lagscluster_t
                    self.accept_prob -= self.norm_const_lag_birth(i, shift_indices[i])

                    # prior ratio for shifting latent changepoint
                    start0 = time.time()
                    self.accept_prob += self.cp_prior_ratio(i, t_p, cond=0) - self.cp_prior_ratio(i, t_, cond=0)
                    end0 = time.time()
                    #print('shift prior', end0 - start0)

                    # propose lags at t_p
                    self.accept_prob -= self.proposal_lag(i, shift_indices[i], sample=1, full_cond=self.lag_full_cond[1])

                    # likelihood ratio for the shift
                    self.accept_prob += self.llikelihood_adjacent_segments(i, shift_indices[i])

                # update auxiliary variables
                aux_shift = [copy.deepcopy(self.u[t_]), copy.deepcopy(self.u[t_p])]
                self.accept_prob += self.update_u_shift(t_, t_p, cluster_t)
                clusters_t_p = self.get_induced_clusters(t_p)
                self.accept_prob -= np.log(len([cluster for cluster in clusters_t_p if t_p in self.ltau[cluster[0]]]))

                # choice of t_p
                existing_ltau_p = list(set(x for l_ in self.ltau for x in l_))
                self.accept_prob += np.log(len(existing_ltau)) - np.log(len(existing_ltau_p))

                if np.random.uniform(0.0, 1.0) <= min(1, np.exp(0 if self.accept_prob > 0 else self.accept_prob)):
                    self.accept_count += 1
                else:
                    for i in cluster_t:
                        self.ltau[i][shift_indices[i]] = t_
                        self.d[i][shift_indices[i]] = cluster_t_lags[i]
                    self.u[t_] = copy.deepcopy(aux_shift[0])
                    self.u[t_p] = copy.deepcopy(aux_shift[1])

        elif move_type == 'lags':

            time_series_with_lags = [i for i in range(self.L) if len(self.ltau[i]) > 2]
            if len(time_series_with_lags) > 0:
                # sample pair (i, j)
                i = np.random.choice(time_series_with_lags)
                j = np.random.choice(range(1, len(self.d[i])-1))

                if not self.lag_full_cond[2]:
                    # likelihood at d_ij
                    self.accept_prob -= self.llikelihood_adjacent_segments(i, j)

                    # sample lag
                    d_ij = self.d[i][j]
                    self.proposal_lag(i, j, sample=1, full_cond=0)

                    # likelihood at t_p
                    self.accept_prob += self.llikelihood_adjacent_segments(i, j)

                    if np.random.uniform(0.0, 1.0) <= min(1, np.exp(self.accept_prob)):
                        self.accept_count += 1
                    else:
                        self.d[i][j] = d_ij

                else:
                    self.proposal_lag(i, j, sample=1, full_cond=1)
                    self.accept_count += 1

        elif move_type == 'lag_upper_bounds':
            # assuming the move is not proposed if w_i if fixed for all i
            i = np.random.choice([i for i in range(self.L) if self.w_hyper[i] is not None])

            # store w_i and associated lags
            w_i = self.w[i]
            d_i = self.d[i][:]

            if len(d_i) > 2:

                # sample w_i
                self.accept_prob += self.propose_w(i)

                # sample d_i
                indices_j = range(1, len(d_i) - 1)  # not working : np.random.permutation(range(1, len(d_i)-1))
                for j in indices_j:
                    self.accept_prob -= self.proposal_lag(i, j, sample=1, full_cond=self.lag_full_cond[3])

                # store proposed parameters
                w_i_p = self.w[i]
                d_i_p = self.d[i][:]

                # updated normalising constant for the lags
                self.accept_prob -= self.norm_const_lag(i)

                # updated conditional log likelihood of the data
                self.accept_prob += self.cond_llikelihood_x(i)

                # likelihood of proposing current lags
                self.w[i] = w_i
                for j in list(indices_j)[::-1]:
                    self.d[i][j] = d_i[j]
                    self.accept_prob += self.proposal_lag(i, j, sample=0, full_cond=self.lag_full_cond[3])

                # normalising constant for the lags
                self.accept_prob += self.norm_const_lag(i)

                # conditional log likelihood of the data
                self.accept_prob -= self.cond_llikelihood_x(i)

                if np.random.uniform(0.0, 1.0) <= min(1, np.exp(self.accept_prob)):
                    self.accept_count += 1
                    self.w[i] = w_i_p
                    self.d[i] = d_i_p[:]

            else:
                # sample w_i
                self.accept_prob += self.propose_w(i)
                self.accept_count += 1

    def run(self, num_iter, burn_in=0, thinning=1, move_prob=None):
        overall_start_time = time.time()

        # prob for moves ['birth_death', 'shift', 'auxi', 'lags', 'lag_upper_bounds']
        move_prob = [0.3, 0.3, 0.1, 0.2, 0.1] if move_prob is None else move_prob
        if self.w_hyper is None:
            move_prob[4] = 0
        if (self.w_hyper is None) and (sum(self.w) == 0):
            move_prob[3] = 0
        if (self.delta_hyper is None) and (self.delta == 0):
            move_prob[2] = 0
        if sum(move_prob) != 1:
            move_prob = [m_/sum(move_prob) for m_ in move_prob]

        for iteration in range(0, burn_in+num_iter):

            move_type = np.random.choice(['birth_death', 'shift', 'auxi', 'lags', 'lag_upper_bounds'], 1, p=move_prob)

            self.propose(move_type)

            if iteration >= burn_in and iteration % thinning == 0:
                self.sample_ltau += [[t[1:-1] for t in self.ltau[:]]]
                self.sample_d += [[t[1:-1] for t in self.d[:]]]
                self.sample_tau += [[[self.ltau[i][j] + self.d[i][j] for j in range(1, len(self.ltau[i][:-1]))]
                                    for i in range(self.L)]]
                self.sample_w += [self.w[:]]
                self.sample_k += [[len(self.ltau[i][1:-1]) for i in range(self.L)]]

            if iteration % 5000 == 0:
                print('iter - ', iteration, ' time ', time.time()-overall_start_time, ' logit ', self.logit_p[0], ' lambda ',
                      next(iter(self.lambdas[0].values())) if self.lambdas is not None else 0)

        overall_end_time = time.time()
        print('sampler ran in ', overall_end_time - overall_start_time)

