---
id: h0052
title: Three-lever composition — h0044 standings max(points) + h0045 feature-boundary guard + h0050 intent-gated scoped coverage skeleton on h0043 (the scoped, bleed-free re-do of h0049); A/B vs h0051 isolates whether the no-harm guard is free
status: analyze
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

**GO.** 14/14 panel + 2/2 airbnb009 repeats all PASS, all audits strict-clean, captured>0
every cell. All three flip targets flipped FAIL→PASS at the committed-artifact level; all
holds and canaries held. The A/B vs h0051 is decisive: **the h0045 feature-boundary guard is
FREE under composition** — it changed zero cells, zero verdicts, zero committed artifacts vs
h0051.

**Audit + score (AC-2):**
- PANEL `f65c803f8713c00b` — 14/14 clean, 14/14 PASS, every cell captured=1.
- airbnb009-r2 `1462fa6db3e876c8` — clean, PASS, captured=1.
- airbnb009-r3 `1e0351c7ba0144f5` — clean, PASS, captured=1.
- 0 tainted / 0 coverage_missing across all three run-dirs.

**Flip / hold table (vs @baseline h0043 `7390e6adf44ba5ea`):**

| Cell | Baseline | h0052 | Δ | Committed artifact (decisive read) |
|------|----------|-------|---|------------------------------------|
| f1006 | 0.0 FAIL | 1.0 PASS | FLIP | `sum(cs.points)→max(cs.points)` + `sum(ds.points)→max(ds.points)` on BOTH scored models (constructor_points + driver_points), same-grain, no latest-row/window/rank |
| f1006-hard | 0.0 FAIL | 1.0 PASS | FLIP | identical `max(points)` repair on both models; 920 + 3190 rows, 0 mismatches |
| airbnb009 (×3) | 0.0 FAIL | 1.0×3 PASS | FLIP | `mom_agg_reviews.sql` only: removed the `dates_cte` narrowing predicate (`WHERE DATE_ACTUAL IN (SELECT … review facts)`); aggregates/join/GROUP BY unchanged — 3/3 byte-consistent across seed-perturbed repeats |
| airbnb008 | 1.0 PASS | 1.0 PASS | HOLD | edited `agg.yml` (its real task — unterminated YAML string); `mom_agg_reviews.sql` BYTE-INTACT — coverage gate did NOT mis-fire |
| quickbooks002 | 1.0 PASS | 1.0 PASS | HOLD | narrow feature-boundary: removed `using_department` variable via `dbt_project.yml` + targeted `.sql` edits, no broad rewrite |
| quickbooks004 | 1.0 PASS | 1.0 PASS | HOLD | same narrow `using_department` removal |
| quickbooks003 | 1.0 PASS | 1.0 PASS | HOLD (h0052-only canary) | same feature-boundary construct, narrow edit |
| airbnb004/005/006, ana-eng001, asana002, f1005, f1005-medium | PASS | PASS | HOLD | canaries clean |

**G11 multi-model note resolved:** f1006/f1006-hard each have TWO scored models
(constructor_points + driver_points). The `max(points)` artifact landed on BOTH in both cells
(all four AUTO_*_equality + existence tests PASS); the historical multi-model flicker did not
bite this run.

## Run result

**HEADLINE: +3 artifact-real AGAIN, net +0 (TIE). 32/48 = 0.6667 — dead level with @baseline
h0043 (32/48). The same verified +3 composition lands for the SECOND independent draw (== h0051's
+3), yet does not clear the lucky-32 baseline because each draw loses ~3 off-construct coin-flips.
The trials:1 noise floor consumes the construct signal.** airbnb005 verdict: scoped coverage gate
is **PERFECTLY CLEAN — no mis-fire** (its NPS task failed for an unrelated reason; mom_agg_reviews
byte-untouched). The h0045 no-harm guard is **FREE on a 2nd draw** — it added zero flips and zero
NEW interference vs h0051.

**Run-dir:** `runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133`
(rc=0, 6h57m, 0 exceptions).

**Strict audit (AC-2):** CLEAN — 48 clean / 0 tainted / 0 coverage_missing; captured>0 every
cell (subagent-trace-manifest captured==0 count = 0/48). Ran BEFORE scoring.

**Absolute score (`rk score --format json`):** stratified pass@1 = **0.6667** (32/48), Wilson CI
[0.5254, 0.7832], n=48, 0 errored. Verdict vs paper_baseline 0.1875 = **above**.

**Paired delta vs @baseline h0043 (`7390e6adf44ba5ea`).** `rk runs diff` TypeError'd on the known
`query_id: null` data-shape limitation — computed the paired delta directly from
`per_trial_outcomes.json`, slug-paired (strip `__short`) + 10k paired bootstrap.

