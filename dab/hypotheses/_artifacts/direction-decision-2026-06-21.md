---
title: Direction decision — close the dead concept board, pivot to determinism+precision judged multi-trial
date: 2026-06-21
decider: captain
status: decision record (the "why" behind closing dab0004/0005/0013/0014, merging dab0002+dab0003 → dab0016)
---

# Why this decision

After dab0015 (the first and only gpt-5.5 GO — flat-string serialization, validated-but-not-promoted,
~1 cell within noise), the captain reviewed the remaining concept board and decided the next move. The
reasoning, recorded so future operators see the *why*, not just the dispositions:

## What we now know (the constraints this decision respects)
1. **Two output-shape families are dead.** README cannot suppress the entity-**decoration reflex**
   (dab0012 inert both cycles; benchmark verifier off-limits) — and the benchmark scorer is never ours
   to change. This kills the whole decoration axis.
2. **Anti-abstention and the tier knob are dead** (dab0009/0010 phantom gains; dab0005/dab0008 refuted —
   high ≯ xhigh).
3. **The one thing that worked is a DELIBERATED-choice lever** (dab0015 serialization). The validated
   principle: gpt-5.5 will follow a README rule that pins a *deliberated representation/analytic choice*,
   but will NOT act on suppressing an *un-perceived reflex*. Future levers must live in the deliberated class.
4. **The band is 28 stable / 14 variable / 12 never-pass.** The never-pass 12 are oracle-blind/hard
   (levers don't touch them). The real opportunity is the **14 variable cells** (3/6–5/6): solvable but
   not reliable.
5. **Individual levers move ~1 cell, within the ±3 noise floor.** No README lever closes the
   gpt-5.5↔Opus gap; that needs a benchmark-design change. So the honest goal is *consistency* —
   stabilizing the variable band — not a headline jump.

## The decisions
- **CLOSE dab0013 (anti-decoration prose) + dab0014 (list prose) — REJECTED, pre-empted.** Both sit on
  the decoration/output-shape axis dab0012 proved README-inert; they would hit the same wall.
- **CLOSE dab0005 (methodology/tier) — REJECTED.** Premise refuted (high ≯ xhigh, dab0008).
- **CLOSE dab0004 (join-grain) — REJECTED/inert for gpt.** Its headline target GITHUB_REPOS-q4 is already
  gpt 6/6; the only real cell (googlelocal-q2) was addressed by dab0015's serialization lever.
- **MERGE dab0002 (determinism/tiebreak) + dab0003 (aggregation/filter precision) → dab0016.** They
  overlap on the same variable cells and are one idea: *pin the analytic semantics*. This is the chosen
  next lever because:
  - it targets the **variable band** (the consistency opportunity), not the dead never-pass set;
  - determinism (ordering, tie-breaks, `>=` vs `>`, inclusive dates, distinct-vs-rows, NULLs) is a
    **deliberated choice** → the tractable class (same class as the dab0015 success), not the dead reflex class.
- **dab0006 (stripped-label, agnews-q4) left active but low-EV** (hard near-tie + integrity-sensitive);
  not closed, not prioritized.

## The method change (the deeper half — "make the score more consistent")
Consistency is a **pass-RATE** property; **single-trial cannot measure it** (the dab0015 yelp-q6 trap: a
4/6 cell's single pass is indistinguishable from luck). So dab0016 is judged **MULTI-TRIAL** (3–6 draws on
target+canary cells), scored as a pass-rate shift vs the 6-draw band (`baseline-variance-6draw.md`) — a
deliberate, scoped refinement of the standing trials:1 rule for consistency-targeting levers.

## De-risk before committing a run
dab0016's first step is a **transcript probe** of 1–2 variable cells (stockmarket-q4, crmarenapro-q3) to
confirm the variance is **under-specification** (fixable by a determinism rule) vs a **hard-analytic
near-tie** (not fixable). Commit to propose/full only if under-specification is confirmed.

## Honest ceiling
Even fully successful, this stabilizes a handful of variable cells — incremental, not a gap-closer. It is
the most durable and best-measured remaining play, and it is the one that actually answers "consistency."
