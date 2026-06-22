---
id: dab0020
title: agnews-q4 - argmax margin-gate requiring two independent content signals to agree before committing
status: hypothesis
kind: hypothesis
source: dab0006 ideate (integrity-safe stripped-label inference); forks spacedock-readme-baseline @baseline
started: 2026-06-22T10:46:00Z
score: 0.3
---

## Hypothesis

The @baseline failure on `agnews-q4` is a **thin-margin instability**, not an effort gap. Its
trace commits "South America" on a top ranking of 357 / 348 / 348 / 346 / 345 across ~6700 World
articles — the top three regions are within 9 of each other (<3%). At that margin a single noisy
content classifier's argmax is a coin-flip; the baseline even narrates "a close margin can be
overturned by boundary cases" and then commits anyway. The lever attacks the *decision under thin
margin*: when the leading group's lead is inside the noise band, the single-signal argmax must NOT
be trusted as-is.

Falsifiable claim: **a rule that, for a label-stripped category-inference ranking, computes TWO
independent content signals (a keyword-lexicon classifier AND a separate term-frequency / weighted
scorer) and requires them to AGREE on the winner before committing — widening the evidence (raise
the per-article assignment confidence threshold, drop no-signal articles) until they do — flips
`agnews-q4`.** The two signals are independent in *construction* (different scoring methods over
the same content), so agreement is a genuine cross-check, not one mind photocopied. If the two
signals agree on the wrong region, the content simply does not separate the regions and the
hypothesis is falsified (the margin is irreducibly within noise → README cannot fix it).

**The README change** (fork `spacedock-readme-baseline` -> `dab0020-argmax-margin-gate-dual-signal`),
ONE idea, in the `analyze` stage as a new precondition-gated checklist item:

> **Thin-margin category-inference gate.** *Trigger:* a ranking/argmax question over a category
> you had to **infer from text** (the category is not a column) AND the leading group's count is
> within 5% of the runner-up. When this triggers, do NOT commit the single-classifier argmax.
> Compute a SECOND, independently-constructed content signal — e.g. signal A = fixed-keyword hit
> count, signal B = TF-weighted category similarity — and:
> 1. If A and B agree on the top group, commit it.
> 2. If they disagree, the per-article assignments are noise-dominated: drop articles with no
>    strong category signal (raise the assignment threshold), recompute both signals, and re-test.
> 3. If they still disagree after the strongest defensible threshold, the data does not separate
>    the groups at this margin — report `"UNABLE TO DETERMINE"` rather than guessing a coin-flip.
> Record both signals' per-group tables in `_artifacts/reasoning.md`.

This is a check-and-widen rule, NOT a self-anchored "re-run your own query and trust it" — the two
signals are separately *constructed* methods (G6/G10 independence-by-different-method).

## Targets

- **PRIMARY flip — agnews-q4**: flip to PASS. Acceptance = committed region is the one BOTH signals
  agree on (shown in `_artifacts/reasoning.md` as two distinct per-region tables), OR a defensible
  `"UNABLE TO DETERMINE"` if they cannot agree (knowledge gain: proves the margin is irreducible).
- **Canaries to hold**: bookreview-q1, stockindex-q3, music_brainz_20k-q1 (gate must not fire —
  none are label-stripped category questions, so the 5% margin clause never triggers).

## Acceptance criteria (falsifiable)

- **GO** iff agnews-q4 flips to PASS by committed artifact with two distinct content-signal tables
  shown AND no canary regresses.
- **NO-GO / falsified** if the two signals agree on the WRONG region (content does not separate the
  groups — closes the dual-signal sub-family for this query) OR the rule degenerates to
  `"UNABLE TO DETERMINE"` while a deterministic classifier (dab0019) would have flipped it (the
  margin gate is over-cautious — favors dab0019) OR a canary regresses (gate mis-scoped → REVISE).
- **Relationship to dab0019:** dab0019 makes the single classifier deterministic; dab0020 adds a
  cross-signal agreement gate. If dab0019 flips alone, dab0020's second signal is redundant; if
  dab0019 lands on a wrong-but-stable region and dab0020's agreement test catches it, the
  cross-check is load-bearing. Either way the comparison sharpens the inference contract.

## Leak-guard (integrity, G2)

No access to `ground_truth.csv` / `expected_*` / `answer_key` / `gold` / `db_description_withhint.txt`;
no external fetch/clone/lookup; existing no-external-reference prose byte-identical. Both signals are
computed from in-workspace `title`/`description` content only. **Inference proof at smoke:** the
committed `_artifacts/reasoning.md` carries TWO independently-constructed per-region tables; the
`verify` external-oracle audit finds no oracle/hint/HF read in the analyze trace.

## Smoke set

| Task | Baseline | Should-pass after lever | Role |
|---|---|---|---|
| agnews-q4 | ❌ FAIL | 🎯 PASS (both signals agree) or defensible UNABLE | primary flip |
| agnews-q3 | ❌ FAIL (business-articles/year, also inferred category) | hold/observe | secondary observe |
| bookreview-q1 | ✅ PASS | ✅ PASS (gate must NOT fire) | gate-scope canary |
| stockindex-q3 | ✅ PASS | ✅ PASS (gate must NOT fire) | gate-scope canary |

Net target: +1 (agnews-q4) with zero canary regression; ETA ~1 dataset smoke.
