---
id: spd0033
title: Stabilize divvy001 (NEW rule) — divvy-staging-test-warn-not-filter
status: smoke
kind: hypothesis
source: "spd0030 fan-out. Bifurcation analysis (_artifacts/flaky-bifurcation-analysis-2026-06-29.md) found divvy001's pass-vs-fail bifurcation. NEW gated directive. forks champion @baseline spd0013. Smoke = divvy001 trials=3 (consistency) + canary f1001."
started: 2026-06-29
completed:
verdict:
score:
worktree:
archived:
---

When a no-filter staging model's column test fails on raw rows, make the test non-blocking (severity: warn) — never add a WHERE that drops rows.

## Smoke
spec `specs/spd0033-divvy-staging-test-warn-not-filter.smoke.frozen.yaml`. TARGET **divvy001** at trials=3 (consistency hold-rate) + canary **f1001**.
GO = divvy001 3/3 AND f1001 holds. NO-GO = divvy001 <3/3 or canary regression → revise directive, re-smoke until exhausted.

## Result
**REV0 SMOKE = NO-GO.** run runs/spd0033-divvy-staging-test-warn-not-filter (rev0): TARGET divvy001 0/3; canary f1001 1/3 (f1001 itself ~60%-flaky, weak canary). Diagnosis: directive NOT engaged — all 3 draws built `PASS=14 WARN=0` and row count 426886 (short by 1) → solver STILL filtered the bad row (kept all tests green) instead of severity:warn. "Talks but doesn't do." REV1: forceful HARD ANTI-PATTERN. **REV1 = NO-GO** (divvy001 0/3 again, still filtered — prose doesn't engage the reflex; canary f1001 2/3 own-variance). REV2: a different mechanism — MANDATORY post-build VALIDATION GATE (count staging vs source; if short, delete the filter + warn + rebuild). Re-smoking (rev2).
