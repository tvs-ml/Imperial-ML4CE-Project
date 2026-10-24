# Tasks: Batch BO bioprocess

## 1. Foundations
- [x] 1.1 Read handout, README, notebook, simulator; constraints in proposal.md
- [x] 1.2 Measure the simulator: deterministic (factor 1.0377), ~0.08 s/evaluation, value range
- [x] 1.3 Set up environment per `requirements.txt` (Python 3.10, numpy 1.26.4, scipy 1.11.4) → `.venv/` in the course folder, via `uv venv --python 3.10`

## 2. Evaluation first
- [x] 2.1 `eval/score.py`: score formula (Σ best-so-far batches 3–15), runtime, 20 runs
- [x] 2.2 Perturbed kinetics parameter sets (at least 2) for robustness testing
- [x] 2.3 Measure random and Sobol baselines, record in design.md

## 3. Candidate 1
- [ ] 3.1 GP (Matérn-5/2, ARD, log target) + hyperparameter fit
- [ ] 3.2 Compare cell-type encodings (one-hot vs. product kernel)
- [ ] 3.3 Batch acquisition (Kriging Believer + UCB/EI schedule)
- [ ] 3.4 Runtime guard
- [ ] 3.5 Measure, record results + rejected variants in design.md

## 4. Polish
- [ ] 4.1 Variants after measuring (e.g. trust region, initial design, β schedule)
- [ ] 4.2 Submission file `MLCE_<group>_BO.py` with allowed imports only, no seeds
- [ ] 4.3 Report building blocks: figure + pseudocode from design.md
