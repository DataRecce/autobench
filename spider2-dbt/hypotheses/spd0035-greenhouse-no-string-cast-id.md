---
id: spd0035
title: Stabilize greenhouse001 (SHARPEN rule) — greenhouse-no-string-cast-id
status: smoke
kind: hypothesis
source: "spd0030 fan-out. Bifurcation analysis (_artifacts/flaky-bifurcation-analysis-2026-06-29.md) found greenhouse001's pass-vs-fail bifurcation. SHARPEN gated directive. forks champion @baseline spd0013. Smoke = greenhouse001 trials=3 (consistency) + canary hubspot001."
started: 2026-06-29
completed:
verdict:
score:
worktree:
archived:
---

Sharpen the existing 'never re-type an id' rule: never wrap an upstream id in type_string()/cast-as-varchar — the grader compares by type-sensitive equality.

## Smoke
spec `specs/spd0035-greenhouse-no-string-cast-id.smoke.frozen.yaml`. TARGET **greenhouse001** at trials=3 (consistency hold-rate) + canary **hubspot001**.
GO = greenhouse001 3/3 AND hubspot001 holds. NO-GO = greenhouse001 <3/3 or canary regression → revise directive, re-smoke until exhausted.

## Result
_(autonomous — recorded after smoke; HELD at smoke, no full/promote)_
