---
id: h0042
title: Coverage repair preserves metric semantics -- when fixing missing rows/date spines, do not change COUNT/SUM/AVG/window definitions unless visible project evidence says the metric itself is wrong
status: propose
kind: hypothesis
source: Captain request 2026-06-10 after Round 2 airbnb009 COUNT(*) vs COUNT(review_date) decision-fork analysis; follows h0019 banking failure and the Round 1 + Round 2 flipped-task choice map. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-10T06:32:33Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`airbnb009` exposed the new Round-2 bankability failure: the solver repeatedly reached the
right local bug location in `mom_agg_reviews` -- the `dates_cte` date spine is narrowed to
days that already have direct reviews -- but one unpinned implementation degree of freedom
still decides the hidden result. Passing runs kept the existing aggregate expression
`COUNT(*)`; the failed standalone h0019 full run made a locally reasonable semantic cleanup
to `COUNT(review_cte.REVIEW_DATE)` so synthetic no-review rows counted as 0. Local date
coverage checks cannot distinguish those choices.

**Falsifiable claim (the single solver-README change -- Implementation policy only):** adding
a general "coverage repair preserves metric semantics" rule will reduce the solver's
wrong-choice rate on this decision fork. When a task is about missing rows, row coverage,
date-spine coverage, or join coverage, the solver must first treat the fix as a coverage
repair and must not change aggregate metric definitions (`COUNT`, `SUM`, `AVG`, window
expressions, business-rule filters) unless the task instruction, existing schema/tests, or
sibling model evidence explicitly says the metric definition itself is wrong. If local
validation passes after the coverage repair, preserve the existing metric semantics.

**The single proposed README text (B variant):**

```text
When the task is about missing rows, date-spine coverage, row coverage, or join
coverage, treat the fix as a coverage repair first. Do not change metric
definitions such as COUNT, SUM, AVG, window expressions, or business-rule filters
unless the task instruction, schema, visible project tests, or sibling model
evidence explicitly says that metric definition is wrong. If local validation
passes after the coverage repair, preserve the existing metric semantics.
```

This is intentionally not task-specific. It does not say "`airbnb009` should keep
`COUNT(*)`." It supplies a general tie-breaker for locally ambiguous repairs:
coverage fixes should not silently become metric-definition rewrites.

**Why this differs from h0019.** h0019 correctly steered the solver toward the date-spine
repair and away from category overproduction, but it did not pin the aggregate line. The
solver therefore had two locally defensible paths after restoring the date spine:

- minimal coverage repair: keep the existing `COUNT(*)`;
- semantic cleanup: change to `COUNT(review_cte.REVIEW_DATE)` so no-review rows count as 0.

The h0019 standalone full failure shows that "found the bug" is not enough at `trials: 1`
when the remaining free line controls the hidden check. h0042 aims to pin the general
decision policy, not the per-task answer.

**Pre-smoke subagent decision-fork evidence (proxy, not a score result).** Before filing this
hypothesis, we ran a controlled subagent decision probe. Each subagent received only the
visible task instruction, the local `mom_agg_reviews.sql`, relevant sibling SQL, and one
solver-rule variant. They were explicitly told not to inspect the repo, not to use tools,
and not to use hidden tests, verifier output, prior runs, or solution files.

Calibration probe:

| Variant | Rule | Kept `COUNT(*)` | Chose column-count |
|---|---|---:|---:|
| A | Weak "smallest local change / prefer siblings" rule | 0/2 | 2/2 |
| B | Coverage repair preserves metric semantics | 2/2 | 0/2 |
| C | Strong COUNT guard + final self-audit | 2/2 | 0/2 |

Follow-up B-only probe:

| Variant | Runs | Kept `COUNT(*)` | Chose `COUNT(review_cte.REVIEW_DATE)` | Other / unclear |
|---|---:|---:|---:|---:|
| B | 10 | 10 | 0 | 0 |

