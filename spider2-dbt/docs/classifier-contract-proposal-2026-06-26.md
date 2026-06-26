# Classifier Contract Proposal

Date: 2026-06-26

## Context

The current champion solver workflow is `spd0007b-value-def-no-idcast`. It has a
`Classify (router)` stage, but the classifier currently acts mostly as advice:
it chooses router branches and names gated rules, while the later implementation
stage still carries many independent dbt rules and patterns.

Recent experiments show a repeated failure mode:

- the classifier or README rule identifies the right family;
- the implementation worker builds a plausible dbt artifact;
- the artifact does not follow the rule tightly enough to pass;
- validation accepts a clean `dbt build` even when the rule-specific shape is
  visibly wrong.

Examples:

- `airbnb001`: the latest-window rule was present, but the worker left the
  filter behind an `is_incremental()` branch, so `--full-refresh` emitted full
  history.
- `salesforce001`: the spine/completeness direction produced a table, but the
  row-shape contract was not strong enough to force the correct date range.
- `jira001`: G1 fixed the row count, but a second value-definition gap remained.

The next solver improvement should make the classifier output enforceable by the
implementation and validation stages.

## Proposal

Do not route directly from `Classify` to `Implementation`. Instead, split the
current loose flow into:

1. `Classify`
2. `Exploration for Contract`
3. `Implementation Contract`
4. `Implementation`
5. `Validation`
6. `Finalization`

This is still a README-only solver change. It does not require harness changes or
multiple workers.

## Stage Responsibilities

### Classify

The classifier remains a router. It should produce a provisional classification,
not a final implementation instruction.

Required output:

- target table list
- router branch for each target: `R1` through `R6`
- candidate Axis rule family: `G1`, `G2`, `G3`, or none
- why the rule fires, using oracle-free evidence
- likely canary/regression risk
- evidence still needed before implementation

### Exploration for Contract

Exploration becomes contract-directed. It should gather only the local evidence
needed to make the contract concrete.

Required probes:

- project naming convention and target table names
- materialization defaults
- schema YAML declarations
- existing sibling model patterns
- source table existence
- source row counts and key distributions
- date bounds when date windows/spines are involved
- incremental/full-refresh behavior when relevant
- package or missing-source blockers

### Implementation Contract

After exploration, the worker must write an explicit contract before editing SQL.

Required fields:

- `selected_rule`
- `target_tables`
- `primary_grain_driver`
- `input_relations`
- `implementation_skeleton`
- `forbidden_patterns`
- `expected_row_shape`
- `validation_signature`
- `fallback_if_contract_fails`

The contract must be derived from local workspace evidence, not hidden gold.

### Implementation Tip Relocation

The current implementation stage carries many generic tips. Under the contract
design, those tips should no longer compete with the classifier output at
implementation time. They should be redistributed by role.

Move classification-shaped tips into `Classify` / `Implementation Contract`:

- `PER-KEY METRIC AGGREGATE`
- `COVERAGE / COMPLETENESS`
- `BUILD / RENAME -- PRESERVE THE COLUMN SET`
- `TMP/INTERMEDIATE-TIER REMOVAL`
- `FEATURE-BOUNDARY REMOVE / TOGGLE / DISABLE`
- `PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX`

These decide which strategy applies. They should be selected before SQL edits
and converted into the contract's `selected_rule`, `implementation_skeleton`,
`forbidden_patterns`, and `validation_signature`.

Keep only calculation-shaped recipes in `Implementation`, and make them usable
only when selected by the contract:

- `EXCLUDE-A-CATEGORY AVERAGE`
- `CUMULATIVE-SNAPSHOT TOTALS -- max() AT ENTITY GRAIN`
- `TOP-N TIE-CROSSES-CUTOFF`

Move proof-shaped requirements into `Validation`:

- row-count and row-shape checks
- grain uniqueness checks
- before/after reconciliation
- full-refresh survival checks
- all target tables exist as base tables
- forbidden patterns were avoided

In particular, `TMP/INTERMEDIATE-TIER REMOVAL` contains a validation requirement:
reconcile before/after row counts, schemas, and value-level behavior. That proof
belongs in the contract signature and validation stage, not only as
implementation advice.

### Implementation

Implementation must follow the contract. If the contract becomes impossible,
the worker must revise the contract explicitly before continuing.

The worker should not silently switch strategy because a generic implementation
rule feels easier.

### Validation

Validation must verify the contract, not just `dbt build`.

Required checks:

- target tables exist as base tables
- target names match project convention
- row shape matches the contract
- grain keys are unique where expected
- forbidden patterns were avoided
- representative values are plausible against local sources
- every target table named in the contract was checked

If a contract signature fails, the task is an implementation failure even if
`dbt build` passes.

## Scope

This proposal should initially be tested as a stabilization hypothesis, not a
full solver rewrite.

The first smoke should target tasks where prior evidence shows the rule was
known but implementation compliance was weak:

- `airbnb001`: latest-window rule must survive `--full-refresh`
- `apple_store001`: report-grain raw grouping key must be preserved
- `salesforce001`: daily report contract must pin date range and row shape
- `jira001`: full-dimension row count plus value-definition second gap

Canaries should include known champion passers and regression-sensitive tasks:

- `activity001`
- `mrr001`
- `retail001`
- `recharge001`
- `asset001`

## Success Criteria

For the first smoke:

- at least one target flips by committed artifact;
- no canary regression attributable to the contract mechanism;
- artifact evidence shows the contract was written before implementation;
- validation reports the rule-specific signature, not only dbt success.

For promotion consideration:

- expanded smoke shows net positive impact;
- the mechanism improves worker compliance, not just one lucky task;
- full run is only launched after targeted evidence shows at least `+1` net with
  zero contract-caused canary regressions.

## Non-Goals

- Do not introduce multiple specialized workers in the first version.
- Do not change the harness, verifier, model, runtime, or sampling.
- Do not fold fixture repairs into this solver hypothesis.
- Do not promote a solver that only changes pass-set composition without net
  gain.

## Expected Benefit

The expected benefit is not a new broad semantic rule. It is better compliance
with rules that already appear to be directionally correct.

The primary gain should come from converting known near-misses and flaky
compliance cases into stable passes.
