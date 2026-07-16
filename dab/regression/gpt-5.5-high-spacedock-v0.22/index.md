---
id:
title: gpt-5.5 @ high — spacedock v0.22 baseline
status: analysis
source: backfill (dab/runs/codex-dab-spacedock-high)
started: 2026-07-16
completed:
verdict:
score:
worktree:
issue:
pr:
trigger: baseline
model: gpt-5.5
effort: high
spacedock-version: v0.22
draws:
  - codex-dab-spacedock-high/run-001
  - codex-dab-spacedock-high/run-002
  - codex-dab-spacedock-high/run-003
  - codex-dab-spacedock-high/run-004
  - codex-dab-spacedock-high/run-005
pass-at-1: 0.7433
pass-at-1-sd: 0.0488
tokens-total: 58274094
mean-session-sec: 637
artifact-url:
---

Backfill of the original pinned-config baseline: spacedock harness + dab0022
semi-structured-rules README, gpt-5.5 @ high, 5-run merge imported from the CAIS
leaderboard submission (`leaderboard_submissions/raw_logs`), consolidated at
`dab/runs/codex-dab-spacedock-high/`. No benchmark runs are launched for this entity —
analysis verifies the recorded numbers against the run dirs, then publishes.

## Acceptance criteria

**AC-1 — Five clean (or disclosed-substitution) full draws exist under `dab/runs/`.**
Verified by: `dab/runs/codex-dab-spacedock-high/run-001..run-005` present with results.

**AC-2 — pass@1, tokens, and timing in frontmatter match the extractor output.**
Verified by: numbers match `codex-dab-spacedock-high/summary.json` and the compare-page
extractor row (`strat 0.7433, sd 0.0488, tokTotal 58274094, meanSec 637`).

**AC-3 — The run's row is live on the regression Artifacts page at the recorded URL.**
Verified by: `artifact-url` set; row visible with matching numbers and caveats.

## Draws

| draw | experiment | stratified pass@1 | notes |
|------|-----------|-------------------|-------|
| 1 | codex-dab-spacedock-high/run-001 | 0.7675 | |
| 2 | codex-dab-spacedock-high/run-002 | 0.7985 | |
| 3 | codex-dab-spacedock-high/run-003 | 0.7058 | |
| 4 | codex-dab-spacedock-high/run-004 | 0.6675 | |
| 5 | codex-dab-spacedock-high/run-005 | 0.7771 | PATENTS is a disclosed fresh-draw substitution (leaderboard README note 4) |

Mean 0.7433 · sd 0.0488 · min 0.6675 · max 0.7985 · median 0.7675

## Caveats (travel with this row on the page)

- Spacedock plugin **v0.22** — plugin version shifts scores ~+0.04 (v0.24 vs older), so
  deltas against v0.24 rows are partly harness-version, not model.
- CAIS-style 5-run merge imported from the leaderboard submission, not an rk-native sweep.
- PATENTS run-005 is a disclosed fresh-draw substitution.

## Taint audit

_(analysis stage fills this in)_

## Publication

_(published stage fills this in)_
