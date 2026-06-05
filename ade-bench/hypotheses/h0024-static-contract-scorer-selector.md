---
id: h0024
title: Static Contract Scorer Selector -- run multiple baseline candidates and choose by local build/artifact contract score
status: hypothesis
kind: hypothesis
source: concept-candidate-selector-contract-scorer fan-out; tests the static scorer selector design, not a new failure-pattern README rule. Forks the current @baseline solver protocol only as a declared protocol-family variant.
started: 2026-06-05T09:42:10Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The current pass@1 protocol commits the artifact from one candidate solve. Pass@k evidence
means that, for some tasks, another candidate in the same family of attempts may already
contain the right artifact. This hypothesis tests whether a deterministic local scorer can
choose a better committed artifact without using the hidden oracle.

**Falsifiable claim:** for each smoke task, run `N >= 3` independent candidates with the
current `@baseline` solver README unchanged, then choose the final committed artifact with a
static Contract Scorer that uses only local workspace evidence. The scorer does not ask a
candidate to write a new contract. It scores the final files directly:

- build health: `dbt compile`, targeted `dbt run`, targeted `dbt test`, or selected
  `dbt build` succeeds for the touched scope;
- artifact shape: required refs/models exist, schema-declared columns are present, and
  instruction-named deliverables are present;
- grain and key sanity: uniqueness/null/row-count checks reconcile against local sources or
  declared grain where that grain is locally derivable;
- type preservation: same-named columns keep local upstream/package types or apply an
  explicit local cast in the committed SQL;
- cleanup and no-harm: generated scratch is not committed, and unrelated package files,
  profiles, namespaces, dependencies, seeds, and unrelated models are not rewritten.

The claim passes smoke only if the selected candidate beats the single-candidate baseline on
at least one target where a local static contract can distinguish candidates, while preserving
all pass canaries. It is falsified if all selected artifacts are identical-or-worse than the
first candidate, if the scorer prefers locally invalid artifacts, or if the scorer needs hidden
verifier output to decide.

## Protocol-family declaration

This is a **protocol-family change**, not a standard solver-README-only hypothesis. It changes
candidate generation and selection: the runner must create multiple isolated candidate solves
for the same task, score each candidate's committed files locally, and commit only the
highest-scoring candidate. Results must be labeled separately from README-only experiments.
At propose, any spec/harness change must be declared as protocol-family metadata; do not claim
the independent variable is only the solver README.

## Target datasets

Smoke targets should exercise local, static artifact checks where hidden-oracle access is not
needed to reject a bad candidate:

- `ade-bench-asana002` -- package/type contract candidate where the local installed package
  type signal is concrete.
- `ade-bench-quickbooks001` -- missing local deliverable models can be detected through the
  `ref()` graph and installed package templates.
- `ade-bench-ana-eng006` -- build/shape/type checks can reject candidates that leave an
  obvious raw string/date mismatch or missing deliverables, even if width remains capped by
  oracle-only columns.
- `ade-bench-f1006` -- value-divergence reachability probe; included to test whether the
  static scorer is blind on locally underdetermined tasks.

Add currently-passing cross-family canaries at smoke because the protocol can select among
broader edits. Include at least `ade-bench-airbnb001`, `ade-bench-asana001`,
`ade-bench-f1007`, and `ade-bench-quickbooks002`; include `ade-bench-f1001` as the
non-package convention-bleed sentinel.

## Acceptance criteria

**AC-1 -- Candidate generation is real and isolated.** For every smoke cell, the run artifact
records `N >= 3` candidate workspaces/attempts with the same baseline solver README, same
model/runtime settings, and no shared mutable task state except the initial workspace copy.

**AC-2 -- Selection is leak-safe and auditable.** The scorer report is saved with the run
artifact and lists, per candidate, the local commands/checks used, the score components, and
the selected candidate. The report contains no hidden `AUTO_*`, `solution__*`,
`check_option_*`, verifier-output, public-fetch, web-search, or LLM-as-oracle references.
`rk audit --policy strict` stays clean on the selected run.

**AC-3 -- Static scoring beats first-candidate pass@1 on smoke.** On the target set, the
selected artifact should flip at least one target or strictly reduce the local distance-to-pass
without regressing any canary. A target with unchanged artifacts and unchanged `Got N` is
evidence that the selector was inert or blind for that cell.

**AC-4 -- The deep-dive verifies artifacts, not chatter.** Smoke analysis must compare the
selected committed SQL/files against the losing candidates and the first candidate, and explain
why the local scorer chose it. Candidate reasoning is not evidence unless the final artifact
satisfies the scored local contract.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
