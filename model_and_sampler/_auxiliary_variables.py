"""
methods related for auxiliary variables for class ChangepointModel
"""

import numpy as np


def u_t_full_conditional(self, t_):
    """
    Sample auxiliary variables u_t from the full conditional distribution.
    Output graph induced by auxiliary variables.
    0 indicates the empty graph, that is no edges, when \delta = 0
    """
    if self.delta > 0:
        #interact_terms = set(self.lambdas[0].keys())
        graph_u = {i: set() for i in range(self.L)}
        S_t = [t_ in self.ltau[i] for i in range(self.L)]

        keys = np.array(list(self.lambdas[0].keys()))
        vals = np.array(list(self.lambdas[0].values()))

        interact_terms = [i for i in range(len(keys)) if S_t[keys[i][0]] == S_t[keys[i][1]]]

        keys = keys[interact_terms]
        vals = vals[interact_terms]

        keys = keys[np.random.uniform(0, np.exp(self.delta * vals)) > 1]

        for k in keys:
            i = k[0]
            j = k[1]
            graph_u[i].add(j)
            graph_u[j].add(i)

        self.u[t_] = graph_u
    else:
        self.u[t_] = 0


def u_full_conditional(self, silent=1):
    """
    Update all auxiliary variables given latent changepoints.
    Silent mode: To avoid sampling auxiliary variables unnecessarily, we indicate with -1 that a u_t has been
    sampled, for all t. As a result, only u_t which are called will be sampled.
    """
    if silent:
        self.u = [-1 for _ in range(len(self.u))]
    else:
        for t_ in range(len(self.u)):
            self.u_t_full_conditional(t_)


def connected_components(neighbors):
    """
    https://stackoverflow.com/questions/10301000/python-connected-components
    """
    seen = set()

    def component(node):
        nodes = {node}
        while nodes:
            node = nodes.pop()
            seen.add(node)
            nodes |= neighbors[node] - seen
            yield node
    for node in neighbors:
        if node not in seen:
            yield component(node)


def get_induced_clusters(self, t_):
    """
    https://stackoverflow.com/questions/10301000/python-connected-components
    Obtain connected components (or clusters) from a graph
    """
    graph = self.u[t_]
    if graph == 0:
        return [[i] for i in range(self.L)]
    else:
        components = []
        for component in connected_components(graph):
            c = list(component)
            components.append(c)
        return components


def sample_delta(self):
    if self.delta_hyper is None:
        pass
    else:
        if np.random.uniform() <= self.delta_hyper[0]:
            self.delta = 0.0
        else:
            if len(self.delta_hyper) > 2:
                self.delta = np.random.beta(self.delta_hyper[1], self.delta_hyper[2])
            else:
                self.delta = self.delta_hyper[1]


def update_u_shift(self, t, tp, cluster):
    """
    update auxiliary variables for a shift of cluster of changepoints from t to tp
    """
    if (self.delta > 0) and (t != tp):
        out = 0.0
        for i in cluster:

            # swap between t and t^\prime for i and i^\prime \in \gamma
            for ip in [ell for ell in cluster if ell > i]:

                if (ip in self.u[t][i]) and (ip not in self.u[tp][i]):
                    self.u[tp][i].add(ip)
                    self.u[tp][ip].add(i)
                    self.u[t][i].remove(ip)
                    self.u[t][ip].remove(i)
                if (ip not in self.u[t][i]) and (ip in self.u[tp][i]):
                    self.u[tp][i].remove(ip)
                    self.u[tp][ip].remove(i)
                    self.u[t][i].add(ip)
                    self.u[t][ip].add(i)

            for ip in [ell for ell in range(self.L) if ell not in cluster]:

                if (ip in self.u[tp][i]) and (tp not in self.ltau[ip]):   # u_{tp}^\prime(i, ip) = 0
                    self.u[tp][i].remove(ip)
                    self.u[tp][ip].remove(i)

                if t not in self.ltau[ip]:      # u_{t}^\prime(i, ip) from full conditional
                    if (min(i, ip), max(i, ip)) in self.lambdas[0].keys():
                        if np.random.uniform(0, np.exp(self.delta * self.lambdas[0][(min(i, ip), max(i, ip))])) > 1:
                        #if 1 == 0:
                            self.u[t][i].add(ip)
                            self.u[t][ip].add(i)

                if t in self.ltau[ip]:      # change in conditional likelihood of auxiliary variables
                    if (min(i, ip), max(i, ip)) in set(self.lambdas[0].keys()):
                        out -= -self.delta * self.lambdas[0][(min(i, ip), max(i, ip))]

                if tp in self.ltau[ip]:     # change in conditional likelihood of auxiliary variables
                    if (min(i, ip), max(i, ip)) in set(self.lambdas[0].keys()):
                        out += -self.delta * self.lambdas[0][(min(i, ip), max(i, ip))]

        return out

    else:
        return 0.0

