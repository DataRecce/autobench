---
id: spd0002
title: Build EVERY result table the instruction enumerates (completeness lever)
status: smoke
kind: hypothesis
source: re-scoped from spd0001 anchor deep-dive (the original materialization framing is dead — 0 ephemeral fails board-wide; re-aimed at the 3 tractable incomplete-deliverable fails)
started: 2026-06-24T14:34:28Z
completed:
verdict:
score: 0.9
worktree:
---

## Hypothesis

> **Re-scope note.** This hypothesis was originally a *materialization* lever (force every named
> target to a BASE TABLE; targeting chinook001). The spd0001 anchor full-board read **killed that
> framing**: the output-contract seed README already lands BASE-TABLE materialization on 100% of fails
> (0 ephemeral board-wide), and chinook001 turned out to be a gold-side packaging defect, not an
> ephemeral miss. So the materialization lever has **no live target**. Re-aimed here at the one
> tractable, artifact-checkable failure family the anchor surfaced.

The anchor showed the solver sometimes **builds only some of the result tables the instruction
enumerates** — it stops after the first deliverable when the task asks for several. Confirmed on the
committed artifacts:
- **intercom001** — gold requires `intercom__company_metrics` + `intercom__admin_metrics`; the agent
  built only `intercom__admin_metrics`.
- **analytics_engineering001** — gold requires `fact_purchase_order` + `obt_customer_reporting`; the
  agent built only `obt_customer_reporting`.

