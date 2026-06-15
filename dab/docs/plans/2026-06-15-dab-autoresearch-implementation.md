# DAB Autoresearch Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up an `rk`-driven autoresearch loop for DataAgentBench (DAB) by adapting ADE-bench's hypotheses workflow skeleton, with the legacy Opus-4.8 run converted into an rk-format `@baseline`.

**Architecture:** A Python shim converts the non-rk legacy Opus run-dir into rk artifacts (`manifest.json` / `summary.json` / `per_trial_outcomes.json` + per-trial `result.json` dirs) so `rk runs diff` / `rk score` / `rk baseline promote` consume it. Codex/gpt-5.5 variants fork the solver-workflow README (the single lever) and run via `rk run`; smoke targeting uses dataset-select + per-query `exclude_tasks`. The spacedock first-officer drives the loop with two human gates (propose, smoke).

**Tech Stack:** Python 3 (stdlib only) for the shim; razorback `rk` CLI; bash drivers; spacedock first-officer/ensign skills; YAML specs.

**Design doc:** `dab/docs/specs/2026-06-15-dab-autoresearch-design.md` (read it first).

**Conventions for every task:**
- Run all `rk` commands from `/home/kent/autobench/dab/` as `uv run --project ../razorback rk <args>`.
- Before any `rk run`: `export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"`.
- **Registry is global and unscoped** (`~/.config/razorback/registry.yaml`, keyed only by `(kind, name)`), and the live ade-bench loop owns the global `@baseline`. DAB MUST use a project-local registry: before any `rk registry` / `rk runs diff` / `rk baseline promote`, `export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml`. Never run a bare `rk registry add run baseline …` — it would overwrite ade-bench's `@baseline`.
- Work on the `dab-autoresearch-design` branch (already created); commit after each task.
- The 12 DAB datasets: `agnews bookreview crmarenapro DEPS_DEV_V1 GITHUB_REPOS googlelocal music_brainz_20k PANCANCER_ATLAS PATENTS stockindex stockmarket yelp`.

---

## Task 1: Baseline shim — legacy Opus run-dir → rk run-dir

**Files:**
- Create: `/home/kent/autobench/dab/tools/legacy_baseline_to_rk.py`
- Test: `/home/kent/autobench/dab/tools/tests/test_legacy_baseline_to_rk.py`

**Context — exact formats (verified in razorback source):**
- Legacy per-query truth lives at `<run>/datasets/<ds>/attempts/attempt-*/validation.json`, shape `{"q1": {"pass": true, ...}, "q2": {"pass": false, ...}}`.
- Legacy aggregate at `<run>/summary.json` has `stratified_score` (we reproduce this number to validate).
- `rk score` rebuilds from trial dirs: `read_trial_outcomes` (aggregate.py:337) walks each subdir containing `result.json`, reads reward from `result["verifier_result"]["rewards"]["reward"]`, and recovers `{dataset, query_id}` by parsing the dir name `<dataset>-q<n>__<suffix>` (aggregate.py:157-168). So per-trial `result.json` dirs are mandatory.
- `rk runs diff` reads `per_trial_outcomes.json` (`outcomes_version == 1`), pairing by `(dataset, int(query_id), int(trial_index))` (pairing.py:8-32).
- `rk runs show` requires both `manifest.json` and `summary.json` (inspect.py:62-67).

- [ ] **Step 1: Write the failing test**