Total B evidence from the two probe batches: **12/12 kept `COUNT(*)`**. The observed proxy
wrong-choice rate for B is 0/12, versus 2/2 wrong for the weak A rule. This is not a real
`rk run` and must not be promoted as pass-rate evidence, but it is a strong preliminary
signal that the README wording changes the solver's local decision policy at the exact fork.

**Falsification path.** h0042 fails if, in fresh real `rk` runs on `ade-bench-airbnb009`, the
committed SQL still changes the aggregate metric definition while performing the date-spine
coverage repair, or if it preserves `COUNT(*)` but fails to reach the date-spine repair at all.
It also fails if the generic rule causes regressions on already-passing canaries by making the
solver over-conservative where a metric definition really did need to change.

**Target dataset.** Primary target: `ade-bench-airbnb009`. This is the one task where the
decision fork and the intended tie-breaker are artifact-proven. The expected movement is not
"discover a new task"; it is "make the already-discovered airbnb009 repair reproducible by
removing the free metric-semantics branch."

**Proposed smoke design.** Because the claim is a probability/decision-policy claim, the first
smoke should be a focused repeated single-cell smoke, not an all-48 run:

1. Create the h0042 solver README and specs in propose as usual.
2. Run `ade-bench-airbnb009` as independent focused smoke repeats (three sequential
   one-task runs, each fresh context / no freeze-CAS reuse).
3. For each run, inspect the committed `models/agg/mom_agg_reviews.sql` and classify:
   `COUNT(*)`, `COUNT(review_cte.REVIEW_DATE)`, other metric rewrite, or no date-spine repair.
4. GO only if at least 2/3 runs both preserve `COUNT(*)` and pass the verifier on clean strict
   audit. A 3/3 result is the desired signal. Any column-count recurrence is a NO-GO for the
   current wording.

If the workflow requires a single ordinary smoke spec first, use `ade-bench-airbnb009` plus
the h0019 canary panel (`airbnb001`, `asana001`, `ana-eng001`, `f1007`, `quickbooks002`);
then follow with sequential focused repeats before any full run. The canaries must stay pass,
but the decisive h0042 read is the committed aggregate choice on `airbnb009`.

**Scope.** Solver README only. No benchmark, runtime, model, sampling, trials, or spec-shape
change. Leak guard remains intact; the proposed README rule references only visible task
instructions, visible schema/tests, sibling models, and local SQL. It does not mention hidden
oracle totals, hidden test names, expected row counts, solution files, or verifier output.

## Gatekeeper review

