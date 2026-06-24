---
id: spd0002
title: Materialize every named target as a BASE TABLE and validate each exists
status: hypothesis
kind: hypothesis
source: commission seed (smoke6-output-contract deep-dive, chinook001 next-lever #1)
started:
completed:
verdict:
score: 0.9
worktree:
---

## Hypothesis

The output-contract solver already produces **convention-correct table names** (smoke#2: chinook001
built `dim_customer` / `fct_invoice` / `obt_invoice`), but chinook001 still scored 0.0 because two of
the three targets were placed under `models/intermediate/`, which the project configures
`materialized: ephemeral`. Ephemeral models compile to CTEs and **never become tables in the output
DuckDB** — so the verifier saw only `obt_invoice` and reported `dim_customer does not exist`. The
agent self-validated only that one table existed (incomplete check = self-anchored false-green).

**Claim:** a single solver-README rule — *"EVERY named target table must land as a BASE TABLE in the
output DuckDB. Never place a target model in an `ephemeral`/intermediate-configured directory; if a
target would inherit `ephemeral`, set `{{ config(materialized='table') }}` on it. Before finishing,
VALIDATE that EACH named target table (not just one) exists as a base table in the built DuckDB"* —
flips chinook001 FAIL→PASS by materializing `dim_customer` and `fct_invoice` as tables.

This is a **generative** lever (the rule fires on every task, not gated to chinook), so the smoke set
carries a regression panel of perturbable passers.

Target task: `spider2-dbt-chinook001`.

## Pre-smoke Decision-Fork Probe

Not run (no local fork harness yet). The fork is well-identified by the smoke#2 committed artifact:
the model SQL existed and was correct, the failure was purely the `ephemeral` materialization
inherited from `models/intermediate/`. The README wording above directly addresses the observed
mechanism. Proxy evidence deferred to the smoke itself; the fork is concrete enough to smoke directly.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `agent.solver_workflow:`.**
Verified by: `diff specs/full-baseline.yaml specs/spd0002-materialize-every-target-table.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites `rk audit --policy strict` on the same run-dir.

**AC-3 — chinook001 flips FAIL→PASS because `dim_customer` and `fct_invoice` now exist as base tables
in the built DuckDB (committed-artifact confirmation), and the two passing sentinels (activity001,
f1001) hold.**

## Gatekeeper review

## Smoke result

Proposed smoke set: targets + regression panel.

| Task | Baseline | Should pass in smoke? | Role |
|---|---|---|---|
| spider2-dbt-chinook001 | ❌ FAIL | 🎯 flip to PASS | Target — ephemeral-materialization miss this lever should fix. |
| spider2-dbt-activity001 | ✅ PASS | ✅ must stay PASS | Sentinel — known passer; a generative rule could perturb it. |
| spider2-dbt-f1001 | ✅ PASS | ✅ must stay PASS | Sentinel — known passer (other family). |
| spider2-dbt-jira001 | ❌ FAIL | (watch) | Hard-core control — correct name, wrong values; should NOT spuriously flip. |
| spider2-dbt-tpch001 | ❌ FAIL | (watch) | Hard-core control. |
| spider2-dbt-xero_new001 | ❌ FAIL | (watch) | Hard-core control. |

(Resolve actual `@baseline` rewards once spd0001 establishes the champion; the ✅/❌ above are from the
pre-anchor smoke#2 and must be re-confirmed against `@baseline` at the propose gate.)

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
