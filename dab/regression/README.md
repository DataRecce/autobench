---
commissioned-by: spacedock@0.20.0
entity-type: regression_run
entity-label: run
entity-label-plural: runs
id-style: slug
state: $inline
stages:
  defaults:
    worktree: false
    concurrency: 1
  states:
    - name: queued
      initial: true
    - name: execution
      parked: true
    - name: analysis
      gate: true
      feedback-to: execution
    - name: published
    - name: done
      terminal: true
---

# DAB regression tracking

Track DAB benchmark regressions over time at a **pinned configuration**: the spacedock
solver harness carrying the dab0022 semi-structured-rules README, at **gpt-5.5 @ high
reasoning effort**. A run is triggered by one of two events: **spacedock releases a new
version** (re-run the pinned config on the new harness), or **a new GPT model ships**
(run the pinned harness with that model substituted, still @ high). Each run executes
**5 full DAB draws as ONE rk run** (`trials: 5`, `concurrency.trials: 4` — never five
sequential single-trial runs) and records three metrics — **stratified pass@1** (per-draw +
mean/sd), **execution time**, and **token usage** (from harbor rollouts, never codex
stdout) — then appends its row to the single **regression Artifacts page**, which is
updated in place at the same URL after every run.

This workflow is NOT the pass@1-maximizing hypotheses loop (`dab/hypotheses/`). The
config is frozen on purpose; the product is the longitudinal record, not a better score.

## Pinned configuration

- Harness: spacedock solver workflow (`agent.kind: spacedock_solver`, `runtime: codex`)
  with the dab0022 `### Semi-structured data rules` README lever
- Model: `gpt-5.5` @ `high` (a model-release trigger substitutes the new model, effort stays `high`)
- Query mode: **batch** (`plugin_args.query_mode: batch`, `workspace_variant: spacedock`) —
  the dab0022 baseline spec already carries this; the four-keys-only copy rule below
  preserves it. Never switch to per-query mode in this workflow.
- Draws per run: 5, configured in ONE spec as `trials: 5` with `concurrency.trials: 4`
  (draws = harbor attempts inside a single run dir; one experiment name per regression run)
- Benchmark: full DAB board (12 datasets, 54 queries)
- Baseline spec: `specs/dab0022-patents-semistructured-rules.yaml` — copy it and change
  ONLY `experiment:`, `model:` (per trigger), `trials: 1 → 5`, `concurrency.trials: 2 → 4`
- Concurrency safety: harbor's trial queue is attempt-major (attempt 1 of all 12 datasets,
  then attempt 2, …), so on a full-board run the 4 concurrent slots hold different datasets
  and the shared global pg volume is safe. A SINGLE-dataset re-run (feedback bounce) makes
  same-dataset trials consecutive and WILL collide on the volume — use `concurrency.trials: 1`
  there (the dab0018 lesson, scoped)

## Regression Artifacts page

- Page source: `dab/docs/benchmark-artifact/dab-regression.html` (created on first publish)
- Published via the Claude `Artifact` tool; re-publishing the same file path keeps the
  same URL. The live URL is recorded below and in each run's `artifact-url` field once known.
- Live URL: _(set at first publish)_

## File Naming

Each run lives as a folder `{slug}/` containing `index.md` as the canonical entity file,
with per-stage artifacts (draw tables, extractor JSON, taint-audit notes) alongside it.
Slugs encode subject + effort + harness version so both trigger types name uniformly:
`gpt55-high-spacedock-v025` (spacedock release), `gpt57-high-spacedock-v025`
(model release). Slugs are lowercase, hyphens, no spaces — and NO DOTS: the slug feeds
dispatch worker names, which reject anything outside `[a-z0-9-]` (drop the dots from
model and version numbers; the human-readable `title` keeps them).

## Schema

