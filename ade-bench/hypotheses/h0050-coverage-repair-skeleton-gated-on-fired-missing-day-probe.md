---
id: h0050
title: Scoped coverage-repair skeleton — gate the all-three-fork predicate-drop on a FIRED local missing-day probe so it fires ONLY on genuine coverage gaps (keep airbnb009, spare airbnb008)
status: smoke
kind: hypothesis
source: "h0046 full analyze (2026-06-11) — h0046 proved airbnb009 is now REPRODUCIBLY pinnable (4/4 byte-identical, breaking the h0019/h0042 non-reproducibility wall) but bled onto same-family airbnb008 (the G8 risk realized): the subtractive skeleton fired on airbnb008 whose narrowing predicate was already correct (its real bug was a 1-line YAML quote). This follow-up scopes the skeleton to fire only when a local probe proves rows are genuinely missing. Forks the current @baseline h0043 (32/48). Captain-approved filing 2026-06-11."
started: 2026-06-12T02:03:54Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

h0046's all-three-fork coverage skeleton is **artifact-correct and reproducible** (airbnb009
flipped FAIL→PASS 4/4 byte-identical across smoke+full) but **too eager**: as an unconditional
"any coverage-shaped CTE → drop the narrowing predicate" rule it FIRED on airbnb008 — a sibling
whose narrowing predicate was already correct (airbnb008's real bug was a YAML quote, NOT missing
days) — and broke `AUTO_mom_agg_reviews_equality` (Got 28631). That is a real generative
same-family scoping defect, not variance.

**Falsifiable claim (the single README change):** fork the current `@baseline` solver
(`solver_workflows/h0043-package-update-optional-resource-matrix`) and add h0046's all-three-fork
coverage-repair worked-example skeleton **gated on a FIRED local missing-day probe** — the
subtractive predicate-drop applies ONLY when the solver has locally verified rows are genuinely
missing (e.g. build the model, compare its date/key coverage against the complete dimension; if
and only if the dimension contains keys absent from the output does the coverage repair fire). The
probe is **oracle-free** (row-count / date-coverage vs the local dimension — no hidden test). When
the probe is empty (no missing rows), the skeleton does NOT fire and the model is left byte-intact.

This will **keep airbnb009** (722 genuinely missing calendar days → probe fires → all-three-fork
repair → FAIL→PASS, reproducibly) AND **spare airbnb008** (no missing days → probe empty → no edit
→ stays PASS). Net target: **clean +1 → 33/48**, zero same-family bleed.

**Falsified if:** the probe fails to fire on airbnb009 (loses the proven flip — gating too tight),
OR still fires on airbnb008 / any other airbnb passer (bleed persists — gating ineffective), OR a
canary regresses. The open empirical question: can a local fired-precondition cleanly separate
"genuine coverage gap" from "coverage-shaped but correct," at trials:1?

## Pre-smoke Decision-Fork Probe

To be run at propose (flipped-task follow-up). The decision fork is now PRECONDITION-FIRING, not
the three forks (those are settled — h0046 proved the skeleton pins them 4/4). Probe whether the
fired-missing-day-probe wording makes the solver (a) FIRE the subtractive repair on airbnb009's
context (missing days present) and (b) NOT fire on airbnb008's context (predicate correct, bug is
a YAML quote). Clean-context subagents, no oracle leakage; classify fire/no-fire per cell.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
The solver README = h0043 + h0046's skeleton with the added fired-missing-day precondition gate,
nothing else.

**AC-2 — Every recorded score is paired with a clean strict audit** (captured>0 every cell).

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (h0043).**

**AC-4 — Committed-artifact reads (the decisive test):** airbnb009 = all three forks present
(drop predicate / keep `COUNT(*)` / no cross-join), run as **≥3 seed-perturbed repeats**; airbnb008
= model left byte-intact (probe did NOT fire — no predicate-drop, original YAML-only fix path).

