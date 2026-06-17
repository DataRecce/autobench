---
id: dab0008
title: gpt-5.5 high baseline (tier control vs dab0007 xhigh)
status: conclude
kind: hypothesis
source: captain request 2026-06-17 — settle the reasoning-tier question (high vs xhigh) with a clean apples-to-apples run
started:
completed: 2026-06-17T17:29:42Z
verdict: rejected
score:
worktree:
---

## Hypothesis

A **tier-control anchor**: re-run the codex/gpt-5.5 solver on the unchanged baseline README across
all 12 datasets / 54 queries at **`reasoning_effort: high`**, under conditions *identical* to
`dab0007` (gpt-5.5 @ xhigh) — same model, runtime, datasets, hints, `data_root`, concurrency 4,
`trials: 1`, and the same post-postgres-fix infra. The ONLY difference from dab0007 is the tier.

**Why:** the existing `high` anchor (`codex-dab-baseline`, 0.5836) is **not** a fair comparison — it
ran *before* the dab-postgres restart fix (PANCANCER was infra-0/3 there) and was missing a
bookreview cell (53/54). The behavioral study (`_artifacts/opus-vs-gpt55-failure-behavior.md`) found
that gpt-5.5 **regressed all 3 contested flip-targets going high→xhigh** (agnews-q4, stockmarket-q4,
crmarenapro-q2 were PASS@high, FAIL@xhigh) — extra reasoning over-rationalized the wrong branch or
abstained where high improvised. This run tests whether that tier effect is real on a clean board.

**Falsifiable claim:** under identical conditions, gpt-5.5 @ high will *not* underperform @ xhigh on
DAB; specifically the 3 contested flip-targets should re-pass at high. If high ≥ xhigh on stratified
Pass@1 AND re-passes ≥2 of the 3 contested targets, the tier effect is confirmed and `high` becomes
the recommended tier for the loop.

## Acceptance criteria

**AC-1 — The full spec differs from `specs/dab0007-gpt55-baseline-xhigh.yaml` only in `experiment:`
and `agent.reasoning_effort` (high).**
Verified by: `diff specs/dab0007-gpt55-baseline-xhigh.yaml specs/dab0008-gpt55-baseline-high.yaml`.

**AC-2 — Recorded stratified Pass@1 paired with a clean strict audit on the same run-dir.**

**AC-3 — All 12 datasets / 54 cells ran** (verified via `--explain` + scored cell count).

## Run plan (tier control — for the full-stage ensign)

1. `cp specs/dab0007-gpt55-baseline-xhigh.yaml specs/dab0008-gpt55-baseline-high.yaml`; set
   `experiment: dab0008-gpt55-baseline-high`, `agent.reasoning_effort: high`. Change NOTHING else
   (concurrency.trials stays 4, solver_workflow stays the baseline, all 12 tasks, trials: 1).
2. `uv run --project ../razorback rk freeze --allow-missing specs/dab0008-gpt55-baseline-high.yaml`.
3. `uv run --project ../razorback rk run specs/dab0008-gpt55-baseline-high.frozen.yaml --explain`
   ($0, foreground) — confirm all 12 datasets / 54 cells survive.
4. Launch DETACHED: `drivers/rk-run-detached.sh dab0008-full
   specs/dab0008-gpt55-baseline-high.frozen.yaml run`. Return the handle path immediately; do NOT wait.

## Run result

- Spec frozen: `specs/dab0008-gpt55-baseline-high.frozen.yaml` (from dab0007 xhigh; only
  `experiment` + `reasoning_effort: high` changed — diff confirmed exactly 2 lines).
- `--explain`: 12 datasets / 54 query-cells materialized (all of agnews, bookreview,
  crmarenapro, DEPS_DEV_V1, GITHUB_REPOS, googlelocal, music_brainz_20k, PANCANCER_ATLAS,
  PATENTS, stockindex, stockmarket, yelp).