Every run file has YAML frontmatter. Fields are documented below; see **Run Template**
for a copy-paste starter.

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Optional — id-style is `slug`, the folder slug is the effective ID |
| `title` | string | Human-readable run name |
| `status` | enum | One of: queued, execution, analysis, published, done |
| `source` | string | Where this run came from (trigger event, or "backfill (…)") |
| `started` | ISO 8601 | When active work began |
| `completed` | ISO 8601 | When the run reached terminal status |
| `verdict` | enum | PASSED or REJECTED — set at final stage |
| `score` | number | Priority score, 0.0–1.0 (optional) |
| `worktree` | string | Unused in this workflow (no worktree stages) |
| `issue` | string | GitHub issue reference (optional) |
| `pr` | string | GitHub PR reference (optional) |
| `trigger` | enum | `spacedock-release`, `model-release`, or `baseline` (backfill) |
| `model` | string | Model under test (e.g., `gpt-5.5`) |
| `effort` | string | Reasoning effort — always `high` in this workflow |
| `spacedock-version` | string | `git -C spacedock describe --tags` at execution time |
| `draws` | list | The 5 draw references: `{experiment}/trial-{n}` for a native `trials: 5` run, or run-dir references for backfills |
| `pass-at-1` | number | Stratified pass@1 mean over the 5 draws |
| `pass-at-1-sd` | number | Stdev of the per-draw stratified pass@1 |
| `tokens-total` | integer | Total tokens across the 5-draw sweep (harbor rollouts, FO+ensign) |
| `mean-session-sec` | integer | Mean codex-session wall time in seconds |
| `artifact-url` | string | The regression Artifacts page URL this run's row is published on |

## Stages

### `queued`

A trigger event has been observed (spacedock release tag, or a new GPT model available
to the codex runtime) and the run is pinned but not yet launched. Set by whoever creates
the entity.

- **Inputs:** The trigger (release tag or model id); this README's Pinned configuration; the reference spec lineage
- **Outputs:** Frontmatter fully pinned: `trigger`, `model`, `effort: high`, `spacedock-version` (from `git -C spacedock describe --tags` — the plugin is sourced live and NOT pinned by rk, so record it now and again at execution); ONE fresh experiment name; ONE spec file written under `specs/` (copy `dab0022-patents-semistructured-rules.yaml`, change only `experiment:`, `model:`, `trials: 5`, `concurrency.trials: 4`)
- **Good:** The spec diffs against the dab0022 baseline in exactly those four keys and nothing else; spacedock version recorded before anything runs; slug matches the naming convention
- **Bad:** Reusing an experiment name from `dab/runs/`; writing 5 separate specs (draws are `trials: 5` attempts, not separate experiments); "improving" the README or spec while pinning — this workflow never tunes; leaving `spacedock-version` blank to fill in later

### `execution`

The 5 full DAB draws are running. This stage sits parked for hours — entities here are
normal, not stalled.

