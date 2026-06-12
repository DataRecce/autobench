---
id: h0050
title: Scoped coverage-repair skeleton — gate the all-three-fork predicate-drop on a FIRED local missing-day probe so it fires ONLY on genuine coverage gaps (keep airbnb009, spare airbnb008)
status: propose
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

**Recommendation: APPROVE** — no FAILs; the lone added idea is the fired-missing-day precondition gate cleanly scoped under Implementation, leak-guard byte-intact, specs two-field, and the smoke carries the mandatory airbnb008 same-family canary plus the perturbable-airbnb panel the h0046 bleed lesson demands. WARNs on G7 and G12 only.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-12T02:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff h0043 → h0050` adds ONE block (55a56-100) entirely inside `## Stage: Implementation`; no other stage touched. `diff h0046 → h0050` confirms the only delta vs the skeleton is the FIRED-probe gate (the precondition prose + the `dim except model` PROBE block + the "only when probe FIRED" guards). |
| G2 leak-guard intact | PASS | Forbidden-token grep hits (`curl/wget/git clone/git ls-remote/verifier`) all fall in the *preserved* parent leak-guard paragraphs (lines 9-26), byte-identical to h0043; the added block (56-99) contains no `AUTO_*`/`solution__*`/`check_option_*`/"equality test"/fetch instruction. Probe is explicitly "oracle-free … never a hidden test." |
| G3 spec two fields | PASS | `diff baseline.yaml → h0050.yaml` = only `experiment:` and `solver_workflow:`; `agent.kind: spacedock_solver` + `runtime: codex` preserved; `trials: 1`. |
| G4 smoke tasks-only | PASS | `diff full → smoke` adds only a `benchmark.tasks:` block; all slugs `ade-bench-` prefixed; includes the named target airbnb009 + the mandatory airbnb008 + per-family canaries. |
| G5 both frozen | PASS | Both `…frozen.yaml` and `…smoke.frozen.yaml` exist; each carries `kind: spacedock_solver` + `runtime: codex` (lines 4-5). |
| G6 resolver fidelity | PASS | Inserted text = the Falsifiable claim verbatim in spirit: same Implementation stage, the one idea (fire the subtractive predicate-drop ONLY when a local `dim except model` probe returns ≥1 missing key; else leave byte-intact). Generative-but-gated against an independent local dimension — not self-anchored re-run-your-own-model. |
| G7 actionability/inert-risk | WARN | Worked-example SQL skeleton (PROBE + BEFORE/AFTER), not abstract prose → clears the actionability bar; h0046 already proved the skeleton pins airbnb009 4/4, so inertness is not the risk. The live risk is the *gate's separation power* (can a trials:1 probe cleanly distinguish genuine gap vs coverage-shaped-but-correct) — judge at smoke by committed artifact on airbnb008 (must stay byte-intact). |
| G8 regression-canary coverage | PASS | Instruction is gated/scoped (fires only on a FIRED probe) yet generative in reach; smoke carries the strong panel: airbnb008 (MANDATORY same-family canary h0046 broke, must stay PASS) + airbnb004/005/006 (≥2 perturbable same-family passers) + asana002/ana-eng001/f1009/quickbooks002 (one passer per other family). intercom legitimately absent (no @baseline passer). All non-targets confirmed h0043 passers. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — single subtractive edit gated on one probe. |
| G10 self-correcting false-positive | N/A | Not a verify-and-fix-on-disagreement lever; the probe gates *whether to edit at all* against an independent local dimension, it does not reconcile a re-derived figure and overwrite. Closest-adjacent but the reconcile target is a separate source (the `dim_*`), edit is subtractive-or-nothing, not replace-a-correct-path. |
| G11 multi-model-target risk | N/A | `_artifacts/bug-type-taxonomy.md` line 36: airbnb009 is scored by a single model (`mom_agg_review_date_range`/`mom_agg_reviews`). The multi-model trap (line 43) is airbnb007, not a target here. Lever covers the one scored model. |
| G12 decision-fork probe quality | WARN | `## Pre-smoke Decision-Fork Probe` present, tests the right fork (FIRE on airbnb009 missing-days context vs NO-FIRE on airbnb008 YAML-quote context), clean-context/no-oracle, classify fire/no-fire. But provenance incomplete (no agent/run count, prompt text, control-A) and it is stated as TO-BE-RUN-AT-PROPOSE, not yet executed — treat its result as cost-control/exploratory, not confirmatory. |

**For the captain:** Clean to advance to smoke — no integrity FAILs, and the smoke panel finally carries the airbnb008 mandatory canary + perturbable airbnb siblings that h0046 lacked. Two things to watch: (G12) the decision-fork probe must actually be run by the FO at propose with provenance recorded before smoke, and its counts stay proxy-only; (G7/G8) the whole bet is the gate's separation power at trials:1 — credit the +1 only if the committed artifact shows airbnb009 with all three forks AND airbnb008 left byte-intact (probe did not fire), since a no-fire-on-airbnb008 is the falsifier for the gate.

## Smoke result

## Run result

## Behavioral analysis

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
