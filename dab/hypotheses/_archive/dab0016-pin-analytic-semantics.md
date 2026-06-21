---
id: dab0016
title: variable-band - pin the analytic semantics (ordering/tiebreak + thresholds/dates/NULLs) to stabilize coin-flip cells, judged multi-trial
status: conclude
kind: hypothesis
source: merge of dab0002 (determinism/tiebreak) + dab0003 (aggregation/filter precision); direction decision _artifacts/direction-decision-2026-06-21.md
score: 0.55
verdict: rejected
archived: 2026-06-21T09:53:17Z
---

## Hypothesis

The benchmark's real opportunity is the **14 variable cells** (3/6–5/6 in `_artifacts/baseline-variance-6draw.md`):
the model *can* solve them but not *reliably*. A common cause of that variance is **under-specified analytic
semantics** — the model resolves an ambiguous ordering, tie-break, threshold comparator, date boundary, or
NULL/distinct decision differently run-to-run. Pinning those decisions is a **deliberated-choice** lever,
which dab0015 established is the *tractable* class for gpt-5.5 (it follows representation/analytic rules,
unlike the dead decoration reflex). So a README rule that pins the analytic semantics should convert
coin-flip cells into reliable passes — i.e. raise the **pass-rate** of variable cells, the direct
"make the score more consistent" goal.

**The README change** (fork `spacedock-readme-baseline` → `dab0016-pin-analytic-semantics`), ONE idea — a
"pin the analytic semantics" rule in the `analyze` stage:

> Before writing the answer, make every ambiguous analytic decision **explicit and deterministic**:
> - **Total order:** every ranking / top-N / argmax gets a full ORDER BY down to the last row — primary
>   metric, then stable secondary keys, then a unique id as the final tiebreak. Never leave a tie unbroken.
> - **Comparators:** state `>=` vs `>` (and `<=`/`<`) exactly as the question's wording implies.
> - **Date windows:** treat endpoints as inclusive unless the question says otherwise; pin the exact bounds.
> - **Counting:** decide distinct-entity vs row count per the question; state which.
> - **NULL / missing rows:** state the policy (exclude vs treat-as-zero) before aggregating.
>
> (Foreign-domain worked example to be added at propose; no target schema leaked.)

This is generative (fires on every analytic query) → smoke needs a G8 regression panel.

## Pre-smoke Decision-Fork Probe (REQUIRED FIRST — gate before propose/full)

Because this targets *variance*, confirm the variance is under-specification, not a hard-analytic near-tie,
BEFORE spending a run:
- Read the committed artifacts + transcripts of ≥2 variable cells across draws (start: `stockmarket-q4`
  4/6, `crmarenapro-q3` 3/6). For each, classify: does the cell flip because the model picks a different
  ORDER/tiebreak/threshold/NULL handling run-to-run (**under-specified → this lever can fix**), or because
  it lands on a different analytic branch / genuine near-tie (**hard-analytic → this lever cannot fix**)?
- Proceed to propose ONLY for the cells confirmed under-specified; drop hard-analytic cells from the target
  set (they belong to a different, probably oracle-blocked, family).

## Acceptance criteria (falsifiable) — MULTI-TRIAL

Consistency is a pass-RATE property; single-trial cannot measure it. Judge **multi-trial (3–6 draws)** on
target + canary cells vs the 6-draw band:
- **GO** iff a confirmed-under-specified target's pass-rate rises materially above its band (e.g. 3/6 or
  4/6 → ≥5–6/6 across the draws) AND no rock-stable (6/6) canary's rate drops — judged per-cell, never on
  a single draw, with the committed artifact showing the pinned semantics were actually applied.
- **NO-GO / falsified** if pinned-target rates don't rise above band (variance was hard-analytic, not
  under-specification → lever inert) OR any 6/6 canary destabilizes (the determinism rule mis-fires).
- **Boundary value:** either way we learn whether the variable band is README-stabilizable — the central
  open question for the consistency goal.

## Target queries