```python
# /home/kent/autobench/dab/tools/tests/test_legacy_baseline_to_rk.py
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from legacy_baseline_to_rk import (
    build_artifacts,
    load_per_query_rewards,
    write_run_dir,
)


def test_load_per_query_rewards_reads_latest_attempt(tmp_path):
    ds = tmp_path / "datasets" / "agnews"
    att = ds / "attempts" / "attempt-001"
    att.mkdir(parents=True)
    (att / "validation.json").write_text(json.dumps({
        "q1": {"pass": True, "answer": "x"},
        "q2": {"pass": False, "answer": "y"},
        "q3": {"pass": True},
    }))
    rewards = load_per_query_rewards(ds)
    assert rewards == {1: 1.0, 2: 0.0, 3: 1.0}


def test_build_artifacts_shapes_and_stratified_math():
    # agnews 2/4 = 0.5 ; yelp 1/1 = 1.0 -> stratified mean = 0.75
    per_dataset = {
        "agnews": {1: 1.0, 2: 0.0, 3: 0.0, 4: 1.0},
        "yelp": {1: 1.0},
    }
    art = build_artifacts(
        experiment="opus-4-8-baseline",
        job_name="deadbeefdeadbeef",
        created_at="2026-06-15T00:00:00Z",
        per_dataset=per_dataset,
    )
    m, s, o = art["manifest"], art["summary"], art["outcomes"]

    assert m["run_dir_version"] == 1
    assert m["experiment"] == "opus-4-8-baseline"
    assert m["n_trials_total"] == 5 and m["n_trials_errored"] == 0
    assert m["benchmark_kind"] == "harbor"
    assert len(m["per_trial_paths"]) == 5

    assert s["summary_version"] == 1
    assert abs(s["stratified_pass_at_1"] - 0.75) < 1e-9
    assert s["datasets"]["agnews"]["dataset_pass_at_1"] == 0.5
    assert s["datasets"]["agnews"]["n_queries"] == 4

    assert o["outcomes_version"] == 1
    assert len(o["trials"]) == 5
    t = next(x for x in o["trials"] if x["trial_name"] == "agnews-q1__opusbase")
    assert t["dataset"] == "agnews" and t["query_id"] == 1
    assert t["trial_index"] == 0 and t["reward"] == 1.0


def test_write_run_dir_emits_score_consumable_trial_dirs(tmp_path):
    per_dataset = {"agnews": {1: 1.0, 2: 0.0}}
    art = build_artifacts(
        experiment="opus-4-8-baseline",
        job_name="abc123abc123abc1",
        created_at="2026-06-15T00:00:00Z",
        per_dataset=per_dataset,
    )
    run_dir = write_run_dir(tmp_path, art)
    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "summary.json").exists()
    assert (run_dir / "per_trial_outcomes.json").exists()
    rj = json.loads((run_dir / "agnews-q1__opusbase" / "result.json").read_text())
    assert rj["exception_info"] is None
    assert rj["verifier_result"]["rewards"]["reward"] == 1.0
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /home/kent/autobench/dab && uv run --project ../razorback python -m pytest tools/tests/test_legacy_baseline_to_rk.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'legacy_baseline_to_rk'`.

- [ ] **Step 3: Write the shim**

