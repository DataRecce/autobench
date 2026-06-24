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

<!-- No structural hypotheses concluded yet. spd0001 (anchor) and spd0002 (rule tweak inside the
output-contract section) are NOT structural — they will not appear here. -->
