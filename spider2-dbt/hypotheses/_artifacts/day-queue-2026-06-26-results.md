# Day-Queue 2026-06-26 — Autonomous Discovery Results Log

Champion at start: `spd0013-lean-lag-period-over-period` 27/60 (run `7f3278d0d61d2577`).
Mode: smoke-only discovery, NO full-run, NO promote (captain 12h autonomous delegation).
Rule: a smoke is useful if it flips ≥2 never-pass targets with no hard-canary regression; 1 flip = bank; 0 = conclude/reject (unless artifact gives a concrete second blocker).

Hard canaries (champion passers, must hold): activity001, app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001, quickbooks002.

| Hypothesis | Queue | Rule | Smoke run dir | Audit | New ever-pass (flips) | Canary regressions | Rule fired? | Outcome |
|---|---|---|---|---|---|---|---|---|
| spd0014 | Q1 | R7 declared-target-closure (build every declared model as base table, exact convention) | small `82d27c97`, large `49007abef31bd042` | clean (8/0/0, 16/0/0) | **0/8** (asana/intercom/netflix/pendo/reddit/social_media/zuora/xero_new all 0) | none | YES (~28×/target) | **REJECTED** — rule fired but inert-on-outcome; blocker is value/grain not closure |

---

## Detail log

### spd0014 — Queue 1 declared-target-closure — REJECTED (0 flips)
R7 fired heavily on all targets (enumerated + built declared model set) but flipped 0/8. Binding blocker
for the Q1 pool is **value/grain** (distinctness/sign/rolling/row-set), not declared-set existence —
these tasks already build "all tables exist" but mismatch on values. Declared-target closure = clean
non-destabilizing scaffold (necessary-not-sufficient, mirrors spd0006 router), 0 canary regressions.
→ Q1 never-pass pool folds into Queue-2 (value semantics). No full, no promote. @baseline = spd0013 27/60.


