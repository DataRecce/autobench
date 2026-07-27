---
title: Re-baseline the champion on gpt-5.6-sol @ xhigh — model swap with the solver README held byte-identical
status: propose
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

**Addendum (found at propose, 2026-07-27): it is three variables, not two.** The codex CLI on
`$PATH` has been upgraded since every board in the comparison set — `provenance.agent_cli_hash`
moves from `d3be844c…` (spd0038 anchor, spd0013 ×2, spd0011, spd0012 — all of them) to
`134063e1…` = `codex-cli 0.145.0`. Evidence and reasoning in `## Propose artifacts` → AC-1b. So the
delta this board produces is **model × plugin × codex-CLI**, and none of the three is separable from
the other two by this run alone. This widens the confound but does not change its shape: the
"≤ ±3 cells is uninterpretable / ≥ +6 cells needed" thresholds above still hold, and the same
single disambiguating arm (spd0038 + gpt-5.5, re-run *today* so plugin AND CLI are current) now
isolates model alone rather than just plugin — which makes that arm more valuable, not less. Note
this is not a defect introduced here: it is drift in the machine that any board run today inherits.
Two things did NOT move and are worth stating: `provenance.image_digest`
(`sha256:224133f0…4742`, the task image) is identical to the anchor, and the solver README is
byte-identical (AC-2).

## Variance ceiling (READ WITH THE ABOVE)

The last four full boards read 27 / 26 / 25 / 24 — statistically one board. At `trials=1` a single
draw cannot resolve anything below roughly +/- 3 cells. This run is therefore **directional
evidence, not a demonstrated lift**, and the verdict must say so. A promote decision on this
entity's number alone would repeat the single-draw error recorded in the DAB characterization
(a lucky draw read as a new champion). If the board comes back ambiguous, the answer is a
`trials=3` re-run compared on per-cell hold-rates, not a re-read of this one.

## Propose artifacts (AC-1 / AC-2 / AC-4 evidence)

Authored at propose, 2026-07-27. Spec: `specs/spd0042-rebaseline-gpt56sol-xhigh.yaml` →
`specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml` (frozen with
`uv run --project ../razorback rk freeze --allow-missing`, `RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock`,
`RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml`).

### AC-1 — the model is the only spec variable ✅

`diff runs/spd0038-compose-6-stabilizers-full/fb10902ab7d9ffa7/spec.frozen.yaml specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml`

```
2c2
< experiment: spd0038-compose-6-stabilizers-full
---
> experiment: spd0042-rebaseline-gpt56sol-xhigh
6c6
<   model: gpt-5.5
---
>   model: gpt-5.6-sol
24c24
<   sealed_hash: ae60c64378b498a3f3f0fd7484870c18
---
>   sealed_hash: 65b01e4bb11ff1c723b6d2908235ad1d
107,108c107,108
<   agent_cli_hash: sha256:d3be844c45c4fd89392536e56e1010963f94785592596b50cd0c45bb8a341406
<   harness_git_sha: b64e30fa8bca83b20a295a21ec6c9758128832cf
---
>   agent_cli_hash: sha256:134063e133f0b4244fa3b251acf973d4fe4b4aeeacbdc135211bf480f59f1477
>   harness_git_sha: db6c2e68223a21982c269f9f1f5723c784ea50d0
```

Five hunks, classified:

| Hunk | Kind | Verdict |
|---|---|---|
| `experiment:` | authored | allowed — required, names the run-dir |
| `agent.model: gpt-5.5 → gpt-5.6-sol` | authored | **the one variable** (AC-1 gate note waives the standing reject-check) |
| `agent.sealed_hash` | freeze-derived | not a knob — the seal covers the agent block, so it MUST move when `model` moves |
| `provenance.agent_cli_hash` | environment-observed | not a knob — see the AC-1b drift note below |
| `provenance.harness_git_sha` | environment-observed | benign — this is the **autobench repo** HEAD, 35 commits of entity/spec bookkeeping since the anchor was frozen (`b64e30f` = the spd0038 merge-validation smoke commit); zero behavioral surface |

