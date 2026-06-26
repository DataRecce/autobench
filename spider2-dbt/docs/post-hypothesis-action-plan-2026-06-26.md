# Post-Hypothesis Action Plan

Date: 2026-06-26

## Goal

If the five planned Spider2-DBT hypotheses complete and the solver still does
not reach the 70% passed-rate target, shift from hypothesis discovery to
stabilization.

The objective is not to immediately open more broad hypotheses. The next phase
should convert already-observed leverage into stable, repeatable passes.

## Scope

The current hypothesis set is:

1. `spd0006`: classifier / materialization gate
2. `spd0007b`: value definition
3. `spd0008`: over-emit collapse
4. `spd0009`: spine completeness
5. `spd0010`: fixture / verifier repair

`spd0010` must remain separately attributed because it repairs fixture or
harness defects rather than improving the solver README itself.

## Phase 0: Close The Hypothesis Loop

Each hypothesis must receive an explicit verdict:

- `promote`
- `partial-promote`
- `bank-learnings`
- `validated-not-promoted`
- `reject`
- `rerun-needed`

Do not treat partial full-run artifacts as final evidence. If a detached handle
does not have a terminal sentinel, recover from Harbor outputs before making a
verdict.

## Phase 1: Build The Outcome Ledger

Create `post-hypothesis-outcome-ledger.md` after all five hypotheses have
settled.

Classify every task into exactly one primary bucket:

- `stable_pass`: passes across repeated full draws.
- `flaky_pass`: has passed before but does not hold consistently.
- `classifier_correct_worker_failed`: the classifier selected the right rule,
  but the worker did not implement it correctly.
- `rule_too_abstract`: the rule direction is right, but the README lacks enough
  concrete implementation guidance.
- `missing_validation_signature`: `dbt build` passes, but the produced artifact
  has an obviously wrong shape.
- `fixture_or_dependency_defect`: source data, gold data, package dependency, or
  verifier setup is missing or defective.
- `low_roi_or_unreachable`: currently not worth pursuing.

The ledger is the control document for the stabilization phase. Every later
README change should map to a ledger bucket and an observed failure mode.

## Phase 2: Stabilization Pass

Prioritize these buckets:

1. `flaky_pass`
2. `classifier_correct_worker_failed`
3. `rule_too_abstract`
4. `missing_validation_signature`

For each high-ROI task family, add:

- a concrete implementation skeleton
- a positive example
- a negative example
- a validation signature
- a forbidden implementation pattern

Example: for latest-window aggregation tasks, the README should state that the
verifier runs `dbt build --full-refresh`, so required latest-window filters must
not live only inside an `is_incremental()` branch.

## Phase 3: Upgrade The Classifier Contract

The classifier should become an execution contract rather than high-level
advice.

Before implementation, the worker should identify:

- selected rule
- primary grain driver
- expected target row shape
- expected validation signature
- forbidden implementation pattern

The implementation stage should then build against that contract. The validation
stage should check the rule-specific signature instead of accepting a clean
`dbt build` as sufficient evidence.

## Phase 4: Measure Stability With Multiple Draws

Run multiple full draws against the current champion solver, preferably
overnight.

Use those runs to classify each task as:

- `always_pass`
- `sometimes_pass`
- `never_pass`
- `regression_sensitive`

The purpose is to estimate the stable floor, expected pass count, flaky upside,
and regression frequency.

## Phase 5: Targeted Repair Rounds

Run small repair hypotheses only after the ledger identifies the failure class.

Priority order:

1. Tasks that have passed before but are flaky.
2. Tasks that flipped in smoke but did not hold in full.
3. Tasks where the classifier was correct but the worker did not comply.
4. Tasks with fixture or dependency defects.
5. New rule families.

Each repair round should use targeted smoke before any full run.

## Phase 6: Recompose The Final Champion

Once stabilization has measurable gains, build a final solver README by
combining only evidence-backed changes:

- keep the `spd0007b` value-definition rules that held in full runs
- merge only successful `spd0008` and `spd0009` grain rules
- add classifier contract requirements
- add task-family skeletons
- add validation signatures
- remove or guard rules that caused regressions

Then run:

1. strict audit
2. targeted smoke
3. full run
4. multiple full draws
5. champion promotion

## Decision Rules

- If the champion reaches 30+/61, prioritize stabilization before opening new
  broad hypotheses.
- If the champion is in the 24-28/61 range, combine stabilization with
  fixture repair and the remaining high-upside spine-completeness work.
- If the champion remains below 24/61, return to the survey and search for a
  new axis.
- If many failures are worker noncompliance, improve the workflow contract
  before adding more rules.
- If many failures are fixture or verifier defects, keep a separate fixture
  track and do not attribute those gains to solver README quality.

## Immediate Next Artifact

After all five hypotheses close, create:

`spider2-dbt/docs/post-hypothesis-outcome-ledger.md`

That ledger should drive the first stabilization round:

`stabilization-pass-001`
