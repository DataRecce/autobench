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
    """Among run-* subdirs, pick the one whose summary.stratified_score is the median.

    Reads the LEGACY run summaries (field `stratified_score`) — distinct from rk's
    `stratified_pass_at_1` emitted by build_artifacts.
    """
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
    return runs[len(runs) // 2][1]  # median (upper-middle for even counts)


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
