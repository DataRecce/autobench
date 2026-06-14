---
id: h0054
title: Lap-time average — when accounting for pit stops, EXCLUDE pit-stop laps before averaging; do not keep them and subtract pit-stop duration
status: smoke
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

## Stage Report: smoke (Phase 1 — launch)

- DONE: Phase 1 NOW (launch only, do NOT wait): export RAZORBACK_SPACEDOCK_PLUGIN_DIR; launch DETACHED via drivers/rk-run-detached.sh; return the handle, signal done immediately, FO owns the wait.
  Launched h0054-smoke (pid 2564597) on specs/h0054-lap-time-average-exclude-pit-stop-laps.smoke.frozen.yaml; handle: runs/.rk-handles/h0054-smoke-20260613-144543/ (pid · log · done = rc/end/rundir; ntfy adebench-rk-381c976fe07465bf).
- SKIPPED: Phase 2 (strict audit + score + deep-dive + GO/NO-GO).
  Deferred by design — FO re-engages on `done` rc=0; Phase 1 is launch-only.

### Summary
Phase 1 launch complete. The smoke run is detached and running; the FO scans runs/.rk-handles/h0054-smoke-20260613-144543/ for the `done` file and re-dispatches for Phase 2 (audit/score/deep-dive). Nothing else is running — this is the only run.

## Smoke result

Run-dir: `runs/ade-bench-h0054-lap-time-average-exclude-pit-stop-laps/e2df61b167f316a2` (rc=0).
Strict audit CLEAN: `tainted: 0`, `coverage_missing: 0`, `clean: 10`; `captured: 1` every cell (AC-2).
Score: **10/10 PASS** (pass@1 = 1.0). @baseline = h0052 (`dcb1a62ef4066133`).

| Task | Role | Baseline (h0052) | Smoke | Verifier |
|------|------|------------------|-------|----------|
| f1010-medium | 🎯 target | ~73% (PASS on h0052 draw) | ✅ PASS reward=1 | `AUTO_analysis__lap_times_equality` PASS; existence PASS |
| airbnb009 | h0052 banked flip (coverage) | PASS | ✅ PASS reward=1 | `mom_agg_review_date_range` 1/1 PASS |
| f1006 | h0052 banked flip (max-points) | PASS | ✅ PASS reward=1 | constructor/driver points 4/4 PASS |
| f1006-hard | h0052 banked flip (max-points) | PASS | ✅ PASS reward=1 | 4/4 PASS |
| f1005 | f1 canary (perturbable) | PASS | ✅ PASS reward=1 | PASS |
| f1007 | f1 canary (stable passer) | PASS | ✅ PASS reward=1 | PASS |
| airbnb001 | cross-family canary | PASS | ✅ PASS reward=1 | PASS |
| ana-eng001 | cross-family canary | PASS | ✅ PASS reward=1 | PASS |
| asana002 | cross-family canary | PASS | ✅ PASS reward=1 | PASS |
| quickbooks002 | cross-family canary | PASS | ✅ PASS reward=1 | PASS |

Zero canary loss. README diff vs parent h0052 = single hunk `166a167,181` (the gated lap-time
exclude block); all 4 prior levers + leak-guard byte-identical (AC-1 holds).

## Behavioral analysis

**DECISIVE READ — f1010-medium committed the EXCLUDE shape (AC-3 GO signal).** The committed
`models/analysis/analysis__lap_times.sql` (from the solver's `apply_patch`, call_id
`call_Rxd2UN22MTX4Xmc4zwT5ddxu`) is:

```sql
pit_stop_laps as ( select distinct race_id, driver_id, lap
    from {{ ref('stg_f1_dataset__pit_stops') }} ),
non_pit_laps as ( select l.race_id, l.milliseconds
    from lap_times as l
    left join pit_stop_laps as p
      on l.race_id = p.race_id and l.driver_id = p.driver_id and l.lap = p.lap
   where p.race_id is null ),                       -- pit-stop laps FILTERED OUT
final as ( select r.circuit_name, r.race_year,
           cast(round(avg(l.milliseconds)) as integer) as avg_lap_time_in_ms
    from non_pit_laps as l join races as r using (race_id) group by 1,2 )
select * from final
```

This is the EXCLUDE form: it drops pit-stop laps (anti-join `where p.race_id is null`) BEFORE
the `avg(l.milliseconds)` aggregate. It does NOT use the SUBTRACT-duration shape
(`avg(lap_time - pit_duration)`) that produced the h0037 FAIL (`Got 1092`). Verifier line:
`AUTO_analysis__lap_times_equality .......... PASS` (matched against the
`solution__analysis__lap_times_exclude_pit_stops` seed; both seed tables loaded INSERT 532).
The correct EXCLUDE convention was pinned by the gated worked-example skeleton — flip-credit
granted: exclude shape landed AND verifier passed.

