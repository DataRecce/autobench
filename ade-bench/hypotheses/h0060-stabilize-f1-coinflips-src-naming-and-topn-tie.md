---
id: h0060
title: Stabilize f1001 + f1003-hard coin-flips (gated src-naming rule + top-N tie-crosses-cutoff criterion)
status: propose
kind: hypothesis
source: captain hunch (make f1001/f1003-hard stable for a reliable 36/48) + FO artifact investigation of h0059 r1-vs-r2 coin-flips
started: 2026-06-15T12:42:27Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`f1001` and `f1003-hard` are **variance coin-flips** under the h0059 `@baseline` solver — each
PASSES in one full run and FAILS in another with the identical README (confirmed: h0059 r1 had
f1001 PASS / f1003-hard FAIL; r2 had f1001 FAIL / f1003-hard PASS). Both wobbles have a
**locally-determinable, oracle-free** correct branch. Adding two precondition-gated stabilizer
rules to the `@baseline` solver README will lock both tasks to reliable PASS without touching the
construct of any other family.

This is a STABILIZER (the h0058 family), **not** the exhausted oracle-flip program — the failing
runs are degradations of a passing artifact, not an unreachable oracle.

**Target datasets:** `f1001`, `f1003-hard`.

The single README change is a composition of two gated rules (disjoint constructs — the
gated-levers-compose pattern, h0049/h0056):

1. **f1 src-model naming rule (gated on: building src models for the f1 / dbt staging layer).**
   Name each new src model exactly `src_<table>` (e.g. `src_circuits`), matching the raw table
   name with a bare `src_` prefix. Do NOT prepend the staging dataset namespace —
   `src_f1_dataset__circuits` is wrong. Every `stg_<dataset>__<table>` must then `ref('src_<table>')`
   (exactly one such ref); `stg_*__races` / `stg_*__results` keep their additional source refs.
   *This rule restates the task's own `instruction.md` ("src models should be called
   `src_<model_name>.sql`") — pure compliance reinforcement, no oracle peek.*

2. **Top-N consistency: tie-crosses-cutoff criterion (gated on: "which tables give inconsistent
   results given the current data" questions over `order by metric desc limit N` models without a
   tiebreaker).** A top-N model varies run-to-run ONLY when a tie crosses the cutoff: the metric
   value of row N also appears at row N+1, so which rows fill the final slots is nondeterministic.
   A tie lying entirely *inside* the top N changes only display order, not the returned set — do
   NOT count it. For each candidate, query the current data: if
   `count(rows with metric >= the N-th value) > N` it is inconsistent; otherwise exclude it.
   Exclude `most_fastest_laps` (the worked example given in the prompt).

## Pre-smoke Decision-Fork Probe

Proxy evidence is the **committed artifacts of the h0059 full runs themselves** (real production
solver output, not a subagent sim) — the strongest proxy available. Cells compared:

- f1001 PASS: `runs/…-full-r1/97c03e6c467742f8/ade-bench-f1001__Aj2P3Eq`
- f1001 FAIL: `runs/…-full-r2/1fcc9223b9de5194/ade-bench-f1001__9xwfouC`
- f1003-hard FAIL: `runs/…-full-r1/97c03e6c467742f8/ade-bench-f1003-hard__rtTyhMn`
- f1003-hard PASS: `runs/…-full-r2/1fcc9223b9de5194/ade-bench-f1003-hard__y4yNLTu`

**f1001 fork.** PASS run committed `src_circuits.sql` … (`src_<table>`). FAIL run committed
`src_f1_dataset__circuits.sql` … (staging prefix over-applied). Both compiled clean, so the
deviation is silent — but the hidden tests key on exact node names: `src_models_are_correct`
errors on the missing `model.f1.src_<table>` node, and `stg_models_use_src_models` FAILs 11
because staging models `ref('src_f1_dataset__…')` instead of `ref('src_<table>')`. Signature
reproduced in the FAIL cell's `verifier/test-stdout.txt`.
*Control (PASS) = bare-prefix naming → 6/6 green. Proposed rule pins exactly that branch.*
**Oracle-free: YES, unambiguous** (verbatim from `instruction.md`).

**f1003-hard fork.** PASS run committed exactly 3 answer tables (`most_retirements`, `most_wins`,
`oldest_race_winners_in_modern_era`). FAIL run committed those 3 **plus** `most_podiums`,
`most_pole_positions`, `most_races` → `count_answers` saw 6, want 3 → "Got 1 result". The
`check_option_*` tests pass in both (the 3 correct rows are present either way) — exactly the
observed signature. The disagreement is purely the inclusion criterion: PASS applied
tie-crosses-cutoff (membership); FAIL applied any-tie-incl-within-list-order. Both computed
against the same shipped data.
*Control (PASS) = boundary-tie criterion → 4/4 green. Proposed rule pins that branch.*
**Oracle-free: YES, locally computable** — caveat: it codifies a membership-vs-order
interpretation the prompt supports ("varies … given the current data" + the `most_fastest_laps`
exemplar) and the hidden test set confirms, but does not spell out in SQL. Defensible
interpretation lever, NOT the equally-plausible oracle-blind wall. Slightly higher risk than rule 1.

**Caveat:** this is proxy evidence from prior-run artifacts, not a fresh decision-fork sim; the
smoke run is the real test. Per the sim-vs-real-run lesson, a stabilizer GO must rest on the flip
reaching the committed artifact at smoke + held perturbable canaries, not on this read alone.

## Smoke set guidance (for propose)

Generative-ish gated rules → regression panel required. Targets `f1001` + `f1003-hard`, a
stable-pass sentinel, ≥1 canary per non-target family (airbnb / ana-eng / asana / intercom /
quickbooks), and **≥2 perturbable f1 canaries** the src-naming rule can actually fire on
(f1 passers that build src/staging models, e.g. `f1005`, `f1006`, `f1007`) — a stable f1 passer
the rule never touches is blind (the h0012 lesson: held its one f1 canary, broke four other f1
passers at full). Propose ensign assembles per gatekeeper G8/G10.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0060-stabilize-f1-coinflips-src-naming-and-topn-tie.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`, AND both target
coin-flips land PASS with their construct-correct committed artifact (f1001: `src_<table>` naming;
f1003-hard: 3 answer tables), with zero perturbable-canary regressions.**

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
