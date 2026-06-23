---
id: dab0023
title: Compose the 2 durable banked levers — flat-string serialization + complete-list/flat-record — into the seed README as pre-verified levers
status: propose
kind: hypothesis
source: "dab0022 PASSED-validated follow-up (captain-directed). dab0022 validated 2 durable, confound-free flips across draws — googlelocal-q2 (flat-string serialization, reconfirming dab0015) and PATENTS-q1 (complete-list + flat simple-record) — but did NOT promote because the single-lever board lift was variance-swamped. This files the composition play: bank both pre-verified mechanisms into the seed README at once (the ade-bench h0049 gated-levers-compose pattern), scoped so they fire only where validated and do not perturb ranking/single-winner cells."
started: 2026-06-23T06:38:33Z
completed:
verdict:
score: 0.5
worktree:
---

## Hypothesis

**Falsifiable claim.** Adding **two pre-verified, scoped banked levers** — (1) a flat-string
serialization rule and (2) a complete-list / flat-record rule — to the seed solver README (fork the
current `@codex-batch-baseline` solver, `solver_workflows/spacedock-readme-baseline-hostfix`) banks the
durable dab0022/dab0015 flips (googlelocal-q2, PATENTS-q1, and any other flat-string / complete-list-shaped
cell) **without regressing the board**, because both mechanisms are already committed-artifact-validated
and are scoped to fire only where they are safe (not on ranking / single-winner cells). This is a
**banking/composition play, NOT a new mechanism** — the h0049 gated-levers-compose pattern
([[ade-bench-gated-levers-compose]]): precondition-gated levers on disjoint construct families compose
additively, the gate IS the isolation.

**The single README change** — add ONE `### Answer serialization & list rules` section with exactly these
two scoped rules (change nothing else; leak-guard prose byte-intact):

```
### Answer serialization & list rules

- Serialize each answer as a flat string of exact database values, not a JSON object/array or nested structure. For a single value, emit the value; for multiple values, emit them as a flat delimited string (e.g. `A; B; C` or `name | code | year`). Do not wrap the answer in JSON, markdown, or quotes-as-data. (Applies to the answer FORMAT only — it does not change which rows you select.)
- For a question that asks for a complete list / every qualifying row ("list all", "which X" with no top-k, "for each"), emit EVERY qualifying row as a flat-delimited record; do not truncate to top-k. This rule fires ONLY on open complete-list questions — for a single-winner question ("which one has the most", "the highest") or an explicit fixed top-k, answer with exactly that one / that k and do NOT broaden the row set or the cohort.
```

**Why these two and why scoped this way:**
- **Flat-string serialization** is the one mechanism validated TWICE: dab0015 (googlelocal-q2 flipped
  across 3 draws — adopted artifact) and dab0022 (googlelocal-q2 4/5 over 5 draws, PATENTS-q1's anchor
  failure was a JSON-list serialization crash the flat-record form fixed). Serialization-FORMAT is
  README-steerable ([[dab-flat-string-serialization-works]]); the DECORATION reflex is not — so the rule
  pins format only, explicitly NOT row selection.
- **Complete-list / flat-record**, SCOPED off single-winner and fixed-top-k questions, is the dab0022
  cycle-2 + cycle-3 scoping lesson made permanent: the un-scoped complete-list/all-associated rule
  regressed stockmarket-q3 (cycle-2, a name+number cell) and is implicated in the yelp-q4/q7 ranking
  wobble; scoping it to open complete-list questions only is what kept the durable PATENTS-q1 flip while
  removing the ranking blast radius.

**Target queries (durable, pre-verified):** googlelocal-q2 (flat-string), PATENTS-q1 (complete-list +
flat-record), plus any other flat-string / open-complete-list-shaped cell the scoped rules safely reach.
**Explicit non-targets (must NOT regress):** ranking / single-winner / fixed-top-k cells — stockmarket
q3/q4, yelp q4/q7, and the crmarenapro/PATENTS variable band (the rules are scoped to NOT fire there).

