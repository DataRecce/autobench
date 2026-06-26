---
id: spd0012
title: MoM = window LAG over the model's own single-window output (drop the raw-grouping template)
status: hypothesis
kind: hypothesis
source: "forks current champion @baseline = spd0008-over-emit-collapse; carries the spd0011-validated Implementation Contract checkpoint + G2_LATEST_WINDOW_FULL_REFRESH template, drops the spd0011 G2_REPORT_RAW_GROUPING_HOLD template (proven net-negative destabilizer over two cycles), and replaces spd0011 FIX A's soft NULL-condition with a hard LAG-over-own-output derivation-method constraint"
started: 2026-06-26
completed:
verdict:
score:
worktree:
---

## Hypothesis

The current registry champion (`@baseline` = `spd0008-over-emit-collapse`,
`runs/spider2-dbt-spd0008-full/4ba55fba0138a84d`, 24/60) leaves `airbnb001` failing on a single
graded column: `mom_agg_reviews.MOM`. spd0011 proved (a) the Implementation Contract checkpoint is
obeyed at gpt-5.5/codex (fire-and-obey, the first counter to the detected-but-not-obeyed wall), (b) its
`G2_LATEST_WINDOW_FULL_REFRESH` template solves the latest-window/full-refresh blocker so airbnb001's
REVIEW_TOTALS/REVIEW_SENTIMENT/grain are all gold-exact, and (c) its `G2_REPORT_RAW_GROUPING_HOLD`
template is a net-negative destabilizer that re-grains passers (recharge002 telemetry, then the
quickbooks003 HARD gate) with no compensating flip.

**Single README change (one knob):** fork the champion `spd0008-over-emit-collapse` solver workflow,
carry forward the validated Implementation Contract checkpoint + the `G2_LATEST_WINDOW_FULL_REFRESH`
template, **DROP the `G2_REPORT_RAW_GROUPING_HOLD` template entirely**, and refine the latest-window
template's period-over-period sub-rule from a soft NULL-condition into a hard **derivation-METHOD
constraint**:

> A period-over-period derived column (MoM / YoY / delta / growth-%) in a single-window build must be
> computed as a window function (`LAG`/`LEAD`) **over the built model's OWN output rows**, partitioned
> by the group key and ordered by the window-anchor date — never against a separately re-materialized
> prior-period window queried from the source. When the build emits exactly one window row per group,
> the window function has no prior row and the column is NULL by construction. (Derive the method from
> the window definition; never bake a literal value, count, or NULL flag.)

This mechanically NULLs MoM when the output is a single window — matching gold — without baking the
answer. It mirrors the scaffold's own sibling `models/agg/wow_agg_reviews.sql`, which computes its
week-over-week metric exactly this way (`LAG(REVIEW_TOTALS,6) OVER (PARTITION BY REVIEW_SENTIMENT ORDER
BY AGGREGATION_DATE ASC)`).

This remains README-only: no harness, verifier, runtime, model, fixture, or routing change. The
no-fetch leak guard stays byte-identical; no gold values/counts/dtypes baked. Target query: `airbnb001`
(flip). `apple_store001` is a hold target.

## Pre-smoke Decision-Fork Probe

**This probe is the spd0011 cycle-2 offline gold reconstruction — the left-shift reachability proof,
performed on the LOCAL source only (no network, no fabricated gold).**

- **The fork.** airbnb001's contract correctly drives a single-window `mom_agg_reviews` (3 rows, one
  AGGREGATION_DATE = 2021-10-22, REVIEW_TOTALS/REVIEW_SENTIMENT gold-exact). The ONLY graded residual is
  `MOM` (verifier grades `mom_agg_reviews` cols `[0,1,3]`). Either MoM should be a real percentage
  (worker's choice, both cycles) or NULL (gold's choice). Which, and is it README-reachable?

- **Control result (the champion + spd0011 both produce).** The worker computes MoM by separately
  re-materializing a prior 30-day window from `fct_reviews` (a `previous_window` CTE) and dividing —
  yielding real percentages `MOM = {−17.99, −20.25, −9.92}`. spd0011 FIX A's soft "NULL where the
  baseline is not present in the single window" did NOT stop this: the worker reasoned a prior window IS
  computable from the 2009–2021 source, so it refused to NULL.

