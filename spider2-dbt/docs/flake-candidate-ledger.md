# spider2-dbt — Flake Candidate Ledger

Per-task pass history across our runs. **Full-board rate** (passes across the 5 apples-to-apples 61-cell
draws) is the authoritative reliability metric: `baseline(19)`, `spd0004-full(21)`, `spd0007-v1(20)`,
`spd0007-v2(16)`, **`spd0007b(24)★`** (★ = current @baseline / champion). Smokes inform but use subsets.

**Goal:** after the flip program banks passers, harden FLAKE candidates to consistent PASS.
**Maintenance:** append each new full run as a full-board draw column; 5/5 full → ROCK, partial → FLAKE.

## Summary

- **@baseline = spd0007b @ 24/61 = 0.3934** (full-board draws: 19 / 21 / 20 / 16 / **24** — ±range still wide).
- **28** tasks passed ≥1; **33** never passed.
- spd0007b's 24 passers = ['activity001', 'app_reporting001', 'app_reporting002', 'asset001', 'f1002', 'f1003', 'google_play001', 'google_play002', 'greenhouse001', 'hubspot001', 'lever001', 'maturity001', 'mrr001', 'mrr002', 'playbook001', 'qualtrics001', 'quickbooks002', 'quickbooks003', 'recharge001', 'retail001', 'tickit001', 'tpch002', 'workday001', 'workday002']

## 🎯 Flake candidates (passed but NOT 5/5 full-board) — hardening backlog

| task | passes/attempts | full-board | in @baseline(spd0007b)? | class |
|---|---|---|---|---|
| jira001 | 1/12 | 0/5 | — | SMOKE-FLICKER |
| salesforce001 | 3/10 | 0/5 | — | SMOKE-FLICKER |
| asset001 | 1/6 | 1/5 | ✅ | FLAKE |
| f1002 | 2/6 | 1/5 | ✅ | FLAKE |
| recharge001 | 2/6 | 1/5 | ✅ | FLAKE |
| f1001 | 7/14 | 2/5 | — | FLAKE |
| marketo001 | 7/10 | 2/5 | — | FLAKE |
| f1003 | 2/5 | 2/4 | ✅ | FLAKE |
| hubspot001 | 3/6 | 3/5 | ✅ | FLAKE |
| quickbooks003 | 5/8 | 3/5 | ✅ | FLAKE |
| retail001 | 8/12 | 4/5 | ✅ | FLAKE |
| greenhouse001 | 4/5 | 4/5 | ✅ | FLAKE |
| maturity001 | 5/6 | 4/5 | ✅ | FLAKE |
| mrr002 | 5/6 | 4/5 | ✅ | FLAKE |
| tpch002 | 6/7 | 4/5 | ✅ | FLAKE |

## ✅ Rock-solid (5/5 full-board)

activity001, app_reporting001, app_reporting002, google_play001, google_play002, lever001, mrr001, playbook001, qualtrics001, quickbooks002, tickit001, workday001, workday002

## ❌ Never passed (33) — flip backlog

airbnb001, airport001, analytics_engineering001, apple_store001, asana001, atp_tour001, chinook001, divvy001, flicks001, hive001, intercom001, movie_recomm001, nba001, netflix001, pendo001, playbook002, provider001, quickbooks001, recharge002, reddit001, sap001, scd001, shopify_holistic_reporting001, social_media001, superstore001, synthea001, tickit002, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001

## Per-draw reward matrix — full boards (✅/❌/·)

| task | baseline(19) | spd0004-full(21) | spd0007-v1(20) | spd0007-v2(16) | spd0007b(24)★ |
|---|---|---|---|---|---|
| activity001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| app_reporting001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| app_reporting002 | ✅ | ✅ | ✅ | ✅ | ✅ |
| asset001 | ❌ | ❌ | ❌ | ❌ | ✅ |
| f1001 | ✅ | ❌ | ❌ | ✅ | ❌ |
| f1002 | ❌ | ❌ | ❌ | ❌ | ✅ |
| f1003 | ❌ | · | ✅ | ❌ | ✅ |
| google_play001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| google_play002 | ✅ | ✅ | ✅ | ✅ | ✅ |
| greenhouse001 | ✅ | ✅ | ✅ | ❌ | ✅ |
| hubspot001 | ✅ | ✅ | ❌ | ❌ | ✅ |
| jira001 | ❌ | ❌ | ❌ | ❌ | ❌ |
| lever001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| marketo001 | ❌ | ✅ | ✅ | ❌ | ❌ |
| maturity001 | ✅ | ✅ | ✅ | ❌ | ✅ |
| mrr001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| mrr002 | ✅ | ✅ | ❌ | ✅ | ✅ |
| playbook001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| qualtrics001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| quickbooks002 | ✅ | ✅ | ✅ | ✅ | ✅ |
| quickbooks003 | ❌ | ✅ | ✅ | ❌ | ✅ |
| recharge001 | ❌ | ❌ | ❌ | ❌ | ✅ |
| retail001 | ❌ | ✅ | ✅ | ✅ | ✅ |
| salesforce001 | ❌ | ❌ | ❌ | ❌ | ❌ |
| tickit001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| tpch002 | ✅ | ✅ | ✅ | ❌ | ✅ |
| workday001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| workday002 | ✅ | ✅ | ✅ | ✅ | ✅ |

_Updated 2026-06-26 with spd0007b-full (promoted to @baseline). 5 full-board draws + 14 smokes._
