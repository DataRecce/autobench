---
id: h0062
title: Generalize the F1-pinned max(points) rule into a semi-additive-measure rule gated on a monotonicity probe
status: conclude
kind: hypothesis
source: Captain conversation 2026-06-17 — categorizing the baseline README's added rules (general-purpose / dbt-craft / benchmark-specific) surfaced CUMULATIVE-SNAPSHOT TOTALS as the one Category-C "memorized answer"; this tests whether its domain fact can be replaced by a locally-checkable structural gate, moving it from a pin to a portable rule.
started: 2026-06-17
completed:
verdict:
score:
worktree:
---

## Hypothesis

**Claim.** The benchmark-pinned `CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN`
rule can be rewritten as a **general semi-additive-measure rule** whose trigger is a
**locally-computable monotonicity probe** (no domain knowledge of F1), and it will
**reproduce h0044's f1006 / f1006-hard flips cell-identically** while **not regressing**
any task that legitimately `SUM`s an additive (per-period delta) measure.

**Why this is the one de-overfittable Category-C rule.** The current rule encodes a
domain fact — *"F1 standings points are a cumulative race-by-race snapshot, so summing
double-counts"* — which cannot be stated without knowing the task is F1. But that fact
is a special case of the dimensional-modeling **additive / semi-additive / non-additive
measure** taxonomy: a *semi-additive* measure (running balance, inventory level,
cumulative standings) must not be `SUM`med across the dimension it accumulates over. And
"is this a cumulative snapshot?" **has an oracle-free probe**: a cumulative measure is
**monotonically non-decreasing within each entity** when ordered by its sequence key; a
per-period delta is not. That probe is the same shape as the existing COVERAGE-REPAIR
`EXCEPT` gate — a FIRED local probe replaces the domain name.

**The single README change.** In `solver_workflows/h0062-.../README.md`, replace the
`CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN (gated)` block with:

> **SEMI-ADDITIVE / SNAPSHOT MEASURE — DON'T SUM A RUNNING TOTAL (gated).** When a task
> repairs an entity/period total that is too high and the model `SUM`s a numeric measure
> across a sequence within each entity, first probe whether the measure is a cumulative
> snapshot rather than a per-period delta: order each entity's rows by the sequence key
> and test whether the measure is non-decreasing (the MONOTONICITY PROBE). If it is
> non-decreasing across (nearly) every entity, the measure is a running cumulative total
> and `SUM` double-counts — replace `sum(measure)` with `max(measure)` at the existing
> entity/period grain. If the probe shows the measure rises *and* falls (a genuine
> per-period delta), `SUM` is correct — leave it byte-intact. Do NOT switch to
> latest-row, rank, `row_number`, `QUALIFY`, or order-by-final-race for the monotonic
> case; `max()` at the grain is the minimal correct repair.
>
> ```sql
> -- MONOTONICITY PROBE (oracle-free): is the measure non-decreasing within each entity?
> select bool_and(m >= prev_m) as is_cumulative
> from (
>   select m,
>          lag(m) over (partition by entity_id order by seq_key) as prev_m
>   from {{ ref('suspect_model') }}
> )
> -- TRUE  -> cumulative snapshot -> use max(m) at the entity/period grain.
> -- FALSE -> additive per-period delta -> keep sum(m); do not touch it.
> ```

**Critical design constraint (keep the fix shape, generalize only the trigger).** h0044
explicitly forbids `row_number` / `QUALIFY` / order-by-final-race because those branches
*hurt* the real run. So this hypothesis generalizes the **detection** (domain name →
monotonicity probe) and the **framing** (F1 standings → any semi-additive measure) but
keeps the **repair = `max()` at the existing grain** for the monotonic-non-decreasing
case. This is the safe edge: a behavior-preserving generalization, not a re-implementation.

**Target datasets.**
- Flip-preservation targets: `ade-bench-f1006`, `ade-bench-f1006-hard` (must stay PASS,
  cell-identical committed SQL = `max()` at grain).