**AC-5 — Regression panel holds, and it MUST carry airbnb008 + ≥2 other perturbable airbnb
passers** (the G8 lesson from h0046: airbnb008 was the unsampled sibling the smoke missed — it is
now a MANDATORY smoke cell), plus ≥1 passer per other family. A same-family regression is a NO-GO.

## Gatekeeper review

**Recommendation: APPROVE** (cycle 2 — REVISE addressed) — no FAILs. The coverage repair is now DOUBLE-GATED with TASK-INTENT as the FIRST test, so it stays one README idea (the scoped coverage repair) in one stage; leak-guard byte-intact, specs two-field, smoke carries the mandatory airbnb008 same-family canary + perturbable airbnb panel. WARNs on G7 and G12 only.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-12T02:40:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff h0043 → h0050` adds ONE block (55a56-114) entirely inside `## Stage: Implementation`; no other stage touched. `diff h0046 skeleton → h0050` confirms the only delta vs the proven skeleton is the double-gate framing + GATE (a) task-intent test + GATE (b) probe block — still one idea (the scoped coverage repair), now double-gated rather than runtime-only. |
| G2 leak-guard intact | PASS | Grep over the added lines 56-114 returns NO forbidden tokens (curl/wget/git clone/ls-remote/AUTO_*/solution__*/check_option/verifier/equality test/fetch/download). Parent leak-guard prose lines 9-32 byte-IDENTICAL to h0043. Probe explicitly "oracle-free — never a hidden test." |
| G3 spec two fields | PASS | `diff baseline.yaml → h0050.yaml` = only `experiment:` and `solver_workflow:`; `agent.kind: spacedock_solver` + `runtime: codex` preserved; trials unchanged (=1). |
| G4 smoke tasks-only | PASS | `diff full → smoke` adds only a `benchmark.tasks:` block; all 9 slugs `ade-bench-` prefixed; includes the named target airbnb009 + mandatory airbnb008 + perturbable airbnb004/005/006 + per-family canaries. |
| G5 both frozen | PASS | Both `…frozen.yaml` and `…smoke.frozen.yaml` exist; each carries `kind: spacedock_solver` + `runtime: codex` (lines 4-5). Full frozen `solver_workflow_content_hash: sha256:3a98d5cd…` matches the revised README (re-frozen after the GATE (a) change). |
| G6 resolver fidelity | PASS | Inserted text = the Falsifiable claim in spirit and now sharper for the captain's separation concern: GATE (a) intent ("apply ONLY if the instruction EXPLICITLY calls for completeness; else do NOT investigate or apply, leave byte-intact") THEN GATE (b) the FIRED oracle-free `dim except model` probe. Generative-but-gated against an independent local dimension + the task's own ask — not self-anchored re-run-your-own-model. Same Implementation stage, no scope creep. |
| G7 actionability/inert-risk | WARN | Worked-example SQL skeleton (PROBE + BEFORE/AFTER) preserved → clears the actionability bar; h0046 already pinned airbnb009 4/4 so inertness is not the risk. The live risk is now the TWO-gate separation power at trials:1 — GATE (a) depends on the solver correctly reading task intent (airbnb008's ask is a YAML/structure fix, not completeness → should not even reach the probe) and GATE (b) on the probe firing only on genuine gaps. Judge at smoke by committed artifact: airbnb008 MUST stay byte-intact. |
| G8 regression-canary coverage | PASS | Gated/scoped (double-gated: intent + fired probe) yet generative in reach; smoke carries the strong panel the h0046 bleed lesson demands — airbnb008 (MANDATORY same-family canary h0046 broke; must stay PASS) + airbnb004/005/006 (≥2 perturbable same-family passers) + asana002/ana-eng001/f1009/quickbooks002 (one passer per other family). intercom legitimately absent (no @baseline passer). All non-targets are confirmed h0043 PASS-set members. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — single subtractive edit gated on intent + one probe. |
| G10 self-correcting false-positive | N/A | Not a verify-and-fix-on-disagreement lever; the gates decide *whether to edit at all* against an independent local dimension and the task's own ask — they do not reconcile a re-derived figure and overwrite a correct path. Edit is subtractive-or-nothing. |
| G11 multi-model-target risk | N/A | `_artifacts/bug-type-taxonomy.md`: airbnb009 is single-model (airbnb007 is the multi-model trap, not a target here). Lever covers the one scored model. |
| G12 decision-fork probe quality | WARN | `## Pre-smoke Decision-Fork Probe` present, tests the right fork (FIRE on airbnb009 missing-days context vs NO-FIRE on airbnb008). Note: the captain has ALREADY executed a first fire/no-fire probe — its result (the runtime-only gate false-fired on airbnb008/005) is exactly what motivated GATE (a). The probe must be RE-RUN against the revised double-gated wording before smoke; provenance (agent/run count, prompt text, control-A) still to be recorded, and counts stay proxy-only — exploratory, not confirmatory. |

**For the captain:** Clean to advance to smoke — the REVISE is satisfied: intent-first double-gating directly targets the genuine-gap-vs-coverage-shaped separation failure that false-fired airbnb008/005, and it remains one idea in the Implementation stage with leak-guard byte-intact and the mandatory airbnb008 + perturbable-airbnb panel in the smoke. Two watch items: (G12) re-run the decision-fork probe against the NEW double-gated wording with provenance recorded, since the prior fire/no-fire probe tested the old runtime-only gate; (G7/G8) the whole bet is two-gate separation at trials:1 — credit the +1 only if the committed artifact shows airbnb009 with all three forks AND airbnb008 left byte-intact (no-fire on airbnb008 is the falsifier).

## Smoke result

**GO.** The scoped fix for the h0046 same-family bleed WORKED at the artifact level. The
intent-first double-gate flipped airbnb009 reproducibly (3/3 draws, all three forks,
byte-consistent) AND spared airbnb008 (model byte-intact — gate (a) task-intent did not pass),
with zero canary loss. Projected net **+1 → 33/48** at full, no bleed.

**Runs (all strict-audit clean, captured>0 every cell):**
- PANEL (9 cells) `runs/…h0050…/3fc58860c7b07ba2` — strict audit `{clean:9, coverage_missing:0, tainted:0}`; score stratified mean **1.0 (9/9 PASS)**.
- airbnb009-r2 (seed 42) `…-airbnb009-r2/9e7661f313166cc5` — `{clean:1, coverage_missing:0, tainted:0}`; PASS.
- airbnb009-r3 (seed 43) `…-airbnb009-r3/e59026184ca1c8db` — `{clean:1, coverage_missing:0, tainted:0}`; PASS.

| Task | @baseline (h0043) | Smoke | Role | Artifact verdict |
|------|------|-------|------|------------------|
| airbnb009 (panel) | ❌ FAIL | ✅ PASS | 🎯 target | all 3 forks in committed `mom_agg_reviews.sql`; scored model `mom_agg_review_date_range` PASS |
| airbnb009 r2 | ❌ FAIL | ✅ PASS | target repeat #2 | committed SQL byte-identical to panel draw |
| airbnb009 r3 | ❌ FAIL | ✅ PASS | target repeat #3 | committed SQL shows identical fork |
| airbnb008 | ✅ PASS | ✅ PASS | ✅ MANDATORY canary (h0046 broke it) | `mom_agg_reviews.sql` BYTE-INTACT (predicate kept); only `agg.yml` YAML-quote fixed |
| airbnb004 | ✅ PASS | ✅ PASS | perturbable airbnb canary | coverage probe NOT run; skeleton did not fire |
| airbnb005 | ✅ PASS | ✅ PASS | perturbable airbnb canary | coverage probe NOT run (false-fired 5/8 in runtime-only probe; gate (a) spared it) |
| airbnb006 | ✅ PASS | ✅ PASS | perturbable airbnb canary | coverage probe NOT run; skeleton did not fire |
| asana002 | ✅ PASS | ✅ PASS | canary (asana) | skeleton did not fire |
| ana-eng001 | ✅ PASS | ✅ PASS | canary (ana-eng) | skeleton did not fire |
| f1009 | ✅ PASS | ✅ PASS | canary (f1) | skeleton did not fire |
| quickbooks002 | ✅ PASS | ✅ PASS | canary (quickbooks) | skeleton did not fire |

**DECISIVE READS:**

*airbnb009 — all three forks, 3 draws byte-consistent.* Committed `models/agg/mom_agg_reviews.sql`
(panel / r2 / r3 identical):
(1) **narrowing predicate DROPPED** — `dates_cte` now `SELECT DATE_ACTUAL FROM dim_dates` with no
`WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE::DATE FROM review_cte)` (only the incremental
predicate kept, as designed); (2) **COUNT(*) byte-intact** — `COUNT(*) AS REVIEW_TOTALS`, not
rewritten to COUNT(col); (3) **no cross-join** — no `cats` CTE / no `cross join`; existing
`dates_cte LEFT JOIN review_cte … GROUP BY REVIEW_SENTIMENT, AGGREGATION_DATE` unchanged. Both
gates fired correctly: solver ran the coverage probe (gate b) — before `missing_dates=25434`
(dim 29220 vs model 3786), after-fix `missing_dates=0` (model 29220).

*airbnb008 — BYTE-INTACT (the h0046 bleed fixed).* Task ask was literally **"The project is
broken."** — NO completeness wording → **gate (a) did not pass**, the solver never ran the
coverage probe and never touched `mom_agg_reviews.sql` (its narrowing predicate is preserved).
The solver's own final summary: *"The final source check shows only the intended YAML source file
edit."* The real bug was fixed instead: `models/agg/agg.yml` had an unterminated quoted
`description` for `mom_agg_reviews.DATE_SENTIMENT_ID` (dbt YAML parse error at line 73); fix =
closed the string. This is exactly the 1-line YAML-quote bug h0046 mis-treated as a coverage gap.

*Canaries.* All 7 non-target passers held PASS; none ran the coverage probe (skeleton inert on
each). Notably airbnb005 — which false-fired 5/8 under the rejected runtime-only gate — did NOT
fire here: its task ask is not completeness, so gate (a) kept it out.

## Run result

## Behavioral analysis

The intent-first double-gate is the mechanism that converts h0046's artifact-correct-but-too-eager
skeleton into a clean +1. h0046 PROVED the three-fork skeleton pins airbnb009 (4/4); its defect was
firing on airbnb008 (whose predicate was already correct, real bug a YAML quote) and breaking
`AUTO_mom_agg_reviews_equality`. h0050 adds GATE (a) — task-intent — as the FIRST test, ahead of
the (unchanged) oracle-free coverage probe (gate b).

Why gate (a) was necessary and gate (b) alone was not: the captain's pre-smoke fire/no-fire probe
showed the runtime-only probe false-fired on airbnb008 (5/8) and airbnb005 (5/8), because the
narrowing predicate — hence "missing days" under `dim_dates EXCEPT output` — exists in EVERY airbnb
model. The probe cannot by itself distinguish "missing days = bug" (airbnb009, instruction asks for
completeness) from "missing days = correct/irrelevant" (airbnb008, instruction is "the project is
broken"). The probe cannot beat task intent. Gating on the instruction's explicit completeness ask
FIRST — and refusing to even investigate coverage otherwise — is what separated genuine-gap from
coverage-shaped-but-correct at trials:1. The committed artifacts confirm the separation held: on
airbnb009 the solver ran the probe (fired, missing_dates 25434→0) and dropped exactly the predicate;
on airbnb008/004/005/006 it never ran the probe at all.

This is the first genuine same-family-clean coverage flip in the airbnb009 line (the h0019/h0042
non-reproducibility wall was already broken by h0046's pinning; h0046's net was 0 from the bleed).
At trials:1 the artifact proof — not aggregate reward — carries the verdict: airbnb009's three forks
are present and byte-consistent across 3 independent draws, and airbnb008 is provably byte-intact.

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver (h0043) → h0050; take h0046's all-three-fork skeleton verbatim and add ONE thing — a FIRED MISSING-DAY/ROW PRECONDITION GATE; oracle-free probe (`dim except model`); fires only on genuine missing rows, else byte-intact; README diff vs h0043 shows exactly this one scoped block, leak-guard intact (AC-1).
  `@baseline` resolved to `runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea`; `diff h0043→h0050` = one block added under `## Stage: Implementation` (the gate + PROBE + the three-fork BEFORE/AFTER); `diff h0046→h0050` = ONLY the fired-probe gate added on top of the skeleton; leak-guard prose (README lines 1-32) byte-identical.
- DONE: Build the FULL spec (experiment: + solver_workflow: only) AND the smoke spec carrying airbnb009 + airbnb008 (MANDATORY) + ≥2 other perturbable airbnb passers + ≥1 passer per other family; prepare airbnb009 r2/r3 seed-perturbed frozen specs; freeze all with `rk freeze --allow-missing`.
  Full spec `diff baseline.yaml` = only `experiment:` + `solver_workflow:`. Smoke 9 tasks: airbnb009 (target) + airbnb008 (mandatory) + airbnb004/005/006 (perturbable airbnb) + asana002/ana-eng001/f1009/quickbooks002; smoke `diff` vs full = only `benchmark.tasks`. r2 (seed 42) + r3 (seed 43) single-cell airbnb009 specs created. All four frozen → `.frozen.yaml` present (full sealed_hash 14addda5…, solver content hash sha256:e4556b4c…).
- DONE: Run the gatekeeper subagent and write the `## Gatekeeper review` block (per-rule PASS/WARN/FAIL + APPROVE/REVISE/REJECT), emphasis G8/G10.
  Gatekeeper returned **APPROVE** — no FAILs; WARNs on G7 (gate separation-power, not inertness, is the live risk) and G12 (decision-fork probe to be run by FO, provenance incomplete). G8 PASS (airbnb008 mandatory + airbnb004/005/006 perturbable + per-family canaries). G10 N/A. Block written to the hypothesis file.

### Summary

h0050 forks the current @baseline (h0043, 32/48) and adds h0046's proven all-three-fork coverage-repair skeleton with exactly ONE new thing: a FIRED local missing-day/row precondition gate (oracle-free `dimension except model` probe) so the subtractive predicate-drop fires only on genuine coverage gaps (keep airbnb009: 722 missing days → fires; spare airbnb008: predicate already correct → empty → byte-intact). Specs are two-field clean; smoke carries the airbnb008 mandatory canary + 3 perturbable airbnb passers (the h0046 G8 lesson) + one passer per other family; r2/r3 seed-perturbed airbnb009 draws prepared for the AC-4 ≥3 repeats; all four specs frozen. Gatekeeper recommendation: APPROVE (WARN-only on G7/G12). No `rk run` launched — propose stops at freeze + gatekeeper; the FO presents the gate and may run the pre-smoke decision-fork probe.

## Stage Report: propose (cycle 2)

- DONE: REVISE — add a TASK-INTENT precondition to the gate (stays ONE idea: the scoped coverage repair, now double-gated). Coverage repair fires ONLY when BOTH hold: (a) the task instruction explicitly calls for row/date/key COMPLETENESS, else do NOT investigate or apply at all; AND (b) the existing oracle-free `dim except model` probe FIRES. Intent gate is the FIRST test. Everything else byte-intact; leak-guard intact; one README idea.
  `diff h0043→h0050` still ONE block under `## Stage: Implementation` (now 55a56-114): GATE (a) intent + GATE (b) probe + the three-fork BEFORE/AFTER; README lines 1-49 byte-identical to h0043 (leak-guard untouched). Fixes the captain's separation failure: the runtime-only probe false-fired on airbnb008 (5/8) and airbnb005 (5/8) because "missing days" exists in every airbnb model — the intent gate stops the repair from even being investigated on a non-completeness task.
- DONE: Re-freeze ALL specs whose solver README changed — full + smoke + airbnb009-r2 + airbnb009-r3 with `rk freeze --allow-missing`.
  All four re-frozen; full frozen `solver_workflow_content_hash` now `sha256:3a98d5cd…` (was `e4556b4c…`), `sealed_hash` `ad60c0f9…` — confirms the revised double-gated README is sealed.
- DONE: Re-run the gatekeeper on the revised README and refresh the `## Gatekeeper review` block.
  Re-gatekeeper returned **APPROVE** (cycle 2) — no FAILs; WARN-only on G7 (the live risk is now two-gate separation power at trials:1) and G12 (the prior fire/no-fire probe tested the old runtime-only gate; re-run against the revised wording before smoke). Stale block (content hash e4556b4c, no GATE (a)) replaced.

### Summary

REVISE addressed: the coverage repair is now DOUBLE-GATED — TASK-INTENT first (apply only when the instruction explicitly asks for completeness; otherwise do not investigate or apply, leave coverage-shaped models byte-intact), then the existing oracle-free fired coverage probe. This directly targets the captain's separation failure (the runtime-only probe false-fired on airbnb008/005 because the narrowing predicate exists in every airbnb model, so "missing days" cannot by itself mean "bug"). Still exactly one README idea in the Implementation stage, leak-guard byte-intact, specs two-field; all four specs re-frozen (new content hash sha256:3a98d5cd…); re-gatekeeper APPROVE (WARN-only G7/G12). No `rk run` launched — the FO re-runs the fire/no-fire probe against the revised wording (expect airbnb009 FIRE; airbnb008/004/005/006 NO_FIRE) before any smoke.

## Stage Report: smoke

- DONE: Strict audit each run-dir clean (tainted 0 / coverage_missing 0) + captured>0 every cell BEFORE score; `rk score` each.
  Panel `3fc58860c7b07ba2` strict `{clean:9, coverage_missing:0, tainted:0}`; r2 `9e7661f313166cc5` and r3 `e59026184ca1c8db` each `{clean:1,0,0}`. captured>0 confirmed (every cell's verifier/test-stdout = real PASS=N output, e.g. airbnb009 `actual_test_total=1, actual_pass=1`). `rk score` all three = stratified mean 1.0.
- DONE: airbnb009 (3 draws) committed `mom_agg_reviews.sql` shows all THREE forks (predicate dropped / COUNT(*) byte-intact / no cross-join); report byte-consistency.
  Panel/r2/r3 committed SQL byte-identical: `dates_cte` predicate dropped, `COUNT(*) AS REVIEW_TOTALS` intact, no cross-join. Probe fired (missing_dates 25434→0). All 3 draws consistent.
- DONE: airbnb008 committed `mom_agg_reviews.sql` BYTE-INTACT (gate (a) did not pass; YAML-quote fix applied instead) — confirm the intent gate spared it for real.
  Task ask = "The project is broken." (no completeness wording) → solver never ran the coverage probe, never touched `mom_agg_reviews.sql` (narrowing predicate preserved). Only `models/agg/agg.yml` changed (closed an unterminated quoted description). Solver summary: "only the intended YAML source file edit."
- DONE: airbnb004/005/006 + per-family canaries hold PASS; confirm the coverage skeleton did NOT fire.
  All 7 canaries PASS; 0 coverage-probe shell invocations on each (skeleton inert). airbnb005 (false-fired 5/8 under the rejected runtime-only gate) did NOT fire — gate (a) kept it out.

### Summary

GO. The intent-first double-gate flips airbnb009 reproducibly (3/3 byte-consistent, all three forks) AND spares airbnb008 byte-intact (gate (a) blocked the coverage repair on a non-completeness task), with zero canary loss — projected net +1 → 33/48 at full, no same-family bleed. This is the artifact-level fix for the exact h0046 defect (h0046: +1 airbnb009 / −1 airbnb008 = net 0). The verdict rests on committed-artifact proof at trials:1, not aggregate reward: airbnb009's three forks present across 3 independent draws; airbnb008's `mom_agg_reviews.sql` provably untouched.
