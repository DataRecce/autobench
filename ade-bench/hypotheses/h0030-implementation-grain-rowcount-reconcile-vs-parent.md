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
Implementation instruction — *when you author an aggregate or per-entity model whose grain is
meant to be COMPLETE over a parent key set — a per-entity or dimension model that should expose one
row per entity, or a date/calendar model that should be gap-free, as described by its `schema.yml`
entry or the task instruction — reconcile its grain against an independent count from the raw
parent. Compute `COUNT(DISTINCT <key>)` directly on the canonical raw PARENT source (a plain
SELECT on the source relation, with NO model logic — do NOT re-run or re-derive your own model),
and compare it to your model's `COUNT(*)`. A shortfall is a **SIGNAL TO INVESTIGATE, not an
automatic rewrite**: re-read the model's intended grain, then — (i) if it is meant to carry every
parent key and some are missing, you grained on a filtered child; rebuild FROM the parent (LEFT
JOIN the child/aggregate relations onto it) and re-reconcile; (ii) if the model is legitimately
scoped to a subset, the shortfall is EXPECTED — leave it. Never replace a simple, correct
aggregate with a structurally-different path merely to change the number. For a date grain the
parent is the complete date spine between the source min and max date. This rule does not apply to
aggregates with no canonical parent key set* — shipped with a concrete worked-example skeleton
(`from <parent> left join (<child agg>) using(key)` plus the `COUNT(DISTINCT key)` reconcile probe)
— will catch the grain-drop false-greens (intercom001/002/003, asana004/005/005-hard, airbnb009)
and let the solver fix them, raising `stratified_pass_at_1` above the `@baseline` 0.6458.

**G10 compliance (self-correcting-lever gating, from the h0012 −4 lesson).** h0012 lost net −4
because a generative reconcile *mandated replacing* a simple-correct `sum→max` aggregate with a
"structurally different" (and wrong) path, then false-greened against a CTE re-deriving that same
path. This lever is the same family (reconcile-and-fix), so it is built to clear G10's three axes:
**(a) scope** — **gated** to models whose grain is *meant* to be complete over a parent key set
(per `schema.yml`/instruction), not run on every aggregate; a legitimately-filtered aggregate is
exempt, so the rule does not fire on the passers it should leave alone. **(b) independence source**
— the reconcile compares against `COUNT(DISTINCT key)` on the **raw parent source** (a plain
SELECT, no model logic), explicitly **not** the solver's own re-run or a re-derived CTE — so it
cannot re-correlate into a false-green (this was already the design and is the axis h0012 got
right). **(c) check-don't-replace** — a shortfall **triggers investigation**, not an automatic
rebuild: the solver re-reads the intended grain and only rebuilds when completeness is genuinely
intended, and is explicitly forbidden from swapping a simple-correct aggregate for a different
path just to move the count. This is precisely the softening from "rebuild until counts agree"
(the h0012 mistake) to "investigate, then rebuild only if the spec calls for completeness."

Honest caveat (carried from the Plan-Reviewer real-data sim, WORKFLOW-REFINE 2026-06-06), now
sharpened by the G10 check-don't-replace gate: `asana004` is partly **underdetermined** — a 13-row
intermediate + downstream coalesce is also a valid refactor. The pre-G10 draft resolved this *by
prescription* (always grain the `_agg` model on its parent → 16 rows). The G10(c) softening trades
some of that power for safety: the reconcile now only *flags* the shortfall and asks the solver to
**re-read the `_agg` model's intended grain** — it flips asana004 only if the solver reads that
grain as one-row-per-project (16), and leaves it untouched if the solver judges the 13-row scope
legitimate. So asana004 becomes **more dependent on the solver correctly reading the schema.yml
grain** than the prescriptive draft was — an accepted cost of not breaking passers. intercom +
airbnb009 carry no such ambiguity (the parent count is unambiguously the target, and the grain is
clearly meant to be complete) and are the cleaner test of the mechanism.

Method/README change only. Forks `solver_workflows/codex-ade-dbt-minimal` (runtime codex); no
dataset/harness/runtime change. Leak-guard intact (raw local source tables only; no public fetch,
no oracle, no hidden `AUTO_*`/`solution__*` reference).