- Same-family sentinels: `ade-bench-f1005`, `ade-bench-f1005-medium`, `ade-bench-f1001`.
- **Additive-SUM canary (the new risk this lever introduces):** ≥2 perturbable passers
  whose committed model legitimately `SUM`s a per-period delta — the general rule's FALSE
  branch must leave them byte-intact. The general (vs pinned) rule fires on *any* "total
  too high + SUM across a sequence" task, so it can mis-fire where the pinned F1 rule never
  could; these canaries are what make the generalization falsifiable. Specific canary IDs
  resolved at `propose` (after `rk registry resolve run @baseline` + per_trial_outcomes).

## Pre-smoke Decision-Fork Probe

*(Design-stage proxy reasoning — the literal local data probe is run at `propose`/`smoke`,
not yet executed here.)*

- **Fork under test.** Does a domain-blind monotonicity probe over the shipped f1
  `*_standings` data fire (points non-decreasing within each driver, ordered by round)?
  If YES, the general rule resolves to the *same* `max()`-at-grain repair the pinned rule
  produces, and the committed artifact is byte-identical → flip preserved. If the probe
  does NOT fire on the real shipped data (e.g. points are stored as per-race deltas, or
  the sequence key isn't obvious to the solver), the general rule would keep `sum()` and
  the flip is LOST — that is the falsification.
- **Prompt context.** Solver-visible only: the f1 standings model SQL + the shipped
  standings seed/source rows. No hidden verifier counts.
- **Control (A).** Current `@baseline` pinned rule → f1006/f1006-hard PASS via `max(points)`.
- **Proposed (B).** General semi-additive rule → expected same `max()` artifact iff the
  probe fires.
- **Expected artifact signature in a real run.** The committed f1006 / f1006-hard models
  use `max(points)` (or `max(<measure>)`) at the existing entity/season grain — *identical*
  to the h0044 / current-baseline artifact; `Got N` distance-to-pass unchanged vs `@baseline`.
- **Proxy caveat.** This is design reasoning about a structural property; it does NOT prove
  the production solver will (a) run the probe, (b) pick the right `seq_key`, or (c) resist
  the `row_number`/latest-row branch under the new wording. Smoke on the real run is required.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0062-semi-additive-measure-generalize-maxpoints.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`.**

**AC-4 — Behavior-preserving generalization (the actual test).** PASSES iff:
  1. `f1006` and `f1006-hard` stay PASS, with the committed SQL still `max()` at the
     entity/season grain (cell-identical to `@baseline`; `Got N` unchanged) — the
     domain-blind probe reproduced the domain-specific flip; AND
  2. zero regressions on the same-family sentinels AND on the additive-SUM canaries — the
     general rule's FALSE branch left legitimate `sum()` models byte-intact.
  FAILS if either f1006/f1006-hard regresses (probe didn't fire, or the new wording drifted
  the solver into the forbidden latest-row/window branch) or any additive-SUM canary flips
  PASS→FAIL (the generalized trigger mis-fired on a legitimate sum).

## Gatekeeper review

**Recommendation: APPROVE** — clean single-idea README generalization; integrity rules (G1/G2/G3/G6) all PASS, all 7 smoke tasks confirmed @baseline(h0061) passers; only WARNs are a benign `concurrency.trials` override in the smoke spec and the broadened-gate mis-fire surface.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-17.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Only one README block changed (lines 188–193 → 188–210, under `## Stage: Implementation`): `CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN` → `SEMI-ADDITIVE / SNAPSHOT MEASURE`. No other `## Stage:` section touched; one idea (domain-name trigger → monotonicity probe). |
| G2 leak-guard intact | PASS | `diff` of lines 1–35 (leak-guard + dependency paras) exit 0 (byte-identical). Leak-token grep over the added `>` lines (`AUTO_`/`solution__`/`verifier`/`equality test`/`curl`/`wget`/`git clone`/`drive…zero`/`re-run your own`) returns no matches. |
| G3 spec two fields | PASS | `diff baseline.yaml h0062.yaml` = only `experiment:` and `solver_workflow:`. `agent.kind: spacedock_solver` + `runtime: codex` preserved (lines 4–5); top-level `trials: 1`. |
| G4 smoke tasks-only | WARN | Smoke diff adds the `benchmark.tasks` block (7 IDs, all `ade-bench-` prefixed, every named target present) BUT ALSO overrides `concurrency.trials: 4→1`. The trials override is a documented harness freeze-repo-race workaround (operator-sanctioned), not experiment scope — but it is a second changed field vs the strict "only benchmark.tasks" rule. Note for captain; does not block. |
| G5 both frozen | PASS | `ls`: both `…frozen.yaml` (1735 B) and `…smoke.frozen.yaml` (1890 B) exist; both carry `kind: spacedock_solver` + `runtime: codex` (lines 4–5). |
| G6 resolver fidelity | PASS | Inserted text == Falsifiable claim: generalize the TRIGGER (F1 standings-points domain name → domain-blind `lag()`-monotonicity probe) while keeping the REPAIR (`max()` at the existing entity/period grain) and the h0044 forbidden-branch list (no latest-row/rank/row_number/QUALIFY/order-by-final-period/recompute). Generative/independent structural gate with a FIRED local probe — NOT self-anchored "re-run/verify your own output." No scope creep. |
| G7 actionability/inert-risk | PASS | Mechanical-substitution + worked-example: a copyable SQL probe skeleton (`bool_and(m >= prev_m) … lag() over (partition by entity_id order by seq_key)`) plus the literal `sum(measure)→max(measure)` edit. Not abstract-structural prose. Inherits h0044's proven flips, so low inert-risk. |
| G8 regression-canary coverage | N/A | Lever is GATED ("entity/period total too high AND model SUMs a numeric measure across a sequence within each entity"), not generative — strictly N/A for the cross-family panel. See captain note: the gate is BROADER than the F1-pin, so two additive-SUM canaries (airbnb005, airbnb001) are added as the new-mis-fire panel and assessed there. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — single gated rule, one repair path. |
| G10 self-correcting false-positive | WARN | The lever is probe-and-act, but (a) it is GATED (fires only on "total too high + SUM across a sequence"), not generative; (b) the probe checks a STRUCTURAL property (monotonicity) of the suspect model's own ordered data — not a re-derivation of the model's number that could re-correlate and false-green (the h0012 trap); (c) it mandates the MINIMAL repair (`max()` at existing grain), not "switch to a structurally different path." The residual concern is the same as G8: a broadened gate can fire on a legitimate sum. Soft WARN — surfaced via the additive-SUM canaries. |
| G11 multi-model-target risk | PASS | Per `_artifacts/bug-type-taxonomy.md` L42, f1006 is scored by a SINGLE model `AUTO_constructor_points_equality`; f1006-hard is its variant. The lever's `max()` repair reaches that scored model. Not the airbnb007 two-model trap (airbnb007 is NOT in this smoke set). Lever covers the target's only scored model. |
| G12 decision-fork probe quality | PASS | `## Pre-smoke Decision-Fork Probe` present with all required fields: Fork under test (does the domain-blind probe fire on shipped f1 `*_standings`, points non-decreasing per driver by round), Prompt context (solver-visible model SQL + standings seed/source, "No hidden verifier counts"), Control A (current pinned rule → f1006/-hard PASS via `max(points)`), Proposed B (general rule → same `max()` iff probe fires), expected committed-artifact signature (`max(points)`/`max(<measure>)` at season grain, `Got N` unchanged), and an explicit Proxy caveat ("does NOT prove the production solver will run the probe / pick seq_key / resist the row_number branch; smoke required"). No hidden-correct labels, no expected totals, no prior pass/fail used as evidence; wording matches the inserted README block. |

**For the captain:**
- **G8 (broadened-gate canary coverage):** The generalization's NEW risk is over-firing on a legitimate additive SUM, and the two canaries cover it well: airbnb005 (committed model SUMs rolling-28d per-listing/day review counts — genuine per-period deltas, probe MUST return FALSE) and airbnb001 (monthly review COUNTs — additive per-period delta, gate must not fire). Both are confirmed @baseline(h0061) passers and both are PERTURBABLE — they are exactly the "total over a sequence within an entity" shape the broadened gate now reaches, so the lever can plausibly FIRE on them; if the FALSE-branch fails to leave `sum()` byte-intact they will regress. Caveat: both canaries live in the **airbnb** family, while the targets' mechanism (additive-SUM repair shape) is shared by the **f1** construct family. The f1 same-family sentinels (f1005, f1005-medium = cumulative-snapshot fixes where the probe must STILL fire; f1001 = a build where the gate must NOT fire) cover the TRUE-branch / no-fire f1 surface, but there is no f1 task in the panel that legitimately SUMs a per-period delta (an f1 FALSE-branch canary). Coverage is adequate for the cross-domain mis-fire surface; the residual blind spot is an f1-family legitimate-sum passer, if one exists.
- **G12 (AC-4 probe):** Strong and leak-free. The one thing the probe cannot establish (and openly flags) is whether the production solver will actually run the probe, pick the right `seq_key`, and resist the forbidden window/latest-row branch under the new domain-blind wording — treat smoke as the real test of behavior-preservation, judging f1006/-hard by the committed `max()`-at-grain artifact (cell-identical, `Got N` unchanged), not the aggregate reward.
- **Net:** No FAILs → APPROVE. Two WARNs to glance at: the `concurrency.trials: 4→1` smoke override (G4 — confirm it is the intended freeze-race workaround, not a stray edit) and the gated-lever mis-fire surface (G8/G10), which the canary panel addresses.

## Smoke result

**4/7 PASS — STRICT AC-4 NO-GO.** Run-dir `runs/ade-bench-h0062-semi-additive-measure-generalize-maxpoints/63ffe07e1eefe1d6` (smoke, concurrency 3, ~27 min, done rc=0).

- **Strict audit: CLEAN.** `rk audit … --policy strict` → 7/7 trials `taint_status: clean`, zero findings.
- **Score:** `rk score` → stratified mean 0.5714 (4/7), `n_completed=7`, `n_errored=0` — every cell captured>0 (no infra error).

| Task | Role | @baseline | h0062 | Committed artifact (this run) |
|------|------|-----------|-------|-------------------------------|
| f1006 | flip target | PASS | **PASS** ✅ | `max(cs.points)` at season grain — cell-identical to @baseline |
| f1006-hard | flip target | PASS | **FAIL** ❌ | `row_number() over (… order by round desc) … WHERE standings_order=1` — FORBIDDEN latest-row branch; `AUTO_constructor_points_equality` Got 2 (driver_points PASSED) |
| f1005 | same-family sentinel | PASS | **PASS** ✅ | `max(cs.points)` at grain — probe fired correctly |
| f1005-medium | same-family sentinel | PASS | **FAIL** ❌ | `QUALIFY ROW_NUMBER() OVER (… ORDER BY round DESC)` — FORBIDDEN qualify branch; `AUTO_constructor_points_equality` Got 2 (driver_points PASSED) |
| f1001 | same-family sentinel (build) | PASS | **FAIL** ❌ | src/stg build; gate never touched a points model; failed `src_models_are_correct` Got 1 — UNRELATED build coin-flip |
| airbnb005 | additive-SUM canary | PASS | **PASS** ✅ | `sum(rolling daily counts)` BYTE-INTACT — gate did NOT mis-fire |
| airbnb001 | additive-SUM canary | PASS | **PASS** ✅ | monthly review COUNT BYTE-INTACT — gate did NOT mis-fire |

**Regression classification: 2 CAUSAL (f1006-hard, f1005-medium), 1 VARIANCE (f1001).** Both canaries HELD — the broadened gate did NOT mis-fire on legitimate additive sums. The failure is the *opposite* risk from the one the canaries guarded: the generalization drifted the solver OFF the safe `max()` edge ONTO the forbidden latest-row/`row_number`/`QUALIFY` branch on the two HARDER cumulative variants.

## Run result

(No full run — NO-GO at smoke.)

## Behavioral analysis

**The generalization is NOT behavior-preserving (AC-4 FAILS).** The committed artifacts are the verdict basis:

1. **The forbidden-branch drift is causal and reproducible across both hard variants.** @baseline h0061 f1006-hard committed `max(cs.points)` (PASS). Under the h0062 generalized wording, f1006-hard committed `row_number() … order by round desc WHERE standings_order=1` and f1005-medium committed `QUALIFY ROW_NUMBER() … ORDER BY round DESC` — two different spellings of the SAME forbidden latest-row branch the README explicitly prohibits ("Do NOT switch to latest-row, rank, row_number, QUALIFY, or order-by-final-period for the monotonic case"). The pinned h0044 rule suppressed this; the generalized rule did not.

2. **Same 2-row constructor failure, driver model correct, on BOTH causal cells.** f1006-hard and f1005-medium are each scored by TWO models. On both, `AUTO_driver_points_equality` PASSED but `AUTO_constructor_points_equality` failed with exactly `Got 2`. The latest-row branch happens to be right for driver standings but wrong for 2 constructors — precisely the tie/duplicate-final-snapshot edge case that makes latest-row unsafe and `max()` correct. This is the multi-model-target trap (G11) realized: a single artifact choice that lands one scored model and breaks the other.

3. **Why the easy targets passed but the hard ones didn't.** f1006 and f1005 (non-hard) committed `max()` and passed — the generalized rule *can* reproduce the flip. But the longer, branch-naming generalized block is less reliable than h0044's terse domain-pinned wording: on the harder variants the solver reasoned its way into "latest snapshot per entity" (a semantically-reasonable but forbidden reading of "cumulative snapshot"), exactly the failure mode the domain-pinned rule's brevity avoided. Wordier generalization → more surface for the solver to rationalize a forbidden branch.

4. **The canaries vindicate the propose-stage design but the lever still loses.** airbnb005 (rolling-28d daily-count SUM) and airbnb001 (monthly COUNT) both held byte-intact — the FALSE-branch worked, the gate did not over-fire on legitimate additive sums. The G8/G10 mis-fire risk did NOT materialize. The lever fails on the TRUE branch (it should produce `max()` and instead drifts), not the FALSE branch.

5. **f1001 is variance, not the lever.** f1001 is an src/staging build task — no "total too high" repair, no points SUM, so the gate's precondition cannot fire. Its committed edits are all `src_*`/`stg_*` models; it failed `src_models_are_correct` (Got 1), a build-correctness test unrelated to the SEMI-ADDITIVE rule. f1001 is a documented build coin-flip (h0023 f1001-bleed, h0059 src-naming history); this regression is the same tail, independent of h0062.

## Failure Review

**Primary failure type: edit-shape-without-oracle drift onto a forbidden branch (causal) — the generalization degraded the cumulative-snapshot construct.** Not a mis-fire (canaries held), not inertness (the rule DID act), not variance for the two f1 hard cells (reproducible forbidden-branch drift on both).

1. **What failed and how do we know?** f1006-hard and f1005-medium regressed PASS→FAIL because the solver committed the forbidden latest-row/`row_number`/`QUALIFY` branch instead of `max()` at grain. Known from the committed apply_patch bodies (`WHERE standings_order=1` / `QUALIFY ROW_NUMBER() … ORDER BY round DESC`) vs @baseline's `max(cs.points)`, with `AUTO_constructor_points_equality` Got 2 on both. f1001 regressed on an unrelated build test (`src_models_are_correct` Got 1), gate never engaged.

2. **Is it the lever or the harness?** The lever (the README change), for the two f1 hard cells: the ONLY variable vs @baseline is the generalized wording, the drift is on the exact construct the rule governs, and it reproduced across two independent cells with the same signature. f1001 is harness/solver variance independent of the lever.

3. **Causal or variance?** 2 causal (f1006-hard, f1005-medium — reproducible forbidden-branch drift), 1 variance (f1001 — unrelated build coin-flip). The two causal regressions are not single-cell noise: they share an identical failure signature (forbidden branch → constructor Got 2, driver PASS) on the two hardest cumulative variants.

4. **Did the canaries / sentinels behave as designed?** Yes for the mis-fire axis: airbnb005/airbnb001 held byte-intact (gate did not over-fire on legitimate sums) and f1006/f1005 confirmed the rule CAN land `max()`. The propose-stage G8/G10 worry (over-firing) was correctly judged low-risk. The realized risk was the under-specified TRUE branch on hard variants, which smoke (not propose) was the right gate to catch.

5. **What's the transferable lesson?** Generalizing a terse domain-pinned rule into longer domain-blind prose that *enumerates* the forbidden alternatives can BACKFIRE: naming "row_number / QUALIFY / latest-row" as things-not-to-do raises their salience and gives the solver a reasoning path into them on harder variants, where the pinned rule's brevity + concrete domain anchor ("treat points as cumulative race-by-race snapshots → max(points)") kept it on the safe edge. The domain fact was load-bearing precisely BECAUSE it was concrete and short. This is a Category-C "memorized answer" that resists de-overfitting: its value is the brevity+concreteness, not just the F1 name. (Connects to the instruction-lever taxonomy: construct>check, and mechanical-substitution > abstract-structural prose.)

## Follow-up Routing

**Recommended route: `conclude` (REJECTED — generalization not behavior-preserving).** AC-4 FAILS: 2 of 3 regressions are causal forbidden-branch drift on the exact construct the rule governs, reproduced across both hard variants with an identical signature. The lever does not preserve the h0044 flip; it loses f1006-hard + f1005-medium at the smoke gate. The canaries held, so the de-overfitting *direction* (probe-gated max() repair) is sound in principle — but the generalized PROSE is the problem, not the probe concept.

Secondary option if the captain wants to salvage rather than conclude: `hypothesis` with a narrowed revision — keep the monotonicity-probe TRIGGER but restore h0044's terse repair wording (drop the long forbidden-branch enumeration that raised latest-row salience; state only "replace sum(measure) with max(measure) at the existing grain" plus the probe). That tests whether brevity, not the domain name, was the load-bearing element. Given the flip program is already documented as EXHAUSTED and this is a de-overfit experiment (not a new flip), `conclude` is the higher-value route: the *knowledge gain* (Category-C max()-points rule resists de-overfitting because its brevity+concreteness is load-bearing; longer branch-naming prose drifts the solver onto the named-forbidden branch) is the deliverable.

## Verdict

## Stage Report: propose

- DONE: Fork @baseline (h0061-lean-readme README) → h0062 solver dir, replacing ONLY the CUMULATIVE-SNAPSHOT max() block with the generalized SEMI-ADDITIVE / SNAPSHOT MEASURE rule (monotonicity-probe trigger + max()-at-grain repair, F1 domain framing removed), leak-clean.
  `diff h0061/README.md h0062/README.md` = one block (lines 188–193 → 188–210, `## Stage: Implementation`); leak-token grep CLEAN (no AUTO_*/solution__*/check_*/dataset-slug/expected-count/curl/wget).
- DONE: Author both specs (cp baseline.yaml → h0062.yaml differing ONLY in experiment: + solver_workflow:; cp → .smoke.yaml adding benchmark.tasks). Smoke set = f1006 + f1006-hard (flip targets), f1005/f1005-medium/f1001 (same-family sentinels), airbnb005 + airbnb001 (additive-SUM canaries). Freeze both with rk freeze --allow-missing.
  `diff baseline.yaml h0062.yaml` = only experiment:+solver_workflow:; smoke diff = +benchmark.tasks block + concurrency.trials 4→1 (freeze-race workaround, matches h0060.smoke). Both `…frozen.yaml` written (1735 B / 1890 B).
- DONE: Run the gatekeeper subagent and record its per-rule table + overall recommendation in ## Gatekeeper review; flag G8 (additive-SUM canary coverage) and G12 (AC-4 decision-fork probe quality).
  Recommendation APPROVE (no FAILs; G2/G3/G6 PASS). G8 N/A (gated lever) — captain note confirms airbnb005/airbnb001 are perturbable additive-SUM canaries (residual gap: no f1-family FALSE-branch canary). G12 PASS — probe leak-free, exact README wording, control A, artifact signature, proxy caveat. WARNs: G4 (concurrency override) + G10 (broadened-gate mis-fire), neither blocks.

### Summary

Generalized the F1-pinned `CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN` rule into a domain-blind `SEMI-ADDITIVE / SNAPSHOT MEASURE` rule: the trigger moves from the F1-standings domain name to a locally-computable `lag()`-monotonicity probe, while the repair (`max()` at the existing grain) and h0044's forbidden-branch list are kept byte-for-byte. Exactly one README idea changed; the full spec differs from baseline only in `experiment:`+`solver_workflow:`. The smoke set adds two additive-SUM canaries (airbnb005 rolling-28d SUM, airbnb001 monthly COUNT) to expose the broadened gate's new mis-fire surface — the legitimate-`sum()` FALSE branch. Gatekeeper APPROVE with two non-blocking WARNs (the sanctioned concurrency freeze-race override and the gated-lever mis-fire surface, which the canary panel addresses). The only residual coverage gap the gatekeeper flagged is the absence of an f1-family legitimate-additive-sum passer (an f1 FALSE-branch canary), if one exists.

## Stage Report: smoke

- DONE: Strict audit + score, captured>0 all cells; recorded in ## Smoke result.
  `rk audit --policy strict` → 7/7 clean, 0 findings; `rk score` → 0.5714 (4/7), n_completed=7, n_errored=0.
- DONE: Per-cell artifact read for the 3 regressions vs @baseline h0061.
  f1006-hard & f1005-medium drifted to FORBIDDEN latest-row/`row_number`/`QUALIFY` branch (constructor_points Got 2; driver_points PASS) vs @baseline `max(cs.points)`; f1001 = unrelated src-build coin-flip (`src_models_are_correct` Got 1, gate never engaged). Canaries airbnb005/airbnb001 held with byte-intact sum()/count().
- DONE: Classify causal vs variance; append ## Failure Review + ## Behavioral analysis; recommend route.
  2 CAUSAL (f1006-hard, f1005-medium — reproducible forbidden-branch drift, identical signature) + 1 VARIANCE (f1001 build coin-flip). Route: `conclude` (REJECTED — generalization not behavior-preserving); secondary salvage = `hypothesis` (restore terse repair wording, keep probe trigger).

### Summary

Smoke 4/7 → strict AC-4 NO-GO. The generalization is NOT behavior-preserving: the wordier domain-blind rule drifted the solver off `max()` at grain onto the forbidden latest-row/`row_number`/`QUALIFY` branch on the two HARDER cumulative variants (f1006-hard, f1005-medium), each failing constructor_points by exactly 2 rows (driver_points correct) — the multi-model-target trap realized. The easy targets (f1006, f1005) committed `max()` and held, and both additive-SUM canaries held byte-intact, so the propose-stage mis-fire worry did not materialize; the lever fails on the under-specified TRUE branch, not the FALSE branch. Transferable lesson: enumerating the forbidden alternatives in longer prose RAISES their salience and gives the solver a reasoning path into them — h0044's brevity + concrete domain anchor was load-bearing, so this Category-C rule resists de-overfitting. Recommended route `conclude` (REJECTED); the knowledge gain is the de-overfit lesson.
