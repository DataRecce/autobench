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
- status: open — revise route (bound R1 repair + R3 precedence, harden R5, re-scope smoke); re-smoke pending.
