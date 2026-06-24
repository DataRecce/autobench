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

- **spd0001 — PASSED (anchor; @baseline = 19/61 = 0.3115, clean audit).** Established the champion. The
  output-contract seed README has fully solved the SHAPE problem: every one of the 42 fails builds the
  correctly-named gold table as a BASE TABLE — **0 ephemeral, 0 wrong-materialization board-wide**, so
  the seeded materialization lever (old spd0002) has NO live target and is dead-on-arrival. The board's
  failure is almost entirely the **oracle-blind wall**: 38/42 fails are wrong-columns-or-grain — correct
  table, wrong analytic content, self-validated green against the agent's own reading of an
  under-specified instruction (no gold to check against; same wall as ade-bench/DAB). Only **3** fails
  are tractable (wrong-table-name / built only 1 of 2 required gold tables: intercom001,
  analytics_engineering001, movie_recomm001). **One smoke→full correction:** chinook001 is NOT ephemeral
  — it's a gold-side packaging defect (gold DB ships only raw sources, never the dim/fct/obt tables), a
  non-signal. **Lesson:** a 6-task smoke can mis-attribute a failure class; the full-board committed-
  artifact read is what reveals the true bucket distribution and kills/keeps a lever family.
