---
id: h0018
title: Output Contract — record a rolling 'over last N days' figure as a calendar-date RANGE copied from the project's own existing rolling-window model, not as N preceding rows
status: conclude
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type Tolerance-band divergence (*_equality_with_tolerance) — root-caused on airbnb007 (daily_agg_nps_reviews) as a date-grain / rolling-window CONSTRUCTION error - a per-day aggregate keyed on actually-occurring review_dates with a rolling 'over last 28 days' figure, NOT a numeric-formula error); realizes the new Output Contract stage. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed: 2026-06-07T23:43:44Z
verdict: REJECTED
score:
worktree: 
archived: 2026-06-07T23:43:44Z
---
## Hypothesis

The baseline value-divergence re-audit flagged `airbnb007` (`daily_agg_nps_reviews_equality_with_tolerance`, `Got 4` — all four numeric columns `nps_daily` / `reviews_daily` / `nps_28d` / `reviews_28d` outside the `0.01` band) while the sibling `listing_agg_nps_reviews` PASSED. I re-root-caused this directly against the delivered workspace and the verifier test SQL, and it is NOT a numeric-formula bug — it is a date-grain / rolling-window CONSTRUCTION bug, and one piece of it is recoverable from a concrete copyable local artifact:

- **The tolerance test aggregates `sum`/`avg` of the four numeric columns + `min/max(review_date)` + a `total_rows` check** (read the test template directly: `numeric_cols = ['nps_daily','reviews_daily','nps_28d','reviews_28d']`, `sum_tolerance = avg_tolerance = 0.01`). So a wrong grain (extra/missing days) shifts the sum/avg of *every* column, and a wrong 28-day window directly mis-sets the sum/avg of `nps_28d`/`reviews_28d`.
- **Grain is the set of actually-occurring review dates, not a padded calendar spine.** The solution daily output has 3,786 data rows and its early dates are *sparse* (`2009-06-20`, then `2009-08-18`, then `2009-11-25` — not consecutive days), proving one row per day-that-has-a-review, recoverable locally as `select count(distinct review_date) from <filtered reviews>`.
- **The rolling 28-day figure is a calendar-date RANGE, and the project ALREADY implements that exact shape.** The workspace's own `models/agg/mom_agg_reviews.sql` computes a trailing window by left-joining the date spine to reviews on `review_cte.REVIEW_DATE::DATE BETWEEN dates_cte.DATE_ACTUAL::DATE - 29 AND dates_cte.DATE_ACTUAL::DATE` (a 30-day calendar RANGE, with the comment "joining by last 30 days range"). The 28-day window the daily model needs is the same construction with `29` → `27` — a copy-and-change-the-interval substitution, not a re-derivation.

The seed solver's prose tells it to "create the models described in the schema.yml" and to "check ... grain ... row counts ... against source data," but nothing points it at the project's own rolling-window sibling as the window template, and nothing names the calendar-RANGE-vs-N-preceding-rows hazard. The `@baseline` solver produced a daily aggregate whose 28d column magnitudes diverge — a wrong window mechanism on a sparse per-day grain.

**Re-framing (FO, 2026-06-07).** The `@baseline` solver `codex-ade-dbt-minimal` has **no Output Contract stage** — its only stages are Exploration / Implementation / Validation / Finalization (verified by `grep '^## Stage:'` of the parent README), and the new-Output-Contract-stage family was REJECTED/inert (h0017/h0023) and skips repair tasks. So the original framing ("extend grain rule (1) of the new `## Stage: Output Contract`") is **non-executable**. The clause is therefore placed in the **Implementation** stage as a mechanical copy-the-sibling worked-example rule — the same concrete shape that just landed E2/airbnb009 (a worked BEFORE/AFTER SQL skeleton in Implementation, h0019). This is an **in-stage Implementation tweak, not a structural workflow change** (so the workflow-refinement log is N/A).

