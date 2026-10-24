# Imperial ML4CE – Working the OpenSpec way

Each coursework task is its own change under `changes/<task>/`:

| File | Question |
|---|---|
| `proposal.md` | Why? What changes? |
| `specs/<area>/spec.md` | What must hold? (requirements + scenarios, measurable) |
| `design.md` | How is it built? Including **Rejected approaches** with measurements |
| `tasks.md` | Which steps, in which order? |

Rules
- Keep it lean: a table of measurements beats three paragraphs of prose.
- Every approach that was tried goes into `design.md` with its result (score, runtime, seeds), even if it was rejected. That keeps the path to the solution traceable and usable for the 2-page report.
- One change per task, not per approach: the spec (metric, evaluation script, budget, baselines) is the same for all approaches. Each approach gets a short section in `design.md` (idea, difference to its predecessor, file under `approaches/`), a row in the results table or under "Rejected approaches", and its own block in `tasks.md`. A new change is only opened when the rules themselves change (new metric, new task).
- Every approach lives as its own file side by side on the main branch (e.g. `BatchBayesianOptimization/approaches/<name>.py`), not as a separate git branch, so `score.py` can compare them in one run and rejected approaches stay visible. A branch is only a workspace for one approach; once measured it is merged, rejected or not. The submission file is a copy of the winner.
- Once a task is submitted, the final spec moves to `specs/<area>/spec.md` (archived).
- All documents and code comments are written in English.
- Anything that is easier to grasp as a picture (flows, loops, data paths) gets a Mermaid diagram (```mermaid block) right in the Markdown.

## Tasks

The source of truth is the course folder on Frank's Mac (`~/repro/Imperial-ML4CE-Course`, a clone of OptiMaL-PSE-Lab/Imperial-ML4CE-Course).

| Folder | Task | Course folder | Status |
|---|---|---|---|
| `changes/batch-bo-bioprocess` | Batch BO of a CHO bioprocess (maximise titre) [2025] | `BatchBayesianOptimization/` | Evaluation + baselines done |
| `changes/rl-inventory` | RL for a three-echelon supply chain (ordering policy) [2025] | `ReinforcementLearning/` | Stub |
| `changes/ddmpc-extraction-column` | Data-driven MPC of a 5-stage extraction column [2024] | `DataDrivenMPC/` | Stub |
| `changes/ddo-pid-tuning` | DDO part 1: PID tuning of a CSTR, 32 dimensions [2023/24] | `DataDrivenOptimization/part1_unconstrained/` | Stub |
| `changes/ddo-williams-otto` | DDO part 2: Williams-Otto with constraints [2023/24] | `DataDrivenOptimization/part2_constrained/` | Stub |
| `changes/control-club-cstr` | Control Club 1: CSTR with disturbance (optional) | `DataDrivenMPC/pc-gym/Control-Club-Challenge/` | Stub |
| `changes/control-club-second-order` | Control Club 2: second-order system (optional) | same | Stub |
