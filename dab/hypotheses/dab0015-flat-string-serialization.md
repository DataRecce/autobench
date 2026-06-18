---
id: dab0015
title: googlelocal-q2 - pin flat-string serialization (no JSON) for list answers
status: hypothesis
kind: hypothesis
source: dab0001 output-contract concept, re-targeted — the DECORATION sub-problem (stockmarket-q3) is dead via README (dab0012 REJECTED, _artifacts/readme-cannot-suppress-output-shape.md); this tests the distinct SERIALIZATION-FORMAT sub-problem, which is a deliberated structural choice rather than an un-perceived reflex
started: 2026-06-18T11:40:00Z
score: 0.5
---

## Hypothesis

The dab0012 boundary proved that README cannot suppress a **reflex** — gpt adds content (entity
descriptions) it does not perceive as wrong. But `googlelocal-q2` is a different failure class: the model
computes the **correct** businesses (Elite Massage 5.0, Angel-A 4.33…) yet serializes them as a **JSON
list-of-dicts** when the verifier wants a flat `name - rating; …` string (gpt ~2/6; log-audited in the
dab0001 concept). Choosing JSON-vs-flat-string is a **deliberated representation choice**, not an
un-perceived reflex — and "format the output as a flat string, not JSON" is the kind of instruction models
follow far more reliably than "withhold helpful content." So the README-inert boundary may NOT transfer to
serialization-format, and the cell is a 2/6 **coin-flip** (a choice it already sometimes gets right), not a
0/6 wall — we are *stabilizing* a choice, the cheaper bet.

**The README change** (fork `spacedock-readme-baseline` → `dab0015-flat-string-serialization`), ONE idea, in
the answer-format section:

> **Write the answer to `answers.json` as a plain flat string — never JSON.** Do not emit arrays, objects,
> key names, or brackets (`[ ] { }`) or quoted field labels. If the answer is a list of items, write them
> as a flat delimited string in the order and field-form the question implies (e.g. `Item A - 4.5; Item B -
> 4.3`), not as a list of dicts.
>
> *(consequence-framing, stated truthfully):* `answers.json` is read by an automated string-matcher, not a
> human — it looks for your answer in the expected flat text form. A JSON / structured / bracketed answer
> will not match and scores zero, even when the values inside it are correct.
>
> Worked example (foreign domain): for "list the top 2 cafes and their ratings," write
> `Blue Bottle - 4.6; Stumptown - 4.4` — NOT `[{"name":"Blue Bottle","rating":4.6}, …]`.

Foreign-domain example only (no target schema leaked). The consequence-framing attaches the format to
**correctness** (matcher fails on structure), not to style ("no commentary") — the framing the dead cycles
lacked.

## Acceptance criteria (falsifiable)

- **GO** iff `googlelocal-q2` flips/stabilizes to PASS **by committed artifact** (the committed answer is a
  flat `name - rating; …` string, not JSON) AND no canary drops — judged per-cell vs
  `_artifacts/baseline-variance-6draw.md`, never single-draw. Because the cell is a 2/6 coin-flip, "GO"
  means the committed artifact shows the flat-string form was adopted *and* the cell passes; a single
  unexplained pass is not enough.
- **NO-GO / falsified** if the committed `googlelocal-q2` answer is still JSON (the serialization rule is
  inert like the decoration rules → the WHOLE output-contract concept is dead, not just decoration) OR any
  perturbable list-answer canary drops (the flat-string rule mis-fires on a cell that needs a different
  shape → the rule is not safe).
- **Boundary value:** either outcome closes the question. GO = the reflex-vs-deliberated distinction is real
  and output-contract survives on serialization; NO-GO = README is inert for output-shape of *any* class,
  and the dab0001 concept is fully, honestly dead.

## Target queries

Primary: `googlelocal-q2` (gpt ~2/6). Generative lever (fires on every list answer) → smoke needs the G8
regression panel: ≥2 PERTURBABLE list-answer canaries (passers whose answer is a list the rule fires on —
e.g. `yelp-q6` 4/6) + ≥1 cross-dataset sentinel from a perfect-score dataset (e.g. `music_brainz_20k-q1`
6/6). Avoid Mongo/Postgres-backed cells if those backends are flaky at launch.
