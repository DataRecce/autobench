---
id: dab0016
title: variable-band - pin the analytic semantics (ordering/tiebreak + thresholds/dates/NULLs) to stabilize coin-flip cells, judged multi-trial
status: hypothesis
kind: hypothesis
source: merge of dab0002 (determinism/tiebreak) + dab0003 (aggregation/filter precision); direction decision _artifacts/direction-decision-2026-06-21.md
score: 0.55
---

## Hypothesis

The benchmark's real opportunity is the **14 variable cells** (3/6–5/6 in `_artifacts/baseline-variance-6draw.md`):
the model *can* solve them but not *reliably*. A common cause of that variance is **under-specified analytic
semantics** — the model resolves an ambiguous ordering, tie-break, threshold comparator, date boundary, or
NULL/distinct decision differently run-to-run. Pinning those decisions is a **deliberated-choice** lever,
which dab0015 established is the *tractable* class for gpt-5.5 (it follows representation/analytic rules,
unlike the dead decoration reflex). So a README rule that pins the analytic semantics should convert
coin-flip cells into reliable passes — i.e. raise the **pass-rate** of variable cells, the direct
"make the score more consistent" goal.

**The README change** (fork `spacedock-readme-baseline` → `dab0016-pin-analytic-semantics`), ONE idea — a
"pin the analytic semantics" rule in the `analyze` stage:

> Before writing the answer, make every ambiguous analytic decision **explicit and deterministic**:
> - **Total order:** every ranking / top-N / argmax gets a full ORDER BY down to the last row — primary
>   metric, then stable secondary keys, then a unique id as the final tiebreak. Never leave a tie unbroken.
> - **Comparators:** state `>=` vs `>` (and `<=`/`<`) exactly as the question's wording implies.
> - **Date windows:** treat endpoints as inclusive unless the question says otherwise; pin the exact bounds.
> - **Counting:** decide distinct-entity vs row count per the question; state which.
> - **NULL / missing rows:** state the policy (exclude vs treat-as-zero) before aggregating.
>
> (Foreign-domain worked example to be added at propose; no target schema leaked.)

This is generative (fires on every analytic query) → smoke needs a G8 regression panel.

## Pre-smoke Decision-Fork Probe (REQUIRED FIRST — gate before propose/full)

Because this targets *variance*, confirm the variance is under-specification, not a hard-analytic near-tie,
BEFORE spending a run:
- Read the committed artifacts + transcripts of ≥2 variable cells across draws (start: `stockmarket-q4`
  4/6, `crmarenapro-q3` 3/6). For each, classify: does the cell flip because the model picks a different
  ORDER/tiebreak/threshold/NULL handling run-to-run (**under-specified → this lever can fix**), or because
  it lands on a different analytic branch / genuine near-tie (**hard-analytic → this lever cannot fix**)?
- Proceed to propose ONLY for the cells confirmed under-specified; drop hard-analytic cells from the target
  set (they belong to a different, probably oracle-blocked, family).

## Acceptance criteria (falsifiable) — MULTI-TRIAL

Consistency is a pass-RATE property; single-trial cannot measure it. Judge **multi-trial (3–6 draws)** on
target + canary cells vs the 6-draw band:
- **GO** iff a confirmed-under-specified target's pass-rate rises materially above its band (e.g. 3/6 or
  4/6 → ≥5–6/6 across the draws) AND no rock-stable (6/6) canary's rate drops — judged per-cell, never on
  a single draw, with the committed artifact showing the pinned semantics were actually applied.
- **NO-GO / falsified** if pinned-target rates don't rise above band (variance was hard-analytic, not
  under-specification → lever inert) OR any 6/6 canary destabilizes (the determinism rule mis-fires).
- **Boundary value:** either way we learn whether the variable band is README-stabilizable — the central
  open question for the consistency goal.

## Target queries

Primary (pending probe confirmation): `stockmarket-q4` (4/6), `crmarenapro-q3` (3/6); consider other
under-specified variable cells (`crmarenapro-q10/q13`, `DEPS_DEV_V1-q2`, `GITHUB_REPOS-q3`,
`PANCANCER_ATLAS-q3`) only if the probe shows under-specification. Hold canaries: ≥2 perturbable
ranking/aggregation passers + ≥1 cross-dataset 6/6 sentinel (generative-lever G8 panel). Judge all
per-cell vs `_artifacts/baseline-variance-6draw.md`, multi-trial.
