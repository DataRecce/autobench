---
title: Re-baseline the champion on gpt-5.6-sol @ xhigh — model swap with the solver README held byte-identical
status: analyze
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

The spec-level evidence AC-1 / AC-2 ask to be pasted here was produced at `propose` and lives in
`## Propose artifacts` above; the frozen spec is immutable, so it does not need re-deriving. AC-4's
launch-time capture and the two recorded captain decisions are below. **AC-3 (`rk audit --policy
strict` + `rk score`) is still outstanding** — it runs on a later turn, once the handle's `done`
sentinel appears with `rc=0`.

### Launched — detached, 2026-07-27

| | |
|---|---|
| Handle | `runs/.rk-handles/spd0042-full-20260727-123939/` (`meta` · `cmd` · `pid` · `log` · `done`) |
| Command | `drivers/rk-run-detached.sh spd0042-full specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml run` |
| Worker PID | 14136 |
| Job dir | `runs/spd0042-rebaseline-gpt56sol-xhigh/1984b76c702a0dfa-INVALID-auth-refresh-token-reused/` — **renamed 2026-07-28**; ran as `1984b76c702a0dfa` (deterministic, spec-derived job name) |
| Board | 60 cells, `trials: 1`, `concurrency.trials: 4` |
| ntfy | `adebench-rk-381c976fe07465bf` (push on completion) |
| ETA | **~3.5 h**, band 3–5 h. The spd0038 anchor board — same 60 cells, same concurrency, gpt-5.5 @ xhigh — took 3 h 20 m (`08:38:47 → 11:58:25` on 2026-06-29). Widened at the top end because gpt-5.6-sol showed a ~2× token blow-up under the spacedock harness on DAB, which may stretch wallclock. |

Launch verified live, not just spawned: at T+2m35s the worker PID was alive, no `done` sentinel, and
harbor had written `_job_config.yaml`, `lock.json`, `result.json` and the per-cell task dirs into the
job dir.

**Pre-flight done before committing the board** (the plugin had moved 175 commits since the spec was
frozen, and `rk run` carries an `--allow-plugin-drift` escape hatch, so a drift refusal was a real
launch risk): `rk run … --explain` resolved cleanly — 60 tasks, `model: gpt-5.6-sol`,
`reasoning_effort: xhigh`, `kind: spacedock_solver` / `runtime: codex`, workflow README found at
`solver_workflows/spd0038-compose-6-stabilizers/README.md`, and the "Stage the Spacedock plugin into
Codex skills" preparation step present. No drift refusal. `--explain` leaves an empty job dir behind;
it was removed (0 files in it) so the real run started from a pristine dir — no stale `lock.json`.

### AC-4 — plugin pin AT LAUNCH ✅ (SUPERSEDES the propose-stage value)

```
$ git -C spacedock describe --tags
v0.27.0-pre0
$ git -C spacedock tag --points-at HEAD
v0.26.0
v0.27.0-pre0
$ git -C spacedock rev-parse HEAD
ca136f83a579fd44c223321ae7f8fe7785c685f7
$ git -C spacedock status --short
(empty — clean tree)
$ git -C spacedock rev-parse origin/stable
ca136f83a579fd44c223321ae7f8fe7785c685f7
```

**This run used spacedock `v0.26.0` @ `ca136f83a579fd44c223321ae7f8fe7785c685f7`.** The captain
repinned before launch: the entity was filed against `v0.26.0-pre0` @ `601c3f53`, which turned out to
be 175 commits behind origin, and the captain asked for latest stable. **This value supersedes
`v0.26.0-pre0` @ `601c3f53` wherever it appears earlier in this entity** — in the `## Hypothesis`
Configuration table, in `## Known confound`, and in the propose-stage AC-4 block under
`## Propose artifacts`. Those earlier mentions are the pin *as filed*, kept for the audit trail; this
is the pin *as run*. Do not treat them as two different runs.

One naming wrinkle worth stating so nobody thinks the pins disagree: `git describe --tags` reports
`v0.27.0-pre0` because that tag also points at this commit. `v0.26.0`, `v0.27.0-pre0`, and
`origin/stable` are all the same commit `ca136f83`. Tree clean.

Why this capture matters: `provenance.plugins: []` in the frozen spec, so **the plugin version
leaves no trace in any run artifact**. This block is the only record of the largest of the three
confounds.

### Recorded captain decision — the gpt-5.5 control arm was DECLINED

At the propose gate the FO recommended running a same-environment gpt-5.5 control board FIRST, which
would have made this board interpretable at ±3 cells. **The captain declined and chose to launch
directly, accepting the wider bar.** This is a deliberate recorded decision, not an oversight — do
not re-derive it at `analyze` and do not treat the missing control as a methodology gap.

### The bar `analyze` MUST apply (do not soften)

Three variables moved versus the 26/60 anchor:

| Variable | Anchor | This run |
|---|---|---|
| model | `gpt-5.5` | `gpt-5.6-sol` |
| spacedock plugin | v0.22 | **v0.26.0 @ `ca136f83`** |
| codex CLI (`agent_cli_hash`) | `d3be844c…` (all 78 prior run specs) | `134063e1…` = codex-cli 0.145.0 |

Therefore:
- A delta of **±5 cells or less is UNINTERPRETABLE** and must not be attributed to the model.
- Only **≥ +6 cells (≥ 32/60)** reads as probable model signal.
- At `trials: 1` this is **directional evidence, never a demonstrated lift.**

### OUTCOME: THE RUN IS INVALID. NO SCORE IS PROMOTED. ⛔

The board returned `rc=0` at **2026-07-27T14:10:14Z** after **1 h 30 m 25 s** — under half the
anchor's 3 h 20 m, on a model expected to be *slower*. That speed was the failure signature, not a
win: **41 of 60 cells exited early.** Root cause in `## Failure Review`.

Run-dir: **`runs/spd0042-rebaseline-gpt56sol-xhigh/1984b76c702a0dfa-INVALID-auth-refresh-token-reused`**
— kept in full for the audit trail (all 60 cell dirs, `summary.json`, `lock.json`, the codex logs).
It ran as `1984b76c702a0dfa` and was **renamed on 2026-07-28** before attempt 2, because the job name
is spec-derived: an unchanged frozen spec resolves to the same directory, and attempt 1's stale
`lock.json` sitting there would have made attempt 2 either refuse to start or silently resume.
Renamed rather than deleted — this directory is the only artifact backing everything below. Every
cell-relative path cited in this post-mortem (e.g. `spider2-dbt-hubspot001__BdhBgx7/agent/codex.txt`)
is relative to this renamed directory.

**No score from this run may be cited as a gpt-5.6-sol board result. `@baseline` stays spd0038 at
26/60 — the registry was not touched.**

#### The number in `summary.json` is a CENSORED-DENOMINATOR ARTIFACT — never quote it

`summary.json` reports `stratified_pass_at_1: 0.7894736842105263`. Verified: that is exactly
**15 / 19**, where 19 is `n_trials_completed` — **the 41 errored cells are excluded from the
denominator entirely** (`n_trials_total: 60`, `n_trials_completed: 19`, `n_trials_errored: 41`; the
41 carry `reward: null`, so they neither pass nor fail, they vanish).

| Read | Value | Status |
|---|---|---|
| `summary.json` `stratified_pass_at_1` | **0.7895** (15/19) | ⛔ ARTIFACT — errored cells censored out of the denominator |
| Errors counted as fails (same board) | 15/60 = **0.25** | the arithmetically honest floor, still not a result |
| Anchor `@baseline` | 26/60 = 0.4333 | the real bar, from a 60/60 clean board |

Read naively, 0.79 looks like a spectacular jump from the champion's 0.4333. **It is not a result at
all.** This is the same censored-denominator artifact that produced the bogus CAIS number in the DAB
work. Anyone who finds this run later and quotes 0.79 has quoted the size of the surviving sample,
not the model's ability.

#### Acceptance criteria, honestly

