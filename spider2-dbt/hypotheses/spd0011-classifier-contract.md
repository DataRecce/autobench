---
id: spd0011
title: Classifier contract checkpoint — make router advice enforceable without a broad stage rewrite
status: smoke
kind: hypothesis
source: "post-hypothesis stabilization plan; forks current registry baseline spd0008; follows spd0006/spd0008/spd0009 evidence that rules are often detected but not obeyed"
started: 2026-06-26
completed:
verdict:
score: 0.8
worktree:
---

## Hypothesis

The current registry baseline is the `spd0008-over-emit-collapse` solver workflow. It inherits the
`spd0007b-value-def-no-idcast` classifier/router stage and adds G2 over-emit rules, but it still does
not force implementation compliance. The solver can correctly identify a rule family and still
produce a noncompliant artifact because the implementation stage has many competing generic rules and
validation mostly accepts a clean `dbt build`.

**Single README change:** add a narrow contract checkpoint between exploration and SQL edits, and
make validation check that contract. This is a micro-hypothesis, not a broad stage rewrite:

1. `Classify` produces a provisional router result and names evidence still needed.
2. `Exploration` gathers only the local evidence needed to finalize the contract.
3. A new `Implementation Contract` checkpoint is written before SQL edits.
4. `Implementation` must follow that contract or mark it blocked.
5. `Validation` must verify the contract signature, not just table existence and build success.

This remains README-only. No harness, verifier, runtime, model, fixture, or multi-worker routing
changes are included. Moving all existing implementation tips to other stages is explicitly out of
scope for this first smoke.

## Rationale

Prior hypotheses surfaced a consistent compliance failure mode:

- `spd0006` showed that classifier/router advice can fire without producing a reliable task flip.
- `spd0008` showed the over-emit rule was directionally right, but `airbnb001` failed because the
  latest-window filter was left behind `is_incremental()`, so `--full-refresh` emitted full history.
- `spd0009` showed G1 could drive from a spine/dimension without pinning enough row-shape and
  second-blocker detail to pass; however, those G1 cells are not clean first-smoke flip targets.

The expected gain is not a new semantic rule. The expected gain is that already-known rules become
hard enough for the worker to execute and validate.

## Proposed README Mechanics

### Classify output

For every target table, the worker must write:

- target table name
- selected router branch: `R1` through `R6`
- candidate Axis rule: `G1`, `G2`, `G3`, or none
- oracle-free evidence for why the rule fires
- canary/regression risk
- evidence still needed before implementation

### Exploration for contract

Exploration must resolve:

- model naming convention
- materialization defaults
- declared model set
- sibling model patterns
- source table existence
- source row counts, key distributions, and date bounds
- incremental/full-refresh behavior when relevant
- package or missing-source blockers

### Implementation contract

Before editing SQL, the worker must write:

- `selected_rule`
- `target_tables`
- `primary_grain_driver`
- `input_relations`
- `implementation_skeleton`
- `forbidden_patterns`
- `expected_row_shape`
- `validation_signature`
- `contract_blocked_condition`

The contract must be based only on local workspace evidence. `expected_row_shape` and
`validation_signature` must be derived from a named rule template plus local evidence, not invented
freely by the worker.

For this first smoke, the allowed contract template inventory is only:

- `G2_LATEST_WINDOW_FULL_REFRESH`: for targets whose target or sibling model has latest-window logic
  tied to `is_incremental()`. The contract must name the sibling/target model, source date column,
  max-date anchor, window length, expected single-window grain, and the forbidden pattern: leaving the
  required window filter only inside an `is_incremental()` branch.
- `G2_REPORT_RAW_GROUPING_HOLD`: for report-grain targets already passing under the current champion.
  The contract must name the raw grouping column, primary anchor relation, lookup relation if any,
  and the forbidden pattern: regrouping on a canonicalized lookup value instead of preserving the raw
  key.

Any other named template is out of scope for the first smoke.

### Implementation-tip relocation

The long-term proposal restructures existing implementation-stage tips so they no longer compete
with the classifier output. That relocation is **future work**, not part of this first smoke lever.
This hypothesis should only add the contract checkpoint and contract-aware validation. The first
smoke must not move these tips.

Future strategy-selection tips:

- `PER-KEY METRIC AGGREGATE`
- `COVERAGE / COMPLETENESS`
- `BUILD / RENAME — PRESERVE THE COLUMN SET`
- `TMP/INTERMEDIATE-TIER REMOVAL`
- `FEATURE-BOUNDARY REMOVE / TOGGLE / DISABLE`
- `PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX`

