---
title: Correct multi-source joins and grain — handle missing-metadata rows across sqlite/duckdb/mongo/postgres
status: concept
kind: concept
source: flipped-query-targets.md + GITHUB-q4 reasoning audit (the NULL-language edge case is the crux)
id: concept-multisource-join-grain
---

## Direction

A solver-README rule for joining across DAB's multi-database workspace at the right grain and
handling rows that lack metadata in one source. Wrong-grain joins (fanning out row counts) and
naive treatment of unmatched/NULL rows are a recurring failure mode; a rule that mandates an
explicit join-grain check and a stated policy for missing-metadata rows protects the answer.

## Evidence

`GITHUB_REPOS-q4`: the passing codex-5.5 SQL had to **exclude `torvalds/linux`** because it has no
parsed main-language row (NULL) — answering "non-Python" correctly required deciding that an
unclassified repo is not "non-Python." `googlelocal-q2`: business-description ⋈ review on `gmap_id`
at business grain before averaging ratings.

## Candidate hypotheses (ideate fans into 2–5)

- An `analyze` rule: state the join grain and confirm row-count sanity before aggregating.
- A missing-metadata policy rule (rows absent from the classifying source are excluded from
  "is/has X" set membership unless the query says otherwise).
- A cross-backend key-consistency rule (sqlite metadata keys ↔ duckdb fact keys ↔ mongo ids).

## Target queries

Primary: `GITHUB_REPOS-q4` (also a free anchor flip — codex already 5/5), `googlelocal-q2`.