```python
# /home/kent/autobench/dab/tools/legacy_baseline_to_rk.py
#!/usr/bin/env python3
# ABOUTME: Convert a legacy (non-rk) DAB run-dir into rk-format run artifacts so it can
# ABOUTME: serve as @baseline for `rk runs diff` / `rk score` / `rk baseline promote`.
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def reward_from_validation(entry) -> float:
    """Legacy validation entry -> reward. Accepts {'pass': bool} or a bare bool."""
    if isinstance(entry, dict):
        return 1.0 if entry.get("pass") is True else 0.0
    return 1.0 if entry is True else 0.0


def load_per_query_rewards(dataset_dir: Path) -> dict[int, float]:
    """Read the latest attempt's validation.json -> {query_id: reward}."""
    matches = sorted(dataset_dir.glob("attempts/attempt-*/validation.json"))
    if not matches:
        raise FileNotFoundError(f"no validation.json under {dataset_dir}/attempts/")
    validation = json.loads(matches[-1].read_text())
    rewards: dict[int, float] = {}
    for key, entry in validation.items():
        if not isinstance(key, str) or not key.startswith("q"):
            continue
        try:
            qid = int(key[1:])
        except ValueError:
            continue
        rewards[qid] = reward_from_validation(entry)
    return rewards


def build_artifacts(
    *,
    experiment: str,
    job_name: str,
    created_at: str,
    per_dataset: dict[str, dict[int, float]],
) -> dict[str, dict]:
    """Pure transform: per-dataset per-query rewards -> rk manifest/summary/outcomes dicts."""
    outcomes_trials: list[dict] = []
    summary_trials: list[dict] = []
    summary_datasets: dict[str, dict] = {}
    per_trial_paths: list[str] = []
    dataset_scores: list[float] = []

    for ds in sorted(per_dataset):
        rewards = per_dataset[ds]
        queries: list[dict] = []
        cell_scores: list[float] = []
        for qid in sorted(rewards):
            r = float(rewards[qid])
            passed = r >= 1.0
            trial_name = f"{ds}-q{qid}__opusbase"
            per_trial_paths.append(trial_name)
            outcomes_trials.append({
                "dataset": ds,
                "query_id": qid,
                "benchmark_kind": None,
                "benchmark_task_id": None,
                "trial_index": 0,
                "trial_name": trial_name,
                "reward": r,
            })
            summary_trials.append({
                "trial_id": trial_name,
                "reward": r,
                "cost_usd": None,
                "wall_seconds": None,
                "error_reason": None,
                "stratum": {"dataset": ds, "query_id": qid},
            })
            queries.append({
                "query_id": qid,
                "n_trials": 1,
                "n_correct": 1 if passed else 0,
                "pass_at_1": 1.0 if passed else 0.0,
            })
            cell_scores.append(1.0 if passed else 0.0)
        ds_pass = sum(cell_scores) / len(cell_scores) if cell_scores else 0.0
        summary_datasets[ds] = {
            "dataset_pass_at_1": ds_pass,
            "n_queries": len(queries),
            "queries": queries,
        }
        dataset_scores.append(ds_pass)

    n = len(outcomes_trials)
    stratified = sum(dataset_scores) / len(dataset_scores) if dataset_scores else None

    manifest = {
        "run_dir_version": 1,
        "experiment": experiment,
        "job_name": job_name,
        "created_at": created_at,
        "spec_path": None,
        "frozen_spec_hash": None,
        "provenance_hash": None,
        "harbor_job_name": job_name,
        "n_trials_total": n,
        "n_trials_completed": n,
        "n_trials_errored": 0,
        "per_trial_paths": per_trial_paths,
        "benchmark_kind": "harbor",
    }
    summary = {
        "summary_version": 1,
        "n_trials_total": n,
        "n_trials_completed": n,
        "n_trials_errored": 0,
        "stratified_pass_at_1": stratified,
        "datasets": summary_datasets,
        "trials": summary_trials,
        "cost_usd": None,
    }
    outcomes = {"outcomes_version": 1, "trials": outcomes_trials}
    return {"manifest": manifest, "summary": summary, "outcomes": outcomes}


def write_run_dir(out_root: Path, artifacts: dict) -> Path:
    """Write rk run-dir + per-trial result.json dirs; return the run-dir path."""
    exp = artifacts["manifest"]["experiment"]
    job = artifacts["manifest"]["job_name"]
    run_dir = out_root / exp / job
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest.json").write_text(json.dumps(artifacts["manifest"], indent=2))
    (run_dir / "summary.json").write_text(json.dumps(artifacts["summary"], indent=2))
    (run_dir / "per_trial_outcomes.json").write_text(
        json.dumps(artifacts["outcomes"], indent=2)
    )
    for t in artifacts["outcomes"]["trials"]:
        td = run_dir / t["trial_name"]
        td.mkdir(parents=True, exist_ok=True)
        (td / "result.json").write_text(json.dumps({
            "exception_info": None,
            "verifier_result": {"rewards": {"reward": t["reward"]}},
            "step_results": [],
        }, indent=2))
    return run_dir


def pick_median_run(experiment_dir: Path) -> Path:
    """Among run-* subdirs, pick the one whose summary.stratified_score is the median."""
    runs = []
    for rd in sorted(experiment_dir.glob("run-*")):
        sp = rd / "summary.json"
        if not sp.exists():
            continue
        score = json.loads(sp.read_text()).get("stratified_score")
        if score is not None:
            runs.append((float(score), rd))
    if not runs:
        raise FileNotFoundError(f"no run-*/summary.json with stratified_score in {experiment_dir}")
    runs.sort(key=lambda x: x[0])
    return runs[len(runs) // 2][1]  # median (lower-middle for even counts)


def convert(source_run: Path, out_root: Path, experiment: str) -> Path:
    manifest = json.loads((source_run / "manifest.json").read_text())
    datasets = manifest["datasets"]
    per_dataset: dict[str, dict[int, float]] = {}
    for ds in datasets:
        per_dataset[ds] = load_per_query_rewards(source_run / "datasets" / ds)
    job_name = hashlib.sha256(
        f"{experiment}:{source_run.resolve()}".encode()
    ).hexdigest()[:16]
    created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    art = build_artifacts(
        experiment=experiment,
        job_name=job_name,
        created_at=created_at,
        per_dataset=per_dataset,
    )
    return write_run_dir(out_root, art)


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert a legacy DAB run-dir to rk format.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--source-run", type=Path, help="A single legacy run-NNN dir.")
    g.add_argument("--from-experiment-dir", type=Path,
                   help="Parent dir with run-* subdirs; the median-stratified run is used.")
    ap.add_argument("--out-root", type=Path, required=True, help="rk runs-dir root (e.g. runs).")
    ap.add_argument("--experiment", required=True, help="rk experiment name for the baseline.")
    args = ap.parse_args()

    source = args.source_run or pick_median_run(args.from_experiment_dir)
    run_dir = convert(source, args.out_root, args.experiment)
    print(f"source-run: {source}")
    print(f"rk run-dir: {run_dir}")
    print(f"stratified_pass_at_1: "
          f"{json.loads((run_dir / 'summary.json').read_text())['stratified_pass_at_1']}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `cd /home/kent/autobench/dab && uv run --project ../razorback python -m pytest tools/tests/test_legacy_baseline_to_rk.py -v`
Expected: PASS — all three tests green.

- [ ] **Step 5: Run the shim on the real legacy run (median of the 5 runs)**

Run:
```bash
cd /home/kent/autobench/dab
uv run --project ../razorback python tools/legacy_baseline_to_rk.py \
  --from-experiment-dir /home/kent/dataagentbench/_runs/spacedock-opus-4-8-xhigh-hint \
  --out-root runs \
  --experiment opus-4-8-baseline
