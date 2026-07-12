#!/usr/bin/env bash
# ABOUTME: Sequential 5-board REPLICATION — dab0022 README @ spacedock/gpt-5.5/XHIGH/batch, CONCURRENCY 4.
# ABOUTME: Independent replication of the d22x run (concurrency 2, mean 0.6899) to firm up the -0.053
# ABOUTME: "xhigh hurts dab0022" finding; pools to 10 draws. Boards run FOREGROUND in strict sequence so no
# ABOUTME: two overlap (no same-dataset postgres collision); within a board concurrency 4 = 4 DISTINCT datasets.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."   # dab/
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
export RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock

MANIFEST="runs/.variance-d22x4-manifest.txt"
: > "$MANIFEST"
SPECS=( codex-dab-d22x4-d1 codex-dab-d22x4-d2 codex-dab-d22x4-d3 codex-dab-d22x4-d4 codex-dab-d22x4-d5 )

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
echo "=== ALL 5 COMPLETE [$(date -Is)] ==="
cat "$MANIFEST"
