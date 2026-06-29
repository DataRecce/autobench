---
id: spd0038
title: Compose the 6 GO flaky-stabilizer directives into one champion fork — confirm they merge without cross-bleed
status: smoke
kind: hypothesis
source: "spd0030 follow-up (captain-directed). The 6 GO stabilizers (spd0031 qb003 reuse-shipped-upstream, spd0032 sap001 re-aggregate-long-to-grain, spd0034 asset001 round-final-product, spd0035 greenhouse001 no-string-cast-id, spd0036 airbnb001 plain-table, spd0037 apple_store001 raw-key-gated) were each validated in ISOLATION. This merges all 6 (winning revs) into one champion fork and smokes them together to confirm they compose without interference/bleed before any full-board promote."
started: 2026-06-29
completed:
verdict:
score:
worktree:
archived:
---

The 6 GO directives sit at disjoint locations in the champion README (Implementation gated-rules ×2, G3 ×2,
G2 ×2), so they should compose. This hypothesis is the composition check: champion + all 6 (each at its
winning revision) in one fork (`solver_workflows/spd0038-compose-6-stabilizers`, +11 lines vs champion,
all 6 signatures present, leak-guard intact).

## Smoke (merge-validation)
spec `specs/spd0038-compose-6-stabilizers.smoke.frozen.yaml`, trials=3 (30 cells).
- TARGETS (each must stay 3/3 when composed): quickbooks003, sap001, asset001, greenhouse001, apple_store001, airbnb001
- CANARIES (must hold — cross-bleed sentinels): google_play001 (the applestore-bleed sentinel), quickbooks002, mrr001, app_reporting001
- **MERGEABLE = all 6 targets 3/3 AND canaries hold.** A target <3/3 or a canary drop = a composition
  conflict to diagnose (which directive interferes with which).

## Result
_(recorded after smoke; HELD — no full board, no promote)_
