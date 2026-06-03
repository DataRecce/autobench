---
id: h0006
title: Validation — run the target AUTO_*_equality checks and drive them to zero rows before finalizing
status: smoke
kind: hypothesis
source: forked from h0005 analyze — post-DuckDB-fix @baseline (622bdedac572b479, 31/48 = 0.6458); attacks the new dominant failure class (equality-test misses) now that the build-error class is gone
started: 2026-06-03T00:50:13Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

After the wrong-DuckDB-dataset fix re-baselined the seed solver to **31/48 (0.6458)**
(`@baseline` = run `622bdedac572b479`), the prior dominant failure mechanism — 27/39
`Catalog Error: Table does not exist` build failures — is **gone**: all 48 cells now
build clean (`dbt build` `ERROR=0`). The new and only remaining failure class is
**target equality-test misses**: 17 tasks where the model graph builds green but a
singular target check (`tests/AUTO_*_equality.sql`, "Got N results, configured to fail
if != 0") returns mismatching rows. 13 of the 17 are off-by-one (a single failing
check).

**Falsifiable claim (the single README change):** the seed solver's Validation stage
stops at "it builds and a few checks pass" and does not reconcile the *target* singular
checks against the expected snapshot. Adding one Validation-stage instruction —
*enumerate the visible target singular tests (`tests/AUTO_*` and any `tests/*.sql`),
run them with `dbt test --select test_type:singular` (or by path), inspect the
mismatching rows each failing `_equality` check returns, and iterate the model logic
until every visible target check returns zero rows before finalizing* — will convert a
material number of the off-by-one equality misses into passes and raise
`stratified_pass_at_1` above the new `@baseline` 0.6458.

This is a method/README change only; it forks the new `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex, gpt-5.5) with no dataset,
harness, or solver-runtime change.

## Acceptance criteria

**AC-1 — Spec diff is a single, localized Validation-stage change.**
Verified by: the diff vs `@baseline`'s `solver_workflows/codex-ade-dbt-minimal/README.md`
touches only the `## Stage: Validation` (and, if needed, `## Stage: Finalization`)
section, adding the "run the visible target `AUTO_*` singular checks and drive them to
zero rows" instruction. No change to Exploration/Implementation or to the
dependency/package guardrails.

**AC-2 — Smoke gate.** On the smoke subset, the variant must not regress any
`@baseline` pass and should flip at least one off-by-one equality miss to a pass before
promotion to full.

**AC-3 — Promotion gate (full run).** Paired `rk runs diff @baseline <variant-run-dir>`
on a clean `rk audit --policy strict`: the adjusted-p / CI clears the tripwire (CI
excludes a regression) AND `stratified_pass_at_1 > 0.6458`. Every recorded score is
paired with a clean strict audit on the same run-dir.

## Target datasets

Drawn from h0005's distance-to-pass failure table (`checks_passed / expected_test_count`,
all build clean — `ERROR` is failing equality checks, not build errors):

- **Off-by-one (single failing equality check) — the cheapest conversions:**
  - `ana-eng007` 9/10 and `ana-eng007-medium` 9/10 — `AUTO_dim_products_equality`
  - `f1002` 9/10 — `AUTO_most_podiums_equality`
  - `asana004` 5/6, `asana005` 7/8, `asana005-hard` 7/8 — `AUTO_int_asana__project_user_agg_equality`
  - `asana002` 2/3 — `AUTO_asana__task_equality`
  - `f1006` 3/4 — `AUTO_constructor_points_equality`
  - `airbnb007` 10/11 — `daily_agg_nps_reviews_equality_with_tolerance`
  - `f1011` 5/6 — `check_option_b`; `airbnb009` 0/1 — `mom_agg_review_date_range`
  - `intercom001` 1/2 — `AUTO_intercom__threads_equality`;
    `intercom003` 1/2 — `AUTO_intercom__conversation_metrics_equality`
  - `ana-eng004` 1/2 — `AUTO_obt_product_inventory_equality`
- **Multi-check misses (stretch targets):**
  - `quickbooks001` 6/12 — `AUTO_stg_quickbooks__estimate_equality` (+5)
  - `ana-eng006` 4/7 — `AUTO_dim_products_equality` + `AUTO_obt_product_inventory_equality` (+1)
  - `intercom002` 2/4 — `AUTO_intercom__conversation_metrics_equality` (+1)

