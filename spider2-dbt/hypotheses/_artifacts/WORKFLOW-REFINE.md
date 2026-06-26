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
  Behavior CHANGED: on airbnb001 the contract drove a correct unconditional latest-window (no
  `is_incremental` gate), making the cell strictly closer (REVIEW_TOTALS/REVIEW_SENTIMENT/grain all
  gold-exact); on recharge002 the contract's spine/coalesce skeleton drove a fuller calendar spine
  (124 rows) that REGRESSED a passing champion construction (122 rows, 1.0→0.0). Net standalone: airbnb001
  still 0.0 (MOM value-definition blocker outside the template), one telemetry regression → NO-GO.
- learning: a structured pre-edit contract IS enforceable at gpt-5.5/codex (fire-and-obey, not
  detected-but-not-obeyed) — so the contract STAGE is validated infrastructure. But two sharp limits:
  (1) a contract template can only make the worker COMPLY with the dimension it names; it is oracle-blind
  to a residual blocker outside its vocabulary — airbnb001's window template solved the window and exposed
  a MOM value-definition gap (gold MOM=NULL) the template cannot reach. A latest-window template needs a
  companion value-def field for derived metrics (when is the metric NULL / what prior period). (2) a
  generative skeleton field ("left-join onto the spine, coalesce to 0") can EXPAND the graded row set past
  the passing grain (recharge002 124 vs 122) — `G2_REPORT_RAW_GROUPING_HOLD` needs an explicit
  forbidden-pattern: a zero-filled spine must be bounded to the same date/grain set the passing
  construction used, never a fuller calendar. The contract's own `validation_signature` passed truthfully
  ("totals equal latest 30-day fact counts") while the graded column was wrong — reconfirms that a
  worker-derived structural signature is necessary-not-sufficient; it cannot self-anchor onto the gold
  value semantics.
- bears-on: spd0007 (the airbnb001 MOM gap is a value-definition fork — that family owns the metric-NULL
  semantics; a value-def contract field belongs there); a future relocation hypothesis (the spine-grain
  forbidden-pattern for report/rollup targets).
- evidence: `runs/spd0011-classifier-contract-smoke/1e6a6226d63abfbb` (strict-clean, rc=0); committed-artifact
  deep-dive in spd0011 `## Behavioral analysis`; champion comparison `runs/spider2-dbt-spd0008-full/4ba55fba0138a84d`.
- status: rejected-as-written (concluded validated-not-promoted 2026-06-26). The contract STAGE is validated
  fire-and-obey infrastructure and bankable, but standalone it is net-negative (0 flips + 1 telemetry
  regression). Carry the IDEA forward with the two refinements (value-def/MoM template field; spine-grain
  forbidden-pattern) into the stabilization loop; do NOT promote to `@baseline` standalone.
