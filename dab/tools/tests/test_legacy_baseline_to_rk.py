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
