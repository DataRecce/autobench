---
id: h0052
title: Three-lever composition — h0044 standings max(points) + h0045 feature-boundary guard + h0050 intent-gated scoped coverage skeleton on h0043 (the scoped, bleed-free re-do of h0049); A/B vs h0051 isolates whether the no-harm guard is free
status: smoke
kind: hypothesis
source: "Captain request 2026-06-12 alongside h0051. Same composition as h0049 (h0044+h0045+h0046) but with the UNSCOPED bleeding h0046 swapped for the intent-gated scoped h0050. Run as an A/B against h0051 (h0044+h0050 only): the delta isolates h0045's no-harm feature-boundary guard — it should contribute zero flips and zero interference (its targets qb002/qb004 already pass; full showed it flips nothing and its losses were pure off-construct variance). Tests whether stacking a third no-harm guard is free or adds bloat/interference."
started: 2026-06-12T09:38:44Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The scoped, bleed-free re-do of h0049. Three construct-gated levers, all individually verified:
- **h0044** — standings `max(points)` (verified +2: f1006 + f1006-hard, inert off-target).
- **h0045** — feature-boundary removal/toggle guard (verified no-harm: flips nothing, targets
  qb002/qb004 hold; its solo full net −4 was entirely off-construct variance, lever silent).
- **h0050** — intent-gated scoped coverage skeleton (verified: airbnb009 3/3, airbnb008 spared).

**Falsifiable claim (the single README change):** fork h0043 and add ALL THREE levers verbatim as
separate precondition-gated Implementation rules. Outcome should equal h0051 (h0044+h0050) PLUS
h0045 holding its targets with zero added flips and zero interference — i.e. the no-harm guard is
**free** under composition. Expected flips: f1006 + f1006-hard + airbnb009 (+3); holds: airbnb008,
qb002, qb004; canaries hold. **Falsified if** adding h0045 degrades h0051's result (interference /
bloat causing a precondition to mis-fire), or any lever loses its solo effect.

**The A/B with h0051 is the point:** h0051 = the two flip levers; h0052 = the same plus the no-harm
guard. Comparing their full results isolates h0045's marginal contribution (predicted: net zero —
neither helps nor harms). Best case both reach +3 → 35/48; if h0052 < h0051, the guard interferes.

Target datasets: f1006, f1006-hard, airbnb009 (flip); airbnb008, qb002, qb004 (hold).

## Pre-smoke Decision-Fork Probe

Skipped — all three constituent levers are individually smoke-verified at the artifact level, and
h0049 already proved construct-gated levers compose without interference. The only new variable vs
h0051 is the presence of h0045's guard, whose no-harm/no-flip behavior is established. No new probe
owed.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Combined README = h0043 + h0044 + h0045 + h0050 rules, each verbatim, nothing else.

**AC-2 — Every recorded score paired with a clean strict audit** (captured>0 every cell).

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (h0043), AND an
explicit A/B vs h0051's run-dir** (does the added guard change any cell?).

**AC-4 — Per-lever committed-artifact reads:** f1006 + f1006-hard = `max(points)`; airbnb009 =
three forks across ≥3 seed-perturbed repeats; airbnb008 = byte-intact; qb002/qb004 = narrow
feature-boundary edits (no broad rewrite); confirm h0045's guard fired only where appropriate.

**AC-5 — Regression panel holds; airbnb008 MANDATORY** + perturbable airbnb (004/005/006) + f1
canaries (f1005, f1005-medium) + qb003 + ≥1 passer per other family. Promote decision rests on the
run-dir net clearing h0043.

## Gatekeeper review

**Recommendation: APPROVE** — no FAILs. The three-lever composition is the single declared idea;
the README diff vs the fork parent h0043 is EXACTLY the three blocks (h0044 max-points, h0045
feature-boundary, h0050 double-gated coverage), each verbatim from its source solver, with the
leak-guard prose byte-identical; the A/B vs h0051 is exactly the h0045 block. Specs and frozen
files are clean.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-12T00:00:00Z.

