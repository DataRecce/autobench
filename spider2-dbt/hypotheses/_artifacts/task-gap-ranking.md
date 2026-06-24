# spider2-dbt task-gap ranking

Which tasks have the most headroom — currently-FAIL tasks whose failure mode looks
README-addressable rank highest for targeting. **Re-derived from the spd0001 anchor run's
`per_trial_outcomes.json`** (`runs/spider2-dbt-full-baseline/13fb630e2cae3eb8`, 19/61 = 0.3115,
clean strict audit). This is the live board.

## Board shape

- **61 duckdb-runnable tasks** = 68 declared − 4 goldless (airbnb002 / biketheft001 / gitcoin001 /
  google_ads001) − 3 postgres-backed (inzight001 / shopify001 / shopify002). Goldless + postgres tasks
  are **non-signal**; never targets, never canaries.
- Metric = flat pass rate (`stratified_pass_at_1`, single `default` stratum). One passer = 1/61 ≈ 0.016.
- Anchor result: **19 PASS / 42 FAIL**, 0 errored, 0 coverage_missing, 0 tainted.

## Failure-bucket counts (42 fails)

| Bucket | Count | What it is | README-addressable? |
|---|---|---|---|
| wrong-columns-or-grain | **38** | correct table NAME, materialized as BASE TABLE, wrong analytic content (column derivation / filter / grain / metric definition diverges from gold) | hard — the oracle-blind wall; no per-cell ground truth for the agent to check against |
| wrong-table-name | **3** | agent built a differently-named table, or built only some of N required gold tables | maybe — completeness/naming discipline lever |
| ephemeral-not-materialized | **0** | (the output-contract README already lands BASE-TABLE materialization board-wide) | n/a — solved by the seed README |
| correct-artifact-still-fail | **0** | — | n/a |
| packaging-fault (non-signal) | **1** | chinook001: gold DB ships only raw sources, never the dim/fct/obt gold tables → verifier gold-fetch raises a Catalog Error → cannot pass regardless of agent output | NO — exclude; benchmark-packaging defect, not content |

> **Revision vs the 6-task smoke:** the smoke labelled chinook001 `ephemeral-not-materialized`. The
> full-board artifact read overturns that: the agent DID build `dim_customer`/`fct_invoice`/`obt_invoice`
> as BASE TABLEs; the failure is gold-side (the gold `chinook.duckdb` lacks those tables). chinook001 is
> a **packaging-fault (non-signal)**, not an ephemeral case, and there is **no** ephemeral bucket on the
> full board. spd0002 (materialization lever) has **no live target** — that family is empty.

## Sentinels (currently-PASS — protect as canaries)

activity001, app_reporting001, app_reporting002, f1001, google_play001, google_play002, greenhouse001,
hubspot001, lever001, maturity001, mrr001, mrr002, playbook001, qualtrics001, quickbooks002, tickit001,
tpch002, workday001, workday002 (19 passers).

## wrong-table-name bucket (3 — highest near-term headroom)

| Task | Gold tables required | What the agent built | Gap |
|---|---|---|---|
| movie_recomm001 | `user_watched_movies` | `original_programs` | built a table matching the instruction's surface description, wrong gold name/scope |
| intercom001 | `intercom__company_metrics`, `intercom__admin_metrics` | only `intercom__admin_metrics` | missed the 2nd required gold table |
| analytics_engineerin (analytics_engineering001) | `fact_purchase_order`, `obt_customer_reporting` | only `obt_customer_reporting` | missed the 2nd required gold table |

Two of three are **multi-table-target misses** — the agent stops after building one named output when the
gold demands two. A "build EVERY required output table" completeness lever could address intercom001 +
analytics_engineerin (the gold-table list is not visible to the agent, so the lever must work from the
instruction's enumeration of deliverables).

## wrong-columns-or-grain bucket (38 — the dominant wall)

airbnb001, airport001, apple_store001, asana001, asset001, atp_tour001, divvy001, f1002, f1003,
flicks001, hive001, jira001, marketo001, nba001, netflix001, pendo001, playbook002, provider001,
quickbooks001, quickbooks003, recharge001, recharge002, reddit001, retail001, salesforce001, sap001,
scd001, shopify_holistic_rep, social_media001, superstore001, synthea001, tickit002, tpch001, twilio001,
xero001, xero_new001, xero_new002, zuora001.

Every one builds the correctly-named gold table(s) as a BASE TABLE and self-validates green, but the
*values* diverge from the unstated gold semantics (which rows to include, how to derive a metric, what
grain to aggregate to, date/null/tiebreak conventions). This is the **oracle-blind wall** — the agent
has no gold to check against and produces a defensible-but-different interpretation. README levers here
must supply *semantic* disambiguation the instruction leaves implicit, and (per ade-bench/DAB priors)
generative "pin the semantics" rules tend to be inert on the real ambiguity. Size any value-level lever
family against this 38-cell bucket but expect most cells to be irreducible without per-task ground truth.

## Concept ideation order

1. **Completeness / multi-table-target lever** (spd0002 re-scoped): smallest, highest-confidence —
   targets intercom001 + analytics_engineerin (build every deliverable the instruction enumerates).
   movie_recomm001 is a naming/scope miss, possibly same family.
2. **Value-level semantic forks** (spd0003): sized against the 38-cell grain bucket; expect a low
   hit-rate and pick cells where the instruction under-specifies a *nameable* convention.
3. The materialization lever family (old spd0002) is **empty** — no ephemeral target exists; do not file it.
