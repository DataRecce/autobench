---
id: h0008
title: Finalization — assert source-derived output invariants (no dropped rows, grain uniqueness, contract completeness) before finalizing
status: smoke
kind: hypothesis
source: forked from the h0005 @baseline (622bdedac572b479, 31/48 = 0.6458) 17-failure raw-log analysis + h0007's rejection note (surviving direction #1 — "check invariants the output must satisfy regardless of how it was computed"). The solver is blind to the grading oracle (no tests/, no solution seeds in /app), so verify-the-target methods (h0006/h0007) are dead; this attacks the failures with INDEPENDENT, source-derived invariants instead of a correlated self-re-derivation. solver_workflows/codex-ade-dbt-minimal unchanged at fork.
started: 2026-06-03T10:11:25Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The 17 `@baseline` failures all share one shape: the solver builds a clean-compiling
project, runs generic spot-checks ("row counts, nulls, uniqueness, representative rows"),
and **declares success while systematically under-/mis-specifying the output** — and
because the grading tests and expected-output seeds are absent from `/app`
([[ade-bench-solver-blind-to-oracle]]), it never learns it was wrong. The misses cluster
into three mechanisms that are all detectable from the **local source data + the project's
declared schema**, with no reference to the hidden oracle:

- **Source rows silently dropped** — e.g. `asana004/005/005-hard`
  (`int_asana__project_user_agg`): projects with zero matching users are dropped because
  the aggregation is join-anchored on the aggregate instead of the base `project` entity
  (3-row miss); `intercom001/002/003`: wrong grain / missing `_fivetran_active` handling
  (2 expected rows, solver emitted 5).
- **Grain not unique** — e.g. `ana-eng006` `fact_inventory` fans out (204 rows vs 102
  expected) because the dedup (`row_number() … where rn = 1`) is missing.
- **Output contract incomplete** — e.g. `f1002` omits the `rank` column; `ana-eng004`
  and `ana-eng006` emit fewer columns than the contract; `quickbooks001` never creates 3
  required staging models (`stg_quickbooks__{estimate,refund_receipt,sales_receipt}`),
  failing both existence and equality.

**Falsifiable claim (the single README change — Finalization stage only):** the seed
solver's Validation/Finalization prose checks generic data-quality properties but does NOT
assert the three **source-derived, computation-independent invariants** above and treat a
violation as a model defect to fix. Adding one Finalization instruction — *for each model
the task creates or changes, before finalizing verify against the local source data and
the project's declared schema (NOT against any verifier/AUTO_* test and NOT by re-deriving
the expected answer): (1) no source rows are silently dropped — every key present in the
upstream source(s) at the model's declared grain appears in the output unless the task
explicitly filters it, reconciling row/key counts to the source; (2) the model is unique
at its stated grain — `count(*) = count(distinct <grain key>)`, no unexpected join
fan-out; (3) the output contract is complete — every column declared in the model's
`schema.yml` is emitted and every model the instruction or project graph implies exists,
builds, and is populated. Treat any invariant violation as a defect in the model logic to
fix before finalizing* — will catch the dropped-row / fan-out / incomplete-contract misses
that currently fail the hidden `_equality` and `_existence` checks, flipping a material
number of failures to passes and raising `stratified_pass_at_1` above the `@baseline`
0.6458.

This is distinct from the REJECTED h0007: h0007 had the solver re-derive the expected
answer the same way and diff (correlated error — a systematic misread repeats in both).
These invariants are checked against the **source and the declared contract**, so they
catch errors even when the task itself was misunderstood — exactly the surviving direction
the captain flagged when rejecting h0007.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex, gpt-5.5); no dataset, harness, or
solver-runtime change. The no-external-reference / leak-guard prose stays intact (invariants
use only the local workspace source data + schema YAML — no public fetch, no oracle, no
reference to hidden tests).

Target datasets (smoke, all `ade-bench-` prefixed): the three invariant sub-classes —
- dropped-rows: `ade-bench-asana004`, `ade-bench-asana005`, `ade-bench-asana005-hard`,
  `ade-bench-intercom001`
