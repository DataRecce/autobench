---
id: spd0022
title: Focused C1-only contract — does narrowing the contract to one template recover reliability across the C1 family?
status: hypothesis
kind: hypothesis
source: "spd0021 trials=3 found the BROAD 7-template gated contract does not compose (1/13 leads reliable: asana001 2/3); spd0011 showed a FOCUSED single-template contract works (airbnb 2/2). This isolates: a contract with ONLY the C1 entity-completeness template, on the C1 family, trials=3. Forks champion spd0013."
started: 2026-06-28
completed:
verdict:
score:
worktree:
---

## Hypothesis

spd0021 (broad 7-template gated contract) trials=3 = only **asana001 landed (2/3)**; the other 12 leads
0–1/3. spd0011 showed a **focused single-template** contract makes its rule reliably obeyed (airbnb 2/2).
**Claim:** narrowing the contract to ONLY the **C1 entity/reference-completeness** template recovers
reliability across the C1 family (asana001's siblings provider001/intercom001/netflix001/hive001 were 0/3
under the broad contract, possibly because the worker's attention was split across 7 templates).

**Single change:** fork champion `spd0013`, add a gated Implementation Contract stage with ONLY the C1
template (entity/reference-completeness: drive FROM the base/dimension relation, LEFT-attach metrics/
crosswalk, keep EVERY base-set row, never INNER-from-aggregate, preserve fan-out, never filter on a
NULL/unknown key; signature = built row count = full base-set). No C2–C7. Oracle-free; leak guard intact.

C1 family targets (all never-pass): `asana001`, `intercom001`, `netflix001`, `hive001`, `provider001`.

## Pre-smoke Decision-Fork Probe

Reachability of each C1 cell is PROVEN offline (residual catalog 2026-06-27). asana001 already landed 2/3
under the broad contract. The OPEN question is purely reliability-under-focus: does a single-template
contract make the C1 siblings land ≥2/3 (vs 0/3 broad)? trials=3 measures it directly.

## Acceptance criteria

**AC-1 — README-only; forks spd0013; adds ONLY the C1 gated contract template.** Leak guard byte-identical.
**AC-2 — clean strict audit per draw.**
**AC-3 — HOLD-RATE (trials=3): a C1 cell is "reliably fixed" at ≥2/3.** Promote only on captain sign-off,
multi-draw. Canaries hold.

## Smoke Plan

trials=3 panel (~13 cells): C1 family (asana001, intercom001, netflix001, hive001, provider001) + canaries
(apple_store001, google_play001, google_play002, mrr001, quickbooks002, activity001, tickit001). No full
board unless ≥2 C1 cells hold ≥2/3.

## Gatekeeper review

## Smoke result

## Verdict
