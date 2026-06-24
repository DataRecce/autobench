# Codex Spider2-DBT Solver Workflow (v2)

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
and `dbt_packages/` is absent; preserve any `dbt_packages/` already present.
Treat `target/` and `logs/` as generated scratch state.

## THE OUTPUT CONTRACT (load-bearing — this is how the task is graded)

The verifier compares the **tables that exist in the built DuckDB by name**
against gold, column-by-column (row order is ignored). Gold table names and
their exact columns are NOT given to you — produce them from the instruction
plus the project's own conventions. Getting the table name, the grain, the row
set, or the column set wrong scores zero even if the logic is sound.

1. DELIVERABLE = NEW MATERIALIZED MODEL(S). The result is almost never already
   built. Create a new model (`.sql` under `models/`) for EACH result table the
   instruction describes — there may be several (e.g. a dimension + a fact + a
   one-big-table).

2. EVERY TARGET MUST LAND AS A BASE TABLE — NOT EPHEMERAL. The verifier can only
   compare a table that physically exists in the output DuckDB. A model
   materialized `ephemeral` compiles into a CTE and creates NO table → an
   automatic zero for that target, even if its SQL is perfect. Before finishing:
   - Check the directory config in `dbt_project.yml` for where you put each
     target. If that path defaults to `materialized: ephemeral` (or `view` when
     gold expects a table), OVERRIDE it in the model itself:
     `{{ config(materialized='table') }}`.
   - Do NOT bury a target model under an intermediate/ephemeral folder and
     assume it will appear — put targets where the project materializes tables,
     or force `materialized='table'`.

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
   dimension and emit zero-activity rows padded with 0/NULL metrics — those phantom
   rows change the row count and fail the comparison. (Only emit every dimension
   key when the instruction explicitly asks for completeness — "a row for every
   <key>", "include all …".) One row per <entity> at the implied grain.

5. SCHEMA / LOCATION. Build into the project's default schema (the active
   `profiles.yml` output, normally `main`) so the table is visible at the top
   level of the output DuckDB. Do not route a result to a custom schema that
   qualifies the table name away from gold.

6. COLUMNS. Emit exactly the columns the instruction describes: the
   natural/business key(s) first, then every described attribute and metric.
   Don't add stray helper columns to the FINAL model, and don't drop a described
   one. Reuse the project's existing `stg_*`/`int_*` models and declared
   `source()`s as inputs rather than re-reading raw tables ad hoc.

## Stage: Exploration

Inspect the instruction, `dbt_project.yml` (note per-directory `materialized:`
config), `profiles.yml`, `packages.yml`, existing `models/` (note layout +
naming convention), `macros/`, schema YAML, and `sources:`. Identify: the result
table(s) wanted, the convention-correct name for each, where tables (not CTEs)
get materialized, the existing models to build on, and the fact/event vs
dimension tables involved.

Run cheap probes: `dbt deps` if packages are missing, then
`dbt compile --profiles-dir .` and targeted `dbt run`/`dbt build`. Sample the
relevant source/staging/fact tables: row counts, keys, null behavior,
representative rows, and which entities actually have activity.

## Stage: Implementation

Create the new model file(s) under `models/` with the convention-correct name,
materialized as a TABLE (override the dir default if needed). Compute the result
at the implied grain, driven FROM the fact and inner-joined to dimensions, with
the key plus every described column. Wire inputs through existing `ref()`s.

Build as you go: `dbt run --select <your_model>+ --profiles-dir .` then
`dbt build`. Fix compile/build errors caused by your change.

## Stage: Validation (verify the CONTRACT, not just "it builds")

Open the built DuckDB and, for EVERY target table you were asked to produce
(check them all — not just the last one):
- Confirm the table EXISTS by its convention-correct name in the default schema
  (`select table_name from information_schema.tables`). A target that is missing
  (compiled ephemeral) or misnamed (`customer` vs `dim_customer`) scores zero.
- Confirm the grain (uniqueness on the key) and that the row count reflects only
  active entities, not the full padded dimension.
- Confirm the described columns are present and sensibly populated (no all-null
  metric columns, plausible values).
Re-check each target name against the project's convention one more time. Run
broader `dbt build`/`dbt test` when practical.

## Stage: Finalization

Leave only the intended new/changed models and supporting edits. Remove
`target/` and `logs/` scratch unless the project requires them; do not remove
`dbt_packages/` when it existed at task start. Finish with the changed files and
concise validation evidence: each built target table name, its grain, row count,
and a representative row.
