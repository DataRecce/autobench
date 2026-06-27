---
id: spd0020
title: Preserve-all-rows LEFT join for reference/dimension tables — never INNER-join-away or filter NULL keys
status: hypothesis
kind: hypothesis
source: "never-pass-residual-catalog-2026-06-27 (provider001 diagnosis); forks champion @baseline spd0013; discovery smoke-only; FINAL sprint hypothesis"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Offline diagnosis of `provider001` (catalog 2026-06-27) found a DETERMINISTIC, oracle-free residual on
BOTH graded tables: the champion INNER-joined / filtered rows that gold keeps. `specialty_mapping` gold =
874 (all taxonomy codes, NULL specialty where the Medicare crosswalk is unmatched) but champion kept only
460 matched; `provider` gold = 85196 (all NPIs) but champion filtered to entity_type ∈ {1,2}, dropping the
2857 NULL-entity-type NPIs → 82339. Both tables reproduce gold EXACTLY with a LEFT join that preserves all
reference rows.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow clause to its grain/coverage guidance:

> When a target is a reference/dimension/crosswalk table built from a full entity set (e.g. "all
> taxonomy codes", "all providers/NPIs", a complete code list), preserve EVERY row of that base set:
> LEFT-join the enrichment/crosswalk relations onto it and leave the enriched columns NULL when
> unmatched. Never INNER-join away unmatched rows, and never filter rows out on a NULL or "unknown"
> key/type/category value — a NULL attribute is a VALID row. Only the base-set's own existence defines
> the row count; joins must not shrink it.

Oracle-free (the "full set" intent + the FK-vs-attribute distinction are in the instruction/schema; no
gold values baked); gated (fires on a reference/dimension/crosswalk target built from a full base set).
NO other change; leak guard byte-identical to spd0013.

Primary target: `provider001` (flip + RELIABILITY test — in BOTH smokes for 2 draws; 2 attributable graded
tables).

## Pre-smoke Decision-Fork Probe

**Reachability PROVEN offline (catalog 2026-06-27, local source only):** both graded gold tables
(`specialty_mapping` 874, `provider` 85196) are reproduced EXACTLY by a LEFT-join-preserve-all-rows build;
the champion's INNER-join/NULL-filter gives 460/82339. Deterministic, oracle-free. The fork is behavioral:
does the preserve-all-rows directive steer the worker off its INNER-join/filter reflex. Discriminator: the
committed `specialty_mapping`/`provider` keep the full base-set row count (LEFT join, NULL where unmatched).

This is the COVERAGE family (spd0004 explored a blanket version, validated-not-promoted on variance) — but
this clause is SHARPER (a specific reference/full-set-preservation directive), and the residual here is a
clean, complete, two-table oracle-free fix (unlike tickit002/movie_recomm001 which had finer sub-residuals).

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.** Leak
guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — RELIABILITY: provider001 must pass in BOTH small and large smoke (2/2)** to count as a durable
flip; NO hard-canary regression (the clause must not suppress a LEGITIMATE inner-join filter and break a
passer — the coverage-family regression risk). NO full-run, NO promote (smoke-only discovery).

## Smoke Plan

Two-step, smoke-only, no full — provider001 in BOTH for a 2-draw reliability check:

- **Small smoke** (~7 cells): `provider001` + core canaries `apple_store001`, `google_play001`, `mrr001`,
  `quickbooks002`, `activity001`, `app_reporting001`.
- **Large smoke** (~11 cells): `provider001`, `superstore001` (other multi-table mart) + full hard-canary
  panel (activity001, app_reporting001, app_reporting002, apple_store001, google_play001, google_play002,
  mrr001, quickbooks002) + `mrr002` (perturbable coverage-shape canary).

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
