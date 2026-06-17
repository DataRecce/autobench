---
id: dab0010
title: Anti-abstention LEAN v2 (None carve-out + failure-gated persistence)
status: smoke
kind: hypothesis
source: dab0009 follow-up (REJECTED as board lever — verbose v1 perturbed stable cells); captain-directed v2
started: 2026-06-17T13:06:22Z
completed:
verdict:
score: 0.85
worktree:
---

## Hypothesis

dab0009 proved the anti-abstention diagnosis is real (flips googlelocal-q3 3/3, artifact-confirmed) but
its **verbose** form perturbed otherwise-stable cells board-wide (PANCANCER-q2 / crmarenapro-q7 /
crmarenapro-q12 are 6/7–7/7 across 5 Opus + 5 CAIS + our runs, yet failed only in the v1 lever run). The
pre-smoke decision sims traced the harm to two concrete clauses. **v2 keeps the flip and removes the two
harm mechanisms** via a minimal, gated rule.

**The v2 README change** (fork `spacedock-readme-baseline` → `dab0010-anti-abstention-lean`), two edits,
nothing else:

- **`## Rules`** — replace the baseline abstention line with:
  > "Do not abstain prematurely. Return `UNABLE TO DETERMINE` only as a last resort when the data is
  > genuinely unreachable — and only after trying the connection paths named in `connections.yaml` and
  > `db_config.yaml`. When the data is reachable, commit your best computed answer.
  > A substantive negative result is a **real answer, not an abstention**: if the correct answer is
  > `None`, `0`, an empty set, or 'no match / no violation found', return it. This rule never means
  > preferring a positive value over a correct negative one."
- **`## Database Access`** — add ONE failure-gated sentence:
  > "If (and only if) a connection attempt **fails**, consult `db_config.yaml` for an alternate
  > connection detail before treating the source as unavailable. If your existing connection already
  > works, keep it — do not switch methods or re-resolve sources."

Leak-guard (no external data / ground-truth lookup) preserved verbatim. The **None carve-out** fixes the
crmarenapro-q7 None-suppression risk; the **failure-gated** clause fixes the PANCANCER-q2
source-reconciliation perturbation. Both were the v1 harm mechanisms.

**Targets:**
- **Keep the flip:** googlelocal-q3 (the real abstention flip — must survive v2).
- **Recover (no regress):** PANCANCER-q2, crmarenapro-q7, crmarenapro-q12.
- **Measure-only (NOT counted as a lever target):** agnews-q4 — a near-tie classification coin-flip the
  rule provably cannot control (sim: INSUFFICIENT). Reported for completeness only.

## Pre-smoke Decision-Fork Probe

Leak-free decision sims (one subagent per cell; given ONLY the question + `db_description.txt`; never
ground_truth/validate/withhint/transcripts). A sim estimates DECISION TENDENCY, not real-run outcome —
used here to catch design flaws, not to skip smoke. Two iterations:

