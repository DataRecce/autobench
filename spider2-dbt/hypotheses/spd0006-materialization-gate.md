---
id: spd0006
title: Classifier router + Axis-1 materialization gate (BUILD_AS_IS / AUTHOR / enumerate-every-target / verbatim-union)
status: smoke
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

Run `runs/spider2-dbt-spd0006-smoke/8f185cee4407c0f4` (rc=0, audit strict CLEAN — 0 tainted,
0 errored). Score 3/7 = **0/4 targets flipped, 3/3 canaries held**.

| cell | role | baseline | smoke | flip? |
|---|---|---|---|---|
| zuora001 | 🎯 R1 build-as-is | FAIL | FAIL | no |
| superstore001 | 🎯 R2 author | FAIL | FAIL | no |
| synthea001 | 🎯 R6 union | FAIL | FAIL | no |
| intercom001 | 🎯 R5 enumerate | FAIL | FAIL | no |
| activity001 | ✅ R4-default authoring canary | PASS | PASS | held |
| f1001 | ✅ sentinel | PASS | PASS | held |
| mrr001 | ✅ sentinel | PASS | PASS | held |

NO-GO on the auto-advance guardrail (target flipped by committed artifact = 0). **But not
inert and not a regression** — the router fired and moved every target's artifact toward gold.

## Run result

n/a — no full run (NO-GO at smoke).

## Behavioral analysis

The router **classification mechanism is validated**: all 4 targets were routed to the
correct branch by oracle-free signals (zuora→R1, superstore→R2, synthea→R6, intercom→R5).
None flipped because each hit a DISTINCT secondary wall:

- **zuora001 — ROUTER_FIRED_NONCOMPLIANT (spd0006-attributable).** R1 fired and the solver did
  NOT create new models (the baseline failure mode) — an improvement. But the stock project
  does NOT `dbt build` clean: it refs an absent source `stg_zuora__payment_method`. R1's
  "repair only if build fails" escape-hatch is UNBOUNDED, so the solver rewrote
  `int_zuora__account_enriched`'s grain/join to force a green build, collapsing
  `zuora__account_overview` to 1 row (gold = 4, NULL name/number on the lone row — exactly the
  compared cols). Two findings: (1) R1's repair clause must be bounded to the feature boundary
  (disable the absent-source staging subtree; NEVER alter a target/intermediate's grain or
  join); (2) an absent `source()` is the **R3 fixture-defect** signal — R3 must take precedence
  over R1's repair. (3) the survey's REACHABLE_VERIFIED for zuora was over-optimistic: the flip
  needs a *bounded disable-absent-source* edit, not zero edits.
- **synthea001 — ROUTER_COMPLIED_STILL_FAILED (infra, NOT steerability).** R6 fired and was
  obeyed: the solver authored `cost` as a verbatim union of the shipped `int__cost_*`
  intermediates and did NOT fabricate condition rows (baseline = 836 with 32 spurious rows;
  this run = 807, 0 fabricated — the R6 mechanism WORKS). The 2-row miss (807 vs gold 809) is
  an ENVIRONMENT defect: `dbt_utils` is absent from the image, the solver hand-shimmed it with
  `adapter.get_columns_in_relation` (violating the README's standing "never shim dbt_utils"
  guard), and the shim dropped 1 row from each of 2 staging domains. Fix is package-layer
  (ensure `dbt deps` installs `dbt_utils`) — same class as the wrong-DuckDB packaging memory.
- **superstore001 — ROUTER_FIRED_NONCOMPLIANT (spd0007-attributable, NOT spd0006).** R2 fired,
  authored the star schema, and FIXED the surrogate-key offsets (1001/101 correct). Residual
  miss: it emitted `fct_sales.order_id` as the raw STRING while gold's `order_id` is
  integer-typed (+ an extra leading surrogate column). That is a per-column VALUE/TYPE contract
  issue = **spd0007 (value-def)** territory, not materialization. This target was mis-scoped
  into spd0006's smoke.