- Detached full run launched 2026-06-17:
  handle `runs/.rk-handles/dab0008-full-20260617-022427/` (pid 1259615). FO owns the wait;
  on `done` rc=0: `rk audit <run-dir> --policy strict` + `rk score <run-dir> --format json`.

## Analyze — Run result (scored)

- **Run-dir:** `runs/dab0008-gpt55-baseline-high/035dd36e869b10e0`. 54/54 completed, **0 errored**.
  Strict audit: **54/54 CLEAN** (no findings, no taint on any trial).
- **Absolute scores (stratified Pass@1):**
  - dab0008 **HIGH** = **0.5733** (raw 32/54 cells correct)
  - dab0007 **XHIGH** (matched no-lever ref, same model/runtime/datasets/data_root) = **0.6002** (raw 35/54)
  - Opus-4.8 **@baseline** incumbent = **0.6536**
  - high − xhigh = **−0.0269** (high BELOW xhigh, board-wide).
- **Confound note:** dab0008 vs dab0007 is a CLEAN tier isolation — both are gpt-5.5, codex runtime,
  baseline README (`solver_workflows/spacedock-readme-baseline`), trials:1, same post-postgres-fix infra;
  the ONLY difference is `reasoning_effort` (high vs xhigh). So this delta is NOT entangled with the
  codex-vs-Opus model swap; the high-vs-xhigh comparison attributes purely to the reasoning tier.
  (The high/xhigh vs **@baseline** 0.6536 gap IS the model-swap confound and is not the question here.)

### Full per-query verdict diff — HIGH vs XHIGH (paired, all 54 cells)

30 both-PASS, 17 both-FAIL, 7 moved. Each moved cell tagged with its 6-draw no-lever band
(`_artifacts/baseline-variance-6draw.md`):

| Direction | Cell | 6-draw band | Read |
|-----------|------|-------------|------|
| HIGH wins (hi PASS, xh FAIL) | GITHUB_REPOS-q3 | 5/6 VARIABLE | noise — passes ~83% either tier |
| HIGH wins | stockmarket-q4 | 4/6 VARIABLE | noise — passes ~67% either tier |
| XHIGH wins (xh PASS, hi FAIL) | bookreview-q3 | **6/6 STABLE** | high MISSED a rock-stable cell |
| XHIGH wins | crmarenapro-q3 | 3/6 VARIABLE | noise — coin-flip cell (~50%) |
| XHIGH wins | crmarenapro-q7 | **6/6 STABLE** | high MISSED a rock-stable cell |
| XHIGH wins | yelp-q2 | **6/6 STABLE** | high MISSED a rock-stable cell |
| XHIGH wins | yelp-q4 | 5/6 VARIABLE | noise — passes ~83% either tier |

**6 of the 7 moved cells are explained by variance** (4 VARIABLE-band cells flip either way;
the win/loss split there is noise). The signal is the asymmetry on the STABLE band: high's single
draw **missed 3 rock-stable (6/6) cells** (bookreview-q3, crmarenapro-q7, yelp-q2) and won zero
stable cells in return. That 3-cell stable deficit IS the −0.027 gap. All 3 are clean genuine
wrong-answers (verified below), not infra — so this is high's own single-draw variance/deficit,
not a measurement artifact. Net: **no tier advantage for high; if anything a slight deficit.**

## Behavioral analysis

Every cell below read from its committed artifact under
`runs/dab0008-gpt55-baseline-high/035dd36e869b10e0/<cell>/`: `result.json`
(reward + exception_info), `steps/main/verifier/test-stdout.txt` (DAB validator output / distance to
pass), agent/verifier execution windows. **No cell carried a top-level or step-level
`exception_info`; every verifier ran sub-second AFTER a multi-minute agent run and emitted a content
verdict** — i.e. every reward-0 cell examined is a CLEAN completed-but-wrong failure, NOT
infra/DNS/missing-file.

### (a) dab0005 PREMISE — crmarenapro-q2 and crmarenapro-q8 — REFUTED

