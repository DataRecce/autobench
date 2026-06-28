---
id: spd0023
title: Structural self-check + rebuild loop — attack execution variance with an oracle-free row-set/grain signature retry
status: hypothesis
kind: hypothesis
source: "the 2026-06-27/28 finding: the contract makes the worker WRITE+CHECK the right fix once but it doesn't reliably LAND (per-cell execution variance is the wall; spd0021/22 = 1/13 reliable). This adds a BUILD->self-check-structural-signature->REBUILD loop (retry on failure), distinct from spd0015's correlated value-recheck. Forks champion spd0013."
started: 2026-06-28
completed:
verdict:
score:
worktree:
---

## Hypothesis

Every prior lever CHECKED the fix once and shipped. The wall is per-cell **execution variance**: the worker
writes the right approach but doesn't reliably produce the correct committed artifact (spd0021/22: the
contract engaged but only 1/13 leads landed). The row-set/grain leads each have an **oracle-free STRUCTURAL
signature** — row-set count, period bound, grain-key uniqueness, fan-out — checkable from the source +
declared grain WITHOUT gold values.

**New mechanism (one knob):** fork champion `spd0013` and add a **build → structural self-check → rebuild
loop**: after building a target whose correctness has an oracle-free structural signature, run a self-check
query computing that signature from the built table AND the source; if they disagree, diagnose the
structural gap and REBUILD; repeat up to 3× before finalizing. This RETRIES on failure (no prior lever did)
and converts a ~30–60% execution rate into a high one for row-set/grain cells.

> **Stage: Structural self-check + rebuild (gated; before finalizing).** For a target whose correctness has
> an ORACLE-FREE structural signature derivable from the source + declared grain (NOT gold values):
> (1) identify the signature — e.g. built row count = the full base-set/source row count (per-entity /
> reference / full-set target); emitted period range = [first..last source-activity period] (spine/balance
> report); grain key unique; a fan-out join's row count = the joined-grain count (not deduped);
> (2) run a self-check query computing it from the built table AND the source;
> (3) if they disagree, diagnose the structural gap (dropped unmatched rows → INNER should be LEFT; periods
> past last activity → spine over-ran; collapsed fan-out → wrong dedup; row count below base-set → a filter
> dropped valid rows) and REBUILD;
> (4) repeat up to 3× — finalize only when the structural signature holds (or local evidence shows it can't).
> The signature is STRUCTURAL (row-set membership/count/grain), never whether values match gold. Never read gold.

Oracle-free (structural, source-derived, "never read gold"); gated (fires only where a structural signature
exists — inert on value-residual cells). NO other change; leak guard byte-identical to spd0013.

Row-set/grain targets (signature applies): provider001, intercom001, hive001, netflix001, xero001
(+ asana001 = known-2/3 positive control).

## Pre-smoke Decision-Fork Probe

Reachability proven offline (catalog). The OPEN question is whether a RETRY-on-structural-signature loop
beats the per-cell variance the one-shot contract could not (spd0021/22 row-set leads 0/3). Distinct from
spd0015's REJECTED value-recheck: that recheck was correlated with the worker's own value error; a STRUCTURAL
signature (row count, period bound, fan-out) is independent of the value, so the self-check can catch a
row-set miss the worker doesn't otherwise see. Smoke measures: does the loop fire + flip the row-set leads.

## Acceptance criteria

**AC-1 — README-only; forks spd0013; adds ONLY the structural self-check+rebuild loop.** Leak guard intact.
**AC-2 — clean strict audit.**
**AC-3 —** smoke useful if the loop fires (self-check + rebuild visible in artifacts) AND ≥2 row-set leads
flip (vs the contract's 0/3); canaries hold. trials=3 confirm follows a GO. NO promote w/o captain sign-off.

## Smoke Plan

trials=1 sanity smoke now (parallel with spd0022), ~11 cells: provider001, intercom001, hive001, netflix001,
xero001, asana001 + canaries apple_store001, google_play001, mrr001, quickbooks002, activity001. Confirms the
loop fires + flips. If ≥2 row-set leads flip → trials=3 panel for the hold-rate.

## Gatekeeper review

## Smoke result

## Verdict
