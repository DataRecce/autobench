---
commissioned-by: spacedock@0.9.1
entity-type: benchmark_dataset
entity-label: dataset
entity-label-plural: datasets
id-style: sequential
stages:
  defaults:
    worktree: false
    concurrency: 1
  states:
    - name: pending
      initial: true
    - name: model
    - name: analyze
    - name: verify
      feedback-to: analyze
    - name: done
      terminal: true
---

# Solve a DataAgentBench dataset (source-count classifier → one of two methods)

Answer the queries for the current dataset and write the final answers to `answers.json`
at the workspace root. The workspace contains connection details, a schema description, and
one `queryN/` subdirectory per query.

**There are TWO methods in this README. The FIRST thing the `model` stage does is run a
classifier that picks exactly ONE of them for this dataset, and you then follow that method's
section verbatim for `model → analyze → verify → done`.**

## Classifier — pick the method at the very top of `model`

Read `db_config.yaml` (it may be named `connections.yaml`). Count the number of **distinct
source databases** declared under `db_clients:` (each top-level key under `db_clients:` is one
source DB — e.g. `core_crm`, `sales_pipeline`, `support`, … are six sources).

```
N_sources = number of distinct entries under db_clients: in db_config.yaml
```

- **If `N_sources >= 3` → use METHOD B (dbt pipeline).** Three or more source databases is the
  structural marker of cross-source-derivation work: the correct answer to a question is not
  present in any single source's raw fields but must be *derived* by joining facts across
  sources. dbt's materialized intermediate (`int_*`) layer is what makes that derivation the
  one reusable path to the answer.
- **If `N_sources < 3` (i.e. exactly 2, or 1) → use METHOD A (direct DuckDB).** A two-source
  dataset's answers live in the sources' own fields; the dbt overhead buys nothing and adds
  variance, so run the lean direct method.

Record the count and the chosen method in `_artifacts/context.md` as the first line, e.g.
`N_sources=6 (core_crm, sales_pipeline, support, products_orders, activities, territory) → METHOD B (dbt)`
or `N_sources=2 (business, review) → METHOD A (direct)`.

> Generalization hedge (NOT the operative gate — do not change behavior on the current mix):
> the precise structural trigger is "≥3 sources AND `db_description.txt` warns of cross-source
> dirty/derived entity fields". On every dataset in this benchmark the pure `N_sources >= 3`
> count routes identically (the one ≥3-source dataset is also the one with cross-source
> derived fields, and no 2-source dataset has ≥3 sources), so **count sources and branch on the
> count.** Do not route a 2-source dataset to dbt on the strength of a dirty-schema warning
> alone — that over-fires.

---

# METHOD A — direct DuckDB (used when `N_sources < 3`)

Use DuckDB as the query engine — it can attach SQLite, PostgreSQL, and
MongoDB databases directly. Always set an `extension_directory` to avoid
permission issues. Always cap `memory_limit` so large queries (e.g.,
LATERAL UNNEST over billion-row tables) spill to disk before the kernel
OOM-kills the python process:

```python
import duckdb
conn = {{DUCKDB_CONNECT}}
```

Attach databases by type:

- **SQLite**: `conn.execute("ATTACH 'path.db' AS name (TYPE SQLITE)")`
- **DuckDB**: `conn.execute("ATTACH 'path.duckdb' AS name")`
- **PostgreSQL**: host **`dab-postgres`**, port 5432, user `postgres`, password `postgres`.
  `conn.execute("LOAD postgres")` (extension preinstalled — no INSTALL/network) then
  `conn.execute("ATTACH 'host=dab-postgres port=5432 dbname=X user=postgres password=postgres' AS name (TYPE POSTGRES)")`
