---
id: dab0018
title: Classifier-gated dbt — route multi-source-derivation datasets to dbt, all others to the direct method
status: analyze
kind: hypothesis
source: dab0017 REJECTED follow-up. Mandatory-dbt failed (0.565 untuned / 0.603 tuned, both < Opus 0.654) because dbt's derived-intermediate-entity value pays off on only ONE of 12 datasets (crmarenapro, 6 sources, derivation-blocked failures) while its overhead+variance taxes the 2-source datasets. This gates dbt to where it has signal so the non-dbt path stays byte-identical to the anchor.
started: 2026-06-22T04:25:01Z
score: 0.5
completed:
verdict:
---

## Hypothesis

A per-dataset **classifier (oracle-free precondition gate)** at the top of the `model` stage
routes each dataset to one of two methods, in a SINGLE forked README:
- **dbt-pipeline path** (dab0017's tuned method: `stg→int→mart` + tests, ATTACH/pymongo, generic
  marts, answer = query the mart) — used when the gate FIRES;
- **direct path** (the current `spacedock-readme-baseline-hostfix` method verbatim: DuckDB
  ATTACH + pymongo, direct analytical SQL) — used when the gate does NOT fire.

**The gate IS the isolation mechanism** (ade-bench gated-levers-compose pattern, h0049). Because
non-firing datasets run the direct method *verbatim*, they are byte-identical to
`@codex-batch-baseline` → **zero regression by construction** on the 11 two-source datasets. The
only delta vs the anchor is on the firing dataset(s) — collapsing the whole experiment to: "does
gated dbt bank crmarenapro's q2/q3/q7/q8 unlock without the board-wide overhead/variance tax?"

### Gate signal (oracle-free, computable from `db_config.yaml` + `db_description.txt`)

**FIRE dbt iff the dataset has ≥3 source databases.** (crmarenapro = 6; all 11 others = 2 —
verified across every db_config.yaml, dab0017.) Rationale: dbt's value is materializing derived
intermediate entities from MULTI-SOURCE joins; ≥3 sources is the structural marker of
cross-source-derivation work, and it cleanly isolates crmarenapro. **Do NOT** gate on the
dirty-schema trigger — it over-fires on 2-source music_brainz (dab0017 §why-only-crmarenapro).
(Open question for propose: is a pure source-count gate too crmarenapro-specific / overfit? An
alternative is `≥3 sources AND db_description warns of cross-source dirty entity fields`.)

## Acceptance criteria (falsifiable)

- **GO** iff stratified Pass@1 over 12 **beats `@codex-batch-baseline` 0.6966** AND **zero** of the
  36 Opus∩codex-batch canaries regress — judged per-query. Since the gate routes all 2-source
  datasets to the verbatim direct method, any regression there is a GATE-LEAK bug (the branch
  fired wrong), not a method effect.
- **The crmarenapro gain must be STABLE** — dab0017 showed it as variance-fragile (untuned 11/13,
  tuned 9/13). Multi-trial crmarenapro (≥3 draws) to confirm the q2/q3/q7/q8 unlock holds; a
  single-draw +2 is not sufficient (the dab0017 calibration lesson: generative paths add ±0.07
  variance).
- **NO-GO / REJECTED** if (a) the gate mis-fires (a 2-source dataset routed to dbt, or crmarenapro
  routed to direct), or (b) crmarenapro's dbt advantage does not hold across draws, or (c) the
  realized lift is within the ±noise band.

## Honest ceiling (from dab0017 structural analysis)

Only crmarenapro fires the gate, so the **best case is ~+2 cells over the anchor (~+0.03
stratified)** — and dab0017 showed even that is variance-fragile. This hypothesis is worth running
ONLY to (1) cleanly isolate whether the dbt derivation advantage on crmarenapro is real+stable
once the overhead/variance tax on other datasets is removed, and (2) validate the gated-composition
mechanism for DAB. If crmarenapro's unlock proves stable under the gate, it is a small but clean,
attributable, promotable win — the first on DAB. If not, the dbt family is fully closed for DAB.

## Target / canaries

- **Target (gate fires):** crmarenapro — bank q2/q3/q7/q8 (q3 held across both dab0017 dbt runs).
- **Canaries (gate must NOT fire → verbatim direct method):** all 11 two-source datasets; the 36
  Opus∩codex-batch passers must stay byte-identical to the anchor. Any drop = gate-leak bug.
- **Anchor:** `@codex-batch-baseline` (`runs/codex-dab-batch-baseline/bf113446fdd94373`, 0.6966).

## Reusable infra (already built in dab0017 — no rebuild needed)

