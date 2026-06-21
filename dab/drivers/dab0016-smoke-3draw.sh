#!/usr/bin/env bash
# ABOUTME: dab0016 multi-trial smoke — 3 sequential draws of the frozen smoke spec.
# Each identical-spec draw collides on the deterministic job-dir, so we move the
# completed run-dir aside to <hash>.draw<i> before the next draw. Runs under the
# detached driver's `cmd` mode; one handle/sentinel for all 3 draws.
set -uo pipefail
SPEC="specs/dab0016-pin-analytic-semantics.smoke.frozen.yaml"
EXP="dab0016-pin-analytic-semantics"
overall=0
for i in 1 2 3; do
  echo "=========== DRAW $i / 3  ($(date -Is)) ==========="
  uv run --project ../razorback rk run "$SPEC" --runs-dir runs
  rc=$?
  echo "draw $i rk rc=$rc"
  [[ $rc -ne 0 ]] && overall=$rc
  rd="$(ls -dt runs/$EXP/*/ 2>/dev/null | grep -v '\.draw[0-9]*/$' | head -1)"
  rd="${rd%/}"
  if [[ -n "$rd" && -d "$rd" ]]; then
    mv "$rd" "${rd}.draw${i}"
    echo "draw $i run-dir -> ${rd}.draw${i}"
  else
    echo "draw $i WARNING: could not locate fresh run-dir under runs/$EXP/"
  fi
done
echo "=========== ALL 3 DRAWS DONE  ($(date -Is))  overall_rc=$overall ==========="
exit $overall
