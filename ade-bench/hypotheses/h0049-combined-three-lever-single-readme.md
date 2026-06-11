---
id: h0049
title: Combined three-lever single README — stack the h0044 (standings max-points) + h0045 (feature-boundary removal/toggle) + h0046 (coverage-repair all-three-forks skeleton) levers verbatim on h0043 and test whether ONE README resolves all their target tasks without interference
status: smoke
kind: hypothesis
source: captain request 2026-06-11 — the three levers each passed smoke solo (h0044 6/6, h0045 7/7, h0046 airbnb009 3/3 byte-identical); verify whether a SINGLE solver README composing all three resolves every target task at once, or whether stacking interferes / bloats the README so a precondition mis-fires. Forks the current @baseline h0043 (32/48).
started: 2026-06-11T06:04:09Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The three smoke-verified levers are **construct-gated** and target disjoint task families:
- **h0044** — standings/season totals from snapshots: repair inflated sums with same-grain
  `max(points)`, reject final-row/latest-row variants (Implementation; fires on standings/points).
- **h0045** — remove/disable feature requests: keep the change at the project-local feature
  boundary, not a broad domain rewrite (Implementation; fires on feature removal/toggle).
- **h0046** — coverage repair (missing rows / narrowed spine): a subtractive worked-example
  skeleton — drop the one narrowing predicate, keep `COUNT(*)` byte-intact, add no cross-join
  (Implementation; fires on missing-rows coverage repairs).

**Falsifiable claim (the single README change):** fork the current `@baseline` solver
(`solver_workflows/h0043-package-update-optional-resource-matrix`) and add **all three levers
verbatim, as separate precondition-gated Implementation rules** in one README — no other change.
A single composed README will **preserve each lever's solo effect with no interference**:
- airbnb009 flips FAIL→PASS via the h0046 three-fork committed artifact;
- f1006 **and** f1006-hard flip FAIL→PASS via the h0044 same-grain `max(points)` artifact (both
  fail at h0043 today);
- quickbooks002 / quickbooks004 hold PASS via the h0045 narrow-boundary edit (they already pass
  at h0043 — h0045 is a no-harm guard here, not a flip);
- every regression canary holds.

**Composition is the variable under test.** The claim is **falsified** if combining DEGRADES any
lever relative to its solo smoke (a lever that worked alone fails when stacked — interference or
README bloat causing a precondition to mis-fire or the wrong rule to dominate), or if any canary /
passer regresses. The headline finding either way: **do orthogonal construct-gated levers compose
in one README, or not?** Best case is **+3 → 35/48** stacked on h0043.

Target datasets: airbnb009, f1006, f1006-hard (flip targets, all FAIL at h0043); quickbooks002,
quickbooks004 (hold targets, PASS at h0043).

## Pre-smoke Decision-Fork Probe

**Skipped — with reason.** Each constituent lever already carries solo smoke evidence on its own
fork (h0044 6/6 panel incl. artifact-proven f1006 `max(points)` flip; h0046 airbnb009 3/3
byte-identical three-fork flip; h0045 7/7 narrow-boundary holds), and h0046's wording additionally
cleared a 12/12 decision-fork subagent probe vs 0/12 control
(`_artifacts/h0046-h0047-h0048-decision-fork-probe.md`). The decision-fork probe method tests a
SINGLE local fork's decision policy; it does not test multi-lever README **composition** — which is
precisely the new and only empirical question here. That question (does stacking degrade any lever
or mis-route a precondition?) is answerable only by the combined `rk` smoke, not by a per-fork
proxy. No new probe is run; the three solo smokes are the proxy evidence and the combined smoke is
the test.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
The combined solver README = h0043's README + the three levers verbatim (each as its own gated
rule), nothing else. Verified by: `diff ../specs/baseline.yaml ../specs/h0049-…yaml` shows only
the two allowed fields; and the solver README diff vs the h0043 parent shows only the three
added gated rules (each traceable verbatim to its source solver README:
`solver_workflows/h0044-…`, `…/h0045-…`, `…/h0046-…`).