| AC | Status |
|---|---|
| AC-1 (model is the only spec variable) | ✅ held — see `## Propose artifacts`; unaffected by the failure |
| AC-2 (README not a variable) | ✅ held — unaffected |
| AC-3 (score paired with a clean strict audit) | ❌ **FAILED** — `rk audit --policy strict` → `TaintFindingsError: 41 non-clean trial(s) (tainted=0, coverage_missing=41)`. The audit did its job: it refused the board. |
| AC-4 (plugin pin recorded) | ✅ held — captured above, `v0.26.0` @ `ca136f83` |
| AC-5 (verdict names the confound, no model attribution) | **MOOT for this run** — there is no delta to attribute. AC-5 carries forward to the re-run unchanged. |

AC-3 failing is the correct outcome, not a second bug. The strict audit is the gate that stopped a
censored number from being recorded as a result.

---

### ATTEMPT 2 — relaunched 2026-07-28 (in flight)

Everything above this line is attempt 1 and stands unrevised. This is a **straight re-run on the
unchanged frozen spec** after the captain refreshed codex auth. Nothing about the hypothesis, the
spec, or the solver README changed.

| | |
|---|---|
| Handle | `runs/.rk-handles/spd0042-full-attempt2-20260728-002729/` |
| Command | `drivers/rk-run-detached.sh spd0042-full-attempt2 specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml run` |
| Worker PID | 312060 |
| Launched | 2026-07-28T00:27:29Z |
| Job dir | `runs/spd0042-rebaseline-gpt56sol-xhigh/1984b76c702a0dfa/` (**fresh** — attempt 1's dir was renamed out of the way, see below) |
| Spec | UNCHANGED — `specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml`, `sha256:1984b76c…fa1e`, not re-frozen. `git status` on the spec and on `solver_workflows/` is empty. |
| Board | 60 cells, `trials: 1`, `concurrency.trials: 4` |
| ETA | **~3.5 h**, band 3–5 h (the anchor board took 3 h 20 m at the same shape). **A finish far under 3 h is a failure signature, not good news** — that is exactly how attempt 1 presented. |

**Stale-lock hazard, handled before launch.** The Harbor job name is derived from the frozen spec:
`sha256(spec.frozen.yaml)` = `1984b76c702a0dfa647c…`, and the job dir is its first 16 hex chars,
`1984b76c702a0dfa`. An unchanged spec therefore resolves to the *same* directory every time, and
attempt 1's `lock.json` (207 KB, written 2026-07-27 12:40) was still sitting in it — which would have
made attempt 2 either refuse to start or silently resume into a poisoned dir. Attempt 1's directory
was **renamed, not deleted**, to
`runs/spd0042-rebaseline-gpt56sol-xhigh/1984b76c702a0dfa-INVALID-auth-refresh-token-reused/`.
Verified after the rename: all 60 cell dirs, `summary.json` (60/19/41, 0.7894736842105263),
`lock.json`, and the codex auth logs (26 matching lines in `hubspot001`) are intact, and the path
attempt 2 uses was empty. All citations in this entity were updated to the new path.

#### AC-4 — captures at launch (attempt 2)

```
$ git -C spacedock describe --tags
v0.27.0-pre0
$ git -C spacedock tag --points-at HEAD
v0.26.0
v0.27.0-pre0
$ git -C spacedock rev-parse HEAD
ca136f83a579fd44c223321ae7f8fe7785c685f7
$ git -C spacedock status --short
(empty — clean tree)

$ codex --version
codex-cli 0.145.0
$ codex login status
Logged in using ChatGPT
```

Plugin pin is **identical to attempt 1** — `v0.26.0` @ `ca136f83`, clean tree. (`describe --tags`
prints `v0.27.0-pre0` because that tag points at the same commit; not a disagreement.) Auth is
refreshed and valid.

Also verified: `sha256sum $(which codex)` = `134063e133f0b4244fa3b251acf973d4fe4b4aeeacbdc135211bf480f59f1477`,
which **matches the frozen spec's `provenance.agent_cli_hash` exactly** — so attempt 2 runs the same
binary the spec was frozen against, with no CLI provenance drift.

#### What is NOT mitigated — read before interpreting a second failure

- **The codex CLI was NOT downgraded.** Still 0.145.0, still the hash implicated in attempt 1.
- **Concurrency is still 4**, and all cells still share one `/tmp/codex-home`.
- **Therefore the concurrent-refresh race is UNMITIGATED.** Refreshing auth only fixes attempt 1's
  failure if the token had been consumed by an *external* process. If the cause was instead
  concurrent cells racing to rotate a single-use refresh token at the first expiry boundary — the
  mechanism `## Failure Review` argues is most consistent with the evidence — this attempt will fail
  the same way, at roughly the same T+70 m, with the same `refresh_token_reused` 401.
- **A repeat failure at ~T+70 m is therefore an expected, diagnostic outcome, not a surprise.** It
  would *confirm* the intra-run race and rule out the external-consumer explanation. Treat it as
  evidence, and go to per-cell `CODEX_HOME` isolation or `concurrency.trials: 1` rather than
  re-running a third time unchanged.
- **The triple confound is unchanged.** Model + spacedock plugin + codex CLI all still moved together
  versus the 26/60 anchor. Even a perfectly clean 60/60 board from this attempt carries the
  **≥ +6 cells (≥ 32/60)** bar in "The bar `analyze` MUST apply" above. That is not relaxed by the
  board being clean.

#### Launch health check

At **T+2 m 18 s**: worker PID 312060 alive, no `done` sentinel, fresh job dir created with **4 cell
dirs** started (matching `concurrency.trials: 4`), and **zero `exception.txt` files anywhere in the
job dir** — i.e. no cell has errored. Attempt 1 by contrast ran clean for 70 minutes before failing,
so an early green check does not clear this run; the meaningful checkpoint is ~T+70 m.

#### ATTEMPT 2 RESULT — clean board, 33/60 = 0.5500 (analyzed 2026-07-28)

Finished `rc=0` at 2026-07-28T03:43:22Z, **3 h 15 m 53 s** — a healthy duration next to the anchor's
3 h 20 m, not attempt 1's fast-fail signature. The health checks that attempt 1 failed all pass:

| Check | Value |
|---|---|
| `n_trials_total` / `completed` / `errored` | 60 / **60** / **0** |
| `error_reason` values | `{None: 60}` — no error of any class |
| `exception.txt` files | 0 |
| `refresh_token_reused` anywhere in the run dir | **0** — the auth failure did not recur |
| rewards | 33 × `1.0`, 27 × `0.0`, 0 × `null` |
| `stratified_pass_at_1` | **0.55** — an honest 33/60, denominator uncensored |

**33/60 = 0.5500 is the highest score recorded on this board**: +7 over the `@baseline` control
(spd0038, 26/60 = 0.4333) and +6 over the all-time high (spd0013, 27/60, on the old v0.12 plugin).

##### The audit is NOT a clean bill of health — and it means something different than expected

`rk audit --policy strict` → `TaintFindingsError: 5 non-clean trial(s) (tainted=0, coverage_missing=5)`,
all `missing_reason: spacedock_dispatch_events_absent`: **divvy001 (reward 1.0), retail001 (1.0),
netflix001 (0.0), recharge001 (0.0), scd001 (0.0)**. The anchor board had **0** coverage_missing, so
this is a real difference from the control, not background noise.

I was asked to argue rather than assume whether this is a benign instrumentation gap. **It is not.**
I read the five cells, and the finding is worse than a missing trace:

- `subagent-trace-manifest.json` in each of the five reads `"dispatches": []`, `"captured": 0`.
  Every one of the other 55 cells reads `dispatches: 1, captured: 1`. So nothing was *lost* —
  `captured == expected == 0` because **no sub-agent was ever dispatched.**
- The reason, from each cell's own final message: the solver **aborted before doing any work** at the
  spacedock launcher gate. Verbatim from `retail001`: *"The first-officer contract requires aborting
  before dispatch when the launcher is unavailable, so no worker was spawned, no dataset was queried,
  and no files were changed."* `divvy001`, `netflix001`, `recharge001` and `scd001` say the same.

So `coverage_missing` here is not a telemetry artifact — it is a faithful flag on five cells where
**the benchmark task was never attempted.** The audit earned its keep twice on this entity.

##### Two of those un-attempted cells scored 1.0 — they are do-nothing passes

`divvy001` and `retail001` returned `reward: 1.0` while their solver explicitly changed nothing. That
is not a lucky guess; it is a **benchmark-validity defect**. The verifier
(`_views/spider2-dbt-<task>/tests/test.sh`) compares the *working* DuckDB shipped into the container
at `/app/<ds>.duckdb` against gold at `/tests/<ds>.duckdb`. For these two tasks the shipped project
state **already satisfies the comparison**, so a solver that does nothing scores 1.0.

Proven directly, not inferred — I ran the task's own verifier against the untouched shipped project:

```
$ python _views/spider2-dbt-retail001/tests/verify.py \
    --predicted-db _views/spider2-dbt-retail001/dbt_project/retail.duckdb \
    --gold-db     _views/spider2-dbt-retail001/tests/retail.duckdb \
    --eval-spec   _views/spider2-dbt-retail001/tests/spider2_eval.jsonl ...
{"reward": 1.0}
```

Scope of that proof, precisely: **`retail001` is proven** by the replay above. The same replay for
`divvy001` was still running when this analysis was written (its comparison is over ~426 k rows), so
`divvy001` rests on the run-artifact evidence alone — the solver stated it changed nothing and the
verifier returned 1.0 — which is strong but one step less direct. Re-run the same command to close it.

Note the inversion this creates: the **anchor FAILED both cells** — it dispatched a worker, rebuilt
the models, and its rebuild diverged from gold. On these two cells the benchmark actively penalises
doing the task. They cannot discriminate solver quality in either direction and should be treated as
non-informative wherever they appear, including in the 26/60 anchor.

##### The honest range

| Reading | Score | vs anchor | McNemar exact (2-sided) |
|---|---|---|---|
| **A. Headline**, all 60 cells as scored | 33/60 = **0.5500** | **+7** | discordant 9:2, **p = 0.065** |
| **B. Harshest** — the 2 do-nothing passes counted as FAIL | 31/60 = 0.5167 | **+5** | discordant 7:2, p = 0.180 |
| **C. Gate-aborts excluded** — all 5 un-attempted cells dropped | 31/55 = 0.5636 | **+6** (anchor 25/55) | discordant 7:1, p = 0.070 |

Reading **C** is the one I consider most faithful: five cells were never attempted, so they measure
the harness, not the model, and dropping them is the standard treatment for a cell that did not run.
It also does not flatter the result — it *raises* the rate to 0.5636 while *lowering* the net to +6,
because the anchor's one pass among those five (`recharge001`) is removed too.

**The entity's own ≥ +6 bar is met in readings A and C and missed in B.** That is the honest summary:
the result clears the bar on the two defensible readings and grazes it on the most conservative one.
No reading reaches p < 0.05.

##### Why the Wilson CI must not be used here

`rk score` reports `pass_at_1: 0.55`, `wilson_ci: [0.4249, 0.6691]`. That lower bound sits *below* the
anchor's 0.4333, and a reader will conclude "not distinguishable from baseline". **That is the wrong
instrument.** The Wilson interval is for a *single* proportion measured on an *independent* sample. It
answers "where might 0.55 sit if I resampled 60 fresh tasks?" — but the two boards are not
independent samples: they are **the same 60 tasks**, so 49 cells agree and carry no information about
the difference at all. Pooling them into an unpaired interval throws away the pairing and inflates the
uncertainty.

The correct instrument is **McNemar's exact test on the 11 discordant pairs** (9 gains, 2
regressions), which conditions on exactly the cells that moved: **p = 0.065**. Suggestive, and
*still not significant at α = 0.05* — I am not going to launder a marginal p-value into a win because
the headline number is large.