No other field moved. `solver_workflow`, `reasoning_effort: xhigh`, `agent.kind: spacedock_solver`,
`runtime: codex`, `max_turns: 200`, `override_timeout_sec: 2400.0`, `sampling.temperature: 0.0`,
`trials: 1`, `concurrency.trials: 4`, `benchmark.kind: harbor-local`, all 60 `benchmark.tasks`, and
`provenance.image_digest: sha256:224133f0…4742` are byte-identical to the anchor. Source-level diff
(`specs/spd0038-compose-6-stabilizers.full.yaml` vs `specs/spd0042-…​.yaml`, ABOUTME headers excluded)
is exactly the two authored lines.

*Wording note (gatekeeper-flagged):* AC-1 above says the spec differs in "the concurrency/trials
knobs the captain set". It does not — the captain's `trials: 1` / `concurrency.trials: 4` were
ALREADY the anchor's values, so those knobs did not move. AC-1 is satisfied more tightly than it
asks. The AC text is left as the captain wrote it; the hunk table is the accurate account.

### AC-1b — UNPLANNED third variable: the codex CLI moved (surfaced, not papered over) ⚠️

`provenance.agent_cli_hash` is `sha256(the codex binary on $PATH)`
(`razorback/src/razorback/provenance/resolvers.py:97`). Every prior spider2-dbt board — the
spd0038 anchor, `spd0013-rebaseline-v022`, `spd0013-lean-lag-period-over-period`, spd0011, spd0012 —
carries `d3be844c…`. This spec froze `134063e1…`, i.e. `codex-cli 0.145.0`, currently at
`/home/kent/.npm-global/bin/codex`. The local codex CLI has been upgraded since every board in the
comparison set.

This is a **third moving variable**, not a second. It is also not fixable at propose: the old binary
is not on disk, and `gpt-5.6-sol` plausibly requires the newer CLI. It is recorded here so `analyze`
attributes honestly — see the addendum in `## Known confound`.

### AC-2 — the solver README is provably not a variable ✅

1. Frozen-spec hash matches the champion literal exactly:
   `specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml:12` →
   `solver_workflow_content_hash: sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f`
   (and `:112` `provenance.solver_workflow_hash` the same). Identical to the anchor frozen spec.
2. Independently recomputed, not just read back — `resolve_solver_workflow_hash(Path('solver_workflows/spd0038-compose-6-stabilizers'))`
   returns `sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f`. Match.
3. **No fork exists.** `ls -d solver_workflows/*spd0042*` → `No such file or directory`.
   `git status --short -- solver_workflows/` → empty (nothing modified, nothing untracked).
   `diff -r` against "the dir this spec points at" is vacuous by construction: the spec points at
   `solver_workflows/spd0038-compose-6-stabilizers` itself, the same path the anchor used.
4. The dir is untouched since it was created: last commit touching it is `d95880e` (2026-06-29,
   the spd0038 ideate commit), which predates the anchor run. `git diff --stat HEAD --` on it is empty.
   `sha256sum README.md` = `4a14efdcb80a1266f29d1005a17bef9d0aafbaabdbc91d482be06f50aea7171a` (409 lines).
5. Leak-guard intact (trivially — byte-identical README): the Classify router still reads
   "Run this router on **oracle-free signals only** … Never read or guess gold values"
   (`solver_workflows/spd0038-compose-6-stabilizers/README.md:86-88`). No `ground_truth.csv` and no
   `db_description_withhint` reference anywhere in the file.

### AC-4 — plugin pin recorded, not assumed ✅

Captured 2026-07-27 at propose (AC-4 also requires a re-capture at launch time in `## Run result`):

