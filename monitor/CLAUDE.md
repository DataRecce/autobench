# CLAUDE.md — monitor/

Developer guide for `monitor.py`, the read-only TUI that watches `rk run` jobs.
Read `README.md` first for the user-facing behavior. This file is for
**developing and refining** the script.

## What this is

A single-file Python TUI (`monitor.py`) built on `rich` (`Live` + `Layout`),
packaged as a self-contained `uv` project (`pyproject.toml`, dep: `rich`). It
polls a razorback `runs/` tree on a timer and renders experiments → jobs →
trials with a live log tail. It is strictly **read-only**: it never writes run
dirs, never calls `rk`, never touches the solver. Treat "do not mutate run
directories" as an invariant.

## Run / dev loop

This folder owns its env — run everything through `uv` from `monitor/`:

```fish
cd /home/kent/autobench/monitor
uv run rk-monitor --runs-dir ../ade-bench/runs   # launch the TUI
uv run pytest                                    # run the unit suite
```

`rk-monitor` is the `[project.scripts]` entry point (`monitor:main`). `uv`
installs the project editable, so edits to `monitor.py` take effect with no
rebuild (`import monitor` in tests resolves straight to the source file).

There **is** a test suite now (`tests/test_monitor.py`): it covers the pure
formatting/parsing helpers and the filesystem-discovery functions over a fake
`runs/` tree built in `tmp_path`. The live TUI loop needs a tty and is not
unit-tested — after a UI/loop change, also launch it against a real `runs/`
dir, navigate with the keys, open the log picker (`f`), and confirm it doesn't
crash on in-flight (partially written) jobs. **New pure helpers should land
with a test**; that's the cheap regression net for schema-decode drift.

## Architecture

Two layers, cleanly split:

1. **`Monitor` class** — owns all UI state (selection indices, focus, sort
   mode, scroll, picker, the per-job trial cache) and the event loop in
   `run()`. `handle_key()` mutates state; `render()` rebuilds the `Layout` from
   current state. State changes never draw directly — they set state and the
   next `render()` reflects it.
2. **Module-level free functions** — two flavors:
   - **discovery/parsing** (`discover_jobs`, `discover_trials`, `trial_*`,
     `job_*`, `read_json`, `*_summary`, `parse_log_entry`): pure functions over
     the filesystem, no UI state. This is where razorback's on-disk schema is
     decoded.
   - **rendering** (`render_*`, `titled_panel`, `*_style`, `*_icon`): take data,
     return `rich` renderables. No filesystem access.

Keep that separation when extending: parsing functions stay pure and
UI-agnostic; rendering functions stay side-effect-free.

### Data model

`Job` and `Trial` (`@dataclass`) and the frozen `DatasetInfo` / `LogEntry` are
the only shared types. `discover_jobs()` builds shallow `Job`s (cheap stats for
every sidebar row); `discover_trials()` is the expensive per-job parse, run
lazily only for the *current* job and memoized in `self.trial_cache`.

### Mouse (click-to-select + scroll-wheel)

`TerminalInput.__enter__` emits `MOUSE_ENABLE` (xterm button tracking + SGR
coordinates, `\x1b[?1000h\x1b[?1006h`) and `__exit__` emits `MOUSE_DISABLE`.
Mouse reports arrive as CSI sequences ending in `M`/`m`, so the existing
escape-sequence assembler (`read_pending_chars`) reassembles them unchanged;
`read_key` then tries `parse_mouse_sequence()` before `normalize_key()` and
returns a `MouseEvent` instead of a key string. `handle_key` dispatches
`MouseEvent` to `handle_mouse`.

Hit-testing maps a screen `(col, row)` back to a logical row. **It does not
re-derive geometry by hand** — `render()` stashes the rendered root layout in
`self._last_layout`, and `compute_regions()` asks rich for the real
`Region(x, y, width, height)` of each named leaf panel
(`layout.render(console, options)`). Panel content starts at `region.y + 1`
(the top border), so `offset = row - (region.y + 1)` indexes into the same
`visible_window(...)` the panel drew — which is why `render()` also stores
`_sidebar_capacity` / `_trials_capacity` (the hit-test must recompute the
*identical* window). State only changes on input, so recomputing the window at
click time is guaranteed consistent with what was drawn. `_last_layout` is set
to `None` for the too-small and picker frames, which disables mouse there.