- **intercom001 — ROUTER_FIRED_NONCOMPLIANT + deeper (spd0009-attributable).** R5 read as a
  soft reminder; the solver built only `intercom__admin_metrics` (1 of 2 contract tables) and
  explicitly dismissed the declared-but-unbuilt `intercom__company_metrics` as "unrelated"
  because the prose named only admin metrics. AND the built table needs full-dimension grain
  (4 rows; it emitted 1 via the README's dominant inner-join rule) = **spd0009 (spine)**
  conflict. Doubly-blocked; mis-scoped into spd0006's smoke.

**WORKFLOW-REFINEMENT (automatic — spd0006 adds a new `## Stage: Classify (router)` to the
solver workflow):** the new stage FIRED across the whole smoke set and produced correct
classifications; it is a real, exercised structural change with a positive effect on artifacts
(zuora stopped creating new models; synthea stopped fabricating rows). Logged in
`_artifacts/WORKFLOW-REFINE.md`.

## Failure Review

**Primary type: `incomplete-artifact` (router classifies correctly but secondary walls block the
flip), compounded by one `infrastructure-failure` (synthea dbt_utils) and two mis-scoped targets.**

1. **Original fork:** materialization routing (what-to-build) is the decisive lever for this
   cluster; reachability proven offline.
2. **What the artifacts revealed:** routing fires correctly, but (a) R1's repair escape-hatch is
   unbounded and corrupts targets when the stock build fails on an absent source; (b) the AUTHOR
   path doesn't pin the per-column type/projection contract; (c) the image lacks `dbt_utils`; (d)
   R5 is too soft to beat prose-scoping; and (e) 2 of the 4 targets' residual gaps belong to
   spd0007/spd0009, not spd0006.
3. **Did the rule fire + evidence:** YES — committed artifacts show correct branch selection on
   all 4 (zuora no-new-models; synthea verbatim-union no-fabrication 836→807; superstore correct
   offsets; intercom acknowledged the missing table). Canaries held (R4 default unchanged).
4. **Next fork to test (revise):** bound R1's repair to the feature boundary + give R3 precedence
   over R1 repair; harden R5 from a reminder into a hard "the declared schema.yml table set IS the
   target list — a declared-but-unbuilt model is in scope even if the prose omits it" rule;
   RE-SCOPE the smoke to spd0006-attributable targets only (zuora001 + synthea001 + one clean
   R2/R6 target), moving superstore001→spd0007 and intercom001→spd0009. Separately ESCALATE the
   `dbt_utils` packaging defect (infra code fix — not an FO main-branch edit).
5. **Next step: `file`/revise** — route `smoke → hypothesis` with the bounded-repair + hardened-R5
   + re-scoped-smoke revision; escalate the dbt_utils infra fix to the captain.

## Follow-up Routing

`escalate` — the revision is concrete (bound R1 repair + R3 precedence, harden R5, re-scope
smoke) but it is entangled with (a) an infra packaging fix (`dbt_utils`) that is NOT an FO
main-branch edit and needs captain sign-off, and (b) a scope decision (move superstore001→spd0007,
intercom001→spd0009). Surface to the captain at the smoke gate with a single REVISE recommendation.

## Revision v2 (captain-approved REVISE + re-smoke, 2026-06-25)

Captain approved REVISE. Changes (still ONE knob — the materialization router; diff vs baseline
remains purely additive, leak-guard byte-intact):
1. **R1 BOUNDED REPAIR** — repair on build-failure may only disable/stub the failing UPSTREAM
   (absent-source staging); NEVER alter a target/intermediate's grain/join/row set. If the build
   can only pass by changing a target's own SELECT, STOP and route to R3. (Fixes the zuora 4→1
   collapse.)
2. **R3 PRECEDENCE** — run the R3 absent-source/-package check BEFORE any R1 repair; an absent
   source/package model routes to R3 (disable), not target re-derivation.
3. **R5 HARDENED** — from a soft reminder to a hard rule: the declared `schema.yml` model set (and
   dbt "missing model" warnings) IS the target list; a declared-but-unbuilt model is in scope even
   if the prose omits it; never dismiss it as "unrelated." (Fixes intercom building 1 of 2.)

Infra fix landed first (captain-approved): `dbt_utils` vendored via a packager donor
(`tools/vendor/dbt_utils`, `_vendor_dbt_utils()`) — synthea001 view fixed for the re-smoke; gold
was built with `dbt_utils`, the offline container could not `dbt deps` it, so the solver shimmed
and dropped rows.

