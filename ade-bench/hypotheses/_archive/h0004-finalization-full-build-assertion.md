---
id: h0004
title: Pre-finalize full-graph build assertion in Stage Finalization — refuse to finish on any Catalog Error
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

Placing the build-and-verify discipline as a **last-line assertion in Stage:
Finalization** — "do not declare done while the full graph has any unresolved upstream" —
catches the build-error class at the one point every task path must pass through, no matter
which earlier stage the solver rushed. This is an alternative framing to h0001 (validation
prose) and h0002 (a dedicated mid-pipeline gate): it relies on the *finalization* boundary
rather than adding a stage or strengthening mid-pipeline checks, testing whether a single
terminal gate is sufficient to convert the 27/39 build-error hard-zeros (each a `Catalog
Error: Table with name <X> does not exist` from an unbuilt/misnamed upstream, 0 target
tests run) into runnable trials.

**The single solver-README change** (independent variable = the README only): edit
**Stage: Finalization** of `codex-ade-dbt-minimal/README.md`. Today it reads "Leave only
intended project changes. Remove scratch files … Finish with changed files and concise
validation evidence." This hypothesis adds a **pre-finalize assertion**: before finishing,
run a **full-graph** `dbt build`/`dbt run` (no `--select` narrowing) and confirm a
zero-error result; if dbt reports **any** `Catalog Error: … does not exist` or non-zero
`ERROR`, the task is **NOT finished** — the solver must resolve the missing/misnamed
upstream and re-assert before declaring done. The "concise validation evidence" the stage
already asks for is specified to include the final zero-error `dbt build` summary line
(`Done. PASS=… ERROR=0 …`). No new stage is added; Implementation and Validation keep their
current prose (the Implementation "edited area compiles" line stays as the cheap inner
check). The leak-guard / no-external-reference prose is kept verbatim.

Target datasets (smoke): `intercom001`, `f1005`, `ana-eng002`, `asana003` (the named
build-error exemplars spanning intercom / f1 / ana-eng / asana — each should be blocked from
finalizing by the assertion until its upstream is built/renamed). Near-miss control:
`quickbooks003` (builds clean at 12/14 — the assertion should pass immediately and add no
regression; it also guards against the assertion mis-firing on the cleanup step and deleting
needed build state).

**Falsifiable.** If the pre-finalize assertion does not reduce the build-error count on the
smoke targets vs `@baseline` (targets still finalize with `Catalog Error`/0 target tests
run), the hypothesis is rejected. Also rejected if `quickbooks003` regresses below 12/14
(e.g. the added build/cleanup interaction breaks its previously-green state).

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Only `codex-ade-dbt-minimal/README.md`'s **Stage: Finalization** prose changes (added
pre-finalize zero-error full-build assertion); no new stage, no leak-guard prose altered.
Verified by: `diff ../specs/baseline.yaml ../specs/h0004-finalization-full-build-assertion.yaml`
shows only `experiment:` + `solver_workflow:` differ; the smoke spec additionally adds
`benchmark.tasks`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`.**
Behavioral read names, per smoke target, whether the finalization assertion fired (agent
refused to finish on a Catalog Error and resolved the upstream — method adherence) and
whether the build error was thereby eliminated; `quickbooks003` checked for non-regression.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
