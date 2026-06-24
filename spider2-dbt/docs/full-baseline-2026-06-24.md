# spider2-dbt FULL run — spider2-dbt-baseline solver — 2026-06-24

First full-board run of spider2-dbt.

- **Spec:** `specs/full-baseline.frozen.yaml` — `kind: harbor-local`, codex
  `spacedock_solver`, gpt-5.5, `reasoning_effort: xhigh`, `trials: 1`,
  **`concurrency.trials: 4`**.
- **Solver:** `solver_workflows/spider2-dbt-baseline/` (output-contract + ade-bench
  gated dbt rules merged).
- **Tasks:** 61 (68 declared − 4 goldless [airbnb002, biketheft001, gitcoin001,
  google_ads001] − 3 Postgres-backed [inzight001, shopify001, shopify002]).
- **Run dir:** `runs/spider2-dbt-full-baseline/13fb630e2cae3eb8/` (rc=0, ~2h38m).

## Headline

| denominator | pass | rate |
|---|---|---|
| 61 tasks launched (build failures counted as fail) | 16 | **26.2%** |
| **52 tasks that actually ran** (9 build-time infra failures excluded) | 16 | **30.8%** |

16 PASS, 36 genuine solver mismatches, 9 build-time exceptions (never reached the
agent).

**Passes (16):** activity001, app_reporting001, app_reporting002, f1001,
google_play001, google_play002, greenhouse001, hubspot001, lever001, maturity001,
mrr001, mrr002, playbook001, qualtrics001, quickbooks002, tickit001.

## The 9 build-time exceptions (NOT solver failures)

All failed at the Docker image build's `razorback_spider2_preflight.py` step
(`exit 2` = declared source tables not found). Two sub-types:

- **Missing source data in the local Spider2 checkout (6):** asset001 (`main.positions`),
  atp_tour001 (countries/matches/players), divvy001 (`divvy_data_raw.divvy_data`),
  nba001 (multi-schema `nba_data.*`/`psa.*`), retail001 (`main.country`), tpch002
  (all TPC-H source tables absent). The shipped DuckDB lacks declared source
  tables — a data-provisioning gap, NOT packager-fixable (faking data would be wrong).
- **Jinja-templated source identifiers (3):** synthea001, workday001, workday002 —
  sources declared as `{{ var(...) }}` / `{% if %}` expressions; the preflight reads
  raw YAML and compares the literal Jinja string. A razorback preflight limitation
  (read-only submodule); would need Jinja rendering of source schema/identifier fields.

These 9 are excluded from the solver-attributable rate (30.8% over 52 ran).

## Reading vs the smokes

- Smoke #2 / v2 on 6 tasks = 2/6 (33%), but that sample was skewed toward hard
  semantic tasks. The full board's 30.8% is the representative solver rate.
- The packager `_align_source_schemas_to_main()` fix held: no schema-alignment
  failures on the full board (f1001 ran and PASSED). The remaining build failures
  are a different class (missing data / Jinja sources).
- Failure mode of the 36 mismatches is the same two buckets diagnosed on tpch001:
  structural (wrong table name / grain / ephemeral) + semantic (right table, wrong
  values on underspecified instructions = the oracle wall).

## Re-run of the 9 (after razorback PR #23 + #25) — MERGED CLEAN BOARD

razorback fixes landed: PR #23 (`fix-spider2-dbt-preflight-sources`, source
resolution in harbor_view.py + preflight) and PR #25 (`fix spider2 dbt templated
source preflight`, Jinja rendering of `{{ var(...) }}` source names/schemas).
Re-packaged the 9 (rebake the preflight) → all 9 preflight-pass locally
(`missing: 0`) → re-ran (`runs/spider2-dbt-full-baseline-rerun9/697486bf1c61c820`,
~31m, conc 4): **PASS=3 (tpch002, workday001, workday002), fail=6, exc=0.**

**MERGED FULL BOARD (original 61 with the 9 exceptions replaced by their real
outcomes): 19 PASS / 42 fail / 0 exc = 19/61 = 31.1%.** No build-time exclusions
remain — every one of the 61 DuckDB-runnable tasks now executes and scores.

## Next-lever candidates
1. The 30.8% is the spider2-dbt-baseline anchor — register as `@baseline` for the
   spider2-dbt namespace if promoting.
2. To recover the 6 missing-data tasks: re-provision source DuckDBs from upstream
   (DBT_start_db re-extract) — infra, not solver.
3. The 3 Jinja-source tasks need a preflight that renders dbt Jinja — razorback change.
4. Solver headroom is the 36 mismatches; per the oracle-wall analysis, the
   structural fraction is addressable, the pure-definition fraction is the floor.
