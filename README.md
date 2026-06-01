# autobench

Auto-research repo for AI-agent benchmarks. It runs a spacedock workflow that fine-tunes
a **solver-workflow README** to maximize a benchmark score, with [razorback](https://github.com/spacedock-dev/razorback)
executing and scoring each variant.

First target: **ade-bench** (48 dbt-repair tasks). Baseline to beat: **9/48 (0.1875)**.

## Layout

- `ade-bench/` — the per-benchmark research repo (`rk research new` layout):
  `specs/`, `solver_workflows/`, `hypotheses/` (the spacedock workflow), `drivers/matrix.sh`,
  `razorback-research.toml`, `runs/` (gitignored).
- `razorback/`, `spacedock/` — submodules (read-only).
- `ade-bench-datasets.md` — the 48 ade-bench task names + difficulties.
- `docs/superpowers/` — design spec + implementation plan.

## Operating the loop

See `AGENTS.md` (operator guide) and `CLAUDE.md`. In short: seed a concept under
`ade-bench/hypotheses/`, run `spacedock:first-officer` on that directory, and approve at
the `propose` (leak-guard) and `smoke → full` (go/no-go) gates.