These are classification or contract decisions that belong in a later relocation hypothesis.

Future calculation recipes that can remain in `Implementation`:

- `EXCLUDE-A-CATEGORY AVERAGE`
- `CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN`
- `TOP-N TIE-CROSSES-CUTOFF`

Future proof requirements:

- row-count and row-shape checks
- grain uniqueness checks
- before/after reconciliation
- full-refresh survival checks
- all target tables exist as base tables
- forbidden patterns were avoided

`TMP/INTERMEDIATE-TIER REMOVAL` is the clearest example: the implementation may inline a model, but
the important proof is before/after reconciliation. That belongs in a future contract signature and
validation relocation hypothesis.

### Implementation constraint

Implementation must follow the contract. If the contract proves infeasible, the worker must mark
`contract_blocked` with local evidence or return to exploration to fill a missing evidence field. It
may not silently switch to a different selected rule.

### Validation constraint

Validation must check the rule-specific signature:

- target tables exist as base tables;
- target names match convention;
- row shape matches the named rule template plus local evidence captured in the contract;
- grain keys are unique where expected;
- forbidden patterns were avoided;
- every contract target is checked;
- a clean `dbt build` alone is not enough.

## Smoke Plan

Run a targeted smoke only. Do not launch full unless the smoke shows a net improvement against the
current registry baseline.

Targets:

- `airbnb001` — primary flip target; known G2 worker-noncompliance where the latest-window filter
  must survive `--full-refresh`.
- `apple_store001` — known report-grain/raw-key success; should hold if the contract preserves the
  useful part of `spd0008`. Because it already passes in the current registry baseline, it is a hold
  target, not a flip target.

Do not count `salesforce001` or `jira001` as first-smoke success targets. They can be diagnostic cells
later, but prior evidence shows second blockers beyond classifier compliance.

Hard gate canaries, all current-registry-baseline passers that must hold:

- `activity001`
- `app_reporting001`
- `google_play001`
- `google_play002`
- `quickbooks003`

Telemetry-only cells may be reported but do not decide go/no-go because they have known variance or
are not current-registry-baseline passers:

- `mrr001`
- `mrr002`
- `retail001`
- `recharge002`
- `f1003`

## Acceptance Criteria

**AC-1 — README-only.** The variant differs from the champion solver only in the README. The no-fetch
leak guard remains intact. The smoke spec differs only by experiment, solver workflow, and narrowed
tasks.

**AC-2 — Contract artifact evidence.** For each target, the agent transcript must show an
implementation contract written before SQL edits or before final implementation decisions.

**AC-3 — Smoke score.** `airbnb001` must flip versus the current registry baseline by committed
artifact. Every hard gate canary listed in the smoke plan must hold. Telemetry-only cells are
reported separately and never reclassified after the result to rescue or reject the smoke.

**AC-4 — Compliance attribution.** At least one target outcome must show that validation checked a
rule-specific signature derived from a named rule template plus local evidence, not only `dbt build`.

**AC-5 — No premature full.** If `airbnb001` does not flip, or if any stable-passer canary regresses,
conclude `validated-not-promoted` or revise narrowly. Do not full-run.

## Expected Outcome

Expected realistic yield is `+1` if the contract mechanism improves compliance on a known near-miss.
The first-smoke win condition is `airbnb001`; `apple_store001` is a hold target.

If the mechanism produces better logs but no target flips, bank the contract idea for the later
autonomous stabilization loop but do not promote it into the champion solver.

## Follow-up If Successful

If the smoke is positive, create a narrowed `spd0011b` or promote to expanded smoke with:

- `airbnb001`
- `apple_store001`
- one or two additional worker-noncompliance tasks from the outcome ledger
- the same regression canaries

Full run should remain a promotion test, not discovery.

## Gatekeeper review

