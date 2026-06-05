---
id: h0015
title: Implementation — on repair/fix-it tasks, create the package-implied models that are missing by copying the installed package's definition
status: propose
kind: hypothesis
source: forked from the h0009 smoke deep-dive — quickbooks001 is a separate gap from the grain-spine cluster: it is a passive "the project is broken, fix it" task where the solver fixes the one visible compile error, sees the build go green, and STOPS — even though dbt_packages/quickbooks_source literally contains the 3 missing staging models the grader wants (stg_quickbooks__estimate/refund_receipt/sales_receipt). Plays to the one proven mechanism (h0009 asana002: copying a concrete local package artifact LANDS; h0010 showed prose-described structural rewrites do NOT). Forks the then-current @baseline (re-fork at propose; @baseline 622bdedac572b479 unless h0009 promotes first).
started: 2026-06-05T08:58:01Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`quickbooks001` is a "the project is erroring out, fix it" task. The solver fixes the one
visible compile error (a missing `quickbooks__general_ledger` ref), the project then builds
green, and it **declares done** — but the grader expects 3 staging models
(`stg_quickbooks__{estimate,refund_receipt,sales_receipt}`) that were never created. Both
`@baseline` and h0009 failed all 6 of those checks (existence + equality) identically. The
key fact: those 3 models are **present in the installed `quickbooks_source` package** under
`dbt_packages/` — the answer is local and copyable, not something to invent. The solver
never looked because a passive "fix-it" framing gave it no trigger to build anything once
the project compiled.

This plays directly to the mechanism that WORKS: h0009's only flip (asana002) came from the
solver **copying a concrete local package artifact** (a column-type contract); h0010 proved
the solver will NOT implement a structurally-described rewrite from prose. Copying a
package-defined model is the former, not the latter.

**Falsifiable claim (the single README change — Implementation stage only):** the seed
solver's Implementation prose classifies the task (no-op/repair/creation/…) and fixes the
smallest visible failure, but for **repair / "broken project" tasks it stops at "builds
green"** and never checks for package-implied models that should exist but don't. Adding one
Implementation instruction — *on a repair / "fix the broken project" task, "builds green" is
necessary but NOT sufficient: enumerate the staging/intermediate models the installed
package(s) under `dbt_packages/` and the project's own schema/refs imply the project should
expose, and for any that are absent, create them by reproducing the installed package's
definition for that entity (copy the package's model/macro usage; do not hand-roll). Do not
finalize a repair task while a package-implied model the project is meant to expose is
missing* — will create the 3 missing quickbooks staging models and flip `quickbooks001`,
raising `stratified_pass_at_1` above `@baseline`.

Method/README change only; forks the then-current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal` unless h0009 promotes first), runtime codex,
gpt-5.5. Leak-guard intact: the source is the **local** `dbt_packages/` tree and the
project's own schema/refs — no public fetch, no `git clone`, no oracle, no reference to the
hidden `AUTO_*` tests. One idea, one stage (Implementation, repair-task handling).

Target datasets (smoke, all `ade-bench-` prefixed): `ade-bench-quickbooks001` (the 3
missing-model target) + `ade-bench-ana-eng007-medium` (another "the project is broken, fix
it" task) + a stable-`@baseline`-pass regression sentinel `ade-bench-quickbooks004`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0015-implementation-repair-package-model-coverage.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs the `@baseline` solver
touches only `## Stage: Implementation` (the single repair-coverage instruction), leaves the
other stages + dependency/package guardrails untouched, and does not reference hidden
`AUTO_*`/verifier tests or weaken the leak-guard. `agent.kind: spacedock_solver`,
`runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean,
`captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
plus the absolute `stratified_pass_at_1` vs `@baseline`.**

**Smoke gate:** must not regress the `quickbooks004` sentinel and should flip
`quickbooks001` (and/or `ana-eng007-medium`) to a pass; the post-smoke deep-dive must
confirm the solver actually CREATED the missing models from the package (artifact check),
not merely discussed coverage.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
