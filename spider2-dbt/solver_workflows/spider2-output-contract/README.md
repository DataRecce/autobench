# Codex Spider2-DBT Solver Workflow

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
their exact columns are NOT given to you — you must produce them from the
instruction plus the project's own conventions. Getting the table name, the
grain, or the column set wrong scores zero even if the logic is sound.

1. DELIVERABLE = NEW MATERIALIZED MODEL(S). The result the instruction asks for
   is almost never already built. Create a new model (a `.sql` under `models/`)
   for each result table the instruction describes — there may be more than one
   (e.g. a dimension + a fact + a one-big-table). Materialize each as a `table`
   or `view` (NOT `ephemeral`) so it lands in the output DuckDB. Do not just edit
   an unrelated existing model and stop.

2. NAME EACH MODEL BY THE PROJECT'S EXISTING CONVENTION. Before writing SQL, list
   the existing model filenames and read their prefixes — they ARE the naming
   contract. Match it exactly for the new entity named in the instruction:
   - dimensional projects use `stg_*` → `int_*`/`dim_*`/`fct_*` → `obt_*` (one
     big table). "A comprehensive <X> table combining …" with `dim_`/`fct_`
     siblings present → build `dim_<entity>`, `fct_<entity>`, and `obt_<entity>`
     as the conventions imply.
   - package-style projects use `<pkg>__<entity>_<suffix>` (e.g.
     `jira__issue_enhanced`, `jira__user_enhanced`); a request about a new entity
     → `<pkg>__<that_entity>_<same_suffix>` (e.g. `jira__project_enhanced`).
   - method/variant projects use `<dataset>__<method>_<n>`; the instruction names
     the methods (e.g. "aggregate after", "aggregate all ever") → build
     `<dataset>__aggregate_after_<n>`, `<dataset>__aggregate_all_ever_<n>`,
     numbering to match the existing siblings.
   A dbt model's materialized table name is its filename stem unless `alias` is
   set — name the FILE as the target table; do not add an alias that changes it.

3. SCHEMA / LOCATION. Build into the project's default schema (the active
   `profiles.yml` output, normally `main` in the project DuckDB) so the table is
   visible at the top level of the output DuckDB. Do not route the result to a
   custom schema that would qualify the table name away from gold.

4. COLUMNS + GRAIN. Emit exactly the columns the instruction describes: the
   natural/business key(s) first, then every described attribute and metric, at
   the grain the instruction implies (one row per <entity>). Don't add stray
   helper columns to the final model, and don't drop a described one. Reuse the
   project's existing `stg_*`/`int_*` models and declared `source()`s as inputs
   rather than re-reading raw tables ad hoc.

## Stage: Exploration

Inspect the instruction, `dbt_project.yml`, `profiles.yml`, `packages.yml`,
existing `models/` (note the directory layout and the naming convention),
`macros/`, schema YAML, and `sources:` declarations. Identify: the result
table(s) the instruction wants, the convention-correct name for each, the
existing models you can build on, and the source/staging tables involved.

Run cheap baseline probes: `dbt deps` if packages are missing, then
`dbt compile --profiles-dir .` and targeted `dbt run`/`dbt build`. For
correctness, sample the relevant source and staging tables: row counts, keys,
null behavior, representative rows.

## Stage: Implementation

Create the new model file(s) under `models/` with the convention-correct name,
following local materialization, `ref()`/`source()`, and macro patterns. Compute
the result the instruction describes at the implied grain, selecting the key plus
every described attribute. Wire inputs through existing `ref()`s where possible.

Build as you go with the cheapest command that proves your model materializes:
`dbt run --select <your_model>+ --profiles-dir .` then `dbt build`. Fix
compile/build errors caused by your change. Confirm each new model actually
appears as a table in the output DuckDB before moving on.

## Stage: Validation

Beyond "it builds": open the built DuckDB and verify each target table EXISTS by
its convention-correct name, at the expected grain (uniqueness on the key), with
the described columns present and sensibly populated (no all-null metric columns,
plausible row counts vs the source). Re-check the table name against the
project's convention one more time — a near-miss name (`customer` vs
`dim_customer`) scores zero. Run broader `dbt build`/`dbt test` when practical.

## Stage: Finalization

Leave only the intended new/changed models and their supporting edits. Remove
`target/` and `logs/` scratch unless the project requires them; do not remove
`dbt_packages/` when it existed at task start. Finish with the changed files and
concise validation evidence (the built table names, grain, and a representative
row).
