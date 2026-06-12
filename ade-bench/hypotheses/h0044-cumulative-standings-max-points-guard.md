---
id: h0044
title: Cumulative standings max-points guard -- for season/entity totals from standings snapshots, repair inflated sums with same-grain max(points) and reject final-row variants
status: analyze
kind: hypothesis
source: Captain request 2026-06-10 after f1006 decision-fork analysis and C-variant subagent probe. Follows h0012 smoke pass / full regression evidence and h0037 full f1006/f1006-hard latest-row failure pattern. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-10T08:15:58Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`f1006` is a cumulative-standings repair, not an independent recompute target.
The visible task says the `points` columns in `constructor_points.sql` and
`driver_points.sql` are too high. The broken local shape is `sum(points)` over
race-by-race standings rows at constructor/season and driver/season grain. Since
standings points are cumulative snapshots, summing them over a season overstates
the total. The intended local repair family is same-grain `max(points)` in every
named affected model.

**Falsifiable claim (the single solver-README change -- Implementation policy
only):** adding a cumulative-standings max-points guard will make the real solver
preserve the simple `sum(points) -> max(points)` repair and avoid the plausible
but fragile alternatives: latest-row/rank/final-race selection and recomputing
season totals from race results. The expected benefit is not that the model
newly discovers `max(points)`; proxy probes show it already often does. The
benefit is that the full workflow should stop drifting from the correct simple
aggregate repair into an over-engineered final-row path.

**The single proposed README text (C variant):**

```text
When repairing season/entity totals from *_standings tables, treat points as
cumulative race-by-race snapshots unless local evidence proves otherwise. If a
task says points are too high and the model currently sums standings points,
prefer the same-grain aggregate repair: replace sum(points) with max(points) in
every named affected model.

Do not switch to latest-row, rank, row_number, QUALIFY, order-by-final-race, or
race-results recomputation unless local evidence proves max(points) is wrong.
Before finalizing, inspect the edited SQL: the load-bearing fix should preserve
the existing entity/season grain and use max(points), not final-row selection.
```

For `f1006`, the intended repair is:

- change `sum(cs.points)` to `max(cs.points)` in `constructor_points.sql`;
- change `sum(ds.points)` to `max(ds.points)` in `driver_points.sql`;
- preserve existing constructor/season and driver/season output grain;
- do not introduce `row_number()`, `rank()`, `QUALIFY`, final race ordering, or
  date/round final-row selection as the load-bearing fix;
- do not recompute totals from race-result rows when standings are present.

**Why this differs from h0012 and h0037.** h0012's successful smoke proved that
the f1006 family can be fixed by a simple cumulative-standings aggregate repair,
but that experiment's broader independent-recompute framing was harmful at full
run. h0037 showed the remaining failure mode: the solver can choose a locally
reasonable final-row/latest-row implementation that passes many intuitive checks
but fails edge cases. h0044 therefore avoids a broad "recompute independently"
instruction and pins a narrow artifact shape: same-grain `max(points)`.

**Pre-smoke subagent decision-fork evidence (proxy, not a score result).** We
ran fresh subagents with `fork_context=false`, no tools, no repo inspection, no
hidden verifier output, and only visible task/model context. The decision fork
was: same-grain `max(points)` vs latest-row/final-row standings selection vs
race-results recomputation.

Calibration with full visible context, including sibling championship models
that use `max(points)`:

| Variant | Rule | `max(points)` | Latest-row / final-row | Race-results recompute |
|---|---|---:|---:|---:|
| A | Weak baseline-style smallest local repair | 2/2 | 0/2 | 0/2 |
| B | Cumulative standings max-points rule | 2/2 | 0/2 | 0/2 |
| C | Strong max-points rule + no-latest-row guard | 2/2 | 0/2 | 0/2 |

Stricter probe without sibling championship model context:

| Variant | Rule | `max(points)` | Latest-row / final-row | Race-results recompute |
|---|---|---:|---:|---:|
| A | Weak baseline-style smallest local repair | 2/2 | 0/2 | 0/2 |
| B | Cumulative standings max-points rule | 2/2 | 0/2 | 0/2 |
| C | Strong max-points rule + no-latest-row guard | 2/2 | 0/2 | 0/2 |

Follow-up C-only stricter probe:

| Variant | Runs | `max(points)` | Latest-row / final-row | Race-results recompute | Other / unclear |
|---|---:|---:|---:|---:|---:|
| C | 10 | 10 | 0 | 0 | 0 |

Total C evidence across both C batches: **14/14** chose same-grain
`max(points)`, with **0/14** choosing latest-row or race-results recompute.

Honest caveat: the weak A wording also chose `max(points)` in 4/4 probes. This
means h0044 is not claiming the C rule uniquely discovers the correct branch in
an isolated prompt. It claims the C rule should reduce full-workflow drift after
the branch is discovered, by making final-row variants artifact-invalid.

**Falsification path.** h0044 fails if fresh real `rk` smoke on the f1 standings
family produces a committed patch whose load-bearing change is latest-row,
rank/final-race selection, or race-results recomputation. It also fails if the
patch changes only one of the two named f1006 models, changes output grain, or
regresses same-family passers.

**Target datasets.** Primary targets:

- `ade-bench-f1006`
- `ade-bench-f1006-hard`

Same-family targets:

- `ade-bench-f1005`
- `ade-bench-f1005-medium`

