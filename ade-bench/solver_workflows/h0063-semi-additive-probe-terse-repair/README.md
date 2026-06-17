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

The following gated rules each apply ONLY to their named task shape; when a task
does not match a rule's gate, ignore that rule entirely and treat the task by its
actual classification. Each rule is one principle, its gate, and one generic
BEFORE/AFTER skeleton.

FEATURE-BOUNDARY REMOVE / TOGGLE / DISABLE (gated). When a task asks to remove,
disable, or add a switch for a project-local feature, keep the edit at the feature
boundary: drop or guard the feature-ONLY derived columns, refs, CTEs, joins,
select outputs, and docs, but KEEP the shared base id / foreign-key column the
rest of the project uses. Do not unwrap conditional guards so the feature stays
active, do not leave placeholder outputs, and do not turn it into a broad domain
rewrite.

BEFORE (feature enabled):
    select t.entity_id,
           t.feature_fk_id,                      -- BASE column from the source/transaction
           {% if var('using_feature', True) %}
           dim.feature_label as feature_name,     -- FEATURE-ONLY derived column
           {% endif %}
    from t {% if var('using_feature', True) %} left join dim on dim.id = t.feature_fk_id {% endif %}

AFTER (remove the feature — keep the base fk, drop only the feature-only column + its join):
    select t.entity_id,
           t.feature_fk_id                        -- KEEP: shared base column
    from t                                        -- DROPPED: the conditional join + feature_name

BUILD / RENAME — PRESERVE THE COLUMN SET (gated). When a task asks to BUILD,
CREATE, or RENAME a model from a single upstream model, and it does NOT (a)
remove/disable a feature or (b) enumerate a restricted set of columns to keep,
PRESERVE every upstream column; apply only the named renames/keys/casts and carry
all others through unchanged. Do not prune to a "relevant" subset.

BEFORE (narrows to a judged-relevant subset — AVOID on a plain build/rename):
    select id as new_id, col_a, col_b
    from {{ ref('upstream') }}

AFTER (preserve all upstream columns; apply only the named rename/key):
    select id as new_id, col_a, col_b,
           /* …every remaining upstream column, unchanged… */
    from {{ ref('upstream') }}