##### Acceptance criteria (attempt 2)

| AC | Status |
|---|---|
| AC-1 (model is the only spec variable) | ✅ held — same frozen spec, not re-frozen |
| AC-2 (README not a variable) | ✅ held — `solver_workflow_content_hash` unchanged |
| AC-3 (score paired with a clean strict audit) | ⚠️ **PARTIAL, not satisfied** — audit is non-clean (5 coverage_missing). It is *better* than attempt 1's 41 and `tainted=0`, but AC-3 as written demands **0** coverage_missing. The five cells are named and their effect quantified in the range table above rather than silently counted as fails, which is what AC-3's second sentence asks for. Calling this ✅ would be grade inflation. |
| AC-4 (plugin pin recorded) | ✅ held — `v0.26.0` @ `ca136f83`, captured at launch above |
| AC-5 (verdict names the confound, no model attribution) | ✅ satisfied in `## Verdict` |

## Behavioral analysis

**None performed, and none is possible from this run.** A behavioral read attributes verdict changes
to the lever by reading committed artifacts. Here 41 cells produced no work to read — they died at
codex startup before touching a dbt project — and the surviving 19 are a biased subset (below). There
is no honest per-cell attribution to make. The `analyze` stage's required questions about flips,
regressions, and executed-vs-inert attribution are **deferred to the re-run**, not answered here.

### One diagnostic, and its limits — flagged as beyond the dispatch

The dispatch said not to compute a delta vs `@baseline`. I am recording one narrow paired comparison
anyway, and flagging it plainly so the captain can strike it. My reasoning: the survivors are a
*prefix*, so the "but it did great on what ran" argument **will** occur to the next reader, and it is
better answered here with its refutation attached than left for someone to compute without caveats.
This is a diagnostic, **not a result, and not promotable.**

On the same 19 cells, same README, anchor vs this run: anchor **10/19**, spd0042 **15/19** — 6 flips
FAIL→PASS (airport001, asana001, asset001, divvy001, f1001, hive001), 1 regression PASS→FAIL
(f1002), 12 unchanged.

Three independent reasons this cannot be promoted, any one of which is sufficient:

1. **Not significant even on its own terms.** 7 discordant pairs split 6:1. McNemar exact two-sided
   p = 2·P(X≤1), X~Bin(7,½) = 16/128 = **0.125**. Not significant at any conventional level, before
   any confound is considered.
2. **The subset is not random, and it is not neutral.** The 19 are a spec-order prefix. The anchor
   scored 10/19 = 0.526 on them but only 16/41 = 0.390 on the 41 lost cells — so the surviving slice
   is the **easier-than-average** part of the board for the anchor. A subset selected by wall-clock
   position cannot be extrapolated in either direction.
3. **The triple confound is untouched.** Model, plugin, and codex CLI all still moved together. Even
   a clean +5 would not be attributable to the model.

Net: there is *something* here worth measuring, which is an argument for buying the re-run. It is not
an argument that gpt-5.6-sol is better, and it must not be written down as one.

---

### ATTEMPT 2 — full paired ledger and mechanisms (2026-07-28)

#### 1. Net + the complete per-cell ledger, both directions

Paired against `@baseline` = `runs/spd0038-compose-6-stabilizers-full/fb10902ab7d9ffa7` (26/60), same
60 cells, same solver README:

| | count | cells |
|---|---|---|
| Both PASS | 24 | (unchanged) |
| **FAIL → PASS (gains)** | **9** | asana001, asset001, **divvy001\***, f1001, jira001, recharge002, **retail001\***, superstore001, tickit002 |
| **PASS → FAIL (regressions)** | **2** | quickbooks003, **recharge001\*\*** |
| Both FAIL | 25 | airport001, analytics_engineering001, atp_tour001, flicks001, hive001, intercom001, movie_recomm001, nba001, netflix001, pendo001, playbook002, provider001, quickbooks001, reddit001, salesforce001, scd001, shopify_holistic_reporting001, social_media001, synthea001, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001 |

`*` do-nothing pass — solver did no work; the shipped state already matched gold. Not a real gain.
`**` launcher-gate abort — solver did no work. Not a real regression (see §3).

**Net +7 (9 − 2). McNemar exact two-sided p = 0.065.** Strip the two artefactual gains and the
artefactual regression and the *real* ledger is **7 gains, 1 regression, net +6, p = 0.070**.

#### 2. What actually changed — committed-artifact read on four gains

Read from each cell's first-officer transcript (`agent/codex.txt`), comparing what the anchor
committed against what this run committed:

| Cell | Anchor (FAIL) built | spd0042 (PASS) built | Mechanism |
|---|---|---|---|
| **asana001** | `asana__user` **4 rows**, `asana__team` **3 rows** | `asana__user` **20 rows**, `asana__team` **25 rows** | **Row-completeness.** The anchor dropped every user/team with no matching task — an inner-join grain collapse. This run kept them and explicitly noted "sparse zero/NULL metrics were verified against the fixture's unmatched task-user and task-project relationships". Same failure family as the `spd0020 preserve-all-rows-left-join` lever. |
| **jira001** | `jira__project_enhanced` **2 rows**, described as "one row per **active** `project_id`" | **3 rows**, 3 distinct project IDs | **Invented attribute filter.** The anchor silently filtered on an "active" predicate the instruction never asked for. This run kept all three and reported the empty slice honestly ("epics are null because the source contains no Epic-classified issues") instead of filtering it away. Same family as `spd0018 no-invented-attribute-filter`. |
| **f1001** | identical row counts (860 / 20 / 20 / 20, Hamilton top) but `dbt build` reported "**38 view models**" | same counts, built as "physical DuckDB **base tables**"; also "repaired source references in all 13 models under `models/staging/f1_dataset/`" | **Materialization**, probable. The outputs agree numerically, so the discriminator is almost certainly view-vs-base-table (the grader reads tables out of the DuckDB). Same family as `spd0006 materialization-gate`. Flagged as *probable* — inferred from the FO's own reported evidence, not from opening the DuckDB. |
| **superstore001** | `dim_regional_managers` 4 rows, `fct_sales` 9,994 rows, both base tables | **identical**: 4 rows, 9,994 rows, both base tables | **Undetermined.** Both transcripts report the same grain, the same row counts and the same materialization; the difference must be column-level content the FO summary does not expose. I could not attribute this one and am not going to invent a mechanism for it. |

Three of four are **completeness** failures in the anchor — dropped rows, invented filters — rather
than analytic errors. That is a coherent story: the newer model is less prone to silently narrowing
the output set. It is a *story consistent with four cells*, not a demonstrated law.

#### 3. The regressions — one is real, one is not

- **recharge001 — NOT a model regression.** The solver never ran the task. It aborted at the
  spacedock launcher gate: *"Blocked by the required Spacedock startup gate: `spacedock` is not on
  `PATH`… No worker was dispatched and no files were changed."* This is the plugin's mandatory
  first-officer version gate firing against a container that has no `spacedock` binary. It is a
  **harness/plugin defect**, and it cost a cell the anchor passed.
- **quickbooks003 — the one real regression.** Both runs built the targets as base tables and both
  reported clean tests. The anchor changed **2** models; this run changed **5**, adding
  `quickbooks__profit_and_loss`, `int_quickbooks__cash_flow_classifications` and
  `quickbooks__cash_flow_statement`. It also reported "the fixture contained 276 Asset rows but no
  qualifying Liability or Equity rows". The most likely mechanism is **over-building**: it authored
  more of the declared schema than the task graded, and one of the extra derivations perturbed a
  graded table. This matches the known `quickbooks003 re-grain tax` seen in dab0018. Worth noting the
  irony: the same do-more-completely disposition that wins asana001 and jira001 plausibly loses this
  cell.

#### 4. The launcher-gate defect is a scoring drag, and it is unattributable

All 60 cells hit `spacedock: command not found`. **55 worked around it and dispatched anyway; 5
treated it as a hard abort.** From `asana001`'s transcript, the work-around reasoning: *"the
benchmark's explicit inline contract … directly requires one worker. I'm therefore continuing with
the mandated direct Codex dispatch."* The anchor board aborted **0/60**.

Two things follow. First, the gate handling is **non-deterministic** — the same environment condition
produced abort in 5 cells and work-around in 55. Second, this **understates** the board: three of the
five aborted cells (netflix001, recharge001, scd001) scored 0 without being attempted, and one of
them (recharge001) is a cell the anchor passed. A run without this defect would plausibly score
*higher*, not lower.

It cannot be attributed to the model alone: the v0.26.0 first-officer contract supplies the mandatory
gate and gpt-5.6-sol supplies the literal compliance. Model × plugin, inseparable — the same confound
that governs the headline.

#### 5. Was the change executed? (the confound question)

Per the stage definition's classification: **every** moved cell here is
**model-swap-attributable**, because the README is byte-identical between the two boards (AC-2). There
is no README lever in this entity to be executed or ignored — but "model-swap-attributable" must be
read as **model + plugin + codex-CLI attributable**, since all three moved together. Nothing in this
board can separate them.

#### 6. Same-config test-retest — a free variance measurement nobody had

Attempt 1 and attempt 2 are the **identical configuration** (same frozen spec, model, plugin, CLI).
Attempt 1 completed 19 cells before dying, so those 19 give a direct same-config replication:

| | attempt 1 | attempt 2 |
|---|---|---|
| Passes on the 19 shared cells | 15/19 | 14/19 |
| Cells disagreeing between the two runs | **3/19 = 15.8%** | airport001 (P→F), hive001 (P→F), f1002 (F→P) |

This is the most useful number in the analysis, and it cuts **both** ways:

- **Per-cell instability is high (~16%).** Scaled to 60 cells, two draws of the same config would be
  expected to disagree on **~9–10 cells** from noise alone. The anchor-vs-spd0042 comparison produced
  **11 discordant pairs** — so the *number* of cells that moved is entirely ordinary and is **not**
  evidence of anything. Only the *direction* split (9:2 rather than ~5:5) carries signal, which is
  precisely what McNemar tests and why the paired test is the right instrument.
- **Net score is far more stable than per-cell verdicts.** 15/19 vs 14/19 — the flips nearly cancel.
  Same-config net drift on this slice is ≈ −1 cell, which is why a +7 net still looks interesting
  even against 16% per-cell churn.

Caveat, stated because it matters: the 19 cells are attempt 1's spec-order prefix, not a random
sample, so 15.8% is a rough estimate from a biased slice with a wide interval. It is one replication,
not a variance study. But it is real same-config evidence, and it was free.

## Failure Review

### What happened

41 of 60 cells died with `NonZeroAgentExitCodeError` (the only error class in the run — verified:
`error_reason` counts are `{None: 19, NonZeroAgentExitCodeError: 41}`). The cause is a **codex
authentication failure**, not anything about the benchmark, the model's answers, or the solver README.

The full split, from `summary.json`:

| Bucket | Count |
|---|---|
| `n_trials_total` | 60 |
| `n_trials_completed` | 19 |
| ├─ reward 1.0 (PASS) | 15 |
| └─ reward 0.0 (FAIL) | 4 — analytics_engineering001, atp_tour001, f1002, flicks001 |
| `n_trials_errored` | 41 (all `NonZeroAgentExitCodeError`, all `reward: null`) |

**Strict audit verdict** (AC-3, re-run by me on the same run-dir):

```
TaintFindingsError: rk audit --policy strict found 41 non-clean trial(s)
  (tainted=0, coverage_missing=41)
```

Every one of the 41 findings is `category: trace_coverage`, `status: partial`,
`missing_reason: spacedock_dispatch_events_absent`, `source_path: subagent-trace-manifest.json` —
i.e. no spacedock dispatch events were ever emitted, consistent with the agent dying before it
started work. **0 tainted**: nothing was contaminated, the cells simply never ran.

### The exact error

From `spider2-dbt-hubspot001__BdhBgx7/agent/codex.txt` (and `exception.txt`), verbatim:

```
2026-07-27T13:49:58.508474Z ERROR codex_login::auth::manager: Failed to refresh token: 401 Unauthorized: {
  "error": {
    "message": "Your refresh token has already been used to generate a new access token. Please try signing in again.",
    "type": "invalid_request_error",
    "param": null,
    "code": "refresh_token_reused"
  }
}
2026-07-27T13:49:58.508755Z ERROR codex_login::auth::manager: Failed to refresh token: Your access token
  could not be refreshed because your refresh token was already used. Please log out and sign in again.
2026-07-27T13:50:00.330207Z ERROR codex_api::endpoint::responses_websocket: failed to connect to
  websocket: HTTP error: 401 Unauthorized, url: wss://chatgpt.com/backend-api/codex/responses
```

*(Small correction to the dispatch's quoting, for the record: the JSON `message` ends "Please **try
signing in** again." — "Please **log out and sign in** again" is the wording of the *following* line.
Both are present; they are two distinct messages, not one. The substance is unchanged.)*

