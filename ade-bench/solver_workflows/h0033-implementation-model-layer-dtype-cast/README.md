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

Run basic confirmation as part of implementation. Use the cheapest command that
proves the edited area compiles or builds: `dbt compile`, targeted `dbt run`,
targeted `dbt test`, or selected `dbt build`. Fix build/compile errors caused by
your change before moving on. Build outputs can remain scratch state during
validation, but remove `target/` and `logs/` before finalizing unless the task
explicitly requires them. Do not remove `dbt_packages/` when it existed at task
start.

When you OBSERVE that one output column's stored type or representation differs
from what a peer signal says it should be — a sibling model that exposes the same
column with a different type, or the task instruction that names the intended
type/representation (e.g. it asks for a timestamp/date/integer but the column
materializes as text, or vice versa) — fix it with a MECHANICAL IN-PLACE `::<type>`
cast IN THE MODEL `.sql` that produces the column (e.g. `due_at::timestamp`,
`amount::numeric`). Two hard constraints:

- ADDITIVE / IN-PLACE ONLY. Cast the existing column where the model selects it;
  do NOT add, drop, or rename a column, and do NOT change its values — a cast only
  changes representation. Keep the column's name and position.
- EDIT THE MODEL `.sql`, NEVER the raw seed or source. The fix belongs in the
  `models/...sql` file that emits the column. Do NOT `ALTER` a seed table, do NOT
  rewrite the raw `*.duckdb`/`*.csv` seed data, and do NOT lean on
  `dbt_project.yml` seed `+column_types` to retype the upstream source — those edit
  the wrong layer and leave the model column unchanged. The graded artifact is the
  model SQL; the cast must land there.

Apply this ONLY to a specific column you have OBSERVED to mismatch a sibling/
instruction signal — do NOT broadly re-type every column to match a package or a
sibling's full convention, and do NOT impose one model's types on an unrelated
model. One observed mismatch, one in-place cast on that one column.

Worked example — a column the instruction/sibling implies is a timestamp is being
emitted as text; cast it in place in the MODEL `.sql`, not in the seed:
```sql
-- BEFORE: the model selects the raw column straight through, so it keeps the
--   upstream text/string representation that mismatches the intended timestamp.
select
    task_id,
    assignee_id,
    due_at,                       -- observed as text; sibling/instruction implies timestamp
    completed
from {{ ref('stg_asana__task') }}

-- AFTER: a single in-place ::timestamp cast on that ONE column, same name, same
--   position, values unchanged. No seed ALTER, no +column_types, no add/drop/rename.
select
    task_id,
    assignee_id,
    due_at::timestamp as due_at,  -- representation fixed IN THE MODEL .sql
    completed
from {{ ref('stg_asana__task') }}
```

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
