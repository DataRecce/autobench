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

- [ ] **STEP 0 — re-baseline finishes.** When `runs/.rk-handles/spd0013-rebaseline-v022-20260628-153335/done`
  exists: audit the board (coverage_missing / errored / usage-limit), compute v0.22 score vs old v0.12
  baseline (spd0013 27/60, true ~20 rock-solid), write the result, and tee up the @baseline promotion
  decision for the captain (do NOT promote). Then recompute the v0.22 never-solved set and for each smoke
  below, DROP any target the v0.22 board now PASSES (note it). Mark STEP 0 DONE.

- [ ] **STEP 1 — SMOKE spd0027 (C7 author-missing-graded-model).** spec
  `specs/spd0027-author-missing-graded-model.smoke.frozen.yaml` (content_hash 845ba003). Targets:
  synthea001, xero_new001. Canaries: f1001, mrr001, quickbooks002. Prune docker networks, launch detached
  via `drivers/rk-run-detached.sh spd0027-smoke <frozen-spec> run`, set a background waiter on its sentinel.
  On done: audit (targets flipped? canaries held? coverage_missing/errored?), record result in the spd0027
  entity + here, HOLD (no full). Mark STEP 1 DONE.

- [ ] **STEP 2 — SMOKE spd0028 (C6 cast-before-string-op).** spec
  `specs/spd0028-cast-before-string-op.smoke.frozen.yaml` (content_hash 4b327448). Target: social_media001.
  Canaries: f1001, mrr001, quickbooks002, hubspot001. Same launch+audit+HOLD protocol. Mark STEP 2 DONE.

- [ ] **STEP 3 — SMOKE spd0029 (C2 financial-statement-spine).** spec
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
