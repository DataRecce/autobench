---
id: spd0009
title: Axis-2 G1 — SPINE_COMPLETENESS (drive daily/rollup/balance-sheet/enhanced targets from the spine/dimension, left-join facts, carry balances forward, keep NULL)
status: propose
kind: hypothesis
source: "resolution-survey ranked-backlog #4; forks CHAMPION spd0008 (24/60); Axis-2 G1 spine is the one knob; 2-step smoke (small gate-isolation -> large at-scale)" #4 — the BINDING-CONSTRAINT experiment; stacks on the spd0008 champion
started: 2026-06-25
completed:
verdict:
score: 0.7
worktree:
---

## Hypothesis

The largest under-emit cluster (12 tasks): the solver drove the row grain from fact ACTIVITY
instead of from a calendar-spine / full dimension, so no-activity periods/keys are dropped.
This is the **literal inverse** of the default README grain rule ("drive from fact activity;
do not pad zero-activity rows") that the **19 current passers depend on** — so this is the
highest-risk, highest-fanout lever and the program's binding constraint. The whole hypothesis
is whether a TIGHT precondition gate isolates the spine rule to the targets WITHOUT regressing
the per-key-aggregate passers.

**The single README change:** add **Axis-2 rule G1**, fired ONLY when an oracle-free
precondition holds:
- (a) target name matches `/_daily_|_rollup|_balance_sheet|_snapshot|_overview/` AND a
  date-spine model (`int_*__calendar_spine` / `int_*date_spine`) ships in `models/`; OR
- (b) the instruction carries completeness verbs ("each / every / for all / map X to Y /
  balance … on a monthly basis") over a NAMED reference/dimension source whose rowcount equals
  the target's expected grain; OR
- (c) target matches the Fivetran `*_enhanced` / `*_metrics` / `*__<entity>` dimension
  convention AND a same-named source dimension table exists.

When fired: DRIVE FROM the spine/dimension (left-join facts), carry cumulative balances forward
across zero-activity periods (`SUM() OVER (PARTITION BY entity ORDER BY date_month)`), add
package-standard synthetic rows (e.g. Retained Earnings = −cumulative P&L), leave metric columns
NULL on no-activity rows (do NOT coalesce-to-0 unless the spec says zero-fill),
`ROUND(money, 2)`. When NOT fired, the default fact-driven rule stays as-is — **protecting the
19 passers; the gate is the isolation.**

**Target tasks (REACHABLE_VERIFIED, 12):** salesforce001, recharge002, xero001, xero_new001,
xero_new002, jira001, marketo001, intercom001, provider001, hive001, flicks001, playbook002.

## Pre-smoke Decision-Fork Probe

Offline-verified (survey wf_32b5a457-a96): each target reconstructed from the spine/dimension
side passed `duckdb_match.py` — e.g. salesforce001 daily-spine grain, xero balance-sheet 60-month
carry-forward, jira `project_enhanced` full-dimension. Reachability is NOT in question; this
smoke is **purely a steerability + canary-isolation test**: does the gated spine rule fire on
`_daily_`/`_balance_sheet`/`_enhanced` targets WITHOUT over-emitting on activity-grained passers?
**A canary regression here is a NO-GO regardless of target flips** — the gate must hold.

## Acceptance criteria

**AC-1** — README-only; spec diff = the two allowed fields.
**AC-2** — scores paired with clean strict audits.
**AC-3** — paired `rk runs diff` vs the spd0008 champion. **Promotion requires net ≥ +1 with
ZERO regression on the per-key-aggregate passers** (smoke carries ≥2 perturbable passer canaries
that MUST stay PASS). Secondary NULL-vs-zero-fill check: the rule must not coalesce-to-0 where
gold keeps NULL (salesforce001/scd001).

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
