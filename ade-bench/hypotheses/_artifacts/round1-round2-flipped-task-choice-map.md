# Round 1 + Round 2 Flipped Task Choice Map

Date: 2026-06-10

Scope: this note covers the 12 unique tasks that flipped at least once relative to
`@baseline` during the Round 1 systematic program and the Round 2 workflow-stage
program. "Flipped" means either baseline `FAIL -> PASS` or baseline `PASS -> FAIL`
in at least one smoke or full run.

Baseline: `runs/ade-bench-baseline/622bdedac572b479`, 31/48.

## Summary

These 12 tasks are not a stable "we can solve these now" set. They are the tasks
where gpt-5.5 at `trials: 1` made different locally plausible implementation
choices across runs. The local workspace often does not fully specify the hidden
grader's convention, so a choice that is reasonable from the visible files can
still fail the hidden oracle.

The central pattern is:

> The model is not usually making syntax mistakes. It is choosing between multiple
> locally defensible repairs, while the hidden oracle accepts only one of them.

## Task Choice Table

| Task | What the task asks for | Locally plausible choices | Observed oracle behavior |
|---|---|---|---|
| `ade-bench-airbnb007` | Create the Airbnb models described in `schema.yml`, including rolling NPS/review aggregates. | A. Compute the 28-day rolling window with a calendar date range. B. Use `ROWS BETWEEN 27 PRECEDING`. C. Fix only `daily_agg_nps_reviews` and leave `listing_agg_nps_reviews` untouched. | A is correct for `daily_agg_nps_reviews`; B fails on sparse dates. C can look green in smoke but is insufficient at full because the task is scored by a second model, `listing_agg_nps_reviews`. |
| `ade-bench-airbnb009` | Fix `mom_agg_reviews` so there is a row for every day; some days are missing. | A. Remove the narrowing date filter and suppress the category cross join while preserving the existing `COUNT(*)`. B. Suppress the cross join but "clean up" the aggregate to `COUNT(review_date)`. | A passes. B is semantically defensible because no-review days count as zero, but the hidden oracle expects the existing `COUNT(*)` behavior. |
| `ade-bench-asana002` | Update the project for a new Fivetran Asana package version. | A. Treat the issue as a representation/type mismatch and add a model-layer cast such as `::timestamp`. B. Treat it as a package-migration shape change where tags became optional and gate tag models/columns with `using_task_tags`. | B passes. A was the proposed cast lever, but the artifact showed no cast surface; the green flip came from a solver-native structural repair. |
| `ade-bench-asana003` | Remove all Asana `tmp` models and make `stg_asana__*` models reference source tables directly. | A. Repoint conservatively while preserving the tmp layer's type/value behavior. B. Rewrite broadly to `var()` source paths and delete tmp models. | A passes. B follows the instruction literally, but it can introduce type/value drift and a `None` date conversion error. |
| `ade-bench-f1005` | Fix `constructor_points.sql` because the `points` column is too high. | A. Use `max(points)` over cumulative standings to recover the final season total. B. Select the latest/final standing row with date/rank logic such as `standings_rank = 1`. | A passes. B looks like the final standing but fails on edge cases where latest row and max cumulative points differ. |
| `ade-bench-f1005-medium` | Fix wrong results in `constructor_points.sql`. | A. Use `max(points)`. B. Use latest/final-row rank logic. | A passes. B fails for the same max-vs-latest reason as `f1005`. |
| `ade-bench-f1006` | Fix too-high `points` columns in both `constructor_points.sql` and `driver_points.sql`. | A. Change cumulative `sum(points)` to `max(points)` in both models. B. Use latest standings rows. C. Recompute from race results. | A has passed in a smoke run. B and C are locally plausible but can diverge from the hidden grader's convention. |
| `ade-bench-f1006-hard` | Fix wrong results in both `constructor_points.sql` and `driver_points.sql`. | A. Use `max(points)` for cumulative standings. B. Use latest/rank path. | A passes. B failed in the h0037 full run on a two-row edge case. |
| `ade-bench-f1010-medium` | Create `analysis__lap_times` by track/year and account for pit stops correctly. | A. Exclude pit-stop laps before averaging. B. Keep pit-stop laps but subtract pit-stop duration. | A passes. B sounds more precise but the hidden oracle expects exclusion, not subtraction. |
| `ade-bench-f1011` | Choose which listed problems apply to an existing adjusted lap-time analysis and write the answer letters. | A. Answer `ADE`. B. Answer `ABDE`, because a local probe makes option B look supported. | A passes. B is the locally tempting wrong answer; prior arbitration reproduced the same `ABDE` mistake. |
| `ade-bench-quickbooks002` | Remove the `using_department` variable and references, but do not edit the Fivetran source package. | A. Remove the variable/reference while preserving the hidden expected output shape, for example by retaining a `department_name` placeholder/null column where needed. B. Remove department columns entirely because departments are no longer used. | A passes. B is reasonable from the instruction, but the hidden equality tests can fail with "has less columns than solution". |
| `ade-bench-quickbooks004` | Add `using_exchange_rate=false` and hide converted amount/payment exchange-rate columns. | A. Apply the variable narrowly to hide exchange-rate columns while preserving the existing 48-check model shape. B. Perform a broad double-entry / transaction-model refactor across many models. | A is safer. B looks like a complete cleanup but is fragile; in one full run it broke 5 of 48 QuickBooks checks. |

## Cross-Task Patterns

1. SQL convention choices:
   `COUNT(*)` vs `COUNT(column)`, `max(points)` vs latest standing row, and
   excluding pit-stop laps vs subtracting pit-stop duration.

2. Scoring-surface choices:
   a repair can fix one scored model while the task is actually gated by another
   scored model, as in `airbnb007`.

3. Cleanup/refactor choices:
   the model often chooses a broad cleanup that is defensible from the instruction,
   but the hidden oracle expects the old output shape to be preserved more tightly.

4. Attribution boundary:
   a green flip is not proof that the hypothesis caused the fix. `asana002` is the
   clean example: it flipped, but not through the proposed cast lever.

5. Trials-1 implication:
   under `trials: 1`, each locally plausible choice is sampled only once. That makes
   pass/fail movement look like task ability, when it is often just one sampled
   branch of an ambiguous local decision.

## Bottom Line

The 12 flipped tasks are best treated as a sensitivity set: they reveal where the
solver's local reasoning branches into multiple plausible repairs. Only
`ade-bench-airbnb009` has a strong, repeated, artifact-level lever signal, and even
that task remains unbankable because the rule does not pin the hidden-oracle
aggregate choice (`COUNT(*)` vs `COUNT(review_date)`).
