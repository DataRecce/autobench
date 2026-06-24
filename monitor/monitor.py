#!/usr/bin/env python3
"""Lightweight Razorback run monitor."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import select
import sys
import termios
import time
import tty
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Callable, Iterable

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.highlighter import JSONHighlighter
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme


# Logs relative to a *step root* — the trial dir itself in the flat ade-bench
# layout, or each steps/<step>/ dir in DAB's multi-step layout. codex stays
# first so it is the default selected source.
STEP_LOG_CANDIDATES = (
    ("codex", Path("agent/codex.txt")),
    ("claude", Path("agent/claude.txt")),
    ("claude-log", Path("agent/claude.log")),
    ("agent-log", Path("agent/agent.log")),
    ("verifier", Path("verifier/test-stdout.txt")),
)
# Logs that always live at the trial root, regardless of layout.
TRIAL_ROOT_LOGS = (
    ("trial", Path("trial.log")),
    ("exception", Path("exception.txt")),
)
JOB_ACTIVITY_FILES = (
    Path("_job_config.yaml"),
    Path("config.json"),
    Path("job.log"),
    Path("events.jsonl"),
    Path("result.json"),
    Path("summary.json"),
    Path("per_trial_outcomes.json"),
    Path("lock.json"),
)
TRIAL_ACTIVITY_FILES = (
    Path("config.json"),
    Path("result.json"),
    Path("exception.txt"),
    Path("trial.log"),
    Path("agent/codex.txt"),
    Path("agent/claude.txt"),
    Path("agent/claude.log"),
    Path("agent/agent.log"),
    Path("verifier/test-stdout.txt"),
)
KEY_ALIASES = {
    "\x03": "quit",
    "\x04": "quit",
    "q": "quit",
    "Q": "quit",
    "\x1b": "escape",
    "\r": "enter",
    "\n": "enter",
    "\t": "tab",
    "\x1b[Z": "shift-tab",
    "\x1b[A": "up",
    "\x1b[B": "down",
    "\x1b[C": "right",
    "\x1b[D": "left",
    "\x1bOA": "up",
    "\x1bOB": "down",
    "\x1bOC": "right",
    "\x1bOD": "left",
    "\x1b[H": "home",
    "\x1b[F": "end",
    "\x1b[1~": "home",
    "\x1b[4~": "end",
    "\x1b[5~": "page-up",
    "\x1b[6~": "page-down",
}
ARROW_FINAL_KEYS = {
    "A": "up",
    "B": "down",
    "C": "right",
    "D": "left",
}
TILDE_KEYS = {
    "1": "home",
    "4": "end",
    "5": "page-up",
    "6": "page-down",
    "7": "home",
    "8": "end",
}
MODIFIED_ARROW_RE = re.compile(r"^\x1b\[[0-9;?]*([ABCD])$")
MODIFIED_TILDE_RE = re.compile(r"^\x1b\[([0-9]+)(?:;[0-9]+)?~$")
# SGR mouse report: ESC [ < button ; col ; row (M=press, m=release), 1-based.
MOUSE_SGR_RE = re.compile(r"^\x1b\[<(\d+);(\d+);(\d+)([Mm])$")
MOUSE_WHEEL_BIT = 64
# Enable/disable xterm button + SGR-coordinate mouse tracking.
MOUSE_ENABLE = "\x1b[?1000h\x1b[?1006h"
MOUSE_DISABLE = "\x1b[?1006l\x1b[?1000l"
# How many lines a single wheel notch scrolls the log panel.
WHEEL_LOG_LINES = 3
# Trial list sort modes cycled by the `s` key.
SORT_MODES = ("name", "passed", "failed")
# dbt's run/test summary line, e.g. "Done. PASS=9 WARN=0 ERROR=2 SKIP=0 NO-OP=0 TOTAL=11".
# The verifier emits one per dbt invocation; the final match is the test run.
TEST_SUMMARY_RE = re.compile(r"Done\. PASS=(\d+).*?TOTAL=(\d+)")

STYLES = {
    "text": "white",
    "muted": "bright_black",
    "chrome": "bold cyan",
    "focus": "bold magenta",
    "selection": "reverse bold yellow",
    "panel.border": "cyan",
    "panel.title": "bold cyan",
    "sidebar.border": "blue",
    "trials.border": "cyan",
    "status.running": "bold cyan",
    "status.pending": "yellow",
    "status.errored": "bold red",
    "status.complete": "green",
    "log.header": "bold magenta",
    "log.type": "bold magenta",
    "log.separator": "bright_black",
    "log.started": "yellow",
    "log.completed": "green",
    "log.error": "bold red",
    "verify.pass": "green",
    "verify.partial": "yellow",
    "verify.pending": "bright_black",
    "verify.fail": "bold red",
}
RICH_THEME = Theme(STYLES)


@dataclass(frozen=True)
class DatasetInfo:
    difficulty: str = ""
    description: str = ""


@dataclass
class Trial:
    name: str
    path: Path | None
    task_id: str
    status: str
    verify_result: str
    agent_answer: str
    truth_summary: str
    log_sources: list[tuple[str, Path]]
    duration_sec: float | None = None
    tests: tuple[int, int] | None = None
    tokens: int | None = None
    # Batch DAB only: a trial is a whole dataset, so its outcome is a pass@1
    # (the verifier reward) over query_passed/query_total queries, not a binary
    # [passed]/[failed]. None for per-query DAB and ade-bench trials.
    pass_at_1: float | None = None
    query_passed: int | None = None
    query_total: int | None = None


@dataclass
class Job:
    experiment: str
    path: Path
    updated: float
    status: str
    trials: list[Trial]
    progress: tuple[int, int] | None = None
    passed: int | None = None
    is_dab: bool = False
    is_batch_dab: bool = False
    pass_at_1: float | None = None  # stratified macro-average (DAB)
    query_passed: int | None = None  # batch DAB: queries passed across datasets
    query_total: int | None = None  # batch DAB: total queries on the slate


@dataclass(frozen=True)
class LogEntry:
    prefix: str
    description: str
    raw: str = ""
    state: str = ""
    is_json: bool = False


@dataclass(frozen=True)
class MouseEvent:
    kind: str  # "press", "release", or "wheel"
    button: str  # "left"/"middle"/"right"/"other" or "wheel-up"/"wheel-down"
    col: int  # 0-based screen column
    row: int  # 0-based screen row


def main() -> int:
    args = parse_args()

    try:
        Monitor(args).run()
    except (KeyboardInterrupt, EOFError):
        return 130
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monitor Razorback run directories.")
    parser.add_argument(
        "--runs-dir",
        type=Path,
        default=Path("runs"),
        help="Run directory root to search for Razorback jobs.",
    )
    parser.add_argument("--datasets", type=Path, default=Path("datasets.md"))
    parser.add_argument("--refresh-sec", type=float, default=2.0)
    return parser


class TerminalInput:
    def __init__(self, stream: IO[str] | None = None) -> None:
        self.stream = stream or sys.stdin
        self.original_settings: list[object] | None = None

    def __enter__(self) -> TerminalInput:
        if self.stream.isatty():
            fd = self.stream.fileno()
            self.original_settings = termios.tcgetattr(fd)
            tty.setcbreak(fd)
            sys.stdout.write(MOUSE_ENABLE)
            sys.stdout.flush()
        return self

    def __exit__(self, *_exc_info: object) -> None:
        if self.original_settings is not None:
            sys.stdout.write(MOUSE_DISABLE)
            sys.stdout.flush()
            termios.tcsetattr(
                self.stream.fileno(),
                termios.TCSADRAIN,
                self.original_settings,
            )

    def read_key(self, timeout: float) -> str | MouseEvent | None:
        if not self.stream.isatty():
            time.sleep(timeout)
            return None
        ready, _write, _error = select.select([self.stream], [], [], timeout)
        if not ready:
            return None
        first = self.read_raw_char()
        if first is None:
            return None
        if first == "\x1b":
            sequence = first + self.read_pending_chars()
            mouse = parse_mouse_sequence(sequence)
            if mouse is not None:
                return mouse
            return normalize_key(sequence)
        return normalize_key(first)

    def read_pending_chars(self) -> str:
        chars = []
        deadline = time.monotonic() + 0.1
        first = self.read_char_before_deadline(deadline)
        if first is None:
            return ""
        chars.append(first)

        if first == "O":
            second = self.read_char_before_deadline(deadline)
            if second is not None:
                chars.append(second)
            return "".join(chars)

        if first != "[":
            return "".join(chars)

        while True:
            char = self.read_char_before_deadline(deadline)
            if char is None:
                break
            chars.append(char)
            if is_csi_final_byte(char):
                break
        return "".join(chars)

    def read_char_before_deadline(self, deadline: float) -> str | None:
        while time.monotonic() < deadline:
            timeout = max(0, deadline - time.monotonic())
            ready, _write, _error = select.select([self.stream], [], [], timeout)
            if ready:
                return self.read_raw_char()
        return None

    def read_raw_char(self) -> str | None:
        # Read straight from the file descriptor, not the buffered stream. A
        # buffered read(1) pulls the rest of an escape sequence (e.g. "[A" of an
        # arrow key) into Python's text buffer, where the next select() on the
        # fd can't see it -- so the sequence never reassembles and arrows look
        # like a bare ESC. os.read keeps select() and reads on the same buffer.
        data = os.read(self.stream.fileno(), 1)
        if not data:
            return None
        return data.decode("latin-1")


class Monitor:
    def __init__(
        self,
        args: argparse.Namespace,
        *,
        console: Console | None = None,
        input_reader: TerminalInput | None = None,
    ) -> None:
        self.console = console or Console(theme=RICH_THEME)
        self.input_reader = input_reader or TerminalInput()
        self.runs_dir = args.runs_dir
        self.datasets = load_dataset_info(args.datasets)
        self.refresh_sec = max(0.5, args.refresh_sec)
        self.experiment_index = 0
        self.job_index = 0
        self.trial_index = 0
        self.focus = 0
        self.sidebar_kind = "experiment"
        self.reset_log_view()
        self.log_scroll = 0
        self.sort_mode = "name"
        self.picker_open = False
        self.picker_index = 0
        self.message = ""
        self.jobs_by_experiment: dict[str, list[Job]] = {}
        self.experiments: list[str] = []
        self.last_refresh = 0.0
        self.trial_cache: dict[Path, tuple[tuple[object, ...], list[Trial]]] = {}
        # Geometry of the last full render, used to map mouse clicks back to
        # rows. _last_layout is None whenever the current frame is not the
        # normal dashboard (terminal-too-small notice or the log picker).
        self._last_layout: Layout | None = None
        self._sidebar_capacity = 0
        self._trials_capacity = 0

    def run(self) -> None:
        self.refresh(force=True)
        with self.input_reader as input_reader:
            with Live(
                self.render(),
                console=self.console,
                refresh_per_second=4,
                auto_refresh=False,
                screen=True,
                transient=False,
            ) as live:
                dirty = False
                while True:
                    dirty = self.refresh() or dirty
                    key = input_reader.read_key(self.key_poll_interval())
                    if key is None:
                        if dirty:
                            live.update(self.render(), refresh=True)
                            dirty = False
                        continue
                    if self.handle_key(key):
                        return
                    live.update(self.render(), refresh=True)
                    dirty = False

    def key_poll_interval(self) -> float:
        remaining = self.refresh_sec - (time.time() - self.last_refresh)
        return max(0.05, min(0.2, remaining))

    def refresh(self, *, force: bool = False) -> bool:
        if not force and time.time() - self.last_refresh < self.refresh_sec:
            return False
        previous_experiment = self.current_experiment()
        previous_job = self.current_job_path()
        previous_trial = self.current_trial_name()

        self.jobs_by_experiment = discover_jobs(self.runs_dir)
        self.experiments = sort_experiments(self.jobs_by_experiment)
        self.last_refresh = time.time()

        if previous_experiment in self.experiments:
            self.experiment_index = self.experiments.index(previous_experiment)
        else:
            self.experiment_index = min(self.experiment_index, max(0, len(self.experiments) - 1))

        jobs = self.current_jobs()
        if previous_job is not None:
            for index, job in enumerate(jobs):
                if job.path == previous_job:
                    self.job_index = index
                    break
            else:
                self.job_index = min(self.job_index, max(0, len(jobs) - 1))
        else:
            self.job_index = min(self.job_index, max(0, len(jobs) - 1))

        self.load_current_job_trials()

        trials = self.current_trials()
        if previous_trial is not None:
            for index, trial in enumerate(trials):
                if trial.name == previous_trial:
                    self.trial_index = index
                    break
            else:
                self.trial_index = min(self.trial_index, max(0, len(trials) - 1))
        else:
            self.trial_index = min(self.trial_index, max(0, len(trials) - 1))

        self.log_source_index = min(
            self.log_source_index,
            max(0, len(self.current_log_sources()) - 1),
        )
        return True

    def load_current_job_trials(self) -> None:
        job = self.current_job()
        if job is None:
            return
        signature = job_trial_signature(job.path)
        cached = self.trial_cache.get(job.path)
        if cached is not None and cached[0] == signature:
            job.trials = cached[1]
        else:
            job.trials = discover_trials(job.path)
            self.trial_cache[job.path] = (signature, job.trials)
        job.status = job_status(job.path, job.trials)

    def reset_log_view(self) -> None:
        self.log_source_index = 0
        self.log_scroll = 0

    def scroll_log(self, delta: int) -> None:
        # Positive delta scrolls up (further back in history). The upper bound
        # depends on the file length, which is enforced in log_view() once we
        # read it; here we only keep the offset from going below the live tail.
        self.log_scroll = max(0, self.log_scroll + delta)

    def log_panel_height(self) -> int:
        body_height = max(1, self.console.size.height - 3)
        return max(3, body_height - 22)

    def log_content_height(self) -> int:
        return max(0, self.log_panel_height() - 3)

    def log_page_size(self) -> int:
        return max(1, self.log_content_height() - 1)

    def log_view(self, count: int) -> tuple[str | None, Path | None, list[str]]:
        source = self.current_log_source()
        if source is None:
            self.log_scroll = 0
            return None, None, []
        label, path = source
        lines, clamped = read_log_window(path, count, self.log_scroll)
        self.log_scroll = clamped
        return label, path, lines

    def handle_key(self, key: str | MouseEvent) -> bool:
        if isinstance(key, MouseEvent):
            return self.handle_mouse(key)
        if self.picker_open:
            return self.handle_picker_key(key)
        if key == "quit":
            return True
        if key == "tab":
            self.focus = (self.focus + 1) % 2
        elif key == "shift-tab":
            self.focus = (self.focus - 1) % 2
        elif key in {"r", "R"}:
            self.refresh(force=True)
        elif key in {"s", "S"}:
            self.cycle_sort()
        elif key in {"f", "F"}:
            self.open_picker()
        elif key in {"l", "L"}:
            sources = self.current_log_sources()
            if sources:
                self.log_source_index = (self.log_source_index + 1) % len(sources)
                self.log_scroll = 0
        elif key == "page-up":
            self.scroll_log(self.log_page_size())
        elif key == "page-down":
            self.scroll_log(-self.log_page_size())
        elif key == "left":
            self.focus = 0
        elif key == "right":
            self.focus = 1
        elif key == "[":
            self.move_job(-1)
        elif key == "]":
            self.move_job(1)
        elif key in {"up", "k"}:
            self.move_selection(-1)
        elif key in {"down", "j"}:
            self.move_selection(1)
        elif key == "home":
            self.set_selection(0)
        elif key == "end":
            self.set_selection(10**9)
        return False

    def cycle_sort(self) -> None:
        # Advance the trial sort mode, keeping the same trial selected.
        selected = self.current_trial_name()
        self.sort_mode = SORT_MODES[(SORT_MODES.index(self.sort_mode) + 1) % len(SORT_MODES)]
        if selected is None:
            return
        for index, trial in enumerate(self.current_trials()):
            if trial.name == selected:
                self.trial_index = index
                break

    def open_picker(self) -> None:
        sources = self.current_log_sources()
        if not sources:
            return
        self.picker_open = True
        self.picker_index = clamp(self.log_source_index, 0, len(sources) - 1)

    def handle_picker_key(self, key: str) -> bool:
        if key == "quit":
            return True
        sources = self.current_log_sources()
        last = max(0, len(sources) - 1)
        if key == "escape":
            self.picker_open = False
        elif key in {"up", "k"}:
            self.picker_index = clamp(self.picker_index - 1, 0, last)
        elif key in {"down", "j"}:
            self.picker_index = clamp(self.picker_index + 1, 0, last)
        elif key == "home":
            self.picker_index = 0
        elif key == "end":
            self.picker_index = last
        elif key in {"enter", "l", "f"}:
            if sources:
                self.log_source_index = clamp(self.picker_index, 0, last)
                self.log_scroll = 0
            self.picker_open = False
        return False

    def handle_mouse(self, event: MouseEvent) -> bool:
        # Mouse is ignored while the picker is open or when the last frame was
        # not the dashboard (so we have no row geometry to hit-test against).
        if self.picker_open or self._last_layout is None:
            return False
        regions = self.compute_regions(self._last_layout)
        if not regions:
            return False
        if event.kind == "wheel":
            self.handle_wheel(event, regions)
        elif event.kind == "press" and event.button == "left":
            self.handle_click(event, regions)
        return False

    def handle_click(self, event: MouseEvent, regions: dict) -> None:
        sidebar = regions.get("sidebar")
        if sidebar is not None and region_contains(sidebar, event.col, event.row):
            self.focus = 0
            items = self.sidebar_items()
            window = visible_window(items, self.current_sidebar_index(), self._sidebar_capacity)
            offset = event.row - (sidebar.y + 1)
            if 0 <= offset < len(window):
                _index, (kind, experiment_index, job_index) = window[offset]
                self.select_sidebar_item(kind, experiment_index, job_index)
            return
        trials = regions.get("trials")
        if trials is not None and region_contains(trials, event.col, event.row):
            self.focus = 1
            trial_list = self.current_trials()
            window = visible_window(trial_list, self.trial_index, self._trials_capacity)
            offset = event.row - (trials.y + 1)
            if 0 <= offset < len(window):
                self.trial_index = window[offset][0]
                self.reset_log_view()
            return

    def handle_wheel(self, event: MouseEvent, regions: dict) -> None:
        direction = -1 if event.button == "wheel-up" else 1
        logs = regions.get("logs")
        if logs is not None and region_contains(logs, event.col, event.row):
            # Wheel up walks back into history (positive scroll offset).
            self.scroll_log(-direction * WHEEL_LOG_LINES)
            return
        sidebar = regions.get("sidebar")
        if sidebar is not None and region_contains(sidebar, event.col, event.row):
            self.focus = 0
            self.move_sidebar_selection(direction)
            return
        trials = regions.get("trials")
        if trials is not None and region_contains(trials, event.col, event.row):
            self.focus = 1
            trial_list = self.current_trials()
            if trial_list:
                self.trial_index = (self.trial_index + direction) % len(trial_list)
                self.reset_log_view()

    def compute_regions(self, layout: Layout) -> dict:
        # Ask rich where it placed each named leaf panel for the current size,
        # so click coordinates map to the exact rows that were drawn.
        size = self.console.size
        options = self.console.options.update_dimensions(size.width, size.height)
        try:
            render_map = layout.render(self.console, options)
        except Exception:
            return {}
        return {lay.name: render.region for lay, render in render_map.items() if lay.name}

    def move_job(self, delta: int) -> None:
        jobs = self.current_jobs()
        if not jobs:
            return
        self.job_index = clamp(self.job_index + delta, 0, len(jobs) - 1)
        self.sidebar_kind = "job"
        self.trial_index = 0
        self.reset_log_view()
        self.load_current_job_trials()

    def move_selection(self, delta: int) -> None:
        if self.focus == 0:
            self.move_sidebar_selection(delta)
        elif self.focus == 1:
            trials = self.current_trials()
            if trials:
                # Wrap around like the sidebar: down from the last trial selects
                # the first and up from the first selects the last.
                self.trial_index = (self.trial_index + delta) % len(trials)
                self.reset_log_view()

    def move_sidebar_selection(self, delta: int) -> None:
        items = self.sidebar_items()
        if not items:
            return
        # Wrap around so up from the top lands on the last row and vice versa.
        index = (self.current_sidebar_index() + delta) % len(items)
        kind, experiment_index, job_index = items[index]
        self.select_sidebar_item(kind, experiment_index, job_index)

    def select_sidebar_item(
        self,
        kind: str,
        experiment_index: int,
        job_index: int | None,
    ) -> None:
        if not self.experiments:
            return
        changed_experiment = experiment_index != self.experiment_index
        self.experiment_index = clamp(experiment_index, 0, len(self.experiments) - 1)
        self.sidebar_kind = kind
        if kind == "job" and job_index is not None:
            jobs = self.current_jobs()
            self.job_index = clamp(job_index, 0, len(jobs) - 1) if jobs else 0
        else:
            self.job_index = 0
        self.trial_index = 0
        self.reset_log_view()
        if changed_experiment or kind == "job":
            self.load_current_job_trials()

    def move_experiment_selection(self, delta: int) -> None:
        if not self.experiments:
            return
        self.experiment_index = clamp(self.experiment_index + delta, 0, len(self.experiments) - 1)
        self.sidebar_kind = "experiment"
        self.job_index = 0
        self.trial_index = 0
        self.reset_log_view()
        self.load_current_job_trials()

    def set_selection(self, value: int) -> None:
        if self.focus == 0 and self.experiments:
            self.experiment_index = min(value, len(self.experiments) - 1)
            self.sidebar_kind = "experiment"
            self.job_index = 0
            self.trial_index = 0
            self.reset_log_view()
            self.load_current_job_trials()
        elif self.focus == 1 and self.current_trials():
            self.trial_index = min(value, len(self.current_trials()) - 1)

    def render(self) -> Layout | Panel | Align:
        size = self.console.size
        if size.height < 12 or size.width < 80:
            self._last_layout = None
            return Panel(
                Text("Terminal too small; use at least 80x12.", style="muted"),
                border_style="panel.border",
            )

        if self.picker_open:
            self._last_layout = None
            return render_log_picker(self)

        body_height = max(1, size.height - 3)
        sidebar_capacity = max(1, body_height - 2)
        log_height = self.log_panel_height()

        layout = Layout(name="root")
        layout.split_column(
            Layout(render_header(), name="header", size=1),
            Layout(name="body"),
            Layout(render_status_line(self.status_line()), name="footer", size=1),
        )
        layout["body"].split_row(
            Layout(
                render_sidebar_panel(self, capacity=sidebar_capacity),
                name="sidebar",
                ratio=1,
                minimum_size=34,
            ),
            Layout(name="main", ratio=2, minimum_size=40),
        )
        layout["main"].split_column(
            Layout(render_trials_panel(self, capacity=10), name="trials", size=12),
            Layout(
                render_trial_info_panel(self.current_trial(), self.datasets),
                name="trial-info",
                size=10,
            ),
            Layout(render_current_log_panel(self, height=log_height), name="logs"),
        )
        # Remember what we drew so a later mouse click can be hit-tested against
        # the same windows. capacity here must match what the panels received.
        self._last_layout = layout
        self._sidebar_capacity = sidebar_capacity
        self._trials_capacity = 10
        return layout

    def status_line(self) -> str:
        job = self.current_job()
        trial = self.current_trial()
        source = self.current_log_source()
        parts = []
        if job is not None:
            parts.append(f"job={job.path.name}")
            parts.append(f"status={job.status}")
        if trial is not None:
            parts.append(f"trial={trial.task_id}")
        if source is not None:
            parts.append(f"log={source[0]}")
        parts.append(f"sort={self.sort_mode}")
        parts.append(time.strftime("%H:%M:%S"))
        return " | ".join(parts)

    def sidebar_items(self) -> list[tuple[str, int, int | None]]:
        items = []
        for experiment_index, experiment in enumerate(self.experiments):
            items.append(("experiment", experiment_index, None))
            if experiment_index == self.experiment_index:
                for job_index, _job in enumerate(self.jobs_by_experiment.get(experiment, [])):
                    items.append(("job", experiment_index, job_index))
        return items

    def current_sidebar_index(self) -> int:
        items = self.sidebar_items()
        if not items:
            return 0
        wanted_job = self.job_index if self.sidebar_kind == "job" else None
        for index, (kind, experiment_index, job_index) in enumerate(items):
            if experiment_index != self.experiment_index:
                continue
            if self.sidebar_kind == "job" and kind == "job" and job_index == wanted_job:
                return index
            if self.sidebar_kind == "experiment" and kind == "experiment":
                return index
        for index, (_kind, experiment_index, _job_index) in enumerate(items):
            if experiment_index == self.experiment_index:
                return index
        return 0

    def current_experiment(self) -> str | None:
        if not self.experiments:
            return None
        return self.experiments[clamp(self.experiment_index, 0, len(self.experiments) - 1)]

    def current_jobs(self) -> list[Job]:
        experiment = self.current_experiment()
        return self.jobs_by_experiment.get(experiment, []) if experiment else []

    def current_job(self) -> Job | None:
        jobs = self.current_jobs()
        if not jobs:
            return None
        return jobs[clamp(self.job_index, 0, len(jobs) - 1)]

    def current_job_path(self) -> Path | None:
        job = self.current_job()
        return job.path if job else None

    def current_trials(self) -> list[Trial]:
        job = self.current_job()
        if job is None:
            return []
        return sort_trials(job.trials, self.sort_mode)

    def current_trial(self) -> Trial | None:
        trials = self.current_trials()
        if not trials:
            return None
        return trials[clamp(self.trial_index, 0, len(trials) - 1)]

    def current_trial_name(self) -> str | None:
        trial = self.current_trial()
        return trial.name if trial else None

    def current_log_sources(self) -> list[tuple[str, Path]]:
        trial = self.current_trial()
        if trial is not None and trial.log_sources:
            return trial.log_sources
        job = self.current_job()
        if job is None:
            return []
        sources = []
        for name in ("job.log", "events.jsonl"):
            path = job.path / name
            if path.exists():
                sources.append((name, path))
        return sources

    def current_log_source(self) -> tuple[str, Path] | None:
        sources = self.current_log_sources()
        if not sources:
            return None
        return sources[clamp(self.log_source_index, 0, len(sources) - 1)]


def normalize_key(sequence: str) -> str:
    key = KEY_ALIASES.get(sequence)
    if key is not None:
        return key
    arrow = MODIFIED_ARROW_RE.match(sequence)
    if arrow:
        return ARROW_FINAL_KEYS[arrow.group(1)]
    tilde = MODIFIED_TILDE_RE.match(sequence)
    if tilde and tilde.group(1) in TILDE_KEYS:
        return TILDE_KEYS[tilde.group(1)]
    return sequence


def is_csi_final_byte(char: str) -> bool:
    return len(char) == 1 and 0x40 <= ord(char) <= 0x7E


def parse_mouse_sequence(sequence: str) -> MouseEvent | None:
    match = MOUSE_SGR_RE.match(sequence)
    if not match:
        return None
    button = int(match.group(1))
    col = max(0, int(match.group(2)) - 1)
    row = max(0, int(match.group(3)) - 1)
    if button & MOUSE_WHEEL_BIT:
        wheel = "wheel-up" if button & 1 == 0 else "wheel-down"
        return MouseEvent("wheel", wheel, col, row)
    kind = "press" if match.group(4) == "M" else "release"
    name = {0: "left", 1: "middle", 2: "right"}.get(button & 0b11, "other")
    return MouseEvent(kind, name, col, row)


def region_contains(region: object, col: int, row: int) -> bool:
    return (
        region.x <= col < region.x + region.width
        and region.y <= row < region.y + region.height
    )


def render_header() -> Text:
    return Text(
        "Razorback Monitor  q:quit  click/wheel:select  up/down:select  tab:panel  []:job  "
        "l:log  f:pick-log  s:sort  pgup/pgdn:scroll  r:refresh",
        style="chrome",
    )


def render_status_line(status: str) -> Text:
    return Text(status, style="chrome")


def render_log_picker(monitor: Monitor) -> Align:
    sources = monitor.current_log_sources()
    trial = monitor.current_trial()
    selected = clamp(monitor.picker_index, 0, max(0, len(sources) - 1))
    body = Text()
    if not sources:
        append_line(body, "No log sources for this trial", "muted")
    else:
        # Window the list around the selection so the panel never overflows the
        # screen (which would crop and hide rows). Every source `l` can cycle to
        # stays reachable here; hidden rows are flagged so nothing looks dropped.
        capacity = max(3, monitor.console.size.height - 6)
        window = visible_window(sources, selected, capacity)
        above = window[0][0] if window else 0
        below = len(sources) - 1 - (window[-1][0] if window else 0)
        if above > 0:
            append_line(body, f"  ... {above} more above", "muted")
        for index, (label, _path) in window:
            cursor = ">" if index == selected else " "
            style = "selection" if index == selected else "text"
            append_line(body, f"{cursor} {label}", style)
        if below > 0:
            append_line(body, f"  ... {below} more below", "muted")
    body.append("\n")
    body.append("up/down move   enter select   esc cancel", style="muted")
    title = f"Select log - {trial.task_id}" if trial is not None else "Select log source"
    width = min(72, max(40, monitor.console.size.width - 8))
    panel = Panel(
        body,
        title=Text(title, style="focus"),
        border_style="focus",
        box=box.SQUARE,
        expand=False,
        width=width,
    )
    return Align.center(panel, vertical="middle")


def render_sidebar_panel(monitor: Monitor, *, capacity: int) -> Panel:
    items = monitor.sidebar_items()
    selected = monitor.current_sidebar_index()
    # no_wrap keeps each item on exactly one screen row -- a wrapped long name
    # would shift every row below it and misalign click hit-testing.
    lines = Text(no_wrap=True, overflow="ellipsis")
    if not items:
        append_line(lines, "No runs found", "muted")
    else:
        for index, item in visible_window(items, selected, capacity):
            append_sidebar_line(lines, monitor, index, item, selected)
    return titled_panel(
        lines,
        "Experiments / Jobs",
        focused=monitor.focus == 0,
        border_style="sidebar.border",
    )


def append_sidebar_line(
    lines: Text,
    monitor: Monitor,
    index: int,
    item: tuple[str, int, int | None],
    selected: int,
) -> None:
    kind, experiment_index, job_index = item
    experiment = monitor.experiments[experiment_index]
    jobs = monitor.jobs_by_experiment.get(experiment, [])
    if kind == "experiment":
        active = any(job.status == "running" for job in jobs)
        marker = "*" if active else " "
        expander = "v" if experiment_index == monitor.experiment_index else ">"
        if not jobs:
            expander = " "
        text = f"{expander} {marker} {experiment} ({len(jobs)})"
        style = "status.running" if active else "log.header"
    else:
        job = jobs[job_index or 0]
        text = f"    {status_icon(job.status)} {job.path.name} {job.status}"
        suffix = job_progress_suffix(job)
        if suffix:
            text = f"{text}  {suffix}"
        style = status_style(job.status)
    append_line(lines, text, "selection" if index == selected else style)


def job_progress_suffix(job: Job) -> str:
    # Sidebar annotation. Terminal jobs (finished/errored) show passed/total;
    # running jobs show a live completed/total "done" count plus passed-so-far.
    # DAB jobs also append pass@1 (stratified macro-average, datasets weighted
    # equally; see job_macro_pass_at_1).
    if job.progress is None:
        return ""
    completed, total = job.progress
    if total <= 0:
        return ""
    # Batch DAB runs one trial per whole dataset and scores queries, not whole
    # datasets, so "passed" is queries passed / total queries on the slate
    # (parsed from each trial's reward_per_query.json + the tasks' stratum.json),
    # not the trial-pass count the per-query layout reports.
    if job.is_batch_dab and job.query_total:
        graded = f"{job.query_passed}/{job.query_total} passed"
        if job.status == "running":
            return f"{completed}/{total} done · {graded}" + pass_at_1_suffix(job)
        return graded + pass_at_1_suffix(job)
    if job.status == "running":
        done = f"{completed}/{total} done"
        if job.passed is not None:
            suffix = f"{done} · {job.passed} passed"
            return suffix + pass_at_1_suffix(job)
        return done
    if job.status in {"finished", "completed", "errored"} and job.passed is not None:
        return f"{job.passed}/{total} passed" + pass_at_1_suffix(job)
    return ""


def pass_at_1_suffix(job: Job) -> str:
    if job.is_dab and job.pass_at_1 is not None:
        return f" · pass@1 {format_pct(job.pass_at_1)}"
    return ""


def format_pct(fraction: float) -> str:
    return f"{fraction * 100:.1f}%"


def render_trials_panel(monitor: Monitor, *, capacity: int) -> Panel:
    trials = monitor.current_trials()
    if not trials:
        body: object = Text("No trials yet", style="muted")
    else:
        # Left column holds the trial label; the three right-aligned columns
        # fill the previously empty right side with duration, tests, and tokens.
        table = Table.grid(expand=True, padding=(0, 1), pad_edge=False)
        table.add_column(ratio=1, no_wrap=True, overflow="ellipsis")
        for _ in range(3):
            table.add_column(justify="right", no_wrap=True)
        for index, trial in visible_window(trials, monitor.trial_index, capacity):
            add_trial_row(table, trial, selected=index == monitor.trial_index)
        body = table
    return titled_panel(body, "Trials", focused=monitor.focus == 1, border_style="trials.border")


def add_trial_row(table: Table, trial: Trial, *, selected: bool) -> None:
    cell_style = "selection" if selected else "muted"
    table.add_row(
        trial_label_text(trial, selected=selected),
        Text(format_duration(trial.duration_sec), style=cell_style),
        trial_tests_text(trial, selected=selected),
        Text(format_tokens(trial.tokens), style=cell_style),
    )


def trial_label_text(trial: Trial, *, selected: bool) -> Text:
    text = Text()
    base_style = "selection" if selected else status_style(trial.status)
    text.append(f"{status_icon(trial.status)} {trial.task_id} {trial.status}", style=base_style)
    if trial.status == "completed":
        tag, tag_style = trial_outcome_tag(trial)
        if tag:
            text.append(f" {tag}", style="selection" if selected else tag_style)
    return text


def trial_outcome_tag(trial: Trial) -> tuple[str, str]:
    # The bracketed tag after a completed trial. A batch DAB trial is a whole
    # dataset scored per-query, so it shows pass@1 + queries passed/total rather
    # than the binary [passed]/[failed] a per-query / ade trial gets.
    if trial.pass_at_1 is not None and trial.query_total:
        tag = f"[{trial.query_passed}/{trial.query_total} · pass@1 {format_pct(trial.pass_at_1)}]"
        return tag, batch_outcome_style(trial.pass_at_1)
    outcome = verify_outcome(trial.verify_result)
    if outcome:
        return f"[{outcome}]", verify_outcome_style(outcome)
    return "", ""


def batch_outcome_style(pass_at_1: float) -> str:
    if pass_at_1 >= 1.0:
        return "verify.pass"
    if pass_at_1 <= 0.0:
        return "verify.fail"
    return "verify.partial"


def append_trial_line(lines: Text, trial: Trial, *, selected: bool) -> None:
    lines.append_text(trial_label_text(trial, selected=selected))
    lines.append("\n")


def trial_tests_text(trial: Trial, *, selected: bool) -> Text:
    if trial.tests is None:
        return Text("-", style="selection" if selected else "muted")
    passed, total = trial.tests
    if selected:
        style = "selection"
    elif total > 0 and passed >= total:
        style = "verify.pass"
    elif passed < total:
        style = "verify.fail"
    else:
        style = "muted"
    return Text(f"{passed}/{total}", style=style)


def verify_outcome(verify_result: str) -> str:
    style = verify_style(verify_result)
    if style == "verify.pass":
        return "passed"
    if style == "verify.fail":
        return "failed"
    return ""


def verify_outcome_style(outcome: str) -> str:
    return "verify.pass" if outcome == "passed" else "verify.fail"


def render_trial_info_panel(
    trial: Trial | None,
    datasets: dict[str, DatasetInfo],
) -> Panel:
    if trial is None:
        return titled_panel(Text("No trial selected", style="muted"), "Trial Info")

    info = datasets.get(trial.task_id, DatasetInfo())
    rows: list[tuple[str, object, str]] = [
        ("Dataset", trial.task_id, "text"),
        ("Trial", trial.name, "text"),
        ("Status", trial.status, status_style(trial.status)),
        ("Verify", trial.verify_result, verify_style(trial.verify_result)),
        ("Agent", trial.agent_answer, "text"),
        ("Truth", trial.truth_summary, "text"),
        ("Diff", info.difficulty or "-", "text"),
        ("Desc", info.description or "-", "text"),
    ]
    if trial.path is not None:
        rows.append(("Path", str(trial.path), "text"))

    table = Table.grid(expand=True, padding=(0, 1), pad_edge=False)
    table.add_column(justify="right", no_wrap=True, style="muted")
    table.add_column(ratio=1)
    for label, value, style in rows:
        table.add_row(f"{label}:", Text(str(value), style=style))
    return titled_panel(table, "Trial Info")


def render_current_log_panel(monitor: Monitor, *, height: int) -> Panel:
    label, path, lines = monitor.log_view(max(0, height - 3))
    return render_log_panel(label, path, lines, scrolled=monitor.log_scroll)


def render_log_panel(
    label: str | None,
    path: Path | None,
    lines: list[str],
    *,
    scrolled: int,
) -> Panel:
    if label is None or path is None:
        return titled_panel(Text("No log source yet", style="muted"), "Trial Logs")

    entries = [parse_log_entry(label, line) for line in lines]
    prefix_width = aligned_log_prefix_width(entries)
    state = f"paused +{scrolled}, PgDn to follow" if scrolled else "live"
    rows = [Text(f"Log: {label} ({path})  [{state}]", style="log.header")]
    rows.extend(render_log_entry_text(entry, prefix_width) for entry in entries)
    title = f"Trial Logs (scrolled +{scrolled})" if scrolled else "Trial Logs"
    return titled_panel(Group(*rows), title)


def render_log_entry_text(entry: LogEntry, prefix_width: int | None = None) -> Text:
    if entry.raw:
        return Text(entry.raw, style="text")
    prefix_style = log_prefix_style(entry.state)
    if not entry.description:
        return Text(entry.prefix, style=prefix_style)

    width = prefix_width if prefix_width is not None else len(entry.prefix)
    text = Text()
    text.append(entry.prefix.ljust(width), style=prefix_style)
    text.append(" | ", style="log.separator")
    if entry.is_json:
        text.append_text(highlighted_json(entry.description))
    else:
        text.append(entry.description, style="text")
    return text


_JSON_HIGHLIGHTER = JSONHighlighter()


def highlighted_json(value: str) -> Text:
    text = Text(value, style="text")
    _JSON_HIGHLIGHTER.highlight(text)
    return text


def titled_panel(
    renderable: object,
    title: str,
    *,
    focused: bool = False,
    border_style: str = "panel.border",
) -> Panel:
    return Panel(
        renderable,
        title=Text(title, style="focus" if focused else "panel.title"),
        border_style="focus" if focused else border_style,
        box=box.SQUARE,
        expand=True,
    )


def append_line(text: Text, line: str, style: str) -> None:
    text.append(line, style=style)
    text.append("\n")


def status_style(status: str) -> str:
    if status == "running":
        return "status.running"
    if status == "pending":
        return "status.pending"
    if status == "errored":
        return "status.errored"
    if status in {"completed", "finished"}:
        return "status.complete"
    return "text"


def verify_style(verify_result: str) -> str:
    if verify_result.startswith("reward=1") or verify_result == "passed":
        return "verify.pass"
    if verify_result in {"not run", "pending"}:
        return "verify.pending"
    return "verify.fail"


def discover_jobs(runs_dir: Path) -> dict[str, list[Job]]:
    jobs_by_experiment: dict[str, list[Job]] = {}
    if not runs_dir.is_dir():
        return jobs_by_experiment

    for experiment_dir in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
        if experiment_dir.name.startswith("."):
            continue
        jobs = []
        for job_dir in sorted(p for p in experiment_dir.iterdir() if p.is_dir()):
            if not looks_like_job_dir(job_dir):
                continue
            jobs.append(build_job(experiment_dir.name, job_dir))
        if jobs:
            jobs.sort(key=lambda job: job.updated, reverse=True)
            jobs_by_experiment[experiment_dir.name] = jobs
    return jobs_by_experiment


def looks_like_job_dir(path: Path) -> bool:
    return any((path / name).exists() for name in ("_job_config.yaml", "config.json", "job.log", "lock.json"))


def build_job(experiment: str, job_dir: Path) -> Job:
    kind = dab_job_kind(job_dir)
    is_batch = kind == "dab-batch"
    if is_batch:
        pass_at_1 = job_batch_pass_at_1(job_dir)
        query_passed, query_total = job_batch_query_counts(job_dir) or (None, None)
    else:
        pass_at_1 = job_macro_pass_at_1(job_dir)
        query_passed = query_total = None
    return Job(
        experiment=experiment,
        path=job_dir,
        updated=job_updated_mtime(job_dir),
        status=shallow_job_status(job_dir),
        trials=[],
        progress=job_progress(job_dir),
        passed=job_pass_count(job_dir),
        is_dab=kind != "ade",
        is_batch_dab=is_batch,
        pass_at_1=pass_at_1,
        query_passed=query_passed,
        query_total=query_total,
    )


def dab_job_kind(job_dir: Path) -> str:
    # Classify a job by its first trial dir: "ade" (flat agent/verifier),
    # "dab" (per-query, nested under steps/<step>/, trial id "<dataset>-q<N>"),
    # or "dab-batch" (one trial per whole dataset, bare "<dataset>" trial id,
    # fractional reward = the dataset's pass@1). A job is uniformly one benchmark,
    # so the first trial decides. Cheap enough to recompute for every sidebar row.
    try:
        for path in job_dir.iterdir():
            if path.is_dir() and "__" in path.name:
                if not (path / "steps").is_dir():
                    return "ade"
                task_id = path.name.split("__", 1)[0]
                return "dab" if re.search(r"-q\d+$", task_id) else "dab-batch"
    except OSError:
        return "ade"
    return "ade"


def job_is_dab(job_dir: Path) -> bool:
    return dab_job_kind(job_dir) != "ade"


def job_progress(job_dir: Path) -> tuple[int, int] | None:
    # (completed, total) for a job, cheap enough to compute for every sidebar
    # row. Prefer result.json's authoritative counts; before it exists, fall
    # back to the configured task count so a just-started run still shows N/total.
    result = read_json(job_dir / "result.json")
    if result:
        total = result.get("n_total_trials")
        completed = (result.get("stats") or {}).get("n_completed_trials")
        if isinstance(total, int) and total > 0 and isinstance(completed, int):
            return completed, total
    task_count = len(list(configured_task_paths(job_dir)))
    if task_count > 0:
        return 0, task_count
    return None


def job_pass_count(job_dir: Path) -> int | None:
    # Number of trials that passed verification (reward >= 1.0), summed across
    # all evals in result.json. result.json accumulates reward_stats as trials
    # complete, so this is correct for running jobs too. Returns None when no
    # result.json exists yet (so the sidebar can omit the count entirely).
    result = read_json(job_dir / "result.json")
    if not result:
        return None
    evals = (result.get("stats") or {}).get("evals")
    if not isinstance(evals, dict):
        return None
    passed = 0
    for eval_data in evals.values():
        if not isinstance(eval_data, dict):
            continue
        reward_stats = eval_data.get("reward_stats")
        reward = reward_stats.get("reward") if isinstance(reward_stats, dict) else None
        if not isinstance(reward, dict):
            continue
        for value, trial_ids in reward.items():
            if not isinstance(trial_ids, list):
                continue
            try:
                if float(value) >= 1.0:
                    passed += len(trial_ids)
            except (TypeError, ValueError):
                continue
    return passed


def job_macro_pass_at_1(job_dir: Path) -> float | None:
    # Stratified macro-average pass@1: every dataset weighted equally, not every
    # trial. Group the per-trial rewards in result.json by dataset (the trial-id
    # prefix, e.g. googlelocal-q1 -> googlelocal), take each dataset's pass rate
    # (reward >= 1.0), then average those rates. Returns None before any rewards.
    result = read_json(job_dir / "result.json")
    if not result:
        return None
    evals = (result.get("stats") or {}).get("evals")
    if not isinstance(evals, dict):
        return None
    groups: dict[str, list[int]] = {}  # dataset -> [passed, total]
    for eval_data in evals.values():
        if not isinstance(eval_data, dict):
            continue
        reward_stats = eval_data.get("reward_stats")
        reward = reward_stats.get("reward") if isinstance(reward_stats, dict) else None
        if not isinstance(reward, dict):
            continue
        for value, trial_ids in reward.items():
            if not isinstance(trial_ids, list):
                continue
            try:
                is_pass = float(value) >= 1.0
            except (TypeError, ValueError):
                continue
            for trial_id in trial_ids:
                if not isinstance(trial_id, str):
                    continue
                bucket = groups.setdefault(dataset_from_trial_id(trial_id), [0, 0])
                bucket[1] += 1
                if is_pass:
                    bucket[0] += 1
    rates = [passed / total for passed, total in groups.values() if total > 0]
    if not rates:
        return None
    return sum(rates) / len(rates)


def dataset_from_trial_id(trial_id: str) -> str:
    # A DAB trial id is "<dataset>-q<N>__<suffix>"; the dataset is the task id
    # with the query suffix stripped. Verified to match stratum.json's dataset.
    task_id = trial_id.split("__", 1)[0]
    return re.sub(r"-q\d+$", "", task_id)


def job_batch_pass_at_1(job_dir: Path) -> float | None:
    # Stratified pass@1 for a batch DAB job: every dataset weighted equally. Each
    # trial is one whole dataset whose reward is already that dataset's pass rate,
    # so this is the mean of the per-dataset rewards.
    #
    # Numerator = Σ rewards from result.json's reward_stats.reward (value ->
    # [trial-ids]). Denominator = every dataset that has *run* (completed +
    # errored), NOT just the rewarded ones -- so a dataset that finished without a
    # reward (verifier abstained / degraded, e.g. PATENTS) counts as 0 and the
    # slate of 12 stays 12, not 11. Falls back to the rewarded count when the
    # trial-state stats are missing. None before any dataset has a reward.
    result = read_json(job_dir / "result.json")
    if not result:
        return None
    stats = result.get("stats") or {}
    evals = stats.get("evals")
    if not isinstance(evals, dict):
        return None
    total_reward = 0.0
    rewarded = 0
    for eval_data in evals.values():
        reward_stats = eval_data.get("reward_stats") if isinstance(eval_data, dict) else None
        reward = reward_stats.get("reward") if isinstance(reward_stats, dict) else None
        if not isinstance(reward, dict):
            continue
        for value, trial_ids in reward.items():
            if not isinstance(trial_ids, list):
                continue
            try:
                v = float(value)
            except (TypeError, ValueError):
                continue
            total_reward += v * len(trial_ids)
            rewarded += len(trial_ids)
    if rewarded == 0:
        return None
    ran = 0
    for key in ("n_completed_trials", "n_errored_trials"):
        count = stats.get(key)
        if isinstance(count, int):
            ran += count
    return total_reward / max(ran, rewarded)


def job_batch_query_counts(job_dir: Path) -> tuple[int, int] | None:
    # (passed_queries, total_queries) for a batch DAB job. A batch trial scores
    # every query in its dataset, recording the breakdown in
    # steps/<step>/verifier/reward_per_query.json; passed = queries with
    # reward >= 1.0 summed across trials. Total is the full slate from each
    # configured task's tests/stratum.json (known from t=0), falling back to the
    # queries observed so far if no stratum is readable. None when nothing graded.
    try:
        trial_dirs = [p for p in job_dir.iterdir() if p.is_dir() and "__" in p.name]
    except OSError:
        return None
    passed = 0
    observed = 0
    graded = False
    for trial_dir in trial_dirs:
        per_query = trial_reward_per_query(trial_dir)
        if per_query is None:
            continue
        graded = True
        for entry in per_query.values():
            observed += 1
            reward = entry.get("reward") if isinstance(entry, dict) else None
            try:
                if float(reward) >= 1.0:
                    passed += 1
            except (TypeError, ValueError):
                continue
    total = job_batch_total_queries(job_dir)
    if total is None:
        total = observed
    if not graded and total == 0:
        return None
    return passed, total


def job_batch_total_queries(job_dir: Path) -> int | None:
    # Total queries on a batch slate: sum of query_ids across the configured
    # tasks' tests/stratum.json. Available before any trial finishes, so the
    # denominator is the full slate even early in a running job. None if no
    # stratum is readable.
    total = 0
    found = False
    for task_path in configured_task_paths(job_dir):
        stratum = read_json(task_path / "tests" / "stratum.json")
        inner = stratum.get("stratum") if isinstance(stratum, dict) else None
        query_ids = inner.get("query_ids") if isinstance(inner, dict) else None
        if isinstance(query_ids, list):
            total += len(query_ids)
            found = True
    return total if found else None


def trial_reward_per_query(trial_dir: Path) -> dict | None:
    # The per-query reward breakdown a batch DAB trial writes to
    # verifier/reward_per_query.json under each step root: {q: {reward, reason}}.
    # Merges across step roots. None when no such file exists (per-query / ade).
    merged: dict = {}
    found = False
    for root in step_roots(trial_dir):
        data = read_json(root / "verifier" / "reward_per_query.json")
        if isinstance(data, dict) and data:
            found = True
            merged.update(data)
    return merged if found else None


def trial_batch_outcome(trial_dir: Path) -> tuple[float | None, int | None, int | None]:
    # For a batch DAB trial (one whole dataset), return its
    # (pass@1, queries_passed, queries_total). pass@1 is the verifier reward
    # (the dataset's pass rate); the query counts come from
    # reward_per_query.json. (None, None, None) for per-query / ade trials, which
    # have no reward_per_query.json.
    per_query = trial_reward_per_query(trial_dir)
    if per_query is None:
        return None, None, None
    passed = 0
    for entry in per_query.values():
        reward = entry.get("reward") if isinstance(entry, dict) else None
        try:
            if float(reward) >= 1.0:
                passed += 1
        except (TypeError, ValueError):
            continue
    total = len(per_query)
    pass_at_1 = trial_reward_value(trial_dir)
    if pass_at_1 is None and total > 0:
        pass_at_1 = passed / total
    return pass_at_1, passed, total


def trial_reward_value(trial_dir: Path) -> float | None:
    # The trial's overall verifier reward (verifier_result.rewards.reward) as a
    # float, or None when absent / non-numeric.
    result = read_json(trial_dir / "result.json")
    verifier_result = result.get("verifier_result") if isinstance(result, dict) else None
    rewards = verifier_result.get("rewards") if isinstance(verifier_result, dict) else None
    reward = rewards.get("reward") if isinstance(rewards, dict) else None
    try:
        return float(reward)
    except (TypeError, ValueError):
        return None


def discover_trials(job_dir: Path) -> list[Trial]:
    # Harbor truncates long cell-dir names (e.g. `…analytics_engineering001`
    # becomes `…analytics_engineerin`), so a trial dir's `<task-id>__…` prefix can
    # be a shortened form of the configured task name. Canonicalize it back to the
    # full configured name; otherwise the reconciliation below fabricates a phantom
    # "pending" trial for a long-named task that actually ran.
    configured_names = [task_path.name for task_path in configured_task_paths(job_dir)]
    canonical_task_id = make_canonical_task_id(configured_names)

    trials = []
    for trial_dir in sorted(p for p in job_dir.iterdir() if p.is_dir() and "__" in p.name):
        task_id = canonical_task_id(trial_dir.name.split("__", 1)[0])
        status = trial_status(trial_dir)
        pass_at_1, query_passed, query_total = trial_batch_outcome(trial_dir)
        trials.append(
            Trial(
                name=trial_dir.name,
                path=trial_dir,
                task_id=task_id,
                status=status,
                verify_result=trial_verify_result(trial_dir),
                agent_answer=trial_agent_answer(trial_dir),
                truth_summary=trial_truth_summary(trial_dataset_path(trial_dir)),
                log_sources=trial_log_sources(trial_dir),
                duration_sec=trial_duration_sec(trial_dir, status),
                tests=trial_test_counts(trial_dir),
                tokens=trial_token_count(trial_dir),
                pass_at_1=pass_at_1,
                query_passed=query_passed,
                query_total=query_total,
            )
        )

    existing_tasks = {trial.task_id for trial in trials}
    for task_path in configured_task_paths(job_dir):
        task_id = task_path.name
        if task_id not in existing_tasks:
            trials.append(
                Trial(
                    name=f"{task_id}__pending",
                    path=None,
                    task_id=task_id,
                    status="pending",
                    verify_result="pending",
                    agent_answer="pending",
                    truth_summary=trial_truth_summary(task_path),
                    log_sources=[],
                )
            )

    trials.sort(key=lambda trial: (status_sort_key(trial.status), trial.task_id))
    return trials


def make_canonical_task_id(configured_names: list[str]) -> Callable[[str], str]:
    """Return a mapper from a (possibly Harbor-truncated) cell-dir task id to the
    full configured task name.

    Harbor truncates long trial-dir names, so a cell's `<task-id>` can be a strict
    prefix of the real task name. Map it back when EXACTLY ONE configured name has
    that prefix and the prefix is not itself a configured name (so a genuinely
    short task like `foo` never shadows a longer `foobar001`). Ambiguous or
    unmatched ids pass through unchanged, so genuinely-missing trials still surface
    as pending."""
    configured_set = set(configured_names)

    def canonical(raw: str) -> str:
        if raw in configured_set:
            return raw
        matches = [name for name in configured_names if name != raw and name.startswith(raw)]
        return matches[0] if len(matches) == 1 else raw

    return canonical


def configured_task_paths(job_dir: Path) -> Iterable[Path]:
    config_path = job_dir / "config.json"
    if not config_path.is_file():
        return []
    try:
        payload = json.loads(config_path.read_text())
    except (json.JSONDecodeError, OSError):
        return []
    paths = []
    for task in payload.get("tasks") or []:
        raw = task.get("path") if isinstance(task, dict) else None
        if raw:
            paths.append(Path(raw))
    return paths


def trial_status(trial_dir: Path) -> str:
    result = read_json(trial_dir / "result.json")
    if result:
        if result.get("exception_info"):
            return "errored"
        if result.get("verifier_result") is not None or result.get("agent_result") is not None:
            return "completed"
        return "finished"
    if (trial_dir / "exception.txt").exists():
        return "errored"
    return "running"


def trial_verify_result(trial_dir: Path) -> str:
    result = read_json(trial_dir / "result.json")
    if not result:
        return "pending"
    verifier_result = result.get("verifier_result")
    if verifier_result is None:
        return "not run"
    rewards = verifier_result.get("rewards") if isinstance(verifier_result, dict) else None
    if isinstance(rewards, dict) and "reward" in rewards:
        return f"reward={rewards['reward']}"
    if isinstance(verifier_result, dict):
        return compact_json(verifier_result)
    return str(verifier_result)


def dab_answers_json_value(trial_dir: Path) -> str | None:
    # DAB tasks write /workspace/answers.json as {"answer": "<str>"}. The file
    # is not persisted, but codex's apply_patch records the written content in a
    # patch_apply_end event in the session rollout. Return the last answer
    # written across all steps, or None when there is no such write (ade-bench).
    content: str | None = None
    for root in content_roots(trial_dir):
        sessions_dir = root / "agent" / "sessions"
        if not sessions_dir.is_dir():
            continue
        for path in sorted(sessions_dir.rglob("rollout-*.jsonl")):
            written = answers_json_from_rollout(path)
            if written is not None:
                content = written
    if content is None:
        return None
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, TypeError):
        return one_line(content)
    if isinstance(data, dict) and "answer" in data:
        return one_line(str(data["answer"]))
    return one_line(content)


def answers_json_from_rollout(path: Path) -> str | None:
    # Scan a session rollout for the last patch_apply_end that wrote a file
    # named answers.json and return its content. Lines are pre-filtered on the
    # substrings so we only JSON-parse the (rare) relevant records.
    written: str | None = None
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for line in lines:
        if "answers.json" not in line or "patch_apply_end" not in line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = event.get("payload") if isinstance(event, dict) else None
        if not isinstance(payload, dict) or payload.get("type") != "patch_apply_end":
            continue
        changes = payload.get("changes")
        if not isinstance(changes, dict):
            continue
        for file_path, change in changes.items():
            if file_path.endswith("answers.json") and isinstance(change, dict):
                value = change.get("content")
                if isinstance(value, str):
                    written = value
    return written


def trial_agent_answer(trial_dir: Path) -> str:
    # DAB's contract is an explicit answers.json value -- prefer it when present.
    answer = dab_answers_json_value(trial_dir)
    if answer is not None:
        return answer
    # Otherwise (ade-bench, or a still-running DAB step) read the last
    # transcript: the agent's final message, or a summary of its changed files.
    path = None
    for root in content_roots(trial_dir):
        candidate = root / "agent" / "codex.txt"
        if candidate.is_file():
            path = candidate
    if path is None:
        return "-"
    latest = ""
    for line in tail_lines(path, 200):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item") if isinstance(event, dict) else None
        if not isinstance(item, dict) or item.get("type") != "agent_message":
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            latest = text
    if not latest:
        return "-"
    changed = changed_files_summary(latest)
    if changed:
        return changed
    for line in latest.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned
    return "-"


def changed_files_summary(text: str) -> str:
    in_section = False
    files = []
    for line in text.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if lower.startswith("changed files"):
            in_section = True
            continue
        if in_section and not stripped:
            if files:
                break
            continue
        if in_section and not stripped.startswith("-"):
            if files:
                break
            continue
        if not in_section or not stripped.startswith("-"):
            continue
        file_name = changed_file_name(stripped)
        if file_name:
            files.append(file_name)
    if not files:
        return ""
    shown = ", ".join(files[:4])
    if len(files) > 4:
        shown = f"{shown}, +{len(files) - 4}"
    return f"changed: {shown}"


def changed_file_name(line: str) -> str:
    link_match = re.search(r"\[([^\]]+)\]\(", line)
    if link_match:
        return Path(link_match.group(1)).name
    path_match = re.search(r"(/app/[^\s:`]+)", line)
    if path_match:
        return Path(path_match.group(1)).name
    raw = line.lstrip("-").strip().split(":", 1)[0].strip("` ")
    return Path(raw).name if raw else ""


def trial_dataset_path(trial_dir: Path) -> Path | None:
    result = read_json(trial_dir / "result.json")
    if not result:
        result = read_json(trial_dir / "config.json")
    raw = None
    task_id = result.get("task_id")
    if isinstance(task_id, dict):
        raw = task_id.get("path")
    if raw is None:
        config = result.get("config")
        task = config.get("task") if isinstance(config, dict) else None
        raw = task.get("path") if isinstance(task, dict) else None
    return Path(raw) if raw else None


def trial_truth_summary(dataset_path: Path | None) -> str:
    if dataset_path is None or not dataset_path.is_dir():
        return "-"
    # DAB tasks carry the actual expected answer as a `ground_truth` literal in
    # tests/validate.py -- show it directly when present.
    ground_truth = validate_ground_truth(dataset_path)
    if ground_truth:
        return ground_truth
    parts = []
    solution_dir = dataset_path / "solution"
    if (solution_dir / "solution.sh").is_file():
        parts.append("solution/solution.sh")
    elif solution_dir.is_dir():
        parts.append(f"solution:{count_files(solution_dir)} files")
    tests_dir = dataset_path / "tests"
    test_count = count_matching(tests_dir, "*.sql")
    seed_count = count_matching(tests_dir / "seeds", "solution__*.csv")
    if test_count:
        parts.append(f"{test_count} tests")
    if seed_count:
        parts.append(f"{seed_count} seeds")
    return "; ".join(parts) if parts else "-"


def validate_ground_truth(dataset_path: Path) -> str | None:
    # Extract the `ground_truth` literal assigned in tests/validate.py (a DAB
    # task) and render it as the ordered list of expected names. Returns None if
    # there is no validate.py or no literal ground_truth (e.g. one loaded from a
    # CSV, or an ade-bench dataset).
    validate_py = dataset_path / "tests" / "validate.py"
    if not validate_py.is_file():
        return None
    try:
        tree = ast.parse(validate_py.read_text(encoding="utf-8", errors="replace"))
    except (OSError, SyntaxError, ValueError):
        return None
    value = ground_truth_literal(tree)
    if value is None:
        return None
    return format_ground_truth(value)


def ground_truth_literal(tree: ast.AST) -> object | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        if any(isinstance(t, ast.Name) and t.id == "ground_truth" for t in targets):
            try:
                return ast.literal_eval(node.value)
            except (ValueError, SyntaxError, TypeError):
                return None
    return None


def format_ground_truth(value: object) -> str:
    # The validators key on names in order; show those. Each item is either a
    # name string or a (name, ...) tuple/list whose first element is the name.
    if isinstance(value, (list, tuple)):
        names = []
        for item in value:
            if isinstance(item, (list, tuple)) and item:
                names.append(str(item[0]))
            else:
                names.append(str(item))
        return "; ".join(names)
    return str(value)


def trial_duration_sec(trial_dir: Path, status: str) -> float | None:
    # Wall-clock from started_at to finished_at. While a trial is still running
    # there is no finished_at yet, so fall back to "now" for a live elapsed time.
    result = read_json(trial_dir / "result.json")
    if not result:
        return None
    start = parse_iso(result.get("started_at"))
    if start is None:
        return None
    end = parse_iso(result.get("finished_at"))
    if end is None:
        if status != "running":
            return None
        end = datetime.now(timezone.utc)
    return max(0.0, (end - start).total_seconds())


def trial_test_counts(trial_dir: Path) -> tuple[int, int] | None:
    # (passed, total) parsed from the final dbt test summary in the verifier
    # stdout. The build phase emits earlier summaries too, so the last match in
    # the file is the one for the test run.
    passed = total = None
    for root in content_roots(trial_dir):
        for line in tail_lines(root / "verifier" / "test-stdout.txt", 200):
            match = TEST_SUMMARY_RE.search(line)
            if match:
                passed, total = int(match.group(1)), int(match.group(2))
    if passed is None or total is None:
        return None
    return passed, total


def trial_token_count(trial_dir: Path) -> int | None:
    # Total agent tokens (input + output). Some agents do not report usage, in
    # which case every count is None and we return None so the column shows "-".
    result = read_json(trial_dir / "result.json")
    agent_result = result.get("agent_result") if result else None
    if not isinstance(agent_result, dict):
        return None
    total = 0
    found = False
    for key in ("n_input_tokens", "n_output_tokens"):
        value = agent_result.get(key)
        if isinstance(value, int):
            total += value
            found = True
    return total if found else None


def parse_iso(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def job_status(job_dir: Path, trials: list[Trial]) -> str:
    result = read_json(job_dir / "result.json")
    if result:
        stats = result.get("stats") or {}
        if stats.get("n_running_trials", 0):
            return "running"
        if stats.get("n_pending_trials", 0):
            return "running"
        if result.get("finished_at"):
            if stats.get("n_errored_trials", 0):
                return "errored"
            return "finished"
    if any(trial.status == "running" for trial in trials):
        return "running"
    if trials and all(trial.status in {"completed", "finished", "errored"} for trial in trials):
        return "finished"
    return "pending"


def shallow_job_status(job_dir: Path) -> str:
    result = read_json(job_dir / "result.json")
    if result:
        stats = result.get("stats") or {}
        if stats.get("n_running_trials", 0) or stats.get("n_pending_trials", 0):
            return "running"
        if result.get("finished_at"):
            if stats.get("n_errored_trials", 0):
                return "errored"
            return "finished"
    if (job_dir / "lock.json").exists():
        return "running"
    return "pending"


def step_roots(trial_dir: Path) -> list[Path]:
    # The dirs that hold agent/ and verifier/ for a trial. DAB nests them under
    # steps/<step>/ (one per pipeline step); ade-bench keeps them flat in the
    # trial dir. Returns the step dirs (sorted) for DAB, else [trial_dir].
    steps_dir = trial_dir / "steps"
    if steps_dir.is_dir():
        steps = sorted(p for p in steps_dir.iterdir() if p.is_dir())
        if steps:
            return steps
    return [trial_dir]


def content_roots(trial_dir: Path) -> list[Path]:
    # Step roots plus the trial dir itself. While a DAB trial runs, codex writes
    # the live transcript to the trial-root agent/ and only moves it into
    # steps/<step>/agent/ when the step finishes -- so the trial root must be
    # searched too. It contributes nothing once the move has happened (the
    # trial-root agent/ is gone), so this never duplicates the finished logs.
    roots = step_roots(trial_dir)
    if trial_dir not in roots:
        roots = roots + [trial_dir]
    return roots


def trial_log_sources(trial_dir: Path) -> list[tuple[str, Path]]:
    sources: list[tuple[str, Path]] = []
    for root in content_roots(trial_dir):
        # Step dirs get a step-name prefix so they don't collide; the trial
        # root (flat layout, or the live transcript) keeps bare labels.
        prefix = "" if root == trial_dir else f"{root.name}:"
        for label, relative in STEP_LOG_CANDIDATES:
            path = root / relative
            if path.exists() and all(path != known for _, known in sources):
                sources.append((f"{prefix}{label}", path))
        agent_dir = root / "agent"
        if agent_dir.is_dir():
            for path in sorted(agent_dir.glob("*.txt")) + sorted(agent_dir.glob("*.log")):
                if all(path != known for _, known in sources):
                    sources.append((f"{prefix}{path.name}", path))
        for source in session_log_sources(root, trial_dir, prefix):
            if all(source[1] != known for _, known in sources):
                sources.append(source)
    # Trial-root logs come last so the agent transcript stays the default.
    for label, relative in TRIAL_ROOT_LOGS:
        path = trial_dir / relative
        if path.exists() and all(path != known for _, known in sources):
            sources.append((label, path))
    return sources


def session_log_sources(root: Path, trial_dir: Path, prefix: str = "") -> list[tuple[str, Path]]:
    # Spacedock writes one Codex session per agent under <root>/agent/sessions:
    # the parent first-officer (thread_source=user) plus each dispatched worker
    # (thread_source=subagent). agent/codex.txt is the rendered parent, but the
    # raw session JSONL carries event-level detail the transcript drops, so we
    # surface the parent session as well as the workers. The subagent-type
    # manifest lives at the trial root in both layouts.
    sessions_dir = root / "agent" / "sessions"
    if not sessions_dir.is_dir():
        return []
    parents: list[Path] = []
    subagents: list[Path] = []
    for path in sorted(sessions_dir.rglob("rollout-*.jsonl")):
        source = rollout_thread_source(path)
        if source == "subagent":
            subagents.append(path)
        elif source == "user":
            parents.append(path)
    sources: list[tuple[str, Path]] = []
    for index, path in enumerate(parents):
        label = "session:first-officer" if len(parents) == 1 else f"session:first-officer#{index}"
        sources.append((f"{prefix}{label}", path))
    types = subagent_types_from_manifest(trial_dir)
    for index, path in enumerate(subagents):
        subagent_type = types[index] if index < len(types) else None
        short = subagent_type.split(":")[-1] if subagent_type else None
        label = f"subagent:{short}#{index}" if short else f"subagent#{index}"
        sources.append((f"{prefix}{label}", path))
    return sources


def rollout_thread_source(path: Path) -> str | None:
    # The session_meta record is the first line of a rollout-*.jsonl file.
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            first_line = handle.readline()
    except OSError:
        return None
    try:
        record = json.loads(first_line)
    except json.JSONDecodeError:
        return None
    payload = record.get("payload") if isinstance(record, dict) else None
    if isinstance(payload, dict):
        return payload.get("thread_source")
    return None


def subagent_types_from_manifest(trial_dir: Path) -> list[str | None]:
    manifest = read_json(trial_dir / "subagent-trace-manifest.json")
    dispatches = manifest.get("dispatches") if manifest else None
    if not isinstance(dispatches, list):
        return []
    ordered = sorted(
        (dispatch for dispatch in dispatches if isinstance(dispatch, dict)),
        key=lambda dispatch: dispatch.get("spawn_index", 0),
    )
    return [dispatch.get("subagent_type") for dispatch in ordered]


def read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def job_updated_mtime(job_dir: Path) -> float:
    mtimes = [path_mtime(job_dir)]
    mtimes.extend(path_mtime(job_dir / relative) for relative in JOB_ACTIVITY_FILES)
    return max(mtimes)


def job_trial_signature(job_dir: Path) -> tuple[object, ...]:
    parts: list[object] = [file_signature(job_dir / relative) for relative in JOB_ACTIVITY_FILES]
    try:
        trial_dirs = sorted(p for p in job_dir.iterdir() if p.is_dir() and "__" in p.name)
    except OSError:
        return tuple(parts)
    for trial_dir in trial_dirs:
        parts.append((trial_dir.name, path_mtime_ns(trial_dir)))
        parts.extend(file_signature(trial_dir / relative) for relative in TRIAL_ACTIVITY_FILES)
        # Watch each content root's agent/ + step logs so both DAB's nested
        # steps/<step>/ content and the live trial-root transcript (which a
        # running step writes there) invalidate the trial cache when they change.
        for root in content_roots(trial_dir):
            parts.append(file_signature(root / "agent"))
            parts.extend(file_signature(root / relative) for _label, relative in STEP_LOG_CANDIDATES)
    return tuple(parts)


def file_signature(path: Path) -> tuple[str, bool, int, int]:
    try:
        stat = path.stat()
    except OSError:
        return (path.as_posix(), False, 0, 0)
    return (path.as_posix(), True, stat.st_mtime_ns, stat.st_size)


def path_mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def path_mtime_ns(path: Path) -> int:
    try:
        return path.stat().st_mtime_ns
    except OSError:
        return 0


def load_dataset_info(path: Path) -> dict[str, DatasetInfo]:
    if not path.is_file():
        return {}
    info = {}
    row_re = re.compile(r"^\| `([^`]+)` \| ([^|]+) \| ([^|]+) \|$")
    for line in path.read_text().splitlines():
        match = row_re.match(line.strip())
        if not match:
            continue
        dataset, difficulty, description = match.groups()
        if dataset == "Dataset":
            continue
        info[dataset] = DatasetInfo(
            difficulty=difficulty.strip(),
            description=description.strip(),
        )
    return info


def read_last_lines(path: Path, count: int) -> tuple[list[str], bool]:
    # Read at least `count` complete lines from the end of the file, walking
    # backwards in blocks. Returns the decoded lines (the first may be partial
    # unless the file start was reached) and whether the start was reached.
    try:
        with path.open("rb") as fh:
            fh.seek(0, 2)
            size = fh.tell()
            block = 4096
            data = b""
            while size > 0 and data.count(b"\n") <= count:
                read_size = min(block, size)
                size -= read_size
                fh.seek(size)
                data = fh.read(read_size) + data
        return data.decode("utf-8", errors="replace").splitlines(), size == 0
    except OSError:
        return [], True


def tail_lines(path: Path, count: int) -> list[str]:
    if count <= 0 or not path.is_file():
        return []
    lines, _reached_start = read_last_lines(path, count)
    return lines[-count:]


def read_log_window(path: Path, count: int, scroll: int) -> tuple[list[str], int]:
    # Return the `count` lines ending `scroll` lines above the bottom, plus the
    # scroll value clamped to the file. scroll=0 is the live tail.
    if count <= 0 or not path.is_file():
        return [], 0
    scroll = max(0, scroll)
    lines, reached_start = read_last_lines(path, scroll + count)
    if reached_start:
        scroll = min(scroll, max(0, len(lines) - count))
    end = len(lines) - scroll
    start = max(0, end - count)
    return lines[start:end], scroll


def clean_line(line: str) -> str:
    return line.replace("\t", "  ")


def format_log_line(label: str, line: str) -> str:
    return render_log_entry(parse_log_entry(label, line))


def format_log_lines(label: str, lines: Iterable[str]) -> list[str]:
    entries = [parse_log_entry(label, line) for line in lines]
    prefix_width = aligned_log_prefix_width(entries)
    return [render_log_entry(entry, prefix_width) for entry in entries]


def parse_log_entry(label: str, line: str) -> LogEntry:
    cleaned = clean_line(line)
    event = parse_json_log_event(cleaned)
    if event is None:
        return LogEntry("", "", cleaned)
    event_type = event.get("type")
    if not isinstance(event_type, str) or not event_type:
        return LogEntry("", "", cleaned)
    payload = event.get("payload")
    if isinstance(payload, dict):
        return parse_rollout_entry(event_type, payload)
    item = event.get("item")
    item_type = item.get("type") if isinstance(item, dict) else None
    prefix = item_type if isinstance(item_type, str) and item_type else event_type
    description, is_json = describe_log_event(event_type, event, item)
    state = log_state(event_type, item)
    return LogEntry(prefix, description, state=state, is_json=is_json)


def log_state(event_type: str, item: object) -> str:
    item_type = item.get("type") if isinstance(item, dict) else None
    if event_type == "error" or item_type == "error":
        return "error"
    if item_type == "command_execution" and isinstance(item, dict):
        exit_code = item.get("exit_code")
        if exit_code not in (None, 0):
            return "error"
    if event_type.endswith(".started"):
        return "started"
    if event_type.endswith(".completed"):
        return "completed"
    return ""


def log_prefix_style(state: str) -> str:
    return {
        "started": "log.started",
        "completed": "log.completed",
        "error": "log.error",
    }.get(state, "log.type")


def aligned_log_prefix_width(entries: Iterable[LogEntry]) -> int:
    return max(
        (len(entry.prefix) for entry in entries if entry.prefix and entry.description),
        default=0,
    )


def render_log_entry(entry: LogEntry, prefix_width: int | None = None) -> str:
    if entry.raw:
        return entry.raw
    if not entry.description:
        return entry.prefix
    width = prefix_width if prefix_width is not None else len(entry.prefix)
    return f"{entry.prefix.ljust(width)} | {entry.description}"


def parse_json_log_event(line: str) -> dict | None:
    if not line.startswith("{"):
        return None
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        return None
    return event if isinstance(event, dict) else None


def describe_log_event(event_type: str, event: dict, item: object) -> tuple[str, bool]:
    # Returns (description, is_json). The prefix already names the event/item
    # type, so descriptions never repeat it. is_json flags leftover payloads
    # that should be rendered with JSON syntax highlighting.
    if isinstance(item, dict) and isinstance(item.get("type"), str) and item.get("type"):
        return describe_log_item(item)
    if event_type == "thread.started":
        return one_line(event.get("thread_id")) if event.get("thread_id") else "", False
    if event_type == "turn.started":
        return "", False
    if event_type == "turn.completed":
        return turn_usage_summary(event), False
    message = event.get("message")
    if isinstance(message, str) and message.strip():
        return one_line(message), False
    return compact_json({key: value for key, value in event.items() if key != "type"}), True


def turn_usage_summary(event: dict) -> str:
    usage = event.get("usage")
    if not isinstance(usage, dict):
        return ""
    parts = []
    for source, label in (
        ("input_tokens", "input"),
        ("cached_input_tokens", "cached"),
        ("output_tokens", "output"),
    ):
        value = usage.get(source)
        if value is not None:
            parts.append(f"{label}={value}")
    return " ".join(parts)


def describe_log_item(item: dict) -> tuple[str, bool]:
    item_type = item.get("type")
    if item_type == "agent_message":
        return one_line(item.get("text")), False
    if item_type == "command_execution":
        return command_execution_summary(item), False
    if item_type == "file_change":
        return file_change_summary(item.get("changes")), False
    if item_type in {"tool_call", "function_call"}:
        return tool_call_summary(item), False
    if item_type in {"tool_call_output", "function_call_output"}:
        return one_line(item.get("output") or item.get("content")), False
    if item_type == "error":
        return one_line(item.get("message") or item.get("text")), False
    if item_type == "reasoning":
        return one_line(item.get("summary") or item.get("text")), False
    return compact_json({key: value for key, value in item.items() if key != "type"}), True


def command_execution_summary(item: dict) -> str:
    command = one_line(item.get("command"))
    exit_code = item.get("exit_code")
    if exit_code not in (None, 0):
        return f"{command} (exit {exit_code})"
    return command


def file_change_summary(changes: object) -> str:
    if not isinstance(changes, list) or not changes:
        return "-"
    names = []
    for change in changes:
        raw = change.get("path") if isinstance(change, dict) else None
        if raw:
            names.append(Path(raw).name)
    if not names:
        return "-"
    shown = ", ".join(names[:4])
    if len(names) > 4:
        shown = f"{shown}, +{len(names) - 4}"
    label = "file" if len(names) == 1 else "files"
    return f"{len(names)} {label}: {shown}"


def tool_call_summary(item: dict) -> str:
    name = item.get("name") or item.get("tool_name") or item.get("function_name")
    arguments = item.get("arguments") or item.get("args")
    if isinstance(arguments, str):
        arguments = one_line(arguments)
    elif arguments is not None:
        arguments = compact_json(arguments)
    if name and arguments:
        return f"{name} {arguments}"
    if name:
        return str(name)
    if arguments:
        return str(arguments)
    return compact_json(item)


def parse_rollout_entry(record_type: str, payload: dict) -> LogEntry:
    # Subagent rollout-*.jsonl records wrap their data in `payload` with its own
    # `type`, unlike codex.txt's `item` shape. Map the common ones to readable
    # descriptions so subagent logs render like the parent transcript.
    payload_type = payload.get("type")
    prefix = payload_type if isinstance(payload_type, str) and payload_type else record_type
    description, is_json = describe_rollout_payload(payload_type, payload)
    return LogEntry(prefix, description, state=rollout_state(payload_type), is_json=is_json)


def describe_rollout_payload(payload_type: object, payload: dict) -> tuple[str, bool]:
    if payload_type in {"agent_message", "user_message"}:
        return one_line(payload.get("message")), False
    if payload_type == "message":
        return one_line(rollout_join_text(payload.get("content")) or payload.get("text")), False
    if payload_type == "reasoning":
        return one_line(rollout_join_text(payload.get("summary"))), False
    if payload_type in {"function_call", "custom_tool_call"}:
        return rollout_tool_call_summary(payload), False
    if payload_type in {"function_call_output", "custom_tool_call_output"}:
        return one_line(payload.get("output") or payload.get("content")), False
    if payload_type == "token_count":
        return rollout_token_summary(payload), False
    if payload_type == "task_complete":
        return one_line(payload.get("last_agent_message")), False
    if payload_type == "patch_apply_end":
        return one_line(payload.get("stdout") or payload.get("message")), False
    if payload_type == "error":
        return one_line(payload.get("message") or payload.get("text")), False
    if payload_type in {None, "task_started"}:
        return "", False
    return compact_json({key: value for key, value in payload.items() if key != "type"}), True


def rollout_state(payload_type: object) -> str:
    if payload_type == "error":
        return "error"
    if payload_type == "task_started":
        return "started"
    if payload_type == "task_complete":
        return "completed"
    return ""


def rollout_join_text(value: object) -> str:
    if isinstance(value, list):
        parts = []
        for entry in value:
            if isinstance(entry, dict) and entry.get("text"):
                parts.append(str(entry["text"]))
            elif isinstance(entry, str) and entry:
                parts.append(entry)
        return " ".join(parts)
    if isinstance(value, str):
        return value
    return ""


def rollout_tool_call_summary(payload: dict) -> str:
    name = payload.get("name")
    arguments = payload.get("arguments")
    if arguments is None:
        arguments = payload.get("input")
    if isinstance(arguments, str):
        arguments = one_line(arguments)
    elif arguments is not None:
        arguments = compact_json(arguments)
    if name and arguments:
        return f"{name} {arguments}"
    return str(name or arguments or "")


def rollout_token_summary(payload: dict) -> str:
    info = payload.get("info")
    usage = info.get("total_token_usage") if isinstance(info, dict) else None
    if not isinstance(usage, dict):
        return ""
    parts = []
    for source, label in (
        ("input_tokens", "input"),
        ("cached_input_tokens", "cached"),
        ("output_tokens", "output"),
    ):
        value = usage.get(source)
        if value is not None:
            parts.append(f"{label}={value}")
    return " ".join(parts)


def one_line(value: object) -> str:
    if value is None:
        return "-"
    text = str(value).replace("\t", "  ")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return "-"


def compact_json(value: object) -> str:
    try:
        return json.dumps(value, separators=(",", ":"), sort_keys=True)
    except (TypeError, ValueError):
        return str(value)


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    total = int(seconds)
    if total < 60:
        return f"{total}s"
    minutes, secs = divmod(total, 60)
    if minutes < 60:
        return f"{minutes}m{secs:02d}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h{minutes:02d}m"


def format_tokens(tokens: int | None) -> str:
    if tokens is None:
        return "-"
    if tokens >= 1_000_000:
        return f"{tokens / 1_000_000:.1f}M"
    if tokens >= 1_000:
        return f"{round(tokens / 1000)}k"
    return str(tokens)


def count_files(path: Path) -> int:
    if not path.is_dir():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def count_matching(path: Path, pattern: str) -> int:
    if not path.is_dir():
        return 0
    return sum(1 for _item in path.glob(pattern))


def status_sort_key(status: str) -> int:
    return {
        "running": 0,
        "pending": 1,
        "errored": 2,
        "completed": 3,
        "finished": 4,
    }.get(status, 5)


def sort_experiments(jobs_by_experiment: dict[str, list[Job]]) -> list[str]:
    # Category sort: an experiment's rank is its most-active job's status, so
    # experiments with a running job float to the top, then pending, errored,
    # and finished; ties broken alphabetically.
    def key(name: str) -> tuple[int, str]:
        jobs = jobs_by_experiment[name]
        rank = min((status_sort_key(job.status) for job in jobs), default=99)
        return (rank, name)

    return sorted(jobs_by_experiment, key=key)


def sort_trials(trials: list[Trial], mode: str) -> list[Trial]:
    # "name" keeps the default status-grouped, alphabetical order; "passed" and
    # "failed" surface verified outcomes first, ties broken by task id.
    if mode == "passed":
        return sorted(trials, key=lambda t: (trial_outcome_rank(t, passed_first=True), t.task_id))
    if mode == "failed":
        return sorted(trials, key=lambda t: (trial_outcome_rank(t, passed_first=False), t.task_id))
    return sorted(trials, key=lambda t: (status_sort_key(t.status), t.task_id))


def trial_outcome_rank(trial: Trial, *, passed_first: bool) -> int:
    outcome = verify_outcome(trial.verify_result)
    order = {"passed": 0, "failed": 1} if passed_first else {"failed": 0, "passed": 1}
    return order.get(outcome, 2)


def status_icon(status: str) -> str:
    return {
        "running": ">",
        "pending": ".",
        "errored": "!",
        "completed": "+",
        "finished": "+",
    }.get(status, "?")


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def visible_window(items: list, selected: int, capacity: int) -> list[tuple[int, object]]:
    if capacity <= 0 or not items:
        return []
    selected = clamp(selected, 0, len(items) - 1)
    start = max(0, selected - capacity // 2)
    start = min(start, max(0, len(items) - capacity))
    end = min(len(items), start + capacity)
    return list(enumerate(items[start:end], start=start))


if __name__ == "__main__":
    raise SystemExit(main())
