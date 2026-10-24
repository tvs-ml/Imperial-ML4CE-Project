"""Local evaluation script for the batch BO submission (not part of the submission).

Runs a submission file the way the course marking does: the file runs in full,
including its own execution block. Beforehand, `conditions_data.df` (kinetics
parameters) and `virtual_lab.conduct_experiment` (call counter, bounds check,
timestamps) are patched.

Score = sum over batches 3..15 of the best-so-far value (13 terms). Batches that
finish after the time limit, or are missing, count with the best-so-far value up
to that point (README, point B).

Usage (from BatchBayesianOptimization/):
    ../.venv/bin/python eval/score.py MLCE_ExampleSubmission_BO.py --runs 20
    ../.venv/bin/python eval/score.py eval/baselines/sobol_BO.py --sets package --runs 5 --jobs 1
"""
import argparse
import copy
import json
import multiprocessing as mp
import os
import runpy
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.dirname(HERE)
sys.path.insert(0, COURSE)

TIME_LIMIT = 60.0
N_INIT, ITERATIONS, BATCH = 6, 15, 5
FIRST_SCORED = 3
BOUNDS = {"T": (30, 40), "pH": (6, 8), "F": (0, 50)}
CELLTYPES = ("celltype_1", "celltype_2", "celltype_3")


# --- Kinetics parameter sets -------------------------------------------------
# "package" = original. The perturbed sets shift exactly the quantities that
# set location and height of the optima (E_a = temperature optimum in °C,
# pH_opt, my_max); "swapped" also swaps the cell types so that the same cell
# type does not always win.
def _shift(p, **kw):
    p = copy.deepcopy(p)
    for key, val in kw.items():
        if key.endswith("_mul"):
            p[key[:-4]] *= val
        else:
            p[key] += val
    return p


def parameter_sets():
    import MLCE_CWBO2025.conditions_data as data
    base = data.process_parameters["3LCONTBATCH"]
    c1, c2, c3 = (base[c] for c in CELLTYPES)
    return {
        "package": base,
        "shifted": {
            "celltype_1": _shift(c1, E_a=+4, pH_opt=-0.5, my_max_mul=1.10),
            "celltype_2": _shift(c2, E_a=-3, pH_opt=+0.6, my_max_mul=0.90),
            "celltype_3": _shift(c3, E_a=+2, pH_opt=+0.9, my_max_mul=1.05),
        },
        "swapped": {
            "celltype_1": _shift(c3, E_a=-1, pH_opt=+0.3),
            "celltype_2": _shift(c1, E_a=+5, pH_opt=-0.7, my_max_mul=1.20),
            "celltype_3": _shift(c2, E_a=-2, pH_opt=+0.8, my_max_mul=0.85),
        },
    }


def _install_params(name):
    import pandas as pd
    import MLCE_CWBO2025.conditions_data as data
    params = parameter_sets()[name]
    data.df = pd.DataFrame(
        [{"reactor": "3LCONTBATCH", "cell_type": c, **params[c]} for c in CELLTYPES])


# --- One run -----------------------------------------------------------------
def _check_point(row):
    T, pH, f1, f2, f3, cell = row
    ok = (BOUNDS["T"][0] <= T <= BOUNDS["T"][1] and BOUNDS["pH"][0] <= pH <= BOUNDS["pH"][1]
          and all(BOUNDS["F"][0] <= f <= BOUNDS["F"][1] for f in (f1, f2, f3)) and cell in CELLTYPES)
    if not ok:
        raise ValueError(f"Point out of bounds: {row}")


def run_once(args):
    path, set_name = args
    import MLCE_CWBO2025.virtual_lab as vl
    _install_params(set_name)
    calls = []
    original = vl.conduct_experiment
    t0 = time.perf_counter()

    def counted(X, *a, **kw):
        X = list(X)
        for row in X:
            _check_point(row)
        y = original(X, *a, **kw)
        calls.append({"n": len(X), "y": list(y), "t": time.perf_counter() - t0})
        return y

    vl.conduct_experiment = counted
    error = None
    g = {}
    os.chdir(os.path.dirname(os.path.abspath(path)))
    try:
        g = runpy.run_path(path, run_name="__main__")
    except Exception as exc:  # a crashing submission keeps what it evaluated
        error = repr(exc)
    runtime = time.perf_counter() - t0
    vl.conduct_experiment = original

    # consistency: the BO object's self.Y must match the recorded calls
    bo = next((v for v in g.values() if hasattr(v, "Y") and hasattr(v, "time")), None)
    y_calls = [y for c in calls for y in c["y"]]
    y_match = bo is not None and np.allclose(np.asarray(bo.Y, float), y_calls)

    budget_ok = (len(calls) == 1 + ITERATIONS and calls[0]["n"] <= N_INIT
                 and all(c["n"] == BATCH for c in calls[1:]))
    return {"score": score_from_calls(calls), "runtime": runtime, "n_calls": len(calls),
            "budget_ok": budget_ok, "y_match": bool(y_match), "error": error,
            "best": max(y_calls) if y_calls else float("nan"),
            "best_so_far": best_so_far_per_batch(calls)}


def best_so_far_per_batch(calls):
    """Best-so-far after init (index 0) and after each batch 1..15, with time limit."""
    out, best = [], -np.inf
    for k in range(1 + ITERATIONS):
        if k < len(calls) and calls[k]["t"] <= TIME_LIMIT:
            best = max(best, max(calls[k]["y"]))
        out.append(best)
    return out


def score_from_calls(calls):
    return float(sum(best_so_far_per_batch(calls)[FIRST_SCORED:]))


# --- Main -------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("submission")
    ap.add_argument("--runs", type=int, default=20)
    ap.add_argument("--sets", default="package,shifted,swapped")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2),
                    help="parallel runs; use --jobs 1 for runtime measurement")
    ap.add_argument("--json", help="write raw data here")
    a = ap.parse_args()

    path = os.path.abspath(a.submission)
    results = {}
    ctx = mp.get_context("spawn")  # fresh process per run, no shared patches
    with ctx.Pool(a.jobs, maxtasksperchild=1) as pool:
        for s in a.sets.split(","):
            results[s] = pool.map(run_once, [(path, s)] * a.runs)

    print(f"{os.path.basename(path)}  ({a.runs} runs, jobs={a.jobs})")
    print(f"{'Set':<11} {'Score':>16} {'Best':>16} {'Time max':>9}  Checks")
    for s, rs in results.items():
        sc = np.array([r["score"] for r in rs])
        be = np.array([r["best"] for r in rs])
        rt = max(r["runtime"] for r in rs)
        checks = []
        if not all(r["budget_ok"] for r in rs):
            checks.append("BUDGET")
        if not all(r["y_match"] for r in rs):
            checks.append("Y!=calls")
        errs = {r["error"] for r in rs if r["error"]}
        if errs:
            checks.append(f"ERROR {errs}")
        print(f"{s:<11} {sc.mean():9.1f} ± {sc.std(ddof=1) if len(sc) > 1 else 0:5.1f} "
              f"{be.mean():9.1f} ± {be.std(ddof=1) if len(be) > 1 else 0:5.1f} {rt:8.1f}s  "
              f"{', '.join(checks) or 'ok'}")
    if a.json:
        with open(a.json, "w") as f:
            json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