- **Inputs:** The pinned spec from `queued`
- **Outputs:** One completed run dir under `dab/runs/{experiment-name}/` containing all 5 trials; launch log path + PID recorded in the entity body; any mid-run incident (crash, re-launch, substitution) noted as it happens
- **Good:** ONE detached `rk run` (`nohup` + log + pid file — a 5-trial full-board run far exceeds the Bash timeout) with `trials: 5`, `concurrency.trials: 4`; `RAZORBACK_SPACEDOCK_PLUGIN_DIR` and `RAZORBACK_REGISTRY=dab/razorback-registry.yaml` exported before the launch
- **Bad:** Foreground `rk run` (dies at Bash timeout); executing the 5 draws one by one as separate runs; silently re-running a failed draw without noting it; single-dataset bounce re-runs at `concurrency.trials` > 1 (same-dataset trials are consecutive in harbor's attempt-major queue and collide on the shared global pg volume)

### `analysis`

All 5 draws are complete and the numbers are being extracted and audited. This is the
approval gate: the captain reviews the audited numbers before they go public. Rejection
(e.g., a tainted draw) bounces back to `execution` to re-run the affected draws.

- **Inputs:** The run dir (5 trials; backfills may span multiple run dirs); `dab/docs/benchmark-artifact/extract_benchmark_data.py`; the taint-audit checklist below
- **Outputs:** Per-draw stratified pass@1 table + mean/sd/min/max in the entity body; `pass-at-1`, `pass-at-1-sd`, `tokens-total`, `mean-session-sec` filled in frontmatter; a taint-audit section stating what was checked and what was found (clean is a finding too); comparison against the previous regression row (delta + whether it exceeds the ±0.03 five-draw noise band)
- **Good:** Tokens measured from harbor `sessions/` rollouts via the extractor (codex stdout undercounts ~5×); taint audit run BEFORE trusting any number — grep `reward_per_query` for "validator error" (the ~1-in-5 dab0022 list-answer crash scores a dataset 0), check for the postgres-degradation dual signature (whole-dataset `coverage_missing` + mid-run Connection-refused abstains), check dataset coverage is complete; a low draw is called tainted only WITH evidence, variance only WITHOUT
- **Bad:** Quoting a mean before the taint audit; calling any single-draw delta a regression (the 5-draw mean itself wobbles ±0.03); comparing across rows without noting harness-version and README-lever differences; recomputing tokens from codex stdout

### `published`

The audited numbers are approved and being added to the regression Artifacts page.

- **Inputs:** The gate-approved entity; `dab/docs/benchmark-artifact/dab-regression.html` (or the template on first publish); the live artifact URL from this README
- **Outputs:** The run's row added to the page (pass@1 mean±sd with per-draw whiskers, tokens, mean session time, spacedock version, model, date, caveats); page re-published to the SAME artifact URL; `artifact-url` set in frontmatter; page source committed
- **Good:** The page stays a longitudinal table/chart over runs — every historical row preserved; caveats travel with their row (e.g., the v0.22 baseline carries its CAIS-import + substitution notes); same file path → same URL on every re-publish
- **Bad:** Minting a new artifact URL (breaks the "one page, updated in place" contract); dropping or restating old rows; publishing numbers that differ from the gate-approved entity

### `done`

Terminal state. The run is recorded on the page and locked.

- **Inputs:** The published entity
- **Outputs:** None — set `completed`, `verdict: PASSED`, done
- **Good:** Entity is a complete, self-contained record a future reader can audit (draws, numbers, taint findings, page URL)
- **Bad:** Reopening a done run to "fix" its numbers — a correction is a new entity referencing the old one

## Workflow State

Workflow state is read by the first officer at boot. To view current state, dispatch the
first officer or run it directly:

```
spacedock claude
```

## Run Template

```yaml
---
id:
title: gpt-5.5 @ high — spacedock vX.Y
status: queued
source:
started:
completed:
verdict:
score:
worktree:
issue:
pr:
trigger:
model: gpt-5.5
effort: high
spacedock-version:
draws: []
pass-at-1:
pass-at-1-sd:
tokens-total:
mean-session-sec:
artifact-url:
---

Brief description: what triggered this run and what it measures.

## Acceptance criteria

**AC-1 — Five clean (or disclosed-substitution) full draws exist under `dab/runs/`.**
Verified by: the 5 entries in `draws` each resolve to a completed trial in the run dir.

**AC-2 — pass@1, tokens, and timing in frontmatter match the extractor output.**
Verified by: re-running `extract_benchmark_data.py` over the 5 run dirs.

**AC-3 — The run's row is live on the regression Artifacts page at the recorded URL.**
Verified by: `artifact-url` set; row visible with matching numbers.

## Draws

| draw | experiment | stratified pass@1 | notes |
|------|-----------|-------------------|-------|

## Taint audit

## Publication
```

## Commit Discipline

- Commit status changes at dispatch and merge boundaries
- Commit run body updates when substantive (draw completion, analysis numbers, publication)
