# spider2-dbt — workflow-refinement log

Track learnings from **structural** solver-workflow changes here (a new stage / reorder / replace /
new protocol-family in the SOLVER README), not just rule tweaks inside an existing section. A rule
tweak's learning goes in the entity + `self-learning.md`; a structural change's learning goes HERE and
must reach a final state before the hypothesis archives (README → `conclude`).

Entry format:

```
## spd<NNNN> — <title>
- layer: <which part of the solver workflow changed>
- refinement type: new-stage | reorder | replace | new-protocol | rule-tweak(N/A here)
- finding: <what happened across the whole smoke/full set, not just the target>
- learning: <the sharp, transferable lesson>
- bears-on: <sibling spd<NNNN> ids this should steer>
- evidence: <run-dir / committed-artifact cite>
- status: open | adopted-into-workflow | rejected-as-written
```

## spd0006 — Classifier router (Axis-1 materialization gate)
- layer: a NEW `## Stage: Classify (router)` prepended to the solver README, before Exploration —
  decides WHAT to build per `condition_tabs` table (R1 build-as-is / R2 author-from-schema.yml /
  R3 fixture-flag / R4 default / R5 enumerate-every-target / R6 verbatim-union) on oracle-free signals.
- refinement type: new-stage
- finding: across the full 7-cell smoke the router FIRED on every target and classified each to the
  correct branch (zuora→R1, superstore→R2, synthea→R6, intercom→R5); 0/4 flipped but 3/3 canaries held
  and the R4 default left ordinary authoring (activity001) unchanged. Artifacts moved toward gold:
  zuora stopped creating new models, synthea stopped fabricating 32 condition rows (836→807, R6 union
  obeyed). So the new stage is exercised and behavior-changing, NOT inert — the classification layer works.
- learning: a per-target oracle-free materialization router IS steerable at gpt-5.5/xhigh (the solver
  reliably reads file/name/schema signals and picks the branch) — the wall is NOT classification but
  the BRANCH BODIES' secondary contracts: (1) an unbounded "repair if build fails" clause lets the
  solver corrupt a target's grain to force a green build — bound repair to the feature boundary and let
  R3 (absent-source) win over R1 repair; (2) the AUTHOR branch must pin the per-column type/projection
  contract (id dtype) or it bleeds into value-def; (3) a "build every contract table" rule must be a HARD
  enumeration source (declared schema.yml table set), not a soft reminder, to beat prose-scoping; (4) a
  verbatim-union branch is defeated by a missing package (`dbt_utils`) that forces a row-perturbing shim
  = infra, not steerability.
- bears-on: spd0007 (the superstore order_id dtype miss is a value-def contract, owns it), spd0009
  (intercom needs full-dimension grain — the spine conflict), spd0010 (the R3 fixture-flag + the
  `dbt_utils` packaging defect are harness-side).
- evidence: `runs/spider2-dbt-spd0006-smoke/8f185cee4407c0f4` (strict-clean); per-target committed-artifact
  deep-dive in spd0006 `## Behavioral analysis`.
- status: open — v2 re-smoke done (`runs/spider2-dbt-spd0006-smoke/1d1af6c748b8fce8`). Verdict on the
  STRUCTURE: the materialization router (R1–R5) is VALIDATED and PROVEN NON-DESTABILIZING — the f1001
  canary "regression" is gpt-5.5 value-level variance (v1/v2 built identical model sets; hardened R5
  added 0 extra tables; identical reported values), NOT router over-fire. So the central risk of the
  classifier-stage strategy (a generative router regressing passers) is DISPROVEN. Two refinements
  remain: (1) **R6 "verbatim union" is defective** — correct for synthea's `cost` (union is the right
  shape) but actively WRONG for apple_store's source_type/territory reports (a naive union of the
  sub-grain intermediates reproduces the over-emit baseline 29/36 vs gold 9/17; the fix is a grain
  ANCHOR + LEFT-join = spd0008's job). R6 should be narrowed or dropped; apple_store routes to spd0008.
  (2) the bounded-repair rule still let the solver edit upstream `int_` intermediates feeding an R6
  union (synthea −13 rows) — verbatim-union must mean `SELECT *` from the intermediates, never edit them.
- learning (v2): a materialization router is NECESSARY-NOT-SUFFICIENT — it makes targets materialize at
  the right name/grain (social_media001: all 5 tables gold-exact) but standalone rarely FLIPS a cell,
  because the residual gap is almost always value-def (spd0007) or grain (spd0008). The "each lever must
  flip ≥1 standalone" smoke gate is mis-fit for enabling-infrastructure; the router's value is realized
  only when composed with the value/grain lever. → recommend banking R1–R5 as a structural base and
  testing spd0007 ON TOP, where the flips (social_media, superstore, retail, divvy…) actually land.
