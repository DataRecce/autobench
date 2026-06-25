#!/usr/bin/env bash
# ABOUTME: Detached launcher for long rk runs — nohup + atomic completion sentinel + ntfy push.
# ABOUTME: smoke/full call this so the run survives Claude-Code's process/turn cap (30min-7hr+).
#
# Design (mirrors ade-bench/spider2-dbt drivers/rk-run-detached.sh + memory note rk-run-detached-nohup):
#   - The launcher returns the handle immediately; it never waits (a multi-hour wait cannot be
#     owned by a synchronous subagent).
#   - The SENTINEL ($HANDLE/done) is the source of truth — never a live process. Scan
#     runs/.rk-handles/*/ at the top of EVERY turn and re-attach. No live poller / no Monitor.
#   - The nohup'd worker fires an ntfy push on completion — autonomous notification independent
#     of whether the agent is awake.
#
# Usage (run from swe/):
#   drivers/rk-run-detached.sh <key> <spec> [run|cmd] [-- <extra args>]
#     <key>    handle key, e.g. smoke1   (handle dir: runs/.rk-handles/<key>-<ts>/)
#     <spec>   frozen spec path, e.g. specs/smoke1.frozen.yaml
#     run      (default) bare: rk run <spec> --runs-dir runs [extra]
#     cmd      run an arbitrary command given after --   (e.g. for tests)
#
# Handle dir contents (read these; all under the always-gitignored runs/):
#   meta   key/spec/mode/experiment/start/ntfy_*   (provenance)
#   cmd    the exact %q-quoted command the worker runs
#   pid    worker PID — alive => running OR writing sentinel; dead + no `done` => crashed
#   log    combined stdout+stderr of the run
#   done   TERMINAL sentinel (atomic same-fs rename): rc=<n> end=<iso> rundir=<path>
#          ABSENT until finished. rc=0 => OK; rc!=0 => failed.
#
# Completion authority on a pid-dead + no-`done` race (worker killed after rk finished but before
# the sentinel write): check harbor's own run-dir artifacts (<rundir>/<cell>/result.json, or
# summary.json/per_trial_outcomes.json) BEFORE declaring "crashed".
#
# ntfy topic resolution: $NTFY_TOPIC, else swe/.ntfy-topic (gitignored). Base: $NTFY_BASE
# or https://ntfy.sh. The push carries only "<key>: OK|FAIL" — no paths/secrets.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCH_DIR="$(dirname "$SCRIPT_DIR")"

# ---------------------------------------------------------------------------
# Internal worker mode — re-invoked under nohup. Owns the run, the sentinel, the ntfy push.
# NOT `-e`: a nonzero rc from the wrapped command must be captured, not abort the worker.
# ---------------------------------------------------------------------------
if [[ "${1:-}" == "__worker" ]]; then
  set -uo pipefail
  HANDLE_DIR="$2"
  cd "$BENCH_DIR"
  echo $$ > "$HANDLE_DIR/pid"   # authoritative worker PID (overwrites the launcher's best-effort)

  meta_get() { sed -n "s/^$1=//p" "$HANDLE_DIR/meta" 2>/dev/null; }
  KEY="$(meta_get key)"
  EXPERIMENT="$(meta_get experiment)"
  NTFY_TOPIC="$(meta_get ntfy_topic)"
  NTFY_BASE="$(meta_get ntfy_base)"
  CMD_Q="$(cat "$HANDLE_DIR/cmd")"

  eval "$CMD_Q" > "$HANDLE_DIR/log" 2>&1
  rc=$?                          # captured IMMEDIATELY — before any other command clobbers $?

  rundir=""
  if [[ -n "$EXPERIMENT" ]]; then
    rundir="$(ls -dt "runs/$EXPERIMENT"/*/ 2>/dev/null | head -1)"
    rundir="${rundir%/}"
  fi

  # Atomic, same-filesystem publish (handle dir lives under runs/ on the same fs as done.tmp).
  { echo "rc=$rc"; echo "end=$(date -Is)"; echo "rundir=$rundir"; } > "$HANDLE_DIR/done.tmp"
  mv -f "$HANDLE_DIR/done.tmp" "$HANDLE_DIR/done"

  if [[ -n "$NTFY_TOPIC" ]]; then
    if [[ "$rc" -eq 0 ]]; then tag="white_check_mark"; verdict="OK"; else tag="x"; verdict="FAIL rc=$rc"; fi
    curl -s --max-time 15 \
      -H "Title: swe ${KEY}" \
      -H "Tags: ${tag}" \
      -d "swe ${KEY}: ${verdict}" \
      "${NTFY_BASE%/}/${NTFY_TOPIC}" >/dev/null 2>&1 || true
  fi
  exit 0
