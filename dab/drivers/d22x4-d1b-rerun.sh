#!/usr/bin/env bash
# ABOUTME: Gated re-run of the canary-lost d22x4 draw. Waits for the main d22x4 chain done-sentinel,
# ABOUTME: then runs d1b once (no overlap with the running boards). Appends to the same manifest.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
export RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock
GATE="runs/.rk-handles/d22x4-20260706-024555/done"
echo "=== [$(date -Is)] d1b GATE: waiting for main d22x4 chain ==="
while [[ ! -f "$GATE" ]]; do sleep 120; done
echo "=== [$(date -Is)] d1b GATE released — running replacement draw ==="
uv run --project ../razorback rk run specs/codex-dab-d22x4-d1b.frozen.yaml --runs-dir runs
rc=$?
rundir="$(ls -dt runs/codex-dab-d22x4-d1b/*/ 2>/dev/null | head -1)"; rundir="${rundir%/}"
strat=""; [[ -n "$rundir" && -f "$rundir/summary.json" ]] && strat="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["stratified_pass_at_1"])' "$rundir/summary.json" 2>/dev/null)"
echo "codex-dab-d22x4-d1b rc=${rc} rundir=${rundir} stratified=${strat}" >> runs/.variance-d22x4-manifest.txt
echo "=== [$(date -Is)] d1b DONE rc=$rc strat=$strat ==="
