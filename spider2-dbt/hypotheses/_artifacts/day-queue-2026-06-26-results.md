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

---

## Detail log

### spd0014 — Queue 1 declared-target-closure — REJECTED (0 flips)
R7 fired heavily on all targets (enumerated + built declared model set) but flipped 0/8. Binding blocker
for the Q1 pool is **value/grain** (distinctness/sign/rolling/row-set), not declared-set existence —
these tasks already build "all tables exist" but mismatch on values. Declared-target closure = clean
non-destabilizing scaffold (necessary-not-sufficient, mirrors spd0006 router), 0 canary regressions.
→ Q1 never-pass pool folds into Queue-2 (value semantics). No full, no promote. @baseline = spd0013 27/60.


