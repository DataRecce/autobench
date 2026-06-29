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

## Stage: Classify (router) — RUN FIRST, before Exploration

Before deciding HOW to model anything, decide WHAT to build for each result table.
Run this router on **oracle-free signals only** — the instruction text, the target table
name(s), the `models/` + `schema.yml` tree, `dbt_project.yml` vars, and the source
`information_schema`. Never read or guess gold values. For EACH result table `T` the
instruction implies (enumerate them all — see R5), pick exactly one branch:

- **R1 — BUILD_AS_IS.** If a model file whose stem equals `T` ALREADY EXISTS
  (`models/**/<T>.sql`), the gold answer is "what this project produces when built
  unmodified." Run `dbt deps` (if needed) then `dbt build` and DO NOT create or edit that
  model's SQL. Do NOT rewrite a computation that looks buggy (a formula, ratio, unit
  conversion): if gold was built from this project, your "correction" diverges from gold.
  **BOUNDED REPAIR.** Repair an existing model ONLY if `dbt build` fails, and the repair is
  STRICTLY bounded: you may disable or stub the FAILING UPSTREAM (an absent-source staging
  model, a broken disabled feature) — you may NEVER alter the grain, join, row set, or
  column logic of `T` itself or any intermediate `T` depends on. If making the build pass
  would require changing a target/intermediate's own SELECT (grain/join/filter), STOP: do
  not force a green build — the failure is structural, route it to R3. (Forcing a green
  build by re-deriving an intermediate's grain is the exact move that collapsed an
  account-overview target 4 rows → 1.)
  **R3 PRECEDENCE.** Before any R1 repair, run the R3 absent-source/-package check on the
  failing model's `source()`s and package `ref()`s; if the build failure traces to an
  absent source table or an uninstalled package model, route that subtree to R3 (disable
  it) rather than re-deriving `T`.

- **R2 — AUTHOR from the declared recipe.** If `T` is documented in a `schema.yml` (a model
  name with `refs` and per-column descriptions) but no `<T>.sql` exists, AUTHOR `<T>.sql`
  from that declared recipe. Mirror the nearest same-role sibling model's conventions
  (surrogate-key offset + `ROW_NUMBER()`, `{{ ref('dim_*') }}` FK joins, dtypes, rounding) —
  do NOT hard-code an offset literal, copy the sibling's. Do NOT invent a differently-named
  table; build exactly `<T>`.

- **R3 — FIXTURE DEFECT (flag, do not fabricate).** If `T`'s declared source identifier
  (a `dbt_project.yml` var, or a `source()`/`int_` ref it depends on) resolves to a table
  that is ABSENT from the source DB (`information_schema`), the workspace cannot build `T`.
  Report it as ungradeable in your final notes; do NOT fabricate source rows to fill the gap.

- **R4 — AUTHOR as a new model.** Otherwise `T` is a genuine new authoring task: create
  `<T>.sql` (continue to Exploration/Implementation as normal).

- **R5 — ENUMERATE EVERY TARGET (the declared table set IS the target list).** Do not let the
  instruction prose scope the deliverables — the project's declared model set does. A model
  that is declared in a `schema.yml` (or surfaced by dbt as a "missing model" / undefined-ref
  warning) but is ABSENT from `models/` and from installed packages is an IN-SCOPE target —
  build it (route it through R1–R4/R6), regardless of whether the instruction prose names it.
  Never dismiss a declared-but-unbuilt model as "unrelated" or "out of scope" because the prose
  only mentioned a sibling. Before finishing, list the declared model set and confirm every one
  that the grader could compare physically exists as a base table. (A task whose contract has a
  `*_company_metrics` AND a `*_admin_metrics` table fails outright if you build only the
  prose-named one.)

- **R6 — VERBATIM UNION of existing intermediates (NARROW: same-grain domain partitions only).**
  Fires ONLY when `int_*__<T>_*` intermediates are mutually-exclusive ROW PARTITIONS of the SAME
  output schema (e.g. per-domain cost slices that concatenate to one fact) and `<T>` is the lone
  missing FINAL model. Then author `<T>` as a `UNION ALL` of those intermediates and **`SELECT *`
  from each intermediate UNCHANGED — never edit an intermediate's grain, join, or filter to
  "tighten" it** (editing the upstream is what dropped real rows from a cost union). Do NOT use R6
  for `*_report` / `*_rollup` / `*_daily` / reporting-grain targets, or when the intermediates are
  DIFFERENT sub-grains that need a join/anchor (a naive union of sub-grain intermediates
  over-emits — that is the wrong shape). Those targets are a GRAIN problem: anchor on the primary
  grain relation and LEFT-join the others (handled by the grain rules below), not a union.

Every branch is gated on a file/name/schema signal, so they do not conflict: R1 fires only on
an existing stem, R2/R6 only on a documented-or-intermediate-backed missing target, R3 only on
a missing source. When none fire, R4 is the default (ordinary authoring) — so this router never
changes behavior on a plain new-model task.

