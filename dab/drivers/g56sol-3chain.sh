#!/usr/bin/env bash
# ABOUTME: Sequential 3-board gpt-5.6-sol @ high sweep — dab0022(spacedock) + minimal + structured, batch.
# ABOUTME: Boards run FOREGROUND in strict sequence (no same-dataset postgres collision; within a board
# ABOUTME: concurrency 4 = 4 distinct datasets). Appends {label rc rundir stratified} to $MANIFEST.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
export RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock
MANIFEST="runs/.g56sol-3-manifest.txt"; : > "$MANIFEST"
SPECS=( codex-dab-d22-g56sol-h2 codex-dab-dm-g56sol-h1 codex-dab-ds-g56sol-h1 )
for exp in "${SPECS[@]}"; do
  echo "=== [$(date -Is)] START $exp ==="
  uv run --project ../razorback rk run "specs/${exp}.frozen.yaml" --runs-dir runs
  rc=$?
  rundir="$(ls -dt runs/${exp}/*/ 2>/dev/null | head -1)"; rundir="${rundir%/}"
  strat=""; [[ -n "$rundir" && -f "$rundir/summary.json" ]] && strat="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["stratified_pass_at_1"])' "$rundir/summary.json" 2>/dev/null)"
  echo "${exp} rc=${rc} rundir=${rundir} stratified=${strat}" >> "$MANIFEST"
  echo "=== [$(date -Is)] DONE  $exp rc=$rc strat=$strat ==="
done
echo "=== ALL 3 COMPLETE [$(date -Is)] ==="; cat "$MANIFEST"
