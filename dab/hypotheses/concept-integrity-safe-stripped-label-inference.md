---
title: Infer answers under stripped/noisy ground-truth labels without leakage (integrity sandbox)
status: concept
kind: concept
source: flipped-query-targets.md (agnews-q4 integrity-sensitive stretch) + codex-5.5 known-cheating concern
id: concept-integrity-safe-stripped-label-inference
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
