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

## Research workflow overview

The repo is operated as an **autoresearch loop** commissioned with
[spacedock](spacedock/) under `ade-bench/hypotheses/`. Each cycle proposes one change to
the solver-workflow README (the **only** independent variable), runs it through razorback,
and either promotes it as the new champion or records why it failed. Full stage-by-stage
detail lives in `ade-bench/hypotheses/README.md`; the operating rules live in `AGENTS.md`.

### Roles

| Role | Who | Responsibility |
|------|-----|----------------|
| **Captain** | The human | Approves the two gates; sets research strategy. |
| **First officer (FO)** | `spacedock:first-officer` agent | Orchestrates the loop: dispatches workers, presents gates, advances entity state, owns the wait on long detached runs. |
| **Ensign** | `spacedock:ensign` subagents | Execute stage work (ideate, author variants, launch runs, analyze) and return immediately. |
| **Gatekeeper** | Review subagent | Advisory pre-review of every proposal against `_gatekeeper/propose-review-guideline.md`; recommends APPROVE / REVISE / REJECT. |
| **Solver** | codex (`agent.kind: spacedock_solver`) | Spawned by razorback inside Harbor to attempt the benchmark tasks. The operator never solves tasks. |

### Entities and lifecycle

Two entity kinds live as markdown files in `ade-bench/hypotheses/`:

- **Concept** (`concept-<slug>.md`) — a research direction (*breadth*). Path:
  `concept → ideate → expanded`. The `ideate` stage fans a concept out into 2–5
  hypothesis files, each naming one specific, falsifiable solver-README change.
- **Hypothesis** (`h<NNNN>-<slug>.md`) — one testable README change run end-to-end
  (*depth*). Path:

```
hypothesis → propose 🚦 → smoke 🚦 → full → analyze → conclude
                              │
                              ├─→ hypothesis  (flawed but revisable; requires a Failure Review)
                              └─→ conclude    (cleanly falsified; REJECTED without a full run)
```

### Stages in brief

1. **propose** *(🚦 captain gate — leak-guard)*. An ensign forks the current `@baseline`
   solver directory, edits its `README.md` (the one variable), creates the full + smoke
   specs (differing from `specs/baseline.yaml` only in `experiment:` + `solver_workflow:`),
   and freezes both. The gatekeeper pre-reviews; the captain gets a boxed smoke-set table
   (targets 🎯, sentinels, per-family canaries) with baseline rewards and an ETA, and
   makes the final call.
2. **smoke** *(🚦 captain gate — go/no-go)*. A focused run on the hypothesis's target
   tasks plus sentinels and regression canaries. Every smoke ends with a required
   **post-run deep-dive**: verdict deltas vs `@baseline`, distance-to-pass from grader
   output, and a behavioral read of the committed artifact (did the README rule actually
   reach the solver's SQL, or was it inert?). Every NO-GO gets a classified
   `## Failure Review`. Worthwhile → `full`; revisable → back to `hypothesis`; cleanly
   falsified → `conclude` (REJECTED).
3. **full**. The complete 48-task run on the frozen full spec, followed by
   `rk audit --policy strict` and `rk score`.
4. **analyze**. Quantitative (paired diff vs `@baseline` with CIs) **and** behavioral
   (per-changed-task transcript + artifact reads). The report must account for every
   verdict flip in both directions — gains *and* regressions on previously-passing tasks —
   plus prevention and the next move.
5. **conclude** *(terminal)*. Promote (`rk baseline promote` — the run becomes the new
   `@baseline` champion that all future hypotheses fork from) or reject; record the
   distilled learnings in the entity file; route follow-ups (`stop` / `probe` / `file` /
   `escalate`).

### Hard disciplines (🔒 in `AGENTS.md`)

- **One variable.** Only the solver README changes between hypotheses. Runtime (codex),
  model, sampling, `trials: 1`, and spec shape are held constant.
- **Leak-guard.** The solver README's no-external-reference prose stays intact (no public
  fetches, no LLM-as-oracle); `rk audit --policy strict` is the backstop; enforced at the
  `propose` gate.
- **Reproducibility.** Every spec is frozen (`rk freeze`) before running; the spec + README
  hash are immutable once smoke starts; the dataset digest is pinned.
- **Detached runs.** `rk run` takes 30 min–7 hr+, so every run launches via
  `drivers/rk-run-detached.sh`, which writes a handle under `runs/.rk-handles/` with an
  atomic `done` sentinel and fires an ntfy push on completion. Ensigns launch and return;
  the FO scans the handles every turn and only audits/scores after the sentinel lands.
- **Evidence over chatter.** A score is only trusted with a clean strict audit; a flip is
  only credited when the change provably reached the committed artifact; learnings are
  written into the entity file (the portable experiment record), with cross-experiment
  structural lessons in `_artifacts/WORKFLOW-REFINE.md`.

### Champion model

The reigning champion is the `@baseline` run-dir in `razorback-research.toml`. New
hypotheses fork its solver README; `analyze` diffs against its run; a promoted hypothesis
replaces it. Concluded entities move to `hypotheses/_archive/` (50+ hypotheses and their
verdicts to date), so the directory doubles as the experiment ledger.

## Operating the loop

See `AGENTS.md` (operator guide) and `CLAUDE.md`. In short: seed a concept under
`ade-bench/hypotheses/`, run `spacedock:first-officer` on that directory, and approve at
the `propose` (leak-guard) and `smoke → full` (go/no-go) gates.