```
Expected output: prints `source-run:` (one of run-003..007), `rk run-dir: runs/opus-4-8-baseline/<hash>`, and `stratified_pass_at_1:` close to the legacy `stratified_score` (~0.68). Note the printed run-dir path — call it `$BASELINE_DIR`.

- [ ] **Step 6: Verify rk consumes it (score + show round-trip)**

Run:
```bash
cd /home/kent/autobench/dab
BASELINE_DIR=$(ls -dt runs/opus-4-8-baseline/*/ | head -1)
uv run --project ../razorback rk score "$BASELINE_DIR" --format json
uv run --project ../razorback rk runs show "$BASELINE_DIR"
```
Expected: `rk score` prints a report whose `stratified_pass_at_1` matches the legacy run's `stratified_score` to within floating-point error (proves the trial-dir `result.json` + name-parse path works). `rk runs show` prints the manifest/summary without error.

- [ ] **Step 7: Commit**

```bash
cd /home/kent/autobench
git add dab/tools/legacy_baseline_to_rk.py dab/tools/tests/test_legacy_baseline_to_rk.py
git commit -m "feat(dab): legacy Opus run-dir -> rk-format baseline shim

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
(The generated `runs/opus-4-8-baseline/` is under the gitignored `runs/` — not committed.)

---

## Task 2: Register the converted run as `@baseline`

**Files:**
- Create: `/home/kent/autobench/dab/razorback-research.toml`

- [ ] **Step 1: Create the DAB registry seed**

```toml
# /home/kent/autobench/dab/razorback-research.toml
# razorback-research.toml — named-reference registry seed for DAB autoresearch.
# Operators `rk registry add run <name> <path>` to bind references.
#   @baseline → the converted Opus-4.8 incumbent run-dir (promotion target)
slug = "dab"
dataset = "dab@1.0"
```

- [ ] **Step 2: Bind `@baseline` to the converted run-dir**

Run:
```bash
cd /home/kent/autobench/dab
BASELINE_DIR=$(ls -dt "$PWD"/runs/opus-4-8-baseline/*/ | head -1)
BASELINE_DIR="${BASELINE_DIR%/}"
uv run --project ../razorback rk registry add run baseline "$BASELINE_DIR"
```
Expected: prints `OK`.

- [ ] **Step 3: Verify resolution round-trips**

Run: `cd /home/kent/autobench/dab && uv run --project ../razorback rk registry resolve run @baseline`
Expected: prints the absolute path to `runs/opus-4-8-baseline/<hash>` (same as `$BASELINE_DIR`).

- [ ] **Step 4: Commit**

```bash
cd /home/kent/autobench
git add dab/razorback-research.toml
git commit -m "feat(dab): registry seed; bind @baseline to converted Opus incumbent

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Port the detached-run drivers

**Files:**
- Create: `/home/kent/autobench/dab/drivers/rk-run-detached.sh`
- Create: `/home/kent/autobench/dab/drivers/matrix.sh`

- [ ] **Step 1: Copy the launcher and retarget it to dab/**

```bash
cp /home/kent/autobench/ade-bench/drivers/rk-run-detached.sh /home/kent/autobench/dab/drivers/rk-run-detached.sh
```

Then apply these exact edits to `/home/kent/autobench/dab/drivers/rk-run-detached.sh`:
- Line 38: change `ADE_BENCH="$(dirname "$SCRIPT_DIR")"` to `DAB_ROOT="$(dirname "$SCRIPT_DIR")"`.
- Replace every other occurrence of `$ADE_BENCH` with `$DAB_ROOT` (lines 47, 106).
- In the worker ntfy block (lines 73-75): change `-H "Title: ade-bench ${KEY}"` to `-H "Title: dab ${KEY}"` and `-d "ade-bench ${KEY}: ${verdict}"` to `-d "dab ${KEY}: ${verdict}"`.
- In usage/help text and comments, replace `ade-bench/` with `dab/` (lines 14, 88, 109).
- Keep the `RAZORBACK_SPACEDOCK_PLUGIN_DIR` export (line 111) unchanged — DAB specs are `spacedock_solver` too.

- [ ] **Step 2: Create a DAB-simplified matrix.sh (no subagent-trace gate)**

The ade-bench matrix gate requires a `subagent-trace-manifest.json` with `captured > 0`, which is ade-specific. DAB does its worthiness check at the smoke STAGE (behavioral read), so the matrix here is just run + audit + score.

```bash
# /home/kent/autobench/dab/drivers/matrix.sh
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
```

- [ ] **Step 3: Make executable and smoke-test the launcher in `cmd` mode**

Run:
```bash
cd /home/kent/autobench/dab
chmod +x drivers/rk-run-detached.sh drivers/matrix.sh
drivers/rk-run-detached.sh selftest - cmd -- bash -c 'echo hello-detached'
sleep 2
HANDLE=$(ls -dt runs/.rk-handles/selftest-*/ | head -1)
cat "$HANDLE/done"; cat "$HANDLE/log"
```
Expected: `done` contains `rc=0` and an `end=`/`rundir=` line; `log` contains `hello-detached`. This proves the nohup + atomic-sentinel mechanism works in dab/.

- [ ] **Step 4: Commit**

```bash
cd /home/kent/autobench
git add dab/drivers/rk-run-detached.sh dab/drivers/matrix.sh
git commit -m "feat(dab): port detached-run launcher + DAB-simplified matrix driver

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Codex anchor full spec (all 12 datasets) + freeze + dry-run

