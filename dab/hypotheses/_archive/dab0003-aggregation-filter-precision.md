---
title: Pin aggregation and filter semantics — counts, thresholds, date windows, NULL handling
status: expanded
kind: concept
source: flipped-query-targets.md (several flipped queries hinge on getting one aggregation/filter rule exactly right)
id: dab0003
score: 0.75
completed: 2026-06-21T03:47:15Z
verdict: expanded
archived: 2026-06-21T03:47:16Z
---

## Direction

A solver-README rule that forces the agent to translate the query's quantitative language into
exact SQL semantics before answering: how to count event-days, distinct-vs-row counts, inclusive
date ranges, `>=` vs `>` membership, and NULL/missing-row treatment. These are not capability gaps
— the model can write the SQL — but small semantic slips (off-by-one date boundary, counting rows
instead of distinct entities, mishandling NULLs) flip the answer.

## Evidence

`stockmarket-q4` — "up days" vs "down days" must be counted per the exact close>open / close<open
definition. `yelp-q6` — "at least 5 reviews" (>=) inside a Jan 1–Jun 30 2016 inclusive window.
`bookreview-q1` (canary) — "at least 10 distinct books" (distinct, not review rows).

## Candidate hypotheses (ideate fans into 2–5)

- A `model`/`analyze` rule that restates each numeric constraint as an explicit predicate before
  writing SQL (a "constraint ledger").
- A NULL/missing-metadata handling rule (exclude vs treat-as-zero, stated per query).
- A date-window boundary rule (inclusive endpoints unless stated otherwise).

## Target queries

Primary: `stockmarket-q4`, `yelp-q6`. Hold canaries: `bookreview-q1`, `stockmarket-q3`.
