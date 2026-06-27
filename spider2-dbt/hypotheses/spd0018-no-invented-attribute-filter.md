---
id: spd0018
title: No invented attribute filter — restrict dim/fact row sets by inventoried join keys only, never by payload columns
status: hypothesis
kind: hypothesis
source: "day-queue-2026-06-26 follow-up; per-task offline diagnosis of the spd0016 tickit002 variance near-miss; forks champion @baseline spd0013; discovery smoke-only"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Per-task offline diagnosis of `tickit002` (the spd0016 1/2 variance near-miss) found the pass↔fail
driver is a **deterministic SQL-shape choice with an oracle-free correct answer**, NOT irreducible
variance. The FAIL run added an INVENTED `WHERE venue_seats IS NOT NULL` filter on a non-key, non-graded,
instruction-unmentioned attribute, dropping 300 valid rows from `dim_events` (8659→8359) and failing the
row-count containment. The PASS run had no such filter and reproduced gold exactly (both `dim_events`
8659 and `fct_listings` 177417, symdiff 0, verified offline). A second divergence (joining the full user
table instead of `int_sellers_extracted_from_users`) is ALREADY covered by the champion's role-dimension
clause — the gap is the invented attribute filter.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow prohibition clause to its grain guidance:

> **Do not invent a row filter on a non-key attribute.** When building a dimension/fact by joining
> staging models, restrict the row set ONLY by the inventoried join keys (the FK inner-joins that define
> the declared grain). Never add a `WHERE <attribute> IS NOT NULL` — or any value predicate — on a
> descriptive/payload column the instruction does not name. A NULL or zero in a descriptive attribute is
> a VALID row; dropping it under-emits and fails the row-count gate. Filter rows on join keys, never on
> payload columns.

Oracle-free (the key-vs-attribute distinction is visible in the model SQL / schema, no gold values);
gated (fires when building a dim/fact by joining staging). NO other change; leak guard byte-identical.

Primary target: `tickit002` (flip + RELIABILITY test — must pass BOTH small and large smoke = 2/2 draws,
vs the 1/2 under spd0016). Bonus discovery: `provider001`, `superstore001` (other never-pass dim/fact
marts that may carry the same invented-filter or under-emit shape).

## Pre-smoke Decision-Fork Probe

**Reachability PROVEN offline (per-task reconstruction, local source only):** the PASS-run committed SQL
reproduces both graded gold tables EXACTLY (dim_events 8659 / fct_listings 177417, symdiff 0). The sole
flip driver is the invented `IS NOT NULL` attribute filter (under-emit) — a deterministic shape choice
with an oracle-free correct answer (keys define the row set; payload columns do not). The fork is purely
behavioral: does the prohibition clause suppress the stochastic "add a defensive `IS NOT NULL`" choice so
tickit002 passes RELIABLY (2/2) instead of 1/2. Discriminator: committed `dim_events` has no invented
attribute filter and the row set matches gold.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
Forks `spd0013`, adds ONLY the no-invented-attribute-filter clause. Leak guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — RELIABILITY: tickit002 must pass in BOTH the small and large smoke (2/2)** to count as a durable
flip (vs the spd0016 1/2 coin-flip). NO hard-canary regression (the clause is a prohibition — must not
suppress a LEGITIMATE key filter and break a passer). NO full-run, NO promote (smoke-only discovery).

## Smoke Plan

Two-step, smoke-only, no full — tickit002 in BOTH for a 2-draw reliability check:

- **Small smoke** (~8 cells): `tickit002`, `provider001`, `superstore001` + core canaries
  `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`, `activity001`.
- **Large smoke** (~14 cells): `tickit002`, `provider001`, `superstore001`, `tpch001` + full hard-canary
  panel (activity001, app_reporting001, app_reporting002, apple_store001, google_play001, google_play002,
  mrr001, quickbooks002) + `tickit001` (sibling passer — must not break).

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