**Files:**
- Create: `/home/kent/autobench/dab/specs/dab-anchor-codex.yaml`

- [ ] **Step 1: Author the anchor full spec**

Base it on `dab/specs/codex-dab-agnews.yaml` (same agent block, plugin_args), but the experiment name is the anchor's and `tasks` lists all 12 datasets (the DAB plugin CLI requires `--datasets`, so the full set must be enumerated). The `solver_workflow` is the unchanged baseline README.

```yaml
# /home/kent/autobench/dab/specs/dab-anchor-codex.yaml
version: 1
experiment: dab-anchor-codex
agent:
  kind: spacedock_solver
  runtime: codex
  model: gpt-5.5
  reasoning_effort: high
  sampling:
    temperature: 0.0
    top_p: null
    seed: null
  solver_workflow: ./solver_workflows/spacedock-readme-baseline
  spacedock_skill_version: "1.0.0"
  max_turns: 200
benchmark:
  kind: harbor
  dataset: dab@1.0
  plugin: dab
  plugin_args:
    hints: true
    data_root: /home/kent/dataagentbench/data
  tasks:
  - agnews
  - bookreview
  - crmarenapro
  - DEPS_DEV_V1
  - GITHUB_REPOS
  - googlelocal
  - music_brainz_20k
  - PANCANCER_ATLAS
  - PATENTS
  - stockindex
  - stockmarket
  - yelp
trials: 1
concurrency:
  trials: 2
observers:
- kind: jsonl
  path: events.jsonl
- kind: stdout
```

- [ ] **Step 2: Freeze the spec**

Run: `cd /home/kent/autobench/dab && uv run --project ../razorback rk freeze --allow-missing specs/dab-anchor-codex.yaml`
Expected: writes `specs/dab-anchor-codex.frozen.yaml` (seals the solver_workflow README content hash; model/image unpinned).

- [ ] **Step 3: Dry-run to confirm the resolved plan covers 54 per-query tasks**

Run:
```bash
cd /home/kent/autobench/dab
export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"
uv run --project ../razorback rk run specs/dab-anchor-codex.frozen.yaml --runs-dir runs --explain
```
Expected: the explain output lists the materialized per-query tasks (`agnews-q1`, …, `yelp-q7`) totaling 54 across 12 datasets, and reports no provenance-drift errors.

- [ ] **Step 4: Commit**

```bash
cd /home/kent/autobench
git add dab/specs/dab-anchor-codex.yaml dab/specs/dab-anchor-codex.frozen.yaml
git commit -m "feat(dab): codex anchor full spec (all 12 datasets) + frozen

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Verify the smoke select-then-exclude mechanism (dry-run only)

**Files:**
- Create: `/home/kent/autobench/dab/specs/dab-smoke-mechanism-check.yaml` (throwaway verification spec)

This task proves `tasks` + `exclude_tasks` selects exactly the intended per-query subset before any hypothesis depends on it.

- [ ] **Step 1: Author a smoke spec selecting agnews + googlelocal, excluding 4 specific queries**

```yaml
# /home/kent/autobench/dab/specs/dab-smoke-mechanism-check.yaml
version: 1
experiment: dab-smoke-mechanism-check
agent:
  kind: spacedock_solver
  runtime: codex
  model: gpt-5.5
  reasoning_effort: high
  sampling:
    temperature: 0.0
    top_p: null
    seed: null
  solver_workflow: ./solver_workflows/spacedock-readme-baseline
  spacedock_skill_version: "1.0.0"
  max_turns: 200
benchmark:
  kind: harbor
  dataset: dab@1.0
  plugin: dab
  plugin_args:
    hints: true
    data_root: /home/kent/dataagentbench/data
  tasks:
  - agnews
  - googlelocal
  exclude_tasks:
  - agnews-q2
  - agnews-q4
  - googlelocal-q1
  - googlelocal-q3
