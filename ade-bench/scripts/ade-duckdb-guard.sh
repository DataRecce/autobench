#!/usr/bin/env bash
# ade-duckdb-guard.sh — detect & fix the "wrong DuckDB shipped in ade-bench images" issue.
#
# ROOT CAUSE (verified): BuildKit keys the `COPY db_file_id.txt` layer on
# (path + size + MTIME), NOT content. Every task's db_file_id.txt has the same
# epoch mtime (from harbor materialization) and ~same size, so BuildKit reuses ONE
# cached COPY layer across ALL tasks -> the `gdown` step fetches whichever Drive id
# was cached first -> every image gets the same (wrong) dataset. The harness builds
# its per-trial `ade-bench-<task>__<id>-main` images via BuildKit and reuses them
# (force_build=false), so the contamination sticks.
#
# FIX: give each db_file_id.txt a UNIQUE mtime (content unchanged -> pinned dataset
# hash unaffected) so BuildKit's COPY keys diverge; purge the poisoned cache; remove
# contaminated images so the harness rebuilds clean. NOTE: do NOT rely on the legacy
# builder (DOCKER_BUILDKIT=0) as the fix — the harness uses BuildKit, so the mtime fix
# is what actually makes the harness's own builds correct.
#
# Usage:
#   ./ade-duckdb-guard.sh verify   # read-only: dataset mtimes + positive per-image check
#   ./ade-duckdb-guard.sh fix      # mtimes + purge + remove images + rebuild + verify
set -uo pipefail

DSROOT="${ADE_DATASET_ROOT:-$HOME/.cache/razorback/harbor/datasets}"

# Positive per-family check (run inside each image; each image ships duckdb).
read -r -d '' PYCHECK <<'PY'
import duckdb, glob, sys
task = sys.argv[1]
fam_sent = {
 'airbnb':     {'raw_hosts','raw_listings','raw_reviews'},
 'ana-eng':    {'suppliers','invoices','inventory_transactions','customer'},
 'asana':      {'task_data','project_data'},
 'f1':         {'circuits','drivers','races'},
 'intercom':   {'admin_data','conversation_history_data'},
 'quickbooks': {'account_data','bill_data'},
}
fam = next((f for f in ('ana-eng','airbnb','asana','f1','intercom','quickbooks')
            if task.startswith(f)), None)
ps = glob.glob('/app/*.duckdb')
if not ps:
    print(f"{task}|NO_DUCKDB|{fam}"); sys.exit()
try:
    c = duckdb.connect(ps[0], read_only=True)
    ts = {r[1].lower() for r in c.execute(
        "select table_schema,table_name from information_schema.tables").fetchall()}
except Exception as e:
    print(f"{task}|DBERR|{fam}|{e}"); sys.exit()
exp = fam_sent.get(fam, set())
present = exp & ts
foreign = sorted(of for of, se in fam_sent.items() if of != fam and (se & ts))
ok = bool(present) and not foreign
print(f"{task}|{'OK' if ok else 'WRONG'}|fam={fam}|has_own={sorted(present)}|foreign={foreign}")
PY

task_of() { basename "$1" | sed -E 's/^ade-bench-//'; }

set_unique_mtimes() {
  echo "== assigning unique mtimes to db_file_id.txt/db_name.txt (defeats BuildKit COPY collision) =="
  local i=0
  for d in "$DSROOT"/ade-bench-*/; do
    local env="$d/environment"; [ -d "$env" ] || continue
    i=$((i+1))
    local ts=$((1577836800 + i*60))   # 2020-01-01 + i minutes; unique & stable per task
    [ -f "$env/db_file_id.txt" ] && touch -d "@$ts" "$env/db_file_id.txt"
    [ -f "$env/db_name.txt" ]    && touch -d "@$ts" "$env/db_name.txt"
  done
  echo "   set on $i tasks"
}

verify_images() {
  echo "== positive per-family image check =="
  local bad=0 n=0
  for img in $(docker images --format '{{.Repository}}:{{.Tag}}' \
               | grep -E '^(hb__dbt-labs-ade-bench-|ade-bench-)' | sort -u); do
    n=$((n+1))
    local task; task=$(echo "$img" | sed -E 's#^hb__dbt-labs-ade-bench-##; s#^ade-bench-##; s/__.*//; s/:.*//')
    local out; out=$(docker run --rm -i "$img" python /dev/stdin "$task" <<<"$PYCHECK" 2>/dev/null)
    echo "  $out"
    [[ "$out" == *"|OK|"* ]] || bad=$((bad+1))
  done
  echo "  images=$n wrong=$bad"
  [[ $bad -eq 0 ]]
}

do_verify() {
  echo "== dataset db_file_id.txt mtime uniqueness =="
  local total uniq
  total=$(ls "$DSROOT"/ade-bench-*/environment/db_file_id.txt 2>/dev/null | wc -l)
  uniq=$(stat -c '%Y' "$DSROOT"/ade-bench-*/environment/db_file_id.txt 2>/dev/null | sort -u | wc -l)
  echo "  $uniq distinct mtimes across $total files $([ "$uniq" -ge "$total" ] && echo OK || echo '<-- COLLISION RISK (run fix)')"
  verify_images
}

do_fix() {
  echo "### FIX (BuildKit-mtime approach)"
  set_unique_mtimes
  echo "== purging BuildKit cache =="
  docker builder prune -af >/dev/null 2>&1
  echo "== removing all contaminated ade-bench task images =="
  docker images --format '{{.Repository}}:{{.Tag}}' \
    | grep -E '^(hb__dbt-labs-ade-bench-|ade-bench-.*__.*-main)' \
    | xargs -r docker rmi -f >/dev/null 2>&1
  echo "== rebuilding all tasks via default BuildKit (collision-free) + verifying =="
  local bad=0 i=0
  mapfile -t dirs < <(ls -d "$DSROOT"/ade-bench-*/ 2>/dev/null | sort)
  for d in "${dirs[@]}"; do
    i=$((i+1)); local task; task=$(task_of "$d"); local env="$d/environment"
    [ -f "$env/Dockerfile" ] || { echo "  SKIP $task"; continue; }
    local tag="hb__dbt-labs-ade-bench-$task"
    if DOCKER_BUILDKIT=1 docker build -q -t "$tag" "$env" >/tmp/ade-fix-"$task".log 2>&1; then
      local out; out=$(docker run --rm -i "$tag" python /dev/stdin "$task" <<<"$PYCHECK" 2>/dev/null)
      [[ "$out" == *"|OK|"* ]] || bad=$((bad+1))
      printf '  [%2d/%2d] %s\n' "$i" "${#dirs[@]}" "$out"
    else
      bad=$((bad+1)); printf '  [%2d/%2d] %-26s BUILD-FAILED (see /tmp/ade-fix-%s.log)\n' "$i" "${#dirs[@]}" "$task" "$task"
    fi
  done
  echo "== done; wrong/failed=$bad =="
  echo "Now: remove stale per-trial images are already gone; trigger the baseline run."
  [[ $bad -eq 0 ]]
}

case "${1:-verify}" in
  verify) do_verify ;;
  fix)    do_fix ;;
  *) echo "usage: $0 {verify|fix}"; exit 1 ;;
esac
