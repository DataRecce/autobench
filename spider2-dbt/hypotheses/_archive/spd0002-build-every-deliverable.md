---
id: spd0002
title: Build EVERY result table the instruction enumerates (completeness lever)
status: conclude
kind: hypothesis
source: re-scoped from spd0001 anchor deep-dive (the original materialization framing is dead — 0 ephemeral fails board-wide; re-aimed at the 3 tractable incomplete-deliverable fails)
started: 2026-06-24T14:34:28Z
completed: 2026-06-24T15:31:51Z
verdict: REJECTED
score: 0.9
worktree:
archived: 2026-06-24T15:31:51Z
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

## Smoke result

**NO-GO — confirmed.** Run `runs/spider2-dbt-spd0002-build-every-deliverable/e911007671be4f08`
(rc=0, 2/5). 0 of 2 targets flipped, and a `@baseline` PASSER (mrr001) REGRESSED to FAIL — a canary
regression is an automatic NO-GO regardless of targets.

**Clean-audit attestation:** `rk audit --policy strict` on the run-dir → `summary: {clean: 5,
coverage_missing: 0, tainted: 0}`, every cell `taint_status: clean`, no findings. The 2/5 is a real
behavioral result, not infra taint.

| Task | Baseline | Smoke | Δ | Built tables (committed artifact) | Distance to PASS |
|---|---|---|---|---|---|
| intercom001 (🎯) | ❌ 0.0 | ❌ 0.0 | — | only `intercom__admin_metrics` (0 rows) | 2nd table `intercom__company_metrics` NEVER built — rule INERT |
| analytics_engineering001 (🎯) | ❌ 0.0 | ❌ 0.0 | — | BOTH `fact_purchase_order` (14r) + `obt_customer_reporting` (14r) | 2nd table BUILT, but values/row-set wrong — fired-but-still-fail |
| app_reporting002 (✅ canary) | ✅ 1.0 | ✅ 1.0 | held | (PASS, empty verifier stdout) | held |
| mrr001 (✅ canary) | ✅ 1.0 | ❌ 0.0 | **REGRESSED** | `mrr` 417 rows (+ added `util_months` spine) | baseline `mrr` was 410 rows — +7 phantom rows |
| activity001 (✅ sentinel) | ✅ 1.0 | ✅ 1.0 | held | (PASS, empty verifier stdout) | held |

Verifier stdout for all 3 fails = `mismatch (predicted=/app/<db>.duckdb)` (a row/value/count mismatch,
not a missing-table error — the named tables all exist; they just don't match gold).

## Behavioral analysis

Per-cell whys from the committed artifacts (built tables + model file list in the worker's final
validation summary), NOT the agent's "0 mismatches" self-report.

**intercom001 — INERT (rule discussed-or-skipped, 2nd table NOT built).** The solver built only
`main.intercom__admin_metrics` (0 rows — upstream had 0 conversations with `last_close_by_admin_id`).
The previously-missing `intercom__company_metrics` was NEVER built; grep of the transcript for
`company_metrics` = 0 hits. The enumerate-deliverables reflex did not fire on the second table at all.
This is the gatekeeper's G7 WARN materialising exactly as predicted: a count-and-add rule with NO
worked enumeration skeleton is acknowledged-but-skipped at gpt-5.5/xhigh — the solver re-counted the
instruction's deliverables to the same (wrong) count of one and stopped. (Note also: even had the rule
fired, the built `admin_metrics` is 0 rows, so intercom001 has a deeper data/grain problem behind the
completeness miss.)

**analytics_engineering001 — FIRED-BUT-STILL-FAIL (2nd table built, wrong values/row-set).** The rule
DID fire: the solver built BOTH `main.fact_purchase_order` (14 rows, grain `purchase_order_detail_id`)
AND `main.obt_customer_reporting` — the missing second gold table now exists as a base table. But it
still scored 0.0, and worse, building the new `fact_purchase_order` and re-sourcing the OBT off it
COLLAPSED `obt_customer_reporting` from the baseline's **55 rows → 14 rows**. The completeness rule
fixed the count (1→2 tables) but the constructed fact narrowed the row set 4x (14 received/approved
detail lines vs the 55 the baseline OBT carried), so neither table matches gold. Adding the second
deliverable changed the FIRST deliverable's row set — the rule is not value-safe in practice even
though it is ADD-ONLY in letter.

**mrr001 — REGRESSION (headline; see Failure Review).** Single `mrr` table both runs, but the rule
drove an extra helper model + a grain expansion 410→417.

