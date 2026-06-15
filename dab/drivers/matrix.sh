#!/usr/bin/env bash
# ABOUTME: Per-cell matrix dispatcher for the DAB research repo: rk run + audit + score.
# ABOUTME: No subagent-trace smoke gate (DAB gates worthiness at the smoke stage instead).
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: matrix.sh [--output-dir <path>] [--specs <pattern>] [--dry-run] [--continue-on-fail]
  --output-dir        Base runs-dir (default: runs)
  --specs             Glob of frozen spec files (default: specs/*.frozen.yaml)
  --dry-run           Print the plan, do not dispatch.
  --continue-on-fail  Do not exit on first cell failure; record and continue.
Per-cell: rk run -> rk audit --policy strict (audit.json) -> rk score (score.json) -> ledger row.
EOF
}

OUTPUT_DIR="runs"; SPECS_GLOB="specs/*.frozen.yaml"; DRY_RUN=0; CONTINUE_ON_FAIL=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir) OUTPUT_DIR="$2"; shift 2;;
    --specs) SPECS_GLOB="$2"; shift 2;;
    --dry-run) DRY_RUN=1; shift;;
    --continue-on-fail) CONTINUE_ON_FAIL=1; shift;;
    -h|--help) usage; exit 0;;
    *) echo "unknown flag: $1" >&2; usage; exit 2;;
  esac
done

mkdir -p "$OUTPUT_DIR"
LEDGER="$OUTPUT_DIR/ledger.tsv"
[[ -f "$LEDGER" ]] || printf 'spec\tstatus\trun_dir\ttaint_count\n' > "$LEDGER"
ok_cells=0; failed_cells=0

for spec in $SPECS_GLOB; do
  [[ -f "$spec" ]] || continue
  echo "== dispatching $spec =="
  if (( DRY_RUN )); then echo "  [dry-run] would rk run + audit + score"; continue; fi

  rc=0
  uv run --project ../razorback rk run "$spec" --runs-dir "$OUTPUT_DIR" || rc=$?
  experiment=$(python3 -c "import yaml; print(yaml.safe_load(open('$spec'))['experiment'])")
  cell_run_dir=$(ls -dt "$OUTPUT_DIR/$experiment"/*/ 2>/dev/null | head -1); cell_run_dir="${cell_run_dir%/}"
  status="ok"; taint_count=0

  if (( rc != 0 )); then
    status="run_failed"; failed_cells=$((failed_cells+1))
    printf '%s\t%s\t%s\t%s\n' "$spec" "$status" "$cell_run_dir" "$taint_count" >> "$LEDGER"
    (( CONTINUE_ON_FAIL )) || { echo "FAIL $spec exit=$rc — stopping" >&2; exit 4; }
    continue
  fi

  audit_rc=0
  uv run --project ../razorback rk audit "$cell_run_dir" --policy strict --format json \
    > "$cell_run_dir/audit.json" 2> "$cell_run_dir/audit.stderr" || audit_rc=$?
  if (( audit_rc != 0 )); then
    status="audit_tainted"
    taint_count=$(python3 -c "import json; r=json.load(open('$cell_run_dir/audit.json')); print(sum(1 for t in r.get('trials',[]) if t.get('status')!='clean'))" 2>/dev/null || echo 1)
    failed_cells=$((failed_cells+1))
    printf '%s\t%s\t%s\t%s\n' "$spec" "$status" "$cell_run_dir" "$taint_count" >> "$LEDGER"
    (( CONTINUE_ON_FAIL )) || { echo "AUDIT FAIL $spec — see $cell_run_dir/audit.json" >&2; exit 4; }
    continue
  fi

  uv run --project ../razorback rk score "$cell_run_dir" --format json \
    > "$cell_run_dir/score.json" 2> "$cell_run_dir/score.stderr" || true
  ok_cells=$((ok_cells+1))
  printf '%s\t%s\t%s\t%s\n' "$spec" "$status" "$cell_run_dir" "$taint_count" >> "$LEDGER"
done

echo ""; echo "Matrix done: ok=$ok_cells failed=$failed_cells"
(( failed_cells == 0 )) || exit 5
