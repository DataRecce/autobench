---
id: dab0010
title: Anti-abstention LEAN v2 (None carve-out + failure-gated persistence)
status: propose
kind: hypothesis
source: dab0009 follow-up (REJECTED as board lever — verbose v1 perturbed stable cells); captain-directed v2
started: 2026-06-17T13:06:22Z
completed:
verdict:
score: 0.85
worktree:
---

## Hypothesis

dab0009 proved the anti-abstention diagnosis is real (flips googlelocal-q3 3/3, artifact-confirmed) but
its **verbose** form perturbed otherwise-stable cells board-wide (PANCANCER-q2 / crmarenapro-q7 /
crmarenapro-q12 are 6/7–7/7 across 5 Opus + 5 CAIS + our runs, yet failed only in the v1 lever run). The
pre-smoke decision sims traced the harm to two concrete clauses. **v2 keeps the flip and removes the two
harm mechanisms** via a minimal, gated rule.

**The v2 README change** (fork `spacedock-readme-baseline` → `dab0010-anti-abstention-lean`), two edits,
nothing else:

- **`## Rules`** — replace the baseline abstention line with:
  > "Do not abstain prematurely. Return `UNABLE TO DETERMINE` only as a last resort when the data is
  > genuinely unreachable — and only after trying the connection paths named in `connections.yaml` and
  > `db_config.yaml`. When the data is reachable, commit your best computed answer.
  > A substantive negative result is a **real answer, not an abstention**: if the correct answer is
  > `None`, `0`, an empty set, or 'no match / no violation found', return it. This rule never means
  > preferring a positive value over a correct negative one."
- **`## Database Access`** — add ONE failure-gated sentence:
  > "If (and only if) a connection attempt **fails**, consult `db_config.yaml` for an alternate
  > connection detail before treating the source as unavailable. If your existing connection already
  > works, keep it — do not switch methods or re-resolve sources."

Leak-guard (no external data / ground-truth lookup) preserved verbatim. The **None carve-out** fixes the
crmarenapro-q7 None-suppression risk; the **failure-gated** clause fixes the PANCANCER-q2
source-reconciliation perturbation. Both were the v1 harm mechanisms.

**Targets:**
- **Keep the flip:** googlelocal-q3 (the real abstention flip — must survive v2).
- **Recover (no regress):** PANCANCER-q2, crmarenapro-q7, crmarenapro-q12.
- **Measure-only (NOT counted as a lever target):** agnews-q4 — a near-tie classification coin-flip the
  rule provably cannot control (sim: INSUFFICIENT). Reported for completeness only.

## Pre-smoke Decision-Fork Probe

Leak-free decision sims (one subagent per cell; given ONLY the question + `db_description.txt`; never
ground_truth/validate/withhint/transcripts). A sim estimates DECISION TENDENCY, not real-run outcome —
used here to catch design flaws, not to skip smoke. Two iterations:

| Cell | v1 (verbose) sim | **v2 (lean) sim** | conf |
|---|---|---|---|
| googlelocal-q3 | HELPS | **FLIP-PRESERVED** (abstention was reachability-driven; v2 failure-gated fallback still fires) | High |
| crmarenapro-q7 | ⚠️ None-suppression | **INERT-SAFE** (None carve-out negates the bias) | High |
| PANCANCER-q2 | ⚠️ perturbs (reconcile) | **INERT-SAFE** (failure-gated; connection works → rule never fires) | High |
| crmarenapro-q12 | INERT | **INERT** (pure computation; rule has no trigger) | High |
| agnews-q4 | INSUFFICIENT | **INSUFFICIENT** (coin-flip; rule can't control) | Low — drop as target |

Fork tested: abstain-vs-persist (googlelocal-q3) and the two v1 harm mechanisms (None-suppression,
source-reconciliation). v2 cleared both at High confidence while preserving the flip. Proxy caveat: sims
are tendency, and agnews-q4 is acknowledged uncontrollable.

## Acceptance criteria

**AC-1 — Exactly the two README edits; full spec differs from `specs/dab0007-gpt55-baseline-xhigh.yaml`
only in `experiment:` + `solver_workflow:`.** Verified by `diff`.

**AC-2 — Every recorded score paired with a clean strict audit.**

**AC-3 — MULTI-TRIAL consistency (trials:3, captain-approved exception to trials:1).** Across the 3 smoke
draws: googlelocal-q3 holds its flip; the 3 recovery cells (PANCANCER-q2, crmarenapro-q7, crmarenapro-q12)
do NOT regress (PASS in the draws), judged with the committed-artifact read (None returned where correct;
connection kept when working). agnews-q4 measured but not counted.

**AC-4 — Leak-guard intact** (no external-data relaxation; only premature abstention + a correct-None
carve-out).

**AC-5 — Board-safety deferred to the full run** (generative lever; the full run's 54 cells are the
native regression panel — do not promote on the smoke alone).

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
