---
id: h0062
title: Generalize the F1-pinned max(points) rule into a semi-additive-measure rule gated on a monotonicity probe
status: hypothesis
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

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
