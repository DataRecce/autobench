---
id: spd0004
title: Conditioned grain — PRESERVE-COVERAGE vs SCOPE-TO-ACTIVE classifier (fix the under-emit GRAIN family)
status: conclude
kind: hypothesis
source: 42-task @baseline failure analysis (docs/failure-analysis-2026-06-24.md) — GRAIN is the largest addressable family
started: 2026-06-24T14:32:32Z
completed: 2026-06-24T18:48:07Z
verdict: validated-not-promoted
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

## Stage Report (smoke)

Run: `runs/spider2-dbt-spd0004-smoke/9785222d3cf0c206` (rc=0, ~28m, 8 cells, conc 4).
Net pass: marketo001 FLIP→PASS, mrr001 held, f1001 REGRESSED → **net +1 −1 = 0**. But the
**construct-touch is strong** (judge by this, per calibration), with a real over-fire defect:

| task | role | @base rows | spd0004 rows (gold) | regime adopted? | outcome |
|---|---|---|---|---|---|
| marketo001 | flip | 3 | (79) all templates | ✅ PRESERVE-COVERAGE | **PASS 🎯** |
| salesforce001 | flip | 55 | **91 = gold 91** | ✅ full 91-day spine | grain FIXED, value-def residual → fail |
| jira001 | flip | 2 | **3 = gold 3** | ✅ LEFT-join projects | grain FIXED, value-def residual → fail |
| pendo001 | flip | (few) | date_day spine built | ✅ spine | grain touched, residual → fail |
| xero001 | flip | 345 | 1614 (gold 1170) | ⚠️ expanded but over-shot (account_name not _id) | over-corrected → fail |
| tpch001 | over-emit canary | 76777 | 76777 (NOT 150k) | ✅ stayed SCOPE-TO-ACTIVE | **AC-2 HOLDS** |
| mrr001 | regression canary | PASS | PASS | n/a | held ✅ |
| f1001 | regression canary | PASS | applied coverage/spine/LEFT-join to F1 stats | ❌ OVER-FIRE | **REGRESSED** |

**Read:** the conditioned-grain lever is VALIDATED as construct-steering — **5/5 should-flips adopted
the coverage regime**, 2 hit the EXACT gold row count (salesforce 55→91, jira 2→3), marketo fully
flipped, and the tpch over-emit canary correctly did NOT flip (AC-2 holds). BUT (a) the grain-fixed
cells (jira/salesforce/pendo) still fail on **value-level** residuals — that is **spd0003's** family,
not spd0004's, so grain alone can't PASS them; and (b) the PRESERVE-COVERAGE default **OVER-FIRES**:
it applied spine/LEFT-join to f1001's F1-stats models (a non-coverage task) and regressed a passer.

**AC status:** AC-1 (≥2 FAIL→PASS) NOT met (1 pass; but the construct flipped on 5/5). AC-2 HOLDS.
AC-3 (canary regression) FAILS (f1001 over-fire). AC-4 holds (diff clean, leak-guard intact).

**Verdict recommendation: smoke → hypothesis (REVISE), do NOT go to full as-is.** The lever is real
but needs a TIGHTER gate so PRESERVE-COVERAGE fires only on genuine reporting/dimension/daily targets
and never on aggregate/stats tasks (the f1001 over-fire). Re-smoke after tightening. The grain-fixed-
but-value-failing cells (jira/salesforce) argue for eventually COMPOSING spd0004 (grain) with spd0003
(value) rather than expecting grain alone to flip them.

### Feedback Cycles

**Cycle 2 (auto-revise, no gate wait).** Smoke c1 over-fired on f1001 (applied spine/LEFT-join to F1
`most_*`/stats models, regressed a passer). Fix: added a NEITHER-regime clause to §4 — aggregate /
ranking / superlative / total targets (`most_*`/`top_*`/"most/top/fastest/total/career/season") get
the ordinary GROUP BY/window aggregate, never a spine or coverage padding; this OVERRIDES the
PRESERVE-COVERAGE default. Keeps marketo/salesforce/jira coverage (genuine dimension/daily/report
targets). Re-smoke as cycle 2.

