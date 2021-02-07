#!/usr/bin/env python3

"""
simulation star structure part 07
"""


# import relevant modules and functions

import sys
import os
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from simulation_study.simulation_study_functions import run_experiment_cluster_detection

# parameters for the experiment
file_name_output = 'simulation_cluster_part07_results.pkl'

theta_1_2_s = [1050]  # [1040, 1050, 1055, 1060, 1070, 1080, 1090]

graph_type = ['rchain', 'lattice'][:1]

lag_mode = [0, 1][1:]

window_type = ['no', 'fixed', 'unknown']

fixed_lag = 5

nrep = 10

seed = 340

run_experiment_cluster_detection(file_name_output, seed, theta_1_2_s, graph_type, lag_mode, window_type, nrep, fixed_lag)



