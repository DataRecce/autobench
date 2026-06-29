---
id: spd0037
title: Stabilize apple_store001 (SHARPEN rule) — applestore-raw-grouping-key
status: smoke
kind: hypothesis
source: "spd0030 fan-out. Bifurcation analysis (_artifacts/flaky-bifurcation-analysis-2026-06-29.md) found apple_store001's pass-vs-fail bifurcation. SHARPEN gated directive. forks champion @baseline spd0013. Smoke = apple_store001 trials=3 (consistency) + canary google_play001."
started: 2026-06-29
completed:
verdict:
score:
worktree:
archived:
---

Sharpen the preserve-raw-grouping-key sub-note: build the reporting grain from the DISTINCT RAW key, no terminal GROUP BY/DISTINCT on the canonicalized lookup name.

## Smoke
spec `specs/spd0037-applestore-raw-grouping-key.smoke.frozen.yaml`. TARGET **apple_store001** at trials=3 (consistency hold-rate) + canary **google_play001**.
GO = apple_store001 3/3 AND google_play001 holds. NO-GO = apple_store001 <3/3 or canary regression → revise directive, re-smoke until exhausted.

## Result
**REV0 SMOKE = NO-GO (canary bleed).** run runs/spd0037-applestore-raw-grouping-key/3c649d47ca73fa8c: TARGET apple_store001 **3/3** (stabilized!) BUT canary google_play001 **1/3** (from ~98% rock-solid) — the raw-grouping-key directive OVER-FIRES onto the sibling google_play report (confirmed: failing draw engaged "raw grouping"/"reporting-grain"/"canonical"). Target fix works; gate too broad. REV1: narrow the gate to fire ONLY when count(distinct raw) > count(distinct canonical) (genuine spelling variants); else group normally. Re-smoking.