**Recommendation: APPROVE** — single Implementation-stage policy block, B-variant text verbatim,
leak-guard byte-identical, specs differ only in the allowed fields; both WARNs (G7 inert-risk,
G8 same-family perturbability) are advisory and do not block the gate.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-08). Reviewed 2026-06-10T08:40:00Z.
Fork parent resolved: `source:` names `solver_workflows/codex-ade-dbt-minimal`; `rk registry resolve run @baseline` → `runs/ade-bench-baseline/622bdedac572b479` whose solver_workflow is the same seed dir — they agree.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff` vs parent = one hunk, `55a56,62`, 6 prose lines + blank, all under `## Stage: Implementation`; exactly one idea (coverage-repair preserves metric semantics); no other stage touched. |
| G2 leak-guard intact | PASS | Leak-guard paragraphs (lines 1-32) and dependency guardrails byte-identical to parent; token scan over added lines: no `AUTO_*`/`solution__*`/`check_*`/`verifier`/`equality test`/`expected output`/`Got N`/`curl`/`wget`/`git clone`/web/fetch. |
| G3 spec two fields | PASS | `diff baseline.yaml h0042…yaml` = only `experiment:` and `solver_workflow:` (lines 2 and 11); `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0042…yaml …smoke.yaml` adds only `benchmark.tasks`; all 6 slugs `ade-bench-` prefixed; includes the named target `ade-bench-airbnb009`. |
| G5 both frozen | PASS | `…frozen.yaml` (1733 B) + `…smoke.frozen.yaml` (1872 B) present; both carry `kind: spacedock_solver` + `runtime: codex` + `trials: 1`. |
| G6 resolver fidelity | PASS | Inserted text is the hypothesis's B variant word-for-word (collapsed-whitespace string-match confirmed). Generative-independent tie-breaker (preserve existing metric / abstain from rewrite), NOT a self-anchored re-run-your-own-model check — none of the dead h0006/h0007/h0008 phrasings present. |
| G7 actionability/inert-risk | WARN | Classify: abstract preference/abstain prose ("treat as coverage repair first; do not change COUNT/SUM/AVG…"), no worked-example SQL skeleton. NOT a structural FROM/spine/join rewrite, so it dodges the primary G7 inert mode, but it is still prose the solver could acknowledge-and-skip. Pre-smoke 12/12-kept-`COUNT(*)` proxy is preliminary only, not a score. Inert-risk noted for the captain. |
| G8 regression-canary coverage | PASS (WARN) | Generative (fires on any coverage-repair task). Smoke panel carries one `@baseline` passer per non-target family: airbnb001 / asana001 / ana-eng001 / f1007 / quickbooks002 (each reward=1.0 in 622bdedac572b479; no intercom canary exists — family has no passer). WARN: the family sharing the target's construct (airbnb) carries only ONE canary (airbnb001), and a date-spine/COUNT coverage rule may perturb a *different* airbnb passer than airbnb001 (the h0012 −4 lesson). G8 wants ≥2 perturbable same-family canaries; mitigated because this is a FLIP-SEEKER whose decisive read is the airbnb009 committed artifact, and the focused-repeat smoke + canary panel both run. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol. |
| G10 self-correcting false-positive | N/A | The lever is the *inverse* of a self-correcting check: it instructs the solver to PRESERVE the existing metric and NOT author a second derivation or reconcile-and-fix. No verify-then-act-on-disagreement mechanism, no re-derived independent CTE, no "replace with a different path" mandate — none of G10's failure axes apply. |
| G11 multi-model-target risk | N/A | Target `airbnb009` is scored by a SINGLE model (`mom_agg_review_date_range`, per `_artifacts/bug-type-taxonomy.md` line 36), distinct from the multi-model airbnb007 trap. Lever reaches the only scored model. |

**For the captain:** Clean APPROVE — all integrity rules (G2/G3/G6) PASS, no FAILs. Two advisory WARNs to weigh at the smoke gate: (1) G7 — the rule is abstract abstain-prose with no worked-example skeleton, so judge by the committed `mom_agg_reviews.sql` aggregate expression, not transcript chatter (AC-3); the 12/12 proxy is NOT pass-rate evidence. (2) G8 — only one airbnb same-family canary (airbnb001); a coverage/COUNT rule could perturb a different airbnb passer the smoke never runs, so watch full-scale airbnb regression if promoted. The decisive read remains the airbnb009 focused-repeat committed artifact (AC-4: ≥2/3 preserve `COUNT(*)` + date-spine repair + verifier pass + clean strict audit).

## Acceptance criteria

**AC-1 -- Exactly one README policy change; specs differ only in allowed fields.**
Verified at propose by diffing the h0042 solver README against
`solver_workflows/codex-ade-dbt-minimal/README.md`: one Implementation policy block added,
leak-guard prose byte-identical, no hidden-test/solution/verifier references. Full spec
diff vs `specs/baseline.yaml` shows only `experiment:` and `solver_workflow:`; smoke spec
adds only `benchmark.tasks`.

**AC-2 -- Every score is paired with strict clean audit and captured traces.**
Each `rk score` must cite `rk audit --policy strict` on the same run-dir with
`tainted: 0`, `coverage_missing: 0`, and captured agent traces.

