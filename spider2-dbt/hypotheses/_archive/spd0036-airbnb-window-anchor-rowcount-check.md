---
id: spd0036
title: Stabilize airbnb001 (SHARPEN rule) — airbnb-window-anchor-rowcount-check
status: conclude
kind: hypothesis
source: "spd0030 fan-out. Bifurcation analysis (_artifacts/flaky-bifurcation-analysis-2026-06-29.md) found airbnb001's pass-vs-fail bifurcation. SHARPEN gated directive. forks champion @baseline spd0013. Smoke = airbnb001 trials=3 (consistency) + canary mrr001."
started: 2026-06-29
completed:
verdict: PASSED-PROMOTED-into-spd0038
score:
worktree:
archived: 2026-06-29T17:39:54Z
---

Sharpen the rolling-window rule: anchor to single MAX source date, emit exactly one window, and self-check row count == distinct group values (not source dates).

## Smoke
spec `specs/spd0036-airbnb-window-anchor-rowcount-check.smoke.frozen.yaml`. TARGET **airbnb001** at trials=3 (consistency hold-rate) + canary **mrr001**.
GO = airbnb001 3/3 AND mrr001 holds. NO-GO = airbnb001 <3/3 or canary regression → revise directive, re-smoke until exhausted.

## Result
**REV0 SMOKE = NO-GO.** run runs/spd0036-airbnb-window-anchor-rowcount-check/069c5604964b92b2: airbnb001 2/3 (F,P,P — same as its ~2/3 baseline, no consistency gain); canary mrr001 3/3. The 1 failing draw over-emitted (~10851/17499 rows = full history) — the window filter was skipped under --full-refresh (left inside is_incremental()); the advisory row-count check was not heeded. REV1: MANDATORY validation gate. **REV1 = NO-GO** (airbnb001 2/3 again, over-emit recurs in 1 draw; mrr001 3/3). REV2: ELIMINATE the incremental path — plain table + unconditional max-date WHERE. **REV2 SMOKE = GO** (run runs/spd0036-airbnb-window-anchor-rowcount-check/5a20c7cde31791dc): airbnb001 **3/3**, canary mrr001 3/3. Removing the is_incremental() full-refresh bypass made it consistent (rev0 2/3 → rev1 2/3 → rev2 3/3). HELD for captain.
