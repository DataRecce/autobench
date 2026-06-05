---
id: h0018
title: Output Contract — record a rolling 'over last N days' figure as a calendar-date RANGE copied from the project's own existing rolling-window model, not as N preceding rows
status: hypothesis
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type Tolerance-band divergence (*_equality_with_tolerance) — root-caused on airbnb007 (daily_agg_nps_reviews) as a date-grain / rolling-window CONSTRUCTION error - a per-day aggregate keyed on actually-occurring review_dates with a rolling 'over last 28 days' figure, NOT a numeric-formula error); realizes the new Output Contract stage. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed:
verdict:
score:
worktree:
---
## Hypothesis

The baseline value-divergence re-audit flagged `airbnb007` (`daily_agg_nps_reviews_equality_with_tolerance`, `Got 4` — all four numeric columns `nps_daily` / `reviews_daily` / `nps_28d` / `reviews_28d` outside the `0.01` band) while the sibling `listing_agg_nps_reviews` PASSED. I re-root-caused this directly against the delivered workspace and the verifier test SQL, and it is NOT a numeric-formula bug — it is a date-grain / rolling-window CONSTRUCTION bug, and one piece of it is recoverable from a concrete copyable local artifact:

- **The tolerance test aggregates `sum`/`avg` of the four numeric columns + `min/max(review_date)` + a `total_rows` check** (read the test template directly: `numeric_cols = ['nps_daily','reviews_daily','nps_28d','reviews_28d']`, `sum_tolerance = avg_tolerance = 0.01`). So a wrong grain (extra/missing days) shifts the sum/avg of *every* column, and a wrong 28-day window directly mis-sets the sum/avg of `nps_28d`/`reviews_28d`.
- **Grain is the set of actually-occurring review dates, not a padded calendar spine.** The solution daily output has 3,786 data rows and its early dates are *sparse* (`2009-06-20`, then `2009-08-18`, then `2009-11-25` — not consecutive days), proving one row per day-that-has-a-review, recoverable locally as `select count(distinct review_date) from <filtered reviews>`.
- **The rolling 28-day figure is a calendar-date RANGE, and the project ALREADY implements that exact shape.** The workspace's own `models/agg/mom_agg_reviews.sql` computes a trailing window by left-joining the date spine to reviews on `review_cte.REVIEW_DATE::DATE BETWEEN dates_cte.DATE_ACTUAL::DATE - 29 AND dates_cte.DATE_ACTUAL::DATE` (a 30-day calendar RANGE, with the comment "joining by last 30 days range"). The 28-day window the daily model needs is the same construction with `29` → `27` — a copy-and-change-the-interval substitution, not a re-derivation.

The seed solver's prose tells it to "create the models described in the schema.yml" and to "check ... grain ... row counts ... against source data," but nothing points it at the project's own rolling-window sibling as the window template, and nothing names the calendar-RANGE-vs-N-preceding-rows hazard. The `@baseline` solver produced a daily aggregate whose 28d column magnitudes diverge — a wrong window mechanism on a sparse per-day grain.

**Falsifiable claim (the single README change — the new `## Stage: Output Contract` only):** extending grain rule (1) of the Output Contract stage with one window clause — *when a model computes a rolling 'over last N days' figure (a window-suffixed column like `_28d`, or an instruction asking for a trailing-window total), express the window as a calendar-date RANGE relative to each row's period and COPY the window shape verbatim from the project's own existing rolling-window sibling (e.g. a `*mom*` aggregate that left-joins the spine on `source_date BETWEEN current_date - (N-1) AND current_date`), changing only the interval length; never express it as a fixed `rows between (N-1) preceding and current row` frame, which assumes one row per calendar day and mis-counts on a sparse per-period grain* — will move the committed `daily_agg_nps_reviews` SQL to the correct calendar-RANGE window and grain, narrowing or clearing the `airbnb007` tolerance failure and raising `stratified_pass_at_1` above the `@baseline` 0.6458.

