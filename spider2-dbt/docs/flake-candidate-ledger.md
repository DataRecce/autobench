# spider2-dbt — Flake Candidate Ledger

Full-board rate across the 6 apples-to-apples 61-cell draws is authoritative:
`baseline(19)`, `spd0004(21)`, `spd0007v1(20)`, `spd0007v2(16)`, `spd0007b(24)`, **`spd0008(24)★`** (★=@baseline).

**Goal:** harden FLAKE candidates to consistent PASS. **Maintenance:** append each full run as a column; 6/6→ROCK.

## Summary
- **@baseline = spd0008 @ 24/61 = 0.3934.** Full-board draws: 19 / 21 / 20 / 16 / 24 / 24 (±range ~16-24 = the variance wall).
- spd0008's 24 passers: ['activity001', 'app_reporting001', 'app_reporting002', 'apple_store001', 'f1003', 'google_play001', 'google_play002', 'greenhouse001', 'hubspot001', 'lever001', 'marketo001', 'maturity001', 'mrr001', 'mrr002', 'playbook001', 'qualtrics001', 'quickbooks002', 'quickbooks003', 'recharge002', 'retail001', 'tickit001', 'tpch002', 'workday001', 'workday002']

## 🎯 Flake candidates (passed a full board but NOT 6/6) — hardening backlog

| task | full-board | in @baseline(spd0008)? | class |
|---|---|---|---|
| airbnb001 | 0/6 | — | NEVER-FULL |
| airport001 | 0/6 | — | NEVER-FULL |
| analytics_engineering001 | 0/6 | — | NEVER-FULL |
| asana001 | 0/6 | — | NEVER-FULL |
| atp_tour001 | 0/6 | — | NEVER-FULL |
| chinook001 | 0/6 | — | NEVER-FULL |
| divvy001 | 0/6 | — | NEVER-FULL |
| flicks001 | 0/6 | — | NEVER-FULL |
| hive001 | 0/6 | — | NEVER-FULL |
| intercom001 | 0/6 | — | NEVER-FULL |
| jira001 | 0/6 | — | NEVER-FULL |
| movie_recomm001 | 0/6 | — | NEVER-FULL |
| nba001 | 0/6 | — | NEVER-FULL |
| netflix001 | 0/6 | — | NEVER-FULL |
| pendo001 | 0/6 | — | NEVER-FULL |
| playbook002 | 0/6 | — | NEVER-FULL |
| provider001 | 0/6 | — | NEVER-FULL |
| quickbooks001 | 0/6 | — | NEVER-FULL |
| reddit001 | 0/6 | — | NEVER-FULL |
| salesforce001 | 0/6 | — | NEVER-FULL |
| sap001 | 0/6 | — | NEVER-FULL |
| scd001 | 0/6 | — | NEVER-FULL |
| shopify_holistic_reporting001 | 0/6 | — | NEVER-FULL |
| social_media001 | 0/6 | — | NEVER-FULL |
| superstore001 | 0/6 | — | NEVER-FULL |
| synthea001 | 0/6 | — | NEVER-FULL |
| tickit002 | 0/6 | — | NEVER-FULL |
| tpch001 | 0/6 | — | NEVER-FULL |
| twilio001 | 0/6 | — | NEVER-FULL |
| xero001 | 0/6 | — | NEVER-FULL |
| xero_new001 | 0/6 | — | NEVER-FULL |
| xero_new002 | 0/6 | — | NEVER-FULL |
| zuora001 | 0/6 | — | NEVER-FULL |
| apple_store001 | 1/6 | ✅ | FLAKE |
| asset001 | 1/6 | — | FLAKE |
| f1002 | 1/6 | — | FLAKE |
| recharge001 | 1/6 | — | FLAKE |
| recharge002 | 1/6 | ✅ | FLAKE |
| f1001 | 2/6 | — | FLAKE |
| marketo001 | 3/6 | ✅ | FLAKE |
| f1003 | 3/5 | ✅ | FLAKE |
| hubspot001 | 4/6 | ✅ | FLAKE |
| quickbooks003 | 4/6 | ✅ | FLAKE |
| greenhouse001 | 5/6 | ✅ | FLAKE |
| maturity001 | 5/6 | ✅ | FLAKE |
| mrr002 | 5/6 | ✅ | FLAKE |
| retail001 | 5/6 | ✅ | FLAKE |
| tpch002 | 5/6 | ✅ | FLAKE |

## ✅ Rock-solid (6/6 full-board)

activity001, app_reporting001, app_reporting002, google_play001, google_play002, lever001, mrr001, playbook001, qualtrics001, quickbooks002, tickit001, workday001, workday002

## ❌ Never passed a full board (33) — flip backlog

airbnb001, airport001, analytics_engineering001, asana001, atp_tour001, chinook001, divvy001, flicks001, hive001, intercom001, jira001, movie_recomm001, nba001, netflix001, pendo001, playbook002, provider001, quickbooks001, reddit001, salesforce001, sap001, scd001, shopify_holistic_reporting001, social_media001, superstore001, synthea001, tickit002, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001

## Per-draw reward matrix — full boards

| task | baseline(19) | spd0004(21) | spd0007v1(20) | spd0007v2(16) | spd0007b(24) | spd0008(24)★ |
|---|---|---|---|---|---|---|
| activity001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| app_reporting001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| app_reporting002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| apple_store001 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| asset001 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| f1001 | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| f1002 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| f1003 | ❌ | · | ✅ | ❌ | ✅ | ✅ |
| google_play001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| google_play002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| greenhouse001 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| hubspot001 | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| lever001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| marketo001 | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| maturity001 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| mrr001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| mrr002 | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| playbook001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| qualtrics001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| quickbooks002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| quickbooks003 | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ |
| recharge001 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| recharge002 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| retail001 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| tickit001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| tpch002 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| workday001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| workday002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

_Updated 2026-06-26 with spd0008-full (promoted @baseline). 6 full-board draws + 16 smokes._
