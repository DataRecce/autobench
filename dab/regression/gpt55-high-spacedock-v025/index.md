---
id:
title: gpt-5.5 @ high — spacedock v0.25 (spacedock release)
status: analysis
source: spacedock v0.25.0 release (captain-filed 2026-07-16)
started: 2026-07-16T16:20:11Z
completed:
verdict:
score:
worktree:
issue:
pr:
trigger: spacedock-release
model: gpt-5.5
effort: high
spacedock-version: v0.25.0 (601c3f53)
draws: []
pass-at-1:
pass-at-1-sd:
tokens-total:
mean-session-sec:
artifact-url:
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

| draw | experiment | stratified pass@1 | notes |
|------|-----------|-------------------|-------|

## Taint audit

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