**Falsifiable claim (the single README change — one new Implementation-stage rule + worked example):** adding to `## Stage: Implementation` one window clause — *when a model computes a rolling 'over last N days' figure (a window-suffixed column like `_28d`, or an instruction asking for a trailing-window total per period), express the window as a calendar-date RANGE relative to each row's date and COPY the window-join shape verbatim from the project's own existing rolling-window sibling (e.g. a `*mom*` aggregate that left-joins the spine on `source_date BETWEEN current_date - (N-1) AND current_date`), changing only the interval length; never express it as a fixed `rows between (N-1) preceding and current row` frame, which assumes one row per calendar day and mis-counts on a sparse per-period grain* — carried with a copyable BEFORE/AFTER SQL worked example (the `rows between` frame as WRONG, the `mom_agg_reviews` `BETWEEN current_date - 29 AND current_date` join changed to `- 27` as RIGHT) — will move the committed `daily_agg_nps_reviews` SQL to the correct calendar-RANGE window and grain, narrowing or clearing the `airbnb007` tolerance failure and raising `stratified_pass_at_1` above the `@baseline` 0.6458.

**Why this escapes the dead-prose ceiling.** The rejected grain levers (h0010 prose, h0016 skeleton) asked the solver to *restructure* SQL in the moment of writing it and were acknowledged-but-not-executed; h0011 asked for a column set the local workspace did not contain (premise falsified). This lever is different on the one axis that has ever mattered (the asana002 win under h0009): it is a **mechanical, copyable, in-place substitution anchored to a concrete local artifact that already exists in the same project** — `mom_agg_reviews.sql`'s `BETWEEN ... - 29 AND ...` join. The instruction is "copy this sibling's window join and change 29 to the N your model needs," not "reason your way into the right frame." It is placed in the **Implementation** stage as a worked BEFORE/AFTER SQL skeleton (the asana002-style mechanical/few-shot form, the one form that has ever moved committed SQL on this `@baseline`), not as abstract restructuring prose. It deliberately does NOT claim to recover the within-tolerance *value targets* or the exact window *length* (those live only in the hidden solution seed; the model name `_28d` is the only local cue for N) — so this is filed as a **completeness, low-leverage construction-side bet**, honest about the h0011 blind-to-oracle ceiling, not a high-confidence flip.

**Distinct from existing coverage.** h0012 covers the same target from the **Validation** stage (post-build numeric reconcile) — a different stage and a post-hoc control point; this prevents the divergence at BUILD time inside the **Implementation** stage. It is distinct from the prior Implementation grain levers (h0010 prose / h0016 entity-spine worked example), which address the entity-spine 'do not narrow / build one-row-per-entity' case; this adds the orthogonal rolling-window calendar-RANGE-vs-N-preceding-rows hazard. It carries **no calendar-spine ban** — the earlier candidate's no-spine rule was dropped because it would actively harm `airbnb009` (whose instruction literally asks for "a row for every day ... some days are missing" — i.e. MORE spine) and conflict with the project convention; `airbnb009` is therefore NOT a target here.