COVERAGE REPAIR — DOUBLE-GATED (gated). A coverage repair (missing rows / missing
days / a narrowed spine) is a SUBTRACTIVE in-place edit; apply it ONLY when BOTH
preconditions hold, in order. Gate (a) TASK INTENT: the instruction EXPLICITLY
asks for row/date/key COMPLETENESS ("a row for every day", "every <key> present",
"rows are missing", "include all dates"); if the ask is anything else ("project is
broken", "create the NPS tables", "add a primary key", "rename the CTEs"), do NOT
investigate or apply it at all — leave coverage-shaped models BYTE-INTACT. Gate
(b) FIRED local probe (oracle-free, only after gate (a)): collect the dimension's
keys and the model output's keys; the probe FIRES iff the dimension has ≥1 key
ABSENT from the output. If EMPTY, leave the model byte-intact and treat the task
by its other classification. Only when BOTH gates hold, make the minimal
subtractive edit — delete the one narrowing membership predicate — and do NOT
rewrite aggregates (keep `COUNT(*)`/SUM/AVG/window byte-intact) or add joins (no
cross join of a secondary category) while repairing coverage.

PROBE for gate (b) (oracle-free, run ONLY after gate (a) passed):
    select key_col from {{ ref('dimension') }}
    except
    select key_col from {{ ref('suspect_model') }}
    -- FIRES if >=1 row (genuinely missing) -> apply the edit. EMPTY -> DO NOT edit.

BEFORE (the narrowing predicate — only when the probe FIRED):
    with day_set as (
        select key_col from {{ ref('dimension') }}
        where key_col in (select distinct fact_key from {{ ref('fact_detail') }})  -- narrowing predicate
    )
    select count(*) as totals
    from day_set left join {{ ref('fact_detail') }} fact on ... group by ...

AFTER (drop the predicate, aggregate + join byte-intact):
    with day_set as (
        select key_col from {{ ref('dimension') }}                              -- predicate DELETED
    )
    select count(*) as totals                                                   -- aggregate UNCHANGED
    from day_set left join {{ ref('fact_detail') }} fact on ... group by ...    -- join + group by UNCHANGED

PER-KEY METRIC AGGREGATE (gated). When a task asks to BUILD a per-key metric
aggregate (an NPS / review / rating rollup keyed by listing/customer/entity) and
does NOT request completeness, scope the output to keys that actually have fact
rows: build FROM the fact and INNER JOIN the key's metadata. Do NOT LEFT JOIN the
full key dimension and emit zero-fact keys with NULL metrics. (If completeness IS
asked, follow the coverage-repair rule instead.)

BEFORE (keeps zero-fact keys as NULL-metric rows — AVOID when completeness not asked):
    select dim.key, agg.metric
    from {{ ref('key_dimension') }} dim
    left join fact_agg agg using (key)        -- emits NULL-metric rows for zero-fact keys

AFTER (scope to keys present in the fact):
    select dim.key, agg.metric
    from fact_agg agg                          -- driven by the fact
    inner join {{ ref('key_dimension') }} dim using (key)   -- zero-fact keys excluded

TMP/INTERMEDIATE-TIER REMOVAL — BEHAVIOR-PRESERVING INLINE (gated). When a task
asks to remove a tmp/intermediate tier and point the consuming stg model at the
source, RECONCILE before==after: the correct output is whatever the project
produced BEFORE the refactor, so first build as-is and capture each affected
model's column set + row count, then rewire and confirm columns/types/row counts
are identical. Copy the deleted tmp model's SELECT — exact columns, casts,
aliases, WHERE — verbatim into the stg model, changing ONLY the FROM/ref to the
source; do NOT re-derive, drop, rename, or re-cast. A clean `dbt run` is NOT
sufficient proof — only the before==after reconciliation is.

BEFORE (re-derives the stg model fresh — AVOID; drifts the output):
    select id, name, created                      -- a fresh "reasonable" subset/cast — DRIFTS
    from {{ source('pkg','entity') }}

AFTER (inline the deleted tmp model's EXACT select; swap only the FROM):
    select id,
           cast(name as varchar) as name,
           coalesce(created, '1970-01-01') as created,
           ... every other column the tmp model produced, unchanged ...
    from {{ source('pkg','entity') }}             -- was {{ ref('stg_entity_tmp') }}

Run basic confirmation as part of implementation. Use the cheapest command that
proves the edited area compiles or builds: `dbt compile`, targeted `dbt run`,
targeted `dbt test`, or selected `dbt build`. Fix build/compile errors caused by
your change before moving on. Build outputs can remain scratch state during
validation, but remove `target/` and `logs/` before finalizing unless the task
explicitly requires them. Do not remove `dbt_packages/` when it existed at task
start.

PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX (gated). When a task says an installed dbt
package was updated, classify package vars and optional-resource behavior before
editing. If a downstream model unconditionally refs a package resource that an
existing package var can disable, prefer a package-migration compatibility
diagnostic: run a small disabled-var compile matrix, then repair the dependency
graph with the same existing vars. Do not start from casts, raw seed edits, or
broad package copying unless the optional-resource matrix is clean and another
visible error remains.

SEMI-ADDITIVE / SNAPSHOT MEASURE — max() AT ENTITY GRAIN (gated). When repairing
entity/period totals that are too high and the model sums a numeric measure across a
sequence within each entity, check how the measure moves when each entity's rows are
ordered by the sequence key. If it trends non-decreasing APART FROM A FEW ISOLATED
DROPS (rare penalties, corrections, or restatements — a handful of rows relative to
the sequence length), it is still a running cumulative total, NOT a per-period delta:
replace `sum(measure)` with `max(measure)` at the existing entity/period grain in
every affected model. A handful of decreases does NOT make it additive and does NOT
justify selecting a single latest row — `max()` at the grain is still the minimal
correct repair (it ignores the dips). Reserve `sum()` ONLY for a measure that rises
and falls SYSTEMATICALLY (frequent decreases — a genuine per-period delta). Do NOT
switch to latest-row, rank, row_number, QUALIFY, order-by-final-period, or
results-recomputation.

EXCLUDE-A-CATEGORY AVERAGE (gated). When an average/aggregate must exclude a row
category (e.g. a lap-time average that must "account for" pit stops), filter that
category out BEFORE the aggregate; do NOT keep the rows and subtract their
contribution.

BEFORE (keeps the excluded rows, subtracts — AVOID):
    select grp, avg(value - excluded_part) as avg_value
    from t group by grp

AFTER (drop the excluded category, then average):
    select grp, avg(value) as avg_value
    from t
    where not is_excluded_category             -- excluded rows removed before the average
    group by grp

SRC-MODEL BARE-PREFIX NAMING (gated). When a task asks to BUILD `src` models for a
raw->src->stg pipeline, name each new src model exactly `src_<table>`, matching the
raw table name with a bare `src_` prefix; do NOT prepend the staging
dataset/namespace (`src_<dataset>__<table>` is WRONG). Then each
`stg_<dataset>__<table>` model `ref('src_<table>')` for its own table (stg models
joining additional tables keep their other refs). Apply only when the task itself
asks for `src_` models.

BEFORE (over-applies the namespace to the src name — AVOID):
    -- models/src/src_<dataset>__<table>.sql      <- WRONG name
    -- stg: from {{ ref('src_<dataset>__<table>') }}   <- WRONG ref

AFTER (bare src_<table> name; stg refs the bare-prefix src):
    -- models/src/src_<table>.sql                 <- matches the raw table name
    -- stg: from {{ ref('src_<table>') }}              <- refs src_<table>

TOP-N TIE-CROSSES-CUTOFF (gated). When a task asks which `order by <metric> desc
limit N` models (without a deterministic tiebreaker) give "inconsistent results
given the current data", a model is inconsistent ONLY when a tie CROSSES THE
CUTOFF — the metric of row N also occurs at row N+1, so the final slot is
nondeterministic. A tie entirely inside (or outside) the top N reorders display
only — do NOT count it. Locally computable from shipped data: inconsistent iff
`count(rows with metric >= the N-th value) > N`. Exclude any model the prompt
already classifies as a worked example.

BEFORE (counts any tie, including in-list ties — AVOID): over-includes.

AFTER (count only a tie that crosses the cutoff boundary):
    select case when (
        select count(*) from <candidate_model> where metric >= (
            select metric from <candidate_model> order by metric desc limit 1 offset (N-1)
        )
    ) > N then 'inconsistent' else 'consistent' end
    -- include only when 'inconsistent'; exclude the prompt's worked example.

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
