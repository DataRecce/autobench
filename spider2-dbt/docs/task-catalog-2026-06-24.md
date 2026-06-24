# spider2-dbt 68-task catalog — 2026-06-24

Source: Spider2 `examples/spider2-dbt.jsonl` + gold `spider2_eval.jsonl`, cross-referenced with the merged 2026-06-24 full baseline and `failure-analysis-2026-06-24.md`.

Summary: 68 declared tasks = 61 DuckDB-runnable board tasks + 7 excluded tasks. Merged baseline: 19 PASS / 42 FAIL / 0 exceptions on the 61-task board. The 7 excluded tasks are 4 without usable local gold in the board and 3 Postgres-backed tasks.

| task | family | eval targets | baseline/catalog | focus |
|---|---|---|---|---|
| `playbook001` | `playbook` | `attribution_touches` | PASS | regression canary |
| `provider001` | `provider` | `specialty_mapping, provider` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `asana001` | `asana` | `asana__team, asana__user` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `shopify001` | `shopify` | `shopify__products, shopify__daily_shop` | EXCLUDED: Postgres-backed | infra/data scope, not solver board |
| `asset001` | `asset` | `bar_quotes, book_value` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `flicks001` | `flicks` | `actor_rating_by_total_movie, movie_actor_by_year` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `analytics_engineering001` | `analytics_engineering` | `fact_purchase_order, obt_customer_reporting` | FAIL: MATERIALIZATION | build every condition_tab as materialized table |
| `xero_new001` | `xero_new` | `xero__general_ledger, xero__balance_sheet_report, xero__profit_and_loss_report` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `chinook001` | `chinook` | `dim_customer, fct_invoice, obt_invoice` | FAIL: MATERIALIZATION | build every condition_tab as materialized table |
| `f1001` | `f` | `finishes_by_driver, most_fastest_laps, most_podiums, most_pole_positions` | PASS | regression canary |
| `netflix001` | `netflix` | `stg_google_sheets__originals_unioned` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `workday002` | `workday` | `workday__job_overview` | PASS | regression canary |
| `pendo001` | `pendo` | `pendo__guide_daily_metrics, pendo__page_daily_metrics` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `synthea001` | `synthea` | `cost` | FAIL: GRAIN over-emit | avoid fabricated fan-out/orphans; scope snapshot correctly |
| `inzight001` | `inzight` | `mrt_capacity_tariff` | EXCLUDED: Postgres-backed | infra/data scope, not solver board |
| `google_play001` | `google_play` | `google_play__country_report, google_play__device_report` | PASS | regression canary |
| `airbnb002` | `airbnb` | `src_hosts, wow_agg_reviews` | EXCLUDED: no usable local gold | infra/data scope, not solver board |
| `biketheft001` | `biketheft` | `fact_theft_reports` | EXCLUDED: no usable local gold | infra/data scope, not solver board |
| `tickit002` | `tickit` | `dim_events, fct_listings` | FAIL: GRAIN over-emit | avoid fabricated fan-out/orphans; scope snapshot correctly |
| `activity001` | `activity` | `dataset__aggregate_after_1, dataset__aggregate_all_ever_1` | PASS | regression canary |
| `scd001` | `scd` | `fct_jafflegaggle, rpt_corporate_accounts` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `lever001` | `lever` | `lever__posting_enhanced` | PASS | regression canary |
| `greenhouse001` | `greenhouse` | `greenhouse__application_enhanced, greenhouse__job_enhanced` | PASS | regression canary |
| `app_reporting002` | `app_reporting` | `int_apple_store__overview, int_google_play__overview, app_reporting__overview_report` | PASS | regression canary |
| `mrr001` | `mrr` | `mrr` | PASS | regression canary |
| `xero001` | `xero` | `xero__balance_sheet_report` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `movie_recomm001` | `movie_recomm` | `user_watched_movies` | FAIL: MATERIALIZATION | build every condition_tab as materialized table |
| `quickbooks003` | `quickbooks` | `quickbooks__balance_sheet, quickbooks__general_ledger_by_period` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `qualtrics001` | `qualtrics` | `qualtrics__directory` | PASS | regression canary |
| `recharge002` | `recharge` | `recharge__customer_daily_rollup` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `atp_tour001` | `atp_tour` | `dim_player, dim_tournament, rpt_match_summary` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `quickbooks002` | `quickbooks` | `quickbooks__ap_ar_enhanced` | PASS | regression canary |
| `google_ads001` | `google_ads` | `google_ads__campaign_report, google_ads__keyword_report` | EXCLUDED: no usable local gold | infra/data scope, not solver board |
| `airport001` | `airport` | `fct_arrivals__malaysia_summary, fct_airports__malaysia_distances_km` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `tpch001` | `tpch` | `client_purchase_status` | FAIL: GRAIN over-emit | avoid fabricated fan-out/orphans; scope snapshot correctly |
| `salesforce001` | `salesforce` | `salesforce__daily_activity` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `hubspot001` | `hubspot` | `hubspot__contacts, hubspot__email_campaigns` | PASS | regression canary |
| `shopify002` | `shopify` | `shopify__discounts` | EXCLUDED: Postgres-backed | infra/data scope, not solver board |
| `social_media001` | `social_media` | `social_media_reporting__instagram_posts_reporting, social_media_reporting__twitter_posts_reporting, social_media_reporting__rollup_report` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `xero_new002` | `xero_new` | `xero__balance_sheet_report` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `divvy001` | `divvy` | `stg_divvy_data, facts_divvy` | FAIL: UNCLEAR / verifier audit | capture predicted DB and diff verifier |
| `playbook002` | `playbook` | `attribution_touches, cpa_and_roas` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `apple_store001` | `apple_store` | `apple_store__source_type_report, apple_store__territory_report` | FAIL: GRAIN over-emit | avoid fabricated fan-out/orphans; scope snapshot correctly |
| `jira001` | `jira` | `jira__project_enhanced` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `zuora001` | `zuora` | `zuora__account_daily_overview, zuora__account_overview` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `superstore001` | `superstore` | `dim_regional_managers, fct_sales` | FAIL: MISSING_COLUMN | match exact columns/star-schema/count grain |
| `marketo001` | `marketo` | `marketo__email_templates` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `f1002` | `f` | `finishes_by_constructor, driver_championships, construtor_drivers_championships` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `gitcoin001` | `gitcoin` | `allo_projects, allo_applications` | EXCLUDED: no usable local gold | infra/data scope, not solver board |
| `shopify_holistic_reporting001` | `shopify_holistic_reporting` | `shopify_holistic_reporting__daily_customer_metrics` | FAIL: GRAIN not-addressable | lower priority / task-specific |
| `hive001` | `hive` | `stg_covid__cases, covid_cases` | FAIL: GRAIN under-emit | preserve full entity/date spine; left join facts |
| `workday001` | `workday` | `workday__organization_overview` | PASS | regression canary |
| `f1003` | `f` | `stg_f1_dataset__drivers, driver_podiums_by_season, driver_fastest_laps_by_season, constructor_retirements_by_season` | FAIL: GRAIN over-emit | avoid fabricated fan-out/orphans; scope snapshot correctly |
| `retail001` | `retail` | `report_customer_invoices` | FAIL: MISSING_COLUMN | match exact columns/star-schema/count grain |
| `google_play002` | `google_play` | `google_play__overview_report` | PASS | regression canary |
| `sap001` | `sap` | `sap__0fi_gl_10, sap__0fi_gl_14` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `airbnb001` | `airbnb` | `dim_listings_hosts, mom_agg_reviews` | FAIL: GRAIN over-emit | avoid fabricated fan-out/orphans; scope snapshot correctly |
| `app_reporting001` | `app_reporting` | `app_reporting__app_version_report, app_reporting__os_version_report` | PASS | regression canary |
| `mrr002` | `mrr` | `mrr` | PASS | regression canary |
| `twilio001` | `twilio` | `twilio__account_overview, twilio__number_overview` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `intercom001` | `intercom` | `intercom__company_metrics, intercom__admin_metrics` | FAIL: MATERIALIZATION | build every condition_tab as materialized table |
| `tickit001` | `tickit` | `fct_sales` | PASS | regression canary |
| `reddit001` | `reddit` | `prod_posts_ghosts, prod_comments_ghosts` | FAIL: MISSING_COLUMN | match exact columns/star-schema/count grain |
| `recharge001` | `recharge` | `recharge__charge_line_item_history` | FAIL: MISSING_COLUMN | match exact columns/star-schema/count grain |
| `maturity001` | `maturity` | `dim_doctors, dim_patients` | PASS | regression canary |
| `tpch002` | `tpch` | `EUR_LOWCOST_BRASS_SUPPLIERS, UK_Lowcost_Brass_Suppliers` | PASS | regression canary |
| `nba001` | `nba` | `reg_season_summary, season_summary` | FAIL: VALUE_DEF | oracle/value semantics; lower README leverage |
| `quickbooks001` | `quickbooks` | `quickbooks__general_ledger` | FAIL: UNCLASSIFIED_IN_ANALYSIS | needs per-task failure analysis |