Primary (pending probe confirmation): `stockmarket-q4` (4/6), `crmarenapro-q3` (3/6); consider other
under-specified variable cells (`crmarenapro-q10/q13`, `DEPS_DEV_V1-q2`, `GITHUB_REPOS-q3`,
`PANCANCER_ATLAS-q3`) only if the probe shows under-specification. Hold canaries: ≥2 perturbable
ranking/aggregation passers + ≥1 cross-dataset 6/6 sentinel (generative-lever G8 panel). Judge all
per-cell vs `_artifacts/baseline-variance-6draw.md`, multi-trial.

## Stage Report

**Stage:** propose (probe-gated). **Date:** 2026-06-21. **Ensign:** DAB autoresearch worker.
**Decision:** probe CLEARED the fork → README authored → gatekeeper APPROVE → **recommend ADVANCE TO SMOKE** (narrowed to one confirmed target).

### PHASE 1 — Decision-Fork Probe (per-cell, cited)

Probe read the committed answers + verifier reasons across the 6 no-lever draws (dab0007 run-dir
`runs/dab0007-gpt55-baseline-xhigh/9b0a658e2274cb22/` + 5 CAIS
`~/CAIS-paper-expriments/spacedock-codex-5.5-xhigh-hint/run-00{1..5}/`). The actual SQL is not preserved
(only `queryN/query.json` survives in the archived workspaces; codex SQL lives in the reasoning trace,
mostly uncaptured) — so classification is from the **answer-set divergence**, which is decisive.

**`stockmarket-q4` (4/6) → UNDER-SPECIFIED (lever CAN fix). TARGET.**
Question: *"the names ... of the top 5 non-ETF stocks listed on NYSE that had more up days than down days
in 2017"* — a top-5 ranking with **no stated ranking metric**. The pass and fail draws return genuinely
DIFFERENT sets of 5 companies, not reorderings of one set:
- PASS (CAIS run-001): MFA Financial, Argo Group, HDFC Bank, Albany International, DTE Energy.
- FAIL (CAIS run-004): HDFC Bank, Albany International, Getty Realty, Mettler-Toledo, Pfizer
  — verifier: *"Name not found within 5 edits: 'Argo Group International Holdings, Ltd'"*.
- FAIL (dab0007): verifier *"Name not found within 5 edits: 'MFA Financial, Inc'"* — i.e. MFA (a top-5
  member in the passing draw) was absent from that draw's committed set.
Many stocks satisfy "more up than down days," so WHICH 5 are "top" is decided entirely by the unstated
ranking key + tiebreak → the model picks a different `ORDER BY` each draw → a different top-5. This is
exactly the lever's **total-order** target. Result tally: dab0007 FAIL + CAIS 001/002/003/005 PASS,
004 FAIL = 4/6, matches the band.

**`crmarenapro-q3` (3/6) → HARD-ANALYTIC (lever CANNOT fix). DROPPED.**
Question: *"Is the stage name accurately representing the tasks for this opportunity? If not, what should
the appropriate stage name be? Return only the correct stage label among (...)"* — a **semantic judgment**
of which stage best fits the opportunity's task text. PASS draws answer `Negotiation` (run-001 built a
keyword CASE: *`like '%contract%' then 'Negotiation'`*, reasoned *"Correct stage: Negotiation"*); FAIL
draws answer `Discovery` (run-002/004/005: *"Found stages ['Discovery'], but expected 'Negotiation'"*).
The divergence is in how the model interprets/classifies the underlying tasks into a stage label — there
is no ORDER/comparator/date/NULL/distinct decision to pin. None of the lever's five rules touch this.
Tally: dab0007 PASS (reward 1.0) + CAIS 001/003 PASS, 002/004/005 FAIL = 3/6, matches the band.

**Secondary candidates probed (all DROPPED from target — none cleanly under-specified):**
- `crmarenapro-q10` (4/6): fail draws answer **"UNABLE TO DETERMINE"** (run-003/004) — the abstention
  reflex, a DEAD family (dab0009/0010), not an ordering ambiguity. DROP.
