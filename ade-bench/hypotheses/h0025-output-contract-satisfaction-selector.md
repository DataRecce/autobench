---
id: h0025
title: Output-Contract Satisfaction Selector -- require each candidate to write a local contract, then select the artifact that best satisfies its contract
status: hypothesis
kind: hypothesis
source: concept-candidate-selector-contract-scorer fan-out; tests the candidate-written-contract satisfaction selector design, not another Output Contract README fix. Forks the current @baseline solver protocol only as a declared protocol-family variant.
started: 2026-06-05T09:42:10Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Prior Output Contract work moved the control point earlier, but it still leaves one failure
mode: a candidate can write a plausible contract as notes and then commit SQL that does not
satisfy it. This hypothesis tests selection after candidate generation: compare candidates by
how well their final artifacts satisfy their own locally-derived contracts.

**Falsifiable claim:** for each smoke task, run `N >= 3` candidates. Each candidate must write
an Output Contract before authoring or restructuring SQL, covering grain/source of key set,
ordered columns, local types, and the complete deliverable set. After the candidate commits,
the selector scores only artifact-vs-contract satisfaction:

- the final SQL emits the candidate's recorded grain and does not narrow the recorded key set;
- the final SQL emits the recorded columns in the recorded order when the column set is locally
  declared or derivable;
- same-named columns preserve the recorded local/source/package type or apply the recorded cast;
- every recorded deliverable model/ref exists in the final project;
- the candidate does not pass with transcript-only contract claims that are absent from final
  files;
- if two candidates both satisfy their contracts, prefer the one whose contract cites more
  concrete local sources and needs fewer unrelated edits.

The claim passes smoke if selecting by contract satisfaction recovers at least one locally
reachable win where a single candidate often writes the right contract but commits a wrong or
incomplete artifact. It is falsified if contracts are noisy self-attestations that do not help
choose a better artifact, or if the scorer rewards candidates whose contracts are locally
unsupported.

## Protocol-family declaration

This is a **protocol-family change**, not a solver-README-only hypothesis. It changes both
candidate generation and final selection: multiple candidates are produced, each candidate
creates a local Output Contract, and a separate selector chooses the committed candidate by
contract satisfaction. Results must be tracked as a new protocol family and not compared as a
pure README independent-variable run.

## Target datasets

Smoke targets should be tasks where the contract is at least partly local and where prior
learnings say "verify the artifact, not the transcript" is load-bearing:

- `ade-bench-asana004` -- grain/refactor task where the contract must preserve the extracted
  CTE output and downstream spine/coalesce behavior.
- `ade-bench-quickbooks001` -- deliverable-set task where the contract must name and build
  the missing local staging models.
- `ade-bench-ana-eng006` -- type/width mixed task where the contract can locally require the
  date cast and locally-supported column/deliverable set, while acknowledging blind width
  deltas.
- `ade-bench-ana-eng004` -- width representative to test whether the selector rejects
  under-derived or over-padded contracts without pretending oracle-only columns are local.

Carry the standard cross-family canary panel for a generative protocol:
`ade-bench-airbnb001`, `ade-bench-ana-eng001`, `ade-bench-asana001`, `ade-bench-f1007`,
`ade-bench-quickbooks002`, plus `ade-bench-f1001` as the non-package convention-bleed
sentinel.

## Acceptance criteria

**AC-1 -- Candidate contracts exist before SQL.** Each candidate artifact contains a
pre-implementation contract with named local evidence for grain, columns, types, and
deliverables. Missing or after-the-fact contracts score zero for contract satisfaction.

**AC-2 -- Selector checks contract-to-artifact, not hidden correctness.** The saved scorer
report lists every contract clause, the final file evidence for or against it, and the chosen
candidate. It must not mention hidden `AUTO_*`, `solution__*`, verifier tests, public fetches,
web search, or external reference material.

**AC-3 -- Smoke improves selection quality.** On the target set, selected pass@1 should flip
at least one locally-derivable target or produce a strictly better artifact-level distance
than the first candidate, with no canary regression. If the selector chooses a contract that
sounds complete but the committed SQL is unchanged, the hypothesis is NO-GO.

**AC-4 -- Blind-to-oracle cases are handled honestly.** For `ana-eng004` and the width parts
of `ana-eng006`, success means rejecting unsupported padding and documenting the local ceiling,
not inventing columns to mimic hidden solutions.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
