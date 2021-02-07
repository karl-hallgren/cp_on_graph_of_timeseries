"""
methods related to lags for class ChangepointModel
"""

import numpy as np
from math import factorial


def conditional_D_j(self, i, j):
    if self.w[i] > 0:
        d_from = max(0, self.ltau[i][j - 1] + self.d[i][j - 1] - self.ltau[i][j] + 1)
        d_to = min(self.w[i], self.ltau[i][j + 1] + self.d[i][j + 1] - self.ltau[i][j]-1)
        return list(range(d_from, d_to + 1))
    else:
        return [0]


def proposal_lag(self, i, j, sample=1, full_cond=0):
    D_ = self.conditional_D_j(i, j)
    if not full_cond:
        if sample:
            self.d[i][j] = np.random.choice(D_)
        return -np.log(float(len(D_)))
    else:
        if self.w[i] > 0:
            tau_beg = self.ltau[i][j-1] + self.d[i][j-1] - 1
            tau_end = self.ltau[i][j+1] + self.d[i][j+1] - 1
            ltau_j = self.ltau[i][j] - 1
            # self.L_ can be found in _segment.py
            d_f_c = [self.L_(i, [tau_beg, ltau_j + d_]) + self.L_(i, [ltau_j + d_, tau_end]) for d_ in D_]
            if len(d_f_c) == 0:
                print(i, j)
            max_d_ = max(d_f_c)
            d_f_c = np.exp([d_ - max_d_ for d_ in d_f_c])
            d_f_c = d_f_c/np.sum(d_f_c)
            if sample:
                self.d[i][j] = np.random.choice(D_, p=d_f_c)
            if self.d[i][j] not in D_:
                return -np.inf  # move cannot be reversed
                # raise Exception("proposal cannot be reversed in proposal_lag()")
            else:
                return np.log(d_f_c[D_.index(self.d[i][j])])
        else:
            if sample:
                self.d[i][j] = 0
            return 0.0


def propose_w(self, i):
    if self.w_hyper is None:
        print('self.w_hyper is None, that is w_i is fixed for all i')
    elif (self.w_hyper[i] is None) or (self.w_hyper[i][0] == 0):
        return 0.0
    else:
        sample_from_prior = 0
        if sample_from_prior:
            self.w[i] = np.random.geometric(p=self.w_hyper[i][0])-1
            return 0.0
        else:
            out = 0.0
            w_i = self.w[i]
            # propose w_i
            if np.random.uniform() > 0.5:   # w_i^\prime > w_i              #or w_i == 0:
                self.w[i] = w_i + np.random.geometric(p=self.w_hyper[i][1])
                out += np.log(0.5) - (w_i > 0)*np.log(0.5) - np.log(1-(1-self.w_hyper[i][1])**self.w[i])
            else:
                if w_i > 0:
                    prob = [(1 - self.w_hyper[i][1]) ** w for w in range(w_i)]
                    prob_dot = sum(prob)
                    prob = [p/prob_dot for p in prob]
                    self.w[i] = w_i - 1 - np.random.choice(range(w_i), p=prob)
                    out += (self.w[i] > 0)*np.log(0.5) - np.log(0.5) + np.log(1-(1-self.w_hyper[i][1])**w_i)
            # prior ratio
            out += np.log(1-self.w_hyper[i][0])*(self.w[i] - w_i)
            return out


def Q_(self, i, u, v, ltau=None):
    if ltau is None:
        ltau = self.ltau[i]
    if ltau[u + v] - ltau[u] <= self.w[i]:
        rho_u_v = min(self.w[i] + 1, self.T + 1 - ltau[u]) - (ltau[u + v] - ltau[u])
        return np.prod(np.arange(rho_u_v, rho_u_v + v + 1)) / factorial(v + 1)
    else:
        return 0


def Z_(self, i, r, s, ltau=None):
    if ltau is None:
        ltau = self.ltau[i]
    Z_r = [1, self.Q_(i, r, 0)]
    for h in range(2, s + 1):
        Z_r_h = 0
        for j in range(h):
            Z_r_h += Z_r[j]*self.Q_(i, r + j, h - 1 - j, ltau)*((-1)**(h - 1 - j))
        Z_r += [Z_r_h]
    return Z_r[-1]


def norm_const_lag(self, i):

    if len(self.ltau[i]) > 2 and self.w[i] > 0:
        out = 0.0

        ell = [1]
        for j in range(2, len(self.ltau[i])-1):
            if self.ltau[i][j] - self.ltau[i][j-1] > self.w[i]:
                ell += [j]
        ell += [len(self.ltau[i])-1]

        for l_ in range(len(ell)-1):
            out += np.log(self.Z_(i, ell[l_], ell[l_+1] - ell[l_]))

        return out
        # alternatively
        # out = self.Z_(i, 1, len(self.ltau[i])-2)
        # return np.log(out)
    else:
        return 0    # np.log(1)


def norm_const_lag_birth(self, i, j):

    if self.w[i] > 0:
        beg = j
        end = j + 1

        while (beg > 1) and (self.ltau[i][beg] - self.ltau[i][beg - 1] <= self.w[i]):
            beg -= 1

        while (end + 1 < len(self.ltau[i])) and (self.ltau[i][end] - self.ltau[i][end-1] <= self.w[i]):
            end += 1

        if end - beg == 1:
            return -np.log(self.Q_(i, j, 0))
        else:
            ltau = [1] + self.ltau[i][beg:end] + [self.T + 1]
            out = -np.log(self.Z_(i, 1, len(ltau)-2, ltau))

            ltau.remove(self.ltau[i][j])
            out += np.log(self.Z_(i, 1, len(ltau)-2, ltau))
        return out
    else:
        return 0.0

