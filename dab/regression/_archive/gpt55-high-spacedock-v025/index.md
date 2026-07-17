---
id:
title: gpt-5.5 @ high — spacedock v0.25 (spacedock release)
status: done
source: spacedock v0.25.0 release (captain-filed 2026-07-16)
started: 2026-07-16T16:20:11Z
completed: 2026-07-17T03:33:54Z
verdict: PASSED
score:
worktree:
issue:
pr:
trigger: spacedock-release
model: gpt-5.5
effort: high
spacedock-version: v0.25.0 (601c3f53)
draws: '["regr-sd0250-gpt55-high/3a67e091dc4b2d5f#attempt-0", "regr-sd0250-gpt55-high/3a67e091dc4b2d5f#attempt-1", "regr-sd0250-gpt55-high/3a67e091dc4b2d5f#attempt-2", "regr-sd0250-gpt55-high/3a67e091dc4b2d5f#attempt-3", "regr-sd0250-gpt55-high/3a67e091dc4b2d5f#attempt-4"]'
pass-at-1: 0.6639
pass-at-1-sd: 0.0780
tokens-total: 75435103
mean-session-sec: 808
artifact-url: https://claude.ai/code/artifact/eb40262c-da0b-4b80-bcf0-b565e7a5dfed
archived: 2026-07-17T03:33:54Z
---

Regression run for the spacedock v0.25.0 release: pinned config (spacedock harness +
dab0022 semi-structured-rules README, gpt-5.5 @ high, batch query mode), 5 full DAB
draws as ONE rk run (`trials: 5`, `concurrency.trials: 4`). Subject checkout confirmed
at tag v0.25.0, commit 601c3f53. Compares against the v0.22 baseline row (0.7433) —
note the ~+0.04 plugin-version effect when reading the delta.

## Acceptance criteria

**AC-1 — Five clean (or disclosed-substitution) full draws exist under `dab/runs/`.**
Verified by: the 5 entries in `draws` each resolve to a completed trial in the run dir.

**AC-2 — pass@1, tokens, and timing in frontmatter match the extractor output.**
Verified by: re-running `extract_benchmark_data.py` over the run dir.

**AC-3 — The run's row is live on the regression Artifacts page at the recorded URL.**
Verified by: `artifact-url` set; row visible with matching numbers.

## Draws