The recurring failing checks — `AUTO_dim_products_equality` (ana-eng cluster),
`AUTO_int_asana__project_user_agg_equality` (asana cluster), and the intercom
`*_equality` pair — are the highest-leverage targets: a fix to the shared aggregation
logic for each cluster could flip several tasks at once.

## Run result

## Smoke result

**Run-dir:** `runs/ade-bench-h0006-validation-run-target-equality-checks/70ec8a5c452e73d5`
(smoke spec `specs/h0006-...smoke.frozen.yaml`, 8 off-by-one targets, trials:1).

### Audit + score (clean-audit attestation)

- **`rk audit --policy strict`: CLEAN** — 8 clean / 0 tainted, exit 0. No leak findings.
- **`rk score`: `stratified_pass_at_1 = 0.0`** — 8 completed, 0 errored, **0/8 PASS**.
  Verdict vs paper_baseline 0.1875: `below`.
- All 8 cells `subagent-trace-manifest.json` → `captured = 1` (the README change WAS
  exercised; the new Validation instruction reached the solver — confirmed in transcripts).

### Per-target read vs @baseline (all 8 — none flipped)

| task | baseline | smoke (pass/total) | failing target check | move |
|---|---|---|---|---|
| ana-eng007 | 9/10 | 9/10 | `AUTO_dim_products_equality` (5 rows) | SAME |
| ana-eng007-medium | 9/10 | **7/10** | `AUTO_obt_product_inventory` + `AUTO_obt_sales_overview` (3 errors) | **REGRESS** |
| f1002 | 9/10 | 9/10 | `AUTO_most_podiums_equality` | SAME |
| asana004 | 5/6 | 5/6 | `AUTO_int_asana__project_user_agg_equality` (3 rows) | SAME |
| asana005 | 7/8 | 7/8 | `AUTO_int_asana__project_user_agg_equality` (3 rows) | SAME |
| asana002 | 2/3 | 2/3 | `AUTO_asana__task_equality` (2 rows) | SAME |
| f1006 | 3/4 | 3/4 | `AUTO_constructor_points_equality` (2 rows) | SAME |
| intercom001 | 1/2 | 1/2 | `AUTO_intercom__threads_equality` (7 rows) | SAME |

**0 flips FAIL→PASS; 1 regression (ana-eng007-medium 9/10 → 7/10).**

### Method-adherence behavioral check (the key question — why 0/8?)

The solver **followed** the new instruction but it was **unactionable**. Read the ensign
sub-transcripts (`<cell>/agent/sessions/.../rollout-*.jsonl`; the `agent/codex.txt`
parent only spawns/waits/closes the worker):

- **asana004 ensign:** ran `dbt test --profiles-dir . --select test_type:singular` →
  *"no singular tests matched. No local `tests/` directory was present."*
- **intercom001 ensign:** *"no singular tests were present because `/app/tests` does not exist."*
- **ana-eng007 ensign:** enumerated and ran the singular-test selector exactly as
  instructed; found none to execute.

