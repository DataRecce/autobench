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
**External-oracle audit** section must stay intact (no HuggingFace `datasets`/`hf://`,
no canonical-data downloads, no web search, no LLM-as-oracle). `rk audit --policy strict`
is the backstop. Enforce at the `propose` gate.

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

## Safety

Never delete or rewrite existing run directories unless asked. Keep outputs under
`ade-bench/runs/` (gitignored). Do not move run outputs into tracked files.