trials: 1
concurrency:
  trials: 2
observers:
- kind: jsonl
  path: events.jsonl
- kind: stdout
```

- [ ] **Step 2: Freeze and dry-run; confirm the exact surviving task set**

Run:
```bash
cd /home/kent/autobench/dab
export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"
uv run --project ../razorback rk freeze --allow-missing specs/dab-smoke-mechanism-check.yaml
uv run --project ../razorback rk run specs/dab-smoke-mechanism-check.frozen.yaml --runs-dir runs --explain --explain-format json
```
Expected: the explain plan's task list contains exactly `agnews-q1`, `agnews-q3`, plus the surviving `googlelocal` queries (all `googlelocal-q*` except `-q1` and `-q3`) — and does NOT contain `agnews-q2`, `agnews-q4`, `googlelocal-q1`, `googlelocal-q3`. This confirms the design §8 mechanism end-to-end.

If `--explain` does not enumerate per-query task ids, fall back: launch the run with the detached driver, wait ~30s for materialization, then inspect the emitted harbor job config (which lists the filtered `TaskConfig` paths) and kill the run before solver cost accrues:
```bash
cd /home/kent/autobench/dab
drivers/rk-run-detached.sh smoke-mech-check specs/dab-smoke-mechanism-check.frozen.yaml run
sleep 30
RD=$(ls -dt runs/dab-smoke-mechanism-check/*/ 2>/dev/null | head -1)
grep -o '[a-zA-Z_]*-q[0-9]*' "$RD/_job_config.yaml" | sort -u   # surviving task ids
HANDLE=$(ls -dt runs/.rk-handles/smoke-mech-check-*/ | head -1); kill "$(cat "$HANDLE/pid")" 2>/dev/null || true
```
Expected from the grep: the same surviving set (no `agnews-q2`/`-q4`, no `googlelocal-q1`/`-q3`).

- [ ] **Step 3: Record the verified mechanism and commit**

If the surviving set is correct, the mechanism is confirmed. Commit the verification spec as a reference example:
```bash
cd /home/kent/autobench
git add dab/specs/dab-smoke-mechanism-check.yaml dab/specs/dab-smoke-mechanism-check.frozen.yaml
git commit -m "test(dab): confirm tasks+exclude_tasks per-query smoke selection via --explain

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
If the surviving set is WRONG (exclude_tasks not applied on the plugin path), STOP and escalate — the smoke-targeting design needs the plugin code change (design §8 alternative).

---

## Task 6: Author the workflow scaffolding

**Files:**
- Create: `/home/kent/autobench/dab/hypotheses/README.md`
- Create: `/home/kent/autobench/dab/hypotheses/_gatekeeper/propose-review-guideline.md`
- Create: `/home/kent/autobench/dab/hypotheses/_artifacts/baseline.yaml`
- Create: `/home/kent/autobench/dab/hypotheses/_artifacts/dataset-gap-ranking.md`
- Create: `/home/kent/autobench/dab/hypotheses/_artifacts/WORKFLOW-REFINE.md`
- Create: `/home/kent/autobench/dab/hypotheses/_artifacts/self-learning.md`

- [ ] **Step 1: Create the workflow README with the (reusable) frontmatter**

Copy the stage frontmatter from ade-bench verbatim (the stage graph is identical) and write DAB-specific prose. Start the file with EXACTLY this frontmatter:

```yaml
---
commissioned-by: spacedock@0.12.1
entity-type: hypothesis
entity-label: hypothesis
entity-label-plural: hypotheses
id-style: slug
stages:
  defaults:
    worktree: false
    concurrency: 1
  states:
    - name: concept
      initial: true
    - name: ideate
    - name: expanded
      terminal: true
    - name: hypothesis
      initial: true
    - name: propose
      gate: true
    - name: smoke
      gate: true
    - name: full
    - name: analyze
    - name: conclude
      terminal: true
  transitions:
    - from: concept
      to: ideate
      label: fan a concept out into candidate hypotheses
    - from: ideate
      to: expanded
      label: the concept has been turned into hypotheses
    - from: hypothesis
      to: propose
      label: begin authoring the variant README + spec
    - from: propose
      to: smoke
      label: README + spec pass the leak-guard gate
    - from: smoke
      to: full
      label: smoke worthwhile; commit to the full run
    - from: smoke
      to: hypothesis
      label: smoke surfaces a flawed change; revise
    - from: smoke
      to: conclude
      label: smoke cleanly falsifies the hypothesis; reject without a full run
    - from: full
      to: analyze
      label: full run complete; interpret evidence
    - from: analyze
      to: conclude
      label: verdict written; promote or discard
---
```

