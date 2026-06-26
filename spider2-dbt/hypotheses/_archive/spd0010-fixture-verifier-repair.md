---
id: spd0010
title: Fixture / verifier repair — build chinook gold from source, ship sap GL source tables, add a pre-flight gold-integrity gate
status: conclude
kind: hypothesis
source: resolution-survey-2026-06-25 ranked-backlog #5 — harness-side, runs in parallel with the solver hypotheses
started: 2026-06-25
completed: 2026-06-26T05:22:00Z
verdict: PASSED
score: 0.6
worktree:
archived: 2026-06-26T05:22:00Z
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



## Behavioral analysis

## Failure Review

## Smoke result

Targeted smoke `runs/spider2-dbt-spd0010-smoke/cd01f071ca825c30` (rc=0, audit strict CLEAN; solver
UNCHANGED = champion spd0008). **sap001 FLIPPED FAIL→PASS**, chinook001 stayed FAIL (expected),
activity001 canary held. No full run (per captain).

## Verdict

**PASSED (infra fixture repair) — split outcome:**
- **sap001 = FIXED + VERIFIED (+1 recoverable).** The upstream `examples/sap001` source duckdb
  omitted 4 GL RAW source tables (`sap_bkpf_data`/`faglflexa`/`faglflext`/`lfa1`) that the
  eval-suite gold db ships, so `sap__0fi_gl_10/14` were unbuildable (the original survey
  "fixture defect"). Restored them (raw sources, NOT answers — faithful) into the solver source db;
  the champion solver then built the GL targets to gold → reward 1.0. Made DURABLE in the packager
  (`_restore_missing_sources`, curated `_MISSING_SOURCE_RESTORE['sap001']`) so re-packaging
  reproduces it; verified idempotent + no-op for other tasks.
- **chinook001 = NOT faithfully fixable (upstream goldless-equivalent defect).** The gold db ships
  NO answer tables (dim_customer/fct_invoice/obt_invoice), the example ships NO mart models for them
  (`models/obt/` has only `obt_invoice.yml`, no SQL), and grep finds NO reference definition
  anywhere in Spider2. "Building gold from source" would mean fabricating gold from a solver's
  output — off-limits (would corrupt grading). The survey's "comparator passes once gold built"
  was tautological. → recommend EXCLUDING chinook001 from the gradeable denominator (like the 4
  goldless tasks: 61→60), NOT fabricating gold.

**Board impact:** the current @baseline run (spd0008 24/61) predates the fix, so its recorded score
is unchanged (no full re-run per captain). The sap001 repair is BANKED into the benchmark (packager
+ views) — every future full run forking the champion now has sap001 buildable+passable, so the
effective ceiling rises by +1. With chinook001 excluded, the gradeable board is 60 (sap001 now a
live passer).

## Follow-up Routing

`stop` (sap fixed + durable) + 2 captain decisions surfaced: (1) EXCLUDE chinook001 from the
gradeable denominator (61→60) — it is upstream-goldless; (2) optional: add a packaging-time
GOLD-INTEGRITY GATE (assert each `condition_tab` exists in the gold db + each declared source-id
exists in the source db) to catch this class (chinook-type missing-gold, sap-type missing-source)
as a packaging error instead of a silent FAIL — recommended but deferred (larger preflight change).
The `lowercase_columns` synthea macro gap (noted in spd0007 analyze) is a similar fixture item, also
deferred here.