- **Gold (reconstructed offline from `_views/spider2-dbt-airbnb001/tests/airbnb.duckdb`).**
  `mom_agg_reviews` = exactly 3 rows, all `AGGREGATION_DATE` 2021-10-22, REVIEW_TOTALS {834, 2745, 4370},
  REVIEW_SENTIMENT {negative, neutral, positive}, **`MOM` (DOUBLE) = NULL for all 3 rows.**
  `dim_listings_hosts` gold = 17,499 rows (worker builds 17,499, 0 mismatch) → not a blocker. Comparator
  (`tests/duckdb_match.py`) = column-containment, `math.isclose(abs_tol=1e-2)`, `NA==NA`; the gold
  `{NULL,NULL,NULL}` MOM vector is not contained in the worker's `{−17.99,−20.25,−9.92}` → mismatch,
  reward 0.0. Confirmed both cycles: MOM is the SOLE residual.

- **Proposed-rule result (verified offline, byte-for-byte == gold).** Applying
  `LAG(REVIEW_TOTALS) OVER (PARTITION BY REVIEW_SENTIMENT ORDER BY AGGREGATION_DATE)` over the exact 3-row
  single-window output yields `MOM = NULL` for negative, neutral, AND positive — identical to gold. So the
  derivation-method constraint mechanically produces the gold MOM without any oracle read or baked value.

- **Why the proxy justifies smoke.** The residual is (1) SINGULAR (one column), (2) REACHABLE (the LAG
  method reproduces gold offline), and (3) README-ADDRESSABLE + oracle-free (the rule names a method, not
  a value; the worker already has the local sibling pattern `wow_agg_reviews`). This is NOT oracle-blind:
  gold MOM=NULL is the mechanical consequence of a LAG over a single-window output, derivable from the
  window definition alone. The open risk is behavioral, not reachability — whether a method-constraint
  README ("use LAG over your own output, do not re-query a prior window") actually steers the worker off
  its prior-window reflex. That is exactly what the smoke tests.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `solver_workflow:`.**
The variant forks `spd0008-over-emit-collapse` and differs only in the README (carry the contract
checkpoint + `G2_LATEST_WINDOW_FULL_REFRESH` with the LAG-method MoM constraint; DROP
`G2_REPORT_RAW_GROUPING_HOLD`). No-fetch leak guard byte-identical; no baked gold. Verified by:
`diff specs/full-baseline.frozen.yaml specs/spd0012-*.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict`,
rc=0, 0 coverage_missing, 0 tainted) on the same run-dir.

**AC-3 — Verdict justified by the committed-artifact read.** `airbnb001` flips iff the committed
`mom_agg_reviews.MOM` column is NULL for all 3 rows (the LAG-over-own-output method reached the
artifact). The hard-gate canaries must hold; with `G2_REPORT_RAW_GROUPING_HOLD` removed, quickbooks003
and recharge002 should NOT be re-grained by a raw-grouping template.

## Smoke Plan

Targeted smoke (mirror the spd0011 panel so the dropped-template effect is observable):

- `airbnb001` — primary flip target (MoM = LAG-over-own-output → NULL).
- `apple_store001` — hold target (raw-key success that spd0008 already passes; must hold WITHOUT the
  raw-grouping template — proves the template was not load-bearing for the hold).

Hard-gate canaries (champion passers that must hold):
`activity001`, `app_reporting001`, `google_play001`, `google_play002`, `quickbooks003` (the spd0011
cycle-2 regression — must RECOVER to 1.0 now that `G2_REPORT_RAW_GROUPING_HOLD` is dropped).

Telemetry-only (reported, not go/no-go): `mrr001`, `mrr002`, `retail001` (known flake), `recharge002`
(must not re-regress with the template gone), `f1003`.

## Expected Outcome

Realistic yield `+1` (airbnb001) with quickbooks003 RECOVERED, IF the LAG-method constraint steers the
worker off its prior-window reflex. The dropped template is the safety win: removing
`G2_REPORT_RAW_GROUPING_HOLD` should un-regress the two cells it destabilized. If airbnb001 still does
not NULL the MOM column despite the method constraint, the residual is a deeper behavioral reflex (the
worker insists on a "real" MoM) and the value-def family is the next escalation, not another template
tweak — conclude `validated-not-promoted` per AC-5 discipline rather than re-tweaking wording.

## Gatekeeper review

(pending — next propose dispatch authors the solver workflow + specs and runs the gatekeeper)

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
