---
id: spd0011
title: Classifier contract checkpoint — make router advice enforceable without a broad stage rewrite
status: hypothesis
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
