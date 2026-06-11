---
id: h0042
title: Coverage repair preserves metric semantics -- when fixing missing rows/date spines, do not change COUNT/SUM/AVG/window definitions unless visible project evidence says the metric itself is wrong
status: analyze
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

## Smoke result

**Verdict: GO — 3/3 airbnb009 attempts preserved `COUNT(*)`, landed the date-spine repair, passed
the verifier, and passed clean strict audits (the 3/3 target, exceeding the 2/3 bar). All 5
canaries held PASS.** The free metric-semantics line that made h0019 non-reproducible at
`trials: 1` is pinned: across three independent solver contexts the committed
`mom_agg_reviews.sql` repaired only the date spine and never rewrote the aggregate.

### AC-4 — decisive reproducibility read (committed-artifact classification)

| # | Run-dir / cell | Aggregate expr (committed) | Date-spine repair landed? | Metric def changed? | Verifier | Strict audit |
|---|---|---|---|---|---|---|
| 1 (panel) | `797604a420d08244` / `airbnb009__NH3nEkU` | `COUNT(*)` (line 34, untouched) | YES — `IN(DISTINCT review dates)` → `BETWEEN MIN..MAX` | NO | PASS (reward 1.0) | clean (tainted 0, captured 1) |
| 2 (focused) | `0a456f136f374439` / `airbnb009__ERR5VmQ` | `COUNT(*)` (untouched) | YES — bounds-CTE + `BETWEEN MIN..MAX` | NO | PASS (reward 1.0) | clean (tainted 0, captured 1) |
| 3 (focused, seed 42) | `a267ccc4c36ec50c` / `airbnb009__dvgEBNs` | `COUNT(*)` (untouched) | YES — `IN(DISTINCT)` → `BETWEEN MIN..MAX` | NO | PASS (reward 1.0) | clean (tainted 0, captured 1) |

**Reproducibility rate: 3/3 (100%) keep `COUNT(*)` + pass.** Zero `COUNT(review_cte.REVIEW_DATE)`
/ column-count recurrences. In all three, the *only* patch to `mom_agg_reviews.sql` edited the
`dates_cte` spine filter; the `COUNT(*) AS REVIEW_TOTALS` line was never in any hunk. (For my
analysis only, never surfaced to the solver: the task oracle also uses `COUNT(*)` with a
`MIN..MAX` spine, confirming `COUNT(*)` is the correct metric and the h0019 standalone's
`COUNT(review_date)` would have been wrong.)

### AC-5 — canary regression check (6-task panel, run-dir `797604a420d08244`)

