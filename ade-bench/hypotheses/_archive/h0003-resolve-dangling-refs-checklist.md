---
id: h0003
title: Implementation-stage checklist — resolve every dangling ref()/source() to a built relation before done
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

Targeting the **root cause** of the build-error class statically — by making the solver
enumerate every `ref()` and `source()` in the touched graph and confirm each resolves to a
relation that will actually be built or already exists, with correct casing/namespacing —
prevents the dangling-upstream class without waiting for a full `dbt build` to surface it.
This is an alternative framing to h0001/h0002 (which gate on *running* a full build):
here the discipline is a **diagnostic reference-resolution checklist** folded into
**Stage: Implementation**, attacking the mechanism directly — the 27/39 build-errors are
all `Catalog Error: Table with name <X> does not exist` from an upstream the solver left
unbuilt or misnamed (e.g. `asana003`→`project_data` is a *wrong source relation name*, not
a missing model; a build gate forces a rebuild loop, whereas a ref-resolution check
catches the naming mismatch before the build).

**The single solver-README change** (independent variable = the README only): edit
**Stage: Implementation** of `codex-ade-dbt-minimal/README.md`. Append a checklist
instruction: before treating the change as done, **enumerate every `ref()` and `source()`
reachable from the edited models**, and for each confirm the target either (a) is a model
in the project that will be built, or (b) is a declared source/seed that exists — matching
the exact name, case, and package/source namespace. Any `ref()`/`source()` that points at
a relation which is neither built nor declared is treated as an unfinished dependency the
solver MUST build or correctly rename (using local naming/source/ref patterns) before
moving on. No new stage is added; the existing "prove the edited area compiles or builds …
fix build/compile errors" line is kept and the checklist is added alongside it. Validation
and Finalization are untouched. The leak-guard / no-external-reference prose is kept
verbatim.

Target datasets (smoke): `intercom001`, `f1005`, `ana-eng002`, `asana003` — the four named
build-error exemplars, each a dangling/misnamed upstream the reference-resolution checklist
should catch (`asana003`'s wrong source name in particular tests the naming-mismatch path).
Near-miss control: `quickbooks003` (already builds clean at 12/14 — its refs already
resolve, so the checklist should be a no-op there and add no regression).

**Falsifiable.** If the reference-resolution checklist does not reduce the build-error
count on the smoke targets vs `@baseline` (targets still finalize with `Catalog Error`/0
target tests run), the hypothesis is rejected. Also rejected if `quickbooks003` regresses
below 12/14.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Only `codex-ade-dbt-minimal/README.md`'s **Stage: Implementation** prose changes (added
ref()/source() resolution checklist); no new stage, no leak-guard prose altered. Verified
by: `diff ../specs/baseline.yaml ../specs/h0003-resolve-dangling-refs-checklist.yaml` shows
only `experiment:` + `solver_workflow:` differ; the smoke spec additionally adds
`benchmark.tasks`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`.**
Behavioral read names, per smoke target, whether the agent enumerated/resolved the dangling
ref()/source() (method adherence) and whether the `Catalog Error` was thereby eliminated;
`quickbooks003` checked for non-regression.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
