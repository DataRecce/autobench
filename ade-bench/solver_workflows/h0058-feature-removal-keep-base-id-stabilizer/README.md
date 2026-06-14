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

When a task asks to remove, disable, or add a switch for a project-local feature,
keep the edit at the feature boundary. Do not turn a feature-boundary request
into a broad domain rewrite.

For removal requests, remove the config/variable and project-local logic whose
only purpose is that feature: feature-specific refs, CTEs, joins, select-list
outputs, and schema docs. Do not simply unwrap old conditional guards so the
feature stays active. Do not leave placeholder outputs whose only purpose was
the removed feature. Do not edit installed packages or dependency code unless
the task explicitly asks. Preserve ordinary raw/source attributes that are part
of the base entity or transaction and do not depend on the removed feature.

When removing a feature, drop the feature-ONLY derived column and its conditional join, but KEEP
the shared base id / foreign-key column that the rest of the project uses.

BEFORE (using_feature enabled):
    select t.entity_id,
           t.feature_fk_id,                         -- BASE column from the source/transaction
           {% if var('using_feature', True) %}
           dim.feature_label as feature_name,       -- FEATURE-ONLY derived column
           {% endif %}
    from t {% if var('using_feature', True) %} left join dim on dim.id = t.feature_fk_id {% endif %}

AFTER (remove the feature — keep the base fk, drop only the feature-only column + its join):
    select t.entity_id,
           t.feature_fk_id                          -- KEEP: shared base column (solution retains it)
    from t                                          -- DROPPED: the conditional join + feature_name

For toggle or disable requests, add the requested flag/default and guard only
the derived outputs and docs controlled by that feature. Preserve the enabled
path's existing formulas and behavior. Adjust unions, column alignment,
grouping, or downstream projections only as needed because disabled outputs
changed shape. Do not recompute unrelated formulas, signs, grains, joins, or
relationship semantics unless the task explicitly asks.

Before finalizing, search project-local files for remaining references to the
removed or disabled feature. Verify the default/disabled path has the intended
refs and outputs absent, and when an enabled path exists, verify it still
compiles or preserves the prior output shape.

BUILD / RENAME — PRESERVE THE COLUMN SET (gated). When a task asks to BUILD, CREATE, or RENAME
a model from a single upstream model, and it does NOT (a) remove/disable a feature or (b)
enumerate a restricted set of columns to keep, then PRESERVE every column from the upstream
model. Apply only the renames, keys, or casts the task names; carry all other columns through
unchanged. Do not prune the select to the columns you judge "relevant" — a downstream contract
may expect the full set.

(If the task removes/disables a feature, follow the feature-boundary rule above instead — there
you DO drop the feature-only columns.)

BEFORE (narrows to a judged-relevant subset — AVOID on a plain build/rename):
    select id as customer_id, company, last_name, first_name, email
    from {{ ref('upstream') }}

AFTER (preserve all upstream columns; apply only the named rename/key):
    select id as customer_id, company, last_name, first_name, email,
           /* …every remaining upstream column, unchanged… */
    from {{ ref('upstream') }}

A coverage repair (missing rows / missing days / a narrowed spine) is a SUBTRACTIVE,
in-place edit, but it is DOUBLE-GATED — apply it ONLY when BOTH preconditions hold, in this
order. Do NOT apply it to any model that merely LOOKS coverage-shaped.

GATE (a) — TASK INTENT (the FIRST test; cheapest, decides whether you even run the probe).
Read the task instruction. Apply the coverage repair only if the instruction EXPLICITLY calls
for row/date/key COMPLETENESS — phrasings like "there should be a row for every day", "every
<key> should be present", "rows are missing / fix the missing rows", "include all dates",
"one row per <key>". If the instruction does NOT request completeness — e.g. "the project is
broken", "create the NPS tables", "add a primary key", "rename the CTEs", or any ask unrelated
to coverage — then do NOT investigate or apply the coverage repair AT ALL, even if a model
looks coverage-shaped or the probe below would return rows. Treat the task by its ACTUAL ask
and leave coverage-shaped models BYTE-INTACT. Only when intent IS completeness do you proceed
to gate (b).

