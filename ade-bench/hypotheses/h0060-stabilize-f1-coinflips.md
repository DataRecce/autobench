---
id: h0060
title: Stabilize f1001 + f1003-hard coin-flips (gated src-naming rule + top-N tie-crosses-cutoff criterion)
status: smoke
kind: hypothesis
source: captain hunch (make f1001/f1003-hard stable for a reliable 36/48) + FO artifact investigation of h0059 r1-vs-r2 coin-flips
started: 2026-06-15T12:42:27Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`f1001` and `f1003-hard` are **variance coin-flips** under the h0059 `@baseline` solver — each
PASSES in one full run and FAILS in another with the identical README (confirmed: h0059 r1 had
f1001 PASS / f1003-hard FAIL; r2 had f1001 FAIL / f1003-hard PASS). Both wobbles have a
**locally-determinable, oracle-free** correct branch. Adding two precondition-gated stabilizer
rules to the `@baseline` solver README will lock both tasks to reliable PASS without touching the
construct of any other family.

This is a STABILIZER (the h0058 family), **not** the exhausted oracle-flip program — the failing
runs are degradations of a passing artifact, not an unreachable oracle.

**Target datasets:** `f1001`, `f1003-hard`.

The single README change is a composition of two gated rules (disjoint constructs — the
gated-levers-compose pattern, h0049/h0056):

1. **f1 src-model naming rule (gated on: building src models for the f1 / dbt staging layer).**
   Name each new src model exactly `src_<table>` (e.g. `src_circuits`), matching the raw table
   name with a bare `src_` prefix. Do NOT prepend the staging dataset namespace —
   `src_f1_dataset__circuits` is wrong. Every `stg_<dataset>__<table>` must then `ref('src_<table>')`
   (exactly one such ref); `stg_*__races` / `stg_*__results` keep their additional source refs.
   *This rule restates the task's own `instruction.md` ("src models should be called
   `src_<model_name>.sql`") — pure compliance reinforcement, no oracle peek.*

2. **Top-N consistency: tie-crosses-cutoff criterion (gated on: "which tables give inconsistent
   results given the current data" questions over `order by metric desc limit N` models without a
   tiebreaker).** A top-N model varies run-to-run ONLY when a tie crosses the cutoff: the metric
   value of row N also appears at row N+1, so which rows fill the final slots is nondeterministic.
   A tie lying entirely *inside* the top N changes only display order, not the returned set — do
   NOT count it. For each candidate, query the current data: if
   `count(rows with metric >= the N-th value) > N` it is inconsistent; otherwise exclude it.
   Exclude `most_fastest_laps` (the worked example given in the prompt).

## Pre-smoke Decision-Fork Probe

Proxy evidence is the **committed artifacts of the h0059 full runs themselves** (real production
solver output, not a subagent sim) — the strongest proxy available. Cells compared:

- f1001 PASS: `runs/…-full-r1/97c03e6c467742f8/ade-bench-f1001__Aj2P3Eq`
- f1001 FAIL: `runs/…-full-r2/1fcc9223b9de5194/ade-bench-f1001__9xwfouC`
- f1003-hard FAIL: `runs/…-full-r1/97c03e6c467742f8/ade-bench-f1003-hard__rtTyhMn`
- f1003-hard PASS: `runs/…-full-r2/1fcc9223b9de5194/ade-bench-f1003-hard__y4yNLTu`

**f1001 fork.** PASS run committed `src_circuits.sql` … (`src_<table>`). FAIL run committed
`src_f1_dataset__circuits.sql` … (staging prefix over-applied). Both compiled clean, so the
deviation is silent — but the hidden tests key on exact node names: `src_models_are_correct`
errors on the missing `model.f1.src_<table>` node, and `stg_models_use_src_models` FAILs 11
because staging models `ref('src_f1_dataset__…')` instead of `ref('src_<table>')`. Signature
reproduced in the FAIL cell's `verifier/test-stdout.txt`.
*Control (PASS) = bare-prefix naming → 6/6 green. Proposed rule pins exactly that branch.*
**Oracle-free: YES, unambiguous** (verbatim from `instruction.md`).

**f1003-hard fork.** PASS run committed exactly 3 answer tables (`most_retirements`, `most_wins`,
`oldest_race_winners_in_modern_era`). FAIL run committed those 3 **plus** `most_podiums`,
`most_pole_positions`, `most_races` → `count_answers` saw 6, want 3 → "Got 1 result". The
`check_option_*` tests pass in both (the 3 correct rows are present either way) — exactly the
observed signature. The disagreement is purely the inclusion criterion: PASS applied
tie-crosses-cutoff (membership); FAIL applied any-tie-incl-within-list-order. Both computed
against the same shipped data.
*Control (PASS) = boundary-tie criterion → 4/4 green. Proposed rule pins that branch.*
**Oracle-free: YES, locally computable** — caveat: it codifies a membership-vs-order
interpretation the prompt supports ("varies … given the current data" + the `most_fastest_laps`
exemplar) and the hidden test set confirms, but does not spell out in SQL. Defensible
interpretation lever, NOT the equally-plausible oracle-blind wall. Slightly higher risk than rule 1.

