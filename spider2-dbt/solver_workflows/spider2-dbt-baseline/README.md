# Codex Spider2-DBT Baseline Solver Workflow

Work in the task workspace as delivered by the benchmark harness. The benchmark
instruction is appended below these workflow instructions. This is a
**text-to-dbt** task: the instruction describes one or more analytic results to
produce, and you deliver them by ADDING (or completing) dbt models in the
project. The graded artifact is the project's built DuckDB — the verifier opens
it and compares specific result tables against a hidden gold. Do not write a
free-text answer file.

Do not fetch public reference material while solving. This includes `curl`,
`wget`, `git clone`, `git ls-remote`, package-source downloads, browser or web
lookup of upstream projects, and searches for published solutions. Use only the
local task workspace: installed packages, `dbt_packages/`, package manifests,
compiled artifacts, logs, macros, models, seeds, profiles, and project data.

Preserve existing dbt dependencies, package files, profiles, seeds, and macros
unless the task explicitly requires changing them. It is acceptable to run
`dbt deps` for setup when `packages.yml`/`package-lock.yml` declares dependencies
and `dbt_packages/` is absent; preserve any `dbt_packages/` already present. In
particular, never replace `dbt_utils` or another declared package with a partial
local shim; hidden verifier tests may call package macros. Treat `target/` and
`logs/` as generated scratch state.

## THE OUTPUT CONTRACT (load-bearing — this is how the task is graded)

The verifier compares the **tables that exist in the built DuckDB by name**
against gold, column-by-column (row order is ignored; comparison is column
CONTAINMENT — every gold column must match some predicted column, but EXTRA
predicted columns are harmless). Gold table names and their exact columns are NOT
given to you — produce them from the instruction plus the project's own
conventions. Getting the table name, the grain, or the row set wrong scores zero
even if the logic is sound.

1. DELIVERABLE = NEW MATERIALIZED MODEL(S). The result is almost never already
   built. Create a new model (`.sql` under `models/`) for EACH result table the
   instruction describes — there may be several (e.g. a dimension + a fact + a
   one-big-table).

2. EVERY TARGET MUST LAND AS A BASE TABLE — NOT EPHEMERAL. The verifier can only
   compare a table that physically exists in the output DuckDB. A model
   materialized `ephemeral` compiles into a CTE and creates NO table → an
   automatic zero for that target, even if its SQL is perfect. Check the
   per-directory `materialized:` config in `dbt_project.yml` for where you put
   each target; if that path defaults to `ephemeral` (or `view` when gold expects
   a table), OVERRIDE it in the model: `{{ config(materialized='table') }}`. Do
   not bury a target under an intermediate/ephemeral folder and assume it appears.

3. NAME EACH MODEL BY THE PROJECT'S EXISTING CONVENTION. Before writing SQL, list
   the existing model filenames and read their prefixes — they ARE the naming
   contract. Match it exactly for the new entity named in the instruction:
   - dimensional projects use `stg_*` → `int_*`/`dim_*`/`fct_*` → `obt_*` (one
     big table). "A comprehensive <X> table combining …" with `dim_`/`fct_`
     siblings present → build `dim_<entity>`, `fct_<entity>`, and `obt_<entity>`.
   - package-style projects use `<pkg>__<entity>_<suffix>` (e.g.
     `jira__issue_enhanced`); a request about a new entity →
     `<pkg>__<that_entity>_<same_suffix>` (e.g. `jira__project_enhanced`).
   - method/variant projects use `<dataset>__<method>_<n>`; the instruction names
     the methods (e.g. "aggregate after", "aggregate all ever") → build
     `<dataset>__aggregate_after_<n>`, `<dataset>__aggregate_all_ever_<n>`.
   A dbt model's materialized table name is its filename stem unless `alias` is
   set — name the FILE as the target table; do not add an alias that changes it.

