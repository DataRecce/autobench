# DAB dbt-Pipeline Solver — Implementation Handoff

**Date:** 2026-06-21
**For:** remote implementation server (executes; does not redesign)
**Design (the "why"):** `dab/docs/specs/2026-06-21-dbt-pipeline-solver-design.md` — read it once,
then use this runbook for the ordered steps. Where they ever disagree, the design doc wins;
file an issue rather than improvising.
**Operating rules:** `AGENTS.md` (run prerequisites, leak-guard, detached-run discipline) and
`dab/docs/specs/2026-06-15-dab-autoresearch-design.md` (the loop this plugs into).

---

## 0. TL;DR — what you're building

Make codex/gpt-5.5 answer DAB by **building a dbt pipeline per dataset, then querying it** —
for **every** dataset (mandatory), with the answer stage reduced to "query the models." The
**only lever** is the solver README. Success = beat the Opus incumbent on stratified Pass@1
**and regress zero currently-passing queries** (per-query, global).

Execute the gates **in order**. Each has a STOP condition — do not proceed past a red gate.

---

## 1. Prerequisites (every shell)

```bash
cd <repo>/dab
export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"
export RAZORBACK_REGISTRY="$(git rev-parse --show-toplevel)/dab/razorback-registry.yaml"  # project-local; do NOT touch the global ade-bench registry
# codex auth configured; Docker/Colima running; dataset dab@1.0 resolves; data_root points at your dataagentbench/data checkout
rk() { uv run --project ../razorback rk "$@"; }   # or the alias from AGENTS.md
```

- **Long runs (>30 min): always** launch via `drivers/rk-run-detached.sh <key> <frozen-spec> [run|matrix]`
  and watch `runs/.rk-handles/<key>-*/done` (the sentinel; absent ⇒ not finished). Never block a
  turn on a multi-hour run. `--runs-dir runs` is implied by the driver.
- `rk run --explain` ($0) before any real run. `rk freeze --allow-missing` every spec before running it.

---

## 2. Step 0 — bake dbt into the agent image (BLOCKER)

The `dab-agent:latest` Dockerfile lives in the **sibling `dataagentbench` repo** (not here;
PKG-24 to vendor it is backlog).

1. Edit `dataagentbench/benchmark/Dockerfile.agent` — append `dbt-core dbt-duckdb` to the
   existing `pip install --break-system-packages …` line (keep `duckdb psycopg2-binary pymongo
   pyyaml python-dotenv`). **Only `dbt-duckdb`** — DAB reaches SQLite/PG/Mongo via DuckDB
   `ATTACH`; no `dbt-postgres`.
2. Rebuild (reuse the pinned base digest so only the dbt layer changes):

   ```bash
   cd <path>/dataagentbench
   EXEUNTU_DIGEST="sha256:3b4a7e6d616929d0c07fe827711d444ca8d1ebd2f0ce54788d697b9f125a2e82"  # = setup.sh:36
   docker pull "ghcr.io/boldsoftware/exeuntu@${EXEUNTU_DIGEST}"
   docker build --build-arg EXEUNTU_DIGEST="${EXEUNTU_DIGEST}" \
     -f benchmark/Dockerfile.agent -t dab-agent:latest .
   docker inspect --format '{{.Id}}' dab-agent:latest   # record this digest in the run notes (provenance only)
   ```

**STOP unless:** `docker run --rm dab-agent:latest dbt --version` prints a version.

---

## 3. Gate 0 — batch feasibility probe (BLOCKER, cheap)

Prove the **load-bearing batch runtime**, not a toy. Author a throwaway solver README that, on
a **multi-query** dataset under **`query_mode: batch` + `workspace_variant: spacedock`**:
builds the dbt pipeline **once**, answers **all** queries into one `answers.json`, passes
`verify_batch`, and confirms the dbt scratch project survives the `model → analyze` boundary.

```bash
# throwaway spec: codex baseline-ish README + plugin_args.query_mode: batch + workspace_variant: spacedock
# benchmark.tasks: [crmarenapro]   (13 queries — exercises build-once + verify_batch)
rk run --explain specs/dab-gate0-probe.smoke.yaml          # $0 sanity
drivers/rk-run-detached.sh gate0-probe specs/dab-gate0-probe.smoke.frozen.yaml run
# watch runs/.rk-handles/gate0-probe-*/done
```

**STOP unless:** one dbt build serves all 13 queries, `verify_batch` runs, per-query rewards
appear. A 1-query/per-query probe is **insufficient** and does not count.
(Mongo is **not** on the critical path — only `agnews`/`yelp` touch it and both have a
relational backend; see design §5 Gate 0 item 3.)

---

## 4. Gate 1 — freeze the comparison anchor + author the variant

The variant is **not** a two-field diff against the old per-query `codex-dab-baseline` (that
spec is per-query). Build the proper anchor first.

