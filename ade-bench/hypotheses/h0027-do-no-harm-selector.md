---
id: h0027
title: Do-No-Harm Selector -- reject candidates with unrelated rewrites before choosing the best local contract score
status: hypothesis
kind: hypothesis
source: concept-candidate-selector-contract-scorer fan-out; tests the do-no-harm selector design, not a new failure-pattern README rule. Forks the current @baseline solver protocol only as a declared protocol-family variant.
started: 2026-06-05T09:42:10Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Multi-candidate solving increases the chance that one attempt finds a useful local edit, but it
also increases the chance that one candidate makes broad, harmful changes. Prior learnings
showed convention bleed and unanchored broad edits can break tasks that already passed. This
hypothesis tests a selector whose first job is to reject candidates that damage unrelated
project surfaces before applying any positive contract score.

**Falsifiable claim:** for each smoke task, run `N >= 3` candidates with the baseline solver
README. The selector applies hard do-no-harm filters before scoring positives:

- reject candidates that rewrite `profiles.yml`, package/dependency files, package namespaces,
  macros, seeds, or unrelated models unless the task explicitly asks for that surface;
- reject candidates that replace installed packages with local shims or remove existing
  `dbt_packages/`;
- reject candidates whose diff touches broad model families when the task names a narrow
  model/scope;
- reject candidates that leave generated scratch as final artifacts;
- among remaining candidates, prefer the smallest relevant diff that builds and satisfies the
  locally visible task contract.

The claim passes if the selector preserves pass canaries while still choosing at least one
target candidate that improves or flips a failure. It is falsified if the hard filters reject
all useful candidates, if the selector still chooses broad harmful rewrites, or if it improves
targets by breaking passers.

## Protocol-family declaration

This is a **protocol-family change**, not a solver-README-only hypothesis. It changes
selection semantics after multiple candidate solves and introduces a hard-filter policy over
candidate diffs. Results must be labeled as the do-no-harm selector protocol family and kept
separate from README-only independent-variable runs.

## Target datasets

The smoke set must include both reachable failures and regression-prone passers, because the
selector's main claim is "choose useful candidates without collateral damage":

- `ade-bench-asana002` -- reachable local package/type candidate where a narrow useful edit can
  beat broad rewrites.
- `ade-bench-quickbooks001` -- deliverable-set target where package templates are useful but
  package/dependency rewrites must remain forbidden.
- `ade-bench-f1006` -- underdetermined/value-divergence target to test whether the selector
  refuses speculative broad rewrites when local evidence is weak.
- `ade-bench-f1001` -- non-package convention-bleed sentinel.
- `ade-bench-quickbooks003` -- quickbooks passer/sentinel for package-convention damage if it
  is still passing at the current baseline.
- `ade-bench-airbnb001`, `ade-bench-asana001`, `ade-bench-f1007`, `ade-bench-quickbooks002`
  as additional currently-passing cross-family canaries.

If any listed canary is no longer passing at the current `@baseline`, replace it with a
currently-passing task from the same family at propose and document the replacement.

## Acceptance criteria

**AC-1 -- Diff filters are explicit and saved.** The scorer report records every candidate's
changed-file list, every hard-filter decision, and the final selected candidate. A rejected
candidate must include the exact local reason for rejection.

**AC-2 -- Leak guard remains strict.** Selection uses only local candidate diffs, local dbt
commands/artifacts, source data, installed packages, and the task instruction. It must not use
hidden verifier output, public solutions, external downloads, web search, or LLM-as-oracle
judgement. `rk audit --policy strict` must be clean.

**AC-3 -- No canary damage.** Every currently-passing canary in the smoke set must remain
passing. A canary regression is NO-GO even if a target flips, because the selector's defining
claim is damage avoidance.

**AC-4 -- Target improvement is still required.** At least one failing target should flip or
show a strictly better artifact-level distance than the first candidate. If the selector only
preserves passers and never helps a target, the protocol is useful as a guardrail but not
sufficient to beat pass@1.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