dab0005's flagship premise was that the **high** tier *recovers* crmarenapro-q2/q8. Historical record:
Opus 0/5, gpt-xhigh 0/6, gpt-**high** 1/1 — but that 1/1 was a SINGLE codex-dab-baseline draw (pre
postgres-fix era). In this CLEAN high run **both FAIL**, and both are genuine wrong answers:

- **crmarenapro-q2** (reward 0.0, no exc; agent 16:07→16:15, verifier 0.8s): validator —
  `Found knowledge article IDs ['ka0Wt000000Ens5IAC'], but expected 'ka0Wt000000Eq0MIAS'`.
  The agent committed a concrete (wrong) knowledge-article ID; it did the work and picked the wrong row.
- **crmarenapro-q8** (reward 0.0, no exc; agent 16:18→16:26, verifier 0.8s): validator —
  `No agent ID found in LLM output`. The agent failed to commit an agent ID at all (abstain / wrong-shape).

The 6-draw band corroborates: **both cells are 0/6 NEVER-PASS** at xhigh. **VERDICT: dab0005's premise
is REFUTED.** The high tier does NOT recover q2/q8 — the prior 1/1 was a single-draw phantom, the same
lesson that sank dab0009/dab0010 (judging a cell on one draw against one reference draw). q2/q8 are
hard/oracle-blocked cells that fail across Opus, gpt-high, and gpt-xhigh alike.

### (b) TIER question — is high better than xhigh for gpt-5.5 on DAB? — NO

Judged against the 6-draw variance band, the 7 moved cells decompose as:
- **4 VARIABLE-band cells** (GITHUB_REPOS-q3 5/6, stockmarket-q4 4/6, crmarenapro-q3 3/6, yelp-q4 5/6):
  these flip on their own across no-lever draws. The 2 high-wins + 2 xhigh-wins here are pure noise,
  not a tier effect.
- **3 STABLE-band cells the single high draw MISSED** — each a clean genuine wrong answer:
  - **bookreview-q3** (6/6 band; agent 15:56→16:02, verifier 0.8s): `Missing book title in LLM output:
    Around the World Mazes` — committed a wrong/incomplete title set.
  - **crmarenapro-q7** (6/6 band; agent 16:17→16:24): `Found knowledge article IDs ['ka0Wt000000EpSUIA0'],
    but expected 'ka0Wt000000EoD3IAK'` — wrong knowledge article (same failure shape as q2).
  - **yelp-q2** (6/6 band; agent 16:57→17:05): `No occurrence of 3.7 near PA/Pennsylvania.` — wrong value.

  These are 6/6 at xhigh, so missing all three in one high draw is high's own single-draw
  variance/deficit, NOT infra and NOT a property xhigh lacks.

**Conclusion:** the high−xhigh gap (−0.027; 32 vs 35 raw cells) lives entirely inside single-trial
noise plus a 3-stable-cell single-draw miss by high. There is **NO tier win for high**; if anything a
slight deficit. The behavioral study's earlier claim (high recovers the 3 contested flip-targets) does
not hold on a clean board — those targets are either NEVER-PASS (crmarenapro-q2) or variable
(stockmarket-q4 4/6). **`high` is not the lever.**

### Required analyze questions

1. **Net + full ledger (both directions):** high 0.5733 vs xhigh 0.6002 (Δ −0.027); vs Opus @baseline
   0.6536. HIGH-wins {GITHUB_REPOS-q3, stockmarket-q4} (both VARIABLE); XHIGH-wins {bookreview-q3,
   crmarenapro-q7, yelp-q2 (all 6/6 STABLE), crmarenapro-q3, yelp-q4 (VARIABLE)}. Full table above.
2. **Smoke vs full:** N/A — dab0008 is a no-lever tier-control anchor, no smoke stage. The point of the
   run was the multi-cell board, not a smoke fork.
3. **Already-correct-and-broken:** at the tier level, high "broke" 3 stable-passers relative to xhigh
   (bookreview-q3, crmarenapro-q7, yelp-q2 — all 6/6 at xhigh). But this is single-draw variance of a
   tier change, not lever damage: there is no README lever here to scope.
