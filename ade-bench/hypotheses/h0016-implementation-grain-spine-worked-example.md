---
id: h0016
title: Implementation — grain-spine fix as a CONCRETE worked-example SQL skeleton (not a prose rule), to test whether copyable beats described
status: hypothesis
kind: hypothesis
source: forked from h0010's failure. h0010 stated the grain-spine fix as a PROSE Implementation rule and it was behaviorally inert (0/4 — solver discussed the spine, even built the CTE for intercom001, but never made the entity the FROM spine in the committed SQL). h0009's only win (asana002) came from copying a CONCRETE local artifact. This re-attempts the SAME grain-spine fix but in concrete, copyable, worked-example form (a generic before/after SQL skeleton with placeholder names) — the decisive test of whether a structural fix can land when made copyable rather than described. Forks the then-current @baseline (re-fork at propose).
started:
completed:
verdict:
score:
worktree:
---

## Hypothesis

h0010 had the right diagnosis (4 failures — `asana004/005`, `intercom001/003` — are the
wrong-grain-spine bug) but failed as an intervention: a **prose** Implementation rule
("build FROM the entity table as the spine, LEFT JOIN children") was behaviorally inert.
The deep-dive showed the solver discussed the spine and even built a `conversation_history`
spine CTE for intercom001, yet the committed SQL still drove the grain off the child table
(intercom001 wired the join backwards; asana004 was byte-identical to `@baseline`).
Meanwhile h0009's lone flip (asana002) came from the solver **copying a concrete local
artifact** (a column-type contract). The lesson: *copyable lands; described does not.*

**Falsifiable claim (the single README change — Implementation stage only):** the failure
mode is that prose structural rules don't reach the committed SQL. Replacing the *prose*
grain-spine guidance with a **concrete worked-example SQL skeleton** the solver can
pattern-match — a generic before/after using placeholder names, e.g.:

```
-- WRONG (drops entities with no children):
--   select entity_id, count(*) ... from <child> group by entity_id
-- RIGHT (one row per entity, 0/NULL where no children):
--   with agg as (select <fk> as entity_id, count(*) ... from <child> group by 1)
--   select e.<id> as entity_id, coalesce(agg.cnt, 0) ...
--   from <entity> e left join agg on agg.entity_id = e.<id>
```

— and instructing the solver to mirror this skeleton (entity table as the FROM driver,
aggregate LEFT JOINed) for any "one row per `<entity>`" model — will flip the grain-spine
failures (asana004/005, intercom001/003) where the prose form (h0010) did not, raising
`stratified_pass_at_1` above `@baseline`. **If even the concrete skeleton is inert, README
prose/examples have a hard ceiling at this model/effort** — a decisive negative either way.

The skeleton is **generic** (placeholder table/column names, a SQL pattern) — it is NOT the
solution for any specific task, so the leak-guard is intact (no ground-truth output, no
hidden-test reference, no public fetch/oracle). Method/README change only; forks the
then-current `@baseline` solver, runtime codex, gpt-5.5. One idea, one stage (Implementation).

Target datasets (smoke, all `ade-bench-` prefixed): the same 4 grain-spine failures h0010
could not move — `ade-bench-asana004`, `ade-bench-asana005`, `ade-bench-intercom001`,
`ade-bench-intercom003` — plus a stable-`@baseline`-pass regression sentinel
`ade-bench-asana001`. (Direct head-to-head vs h0010's null result on the same targets.)

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0016-implementation-grain-spine-worked-example.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs the `@baseline` solver
touches only `## Stage: Implementation` (the worked-example skeleton), leaves the other
stages + dependency/package guardrails untouched, and the skeleton is GENERIC (placeholder
names — no task-specific solution, no `AUTO_*`/verifier reference, leak-guard intact).
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean,
`captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
plus the absolute `stratified_pass_at_1` vs `@baseline`.**

**Smoke gate:** must not regress the `asana001` sentinel and should flip at least one of the
4 grain-spine targets h0010 left at 0/4; the post-smoke deep-dive must confirm (artifact
check) whether the committed SQL now drives the grain off the entity table — answering
whether a concrete example lands where prose did not.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