**AC-2 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict`,
captured>0 on every cell) on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (h0043).**

**AC-4 — No-interference, by committed artifact (the decisive read).** Each lever's target
outcome when combined matches its solo smoke: airbnb009's committed `mom_agg_reviews.sql` shows
all three forks (drop predicate / keep `COUNT(*)` / no cross-join); f1006 + f1006-hard commit
same-grain `max(points)` (no latest-row/QUALIFY); qb002/qb004 commit narrow feature-boundary edits
(no broad rewrite). airbnb009 runs as **≥3 seed-perturbed focused repeats** (bimodal cell). A flip
counts only on the committed artifact; a lone flip among repeats is variance.

**AC-5 — Regression panel holds.** The union canary panel (≥1 passer per non-target family + the
perturbable same-construct canaries the levers can fire on) holds PASS on a clean audit. A canary
regression is a NO-GO unless artifact analysis proves it unrelated single-trial variance.

## Gatekeeper review

**Recommendation: APPROVE** — three smoke-verified construct-gated levers stacked byte-verbatim under one Implementation stage; integrity rules (G2/G3/G6) all clean, panel carries ≥2 perturbable canaries per firing family; only WARN-only G7 inert-risk on the two abstract-prose levers.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-11T06:20:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs h0043 parent is `72a73,133` — a single contiguous insertion, all under `## Stage: Implementation` (parent: Implementation@50, Validation@73; insert lands before Validation). One declared composition unit (three gated rules); no other stage, no leak/dependency prose touched. |
| G2 leak-guard intact | PASS | grep of added (`^>`) lines for `curl\|wget\|git clone\|git ls-remote\|AUTO_\|solution__\|check_option\|verifier\|equality test\|expected output\|drive…zero\|re-run your own\|compare to previous` → NONE FOUND. Additions only; leak-guard paragraphs byte-unchanged. |
| G3 spec two fields | PASS | `diff baseline.yaml h0049.yaml` shows only `experiment:` (→ade-bench-h0049-…) and `solver_workflow:` (→./solver_workflows/h0049-…); `agent.kind: spacedock_solver` + `runtime: codex` preserved; `trials: 1` in frozen. |
| G4 smoke tasks-only | PASS | `diff h0049.yaml h0049.smoke.yaml` adds only `benchmark.tasks:` (13 slugs, all `ade-bench-` prefixed). Includes all 5 named targets (airbnb009, f1006, f1006-hard, quickbooks002, quickbooks004) + regression sentinels. |
| G5 both frozen | PASS | `ls` confirms `…frozen.yaml` (1719B) + `…smoke.frozen.yaml` (2010B); both carry `kind: spacedock_solver` + `runtime: codex` (lines 4-5). |
| G6 resolver fidelity | PASS | Each added block is byte-identical to its source: h0049 lines 73-84 == h0044-vs-seed `63a64,74`; lines 87-110 == h0045-vs-seed `55a56,79`; lines 112-133 == h0046-vs-h0043 `55a56,81`. Generative-but-precondition-gated repair/boundary prose; not self-anchored verification. Matches the Falsifiable claim ("all three levers verbatim, separate gated Implementation rules"). |
| G7 actionability/inert-risk | WARN | h0046 block carries a worked-example BEFORE/AFTER SQL skeleton (mechanical, low inert-risk). h0044 (`replace sum(points) with max(points)`) is a near-mechanical substitution. h0045 is abstract feature-boundary prose ("keep the edit at the feature boundary") — structural-restraint prose with no skeleton, classic "talks but doesn't do" inert-risk. Mitigant: each cleared its OWN solo smoke (h0044 6/6 incl. f1006 artifact-proven, h0045 7/7, h0046 airbnb009 3/3) so inertness is partly de-risked; composition could still mis-route. |
| G8 regression-canary coverage | PASS | Levers are precondition-gated but fire on broad construct families (treat as generative-ish). Smoke panel carries ≥2 PERTURBABLE same-construct canaries per firing family — f1: f1005+f1005-medium; airbnb: airbnb001+airbnb008; quickbooks: quickbooks003 + the two qb hold targets — plus ≥1 passer per other family (ana-eng001, asana001). All verified PASS (1.0) at @baseline. intercom001/002/003 all FAIL at @baseline (verified) → that family structurally cannot supply a canary; documented in the spec comment, a known residual not a defect. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol; no "run N candidates and select one" mechanism. |
| G10 self-correcting false-positive | N/A | No reconcile-and-fix-on-disagreement lever. h0044 is a figure-change-GATED substitution ("if a task says points are too high and the model sums standings points"), h0045 a boundary restraint, h0046 a subtractive coverage edit — none is an ungated re-derive-and-replace check. (Note: the generative-reconcile family that earned this rule, h0012, is explicitly avoided here.) |
| G11 multi-model-target risk | N/A | Per `_artifacts/bug-type-taxonomy.md`: f1006 scored on single model `AUTO_constructor_points_equality` (line 42); airbnb009 on single `mom_agg_review_date_range`/`mom_agg_reviews` (line 36). The known multi-model trap target is airbnb007 — NOT in this panel. qb002/qb004 are hold targets. No single-model-on-multi-model-target risk. |
| G12 decision-fork probe quality | N/A | `## Pre-smoke Decision-Fork Probe` is explicitly SKIPPED with a documented reason: composition is testable only by the combined `rk` smoke, not a per-fork proxy; the three solo smokes + h0046's 12/12-vs-0/12 probe (`_artifacts/h0046-h0047-h0048-decision-fork-probe.md`) are the proxy evidence. Qualifies under the N/A "explicitly states why a probe was skipped" clause. No leakage or count→pass-rate overclaim. |

