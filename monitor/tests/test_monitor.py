"""Unit tests for monitor.py pure helpers and filesystem discovery.

These cover the bits that decode razorback's on-disk schema and the small
formatting/navigation utilities — the parts most likely to break when the
schema drifts or someone refactors. The TUI event loop itself needs a tty and
is left for manual verification (see CLAUDE.md).
"""

from __future__ import annotations

import json
from pathlib import Path

import monitor as m


# --- formatting ------------------------------------------------------------

def test_format_duration():
    assert m.format_duration(None) == "-"
    assert m.format_duration(0) == "0s"
    assert m.format_duration(45) == "45s"
    assert m.format_duration(90) == "1m30s"
    assert m.format_duration(3661) == "1h01m"


def test_format_tokens():
    assert m.format_tokens(None) == "-"
    assert m.format_tokens(500) == "500"
    assert m.format_tokens(1500) == "2k"
    assert m.format_tokens(2_500_000) == "2.5M"


def test_clamp():
    assert m.clamp(5, 0, 10) == 5
    assert m.clamp(-1, 0, 10) == 0
    assert m.clamp(99, 0, 10) == 10


def test_visible_window_keeps_selection_in_view():
    items = list(range(100))
    window = m.visible_window(items, selected=50, capacity=10)
    indices = [i for i, _ in window]
    assert len(window) == 10
    assert 50 in indices
    # Window is clamped to the list bounds at the edges.
    assert m.visible_window(items, selected=0, capacity=10)[0][0] == 0
    assert m.visible_window(items, selected=99, capacity=10)[-1][0] == 99
    assert m.visible_window([], selected=0, capacity=10) == []


# --- key handling ----------------------------------------------------------

def test_normalize_key_aliases_and_sequences():
    assert m.normalize_key("q") == "quit"
    assert m.normalize_key("\x03") == "quit"
    assert m.normalize_key("\x1b[A") == "up"
    assert m.normalize_key("\x1bOB") == "down"
    # Modified arrow (e.g. with Ctrl/Shift) still resolves to the base arrow.
    assert m.normalize_key("\x1b[1;5A") == "up"
    assert m.normalize_key("\x1b[6~") == "page-down"
    # Unknown sequence passes through unchanged.
    assert m.normalize_key("zzz") == "zzz"


# --- status / verify styling ----------------------------------------------

def test_status_style_and_icon():
    assert m.status_style("running") == "status.running"
    assert m.status_style("errored") == "status.errored"
    assert m.status_style("completed") == "status.complete"
    assert m.status_icon("running") == ">"
    assert m.status_icon("errored") == "!"
    assert m.status_icon("mystery") == "?"


def test_verify_style_and_outcome():
    assert m.verify_style("reward=1.0") == "verify.pass"
    assert m.verify_style("reward=0.0") == "verify.fail"
    assert m.verify_style("pending") == "verify.pending"
    assert m.verify_outcome("reward=1.0") == "passed"
    assert m.verify_outcome("reward=0") == "failed"
    assert m.verify_outcome("pending") == ""


# --- small text utils ------------------------------------------------------

def test_one_line():
    assert m.one_line(None) == "-"
    assert m.one_line("  hello  ") == "hello"
    assert m.one_line("\n\n  first\nsecond") == "first"
    assert m.one_line("   ") == "-"


def test_compact_json():
    assert m.compact_json({"b": 1, "a": 2}) == '{"a":2,"b":1}'


def test_changed_files_summary():
    text = "Changed files\n- /app/models/foo.sql\n- /app/models/bar.sql\n\ndone"
    assert m.changed_files_summary(text) == "changed: foo.sql, bar.sql"
    assert m.changed_files_summary("no section here") == ""


# --- log entry parsing -----------------------------------------------------

def test_parse_log_entry_plain_line():
    entry = m.parse_log_entry("trial", "just a plain log line")
    assert entry.raw == "just a plain log line"
    assert entry.prefix == ""


def test_parse_log_entry_codex_command():
    line = json.dumps({
        "type": "item.completed",
        "item": {"type": "command_execution", "command": "ls -la", "exit_code": 0},
    })
    entry = m.parse_log_entry("codex", line)
    assert entry.prefix == "command_execution"
    assert entry.description == "ls -la"


