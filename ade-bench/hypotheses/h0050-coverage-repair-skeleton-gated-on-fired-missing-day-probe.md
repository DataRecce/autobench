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

## Stage Report: propose (cycle 2)

- DONE: REVISE — add a TASK-INTENT precondition to the gate (stays ONE idea: the scoped coverage repair, now double-gated). Coverage repair fires ONLY when BOTH hold: (a) the task instruction explicitly calls for row/date/key COMPLETENESS, else do NOT investigate or apply at all; AND (b) the existing oracle-free `dim except model` probe FIRES. Intent gate is the FIRST test. Everything else byte-intact; leak-guard intact; one README idea.
  `diff h0043→h0050` still ONE block under `## Stage: Implementation` (now 55a56-114): GATE (a) intent + GATE (b) probe + the three-fork BEFORE/AFTER; README lines 1-49 byte-identical to h0043 (leak-guard untouched). Fixes the captain's separation failure: the runtime-only probe false-fired on airbnb008 (5/8) and airbnb005 (5/8) because "missing days" exists in every airbnb model — the intent gate stops the repair from even being investigated on a non-completeness task.
- DONE: Re-freeze ALL specs whose solver README changed — full + smoke + airbnb009-r2 + airbnb009-r3 with `rk freeze --allow-missing`.
  All four re-frozen; full frozen `solver_workflow_content_hash` now `sha256:3a98d5cd…` (was `e4556b4c…`), `sealed_hash` `ad60c0f9…` — confirms the revised double-gated README is sealed.
- DONE: Re-run the gatekeeper on the revised README and refresh the `## Gatekeeper review` block.
  Re-gatekeeper returned **APPROVE** (cycle 2) — no FAILs; WARN-only on G7 (the live risk is now two-gate separation power at trials:1) and G12 (the prior fire/no-fire probe tested the old runtime-only gate; re-run against the revised wording before smoke). Stale block (content hash e4556b4c, no GATE (a)) replaced.

### Summary

REVISE addressed: the coverage repair is now DOUBLE-GATED — TASK-INTENT first (apply only when the instruction explicitly asks for completeness; otherwise do not investigate or apply, leave coverage-shaped models byte-intact), then the existing oracle-free fired coverage probe. This directly targets the captain's separation failure (the runtime-only probe false-fired on airbnb008/005 because the narrowing predicate exists in every airbnb model, so "missing days" cannot by itself mean "bug"). Still exactly one README idea in the Implementation stage, leak-guard byte-intact, specs two-field; all four specs re-frozen (new content hash sha256:3a98d5cd…); re-gatekeeper APPROVE (WARN-only G7/G12). No `rk run` launched — the FO re-runs the fire/no-fire probe against the revised wording (expect airbnb009 FIRE; airbnb008/004/005/006 NO_FIRE) before any smoke.