**Recommendation: APPROVE** — the two refinements (FIX A period-over-period NULL rule on G2_LATEST_WINDOW_FULL_REFRESH; FIX B spine-bound rule on G2_REPORT_RAW_GROUPING_HOLD) are oracle-free derivation rules with explicit "never bake a literal value / count" guards, added in-place to the two existing templates with no relocation, no new template, leak-guard byte-identical, and specs in scope.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-26T00:00:00Z.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | Re-review diff vs champion spd0008 still shows pure-add hunks (`90a91-103`, `269a283-361`, `383a476-493`); no `d`/`c` hunks. This revision added exactly the two named refinements: a "Period-over-period derived columns inside a single-window build" sub-bullet under G2_LATEST_WINDOW_FULL_REFRESH (FIX A) and a "Forbidden: a spine WIDER than the source's observed range" sub-bullet under G2_REPORT_RAW_GROUPING_HOLD (FIX B), plus matching validation_signature lines. Both serve the one idea (enforceable contract); leak-guard untouched. |
| G2 leak-guard (hidden gold) | PASS | Parent README lines 1-30 (no-fetch guard) byte-identical to child. Grep of added lines: every `gold` hit is PROTECTIVE ("never bake a gold count", "never on gold values, expected counts, or external lookup", "rows the gold does not have", "SEPARATE gold rows"). FIX A ends "Derive whether the column is NULL from the window definition + the instruction text; never bake a literal value." FIX B ends "Derive the bound from the source's actual min/max via a local query; never bake a count." No `curl`/`wget`/`git clone`/`ls-remote`/`http`, no `answer_key`/`ground_truth` read. Task-name/value-leak grep (`airbnb`/`recharge`/`122`/`124`) on added lines = zero hits — no "MOM must be NULL for airbnb001", no baked 122/124. |
| G3 spec two fields | PASS | `diff full-baseline.yaml spd0011-classifier-contract.yaml` shows only `experiment:` (→ spd0011-classifier-contract) and `agent.solver_workflow:` (→ ./solver_workflows/spd0011-classifier-contract) changed. `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1` all preserved. |
| G4 smoke narrows tasks only | PASS | `diff` of full vs smoke changes only ABOUTME comments + `experiment:` suffix `-smoke` + `benchmark.tasks:` narrowed to exactly 12: targets airbnb001 (flip) + apple_store001 (hold); hard-gate canaries activity001/app_reporting001/google_play001/google_play002/quickbooks003; telemetry mrr001/mrr002/retail001/recharge002/f1003. No `exclude_tasks` (harbor-local rejects it — positive allowlist is correct). Both hypothesis-named targets present; `trials: 1` preserved. |
| G5 both frozen | PASS | Both `spd0011-classifier-contract.frozen.yaml` (3176B) and `…smoke.frozen.yaml` (1865B) exist (Jun 26 re-freeze). Both carry `agent.kind: spacedock_solver` + `runtime: codex` (lines 4-5). |
| G6 resolver fidelity | PASS | Both refinements match the hypothesis claim and stay generative/independent. FIX A: a derived-NULL rule keyed to "the window definition + the instruction text… UNLESS the task instruction explicitly defines an external comparison baseline" — derivation from local+instruction signal, NOT a self-anchored "confirm your answer matches." FIX B: "BOUNDED to the date/key set the source actually contains (its observed min..max from local evidence)… via a local query" — an independent source-derived bound. The matching validation_signature lines check the BUILT artifact's row set against these derived bounds, authored before the SQL exists. No scope creep, no baked oracle. |
| G7 actionability/inert-risk | WARN | Both refinements are concrete (FIX A names a literal forbidden behavior — "do NOT compute it against out-of-window source rows"; FIX B names a literal local query — "the source's actual min/max"), which lands better than abstract prose. But the host lever remains a process/discipline checkpoint, and spider2-dbt's recurring mode is "rule detected but not obeyed." The prior smoke proved the contract stage is NOT inert (AC-2/AC-4 satisfied; FIX A's exact gap — worker computed real MoM where gold=NULL — is the value-def hole this revision now targets). Judge the smoke by committed-artifact, not transcript mention. WARN-only; does not move the recommendation. |
| G8 regression-canary coverage | PASS | The two templates are precondition-gated (fire only on targets whose model/sibling carries the named structure; non-matching → `selected_rule: none`, existing guidance unchanged). The contract/validation stages are generative, so the smoke carries the 5 hard-gate non-target @baseline passers (activity001/app_reporting001/google_play001/google_play002/quickbooks003) plus apple_store001 as a perturbable raw-grouping hold and recharge002 (telemetry) as the previously-regressed spine cell FIX B directly addresses — ≥2 perturbable canaries on the at-risk raw-grouping/spine family present. |
| G9 selector independence | N/A | No multi-candidate / N-of-K selector protocol; the contract is a single per-target plan, not competing candidates scored against each other. |
| G10 self-correcting false-positive | PASS | The validation_signature is a check-and-fix-or-block lever, so G10 applies. (a) Scope: gated to targets that adopted a template; `none` targets fall through. (b) Independence: FIX A/FIX B signature checks are STRUCTURAL invariants of the built artifact ("any period-over-period derived column is NULL where no in-window prior period exists (matches the window definition)"; "the zero-filled spine's row set equals the bounded source date/key set… not an unbounded calendar"), derived from the template + local evidence before the SQL exists — not a re-run of the solver's own derivation, so no correlated false-green. (c) Check-don't-replace: on failure says "fix it or mark `contract_blocked` with local evidence" — investigate/block, not mandated value-rewrite. |