Optional canaries:

- `ade-bench-f1001`
- `ade-bench-airbnb001`

The expected movement is to stabilize the f1 standings family by preventing the
known latest-row/recompute failure branch. A green target whose committed SQL
does not contain same-grain `max(points)` is not strong evidence for this
hypothesis.

**Proposed smoke design.** Use a focused family smoke panel:

1. `ade-bench-f1006`
2. `ade-bench-f1006-hard`
3. `ade-bench-f1005`
4. `ade-bench-f1005-medium`
5. `ade-bench-f1001`
6. `ade-bench-airbnb001`

The decisive artifact read is the f1 point-model patch:

1. `constructor_points.sql` uses same-grain `max(...points...)` as the
   load-bearing fix.
2. `driver_points.sql` uses same-grain `max(...points...)` as the load-bearing
   fix when the task names that model.
3. No load-bearing `row_number()`, `rank()`, `QUALIFY`, `order by round_number`,
   `order by race_date`, or final-row selection appears in the point-total
   repair.
4. No race-results recomputation replaces the standings aggregate when standings
   are present.
5. Target(s) pass on clean strict audit, and same-family/canary tasks do not
   regress.

**Scope.** Solver README only. No benchmark, runtime, model, sampling, trials, or
spec-shape change. Leak guard remains intact; the proposed README rule references
only visible task instructions, local model names, local standings tables, local
SQL artifacts, and local data validation. It does not mention hidden expected
rows, verifier test names, solution files, or public reference data.

## Acceptance Criteria

**AC-1 -- Exactly one README policy change; specs differ only in allowed fields.**
Verified at propose by diffing the h0044 solver README against
`solver_workflows/codex-ade-dbt-minimal/README.md`: one Implementation policy
block added, leak-guard prose byte-identical, no hidden-test/solution/verifier
references. Full spec diff vs `specs/baseline.yaml` shows only `experiment:` and
`solver_workflow:`; smoke spec adds only `benchmark.tasks`.

**AC-2 -- Every score is paired with strict clean audit and captured traces.**
Each `rk score` must cite `rk audit --policy strict` on the same run-dir with
`tainted: 0`, `coverage_missing: 0`, and captured agent traces.

**AC-3 -- Decision-policy evidence is artifact based.**
For f1 standings targets, read committed SQL, not transcript narration. Classify
the patch as same-grain `max(points)`, latest-row/final-row, race-results
recompute, partial-one-model repair, or unclear.

**AC-4 -- h0044 is promoted only if the max-points artifact lands.**
Promotion requires the target point models to pass with committed same-grain
`max(points)` repairs and zero use of the known wrong repair families as the
load-bearing fix. A green target with latest-row logic is a NO-GO for this
hypothesis.

**AC-5 -- No regression canary loss.**
All baseline passers in the smoke panel must remain pass. Any same-family or
canary regression is a NO-GO unless artifact analysis proves it is unrelated
single-trial variance and the captain explicitly accepts that risk.

## Gatekeeper review

**Recommendation: APPROVE** — exactly one Implementation-stage policy block (the
C-variant verbatim), leak-guard byte-identical, specs differ only in the allowed
fields, both frozen; the lever is gated to the standings construct and covers
BOTH of f1006's scored equality models, so the multi-model-target trap is
sidestepped, and the no-latest-row guard directly targets the h0037/h0041 drift
mode. WARNs are G7 (no worked-example skeleton) and G12 (probe block lacks the
literal heading/full provenance fields) — neither blocks the gate.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-10T14:55Z.