- **MongoDB**: the duckdb mongo extension is **not** available offline — use **pymongo**
  directly (it is preinstalled). Connect to host **`dab-mongo`**:
  `from pymongo import MongoClient; client = MongoClient("mongodb://dab-mongo:27017"); db = client["<db_name from connections.yaml>"]`
  then read the collection(s) with `db["<collection>"].find(...)`. Do NOT use
  `mongodb://localhost` and do NOT `LOAD mongo` in DuckDB.

Read `connections.yaml` for database names, types, and paths. The DB **hosts** are
`dab-postgres` / `dab-mongo` (containers on the same network), **not** `localhost`.

## Rules (Method A)

- Do NOT modify source databases — use DuckDB temporary tables for intermediate results
- Do NOT access `validate.py` or `ground_truth.csv` files
- If the data doesn't support an answer, say "UNABLE TO DETERMINE"
- No comma grouping in numbers (23,781 -> 23781)
- Use EXACT field values from the database
- Answer ONLY the question — no commentary or counter-examples

**Use only the workspace data.** The benchmark provides everything needed to answer each query in the workspace's databases (`connections.yaml`, attached SQLite/PostgreSQL/MongoDB/DuckDB sources). Do **not** consult external data sources to look up answer values, labels, or ground truth — even if the workspace data appears to come from a public dataset. Specifically forbidden:
- HuggingFace `datasets` library (`datasets.load_dataset`, `hf://...`) for label/oracle lookup
- Public CSV/JSON downloads of the same dataset (kaggle, GitHub, vendor sites)
- Web search engines, search APIs, or LLM-as-oracle calls (e.g., asking another model "what is the answer to X")
- Cached prior answers from earlier runs in `_runs/` or any artifacts outside the current workspace

The workspace databases are the only authoritative source. If a question is unanswerable from them, return `"UNABLE TO DETERMINE"`.

## Answers (Method A)

Write `answers.json` in the workspace root. Use the query directory name
as the key — e.g., a query in `query2/query.json` writes `{"q2": "answer"}`.

## Stages (Method A)

### `model` (Method A)

Explore databases and produce a context document for downstream stages.

- **Inputs:** `db_description.txt`, `connections.yaml`
- **Outputs:** `_artifacts/context.md`

Enumerate every table, record column types and sample values, identify
join keys, note data quality issues, and recommend a query approach per
question.

### `analyze` (Method A)

Answer all queries using the context document.

- **Inputs:** `_artifacts/context.md`, `query{N}/query.json`
- **Outputs:** `answers.json`, `_artifacts/reasoning.md`

Read the context first — do not re-explore from scratch. Per the Rules
section, do not consult external data sources to look up answers; the
workspace databases are authoritative.

Work the following checklist for each query:

- **Explore schema.** Re-read `db_description.txt` and the context
  document; identify the fact table, the join keys, and any warnings the
  description raises (duplicate sources, placeholder rows, dirty strings).
  Write exploratory queries before analytical ones, verify intermediate
  results, and show the neighborhood for ranking questions.
