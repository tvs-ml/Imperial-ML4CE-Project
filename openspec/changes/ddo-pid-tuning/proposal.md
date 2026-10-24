# Proposal: DDO part 1 – PID tuning of a CSTR (stub)

## Why
Older coursework (`DataDrivenOptimization/part1_unconstrained/`): choose 32-dimensional PID parameters so that the control error, control input and control smoothness of a CSTR are minimal. Fixed evaluation budget, max. 1 min runtime. Compared against COBYQA, TuRBO and SciPy methods in the notebook.

## What
Function `your_alg(f, x_dim, bounds, iter_tot)` (submitted as `CW1_<team>.py`).
