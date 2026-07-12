#!/usr/bin/env bash
# ABOUTME: Sequential 8-board variance chain — direct-minimal x4 then direct-structured x4.
# ABOUTME: Runs each board FOREGROUND in strict sequence so no two boards ever overlap
# ABOUTME: (guarantees no same-dataset postgres-volume collision; dab0018 scar). Appends a
# ABOUTME: per-draw line {label rc rundir stratified} to $MANIFEST as each board finishes.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."   # dab/
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
export RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock

MANIFEST="runs/.variance8-manifest.txt"
: > "$MANIFEST"

SPECS=(
  codex-dab-dm-d1 codex-dab-dm-d2 codex-dab-dm-d3 codex-dab-dm-d4
  codex-dab-ds-d1 codex-dab-ds-d2 codex-dab-ds-d3 codex-dab-ds-d4
)

for exp in "${SPECS[@]}"; do
  spec="specs/${exp}.frozen.yaml"
  echo "=== [$(date -Is)] START $exp ==="
  uv run --project ../razorback rk run "$spec" --runs-dir runs
  rc=$?
  rundir="$(ls -dt runs/${exp}/*/ 2>/dev/null | head -1)"; rundir="${rundir%/}"
  strat=""
  if [[ -n "$rundir" && -f "$rundir/summary.json" ]]; then
    strat="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["stratified_pass_at_1"])' "$rundir/summary.json" 2>/dev/null)"
  fi
  echo "${exp} rc=${rc} rundir=${rundir} stratified=${strat}" >> "$MANIFEST"
  echo "=== [$(date -Is)] DONE  $exp rc=$rc strat=$strat ==="
done

echo "=== ALL 8 COMPLETE [$(date -Is)] ==="
cat "$MANIFEST"
