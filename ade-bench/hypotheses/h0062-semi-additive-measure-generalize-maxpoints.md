---
id: h0062
title: Generalize the F1-pinned max(points) rule into a semi-additive-measure rule gated on a monotonicity probe
status: propose
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

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

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