def test_parse_log_entry_codex_command_nonzero_exit_marks_error():
    line = json.dumps({
        "type": "item.completed",
        "item": {"type": "command_execution", "command": "false", "exit_code": 1},
    })
    entry = m.parse_log_entry("codex", line)
    assert entry.state == "error"
    assert "(exit 1)" in entry.description


def test_parse_log_entry_rollout_payload():
    line = json.dumps({
        "type": "response_item",
        "payload": {"type": "agent_message", "message": "hello world"},
    })
    entry = m.parse_log_entry("session:first-officer", line)
    assert entry.prefix == "agent_message"
    assert entry.description == "hello world"


# --- dataset table ---------------------------------------------------------

def test_load_dataset_info(tmp_path: Path):
    md = tmp_path / "datasets.md"
    md.write_text(
        "| Dataset | Diff | Description |\n"
        "| --- | --- | --- |\n"
        "| `airbnb001` | easy | count listings |\n"
    )
    info = m.load_dataset_info(md)
    assert info["airbnb001"].difficulty == "easy"
    assert info["airbnb001"].description == "count listings"
    # Header row is skipped, missing file is empty.
    assert "Dataset" not in info
    assert m.load_dataset_info(tmp_path / "nope.md") == {}


# --- filesystem discovery --------------------------------------------------

def _make_job(runs: Path, experiment: str, job: str) -> Path:
    job_dir = runs / experiment / job
    job_dir.mkdir(parents=True)
    return job_dir


def test_discover_jobs_and_status(tmp_path: Path):
    runs = tmp_path / "runs"
    # A finished job.
    done = _make_job(runs, "exp-a", "job1")
    (done / "config.json").write_text(json.dumps({"tasks": [{"path": "/d/airbnb001"}]}))
    (done / "result.json").write_text(json.dumps({
        "finished_at": "2026-06-11T00:00:00Z",
        "n_total_trials": 1,
        "stats": {"n_completed_trials": 1, "n_errored_trials": 0},
    }))
    # A running job (lock present, no result).
    running = _make_job(runs, "exp-a", "job2")
    (running / "config.json").write_text(json.dumps({"tasks": []}))
    (running / "lock.json").write_text("{}")

    jobs_by_exp = m.discover_jobs(runs)
    assert set(jobs_by_exp) == {"exp-a"}
    statuses = {j.path.name: j.status for j in jobs_by_exp["exp-a"]}
    assert statuses == {"job1": "finished", "job2": "running"}


def test_discover_trials_real_and_pending(tmp_path: Path):
    runs = tmp_path / "runs"
    job = _make_job(runs, "exp", "job")
    # config lists two tasks; only one has a trial dir on disk.
    (job / "config.json").write_text(json.dumps({
        "tasks": [{"path": "/data/airbnb001"}, {"path": "/data/airbnb002"}],
    }))
    trial = job / "airbnb001__abc123"
    trial.mkdir()
    (trial / "result.json").write_text(json.dumps({
        "started_at": "2026-06-11T00:00:00Z",
        "finished_at": "2026-06-11T00:01:00Z",
        "verifier_result": {"rewards": {"reward": 1.0}},
        "agent_result": {"n_input_tokens": 100, "n_output_tokens": 50},
    }))

    trials = m.discover_trials(job)
    by_id = {t.task_id: t for t in trials}
    assert set(by_id) == {"airbnb001", "airbnb002"}
    # The on-disk trial is parsed as completed+passed with duration and tokens.
    real = by_id["airbnb001"]
    assert real.status == "completed"
    assert real.verify_result == "reward=1.0"
    assert real.duration_sec == 60.0
    assert real.tokens == 150
    # The configured-but-absent task shows up as a pending placeholder.
    assert by_id["airbnb002"].status == "pending"
    assert by_id["airbnb002"].path is None


def test_trial_status_errored(tmp_path: Path):
    trial = tmp_path / "t__x"
    trial.mkdir()
    (trial / "exception.txt").write_text("boom")
    assert m.trial_status(trial) == "errored"