| Cell | v1 (verbose) sim | **v2 (lean) sim** | conf |
|---|---|---|---|
| googlelocal-q3 | HELPS | **FLIP-PRESERVED** (abstention was reachability-driven; v2 failure-gated fallback still fires) | High |
| crmarenapro-q7 | ⚠️ None-suppression | **INERT-SAFE** (None carve-out negates the bias) | High |
| PANCANCER-q2 | ⚠️ perturbs (reconcile) | **INERT-SAFE** (failure-gated; connection works → rule never fires) | High |
| crmarenapro-q12 | INERT | **INERT** (pure computation; rule has no trigger) | High |
| agnews-q4 | INSUFFICIENT | **INSUFFICIENT** (coin-flip; rule can't control) | Low — drop as target |

Fork tested: abstain-vs-persist (googlelocal-q3) and the two v1 harm mechanisms (None-suppression,
source-reconciliation). v2 cleared both at High confidence while preserving the flip. Proxy caveat: sims
are tendency, and agnews-q4 is acknowledged uncontrollable.

## Propose-gate smoke set

Surviving cells confirmed via `rk run --explain` on the frozen smoke spec = **Tasks: 5**, `trials: 3`
(captain-approved multi-trial) → **15 trials**, concurrency.trials:4. `@baseline` rewards read from
`runs/dab0007-gpt55-baseline-xhigh/9b0a658e2274cb22/per_trial_outcomes.json`.

```
┌──────────────────────┬──────────┬─────────────────────┬──────────────────────────────────────────────────┐
│        Task          │ Baseline │ Should pass in smoke?│             Role / why we picked it                │
├──────────────────────┼──────────┼─────────────────────┼──────────────────────────────────────────────────┤
│ googlelocal-q3       │ ❌ FAIL  │ 🎯 want it to flip  │ Target — the real abstention flip; must survive v2.│
│ PANCANCER_ATLAS-q2   │ ✅ PASS  │ ✅ must stay PASS   │ Recovery — v1 regressed it (source-reconcile); v2  │
│                      │          │                     │ failure-gated clause should leave it untouched.    │
│ crmarenapro-q7       │ ✅ PASS  │ ✅ must stay PASS   │ Recovery — v1 regressed it (None-suppression); v2  │
│                      │          │                     │ None carve-out should leave it untouched.          │
│ crmarenapro-q12      │ ✅ PASS  │ ✅ must stay PASS   │ Recovery — v1 regressed it; pure-computation cell, │
│                      │          │                     │ v2 rule has no trigger.                            │
│ agnews-q4            │ ❌ FAIL  │ measure-only        │ Coin-flip — rule provably can't control; reported, │
│                      │          │                     │ NOT counted as a target.                           │
└──────────────────────┴──────────┴─────────────────────┴──────────────────────────────────────────────────┘
```

**Net hoped for:** googlelocal-q3 flips FAIL→PASS and HOLDS across all 3 draws; the 3 recovery cells
stay PASS across all 3 draws (artifact-read: None returned where correct, connection kept when working);
agnews-q4 measured but not counted. Board-safety (other-cell regressions) is DEFERRED to the full run
per AC-5 — do NOT promote on the smoke alone. ETA: 5 cells × 3 draws = 15 trials, detached (nohup).

## Acceptance criteria

**AC-1 — Exactly the two README edits; full spec differs from `specs/dab0007-gpt55-baseline-xhigh.yaml`
only in `experiment:` + `solver_workflow:`.** Verified by `diff`.

**AC-2 — Every recorded score paired with a clean strict audit.**

**AC-3 — MULTI-TRIAL consistency (trials:3, captain-approved exception to trials:1).** Across the 3 smoke
draws: googlelocal-q3 holds its flip; the 3 recovery cells (PANCANCER-q2, crmarenapro-q7, crmarenapro-q12)
do NOT regress (PASS in the draws), judged with the committed-artifact read (None returned where correct;
connection kept when working). agnews-q4 measured but not counted.

**AC-4 — Leak-guard intact** (no external-data relaxation; only premature abstention + a correct-None
carve-out).

**AC-5 — Board-safety deferred to the full run** (generative lever; the full run's 54 cells are the
native regression panel — do not promote on the smoke alone).

## Gatekeeper review

**Recommendation: APPROVE** — exactly the two intended README edits, leak-guard byte-identical, both specs scoped/frozen correctly; generative lever carries its in-target recovery sentinels per the captain-approved AC-5 board-safety-deferred deviation.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-17T13:42:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs `spacedock-readme-baseline` = exactly two hunks: (a) `## Database Access` +1 failure-gated sentence (L68); (b) `## Rules` abstention line rewritten to anti-abstention + None carve-out (L74). One coherent anti-abstention idea across the Rules + Database-Access prose; no analyze/verify methodology or leak-guard prose touched. |
| G2 leak-guard intact | PASS | `grep` over added lines: no `curl`/`wget`/`git clone`/`git ls-remote`/`withhint`/`expected_`/`answer_key`/`gold`. `ground_truth` appears ONLY in the pre-existing leak-guard line (L73), not the added text. The "Use only the workspace data" / forbidden-sources block (L79-84) is unchanged. No oracle file read, no withhint paraphrase, no external fetch introduced. |
| G3 spec two fields | PASS | Per captain G3 anchor override, diffed vs full-spec parent `dab0007-gpt55-baseline-xhigh.yaml`: only `experiment:` (→dab0010-anti-abstention-lean) and `solver.solver_workflow:` (→./solver_workflows/dab0010-anti-abstention-lean) differ. `agent.kind: spacedock_solver` + `runtime: codex` preserved; full-spec `trials: 1` (unchanged). |
| G4 smoke tasks+exclude | PASS | Smoke diff vs full = only `benchmark.tasks` (googlelocal/PANCANCER_ATLAS/crmarenapro/agnews — dataset names, not query ids) + `benchmark.exclude_tasks` (18 `{ds}-q{n}` ids) **plus `trials: 1→3`** (captain-approved multi-trial-consistency exception, AC-3). Surviving per-query set = googlelocal-q3 (target flip), PANCANCER_ATLAS-q2 + crmarenapro-q7 + crmarenapro-q12 (recovery), agnews-q4 (measure-only); the lone named target (googlelocal-q3) is present. |
| G5 both frozen | PASS | `.frozen.yaml` (1797B) and `.smoke.frozen.yaml` (2028B) both present; both carry `kind: spacedock_solver` + `runtime: codex` (L4-5). Frozen smoke retains `trials: 3`. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim verbatim in intent: anti-abstention WITH a None/0/empty/'no match' carve-out ("a real answer, not an abstention … never means preferring a positive over a correct negative") + a failure-gated persistence sentence ("if and only if a connection attempt fails … if your connection works, keep it"). Generative behavior guidance, not self-anchored verification; no scope creep, no dead-family "re-run/verify your own result" phrasing. |
| G7 actionability/inert-risk | WARN | Both clauses are behavioral-disposition prose ("commit your best computed answer", "return it", "keep it") rather than a mechanical SQL/cast/column edit or worked-example skeleton — inert-risk class "abstract-behavioral." It worked at gpt-5.5/xhigh in dab0009 (flipped googlelocal-q3 3/3), so the disposition does land here; v2's lean form is the de-risked version. Advisory only — does not block. |
| G8 regression-canary coverage | PASS | Generative (fires on every query, not gated to targets). Smoke keeps no cross-dataset `@baseline` canary panel — a known captain-approved AC-5 deviation: board-safety is DEFERRED to the full run's 54-cell native regression panel; this focused smoke is a flip+recovery consistency check. The three recovery cells (PANCANCER_ATLAS-q2, crmarenapro-q7, crmarenapro-q12) are themselves `@baseline-xhigh` passers the v1 lever regressed, so they act as **perturbable in-target sentinels** (≥2 perturbable passers on the construct the lever most likely perturbs). Scored PASS on that perturbable-sentinel basis; see captain note for the deferred broad-panel caveat. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — single solver session, no "run N candidates and select." |
| G10 self-correcting false-positive | N/A | Not a verify-and-act-on-disagreement lever. The None carve-out is answer-disposition guidance and the failure-gated clause triggers ONLY on a connection failure (not on a number mismatch); neither re-derives a result and replaces it on disagreement. No `reward_per_query` false-green surface. |

**For the captain:** Clean APPROVE — the diff is exactly the two intended hunks and integrity rules (G2/G3/G6) are all PASS. Two advisory notes: (1) **G7 WARN** — the lever is abstract-behavioral prose, not a mechanical edit; inert-risk is real in general but dab0009 already demonstrated the disposition fires at xhigh, and v2 is the lean de-risk, so confidence is reasonable. (2) **G8 deviation** — this generative lever ships NO broad cross-dataset canary panel; board-safety is deliberately deferred to the full run per AC-5, with the 3 recovery cells serving as perturbable in-target sentinels only. Do NOT promote on the smoke alone — the full run's 54 cells are the regression gate. The Pre-smoke Decision-Fork Probe is clean as a proxy: sims got only question + `db_description.txt` (no ground_truth/validate/withhint/transcripts), used a v1-verbose-vs-v2-lean control fork, and the block explicitly claims DECISION TENDENCY (not a pass-rate) — used to catch design flaws, not to skip smoke. Also note the captain-approved `trials: 3` smoke exception to the standing trials:1 rule (full spec keeps trials:1).

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: README forked (spacedock-readme-baseline -> solver_workflows/dab0010-anti-abstention-lean) with EXACTLY the two v2 edits, nothing else
  `diff` vs parent = exactly 2 hunks: (a) `## Rules` abstention line -> anti-abstention + None/0/empty/'no match' carve-out; (b) `## Database Access` +1 failure-gated sentence. Leak-guard + analyze/verify byte-identical.
- DONE: Full spec specs/dab0010-anti-abstention-lean.yaml differs from dab0007-gpt55-baseline-xhigh.yaml only in experiment + solver_workflow (AC-1)
  `diff` shows only those 2 lines; xhigh/trials:1/concurrency.trials:4/all-12-tasks preserved.
- DONE: Multi-trial smoke spec with tasks+exclude_tasks; surviving cells EXACTLY the 5 targets; trials:3; both frozen; --explain confirms
  `--explain` on frozen smoke = `Tasks: 5` x trials:3 = 15 trials. Survivors: googlelocal-q3, PANCANCER_ATLAS-q2, crmarenapro-q7, crmarenapro-q12, agnews-q4.
- DONE: Gatekeeper subagent run; per-rule table + APPROVE/REVISE/REJECT in ## Gatekeeper review; trials:3 + board-safety-deferred deviations noted; Pre-smoke probe reviewed; 5 baseline rewards resolved for the gate table
  Recommendation: APPROVE (no FAILs; G7 WARN abstract-behavioral inert-risk, G8 PASS-with-AC-5-deviation, G9/G10 N/A). Baseline rewards: googlelocal-q3=0.0, PANCANCER_ATLAS-q2=1.0, crmarenapro-q7=1.0, crmarenapro-q12=1.0, agnews-q4=0.0.

### Summary

Authored dab0010 (anti-abstention LEAN v2), the de-risked refinement of dab0009. Forked the seed
baseline README with exactly two minimal edits — the anti-abstention Rules rewrite WITH a correct-negative
(None/0/empty) carve-out, and one failure-gated `db_config.yaml` fallback sentence — deliberately NOT
re-adding dab0009's verbose ~14-line persistence block that caused the board perturbation. Full spec is
a clean 2-field fork of the xhigh baseline; the focused multi-trial smoke (trials:3, captain-approved)
surfaces exactly the keep-the-flip target (googlelocal-q3) + 3 recovery sentinels + 1 measure-only
coin-flip, with board-safety deferred to the full run per AC-5. Gatekeeper APPROVE recorded. No run
launched — smoke fires only after the captain's propose-gate GO.
