---
title: stockmarket-q4 - Kill run-to-run flakiness with deterministic ordering, explicit tie-breakers, and stable filters
status: expanded
kind: concept
source: flipped-query-targets.md (the flipped 1/5–4/5 Opus queries are unstable, not unsolvable)
id: dab0002
score: 0.6
completed: 2026-06-21T03:47:15Z
verdict: expanded
archived: 2026-06-21T03:47:15Z
---

## Direction

A solver-README rule that makes ranking/selection queries **deterministic**: every `ORDER BY` gets
a full tie-break key, every `LIMIT`/top-N has a defined ordering down to the last row, threshold
filters state `>=` vs `>` explicitly, and date windows pin inclusive/exclusive bounds. The flipped
queries prove the model *can* solve them; the variance comes from under-specified ordering/ties, so
pinning determinism converts a coin-flip into a reliable PASS.

## Evidence

`stockmarket-q4` (Opus 3/5) — top-5 NYSE non-ETF by up>down days: ordering/tie variance.
`crmarenapro-q3` (3/5) — 5-way stage-label choice flips run to run.
`yelp-q6` (1/5) — highest-avg-rating business with a category tie / review-count threshold.

## Candidate hypotheses (ideate fans into 2–5)

- An `analyze`-stage rule mandating a deterministic total order (primary metric, then stable
  secondary keys, then a unique id) for every top-N / argmax query.
- A rule pinning threshold comparators and date-window boundaries to the query's exact wording.
- A tie-break-disclosure rule: when the metric ties at the cutoff, break by the named id column.

## Target queries

Primary: `stockmarket-q4`, `crmarenapro-q3`, `yelp-q6`. Hold canaries: `stockmarket-q3`,
`crmarenapro-q12`.