## Failure Review

**Primary failure type: `canary-bleed`.** (The lone gate-decisive fact is the mrr001 regression: a
generative ADD-ONLY rule, claimed value-safe at the gate, bled onto an unrelated single-deliverable
passer and broke it. The two targets are secondary — one inert, one fired-but-still-fail — and neither
flips, but the canary regression alone forces the verdict.)

**mrr001 regression root-cause (the headline).** Baseline mrr001 (`13fb630e2cae3eb8/…__cmzeCgv`,
reward 1.0) built ONE model `models/mrr.sql` → `main.mrr` at **410 rows**, first row
`2019-04-01, customer_id=1, mrr=50.0, change_category=reactivation`. Under the lever
(`e911…/…__HhNGgtW`, reward 0.0) the solver built `main.mrr` at **417 rows** AND added a SECOND model
`models/utils/util_months.sql` — a month-spine helper. The "build a separate base table for EACH
enumerated deliverable / build EVERY deliverable" rule was read as license to construct a complete
month dimension and join `mrr` against it, zero-filling ~7 phantom customer-months that have no MRR
activity (410→417). The committed first row shifted from `2019-04-01` to `2019-06-01` and from
`change_category=reactivation` to `upgrade`, so the row-by-row compare against gold mismatches. This
is a direct violation of Output-Contract §4 ("scope output to the entities that actually have the
relevant activity unless completeness is explicitly requested; do not zero-fill phantom rows"): the
new completeness paragraph under §1 semantically OVER-RODE the §4 anti-zero-fill rule. The exact
mechanism the gatekeeper flagged borderline at G8 — an ungated generative reflex perturbing a passer.
The lever is "ADD-ONLY" only at the table-COUNT level; at the ROW-SET level it is destructive (the
spine helper expands grain on a table that was already correct).

**The 5 questions.**
1. **Original hypothesized fork:** the solver stops after the first deliverable; a count-and-add rule
   makes it build the missing second gold table → intercom001 / analytics_engineering001 flip.
2. **Fork the artifact actually revealed:** the rule is BOTH inert (intercom — no skeleton, re-counts
   to one) AND, where it fires, not row-set-safe (analytics — building deliverable #2 collapses
   deliverable #1 from 55→14; mrr — the "build every deliverable" framing licenses a spurious month
   spine that zero-fills 7 phantom rows). Completeness-of-COUNT does not equal correctness-of-ROW-SET,
   and the rule trades against the existing anti-zero-fill contract.
3. **Did the rule fire, with artifact evidence?** Mixed: INERT on intercom001 (`company_metrics`
   never built, 0 grep hits); FIRED on analytics_engineering001 (both `fact_purchase_order` +
   `obt_customer_reporting` materialized as base tables); FIRED-and-overbuilt on mrr001 (added
   `util_months` spine, 410→417 rows). Evidence = each cell's worker final validation summary (built
   table names, grain, row counts, representative rows) cross-checked vs the baseline cells.
4. **New fork / mechanism to test next:** none promising. The two distinct failure modes (no-skeleton
   inertness; count-safe-but-row-set-destructive over-fire) are in tension — adding a worked skeleton
   to cure the inertness would make the over-fire HOTTER (more spurious spines / wider grain on more
   tasks), worsening the canary bleed. A count-of-deliverables reflex cannot be made row-set-safe via
   README prose because it has no oracle for the correct row scope; "every deliverable" is intrinsically
   pro-completeness and fights §4's pro-activity-scope rule. This is the same wall as DAB's generative
   over-fire family (e.g. dab0017 fires-everywhere levers add ±variance not stable lift).
5. **Next step:** `stop` → conclude REJECTED. Cleanly falsified by committed artifacts: 0/2 targets
   flip, a 6/6-equivalent single-draw passer regresses via a lever-attributable spurious-spine
   mechanism, and the two failure modes are mutually exclusive to fix.

**Route recommendation: smoke → conclude (REJECTED).** Not revisable — a worked skeleton (the only
obvious "fix" for the intercom inertness) would amplify the mrr/analytics over-fire, not cure it.
This is a rule tweak inside an existing §1, NOT a structural solver-workflow change, so no
WORKFLOW-REFINE entry is required (entity + self-learning suffice).

## Follow-up Routing

`smoke → conclude (REJECTED)`. No follow-up hypothesis. The completeness/enumerate-deliverables
README lever family is closed for spider2-dbt at gpt-5.5/xhigh on this evidence: count-completeness is
not row-set-correctness, and the reflex cannot be tightened (skeleton) without worsening the canary
bleed it already causes. Do NOT advance the stage here — the FO presents the gate.

