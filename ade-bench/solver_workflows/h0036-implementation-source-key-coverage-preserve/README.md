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

When a model is meant to carry ONE ROW PER raw-source key — a dimension or
per-entity table keyed by an id — a type change, dedup, or join must NOT silently
drop source rows. In particular, never cast a key to a NARROWER type that discards
non-conforming values: casting an id to integer when the source now holds
non-numeric string ids (e.g. hashed or alphanumeric ids) drops exactly those rows,
because the non-numeric values fail the cast and disappear. The same trap hides in
a join or filter that only matches numeric-shaped ids. Preserve every distinct key
in the raw source all the way through to the output; if the source key type changed
to a string, keep the key as a string end to end rather than narrowing it back. The
local acceptance signal is a RAW-SOURCE coverage anti-join: every distinct key in
the raw source appears in the output, so an anti-join FROM the raw source LEFT JOIN
the output (keeping rows with no match) returns zero rows. Read this against the RAW
SOURCE table and its key column — not against the model's own upstream/intermediate
output, and not against any expected or external row count. A non-empty anti-join
means the model is dropping source keys and the type change or join is narrowing the
key; an empty anti-join means coverage is preserved. This constrains the edit's
shape and reconciles against the raw source by a different route than the model's
own CTEs; it is not a check of the model against itself. (It does not force you to
ADD rows the source never had — a model that legitimately filters rows on a
business rule is fine; the rule only forbids LOSING distinct raw-source keys to a
narrowing type change or join.)

Worked example — keep the key as it is in the raw source; do NOT narrow it back to
a type that drops non-conforming values, and reconcile coverage against the raw
source:
```sql
-- BEFORE: the raw source key changed to a string and now holds some non-numeric
--   ids. Casting it (back) to integer NULLs/drops every non-numeric id, so those
--   distinct source keys never reach the output. This is a silent coverage drop.
select cast(s.key_col as integer) as key_col, s.attr_a, s.attr_b
from {{ source('raw', 'source_table') }} s

-- AFTER: carry the key in the type the raw source actually has (string), so every
--   distinct source key survives. No narrowing cast, no numeric-only join/filter.
select s.key_col, s.attr_a, s.attr_b
from {{ source('raw', 'source_table') }} s

-- COVERAGE ANTI-JOIN (acceptance signal, read against the RAW SOURCE, returns
--   zero rows when every distinct source key is present in the output):
select s.key_col
from {{ source('raw', 'source_table') }} s
left join {{ ref('the_output_model') }} o on o.key_col = s.key_col
where o.key_col is null
```

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