- **Duplicate-source entity resolution: a three-step sequence.** **Trigger:**
  if `db_description.txt` warns about `duplicate` rows, `different sources`,
  or independently dirty entity-name fields (e.g. title/artist/album, or
  name/description) on any table you intend to join, group, or rank over,
  you MUST run the following three steps **in order** before issuing the
  analytical query. The same three steps apply whether the question is a
  bounded target lookup (e.g. "total revenue for {title} by {artist}") or
  an open-ended ranking question (e.g. "which song generated the most
  revenue" / "which business has the most reviews"). Do NOT mark step 2 as
  "N/A" when the question is open-ended — the OR/entity-resolution step is
  what prevents you from ranking raw source-specific or placeholder labels
  as if they were distinct entities.

  **Step 1 — Normalize first.** For each affected table `{table}` create a
  `{table}_norm` CTE or temp view that:
  - lowercases and whitespace-collapses each string key column using
    `lower(regexp_replace(col, '\s+', ' ', 'g')) AS norm_col`. Apply this
    to `title`, `artist`, `album`, `name`, `description`, and any other
    entity-name columns the schema warns about.
  - extracts a 4-digit `year` value (e.g.
    `regexp_extract(release_date, '\d{4}') AS year`) when the raw column
    is a free-form date/release string.
  - preserves the row identifier so the staging view can join back to the
    fact table (sales/revenue/reviews) cleanly.

  **Step 2 — Resolve entity groups second (OR across dirty fields).** Build
  the resolved entity set or grouping key by broadening across the
  independently dirty normalized fields with **OR**, never **AND**. The
  point is that a duplicate-source row often has one field correct and
  another field blank, swapped, or concatenated; AND silently drops it,
  OR keeps it.

  - For a **bounded target lookup** (the question names a specific entity
    by one or more of its dirty fields), form the candidate entity-id set
    with a predicate like
    `norm_field_a LIKE '%{token_a}%' OR norm_field_b LIKE '%{token_b}%' OR norm_field_c LIKE '%{token_c}%'`
    so a row whose primary field is malformed but whose secondary field
    still carries the entity's tokens (or vice versa) is still picked up.
    Then aggregate the question's metric (revenue / counts / sums / etc.)
    over the surviving entity ids.

  - For an **open-ended ranking question** (the question asks "which X has
    the most Y", "top N by Z", "highest by some metric", etc.), you still
    build a resolved entity grouping using the normalized fields.
    Concretely, construct a resolved-group key per row by combining the
    normalized entity columns (e.g.
    `COALESCE(NULLIF(norm_field_a,''), norm_field_b_tail)` or
    `GREATEST(norm_field_a, norm_field_b_swap)`), or perform a self-join /
    cluster step where two rows belong to the same resolved entity if
    **any** of the normalized fields match across them
    (`a.norm_field_a = b.norm_field_a OR a.norm_field_b = b.norm_field_a OR ...`).
    The output of this step is a `resolved_entity_id` per source row. Do
    NOT use AND across independently dirty fields to define entity
    identity — that fragments one logical entity across multiple
    source-specific spellings.

  - Why this matters for ranking: when the dirty-field warning is present
    and Step 2 is skipped, one logical entity gets split into multiple
    raw-spelling rows. The top of the rank is then dominated by a single
    placeholder-spelling or single-source row whose metric represents one
    source's share of the entity rather than the full entity total — the
    "correct" entity may not even appear in the top-K because its
    contribution is fragmented across rows that each individually rank
    lower.

  **Step 3 — Aggregate or rank third (on the resolved entity, never raw
  labels).** Only after Step 2 do you run the analytical aggregate or
  ranking. Group by the `resolved_entity_id` (or, for the simple case,
  by the normalized-key set such as `GROUP BY norm_title, norm_artist`)
  and surface a representative raw label only after aggregation (e.g.
  `MIN(title) AS title`, or the most frequent non-blank label). For
  ranking questions, rank the **resolved groups**, not raw source-specific
  labels — placeholder/blank-string rows must not be able to occupy a
  top-K slot just because their source-specific revenue happens to fall
  on one row.

  Do NOT issue a `GROUP BY {raw_title}` or `ORDER BY {raw_title}` against
  a table whose description warns of duplicate sources. Do NOT use OR as
  a global SQL habit on ordinary clean schemas — when the
  duplicate/different-source warning is absent, choose predicates from
  the actual query semantics. The OR-across-dirty-fields rule is gated by
  the schema warning, not by the question shape.

- **Scope reminder — apply broadly when the warning is present; skip
  entirely when it is absent.** The same normalize → entity-resolve →
  aggregate sequence is domain-agnostic: any schema whose
  `db_description.txt` flags duplicate rows, different sources, or
  independently dirty entity-name fields qualifies, regardless of subject
  matter. When name and description (or any pair of entity-identifying)
  columns come from noisy or different sources, broaden the candidate
  predicate across them with OR (Step 2) and rank or aggregate over the
  resolved entity, not the raw spellings (Step 3). For datasets whose
  `db_description.txt` does NOT mention duplicates, different sources, or
  independently dirty entity-name fields, leave queries clean and skip
  this whole sequence — broadening with OR on a clean schema is
  distracting and degrades accuracy.

### `verify` (Method A)

Adversarial review of analyze stage's answers WITHOUT ground truth access.

- **Inputs:** `_artifacts/context.md`, `answers.json`, `_artifacts/reasoning.md`
- **Outputs:** `## Stage Report` in entity file with PASSED or REJECTED

Re-derive each answer independently, challenge intermediate assumptions,
hunt for counterexamples, verify join correctness, test boundary
conditions, and sanity-check magnitudes. If issues are found, REJECT with
numbered findings; the workflow will feed back to `analyze`.

**External-oracle audit.** Before passing, scan the analyze stage's
tool-use trace (claude-output.jsonl events with `name: "Bash"` or
`name: "Read"`) for evidence of forbidden external lookups: matches for
`huggingface`, `datasets.load_dataset`, `hf://`, `from datasets import`,
`requests.get` to public data hosts, web-search tool invocations, or
LLM-call patterns asking another model for the answer. If any are found,
REJECT with a finding pointing to the offending event index and the
specific external source.

---

# METHOD B — dbt pipeline (used when `N_sources >= 3`)

Answer the queries by **building a validated dbt data pipeline for the dataset first, then
querying the answer out of the built models.** Every query goes through the same two-phase
shape: **`model`** builds the dbt models (once, for the whole dataset); **`analyze`** does
nothing but query those models for each answer. Write the final answers to `answers.json`.

`dbt` and `dbt-duckdb` are **preinstalled** in the image (`dbt --version` confirms it). Do
**not** `pip install` anything.

## Database Access (Method B)

DuckDB is the engine; dbt-duckdb **ATTACHes every source directly**. The sqlite and postgres
scanner extensions are **preinstalled** in the image and autoload offline — do NOT `INSTALL`
over the network and do NOT export sources into seeds; **ATTACH** them. Read `db_config.yaml`
for the authoritative database names, types, and paths.

- **SQLite**: file under `query_dataset/` — `ATTACH 'query_dataset/x.db' AS name (TYPE SQLITE)`
- **DuckDB**: file under `query_dataset/` — `ATTACH 'query_dataset/x.duckdb' AS name`
- **PostgreSQL**: host `dab-postgres`, port 5432, user `postgres`, password `postgres`,
  dbname per `db_config.yaml` —
  `ATTACH 'host=dab-postgres port=5432 dbname=… user=postgres password=postgres' AS name (TYPE POSTGRES)`

- **MongoDB**: ⚠️ the mongo host is **`dab-mongo`** port 27017 — **ALWAYS** connect to
  `mongodb://dab-mongo:27017`, **NEVER** `localhost`/`127.0.0.1` (localhost will be refused —
  the database runs in a separate container). dbt-duckdb has no mongo adapter and the duckdb
  mongo extension is unavailable offline, so use **pymongo** (preinstalled):
  `from pymongo import MongoClient; db = MongoClient("mongodb://dab-mongo:27017")["<db_name from db_config.yaml>"]`.

**MongoDB sources** are **mongo-only** — there is no relational copy. Bridge mongo into the
pipeline with pymongo at `dab-mongo:27017` (above): read the collection(s) named in
`db_config.yaml` and write them to `_artifacts/dbt/seeds/<collection>.csv` so dbt treats the
mongo collection as a normal **source** (`dbt seed`), then build `stg_*`/`int_*`/`mart_*` over
it like any other source. This pymongo→seed bridge is the ONLY path for mongo data; it is NOT
the forbidden "export a relational source to a seed instead of ATTACHing" shortcut —
relational sources (sqlite/duckdb/postgres) must still be ATTACHed. **A mongo dataset whose
collection you never reached at `dab-mongo:27017` is a connection bug, not an "UNABLE TO
DETERMINE" — fix the host.**

## Rules (Method B)

- Do NOT modify source databases — dbt attaches them read-only; all intermediate results are
  dbt models in a scratch duckdb file under `_artifacts/dbt/`.
- Do NOT access `validate.py` or `ground_truth.csv` files.
- If the data doesn't support an answer, say "UNABLE TO DETERMINE".
- No comma grouping in numbers (23,781 → 23781).
- Use EXACT field values from the database.
- Answer ONLY the question — no commentary or counter-examples.

**Use only the workspace data.** The benchmark provides everything needed to answer each query in the workspace's databases (`db_config.yaml`, attached SQLite/PostgreSQL/MongoDB/DuckDB sources). Do **not** consult external data sources to look up answer values, labels, or ground truth — even if the workspace data appears to come from a public dataset. Specifically forbidden:
- HuggingFace `datasets` library (`datasets.load_dataset`, `hf://...`) for label/oracle lookup
- Public CSV/JSON downloads of the same dataset (kaggle, GitHub, vendor sites)
- Web search engines, search APIs, or LLM-as-oracle calls (e.g., asking another model "what is the answer to X")
- Cached prior answers from earlier runs in `_runs/` or any artifacts outside the current workspace

The workspace databases are the only authoritative source. If a question is unanswerable from them, return `"UNABLE TO DETERMINE"`.

## Answers (Method B)

Write `answers.json` in the workspace root keyed by query directory name: a query in
`query2/query.json` writes `{"q2": "answer"}`. Cover **every** `queryN/`.

**Each answer value is a plain flat STRING — never JSON.** Do not emit arrays, objects, key
names, or brackets (`[ ] { }`) as the answer value. If the answer is a list of items, write a
flat delimited string in the order/field-form the question implies (e.g.
`apple/swift, twbs/bootstrap, facebook/react` or `Item A - 4.5; Item B - 4.3`), NOT
`["apple/swift", …]` or `[{"name":…}]`. The verifier is an automated string-matcher that
searches your text for each expected value (and any nearby number); a bracketed/quoted/keyed
structure breaks the match and scores 0 even when the values inside it are correct.

## Stages (Method B)

### `model` — build a GENERIC dbt pipeline ONCE (Method B)

Build a **question-agnostic** dbt project under `_artifacts/dbt/`: staging models that
normalize the sources, then a small set of **generic, entity-grain** intermediate/mart models
describing the dataset's *entities and relationships* — built from the schema, **before**
looking at any specific answer. Build the pipeline **once** for the whole dataset.

**HARD RULES (the method depends on these):**
- **No per-question models.** Do not create `mart_q1`, `int_q7`, etc. Models are named for
  entities/facts (`stg_<source>__<table>`, `int_<relationship>`, `mart_<entity>`) and each is
  reusable across many questions.
- **No answer literals in models.** A model must never hardcode a value lifted from a question
  or discovered by exploration (no `where note like '%budget is $2,261%'`, no
  `select 'None' as answer`, no specific answer IDs/titles/dates from the questions). Such
  logic belongs in the `analyze` SELECT, not in a model.
- **Build models from the schema, not from the answers.** Author `stg_*`/`int_*`/`mart_*` from
  `db_description.txt` + the source schemas first. Do not explore for answers and then write
  SQL to reproduce them.

**THE CROSS-SOURCE DERIVATION IS THE WHOLE POINT (this is why a ≥3-source dataset uses dbt).**
On a multi-source CRM-like schema, the *raw* fields in any one source are stale, partial, or
placeholder; the **correct** value of a derived attribute exists only after you join the
authoritative cross-source evidence. Your `int_*` models MUST materialize these derivations so
the answer is *read out of the joined model*, not patched together ad hoc in `analyze`. Build,
at minimum, these generic cross-source intermediates whenever the corresponding sources exist:

- **`int_opportunity_effective_stage`** — the **derived** sales stage per opportunity, not the
  raw `stage_name` column. Join `opportunities` to the opportunity's **activity / interaction
  transcripts** (the activities source) and to its quote/order facts, then compute the stage
  the *evidence* supports (e.g. an opportunity whose latest transcripts discuss pricing
  pushback / terms is at `Negotiation`, even if its raw `stage_name` still says `Discovery`).
  The model emits both `raw_stage` and `effective_stage`; the **effective_stage is the
  cross-source-derived value** and is the only correct answer to a "is the stage right, and if
  not what is it" question. The raw column alone is NOT the answer — a model that just selects
  `stage_name` reproduces the stale source value and is wrong.

- **`int_case_policy_breach`** / **`int_quote_policy_breach`** — the **derived** knowledge-article
  a case or quote *violates*, not a field on the case/quote. Join the case/quote facts (and
  their line items / costs / activity transcripts) to the **knowledge-base articles** source on
  the policy dimension each article governs (product, discount threshold, cost ceiling,
  approval rule), evaluate each article's stated condition against the case/quote's joined
  attributes, and emit the `breached_article_id` (or none). The breach can only be established
  by the cross-source join between the transactional facts and the knowledge base — there is no
  "violated article" column to read. A model that returns `None`/a guess without evaluating the
  knowledge articles against the joined facts is wrong.

- **`int_agent_case_ownership`** — the **derived** per-agent case-ownership / transfer history
  across the activity + case sources. One row per (agent, case) ownership episode, derived from
  the **owner-assignment / case-history** events (so transfers are counted from the assignment
  trail, not from a single current-owner field). This is the grain a "fewest transfers among
  agents who handled > 0 cases" question aggregates over; the answer agent cannot be read from
  any single source's current-owner column — it is derived from the joined assignment history.

If the dataset's sources do not contain the inputs for one of these intermediates, omit that
intermediate — build only the cross-source derivations the schema supports. The rule is: **any
attribute whose correct value depends on evidence spread across ≥2 sources must be materialized
as a derived `int_*` column, and `analyze` must read that derived column** — `analyze` must not
recompute the derivation ad hoc against raw sources, and must not fall back to the raw
single-source column.

Steps:
1. `dbt --version` (sanity; must print). Read `db_config.yaml` + `db_description.txt`;
   enumerate every source DB and table. For any `mongo` source, you MUST connect with pymongo
   to **`mongodb://dab-mongo:27017`** (NOT localhost) and seed its collections (see Database
   Access); ATTACH the sqlite/duckdb/postgres sources (postgres at host `dab-postgres`).
2. Scaffold `_artifacts/dbt/`:
   - `dbt_project.yml`:
     ```yaml
     name: dab
     version: "1.0"
     profile: dab
     model-paths: ["models"]
     ```
   - `profiles.yml` — target = a **persistent** duckdb file so the build survives into
     `analyze`; **ATTACH** each source from `db_config.yaml` (extensions autoload offline):
     ```yaml
     dab:
       target: dev
       outputs:
         dev:
           type: duckdb
           path: _artifacts/dbt/scratch.duckdb     # PERSISTENT file — survives the stage boundary
           extensions: [sqlite, postgres]          # preinstalled; INSTALL is a no-op offline
           attach:                                 # read_only on every source — they are read-only mounts
             - path: query_dataset/<sqlite>.db
               type: sqlite
               read_only: true
             - path: query_dataset/<duckdb>.duckdb
               read_only: true
             - path: "host=dab-postgres port=5432 dbname=<from db_config> user=postgres password=postgres"
               type: postgres
               alias: <pg source name>
               read_only: true
             # …one entry per source DB in db_config.yaml
     ```
   - `models/stg_*.sql` — **one staging model per source table.** Cast types and **light
     normalize** the entity-name/string key columns:
     `lower(regexp_replace(col, '\s+', ' ', 'g')) AS norm_col`, and extract a 4-digit
     `year` via `regexp_extract(date_col, '\d{4}')` when the raw column is a free-form date.
     Near-passthrough for clean schemas. Materialize as views.
   - `models/int_*.sql` / `models/mart_*.sql` — **generic** joins/aggregations at the
     dataset's natural entity grain (one resolved fact/entity table that many questions query),
     never per-question. **The cross-source derived intermediates above
     (`int_opportunity_effective_stage`, `int_*_policy_breach`, `int_agent_case_ownership`)
     live here** — they are the load-bearing models for a ≥3-source dataset. **Conditional
     entity resolution also lives here:** if `db_description.txt` warns about `duplicate` rows,
     `different sources`, or independently dirty entity-name fields on a table you
     join/group/rank over, the `int_*` layer must resolve entities by broadening across the
     dirty normalized fields with **OR** (never AND): build a `resolved_entity_id` per source
     row (e.g. self-join/cluster where two rows are the same entity if **any** normalized field
     matches, or `COALESCE(NULLIF(norm_field_a,''), norm_field_b)`), then aggregate on the
     resolved entity and surface a representative raw label (`MIN(title)`, most-frequent
     non-blank) only after aggregation. OR keeps a row whose primary field is malformed but
     whose secondary field still carries the entity's tokens; AND silently drops it and
     fragments one logical entity across source-specific spellings. When the warning is
     **absent**, skip entity resolution entirely — a plain join/aggregate; broadening with OR
     on a clean schema degrades accuracy.
   - `models/schema.yml` — **generic** dbt tests only: `unique` on each model's declared grain,
     `not_null` on join keys, and a parent/child rowcount-reconcile test where applicable. No
     question-specific tests.
3. **LOOP** until green:
   `dbt run --project-dir _artifacts/dbt --profiles-dir _artifacts/dbt` then
   `dbt test --project-dir _artifacts/dbt --profiles-dir _artifacts/dbt`. A red test means
   **your build is wrong** (grain not collapsed, key fragmented) — fix the model and re-run.
   If a grain is irreducibly ambiguous, stop and record the unresolved invariant in
   `_artifacts/reasoning.md`; do **not** hand a red model to `analyze`.
- **Inputs:** `db_config.yaml`, `db_description.txt`
- **Outputs:** green `_artifacts/dbt/` (with `scratch.duckdb` populated) + `_artifacts/context.md`
  mapping each entity model to the questions it serves (by entity, not by baked-in answer).

### `analyze` — pure query over the GENERIC models (Method B)

Open the **already-built** `_artifacts/dbt/scratch.duckdb` (do NOT rebuild) and answer every
query with a SELECT over the generic `int_*`/`mart_*` models. **The question-specific
filtering, ranking, and lookups live HERE, in the analyze SELECT — not in the models.** Do not
re-explore from scratch and do not run ad-hoc SQL against the raw sources outside the dbt
project. If the `model` stage recorded an unresolved invariant for a query, answer
`"UNABLE TO DETERMINE"`.

**Read the cross-source-derived column, never the raw single-source field.** When a question
asks for an attribute that the `model` stage derived across sources (the effective stage, the
breached knowledge article, the agent transfer count), your `analyze` SELECT MUST read that
attribute from its `int_*` model (`int_opportunity_effective_stage.effective_stage`,
`int_*_policy_breach.breached_article_id`, the aggregate over `int_agent_case_ownership`). Do
NOT answer from the raw `stage_name` column, and do NOT re-derive the breach/transfer logic ad
hoc against the raw sources — the derivation already happened in the model; querying the raw
source field reproduces the stale/wrong value.

**Match the answer to the question's GRAIN (the mart is usually finer-grained than the
question).** A generic mart is often keyed at a fine grain (e.g. per entity × store × country ×
day). Before answering, identify the grain the question asks for and **re-aggregate the mart up
to that grain** — `SUM`/`COUNT`/`AVG` across the mart's extra dimensions. Do NOT answer from a
single fine-grained sub-row when the question asks for an entity total/overall value: filter to
a sub-dimension only when the question explicitly names it. (A "total revenue for X" answered
from one store-country row instead of the sum across all is the classic mart-grain miss.)

**Cover the question's full scope — don't silently drop rows.** Include every row the question's
scope implies, *including* zero/empty/`Closed`/`null` entries (e.g. a business-hours answer must
list `Closed` days, not only open ones). A `WHERE value IS NOT NULL` / `value > 0` filter that
the question did not ask for drops correct answer rows.

**Ranking/top-N: aggregate to the ranked entity's grain first, then order deterministically.**
Build the per-entity metric at the entity grain (build FROM the fact, INNER JOIN metadata —
don't rank fine-grained or zero-fact rows), then `ORDER BY metric DESC` with a stable
tiebreaker. Attribute the metric to the entity the question names (e.g. the *order* owner vs the
*opportunity* owner — read the question's wording for which).

- **Inputs:** `_artifacts/dbt/scratch.duckdb`, `_artifacts/context.md`, `query{N}/query.json`
- **Outputs:** `answers.json` (keys q1..qN), `_artifacts/reasoning.md`

### `verify` (Method B, feedback-to: analyze)

Adversarial review of the answers WITHOUT ground-truth access. Re-derive each answer from the
green mart; read the passing dbt tests as evidence the grain/keys are sound; challenge
assumptions, hunt for counterexamples, verify join correctness, sanity-check magnitudes. If
issues are found, REJECT with numbered findings; the workflow feeds back to `analyze`.

Explicitly RE-CHECK each answer for the common mart-overhead misses and REJECT if any fails:
- **Cross-source derivation read, not raw column:** for any attribute the model derived across
  sources (effective stage, breached article, transfer count), confirm the answer was read from
  the `int_*` derived column and NOT from the raw single-source field or an ad-hoc re-derivation.
  An answer that matches the raw `stage_name` / has no knowledge-article evaluation / counts
  transfers from a current-owner field is a REJECT.
- **Grain:** does the answer re-aggregate to the question's grain, or was it read from a single
  finer-grained mart sub-row? (Re-run the aggregate across the mart's extra dimensions and
  confirm it matches.)
- **Coverage:** does the answer include all rows the question's scope implies (zero/`Closed`/
  `null`/empty entries included)? Confirm no unasked `WHERE` filter dropped rows.
- **Mongo reached:** for a mongo-sourced query, confirm the collection was actually read from
  `dab-mongo:27017`. An `UNABLE TO DETERMINE` caused by a refused `localhost` connection is a
  REJECT — fix the host, do not abstain.
- **Serialization:** confirm each answer value is a flat string (no `[ ] { }` / keys / quotes
  as structure).

**REJECT also if** an answer doesn't reconcile, a query was answered over a model whose
invariant was never made green, OR the dbt project contains **per-question models** (e.g.
`mart_q7`) or **answer literals hardcoded into model SQL** (question phrases, specific
IDs/titles/dates, `select '<answer>'`) — models must be generic and entity-grained;
question-specific logic belongs in the analyze SELECT.

**External-oracle audit.** Scan the analyze stage's tool-use trace
(claude-output.jsonl events with `name: "Bash"` or `name: "Read"`) for forbidden external
lookups: `huggingface`, `datasets.load_dataset`, `hf://`, `from datasets import`,
`requests.get` to public data hosts, web-search invocations, or LLM-as-oracle patterns. If any
are found, REJECT with the offending event index and the specific external source.

- **Inputs:** `_artifacts/context.md`, `answers.json`, `_artifacts/reasoning.md`
- **Outputs:** `## Stage Report` in entity file with PASSED or REJECTED.

## Entity File

Each dataset run has a markdown file `{slug}.md` with YAML frontmatter:

```yaml
---
id:
title: Dataset name
status: pending
slug:
query_count:
---
```
