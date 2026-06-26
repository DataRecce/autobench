---
id: spd0008
title: Axis-2 G2 — OVER_EMIT_COLLAPSE (respect incremental window / role-dimension inner-join / sibling-mirror grain / passthrough no-prune)
status: smoke
kind: hypothesis
source: "resolution-survey-2026-06-25 ranked-backlog #3; forks CHAMPION spd0007b (24/61); Axis-2 G2 over-emit-collapse is the one knob" #3; stacks on the spd0007 champion
started: 2026-06-25
completed:
verdict:
score: 0.75
worktree:
---

## Hypothesis

A set of failures over-emit rows: the solver full-refreshes an incremental model into full
history, joins the full user table instead of a role-specific dimension, uses the wrong filter
column, or prunes a passthrough. Each has a **distinct structural gate**, so a collapse rule
composes without bleeding.

**The single README change:** add **Axis-2 rule G2** (collapse-to-canonical-slice), gated:

- target maps to a `config(materialized='incremental')` model with an `is_incremental()`
  period-restriction WHERE clause → emit ONLY the latest window *[airbnb001]*
- target fact carries `seller_*`/`buyer_*` role-prefixed columns AND an
  `int_<role>_extracted_from_users` dimension ships → inner-join THROUGH the role dimension,
  not the raw user table *[tickit002]*
- a `*_by_<entity>` stat has an opposite-entity sibling model → copy the sibling's filter /
  aggregation column verbatim, swap only the entity (e.g. `position` not `position_order`)
  *[f1003]*
- parallel `prod_<entity>` passthrough tables built 1:1 from `raw_<entity>` → preserve source
  grain, do NOT inner-join-prune *[reddit001 — partial; carries a residual 1-row curated drop]*

**Target tasks (REACHABLE_VERIFIED):** airbnb001, apple_store001, synthea001,
shopify_holistic_reporting001, tickit002, reddit001 (partial), f1003. (Note: apple_store001 /
synthea001 / shopify also touched by spd0006 R6; the survey lists them under both — the row-set
exactness is what G2 enforces.)

## Pre-smoke Decision-Fork Probe

Offline-verified (survey wf_32b5a457-a96): e.g. airbnb001 `mom_agg_reviews` emitting only the
single 30-day window (3 rows: neg 834 / neu 2745 / pos 4370) matched gold vs the baseline's
11,135-row full-history over-emit; tickit002 role-dimension inner-join produced the exact gold
row set. The comparator's `len(v)==len(v)` gate makes grain exactness binary — one extra/missing
row fails every gold column. reddit001 has a residual undocumented 1-row post drop, so it may not
flip even at full compliance. Smoke tests collapse compliance.

## Acceptance criteria

**AC-1** — README-only change; spec diff = the two allowed fields.
**AC-2** — scores paired with clean strict audits.
**AC-3** — paired `rk runs diff` vs the spd0007 champion, attributed by the committed SQL; GO
requires ≥1 target flip by artifact + 0 regression (watch: a "union/preserve intermediates"
clause must not regress a task whose final model legitimately filters its intermediates).

## Gatekeeper review

**Recommendation: APPROVE** — clean single-knob additive G2 block over the resolved champion spd0007b; every rule gated on an oracle-free structural signal, leak-guard byte-intact, specs scoped correctly; the only soft spots are WARN-class (partial smoke target coverage vs the broad survey list; one abstract-prose rule).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-26T00:00:00Z.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

