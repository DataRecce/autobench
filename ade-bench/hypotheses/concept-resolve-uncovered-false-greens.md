---
title: Resolve the baseline false-green failures that no hypothesis yet targets
status: expanded
kind: concept
source: evidence re-audit of the @baseline run (622bdedac572b479, 31/48) following docs/baseline-validation-self-anchored-false-green.md — h0009/h0010 only target ~6 of the 17 failures; 12 are uncovered.
started: 2026-06-04T13:40:51Z
completed: 2026-06-04T13:40:51Z
verdict:
---

## Direction

The baseline false-green finding (`docs/baseline-validation-self-anchored-false-green.md`)
proved that all 17 `@baseline` failures are false-greens — the solver's own check reports
clean while the hidden oracle finds the answer wrong — and that only two fix families ever
work: **independent checks** (reconcile to the raw source a different way, as `f1007-hard`
did) and **upstream/generative fixes** (get the model right before the bug is born). The
self-verification family on Validation/Finalization is dead (h0006/h0007/h0008).

h0009 (package fidelity) and h0010 (grain spine) only target ~6 of the 17 failures. A direct
evidence re-audit of the **12 uncovered** failing transcripts (airbnb007, airbnb009,
ana-eng004, ana-eng006, ana-eng007, ana-eng007-medium, asana005-hard, f1002, f1006, f1011,
intercom002, quickbooks001) surfaced four distinct, attackable root causes — including one
(**too-few output columns**, 3 tasks) the prose-only report never named, and one
(**stopped at compile-green / incomplete deliverable set**, quickbooks001) it flagged only in
passing. intercom002 is a grain-spine sibling already in h0010's family; the rest cluster as:

1. **Missing output columns** (ana-eng004, f1002, ana-eng007-medium) — equality test ERRORs
   "has less columns than solution"; a column-set contract is genuinely catchable.
2. **Value divergence, shape right** (ana-eng006/007, airbnb007, asana005-hard, f1006,
   airbnb009) — the heavyweight cluster; only an *independent* recompute can catch it.
3. **Incomplete deliverable set** (quickbooks001) — fixed the visible compile error, project
   went green, never built the models the oracle grades.
4. **Analytical-answer guess** (f1011) — included an option on plausibility without an
   independent per-claim query.

Each fans out to one generative-or-independent solver-README change, one stage, leak-guard
intact: h0011 (full-column-set, Implementation), h0012 (independent recompute, Validation),
h0013 (complete-deliverable, Exploration), h0014 (per-claim evidence, Implementation). The
count is earned from the evidence clusters — not a chosen number.
