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

**Scope (E1, revised 2026-06-07).** This hypothesis now targets the **intercom grain cluster
ONLY** — `intercom001/002/003` (`Got 7`), one clean shared child-driven grain-drop cause. Two
former targets were removed to their correct experiments: **`airbnb009` → E2/h0019** (its date
spine is already built unprompted; the residual is a cross-join, NOT a missing spine, so the
reconcile is the wrong lever there) and **`asana004` → Track Z** (oracle-only `int_` convention,
not in the flip portfolio — see `_proposal/oracle-problem-systematic-program.md` §4/§5). E1 is the
program's make-or-break bet: run-first-CAPPED — one smoke; if `intercom Got 7` does not drop below
5 (h0016 already reached `7→5`; ≥5 is the inert wall that held h0010/h0016/h0017), it is the inert
NO-GO and we do NOT iterate.

Grain-drop failures (`intercom001/002/003` `Got 7` — and, in the broader cluster the lever's
*rule* still covers, `asana004/005/005-hard` `Got 3`, `airbnb009` date-spine `Got 1`) all share one
shape: the solver builds an aggregate/entity model FROM a pre-filtered child/intermediate (only
keys that have a child row), so parent keys with no children silently vanish — and its self-check,
run against its own derivation, confirms the short table is "correct." This is the
[[ade-bench-solver-blind-to-oracle]] wall, but with an escape the verification-without-oracle
synthesis names: the deciding fact ("every parent key must appear") is a **completeness invariant**
that can be checked **independently** against the raw parent source by two complementary probes —
(a) recomputing the expected row count via `COUNT(DISTINCT key)` (exactly the f1007-hard move, the
only self-check that ever caught a real false-green, because it compared an INDEPENDENT number) AND
(b) an **anti-join** that asserts every DISTINCT raw-parent key actually appears in the output.

**Why both probes, not just the count (E0/h0032 finding).** E0's controlled 2×2 harness
(`_artifacts/h0032-e0-harness/result_2x2.json`) proved a bare `COUNT(*)` vs `COUNT(DISTINCT key)`
reconcile is **blind to drop-N-add-N**: drop 7 real parent rows and admit 7 wrong rows and the two
counts still match while the grain is wrong (`count_blind_spot`: `count_reconcile_fires=false`,
`completeness_check_fires=true`). The `ref_graph_existence_completeness` anti-join (every raw-source
key must appear in the output) CLEARED E0 two-sided (fires on the injected 47-key drop, silent on
the known-good) and catches exactly that case. So the Implementation rule now PAIRS the count with
the anti-join. E0 also confirmed the **raw-source binding is load-bearing**: the `correlated_error_trap`
showed a reconcile that reads a solver-rebuilt intermediate re-introduces the correlated error and
false-greens; only a plain SELECT on the immutable `{{ source() }}` parent stays independent —
preserved verbatim in the rule.

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
entry or the task instruction — reconcile its grain against an independent view of the raw parent
via TWO complementary probes, both a plain SELECT on the raw source (NO model logic — do NOT re-run
or re-derive your own model): (1) a **count reconcile** — `COUNT(DISTINCT <key>)` on the canonical
raw PARENT source vs your model's `COUNT(*)`; and (2) a **completeness anti-join** — every DISTINCT
raw-parent key must appear in your output (the missing-key set must be empty), because the count
alone is blind to a drop-N-add-N error. A shortfall in the count OR any missing key is a **SIGNAL
TO INVESTIGATE, not an automatic rewrite**: re-read the model's intended grain, then — (i) if it is
meant to carry every parent key and some are missing, you grained on a filtered child; rebuild FROM
the parent (LEFT JOIN the child/aggregate relations onto it) and re-reconcile both probes; (ii) if
the model is legitimately scoped to a subset, the shortfall is EXPECTED — leave it. Never replace a
simple, correct aggregate with a structurally-different path merely to change the number. For a
date grain the parent is the complete date spine between the source min and max date. This rule
does not apply to aggregates with no canonical parent key set* — shipped with a concrete
worked-example skeleton (`from <parent> left join (<child agg>) using(key)` plus the `COUNT(DISTINCT
key)` reconcile probe AND the `raw keys EXCEPT output` anti-join probe) — will catch the grain-drop
false-greens (the E1 smoke targets **intercom001/002/003**) and let the solver fix them, raising
`stratified_pass_at_1` above the `@baseline` 0.6458.

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
resolved by the E1 triage: `asana004` is partly **underdetermined** — a 13-row intermediate +
downstream coalesce is also a valid refactor — and sits on the oracle-only `int_` convention. That
is precisely why it has been **routed out of h0030 to Track Z** (enforced abstention) rather than
flipped by prescription. The intercom cluster carries no such ambiguity: the parent count is
unambiguously the target, the grain is clearly meant to be complete, and all three intercom tasks
share one mechanism — so intercom is the clean, decisive test of whether a mechanical raw-source
reconcile (now count + anti-join) breaks the construct-inertness wall. This is a bimodal {0, 3}
bet: 3 shots at one shared cause; if it stays inert (`Got 7→7`, the h0010/h0016/h0017 prior), 0.

