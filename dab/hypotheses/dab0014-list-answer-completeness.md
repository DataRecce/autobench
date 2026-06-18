---
id: dab0014
title: yelp-q6 - list-answer completeness (emit every element; do not collapse to the first)
status: hypothesis
kind: hypothesis
source: dab0001 ideate (the LIST half of the shape-aware contract, isolated as a stabilizer probe)
started: 2026-06-18T08:50:00Z
score: 0.55
---

## Hypothesis

This isolates the LIST half of the shape-aware contract (dab0012) as a stabilizer/safety probe. It
does NOT target stockmarket-q3 — it tests whether an explicit list-completeness rule can be added
WITHOUT regressing the protected band, so that the list branch is proven harmless before it ships
inside dab0012. The mechanism: when the gold answer is a multi-element list (e.g. yelp-q6's category
field `Restaurants, Breakfast & Brunch, American (New), Cafes`), Opus's terseness drops elements and
fails ("Missing category: breakfast & brunch"); gpt's elaborative bias already emits the full list
and passes 4/6 (`_artifacts/model-strengths-cross-learning.md` §2c). Because gpt is our solver and
already list-complete on yelp-q6, this rule is expected to be **INERT on gpt** — the value is proving
that the list-completeness clause does not perturb already-passing list/format cells, de-risking the
list branch for dab0012.

**The README change** (fork `spacedock-readme-baseline` -> `dab0014-list-answer-completeness`), ONE
idea, in `## Rules`, ADD after the existing answer-shape lines:

> **When the question asks for a SET — the categories, tags, members, or "and its X" of an entity —
> emit EVERY element, comma-separated, in the database's field order. Do not collapse a multi-element
> list to its first element or summarize it.** Worked example (foreign domain): for "name the busiest
> airport and the airline alliances operating there," answer
> `Hartsfield-Jackson; Star Alliance, Oneworld, SkyTeam` — all three alliances, not just the first.

No terse/concision language, no ranking instruction — the clause is gated to set/list answers only.

## Targets

- **Hold (expected INERT-pass) — yelp-q6** (gpt 4/6): must stay ≥4/6. If the explicit list rule were
  to *raise* yelp-q6 above its band that is a bonus, but the primary claim is no regression.
- **Stable list/format canaries to hold** — bookreview-q1/q2/q3 (6/6), yelp-q1/q2/q3/q5 (6/6): no
  regression. This is the real test: does an added list-completeness clause perturb any
  already-passing format cell?
- **Measure-only (NOT a target) — stockmarket-q3**: a ranking answer; the list clause has no trigger
  on it, so it should stay 0/6. Reported only to confirm the clause is correctly gated (it must NOT
  accidentally help or hurt the ranking cell).

## Acceptance criteria (falsifiable)

- **GO (de-risks dab0012's list branch)** iff yelp-q6 holds ≥4/6 AND no 6/6 list/format canary drops
  — judged per-cell against `_artifacts/baseline-variance-6draw.md`, never single-draw. A clean hold
  proves the list-completeness clause is safe to compose into dab0012.
- **NO-GO / falsified** if any 6/6 list/format canary drops, OR yelp-q6 drops below band — meaning an
  explicit list rule perturbs already-passing cells, which would argue AGAINST adding a list branch
  to dab0012 (and toward dab0013's narrow anti-decoration-only design).

## Smoke set

| Task | Baseline (6-draw) | Should-pass after lever | Role |
|---|---|---|---|
| yelp-q6 | 4/6 (variable) | hold ≥4/6 | 🎯 primary hold |
| bookreview-q1 | 6/6 | PASS | ✅ stable list/format canary |
| yelp-q1 | 6/6 | PASS | ✅ stable list canary |
| stockmarket-q3 | 0/6 | stay 0/6 (no trigger) | ➖ gating check |
