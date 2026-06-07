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

When a repair is about completeness — the instruction says some rows are
missing and there should be a row for every value of a key — prefer a
subtractive, in-place edit over a rewrite: find the one narrowing filter that
is dropping rows and remove just that filter, while keeping the model's existing
`LEFT JOIN` and `GROUP BY` byte-for-byte intact. Do not restructure the query or
re-derive what the model already computes correctly. If the model carries a
secondary grouping column alongside the key (e.g. a category, type, or status
dimension), do NOT manufacture a row for every possible category value on every
key by cross-joining the distinct category values against the keys. Let each
category emerge per key through the join the model already has: a key's category
values are whatever its own joined rows produce, so the number of rows per key
VARIES with the data. A result where every key carries exactly (number of
distinct category values) rows — a constant (keys) × (categories) product — is
the signature of a wrong, over-producing cross join; if you see that pattern,
you have added a cross join that should not be there. This is a check on the
edit's shape against the model's own data, not a check against any external or
expected count.

Worked example — do NOT cross join the category dimension against the keys;
let it emerge per key through the join the model already has:
```sql
-- BEFORE: every distinct category value is CROSS JOINed against every key, so
--   each key is forced to carry exactly one row per category. rows-per-key is a
--   CONSTANT = (number of distinct category values); total rows = keys x
--   categories. This manufactures rows the data never had.
select k.key_col, c.category_col, count(fct.id) as n
from {{ ref('key_set') }} k
cross join (select distinct category_col from {{ ref('fact_detail') }}) c
left join {{ ref('fact_detail') }} fct
  on fct.key_col = k.key_col and fct.category_col = c.category_col
group by 1, 2

-- AFTER: drop the cross join. The category comes only from the EXISTING LEFT
--   JOIN onto the detail relation, then GROUP BY key + category. A key carries a
--   category row only when its own joined rows produce that category, so
--   rows-per-key VARIES with the data (some keys 0, some 1, some many) instead
--   of a constant keys x categories product.
select k.key_col, fct.category_col, count(fct.id) as n
from {{ ref('key_set') }} k
left join {{ ref('fact_detail') }} fct on fct.key_col = k.key_col
group by 1, 2
```

Run basic confirmation as part of implementation. Use the cheapest command that
proves the edited area compiles or builds: `dbt compile`, targeted `dbt run`,
targeted `dbt test`, or selected `dbt build`. Fix build/compile errors caused by
your change before moving on. Build outputs can remain scratch state during
validation, but remove `target/` and `logs/` before finalizing unless the task
explicitly requires them. Do not remove `dbt_packages/` when it existed at task
start.

When the model computes a rolling "over last N days" figure — a
window-suffixed column such as `_28d` / `_7d` / `_30d`, or an instruction asking
for a trailing-window total per period — express the window as a calendar-date
RANGE relative to each row's date, and COPY the window-join shape verbatim from
the project's own existing rolling-window sibling (an aggregate model that
already does this, typically a `*mom*` model that LEFT JOINs the date spine onto
the source on `source_date BETWEEN current_date - (M-1) AND current_date`),
changing ONLY the interval length to the N your column needs. Never express the
window as a fixed `rows between (N-1) preceding and current row` frame: that
frame counts ROWS, not calendar days, so on a sparse per-period grain (one row
per day-that-has-data, with gaps) it spans the wrong calendar span and
mis-counts the window total.

Worked example — copy the sibling's `BETWEEN current_date - (M-1) AND
current_date` join and change only the interval (here a 30-day sibling becomes
the 28-day window the model needs), instead of a `rows between` frame:
```sql
-- WRONG (rows-based frame): counts the previous (N-1) ROWS, not the previous N
--   calendar days. On a per-day grain that skips days with no data, the 28
--   preceding ROWS reach back far more than 28 calendar days, so the window
--   total is wrong.
-- select agg_date,
--        sum(metric) over (order by agg_date
--                          rows between 27 preceding and current row) as metric_28d
-- from daily_facts

-- RIGHT (calendar-date RANGE, lifted from the project's own *mom* sibling which
--   used `... - 29` for its 30-day window; change only 29 -> 27 for 28 days):
--   the sibling's shape is
--     left join review_cte
--       on review_cte.REVIEW_DATE::DATE
--          between dates_cte.DATE_ACTUAL::DATE - 29 and dates_cte.DATE_ACTUAL::DATE
select d.agg_date,
       sum(f.metric) as metric_28d
from period_dates d
left join daily_facts f
  on f.source_date::date between d.agg_date::date - 27 and d.agg_date::date
group by d.agg_date
```
The CTE/column names above are placeholders — substitute the actual local sibling
(its `*mom*`-style date-range join), date column, and source relation; change
only the interval number to match the N your column's name implies.

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
