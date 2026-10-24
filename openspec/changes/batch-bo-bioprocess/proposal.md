# Proposal: Batch BO to maximise the titre of a CHO bioprocess

## Why
Coursework "Data-driven Optimisation of a Bioprocess" (`BatchBayesianOptimization/`). A simulated bioprocess (CHO cells, ODE model in `MLCE_CWBO2025/virtual_lab.py`) maps 6 inputs to the final titre [g/L]. Experiments count as expensive and the budget is fixed. 80 % of the mark comes from the algorithm's score, 20 % from a 2-page report (intuition, methodology, pseudocode, 1 figure).

## What changes
- New submission file `MLCE_<group>_BO.py` with group details, helpers, class `BO(X_initial, X_searchspace, iterations, batch, objective_func)` and an execution block.
- Own optimiser (no off-the-shelf BO package). Goal: find high values early, because from batch 3 onwards every batch is scored by its best-so-far value.
- Report material (figure, pseudocode) is derived from `design.md`.

## Constraints (from handout + README)
- Fixed budget: 6 initial points + 15 rounds × 5 = 81 evaluations.
- Marking uses **different cell kinetics parameters** than the package → do not tune anything to the known optima.
- Only output produced within 60 s of runtime counts.
- Allowed packages: numpy, scipy, sobol-seq, random, time, datetime. Do not set seeds. `scipy.optimize` only for hyperparameters.

## Out of scope
Changing the simulator; multi-fidelity (the package only knows `3LCONTBATCH`).
