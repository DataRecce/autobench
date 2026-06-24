---
id: spd0002
title: Build EVERY result table the instruction enumerates (completeness lever)
status: propose
kind: hypothesis
source: re-scoped from spd0001 anchor deep-dive (the original materialization framing is dead — 0 ephemeral fails board-wide; re-aimed at the 3 tractable incomplete-deliverable fails)
started: 2026-06-24T14:34:28Z
completed:
verdict:
score: 0.9
worktree:
---

## Hypothesis

> **Re-scope note.** This hypothesis was originally a *materialization* lever (force every named
> target to a BASE TABLE; targeting chinook001). The spd0001 anchor full-board read **killed that
> framing**: the output-contract seed README already lands BASE-TABLE materialization on 100% of fails
> (0 ephemeral board-wide), and chinook001 turned out to be a gold-side packaging defect, not an
> ephemeral miss. So the materialization lever has **no live target**. Re-aimed here at the one
> tractable, artifact-checkable failure family the anchor surfaced.

The anchor showed the solver sometimes **builds only some of the result tables the instruction
enumerates** — it stops after the first deliverable when the task asks for several. Confirmed on the
committed artifacts:
- **intercom001** — gold requires `intercom__company_metrics` + `intercom__admin_metrics`; the agent
  built only `intercom__admin_metrics`.
- **analytics_engineering001** — gold requires `fact_purchase_order` + `obt_customer_reporting`; the
  agent built only `obt_customer_reporting`.

Both are convention-correct on what they *did* build — they are pure **completeness** misses, not
value misses. (The gold table *names* are not visible to the agent, so the lever must work from the
instruction's own enumeration of deliverables, not from the gold list.)

**Claim:** a single solver-README rule — *"Before finishing, re-read the instruction and enumerate
EVERY distinct result table / deliverable it describes (a dimension AND a fact AND a one-big-table are
separate deliverables). Build a separate materialized base table for EACH enumerated deliverable.
Confirm the count of built target tables equals the count of deliverables the instruction names —
do not stop after the first."* — flips intercom001 and analytics_engineering001 FAIL→PASS by making
the solver build the second required table.

This is a **completeness check**, not a value-rewrite (G10-safe: it only *adds* missing deliverables;
it cannot turn a correct table's values wrong). It is mildly **generative** (the "enumerate
deliverables" reflex fires on every task), so the smoke set carries a regression panel of
currently-passing tasks — a single-deliverable passer must NOT sprout spurious extra tables, and a
multi-task family passer guards the most-at-risk shape.

Target tasks: `spider2-dbt-intercom001`, `spider2-dbt-analytics_engineering001`. Stretch/optional
3rd: `spider2-dbt-movie_recomm001` (a wrong-name/scope miss — may or may not be the same family;
include only if the propose-gate read supports it).

## Pre-smoke Decision-Fork Probe

Not run (no local fork harness). The fork is well-identified by the anchor committed artifacts: in
both target cells the model SQL for the built table is correct and materialized as a base table; the
sole gap is a *missing second model*. The README wording above directly addresses that mechanism
(enumerate-and-count deliverables). Proxy evidence deferred to the smoke; the fork is concrete enough
to smoke directly.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `agent.solver_workflow:`.**
Verified by: `diff specs/full-baseline.yaml specs/spd0002-build-every-deliverable.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites `rk audit --policy strict` on the same run-dir.

**AC-3 — intercom001 and/or analytics_engineering001 flip FAIL→PASS because the previously-missing
second gold table (`intercom__company_metrics` / `fact_purchase_order`) now exists as a base table in
the built DuckDB (committed-artifact confirmation), and the passing sentinels hold (no spurious extra
tables, no regression).**

## Gatekeeper review

## Smoke result

Proposed smoke set: targets + regression panel (re-confirm `@baseline` rewards at the propose gate —
`@baseline` = `runs/spider2-dbt-full-baseline/13fb630e2cae3eb8`, 19/61).

| Task | Baseline | Should pass in smoke? | Role |
|---|---|---|---|
| spider2-dbt-intercom001 | ❌ FAIL | 🎯 flip to PASS | Target — built 1 of 2 required tables (missing `intercom__company_metrics`). |
| spider2-dbt-analytics_engineering001 | ❌ FAIL | 🎯 flip to PASS | Target — built 1 of 2 required tables (missing `fact_purchase_order`). |
| spider2-dbt-app_reporting002 | ✅ PASS | ✅ must stay PASS | Perturbable canary — `app_reporting` is a multi-task family; guards the most-at-risk multi-deliverable shape. |
| spider2-dbt-mrr001 | ✅ PASS | ✅ must stay PASS | Perturbable canary — `mrr` family passer (mrr001+mrr002 both pass). |
| spider2-dbt-activity001 | ✅ PASS | ✅ must stay PASS | Sentinel — single-deliverable passer; must NOT sprout spurious extra tables. |

Net hoped-for: flip ≥1 of the 2 targets, lose zero sentinels/canaries. (movie_recomm001 omitted from the
smoke unless the propose read confirms it is the same completeness family rather than a value/scope miss.)

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