- `crmarenapro-q13` (4/6): one fail (run-003) returns a different agent Id (`...NEa3` vs `...NIXC`) for a
  single argmax with a date-window eligibility rule; no near-tie visible in trace → under-spec only weakly
  suggested (possible date-window divergence). Kept as **watch-only secondary** in the panel, NOT a GO gate.
- `DEPS_DEV_V1-q2` (5/6): fail draw (run-001) MISSED `mui-org/material-ui` — the **#1 highest-fork**
  project (30522) — a different filter/branch (the "marked as release" filter dropped the top item), not a
  boundary tiebreak. Leans hard-analytic. DROP (used as inert reference only).
- `GITHUB_REPOS-q3` (5/6, **5/5 in CAIS**): a COUNT with comparator (`< 1000`) + prefix-exclusion filters,
  deterministic and stable in all 5 CAIS draws → perturbable **CANARY**, not a target.
- `PANCANCER_ATLAS-q3` (5/6, 5/5 in CAIS, all ≈305.12): float near-tie/format variance, hard-numeric. DROP.

### PHASE 1 fork decision

≥1 primary target confirmed UNDER-SPECIFIED (`stockmarket-q4`) → **proceed to PHASE 2**, targeting ONLY
`stockmarket-q4`. `crmarenapro-q3` dropped (hard-analytic). No other variable cell was probe-confirmed
under-specified, so the target set is honestly NARROW (one cell). This is the entity's anticipated outcome:
the variable band is mostly NOT determinism-under-specification.

### PHASE 2 — README authored

Fork: `solver_workflows/spacedock-readme-baseline` → `solver_workflows/dab0016-pin-analytic-semantics`
(clean copy, then one edit). ONE idea added to the **`analyze`** stage: a "Pin the analytic semantics"
checklist bullet with the five sub-rules verbatim from `## Hypothesis` (total order / comparators / date
windows / counting / NULLs) plus a **foreign-domain worked example** (a public-library catalog: top-3
authors by checkouts in 2023 — full `ORDER BY checkout_count DESC, total_pages DESC, author_id ASC LIMIT 3`
+ inclusive 2023 date window). No target-cell schema used. `### verify` untouched. No decoration/output-shape
rule added (dead family). **No claim about the DAB matcher is made** (integrity-safe). Diff vs seed = one
added analyze bullet (36 lines), nothing else. Specs forked (anchor → full → smoke); both frozen via
`rk freeze --allow-missing`. `--explain` confirms **7** surviving smoke tasks.

### Smoke table (G8 regression panel)

```
┌──────────────────────┬──────────────┬─────────────┬──────────────────────────────────────────────┐
│ Task                 │ Baseline band│ Should-pass │ Role                                           │
├──────────────────────┼──────────────┼─────────────┼──────────────────────────────────────────────┤
│ stockmarket-q4    🎯 │ 4/6          │ ≥5–6/6      │ TARGET — confirmed under-specified top-5       │
│ stockmarket-q5    ✅ │ 6/6          │ 6/6 hold    │ perturbable canary (top-5 ranking, SAME ds)    │
│ stockindex-q3     ✅ │ 6/6          │ 6/6 hold    │ perturbable canary (top-5 ranking, sibling ds) │
│ stockindex-q2     ✅ │ 6/6          │ 6/6 hold    │ perturbable canary (up/down-days comparator)   │
│ GITHUB_REPOS-q3   ✅ │ 5/6 (5/5 CAIS)│ hold        │ perturbable canary (comparator+count, NON-tgt) │
│ music_brainz_20k-q3✅│ 6/6          │ 6/6 hold    │ cross-dataset 6/6 sentinel (ranking, perfect)  │
│ crmarenapro-q13   ❌ │ 4/6          │ watch-only  │ secondary (date-window argmax; thin under-spec) │
└──────────────────────┴──────────────┴─────────────┴──────────────────────────────────────────────┘
Net target: +1 cell stabilized (4/6 → 5–6/6) if GO.  Draws planned: 3 (multi-trial), judge per-cell vs band.
ETA: ~7 cells × 3 draws.
```

