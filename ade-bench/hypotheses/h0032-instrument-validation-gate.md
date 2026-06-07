---
id: h0032
title: E0 -- Instrument-validation gate; an independent check must fire on an injected error and stay silent on a known-good before it touches a real task
status: propose
kind: hypothesis
source: _proposal/oracle-problem-systematic-program.md (E0 instrument-control); captain go-ahead 2026-06-07
started: 2026-06-07T10:11:20Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

*(Seeded by the FO from the proposal; the propose stage turns this into the concrete harness.)*

Before any independent "second-path" check is trusted on a real ade-bench task, it MUST be proven
**two-sided discriminating** on a controlled fixture: it **FIRES on a known injected error** and stays
**SILENT on a known-good**. A check that cannot demonstrably fire is **inert** (the h0010/h0016 prose
signature); a check that fires on a known-good is **correlated / self-anchored** (the h0008/h0012
signature). E0 is a per-check GATE, not a pass-rate lever -- its job is to make every downstream flip
(E1/h0030, E4/h0021, E5) trustworthy. Direct flip contribution: **0**.

**Method.** Take 2-3 currently-PASSING `@baseline` models. On a copy, inject a known error
(drop a parent key -> grain shortfall; cast a column to the wrong dtype; remove a calendar day). Run
each candidate independent dbt check against BOTH the good and the injected copy:

- raw-parent `output COUNT(*) == COUNT(DISTINCT parent_key)` reconcile (gates **E1 / h0030**, priority),
- `information_schema` dtype-vs-declared-contract assertion (gates **E4**),
- ref-graph / `_existence` completeness check (gates **E5**).

This is an **instrument-validation harness, NOT a solver-README change** -- it may run offline rather
than as a 48-task `rk run`. The propose stage authors the concrete fixtures + harness; the smoke runs
the 2x2.

## Acceptance criteria

**AC-1 -- Two-sided discrimination per check.** For each candidate check, a recorded 2x2:
`fires-on-injected = TRUE` AND `fires-on-known-good = FALSE`. A check failing either side is KILLED for
its downstream experiment only (silent-on-injected = inert; fires-on-known-good = correlated); other
experiments proceed.

**AC-2 -- Independent, not self-anchored.** Each check recomputes from the RAW SOURCE / a structural
relation, never from the model's own CTE or the solver's framing (the sharp test,
`_artifacts/verification-without-oracle.md`).

**AC-3 -- Machine-readable result.** The per-check 2x2 is saved as an artifact so downstream propose
gates can cite "E0-cleared" for the check they rely on.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
