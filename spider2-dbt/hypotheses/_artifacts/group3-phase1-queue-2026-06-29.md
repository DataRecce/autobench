# Group-3 Phase-1 queue — single-mechanism never-pass (concept spd0039, off NEW champion spd0038)
Autonomous loop: ≤2 concurrent smokes, target trials=3 + 1 canary. GO = target reliably passes (0→3/3 = clean flip; 2/3 = partial-note) AND canary holds. NO-GO → diagnose transcript (did directive engage? hit multi-step execution wall?), revise (cap 3) or, if execution-walled, mark NEEDS-PHASE2 (stronger model). HELD for captain. Prune networks per launch; watch Jul-2 codex limit.

| # | hyp | target | canary | spec | status |
|---|-----|--------|--------|------|--------|
| 1 | spd0040 | movie_recomm001 | mrr001 | spd0040-movie-recomm-prefix-like | rev0 NO-GO(0/3, still deduped)→RUNNING-rev1 |
| 2 | spd0041 | nba001 | app_reporting001 | spd0041-nba-read-snapshot-not-simulate | **NEEDS-PHASE2 (0/3; snapshot engaged 27x but multi-step integration wall)** |

Next tier (C1-family, lower confidence, queue if Phase-1 method validates): netflix001, intercom001, hive001.

## Log
- 2026-06-29 — concept spd0039 fired; spd0040+spd0041 forks authored off champion spd0038 (both verified: 6 stabilizer signatures intact, leak-safe); diagnoses verified (nba snapshot parquet exists, movie_recomm prefix-match in schema.yml). Launching both.
- 2026-06-29 ~15:10 — Phase-1 first results: BOTH 0/3. nba001 = NEEDS-PHASE2 (directive engaged heavily [season_summary 27x] but couldn't integrate the snapshot into the graded model = multi-step execution wall; don't revise). movie_recomm001 rev0 = directive engaged (prefix/fan-out/strip) BUT solver still deduped (distinct 7x) → 9817 not 56596; revised→rev1 (HARD no-dedup + rowcount self-check), re-smoking. canary mrr001 1/3 = own variance (title-match gate can't touch it).
