# Group-3 Phase-1 queue — single-mechanism never-pass (concept spd0039, off NEW champion spd0038)
Autonomous loop: ≤2 concurrent smokes, target trials=3 + 1 canary. GO = target reliably passes (0→3/3 = clean flip; 2/3 = partial-note) AND canary holds. NO-GO → diagnose transcript (did directive engage? hit multi-step execution wall?), revise (cap 3) or, if execution-walled, mark NEEDS-PHASE2 (stronger model). HELD for captain. Prune networks per launch; watch Jul-2 codex limit.

| # | hyp | target | canary | spec | status |
|---|-----|--------|--------|------|--------|
| 1 | spd0040 | movie_recomm001 | mrr001 | spd0040-movie-recomm-prefix-like | **NEEDS-PHASE2 (rev0+rev1 both 0/3; fuzzy-join execution wall)** |
| 2 | spd0041 | nba001 | app_reporting001 | spd0041-nba-read-snapshot-not-simulate | **NEEDS-PHASE2 (0/3; snapshot engaged 27x but multi-step integration wall)** |

Next tier (C1-family, lower confidence, queue if Phase-1 method validates): netflix001, intercom001, hive001.

## Log
- 2026-06-29 — concept spd0039 fired; spd0040+spd0041 forks authored off champion spd0038 (both verified: 6 stabilizer signatures intact, leak-safe); diagnoses verified (nba snapshot parquet exists, movie_recomm prefix-match in schema.yml). Launching both.
- 2026-06-29 ~15:10 — Phase-1 first results: BOTH 0/3. nba001 = NEEDS-PHASE2 (directive engaged heavily [season_summary 27x] but couldn't integrate the snapshot into the graded model = multi-step execution wall; don't revise). movie_recomm001 rev0 = directive engaged (prefix/fan-out/strip) BUT solver still deduped (distinct 7x) → 9817 not 56596; revised→rev1 (HARD no-dedup + rowcount self-check), re-smoking. canary mrr001 1/3 = own variance (title-match gate can't touch it).

## PHASE 1 CONCLUDED (2026-06-29) — 0 flips; README cannot crack never-pass cells (execution wall)
Both single-mechanism never-pass targets NO-GO at trials=3 even though the directive ENGAGED:
- **nba001** (spd0041): NEEDS-PHASE2 — referenced the snapshot 27x but couldn't integrate it into the graded model (multi-step wall).
- **movie_recomm001** (spd0040): NEEDS-PHASE2 — rev0 still deduped (0/3); rev1 forceful no-dedup + rowcount self-check STILL 0/3 (the prefix-LIKE fan-out join to the exact gold shape is multi-step the solver can't nail). canary mrr001 recovered 3/3 (earlier 1/3 was own variance).
CONCLUSIVE across 6 never-pass cells (spd0027/28/29 + spd0040/41): a README directive can TEACH the recipe + the solver READS it, but gpt-5.5 cannot EXECUTE the multi-step build → true never-pass cells (0/N ever) do NOT flip from prose. The flaky-stabilization method worked ONLY because those cells had a passing-draw oracle (the solver could already execute it sometimes). NOT queuing next tier (netflix/intercom/hive) — no flip. **Path to group-3 = Phase 2 (stronger solver model)**, scoped in group3-model-swap-scoping-2026-06-29.md, BLOCKED on captain confirming an available stronger model + auth. HELD; nothing promoted; loop STOPPED.