| Task | Family | @baseline | Smoke result | Audit |
|---|---|---|---|---|
| airbnb009 (target) | airbnb | 0.0 FAIL | **1.0 PASS** (attempt #1) | clean |
| airbnb001 | airbnb | 1.0 | 1.0 PASS | clean |
| asana001 | asana | 1.0 | 1.0 PASS | clean |
| ana-eng001 | ana-eng | 1.0 | 1.0 PASS | clean |
| f1007 | f1 | 1.0 | 1.0 PASS | clean |
| quickbooks002 | quickbooks | 1.0 | 1.0 PASS | clean |

Panel `stratified_pass_at_1 = 1.0` (6/6); audit `{clean: 6, tainted: 0, coverage_missing: 0}`;
every cell `captured = 1`. No canary lost (AC-5 satisfied).

## Run result

**Status: COMPLETE — NO-GO. `stratified_pass_at_1 = 0.5625` (27/48) = net −4 vs @baseline 31/48
(0.6458). The PRIMARY FLIP TARGET airbnb009 = 0.0 FAIL — it did NOT flip at full.** The clean
3/3 smoke did NOT reproduce at 48-scale, AND the generative coverage rule regressed 5 baseline
passers (the G8 unsampled-regression risk materialized). This is a NO-GO direction.

- **Run-dir:** `runs/ade-bench-h0042-coverage-repair-preserve-metric-semantics/1948ab42a6a5d9b7/`
  (48 cells). Launched detached 2026-06-10T17:25:57Z, finished 2026-06-11T00:00:37Z (rc=0,
  ~6.6h); handle `runs/.rk-handles/h0042-full-20260610-172557/` (sentinel rc=0).
- **Strict audit (run BEFORE the score was trusted):** `rk audit … --policy strict` →
  `summary: {clean: 48, coverage_missing: 0, tainted: 0}`; all 48 trials `taint_status: clean`,
  zero findings. `coverage_missing: 0` attests captured traces on every cell. CLEAN.
- **Score:** `rk score … --format json` → `stratified_pass_at_1: 0.5625`,
  `n_total: 48, n_completed: 48, n_errored: 0, n_pass: 27` (Wilson CI [0.423, 0.693]).
  **27 PASS / 21 FAIL.**
- **Net vs @baseline (paired, identical 48-task set):** **−4** (baseline 31 PASS → h0042 27 PASS).
  - 5 REGRESSIONS (baseline PASS → h0042 FAIL): `airbnb005`, `asana003`, `f1005-medium`,
    `f1006-hard`, `quickbooks003`.
  - 1 incidental GAIN (baseline FAIL → h0042 PASS): `asana002` — NOT the intended target.
  - Intended target `airbnb009`: baseline 0.0 → h0042 0.0 (unchanged FAIL; the smoke flip did
    not reproduce).
  - Arithmetic: +1 (asana002) − 5 (regressions) = −4. airbnb009 contributes 0.
- **Methodology consistency (no smoke→full drift) — from SEALED run-dir artifacts:** the full
  run-dir and the smoke run-dir (`797604a420d08244`) both carry
  `solver_workflow_content_hash / solver_workflow_hash =
  sha256:b0103e7a29f39b2e17c7cd7c889f9c06f540451ccd2915e5ad3585545160ed6c` and identical agent
  `sealed_hash 14e4e3f015cd0dbf775caf60818ef1d6`. IDENTICAL — the full used the exact same solver
  README as smoke; only the task set differed (full `tasks: null`/all-48 vs smoke 6-task panel).
- **Full FAIL list (21):** airbnb005, airbnb007, airbnb009, ana-eng004, ana-eng006, ana-eng007,
  ana-eng007-medium, asana003, asana004, asana005, asana005-hard, f1002, f1005-medium, f1006,
  f1006-hard, f1011, intercom001, intercom002, intercom003, quickbooks001, quickbooks003.

The per-task behavioral ledger — (a) why airbnb009's committed `COUNT(*)` pin did NOT reproduce/pass
at full despite the 3/3 smoke, and (b) which of the 5 regressions are lever-attributable vs
single-trial variance — is the NEXT stage (analyze), deliberately not started here.

### Paired delta (analyze stage; `rk runs diff` TypeErrors on these run-dirs → computed from `per_trial_outcomes.json`, slug-paired, 10k bootstrap)

`rk runs diff` raises `TypeError` on ade-bench run-dirs (`query_id: null`, keyed on `trial_name`),
so the paired delta was computed directly from `per_trial_outcomes.json` slug-paired over the
identical 48-task set:

- Observed paired delta (h0042 − @baseline): **−4 tasks** (−0.0833 pass-rate); 31 → 27.
- 10k-bootstrap 95% CI on the pass-rate delta: **[−0.1875, +0.0000]** = [−9, 0] tasks — **the CI
  touches 0**.
- Discordant pairs: 5 regressions (P→F), 1 gain (F→P); exact two-sided sign-test **p = 0.219**.
- Absolute score 0.5625 vs `paper_baseline` 0.1875 (well above the paper anchor, as all forks are).

Read: the −4 point estimate is negative but **NOT statistically distinguishable from zero** (CI
includes 0, p = 0.22). This matches the per-task variance analysis below — the regressions are
dominated by single-trial churn on coin-flip cells, not a clean lever-caused harm. It is still a
NO-GO: the point estimate is negative AND the decisive flip target (airbnb009) did not reproduce.

## Behavioral analysis

- **The lever pins the exact fork it was authored for.** h0019 steered the spine repair but left
  the aggregate line free; at `trials: 1` the solver coin-flipped `COUNT(*)` (pass) vs
  `COUNT(review_date)` (fail). h0042's Implementation-stage policy ("coverage repair preserves
  metric semantics") removed that free branch: 3/3 fresh contexts kept `COUNT(*)` and committed a
  spine-only edit. The pre-smoke 12/12 proxy now has matching real-run evidence (3/3 committed
  artifacts), so the proxy was directionally correct without being promoted as a score.
- **Mechanism is artifact-proven, not chatter.** Every classification above is from the
  dispatched solver's `apply_patch` payload (the committed `mom_agg_reviews.sql` hunk), not
  transcript narration (AC-3). In all three the COUNT line is absent from the diff = preserved by
  construction; the edit is confined to `dates_cte` / a bounds CTE.
- **G7 inert-risk did not materialize.** The gatekeeper flagged the rule as abstract abstain-prose
  with no worked example. It nonetheless fired correctly here because it acts as a *don't-rewrite*
  preference at a fork where the minimal coverage repair is also the correct one — it suppresses an
  over-eager semantic cleanup rather than asking for a structural rewrite (the dead inert family).
- **G8 same-family caveat — still open at full scale.** The smoke carried only one airbnb
  same-family canary (airbnb001), which held. The rule is generative (fires on any
  coverage-repair task), so a different airbnb (or other-family) passer the smoke never ran could
  still be perturbed at full. The smoke cannot close this; it is a full-stage watch item.
- **Run-mechanics note (not a result):** the first focused re-run collapsed into the content-
  addressed run-dir cache (identical frozen spec → identical `sealed_hash` → cached result, no
  re-solve). Attempt #3 was made genuinely independent by perturbing `sampling.seed` (→ a distinct
  `sealed_hash 32f429…`), which forced a fresh run-dir `a267ccc4c36ec50c` and a real solver
  context. The experiment-name change alone did NOT bust the cache (sealed_hash is task+solver+
  sampling content, not the experiment label). This is an in-stage instruction lever, so no
  WORKFLOW-REFINE entry is required.

