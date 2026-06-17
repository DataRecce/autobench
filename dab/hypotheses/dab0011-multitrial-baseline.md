---
id: dab0011
title: Multi-trial no-lever variance baseline (the stable-cell reference)
status: analyze
kind: hypothesis
source: dab0010 reject — captain bar "stable cells must not destabilize" needs a multi-trial baseline to be provable
started: 2026-06-17
completed:
verdict:
score: 0.95
worktree:
---

## Hypothesis

The dab0010 reject exposed that at trials:1–3 we cannot tell a lever-caused regression from intrinsic
cell variance, so every global lever risks coinciding with a stable-cell dip and being unprovable-safe.
**Claim:** a multi-trial no-lever baseline (per-cell pass-rate + variance band) makes stable-cell safety
*provable* — a lever destabilizes a cell only if it drops the cell below its baseline band — and it
retro-corrects the single-trial misjudgements of dab0009/dab0010.

**Method (cheap — existing data):** aggregate the **6 no-lever gpt-5.5/xhigh draws already on disk** —
dab0007 (our exact baseline README) + 5 CAIS `spacedock-codex-5.5-xhigh-hint` runs — into a per-cell
pass-rate. (Opus 5-run as cross-model cross-reference.) Artifact: `_artifacts/baseline-variance-6draw.md`.

## Run result

**6-draw no-lever xhigh baseline (54 cells):** 28 ROCK-STABLE (6/6) · 14 VARIABLE · 12 NEVER-PASS (0/6).
Full per-cell table in `_artifacts/baseline-variance-6draw.md`.

**It immediately resolves dab0009/dab0010 (the payoff):**
- **crmarenapro-q7, crmarenapro-q12 = 6/6** (zero natural variance) → their 1/3 under dab0010 was a
  **real lever destabilization**, not intrinsic variance. The dab0010 deep-dive's variance defense is
  refuted; the captain's reject was correct and is now evidence-backed.
- **googlelocal-q3 = 5/6** (passes without any lever) → the anti-abstention "win" was a **phantom gain**,
  an artifact of comparing lever runs against dab0007's single unlucky FAIL.
- Net: the anti-abstention program had ~no real gain and a real cost — invisible at single-trial.

## Behavioral analysis

The 12 NEVER-PASS-at-xhigh cells (DEPS_DEV_V1-q1, GITHUB_REPOS-q1/q2, PANCANCER_ATLAS-q1, PATENTS-q1/q2/q3,
agnews-q2/q3, crmarenapro-q2/q8, stockmarket-q3) are the true hard set; note crmarenapro-q2/q8 pass at the
`high` tier but are 0/6 at xhigh (tier effect — bears on dab0008). The 14 VARIABLE cells are where
single-draw flips/regressions are noise, not signal. The 28 ROCK-STABLE cells are the **protected set** any
future lever must not drop.

## Acceptance criteria

**AC-1 — A reusable per-cell baseline (pass-rate + band) exists and is committed.** ✅
`_artifacts/baseline-variance-6draw.md`.
**AC-2 — The protected set (rock-stable cells) and the variable set are enumerated**, so future levers are
judged per-cell against the band, not a single reference draw. ✅
**AC-3 — Optional:** a fresh 3-draw run of the *exact* current `spacedock-readme-baseline` to remove the
CAIS README-version confound and tighten the 14 variable cells. (Captain decision — the 28 6/6 cells are
robust without it.)

## Follow-up Routing

## Verdict
