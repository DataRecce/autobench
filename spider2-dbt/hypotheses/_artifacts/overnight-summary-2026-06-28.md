# Overnight summary — 2026-06-28 (concept spd0026, for captain morning review)

**Headline: v0.22 solver upgrade is board-neutral, and all 3 fresh-family levers (C7/C6/C2) are clean
NO-GOs at smoke with no real canary bleed. Nothing promoted, nothing run full — everything HELD for you.**

## 1. v0.22 re-baseline (STEP 0) — board-neutral, decision teed up
Champion solver spd0013 UNCHANGED, full 60-task board, under the new v0.22 spacedock solver plugin.
- **25 PASS / 34 FAIL / 1 EXC** (recharge001 = 2400s AgentTimeoutError, infra not regression → effective ~26/60).
- vs old v0.12 @baseline 27/60: **statistically the same board** — 19/20 rock-solid held (recharge001 lost
  only to the timeout), the 6 extra passes are exactly the flaky band. Confirms the upgrade is behavior-neutral.
- **DECISION FOR YOU:** re-point `@baseline` from the v0.12 run to the v0.22 run
  `runs/spd0013-rebaseline-v022/d826c153beb3134b` so future v0.22 deltas are comparable. Recommend yes.
  (Not auto-promoted.) Detail: `docs/v022-rebaseline-2026-06-28.md`.

## 2. Three fresh-family smokes — all NO-GO (held; no full, no promote)
| Hyp | Family | Targets | Result | Canaries |
|---|---|---|---|---|
| spd0027 | C7 author-missing-model | synthea001, xero_new001 | both **FAIL** | f1001/mrr001/quickbooks002 all held |
| spd0028 | C6 cast-before-string-op | social_media001 | **FAIL** | f1001/mrr001/quickbooks002/hubspot001 all held |
| spd0029 | C2 financial-statement spine | xero001, xero_new001, xero_new002 | all **FAIL** | mrr001/quickbooks002 held; f1001 infra-EXC |

- **spd0027 C7:** directive WAS read (3–5 agent-log mentions) but the multi-source builds didn't land →
  the execution wall (R5/R6 already in champion; sharpening doesn't make the build succeed).
- **spd0028 C6:** lever **didn't engage** (0 cast/split_part mentions) → social_media001's real residual is
  likely not the cast-before-split_part the catalog diagnosed, or the solver routed elsewhere. Re-diagnose
  before any retry.
- **spd0029 C2:** balance-sheet spine rule flipped nothing; xero is multi-model (overlaps the C7 wall) and
  the full derivation exceeds a single gated directive at trials=1.

**Net:** 0 new tasks flipped. Zero real canary regressions (the two infra EXCs — recharge001 timeout, f1001
NonZeroAgentExitCode — are not lever effects). This RECONFIRMS under v0.22 the prior program's conclusion:
the reachable never-pass set is bound by the execution wall, not by a missing README directive.

## 3. Infra notes
- recharge001: 2400s timeout on the re-baseline (rock-solid at v0.12). Watch for recurrence → bump its timeout.
- f1001: NonZeroAgentExitCodeError in the spd0029 smoke (rock-solid). One-off; not contamination (no usage-limit
  signal). No parallel boards were ever run; docker networks pruned between every launch.

## 4. Status / your calls
- All of spd0026's children (spd0027/28/29) are HELD at smoke = NO-GO. Recommend **conclude all 3 REJECTED**
  and concept spd0026 EXHAUSTED — but that's your conclude decision.
- @baseline re-point to the v0.22 run (above) — your promote decision.
- No outstanding codex runs; loop stopped.
