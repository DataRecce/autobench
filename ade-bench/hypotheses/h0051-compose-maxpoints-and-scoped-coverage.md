---
id: h0051
title: Compose the two VERIFIED bleed-free levers — h0044 standings max(points) + h0050 intent-gated scoped coverage skeleton — in one README on h0043 to bank f1006 + f1006-hard + airbnb009 in a single run
status: smoke
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

**Recommendation: APPROVE** — sanctioned 2-lever composition; the README diff is exactly the two individually-verified, precondition-gated blocks (h0050 coverage + h0044 max-points), both byte-matching their source levers, in one Implementation stage; no FAILs, all WARN-only rules clear.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-12T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs h0043 touches only `## Stage: Implementation` (hunks `55a56,114` = h0050 double-gated coverage block; `71a131,141` = h0044 max-points block). The package-update block (lines 122-130) is preserved byte-intact; no Validation/leak-guard prose changed. Falsifiable claim names BOTH levers as the single composed change ("verbatim as separate precondition-gated Implementation rules — nothing else"). Sanctioned 2-lever composition, not scope creep; no third idea. |
| G2 leak-guard intact | PASS | Grep of all added (`>`) lines for AUTO_/solution__/check_option/verifier/equality test/expected output/drive-to-zero/curl/wget/git clone/git ls-remote/download/web lookup/published-solution → NONE FOUND. The probe is oracle-free (`select … except select …` against a local `dim_*`). Leak-guard + dependency paragraphs unchanged from h0043. |
| G3 spec two fields | PASS | `diff baseline.yaml h0051.yaml` shows only `experiment:` and `solver_workflow:` changed. `agent.kind: spacedock_solver`, `runtime: codex` preserved; `trials: 1`. |
| G4 smoke tasks-only | PASS | `diff h0051.yaml h0051.smoke.yaml` adds only a `benchmark.tasks:` block. All three named flip targets present and `ade-bench-` prefixed: f1006, f1006-hard, airbnb009. Regression sentinels included (airbnb008 mandatory + airbnb004/005/006, f1005/f1005-medium, qb002/004, asana002, ana-eng001). No other field differs. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1725B) and `…smoke.frozen.yaml` (2036B) exist; each carries `kind: spacedock_solver` + `runtime: codex` (lines 4-5). |
| G6 resolver fidelity | PASS | Coverage block (README 56-114) byte-matches the `>` lines of `diff h0043 h0050`; max-points block (README 131-141) byte-matches the `>` lines of `diff h0043 h0044`. Both generative-or-gated (each fires only on a fired precondition), not self-anchored re-run-your-own-model. Matches the claim's "verbatim" promise exactly. |
| G7 actionability/inert-risk | PASS | Coverage lever carries a literal BEFORE→AFTER SQL skeleton + an oracle-free probe (copyable, not abstract-structural). Max-points lever is a concrete mechanical substitution (`sum(points)`→`max(points)`, same grain). Both are the PASS form, not "restructure FROM/spine" abstract prose. Note: both levers are individually smoke-verified at the artifact level, lowering inert-risk further. |
| G8 regression-canary coverage | N/A (PASS) | Both instructions are GATED, not generative: coverage = double-gated (task-intent completeness AND a fired missing-day probe); max-points = gated on "season/entity totals from *_standings tables" + "task says points too high and model sums standings points." → N/A. The smoke panel is nonetheless rich: airbnb008 mandatory same-family canary (h0046 broke it; intent gate must spare it) + airbnb004/005/006 (≥2 perturbable coverage-shaped airbnb) + f1005/f1005-medium (≥2 perturbable standings-shaped f1) + qb002/004 + asana002 + ana-eng001. Intercom correctly excluded (no @baseline passer). |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — two direct gated Implementation rules. |
| G10 self-correcting false-positive | PASS | Coverage lever is fix-on-disagreement but (a) double-GATED to intent+fired-probe (not generative); (b) reconciles against a SEPARATELY-SOURCED signal (local `dim_*` dimension keys via `except`), not a re-derived CTE of the model's own logic; (c) check-don't-replace — deletes the one narrowing predicate, leaves aggregate/join/GROUP BY byte-intact (explicitly forbids COUNT(*)→COUNT(col) and cross-join rewrites). Max-points is a gated mechanical substitution, not a generative reconcile, and forbids switching to latest-row/rank/QUALIFY unless local evidence proves max wrong. No FAIL axis. |
| G11 multi-model-target risk | N/A (PASS) | Per `_artifacts/bug-type-taxonomy.md`: f1006 scored by single `AUTO_constructor_points_equality` (L42); airbnb009 scored by single `mom_agg_review_date_range` (L36); the multi-model trap names ONLY airbnb007, which is not a target here. f1006-hard sits in the same single-scored-model f1 constructor-points family. All flip targets single-model → N/A. |
| G12 decision-fork probe quality | N/A (PASS) | `## Pre-smoke Decision-Fork Probe` states the probe was skipped because both levers are already individually smoke-verified at the artifact level (h0044 6/6 incl. f1006/f1006-hard; h0050 airbnb009 3/3 + airbnb008 byte-intact + 0/32-passer false-fire fire/no-fire probe), and the only new question is composition/interference, which h0049 answered affirmatively for construct-gated levers. Adequate skip-rationale — N/A with explicit reason. |

