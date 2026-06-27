# Day-Queue 2026-06-26 — Autonomous Discovery Results Log

Champion at start: `spd0013-lean-lag-period-over-period` 27/60 (run `7f3278d0d61d2577`).
Mode: smoke-only discovery, NO full-run, NO promote (captain 12h autonomous delegation).
Rule: a smoke is useful if it flips ≥2 never-pass targets with no hard-canary regression; 1 flip = bank; 0 = conclude/reject (unless artifact gives a concrete second blocker).

Hard canaries (champion passers, must hold): activity001, app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001, quickbooks002.

| Hypothesis | Queue | Rule | Smoke run dir | Audit | New ever-pass (flips) | Canary regressions | Rule fired? | Outcome |
|---|---|---|---|---|---|---|---|---|
| spd0014 | Q1 | R7 declared-target-closure (build every declared model as base table, exact convention) | small `82d27c97`, large `49007abef31bd042` | clean (8/0/0, 16/0/0) | **0/8** (asana/intercom/netflix/pendo/reddit/social_media/zuora/xero_new all 0) | none | YES (~28×/target) | **REJECTED** — rule fired but inert-on-outcome; blocker is value/grain not closure |

| spd0015 | Q2 | report value-semantics (grain-aware COUNT + raw-grain + independent value-recheck) | small `90f430c9`, large `582854b932b0c604` | clean (8/0/0, 16/0/0) | **0/8** (flicks/movie_recomm/nba/playbook002/twilio/xero001/xero_new002/quickbooks001 all 0) | none | YES (~19×/target) | **REJECTED** — fired but inert; the "independent recheck" is correlated→self-confirms wrong value |

## META-PATTERN (after Q1+Q2, both 0-flip)

Two broad generative rules over 8-target pools both FIRED heavily but flipped **0** never-pass tasks, with
**0 canary regressions** (clean + non-destabilizing, but inert-on-outcome). The never-pass cells each carry
a SPECIFIC per-task residual a broad rule cannot reach — mirroring airbnb001, the one cell that flipped this
arc, which needed the EXACT `LAG`-over-own-output insight found only by **per-task offline diagnosis**.
spd0015 also reconfirmed the verification-without-oracle wall: a solver's self-recheck is correlated with its
own error, so it cannot catch a value it doesn't know is wrong. **Implication: the productive lever for the
never-pass pool is per-task offline gold reconstruction → narrow per-task rule, not broad README rules.**
Continuing Q4/Q3 for coverage (different mechanisms), but tempering yield expectations.

| spd0016 | Q4 | per-target model-inventory (grain/PK/support-refs, validate each separately) | small `a60b0165`, large `36577512f9e2d5c3` | clean (8/0/0, 14/0/0) | **tickit002 1/2 (VARIANCE near-miss)**; 0 durable | none | YES (inventory/validate-each heavy) | **REJECTED** — tickit002 reached gold once (lever-attributable) but coin-flip; BANK for per-task diagnosis |

### ⭐ BANKED NEAR-MISS: tickit002 (top discovery signal of the sweep)
tickit002 PASSED the spd0016 small smoke (1.0) under the per-target grain/PK inventory rule (rule fired:
INVENTORY×10, VALIDATE EACH×10, grain×25) then reverted (0.0) in the large smoke = a 1/2 coin-flip. Its
known issue is sibling-grain — exactly what the inventory targets — so the pass is plausibly
lever-attributable. **RECOMMENDED FOLLOW-UP: per-task offline gold reconstruction of tickit002 (the
airbnb001 method) → a narrow, reliable grain rule.** This is the highest-value next bet from the sweep.

| spd0017 | Q3 | minimal package/dependency repair (compile-boundary only) | (no smoke — premise falsified) | n/a | n/a | n/a (rule never fires) | **REJECTED** — zero compile-failures left among gradeable tasks; package-repair family already fixed by the packaging layer; inert by construction |

## SWEEP SUMMARY (all 4 day-queue queues covered)

- **Q1 spd0014** declared-target-closure → REJECTED (fired, 0/8, blocker is value not closure).
- **Q2 spd0015** report value-semantics → REJECTED (fired, 0/8, self-recheck correlated=false-green).
- **Q4 spd0016** per-target model-inventory → REJECTED (0 durable; **tickit002 1/2 variance near-miss BANKED**).
- **Q3 spd0017** minimal package-repair → REJECTED without smoke (premise falsified: 0 compile-failures left among gradeable tasks; packaging layer already fixed the build-failure family).

**Headline: broad README rules over multi-target pools FIRE reliably but flip ~0 never-pass tasks; 0 hard-canary regressions throughout (all rules non-destabilizing).** The never-pass pool's binding blockers are SPECIFIC per-task residuals (value/grain), not addressable by a single broad rule — reconfirming that the one durable flip of this program (airbnb001) came from per-task offline diagnosis, not a broad rule. **Pivoting remaining sprint time to per-task offline diagnosis of the banked reachable near-miss (tickit002) → narrow reliable rule.** @baseline unchanged = spd0013 27/60 (no promote, no full, as instructed).

---

## Detail log

### spd0014 — Queue 1 declared-target-closure — REJECTED (0 flips)
R7 fired heavily on all targets (enumerated + built declared model set) but flipped 0/8. Binding blocker
for the Q1 pool is **value/grain** (distinctness/sign/rolling/row-set), not declared-set existence —
these tasks already build "all tables exist" but mismatch on values. Declared-target closure = clean
non-destabilizing scaffold (necessary-not-sufficient, mirrors spd0006 router), 0 canary regressions.
→ Q1 never-pass pool folds into Queue-2 (value semantics). No full, no promote. @baseline = spd0013 27/60.


