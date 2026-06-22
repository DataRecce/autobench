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

# Gate-0 feasibility probe — dbt pipeline (THROWAWAY)

This is a **feasibility probe**, not a scored hypothesis. The goal is to prove the
*runtime* works end-to-end: build a **dbt** pipeline **once** for this dataset in the
`model` stage, then answer **every** query from the built models in the `analyze` stage,
into one `answers.json`. Correctness of individual answers is secondary — what we are
proving is that one dbt build serves all queries, the dbt scratch DB survives the
`model -> analyze` stage boundary, and the batch verifier produces per-query rewards.

`dbt` and `dbt-duckdb` are **preinstalled** in the image — confirm with `dbt --version`.
Do **not** `pip install` anything.

## Workspace Layout (batch mode — one workspace for the whole dataset)

```
workdir/
├── README.md             ← workspace README (DB hosts/paths)
├── db_config.yaml        ← database connection details (may also be connections.yaml)
├── db_description.txt    ← schema documentation
├── query_dataset/        ← raw source DB files (read-only)
├── query1/query.json     ← one subdir per query
├── query2/query.json
├── ...
└── answers.json          ← write ALL answers here, keyed q1, q2, …
```

## Database access (read `db_config.yaml` for the authoritative names/paths)

DuckDB is the engine; dbt-duckdb **ATTACHes every source directly** (the sqlite & postgres
scanner extensions are **preinstalled** in the image and autoload offline — no `INSTALL`/
network needed). Do NOT export sources into seeds; ATTACH them.
- **sqlite** / **duckdb** sources: files under `query_dataset/` (attach by path).
- **postgres** sources: host `dab-postgres`, port 5432, user `postgres`, password
  `postgres`, dbname per `db_config.yaml` (`ATTACH 'host=dab-postgres port=5432
  dbname=… user=postgres password=postgres' (TYPE POSTGRES)`).

## Rules

- Do NOT modify source databases — dbt attaches them read-only; all intermediate
  results are dbt models in a scratch duckdb file under `_artifacts/dbt/`.
- Do NOT access `validate.py` or `ground_truth.csv`.
- If the data doesn't support an answer, write `"UNABLE TO DETERMINE"` for that query.

**Use only the workspace data.** Do not consult external sources (HuggingFace `datasets`,
`hf://`, public CSV/JSON downloads, web search, or LLM-as-oracle) — even if the data looks
public. The workspace databases are the only authoritative source.

## Answers

Write `answers.json` in the workspace root keyed by query directory name: a query in
`query2/query.json` writes `{"q2": "answer"}`. Cover **every** `queryN/`.

## Stages

### `model` — build a GENERIC dbt pipeline ONCE (every dataset)

Build a **question-agnostic** dbt project under `_artifacts/dbt/`: staging models that
normalize the sources and a small set of **generic, entity-grain** intermediate/mart models
that describe the dataset's *entities and relationships* — NOT one model per question. Build
it **once** for the whole dataset, before looking at any specific answer.

**HARD RULES (the method depends on these):**
- **No per-question models.** Do not create `mart_q1`, `mart_q7`, etc. Models are named for
  entities/facts (`int_leads`, `mart_cases`, `mart_agent_activity`), and each is reusable
  across many questions.
- **No answer literals in models.** A model must never hardcode a value lifted from a
  question or discovered by exploration (no `where x like '%budget is $2,261%'`, no
  `select 'None' as answer`, no specific IDs/titles/dates from the questions). If you catch
  yourself pasting a question's literal into a model, that logic belongs in the `analyze`
  SELECT instead.
- **Build models from the schema, not from the answers.** Author `stg_*`/`int_*`/`mart_*`
  from `db_description.txt` + the source schemas FIRST. Do not explore for answers and then
  write SQL to reproduce them.

