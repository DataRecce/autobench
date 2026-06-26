---
id: spd0008
title: Axis-2 G2 — OVER_EMIT_COLLAPSE (respect incremental window / role-dimension inner-join / sibling-mirror grain / passthrough no-prune)
status: propose
kind: hypothesis
source: "resolution-survey-2026-06-25 ranked-backlog #3; forks CHAMPION spd0007b (24/61); Axis-2 G2 over-emit-collapse is the one knob" #3; stacks on the spd0007 champion
started: 2026-06-25
completed:
verdict:
score: 0.75
worktree:
---

## Hypothesis

A set of failures over-emit rows: the solver full-refreshes an incremental model into full
history, joins the full user table instead of a role-specific dimension, uses the wrong filter
column, or prunes a passthrough. Each has a **distinct structural gate**, so a collapse rule
composes without bleeding.

**The single README change:** add **Axis-2 rule G2** (collapse-to-canonical-slice), gated:

- target maps to a `config(materialized='incremental')` model with an `is_incremental()`
  period-restriction WHERE clause → emit ONLY the latest window *[airbnb001]*
- target fact carries `seller_*`/`buyer_*` role-prefixed columns AND an
  `int_<role>_extracted_from_users` dimension ships → inner-join THROUGH the role dimension,
  not the raw user table *[tickit002]*
- a `*_by_<entity>` stat has an opposite-entity sibling model → copy the sibling's filter /
  aggregation column verbatim, swap only the entity (e.g. `position` not `position_order`)
  *[f1003]*
- parallel `prod_<entity>` passthrough tables built 1:1 from `raw_<entity>` → preserve source
  grain, do NOT inner-join-prune *[reddit001 — partial; carries a residual 1-row curated drop]*

**Target tasks (REACHABLE_VERIFIED):** airbnb001, apple_store001, synthea001,
shopify_holistic_reporting001, tickit002, reddit001 (partial), f1003. (Note: apple_store001 /
synthea001 / shopify also touched by spd0006 R6; the survey lists them under both — the row-set
exactness is what G2 enforces.)

## Pre-smoke Decision-Fork Probe

Offline-verified (survey wf_32b5a457-a96): e.g. airbnb001 `mom_agg_reviews` emitting only the
single 30-day window (3 rows: neg 834 / neu 2745 / pos 4370) matched gold vs the baseline's
11,135-row full-history over-emit; tickit002 role-dimension inner-join produced the exact gold
row set. The comparator's `len(v)==len(v)` gate makes grain exactness binary — one extra/missing
row fails every gold column. reddit001 has a residual undocumented 1-row post drop, so it may not
flip even at full compliance. Smoke tests collapse compliance.

## Acceptance criteria

**AC-1** — README-only change; spec diff = the two allowed fields.
**AC-2** — scores paired with clean strict audits.
**AC-3** — paired `rk runs diff` vs the spd0007 champion, attributed by the committed SQL; GO
requires ≥1 target flip by artifact + 0 regression (watch: a "union/preserve intermediates"
clause must not regress a task whose final model legitimately filters its intermediates).

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