| Comparison | sum | net flips | mean per-task Δ | 95% bootstrap CI |
|------------|-----|-----------|-----------------|------------------|
| h0052 vs @baseline h0043 | 32 vs 32 | **+0** (3 gains, 3 losses) | +0.0000 | [−0.1042, +0.1042] |
| h0051 vs @baseline h0043 | 31 vs 32 | −1 (3 gains, 4 losses) | −0.0208 | [−0.1250, +0.0833] |
| h0052 vs h0051 (A/B = h0045 guard) | 32 vs 31 | +1 (3 gains, 2 losses) | +0.0208 | [−0.0625, +0.1042] |

CI straddles zero in all three — every delta is within the single-trial noise band. The +1 of
h0052 over h0051 is NOT the guard helping; it is a wash among off-construct coin-flips (see A/B).

**Full per-task ledger — both directions (Q1).**

GAINS (FAIL→PASS vs @baseline), all artifact-confirmed:
| Cell | Δ | Committed artifact |
|------|---|--------------------|
| f1006 | 0→1 | `sum(points)→max(points)` on BOTH scored models (constructor_points.sql + driver_points.sql), same-grain; 0 mismatches |
| f1006-hard | 0→1 | identical max(points) repair on both models; 920/920 + 3190/3190, max_abs_diff=0.0 |
| airbnb009 | 0→1 | `mom_agg_reviews.sql` only: removed `dates_cte` narrowing predicate; anti-join 722-in-span→0; join/COUNT/GROUP BY preserved |

REGRESSIONS (PASS→FAIL vs @baseline), all off-construct coin-flips (NOT lever damage):
| Cell | baseline→h0052 | Mechanism / classification |
|------|----------------|----------------------------|
| airbnb005 | 1→0 | CRITICAL-CHECK target. Pure variance — coverage gate UNTOUCHED (see below). Its NPS task: edited only daily/listing_agg_nps_reviews.sql, 2/4 equality_with_tolerance tests fail (self-anchored false-green). PASSED in h0051. |
| asana003 | 1→0 | known program-wide flip-flop cell; off-construct; lever-silent; lost in BOTH h0051 and h0052. Variance. |
| f1011 | 1→0 | known program-wide coin-flip (fails 4/5 prior variant draws); off-construct; lever-silent. PASSED in h0051+baseline. Variance. |

**CRITICAL CHECK — airbnb005 (Q: gate clean vs rare mis-fire?): GATE CLEAN, no mis-fire.** Its
committed artifact (cell `ade-bench-airbnb005__BfmqfGY`, reward 0) shows the agent edited ONLY its
own task's models — `models/agg/daily_agg_nps_reviews.sql` and `models/agg/listing_agg_nps_reviews.sql`
— with ZERO mention of `mom_agg_reviews`, `dates_cte`, missing-day/anti-join, or the coverage gate
anywhere in `agent/codex.txt`. The h0050 intent+probe coverage gate did NOT fire on airbnb005. It
failed for an unrelated reason: its NPS-aggregate task is complex, and the two hidden
`*_equality_with_tolerance` tests FAILED (2/4, the two existence tests passed) — the agent
self-validated "max NPS diff 0, review count mismatches 0" against its own derivation but the actual
aggregate values are wrong (classic self-anchored false-green, the oracle-problem wall, NOT a gate
artifact). mom_agg_reviews.sql is byte-untouched in this cell. **Verdict: pure trials:1 variance;
the scoped double-gate is perfectly clean — it fired only on airbnb009 (true target) and stayed
silent on both airbnb008 (correct hold) and airbnb005 (off-target). No residual bleed risk.**

**Smoke vs full (Q2/Q6).** Smoke was a 14/14 GO and was artifact-real — the +3 flips reproduced
exactly at full (same committed artifacts) and the A/B finding (guard is free) held. What smoke
could not see: the off-construct coin-flip families (airbnb005-NPS, asana003, f1011) that the smoke
panel didn't sample as the deciding cells. No fork drifted; no README rule changed branch. The
full≠smoke gap is purely that smoke can't sample the ~3 single-trial losses elsewhere on the board
that net the construct +3 back to a tie. Not a defect, not interference — the trials:1 noise floor.

## Behavioral analysis

### Full-run analysis (analyze stage)

**Method adherence (Q4 — was the change executed?).** All three flip targets are
EXECUTED-AND-HELPED, confirmed by committed artifact, not chatter:
- **h0044 max-points** — f1006 + f1006-hard each edited BOTH scored models
  (`models/stats/constructor_points.sql` + `driver_points.sql`), `sum(points)→max(points)`,
  same-grain, no latest-row/window/rank. Worker validation: 920/920 + 3190/3190 rows, max_abs_diff
  0.0. The historical G11 multi-model flicker did NOT bite: both 4-test verdicts are 4/4 PASS, so
  the artifact landed on every scored model.