- bears-on: spd0007 (social_media + superstore flips are gated here, router already materializes them),
  spd0008 (apple_store grain-anchor; R6 rework), spd0010 (synthea `lowercase_columns` macro + zuora_source
  are fixture gaps).
- status: **adopted-as-scaffolding** (concluded validated-not-promoted 2026-06-25). The router (R1–R5)
  is carried into spd0007 as the base solver with R6 NARROWED (same-grain domain-partition unions only;
  never report/rollup targets; never edit the intermediates). Not promoted to `@baseline` standalone
  (0 flips), but proven non-destabilizing and necessary infrastructure; earns promotion by composition
  in spd0007 where the value-def lever supplies the flips.

## spd0011 — Implementation Contract checkpoint (make router advice enforceable)
- layer: new pre-SQL "Implementation Contract" stage between Exploration and Implementation + a
  contract-signature check added to Validation (forked from champion spd0008; purely additive).
- refinement type: new-stage + new-protocol (a 9-field contract artifact + a 2-template inventory:
  `G2_LATEST_WINDOW_FULL_REFRESH`, `G2_REPORT_RAW_GROUPING_HOLD`).
- finding: across the 12-cell smoke the contract stage FIRED and produced its declared artifact on EVERY
  target and was OBEYED in the committed SQL — it is NOT inert (directly refutes the G7 propose-WARN that
  a process checkpoint would be acknowledged-and-skipped). AC-2 met (contract written 08:33:05Z before the
  first apply_patch 08:33:47Z on airbnb001) and AC-4 met (Validation ran direct DuckDB structural checks —
  base-table type, grain uniqueness, single-date, representative rows — beyond the clean `dbt build`).
  TWO SMOKE CYCLES. Cycle-1 (`1e6a6226…`, 10/12): contract drove a correct unconditional latest-window on
  airbnb001 (totals/sentiment/grain gold-exact) but `G2_REPORT_RAW_GROUPING_HOLD`'s spine/coalesce skeleton
  drove a fuller calendar spine on recharge002 (124 vs the champion's passing 122 rows, telemetry 1.0→0.0).
  Cycle-2 (`071b7ef9…`, 8/12 — WORSE) added FIX A (derived-metric NULL-condition on the window template)
  and FIX B (source-bounded spine on the raw-grouping template). Both fixes failed: FIX A fired but the
  worker STILL emitted a real MoM (it re-materialized a prior window rather than NULL-ing); FIX B did not
  stop `G2_REPORT_RAW_GROUPING_HOLD` from re-graining a passer — the worker selected it as primary on
  **quickbooks003** (committed-artifact proof: 4 transcript hits `selected_rule G2_REPORT_RAW_GROUPING_HOLD;
  primary`) and re-grained the general-ledger rollup, REGRESSING a HARD-GATE canary 1.0→0.0. retail001
  dropped with `selected_rule:none` = flake, not lever. Net both cycles: 0 flips; the raw-grouping template
  destabilized a passer EACH cycle (telemetry → then hard gate) → NO-GO, worsening.
- learning: a structured pre-edit contract CHECKPOINT stage IS obeyed at gpt-5.5/codex (fire-and-obey, not
  detected-but-not-obeyed) — the contract STAGE is validated, bankable infrastructure and the program's
  most transferable win. BUT a generative report-grain skeleton template (`G2_REPORT_RAW_GROUPING_HOLD`)
  REGRESSES passers: it has no oracle for correct SCOPE, selects itself as primary on report/rollup
  targets, and re-grains stable constructions (recharge002 telemetry cyc1; quickbooks003 hard gate cyc2) —
  net-negative across both cycles, even with a source-bounded-spine guard. DROP it. Two more sharp limits:
  (1) a soft NULL-condition ("NULL where the baseline is not present") is too weak — the worker found a
  computable prior window in the 12-year source and refused to NULL; the airbnb MOM fix is a derivation-
  METHOD constraint (compute period-over-period as a window `LAG` over the model's OWN single-window output,
  which mechanically NULLs MoM with one window row — proven offline == gold; mirrors the scaffold's
  `wow_agg_reviews` sibling), NOT a value-def NULL flag. (2) a worker-derived `validation_signature` passed
  truthfully ("totals equal latest 30-day fact counts") while the graded MOM column was wrong — a structural
  signature is necessary-not-sufficient and cannot self-anchor onto gold value semantics.
- bears-on: spd0012 (forks spd0008; keeps the validated contract checkpoint + `G2_LATEST_WINDOW_FULL_REFRESH`
  with the LAG-over-own-output method constraint, DROPS `G2_REPORT_RAW_GROUPING_HOLD`); future
  contract/template hypotheses (a template must name a derivation METHOD, not just a NULL flag; never ship a
  generative report-grain skeleton without a re-grouping/re-grain forbidden-pattern); spd0007 value-def
  family.
- evidence: cycle-1 `runs/spd0011-classifier-contract-smoke/1e6a6226d63abfbb`; cycle-2
  `runs/spd0011-classifier-contract-smoke/071b7ef95ce1a1d1` (both strict-clean, rc=0); committed-artifact
  deep-dives in spd0011 `## Behavioral analysis` + `## Behavioral analysis (cycle 2)` (incl. the offline
  gold reconstruction); champion comparison `runs/spider2-dbt-spd0008-full/4ba55fba0138a84d`.
- status: rejected-as-written (concluded REJECTED / validated-not-promoted 2026-06-26). The contract STAGE
  is validated fire-and-obey infrastructure and bankable; the `G2_REPORT_RAW_GROUPING_HOLD` template is a
  proven net-negative destabilizer (DROP). Carry the contract checkpoint + the latest-window template (with
  the LAG-method MoM constraint) forward in spd0012; do NOT promote spd0011 to `@baseline`.

---

## spd0012 — single-template contract checkpoint (LAG-over-own-output MoM; raw-grouping template dropped)

- layer: solver-workflow structure (carries the spd0011 contract-checkpoint STAGE forward; one-template inventory)
- refinement type: stage retained + template pruned + sub-rule hardened (soft NULL-flag → derivation-METHOD constraint)
- finding (FULL, `runs/spd0012-mom-window-lag-single-window/73c08047c34ee18a`, strict-clean 60/0/0 rc=0,
  **24/60 = 0.40 = `@baseline` net +0**): the contract checkpoint with ONLY `G2_LATEST_WINDOW_FULL_REFRESH`
  flipped airbnb001 0→1 ARTIFACT-REAL and the flip HELD smoke+full (durable; committed `LAG`-over-own-output
  ⇒ MOM NULL = gold, `selected_rule` set). EVERY other moved cell selected `selected_rule: none` (NO template):
  gains airport001/f1001/recharge001 + regressions marketo001/recharge002/retail001/f1003 = variance/flake;
  sap001 0→1 = the spd0010 FIXTURE repair (deterministic, free to any solver on the repaired board ⇒ a
  fixture-corrected spd0008 also banks it ≈25/60). quickbooks003 1→0 = 0/3 across all three contract-stage draws
  (spd0011-c2/smoke/full) with `selected_rule: none` every time ⇒ suspected DIFFUSE cost of the heavy contract
  PROSE on a borderline passer (UNRESOLVED — would need a multi-draw spd0008-vs-contract probe; captain chose to
  isolate instead). recharge002 flip-flopped smoke(1.0)↔full(0.0) = the smoke "recovery" was variance.
- learning: the contract CHECKPOINT stage flips a value-def cell via a derivation-METHOD constraint AND is obeyed
  (airbnb001 durable two-draw, artifact-attributable — the first value-def flip made README-addressable through a
  METHOD, vs spd0007's oracle-blind dtype/formula value-defs); the MECHANISM works. BUT as a whole-solver it is
  net+0 (the one durable flip is swamped by the sap001 fixture confound + `selected_rule:none` variance both
  directions and does not clear a fixture-corrected champion), and the heavy prose may DIFFUSELY cost a borderline
  passer (quickbooks003 0/3 under the stage, no template). A lighter INLINE rule may capture the same flip without
  the contract vehicle's cost — the isolation test. Confirms: a method-constraint beats a value/NULL flag, and a
  durable artifact-attributable cell can still be NON-promotable when the headline is variance-swamped + confounded.
- bears-on: spd0013 (lean-LAG isolation — does the lean inline rule flip airbnb001 without the contract scaffold,
  and does quickbooks003 recover without the contract prose?); future contract/template hypotheses (prefer the
  lightest vehicle that lands the flip); spd0007 value-def family (method-vs-definition distinction).
- evidence: full run above; smoke `runs/spd0012-mom-window-lag-single-window-smoke/14fe861107f3b0ff`;
  committed-artifact read + full attribution in spd0012 `## Behavioral analysis (full run)`; champion comparison
  `runs/spider2-dbt-spd0008-full/4ba55fba0138a84d`.
- status: rejected-as-written (concluded REJECTED / validated-not-promoted 2026-06-26). The contract checkpoint +
  LAG-method MECHANISM is validated and bankable, but the whole-solver is net+0 and the heavy prose may diffusely
  cost a borderline passer; `@baseline` UNCHANGED = spd0008 24/60. Isolation follow-up filed as spd0013.
