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

- **spd0002 — REJECTED at smoke (completeness/build-every-deliverable lever; 2/5, clean audit).**
  A generative "enumerate EVERY result table the instruction names; build a base table for each;
  confirm built-count == enumerated-count" rule. NO-GO on both axes: **0/2 targets flipped**
  (intercom001 INERT — count-reflex re-counted to one with no worked skeleton, the G7 risk realized;
  analytics_engineering001 FIRED-but-fail — built deliverable #2 but the new `fact_purchase_order`
  collapsed deliverable #1's row set 55→14) AND a **canary REGRESSED** (mrr001 PASS→FAIL: the rule
  licensed a spurious `util_months` month-spine that zero-filled ~7 phantom rows, 410→417, violating
  the anti-zero-fill contract). **Lesson:** count-completeness ≠ row-set-correctness; a generative
  "build everything" reflex has no oracle for correct SCOPE and structurally fights the row-set
  discipline — and the two failure modes are mutually exclusive to fix (a skeleton cures inertness but
  amplifies the over-fire bleed). The **completeness/enumerate-deliverables family is CLOSED** at
  gpt-5.5/xhigh. Refines spd0001: the "3 tractable" misses were not one closeable gap — pushing
  completeness makes the solver OVER-build and damages single-deliverable passers board-wide. Same
  wall as DAB's generative over-fire family ([[dab-readme-prose-output-contract-inert]],
  [[dab-determinism-lever-family-dead]]).
- **spd0011 — REJECTED / validated-not-promoted (Implementation Contract checkpoint; 2 smoke cycles, both clean, 10/12→8/12).** A pre-SQL contract checkpoint IS obeyed at gpt-5.5/codex (fire-and-obey, AC-2/AC-4 met across all 12 cells) — the FIRST hard counter to spider2-dbt's detected-but-not-obeyed wall (spd0006/spd0009) and the bankable win. But the contract's `G2_REPORT_RAW_GROUPING_HOLD` report-grain template is a net-negative destabilizer: it re-grains passers (recharge002 telemetry cyc1; quickbooks003 HARD-GATE 1.0→0.0 cyc2, committed-artifact proof "selected_rule G2_REPORT_RAW_GROUPING_HOLD; primary") with no compensating flip, even after a source-bounded-spine guard. airbnb001 never flipped: offline gold reconstruction (LOCAL source) proved the SOLE residual is the MOM column (gold=NULL) and it is README-fixable + oracle-free — gold MOM=NULL is `LAG()` over a single-window output (no prior row→NULL, == the scaffold's `wow_agg_reviews` sibling), so the fix is a derivation-METHOD constraint (LAG over the model's own output), NOT a soft "NULL-where-no-baseline" flag (the worker re-materialized a prior window from the 12-yr source and refused to NULL). → filed spd0012 (keep contract checkpoint + latest-window template w/ LAG-method MoM, DROP raw-grouping template).
- **spd0012 — REJECTED / validated-not-promoted (single-template contract checkpoint, LAG-over-own-output MoM; full 24/60 = @baseline, net +0).** Dropping the proven net-negative `G2_REPORT_RAW_GROUPING_HOLD` template and hardening the MoM sub-rule to a derivation-METHOD constraint FLIPPED airbnb001 0→1 ARTIFACT-REAL and DURABLE across two draws (smoke+full): committed `LAG(REVIEW_TOTALS,…) OVER (PARTITION BY REVIEW_SENTIMENT ORDER BY AGGREGATION_DATE)` over the model's OWN single-window output ⇒ MOM NULL by construction = gold, `selected_rule` fired. This is the program's FIRST value-definition flip made README-addressable through a METHOD (how to derive), vs spd0007's oracle-blind dtype/formula value-defs — the contract+method MECHANISM works and is bankable. BUT the whole-solver headline is net +0: every other moved cell (gains airport001/f1001/recharge001 + regressions marketo001/recharge002/retail001/f1003) selected `selected_rule: none` (no template) = variance/flake, and sap001 0→1 is the deterministic spd0010 FIXTURE repair (free to any solver on the repaired board ⇒ a fixture-corrected spd0008 ≈25/60 ⇒ spd0012 at 24 does NOT clear a fixture-corrected champion). quickbooks003 1→0 is 0/3 across all three contract-stage draws with `selected_rule: none` every time ⇒ suspected DIFFUSE cost of the heavy contract PROSE on a borderline passer (UNRESOLVED). **Lesson:** a durable, airtight artifact-attributable cell can still be NON-promotable when the headline is variance-swamped + fixture-confounded, AND a costly heavyweight vehicle (the contract checkpoint) may carry a diffuse cost on a marginal passer. @baseline UNCHANGED = spd0008 24/60. → filed spd0013 (lean-LAG isolation: does the inline rule flip airbnb001 WITHOUT the contract scaffold, and does quickbooks003 recover without the prose?).
