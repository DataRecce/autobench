---
id: h0016
title: Implementation — grain-spine fix as a CONCRETE worked-example SQL skeleton (not a prose rule), to test whether copyable beats described
status: conclude
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

**Run-dir:** `runs/ade-bench-h0016-implementation-grain-spine-worked-example/404f632989ecc074`
(frozen smoke spec, 9/9 trials, 0 errored). **Audit:** `rk audit --policy strict` =
`clean_trials: 9/9`, zero findings; every cell `subagent-trace-manifest.json` `captured=1`
(AC-2 satisfied). **Score:** `stratified_pass_at_1 = 4/9 = 0.4444` (`above` the 0.1875
paper anchor — but that anchor is irrelevant on a hand-picked smoke set; the live question
is target flips + canary holds).

**Verdict / distance-to-pass vs `@baseline` (`622bdedac572b479`):**

| Task | Role | base reward | smoke reward | base Got-N | smoke Got-N | moved? | classification |
|------|------|-------------|--------------|------------|-------------|--------|----------------|
| asana004 | 🎯 target | 0 | 0 | 3 | 3 | no | **inert** — grain bug lifted verbatim into new model |
| asana005 | 🎯 target | 0 | 0 | 3 | 3 | no | **inert** — same |
| intercom001 | 🎯 target | 0 | 0 | 7 | **5** | **yes** | **executed-but-still-failing** — skeleton landed, gap narrowed |
| intercom003 | 🎯 target | 0 | 0 | 7 | 7 | no | **inert** — grain still driven off child |
| asana001 | ✅ sentinel | 1 | 1 | — | — | — | held ✅ |
| airbnb001 | ✅ canary | 1 | 1 | — | — | — | held ✅ |
| ana-eng008 | ✅ canary | 1 | 1 | — | — | — | held ✅ |
| quickbooks004 | ✅ canary | 1 | 1 | — | — | — | held ✅ |
| f1001 | ✅ canary | 1 | **0** | (PASS) | **14** | regressed | **PASS→FAIL** (mechanism below — NOT lever-attributable) |

**Net: 0/4 targets flipped; 1 canary (f1001) regressed PASS→FAIL; sentinel + 3 canaries held.
Go/No-Go = NO-GO** (a canary dropping FAIL is a NO-GO regardless of target movement; here
target movement was also zero flips).

## Run result

Smoke-only NO-GO — no full run. The smoke deep-dive below is the evidence of record
(`smoke → conclude`, REJECTED).

## Behavioral analysis

Committed-artifact reads (the dispatched-ensign `apply_patch` payloads in each cell's
`agent/sessions/*.jsonl` — the SQL the solver actually wrote, not chatter):

**asana004 / asana005 (refactor tasks — INERT).** Task: move the `agg_project_users` +
`count_project_users` CTEs out of `asana__project` into a new `int_asana__project_user_agg`
model. The solver lifted the two CTEs **verbatim** into the new model and stitched them with
`from count_project_users left join agg_project_users` — i.e. it drove the new model's grain
off a child-aggregation CTE, exactly the original bug, and wired `asana__project` to
`ref('int_asana__project_user_agg')`. The worked-example skeleton (entity table as the FROM
spine) did **not** reach the committed SQL. `Got 3` is byte-for-byte the baseline distance ⇒
inert on these cells. Root cause: these are **refactor** tasks ("move this CTE"), and the
skeleton's premise ("one row per `<entity>`, 0/NULL where no children") has no clean analog —
there is no entity table to spine from; the solver correctly preserved behaviour (the refactor
is faithful) and so preserved the latent grain mismatch the AUTO test catches.

**intercom001 (THE decisive result — EXECUTED-BUT-STILL-FAILING).** The skeleton **landed**:
the committed `intercom__threads.sql` builds a `conversation_ids` spine (UNION of ids from
both history sources), then `left join`s the aggregates with `coalesce(..., 0)` for the
no-child rows — the entity-spine + LEFT-JOIN-agg + 0/NULL pattern the worked example
prescribes. Distance moved `Got 7 → 5`. This is the direct head-to-head win over h0010's
inert PROSE: the **concrete copyable skeleton reached the committed SQL where the prose did
not**. It still fails because the chosen spine (a UNION of ids observed in either child) is
not the true conversation-entity grain — closer, not correct.