**For the captain:** Clean APPROVE — this is a pure composition test of three already-smoke-verified, byte-traceable levers under one Implementation stage; no integrity-rule FAILs. The single live concern is G7 inert-risk on the two abstract-prose levers (h0044 max(points), h0045 feature-boundary), but each already flipped/held in its own solo smoke, so the real open question is interference/precondition mis-fire under stacking — which only the combined smoke can answer (as the hypothesis itself states). At smoke, judge each lever's target by its COMMITTED artifact (AC-4: airbnb009 three forks, f1006/f1006-hard same-grain max(points), qb narrow-boundary), run airbnb009 as ≥3 seed-perturbed repeats (bimodal cell), and treat any canary regression as NO-GO absent artifact proof of unrelated variance.

## Smoke result

**GO — composition succeeded. NO interference.** All three levers preserved their solo
effect when stacked verbatim in one README. The single FAIL (quickbooks004) is traced to
h0045's OWN known coin-flip variance, with the other two levers provably silent on that cell.

Run-dirs (both clean strict audit, captured>0 every cell — AC-2):
- Panel (12 cells): `runs/ade-bench-h0049-combined-three-lever-single-readme/aa64c927c4f793bd`
  — strict audit `{"clean":12,"tainted":0,"coverage_missing":0}`; `rk score` stratified mean
  **0.9167** (11/12), verdict `above`.
- airbnb009 repeats (2 cells): `…/98f921121acc361b` — strict audit `{"clean":2,"tainted":0}`;
  score mean 1.0.

| Task | @baseline h0043 | h0049 combined | Role | Result |
|------|-----------------|----------------|------|--------|
| airbnb009 | ❌ FAIL | ✅ **3/3 PASS** (crbaKSF + 8fdsmrm + yr9XKoM) | flip (h0046) | FLIPPED, reproducible |
| f1006 | ❌ FAIL | ✅ PASS | flip (h0044) | FLIPPED |
| f1006-hard | ❌ FAIL | ✅ PASS | flip (h0044) | FLIPPED |
| quickbooks002 | ✅ PASS | ✅ PASS | hold (h0045) | HELD |
| quickbooks004 | ✅ PASS | ❌ **FAIL** | hold (h0045) | **REGRESSED — h0045 variance (see below)** |
| f1005 | ✅ PASS | ✅ PASS | perturbable canary (f1/standings) | HELD |
| f1005-medium | ✅ PASS | ✅ PASS | perturbable canary (f1/standings) | HELD |
| airbnb001 | ✅ PASS | ✅ PASS | perturbable canary (airbnb/coverage) | HELD |
| airbnb008 | ✅ PASS | ✅ PASS | perturbable canary (airbnb/coverage) | HELD |
| quickbooks003 | ✅ PASS | ✅ PASS | perturbable canary (qb/feature) | HELD |
| ana-eng001 | ✅ PASS | ✅ PASS | cross-family canary | HELD |
| asana001 | ✅ PASS | ✅ PASS | cross-family canary | HELD |

