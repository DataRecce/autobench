---
title: gpt-5.5 @xhigh no-lever variance baseline (6-draw) — the stable-cell reference
date: 2026-06-17
purpose: the multi-trial no-lever baseline that makes stable-cell-safety PROVABLE (dab0011). A future lever DESTABILIZES a cell only if it drops the cell below its band here. Built to fix the single-trial blind spot that sank dab0009/dab0010 judgement.
sources: dab0007 (our exact baseline README, 1 draw) + 5 CAIS spacedock-codex-5.5-xhigh-hint runs (~/CAIS-paper-expriments). All gpt-5.5/xhigh/hint, no lever.
caveat: the 5 CAIS draws may use a slightly older baseline README than spacedock-readme-baseline; treat as a strong empirical PRIOR on each cell's natural variance. The 28 rock-stable (6/6) cells are robust regardless; a fresh 3-draw run of the exact current baseline README would tighten the 14 variable cells (optional).
---

# The finding that motivated this baseline

Judging dab0009/dab0010 on single-draw deltas vs dab0007 was **doubly misleading**, and this 6-draw
baseline proves it:

- **crmarenapro-q7 and crmarenapro-q12 are 6/6 (zero natural variance).** Their 1/3 under dab0010 was
  therefore a **real lever-caused destabilization**, NOT "intrinsic variance" (the dab0010 deep-dive's
  variance defense is refuted; the captain's reject was correct).
- **googlelocal-q3 is 5/6 naturally — it PASSES without any lever.** It failed only in dab0007's single
  draw, so the anti-abstention lever's one "win" was a **phantom gain**: comparing the lever runs against
  dab0007's one unlucky FAIL. The lever didn't flip a stable-fail; the cell passes ~83% on its own.

Net: the anti-abstention program had ~no real gain and a real cost — invisible under single-trial,
obvious against a multi-trial baseline. **Rule for the loop:** judge any lever's per-cell effect against
this band, never against a single reference draw.

# gpt-5.5 @xhigh no-lever 6-draw variance baseline (dab0007 + 5 CAIS codex-5.5-xhigh)

Per-cell pass-rate across 6 no-lever xhigh draws. A future lever DESTABILIZES a cell only if it drops below this band.

## ROCK-STABLE — protected set (must stay PASS)  [28]
- GITHUB_REPOS-q4: 6/6
- PANCANCER_ATLAS-q2: 6/6
- agnews-q1: 6/6
- bookreview-q1: 6/6
- bookreview-q2: 6/6
- bookreview-q3: 6/6
- crmarenapro-q1: 6/6
- crmarenapro-q4: 6/6
- crmarenapro-q5: 6/6
- crmarenapro-q6: 6/6
- crmarenapro-q7: 6/6
- crmarenapro-q9: 6/6
- crmarenapro-q11: 6/6
- crmarenapro-q12: 6/6
- googlelocal-q1: 6/6
- music_brainz_20k-q1: 6/6
- music_brainz_20k-q2: 6/6
- music_brainz_20k-q3: 6/6
- stockindex-q1: 6/6
- stockindex-q2: 6/6
- stockindex-q3: 6/6
- stockmarket-q1: 6/6
- stockmarket-q2: 6/6
- stockmarket-q5: 6/6
- yelp-q1: 6/6
- yelp-q2: 6/6
- yelp-q3: 6/6
- yelp-q5: 6/6

## VARIABLE — naturally noisy (do NOT count flips/regressions here as signal)  [14]
- DEPS_DEV_V1-q2: 5/6
- GITHUB_REPOS-q3: 5/6
- PANCANCER_ATLAS-q3: 5/6
- googlelocal-q3: 5/6
- googlelocal-q4: 5/6
- yelp-q4: 5/6
- yelp-q7: 5/6
- agnews-q4: 4/6
- crmarenapro-q10: 4/6
- crmarenapro-q13: 4/6
- stockmarket-q4: 4/6
- yelp-q6: 4/6
- crmarenapro-q3: 3/6
- googlelocal-q2: 2/6

## NEVER-PASS (0/6) — hard/oracle-blocked  [12]
- DEPS_DEV_V1-q1: 0/6
- GITHUB_REPOS-q1: 0/6
- GITHUB_REPOS-q2: 0/6
- PANCANCER_ATLAS-q1: 0/6
- PATENTS-q1: 0/6
- PATENTS-q2: 0/6
- PATENTS-q3: 0/6
- agnews-q2: 0/6
- agnews-q3: 0/6
- crmarenapro-q2: 0/6
- crmarenapro-q8: 0/6
- stockmarket-q3: 0/6

