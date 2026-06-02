# Fix: ade-bench non-airbnb images shipped the airbnb DuckDB

**Status:** ✅ RESOLVED 2026-06-02 (no razorback changes). See "Resolution" below.
**Discovered:** 2026-06-02, while tracing run `runs/ade-bench-baseline/d132984257eca967`
(tasks `ana-eng001`, `ana-eng002`, both `reward 0`).

> **Note:** the original root-cause theory in §2 (transient gdown/Drive failure under
> concurrency) was **wrong**. The real cause was a poisoned BuildKit `COPY` cache layer —
> see "Corrected root cause" and "Resolution" at the end. §1 (symptom) and the scope table
> remain accurate.

---

## 1. Symptom

Every **non-airbnb** ade-bench family image (`ana-eng`, `asana`, `f1`, `intercom`,
`quickbooks`) has `/app/<db_name>.duckdb` populated with the **airbnb** raw tables
(`RAW_HOSTS / RAW_LISTINGS / RAW_REVIEWS`) instead of its own source data.

Consequence: the dbt projects reference sources that don't exist, so models error at
run/verify time and every affected task is effectively unsolvable.

Observed in the traced run:

- **ana-eng001** — task is a genuine no-op ("do not make any changes"); agent correctly
  did nothing, but the verifier expects a fully-built project (519 columns) and the DB
  has only 31 columns of airbnb data → `reward 0`.
- **ana-eng002** — task "fix the syntax error in `obt_product_inventory.sql`"; agent's
  fix (missing comma) was correct, but `dbt run` failed with
  `Catalog Error: Table with name fact_inventory does not exist!` (upstream northwind
  sources `inventory_transactions`, `invoices`, … absent) → `reward 0`.

Per-family evidence (one image each):

| family     | built image contains                              | size    | correct? |
|------------|---------------------------------------------------|---------|----------|
| airbnb     | `RAW_HOSTS/RAW_LISTINGS/RAW_REVIEWS`               | 110 MB  | ✅       |
| ana-eng    | airbnb tables + `dim_date`                        | 110 MB  | ❌       |
| f1         | airbnb tables (md5 identical to airbnb)           | 110 MB  | ❌       |
| asana      | airbnb tables                                     | 110 MB  | ❌       |
| intercom   | airbnb tables                                     | 110 MB  | ❌       |
| quickbooks | airbnb tables + `int_quickbooks__*` models        | 113 MB  | ❌       |

---

## 2. Root cause

**The config and the Drive files are correct. The image build is what went wrong.**

- Each family's `environment/db_file_id.txt` Google-Drive ID is **distinct and correct**.
- A **fresh `gdown`** of every ID today returns the **correct** per-family DB:

  | family     | Drive ID serves now (tables)                       | size   |
  |------------|----------------------------------------------------|--------|
  | airbnb     | `RAW_HOSTS/RAW_LISTINGS/RAW_REVIEWS`               | 110 MB |
  | ana-eng    | `customer, employees, inventory_transactions, invoices, …` (northwind) | 6.3 MB |
  | f1         | `circuits, constructors, constructor_standings, …` | 9.7 MB |
  | asana      | `project_data, task_data, section_data, …`         | 3.7 MB |
  | intercom   | `admin_data, conversation_history_data, …`         | 4.7 MB |
  | quickbooks | `account_data, bill_data, invoice_data, …`         | 49 MB  |

- The built images (created ~6 days before the run, **concurrently across 48 tasks**)
  used the old `COPY db_file_id.txt` Dockerfile form with **no preflight layer**. The
  `gdown <correct_id>` step nonetheless produced the 110 MB airbnb file for non-airbnb
  families.
- `f1`'s image is **byte-identical** to airbnb's (`md5 5e90fde7…`), and its correct DB is
  only 9.7 MB → `gdown` definitively fetched the wrong (airbnb) file at build time.

