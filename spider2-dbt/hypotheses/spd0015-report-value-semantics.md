---
id: spd0015
title: Report value-semantics contract — grain-aware COUNT, raw-grain preservation, independent value-recheck (not order/top-N)
status: hypothesis
kind: hypothesis
source: "day-queue-2026-06-26 Queue 2; forks champion @baseline spd0013-lean-lag-period-over-period; discovery smoke-only (no full)"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Several never-pass tasks produce the expected named report tables and pass `dbt build`, but the graded
**values** are off — wrong distinctness (`COUNT(*)` vs `COUNT(DISTINCT)`), a collapsed/regrouped grain,
sign, rolling/period semantics, or row-set scope — and the worker's self-validation only checks row
ORDER / top-N, which hides the value mismatch (self-anchored false-green, the recurring spider2-dbt wall).

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow **report value-semantics contract** clause to its existing G3 COLUMN-VALUE CONTRACT guidance:

> For a report/aggregate target, pin three things from LOCAL evidence before trusting `dbt build`:
> (1) **grain-aware distinctness** — choose `COUNT(*)` vs `COUNT(DISTINCT key)` from BOTH the metric
> name AND the local source grain: if one source row already IS the countable entity use `COUNT(*)`;
> if multiple source rows map to one entity (a fan-out join or a repeated key) use `COUNT(DISTINCT)`;
> (2) **raw-grain preservation** — group at the report grain the task names; do NOT pre-aggregate or
> re-group onto a canonicalized/lookup value that collapses rows the gold keeps separate;
> (3) **independent value-recheck** — before declaring done, recompute at least one report metric a
> SECOND, independent way (e.g. a direct `COUNT`/`SUM` over the source filtered to the report scope)
> and confirm it equals the built table's value. A clean `dbt build` and correct row ORDER / top-N are
> NOT sufficient — order-only checks hide value mismatches.

Derived from the metric name + local source grain (oracle-free, no gold values/counts baked); leak-safe.
NO other change; no-fetch leak guard byte-identical to spd0013.

Primary targets (all never-pass at champion = 0): `flicks001`, `movie_recomm001`, `nba001`,
`playbook002`, `twilio001`, `xero001`, `xero_new002`, `quickbooks001`.

## Pre-smoke Decision-Fork Probe

**Discovery hypothesis — reachability per the 2026-06-25 resolution survey** (these were
REACHABLE_VERIFIED/PROBABLE; "most artifacts already build clean base tables" per the day-queue, so the
gap is value semantics, not existence). No per-task offline reconstruction for this breadth sweep; the
smoke tests **steerability** of the report value-semantics contract. Fork per target: worker emits the
named report table with values off on distinctness/grain/sign/scope, self-validated by order/top-N
(champion control = FAIL) vs worker pins grain-aware distinctness + raw grain + independent value-recheck
(proposed). Artifact discriminator: the graded report value matches gold under column-containment.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
Forks `spd0013`, adds ONLY the report value-semantics clause. Leak guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — Discovery smoke useful iff ≥2 primary targets become new ever-pass with NO hard-canary
regression.** 1 flip = bank, no full. 0 flips = conclude/reject unless artifact gives a concrete second
blocker. NO full-run, NO promote.

## Smoke Plan

Two-step, smoke-only, no full:

- **Small smoke** (~8 cells): primary subset `flicks001`, `nba001`, `twilio001`, `xero001` + core
  canaries `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`.
- **Large smoke** (~16 cells): all 8 primary targets + full hard-canary panel (activity001,
  app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001,
  quickbooks002).

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
