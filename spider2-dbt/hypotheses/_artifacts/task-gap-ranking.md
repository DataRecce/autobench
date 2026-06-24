# spider2-dbt task-gap ranking

Which tasks have the most headroom — currently-FAIL tasks whose failure mode looks
README-addressable rank highest for targeting. **Re-derive this table from the `@baseline`
champion's `per_trial_outcomes.json`** once spd0001 establishes the full board (it does not exist yet —
only the 6-task smoke is scored).

## Board shape

- **61 duckdb-runnable tasks** = 68 declared − 4 goldless (airbnb002 / biketheft001 / gitcoin001 /
  google_ads001) − 3 postgres-backed (inzight001 / shopify001 / shopify002). Goldless + postgres tasks
  are **non-signal**; never targets, never canaries.
- Metric = flat pass rate (`stratified_pass_at_1`, single `default` stratum). One passer = 1/61 ≈ 0.016.

## Known cells (from the 6-task output-contract smoke — NOT the full board)

| Task | Smoke verdict | Failure class | README-addressable? |
|---|---|---|---|
| activity001 | ✅ PASS | — | sentinel (passer) |
| f1001 | ✅ PASS | — (after packager schema-align fix) | sentinel (passer) |
| chinook001 | ❌ FAIL | ephemeral-not-materialized | YES → spd0002 |
| jira001 | ❌ FAIL | wrong-columns/values | hard core → spd0003 |
| tpch001 | ❌ FAIL | wrong-columns/values | hard core → spd0003 |
| xero_new001 | ❌ FAIL | wrong-columns/values | hard core → spd0003 |

The other 55 tasks are **un-scored** — the spd0001 anchor run produces their verdicts and failure
classes. Bucket each fail as: `wrong-table-name` / `ephemeral-not-materialized` / `wrong-columns-or-grain`
/ `correct-artifact-still-fail` / `packaging-fault` (non-signal). The size of each bucket bounds the
headroom of the corresponding lever family.

## Concept ideation order

Until the full board exists, ideate in this order: (1) spd0002 materialization (highest-confidence,
one known target + likely siblings), then (2) spd0003 value-level forks sized against the anchor's
hard-core bucket count.