**Lever class — GENERATIVE but SCOPED.** Both rules fire by question-shape, so propose MUST carry a G8
regression panel: the durable target cells (googlelocal, PATENTS) PLUS the perturbable ranking canaries
the scope is designed to protect (stockmarket, yelp) to PROVE the scope holds — a ranking-cell regression
here means the scope failed, which is the whole falsification point.

## Pre-smoke Decision-Fork Probe

**Skipped — pre-verified banked mechanisms, no new fork to probe.** Both levers are already validated by
committed artifact from prior runs, so there is no novel mechanism whose decision-tendency a probe would
de-risk:
- **Flat-string serialization**: dab0015 CONCLUDED validated (googlelocal-q2 adopted-artifact across 3
  draws); dab0022 reconfirmed it (googlelocal-q2 4/5 over 5 draws, committed-artifact read in
  `runs/dab0022-patents-semistructured-rules/*` — "All names and scores matched", the flat form fixed the
  JSON-vs-flat output gap). See [[dab-flat-string-serialization-works]] and
  [[dab-semistructured-rules-first-real-go]].
- **Complete-list + flat-record (scoped)**: dab0022 cycle-3 proved the scoped form banks PATENTS-q1 (4/5)
  while the cycle-2→cycle-3 scoping fix removed the stockmarket-q3 / yelp ranking regression
  (committed-artifact-confirmed in the dab0022 entity ## Behavioral analysis).
The open question is COMPOSITION + SCOPE-HOLD on the full board (do the two banked cells hold together and
does the scope keep the ranking cells safe), which the smoke + a multi-draw read answer directly — a
decision-fork sim would add nothing over the existing artifact evidence. (If smoke surfaces a specific
committed-artifact fork on a still-moving cell, a probe becomes meaningful for a `smoke → hypothesis`
revision.)

## Acceptance criteria (falsifiable)

**AC-0 — Anchor is the current `@codex-batch-baseline`** (codex/gpt-5.5, high; `rk registry resolve run
@codex-batch-baseline`). Model AND effort held constant → the README is the sole variable (confound-free,
the dab0022-cycle-3 regime). Propose confirms the resolved anchor.

**AC-1 — Exactly the README change; full spec differs from the anchor only in `experiment:` +
`solver_workflow:`** (effort stays `high` to match the anchor — NO xhigh). Verified by `diff`. Leak-guard
prose byte-intact; the added section is the two scoped rules only.

**AC-2 — Every recorded score paired with a clean strict audit** (`rk audit --policy strict`:
`0 coverage_missing`, `0 tainted`; exclude both dab-postgres dual-signatures before any verdict).

**AC-3 — Verdict by committed-artifact + multi-draw hold-rate, NOT a single-draw headline.** Per the
dab0022 calibration lesson (a generative lever's single full draw carries ±0.07; a confound-free executed
cell can still be variable-band), the durable cells must be judged by their ≥2/3 (or ≥3/5) hold-rate
across draws, not one draw's board delta.

**GO** iff the durable banked cells (googlelocal-q2 + PATENTS-q1) **hold across draws** (≥2/3) AND
**zero ranking/single-winner canary regression** (the scope holds — stockmarket q3/q4, yelp q4/q7 not
dragged below anchor by the complete-list rule) AND the board median ≥ anchor. **NO-GO / REJECTED** if the
composed cells don't hold, if the scope leaks (a ranking cell regresses by the complete-list rule, by
committed artifact), or if the board median sits within the ±0.07 noise of the anchor with no durable
attributable gain (the dab0022 outcome — validated-but-not-promotable, in which case CONCLUDE-validated
without moving the seed). **PROMOTE** (move `@codex-batch-baseline` → this README) only on GO with the
durable cells held across a multi-draw confirm — this is the composition's whole point: bank pre-verified
flips into the seed so they STICK.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
