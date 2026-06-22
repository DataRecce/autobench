---
id: dab0021
title: agnews-q4 - inference-provenance no-leak rule (committed category must trace to a logged content-score table)
status: hypothesis
kind: hypothesis
source: dab0006 ideate (integrity-safe stripped-label inference); the explicit no-leak half of the concept; forks spacedock-readme-baseline @baseline
started: 2026-06-22T10:47:00Z
score: 0.3
---

## Hypothesis

The concept pairs the inference lever with a HARD integrity boundary because the codex-5.5
spacedock run group is known to contain cheating on other queries — any label-stripped inference
lever is only trustworthy if we can prove the committed category was *inferred from content*, not
lifted from an oracle/hint. This hypothesis isolates that integrity half as a single change: a
**provenance rule** requiring the committed answer to a label-stripped category query to TRACE to a
content-derived score table the solver itself logged, with a `verify`-stage audit that the trace
contains no oracle/hint read.

Falsifiable claim: **a rule requiring (a) every label-stripped category answer to be backed by a
logged per-class content-score table in `_artifacts/reasoning.md`, and (b) a `verify`-stage check
that the analyze trace shows the category was computed from `title`/`description` and contains no
read of `ground_truth.csv` / `db_description_withhint.txt` / any `*_withhint` / oracle file, keeps
the inference leak-free without degrading correctness.** This is an *independent audit* (it reads
the produced trace and the score table — artifacts that exist before the audit runs), NOT a
self-anchored "re-run your own query and trust it" check, so it sidesteps the dead self-verification
family. Falsified if the audit fires on a legitimately-inferred answer (false-positive: it cannot
distinguish content-derived from leaked) or is inert (the solver logs the table but the audit never
changes a verdict).

**The README change** (fork `spacedock-readme-baseline` -> `dab0021-inference-provenance-noleak-audit`),
ONE idea, split across the two stages it naturally spans BUT one idea (provenance): a clause in
`analyze` mandating the logged score table, and the matching audit sentence in the EXISTING
`verify` "External-oracle audit" paragraph (extending it, not adding a new stage):

> *(analyze, gated)* When a category/label answer is **inferred from text** (the category is not a
> column), you MUST log in `_artifacts/reasoning.md` the per-class content-score table the argmax
> came from — the score formula and the per-group counts. An inferred-category answer with no such
> table is not admissible.
>
> *(verify, appended to External-oracle audit)* Additionally, for any answer derived from an
> inferred category, confirm `_artifacts/reasoning.md` contains the content-score table backing it
> AND the analyze trace shows the category came from `title`/`description` scoring — NOT from any
> read of `ground_truth.csv`, `*_withhint`, `expected_*`, `answer_key`, or `gold`. If the backing
> table is absent or the trace shows an oracle/hint read, REJECT with the offending event index.

## Targets

- **PRIMARY (integrity-anchor) — agnews-q4** (and the agnews label-stripped class q2/q3): the
  answer must remain at least as correct as @baseline AND now carry a verifiable content-provenance
  trail. Acceptance = committed answer is backed by a logged content-score table; the verify audit
  PASSES on a genuinely-inferred answer (no false-reject) and would REJECT a planted oracle-read
  (tested by reading the existing baseline trace, which has no oracle read → must PASS).
- **Canaries to hold**: bookreview-q1, stockindex-q3, music_brainz_20k-q1 — the provenance clause
  is gated to inferred-category answers, so non-inferred queries are untouched and must not regress.

## Acceptance criteria (falsifiable)

- **GO** iff agnews-q4 (and agnews siblings) hold/flip with a logged content-score table present
  AND the verify audit PASSES the legitimately-inferred answer (no false-reject) AND no canary
  regresses — i.e. the integrity boundary is enforceable without correctness cost.
- **NO-GO / falsified** if the audit FALSE-REJECTS a content-inferred answer (cannot tell inference
  from leak → the boundary is not README-enforceable, an integrity-family wall) OR is fully inert
  (the table is logged but no verdict ever changes → it is decoration, not a guard) OR a canary
  regresses (gate mis-scoped → REVISE).
- **Relationship to dab0019/dab0020:** those raise inference *quality*; dab0021 makes the inference
  *auditable*. dab0021 is the lever you compose with whichever of dab0019/dab0020 wins, to keep the
  resulting answer provably leak-free — directly the concept's "raise inference quality AND keep it
  leak-free" pairing.

## Leak-guard (integrity, G2)

This hypothesis IS a leak-guard reinforcement: it STRENGTHENS the existing no-external-reference
prose and never weakens it; it adds NO read of any oracle/hint file (it *forbids* such reads and
*audits against* them). It reproduces no `db_description_withhint.txt` content. **Inference proof at
smoke:** the verify audit's PASS on the baseline-style inferred answer (with the logged score table
present, no oracle read in trace) is itself the proof the answer was inferred, not leaked; a planted
oracle-read in a probe trace must produce a REJECT.

## Smoke set

| Task | Baseline | Should-pass after lever | Role |
|---|---|---|---|
| agnews-q4 | ❌ FAIL | hold/flip WITH logged score table; verify PASSES (no false-reject) | 🎯 integrity anchor |
| agnews-q2 | ❌ FAIL | hold/observe with provenance table | secondary observe |
| bookreview-q1 | ✅ PASS | ✅ PASS (clause gated off) | gate-scope canary |
| stockindex-q3 | ✅ PASS | ✅ PASS (clause gated off) | gate-scope canary |

Net target: integrity boundary enforced at zero correctness cost (no canary regression); ETA ~1
dataset smoke. This is the "no-leak rule paired with the inference lever" the concept names.