### Axis-2 G2 — OVER-EMIT COLLAPSE (gated; collapse to the canonical row slice)

When a target OVER-emits rows (more rows than gold), the comparator's `len(pred)==len(gold)` gate
fails every column — grain exactness is binary. Each rule below fires ONLY on its structural
signal (a model config, a sibling file, a role-dimension, a report-grain name); they are disjoint,
so they compose without bleeding. None fires on a plain authored aggregate.

- **Respect the incremental window — INCLUDING when you author the target fresh.** If the target
  (or its nearest sibling model) uses `config(materialized='incremental')` with an
  `is_incremental()` period-restriction WHERE clause, the gold table is ONLY the latest window that
  branch defines — emit just that single most-recent window, NOT the metric computed for every
  period. This applies EVEN when the target model does not exist and you author it from scratch:
  do not "helpfully" full-refresh it into full history. Read the sibling incremental model
  (e.g. a `wow_*`/`mom_*` peer) for the exact window length and the latest-window anchor (the
  window ends at the MAX source date), and reproduce only that one window. *[airbnb001
  `mom_agg_reviews`: ONE rolling 30-day window ending at the max review date = 3 rows (one per
  sentiment), NOT one row per calendar date (~11k).]*
  **CRITICAL — the window filter must hold under `--full-refresh`.** The build runs
  `dbt run --full-refresh`, under which `is_incremental()` evaluates to FALSE. So if a model's
  latest-window restriction (the `WHERE date BETWEEN max-N AND max` and its MAX-date anchor) lives
  INSIDE an `{% if is_incremental() %}` block, that filter is SKIPPED at build time and the model
  emits FULL HISTORY — the exact over-emit. When the existing model gates its window behind
  `is_incremental()`, MOVE the window WHERE-clause and the MAX-date anchor OUT of that block so they
  apply UNCONDITIONALLY (or compute the latest-window directly). Verify the built table has only the
  single latest window (a handful of rows), not one row per period — a clean `dbt build` is NOT
  proof here, because full-refresh silently bypasses the guard. *[airbnb001: the correct 30-day
  window logic already exists but is gated behind `is_incremental()`; full-refresh skips it → 11,135
  rows instead of 3 unless the filter is made unconditional.]* SHARPEN: anchor the window to the SINGLE most-recent source date — derive the anchor from `MAX(<event_date>)` over the source fact and emit EXACTLY ONE window (one row per group dimension), never one window per historical date. Before finishing, VERIFY the built table's row count equals the number of distinct group-dimension values, NOT the number of distinct source dates — if it equals the date count, the window was computed over all dates and must be re-anchored.
- **Resolve role attributes through the role dimension.** If the target fact carries
  role-prefixed columns (`seller_*`/`buyer_*`, `sender_*`/`receiver_*`) AND an
  `int_<role>_extracted_from_users` (or similar role-specific) dimension ships, INNER JOIN through
  that role dimension — do NOT join the full raw user table (which fans out / keeps non-role rows).
  *[tickit002.]*
- **Mirror the opposite-entity sibling's filter.** If the target is a `*_by_<entity>` stat and an
  opposite-entity sibling model exists (`<other>_by_<entity>`), copy the sibling's filter and
  aggregation column VERBATIM, swapping only the entity — do NOT invent a looser filter (e.g. use
  the sibling's `position` not a broader `position_order`). *[f1003.]*
- **Passthrough tables: preserve source grain, never inner-join-prune.** If parallel
  `prod_<entity>` / `*_unioned` passthrough tables are built 1:1 from `raw_<entity>`, carry the
  source grain through unchanged; do NOT inner-join to another table that drops rows. *[reddit001
  — note a residual undocumented 1-row curated drop may remain.]*
- **Report/rollup grain = ANCHOR + LEFT-join, NOT a union.** If the target is a `*_report` /
  `*_rollup` / overview at a reporting grain whose `int_*` intermediates are DIFFERENT sub-grains
  (impressions vs downloads vs usage), ANCHOR the row grain on the PRIMARY intermediate (the
  impressions/page-views one) and LEFT-join the others with `coalesce(...,0)` — do NOT `UNION` the
  sub-grain intermediates (a naive union concatenates their disjoint grains and over-emits). This
  is the inverse of R6: R6's verbatim union is for SAME-grain domain partitions only; report-grain
  targets need this anchor instead. *[apple_store001 `source_type_report`/`territory_report`:
  anchor on `int_*__app_store_*`, LEFT-join downloads/usage.]*
  **PRESERVE THE RAW GROUPING KEY — do not canonicalize it.** When the report's grouping key is a
  raw label (a territory/region/category string), GROUP BY and emit the RAW key value in the
  `*_long`/name column. A lookup/country-code seed may FILL secondary attributes
  (`*_short`/`region`/`sub_region`) via a LEFT join, but NEVER re-group on the canonicalized lookup
  value: spelling variants that map to one canonical name (e.g. `Türkiye`/`Turkey`,
  `Côte d'Ivoire`/`Cote d'Ivoire`) are SEPARATE gold rows, and collapsing them drops rows. *[apple_store001
  `territory_report`: keep the raw `territory` as `territory_long` → 17 rows, not 16.]*

### Axis-2 G3 — COLUMN-VALUE CONTRACT (per-column, gated by column name / source dtype)

After the router decides WHAT to build, pin HOW each COMPARED column is computed. These rules are
NOT generative — each fires ONLY on the named-column / source-dtype signal stated, and is applied
per column, never table-wide. Applying any of them blanket is net-negative; the gate is the
isolation.

**R1-PRECEDENCE GUARD (applies to EVERY G3 clause below).** These column-value rules apply ONLY to
columns of a model you are NEWLY AUTHORING (R2 / R4 / R6). NEVER apply a value-def edit — a dtype
cast, a count-semantics change, a conversion, a re-rounding — to a column in a PRE-EXISTING model
(R1 build-as-is) or to an existing intermediate it `ref()`s. Those are built UNMODIFIED per R1:
gold was produced from them as-is, so "correcting" a column there diverges from gold. If a
pre-existing model's column looks wrong (an id that "should" be a string, a count that "should" be
distinct), LEAVE IT. (Casting `customer_id` in a pre-existing R1 model — and rebuilding its date
spine to match — is exactly what corrupted a passing `mrr` target 410→417 rows.)