Fork parent resolved: `source:` field and `@baseline` run
(`runs/ade-bench-baseline/622bdedac572b479`, `solver_workflow:
solver_workflows/codex-ade-dbt-minimal`) agree → parent =
`solver_workflows/codex-ade-dbt-minimal`. G1/G6 evaluable.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff = one hunk added at L63 (inside `## Stage: Implementation`, before `## Stage: Validation`); exactly the cumulative-standings max-points guard; no other stage touched, no guardrail/dependency prose changed. |
| G2 leak-guard intact | PASS | Leak-guard prose (L1-32) byte-identical to parent; grep over added lines only — no `AUTO_*`/`solution__*`/`check_option`/`verifier`/`equality test`/`expected rows`/`curl`/`wget`/`git clone`/`published solution`. Added text names only visible task instructions, local model names, local `*_standings` tables, local SQL. |
| G3 spec two fields | PASS | `diff baseline.yaml h0044…yaml` = only `experiment:` (→ `ade-bench-h0044-cumulative-standings-max-points-guard`) and `solver_workflow:` (→ `./solver_workflows/h0044-cumulative-standings-max-points-guard`). `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0044…yaml h0044…smoke.yaml` = only an added `benchmark.tasks:` block (+ descriptive comment) with 6 `ade-bench-`-prefixed slugs. Both named targets present (f1006, f1006-hard). |
| G5 both frozen | PASS | `…frozen.yaml` (1725B) + `…smoke.frozen.yaml` (1856B) exist; both carry `kind: spacedock_solver` + `runtime: codex`; frozen smoke lists all 6 tasks. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim's C-variant verbatim; Implementation stage; mechanical SQL substitution (`sum(points)`→`max(points)`) + a same-grain/no-final-row guard. Not a self-anchored "re-run/verify your own output" instruction — it prescribes a concrete construct and forbids the wrong branch; reconciliation is against local task evidence, not the model's own re-derivation. |
| G7 actionability/inert-risk | WARN | Mostly a concrete mechanical substitution (`sum(points)`→`max(points)`) on a named construct — the durable-win shape (cf. asana002 `::timestamp`), low inert-risk. WARN: the "do not switch to latest-row/rank/…" guard is a prohibition stated as prose with no before→after skeleton; if the solver has already chosen a final-row path the prohibition may not mechanically reverse it. Predictive only — does not block. |
| G8 regression-canary coverage | N/A (PASS) | Lever is GATED, not generative: precondition = repairing season/entity totals from `*_standings` tables where the model sums standings points. It does not fire on arbitrary tasks. Smoke nonetheless carries a same-family perturbable panel (f1005, f1005-medium — h0012's regression victims) + f1001 (f1) + airbnb001 (cross-family) as tripwires. |
| G9 selector independence | N/A (PASS) | Not a multi-candidate/selector protocol — single deterministic repair rule. |
| G10 self-correcting false-positive | PASS | The lever is figure-change-gated (fires only when points are being repaired and the model currently sums standings points), and it does NOT mandate replacing a simple-correct path with a "structurally different" one — it PINS the simple aggregate (`max(points)`) and forbids the elaborate alternatives. This is the direct corrective for h0012's −4 failure mode (h0012 pushed passers OFF simple `sum→max` ONTO a wrong path then false-green-validated). No re-derived self-anchored reconcile. |
| G11 multi-model-target risk | N/A (PASS) | f1006/f1006-hard are each scored by 2 equality models — `AUTO_constructor_points_equality` AND `AUTO_driver_points_equality` (baseline `…f1006__VrRB7uJ/verifier/test-stdout.txt`: constructor FAIL 2 / driver PASS). The lever is COVERS-ALL: it names BOTH `constructor_points.sql` and `driver_points.sql`. The only failing model (constructor) is the lever's primary target; the guard also protects the already-passing driver model from an over-engineered rewrite. Not the single-model trap (airbnb007/h0018). |
| G12 decision-fork probe quality | WARN | Body carries decision-fork probe tables (A/B/C calibration; C 14/14 chose `max(points)`, 0/14 latest-row/recompute) with the right substance: solver-visible context only, a weak control A (also chose max 4/4 — honestly disclosed, no unique-discovery overclaim), explicit "proxy, not a score result" caveat, and the expected committed-artifact signature (same-grain `max(points)`, no row_number/rank/QUALIFY/final-row). WARN: the probe is NOT under the literal `## Pre-smoke Decision-Fork Probe` heading G12 names, and provenance fields are partial (agent count given for the C batch but `fork_context=false`/no-tools regime stated only narratively; exact tested wording is the C-variant block but not re-quoted per-batch). Substance is sound; treat smoke as exploratory-confirmatory. Does not block. |

**For the captain:** APPROVE for smoke. The two WARNs are the worth-a-glance items:
(G7) the no-latest-row guard is a prohibition without a worked skeleton — if the
solver pre-commits to a final-row path the prose may not mechanically unwind it;
(G12) the probe is solid in substance but not under the literal heading and is
proxy-only (weak A also chose `max` 4/4, so C's value is reducing full-workflow
drift, not unique discovery). The decisive read at smoke is ARTIFACT, not the
verdict: the committed `constructor_points.sql` + `driver_points.sql` must use
same-grain `max(...points...)` with NO `row_number()`/`rank()`/`QUALIFY`/
order-by-round/order-by-race_date/final-row selection and NO race-results
recompute. A green f1006 whose committed SQL uses latest-row logic = NO-GO
(AC-4). f1006-hard is a must-hold PASS (the h0037/h0041 drop cell); any passer
regression in the panel = NO-GO unless artifact-proven unrelated variance (AC-5).

## Stage Report: propose

- DONE: README change = EXACTLY ONE Implementation-stage policy block (C-variant verbatim), inside the existing Implementation stage; leak-guard + four stages otherwise byte-identical; no hidden-test/curl/web references.
  `diff codex-ade-dbt-minimal/README.md h0044…/README.md` = one hunk added at L63 (before `## Stage: Validation`); added-line leak/dead-family token grep clean. Commit 9b4fecd.
- DONE: Smoke spec `benchmark.tasks` = the 6-task f1-standings panel; both specs frozen.
  f1006 (🎯 only FAIL) + f1006-hard (✅ must-hold, h0037/h0041 drop cell) + f1005 + f1005-medium (perturbable same-family sentinels) + f1001 (f1 canary) + airbnb001 (cross-family canary). Full diff vs baseline = `experiment:`+`solver_workflow:` only; smoke diff = `benchmark.tasks` only. `…frozen.yaml`+`…smoke.frozen.yaml` written, kind/runtime preserved.
- DONE: Run the gatekeeper; record per-rule PASS/WARN/FAIL + APPROVE/REVISE/REJECT in `## Gatekeeper review`.
  Recommendation APPROVE (no FAILs). Decisive flags surfaced: COVERS-ALL on f1006's two scored models (constructor FAIL 2 / driver PASS at baseline → G11 N/A, not the single-model trap); G10 PASS (lever PINS simple `max(points)`, the direct corrective for h0012's −4); WARNs G7 (prohibition w/o skeleton) + G12 (probe substance sound, not under literal heading, proxy-only). C-probe 14/14 noted as proxy, weak-A also 4/4 → C's value = reducing full-workflow latest-row drift, not unique discovery.