## Stage Report (smoke — cycle 2, GO)

Run: `runs/spider2-dbt-spd0004-smoke-c2/4ff7d67ce38432b0` (rc=0, ~27m, 8 cells). **Clean GO.**

| task | role | base | c2 | note |
|---|---|---|---|---|
| marketo001 | flip | ❌ | ✅ FLIP | full 79-template coverage |
| salesforce001 | flip | ❌ | ✅ FLIP | full 91-day spine, now passes (c1 had grain but value residual) |
| f1001 | regression canary | ✅ | ✅ | **over-fire FIXED** by the aggregate/ranking exclusion |
| mrr001 | regression canary | ✅ | ✅ | held |
| tpch001 | over-emit canary | ❌ | ❌ | stayed SCOPE-TO-ACTIVE (~76777, not 150k) — AC-2 holds |
| jira001 | flip | ❌ | ❌ | grain fixed (3=gold) but value-level residual → spd0003 |
| pendo001 | flip | ❌ | ❌ | spine adopted, value/column residual → spd0003 |
| xero001 | flip | ❌ | ❌ | over-shoots (account_name key) — value/key residual |

**flips=2, regressions=0, tpch held.** GO bar met (≥2 flips ∧ 0 regr ∧ tpch scoped).

**AC scorecard:** AC-1 ✅ (2 FAIL→PASS: marketo, salesforce). AC-2 ✅. AC-3 ✅ (0 regressions — f1001
over-fire fixed in c2). AC-4 ✅ (grain-only diff, leak-guard intact). **All ACs met.**

**Verdict: smoke PASSES → recommend FULL.** The conditioned-grain lever is validated and converged in
2 cycles: it steers grain correctly (5/5 should-flips adopt the regime; 2 fully flip), the over-fire is
gated, and it does not disturb the SCOPE-TO-ACTIVE / aggregate tasks. The 3 non-flipping should-flips
(jira/pendo/xero) now carry the CORRECT grain but fail on value-level residuals = spd0003's family —
evidence for a future spd0004+spd0003 composition, not a spd0004 defect. Holding at the smoke→full
boundary for captain go on the multi-hour full run (not auto-launched).

## Stage Report (analyze + conclude)

Full run: `runs/spider2-dbt-spd0004-full/7e2d204bc5c4a978` (rc=0). `rk score`: **21 pass / 60 completed
(1 errored) = stratified_pass_at_1 0.35**; counting the errored cell as fail vs the 61-task @baseline,
**21/61 = 0.3443 vs @baseline 19/61 = 0.3115, NET +2**.

- FLIPS (+3): marketo001 (grain-attributable, full-coverage templates — stable across smoke+full),
  quickbooks003, retail001 (value-def "count-grain"/teachable cells — partly serendipity/variance).
- REGRESSION (−1): f1001 (recovered in smoke c2 but regressed on the full draw; transcript still shows
  residual spine/coverage reasoning — a boundary/coin-flip cell the aggregate-exclusion only partly tames).
- The DESIGNED flip **salesforce001 did NOT hold full-board** (passed smoke, failed full) — single-trial
  variance on a boundary cell.
- 1 new errored cell (flaky build, not solver-attributable).

**Verdict: PASSED-validated, NOT promoted.** The conditioned-grain lever is construct-validated (smoke:
5/5 should-flips adopt the regime, marketo+salesforce flip, over-fire gateable) and yields a grain-
attributable flip (marketo) that holds across draws. BUT the full-board **+2 is inside the single-draw
variance band**: the designed flip (salesforce) is non-reproducible smoke→full, f1001 regressed, and the
other flips are partly serendipitous. Per the standing discipline (a single full draw is not promotable
without a ≥3-draw hold-rate; grain levers add ±variance), **@baseline stays 19/61 — NOT re-registered.**

Durable signal banked: (1) conditioned grain is README-steerable and the right diagnosis for the
under-emit family; (2) grain-fixed cells (jira/salesforce/pendo) still fail on VALUE-level residuals →
the durable path is a **spd0004(grain)+spd0003(value) composition**, not grain alone. → filed spd0005.