**Conclusion:** a transient **Google Drive rate-limit / content substitution under
concurrent builds** (the Dockerfile comment explicitly warns about Drive rate limits),
combined with **no download content-verification**, so the wrong DB shipped silently.

### Guard that exists but didn't catch it

`razorback/src/razorback/benchmarks/ade_bench/preflight.py` injects a build-time DuckDB
table check (required/forbidden family "sentinel" tables, fail-closed). But:

1. The affected images **predate** that feature (commits `c02e80c`, `8383c92`).
2. `_CONTRACTS` only covers **airbnb / f1 / quickbooks** — `ana-eng / asana / intercom`
   have no contract, so `contract_for_task_id()` returns `None` and the check is skipped.

➡️ A plain rebuild will *likely* fix the data (Drive is correct now), but only the
preflight-coverage fix **guarantees** it and protects future builds. Do both.

---

## 3. Plan

### Phase 1 — Confirm full scope (cheap)
Audit all 48 built images (not one-per-family) and record which ship airbnb data:

```bash
for img in $(docker images --format '{{.Repository}}:{{.Tag}}' | grep ade-bench); do
  docker run --rm "$img" python -c "import duckdb,glob;p=glob.glob('/app/*.duckdb')[0];\
print('$img', sorted({r[1].lower() for r in duckdb.connect(p,read_only=True)\
.execute('select table_schema,table_name from information_schema.tables').fetchall()})[:6])"
done
```
Flag any non-airbnb image whose tables include `raw_hosts/raw_listings/raw_reviews`.
Verify quickbooks specifically (its image is partial).

### Phase 2 — Close the verification gap (code) — **required**
File: `razorback/src/razorback/benchmarks/ade_bench/preflight.py`
1. Add `_FAMILY_SENTINELS` + `_CONTRACTS` entries for the uncovered families:
   - `ana-eng`  → `expected_db_name="analytics_engineering"`, `task_prefixes=("ana-eng",)`,
     sentinels e.g. `{invoices, inventory_transactions, customer}`
   - `asana`    → `expected_db_name="asana"`, sentinels e.g. `{task_data, project_data}`
   - `intercom` → `expected_db_name="intercom"`, sentinels e.g. `{admin_data, conversation_history_data}`
2. Make **every** non-airbnb contract list the airbnb sentinels in `forbidden_tables`
   (the exact cross-contamination signal we hit). Required tables still auto-derive from
   each project's dbt `sources:`.
3. Extend `razorback/tests/unit/test_ade_bench_harbor_view.py` to cover the new families.

### Phase 3 — Harden the download — **recommended**
In the gdown block (templated via `harbor_view.py`):
1. **Retry with backoff** around `gdown` (Drive 429s are transient).
2. After download, assert it's a valid DuckDB and (ideally) matches a **per-family
   content sha256** baked alongside the existing `db_file_id_sha256`. Turns silent
   substitution into a hard build failure even before preflight.
3. Serialize / rate-limit concurrent builds to avoid re-triggering Drive throttling.

### Phase 4 — Force a clean rebuild — **required**
1. Bust the Docker cache so the gdown layer actually re-runs: build with `--no-cache`
   (or set `environment.force_build: true` in `specs/baseline.yaml` **and** ensure a
   no-cache path). A cached layer would keep the bad DB.
2. With Phase 2 in place, any build that still pulls wrong data **fails closed**.
3. Scope: at minimum all non-airbnb families; cleanest is all 48 for a consistent set.

### Phase 5 — Re-run & verify — **required**
1. Re-run `ade-bench-baseline` (or first just the previously-broken tasks: ana-eng,
   asana, f1, intercom, quickbooks).
2. Spot-check ana-eng002 `obt_product_inventory` now builds against real northwind data
   and rewards reflect genuine solving, not infra failure.
3. Re-baseline `specs/baseline.frozen.yaml` if reference numbers shift.

---

## 4. Decision

