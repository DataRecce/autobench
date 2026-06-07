---
id: h0034
title: Combined confirmation -- E2 anti-cross-join (airbnb009) + E3 rolling-window calendar-RANGE-copy (airbnb007) in ONE variant; full 48-task confirmation + promote
status: conclude
kind: hypothesis
source: _proposal/oracle-problem-systematic-program.md (E2+E3 batch-full, captain 2026-06-07); confirms h0019 (airbnb009 smoke-GO) + h0018 (airbnb007 smoke-GO) at full scale in ONE run (run-economy + interaction check); promote @baseline if the paired delta clears.
started: 2026-06-07T16:22:23Z
completed: 2026-06-07T23:43:44Z
verdict: REJECTED
score:
worktree: 
archived: 2026-06-07T23:43:44Z
---

## Hypothesis

*(Seeded by the FO; the propose stage builds the combined variant + FULL spec.)*

E2/h0019 (anti-cross-join, airbnb009) and E3/h0018 (rolling-window expressed as a calendar-date RANGE
copied from the project's own passing sibling, airbnb007) BOTH flipped their targets at smoke,
artifact-proven (the committed SQL carried the prescribed shape), with zero canary regression. Both
are independent single-rule **Implementation-stage** additions with copyable worked examples. This
combined variant carries BOTH rules and runs the **full 48-task confirmation in one run** (cheaper
than two separate fulls; also checks the two rules do not interact to harm passers) before promotion.

**Falsifiable claim:** the combined variant holds BOTH flips (airbnb007 + airbnb009 PASS) at full
48-task scale with zero NET regression; the paired `rk runs diff` delta vs `@baseline` clears the
tripwire (CI excludes a regression) on a clean strict audit; and `stratified_pass_at_1 > 0.6458`.
**Promote `@baseline`** on success. Falsified if either flip reverts at full (variance), if the two
rules interact to regress passers, or if the net delta does not clear.

This combined run **skips smoke** (both levers were already smoke-GO'd individually): `propose -> full`.

## Acceptance criteria

**AC-1 -- Combined variant README = baseline + EXACTLY the two Implementation rules.** The forked
README adds the h0019 anti-cross-join rule AND the h0018 rolling-window calendar-RANGE-copy rule
(both lifted VERBATIM from their smoke-GO forks `solver_workflows/h0019-*` and
`solver_workflows/h0018-*`), and nothing else; leak-guard + other stages byte-identical to
`codex-ade-dbt-minimal`. The FULL spec differs from `specs/baseline.yaml` only in `experiment:` +
`solver_workflow:` and carries NO `benchmark.tasks` selector (all 48). `kind: spacedock_solver`,
`runtime: codex`, `trials: 1` preserved.

**AC-2 -- Clean strict audit on the full run** (`tainted: 0`, `captured > 0` every cell).

**AC-3 -- Verdict by the paired `rk runs diff @baseline <run>` delta (CI, adjusted p) + absolute
`stratified_pass_at_1` vs 0.6458.** Promote only if the delta clears the tripwire AND both target
flips (airbnb007, airbnb009) hold artifact-proven AND no passer regressed.

## Gatekeeper review

**Recommendation: APPROVE** — confirmation/promote variant: two PREVIOUSLY-SMOKE-GO'd
Implementation rules (h0019 anti-cross-join + h0018 rolling-window calendar-RANGE) lifted
VERBATIM into ONE in-stage fork; leak-guard byte-identical; full spec two-field; clean combination.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T16:30:00Z.

Fork parent resolved: `source:` names `codex-ade-dbt-minimal` (seed); `rk registry resolve run
@baseline` → `runs/ade-bench-baseline/622bdedac572b479`, whose `solver_workflow` =
`solver_workflows/codex-ade-dbt-minimal` (content hash `133891fa…`). Both agree → `<parent-solver>`
= `codex-ade-dbt-minimal`, the dir forked and diffed against.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Diff vs parent adds only inside `## Stage: Implementation` (no `## Stage:` header in the diff; 4 stage headers in both parent and fork). **Confirmation variant:** intentionally carries TWO rules, but BOTH are previously-smoke-GO'd, BOTH live in the SAME Implementation stage, combined for run-economy + interaction check (per captain). Gate question = clean combination + leak-guard, not single-idea. |
| G2 leak-guard intact | PASS | Header/leak-guard lines 1–49 byte-identical to parent; grep over the 86 added lines finds none of AUTO_/solution__/check_option_/verifier/equality test/expected output seed/Got N/curl/wget/git clone/git ls-remote. |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0034-…yaml` shows only `experiment:` + `solver_workflow:`. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. NO `benchmark.tasks` (all 48). |
| G4 smoke tasks-only | N/A | No smoke spec — this run skips smoke (propose→full); both levers were smoke-GO'd individually (h0019 airbnb009, h0018 airbnb007). |
| G5 both frozen | PASS | `specs/h0034-…frozen.yaml` exists, carries `kind: spacedock_solver` + `runtime: codex`. No smoke frozen by design (skips smoke). |
| G6 resolver fidelity | PASS | Combined added-set is set-equal to (h0019 added 43 lines) ∪ (h0018 added 43 lines) = 86 lines, VERBATIM. Both rules are gated/generative-constructive derivations (how to build the SQL) with worked examples — neither is self-anchored "check your own work." Matches the claim (carry BOTH flips). |
| G7 actionability/inert-risk | PASS | Both rules carry a worked-example SQL skeleton (BEFORE/AFTER cross-join; WRONG/RIGHT rows-frame vs calendar-RANGE) — the copyable few-shot form, not abstract structural prose. Already smoke-proven to reach the committed artifact. |
| G8 regression-canary coverage | N/A | Both rules are GATED on narrow preconditions (h0019: completeness-repair carrying a secondary grouping column; h0018: a rolling "over last N days" window-suffixed column), not blanket-generative. Also a FULL 48-task run — all 48 ARE the panel; no smoke subset to under-cover. |
| G9 selector independence | N/A | No multi-candidate / selector protocol — two single-shot Implementation derivations. |
| G10 self-correcting false-positive | N/A | Neither rule is a verify-and-fix-on-disagreement lever; both are constructive Implementation derivations (build the SQL this shape), not reconcile-and-replace against a re-derived check. |

**For the captain:** No FAILs. This is a confirmation/promote variant, not a new idea — the two
rules read as independent, non-overlapping paragraphs (disjoint preconditions:
completeness-repair vs rolling-window column), both lifted byte-for-byte from their smoke-GO'd
forks. Decide: advance to the FULL 48-task run (skips smoke). The full run itself is the
interaction check (do the two rules harm any passer when both are live).

## Smoke result

## Run result

**DONE** (completed 2026-06-07T23:00Z; PID `2522572` exited). FULL 48-task confirmation, 1 trial/task.

- **Spec:** `specs/h0034-combined-e2-e3-full-confirmation.frozen.yaml` (all 48 tasks; `kind: spacedock_solver`, `runtime: codex`, `trials: 1`).
- **Run dir:** `runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303/` (48 task cells + `_razorback`).

### Strict audit (AC-2) — CLEAN
`rk audit … --policy strict` → `summary: {clean: 48, coverage_missing: 0, tainted: 0}`. All 48 cells clean, 0 tainted, 0 coverage-missing (captured everywhere). AC-2 PASS.

### Score (absolute, AC-3) — NO LIFT
`rk score --format json` → `stratified_pass_at_1 = 0.6458333…` (31/48), `stratified_n_completed: 48`, `n_errored: 0`. **Exactly equal to @baseline 0.6458** — zero absolute lift. Fails `stratified_pass_at_1 > 0.6458`.

### Paired ledger vs @baseline (`runs/ade-bench-baseline/622bdedac572b479`), slug-paired
`rk runs diff` TypeErrors on ade-bench run-dirs (`int(query_id)` with `query_id: null` — known issue), so paired by slug from `trial_name` (strip `__SUFFIX`, drop `ade-bench-` prefix) over `per_trial_outcomes.json`. 48/48 slugs paired, no orphans.

- **baseline:** 31/48 pass · **h0034:** 31/48 pass · **observed paired mean delta = +0.0000** (abs net = **+0**)
- **GAINS (2):** `airbnb009` 0→1 · `f1011` 0→1
- **REGRESSIONS (2):** `asana003` 1→0 · `f1005` 1→0
- **Targets:** `airbnb009` 0→1 (E2 HELD, artifact-proven) · **`airbnb007` 0→0 (E3 REVERTED)**
- 29 same-pass, 15 same-fail.

| Direction | Slug | Base | h0034 | Mechanism (artifact-proven) |
|-----------|------|------|-------|------------------------------|
| GAIN (E2 target) | airbnb009 | 0 | 1 | `apply_patch` on `models/agg/mom_agg_reviews.sql`: date-spine filter `WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE…)` → `WHERE DATE_ACTUAL BETWEEN (MIN…) AND (MAX…)`. The anti-cross-join / full-calendar-range completeness shape the E2 rule prescribes. Post-fix: 4,508 aggregation dates (was 3,786). |
| GAIN (incidental) | f1011 | 0 | 1 | Not a target; flipped by solver variance (the two rules don't touch F1 results model). |
| REGRESSION (canary) | asana003 | 1 | 0 | Runtime Error building `asana__daily_metrics`: `Conversion Error: invalid date field "None"` — solver re-wired staging models to `var('task')`/`var('project')` (asana fivetran-package wiring) and a column resolved to literal `'None'` flowing into a `date_diff(cast('None' as date)…)`. **Rule-independent** — neither rule touches asana staging; gpt-5.5 wiring non-determinism (baseline wired it clean). |
| REGRESSION | f1005 | 1 | 0 | `AUTO_constructor_points_equality` off by 2 rows: solver rewrote `constructor_points.sql` from `SUM(points) GROUP BY name,season` to last-round cumulative standings via `QUALIFY row_number() over (… order by round_number desc)=1` — a wrong points interpretation for 2 constructor-seasons. **Rule-independent** — no date-spine/rolling-window/cross-join; gpt-5.5 semantic non-determinism (baseline picked the SUM interpretation). |

### Paired bootstrap (AC-3) — TRIPWIRE NOT CLEARED
10k paired bootstrap over the 48 per-task deltas (seed 20260607): **95% CI on mean delta = [-0.0833, +0.0833]** = **[-4, +4] tasks** — straddles 0, does **not** exclude a regression. Observed delta +0.0000. The do-no-harm tripwire requires the CI to exclude a regression; it does not. **AC-3 FAILS** on all three legs: net non-positive, CI includes regression, and one target flip (airbnb007) reverted.

### airbnb007 (E3) revert — diagnosis
**The rolling-window calendar-RANGE copy DID reach the SQL this run** — `daily_agg_nps_reviews.sql` was written with a 28-day rolling RANGE (`LEFT JOIN daily_reviews windowed ON windowed.review_date BETWEEN dateadd('day',-27,dates.review_date) AND dates.review_date`), and `daily_agg_nps_reviews_equality_with_tolerance` **PASSED**. The reward is 0 because a **different** scored model, `listing_agg_nps_reviews` (per-listing lifetime NPS total, no rolling window), failed `listing_agg_nps_reviews_equality_with_tolerance` by **2 rows** (`Got 2 results`). The E3 rule's precondition (a rolling "over last N days" column) does not match `listing_agg`, so the rule never fires there. **The h0018 smoke-GO was variance on `listing_agg`, not a real fix of the rolling window — the h0012/f1006 multi-model pattern: a target whose verdict is gated by a model the lever doesn't address.**

## Behavioral analysis

The 5 required analyze questions:

**1. Net + ledger (both directions).** Net = **+0** (2 gains − 2 regressions). `stratified_pass_at_1 = 0.6458 = @baseline` exactly; paired bootstrap 95% CI [-4, +4] tasks straddles 0. GAINS: `airbnb009` 0→1 (E2 target, artifact-proven), `f1011` 0→1 (incidental variance). REGRESSIONS: `asana003` 1→0 (build error in `asana__daily_metrics`), `f1005` 1→0 (constructor-points semantic rewrite off by 2). Both regressions are damage to passers and are **rule-independent** (neither E2 nor E3 touches asana staging or F1 constructor points).

**2. Smoke vs full — why airbnb007 reverted.** E2/airbnb009 held smoke→full (real fix, the same date-spine completeness mechanism reaches the same `mom_agg_reviews` edit). E3/airbnb007 reverted: at smoke (h0018) the listing-level model happened to score green; at full it failed by 2 rows. The rolling-window-copy **did** reach the SQL this run (`daily_agg_nps_reviews` carried the 28-day RANGE and its test PASSED) — but airbnb007's verdict is gated by a *second* model, `listing_agg_nps_reviews` (lifetime NPS, no rolling window), which the E3 rule's precondition never matches. So the h0018 smoke-GO was variance on the unaddressed model, exactly the **h0012/f1006 pattern**: a multi-model target whose pass/fail flickers on a model the lever does not touch.

**3. Already-correct-and-broken (per regression).** `asana003`: baseline built `asana__daily_metrics` cleanly (PASS); this run the solver's staging re-wiring produced a `'None'` literal in a date column → `cast('None' as date)` Runtime Error → cascade FAILs. `f1005`: baseline computed constructor points as `SUM(points) GROUP BY name,season` (correct); this run the solver reinterpreted them as last-round cumulative standings (`QUALIFY row_number()… order by round_number desc =1`), wrong for 2 constructor-seasons. In both, the baseline was correct and the new run broke it — but via solver non-determinism on models with no E2/E3 precondition, not via the rule text.

**4. Was-the-change-executed (committed-artifact check).** GAIN `airbnb009`: YES — `apply_patch` (exit 0, `M models/agg/mom_agg_reviews.sql`) replaced the `IN (DISTINCT review dates)` spine filter with `BETWEEN MIN..MAX`, the E2 full-calendar-range shape; full-refresh succeeded; post-fix 4,508 dates. REVERTED target `airbnb007`: the E3 shape WAS executed in `daily_agg_nps_reviews` (28-day RANGE self-join, test passed) — execution confirmed, but on the wrong model relative to the failing test. REGRESSION `asana003`: only one `apply_patch`, and it edited `dbt_packages/asana_source/models/stg_asana__*` (staging re-wiring) — it did **not** touch `asana__daily_metrics`, confirming the build error is downstream of a solver wiring change, not a rule edit. REGRESSION `f1005`: the `apply_patch` rewrote only `models/stats/constructor_points.sql`, with no date-spine/rolling/cross-join token — confirming rule-independence.

**5. Prevention + next move.** Prevention: (a) the **multi-model-target trap** — before crediting a single-model lever (E3) with a target flip, check ALL scored models for that task; airbnb007 has two NPS models and E3 only addresses one, so a single smoke-GO can't be trusted. Encode this in the propose gatekeeper (G8-style: enumerate the target's scored models; if the lever's precondition matches fewer than all, treat a single-run flip as variance, require a repeat or a wider lever). (b) **gpt-5.5 base variance** is large enough (CI ±4 tasks at n=48, trials=1) to manufacture ±2 incidental flips per run independent of any lever — confirms the variance-caution lesson; single-trial fulls cannot distinguish a +1 real lever from noise. Next move: do **NOT** promote @baseline. E2/airbnb009 is a real, artifact-proven fix and is worth re-running ALONE (its own clean full, or trials>1) so its +1 is not masked by unrelated variance; airbnb007/E3 should be REJECTED as a target flip (variance on the unaddressed `listing_agg` model) unless re-scoped to a lever that addresses the per-listing model too.

## Verdict

**REJECTED as a promote candidate (NO-PROMOTE).** Net = +0 on a clean strict audit; `stratified_pass_at_1 = 0.6458` = @baseline (no absolute lift); paired bootstrap 95% CI [-4, +4] tasks straddles 0 (does not exclude a regression); and one target flip (airbnb007/E3) reverted. Two passers regressed (`asana003`, `f1005`) — a do-no-harm tripwire violation — both via rule-independent gpt-5.5 non-determinism. The one real signal is **E2/airbnb009** (artifact-proven anti-cross-join calendar-range fix in `mom_agg_reviews.sql`); E3/airbnb007 is **variance, not a fix** (the rolling-window-copy reached `daily_agg` and passed, but the verdict is gated by the unaddressed `listing_agg` model — the h0012/f1006 multi-model pattern). Recommend to the FO/captain: do not promote; consider an E2-only re-confirmation (alone, or trials>1) to recover the real +1 without the offsetting noise.

## Stage Report: propose

- DONE: Combined variant fork = codex-ade-dbt-minimal + EXACTLY the two Implementation rules lifted VERBATIM
  `solver_workflows/h0034-combined-e2-e3-full-confirmation/README.md`; combined added-set is set-equal to (h0019 added 43 lines) ∪ (h0018 added 43 lines) = 86 lines; both rules inside `## Stage: Implementation` (h0019 anti-cross-join + worked example before "Run basic confirmation", h0018 rolling-window calendar-RANGE + worked example after it); header/leak-guard lines 1–49, Exploration, Validation, Finalization all byte-identical to parent; no AUTO_*/solution__*/Got N tokens.
- DONE: FULL spec specs/h0034-…yaml differs from baseline.yaml ONLY in experiment: + solver_workflow:, NO benchmark.tasks (all 48); frozen via rk freeze --allow-missing
  `diff specs/baseline.yaml specs/h0034-…yaml` = the two fields only; `kind: spacedock_solver`/`runtime: codex`/`trials: 1` preserved; `specs/h0034-…frozen.yaml` written (`tasks: null` = all 48). No smoke spec (run skips smoke).
- DONE: Gatekeeper ran; ## Gatekeeper review block written (per-rule PASS/WARN/FAIL + overall)
  APPROVE, no FAILs; G1 = two PREVIOUSLY-SMOKE-GO'd rules combined for confirmation, G2 leak-guard byte-identical, G3 spec two-field; G4/G8/G9/G10 N/A (no smoke / gated rules / no selector / not self-correcting). Fork parent resolved to `codex-ade-dbt-minimal` (source + @baseline registry agree).

### Summary

Built the combined confirmation variant (h0034) by forking `codex-ade-dbt-minimal` and lifting the two already-smoke-GO'd Implementation rules VERBATIM into one fork: h0019's anti-cross-join rule (airbnb009) and h0018's rolling-window calendar-RANGE-copy rule (airbnb007), each with its worked-example skeleton, both inside `## Stage: Implementation` with disjoint preconditions (completeness-repair vs rolling-window column) so they read as two independent, non-interacting rules. Set-diff confirms the combined additions = union of the two source forks' additions, byte-for-byte; everything outside Implementation is byte-identical to the parent. Built and froze ONLY the FULL 48-task spec (two-field delta vs baseline, no task selector, no smoke spec — this run goes propose→full since both levers were smoke-GO'd individually). Gatekeeper recommendation: APPROVE (no FAILs). Propose STOPS at the gate — no `rk run` launched; the FULL run is the next stage.

## Stage Report: full

- DONE: The FULL 48-task run is LAUNCHED DETACHED on specs/h0034-combined-e2-e3-full-confirmation.frozen.yaml: nohup, stdout/err -> /tmp/rk-h0034-full.log, PID -> /tmp/rk-h0034-full.log.pid; confirm it actually started (run dir + first cell/image-build underway). Record run-dir + PID in ## Run result (mark 'in progress').
  Run dir `runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303/`, PID `2522572` (alive). First cell `ade-bench-airbnb001__Dmadk6o` image built (`ade-bench-airbnb001__dmadk6o-main:latest`, in use); `job.log` shows agent bootstrap (NVM/node 22 + `@openai/codex@latest`). `--explain` resolved the combined README cleanly. `## Run result` marked IN PROGRESS.
- DONE: Report the run-dir path + PID + that the run is in progress, then STOP. Do NOT poll/hold for the ~7-hour duration -- the FO adopts the completed run for audit + score + analyze.
  Launch-only assignment honored: no audit/score launched (run not done); no second run launched; stopping after this commit + completion signal.

### Summary

Launched the FULL 48-task confirmation run for the combined E2+E3 variant detached via `nohup` after a clean `--explain` sanity check. The run is in progress: run dir `runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303/`, PID `2522572` (alive), log `/tmp/rk-h0034-full.log`. First cell (airbnb001) image is built and the codex agent bootstrap is underway in `job.log`. Per the assignment I did NOT poll/hold for the ~7 h duration and did NOT run audit/score — the FO adopts the completed run for the strict audit + score + paired `rk runs diff` + promote decision.

## Stage Report: analyze

- DONE: Strict audit + score on the COMPLETED run dir (tainted:0, captured>0 across all 48 cells) + absolute stratified_pass_at_1 vs @baseline 0.6458. Recorded in ## Run result.
  `rk audit --policy strict` → `{clean:48, coverage_missing:0, tainted:0}`; `rk score --format json` → `stratified_pass_at_1 = 0.6458` (31/48, n_completed 48, n_errored 0) = @baseline exactly (no lift).
- DONE: FULL per-task ledger vs @baseline (622bdedac572b479), paired by slug, BOTH directions; paired delta + 10k bootstrap; confirm airbnb009 HELD and airbnb007 REVERTED; name every changed verdict.
  `rk runs diff` TypeErrors on `int(query_id=null)` (known issue) → slug-paired from per_trial_outcomes.json. Net +0: GAINS airbnb009 (E2, artifact-proven `mom_agg_reviews.sql` BETWEEN-spine), f1011 (incidental); REGRESSIONS asana003 (build error `asana__daily_metrics` cast('None')), f1005 (constructor-points QUALIFY rewrite off-by-2). 10k bootstrap 95% CI = [-4,+4] tasks, straddles 0. airbnb007 reverted: rolling-window-copy DID reach `daily_agg` (passed) but verdict gated by unaddressed `listing_agg` (off by 2) — h0012/f1006 multi-model pattern.
- DONE: Answer the 5 required analyze questions + a clear PROMOTE/NO-PROMOTE recommendation.
  All 5 answered in ## Behavioral analysis; ## Verdict = NO-PROMOTE / REJECTED as a promote candidate. Net non-positive, CI includes a regression, E3 target reverted, two passers regressed (do-no-harm violation). Both regressions rule-independent gpt-5.5 variance. Only real signal = E2/airbnb009 (artifact-proven); recommend E2-only re-confirmation (alone or trials>1) to recover the +1 without offsetting noise.

### Summary

Combined E2+E3 full 48-task confirmation: clean strict audit (0 tainted), but NET = +0 and `stratified_pass_at_1 = 0.6458` = @baseline exactly. airbnb009 (E2 anti-cross-join) HELD and is artifact-proven — the committed `mom_agg_reviews.sql` swaps the `IN(DISTINCT review dates)` spine filter for `BETWEEN MIN..MAX` (3,786→4,508 dates). airbnb007 (E3 rolling-window) REVERTED: the 28-day RANGE copy reached `daily_agg_nps_reviews` and that test passed, but airbnb007's verdict is gated by `listing_agg_nps_reviews` (a per-listing lifetime NPS model the E3 precondition never matches), which failed by 2 rows — variance on the unaddressed model, the h0012/f1006 multi-model pattern. Two passers regressed (`asana003` build error, `f1005` constructor-points rewrite), both rule-independent gpt-5.5 non-determinism. Paired bootstrap 95% CI [-4,+4] straddles 0. **Recommendation: NO-PROMOTE.** Note for the FO/taxonomy: encode the multi-model-target trap (a single-model lever must check ALL of a target's scored models before a flip is credited) and re-confirm whether the lesson belongs in the instruction-lever taxonomy note vs verification-without-oracle artifact.

## Stage Report: conclude

- DONE: Write the END-OF-PROGRAM RETROSPECTIVE to hypotheses/_proposal/retrospective-2026-06-07.md (honest accounting, methodological findings, dead-family map, method deliverables, recommended next moves)
  `_proposal/retrospective-2026-06-07.md` written: §1 honest accounting (@baseline UNCHANGED 31/48; E1-E4+combined netted +0; airbnb009 the ONE genuine fix, unpromoted due to variance), §2 the variance wall + multi-model-target trap, §3 dead-family map (grain construct/reconcile, cast, candidate-gen/arbitration all EXHAUSTED), §4 method deliverables (E0 instrument-gate, correlated-error-via-shared-filter, green-but-inert/attribution, worked-example-decisive, multi-model trap), §5 next moves to close toward 75%, §6 plain-words bottom line.
- DONE: Finalize the cross-experiment records — bug-type-taxonomy.md (airbnb009 real fix; airbnb007 multi-model; multi-model-target trap) + WORKFLOW-REFINE.md (combined-full methodology + single-trial-variance-masking)
  bug-type-taxonomy.md: airbnb009 per-task row + board #1b marked FIXED-by-h0019; airbnb007 per-task row + board #4 marked MULTI-MODEL/REJECTED; new "multi-model-target trap" section; per-type lessons updated for #1b (win) + #4 (revert). WORKFLOW-REFINE.md: new ledger entry "Combined-full confirmation methodology + the single-trial-variance-masking wall (h0034)" with the variance-wall + freeze-repo-race + multi-model trap learnings.
- DONE: h0034 ## Verdict = REJECTED (NET +0, paired CI [-4,+4] straddles 0, no promote); append ## Stage Report: conclude; do NOT set verdict frontmatter / do NOT archive
  ## Verdict already records "REJECTED as a promote candidate (NO-PROMOTE)" (net +0, CI [-4,+4], airbnb007 reverted, 2 passers regressed). Frontmatter untouched; not archived (FO performs terminal frontmatter + archive).

### Summary

End-of-program synthesis for the oracle-problem program (E0-E4 + combined full). The honest finding: `@baseline` is UNCHANGED at 31/48 — the whole flip portfolio netted +0. airbnb009 (E2/h0019) is the ONE genuine, artifact-proven fix (held smoke→full) but is UNPROMOTED because single-trial variance (paired CI ±4 tasks > a +1 signal) masked it in the combined full. The deliverable is the METHOD: the variance wall (a real +1 cannot be banked at trials=1; the freeze-repo race blocks trials>1), the multi-model-target trap (airbnb007 needs 2 scored models; a single-model lever can't credit the flip), the dead-family map (grain construct/reconcile, cast, candidate-gen/arbitration all exhausted/oracle-blocked), the method deliverables (E0 instrument-gate, correlated-error-via-shared-filter, green-but-inert, worked-example-decisive), and a concrete path to 75% (fix the freeze-repo race → multi-trial E2-only re-confirm; re-triage Track Z; source 6th/7th targets; add a multi-model-target gate check). Retrospective at `_proposal/retrospective-2026-06-07.md`; cross-experiment records (bug-type-taxonomy.md, WORKFLOW-REFINE.md) finalized. NO promote — combined full did not clear. FO performs terminal frontmatter + archives.