One rk job (`regr-sd0250-gpt55-high/3a67e091dc4b2d5f`, 60/60 trials completed, 0
errors), 5 harbor attempts x 12 datasets. Draw = harbor attempt, grouped by
`trial_index` in the job's `per_trial_outcomes.json` (verified: every dataset has
exactly trial_index 0–4; attempts interleave in wall-clock, they are not time blocks).
Stratified pass@1 per draw = mean over the 12 per-dataset trial rewards of that
attempt. Numbers produced by the one-off script
`analyze_sd0250.py` (committed beside this entity; reuses
`extract_benchmark_data.py`'s harbor token/duration functions unmodified); micro
trial-mean cross-check 0.663855 == harbor `result.json` headline.

| draw | experiment | stratified pass@1 | notes |
|------|-----------|-------------------|-------|
| 0 | 3a67e091dc4b2d5f attempt-0 | 0.7022 | music_brainz q1 validator crash (float answer) |
| 1 | 3a67e091dc4b2d5f attempt-1 | 0.7280 | PANCANCER_ATLAS zeroed 3/3 queries by validator crashes |
| 2 | 3a67e091dc4b2d5f attempt-2 | 0.7302 | PATENTS q1 validator crash (list answer) |
| 3 | 3a67e091dc4b2d5f attempt-3 | 0.5730 | PANCANCER_ATLAS zeroed 3/3 + music_brainz q1 crash |
| 4 | 3a67e091dc4b2d5f attempt-4 | 0.5858 | PATENTS zeroed 3/3 + GITHUB_REPOS 3/4 queries crashed |

**mean 0.6639, sd 0.0780, min 0.5730, max 0.7302** (raw, as-scored).

Sensitivity: substituting each crashed query-cell with that query's mean reward over
its crash-free draws gives per-draw 0.7300 / 0.7835 / 0.7580 / 0.6564 / 0.6761 →
**substituted mean 0.7208, sd 0.0538**. Draws 3–4 stay lowest even after
substitution, so part of their gap is genuine variance, but ~0.06 of the headline
drop is validator-crash mechanics.

Tokens (harbor `sessions/` rollouts, FO+ensign threads, extractor `tokens_harbor`
path): **75,435,103 total / 1,614,608 output**, no incomplete-rollout trials flagged.
Mean session wall-clock (trial `result.json` started→finished): **808 s** (p50 715,
max 1774), no timeouts, no failed sessions. Whole-job wall-clock: 2026-07-16
16:27:28Z → 19:57:42Z = **3h30m14s** (trial activity window 16:27:35 → 19:57:42).

## Taint audit

Run BEFORE trusting any number; all 60 trial dirs swept.

- **Validator-error grep** (`reward_per_query.json`, all 60 trials): **7 trials hit,
  15/270 query-cells zeroed by `validator error`** — the known answer-shape crash
  family (`'list' object has no attribute 'lower'`, plus float/int/dict variants of
  the same non-string-answer TypeError/AttributeError). Every one of the 5 draws is
  hit at least once; 4 dataset-trials were fully zeroed (PANCANCER_ATLAS in draws 1
  and 3, PATENTS in draw 4, GITHUB_REPOS 3-of-4-queries in draw 4). This is a large
  spike vs the historical rate (~1 dataset per 5 draws, ~1–2 cells/60 trials). Per
  standing policy these are genuine draws (solver emitted non-string answers; the
  fragile validator zeroes them), NOT infra taint — but at this frequency the crash
  spike is itself the candidate v0.25 regression signal, and clean-draw substitution
  is not available as a headline fix since no draw is crash-free.
- **Postgres-degradation dual signature**: zero `coverage_missing` hits and zero
  mid-run Connection-refused abstains across all verifier outputs — **clean**.
- **Coverage**: all 12 datasets present in all 5 draws (12 x trial_index {0..4}),
  60/60 trials completed, 0 errored — **complete**.
- **Session health**: no codex timeouts, no failed sessions (extractor
  `timeouts_harbor`: none); attempts interleave across the full 3.5 h window, so the
  two low draws are not correlated with any time-local degradation — **clean**.

Verdict: no infrastructure taint. The low draws are explained by (a) the validator
answer-shape crash spike and (b) residual genuine variance, both solver-behavior
phenomena under the v0.25 harness.

## Comparison vs v0.22 baseline

Raw stratified **0.6639 (sd 0.0780) vs the v0.22 baseline row 0.7433 (sd 0.0488):
delta −0.0795**, far outside the ±0.03 five-draw noise band. The confound cuts the
wrong way for v0.25: plugin version alone measured ~**+0.04** going v0.22→v0.24 on
this config (gpt-5.5 dab0022 xhigh 0.704→0.748; v0.24 ≈ high on 5.5), so against a
v0.24-era expectation (~0.74–0.78) the raw gap is effectively ~−0.08 to −0.12. Even
the crash-substituted sensitivity number 0.7208 sits −0.023 below the v0.22 baseline
(within the noise band, but the direction is negative and the baseline itself
predates the +0.04 plugin lift). Cost also moved: tokens 75.4M vs 58.3M (**+29%**)
and mean session 808 s vs 637 s (**+27%**). This is the first row on plugin v0.25
(checkout 601c3f53, tag v0.25.0); no other v0.25 measurements exist yet, so
attribution to the release vs. an unlucky job cannot be settled from this run alone —
but the coherent picture (score down, answer-shape crash rate up ~7x, tokens and
wall-clock up ~30%) points at a real behavioral change in the v0.25 harness rather
than sampling noise.

## Re-grade of the 15 validator-crashed cells (faithful str-coercion)

The 15 `validator error` cells were re-graded the way the harness's own **single-answer**
path would grade them: recover the solver's JSON answer value, apply `str()`-coercion
exactly as `verify.py:33` (`return str(raw["answer"])`) does, then re-run that query's
shipped `validate.py`. Answer values were recovered **literally** from each trial's
`sessions/` rollout — the solver's own verification commands echoed the full
`answers.json` (via `python -m json.tool` / `sed` dumps or the `apply_patch` add-block).
Every raw value was first confirmed to reproduce the **same** exception recorded in
`reward_per_query.json` (proof the source `validate.py` is the identical validator), then
str-coerced and re-graded. One cell (`PATENTS gyJU8bk q1`, a 1503-item list) was
**regenerated** by re-running the solver's deterministic `analyze_dataset.py` against the
local `patent_publication.db` (q1 head + count 1503 reproduced byte-for-byte).

| dataset · trial | q | recovered value (shape) | method | raw | corrected | basis |
|---|---|---|---|:--:|:--:|---|
| GITHUB_REPOS · naR27Bq | q1 | float `0.17894…` | recovered | 0 | **0** | rounds to 0.18, gt wants 0.33 — genuine wrong value |
| GITHUB_REPOS · naR27Bq | q3 | int `1077` | recovered | 0 | **1** | `1077` present as substring |
| GITHUB_REPOS · naR27Bq | q4 | list[5] repos | recovered | 0 | **1** | all 5 repo names fuzzy-match |
| music_brainz · GWkSAqQ | q1 | float `1059.46` | recovered | 0 | **1** | equals gt 1059.46 |
| music_brainz · qpXdM35 | q1 | float `1059.46` | recovered | 0 | **1** | equals gt 1059.46 |
| PANCANCER · RQG9mgJ | q1 | list[3] dicts (names) | recovered | 0 | **0** | answered histology **names**, gt needs codes `9382/3…` — genuine miss |
| PANCANCER · RQG9mgJ | q2 | list[3] dicts | recovered | 0 | **1** | all 3 gt names present |
| PANCANCER · RQG9mgJ | q3 | float `305.1239` | recovered | 0 | **1** | equals gt 305.12 |
| PANCANCER · twXnPRq | q1 | dict[3] (names) | recovered | 0 | **0** | names not codes — genuine miss |
| PANCANCER · twXnPRq | q2 | list[3] dicts | recovered | 0 | **0** | missing `Mixed Histology (please specify)` — genuine miss (differs from RQG9mgJ) |
| PANCANCER · twXnPRq | q3 | float `47.519` | recovered | 0 | **0** | chi-square 47.5 vs gt 305.12 — genuine wrong value |
| PATENTS · gyJU8bk | q1 | list[1503] level-5 codes | regenerated | 0 | **0** | level-5 granularity misses 11/72 gt subclasses (A41G, B04B…) — genuine miss |
| PATENTS · vxdxuQ6 | q1 | list[72] codes | recovered | 0 | **1** | all 72 gt CPC codes present |
| PATENTS · vxdxuQ6 | q2 | list[23] dicts | recovered | 0 | **0** | correct data, but `str(dict)` interleaves keys → year falls outside validator's ±15-char proximity window |
| PATENTS · vxdxuQ6 | q3 | list[3] dicts | recovered | 0 | **0** | same ±15-char proximity break from dict serialization |

**7 of 15 flipped to PASS; 8 stay 0.** Of the 8 that stay 0: **6 are genuine misses**
(wrong value or wrong format — would score 0 at any serialization), and **2**
(vxdxuQ6 q2/q3) are correct-data cells that fail a proximity-sensitive validator only
because the solver's list-of-dicts `str()` interleaves key names between value and year —
these are NOT recoverable by the coercion fix (the single-answer path str-coerces the
same list and would also fail). So the batch-path bug wrongly zeroed **7** cells, not 15.

### Corrected v0.25 stratified pass@1

Overlaying the 15 corrected rewards onto the per-query rewards and recomputing
(`corrected_recompute.py`; raw-recompute re-derives the per-trial rewards and asserts they
match `per_trial_outcomes.json` before overlaying):

| draw | raw | corrected | delta |
|------|-----|-----------|-------|
| 0 | 0.7022 | 0.7300 | +0.0278 |
| 1 | 0.7280 | 0.7835 | +0.0556 |
| 2 | 0.7302 | 0.7302 | +0.0000 |
| 3 | 0.5730 | 0.6008 | +0.0278 |
| 4 | 0.5858 | 0.6553 | +0.0694 |

**Corrected mean 0.7000, sd 0.0718** (raw 0.6639 sd 0.0780). **delta vs raw +0.0361**;
**delta vs v0.22 baseline 0.7433 = −0.0433** (raw was −0.0794). The faithful re-grade
lands **below** the earlier optimistic clean-draw substitution (0.7208) — because that
substitution assumed crashed cells would recover to the clean-draw mean, whereas 8/15 are
genuine misses. Even fully crediting the harness batch-bug (+0.036), v0.25 still sits
−0.043 under the v0.22 baseline and further under a v0.24-era expectation (~+0.04 plugin
lift), so the batch-path crash is **not** the whole story — a real ~−0.04 to −0.08
component remains (wrong answers + list-serialization proximity failures + variance).

## Root cause

Two distinct effects, only one of which is a harness bug:

1. **Batch-verifier answer-shape crash (harness bug, AMPLIFIER).** The batch verifier
   `verify_batch.py:24` reads `answer = answers.get(key, "") if isinstance(answers, dict)
   else ""` and passes that **raw** JSON value straight into `validate_fn(answer)`
   (line 33). The single-answer path `verify.py:33` instead coerces `return
   str(raw["answer"])` before validating. So when a solver emits a list/dict/number-shaped
   answer, the single path grades a stringified answer while the **batch path crashes**
   inside the validator (`.lower()`/`re.*`/`unicodedata.normalize` on a non-str →
   `AttributeError`/`TypeError`), and the offending query is scored 0 with the exception as
   its reason. This is a batch-path bug that **amplifies** the solver's list-answer style
   into score-0. Faithful fix = coerce `str(answer)` at line 24 (mirroring line 33); it
   recovers **7** of the 15 cells (+0.036 headline). NOTE the fix is a follow-up the
   captain decides — the shipped verifier was **not** edited here (demonstrated in a scratch
   copy only).
2. **Genuine solver behavior (NOT a harness bug).** 8/15 crashed cells fail even after
   str-coercion: 6 are wrong answers/formats (e.g. PANCANCER histology **names** vs gt
   **codes**; gyJU8bk's level-5 granularity missing 11/72 subclasses; twXnPRq q3 chi-square
   47.5 vs gt 305.12) and 2 are correct-data list-of-dicts whose `str()` serialization
   breaks a validator's ±15-char proximity window. These would be 0 regardless of the batch
   bug. The crash spike therefore **co-occurs with** but does not fully explain the v0.25
   score drop.

## Publication

## Execution log

- **Spec:** `dab/specs/regr-sd0250-gpt55-high.yaml` (commit 69d82e9) — exact copy of
  `dab/specs/dab0022-patents-semistructured-rules.yaml` with only 3 lines changed
  (`experiment`, `trials: 1→5`, `concurrency.trials: 2→4`); proven by `diff` (3 hunks,
  model gpt-5.5 / reasoning_effort high / query_mode batch untouched).
- **Freeze step (incident, resolved):** first launch (PID 149447, 16:23:11Z) died at spec
  validation — `SpecError: spacedock_solver spec must be frozen (agent.sealed_hash missing)`.
  No run dir was created (no collision, no taint). Froze the spec with
  `rk freeze specs/regr-sd0250-gpt55-high.yaml --allow-missing` (same `--allow-missing`
  pattern as all prior frozen specs, which carry `model_resolved_version: null`) →
  `dab/specs/regr-sd0250-gpt55-high.frozen.yaml` (sealed_hash `98a1bcc03aec6391dd622e641d3659cf`,
  commit c97d681; `specs/provenance.yaml` is gitignored) and relaunched on the frozen spec.
- **Launch command (relaunch, the live run):**
  `cd /home/kent/autobench/dab && nohup env RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml uv run --project ../razorback rk run specs/regr-sd0250-gpt55-high.frozen.yaml > /tmp/regr-sd0250-gpt55-high.log 2>&1 & echo $! > /tmp/regr-sd0250-gpt55-high.pid`
- **Log:** `/tmp/regr-sd0250-gpt55-high.log` (empty early on — rk stdout is block-buffered
  under nohup; startup was instead proven via docker)
- **PID:** 150290 (nohup wrapper; rk child 150292), pid file `/tmp/regr-sd0250-gpt55-high.pid`
- **Launched:** 2026-07-16T16:26:21Z
- **Startup confirmed:** at ~16:30Z the rk child was alive (etime 03:40) and 4 task
  environments were Up in docker — `patents`, `pancancer_atlas`, `github_repos`,
  `deps_dev_v1` — i.e. 4 concurrent slots on 4 different datasets, matching
  `concurrency.trials: 4` and harbor's attempt-major queue.
- **Spacedock checkout re-confirmed:** `git -C /home/kent/autobench/spacedock rev-parse HEAD`
  = `601c3f53`; that commit carries BOTH tags `v0.25.0` and `v0.26.0-pre0` (same commit),
  so bare `describe --tags` prints `v0.26.0-pre0` while
  `describe --tags --exact-match --match 'v0.25.0'` confirms `v0.25.0`. Checkout is the
  v0.25.0 release commit as required; not modified by this stage.
- Stage parked; run in progress (expected hours for 60 trials).

## Stage Report: execution

- DONE: Write the pinned spec dab/specs/regr-sd0250-gpt55-high.yaml as an exact copy of dab/specs/dab0022-patents-semistructured-rules.yaml changing ONLY experiment, trials 1->5, concurrency.trials 2->4, and commit the spec
  diff proved exactly 3 hunks (experiment/trials/concurrency; model+effort+query_mode untouched); committed 69d82e9; frozen copy (required by rk SpecError) committed c97d681
- DONE: Launch ONE detached rk run of that spec (nohup + log + pid file) with RAZORBACK_SPACEDOCK_PLUGIN_DIR and RAZORBACK_REGISTRY exported first; verify the process is alive and the run started before signaling
  PID 150290 launched 16:26:21Z on the frozen spec; alive at 03:40 etime with 4 dataset environments Up in docker (patents/pancancer_atlas/github_repos/deps_dev_v1) = run materializing; log buffered-empty, startup proven via docker
- DONE: Record in the entity body under a new "## Execution log" section: launch command, log path, PID, timestamp, and v0.25.0/601c3f53 re-confirmation; do NOT wait for the benchmark to finish
  Execution log section added above; 601c3f53 confirmed carrying tag v0.25.0 (also tagged v0.26.0-pre0, same commit — bare describe shows the later tag)

### Summary

Pinned spec created as a verified 3-line fork of the dab0022 spec and committed. First launch failed fast on rk's frozen-spec requirement (SpecError, no run dir created); spec was frozen with --allow-missing per repo convention and relaunched. The 60-trial run (5 draws x 12 datasets, concurrency 4) is confirmed live via docker task environments and is parked to completion; log/PID/timestamps and the v0.25.0 checkout confirmation are recorded in the Execution log.

## Stage Report: analysis

- DONE: Fill the entity's "## Draws" table with the per-draw stratified pass@1 (5 draws = the 5 harbor attempts of the 60-trial job, grouped by attempt from trial metadata) plus mean/sd/min/max, and set frontmatter pass-at-1, pass-at-1-sd, tokens-total (harbor sessions/ rollouts via the extractor's tokens_harbor path — NEVER codex stdout), mean-session-sec, and draws (5 attempt references)
  Draws table filled (0.7022/0.7280/0.7302/0.5730/0.5858, mean 0.6639 sd 0.0780); frontmatter set via spacedock status (pass-at-1 0.6639, sd 0.0780, tokens-total 75435103 from tokens_harbor over sessions/ rollouts, mean-session-sec 808, draws = 5 attempt refs); draw split verified against trial_index in per_trial_outcomes.json and micro-mean cross-check 0.663855 == harbor result.json