**For the captain:** No FAILs → APPROVE; auto-advance to smoke. The leak-guard ask is satisfied: FIX A is a derive-from-window+instruction NULL rule (explicit "never bake a literal value", no "MOM must be NULL for airbnb001"), FIX B is a derive-from-source-min/max bound (explicit "never bake a count", no 122/124), and grep finds zero task-name/count leaks in the added lines. The one WARN (G7) is the standing process-checkpoint inert-risk — but the prior smoke already proved the stage fires-and-is-obeyed, so the real test is whether FIX A actually closes the airbnb001 MoM-NULL gap and FIX B holds recharge002 at the source-bounded grain; judge both by committed artifact (AC-2/AC-4), not log mentions.

## Stage Report: propose

- DONE: Fork the champion solver: cp -r solver_workflows/spd0008-over-emit-collapse solver_workflows/spd0011-classifier-contract
  Forked; pre-edit diff -r was identical.
- DONE: Edit ONLY solver_workflows/spd0011-classifier-contract/README.md to add the narrow Implementation Contract checkpoint + contract-aware validation per the hypothesis Proposed README Mechanics (one knob)
  3 purely-additive hunks (90a91-103 Classify output, 269a283-349 Exploration-resolve + new Implementation Contract stage, 383a464-477 Validation signature); no deletions.
- DONE: Keep the no-external-reference / leak-guard prose byte-intact; embed no gold values, dtypes, counts, or row numbers
  Lines 1-30 byte-identical to parent; all added "gold" mentions are protective; expected_row_shape/validation_signature explicitly worker-derived from template + local evidence.
- DONE: Do NOT relocate or delete any existing implementation-stage tips (relocation is explicit future work, out of scope for this smoke)
  All 6 tips intact in the Implementation stage; diff shows zero d/c hunks.
- DONE: Create full spec: cp specs/full-baseline.frozen.yaml ... then set experiment + solver_workflow (no other field changes)
  Built from full-baseline.yaml (editable source); experiment: spd0011-classifier-contract, solver_workflow: ./solver_workflows/spd0011-classifier-contract.
- DONE: Create smoke spec ... so ONLY these survive: airbnb001, apple_store001, activity001, app_reporting001, google_play001, google_play002, quickbooks003 (+ telemetry mrr001, mrr002, retail001, recharge002, f1003)
  Positive benchmark.tasks allowlist of exactly 12 dataset names (harbor-local rejects exclude_tasks as extra_forbidden, so positive allowlist is the proven pattern).
- DONE: Freeze both
  Wrote spd0011-classifier-contract.frozen.yaml and .smoke.frozen.yaml.
- DONE: Verify smoke selection via --explain
  rk run ... --explain reports Tasks: 12, solver_workflow resolves to solver_workflows/spd0011-classifier-contract.
- DONE: Confirm full-spec diff vs full-baseline.frozen.yaml shows ONLY experiment: + solver_workflow: changed
  Only authored changes are experiment + solver_workflow; remaining diffs (solver_workflow_content_hash, solver_workflow_hash, sealed_hash, harness_git_sha) are auto-derived freeze provenance.
- DONE: Run the gatekeeper review subagent and write a ## Gatekeeper review block
  Appended; overall APPROVE (no FAILs; one G7 WARN = process-checkpoint inert-risk).

### Summary

Forked champion spd0008-over-emit-collapse into spd0011-classifier-contract and made the single one-knob README change: added per-target Classify output fields, an Exploration-for-contract evidence-resolution list, a new pre-SQL Implementation Contract checkpoint (9 named fields + a 2-template inventory: G2_LATEST_WINDOW_FULL_REFRESH and G2_REPORT_RAW_GROUPING_HOLD), and a contract-signature Validation check. The diff is purely additive; existing implementation tips and the no-fetch leak-guard are untouched, no gold baked in. Full spec diffs only experiment + solver_workflow; smoke is a 12-task positive allowlist (--explain confirms Tasks: 12). Gatekeeper recommends APPROVE with one G7 WARN (judge the smoke by AC-2/AC-4 committed-artifact evidence, not transcript mentions). Stopped at the propose gate; no rk run launched beyond $0 --explain.