Steps:
1. `dbt --version` (sanity; must print).
2. Read `db_config.yaml` + `db_description.txt`. Enumerate every source DB and table.
3. Scaffold `_artifacts/dbt/`:
   - `dbt_project.yml`:
     ```yaml
     name: dab
     version: "1.0"
     profile: dab
     model-paths: ["models"]
     ```
   - `profiles.yml` (target = a **persistent** duckdb file so the build survives into
     `analyze`; **ATTACH** each source from `db_config.yaml` — extensions autoload offline):
     ```yaml
     dab:
       target: dev
       outputs:
         dev:
           type: duckdb
           path: _artifacts/dbt/scratch.duckdb     # PERSISTENT file — survives stage boundary
           extensions: [sqlite, postgres]          # preinstalled; INSTALL is a no-op offline
           attach:
             - path: query_dataset/core_crm.db          # sqlite
               type: sqlite
             - path: query_dataset/sales_pipeline.duckdb # duckdb (no type)
             - path: "host=dab-postgres port=5432 dbname=<from db_config> user=postgres password=postgres"
               type: postgres
               alias: <pg source name>
             # …one entry per source DB in db_config.yaml
     ```
   - `models/stg_*.sql` — **one staging model per source table**: `SELECT`-cast + light
     normalize (lowercase/whitespace-collapse string keys, extract years). Views are fine.
   - `models/int_*.sql` / `models/mart_*.sql` — **generic** joins/aggregations at the
     dataset's natural entity grain (one resolved fact/entity table that many questions
     query). When `db_description.txt` warns of duplicate/different-source/dirty
     entity-name fields, the `int_*` layer also does entity resolution (OR across the dirty
     normalized fields). No question-specific filtering here.
   - `models/schema.yml` — generic tests: `unique` on each model's declared grain,
     `not_null` on join keys.
4. **LOOP** from inside `_artifacts/dbt/`:
   `dbt run --project-dir _artifacts/dbt --profiles-dir _artifacts/dbt` then
   `dbt test  --project-dir _artifacts/dbt --profiles-dir _artifacts/dbt`. If a model
   fails to build or a test is red, fix the model and repeat **until green** (or, if a
   grain is irreducibly ambiguous, record the unresolved invariant and move on — do not
   hand a red model to `analyze`).
- **Inputs:** `db_config.yaml`, `db_description.txt`
- **Outputs:** green `_artifacts/dbt/` (with `scratch.duckdb` populated) + `_artifacts/context.md`
  mapping each entity model to the questions it serves (by entity, not by baked-in answer).

### `analyze` — pure query over the GENERIC models

Open the **already-built** `_artifacts/dbt/scratch.duckdb` (do NOT rebuild) and answer
every query with a SELECT over the generic `int_*`/`mart_*` models. **The question-specific
filtering, ranking, and lookups live HERE, in the analyze SELECT — not in the models.** No
ad-hoc SQL against the raw sources outside the dbt project; query the built models.

- **Inputs:** `_artifacts/dbt/scratch.duckdb`, `_artifacts/context.md`, `query{N}/query.json`
- **Outputs:** `answers.json` (keys q1..qN), `_artifacts/reasoning.md`

### `verify` (feedback-to: analyze)

Re-derive each answer from the green models; read the passing dbt tests as evidence the
grain/keys are sound. REJECT if an answer doesn't reconcile or a query was answered over a
model whose invariant was never made green. **Also REJECT if the dbt project contains
per-question models (e.g. `mart_q7`) or answer literals hardcoded into model SQL (question
phrases, specific IDs/titles/dates, `select '<answer>'`) — models must be generic and
entity-grained; question-specific logic belongs in the analyze SELECT.** Scan the analyze
tool-use trace for forbidden external lookups (`huggingface`, `datasets.load_dataset`,
`hf://`, web-search, LLM-oracle); REJECT with the offending event index if found.

- **Outputs:** `## Stage Report` with PASSED or REJECTED.

## Entity File

Each run has `{slug}.md` with YAML frontmatter (`id`, `title`, `status`, `slug`,
`query_count`).
