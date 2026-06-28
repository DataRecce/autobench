---
id: spd0028
title: Cast-to-text for a string-operation INPUT, distinct from re-typing the emitted id (C6)
status: smoke
kind: hypothesis
source: "spd0026 fan-out, family C6 (NEW). social_media001 needs a numeric id cast to varchar BEFORE split_part. Threads a narrow exception against the README's existing 'never cast an id' identifier-dtype guard. forks champion @baseline spd0013."
started: 2026-06-28
completed:
verdict:
score:
worktree:
archived:
---

The champion README forbids casting an identifier column's dtype (correct, for the EMITTED column). But a
numeric id used as the INPUT to a string operation (`split_part`/`regexp_*`/`||`) must be cast to varchar
for the operation to work. The lever adds one G3 bullet drawing that distinction: cast for the op input,
keep the emitted key at source dtype.

## Lever (one gated G3 bullet, after "Identifier dtype — DO NOT GUESS")
see `solver_workflows/spd0028-cast-before-string-op/README.md`. Content hash 4b327448.

## Smoke
spec `specs/spd0028-cast-before-string-op.smoke.frozen.yaml`, trials=1.
- FLIP target: social_media001
- canaries (must hold): f1001, mrr001, quickbooks002, hubspot001

## Result
_(autonomous — recorded after smoke; HELD at smoke, no full/promote)_
