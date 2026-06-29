---
id: spd0031
title: Stabilize quickbooks003 (NEW rule) — qb003-reuse-shipped-upstream
status: smoke
kind: hypothesis
source: "spd0030 fan-out. Bifurcation analysis (_artifacts/flaky-bifurcation-analysis-2026-06-29.md) found quickbooks003's pass-vs-fail bifurcation. NEW gated directive. forks champion @baseline spd0013. Smoke = quickbooks003 trials=3 (consistency) + canary quickbooks002."
started: 2026-06-29
completed:
verdict:
score:
worktree:
archived:
---

Reuse shipped int_/stg_ upstream — build ONLY the missing leaf via narrow --select (no +); never rebuild/edit a pre-existing upstream model or its casts.

## Smoke
spec `specs/spd0031-qb003-reuse-shipped-upstream.smoke.frozen.yaml`. TARGET **quickbooks003** at trials=3 (consistency hold-rate) + canary **quickbooks002**.
GO = quickbooks003 3/3 AND quickbooks002 holds. NO-GO = quickbooks003 <3/3 or canary regression → revise directive, re-smoke until exhausted.

## Result
**REV0 SMOKE = NO-GO (backfired).** run runs/spd0031-qb003-reuse-shipped-upstream (rev0): TARGET quickbooks003 0/3 (worse than ~65% baseline); canary quickbooks002 3/3. Diagnosis: directive ENGAGED (ran narrow --select) but it FAILED on a broken upstream package-staging model → solver rebuilt the chain → widened period set (the exact fail mode). The bifurcation premise (intermediates pre-materialized) doesn't hold in a clean run. REV1: handle broken-package case via R3 stub + forbid widening the date-spine (emit only periods with fact rows). Re-smoking.
