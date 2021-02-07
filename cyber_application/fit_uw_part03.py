#!/usr/bin/env python3

"""
fit lanl data no window part 03
"""

# import modules and functions

import sys
import os
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from cyber_application.fit_function import run_fit_lanl

import numpy as np
import pickle


file_name = 'auth_weekly_uw_part03'


logit_p_s = [-60]

window = -1

np.random.seed(666)

results = run_fit_lanl(logit_p_s, window)


# print results

dump_file = open('cyber_application/results/' + file_name, "wb")
pickle.dump(results, dump_file)
dump_file.close()

