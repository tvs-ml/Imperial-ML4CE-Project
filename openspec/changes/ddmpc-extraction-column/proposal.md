# Proposal: Data-driven MPC for a multi-stage extraction column (stub)

## Why
Coursework part 3 (`DataDrivenMPC/coursework_part_3.pdf`): a data-driven MPC has to control a 5-stage counter-current extraction column (10 ODEs, pc-gym) to changing setpoints. 80 % of the mark = score from `evaluate.py` (weighted sum of setpoint error and control effort, lower is better), 20 % = 2-page report.

## What
Three functions in the format of `your_alg.py`: explorer (max. 5 system simulations), model trainer, controller. Budget: 2 min data collection + training, 5 min per control simulation. Allowed: numpy, scipy, sobol-seq, random, time, pc-gym, scikit-learn.

## Material
In the course folder on the Mac under `DataDrivenMPC/src/`: `your_alg.py`, `control_task.py`, `evaluate.py`, `time_series/`.