```
$ git -C spacedock describe --tags
v0.26.0-pre0
$ git -C spacedock rev-parse HEAD
601c3f53e388a19814807962302a01f53db61395
$ git -C spacedock status --short
(empty — clean tree)
```

Matches the captain-set pin. One note for the launch-time re-capture: `git status --short` in the
**parent** repo shows ` M spacedock`. That is the submodule *pointer* differing from the parent's
recorded gitlink (`f96f4a1a`), NOT a dirty plugin tree — the plugin tree itself is clean, which is
what AC-4 asks about. The pin is deliberate; do not "resolve" it by checking out `f96f4a1a`.

### Not done at propose, by design

- **No smoke spec, smoke SKIPPED** — anchor exemption (README Stages line 457); a whole-board model
  swap has no targets and no canaries. No `--explain` verification, because that step exists to audit
  a smoke `exclude_tasks` selection and there is no smoke selection here. The full task list is
  proved identical to the anchor by the AC-1 diff instead.
- **No run launched** — `rk run` belongs to `full`, behind the captain's gate.
- **Model-id sanity** (cheap pre-flight, since a bad model string would burn the whole board):
  `gpt-5.6-sol` is not a guess — it has completed real runs on the DAB benchmark
  (`dab/runs/codex-dab-d22-g56sol-h1|h2|h6/*/spec.frozen.yaml`).

## Gatekeeper review