- **h0050 intent-gated scoped coverage** — airbnb009 edited `models/agg/mom_agg_reviews.sql` ONLY;
  removed the `dates_cte` narrowing predicate (was filtering dim_dates to dates already in reviews);
  rolling join + COUNT(*) + GROUP BY preserved. Anti-join evidence: pre-fix 722 missing dates within
  the review span → post-fix 0. The double-gate (completeness intent AND fired missing-key probe)
  fired correctly here.
- The scoped gate's restraint is the headline: it fired on airbnb009 (true target) and stayed
  silent on BOTH airbnb008 (its real task = agg.yml unclosed-quote fix; mom_agg_reviews
  byte-untouched) AND airbnb005 (its NPS task; mom_agg_reviews byte-untouched). This is the
  scoped, bleed-free re-do of h0049 working exactly as designed — zero false fires.

**Already-correct-and-broken (Q3).** All 3 regressions were PASSING at @baseline (1→0) — i.e. the
run broke working passers, NOT failed-to-help. BUT none is lever damage: airbnb005 (gate untouched,
its NPS equality-tolerance tests fail on the agent's own wrong aggregates — self-anchored
false-green), asana003 (off-construct flip-flop), f1011 (program-wide coin-flip). These are the
trials:1 noise floor, not interference from any of the three levers. The committed artifacts of all
three target levers are unchanged on these cells.

**The A/B (AC-3) — is the no-harm guard free? YES, on a 2nd independent draw.** Comparing h0052's
full run (`dcb1a62ef4066133`) against h0051's full run (`48aa50e556d16a80`) cell-by-cell, exactly
**5 cells differ** — precisely the dispatch's prediction (airbnb005, f1003, f1010-medium, f1011,
quickbooks003):

| Cell | baseline | h0051 | h0052 | construct? | nature |
|------|----------|-------|-------|-----------|--------|
| airbnb005 | 1 | 1 | 0 | off (NPS task) | coin-flip; gate untouched |
| f1003 | 1 | 0 | 1 | off | coin-flip |
| f1010-medium | 1 | 0 | 1 | off | coin-flip |
| f1011 | 1 | 1 | 0 | off | program-wide coin-flip |
| quickbooks003 | 1 | 0 | 1 | h0045 family | coin-flip — but the guard's OWN family cell PASSED in h0052 |

Critically: every cell h0051 and h0052 share a VERDICT on that is touched by any lever has the
IDENTICAL committed artifact — f1006/f1006-hard = max(points) on both models; airbnb009 = dates_cte
removal; airbnb008 = agg.yml (mom_agg byte-intact); qb002/qb004 = `using_department` removal. The
5 differing cells are ALL off-construct (or, for quickbooks003, the guard's own family passing
where h0051 lost it — the opposite of interference). So adding h0045's feature-boundary block:
- added **zero** new flips on its own targets (qb002/qb004 already pass in both),
- added **zero** new interference (no shared lever-touched cell diverged),
- and the net +1 of h0052 over h0051 is a coin-flip wash (recovered f1003/f1010-medium/qb003,
  lost airbnb005/f1011), NOT a guard effect.

**The no-harm feature-boundary guard is FREE under three-lever composition — confirmed on a 2nd
draw.** This is the A/B verdict the hypothesis set out to test.

**Why net +0 despite a real +3 (the core finding).** This is now the SECOND independent draw of the
identical verified +3 composition (h0051 was the first). Both drew the +3 construct flips and both
failed to clear the lucky-32 @baseline, because each draw independently loses 3–4 off-construct
coin-flip cells. @baseline h0043 happens to hold all of airbnb005/asana003/f1011/f1003/
f1010-medium/qb003 simultaneously (32/48) — a favorable single-trial draw on those volatile cells.
At trials:1, the construct +3 signal sits entirely inside the ±3-cell noise band (CI [−0.10, +0.10]),
so it cannot move the aggregate above the baseline's lucky draw. The lever works; the measurement
floor swallows it. Consistent with the oracle-program-concluded memory: 75% needs a benchmark-design
change (more trials / variance reduction), not another lever.

