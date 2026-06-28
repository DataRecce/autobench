---
id: spd0023
title: Structural self-check + rebuild loop — attack execution variance with an oracle-free row-set/grain signature retry
status: conclude
kind: hypothesis
source: "the 2026-06-27/28 finding: the contract makes the worker WRITE+CHECK the right fix once but it doesn't reliably LAND (per-cell execution variance is the wall; spd0021/22 = 1/13 reliable). This adds a BUILD->self-check-structural-signature->REBUILD loop (retry on failure), distinct from spd0015's correlated value-recheck. Forks champion spd0013."
started: 2026-06-28
completed: 2026-06-28
verdict: REJECTED
score:
worktree:
archived: 2026-06-28T03:38:16Z
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

**Recommendation: APPROVE** — a gated, structural (row-set/count/grain/period), source-derived self-check→rebuild loop that never reads gold and is explicitly inert on value-residual cells; clean single-idea README diff, leak-guard byte-identical, smoke covers all 6 named targets + 5 baseline-passing canaries at trials:1.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-28T00:00:00Z.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | `diff` of parent spd0013 vs spd0023 README = one hunk only (`397a398,419`): adds the single "## Stage: Structural self-check + rebuild (gated; before finalizing)" section ahead of Finalization. No other prose, no guardrail/output-contract edits. Matches the hypothesis's one-knob claim (build→structural self-check→rebuild loop). |
| G2 leak-guard (hidden gold) | PASS | grep over added lines 398–419 for `gold/expected_/answer_key/ground_truth/curl/wget/git clone/git ls-remote`: only hits are negations — "from the source + declared grain (NOT gold values)" and "never whether values match gold. Never read gold." No gold-table/column names, no read-gold/fetch instruction. No-fetch paragraph (lines 11–15) byte-identical to parent (`diff` → IDENTICAL). |
| G3 spec two fields | PASS (full spec absent — noted) | No spd0023 full spec authored (intentional per hypothesis: trials:3 panel follows a GO). Evaluated smoke source vs `full-baseline.yaml`: `kind:spacedock_solver`, `runtime:codex`, `model:gpt-5.5`, `reasoning_effort:xhigh`, `trials:1` all preserved; only `experiment:` (`spd0023-…`) and `agent.solver_workflow:` (`./solver_workflows/spd0023-…`) differ (plus the deliberate trials:1 smoke shape, already 1 in baseline, and the task subset evaluated under G4). No third field differs. |
| G4 smoke narrows tasks only | PASS | Smoke `benchmark.tasks` = 11: all 6 hypothesis-named targets (provider001, intercom001, hive001, netflix001, xero001, asana001) + canaries apple_store001, google_play001, mrr001, quickbooks002, activity001. trials:1, no `exclude_tasks`, only the task list + experiment/solver_workflow differ from baseline. Every target the `## Hypothesis` names is included. |
| G5 both frozen | PASS (full frozen absent — noted) | `…smoke.frozen.yaml` exists (1850 B, 2026-06-28) and carries `kind: spacedock_solver` + `runtime: codex`. No full frozen file — expected for this hypothesis (no full spec yet); not failed per scope note. |
| G6 resolver fidelity | PASS | Inserted text matches the claim verbatim in spirit: identify an ORACLE-FREE structural signature (row-count/period-range/grain-uniqueness/fan-out) → self-check from built table AND source → diagnose structural gap → rebuild, up to 3×. Stays independent/generative (checks a source-derived structural invariant), NOT self-anchored "verify your answer matches" — it explicitly says the signature is structural "never whether values match gold." No scope creep. |
| G7 actionability/inert-risk | PASS | Mechanical and concrete: names specific self-check queries (built row count = base-set/source count; emitted period range = [first..last source-activity period]; grain key unique; fan-out row count = joined-grain count) and concrete diagnose-and-fix moves (INNER→LEFT, spine over-ran, wrong dedup, filter dropped rows). Not abstract "get the grain right" prose. |
| G8 regression-canary coverage | N/A (PASS) | Lever is gated: fires ONLY where an oracle-free structural signature exists, explicitly inert on value-residual cells. Not a fires-everywhere generative change. (Even so, smoke retains 5 baseline-PASS canaries — apple_store001/google_play001/mrr001/quickbooks002/activity001 all reward 1.0 in @baseline — so a perturbation would surface.) |
| G9 selector independence | N/A (PASS) | Not a multi-candidate/selector protocol — it is a single-build retry loop, not "run N candidates and pick one." |
| G10 self-correcting false-positive | PASS | Self-correcting lever; evaluated all three sub-clauses. (a) Scope: GATED — fires only where an oracle-free structural signature is derivable, explicitly skipped on value-residual cells (not ungated-generative). (b) Independence source: checks a STRUCTURAL invariant (row-set count/period bound/grain uniqueness/fan-out) computed from the built table AND the source — independent of the solver's own value derivation, not a re-run of it (distinct from spd0015's REJECTED correlated value-recheck; a structure/membership check cannot turn a right value wrong). (c) Check-don't-replace: mandates *diagnose the structural gap* (named gap→fix mapping) and rebuild, not a blind replace-with-a-structurally-different model. No FAIL trigger on any clause. |

