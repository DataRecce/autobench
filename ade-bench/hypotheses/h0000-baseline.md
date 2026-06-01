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

**PASSED — 9/48 (0.1875), anchor established.** This is the first full run, so
promotion is unconditional: there is no prior `@baseline` to diff against and no
tripwire to clear. `@baseline` is now bound to run `432500212a02092c` (audit clean,
48/48 trials, score 9/48 matches the paper_baseline pass-rate constant of 0.1875,
Wilson CI [0.102, 0.319]). This run is the reference all future variants fork and
diff against.

**Top failure modes to attack next** (39 failures, two mechanisms):

1. **Build-errors on unbuilt/misnamed upstreams (27/39 — the dominant lever).** The
   model graph never compiles: dbt raises `Catalog Error: Table with name <X> does
   not exist`, so 0 target tests run (`actual_pass=0`). These are far-from-pass and
   structural — the solver ships dangling references to upstream relations it never
   built or misnamed (e.g. intercom001 → `stg_intercom__conversation_part_history`,
   ana-eng002 → `fact_inventory`, f1005 → `stg_f1_dataset__constructor_standings`,
   asana003 → `project_data`). Wipes out intercom (3/3), most of f1 (13/16), most of
   ana-eng (7/10). Highest-leverage fix: force the ensign to `dbt build`/compile and
   resolve every Catalog Error before declaring done.

2. **Test-fail near-misses (12/39 — the cheapest points).** Models build clean
   (`ERROR=0`) but a minority of target singular checks return rows. The standout
   cohort is quickbooks, all four building cleanly and failing only a few checks:
   **quickbooks003 12/14 (86%)**, **quickbooks002 7/8 (88%)**, quickbooks004 35/48
   (73%), quickbooks001 5/12; plus ana-eng007-medium 6/10 (60%), asana001 1/2,
   f1003 3/4, airbnb009 0/1. A logic/column/aggregation tweak on one or two checks
   converts these to passes — the next-cheapest gains after the build-error class.

The baseline is the anchor; the captain seeds the next concept/hypothesis from
these failure modes.

## Stage Report: analyze

- DONE: rk audit --policy strict on the run-dir is clean (taint_status: clean) and rk score records stratified_pass_at_1 = 9/48 (0.1875) into the entity body's ## Run result
  Audit summary `{clean: 48, tainted: 0, coverage_missing: 0}`, 0 findings; `rk score` JSON `stratified_pass_at_1: 0.1875`, n_pass 9 / n_total 48, Wilson CI [0.102, 0.319], against_constant verdict "matches"; both recorded in ## Run result.
- DONE: ## Behavioral analysis gives the per-task-group pass/fail tally and distance-to-pass (#checks_passed / expected_test_count from verifier/test-stdout.txt) for notable failures
  Per-group table (airbnb 8/9, ana-eng 0/10, asana 0/6, f1 1/16, intercom 0/3, quickbooks 0/4) plus distance-to-pass on near-misses and named Catalog-Error build failures; failure split 27 build-error / 12 test-fail.

### Summary

Baseline run `432500212a02092c` audits clean (48/48 trials, strict policy) and scores 9/48 = 0.1875, matching the paper_baseline constant. Since this is the first run there is no `@baseline` to diff, so the paired-delta step was skipped (absolute score + behavioral read only) and `@baseline` was not bound. Behavioral read: airbnb carries the score (8/9); the 39 failures split into a dominant build-error class (27, dbt `Catalog Error: table does not exist` from unbuilt/misnamed upstream relations, 0 target tests run) and a smaller test-fail class (12 near-misses, notably quickbooks 73-88% and ana-eng007-medium/f1003), pointing to "compile/build clean before declaring done" as the highest-leverage README change.

## Stage Report: conclude

- DONE: Bind @baseline to this run via `rk baseline promote` then `rk registry add run baseline <run-dir>`; confirm `rk registry resolve run @baseline` prints the run-dir and razorback-research.toml now has the [[refs]] entry
  `rk registry add run baseline /…/432500212a02092c` returned OK; `rk registry resolve run @baseline` prints the run-dir and `rk registry list` shows `run @baseline → …/432500212a02092c`. NOTE: this razorback version persists the binding to `~/.config/razorback/registry.yaml` (the registry store's actual location), NOT to `razorback-research.toml` — the toml `[[refs]]` block is only a commented seed/example and was not rewritten by the CLI. `rk baseline promote` was NOT run: its signature requires `--to <baseline-dir> --constraints <constraints.yaml>` (a snapshot+tripwire-verify step), no `constraints.yaml` exists in the repo, and the anchor is unconditional with no tripwire — so the load-bearing `registry add` binding is what establishes `@baseline`.
- DONE: Write ## Verdict in the entity body: PASSED — 9/48 (0.1875) anchor established; name the top failure modes to attack next (27 build-errors on unbuilt upstreams; near-misses quickbooks003 12/14, quickbooks002 7/8)
  `## Verdict` records PASSED 9/48 (0.1875) anchor established and names the two failure mechanisms: 27 build-errors on unbuilt/misnamed upstreams (dominant lever) and the test-fail near-misses led by quickbooks003 12/14 and quickbooks002 7/8.

### Summary

Bound `@baseline` to run `432500212a02092c` via `rk registry add run baseline` (confirmed by `rk registry resolve run @baseline` and `rk registry list`) and wrote the PASSED verdict (9/48 = 0.1875 anchor, Wilson CI [0.102, 0.319]) naming the top failure modes to attack next. Two divergences from the checklist phrasing, both benign for the unconditional anchor: (1) the binding persists to `~/.config/razorback/registry.yaml`, not `razorback-research.toml` (the toml `[[refs]]` is a commented seed, untouched by the CLI); (2) `rk baseline promote` was not run because it requires a `--to`/`--constraints` snapshot pair and no `constraints.yaml` exists — the `registry add` is the load-bearing step that establishes `@baseline`. Per dispatch instructions, no follow-up hypothesis was filed and frontmatter was left untouched for the first officer to terminalize.
