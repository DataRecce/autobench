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

## Stage: Output Contract

Run this stage only when the task requires you to **author or restructure** one or
more models (creation, refactor/config, or the model-building part of a mixed task).
**Skip it entirely for no-op and pure-repair tasks**: on a no-op, change nothing; on a
repair, the contract is already fixed by the existing model and downstream consumers, so
go straight to Implementation and make the smallest fix. Do not invent a contract a
plain repair does not need.

When it does apply, **write the contract down before you write any model SQL.** For each
model you must deliver, derive these four things from the local workspace only and record
them (in the freeze notes if available, otherwise as a short comment block you keep next
to your work):

1. **Grain — what one row is, and which key set must be present.** Name the exact key
   column(s) and, critically, the *source of the full key set*. The full key set is the
   relation the existing code or the instruction treats as the driver — the table that is
   the `FROM` / left-most relation onto which other relations are `LEFT JOIN`ed, the table
   the instruction names as the thing being described, or the relation a stated uniqueness
   rule applies to. If the instruction says the model is unique on a key, that key is the
   grain. If you are extracting CTEs out of an existing model, the new model's key set must
   stay the key set those CTEs produced *before* the downstream model re-keyed or
   `coalesce`d them — do not narrow it to only the keys that have matching child rows.
2. **Columns — the full required set, in order.** If a `schema.yml` / `*.yml` declares
   `columns:` for this model, that ordered list is the contract; reproduce every declared
   column. If no yml declares this model, derive the column set from the relations you are
   selecting from (the upstream models' / sources' `SELECT` lists) plus the convention of
   the closest sibling model of the *same kind* (e.g. another model in the same directory
   that joins the same dims onto a fact). Use the instruction's named columns verbatim when
   it lists them.
3. **Types.** For each column, take the type from the relation it is sourced from. When you
   are matching a model to an installed package's staging model (the package is resolved in
   `dbt_packages/`), read that package model's column and adopt its type for the same-named
   column — apply the matching cast in place. A local yml description is *not* a type
   source; types come from the upstream relation or the installed package model.
4. **Deliverable set — every model that must exist.** Resolve the full `ref()` graph: if a
   local model `ref()`s a model that does not exist, that missing model is part of the
   deliverable set. If an installed package in `dbt_packages/` ships a model your local
   models `ref()` by name, that package model is the template for the one you must
   reproduce. Cross-check against any yml that declares models.

**Then build to satisfy the written contract**, and treat the contract as the acceptance
condition for the Implementation stage: a model is not done until its committed SQL emits
exactly the recorded grain key set, the recorded columns in order, and the recorded types.

Two guards on the contract itself:

- **Same-thing, same-shape only.** Only adopt a key set, column, type, or template from a
  local relation that is genuinely the analog for *this* model — the spine the code already
  joins onto, a same-layer sibling, or the installed package model for the same staging
  entity. Do not import naming, grain, or columns from a relation that is not the analog,
  and do not impose a package convention on a model that has no package analog. Where a
  local signal and the project's own existing structure conflict, keep the project's
  structure.
- **Derive, do not pad.** Only list a column you can point to in a local relation, an
  instruction, or a declaring yml for *this* model. If a yml appears to declare more
  columns than the relations you select from can produce, prefer the columns the data and
  instruction actually support; do not fabricate columns to match an over-broad
  declaration.

Worked derivation (refactor example, fully local). Instruction: *"refactor `asana__project`
into a new intermediate model … do the calculations done in the `agg_project_users` and
`count_project_users` CTEs in a new model `int_asana__project_user_agg` with columns
`project_id`, `users`, `number_of_users_involved` … then update `asana__project` to use it."*
Open the model named in the instruction (`models/asana__project.sql`) and read how those two
CTEs feed the rest of the model:

- The CTEs `agg_project_users` and `count_project_users` each `group by project_id` over
  `int_asana__project_user` — so their *own* key set is the set of `project_id`s that have a
  matching user, which is **narrower** than the full project list.
- But in the assembling CTE (`project_join`) the model does
  `from project left join agg_project_users … left join count_project_users …` and applies
  `coalesce(count_project_users.number_of_users_involved, 0)` **there**, after the join.

Contract derivation for the new `int_asana__project_user_agg`: (1) **Grain** = one row per
`project_id`; the full key set is the keys the CTE output is *consumed against*, i.e. the
CTE output as-is (do not pre-filter or re-key it) — the new model must reproduce exactly
what those CTEs produced, with no `coalesce` and no narrowing, because the `coalesce` and the
full-project spine live downstream in `asana__project` and must stay there. (2) **Columns**
= `project_id`, `users`, `number_of_users_involved` (instruction-named, in order).
(3) **Types** = inherited from `int_asana__project_user` / the existing CTE expressions.
(4) **Deliverable set** = the one new intermediate model plus the edit to `asana__project`
so it `ref()`s the new model in place of the two inline CTEs, with the existing downstream
`coalesce(...)`/spine join left intact. A secondary local check: `intermediate_asana.yml`
declares a `dbt_utils.unique_combination_of_columns` test on the upstream
`int_asana__project_user`, confirming that is the child grain you are aggregating from. With
the contract written this way, Implementation is a fill-in (lift the CTE bodies verbatim into
the new model, repoint the `ref`) rather than a re-derivation — and you do not silently move
the `coalesce`/spine into the new model, which would change its grain.

## Stage: Implementation

Classify the task locally as no-op, repair, creation, refactor/config, or mixed.
Make the smallest task-relevant dbt project change, following local naming,
materialization, source, ref, macro, and schema patterns.

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