**Recommendation: APPROVE** — the "one variable is the model" property holds under independent
verification: the README is provably byte-identical (hash recomputed, no fork, clean git), every
unwaived spec knob is preserved, and the only undisclosed-field risk (`agent_cli_hash`) is
environment drift the entity surfaced itself.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-07-27.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke; smoke SKIPPED here
per anchor exemption ⇒ `propose → full`).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | Empty README diff is the REQUIREMENT here (model swap). Verified: `ls -d solver_workflows/*spd0042*` → no such file; `git status --short -- solver_workflows/` → empty; `git diff --stat HEAD --` on the champion dir → empty; last commit `d95880e` (2026-06-29) predates the anchor run. Exactly one authored knob moved (`agent.model`). |
| G2 leak-guard (hidden gold) | PASS | README byte-identical (`sha256sum` = `4a14efdc…7171a`, 409 lines; workflow hash recomputed = anchor's). No-fetch prose intact verbatim at `README.md:11-15` (`curl`/`wget`/`git clone`/`git ls-remote` appear ONLY inside the prohibition); oracle-free router intact at `:86-88`. All 17 `gold` hits are prohibitions/definitions — `:30` "Gold table names and their exact columns are NOT given to you", `:88` "Never read or guess gold values". Zero hits for `expected_`, `answer_key`, `ground_truth`. |
| G3 spec two fields | WARN | `model:` waived per AC-1 gate note. Independently diffed vs `runs/spd0038-…/fb10902ab7d9ffa7/spec.frozen.yaml` + parsed key-by-key: exactly 5 fields moved, no undisclosed field. Preserved: `kind: spacedock_solver`, `runtime: codex`, `reasoning_effort: xhigh`, `trials: 1`, `concurrency.trials: 4`, `max_turns: 200`, `temperature: 0.0`, `image_digest: sha256:224133f0…4742`, all 60 tasks (`tasks==tasks` → True). **WARN:** `provenance.agent_cli_hash` is a third uncontrolled variable (see captain note). |
| G4 smoke narrows tasks only | N/A | No smoke spec by design — anchor exemption, `hypotheses/README.md:457`; a whole-board swap has no targets/canaries to narrow to. |
| G5 both frozen | PASS | Full frozen exists (`specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml`, 2026-07-27 12:22) carrying `kind: spacedock_solver` (`:4`) and `runtime: codex` (`:5`). Smoke-frozen half N/A per G4. |
| G6 resolver fidelity | PASS | Claim = "model swaps, README held byte-identical." Artifacts match exactly: `agent.model: gpt-5.5 → gpt-5.6-sol` is the sole authored knob; `solver_workflow_content_hash` at `:12` = `sha256:607dec29…011f`, independently recomputed via `resolve_solver_workflow_hash()` → match True, and identical to the anchor's `solver_workflow_hash`. No inserted prose, no scope creep, no self-anchored check added. |
| G7 actionability/inert-risk | PASS | Class = **config knob**, not prose — a model swap cannot be acknowledged-and-skipped, so the gpt-5.5/xhigh inert-prose risk G7 exists for does not apply. Model-id de-risked: `gpt-5.6-sol` has 31 completed frozen specs under `dab/runs/*g56sol*/`, so it is not a string guess that would burn the board. |
| G8 regression-canary coverage | N/A | Not a gated-vs-generative instruction. The change fires on all 60 cells AND the run IS the full 60-task board, so every currently-passing `@baseline` cell is its own canary — coverage is total by construction, and the targets-only blindspot G8 guards against cannot exist. |
| G9 selector independence | N/A | No multi-candidate / selector protocol declared; README unchanged from the control. |
| G10 self-correcting false-positive | N/A | No validate-and-fix lever authored. Any check prose in the README is the champion's and is already present in the 26/60 control, so it is not a variable. |

**For the captain:** Auto-approved to `full`; I confirmed the anchor is `@baseline` =
`runs/spd0038-…/fb10902ab7d9ffa7` and the frozen diff is exactly the 5 hunks the entity discloses —
nothing hidden. On the AC-1b judgement you asked for: **the disclosure is adequate and should NOT
halt.** `agent_cli_hash` is environment-observed, not an authored knob, so it is outside G3's scope;
it is unfixable at propose (old binary gone); and it is symmetric — the proposed spd0038+gpt-5.5
disambiguating arm run today inherits the same plugin AND CLI, so it still cleanly isolates the
model. I verified the drift is broader than stated: **all 78** prior run frozen specs carry
`d3be844c…`, vs this spec's `134063e1…` (= `codex-cli 0.145.0`, hash confirmed against
`/home/kent/.npm-global/bin/codex`). Two things to weigh before spending the board:
(1) **experiment order** — with three confounds the entity needs ≥+6 cells (≥32/60) to say anything,
and the last four boards read 27/26/25/24, so an uninterpretable result is the likely outcome;
running the gpt-5.5 control arm on today's plugin+CLI *first* would make this board interpretable at
±3 instead of +6. That is a budget/ordering call for you, not an integrity defect, so I did not FAIL
it. (2) `provenance.plugins: []` in **both** frozen specs — the v0.22 → v0.26.0-pre0 shift leaves
**no trace in any artifact**, so the AC-4 launch-time capture is the only record of the largest
confound; make sure it actually lands in `## Run result`. Plugin pin verified clean at
launch-eligible state: `v0.26.0-pre0` @ `601c3f53e388a198…`, `git -C spacedock status --short`
empty. Minor: AC-1's prose says the spec differs in "the concurrency/trials knobs the captain set" —
those did **not** move (both identical to the anchor); the hunk table below it is correct.

