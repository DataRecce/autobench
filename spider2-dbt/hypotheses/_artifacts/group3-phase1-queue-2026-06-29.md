# Group-3 Phase-1 queue — single-mechanism never-pass (concept spd0039, off NEW champion spd0038)
Autonomous loop: ≤2 concurrent smokes, target trials=3 + 1 canary. GO = target reliably passes (0→3/3 = clean flip; 2/3 = partial-note) AND canary holds. NO-GO → diagnose transcript (did directive engage? hit multi-step execution wall?), revise (cap 3) or, if execution-walled, mark NEEDS-PHASE2 (stronger model). HELD for captain. Prune networks per launch; watch Jul-2 codex limit.

| # | hyp | target | canary | spec | status |
|---|-----|--------|--------|------|--------|
| 1 | spd0040 | movie_recomm001 | mrr001 | spd0040-movie-recomm-prefix-like | RUNNING |
| 2 | spd0041 | nba001 | app_reporting001 | spd0041-nba-read-snapshot-not-simulate | RUNNING |

Next tier (C1-family, lower confidence, queue if Phase-1 method validates): netflix001, intercom001, hive001.

## Log
- 2026-06-29 — concept spd0039 fired; spd0040+spd0041 forks authored off champion spd0038 (both verified: 6 stabilizer signatures intact, leak-safe); diagnoses verified (nba snapshot parquet exists, movie_recomm prefix-match in schema.yml). Launching both.
