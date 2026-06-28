# spider2-dbt — Flake Candidate Ledger

Full-board rate across the 7 apples-to-apples draws is authoritative:
`baseline(19)`, `spd0004(21)`, `spd0007v1(20)`, `spd0007v2(16)`, `spd0007b(24)`, `spd0008(24)`,
**`spd0013(27)★`** (★=@baseline). Note: baseline–spd0008 were 61-cell boards; spd0013 is the 60-cell
board (post spd0010 fixture; chinook001 packaging-defect excluded).

**Goal:** harden FLAKE candidates to consistent PASS. **Maintenance:** append each full run as a column; 7/7→ROCK.

## Summary
- **@baseline = spd0013 @ 27/60 = 0.45 (program HIGH-WATER).** Full-board draws: 19 / 21 / 20 / 16 / 24 / 24 / **27** (±range ~16–27 = the variance wall; **27 is a new high, likely the top of the band**).
- **CAVEAT:** the spd0013 +3 over spd0008 is **variance + the sap001 FIXTURE**, NOT lever-attributable. The four gains asset001/divvy001/f1001/recharge001 are flake cells bouncing UP this draw; sap001 is the deterministic spd0010 fixture repair. The lever target **airbnb001 did NOT flip at full** (smoke 1.0 → full 0.0; outcome b). A re-run may land well below 27.
- spd0013's 27 passers: ['activity001', 'app_reporting001', 'app_reporting002', 'apple_store001', 'asset001', 'divvy001', 'f1001', 'f1003', 'google_play001', 'google_play002', 'greenhouse001', 'hubspot001', 'lever001', 'marketo001', 'maturity001', 'mrr001', 'mrr002', 'playbook001', 'qualtrics001', 'quickbooks002', 'recharge001', 'retail001', 'sap001', 'tickit001', 'tpch002', 'workday001', 'workday002']

## ⭐ WITHIN-RUN VARIANCE MAP — first clean trials=3 full board (spd0022 focused-C1, 2026-06-28)

