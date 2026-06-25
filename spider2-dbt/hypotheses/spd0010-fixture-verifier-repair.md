---
id: spd0010
title: Fixture / verifier repair — build chinook gold from source, ship sap GL source tables, add a pre-flight gold-integrity gate
status: hypothesis
kind: hypothesis
source: resolution-survey-2026-06-25 ranked-backlog #5 — harness-side, runs in parallel with the solver hypotheses
started: 2026-06-25
completed:
verdict:
score: 0.6
worktree:
---

## Hypothesis

Two baseline FAILs are **fixture defects, not solver misses** — recoverable by a one-time
packaging/harness repair, NOT a solver README lever (the verifier itself stays untouched).

- **chinook001 (VERIFIER_FALSE_NEGATIVE):** the shipped gold `.duckdb` is byte-identical to the
  raw source — 0 of 3 `condition_tabs` were ever materialized, so the gold side of the compare
  raises a Catalog Error before any predicted column is read. The survey confirmed the comparator
  PASSES once gold is built from source. **Repair:** rebuild the gold project during packaging so
  the 3 target tables exist in gold.
- **sap001 (fixture defect):** the three GL fact source tables (`sap_faglflext` / `faglflexa` /
  `bkpf_data`) are omitted from the task-image source DB, so the targets are unbuildable from the
  shipped workspace. **Repair:** ship the omitted GL source tables in the packaged view.
- **zuora001 (fixture-incompleteness, re-routed from spd0006):** the project declares
  `fivetran/zuora_source` in `packages.yml` and refs its `stg_zuora__*` package staging models
  (e.g. `stg_zuora__payment_method`), but the `zuora_source` package is NOT vendored and is
  **unobtainable offline** (not in the Spider2 checkout, no dbt-hub network in the container).
  So the project cannot `dbt build` as shipped — the R1 build-as-is path is package-blocked.
  **Repair:** vendor the `zuora_source` package (+ its `fivetran_utils`/`dbt_utils` deps) into the
  zuora001 view at packaging time (same vendor-donor mechanism added for `dbt_utils`), OR confirm
  it is a true upstream fixture gap. Until then zuora001 is not solver-addressable.
- **Guard:** add a pre-flight **gold-integrity gate** (assert each `condition_tab` exists in gold
  + each declared source-id exists in the source `information_schema`) so future fixture defects
  surface as a packaging error instead of a silent solver FAIL.

This is NOT a solver-compliance experiment — there is nothing to smoke on the solver side. It is
a benchmark repair validated by re-running the full board and confirming chinook001/sap001 flip
with **0 change to any previously-passing gold** (the gold rebuild must be idempotent — only
build when `condition_tabs` are absent).

**Off-limits invariant:** the comparator / scorer (`tests/duckdb_match.py`, `eval_spec.py`,
`verify.py`) is NEVER edited. This repair is confined to the packager (`tools/`) and the gold
build, which produce the data the verifier reads — the verification logic is untouched.

## Pre-smoke Decision-Fork Probe

Offline-verified (survey wf_32b5a457-a96): chinook001 comparator returns True once gold is
materialized from source; sap001 targets are unbuildable until the GL tables ship. No solver
smoke applies.

## Acceptance criteria

**AC-1 (audit/integrity)** — the gold rebuild is idempotent: re-running the full board changes
0 previously-passing cells; chinook001/sap001 flip FAIL→PASS. The verifier/scorer files are
byte-identical (only `tools/` + packaged views change).
**AC-2** — every score paired with a clean strict audit; the new gold-integrity gate passes on
all 61 views.
**AC-3** — board delta is exactly +2 (chinook001 + sap001), no collateral movement.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
