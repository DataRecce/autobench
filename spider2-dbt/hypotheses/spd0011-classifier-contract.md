---
id: spd0011
title: Classifier contract — turn router advice into an enforceable implementation and validation contract
status: hypothesis
kind: hypothesis
source: "post-hypothesis stabilization plan; follows spd0006/spd0008/spd0009 evidence that rules are often detected but not obeyed"
started: 2026-06-26
completed:
verdict:
score: 0.8
worktree:
---

## Hypothesis

The current champion README (`spd0007b-value-def-no-idcast`) has a classifier/router stage, but it
does not force implementation compliance. The solver can correctly identify a rule family and still
produce a noncompliant artifact because the implementation stage has many competing generic rules and
validation mostly accepts a clean `dbt build`.

**Single README change:** upgrade the stage flow from advisory classification to an enforceable
contract:

1. `Classify` produces a provisional router result and names evidence still needed.
2. `Exploration` gathers only the local evidence needed to finalize the contract.
3. A new `Implementation Contract` checkpoint is written before SQL edits.
4. `Implementation` must follow that contract or explicitly revise it.
5. `Validation` must verify the contract signature, not just table existence and build success.

This remains README-only. No harness, verifier, runtime, model, fixture, or multi-worker routing
changes are included.

## Rationale

Prior hypotheses surfaced a consistent compliance failure mode:

- `spd0006` showed that classifier/router advice can fire without producing a reliable task flip.
- `spd0008` showed the over-emit rule was directionally right, but `airbnb001` failed because the
  latest-window filter was left behind `is_incremental()`, so `--full-refresh` emitted full history.
- `spd0009` showed G1 could drive from a spine/dimension without pinning enough row-shape and
  second-blocker detail to pass.

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
- `fallback_if_contract_fails`

The contract must be based only on local workspace evidence.

### Implementation-tip relocation

The variant also restructures the existing implementation-stage tips so they no longer compete with
the classifier output.

Move strategy-selection tips into `Classify` / `Implementation Contract`:

- `PER-KEY METRIC AGGREGATE`
- `COVERAGE / COMPLETENESS`
- `BUILD / RENAME — PRESERVE THE COLUMN SET`
- `TMP/INTERMEDIATE-TIER REMOVAL`
- `FEATURE-BOUNDARY REMOVE / TOGGLE / DISABLE`
- `PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX`

These are classification or contract decisions. They should be selected before SQL edits and become
the contract's skeleton, forbidden pattern, and validation signature.

Keep only calculation recipes in `Implementation`, gated by the contract:

- `EXCLUDE-A-CATEGORY AVERAGE`
- `CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN`
- `TOP-N TIE-CROSSES-CUTOFF`

Move proof requirements into `Validation`:

- row-count and row-shape checks
- grain uniqueness checks
- before/after reconciliation
- full-refresh survival checks
- all target tables exist as base tables
- forbidden patterns were avoided

`TMP/INTERMEDIATE-TIER REMOVAL` is the clearest example: the implementation may inline a model, but
the important proof is before/after reconciliation. That belongs in the contract signature and
validation stage.

### Implementation constraint

Implementation must follow the contract. If the contract proves infeasible, the worker must revise
the contract explicitly before changing strategy.

### Validation constraint

Validation must check the rule-specific signature:

- target tables exist as base tables;
- target names match convention;
- row shape matches the contract;
- grain keys are unique where expected;
- forbidden patterns were avoided;
- every contract target is checked;
- a clean `dbt build` alone is not enough.

## Smoke Plan

Run a targeted smoke only. Do not launch full unless the smoke shows a net improvement.

Targets:

- `airbnb001` — known G2 worker-noncompliance; latest-window filter must survive `--full-refresh`.
- `apple_store001` — known report-grain/raw-key success; should hold if the contract preserves the
  useful part of `spd0008`.
- `salesforce001` — known G1 near-miss; contract should pin daily row shape/date bounds better.
- `jira001` — known G1 row-count fix plus value-definition second blocker; tests whether the contract
  surfaces second blockers before implementation.

Canaries:

- `activity001`
- `mrr001`
- `retail001`
- `recharge001`
- `asset001`

## Acceptance Criteria

**AC-1 — README-only.** The variant differs from the champion solver only in the README. The no-fetch
leak guard remains intact. The smoke spec differs only by experiment, solver workflow, and narrowed
tasks.

**AC-2 — Contract artifact evidence.** For each target, the agent transcript must show an
implementation contract written before SQL edits or before final implementation decisions.

**AC-3 — Smoke score.** Smoke must produce at least one target flip versus the champion baseline with
zero contract-caused canary regressions.

**AC-4 — Compliance attribution.** At least one target outcome must show that validation checked a
rule-specific signature, not only `dbt build`.

**AC-5 — No premature full.** If smoke is 0 target flips, or if any canary regression is attributable
to the contract mechanism, conclude `validated-not-promoted` or revise narrowly. Do not full-run.

## Expected Outcome

Expected realistic yield is `+1` to `+3` if the contract mechanism improves compliance on known
near-misses. The most likely first win is `airbnb001`; the strongest hold target is `apple_store001`.

If the mechanism produces better logs but no target flips, bank the contract idea for the later
autonomous stabilization loop but do not promote it into the champion solver.

## Follow-up If Successful

If the smoke is positive, create a narrowed `spd0011b` or promote to expanded smoke with:

- `airbnb001`
- `apple_store001`
- one or two additional worker-noncompliance tasks from the outcome ledger
- the same regression canaries

Full run should remain a promotion test, not discovery.
