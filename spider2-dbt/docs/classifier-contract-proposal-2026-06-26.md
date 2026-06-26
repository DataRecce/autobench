# Classifier Contract Proposal

Date: 2026-06-26

## Context

The current Spider2-DBT registry baseline resolves to the `spd0008-over-emit-collapse`
solver workflow. That workflow inherits the `spd0007b-value-def-no-idcast`
classifier/router stage and adds G2 over-emit rules. It has a
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
- `salesforce001` and `jira001`: prior G1 runs showed that a contract can expose
  second blockers, but these are not clean first-smoke flip targets because the
  remaining blockers are not pure classifier-compliance failures.

The next solver improvement should make the classifier output enforceable by the
implementation and validation stages.

## Proposal

Do not route directly from `Classify` to unconstrained `Implementation`. In the
first version, add one narrow checkpoint between exploration and SQL edits:

1. `Classify`
2. `Exploration for Contract`
3. `Implementation Contract`
4. `Implementation`
5. `Validation`
6. `Finalization`

This is still a README-only solver change. It does not require harness changes or
multiple workers.

This first version is deliberately **not** a full stage rewrite. It should add a
contract checkpoint and contract-aware validation while leaving the existing rule
families substantively intact.

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
- `contract_blocked_condition`

The contract must be derived from local workspace evidence, not hidden gold.
`expected_row_shape` and `validation_signature` must come from a named rule
template plus local evidence, not from free-form worker preference.

For the first smoke, the allowed contract template inventory is deliberately
small:

- `G2_LATEST_WINDOW_FULL_REFRESH`: for targets whose target or sibling model has
  latest-window logic tied to `is_incremental()`. The contract must name the
  sibling/target model, the source date column, the max-date anchor, the window
  length, the expected single-window grain, and the forbidden pattern: leaving
  the required window filter only inside an `is_incremental()` branch.
- `G2_REPORT_RAW_GROUPING_HOLD`: for report-grain targets already passing under
  the current champion. The contract must name the raw grouping column, the
  primary anchor relation, the lookup relation if any, and the forbidden pattern:
  regrouping on a canonicalized lookup value instead of preserving the raw key.

Any other named template is out of scope for the first smoke.

### Implementation Tip Relocation

The current implementation stage carries many generic tips. In the long-term
contract design, those tips should no longer compete with the classifier output
at implementation time. They should eventually be redistributed by role.

This relocation is **future work**, not part of the first smoke lever. The first
smoke must not move these tips, because that would make the hypothesis too broad
to attribute. The future relocation inventory is recorded here only so the next
hypothesis can split it cleanly:

Future classification-shaped tips:

- `PER-KEY METRIC AGGREGATE`
- `COVERAGE / COMPLETENESS`
- `BUILD / RENAME -- PRESERVE THE COLUMN SET`
- `TMP/INTERMEDIATE-TIER REMOVAL`
- `FEATURE-BOUNDARY REMOVE / TOGGLE / DISABLE`
- `PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX`

These decide which strategy applies and would belong in a later
classification/contract relocation hypothesis.

Future calculation-shaped recipes that can remain in `Implementation`:

- `EXCLUDE-A-CATEGORY AVERAGE`
- `CUMULATIVE-SNAPSHOT TOTALS -- max() AT ENTITY GRAIN`
- `TOP-N TIE-CROSSES-CUTOFF`

Future proof-shaped requirements:

- row-count and row-shape checks
- grain uniqueness checks
- before/after reconciliation
- full-refresh survival checks
- all target tables exist as base tables
- forbidden patterns were avoided

In particular, `TMP/INTERMEDIATE-TIER REMOVAL` contains a validation requirement:
reconcile before/after row counts, schemas, and value-level behavior. That proof
would belong in a future contract signature and validation stage, not only as
implementation advice.

### Implementation

Implementation must follow the contract. If the contract becomes impossible, the
worker must stop and mark `contract_blocked` with the local evidence. It may
return to exploration to fill a missing evidence field, but it may not silently
switch to a different selected rule.

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
`dbt build` passes. The signature is evidence that the committed artifact matches
the selected local rule, not an independent substitute for the hidden verifier.

## Scope

This proposal should initially be tested as a stabilization hypothesis, not a
full solver rewrite.

The first smoke should target tasks where prior evidence shows the rule was
known but implementation compliance was weak, while avoiding tasks whose residual
blockers are not mainly classifier compliance.

- `airbnb001`: latest-window rule must survive `--full-refresh`
- `apple_store001`: report-grain raw grouping key must hold under the current
  champion; because it already passes in `spd0008`, it is a hold target, not a
  flip target

Do not use `salesforce001` or `jira001` as first-smoke success targets. They can
be diagnostic cells later, but prior evidence shows second blockers beyond a
contract-compliance failure.

Hard gate canaries must be current-registry-baseline passers and must all hold:

- `activity001`
- `app_reporting001`
- `google_play001`
- `google_play002`
- `quickbooks003`

Telemetry-only cells may be included in smoke output but do not decide go/no-go
because they have known variance or are not current-registry-baseline passers:

- `mrr001`
- `mrr002`
- `retail001`
- `recharge002`
- `f1003`

## Success Criteria

For the first smoke:

- `airbnb001` flips by committed artifact, or the run is marked no-go;
- all hard gate canaries listed above hold;
- telemetry-only cells are reported separately and never reclassified after the
  result to rescue or reject the smoke;
- artifact evidence shows the contract was written before implementation;
- validation reports the rule-specific signature, not only dbt success.

For promotion consideration:

- expanded smoke shows net positive impact versus the current registry baseline;
- the mechanism improves worker compliance, not just one lucky task;
- full run is only launched after targeted evidence shows at least `+1` net with
  no stable-passer canary regression.

## Non-Goals

- Do not introduce multiple specialized workers in the first version.
- Do not change the harness, verifier, model, runtime, or sampling.
- Do not fold fixture repairs into this solver hypothesis.
- Do not relocate all implementation tips in the first version; that is a
  follow-up after the contract checkpoint has evidence.
- Do not promote a solver that only changes pass-set composition without net
  gain.

## Expected Benefit

The expected benefit is not a new broad semantic rule. It is better compliance
with rules that already appear to be directionally correct.

The primary gain should come from converting known near-misses and flaky
compliance cases into stable passes.