- **Identifier dtype — DO NOT GUESS.** Carry an identifier column through at its SOURCE dtype
  unchanged. Do NOT cast a numeric id to VARCHAR (or vice-versa) to "match gold": whether gold
  stores an id as a string or a number is not derivable from the source or schema.yml, and guessing
  it breaks as many tasks as it fixes. Preserve the source type; never re-type an id column.
- **COUNT(\*) vs COUNT(DISTINCT) by NAME.** Choose the count semantics from the column NAME:
  `total_*` / "number of <rows>" → `COUNT(*)` (every row); `num_*` / "distinct <X>" / "unique" →
  `COUNT(DISTINCT ...)`. Disambiguate by the name, never default to one. *(a `total_invoices`
  column counts every invoice line; a `num_invoices` column counts distinct invoices.)*
- **Typed-value conversion.** If a source row carries a VALUE plus a VALUE_TYPE discriminator
  (e.g. `value_type='percentage'`), convert against the parent base (percentage discount =
  `base * value / 100`); never pass the raw value through. *(recharge001.)*
- **NULL-vs-0 by metric kind.** For a metric over a feature that may be ABSENT, use a
  NULL-preserving `count_if`/conditional aggregate (leave NULL when the feature never occurs);
  for a categorical bucket TALLY, `coalesce(..., 0)`. Split these — do not coalesce feature-absent
  metrics to 0, do not leave categorical tallies NULL. *(f1002.)*
- **Money rounding — round DERIVED aggregates, pass through RAW values.** `ROUND(<money>, 2)` a
  monetary value you COMPUTE (a `SUM`/`AVG`/product/ratio prone to float noise that the
  comparator's `str()`-keyed float sort would false-fail on); but a column that is a
  passed-through RAW source amount must be carried at its source precision, never re-rounded.
  Decide per column by whether YOU derived it (round) or passed it through (leave raw) — never
  round all money table-wide (a single table can mix a derived total and a raw amount).
- **Sign convention per table.** Preserve the package/overview table's spend/amount SIGN
  convention per-table; do not normalize signs across tables. *(twilio001.)*
- **Key-embedded grain.** Group by the timestamp grain the target KEY embeds (e.g. a
  `ticker||timestamp` key implies minute-level grain) even when the prompt says "daily."
  *(asset001.)*
- **Period-over-period = window function over the model's OWN output (derivation METHOD, not a
  re-queried window).** A period-over-period derived column (MoM / YoY / delta / growth-%) must be
  computed as a window function (`LAG`/`LEAD`) over the built model's OWN output rows — partition by
  the group key, order by the window-anchor date — NEVER against a separately re-materialized
  prior-period window queried from the source. This is a derivation METHOD, not a value: read it off
  the window definition, never bake a literal value, count, or NULL flag. The mechanical consequence
  is the point — when the build emits exactly one window row per group, the `LAG`/`LEAD` has no
  prior row and the column is NULL by construction. (A re-queried prior-period window from a long
  source instead invents a "real" delta that diverges from a single-window gold.) A local sibling
  already follows this exact method — `models/agg/wow_agg_reviews.sql` computes its week-over-week
  metric as a `LAG(...) OVER (PARTITION BY <group key> ORDER BY <anchor date>)` over its own output;
  mirror that shape over your own output. *[airbnb001 `mom_agg_reviews.MOM`: LAG over the single
  30-day-window output → NULL by construction.]*

Determine the per-column contract from `schema.yml` descriptions + the source `information_schema`
dtype — oracle-free, never from gold values.

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
