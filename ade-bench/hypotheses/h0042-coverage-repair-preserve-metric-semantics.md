---
id: h0042
title: Coverage repair preserves metric semantics -- when fixing missing rows/date spines, do not change COUNT/SUM/AVG/window definitions unless visible project evidence says the metric itself is wrong
status: hypothesis
kind: hypothesis
source: Captain request 2026-06-10 after Round 2 airbnb009 COUNT(*) vs COUNT(review_date) decision-fork analysis; follows h0019 banking failure and the Round 1 + Round 2 flipped-task choice map. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-10T06:32:33Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`airbnb009` exposed the new Round-2 bankability failure: the solver repeatedly reached the
right local bug location in `mom_agg_reviews` -- the `dates_cte` date spine is narrowed to
days that already have direct reviews -- but one unpinned implementation degree of freedom
still decides the hidden result. Passing runs kept the existing aggregate expression
`COUNT(*)`; the failed standalone h0019 full run made a locally reasonable semantic cleanup
to `COUNT(review_cte.REVIEW_DATE)` so synthetic no-review rows counted as 0. Local date
coverage checks cannot distinguish those choices.

**Falsifiable claim (the single solver-README change -- Implementation policy only):** adding
a general "coverage repair preserves metric semantics" rule will reduce the solver's
wrong-choice rate on this decision fork. When a task is about missing rows, row coverage,
date-spine coverage, or join coverage, the solver must first treat the fix as a coverage
repair and must not change aggregate metric definitions (`COUNT`, `SUM`, `AVG`, window
expressions, business-rule filters) unless the task instruction, existing schema/tests, or
sibling model evidence explicitly says the metric definition itself is wrong. If local
validation passes after the coverage repair, preserve the existing metric semantics.

**The single proposed README text (B variant):**

```text
When the task is about missing rows, date-spine coverage, row coverage, or join
coverage, treat the fix as a coverage repair first. Do not change metric
definitions such as COUNT, SUM, AVG, window expressions, or business-rule filters
unless the task instruction, schema, visible project tests, or sibling model
evidence explicitly says that metric definition is wrong. If local validation
passes after the coverage repair, preserve the existing metric semantics.
```

This is intentionally not task-specific. It does not say "`airbnb009` should keep
`COUNT(*)`." It supplies a general tie-breaker for locally ambiguous repairs:
coverage fixes should not silently become metric-definition rewrites.

**Why this differs from h0019.** h0019 correctly steered the solver toward the date-spine
repair and away from category overproduction, but it did not pin the aggregate line. The
solver therefore had two locally defensible paths after restoring the date spine:

- minimal coverage repair: keep the existing `COUNT(*)`;
- semantic cleanup: change to `COUNT(review_cte.REVIEW_DATE)` so no-review rows count as 0.

The h0019 standalone full failure shows that "found the bug" is not enough at `trials: 1`
when the remaining free line controls the hidden check. h0042 aims to pin the general
decision policy, not the per-task answer.

**Pre-smoke subagent decision-fork evidence (proxy, not a score result).** Before filing this
hypothesis, we ran a controlled subagent decision probe. Each subagent received only the
visible task instruction, the local `mom_agg_reviews.sql`, relevant sibling SQL, and one
solver-rule variant. They were explicitly told not to inspect the repo, not to use tools,
and not to use hidden tests, verifier output, prior runs, or solution files.

Calibration probe:

| Variant | Rule | Kept `COUNT(*)` | Chose column-count |
|---|---|---:|---:|
| A | Weak "smallest local change / prefer siblings" rule | 0/2 | 2/2 |
| B | Coverage repair preserves metric semantics | 2/2 | 0/2 |
| C | Strong COUNT guard + final self-audit | 2/2 | 0/2 |

Follow-up B-only probe:

| Variant | Runs | Kept `COUNT(*)` | Chose `COUNT(review_cte.REVIEW_DATE)` | Other / unclear |
|---|---:|---:|---:|---:|
| B | 10 | 10 | 0 | 0 |