**Root cause:** the target `tests/AUTO_*_equality.sql` checks are **hidden verifier tests
injected only at grading time** — they are NOT present in the solver's `/app` workspace.
`dbt test --select test_type:singular` returns zero matches, so there is nothing for the
solver to inspect or iterate against. The hypothesis's premise that these are *visible*
target checks the solver can run and drive to zero rows is **false** for this benchmark;
the existing README already warned of exactly this ("Hidden verifier tests may depend on
the existing project structure"). 0/8 is therefore a **method-premise failure**, not a
solver non-compliance failure.

### Go / no-go

Gate bar = ≥1 flip FAIL→PASS AND no regression. Result: **0 flips and 1 regression** →
**NO-GO. Recommend back to `hypothesis`, not `full`.** The instruction cannot work as
written because the target equality tests are hidden from the solver. A viable redesign
would have the Validation stage reason about expected output from the *visible* source
data / task spec (i.e. independently reconstruct the expected aggregation), rather than
relying on running the hidden `AUTO_*` checks — that is a materially different hypothesis.

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: Fork the @baseline solver and edit ONLY its README `## Stage: Validation` to add the target-equality-check instruction
  `solver_workflows/h0006-validation-run-target-equality-checks/` forked from `codex-ade-dbt-minimal`; single new paragraph appended to the Validation stage (after "Run broader dbt validation…"); Finalization unchanged; leak-guard/no-external-reference prose and dependency guardrails intact; Exploration/Implementation untouched.
- DONE: FULL spec differs from baseline ONLY in `experiment:` and `solver_workflow:`
  `diff specs/baseline.yaml specs/h0006-...yaml` shows exactly two lines changed (see diff below); agent.kind=spacedock_solver, runtime=codex preserved.
- DONE: Smoke spec is the full spec PLUS `benchmark.tasks` listing the off-by-one targets
  `benchmark.tasks: [ana-eng007, ana-eng007-medium, f1002, asana004, asana005, asana002, f1006, intercom001]`.
- DONE: Freeze BOTH specs producing the two `.frozen.yaml` files
  `rk freeze --allow-missing` wrote `...frozen.yaml` and `...smoke.frozen.yaml`; both share `sealed_hash e11eb650...` and `solver_workflow_hash sha256:d2d1df3e...`; smoke task slugs resolved against the dataset (freeze would error on a missing slug).

### Two-field full-spec diff (evidence for the leak-guard gate)

```
2c2
< experiment: ade-bench-baseline # variants: ade-bench-h0001-<slug>
---
> experiment: ade-bench-h0006-validation-run-target-equality-checks # variants: ade-bench-h0001-<slug>
11c11
<   solver_workflow: ./solver_workflows/codex-ade-dbt-minimal # variants repoint to ./solver_workflows/h<NNNN>-<slug>
---
>   solver_workflow: ./solver_workflows/h0006-validation-run-target-equality-checks # variants repoint to ./solver_workflows/h<NNNN>-<slug>
```

### README Validation-stage diff (the single independent variable)

Added to `## Stage: Validation`, immediately after "Run broader dbt validation when practical for the task scope.":

> Before finalizing, enumerate the visible target singular tests in the project
> (`tests/AUTO_*` and any `tests/*.sql`) and run them — `dbt test --select
> test_type:singular`, or by path. For each `_equality` check that fails, inspect
> the mismatching rows it returns and iterate the model logic until every visible
> target singular check returns zero rows. Do not finalize while a visible target
> check is still failing.

### Summary

Forked the @baseline solver (`codex-ade-dbt-minimal`) to `h0006-validation-run-target-equality-checks` and made one surgical README change: a single instruction in the Validation stage to enumerate and run the visible target singular tests (`tests/AUTO_*`, `tests/*.sql`) and drive every `_equality` check to zero rows before finalizing. The full spec differs from baseline only in `experiment:` and `solver_workflow:`; the smoke spec adds the 8 off-by-one `benchmark.tasks`. Both specs froze cleanly with `--allow-missing`. Note: dispatch paths used `../specs`/`../solver_workflows`, but from `ade-bench/` the correct paths are `specs/`/`solver_workflows/` (used here); `rk freeze` also regenerated the shared `specs/provenance.yaml` (expected freeze side effect — new solver_workflow_hash + current harness_git_sha).

## Stage Report: smoke

- DONE: Run the frozen smoke spec; confirm `captured > 0`
  Run-dir `runs/ade-bench-h0006-validation-run-target-equality-checks/70ec8a5c452e73d5`; all 8 cells `captured=1`. (First launch crashed on cell 1 / orphaned container — cleaned up; re-run completed manually outside the team to dodge the process-reaper. Smoke task slugs also had to be fixed to `ade-bench-` prefixed ids — `rk run --explain` rejected the bare slugs; fixed + re-frozen, committed 294c380.)
- DONE: Clean strict audit BEFORE scoring; record focused score + clean-audit attestation
  `rk audit --policy strict` → 8 clean / 0 tainted, exit 0. `rk score` → `stratified_pass_at_1 = 0.0` (8 completed, 0 errored). Both recorded in `## Smoke result`.
- DONE: Per-target FAIL→PASS comparison vs @baseline for the 8; name flips; go/no-go read
  0/8 flips; ana-eng007-medium REGRESSED 9/10→7/10; other 7 unchanged. Full table + behavioral root-cause in `## Smoke result`.

### Summary

Smoke is a NO-GO: 0/8 flips and 1 regression, against a clean strict audit. The README change was exercised (captured=1 on all 8) and the solver followed it — but the instruction is unactionable: the target `tests/AUTO_*_equality.sql` checks are hidden verifier tests injected only at grading time and are absent from the solver's `/app/tests`, so `dbt test --select test_type:singular` returns zero matches (confirmed verbatim in the asana004/intercom001/ana-eng007 ensign sub-transcripts). The hypothesis premise — that these are visible checks the solver can run and drive to zero rows — is false for this benchmark. Recommend back to `hypothesis`; a viable redesign must reconstruct expected output from visible source data rather than running the hidden checks.
