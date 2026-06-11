---
id: h0025
title: Output-Contract Satisfaction Selector -- require each candidate to write a local contract, then select the artifact that best satisfies its contract
status: conclude
kind: hypothesis
source: concept-candidate-selector-contract-scorer fan-out; tests the candidate-written-contract satisfaction selector design, not another Output Contract README fix. Forks the current @baseline solver protocol only as a declared protocol-family variant.
started: 2026-06-05T09:42:10Z
completed: 2026-06-11T02:53:53Z
verdict: REJECTED
score:
worktree:
archived: 2026-06-11T02:53:53Z
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

No run was performed. This was a captain strategic sibling-kill on accumulated
candidate-selector family evidence (h0024 REJECTED 2026-06-11, h0026 REJECTED-by-run
2026-06-05, h0031 REJECTED 2026-06-07). The mechanism that sinks h0025 is the same
self-anchored-scoring wall the family has hit three times:

- h0025 has each candidate write its OWN local Output Contract (grain/key set, ordered
  columns, local types, deliverable set) and then scores the committed artifact ONLY against
  that candidate's own self-written contract.
- A confident, uniformly-held WRONG reading produces a self-consistent contract: the SQL emits
  exactly the grain/columns/types the candidate recorded, so it scores perfect contract
  satisfaction (support N/N, contradictions 0) while still being wrong against the hidden
  oracle. This is precisely the false-green h0026 demonstrated by run (all three candidates
  shared one plausible-wrong option; each self-scored 6/6 and the wrong one won).
- The "prefer more concrete local sources / fewer unrelated edits" tiebreaker (AC-3) only
  orders candidates that ALL satisfy their own contracts; it does not break toward the oracle.
- The AC-4 honest-ceiling handling for `ana-eng004` / width parts of `ana-eng006` does not
  rescue the design: refusing to invent columns is correct but is not a selection signal that
  moves a wrong-but-self-consistent candidate toward the right answer.

There is NO candidate diversity (single-session harness cannot supply N genuinely independent
readings — G9 generation-independence axis) and NO independent IN-decision falsifier (the only
judge is the candidate's own contract — G9 judgment-independence axis). h0025 fails BOTH G9
axes at propose, so it would not earn a smoke run. Transferable rule confirmed (4th instance):
a selection criterion anchored to the candidate's own checks/contract is a false-green; only
forced candidate divergence + an external falsifier escapes the self-anchored trap, and per
h0031 even that is table stakes, not a guaranteed win.

## Verdict

REJECTED: sibling-killed by the candidate-selector family wall (h0024 / h0026 / h0031). h0025
requires each candidate to write its OWN local Output Contract, then selects the artifact that
best satisfies that self-written contract — the same self-anchored-scoring design the family
has falsified three times. A confident, uniformly-held wrong answer scores perfect against its
own contract, so it cannot be moved toward the oracle. No candidate diversity + no independent
IN-decision falsifier => fails propose gate G9 (judgment-independence axis). No run performed;
captain strategic kill on the family evidence. Family CLOSED.

## Follow-up Routing

stop — candidate-selector family exhausted / CLOSED. Four instances now confirm the
self-anchored-scoring wall (h0024, h0025, h0026 by run, h0031). Do NOT file another
self-anchored selector variant. The one still-open sibling **h0028** (adversarial re-fire) is
intentionally kept queued because it explicitly attempts the G9 independence axes
(forced-divergence + cross-examination) rather than re-running self-scored completeness — it is
the family's only remaining legitimate fork and is left in place, not closed here.

## Stage Report: conclude

- DONE: Write ## Verdict = REJECTED (sibling-killed by candidate-selector family wall h0024/h0026/h0031)
  Verdict + Behavioral analysis sections written; self-anchored-contract mechanism + G9 dual-axis failure recorded. No run (captain strategic kill).
- DONE: Write ## Follow-up Routing = stop (family exhausted/CLOSED; h0028 kept queued)
  Routing notes h0028 explicitly attempts G9 independence axes and is intentionally left open; no new self-anchored variant filed.
- DONE: Finalize the workflow-refinement finding (structural / protocol-family hypothesis)
  WORKFLOW-REFINE.md candidate-selector family Status line updated: h0025 REJECTED 2026-06-11, h0028 queued note added; family CLOSED.

### Summary

h0025 concluded REJECTED via captain strategic sibling-kill — no run. It is the 4th instance
of the candidate-selector self-anchored-scoring wall: scoring an artifact against the
candidate's OWN self-written Output Contract gives a confident-wrong candidate a perfect score,
so it fails both G9 axes (no candidate diversity, no independent IN-decision falsifier) at
propose. Follow-up routing is `stop`; the family is CLOSED, with only the adversarial re-fire
h0028 (which targets the G9 independence axes directly) left intentionally queued.
