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

## Stage Report: propose

- DONE: The forked solver README's ONLY change vs codex-ade-dbt-minimal/README.md is the single Exploration-stage package-fidelity instruction; leak-guard / no-external-reference prose intact; NO reference to hidden AUTO_*/verifier tests.
  `diff` shows a single 7-line addition at line 49 inside `## Stage: Exploration`; the no-external-reference paragraph (curl/wget/git clone/package-source) and dbt_packages preservation prose are untouched; the new text says "do not hand-roll a simpler aggregation" and "read that package's existing models" — local-only, no test/verifier mention.
- DONE: FULL spec specs/h0009-exploration-package-fidelity.yaml diffs specs/baseline.yaml in ONLY experiment: + solver_workflow:; the smoke spec adds ONLY benchmark.tasks: [intercom001, intercom003, asana002, asana004, asana005, quickbooks001, asana001]; agent.kind=spacedock_solver and runtime=codex preserved.
  See Gate evidence FULL spec diff (two lines). Smoke diff vs full adds only the 7-task `tasks:` block. Frozen smoke spec lines 4-5 confirm `kind: spacedock_solver` / `runtime: codex`.
- DONE: Both specs frozen with rk freeze --allow-missing (full + smoke); paste the two-field FULL spec diff and the README diff into a ### Gate evidence block.
  Wrote specs/h0009-exploration-package-fidelity.frozen.yaml and specs/h0009-exploration-package-fidelity.smoke.frozen.yaml; evidence below.

### Gate evidence

FULL spec diff (`diff specs/baseline.yaml specs/h0009-exploration-package-fidelity.yaml` — exactly two fields):

```
2c2
< experiment: ade-bench-baseline # variants: ade-bench-h0001-<slug>
---
> experiment: ade-bench-h0009-exploration-package-fidelity # variants: ade-bench-h0001-<slug>
11c11
<   solver_workflow: ./solver_workflows/codex-ade-dbt-minimal # variants repoint to ./solver_workflows/h<NNNN>-<slug>
---
>   solver_workflow: ./solver_workflows/h0009-exploration-package-fidelity # variants repoint to ./solver_workflows/h<NNNN>-<slug>
```

README diff (`diff solver_workflows/codex-ade-dbt-minimal/README.md solver_workflows/h0009-exploration-package-fidelity/README.md` — single Exploration-stage addition):

```
49a50,56
> When the project embeds a known dbt package (e.g. a Fivetran `*_source`/staging
> package in `dbt_packages/`), read that package's existing staging/intermediate
> models and reproduce their conventions exactly for the models you build or
> change: the active-record / `_fivetran_active` filtering, the dedup keys, the
> output column set, and the grain (one-row-per-which-entity); do not hand-roll a
> simpler aggregation that diverges from the package's join anchor and filters.
> 
```

Smoke spec diff vs FULL (`diff specs/h0009-exploration-package-fidelity.yaml specs/h0009-exploration-package-fidelity.smoke.yaml` — adds only benchmark.tasks):

```
23a24,31
>   tasks: # Fivetran package-fidelity cluster + asana001 stable-pass regression sentinel; ade-bench- prefixed (bare slugs rejected by rk run)
>     - ade-bench-intercom001
>     - ade-bench-intercom003
>     - ade-bench-asana002
>     - ade-bench-asana004
>     - ade-bench-asana005
>     - ade-bench-quickbooks001
>     - ade-bench-asana001
```

Frozen artifacts: `specs/h0009-exploration-package-fidelity.frozen.yaml` (full), `specs/h0009-exploration-package-fidelity.smoke.frozen.yaml` (smoke). Both preserve `agent.kind: spacedock_solver`, `runtime: codex`. `provenance.yaml` was regenerated by `rk freeze` (shared file; harness_git_sha bumped vs baseline.frozen — a freeze-time artifact, not a spec change).

### Summary

Forked the current @baseline solver (codex-ade-dbt-minimal, 622bdedac572b479) into solver_workflows/h0009-exploration-package-fidelity and added exactly one Exploration-stage instruction: when a known dbt package is present in dbt_packages/, read its staging/intermediate models and reproduce their conventions (active-record/_fivetran_active filtering, dedup keys, output column set, grain) rather than hand-rolling a divergent aggregation. Leak-guard prose (no public fetch/clone) is intact and the change references only the local package source — no hidden-test/verifier mention. FULL spec differs from baseline in only experiment: + solver_workflow:; the smoke spec adds only the 7-task Fivetran cluster + asana001 sentinel; both specs frozen.
