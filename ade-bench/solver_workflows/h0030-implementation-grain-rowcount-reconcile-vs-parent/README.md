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

When you author an aggregate or per-entity model whose grain is meant to be
COMPLETE over a parent key set — a per-entity or dimension model that should
expose one row per entity, or a date/calendar model that should be gap-free, as
described by its `schema.yml` entry or the task instruction — reconcile its grain
against an INDEPENDENT count taken from the raw parent, not against your own
judgment that the output looks right. Compute `COUNT(DISTINCT <key>)` directly on
the canonical raw PARENT source — a plain SELECT on the source relation, with NO
model logic; do NOT re-run, re-derive, or wrap your own model — and compare it to
your model's `COUNT(*)`. (For a date grain the parent is the complete date spine
between the source min and max date.) A shortfall is a SIGNAL TO INVESTIGATE, NOT
an automatic rewrite: re-read the model's intended grain, then — (i) if it is
meant to carry every parent key and some are missing, you grained on a filtered
child; rebuild FROM the parent (LEFT JOIN the child/aggregate relations onto it)
and re-reconcile; (ii) if the model is legitimately scoped to a subset, the
shortfall is EXPECTED — leave it. NEVER replace a simple, correct aggregate with
a structurally-different path merely to change the number. This rule does not
apply to aggregates with no canonical parent key set — do not invent a parent.

Worked example — reconcile produced count against the raw parent, rebuild only if
completeness is the intended grain:
```text
# 1. CONFIRM the intended grain from schema.yml / the instruction:
#    int_project_user_agg is meant to expose one row per project (complete).
# 2. COUNT(*) of your current model:
#    produced = 13
# 3. INDEPENDENT count from the RAW PARENT source (plain SELECT, no model logic):
#    expected = (select count(distinct project_id) from {{ source('app','projects') }})  -- 16
# 4. SHORTFALL (13 < 16) AND completeness is intended => you grained on a filtered
#    child; rebuild FROM the parent. (If the 13-row scope were legitimate, leave it.)
```
```sql
-- BEFORE: grained on a pre-filtered child — parent keys with no child row vanish
select project_id, count(*) as n_tasks
from {{ ref('int_project_tasks') }}   -- only projects that HAVE tasks
group by 1

-- AFTER: parent is the spine; the child aggregate is LEFT JOINed onto it, so
--   every parent key survives. COUNT(*) now reconciles to COUNT(DISTINCT) on parent.
select p.project_id, coalesce(c.n_tasks, 0) as n_tasks
from {{ source('app','projects') }} p        -- the canonical parent key set
left join (
    select project_id, count(*) as n_tasks
    from {{ ref('int_project_tasks') }}
    group by 1
) c using (project_id)
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