If you add or rename a clickable panel, give its `Layout` a stable `name=` and
look it up in `handle_click`/`handle_wheel`; if you change the capacity a panel
is rendered with, update the stored capacity so the hit-test stays aligned.

### Refresh & caching

- `refresh()` runs at most every `refresh_sec`, re-discovers jobs, and restores
  the prior experiment/job/trial selection by identity (path / name) so the
  cursor doesn't jump when the list reorders.
- `load_current_job_trials()` re-parses trials only when
  `job_trial_signature()` (mtimes + sizes of activity files) changes. **If you
  add a file the parser reads, add it to `TRIAL_ACTIVITY_FILES` /
  `JOB_ACTIVITY_FILES`** (or, for per-step files, the `step_roots` loop in
  `job_trial_signature`) or the cache will serve stale data.
- The event loop (`run()`) interleaves key polling and refresh: `key_poll_interval()`
  keeps input latency low while honoring the refresh cadence, and `dirty`
  tracking avoids redundant repaints.

## razorback schema this depends on

These are the external contracts; they can drift if razorback changes its
output. The most likely sources of future breakage:

- **Job dir markers**: `looks_like_job_dir()` → `_job_config.yaml`,
  `config.json`, `job.log`, `lock.json`.
- **Trial dir convention**: name contains `__`, `<task-id>__<suffix>`.
- **Trial content layout** (`step_roots()` / `content_roots()`): ade-bench keeps
  `agent/` and `verifier/` flat in the trial dir; DAB (`dataagentbench`) nests
  them under `steps/<step>/` (one per pipeline step). **While a DAB step runs,
  codex writes the live transcript to the trial-root `agent/` and only moves it
  into `steps/<step>/agent/` when the step finishes** — so readers iterate
  `content_roots(trial_dir)` (= step roots **plus the trial dir itself**), not
  `step_roots` alone, or a running trial shows only `trial.log`. The trial root
  contributes nothing once the move happens (its `agent/` is gone), so finished
  logs aren't duplicated. DAB step-root labels are step-prefixed (`main:codex`);
  trial-root labels are bare (`codex`); `trial.log`/`exception.txt` stay at the
  trial root in both layouts. **Anything reading `agent/*` or `verifier/*` must
  go through `content_roots`, not `trial_dir / "agent"` directly.**
- **`result.json`**: `stats.{n_running,n_pending,n_errored,n_completed}_trials`,
  `n_total_trials`, `finished_at`, `started_at`, `verifier_result.rewards.reward`,
  `agent_result.{n_input_tokens,n_output_tokens}`, `exception_info`,
  `stats.evals[*].reward_stats.reward` (reward-value → trial-id list; drives the
  pass count and the DAB **stratified macro-average** pass@1, where trials are
  grouped by dataset via `dataset_from_trial_id` — the `<dataset>-q<N>` prefix,
  verified against `stratum.json` — and per-dataset rates are averaged equally).
- **DAB run modes** (`dab_job_kind()`): `"dab"` = per-query (one trial per query,
  trial id `<dataset>-q<N>__…`, **binary** reward); `"dab-batch"` = one trial per
  whole dataset (bare `<dataset>__…` id, **fractional** reward = that dataset's
  pass rate) — distinguished by whether the first trial id carries a `-q<N>`
  segment. For **batch**, the sidebar `passed/total` is **queries**, not trials:
  - `verifier/reward_per_query.json` (`trial_reward_per_query`, under each step
    root) = `{q: {reward, reason}}`; passes = entries with `reward >= 1.0`.
  - total queries = Σ `tests/stratum.json` `stratum.query_ids` over the
    *configured* tasks (`job_batch_total_queries`) — the full slate, known from
    t=0; falls back to observed queries if no stratum is readable.
  - `pass@1` = mean of the per-dataset rewards (`job_batch_pass_at_1`, the
    value-weighted mean of `reward_stats.reward`) — equals the mean of the
    per-trial `reward.json` files and **excludes** completed-but-unrewarded
    datasets (verifier abstained / degraded), rather than `metrics[*].mean`,
    which counts them as 0.
