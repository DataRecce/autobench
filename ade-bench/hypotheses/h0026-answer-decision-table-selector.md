---
id: h0026
title: Answer Decision Table Selector -- run multiple answer candidates and choose by per-option local-check completeness plus mechanical answer transcription
status: hypothesis
kind: hypothesis
source: concept-candidate-selector-contract-scorer fan-out; tests the answer-task selector design, not another answer-task README rule. Forks the current @baseline solver protocol only as a declared protocol-family variant.
started: 2026-06-05T09:42:10Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Answer-style tasks can fail even when the output shape is correct, because the committed
answer string is assembled from plausible narrative rather than a decisive local check per
option. A multi-candidate protocol can produce several plausible strings; the missing lever is
to choose the candidate whose answer is mechanically supported by the best local decision
table.

**Falsifiable claim:** for answer-style tasks, run `N >= 3` candidates. Each candidate must
produce a per-option decision table before committing the answer:

- option label;
- local file/relation inspected;
- exact local check to run or read;
- IN/OUT decision;
- one-line reason tied to the local check;
- final answer string mechanically transcribed from the IN rows.

The selector scores candidates by table completeness, absence of unsupported IN decisions,
absence of contradictory local evidence, and exact string transcription. A candidate that
answers from prose plausibility, omits a listed option, includes an option with no local
support, or commits a string that does not match its table is rejected even if the dbt model
builds.

The claim passes smoke if the selected answer flips the answer-style target or shows a
strictly better per-option local evidence ledger than the first candidate without harming
non-answer canaries. It is falsified if all candidates produce equally unsupported tables, or
if the selector cannot distinguish a plausible wrong answer from a locally checked one.

## Protocol-family declaration

This is a **protocol-family change**, not a solver-README-only hypothesis. It adds multiple
candidate answer solves and a post-candidate selector that chooses one final answer based on
local table quality and transcription. It must be labeled as an answer-selector protocol
family; do not report it as a pure README independent-variable change.

## Target datasets

Primary smoke target:

- `ade-bench-f1011` -- analysis/answer-style task where the local model SQL and source/staging
  relations can support or reject each listed option.

No other known active target is the same clean answer-style shape, so the smoke should carry
canaries to prove the answer selector is gated off elsewhere:

- `ade-bench-f1007` -- same broad f-series family but not the answer decision-table target.
- `ade-bench-airbnb001`
- `ade-bench-ana-eng001`
- `ade-bench-asana001`
- `ade-bench-quickbooks002`

Intercom cannot supply a passing canary if the current baseline still has zero intercom
passers; document that at propose if true.

## Acceptance criteria

**AC-1 -- Candidate decision tables are complete.** Every `f1011` candidate writes one row per
listed option before committing the final answer SQL. The selector artifact preserves all
candidate tables and the chosen table.

**AC-2 -- Selection is local and mechanical.** The scorer uses only the task instruction,
local model SQL, local source/staging data, installed packages, and committed candidate
artifacts. It rejects hidden verifier output, public answers, web search, and LLM-as-oracle
reasoning. The final answer string must exactly equal the ordered IN rows from the chosen
table.

**AC-3 -- Smoke flips or cleanly falsifies the answer selector.** The selected candidate
should flip `ade-bench-f1011` to pass before any full run. If `f1011` does not flip, the
deep-dive must identify whether the chosen table was unsupported, the local evidence was
insufficient, or the candidate tables were correct but the final SQL transcription failed.

**AC-4 -- Applicability gate prevents regressions.** Non-answer canaries should have no extra
answer-table selection behavior and must remain passing. Any canary regression is NO-GO even
if `f1011` improves.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
