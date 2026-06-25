---
id: spd0006
title: Classifier router + Axis-1 materialization gate (BUILD_AS_IS / AUTHOR / enumerate-every-target / verbatim-union)
status: hypothesis
kind: hypothesis
source: resolution-survey-2026-06-25 (docs/resolution-survey-2026-06-25.md) ranked-backlog #1; reframes spd0002 (build-every-deliverable, REJECTED) into a precondition-GATED router
started: 2026-06-25
completed:
verdict:
score: 0.9
worktree:
---

## Hypothesis

The solver fails a cluster of tasks not on grain/value but on **what to build**: it
invents a differently-named model, edits/rewrites an existing model that already encodes
gold, builds only the prose-named target while the eval contract names several, or
re-derives a final model from raw when the project ships the intermediates. A
**classifier router prepended to the solver README**, deciding materialization per
`condition_tabs` table on **oracle-free signals only** (existing `.sql` stem, `schema.yml`
docs, `dbt_project.yml` source-ids vs `information_schema`, presence of `int_*__<T>_*`
intermediates), fixes this without touching grain/value.

**The single README change:** add a `## Stage: Classify (router)` section with **Axis-1**
rules, BEFORE Implementation:

- **R1 BUILD_AS_IS** — if `models/**/<T>.sql` already exists (stem == a target table),
  `dbt deps && dbt build` only; do NOT create or edit that model's SQL (repair only if
  `dbt build` fails, never to "improve" a passing build). *[zuora001]*
- **R2 AUTHOR-from-recipe** — if `schema.yml` documents a model named `<T>` (refs + column
  descriptions) but no `<T>.sql`, author it from that declared recipe, mirroring the nearest
  same-role sibling's conventions (surrogate-key offset + `ROW_NUMBER()`, `{{ ref('dim_*') }}`
  FK joins, dtypes); do NOT invent a differently-named table. *[superstore001, social_media001,
  movie_recomm001]*
- **R3 FIXTURE-flag** — if a target's declared source identifier (`dbt_project.yml` vars /
  an `int_` ref) resolves to a table ABSENT from the source `information_schema`, report
  ungradeable; do NOT fabricate source rows. *[sap001 — harness defect, not a solver miss]*
- **R5 enumerate-every-target** — always build EVERY table in `condition_tabs`, not just the
  prose-named one. *[intercom001 built 1 of 2]*
- **R6 verbatim-union** — if `int_*__<T>_*` intermediates exist and `<T>` is the lone missing
  final model in an otherwise-complete dir, author `<T>` as a verbatim `UNION ALL` / `FULL
  OUTER JOIN` of those intermediates; do NOT re-derive from raw. *[synthea001,
  shopify_holistic_reporting001, apple_store001]*

This GATES the spd0002 "build every deliverable" idea (REJECTED as a blanket generative
reflex) behind per-target preconditions — the gate is the isolation.

**Target tasks (offline-verified reachable):** zuora001, superstore001, social_media001,
synthea001, intercom001, apple_store001 (REACHABLE_VERIFIED); movie_recomm001, quickbooks001
(REACHABLE_PROBABLE). chinook001/sap001 are fixture defects routed to spd0010.

## Pre-smoke Decision-Fork Probe

**Left-shifted and stronger than a proxy:** each target was reconstructed from SOURCE and run
through the verifier's own `tests/duckdb_match.py` against gold OFFLINE (survey run
wf_32b5a457-a96; per-task records in `docs/resolution-survey-2026-06-25-pertask.json`).

- **zuora001** — BUILD_AS_IS: comparator returns True when the existing models are built
  unmodified; the baseline's edits to 5 models caused the miss. REACHABLE_VERIFIED.
- **superstore001 / social_media001** — AUTHOR-from-`schema.yml`: target reconstructed from
  declared refs matched gold columns. REACHABLE_VERIFIED.
- **synthea001 / apple_store001 / shopify_holistic_reporting001** — verbatim `UNION` of the
  shipped `int_` intermediates reproduced the gold row set. REACHABLE_VERIFIED.
- **intercom001** — both `condition_tabs` tables individually reproduce gold; baseline built
  only one. REACHABLE_VERIFIED.

**Expected artifact signature in a real run:** for zuora001, a `git diff` of `models/` is
empty (build-as-is, no model SQL edited); for the AUTHOR/UNION targets, a new `<T>.sql`
whose committed SQL matches the declared recipe / unions the named intermediates. The
residual risk smoke tests is purely **compliance** — does the production solver pick the
right router branch and stop the "create a new model"/"fix the math" reflex — NOT whether
gold is reachable (already proven).

Caveat: offline reachability proves the gold is attainable, not that the temp=0 solver
complies (sim-validates-tendency scar — verify the committed artifact at smoke).

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/full-baseline.frozen.yaml specs/spd0006-materialization-gate.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict`).

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`**, attributed via
the committed-artifact read (build-as-is ⇒ empty `models/` diff; author/union ⇒ the new model
SQL matches the recipe). Smoke GO requires ≥1 target flip proven by artifact + 0 canary
regression.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
