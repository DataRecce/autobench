---
id: h0019
title: Implementation — on a repair, let each category/group emerge from the existing join, never force a constant per-key row by cross-joining every category against every key value
status: hypothesis
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

## Smoke result

## Run result

## Behavioral analysis

## Verdict