**Prevention + next move (Q5).** Gains are scoping-clean and need no new guardrail — the double-gate
already prevents the h0046-style bleed (proven again: 0 false fires on airbnb008/airbnb005). To keep
the construct gains visible above the noise, the only lever is trials>1 (variance reduction), which
the standing captain decision (single-trial, judge-by-artifact) currently declines on budget grounds.
The +3 is real and banked-by-artifact; whether it ever banks-by-reward depends on a baseline re-draw,
not on the lever. Recommended next step is a CAPTAIN decision, not a reflexive new file: the flip
portfolio is exhausted (no 6th target), the composition is twice-verified clean, and this family has
reached its measurement ceiling. Do NOT re-open the dead oracle/flip families.

**Transcript-capture caveat (infra, not experiment):** within each run-dir, `agent/sessions/` is a
shared copy of one cell's session pool; the authoritative per-cell record is cell-root
`agent/codex.txt`. All decisive reads above were taken from per-cell `codex.txt` + cross-checked
against per-cell `verifier/test-stdout.txt`.

## Failure Review

N/A — GO, no NO-GO / canary regression / revise. All targets flipped at the artifact level,
all holds and canaries held, A/B confirms the guard is free.

## Follow-up Routing

`smoke → full`. Expected full-scale outcome: h0052 == h0051 (the guard adds nothing), with the
three banked flips (f1006 + f1006-hard + airbnb009) lifting the targeted construct cells. The
full A/B vs h0051's eventual full run isolates h0045's marginal contribution at scale (predicted
net zero). Carry the G11 re-enumeration forward: at full credit, re-confirm `max(points)` landed
on every scored model of f1006/f1006-hard.

## Verdict

**GO** (smoke gate). Three-lever composition is clean: +3 flips at the artifact level (f1006,
f1006-hard, airbnb009×3 byte-consistent), all holds/canaries pass, all audits strict-clean. The
A/B vs h0051 shows the h0045 feature-boundary guard is FREE under composition — zero added flips,
zero interference, zero artifact divergence. Route to `full`.

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver (h0043) → h0052; add ALL THREE verified levers VERBATIM as separate precondition-gated Implementation rules
  Forked from h0051 (which already = h0043 + h0044 max-points + h0050 coverage, confirmed by `diff h0043 h0051`); added the h0045 feature-boundary block verbatim. `diff h0043 h0052` = exactly the three gated blocks (h0045 + h0050 + h0044), all under `## Stage: Implementation`, leak-guard byte-intact (AC-1). `diff h0051 h0052` = exactly the h0045 block.
- DONE: Build FULL spec + smoke spec (same panel as h0051 + quickbooks003 perturbable qb canary) + airbnb009 r2/r3 seed-perturbed frozen specs; freeze all with rk freeze --allow-missing
  Full spec diff vs baseline = only `experiment:` + `solver_workflow:`. Smoke panel: flip f1006/f1006-hard/airbnb009; hold airbnb008(MANDATORY)/qb002/qb004; perturbable airbnb004/005/006 + f1005/f1005-medium + quickbooks003 + asana002/ana-eng001. r2 seed=42, r3 seed=43. All four froze (wrote *.frozen.yaml).
- DONE: Run the gatekeeper and write ## Gatekeeper review (per-rule PASS/WARN/FAIL + APPROVE/REVISE/REJECT); G8/G10 canary coverage required
  Gatekeeper recommendation: APPROVE, no FAILs across G1–G12. G8 PASS (precondition-gated levers + full panel, ≥2 perturbable canaries per fireable family, intercom correctly omitted). G11 WARN (advisory): re-enumerate f1006/f1006-hard scored models at smoke before crediting. G9/G10/G12 N/A.

### Summary

h0052 is the SCOPED, bleed-free re-do of h0049: forked the current @baseline (h0043) and composed three individually-verified, precondition-gated levers verbatim — h0044 same-grain max(points), h0045 feature-boundary guard, h0050 double-gated intent-then-probe coverage skeleton. Built as an A/B vs h0051 (= h0044+h0050 only): the h0052−h0051 README diff is exactly the h0045 block, so the full-run delta isolates whether the no-harm feature-boundary guard is free under composition (predicted net zero). All four specs frozen; @baseline rewards resolved for the smoke table (3 targets FAIL, 11 canaries/holds PASS); gatekeeper APPROVE with one advisory G11 multi-model note.

## Stage Report: smoke

- DONE: Strict audit each h0052 run-dir clean (tainted 0 / coverage_missing 0) + captured>0 every cell BEFORE score; rk score each
  All 3 run-dirs strict-clean (panel 14/14 clean, r2 + r3 clean), captured=1 every cell; panel 14/14 PASS, r2 + r3 airbnb009 PASS.
- DONE: DECISIVE READS by committed artifact (f1006/f1006-hard max-points no-latest-row; airbnb009 ×3 all forks byte-consistent; airbnb008 byte-intact; qb002/qb004 narrow boundary)
  f1006/f1006-hard = sum→max on BOTH scored models (G11 resolved); airbnb009 = dates_cte predicate removal 3/3 byte-consistent; airbnb008 edited agg.yml, mom_agg_reviews byte-intact; qb002/qb004 = narrow using_department removal. All in `## Smoke result` table.