Fork parent resolved: `source:` names h0043 and `@baseline` resolves to
`runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea` →
solver `solver_workflows/h0043-package-update-optional-resource-matrix` (agree).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff h0043 h0052` = three added blocks ALL under `## Stage: Implementation` (after L55 + after the package-matrix para); no other stage touched. The composition is the single idea (analogous to APPROVED h0049/h0051). Each block verbatim: h0044 max-points block IDENTICAL to source L64-73; h0045 feature-boundary block IDENTICAL to source L56-79; h0050 coverage block IDENTICAL (normalized extract, 58 lines, 0 diff). |
| G2 leak-guard intact | PASS | Header L1-50 byte-IDENTICAL to parent (no-fetch + dependency/package guardrails unchanged). Forbidden-token grep over the ADDED region (L56-165): CLEAN — no `AUTO_`/`solution__`/`check_option`/`verifier`/`equality test`/`expected output seed`/`curl`/`wget`/`git clone`/`drive-to-zero`/`published solution`. All token hits are in the unchanged leak-guard prose (L9-28). |
| G3 spec two fields | PASS | `diff baseline.yaml h0052.yaml` = only `experiment:` and `solver_workflow:`. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff full smoke` = single addition `23a24,39`, only a `benchmark.tasks:` block. All slugs `ade-bench-` prefixed. Includes every named flip target (f1006, f1006-hard, airbnb009) and every named hold (airbnb008, quickbooks002, quickbooks004). |
| G5 both frozen | PASS | Both `…frozen.yaml` (1743 B) and `…smoke.frozen.yaml` (2082 B) exist; both carry `kind: spacedock_solver` + `runtime: codex` (L4-5) and `trials: 1`. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim ("add ALL THREE levers verbatim as separate precondition-gated Implementation rules"). All three levers are generative-or-precondition-gated derivation rules (substitution `sum→max`; feature-boundary edit boundaries; subtractive coverage edit gated on intent+probe) — none is a self-anchored "re-run/verify your own output" instruction. A/B vs h0051 diff = EXACTLY the h0045 feature-boundary block, confirming h0052 = h0051 + h0045 only. |
| G7 actionability/inert-risk | PASS | h0044 = concrete mechanical substitution (`replace sum(points) with max(points)`). h0050 = carries a literal BEFORE/AFTER SQL worked-example skeleton (copyable, not abstract prose). h0045 = bounded edit-locality rule. None is abstract FROM/spine restructuring prose; not a build/deliverable-completion rule. All three individually artifact-verified at smoke per the body. |
| G8 regression-canary coverage | PASS | All three levers are PRECONDITION-GATED (h0044 fires only on `*_standings` sum(points); h0045 on remove/disable/toggle asks; h0050 double-gated on completeness intent AND a fired missing-key probe), not unconditionally generative. Nonetheless the smoke carries a full panel: airbnb008 MANDATORY same-family canary (h0046 broke it) + airbnb004/005/006 perturbable coverage-shaped + f1005/f1005-medium perturbable standings-shaped + quickbooks003 perturbable feature-boundary-shaped (the h0045 construct family) + quickbooks002/004 + asana002 + ana-eng001. ≥2 perturbable canaries in each family the levers can fire on. No intercom canary — intercom has no `@baseline` passer (all FAIL), so that family cannot supply one (correctly noted in the spec; not a defect). |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — three precondition-gated mechanical/edit-locality rules, no N-candidate generation-and-selection mechanism. |
| G10 self-correcting false-positive | N/A | None of the three is a "verify-a-figure-and-act-on-disagreement" reconcile lever. h0050's probe is a GATE on whether to make a subtractive edit (oracle-free anti-join against the local dimension), not a reconcile-then-replace of an authored figure; it is double-gated and check-don't-replace by construction (edit only fires when intent AND a missing-key probe both hold). h0044/h0045 are direct edits, not validate-and-fix. |
| G11 multi-model-target risk | WARN (advisory) | airbnb009 scored by single model `mom_agg_review_date_range` (taxonomy L36) — covers-all. f1006 listed in taxonomy with `AUTO_constructor_points_equality` (L42); h0044 already artifact-verified +2 on f1006 + f1006-hard, strong evidence the lever reaches the scored model. CAUTION: taxonomy L222 calls f1006 "a target whose pass/fail flickers on a model the lever does not touch" (h0012 lineage) — surface to captain: at smoke/credit time, re-enumerate f1006 / f1006-hard scored models from `verifier/test-stdout.txt` and confirm the `max(points)` artifact landed on every scored model before banking. Advisory only; does not block. |
| G12 decision-fork probe quality | N/A | Body explicitly states the Pre-smoke Decision-Fork Probe is skipped: all three constituent levers are individually smoke-verified at the artifact level and h0049 already proved construct-gated composition; no new fork variable vs h0051 beyond h0045's established no-harm guard. Valid skip per guideline (no new visible local fork). |

**For the captain:** Clean APPROVE — verbatim three-block composition, leak-guard byte-intact, A/B vs
h0051 isolates exactly the h0045 block, full regression panel present. Two advisory notes: (1) G11 —
f1006/f1006-hard carry a historical multi-model flicker hint (taxonomy L222); at smoke confirm the
`max(points)` artifact landed on every scored model of those targets before crediting, not just the
aggregate verdict. (2) The whole point is the A/B delta vs h0051's run-dir — judge h0045's marginal
contribution by per-cell artifact comparison (predicted net zero), not just the aggregate.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver (h0043) → h0052; add ALL THREE verified levers VERBATIM as separate precondition-gated Implementation rules
  Forked from h0051 (which already = h0043 + h0044 max-points + h0050 coverage, confirmed by `diff h0043 h0051`); added the h0045 feature-boundary block verbatim. `diff h0043 h0052` = exactly the three gated blocks (h0045 + h0050 + h0044), all under `## Stage: Implementation`, leak-guard byte-intact (AC-1). `diff h0051 h0052` = exactly the h0045 block.
