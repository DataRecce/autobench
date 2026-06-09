# autobench — operator guide

autobench is an auto-research repo. It tunes a **codex spacedock solver-workflow README**
(the independent variable) to push the ade-bench `stratified_pass_at_1` above the
**9/48 (0.1875)** baseline. razorback runs and scores each variant; a spacedock workflow
(`ade-bench/hypotheses/`) ideates, gates, and analyzes. First target benchmark:
`ade-bench` (48 tasks). See `docs/superpowers/specs/2026-06-01-autobench-auto-research-design.md`.

## Submodules (read-only — never edit)

- `razorback/` — benchmark runner. Run `rk` from `ade-bench/`:
  `uv run --project ../razorback rk <args>`. (Optional shell alias:
  `alias rk='uv run --project '"$PWD"'/razorback rk'`.)
- `spacedock/` — workflow framework + `first-officer`/`ensign` skills + the `status` CLI
  at `spacedock/skills/commission/bin/status`.

## 🔒 Run prerequisites (load-bearing — before any `rk run`)

- `export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"` —
  specs with `agent.kind: spacedock_solver` fail at agent setup without it.
- `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` set; codex auth configured (the
  first loops run on a flat OpenAI personal subscription).
- Docker / Colima running (Harbor's execution environment).
- The ade-bench dataset resolves anonymously (it is public).

## Running the loop

1. Seed a concept: `ade-bench/hypotheses/concept-<slug>.md`.
2. Start the orchestrator: `spacedock:first-officer` on `ade-bench/hypotheses/`.
3. Flow: concept → `ideate` (fan-out) ; hypothesis → `propose` → `smoke` → `full` →
   `analyze` → `conclude`.
4. Two human gates: `propose` (leak-guard) and `smoke → full` (go/no-go). Always pass
   `--runs-dir runs`; prefer `rk run --explain` first.

## 🔒 The independent-variable rule

Only the solver README changes between hypotheses. Runtime (codex), model (gpt-5.5),
sampling, `reasoning_effort: xhigh`, `trials: 1` (every run, smoke and full), and spec
shape are held constant. A variant spec differs from `ade-bench/specs/baseline.yaml`
only in `experiment:` + `solver_workflow:`. Anything else is a separate, declared
hypothesis.

## 🔒 Leak-guard discipline

The workspace data is the only authoritative source. The solver README's
**no-external-reference / leak-guard prose** must stay intact (no public fetches —
`curl`/`wget`/`git clone`, HuggingFace `datasets`/`hf://`, package-source or canonical-data
downloads, web search, LLM-as-oracle). `rk audit --policy strict` is the backstop. Enforce
at the `propose` gate.

## Budget discipline

`rk run --explain` ($0) first; smoke (the hypothesis's target datasets) before full.
Budget caps are **deferred** while on a flat OpenAI subscription; reinstate
`--max-budget-usd-running` / `experiment_meta.max_budget_usd` when moving to metered API.

## 🔒 Reproducibility discipline

Always `rk freeze --allow-missing` (seals the solver-README content hash; `--allow-missing`
because model/image are deliberately unpinned). The dataset digest is pinned.
A frozen spec + README hash are immutable once smoke starts.

## Native primitives

- Champion = `@baseline`: `rk baseline promote <run-dir>` + `rk registry add run baseline <run-dir>`.
- Compare: `rk runs diff "$(... rk registry resolve run @baseline)" <variant-run-dir>`.
- Per-cell pipeline: `ade-bench/drivers/matrix.sh` (chains run + `captured>0` + audit + score + ledger).

## Monitoring & log analysis

Live: `<run-dir>/job.log`, `<cell>/trial.log`, main agent `<cell>/agent/codex.txt`;
sub-agent (ensign) transcripts under `<cell>/agent/sessions/<year>/…` (dispatch summary
in `<cell>/subagent-trace-manifest.json`); grader output in `<cell>/verifier/`
(`reward.txt`, `test-stdout.txt`); failures in `<cell>/exception.txt`; results in
`summary.json` / `per_trial_outcomes.json` / `result.json`. `events.jsonl` is often
**empty** for these Harbor runs — do not rely on it. The `analyze` stage reads these
per-task logs for distance-to-pass + behavioral findings.

## 🔒 Detached runs (`rk run` / `matrix.sh`) + how the FO learns they finished

`rk run` is 30 min–7 hr+ — far past the Bash-tool timeout, and plain background tasks are
reaped at turn-end. So every `rk run` (and `matrix.sh`) launches through
**`ade-bench/drivers/rk-run-detached.sh <key> <spec> [run|matrix]`** (run from `ade-bench/`), which:

- `nohup`s the run so it survives the process/turn/session cap (reparented to init);
- writes a handle dir `runs/.rk-handles/<key>-<ts>/` (`<key>` e.g. `h0037-smoke`):
  `pid` (worker PID) · `log` (combined output) · `cmd`/`meta` (provenance) ·
  **`done`** — the terminal sentinel (atomic same-fs rename): `rc=<n> end=<iso> rundir=<path>`.
  **Absent ⇒ not finished.** This file — never a live process — is the source of truth.
- fires an **ntfy** push on completion (topic in `ade-bench/.ntfy-topic`, gitignored) to the
  captain's phone, autonomously, whether or not the agent is awake.

**Roles.** The ensign LAUNCHES and returns the handle immediately; it NEVER waits (subagents
are synchronous and cannot own a multi-hour wait). The **FO owns the wait**.

**FO rule — scan every turn.** At the top of EVERY turn, scan `runs/.rk-handles/*/` and
re-attach any in-flight run. Per handle, read the 4-state model:

| `done`? | pid (`kill -0`) | meaning | action |
|---|---|---|---|
| present, `rc=0` | — | finished OK | run `rk audit`/`score`, judge artifact → present the gate |
| present, `rc≠0` | — | run failed | surface the error; do not gate |
| absent | alive | still running | keep waiting (never block a single Bash call on it) |
| absent | dead | crashed before the verdict — OR killed just after `rk` finished | **before crying crash, check harbor's own output** (`<rundir>/<cell>/result.json`, `summary.json`/`per_trial_outcomes.json`, or `matrix.sh`'s `score.json`/`audit.json`); if present, treat as finished and recover `rc` from there |

**Wall-clock backstop.** If a handle's `start` (in `meta`) is >~9 h ago and it is still
non-terminal, escalate to the captain regardless of pid state (covers a pid-reuse false-alive).

There is **no live poller / no `Monitor`** — its multi-hour lifetime is unproven and a short
test cannot prove it (it would be a self-anchored false-green; cf. the false-green wall). The
sentinel + scan-every-turn is the correctness floor; ntfy is the autonomous push. Full rationale
+ the adversarial-review reasoning: `ade-bench/hypotheses/_artifacts/WORKFLOW-REFINE.md`.

The fast `--explain` / `rk audit` / `rk score` calls stay foreground and run after the sentinel lands.

## Safety

Never delete or rewrite existing run directories unless asked. Keep outputs under
`ade-bench/runs/` (gitignored). Do not move run outputs into tracked files.
