---
title: Re-baseline the champion on gpt-5.6-sol @ xhigh — model swap with the solver README held byte-identical
status: hypothesis
kind: hypothesis
source: "captain-directed (2026-07-27). spd0039 closed NEEDS-PHASE2-readme-exhausted: the README-lever program is spent at ~26/60 with a ~31/60 stabilization ceiling, and the leaderboard top-1 is ~65%. A stronger solver model is the Phase 2 lever that scoping doc (_artifacts/group3-model-swap-scoping-2026-06-29.md) was written for. This is the first model-swap arm: champion spd0038 solver README UNCHANGED, model gpt-5.5 -> gpt-5.6-sol, effort held at xhigh."
started: 2026-07-27T12:19:42Z
completed:
verdict:
score: 0.9
worktree:
id: spd0042
---

## Hypothesis

**Claim (falsifiable):** swapping the solver model from `gpt-5.5` to `gpt-5.6-sol` at unchanged
`reasoning_effort: xhigh`, with the champion solver README held byte-identical, raises the
spider2-dbt board above the champion's 26/60 by more than the flaky-band noise (>= +4 cells).

**The one variable is the MODEL.** This entity authors NO solver README. It reuses
`solver_workflows/spd0038-compose-6-stabilizers` verbatim (content hash
`sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f`). Any diff in that
directory is a methodology failure, not a variant.

**Target queries:** none — this is a whole-board re-baseline, not a per-cell lever. Every one of
the 60 gradeable cells is in scope; there are no targets and no canaries to name.

### Configuration (captain-set, 2026-07-27)

| Knob | Value | Note |
|---|---|---|
| `model` | `gpt-5.6-sol` | the one variable; anchor was `gpt-5.5` |
| `reasoning_effort` | `xhigh` | HELD — same as all three reference boards |
| `solver_workflow` | `./solver_workflows/spd0038-compose-6-stabilizers` | UNCHANGED, byte-identical to champion |
| `trials` | 1 | captain: "trials=1 first" |
| `concurrency.trials` | 4 | captain-set |
| spacedock plugin | pinned `v0.26.0-pre0` @ commit `601c3f53` | captain-set; submodule tree verified clean at file time |

### Reference boards (all gpt-5.5 @ xhigh, trials=1, plugin v0.22)

| Run | Score | Note |
|---|---|---|
| `runs/spd0038-compose-6-stabilizers-full/fb10902ab7d9ffa7` | **26/60 = 0.4333** | `@baseline`; 0 errors; the control for this entity |
| `runs/spd0013-rebaseline-v022/d826c153beb3134b` | 25/59 = 0.4237 | 1 EXC (recharge001 timeout); ~26/60 effective |
| `runs/spd0013-lean-lag-period-over-period/7f3278d0d61d2577` | 27/60 = 0.4500 | plugin v0.12 — NOT comparable, do not cite as the bar |

## Pre-smoke Decision-Fork Probe

**Not applicable — no local fork exists to probe.** This is not a flipped-task follow-up and not a
README rule; there is no prompt-level fork a subagent could exercise. The mechanism under test is a
model swap, which is only observable in a real run.

**Smoke is SKIPPED (`propose -> full`)** under the README's anchor exemption (Stages, line 457:
"Anchor / first run skips `smoke`"). A smoke set is composed of targets + canaries chosen for a
gated lever; a whole-board model swap has neither, so a subset run would answer nothing the full
board does not. The full board at trials=1 IS the cheapest check that can fail here.

## Acceptance criteria

**AC-1 — The model is the only spec variable.** The full spec differs from the spd0038 anchor
frozen spec ONLY in `experiment:`, `model:`, and the concurrency/trials knobs the captain set;
`solver_workflow:`, `reasoning_effort: xhigh`, `agent.kind: spacedock_solver`, `runtime: codex`,
and the benchmark/task set are unchanged.
Verified by: `diff runs/spd0038-compose-6-stabilizers-full/fb10902ab7d9ffa7/spec.frozen.yaml specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml` pasted into `## Run result`.

> **Gate note — AC-1 deliberately overrides the standing `propose` reject-check.** That check reads
> "the FULL spec differs from the anchor in anything other than `experiment:` + `solver_workflow:`".
> This entity changes `model:` BY DESIGN, on captain instruction. The propose gate and the
> gatekeeper MUST NOT reject on that rule. Every other reject-check (leak-guard intact,
> `agent.kind: spacedock_solver`, `runtime: codex`) applies unchanged.

**AC-2 — The solver README is provably not a variable.** The `solver_workflow_content_hash` in
this run's frozen spec equals `sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f`,
and `diff -r solver_workflows/spd0038-compose-6-stabilizers <the dir this spec points at>` is empty.
Verified by: both commands run and their output pasted into `## Run result`. A mismatch is a hard stop.

**AC-3 — The score is paired with a clean strict audit.** `rk audit <run-dir> --policy strict` is
run on the same run-dir as `rk score`, and shows 0 `coverage_missing` and 0 tainted cells. Any
`AgentTimeoutError` / usage-limit / backend-degradation cell is named and excluded from the
headline rather than silently counted as a fail.

**AC-4 — The plugin version is recorded, not assumed.** `git -C spacedock describe --tags` and
`git -C spacedock rev-parse HEAD` are captured at launch time into `## Run result`, and
`git -C spacedock status --short` is confirmed empty. A dirty plugin tree invalidates the run.

**AC-5 — The verdict names the model x plugin confound and does not attribute the delta to the
model alone.** See `## Known confound` below; the verdict must state which part of any delta
is unattributable.

## Known confound (READ BEFORE INTERPRETING THE RESULT)

The `@baseline` control (26/60) was produced under spacedock plugin **v0.22**. This run is pinned
to **v0.26.0-pre0** on captain instruction. **Two variables therefore move at once: model AND
plugin.** On the DAB benchmark, plugin version alone shifted scores by ~0.04 (~2-3 cells on a
60-cell board) — the same magnitude as the effect under test.

Consequences, to be honored at `analyze`:
- A delta of +/- 3 cells or less is **uninterpretable**. It cannot be assigned to the model.
- Only a LARGE move (>= +6 cells, ~32/60) survives the confound as probable model signal.
- The clean disambiguator is a second arm: **spd0038 + gpt-5.5 + plugin v0.26.0-pre0**, which
  isolates the plugin. It is NOT part of this entity; `## Follow-up Routing` decides whether to
  spend it once this board lands.

## Variance ceiling (READ WITH THE ABOVE)

The last four full boards read 27 / 26 / 25 / 24 — statistically one board. At `trials=1` a single
draw cannot resolve anything below roughly +/- 3 cells. This run is therefore **directional
evidence, not a demonstrated lift**, and the verdict must say so. A promote decision on this
entity's number alone would repeat the single-draw error recorded in the DAB characterization
(a lucky draw read as a new champion). If the board comes back ambiguous, the answer is a
`trials=3` re-run compared on per-cell hold-rates, not a re-read of this one.

## Gatekeeper review

## Smoke result

SKIPPED — anchor exemption (README Stages line 457). See `## Pre-smoke Decision-Fork Probe`.

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
