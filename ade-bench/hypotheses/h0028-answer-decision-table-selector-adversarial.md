---
id: h0028
title: Answer Decision Table Selector (adversarial re-fire) -- forced-divergence candidates with cross-examination; an IN survives only if it withstands an adversarial attack
status: conclude
kind: hypothesis
source: "re-fire of h0026 (REJECTED — implementation wrong, hypothesis sound). h0026 falsified the *self-anchored* selector design (one session simulating N candidates, scoring by own checks); it did NOT falsify the multi-candidate selector idea itself. Two G9 axes unmet in h0026: (a) generation independence — one session = one mind photocopied 3 times; (b) judgment independence — selector scored candidates by their own checks, so a confident wrong answer scores perfect. This variant fixes both axes without a harness change, using forced-divergence stances and adversarial cross-examination within the same session. Forks the current @baseline solver protocol as a declared protocol-family variant."
started: 2026-06-06T00:00:00Z
completed: 2026-06-16T17:11:18Z
verdict: REJECTED
score:
worktree:
---

## Hypothesis

Answer-style tasks can fail even when the output shape is correct, because the committed
answer string is assembled from plausible narrative rather than a decisive local check per
option. h0026 showed this is real — but its selector was self-anchored: three candidates
sharing the same exploration converged on the same wrong answer (`ABDE`), and the scorer
graded their shared wrong belief 6/6. The idea is correct; the implementation was wrong.

**Falsifiable claim:** for answer-style tasks, run a three-role adversarial protocol:

**Role C1 — Normal candidate.** Produces a per-option decision table exactly as h0026 did:
- option label;
- local file/relation inspected;
- exact local check run + observed result;
- IN/OUT decision;
- one-line reason tied to the local check;
- final answer string mechanically transcribed from the IN rows.

**Role C2 — Attacker.** Reads C1's table. For every option C1 marked IN: finds and runs a
local check that *contradicts* the IN decision — evidence that the option is NOT a real
problem. C2 must find real counter-evidence from the data, not just assert "actually it's
fine." If C2 cannot find counter-evidence for a given IN, it records "attack failed."

**Role C3 — Devil's advocate.** Reads C1's table. For every option C1 marked OUT: finds and
runs a local check that *supports* the option being IN — evidence that it IS a real problem.
C3 must find real supporting evidence from the data. If C3 cannot find evidence for a given
OUT, it records "support failed."

**Selector rule (the outside judge):**
- An option is confirmed **IN** only if: C1 said IN **and** C2's attack on it FAILED (C2
  could not find counter-evidence). C2's failed attack IS the independent external criterion.
- An option is confirmed **OUT** only if: C1 said OUT **and** C3's support for it FAILED (C3
  could not find supporting evidence).
- If C1 said IN but C2's attack SUCCEEDED (C2 found real counter-evidence): mark **OUT**.
- If C1 said OUT but C3's support SUCCEEDED (C3 found real supporting evidence): mark **IN**.
- Any remaining conflict → default **OUT** (conservative).
- Final answer string is mechanically transcribed from the confirmed IN options only.

**Why this satisfies G9 (the axes h0026 missed):**
- **G9a — generation independence:** C2 and C3 are assigned *opposite stances* to C1 — they
  are structurally forced to disagree. C2's job is to defeat C1's INs; C3's job is to defeat
  C1's OUTs. They cannot simply echo C1's conclusions without failing their assignment.
- **G9b — judgment independence:** the selector's load-bearing criterion is not "does C1's
  table look complete" — it is "did C2's attack on this IN succeed or fail?" C2 authors and
  runs that attack independently; the attack's result is external to C1's own reasoning. A
  plausible-but-wrong IN (like h0026's option B) must now survive a dedicated adversarial
  probe — not just self-score.

The claim passes smoke if the adversarial protocol flips `f1011` to pass. It is falsified if
the adversarial probes also converge on the same wrong answer (C2 cannot find counter-evidence
for a wrong IN, meaning the data genuinely does not distinguish it — a deeper problem than
selector design).

## Protocol-family declaration

This is a **protocol-family change**, not a solver-README-only hypothesis. It adds the
three-role adversarial candidate protocol and the cross-examination selector rule. It must be
labeled as an answer-selector protocol family; do not report it as a pure README
independent-variable change. It is a direct re-fire of h0026 with the G9 fixes applied.

## Target datasets

Primary smoke target:

- `ade-bench-f1011` -- analysis/answer-style task; same target as h0026.

Canaries to prove the protocol is gated off elsewhere (same panel as h0026, trimmed to 2):

- `ade-bench-f1007` -- f1 gate-off tripwire.
- `ade-bench-asana001` -- distant-family gate-leakage tripwire.

## Acceptance criteria

**AC-1 — All three roles execute and save artifacts.** C1 saves a full per-option decision
table (six columns as h0026). C2 saves a per-IN attack log (option / attack check run /
result / attack-succeeded-or-failed). C3 saves a per-OUT support log (option / support check
run / result / support-succeeded-or-failed). All three artifacts are recoverable from the
rollout.

**AC-2 — Selection is local and mechanical.** Same leak-guard as h0026: local files/relations
only; no hidden verifier output, no public answers, no web lookup, no LLM-as-oracle reasoning.
C2 and C3 run real local SQL probes, not assertions.

**AC-3 — Smoke flips or cleanly falsifies.** The selector's confirmed-IN set should produce
the correct `ADE` answer and flip `ade-bench-f1011` to pass. If it does not flip, the
deep-dive must identify whether: (i) C2's attack on option B failed (data genuinely does not
distinguish it — a deeper problem); or (ii) C2 did find counter-evidence but the selector
did not apply it correctly.

**AC-4 — Applicability gate prevents regressions.** Non-answer canaries have no adversarial
protocol markers and remain PASS. Any canary regression is NO-GO even if `f1011` improves.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict

REJECTED (administrative close — captain-directed backlog clear, never run).

REJECTED — administrative close 2026-06-16 (FO, captain-directed backlog clear; never run). Re-fire of h0026 (multi-candidate answer-decision selector). The self-anchored-selector wall stands (see [[ade-bench-validation-self-anchored-false-green]]): without candidate diversity + an INDEPENDENT in-decision falsifier (a harness change), the design can't beat a uniformly-held plausible-wrong option. Superseded by the oracle-flip program conclusion ([[ade-bench-oracle-program-concluded]]) and the h0060 follow-up STOP. Recoverable from _archive.

## Stage Report: propose
