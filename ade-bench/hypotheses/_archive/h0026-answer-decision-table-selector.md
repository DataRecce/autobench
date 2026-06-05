---
id: h0026
title: Answer Decision Table Selector -- run multiple answer candidates and choose by per-option local-check completeness plus mechanical answer transcription
status: conclude
kind: hypothesis
source: concept-candidate-selector-contract-scorer fan-out; tests the answer-task selector design, not another answer-task README rule. Forks the current @baseline solver protocol only as a declared protocol-family variant.
started: 2026-06-05T09:42:10Z
completed: 2026-06-05T13:34:38Z
verdict: REJECTED
score:
worktree:
archived: 2026-06-05T13:34:38Z
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
| G8 regression-canary coverage | PASS | Instruction is **gated** (fires only on answer-style tasks), so a full cross-family panel is not required; the smoke carries a trimmed 2-canary gate-off sample to prove the gate stays OFF: f1007 (f1 — closest family to the target) and asana001 (asana — structurally distant family), each an `@baseline` PASS (reward=1.0) from a non-target family. Panel trimmed at captain direction from 5 canaries to 2 (dropped airbnb001, ana-eng001, quickbooks002). Intercom omitted: `@baseline` has zero intercom passers (intercom001/002/003 all reward=0.0), documented in-spec. |