Both are convention-correct on what they *did* build — they are pure **completeness** misses, not
value misses. (The gold table *names* are not visible to the agent, so the lever must work from the
instruction's own enumeration of deliverables, not from the gold list.)

**Claim:** a single solver-README rule — *"Before finishing, re-read the instruction and enumerate
EVERY distinct result table / deliverable it describes (a dimension AND a fact AND a one-big-table are
separate deliverables). Build a separate materialized base table for EACH enumerated deliverable.
Confirm the count of built target tables equals the count of deliverables the instruction names —
do not stop after the first."* — flips intercom001 and analytics_engineering001 FAIL→PASS by making
the solver build the second required table.

This is a **completeness check**, not a value-rewrite (G10-safe: it only *adds* missing deliverables;
it cannot turn a correct table's values wrong). It is mildly **generative** (the "enumerate
deliverables" reflex fires on every task), so the smoke set carries a regression panel of
currently-passing tasks — a single-deliverable passer must NOT sprout spurious extra tables, and a
multi-task family passer guards the most-at-risk shape.

Target tasks: `spider2-dbt-intercom001`, `spider2-dbt-analytics_engineering001`. Stretch/optional
3rd: `spider2-dbt-movie_recomm001` (a wrong-name/scope miss — may or may not be the same family;
include only if the propose-gate read supports it).

## Pre-smoke Decision-Fork Probe

Not run (no local fork harness). The fork is well-identified by the anchor committed artifacts: in
both target cells the model SQL for the built table is correct and materialized as a base table; the
sole gap is a *missing second model*. The README wording above directly addresses that mechanism
(enumerate-and-count deliverables). Proxy evidence deferred to the smoke; the fork is concrete enough
to smoke directly.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `agent.solver_workflow:`.**
Verified by: `diff specs/full-baseline.yaml specs/spd0002-build-every-deliverable.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites `rk audit --policy strict` on the same run-dir.

**AC-3 — intercom001 and/or analytics_engineering001 flip FAIL→PASS because the previously-missing
second gold table (`intercom__company_metrics` / `fact_purchase_order`) now exists as a base table in
the built DuckDB (committed-artifact confirmation), and the passing sentinels hold (no spurious extra
tables, no regression).**

## Gatekeeper review

**Recommendation: APPROVE** — single ADD-ONLY completeness rule, leak-guard byte-intact, specs clean, frozen present, generative panel keeps a non-target passer with both perturbable failure-modes guarded.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-24T15:18:42Z.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | Parent resolved = `solver_workflows/spider2-dbt-baseline` (`source:` + `@baseline` run `13fb630e2cae3eb8` config.json agree). Diff adds ONE hunk (`39a40,50`), a single "COMPLETENESS — BUILD EVERY DELIVERABLE" paragraph under §1 (DELIVERABLE = NEW MATERIALIZED MODEL(S)) of THE OUTPUT CONTRACT. No other section, no leak-guard/no-fetch prose touched. |
| G2 leak-guard (hidden gold) | PASS | grep of added (`>`) lines for `gold/expected_/answer_key/ground_truth/curl/wget/git clone/git ls-remote` = NO hits. Added text works only from "the instruction's own enumeration"; names no gold table/columns, reads no gold/expected file. No-fetch paragraph (README L11–15) unchanged by the diff. |
| G3 spec two fields | PASS | `diff full-baseline.yaml spd0002…yaml` = exactly 2 lines: `experiment:` and `agent.solver_workflow:`. spd0002 full spec preserves `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1`. |
| G4 smoke narrows tasks only | PASS | Smoke diff narrows only `benchmark.tasks` (61→5); no `exclude_tasks`, no other field. Surviving 5 = intercom001, analytics_engineering001, app_reporting002, mrr001, activity001 — both named targets present. (Header ABOUTME comment is stale boilerplate, not a field.) |
| G5 both frozen | PASS | Both frozen files exist (3223B / 1700B, Jun 24 14:37); full frozen carries `kind: spacedock_solver` + `runtime: codex`; smoke frozen carries `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the `## Hypothesis` claim verbatim-in-spirit (enumerate every distinct deliverable, build a separate base table for each, confirm count matches, do not stop after the first). Generative-build instruction, NOT self-anchored "verify your answer matches"; no added scope. |
| G7 actionability/inert-risk | WARN | Class = mechanical-ish ("enumerate EVERY distinct result table", "confirm the COUNT … equals the COUNT of deliverables") with concrete trigger cues ("and"/"as well as"/numbered/comma list) but NO worked-example skeleton. Count-and-add is more concrete than pure analytic prose, yet at gpt-5.5/xhigh an enumeration reflex with no skeleton can be acknowledged-but-skipped. Inert-risk: solver may re-count to the same wrong number. Suggest a worked deliverable-enumeration example if smoke is inert. |
| G8 regression-canary coverage | PASS | Generative (fires on every task, ungated). Smoke keeps a non-target `@baseline`-PASS canary (mrr001=1.0, other family) → not FAIL. Most-at-risk family = multi-deliverable: app_reporting002=1.0 is a perturbable multi-deliverable-family passer guarding mis-enumeration; activity001=1.0 single-deliverable sentinel guards the ADD-ONLY over-build mode (spurious extra table). Two distinct perturbable failure-modes covered. Note: only ONE perturbable canary (app_reporting002) for the multi-deliverable family specifically — borderline vs the "≥2 perturbable for most-at-risk family" PASS bar; treated PASS because the lever's dominant risk mode (over-build on single-deliverable) is separately and directly sentineled. |
| G9 selector independence | N/A | No multi-candidate / selector protocol declared. |
| G10 self-correcting false-positive | PASS | Self-correcting (check-and-add). (a) Generative but (b) the check is a structural COUNT/existence comparison ("count of built target tables = count of deliverables named"), not a re-derivation of values. (c) Explicitly ADD-ONLY: inserted text states "This step only ADDS any deliverable you have not yet built; it does NOT re-derive, rewrite, or change the values of a table you already built correctly. If your count already matches, change nothing." Cannot turn a right value wrong → spd0002-class SAFE. |

**For the captain:** Auto-approved to smoke — no FAILs. The 5-task smoke (2 targets FAIL→flip, mrr001/app_reporting002/activity001 PASS-canaries) is correct and baseline rewards re-confirmed from `13fb630e2cae3eb8/per_trial_outcomes.json`. Two WARN-adjacent watch-items: (1) G7 — no worked enumeration skeleton, so the count-reflex may be behaviorally inert at xhigh (re-counting to the same wrong number); add a skeleton if both targets stay FAIL. (2) G8 — only app_reporting002 is a perturbable multi-deliverable canary (one, not two) for the family the lever most directly perturbs; if the lever fires hot, watch for an UNSMOKED multi-deliverable family regressing on the full board.

## Smoke result

Proposed smoke set: targets + regression panel. `@baseline` rewards **re-confirmed at the propose gate**
from `runs/spider2-dbt-full-baseline/13fb630e2cae3eb8/per_trial_outcomes.json` (trial_name / reward):
intercom001=0.0 ❌, analytics_engineering001 (`analytics_engineerin__rukNQHo`)=0.0 ❌, app_reporting002=1.0 ✅,
mrr001=1.0 ✅, activity001=1.0 ✅ — all five glyphs below confirmed. `--explain` on the frozen smoke spec
lists exactly these 5 tasks (`Tasks: 5`), no more, none missing.

| Task | Baseline | Should pass in smoke? | Role |
|---|---|---|---|
| spider2-dbt-intercom001 | ❌ FAIL | 🎯 flip to PASS | Target — built 1 of 2 required tables (missing `intercom__company_metrics`). |
| spider2-dbt-analytics_engineering001 | ❌ FAIL | 🎯 flip to PASS | Target — built 1 of 2 required tables (missing `fact_purchase_order`). |
| spider2-dbt-app_reporting002 | ✅ PASS | ✅ must stay PASS | Perturbable canary — `app_reporting` is a multi-task family; guards the most-at-risk multi-deliverable shape. |
| spider2-dbt-mrr001 | ✅ PASS | ✅ must stay PASS | Perturbable canary — `mrr` family passer (mrr001+mrr002 both pass). |
| spider2-dbt-activity001 | ✅ PASS | ✅ must stay PASS | Sentinel — single-deliverable passer; must NOT sprout spurious extra tables. |

Net hoped-for: flip ≥1 of the 2 targets, lose zero sentinels/canaries. (movie_recomm001 omitted from the
smoke unless the propose read confirms it is the same completeness family rather than a value/scope miss.)

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the @baseline solver to solver_workflows/spd0002-build-every-deliverable and add ONLY the completeness rule — a ONE-KNOB diff vs the parent README; leak-guard byte-intact.
  Forked from `solver_workflows/spider2-dbt-baseline`; `diff` shows a single hunk (`39a40,50`) adding the "COMPLETENESS — BUILD EVERY DELIVERABLE THE INSTRUCTION NAMES" paragraph under §1 of THE OUTPUT CONTRACT; grep of added lines for `gold/expected_/answer_key/ground_truth/curl/wget/git clone` = 0 hits; ADD-ONLY (does not re-derive/rewrite values — G10-safe).
- DONE: Make + freeze the full spec (differing from full-baseline.yaml ONLY in experiment: + agent.solver_workflow:) and the smoke spec (tasks narrowed to EXACTLY the 5 smoke tasks).
  `diff full-baseline.yaml spd0002…yaml` = exactly 2 lines (experiment + solver_workflow); smoke diff narrows only `benchmark.tasks` (61→5, no exclude_tasks); both frozen via `rk freeze --allow-missing`.
- DONE: Verify the frozen smoke selection lists EXACTLY the 5 smoke tasks; re-confirm each @baseline reward and update the smoke-set table.
  `rk run …smoke.frozen.yaml --explain` → `Tasks: 5` = intercom001/analytics_engineering001/app_reporting002/mrr001/activity001; rewards from `13fb630e2cae3eb8/per_trial_outcomes.json`: 0.0/0.0/1.0/1.0/1.0 — matches the ❌/❌/✅/✅/✅ table.
- DONE: Run the gatekeeper subagent per `_gatekeeper/propose-review-guideline.md` and write the `## Gatekeeper review` block.
  Recommendation **APPROVE**; G1–G6/G8/G10 PASS, G7 WARN (no worked skeleton — possible inert-risk), G9 N/A; per-rule table + "For the captain" note written into the entity.

### Summary

Authored the spd0002 propose variant: a one-knob, additive, generative completeness rule on the forked
solver README (enumerate every deliverable the instruction names, build a base table for each, confirm
built-count == enumerated-count; ADD-ONLY, no value rewrite). Full + smoke specs made and frozen; full
spec differs from the anchor in only the two allowed fields, smoke narrows to exactly the 5 smoke tasks
(verified via `--explain`), and all five @baseline rewards re-confirmed. Gatekeeper returned APPROVE
(no FAILs; G7 WARN on inert-risk, G8 borderline-PASS with one perturbable multi-deliverable canary).
Did NOT launch the smoke run or advance the stage — that is the FO/captain's call.
