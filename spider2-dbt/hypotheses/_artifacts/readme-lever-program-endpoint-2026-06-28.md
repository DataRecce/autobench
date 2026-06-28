# Spider2-DBT README-Lever Program — Endpoint Memo (2026-06-28)

The program tuning the codex/gpt-5.5 **solver README** to raise spider2-dbt Pass@1 has reached its ceiling.
This memo states where it ended, why, and the only paths left to 70%.

## Where it ended
- **@baseline: spd0013 = 27/60 = 0.45** (a high-variance draw; band 19/21/20/16/24/24/27). +asana001 → ~28/60 once spd0022 confirms (full-board trials=3 in flight).
- Journey: 19/61 (Opus incumbent) → 24/60 (spd0007b/spd0008) → 27/60 (spd0013), across 23 hypotheses.
- **Reliable ceiling ≈ 27–28/60.** ~13 rock-solid passers; the rest of the 27 is variance.

## The wall (why 70% is not reachable via the README)
Two compounding constraints, both proven across the program:
1. **Per-cell execution variance.** Even with the EXACT oracle-free fix in the README, the worker doesn't
   reliably produce the correct committed artifact — precise rules flip a cell ~30–67% per draw
   (tickit002 2/4, movie_recomm001 0/2, provider001 0/2). A single full draw is never promotable.
2. **The structural target itself requires a derivation the worker can't do reliably (spd0023).** The
   deepest finding: a retry-on-structural-signature loop FIRES (self-checks run, models rebuilt 7-9×) but
   can't converge multi-source cells, because the worker can't reliably derive WHAT the correct row-set
   should be (which sources compose it) without gold. "Oracle-free structural signature" is only oracle-free
   if the target structure is reliably derivable — and that derivation is the wall.

## What WORKS vs what DOESN'T (mechanism evidence)
- **WORKS — only the simplest, single-source-derivable fixes:** asana001 (drive-from-one-dimension LEFT-attach,
  4/6 across panels), airbnb001 (LAG-over-own-output, 2/2 spd0011). These have a trivially-derivable target.
- **DOESN'T — the two best general mechanisms:**
  - *Contract forcing-function* (write-the-plan-then-obey): reliable FOCUSED on one simple cell (spd0011
    airbnb 2/2) but does NOT compose — broad 7-template contract = 1/13 reliable (spd0021), focused C1 =
    only asana lands, siblings 0/3 (spd0022).
  - *Retry-on-structural-signature loop* (spd0023): fires + rebuilds but can't converge multi-source targets
    (target-derivation is the wall).
  - *Broad/precise README rules* (spd0014-20): adopted in the artifact but variance-bound; 0 durable flips.
- **Secondary rules:** positive directives are non-destabilizing; prohibitions over-fire onto passers
  (spd0018 → google_play001). Gating prevents passer cost. Multi-draw (trials≥3) is mandatory discipline.

## The never-pass pool — final map (residual catalog, 23 cells diagnosed offline)
- **Reachable but variance/derivation-blocked** (oracle-free fix known, won't reliably land via README):
  provider001, intercom001, hive001, netflix001, reddit001-comments (C1 family); xero001, xero_new001,
  xero_new002 (C2 balance-sheet); movie_recomm001 (fuzzy-join); tickit002 (no-invented-filter);
  social_media001 (cast); synthea001 (author-union); flicks001-movie_actor, playbook002-cpa (partial).
- **Oracle-blind / frozen-clock / dead** (do NOT pursue): superstore001 (ROW_NUMBER surrogate keys),
  twilio001 (package sign), playbook002-model (spec-vs-gold contradiction), flicks001-actor_rating (float
  cusp), tpch001 (gold-only thresholds), atp_tour001 + pendo001 (frozen-clock), scd001 (tiebreak),
  reddit001-posts, zuora001/quickbooks001 (variance/lineage), nba001 (read-snapshot, compliance-risky).

## The only paths left to 70% (all NON-README — captain-level strategy)
1. **Agent-scaffold retry harness** — do spd0023's loop *mechanically outside the model's discretion* (a
   wrapper that builds, runs the structural check, and rebuilds), AND supply the correct target structure
   rather than rely on the model deriving it. This is the most direct attack on both walls, but it's an
   engineering change to the solver harness, not a README edit.
2. **A stronger / more deterministic model** — the variance is gpt-5.5 execution noise at this task
   complexity; a model that reliably reproduces a known multi-step SQL would lift the reachable pool.
3. **Benchmark/verifier change** — OFF-LIMITS by standing rule (never change the scorer). Noted only for
   completeness (e.g. the frozen-clock cells are benchmark defects, not solver failures).

## Recommendation
Conclude the README-lever program. Bank the durable gains (asana001 via spd0022; airbnb001). Treat the
reachable-but-blocked catalog as the spec for a future agent-scaffold effort (path 1). Do not fire more
README hypotheses into the variance wall — the mechanism evidence is now conclusive.
