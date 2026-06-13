---
id: h0054
title: Lap-time average — when accounting for pit stops, EXCLUDE pit-stop laps before averaging; do not keep them and subtract pit-stop duration
status: propose
kind: hypothesis
source: Captain request 2026-06-13 from _proposal/leverable-flipped-tasks-research-2026-06-13.md (CARD 2, f1010-medium). Method artifact-confirmed 2026-06-13 (h0043 PASS = exclude pit laps; h0037 FAIL = subtract pit duration, Got 1092). Forks the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133).
started: 2026-06-13T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`f1010-medium` builds `analysis__lap_times` (lap times by track/year, accounting for pit
stops). It flips on one locally-ambiguous convention:

- **A (oracle-correct):** EXCLUDE pit-stop laps before averaging. The h0043 passing run
  committed this (e.g. "101 pit laps excluded" for Zandvoort 2023; recomputed non-pit average
  matched the oracle).
- **B (the failure):** KEEP the full lap spine and SUBTRACT pit-stop duration per lap
  (`avg(lap_time - pit_duration)`, anomalous rows left unadjusted). The h0037 failing run
  committed this → `AUTO_analysis__lap_times_equality` Got 1092.

**Verifier note (verified):** the equality test compares the submission against TWO seed
tables — the base seed and `…_exclude_pit_stops` — and passes if it matches EITHER. The EXCLUDE
convention matches the exclude-seed; the SUBTRACT approach is a third computation that matches
NEITHER, which is why it fails. So pinning EXCLUDE is both correct and sufficient.

**Falsifiable claim (the single README change — Implementation stage only):** adding a
precondition-gated worked-example skeleton — "when averaging lap times accounting for pit
stops, filter out pit-stop laps before the aggregate; do not retain them and subtract
pit-stop duration" — will make the committed `analysis__lap_times.sql` use the exclude shape,
flipping `f1010-medium` FAIL→PASS, without regressing the canary panel.

**The single proposed README skeleton (generic identifiers, Implementation stage):**

```text
LAP-TIME (and similar duration) AVERAGE WITH PIT STOPS (gated). When a task asks for an
average/aggregate of lap times (or analogous per-event durations) that must "account for"
pit stops, EXCLUDE the pit-stop laps before the aggregate. Do NOT keep pit-stop laps in the
spine and subtract pit-stop duration from the lap time.

BEFORE (keeps pit laps, subtracts duration — AVOID):
    select track, year, avg(lap_time - pit_stop_duration) as avg_lap
    from laps group by track, year

AFTER (drop pit laps, then average):
    select track, year, avg(lap_time) as avg_lap
    from laps
    where not is_pit_lap                      -- pit-stop laps excluded before the average
    group by track, year
```

## Acceptance criteria

**AC-1 — Exactly one README change; specs differ only in `experiment:` + `solver_workflow:`.**
README diff vs the h0052 solver README adds exactly one Implementation-stage gated block (the
lap-time exclude-pit-laps rule); the other four levers, leak-guard, and the remaining stages
byte-identical. No `AUTO_*`/`solution__*`/`check_*`/`analysis__lap_times`/`exclude_pit_stops`/
expected-value token; no web-fetch token. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved.

**AC-2 — Every score paired with a clean strict audit** (`tainted: 0`, `coverage_missing: 0`,
`captured > 0`).

**AC-3 — The decisive read is the committed artifact.** Read the committed
`analysis__lap_times.sql` from the ensign `apply_patch`. Classify: does it FILTER OUT pit-stop
laps before the average (exclude), or keep them and subtract duration? A flip is credited only
when the exclude shape lands AND the verifier passes.

**AC-4 — No regression-canary loss.** All `@baseline` passers in the smoke panel stay PASS.
Any canary regression is a NO-GO unless artifact-proven unrelated single-trial variance and the
captain accepts the risk.

**AC-5 — Reproducibility judged against the base rate.** f1010-medium is ~73% at @baseline.
Smoke runs it as ≥2 seed-perturbed repeats; GO requires the exclude artifact + verifier pass +
clean audit on every repeat.

## Target dataset

Primary target: `ade-bench-f1010-medium`.

Smoke panel (target + canaries):
- `ade-bench-f1010-medium` — 🎯 target.
- `ade-bench-f1005` — ✅ same-family f1 canary (standings/points — proves the lap-time rule
  does not bleed onto the max-points construct).
- `ade-bench-f1006` — ✅ same-family f1 canary (max-points construct).
- `ade-bench-f1007` — ✅ same-family f1 canary (stable passer).
- `ade-bench-airbnb001`, `ade-bench-quickbooks002` — ✅ cross-family canaries.

GO requires the exclude artifact read on f1010-medium (≥2 repeats) + every canary PASS on a
clean audit.

## Honest tension with the standing decisions

- **Bleed risk: LOW.** The rule is narrowly gated to lap-time (duration) averages that account
  for pit stops; it is the cleanest single-construct candidate, the same "pin-the-correct-
  convention" shape that made the max-points lever (h0044) work.
- **`trials: 1`.** A ~73% cell; the lever raises the per-draw probability of the exclude shape.
  Judge by committed artifact (AC-3), not the single reward.

Method/README change only. Forks @baseline h0052 (`solver_workflows/h0052-compose-maxpoints-featureguard-scoped-coverage`, runtime codex); no dataset, harness, or runtime change.

## Gatekeeper review