**For the captain:** Two WARNs, no FAILs → APPROVE. (1) G1 — confirm the new `## Protocol:` block shape is the intended form for a protocol-family hypothesis (the guideline's "exactly one `## Stage:`" wording predates the selector family). (2) G7 — this is the family's first smoke; verify the flip by inspecting f1011's committed answer string + the saved candidate decision tables, not the solver chatter, and confirm the 5 canaries stay PASS (gate-off proof). A canary drop is NO-GO even if f1011 flips.

## Smoke result

**Go/no-go: NO-GO (do not advance to full). One-line reason: the selector ran for real but
all three candidates converged on the same wrong answer (`ABDE` vs. correct `ADE`) and the
local-completeness scorer self-graded that wrong answer 6/6 — a self-anchored false-green, not
the inert narration we feared; the lever as written cannot catch a plausible-wrong option.**

Run dir: `runs/ade-bench-h0026-answer-decision-table-selector/a01f97caf6d6462e/`
(strict audit clean=3/3, tainted=0; `subagent-trace-manifest.json` captured=1 on all 3 cells;
`stratified_pass_at_1=0.6667` — a mixed number that just counts the 2 always-passing canaries
plus the 1 non-flipping target, not a meaningful headline).

| Task | Role | @baseline | h0026 | Flipped? | Distance / why |
|------|------|-----------|-------|----------|----------------|
| `ade-bench-f1011` | answer-style TARGET | 0.0 (FAIL) | **0.0 (FAIL)** | **NO** | 1 option wrong: grader runs 6 hidden `check_option_{a..f}` singular tests; 5 PASS, **`check_option_b` FAIL**. Committed answer `ABDE`; correct answer is `ADE`. Model **over-included option B**. |
| `ade-bench-f1007` | f1 gate-off canary | 1.0 (PASS) | **1.0 (PASS)** | held | Zero answer-selector markers in transcript — protocol gated OFF; baseline behavior. |
| `ade-bench-asana001` | asana gate-off canary | 1.0 (PASS) | **1.0 (PASS)** | held | Zero answer-selector markers in transcript — protocol gated OFF; baseline behavior. |

No canary regressed (AC-4 holds). The target did not flip and the deep-dive (below) shows the
failure is a property of the lever, not of execution — so the result is a **clean falsification**
of the answer-selector claim in its current form, matching AC-3's "selector cannot distinguish a
plausible wrong answer from a locally checked one" branch.

## Run result

- Tasks: 3 / 3 completed, 0 errored (`result.json`, `summary.json`).
- Rewards: f1011=0.0, f1007=1.0, asana001=1.0 (`per_trial_outcomes.json`).
- `rk audit --policy strict` → exit 0, `summary={clean:3, tainted:0, coverage_missing:0}`
  (`audit.json`). Score trusted only after this clean audit.
- `rk score` → `stratified_pass_at_1=0.6667` (2/3), `against_constant pass_rate=0.1875 → above`,
  `taint_status clean=3` (`score.json`).
- Subagent capture gate: all 3 cells have `subagent-trace-manifest.json` with `captured=1` (>0).
- Wall: ~28 min (10:36:48 → 11:05:07), trials=1, concurrency=1.

## Behavioral analysis

**Source of truth: the committed dbt model + saved candidate decision table, not the solver
chatter** (per the propose-stage G7 inert-risk WARN).

**The committed artifact.** The grader compiled and built the committed model `analysis__answer`
(`verifier/test-stdout.txt`: `OK created sql table model main.analysis__answer`). Its value is
`answer = 'ABDE'` (the literal appears 21× in the ensign rollout and matches the model the grader
ran). The grader then runs six hidden singular tests, one per option (`check_option_a..f`,
`expected_test_count=6`). Result: **5 PASS, `check_option_b` FAIL** → `actual_pass=5, actual_fail=1`
→ reward 0 (all-or-nothing). Since C and F (committed OUT) pass and A, D, E (committed IN) pass,
the only disagreement is **B: committed IN, ground truth OUT**. The correct answer is **`ADE`**.

**The pre-flagged inert risk did NOT materialize.** The model genuinely ran the protocol:
- It saved a full per-option decision table (candidate **C1**) with exactly the six README
  columns (option / local relation / exact local check + observed result / IN-OUT / one-line
  reason / transcribed answer string), recovered from the rollout.
- It ran real local-evidence SQL via `dbt show --inline` against the actual source/staging
  relations — column-existence probes for A (track/layout columns) and D (caution/safety/flag
  columns), a pit-stop duplication probe for C, and a `results.laps`/`status` vs `lap_times`
  join probe for B. These are independent local checks, not narration.
- The final ensign report states "Three independent local candidate tables all produced `ABDE`;
  the mechanical scorer selected candidate C1 with completeness 1/1, support 6/6, contradictions
  0, exact transcription 1." N>=3 candidates + a selection happened.

**Why it still failed — the real (and more interesting) failure mode.** This is a *self-anchored
false-green*, the exact pattern in memory `[[ade-bench-validation-self-anchored-false-green]]`.
For option B, the model's lap-completeness probe returned real evidence that incomplete/unfinished
laps exist in the data (`lap_count_mismatches=89`, `non_finished_results=5868`), and the C1 row
reads: *"joins only laps/races/pit stops; no results/status join despite results.laps/status_desc
available... Incomplete/unfinished result context is available but unused → IN."* That is a
plausible reading — but ground truth says B is OUT (the `analysis__lap_times` model's lap-time
handling is in fact acceptable on this axis). The selector's scoring criteria — completeness,
"support N/N", "contradictions 0", exact transcription — are all computed *against the candidate's
own local checks*. There is no independent oracle, so a uniformly-held plausible-but-wrong IN
decision scores 6/6 and wins. All three "independent" candidates shared the same misread of B and
converged on `ABDE`; the selector had nothing to break the tie toward `ADE`.

**Classification (AC-3 branches):** NOT inert-narration; NOT a transcription failure (the
committed string exactly matches the chosen table's "ABDE"); NOT instruction-inapplicable (the
protocol fired correctly). It is **"chose an unsupported table" / "all candidates produced equally
unsupported tables; the selector cannot distinguish a plausible wrong answer from a locally checked
one."** The missing ingredient is candidate *diversity* and an *independent* falsifier for an IN
decision — local-check completeness alone is self-anchored and cannot catch the one wrong option.

**Gate-off proof (AC-4).** Both canaries ran with **zero** answer-selector markers in their
transcripts (no candidate refs, no decision-table headers, no `analysis__answer`), confirming the
protocol is gated strictly to answer-style tasks; both stayed PASS = byte-for-byte baseline
behavior. No regression.

## Verdict

**NO-GO at the smoke gate — do not advance to full (captain decides).** The answer-selector
protocol-family lever is *falsified in its current form*: it executes faithfully (N>=3 candidates,
real local checks, saved tables, mechanical selection) but does not flip the one answer-style
target, because its completeness/support scoring is self-anchored and all candidates share the
same plausible-wrong reading of option B. Advancing to full would spend ~21 more tasks to confirm
a lever the single clean target already disproves. If the family is to continue, the next variant
must add (a) candidate *diversity* (force candidates to disagree on borderline options) and (b) an
*independent* falsifier for IN decisions rather than self-scored "support N/N" — otherwise it
repeats the self-anchored false-green. Canaries clean, so the gating design itself is sound.

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

**Update (captain revision before gate):** smoke canary panel trimmed from 5 to 2. Since the
lever is gated to answer-style tasks, a full cross-family panel is unnecessary with a single
flip target; the smoke now carries exactly 3 tasks — `ade-bench-f1011` (target), `ade-bench-f1007`
(f1 — closest gate-off tripwire), `ade-bench-asana001` (asana — distant-family gate-leakage
tripwire). Dropped airbnb001, ana-eng001, quickbooks002. Smoke spec comment block updated, smoke
spec re-frozen (full spec unchanged, not re-frozen), G8 gatekeeper row updated to reflect the
trimmed panel (still PASS). ETA: 3 tasks × ~9 min ≈ 27 min.

## Stage Report: smoke

- DONE: Smoke run audited clean (rk audit --policy strict) and scored, with subagent-trace-manifest.json captured > 0
  Run dir `runs/ade-bench-h0026-answer-decision-table-selector/a01f97caf6d6462e`; `rk audit --policy strict` exit 0, `summary={clean:3, tainted:0, coverage_missing:0}`; `rk score` `stratified_pass_at_1=0.6667`, `against_constant pass_rate=0.1875 → above`; all 3 cells `subagent-trace-manifest.json` `captured=1`.
- DONE: Per-target deep-dive backed by the COMMITTED artifact + canary gate-off check
  f1011 committed `analysis__answer = 'ABDE'` (grader compiled it); 6 hidden `check_option_*` tests → 5 PASS, `check_option_b` FAIL → correct answer `ADE`, model over-included B. Saved candidate table C1 (six README columns) + real `dbt show` local probes recovered from rollout: protocol fired for real, NOT inert. Both canaries (f1007, asana001) PASS with zero answer-selector markers = gated-off baseline behavior.
- DONE: Plain-words go/no-go for the captain led by the verdict + one-line reason
  `## Smoke result` leads with NO-GO + one-line reason; full flip/distance/why table + the self-anchored-false-green artifact read in `## Behavioral analysis`; `## Verdict` written. Captain decides advancement; not self-advanced.

### Summary

Smoke ran clean (3/3 completed, strict audit clean, captured>0). The answer-style target
`ade-bench-f1011` did NOT flip (reward 0.0, unchanged from @baseline). The pre-flagged inert risk
did not materialize — the committed artifact shows the model genuinely ran N>=3 candidates with
saved per-option decision tables and real local SQL probes. The failure is sharper and more useful
than inert: a single wrong option (B, committed IN; ground truth OUT → `check_option_b` FAIL),
caused by a self-anchored false-green — all three candidates shared the same plausible-wrong B
reading and the local-completeness scorer self-graded it 6/6, with no independent falsifier to
prefer the correct `ADE`. Both canaries held (gated OFF, baseline behavior), so the gating design
is sound but the selection criterion is. Recommendation: NO-GO; do not advance to full — the
single clean target already falsifies the lever as written. A follow-on variant would need
candidate diversity + an independent IN-decision falsifier.
