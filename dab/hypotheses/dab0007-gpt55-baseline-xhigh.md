---
id: dab0007
title: gpt-5.5 xhigh baseline anchor (concurrency 4)
status: full
kind: hypothesis
source: captain request 2026-06-16 — establish the codex/gpt-5.5 reference at xhigh reasoning
started:
completed:
verdict:
score:
worktree:
---

## Hypothesis

This is a **baseline anchor**, not a solver-README lever. It re-runs the codex/gpt-5.5 solver on
the **unchanged seed baseline README** (`../solver_workflows/spacedock-readme-baseline`) across all
12 datasets / 54 queries, to establish a clean gpt-5.5 reference point at the **xhigh** reasoning
tier — matching the Opus incumbent's `xhigh` setting (the Opus `@baseline` was run as
`spacedock-opus-4-8-xhigh-hint`).

It differs from the prior anchor (`specs/dab-anchor-codex.yaml`, gpt-5.5 @ high) in exactly two
knobs:

- `agent.reasoning_effort: high → xhigh`
- `concurrency.trials: 2 → 4` (throughput only; `trials: 1` unchanged — single run per cell)

The solver README, model (gpt-5.5), runtime (codex), dataset set, hints, and `data_root` are all
held fixed. No README change ⇒ no leak-guard / smoke needed; this follows the README's
**anchor / first-run skips smoke** path (direct full run).

There is no FAIL→PASS flip claim — the deliverable is the run-dir + its clean-audited stratified
Pass@1, read against the current Opus `@baseline` (~0.65 / 0.6536) and the prior gpt-5.5 @ high
anchor (`codex-dab-baseline`).

## Acceptance criteria

**AC-1 — The full spec differs from `specs/dab-anchor-codex.yaml` only in `experiment:`,
`agent.reasoning_effort` (xhigh), and `concurrency.trials` (4).**
Verified by: `diff specs/dab-anchor-codex.yaml specs/dab0007-gpt55-baseline-xhigh.yaml`.

**AC-2 — The recorded stratified Pass@1 is paired with a clean strict audit on the same run-dir.**
Verified by: `rk score <run-dir>` cites `rk audit <run-dir> --policy strict`.

**AC-3 — All 12 datasets / 54 query-cells ran** (no silent dataset/query drop).
Verified by: `rk run --explain` on the frozen spec shows the full cell list before launch; the
scored run-dir reports 54 cells.

## Run plan (anchor — for the full-stage ensign)

1. `cp specs/dab-anchor-codex.yaml specs/dab0007-gpt55-baseline-xhigh.yaml`; set
   `experiment: dab0007-gpt55-baseline-xhigh`, `agent.reasoning_effort: xhigh`,
   `concurrency.trials: 4`. Leave `solver_workflow: ./solver_workflows/spacedock-readme-baseline`
   (baseline README — this is an anchor, NOT a forked variant).
2. `uv run --project ../razorback rk freeze --allow-missing specs/dab0007-gpt55-baseline-xhigh.yaml`.
3. `uv run --project ../razorback rk run specs/dab0007-gpt55-baseline-xhigh.frozen.yaml --explain`
   ($0, foreground) — confirm all 12 datasets / 54 cells survive.
4. Launch DETACHED (never foreground): `drivers/rk-run-detached.sh dab0007-full
   specs/dab0007-gpt55-baseline-xhigh.frozen.yaml run`. Return the handle path
   (`runs/.rk-handles/dab0007-full-<ts>/`) immediately; do NOT wait for the run.

## Run result

(pending — detached full run in flight; handle `runs/.rk-handles/dab0007-full-20260616-181559`)

## Behavioral analysis

## Verdict

## Stage Report: full

- DONE: Spec prepared + frozen; `diff specs/dab-anchor-codex.yaml specs/dab0007-gpt55-baseline-xhigh.yaml` shows ONLY experiment=dab0007-gpt55-baseline-xhigh, agent.reasoning_effort=xhigh, concurrency.trials=4 (AC-1).
  Diff = exactly 3 hunks (lines 3/8/38); solver_workflow stays `solver_workflows/spacedock-readme-baseline`; all 12 tasks intact in frozen spec.
- DONE: rk run --explain confirms all 12 datasets / 54 query-cells survive before launch (AC-3).
  `rk run ...frozen.yaml --explain` reports `- Tasks: 54`; sample task `DEPS_DEV_V1-q1`; awk count of `benchmark.tasks` = 12 datasets.
- DONE: Detached full run launched via drivers/rk-run-detached.sh; handle path returned.
  `drivers/rk-run-detached.sh dab0007-full specs/dab0007-gpt55-baseline-xhigh.frozen.yaml run` → handle `runs/.rk-handles/dab0007-full-20260616-181559` (pid 801782, alive; `done` sentinel absent = in progress). Did NOT wait — FO owns the wait.

### Summary

Anchor spec built by copying `dab-anchor-codex.yaml` and changing exactly three knobs (experiment, reasoning_effort high→xhigh, concurrency.trials 2→4); baseline README, model gpt-5.5, codex runtime, 12 tasks, hints, and data_root all held fixed — no README change, so no smoke/gatekeeper (anchor path). Frozen and --explain confirmed 12 datasets / 54 cells. Launched detached at handle `runs/.rk-handles/dab0007-full-20260616-181559`; specs committed (cb6e82b), runs/ gitignored. Run is long (30 min–8 hr+); first officer owns the wait via the handle's `done` sentinel.