Method/README change only. Forks `solver_workflows/codex-ade-dbt-minimal` (runtime codex); no
dataset/harness/runtime change. Leak-guard intact (raw local source tables only; no public fetch,
no oracle, no hidden `AUTO_*`/`solution__*` reference).

## Target datasets

Primary smoke targets = **E1 = the intercom grain cluster ONLY** (all `ade-bench-` prefixed, all
FAIL `@baseline`, one clean shared child-driven grain-drop cause — 3 shots at the same mechanism):

- `ade-bench-intercom001` — `AUTO_intercom__threads_equality` `Got 7` (clean child-driven drop, no ambiguity).
- `ade-bench-intercom002` — same shared child-driven grain-drop cause `Got 7`.
- `ade-bench-intercom003` — same shared child-driven grain-drop cause `Got 7`.

**Removed from h0030 (re-routed 2026-06-07 per E1 triage, `_proposal/oracle-problem-systematic-program.md`):**

- `airbnb009` → **E2/h0019.** Its date spine is already built unprompted (`expected_days=4508`,
  `missing_mom_days=0`); the residual `Got 1` is a single over-produced row from a cross-join, NOT
  a missing spine — so the completeness reconcile is the wrong lever there. The net-new lever is
  h0019's anti-cross-join clause.
- `asana004` → **Track Z.** Oracle-only `int_` convention (`AUTO_int_asana__project_user_agg`,
  taxonomy line 71: "intercom/airbnb009 are the cleaner test"), partly underdetermined; it is on
  the enforced-abstention rail, not in the flip portfolio.

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
README diff touches only `## Stage: Implementation` (the single grain rule — the paired count
reconcile + completeness anti-join against the raw parent); other stages and the
dependency/package/leak-guard prose untouched; no hidden-test tokens. `agent.kind: spacedock_solver`,
`runtime: codex` preserved.

**AC-2 — G6 independence + G10 self-correcting-lever gating + G7 actionability.** The lever runs two
probes against the raw parent: a `COUNT(DISTINCT key)` reconcile AND a completeness anti-join (every
raw-parent key must appear in the output), both a plain SELECT on `{{ source() }}` with an explicit
ban on re-running the solver's own model — not the dead self-verification family (G6). E0/h0032
proved the anti-join is the load-bearing complement: a bare count is blind to drop-N-add-N, the
anti-join CLEARED two-sided on the injected drop. It satisfies **G10** on all three axes: **(a)**
gated to models meant to be complete over a parent key set (legitimately-filtered aggregates exempt
— does not fire on the passers it should leave alone); **(b)** both probes target the raw parent
source, a separately-sourced signal, never a re-derived CTE (the axis h0012 got right, preserved;
E0's `correlated_error_trap` confirmed reading a rebuilt intermediate re-correlates into a
false-green); **(c)** a shortfall or missing key triggers *investigation*, not an automatic rebuild
— the explicit ban on replacing a simple-correct aggregate with a different path is the direct fix
for the h0012 mandate-replace failure. **G7:** ships a worked-example `from parent left join child`
+ `COUNT(DISTINCT)` + `raw keys EXCEPT output` anti-join skeleton (mechanical), mitigating the
inert-risk that sank h0010/h0016/h0017.

**AC-3 — Every recorded score is paired with a clean strict audit** (`tainted: 0`, `captured > 0`).