*(Recorded by the propose ensign from the gatekeeper subagent's returned block. The gatekeeper was
run read-only — it modified no files, per the guideline's "must NOT modify any file other than
appending its review block".)*

## Smoke result

SKIPPED — anchor exemption (README Stages line 457). See `## Pre-smoke Decision-Fork Probe`.

## Run result

*(empty until `full`.)* The spec-level evidence AC-1 / AC-2 / AC-4 ask to be pasted here was
produced at `propose` and lives in `## Propose artifacts` above — the frozen spec is immutable, so
that evidence does not need re-deriving. Two things the `full` ensign still MUST capture HERE at
launch time:
1. **AC-4 re-capture at launch:** `git -C spacedock describe --tags` / `rev-parse HEAD` /
   `status --short`, taken at the moment `rk run` starts. This is not redundant with the propose
   capture — the gatekeeper flagged that `provenance.plugins: []` in the frozen spec, so the plugin
   version leaves **no trace in any run artifact** and this manual capture is the ONLY record of the
   largest confound.
2. **AC-3:** `rk audit <run-dir> --policy strict` on the same run-dir as `rk score`.

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Author + freeze the FULL spec specs/spd0042-rebaseline-gpt56sol-xhigh.yaml with model: gpt-5.6-sol, reasoning_effort: xhigh, trials: 1, concurrency.trials: 4, and solver_workflow: pointing at the UNCHANGED ./solver_workflows/spd0038-compose-6-stabilizers — then paste into the entity a diff of the frozen spec vs runs/spd0038-compose-6-stabilizers-full/fb10902ab7d9ffa7/spec.frozen.yaml proving NO field other than experiment/model/trials/concurrency moved (AC-1).
  `## Propose artifacts` → AC-1. Frozen diff = 5 hunks: `experiment`, `model` (the one variable), plus 3 non-knob fields (`sealed_hash` — derived, MUST move when model moves; `agent_cli_hash` + `harness_git_sha` — environment-observed). trials/concurrency did NOT move: the captain's 1/4 were already the anchor's values. Source-to-source diff is exactly the 2 authored lines.
- DONE: Prove the solver README is not a variable (AC-2): confirm the frozen spec's solver_workflow_content_hash equals sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f, confirm NO new solver_workflows/ dir was forked or edited for this hypothesis, and paste both proofs into the entity. A hash mismatch is a HARD STOP — report it, do not improvise a fix.
  `## Propose artifacts` → AC-2. Hash matches, and was independently RECOMPUTED via `resolve_solver_workflow_hash()` rather than only read back. No fork: `ls -d solver_workflows/*spd0042*` → no such file; `git status --short -- solver_workflows/` empty; dir untouched since `d95880e` (2026-06-29), which predates the anchor run.
- DONE: Record the plugin pin (AC-4) and run the gatekeeper: capture git -C spacedock describe --tags, rev-parse HEAD, and an empty status --short into the entity, then dispatch the gatekeeper subagent per _gatekeeper/propose-review-guideline.md and write its per-rule PASS/WARN/FAIL table plus APPROVE/REVISE/REJECT into '## Gatekeeper review'.
  `## Propose artifacts` → AC-4 (`v0.26.0-pre0` @ `601c3f53e388a198…`, tree clean) and `## Gatekeeper review` (**APPROVE**; 5 PASS / 1 WARN / 4 N/A; zero FAIL). Read-only gatekeeper: it re-ran every check itself and modified no files.
- SKIPPED: smoke spec, `--explain` selection check, smoke-set table
  Anchor exemption (hypotheses/README.md:457) — a whole-board model swap has no targets and no canaries; captain-approved deviation #2 in the dispatch.
- SKIPPED: launching the run
  `rk run` belongs to `full`, behind the captain's gate — dispatch deviation #4.

### Summary

Authored and froze the full-board spec; the model is the only authored variable and the champion
solver README is provably byte-identical (hash independently recomputed, no fork, dir untouched
since before the anchor run). Gatekeeper returned APPROVE with one WARN and zero FAILs.

One finding the captain should see before spending the board: **the confound is three variables, not
two.** Beyond the known model × plugin pair, `provenance.agent_cli_hash` shows the local codex CLI
was upgraded (`d3be844c…` → `134063e1…` = codex-cli 0.145.0) since **every** prior board — the
gatekeeper independently confirmed all 78 prior run specs carry the old hash. Recorded as AC-1b and
as an addendum to `## Known confound`. It is unfixable at propose (old binary gone) and symmetric
with the disambiguating arm, so it does not block — but the gatekeeper's captain note argues the
gpt-5.5 control arm on today's plugin+CLI should arguably run FIRST, since it would make this board
interpretable at ±3 cells instead of the ≥+6 the triple confound now demands.
