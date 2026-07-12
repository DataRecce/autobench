#!/usr/bin/env bash
# ABOUTME: Clean rerun — gpt-5.5 dab0022 xhigh, 5 draws, uncapped, conc4, spacedock v0.24.
# ABOUTME: Replaces the (captain-flagged) timeout-suspect dab0022 xhigh cell on the 5.5 result page.
# ABOUTME: Strict FOREGROUND sequence (no same-dataset postgres collision). Appends to $MANIFEST.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
export RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock
MANIFEST="runs/.d22xr-rerun-manifest.txt"; : > "$MANIFEST"
SPECS=( codex-dab-d22xr-d1 codex-dab-d22xr-d2 codex-dab-d22xr-d3 codex-dab-d22xr-d4 codex-dab-d22xr-d5 )
for exp in "${SPECS[@]}"; do
  echo "=== [$(date -Is)] START $exp ==="
  uv run --project ../razorback rk run "specs/${exp}.frozen.yaml" --runs-dir runs
  rc=$?
  rundir="$(ls -dt runs/${exp}/*/ 2>/dev/null | head -1)"; rundir="${rundir%/}"
  strat=""; [[ -n "$rundir" && -f "$rundir/summary.json" ]] && strat="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["stratified_pass_at_1"])' "$rundir/summary.json" 2>/dev/null)"
  echo "${exp} rc=${rc} rundir=${rundir} stratified=${strat}" >> "$MANIFEST"
  echo "=== [$(date -Is)] DONE  $exp rc=$rc strat=$strat ==="
done
echo "=== ALL 5 COMPLETE [$(date -Is)] ==="; cat "$MANIFEST"
