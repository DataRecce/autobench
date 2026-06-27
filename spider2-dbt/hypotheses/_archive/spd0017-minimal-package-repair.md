---
id: spd0017
title: Minimal package/dependency repair (compile-boundary only) — Queue 3
status: conclude
kind: hypothesis
source: "day-queue-2026-06-26 Queue 3; forks champion @baseline spd0013; discovery smoke-only"
started: 2026-06-27
completed: 2026-06-27
verdict: REJECTED
score:
worktree:
archived: 2026-06-27T03:40:06Z
---

## Hypothesis

Queue-3 premise: some never-pass tasks FAIL TO COMPILE/BUILD due to missing package vars, missing
package source relations, or failing generic tests; a minimal compile-boundary repair (add the missing
var/source, disable the stale test locally; do NOT edit package model logic) would make them buildable
and then gradeable.

**Single README change (one knob):** a gated "minimal package-repair" clause — when `dbt compile`/`build`
fails on a missing package var / source relation / generic test, repair only the minimal LOCAL boundary
needed to compile, never package internals unless a local source/type defect proves it required.

## Pre-smoke evidence check (premise FALSIFIED — concluded without a smoke)

**The Q3 package-repair rule is gated on a compile/build failure. Verified against the champion run
`runs/spd0013-lean-lag-period-over-period/7f3278d0d61d2577`: ALL gradeable Q3 targets BUILD and grade —
ZERO compile/build failures.** (`result.json` has no `exception_info` for hive001, synthea001,
quickbooks001, pendo001, xero_new001, zuora001; shopify_holistic_reporting001 is not in the gradeable
60-board.) Their reward=0 is a VALUE/GRAIN mismatch, not a build failure.

The build-failure family that motivated Queue-3 was already eliminated by the **packaging-layer repairs
shipped earlier**: dbt_utils vendored (synthea), sap GL sources restored (spd0010), f1001
`_align_source_schemas_to_main`, and razorback PR#23/#25 (harbor source resolution + Jinja `var()`
rendering). With no compile-failures left among the gradeable tasks, the package-repair rule is **inert
by construction** — it would never fire. A smoke would cost ~1h to confirm "the rule did not fire."

## Verdict

**REJECTED — premise inapplicable at the current champion (concluded without a smoke, evidence-based).**
Queue-3's compile-failure family no longer exists among the 60 gradeable tasks (the packaging repairs
fixed it); the remaining failures on the Q3 target pool are value/grain (Queue-2 family). No solver
README change is warranted. Time redirected to per-task diagnosis of the banked tickit002 near-miss
(higher value for the "find resolvable tasks" goal). @baseline unchanged = spd0013 27/60.

NOTE: if a FUTURE never-pass task is found to genuinely fail to COMPILE (not just mismatch), reopen this
hypothesis — the minimal-boundary repair rule is sound; it simply has no live target now.