Method/README change only. Forks the current `@baseline` solver (`solver_workflows/codex-ade-dbt-minimal`, runtime codex) and adds the one rule to its existing `## Stage: Implementation`; no dataset, harness, or solver-runtime change. Leak-guard intact (references only the project's own sibling model + a `count(distinct date)` probe of local source — no public fetch, no oracle, no reference to hidden `AUTO_*` / `solution__*` / `_with_tolerance` / `_equality` tests). Spec differs from baseline only in `experiment:` + `solver_workflow:` (smoke adds only `benchmark.tasks`).

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h<NNNN>-contract-rolling-window-calendar-range.yaml` shows only `experiment:` + `solver_workflow:`; the README diff vs the `codex-ade-dbt-minimal` parent is a SINGLE pure-addition hunk inside the `## Stage: Implementation` block (the rolling-window clause + its BEFORE/AFTER worked example), leaves Exploration/Validation/Finalization and the leak-guard/dependency-package prose (lines ~1-49) byte-identical, and references no hidden `AUTO_*` / `solution__*` / `_with_tolerance` / verifier tests. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean (`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta (CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean audit AND `stratified_pass_at_1 > 0.6458`. Because the within-tolerance values and exact window length for `daily_agg_nps_reviews` are not locally derivable, the load-bearing smoke signal is the per-target flip on `airbnb007` plus zero regression on the canary panel — NOT the smoke-panel mean.

**Smoke gate:** on the single target `ade-bench-airbnb007` plus the cross-family `@baseline`-passer canaries `ade-bench-airbnb001` / `ade-bench-ana-eng001` / `ade-bench-asana001` / `ade-bench-f1007` / `ade-bench-quickbooks002` (this rule is generative — it fires on every authoring task that has a rolling-window column — so per gatekeeper G8 it carries one passing canary from each non-target family; intercom supplies no canary because it has no `@baseline` passer), the variant must hold every canary PASS and should move `airbnb007`'s committed `daily_agg_nps_reviews` SQL to the copied calendar-RANGE window (verify the committed apply_patch payload contains a `BETWEEN <date> - 27 AND <date>`-style join lifted from `mom_agg_reviews`, and check the `Got N` distance vs `@baseline` — do not trust transcript chatter) before any promotion to full.

## Gatekeeper review

**Recommendation: APPROVE** — single Implementation-stage worked-example rule, leak-guard byte-identical, spec scope clean; one WARN: the airbnb family that shares the target's rolling-window construct carries only one canary (G8), and inert-risk is non-zero given the prior grain levers (G7).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T14:10Z.
Fork parent resolved: `source:` forks `solver_workflows/codex-ade-dbt-minimal`; `@baseline` (runs/ade-bench-baseline/622bdedac572b479) `spec.frozen.yaml` solver_workflow = `solver_workflows/codex-ade-dbt-minimal` — agree.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Diff is one pure-addition hunk `63a64,106` (43 added, 0 removed) falling entirely between `## Stage: Implementation` (L50) and `## Stage: Validation` (L107); one idea: rolling-window = calendar-RANGE-copied-from-sibling. |
| G2 leak-guard intact | PASS | Lines 1-33 (no-external-reference + dependency/package prose) byte-identical to parent; added lines contain no `AUTO_*`/`solution__*`/`_with_tolerance`/`_equality`/`check_option`/`verifier`/`Got N`/`curl`/`wget`/`git clone`/`http` tokens (grep clean). |
| G3 spec two fields | PASS | `diff baseline.yaml h0018…yaml` = only `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff full smoke` = only an added `benchmark.tasks` block; all 6 IDs `ade-bench-`-prefixed; the hypothesis's named target `ade-bench-airbnb007` is present. |
| G5 both frozen | PASS | `h0018…frozen.yaml` (1727B) + `…smoke.frozen.yaml` (1866B) both exist; both carry `kind: spacedock_solver` + `runtime: codex`; smoke frozen lists all 6 tasks. |
| G6 resolver fidelity | PASS | Inserted text = the claim verbatim in spirit: calendar-date RANGE copied from the project's own `*mom*` sibling, change only the interval; never `rows between`. Generative construction rule (tells the solver how to BUILD), not self-anchored "check your own work". No scope creep. |
| G7 actionability/inert-risk | WARN | Carries a worked-example BEFORE/AFTER SQL skeleton (the asana002-style mechanical/few-shot form) → not the pure-abstract-prose G7 flags. But it is still a *window-mechanism* change (`rows between` → date-RANGE join) on the same grain/SQL-shape axis the prior grain levers (h0010 0/4, h0016) found inert at gpt-5.5/xhigh. Inert-risk noted; the worked example is the mitigation. |
| G8 regression-canary coverage | WARN | Generative (fires on any task with a rolling-window column). Panel carries ≥1 `@baseline` passer from every non-target family that HAS one: ana-eng001 / asana001 / f1007 / quickbooks002 (intercom has 0/3 passers → no canary possible, correctly omitted). NOT FAIL (every available family is covered). WARN: the **airbnb** family shares the target's rolling-window construct yet carries only ONE canary (airbnb001); G8 wants ≥2 *perturbable* airbnb passers (e.g. another airbnb agg with a window column) so the smoke can catch a break in a *different* airbnb member than the one picked (the h0012 −4 failure mode). |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — single generative construction rule. |
| G10 self-correcting false-positive | N/A | Not a check / reconcile / validate-and-fix lever; it instructs how to CONSTRUCT the window, with no "verify a result and act on disagreement" step. |

**For the captain:** No FAILs → advisory APPROVE; you may advance to smoke. Two things to weigh before the spend: (1) **G8 WARN** — only one airbnb canary guards the construct-sharing family; the panel will catch a *target* regression but is blind to a break in another airbnb rolling-window passer. Optionally add a 2nd perturbable airbnb passer to the smoke `benchmark.tasks` (REVISE-class, idea unchanged) to harden the canary panel. (2) **G7 WARN** — same window/grain axis the prior grain levers found inert; the decisive smoke read is the *committed* `daily_agg_nps_reviews.sql` (does it use a `BETWEEN <date> - 27 AND <date>` calendar-RANGE join lifted from `mom_agg_reviews`, not `rows between … preceding`?) plus the `Got 4` distance vs `@baseline` — inert ⇒ NO-GO per the capped one-shot.

## Smoke result

**GO — artifact-proven flip, zero canary regression.** Run dir: `runs/ade-bench-h0018-contract-rolling-window-calendar-range/72b3c0a6d7ac9f05` (gpt-5.5@xhigh, trials:1).

**Strict audit (clean):** `rk audit --policy strict` → `tainted: 0`, `clean: 6`, `coverage_missing: 0` (coverage captured for every cell, no taint findings). **Score:** `rk score` → `stratified_pass_at_1 = 1.0` (6/6 PASS), Wilson CI [0.610, 1.0], above the `against_constant` 0.1875 and above `@baseline` 0.6458.

| Task | Role | @baseline | h0018 variant | Delta |
|------|------|-----------|---------------|-------|
| ade-bench-airbnb007 | TARGET | FAIL (Got 4) | **PASS** | **flip +1** |
| ade-bench-airbnb001 | canary (airbnb family) | PASS | PASS | hold |
| ade-bench-ana-eng001 | canary | PASS | PASS | hold |
| ade-bench-asana001 | canary | PASS | PASS | hold |
| ade-bench-f1007 | canary | PASS | PASS | hold |
| ade-bench-quickbooks002 | canary | PASS | PASS | hold |

Paired smoke-panel delta vs `@baseline` on these 6 slugs: 5/6 → 6/6 (+1), the single moving cell being the named target `airbnb007`; 5/5 canaries held PASS (all 5 were `@baseline` passers, reward=1). No canary regression.

**Got-N distance (target):** `@baseline` `daily_agg_nps_reviews_equality_with_tolerance` = **FAIL 4** (`Got 4 results, configured to fail if != 0` — all four numeric cols outside the 0.01 band). h0018 variant = **PASS** (Got 0; full test suite 11/11 PASS). The oracle distance cleared completely, not merely narrowed.

**ARTIFACT PROOF (the decisive read — committed `daily_agg_nps_reviews.sql`, read from the `Add File` apply_patch payload in the airbnb007 cell session rollout, NOT transcript chatter):**

- `@baseline` committed model (WRONG, rows-based frame):
  `SUM(COALESCE(R.NPS_SCORE_DAILY,0)) OVER (ORDER BY D.REVIEW_DATE ROWS BETWEEN 27 PRECEDING AND CURRENT ROW) AS NPS_SCORE_28D` — a `ROWS BETWEEN 27 PRECEDING` frame that counts ROWS on the sparse per-day grain, spanning far more than 28 calendar days.
- h0018 variant committed model (RIGHT, calendar-date RANGE lifted from the `*mom*` sibling shape):
  `LEFT JOIN daily_reviews AS review_28d ON review_28d.review_date BETWEEN current_day.review_date - INTERVAL '27 day' AND current_day.review_date` — the `BETWEEN <date> - 27 AND <date>` calendar-RANGE window the hypothesis predicted (the `mom_agg_reviews` `BETWEEN current_date - 29 AND current_date` shape with the interval changed to 27). The 28d totals are computed by `SUM(review_28d.reviews_daily)` / `SUM(review_28d.promoters_daily - detractors_daily)` over that join.

The variant's committed model is a single `Add File: models/daily_agg_nps_reviews.sql` patch; a regex scan of both airbnb007 session rollouts found **zero** added (`+`) lines containing `rows between … preceding` (the only `rows between` text in the rollout is the README worked-example prompt echo). The window mechanism flipped from rows-between-preceding to a copied calendar-date RANGE exactly as the lever predicted, and `Got 4 → PASS` moved with it. Both GO conditions (artifact-proven window-copy + Got-4 movement) are banked on the artifact, not on the non-deterministic reward alone.

## Run result

**FULL confirmation carried in the combined E2+E3 run (h0034), NOT a standalone full.** Per the program,
E3/h0018 was confirmed at full inside `h0034-combined-e2-e3-full-confirmation` (run
`runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303/`, clean strict audit `tainted:0`,
`trials:1`).

- **airbnb007 REVERTED at full: 0→0 (no flip).** The smoke-GO did NOT hold.
- **The rolling-window calendar-RANGE copy DID reach the SQL** — the committed `daily_agg_nps_reviews.sql`
  carried the 28-day rolling RANGE (`LEFT JOIN daily_reviews windowed ON windowed.review_date BETWEEN
  dateadd('day',-27,dates.review_date) AND dates.review_date`) and `daily_agg_nps_reviews_equality_with_tolerance`
  **PASSED**. The lever's mechanism is artifact-proven to land.
- **The task still scored 0 because a SECOND scored model failed.** airbnb007's verdict is gated by
  `listing_agg_nps_reviews` (per-listing lifetime NPS total, NO rolling window), whose
  `listing_agg_nps_reviews_equality_with_tolerance` failed by 2 rows (`Got 2`). The E3 rule's precondition
  (a rolling "over last N days" column) never matches `listing_agg`, so the lever cannot fire there.

**Diagnosis — the multi-model-target trap (the h0012/f1006 pattern).** airbnb007 is scored by TWO models;
the E3 lever addresses only the rolling-window one. The h0018 smoke-GO was **variance on the unaddressed
`listing_agg` model**, not a real fix of the rolling window. A single-model lever cannot credit a flip on a
target scored by ≥2 models when it matches only one. (Compounded by single-trial variance — see
`_artifacts/WORKFLOW-REFINE.md` combined-full entry + `_proposal/retrospective-2026-06-07.md` §2.2.)

## Behavioral analysis

### Full revert (E3, via h0034)

**The rolling-window calendar-RANGE-copy MECHANISM is sound but INSUFFICIENT for this target.** At full the
copy reached `daily_agg_nps_reviews` and that test passed — the construction lever works exactly as the
smoke proved. But airbnb007 is a MULTI-MODEL target: its second scored model `listing_agg_nps_reviews`
(lifetime per-listing NPS, no window) is outside the lever's precondition and failed by 2 rows, so the task
verdict stayed FAIL. The smoke flip was variance on that unaddressed model — the h0012/f1006 multi-model
pattern. This is the live reason the lever cannot be credited with the flip, distinct from inertness
(it is NOT inert — it landed) and distinct from correlated error.

### Smoke analysis (retained — the mechanism IS real)

**The lever fired exactly as designed, and on the one axis that has ever mattered on this `@baseline`.** The hypothesis was filed as a low-confidence completeness bet because the prior grain levers (h0010 prose 0/4, h0016 entity-spine skeleton) were acknowledged-but-not-executed at gpt-5.5/xhigh — the G7 inert-risk WARN. The differentiator claimed was the asana002-shape: a mechanical, copyable, in-place substitution anchored to a concrete local artifact already present in the same project (`mom_agg_reviews.sql`'s `BETWEEN … - 29 AND …` join), delivered as a BEFORE/AFTER worked example in the Implementation stage rather than abstract restructuring prose. The committed SQL confirms the solver did precisely the copy-and-change-the-interval the worked example prescribed: it built the 28d columns from a `BETWEEN current_day.review_date - INTERVAL '27 day' AND current_day.review_date` self-join, not a `rows between` window function. This is the second confirmed instance (after the asana002 win under h0009) that a mechanical copyable worked example anchored to a local sibling moves committed SQL where restructuring prose does not.

**Grain handling came along for free.** The model groups `daily_reviews` by `review_date` from `fct_reviews` (one row per day-that-has-a-review), matching the sparse 3,786-row actually-occurring-dates grain the solution uses — no calendar-spine padding. The full tolerance test (which also checks `sum`/`avg` of all four numeric cols + `min/max(review_date)` + `total_rows`) passed, so both the grain and the window are within the 0.01 band: `INSERT 3786` rows matches the solution seed exactly.

**Honest scope of the win.** This is a single-trial smoke under non-deterministic gpt-5.5@xhigh. The GO is banked on the committed-artifact proof (the calendar-RANGE join is in the file) plus the Got-4→PASS movement, NOT on the reward being deterministically reproducible. The hypothesis explicitly did NOT claim to recover the within-tolerance value targets or the exact window length (those live only in the hidden solution seed; `_28d` was the only local cue for N=28) — yet the solver inferred N=28 from the column name and landed inside tolerance. That is a stronger result than the filed completeness bet, but full-scale variance is the open question for the `full` stage: the construct is generative (fires on any rolling-window column), so the airbnb-family canary coverage (G8 WARN: only airbnb001 guards the construct-sharing family) should be watched at full scale for a break in a different airbnb member.

## Verdict

**REJECTED (E3 — airbnb007 reverted at full + multi-model target).** The rolling-window calendar-RANGE-copy
**mechanism itself is sound** — at full (via the combined run h0034) the committed `daily_agg_nps_reviews.sql`
carried the 28-day calendar-RANGE self-join lifted from the `mom_agg_reviews` sibling and
`daily_agg_nps_reviews_equality_with_tolerance` PASSED, artifact-proven exactly as the smoke predicted — **but
it is insufficient for this target.** airbnb007's verdict is gated by a SECOND scored model,
`listing_agg_nps_reviews` (per-listing lifetime NPS total, NO rolling window), which the E3 rule's
precondition never matches and which failed by 2 rows (`Got 2`) at full. airbnb007 therefore reverted 0→0.
**The h0018 smoke-GO was variance on the unaddressed `listing_agg` model, not a real fix of the rolling
window — the h0012/f1006 multi-model-target trap.** A single-model rolling-window lever cannot satisfy a
target scored on two models when it addresses only one.

The smoke GO (artifact-proven window-copy on `daily_agg`, zero canary regression) remains a genuine
demonstration that the worked-example calendar-RANGE-copy form reaches the committed SQL — it is the second
confirmation of the worked-example-decisive lever family (after airbnb009/h0019), and that mechanism is
banked as a method deliverable. But airbnb007 as a *target* is not winnable by this single-model lever; a
flip would require a lever that also addresses the per-listing `listing_agg` model, or `trials>1` to
distinguish the smoke flip from variance. **No promote.** Cross-refs: `bug-type-taxonomy.md` (#4 + the
multi-model-target trap), `_artifacts/WORKFLOW-REFINE.md` (combined-full entry),
`_proposal/retrospective-2026-06-07.md` §2.2.

(In-stage Implementation tweak; the methodology/variance learning is recorded in WORKFLOW-REFINE — the
lever mechanism itself is not a structural workflow change.)

## Stage Report: propose

- DONE: Forked README adds ONE IMPLEMENTATION-stage rule (rolling 'over last N days' = calendar-date RANGE COPIED from the project's own `*mom*` rolling-window sibling, change only the interval; never `rows between (N-1) preceding and current row`), with a copyable BEFORE/AFTER SQL worked example.
  Diff `solver_workflows/codex-ade-dbt-minimal → h0018` is one pure-addition hunk `63a64,106` (43 added, 0 removed) entirely between `## Stage: Implementation` (L50) and `## Stage: Validation` (L107); WRONG=`rows between 27 preceding`, RIGHT lifts `mom_agg_reviews` `BETWEEN dates_cte.DATE_ACTUAL::DATE - 29 …` changed to `- 27`.
- DONE: Exploration/Validation/Finalization + leak-guard byte-identical to parent; no hidden AUTO_*/solution__*/_with_tolerance/_equality/Got N tokens.
  Lines 1-33 (leak-guard) and 34-63 (Exploration + Impl-prefix) byte-identical; Validation+Finalization tail identical shifted +43; forbidden-token grep over added lines clean.
- DONE: Full spec differs from baseline ONLY in `experiment:` + `solver_workflow:`; smoke adds ONLY `benchmark.tasks` = airbnb007 (target) + airbnb001/ana-eng001/asana001/f1007/quickbooks002 (G8 panel, no intercom passer); both frozen via `rk freeze --allow-missing`; kind=spacedock_solver/runtime=codex/trials=1 preserved.
  `diff baseline.yaml h0018.yaml` = 2 fields; `diff full smoke` = only `benchmark.tasks`; `h0018…frozen.yaml` + `…smoke.frozen.yaml` both present with kind/runtime intact.
- DONE: Gatekeeper ran; `## Gatekeeper review` block written (per-rule PASS/WARN/FAIL incl. G7 worked-example + G8 panel) + overall APPROVE.
  10-rule table appended; overall APPROVE (no FAILs); WARNs on G7 (window/grain inert-risk axis) and G8 (only one airbnb canary on the construct-sharing family).
- DONE: Entity body Hypothesis/claim updated to the IMPLEMENTATION-stage framing (dropped 'Output Contract stage' wording — baseline has no such stage).
  Added FO re-framing note; rewrote Falsifiable claim, "Why this escapes", "Distinct from existing coverage", the method line, and AC-1 to reference `## Stage: Implementation` + the worked example.
- SKIPPED: Launch any rk run.
  Propose STOPS at the gate per dispatch — no smoke/full launched.

### Summary

Re-framed h0018 from the non-executable "extend the new Output Contract stage" (the `@baseline` solver `codex-ade-dbt-minimal` has no such stage) into a single Implementation-stage worked-example rule: a rolling 'over last N days' figure must be a calendar-date RANGE copied verbatim from the project's own `*mom*` sibling's `BETWEEN current_date - (N-1) AND current_date` join (change only the interval), never a `rows between (N-1) preceding and current row` frame that mis-counts on a sparse per-day grain. Forked the solver, built + froze full and smoke specs (smoke = target airbnb007 + 5 cross-family canaries; intercom omitted, 0/3 passers), and recorded an advisory APPROVE gatekeeper review with WARNs on G7 (same window/grain axis prior grain levers found inert) and G8 (only one airbnb canary guards the construct-sharing family). No rk run launched — gate stops here for the captain's decision.

## Stage Report: smoke

- DONE: Strict audit + score recorded for the ALREADY-COMPLETED run.
  `rk audit --policy strict` on runs/ade-bench-h0018-contract-rolling-window-calendar-range/72b3c0a6d7ac9f05 → tainted:0, clean:6, coverage_missing:0; `rk score` → stratified_pass_at_1=1.0 (6/6), above @baseline 0.6458. Results in ## Smoke result.
- DONE: Per-target deep-dive on airbnb007 — oracle distance Got 4 cleared and improvement is ARTIFACT-PROVEN.
  Committed `daily_agg_nps_reviews.sql` (from the `Add File` apply_patch payload in the airbnb007 cell rollout) uses `LEFT JOIN … ON review_28d.review_date BETWEEN current_day.review_date - INTERVAL '27 day' AND current_day.review_date` — the calendar-date RANGE lifted from `mom_agg_reviews` (29→27), NOT `rows between … preceding` (zero added `rows between … preceding` lines in either rollout). @baseline used `ROWS BETWEEN 27 PRECEDING`; daily test FAIL 4 → PASS. All 5 canaries (airbnb001/ana-eng001/asana001/f1007/quickbooks002) were @baseline passers and held PASS — zero regression.
- DONE: Plain-words go/no-go written to ## Smoke result + reported. CAPPED: one smoke, no iteration.
  GO: airbnb007 flips FAIL→PASS with the calendar-RANGE window artifact-proven in committed SQL AND zero canary regression. Gate routing ⇒ full.

### Summary

The h0018 smoke run (PID already exited; no new run launched) is a clean GO. Strict audit clean (tainted:0, coverage_missing:0), score 6/6 (stratified_pass_at_1=1.0). The named target airbnb007 flipped FAIL→PASS: its committed `daily_agg_nps_reviews.sql` expresses the 28-day window as a calendar-date RANGE (`BETWEEN <date> - INTERVAL '27 day' AND <date>`, the `mom_agg_reviews` sibling shape with the interval changed), replacing the @baseline `ROWS BETWEEN 27 PRECEDING` frame, and the `daily_agg_nps_reviews_equality_with_tolerance` test went FAIL 4 → PASS (11/11). Window-mechanism flip is artifact-proven from the apply_patch payload, not transcript chatter; all 5 canaries held PASS (zero regression). Gate: flip + zero canary regression ⇒ advance to full. In-stage Implementation tweak ⇒ workflow-refinement-log N/A.

## Stage Report: conclude

- DONE: h0018 ## Verdict = REJECTED (airbnb007 reverted at full + multi-model target the single-model rolling-window rule cannot fully satisfy; mechanism sound but insufficient)
  ## Verdict rewritten from the smoke "GO → advance to full" to REJECTED: at full (via h0034) the calendar-RANGE copy reached `daily_agg_nps_reviews` and that test PASSED (mechanism artifact-proven), but airbnb007's verdict is gated by a SECOND model `listing_agg_nps_reviews` (no rolling window, failed by 2 rows) the E3 precondition never matches → reverted 0→0. The smoke-GO was variance on the unaddressed model (h0012/f1006 multi-model pattern).
- DONE: ## Run result + ## Behavioral analysis updated with the full revert (carried in h0034), the multi-model-target diagnosis, and the retained smoke mechanism
  ## Run result records the full revert via run `1880d6497bdd6303` (daily_agg passed, listing_agg failed); ## Behavioral analysis adds a "Full revert (E3, via h0034)" section (mechanism sound, multi-model insufficient) above the retained smoke analysis.
- DONE: Append ## Stage Report: conclude; do NOT set verdict frontmatter / do NOT archive
  This report appended; frontmatter untouched; not archived (FO performs terminal frontmatter + archive).

### Summary

E3/h0018 concluded REJECTED. The rolling-window calendar-RANGE-copy MECHANISM is sound — at full (carried in the combined run h0034) the committed `daily_agg_nps_reviews.sql` carried the 28-day calendar-RANGE self-join lifted from the `mom_agg_reviews` sibling and its test PASSED, artifact-proven exactly as the smoke predicted. But airbnb007 is a MULTI-MODEL target: its verdict is also gated by `listing_agg_nps_reviews` (per-listing lifetime NPS, no rolling window), which the lever's precondition never matches and which failed by 2 rows at full, so airbnb007 reverted 0→0. The h0018 smoke-GO was variance on the unaddressed `listing_agg` model — the h0012/f1006 multi-model-target trap. The mechanism is banked as the second confirmation of the worked-example-decisive lever family (after airbnb009/h0019); the target itself needs a wider lever or trials>1. No promote. The multi-model-target trap + variance learnings are recorded in bug-type-taxonomy.md and WORKFLOW-REFINE.md; full synthesis in `_proposal/retrospective-2026-06-07.md`. FO performs terminal frontmatter + archive.
