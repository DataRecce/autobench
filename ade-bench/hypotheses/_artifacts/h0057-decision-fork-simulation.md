# h0057 two-move pass-probability simulation (pre-smoke)

Date: 2026-06-14. Method: `_artifacts/subagent-decision-fork-probe-method.md`. Captain asked for a
pass-probability sim before launching smoke. Rulebook under test: the committed h0057 Implementation
stage (`solver_workflows/h0057-.../README.md`, the six h0056 levers with Move A widened + Move B worked
example) → `/tmp/h0057-sim/rulebook.md`. 8 tasks × 6 fresh, context-isolated decision agents (explicit
run-cell paths; extended schema captures the COLUMN-SET outcome, the load-bearing variable for both moves).

## Result

| Task | Role | Desired | Bleed | Column outcome |
|------|------|---------|-------|----------------|
| ana-eng004 | Move-A flip target | **6/6** | 0 | preserve-all-columns (×6) |
| quickbooks002 | Move-B stabilize + h0045↔h0055 collision | **6/6** | 0 | drop-feature-keep-base (×6) |
| quickbooks003 | Move-B stabilize + h0045↔h0055 collision | **6/6** | 0 | drop-feature-keep-base (×6) |
| ana-eng003 | Move-A must-hold (h0055 base case, single upstream) | 6/6 | 0 | preserve-all-columns (×6) |
| airbnb005 | h0053 collision pair | 6/6 | 0 | (inner-join scope; preserve-columns silent) |
| airbnb009 | h0050↔h0053 collision | 6/6 | 0 | coverage-repair; per-key silent |
| ana-eng007 | generalization watch | 0/6 | 0 | type-cast repair (id→STRING), NOT an OBT build → preserve-columns correctly silent |
| ana-eng007-medium | generalization watch | 2/6 | 0 | ambiguous (missing-model build) — unreliable flip |

## Interpretation

- **Move A (flip) — STRONG.** ana-eng004 routes 6/6 to the widened preserve-columns rule and preserves
  all columns from the fact⋈dim OBT join (the agents specifically note adding the omitted
  dim_products.attachments so all upstream cols carry through). It is a 0/23 stable-FAIL with a clear
  column-preservation fix, so the decision tendency + artifact shape both point at the grader's target.
- **Move B (stabilize) — STRONG.** Under the new worked example qb002/qb003 both go 6/6 to
  `drop-feature-keep-base` (keep department_id, drop only department_name) — a decisive shift away from
  r1's over-drop coin-flip that cost the 35→32 gap.
- **Move-A bleed tripwire — CLEAN.** The widened "join" precondition fired on ZERO feature-removal draws
  (qb002/qb003 bleed = 0; preserve-columns never appeared there). airbnb005 still per-key inner-join,
  airbnb009 still coverage-repair. Every collision pair held.
- **Honest soft spot (harmless):** the ana-eng007/-medium "generalization watch" tasks are DIFFERENT
  failure modes (ana-eng007 = a string/numeric type-cast repair; -medium = a missing-model build), so
  the widened rule won't reliably flip them. They are FAIL at baseline, so this is no-regression, just
  no bonus — the durable margin must come from ana-eng004 (+1) + the qb stabilization, exactly as the
  hypothesis stated (it never promised ana-eng007).
- **Caveat (method):** estimates decision tendency, not pass rate. The real smoke confirms the committed
  artifacts (ana-eng004 full-column OBT; qb002/003 keep-department_id) pass the hidden grader.

Raw per-draw edits: workflow output `w5rtbxrb6`.
