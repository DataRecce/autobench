---
id: h0002
title: Insert a Build Gate stage between Implementation and Validation, build-fail routes back to Implementation
status: hypothesis
kind: hypothesis
source: concept-build-and-verify fan-out
started: 2026-06-02T01:08:04Z
completed: 2026-06-03T00:52:37Z
verdict: REJECTED
score:
worktree:
---

## Hypothesis

Inserting a **dedicated Build Gate stage** between Implementation and Validation — one
that must reach a zero-error full-graph build and, on failure, **routes back to
Implementation** to build the missing/correctly-named upstream and re-gates — eliminates
build-error hard-zeros more reliably than relying on Validation prose, because a named
gate with an explicit back-edge makes "the graph does not build yet" a first-class,
non-skippable control-flow state rather than a check folded into a later stage the solver
can rush past. The dominant failure class is 27/39 (69%) build-errors: `Catalog Error:
Table with name <X> does not exist` from unbuilt/misnamed upstreams, 0 target tests run.

**The single solver-README change** (independent variable = the README only): edit
`codex-ade-dbt-minimal/README.md` to add ONE new stage, **`## Stage: Build Gate`**,
positioned between **Stage: Implementation** and **Stage: Validation**. The new stage
runs a **full-graph** `dbt build`/`dbt run` (no `--select` narrowing) and requires a
zero-error result. On a build failure (any `Catalog Error: … does not exist` or non-zero
dbt `ERROR`), the stage instructs the solver to **return to Implementation** — build or
correctly rename the missing upstream model/source the error names — then re-run the gate.
The loop is **bounded** (a small fixed cap, e.g. up to 3 gate attempts), not open-ended;
if still failing at the cap, the solver records the unresolved build error and proceeds so
the trial is still scored. Implementation, Validation, and Finalization keep their current
prose otherwise (Implementation's existing "prove the edited area compiles" line stays as
the cheap inner-loop check; the new gate is the full-graph outer check). The leak-guard /
no-external-reference prose is kept verbatim.

Target datasets (smoke): `intercom001`, `f1005`, `ana-eng002`, `asana003` (build-error
exemplars; `intercom001`→`stg_intercom__conversation_part_history`,
`ana-eng002`→`fact_inventory`, `f1005`→`stg_f1_dataset__constructor_standings`,
`asana003`→`project_data` are exactly the unbuilt/misnamed upstreams the gate should force
resolution of). Near-miss control: `quickbooks003` (builds clean at 12/14 — the gate
should pass on the first attempt and add no regression).

**Falsifiable.** If the Build Gate stage does not reduce the build-error count on the
smoke targets vs `@baseline` (targets still finalize with `Catalog Error`/0 target tests),
or if the bounded retry loop fails to converge (gate keeps failing through the cap on all
targets), the hypothesis is rejected. Also rejected if `quickbooks003` regresses below
12/14.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Only `codex-ade-dbt-minimal/README.md` changes — one new `## Stage: Build Gate` inserted
between Implementation and Validation with a bounded build-fail→Implementation back-edge;
no leak-guard prose altered. Verified by: `diff ../specs/baseline.yaml ../specs/h0002-build-gate-stage.yaml`
shows only `experiment:` + `solver_workflow:` differ; the smoke spec additionally adds
`benchmark.tasks`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`.**
Behavioral read confirms, per smoke target, that the agent actually entered the Build Gate
stage, hit the back-edge to Implementation on a Catalog Error, and re-gated (method
adherence) — and whether that eliminated the build error; `quickbooks003` checked for
non-regression.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