## Stage Report: smoke

- DONE: CANARY REGRESSION CHECK (AC-5) — run the frozen 6-task panel smoke spec; all 5 canaries hold PASS on clean strict audit
  Panel run-dir `797604a420d08244`: 6/6 reward 1.0; audit `{clean:6, tainted:0, coverage_missing:0}`; airbnb001/asana001/ana-eng001/f1007/quickbooks002 all PASS (= @baseline); airbnb009 PASS (attempt #1).
- DONE: THE DECISIVE REPRODUCIBILITY READ (AC-4) — airbnb009 run as 3 fresh focused attempts, committed-SQL aggregate classified per attempt
  3/3 preserved `COUNT(*)` + landed the spine repair + PASS. Cells: `NH3nEkU` (panel), `ERR5VmQ` (focused `0a456f136f374439`), `dvgEBNs` (focused seed-42 `a267ccc4c36ec50c`). Zero column-count recurrence. Classified from `apply_patch` payloads.
- DONE: Strict audit `--policy strict` clean (`tainted: 0`) + `captured > 0` on every cell before any score trusted; per-attempt table + reproducibility rate + canary results recorded
  All three run-dirs audited clean (tainted 0, coverage_missing 0), captured=1 each; `audit-strict.json` saved in each run-dir; tables in `## Smoke result`, narrative in `## Behavioral analysis`. No WORKFLOW-REFINE entry (in-stage instruction lever).

### Summary

GO. The h0042 coverage-repair-preserves-metric-semantics rule reproducibly pins the airbnb009
decision fork: 3/3 independent fresh solver contexts kept the existing `COUNT(*)` aggregate while
repairing the date spine (`IN(DISTINCT)` → `BETWEEN MIN..MAX`), each PASS on a clean strict audit
— the 3/3 target, well past the 2/3 bar. All 5 cross-family canaries held PASS with clean audits
(AC-5). All verdicts are artifact-proven from committed `apply_patch` hunks, not transcript
narration (AC-3). One open watch item for full: the smoke carried a single airbnb same-family
canary, so a generative-rule regression on an unrun airbnb/other passer can only be ruled out at
full scale (G8). Recommend advancing to `full`.

## Stage Report: full

- DONE: Full 48-task run on `specs/h0042-coverage-repair-preserve-metric-semantics.frozen.yaml` completed (launched DETACHED via nohup, polled across turns, never foregrounded); strict audit clean; run-dir + headline recorded in `## Run result`
  Run-dir `runs/ade-bench-h0042-coverage-repair-preserve-metric-semantics/1948ab42a6a5d9b7` (48 cells); launched 2026-06-10T17:25:57Z via `drivers/rk-run-detached.sh`, sentinel rc=0 at 2026-06-11T00:00:37Z (~6.6h). `rk audit --policy strict` → `{clean:48, tainted:0, coverage_missing:0}`, 0 findings (captured attested on every cell) BEFORE the score was trusted. `rk score --format json` → `stratified_pass_at_1 0.5625` = 27/48. **NO-GO: net −4 vs @baseline 31/48; airbnb009 = 0.0 did NOT flip; 5 regressions (airbnb005/asana003/f1005-medium/f1006-hard/quickbooks003), 1 incidental gain (asana002).**
- DONE: Methodology consistency (no smoke→full drift): the full run used the SAME solver README as smoke (only the task set differs); hash stated
  From the SEALED run-dir artifacts, the full run-dir and the smoke run-dir (`797604a420d08244`) both carry `solver_workflow_content_hash` = `sha256:b0103e7a29f39b2e17c7cd7c889f9c06f540451ccd2915e5ad3585545160ed6c` and identical agent `sealed_hash 14e4e3f015cd0dbf775caf60818ef1d6`. IDENTICAL — no drift.

### Summary

NO-GO at full. h0042 scored 27/48 (0.5625) on a clean strict audit (tainted 0, coverage_missing 0,
0 findings) — net −4 vs @baseline 31/48. The decisive flip target airbnb009 stayed 0.0 FAIL: the
clean 3/3 airbnb009 smoke did NOT reproduce at 48-scale. The generative coverage-repair rule also
regressed 5 baseline passers (airbnb005, asana003, f1005-medium, f1006-hard, quickbooks003) against
1 incidental gain (asana002), exactly the G8 unsampled-regression risk the 6-task smoke could not
cover. Methodology was drift-free: full and smoke share the identical solver-workflow content-hash
`b0103e7a…`. This stage is the clean run accounting only; the per-task behavioral ledger (why the
airbnb009 COUNT(*) pin did not reproduce, and which regressions are lever-attributable vs variance)
is the next stage (analyze), not started here.

## Analyze (full vs @baseline 31/48)

**Recommended verdict: REJECTED.** Net −4 (27/48), the decisive flip target airbnb009 did NOT
reproduce, and the −4 is dominated by ordinary single-trial variance on coin-flip cells (CI touches
0, sign-test p=0.22) rather than a clean lever-caused harm. @baseline is NOT promoted. All
classifications below are from committed `apply_patch` payloads (AC-3), not transcript chatter.

### Decisive: THE REPRODUCIBILITY GAP — why the clean 3/3 airbnb009 smoke did not predict the full

**At full, airbnb009 did NOT keep `COUNT(*)` — the pin did not hold this run.** The committed
`models/agg/mom_agg_reviews.sql` hunk (cell `airbnb009__uo2JG9E`) changed the aggregate to the
**exact h0019 wrong fork** AND additionally restructured the model:

```text
-	COUNT(*) AS REVIEW_TOTALS ,
+	COUNT(review_cte.REVIEW_DATE) AS REVIEW_TOTALS ,
... + a new sentiments_cte + date_sentiments_cte CROSS JOIN, FROM date_sentiments_cte
```

The date-spine repair landed (`IN(DISTINCT)` → `BETWEEN MIN..MAX`), but the aggregate was rewritten
exactly as h0019's failing standalone did — and exactly as **@baseline** did (baseline
`airbnb009__zaFEXfL` committed the same `COUNT(*)` → `COUNT(review_cte.REVIEW_DATE)`). Verifier:
`mom_agg_review_date_range` "Got 1 result, configured to fail if != 0" — a semantic mismatch, model
built fine. So the lever did NOT suppress the wrong fork in this context.

