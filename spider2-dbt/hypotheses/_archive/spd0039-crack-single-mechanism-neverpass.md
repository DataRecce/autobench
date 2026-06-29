---
title: Crack the single-mechanism reachable never-pass cells (group-3) via focused directives off the new champion
status: concept
kind: concept
id: spd0039
source: "captain-directed (2026-06-29). Leaderboard top-1 = 65%/68 proves group-3 (never-pass) IS solvable. The residual catalog splits the ~13 reachable never-pass cells into MULTI-STEP (xero/synthea/provider/social_media — already README-NO-GO, execution-walled, need a stronger solver = Phase 2) vs SINGLE-MECHANISM (movie_recomm001/nba001/netflix001/intercom001/hive001 — one clean pinnable bifurcation, NEVER focus-tried). This concept applies the proven flaky-stabilization method (pin one bifurcation) to the single-mechanism never-pass cells. forks NEW champion spd0038."
started: 2026-06-29
completed:
verdict: NEEDS-PHASE2-readme-exhausted
archived: 2026-06-29T15:42:06Z
---

Phase 1 of the group-3 dig-in (captain decision: both Phase 1 README + Phase 2 model-swap-scope). These are
NEVER-PASS cells (no passing-draw oracle), so each directive comes from the catalog's offline
gold-reconstruction (read-only from source/schema.yml), encoded as a GENERAL leak-safe method. A flip here
is a genuine new pass (0/N → passing).

## Fan-out (priority: novel single-mechanism first)
- **spd0040 movie_recomm001** (C3, novel) — schema.yml documents a partial-title match (strip trailing year,
  match titles); implement as prefix-LIKE not equality, preserve natural fan-out, no per-key dedup. VERIFIED:
  schema.yml describes the match.
- **spd0041 nba001** (C5, novel) — graded cols are Monte-Carlo playoff milestones; a committed snapshot
  parquet ships (`data/data_catalog/season_summary_2024-04-15.parquet`); read it instead of re-running an
  unseeded simulation. VERIFIED: snapshot exists.
- (next tier, C1-family, lower confidence — completeness already broadly failed but not focus-tried per-cell):
  netflix001, intercom001, hive001.

## Method
Each fork = NEW champion spd0038 + ONE gated leak-safe directive. Smoke = target trials=3 + 1 canary.
GO = target reaches a reliable pass (ideally 3/3); a never-pass cell going 0→3/3 is a clean flip. NO-GO →
revise (cap 3) or, if it hits the multi-step execution wall, hand to Phase 2 (stronger model). HELD for captain.

## Phase 2 (parallel, scoping only — NOT launched)
See `_artifacts/group3-model-swap-scoping-2026-06-29.md` — cost/auth/cells for testing a stronger solver
model/runtime (gpt-5.5 → stronger codex, or runtime:claude/Opus) on the multi-step reachable cells README
can't crack. Captain greenlights the actual run separately.