Acceptance is **MULTI-TRIAL** (entity §Acceptance): run the smoke spec **3 draws** (separate run-dirs;
`trials: 1` per G3, multi-draw achieved by repeated invocation, mirroring how the 6-draw baseline was
built). GO iff `stockmarket-q4` rises materially above its 4/6 band (≥5–6/6 across draws) with the
committed artifact showing a full deterministic `ORDER BY`, AND no 6/6 canary (stockmarket-q5,
stockindex-q2/q3, music_brainz_20k-q3) drops below its band. Single-draw deltas are NOT signal.

### PHASE 3 — Gatekeeper verdict

**APPROVE** (self-review applied per `_gatekeeper/propose-review-guideline.md`). No FAILs. Full table in
the `## Gatekeeper review` block below.

### Checklist

- [x] DONE — PHASE 1 probe: both primary cells classified with cited artifact lines (stockmarket-q4
  UNDER-SPECIFIED, crmarenapro-q3 HARD-ANALYTIC); 5 secondary candidates probed.
- [x] DONE — fork decision: proceed, target narrowed to stockmarket-q4 only.
- [x] DONE — README forked + one analyze rule + foreign-domain (library) worked example; no matcher claim.
- [x] DONE — full + smoke specs authored; G3 (two-field) and G4 (tasks+exclude only) diffs clean.
- [x] DONE — both specs frozen (`rk freeze --allow-missing`); kind/runtime/trials=1 preserved.
- [x] DONE — `rk run --explain` confirms 7 surviving smoke tasks incl. target.
- [x] DONE — gatekeeper self-review: APPROVE.
- [ ] SKIPPED (next stage) — `rk run` smoke/full; promotion; baseline seed-edit; archive.

## Gatekeeper review