**Recommendation: APPROVE** — clean single-stage gated worked-example skeleton, leak-guard byte-identical, specs two-field, both frozen, no FAILs; G11 single-model count is hypothesis-asserted (not in taxonomy) but the lever covers the only scored model, so it cannot mis-credit.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-13T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff = one hunk `166a167,181`, the lap-time exclude-pit-laps block; inserted at line 167, between `## Stage: Implementation` (L50) and `## Stage: Validation` (L182) → one stage, one idea. |
| G2 leak-guard intact | PASS | `diff` lines 1-166 IDENTICAL to parent (leak-guard prose byte-identical); grep of the added range (167-181) for `AUTO_*`/`solution__*`/`check_*`/`verifier`/`equality test`/`expected`/`curl`/`wget`/`git clone`/`analysis__lap_times`/`exclude_pit_stops` = empty (the token hits at L9-26 are the unchanged baseline guardrail). |
| G3 spec two fields | PASS | `diff baseline.yaml h0054.yaml` shows only `experiment:` (L2) and `solver_workflow:` (L11); `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | smoke diff adds only a `benchmark.tasks:` block; all 10 slugs `ade-bench-` prefixed; target `ade-bench-f1010-medium` present; includes h0052 banked-flip must-holds (airbnb009/f1006/f1006-hard) + per-family canaries. |
| G5 both frozen | PASS | `ls` confirms both `…frozen.yaml` and `…smoke.frozen.yaml` exist; both carry `agent.kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text ("EXCLUDE the pit-stop laps before the aggregate … do NOT keep … and subtract pit-stop duration") matches the Falsifiable claim exactly; generative-mechanical filter (`where not is_pit_lap`), not self-anchored verification; no scope creep (rest of README + tail byte-identical). |
| G7 actionability/inert-risk | PASS | Carries a worked-example BEFORE/AFTER SQL skeleton (the copyable `where not is_pit_lap` filter form), not abstract structural prose — the favored mechanical form. |
| G8 regression-canary coverage | N/A | Lever is precondition-GATED ("when a task asks for an average/aggregate of lap times … that must account for pit stops"), NOT generative → N/A; panel nonetheless carries ≥1 passing canary per non-target family (airbnb001/asana002/ana-eng001/quickbooks002) + 2 perturbable f1 canaries (f1005/f1007). |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — single derivation. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever — a generative-but-gated construct substitution. |
| G11 multi-model-target risk | N/A (taxonomy-unverified) | f1010-medium is NOT in the taxonomy's multi-model list (only airbnb007 is); the hypothesis's verified note states it is scored by a single equality test (`AUTO_analysis__lap_times_equality`, matched against either of two seed tables = one model) and the lever covers that model → lever covers all scored models. Scored-model count is hypothesis-asserted, not independently confirmed from the dataset tests by the gatekeeper. |
| G12 decision-fork probe quality | N/A | No `## Pre-smoke Decision-Fork Probe` block, but the hypothesis explicitly states why one was skipped: the method is artifact-confirmed from prior runs (h0043 PASS committed the EXCLUDE artifact; h0037 FAIL committed the SUBTRACT artifact, `Got 1092`) — the fork is already observed in committed SQL, not a simulated probe. |

**For the captain:** No FAILs — clear to advance to `smoke`. Two WARN-adjacent notes to glance at: (1) G11 — the single-scored-model claim for f1010-medium is the hypothesis's own "verified" note, not independently re-enumerated by the gatekeeper from the dataset tests; if you want belt-and-suspenders, confirm the scored-model count from `…/verifier/test-stdout.txt` at smoke before crediting. (2) f1010-medium already passed the h0052 single draw (~73% cell), so the smoke GO must rest on the EXCLUDE artifact landing across the ≥2 seed-perturbed repeats (AC-3/AC-5), not on a single reward.

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver (h0052) → solver_workflows/h0054-lap-time-average-exclude-pit-stop-laps; add ONLY the lap-time exclude-pit-laps worked-example skeleton as a new precondition-gated Implementation rule.
  `rk registry resolve run @baseline` = h0052 (dcb1a62ef4066133); `diff` vs parent README = one hunk (166a167,181), the gated lap-time block in `## Stage: Implementation`; all 4 existing levers + leak-guard byte-unchanged (AC-1).
- DONE: Build FULL spec (cp baseline.yaml; set ONLY experiment + solver_workflow) AND smoke spec (FLIP TARGET f1010-medium + MUST-HOLD h0052 banked flips airbnb009/f1006/f1006-hard + per-family canaries + 2nd perturbable f1 canary f1005); resolve each smoke task @baseline reward; freeze both with --allow-missing.
  FULL diff vs baseline.yaml = only `experiment:` + `solver_workflow:`; smoke diff = only `benchmark.tasks` (10 tasks). All 10 smoke tasks @baseline (h0052 dcb1a62ef4066133) = 1.0 PASS. Both frozen files written.
- DONE: Run the gatekeeper and write `## Gatekeeper review` (per-rule PASS/WARN/FAIL + APPROVE/REVISE/REJECT). Did NOT launch any rk run.
  Gatekeeper recommendation = APPROVE; no FAILs; G1-G7 PASS, G8/G9/G10/G11/G12 N/A (gated, not generative; not a selector; not self-correcting; single scored model; artifact-confirmed in place of probe).

### Summary
Forked the live @baseline (h0052 3-lever composition) into h0054 and added exactly one precondition-gated Implementation rule: when averaging lap times "accounting for" pit stops, EXCLUDE pit-stop laps before the aggregate (do NOT keep them and subtract pit duration). README diff is a single byte-clean hunk with all 4 prior levers and the leak-guard intact (AC-1). FULL and smoke specs differ from baseline only in the allowed fields; both frozen. Notable: in the h0052 single @baseline draw f1010-medium already PASSED (it is a ~73% cell), so the smoke GO must rest on the EXCLUDE artifact landing across ≥2 seed-perturbed repeats (AC-3/AC-5), not on a single reward flip — flagged in the gate table below and by the gatekeeper. Gatekeeper recommends APPROVE with no FAILs.
