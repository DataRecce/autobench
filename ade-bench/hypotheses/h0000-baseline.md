---
id: h0000
title: Baseline — codex ade-dbt-repair solver, full 48 tasks
status: analyze
kind: hypothesis
source: setup
started: 2026-06-01T16:34:03Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Establish the anchor: the baseline codex solver README on all 48 ade-bench tasks. No
README change — this run defines `@baseline` and the 9/48 (0.1875) reference. Skips
smoke (`propose → full`).

## Run result

_Pending the live baseline full run (deferred). To execute — see Task 9 of
`docs/superpowers/plans/2026-06-01-autobench-setup.md`. In short, from repo root:_

```bash
export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(pwd)/spacedock"   # Docker must be running; codex auth configured
cd ade-bench
uv run --project ../razorback rk run specs/baseline.frozen.yaml --explain          # $0 pre-flight
uv run --project ../razorback rk run specs/baseline.frozen.yaml --runs-dir runs     # full 48 tasks
BASELINE_RUN=$(ls -dt runs/ade-bench-baseline/*/ | head -1)
uv run --project ../razorback rk audit "$BASELINE_RUN" --policy strict
uv run --project ../razorback rk score "$BASELINE_RUN" --format json                # expect ~9/48 = 0.1875
uv run --project ../razorback rk baseline promote "$BASELINE_RUN"
uv run --project ../razorback rk registry add run baseline "$BASELINE_RUN"
```

_Then paste the `score.json` headline here, set `status: conclude` / `completed:` /
`verdict: PASSED` / `score:`, and write the Verdict below._

## Behavioral analysis

_Filled after the run — which task groups (airbnb / ana-eng / asana / f1 / intercom /
quickbooks) passed vs failed, and the distance-to-pass on notable failures._

## Verdict

_Filled after the run._
