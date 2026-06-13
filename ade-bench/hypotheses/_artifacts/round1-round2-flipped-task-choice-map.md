# Round 1 + Round 2 + Round 3 Flipped Task Choice Map

Date: 2026-06-10 (created) · **Updated 2026-06-13** (extended to Round 3 / composition
runs h0042–h0052; added 7 missing volatile tasks; added canonical gpt-5.5 pass rates).

Scope: this note covers every task that flipped at least once relative to `@baseline`
across the Round 1 systematic program, the Round 2 workflow-stage program, and the
Round 3 lever / composition program (h0042–h0052). "Flipped" means a task both PASSED
and FAILED across the gpt-5.5 `trials: 1` run-dirs on disk (equivalently: it diverges
from baseline `FAIL -> PASS` or `PASS -> FAIL` in at least one smoke or full run).

Baselines:
- Original anchor: `runs/ade-bench-baseline/622bdedac572b479`, 31/48.
- Current `@baseline`: h0043 `runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea`, 32/48.

Pass rates below are computed over all **gpt-5.5** run-dirs on disk (the 2 gpt-5.4-mini
runs are excluded — different solver model). They mix focused smoke panels with full
runs, so the denominator varies per task; treat the rate as a volatility indicator, not
a precise per-draw probability.

## Summary

The volatile set is now **19 unique tasks** (was 12 in the Round 1+2 note). These are
not a stable "we can solve these now" set. They are the tasks where gpt-5.5 at
`trials: 1` made different locally plausible implementation choices across runs. The
local workspace often does not fully specify the hidden grader's convention, so a
choice that is reasonable from the visible files can still fail the hidden oracle.

The central pattern is:

> The model is not usually making syntax mistakes. It is choosing between multiple
> locally defensible repairs, while the hidden oracle accepts only one of them.

**One exception to that rule:** `airbnb008` is the only task here whose flip was
*lever-caused*, not model-choice variance — see its row. Every other task flips on its
own sampling variance independent of any hypothesis.

## Task Choice Table

