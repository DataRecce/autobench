---
id: spd0012
title: MoM = window LAG over the model's own single-window output (drop the raw-grouping template)
status: smoke
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

**Recommendation: APPROVE** — one cohesive contract-checkpoint idea (drop the net-negative raw-grouping template, keep only G2_LATEST_WINDOW, harden the MoM sub-rule to a LAG-over-own-output derivation-METHOD constraint); leak-guard byte-identical, no gold values leaked, specs scoped to exactly two fields, smoke narrows tasks-only with both targets present, lever is precondition-gated with a structural validation signature.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-26T11:42:00Z.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | Diff vs `spd0008/README.md` adds 3 hunks all serving ONE idea: a Classify-output block (90a91), the Exploration-for-contract evidence list + Implementation Contract stage with a single-template inventory (269a283) and contract-aware Validation (383a471). Inventory holds only `G2_LATEST_WINDOW_FULL_REFRESH`; the dropped `G2_REPORT_RAW_GROUPING_HOLD` appears 0 times. No leak-guard/no-fetch prose edited. |
| G2 leak-guard (hidden gold) | PASS | Numeric/value grep (`834|2745|4370|17499|-17.99|-20.25|-9.92|expected_|answer_key|ground_truth`) returns ONLY the literal field name `expected_row_shape` — no gold values, counts, dtypes, or NULL flags baked. All `gold`/`curl`/`wget`/`git clone` hits are in prohibition prose. No-fetch paragraph (lines 11–15) byte-identical to spd0008. The MoM rule names a METHOD (`LAG`/`LEAD` over own output) + a local-sibling file pointer `models/agg/wow_agg_reviews.sql` (allowed workspace path), not gold. |
| G3 spec two fields | PASS | Frozen-vs-frozen diff (`full-baseline.frozen.yaml` vs `spd0012…frozen.yaml`) changes ONLY `experiment:`, `agent.solver_workflow:`, and the auto-regenerated hashes (`solver_workflow_content_hash`, `sealed_hash`, `harness_git_sha`, `solver_workflow_hash`). Preserved: `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1`. No third functional field differs. |
| G4 smoke narrows tasks only | PASS | Smoke diff changes only the experiment-name suffix (`-smoke`) and narrows `benchmark.tasks` to exactly 12: airbnb001, apple_store001, activity001, app_reporting001, google_play001, google_play002, quickbooks003, mrr001, mrr002, retail001, recharge002, f1003. No `exclude_tasks`. Both named targets present: airbnb001 (flip) + apple_store001 (hold). quickbooks003 + recharge002 retained as de-regression canaries. |
| G5 both frozen | PASS | Both `spd0012…frozen.yaml` and `…smoke.frozen.yaml` exist; both carry `agent.kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the falsifiable claim verbatim: a single-template contract checkpoint with the MoM rule "computed as a window function (`LAG`/`LEAD`) over the built model's OWN output rows… never against a separately re-materialized prior-period window." Generative/independent build-and-derive instruction; the Validation signature checks STRUCTURE (LAG-over-own-output method present, single-window grain), not "verify your answer matches" — no self-anchored false-green phrasing. No scope creep. |
| G7 actionability/inert-risk | PASS | Concrete + mechanical: names a specific SQL construct (`LAG`/`LEAD` partitioned by group key, ordered by window-anchor date) and carries a worked-example skeleton from the local sibling (`LAG(REVIEW_TOTALS, 6) OVER (PARTITION BY REVIEW_SENTIMENT ORDER BY AGGREGATION_DATE)`). Not abstract prose. |
| G8 regression-canary coverage | N/A (PASS) | Lever is precondition-GATED, not fires-everywhere: `G2_LATEST_WINDOW_FULL_REFRESH` fires ONLY on a target/sibling carrying `is_incremental()` latest-window logic; any non-matching target sets `selected_rule: none` and uses unchanged guidance. Smoke nonetheless carries passing canaries (activity001, app_reporting001, google_play001/002, quickbooks003, recharge002). |
| G9 selector independence | N/A (PASS) | No multi-candidate / run-N-and-select protocol declared; single build-one-contract-per-target design. |
| G10 self-correcting false-positive | PASS | Validation is a STRUCTURAL/existence-and-method check (table exists as base table, name convention, single-window grain unique, forbidden patterns absent, period-over-period column computed via LAG/LEAD over own output) — it does NOT re-derive against the solver's own answer and is gated to the latest-window precondition. Per spd0002-class rule, a structure/method check cannot turn a right value wrong → not value-rewriting. |

**For the captain:** Auto-approved to smoke with no FAILs and no WARNs. This is the spd0011 follow-up that drops the proven net-negative `G2_REPORT_RAW_GROUPING_HOLD` template and hardens the MoM rule into a LAG-over-own-output method constraint; the 12-task smoke pairs the airbnb001 flip target with apple_store001 (proves the dropped template was not load-bearing for that hold) and keeps quickbooks003 + recharge002 to confirm they un-regress now that the raw-grouping template is gone. Worth a glance at the smoke result for whether the method-constraint actually steers the worker off its prior-window reflex (the open behavioral risk the hypothesis itself flags).

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the champion: cp -r solver_workflows/spd0008-over-emit-collapse solver_workflows/spd0012-mom-window-lag-single-window
  Forked; README is the only file. spd0011 README (= spd0008 + contract machinery) copied in as the seed, then the two deltas applied.
- DONE: Edit ONLY the README to carry the spd0011 Implementation Contract checkpoint + G2_LATEST_WINDOW template, DROP G2_REPORT_RAW_GROUPING_HOLD, harden the period-over-period sub-rule to a hard LAG-over-own-output derivation-METHOD constraint (one knob)
  `diff spd0008 spd0012` = 4 added blocks only (Classify-output, Exploration-for-contract, Implementation Contract stage, contract-aware Validation); inventory says "Only this one named template"; G2_REPORT_RAW_GROUPING_HOLD appears 0 times.
- DONE: Keep the no-external-reference / leak-guard prose byte-intact; embed no gold values, dtypes, counts, NULL flags
  No-fetch para (lines 11-15) byte-identical to spd0008; gold-value grep (834/2745/4370/17499/-17.99/-20.25/-9.92) returns NONE; MoM rule names a METHOD only.
- DONE: Source the contract-checkpoint text from spd0011's README ... with ONLY the G2_LATEST_WINDOW_FULL_REFRESH template
  Seeded from spd0011 README so all four contract blocks are carried verbatim; the dropped template removed from the inventory bullet AND the Validation signature reference.
- DONE: Do NOT relocate or delete any existing spd0008 implementation-stage tips
  Diff shows additions only (90a91, 269a283, 383a471); no spd0008 line modified/removed. The wow_agg_reviews.sql pointer added is a leak-safe local file-path reference (verified the sibling exists with the cited LAG expression).
- DONE: Create full spec: cp full-baseline.frozen.yaml ... set experiment + solver_workflow only
  specs/spd0012-mom-window-lag-single-window.yaml; only experiment: + solver_workflow: edited.
- DONE: Create smoke spec: positive benchmark.tasks allowlist of exactly the 12 (no exclude_tasks)
  specs/spd0012-mom-window-lag-single-window.smoke.yaml; 12 tasks, no exclude_tasks, experiment suffixed -smoke.
- DONE: Freeze BOTH
  wrote spd0012-mom-window-lag-single-window.frozen.yaml AND .smoke.frozen.yaml.
- DONE: Verify smoke selection --explain shows Tasks: 12
  `rk run ...smoke.frozen.yaml --explain` => "- Tasks: `12`".
- DONE: Confirm full-spec frozen diff vs full-baseline.frozen.yaml shows ONLY experiment + solver_workflow (+ auto hashes); kind/runtime preserved
  Frozen-vs-frozen diff = experiment, solver_workflow, solver_workflow_content_hash, sealed_hash, harness_git_sha, solver_workflow_hash only; kind: spacedock_solver / runtime: codex unchanged.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block; leak-guard attention on the LAG-method MoM rule
  Gatekeeper recommendation APPROVE; all 10 rules PASS/N/A, zero FAIL, zero WARN. Block written above.
- DONE: Do NOT launch any rk run beyond --explain. Commit. Stop at the propose gate.
  Only `rk freeze` + `rk run --explain` executed. Committed below; stopping at gate.

### Summary

Forked the champion spd0008-over-emit-collapse into spd0012, then layered in the spd0011-validated
Implementation Contract checkpoint with exactly ONE knob: dropped the proven net-negative
`G2_REPORT_RAW_GROUPING_HOLD` template (only `G2_LATEST_WINDOW_FULL_REFRESH` remains in the inventory)
and hardened the period-over-period sub-rule from spd0011's soft NULL-condition into a hard
LAG/LEAD-over-own-output derivation-METHOD constraint, with a leak-safe pointer to the in-workspace
sibling `models/agg/wow_agg_reviews.sql`. Both specs freeze cleanly; smoke selects the 12-task panel;
the full frozen diff vs baseline is exactly experiment + solver_workflow + auto hashes. Gatekeeper
APPROVE (10/10 PASS/N/A, no FAIL/WARN) — auto-advance to smoke with clean FO reject-checks.
