---
title: Propose-stage gatekeeper review guideline
applies-to-stage: propose
gate-mode: captain-gated by default; optional auto-approve only when all rules pass
maintained-by: workflow owner
last-updated: 2026-06-29
---

# Propose-Stage Gatekeeper Review Guideline

The gatekeeper reviews a proposed experiment before the pilot runs. It checks
whether the protocol is testable, honest, reproducible, and scoped to the
declared independent variable.

The gatekeeper may append only the `## Gatekeeper review` block to the hypothesis
entity. It must not run the experiment, change the protocol, fetch external data,
or resolve scientific judgment by assertion.

## Inputs

- Hypothesis entity.
- Baseline protocol or current champion method.
- Proposed protocol diff.
- Pilot and full-run execution plans.
- Frozen, versioned, or otherwise immutable execution artifacts.
- Prior learning logs in `_artifacts/`.

## Rules

Each rule receives `PASS`, `WARN`, or `FAIL`. Unevaluable rules are `FAIL` with
evidence naming what was missing.

### G1 - Single Independent Variable

The proposed protocol changes exactly the variable named in the hypothesis.

- **FAIL if:** unrelated controls, scoring, data, model, instrument settings, or
  inclusion criteria changed.
- **WARN if:** a support change is necessary but not clearly separated from the
  scientific claim.

### G2 - Provenance and Leakage Guard

The protocol must not use holdout answers, hidden labels, future observations,
published solutions, or unauthorized external references.

- **FAIL if:** any text instructs the executor to inspect answer keys, expected
  outputs, hidden verifier files, unpublished ground truth, web search, or
  external solution repositories.
- **WARN if:** allowed references are not named clearly enough to audit.

### G3 - Controls Held Constant

Controls and invariants are explicit and preserved.

- **FAIL if:** baseline, control group, sample definition, scoring rule,
  environment, randomization, or runtime changes without being the declared
  hypothesis.
- **WARN if:** a control is implicit but inferable.

### G4 - Pilot Is Focused and Representative

The pilot includes target cases, stable controls, and canaries for broad changes.

- **FAIL if:** targets are missing, no controls are present, or a broad/generative
  intervention lacks canaries that it could plausibly perturb.
- **WARN if:** the pilot is likely underpowered but still useful for mechanism
  detection.

### G5 - Auditability and Reproducibility

The execution artifacts are frozen, versioned, or immutable enough to rerun.

- **FAIL if:** protocol files are missing, mutable inputs are unrecorded, random
  seeds are omitted where applicable, or the result cannot be linked to exact
  inputs.
- **WARN if:** minor environment details are implicit but recoverable.

### G6 - Measurement Validity

The measured outcomes match the hypothesis and are not self-anchored.

- **FAIL if:** the success check compares the result only to the executor's own
  re-derived answer, or if the metric does not measure the claim.
- **WARN if:** the metric is valid but only indirect.

### G7 - Actionability

The protocol tells the executor what to do mechanically enough that the pilot can
show whether it fired.

- **FAIL if:** the proposed change is vague and cannot produce an observable
  artifact signature.
- **WARN if:** the instruction is understandable but may be acknowledged without
  changing behavior.

### G8 - Safety, Ethics, and Cost

Risks are declared and bounded.

- **FAIL if:** the protocol violates safety, privacy, policy, consent,
  compliance, or budget constraints.
- **WARN if:** risk is acceptable but mitigation is underspecified.

### G9 - Analysis Plan Before Results

The analysis plan is written before execution.

- **FAIL if:** acceptance criteria, exclusion criteria, or statistical tests will
  be chosen after seeing results.
- **WARN if:** exploratory analysis is planned but clearly separated from the
  confirmatory decision.

### G10 - Follow-Up Routing

The proposal names how outcomes will route.

- **FAIL if:** there is no rule for advance, revise, reject, or escalate.
- **WARN if:** routing exists but lacks a threshold for ambiguous outcomes.

## Recommendation

- **APPROVE** - no `FAIL` rules. Warnings are recorded for the captain.
- **REVISE** - failures are mechanical and fixable without changing the
  hypothesis.
- **REJECT** - a failure compromises integrity, leakage guard, controls, safety,
  or the declared scientific claim.

## Output Format

```markdown
## Gatekeeper review

**Recommendation: APPROVE | REVISE | REJECT** - <one-line rationale>.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated <date>).
Reviewed: <ISO 8601>.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single independent variable | PASS/WARN/FAIL | <cite> |
| G2 provenance/leakage guard | PASS/WARN/FAIL | <cite> |
| G3 controls held constant | PASS/WARN/FAIL | <cite> |
| G4 pilot coverage | PASS/WARN/FAIL | <cite> |
| G5 reproducibility | PASS/WARN/FAIL | <cite> |
| G6 measurement validity | PASS/WARN/FAIL | <cite> |
| G7 actionability | PASS/WARN/FAIL | <cite> |
| G8 safety/cost | PASS/WARN/FAIL | <cite> |
| G9 analysis plan | PASS/WARN/FAIL | <cite> |
| G10 follow-up routing | PASS/WARN/FAIL | <cite> |

Captain note: <brief decision-relevant summary>.
```

