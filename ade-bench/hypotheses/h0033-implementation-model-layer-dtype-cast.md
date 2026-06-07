---
id: h0033
title: E4 -- Implementation; apply a mechanical in-place ::type cast in the MODEL .sql (never the raw seed) when a column's representation mismatches a sibling/instruction contract -- recover asana002 without convention-bleed
status: propose
kind: hypothesis
source: _proposal/oracle-problem-systematic-program.md (E4); successor to archived h0020 (REJECTED -- cast the raw seed, wrong layer) and h0009 (asana002 win but convention-bled -3); E0/h0032 found NO declared data_type/contract entries in the project, so the cast keys off the observed type mismatch vs a sibling/instruction, not a declared contract. captain go-ahead 2026-06-07.
started: 2026-06-07T15:17:49Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

*(Seeded by the FO from the proposal E4; the propose stage builds the variant + worked example.)*

`asana002` is a type/contract mismatch (oracle `AUTO_asana__task_equality`, `Got 2`): the committed
`asana__task` model emits a column (e.g. `due_at`) whose representation/type differs from what the
hidden oracle expects; a `::timestamp` cast fixes it -- Mini-confirmed solvable and the h0009 win.
The prior attempts each failed on HOW: **h0009** landed the cast but **convention-bled** (-3 on
f1/quickbooks by over-applying the package convention); **h0020** precondition-gated the cast but
applied it to the **raw SEED** (the wrong layer). E0/h0032 found the project has **no declared
`data_type:`/`contract:` entries**, so the cast cannot key off a declared contract -- it keys off the
**observed type mismatch** vs a sibling model / the task instruction.

**Lever (single Implementation-stage rule + a copyable worked example):** when a model column's
type/representation mismatches what a sibling model or the task instruction implies, apply a
mechanical **in-place `::<type>` cast IN THE MODEL `.sql`** (e.g. `due_at::timestamp`) --
additive/in-place ONLY: no add/drop/rename of columns, and **NEVER edit the raw seed or source**
(the h0020 failure). Precondition-gated to an observed mismatch on a specific column; do **not**
broadly re-type every column (the h0009 convention-bleed).

**Falsifiable claim:** the model-layer in-place cast rule flips `asana002` (`Got 2 -> 0`) with ZERO
convention-bleed regression, raising `stratified_pass_at_1` above `@baseline` 0.6458. Falsified if
inert (committed `asana__task.sql` unchanged / still wrong type), if it edits the seed (h0020
failure mode), or if any perturbable canary regresses (h0009 failure mode).

## Target datasets

Target (smoke): `ade-bench-asana002`. This rule is generative (fires on any model with a column
type mismatch), so per G8 the smoke carries >=2 **perturbable** canaries from the families the cast
could over-apply to (the h0009 convention-bleed families): `ade-bench-f1001`,
`ade-bench-quickbooks003`; plus cross-family canaries `ade-bench-airbnb001`, `ade-bench-ana-eng001`,
`ade-bench-asana001` (the asana same-family sentinel). All confirmed `@baseline` passers.

## Acceptance criteria

**AC-1 -- Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
One `## Stage: Implementation` rule; leak-guard + other stages byte-identical; no hidden-test tokens.

**AC-2 -- The cast is applied to the MODEL `.sql` (artifact-verified from the committed apply_patch),
NOT the raw seed (the h0020 failure mode); clean strict audit (`tainted:0`, `captured>0`).**

**AC-3 -- Verdict via the paired diff vs `@baseline`: `asana002` flips AND zero convention-bleed
regression on the perturbable canaries (`f1001`/`quickbooks003`).**

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
