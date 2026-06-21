# Razorback Run Monitor

A lightweight terminal UI (TUI) for watching `rk run` jobs live while they
execute inside Harbor. It reads the on-disk run directory that razorback writes
and renders a refreshing dashboard of experiments → jobs → trials, with a live
log tail for the selected trial.

It is **read-only**: the monitor never writes to run directories, never talks to
razorback, and never touches the solver. It just polls the filesystem.

```
┌ Razorback Monitor  q:quit  …                                                 ┐
├──────────────────────────┬───────────────────────────────────────────────────┤
│ Experiments / Jobs       │ Trials                                            │
│ v * ade-bench-h0043 (2)  │ > airbnb009 running                 12m  -    340k │
│     > 7390e6a running    │ + asana002 completed [passed]       3m   9/11 210k │
│       32/48 done · 32 ✓  │ ! quickbooks001 errored             1m   -    12k  │
│   > ade-bench-baseline   ├───────────────────────────────────────────────────┤
│                          │ Trial Info  (dataset, status, verify, answer, …)  │
│                          ├───────────────────────────────────────────────────┤
│                          │ Trial Logs  (live tail of selected log source)    │
└──────────────────────────┴───────────────────────────────────────────────────┘
```

## Running

This folder is a self-contained `uv` project (its only runtime dependency is
`rich`). From `monitor/`, `uv` creates the venv on first run automatically:

```fish
cd /home/kent/autobench/monitor
uv run rk-monitor --runs-dir ../ade-bench/runs
```

`rk-monitor` is the console entry point declared in `pyproject.toml`
(`monitor:main`). Equivalent forms:

```fish
uv run python monitor.py --runs-dir ../ade-bench/runs   # run the file directly
./monitor.py --runs-dir ../ade-bench/runs               # if rich is on system Python
```

Point `--runs-dir` at the `ade-bench/runs` tree (or wherever razorback writes
jobs). Pass `--datasets ../ade-bench/datasets.md` to populate the dataset
difficulty/description fields if that file exists.

### Options

| Flag | Default | Meaning |
|------|---------|---------|
| `--runs-dir PATH` | `runs` | Root directory to scan for jobs. Point this at `ade-bench/runs`. |
| `--datasets PATH` | `datasets.md` | Markdown table of dataset difficulty/descriptions, shown in **Trial Info**. Optional — missing file just leaves those fields blank. |
| `--refresh-sec FLOAT` | `2.0` | Filesystem poll interval (clamped to ≥ 0.5s). |

The terminal must be at least **80×12**; smaller shows a "too small" notice.

## What it discovers

The monitor expects razorback's standard run layout:

```
<runs-dir>/
  <experiment>/                 # e.g. ade-bench-h0043-...
    <job-hash>/                 # a single `rk run` job
      _job_config.yaml
      config.json               # task list, used for pending/total counts
      result.json               # authoritative stats once trials complete
      lock.json                 # present ⇒ job is running
      <task-id>__<suffix>/      # one trial dir per task (must contain "__")
        result.json
        exception.txt
        trial.log
        agent/codex.txt         # solver transcript        (ade-bench, flat)
        agent/sessions/*.jsonl  # raw Codex/spacedock session rollouts
        verifier/test-stdout.txt
```

Two layouts are supported for where a trial keeps its agent/verifier content:

- **ade-bench (flat)** — `agent/` and `verifier/` live directly in the trial dir
  (as above).
- **DAB (`dataagentbench`, multi-step)** — the trial is split into pipeline
  steps, and each step has its own content under `steps/<step>/agent/...` and
  `steps/<step>/verifier/...`. The monitor finds these per-step logs and labels
  them with the step name (e.g. `main:codex`, `main:session:first-officer`).
  `trial.log` and `exception.txt` stay at the trial root in both layouts.

- A directory is treated as a **job** if it contains any of `_job_config.yaml`,
  `config.json`, `job.log`, or `lock.json`.
- A subdirectory is treated as a **trial** if its name contains `__`
  (`<task-id>__<random-suffix>`).
- Pending trials (configured but not yet started) are synthesized from
  `config.json`'s task list so you see the full slate from the first second.

### Status meanings

| Icon | Status | How it's decided |
|------|--------|------------------|
| `>` | running | trial has no `result.json` yet, or job stats report running/pending |
| `.` | pending | configured but not started |
| `!` | errored | `exception.txt` exists or `result.json` has `exception_info` |
| `+` | completed / finished | `result.json` has a verifier/agent result |

`[passed]` / `[failed]` tags on completed trials come from the verifier reward
(`reward=1.0` ⇒ passed). For **batch DAB** trials (one whole dataset per trial,
scored per query) the binary tag is replaced by the dataset's per-query result —
`[2/3 · pass@1 66.7%]` — green at 100%, red at 0%, yellow in between.

## Keys

