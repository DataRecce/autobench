# dab0017 — Gate 1.5 anchor + canary set

**@codex-batch-baseline** = `runs/codex-dab-batch-baseline/bf113446fdd94373` (host-fixed README,
fixed verifier, concurrency 2). All 12 datasets graded, 0 errored, audit `clean:12 tainted:0`.
**Stratified Pass@1 = 0.6966** over all 12 — **already beats Opus incumbent 0.654** (no dbt).

Per-dataset (codex-batch): yelp 7/7, stockmarket 5/5, bookreview 3/3, music_brainz 3/3,
stockindex 3/3, crmarenapro 9/13 (fail q2,q3,q7,q8), googlelocal 3/4 (fail q2), PANCANCER 2/3
(fail q1), DEPS_DEV 1/2 (fail q1), GITHUB_REPOS 2/4 (fail q1,q2), agnews 1/4 (fail q2,q3,q4),
PATENTS 0/3.

## Canary set — 36 queries (Opus ∩ codex-batch passers). The variant must NOT regress ANY.

| dataset | canary queries |
| --- | --- |
| bookreview | q1,q2,q3 |
| music_brainz_20k | q1,q2,q3 |
| stockindex | q1,q2,q3 |
| stockmarket | q1,q2,q3,q5 |
| yelp | q1,q2,q3,q4,q5,q7 |
| crmarenapro | q1,q4,q5,q6,q9,q10,q11,q12,q13 |
| googlelocal | q1,q3,q4 |
| PANCANCER_ATLAS | q2,q3 |
| DEPS_DEV_V1 | q2 |
| agnews | q1 |
| GITHUB_REPOS | q3 |
| PATENTS | (none — Opus 0/3) |

Non-regression is **per-query across the whole evaluated set**, not just named canary datasets.

## codex-batch vs Opus deltas (dbt-INDEPENDENT — model-swap + host-fix effects)

- **Regression:** crmarenapro q7 (Opus pass → codex-batch fail). Hard postgres knowledge-article
  query; single-trial. Recorded as a codex/batch finding BEFORE judging the dbt variant.
- **Gains:** GITHUB_REPOS q4, stockmarket q4, yelp q6 (codex-batch passes, Opus fails).

## Variant acceptance (restated against this anchor)

- (a) stratified Pass@1 over 12 beats Opus 0.654 — codex-batch already does (0.697); the dbt
  variant must at least hold this AND ideally beat the codex-batch anchor 0.697 (the overhead-clean
  dbt-method effect).
- (b) ZERO of the 36 canary queries regress anywhere (per-query table required).
- Flip ≥1 currently-failing target (crmarenapro q2/q3/q7/q8 or GITHUB_REPOS q1/q2 …) via the
  committed dbt-model artifact (behavioral read, not just reward).
