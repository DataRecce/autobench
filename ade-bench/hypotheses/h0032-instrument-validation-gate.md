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

**This is the INDEPENDENCE sanity-check (the sharp test from
`_artifacts/verification-without-oracle.md`), per check — NOT a leak-guard review.** E0 ships
nothing to the solver, so there is no README/spec/ground-truth-leak surface to audit. Sharp test:
*reads the RAW source / a must-hold structural relation → independent (keep); re-runs the model's
own CTE or the solver's framing → correlated (kill).*

| Check (gates) | Reads from | Independent? | Verdict |
|---|---|---|---|
| raw-parent row-count reconcile — `finishes_by_driver`, `driver_wins_by_season` (**E1/h0030**) | RAW `results`/`races`/`drivers` (native cols `driverId`,`year`), `COUNT(DISTINCT key)` | YES — never touches the model CTE nor the hidden `solution__` oracle seed | **independent — keep** |
| info_schema dtype-vs-**declared-contract** (**E4**) | the model yml `data_type:` / `contract: enforced` | N/A — **the artifact does not exist** (grep across all of `shared/projects/dbt/`: zero `data_type:`, zero `contract:`) | **as-specified: unavailable.** Deriving "expected" dtype from the model SQL would be CORRELATED. |
| info_schema dtype-vs-**raw-source** (E4 viable substitute) | RAW source column dtype via `describe`/`information_schema` | YES, but NARROW — applies only to pass-through key/identity cols (2 of 33 in `finishes_by_driver`); the 31 derived aggregates have no raw dtype oracle | **independent — keep (re-spec E4 to this variant)** |
| ref-graph / `_existence` completeness (**E5**) | RAW `results`+`drivers` required key-set, anti-joined to output | YES — recomputes the key-set from raw, never from `solution__` (which is the leak the verifier hides) nor the model CTE | **independent — keep** |

**Load-bearing caveat (the h0012 trap), proved by adversarial probe A in the harness:** the reconcile
is sound *only* if it reads the **immutable raw source**. If the downstream E1 check instead reads a
**solver-rebuilt intermediate** (e.g. a `stg_*` the solver itself produced), a correlated error in
that intermediate is re-introduced into the check and it **false-greens** (probe A: a polluted parent
gives output=737 and a correlated read=737 → MATCH, while the true-raw read=860 → correctly FIRES).
E1/h0030 MUST bind its raw-parent read to `{{ source(...) }}` / the original loaded tables, not to any
model the solver can overwrite.

## Smoke result

**Offline instrument-validation harness** (NOT a 48-task `rk run`):
`_artifacts/h0032-e0-harness/harness.py` → 2x2 JSON `_artifacts/h0032-e0-harness/result_2x2.json`.
Fixture = the real ade-bench **f1 DuckDB** (downloaded from the `databases` GitHub release), which
ships the RAW source tables *and* the canonical currently-PASSING `@baseline` model outputs
side-by-side. Known-good = the canonical model table; injected = a mutated copy (added filter drops a
parent-key cohort; cast a key column to VARCHAR; remove a whole season slice). Each check reads the
RAW source independently and runs against BOTH copies.

**The 2x2 (AC-1 — want `fires-on-injected=TRUE` AND `fires-on-known-good=FALSE`):**

| Check (gates) | Model | known-good fires? | injected fires? | Verdict |
|---|---|---|---|---|
| raw-parent row-count reconcile | `finishes_by_driver` | FALSE (860==860) | **TRUE** (813 vs 860, Δ−47) | **CLEARED** |
| raw-parent row-count reconcile | `driver_wins_by_season` | FALSE (403==403) | **TRUE** (396 vs 403, Δ−7) | **CLEARED** |
| info_schema dtype vs **raw source** | `finishes_by_driver.driver_id` | FALSE (INTEGER==INTEGER) | **TRUE** (VARCHAR≠INTEGER) | **CLEARED** (narrow; pass-through cols only) |
| ref-graph / `_existence` completeness | `finishes_by_driver` | FALSE (0 missing) | **TRUE** (47 keys missing) | **CLEARED** |
| info_schema dtype vs **declared contract** (E4 as literally specified) | — | n/a | n/a | **KILLED — artifact does not exist** (no `data_type:`/`contract:` anywhere in the corpus) |