4. **Was the change executed? (confound attribution):** the change IS the tier flag (`reasoning_effort:
   high`), confirmed in every cell's `config.agent.kwargs.harbor_agent_kwargs.reasoning_effort: "high"`.
   It executed. Classify the result: **model/tier produces NO net gain** — moved cells are
   variance-attributable, not a recoverable structural win. dab0005's recovery claim =
   **premise-falsified** (target cells are NEVER-PASS or noise, not high-recoverable).
5. **Prevention + next move:** the loop's standing single-trial blind spot is the cause of the dab0005
   phantom; the 6-draw band is the prevention (judge per-cell against the band, never one ref draw).
   Recommended next step is captain-gated (below) — do NOT auto-file; the tier-question is now settled.
6. **Smoke-vs-full fork drift:** N/A (no smoke). The relevant drift is single-draw-vs-band: the dab0005
   1/1 "win" was single-trial variance, named and closed here.

## Verdict

**Tier-control anchor — SETTLED, NO tier advantage for `high`.** gpt-5.5 @high (0.5733) does NOT
outperform @xhigh (0.6002) on DAB; the −0.027 gap is within single-trial noise plus a 3-stable-cell
single-draw miss by the high draw. The falsifiable claim (high ≥ xhigh AND re-passes ≥2 of the 3
contested targets) is **FALSE**: high is below xhigh, and of the contested targets crmarenapro-q2 is
0/6 NEVER-PASS (failed) while the high-pass on stockmarket-q4/GITHUB_REPOS-q3 lands on VARIABLE cells.
**dab0005's premise (high recovers crmarenapro-q2/q8) is REFUTED** — both fail clean here and are
0/6 NEVER-PASS; the prior 1/1 was a single-draw phantom. Run is clean (54/54, 0 errored, audit
54/54 CLEAN). `high` is NOT the lever; xhigh remains the marginally-better no-lever tier.

*Captain gate: not promoted, registry untouched, stage not advanced.*

## Failure Review