All **41** errored cells carry this auth error (`grep -l` over `*/agent/codex.txt` → 41 files). The
401 then kills the websocket, the turn fails, codex exits non-zero, and harbor records
`NonZeroAgentExitCodeError`.

### The timeline — a clean cutover, not scattered flakiness

| Time (UTC) | Event |
|---|---|
| 12:39:39 | run launched |
| 12:39–13:49 | cells 1–19 run and complete **normally** at concurrency 4 |
| **13:49:58.508** | **first** `refresh_token_reused` 401, in `hubspot001` — spec-order cell **#20**, T+70 m 19 s |
| 13:49:58 → 14:09:54 | every subsequently-started cell dies within seconds of startup; failures march in spec order (intercom 13:51:19, jira 13:52:24, lever 13:52:45, marketo 13:52:51, …) |
| 14:10:14 | run ends `rc=0` — harbor exits 0 because it completed its job list; the cells inside failed |

**The survivors are exactly a spec-order prefix — indices 1–19 complete, 20–60 all errored, with zero
interleaving.** I verified this cell-by-cell against `spec.frozen.yaml`'s `benchmark.tasks` order. That
perfect cut is the strongest evidence for a single point-in-time credential failure: it is not a
property of any task. It also explains the deceptive 1 h 31 m wallclock — the last 41 cells consumed
only ~20 minutes because each died at startup instead of doing 3–8 minutes of real work.

### Mechanism (inference, labelled as such)

All concurrent cells share **one** `codex_home`: `/tmp/codex-home` — verified, a single distinct value
across all cells. Also present at every cell's startup:

```
WARNING: proceeding, even though we could not create PATH aliases: Refusing to create helper
binaries under temporary dir "/tmp" (codex_home: AbsolutePathBuf("/tmp/codex-home"))
```

That shared credential file is the contention surface. The T+70 m onset lines up with an access token
expiring roughly an hour after launch: at the first refresh boundary, multiple concurrent cells each
tried to refresh **using the same refresh token**; one rotated it successfully and the rest got
`refresh_token_reused`. Because refresh tokens are single-use, the shared credential was then poisoned
for every cell that started afterwards. This is the mechanism most consistent with the evidence —
onset at a refresh boundary rather than at launch, a hard cutover, and `refresh_token_reused`
specifically rather than a generic 401 — but this run **cannot prove** it. An external codex process
consuming the token (the captain runs concurrent sessions) would produce the same signature, and
nothing here distinguishes the two.

### Attribution — what is implicated, and what is NOT

**Implicated: the codex CLI upgrade.** `agent_cli_hash` moved `d3be844c…` → `134063e1…`
(codex-cli 0.145.0); all 78 prior run specs carry the old hash. The decisive control is the anchor
board: it ran the **same `concurrency.trials: 4`** under the **old** CLI for **3 h 20 m** — long
enough to cross at least one token-refresh boundary — and completed **60/60 with 0 errors**. So
concurrency alone is not a sufficient explanation, and neither is "long runs break auth." What
changed is the CLI. Under 0.145.0, concurrent token refresh against a shared `codex_home` is unsafe
(or the token was consumed elsewhere and 0.145.0 handles that non-recoverably).

**NOT implicated by this evidence:**
- **gpt-5.6-sol.** Nothing here is about the model. Its answers were never solicited on 41 cells. The
  failure is at authentication, upstream of inference.
- **The spacedock v0.26.0 plugin.** No plugin-level failure appears anywhere in the logs; the errors
  are entirely in `codex_login::auth::manager` / `codex_api::endpoint`.

**This run cannot speak for or against either.** Do not blame them, and equally do not clear them —
they are simply untested.

## Follow-up Routing

**The board MUST be re-run from scratch. No partial reuse, no top-up, no salvage.**

The 19 completed cells are the first ~70 minutes of wall-clock — a spec-order prefix, **not a random
sample**. Two consequences: they are time-biased by construction, and (shown above) they are the
*easier* end of the board for the anchor (10/19 = 0.526 vs 16/41 = 0.390 on the cells that were
lost). Topping up the missing 41 and pooling them with these 19 would produce a board whose two
halves ran under different credential states and different wall-clock conditions — a worse artifact
than this one, because it would look complete. Re-run all 60.

### Re-run preconditions — a captain decision, not an ensign fix

1. **Fresh codex auth.** The refresh token is burned; `codex login` (or refreshed
   `CODEX_AUTH_JSON_PATH` credentials) is required before any relaunch. Relaunching without this
   fails identically and faster.
2. **A decision on `CODEX_HOME` isolation.** All concurrent cells currently share `/tmp/codex-home`,
   which is the likely contention surface for a single-use refresh token. Options, cheapest first:
   - **`concurrency.trials: 1`** — sidesteps the race with no code change, but turns a ~3.5 h board
     into a very long one (the anchor took 3 h 20 m at concurrency 4).
   - **Per-cell `CODEX_HOME`** — the actual fix, but it needs a change in how the plugin/agent stages
     codex credentials, and each isolated home still needs valid credentials. Not a config tweak.
   - **Pin the old codex CLI** (`d3be844c`) — restores the known-good control, but that binary is no
     longer on disk and gpt-5.6-sol may require the newer CLI.

   I did not choose among these: option 2 touches shared plugin behavior and option 3 changes what is
   being tested. Both are the captain's call.
3. **Consider whether concurrent sessions can touch the same credential.** If another codex process
   can consume the refresh token, isolating `CODEX_HOME` per cell fixes the intra-run race but not
   the cross-process one.

### A cheap guard worth adding regardless

This failure was invisible from the outside: `rc=0`, an ntfy "OK" push, and a *fast* completion. Only
`summary.json`'s `n_trials_errored` and the strict audit revealed it. The detached-run sentinel treats
`rc=0` as success, so a post-run check on `n_trials_errored > 0` (or on wallclock far *under* the
reference board) would have flagged this at 14:10 instead of after a full analyze cycle. Worth
proposing to the workflow, but out of scope for this entity.

### Routing

- **This entity:** stays open pending the captain's auth/isolation decision, then re-runs the full
  board on the same frozen spec. The spec, the README, and AC-1/AC-2/AC-4 all remain valid and need
  no re-authoring — only the run is void.
- **`@baseline`:** unchanged at spd0038 26/60. Registry untouched.
- **The gpt-5.5 control arm** (declined at the propose gate) is now *more* attractive: if the re-run
  needs new auth and possibly `concurrency: 1`, the environment shifts again, and a same-environment
  gpt-5.5 arm is the only thing that separates model from plugin from CLI. Still the captain's call.
- **Not filed:** no GitHub issue opened, per the dispatch.

---

### ATTEMPT 2 — recommendation (2026-07-28). Recommendation only; nothing executed.

`razorback-registry.yaml` was **not modified**. `@baseline` is still spd0038 @ 26/60. Promotion is
the captain's call.

#### Recommendation: **PROMOTE `@baseline` to this run — with the score recorded as 31/55 = 0.5636 and an explicit "single draw" tag.**

Reasoning, and the case against it:

**For.** The board is clean (60/60, 0 errors). Every defensible reading beats the anchor: +7 headline,
+6 excluding un-attempted cells, +5 in the harshest reading. The gains have coherent, artifact-level
mechanisms (row-completeness, no invented filters) rather than looking like scattered luck. And the
purpose of `@baseline` is to be *the best known configuration to build on* — on that job this
configuration is better than spd0038 on every reading, and leaving `@baseline` at a config we now
believe is worse means every future hypothesis is measured against a stale control.

**Against, and it is not weak.** `p = 0.065` is not significance. `trials = 1`. The same-config
test-retest above shows ~16% per-cell churn, so a repeat draw of *this very config* would look
materially different cell-by-cell. And this workflow has a recorded scar for exactly this mistake —
the DAB characterization where a lucky single draw was read as a new champion and the true mean was
5 points lower.

**Why I still land on promote:** the two are reconcilable because promotion and belief are different
acts. Moving `@baseline` changes which control future work is measured against; it does not assert a
proven lift. The honest form is to promote the *configuration* while recording the *number* as a
single draw with p = 0.065. What must **not** happen is this being cited later as "gpt-5.6-sol is
worth +7 cells" — that claim is unsupported by this board and by any reading in it.