- grain-uniqueness: `ade-bench-ana-eng006`
- contract-completeness: `ade-bench-f1002`, `ade-bench-quickbooks001`
plus one stable-`@baseline`-pass regression sentinel: `ade-bench-airbnb001`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0008-finalization-source-derived-invariants.yaml`
shows only the `experiment:` and `solver_workflow:` lines; the README diff vs
`codex-ade-dbt-minimal/README.md` touches only the `## Stage: Validation`/`## Stage:
Finalization` section (the single invariants instruction), leaves Exploration/Implementation
and the dependency/package guardrails untouched, and does not reference the hidden
`AUTO_*`/verifier tests or weaken the leak-guard prose. `agent.kind: spacedock_solver`,
`runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir,
clean (`tainted: 0`), with `captured > 0` on the cells.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on the target datasets above, the variant must not regress the
`airbnb001` sentinel (or any `@baseline` pass present) and should flip at least one of the
targeted failures to a pass before promotion to full.

## Smoke result

**Run dir:** `runs/ade-bench-h0008-finalization-source-derived-invariants/809de1a923b89ff6`
(experiment `ade-bench-h0008-finalization-source-derived-invariants`, job `809de1a923b89ff6`).

**Audit (strict, paired to the scored run-dir):** CLEAN — `summary: {clean: 8, tainted: 0,
coverage_missing: 0}`; every cell has `captured = 1 (> 0)` in
`subagent-trace-manifest.json`. AC-2 satisfied.

**Score (same run-dir):** `stratified_pass_at_1 = 0.125` (1/8 pass, 8 completed, 0 errored;
Wilson CI [0.022, 0.471]). Against the spec `pass_rate` constant 0.1875: verdict `below`.

**Per-task smoke verdicts vs `@baseline` (622bdedac572b479):**

| task | class | @baseline | h0008 variant | delta |
|---|---|---|---|---|
| ade-bench-airbnb001 | regression sentinel | PASS | **PASS** | held — no regression |
| ade-bench-asana004 | dropped-rows | FAIL | FAIL | no change |
| ade-bench-asana005 | dropped-rows | FAIL | FAIL | no change |
| ade-bench-asana005-hard | dropped-rows | FAIL | FAIL | no change |
| ade-bench-intercom001 | dropped-rows | FAIL | FAIL | no change |
| ade-bench-ana-eng006 | grain-uniqueness | FAIL | FAIL | no change |
| ade-bench-f1002 | contract-completeness | FAIL | FAIL | no change |
| ade-bench-quickbooks001 | contract-completeness | FAIL | FAIL | no change |

(Per-cell `verifier/reward.txt`: airbnb001=1, all 7 targets=0. `@baseline` rewards for the
same 8 tasks confirm airbnb001=PASS and all 7 targets are among the 17 `@baseline` failures.)