Fork parent resolved: `@baseline` = `runs/spider2-dbt-spd0007b-full/b0ebdde3817a52ab` (24/61), `agent.solver_workflow = ./solver_workflows/spd0007b-value-def-no-idcast` — matches `source:`. Champion canary status pulled from its `per_trial_outcomes.json`: airbnb001/tickit002/apple_store001 = 0.0 (FAIL, valid targets); f1003/retail001/activity001/mrr001 = 1.0 (PASS, valid canaries).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | Diff vs champion adds exactly ONE section header `### Axis-2 G2 — OVER-EMIT COLLAPSE` (lines 151–184); zero deletions/edits to existing lines; no other idea added. |
| G2 leak-guard (hidden gold) | PASS | No-fetch sentence byte-identical to champion (both line 11: "Do not fetch public reference material…`curl`/`wget`/`git clone`/`git ls-remote`"). Added block uses `gold` only as the contrast noun ("more rows than gold", `len(pred)==len(gold)`) — no gold table/column names, no `expected_`/`answer_key`/`ground_truth`, no read-gold-file or fetch instruction. Probe numbers (834/2745/4370/11135) live only in the .md body, NOT the README (grep: NONE). |
| G3 spec two fields | PASS | `diff full-baseline.yaml spd0008-…yaml` = ABOUTME comments + `experiment:` + `agent.solver_workflow:` only. `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1` all preserved. |
| G4 smoke narrows tasks only | WARN | Smoke diff changes ABOUTME + `experiment:` + `benchmark.tasks:` (narrowed to 7: airbnb001/tickit002/apple_store001 + f1003/retail001/activity001/mrr001); no other field, no `exclude_tasks`. WARN: the `## Hypothesis` "Target tasks" line names 7 (incl. synthea001/shopify_holistic_reporting001/reddit001) but only 3 flip-targets are smoked. Defensible — the 3 included carry the cleanest distinct gates (incremental / role-dim / report-grain-anchor), f1003 is a passer so correctly a canary not a target, reddit001 is self-flagged "may not flip", and synthea/shopify overlap spd0006 R6 — but full smoke target coverage is partial. |
| G5 both frozen | PASS | `spd0008-…frozen.yaml` (3199B) + `…smoke.frozen.yaml` (1706B) both exist; both carry `kind: spacedock_solver` + `runtime: codex` (lines 4–5). |
| G6 resolver fidelity | PASS | Inserted text matches the claim's four+one gated rules verbatim in intent (incremental-window / role-dimension inner-join / sibling-mirror filter / passthrough-no-prune + the report-grain anchor for apple_store001). No self-anchored "verify your answer matches" prose; each rule is generative-on-build gated to a structural signal. No unpromised scope. |
| G7 actionability/inert-risk | WARN | 4 of 5 rules are concrete + mechanical (named config `materialized='incremental'`/`is_incremental()`, role-dim INNER JOIN, copy-sibling-filter-verbatim, ANCHOR+LEFT-join+`coalesce`). The passthrough rule ("preserve source grain, never inner-join-prune") is the most abstract — carries a `prod_<entity>`/`raw_<entity>` gate but no worked skeleton; mild inert-risk at xhigh. WARN-only, never moves the recommendation. |
| G8 regression-canary coverage | PASS | GATED, not generative — every rule fires only on its structural precondition (model config / role-prefix+role-dim / `*_by_<entity>` sibling / `prod_*`+`raw_*` / `*_report`·`*_rollup` name); the closing line states none fires on a plain authored aggregate. Smoke nonetheless keeps non-target passers: retail001 (value-def passer), activity001, mrr001 (the R1/value-def regression sentinel from spd0007b lore), plus f1003 (the perturbable sibling-mirror passer). |
| G9 selector independence | N/A | No multi-candidate / selector protocol declared. |
| G10 self-correcting false-positive | N/A | No validate-and-fix / reconcile-and-replace instruction; G2 is a build-shape directive, not a self-check. (The standing R1-precedence guard already forbids value edits to pre-existing/R1 models, which contains the "report-grain anchor / passthrough" perturbation risk AC-3 flags.) |

**For the captain:** AUTO-APPROVED to smoke. Two WARNs to note: (1) **G4** — the smoke flips only 3 of the 7 survey-listed targets (airbnb001/tickit002/apple_store001); synthea001/shopify_holistic_reporting001/reddit001 are NOT smoked, so a smoke GO confirms the 3 cleanest gates only — full-run attribution is where the other targets get tested. (2) **G7** — the passthrough-no-prune rule is the one abstract clause (gated but no skeleton), mildly inert-risk at xhigh. On the G8 perturbation worry AC-3 raises (report-grain/passthrough could perturb a passer whose final model legitimately filters its intermediates): f1003 + retail001 cover the sibling-mirror and value-def families, and the R1-precedence guard blocks edits to pre-existing models — but no smoked passer is itself a `*_report`/`*_rollup` whose final model legitimately filters intermediates, so the report-grain-anchor rule's over-fire potential is NOT directly canaried (only the full run's broader passer set covers it).

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
