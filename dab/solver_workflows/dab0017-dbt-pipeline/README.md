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

# Solve a DataAgentBench dataset by building a dbt pipeline

Answer the queries for the current dataset by **building a validated dbt data pipeline for
the dataset first, then querying the answer out of the built models.** Every dataset goes
through the same two-phase shape: **`model`** builds the dbt models (once, for the whole
dataset); **`analyze`** does nothing but query those models for each answer. Write the final
answers to `answers.json` at the workspace root.

`dbt` and `dbt-duckdb` are **preinstalled** in the image (`dbt --version` confirms it). Do
**not** `pip install` anything.

## Workspace Layout (one workspace for the whole dataset)

```
workdir/
├── README.md             ← workspace README (DB hosts/paths)
├── db_config.yaml        ← database connection details (may be named connections.yaml)
├── db_description.txt    ← schema documentation
├── query_dataset/        ← raw source DB files (read-only)
├── query1/query.json     ← one subdir per query
├── query2/query.json
├── ...
└── answers.json          ← write ALL answers here, keyed q1, q2, …
```

## Database Access

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

**MongoDB sources** (e.g. yelp business info, agnews articles) are **mongo-only** — there is
no relational copy. Bridge mongo into the pipeline with pymongo at `dab-mongo:27017` (above):
read the collection(s) named in `db_config.yaml` and write them to
`_artifacts/dbt/seeds/<collection>.csv` so dbt treats the mongo collection as a normal
**source** (`dbt seed`), then build `stg_*`/`int_*`/`mart_*` over it like any other source.
This pymongo→seed bridge is the ONLY path for mongo data; it is NOT the forbidden "export a
relational source to a seed instead of ATTACHing" shortcut — relational sources
(sqlite/duckdb/postgres) must still be ATTACHed. **A mongo dataset whose collection you never
reached at `dab-mongo:27017` is a connection bug, not an "UNABLE TO DETERMINE" — fix the host.**

## Rules

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

## Answers

Write `answers.json` in the workspace root keyed by query directory name: a query in
`query2/query.json` writes `{"q2": "answer"}`. Cover **every** `queryN/`.

**Each answer value is a plain flat STRING — never JSON.** Do not emit arrays, objects, key
names, or brackets (`[ ] { }`) as the answer value. If the answer is a list of items, write a
flat delimited string in the order/field-form the question implies (e.g.
`apple/swift, twbs/bootstrap, facebook/react` or `Item A - 4.5; Item B - 4.3`), NOT
`["apple/swift", …]` or `[{"name":…}]`. The verifier is an automated string-matcher that
searches your text for each expected value (and any nearby number); a bracketed/quoted/keyed
structure breaks the match and scores 0 even when the values inside it are correct.

## Stages

### `model` — build a GENERIC dbt pipeline ONCE (every dataset)

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
     never per-question. **Conditional entity resolution lives here:** if `db_description.txt`
     warns about `duplicate` rows, `different sources`, or independently dirty entity-name
     fields on a table you join/group/rank over, the `int_*` layer must resolve entities by
     broadening across the dirty normalized fields with **OR** (never AND): build a
     `resolved_entity_id` per source row (e.g. self-join/cluster where two rows are the same
     entity if **any** normalized field matches, or
     `COALESCE(NULLIF(norm_field_a,''), norm_field_b)`), then aggregate on the resolved entity
     and surface a representative raw label (`MIN(title)`, most-frequent non-blank) only after
     aggregation. OR keeps a row whose primary field is malformed but whose secondary field
     still carries the entity's tokens; AND silently drops it and fragments one logical entity
     across source-specific spellings. When the warning is **absent**, skip entity resolution
     entirely — a plain join/aggregate; broadening with OR on a clean schema degrades accuracy.
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

### `analyze` — pure query over the GENERIC models

Open the **already-built** `_artifacts/dbt/scratch.duckdb` (do NOT rebuild) and answer every
query with a SELECT over the generic `int_*`/`mart_*` models. **The question-specific
filtering, ranking, and lookups live HERE, in the analyze SELECT — not in the models.** Do not
re-explore from scratch and do not run ad-hoc SQL against the raw sources outside the dbt
project. If the `model` stage recorded an unresolved invariant for a query, answer
`"UNABLE TO DETERMINE"`.

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

### `verify` (feedback-to: analyze)

Adversarial review of the answers WITHOUT ground-truth access. Re-derive each answer from the
green mart; read the passing dbt tests as evidence the grain/keys are sound; challenge
assumptions, hunt for counterexamples, verify join correctness, sanity-check magnitudes. If
issues are found, REJECT with numbered findings; the workflow feeds back to `analyze`.

Explicitly RE-CHECK each answer for the common mart-overhead misses and REJECT if any fails:
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