Total B evidence from the two probe batches: **12/12 kept `COUNT(*)`**. The observed proxy
wrong-choice rate for B is 0/12, versus 2/2 wrong for the weak A rule. This is not a real
`rk run` and must not be promoted as pass-rate evidence, but it is a strong preliminary
signal that the README wording changes the solver's local decision policy at the exact fork.

**Falsification path.** h0042 fails if, in fresh real `rk` runs on `ade-bench-airbnb009`, the
committed SQL still changes the aggregate metric definition while performing the date-spine
coverage repair, or if it preserves `COUNT(*)` but fails to reach the date-spine repair at all.
It also fails if the generic rule causes regressions on already-passing canaries by making the
solver over-conservative where a metric definition really did need to change.

**Target dataset.** Primary target: `ade-bench-airbnb009`. This is the one task where the
decision fork and the intended tie-breaker are artifact-proven. The expected movement is not
"discover a new task"; it is "make the already-discovered airbnb009 repair reproducible by
removing the free metric-semantics branch."

**Proposed smoke design.** Because the claim is a probability/decision-policy claim, the first
smoke should be a focused repeated single-cell smoke, not an all-48 run:

1. Create the h0042 solver README and specs in propose as usual.
2. Run `ade-bench-airbnb009` as independent focused smoke repeats (three sequential
   one-task runs, each fresh context / no freeze-CAS reuse).
3. For each run, inspect the committed `models/agg/mom_agg_reviews.sql` and classify:
   `COUNT(*)`, `COUNT(review_cte.REVIEW_DATE)`, other metric rewrite, or no date-spine repair.
4. GO only if at least 2/3 runs both preserve `COUNT(*)` and pass the verifier on clean strict
   audit. A 3/3 result is the desired signal. Any column-count recurrence is a NO-GO for the
   current wording.

If the workflow requires a single ordinary smoke spec first, use `ade-bench-airbnb009` plus
the h0019 canary panel (`airbnb001`, `asana001`, `ana-eng001`, `f1007`, `quickbooks002`);
then follow with sequential focused repeats before any full run. The canaries must stay pass,
but the decisive h0042 read is the committed aggregate choice on `airbnb009`.

**Scope.** Solver README only. No benchmark, runtime, model, sampling, trials, or spec-shape
change. Leak guard remains intact; the proposed README rule references only visible task
instructions, visible schema/tests, sibling models, and local SQL. It does not mention hidden
oracle totals, hidden test names, expected row counts, solution files, or verifier output.

## Acceptance criteria

**AC-1 -- Exactly one README policy change; specs differ only in allowed fields.**
Verified at propose by diffing the h0042 solver README against
`solver_workflows/codex-ade-dbt-minimal/README.md`: one Implementation policy block added,
leak-guard prose byte-identical, no hidden-test/solution/verifier references. Full spec
diff vs `specs/baseline.yaml` shows only `experiment:` and `solver_workflow:`; smoke spec
adds only `benchmark.tasks`.

**AC-2 -- Every score is paired with strict clean audit and captured traces.**
Each `rk score` must cite `rk audit --policy strict` on the same run-dir with
`tainted: 0`, `coverage_missing: 0`, and captured agent traces.

**AC-3 -- Decision-policy evidence is artifact based.**
For every focused `airbnb009` run, read the committed SQL artifact, not the transcript
narration. Classify the actual aggregate expression in `mom_agg_reviews.sql`, whether the
date-spine coverage repair landed, and whether any metric definition changed. Transcript
claims such as "kept semantics" do not count without the committed SQL.

**AC-4 -- h0042 is promoted only if it reduces the known fork.**
Promotion requires fresh-run evidence that the solver reliably chooses the minimal coverage
repair path: preserve the existing aggregate metric expression while repairing the date spine.
The minimum smoke bar is 2/3 independent `airbnb009` focused runs with `COUNT(*)` preserved,
date-spine repair landed, verifier pass, and clean strict audit. 3/3 is the target.

**AC-5 -- No regression canary loss.**
If the smoke includes canaries, all baseline passers must remain pass. Any canary regression
is a NO-GO unless artifact analysis proves it is unrelated single-trial variance and the
captain explicitly accepts that risk.

