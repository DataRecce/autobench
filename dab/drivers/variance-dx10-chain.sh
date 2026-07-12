#!/usr/bin/env bash
# ABOUTME: Sequential 10-board XHIGH sweep — direct-minimal x5 then direct-structured x5, gpt-5.5 xhigh, batch.
# ABOUTME: GATED: first blocks until the spacedock-xhigh chain's done-sentinel appears, so it never overlaps
# ABOUTME: that run (no same-dataset postgres collision; dab0018 scar). Then runs each board FOREGROUND in
# ABOUTME: strict sequence. Appends {label rc rundir stratified} to $MANIFEST as each board finishes.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."   # dab/
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
export RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock

GATE_DONE="runs/.rk-handles/d22x5-20260704-074631/done"
MANIFEST="runs/.variance-dx10-manifest.txt"

echo "=== [$(date -Is)] GATE: waiting for spacedock-xhigh chain to finish ($GATE_DONE) ==="
while [[ ! -f "$GATE_DONE" ]]; do sleep 120; done
echo "=== [$(date -Is)] GATE released — spacedock chain done, starting xhigh direct sweep ==="

: > "$MANIFEST"
SPECS=(
  codex-dab-dmx-d1 codex-dab-dmx-d2 codex-dab-dmx-d3 codex-dab-dmx-d4 codex-dab-dmx-d5
  codex-dab-dsx-d1 codex-dab-dsx-d2 codex-dab-dsx-d3 codex-dab-dsx-d4 codex-dab-dsx-d5
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

echo "=== ALL 10 COMPLETE [$(date -Is)] ==="
cat "$MANIFEST"