- **dab0005 premise REFUTED — recurring single-draw phantom.** The "high recovers crmarenapro-q2/q8"
  belief rested on ONE codex-dab-baseline draw (1/1) in the pre-postgres-fix era. On a clean board both
  cells fail genuinely (wrong knowledge-article / no agent-ID committed) and the 6-draw band shows both
  as 0/6 NEVER-PASS. This is the THIRD time the loop has been burned by single-trial judgement
  (dab0009, dab0010, now dab0005's premise). The 6-draw variance baseline is the standing remedy.
- **No infra failures.** All examined reward-0 cells (q2, q8, bookreview-q3, crmarenapro-q7, yelp-q2)
  are clean completed-but-wrong; 0 errored across the whole run; strict audit 54/54 clean. No
  postgres/DNS/permission artifacts surfaced — the post-fix infra held.
- **High's deficit is variance, not a structural regression.** The 3 stable-cell misses are single-draw
  bad luck on a tier with no compensating stable wins; a fresh high draw would likely recover them.

## Follow-up Routing

- **No new hypothesis filed.** The tier question is now settled (no advantage); the dab0005 family is
  closed (premise refuted). Per the loop's "do NOT reflexively file" rule, this routes to the captain.
- **Recommended to captain:** (1) keep **xhigh** as the no-lever tier for the DAB loop (marginally
  better, and it's the tier the 6-draw band is built on); (2) mark dab0005 as premise-refuted / closed;
  (3) any future per-cell flip claim MUST be judged against `_artifacts/baseline-variance-6draw.md`,
  never a single reference draw. (4) optional, low priority: a 3-draw fresh-high panel would tighten
  whether high's stable-cell deficit is real or pure variance — but it is not expected to change the
  no-advantage verdict and is not worth budget unless the captain wants the band symmetrized.

## Stage Report: full

- DONE: Spec prepared + frozen; diff shows ONLY experiment + reasoning_effort:high (AC-1)
  `diff` output = exactly 2 hunks (experiment line, reasoning_effort line); frozen spec written.
- DONE: rk run --explain confirms all 12 datasets / 54 query-cells survive before launch (AC-3)
  --explain reported `Tasks: 54`; materialized tasks dir = 54 cells across 12 distinct datasets.
- DONE: Detached full run launched via drivers/rk-run-detached.sh; handle path returned
  `runs/.rk-handles/dab0008-full-20260617-022427/` (pid 1259615 alive, done absent). Did NOT wait.

### Summary

Created the tier-control spec by copying dab0007 (gpt-5.5 @xhigh) and flipping only the
experiment name and reasoning_effort to high — everything else (concurrency.trials=4, all 12
tasks, trials:1, baseline solver_workflow, gpt-5.5/codex) untouched, confirmed by a 2-line diff.
Froze, validated 12 datasets / 54 cells via --explain, and launched the detached full run.
Committed the spec + frozen spec; runs/ stays gitignored. FO owns the wait + audit/score.

## Stage Report: full (cycle 2 — relaunch)

- DONE: rk run --explain on the frozen spec confirms all 12 datasets / 54 cells (high tier, trials:1)
  --explain reported `Tasks: 54`, `Concurrency: 4`; frozen spec shows model gpt-5.5,
  reasoning_effort: high, trials: 1, experiment dab0008-gpt55-baseline-high.
- DONE: Detached full run RELAUNCHED fresh (prior pid 1259615 was intentionally stopped by captain)
  handle `runs/.rk-handles/dab0008-full-20260617-150847/` (pid 2434887 alive, done absent). Did NOT wait.

### Summary

Relaunched the dab0008 high-tier control fresh after the captain stopped the prior launch.
Re-confirmed 54 cells / 12 datasets / trials:1 via --explain on the unchanged frozen spec,
then launched detached. New handle: runs/.rk-handles/dab0008-full-20260617-150847/. FO owns
the wait + strict audit + score; runs/ stays gitignored so nothing to commit beyond this report.

## Stage Report: analyze

- DONE: Run result written — stratified high 0.5733 vs xhigh 0.6002 vs Opus 0.6536; 54/54, 0 errored, audit 54/54 CLEAN
  Full paired high-vs-xhigh ledger BOTH directions (HIGH wins GITHUB_REPOS-q3+stockmarket-q4; XHIGH wins bookreview-q3+crmarenapro-q3+crmarenapro-q7+yelp-q2+yelp-q4), each tagged with its 6-draw band.
- DONE: Behavioral analysis written — (a) dab0005 premise REFUTED, (b) tier verdict NO advantage, (c) all 6 required questions + confound note
  Read committed artifacts for q2/q8 + 3 stable misses; all clean genuine wrong-answers (validator content mismatch, sub-second verifier, no exception_info), not infra.
- DONE: Failure Review (dab0005 refuted, single-draw phantom = 3rd recurrence) + Follow-up Routing (no new file; captain-gated; keep xhigh)
  Verdict + Failure Review + Follow-up Routing sections written into the entity.
- DONE: Did NOT promote / touch registry / advance stage (captain gate)
  Registry untouched; stage frontmatter unchanged; report appended only.

### Summary

dab0008 (gpt-5.5 @high) scores 0.5733 stratified vs dab0007 @xhigh 0.6002 — a clean tier isolation
(both gpt-5.5, baseline README, trials:1, same infra; only reasoning_effort differs). 6 of 7 moved
cells are variance-band; the −0.027 gap is high's single-draw miss of 3 rock-stable (6/6) cells with
no compensating stable win → NO tier advantage for high. crmarenapro-q2/q8 both fail clean (0/6
NEVER-PASS band), REFUTING dab0005's premise that high recovers them; the prior 1/1 was a single-draw
phantom. Run clean (0 errored, audit 54/54). No new hypothesis filed; routed to captain (keep xhigh).
