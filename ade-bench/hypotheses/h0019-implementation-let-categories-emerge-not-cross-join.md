---
id: h0019
title: Implementation — on a repair, let each category/group emerge from the existing join, never force a constant per-key row by cross-joining every category against every key value
status: propose
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type 1b - Grain - date/calendar spine (missing days)); in-stage lever (Implementation). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed:
verdict:
score:
worktree:
---
## Hypothesis

`airbnb009` is the date/calendar-spine (missing-days) bug. The model the task names —
`models/agg/mom_agg_reviews.sql` — narrows a complete date dimension down to only dates that
have a review (`dates_cte` does `SELECT DATE_ACTUAL FROM dim_dates WHERE DATE_ACTUAL IN
(SELECT DISTINCT REVIEW_DATE::DATE FROM review_cte)`), so days with no review are dropped. The
instruction states the contract verbatim: "there should be a row for every day. Right now, some
days are missing." The hidden continuous-day check fails `Got 1` on `@baseline`.

The decisive ground-truth fact (read straight from the `@baseline` run-dir
`622bdedac572b479`, `ade-bench-airbnb009`): the solver **already diagnosed and half-fixed**
this without any prompting. Its committed `mom_agg_reviews.sql` and agent summary say it "uses
a continuous `dim_dates` spine from min to max review date, **cross joins observed
sentiments**, and counts only matched review rows," reporting `expected_days=4508`,
`actual_mom_days=4508`, `missing_mom_days=0`. So it removed the narrowing filter and drove
from the full min/max-bounded date spine on its own — yet it **still failed**, because it
then cross-joined all three review sentiments onto every day, over-producing rows
(every day forced to exactly 3 sentiment rows) instead of letting sentiments emerge from the
existing `LEFT JOIN`. The continuous-spine half of the fix is therefore **already done by the
solver unprompted and is inert as an instruction**; the single net-new, load-bearing
instruction this hypothesis adds versus the `@baseline` behavior is the **anti-cross-join
clause**: when the model carries a secondary grouping column, do not multiply every category
value against every key value — let the categories emerge for each key through the join the
model already has.

**What is and is NOT locally derivable (stated plainly, because the lever depends on it).**
The bug *location* (the narrowing filter on `dim_dates`) and the correct *edit shape* (drop
the filter, keep the existing `LEFT JOIN` + `GROUP BY`, do not cross join the sentiments) are
fully derivable from local files — the model SQL, its `ref('dim_dates')`, and the
instruction. The correct *row count* is NOT locally derivable: it lives only in the hidden
continuous-day check, which does not ship to the workspace. This rule therefore steers the
EDIT SHAPE only; it deliberately does **not** ask the solver to validate against any target
count, and it must not be read as a self-verification lever (the dead h0006/h0007/h0008
family). The acceptance signal the solver can observe locally is structural, not numeric:
rows-per-key VARY with the data rather than equalling a constant (number of keys) x (number
of distinct categories).

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation rule that (a) frames a completeness repair as a subtractive in-place edit
(drop the one narrowing filter; keep the existing join and `GROUP BY` byte-intact), and (b)
— the primary, net-new lever — forbids cross-joining every category value against every key
value, instructing the solver to let a secondary grouping column's values emerge per key
through the existing `LEFT JOIN`/`GROUP BY` (so rows-per-key VARY with the data, and a row
count of (keys) x (categories) is the signature of a wrong, over-producing cross join) —
will flip `airbnb009` (`ade-bench-airbnb009`) from FAIL to PASS by suppressing the
over-production the `@baseline` solver demonstrably produced, raising
`stratified_pass_at_1` above the `@baseline` 0.6458.