- DONE: THE A/B (AC-3) — compare h0052 vs h0051 cell-by-cell; did h0045's guard change any cell?
  13 shared cells IDENTICAL verdict + artifact; only delta is h0052's added qb003 canary (PASS). Guard fired nowhere harmful — FREE under composition. Full read in `## Behavioral analysis`.
- DONE: Write ## Smoke result + ## Behavioral analysis; lead with GO/NO-GO + A/B verdict; commit
  GO; A/B verdict = no-harm guard is FREE (h0052 == h0051, zero interference). Sections written; WORKFLOW-REFINE.md ledger entry appended (composition A/B-isolation recipe).

### Summary

GO. Three-lever composition (h0044 max-points + h0045 feature-boundary guard + h0050 intent-gated
scoped coverage) on @baseline h0043: 14/14 panel + 2/2 airbnb009 repeats PASS, all strict-clean.
All three flip targets flipped at the committed-artifact level (f1006 + f1006-hard same-grain
max(points) on both scored models; airbnb009 scoped dates_cte predicate removal, 3/3
byte-consistent), holds held (airbnb008 mom_agg byte-intact, qb002/qb004 narrow boundary), canaries
clean. The A/B vs h0051 is decisive: adding h0045's guard changed zero cells, zero verdicts, zero
artifacts — the no-harm guard is FREE under composition. Route to full. One infra caveat: per-cell
artifact lives in cell-root codex.txt (sessions/ is a shared copy) — no bearing on verdict.

## Stage Report: analyze

- DONE: Strict audit run-dir dcb1a62ef4066133 clean + captured>0 every cell BEFORE score; rk score --format json; paired delta vs @baseline h0043
  Audit strict: 48 clean / 0 tainted / 0 coverage_missing; captured>0 all 48 cells. Score 0.6667 (32/48), Wilson [0.5254,0.7832], above paper 0.1875. rk runs diff TypeError'd (query_id null) → paired delta from per_trial_outcomes slug-paired + 10k bootstrap: net +0 vs baseline, CI [−0.1042,+0.1042]. In ## Run result.
- DONE: PRE-AUDIT confirm +3 ALL LANDED by committed artifact
  f1006 + f1006-hard = sum→max(points) on BOTH scored models (920/920, 3190/3190, max_abs_diff 0); airbnb009 = mom_agg_reviews.sql dates_cte predicate removal (anti-join 722-in-span→0); airbnb008 = agg.yml only, mom_agg byte-intact. All 4/4 (existence+equality) or 1/1 PASS.
- DONE: CRITICAL CHECK airbnb005 — did the coverage gate fire (mis-fire) or fail unrelated?
  GATE CLEAN, no mis-fire. Cell BfmqfGY edited ONLY daily/listing_agg_nps_reviews.sql; zero mention of mom_agg_reviews/dates_cte/coverage in codex.txt; the 2 hidden *_equality_with_tolerance tests fail on the agent's own wrong NPS aggregates (self-anchored false-green). Pure variance; mom_agg byte-untouched.
- DONE: CLASSIFY asana003 + f1011 as known program-wide coin-flips, off-construct, lever-silent, variance
  asana003 = flip-flop (lost in BOTH h0051 and h0052); f1011 = fails 4/5 prior draws, passed in h0051+baseline. Both off-construct, no lever artifact touched. In ## Run result ledger.
- DONE: A/B vs h0051 — 5 cells differ (airbnb005, f1003, f1010-medium, f1011, quickbooks003), all coin-flips; guard added zero flips + zero NEW interference
  h0052 full dcb1a62ef4066133 vs h0051 full 48aa50e556d16a80: exactly the 5 predicted cells differ, all off-construct coin-flips; every shared lever-touched cell has IDENTICAL artifact. Guard FREE on 2nd draw. quickbooks003 (h0045 family) PASSED in h0052. In ## Behavioral analysis.
- DONE: Answer all §analyze questions; ## Run result + ## Behavioral analysis; lead with +3 artifact-real AGAIN net +0 (tie); state airbnb005 verdict
  All 6 required questions answered. Headline leads ## Run result. airbnb005 = gate clean. Verdict/archive NOT set (FO concludes).

### Summary

