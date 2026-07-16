---
id:
title: gpt-5.5 @ high — spacedock v0.25 (spacedock release)
status: queued
source: spacedock v0.25.0 release (captain-filed 2026-07-16)
started:
completed:
verdict:
score:
worktree:
issue:
pr:
trigger: spacedock-release
model: gpt-5.5
effort: high
spacedock-version: v0.25.0 (601c3f53)
draws: []
pass-at-1:
pass-at-1-sd:
tokens-total:
mean-session-sec:
artifact-url:
---

Regression run for the spacedock v0.25.0 release: pinned config (spacedock harness +
dab0022 semi-structured-rules README, gpt-5.5 @ high, batch query mode), 5 full DAB
draws as ONE rk run (`trials: 5`, `concurrency.trials: 4`). Subject checkout confirmed
at tag v0.25.0, commit 601c3f53. Compares against the v0.22 baseline row (0.7433) —
note the ~+0.04 plugin-version effect when reading the delta.

## Acceptance criteria

**AC-1 — Five clean (or disclosed-substitution) full draws exist under `dab/runs/`.**
Verified by: the 5 entries in `draws` each resolve to a completed trial in the run dir.

**AC-2 — pass@1, tokens, and timing in frontmatter match the extractor output.**
Verified by: re-running `extract_benchmark_data.py` over the run dir.

**AC-3 — The run's row is live on the regression Artifacts page at the recorded URL.**
Verified by: `artifact-url` set; row visible with matching numbers.

## Draws

| draw | experiment | stratified pass@1 | notes |
|------|-----------|-------------------|-------|

## Taint audit

## Publication