def test_read_json_tolerates_garbage(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json")
    assert m.read_json(bad) == {}
    assert m.read_json(tmp_path / "missing.json") == {}


# --- mouse parsing & hit-testing -------------------------------------------

from argparse import Namespace
from collections import namedtuple

Region = namedtuple("Region", "x y width height")


def test_parse_mouse_sequence_left_click():
    # SGR: ESC [ < button ; col ; row M/m, coords 1-based.
    ev = m.parse_mouse_sequence("\x1b[<0;13;6M")
    assert ev == m.MouseEvent("press", "left", 12, 5)
    assert m.parse_mouse_sequence("\x1b[<0;13;6m").kind == "release"


def test_parse_mouse_sequence_wheel():
    assert m.parse_mouse_sequence("\x1b[<64;5;5M") == m.MouseEvent("wheel", "wheel-up", 4, 4)
    assert m.parse_mouse_sequence("\x1b[<65;5;5M") == m.MouseEvent("wheel", "wheel-down", 4, 4)


def test_parse_mouse_sequence_rejects_non_mouse():
    assert m.parse_mouse_sequence("\x1b[A") is None
    assert m.parse_mouse_sequence("q") is None


def test_region_contains():
    region = Region(x=5, y=2, width=10, height=4)  # x:5..14, y:2..5
    assert m.region_contains(region, 5, 2)
    assert m.region_contains(region, 14, 5)
    assert not m.region_contains(region, 15, 2)
    assert not m.region_contains(region, 5, 6)


def _monitor_with_runs(tmp_path: Path) -> m.Monitor:
    runs = tmp_path / "runs"
    job = runs / "exp" / "job"
    job.mkdir(parents=True)
    (job / "config.json").write_text(json.dumps({
        "tasks": [{"path": "/d/a001"}, {"path": "/d/a002"}, {"path": "/d/a003"}],
    }))
    for tid in ("a001", "a002", "a003"):
        (job / f"{tid}__x").mkdir()
    args = Namespace(runs_dir=runs, datasets=tmp_path / "none.md", refresh_sec=2.0)
    monitor = m.Monitor(args)
    monitor.refresh(force=True)
    return monitor


def test_handle_click_selects_trial(tmp_path: Path):
    monitor = _monitor_with_runs(tmp_path)
    monitor._trials_capacity = 10
    trials_region = Region(x=34, y=1, width=66, height=12)  # content rows at y=2..
    # Click the 3rd content row -> trial index 2.
    monitor.handle_click(m.MouseEvent("press", "left", 40, 4), {"trials": trials_region})
    assert monitor.focus == 1
    assert monitor.trial_index == 2


def test_handle_click_selects_sidebar_item(tmp_path: Path):
    monitor = _monitor_with_runs(tmp_path)
    monitor._sidebar_capacity = 20
    side_region = Region(x=0, y=1, width=34, height=20)
    # Row 0 of sidebar content is the experiment header; clicking it focuses
    # the sidebar and selects that experiment.
    monitor.handle_click(m.MouseEvent("press", "left", 5, 2), {"sidebar": side_region})
    assert monitor.focus == 0
    assert monitor.sidebar_kind == "experiment"


def test_handle_click_outside_rows_is_ignored(tmp_path: Path):
    monitor = _monitor_with_runs(tmp_path)
    monitor._trials_capacity = 10
    monitor.trial_index = 1
    trials_region = Region(x=34, y=1, width=66, height=12)
    # Click far below the last trial row (only 3 trials) -> no change.
    monitor.handle_click(m.MouseEvent("press", "left", 40, 10), {"trials": trials_region})
    assert monitor.trial_index == 1


def test_handle_wheel_scrolls_log(tmp_path: Path):
    monitor = _monitor_with_runs(tmp_path)
    logs_region = Region(x=34, y=13, width=66, height=10)
    monitor.handle_wheel(m.MouseEvent("wheel", "wheel-up", 40, 15), {"logs": logs_region})
    assert monitor.log_scroll > 0
    before = monitor.log_scroll
    monitor.handle_wheel(m.MouseEvent("wheel", "wheel-down", 40, 15), {"logs": logs_region})
    assert monitor.log_scroll < before


def test_handle_wheel_moves_trial_selection(tmp_path: Path):
    monitor = _monitor_with_runs(tmp_path)
    monitor.focus = 1
    monitor.trial_index = 0
    trials_region = Region(x=34, y=1, width=66, height=12)
    monitor.handle_wheel(m.MouseEvent("wheel", "wheel-down", 40, 5), {"trials": trials_region})
    assert monitor.trial_index == 1
