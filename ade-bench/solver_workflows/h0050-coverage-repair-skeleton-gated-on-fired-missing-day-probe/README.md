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

A coverage repair (missing rows / missing days / a narrowed spine) is a SUBTRACTIVE,
in-place edit, but it is GATED on a FIRED local coverage probe — do NOT apply it to any
model that merely LOOKS coverage-shaped. FIRST run the probe; apply the edit only if the
probe FIRES. The probe is oracle-free — it uses only local task data, never a hidden test:
build the suspect model and compare the key/date coverage of its output against the complete
local dimension (the `dim_*` / reference table the model selects from). Concretely: collect
the set of dimension keys (e.g. every `date_col` in `{{ ref('dimension') }}`) and the set of
keys actually present in the model output; the probe FIRES iff the dimension contains one or
more keys ABSENT from the output (rows are genuinely missing). If every dimension key already
appears in the output (no missing rows — the spine is already complete, or the narrowing
predicate is in fact correct), the probe is EMPTY: do NOT make the subtractive edit, leave the
model BYTE-INTACT, and treat the task by its other classification (the real bug, if any, is
elsewhere — e.g. a YAML/config fix). Only when the probe FIRES make exactly these edits and
NOTHING ELSE: (1) delete the one narrowing membership predicate that filters the complete
dimension down to keys that already appear in the fact; (2) leave the aggregate expression
BYTE-INTACT — do not rewrite a COUNT(*) into COUNT(col), or change any SUM/AVG/window, while
repairing coverage; (3) leave the existing join and GROUP BY BYTE-INTACT — do not add a cross
join of a secondary category against the dimension. Let categories emerge per key through the
join the model already has.

PROBE (oracle-free, run it FIRST — decides whether to edit at all):
    -- missing keys = dimension keys NOT present in the model output
    select date_col from {{ ref('dimension') }}
    except
    select date_col from {{ ref('suspect_model') }}
    -- FIRES if this returns >=1 row (genuinely missing days/rows) -> apply the edit below.
    -- EMPTY (0 rows) -> spine already complete / predicate correct -> DO NOT edit; leave byte-intact.

BEFORE (the bug + the two over-eager rewrites to AVOID — only when the probe FIRED):
    with day_set as (
        select date_col from {{ ref('dimension') }}
        where date_col in (select distinct fact_date from {{ ref('fact_detail') }})  -- the narrowing predicate
    ),
    cats as (select distinct category_col from {{ ref('fact_detail') }}),       -- DO NOT add this
    grid as (select * from day_set cross join cats)                             -- DO NOT add this
    select count(fact.fact_date) as totals                                      -- DO NOT rewrite the aggregate
    from grid left join {{ ref('fact_detail') }} fact on ... group by ...

AFTER (drop the predicate, keep COUNT(*) byte-intact, no cross join):
    with day_set as (
        select date_col from {{ ref('dimension') }}                            -- narrowing predicate DELETED
    )
    select count(*) as totals                                                  -- aggregate UNCHANGED
    from day_set left join {{ ref('fact_detail') }} fact on ... group by ...   -- existing join + group by UNCHANGED

Run basic confirmation as part of implementation. Use the cheapest command that
proves the edited area compiles or builds: `dbt compile`, targeted `dbt run`,
targeted `dbt test`, or selected `dbt build`. Fix build/compile errors caused by
your change before moving on. Build outputs can remain scratch state during
validation, but remove `target/` and `logs/` before finalizing unless the task
explicitly requires them. Do not remove `dbt_packages/` when it existed at task
start.

When a task says an installed dbt package was updated, first classify package vars
and optional-resource behavior before editing. If a downstream model
unconditionally refs a package resource that can be disabled by an existing
package var, prefer a package-migration compatibility diagnostic: run or consider
a small disabled-var compile matrix and then repair the dependency graph with the
same existing vars. Do not start from casts, raw seed edits, or broad package
copying unless the optional-resource matrix is clean and another visible error
remains.

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
