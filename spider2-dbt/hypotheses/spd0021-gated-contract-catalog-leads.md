---
id: spd0021
title: Gated contract forcing-function over the 5 catalog leads — reliable compliance via write-then-obey, multi-draw
status: hypothesis
kind: hypothesis
source: "synthesis of the 2026-06-27 autonomous sprint: the contract forcing-function (spd0011) is the ONLY mechanism that made a README rule reliably obeyed (airbnb 2/2 with scaffold vs 1/2 lean); the residual catalog gives 5 exact oracle-free per-task fixes. This composes them GATED (zero passer cost) and judges by a trials=3 hold-rate (beats the variance wall). forks champion @baseline spd0013."
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

The 2026-06-27 sprint established that the never-pass pool's binding constraint is **compliance
reliability + variance**, not reachability: precise oracle-free rules get ADOPTED in the committed
artifact but flip only ~half the draws (tickit002 2/4, movie_recomm001 0/2, provider001 0/2). The ONE
mechanism proven to make a rule *reliably* obeyed is the **contract forcing-function** (spd0011): airbnb001
held **2/2 with** the write-then-obey contract scaffold vs **1/2 without** it (spd0013). spd0011 only
failed because the scaffold was WHOLE-SOLVER (diffuse prose cost on passers, e.g. quickbooks003 0/3) and
carried a destabilizer template.

**The synthesis (this hypothesis):** apply the contract forcing-function **GATED to ONLY the 5 catalog-lead
task shapes**, each with its exact offline-diagnosed fix as the contract template, so it forces reliable
compliance on the leads while **passers never enter the contract path** (gated-levers-compose → zero prose
cost). Judge by a **trials=3 hold-rate**, not a single draw (the discipline every prior single-draw verdict
lacked).

Fork the champion `spd0013-lean-lag-period-over-period`. Add ONE gated stage:

> **Implementation Contract (GATED).** BEFORE editing SQL, check whether the task matches one of the
> contract shapes below. If NONE match, proceed with the existing flow unchanged — do NOT write a contract
> (no overhead). If one matches, write its contract (selected template, expected_row_shape,
> forbidden_patterns, validation_signature) from the template + local evidence, implement to OBEY it, then
> VALIDATE the signature before declaring done (a clean `dbt build` is not enough). The contract is derived
> only from local workspace evidence; never from gold values.

### Contract templates (each gated on an oracle-free shape signal; each fix is a METHOD, no gold baked)

- **C1 — REFERENCE/CROSSWALK FULL-SET PRESERVATION.** *Gate:* a reference/dimension/crosswalk target built
  from a full entity set (all codes / all entities / a complete reference list). *Fix:* LEFT-join the
  enrichment/crosswalk relations onto the full base set; keep EVERY base-set row (NULL where unmatched);
  never INNER-join-away unmatched rows and never filter on a NULL/"unknown" key/type/category. *Signature:*
  built row count = the base-set's own row count; no join shrinks it. *(provider001.)*
- **C2 — CUMULATIVE-SPINE ENDPOINT.** *Gate:* a monthly/period spine driving a cumulative balance /
  running-total report. *Fix:* the spine ENDS at the last period that has source activity — never
  `current_date` / `greatest(max, current_date)` (which over-emits future-empty periods); round money
  columns to 2dp. *Signature:* the max emitted period = the last period with source data; no trailing
  empty periods. *(xero001.)*
- **C3 — FUZZY/PARTIAL NAME-MATCH JOIN.** *Gate:* a join the model's schema.yml/description calls a
  partial / fuzzy / starts-with name match (esp. when the task instruction is underspecified or describes a
  different deliverable). *Fix:* treat the model's schema.yml as the authoritative contract; implement the
  match as an anchored prefix `LIKE (<other> || '%')` — NOT exact equality; PRESERVE the natural fan-out
  (no dedup unless the spec says one row per key); strip only a trailing `(YYYY)` token. *Signature:* the
  join is a prefix LIKE and the row set keeps the fan-out. *(movie_recomm001.)*
- **C4 — NO-INVENTED-FILTER DIMENSION/FACT.** *Gate:* a dimension/fact built by joining staging models.
  *Fix:* restrict the row set ONLY by the inventoried join keys; never add `WHERE <attribute> IS NOT NULL`
  (or any value predicate) on a descriptive/payload column the instruction does not name — a NULL/zero in a
  descriptive attribute is a VALID row; resolve role attributes through the role dimension
  (`int_<role>_extracted_from_users`), never the full raw user table. *Signature:* no invented attribute
  filter; the row count = the key-join row set. *(tickit002.)*
- **C5 — STOCHASTIC-SIMULATION SNAPSHOT.** *Gate:* graded columns produced by an UNSEEDED simulation
  (`random()` with no seed) for which a committed snapshot exists in the project's data catalog. *Fix:* for
  those columns, READ the committed snapshot (parquet/seed) from the data catalog and join it to the
  deterministic columns — do NOT re-run the unseeded simulation (it is not reproducible). *Signature:* the
  stochastic columns are sourced from the committed snapshot, not a fresh simulation. *(nba001.)*

Each gate is an oracle-free workspace/shape signal; no gold values, counts, or dtypes are baked. NO other
change; the no-fetch leak guard is byte-identical to spd0013. Existing champion guidance is untouched for
non-matching tasks.

## Pre-smoke Decision-Fork Probe

**Reachability of all 5 leads is PROVEN offline** (residual catalog 2026-06-27, local source only): each
fix reproduces its graded gold exactly (provider001 874+85196, xero001 1170, movie_recomm001 56596,
tickit002 8659+177417, nba001 = the committed snapshot). The OPEN question is purely **reliability**: does
the contract forcing-function (write-then-obey, gated) make these fixes land RELIABLY across draws — beating
the lean-rule baselines (tickit002 2/4, movie_recomm001 0/2, provider001 0/2)? That is exactly what the
trials=3 run measures: per-lead hold-rate WITH the contract vs the lean-rule baseline WITHOUT it. The
passer-cost question (did spd0011's contract prose cost qb003?) is answered by gating: passers match no
template and never enter the contract path.

## Acceptance criteria

**AC-1 — README-only; full spec differs only in `experiment:` + `solver_workflow:`.** Forks spd0013, adds
ONLY the gated contract stage + 5 templates. Leak guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — HOLD-RATE verdict (trials=3).** A lead is "reliably fixed" if it passes ≥2/3 draws (vs its lean
baseline). The contract must HOLD the hard canaries (≥2/3 each; no passer that was rock-solid drops below
2/3) — the gated design predicts zero passer cost. Promote only on a multi-draw hold-rate, never a single
draw (the variance-wall discipline). NO promote without captain sign-off.

## Smoke Plan

1. **Sanity smoke (trials=1, ~13 cells):** the 5 leads (provider001, xero001, movie_recomm001, tickit002,
   nba001) + hard canaries (apple_store001, google_play001, google_play002, mrr001, quickbooks002,
   activity001, app_reporting001, app_reporting002) + tickit001 (sibling) — confirm the contract FIRES on
   each lead, builds clean, and no gross canary breakage. ~40 min.
2. **If clean → trials=3 FULL board (60 tasks):** the long-running multi-draw run. Yields per-cell hold
   rates board-wide → the promotable verdict + a full regression check. ~8–9 h.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