- DONE: Run the taint audit BEFORE trusting any number and record findings under "## Taint audit" (clean is a finding): grep every trial's reward_per_query for "validator error" (the known list-answer crash zeroes a dataset), check for the postgres-degradation dual signature (whole-dataset coverage_missing + mid-run connection-refused abstains), and confirm all 12 datasets have complete coverage in all 5 draws
  All 60 trials swept: 7 trials / 15 of 270 query-cells hit the answer-shape validator crash (every draw affected; 4 dataset-trials fully zeroed); postgres dual signature ZERO hits; coverage complete 12 datasets x 5 draws, 60/60 completed 0 errored; no timeouts/failed sessions
- DONE: Write a comparison paragraph in the entity body: delta vs the v0.22 baseline row (0.7433 sd 0.0488) and vs the ±0.03 five-draw noise band, explicitly noting the plugin-version confound (~+0.04 v0.22→v0.24 effect on this config) and that this is the first row on plugin v0.25
  "## Comparison vs v0.22 baseline" section added: raw delta −0.0795 (outside ±0.03), crash-substituted sensitivity 0.7208 (−0.023), plugin confound cuts AGAINST v0.25 (~−0.08 to −0.12 vs v0.24-era expectation), tokens +29% and session time +27%, first-v0.25-row caveat stated

