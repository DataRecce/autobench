---
id: h0056
title: Six-lever composition — stack the three new smoke-verified levers (h0053 per-key inner-join + h0054 lap-time exclude-pit-laps + h0055 build/rename preserve-columns) onto @baseline h0052's three (max-points + feature-boundary + coverage) in ONE README
status: propose
kind: hypothesis
source: "Captain request 2026-06-13 — merge the three individually smoke-verified levers (h0053 airbnb005 inner-join GO; h0054 f1010-medium exclude-pit-laps GO; h0055 ana-eng003 preserve-columns, smoke in progress / ana-eng003 artifact passing) into one composition on the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133). Same compose-verified-bleed-free-levers play that promoted h0052; each new lever is precondition-gated and explicitly non-colliding with an existing one."
started: 2026-06-13T17:45:52Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The h0052 baseline README already composes three construct-gated levers (h0044 same-grain
`max(points)`, h0045 feature-boundary removal/toggle, h0050 intent-gated scoped coverage). This
hypothesis stacks the three NEW smoke-verified levers on top, in one README — six gated
Implementation rules total:

| # | Lever | Construct it gates on | Smoke evidence |
|---|-------|-----------------------|----------------|
| 1 | h0044 max(points) | standings/season points | (in h0052) f1006 + f1006-hard flips |
| 2 | h0045 feature-boundary | remove/disable feature | (in h0052) qb002/qb004 narrow holds |
| 3 | h0050 scoped coverage | completeness-intent missing rows | (in h0052) airbnb009 flip |
| 4 | **h0053 per-key inner-join** | per-key metric, NO completeness intent | **GO** — airbnb005 inner-join, 14,243-row oracle match |
| 5 | **h0054 lap-time exclude** | lap/duration avg accounting for pit stops | **GO** — f1010-medium EXCLUDE artifact |
| 6 | **h0055 preserve-columns** | build/rename, no feature-removal, no col-subset | smoke in progress (ana-eng003 artifact passing) |

**Two gated dual-pairs must coexist without collision (the integration risk):**
- **h0050 ↔ h0053** — opposite sides of the completeness-intent signal. h0050 ADDS missing keys
  when completeness IS requested (airbnb009); h0053 scopes to fact keys when it is NOT (airbnb005).
  Proven non-colliding in h0053's solo smoke (airbnb009 held while airbnb005 flipped).
- **h0045 ↔ h0055** — opposite task types. h0045 DROPS feature-only columns on remove/disable
  tasks (qb002/qb004); h0055 PRESERVES all upstream columns on build/rename (ana-eng003).

**Falsifiable claim (the single README change):** fork the current `@baseline` (h0052) solver and
add the three new levers **verbatim, each as its own precondition-gated Implementation rule** —
nothing else. The six-lever composition will preserve every lever's solo effect with **no
interference and no collision**:
- airbnb005 flips via the inner-join shape (h0053);
- f1010-medium commits the EXCLUDE artifact and ana-eng003 the full-18-column artifact
  (h0054/h0055 — noise-reducers that pin two coin-flip cells, shrinking the trials:1 variance pool);
- airbnb009 + f1006 + f1006-hard (h0052's banked flips) HOLD;
- qb002 + qb004 still drop their feature columns (h0045 fires, h0055 does NOT);
- every canary holds.

**Why compose:** the program-wide lesson is that trials:1 ±noise (~±3 cells) washes a single
flip's net. Stacking verified bleed-free levers (a) banks airbnb005 (+1 over h0052) AND (b) **pins
two of the coin-flip cells** (f1010-medium, ana-eng003) that have been costing nets — a tighter
variance band, not just a higher signal. Best case nets above h0052's true expectation (~30) and
clears it on a fresh draw.

**Falsified if** composing degrades any lever vs its solo smoke (interference / README bloat
mis-routing a precondition), OR a dual-pair collides (airbnb009 coverage suppressed; qb feature
columns force-preserved), OR a canary regresses beyond off-construct trials:1 variance.

Target datasets: airbnb005 (flip); f1010-medium, ana-eng003 (pin/stabilize); airbnb009, f1006,
f1006-hard, qb002, qb004 (hold).

## Pre-smoke Decision-Fork Probe

Skipped — each of the three new levers is individually smoke-verified at the committed-artifact
level (h0053 GO, h0054 GO, h0055 GO-pending) and each was already shown non-colliding with its dual
in its solo smoke (h0053: airbnb009 held; h0055: qb002/003 held). The only new question is the
six-way composition / mutual interference, which the combined smoke tests directly (and the h0052
promotion already established that construct-gated levers compose). No new probe owed.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Composed README = h0052's README + the h0053, h0054, h0055 lever blocks verbatim (each traceable to
its source solver dir), nothing else; the existing three levers + leak-guard byte-unchanged.

**AC-2 — Every recorded score paired with a clean strict audit** (captured>0 every cell).

**AC-3 — Verdict by paired delta vs `@baseline` (h0052), read through the known ~±3 trials:1 noise
floor.** Promote on committed-artifact + expectation (per the h0052 self-consistency precedent), not
a single-draw net alone.

**AC-4 — Per-lever committed-artifact reads (the decisive test):** airbnb005 = inner-join-from-fact
(no zero-fact NULL rows); f1010-medium = EXCLUDE pit laps before avg; ana-eng003 = all 18 columns;
airbnb009 = coverage predicate dropped (h0050 still fires); f1006/f1006-hard = `max(points)`;
qb002/qb004 = narrow feature-boundary (columns dropped, h0045 still fires).

**AC-5 — Regression panel + BOTH collision-canary pairs hold:** airbnb009 (h0050↔h0053 collision),
quickbooks002 + quickbooks003 (h0045↔h0055 collision), plus ≥1 perturbable passer per family. A
collision or same-construct regression is a NO-GO; off-construct trials:1 variance is classified,
not auto-fatal; the promote decision rests on the run-dir clearing h0052's expectation.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
