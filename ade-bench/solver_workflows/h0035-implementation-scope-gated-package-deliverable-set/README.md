# Codex ADE dbt Minimal Workflow

Work in the task workspace as delivered by the benchmark harness. Do not clear
proxy environment variables or treat public-network access as a source-code fix.
The benchmark instruction is appended below these workflow instructions. The
graded artifact is the final dbt project source state; do not create an answer
file unless the task explicitly asks for one.

Do not fetch public reference material while solving. This includes `curl`,
`wget`, `git clone`, `git ls-remote`, package-source downloads, browser or web
lookup of upstream projects, and searches for published solutions. Use only the
local task workspace: installed packages, `dbt_packages/`, package manifests,
compiled artifacts, logs, macros, models, seeds, profiles, and project data.

Preserve existing dbt dependencies, package files, profiles, seeds, and macros
unless the task explicitly requires changing them. Hidden verifier tests may
depend on the existing project structure and package namespaces.

It is acceptable to run `dbt deps` for setup and validation when `packages.yml`
or `package-lock.yml` declares dependencies and `dbt_packages/` is absent.
Preserve any `dbt_packages/` directory already present at task start; the
verifier may reuse image-installed dependencies without registry access. Treat
`target/` and `logs/` as generated scratch state. Do not rewrite `packages.yml`,
`package-lock.yml`, package namespaces, profiles, or dependency macros unless the
task explicitly requires that change. In particular, never replace `dbt_utils`
or another declared package with a partial local shim; hidden verifier tests may
call package macros such as `dbt_utils.test_equality` even when visible models
only use one helper macro.

If `/razorback-freeze` exists and has exactly one child directory, write concise
stage notes there as `exploration.md`, `implementation.md`, and `validation.md`.
These notes are for resume/debug context; they are not the graded artifact.

## Stage: Exploration

Before editing, inspect the task instruction, project guidance files,
`dbt_project.yml`, `profiles.yml`, `packages.yml`, `package-lock.yml`, models,
macros, seeds, schema YAML, and existing logs.

Run cheap baseline probes when useful, such as `dbt compile --profiles-dir .`,
targeted `dbt run`, targeted `dbt test`, or log inspection. If a baseline probe
fails because declared packages are missing, run `dbt deps` before interpreting
the project as broken. For data-correctness tasks, sample relevant source tables
and current model outputs: row counts, nulls, duplicates, key distributions, and
representative rows.

Record suspected task type, affected files/models, baseline errors, and useful
data observations before making project changes.

## Stage: Implementation

Classify the task locally as no-op, repair, creation, refactor/config, or mixed.
Make the smallest task-relevant dbt project change, following local naming,
materialization, source, ref, macro, and schema patterns.

Referenced-but-absent staging models (scope-gated deliverable completion). When
the project's OWN ref-graph names a staging model that does not exist in
`models/`, and an already-installed package provides a template of that exact
name, materialize exactly that referenced-but-absent set. Derive the set
generically — do not hardcode model names:

- Collect the staging models the project itself references but does not define:
  scan the project's own `models/` and config/schema declarations
  (`dbt_project.yml` vars, `*.yml` schema, `int_*`/downstream model bodies) for
  `{{ ref('<stg_model>') }}` calls, then subtract the staging models that already
  have a file under `models/`. The completion set is exactly this set-difference
  — staging names the project references but has not built.
- Keep only those names for which an already-installed package (declared in
  `packages.yml` / present under `dbt_packages/`) ships a model template of that
  exact name. Materialize each one in the project's `models/` staging area from
  that installed template, following the local staging naming and materialization
  conventions (the same shape as the project's existing `stg_*` models, e.g. a
  `_tmp` + final pair if that is the local pattern). After this, the previously
  dangling `ref()`s resolve and the named models build.

Copyable shape (illustrative, not literal names): if the local ref-graph names
`{{ ref('stg_x__foo') }}` but `models/.../stg_x__foo.sql` is absent while the
installed package provides a `stg_x__foo` template, add
`models/<local-staging-path>/stg_x__foo.sql` mirroring the installed template and
the project's existing staging convention — repeating for each name in the
set-difference.

Scope-gate (load-bearing — do NOT cross it): fire ONLY on staging models the
project ALREADY references but that are absent. Never add a model the project
does not reference. Never treat an installed package as a new source, and never
invent `src_*` or `source()` declarations to satisfy a name. Never "complete" a
package's full model set on a project that does not reference the missing
members. A project whose ref-graph names no missing installed-package model gets
zero new models from this rule — leave it untouched.

Run basic confirmation as part of implementation. Use the cheapest command that
proves the edited area compiles or builds: `dbt compile`, targeted `dbt run`,
targeted `dbt test`, or selected `dbt build`. Fix build/compile errors caused by
your change before moving on. Build outputs can remain scratch state during
validation, but remove `target/` and `logs/` before finalizing unless the task
explicitly requires them. Do not remove `dbt_packages/` when it existed at task
start.

## Stage: Validation

Do additional correctness checks beyond "it builds".

For repairs, confirm the original failure mode is gone and the affected output
matches the source-data expectation. For refactors/config changes, check row
counts, schemas, and value-level behavior for affected and downstream models.
For new models or analysis tasks, check required columns, grain, uniqueness,
null behavior, row counts, and representative rows against source data. For
no-op tasks, confirm no project change was needed and leave files untouched.

Run broader dbt validation when practical for the task scope.

## Stage: Finalization

Leave only intended project changes. Remove scratch files unless the dbt project
requires them. Finish with changed files and concise validation evidence.