**For the captain:** No FAILs — clean APPROVE. The integrity rules (G1/G2/G3/G6) all PASS: the diff is exactly the two verified gated blocks byte-matching their sources, in one stage, no leak. Both levers are gated (G8/G10 N/A→PASS) and both flip targets are single-model (G11 N/A), so there is no variance-on-unaddressed-model trap. The only thing to confirm at smoke is the composition claim itself: that the two gates stay mutually disjoint (coverage gate does NOT fire on the f1 standings tasks, max-points gate does NOT fire on airbnb009), airbnb008 stays byte-intact, and the run-dir net clears h0043 (≥32/48; needs the +3 to survive ±4 single-trial variance, per the standing single-trial caution).

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver (h0043) → h0051; add BOTH verified levers VERBATIM as separate precondition-gated Implementation rules; NO integration prose; README diff vs h0043 = exactly those two gated blocks, leak-guard intact (AC-1).
  `solver_workflows/h0051-compose-maxpoints-and-scoped-coverage/README.md`; `diff` vs h0043 = exactly two pure-addition hunks: `55a56,114` (h0050 double-gated coverage) + `71a131,141` (h0044 max-points). h0043 package block + leak-guard (lines 1-32) byte-intact. Coverage block byte-matches `diff h0043 h0050`; max-points content byte-matches `diff h0043 h0044`.
- DONE: Build the FULL spec (cp baseline; set ONLY experiment + solver_workflow) AND the smoke spec (3 flip targets + airbnb008 mandatory + qb002/qb004 holds + perturbable airbnb004/005/006 + f1005/f1005-medium + asana002 + ana-eng001). Prepare airbnb009 r2/r3 seed-perturbed frozen specs (≥3 airbnb009 draws). Freeze all with rk freeze --allow-missing.
  `diff baseline.yaml h0051.yaml` = only experiment: + solver_workflow:. `diff h0051.yaml h0051.smoke.yaml` = only benchmark.tasks (13 tasks). r2 seed=42, r3 seed=43 (single-task airbnb009). All 4 froze: `h0051-*.frozen.yaml` + `.smoke.frozen.yaml` + `.airbnb009-r2/r3.frozen.yaml`.
- DONE: Run the gatekeeper subagent and write the ## Gatekeeper review block (per-rule PASS/WARN/FAIL + APPROVE/REVISE/REJECT). G8/G10: airbnb008 mandatory + perturbable airbnb + f1 canaries are required.
  `## Gatekeeper review` block written: **APPROVE**, no FAILs/no WARNs. G8 N/A (both levers gated), G10 PASS (coverage reconciles vs separately-sourced dim, check-don't-replace), G11 N/A (both flip targets single-model). Panel: airbnb008 mandatory + 004/005/006 + f1005/f1005-medium present.

### Summary

Composed h0044's same-grain `max(points)` standings guard and h0050's double-gated (intent + fired-probe) scoped coverage skeleton onto the current @baseline (h0043), each added verbatim as a separate precondition-gated Implementation rule — no integration prose, no third knob, leak-guard intact. @baseline rewards resolved from h0043 run-dir 7390e6adf44ba5ea: f1006/f1006-hard/airbnb009 all FAIL (flip targets); airbnb008/004/005/006, f1005/f1005-medium, qb002/004, asana002, ana-eng001 all PASS (canaries/holds). Built + froze the FULL spec (two-field diff), the 13-task smoke spec (tasks-only diff), and two seed-perturbed airbnb009 single-task specs (r2 seed=42, r3 seed=43) for the ≥3-draw AC-4 requirement. Gatekeeper recommends APPROVE with zero FAILs/WARNs; the only smoke-time watch is gate disjointness, airbnb008 byte-intact, and the run-dir net clearing h0043. Propose stops here — no rk run launched; the FO presents the gate.