**Smoke gate: NO-GO → back to `hypothesis`.** The `airbnb001` sentinel did NOT regress
(gate's regression condition satisfied), but the gate also requires flipping **at least one**
targeted failure to a pass before promotion to full. The Finalization source-derived-invariant
instruction flipped **zero** of the 7 targeted failures (all still reward=0). No worthwhile
movement on the targeted behavior → not worth committing the full 48-task run. The variant is
behaviorally inert on these failures at xhigh/gpt-5.5: adding the invariant-check prose to the
Finalization stage did not change any targeted outcome.

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: The forked solver README's ONLY change vs codex-ade-dbt-minimal/README.md is the single Finalization source-derived-invariants instruction; leak-guard / no-external-reference prose intact; NO reference to hidden AUTO_*/verifier tests and NO instruction to re-derive the expected answer.
  README diff is a single added paragraph in `## Stage: Finalization` (lines 78a79-90); parenthetical states "NOT against any verifier/AUTO_* test and NOT by re-deriving the expected answer"; Exploration/Implementation/Validation and dependency guardrails untouched.
- DONE: FULL spec diffs baseline.yaml in ONLY experiment: + solver_workflow:; smoke spec adds ONLY benchmark.tasks: [8 targets]; agent.kind=spacedock_solver and runtime=codex preserved.
  `diff specs/baseline.yaml specs/h0008-...yaml` = exactly 2 changed lines (2c2, 11c11); `diff` full vs smoke = only `tasks:` block (23a24-32); kind/runtime unchanged from baseline.
- DONE: Both specs frozen with rk freeze --allow-missing (full + smoke); two-field FULL spec diff and README diff pasted into ### Gate evidence below.
  `rk freeze` wrote h0008-...frozen.yaml and h0008-...smoke.frozen.yaml; evidence block below.

### Gate evidence

FULL spec vs baseline (exactly two fields):

```
2c2
< experiment: ade-bench-baseline # variants: ade-bench-h0001-<slug>
---
> experiment: ade-bench-h0008-finalization-source-derived-invariants # variants: ade-bench-h0001-<slug>
11c11
<   solver_workflow: ./solver_workflows/codex-ade-dbt-minimal # variants repoint to ./solver_workflows/h<NNNN>-<slug>
---
>   solver_workflow: ./solver_workflows/h0008-finalization-source-derived-invariants # variants repoint to ./solver_workflows/h<NNNN>-<slug>
```

SMOKE vs FULL (only the tasks block added):

```
23a24,32
>   tasks: # invariant sub-classes + airbnb001 regression sentinel; ade-bench- prefixed (bare slugs rejected by rk run)
>     - ade-bench-asana004
>     - ade-bench-asana005
>     - ade-bench-asana005-hard
>     - ade-bench-intercom001
>     - ade-bench-ana-eng006
>     - ade-bench-f1002
>     - ade-bench-quickbooks001
>     - ade-bench-airbnb001
```

README diff vs codex-ade-dbt-minimal (single Finalization instruction):

```
78a79,90
> For each model the task creates or changes, before finalizing verify against the
> local source data and the project's declared schema (NOT against any
> verifier/AUTO_* test and NOT by re-deriving the expected answer): (1) no source
> rows are silently dropped — every key present in the upstream source(s) at the
> model's declared grain appears in the output unless the task explicitly filters
> it, reconciling row/key counts to the source; (2) the model is unique at its
> stated grain — `count(*) = count(distinct <grain key>)`, no unexpected join
> fan-out; (3) the output contract is complete — every column declared in the
> model's `schema.yml` is emitted and every model the instruction or project graph
> implies exists, builds, and is populated. Treat any invariant violation as a
> defect in the model logic to fix before finalizing.
>
```

### Summary

Forked `codex-ade-dbt-minimal` to `h0008-finalization-source-derived-invariants` and added the single source-derived-invariants instruction to the `## Stage: Finalization` section only — the one independent variable. Full and smoke specs created from baseline with only the allowed field changes (full: experiment + solver_workflow; smoke additionally adds the 8-task benchmark.tasks block covering the three invariant sub-classes plus the airbnb001 regression sentinel). Both specs frozen with `rk freeze --allow-missing`; leak-guard prose intact, no reference to hidden AUTO_*/verifier tests, no re-derive-expected instruction.

## Stage Report: smoke

- DONE: Smoke run launched DETACHED, polled across turns; all 8 cells completed with 0 errored and `captured > 0` on the cells.
  Run dir `runs/.../809de1a923b89ff6`; result.json `completed=8, errored=0`; every cell `subagent-trace-manifest.json` has `captured = 1`.
- DONE: `rk audit <run-dir> --policy strict` is CLEAN and the `rk score` is paired to that same run-dir; both recorded in `## Smoke result`.
  Audit `summary: {clean: 8, tainted: 0, coverage_missing: 0}`; score `stratified_pass_at_1 = 0.125` on the SAME run-dir.
- DONE: Per-task smoke verdicts vs `@baseline` recorded; named flips and confirmed the sentinel.
  Table in `## Smoke result`: airbnb001 sentinel held PASS→PASS; ALL 7 targeted failures stayed FAIL (zero flips).

### Summary

Smoke executed and exercised the changed Finalization behavior cleanly (8/8 completed, 0 errored,
strict audit clean, captured>0 on every cell), so the score is trustworthy. Result is a go/no-go
NO-GO: `stratified_pass_at_1 = 0.125` (1/8), the `airbnb001` sentinel did not regress, but the
source-derived-invariant Finalization instruction flipped **zero** of the 7 targeted `@baseline`
failures (asana004/005/005-hard, intercom001, ana-eng006, f1002, quickbooks001 all still
reward=0). The change is behaviorally inert on the targeted misses at xhigh/gpt-5.5 — not worth
the full 48-task run. Recommend returning to `hypothesis`.
