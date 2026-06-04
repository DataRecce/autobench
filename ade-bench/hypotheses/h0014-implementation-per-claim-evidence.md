---
id: h0014
title: Implementation — for analysis/answer deliverables, back each component of the answer with its own direct query (include/exclude only on confirmation)
status: hypothesis
kind: hypothesis
source: concept-resolve-uncovered-false-greens fan-out; evidence re-audit of @baseline (622bdedac572b479, 31/48). Lone tail — f1011: the analysis answer model emitted "ABDE" but the correct answer was "ABE"; option D was included on plausibility, never verified, and check_option_b failed (1/6). Isolated task type (answer-style deliverable). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-04T13:40:51Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The re-audit found `f1011` is a distinct, isolated failure type: the deliverable is an
**analysis answer** model (`analysis__answer`, value `ABDE`) graded per-option by
`check_option_*` tests. The solver included option **D** ("caution flags affect lap times")
on the strength of reading model logic and gathering supportive "evidence," but never ran a
direct query confirming D against the data; the correct answer was `ABE`, and
`check_option_b` failed (1 of 6 checks). Its shape check ("row_count=1, column_count=1,
value ABDE") was a false-green because shape says nothing about which letters are right.

The seed solver has no rule for how to construct an answer-style deliverable, so it assembles
the answer from plausibility and narrative evidence rather than a decisive per-option query.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation instruction — *for analysis/answer-style deliverables (e.g. selecting which
statements are true, or a single derived conclusion), back each component of the answer with
its own explicit query against the data: include an option only if a direct query confirms
it, and exclude it if the query refutes it; do not include or drop an option based on reading
model logic or plausibility alone* — will flip `f1011` by forcing a confirming/refuting query
per option (which would have dropped D), raising `stratified_pass_at_1` above the `@baseline`
0.6458.

This is the independent-evidence idea (surviving direction #1) applied to a categorical answer
rather than a numeric reconcile — distinct from h0012 (numeric/row-count recompute). It is
generative (how to build the answer), not a self-anchored re-derivation: each option is tested
against the raw data, not against the solver's prior reasoning. One idea, one stage
(Implementation). NOTE: this targets a single failure, so its expected full-run delta is
small; it is filed for completeness of the cluster, not as a high-leverage bet.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact (local data only — no public fetch, no oracle, no
reference to hidden `AUTO_*`/`check_option_*`/verifier tests).

Target datasets (smoke, all `ade-bench-` prefixed): the analysis-answer failure —
`ade-bench-f1011` — plus stable-`@baseline`-pass regression sentinels `ade-bench-f1007`,
`ade-bench-f1004` (f-series passes that exercise the same solver path without being
answer-style).

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0014-implementation-per-claim-evidence.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Implementation` (the single per-claim-evidence rule), leaves
Exploration/Validation/Finalization and the dependency/package guardrails untouched, and does
not reference hidden `AUTO_*`/`check_option_*`/`solution__*`/verifier tests or weaken the
leak-guard. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on `f1011` + the 2 f-series sentinels, the variant must not regress the
sentinels and should flip `f1011` to a pass before promotion to full.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
