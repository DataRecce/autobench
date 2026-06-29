# Setting Up Pilot and Full Run Executors

Spacedock orchestrates the research workflow; it does not know how to run a
specific lab experiment, simulation, evaluation, survey, or analysis job until
the project provides an executor.

When adapting this template, create a small project-specific executor interface
that both `pilot` and `full` can call.

## Executor Contract

Use one command shape for both tiers:

```bash
./scripts/run-experiment <hypothesis-id> --tier pilot --out runs/<hypothesis-id>/pilot
./scripts/run-experiment <hypothesis-id> --tier full  --out runs/<hypothesis-id>/full
```

The executor should:

- read the hypothesis entity and protocol files;
- select the pilot or full sample according to `--tier`;
- run the experiment without changing the protocol;
- write raw outputs, logs, and analysis-ready artifacts under `--out`;
- write a machine-readable summary file;
- exit non-zero on infrastructure or execution failure.

## Required Output Files

Each run directory should contain:

```text
runs/<hypothesis-id>/<tier>/
  meta.json          # command, git sha, timestamp, executor version, tier
  protocol.md        # copied protocol used for this run
  results.json       # primary/secondary metrics and per-case outcomes
  audit.json         # provenance, coverage, exclusions, leakage/safety checks
  logs/              # raw execution logs
  artifacts/         # generated data, model outputs, figures, tables, notebooks
```

Minimum `results.json` shape:

```json
{
  "hypothesis_id": "exp0007",
  "tier": "pilot",
  "status": "completed",
  "primary_metric": {
    "name": "accuracy",
    "value": 0.82,
    "baseline": 0.76,
    "delta": 0.06
  },
  "secondary_metrics": {},
  "cases": []
}
```

Minimum `audit.json` shape:

```json
{
  "status": "clean",
  "coverage_missing": 0,
  "tainted": 0,
  "exclusions": [],
  "provenance": {
    "git_sha": "<sha>",
    "protocol_hash": "<hash>",
    "data_version": "<version>"
  },
  "notes": []
}
```

## Pilot vs Full

The same executor should run both tiers. The difference is sample coverage, not
methodology.

| Tier | Purpose | Typical scope |
|------|---------|---------------|
| `pilot` | Detect whether the intervention fires and whether the setup is valid. | Small target sample plus controls/canaries. |
| `full` | Estimate the real effect under the approved protocol. | Full planned sample or evaluation set. |

Do not change prompts, treatment, scoring, inclusion criteria, model/runtime,
instrument settings, or analysis method between pilot and full unless the
hypothesis explicitly declares that change.

## Detached Runs

If pilot or full runs may outlive an agent turn, wrap the executor in a detached
launcher that writes:

```text
runs/.handles/<key>-<timestamp>/
  pid
  log
  meta
  done
```

The `done` file is the terminal sentinel and should contain at least:

```text
rc=<exit-code> end=<iso-time> rundir=<run-dir>
```

The first officer should scan handles at the start of each turn, then run audit
and analysis only after the sentinel lands.

## Example Foreground Wrapper

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <hypothesis-id> --tier pilot|full --out <run-dir>" >&2
  exit 2
fi

hypothesis_id="$1"
shift

tier=""
out=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tier)
      tier="$2"
      shift 2
      ;;
    --out)
      out="$2"
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$hypothesis_id" || -z "$tier" || -z "$out" ]]; then
  echo "usage: $0 <hypothesis-id> --tier pilot|full --out <run-dir>" >&2
  exit 2
fi

mkdir -p "$out"/{logs,artifacts}

git_sha="$(git rev-parse HEAD 2>/dev/null || true)"
started="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cat > "$out/meta.json" <<EOF
{"hypothesis_id":"$hypothesis_id","tier":"$tier","git_sha":"$git_sha","started":"$started"}
EOF

# Replace this block with the real experiment command.
# Examples: run a notebook, call a simulator, run an eval harness, start a lab
# acquisition script, or submit a batch job.
python scripts/experiment_job.py \
  --hypothesis "$hypothesis_id" \
  --tier "$tier" \
  --out "$out" \
  > "$out/logs/stdout.log" \
  2> "$out/logs/stderr.log"

test -f "$out/results.json"
test -f "$out/audit.json"
```

## Example Detached Launcher

Use a detached launcher when a pilot or full run can outlive an agent turn. This
wrapper starts the foreground executor with `nohup`, records a handle, and writes
the terminal `done` sentinel atomically.

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: $0 <key> <hypothesis-id> pilot|full <run-dir>" >&2
  exit 2
fi

key="$1"
hypothesis_id="$2"
tier="$3"
out="$4"

timestamp="$(date -u +%Y%m%d-%H%M%S)"
handle_dir="runs/.handles/${key}-${timestamp}"
mkdir -p "$handle_dir"

{
  printf 'key=%s\n' "$key"
  printf 'hypothesis_id=%s\n' "$hypothesis_id"
  printf 'tier=%s\n' "$tier"
  printf 'out=%s\n' "$out"
  printf 'start=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$handle_dir/meta"

nohup bash -c '
  set +e
  hypothesis_id="$1"
  tier="$2"
  out="$3"
  handle_dir="$4"
  ./scripts/run-experiment "$hypothesis_id" --tier "$tier" --out "$out" \
    > "$handle_dir/log" 2>&1
  rc="$?"
  end="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  tmp="$handle_dir/done.tmp"
  printf "rc=%s end=%s rundir=%s\n" "$rc" "$end" "$out" > "$tmp"
  mv "$tmp" "$handle_dir/done"
' _ "$hypothesis_id" "$tier" "$out" "$handle_dir" >/dev/null 2>&1 &

pid="$!"
printf '%s\n' "$pid" > "$handle_dir/pid"
printf 'handle=%s\n' "$handle_dir"
```

The first officer should treat `done` as the source of truth. If `done` is
absent, the run is not terminal yet unless the run directory already contains
complete `results.json` and `audit.json` that prove the executor finished.

## What the Spacedock Stages Do With It

- `propose`: writes or reviews the protocol and confirms the executor command.
- `pilot`: runs `./scripts/run-experiment ... --tier pilot`, checks `audit.json`,
  reads `results.json`, and performs artifact-level attribution.
- `full`: runs the same executor with `--tier full`.
- `analyze`: compares full results to baseline and reads artifacts for mechanism.
- `conclude`: records verdict and follow-up routing.