**For the captain:** Auto-approved to smoke. The lever is a gated, structural-invariant (not value) self-check→rebuild loop — the G10 danger class — but it passes all three G10 sub-checks: gated to signature-bearing cells, independence-sourced from the raw source/declared grain rather than a re-derivation (the explicit contrast with the REJECTED spd0015 value-recheck), and diagnose-then-rebuild rather than blind replace. Two structural notes you waived in scope: no full spec / full frozen file yet (trials:3 panel follows a GO). Smoke retains 5 currently-passing canaries (all 1.0 at @baseline) against the 6 baseline-FAIL targets, so a regression would show. Watch in the smoke artifacts: that the loop actually FIRES (self-check + rebuild visible) and is not behaviorally inert at gpt-5.5/xhigh (the G7 inert-risk that has bitten prior generative-feeling levers).

## Smoke result

## Verdict

## Stage Report: propose

- DONE: Fork the champion: cp -r solver_workflows/spd0013-lean-lag-period-over-period solver_workflows/spd0023-structural-selfcheck-retry-loop
  `diff` of forked README vs spd0013 was IDENTICAL before editing.
- DONE: Edit ONLY README.md to add ONE new stage (build→structural self-check→rebuild loop, from the hypothesis blockquote). One knob.
  Added "## Stage: Structural self-check + rebuild (gated; before finalizing)" between Validation and Finalization.
- DONE: The stage carries the oracle-free structural signature + diagnose-and-rebuild-up-to-3x logic; structural (row-set/count/grain/period), never gold.
  Verbatim from the hypothesis ## Hypothesis blockquote; gated-inert note added for value-residual cells.
- DONE: Keep no-external-reference / leak-guard prose byte-intact; NO gold values/counts/dtypes baked
  G2 grep: only "gold" hits are negations ("NOT gold values", "never read gold"); no-fetch para byte-identical (diff IDENTICAL).
- DONE: Do NOT relocate or delete any existing spd0013 guidance; only ADD the one self-check+rebuild stage
  `diff` = `397a398,419` (pure append, zero deletions).
- DONE: Create a trials=1 sanity smoke spec specs/spd0023-structural-selfcheck-retry-loop.smoke.yaml (exact 11-task allowlist; drop stale baseline content-hash)
  experiment spd0023-structural-selfcheck-retry-loop, solver_workflow ./solver_workflows/spd0023-…, trials:1; dropped stale provenance.solver_workflow_hash 9660d413 so freeze recomputes.
- DONE: Freeze from REPO ROOT; verify content_hash non-null + differs from baseline 9660d413; trials:1; --explain shows Tasks: 11
  Frozen content_hash d6d313fd (≠ 9660d413, grep count 0); trials:1; `rk run --explain` => Tasks: 11.
- DONE: README diff vs spd0013 = ONLY the added self-check+rebuild stage (no deletions)
  Single hunk `397a398,419`, append-only.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block
  Gatekeeper APPROVE, zero FAILs (G3/G5 noted full-spec-absent per scope); block written above.
- DONE: Do NOT launch any rk run beyond $0 --explain. Commit. Stop; the FO owns the smoke launch.
  Only `--explain` ($0) run; no rk run launched.

### Summary

Forked champion spd0013 into solver_workflows/spd0023-structural-selfcheck-retry-loop and added exactly one new stage — a gated build→structural-self-check→rebuild loop (retry up to 3× on an oracle-free row-set/count/grain/period signature, never gold) — as a pure append (diff 397a398,419, zero deletions, leak-guard byte-intact). Authored + froze the trials=1 / 11-task smoke spec (5 row-set/grain leads + asana001 positive control + 5 baseline-passing canaries), dropping the stale baseline hash so freeze recomputed content_hash d6d313fd (≠ baseline 9660d413); `--explain` confirms Tasks: 11. Gatekeeper returned APPROVE with no FAILs (G10 self-correcting family passes all three sub-checks — gated, structural-not-value independence, diagnose-then-rebuild). No rk run launched beyond $0 --explain; the FO owns the smoke launch.


## Smoke result + Verdict

**REJECTED (mode-2: loop fires but cannot converge multi-source targets).** trials=1 smoke
`runs/spd0023-structural-selfcheck-retry-loop/7756f6b416d01b43` (11 cells, strict audit CLEAN). Flip targets
provider001/intercom001/hive001/netflix001/xero001 + asana001-control = **0/6**; canaries 5/5 hold.

**The loop FIRED** (artifact-proven): provider001 ran genuine structural self-checks
(`count(*) ... rows_unmatched_to_nucc`, `count(*) filter (where provider_taxonomy_code is null)`,
distinct-NPI counts) and REBUILT the models 7-9× — exactly the build→check→rebuild loop. It still didn't
converge. **Root cause = the retry checks the built table against the worker's OWN derivation of the correct
structure, and for multi-source cells that derivation is itself the variance.** The worker can't reliably
determine what the full base-set should be (which sources compose 874 nucc codes / 85196 NPIs) without gold,
so retrying against a self-derived (sometimes-wrong) target never reaches gold. The "oracle-free structural
signature" is only oracle-free if you can reliably derive the target structure — and that derivation IS the
wall. (asana001 lands 2/3 elsewhere because its target is trivially one source table; here it ran low =
single-draw variance.) The mode-2 decision-table follow-up is futile: the problem is target-DERIVATION, not
fix-mapping. @baseline unchanged. Concludes the README-lever program (see
`_artifacts/readme-lever-program-endpoint-2026-06-28.md`).
