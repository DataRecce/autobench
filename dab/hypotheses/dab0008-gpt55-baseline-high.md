---
id: dab0008
title: gpt-5.5 high baseline (tier control vs dab0007 xhigh)
status: analyze
kind: hypothesis
source: captain request 2026-06-17 — settle the reasoning-tier question (high vs xhigh) with a clean apples-to-apples run
started:
completed:
verdict:
score:
worktree:
---

## Hypothesis

A **tier-control anchor**: re-run the codex/gpt-5.5 solver on the unchanged baseline README across
all 12 datasets / 54 queries at **`reasoning_effort: high`**, under conditions *identical* to
`dab0007` (gpt-5.5 @ xhigh) — same model, runtime, datasets, hints, `data_root`, concurrency 4,
`trials: 1`, and the same post-postgres-fix infra. The ONLY difference from dab0007 is the tier.

**Why:** the existing `high` anchor (`codex-dab-baseline`, 0.5836) is **not** a fair comparison — it
ran *before* the dab-postgres restart fix (PANCANCER was infra-0/3 there) and was missing a
bookreview cell (53/54). The behavioral study (`_artifacts/opus-vs-gpt55-failure-behavior.md`) found
that gpt-5.5 **regressed all 3 contested flip-targets going high→xhigh** (agnews-q4, stockmarket-q4,
crmarenapro-q2 were PASS@high, FAIL@xhigh) — extra reasoning over-rationalized the wrong branch or
abstained where high improvised. This run tests whether that tier effect is real on a clean board.

**Falsifiable claim:** under identical conditions, gpt-5.5 @ high will *not* underperform @ xhigh on
DAB; specifically the 3 contested flip-targets should re-pass at high. If high ≥ xhigh on stratified
Pass@1 AND re-passes ≥2 of the 3 contested targets, the tier effect is confirmed and `high` becomes
the recommended tier for the loop.

## Acceptance criteria

**AC-1 — The full spec differs from `specs/dab0007-gpt55-baseline-xhigh.yaml` only in `experiment:`
and `agent.reasoning_effort` (high).**
Verified by: `diff specs/dab0007-gpt55-baseline-xhigh.yaml specs/dab0008-gpt55-baseline-high.yaml`.

**AC-2 — Recorded stratified Pass@1 paired with a clean strict audit on the same run-dir.**

**AC-3 — All 12 datasets / 54 cells ran** (verified via `--explain` + scored cell count).

## Run plan (tier control — for the full-stage ensign)

1. `cp specs/dab0007-gpt55-baseline-xhigh.yaml specs/dab0008-gpt55-baseline-high.yaml`; set
   `experiment: dab0008-gpt55-baseline-high`, `agent.reasoning_effort: high`. Change NOTHING else
   (concurrency.trials stays 4, solver_workflow stays the baseline, all 12 tasks, trials: 1).
2. `uv run --project ../razorback rk freeze --allow-missing specs/dab0008-gpt55-baseline-high.yaml`.
3. `uv run --project ../razorback rk run specs/dab0008-gpt55-baseline-high.frozen.yaml --explain`
   ($0, foreground) — confirm all 12 datasets / 54 cells survive.
4. Launch DETACHED: `drivers/rk-run-detached.sh dab0008-full
   specs/dab0008-gpt55-baseline-high.frozen.yaml run`. Return the handle path immediately; do NOT wait.

## Run result

- Spec frozen: `specs/dab0008-gpt55-baseline-high.frozen.yaml` (from dab0007 xhigh; only
  `experiment` + `reasoning_effort: high` changed — diff confirmed exactly 2 lines).
- `--explain`: 12 datasets / 54 query-cells materialized (all of agnews, bookreview,
  crmarenapro, DEPS_DEV_V1, GITHUB_REPOS, googlelocal, music_brainz_20k, PANCANCER_ATLAS,
  PATENTS, stockindex, stockmarket, yelp).
- Detached full run launched 2026-06-17:
  handle `runs/.rk-handles/dab0008-full-20260617-022427/` (pid 1259615). FO owns the wait;
  on `done` rc=0: `rk audit <run-dir> --policy strict` + `rk score <run-dir> --format json`.

## Behavioral analysis

## Verdict

## Stage Report: full

- DONE: Spec prepared + frozen; diff shows ONLY experiment + reasoning_effort:high (AC-1)
  `diff` output = exactly 2 hunks (experiment line, reasoning_effort line); frozen spec written.
- DONE: rk run --explain confirms all 12 datasets / 54 query-cells survive before launch (AC-3)
  --explain reported `Tasks: 54`; materialized tasks dir = 54 cells across 12 distinct datasets.
- DONE: Detached full run launched via drivers/rk-run-detached.sh; handle path returned
  `runs/.rk-handles/dab0008-full-20260617-022427/` (pid 1259615 alive, done absent). Did NOT wait.

### Summary

Created the tier-control spec by copying dab0007 (gpt-5.5 @xhigh) and flipping only the
experiment name and reasoning_effort to high — everything else (concurrency.trials=4, all 12
tasks, trials:1, baseline solver_workflow, gpt-5.5/codex) untouched, confirmed by a 2-line diff.
Froze, validated 12 datasets / 54 cells via --explain, and launched the detached full run.
Committed the spec + frozen spec; runs/ stays gitignored. FO owns the wait + audit/score.

## Stage Report: full (cycle 2 — relaunch)

- DONE: rk run --explain on the frozen spec confirms all 12 datasets / 54 cells (high tier, trials:1)
  --explain reported `Tasks: 54`, `Concurrency: 4`; frozen spec shows model gpt-5.5,
  reasoning_effort: high, trials: 1, experiment dab0008-gpt55-baseline-high.
- DONE: Detached full run RELAUNCHED fresh (prior pid 1259615 was intentionally stopped by captain)
  handle `runs/.rk-handles/dab0008-full-20260617-150847/` (pid 2434887 alive, done absent). Did NOT wait.

### Summary

Relaunched the dab0008 high-tier control fresh after the captain stopped the prior launch.
Re-confirmed 54 cells / 12 datasets / trials:1 via --explain on the unchanged frozen spec,
then launched detached. New handle: runs/.rk-handles/dab0008-full-20260617-150847/. FO owns
the wait + strict audit + score; runs/ stays gitignored so nothing to commit beyond this report.