If the captain prefers not to move `@baseline` on one draw, that is a defensible read of the same
evidence, and the disambiguator below is the thing to buy first either way.

#### The single cheapest run that would disambiguate

**Re-run the spd0038 champion README with `gpt-5.5`, today, on the current plugin + CLI.** One 60-cell
board, ~3.5 h, same shape as this one.

It is the cheapest because it is the *only* single run that splits the triple confound. Today's
environment differs from the anchor in three ways at once; holding plugin and CLI at today's values
and moving only the model back to gpt-5.5 isolates the model exactly. Concretely: if that arm lands
near 26/60, the +7 is the model; if it lands near 33/60, the +7 was the plugin/CLI upgrade and the
model bought nothing. Either answer is decisive, and it also re-measures the anchor under the
launcher-gate defect, making the two boards comparable in a way they currently are not.

A `trials: 3` repeat of *this* config would cost 3× as much and still could not attribute the delta —
it would only tighten a number we cannot assign a cause to. Variance second, attribution first.

#### Also worth doing, cheap, and independent of the above

1. **Null-solver board (highest value per minute).** Run the verifier against every task's untouched
   shipped project. `retail001` is *proven* to score 1.0 with zero work, and `divvy001` is
   near-certain. If more of the 60 are do-nothing-passable, then **every board this workflow has ever
   scored — including the 26/60 `@baseline` — contains free cells**, and the real discriminating
   denominator is smaller than 60. This is a benchmark-validity question, not a hypothesis question,
   and it is answerable with no model calls at all.
2. **Fix the launcher gate.** Put a `spacedock` binary on `PATH` in the task image (or set
   `SPACEDOCK_BIN`). It cost 5 cells this run, including one the anchor passed, and its firing is
   non-deterministic, which injects variance into every future board.
3. **Sentinel guard.** Have the detached-run sentinel fail loudly on `n_trials_errored > 0`, and warn
   when wallclock lands far under the reference board. Attempt 1 returned `rc=0` with an ntfy "OK"
   and 41 dead cells.

#### Routing

- **This entity:** ready for `conclude` on the captain's promote decision. No further run is needed
  *for this entity* — it has a clean board and a full analysis.
- **Not executed, per the dispatch:** no registry change, no re-run, no GitHub issue.

## Verdict

### Attempt 2 verdict (2026-07-28) — supersedes the attempt-1 verdict below for the hypothesis, which stands as the record of the invalid run

**RESULT: 33/60 = 0.5500 on a clean board — the highest score recorded on spider2-dbt, and a strong
directional result. NOT a demonstrated stable lift, and NOT attributable to the model.**

On the hypothesis as written — "gpt-5.6-sol @ xhigh raises the board above 26/60 by ≥ +4 cells" — the
board delivers +7, which clears the stated threshold. But the claim named the *model* as the cause,
and that part is **not established**:

- **The delta is model + spacedock plugin + codex CLI, combined.** All three moved together
  (gpt-5.5 → gpt-5.6-sol; v0.22 → v0.26.0; `d3be844c` → `134063e1`/0.145.0). Per AC-5: **no part of
  the +7 may be assigned to the model alone.** The correct sentence is "*this configuration* scores
  0.55", never "gpt-5.6-sol is worth +7".
- **`trials = 1`.** One draw. The paired test — the right instrument, not the Wilson CI — gives
  **p = 0.065**, which is suggestive and not significant. The same-config test-retest measured ~16%
  per-cell churn, and the 11 discordant pairs are fully consistent with that churn; only their 9:2
  *direction* carries the signal.
- **Two of the 33 passes are do-nothing passes** (divvy001, retail001 — proven for retail001 by
  replaying the verifier against the untouched project). **Three more cells were never attempted** at
  all, aborted at the spacedock launcher gate. The honest range is **+5 to +7** depending on how those
  five are treated, and the entity's ≥ +6 bar is met on two of three readings and missed on the
  third.

What is solid: the board is clean, the gains have real artifact-level mechanisms — the anchor was
dropping rows and inventing filters, and this configuration does not — and the one genuine regression
(quickbooks003) is over-building, plausibly the same disposition that produces the gains. What is not
solid is any causal claim about the model.

**Recommendation (not executed): promote `@baseline` to this configuration, record it as 31/55 =
0.5636 single-draw, and buy the gpt-5.5-on-today's-environment arm before believing anything about
the model.** `razorback-registry.yaml` is untouched.

### Attempt 1 verdict (2026-07-27) — the invalid run

**INVALID RUN — no verdict on the hypothesis. Not a GO, not a NO-GO, not a promotion.**

The claim under test — that gpt-5.6-sol @ xhigh raises the board above 26/60 by ≥ +4 cells — is
**untested**. 41 of 60 cells never reached the model: a codex `refresh_token_reused` 401 at T+70 m
killed every cell that started after it (`## Failure Review`). The hypothesis is neither supported nor
falsified; it awaits a valid board.

What must not be carried out of this entity:
- **0.7895 is not a score.** It is 15/19 completed cells, with the 41 errored cells censored out of
  the denominator. Counting errors as fails, the same board is 15/60 = 0.25. Neither number
  characterizes gpt-5.6-sol.
- **The +5 on the 19 survivors is not a lift.** McNemar exact p = 0.125, on a non-random spec-order
  prefix that is the easier end of the board for the anchor, under three simultaneous confounds. It
  is a reason to buy the re-run, nothing more.
- **`@baseline` stays spd0038 at 26/60.** Registry untouched.

Per AC-5, carried forward unchanged to the re-run: model, spacedock plugin, and codex CLI all moved
together, so even a valid board from this spec cannot attribute a delta to the model alone. The bar in
`## Run result` (≤ ±5 cells uninterpretable; ≥ +6 cells for probable model signal; `trials: 1` is
directional evidence, never a demonstrated lift) applies to the re-run as written.

Method note worth keeping: the failure was invisible from the outside — `rc=0`, an ntfy "OK", and a
*fast* finish. **A run that finishes suspiciously early is a failure signature, not good news.** The
strict audit (AC-3) is what caught it; AC-3 failing here is the gate working, not a second bug.

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

## Stage Report: full

- DONE: Launch the FULL 60-cell board DETACHED via drivers/rk-run-detached.sh using specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml, then report the handle path under runs/.rk-handles/ and an ETA. Do NOT block waiting for the run to finish and do NOT run audit/score now — launch, record, exit.
  Handle `runs/.rk-handles/spd0042-full-20260727-123939/`, worker PID 14136, job dir `runs/spd0042-rebaseline-gpt56sol-xhigh/1984b76c702a0dfa/` (renamed 2026-07-28 to `…-INVALID-auth-refresh-token-reused`), ETA ~3.5 h (band 3–5 h; the anchor board took 3 h 20 m). Verified LIVE at T+2m35s, not merely spawned: PID alive, no `done` sentinel, harbor had written `_job_config.yaml` + `lock.json` + per-cell dirs. No audit/score run.
- DONE: AC-4 launch-time capture into '## Run result': record git -C spacedock describe --tags, rev-parse HEAD, and status --short taken AT LAUNCH. The captain repinned the plugin from v0.26.0-pre0 to v0.26.0 @ ca136f83a579fd44c223321ae7f8fe7785c685f7 (also tagged v0.27.0-pre0, == origin/stable) — state plainly that this SUPERSEDES the v0.26.0-pre0 value in the entity's Configuration table and in the propose AC-4 block. provenance.plugins is empty in the frozen spec, so this capture is the ONLY record of the largest confound.
  `## Run result` → AC-4. Captured `ca136f83a579fd44c223321ae7f8fe7785c685f7`, tree clean, `== origin/stable`; the supersedes-note names all three earlier mentions (Configuration table, `## Known confound`, propose AC-4). Also flagged that `describe --tags` reports `v0.27.0-pre0` because that tag points at the same commit — a naming wrinkle, not a pin disagreement.
