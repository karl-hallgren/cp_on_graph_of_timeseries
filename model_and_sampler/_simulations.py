"""
simulate data from the changeppoint model
"""

import numpy as np
import matplotlib.pyplot as plt

def sample_segment_parameter(self, i):
    if self.x_distr[i] == 'Poisson':
        return np.random.gamma(self.x_hyper[i][0], 1/self.x_hyper[i][1])
    elif self.x_distr[i] == 'Normal':
        return np.random.normal(self.x_hyper[i][1], self.x_hyper[i][2])
    elif self.x_distr[i] == 'Multinomial':
        return list(np.random.dirichlet(tuple(self.x_hyper[i][0])))
    else:
        pass


def sample_segment_data(self, i, j, theta_ij=None):
    n_ij = self.ltau[i][j] + self.d[i][j] - (self.ltau[i][j-1] + self.d[i][j-1])

    if theta_ij is None:
        theta_ij = self.sample_segment_parameter(i)

    if self.x_distr[i] == 'Poisson':
        return np.random.poisson(theta_ij, n_ij)
    elif self.x_distr[i] == 'Normal':
        return np.random.normal(theta_ij, self.x_hyper[i][0], n_ij)
    elif self.x_distr[i] == 'Multinomial':
        out = np.random.multinomial(self.x_hyper[i][1], theta_ij, n_ij)
        return out.tolist()
    else:
        pass


def sample_data(self, theta=None):
    self.x = []
    for i in range(self.L):
        self.x += [np.concatenate([self.sample_segment_data(i, j, theta_ij=None if theta is None else theta[i][j-1])
                                   for j in range(1, len(self.ltau[i]))])]
    self.x = np.array(self.x)


def plot_data(self, tau_show=True):
    plt.figure()
    for i in range(self.L):
        plt.subplot(self.L, 1, i + 1)
        plt.plot(range(0, self.T), self.x[i], 'k+', markersize=3)
        if tau_show:
            for j in range(1, len(self.ltau[i])-1):
                plt.axvline(x=self.ltau[i][j] + self.d[i][j] - 1, color='r', linestyle='-', alpha=0.3, linewidth=3.0)
    plt.show()


