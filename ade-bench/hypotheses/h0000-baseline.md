---
id: h0000
title: Baseline — codex ade-dbt-repair solver, full 48 tasks
status: conclude
kind: hypothesis
source: setup
started: 2026-06-01T16:34:03Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Establish the anchor: the baseline codex solver README on all 48 ade-bench tasks. No
README change — this run defines `@baseline` and the 9/48 (0.1875) reference. Skips
smoke (`propose → full`).

## Run result

Run dir: `runs/ade-bench-baseline/432500212a02092c/` (48/48 trials completed, 0 errored).

**Audit** — `rk audit --policy strict`: **clean**. Top-level summary
`{clean: 48, tainted: 0, coverage_missing: 0}`; every one of the 48 trials reports
`taint_status: clean` with zero findings.

**Score** — `rk score --format json`:

```json
{
  "stratified_pass_at_1": 0.1875,
  "strata": { "default": { "n_total": 48, "n_pass": 9,
    "pass_at_1": 0.1875, "wilson_ci": [0.1019, 0.3194] } },
  "against_constant": { "name": "pass_rate", "value": 0.1875, "verdict": "matches" }
}
```

**Absolute score: 9/48 = 0.1875** (Wilson 95% CI [0.102, 0.319]) — matches the
paper_baseline pass-rate constant of 0.1875. This is the FIRST run, so there is no
`@baseline` registry entry to diff against; per the analyze stage that quantitative
paired-delta step is **skipped** (recorded as absolute score + behavioral read only).
`@baseline` is NOT bound here — that is the conclude stage.

## Behavioral analysis

**Method adherence.** Spot-checked `agent/codex.txt` + `subagent-trace-manifest.json`
across cells: every trial ran `prompt_mode: spacedock-codex-first-officer` with
`captured: 1` and exactly one dispatch of `subagent_type: spacedock:ensign`. The main
(codex first-officer) agent loads the Spacedock entrypoint and delegates the actual dbt
repair to a dispatched ensign worker, as prescribed. So pass/fail reflects the solver's
dbt-repair quality, not a harness/orchestration miss.

**Per-group tally** (passes named; distance-to-pass = `actual_pass / expected_test_count`
from `verifier/test-stdout.txt`):

| Group       | Pass/Total | Notes |
|-------------|-----------|-------|
| airbnb      | **8/9**   | only failure: airbnb009 (0/1, test-fail) |
| ana-eng     | 0/10      | 1 near-miss (ana-eng007-medium 6/10); rest 0/N |
| asana       | 0/6       | best asana001 1/2, asana002 1/3 |
| f1          | **1/16**  | pass: f1011 (6/6); near-miss f1003 3/4 |
| intercom    | 0/3       | all 0/N, all build-errors |
| quickbooks  | 0/4       | closest cohort: qb002 7/8, qb003 12/14, qb004 35/48, qb001 5/12 |

**Why it works (the 9 passes).** airbnb is the carry group — 8/9 fully green
(`actual_pass == expected`, dbt `ERROR=0`). These tasks are repairs the solver
completes end-to-end: models build and all target singular tests pass. f1011 (6/6) is
the lone f1 success.

**Why it fails — two distinct mechanisms** (39 failures: **27 build-error, 12 test-fail**):

- **Build-error (dominant, 27/39).** The model graph never compiles — dbt reports
  `Runtime Error … Catalog Error: Table with name <X> does not exist`, so 0 target
  tests can even run (`actual_pass=0`). The agent left dangling references to upstream
  relations it never built or misnamed. Concrete instances:
  - intercom001 → `stg_intercom__conversation_part_history does not exist`
  - ana-eng002 → `fact_inventory does not exist` (downstream OBT references an unbuilt mart)
  - f1005 → `stg_f1_dataset__constructor_standings does not exist`
  - asana003 → `project_data does not exist` (wrong source relation name)

  This mechanism wipes out essentially all of intercom (3/3), most of f1 (13/16), and
  most of ana-eng (7/10). These are far-from-pass (0/N) — the fix is structural
  (build the missing/correctly-named upstream model), not a tweak.

- **Test-fail (12/39).** Models build clean (`ERROR=0`, large dbt `PASS` counts) but a
  subset of the *target* singular checks return rows. These are the **close** failures —
  distance-to-pass is high: quickbooks002 7/8 (88%), quickbooks003 12/14 (86%),
  quickbooks004 35/48 (73%), ana-eng007-medium 6/10 (60%), asana001 1/2, f1003 3/4,
  airbnb009 0/1. The pipeline is correct in shape but a logic/column/aggregation detail
  is off on one or two checks. quickbooks is the standout near-miss cohort — all four
  build cleanly (dbt TOTAL=100, ERROR=0) and fail only a minority of target equality/
  existence checks.

**Takeaway for the README iteration.** The biggest lever is the build-error class:
27 of 39 failures never get a single target test to run because the solver ships a
graph with unresolved/misnamed upstream relations. A method change that forces the
ensign to `dbt build` (or compile) and resolve every Catalog Error *before* declaring
done would convert many 0/N failures into at-least-runnable trials, and the test-fail
near-misses (quickbooks, ana-eng007-medium, f1003) are the next-cheapest points.

## Verdict

_Filled after the run._

## Stage Report: analyze

- DONE: rk audit --policy strict on the run-dir is clean (taint_status: clean) and rk score records stratified_pass_at_1 = 9/48 (0.1875) into the entity body's ## Run result
  Audit summary `{clean: 48, tainted: 0, coverage_missing: 0}`, 0 findings; `rk score` JSON `stratified_pass_at_1: 0.1875`, n_pass 9 / n_total 48, Wilson CI [0.102, 0.319], against_constant verdict "matches"; both recorded in ## Run result.
- DONE: ## Behavioral analysis gives the per-task-group pass/fail tally and distance-to-pass (#checks_passed / expected_test_count from verifier/test-stdout.txt) for notable failures
  Per-group table (airbnb 8/9, ana-eng 0/10, asana 0/6, f1 1/16, intercom 0/3, quickbooks 0/4) plus distance-to-pass on near-misses and named Catalog-Error build failures; failure split 27 build-error / 12 test-fail.

### Summary

Baseline run `432500212a02092c` audits clean (48/48 trials, strict policy) and scores 9/48 = 0.1875, matching the paper_baseline constant. Since this is the first run there is no `@baseline` to diff, so the paired-delta step was skipped (absolute score + behavioral read only) and `@baseline` was not bound. Behavioral read: airbnb carries the score (8/9); the 39 failures split into a dominant build-error class (27, dbt `Catalog Error: table does not exist` from unbuilt/misnamed upstream relations, 0 target tests run) and a smaller test-fail class (12 near-misses, notably quickbooks 73-88% and ana-eng007-medium/f1003), pointing to "compile/build clean before declaring done" as the highest-leverage README change.