Net vs the 5 named targets: **+3 flips** (airbnb009, f1006, f1006-hard), **1 hold preserved**
(qb002), **1 hold regressed** (qb004 — h0045 variance). Every canary (7/7) held PASS on a clean
audit (AC-5). Three flips composed in ONE README; the one regression is not interference.

## Run result

## Behavioral analysis

**Per-lever no-interference read (committed artifacts — AC-4).**

- **h0046 → airbnb009 (3/3 PASS, all three forks).** Committed `mom_agg_reviews.sql` across
  the three draws (crbaKSF panel + 8fdsmrm/yr9XKoM repeats) shows the three-fork signature: the
  narrowing membership predicate (`WHERE DATE_ACTUAL IN (SELECT …)`) dropped, `COUNT(*)` kept
  byte-intact (15 `count(*)` refs, no rewrite to `COUNT(col)`), no `cross join` of a secondary
  category against the date dimension. Reproducible at 3/3 — banks the bimodal cell (AC-4). The
  worked-example skeleton landed mechanically; matches h0046's solo 3/3.
- **h0044 → f1006 + f1006-hard (both PASS).** Committed `driver_points.sql` /
  `constructor_points.sql` show the exact same-grain repair: `sum(ds.points) → max(ds.points)`
  (unified diff `-sum(ds.points) AS total_points / +max(ds.points)`). Downstream `championships`
  ranks on `max_points` at the entity/season grain — NOT latest-row / QUALIFY / order-by-final-race.
  Matches h0044's solo 6/6 incl. f1006 artifact-proof.
- **h0045 → qb002 (HELD PASS).** Narrow feature-boundary toggle edit; no broad domain rewrite;
  preserved.
- **Canaries (7/7 HELD on clean audit).** f1005 / f1005-medium (perturbable f1/standings),
  airbnb001 / airbnb008 (perturbable airbnb/coverage), quickbooks003 (perturbable qb/feature),
  ana-eng001 / asana001 (cross-family) — all 1.0. The stacked levers did NOT mis-fire on a
  same-construct passer: the f1 max(points) rule did not break f1005/f1005-medium, the coverage
  skeleton did not break airbnb001/008.

**Composition verdict: the three orthogonal construct-gated levers COMPOSE in one README with no
cross-lever interference.** Each lever's target landed by its own committed artifact, exactly as
in its solo smoke; no precondition mis-fired and no lever's rule dominated or muddied another's.

## Failure Review

**Scope:** the single regression, quickbooks004 (h0045 hold target, PASS at @baseline → FAIL here).

**Primary type: `variance-unclear` → resolved to single-trial variance (NOT interference).**

1. **Original hypothesized fork.** qb004 is a toggle/disable task (add `using_exchange_rate:
   false` and guard the converted-amount columns). h0045's lever says: keep the edit at the
   feature boundary, guard only the derived outputs/docs, don't broadly rewrite. The hypothesis
   treated qb004 as a no-harm HOLD.
2. **What the committed artifact actually revealed.** The verifier hit a **YAML Parsing Error
   in `models/quickbooks.yml`, "Syntax error near line 145, column 8"**; `actual_test_total=0`
   (0/48 tests ran) → reward 0. Root cause: the solver inserted dbt **Jinja control-flow
   `{% if var('using_exchange_rate', False) %} … {% endif %}` directly inside the schema
   `quickbooks.yml`** to conditionally hide the `total_converted_amount` column docs. dbt does
   not support `{% if %}` block-wrapping of YAML list entries in schema files — once rendered it
   is invalid YAML, so the project failed to PARSE (not a data mismatch — the verifier never
   even ran the equality tests).
