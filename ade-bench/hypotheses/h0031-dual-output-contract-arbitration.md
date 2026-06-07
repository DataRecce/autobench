---
id: h0031
title: Dual Output Contract Arbitration -- generate two independent contracts, then select/abstain by visible evidence before implementation
status: hypothesis
kind: hypothesis
source: captain synthesis after _artifacts/arbitration-without-oracle.md and WORKFLOW-REFINE findings: Output Contract is useful as an observability surface (h0017) but not sufficient for correctness; h0026 proved self-anchored candidate scoring fails without independent judgment. This hypothesis tests the next protocol-family step: two independent contract routes plus an evidence-hierarchy arbitrator that can SELECT, REJECT_BOTH, or ABSTAIN before any SQL is authored.
started: 2026-06-07T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The Output Contract stage gave useful visibility into the solver's mental model: h0017 showed the
contract can reach the committed artifact and reveal the exact wrong assumption (child-driven grain).
But h0017 and h0023 also showed that a single contract author is not enough. The contract can be
wrong, under-scoped, or unsafe, and then Implementation builds to the wrong contract. h0026 showed
the same wall in selector form: multiple candidates are worthless if selection is anchored to each
candidate's own checks.

This hypothesis tests a resolver protocol that separates three jobs:

1. **Evidence snapshot** -- collect visible, local evidence without deciding the answer.
2. **Independent contract generation** -- two isolated routes write Output Contracts from the same
   evidence snapshot, without seeing each other's contract.
3. **Evidence arbitration** -- a separate arbitrator compares contract claims against a pre-declared
   evidence hierarchy and either selects a contract, merges non-conflicting claims, rejects both, or
   abstains when the visible workspace cannot distinguish them.

The key claim is not "two contracts will magically find the oracle." The key claim is that two
contracts expose disagreement, and an evidence-based arbitrator prevents the workflow from selecting
a plausible but unsupported contract. If visible evidence cannot decide, the correct result is
`ABSTAIN`, not a forced choice.

**Falsifiable claim:** for each smoke task, run two independent Output Contract routes (`A` and
`B`) before any SQL change. Each route must produce a contract with deliverables, grain/key source,
declared columns, local types, metric logic, assumptions, and evidence references. Then run an
arbitrator that compares the two contracts claim-by-claim using this hierarchy:

1. explicit task instruction;
2. `schema.yml` / declared local contract;
3. raw source data and conservation relations;
4. project-local tests / dbt constraints;
5. same-project sibling model patterns;
6. installed package artifacts only when the task/project clearly uses that package shape;
7. candidate transcript / plan / self-written contract (debug only, never a tie-breaker).

The arbitrator writes `arbitration.json` with one of:

- `SELECT_A` / `SELECT_B` -- one contract is supported by higher-authority visible evidence and the
  other violates it;
- `MERGE_NON_CONFLICTING` -- contracts disagree only on separable claims and each selected claim has
  visible support;
- `REJECT_BOTH` -- both contracts violate hard local evidence;
- `ABSTAIN` -- the visible workspace cannot decide the disagreement.

Implementation may proceed only from the selected or merged contract. If the arbitrator abstains on a
load-bearing claim, the run must record the unresolved claim and avoid presenting the final answer as
locally verified.

The hypothesis passes smoke if the protocol both (a) proves real independence/arbitration artifacts
exist and (b) flips or strictly improves at least one locally arbitrable target without regressing any
canary. It is falsified if the two routes converge on the same unsupported premise, if the arbitrator
chooses by narrative plausibility or transcript claims, if `arbitration.json` is missing, if it forces
a choice on an oracle-only disagreement, or if selected-contract implementation regresses canaries.

## Protocol-family declaration

This is a **protocol-family change**, not a solver-README-only hypothesis. It changes the resolver
workflow shape by adding two contract-generation routes and a pre-Implementation arbitrator. Results
must be labeled as "dual-output-contract arbitration" and kept separate from README-only
independent-variable runs.

This hypothesis should not be sold as "better instructions." The test is whether the resolver creates
auditable independent contracts and applies visible-evidence arbitration before Implementation.

## Target datasets

The first smoke should cover three locally arbitrable disagreement types, not the full benchmark:

- `ade-bench-ana-eng004` -- width/missing-columns representative. Contracts should name the expected
  column set; arbitration should use declared schema/instruction evidence and abstain if the expected
  width is oracle-only.
- `ade-bench-intercom001` -- grain/missing-parent-rows representative with a cleaner local parent
  signal than the underdetermined asana intermediate convention. Contracts should name the parent/key
  source; arbitration should use raw parent `COUNT(DISTINCT key)` and local sibling patterns.
- `ade-bench-f1011` -- answer-style representative. Contracts should produce option-level local
  checks; arbitration should prefer disconfirming evidence for included options and reject
  self-anchored completeness scoring.

Because this protocol can affect broad task behavior, the smoke carries a regression panel of
currently-passing `@baseline` canaries:

- `ade-bench-airbnb001`
- `ade-bench-ana-eng001`
- `ade-bench-asana001`
- `ade-bench-f1007`
- `ade-bench-quickbooks002`
- `ade-bench-f1001` as the non-package convention-bleed tripwire

No intercom canary is possible if the current `@baseline` still has zero passing intercom tasks.

## Acceptance criteria

**AC-1 -- Real contract independence.** For every target cell, route A and route B must be generated
in isolated sessions/workspaces or under forced-divergence stances. Route B must not read route A's
contract. The run artifact records both contracts and the isolation method.

**AC-2 -- Contracts are evidence-bearing, not narrative.** Each contract claim cites a visible local
evidence source: task instruction, schema, source query, local test, sibling model, or qualified
package artifact. Claims with no visible support must be marked as assumptions, not facts.

**AC-3 -- Arbitration is evidence-based and machine-readable.** The run saves `arbitration.json`
containing the decision, selected/rejected/unresolved claims, evidence authority for each selected
claim, and every abstention. Candidate transcript quality is never a tie-breaker.

**AC-4 -- Abstention is honored.** If the arbitrator marks a load-bearing claim `ABSTAIN`, the
workflow must not pretend the selected artifact is locally verified. An abstained target can still be
useful diagnostic evidence, but it does not count as a controllable +1 candidate.

**AC-5 -- Implementation follows the arbitrated contract.** The final SQL/files must satisfy the
selected or merged contract. If final artifacts diverge from the selected contract, the hypothesis is
NO-GO even if dbt builds.

**AC-6 -- Every recorded score is paired with a clean strict audit.** `rk audit --policy strict`
must report `tainted: 0`, and each cell must have captured solver artifacts.

**Smoke gate:** require all three protocol artifacts (`contract_a`, `contract_b`,
`arbitration.json`) on every target. The smoke is GO only if at least one target flips or strictly
improves by artifact-level distance, zero canaries regress, and the improvement is attributable to an
arbitrated claim rather than transcript plausibility. A canary dropping FAIL is NO-GO regardless of
target movement.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict

