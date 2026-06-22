---
id: dab0019
title: agnews-q4 - deterministic keyword-anchored content classifier for label-stripped category queries
status: hypothesis
kind: hypothesis
source: dab0006 ideate (integrity-safe stripped-label inference); forks spacedock-readme-baseline @baseline
started: 2026-06-22T10:45:00Z
score: 0.3
---

## Hypothesis

`agnews-q4` ("In 2015, which region published the largest number of articles in the World
category?") has **no `category` column** — the AG-News labels are stripped, so the solver must
*infer* each article's category from `title`+`description` content and then argmax the per-region
World count. The @baseline solver already attempts this (seeded TF-IDF + a "stress-test" rule
scorer), yet commits the WRONG region: its own trace shows the 2015 World-count ranking as
South America 357, Africa 348, North America 348, Asia 346, Europe 345 — five regions inside a
~3% band, a 9-article margin over ~6700 articles. The classification *effort* is not the gap; the
**non-determinism** is: an ad-hoc, model-authored lexicon + a seeded random component makes the
argmax a coin-flip that lands on a wrong region. The fix is to remove the randomness, not add more
of it.

Falsifiable claim: **a precondition-gated rule that, for a label-stripped category query, makes the
content classifier DETERMINISTIC — a fixed published keyword lexicon per category, a fixed
per-article scoring rule, and a fixed lexicographic region tie-break — produces a reproducible
argmax that flips `agnews-q4` to PASS.** If a deterministic classifier still lands on the wrong
region, the lexicon is mis-specified (not the determinism) and the hypothesis is falsified.

**The README change** (fork `spacedock-readme-baseline` -> `dab0019-deterministic-keyword-classifier`),
ONE idea, in the `analyze` stage as a new precondition-gated checklist item AFTER the
duplicate-source sequence (it does not touch that sequence). Gate, then mechanical recipe:

> **Label-stripped category inference (gated).** *Trigger:* the question names a category /
> class / label (e.g. "World", "Sports", "Business", "Science/Technology") that is **not a column**
> in any table — you must infer it from text fields (`title`, `description`). When this triggers,
> do NOT use a random seed, a sampled subset, or an LLM judgement call per row — those make the
> argmax irreproducible. Instead build a DETERMINISTIC classifier:
> 1. Define one fixed, lowercased keyword set per candidate category (e.g. World →
>    {war, nation, government, minister, election, diplomatic, treaty, …}; keep the lexicon in
>    `_artifacts/reasoning.md`).
> 2. Score every article by the count of category-keyword hits in `lower(title || ' ' || description)`;
>    assign the article to its single highest-scoring category; on a per-article score tie, assign
>    to NONE (drop it) so a tie cannot inflate a category.
> 3. Aggregate the target metric over the assigned category, then rank the groups; on a
>    between-group count tie at the top, break **lexicographically by the group key** and state the
>    tie in `_artifacts/reasoning.md`.
> This whole step is **skipped** when the category IS a column — read it directly.

No new external access; the lexicon is author-built from general knowledge of the category names
in the question, never from any hint/oracle file (see leak-guard below).

## Targets

- **PRIMARY flip — agnews-q4** (Opus 1/5, gpt-5.5 0/1 by trace): flip to PASS. Acceptance =
  committed `answers.json` region differs from the baseline's "South America", AND
  `_artifacts/reasoning.md` shows the fixed lexicon + a deterministic per-region World-count table
  with the stated tie-break — proving the answer was *inferred deterministically from content*, not
  drawn from any oracle.
- **Canaries to hold** (non-agnews, currently-passing — guard the gate): bookreview-q1 (perfect
  dataset, no category-inference shape — the gate must NOT fire), stockindex-q3 (perfect dataset),
  music_brainz_20k-q1 (perfect). The gate must leave every non-label-stripped query untouched.

## Acceptance criteria (falsifiable)

- **GO** iff agnews-q4 flips to PASS by committed artifact AND the reasoning artifact shows the
  deterministic lexicon + region table (inference proof) AND no canary regresses.
- **NO-GO / falsified** if agnews-q4 stays FAIL (deterministic classification with an author-built
  lexicon is insufficient — the content signal is too weak for ANY README-buildable classifier,
  closing the keyword-classifier sub-family) OR if the gate fires on a non-category query and
  regresses a canary (gate is mis-scoped → REVISE the trigger).

## Leak-guard (integrity, G2)

The added text adds NO access to hidden grading artifacts: it never reads/opens/inspects
`ground_truth.csv`, `expected_*`, `answer_key`, `gold`, or `db_description_withhint.txt`, and never
fetches/clones/looks up anything external. The lexicon is built from the category NAMES already in
the question text — not copied from any withheld description. The existing no-external-reference
prose is left byte-identical. **Inference proof at smoke:** the committed
`_artifacts/reasoning.md` must contain the per-article scoring lexicon and the per-region count
table; the `verify`-stage external-oracle audit (already in the baseline README) must find no
`ground_truth` / `huggingface` / `datasets.load_dataset` / hint-file read in the analyze trace.

## Smoke set

| Task | Baseline | Should-pass after lever | Role |
|---|---|---|---|
| agnews-q4 | ❌ FAIL (Opus 1/5) | 🎯 PASS (flip) | primary flip |
| agnews-q2 | ❌ FAIL | hold/observe (also category-inference: Science/Technology fraction) | secondary observe |
| bookreview-q1 | ✅ PASS | ✅ PASS (gate must NOT fire) | gate-scope canary |
| stockindex-q3 | ✅ PASS | ✅ PASS (gate must NOT fire) | gate-scope canary |

Net target: +1 (agnews-q4) with zero canary regression; ETA ~1 dataset smoke.