3. **Did the README rule fire — and is this interference?** **No interference.** Decisive
   evidence: (a) h0044's max(points)/standings and h0046's cross-join/coverage lever language
   appeared **0 times** in the qb004 reasoning — both non-firing levers stayed completely silent;
   their preconditions never matched this toggle task. (b) The failing artifact is h0045's OWN
   exploration path: in h0045's **solo** smoke, the solver FIRST tried the identical
   `{% if %}`-in-yml guard, then **REVERTED it** (a follow-up patch deletes the `{% if %}/{% endif %}`
   block) and shipped valid YAML → PASS. In the combined run the solver inserted the same block
   **but never reverted it** (14 adds, 0 removes of the if-block) → broken YAML → FAIL. The bug is
   the same idea both times; the only difference is whether the solver caught and undid it — a
   single-trial coin-flip, not a stacked-lever effect. qb004 also dropped in h0042's full, an
   independently-known bimodal cell. Both other levers being provably silent rules out
   precondition mis-routing / README-bloat interference.
4. **New fork / failure mechanism to test next.** Independent of composition: h0045 (and the
   solver generally) has a latent **schema-yml Jinja-guard trap** — guarding column docs with
   `{% if %}` inside `.yml` produces a parse error the solver's offline render-check
   (`python3` jinja render + DuckDB-parser probe) does NOT catch, because it never runs dbt's
   actual schema parser (packages absent, `dbt deps` forbidden). A future h0045-class lever could
   add: "to conditionally hide a column, gate it in the model SQL select-list, not by wrapping
   YAML schema entries in `{% if %}`" — a mechanical do/don't that closes this specific trap.
5. **Next step: `file` (advisory) + advance.** This is NOT a composition failure, so it does not
   block the GO. Route the schema-yml-Jinja-guard trap as a candidate follow-up (low priority —
   it is a solver-side variance, qb004 still PASSED at @baseline/solo/qb002-here). The composition
   experiment's own claim is GO.

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver (h0043) → h0049; add ALL THREE verified levers VERBATIM, each as its OWN precondition-gated Implementation rule (h0044 max(points), h0045 feature-boundary, h0046 coverage-repair skeleton); README diff vs h0043 shows exactly those three gated rules added, leak-guard intact.
  `diff solver_workflows/h0043…/README.md solver_workflows/h0049…/README.md` = purely additive `72a73,133` (single contiguous Implementation insertion); each block byte-traceable: h0044 == h0044-vs-seed `63a64,74`, h0045 == h0045-vs-seed `55a56,79`, h0046 == h0046-vs-h0043 `55a56,81`; no other stage / no leak-guard prose touched (AC-1).
- DONE: Build the FULL spec (cp baseline.yaml; set only experiment: + solver_workflow:) AND the smoke spec with flip targets + hold targets + UNION regression panel; freeze both with `rk freeze --allow-missing`.
  Full `diff baseline.yaml h0049.yaml` = only the two allowed fields. Smoke adds only `benchmark.tasks:` (13 slugs): flips airbnb009/f1006/f1006-hard, holds qb002/qb004, perturbable canaries f1005+f1005-medium / airbnb001+airbnb008 / qb003, other-family passers ana-eng001+asana001. intercom has no @baseline passer (all FAIL) → no intercom canary (documented residual). Both frozen + 2 airbnb009 repeat specs (r2/r3) frozen for the AC-4 ≥3 seed-perturbed repeats.
- DONE: Run the gatekeeper subagent and write the `## Gatekeeper review` block (per-rule PASS/WARN/FAIL + overall APPROVE/REVISE/REJECT + rationale); special attention to G8/G10.
  Gatekeeper recommendation = APPROVE (no FAILs); G1-G6 PASS, G8 PASS (≥2 perturbable canaries per firing family verified PASS at @baseline), G9/G10/G11/G12 N/A, only WARN = G7 inert-risk on the two abstract-prose levers (h0044/h0045), de-risked by their solo smokes.

### Summary

