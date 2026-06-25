# spider2-dbt — Flake Candidate Ledger

Tracks every task that has PASSED at least once across our runs: how many attempts, how many
passes, the pass-rate, and — the key reliability metric — the **full-board rate** (passes across the
3 apples-to-apples full 61-cell draws: `baseline@1`, `spd0004-full`, `spd0007-full`).

**Why:** gpt-5.5/xhigh is non-deterministic; a single FAIL→PASS flip can be a lucky draw, and a
"passer" can be flaky. After the failure-pattern flip program (spd0006–spd0010) banks new passers,
the next phase is **hardening the flaky ones to consistent PASS**. This ledger is that backlog.

**Maintenance:** regenerate after every full run (append the run as a new full-board draw column);
a task graduating to 3/3 full-board moves from FLAKE → ROCK-SOLID. Smoke draws inform but the
full-board rate is authoritative (smokes use different task subsets + sometimes rejected levers).

## Summary

- **25** tasks have passed ≥1 time; **36** never passed (the flip backlog).
- **16** are ROCK-SOLID (3/3 full boards) — the reliable core.
- The rest are FLAKE CANDIDATES — passed but not every full board (or only in smokes). **These are the consistency-hardening targets.**

## 🎯 Flake candidates (passed but NOT 3/3 full-board) — the hardening backlog

| task | passes/attempts | rate | full-board | class | notes |
|---|---|---|---|---|---|
| jira001 | 1/10 | 10% | 0/3 | SMOKE-ONLY FLICKER | only passed once (a grain-lever smoke); 0/3 full — effectively a near-miss, not a real passer |
| salesforce001 | 3/8 | 38% | 0/3 | SMOKE-ONLY FLICKER | passes only in spd0004/0005 grain smokes; 0/3 full — spine task (spd0009) |
| f1001 | 6/12 | 50% | 1/3 | FLAKE (full-board) | known value-level coin-flip (position_desc status cols); the canonical flake |
| f1003 | 1/2 | 50% | 1/2 | FLAKE (full-board) | OUR spd0007 router flip (sibling-mirror); thin (2 draws) — needs more draws |
| retail001 | 4/8 | 50% | 2/3 | FLAKE (full-board) | OUR spd0007 value-def flip (COUNT*) — attributable but flaky 2/3; harden after promotion |
| quickbooks003 | 4/6 | 67% | 2/3 | FLAKE (full-board) | build-completeness coin-flip (final statements materialize or not) |
| hubspot001 | 2/3 | 67% | 2/3 | FLAKE (full-board) | regressed under spd0007 (R2-author+id-cast nudge); guard added in v2 |
| mrr002 | 2/3 | 67% | 2/3 | FLAKE (full-board) | regressed under spd0007 (id-cast on R1 model); guard added in v2 |
| marketo001 | 7/8 | 88% | 2/3 | FLAKE (full-board) | mostly solid (2/3 full); spine/coverage sensitive |

## ✅ Rock-solid passers (3/3 full-board) — the reliable core

| task | passes/attempts | full-board |
|---|---|---|
| activity001 | 9/9 | 3/3 |
| app_reporting001 | 3/3 | 3/3 |
| app_reporting002 | 4/4 | 3/3 |
| google_play001 | 3/3 | 3/3 |
| google_play002 | 3/3 | 3/3 |
| greenhouse001 | 3/3 | 3/3 |
| lever001 | 3/3 | 3/3 |
| maturity001 | 3/3 | 3/3 |
| mrr001 | 10/12 | 3/3 |
| playbook001 | 3/3 | 3/3 |
| qualtrics001 | 3/3 | 3/3 |
| quickbooks002 | 4/4 | 3/3 |
| tickit001 | 3/3 | 3/3 |
| tpch002 | 4/4 | 3/3 |
| workday001 | 4/4 | 3/3 |
| workday002 | 4/4 | 3/3 |

## ❌ Never passed (36) — the flip backlog (failure-pattern hypotheses spd0006–spd0010)

airbnb001, airport001, analytics_engineering001, apple_store001, asana001, asset001, atp_tour001, chinook001, divvy001, f1002, flicks001, hive001, intercom001, movie_recomm001, nba001, netflix001, pendo001, playbook002, provider001, quickbooks001, recharge001, recharge002, reddit001, sap001, scd001, shopify_holistic_reporting001, social_media001, superstore001, synthea001, tickit002, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001

## Per-draw reward matrix (passers only; ✅ pass · ❌ fail · · not in draw)

| task | baseline@1 | spd0004-full | spd0007-full | baseline-rerun9 | spd0004-smoke | spd0004-smoke-c2 | spd0005-smoke | spd0005-smoke-c2 | spd0005-confirm3(x3) | spd0006-smoke-v1 | spd0006-smoke-v2 | spd0007-smoke-v1 | spd0007-smoke-old | spd0002-smoke | smoke6-oc | smoke6-oc-v2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| activity001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | ✅ | ✅ | ✅ | · | ✅ | ✅ | ✅ |
| app_reporting001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| app_reporting002 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | ✅ | · | · |
| f1001 | ✅ | ❌ | ❌ | · | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | · | · | · | ✅ | ✅ |
| f1003 | ❌ | · | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| google_play001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| google_play002 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| greenhouse001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| hubspot001 | ✅ | ✅ | ❌ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| jira001 | ❌ | ❌ | ❌ | · | ❌ | ❌ | ✅ | ❌ | ❌ | · | · | · | · | · | ❌ | ❌ |
| lever001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| marketo001 | ❌ | ✅ | ✅ | · | ✅ | ✅ | ✅ | ✅ | ✅ | · | · | · | · | · | · | · |
| maturity001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| mrr001 | ✅ | ✅ | ✅ | · | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | · | ❌ | · | · |
| mrr002 | ✅ | ✅ | ❌ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| playbook001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| qualtrics001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| quickbooks002 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | ✅ | · | · | · | · |
| quickbooks003 | ❌ | ✅ | ✅ | · | · | · | ✅ | ✅ | ❌ | · | · | · | · | · | · | · |
| retail001 | ❌ | ✅ | ✅ | ❌ | · | · | ✅ | ❌ | ❌ | · | · | ✅ | · | · | · | · |
| salesforce001 | ❌ | ❌ | ❌ | · | ❌ | ✅ | ❌ | ✅ | ✅ | · | · | · | · | · | · | · |
| tickit001 | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · | · |
| tpch002 | ✅ | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · |
| workday001 | ✅ | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · |
| workday002 | ✅ | ✅ | ✅ | ✅ | · | · | · | · | · | · | · | · | · | · | · | · |

_Generated 2026-06-25 from 16 run draws (3 full-board + 13 smokes/partials). spd0007-smoke-v2 (in flight) not yet included._
