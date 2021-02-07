"""
methods for interaction parameters for the class ChangepointModel
"""


def interaction_parameters(self, graph, lbda, hyper_param=None, zeta=None):
    if lbda is None or lbda == 0:
        self.lambdas = None
    else:
        zeta = [] if zeta is None else zeta
        out = [{}, [0.0] * self.L]
        if graph == 'lattice':  # hyper_param[0] is \ell_2
            for i in range(self.L-1):
                for j in range(i + 1, self.L):
                    if (j == i + 1 and j % hyper_param[0] > 0) or (j - i == hyper_param[0]):
                        out[0][(i, j)] = lbda

        elif graph == 'rchain':  # hyper_param[0] is r
            for i in range(self.L-1):
                for j in range(i + 1, min(i + hyper_param[0] + 1, self.L)):
                    out[0][(i, j)] = lbda

        elif graph == 'complete':
            for i in range(self.L-1):
                for j in range(i+1, self.L):
                    out[0][(i, j)] = lbda

        elif graph == 'star':
            for i in range(1, self.L):
                out[0][(0, i)] = lbda

        elif graph == 'edge_set':
            if hyper_param[0] == 1:
                E = hyper_param[2]
                stick = 1
            else:
                E = hyper_param
                stick = 0
            for i in range(self.L):
                for j in range(i+1, self.L):
                    if [i, j] in E:
                        out[0][(i, j)] = lbda
                    else:
                        if stick:
                            out[0][(i, j)] = hyper_param[1]

        self.lambdas = out