| Task | Pass rate (gpt-5.5) | What the task asks for | Locally plausible choices | Observed oracle behavior |
|---|---|---|---|---|
| `ade-bench-airbnb005` | 16/18 (89%) | Build the NPS review aggregates, incl. `listing_agg_nps_reviews`. | A. Emit only listings with reviews (or assign the oracle's zero/0.0 NPS convention to zero-review groups). B. Include every listing, leaving NULL NPS on the ~3.2k zero-review groups. | A passes. B emits extra NULL-metric rows that fail `listing_agg_nps_reviews_equality_with_tolerance` (Got 2). The solver self-validates "0 mismatches" against its own derivation — a self-anchored false-green. Failed in h0042 and h0052. |
| `ade-bench-airbnb007` | 4/17 (24%) | Create the Airbnb models in `schema.yml`, incl. rolling NPS/review aggregates. | A. 28-day rolling window via calendar date range. B. `ROWS BETWEEN 27 PRECEDING`. C. Fix only `daily_agg_nps_reviews`, leave `listing_agg_nps_reviews` untouched. | A is correct for `daily_agg_nps_reviews`; B fails on sparse dates. C looks green in smoke but is insufficient at full because a second model, `listing_agg_nps_reviews`, is also scored. |
| `ade-bench-airbnb008` | 18/19 (95%) | (Real fix:) a one-line YAML quote balance in `agg.yml`. **Not** a coverage task. | A. Edit only the YAML quote (correct). B. Apply a date-spine / coverage repair to `mom_agg_reviews` / `wow_agg_reviews`. | A passes. **The single failure (h0046) was LEVER-CAUSED, not solver variance:** the ungated coverage-repair skeleton fired here and applied a predicate-drop to two date-spine models the task never asked to touch, breaking `AUTO_mom_agg_reviews_equality` (Got 28631). Fixed by gating the lever (h0050). The program's only confirmed lever-caused regression. |
| `ade-bench-airbnb009` | 25/36 (69%) | Fix `mom_agg_reviews` so there is a row for every day; some days are missing. | A. Remove the narrowing date filter and suppress the category cross join while preserving `COUNT(*)`. B. Suppress the cross join but "clean up" the aggregate to `COUNT(review_date)`. | A passes. B is defensible (no-review days count as zero) but the hidden oracle expects the existing `COUNT(*)` behavior. The one task with a strong, repeated artifact-level lever signal (h0046/h0050/h0051/h0052 all flip it FAIL→PASS via the same byte-identical edit). |
| `ade-bench-ana-eng003` | 15/16 (94%) | Build `dim_customer` (analytics-engineering). | A. Emit the full solution column set. B. Drop one or more derived columns. | A passes. B triggers a compile-time `AUTO_dim_customer_equality` "has less columns than `solution__dim_customer`" (width) error. Rare flip (only h0012 among gpt-5.5 runs). |
| `ade-bench-asana002` | 14/22 (64%) | Update the project for a new Fivetran Asana package version. | A. Treat as a representation/type mismatch; add a model-layer cast such as `::timestamp`. B. Treat as a package-migration shape change where tags became optional; gate tag models/columns with `using_task_tags`. | B passes. A was the proposed cast lever, but the artifact showed no cast surface; the green flip came from a solver-native structural repair (attribution-boundary example — see Pattern 4). |
| `ade-bench-asana003` | 14/20 (70%) | Remove all Asana `tmp` models; make `stg_asana__*` reference source tables directly. | A. Repoint conservatively, preserving the tmp layer's type/value behavior (keeps `created_at` populated downstream). B. Rewrite broadly to `var()` source paths and delete tmp models. | A passes. B follows the instruction literally but can leave `asana__task` empty/malformed → `asana__daily_metrics`'s Jinja `run_query()` for `min(created_at)` returns None → compiled `cast('None' as date)` parse error → all 6 equality tests cascade-fail. |
| `ade-bench-f1001` | 23/28 (82%) | Re-wire the F1 staging layer onto the correct `src` models / sources. | A. Point every `stg_*` at the correct `src` model and source. B. Leave some staging models on the old/wrong sources. | A passes. B fails `stg_models_use_src_models` (Got 11), `stg_races/stg_results_uses_correct_sources`, and `src_models_are_correct` — incomplete or incorrect source-rewiring. 5 failing runs; broad-footprint convention-bleed canary. |
| `ade-bench-f1003` | 13/15 (87%) | Multiple-choice: choose which listed problems apply and write the answer letters. | A. The oracle's exact letter set. B. A near-miss set (one option too many/few). | A passes. B fails `count_answers` (Got 1) — wrong number of selected options. Oracle-only answer-selection, same family as `f1011`/`f1003-hard`; the deciding option has no local signal. |
| `ade-bench-f1003-hard` | 13/15 (87%) | Multiple-choice answer task (hard variant). | A. The oracle's exact letter set. B. A near-miss set. | A passes. B fails `count_answers` (Got 1). Oracle-only answer-selection (same family as `f1011`/`f1003`). Failed in h0012, h0050. |
| `ade-bench-f1005` | 17/20 (85%) | Fix `constructor_points.sql` because the `points` column is too high. | A. `max(points)` over cumulative standings to recover the season total. B. Select the latest/final standing row with date/rank logic (`standings_rank = 1`). | A passes. B looks like the final standing but fails edge cases where the latest row and max cumulative points differ. |
| `ade-bench-f1005-medium` | 16/19 (84%) | Fix wrong results in `constructor_points.sql`. | A. `max(points)`. B. latest/final-row rank logic. | A passes. B fails for the same max-vs-latest reason as `f1005`. |
| `ade-bench-f1006` | 11/21 (52%) | Fix too-high `points` in both `constructor_points.sql` and `driver_points.sql`. | A. Change cumulative `sum(points)` to `max(points)` in both models. B. Latest standings rows. C. Recompute from race results. | A passes (artifact-proven in h0044/h0050/h0051/h0052). B and C are locally plausible but diverge from the hidden grader's convention. |
| `ade-bench-f1006-hard` | 10/19 (53%) | Fix wrong results in both `constructor_points.sql` and `driver_points.sql`. | A. `max(points)` for cumulative standings. B. latest/rank path. | A passes. B failed in the h0037 full run on a two-row edge case. |
| `ade-bench-f1010-medium` | 11/15 (73%) | Create `analysis__lap_times` by track/year, accounting for pit stops. | A. Exclude pit-stop laps before averaging. B. Keep pit-stop laps but subtract pit-stop duration. | A passes. B sounds more precise but the hidden oracle expects exclusion, not subtraction. |
| `ade-bench-f1011` | 5/17 (29%) | Multiple-choice: which listed problems apply to the adjusted lap-time analysis; write the answer letters. | A. Answer `ADE`. B. Answer `ABDE`, because a local probe makes option B look supported. | A passes. B is the locally tempting wrong answer (`check_option_b` Got 1); reproduced across many draws. Lowest pass rate — passing is the minority outcome; the deciding option B is oracle-only. |
| `ade-bench-quickbooks002` | 34/36 (94%) | Remove the `using_department` variable/references; do not edit the Fivetran source package. | A. Remove the variable/reference while preserving the hidden expected output shape (e.g. retain a `department_name` placeholder/null where needed). B. Remove department columns entirely. | A passes. B is reasonable from the instruction but the hidden equality tests can fail with "has less columns than solution". |
| `ade-bench-quickbooks003` | 17/22 (77%) | (QuickBooks union/enhanced models.) | A. Emit the full solution column set on the union models. B. Drop columns from `int_quickbooks__*_union` / `ap_ar_enhanced`. | A passes. B triggers compile-time `AUTO_int_quickbooks__*_union_equality` "has less columns than solution" (width) errors. 5 failing runs; same width family as `quickbooks002`/`ana-eng003`. |
| `ade-bench-quickbooks004` | 19/21 (90%) | Add `using_exchange_rate=false` and hide converted amount/payment exchange-rate columns. | A. Apply the variable narrowly to hide exchange-rate columns, preserving the 48-check model shape. B. Broad double-entry / transaction-model refactor across many models. | A is safer. B looks like a complete cleanup but is fragile; in one full run it broke 5 of 48 QuickBooks checks. |

## Cross-Task Patterns

1. SQL convention choices:
   `COUNT(*)` vs `COUNT(column)`, `max(points)` vs latest standing row, excluding
   pit-stop laps vs subtracting pit-stop duration, and zero-group → NULL vs
   excluded/zeroed (`airbnb005`).

2. Width / "less columns" choices:
   a defensible column drop produces a compile-time "has less columns than solution"
   error. Shared by `ana-eng003` (dim_customer), `quickbooks002`/`quickbooks003`
   (union/enhanced), and the `airbnb007` second-model surface.

3. Oracle-only answer-selection family:
   `f1011`, `f1003`, `f1003-hard` are multiple-choice answer models checked by
   `count_answers` / `check_option_*`. The deciding option has no local signal, so the
   model coin-flips between letter sets across draws. These are the least bankable —
   no README lever can pin them (the solver-blind-to-oracle wall).

4. Scoring-surface choices:
   a repair can fix one scored model while the task is gated by another, as in
   `airbnb007` (`daily` vs `listing` agg).

5. Cleanup/refactor choices:
   the model often picks a broad cleanup defensible from the instruction, but the oracle
   expects the old output shape preserved more tightly (`asana003`, `quickbooks004`,
   `f1001` source-rewiring).

6. Attribution boundary:
   a green flip is not proof that the hypothesis caused the fix. `asana002` flipped, but
   not through the proposed cast lever (solver-native structural repair).

7. Lever-caused vs variance flip:
   exactly one task here (`airbnb008`) flipped because a *hypothesis lever fired where it
   should not have* (h0046's ungated coverage skeleton), not because of sampling variance.
   This is the distinction that separates a real regression-to-fix (gate the lever → h0050)
   from the noise-floor wobble that dominates every other row.

8. Trials-1 implication:
   under `trials: 1`, each locally plausible choice is sampled only once. That makes
   pass/fail movement look like task ability when it is often just one sampled branch of
   an ambiguous local decision. With ~19 volatile cells, a single full run loses ~3–4
   off-construct cells to this noise regardless of the lever — which is why artifact-real
   `+3` construct gains (h0051, h0052) keep netting back to a tie against the lucky-32
   baseline.

## Bottom Line

The 19 flipped tasks are best treated as a sensitivity set: they reveal where the
solver's local reasoning branches into multiple plausible repairs. Only
`ade-bench-airbnb009` (and, post-h0044, the `f1006`/`f1006-hard` `max(points)` repair)
has a strong, repeated, artifact-level lever signal — yet even those remain unbankable
at `trials: 1`, because each independent draw loses a different ~3 off-construct cells
to the noise floor. The three oracle-only answer tasks (`f1011`, `f1003`, `f1003-hard`)
are structurally un-leverable. The single lever-caused flip (`airbnb008`) has already
been addressed by gating (h0050). The remaining path to banking the real gains is a
measurement change (multi-trial on the volatile tail), not another README lever.
