"""
methods related to conditional likelihood of the data for class ChangepointModel
"""

import numpy as np
import scipy.special as special


def L_(self, i, seg):
    x_ = self.x[i][seg[0]:seg[1]]
    out = 0.0

    if self.x_distr[i] == 'Poisson':     # hyper[0] is alpha, hyper[1] is gamma
        n = len(x_)
        x_dot = np.sum(x_)
        out = self.x_hyper[i][0] * np.log(self.x_hyper[i][1]) - special.gammaln(self.x_hyper[i][0])
        out += special.gammaln(x_dot + self.x_hyper[i][0]) - (x_dot + self.x_hyper[i][0]) * np.log(self.x_hyper[i][1] + n)

    elif self.x_distr[i] == 'Normal':    # hyper[0] is lambda (scale), hyper[1] is mu_0 and hyper[2] is lambda_0 (scale)
        n = len(x_)
        x_dot = np.sum(x_)
        x_dot_sq = np.sum(np.square(x_))
        lda_n = self.x_hyper[i][2] + n * self.x_hyper[i][0]
        mu_n = (self.x_hyper[i][1] * self.x_hyper[i][2] + self.x_hyper[i][0] * x_dot) / lda_n
        out = 0.5 * np.log(self.x_hyper[i][2] / lda_n) + (n / 2.) * np.log(self.x_hyper[i][0] / (2 * np.pi))
        out += lda_n * (mu_n ** 2) - self.x_hyper[i][0] * x_dot_sq - self.x_hyper[i][2] * (self.x_hyper[i][1] ** 2)

    elif self.x_distr[i] == 'Multinomial':      # hyper[0] are concentration parameters, hyper[1] (used for simulations only)
        alpha_sum = sum(self.x_hyper[i][0])
        x_sums = x_.sum(0)
        out = special.gammaln(alpha_sum) - np.sum(special.gammaln(self.x_hyper[i][0]))
        out += np.sum(special.gammaln(x_sums+np.array(self.x_hyper[i][0]))) - special.gammaln(sum(x_sums)+alpha_sum)

    return out

def llikelihood_ratio_birth(self, i, j):

    tau_beg = self.ltau[i][j-1] + self.d[i][j-1] - 1
    tau_p = self.ltau[i][j] + self.d[i][j] - 1
    tau_end = self.ltau[i][j+1] + self.d[i][j+1] - 1

    out = self.L_(i, [tau_beg, tau_p]) + self.L_(i, [tau_p, tau_end]) - self.L_(i, [tau_beg, tau_end])

    return out


def llikelihood_adjacent_segments(self, i, j):

    tau_beg = self.ltau[i][j-1] + self.d[i][j-1] - 1
    tau_j = self.ltau[i][j] + self.d[i][j] - 1
    tau_end = self.ltau[i][j+1] + self.d[i][j+1] - 1

    out = self.L_(i, [tau_beg, tau_j]) + self.L_(i, [tau_j, tau_end])
    return out


def cond_llikelihood_x(self, i):

    out = 0.0
    for j in range(len(self.ltau[i])):
        tau_beg = self.ltau[i][j-1] + self.d[i][j-1] - 1
        tau_end = self.ltau[i][j] + self.d[i][j] - 1
        out += self.L_(i, [tau_beg, tau_end])

    return out


