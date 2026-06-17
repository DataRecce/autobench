---
name: ade-bench-category-c-pin-resists-deoverfit
description: h0062 REJECTED — the Category-C max()-points domain pin RESISTS de-overfitting; h0044's brevity+concrete-anchor is itself load-bearing, enumerating forbidden branches at length drifts the solver onto them
metadata:
  type: project
---

h0062 (REJECTED, smoke 4/7) tried to de-overfit the ONE Category-C "memorized
answer" in the @baseline README — the F1-pinned `CUMULATIVE-SNAPSHOT TOTALS —
max() AT ENTITY GRAIN` rule — by replacing the domain name with a domain-blind
`lag()` MONOTONICITY PROBE trigger while keeping the `max()`-at-grain repair. It
coupled TWO changes: (1) trigger F1-name→domain-blind probe, (2) added verbosity
(a 6-line inline probe-SQL block + a longer paragraph that ENUMERATES the
forbidden branches latest-row/rank/row_number/QUALIFY/order-by-final-period).

**Result (verified committed artifacts, run 63ffe07e1eefe1d6):** the two HARD
cumulative variants drifted OFF `max()` ONTO the forbidden branch — f1006-hard
committed `row_number() over (… order by round desc) WHERE standings_order=1`,
f1005-medium committed `QUALIFY ROW_NUMBER() OVER (… ORDER BY round DESC)` — vs
@baseline's `max(cs.points)`. Both failed `AUTO_constructor_points_equality`
Got 2 while `AUTO_driver_points_equality` PASSED (the multi-model-target trap,
G11, realized: the latest-row choice lands one scored model, breaks the other by
2 rows). The EASY targets (f1006, f1005) still committed `max()` and held; both
additive-SUM canaries (airbnb005 rolling-28d SUM, airbnb001 monthly COUNT) held
BYTE-INTACT — the over-fire worry the propose canaries guarded did NOT
materialize. f1001 was unrelated build-task variance (gate never engaged).

**Why:** Not every Category-C memorized domain answer is de-pinnable into a
portable structural rule. h0044's **brevity + concrete domain anchor is itself
load-bearing**, not just the F1 name: a terse "treat points as cumulative
race-by-race snapshots → max(points)" kept the solver on the safe edge, but
EXPANDING it and NAMING the forbidden alternatives at length RAISED their
salience and handed the solver a reasoning path straight into them on the hardest
cells. Naming what-not-to-do at length is anti-helpful.

**How to apply:** (1) Before filing a de-overfit lever on a domain-pinned rule,
ask whether the rule's BREVITY/concreteness — not just its domain name — is doing
the work; if so it may be un-de-overfittable. (2) Do NOT add long forbidden-branch
enumerations or inline probe-SQL blocks to a working terse rule — it costs
robustness on the hardest variants. Dovetails with [[ade-bench-baseline-registry-lost]]
h0061 finding "verbosity is not robustness" (removing scar-prose from a working
rule is dilution-safe; this is the mirror — ADDING bulk to a working terse rule
actively harms). (3) The de-overfit DIRECTION (probe-gated max() repair) is sound
— probe and gate both behaved; the failure is the verbose PROSE. Follow-up h0063
(filed, queued) isolates verbosity vs domain-name removal: keep the domain-blind
probe trigger, restore h0044's terse repair wording. See
[[knowledge-gains-are-small-successes]] and [[ade-bench-instruction-lever-taxonomy]].