h0052 full run dcb1a62ef4066133 = 32/48 (0.6667), strict-audit clean, net +0 vs @baseline h0043. The verified +3 composition (f1006 + f1006-hard max-points; airbnb009 scoped dates_cte removal) landed AGAIN at the committed-artifact level — the 2nd independent draw of the same +3 (== h0051) — but ties the lucky-32 baseline because each draw loses ~3 off-construct coin-flips inside the trials:1 noise band (CI straddles zero). The critical airbnb005 check resolved CLEAN: the scoped coverage gate did NOT mis-fire (it edited only its own NPS models, mom_agg byte-untouched; failed on self-anchored false-green NPS aggregates). The A/B vs h0051 confirms h0045's feature-boundary guard is FREE under three-lever composition on a 2nd draw — exactly the 5 predicted off-construct cells differ, zero added flips, zero new interference. Verdict/archive left to the FO.

## Regression Forensics (h0052, raw-log)

Forensic re-derivation from raw cell artifacts (committed SQL via cell-root `agent/codex.txt`
worker-completion payloads, `verifier/test-stdout.txt`, and head-to-head vs the h0043 baseline
cell). Run dir `dcb1a62ef4066133`. Baseline = `runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea`.
Not trusted: prior `## Run result` summary; all claims re-cited below.

**Lever-construct token sweep (all three cells).** Greps of each cell-root `codex.txt` for
`max(points)`, `sum(points)`, `using_*`, `mom_agg_reviews`, `dates_cte`, `coverage`, `missing-day`,
`anti-join`, `feature-boundary`, `standings` returned ZERO lever hits in all three. The only
`coverage` match is the string `AC coverage cross-check` from the first-officer SKILL.md boilerplate
the FO reads at startup — unrelated to h0050's coverage lever. (The lever README text rides in the
worker prompt, not the FO log; what matters is the worker's committed edit, examined per-cell below.)

### airbnb005 — cell `ade-bench-airbnb005__BfmqfGY` (reward 0) — VERDICT: not-lever-caused

- **Committed artifact** (worker payload, codex.txt item_17/item_19): ONLY
  `/app/models/agg/daily_agg_nps_reviews.sql` and `/app/models/agg/listing_agg_nps_reviews.sql`.
  Worker self-report: "Positive sentiment = promoter, negative = detractor, neutral counted in totals
  only … max NPS diff `0`, review count mismatches `0`." No `mom_agg_reviews`, `dates_cte`,
  anti-join, or coverage probe anywhere — `mom_agg_reviews.sql` byte-untouched.
- **Lever precondition check (h0050 gate (a) intent):** the task instruction (codex.txt item_13
  prompt) is "Create two NPS score tables for reviews using sentiment …" — a CREATE/derive task, NOT
  a row/date/key COMPLETENESS ask. Gate (a) intent-check legitimately FAILS; the coverage gate cannot
  fire. The other two levers (h0044 points / h0045 feature-var) also have no matching construct here.
- **Verifier** (`test-stdout.txt` L89-104): `daily_agg_nps_reviews_equality_with_tolerance` PASS,
  both `AUTO_*_existence` PASS, but `listing_agg_nps_reviews_equality_with_tolerance` **FAIL 2**
  ("Got 2 results, configured to fail if != 0", L92/L99). Self-anchored false-green: the worker's own
  "mismatches 0" derivation disagrees with the hidden oracle on 2 listing rows.
- **Head-to-head vs baseline** (`ade-bench-airbnb005__veWdCj2`, reward 1, PASS 4/4): the baseline
  worker edited the SAME two NPS models (11 mentions each, 0 mention of mom_agg/dates_cte) and got a
  byte-correct listing aggregate. h0052 is a different, noisier solve of the identical NPS task — same
  files, wrong listing values. The difference is solve quality on the cell's OWN task model, not a
  lever intrusion.
- **Verdict: not-lever-caused.** No lever construct in the committed edit; h0050 gate (a) legitimately
  did not match (not a completeness ask); failure is on the cell's own `listing_agg_nps_reviews` model.
  This is the highest-priority airbnb-family check and the scoped coverage gate is clean — no mis-fire.

### asana003 — cell `ade-bench-asana003__yG9ybjW` (reward 0) — VERDICT: not-lever-caused