**Smoke gate (run-first-CAPPED, captain 2026-06-07):** the smoke runs ONCE over the intercom
cluster (intercom001/002/003) + the 7-canary panel. The **decisive leading indicator is distance**:
if `intercom Got 7` does NOT drop **below 5** on any target, the lever is inert (h0016 already
reached `7→5`; ≥5 is the same wall that held h0010/h0016/h0017) — that is the inert NO-GO and we do
**NOT iterate**. A flip (FAIL→PASS) on ≥1 intercom target is the lagging confirmation, but it is
only bankable with **artifact-proof** (the parent-grained SQL — `from {{ source }} left join
(child agg)` plus a non-empty-anti-join fix — visible in the commit); a lone reward change without
that SQL may be variance (h0012's f1006 flipped at smoke and reverted at full). **Zero** canary
regressions across the full panel, and specifically zero on the **≥2 perturbable canaries per
fragile family** (f1001/f1005, ana-eng001/002) — a generative grain rule can break a *different*
member than a single canary, which is exactly how h0012 lost −4 past a clean smoke (G8). A canary
dropping FAIL is NO-GO regardless of target movement.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Gatekeeper review

**Recommendation: APPROVE** — REVISED artifacts (count + completeness anti-join pairing; E1 intercom-only target set) re-reviewed; clean single-stage Implementation addition; G10 cleared on all three axes (gated scope, raw-parent independence on BOTH probes, check-don't-replace); G8 panel carries ≥2 perturbable canaries on both construct-sharing families; the prior G4 WARN is now PASS (smoke targets exactly equal the Target datasets). No FAILs.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T10:34:00Z (revision cycle 2).

Parent resolved: `@baseline` = `runs/ade-bench-baseline/622bdedac572b479`, `solver_workflow: solver_workflows/codex-ade-dbt-minimal` — matches the hypothesis `source:`; parent-dependent rules (G1/G6) diffed against it.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is a single pure addition `63a64,128` (0 `<` lines confirmed). Insertion sits at the tail of `## Stage: Implementation` (parent line 50–63), immediately before `## Stage: Validation`. Still ONE stage, ONE idea — the grain rule is now a paired count-reconcile + completeness anti-join, but both probes are the same single "reconcile grain against the raw parent" idea (the anti-join is the row-level dual of the count, not a second independent instruction). No other stage, no leak-guard/dependency prose touched. |
| G2 leak-guard intact | PASS | Pure addition (0 deletions) — leak-guard/dependency paragraphs byte-identical to parent. Grep over added lines for `AUTO_*`/`solution__*`/`check_option_*`/`verifier`/`equality test`/`expected output seed`/`drive…to zero`/`curl`/`wget`/`git clone`/`download`/`published-solution`/`fetch` = NONE_FOUND. Both probes (count + anti-join) read only `{{ source(...) }}` raw local tables and `{{ ref() }}` of the solver's own model; no hidden grading artifact. |
| G3 spec two fields | PASS | `diff baseline.yaml h0030.yaml` = only line 2 (`experiment:`) and line 11 (`solver_workflow:`). No third field. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` all preserved. |
| G4 smoke tasks-only | PASS | `diff full smoke` = only an added `benchmark.tasks` block (10 `ade-bench-`-prefixed slugs); nothing else differs. The smoke now lists EXACTLY the Target datasets — intercom001/002/003 — plus the 7-canary panel; airbnb009 and asana004 removed (re-routed to E2/h0019 and Track Z, recorded in `## Target datasets`). The prior WARN (claim parenthetical named more targets than the spec) is resolved: the body now scopes E1 to intercom only, so the spec and the named target set agree. No stable-pass sentinel among the targets (all 3 FAIL by design) — the regression sentinels are the 7 canaries, the intended split (sentinel-regression note carried to G8). |
| G5 both frozen | PASS | Both re-frozen Jun 7 10:33. `…frozen.yaml` (1749B) and `…smoke.frozen.yaml` (1987B) exist. Both carry `kind: spacedock_solver` + `runtime: codex`; both `sealed_hash 00483f8e…`, `solver_workflow_content_hash sha256:a49994d6…` (changed from the pre-revision `9e8f75e3…` — confirms the anti-join README edit is captured in the freeze). |
| G6 resolver fidelity | PASS | Inserted text matches the revised Falsifiable claim: Implementation stage, TWO complementary raw-parent probes — (1) model `COUNT(*)` vs `COUNT(DISTINCT key)` on the raw parent, (2) a completeness anti-join (`raw keys EXCEPT output` must be empty) — both a "plain SELECT on the raw source, NO model logic; do NOT re-run, re-derive, or wrap your own model." The anti-join pairing is exactly the E0/h0032 finding (`result_2x2.json` `count_blind_spot`: count blind to drop-N-add-N, completeness anti-join catches it). Generative-but-independent, NOT the dead self-anchored h0006/h0007/h0008 family. No scope creep beyond the single grain rule. |
| G7 actionability/inert-risk | PASS (WARN-class note) | Carries a worked-example skeleton (the G7 mechanical form): a `text` recipe (`produced=13` vs `expected=count(distinct project_id)=16`, plus a `raw keys EXCEPT output` anti-join returning 3 missing keys) and a literal BEFORE/AFTER `sql` block (`from {{ source('app','projects') }} p left join (<child agg>) c using(project_id)`). Copyable, not abstract structural prose. Inert-risk persists and is the real go/no-go: this @baseline rejected three prior grain levers (h0010/h0016/h0017) as talks-but-doesn't-do — the run-first-CAPPED smoke inert-detector (`Got 7` must drop below 5) is the decisive read; ≥5 byte-unchanged ⇒ inert NO-GO, no iteration. |
| G8 regression-canary coverage | PASS | Generative-class (fires on every aggregate/entity model meant to be complete over a parent key set ≈ most aggregates) — the anti-join does NOT narrow scope, it adds a second probe on the same gated set, so the canary requirement is unchanged. Smoke panel: f1001/f1005 (f1, the h0012-fragile figure-rewrite family — f1005 a direct h0012 casualty), ana-eng001/ana-eng002 (ana-eng, aggregate-heavy) = ≥2 perturbable canaries on EACH construct-sharing family; plus airbnb001/asana001/quickbooks002 one-per-family. All 7 re-confirmed `@baseline` reward=1.0 passers (re-read from 622bdedac572b479 `per_trial_outcomes.json` `trials[]`). intercom legitimately supplies no canary (intercom001/002/003 all reward=0.0; all 3 are targets). |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — single generative Implementation instruction, no N-candidate scoring. |
| G10 self-correcting false-positive | PASS | Self-correcting (reconcile-and-fix-on-shortfall) — direct successor to REJECTED h0012. **(a) scope:** GATED to models "whose grain is meant to be COMPLETE over a parent key set … as described by its `schema.yml` entry or the task instruction"; legitimately-filtered aggregates explicit-exempt and "do not invent a parent" — NOT generative-on-every-aggregate. **(b) independence source:** BOTH probes target the raw PARENT via "a plain SELECT on the raw source, with NO model logic; do NOT re-run, re-derive, or wrap your own model" — separately-sourced, not a re-derived CTE. E0/h0032 `correlated_error_trap` independently confirmed that reading a solver-rebuilt intermediate re-correlates into a false-green, so the raw-source binding is load-bearing and is preserved verbatim. **(c) check-don't-replace:** a shortfall OR a non-empty anti-join is "a SIGNAL TO INVESTIGATE, NOT an automatic rewrite" — re-read intended grain, rebuild only if completeness is intended (case i), leave-it if legitimately scoped (case ii), and "NEVER replace a simple, correct aggregate with a structurally-different path merely to change the number" — the direct softening of the h0012 mandate-replace that lost −4. |

**For the captain:** No blockers — APPROVE to `smoke`. (1) The revision did exactly what was asked: the count is now PAIRED with the completeness anti-join (the E0/h0032 drop-N-add-N fix), and the target set is scoped to E1 = intercom001/002/003 only (airbnb009 → E2/h0019, asana004 → Track Z, recorded in the body). The prior G4 WARN is gone — the spec and the named targets now agree. (2) G7/inert-risk is the only real go/no-go and it is unchanged by the anti-join: this @baseline has rejected three prior grain levers as talks-but-doesn't-do. Per the run-first-CAPPED decision, the smoke runs ONCE; the decisive leading indicator is `intercom Got 7` dropping below 5 — if it does not, it is the inert wall (h0010/h0016/h0017) and we do NOT iterate. Require artifact-proven parent-grained SQL in the commit before banking any flip (h0012's f1006 flipped at smoke and reverted at full).

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

## Stage Report: propose (cycle 2 — E1/anti-join revision)

- DONE: Forked solver README's reconcile instruction now PAIRS the raw-parent COUNT(*) vs COUNT(DISTINCT key) reconcile WITH a completeness ANTI-JOIN (every DISTINCT parent key from the RAW source must appear in the output) -- per E0/h0032's drop-N-add-N finding (`_artifacts/h0032-e0-harness/result_2x2.json` `count_blind_spot`: count silent, anti-join fires).
  `diff codex-ade-dbt-minimal/README.md fork/README.md` = single pure addition `63a64,128` (0 `<` lines). The Implementation paragraph now lists TWO probes (count + anti-join) both a plain SELECT on `{{ source() }}`; raw-source binding preserved verbatim ("do NOT re-run/re-derive/wrap your own model"); worked-example `text` skeleton updated to show BOTH `count(distinct ...)` and a `raw keys EXCEPT output` anti-join. Still a SINGLE Implementation idea; leak-guard byte-identical (G2 grep NONE_FOUND).
- DONE: Smoke spec scoped to E1 = intercom001/002/003 ONLY plus the existing perturbable canary panel (f1001/f1005/ana-eng001/ana-eng002 + airbnb001/asana001/quickbooks002); airbnb009 and asana004 REMOVED from the spec and the body's `## Target datasets` updated to record airbnb009 -> E2/h0019 (date-spine already built; residual is a cross-join, not a missing spine) and asana004 -> Track Z (oracle-only int_ convention).
  `diff full smoke` = only the added `benchmark.tasks` (10 tasks: intercom001/002/003 + the 7 canaries). Full spec still differs from baseline.yaml ONLY in experiment + solver_workflow. Baseline rewards re-read from 622bdedac572b479 `trials[]`: intercom001/002/003 = 0.0 (targets); all 7 canaries = 1.0 (passers).
- DONE: Both specs re-frozen via rk freeze --allow-missing; kind=spacedock_solver / runtime=codex / trials=1 preserved.
  `…frozen.yaml` (1749B) + `…smoke.frozen.yaml` (1987B), re-frozen Jun 7 10:33; both `sealed_hash 00483f8e…`, `solver_workflow_content_hash sha256:a49994d6…` (changed from pre-revision `9e8f75e3…` — anti-join README captured).
- DONE: Gatekeeper re-run on the REVISED artifacts; the `## Gatekeeper review` block refreshed (per-rule PASS/WARN/FAIL incl. G8/G10 + overall APPROVE) reflecting the anti-join pairing and the intercom-only target set.
  Recommendation APPROVE (cycle 2). The prior G4 WARN is now PASS (smoke targets == Target datasets == intercom001/002/003). G6/G10 cite the anti-join pairing + E0's `correlated_error_trap` (raw-source binding load-bearing). No FAILs.

### Summary

Revised the already-APPROVED h0030 to align with E0/h0032 + the E1 triage. Three changes: (1) the Implementation rule now runs TWO raw-parent probes — the COUNT(DISTINCT key) reconcile AND a completeness anti-join (every raw parent key must appear in the output), because E0 proved a bare count is blind to drop-N-add-N while the anti-join CLEARED two-sided; the raw-source binding (plain SELECT on `{{ source() }}`, never the model's own CTE) is preserved as load-bearing. (2) The smoke is scoped to E1 = intercom001/002/003 only plus the existing 7-canary panel; airbnb009 and asana004 were removed and re-routed (E2/h0019 and Track Z) with the body's Target datasets + Hypothesis + caveat updated. (3) The gatekeeper review block is refreshed to APPROVE with the G4 WARN resolved. Both specs re-frozen with a new solver_workflow_content_hash; kind/runtime/trials preserved. NOTE: the dispatch fetch command `claude-team show-stage-def` was not on PATH (exit 127); recovered it from the on-disk binary `/home/kent/spacedock/skills/commission/bin/claude-team` — flagging the broken PATH to the FO. Per the run-first-CAPPED captain decision, propose stops at the gate; the smoke is NOT launched.