1. **`specs/codex-dab-batch-baseline.yaml`** = current baseline README (no dbt) **+**
   `plugin_args: { query_mode: batch, workspace_variant: spacedock, hints: true, data_root: … }`.
   `rk freeze --allow-missing`; register the run later as **`@codex-batch-baseline`**.
2. Fork `solver_workflows/spacedock-readme-baseline` → `solver_workflows/dab00NN-dbt-pipeline`,
   edit its README to the mandatory dbt method (design §4: `model` builds `stg_* → int_*/mart`
   + tests, loops `dbt run; dbt test` until green; `analyze` = pure query; `verify` unchanged).
3. **`specs/dab00NN-dbt-pipeline.yaml`** = copy of `codex-dab-batch-baseline.yaml` changing
   **only** `experiment:` + `solver_workflow:`. `query_mode`/`workspace_variant` identical on
   both sides (they cancel). Make a `.smoke.yaml` too (adds `benchmark.tasks:` = the smoke set).
   `rk freeze --allow-missing` both.

**Invariant:** baseline and variant differ **only** in the README. The leak-guard prose in the
README stays intact (no external fetches); `rk audit --policy strict` is the backstop.

---

## 5. Gate 1.5 — measure the baseline + fix the canary set

```bash
drivers/rk-run-detached.sh codex-batch-baseline specs/codex-dab-batch-baseline.frozen.yaml run
rk registry add run baseline @codex-batch-baseline <run-dir>     # project-local registry
```

- **Canaries = the intersection:** queries that pass in **both** Opus incumbent (design §6
  table) **and** `@codex-batch-baseline`. Drop any Opus-passer that codex-batch already fails.
- **Separately record** any Opus-passer that `@codex-batch-baseline` itself regresses — that's
  a codex/batch finding, independent of dbt, to note before judging the variant.

---

## 6. Gate 2 — smoke (mix of reach + safety)

Smoke set = **targets** `crmarenapro` + `GITHUB_REPOS` **and** **canaries** (from the §5
intersection: start `bookreview` / `music_brainz_20k` / `stockindex` + one near-perfect, drop
any not passing in codex-batch).

```bash
drivers/rk-run-detached.sh dab00NN-smoke specs/dab00NN-dbt-pipeline.smoke.frozen.yaml matrix   # run+audit+score
rk runs diff "$(rk registry resolve run @codex-batch-baseline)" <variant-smoke-run-dir>   # overhead/regression
rk runs diff "$(rk registry resolve run @baseline)"             <variant-smoke-run-dir>   # Opus headline
```

**GO only if** (both): a failing-target query **flips** to pass (confirm by the committed
dbt-model artifact, not just reward) **AND zero** Opus ∩ `@codex-batch-baseline` passers
regress **anywhere in the smoke set** (per-query — targets included, not only canaries).
Produce a **per-query regression table**. Any single regression ⇒ NO-GO.

---

## 7. Full run + acceptance

```bash
drivers/rk-run-detached.sh dab00NN-full specs/dab00NN-dbt-pipeline.frozen.yaml matrix     # all 12 datasets
rk runs diff "$(rk registry resolve run @codex-batch-baseline)" <variant-full-run-dir>
rk runs diff "$(rk registry resolve run @baseline)"             <variant-full-run-dir>
```

**PASS requires BOTH:**
- **(a)** stratified Pass@1 over all 12 beats the Opus incumbent (clean `rk audit --policy strict`), and
- **(b)** **zero** Opus ∩ `@codex-batch-baseline` passers regress anywhere in the full 12 —
  shown by an explicit per-query regression table.

Aggregate Pass@1 beating Opus is **necessary but not sufficient**: a net-positive run that
silently trades away incumbent passers is a **FAIL**. If it passes both, promote
(`rk baseline promote` + `rk registry add run baseline`).

---

## 8. Invariants & fallback (do not violate)

- **Single lever:** only the README varies between `@codex-batch-baseline` and the variant.
  `query_mode: batch` + `workspace_variant: spacedock` are held-constant in **both** specs.
- **Image:** same rebuilt `dab-agent:latest` for baseline + variant (digest recorded for
  provenance; not enforced — accepted confound, design §7).
- **Failure contract:** dbt tests are a hard gate on the resolved models — green before
  `analyze`, else the query is `UNABLE TO DETERMINE`. No answer rides on a red test.
- **Overhead is the primary risk.** If regressions are **broad** across many datasets, the
  mandatory decision itself is falsified → fall back to gating (design §3/§7). A *single*
  regression blocks the run; *broad* regression falsifies the approach.

---

## 9. Deliverables back to the captain

1. Image digest (Step 0) + Gate 0 probe result (`feasibility.md`).
2. `@codex-batch-baseline` run-dir + the canary-intersection list (and any codex-batch-vs-Opus
   regressions).
3. Smoke + full run-dirs, both `rk runs diff` outputs, and the **per-query regression table**.
4. GO/NO-GO + PASS/FAIL calls with the behavioral read attributing the flip(s) to the README.