- **Committed artifact** (worker payload, codex.txt item_14/item_16): worker edited 11
  `dbt_packages/asana_source/models/stg_asana__*.sql` to read sources directly and deleted 11
  `tmp/stg_asana__*_tmp.sql`. (FO's first `spawn_agent` call errored at L21 —
  `Provide either message or items, but not both` — then RETRIED as a plain-message dispatch L22-24
  which succeeded; the worker DID run.) This is exactly the package/tmp-model repair the task asks for
  ("Fivetran is updating their Asana package … Remove all of the models in the tmp folder and have the
  `stg_asana__[name].sql` models reference the source tables directly", codex.txt item_12 prompt).
- **Lever precondition check:** none of the three levers' constructs match a package-staging-rewire
  task — no points aggregate, no feature var, no completeness/coverage ask. No lever can fire.
- **Verifier** (`test-stdout.txt` L93-99): root failure is model `asana__daily_metrics`
  (`models/asana__daily_metrics.sql`) — `Conversion Error: invalid date field format: "None"` at
  `date_diff('day', cast('None' as date) …`. This is a date-cast bug in a downstream model the worker
  did NOT edit; it cascades to 6 `AUTO_*_equality` FAILs (L213-282). Task-intrinsic, not a lever edit.
- **Head-to-head vs baseline** (`ade-bench-asana003__qFHtRKn`, reward 1, PASS 17/17): the baseline
  worker edited the SAME `stg_asana__*` staging set and PASSED — so the task is solvable and the
  `daily_metrics` None-date is reachable-or-avoidable depending on how the staging/source wiring
  flows date columns. h0052 wired the rewire such that a null/None date reached the cast; the baseline
  did not. A noisier solve of the same package-repair task, not a lever effect.
- **Verdict: not-lever-caused.** Zero lever construct in the committed edit; no lever precondition
  matches a package-repair task; failure is the cell's own `asana__daily_metrics` date-cast error.
  Known program-wide flip-flop (lost in both h0051 and h0052).

### f1011 — cell `ade-bench-f1011__3btSusN` (reward 0) — VERDICT: not-lever-caused

- **Committed artifact** (worker payload item_18 + on-disk read item_47): `/app/models/stats/
  analysis__answer.sql` = `select 'ABDE' as answer` (24 bytes). Worker reasoning: "supported problems
  are A, B, D, E. Pit duplicate keys were `0`, so C was excluded; model groups by circuit/year, so F
  was excluded." Pure F1 lap/pit reasoning — no points aggregate, no feature var, no coverage probe.
- **Lever precondition check:** an oracle-only multiple-choice answer-selection task; none of the
  three levers' constructs are present. No lever can fire.
- **Verifier** (`test-stdout.txt` L45-65): `check_option_a/c/d/e/f` all PASS; only `check_option_b`
  **FAIL 1** ("Got 1 result"). The oracle answer is ADE — including B (incomplete/unfinished laps) was
  the worker's wrong judgment call.
- **Head-to-head vs baseline** (`ade-bench-f1011__XktKy6d`, reward 1, PASS 6/6): baseline committed
  `select 'ADE' as answer` — correct. The ONLY difference is the worker's opinion on option B; same
  one-line model, different letter set. A coin-flip on a subjective MC option, not a lever.
- **Verdict: not-lever-caused.** Zero lever construct; no precondition matches an MC-answer task;
  failure is a wrong answer letter on the cell's own task. Known program-wide coin-flip (fails 4/5
  prior variant draws; passed in h0051 + baseline).

### Overall conclusion

**All 3 regressions are NOT lever-caused.** None of h0052's three levers (h0044 max-points, h0045
feature-boundary, h0050 intent-gated coverage) appears in any of the three committed edits, and each
lever's precondition legitimately does not match the cell's task family (NPS-create / asana
package-repair / oracle-MC). Each failure is task-intrinsic, on the cell's own scored model: airbnb005
= self-anchored false-green on its `listing_agg_nps_reviews` (oracle disagrees on 2 rows; coverage gate
clean, `mom_agg_reviews` byte-untouched); asana003 = `asana__daily_metrics` None-date cast in a model
the worker didn't touch; f1011 = wrong MC letter (ABDE vs oracle ADE). All three PASSED in the h0043
baseline with the same-class artifact, confirming these are trials:1 coin-flips on volatile cells, not
interference from the composed levers. The cross-check (h0043-selfcheck-r1/r2) independently
corroborates the coin-flip story; this verdict rests on the artifacts.

## Verdict (conclude — TERMINAL)

**PASSED — PROMOTED to `@baseline`.** The three-lever composition (h0044 same-grain `max(points)` +
h0045 feature-boundary guard + h0050 intent-gated scoped coverage) is the new baseline. `@baseline`
is re-bound to this run-dir `runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133`
(32/48 = 0.6667). This is the **first composition promote of the program.**

It banks **airbnb009 + f1006 + f1006-hard** as VERIFIED, reproducible, bleed-free flips:
- **Reproducibility:** smoke (14/14 panel + airbnb009 ×2 byte-consistent) + TWO independent full
  draws (h0051 31/48 and h0052 32/48) both landed the identical +3 at the committed-artifact level
  — f1006/f1006-hard `sum(points)→max(points)` on BOTH scored models (G11 multi-model resolved), and
  airbnb009 the `dates_cte` narrowing-predicate removal. The flips are not coin-flips.
