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

| spd0018 | follow-up | no-invented-attribute-filter (filter rows by join keys only, not payload cols) | small `b2c23e69`, large `abd24136c9d9d407` | clean (8/0/0, 13/0/0) | tickit002 **2/4 across all draws** (not reliable) | **google_play001** (clause fired + regressed = over-fire) | YES | **REJECTED** — precise rule unreliable-on-target + passer-regression risk; variance wall holds |

## CAPSTONE FINDING (after 5 hypotheses)

The day-queue's premise — narrow README rules can each flip ≥2 never-pass tasks — did **not** bear out:
- **Broad rules (Q1 closure, Q2 value-semantics, Q4 inventory): fire reliably, flip ~0.** Each never-pass cell has a SPECIFIC per-task residual a broad rule can't reach.
- **Q3 package-repair: moot** — the packaging layer already eliminated all build-failures among gradeable tasks.
- **Per-task diagnosis (tickit002): correctly locates the residual, but the FIX hits the variance wall.** tickit002 is REACHABLE (reproduces gold offline) yet only 2/4 across draws even with a precisely-diagnosed oracle-free rule — the worker's draw-to-draw SQL-shape variance dominates a single README clause. And a prohibition clause carries passer-regression risk (google_play001 over-fire).

This reconfirms the program-wide wall (spd0013): **README levers are steerable-but-UNRELIABLE; only the heavy contract forcing-function bought reliable compliance, at a passer/prose cost.** The 70% target is not reachable at the current draw-to-draw variance via README rules alone. Net new ever-pass from this sprint: **0 durable** (tickit002 banked reachable-but-variance-bound). 0 regressions to the champion (all smoke-only, nothing promoted). @baseline unchanged = spd0013 27/60.

**Remaining sprint time → a per-task RESIDUAL CATALOG** (offline, read-only) so the captain has a precise map of which never-pass cells are reachable and what each needs — see `_artifacts/never-pass-residual-catalog-2026-06-27.md`.

| spd0019 | catalog (movie_recomm001) | partial-match join (prefix-LIKE + schema-as-spec + no-dedup) | small `300860b7`, large `660df86057bb6353` | clean (7/0/0, 11/0/0) | movie_recomm001 **0/2** | mrr001 (flake, gate doesn't match) | YES (heavy) | **REJECTED** — rule adopted but finer title-normalization residual remains |

| spd0020 | catalog (provider001) | preserve-all-rows LEFT-join for reference/dim/crosswalk targets | small `505ade11`, large `9e0bca7102369194` | clean (7/0/0, 11/0/0) | provider001 **0/2** | **none** (positive directive is safe) | YES (discussed gold counts) | **REJECTED** — adopted but two-table artifact unreliable; 0 regressions |

## FINAL SPRINT SUMMARY (7 hypotheses spd0014–spd0020 + residual catalog)

**Net durable new ever-pass = 0. @baseline UNCHANGED = spd0013 27/60. Nothing promoted, no full runs, no champion edits — exactly as instructed.** All 14 smoke runs strict-audit-clean (0 coverage_missing, 0 tainted).

**What was tested:**
- **Broad rules (Q1 closure / Q2 value-semantics / Q4 inventory):** fire reliably, flip **0** never-pass tasks. Each cell has a per-task residual a broad rule can't reach.
- **Q3 package-repair:** moot — 0 compile-failures remain among gradeable tasks (packaging layer already fixed them). Concluded without a smoke.
- **3 precise, oracle-free, per-task fixes** from offline diagnosis (tickit002, movie_recomm001, provider001): each was ADOPTED in the artifact (rules fired heavily) but **none flipped reliably** — tickit002 2/4, movie_recomm001 0/2, provider001 0/2.

**THE DEFINITIVE FINDING:** README levers — broad OR surgically-precise-and-oracle-free — do **not** reliably flip the never-pass pool. Two compounding walls: (1) **finer-than-captured residuals** — a precise rule fixes its named residual but a finer one survives (movie_recomm001 title-normalization, provider001 two-table); (2) **draw-to-draw worker SQL-shape variance** — the worker doesn't reliably adopt even a once-adopted rule (tickit002 flipped 2/4 across draws). This reconfirms spd0013 at depth: **lean README rules are steerable-but-UNRELIABLE; reliable compliance needed the heavy contract forcing-function (spd0011/spd0013), which carries a passer/prose cost.** The 70% target is not reachable via README rules at the current variance.

**Secondary finding:** POSITIVE directives ("do X this way", spd0020) are non-destabilizing (0 regressions), while PROHIBITIONS ("don't do Y", spd0018) over-fire onto passers (google_play001). Prefer positive directives.

**Banked reachable leads (for a future approach that can beat the variance wall — e.g. the heavy contract checkpoint, or a verifier-side change):** tickit002 (grain + no-invented-filter), movie_recomm001 (prefix-LIKE + finer title-norm), provider001 (two-table LEFT-join), xero001 (spine-endpoint), nba001 (read-snapshot-parquet), flicks001 `movie_actor_by_year`, playbook002 `cpa_and_roas` join-grain. **Confirmed oracle-blind / not pursuable:** superstore001 (ROW_NUMBER surrogate keys), twilio001 (package sign), playbook002 model-choice (spec-vs-gold contradiction), flicks001 `actor_rating` (float cusp). Full map in `_artifacts/never-pass-residual-catalog-2026-06-27.md`.

---

## Detail log

### spd0014 — Queue 1 declared-target-closure — REJECTED (0 flips)
R7 fired heavily on all targets (enumerated + built declared model set) but flipped 0/8. Binding blocker
for the Q1 pool is **value/grain** (distinctness/sign/rolling/row-set), not declared-set existence —
these tasks already build "all tables exist" but mismatch on values. Declared-target closure = clean
non-destabilizing scaffold (necessary-not-sufficient, mirrors spd0006 router), 0 canary regressions.
→ Q1 never-pass pool folds into Queue-2 (value semantics). No full, no promote. @baseline = spd0013 27/60.