- DONE: Build FULL spec + smoke spec (same panel as h0051 + quickbooks003 perturbable qb canary) + airbnb009 r2/r3 seed-perturbed frozen specs; freeze all with rk freeze --allow-missing
  Full spec diff vs baseline = only `experiment:` + `solver_workflow:`. Smoke panel: flip f1006/f1006-hard/airbnb009; hold airbnb008(MANDATORY)/qb002/qb004; perturbable airbnb004/005/006 + f1005/f1005-medium + quickbooks003 + asana002/ana-eng001. r2 seed=42, r3 seed=43. All four froze (wrote *.frozen.yaml).
- DONE: Run the gatekeeper and write ## Gatekeeper review (per-rule PASS/WARN/FAIL + APPROVE/REVISE/REJECT); G8/G10 canary coverage required
  Gatekeeper recommendation: APPROVE, no FAILs across G1–G12. G8 PASS (precondition-gated levers + full panel, ≥2 perturbable canaries per fireable family, intercom correctly omitted). G11 WARN (advisory): re-enumerate f1006/f1006-hard scored models at smoke before crediting. G9/G10/G12 N/A.

### Summary

h0052 is the SCOPED, bleed-free re-do of h0049: forked the current @baseline (h0043) and composed three individually-verified, precondition-gated levers verbatim — h0044 same-grain max(points), h0045 feature-boundary guard, h0050 double-gated intent-then-probe coverage skeleton. Built as an A/B vs h0051 (= h0044+h0050 only): the h0052−h0051 README diff is exactly the h0045 block, so the full-run delta isolates whether the no-harm feature-boundary guard is free under composition (predicted net zero). All four specs frozen; @baseline rewards resolved for the smoke table (3 targets FAIL, 11 canaries/holds PASS); gatekeeper APPROVE with one advisory G11 multi-model note.
