---
title: Infer answers under stripped/noisy ground-truth labels without leakage (integrity sandbox)
status: expanded
kind: concept
source: flipped-query-targets.md (agnews-q4 integrity-sensitive stretch) + codex-5.5 known-cheating concern
id: dab0006
score: 0.3
started: 2026-06-22T10:28:36Z
completed: 2026-06-22T10:34:56Z
verdict: PASSED
archived: 2026-06-22T10:35:03Z
---

## Direction

A solver-README rule for queries whose gold labels are deliberately stripped from the workspace
(so the agent must *infer* a category/argmax from content) while keeping a hard integrity boundary:
no `ground_truth.csv`, no external lookups, no copying hint files into the answer. The aim is to
raise the inference quality (so the argmax is right more often) **and** keep the lever leak-free —
the gatekeeper's G2 leak-guard is part of this concept, not separate from it.

## Evidence

`agnews-q4`: "2015 region with most World-category articles" — AG-News category labels are stripped,
so the answer rides on noisy content classification; Opus hit it only 1/5. Separately, the
codex-5.5 spacedock run group is known to contain cheating on *other* queries, so any inference
lever here must be paired with an explicit no-leak rule and artifact-verified at smoke.

## Candidate hypotheses (ideate fans into 2–5)

- A content-classification rule that aggregates a robust signal (majority over multiple cues)
  before taking the argmax, reducing single-cue noise.
- A reinforced no-leak rule (no ground_truth/solution/validate reads; no hint-file paste) with an
  artifact check at verify.
- An argmax-stability rule (report the winner only when its margin clears a stated threshold; else
  widen the evidence).

## Target queries

Primary (stretch): `agnews-q4`. Treat as integrity-sensitive — smoke must artifact-verify the
answer was inferred, not leaked.

## Stage Report: ideate

- DONE: File 2–5 hypothesis entities (status `hypothesis`, `dab<NNNN>-<slug>.md`, next free dab id), each ONE solver-README change, falsifiable, named target (primary agnews-q4).
  Filed 3: dab0019-deterministic-keyword-classifier, dab0020-argmax-margin-gate-dual-signal, dab0021-inference-provenance-noleak-audit; ids 0019–0021 are next free (0018 was the max present).
- DONE: Each keeps the leak-guard intact (no ground_truth/solution/validate/hint reads or pastes) and states the smoke artifact-verification that proves the answer was INFERRED, not leaked.
  Each has a `## Leak-guard (integrity, G2)` section: no oracle/hint reads, existing no-external prose byte-identical, inference proof = logged content-score table in reasoning.md + verify external-oracle audit on the analyze trace.
- DONE: Ground each in the current @baseline README + dataset-gap-ranking + latest learnings; derive concrete README changes.
  Anchored to the actual @baseline failure trace (agnews-q4 committed "South America" on a 357/348/348/346/345 razor-thin band — instability, not effort); each names the exact `analyze`/`verify` stage edit; respects dbt-CLOSED + serialization-only-validated + "talks-but-doesn't-do" by making edits mechanical/gated and avoiding self-anchored verification.

### Summary

Three single-change hypotheses targeting agnews-q4's label-stripped category inference. The
root cause from the baseline trace is a thin-margin (9-of-6700) coin-flip on a noisy
content classifier, not insufficient effort. dab0019 removes the randomness (deterministic
keyword lexicon + fixed tie-break); dab0020 adds a dual-signal agreement gate on thin margins
(falls back to UNABLE rather than guess); dab0021 isolates the concept's no-leak half as an
auditable content-provenance rule. All three are precondition-gated so canaries on perfect
datasets (bookreview/stockindex/music_brainz_20k) are untouched, and all carry an explicit
inference-vs-leak artifact proof per the integrity-sensitive mandate.
