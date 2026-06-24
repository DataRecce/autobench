# spider2-dbt failure analysis — 42 failed baseline tasks — 2026-06-24

Per-task classification of every failure in the `@baseline` run
(`runs/spider2-dbt-full-baseline/13fb630e2cae3eb8`, 19/61). Method: one read-only
analysis agent per task (dynamic workflow `spider2-failure-analysis`), each
comparing the gold answer DB shape against what the solver's transcript shows it
built. Predicted DBs are not persisted, so classifications are evidence-based
inference (except tpch001, captured).

## Category breakdown (42)

| category | count | addressable | note |
|---|---|---|---|
| **GRAIN** | 22 | 20 | wrong row set — under-emit 15, over-emit 7 |
| **VALUE_DEF** | 11 | 3 | right shape, wrong values — the oracle wall |
| **MATERIALIZATION** | 4 | 4 | missing/ephemeral/incomplete target tables |
| **MISSING_COLUMN** | 4 | 4 | wrong/absent compared column (FK vs attr, count-grain) |
| **UNCLEAR** | 1 | — | divvy001 — likely verifier false-negative (see below) |
| **Addressable total** | | **31/42** | |

## GRAIN (22) — the dominant, mostly-addressable failure

The recurring mistake: the solver **inner-joins / dedups / uses activity-only rows**
when gold wants full coverage. Direction matters:

- **under-emitted (15):** asset001, flicks001, hive001, jira001, marketo001,
  netflix001, pendo001, playbook002, provider001, recharge002, salesforce001,
  xero001, xero_new001, xero_new002, zuora001. Mechanisms: inner-joined away
  entities (jira projects w/o issues, playbook unpaid sources, marketo zero-event
  templates), no continuous **date spine** (pendo/salesforce/recharge002 daily
  models, xero balance-sheet 60-month spine), over-dedup of pass-through unions
  (netflix `*_unioned`), or collapsed to the wrong period grain.
- **over-emitted (7):** airbnb001 (daily fan-out vs MoM snapshot), apple_store001
  (broadened the Fivetran package join), asset001-mirror, f1003, synthea001
  (fabricated a domain the prose named), tickit002 (kept orphan listings),
  tpch001 (kept zero-activity customers, 150k vs 75k).

**Critical:** the current `spider2-dbt-baseline` README explicitly says *"build FROM
the fact and INNER JOIN the dimension; do NOT LEFT JOIN the full dimension and
zero-fill."* That rule **directly causes the 15 under-emit failures** — yet tpch001
(over-emit) genuinely wanted the filter. So grain is **task-dependent**; a blanket
rule is wrong in both directions. (2 GRAIN cases judged NOT addressable:
shopify_holistic_reporting001, zuora001.)

## MATERIALIZATION (4) — all addressable
chinook001, analytics_engineering001, intercom001, movie_recomm001: a target named
in the eval `condition_tabs` was never built as a base table (ephemeral under
`intermediate/`, dismissed as "out of scope", or built under the wrong name). The
solver scoped "the deliverable" to one table and ignored the others.

## MISSING_COLUMN (4) — all addressable
- superstore001: built a denormalized wide fact (attrs inline) instead of a star
  schema with `dim_*_id` FK columns; surrogate-key offset wrong (101 vs 1001).
- retail001: "number of invoices" = COUNT lines (354321) not COUNT DISTINCT (16646).
- recharge001: carried wrong native label into `title`.
- reddit001: ghost/dedup handling off by a few rows.

## VALUE_DEF (11) — mostly the oracle wall (3 teachable)
airport001 (non-standard km formula), asana001 (package string-agg ordering),
atp_tour001 (external country enrichment), f1002 (status bucketing), nba001
(frozen Monte-Carlo seed), sap001, scd001, twilio001 (signed-vs-abs spend) —
not blind-fixable. Teachable sub-traps (addressable=Y): quickbooks003 (balance
roll-forward), retail001-style count-grain, social_media001 (reproduce package
column defs incl. NULL-resolving columns).

## UNCLEAR (1) — divvy001 = likely VERIFIER FALSE-NEGATIVE
The analysis agent replayed the solver's exact committed SQL inside the gold DB and
got **0 set-difference** on both compared tables (stg 426887, facts 413689) across
every compared column, with the surrogate keys byte-identical — yet the verifier
returned a bare binary "mismatch". The predicted DB isn't persisted and the verifier
emits no per-column diagnostic. This may be a real verifier/harness bug; if so, an
unknown number of the "VALUE_DEF exact-shape" fails could be false-negatives too.
ACTION: re-run divvy001 with predicted-DB capture and diff vs gold to confirm.

## Improvement plan (ranked by leverage)

1. **Conditioned grain rule (README v3) — biggest win (~15-20 GRAIN).** Replace the
   blanket inner-join rule with a CLASSIFIER: if the instruction/target implies
   completeness ("daily", "every <X>", a `*_spine`/dimension rollup, a balance
   carried forward), preserve the full entity set / continuous date spine and
   LEFT-join facts (zero/NULL on no-activity); only scope-to-active when the
   instruction explicitly says "only those with activity" or it's a per-entity
   lifetime-value rollup. Add: `*_unioned` staging = pass-through UNION ALL, never
   dedup. CAVEAT: the solver cannot self-verify grain (self-anchored false-green),
   and grain levers historically add ±variance — expect a meaningful fraction, not
   all 15, to flip.
2. **Multi-target materialization (4 MAT).** Enumerate ALL `condition_tabs` targets;
   build each as its own base table (`config(materialized='table')`); never treat a
   referenced target as out-of-scope. (Sharper than the inert v2 attempt.)
3. **Star-schema / package faithfulness (4 MISSING_COLUMN + ~3 VALUE_DEF).** Marts
   are star schemas: facts carry dimension FK surrogate ids, not denormalized attrs.
   For Fivetran-package tasks, replicate the package's exact column definitions
   (incl. columns that resolve to NULL). Count-grain trap: confirm what a "count"
   counts (lines vs distinct) against the source.
4. **Verifier false-negative audit (divvy001 first).** Capture + diff; if confirmed,
   recover possibly-free points and fix/flag the comparator.

## Calibrated expectation
31/42 are addressable in principle, but grain is double-edged and oracle-blind, so
not all flip. A v3 README (conditioned grain + multi-target + star-schema) is a
plausible path from 19/61 (31%) toward the high-20s/low-30s out of 61; the ~8 pure
VALUE_DEF oracle-wall cases are the floor. Validate on a targeted smoke of the
under-emit GRAIN + MAT tasks before a full re-run (smoke is not full-board
predictive — see DAB calibration lessons).
