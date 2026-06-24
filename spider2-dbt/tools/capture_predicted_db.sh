#!/usr/bin/env bash
# ABOUTME: Poll a live spider2-dbt task container and docker-cp its built /app/<db>.duckdb
# ABOUTME: to a host file; the last copy before teardown = the agent's final predicted DB.
# Usage: capture_predicted_db.sh <container-name-filter> <db-basename> <out-file> <done-sentinel>
set -uo pipefail
FILTER="$1"; DB="$2"; OUT="$3"; DONE="$4"
mkdir -p "$(dirname "$OUT")"
copies=0
while true; do
  cid="$(docker ps --filter "name=${FILTER}" --format '{{.ID}}' 2>/dev/null | head -1)"
  if [ -n "$cid" ]; then
    if docker cp "${cid}:/app/${DB}.duckdb" "${OUT}.tmp" 2>/dev/null; then
      mv -f "${OUT}.tmp" "$OUT"; copies=$((copies+1))
    fi
  fi
  # stop once the run is done AND the container is gone (final copy already taken)
  if [ -f "$DONE" ] && [ -z "$cid" ]; then break; fi
  sleep 5
done
echo "captured=$copies out=$OUT exists=$([ -f "$OUT" ] && echo yes || echo no)"
