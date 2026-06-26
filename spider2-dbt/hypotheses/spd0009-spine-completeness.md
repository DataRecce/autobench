---
id: spd0009
title: Axis-2 G1 — SPINE_COMPLETENESS (drive daily/rollup/balance-sheet/enhanced targets from the spine/dimension, left-join facts, carry balances forward, keep NULL)
status: smoke
kind: hypothesis
source: "resolution-survey ranked-backlog #4; forks CHAMPION spd0008 (24/60); Axis-2 G1 spine is the one knob; 2-step smoke (small gate-isolation -> large at-scale)" #4 — the BINDING-CONSTRAINT experiment; stacks on the spd0008 champion
started: 2026-06-25
completed:
verdict:
score: 0.7
worktree:
---

## Hypothesis

The largest under-emit cluster (12 tasks): the solver drove the row grain from fact ACTIVITY
instead of from a calendar-spine / full dimension, so no-activity periods/keys are dropped.
This is the **literal inverse** of the default README grain rule ("drive from fact activity;
do not pad zero-activity rows") that the **19 current passers depend on** — so this is the
highest-risk, highest-fanout lever and the program's binding constraint. The whole hypothesis
is whether a TIGHT precondition gate isolates the spine rule to the targets WITHOUT regressing
the per-key-aggregate passers.

**The single README change:** add **Axis-2 rule G1**, fired ONLY when an oracle-free
precondition holds:
- (a) target name matches `/_daily_|_rollup|_balance_sheet|_snapshot|_overview/` AND a
  date-spine model (`int_*__calendar_spine` / `int_*date_spine`) ships in `models/`; OR
- (b) the instruction carries completeness verbs ("each / every / for all / map X to Y /
  balance … on a monthly basis") over a NAMED reference/dimension source whose rowcount equals
  the target's expected grain; OR
- (c) target matches the Fivetran `*_enhanced` / `*_metrics` / `*__<entity>` dimension
  convention AND a same-named source dimension table exists.

When fired: DRIVE FROM the spine/dimension (left-join facts), carry cumulative balances forward
across zero-activity periods (`SUM() OVER (PARTITION BY entity ORDER BY date_month)`), add
package-standard synthetic rows (e.g. Retained Earnings = −cumulative P&L), leave metric columns
NULL on no-activity rows (do NOT coalesce-to-0 unless the spec says zero-fill),
`ROUND(money, 2)`. When NOT fired, the default fact-driven rule stays as-is — **protecting the
19 passers; the gate is the isolation.**

**Target tasks (REACHABLE_VERIFIED, 12):** salesforce001, recharge002, xero001, xero_new001,
xero_new002, jira001, marketo001, intercom001, provider001, hive001, flicks001, playbook002.

## Pre-smoke Decision-Fork Probe

Offline-verified (survey wf_32b5a457-a96): each target reconstructed from the spine/dimension
side passed `duckdb_match.py` — e.g. salesforce001 daily-spine grain, xero balance-sheet 60-month
carry-forward, jira `project_enhanced` full-dimension. Reachability is NOT in question; this
smoke is **purely a steerability + canary-isolation test**: does the gated spine rule fire on
`_daily_`/`_balance_sheet`/`_enhanced` targets WITHOUT over-emitting on activity-grained passers?
**A canary regression here is a NO-GO regardless of target flips** — the gate must hold.

## Acceptance criteria

**AC-1** — README-only; spec diff = the two allowed fields.
**AC-2** — scores paired with clean strict audits.
**AC-3** — paired `rk runs diff` vs the spd0008 champion. **Promotion requires net ≥ +1 with
ZERO regression on the per-key-aggregate passers** (smoke carries ≥2 perturbable passer canaries
that MUST stay PASS). Secondary NULL-vs-zero-fill check: the rule must not coalesce-to-0 where
gold keeps NULL (salesforce001/scd001).

## Gatekeeper review

**Recommendation: APPROVE** — purely-additive single G1 block on the resolved champion spd0008 (24/61 @baseline), gate is TIGHT (conjunctive oracle-free FIRE preconditions + an explicit DO-NOT-FIRE exclusion protecting active-grain per-key aggregates; G1 replaces the default grain rule only WHEN fired), no leak, and the perturbable-canary panel directly targets the one risk (gate bleed onto active-grain passers).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-26T00:00:00Z.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

**Fork parent resolved:** `source:` names spd0008; `rk registry resolve run @baseline` → `runs/spider2-dbt-spd0008-full/4ba55fba0138a84d`, `agent.solver_workflow` = spd0008-over-emit-collapse. Agree — parent is the champion (24 passers in `per_trial_outcomes.json`). G1 diffed against it.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | `diff spd0008 spd0009 README` = `150a151,183` — pure append, 0 deletions/edits. The ONE added idea is `### Axis-2 G1 — SPINE COMPLETENESS`. The default "GRAIN + ROW SET — DON'T ZERO-FILL" rule and the PER-KEY METRIC AGGREGATE rule are untouched. |
| G2 leak-guard (hidden gold) | PASS | No-fetch paragraph (README L8/L11–12: `curl`/`wget`/`git clone`/`git ls-remote`) byte-identical to parent. Added G1 lines name NO gold table, NO gold columns, NO rowcounts; "gold" appears only in oracle-free framing ("gold keeps NULL", "gold = one row per dimension member"). No `expected_`/`answer_key`/`ground_truth`, no fetch/clone token in the added block. |
| G3 spec two fields | PASS | Both smoke specs differ from `full-baseline.yaml` only by ABOUTME comments + `experiment:` + `agent.solver_workflow:` + the narrowed `tasks:` list. `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1` all preserved (smoke = the SMOKE spec; no separate full spec yet, 2-step smoke design). |
| G4 smoke narrows tasks only | PASS | Only `benchmark.tasks` narrowed; no `exclude_tasks`. smoke-sm (7): salesforce001/jira001/xero001 targets + marketo001/mrr001/app_reporting001/activity001 canaries. smoke-lg (17): 9 spine targets (salesforce001/xero001/xero_new001/jira001/provider001/hive001/flicks001/playbook002/intercom001) + marketo001/recharge002 must-hold spine passers + mrr001/mrr002/app_reporting001/google_play001/quickbooks003 perturbable + activity001. Every `## Hypothesis` target is covered across the two panels (xero_new002 deferred to full — acceptable for a 2-step smoke). |
| G5 both frozen | PASS | `specs/spd0009-spine.smoke-sm.frozen.yaml` + `…smoke-lg.frozen.yaml` both exist; both carry `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text = the claim verbatim: gated spine rule (3 oracle-free FIRE preconditions a/b/c), DRIVE-FROM-spine + LEFT-join + carry-forward balance + NULL-not-0, with the explicit DO-NOT-FIRE exclusion. Generative/derivational (tells the solver HOW to build the grain), NOT self-anchored "verify your answer matches" — no dead-family phrasing. No scope creep. |
| G7 actionability/inert-risk | WARN | Largely mechanical (named regex tokens, a concrete `sum(...) over (partition by entity order by period)` carry-forward, LEFT-join recipe, `ROUND(money,2)`). Residual inert-risk: precondition (b)'s completeness-phrase match + the "drive from the spine/dimension" core are structural-analytic prose the solver could acknowledge but not re-grain at gpt-5.5/xhigh — the recurring inert pattern. Worth watching in smoke; never FAILs. |
| G8 regression-canary coverage | PASS | GATED (fires only on the 3 oracle-free preconditions), so not flat-generative — but the whole hypothesis is gate-bleed risk, so canary coverage matters. Both panels keep a non-target passing canary AND ≥2 PERTURBABLE active-grain passers (the most-at-risk family): smoke-sm = mrr001 + app_reporting001 (2); smoke-lg = mrr001/mrr002/app_reporting001/google_play001/quickbooks003 (5). All 8 canaries confirmed @baseline reward 1.0 in spd0008 `per_trial_outcomes.json` — none inert/dead. marketo001 + recharge002 are must-hold SPINE passers (catch over-firing on a fired-correctly neighbor). |
| G9 selector independence | N/A | Not a multi-candidate / selector-protocol hypothesis. |
| G10 self-correcting false-positive | N/A | G1 is a build/derivation rule (how to grain the model), not a validate-and-fix / reconcile-and-replace check. No re-derivation against a re-correlated artifact. |

**Gate-tightness verdict (the critical review): TIGHT — APPROVE.** The FIRE preconditions are all oracle-free and (a)/(c) are CONJUNCTIONS (name-token AND a shipped date-spine model / AND a same-named source dimension), not a bare name match. An explicit **DO-NOT-FIRE** clause protects exactly the at-risk family — per-key metric aggregates/rollups scoped to active rows (NPS/review/spend/LTV), rankings/`most_*`/`top_*`, and any target with no spine model and no completeness phrase — plus an in-doubt default-to-not-fire. G1 only REPLACES the default grain rule WHEN a precondition fires; otherwise the default fact-driven rule stands ("the gate IS the isolation"), so the 19/24 active-grain passers are protected by construction. One residual SEAM (WARN-level, not a FAIL): the `_rollup` token appears in BOTH the FIRE regex (a) and the DO-NOT-FIRE exclusion — disambiguated only by the AND-shipped-spine-model conjunction and the active-scoped exclusion. A per-key rollup with no date-spine model correctly fails (a) and is caught by the exclusion, but this is the precise place a bleed could occur, and it is exactly what app_reporting001 (a report/rollup-grain passer, in BOTH panels) is positioned to catch. The gate is tight enough to approve and the canary panel is built to falsify the seam — the intended posture.

**Leak verdict:** CLEAN — no-fetch prose byte-intact vs parent; added block carries no gold table/column/rowcount, signals are name/schema/instruction only.

**Canary-adequacy verdict:** ADEQUATE — both panels carry a non-target passing canary + ≥2 perturbable active-grain passers (2 sm / 5 lg), all confirmed @baseline passers, plus must-hold spine passers (marketo001/recharge002). Coverage directly targets the gate-bleed risk; app_reporting001 specifically guards the `_rollup` seam.

**For the captain:** AUTO-APPROVED to smoke. This is the program's highest-risk lever (inverse of the default grain rule the 19 passers depend on), and the gate review is the whole story: the gate is tight by construction, but the live question is whether gpt-5.5/xhigh HONORS the DO-NOT-FIRE exclusion. Watch the perturbable canaries — ANY of mrr001/mrr002/app_reporting001/google_play001/quickbooks003 dropping in smoke is a gate-bleed NO-GO regardless of target flips (per the hypothesis's own AC-3). Two soft notes: (1) G7 inert-risk on the "drive from the spine" analytic core; (2) recharge002 is both a named target in `## Hypothesis` and an already-PASSING @baseline cell, so in smoke-lg it is correctly a must-hold spine passer, not a flip candidate — don't score it as a target flip.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Smoke result (step 1 — SMALL, gate-isolation)

Run `runs/spider2-dbt-spd0009-smoke-sm/4fc7a44b9c1373f5` (rc=0, audit strict CLEAN). **NO-GO: 0/3
spine targets flipped; mrr001 canary dropped.** Large smoke (step 2) NOT run — small is a NO-GO and
the targets are blocked (running it would be predictable non-flips). But the deep-dive is positive
on the central risk and pinpoints the blockers:

- **GATE IS SAFE (binding-constraint risk ALLAYED).** mrr001's drop = **VARIANCE, not gate bleed**:
  G1 did NOT fire on mrr001 (no precondition matched — name fails the regex, no completeness phrase,
  not `*_enhanced`; mrr is an R1 build-as-is task). The 410→417 over-emit is the known flaky
  date-spine-rebuild flicker. The DO-NOT-FIRE exclusion held — G1 did not bleed onto an active-grain
  passer, which was the whole risk of this lever. marketo001/app_reporting001/activity001 all held.
- **salesforce001 = G1 COMPLIED, blocked by FROZEN-CLOCK spine non-determinism.** G1 drove from
  `int_salesforce__date_spine` correctly (LEFT-join, keep NULL) — textbook. But that spine computes
  `last_date = greatest(max(created_date), current_date)` → a fresh `dbt build` floored it to TODAY
  (2026-06-26) = 752 rows vs gold's 91 (gold ends 2024-09-03 = max activity). G1's mechanism is
  right; the package spine model over-runs to current_date. **FIXABLE** (gold ends at max-fact-date,
  deterministic — unlike the truly-frozen pendo001/atp_tour001): clamp the spine upper bound to the
  max observed fact/source date, not current_date.
- **jira001 = G1 COMPLIED (under-emit FIXED), blocked by a 2nd value-def gap.** G1 drove from the
  full project dimension → 3 rows = gold (the baseline's 2-row under-emit is fixed). Residual 0.0 is
  a column-VALUE divergence in the hand-rolled `epics`/`components` string-aggs vs the canonical
  Fivetran output — a value-def gap G1 doesn't address.

## Failure Review

Primary type: **incomplete-artifact** (G1 mechanism works + gate is safe, but each target has a 2nd
blocker), NOT canary-bleed (mrr001 = variance, gate held).
1. G1 fires correctly on the spine shapes and drives from the spine/dimension; the gate did NOT
   bleed onto active-grain passers (the binding-constraint risk is allayed).
2. Blockers are downstream of G1: (a) FROZEN-CLOCK spine non-determinism — package date-spine models
   floor to `current_date`, over-emitting future-empty periods at 2026 wall-clock (salesforce001;
   likely xero balance-sheet too) — FIXABLE via a max-fact-date spine clamp where gold ends at max
   activity, but genuinely UNREACHABLE where gold's spine is itself at the frozen build-clock
   (pendo001/atp_tour001); (b) residual value-def (jira001 epics/components agg).
3. Next fork: REVISE G1 to add a **spine upper-bound clamp** ("clamp the spine to the max observed
   fact/source date; do not let a package spine's `current_date` floor extend it") — would flip
   salesforce001 and any current_date-floored spine target whose gold ends at max activity. jira001
   needs an additional epics/components value-def clause (separate). Add `mrr`/lag-MRR as a named
   DO-NOT-FIRE negative example to fully de-risk the salience caveat.
4. Step: **escalate** — revise-vs-conclude is the captain's call; the large smoke is deferred until
   the spine-clamp revise (running it now = predictable non-flips on frozen-clock-blocked targets).

## Smoke result (step 2 — LARGE, spine family at scale)

Run `runs/spider2-dbt-spd0009-smoke-lg/cb95763176d0bb66` (rc=0, audit strict CLEAN). **0/9 spine
targets flipped.** Across BOTH steps: **0/12 spine targets flipped.** GATE CONFIRMED SAFE at scale:
mrr001 HELD here (small-smoke drop = variance), marketo001/app_reporting001/google_play001/mrr002/
quickbooks003/activity001 all held; recharge002 dropped = VARIANCE (G1 inert on it — a spine
end-boundary exclusive/inclusive coin-flip, NOT G1-caused over-emit).

**Spine-family characterization (5 of 12 deep-dived) — the family is HETEROGENEOUS:**
- **FROZEN-CLOCK, CLAMPABLE (salesforce001, xero001):** G1 drove from the spine correctly but the
  package spine over-ran to `current_date` (2026) — salesforce 752 vs gold 91; xero 1890/90mo vs
  gold 1170/60mo. Gold ends at MAX ACTIVITY (deterministic), so a max-fact-date spine clamp would
  fix these. (Distinct from the truly-frozen pendo001/atp_tour001 whose gold IS at the build-clock.)
- **VALUE-DEF SECOND GAP (jira001):** G1 fixed the under-emit (3 rows = gold); residual is the
  hand-rolled epics/components string-agg vs canonical Fivetran output.
- **DIFFERENT GRAIN PROBLEM (provider001, hive001):** not date-spine tasks — provider001 needs a
  full-dimension LEFT-join completeness (G1 didn't fire/comply; under-emit 454/82339 vs gold
  874/85196), hive001 needs preserve-the-fan-out (over-collapsed 486 vs gold 558). Spine-clamp
  doesn't touch these.

## Verdict

**NO-GO as written (0/12 spine flips); G1 mechanism + gate VALIDATED but the spine target family is
contaminated.** Key results: (1) G1's gate is SAFE — it does not bleed onto active-grain passers
(the binding-constraint fear is fully allayed across 12 canary-checks); (2) G1's spine-drive
mechanism is correct where it fires (salesforce/xero/jira all drove from the spine); (3) but 0/12
flip because the under-emit grain G1 fixes is rarely the SOLE blocker — the family is dominated by
FROZEN-CLOCK spine over-run (clampable), value-def second gaps, and non-date-spine grain problems
G1 doesn't address. The survey's "12 reachable spine flips" was over-optimistic.

**RECOMMENDATION (captain decision — bounded stop, 2 smokes done):**
- **REVISE (targeted):** add a **max-fact-date SPINE CLAMP** to G1 ("clamp the spine upper bound to
  the max observed fact/source date; do NOT let a package spine's `current_date` floor extend it")
  + add `do-not-re-derive-an-existing-spine's-min/max-boundary` (recharge002 hardening). Re-smoke
  the 2 clampable targets (salesforce001 + xero001) — realistic yield ~+2, then a hold-rate. jira
  needs a separate epics value-def clause; provider/hive are different families (not this lever).
- **OR CONCLUDE validated-not-promoted:** bank G1 (mechanism + gate validated, non-destabilizing)
  and the heterogeneous-spine-family finding; the realistic spine yield (~2-4) may not justify more
  cycles. `@baseline` stays spd0008 24/60.