Then write the prose body, reading `ade-bench/hypotheses/README.md` (552 lines) as the structural template and applying these DAB substitutions throughout:

| ade-bench | DAB replacement |
|-----------|-----------------|
| run `rk` from `ade-bench/` | run `rk` from `dab/` |
| `rk registry resolve run @baseline` (bare) | prepend `export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml` — the global registry is owned by the live ade-bench loop; add this to the README's run-prerequisites section |
| `h<NNNN>-<slug>.md` entity id | `dab<NNNN>-<slug>.md` (id-style still slug; prefix is `dab`) |
| solver dir `../solver_workflows/codex-ade-dbt-minimal` | `./solver_workflows/spacedock-readme-baseline` |
| `cp ../specs/baseline.yaml` | `cp specs/dab-anchor-codex.yaml specs/dab<NNNN>-<slug>.yaml` |
| metric `stratified_pass_at_1` above **9/48 (0.1875)** | `stratified_pass_at_1` above the **Opus incumbent (~0.68, resolve `@baseline`)** |
| 48 tasks / `benchmark.n_tasks: 5` smoke | 54 queries / 12 datasets; smoke uses `tasks: [<ds>...]` + `exclude_tasks: [<ds>-q<n>...]` (design §8) |
| dbt `Got N` distance-to-pass / `verifier/test-stdout.txt` | DAB per-query `validation.json` / `reward_per_query.json` distance-to-pass |
| `AUTO_*` / `solution__*` leak tokens | DAB `ground_truth.csv` access + `data/<ds>/db_description_withhint.txt` leak into README |
| smoke-set table `Task` ids | DAB `{dataset}-q{n}` task ids; Baseline column = Opus `@baseline` reward from `per_trial_outcomes.json` |
| `drivers/rk-run-detached.sh` (ade) | same path under `dab/drivers/` (ported in Task 3) |

Keep the §"Detached runs", §"propose stage" (leak-guard + gatekeeper + smoke-set table), §"smoke stage" (deep-dive + Failure Review), §"analyze stage" (required questions), and §"conclude stage" (promote via `rk baseline promote` + Follow-up Routing) structure intact — only the substitutions above change. Add one DAB-specific note in the analyze section: **the codex-vs-Opus model swap is confounded with the README lever (design §7); the behavioral artifact-read must attribute whether the README change itself moved the committed answer.**

- [ ] **Step 2: Create the gatekeeper guideline (adapted)**

```bash
cp /home/kent/autobench/ade-bench/hypotheses/_gatekeeper/propose-review-guideline.md \
   /home/kent/autobench/dab/hypotheses/_gatekeeper/propose-review-guideline.md
```
Then edit `/home/kent/autobench/dab/hypotheses/_gatekeeper/propose-review-guideline.md`:
- Keep rules G1 (single idea/stage), G3 (full spec differs only in `experiment` + `solver_workflow`), G5 (both specs frozen, `spacedock_solver`/`runtime: codex`), G7 (inert-risk advisory), G9 (selector independence).
- Rewrite G2 (leak-guard): forbid `curl`/`wget`/`git clone`/web fetch AND any read of `ground_truth.csv` or copying `data/<ds>/db_description_withhint.txt` content into the README.
- Rewrite G4 (smoke selectors): smoke spec adds only `tasks` (dataset names) + `exclude_tasks` (`{dataset}-q{n}` ids); no other diff from the full spec.
- Rewrite G8 (canary coverage): smoke must keep ≥1 currently-passing canary query from ≥1 non-target dataset (regression tripwire), expressed in DAB stratified terms.
- Replace G10 dbt-specific wording with DAB validator/`reward_per_query.json` reconcile wording.
- Delete G6/G11/G12 if they reference ade-only constructs (dbt test counts, multi-model-scored targets) that have no DAB analogue; renumber remaining rules.

- [ ] **Step 3: Create the `_artifacts` seed files**

`/home/kent/autobench/dab/hypotheses/_artifacts/baseline.yaml`:
```yaml
# @baseline pointer + per-dataset incumbent scores (Opus-4.8 xhigh +hints, converted).
# Resolve the live ref with: rk registry resolve run @baseline
baseline_ref: "@baseline"
solver: "claude-opus-4-8 (xhigh, hints on) — converted legacy run; variants run codex/gpt-5.5"
stratified_pass_at_1: 0.6808   # update to the median-run number printed by the shim in Task 1
note: "Single-reference comparison (design §7): codex variants diff directly against this Opus incumbent."
```

`/home/kent/autobench/dab/hypotheses/_artifacts/dataset-gap-ranking.md`: write a table of the 12 datasets with their Opus-incumbent `dataset_pass_at_1` (read from `$BASELINE_DIR/summary.json`), sorted ascending (lowest score = highest research priority). Header: "Concept/ideate selection input — which dataset+queries to target. Lower dataset_pass_at_1 = more headroom." One row per dataset: `dataset | dataset_pass_at_1 | n_queries | failing query ids`.