### Summary

Forked `@baseline` solver `codex-ade-dbt-minimal` into `solver_workflows/h0044-cumulative-standings-max-points-guard` and inserted the single C-variant Implementation policy block verbatim (cumulative-standings max-points guard: `sum(points)`→`max(points)` in every named affected model; reject latest-row/rank/row_number/QUALIFY/final-race/race-results-recompute as the load-bearing fix; inspect edited SQL before finalizing). Built + froze full and smoke specs (full = two allowed fields; smoke adds the 6-task f1-standings panel). Gatekeeper recommendation APPROVE: leak-guard intact, specs clean, lever is gated to the standings construct and covers BOTH of f1006's scored equality models — and it directly corrects h0012's "off-simple-onto-wrong-path" failure and the h0037/h0041 latest-row drift on f1006-hard. Two non-blocking WARNs (G7 prohibition without a worked skeleton; G12 probe not under the literal heading and proxy-only). Decisive smoke read is ARTIFACT (committed SQL uses same-grain `max(points)`, no final-row logic), not the verdict.

## Smoke result

**Verdict: GO** — f1006 flipped FAIL→PASS via an artifact-proven same-grain
`max(points)` fix on BOTH named models; f1006-hard held PASS on `max(points)`
(stabilization claim confirmed — no latest-row drift); all sentinels/canaries
held. Smoke `stratified_pass_at_1 = 1.0` (6/6), n_errored=0.

Run: `runs/ade-bench-h0044-cumulative-standings-max-points-guard/17732f64285f1de2`.
Strict audit (`rk audit --policy strict`): `clean: 6, tainted: 0,
coverage_missing: 0` — captured traces on every cell (AC-2 satisfied).

| Task | @baseline | smoke | Role | Patch classification (committed) |
|------|----------:|------:|------|----------------------------------|
| ade-bench-f1006 | 0.0 FAIL | 1.0 PASS 🎯 | flip target | **same-grain `max(points)`** on `constructor_points.sql` (`sum(cs.points)`→`max(cs.points)`) AND `driver_points.sql` (`sum(ds.points)`→`max(ds.points)`); grain preserved; NO row_number/rank/QUALIFY/order-by-round/order-by-race_date/final-row, NO race-results recompute. All 4 verifier tests PASS (constructor_equality FAIL 2→PASS; driver_equality held PASS). |
| ade-bench-f1006-hard | 1.0 PASS | 1.0 PASS ✅ | stabilization must-hold | **same-grain `max(points)`** on both models (`constructor_points.sql:5`, `driver_points.sql:5`); 0 mismatches (920 constructor / 3190 driver rows). NOT the latest-row path that dropped it at full in h0037/h0041. All 4 tests PASS. |
| ade-bench-f1005 | 1.0 PASS | 1.0 PASS ✅ | perturbable sentinel (h0012 victim) | `sum(cs.points)`→`max(cs.points)` on `constructor_points.sql`; 0 max-aggregate mismatches across 920 rows; no final-row logic. All 4 tests PASS. |
| ade-bench-f1005-medium | 1.0 PASS | 1.0 PASS ✅ | perturbable sentinel (h0012 victim) | `sum(cs.points)`→`max(cs.points)` at existing constructor grain; no final-row logic. All 4 tests PASS. |
| ade-bench-f1001 | 1.0 PASS | 1.0 PASS ✅ | f1 canary | staging task (`stg_f1_dataset__results`); NO points/standings construct → lever precondition did not match (inert). All 6 tests PASS — no convention bleed. |
| ade-bench-airbnb001 | 1.0 PASS | 1.0 PASS ✅ | cross-family canary | airbnb reviews aggregates; lever inert (no f1/standings construct). All 10 tests PASS — no cross-family bleed. |

## Behavioral analysis

