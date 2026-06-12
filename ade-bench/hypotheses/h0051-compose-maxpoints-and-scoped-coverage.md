---
id: h0051
title: Compose the two VERIFIED bleed-free levers — h0044 standings max(points) + h0050 intent-gated scoped coverage skeleton — in one README on h0043 to bank f1006 + f1006-hard + airbnb009 in a single run
status: propose
kind: hypothesis
source: "h0044 + h0050 full/smoke analyses (2026-06-12). h0044's max(points) lever is artifact-correct and provably inert off-target (real +2 on f1006/f1006-hard; its full net -1 was off-construct variance, NOT lever damage — so it cannot promote alone but the lever is verified-good). h0050's intent-gated scoped coverage skeleton is smoke-GO (airbnb009 3/3 + airbnb008 byte-intact, no same-family bleed). Both are bleed-free on disjoint constructs; h0049 already proved construct-gated levers compose. Composing them lands +3 real flips in one run-dir to clear the ~±4 trials:1 variance band. Supersedes h0049 (which used the UNSCOPED h0046 that bleeds airbnb008). Captain-approved filing 2026-06-12."
started: 2026-06-12T09:29:05Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Two individually-verified, bleed-free levers on disjoint constructs:
- **h0044** — standings/season totals: same-grain `max(points)`, reject final-row variants. Full
  run flipped f1006 AND f1006-hard on artifact-proven `max(points)`; provably inert on every
  non-standings task (its net −1 was off-construct single-trial variance, not lever damage).
- **h0050** — coverage repair DOUBLE-GATED on (a) task-intent explicitly asking row/date
  completeness AND (b) a fired oracle-free missing-day probe. Smoke-GO: airbnb009 flipped 3/3
  byte-consistent (all three forks), airbnb008 left byte-intact (intent gate spared it), zero
  canary loss.

**Falsifiable claim (the single README change):** fork the current `@baseline` (h0043) solver and
add BOTH levers **verbatim as separate precondition-gated Implementation rules** — nothing else. A
single composed README banks all three real flips at once with no interference and no bleed:
- f1006 + f1006-hard flip via same-grain `max(points)`;
- airbnb009 flips via the three-fork coverage repair (intent+probe gated);
- airbnb008 stays PASS (intent gate blocks the coverage repair on its non-completeness task);
- every canary holds.

**Why this can promote when h0044/h0046/h0050 alone could not:** each alone netted ≤0 because a
single real flip (or +2) was swamped by ~±4 off-construct variance, OR (h0046) bled a sibling.
Stacking the two verified bleed-free levers puts **+3 artifact-real flips** in ONE run-dir — enough
to clear the variance band and produce a run scoring **>32/48 (target 35/48)**, a promotable
baseline. **Falsified if** composition degrades any lever vs its solo result (interference), or any
canary/passer regresses beyond off-construct variance, or the run-dir nets ≤ h0043.

Target datasets: f1006, f1006-hard, airbnb009 (flip targets, all FAIL at h0043); airbnb008 +
qb002/qb004 (hold targets).

## Pre-smoke Decision-Fork Probe

Skipped — both levers are already individually smoke-verified at the artifact level (h0044 6/6
incl. f1006/f1006-hard max(points); h0050 airbnb009 3/3 + airbnb008 byte-intact + a 0/32-passer-
false-fire fire/no-fire probe on the intent gate). The only new question is composition/interference,
which h0049 already answered affirmatively for construct-gated levers and which the combined smoke
re-confirms. No new probe owed.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Combined README = h0043 + h0044's max(points) rule + h0050's intent-gated scoped coverage rule,
each verbatim, nothing else.

**AC-2 — Every recorded score paired with a clean strict audit** (captured>0 every cell).

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (h0043).**

**AC-4 — Per-lever committed-artifact reads:** f1006 + f1006-hard = same-grain `max(points)` (no
latest-row/QUALIFY); airbnb009 = all three forks across **≥3 seed-perturbed repeats**; airbnb008 =
`mom_agg_reviews.sql` BYTE-INTACT (intent gate did not fire).

**AC-5 — Regression panel holds; airbnb008 MANDATORY** + ≥2 perturbable airbnb (004/005/006) + f1
perturbable canaries (f1005, f1005-medium) + ≥1 passer per other family. A same-family or
lever-attributable regression is a NO-GO; off-construct single-trial variance is classified, not
auto-fatal, but the promote decision rests on the run-dir net clearing h0043.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
