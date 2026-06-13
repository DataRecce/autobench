# h0056 six-lever composition — decision-fork mutual-non-interference simulation

Date: 2026-06-13. Method: `_artifacts/subagent-decision-fork-probe-method.md`.

## Why this probe (not the usual single-fork probe)

Each of the three new levers (h0053 per-key inner-join, h0054 lap-time exclude-pit, h0055
preserve-columns) was already smoke-verified SOLO and shown non-colliding with its dual in its own
solo smoke. The only NEW question the merge introduces is **six-way mutual interference**: with all
six gated rules present in ONE README, does the longer rulebook mis-route a precondition — i.e. does
a rule fire on a task it must not, or fail to fire on its own target? Captain asked to verify the
merged README has "enough probability to overcome all the target tasks" before spending the full run.

## Design

- Rulebook under test: the COMMITTED merged Implementation stage of
  `solver_workflows/h0056-compose-six-levers-on-h0052/README.md` (all six gated rules), captured to
  `/tmp/h0056-sim/rulebook.md`.
- Per task: an extractor pulled the CLEAN visible starting context (task instruction + starting model
  SQL) from a prior run cell's `agent/codex.txt`, stripped of any solver patch / verifier / oracle /
  expected totals — written to `/tmp/h0056-sim/ctx-<slug>.md`.
- Per task: **6 fresh, isolated decision agents** each given ONLY (the merged rulebook + that task's
  clean context), no repo access, no tools beyond reading those two files. Each reports which gated
  rule(s) it judges FIRE and its concrete edit. Classified in code: DESIRED iff the expected rule
  fires AND no must-not (collision) rule fires.
- 8 tasks × 6 draws = **48 isolated decisions**. (f1010-medium + quickbooks002 re-run separately
  with explicit cell paths after a 3-level glob bug failed their extraction in batch 1.)

## Result — 48/48 desired branch, 0 collisions

| Task | Role | Expected rule | Must NOT fire | Result |
|------|------|---------------|---------------|--------|
| airbnb005 | FLIP target (h0053) | per-key-inner-join | coverage-repair | **6/6 desired, 0 coll** |
| f1010-medium | FLIP/PIN target (h0054) | lap-time-exclude-pit | — | **6/6 desired, 0 coll** |
| ana-eng003 | FLIP target (h0055) | preserve-columns | feature-boundary | **6/6 desired, 0 coll** |
| airbnb009 | COLLISION canary (h0050↔h0053) | coverage-repair | per-key-inner-join | **6/6 desired, 0 coll** |
| f1006 | HOLD (h0044) | max-points | — | **6/6 desired, 0 coll** |
| f1006-hard | HOLD (h0044) | max-points | — | **6/6 desired, 0 coll** |
| quickbooks002 | COLLISION canary (h0045↔h0055) | feature-boundary | preserve-columns | **6/6 desired, 0 coll** |
| quickbooks003 | COLLISION canary (h0045↔h0055) | feature-boundary | preserve-columns | **6/6 desired, 0 coll** |

### The two collision dual-pairs both hold their correct sides
- **h0050 ↔ h0053** (completeness-intent): airbnb009 (completeness IS asked) → all 6 draws chose
  COVERAGE-REPAIR (delete the narrowing predicate, keep COUNT(*) byte-intact); the per-key inner-join
  rule did NOT fire. airbnb005 (no completeness ask) → all 6 chose PER-KEY INNER-JOIN-from-fact; the
  coverage rule did NOT fire. Opposite sides cleanly separated by the intent gate.
- **h0045 ↔ h0055** (build-vs-remove): quickbooks002+003 (feature removal) → all 12 draws chose
  FEATURE-BOUNDARY (delete the department-only guarded logic), NOT preserve-all. ana-eng003 (plain
  build/rename) → all 6 chose PRESERVE-COLUMNS (carry all 18 upstream cols), NOT feature-drop.

## Interpretation (and caveats per the method)

- **Proxy result:** the merged six-lever rulebook has no detectable decision-policy interference —
  every target routes to its intended rule and every collision canary holds its correct branch, at a
  100% rate across 48 independent draws. This clears the captain's "enough probability" bar to skip
  smoke and go to the full run.
- **What this does NOT prove (still rests on the full run):** that the solver finds the bug, writes a
  committed artifact of the chosen shape, and passes the hidden grader; and the off-construct
  trials:1 ~±3-cell variance on the 40 untouched cells. The promote decision rests on the full
  run-dir clearing h0052's expectation + committed-artifact reads (AC-3/AC-4/AC-5), not this proxy.
- Raw per-draw edits: workflow outputs `wfuvodcdu` (batch 1, 6 tasks) and `wx1zjz555` (fill-in 2).