**Why this escapes the dead-prose ceiling.** The rejected grain levers (h0010 prose, h0016 skeleton) asked the solver to *restructure* SQL in the moment of writing it and were acknowledged-but-not-executed; h0011 asked for a column set the local workspace did not contain (premise falsified). This lever is different on the one axis that has ever mattered (the asana002 win under h0009): it is a **mechanical, copyable, in-place substitution anchored to a concrete local artifact that already exists in the same project** — `mom_agg_reviews.sql`'s `BETWEEN ... - 29 AND ...` join. The instruction is "copy this sibling's window join and change 29 to the N your model needs," not "reason your way into the right frame." It is placed in the new Output Contract stage (written down *before* Implementation), the earlier control point the new-stage design argues escapes the in-line-Implementation inertness. It deliberately does NOT claim to recover the within-tolerance *value targets* or the exact window *length* (those live only in the hidden solution seed; the model name `_28d` is the only local cue for N) — so this is filed as a **completeness, low-leverage construction-side bet**, honest about the h0011 blind-to-oracle ceiling, not a high-confidence flip.

**Distinct from existing coverage.** h0012 covers the same target from the **Validation** stage (post-build numeric reconcile) — a different stage and a post-hoc control point; this prevents the divergence at BUILD time inside the Output Contract stage. It is distinct from the Output Contract stage's existing grain rule (1), which only addresses the entity-spine 'do not narrow an extracted CTE key set' case; this adds the orthogonal rolling-window hazard. It carries **no calendar-spine ban** — the earlier candidate's no-spine rule was dropped because it would actively harm `airbnb009` (whose instruction literally asks for "a row for every day ... some days are missing" — i.e. MORE spine) and conflict with the project convention; `airbnb009` is therefore NOT a target here.

Method/README change only. Forks the current `@baseline` solver (`solver_workflows/codex-ade-dbt-minimal`, runtime codex) once the Output Contract stage is in place; no dataset, harness, or solver-runtime change. Leak-guard intact (references only the project's own sibling model + a `count(distinct date)` probe of local source — no public fetch, no oracle, no reference to hidden `AUTO_*` / `solution__*` / `_with_tolerance` / `_equality` tests). Spec differs from baseline only in `experiment:` + `solver_workflow:` (smoke adds only `benchmark.tasks`).

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h<NNNN>-contract-rolling-window-calendar-range.yaml` shows only `experiment:` + `solver_workflow:`; the README diff vs the Output-Contract-bearing parent touches ONLY grain rule (1) inside the `## Stage: Output Contract` block (the single rolling-window clause), leaves Exploration/Implementation/Validation/Finalization and the leak-guard/dependency-package prose (lines ~1-32) byte-identical, and references no hidden `AUTO_*` / `solution__*` / `_with_tolerance` / verifier tests. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean (`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta (CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean audit AND `stratified_pass_at_1 > 0.6458`. Because the within-tolerance values and exact window length for `daily_agg_nps_reviews` are not locally derivable, the load-bearing smoke signal is the per-target flip on `airbnb007` plus zero regression on the canary panel — NOT the smoke-panel mean.

**Smoke gate:** on the single target `ade-bench-airbnb007` plus the cross-family `@baseline`-passer canaries `ade-bench-airbnb001` / `ade-bench-ana-eng001` / `ade-bench-asana001` / `ade-bench-f1007` / `ade-bench-quickbooks002` (this rule is generative — it fires on every authoring task that has a rolling-window column — so per gatekeeper G8 it carries one passing canary from each non-target family; intercom supplies no canary because it has no `@baseline` passer), the variant must hold every canary PASS and should move `airbnb007`'s committed `daily_agg_nps_reviews` SQL to the copied calendar-RANGE window (verify the committed apply_patch payload contains a `BETWEEN <date> - 27 AND <date>`-style join lifted from `mom_agg_reviews`, and check the `Got N` distance vs `@baseline` — do not trust transcript chatter) before any promotion to full.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
