# Subagent Decision-Fork Probe Method

Date: 2026-06-10

This note records the cheap pre-smoke method used to test whether solver README wording
changes the model's choice at a known local decision fork. It is a proxy for decision policy,
not a substitute for `rk smoke`.

## Purpose

Some ADE tasks do not fail because the model cannot find any plausible fix. They fail because
the local workspace admits multiple reasonable fixes, while the hidden grader accepts only
one convention. A full `rk run` is expensive when the question is narrower:

> Given the visible task context and a proposed solver README rule, which branch would the
> model choose at this fork?

The subagent probe answers that narrower question quickly. It helps decide whether a README
wording is worth promoting to real smoke.

## Method

1. Pick one concrete decision fork.
   Use prior run forensics to identify the exact local ambiguity, for example
   `COUNT(*)` vs `COUNT(review_date)`.

2. Build a clean prompt.
   Include only visible information the solver would have: task instruction, relevant model
   SQL, visible schema/tests if they are part of the workspace, and sibling models. Do not
   include hidden verifier output, solution files, previous run outcomes, expected totals, or
   our conclusion about which branch is correct.

3. Define rule variants.
   At minimum compare a weak baseline wording against the proposed wording. If useful, test a
   stronger wording too. Keep the task context identical across variants so the only intended
   variable is the README rule.

4. Spawn fresh subagents.
   Use `fork_context=false`. Instruct each subagent not to use tools, not to inspect the repo,
   not to edit files, and to answer only from the supplied context. This keeps the probe from
   leaking our current conversation or hidden run knowledge into the decision.

5. Require machine-classifiable output.
   Ask for compact JSON with a small enum such as:

   ```json
   {
     "variant": "B",
     "count_choice": "COUNT(*)|COUNT(review_cte.REVIEW_DATE)|other|unclear",
     "patch_summary": "...",
     "reason": "..."
   }
   ```

6. Classify only the decision.
   The output is not a dbt build, not a verifier result, and not a pass/fail claim. Count only
   whether the subagent chose the desired branch, the undesired branch, some other branch, or
   was unclear.

7. Treat results as a gate to smoke, not a replacement for smoke.
   A strong result (for example 10/10 choosing the desired branch) means the wording is worth
   real `rk` validation. It does not prove the full solver workflow will find the bug, patch it
   correctly, or pass the hidden grader.

## Worked Example: airbnb009

Decision fork: after repairing the `mom_agg_reviews` date spine, should the solver preserve
the existing `COUNT(*)` or change it to `COUNT(review_cte.REVIEW_DATE)`?

Prompt inputs:

- Task instruction: "In mom_agg_reviews, there should be a row for every day..."
- `mom_agg_reviews.sql`, especially `dates_cte` and `final_cte`
- Relevant sibling models: `daily_agg_reviews.sql`, `wow_agg_reviews.sql`
- `dim_dates` span and `fct_reviews` visible filter
- No hidden date-range test, no previous run pass/fail, no expected totals

Variants tested:

| Variant | Rule | Kept `COUNT(*)` | Chose column-count |
|---|---|---:|---:|
| A | Weak "smallest local change / prefer siblings" rule | 0/2 | 2/2 |
| B | Coverage repair preserves metric semantics | 2/2 | 0/2 |
| C | Strong COUNT guard + final self-audit | 2/2 | 0/2 |

Follow-up B-only probe:

| Variant | Runs | Kept `COUNT(*)` | Chose `COUNT(review_cte.REVIEW_DATE)` | Other / unclear |
|---|---:|---:|---:|---:|
| B | 10 | 10 | 0 | 0 |

Interpretation: the B wording materially changed the model's local decision policy in this
proxy. It moved the observed wrong-choice rate from 2/2 under the weak rule to 0/12 under the
coverage-repair rule. This supports filing h0042, but h0042 still needs real focused `rk`
smoke.

## Worked Example: asana002

Decision fork: on an Asana package-update task, should the solver treat the failure as a
structural package migration where tag/task-tag resources became optional, or as a
representation/type-cast problem?

Prompt inputs:

- Task instruction: "This project is erroring because Fivetran updated their Asana package..."
- Visible package vars such as `asana__using_tags` and `asana__using_task_tags`
- `asana__task.sql` unconditionally depending on task-tag intermediates and tag fields
- `int_asana__task_tags.sql` unconditionally referencing tag/task-tag staging models
- `asana__tag.sql` depending on tag staging and task-tag metrics
- No hidden equality tests, no previous run outcomes, no solution files

Calibration with disabled-resource compile error included:

| Variant | Rule | Optional-resource gating | Cast / seed / broad-copy |
|---|---|---:|---:|
| A | Weak baseline-style "smallest task-relevant change" | 2/2 | 0/2 |
| B | Package-update optional-resource rule | 2/2 | 0/2 |
| C | Strong matrix + no-cast guard | 2/2 | 0/2 |

Pre-diagnostic prompt without compile error:

| Variant | Runs | Chose `vars_disabled_compile_matrix` | Chose optional-resource gating | Cast / seed / broad-copy |
|---|---:|---:|---:|---:|
| A | 2 | 2 | 2 | 0 |
| B | 2 | 2 | 2 | 0 |
| C | 2 | 2 | 2 | 0 |

