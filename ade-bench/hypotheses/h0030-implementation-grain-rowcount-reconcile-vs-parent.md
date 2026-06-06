---
id: h0030
title: Implementation — grain aggregate/entity models on the canonical PARENT source and reconcile the output row count against an INDEPENDENT COUNT(DISTINCT key) on that parent; a shortfall proves you grained on a filtered child — rebuild from the parent
status: hypothesis
kind: hypothesis
source: verification-without-oracle synthesis (_artifacts/verification-without-oracle.md) — grain-drop (#1a entity, #1b date-spine) is a metamorphic/completeness bug: the output must contain one row per key in the canonical parent, so an INDEPENDENT row-count reconcile (the f1007-hard mechanism, the only check that ever caught a false-green) detects the drop without the oracle. Prior grain attempts h0010 (construct-prose, REJ 0/4), h0016 (worked-example, REJ 0/4), h0017 (Output-Contract grain clause, REJ — reached SQL but built backwards) were all CONSTRUCT-only and inert at gpt-5.5/xhigh; none carried an independent reconcile NUMBER. The taxonomy flags "a mechanical [number] lever" as the only grain shot untried before conceding. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-06T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Grain-drop failures (`asana004/005/005-hard` `Got 3`; `intercom001/002/003` `Got 7`;
`airbnb009` date-spine `Got 1`) all share one shape: the solver builds an aggregate/entity model
FROM a pre-filtered child/intermediate (only keys that have a child row), so parent keys with no
children silently vanish — and its self-check, run against its own derivation, confirms the
short table is "correct." This is the [[ade-bench-solver-blind-to-oracle]] wall, but with an
escape the verification-without-oracle synthesis names: the deciding fact ("every parent key must
appear") is a **completeness invariant** that can be checked **independently** by recomputing the
expected row count straight from the raw parent source — exactly the f1007-hard move (the only
self-check that ever caught a real false-green, because it compared an INDEPENDENT number).

Why this is not h0010/h0016/h0017 re-filed: those instructed the solver to *restructure* the SQL
("make the entity the spine", "build one row per entity") as prose or a copyable skeleton, and at
gpt-5.5/xhigh that is behaviorally **inert** — the solver discusses it and the committed SQL is
unchanged (`Got N` byte-identical). The one durable win on this benchmark (asana002) was a
concrete mechanical NUMBER the solver had to match (`::timestamp`), not a rewrite it had to reason
into. This hypothesis adds the missing ingredient: a **mechanical independent row-count number**
plus a hard "if short, rebuild" rule. The reconcile is the forcing function the construct-only
levers lacked.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation instruction — *when you author an aggregate or per-entity model, grain it on its
canonical PARENT source (the relation that defines the full key set), LEFT JOINing the
child/aggregate relations onto it (never the reverse). Then reconcile: compute
`COUNT(DISTINCT <key>)` directly on that raw parent source, and compare it to your model's
`COUNT(*)`. If your model has FEWER rows, you grained on a filtered child and dropped keys —
rebuild FROM the parent and re-reconcile until the counts agree. For a date/calendar grain, the
parent is the complete date spine between the source min and max date. This row count is an
INDEPENDENT number derived from raw source — do NOT "reconcile" by re-running your own model* —
shipped with a concrete worked-example skeleton (`from <parent> left join (<child agg>) using(key)`
plus the `COUNT(DISTINCT key)` reconcile probe) — will catch the grain-drop false-greens
(intercom001/002/003, asana004/005/005-hard, airbnb009) and let the solver fix them, raising
`stratified_pass_at_1` above the `@baseline` 0.6458.

Honest caveat (carried from the Plan-Reviewer real-data sim, WORKFLOW-REFINE 2026-06-06):
`asana004` is partly **underdetermined** — a 13-row intermediate + downstream coalesce is also a
valid refactor. This rule resolves that ambiguity *by prescription* (grain the named `_agg`
entity model on its parent → 16 rows), which matches the oracle's convention; if the solver
honors the prescription the count reconcile flips it, but if it treats the prescription as
optional this task may stay at the wall. intercom + airbnb009 carry no such ambiguity (the parent
count is unambiguously the target) and are the cleaner test of the mechanism.

Method/README change only. Forks `solver_workflows/codex-ade-dbt-minimal` (runtime codex); no
dataset/harness/runtime change. Leak-guard intact (raw local source tables only; no public fetch,
no oracle, no hidden `AUTO_*`/`solution__*` reference).

## Target datasets

Primary smoke targets (grain cluster, all `ade-bench-` prefixed):

- `ade-bench-intercom001` — `AUTO_intercom__threads_equality` `Got 7` (clean child-driven drop, no ambiguity).
- `ade-bench-airbnb009` — `mom_agg_review_date_range` `Got 1` (date-spine; complete-calendar grain).
- `ade-bench-asana004` — `AUTO_int_asana__project_user_agg_equality` `Got 3` (prescription test; see caveat).

This rule fires on every aggregate/entity model (generative) → G8 cross-family canary panel (one
`@baseline` passer per non-target family): `ade-bench-asana001`, `ade-bench-quickbooks002`,
`ade-bench-f1001` (the convention-bleed tripwire), `ade-bench-ana-eng001`, `ade-bench-airbnb001`.
No intercom canary possible (no intercom @baseline passer) — but intercom001 is a target here.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
README diff touches only `## Stage: Implementation` (the single grain + row-count-reconcile rule);
other stages and the dependency/package/leak-guard prose untouched; no hidden-test tokens.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — G6 independence + G7 actionability.** The reconcile compares against an INDEPENDENT
`COUNT(DISTINCT key)` on the raw parent (external signal), with an explicit ban on re-running the
solver's own model — not the dead self-verification family. Ships a worked-example
`from parent left join child` + `COUNT(DISTINCT)` skeleton (mechanical number), mitigating the
inert-risk that sank h0010/h0016/h0017.

**AC-3 — Every recorded score is paired with a clean strict audit** (`tainted: 0`, `captured > 0`).

**Smoke gate:** flip ≥1 grain target — and the inert-detector is decisive here: if a target's
`Got N` is byte-unchanged vs @baseline, the lever was inert (the h0010/h0016/h0017 failure mode);
this hypothesis is only interesting if the reconcile number actually moves the committed SQL.
**Zero** canary regressions or it is NO-GO.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Gatekeeper review

## Stage Report: propose
