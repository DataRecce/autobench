---
id: h0044
title: Cumulative standings max-points guard -- for season/entity totals from standings snapshots, repair inflated sums with same-grain max(points) and reject final-row variants
status: hypothesis
kind: hypothesis
source: Captain request 2026-06-10 after f1006 decision-fork analysis and C-variant subagent probe. Follows h0012 smoke pass / full regression evidence and h0037 full f1006/f1006-hard latest-row failure pattern. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-10T08:15:58Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`f1006` is a cumulative-standings repair, not an independent recompute target.
The visible task says the `points` columns in `constructor_points.sql` and
`driver_points.sql` are too high. The broken local shape is `sum(points)` over
race-by-race standings rows at constructor/season and driver/season grain. Since
standings points are cumulative snapshots, summing them over a season overstates
the total. The intended local repair family is same-grain `max(points)` in every
named affected model.

**Falsifiable claim (the single solver-README change -- Implementation policy
only):** adding a cumulative-standings max-points guard will make the real solver
preserve the simple `sum(points) -> max(points)` repair and avoid the plausible
but fragile alternatives: latest-row/rank/final-race selection and recomputing
season totals from race results. The expected benefit is not that the model
newly discovers `max(points)`; proxy probes show it already often does. The
benefit is that the full workflow should stop drifting from the correct simple
aggregate repair into an over-engineered final-row path.

**The single proposed README text (C variant):**

```text
When repairing season/entity totals from *_standings tables, treat points as
cumulative race-by-race snapshots unless local evidence proves otherwise. If a
task says points are too high and the model currently sums standings points,
prefer the same-grain aggregate repair: replace sum(points) with max(points) in
every named affected model.

Do not switch to latest-row, rank, row_number, QUALIFY, order-by-final-race, or
race-results recomputation unless local evidence proves max(points) is wrong.
Before finalizing, inspect the edited SQL: the load-bearing fix should preserve
the existing entity/season grain and use max(points), not final-row selection.
```

For `f1006`, the intended repair is:

- change `sum(cs.points)` to `max(cs.points)` in `constructor_points.sql`;
- change `sum(ds.points)` to `max(ds.points)` in `driver_points.sql`;
- preserve existing constructor/season and driver/season output grain;
- do not introduce `row_number()`, `rank()`, `QUALIFY`, final race ordering, or
  date/round final-row selection as the load-bearing fix;
- do not recompute totals from race-result rows when standings are present.

**Why this differs from h0012 and h0037.** h0012's successful smoke proved that
the f1006 family can be fixed by a simple cumulative-standings aggregate repair,
but that experiment's broader independent-recompute framing was harmful at full
run. h0037 showed the remaining failure mode: the solver can choose a locally
reasonable final-row/latest-row implementation that passes many intuitive checks
but fails edge cases. h0044 therefore avoids a broad "recompute independently"
instruction and pins a narrow artifact shape: same-grain `max(points)`.

**Pre-smoke subagent decision-fork evidence (proxy, not a score result).** We
ran fresh subagents with `fork_context=false`, no tools, no repo inspection, no
hidden verifier output, and only visible task/model context. The decision fork
was: same-grain `max(points)` vs latest-row/final-row standings selection vs
race-results recomputation.

Calibration with full visible context, including sibling championship models
that use `max(points)`:

| Variant | Rule | `max(points)` | Latest-row / final-row | Race-results recompute |
|---|---|---:|---:|---:|
| A | Weak baseline-style smallest local repair | 2/2 | 0/2 | 0/2 |
| B | Cumulative standings max-points rule | 2/2 | 0/2 | 0/2 |
| C | Strong max-points rule + no-latest-row guard | 2/2 | 0/2 | 0/2 |

Stricter probe without sibling championship model context:

| Variant | Rule | `max(points)` | Latest-row / final-row | Race-results recompute |
|---|---|---:|---:|---:|
| A | Weak baseline-style smallest local repair | 2/2 | 0/2 | 0/2 |
| B | Cumulative standings max-points rule | 2/2 | 0/2 | 0/2 |
| C | Strong max-points rule + no-latest-row guard | 2/2 | 0/2 | 0/2 |