- **Quick path:** Phase 4 + 5 only (rebuild `--no-cache` + re-run). Fastest; relies on
  Drive being healthy now; leaves no future guard for ana-eng/asana/intercom.
- **Durable path (recommended):** Phase 2 → 3 → 4 → 5. ~1–2 hrs of code work; every
  family is verified at build time and fails closed forever.

---

## Corrected root cause (what it actually was)

A **poisoned BuildKit `COPY db_file_id.txt` layer** — not Drive, not the config.

- Every task's `db_file_id.txt` Drive ID is correct; a fresh `gdown` of each ID returns
  the right per-family DB.
- The images were originally built when the IDs were wrong (all pointing at airbnb's
  `1a26gCSe…`). BuildKit cached the `COPY db_file_id.txt` + `RUN gdown` layers.
- After the IDs were corrected on disk, rebuilding **from the same dataset cache path
  reused the stale cached `COPY` layer (still holding the airbnb id) even with
  `--no-cache`** → re-downloaded airbnb every time.
- **Proof:** building from the original path logged `FILE_ID=1a26gCSe…` (airbnb) while the
  on-disk file was `19c9UiDU…`; building from a fresh-copied context, or after
  `docker builder prune -af`, logged the correct id and pulled the right DB.
- The earlier `:rebuild` fix attempt failed for exactly this reason (rebuilt without
  purging the cache).

## Resolution (applied 2026-06-02, no razorback changes)

1. `docker builder prune -af` — evicted the poisoned BuildKit cache (freed ~59 GB).
2. Verified: a post-purge build from the original path used the correct id and produced
   real northwind data (ana-eng002 → 46 tables, status ok).
3. Rebuilt **all 48 base images** from `~/.cache/razorback/harbor/datasets/ade-bench-*/environment`,
   tagging each `hb__dbt-labs-ade-bench-<task>` (the exact tag the harbor-dataset run
   reuses: `delete=False`, `force_build=false`). Verified each image's DuckDB:
   all 48 `ok`, **0 contaminated** (airbnb 20–21 tables, ana-eng 39–47, asana/f1/intercom 20,
   quickbooks 20–120).
4. Removed 277 stale per-trial `*-main` images and 48 contaminated `:rebuild` orphans.

**Re-verify any image:**
```bash
docker run --rm <img> python -c "import duckdb,glob;\
print(sorted(r[1] for r in duckdb.connect(glob.glob('/app/*.duckdb')[0],read_only=True)\
.execute('select table_schema,table_name from information_schema.tables').fetchall()))"
```
Non-airbnb must NOT contain `raw_hosts/raw_listings/raw_reviews`.

**Next step:** re-run `ade-bench-baseline`; the harbor path will reuse the clean
`hb__dbt-labs-ade-bench-<task>` images. If any task rebuilds, the cache is now clean so it
will fetch correct data.

**Durable prevention (needs razorback, deferred):** extend `preflight.py` `_CONTRACTS` to
ana-eng/asana/intercom so the build fail-closes on wrong data; and note that a clean
rebuild requires a purged BuildKit cache (or fresh context) — `--no-cache` alone did not
evict the poisoned `COPY` layer.

## 5. Reference: key paths

- Run traced: `runs/ade-bench-baseline/d132984257eca967/{ade-bench-ana-eng001__*,ade-bench-ana-eng002__*}/`
- Dataset cache: `~/.cache/razorback/harbor/datasets/ade-bench-<task>/environment/{Dockerfile,db_file_id.txt,db_name.txt,setup.sh}`
- Preflight guard: `razorback/src/razorback/benchmarks/ade_bench/preflight.py`
- Dockerfile/gdown templating: `razorback/src/razorback/benchmarks/ade_bench/harbor_view.py`
- Dataset pin: `specs/baseline.yaml` → `benchmark.dataset: dbt-labs/ade-bench@sha256:2c1f9e69…`
