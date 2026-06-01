# ADE-Bench Harbor Datasets

Source:

```text
dbt-labs/ade-bench@sha256:2c1f9e6966d01b0a5de2235d1a0b64089c7eead42c85c3b7b61d0929405c2bd5
```

Harbor Hub:

```text
https://hub.harborframework.com/datasets/dbt-labs/ade-bench/latest
```

These are the Harbor task package names returned by Razorback for the pinned
ADE-Bench dataset. Use these names in Razorback `benchmark.tasks` when
`benchmark.kind: harbor` points at the pinned Harbor dataset ref.

## Airbnb

| Dataset | Difficulty | Description |
| --- | --- | --- |
| `ade-bench-airbnb001` | easy | Fix a dbt-utils surrogate key macro deprecation warning in `monthly_agg_reviews`. |
| `ade-bench-airbnb002` | medium | Preserve old surrogate-key null behavior while fixing the same dbt-utils migration issue. |
| `ade-bench-airbnb003` | easy | Refactor source models so they materialize as views. |
| `ade-bench-airbnb004` | medium | Add `review_id` as a primary key to `fct_reviews` and update the model. |
| `ade-bench-airbnb005` | medium | Build daily and monthly NPS review aggregate models from review sentiment. |
| `ade-bench-airbnb006` | medium | Rename CTEs across models to match expected naming conventions. |
| `ade-bench-airbnb007` | hard | Create all models described by the project schema file. |
| `ade-bench-airbnb008` | easy | Repair a broken dbt project configuration. |
| `ade-bench-airbnb009` | medium | Diagnose and fix missing dates in `mom_agg_reviews`. |

## Analytics Engineering

| Dataset | Difficulty | Description |
| --- | --- | --- |
| `ade-bench-ana-eng001` | easy | Diagnostic no-op task: inspect the dbt project and avoid unnecessary changes. |
| `ade-bench-ana-eng002` | easy | Fix a syntax error in `obt_product_inventory.sql`. |
| `ade-bench-ana-eng002-medium` | medium | Diagnose and repair a broken dbt project. |
| `ade-bench-ana-eng003` | easy | Create `dim_customer` with renamed `customer_id` and uniqueness expectations. |
| `ade-bench-ana-eng004` | medium | Create `obt_product_inventory` by joining inventory with product details. |
| `ade-bench-ana-eng005` | easy | Fix `fact_inventory` so it has one row per `inventory_id`. |
| `ade-bench-ana-eng006` | hard | Create `dim_products`, `fact_inventory`, and `obt_product_inventory`. |
| `ade-bench-ana-eng007` | medium | Update models after product IDs change from numeric to string. |
| `ade-bench-ana-eng007-medium` | medium | Diagnose and repair a project broken by product ID changes. |
| `ade-bench-ana-eng008` | easy | Create a new dbt project for the analytics engineering DuckDB database. |

## Asana

| Dataset | Difficulty | Description |
| --- | --- | --- |
| `ade-bench-asana001` | medium | Fix breakage caused by a Fivetran Asana package update without changing source data. |
| `ade-bench-asana002` | medium | Adapt local data to match the updated Fivetran Asana package expectations. |
| `ade-bench-asana003` | hard | Refactor package internals by replacing temporary Asana models with staging-source dependencies. |
| `ade-bench-asana004` | medium | Refactor `asana__project` calculations into a new intermediate model. |
| `ade-bench-asana005` | medium | Refactor `asana__project` while handling changed data behavior. |
| `ade-bench-asana005-hard` | hard | Harder variant of the `asana__project` refactor under changed data conditions. |

## F1

| Dataset | Difficulty | Description |
| --- | --- | --- |
| `ade-bench-f1001` | medium | Add source models and update staging models to point to them. |
| `ade-bench-f1002` | hard | Create four stats models defined by project YAML configuration. |
| `ade-bench-f1003` | medium | Fix top-N list models whose rankings are wrong. |
| `ade-bench-f1003-hard` | hard | Harder top-N ranking repair across multiple F1 models. |
| `ade-bench-f1004` | medium | Fix zero-valued columns in `finishes_by_driver`. |
| `ade-bench-f1005` | medium | Diagnose and repair inflated constructor points. |
| `ade-bench-f1005-medium` | medium | Repair incorrect constructor point results. |
| `ade-bench-f1006` | hard | Fix inflated points in both constructor and driver point models. |
| `ade-bench-f1006-hard` | hard | Harder repair for incorrect constructor and driver point results. |
| `ade-bench-f1007` | medium | Fix staging results missing many rows. |
| `ade-bench-f1007-hard` | hard | Diagnose broad stat-model value drift and repair affected tables. |
| `ade-bench-f1007-medium` | medium | Fix an empty `driver_wins_by_season` table. |
| `ade-bench-f1009` | medium | Create a model calculating current driver ages. |
| `ade-bench-f1010` | medium | Create lap-time analysis to study whether drivers got faster over time. |
| `ade-bench-f1010-medium` | medium | Medium variant of the lap-time trend analysis task. |
| `ade-bench-f1011` | medium | Repair or improve an existing driver speed trend analysis model. |

## Intercom

| Dataset | Difficulty | Description |
| --- | --- | --- |
| `ade-bench-intercom001` | medium | Create `intercom__threads` by aggregating conversation parts by conversation. |
| `ade-bench-intercom002` | hard | Create thread and conversation metric models from Intercom conversation parts. |
| `ade-bench-intercom003` | hard | Create `intercom__conversation_metrics` with conversation-level aggregates. |

## QuickBooks

| Dataset | Difficulty | Description |
| --- | --- | --- |
| `ade-bench-quickbooks001` | easy | Fix a broken QuickBooks dbt project and update the tables. |
| `ade-bench-quickbooks002` | medium | Remove department usage from billing models while preserving package compatibility. |
| `ade-bench-quickbooks003` | hard | Harder department-removal task across QuickBooks package and model references. |
| `ade-bench-quickbooks004` | medium | Remove confusing exchange-rate converted amount/payment columns. |
