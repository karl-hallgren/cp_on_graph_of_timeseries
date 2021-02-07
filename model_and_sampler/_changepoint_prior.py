"""
methods related to the prior for (latent) changepoint parameters (k,\tau)
for class ChangepointModel
"""


def cp_prior_ratio(self, i, t, cond=0):
    """
    prior ratio for adding a changepoint
    conditional on auxiliary variables if cond=1
    """
    out = self.logit_p[i]
    if self.lambdas is not None:
        out -= self.lambdas[1][i]
        if cond:
            for ell in range(self.L):
                if i != ell:
                    if (min(i, ell), max(i, ell)) in self.lambdas[0].keys():
                        if t in self.ltau[ell]:
                            out += (1-self.delta) * self.lambdas[0][(min(i, ell), max(i, ell))]
                        else:
                            out += self.delta * self.lambdas[0][(min(i, ell), max(i, ell))]
        else:
            for ell in range(self.L):
                if i != ell:
                    if t in self.ltau[ell]:
                        if (min(i, ell), max(i, ell)) in self.lambdas[0].keys():
                            out += self.lambdas[0][(min(i, ell), max(i, ell))]

    return out


def cp_prior_unnormalised(self):
    """
    unnormalised prior for latent changepoints
    """
    out = 0.0
    for i in range(self.L):
        out += (self.logit_p[i] - self.lambdas[1][i])*len(self.ltau[i][1:-1])
        if self.lambdas is not None:
            for j in range(i + 1, self.L):
                if (min(i, j), max(i, j)) in self.lambdas[0].keys():
                    out += self.lambdas[0][(i, j)]*len(list(set(self.ltau[i][1:-1]) & set(self.ltau[j][1:-1])))
    return out