### Summary

All five draws of the 60-trial v0.25 regression job were split by harbor attempt, audited, and scored: raw stratified pass@1 0.6639 sd 0.0780 vs the v0.22 baseline 0.7433 — a −0.08 drop that the plugin-version confound makes LARGER, not smaller. The taint audit found no infrastructure taint (postgres clean, coverage complete, no timeouts), but a ~7x spike in the known answer-shape validator crash (15/270 query-cells, every draw hit, 4 dataset-trials zeroed); crash-substituted sensitivity is 0.7208, still below baseline. Tokens (+29%) and session time (+27%) rose in the same run — a coherent behavioral-regression picture for the v0.25 harness rather than sampling noise.

GATE RECOMMENDATION: **PASSED** as a valid measurement — no draw is infrastructure-tainted, so re-running draws is not indicated (per standing policy the answer-shape crashes are genuine solver behavior, and with all 5 draws affected a re-run would sample the same elevated crash rate, which is itself the finding). The number that should go public is the raw 0.6639 with the crash-spike disclosure and the 0.7208 sensitivity alongside. Recommend the captain treat the v0.25 release as regression-flagged pending a confirming run or a v0.24-vs-v0.25 bisect before publicizing any release verdict.

## Stage Report: analysis (cycle 2 — re-grade of validator-crashed cells)