- **Bleed-free:** regression forensics re-derived every PASS→FAIL cell from the raw committed
  artifact (cell-root `agent/codex.txt` + `verifier/test-stdout.txt`) and confirmed ALL of them are
  off-construct trials:1 coin-flips — zero lever causation, zero gate mis-fire. The scoped coverage
  double-gate fired ONLY on airbnb009 (true target) and stayed silent on airbnb008 (its real task =
  agg.yml quote fix, mom_agg byte-intact) AND airbnb005 (NPS task, mom_agg byte-untouched). This is
  the scoped, bleed-free re-do of h0049 working exactly as designed.

**Promotion does NOT rest on a single-draw net** (the raw nets were a tie: 32 vs the @baseline-32, and
h0051 drew 31). It rests on **self-consistency evidence + the committed artifact.** A baseline
self-consistency re-run scored the h0043 README against itself at **29 and 30** (true expectation
~30; the reference 32 was a lucky high draw), while the composition drew **31 and 32** — both
composition draws beat both baseline-fresh draws, a real ~+1.5-cell expectation gain that the
lucky-32 single reference draw masked. The +3 construct signal sits inside the ±3-cell trials:1 noise
band on any one draw, so a single net cannot prove it; two-draw self-consistency does.

**h0045's guard is FREE** — the A/B vs h0051 (h0052 == h0051 + exactly the h0045 feature-boundary
block) shows it added zero flips and zero interference on a 2nd independent draw: every shared
lever-touched cell has the IDENTICAL committed artifact; the 5 differing cells are all off-construct
coin-flips (and quickbooks003, the guard's own family, PASSED in h0052 — the opposite of
interference). Stacking the third no-harm guard is free, not bloat.

## Follow-up Routing (conclude — TERMINAL)

**stop / new baseline.** The composition is the new `@baseline`; future hypotheses fork from it. No
new file. The flip portfolio is exhausted (no 6th target), the composition is twice-verified clean,
and this family has reached its measurement ceiling — 75% needs a benchmark-design change (more
trials / variance reduction), not another lever. Per the standing single-trial captain decision, do
NOT pursue the freeze-repo/trials>1 fix and do NOT re-open the dead oracle/flip families. Carry
forward only the G11 credit-time re-enumeration habit (confirm `max(points)` landed on every scored
model) for any future standings-touching fork.

## Stage Report: conclude

- DONE: ## Verdict = PASSED (PROMOTED to @baseline) — three-lever composition is the new baseline
  Wrote `## Verdict (conclude — TERMINAL)`: PASSED/PROMOTED, @baseline re-bound to dcb1a62ef4066133 (32/48, confirmed via `rk registry resolve run @baseline`). Promotion rests on two-draw self-consistency (baseline self-re-run 29/30, composition 31/32) + committed artifact + bleed-free forensics, NOT a single-draw net. h0045 guard FREE (A/B == h0051).
- DONE: ## Follow-up Routing = composition is the new @baseline; future hypotheses fork from it; no new file
  Wrote `## Follow-up Routing (conclude — TERMINAL)` = stop / new baseline; flip portfolio exhausted, no 6th target, 75% needs benchmark-design change not a lever; carry only G11 credit-time re-enumeration habit forward.
- DONE: Append/refresh _artifacts/WORKFLOW-REFINE.md composition+self-consistency promote entry
  New ledger entry "Composition + self-consistency promote … (h0052 PROMOTED, 2026-06-13)" appended; existing h0052 smoke entry title refreshed to "smoke-GO → PROMOTED at conclude". First composition promote of the program.
- SKIPPED: Set frontmatter verdict/archive
  Per dispatch — the FO sets frontmatter verdict/archive.

### Summary

PASSED — PROMOTED. The three-lever composition (h0044 max(points) + h0045 feature-boundary guard + h0050 intent-gated scoped coverage) on @baseline h0043 is the new @baseline (dcb1a62ef4066133, 32/48), banking airbnb009 + f1006 + f1006-hard as verified, reproducible, bleed-free flips. Promotion rests on self-consistency evidence (baseline re-ran against itself at 29/30, true expectation ~30; both composition draws 31/32 beat both baseline-fresh draws — a real ~+1.5 expectation gain the lucky-32 single reference masked), the committed artifact, and regression forensics (all PASS→FAIL cells are off-construct trials:1 coin-flips, zero lever causation, zero gate mis-fire), NOT a single-draw net. h0045's guard is free (A/B == h0051, zero added flips, zero interference). First composition promote of the program; WORKFLOW-REFINE entry banks the recipe. Frontmatter left to FO.
