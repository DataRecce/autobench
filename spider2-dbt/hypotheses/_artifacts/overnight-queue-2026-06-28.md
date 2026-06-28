# Overnight autonomous queue — 2026-06-28 (concept spd0026: reachable fresh families)

**Captain directive (verbatim intent):** fire concept + dispatch each expanded hypothesis one-by-one
through to SMOKE without approval; HOLD at the smoke result (NO full run, NO promote); captain reviews
on waking. Standing rules still bind: trials=1 judge-by-artifact; NEVER run two codex boards in parallel;
docker network prune between runs; rk freeze from repo root; promote/full/conclude = captain only.

**HARD GATE — codex serialization:** the v0.22 re-baseline full board (handle
`spd0013-rebaseline-v022-20260628-153335`, run dir `runs/spd0013-rebaseline-v022/d826c153beb3134b`) is the
CURRENT codex board. Do NOT launch ANY smoke until its `done` sentinel exists. Then run the 3 smokes
SERIALLY — each smoke's `done` sentinel must exist before the next launches.

## State machine (each wake-up: read this file, find the first non-DONE step, act, update status here)

- [x] **STEP 0 — re-baseline finishes. DONE 2026-06-28 ~18:44.** v0.22 board = 25 PASS / 34 FAIL / 1 EXC
  (recharge001 = infra timeout, not a regression → effective ~26/60). Board-NEUTRAL vs v0.12 27/60 (inside
  flaky-band variance; 19/20 rock-solid held + 6 flaky-band flips). All 5 smoke targets confirmed STILL
  never-solved under v0.22 → DROP NONE. @baseline promotion teed up for captain (recommend re-point to
  runs/spd0013-rebaseline-v022/d826c153beb3134b; NOT auto-promoted). Detail: docs/v022-rebaseline-2026-06-28.md.

- [x] **STEP 1 DONE (NO-GO; synthea001 FAIL + xero_new001 FAIL, 3/3 canaries held) — SMOKE spd0027 (C7 author-missing-graded-model).** spec
  `specs/spd0027-author-missing-graded-model.smoke.frozen.yaml` (content_hash 845ba003). Targets:
  synthea001, xero_new001. Canaries: f1001, mrr001, quickbooks002. Prune docker networks, launch detached
  via `drivers/rk-run-detached.sh spd0027-smoke <frozen-spec> run`, set a background waiter on its sentinel.
  On done: audit (targets flipped? canaries held? coverage_missing/errored?), record result in the spd0027
  entity + here, HOLD (no full). Mark STEP 1 DONE.

- [x] **STEP 2 DONE (NO-GO; social_media001 FAIL, lever didn't engage, 4/4 canaries held) — SMOKE spd0028 (C6 cast-before-string-op).** spec
  `specs/spd0028-cast-before-string-op.smoke.frozen.yaml` (content_hash 4b327448). Target: social_media001.
  Canaries: f1001, mrr001, quickbooks002, hubspot001. Same launch+audit+HOLD protocol. Mark STEP 2 DONE.

- [~] **STEP 3 (RUNNING) — SMOKE spd0029 (C2 financial-statement-spine).** spec
  `specs/spd0029-financial-statement-spine.smoke.frozen.yaml` (content_hash 3aea076e). Targets: xero001,
  xero_new001, xero_new002. Canaries: f1001, mrr001, quickbooks002. Same protocol. Mark STEP 3 DONE.

- [ ] **STEP 4 — DONE.** Write a single overnight summary (re-baseline score + 3 smoke verdicts: which
  targets flipped, which canaries held/bled, any infra issues) for the captain's morning review. Stop the
  loop (no more wake-ups).

## Flip-target / canary cheat-sheet (lead with this when reporting each smoke)
- spd0027 C7 → FLIP targets: synthea001, xero_new001 | canaries (must hold): f1001, mrr001, quickbooks002
- spd0028 C6 → FLIP target: social_media001 | canaries: f1001, mrr001, quickbooks002, hubspot001
- spd0029 C2 → FLIP targets: xero001, xero_new001, xero_new002 | canaries: f1001, mrr001, quickbooks002

## Log (append per wake-up)
- 2026-06-28 ~15:5x — queue created; 3 forks authored + frozen (distinct content hashes); re-baseline still
  running (~43/60 at last check). STEP 0 pending re-baseline sentinel.

- 2026-06-28 ~18:44 — STEP 0 DONE: v0.22 board ~26/60 board-neutral; no targets dropped. @baseline promotion teed up.
- 2026-06-28 ~18:46 — STEP 1 launched: spd0027 C7 smoke (synthea001,xero_new001 + 3 canaries), pid 2302649.
- 2026-06-28 ~19:15 — STEP 1 DONE: spd0027 C7 NO-GO (both targets FAIL, canaries clean; execution wall). Launching STEP 2.
- 2026-06-28 ~19:43 — STEP 2 DONE: spd0028 C6 NO-GO (social_media001 FAIL, lever didn't engage; canaries clean). Launching STEP 3.