**Adversarial probes (characterise each cleared check's blind spot, so the CLEARED verdict is earned):**

- **correlated-error trap (probe A):** if the reconcile reads a solver-rebuilt intermediate instead of
  the raw source, it false-greens (polluted output 737 == correlated read 737); reading the true raw
  source fires (737 ≠ 860). → **E1's raw read must bind to `{{ source() }}`.**
- **count blind spot (probe B):** a drop-N-add-N mutation keeps `COUNT(*)` equal (860==860) so the
  count reconcile is BLIND, but the completeness anti-join FIRES (5 keys missing). → **the E1 count
  reconcile and the E5 completeness check are complementary, not redundant; E1 should pair the count
  with the key-level anti-join to close this gap.**

**Cleared (safe for downstream) — AC-1+AC-2+AC-3 met:**
- **E1/h0030** raw-parent reconcile — **CLEARED**, with the binding caveat above.
- **E5** ref-graph/`_existence` completeness — **CLEARED**.
- **E4** — the *declared-contract* form is **KILLED (unavailable)**; the *dtype-vs-raw-source* form is
  **CLEARED but narrow** (only pass-through key/identity columns; derived aggregates have no raw
  oracle). E4 should be re-specified to the raw-source variant before it is trusted.

(AC-3) Machine-readable artifact: `_artifacts/h0032-e0-harness/result_2x2.json`
(`checks[]` + `adversarial{}`), regenerable via `python3 _artifacts/h0032-e0-harness/harness.py`.

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: Build the instrument-validation harness for the RAW-PARENT ROW-COUNT RECONCILE check (PRIORITY)
  `_artifacts/h0032-e0-harness/harness.py`; 2 passing @baseline models (`finishes_by_driver`, `driver_wins_by_season`); known-good vs injected-parent-key-drop; reconcile reads RAW `results`/`races` (native cols), not the model CTE.
- DONE: Record a machine-readable 2x2 per candidate check + tag CLEARED/KILLED + write into entity + save artifact
  `result_2x2.json` (`checks[]`+`adversarial{}`); 2x2 table in `## Smoke result`. Reconcile (E1) ×2 CLEARED; completeness (E5) CLEARED; dtype-vs-raw (E4 substitute) CLEARED-narrow; dtype-vs-declared-contract (E4 as-specified) KILLED — artifact absent.
- DONE: Independence sanity-check (the sharp test) for each check
  `## Gatekeeper review` table; all kept checks recompute from RAW source / a must-hold relation, never `solution__` (the hidden oracle) nor the model CTE. Adversarial probe A proves independence is load-bearing (correlated read false-greens 737==737; raw read fires).
- SKIPPED: standard propose Outputs (fork solver README, full/smoke rk spec, 48-task run, leak-guard gatekeeper)
  Per dispatch: E0 DEVIATES — it is an OFFLINE instrument-validation harness that ships nothing to the solver; no README/spec/leak surface exists.

### Summary

E0 is a per-check instrument gate, not a pass-rate lever. Built an offline harness over the real f1
DuckDB (raw source + canonical @baseline outputs ship together), validating each candidate
independent check is two-sided discriminating. PRIORITY raw-parent reconcile (E1/h0030) CLEARED on two
models; E5 completeness CLEARED; E4's *declared-contract* form is KILLED (no `data_type:`/`contract:`
exists anywhere in the corpus) but a *dtype-vs-raw-source* substitute CLEARED narrowly (pass-through
key cols only). Two adversarial probes pin the load-bearing caveats: E1 must read the immutable
`{{ source() }}` (a solver-rebuilt intermediate re-introduces correlated error and false-greens), and
the count reconcile is blind to drop-N-add-N (E5's key-level anti-join is the complement). Net for the
gate: E1/h0030's reconcile is trustworthy enough to proceed, *provided* it binds its raw read to the
source and pairs the count with the completeness anti-join.