GATE (b) — FIRED local coverage probe (only reached if gate (a) passed). Run the probe; apply
the edit only if the probe FIRES. The probe is oracle-free — it uses only local task data,
never a hidden test: build the suspect model and compare the key/date coverage of its output
against the complete local dimension (the `dim_*` / reference table the model selects from).
Concretely: collect the set of dimension keys (e.g. every `date_col` in `{{ ref('dimension') }}`)
and the set of keys actually present in the model output; the probe FIRES iff the dimension
contains one or more keys ABSENT from the output (rows are genuinely missing). If every
dimension key already appears in the output (no missing rows — the spine is already complete,
or the narrowing predicate is in fact correct), the probe is EMPTY: do NOT make the subtractive
edit, leave the model BYTE-INTACT, and treat the task by its other classification (the real
bug, if any, is elsewhere — e.g. a YAML/config fix). Only when BOTH gate (a) AND gate (b) hold
make exactly these edits and NOTHING ELSE: (1) delete the one narrowing membership predicate
that filters the complete
dimension down to keys that already appear in the fact; (2) leave the aggregate expression
BYTE-INTACT — do not rewrite a COUNT(*) into COUNT(col), or change any SUM/AVG/window, while
repairing coverage; (3) leave the existing join and GROUP BY BYTE-INTACT — do not add a cross
join of a secondary category against the dimension. Let categories emerge per key through the
join the model already has.

PROBE for gate (b) (oracle-free, run ONLY after gate (a) intent-check passed):
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

PER-KEY METRIC AGGREGATE (gated). When a task asks to BUILD or create a per-key metric
aggregate (e.g. an NPS / review / rating rollup keyed by listing/customer/entity) and the
instruction does NOT request row/key COMPLETENESS (no "a row for every <key>", "include all
<keys>", "rows are missing"), scope the output to keys that actually have fact rows: build the
aggregate FROM the fact and INNER JOIN the key's metadata. Do NOT LEFT JOIN the full key
dimension and emit keys with zero fact rows carrying NULL metrics.

(If the instruction DOES request completeness, this rule does not apply — follow the
coverage-repair rule above instead.)

BEFORE (keeps zero-fact keys as NULL-metric rows — AVOID when completeness is not asked):
    select dim.key, agg.metric
    from {{ ref('key_dimension') }} dim
    left join fact_agg agg using (key)        -- emits NULL-metric rows for zero-fact keys

AFTER (scope to keys present in the fact):
    select dim.key, agg.metric
    from fact_agg agg                          -- driven by the fact
    inner join {{ ref('key_dimension') }} dim using (key)   -- zero-fact keys excluded

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

When repairing season/entity totals from *_standings tables, treat points as
cumulative race-by-race snapshots unless local evidence proves otherwise. If a
task says points are too high and the model currently sums standings points,
prefer the same-grain aggregate repair: replace sum(points) with max(points) in
every named affected model.

Do not switch to latest-row, rank, row_number, QUALIFY, order-by-final-race, or
race-results recomputation unless local evidence proves max(points) is wrong.
Before finalizing, inspect the edited SQL: the load-bearing fix should preserve
the existing entity/season grain and use max(points), not final-row selection.

LAP-TIME (and similar duration) AVERAGE WITH PIT STOPS (gated). When a task asks for an
average/aggregate of lap times (or analogous per-event durations) that must "account for"
pit stops, EXCLUDE the pit-stop laps before the aggregate. Do NOT keep pit-stop laps in the
spine and subtract pit-stop duration from the lap time.

BEFORE (keeps pit laps, subtracts duration — AVOID):
    select track, year, avg(lap_time - pit_stop_duration) as avg_lap
    from laps group by track, year

AFTER (drop pit laps, then average):
    select track, year, avg(lap_time) as avg_lap
    from laps
    where not is_pit_lap                      -- pit-stop laps excluded before the average
    group by track, year

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
