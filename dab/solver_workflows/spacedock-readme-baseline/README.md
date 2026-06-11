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

# Solve a DataAgentBench dataset

Answer the queries for the current dataset. The workspace contains
connection details, a schema description, and one `queryN/` subdirectory
per query. Work the dataset through the stages below
(`model -> analyze -> verify -> done`) and write the final answers to
`answers.json` at the workspace root.

## Workspace Layout

```
workspace/
├── README.md             ← this file
├── connections.yaml      ← database connection details
├── db_description.txt    ← schema documentation
├── query1/query.json
├── query2/query.json
├── ...
└── answers.json          ← write your final answers here
```

## Database Access

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
- **PostgreSQL**: `conn.execute("INSTALL postgres"); conn.execute("LOAD postgres")` then
  `conn.execute("ATTACH 'host=localhost port=5432 dbname=X user=postgres password=dabench' AS name (TYPE POSTGRES)")`
- **MongoDB**: `conn.execute("LOAD mongo")` then
  `conn.execute("ATTACH 'mongodb://localhost:27017/dbname' AS name (TYPE MONGO)")`
  Mongo tables use triple-level naming: `attach_name.db_name.collection`.

Read `connections.yaml` for database names, types, and paths.

## Rules

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

## Answers

Write `answers.json` in the workspace root. Use the query directory name
as the key — e.g., a query in `query2/query.json` writes `{"q2": "answer"}`.

## Stages

### `model`

Explore databases and produce a context document for downstream stages.

- **Inputs:** `db_description.txt`, `connections.yaml`
- **Outputs:** `_artifacts/context.md`

Enumerate every table, record column types and sample values, identify
join keys, note data quality issues, and recommend a query approach per
question.

### `analyze`

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

### `verify`

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
