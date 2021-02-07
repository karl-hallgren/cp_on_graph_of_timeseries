"""
simulation star structure part 04
"""

import sys
import os
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())


from simulation_study.simulation_study_functions import run_experiment_star_structure

# parameters of the experiment

theta_1_2_s = [1070]  # [1030, 1040, 1050, 1060, 1070]

file_name_output = 'simulation_star_part04_results.pkl'


# run experiment

run_experiment_star_structure(file_name_output, theta_1_2_s)


