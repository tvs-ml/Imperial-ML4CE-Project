# Proposal: RL for inventory management of a three-echelon supply chain (stub)

## Why
Coursework 2025 (`ReinforcementLearning/`): supplier → distribution centre → retailer, Poisson demand, 4 weeks in daily steps. The goal is an ordering policy for the DC and the retailer that maximises profit (revenue minus delivery fees, variable ordering costs, holding costs, stock-out penalties, over-capacity). 80 % of the mark = mean over several seeds on a different, possibly harder environment; 20 % = 2-page report.

## What
`your_optimization_alg(...)` in `algorithms/your_algorithm.py` (submitted as `RL_<team>.py`), returns NN weights + plot data. The NN architecture must not be changed. Budget per run: 5000 episodes, 5 min. Baselines: REINFORCE with baseline, simulated annealing, (s,S) heuristic.