## Smoke result

Run dir: `runs/spd0011-classifier-contract-smoke/1e6a6226d63abfbb` (strict audit CLEAN, rc=0,
`0 coverage_missing`, `0 tainted`). 10/12 cells pass.

**Verdict: NO-GO.** The primary flip target `airbnb001` did NOT flip (0.0, same as `@baseline`), and a
telemetry cell `recharge002` regressed 1.0→0.0 by a lever-attributable construction divergence. Per AC-5,
do not full-run; conclude `validated-not-promoted` or revise narrowly. The hard-gate panel held cleanly.

| Cell | Role | @baseline (spd0008) | spd0011 | Flip? | Distance / why |
|------|------|--------------------|---------|-------|----------------|
| airbnb001 | FLIP target | 0.0 | 0.0 | NO | Closer-but-still-fail. Window logic now CORRECT (totals match gold exactly); residual blocker = `MOM` column: gold=NULL, worker computed real MoM %. See Behavioral analysis. |
| apple_store001 | HOLD target | 1.0 | 1.0 | held | `G2_REPORT_RAW_GROUPING_HOLD` preserved the spd0008 raw-key win. |
| activity001 | hard-gate canary | 1.0 | 1.0 | held | |
| app_reporting001 | hard-gate canary | 1.0 | 1.0 | held | |
| google_play001 | hard-gate canary | 1.0 | 1.0 | held | |
| google_play002 | hard-gate canary | 1.0 | 1.0 | held | |
| quickbooks003 | hard-gate canary | 1.0 | 1.0 | held | |
| mrr001 | telemetry | 1.0 | 1.0 | held | |
| mrr002 | telemetry | 1.0 | 1.0 | held | |
| retail001 | telemetry | 1.0 | 1.0 | held | |
| f1003 | telemetry | 1.0 | 1.0 | held | |
| recharge002 | telemetry | 1.0 | 0.0 | REGRESSED | Lever-attributable: `G2_REPORT_RAW_GROUPING_HOLD` + spine/coalesce skeleton steered the worker into a fuller calendar spine (124 rows vs champion's passing 122). See Behavioral analysis. |

**Clean-audit attestation:** strict audit clean, rc=0, no dataset errored, no infra taint. Backend N/A
(harbor-local DuckDB, file-graded). The two failures are real artifact mismatches, not infra abstains.

**AC scorecard:**
- AC-1 (README-only): satisfied at propose (gatekeeper PASS).
- AC-2 (contract written before SQL edits): **SATISFIED** — airbnb001 contract written 08:33:05Z,
  first `apply_patch` 08:33:47Z; recharge002 contract written 08:57:22Z before its edits. Full 9-field
  contracts present for every target. The contract stage is NOT inert.
- AC-3 (airbnb001 flips + canaries hold): **FAILED on the flip** — airbnb001 did not flip. Canaries held.
- AC-4 (validation ran a template-derived signature beyond `dbt build`): **SATISFIED** — both workers ran
  direct DuckDB structural checks (base-table type, grain uniqueness, single-AGGREGATION_DATE,
  representative rows) beyond the clean build. But the signature is oracle-blind on the residual blocker
  (see Failure Review).
- AC-5 (no premature full): honored — NO-GO, no full launched.

## Behavioral analysis

### airbnb001 — closer-but-still-failing (committed-artifact read)

Graded tables + columns (from `tests/spider2_eval.jsonl`):
- `dim_listings_hosts` cols [2,3,4,5,6,7,8] (LISTING_ID…HOST_NAME), order-insensitive — worker built
  17,499 rows = gold 17,499; not the blocker.
- `mom_agg_reviews` cols [0,1,3] = REVIEW_TOTALS, REVIEW_SENTIMENT, MOM, order-insensitive.

The contract (written pre-edit) selected `G2_LATEST_WINDOW_FULL_REFRESH` for `mom_agg_reviews` and
correctly predicted "3 rows for 2021-10-22", "exactly one AGGREGATION_DATE", and forbade "window filter
solely inside `is_incremental()`". The committed `models/agg/mom_agg_reviews.sql` applies the latest-window
filter **UNCONDITIONALLY** (a `dates_cte` anchored to `MAX(REVIEW_DATE)` + `WHERE … BETWEEN
AGGREGATION_DATE-29 AND AGGREGATION_DATE`), with **no `is_incremental()` gate anywhere**. So the
`is_incremental`/full-refresh blocker that the hypothesis (via spd0008's diagnosis) targeted was already a
non-issue at this draw — the contract template solved its targeted problem.

The worker's built `mom_agg_reviews` matched gold on the two columns the template reasons about:
REVIEW_TOTALS = {neg 834, neu 2745, pos 4370}, REVIEW_SENTIMENT exact, exactly 3 rows, single date
2021-10-22 (verified: gold totals reproduce the inclusive 30-day window through `fct_reviews`, which dedups
the 6-row raw discrepancy and drops the NULL-sentiment group). The **sole residual graded mismatch is the
`MOM` column (col 3): gold = NULL for all 3 rows; the worker computed real MoM percentages (−17.99 / −20.25
/ −9.92)**. Because the verifier ANDs all condition_tabs, this one column fails the whole cell.

The template's vocabulary (latest-window grain, full-refresh survival, single-date anchor) does not contain
the MoM semantics. Gold defines MOM as NULL here (no comparable prior-period value in the gold definition);
the worker's `previous_window` 30–59-day-prior CTE manufactured a non-null comparison gold does not want.
This is a **second blocker outside the contract template** — a value/semantics definition, not a compliance
or grain failure. The contract made airbnb001 strictly closer (window correct, totals/sentiment/grain all
gold-exact) but cannot reach the answer because its template has no MoM-definition lever.

### recharge002 — lever-attributable regression (committed-artifact read)

Graded table `recharge__customer_daily_rollup`, cols [0, 37], order-insensitive. Champion spd0008 (PASS,
1.0) built it in ONE model at **122 rows**. The spd0011 worker selected `G2_REPORT_RAW_GROUPING_HOLD` and,
following the contract's `implementation_skeleton` ("left join daily metrics onto the customer-date spine,
coalesce absent daily counts/amounts to 0"), added a NEW `models/intermediate/int_recharge__calendar_spine.sql`
that "included the max charge day in the spine" → **124 rows**. The 2-row spine expansion changes the graded
row set, breaking the match. The divergence traces directly to the contract's spine/coalesce skeleton +
template selection, NOT to pre-existing variance — this is the generative contract stage perturbing a
previously-passing construction. recharge002 is telemetry-only (not a hard gate), so it does not by itself
decide the go/no-go, but it is recorded as lever-caused regression evidence, not flake.

## Failure Review

**Primary failure type: correct-artifact-still-fail** (airbnb001), with a secondary
**lever-attributable canary-style regression** on a telemetry cell (recharge002).

1. **Original fork (what the hypothesis bet on):** airbnb001 fails because the latest-window filter is left
   behind `is_incremental()`, so `--full-refresh` emits full history (the spd0008 diagnosis). The contract's
   `G2_LATEST_WINDOW_FULL_REFRESH` template would force the filter to survive full-refresh and flip the cell.

2. **Fork the artifact revealed:** that blocker was already gone at this draw — the worker applied the window
   UNCONDITIONALLY (no `is_incremental` gate) and produced gold-exact REVIEW_TOTALS/REVIEW_SENTIMENT, 3 rows,
   single date. The TRUE residual blocker is the **`MOM` column value definition**: gold MOM = NULL, worker
   computed a real prior-window MoM %. This is a value/semantics fork the 2-template inventory does not cover.

3. **Did the rule fire, and what does the artifact show?** YES — fired and was obeyed (refutes the G7
   "detected-but-not-obeyed" worry for THIS draw). AC-2 met: a full 9-field contract was written before SQL
   edits (08:33:05Z contract vs 08:33:47Z first patch); the committed SQL implements exactly the contract
   skeleton; AC-4 met: validation ran direct DuckDB structural checks beyond `dbt build`. The contract was
   the OPPOSITE of inert — it changed behavior, made airbnb001 strictly closer, and (on recharge002) changed
   behavior enough to regress a passer. The wall is not compliance; it is that the template's structural
   signature is oracle-blind to the MoM-definition gap (the worker's own validation_signature "current totals
   equal latest 30-day fact counts" passed truthfully while the graded MOM column was wrong).

4. **New fork to test next:** airbnb001's real lever is a **MoM-definition / value-semantics** contract field
   (when is MOM NULL? what prior period?), NOT a window-compliance template. This is a value-def fork
   (kin to spd0007's value-definition family), not a G2 latest-window fork. Separately, the
   `G2_REPORT_RAW_GROUPING_HOLD` spine/coalesce skeleton needs a forbidden-pattern guard against
   **expanding the calendar spine beyond the champion's grain** (recharge002: 124 vs 122) — a spine that
   zero-fills must be bounded to the same date set the passing construction used.

5. **Next step: file (do not promote, do not probe-rerun).** Conclude `validated-not-promoted`. The contract
   mechanism is VALIDATED as fire-and-obey (banks the AC-2/AC-4 evidence that the contract stage is not inert
   at gpt-5.5/codex), but it does not flip airbnb001 and it regresses recharge002, so it is net-negative as a
   standalone promotion. Bank the contract idea + the two refinements (a value-def/MoM template; a spine-grain
   forbidden-pattern) for the later stabilization loop. No re-run needed — the artifact read is decisive.

## Stage Report: smoke

- DONE: Read the airbnb001 cell sub-agent session jsonl and extract the FINAL committed dbt model SQL and the Implementation Contract the worker wrote
  Reconstructed final `models/agg/mom_agg_reviews.sql`, `daily_agg_reviews.sql`, `dim_listings_hosts.sql` from codex `apply_patch` events; full 9-field contract quoted in Behavioral analysis.
- DONE: Determine AC-2: was an Implementation Contract written BEFORE the SQL edits
  YES. Contract msg 08:33:05Z; first apply_patch 08:33:47Z. selected_rule=G2_LATEST_WINDOW_FULL_REFRESH; forbidden_patterns include "no window filter solely inside is_incremental()"; expected_row_shape="3 rows for 2021-10-22"; validation_signature="exactly one AGGREGATION_DATE, unique DATE_SENTIMENT_ID, current totals equal latest 30-day fact counts".
- DONE: Determine AC-4: did Validation run a rule-specific signature check beyond dbt build?
  YES. Worker ran direct DuckDB checks (base-table type, grain uniqueness, single AGGREGATION_DATE, representative rows) beyond the 39/39 clean build.
- DONE: Determine the airbnb001 failure mechanism
  Window filter is UNCONDITIONAL (survives --full-refresh, no is_incremental gate). REVIEW_TOTALS/REVIEW_SENTIMENT gold-exact (834/2745/4370, 3 rows). SECOND blocker = MOM column (graded col 3): gold=NULL, worker computed real MoM %. Verified by reproducing gold totals from fct_reviews + gold mom_agg_reviews dump.
- DONE: Classify the airbnb001 result
  closer-but-still-failing (window solved; residual = MOM value-definition mismatch, a fork outside the template inventory).
- DONE: Check recharge002 drop, classify lever vs flake
  Lever-attributable regression. Worker chose G2_REPORT_RAW_GROUPING_HOLD + added int_recharge__calendar_spine → 124 rows vs champion's passing 122. Spine/coalesce skeleton from the contract drove the divergence, not variance.
- DONE: Confirm apple_store001 HOLD and the 5 hard-gate canaries held
  apple_store001=1.0; activity001/app_reporting001/google_play001/google_play002/quickbooks003 all 1.0. Noted in Smoke result table.
- DONE: Write the ## Smoke result block
  Per-target flip/distance/why table + clean-audit attestation + AC scorecard appended.
- DONE: Write the ## Behavioral analysis block
  Committed-artifact read for airbnb001 (MOM blocker) and recharge002 (spine row-set divergence) appended.
- DONE: Write the ## Failure Review block
  Primary type correct-artifact-still-fail; 5 required questions answered; next step = file (validated-not-promoted).
- DONE: Workflow-refinement evaluation (MANDATORY — new contract STAGE)
  Appended spd0011 entry to _artifacts/WORKFLOW-REFINE.md (the contract stage fired + was obeyed on all 12 cells, not inert; changed artifacts; helped airbnb001 closer, harmed recharge002).
- DONE: Do NOT change verdict/frontmatter or promote; commit entity + WORKFLOW-REFINE edits
  No frontmatter/verdict touched, no rk run. Commit below.

### Summary

NO-GO confirmed by committed-artifact read. The Implementation Contract stage is NOT inert (AC-2/AC-4 both
satisfied: contract written pre-edit, obeyed in the committed SQL, validation ran a structural signature) —
refuting the G7 detected-but-not-obeyed worry for this draw. But airbnb001 does not flip: the contract's
G2_LATEST_WINDOW_FULL_REFRESH template solved the window/full-refresh blocker (totals + sentiment + grain
now gold-exact), revealing the TRUE residual blocker is the MOM column value-definition (gold NULL vs
worker-computed MoM %), which is outside the template inventory. recharge002 regressed 1.0→0.0 by a
lever-attributable spine expansion (124 vs the champion's passing 122 rows). Net standalone = negative.
Recommend conclude validated-not-promoted; bank the contract idea + two refinements (a value-def/MoM
template; a spine-grain forbidden-pattern) for the stabilization loop.

## Revise Note (propose cycle 2, 2026-06-26)

Refined the two EXISTING contract templates with the two banked smoke fixes (no new template, no
relocation, leak-guard untouched):
- **FIX A (G2_LATEST_WINDOW_FULL_REFRESH):** added a period-over-period derived-metric NULL-condition
  requirement — a MoM/YoY/delta/growth-% column must be NULL where its comparison baseline is not
  present in the single built window (derive NULL-ness from the window definition + instruction text,
  never bake a value), plus a matching `validation_signature` check. Targets the airbnb001 residual
  (gold MOM=NULL vs worker-computed real MoM %, the second blocker the window template was oracle-blind to).
- **FIX B (G2_REPORT_RAW_GROUPING_HOLD):** added a forbidden-pattern + `validation_signature` check that
  a zero-filled spine must be BOUNDED to the source's observed min..max (via a local query), never a
  fuller/standalone calendar. Targets the recharge002 regression (unbounded calendar spine → 124 rows vs
  the champion's passing source-bounded grain).
Re-froze BOTH specs (solver_workflow_hash `80f047…` → `d1ac7c…` in both .frozen.yaml). Gatekeeper
re-review = APPROVE (one standing G7 WARN). FO owns the re-smoke launch.

## Stage Report: propose (cycle 2)

- DONE: Edit solver_workflows/spd0011-classifier-contract/README.md ONLY: refine the two existing contract templates with the two banked fixes
  3 in-place additive sub-edits; no new template, no relocation, leak-guard byte-identical (diff lines 1-30 exit 0).
- DONE: Fix A on G2_LATEST_WINDOW_FULL_REFRESH: derived-metric NULL-condition requirement + matching validation_signature check (general, oracle-free, no baked value)
  Added "Period-over-period derived columns inside a single-window build" sub-bullet + a NULL-where-no-in-window-prior-period validation_signature line; ends "never bake a literal value".
- DONE: Fix B on G2_REPORT_RAW_GROUPING_HOLD: spine-grain forbidden-pattern + matching validation_signature check (general, oracle-free)
  Added "Forbidden: a spine WIDER than the source's observed range" sub-bullet + a spine-row-set-equals-source-bounded-min..max validation_signature line; ends "never bake a count".
- DONE: Re-freeze BOTH specs
  rk freeze --allow-missing on both full + smoke; both wrote .frozen.yaml.
- DONE: Verify the solver_workflow_hash changed in both .frozen.yaml files
  Both 80f047515712… → d1ac7cf69e3e… (content_hash == solver_workflow_hash, identical across full + smoke as expected).
- DONE: Re-verify smoke selection via --explain
  rk run …smoke.frozen.yaml --explain → Tasks: 12, content_hash resolves to d1ac7c….
- DONE: Confirm leak-guard byte-intact and full-spec frozen diff still only experiment: + solver_workflow: (+ auto hashes)
  Leak-guard lines 1-30 diff exit 0; full frozen diff = experiment + solver_workflow + 4 auto hashes (content_hash, sealed_hash, harness_git_sha, solver_workflow_hash) only.
- DONE: Re-run the gatekeeper review subagent; replace the ## Gatekeeper review block with the new verdict
  Replaced; APPROVE, G2 PASS (zero task-name/count leak on added lines), one standing G7 WARN.
- DONE: Append a one-line revise note recording what changed and why
  Added ## Revise Note (propose cycle 2) above.
- SKIPPED: Launch any rk run beyond $0 --explain
  Per assignment — FO owns the re-smoke launch.

### Summary

Refined the two existing contract templates with the two banked smoke fixes: FIX A adds an oracle-free
period-over-period derived-metric NULL-condition (targets the airbnb001 MOM=NULL residual) and FIX B adds
an oracle-free source-bounded-spine forbidden-pattern (targets the recharge002 unbounded-spine regression),
each with a matching validation_signature check. No new template, no relocation, leak-guard byte-intact.
Re-froze both specs (solver_workflow_hash changed 80f047…→d1ac7c… in both); smoke --explain confirms
Tasks: 12. Gatekeeper re-review = APPROVE (one standing G7 WARN). No rk run beyond --explain; FO owns the
re-smoke.