## Verdict

**REJECTED** at smoke (captain-approved 2026-06-24; routed `smoke → conclude`, no full run). Clean
strict audit (5/5 clean, 0 coverage_missing, 0 tainted) — the 2/5 is a real behavioral result.

The "build EVERY deliverable the instruction enumerates" completeness lever failed on both axes:
- **0/2 targets flipped.** intercom001 INERT (count-reflex re-counted to one, never built the 2nd
  table — the G7 no-skeleton inert-risk, realized); analytics_engineering001 FIRED-but-still-fail
  (built deliverable #2 but the new `fact_purchase_order` collapsed deliverable #1's OBT row set
  55→14 — adding the 2nd table broke the 1st).
- **mrr001 canary REGRESSED** (PASS→FAIL): the generative rule licensed a spurious `util_months`
  month-spine, zero-filling ~7 phantom customer-months (410→417 rows), directly violating the output
  contract's anti-zero-fill rule. The G8 generative bleed the gatekeeper flagged borderline.

**Transferable lesson (also `_artifacts/self-learning.md`):** count-completeness is NOT
row-set-correctness. A generative "build every deliverable" reflex has no oracle for *correct scope*,
so it structurally fights the contract's row-set discipline — and the only cure for the inert target
(a worked skeleton) makes the over-fire bleed *hotter*. The two failure modes are mutually exclusive
to fix via README prose. The completeness/enumerate-deliverables lever family is **closed** for
spider2-dbt at gpt-5.5/xhigh. This also refines the spd0001 anchor read: the "3 tractable
incomplete-deliverable" misses were not a single closeable gap — analytics over-built when pushed, and
the generic push damages single-deliverable passers board-wide. Same wall as DAB's generative
over-fire family.

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

## Stage Report: smoke

- DONE: Per-TARGET behavioral why (intercom001, analytics_engineering001): did the completeness rule FIRE — i.e., did the solver build the previously-missing SECOND gold table as a base table? Classify each. Cite the artifact, not the agent's self-report.
  intercom001 = INERT: only `intercom__admin_metrics` (0 rows) built; `intercom__company_metrics` NEVER materialized (0 grep hits) — G7 WARN realized. analytics_engineering001 = FIRED-but-still-fail: BOTH `fact_purchase_order` (14r) + `obt_customer_reporting` built, but the new fact collapsed the OBT row set 55→14 vs baseline. Evidence = each cell's worker final validation summary (built table names + grain + row counts).
- DONE: mrr001 REGRESSION root-cause (headline): compare smoke vs @baseline; name the exact mechanism.
  Baseline `main.mrr` = 410 rows (one model). Smoke `main.mrr` = 417 rows + an added `models/utils/util_months.sql` spine. The "build EVERY deliverable" rule licensed a complete month dimension joined to `mrr`, zero-filling ~7 phantom customer-months (violates Output-Contract §4 anti-zero-fill) → row-by-row mismatch. The G8 generative canary-bleed the gatekeeper flagged borderline.
- DONE: Write `## Smoke result` (flip/distance table + clean-audit attestation), `## Behavioral analysis`, `## Failure Review` (one primary type + 5 questions + route). Do NOT advance the stage.
  All sections written. Clean-audit attested: `rk audit --policy strict` → clean 5 / coverage_missing 0 / tainted 0. Primary failure type = `canary-bleed`. Route recommendation = smoke → conclude (REJECTED). Stage NOT advanced (FO presents the gate).

### Summary

spd0002 smoke is a confirmed NO-GO. Clean strict audit (5 clean, 0 coverage_missing, 0 tainted) — the 2/5 is real, not infra. Both targets miss: intercom001 INERT (no worked skeleton → count-reflex re-counts to one, second table never built), analytics_engineering001 FIRED-but-still-fail (built deliverable #2 but the new fact collapsed deliverable #1's row set 55→14). The headline is the mrr001 regression: the generative "build every deliverable" rule drove a spurious `util_months` month-spine that zero-filled 7 phantom rows (410→417), breaking a passer and directly contradicting Output-Contract §4. Primary failure type `canary-bleed`; recommend conclude REJECTED — the two failure modes are mutually exclusive to fix (a skeleton cures inertness but amplifies the over-fire bleed). Rule tweak inside §1, so no WORKFLOW-REFINE entry needed.