| Key | Action |
|-----|--------|
| `q` / `Ctrl-C` | quit |
| `←` / `→` | focus sidebar / trials panel |
| `Tab` / `Shift-Tab` | cycle focus |
| `↑` `↓` / `k` `j` | move selection in the focused panel (wraps) |
| `Home` / `End` | jump to first / last item |
| `[` / `]` | previous / next job within the experiment |
| `l` | cycle to the next log source for the current trial |
| `f` | open the log-source picker (↑↓ to choose, Enter to select, Esc to cancel) |
| `s` | cycle trial sort: name → passed-first → failed-first |
| `PgUp` / `PgDn` | scroll the log up (history) / down (toward live tail) |
| `r` | force an immediate refresh |

When the log is scrolled into history the panel title shows `scrolled +N` and
`paused +N, PgDn to follow`; scrolling back to the bottom resumes the live tail.

### Mouse

The monitor enables xterm mouse tracking, so you can also drive it by pointer:

| Action | Effect |
|--------|--------|
| Click a sidebar row | focus the sidebar and select that experiment/job |
| Click a trial row | focus the trials panel and select that trial |
| Scroll wheel over sidebar / trials | move that panel's selection up/down |
| Scroll wheel over the log panel | scroll the log through history / toward the live tail |

Mouse mode is turned off again on exit. While it's on, the terminal's own
click-to-select/copy is suppressed — hold your terminal's modifier (often
`Shift`) to select text the normal way.

## Panels

- **Experiments / Jobs** (left sidebar): every experiment with a job count.
  Experiments are category-sorted by their most-active job — those with a
  running job float to the top, then pending, errored, and finished, with
  alphabetical ties — and active experiments are marked `*`. The selected
  experiment expands to its jobs (newest first by mtime). Each job row shows
  status plus a progress suffix (`N/total done · K passed` while running,
  `K/total passed` when terminal). DAB jobs also append the `pass@1` rate
  (`K/total passed · pass@1 58.4%`) — a **stratified macro-average** that weights
  every dataset equally (mean of per-dataset pass rates), not every trial. It is
  omitted for ade-bench jobs and for jobs with no graded trials yet.
  - **Batch DAB** runs (`runs/codex-dab-batch-*`) execute every query of a
    dataset in a single trial, so each trial's reward is a fraction (that
    dataset's pass rate) rather than 0/1. There the `passed/total` count is
    **queries** passed across all datasets — passes read from each trial's
    `verifier/reward_per_query.json`, the total slate from each task's
    `tests/stratum.json` (so it shows the full denominator from the first
    second) — and `pass@1` is the mean of the per-dataset rewards
    (`8/12 done · 23/54 passed · pass@1 69.4%`).
- **Trials** (top right): one row per trial with status, `[passed]`/`[failed]`
  (or, for batch DAB, the dataset's `[2/3 · pass@1 66.7%]`), wall-clock duration,
  dbt test counts (`passed/total`), and agent token usage.
- **Trial Info**: dataset id, trial name, status, verify result, the **agent**
  answer, the ground **truth**, difficulty + description from `datasets.md`, and
  the trial path. For DAB the agent field is the value the agent wrote to
  `answers.json` and truth is the `ground_truth` from the task's
  `tests/validate.py`; for ade-bench (no answer contract) the agent field falls
  back to a one-line transcript / changed-files summary and truth to a
  solution/tests/seeds summary.
- **Trial Logs**: live tail of the selected log source. Codex transcript JSON
  (`agent/codex.txt`) and spacedock session rollouts (`agent/sessions/*.jsonl`)
  are parsed into readable `type | description` lines; plain logs render as-is.

## Log sources

For a trial the monitor surfaces, per step root, in order: known agent/verifier
files (`agent/codex.txt`, `agent/claude.txt`, `verifier/test-stdout.txt`, …),
any other `agent/*.txt` / `agent/*.log`, and each spacedock session rollout
under `agent/sessions/` — labelled `session:first-officer` for the parent and
`subagent:<type>#N` for dispatched workers (types read from the trial-root
`subagent-trace-manifest.json`). For DAB's multi-step layout every label is
prefixed with the step name (`main:codex`, …); the flat ade-bench layout uses
bare labels. While a DAB step is still running its transcript lives at the
trial-root `agent/` (it moves into `steps/<step>/` only when the step finishes),
so a running trial shows the live `codex` plus `trial.log`. `trial.log` and
`exception.txt` (trial root) come last, and the agent transcript stays the
default selection. With no trial selected it falls back to the job's
`job.log` / `events.jsonl`.

## Development

```fish
cd /home/kent/autobench/monitor
uv run pytest          # run the unit suite (tests/)
```

`uv run` installs the project editable, so edits to `monitor.py` are picked up
without a rebuild. The tests cover the pure formatting/parsing helpers and the
filesystem-discovery functions (the razorback schema decode); the live TUI loop
needs a tty and is verified by running it against a real `runs/` dir. See
`CLAUDE.md` for architecture and the refining checklist.

## Notes

- The monitor caches trial parsing per job keyed by a filesystem signature
  (mtimes + sizes of activity files), so idle jobs cost almost nothing to poll.
- It tolerates partial/half-written JSON: unreadable or malformed files are
  treated as empty rather than crashing the UI.
