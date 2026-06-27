---
id: spd0016
title: Model-inventory per-target grain/PK contract — validate every dimensional target separately, not just the final report
status: hypothesis
kind: hypothesis
source: "day-queue-2026-06-26 Queue 4; forks champion @baseline spd0013-lean-lag-period-over-period; discovery smoke-only (no full)"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Large multi-target dimensional marts build many plausible tables and pass `dbt build`, but one
dimension/fact GRAIN, ID mapping, or support relation is subtly wrong — and the worker only validates
the final report, not each target separately.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow **per-target model-inventory** clause to its router/Implementation guidance:

> For a multi-target mart (≥2 graded/declared target tables), before editing SQL write a one-line
> inventory PER target: target name · declared grain · source grain · primary key · required support
> refs. Then implement and VALIDATE EACH target separately against its own inventory line (its grain key
> is unique, its row set matches the declared grain, its support refs resolve) — do NOT declare done on
> the final report alone. A subtly-wrong dimension/fact grain or ID mapping in a non-final target fails
> the hidden comparison even when `dbt build` is green.

Derived from the project's own declarations/sources (oracle-free, no gold baked); leak-safe. NO other
change; no-fetch leak guard byte-identical to spd0013.

Primary targets (all never-pass at champion = 0; `analytics_engineering001` dropped — not in the gradeable
60-board): `atp_tour001`, `superstore001`, `tickit002`, `tpch001`, `provider001`, `scd001`.

**Survey caveat (recorded for honest yield):** `scd001` (unstable `row_number` tiebreak) and `atp_tour001`
(frozen-clock spine) were flagged NOT-reachable by the 2026-06-25 survey — included for coverage but the
realistic reachable pool is `superstore001`, `tickit002`, `tpch001`, `provider001`.

## Pre-smoke Decision-Fork Probe

**Discovery hypothesis — reachability per the 2026-06-25 survey** (superstore001 downstream-FK gap,
tickit002 sibling-grain, tpch001 genuine-difficulty, provider001 full-dim-LEFT-join were REACHABLE/PROBABLE;
scd001/atp_tour001 NOT-reachable). No per-task offline reconstruction for this breadth sweep; the smoke
tests **steerability** of the per-target inventory+separate-validation contract. Fork per target: worker
validates only the final report and ships a subtly-wrong non-final grain (champion control = FAIL) vs
worker writes a per-target inventory and validates each separately (proposed). Discriminator: each graded
target matches gold under column-containment.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
Forks `spd0013`, adds ONLY the per-target inventory clause. Leak guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — Discovery smoke useful iff ≥2 primary targets become new ever-pass with NO hard-canary
regression.** 1 flip = bank, no full. 0 flips = conclude/reject unless artifact gives a concrete second
blocker. NO full-run, NO promote.

## Smoke Plan

Two-step, smoke-only, no full:

- **Small smoke** (~8 cells): reachable subset `superstore001`, `tickit002`, `tpch001`, `provider001`
  + core canaries `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`.
- **Large smoke** (~14 cells): all 6 primary targets + full hard-canary panel (activity001,
  app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001,
  quickbooks002).

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