**Recommendation: APPROVE** — one analyze-stage idea matching the claim, leak-guard intact, foreign-domain
example, generative lever carries a perturbable G8 panel; no integrity FAILs.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-21T04:10Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff` vs seed = one added bullet, all under `### analyze`; one idea (pin analytic semantics). |
| G2 leak-guard intact | PASS | leak-guard paragraphs byte-identical to seed; added lines contain no `ground_truth`/`db_description_withhint`/`curl`/`wget`/`git clone`/`hf://` (the token hits are in unchanged baseline prose); library example is foreign-domain. |
| G3 spec two fields | PASS | anchor→full diff = only `experiment:` + `solver_workflow:`; `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks+exclude | PASS | full→smoke diff = only reduced `tasks` + added `exclude_tasks`; `--explain` → 7 tasks incl. target `stockmarket-q4`. |
| G5 both frozen | PASS | `dab0016-…frozen.yaml` + `…smoke.frozen.yaml` exist; both carry `kind: spacedock_solver`/`runtime: codex` (same content_hash sha256:95b20f0b…). |
| G6 resolver fidelity | PASS | inserted text = the entity's five pins verbatim, in `analyze`, generative (not self-anchored); no scope creep. |
| G7 actionability/inert-risk | PASS | structural ("full ORDER BY") BUT carries a concrete copyable worked-example skeleton (library `ORDER BY … LIMIT 3` + date window) → mechanical anchor present. Residual inert-risk noted: "talks-but-doesn't-do" at gpt-5.5 is the live failure mode for structural rules — smoke must verify the committed SQL actually changed. |
| G8 regression-canary coverage | PASS | generative; non-target `@baseline` passers kept (GITHUB_REPOS-q3, music_brainz_20k-q3); ≥2 perturbable top-N canaries on the target's construct (stockmarket-q5, stockindex-q3) + comparator canary (stockindex-q2). |
| G9 selector independence | N/A | not a multi-candidate/selector protocol. |
| G10 self-correcting false-positive | N/A | not a check/reconcile/validate-and-fix lever; `verify` stage untouched. |

**For the captain:** the lever is honestly narrow — exactly ONE probe-confirmed target (`stockmarket-q4`);
`crmarenapro-q3` and the other variable cells were probed and are hard-analytic / abstention / branch /
near-tie, not determinism-under-specification. The central question ("is the variable band
README-stabilizable?") gets a clean read on this one well-characterized cell. Main risk is G7 inert-risk
(structural rule may be acknowledged-but-not-applied); smoke is multi-trial (3 draws) and must check the
committed `ORDER BY` actually became total before crediting a GO.

## Stage Report — smoke (3-draw multi-trial)

**Stage:** smoke. **Date:** 2026-06-21. **Run:** `runs/dab0016-pin-analytic-semantics/3ce08c53d5abe457.draw{1,2,3}`
(handle `runs/.rk-handles/dab0016-smoke-3draw-20260621-075111`). **Verdict: NO-GO / FALSIFIED.**
All 3 draws: strict audit clean, 0 errored, 7/7 completed → genuine answer differences, not infra.

| cell | band | d1 d2 d3 | smoke | role |
|------|------|----------|-------|------|
| stockmarket-q4 | 4/6 | F F P | **1/3** | 🎯 TARGET — did NOT rise (below band) |
| stockmarket-q5 | 6/6 | P P P | 3/3 | canary held ✅ |
| stockindex-q2 | 6/6 | P P P | 3/3 | canary held ✅ |
| stockindex-q3 | 6/6 | F P F | **1/3** | canary DESTABILIZED ❌ |
| GITHUB_REPOS-q3 | 5/6 | P F F | **1/3** | canary DESTABILIZED ❌ |
| music_brainz_20k-q3 | 6/6 | P P P | 3/3 | sentinel held ✅ |
| crmarenapro-q13 | 4/6 | F F F | 0/3 | watch-only |

**Both acceptance arms fail:** (1) target 1/3 is BELOW its 4/6 band, not ≥5–6/6; (2) a rock-stable 6/6
canary (stockindex-q3) destabilized — the explicit falsification condition ("determinism rule mis-fires").

**Mechanism (artifact-confirmed, from the codex rollouts):**
- **stockmarket-q4 — rule INERT on the actual ambiguity.** The rule fired (full `ORDER BY … , symbol ASC`
  every draw) but the variance is in the unstated *primary ranking metric*, which the rule explicitly
  DEFERS to the model ("the primary metric you infer"). Fails ranked by `up_count DESC` (→ HDFC/Albany/
  Getty/Mettler/Pfizer); the pass ranked by up-minus-down *surplus* (→ MFA/Argo/HDFC/Albany/DTE). Pinning
  tiebreaks cannot fix a cell whose flip is *which metric*, not *how to break ties*. The probe correctly
  saw "under-specified ordering" but mis-identified the locus (metric choice, not tiebreak).
- **stockindex-q3 — generative rule plausibly HARMFUL.** Pass (d2) INCLUDED NSEI; fail (d3) EXCLUDED NSEI
  + J203.JO "because their data starts after 2000" — a date-window/eligibility flip. The rule's
  "pin the exact date bounds" emphasis plausibly nudged a stricter since-2000 eligibility filter that
  drops a valid index, breaking a 6/6 cell. (3 draws is thin to prove harm, but the direction is wrong.)

**Boundary learned (the central question answered):** the variable band is **NOT** README-stabilizable by a
generative "pin the analytic semantics" rule. Real under-specification in ranking cells is *metric choice*
and *eligibility-filter interpretation* — both oracle-blind decisions the rule can't pin — and a blanket
determinism rule ADDS variance to previously-stable ranking/eligibility canaries rather than removing it.
This closes the determinism/precision lever family (dab0002+dab0003 merged here). Mirrors the oracle-blind
wall: you cannot pin the *correct* metric/eligibility without the oracle.

### Checklist
- [x] DONE — 3-draw smoke launched detached, all draws rc=0, strict audit clean, 0 errored.
- [x] DONE — per-cell matrix vs 6-draw band; target + 2 canaries scored below band.
- [x] DONE — mechanism characterized by rollout artifacts (metric-choice inertness; eligibility mis-fire).
- [ ] N/A — full run (NO-GO, do not advance); promote/seed-edit (none).
