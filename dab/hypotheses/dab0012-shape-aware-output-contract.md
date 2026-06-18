---
id: dab0012
title: stockmarket-q3 - shape-aware output contract (scalar/ranking -> terse names+numbers; list -> full enumeration)
status: hypothesis
kind: hypothesis
source: dab0001 ideate (retargeted to stockmarket-q3); _artifacts/model-strengths-cross-learning.md §2a + §4
started: 2026-06-18T08:50:00Z
score: 0.9
---

## Hypothesis

gpt-5.5 fails `stockmarket-q3` 0/6 NOT on a compute gap but on output SHAPE: it computes the exact
same 15 financially-troubled NASDAQ companies and the same 2008 average-volume numbers Opus does
(Opus passes 5/6), then **decorates each ranking row with the company's description** ("Apex Global
Brands Inc. specializes in creating and marketing…: 23781.42; …"). The verifier's normalized-string
match rejects the narrative. Opus emits `name: number; name: number` and passes. This is the
cleanest output-shape signal in the target set: the answer is already correct, only the shape is
wrong (`_artifacts/model-strengths-cross-learning.md` §2a, raw-log audited).

The fix is **shape-aware** because the two output biases are in TENSION. A blunt "be terse / answer
only the question" rule fixes stockmarket-q3 but BREAKS `yelp-q6`, where the gold answer is a
multi-element category LIST and Opus's terseness drops elements (Opus 1/6; gpt passes 4/6 by
emitting the full list). So the rule MUST branch on answer SHAPE.

**The README change** (fork `spacedock-readme-baseline` -> `dab0012-shape-aware-output-contract`),
ONE idea, in the `## Rules` section. The existing line `Answer ONLY the question — no commentary
or counter-examples` has proven insufficient (gpt still injects descriptions), so REPLACE it with a
shape-branched contract:

> **Match the answer's shape to the question, then write nothing extra.**
> - **Scalar or ranking answer** (a single value, or a `name: number; name: number; …` ordered
>   list): emit ONLY the entity names and their numeric values. Do NOT append a description,
>   definition, explanation, or any narrative about an entity — the row is `name: number`, never
>   `name (what it does): number`.
> - **List answer** (the question asks for the categories / tags / set / "and its X" of an entity):
>   emit the COMPLETE enumeration of every element, comma-separated. Do NOT collapse a multi-element
>   list to its first element.
>
> Worked example (foreign domain): for "rank the 3 longest rivers by length," write
> `Nile: 6650; Amazon: 6400; Yangtze: 6300` — not `Nile (a river in Africa flowing north): 6650; …`.
> For "name the busiest airport and the airline alliances operating there," write
> `Hartsfield-Jackson; Star Alliance, Oneworld, SkyTeam` — emit all three alliances, not just the first.

The foreign-domain worked examples (rivers / airports) avoid leaking the target schema into the
README and avoid contaminating any decision sim (per the leak-catch rule in
`ade-bench-sim-validates-tendency-not-real-run`).

## Targets

- **PRIMARY flip — stockmarket-q3** (gpt 0/6, Opus 5/6): must flip to PASS. Acceptance = the scalar/
  ranking branch suppresses the description injection so the ranking string matches gold; verified
  by committed artifact (the emitted answer string for q3 is `name: number; …`, no descriptions).
- **LOAD-BEARING regression canary — yelp-q6** (gpt 4/6, VARIABLE list-answer cell): MUST NOT regress
  below its 4/6 band. This is the cell a terse-only rule would break; the list branch exists to
  protect it. A drop here falsifies the shape-awareness of the rule.
- **Stable format-sensitive canaries to hold** — bookreview-q1 (6/6), stockmarket-q1/q2/q5 (6/6),
  yelp-q1/q2/q3/q5 (6/6): no regression (the rule must not perturb already-passing format-sensitive
  ranking/list cells).

## Acceptance criteria (falsifiable)

- **GO** iff stockmarket-q3 flips to PASS by committed artifact AND yelp-q6 holds at/above its 4/6
  band AND no ROCK-STABLE (6/6) canary drops — judged per-cell against the 6-draw band in
  `_artifacts/baseline-variance-6draw.md`, never on a single draw (standing captain rule:
  single-trial, judge by committed artifact + bleed-free canaries).
- **NO-GO / falsified** if stockmarket-q3 stays FAIL (the description injection is not the cause, or
  the rule does not suppress it), OR if yelp-q6 drops below its band (the rule is effectively
  terse-only and the list branch failed to protect the list answer).

## Smoke set

| Task | Baseline (6-draw) | Should-pass after lever | Role |
|---|---|---|---|
| stockmarket-q3 | 0/6 | PASS (flip) | 🎯 primary flip |
| yelp-q6 | 4/6 (variable) | hold ≥4/6 | ❌ load-bearing list canary |
| bookreview-q1 | 6/6 | PASS | ✅ stable format canary |
| stockmarket-q1 | 6/6 | PASS | ✅ stable ranking canary |
