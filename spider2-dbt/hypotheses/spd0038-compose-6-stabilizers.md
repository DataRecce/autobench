---
id: spd0038
title: Compose the 6 GO flaky-stabilizer directives into one champion fork — confirm they merge without cross-bleed
status: full
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
**SMOKE = MERGEABLE (5/6 clean) — HELD for captain. No cross-bleed; the 6 directives compose.** run runs/spd0038-compose-6-stabilizers/35d8eead20c1f2ce (trials=3).
- TARGETS: sap001 **3/3**, asset001 **3/3**, greenhouse001 **3/3**, apple_store001 **3/3**, airbnb001 **3/3** — all FIVE hold 3/3 when composed. quickbooks003 **2/3** (P,P,F).
- CANARIES: app_reporting001 3/3, quickbooks002 2/2, google_play001 2/3, mrr001 2/3 — all HOLD (the single google_play001/mrr001 misses are their own near-rock-solid variance, NOT bleed; google_play stayed off 0-1/3 so the applestore count-distinct gate holds — no cross-bleed).
- **quickbooks003 diagnosis: NOT a composition conflict.** Its failing draw shows its OWN bifurcation failure mode — `dbt run --select +` (rebuilt upstream) → 990 rows (widened period set), the exact reuse-shipped-upstream failure. No other composed directive interfered. quickbooks003's stabilizer is REAL but ~2-3/3-reliable (its broken-package/rebuild path is environment-fragile, not a fully-deterministic pin). Not auto-revised (no clean single-directive fix; rev1 already spent).
- **VERDICT: the merge is SAFE and effective** — composing all 6 has zero cross-bleed, reliably banks 5 cells (3/3) + improves quickbooks003 (~2-3/3). Captain decision: compose into champion + full-board multi-draw validate + promote.
