# ade-bench research repo

Scaffolded by `rk research new ade-bench --from dbt-labs/ade-bench@sha256:2c1f9e6966d01b0a5de2235d1a0b64089c7eead42c85c3b7b61d0929405c2bd5`.

This repo holds one Harbor-published benchmark's research lifecycle: a
baseline run, hypothesis variants, paired tests, and the captain-facing
artifacts each stage produces.

## Layout

```
ade-bench-research/
├── specs/                       # frozen + unfrozen spec YAML
│   ├── baseline.yaml            # first runnable spec — edit & freeze
│   └── README.md
├── solver_workflows/            # spacedock-solver workflow READMEs
│   ├── baseline/README.md       # the agent reads this per trial
│   └── README.md
├── hypotheses/                  # per-hypothesis notes you author
│   └── README.md
├── runs/                        # razorback writes here (gitignored)
│   └── .gitignore
├── drivers/
│   └── matrix.sh                # per-cell pipeline (rk run + audit + score)
└── razorback-research.toml      # named-ref registry seed
```

## First run

```bash
$ rk freeze specs/baseline.yaml --out specs/baseline.frozen.yaml
$ rk run specs/baseline.frozen.yaml --runs-dir runs --n-tasks 5
$ rk audit runs/ade-bench-baseline/ade-bench-baseline_<sealed>/ --policy strict
$ rk score runs/ade-bench-baseline/ade-bench-baseline_<sealed>/
```

`rk score` auto-pulls `experiment_meta.paper_baseline` from the frozen
spec and surfaces `taint_status:` from `audit.json`. Use `--n-tasks` for
smokes; drop it for the full benchmark.

## Autoresearch lifecycle

1. **Baseline.** Run the scaffolded `specs/baseline.yaml` against the
   full benchmark. Capture the headline + `audit.json` clean
   attestation in `hypotheses/0001-baseline-headline.md`.

2. **Hypothesis.** Copy `solver_workflows/baseline/` to
   `solver_workflows/h0001-<slug>/`. Edit the README. Copy
   `specs/baseline.yaml` to `specs/h0001.yaml` and point the new
   `solver_workflow:` at the copied directory.

3. **Pair test.** Freeze + run + audit the hypothesis. Run
   `rk diff <baseline-run-dir> <h0001-run-dir>` for the paired
   delta with bootstrap CIs and Holm-Bonferroni-adjusted p-values.

4. **Conclude.** Promote the hypothesis as the new baseline if the
   delta clears your tripwire, or discard. Either way, record the
   verdict in `hypotheses/0001-<slug>/verdict.md`.

For batch matrix runs (variants × subsets), use `drivers/matrix.sh`.

## Live preconditions

The autoresearch loop is "live" when:
- `ANTHROPIC_API_KEY` (or `CLAUDE_CODE_OAUTH_TOKEN`) is in the env
- Docker / Colima is running (harbor's docker environment uses it)
- `dbt-labs/ade-bench@sha256:2c1f9e6966d01b0a5de2235d1a0b64089c7eead42c85c3b7b61d0929405c2bd5` resolves anonymously (public datasets) or your
  Harbor auth is configured (private datasets — out of scope for this
  scaffold)
- `rk audit --policy strict` runs after each `rk run` before
  `rk score` / `rk diff`. The matrix driver chains this automatically.
- For spacedock-variant trials, every cell writes
  `subagent-trace-manifest.json` with `captured > 0`. The matrix
  driver REJECTs cells with `captured == 0` (signals the spacedock
  crew failed to load).