dab-agent image with dbt + sqlite/postgres scanners baked in (digest `sha256:224133f0…`);
`verify_batch` per-query try/except (razorback PR #19, merged); `spacedock-readme-baseline-hostfix`
(the verbatim direct path); the tuned dab0017 README (the dbt path); `@codex-batch-baseline`
registered. The fork for this entity = a single README that branches on the source-count gate.

## Gatekeeper review

**Recommendation: APPROVE** — gated composition is clean: Method A body byte-identical to the @codex-batch-baseline parent (only `(Method A)` header suffixes differ), the source-count gate cannot fire on the 2-source canaries by construction, specs/frozen/leak-guard all intact.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-22T05:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Parent = `solver_workflows/spacedock-readme-baseline-hostfix` (per `source:` and the @codex-batch-baseline solver_workflow). The single idea is the source-count classifier (N_sources≥3→Method B dbt; else Method A direct) + the dbt cross-source-derivation method. By design this is a GATED COMPOSITION, not a one-stage tweak: the diff ADDS the classifier preamble + the entire Method B block, but Method A's body (Database Access, Rules, 3-step duplicate-source entity-resolution, Answers, model/analyze/verify, External-oracle audit) is byte-intact vs the parent — `diff` shows ONLY the `(Method A)` header-suffix relabels and the `## Entity File` block relocated to the file end. No leak-guard prose touched. Not failed for "more than one section" because the added Method B path is the composed second method, and the Method A path is unchanged. |
| G2 leak-guard intact | PASS | `grep -nE "ground_truth|db_description_withhint|curl|wget|git clone|git ls-remote"` over the README hits ONLY the two intact `Do NOT access validate.py or ground_truth.csv files` leak-guards (one per method). No `db_description_withhint` paste, no external fetch/clone. The "Use only the workspace data" external-source-forbidden paragraph and the verify-stage External-oracle audit are present in BOTH Method A and Method B, byte-equal to the parent's wording. |
| G3 spec two fields | PASS | `diff specs/codex-dab-batch-baseline.yaml specs/dab0018-gated-dbt-classifier.yaml` changes ONLY: ABOUTME comment lines (non-field), `experiment:` (→dab0018-gated-dbt-classifier), `solver_workflow:` (→./solver_workflows/dab0018-gated-dbt-classifier). `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` all preserved. |
| G4 smoke tasks+exclude | PASS | `diff` of full→smoke adds ONLY `benchmark.tasks` (dataset names: crmarenapro, yelp, stockmarket, googlelocal — names not per-query ids, correct for the plugin selector) and `benchmark.exclude_tasks` (the other 8 dataset names). `--explain` surviving set = crmarenapro (target, gate fires) + yelp/stockmarket/googlelocal (2-source canaries, gate must NOT fire). Target dataset crmarenapro (the only ≥3-source set, banks q2/q3/q7/q8) is in the surviving set. Stable-passer sentinels present (yelp 7/7, stockmarket 5/5 at anchor). |
| G5 both frozen | PASS | `specs/dab0018-gated-dbt-classifier.frozen.yaml` and `…smoke.frozen.yaml` both exist; both carry `agent.kind: spacedock_solver` + `runtime: codex`. Smoke frozen retains its `tasks:`/`exclude_tasks:` blocks. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: a classifier at the top of `model` counting `db_clients:` entries, routing N_sources≥3→Method B(dbt), else Method A(direct verbatim). The Method B derivation instruction ("read the cross-source-derived int_ column, never the raw single-source field") is a build/derivation directive within Method B, NOT a self-anchored "check your own answer" reconcile — generative, in-scope, no scope creep. Generalization-hedge note in the README explicitly does NOT change behavior on the current mix (pure source-count is the operative gate). |
| G7 actionability/inert-risk | WARN | Method B is largely abstract-structural prose (build stg→int→mart, "materialize the cross-source derivation in int_*", route per source count) — the dab0017 dead-family lesson is that a generative dbt README adds ±0.07 variance and its smoke is not predictive of the full board. MITIGATED here: Method B carries concrete worked-example skeletons (named int_ models with join recipes: int_opportunity_effective_stage, int_*_policy_breach, int_agent_case_ownership; dbt_project.yml/profiles.yml YAML to copy), and the classifier itself is a mechanical count-and-branch. Inert-risk is on whether the dbt derivation actually FIRES on crmarenapro's q2/q3/q7/q8 — the hypothesis already plans ≥3-draw multi-trial on crmarenapro to test stability. Carry to captain: this is the same generative-dbt path dab0017 rejected; the gate removes the board-wide tax but the crmarenapro lift itself remains variance-fragile. |
| G8 regression-canary coverage | N/A (PASS) | The lever is GATED (precondition N_sources≥3), NOT generative — by construction it cannot fire on the 2-source canaries, which run Method A verbatim → byte-identical to the anchor → zero regression by construction. Marked N/A(PASS)-class per gated-scope. Confirmed the smoke set keeps perturbable 2-source canaries that prove the gate does NOT leak: yelp (7/7 anchor), stockmarket (5/5), googlelocal (3/4) — any drop on these = a gate-leak bug, exactly the failure the panel is designed to catch. |
| G9 selector independence | N/A (PASS) | No multi-candidate / selector protocol — the classifier picks ONE method deterministically from a structural count; it does not run N candidates and select. |
| G10 self-correcting false-positive | N/A (PASS) | Method B's "read the cross-source-derived int_ column, never the raw single-source field" is a derivation/build instruction (generative-within-Method-B): it tells the solver which materialized column to query, not to re-run its own query and fix-on-disagreement. The verify stage is the parent's adversarial-review-without-ground-truth (unchanged shape), not a self-anchored reconcile-and-replace. Not a self-correcting lever → N/A. |

**For the captain:** No FAILs → APPROVE; safe to advance to `smoke`. The single WARN is G7 (advisory): Method B is the same generative dbt path dab0017 REJECTED, so the dbt lift is intrinsically variance-fragile — the gate's value is removing the board-wide tax, isolating the experiment to "does crmarenapro's q2/q3/q7/q8 unlock hold across draws." Honor the hypothesis's own ≥3-draw crmarenapro stability requirement before reading any +2 as a real flip; a single-draw gain is the dab0017 calibration trap. Gate-leak sentinels (yelp/stockmarket/googlelocal byte-identical to anchor) are the key thing to eyeball in the smoke result.

## Smoke-set boxed table (captain gate) — @codex-batch-baseline rewards resolved

Anchor: `@codex-batch-baseline` = `runs/codex-dab-batch-baseline/bf113446fdd94373` (0.6966).
Smoke = 4 datasets / 29 query-cells. crmarenapro FIRES the gate (6 sources → Method B dbt);
yelp / stockmarket / googlelocal are 2-source → gate must NOT fire → Method A direct VERBATIM →
byte-identical to the anchor. Any drop on a 2-source canary = a GATE-LEAK bug (the dbt branch
fired on a 2-source set), NOT a method effect.

```
┌──────────────────────┬──────────┬─────────────────────┬───────────────────────────────────────────────────────┐
│         Task         │ Baseline │ Should pass in smoke?│              Role / why we picked it                  │
├──────────────────────┼──────────┼─────────────────────┼───────────────────────────────────────────────────────┤
│ crmarenapro-q2       │ ❌ FAIL  │ 🎯 want it to flip  │ TARGET — knowledge-article breach; int_quote_policy   │
│                      │          │                     │ _breach cross-source join (quote↔KB) is the only path.│
│ crmarenapro-q3       │ ❌ FAIL  │ 🎯 want it to flip  │ TARGET — stage correction; int_opportunity_effective_ │
│                      │          │                     │ stage (opp↔activity transcripts) → Negotiation, NOT   │
│                      │          │                     │ raw stage_name=Discovery. Held both dab0017 dbt runs.  │
│ crmarenapro-q7       │ ❌ FAIL  │ 🎯 want it to flip  │ TARGET — case policy breach; int_case_policy_breach   │
│                      │          │                     │ (case↔KB) join, not the anchor's None/LLM-judge guess.│
│ crmarenapro-q8       │ ❌ FAIL  │ 🎯 want it to flip  │ TARGET — fewest-transfer agent; int_agent_case_owner  │
│                      │          │                     │ ship derived from owner-assignment history.           │
│ crmarenapro-q1,4,5,6,│ ✅ PASS  │ ✅ must stay PASS   │ SENTINEL (same dataset) — Method-B build must not     │
│   9,10,11,12,13 (9)  │          │                     │ regress crmarenapro's 9 anchor passers.               │
│ yelp-q1..q7 (7/7)    │ ✅ PASS  │ ✅ must stay PASS   │ CANARY (2-source, mongo+pg) — gate must NOT fire;     │
│                      │          │                     │ dab0017 REGRESSED yelp → strongest gate-leak tripwire.│
│ stockmarket-q1..q5   │ ✅ PASS  │ ✅ must stay PASS   │ CANARY (2-source) — dab0017 destabilized its sibling  │
│   (5/5)              │          │                     │ stockindex; clean here → byte-identical-direct proof. │
│ googlelocal-q1,3,4   │ ✅ PASS  │ ✅ must stay PASS   │ CANARY (2-source) — dab0017 REGRESSED googlelocal;    │
│   (3/4; q2 ❌ anchor)│          │                     │ q2 already FAIL at anchor (not a target, stays FAIL). │
└──────────────────────┴──────────┴─────────────────────┴───────────────────────────────────────────────────────┘
```

**Net we're hoping for:** flip ≥1 of crmarenapro's 4 targets (q2/q3/q7/q8) via the cross-source
`int_` derivation — with the committed mart-query answer DIFFERING from the direct-SQL anchor
(the dab0017 no-mechanism-delta trap) — AND lose ZERO of the 21 byte-identical canary/sentinel
cells (9 crmarenapro sentinels + yelp 7 + stockmarket 5 + googlelocal 3). A drop on any
2-source canary is a gate-leak bug, not a method signal. ETA ~45–75 min for 29 query-cells at
concurrency.trials:2 (crmarenapro's dbt build dominates wall time). The run is detached (nohup)
— next stage, NOT launched in propose.

## Stage Report: propose

- DONE: Author ONE forked solver README that branches on a source-count gate (≥3 source DBs → dbt path; else the verbatim direct path); crmarenapro's dbt path REVISED to derive the mart answer through the cross-source int_ join; leak-guard prose byte-intact.
  `solver_workflows/dab0018-gated-dbt-classifier/README.md`: top-of-`model` classifier counts `db_clients:` entries; Method A body byte-identical to `spacedock-readme-baseline-hostfix` (verified: Database Access + 3-step entity-resolution + leak-guard blocks all `in new` True); Method B adds load-bearing `int_opportunity_effective_stage` / `int_*_policy_breach` / `int_agent_case_ownership` cross-source derivations + an analyze/verify rule "read the derived int_ column, never the raw single-source field." Both leak-guard blocks byte-intact (grep count 2).
- DONE: Build full spec + smoke spec forked from the BATCH anchor (differing only in experiment: + solver_workflow:); freeze both; verify the smoke per-query selection via rk run --explain = crmarenapro + ≥2 perturbable two-source canaries.
  `specs/dab0018-gated-dbt-classifier{,.smoke}.yaml` + `.frozen.yaml`; full-spec diff vs anchor = ABOUTME comments + experiment: + solver_workflow: only; `--explain` materialized exactly {crmarenapro, yelp, stockmarket, googlelocal} (Tasks: 4).
- DONE: Run the gatekeeper, record its per-rule PASS/WARN/FAIL table + APPROVE/REVISE/REJECT block; prepare the smoke-set boxed table with @codex-batch-baseline rewards resolved.
  `## Gatekeeper review` appended → APPROVE (no FAILs; sole WARN = G7 generative-dbt variance-fragility, advisory). Smoke-set boxed table above with anchor rewards resolved from `runs/codex-dab-batch-baseline/bf113446fdd94373` reward_per_query.json.

### Summary

dab0018 is a GATED-COMPOSITION lever: one forked README with a source-count classifier
(N_sources≥3 → Method B dbt; else Method A direct). Method A is the `@codex-batch-baseline`
hostfix README verbatim, so the gate IS the isolation mechanism — the 11 two-source datasets run
byte-identical to the anchor (zero regression by construction) and the only delta is on
crmarenapro. The load-bearing revision vs dab0017: Method B forces crmarenapro's q2/q3/q7/q8
answers to be DERIVED through cross-source `int_` joins (effective stage, policy breach,
ownership history), so the committed mart answer differs from the direct #-strip the anchor uses
— curing the dab0017 no-mechanism-delta NO-OP. Gatekeeper APPROVE (sole WARN G7: same generative
dbt path dab0017 found variance-fragile → honor the ≥3-draw crmarenapro stability test before
reading a +2 as a flip). Smoke run NOT launched (next gated stage).

## Smoke run (launched — detached)

- **Handle:** `runs/.rk-handles/dab0018-smoke-20260622-044911/` (pid 1387650)
- **Spec:** `specs/dab0018-gated-dbt-classifier.smoke.frozen.yaml`
- **Selection re-confirmed** (`rk run --explain`, $0 foreground): exactly 4 datasets =
  {crmarenapro, googlelocal, stockmarket, yelp} — crmarenapro fires the gate (6 sources → dbt),
  the other 3 are 2-source (gate must NOT fire → direct path verbatim).
- **ETA** ~45–75 min (29 query-cells, concurrency.trials:2; crmarenapro's dbt build dominates).
- Phase 2 (audit `--policy strict` + score + mechanism-delta deep-dive + canary byte-identity
  check) runs after the FO re-engages on the `done` sentinel (rc=0).

## Smoke result

**Run:** `runs/dab0018-gated-dbt-classifier/bafa25eaad285e74` (rc=0, 30 min, 2026-06-22).
**Audit (`--policy strict`): CLEAN** — clean:4 / coverage_missing:0 / tainted:0. No dataset
errored; no infrastructure taint. `rk score` stratified Pass@1 over the 4 smoke datasets =
**0.7302**.

**Classifier fired CORRECTLY on every dataset — ZERO gate-leak (verified from each codex
transcript's `_artifacts/context.md` classifier line):**
- crmarenapro → `N_sources=6 (core_crm, sales_pipeline, support, products_orders, activities, territory) -> METHOD B (dbt)`
- yelp → `N_sources=2 (businessinfo_database, user_database) -> METHOD A (direct)`
- stockmarket → `N_sources=2 (business, review) -> METHOD A (direct)`
- googlelocal → `N_sources=2 (business, review) -> METHOD A (direct)`

"Zero regression by construction" is **NOT falsified** — the dbt branch never fired on a
2-source dataset. All canary moves are on the DIRECT path (Method A, the same README the anchor
ran), i.e. solver run-to-run variance at temp=0, NOT a method effect of this lever.

### Per-query vs `@codex-batch-baseline` (anchor `runs/codex-dab-batch-baseline/bf113446fdd94373`)

| Dataset | Method ran | Anchor | Smoke | Per-query delta | Adjudication |
|---|---|---|---|---|---|
| crmarenapro | **B (dbt)** | 9/13 | 9/13 | **q3 IN, q7 IN; q12 OUT, q13 OUT** (q2/q8 still FAIL) | net **0** — 2 genuine derivation flips offset by 2 dbt-overhead ranking regressions |
| yelp | A (direct) | 7/7 | 3/7 | q1,q2,q4,q5 OUT | **direct-path variance** (city/state parsed from noisy free-text `description`; gate=Method A, not dbt) |
| stockmarket | A (direct) | 5/5 | 4/5 | q3 OUT | **direct-path variance** (q3 ranking-metric cell, known-variable band — dab0016) |
| googlelocal | A (direct) | 3/4 | 4/4 | q2 IN | **direct-path variance** (q2 flipped IN; anchor had it FAIL) |

### crmarenapro target check — the dbt int_ derivations FIRED (mechanism delta PROVEN)

The dbt pipeline built all prescribed cross-source intermediates (`dbt run`×17, `dbt test`×19
to green; `int_opportunity_effective_stage`, `int_case_policy_breach`, `int_quote_policy_breach`,
`int_agent_case_ownership` all materialized; no `mart_qN`, no answer literals).

- **q3 FAIL→PASS (Negotiation)** — TRUE mechanism delta. `int_opportunity_effective_stage`
  emitted `raw_stage=Discovery`, `effective_stage=Negotiation` for opp `006Wt000007BGGjIAO`,
  **derived from the opportunity↔tasks/events/call-transcripts/quotes/contracts join** (proposal,
  terms, negotiation, contract-prep evidence). analyze read `effective_stage`, NOT raw
  `stage_name`. The anchor's direct SQL read `stage_name=Discovery` → scored 0. Not a #-strip.
- **q7 FAIL→PASS (`ka0Wt000000EoD3IAK`)** — TRUE mechanism delta. The breached article was
  derived by joining case `500Wt00000DDyznIAD` → OrderItem `802Wt000007928FIAQ` → the
  knowledge-base policy ("Scalability Enhancement Package referenced outside the 30–365-day
  purchase window") and evaluating that policy condition against the joined facts. The anchor
  returned "no policy violation / None" → scored 0. Genuine cross-source derivation.
- **q2 FAIL→FAIL, q8 FAIL→FAIL** — the int_ derivation did not crack these two (q2 picked a
  different-but-still-wrong article; q8 the wrong fewest-transfer agent).
- **q12 PASS→FAIL, q13 PASS→FAIL** — dbt-OVERHEAD regressions. Both are agent-attribution
  ranking queries the dbt mart re-grained; the solver ranked a different agent
  (q12: 005Wt000003NJgAIAW vs anchor 005Wt000003NDEBIA4) and self-checked it as "PASS"
  (self-anchored false-green), but the validator scored 0. The simpler direct path got these
  right at the anchor; the mart re-grain perturbed the ranking attribution. This is the exact
  dab0017 "dbt adds ±variance on the queries it doesn't help" cost — now landing INSIDE the one
  dataset the gate routes to dbt.

## Behavioral analysis

The gated classifier is mechanically SOUND: it routed all 4 datasets to the correct method with
zero leak, so the isolation thesis holds — the only place dbt touched the board was crmarenapro.
And on crmarenapro the dbt cross-source `int_` derivation is REAL and BANKABLE in principle:
q3 and q7 flipped on a genuine mechanism delta (effective_stage from the transcript join; breach
from the case↔order↔KB join), curing the dab0017 no-mechanism-delta NO-OP — the README revision
did exactly what it was designed to.

BUT the dbt path's overhead/variance tax did not vanish; it relocated. On crmarenapro the same
dbt re-grain that unlocked q3/q7 simultaneously knocked out q12/q13 (ranking-attribution
queries the direct path answered correctly). crmarenapro nets **0** (9/13 → 9/13, a different
9). The gate removed the board-wide tax (the 2-source datasets are untouched by dbt) but could
not remove the WITHIN-dataset tax on the one firing dataset — dbt helps the derivation-blocked
queries and hurts the ranking queries on the SAME dataset, and they cancel. This refines the
dab0017 honest-ceiling finding: the dbt advantage on crmarenapro is not just variance-fragile,
it is **self-cancelling at the dataset grain** — you cannot bank q3/q7 without paying q12/q13.

The direct-path canary swings (yelp −4, stockmarket −1, googlelocal +1; net −4 on the direct
path) are NOT this lever's effect — they are the codex/gpt-5.5 temp=0 run-to-run variance on
the verbatim baseline README (yelp's city/state extraction from a noisy free-text field is a
classic variable-band cell). They confirm the dab0017 calibration lesson (temp=0 is not
cell-stable; a single draw swings ±several cells) and are exactly what the gate is designed to
leave alone — and it did.

## Failure Review

**Primary type: variance-unclear / diagnosis-confirmed (NOT gate-leak, NOT infrastructure).**

1. **What did we expect, what happened?** Expected: gate fires only on crmarenapro, banks ≥1 of
   q2/q3/q7/q8 via the int_ derivation with the 2-source canaries byte-identical to the anchor.
   Happened: gate fired perfectly (zero leak); the int_ derivation genuinely flipped q3+q7 (+2);
   but dbt-overhead regressed q12+q13 (−2) on the SAME dataset → crmarenapro net 0. Direct-path
   canaries wobbled on solver variance (gate correctly did not touch them).
2. **Is it the lever or the harness?** The LEVER (and the method), not the harness. Audit clean,
   no taint, no mongo/PG/host failures; every dataset completed. The classifier is correct. The
   net-0 is a real property of dbt-on-crmarenapro, not a bug.
3. **Gate-leak?** NO — proven from all 4 classifier lines: crmarenapro=6→B, the three 2-source
   datasets=2→A. "Zero regression by construction" holds; the canary drops are direct-path
   variance, not the dbt branch firing.
4. **Is the crmarenapro unlock stable / worth banking?** NO at the dataset grain. q3/q7 are real
   derivation flips, but q12/q13 dbt-overhead losses cancel them WITHIN crmarenapro. A finer gate
   (route to dbt, then for the ranking queries fall back to the direct mart) is conceivable but
   is no longer the clean "one classifier" idea — it is per-query method selection, which needs
   an oracle-free signal for "is this a derivation query or a ranking query" that the README
   cannot reliably supply (the solver already self-false-greened q12).
5. **Stop / probe / file / escalate?** STOP this lever as specified (NO-GO). The dbt family for
   DAB is now CLOSED with a sharper boundary than dab0017: gated-dbt removes the board-wide tax
   but the crmarenapro dbt advantage is self-cancelling at the dataset grain (q3/q7 in, q12/q13
   out). Bank the knowledge; do not promote.

**Decision: NO-GO.** The gate mechanism is validated (sound, zero-leak) and the int_ derivation
is proven real (q3/q7 mechanism delta) — both are genuine knowledge gains — but the hypothesis's
GO criterion (beat the anchor with zero canary regression) is not met: crmarenapro nets 0 because
dbt's within-dataset overhead tax cancels its derivation advantage, and the direct-path canaries
confirm single-draw temp=0 variance rather than a lift. Recommend CONCLUDE/REJECTED.

## Workflow-refinement evaluation

No new stage / reorder / protocol change. This run REINFORCES two existing protocol rules rather
than refining them: (1) judge a flip by committed-artifact mechanism delta, not the headline rate
— crmarenapro's 9/13→9/13 hides a 4-cell recomposition that only the per-query + transcript
adjudication surfaces; (2) the gate-leak vs direct-path-variance distinction REQUIRES reading the
classifier line in each dataset's transcript before calling any canary drop a regression (here it
prevented mislabeling yelp's −4 as a gate-leak NO-GO). No WORKFLOW-REFINE.md edit needed (DAB
tracks learnings in the entity + memory).

## Stage Report: smoke

- DONE: Launch the detached smoke run and return the handle immediately without waiting; --explain selection re-confirmed = {crmarenapro, yelp, stockmarket, googlelocal}.
  Launched handle `runs/.rk-handles/dab0018-smoke-20260622-044911/`; --explain materialized exactly the 4 datasets; FO owned the wait.
- DONE: rk audit --policy strict + rk score; capture the focused score + clean-audit attestation in ## Smoke result.
  Audit CLEAN (4 clean / 0 coverage_missing / 0 tainted); stratified Pass@1 = 0.7302 over 4 datasets. See `## Smoke result`.
- DONE: Deep-dive — prove the mechanism delta for each crmarenapro flip; confirm 2-source canaries vs gate-leak/infra/variance. Write ## Smoke result + ## Behavioral analysis; append ## Failure Review on NO-GO.
  q3+q7 flipped via PROVEN int_ cross-source derivations (effective_stage from transcript join; breach from case↔order↔KB join) — mechanism delta confirmed from the transcript. q12+q13 regressed on dbt-mart re-grain (overhead tax). All 3 two-source canaries ran METHOD A (classifier lines verified) → ZERO gate-leak; canary swings are direct-path temp=0 variance. ## Failure Review (primary type: variance-unclear/diagnosis-confirmed) + Workflow-refinement eval appended. Verdict NO-GO.

### Summary

The gated classifier is mechanically SOUND (routed all 4 datasets to the correct method, zero
gate-leak — "zero regression by construction" holds) and the dbt cross-source int_ derivation is
REAL on crmarenapro: q3 (effective_stage=Negotiation from the activity-transcript join) and q7
(breached article from the case↔order↔knowledge-base join) flipped FAIL→PASS on a genuine
mechanism delta, curing the dab0017 no-mechanism-delta NO-OP. BUT the dbt overhead tax relocated
into the firing dataset — q12/q13 (ranking-attribution queries) regressed on the mart re-grain,
cancelling the gain (crmarenapro 9/13→9/13, net 0). The dbt advantage on crmarenapro is
self-cancelling at the dataset grain. Direct-path canary swings (yelp −4, stockmarket −1,
googlelocal +1) are codex temp=0 variance, not this lever. NO-GO; recommend CONCLUDE/REJECTED —
dbt family CLOSED for DAB with a sharper boundary than dab0017.

## Multi-trial crmarenapro probe (launched — detached)

AC-mandated ≥3-draw crmarenapro-ONLY probe (captain decision at the smoke gate: the gate
provably isolated dbt to crmarenapro, so the score can only move via crmarenapro, which netted 0
on one draw — and dab0017 saw crmarenapro swing to 11/13 on a single draw, so judge by ≥3 draws).

- **Spec:** `specs/dab0018-gated-dbt-classifier.crma3.frozen.yaml` — crmarenapro only, `trials: 3`,
  SAME `solver_workflow: ./solver_workflows/dab0018-gated-dbt-classifier` (no IV change).
- **Handle:** `runs/.rk-handles/dab0018-crma3-20260622-063822/` (pid 1457514).
- **Selection re-confirmed** (`rk run --explain`, $0): Tasks=1 (crmarenapro), trials=3 → 39 cells.
- **ETA** ~30–45 min (crmarenapro dbt build dominates, ×3 draws at concurrency.trials:2).
- **Decision rule:** GO-to-full iff crmarenapro STABLY nets ≥+1 vs anchor 9/13 — i.e. ≥10/13 in a
  clear majority of draws WITH q3/q7 holding. Else NO-GO → conclude/REJECTED.
- Phase 2 (audit + score + per-draw/per-query analysis) runs after the FO re-engages on `done` rc=0.

## Multi-trial crmarenapro probe

**Run:** `runs/dab0018-gated-dbt-classifier/a4bd65ccaa565853` (rc=0, 21 min, 2026-06-22).
**Spec:** `specs/dab0018-gated-dbt-classifier.crma3.frozen.yaml` (crmarenapro only, trials:3, same
gated README). **Score:** stratified 0.7692, **n_completed=2, n_errored=1.**

### Audit + the RuntimeError (resolved FIRST) — 2 clean draws, 1 infra-killed

`rk audit --policy strict`: **clean:2 / coverage_missing:1 / tainted:0.**
- `crmarenapro__W3gXnUG` — CLEAN
- `crmarenapro__hY8viTH` — CLEAN
- `crmarenapro__RLfCSTP` — **coverage_missing (the RuntimeError) = INFRASTRUCTURE, NOT a result.**
  `trial.log`: `Docker compose ... up --wait ... Return code: 1 ... volume
  "dab-postgres-data-crmarenapro-v1-crmarenapro" already exists but was created for project
  "crmarenapro__rhkgy2a" (expected "crmarenapro__rlfcstp") ... container
  crmarenapro__rlfcstp-dab-postgres-1 is unhealthy ... dependency failed to start`. Two
  same-dataset draws ran concurrently (`concurrency.trials:2`) and **collided on the shared named
  postgres volume/network** → postgres never went healthy → the draw lost all 13 queries before
  the agent ran. This is the dab-postgres concurrency/degradation signature (memory:
  dab-postgres-degradation-dual-signature; the per-dataset volume isolation PR #18 covers the
  multi-dataset case, not two draws of the SAME dataset sharing one volume name). **Excluded from
  the verdict — not counted as a crmarenapro failure.** We have **2 clean draws**, below the AC's ≥3.

### Per-draw crmarenapro totals (CLEAN draws only)

| Draw | Total | FAILs |
|---|---|---|
| W3gXnUG | **11/13** | q8, q13 |
| hY8viTH | **9/13** | q2, q8, q12, q13 |

vs anchor `@codex-batch-baseline` crmarenapro = 9/13. So the two clean draws are **+2 and +0**.

### Per-query pass-count across the 2 clean draws (out of 2)

`q1=2 q2=1 q3=2 q4=2 q5=2 q6=2 q7=2 q8=0 q9=2 q10=2 q11=2 q12=1 q13=0`

- **q3 (effective_stage=Negotiation) HOLDS 2/2** ✅ and **q7 (breach ka0Wt000000EoD3IAK) HOLDS 2/2** ✅
  — the proven cross-source int_ derivations are STABLE. Both clean draws fired METHOD B (dbt,
  classifier `N_sources=6 -> METHOD B` on both; `dbt run`×15 / ×14; q7 article derived in both).
- **q13 regresses 0/2** — a DETERMINISTIC dbt-mart re-grain cost (ranking-attribution; the direct
  anchor got it right).
- **q12 is VARIANCE 1/2** — passed in W3gXnUG, failed in hY8viTH (not a deterministic dbt cost).
- **q2 is VARIANCE 1/2** — cracked once (W3gXnUG) via the int_quote_policy_breach join, missed once.
- **q8 never cracks 0/2** — the fewest-transfer agent stays wrong both draws.

### Verdict — NO-GO (decision rule not met)

Decision rule: GO-to-full iff crmarenapro STABLY nets ≥+1 vs anchor 9/13 — ≥10/13 in a **clear
majority** of clean draws WITH q3/q7 holding. q3/q7 DO hold 2/2 (the lever's core derivation is
real and stable). BUT on the ≥10/13 threshold the 2 clean draws are a **1–1 split** (11/13 and
9/13) — NOT a clear majority. crmarenapro's NET swings between +2 and 0 depending on whether the
VARIANCE cells (q2, q12) land, while q13 (det. dbt cost) and q8 (never-crack) bound the ceiling.
The dbt advantage is **real on q3/q7 but the dataset net is not stably ≥+1** — it is variance
between +2 and 0, the same temp=0 instability dab0017 flagged.

**NO-GO → CONCLUDE/REJECTED.** The 1–1 split does not clear the bar. Caveat for the captain: the
3rd draw was infra-killed, so this rests on 2 (not 3) clean draws; a tie-breaking relaunch of the
3rd draw at **concurrency.trials:1** (to avoid the same-dataset volume collision) would resolve
11-vs-9 cleanly. But even a 2-of-3 ≥10/13 would be a thin, variance-bounded +1–+2 on a single
dataset whose q13 deterministically regresses — consistent with the smoke-stage finding that the
crmarenapro dbt advantage **self-cancels at the dataset grain**. Recommend concluding REJECTED;
the relaunch is optional tie-break, not likely to change the family verdict.

### Tie-break 3rd clean draw (launched — detached)

Captain wants a full 3-draw read; the crma3 3rd draw was infra-killed by a same-dataset volume
collision, so this draw runs at **`concurrency.trials:1`** (only one crmarenapro instance at a
time → no shared named-volume race).

- **Spec:** `specs/dab0018-gated-dbt-classifier.crma1.frozen.yaml` — crmarenapro only, `trials:1`,
  `concurrency.trials:1`, SAME gated `solver_workflow` (no IV change).
- **Handle:** `runs/.rk-handles/dab0018-crma1-20260622-072128/` (pid 1493371).
- **Selection** (`rk run --explain`): Tasks=1 (crmarenapro), 13 cells.
- **ETA** ~12–18 min (one crmarenapro dbt build, single draw).
- **Decision rule (over 3 clean draws):** GO-to-full iff crmarenapro nets ≥10/13 in a clear
  majority (≥2 of 3) WITH q3/q7 holding; else NO-GO → conclude/REJECTED. Prior clean draws:
  W3gXnUG 11/13, hY8viTH 9/13.

### Tie-break 3rd clean draw — RESULT + FULL 3-DRAW READ (verdict REVISED to GO-to-full)

**Run:** `runs/dab0018-gated-dbt-classifier/b4ca814473aa3d00` (rc=0, 16 min). **Audit `--policy
strict`: CLEAN 1/0/0** — the `concurrency.trials:1` fix worked, no same-dataset volume
collision. **This draw (`crmarenapro__7yYuxr3`) = 11/13** (fails q2, q8). METHOD B fired
(classifier `N_sources=6 -> METHOD B`; `dbt run`×16); q3 (effective_stage=Negotiation) and q7
(breach ka0Wt000000EoD3IAK ×8 in trace) BOTH derived and PASSED again.

**Three clean draws (vs anchor `@codex-batch-baseline` crmarenapro = 9/13):**

| Draw | Total | vs anchor | FAILs |
|---|---|---|---|
| W3gXnUG | **11/13** | +2 | q8, q13 |
| hY8viTH | 9/13 | +0 | q2, q8, q12, q13 |
| 7yYuxr3 | **11/13** | +2 | q2, q8 |

**Per-query pass-count across all 3 clean draws (out of 3):**

`q1=3 q2=1 q3=3 q4=3 q5=3 q6=3 q7=3 q8=0 q9=3 q10=3 q11=3 q12=2 q13=1`

- **q3 = 3/3 and q7 = 3/3** — the proven cross-source int_ derivations hold EVERY clean draw.
  All 3 draws fired METHOD B (dbt); classifier never flaked.
- **q8 = 0/3** — the fewest-transfer agent never cracks (a genuine miss, not variance).
- **q2 = 1/3, q12 = 2/3, q13 = 1/3** — variance cells (none deterministic). q13 is NOT a
  deterministic dbt cost after all — it recovered in the 3rd draw (the 2-draw read mislabeled it
  0/2 → it's 1/3); q12 passes in 2/3.

**DECISION RULE over 3 clean draws (≥10/13 in a clear majority WITH q3/q7 holding): MET.**
2 of 3 draws are ≥10/13 (11, 9, 11) — a clear majority — and q3/q7 hold 3/3. **Verdict REVISED
from NO-GO to GO-to-full.**

**Honest magnitude + caveat (both, per the captain's ask):**
- **Does it clear the rule?** YES — 11/9/11, median 11/13 = **+2 over anchor on crmarenapro**,
  with the lift mechanism PROVEN (q3/q7 cross-source int_ derivation, not a #-strip).
- **Is the lift real enough to justify a full run?** Marginal but real. The stable structure is:
  q3+q7 reliably IN (the +2 mechanism), q8 reliably OUT; q2/q12/q13 wobble. So crmarenapro's
  typical outcome is 11/13 (+2) with a 9/13 floor on a bad draw. The earlier "self-cancelling"
  read was an artifact of the single smoke draw + the 2-draw sample (where q13's lone failure
  looked deterministic); the 3-draw read shows q13/q12 are variance, not a fixed dbt tax, so the
  derivation gain is NOT fully cancelled — median net is **+2**.
- **dab0017 calibration caveat (still load-bearing):** +2 on ONE dataset ≈ **+0.013 stratified**
  (1/12 datasets × +2/13). The other 11 datasets run the verbatim direct path and, at temp=0,
  inject ±several cells of run-to-run noise each (the smoke draw already showed yelp swinging
  −4). A single full-run draw's stratified number could easily move ±0.02–0.05 from that
  direct-path noise alone — i.e. the +0.013 crmarenapro signal can be SWAMPED by direct-path
  variance on any single full draw. The gate guarantees the EXPECTED direct-path contribution
  equals the anchor's (byte-identical method), so over draws it is unbiased, but a single full
  draw is not a clean readout. **Recommendation for the full stage: if run, judge the full board
  the same way — crmarenapro per-query (q3/q7 hold? +2?) attributed as the lift, the 11 direct
  datasets judged against their multi-draw band, NOT a single stratified delta.**

**Bottom line: GO-to-full** — the gate is sound (zero leak), the dbt derivation is real and
STABLE on q3/q7 (3/3), crmarenapro nets a median +2 (11/13) clearing the decision rule. The
honest ceiling is small (≈+0.013 stratified) and exposed to direct-path temp=0 noise on a single
full draw, so the full run is worth doing but must be judged by attributed per-query mechanism,
not a single headline stratified number.

## Full run (launched — detached)

Captain APPROVED smoke → full (3-draw probe cleared the bar: crmarenapro 11/9/11, q3/q7 hold 3/3).

- **Spec:** `specs/dab0018-gated-dbt-classifier.frozen.yaml` — all 12 datasets (54 cells),
  `trials:1`, `concurrency.trials:2`, SAME gated `solver_workflow` (the IV). No spec change: the
  crma3 same-dataset volume collision does NOT apply — concurrency.trials:2 runs two DIFFERENT
  datasets in parallel (isolated per-dataset volumes, PR #18).
- **Handle:** `runs/.rk-handles/dab0018-full-20260622-075729/` (pid 1514664).
- **ETA** ~60–120 min (54 cells; crmarenapro dbt build + 11 direct datasets at concurrency.trials:2).
- Phase 2 (audit `--policy strict` + score → ## Run result; behavioral attribution held for the
  analyze stage) runs after the FO re-engages on the `done` sentinel (rc=0).

### Full run RELAUNCHED (prior run auth-tainted)

The first full launch (`runs/dab0018-gated-dbt-classifier/adcde4521869777a`) was TAINTED — a codex
`refresh_token_reused` auth failure hit all 12 datasets at launch, every cell returned reward 0 in
~9 min with nothing executed. NOT a lever/method result. Captain re-authenticated codex
(`codex login --device-auth`, successful) and relaunched.

- **Relaunch handle:** `runs/.rk-handles/dab0018-full2-20260622-082125/` (pid 1569593), SAME full
  frozen spec (no spec change). ETA ~60–120 min.
- Phase 2 (audit `--policy strict` + score → ## Run result) at the `done` sentinel (rc=0).

### Full run RELAUNCHED (3rd attempt — fresh run dir)

The 2nd full launch's run dir (`runs/dab0018-gated-dbt-classifier/adcde4521869777a`) was removed —
it was the auth-tainted run (codex `refresh_token_reused` at launch) AND it left a `lock.json`
conflict blocking a clean relaunch. This 3rd attempt is a FRESH run dir.

- **Relaunch handle:** `runs/.rk-handles/dab0018-full3-20260622-083253/` (pid 1573694), SAME full
  frozen spec `specs/dab0018-gated-dbt-classifier.frozen.yaml` (no spec change). ETA ~60–120 min.
- Phase 2 (audit `--policy strict` + score → ## Run result) at the `done` sentinel (rc=0).

## Run result

**Run:** `runs/dab0018-gated-dbt-classifier/adcde4521869777a` (full3, fresh run dir; rc=0,
~81 min — started 2026-06-22T08:32:53Z, ended 09:54:07Z). **All 12 datasets / 54 cells, trials:1.**

**Audit (`--policy strict`): CLEAN — clean:12 / coverage_missing:0 / tainted:0.** Not an
auth-taint repeat: the run took ~81 min (the taint signature is every-cell-0 in ~9 min) and every
dataset has a populated `reward_per_query.json` with executed results.

**Score (`rk score --format json`): stratified Pass@1 = `0.6927` (n_completed=12, n_errored=0).**
vs anchor `@codex-batch-baseline` (`runs/codex-dab-batch-baseline/bf113446fdd94373`) = **0.6966** →
**−0.0039**, i.e. essentially flat, INSIDE the direct-path temp=1 noise band the 3-draw probe
flagged (the gate makes the 11 direct datasets unbiased vs anchor in expectation, but a single full
draw injects ±several direct-path cells).

**Per-dataset (this draw):**

| Dataset | Pass | Dataset | Pass |
|---|---|---|---|
| crmarenapro (Method B, dbt) | **11/13** | bookreview | 3/3 |
| yelp | 7/7 | music_brainz_20k | 3/3 |
| stockmarket | 4/5 | stockindex | 3/3 |
| googlelocal | 3/4 | PANCANCER_ATLAS | 2/3 |
| GITHUB_REPOS | 2/4 | DEPS_DEV_V1 | 1/2 |
| agnews | 1/4 | PATENTS | 0/3 |

**crmarenapro per-query (the gate-fires dataset — `N_sources=6 → METHOD B`):** 11/13, fails only
**q8** (never-crack across all probe draws — `005Wt000003NBcAIAW` vs expected `005Wt000003NIliIAG`)
and **q9** (`SC` vs expected `MI`). The lever's core derivation flips **HELD**: **q3 PASS**
(effective_stage=Negotiation), **q7 PASS** (breach `ka0Wt000000EoD3IAK`), and q2/q12/q13 all PASS
this draw — the +2 / 11-13 outcome the 3-draw probe predicted as the typical case. Full behavioral
attribution (mechanism delta per flip, direct-path canary band, q8/q9 diagnosis) is deferred to the
**analyze** stage per the stage split.

## Stage Report: full

- DONE: Record the dab0018-full3 relaunch in the entity file.
  Appended `### Full run RELAUNCHED (3rd attempt — fresh run dir)` under `## Full run (launched — detached)`: handle `runs/.rk-handles/dab0018-full3-20260622-083253/` (pid 1573694), spec `specs/dab0018-gated-dbt-classifier.frozen.yaml`; context = adcde4521869777a removed (tainted auth + lock.json conflict), fresh run dir. Handle dir + pid 1573694 verified live (`ps`), meta confirms key=dab0018-full3 / mode=run.

### Summary

Pure record-keeping for the full stage: documented the 3rd full-run launch attempt. The prior run
dir `adcde4521869777a` (auth-tainted, `refresh_token_reused`) was removed because it left a
`lock.json` conflict blocking a clean relaunch, so full3 runs in a fresh run dir on the same full
frozen spec (no IV/spec change). Run is detached (pid 1573694, verified live); audit + score happen
when the FO re-engages on the `done` sentinel.

## Stage Report: full (audit + score)

- DONE: `rk audit --policy strict` — confirm clean; not an auth-taint repeat.
  CLEAN clean:12 / coverage_missing:0 / tainted:0 (all 12 datasets present). NOT auth-taint: ~81 min wall (08:32:53→09:54:07), every dataset has a populated `reward_per_query.json` with executed results.
- DONE: `rk score --format json` — record absolute stratified Pass@1 + crmarenapro per-query line; write run-dir + headline into `## Run result`.
  Stratified Pass@1 = 0.6927 (12 completed / 0 errored) vs anchor @codex-batch-baseline 0.6966 → −0.0039 (flat, inside direct-path noise). crmarenapro (Method B, N_sources=6) = 11/13; q3 PASS + q7 PASS hold, q2/q12/q13 also PASS, only q8 (never-crack) + q9 fail. `## Run result` written. Full behavioral attribution deferred to analyze.

### Summary

full3 landed clean (audit 12/0/0, ~81 min — not the ~9 min auth-taint signature). Stratified
Pass@1 = 0.6927, essentially flat vs anchor 0.6966 (−0.0039, inside the direct-path single-draw
noise band the 3-draw probe predicted). The gate-fires dataset crmarenapro hit its typical 11/13
with the proven q3/q7 cross-source int_ derivations holding (q2/q12/q13 also passed this draw; q8
never-cracks, q9 the only other miss). Mechanism attribution + canary-band judgment are the
analyze stage's job.
