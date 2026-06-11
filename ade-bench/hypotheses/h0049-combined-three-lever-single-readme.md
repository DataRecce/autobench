---
id: h0049
title: Combined three-lever single README — stack the h0044 (standings max-points) + h0045 (feature-boundary removal/toggle) + h0046 (coverage-repair all-three-forks skeleton) levers verbatim on h0043 and test whether ONE README resolves all their target tasks without interference
status: hypothesis
kind: hypothesis
source: captain request 2026-06-11 — the three levers each passed smoke solo (h0044 6/6, h0045 7/7, h0046 airbnb009 3/3 byte-identical); verify whether a SINGLE solver README composing all three resolves every target task at once, or whether stacking interferes / bloats the README so a precondition mis-fires. Forks the current @baseline h0043 (32/48).
started:
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

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
