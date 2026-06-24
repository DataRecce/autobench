---
id: spd0001
title: Establish @baseline — full run of the spider2-dbt-baseline output-contract solver
status: hypothesis
kind: hypothesis
source: commission seed (loop-anchor; no scored full board exists yet)
started:
completed:
verdict:
score: 1.0
worktree:
---

## Hypothesis

This is the **loop anchor**, not a lever test. There is no scored full board for spider2-dbt yet —
only two 6-task smokes (`docs/smoke6-2026-06-24.md` 0/6 on the ade README; `docs/smoke6-output-contract-2026-06-24.md`
2/6 on the output-contract README). The output-contract solver `solver_workflows/spider2-dbt-baseline`
is the right seed README, but its pass rate over the full 61 duckdb-runnable tasks is unknown.

**Claim:** running `spider2-dbt-baseline` (codex/gpt-5.5, `reasoning_effort: xhigh`, `trials: 1`,
`concurrency.trials: 4`) over the full 61-task board produces a clean, scored run that we can promote
to `@baseline` — the champion every future hypothesis diffs against. No README change is made; the
spec is `specs/full-baseline.frozen.yaml` as-is.

This entity follows the **anchor exception**: `propose → full`, skipping `smoke` (the README is the
seed, there is nothing to pre-flight). It exists so the FO's first action on the loop is unambiguous.

Target tasks: all 61 (the full board).

## Pre-smoke Decision-Fork Probe

N/A — no lever, no fork. This is the baseline-establishing run.

## Acceptance criteria

**AC-1 — Clean strict audit, no `coverage_missing`, no taint.**
Verified by: `rk audit <run-dir> --policy strict` reports 0 coverage_missing, 0 tainted. Any
build-time preflight failure or packager crash HALTS + escalates (packaging health, see README →
*Packaging / preflight health*) — it is not a result.

**AC-2 — A real scored pass rate is recorded and promoted to `@baseline`.**
Verified by: `rk score <run-dir>` emits `stratified_pass_at_1` (= flat pass rate over the scored
tasks); then
`export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml` →
`rk baseline promote <run-dir>` → `rk registry add run baseline <run-dir>` binds `@baseline`.

**AC-3 — The per-task ledger is captured** so future hypotheses can pick currently-FAIL targets and
currently-PASS canaries.
Verified by: `_artifacts/task-gap-ranking.md` is re-derived from this run's `per_trial_outcomes.json`
(which tasks pass, which fail, the failure class for the fails).

## Gatekeeper review

(Anchor run — gatekeeper N/A; no README diff, no smoke spec. The FO still confirms the full spec is
unmodified vs `specs/full-baseline.frozen.yaml` and `agent.kind: spacedock_solver` / `runtime: codex`.)

## Smoke result

N/A — anchor skips smoke (`propose → full`).

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
