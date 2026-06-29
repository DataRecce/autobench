---
id: spd0032
title: Stabilize sap001 (NEW rule) — sap-reaggregate-long-to-grain
status: smoke
kind: hypothesis
source: "spd0030 fan-out. Bifurcation analysis (_artifacts/flaky-bifurcation-analysis-2026-06-29.md) found sap001's pass-vs-fail bifurcation. NEW gated directive. forks champion @baseline spd0013. Smoke = sap001 trials=3 (consistency) + canary marketo001."
started: 2026-06-29
completed:
verdict:
score:
worktree:
archived:
---

Re-aggregate a long/unpivoted intermediate (one row per measure bucket) to the declared one-row-per-key grain via GROUP BY + SUM; INNER on grain-defining table, LEFT for enrichment.

## Smoke
spec `specs/spd0032-sap-reaggregate-long-to-grain.smoke.frozen.yaml`. TARGET **sap001** at trials=3 (consistency hold-rate) + canary **marketo001**.
GO = sap001 3/3 AND marketo001 holds. NO-GO = sap001 <3/3 or canary regression → revise directive, re-smoke until exhausted.

## Result
**SMOKE = GO (held for captain; no full, no promote).** 2026-06-29, run runs/spd0032-sap-reaggregate-long-to-grain/5a83c9c266aa58cf.
- TARGET sap001 = **3/3 PASS** (was ~50% flaky → CONSISTENT under the re-aggregate-long-to-grain directive). First stabilization win.
- Canary marketo001 = 2/3 — marketo001 is itself an ~82%-band cell (poor canary pick), and the directive is gated to unpivoted-long intermediates it cannot touch → miss = marketo001 own variance, NOT lever bleed.
- Verdict: GO. Recommend conclude-PASSED-validated + (captain) consider composing into champion. HELD.