## Target datasets

Primary smoke targets (grain cluster, all `ade-bench-` prefixed):

- `ade-bench-intercom001` — `AUTO_intercom__threads_equality` `Got 7` (clean child-driven drop, no ambiguity).
- `ade-bench-airbnb009` — `mom_agg_review_date_range` `Got 1` (date-spine; complete-calendar grain).
- `ade-bench-asana004` — `AUTO_int_asana__project_user_agg_equality` `Got 3` (prescription test; see caveat).

Scope classification (G10(a)): **gated** to aggregate/entity models whose grain is meant to be
complete over a parent key set — but that covers most aggregate models, so for G8 carry a full
panel and **double the families whose aggregates a grain/count reconcile is most likely to
perturb**. h0012 proved **f1** is the fragile family for a figure-rewrite lever (it broke four f1
`constructor_points` passers); **ana-eng** is aggregate/obt-heavy. Those two each carry ≥2
**perturbable** canaries (passers with aggregate models the count-reconcile can fire on), per G8:

- **f1 (proven-fragile to figure-rewrite, ≥2 perturbable):** `ade-bench-f1001` (the
  convention-bleed tripwire), `ade-bench-f1005` (a direct h0012 casualty — if a grain/count lever
  survives f1005 it is a meaningful safety signal).
- **ana-eng (aggregate-heavy, ≥2 perturbable):** `ade-bench-ana-eng001`, `ade-bench-ana-eng002`.
- **One `@baseline` passer per other non-target family:** `ade-bench-airbnb001`,
  `ade-bench-asana001`, `ade-bench-quickbooks002`. No intercom canary possible (no intercom
  `@baseline` passer) — but intercom001 is a target here.

(All seven canaries are confirmed `@baseline` passers from the 31/48 outcomes.)

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
README diff touches only `## Stage: Implementation` (the single grain + row-count-reconcile rule);
other stages and the dependency/package/leak-guard prose untouched; no hidden-test tokens.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — G6 independence + G10 self-correcting-lever gating + G7 actionability.** The reconcile
compares against an INDEPENDENT `COUNT(DISTINCT key)` on the raw parent (external signal), with an
explicit ban on re-running the solver's own model — not the dead self-verification family (G6). It
satisfies **G10** on all three axes: **(a)** gated to models meant to be complete over a parent key
set (legitimately-filtered aggregates exempt — does not fire on the passers it should leave alone);
**(b)** reconcile target is the raw parent `COUNT(DISTINCT)`, a separately-sourced signal, never a
re-derived CTE (the axis h0012 got right, preserved); **(c)** a shortfall triggers *investigation*,
not an automatic rebuild — the explicit ban on replacing a simple-correct aggregate with a
different path is the direct fix for the h0012 mandate-replace failure. **G7:** ships a
worked-example `from parent left join child` + `COUNT(DISTINCT)` skeleton (mechanical number),
mitigating the inert-risk that sank h0010/h0016/h0017.

**AC-3 — Every recorded score is paired with a clean strict audit** (`tainted: 0`, `captured > 0`).

**Smoke gate:** flip ≥1 grain target — and the inert-detector is decisive here: if a target's
`Got N` is byte-unchanged vs @baseline, the lever was inert (the h0010/h0016/h0017 failure mode);
this hypothesis is only interesting if the reconcile number actually moves the committed SQL.
**Zero** canary regressions across the full panel, and specifically zero on the **≥2 perturbable
canaries per fragile family** (f1001/f1005, ana-eng001/002) — a generative grain rule can break a
*different* member than a single canary, which is exactly how h0012 lost −4 past a clean smoke
(G8). A canary dropping FAIL is NO-GO regardless of target movement. Variance caution: a lone flip
with no artifact-proof (the parent-grained SQL visible in the commit) may be noise — bank a GO on
artifact-proven flips, not a single reward change (h0012's f1006 flipped at smoke and reverted at
full).

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Gatekeeper review

## Stage Report: propose