`/home/kent/autobench/dab/hypotheses/_artifacts/WORKFLOW-REFINE.md`:
```markdown
# DAB Workflow-Refinement Ledger

Track learnings from STRUCTURAL workflow-refining hypotheses/decisions here (new stage /
reorder / replace / new protocol), not just the entity file. In-stage rule tweaks go to the
gatekeeper guideline.

## Seed
- Pipeline adapted from ade-bench skeleton (design doc 2026-06-15). Stage graph, gates,
  detached-run architecture inherited verbatim. DAB-specific: codex variants vs Opus @baseline
  (confounded — design §7), query-level smoke via tasks+exclude_tasks (design §8).
```

`/home/kent/autobench/dab/hypotheses/_artifacts/self-learning.md`:
```markdown
# DAB Self-Learning Log

Append one entry per concluded hypothesis: verdict (PASSED/REJECTED), the concrete dial it
moved or ruled out, and the transferable takeaway. Keyed to committed-artifact evidence.
```

- [ ] **Step 4: Commit**

```bash
cd /home/kent/autobench
git add dab/hypotheses
git commit -m "feat(dab): autoresearch workflow scaffolding (README, gatekeeper, artifacts)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Anchor full run — validate the loop end-to-end

This is the validation milestone (design §11 step 5). It is long-running (hours); use the detached launcher and let the first-officer own the wait.

- [ ] **Step 1: Launch the anchor full run detached**

Run:
```bash
cd /home/kent/autobench/dab
export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"
drivers/rk-run-detached.sh dab-anchor-full specs/dab-anchor-codex.frozen.yaml run
```
Expected: prints `launched: dab-anchor-full`, a handle dir under `runs/.rk-handles/dab-anchor-full-<ts>/`, and a `log:` path. Returns immediately.

- [ ] **Step 2: Await completion via the sentinel (do NOT foreground-wait)**

Poll across turns:
```bash
cd /home/kent/autobench/dab
HANDLE=$(ls -dt runs/.rk-handles/dab-anchor-full-*/ | head -1)
[[ -f "$HANDLE/done" ]] && cat "$HANDLE/done" || echo "still running (no done sentinel yet)"
```
Expected when finished: `done` contains `rc=0`, `end=<iso>`, `rundir=runs/dab-anchor-codex/<hash>`. If `rc!=0`, read `$HANDLE/log` and triage.

- [ ] **Step 3: Audit + score the anchor run**

Run:
```bash
cd /home/kent/autobench/dab
ANCHOR_DIR=$(ls -dt runs/dab-anchor-codex/*/ | head -1); ANCHOR_DIR="${ANCHOR_DIR%/}"
uv run --project ../razorback rk audit "$ANCHOR_DIR" --policy strict
uv run --project ../razorback rk score "$ANCHOR_DIR" --format json
```
Expected: audit clean (exit 0); score prints the codex anchor's `stratified_pass_at_1` over all 12 datasets.

- [ ] **Step 4: Diff the anchor against the Opus `@baseline`**

Run:
```bash
cd /home/kent/autobench/dab
export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
ANCHOR_DIR=$(ls -dt runs/dab-anchor-codex/*/ | head -1); ANCHOR_DIR="${ANCHOR_DIR%/}"
uv run --project ../razorback rk runs diff \
  "$(uv run --project ../razorback rk registry resolve run @baseline)" "$ANCHOR_DIR"
```
Expected: a paired diff prints without a pairing error. **If pairing fails** with "key sets differ", the legacy and plugin `(dataset, query_id)` sets diverge — record which queries differ and reconcile (the shim covers exactly the legacy `validation.json` queries; a mismatch means the plugin materializes a different query set for some dataset). This is the real-data confirmation that the shim's `(dataset, query_id)` universe matches the rk plugin's.

- [ ] **Step 5: Record the milestone**

Append the anchor result (codex stratified vs Opus incumbent, paired delta, audit status) to `dab/hypotheses/_artifacts/self-learning.md` as the first entry, and commit:
```bash
cd /home/kent/autobench
git add dab/hypotheses/_artifacts/self-learning.md
git commit -m "track(dab): anchor full run — codex baseline vs Opus incumbent

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## After this plan

The loop is live. To open the first hypothesis, run the spacedock first-officer skill on `dab/hypotheses/` — it will fan a concept into `dab0001-*` hypotheses, gate them at propose (leak-guard + gatekeeper + smoke-set table), gate at smoke (deep-dive), run full, analyze (with the §7 confound caveat), and conclude (promote via `rk baseline promote` if a codex variant clears the Opus incumbent on a clean audit).
