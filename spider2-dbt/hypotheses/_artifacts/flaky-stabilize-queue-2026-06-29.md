# Flaky-stabilization autonomous queue — 2026-06-29 (concept spd0030)

**Captain directive:** target the flipped-but-not-banked (flaky) cells; fine-tune the champion README to make
each consistently pass. Auto-dispatch each hypothesis to SMOKE without approval. GO → HOLD (no full, no
promote) + switch to next. NO-GO → revise the directive MULTIPLE times until no method works, then drop.
Smoke = TARGET at trials=3 (consistency) + 1 canary. **Up to 2 smokes CONCURRENT.** Frequent, focused.

## Codex-concurrency rule
At most **2** smokes running at once. Each smoke = 2 tasks × 3 trials = 6 cells. Different target tasks →
no backend collision (per-task duckdb, isolated workspace). Prune docker networks before each launch. Watch
for codex usage-limit (resets Jul 2) — if hit, pause and report.

## GO / NO-GO / revise rules
- **GO** = target 3/3 AND canary holds (≥ its rock-solid norm) → record in entity, conclude-pending HOLD, free slot.
- **NO-GO** = target <3/3 OR canary regression. Diagnose from the smoke transcript (did the directive ENGAGE?
  did it engage but still fail? did the canary bleed?). REVISE the fork's directive accordingly, re-freeze,
  re-smoke (same hypothesis, revision N+1). Cap at **3 revisions**; then mark NO-GO/exhausted, free slot.
- Never run full board, never promote — all HELD for captain.

## Hypothesis queue (priority order: NEW-rule cells first = highest GO odds)
| # | hyp | target | canary | spec (frozen) | kind | status | revs |
|---|-----|--------|--------|---------------|------|--------|------|
| 1 | spd0031 | quickbooks003 | quickbooks002 | spd0031-qb003-reuse-shipped-upstream | NEW | RUNNING-rev1(h=spd0031-smoke-rev1-20260629-024422) | 1 |
| 2 | spd0032 | sap001 | marketo001 | spd0032-sap-reaggregate-long-to-grain | NEW | **GO 3/3 (HELD)** | 0 |
| 3 | spd0033 | divvy001 | f1001 | spd0033-divvy-staging-test-warn-not-filter | NEW | RUNNING-rev1(h=spd0033-smoke-rev1-20260629-025321) | 1 |
| 4 | spd0034 | asset001 | app_reporting001 | spd0034-asset-round-final-product-only | NEW | rev0 NO-GO(1/3)→QUEUED-rev1 | 1 |
| 5 | spd0035 | greenhouse001 | hubspot001 | spd0035-greenhouse-no-string-cast-id | SHARPEN | QUEUED | 0 |
| 6 | spd0036 | airbnb001 | mrr001 | spd0036-airbnb-window-anchor-rowcount-check | SHARPEN | QUEUED | 0 |
| 7 | spd0037 | apple_store001 | google_play001 | spd0037-applestore-raw-grouping-key | SHARPEN | QUEUED | 0 |

## Loop procedure (each wake-up)
1. Read this table. Count RUNNING smokes (handles without `done`). If <2 and a QUEUED hyp exists, launch the
   next: prune networks → `drivers/rk-run-detached.sh <hyp>-smoke specs/<spec>.frozen.yaml run` → set sentinel
   waiter → mark RUNNING. Fill up to 2 concurrent.
2. For any RUNNING smoke whose `done` exists: audit (target 3/3? canary held?). GO → record + HOLD + DONE.
   NO-GO → revise+re-freeze+re-smoke (rev++) or, if revs==3, mark NO-GO-EXHAUSTED + DONE. Free the slot.
3. Re-arm a ~900s ScheduleWakeup with the loop prompt while any hyp is QUEUED/RUNNING. When all 7 are
   DONE/EXHAUSTED, write the summary (_artifacts/flaky-stabilize-summary-...) and STOP re-arming.

## Log
- 2026-06-29 — queue created; 7 forks authored + frozen (distinct hashes); concept spd0030 fan-out set.
  lever001/workday001 DROPPED (champion-stable, not intrinsically flaky). Launching slots 1+2 (spd0031, spd0032).
- 2026-06-29 ~01:46 — slots 1+2 launched concurrently: spd0031 (qb003) pid2423168, spd0032 (sap001) pid2423201.
- 2026-06-29 ~02:15 — spd0032 sap001 GO (3/3, held); slot freed → launched spd0033 divvy001 pid2486398. spd0031 still running.
- 2026-06-29 ~02:30 — spd0031 rev0 NO-GO (qb003 0/3 backfired, canary held); revised→rev1 (R3 stub + no-widen-spine), re-queued. spd0031 done freed slot → launching spd0034 asset001.
- 2026-06-29 ~02:44 — spd0033 divvy001 rev0 NO-GO (0/3, directive not-engaged/still-filtered); revised→rev1 (hard anti-pattern), re-queued. spd0033 freed slot → launched spd0031-rev1 pid2547066. Running: spd0034 + spd0031-rev1.
- 2026-06-29 ~03:00 — spd0034 asset001 rev0 NO-GO (1/3; recharge001 weak canary→swap app_reporting001); revised→rev1 (concrete round form+self-check), re-queued. spd0034 freed slot → launching spd0033-rev1 divvy.
