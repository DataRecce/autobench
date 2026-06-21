---
id: dab0013
title: stockmarket-q3 - strip entity descriptions from ranking rows (anti-decoration, no list branch)
status: conclude
kind: hypothesis
source: dab0001 ideate (retargeted to stockmarket-q3); isolates the anti-decoration half of dab0012
started: 2026-06-18T08:50:00Z
score: 0.75
completed: 2026-06-21T03:47:05Z
verdict: rejected
archived: 2026-06-21T03:47:15Z
---

## Hypothesis

This isolates the ANTI-DECORATION half of dab0012 to answer one question: is the description
injection *alone* the whole gpt-5.5 failure on `stockmarket-q3`, with NO list branch needed? gpt
computes the right 15 NASDAQ companies + 2008 volumes every draw but writes each ranking row as
`name (what the company does): number`; the verifier rejects the narrative
(`_artifacts/model-strengths-cross-learning.md` §2a). dab0012 fixes this AND adds a list branch to
protect yelp-q6. dab0013 makes ONLY the anti-decoration edit — a single, narrow, ranking-scoped rule
— and uses yelp-q6 as a pure falsification probe: if a description-only rule (no "be terse"
language, no list instruction) flips stockmarket-q3 WITHOUT touching yelp-q6, then the minimal
mechanism is "strip descriptions from ranking rows," and the list branch in dab0012 is redundant
defense rather than load-bearing.

**The README change** (fork `spacedock-readme-baseline` -> `dab0013-ranking-row-no-description`),
ONE idea, in `## Rules`. KEEP the existing `Answer ONLY the question` line; ADD one ranking-scoped
clause immediately after it:

> **In a ranking or `name: value` answer, each row is the entity's NAME and its numeric value
> only.** Never append the entity's description, definition, sector, or any explanatory phrase to a
> row. Write `Frontier Communications Corporation: 254397.63`, never
> `Frontier Communications Corporation (a telecommunications provider…): 254397.63`.

No "be terse" framing, no list instruction, no global concision dial — the clause is gated to
`name: value` ranking rows so it cannot reach a list answer like yelp-q6's category enumeration. The
worked example uses the target's own answer style but a generic phrasing; an alternate foreign-domain
example (`Nile: 6650`, never `Nile (a river…): 6650`) is preferred at propose time per the
leak-catch rule.

## Targets

- **PRIMARY flip — stockmarket-q3** (gpt 0/6, Opus 5/6): flip to PASS. Acceptance = committed
  artifact shows q3's ranking string carries names + numbers with NO appended descriptions.
- **Falsification probe — yelp-q6** (gpt 4/6 list cell): MUST hold at/above 4/6. Because dab0013 has
  NO list branch, a regression here would prove a description-stripping rule still bleeds into list
  answers (and would argue FOR dab0012's explicit list branch). Holding confirms the narrow rule is
  list-safe on its own.
- **Stable canaries to hold** — bookreview-q1 (6/6), stockmarket-q1/q5 (6/6): no regression.

## Acceptance criteria (falsifiable)

- **GO** iff stockmarket-q3 flips by committed artifact AND yelp-q6 holds ≥4/6 AND no 6/6 canary
  drops — judged per-cell against `_artifacts/baseline-variance-6draw.md`, never single-draw.
- **NO-GO / falsified** if stockmarket-q3 stays FAIL (description injection is not the sole cause) OR
  yelp-q6 drops (the ranking-scoped clause is not actually list-safe -> dab0012's branch is needed).
- **Relationship to dab0012:** if dab0013 flips stockmarket-q3 AND holds yelp-q6, the list branch in
  dab0012 is redundant; if dab0013 flips but yelp-q6 *drops*, dab0012's explicit list branch is
  vindicated as load-bearing. Either outcome sharpens the contract design — a knowledge gain.

## Smoke set

| Task | Baseline (6-draw) | Should-pass after lever | Role |
|---|---|---|---|
| stockmarket-q3 | 0/6 | PASS (flip) | 🎯 primary flip |
| yelp-q6 | 4/6 (variable) | hold ≥4/6 | ❌ list-safety falsification probe |
| bookreview-q1 | 6/6 | PASS | ✅ stable canary |
| stockmarket-q1 | 6/6 | PASS | ✅ stable ranking canary |