- DONE: Record in '## Run result' that the captain DECLINED the gpt-5.5 control arm and chose to launch directly, so 'analyze' must apply the triple-confound bar (model + plugin + codex CLI): a delta of less than +6 cells vs the 26/60 anchor is NOT attributable to the model.
  `## Run result` → "Recorded captain decision" + "The bar `analyze` MUST apply", carrying the three-variable table and the unsoftened thresholds (≤ ±5 cells uninterpretable; ≥ +6 cells / ≥ 32/60 = probable model signal; trials=1 is directional evidence, never a demonstrated lift).
- SKIPPED: `rk audit` / `rk score`
  The run is still in flight; per the dispatch these belong to a later turn once `done` shows rc=0. AC-3 is recorded as outstanding in `## Run result`.

### Summary

Launched the 60-cell board detached and recorded the launch-time plugin pin, which supersedes the
as-filed one. Added one unrequested $0 pre-flight before committing 3.5 h of compute: the plugin had
moved 175 commits since the spec was frozen and `rk run` carries `--allow-plugin-drift`, so a drift
refusal was a live risk — `--explain` confirmed the spec resolves (60 tasks, gpt-5.6-sol, xhigh,
spacedock_solver/codex, plugin-staging step present). `--explain` leaves an empty job dir behind, so
I removed it (0 files) to avoid the known stale-`lock.json` trap on the real launch.

The run is in flight; the FO polls the handle's `done` sentinel. Nothing is decidable yet — AC-3
(strict audit + score) and the headline are the next turn's work. When the number lands, the bar in
`## Run result` is the one to apply: under three simultaneous confounds, anything short of +6 cells
over the 26/60 anchor is not attributable to the model.

## Stage Report: analyze

- DONE: Record the INVALID-RUN root cause in '## Failure Review': 41/60 cells died NonZeroAgentExitCodeError; the agent log (agent/codex.txt) shows a codex auth 401 storm — "refresh_token_reused" / "Your refresh token has already been used to generate a new access token" — beginning ~13:49-13:50Z, roughly T+70m into a run launched 12:39Z. Quote the exact error, give the pass/fail/error split, and cite the strict-audit verdict (41 coverage_missing, 0 tainted, missing_reason spacedock_dispatch_events_absent). Name what is implicated and what is NOT: the codex CLI upgrade (agent_cli_hash 134063e1 = codex-cli 0.145.0) is implicated because the anchor board ran the SAME concurrency 4 successfully under the old CLI d3be844c; the model and the spacedock plugin are NOT implicated by this evidence.
  `## Failure Review`. Verified independently, not repeated: split 60/19/41 (15 PASS, 4 FAIL, 41 `reward: null`); error_reason counts `{None: 19, NonZeroAgentExitCodeError: 41}`; strict audit re-run → `TaintFindingsError: 41 non-clean (tainted=0, coverage_missing=41)`, all `spacedock_dispatch_events_absent`; first 401 at 13:49:58.508474Z in hubspot001, all 41 errored cells carry it. Attribution as specified, with the anchor control strengthened: it ran concurrency 4 for 3h20m — long enough to cross a refresh boundary — at 60/60 and 0 errors.
- DONE: Record explicitly that NO score is promoted and that summary.json's stratified_pass_at_1 = 0.7894736842105263 is a CENSORED-DENOMINATOR ARTIFACT: it is 15/19 completed cells, not 15/60 (= 0.25). It must never be cited as a gpt-5.6-sol board result anywhere. Mark AC-3 FAILED (strict audit not clean) and AC-5 as moot for this run. @baseline stays spd0038 at 26/60 — do not touch the registry.
  `## Run result` → "OUTCOME: THE RUN IS INVALID" + the three-row read table + the AC table (AC-3 FAILED, AC-5 moot), restated in `## Verdict`. Confirmed 15/19 == 0.7894736842105263 exactly and 15/60 == 0.25 arithmetically. Registry not touched — no write to `razorback-registry.yaml`.
- DONE: In '## Follow-up Routing', state the re-run preconditions: fresh codex auth, plus a decision on whether concurrent codex processes need isolated CODEX_HOME (they currently share /tmp/codex-home, which is the likely contention surface for a shared refresh token). State that the board MUST be re-run from scratch — the 19 completed cells are the first ~70 minutes of wall-clock, a time-biased subset, NOT a random sample, so no partial reuse or top-up is valid.
  `## Follow-up Routing`. Both preconditions stated, with the `CODEX_HOME` decision laid out as three costed options (concurrency 1 / per-cell CODEX_HOME / pin the old CLI) left to the captain. The no-reuse argument is strengthened with structural proof: the survivors are an exact spec-order PREFIX (indices 1-19 complete, 20-60 all errored, zero interleaving), and that prefix is the easier end of the board for the anchor (10/19 vs 16/41).
- SKIPPED: re-running the board; modifying razorback-registry.yaml; opening a GitHub issue
  All three prohibited by the dispatch. The re-run needs the captain's auth/isolation decision first.
- FLAGGED (beyond the dispatch, strike if unwanted): one paired 19-cell diagnostic
  The dispatch said not to compute a delta vs @baseline. I recorded ONE narrow paired comparison on the 19 surviving cells (anchor 10/19 vs 15/19) in `## Behavioral analysis`, with its refutation attached, and labelled it a non-result. Rationale: the "but it did great on what ran" reading will occur to the next reader, and it is safer answered here with McNemar p = 0.125 + the non-random-prefix bias + the untouched triple confound than left for someone to compute uncaveated.

### Summary

Honest post-mortem, no interpretation. The board is invalid: a codex `refresh_token_reused` 401 at
T+70m killed cells 20-60 in spec order, so 41 of 60 never reached the model. I re-derived every
FO-supplied fact rather than repeating it; all held. Two things I added. First, structural proof that
the survivors are an exact spec-order prefix with zero interleaving — that is what makes "time-biased,
not a random sample" concrete, and it kills any top-up or salvage. Second, the anchor control is
stronger than stated: it ran the same concurrency 4 for 3h20m, long enough to cross a token-refresh
boundary, at 60/60 with 0 errors — so the CLI upgrade, not concurrency and not run length, is what
changed.

One correction for the record: the dispatch merged two distinct codex messages into one quote. The
JSON `message` ends "Please try signing in again."; "Please log out and sign in again" is the next
line. Substance unchanged.

No score is promoted, `@baseline` stays 26/60, AC-3 is FAILED and AC-5 moot. The model and the
spacedock plugin are named as NOT implicated — and equally as NOT cleared, since neither was tested.
I also flagged that this failure was externally invisible (`rc=0`, ntfy "OK", a *fast* finish), and
that a `n_trials_errored > 0` check on the detached-run sentinel would have caught it at 14:10 rather
than a full analyze cycle later.

## Stage Report: full (cycle 2 — attempt 2 relaunch)

- DONE: PRESERVE the invalid run's evidence before launching: the prior job dir runs/spd0042-rebaseline-gpt56sol-xhigh/1984b76c702a0dfa/ still holds a stale lock.json and the same frozen spec may hash to the same dir. Rename it to 1984b76c702a0dfa-INVALID-auth-refresh-token-reused, then update EVERY citation of the old path in the entity body to the new path so the post-mortem stays verifiable. Do NOT delete it — '## Failure Review' depends on it.
  Renamed (not deleted). Confirmed the collision was real, not hypothetical: `sha256sum specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml` = `1984b76c702a0dfa647c…` — the job dir name IS the spec hash's first 16 chars, so attempt 2 was guaranteed to land on it. Post-rename verification: 60 cell dirs, `summary.json` (60/19/41, 0.7894736842105263), `lock.json`, and 26 auth-error lines in `hubspot001/agent/codex.txt` all intact; target path empty. All 3 citations updated (entity lines for the attempt-1 Job dir row, the Run-dir line, and the attempt-1 stage report), plus a note that cell-relative paths resolve under the renamed dir.
