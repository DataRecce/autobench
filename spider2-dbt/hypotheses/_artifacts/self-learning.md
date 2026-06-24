# spider2-dbt autoresearch — self-learning log

One line per concluded hypothesis (and any durable cross-cutting lesson). Append on `conclude`.
The entity body is the source of truth; this is the scannable index.

## Pre-loop standups (before any scored full board)

- **smoke6 (ade README, 0/6).** The ade `@baseline` README is the WRONG starting point — it is tuned
  for repair/refactor ("do not create an answer file", "preserve structure") and gives the solver no
  spider2-dbt output-table contract, so it builds plausibly-named models that miss the gold table name
  (chinook built `customer`, gold wants `dim_customer`) or miss exact columns. Wiring proven
  end-to-end. (`docs/smoke6-2026-06-24.md`)
- **smoke6 output-contract (2/6, was 0/6).** A spider2-dbt-tuned README centering the output-table
  contract (build NEW materialized models; name by project convention `dim_`/`fct_`/`obt_`/
  `<pkg>__<entity>`; build into `main`; match key+columns+grain) flipped activity001 + f1001 and
  produced convention-correct names in 6/6. The **naming lever is real and README-steerable.**
  (`docs/smoke6-output-contract-2026-06-24.md`)
- **Residual failure split (post output-contract):**
  - **ephemeral-not-materialized** (chinook001) — correct names built but placed under an
    `ephemeral`-configured `models/intermediate/` → compiled to CTEs, never tables → invisible to the
    verifier. README-addressable → seeded as **spd0002**.
  - **wrong-columns/values** (jira001 / tpch001 / xero_new001) — correct table name, wrong analytic
    result. Genuine benchmark difficulty; no cheap README lever → seeded as concept **spd0003**.
- **Self-anchored false-green recurs here too.** The agent self-validated only `obt_invoice` existed
  (one of three targets) and reported success — the same false-green seen in ade-bench/DAB. Validation
  levers must check structural invariants (every named target exists as a base table), not the
  solver's own re-derivation.

## Concluded hypotheses

<!-- spd<NNNN> — VERDICT (one-line lesson). Append on conclude. -->