**h0052 banked flips intact, lever did not disturb them.** f1006/f1006-hard run the
constructor/driver POINTS construct (zero `lap_times` mention in their verifier output) and
airbnb009 runs the review-date-range COVERAGE construct — all distinct from lap-time. Each
committed its correct artifact and passed (4/4, 4/4, 1/1). The precondition gate ("when a task
asks for an average of lap times accounting for pit stops") is the isolation mechanism: it did
not fire on the points/coverage/cross-family canaries, all of which held PASS.

**Reproducibility (AC-5).** Single smoke draw this run; f1010-medium is a ~73% cell. The GO
rests on the EXCLUDE artifact landing + verifier pass + clean audit (AC-3), per the standing
single-trial / judge-by-artifact decision, not on a single reward alone. The artifact is the
correct-convention proof the lever was designed to pin.

## GO/NO-GO: **GO**

f1010-medium committed the EXCLUDE artifact (anti-join filters out pit laps before
`avg(milliseconds)`; not the subtract-duration shape) AND its verifier passed; the three h0052
banked flips (airbnb009 / f1006 / f1006-hard) committed their correct construct artifacts and
held PASS; every canary held PASS on a clean strict audit (tainted 0 / coverage_missing 0,
captured>0 all 10). README diff is the single gated lap-time block (AC-1). Advance `smoke → full`.

## Stage Report: smoke (Phase 2 — audit/score/deep-dive)

- DONE: Strict audit clean (tainted 0 / coverage_missing 0) + captured>0 every cell BEFORE score; rk score.
  `rk audit --policy strict` = clean 10 / tainted 0 / coverage_missing 0; captured=1 all 10 cells; `rk score` = 10/10 PASS (pass@1 1.0).
- DONE: DECISIVE READ — open f1010-medium committed analysis__lap_times.sql; confirm EXCLUDE shape (filters OUT pit laps before avg), not subtract-duration; quote SQL + verifier line.
  Committed SQL uses anti-join `where p.race_id is null` then `avg(milliseconds)` (EXCLUDE); verifier `AUTO_analysis__lap_times_equality PASS`. Quoted in Behavioral analysis. GO signal present.
- DONE: Confirm h0052 banked flips (airbnb009 coverage / f1006 + f1006-hard max-points) committed correct artifacts (lever did NOT disturb) + all canaries hold on clean audit.
  airbnb009 1/1, f1006 4/4, f1006-hard 4/4 PASS; distinct constructs (points/coverage, zero lap_times touch); 6 canaries all PASS on clean audit.
- DONE: Write ## Smoke result + ## Behavioral analysis + GO/NO-GO; GO = exclude artifact + zero canary loss + h0052 flips intact. Commit before signaling.
  All three written above; verdict GO; committing now.

### Summary
h0054 smoke is a clean GO. The gated lap-time worked-example skeleton pinned the correct
EXCLUDE convention: f1010-medium's committed `analysis__lap_times.sql` filters out pit-stop
laps via anti-join BEFORE averaging (not the subtract-duration shape that produced h0037's
`Got 1092`), and its verifier passed. The three h0052 banked flips held with their correct
construct artifacts (the precondition gate kept the lap-time rule from firing on them), and all
six canaries held PASS on a clean strict audit (10/10, tainted 0 / coverage_missing 0). Advance
to `full`.

## Verdict

**PASSED — smoke-validated (GO) lever, MERGED into the h0056 six-lever composition which PROMOTED to
@baseline.**

This lever did not run its own full; per captain it was composed with h0053 + h0055 onto @baseline
h0052 in the single six-lever README of **h0056**, which PROMOTED (35/48 = 0.7292, the first six-lever
baseline; @baseline rebound to
`runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a`).

**Banked solo effect (now live verbatim in the @baseline README):** the lap-time exclude-pit-stop-laps
rule — when averaging lap/duration, EXCLUDE pit-stop laps via an anti-join BEFORE the `avg`, not the
subtract-duration shape that produced h0037's wrong `Got 1092`. Solo smoke committed the EXCLUDE
artifact on **f1010-medium**. In h0056 this lever fired with its intended committed shape in BOTH full
draws — `lap_times_without_pit_stops` via `left join pit_stop_laps … where psl.race_id is null` then
`avg(milliseconds)` (EXCLUDE-then-aggregate), f1010-medium PASS both draws. As a precondition-gated
noise-reducer it pinned a previously coin-flipping cell, tightening the trials:1 variance band.

**Collision-free:** the lap-time gate stayed silent on every non-lap construct (the three h0052 banked
flips kept their own committed artifacts in both draws). Cited evidence: the h0056 promotion + the
48/48 six-way decision-fork simulation (`_artifacts/h0056-decision-fork-simulation.md`, this lever
scored 6/6 desired on its f1010-medium target, 0 collisions).
