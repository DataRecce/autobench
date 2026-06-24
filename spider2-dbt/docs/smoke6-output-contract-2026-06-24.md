# spider2-dbt smoke6 #2 — output-contract README + f1001 fix — 2026-06-24

Second smoke. Two changes vs smoke #1 (`docs/smoke6-2026-06-24.md`):
1. **f1001 packaging fix** — `tools/package_spider2_dbt_views.py` now runs
   `_align_source_schemas_to_main()`: a faithful, idempotent normalization that
   sets `schema: main` on a `sources:` source whose default-name schema is absent
   from the DuckDB while `main` holds its tables. f1001 declared source
   `f1_dataset` with no `schema:` (dbt defaults schema→source name) but the export
   loaded raw tables into `main`, so the build-time preflight (and `dbt build`)
   failed. Fired only for f1001; no-op for the 5 consistent tasks. Verified
   preflight → `status: passed`.
2. **spider2-dbt-tuned solver README** — `solver_workflows/spider2-output-contract/`,
   replacing the ade `@baseline` README. Centers on the output-table contract:
   build NEW materialized model(s); name each by the project's existing
   convention (`dim_`/`fct_`/`obt_`, `<pkg>__<entity>_<suffix>`,
   `<dataset>__<method>_<n>`); build into `main`; match key+columns+grain.

- **Spec:** `specs/smoke6-output-contract.frozen.yaml` (only `solver_workflow`
  changed vs smoke #1 — independent-variable rule holds).
- **Run dir:** `runs/spider2-dbt-smoke6-output-contract/ee0dbcbc3efb04a5/` (rc=0, 35m44s).

## Result: 2/6 pass (was 0/6), 0 crashes (was 1)

| task | smoke#1 | smoke#2 | what changed |
|---|---|---|---|
| activity001 | 0.0 | **1.0** | built `dataset__aggregate_after_1` + `dataset__aggregate_all_ever_1` (convention naming landed) |
| f1001 | CRASH | **1.0** | packaging fix → runs; solved correctly |
| chinook001 | 0.0 (wrong name) | 0.0 | **correct names built** (`dim_customer`/`fct_invoice`/`obt_invoice`) but 2 placed under `models/intermediate/` = **ephemeral** → not in output DuckDB; only `obt_invoice` materialized |
| jira001 | 0.0 | 0.0 | **correct name** `jira__project_enhanced` built; column/value mismatch |
| tpch001 | 0.0 | 0.0 | correct name `client_purchase_status`; value mismatch |
| xero_new001 | 0.0 | 0.0 | **correct names** (all 3 xero__* reports) built; value mismatch |

## Reading

- **The README change fixed the dominant failure mode.** Smoke #1's zeros were
  largely wrong/missing table NAMES (chinook built `customer`). Smoke #2 produces
  convention-correct names in 6/6 tasks and flips 2 cells to PASS. The naming
  lever is real and README-steerable.
- **Residual failures split cleanly into two buckets:**
  - **chinook001 — a materialization/validation gap, still README-addressable.**
    Correct model names, but `models/intermediate/` is configured `ephemeral`, so
    `dim_customer`/`fct_invoice` compiled to CTEs and never became tables. The
    agent self-validated only `obt_invoice` existed (incomplete check =
    self-anchored false-green). Next README refinement: each target table must
    appear as a BASE TABLE in the output DuckDB — don't place targets in an
    `ephemeral`-configured dir; VALIDATE EVERY target table exists, not just one.
  - **jira001 / tpch001 / xero_new001 — genuine analytic difficulty.** Correct
    table names, wrong columns/values. This is the hard core of spider2-dbt
    (exact multi-table transformation semantics); not a simple README lever.

## Next levers (not yet run)
1. README: "validate EACH named target table exists as a BASE TABLE in the output
   DuckDB; if a target lands in an ephemeral/intermediate dir, override its
   materialization to `table`." (Targets chinook-class misses.)
2. The value-level core (jira/tpch/xero) is real benchmark difficulty — expect low
   pass rates; no cheap README fix. Candidate for a larger task sample to size the
   ceiling before investing.
