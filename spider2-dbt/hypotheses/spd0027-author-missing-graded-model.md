---
id: spd0027
title: Build-the-gap forcing check — author every declared-but-absent graded model (C7)
status: smoke
kind: hypothesis
source: "spd0026 fan-out, family C7. synthea001 (champion errored building cost = UNION of int__cost_*) + xero_new001 (champion authored none of 3 declared models). Sharpens existing R5/R6 into a Validation-stage declared-vs-built diff forcing check. forks champion @baseline spd0013."
started: 2026-06-28
completed:
verdict:
score:
worktree:
archived:
---

A graded target that is never built is an automatic zero. The champion README already says to enumerate
every declared model (R5) and to union sibling intermediates (R6), but synthea001 and xero_new001 still
produce nothing. The lever adds a Validation-stage **build-the-gap check**: diff the declared model set
(schema.yml + dbt's undefined-ref/missing-model warnings) against the built base-table set, and author +
build every gap, fixing build errors inside the new model rather than abandoning it.

## Lever (one gated addition, Validation stage)
`### Build-the-gap check — every declared graded model MUST exist as a base table` (see
`solver_workflows/spd0027-author-missing-graded-model/README.md`). Content hash 845ba003.

## Smoke
spec `specs/spd0027-author-missing-graded-model.smoke.frozen.yaml`, trials=1.
- FLIP targets: synthea001, xero_new001
- canaries (must hold): f1001, mrr001, quickbooks002

## Result
**SMOKE = NO-GO (held for captain; no full, no promote).** 2026-06-28, run
`runs/spd0027-author-missing-graded-model/c58c5d339fcf7372`.
- Targets: synthea001 **FAIL**, xero_new001 **FAIL** — neither flipped.
- Canaries: f1001, mrr001, quickbooks002 — all **PASS** (clean, no bleed → lever is gated/safe).
- Mechanism: the build-the-gap directive WAS read (3–5 mentions in the agent logs) but the targets
  still failed → the execution wall, not non-reading. Consistent with the prior C7 prediction (R5/R6
  already in the champion; sharpening them is read-but-the-multi-source build still doesn't land).
  No regression. Captain decides conclude/REJECTED.
