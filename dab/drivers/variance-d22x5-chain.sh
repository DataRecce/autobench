#!/usr/bin/env bash
# ABOUTME: Sequential 5-board variance chain — spacedock variant, gpt-5.5, reasoning_effort=XHIGH, batch.
# ABOUTME: Runs each board FOREGROUND in strict sequence so no two overlap (no same-dataset postgres
# ABOUTME: collision; dab0018 scar). Uses the LATEST baseline solver_workflow spacedock-readme-baseline-hostfix
# ABOUTME: (content-identical to @codex-batch-baseline). Appends {label rc rundir stratified} to $MANIFEST.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."   # dab/
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
export RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock

MANIFEST="runs/.variance-d22x5-manifest.txt"
: > "$MANIFEST"

SPECS=( codex-dab-d22x-d1 codex-dab-d22x-d2 codex-dab-d22x-d3 codex-dab-d22x-d4 codex-dab-d22x-d5 )

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