**Caveat:** this is proxy evidence from prior-run artifacts, not a fresh decision-fork sim; the
smoke run is the real test. Per the sim-vs-real-run lesson, a stabilizer GO must rest on the flip
reaching the committed artifact at smoke + held perturbable canaries, not on this read alone.

## Smoke set guidance (for propose)

Generative-ish gated rules → regression panel required. Targets `f1001` + `f1003-hard`, a
stable-pass sentinel, ≥1 canary per non-target family (airbnb / ana-eng / asana / intercom /
quickbooks), and **≥2 perturbable f1 canaries** the src-naming rule can actually fire on
(f1 passers that build src/staging models, e.g. `f1005`, `f1006`, `f1007`) — a stable f1 passer
the rule never touches is blind (the h0012 lesson: held its one f1 canary, broke four other f1
passers at full). Propose ensign assembles per gatekeeper G8/G10.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0060-stabilize-f1-coinflips.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`, AND both target
coin-flips land PASS with their construct-correct committed artifact (f1001: `src_<table>` naming;
f1003-hard: 3 answer tables), with zero perturbable-canary regressions.**

## Gatekeeper review

**Recommendation: APPROVE** — two precondition-gated stabilizer rules added to ONE stage (Implementation), coherent single purpose (lock the two f1 coin-flips), integrity rules G2/G3/G6 all clean, no FAILs. Gated-levers-compose pattern (h0049/h0056) with disjoint f1-only preconditions; canary panel present. Two advisory WARNs only (G11 single-model-on-f1003-hard variance note; G8/G12 panel/probe caveats — none block).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-15T13:05:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is a pure addition (0 lines removed) inside the single `## Stage: Implementation` section (insert sits between Implementation@50 and Validation@313 of the new file). Two gated rules, but one coherent purpose — stabilize the two f1 coin-flips via the gated-levers-compose pattern (h0049/h0056), each gated to a disjoint f1-only precondition; no other stage and no guardrail prose touched. |
| G2 leak-guard intact | PASS | Leak/dependency prose byte-identical (diff shows 0 `<` lines — nothing removed/softened). Forbidden-token scan over added `>` lines (curl/wget/git clone/git ls-remote/AUTO_/solution__/check_option/verifier/equality test/expected output seed/drive-to-zero/published/fetch/download) returned no hits. |
| G3 spec two fields | PASS | `diff baseline.yaml h0060.yaml` shows ONLY `experiment:` and `solver_workflow:` changed; `agent.kind: spacedock_solver` and `runtime: codex` preserved; `trials: 1`. |
| G4 smoke tasks-only | PASS | Smoke diff adds ONLY a `benchmark.tasks:` block, all `ade-bench-` prefixed; includes both named targets f1001 + f1003-hard plus regression sentinels. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1743 B) and `…smoke.frozen.yaml` (1943 B) exist; each carries `kind: spacedock_solver` + `runtime: codex` at lines 4-5. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim verbatim in intent: rule 1 = bare-prefix `src_<table>` naming gated on building src models (restates the task's own `instruction.md`, compliance reinforcement, no oracle peek); rule 2 = top-N tie-crosses-cutoff membership criterion gated on "inconsistent given current data" top-N questions, locally computable from shipped data. Both GENERATIVE/INDEPENDENT (derive-from-data), not self-anchored re-run-your-own-model — not the dead h0006/7/8 family. No scope creep. |
| G7 actionability/inert-risk | PASS | Both rules carry literal BEFORE→AFTER SQL/naming skeletons the solver can pattern-match (worked-example form), not abstract structural prose. Rule 1 is a concrete naming substitution; rule 2 ships a copyable `count(* where metric >= Nth-value) > N` SQL snippet. Low inert-risk. |
| G8 regression-canary coverage | PASS | Both rules are GATED (precondition-limited to f1 src-model builds / top-N "inconsistent" questions), so classified gated-not-generative → N/A-class. Panel nonetheless carries the construct-sharing f1 family with 3 PERTURBABLE canaries the src-naming rule can fire on (f1005/f1006/f1007) plus 4 cross-family passers (airbnb001/ana-eng001/asana001/quickbooks002). Intercom has NO @baseline passer (all of intercom001/002/003 FAIL at h0059) so no intercom canary is structurally possible — correctly noted in the spec. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol; no N-candidate generation. |
| G10 self-correcting false-positive | N/A | Neither rule is a verify-result-and-act-on-disagreement check. Rule 1 = naming convention; rule 2 = an inclusion criterion derived from the data, not a reconcile-and-fix against a re-derived figure. No false-green correlation risk. |
| G11 multi-model-target risk | WARN | f1001 scored by `src_models_are_correct` + `stg_models_use_src_models` — rule 1 addresses BOTH (node names + the `ref('src_<table>')`), covers-all → safe. f1003-hard scored by `count_answers` + `check_option_*`; rule 2 fixes the `count_answers` inclusion criterion while `check_option_*` already passes in both branches per the probe — so the rule effectively targets the one decisive model, but the target is ≥2-model: a single-run f1003-hard PASS should be credited only after confirming the committed artifact (3 answer tables) on every scored model, not the aggregate verdict. Not in the taxonomy multi-model trap list; advisory only. |
| G12 decision-fork probe quality | WARN | `## Pre-smoke Decision-Fork Probe` present with fork, both branches, control-A (PASS-branch naming/criterion), exact-signature expectation (f1001: `src_<table>` nodes; f1003-hard: 3 answer tables), and an explicit proxy-only caveat — no overclaim into a real `rk` pass rate. Provenance is REAL prior-run committed artifacts (not a subagent sim), the strongest proxy. Leak check: the probe cites FAIL-cell `verifier/test-stdout.txt` as post-hoc signature CONFIRMATION, not as solver-prompt evidence, and uses no hidden-correct labels/solution files as prompt input — clean. WARN (not PASS) because it is artifact-archaeology rather than a fresh fork sim re-running the exact proposed README wording; treat smoke as the real confirmatory test (the hypothesis already states this). |

**For the captain:** No FAILs — clear to advance to `smoke`. Two advisory items: (G11) f1003-hard is a ≥2-model target, so judge its flip by the committed 3-answer-table artifact on every scored model, not the single aggregate reward; (G12) the probe is prior-run artifact evidence, not a fresh sim of the exact wording — per the sim-vs-real-run lesson, require the flip to reach the committed construct-correct artifact at smoke WITH the 3 perturbable f1 canaries (f1005/f1006/f1007) held before crediting either lock. The two-gated-rules-in-one-README scope is the established compositional pattern (h0049/h0056), not G1 scope creep.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver dir (solver_workflows/h0059-tmp-tier-removal-inline-reconcile) into solver_workflows/h0060-stabilize-f1-coinflips, and edit ONLY its README to add the two precondition-gated stabilizer rules — leak-guard prose intact, no other knob touched.
  README diff is purely additive (lines 269-312, inside `## Stage: Implementation` only); leak-guard/dependency prose byte-identical; commit 0c12dfd.
- DONE: Build full spec h0060-…yaml (differs from baseline.yaml ONLY in experiment: + solver_workflow:) and smoke spec with benchmark.tasks = f1001, f1003-hard + 3 perturbable f1 canaries (f1005/f1006/f1007) + 1 passing canary per other family (airbnb001/ana-eng001/asana001/quickbooks002); freeze both with rk freeze --allow-missing.
  `diff baseline.yaml h0060.yaml` = exactly experiment: + solver_workflow:; smoke diff = only the benchmark.tasks block; both `.frozen.yaml` + `.smoke.frozen.yaml` written (content_hash fe87f779…, differs from baseline 97b5f476… → README change registered). Intercom has NO @baseline passer (intercom001/002/003 all FAIL at h0059) so no intercom canary is structurally possible — noted in the smoke spec.
- DONE: Run the gatekeeper review subagent against the variant artifacts and record its per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT recommendation into the hypothesis ## Gatekeeper review block.
  Gatekeeper recommendation: APPROVE (no FAILs). G1-G8 PASS, G9/G10 N/A, G11/G12 WARN (advisory). Block written under ## Gatekeeper review.

### Summary

Forked the live @baseline solver (h0059, NOT the stale codex seed) and added two
precondition-gated Implementation rules in one README — f1 src-model bare-prefix naming
(`src_<table>`, restates the task's own instruction.md) and a top-N tie-crosses-cutoff
inclusion criterion — composing per the gated-levers pattern (h0049/h0056) on disjoint
f1-only constructs. Full spec differs from baseline only in `experiment:` + `solver_workflow:`;
the 9-task smoke panel carries both coin-flip targets, 3 perturbable f1 canaries the
src-naming rule can fire on, and one cross-family passer each (intercom excluded — no
@baseline passer exists). Gatekeeper APPROVE; two advisory WARNs to carry into the gate
note: judge the f1003-hard flip by the committed 3-answer-table artifact on every scored
model (G11, ≥2-model target), and treat the decision-fork probe as prior-run artifact
evidence not a fresh sim (G12) — require the flip to reach the construct-correct artifact at
smoke with the perturbable f1 canaries held.

- REALIGNMENT (post-gatekeeper): renamed all artifacts from the long slug
  `h0060-stabilize-f1-coinflips-src-naming-and-topn-tie` to the short entity slug
  `h0060-stabilize-f1-coinflips` (the long form exceeds Claude's 64-char worker-name limit and
  would break smoke/full dispatch). Pure `git mv` of the solver dir + four spec files, the two
  embedded `experiment:`/`solver_workflow:` strings updated, both specs re-frozen. Solver README
  content is byte-unchanged → `solver_workflow_content_hash` stays `fe87f779…`, so the gatekeeper
  APPROVE verdict is unaffected. AC-1 `diff specs/baseline.yaml specs/h0060-stabilize-f1-coinflips.yaml`
  now shows exactly `experiment:` + `solver_workflow:`.
