---
id: spd0019
title: Partial-match join via prefix LIKE + schema.yml-as-spec — preserve fan-out, no dedup
status: hypothesis
kind: hypothesis
source: "never-pass-residual-catalog-2026-06-27 (movie_recomm001 diagnosis); forks champion @baseline spd0013; discovery smoke-only"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Offline diagnosis of `movie_recomm001` (catalog 2026-06-27) found a DETERMINISTIC, oracle-free residual:
the graded `user_watched_movies` (gold 56596 rows, fan-out, NOT deduped) requires a **prefix `LIKE`
partial-title match** between the MovieLens title and the OMDB name, with the natural fan-out preserved.
The champion instead used **exact case-insensitive equality + dedup to min(movie_id)** → 9817 rows (wrong
count, wrong OMDB_movie_id multiset). The task instruction is misleading (it describes a different table,
`original_programs`); the real contract for `user_watched_movies` lives only in the model's `schema.yml`.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow clause:

> When the task instruction is underspecified or appears to describe a different deliverable than a
> graded model, treat that model's own `schema.yml` column descriptions as the authoritative contract.
> When a join is described as a "partial", "fuzzy", or "starts-with" name match, implement it as an
> anchored prefix `LIKE` (`<other> || '%'`) — NOT exact equality — and PRESERVE the natural fan-out: do
> NOT dedup to one row per key unless the spec explicitly says one row per key. Strip only the trailing
> `(YYYY)` token when normalizing a title.

Oracle-free (reads the model's own schema.yml + the join description; no gold values/counts baked);
gated (fires on a partial/fuzzy name-match join). NO other change; leak guard byte-identical to spd0013.

Primary target: `movie_recomm001` (flip + RELIABILITY test — in BOTH smokes for 2 draws).

## Pre-smoke Decision-Fork Probe

**Reachability PROVEN offline (catalog 2026-06-27, local source only):** the gold `user_watched_movies`
row set (56596, fan-out) is exactly reproduced by `stripped_ml_title LIKE omdb_name || '%'` with no dedup;
the champion's equality+dedup gives 9817. The fix is a deterministic, oracle-free join-method choice. The
fork is behavioral: does the prefix-LIKE + schema-as-spec + no-dedup directive steer the worker off its
equality+dedup reflex (and off the misleading instruction). Discriminator: committed `user_watched_movies`
uses a prefix `LIKE` join, preserves fan-out, and its row set matches gold.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.** Leak
guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — RELIABILITY: movie_recomm001 must pass in BOTH small and large smoke (2/2)** to count as a
durable flip; NO hard-canary regression. NO full-run, NO promote (smoke-only discovery).

## Smoke Plan

Two-step, smoke-only, no full — movie_recomm001 in BOTH for a 2-draw reliability check:

- **Small smoke** (~7 cells): `movie_recomm001` + core canaries `apple_store001`, `google_play001`,
  `mrr001`, `quickbooks002`, `activity001`, `app_reporting001`.
- **Large smoke** (~12 cells): `movie_recomm001`, `netflix001`, `flicks001` (other movie/title cells that
  may carry a fuzzy-match join) + full hard-canary panel (activity001, app_reporting001, app_reporting002,
  apple_store001, google_play001, google_play002, mrr001, quickbooks002).

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