- DONE: Re-grade all 15 crashed query-cells (recover answer value, str-coerce per verify.py:33, re-run shipped validate.py, record per-cell corrected-reward table with method)
  14 recovered literally from rollout-captured `answers.json`, 1 (gyJU8bk q1) regenerated via the solver's `analyze_dataset.py` against the local DB; every raw value first reproduced the exact recorded exception (validators confirmed identical); table in "## Re-grade of the 15 validator-crashed cells"; 7 PASS / 8 stay-0; scripts+recovered data committed beside entity (`regrade.py`, `regrade_data/`, `regrade_results.json`)
- DONE: Recompute CORRECTED v0.25 stratified pass@1 (per-draw + mean/sd), state delta vs raw 0.6639 and vs v0.22 0.7433, plus flip count
  `corrected_recompute.py` (raw-recompute asserts match to per_trial_outcomes before overlay): corrected 0.7000 sd 0.0718; per-draw 0.7300/0.7835/0.7302/0.6008/0.6553; +0.0361 vs raw, −0.0433 vs v0.22; 7/15 flipped
- DONE: Record the root-cause reframe in "## Root cause" — batch verifier passes raw JSON value (verify_batch.py:24) vs single-path str-coercion (verify.py:33), amplifying list/dict answers into score-0
  "## Root cause" section added: (1) batch-path bug wrongly zeroed 7 cells (+0.036, faithful fix = str() at line 24, NOT applied to shipped code — scratch-copy demo only); (2) 8/15 are genuine solver behavior (6 wrong answers/formats + 2 dict-serialization proximity failures), so the crash spike co-occurs with but does not fully explain the drop