Follow-up C-only stricter probe:

| Variant | Runs | `max(points)` | Latest-row / final-row | Race-results recompute | Other / unclear |
|---|---:|---:|---:|---:|---:|
| C | 10 | 10 | 0 | 0 | 0 |

Total C evidence across both C batches: **14/14** chose same-grain
`max(points)`, with **0/14** choosing latest-row or race-results recompute.

Honest caveat: the weak A wording also chose `max(points)` in 4/4 probes. This
means h0044 is not claiming the C rule uniquely discovers the correct branch in
an isolated prompt. It claims the C rule should reduce full-workflow drift after
the branch is discovered, by making final-row variants artifact-invalid.

**Falsification path.** h0044 fails if fresh real `rk` smoke on the f1 standings
family produces a committed patch whose load-bearing change is latest-row,
rank/final-race selection, or race-results recomputation. It also fails if the
patch changes only one of the two named f1006 models, changes output grain, or
regresses same-family passers.

**Target datasets.** Primary targets:

- `ade-bench-f1006`
- `ade-bench-f1006-hard`

Same-family targets:

- `ade-bench-f1005`
- `ade-bench-f1005-medium`

Optional canaries:

- `ade-bench-f1001`
- `ade-bench-airbnb001`

The expected movement is to stabilize the f1 standings family by preventing the
known latest-row/recompute failure branch. A green target whose committed SQL
does not contain same-grain `max(points)` is not strong evidence for this
hypothesis.

**Proposed smoke design.** Use a focused family smoke panel:

1. `ade-bench-f1006`
2. `ade-bench-f1006-hard`
3. `ade-bench-f1005`
4. `ade-bench-f1005-medium`
5. `ade-bench-f1001`
6. `ade-bench-airbnb001`

The decisive artifact read is the f1 point-model patch:

1. `constructor_points.sql` uses same-grain `max(...points...)` as the
   load-bearing fix.
2. `driver_points.sql` uses same-grain `max(...points...)` as the load-bearing
   fix when the task names that model.
3. No load-bearing `row_number()`, `rank()`, `QUALIFY`, `order by round_number`,
   `order by race_date`, or final-row selection appears in the point-total
   repair.
4. No race-results recomputation replaces the standings aggregate when standings
   are present.
5. Target(s) pass on clean strict audit, and same-family/canary tasks do not
   regress.

**Scope.** Solver README only. No benchmark, runtime, model, sampling, trials, or
spec-shape change. Leak guard remains intact; the proposed README rule references
only visible task instructions, local model names, local standings tables, local
SQL artifacts, and local data validation. It does not mention hidden expected
rows, verifier test names, solution files, or public reference data.

## Acceptance Criteria

**AC-1 -- Exactly one README policy change; specs differ only in allowed fields.**
Verified at propose by diffing the h0044 solver README against
`solver_workflows/codex-ade-dbt-minimal/README.md`: one Implementation policy
block added, leak-guard prose byte-identical, no hidden-test/solution/verifier
references. Full spec diff vs `specs/baseline.yaml` shows only `experiment:` and
`solver_workflow:`; smoke spec adds only `benchmark.tasks`.

**AC-2 -- Every score is paired with strict clean audit and captured traces.**
Each `rk score` must cite `rk audit --policy strict` on the same run-dir with
`tainted: 0`, `coverage_missing: 0`, and captured agent traces.

**AC-3 -- Decision-policy evidence is artifact based.**
For f1 standings targets, read committed SQL, not transcript narration. Classify
the patch as same-grain `max(points)`, latest-row/final-row, race-results
recompute, partial-one-model repair, or unclear.

**AC-4 -- h0044 is promoted only if the max-points artifact lands.**
Promotion requires the target point models to pass with committed same-grain
`max(points)` repairs and zero use of the known wrong repair families as the
load-bearing fix. A green target with latest-row logic is a NO-GO for this
hypothesis.

**AC-5 -- No regression canary loss.**
All baseline passers in the smoke panel must remain pass. Any same-family or
canary regression is a NO-GO unless artifact analysis proves it is unrelated
single-trial variance and the captain explicitly accepts that risk.
