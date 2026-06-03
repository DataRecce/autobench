---
id: h0009
title: Exploration — reproduce the installed dbt package's conventions (grain, active-filter, dedup, column set) instead of hand-rolling
status: propose
kind: hypothesis
source: forked from the h0005 @baseline (622bdedac572b479, 31/48 = 0.6458) 17-failure raw-log analysis + h0007's rejection note (surviving direction #2 — "improve the solver's up-front understanding so it does not form the wrong mental model"). Queued behind h0008; both attack the same failures from different stages (Finalization invariants vs Exploration root-cause). solver_workflows/codex-ade-dbt-minimal at fork (re-fork from whatever @baseline is when this fires).
started: 2026-06-03T14:07:16Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

A large share of the `@baseline` failures sit on **Fivetran-package** datasets
(asana, intercom, quickbooks — ~8 of 17) whose canonical answer closely mirrors the
modeling conventions of the dbt package already installed in the local `dbt_packages/`
tree. The solver fails them by **hand-rolling a plausible-but-divergent transformation**
instead of reproducing the installed package's idioms: it skips the `_fivetran_active`
active-record filter (intercom grain: 2 expected vs 5 emitted), invents a join grain that
drops base-entity rows (asana `int_asana__project_user_agg`), or misses a package-shaped
cast (asana002 `due_at::timestamp`). The package source is a **local, leak-guard-allowed**
signal the solver under-uses.

**Falsifiable claim (the single README change — Exploration stage only):** the seed
solver's Exploration prose inspects project files generically but does NOT direct the
solver to study and reproduce the conventions of any dbt package already present in
`dbt_packages/`. Adding one Exploration instruction — *when the project embeds a known dbt
package (e.g. a Fivetran `*_source`/staging package in `dbt_packages/`), read that
package's existing staging/intermediate models and reproduce their conventions exactly for
the models you build or change: the active-record / `_fivetran_active` filtering, the
dedup keys, the output column set, and the grain (one-row-per-which-entity); do not
hand-roll a simpler aggregation that diverges from the package's join anchor and filters*
— will fix the root-cause mental-model error on the Fivetran cluster, flipping a material
number of those failures to passes and raising `stratified_pass_at_1` above whatever
`@baseline` is when this fires.

Distinct from h0008 (Finalization invariants, a detect-and-fix check): this is a
generative Exploration change that prevents the wrong model from being built in the first
place. One idea, one stage.

Method/README change only. Forks the then-current `@baseline` solver; no dataset, harness,
or solver-runtime change. Leak-guard intact (the package source is local — no public
fetch, no `git clone` of the upstream package, no oracle).

Target datasets (smoke, all `ade-bench-` prefixed): the Fivetran cluster —
`ade-bench-intercom001`, `ade-bench-intercom003`, `ade-bench-asana002`,
`ade-bench-asana004`, `ade-bench-asana005`, `ade-bench-quickbooks001`, plus a
stable-pass regression sentinel `ade-bench-asana001`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0009-exploration-package-fidelity.yaml` shows
only `experiment:` + `solver_workflow:`; the README diff vs the `@baseline` solver touches
only `## Stage: Exploration` (the single package-fidelity instruction), leaves
Implementation/Validation/Finalization and the dependency/package guardrails untouched, and
does not reference hidden tests or weaken the leak-guard. `agent.kind: spacedock_solver`,
`runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean,
`captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs the then-current `@baseline`.**

**Smoke gate:** must not regress the `asana001` sentinel and should flip at least one
targeted Fivetran failure to a pass before promotion to full.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