**intercom003 (INERT).** Committed model drives FROM `conversation_part_metrics` (a child
agg) and LEFT JOINs `conversations` with coalesce — coalesce present, but the FROM driver is
still the child, so the spine is wrong. `Got 7` unchanged ⇒ inert on grain.

**f1001 regression (NOT lever-attributable — task-level solver variance).** f1001 is a
"create `src_` models" task, unrelated to grain. Baseline (PASS) created
`src_*` views `from {{ source('f1_dataset', 'circuits') }}` under
`models/staging/f1_dataset/`. This run created the same 14 `src_*` views but `from main.circuits`
(raw schema-qualified, no `source()` macro) under `models/core/` — so `src_models_are_correct`
flagged all 14 (`Got 14`). The cell transcript has **zero** references to
grain/spine/one-row-per/worked-example: the lever never fired on f1001 (no "one row per
entity" model). The regression is the `source()`-vs-`main.` convention choice flipping
run-to-run — codex is not bit-reproducible here even at `temperature 0`. It is the noisy
canary doing its job, but it is **independent of the README change**, not convention-bleed
from the skeleton.

**Transferable rule.** The copyable-vs-described claim is *confirmed in the direction it could
be tested*: the concrete skeleton reached the committed SQL on the one target whose task shape
matched its premise (intercom001, 7→5), where h0010's prose was wholly inert. But "lands"
≠ "passes": a copyable structural example only helps when (a) the task is a build, not a
refactor, and (b) the skeleton's spine maps to the true entity grain. On the 3 inert cells
the premise didn't apply (2 refactors with no entity-spine; 1 build where the solver still
picked the child driver). README prose/examples have a hard ceiling here: even a verbatim
worked example flips 0/4 because the grain bug is per-task-specific, not a generic shape the
skeleton can name without leaking the answer.

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

## Stage Report: smoke

- DONE: Smoke run executes detached (nohup) and audits clean — the worked-example change is actually exercised, not inert.
  `runs/.../404f632989ecc074`, 9/9 trials 0 errored; `rk audit --policy strict` = clean 9/9, all cells `captured=1`; no infra/PermissionError recurrence (fresh run was clean).
- DONE: Post-run deep-dive: each of the 4 targets' dbt Got-N vs @baseline (moved vs unchanged), and all 4 canaries (airbnb001/ana-eng008/f1001/quickbooks004) + the asana001 sentinel still PASS.
  asana004/005 Got 3→3 (inert, refactor lifted bug verbatim); intercom001 Got 7→5 (skeleton LANDED, narrowed); intercom003 Got 7→7 (inert, child-driver spine). Sentinel asana001 + canaries airbnb001/ana-eng008/quickbooks004 held PASS; f1001 regressed PASS→FAIL.
- DONE: Go/No-Go recommendation with the net (targets flipped, zero canary/sentinel regressions); a canary dropping to FAIL is a NO-GO.
  NO-GO. Net: 0/4 targets flipped + 1 canary (f1001) regressed. f1001 regression is task-level solver variance (`main.x` vs `source()` macro on a create-src-models task), NOT lever-attributable — lever never fired (0 spine refs in its transcript).

### Summary

Clean smoke run (9/9, strict-audit clean, captured=1 everywhere). NO-GO: zero target flips and an f1001 PASS→FAIL canary drop. The decisive copyable-vs-described finding is positive but partial — on intercom001 the concrete worked-example skeleton REACHED the committed SQL (entity-spine + LEFT JOIN agg + coalesce, Got 7→5) where h0010's PROSE rule was wholly inert; but "lands" did not become "passes" anywhere. The other 3 targets were inert because their task shape (2 refactors, 1 child-driver build) didn't match the skeleton's "one row per entity" premise. f1001's regression is independent run-to-run codex variance, not convention-bleed. Recommend `smoke → conclude` REJECTED; the per-task artifact reads above are the evidence of record.
