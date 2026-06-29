---
id: spd0034
title: Stabilize asset001 (NEW rule) — asset-round-final-product-only
status: smoke
kind: hypothesis
source: "spd0030 fan-out. Bifurcation analysis (_artifacts/flaky-bifurcation-analysis-2026-06-29.md) found asset001's pass-vs-fail bifurcation. NEW gated directive. forks champion @baseline spd0013. Smoke = asset001 trials=3 (consistency) + canary recharge001."
started: 2026-06-29
completed:
verdict:
score:
worktree:
archived:
---

Round ONLY the final derived product (aggregated price × magnitude) to 2dp; keep intermediate prices full-precision; never round a per-unit price before multiplying, never leave the final value unrounded.

## Smoke
spec `specs/spd0034-asset-round-final-product-only.smoke.frozen.yaml`. TARGET **asset001** at trials=3 (consistency hold-rate) + canary **recharge001**.
GO = asset001 3/3 AND recharge001 holds. NO-GO = asset001 <3/3 or canary regression → revise directive, re-smoke until exhausted.

## Result
_(autonomous — recorded after smoke; HELD at smoke, no full/promote)_
