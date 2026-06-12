---
id: h0052
title: Three-lever composition — h0044 standings max(points) + h0045 feature-boundary guard + h0050 intent-gated scoped coverage skeleton on h0043 (the scoped, bleed-free re-do of h0049); A/B vs h0051 isolates whether the no-harm guard is free
status: propose
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

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