### Summary

Faithfully re-graded the 15 `validator error` cells by recovering each solver answer from the `sessions/` rollouts (one regenerated from the solver's deterministic script) and re-running the shipped `validate.py` after the same `str()`-coercion the single-answer path uses. Result: only **7 of 15** cells were wrongly zeroed by the batch-verifier bug; **8 are genuine misses** (wrong values/formats, or correct-data list-of-dicts that break a proximity-sensitive validator). Corrected stratified pass@1 is **0.7000** (sd 0.0718) — +0.036 over the raw 0.6639 but still **−0.043 below** the v0.22 baseline, and below the earlier optimistic substitution (0.7208). The batch-path crash is a real harness bug worth a one-line fix, but it is an amplifier, not the cause of the v0.25 regression.

UPDATED GATE RECOMMENDATION: **PASSED as a valid measurement, v0.25 REMAINS REGRESSION-FLAGGED.** The re-grade removes the "was it just the crash bug?" ambiguity: correcting the batch-verifier bug still leaves v0.25 at 0.700, −0.043 under v0.22 (and further under a v0.24-era expectation given the ~+0.04 plugin lift), with tokens +29% / session +27%. Publish the corrected **0.700** as the headline (raw 0.6639 with the batch-bug disclosure alongside), not the optimistic 0.7208. Two concrete follow-ups for the captain: (1) land the one-line `str()` coercion at `verify_batch.py:24` so future runs don't lose list-answer cells; (2) still run a v0.24-vs-v0.25 confirming bisect before any public release verdict, since ~−0.04 to −0.08 of genuine drop is unexplained by the crash bug.