fi

# ---------------------------------------------------------------------------
# Launcher mode
# ---------------------------------------------------------------------------
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage (run from swe/): drivers/rk-run-detached.sh <key> <spec> [run|cmd] [-- <extra>]
  <key>   handle key, e.g. smoke1   (handle: runs/.rk-handles/<key>-<ts>/)
  <spec>  frozen spec path (run); "-" allowed in cmd mode
  run     (default)  uv run --project ../razorback rk run <spec> --runs-dir runs [extra]
  cmd                run an arbitrary command given after --   (e.g. for tests)
Detaches via nohup; writes runs/.rk-handles/<key>-<ts>/{meta,cmd,pid,log,done}; ntfy on done.
EOF
}

[[ $# -ge 2 ]] || { echo "error: need <key> <spec>" >&2; usage >&2; exit 2; }
KEY="$1"; SPEC="$2"; MODE="${3:-run}"
if [[ $# -ge 3 ]]; then shift 3; else shift 2; fi
[[ "${1:-}" == "--" ]] && shift || true
EXTRA=( "$@" )

case "$MODE" in run|cmd) ;; *) echo "error: bad mode '$MODE' (expected run|cmd)" >&2; exit 2;; esac

cd "$BENCH_DIR"
# run launches from a frozen spec; cmd wraps an arbitrary command (spec may be "-").
if [[ "$MODE" != "cmd" ]]; then
  [[ -f "$SPEC" ]] || { echo "error: spec not found: $SPEC (paths are relative to swe/)" >&2; exit 2; }
fi
export RAZORBACK_SPACEDOCK_PLUGIN_DIR="${RAZORBACK_SPACEDOCK_PLUGIN_DIR:-$(git rev-parse --show-toplevel)/spacedock}"

# Experiment name → run-dir resolution after completion. Best-effort.
EXPERIMENT=""
if [[ -f "$SPEC" ]]; then
  EXPERIMENT="$(python3 -c 'import yaml,sys; print(yaml.safe_load(open(sys.argv[1]))["experiment"])' "$SPEC" 2>/dev/null \
             || python -c 'import yaml,sys; print(yaml.safe_load(open(sys.argv[1]))["experiment"])' "$SPEC" 2>/dev/null \
             || true)"
fi

NTFY_TOPIC="${NTFY_TOPIC:-}"
if [[ -z "$NTFY_TOPIC" && -f .ntfy-topic ]]; then NTFY_TOPIC="$(tr -d '[:space:]' < .ntfy-topic)"; fi
NTFY_BASE="${NTFY_BASE:-https://ntfy.sh}"

case "$MODE" in
  run)  CMD=( uv run --project ../razorback rk run "$SPEC" --runs-dir runs "${EXTRA[@]}" );;
  cmd)  [[ ${#EXTRA[@]} -ge 1 ]] || { echo "error: cmd mode needs a command after --" >&2; exit 2; }
        CMD=( "${EXTRA[@]}" );;
esac

TS="$(date +%Y%m%d-%H%M%S)"
HANDLE_DIR="runs/.rk-handles/${KEY}-${TS}"
mkdir -p "$HANDLE_DIR"

printf '%q ' "${CMD[@]}" > "$HANDLE_DIR/cmd"
{
  echo "key=$KEY"
  echo "spec=$SPEC"
  echo "mode=$MODE"
  echo "experiment=$EXPERIMENT"
  echo "start=$(date -Is)"
  echo "ntfy_topic=$NTFY_TOPIC"
  echo "ntfy_base=$NTFY_BASE"
} > "$HANDLE_DIR/meta"

# Launch detached. nohup execs into bash (PID stable), so $! is the worker; the worker also
# rewrites pid with $$ as its first act, so the pidfile is authoritative either way.
nohup bash "${BASH_SOURCE[0]}" __worker "$HANDLE_DIR" >/dev/null 2>&1 &
echo $! > "$HANDLE_DIR/pid"

cat <<EOF
launched: ${KEY}  (mode=${MODE})
handle:   ${HANDLE_DIR}
pid:      $(cat "$HANDLE_DIR/pid")
log:      ${HANDLE_DIR}/log       (tail -f to watch progress)
done:     ${HANDLE_DIR}/done      (absent until finished; then rc/end/rundir)
ntfy:     ${NTFY_TOPIC:-<none configured — set swe/.ntfy-topic or \$NTFY_TOPIC>}
EOF
