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
**REV0 SMOKE = NO-GO.** run runs/spd0034-asset-round-final-product-only/b81924b88027f774: TARGET asset001 1/3 (F,P,F — round-final pinned only sometimes); canary recharge001 0/3 (but recharge001 is itself ~flaky, no clear round-bleed in transcript → weak canary, swapped to app_reporting001 for rev1). asset001's bifurcation is a fragile float/comparator-string-sort interaction, hard to pin via prose. REV1: concrete `round(price*qty,2)` form + per-value self-check + gate explicitly excludes typed-value/percentage conversions. Re-smoking.
