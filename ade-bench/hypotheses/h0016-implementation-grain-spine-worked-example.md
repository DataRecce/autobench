---
id: h0016
title: Implementation — grain-spine fix as a CONCRETE worked-example SQL skeleton (not a prose rule), to test whether copyable beats described
status: smoke
kind: hypothesis
source: forked from h0010's failure. h0010 stated the grain-spine fix as a PROSE Implementation rule and it was behaviorally inert (0/4 — solver discussed the spine, even built the CTE for intercom001, but never made the entity the FROM spine in the committed SQL). h0009's only win (asana002) came from copying a CONCRETE local artifact. This re-attempts the SAME grain-spine fix but in concrete, copyable, worked-example form (a generic before/after SQL skeleton with placeholder names) — the decisive test of whether a structural fix can land when made copyable rather than described. Forks the then-current @baseline (re-fork at propose).
started: 2026-06-05T02:33:17Z
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
Because the worked-example fires on **any** "one row per `<entity>`" model (it is a
**generative** instruction, not gated to the targets), the smoke set also carries a G8
regression-canary panel — one currently-passing `@baseline` task from each NON-target family:
`ade-bench-airbnb001`, `ade-bench-ana-eng008`, `ade-bench-f1001`, `ade-bench-quickbooks004`
(`f1001` + `quickbooks004` specifically guard against the convention-bleed that lost h0009
−3 at full scale). A canary dropping FAIL is a NO-GO regardless of how many targets flip.

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

## Gatekeeper review

**Recommendation: APPROVE** — single Implementation-stage addition of the exact
worked-example SQL skeleton the claim names; leak-guard byte-identical; full spec diffs
in only `experiment:`+`solver_workflow:`; generative instruction carries the full G8
canary panel.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-04). Reviewed 2026-06-05.

Fork parent resolved: `source:` = forked from then-current `@baseline`; `rk registry resolve
run @baseline` = `runs/ade-bench-baseline/622bdedac572b479` whose `solver_workflow` =
`./solver_workflows/codex-ade-dbt-minimal`. Agree → `<parent-solver>` = `solver_workflows/codex-ade-dbt-minimal`.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff parent fork` = one hunk `55a56,74`, a pure addition inside `## Stage: Implementation` (between "schema patterns." and "Run basic confirmation"); 0 `## Stage:` headers in diff; exactly the worked-example skeleton the claim names, no other stage/guardrail touched. |
| G2 leak-guard intact | PASS | leak-guard lines 9-31 byte-identical parent↔fork; grep of added (`^>`) lines for `AUTO_/solution__/check_option/verifier/equality test/expected output/curl/wget/git clone/ls-remote` = none. Added text is generic placeholders (`<entity>/<child>/<fk>/<id>/cnt`) — no ground-truth, no hidden-test ref. |
| G3 spec two fields | PASS | `diff baseline.yaml h0016….yaml` = only L2 `experiment:` and L11 `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0016….yaml …smoke.yaml` = only an added `benchmark.tasks:` block; all 9 slugs `ade-bench-` prefixed; all 4 named targets (asana004/005, intercom001/003) present; asana001 stable-pass sentinel present. |
| G5 both frozen | PASS | `…frozen.yaml` (1733B) + `…smoke.frozen.yaml` (1946B) both exist; both carry `kind: spacedock_solver` + `runtime: codex`; smoke frozen carries all 9 task slugs. |
| G6 resolver fidelity | PASS | Inserted skeleton matches the claim's quoted WRONG/RIGHT block verbatim; generative-CONSTRUCTIVE ("make the entity the FROM driver and LEFT JOIN the aggregate") — tells the solver how to build, not a self-anchored "re-run/verify your own output" check. Not in the dead h0006/07/08 family. |
| G7 actionability/inert-risk | PASS | Worked-example / few-shot form (literal before→after SQL skeleton to pattern-match) — this IS the cure G7 recommends for h0010's inert abstract-structural prose. No WARN. |
| G8 regression-canary coverage | PASS | Generative (fires on ANY "one row per entity" model, not gated). Smoke canary panel present: airbnb001, ana-eng008, f1001, quickbooks004 — verified @baseline passers (reward=1.0 each in `622bdedac572b479/per_trial_outcomes.json`), one per non-target family (airbnb/ana-eng/f1/quickbooks). |

**For the captain:** Clean APPROVE — no FAILs, no WARNs. This is the deliberate worked-example
re-test of h0010's inert prose grain-spine rule; G7 is satisfied (not flagged) precisely because
the fix is now copyable. G8 panel is complete with f1/quickbooks canaries guarding the
convention-bleed that lost h0009 −3 at full scale. Advance to `smoke`.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: Fork the @baseline solver (codex-ade-dbt-minimal) and edit ONLY ## Stage: Implementation: add the grain-spine fix as a CONCRETE worked-example SQL skeleton
  `cp -r` → `solver_workflows/h0016-implementation-grain-spine-worked-example/`; diff vs parent = single addition `55a56,74` inside Implementation only (generic WRONG/RIGHT skeleton, placeholder names `<entity>/<child>/<fk>/<id>/cnt`, entity-as-FROM-spine + LEFT JOIN agg with 0/NULL); leak-guard bytes-identical, 0 other stages/guardrails touched.
- DONE: FULL spec diffs baseline ONLY in experiment: + solver_workflow:. SMOKE spec benchmark.tasks = 4 targets + sentinel + G8 canary panel; kind/runtime preserved; Freeze both.
  Full diff = only L2 experiment + L11 solver_workflow; smoke adds only benchmark.tasks (asana004/005, intercom001/003, asana001 sentinel, + airbnb001/ana-eng008/f1001/quickbooks004 canaries); both frozen (commit 2e… ; `…frozen.yaml` + `…smoke.frozen.yaml` carry spacedock_solver/codex).
- DONE: Run the propose gatekeeper applying G1-G8; record APPROVE/REVISE/REJECT; confirm G8 PASSES; paste two-field spec diff + README diff into gate evidence.
  Gatekeeper review block appended: all 8 rules PASS, overall APPROVE; G8 PASS (generative + 4 non-target @baseline-passer canaries verified reward=1.0). Spec diffs + README diff hunk cited inline in evidence.

### Summary

Forked the @baseline solver and replaced h0010's behaviorally-inert PROSE grain-spine rule with the CONCRETE worked-example SQL skeleton (generic before/after with placeholder names) quoted in the falsifiable claim — the decisive copyable-vs-described re-test, Implementation stage only. Full spec differs from baseline only in the two allowed fields; smoke spec carries the 4 grain-spine targets + asana001 sentinel + the mandatory G8 regression-canary panel (this is a generative instruction firing on any "one row per entity" model, with f1001/quickbooks004 specifically guarding the convention-bleed that sank h0009). Both specs frozen; the gatekeeper returned a clean APPROVE (no FAILs, no WARNs).
