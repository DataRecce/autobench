---
id: spd0036
title: Stabilize airbnb001 (SHARPEN rule) — airbnb-window-anchor-rowcount-check
status: smoke
kind: hypothesis
source: "spd0030 fan-out. Bifurcation analysis (_artifacts/flaky-bifurcation-analysis-2026-06-29.md) found airbnb001's pass-vs-fail bifurcation. SHARPEN gated directive. forks champion @baseline spd0013. Smoke = airbnb001 trials=3 (consistency) + canary mrr001."
started: 2026-06-29
completed:
verdict:
score:
worktree:
archived:
---

Sharpen the rolling-window rule: anchor to single MAX source date, emit exactly one window, and self-check row count == distinct group values (not source dates).

## Smoke
spec `specs/spd0036-airbnb-window-anchor-rowcount-check.smoke.frozen.yaml`. TARGET **airbnb001** at trials=3 (consistency hold-rate) + canary **mrr001**.
GO = airbnb001 3/3 AND mrr001 holds. NO-GO = airbnb001 <3/3 or canary regression → revise directive, re-smoke until exhausted.

## Result
_(autonomous — recorded after smoke; HELD at smoke, no full/promote)_