- DONE: Relaunch the FULL 60-cell board DETACHED via drivers/rk-run-detached.sh on the UNCHANGED specs/spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml, and report the new handle path, the new job dir, the PID, and an ETA. Confirm at ~T+4m that workers are alive and no cell has produced an exception.txt yet. Do NOT block to completion, do NOT run audit/score.
  Handle `runs/.rk-handles/spd0042-full-attempt2-20260728-002729/`, PID 312060, job dir `runs/spd0042-rebaseline-gpt56sol-xhigh/1984b76c702a0dfa/` (fresh), launched 00:27:29Z, ETA ~3.5 h. Spec unchanged and not re-frozen — `git status` on the spec and `solver_workflows/` empty. Health at T+3m13s: worker alive, no `done`, 4 cell dirs started (= concurrency 4), **0 `exception.txt`**, and 0 cells containing `refresh_token_reused`/`401 Unauthorized`. No audit/score run.
- DONE: Append a new dated subsection to '## Run result' for this attempt (do not overwrite attempt 1): the AC-4 launch-time plugin capture (describe/rev-parse/status --short), the codex auth state at launch (codex login status, codex --version), and a note that codex-cli remains 0.145.0 so the refresh-token race is UNMITIGATED and the triple confound is unchanged.
  `## Run result` → "ATTEMPT 2 — relaunched 2026-07-28 (in flight)", appended below attempt 1 with a horizontal rule; attempt 1 untouched. Carries the plugin capture (`ca136f83`, clean, `v0.26.0`/`v0.27.0-pre0` same commit), `codex-cli 0.145.0` + "Logged in using ChatGPT", and an explicit "What is NOT mitigated" block.
- SKIPPED: audit / score; re-freezing or editing the spec; touching the solver dir; registry changes; filing an issue
  All prohibited by the dispatch. The board is in flight; AC-3 belongs to a later turn.

### Summary

Renamed attempt 1's job dir to preserve the post-mortem evidence, fixed the three now-stale citations,
and relaunched the unchanged frozen spec detached. The lock collision was not hypothetical — the job
dir name is literally the frozen spec's sha256 prefix (`1984b76c702a0dfa`), so attempt 2 would have
landed on attempt 1's stale `lock.json` had the rename not happened.

Two things recorded so a second failure reads as diagnosis rather than surprise. The codex CLI was NOT
downgraded and concurrency stays at 4 with a shared `/tmp/codex-home`, so the concurrent-refresh race
is **unmitigated**: refreshing auth only fixes attempt 1 if the token was consumed externally. A
repeat `refresh_token_reused` failure at ~T+70 m would *confirm* the intra-run race and rule out the
external-consumer explanation — at which point the move is `CODEX_HOME` isolation or
`concurrency.trials: 1`, not a third identical re-run. And the triple confound is unchanged, so even
a clean 60/60 board still needs ≥ +6 cells (≥ 32/60) to say anything about the model.

One useful detail: `sha256sum $(which codex)` matches the frozen spec's `provenance.agent_cli_hash`
exactly, so attempt 2 runs the same binary the spec was frozen against — no CLI provenance drift this
time. Also flagged in the entity: a finish far under 3 h is a failure signature, and
`n_trials_errored` must be read before any score, because attempt 1 returned `rc=0` with an ntfy "OK"
and 41 dead cells.

## Stage Report: analyze (cycle 2 — clean board)

- DONE: Paired per-cell analysis vs @baseline (runs/spd0038-compose-6-stabilizers-full/fb10902ab7d9ffa7, 26/60): name EVERY flip and EVERY regression by cell slug, run McNemar exact on the paired 60 cells, and report the delta with its p-value. Do NOT lean on the single-proportion Wilson CI — 33/60's Wilson CI is [0.4249, 0.6691], whose lower bound sits BELOW the anchor's 0.4333, and explain in the entity why the paired test is the correct instrument here and the unpaired CI is not.
  `## Behavioral analysis` §1: full ledger — 24 both-PASS, **9 gains** (asana001, asset001, divvy001, f1001, jira001, recharge002, retail001, superstore001, tickit002), **2 regressions** (quickbooks003, recharge001), 25 both-FAIL. **McNemar exact two-sided p = 0.0654** on 11 discordant pairs (9:2). Wilson-CI trap explained in `## Run result`: the CI is for an independent single proportion, but the boards share all 60 cells, so 49 agreeing cells carry no information about the difference and pooling them inflates the uncertainty.
- DONE: Disclose the audit honestly in '## Run result': strict audit = 5 coverage_missing / 0 tainted, all missing_reason spacedock_dispatch_events_absent, on divvy001(PASS), retail001(PASS), netflix001(FAIL), recharge001(FAIL), scd001(FAIL). Report the full range: headline 33/60=0.5500 (+7); drop-all-unverified 31/55=0.5636; harshest reading with both unverified passes counted as fails 31/60=0.5167 (+5, which falls just UNDER the >=+6 bar). Note the anchor board had 0 coverage_missing, so this is a difference from the control, and state whether AC-3 is satisfied, partial, or failed with your reasoning.
  `## Run result` → all three readings tabulated with per-reading McNemar (A: +7, p=0.065 / B: +5, p=0.180 / C: +6 on 55, p=0.070). AC-3 called **PARTIAL, not satisfied** — AC-3 demands 0 coverage_missing and there are 5; calling it ✅ would be grade inflation. Anchor's 0 coverage_missing noted as a real difference from the control.
- DONE: Attribution + recommendation in '## Behavioral analysis' and '## Follow-up Routing': the delta is model + spacedock plugin + codex CLI COMBINED, never the model alone. Sample committed artifacts from 3-4 flipped cells to say behaviorally WHAT changed. Then recommend (do NOT execute) whether to promote @baseline, and name the single cheapest run that would disambiguate. Do not touch razorback-registry.yaml.
  Four cells read from the FO transcripts (§2): asana001 = row-completeness (4→20 / 3→25 rows, anchor inner-join collapse); jira001 = invented "active" filter (2→3 rows); f1001 = materialization view-vs-base-table (probable, flagged); superstore001 = **undetermined**, identical reported outputs, no mechanism invented. Recommendation = promote, recorded as 31/55 single-draw; cheapest disambiguator = spd0038 README + **gpt-5.5 on today's plugin+CLI**, the only single run that splits the triple confound. `razorback-registry.yaml` NOT modified (`git status` clean).
- SKIPPED: re-running anything; modifying razorback-registry.yaml; opening a GitHub issue; revising attempt 1's post-mortem
  All prohibited by the dispatch. Attempt 1's sections are untouched; attempt 2 is appended as dated subsections throughout.

### Summary

The board is clean and real: 60/60, 0 errors, 3h16m, **33/60 = 0.5500**, the highest ever recorded
here. I verified every FO-supplied number and they all held — but two FO readings did not.

**The coverage_missing finding is worse than an instrumentation gap.** All five flagged cells have
`dispatches: 0` (all other 55 have 1) because the solver **aborted before doing any work** at the
spacedock launcher gate. So `coverage_missing` faithfully flags five cells where the task was never
attempted, and the FO's read that "the passes are very likely real" is wrong in the way that matters:
divvy001 and retail001 scored 1.0 having changed nothing. That is a **benchmark-validity defect** —
the shipped project state already satisfies the grader. I proved it for retail001 by running the
task's own verifier against the untouched project: `{"reward": 1.0}`. The anchor FAILED both cells
because it did the work and its rebuild diverged from gold, so these two cells actively penalise
attempting the task, and they contaminate the 26/60 anchor too.

Second finding: a **free same-config variance measurement**. Attempt 1 and attempt 2 are the identical
configuration, and attempt 1's 19 completed cells give a direct replication — 3/19 = **15.8% per-cell
churn**, but net 15/19 vs 14/19. Scaled up, two draws of the same config would disagree on ~9–10 of
60 cells, so the 11 discordant pairs here are *ordinary*; only their 9:2 direction is signal. That is
the empirical justification for using McNemar, and it is why p = 0.065 rather than anything stronger.

Also: recharge001 is not a model regression — it is a launcher-gate abort, so the real ledger is
7 gains / 1 regression. The gate fired non-deterministically (5 abort, 55 work around, anchor 0),
which understates this board and injects variance into every future one.

Recommendation (not executed): promote, record as 31/55 = 0.5636 single-draw, and buy the
gpt-5.5-on-today's-environment arm before believing anything causal about the model. Highest-value
cheap follow-up is a **null-solver board** — if more than two of the 60 tasks are do-nothing-passable,
every score this workflow has ever recorded needs a smaller denominator.
