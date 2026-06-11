---
id: h0027
title: Do-No-Harm Selector -- reject candidates with unrelated rewrites before choosing the best local contract score
status: conclude
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

This hypothesis was concluded as a captain strategic sibling-kill on the
`concept-candidate-selector-contract-scorer` family wall, with no run performed. The
behavioral evidence is the family's three prior runs/decisions:

- **h0026** (answer-decision-table selector, REJECTED by run `a01f97caf6d6462e`): all N≥3
  candidates shared the SAME plausible-but-wrong reading (committed `ABDE`, oracle `ADE`),
  and the scorer graded each candidate against its OWN local checks ("support 6/6,
  contradictions 0"). A uniformly-held wrong answer self-scores perfect and wins — the
  self-anchored false-green.
- **h0031** (dual-output-contract arbitration, REJECTED at smoke `0de9870ae2220bca`):
  genuinely-independent route B + an external-criterion (raw conservation/coverage) arbitrator
  are TABLE STAKES, not a contribution — they were both achieved and STILL reproduced
  baseline's byte-identical wrong answer (f1011 → `ABDE`). More candidate generation +
  arbitration does not create an oracle.
- **h0024** (static-contract-scorer selector, REJECTED 2026-06-11, captain sibling-kill): its
  static build/shape/type rubric is the same self-anchored scorer.

**Why h0027 inherits the wall.** The do-no-harm filter (reject candidates that rewrite
`profiles.yml` / packages / namespaces / macros / seeds / unrelated models, replace installed
packages with shims, touch broad model families on a narrow-scope task, or leave scratch as
final artifacts) is a useful HYGIENE check — it would plausibly reduce convention-bleed and
broad-edit regressions. But the actual SELECTION among the surviving candidates still rests on
"prefer the smallest relevant diff that builds and satisfies the locally visible task
contract" — i.e. self-anchored local-contract scoring. On a uniformly-held plausible-wrong
answer (the f1011 / asana004 class), every surviving candidate satisfies its OWN local
contract, so the filter changes WHICH candidate wins but cannot distinguish the plausible-wrong
from the oracle-correct one. There is no candidate DIVERSITY requirement (force candidates to
disagree on borderline decisions) and no INDEPENDENT IN-decision falsifier — exactly the two
axes propose-gate G9 ("selector independence") screens for. h0027 would FAIL G9 at propose,
without spending a smoke run.

## Verdict

**REJECTED** — sibling-killed by the candidate-selector family wall (h0024 / h0026 / h0031).
h0027 rejects candidates with unrelated rewrites before choosing the best local contract score;
the do-no-harm filter is a useful hygiene check, but the SELECTION still rests on self-anchored
local-contract scoring, so it inherits the same wall: it cannot distinguish a uniformly-held
plausible-wrong answer from the oracle-correct one. No candidate diversity + no independent
IN-decision falsifier => would fail propose gate G9 (selector independence). No run performed;
captain strategic kill on the family evidence.

## Follow-up Routing

**stop** — candidate-selector family exhausted / CLOSED. The
`concept-candidate-selector-contract-scorer` fan-out is rejected-as-written across the board
(h0024 / h0025 / h0026 / h0027 terminal; h0031 confirmed the wall survives genuine candidate
diversity + external-criterion arbitration). h0028 (adversarial re-fire) is the one kept-open
sibling attempting the G9 independence axes; do not file another self-anchored selector variant.

## Stage Report: conclude

- DONE: Write ## Verdict = REJECTED: sibling-killed by the candidate-selector family wall (h0024/h0026/h0031)
  Verdict section records REJECTED, the self-anchored selection wall, G9 failure, no run / captain strategic kill.
- DONE: Write ## Follow-up Routing = stop: candidate-selector family exhausted/CLOSED
  Follow-up Routing section = stop; notes h0028 as the one kept-open G9-independence sibling; do not file another self-anchored variant.
- DONE: Finalize the workflow-refinement finding (protocol-family hypothesis)
  Updated the family status block in `_artifacts/WORKFLOW-REFINE.md` to record h0027 REJECTED 2026-06-11 (sibling-kill); all four scorer-style siblings h0024/h0025/h0026/h0027 now terminal, family CLOSED.

### Summary

h0027 concluded as a captain strategic sibling-kill (no run) on the
`concept-candidate-selector-contract-scorer` family wall. The do-no-harm diff filter is useful
hygiene, but selection among surviving candidates still rests on self-anchored local-contract
scoring, so it cannot break a uniformly-held plausible-wrong answer (the f1011/asana004 class) —
it would fail propose gate G9 (selector independence). Recorded the verdict + stop routing in the
entity, and folded h0027's terminal state into the WORKFLOW-REFINE family ledger (all four
scorer-style siblings now terminal; h0028 kept open for the G9 independence attempt).
