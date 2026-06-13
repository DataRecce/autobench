---
id: h0054
title: Lap-time average — when accounting for pit stops, EXCLUDE pit-stop laps before averaging; do not keep them and subtract pit-stop duration
status: hypothesis
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
