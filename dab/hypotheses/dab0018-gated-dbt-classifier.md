---
id: dab0018
title: Classifier-gated dbt — route multi-source-derivation datasets to dbt, all others to the direct method
status: propose
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