- **`config.json`**: `tasks[*].path` (pending trials + total count).
- **Codex transcript** `agent/codex.txt`: line-delimited JSON events with
  `item.type` ∈ {`agent_message`, `command_execution`, `file_change`,
  `tool_call`, …}; parsed by `describe_log_item()`.
- **Spacedock session rollouts** `agent/sessions/**/rollout-*.jsonl`: first line
  is `session_meta` with `payload.thread_source` (`user` = first-officer,
  `subagent` = worker); body records have `payload.type`; parsed by
  `parse_rollout_entry()` / `describe_rollout_payload()`.
- **DAB agent answer** (`dab_answers_json_value`): the agent writes
  `/workspace/answers.json` = `{"answer": "<str>"}`, which is **not persisted as
  a file** — it is recovered from the last `patch_apply_end` rollout event whose
  `changes` has a path ending in `answers.json` (`.content` holds the written
  text). The `Agent` field prefers this; ade-bench falls back to the transcript
  summary.
- **DAB ground truth** (`validate_ground_truth`): the task's
  `tests/validate.py` assigns a `ground_truth` literal (list of names, or
  `(name, …)` tuples). Extracted via `ast.literal_eval` and rendered as ordered
  names for the `Truth` field; ade-bench falls back to the solution/tests/seeds
  summary. Non-literal ground truth (e.g. loaded from `ground_truth.csv`) yields
  None.
- **`subagent-trace-manifest.json`**: `dispatches[*].{spawn_index,subagent_type}`
  for labelling worker session logs.
- **Verifier** `verifier/test-stdout.txt`: dbt `Done. PASS=n … TOTAL=n` summary
  line; the *last* match is the test run (`TEST_SUMMARY_RE`).
- **`datasets.md`**: pipe table `` | `dataset` | difficulty | description | ``
  parsed by `load_dataset_info()`.

When adding a new field, decode it in a small pure helper next to its siblings,
fail soft (return `None`/`"-"`/`{}` on missing or malformed data — see
`read_json`, `parse_iso`), and never let a half-written file raise into the
render loop.

## Conventions

- **Fail soft, never crash the UI.** Every filesystem read tolerates missing /
  partial / malformed files. A running job is constantly being written; assume
  any file may be truncated mid-read.
- **Styles go through the theme.** Add a semantic key to `STYLES` and reference
  it; don't hardcode colors in renderers. Status/verify colors and icons are
  centralized in `status_style`/`verify_style`/`status_icon`.
- **Keys are normalized once.** `normalize_key()` + the `KEY_ALIASES` /
  regex tables map raw escape sequences to logical names; `handle_key()` only
  ever sees logical names. Add new bindings there and document them in
  `render_header()` and the README key table.
- **Windowing** for any scrollable list goes through `visible_window()` so long
  lists never overflow and crop silently.
- Comments explain *why* (e.g. the `os.read` vs buffered-read note in
  `read_raw_char`, the "last dbt summary is the test run" note). Match that
  density — explain non-obvious schema/terminal quirks, skip the obvious.

## Refining checklist

When asked to add a feature:
1. New data to show → add a pure `trial_*`/`job_*` parser + the field on the
   dataclass, and register any new source file in the `*_ACTIVITY_FILES` tuples.
2. New display → a `render_*` helper returning a renderable, wired into
   `render()`'s layout; reuse `titled_panel`.
3. New key → `handle_key()` (logical name), the header string, the README table.
4. Add/extend a test in `tests/test_monitor.py`, run `uv run pytest`, and for
   UI changes also verify against a live `runs/` dir.
