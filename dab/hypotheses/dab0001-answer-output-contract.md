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

## Evidence

`googlelocal-q2`: codex-5.5 on our spacedock surface computed the **correct** businesses
(Elite Massage 5.0, Angel-A 4.33…) in all 5 CAIS runs, but 4/5 emitted a JSON list-of-dicts while
the verifier expected a `name - rating; …` string — a pure output-format miss (log-audited, not
cheating). This is the cleanest same-model lever signal in the target set.

## Candidate hypotheses (ideate fans into 2–5)

- A `verify`-stage rule that re-serializes the answer to the format the query's phrasing implies
  (scalar / delimited string / list), with a worked foreign-domain example.
- A decimal-precision / rounding normalization rule (≥4 dp where asked; no thousands separators).
- An ordering/label normalization rule for list answers.

## Target queries

Primary: `googlelocal-q2`. Format-sensitive canaries to hold: `bookreview-q1`, `stockmarket-q3`.
