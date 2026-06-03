---
id: h0005
title: Baseline rerun — codex ade-dbt-minimal solver, full 48 tasks (post wrong-DuckDB-dataset fix)
status: analyze
kind: hypothesis
source: captain directive — new full baseline run after the wrong-DuckDB-in-images mtime-collision fix; re-analyze to confirm the anchor still holds
started: 2026-06-03T00:06:32Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

This is **not a README change** — it is a clean re-run of the seed baseline solver
(`solver_workflows/codex-ade-dbt-minimal`) on all 48 ade-bench tasks, produced after the
wrong-DuckDB-in-images dataset fix (BuildKit COPY mtime-collision; unique-mtime fix +
guard script). The question: does the post-fix full run still match the established
`@baseline` anchor (9/48, 0.1875), or did the dataset fix shift which tasks pass?

Run to analyze: `runs/ade-bench-baseline/622bdedac572b479/` (48 cells, same solver as
`@baseline`, `runtime: codex`).

Fired directly at `analyze` by captain directive — the `propose`/`smoke`/`full`
authoring stages are skipped because there is no variant solver/spec to author; the run
already exists.

## Acceptance criteria

**AC-1 — Every recorded score is paired with a clean strict audit.**
Verified by: `rk audit --policy strict <run-dir>` is clean on the same run-dir the
`rk score` reads.

**AC-2 — Quantitative read cites the paired `rk runs diff @baseline <run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs paper_baseline 0.1875.**

**AC-3 — Behavioral read names per-task verdict changes vs `@baseline` and the
distance-to-pass (`checks_passed / expected_test_count`) for notable failures, with a
verdict on whether the dataset fix changed the anchor.**

## Run result

## Behavioral analysis

## Verdict
