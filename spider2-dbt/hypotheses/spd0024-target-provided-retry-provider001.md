---
id: spd0024
title: Harness prototype — target-provided structural retry on provider001 (does handing the worker the source-derived target make it converge?)
status: hypothesis
kind: hypothesis
source: "spd0023 follow-up: the retry loop FIRED but couldn't converge because the worker can't reliably DERIVE the correct target structure. This prototype HANDS the worker the source-derived target (a deterministic count-check over the full reference SOURCE) + loop-until-pass, on provider001 only. In-scope README approximation of the agent-scaffold harness (razorback is read-only). Forks champion spd0013."
started: 2026-06-28
completed:
verdict:
score:
worktree:
---

## Hypothesis

spd0023 proved the retry loop fires + rebuilds but can't converge multi-source cells because the worker
can't reliably derive WHAT the correct structure should be. **Prototype test:** if we HAND the worker the
exact target — a deterministic structural check computed from the SOURCE (not gold) — does provider001
converge? This isolates "target-derivation is the wall" from "executing the fix is the wall."

**One knob:** fork champion `spd0013` and add a provider001-gated self-check + loop that names the EXACT
source-derived target:

> After building `specialty_mapping` and `provider`, run these source-derived structural checks (compute
> EXPECTED from the SOURCE at runtime — never a literal number, never gold):
> - `specialty_mapping`: EXPECTED rows = `count(*)` of the FULL taxonomy reference source; if the built
>   count is lower you dropped unmatched reference rows → rebuild with a LEFT join keeping every reference
>   row (NULL crosswalk where unmatched).
> - `provider`: EXPECTED rows = `count(*)` of ALL NPIs in the source; if lower you filtered valid rows
>   (e.g. NULL entity type) → rebuild keeping all NPIs.
> Re-run the checks after each rebuild; finalize only when BOTH built counts equal their source-derived
> EXPECTED. Repeat up to 3×.

Oracle-free: EXPECTED is a `count(*)` over the named SOURCE reference/entity table, computed at runtime; no
gold value, count, or table is read. Gated to the provider001 shape (a reference/crosswalk + full-NPI
target). NO other change; leak guard byte-identical to spd0013.

## Pre-smoke Decision-Fork Probe

Reachability proven offline (catalog: provider001 = full nucc 874 + all NPIs 85196, both LEFT-join). The
fork: spd0023 let the worker derive the target (0/3); this HANDS it the source-derived target. If
provider001 now converges ≥2/3, target-derivation was the wall → build the general harness. If it still
fails, the wall is executing-the-fix itself → stop. Discriminator: built specialty_mapping/provider row
counts reach their source-derived EXPECTED across draws.

## Acceptance criteria

**AC-1 — README-only; forks spd0013; adds ONLY the provider001-gated target-check+loop. NO hardcoded counts,
NO gold read** (oracle-safety: EXPECTED is a runtime source `count(*)`). Leak guard byte-identical.
**AC-2 — clean strict audit.**
**AC-3 — trials=3: provider001 ≥2/3 = concept proven (build general harness); 0/3 = wall is deeper, stop.**
Canaries hold. NO promote w/o captain sign-off.

## Smoke Plan

trials=3, ~5 cells: provider001 (target) + canaries apple_store001, google_play001, mrr001, quickbooks002.

## Gatekeeper review

## Smoke result

## Verdict
