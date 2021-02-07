"""
class for changepoint model
"""



import sys
import os
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())


import copy
import numpy as np


class ChangepointModel:

    from model_and_sampler._auxiliary_variables import u_t_full_conditional, u_full_conditional, get_induced_clusters, sample_delta
    from model_and_sampler._auxiliary_variables import update_u_shift
    from model_and_sampler._changepoint_prior import cp_prior_ratio, cp_prior_unnormalised
    from model_and_sampler._lags import proposal_lag, norm_const_lag, propose_w, norm_const_lag, norm_const_lag_birth, Z_, Q_
    from model_and_sampler._lags import conditional_D_j
    from model_and_sampler._segment import llikelihood_ratio_birth, llikelihood_adjacent_segments, cond_llikelihood_x, L_
    from model_and_sampler._interaction_parameters import interaction_parameters
    from model_and_sampler._simulations import sample_segment_parameter, sample_segment_data, sample_data, plot_data

    def __init__(self, x_distr=None, x_hyper=None, x=None, logit_p=None, lambdas=None, w_hyper=None,
                 delta_hyper=None, ltau=None, d=None, w=None, delta=None, L=None, T=None):
        # the data
        self.x_distr = x_distr
        self.x_hyper = x_hyper
        self.x = x

        if x is None:
            self.L = L
            self.T = T
        elif isinstance(x, np.ndarray):
            self.L = x.shape[0] if x is not None else L
            self.T = x.shape[1] if x is not None else T
        else:
            self.L = len(x)
            self.T = len(x[0])

        # the hyperparameters
        self.logit_p = [np.log(1 / float(self.T)) / np.log(1 - 1 / float(self.T))]*self.L if logit_p is None else logit_p
        if not isinstance(self.logit_p, list):
            self.logit_p = [self.logit_p]*self.L
        self.lambdas = lambdas   # None is all interaction parameters are 0
        self.w_hyper = w_hyper   # if None then w_i is fixed for all i, otherwise None (if w_i fixed)
                                 # or [prior geometric parameter, proposal geometric parameter] for each i
        self.delta_hyper = delta_hyper   # if None then delta is fixed, otherwise [prob = 0, alpha, beta] for prior

        # full model parameter
        self.ltau = [[1, self.T + 1] for _ in range(self.L)] if ltau is None else copy.deepcopy(ltau)
        self.d = [[0 for _ in range(len(self.ltau[i]))] for i in range(self.L)] if d is None else copy.deepcopy(d)
        for i in range(len(self.ltau)):
            if 1 not in self.ltau[i]:
                self.ltau[i].insert(0, 1)
                self.d[i].insert(0, 0)
            if (self.T + 1) not in self.ltau[i]:
                self.ltau[i] += [self.T + 1]
                self.d[i] += [0]
        self.u = [0 for _ in range(self.T+1)]
        self.w = [0 for _ in range(self.L)] if w is None else w
        self.delta = 0 if delta is None else delta

