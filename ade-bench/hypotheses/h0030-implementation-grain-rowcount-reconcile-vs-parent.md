---
id: h0030
title: Implementation — grain aggregate/entity models on the canonical PARENT source and reconcile the output row count against an INDEPENDENT COUNT(DISTINCT key) on that parent; a shortfall proves you grained on a filtered child — rebuild from the parent
status: propose
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

**Recommendation: APPROVE** — clean single-stage Implementation addition; G10 cleared on all three axes (gated scope, raw-parent independence, check-don't-replace) — the direct, verified fix to the h0012 mandate-replace failure; G8 panel carries ≥2 perturbable canaries on both construct-sharing families; no FAILs.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T04:44:37Z.

Parent resolved: `@baseline` = `runs/ade-bench-baseline/622bdedac572b479`, `solver_workflow: solver_workflows/codex-ade-dbt-minimal` — matches the hypothesis `source:`; parent-dependent rules (G1/G6) diffed against it.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is a single pure addition `63a64,110` (no `<` lines). Insertion sits at the tail of `## Stage: Implementation` (parent line 50–63), immediately before `## Stage: Validation` (parent line 64). One stage, one idea (grain row-count reconcile). No other stage, no leak-guard/dependency prose touched. |
| G2 leak-guard intact | PASS | Pure addition — leak-guard/dependency paragraphs byte-identical to parent. Grep over added lines for `AUTO_*`/`solution__*`/`check_option_*`/`verifier`/`equality test`/`expected output seed`/`drive…to zero`/`curl`/`wget`/`git clone`/`download`/`published-solution` = NONE_FOUND. Added text scopes the reconcile to `{{ source(...) }}` raw local tables only. |
| G3 spec two fields | PASS | `diff baseline.yaml h0030.yaml` = only line 2 (`experiment:`) and line 11 (`solver_workflow:`). No third field. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` all preserved. |
| G4 smoke tasks-only | WARN | `diff full smoke` = only an added `benchmark.tasks` block (10 `ade-bench-`-prefixed slugs); nothing else differs. All three named Primary smoke targets (intercom001/airbnb009/asana004) present. WARN: the `## Hypothesis` falsifiable claim's parenthetical also names asana005/005-hard and intercom002/003 as expected catches, but `## Target datasets` formally designates only the three as smoke targets and they are all in the spec — a deliberate reduced target set, not a missing target. Also a sentinel-regression note for the G4 WARN below. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1749B) and `…smoke.frozen.yaml` (1982B) exist (Jun 7 04:40). Both carry `kind: spacedock_solver` + `runtime: codex`; full frozen `sealed_hash 4fc450dc…`, `solver_workflow_content_hash sha256:9e8f75e3…`. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim verbatim in spirit: Implementation stage, reconcile model `COUNT(*)` against `COUNT(DISTINCT key)` on the **raw parent source** (a named INDEPENDENT local signal — a different relation, not a self-re-run), explicit "do NOT re-run/re-derive/wrap your own model." Generative-but-independent, NOT the dead self-anchored h0006/h0007/h0008 family. No scope creep beyond the single grain rule. |
| G7 actionability/inert-risk | PASS | Carries a worked-example skeleton (the G7 mechanical-number form): a `text` count-reconcile recipe (`produced=13` vs `expected=count(distinct project_id)…=16`) plus a literal BEFORE/AFTER `sql` block (`from {{ source('app','projects') }} p left join (<child agg>) c using(project_id)`). This is copyable, not abstract structural prose — the ingredient h0010/h0016/h0017 lacked. Inert-risk noted but mitigated by the worked example; the empirical caution stands (this @baseline talks-but-doesn't-do on restructures) and the smoke inert-detector should be the decisive read. |
| G8 regression-canary coverage | PASS | Generative-class (fires on every aggregate/entity model meant to be complete over a parent key set ≈ most aggregates). Smoke panel: f1001/f1005 (f1, the h0012-fragile figure-rewrite family — f1005 a direct h0012 casualty), ana-eng001/ana-eng002 (ana-eng, aggregate-heavy) = ≥2 perturbable canaries on each construct-sharing family; plus airbnb001/asana001/quickbooks002 one-per-family. All 7 confirmed `@baseline` reward=1.0 passers (from 622bdedac572b479 per_trial_outcomes). intercom legitimately supplies no canary (intercom001/002/003 all reward=0.0). |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — single generative Implementation instruction, no N-candidate scoring. |
| G10 self-correcting false-positive | PASS | Self-correcting (reconcile-and-fix-on-shortfall) — direct successor to REJECTED h0012. **(a) scope:** GATED to models "whose grain is meant to be COMPLETE over a parent key set … as described by its `schema.yml` entry or the task instruction"; legitimately-filtered aggregates explicit-exempt and "do not invent a parent" — NOT generative-on-every-aggregate. **(b) independence source:** reconciles against `COUNT(DISTINCT <key>)` on the raw PARENT via "a plain SELECT on the source relation, with NO model logic; do NOT re-run, re-derive, or wrap your own model" — separately-sourced, not a re-derived CTE (the axis h0012 already got right, preserved; cannot re-correlate into a false-green). **(c) check-don't-replace:** a shortfall is "a SIGNAL TO INVESTIGATE, NOT an automatic rewrite" — re-read intended grain, rebuild only if completeness is intended (case i), leave-it if legitimately scoped (case ii), and "NEVER replace a simple, correct aggregate with a structurally-different path merely to change the number" — the direct softening of the h0012 mandate-replace that lost −4. |

**For the captain:** No blockers — APPROVE to `smoke`. Two things to eyeball: (1) G4 WARN — the smoke runs only 3 of the ~6 grain-drop targets the claim names (asana005/005-hard, intercom002/003 omitted); fine as a reduced target set, but if you want a stronger flip signal, asana005/005-hard would not add a new family. There is **no stable-`@baseline`-pass regression sentinel among the three smoke targets** (all are failers by design) — the regression sentinels are the 7 canaries, which is the intended split. (2) G7/inert-risk is the real go/no-go: this @baseline has rejected three prior grain levers as talks-but-doesn't-do; lean on the smoke inert-detector (`Got N` byte-unchanged vs @baseline ⇒ inert NO-GO) and require artifact-proven parent-grained SQL in the commit before banking any flip (h0012's f1006 flipped at smoke and reverted at full).

## Stage Report: propose

- DONE: Forked solver README adds EXACTLY the G10-gated grain row-count reconcile as ONE Implementation-stage instruction (with the from-parent-left-join + COUNT(DISTINCT) worked-example skeleton); a shortfall INVESTIGATES, never auto-replaces a simple-correct aggregate; leak-guard / dependency prose byte-identical to the codex-ade-dbt-minimal parent.
  `diff parent vs fork` = a single pure addition (63a64-110): the reconcile paragraph + a `text` count-skeleton + a `sql` BEFORE/AFTER (`from parent left join (child agg) using(key)`). All other stages, leak-guard, and package/dependency prose unchanged. Fork: `solver_workflows/h0030-implementation-grain-rowcount-reconcile-vs-parent/README.md`.
- DONE: Full spec differs from baseline.yaml ONLY in experiment + solver_workflow; smoke spec adds benchmark.tasks with the 10 tasks named in the body.
  `diff baseline.yaml h0030...yaml` = only lines 2 (experiment) + 11 (solver_workflow). `diff full smoke` = only the added `benchmark.tasks` (10 tasks: targets intercom001/airbnb009/asana004 + canaries f1001/f1005/ana-eng001/ana-eng002/airbnb001/asana001/quickbooks002). No intercom canary (no @baseline passer; intercom001 is a target).
- DONE: Both specs frozen via rk freeze --allow-missing; agent.kind=spacedock_solver and runtime=codex preserved in both.
  `specs/h0030-...frozen.yaml` (sealed_hash 4fc450dc..., solver_workflow_content_hash sha256:9e8f75e3...) + `...smoke.frozen.yaml` (10 tasks present); both show `kind: spacedock_solver` / `runtime: codex`.
- SKIPPED: Run the gatekeeper (Output 5).
  Per dispatch: the FO dispatches an INDEPENDENT gatekeeper review after this ensign completes; ensign does NOT self-run it.

### Summary

Forked the @baseline solver (codex-ade-dbt-minimal) into h0030 and added exactly one Implementation-stage instruction: when a model's grain is meant to be complete over a parent key set, reconcile its COUNT(*) against an INDEPENDENT COUNT(DISTINCT key) on the raw parent source (plain SELECT, no model logic), and on a shortfall INVESTIGATE the intended grain — rebuild FROM the parent only if completeness is intended, never swap a simple-correct aggregate for a different path just to move the number (G10 check-don't-replace). Carries a from-parent-left-join + COUNT(DISTINCT) worked-example skeleton (the G7 mechanical-number ingredient h0010/h0016/h0017 lacked). Full spec differs from baseline only in experiment+solver_workflow; smoke spec adds 10 tasks (3 grain targets + a G8 panel with G8/G10 perturbable doubling on f1 and ana-eng). Both specs frozen with kind/runtime preserved. Note: the dispatch fetch command `claude-team show-stage-def` is not on PATH (exit 127) — recovered the propose stage definition directly from `hypotheses/README.md` and mirrored sibling h0029's structure; flagging the broken fetch command to the FO.
