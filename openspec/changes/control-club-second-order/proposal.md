# Proposal: Control Club Challenge 2 – second-order system (stub)

## Why
Optional exercise in `Problem_2_BBControl.ipynb`: linear system ẋ = [[0,1],[-2,-3]]x + [0,1]u, x0 = (1, −1), u ∈ [−1, 1]; drive x1 to 0 within 3 s / 150 steps. Reward = scaled L1 error (higher is better). The model is known, so this is more control engineering than ML (LQR/MPC as reference).

## What
A policy class with `predict(s)`.
