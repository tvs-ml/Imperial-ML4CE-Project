# Baseline: pure Sobol search in the continuous space, cell type round-robin.
# Randomly shifted per run (Cranley-Patterson rotation via `random`) so that
# 20 runs are not identical.
import os
import random
import sys
from datetime import datetime

import numpy as np
import sobol_seq

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import MLCE_CWBO2025.virtual_lab as virtual_lab

LOW = np.array([30, 6, 0, 0, 0])
HIGH = np.array([40, 8, 50, 50, 50])
CELLTYPES = ['celltype_1', 'celltype_2', 'celltype_3']


def objective_func(X: list):
    return np.array(virtual_lab.conduct_experiment(X))


class BO:
    def __init__(self, X_initial, X_searchspace, iterations, batch, objective_func):
        start_time = datetime.timestamp(datetime.now())
        n = len(X_initial) + iterations * batch
        shift = np.array([random.random() for _ in range(5)])
        u = (sobol_seq.i4_sobol_generate(5, n) + shift) % 1.0
        X = [list(LOW + ui * (HIGH - LOW)) + [CELLTYPES[i % 3]] for i, ui in enumerate(u)]

        self.Y = objective_func(X[:len(X_initial)])
        self.time = [datetime.timestamp(datetime.now()) - start_time] * len(self.Y)
        for it in range(iterations):
            k = len(X_initial) + it * batch
            y = objective_func(X[k:k + batch])
            self.Y = np.concatenate([self.Y, y])
            self.time += [datetime.timestamp(datetime.now()) - start_time] * len(y)


X_initial = [None] * 6  # only the count matters, points come from the Sobol sequence
BO_m = BO(X_initial, None, 15, 5, objective_func)
