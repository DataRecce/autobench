#!/usr/bin/env bash
# ABOUTME: Master xhigh sweep — 20 boards, strict FOREGROUND sequence (no same-dataset postgres
# ABOUTME: collision; dab0018 scar). Phase 1: gpt-5.5 spacedock BASELINE xhigh × 5 (sx, clean rk
# ABOUTME: re-run of the 35%-censored CAIS spacedock·xhigh). Phase 2 (only after Phase 1): gpt-5.6-sol
# ABOUTME: xhigh × 5 each for minimal / structured / dab0022, interleaved by round. Appends to $MANIFEST.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."   # dab/
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
export RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock

MANIFEST="runs/.xhigh-55sx-56trio-manifest.txt"; : > "$MANIFEST"

# Phase 1 — gpt-5.5 spacedock baseline xhigh (5 draws)
PHASE1=( codex-dab-sx-d1 codex-dab-sx-d2 codex-dab-sx-d3 codex-dab-sx-d4 codex-dab-sx-d5 )

# Phase 2 — gpt-5.6-sol xhigh trio, interleaved by round (dab0022 / minimal / structured)
PHASE2=(
  codex-dab-d22x-g56sol-d1 codex-dab-dmx-g56sol-d1 codex-dab-dsx-g56sol-d1
  codex-dab-d22x-g56sol-d2 codex-dab-dmx-g56sol-d2 codex-dab-dsx-g56sol-d2
  codex-dab-d22x-g56sol-d3 codex-dab-dmx-g56sol-d3 codex-dab-dsx-g56sol-d3
  codex-dab-d22x-g56sol-d4 codex-dab-dmx-g56sol-d4 codex-dab-dsx-g56sol-d4
  codex-dab-d22x-g56sol-d5 codex-dab-dmx-g56sol-d5 codex-dab-dsx-g56sol-d5
)

run_board () {
  local exp="$1"
  echo "=== [$(date -Is)] START $exp ==="
  uv run --project ../razorback rk run "specs/${exp}.frozen.yaml" --runs-dir runs
  local rc=$?
  local rundir; rundir="$(ls -dt runs/${exp}/*/ 2>/dev/null | head -1)"; rundir="${rundir%/}"
  local strat=""
  [[ -n "$rundir" && -f "$rundir/summary.json" ]] && \
    strat="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["stratified_pass_at_1"])' "$rundir/summary.json" 2>/dev/null)"
  echo "${exp} rc=${rc} rundir=${rundir} stratified=${strat}" >> "$MANIFEST"
  echo "=== [$(date -Is)] DONE  $exp rc=$rc strat=$strat ==="
}

echo "########## PHASE 1: gpt-5.5 spacedock baseline xhigh (5 boards) [$(date -Is)] ##########"
for exp in "${PHASE1[@]}"; do run_board "$exp"; done
echo "########## PHASE 1 COMPLETE [$(date -Is)] — starting Phase 2 ##########"

echo "########## PHASE 2: gpt-5.6-sol xhigh trio (15 boards) [$(date -Is)] ##########"
for exp in "${PHASE2[@]}"; do run_board "$exp"; done

echo "=== ALL 20 COMPLETE [$(date -Is)] ==="; cat "$MANIFEST"
