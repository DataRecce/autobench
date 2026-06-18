---
title: stockmarket-q3 - Lock the answer output contract so correctly-computed answers aren't failed on format
status: ideate
kind: concept
source: flipped-query-targets.md + CAIS log audit (googlelocal-q2 codex computes the right businesses every run, 4/5 fail only on output shape)
id: dab0001
score: 0.9
started: 2026-06-18T08:41:29Z
---

## Direction

Add a solver-README rule that pins the **shape** of the final answer written to `answers.json`
(string vs list-of-dicts, decimal precision, ordering, label/units), independent of how the
analysis was computed. Many DAB verifiers compare a normalized string; a correct computation
serialized in the wrong shape is scored FAIL. A format-contract rule turns those near-misses into
reliable passes without touching the (already-correct) query logic.

## Evidence (RETARGETED 2026-06-18 — stockmarket-q3 is now primary)

`stockmarket-q3` (gpt-5.5 **0/6**, Opus **5/6** on the 6-draw band): both models compute the SAME 15
financially-troubled NASDAQ companies and the SAME 2008 average-volume numbers. gpt fails 0/6 PURELY
by decorating each ranking row with the company description ("Apex Global Brands Inc. specializes in
creating and marketing…: 23781.42; …"); the verifier's normalized-string match rejects the narrative.
Opus emits names + numbers only and passes. This is a pure output-shape miss, not a compute gap — the
cleanest output-contract lever signal in the target set
(`_artifacts/model-strengths-cross-learning.md` §2a + §4, raw-log audited).

**Design constraint (non-negotiable, §4 catch):** the two output biases are in TENSION. A blunt
"be terse" rule fixes stockmarket-q3 but BREAKS `yelp-q6`, whose gold answer is a multi-element
category LIST (gpt passes 4/6 by emitting the full list; Opus 1/6 drops elements). So the contract
MUST branch on answer SHAPE — scalar/ranking -> names+numbers only; list -> full enumeration — and
yelp-q6 is the load-bearing regression canary any terse-only rule would break.

`googlelocal-q2` (gpt 2/6): demoted to a weak secondary — a separate JSON-shape miss, not the
primary signal. NOTE: `GITHUB_REPOS-q4` is gpt 6/6 (only Opus fails it) — inert for our gpt solver,
do NOT pull it into this concept.

## Candidate hypotheses (fanned out 2026-06-18)

- **dab0012** — shape-aware output contract: scalar/ranking -> terse names+numbers; list -> full
  enumeration. PRIMARY flip stockmarket-q3, load-bearing canary yelp-q6. (the core lever)
- **dab0013** — anti-decoration only: strip entity descriptions from ranking rows, NO list branch.
  Isolates whether description-injection is the whole gpt failure; yelp-q6 as list-safety probe.
- **dab0014** — list-completeness only: emit every list element, do not collapse to the first.
  Stabilizer probe — de-risks dab0012's list branch against the protected band (INERT on gpt).

## Target queries

Primary: `stockmarket-q3` (scalar/ranking flip). Load-bearing list-answer canary: `yelp-q6`. Stable
format-sensitive canaries to hold: `bookreview-q1`, `stockmarket-q1/q2/q5`, `yelp-q1/q2/q3/q5`. Weak
secondary: `googlelocal-q2`.

## Stage Report: ideate

- DONE: At least one emitted hypothesis names stockmarket-q3 as the PRIMARY target, grounded in model-strengths-cross-learning.md
  dab0012 + dab0013 both name stockmarket-q3 PRIMARY, grounded in §2a (both models compute the same 15-company ranking + 2008 volumes; gpt fails 0/6 ONLY by injecting company descriptions — a pure output-shape miss).
- DONE: The single README change is SHAPE-AWARE — terse names+numbers for scalar/ranking, FULL enumeration for list — NOT a blunt "be concise"; and names yelp-q6 (gpt 4/6) as the load-bearing regression canary
  dab0012 is the shape-branched contract (scalar/ranking vs list); all three hypotheses name yelp-q6 as the load-bearing list canary / falsification probe per §4 tension.
- DONE: Each emitted hypothesis changes ONE idea, is falsifiable, states acceptance criteria + target datasets/queries (scalar/ranking vs list separated)
  dab0012 (full shape-aware contract), dab0013 (anti-decoration only), dab0014 (list-completeness only) — each one idea, each with GO/NO-GO acceptance + a smoke-set table separating ranking targets from list canaries.

### Summary

Retargeted dab0001 from googlelocal-q2 to stockmarket-q3 (gpt 0/6, Opus 5/6 — pure output-shape miss, the cleanest lever signal). Fanned into three single-idea hypotheses: dab0012 (the core shape-aware contract — scalar/ranking->names+numbers, list->full enumeration), dab0013 (anti-decoration half isolated, no list branch), dab0014 (list-completeness half isolated as a band-safety stabilizer). dab0013 and dab0014 are designed to falsify-or-confirm whether dab0012's list branch is load-bearing — either outcome sharpens the contract. All three carry yelp-q6 (gpt 4/6) as the load-bearing canary that a terse-only rule would break, with foreign-domain worked examples to avoid README/sim leak. googlelocal-q2 demoted to weak secondary; GITHUB_REPOS-q4 explicitly excluded as inert for the gpt solver.
