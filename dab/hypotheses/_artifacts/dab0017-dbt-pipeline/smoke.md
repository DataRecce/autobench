# dab0017 — Gate 2 smoke: NO-GO

**Variant smoke:** `runs/dab0017-dbt-pipeline/01e0442e6da23d51` (dbt method, host-fixed,
concurrency 2). **Anchor:** `@codex-batch-baseline` (`…/bf113446fdd94373`).
Smoke set: crmarenapro, GITHUB_REPOS (targets) + bookreview, music_brainz_20k, stockindex,
stockmarket (canary datasets).

## Per-query table (variant vs anchor)

| dataset | anchor | variant | Δ |
| --- | --- | --- | --- |
| crmarenapro | 9/13 | 8/13 | **−1** (flip q3 ↑; regress q12,q13 ↓) |
| GITHUB_REPOS | 2/4 | 2/4 | 0 (q1,q2 targets NOT flipped) |
| bookreview | 3/3 | 3/3 | 0 ✓ |
| music_brainz_20k | 3/3 | 3/3 | 0 ✓ |
| stockindex | 3/3 | 3/3 | 0 ✓ |
| stockmarket | 5/5 | 4/5 | **−1** (regress q3) |

### Target flips (anchor fail → variant pass)
- **crmarenapro q3** (0→1) — via the generic pipeline (no per-question model). The only flip.

### Canary regressions (anchor pass → variant fail) — the blocker
- **crmarenapro q12** (1→0): variant ranked agent `…NJgAIAW`, expected `…NDEBIA4`. q12 is a
  **6/6-stable** passer in baseline-variance → a real dbt-method ranking difference, not noise.
- **crmarenapro q13** (1→0): variant `…NEa3IAG` vs expected `…NIXCIA4` (different ranking winner).
- **stockmarket q3** (1→0): variant produced a different answer shape ("No number found near
  Apex Global Brands Inc"); anchor matched names+numbers.

## Verdict: NO-GO

Gate-2 GO requires a target flip AND **zero** canary regressions. Result: **1 flip, 3
regressions (net −1)** → **NO-GO**. The generic-mart discipline held (no per-question models —
`mart_q` hits are README-echo; 17 generic marts, 133 ATTACH, no hardcoded answers). The
failure mode is the design's **PRIMARY risk**: mandatory dbt's generic-mart indirection changes
ranking/aggregation winners and regresses **stable** direct-SQL passers, while flipping fewer
targets than it breaks. Do NOT proceed to the full run.

## Gate-2 antagonist (CONFIRMED NO-GO) — but regressions are NOT dbt overhead

Independent artifact reconstruction. NO-GO is objectively correct (zero-canary-regression bar
violated). But the *character* of all 3 regressions is dbt-orthogonal:

- **crmarenapro q12** — interpretation divergence, NOT mart-grain overhead. "April 2023" is
  ambiguous (opp *created* vs *company-signed* date). The variant's marts HELD the correct data
  and its own signed-scope query produced the correct `…NDEBIA4`; the analyze stage simply chose
  the created-date scope. Groups are n=1 → draw-fragile.
- **crmarenapro q13** — interpretation divergence (order-owner vs opportunity-owner attribution).
  Same top order/number; variant credited the opportunity owner, anchor the order owner. Not a
  grain artifact.
- **stockmarket q3** — the variant's NUMBERS WERE CORRECT and identical to anchor; it failed only
  because it injected a company description between name and number, breaking the verifier's
  "number near name" proximity check. A **false-RED**, the known output-decoration reflex.

Flip **crmarenapro q3** is REAL + generic (mart_opportunities ⨝ mart_activity_touchpoints
surfaced negotiation-from-transcript evidence the anchor missed). Generic-mart discipline held
(agent's own verify grep: no per-question models, no answer literals). No false-greens.

## Cross-learning (memory-informed) — the fix paths are DEAD families

The antagonist (lacking the DAB memory) suggested iterate-README on date-anchor/owner
disambiguation. But:
- date/owner/comparator **analytic-semantics pinning** is the **dab0016 dead family**
  ("pin the analytic semantics" — INERT on the real ambiguity AND destabilizes stable ranking
  canaries). q12/q13 are exactly this.
- stockmarket q3 decoration is the **dab0012/dab0015 dead family** (README cannot suppress
  output-shape over-elaboration).
- temperature=0 → these are near-deterministic interpretation choices, so a re-run would
  reproduce them; multi-trial is unlikely to rescue q12/q13.

**Verdict: NO-GO, validated-not-promoted.** The dbt method is a *validated capability* (reaches
all backends, holds generic-mart discipline, produces a genuine generic-model flip), but as a
**mandatory single-lever** change it nets −1 on this smoke, and the regressions are README-inert
(dead families), not dbt-fixable. Do NOT proceed to the full run. Mandatory-dbt is **not
falsified** (regressions are interpretation/decoration, not dbt overhead) — but it does not clear
the non-regression bar and the gap is not README-recoverable.
