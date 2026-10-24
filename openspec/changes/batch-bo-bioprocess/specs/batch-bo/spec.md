# Spec: Batch BO bioprocess

## Requirement: Submission format
The submission MUST be a single `.py` file with class `BO(X_initial, X_searchspace, iterations, batch, objective_func)` that sets `self.Y` (all evaluations in order) and `self.time` (timestamp per batch, otherwise 0, as in the example).

### Scenario: Run in the evaluation script
- WHEN the evaluation script runs the file with `iterations=15, batch=5`
- THEN `self.Y` holds exactly 6 + 75 = 81 values
- AND the file imports only numpy, scipy, sobol_seq, random, time, datetime.

## Requirement: Budget
The algorithm MUST call `objective_func` exactly once for the initial points and exactly once per round with exactly 5 points.

### Scenario: No hidden evaluations
- WHEN the algorithm runs
- THEN there are exactly 16 calls to `objective_func` (1 + 15)
- AND every point lies within the bounds: T 30–40 °C, pH 6–8, F1/F2/F3 0–50 mM, cell type ∈ {celltype_1, celltype_2, celltype_3}.

## Requirement: Runtime
The whole run SHOULD stay below 45 s (margin to the 60 s limit on slower machines).

### Scenario: Time limit
- WHEN the run is repeated 5 times on the development machine
- THEN the longest runtime is < 45 s (the simulator alone takes ≈ 0.08 s/evaluation ≈ 7 s).

## Requirement: Quality (main metric)
Score = Σ over batches 3…15 of the best value found so far (13 terms). On average over 20 runs the algorithm SHOULD be clearly above random search, also with changed kinetics parameters.

### Scenario: Comparison with baselines
- WHEN the score is measured over 20 runs, each with the package parameters and with the perturbed parameter sets `shifted` and `swapped` from `eval/score.py`
- THEN the mean is above that of random search (`MLCE_ExampleSubmission_BO.py`) and above pure Sobol search
- AND the results are tabulated in `design.md`.

### Scenario: Robustness
- WHEN a run starts badly (all initial values small)
- THEN the algorithm still finds a value in the upper range of random search by batch 3 (exploration must not starve).