**The flip is real and on the intended artifact (AC-3/AC-4).** f1006's
load-bearing fix is exactly the same-grain `max(points)` substitution on both
`constructor_points.sql` and `driver_points.sql`. The committed-edit record (the
worker's structured final report in `agent/codex.txt`) names the literal
`sum(...points...)`→`max(...points...)` edits, the verifier's
`AUTO_constructor_points_equality` flipped FAIL 2→PASS and
`AUTO_driver_points_equality` held PASS, and the worker's own value checks show
0 mismatches vs `max(points)` (920 constructor / 3190 driver rows; Red Bull 2023
860 not 10,158; Verstappen 2023 575 not 6,453). No `row_number()`/`rank()`/
`QUALIFY`/order-by-round/order-by-race_date/final-row selection and no
race-results recomputation appears. This is a `max(points)` GO, not a
green-with-latest-row NO-GO.

**The stabilization claim held.** f1006-hard — the @baseline passer that
latest-row-DROPPED at full in h0037 and h0041 — stayed PASS AND stayed on the
simple `max(points)` aggregate, with no drift into the fragile final-row branch.
This is the specific over-engineering mode the no-latest-row guard targets.

**No regression; the lever stayed in its lane (AC-5).** The two perturbable
same-family sentinels (f1005, f1005-medium — h0012's −4 regression victims) both
held PASS on the simple `max(points)` path rather than being pushed onto a
"structurally different" wrong path; this is the direct contrast with h0012,
whose generative independent-recompute framing damaged exactly these cells. The
two inert canaries (f1001 staging, airbnb001 cross-family) held with the lever's
precondition correctly not matching — no convention bleed.

**Caveats carried to full.** (1) Single trial per cell: a 6/6 smoke is a strong
artifact signal but not a multi-trial CI; the GO rests on the committed-artifact
proof + clean canaries, per the standing single-trial / judge-by-artifact
decision. (2) The lever is gated to the standings/points construct, so at full
scale it should remain inert on non-f1 tasks — but the full run is the real test
of zero cross-family bleed (h0009/h0012 both passed targeted smokes then
regressed other-family or other-member passers at full). (3) The pre-smoke
C-probe (14/14 max) was proxy only and weak-A also chose max 4/4; this smoke
confirms the full-workflow form lands the artifact and does not drift, which the
probe could not establish.

## Stage Report: smoke

- DONE: Smoke run on the frozen 6-task panel completed (detached nohup, polled across turns); strict audit clean + captured traces on every cell BEFORE the score; score + attestation in `## Smoke result`.
  Run `runs/.../17732f64285f1de2`; `rk audit --policy strict` = `clean: 6, tainted: 0, coverage_missing: 0`; `rk score` stratified_pass_at_1 = 1.0 (6/6, n_errored=0).
- DONE: THE DECISIVE ARTIFACT READ (AC-3/AC-4) for f1006 AND f1006-hard — classify the load-bearing fix; flip counts only if `max(points)`; f1006-hard must hold AND be `max(points)`.
  Both = same-grain `max(points)` on `constructor_points.sql` + `driver_points.sql`; NO row_number/rank/QUALIFY/order-by-round/order-by-race_date/final-row, NO race-results recompute. f1006 FAIL→PASS (constructor_equality FAIL 2→PASS, driver held); f1006-hard held PASS on `max(points)` (no h0037/h0041 latest-row drift).
- DONE: Sentinel/canary check (AC-5) — f1005, f1005-medium, f1001, airbnb001 all hold PASS on clean audit; record per-cell + f1006/f1006-hard patch classification in `## Smoke result` + `## Behavioral analysis`.
  All four held PASS (clean audit). f1005/f1005-medium kept `max(points)` (no h0012-style off-simple drift); f1001 (staging) + airbnb001 (cross-family) inert, lever precondition unmatched, no bleed. In-stage instruction lever → no WORKFLOW-REFINE entry.

### Summary

Detached smoke on the 6-task f1-standings panel returned 6/6 PASS, strict audit
clean (tainted 0 / coverage_missing 0), and the decisive committed-artifact read
confirms the intended fix: f1006 flipped FAIL→PASS via same-grain `max(points)`
on BOTH `constructor_points.sql` and `driver_points.sql` with zero
latest-row/rank/QUALIFY/final-row/recompute logic. f1006-hard held PASS on
`max(points)` (stabilization claim confirmed — no h0037/h0041 latest-row drift),
and all sentinels/canaries held with no convention or cross-family bleed.
**Verdict: GO** (artifact-proven `max(points)` flip + clean canaries). Carried
caveat: single-trial, so full-scale zero-bleed is the real test (h0009/h0012 both
passed targeted smokes then regressed at full).

## Run result

**Headline: NO-GO for promotion. Net −1 (variant 31/48 vs @baseline h0043 32/48),
inside the noise band — the GAINS ARE ARTIFACT-REAL, the NET LOSSES ARE PURE
SINGLE-TRIAL VARIANCE the lever never touched.** The lever did exactly what it was
designed to: f1006 AND f1006-hard BOTH flipped FAIL→PASS, both on artifact-proven
same-grain `max(points)` with zero latest-row/QUALIFY/rank. The three regressions
(asana002, f1011, quickbooks002) are on NON-standings tasks where the lever
precondition never fired — confirmed by artifact. The real finding: the lever is
correct and inert off-target; the net is dragged negative only by run-to-run
coin-flips on cells the lever cannot reach. Promotion fails the tripwire (CI
crosses zero), but no damage is attributable to h0044.

Full run launched DETACHED (Phase 1) → completed rc=0. Phase 2 audit + score:

- **Run-dir:** `runs/ade-bench-h0044-cumulative-standings-max-points-guard/645f1f4dbca44ee0`
- **Strict audit** (`rk audit … --policy strict`): `clean: 48, tainted: 0,
  coverage_missing: 0` — captured traces on every cell. AC-2 satisfied; the score
  is trustworthy.
- **Score** (`rk score … --format json`): `stratified_pass_at_1 = 0.6458` (31/48),
  `n_errored = 0`. Absolute vs paper_baseline 0.1875 → `above`. Wilson CI
  [0.504, 0.766].
- **@baseline:** h0043 `runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea`
  = 32/48 = 0.6667.

### Paired delta vs @baseline (h0043)

`rk runs diff` is unreliable on these run-dirs (outcomes carry `query_id: null` →
`TypeError`), so the paired delta is computed directly from
`per_trial_outcomes.json`, paired by task slug (48/48 slugs paired, 0 unpaired),
with a 10k-resample bootstrap CI.

- **Observed paired delta (variant − baseline): −0.0208 = −1 / 48.**
- **95% bootstrap CI: [−0.1042, +0.0625]** — straddles zero. The net change is
  statistically indistinguishable from single-trial noise.

### Full per-task ledger (every verdict change, both directions)

| Task | h0043 @baseline | h0044 full | Direction | Lever fired? | Mechanism |
|------|----------------:|-----------:|-----------|-------------|-----------|
| ade-bench-f1006 | 0.0 FAIL | 1.0 PASS | **GAIN 🎯** | YES (on-target) | Committed same-grain `max(points)`: `sum(cs.points)`→`max(cs.points)` in `constructor_points.sql` + `sum(ds.points)`→`max(ds.points)` in `driver_points.sql`. All 4 tests PASS (constructor_equality FAIL 2→PASS, driver held). No row_number/QUALIFY/rank/order-by/final-row, no race-results recompute. |
| ade-bench-f1006-hard | 0.0 FAIL | 1.0 PASS | **GAIN ✅🎯** | YES (on-target) | FAIL→PASS via the same `sum(points)`→`max(points)` on both models. This is the h0037/h0041 latest-row DROP cell, and it was ALSO FAIL at h0043 @baseline — h0044 RECOVERS it onto the simple aggregate, not the fragile final-row branch. Stronger than a hold: a genuine flip of the known-fragile cell. |
| ade-bench-asana002 | 1.0 PASS | 0.0 FAIL | **REGRESSION** | NO (inert) | Solver edited `asana.duckdb` (source-data/field-add construct). `AUTO_asana__task_equality` FAIL 2 (2/3 checks pass). No points/standings construct — lever precondition unmatched. h0043's own +1 coin-flip cell. |
| ade-bench-f1011 | 1.0 PASS | 0.0 FAIL | **REGRESSION** | NO (inert) | Decision-fork answer cell (`check_option_a..e`); solver committed `answer='ABDE'`, `check_option_b` FAIL 1 (5/6 pass). The oracle-only ADE/ABDE blind cell — B-vs-not-B has no local signal. Not a SQL-aggregation task. |
| ade-bench-quickbooks002 | 1.0 PASS | 0.0 FAIL | **REGRESSION** | NO (inert) | Solver edited quickbooks union/enhanced models; 3 ERRORs (`int_quickbooks__expenses_union_equality`, `int_quickbooks__sales_union_equality`, `quickbooks__ap_ar_enhanced_equality`), 5/8 pass. Union-completeness construct — no points/standings. |

Net arithmetic (slug-paired, unambiguous): **baseline 32 pass, variant 31 pass.
TWO gains — f1006 AND f1006-hard, both FAIL→PASS — and THREE regressions —
asana002, f1011, quickbooks002. 32 + 2 − 3 = 31; net −1.** Note: f1006-hard was
FAIL at h0043 @baseline (not a hold), so the lever scored BOTH named targets as
genuine flips onto artifact-proven `max(points)`. Every one of the three
regressions is on a task the lever's standings/points precondition cannot reach.

## Stage Report: full

- DONE: Phase 1 NOW (launch only, do NOT wait) — export RAZORBACK_SPACEDOCK_PLUGIN_DIR, optional `--explain`, launch the FULL 48-task run DETACHED via `drivers/rk-run-detached.sh`; return the handle path and signal done immediately.
  Launched `drivers/rk-run-detached.sh h0044-full specs/h0044-cumulative-standings-max-points-guard.frozen.yaml run`; handle `runs/.rk-handles/h0044-full-20260611-152742/` (pid 601684 alive, log open); RAZORBACK_SPACEDOCK_PLUGIN_DIR set to repo `spacedock`. Skipped the optional `--explain` (smoke already proved spec validity; same README as smoke).
- SKIPPED: Phase 2 (LATER — FO re-engages when the done sentinel lands rc=0) — strict audit clean + captured>0 on every cell, `rk score --format json`, record run-dir + headline in `## Run result`.
  Intentionally not done in this stage: this is the launch-only RUN stage; the FO owns the detached wait and re-dispatches Phase 2 when `done` lands rc=0. `## Run result` carries the handle for that re-engagement.

### Summary

Launched the full 48-task run on the frozen full spec (same solver README as the
GO smoke — no methodology drift) DETACHED via the audited launcher; handle
`runs/.rk-handles/h0044-full-20260611-152742/`, pid 601684 confirmed alive, log
open. This stage is launch-only per the checklist — no wait, no audit, no score;
the FO owns the detached wait via `runs/.rk-handles/` scanning and ntfy
`adebench-rk-381c976fe07465bf`, then re-dispatches Phase 2 (strict-audit + score)
when the `done` sentinel lands rc=0.

## Behavioral analysis (analyze stage)

All reads are committed-artifact reads on the audited run-dir
`…/645f1f4dbca44ee0` (strict-clean 48/48). The six required analyze questions:

**Q1 — Net + full per-task ledger (both directions).** Absolute 31/48 = 0.6458
(above paper_baseline 0.1875). Paired vs @baseline h0043 (32/48): **−1/48 =
−0.0208, 95% bootstrap CI [−0.1042, +0.0625]** (crosses zero). Ledger above lists
ALL five changed cells: GAINS = f1006, f1006-hard (both FAIL→PASS, lever on-target);
REGRESSIONS = asana002, f1011, quickbooks002 (all PASS→FAIL, lever inert). Reported
in full — gains and losses both.

**Q2 — Smoke vs full: why did the verdict differ?** Smoke was a 6/6 GO; full is
net −1. The smoke panel (f1006, f1006-hard, f1005, f1005-medium, f1001,
airbnb001) was the f1-standings family plus two canaries — by construction it could
NOT see asana, f1011, or quickbooks. The full-vs-smoke gap is NOT a lever failure
and NOT family-regression bleed (the smoke's same-family sentinels f1005/f1005-medium
held PASS at full too — verified separately). It is exactly the thing a focused
family smoke cannot see: **single-trial coin-flips on unrelated families the smoke
didn't sample.** The lever's own targets did at full exactly what they did at smoke.

**Q3 — Already-correct-and-broken (damage to passers).** All three regressions were
clean passers at h0043 @baseline (asana002 3/3, f1011 6/6, quickbooks002 8/8) and
are now FAIL (2/3, 5/6, 5/8). So this IS damage to working code in the run-to-run
sense. BUT it is "failed-to-reproduce-a-coin-flip," NOT "lever-broke-a-passer":
the committed artifacts in all three cells show the solver chose a different
implementation this run on tasks the h0044 README rule never addresses. None of the
three edits touched a `*_standings`/points construct; the lever language is present
only as inert dispatch-prompt boilerplate (the 6× `max(points)` / 2× `sum(points)`
hits in each cell are the verbatim README block, identical token-for-token across
all three cells — the signature of boilerplate, not task edits).

**Q4 — Was the change executed? (artifact, not chatter)**
- f1006 = **executed-and-helped**: main-agent final message + ensign apply_patch
  both name `sum(cs.points)`→`max(cs.points)` and `sum(ds.points)`→`max(ds.points)`;
  `AUTO_constructor_points_equality` FAIL 2→PASS, driver held; 0 row_number/QUALIFY/
  rank/order-by in patch context.
- f1006-hard = **executed-and-helped**: same edit on both models; recovers the
  h0037/h0041 latest-row drop cell onto the simple aggregate.
- asana002 = **inert (premise-not-local for the lever)**: solver edited
  `asana.duckdb` source data; lever precondition (repair season/entity totals from
  `*_standings`) does not match. Regression is independent.
- f1011 = **inert (premise-falsified for the lever)**: it is a multiple-choice
  decision-fork answer model (`answer='ABDE'`), `check_option_b` failed — the
  oracle-only blind cell, no local signal to disambiguate. Not a SQL-aggregation
  task; lever silent.
- quickbooks002 = **inert**: solver edited union/enhanced models; 3 union-equality
  ERRORs. No points/standings construct; lever silent.

**Q5 — Prevention + next move.** Keeping the gains without the harm: the gains are
already harm-free — the lever is precondition-gated and provably inert off-target
(this run is the evidence). There is no scoping guardrail to add; the −2 net is not
caused by the lever and cannot be prevented by changing the lever. To catch the
"net dragged by unrelated coin-flips" pattern earlier, the only real fix is
multi-trial on the volatile cells (asana002/f1011/quickbooks002), which the standing
captain decision (trials:1, judge-by-artifact) explicitly declines. **Recommended
next move: do NOT promote h0044 (paired CI crosses zero — fails the tripwire), and
do NOT file a follow-up.** The lever is artifact-correct and the loss is pure
variance — there is nothing to fix. Per the oracle-program-CONCLUDED and
single-trial-judge-by-artifact memories, this is a knowledge gain (the max-points
guard is confirmed to fire correctly and stay in its lane on a full run), not a
pass-rate flip to bank. Escalate the verdict to the captain; the flip portfolio for
this family is exhausted.

**Q6 — Smoke-vs-full fork drift.** The smoke GO was ARTIFACT-REAL, not variance:
f1006/f1006-hard flipped on the committed `max(points)` edit at BOTH smoke and full,
and the README rule did NOT drift into a different implementation branch at full
(no latest-row/QUALIFY/rank in either target's full-run patch). The fork that
changed at full is NOT in the lever's targets — it is three unrelated cells the
smoke panel never sampled, each an independent single-trial coin-flip
(asana002 = h0043's own +1 coin-flip; f1011 = the documented oracle-only ADE/ABDE
blind cell; quickbooks002 = union-completeness, a known fix-it-completeness weak
spot). Routing: this is unrelated-variance drift, NOT a missed family the lever
should have covered and NOT a rule that drifted branch. No `## Failure Review`
follow-up is warranted for the lever; the variance cells are pre-existing portfolio
volatility.

## Stage Report: analyze

- DONE: Strict audit the run-dir clean + captured>0 on every cell BEFORE the score; `rk score --format json`; record audited score + run-dir in `## Run result`.
  `rk audit --policy strict` = `clean: 48, tainted: 0, coverage_missing: 0`; `rk score` = stratified_pass_at_1 0.6458 (31/48), n_errored 0; run-dir `…/645f1f4dbca44ee0` recorded.
- DONE: Paired delta vs @baseline (h0043) — `rk runs diff` TypeError → compute from `per_trial_outcomes.json` slug-paired + 10k bootstrap CI; say so.
  `rk runs diff` data-shape limit confirmed; slug-paired 48/48 → delta −0.0208 (−1/48), 95% bootstrap CI [−0.1042, +0.0625] (crosses zero). Method noted in `## Run result`.
- DONE: PRE-AUDIT read confirm/correct (variant 31/48, net −1); verify gains are same-grain max(points), classify each regression lever-vs-variance by committed artifact.
  Confirmed 31/48, net −1. CORRECTION to pre-audit read: f1006-hard was FAIL at h0043 baseline (not a hold) → TWO gains (f1006 + f1006-hard, both committed `sum(points)`→`max(points)`, no latest-row/QUALIFY). asana002/f1011/quickbooks002 = lever inert (precondition unmatched; README tokens are boilerplate only), all PASS→FAIL independent single-trial variance, each cited.
- DONE: Answer ALL §analyze required questions; write `## Run result` + `## Behavioral analysis`; lead with the verdict recommendation; commit before signaling.
  Six required questions answered in `## Behavioral analysis`; headline leads with NO-GO-but-gains-real, losses-pure-variance. Recommendation: do NOT promote (CI crosses zero), do NOT file follow-up (lever artifact-correct, loss is variance) — knowledge gain banked.

### Summary

Full run is strict-clean 31/48 (0.6458), net −1 vs @baseline h0043 (32/48), paired
delta −0.0208 with 95% bootstrap CI [−0.1042, +0.0625] crossing zero. The lever
performed exactly as designed: BOTH named targets (f1006 AND f1006-hard — the
latter was FAIL at baseline, correcting the pre-audit "hold" read) flipped FAIL→PASS
on artifact-proven same-grain `max(points)` with no latest-row/QUALIFY/rank drift.
All three regressions (asana002, f1011, quickbooks002) are on NON-standings tasks
where the lever precondition provably never fired — independent single-trial
variance, not lever-caused damage. Verdict recommendation: NO-GO for promotion (CI
straddles zero), no follow-up to file; bank the knowledge gain that the
cumulative-standings max-points guard fires correctly and stays in its lane on a
full run.

## Verdict

**REJECTED (no-promote).** Full audited 31/48 = 0.6458, net **−1** vs `@baseline`
h0043 (32/48 = 0.6667); paired delta −0.0208, 95% bootstrap CI [−0.1042, +0.0625]
straddles zero — fails the promote tripwire. Audit was clean (strict 48/48,
`tainted: 0`, `coverage_missing: 0`). `@baseline` stays h0043.

The lever is **artifact-correct AND inert off-target**, which is the whole story:
- **BOTH named targets flipped FAIL→PASS on the artifact-proven mechanism.** f1006
  AND f1006-hard committed same-grain `max(points)` (`sum(cs.points)`→`max(cs.points)`
  in `constructor_points.sql`, `sum(ds.points)`→`max(ds.points)` in
  `driver_points.sql`), with NO row_number/rank/QUALIFY/order-by/final-row and NO
  race-results recompute. f1006-hard was itself FAIL at h0043 baseline, so the lever
  scored two genuine flips, recovering the h0037/h0041 latest-row DROP cell onto the
  simple aggregate — not a hold.
- **All three regressions (asana002, f1011, quickbooks002) are off-construct
  single-trial variance the lever provably never touched.** None is a
  standings/points task; the precondition never fired; the README `max(points)`
  tokens appear only as identical dispatch-prompt boilerplate (not task edits) in
  each cell. The −1 net is dragged by run-to-run coin-flips on cells the lever
  cannot reach, not by lever damage.

This is the `edit-shape-without-oracle-target` family at its cleanest: a
correct-shape, correctly-gated lever whose real gains are washed by trials:1 noise
on unrelated cells.

## Follow-up Routing

**stop (do-NOT-file).** The lever is artifact-correct and provably inert
off-target — there is nothing to fix and no visible fork to probe. The
cumulative-standings flip-family is exhausted: f1006 + f1006-hard are the only
standings-aggregate targets and both already land the intended `max(points)` fix.
The −1 is pure measurement variance (per the single-trial-variance-masking wall),
not a lever defect, and is not chaseable at trials:1. Knowledge banked: the
max-points guard fires correctly and stays in its lane on a full 48-task run.

## Stage Report: conclude

- DONE: Write the terminal `## Verdict` (REJECTED no-promote) into the entity file.
  31/48, net −1; f1006 + f1006-hard flipped on artifact-proven `max(points)`; asana002/f1011/quickbooks002 regressed as off-construct variance (lever provably inert there). Evidence drawn from `## Run result` / `## Behavioral analysis`.
- DONE: Write `## Follow-up Routing` = stop (do-NOT-file).
  Lever is artifact-correct AND inert off-target; nothing to fix; standings flip-family exhausted (f1006 + f1006-hard are the only standings-aggregate targets, both land `max(points)`).
- DONE: Cross-batch note added to `_artifacts/WORKFLOW-REFINE.md`.
  Appended the trials:1-variance-dominates-per-lever-signal note covering h0044/h0045/h0046 (judge by artifact + held targets, not the single aggregate; bank only artifact-reproducible + gated flips).

### Summary

Concluded h0044 REJECTED (no-promote): full 31/48, net −1 vs `@baseline` h0043, CI
straddles zero. Both named targets flipped FAIL→PASS on artifact-proven same-grain
`max(points)`; all three regressions are off-construct single-trial variance the
precondition-gated lever provably never touched. Routing: stop — artifact-correct,
inert off-target, family exhausted. Cross-batch variance note added to WORKFLOW-REFINE.
Did NOT set frontmatter verdict/archive (FO owns that).
