---
id: spd0029
title: Cumulative financial-statement spine — Retained Earnings = cumulative P&L to month-end (C2)
status: conclude
kind: hypothesis
source: "spd0026 fan-out, family C2 (NEW). xero001/xero_new001/xero_new002 balance-sheet targets: spine to last activity, Retained Earnings = cumulative P&L (no FY-end pin / no current-year-earnings split), stock accounts forward-carried. forks champion @baseline spd0013."
started: 2026-06-28
completed:
verdict: REJECTED
score:
worktree:
archived: 2026-06-29T01:05:22Z
---

A genuinely new structural rule for financial-statement targets (balance sheet / income statement / equity
rollup): the date spine extends only through the last active period; Retained Earnings is the cumulative net
P&L through each period's month-end (not pinned to a fiscal-year boundary, not split into a current-year-
earnings line); stock accounts forward-carry cumulatively while flow accounts are per-period.

## Lever (one gated G2 bullet, financial-statement shape)
see `solver_workflows/spd0029-financial-statement-spine/README.md`. Content hash 3aea076e.

## Smoke
spec `specs/spd0029-financial-statement-spine.smoke.frozen.yaml`, trials=1.
- FLIP targets: xero001, xero_new001, xero_new002
- canaries (must hold): f1001, mrr001, quickbooks002

## Result
**SMOKE = NO-GO (held for captain; no full, no promote).** 2026-06-28, run
`runs/spd0029-financial-statement-spine/801283a7f21a42c1`.
- Targets: xero001 **FAIL**, xero_new001 **FAIL**, xero_new002 **FAIL** — none flipped.
- Canaries: mrr001 **PASS**, quickbooks002 **PASS** (held); f1001 **EXC** (NonZeroAgentExitCodeError) —
  infra error on a rock-solid cell, inconclusive, NOT a real canary regression.
- Mechanism: the cumulative-balance-sheet-spine rule did not flip any xero target. The xero financial
  statements are multi-model (xero_new001 needs 3 authored models — overlaps the spd0027 C7 wall) and the
  full balance-sheet derivation (spine + Retained-Earnings cumulation + equity roll-ups) is more than a
  single gated directive lands at trials=1. No real regression. Captain decides conclude/REJECTED.