4. GRAIN + ROW SET — DON'T ZERO-FILL. Scope the output to the entities that
   actually have the activity the instruction is about. Build FROM the relevant
   fact/event table and INNER JOIN the dimension; do NOT LEFT JOIN the full
   dimension and emit zero-activity rows padded with 0/NULL metrics — those
   phantom rows change the row count and fail the comparison. (Only emit every
   dimension key when the instruction explicitly asks for completeness.) One row
   per <entity> at the implied grain.

5. SCHEMA / LOCATION. Build into the project's default schema (the active
   `profiles.yml` output, normally `main`) so the table is visible at the top
   level of the output DuckDB.

6. COLUMNS. Emit the natural/business key(s) first, then every described
   attribute and metric, at the implied grain. Because grading is containment,
   extra columns are harmless — so when unsure whether a column belongs, KEEP it
   rather than prune; only never DROP a described column. Reuse the project's
   existing `stg_*`/`int_*` models and declared `source()`s as inputs rather than
   re-reading raw tables ad hoc.

## Stage: Exploration

Inspect the instruction, `dbt_project.yml` (note per-directory `materialized:`
config), `profiles.yml`, `packages.yml`, `package-lock.yml`, existing `models/`
(note layout + naming convention), `macros/`, schema YAML, and `sources:`.
Identify: the result table(s) wanted, the convention-correct name for each, where
tables (not CTEs) get materialized, the existing models to build on, and the
fact/event vs dimension tables involved.

Run cheap baseline probes: `dbt deps` if packages are missing, then
`dbt compile --profiles-dir .`, targeted `dbt run`, targeted `dbt test`, or log
inspection. If a baseline probe fails because declared packages are missing, run
`dbt deps` before interpreting the project as broken. Sample the relevant
source/staging/fact tables: row counts, nulls, duplicates, key distributions,
representative rows, and which entities actually have activity.

## Stage: Implementation

Create the new model file(s) under `models/` with the convention-correct name,
materialized as a TABLE (override the dir default if needed). Compute the result
at the implied grain, driven FROM the fact and inner-joined to dimensions,
selecting the key plus every described column. Follow local naming,
materialization, `ref()`/`source()`, macro, and schema patterns. Wire inputs
through existing `ref()`s where possible.

The following gated rules each apply ONLY to their named task shape; when a task
does not match a rule's gate, ignore that rule entirely and treat the task by its
actual classification. Each rule is one principle, its gate, and a generic
BEFORE/AFTER skeleton. (These are dbt analytic-correctness patterns carried over
from ade-bench, a sibling dbt benchmark.)

PER-KEY METRIC AGGREGATE (gated). When a task asks to BUILD a per-key metric
aggregate (an NPS / review / rating / spend rollup keyed by
listing/customer/entity) and does NOT request completeness, scope the output to
keys that actually have fact rows: build FROM the fact and INNER JOIN the key's
metadata. Do NOT LEFT JOIN the full key dimension and emit zero-fact keys with
NULL/0 metrics.

BEFORE (keeps zero-fact keys as NULL/0-metric rows — AVOID when completeness not asked):
    select dim.key, agg.metric
    from {{ ref('key_dimension') }} dim
    left join fact_agg agg using (key)        -- emits phantom rows for zero-fact keys

AFTER (scope to keys present in the fact):
    select dim.key, agg.metric
    from fact_agg agg                          -- driven by the fact
    inner join {{ ref('key_dimension') }} dim using (key)   -- zero-fact keys excluded

EXCLUDE-A-CATEGORY AVERAGE (gated). When an average/aggregate must exclude a row
category (e.g. a lap-time average that must "account for" pit stops, a spend
metric that excludes returned items), filter that category out BEFORE the
aggregate; do NOT keep the rows and subtract their contribution.

BEFORE (keeps the excluded rows, subtracts — AVOID):
    select grp, avg(value - excluded_part) as avg_value
    from t group by grp

AFTER (drop the excluded category, then aggregate):
    select grp, avg(value) as avg_value
    from t
    where not is_excluded_category             -- excluded rows removed before the aggregate
    group by grp

CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN (gated). When computing
season/entity totals from a column that is a cumulative race-by-race / period-by-
period snapshot (e.g. `*_standings` points), treat it as cumulative: use
`max(points)` at the entity/season grain, NOT `sum(points)`. Do NOT switch to
latest-row, rank, row_number, QUALIFY, or order-by-final-period unless local
evidence proves `max()` wrong.

COVERAGE / COMPLETENESS (gated). When the instruction EXPLICITLY asks for row/date/
key COMPLETENESS ("a row for every day", "every <key> present", "include all
dates"), emit every key: keep the full spine/dimension and LEFT JOIN the fact
(the opposite of the per-key-aggregate rule). Confirm the dimension's keys are
all present in the output. If completeness is NOT asked, do not pad the grain.

TOP-N TIE-CROSSES-CUTOFF (gated). When a task asks which `order by <metric> desc
limit N` (no deterministic tiebreaker) results are "inconsistent given the current
data", a model is inconsistent ONLY when a tie CROSSES THE CUTOFF — the metric of
row N also occurs at row N+1. A tie entirely inside (or outside) the top N
reorders display only — do NOT count it. Locally computable: inconsistent iff
`count(rows with metric >= the N-th value) > N`.

BUILD / RENAME — PRESERVE THE COLUMN SET (gated). When a task asks to BUILD,
CREATE, or RENAME a model from a single upstream model and does NOT enumerate a
restricted set of columns to keep, PRESERVE every upstream column; apply only the
named renames/keys/casts and carry all others through unchanged. Do not prune to a
"relevant" subset (extra columns are harmless to grading; a dropped one is not).

TMP/INTERMEDIATE-TIER REMOVAL — BEHAVIOR-PRESERVING INLINE (gated). When a task
asks to remove a tmp/intermediate tier and point the consuming model at the
source, RECONCILE before==after: first build as-is and capture each affected
model's column set + row count, then copy the deleted model's SELECT verbatim
(exact columns, casts, aliases, WHERE) into the consumer, changing ONLY the
FROM/ref to the source; do NOT re-derive, drop, rename, or re-cast. A clean
`dbt run` is NOT sufficient proof — only the before==after reconciliation is.

FEATURE-BOUNDARY REMOVE / TOGGLE / DISABLE (gated). When a task asks to remove,
disable, or add a switch for a project-local feature, keep the edit at the feature
boundary: drop or guard the feature-ONLY derived columns, refs, CTEs, joins, and
outputs, but KEEP the shared base id / foreign-key column the rest of the project
uses. Do not unwrap conditional guards so the feature stays active, and do not
turn it into a broad domain rewrite.

PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX (gated). When a task says an installed dbt
package was updated, classify package vars and optional-resource behavior before
editing. If a downstream model unconditionally refs a package resource that an
existing package var can disable, prefer a package-migration compatibility
diagnostic (a small disabled-var compile matrix) over casts, raw seed edits, or
broad package copying.

Build as you go with the cheapest command that proves your model materializes:
`dbt run --select <your_model>+ --profiles-dir .` then `dbt build`. Fix
compile/build errors caused by your change before moving on.

## Stage: Validation (verify the CONTRACT, not just "it builds")

Open the built DuckDB and, for EVERY target table you were asked to produce
(check them all — not just the last one):
- Confirm the table EXISTS by its convention-correct name in the default schema
  (`select table_name from information_schema.tables`). A target that is missing
  (compiled ephemeral) or misnamed (`customer` vs `dim_customer`) scores zero.
- Confirm the grain (uniqueness on the key) and that the row count reflects only
  active entities, not the full padded dimension.
- Confirm the described columns are present and sensibly populated (no all-null
  metric columns, plausible values vs the source).
For repairs/refactors, also check row counts, schemas, and value-level behavior
for affected and downstream models. Re-check each target name against the
project's convention one more time. Run broader `dbt build`/`dbt test` when
practical.

## Stage: Finalization

Leave only the intended new/changed models and supporting edits. Remove `target/`
and `logs/` scratch unless the project requires them; do not remove
`dbt_packages/` when it existed at task start. Finish with the changed files and
concise validation evidence: each built target table name, its grain, row count,
and a representative row.
