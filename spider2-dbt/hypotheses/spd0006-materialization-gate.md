---
id: spd0006
title: Classifier router + Axis-1 materialization gate (BUILD_AS_IS / AUTHOR / enumerate-every-target / verbatim-union)
status: propose
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

**Recommendation: APPROVE** — a purely-additive, precondition-GATED `## Stage: Classify (router)` block with leak-guard byte-intact, specs differ in exactly the two allowed fields, both frozen, and a regression panel that exercises the R4 default path; no FAIL on any rule.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-25.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

Fork parent resolved: `source:` = `solver_workflows/spider2-dbt-baseline`; `@baseline` resolves to `runs/spider2-dbt-full-baseline/13fb630e2cae3eb8` whose `agent.solver_workflow` = `solver_workflows/spider2-dbt-baseline`. They agree — G1 diffed against the seed solver.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | README diff is purely additive (`82a83,128`): one new `## Stage: Classify (router)` block with R1–R6; no other section edited. The single idea = the Axis-1 materialization router named in the claim. |
| G2 leak-guard (hidden gold) | PASS | No-fetch paragraph (README lines 11–13: `curl`/`wget`/`git clone`/`git ls-remote`/web lookup/published solutions) byte-identical in both files. Added-line `gold` hits are all leak-REINFORCING ("Never read or guess gold values"; "if gold was built from this project, your correction diverges from gold") — no gold table/columns named, no `expected_`/`answer_key`/`ground_truth`/fetch token; R3 says report ungradeable, don't fabricate. |
| G3 spec two fields | PASS | `diff full-baseline.yaml … spd0006…yaml` differs only in `experiment:` + `agent.solver_workflow:` (+ ABOUTME). `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, agent `trials: 1` all preserved (`concurrency.trials: 4` = parallelism, same as baseline). |
| G4 smoke narrows tasks only | PASS | Smoke diff changes only `experiment:` + `benchmark.tasks` (narrowed to 7), no `exclude_tasks`. Surviving set = 4 targets (zuora001/superstore001/synthea001/intercom001 — every target the `## Hypothesis` smoke names) + 3 passing canaries; ≥1 currently-PASSING sentinel present. |
| G5 both frozen | PASS | `spd0006-materialization-gate.frozen.yaml` (3201B) + `…smoke.frozen.yaml` (1709B) both exist; both carry `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted R1–R6 match the claim's branches 1:1 (R1 BUILD_AS_IS / R2 AUTHOR-from-recipe / R3 fixture-flag / R4 default / R5 enumerate-every-target / R6 verbatim-union); decisions on oracle-free signals only (stem, schema.yml, dbt_project vars, information_schema). Not self-anchored — R1 explicitly forbids rewriting a passing build; no "verify your answer matches" disease. |
| G7 actionability/inert-risk | PASS | Mechanical, not abstract: named file-signal preconditions (`models/**/<T>.sql` stem, `int_*__<T>_*`), concrete edits (`dbt deps && dbt build`, `UNION ALL`/`FULL OUTER JOIN`, copy sibling's surrogate-key offset). Each branch is a literal file/name/schema test, not a "get the grain right" abstraction. |
| G8 regression-canary coverage | PASS (N/A-gated) | GATED, not generative — every branch fires only on a file/name/schema precondition and R4 (default authoring) leaves plain new-model tasks unchanged ("this router never changes behavior on a plain new-model task"). Panel still keeps non-target `@baseline` passers: activity001 (1.0, exercises the R4 default path), f1001 (1.0), mrr001 (1.0). Targets baseline-FAIL (all 0.0), canaries baseline-PASS (all 1.0) — confirmed in per_trial_outcomes.json. |
| G9 selector independence | N/A (PASS) | Not a multi-candidate/selector protocol — the router picks one branch per table by precondition, no N-candidate generation. |
| G10 self-correcting false-positive | PASS | The only check-flavored prose is R1's "repair ONLY if `dbt build` fails — never to improve a passing build", gated to the existing-stem precondition and explicitly ANTI-rewrite (it suppresses value-rewriting). No branch re-derives against the solver's own answer; R3 flags-don't-fabricate. A gated, structure/existence-anchored, no-rewrite check is the SAFE class. |

**For the captain:** Auto-approved to smoke. This is a precondition-gated router (the gate is the isolation), so the regression risk is contained to tasks whose signals trip a non-R4 branch; the panel correctly includes activity001 as an R4-default-path passer plus two stable sentinels. Baseline statuses verified from per_trial_outcomes.json (4 targets 0.0, 3 canaries 1.0). No WARNs. Watch at smoke (per the sim-validates-tendency scar): does the temp=0 solver actually pick the right branch and suppress the "create a new model"/"fix the math" reflex — judge by committed artifact (empty `models/` diff for zuora001 R1; new `<T>.sql` matching recipe/union for the others).

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
