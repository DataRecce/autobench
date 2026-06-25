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

4. GRAIN + ROW SET — CLASSIFY FIRST, THEN CHOOSE THE JOIN. Decide the intended row
   set BEFORE writing the model, from the instruction wording and the target's name.
   There are two regimes; picking the wrong one is the single most common miss.

   PRESERVE-COVERAGE (the DEFAULT for reporting / dimension / daily targets — LEFT
   join, keep every entity/period):
   - the target is a dimension, a `*_report`/`*_metrics`/`*_overview`/`*_enhanced`
     rollup, or names "daily/monthly/over-time"; or the instruction says "every
     <X>", "all <X>", "for each <X>", "include …", "complete".
   - Build FROM the full entity dimension / a continuous DATE SPINE (first→last
     period, EVERY period present) and LEFT JOIN the facts. KEEP zero-activity
     entities and no-activity days with 0/NULL metrics. Carry balances FORWARD into
     no-activity periods (point-in-time snapshots like balance sheets). A
     `*_unioned`/`*_union` staging model is a pass-through `UNION ALL` at SOURCE-ROW
     grain — never dedup, GROUP BY, or collapse it to a business key.

   SCOPE-TO-ACTIVE (only when EXPLICITLY signalled — INNER join / filter):
   - the instruction says "only <X> that have …", "with at least one …", "exclude
     <X> without …", or it is a per-entity lifetime/value rollup keyed to entities
     that actually transacted.
   - Build FROM the fact and INNER JOIN the dimension; do not emit zero-activity rows.

   NEITHER regime — PLAIN AGGREGATE / RANKING / SUPERLATIVE (do NOT pad, do NOT
   spine, do NOT LEFT-join phantom rows). When the target is an aggregate, ranking,
   leaderboard, superlative, or total — its name reads `most_*`/`top_*`/`*_ranking`/
   `*_summary` or "most / top / fewest / best / fastest / total / career / season"
   — it is NOT a coverage table. Compute it as the ordinary GROUP BY / window
   aggregate at its own natural grain over the existing models, exactly as the
   project already builds its sibling aggregates. PRESERVE-COVERAGE does NOT apply:
   adding a date spine, a full-dimension LEFT join, or zero/NULL padding rows here
   CORRUPTS the aggregate and regresses it. This exclusion OVERRIDES the
   PRESERVE-COVERAGE default below.

   When unsure BETWEEN coverage and active-scope FOR A PER-ENTITY OR DATED TARGET
   (a dimension, a `*_report`/`*_metrics`/`*_enhanced` rollup, a daily series),
   PREFER PRESERVE-COVERAGE — under-emitting by inner-joining away entities/periods
   is the more common miss. But do NOT reach for coverage on a plain aggregate /
   ranking / superlative (above) — those get the ordinary aggregate, never a spine.
   Do not collapse a per-row/per-timestamp source to a coarser period unless the
   target name IS the aggregate. Sanity-check the row count against the driving
   source's distinct-key (or spine-period) count — far SMALLER than its source
   dimension is an over-restrictive-join smell; far LARGER is an un-collapsed
   fan-out (or wrong padding on an aggregate).

5. SCHEMA / LOCATION. Build into the project's default schema (the active
   `profiles.yml` output, normally `main`) so the table is visible at the top
   level of the output DuckDB.

6. COLUMNS. Emit the natural/business key(s) first, then every described
   attribute and metric, at the implied grain. Because grading is containment,
   extra columns are harmless — so when unsure whether a column belongs, KEEP it
   rather than prune; only never DROP a described column. Reuse the project's
   existing `stg_*`/`int_*` models and declared `source()`s as inputs rather than
   re-reading raw tables ad hoc.

7. VALUE-LEVEL DISCIPLINE (once the grain/row-set is right per §4, the residual
   misses are wrong column VALUES — address them here). APPLY MINIMALLY: this
   discipline is for getting a WRONG or incomplete value right, NOT for re-litigating
   a model that already builds clean. If a target already builds and its columns
   already match the instruction's described semantics on inspection, LEAVE IT —
   re-engineering a correct model (extra re-derivations, refactors, "tidying") is a
   net regression risk, not an improvement. Touch only what is demonstrably wrong.
   - COLUMN COMPLETENESS + TYPE. Enumerate every column the instruction names or
     implies; ensure each target column is present AND of the right kind. In a mart,
     a FACT carries dimension surrogate-key FK columns (`dim_*_id`), NOT the
     denormalized descriptive attribute; preserve the project's surrogate-key
     offsets (do not renumber a dimension's ids).
   - COUNT / METRIC GRAIN. For a "count" or "number of <X>" metric, confirm against
     the source whether it counts ROWS/LINES or `COUNT(DISTINCT key)` — do not
     default to distinct; an invoice "count" is often the line count.
   - DEFINITION FROM THE PROJECT, NOT THE PROSE. When a vendored package or an
     existing `int_*`/`stg_*` model already computes a measure, `ref()` it and carry
     its definition and columns VERBATIM (including columns that resolve to NULL and
     the package's own join scope); do not re-derive the measure from the
     instruction's narrative wording, and do not invent a column the prose names but
     the package omits.
   - INDEPENDENT RE-DERIVATION (the only oracle-free guard against false-green),
     applied to the PRIMARY target metric ONLY. The gold is not visible, so "it
     builds / 0 dup keys" proves nothing about values. For the single most important
     output metric, compute it a SECOND independent way (a different join path or
     aggregation order) and reconcile the two numbers. If they AGREE, you are done —
     stop, do not keep changing the model. If they disagree, your interpretation is
     wrong — fix it. This is a one-shot check on the primary metric, not a license to
     refactor every column; validate against the instruction's described semantics,
     never against your own build.

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

PER-KEY METRIC AGGREGATE (gated — this is the SCOPE-TO-ACTIVE case of §4, apply
ONLY when §4 classified the target as SCOPE-TO-ACTIVE). When a per-key metric
aggregate (an NPS / review / rating / spend rollup) is explicitly scoped to keys
that transacted, build FROM the fact and INNER JOIN the key's metadata; do NOT
emit zero-fact keys. If §4 classified the target as PRESERVE-COVERAGE instead
(a dimension/report/daily rollup, or "every <key>"), do the opposite — LEFT JOIN
the full dimension and keep zero-fact keys with 0/NULL metrics. The default is
PRESERVE-COVERAGE; only this rule's INNER-join form when SCOPE-TO-ACTIVE is signalled.

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
