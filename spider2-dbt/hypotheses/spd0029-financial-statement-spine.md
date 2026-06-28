---
id: spd0029
title: Cumulative financial-statement spine — Retained Earnings = cumulative P&L to month-end (C2)
status: smoke
kind: hypothesis
source: "spd0026 fan-out, family C2 (NEW). xero001/xero_new001/xero_new002 balance-sheet targets: spine to last activity, Retained Earnings = cumulative P&L (no FY-end pin / no current-year-earnings split), stock accounts forward-carried. forks champion @baseline spd0013."
started: 2026-06-28
completed:
verdict:
score:
worktree:
archived:
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
_(autonomous — recorded after smoke; HELD at smoke, no full/promote)_
