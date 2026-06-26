---
id: spd0014
title: Declared-target closure — build every declared target/support model as a base table with exact convention naming
status: hypothesis
kind: hypothesis
source: "day-queue-2026-06-26 Queue 1; forks champion @baseline spd0013-lean-lag-period-over-period; discovery smoke-only (no full)"
started: 2026-06-26
completed:
verdict:
score:
worktree:
---

## Hypothesis

Several never-pass tasks build *plausible* tables and pass `dbt build`, but the hidden comparison
still fails because one **declared** target or support model is missing, or the convention-correct
name is wrong — the worker stops at "the final report table exists" and never closes the full
declared model set.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add
ONE narrow clause to its existing router / Implementation guidance — a **declared-target-closure**
rule:

> Before finishing, enumerate every model the project DECLARES — every model named in `schema.yml`
> and every model referenced by the compiled manifest / `dbt ls` (including support and intermediate
> models the targets depend on). Build EACH declared model that the task asks to materialize as a
> BASE TABLE under the project's exact existing naming convention (match sibling prefixes/suffixes —
> `dim_`/`fct_`/`obt_`/`<pkg>__<entity>_<suffix>`). Do not stop when the final report table exists and
> `dbt build` is green: a task can declare several target/support models and the grader compares a
> specific one whose convention-correct name or base-table materialization you have not yet produced.
> Do NOT broadly rewrite existing passing models — only ADD/correct the missing declared targets.

Gated (fires when `schema.yml`/manifest declares multiple targets/support models), oracle-free (reads
the project's own declarations, never gold), leak-safe (no values/counts/dtypes baked). NO other
change; no-fetch leak guard byte-identical to spd0013.

Primary targets (all never-pass at champion = 0): `asana001`, `intercom001`, `netflix001`,
`pendo001`, `reddit001`, `social_media001`, `zuora001`, `xero_new001`.

## Pre-smoke Decision-Fork Probe

**Discovery hypothesis — reachability is per the 2026-06-25 resolution survey** (these targets were
mostly REACHABLE_VERIFIED/PROBABLE: declared-but-unbuilt or convention-name misses, not oracle-blind).
A per-task offline gold reconstruction is NOT run for this breadth sweep (8 targets); the smoke tests
**steerability** of the declared-target-closure rule — does naming "close the full declared set, not
just the final report" steer the worker to build the missing/mis-named declared target. The fork per
target: worker builds plausible tables + green `dbt build` (champion control = FAIL) vs worker closes
the full declared target set with convention-correct base tables (proposed). Artifact discriminator:
the graded target table exists as a convention-named base table AND the comparison passes.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
Forks `spd0013-lean-lag-period-over-period`, adds ONLY the declared-target-closure clause. Leak guard
byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — Discovery smoke is useful iff ≥2 primary targets become new ever-pass with NO hard-canary
regression** (day-queue rule). 1 flip = bank, do not full. 0 flips = conclude/reject unless artifact
gives a concrete second blocker. NO full-run, NO promote (smoke-only discovery).

## Smoke Plan

Two-step (small then large), smoke-only, no full:

- **Small smoke** (~8 cells): primary subset `asana001`, `netflix001`, `social_media001`, `zuora001`
  + core canaries `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`.
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