Follow-up B-only pre-diagnostic probe:

| Variant | Runs | Chose `vars_disabled_compile_matrix` | Chose optional-resource gating | Cast / seed / broad-copy |
|---|---:|---:|---:|---:|
| B | 10 | 10 | 10 | 0 |

Interpretation: B has strong proxy support, **14/14** across both B batches. However,
weak A also selected the desired branch in **4/4** probes when the visible tag-var context
was present. The value of B is therefore less about overturning an otherwise-wrong local
choice and more about making the diagnostic and patch shape explicit enough to verify in
real `rk` smoke. The real smoke must confirm committed optional-resource gating in
`asana__task.sql`, `int_asana__task_tags.sql`, and `asana__tag.sql`, and must reject a green
result caused by an unrelated cast or raw seed edit as green-but-inert.

## Probe Map For The Remaining 11 Flipped Tasks

For each task, the probe should hide the observed oracle result from the subagent. The
"preferred branch to measure" below is for the operator's classifier, not text to reveal as
"the correct answer" in the subagent prompt.

| Task | Local decision fork to simulate | Prompt context to include | Preferred branch to measure |
|---|---|---|---|
| `ade-bench-airbnb007` | Calendar-date rolling range vs `ROWS BETWEEN`; also whether fixing only one scored model is enough. | Task instruction, `daily_agg_nps_reviews`, `listing_agg_nps_reviews`, sibling rolling-window SQL, visible schema. | Calendar date-range logic, plus explicit scan for every model named/scored by the task. |
| `ade-bench-asana002` | Package-migration structural optional tags vs representation/type-cast patch. | Task instruction, package vars, staging/intermediate models around task tags, visible package README/schema snippets. | Structural package migration / conditional tag handling, not an inert cast-only patch. |
| `ade-bench-asana003` | Conservative tmp-model repoint preserving tmp semantics vs broad source-var rewrite and tmp deletion. | Task instruction, tmp models, target `stg_asana__*` models, visible schema/type expectations. | Conservative repoint that preserves tmp layer type/value behavior. |
| `ade-bench-f1005` | `max(points)` over cumulative standings vs latest/final standing row. | Task instruction, `constructor_points.sql`, standings source/model SQL, any visible season/constructor grain docs. | `max(points)` if local evidence says points are cumulative. |
| `ade-bench-f1005-medium` | Same max-vs-latest fork as `f1005`. | Same context as `f1005`, but with the medium task instruction. | `max(points)` if local evidence says points are cumulative. |
| `ade-bench-f1006` | Apply cumulative-points logic to both constructor and driver models vs latest-row or recompute-from-race-results path. | Task instruction, both `constructor_points.sql` and `driver_points.sql`, standings/race source SQL, visible schema. | Consistent cumulative-standing aggregation across both models. |
| `ade-bench-f1006-hard` | Same max-vs-latest fork across both constructor and driver point models. | Same context as `f1006-hard`: both point models and standings source models. | `max(points)` if local evidence says points are cumulative. |
| `ade-bench-f1010-medium` | Exclude pit-stop laps before averaging vs subtract pit-stop duration and keep pit-stop laps. | Task instruction, lap-time model, pit-stop source/model, any visible wording about "account for pit stops". | Exclusion only if local evidence supports "remove contaminated laps"; otherwise classify branch. |
| `ade-bench-f1011` | Answer letters `ADE` vs `ABDE`, especially whether option B is truly supported. | Task instruction/options, current analysis SQL, visible local probes only. | Require explicit local evidence per letter; classify whether B is included or rejected. |
| `ade-bench-quickbooks002` | Remove department variable/reference while preserving output shape vs delete department columns entirely. | Task instruction, package vars, models containing department fields, visible schema/contracts. | Preserve column shape unless visible evidence says the output contract changed. |
| `ade-bench-quickbooks004` | Narrow `using_exchange_rate=false` column hiding vs broad double-entry/transaction refactor. | Task instruction, project vars, models with exchange-rate/converted amount columns, visible schema/contracts. | Narrow column hiding with minimal model-shape preservation. |

## Result Template

Use this table when recording a probe:

| Variant | Runs | Preferred branch | Undesired branch | Other / unclear | Notes |
|---|---:|---:|---:|---:|---|
| A |  |  |  |  |  |
| B |  |  |  |  |  |
| C |  |  |  |  |  |

Then write the interpretation in two layers:

- Proxy result: the observed decision rate inside the subagent simulation.
- Required real validation: the smallest focused `rk` smoke that would verify the same branch
  in committed artifacts.

## Caveats

- This method estimates local decision tendency, not pass rate.
- It is sensitive to prompt leakage. Do not include "hidden-correct" labels, expected totals,
  or prior pass/fail outcomes.
- It is sensitive to task-context selection. If the real solver would discover a file that the
  probe omits, the proxy may understate or overstate the branch probability.
- Repeated subagents are not a statistical substitute for `trials > 1`; they are cheap
  pre-smoke evidence for whether a README wording is worth running.
- A positive probe should lower the cost of deciding what to smoke. It should not skip audit,
  scoring, or committed-artifact inspection in the real run.
