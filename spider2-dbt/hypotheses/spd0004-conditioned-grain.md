---
id: spd0004
title: Conditioned grain — PRESERVE-COVERAGE vs SCOPE-TO-ACTIVE classifier (fix the under-emit GRAIN family)
status: propose
kind: hypothesis
source: 42-task @baseline failure analysis (docs/failure-analysis-2026-06-24.md) — GRAIN is the largest addressable family
started: 2026-06-24T14:32:32Z
completed:
verdict:
score: 0.85
worktree:
---

## Hypothesis

The 42-task `@baseline` (19/61) failure analysis found **GRAIN is the dominant addressable failure
family (22/42), and 15 of those are UNDER-emitted** — the solver inner-joins / dedups / uses
activity-only rows when the gold wants full coverage (every entity, a continuous date spine,
pass-through unions). The cause is in the `@baseline` solver README itself: its grain rule is the
**blanket** *"build FROM the fact, INNER JOIN the dimension, do NOT LEFT JOIN and zero-fill"* — which
is correct for tpch001 (the lone over-emit/scope-to-active case) but **backwards for the 15
under-emit tasks**.

**Lever (single change vs `@baseline`):** replace the blanket grain rule with a **classifier** —
default **PRESERVE-COVERAGE** (full dimension / continuous DATE SPINE / LEFT-join / keep
zero-activity rows / never dedup a `*_unioned`) for reporting/dimension/daily targets, and
**SCOPE-TO-ACTIVE** (INNER join / filter) ONLY when the instruction explicitly signals it ("only X
that have…", a per-entity lifetime rollup). The gated PER-KEY rule is subordinated to the classifier.
Solver README: `../solver_workflows/spd0004-conditioned-grain/README.md` (fork of `@baseline`
`spider2-dbt-baseline`; `diff` shows ONLY the grain rule changed — independent-variable rule holds).

Disjoint from siblings: **spd0002** owns multi-target completeness, **spd0003** owns value-level
semantics. spd0004 owns grain/row-set only.

## Acceptance criteria

- **AC-1** — Flips ≥2 under-emit GRAIN target tasks FAIL→PASS by their committed artifacts
  (convention-correct table now spans the full dimension/date-spine, row count matches gold), with the
  flip attributable to the PRESERVE-COVERAGE regime (not noise).
- **AC-2** — Zero regression on the SCOPE-TO-ACTIVE canary: tpch001's grain regime stays *filtered*
  (the classifier must NOT flip tpch onto full-dimension coverage). tpch may still fail on value-def,
  but its row set must not regress toward 150k.
- **AC-3** — Zero regression on the currently-PASSING regression canaries in the smoke set.
- **AC-4** — Independent-variable: `diff @baseline spd0004` README touches only the grain rule;
  leak-guard prose intact (`rk audit --policy strict` clean).

## Smoke set (propose → smoke gate)

Spec: `specs/spd0004-conditioned-grain.smoke.frozen.yaml` (kind: harbor-local, gpt-5.5/xhigh,
trials 1, concurrency 4; solver_workflow → spd0004-conditioned-grain).

| task | @baseline | role | expected under spd0004 |
|---|---|---|---|
| jira001 | ❌ (under-emit: dropped projects w/o issues) | 🎯 should-flip | LEFT-join projects → 3 rows |
| marketo001 | ❌ (under-emit: 3 vs 79 templates) | 🎯 should-flip | keep all 79 templates, zero-fill |
| pendo001 | ❌ (under-emit: no date spine) | 🎯 should-flip | full per-guide daily spine |
| salesforce001 | ❌ (under-emit: 55 vs 91-day spine) | 🎯 should-flip | contiguous 91-day spine |
| xero001 | ❌ (under-emit: 345 vs 1170, truncated spine) | 🎯 should-flip | full 60-month account spine |
| tpch001 | ❌ (over-emit + value-def) | 🛡️ over-emit canary | grain stays SCOPE-TO-ACTIVE (filtered), NOT flipped to coverage |
| f1001 | ✅ | 🛡️ regression canary | stays PASS |
| mrr001 | ✅ | 🛡️ regression canary | stays PASS |

Net read: GO to full if ≥2 of the 5 should-flip cells flip AND both regression canaries hold AND tpch
does not regress its row set. ETA ~8 cells ÷ conc 4 ≈ 2 slots × ~12 min ≈ ~25–35 min.

Calibration: grain is oracle-blind (solver can't self-verify the intended row set — the recurring
self-anchored false-green) and grain levers historically add ±variance, so judge by per-cell
construct-touch (did the committed model switch to the coverage regime?) not just net pass count.
Do NOT launch the full run without captain go at the smoke gate.

## Stage Report (propose)

Authored by the operator (single-entity propose prep):
- **Spec**: `specs/spd0004-conditioned-grain.smoke.frozen.yaml` authored + frozen + `rk run --explain`
  clean (resolves the 8 smoke tasks; the v3 grain prose is present in the assembled prompt).
- **Leak-guard**: README forked from `@baseline`; the no-external-reference / workspace-only prose is
  intact (1 match, unchanged from baseline); no new fetch/oracle affordance introduced. `diff` confirms
  only the grain rule changed.
- **Smoke table**: above (5 should-flip + 1 over-emit canary + 2 regression canaries).