The 7-draw history above infers variance ACROSS different lever-runs over time. This is the FIRST clean
**within-run trials=3** full board (`runs/spd0022-focused-c1-contract-full-t3/6686fe7f84c0be75`, 179 clean
cells after the usage-limit topup merge), so per-task hold-rate is measured DIRECTLY — the authoritative
reliability structure. (Solver = focused-C1 contract, but it is board-NEUTRAL / no attributable move, so
these hold-rates ≈ the champion's true per-cell reliability.)

**Distribution (60 tasks × 3 draws): 20 rock-solid + 11 flaky + 28 never (+1 at 0/2).**

| Band | n | tasks |
|---|---|---|
| **3/3 ROCK-SOLID** | 20 | activity001, app_reporting001, app_reporting002, f1001, f1003, google_play001, google_play002, hubspot001, marketo001, maturity001, mrr001, mrr002, playbook001, qualtrics001, quickbooks002, recharge001, retail001, tickit001, tpch002, workday002 |
| **2/3 flaky** | 7 | apple_store001, divvy001, greenhouse001, lever001, quickbooks003, sap001, workday001 |
| **1/3 flaky** | 4 | airbnb001, airport001, asset001, f1002 |
| **0/3 never** | 28 | analytics_engineering001, asana001, atp_tour001, flicks001, hive001, intercom001, jira001, movie_recomm001, nba001, netflix001, pendo001, playbook002, provider001, quickbooks001, recharge002, reddit001, salesforce001, scd001, shopify_holistic_reporting001, social_media001, superstore001, tickit002, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001 |
| 0/2 | 1 | synthea001 (2 clean draws after merge) |

**KEY FINDING: the "27/60 champion" is really ~20 rock-solid + a rotating ~6 of the 11-cell flaky band.**
Variance math: 20 floor + E[flaky hits] (7×⅔ + 4×⅓ ≈ 6.0) = **expected ~26/60**; the documented 16–27 draw
spread is exactly *20 floor + 0–11 flaky hits*. **The TRUE reliable baseline is ~20/60, not 27** — every
single-draw score was buoyed by coin-flips.

**Earlier-banked "flips" that are actually FLAKY (not the rock-solid we treated them as):**
- **airbnb001 = 1/3** — the cell that drove the 19→24 promotion (spd0007b/spd0008) is a coin-flip.
- **apple_store001 = 2/3** — spd0008's promoted construct-dominance flip.
- asset001 = 1/3, f1002 = 1/3.
- (Genuinely held 3/3: retail001, recharge001, marketo001, maturity001, tpch002.)

**Implication:** promotion-on-single-draw was systematically optimistic — this explains the whole arc
(panel 2/3 → full 0/3; "durable" flips that don't reproduce). A real gain must move a cell into the 3/3
set, which the execution-variance wall (spd0023/spd0024) blocks for multi-step cells. Honest scoreboard =
**~20 reliable + 11 flaky + 28 unreachable**, NOT a single "27."

## 🎯 Flake candidates (passed a full board but NOT 7/7) — hardening backlog

| task | full-board (passes/draws) | in @baseline(spd0013)? | class |
|---|---|---|---|
| airbnb001 | 0/7 | — | NEVER-FULL — **lever target, STILL 0 at full** despite spd0013 lean LAG (outcome b) |
| airport001 | 0/7 | — | NEVER-FULL |
| analytics_engineering001 | 0/7 | — | NEVER-FULL |
| asana001 | 0/7 | — | NEVER-FULL |
| atp_tour001 | 0/7 | — | NEVER-FULL |
| chinook001 | 0/6 (excl. on 60-board) | — | NON-SIGNAL (gold packaging defect) |
| flicks001 | 0/7 | — | NEVER-FULL |
| hive001 | 0/7 | — | NEVER-FULL |
| intercom001 | 0/7 | — | NEVER-FULL |
| jira001 | 0/7 | — | NEVER-FULL |
| movie_recomm001 | 0/7 | — | NEVER-FULL |
| nba001 | 0/7 | — | NEVER-FULL |
| netflix001 | 0/7 | — | NEVER-FULL |
| pendo001 | 0/7 | — | NEVER-FULL |
| playbook002 | 0/7 | — | NEVER-FULL |
| provider001 | 0/7 | — | NEVER-FULL |
| quickbooks001 | 0/7 | — | NEVER-FULL |
| reddit001 | 0/7 | — | NEVER-FULL |
| salesforce001 | 0/7 | — | NEVER-FULL |
| scd001 | 0/7 | — | NEVER-FULL |
| shopify_holistic_reporting001 | 0/7 | — | NEVER-FULL |
| social_media001 | 0/7 | — | NEVER-FULL |
| superstore001 | 0/7 | — | NEVER-FULL |
| synthea001 | 0/7 | — | NEVER-FULL |
| tickit002 | 0/7 | — | NEVER-FULL |
| tpch001 | 0/7 | — | NEVER-FULL |
| twilio001 | 0/7 | — | NEVER-FULL |
| xero001 | 0/7 | — | NEVER-FULL |
| xero_new001 | 0/7 | — | NEVER-FULL |
| xero_new002 | 0/7 | — | NEVER-FULL |
| zuora001 | 0/7 | — | NEVER-FULL |
| divvy001 | 1/7 | ✅ | FLAKE — build-nondeterminism; bounced UP this draw (confirmed bouncer) |
| sap001 | 1/7 | ✅ | DETERMINISTIC — now passes post spd0010 FIXTURE repair (free to any solver; NOT flake going forward) |
| f1002 | 1/7 | — | FLAKE |
| asset001 | 2/7 | ✅ | FLAKE — bounced UP this draw (confirmed bouncer) |
| recharge001 | 2/7 | ✅ | FLAKE — bounced UP this draw (confirmed bouncer) |
| apple_store001 | 2/7 | ✅ | FLAKE |
| recharge002 | 1/7 | — | FLAKE — bounced DOWN this draw (confirmed bouncer) |
| f1001 | 3/7 | ✅ | FLAKE — bounced UP this draw (confirmed bouncer) |
| marketo001 | 4/7 | ✅ | FLAKE |
| f1003 | 4/6 | ✅ | FLAKE |
| hubspot001 | 5/7 | ✅ | FLAKE |
| quickbooks003 | 4/7 | — | FLAKE — bounced DOWN this draw (confirmed bouncer; spd0013-smoke "recovery" was variance) |
| greenhouse001 | 6/7 | ✅ | FLAKE |
| maturity001 | 6/7 | ✅ | FLAKE |
| mrr002 | 6/7 | ✅ | FLAKE |
| retail001 | 6/7 | ✅ | FLAKE |
| tpch002 | 6/7 | ✅ | FLAKE |

## ✅ Rock-solid (7/7 full-board)

activity001, app_reporting001, app_reporting002, google_play001, google_play002, lever001, mrr001, playbook001, qualtrics001, quickbooks002, tickit001, workday001, workday002

## ❌ Never passed a full board (30 on the 60-board) — flip backlog

airbnb001, airport001, analytics_engineering001, asana001, atp_tour001, flicks001, hive001, intercom001, jira001, movie_recomm001, nba001, netflix001, pendo001, playbook002, provider001, quickbooks001, reddit001, salesforce001, scd001, shopify_holistic_reporting001, social_media001, superstore001, synthea001, tickit002, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001

(chinook001 is non-signal / excluded on the 60-board.)

## Per-draw reward matrix — full boards

| task | baseline(19) | spd0004(21) | spd0007v1(20) | spd0007v2(16) | spd0007b(24) | spd0008(24) | spd0013(27)★ |
|---|---|---|---|---|---|---|---|
| activity001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| app_reporting001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| app_reporting002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| apple_store001 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| asset001 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| divvy001 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| f1001 | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| f1002 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| f1003 | ❌ | · | ✅ | ❌ | ✅ | ✅ | ✅ |
| google_play001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| google_play002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| greenhouse001 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| hubspot001 | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| lever001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| marketo001 | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| maturity001 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| mrr001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| mrr002 | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| playbook001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| qualtrics001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| quickbooks002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| quickbooks003 | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| recharge001 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| recharge002 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| retail001 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| sap001 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| tickit001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| tpch002 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| workday001 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| workday002 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| airbnb001 (lever target) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

_Updated 2026-06-26 with spd0013-full (promoted @baseline 27/60, captain decision on the headline).
7 full-board draws + 16 smokes. airbnb001 added to the matrix: 0/7, STILL 0 at full despite the
spd0013 lean LAG lever (outcome b — the contract forcing-function was load-bearing, the lean inline
rule is steerable-but-unreliable). sap001 now deterministically passes post spd0010 fixture._