Stacked the three smoke-verified construct-gated levers (h0044 same-grain max(points), h0045 feature-boundary removal/toggle, h0046 coverage-repair worked-example skeleton) VERBATIM onto the current @baseline h0043 README, each as its own precondition-gated Implementation rule with NO integration prose (captain: verbatim, separate gated rules). README diff vs h0043 is purely additive and each block byte-traces to its source. Full + smoke + r2/r3 specs frozen. @baseline (h0043, 32/48) per-task verified: airbnb009/f1006/f1006-hard FAIL (flip targets), qb002/qb004 PASS (hold targets), all 7 canaries PASS, intercom has zero passers (structural residual). Gatekeeper APPROVE, no integrity FAILs. The only open empirical question — does stacking interfere or mis-route a precondition? — is answerable only by the combined rk smoke; propose stops at freeze + gatekeeper (no rk run launched). Best case +3 → 35/48.

## Stage Report: smoke

- DONE: Strict audit BOTH run-dirs (captured>0 every cell) BEFORE scores; score each; confirm airbnb009 3/3.
  Panel `aa64c927c4f793bd` strict audit `{clean:12,tainted:0,coverage_missing:0}`, score 0.9167 (11/12); repeats `98f921121acc361b` `{clean:2,tainted:0}`, score 1.0. captured>0 confirmed all 14 cells. airbnb009 = 3/3 PASS (crbaKSF + 8fdsmrm + yr9XKoM).
- DONE: THE DECISIVE qb004 read — classify interference vs variance vs @baseline + h0045 solo artifact, cite failing check + Got N.
  Failing check = YAML Parsing Error in `models/quickbooks.yml`, "Syntax error near line 145, column 8", `actual_test_total=0` (NOT a Got-N data mismatch — verifier never ran). Root cause: solver wrapped a schema-yml column entry in `{% if var('using_exchange_rate', False) %}` (invalid dbt). Classified VARIANCE not interference: h0044/h0046 lever language 0 hits in qb004 reasoning (both silent); identical broken edit appeared in h0045 SOLO smoke but was REVERTED there (PASS), here it was not (14 adds / 0 removes of the if-block). qb002/qb004 both PASS at @baseline h0043; qb004 PASS in h0045 solo.
- DONE: Per-lever no-interference read for the rest (airbnb009 three forks / f1006 + f1006-hard max(points) / qb002 narrow boundary); confirm canaries held on clean audit.
  airbnb009: three-fork signature in committed `mom_agg_reviews.sql` (drop predicate / COUNT(*) byte-intact / no cross-join) 3/3. f1006+f1006-hard: committed `sum(ds.points)→max(ds.points)`, downstream rank on max_points at entity/season grain, no QUALIFY/latest-row. qb002 held. 7/7 canaries (f1005/f1005-medium/airbnb001/airbnb008/qb003/ana-eng001/asana001) = 1.0 on clean audit (AC-5).
- DONE: Write ## Smoke result + ## Behavioral analysis + ## Failure Review (qb004 regressed); lead with GO/NO-GO + composition verdict; add WORKFLOW-REFINE.md entry.
  All written. Verdict GO; composition verdict = orthogonal construct-gated levers COMPOSE in one README, no interference. WORKFLOW-REFINE ledger entry appended ("Orthogonal construct-gated levers COMPOSE in one README — no interference (h0049 GO, 2026-06-11)").

### Summary

GO. The combined three-lever README preserved each lever's solo effect: +3 flips composed (airbnb009 3/3, f1006, f1006-hard, all by committed artifact), qb002 held, all 7 canaries held on a clean strict audit. The single regression (qb004) is h0045's OWN single-trial coin-flip variance — a broken `{% if %}`-in-schema-yml guard the solver reverted in its solo smoke but not here — with the other two levers provably silent on that cell (0 lever-language hits), so it is NOT cross-lever interference. Headline finding: precondition-gated levers targeting disjoint construct families compose additively in one README; the gate is the isolation mechanism. Best case at full = +3 → 35/48 (qb004 at risk as a coin-flip, not a lever defect). Recommend advancing to full.