**AC-3 -- Decision-policy evidence is artifact based.**
For every focused `airbnb009` run, read the committed SQL artifact, not the transcript
narration. Classify the actual aggregate expression in `mom_agg_reviews.sql`, whether the
date-spine coverage repair landed, and whether any metric definition changed. Transcript
claims such as "kept semantics" do not count without the committed SQL.

**AC-4 -- h0042 is promoted only if it reduces the known fork.**
Promotion requires fresh-run evidence that the solver reliably chooses the minimal coverage
repair path: preserve the existing aggregate metric expression while repairing the date spine.
The minimum smoke bar is 2/3 independent `airbnb009` focused runs with `COUNT(*)` preserved,
date-spine repair landed, verifier pass, and clean strict audit. 3/3 is the target.

**AC-5 -- No regression canary loss.**
If the smoke includes canaries, all baseline passers must remain pass. Any canary regression
is a NO-GO unless artifact analysis proves it is unrelated single-trial variance and the
captain explicitly accepts that risk.

## Stage Report: propose

- DONE: Fork the current @baseline solver into `solver_workflows/h0042-coverage-repair-preserve-metric-semantics`
  `cp -r` from `codex-ade-dbt-minimal`; one file (README.md), all other surfaces unchanged.
- DONE: README change = EXACTLY ONE Implementation-stage policy block, B-variant text VERBATIM
  `diff` vs parent = single hunk `55a56,62` under `## Stage: Implementation`; collapsed-whitespace string-match against the B variant is byte-identical; leak-guard (lines 1-32) + 4 stage headers byte-identical; token scan over added lines clean (no AUTO_*/solution__*/check_*/verifier/Got N/curl/wget/git clone/web/fetch). AC-1 met.
- DONE: Full spec differs only in `experiment:` + `solver_workflow:`
  `diff specs/baseline.yaml specs/h0042….yaml` = lines 2 and 11 only; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved.
- DONE: Smoke spec `benchmark.tasks` = airbnb009 PRIMARY FLIP target + h0019 canary panel
  airbnb009 (target) + airbnb001 / asana001 / ana-eng001 / f1007 / quickbooks002; `diff` vs full adds only the `benchmark.tasks` block; verified against @baseline 622bdedac572b479: airbnb009 reward=0.0, all 5 canaries reward=1.0.
- DONE: Freeze both specs (`rk freeze --allow-missing`)
  `…frozen.yaml` (1733 B) + `…smoke.frozen.yaml` (1872 B) written; both carry kind=spacedock_solver / runtime=codex / trials=1.
- DONE: Run the gatekeeper; record per-rule table + recommendation in `## Gatekeeper review`
  Recommendation APPROVE (no FAILs). G1-G6 PASS, G7 WARN (abstract abstain-prose, no worked example), G8 PASS+WARN (one airbnb same-family canary), G9/G10/G11 N/A (not a selector; not self-correcting — the inverse, preserve-don't-rewrite; airbnb009 single-model).

### Summary

Authored the h0042 variant: forked the @baseline solver and added one Implementation-stage policy
block (B-variant text verbatim) telling the solver to treat missing-rows/date-spine/coverage tasks
as coverage repairs first and preserve existing COUNT/SUM/AVG/window/filter definitions unless
visible evidence says the metric is wrong. Full + smoke specs created and frozen, differing from
baseline only in the allowed fields; smoke carries airbnb009 (the PRIMARY FLIP target, @baseline
0.0) plus the h0019 5-family canary panel (all @baseline 1.0). Gatekeeper recommendation APPROVE
(no FAILs); two advisory WARNs noted — G7 inert-risk (abstract prose, judge by committed SQL not
chatter; the 12/12 pre-smoke probe is proxy, NOT a score) and G8 single airbnb same-family canary.
NOTE: the smoke STAGE will additionally run 3 SEQUENTIAL FOCUSED airbnb009 repeats (fresh context
each); AC-4 GO bar is ≥2/3 runs that BOTH preserve `COUNT(*)` AND pass a clean strict audit (3/3
target) — a decision-policy/reproducibility claim, not a single-shot flip.

