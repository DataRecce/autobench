# spider2-dbt — Flake Candidate Ledger

Per-task pass history across our runs. The **full-board rate** (passes across the 4 apples-to-apples
61-cell draws: `baseline@1`, `spd0004-full`, `spd0007-full-v1`, `spd0007-full-v2`) is the authoritative
reliability metric. Smokes inform but use different subsets / sometimes rejected levers.

**Goal:** after the flip program banks new passers, harden the FLAKE candidates to consistent PASS.
**Maintenance:** append each new full run as a full-board draw; 4/4 → ROCK, partial → FLAKE.

## Summary
- **25** passed ≥1; **36** never passed.
- **13** ROCK-SOLID (4/4 full boards). The rest are FLAKE candidates (hardening backlog).
- KEY: 4 full draws now show the board swings hard on variance (baseline 19, spd0004 21, spd0007-v1 20, spd0007-v2 16) — single draws don't decide.

## 🎯 Flake candidates (passed but NOT 4/4 full-board) — hardening backlog

| task | passes/attempts | full-board | class |
|---|---|---|---|
| jira001 | 1/11 | 0/4 | SMOKE-FLICKER |
| salesforce001 | 3/9 | 0/4 | SMOKE-FLICKER |
| f1003 | 1/4 | 1/3 | FLAKE |
| hubspot001 | 2/5 | 2/4 | FLAKE |
| f1001 | 7/13 | 2/4 | FLAKE |
| quickbooks003 | 4/7 | 2/4 | FLAKE |
| marketo001 | 7/9 | 2/4 | FLAKE |
| retail001 | 6/10 | 3/4 | FLAKE |
| maturity001 | 3/4 | 3/4 | FLAKE |
| greenhouse001 | 3/4 | 3/4 | FLAKE |
| tpch002 | 4/5 | 3/4 | FLAKE |
| mrr002 | 4/5 | 3/4 | FLAKE |

## ✅ Rock-solid (4/4 full-board)

activity001, app_reporting001, app_reporting002, google_play001, google_play002, lever001, mrr001, playbook001, qualtrics001, quickbooks002, tickit001, workday001, workday002

## ❌ Never passed (36) — flip backlog

airbnb001, airport001, analytics_engineering001, apple_store001, asana001, asset001, atp_tour001, chinook001, divvy001, f1002, flicks001, hive001, intercom001, movie_recomm001, nba001, netflix001, pendo001, playbook002, provider001, quickbooks001, recharge001, recharge002, reddit001, sap001, scd001, shopify_holistic_reporting001, social_media001, superstore001, synthea001, tickit002, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001

## Per-draw reward matrix — full boards (✅/❌/·)

| task | baseline@1 | spd0004-full | spd0007-full-v1 | spd0007-full-v2 |
|---|---|---|---|---|
| activity001 | ✅ | ✅ | ✅ | ✅ |
| app_reporting001 | ✅ | ✅ | ✅ | ✅ |
| app_reporting002 | ✅ | ✅ | ✅ | ✅ |
| f1001 | ✅ | ❌ | ❌ | ✅ |
| f1003 | ❌ | · | ✅ | ❌ |
| google_play001 | ✅ | ✅ | ✅ | ✅ |
| google_play002 | ✅ | ✅ | ✅ | ✅ |
| greenhouse001 | ✅ | ✅ | ✅ | ❌ |
| hubspot001 | ✅ | ✅ | ❌ | ❌ |
| jira001 | ❌ | ❌ | ❌ | ❌ |
| lever001 | ✅ | ✅ | ✅ | ✅ |
| marketo001 | ❌ | ✅ | ✅ | ❌ |
| maturity001 | ✅ | ✅ | ✅ | ❌ |
| mrr001 | ✅ | ✅ | ✅ | ✅ |
| mrr002 | ✅ | ✅ | ❌ | ✅ |
| playbook001 | ✅ | ✅ | ✅ | ✅ |
| qualtrics001 | ✅ | ✅ | ✅ | ✅ |
| quickbooks002 | ✅ | ✅ | ✅ | ✅ |
| quickbooks003 | ❌ | ✅ | ✅ | ❌ |
| retail001 | ❌ | ✅ | ✅ | ✅ |
| salesforce001 | ❌ | ❌ | ❌ | ❌ |
| tickit001 | ✅ | ✅ | ✅ | ✅ |
| tpch002 | ✅ | ✅ | ✅ | ❌ |
| workday001 | ✅ | ✅ | ✅ | ✅ |
| workday002 | ✅ | ✅ | ✅ | ✅ |

_Updated 2026-06-25 with spd0007-full-v2 (guarded). 4 full-board draws + 13 smokes._
