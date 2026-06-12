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

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
