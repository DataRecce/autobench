---
id: h0001
title: Strengthen Stage Validation — mandatory zero-error full dbt build before finalize
status: hypothesis
kind: hypothesis
source: concept-build-and-verify fan-out
started: 2026-06-02T01:08:04Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Making **Stage: Validation** require a clean full-graph build — not just "additional
correctness checks beyond it builds" — converts build-error hard-zeros into runnable
trials, because the dominant failure class (27/39 = 69%) is the solver finalizing a graph
with dangling/misnamed upstreams that dbt rejects with `Catalog Error: Table with name
<X> does not exist`, so zero target tests run.

**The single solver-README change** (independent variable = the README only): edit
**Stage: Validation** of `codex-ade-dbt-minimal/README.md`. Today that stage opens "Do
additional correctness checks beyond 'it builds'." and ends with the permissive "Run
broader dbt validation when practical for the task scope." This hypothesis prepends a
mandatory, non-optional build step to that stage: run a **full-graph** `dbt build`
(or `dbt run` over the whole graph, no `--select` narrowing) over the project, and treat
**any** `Catalog Error: … does not exist` (or any non-zero dbt `ERROR` count) as
**unfinished implementation work, not a passable result** — the solver MUST NOT proceed
to Finalization until the full graph builds with zero errors. No new stage is added and
no other stage is touched; the change lives entirely inside the prose of Stage:
Validation. The leak-guard / no-external-reference prose (no `curl`/`wget`/`git
clone`/web lookup; local workspace only; preserve packages/profiles/`dbt_packages/`) is
kept verbatim.

Target datasets (smoke): `intercom001`, `f1005`, `ana-eng002`, `asana003` (the named
build-error exemplars spanning intercom / f1 / ana-eng / asana). Near-miss control to
watch for regression: `quickbooks003` (builds clean today at 12/14 — the strengthened
validation must not break its already-green build).

**Falsifiable.** If the strengthened Validation stage does not reduce the build-error
count on the smoke targets relative to `@baseline` (i.e. the targeted tasks still finalize
with `Catalog Error`/non-zero dbt ERROR and 0 target tests run), the hypothesis is
rejected. It is also rejected if `quickbooks003` regresses from its baseline 12/14.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Only `codex-ade-dbt-minimal/README.md`'s **Stage: Validation** prose changes (full-graph
build made mandatory, Catalog Error = unfinished); no other stage and no leak-guard prose
is altered. Verified by: `diff ../specs/baseline.yaml ../specs/h0001-validation-full-build-gate.yaml`
shows only `experiment:` + `solver_workflow:` differ; the smoke spec additionally adds
`benchmark.tasks`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`.**
Behavioral read names, per smoke target, whether the build-error (`Catalog Error … does
not exist`, dbt ERROR>0) was eliminated and whether target tests then ran; `quickbooks003`
is checked for non-regression.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