**Why the 3/3 smoke did not predict it (the h0019 lesson restated): airbnb009 is a low-base-rate
cell, and the focused smoke was a high-end streak, not a guarantee.** Across the 12 full-scale runs
on disk, airbnb009 passes in only **2/12 (~17%)**. A focused 3/3 single-cell smoke is a sample of 3
draws from a ~17%-pass process *that happened to cluster on the good branch* (it is not even
representative — it over-sampled the pass side). At `trials: 1` the single full draw fell on the
modal FAIL branch. **The pin REDUCES but does not ELIMINATE the gpt-5.5 fork variance**; a 3/3
reproducibility smoke is necessary-not-sufficient evidence at `trials: 1`. This is the h0019 lesson:
"found/pinned the fork in N fresh contexts" ≠ "the single scored trial lands there."

### Per-task ledger — both directions (committed-artifact classified)

| Task | @baseline | h0042 full | Δ | Committed-artifact mechanism | P/F across 12 full runs | Classification |
|---|---|---|---|---|---|---|
| **airbnb009** (target) | 0.0 F | 0.0 F | 0 | aggregate rewritten to `COUNT(review_cte.REVIEW_DATE)` + CROSS-JOIN restructure (the h0019 wrong fork; pin did not hold) | P 2/12 | **target did not flip** (low base-rate ~17%; pin reduces ≠ eliminates) |
| airbnb005 | 1.0 P | 0.0 F | −1 | from-scratch `Add File` of two NPS rolling-window models; failed `*_nps_reviews_equality_with_tolerance` (Got 4 / Got 2) — value/window-frame divergence in a from-scratch authoring task | P 10/12 (F only 2/12) | possibly LEVER-ADJACENT but rare-drop; not clean attribution |
| asana003 | 1.0 P | 0.0 F | −1 | edited 11 `dbt_packages/asana_source/stg_asana__*` package-staging models; 6/17 equality fails (task/metrics/user/tags) — package-migration family, NOT coverage-repair | P 8/12 (F 4/12) | single-trial VARIANCE (not a coverage task; rule wouldn't fire) |
| f1005-medium | 1.0 P | 0.0 F | −1 | edited `models/stats/constructor_points.sql`; `AUTO_constructor_points_equality` Got 2 — value divergence, NOT coverage | P 8/12 (F 4/12) | single-trial VARIANCE |
| f1006-hard | 1.0 P | 0.0 F | −1 | edited `constructor_points.sql` + `driver_points.sql`; same `AUTO_constructor_points_equality` Got 2 — value divergence | **F 8/12** (fails MORE than passes — chronic variance cell, also dropped h0037/h0041/h0043) | single-trial VARIANCE |
| quickbooks003 | 1.0 P | 0.0 F | −1 | removed `using_department: true`, edited union models; verifier = **Compilation Error** "has less columns than solution" (under-inclusion / broken edit) on a package-config task, NOT coverage | P 6/12 / F 6/12 (coin-flip) | single-trial VARIANCE (possibly lever-conservatism-adjacent but compile-broken) |
| asana002 (gain) | 0.0 F | 1.0 P | +1 | conditional-inclusion package-migration fix (Fivetran made tags optional) — solver-native, a known "Mini flip" | P 6/12 / F 6/12 (coin-flip) | incidental VARIANCE gain, NOT the lever's target |

**Bottom line on attribution:** of the 5 regressions, **4 (asana003, f1005-medium, f1006-hard,
quickbooks003) are within normal single-trial variance** — each fails in 4–8 of the other 12 full
runs and none is a coverage-repair task where the rule fires. **airbnb005 is the one anomaly**
(fails only 2/12), and even it is a from-scratch NPS-authoring task with many free knobs, not a clean
"rule preserved a metric that should have changed." There is **no clean evidence the coverage-repair
rule caused a −N**; the net −4 is variance churn (CI [−9, 0] tasks, p=0.22) plus the target's
non-reproduction. The single incidental gain (asana002) is also a coin-flip cell, not a lever win.

### The 6 required questions

1. **Net + full per-task ledger (both directions):** −4 (27/48 vs 31/48); paired delta −0.0833,
   10k-bootstrap 95% CI [−0.1875, +0.0000] (CI touches 0), sign-test p=0.219. Gains: asana002
   (F→P). Regressions: airbnb005, asana003, f1005-medium, f1006-hard, quickbooks003 (all P→F). Each
   mechanism in the ledger table above. Target airbnb009 unchanged FAIL.
2. **Smoke vs full:** the smoke was a focused 3/3 single-cell airbnb009 repeat + a 6-task canary
   panel. It could NOT see (a) airbnb009's true ~17% base rate — 3/3 was a high-end streak, not a
   guarantee, so it over-stated reproducibility; and (b) the 41 unsampled tasks, where coin-flip
   cells (f1005-medium, f1006-hard, asana003, quickbooks003, asana002) churn between runs. The 6-task
   panel held PASS at full too (the canaries themselves did not regress) — the regressions were all
   on UNSAMPLED tasks, exactly the G8 gap.
3. **Already-correct-and-broken:** all 5 regressions were @baseline passers (1.0) — this is damage to
   working code, not "failed to help." BUT artifact + cross-run evidence shows 4/5 are single-trial
   variance (they break in 4–8 of the other 12 runs regardless of any lever), and the rule does not
   fire on them (they are package-migration / value-divergence tasks, not coverage repairs). Only
   airbnb005 is a rare drop. So: damage is real at the row level, but mostly NOT lever-caused.
4. **Was the change executed?** Yes — every cell's committed artifact changed. Classify: airbnb009 =
   **executed-and-hurt-via-wrong-branch** (rule present but did not suppress the wrong fork; the pin
   did not hold). The 4 variance regressions = **executed-but-on-non-coverage-tasks** (the rule's
   premise "this is a coverage-repair task" was not met → the rule is effectively inert there; the
   FAILs are independent variance). airbnb005 = **executed**, from-scratch authoring, value
   divergence. asana002 gain = **executed** (solver-native conditional-inclusion), not lever-driven.
   No inert "discussed-not-done" cells.
5. **Prevention + next move:** (a) **Don't trust a focused single-cell reproducibility smoke as a
   flip predictor for a low-base-rate target at `trials: 1`** — a 3/3 on a ~17%-pass cell is a streak;
   either measure the base rate first (the cross-run table existed) or require multi-trial CI on the
   target before promoting (which the standing single-trial decision forbids → so such flips should be
   treated as un-promotable by construction). (b) The G8 smoke gap (unsampled regressions) is inherent
   to a 6-task panel; only a full run reveals it — so for generative rules, the smoke verdict should be
   explicitly provisional pending full. (c) **Next move: do NOT re-file.** This re-confirms the
   oracle-problem / single-trial-variance wall already documented (the flip portfolio is concluded,
   @baseline 31/48; airbnb009 is a ~17% cell whose only genuine fix was h0019, itself unpromotable due
   to variance masking). Escalate to the captain — the coverage-semantics lever is net-harmful-or-null
   at full and adds no new movement; the box remains closed at the program level.
6. **Smoke-vs-full fork drift:** the smoke result was **artifact-real but not population-representative**
   — the 3/3 committed `COUNT(*)` artifacts were genuine, but they sampled the favorable tail of a
   bimodal fork. The fork that changed at full: the airbnb009 aggregate-line choice flipped from
   `COUNT(*)` (smoke) to `COUNT(review_cte.REVIEW_DATE)` (full) — the README rule **drifted into the
   wrong implementation branch** despite being present (it is abstract abstain-prose, the G7 inert-risk
   the gatekeeper flagged — it can be acknowledged-and-skipped). The 5 regressions are **unrelated
   single-trial variance** on unsampled cells, not a rule-driven fork. This feeds the Failure
   Review: a focused reproducibility smoke on a low-base-rate, abstract-prose lever is not a reliable
   GO signal at `trials: 1`.

### WORKFLOW-REFINE note

This is an in-stage instruction lever (solver README only), so per the standing rule the per-task
learnings stay in this entity + the instruction-lever taxonomy, not WORKFLOW-REFINE. The transferable
**methodology** lesson — *a focused single-cell reproducibility smoke (even 3/3) is not a flip
predictor for a low-base-rate target at `trials: 1`; measure the cross-run base rate before
promoting* — is worth recording for the loop (candidate for the single-trial / judge-by-artifact
note), as it generalizes beyond this lever.

## Stage Report: analyze

- DONE: THE REPRODUCIBILITY GAP (decisive) — airbnb009 committed SQL read at full + why the 3/3 smoke did not predict
  At full airbnb009 did NOT keep `COUNT(*)`: committed hunk rewrote it to `COUNT(review_cte.REVIEW_DATE)` + CROSS-JOIN restructure (the exact h0019 wrong fork; same as @baseline). Explained: airbnb009 passes only 2/12 (~17%) across full runs; the 3/3 focused smoke was a high-end streak, not a guarantee — the pin reduces but does not eliminate the gpt-5.5 fork variance at trials:1 (h0019 lesson restated). Artifact-classified, not chatter.
- DONE: THE 5 REGRESSIONS + 1 GAIN — each confirmed a @baseline passer/failer, committed SQL read, classified lever-attributable vs variance
  All 5 regressions were @baseline 1.0; asana002 was @baseline 0.0. Per-task ledger + cross-run P/F frequency table recorded. Verdict: 4/5 regressions (asana003, f1005-medium, f1006-hard, quickbooks003) are single-trial VARIANCE (non-coverage tasks where the rule doesn't fire; each fails in 4–8/12 other runs; f1006-hard fails 8/12 — chronic). airbnb005 the lone rare-drop (2/12). No clean lever-caused −N. asana002 gain = incidental coin-flip, not a lever win.
- DONE: 6 required questions answered in `## Run result` + `## Analyze`; recommend conclude verdict
  Paired delta −4 / CI [−9,0] tasks / p=0.219 (computed from per_trial_outcomes.json, slug-paired, 10k bootstrap, because `rk runs diff` TypeErrors on query_id:null). All 6 questions answered. **Recommended verdict: REJECTED — net −4, target didn't flip, no new movement; @baseline NOT promoted; escalate (do not re-file — re-confirms the single-trial-variance / oracle-problem wall).**

### Summary

REJECTED recommendation. h0042 = 27/48, net −4 vs @baseline 31/48; the decisive flip target
airbnb009 did NOT reproduce — at full the committed SQL fell to the exact h0019 wrong fork
(`COUNT(review_cte.REVIEW_DATE)`, same as @baseline) despite the rule. The 3/3 focused smoke did not
predict this because airbnb009 is a ~17%-pass cell and 3/3 was a favorable-tail streak: the pin
reduces but does not eliminate the gpt-5.5 fork variance at `trials: 1` (the h0019 lesson). The −4
is NOT statistically distinguishable from zero (CI [−9,0] tasks, p=0.22) and is dominated by
single-trial variance on coin-flip cells (4/5 regressions fail in 4–8 of the other 12 full runs and
are not coverage-repair tasks where the rule fires); only airbnb005 is a rare drop. No clean
lever-caused harm and no new movement. @baseline stays 31/48. Next move: escalate — do not re-file;
this re-confirms the concluded flip-portfolio / single-trial-variance wall.
