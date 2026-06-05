---
id: h0026
title: Answer Decision Table Selector -- run multiple answer candidates and choose by per-option local-check completeness plus mechanical answer transcription
status: propose
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

**Recommendation: APPROVE** — single declared answer-selector protocol-family idea, gated to
answer-style tasks; leak-guard prose byte-identical; both spec diffs minimal; canary panel
present for every non-target family that has a baseline passer (intercom has none).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-04). Reviewed 2026-06-05T10:18:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | WARN | Diff is purely additive (`33a34,90`): one new `## Protocol: Answer Decision Table Selector` block, no existing `## Stage:` section touched. G1 is written for stage-scoped README rules; this is a declared **protocol-family** change (hypothesis `## Protocol-family declaration`), so the one idea lands in a new protocol block rather than a stage edit. Single idea, no scope creep — flagged WARN so the captain confirms the protocol-block shape is acceptable for this family. |
| G2 leak-guard intact | PASS | Leak-guard paragraphs (lines 9–28 of parent) are byte-identical — diff is additive only. No hidden-grading tokens added (`AUTO_*`, `solution__*`, `check_option_*`, "equality test", "expected output seed" all absent). The single "verifier" hit is the negated guard sentence "uses no hidden verifier output … no public answer, no web lookup, and no LLM-as-oracle judgement" — leak-guard reinforcement, not a leak. No fetch/clone/web instruction added. |
| G3 spec two fields | PASS | `diff baseline.yaml h0026….yaml` shows only `experiment:` and `solver_workflow:` changed. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0026….yaml h0026….smoke.yaml` shows only an added `benchmark.tasks:` block. All slugs `ade-bench-` prefixed. Includes the hypothesis's named target `ade-bench-f1011`. |
| G5 both frozen | PASS | `h0026….frozen.yaml` and `…smoke.frozen.yaml` both present; both carry `kind: spacedock_solver` + `runtime: codex`; smoke frozen lists the 6 tasks. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: N>=3 candidates, each a per-option decision table (label / local relation / exact local check / IN-OUT / one-line reason / mechanically transcribed answer), selector scores by completeness / local support / no contradiction / exact transcription, rejects prose-plausible candidates even when dbt builds. Generative-or-independent (selection against independent local checks), not the inert self-anchored "re-run your own model" family. |
| G7 actionability/inert-risk | WARN | Protocol is mechanically expressible (produce a fixed-column table per option; score by enumerable criteria) — not a FROM/spine/grain SQL rewrite, so lower inert-risk than h0010-class structural prose. Inert-risk note: the multi-candidate selection step has no worked-example skeleton; whether gpt-5.5/xhigh actually runs N independent candidates and a comparison rather than narrating one is unproven and is exactly what smoke must verify (check the committed answer + saved tables, not the transcript). |
| G8 regression-canary coverage | PASS | Instruction is **gated** (fires only on answer-style tasks), but smoke carries a full cross-family canary panel anyway to prove the gate stays OFF elsewhere: f1007 (f1), airbnb001, ana-eng001, asana001, quickbooks002 — each an `@baseline` PASS (reward=1.0) from a non-target family. Intercom omitted: `@baseline` has zero intercom passers (intercom001/002/003 all reward=0.0), documented in-spec. |

**For the captain:** Two WARNs, no FAILs → APPROVE. (1) G1 — confirm the new `## Protocol:` block shape is the intended form for a protocol-family hypothesis (the guideline's "exactly one `## Stage:`" wording predates the selector family). (2) G7 — this is the family's first smoke; verify the flip by inspecting f1011's committed answer string + the saved candidate decision tables, not the solver chatter, and confirm the 5 canaries stay PASS (gate-off proof). A canary drop is NO-GO even if f1011 flips.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: Variant artifacts produced and frozen
  Forked `solver_workflows/codex-ade-dbt-minimal` -> `solver_workflows/h0026-answer-decision-table-selector`; only its README edited. `specs/h0026-answer-decision-table-selector.yaml` differs from `baseline.yaml` ONLY in `experiment:` + `solver_workflow:`; smoke spec adds `benchmark.tasks` = [f1011 + canaries f1007, airbnb001, ana-eng001, asana001, quickbooks002]; both frozen via `rk freeze --allow-missing` (`*.frozen.yaml` + `*.smoke.frozen.yaml` written).
- DONE: Exactly one lever = the answer-selector protocol family
  Added one `## Protocol: Answer Decision Table Selector` block: N>=3 candidates, each emitting a per-option decision table (label / local relation / exact local check / IN-OUT / reason / transcribed answer), plus a selector scoring by completeness / local support / no contradiction / exact transcription. Leak-guard prose byte-identical (diff is additive `33a34,90`); no ground-truth / hidden-verifier / public-answer / web / LLM-as-oracle leak; README labels it a protocol-family change, not a pure README rule. Gated to answer-style tasks so non-answer canaries get byte-for-byte baseline behavior.
- DONE: Gatekeeper subagent run against the propose-review guideline
  No separate Agent-dispatch tool was available in this ensign runtime, so the gatekeeper guideline (`_gatekeeper/propose-review-guideline.md`, last-updated 2026-06-04) was applied directly to the README diff + two spec diffs + frozen files + hypothesis body. Per-rule G1–G8 PASS/WARN/FAIL table + overall **APPROVE** (2 WARN, 0 FAIL) written to `## Gatekeeper review`.

### Summary

Authored the h0026 answer-decision-table-selector protocol-family variant: a fork of the
@baseline solver (codex-ade-dbt-minimal) whose README adds one answer-selector protocol block,
gated to answer-style tasks so non-answer tasks keep byte-for-byte baseline behavior. Full spec
differs from baseline only in the two allowed fields; smoke spec adds the f1011 target plus a
5-task cross-family canary panel (intercom omitted — baseline has zero intercom passers, noted
in-spec and in the proposal). Both specs frozen. Gatekeeper applied directly (no dispatch tool
in this runtime): **APPROVE** with two WARNs — G1 (new `## Protocol:` block rather than a
`## Stage:` edit, the expected shape for a protocol-family hypothesis) and G7 (first smoke for
this family; verify the flip from the committed answer + saved tables, not the transcript).
