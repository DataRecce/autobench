---
title: Diagnosing an unexpected smoke/full result — post-result investigation playbook
date: 2026-06-17
purpose: when a DAB run diverges from expectation, this is the fixed logic to explain WHY before deciding the route
motivated_by: dab0009 (anti-abstention lever) — smoke GO that went net-negative at full; this is the process the captain drove to understand it
applies_to: the analyze stage, and any smoke/full whose result surprises you (a GO that didn't translate, a flip that didn't reproduce, an unexpected regression, a score below the matched reference)
---

# When a result is unexpected, run this ladder

A surprising result is not a verdict — it is a question ("why?"). Do not route (`promote` / `reject` /
`revise`) until you have walked these steps. Each step upgrades a guess into a calibrated claim.

## Step 1 — Quantify the surprise against the MATCHED reference

- **Never reason from the headline stratified score.** Compute the **paired per-query diff** from
  `per_trial_outcomes.json` against the **matched reference** — same model + same reasoning tier as the
  run under test (e.g. dab0009 vs dab0007, both gpt-5.5/xhigh), **not** vs the Opus `@baseline` (which
  entangles the model swap with your change).
- List **GAINS** (FAIL→PASS) and **REGRESSIONS** (PASS→FAIL) explicitly. The specific cells that moved
  and the net cell count are the real signal; the stratified delta is downstream of them.

## Step 2 — Read the raw logs of the cells that moved (artifact, not chatter)

- For each gain and regression, open the cell's codex transcript
  (`steps/main/agent/sessions/**/rollout-*.jsonl`), the committed answer, and the validator output.
- Ask the load-bearing question: **did the change's mechanism actually fire?** For a README lever, did
  its rule reach the *committed artifact* (the SQL/answer the solver wrote)? A cell that moved **without
  the mechanism firing is not mechanism-caused.**
- Classify each moved cell: `mechanism-caused` / `infra` / `sampling-variance` / `output-format`.

## Step 3 — Separate infrastructure from behavior

- Grep the moved cells' logs for connection/DNS/exception signals: `gaierror`,
  `could not translate host`, `Connection refused`, non-empty `exception_info`.
- Infra failures (e.g. `dab-postgres` DNS dropping mid-trial, a forced abstain against a dead host) are
  **not experiment evidence** — exclude them from the behavioral verdict. (DAB has a recurring
  `dab-postgres` DNS flake; expect 0–2 involuntary abstains per full run on PG-backed cells.)

## Step 4 — Triangulate with run-history (the *related-vs-causal* test)

This is the step that converts "I read one log" into a population claim.

- Pull the moved cell's pass/fail across **all available historical runs**:
  - Opus 5-run set: `~/dataagentbench/_runs/spacedock-opus-4-8-xhigh-hint/run-00*/datasets/<DS>/attempts/attempt-001/validation.json`
  - CAIS codex-5.5 runs: `~/CAIS-paper-expriments/spacedock-codex-5.5-xhigh-hint/run-00*/...` (same format)
  - our prior gpt-5.5 runs (`per_trial_outcomes.json`).
- Read the pattern:
  - **STABLE passer in history (e.g. 6/7, 5/5) that failed ONLY in the changed run → the change is the
    prime suspect (RELATED).** Three independent stable cells all failing in one run is not chance.
  - **Flaky in history (e.g. 1/3, 4/5) → the move sits within the cell's own noise (NOISE).**
- A "regression" on a flaky cell is noise; a "regression" on a rock-stable cell is a signal.

## Step 5 — State causation at the honest ceiling

- **Single-trial cannot prove causation.** Any change rewrites the whole prompt, and gpt-5.5 is
  non-deterministic even at `temperature 0` — so a change re-rolls the dice on *every* cell.
- Honest claims, strongest → weakest:
  1. `infra` — proven by an exception in the log.
  2. `RELATED` — run-history shows N stable cells failed only in the changed run.
  3. `no mechanism fired` — the change's rule is absent from the failing committed artifact.
  4. `sampling variance` — the move is inside the cell's historical noise band.
- **"Proven causal" requires a MULTI-TRIAL run** (N draws, changed vs unchanged, same cells). When the
  verdict hinges on causation, say multi-trial is the only thing that settles it — do not overclaim from
  one draw, in either direction.

## Step 6 — Pre-(re)run decision simulation (leak-free) to catch design flaws

Before re-running a revised change, simulate the decision process to predict behavior and catch flaws.

- One subagent per target cell. Give it **only solver-visible inputs**: the question (`query.json`) and
  `db_description.txt` (NOT `db_description_withhint.txt`). **Hard leak ban:** never let it read
  `ground_truth.csv`, `validate.py`, the withhint file, or any prior run transcript. A sim that sees the
  truth overfits and returns a **false GO** (the h0057 lesson).
- Per cell, classify the change's effect: **HELPS** (fixes the failure) / **NEUTRAL-INERT** (no trigger;
  proceeds identically) / **INSUFFICIENT** (a coin-flip the change can't control — e.g. a near-tie
  classification) / **PERTURBS** (a concrete mechanism by which the change could harm a normally-passing
  cell — e.g. an "always commit a value" rule suppressing a correct `None`).
- **A sim estimates DECISION TENDENCY, not real-run outcome.** Use it to catch design flaws and
  calibrate confidence — never to skip the (multi-trial) smoke for a new change.

## The principles that anchor every step

1. **Match the reference** (isolate the variable); per-query, never the headline score.
2. **Artifact over chatter; mechanism-fired over verdict-moved.**
3. **Infra ≠ behavior.**
4. **Stable-in-history + failed-only-here = related; flaky-in-history = noise.**
5. **Single-trial = no causation proof.** ±3-cell noise floor; multi-trial is the only proof.
6. **Generative changes perturb cells they never explicitly touch** (the dab0009 lesson) — and a
   board-safety check (canary panel at smoke, or the whole board at full) is the only way to see it.
7. **Sims: leak-free, tendency-not-truth.**

## Worked example — dab0009 (anti-abstention lever)

- **Surprise:** smoke was GO (abstention cells flipped 3/3, 3/3, 2/3), but the full came in at 0.5902 —
  **−0.010 below the matched no-lever reference** (dab0007, 0.6002). A GO that went net-negative.
- **Step 1:** paired diff vs dab0007 → 3 gains (agnews-q4, googlelocal-q3, stockmarket-q4),
  4 regressions (PANCANCER-q2, bookreview-q3, crmarenapro-q7, crmarenapro-q12) — all 4 were passers.
- **Steps 2–3:** logs showed the lever's rule did **not** fire on the regressions; `bookreview-q3` was a
  `dab-postgres` DNS outage (infra, excluded).
- **Step 4:** run-history (5 Opus + 5 CAIS + our runs) showed PANCANCER-q2 / crmarenapro-q7 / q12 are
  **6/7–7/7 stable** and failed **only** in the lever run → **RELATED**, not noise. (Earlier "probably
  noise" was wrong — it was based on too few runs; the CAIS 5-run set flipped the read.)
- **Step 5:** verdict = lever is net-neutral-to-negative; the regressions are *related* to the change
  (likely global prompt perturbation), **not proven causal** at single-trial.
- **Step 6:** pre-resmoke sims of a leaner rule caught two concrete design flaws before spending a run —
  a `None`-suppression risk on crmarenapro-q7 and a source-reconciliation perturbation on PANCANCER-q2 —
  and confirmed agnews-q4 is an uncontrollable coin-flip.