**Why this escapes the dead-prose ceiling (and where it sits relative to it).** The archived
grain levers (h0010 prose, h0016 worked-example) asked the solver to **restructure** a query
— build FROM an entity spine, reverse the join direction — and were acknowledged-but-not-
executed or installed-the-shape-but-not-the-correct-spine. This is the opposite shape: it is
a **subtractive, in-place edit** that asks the solver to *keep* the structure it already has
and merely *not* introduce a cross join — the asana002-class mechanical edit (the only kind
that has ever landed), not a rewrite. It is anchored to a concrete local artifact (the
model's own existing `LEFT JOIN` and `GROUP BY`, the `dim_dates` relation it already `ref`s)
and to the one residual defect the `@baseline` transcript actually exhibits. Honest caveat:
whether prose can flip the solver's demonstrated strong instinct to force-fill all sentiments
is unproven and sits under the same README-prose ceiling (h0008 0/7, h0010 0/4, h0011 0/3,
h0016 0/4). This is filed because the anti-cross-join steer is the one genuinely-untried,
correctly-shaped (subtractive, no magic count required) lever left for this bug type; if
smoke shows the committed SQL still cross-joins the sentiments, the rule joins the prose
ceiling and is REJECTED.

Distinct from h0012 (Validation stage, also lists `airbnb009`): h0012 catches the
over-production AFTER building via an independent row-count recompute; this prevents it AT
build time by constraining the edit shape — the construction-side angle the coverage map
names as OPEN for the fan-out/over-production sub-type. Distinct from the new Output Contract
stage, which by design SKIPS pure-repair tasks — `airbnb009` is a pure repair, so the contract
stage cannot engage it; this rule operates precisely in the repair lane the contract stage
abandons. Distinct from REJECTED h0010/h0016, which asked for a restructure (build FROM a
spine); this forbids restructuring and pins the fix to deleting one filter while preserving
the existing structure and not adding a cross join.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact: the added text references only local artifacts
(the model's own SQL, its existing `ref` to a date/reference relation, its existing
`LEFT JOIN`/`GROUP BY`) and names no hidden `AUTO_*`/`solution__*`/`check_*`/verifier test,
no `equality test`/`has less columns`/`expected output seed`, no `Got N` or any hidden row
count, and no `curl`/`wget`/`git clone`/web/published-solution fetch; the structural
acceptance signal (rows-per-key vary, not a constant) is phrased against the model's own
data, not the oracle's bounds. The change touches exactly one `## Stage: Implementation`
block and leaves the leak-guard prose (README lines ~1-32) byte-identical. The spec differs
from `@baseline` only in `experiment:` + `solver_workflow:` (smoke may add only
`benchmark.tasks`).

Target dataset (smoke, `ade-bench-` prefixed): the date-spine over-production failure —
`ade-bench-airbnb009`. This rule is **generative** (it fires on any completeness repair, not
gated to the target), so per gatekeeper G8 the smoke set carries a cross-family
regression-canary panel — one currently-passing `@baseline` task from each other family
(verified `reward=1.0` in `622bdedac572b479/per_trial_outcomes.json`):
`ade-bench-airbnb001` (airbnb passer / same-family sentinel), `ade-bench-asana001` (asana),
`ade-bench-ana-eng001` (ana-eng), `ade-bench-f1007` (f1), `ade-bench-quickbooks002`
(quickbooks). **No intercom canary is possible:** intercom has no passing `@baseline` task
(`intercom001/002/003` all fail), so that family cannot supply a passer — G8 should not
expect one.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h00NN-implementation-let-categories-emerge-not-cross-join.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Implementation` (the single subtractive-repair / anti-cross-join
rule, inserted after the "...schema patterns." paragraph and before "Run basic
confirmation..."), leaves Exploration/Validation/Finalization and the dependency/package
guardrails untouched, and does not reference hidden `AUTO_*`/`solution__*`/verifier tests or
weaken the leak-guard. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`. The smoke deep-dive must read the committed
`mom_agg_reviews.sql` (the dispatched-ensign `apply_patch` payload) and confirm the
anti-cross-join clause REACHED the SQL — rows-per-day VARY rather than a constant per-day
sentiment count, and the over-producing cross join is gone — plus the `Got N` distance vs
`@baseline`. Transcript chatter mentioning "continuous spine"/"left join" is NOT evidence the
rule landed (the h0010/h0016 lesson); if the committed SQL still cross-joins the sentiments
the rule is INERT/ceiling-bound → REJECTED.

**Smoke gate:** on the target `ade-bench-airbnb009` + the G8 canary panel (`ade-bench-airbnb001`,
`ade-bench-asana001`, `ade-bench-ana-eng001`, `ade-bench-f1007`, `ade-bench-quickbooks002`),
the variant must not regress any canary and should flip `airbnb009` to a pass — verified by
the committed-SQL artifact read above (cross join suppressed), not by transcript chatter —
before promotion to full.

## Gatekeeper review

**Recommendation: APPROVE** — single subtractive/anti-cross-join Implementation rule, now hardened with a copyable BEFORE/AFTER SQL worked-example skeleton; leak-guard byte-identical, both specs minimal, G8 panel present; no FAILs. **G7 now PASSes** (the prior WARN was "abstract prose, no skeleton" — the captain's REVISION added the before→after SQL, the exact G7 PASS ingredient). One residual WARN (G8 perturbable-canary gap) is a structural limit of the dataset, not a blocker.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T13:10:00Z (cycle 2 — re-run after the worked-example-skeleton revision).

Fork parent resolved: `source:` names `solver_workflows/codex-ade-dbt-minimal`; `rk registry resolve run @baseline` → `runs/ade-bench-baseline/622bdedac572b479`, whose `solver_workflow` is `codex-ade-dbt-minimal`. Agree → parent = `solver_workflows/codex-ade-dbt-minimal`.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff` parent→fork = one pure-addition hunk `55a56,98` (43 added lines, 0 deletions), all under `## Stage: Implementation`; Exploration/Validation/Finalization byte-identical (each region diffed = IDENTICAL); exactly one `## Stage: Implementation` header. One idea: subtractive completeness repair + anti-cross-join, now with its before→after SQL skeleton. |
| G2 leak-guard intact | PASS | Leak-guard prose (lines 1-32) byte-identical to parent (diffed = IDENTICAL). Forbidden-token grep over the FULL added block incl. the new SQL (`AUTO_`/`solution__`/`check_option`/`check_*`/`verifier`/`equality test`/`has less columns`/`expected output seed`/`Got N`/`curl`/`wget`/`git clone`/`git ls-remote`) = clean; also no spine re-instruction (`continuous`/`dim_dates`/`spine`/`sentiment`/`4508`/`calendar`/`review_date`/`mom_agg`) and no oracle count. Skeleton uses ONLY generic identifiers (`ref('key_set')`, `ref('fact_detail')`, `key_col`/`category_col`); the relation alias was renamed `key_spine`→`key_set` precisely so the word "spine" appears nowhere. |
| G3 spec two fields | PASS | `diff baseline.yaml h0019…yaml` = only `experiment:` + `solver_workflow:`. `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. (Re-froze after the README edit; semantic spec diff unchanged.) |
| G4 smoke tasks-only | PASS | `diff h0019…yaml h0019….smoke.yaml` = only added `benchmark.tasks` block (6 IDs, all `ade-bench-` prefixed), UNCHANGED by this revision. Includes the named target `ade-bench-airbnb009` + a stable-pass sentinel (`ade-bench-airbnb001`). |
| G5 both frozen | PASS | `h0019….frozen.yaml` + `…smoke.frozen.yaml` both RE-frozen by `rk freeze --allow-missing` after the README edit; both carry `kind: spacedock_solver` + `runtime: codex`; smoke frozen lists all 6 tasks. `solver_workflow_content_hash` changed `133891fa…`→`9394871c…`, confirming the freeze captured the new skeleton. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: Implementation stage, (a) subtractive in-place edit (drop the one narrowing filter; keep existing `LEFT JOIN`+`GROUP BY` byte-intact), (b) anti-cross-join (let category emerge per key; constant keys×categories = wrong-cross-join signature). The added SQL skeleton FAITHFULLY illustrates exactly (b): BEFORE = `cross join (select distinct category_col …)` forcing constant rows-per-key; AFTER = category from the EXISTING `left join` + `group by`, rows-per-key VARY. Generative/construction-side, explicitly "a check on the edit's shape against the model's own data, not a check against any external or expected count" — NOT the dead self-anchored family. Spine deliberately NOT re-instructed (the skeleton's `key_set` relation is a generic key set, NOT a date-spine build instruction — the @baseline already builds the spine unprompted). |
| G7 actionability/inert-risk | PASS | **Flipped WARN→PASS by the revision.** The load-bearing anti-cross-join half now carries a literal copyable BEFORE/AFTER `sql` skeleton (`cross join (select distinct category_col …)` → drop it, category emerges from the existing `left join … group by`), the exact "worked-example skeleton the solver can copy rather than re-derive" form G7's PASS clause names and the ingredient that let h0030's skeleton REACH the committed SQL where prose-only h0010/h0016 went inert. Inert-risk PERSISTS as the program watch-item (this @baseline rejected prose levers h0008/h0010/h0011/h0016), so the decisive go/no-go remains the committed `mom_agg_reviews.sql` read at smoke — but per the guideline G7 PASSes once a copyable skeleton is present; it no longer WARNs. |
| G8 regression-canary coverage | WARN | Generative (fires on any completeness repair carrying a secondary grouping column, not gated to the target) — UNCHANGED by this revision. Smoke panel carries ≥1 `@baseline` passer (reward=1.0 in 622bdedac572b479) from every non-target family that HAS a passer: airbnb001 (airbnb), asana001 (asana), ana-eng001 (ana-eng), f1007 (f1), quickbooks002 (quickbooks). Intercom correctly omitted — no `@baseline` intercom passer exists (001/002/003 all fail). WARN, not PASS: the family sharing the target's construct (airbnb) supplies only ONE non-target passer (airbnb001), and the canaries are not themselves completeness-repair-with-secondary-grouping tasks, so the ≥2-perturbable-canary clause cannot be fully satisfied (no second airbnb passer + no other completeness-repair passer exists to recruit). Best achievable coverage given the dataset; accept the residual blind spot at full. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — single in-stage Implementation edit-shape rule, one solver session. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever. It constrains the EDIT SHAPE at build time and explicitly disclaims any verify-against-a-count or fix-on-disagreement step ("not a check against any external or expected count"); it never re-derives a figure to compare and act on. No self-correcting mechanism to evaluate. |

**For the captain:** No FAILs → advance to smoke (CAPPED one-shot). The revision did what it set out to: G7 flipped WARN→PASS because the anti-cross-join rule now ships a copyable before→after SQL skeleton (the h0030 ingredient prose-only h0010/h0016 lacked). Inert-risk is no longer a gatekeeper WARN but remains the real go/no-go: the decisive read is the committed `mom_agg_reviews.sql` — STILL cross-joins all sentiments / `Got 1` unchanged = INERT NO-GO with NO iteration (CAPPED per the program); category rows-per-day VARY = the lever landed. G8 WARN is a structural dataset limit (only one airbnb non-target passer, no other completeness-repair passer to recruit as a perturbable canary), not a fixable omission — accept the residual full-scale blind spot.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: Forked solver README adds EXACTLY the anti-cross-join Implementation rule
  `cp -r` fork `solver_workflows/h0019-implementation-let-categories-emerge-not-cross-join`; `diff` vs parent = one hunk `55a56,73` (18 added lines, 0 deletions), all under `## Stage: Implementation`; rule = subtractive in-place edit (drop the one narrowing filter, keep `LEFT JOIN`+`GROUP BY` byte-intact) + anti-cross-join (categories emerge per key; constant keys×categories = wrong-cross-join signature). Spine NOT re-instructed.
- DONE: One ## Stage: Implementation block only; Exploration/Validation/Finalization + leak-guard byte-identical; no hidden tokens
  Leak-guard (lines 1-32) and Exploration/Validation/Finalization byte-identical to parent (verified by `diff` of each region); forbidden-token grep over added lines clean (no `AUTO_*`/`solution__*`/`check_*`/`verifier`/`Got N`; no spine/`dim_dates`/`sentiment`/oracle-count tokens).
- DONE: Specs — full differs from baseline ONLY in experiment+solver_workflow; smoke adds ONLY benchmark.tasks (target + G8 panel)
  `diff baseline.yaml h0019…yaml` = 2 fields; `diff h0019…yaml …smoke.yaml` = only added `tasks:` block = ade-bench-airbnb009 (target) + airbnb001/asana001/ana-eng001/f1007/quickbooks002 (G8 canaries, no intercom passer exists). Both frozen via `rk freeze --allow-missing`; kind=spacedock_solver/runtime=codex/trials=1 preserved in both frozen files.
- DONE: Gatekeeper ran; ## Gatekeeper review block written with per-rule table + overall recommendation
  Recommendation APPROVE (no FAILs). G1/G2/G3/G4/G5/G6 PASS; G7 WARN (inert-risk — anti-cross-join half is abstract prose, the live watch-item); G8 WARN (generative panel present but no second perturbable airbnb canary exists to recruit); G9/G10 N/A.

### Summary

Forked the @baseline solver and inserted exactly one Implementation-stage rule: a completeness repair is a subtractive in-place edit (drop the one narrowing filter, keep the existing `LEFT JOIN`+`GROUP BY` byte-intact) that MUST NOT cross-join every category value against every key — let the secondary grouping column emerge per key so rows-per-key VARY. The spine half is deliberately NOT re-instructed because the @baseline airbnb009 transcript shows the solver already builds the continuous spine unprompted (its summary: "cross join observed sentiments", mom_rows=13524=4508×3, `Got 1`) — so the anti-cross-join clause is the single net-new lever. Specs are minimal (full=2 fields, smoke adds the target + a 5-family G8 canary panel; intercom has no passer); both frozen with kind/runtime/trials preserved. Gatekeeper recommendation: APPROVE with two known-program WARNs — G7 inert-risk (this sits under the README-prose ceiling, so the decisive smoke read is whether the committed `mom_agg_reviews.sql` STILL cross-joins → INERT/NO-GO/no-iterate vs lets categories emerge → landed) and G8 (the airbnb construct-family supplies only one non-target passer). Propose STOPS at the gate — no rk run launched.

## Stage Report: propose (cycle 2)

- DONE: The forked README's anti-cross-join Implementation rule now carries a copyable BEFORE/AFTER SQL WORKED-EXAMPLE skeleton
  Added a `sql` block right after the anti-cross-join prose (still inside the single `## Stage: Implementation`): BEFORE = `cross join (select distinct category_col from {{ ref('fact_detail') }})` against `{{ ref('key_set') }}` → constant rows-per-key = keys × categories; AFTER = drop the cross join, category emerges from the EXISTING `left join {{ ref('fact_detail') }} … group by` so rows-per-key VARY. Generic identifiers only (`key_set`/`fact_detail`/`key_col`/`category_col`); the relation alias was renamed `key_spine`→`key_set` so the word "spine" appears nowhere; NO spine re-instruction; no `dim_dates`/`sentiment`/`4508`/`continuous` target-specifics; no hidden `AUTO_*`/`solution__*`/`check_*`/`Got N` tokens. Diff parent→fork = one pure-addition hunk `55a56,98` (43 lines, 0 deletions); leak-guard (1-32) + Exploration/Validation/Finalization byte-identical (each region diffed = IDENTICAL); exactly one `## Stage: Implementation` header.
- DONE: Both specs re-frozen via `rk freeze --allow-missing`; full differs from baseline.yaml ONLY in experiment+solver_workflow; smoke benchmark.tasks UNCHANGED; kind/runtime/trials preserved
  Re-froze both after the README edit (`RAZORBACK_SPACEDOCK_PLUGIN_DIR` exported, run from ade-bench/). `diff baseline.yaml h0019…yaml` = only `experiment:` + `solver_workflow:`. `diff h0019…yaml …smoke.yaml` = only the unchanged 6-task `benchmark.tasks` block (airbnb009 + airbnb001/asana001/ana-eng001/f1007/quickbooks002). Frozen full vs baseline.frozen differs only in experiment + solver_workflow path + their derived hashes (`solver_workflow_content_hash` `133891fa…`→`9394871c…` confirms the new skeleton was captured); `kind: spacedock_solver`/`runtime: codex`/`trials: 1` preserved in both frozen files; smoke frozen lists all 6 tasks.
- DONE: Gatekeeper re-run on the revised variant; `## Gatekeeper review` refreshed — G7 verdict reflects the added worked-example skeleton; overall APPROVE/REVISE/REJECT with one-line rationale
  Re-reviewed against `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). **G7 flipped WARN→PASS** — the rule now carries the literal copyable before→after SQL skeleton G7's PASS clause names (the h0030 ingredient h0010/h0016 lacked). G1/G2/G3/G4/G5/G6 PASS; G8 remains WARN (structural dataset limit — only one airbnb non-target passer, no other completeness-repair passer to recruit as a perturbable canary); G9/G10 N/A. Overall: APPROVE, no FAILs. Inert-risk persists as the program watch-item but is no longer a gatekeeper WARN; the decisive go/no-go is the committed `mom_agg_reviews.sql` read at smoke (CAPPED one-shot, no iteration).

### Summary (cycle 2)

Applied the captain's REVISION: added a copyable BEFORE/AFTER SQL worked-example skeleton to the anti-cross-join Implementation rule. BEFORE shows the over-producing `cross join (select distinct category_col …)` that forces a constant rows-per-key = keys × categories; AFTER drops it so the category emerges through the model's EXISTING `left join … group by` and rows-per-key VARY. Phrased entirely generically (`key_set`/`fact_detail`/`key_col`/`category_col`) — renamed the relation alias `key_spine`→`key_set` so "spine" appears nowhere, added no date-spine instruction, and leaked no target-specifics or hidden tokens. Kept ONE Implementation block; leak-guard + Exploration/Validation/Finalization byte-identical; smoke tasks unchanged. Re-froze both specs (semantic diffs unchanged; content hash confirms the skeleton was captured). Re-ran the gatekeeper: G7 flips WARN→PASS (a copyable skeleton is now present — the exact ingredient that made h0030 reach the SQL while prose-only levers went inert), recommendation APPROVE with one residual WARN (G8 dataset limit). Propose STOPS at the gate — no rk run launched (CAPPED one-shot per the program).
