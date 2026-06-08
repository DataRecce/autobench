---
title: Round-2 workflow-stage program — fan the R2 proposal into its 5 pre-designed hypotheses
status: ideate
kind: concept
source: _proposal/round-2-workflow-stage-program.md (captain-approved 2026-06-08; full-five subset)
started: 2026-06-08T07:37:52Z
completed:
verdict:
---

## Direction

Realize the captain-approved **Round-2 workflow-stage proposal**
(`_proposal/round-2-workflow-stage-program.md`) as five concrete hypothesis entities. This is a
**faithful fan-out, NOT a re-ideation** — every claim, mechanism, target, kill-path, and expected
gatekeeper verdict is already designed in the proposal (produced by the R2 ideation workflow and
adversarially verified). The `ideate` ensign transcribes each proposal item into a well-formed,
falsifiable `h<NNNN>-<slug>.md` (one README change each, named target datasets, AC-1/2/3); it does
NOT invent new hypotheses, merge them, or drop any.

**Strict scope (binds every child hypothesis).** Workflow-stage + prompt/README levers only; the
benchmark is FIXED (decision #4 holds); no expanded solver access; no oracle leak (`AUTO_*_equality`,
`solution__*`, `check_option_*`, `tests/AUTO_*`). `trials: 1`; judge by committed-artifact proof +
bleed-free canaries, not multi-trial CI. Honest ceiling ≈ 32/48 (31 today + airbnb009 banked, which
is a separate run of the existing h0019, NOT one of these entities). Each child below is expected to
flip **{0}** of the known 17; their value is structural knowledge + net-protection (the
knowledge-gains-are-small-successes doctrine). Each still faces its own `propose` + `smoke` gate — the
captain decides per entity whether it ever runs.

**The five hypotheses to author (use these exact ids/slugs):**

1. **`h0037-reference-mining-stage`** (proposal §3 E-RMS, rank 1) — NEW `## Stage: Reference Mining`
   between Exploration and Implementation: before editing any model, locate the closest already-passing
   in-project sibling (or installed-package template) and copy its FROM/join/spine/window construction
   verbatim, citing `Analog: <file>:<line-range>`. Systematizes the lone survivor lever. Generative →
   needs the G8 canary panel (≥2 perturbable canaries per OBT family). Primary target: ana-eng004;
   secondary reach: intercom001/003. Expected gatekeeper: METHOD-ONLY, G7 WARN.

2. **`h0038-plan-review-method-b`** (proposal §3 E-PRMB, rank 2) — NEW `## Stage: Plan Review` between
   Exploration and Implementation: the never-run Method B (independent re-derivation + a generic
   leak-clean grain invariant, committed to `plan_review.json`); REJECT only on a locally-visible
   code-contradicts-contract bug, else `PROCEED_UNDETERMINED` and build as baseline; never reverse-
   inference (Method A, proven to false-reject). Target: infrastructure/regression-rail (no known
   failure is a clean code-contradicts-contract case). Expected gatekeeper: METHOD-ONLY, G7 HIGH.

3. **`h0039-observe-only-debug-lens`** (proposal §4 M1) — observe-only stage that ALWAYS writes a
   machine-readable reasoning record (the un-built WORKFLOW-REFINE Opening #2) and then builds EXACTLY
   as baseline. Success = `Got N` UNCHANGED on all 48 (any movement = the gate-strip failed =
   contamination = NO-GO). Method instrument; expected 0 flips by construction.

4. **`h0040-enforced-abstention-rail`** (proposal §4 M2) — the enforced abstention precondition
   (Track Z / h00Z): a fixed three-clause trigger (instruction? schema? raw-`source()` conservation/
   coverage probe — count + key-level anti-join from the IMMUTABLE source) that mechanically emits
   ABSTAIN and REVERTS edits made only to satisfy an undecidable load-bearing claim, recording
   `triage.json`. The enforcement primitive h0031 named as missing (not a third route). Net-protection;
   expected 0 flips. Carries the live G10 inverted-false-green risk (a wrong revert) → needs E0-style
   instrument validation + perturbable canaries. Note the §8-Q2 open design choice (new stage between
   Validation/Finalization vs gate-change on Finalization) for the propose worker/captain to resolve.

5. **`h0041-observe-only-triage-ledger`** (proposal §4 M3) — the h0040 three-clause trigger in
   OBSERVE-ONLY mode: writes `triage.json {claim, clause_results, would_abstain}` on all 48, never
   reverts. De-risks h0040 before it is trusted to revert (a passer flagged `would_abstain` = a
   predicted false-revert; airbnb009 must NOT be flagged). Method instrument; guaranteed 0 score impact.

Each entity must cite its proposal section, name target datasets, and write AC-1/2/3 per the
hypothesis template. Cross-ref the dead-family map (proposal §6) so none re-treads a dead family.
