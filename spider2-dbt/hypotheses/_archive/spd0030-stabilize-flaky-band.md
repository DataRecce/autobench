---
title: Stabilize the flaky band — per-cell variance-pinning README directives to bank the flipped-but-inconsistent cells
status: conclude
kind: concept
id: spd0030
source: "captain-directed (2026-06-29). New target: NOT the never-pass set (execution-wall-bound, exhausted) but the FLAKY band — cells that ALREADY pass in some champion draws but not consistently, so they aren't banked in the v0.22 baseline. A passing draw is an oracle-free CORRECT-ANSWER reference, so the variance source is recoverable by diffing passing-vs-failing transcripts. Fine-tune the champion README to PIN each cell's bifurcation → consistency. forks champion @baseline spd0030(=spd0013 lineage)."
started: 2026-06-29
completed:
verdict: 6-of-7-stabilized (HELD for captain compose)
archived: 2026-06-29T17:39:54Z
---

The never-pass program is exhausted (oracle-blind or execution-wall-bound). This concept pivots to the
**flaky band**: cells the champion passes SOME draws but not all. Because a passing draw is a verified
correct answer, the variance is diagnosable (diff passing vs failing transcripts) and potentially pinnable
with a targeted gated README directive — escaping the oracle wall that blocked the never-pass work.

## Target set (flipped-but-not-banked; all have diffable pass+fail champion-ish draws)
2/3-band (pass most draws, just need a nudge): airbnb001, apple_store001, greenhouse001, lever001,
quickbooks003, workday001. ~50%-band: asset001, sap001, divvy001.

## Method
1. Per-cell bifurcation analysis (parallel subagents): diff passing-draw vs failing-draw transcripts →
   identify the SPECIFIC choice the solver wavers on (a column kept/dropped, a grain/join, a filter, a
   tiebreak, a materialization, a cast) → classify PINNABLE (one clear bifurcation) vs DIFFUSE (varies
   every which way → not README-stabilizable, drop it honestly).
2. Cluster pinnable cells into gated hypotheses (each lever fires only on its structural signal → composes
   without bleeding; one or few cells per hypothesis).
3. Smoke each = the target cell at **trials=3** (measure the consistency hold-rate, NOT a single draw —
   single-draw is the known optimism trap) + 1–2 rock-solid canaries (trials=1). GO = target holds 3/3
   with canaries clean. NO-GO = revise the directive and re-smoke until no method works, then drop.

## Process (captain-directed, fully automated)
Auto-dispatch each hypothesis to smoke without approval. GO → HOLD (no full, no promote) + switch to next.
NO-GO → revise multiple times until exhausted. Up to 2 smokes concurrent. Frequent, focused execution.

## Fan-out (7 hypotheses; bifurcation analysis in _artifacts/flaky-bifurcation-analysis-2026-06-29.md)
NEW-rule (champion lacks it; highest GO odds): spd0031 quickbooks003 (reuse-shipped-upstream), spd0032 sap001
(re-aggregate long→grain), spd0033 divvy001 (staging-test→warn), spd0034 asset001 (round-final-product).
SHARPEN existing-but-under-obeyed: spd0035 greenhouse001 (no-string-cast-id), spd0036 airbnb001 (window-anchor),
spd0037 apple_store001 (raw-grouping-key). DROPPED (champion-stable, fails were spd0022-lever-induced/harness):
lever001, workday001. Autonomous loop: _artifacts/flaky-stabilize-queue-2026-06-29.md.