**Re-scoped smoke** (spd0006-attributable + infra-clean only): targets synthea001 (R6 union,
dbt_utils now present), social_media001 (R2 author, packages complete), apple_store001 (R6 union,
packages complete); canaries activity001 (R4 default) / f1001 / mrr001. Dropped: zuora001
(zuora_source package unobtainable offline → spd0010), superstore001 (order_id dtype → spd0007),
intercom001 (full-dimension grain → spd0009).

Self reject-checks (re-run): README diff vs baseline purely additive (`82a83,144`); leak-guard
intact; full-spec diff = `experiment:` + `solver_workflow:` only; smoke `--explain` = exactly the
6 cells. Frozen: `specs/spd0006-materialization-gate.smoke.frozen.yaml`.

## Smoke result (v2)

Run `runs/spider2-dbt-spd0006-smoke/1d1af6c748b8fce8` (rc=0, audit strict CLEAN — 6 clean, 0
tainted, 0 errored). 0/3 targets flipped; canaries activity001 + mrr001 HELD; **f1001 dropped to
0.0**. Per-target committed-artifact deep-dive:

- **f1001 (canary drop) = VARIANCE, NOT router over-fire (the key finding).** v1(PASS) and
  v2(FAIL) built IDENTICAL model sets (both `dbt build` PASS=40), same R2 classification on all 4
  targets, byte-identical SQL on 3/4, logically identical on the 4th, and IDENTICAL reported
  values (Hamilton 348 races/201 podiums/104 poles/66 fastest). The hardened R5 added ZERO extra
  tables. The FAIL is a gpt-5.5 value-level coin-flip on non-echoed `position_desc`-derived status
  columns (condition_cols 27–32) — a known f1001 variable cell (cf. spd0004 history). **The
  classifier-router does NOT over-fire / is NOT generative — the central risk for the whole
  classifier-stage strategy is disproven.**
- **social_media001 = router materialization SUCCESS, flip gated on spd0007.** Router fired
  R2/R5, built ALL 5 contract tables as base tables at GOLD-EXACT rowcounts (ig 3, tw 100, rollup
  180). The sole 0-reward cause is the linkedin `post_message` value-def (`coalesce(post_title,
  commentary)`) — invisible on the per-platform tables, fails only the rollup col-3 containment.
  This is a per-column VALUE-DEF = **spd0007**, not materialization. Clean evidence the router does
  its job and the flip is gated on the NEXT lever.
- **synthea001 = dbt_utils fix WORKED + new gaps.** The vendored dbt_utils loaded (no re-shim; the
  `local:` packages.yml form + env copy resolved) and R6 authored `cost` as a verbatim union. But
  (a) the solver still EDITED the upstream `int__cost_*` intermediates (added datetime-equality
  joins + QUALIFY dedup), over-filtering 13 rows (796 vs gold 809) — the bounded-repair/"don't
  touch upstream grain" rule is not strong enough to stop editing intermediates feeding an R6
  union; (b) a SECOND fixture gap — the project-local `lowercase_columns` macro (referenced by 74
  staging models) is not shipped, so the solver had to author it. synthea is fixture-gap-laden.
- **apple_store001 = R6 MISFIRES (the one real router defect).** The solver applied R6 "verbatim
  UNION ALL of the intermediates" and got 29/36 rows = the EXACT over-emit baseline (gold 9/17).
  For these report-grain tables a naive union of the sub-grain intermediates IS the over-emission;
  the verified fix is the OPPOSITE (anchor on the app_store impressions intermediate + LEFT-join,
  = a grain rule). **R6 is mis-scoped; apple_store belongs to spd0008.**

**WORKFLOW-REFINEMENT (v2):** router classification validated + proven non-destabilizing (R5 adds
0 tables; f1001 is variance). R6 "verbatim union" is defective — correct for synthea's `cost`,
wrong for apple_store's reports. Materialization routing is NECESSARY-NOT-SUFFICIENT: standalone
flips are gated on value-def (spd0007) / grain (spd0008). Logged in `_artifacts/WORKFLOW-REFINE.md`.

## Verdict

Pending the v2 smoke gate. (v1 was NO-GO: router classification validated, secondary walls
diagnosed and addressed in v2 + re-scope.)
