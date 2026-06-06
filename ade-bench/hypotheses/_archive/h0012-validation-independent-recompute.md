---
id: h0012
title: Validation — reconcile one key figure (and row count) against an INDEPENDENT derivation from raw source, never against your own re-run
status: conclude
kind: hypothesis
source: concept-resolve-uncovered-false-greens fan-out; evidence re-audit of @baseline (622bdedac572b479, 31/48). The heavyweight cluster — 6 value-divergence false-greens (ana-eng006, ana-eng007, airbnb007, asana005-hard, f1006, airbnb009). This is the ONLY proven lever (the f1007-hard catch worked solely because it compared an independent number). The dead part is *self-anchored* checks, not the Validation stage itself (per docs/baseline-validation-self-anchored-false-green.md §4). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-04T13:40:51Z
completed: 2026-06-06T22:49:08Z
verdict: REJECTED
score:
worktree:
archived: 2026-06-06T22:49:09Z
---

## Hypothesis

The baseline false-green finding established that the only self-check that ever caught a real
bug (`f1007-hard`) worked **solely because it compared against an independent number** — the
raw `results` table counted a structurally different way (3,373 vs the season-table sum
3,372). Every other check was self-anchored and confirmed the solver's own wrong derivation.
The re-audit confirms the largest uncovered cluster is exactly this shape:

- `ana-eng006`, `ana-eng007` (`AUTO_dim_products_equality`, `Got 5`): 5 row-level **value**
  mismatches; the solver only ran `dbt run`/spot-checks, never recomputed the values.
- `airbnb007` (`daily_agg_nps_reviews_equality_with_tolerance`, `Got 4`): 4 value mismatches;
  validated NPS ranges and row counts (shape), not values.
- `asana005-hard` (`AUTO_int_asana__project_user_agg_equality`, `Got 3`): refactor diverges;
  the self-check (`mismatch_count=0`) compared the refactor to its **own** re-derivation.
- `f1006` (`AUTO_constructor_points_equality`, `Got 2`): summed **all** cumulative season
  rows instead of the final standing (11–22× overstated); the solver even *observed* the
  discrepancy, then "validated" by re-running its own build without an independent recompute.
- `airbnb009` (`mom_agg_review_date_range`, `Got 1`): a continuous-spine fix over-produced
  rows (13,524 vs the expected 12,278) — an independent **row-count** recompute from source
  grain would have caught it.

The seed solver's Validation prose says "do additional correctness checks beyond it builds"
and "match the source-data expectation," but the solver operationalizes this by re-running its
own model or comparing to the pre-existing code — which shares the bug's blind spot.

**Falsifiable claim (the single README change — Validation stage only):** adding one
Validation instruction — *when validating a numeric result, reconcile at least one key figure
against an INDEPENDENT derivation computed straight from the raw source tables by a
structurally different path (a different join order/grain, or a coarser source-level count),
and reconcile the model's row count against the count implied by its declared grain on the
raw source; treat any disagreement as a real defect to root-cause and fix; do NOT "validate"
by re-running your own model or comparing to the pre-existing code, because a check that
reuses your own derivation shares its blind spot* — and which ships with a concrete
worked-example recompute skeleton (an independent raw-source derivation of one figure plus a
grain-implied row-count reconcile), not abstract prose alone — will catch the value-divergence and
wrong-row-count failures (ana-eng006/007, airbnb007, asana005-hard, f1006, airbnb009) and let
the solver fix them, raising `stratified_pass_at_1` above the `@baseline` 0.6458.

This is the report's surviving direction #1 (independent invariant) stated as a generic
Validation rule — NOT the dead self-verification family (h0006/h0007/h0008), which compared
against the solver's own re-derivation. The distinguishing instruction is the explicit ban on
self-anchored re-runs and the demand for a structurally different derivation path. One idea,
one stage (Validation).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact (raw local source tables only — no public fetch, no
oracle, no reference to hidden `AUTO_*`/`solution__*` tests).

Target datasets (smoke, all `ade-bench-` prefixed): a representative spread of the cluster —
`ade-bench-ana-eng006`, `ade-bench-airbnb007`, `ade-bench-f1006`, `ade-bench-airbnb009`. This
rule is **generative** (it fires on every numeric task, not gated on a precondition), so per
gatekeeper G8 the smoke set additionally carries a cross-family regression-canary panel — one
currently-passing `@baseline` task from each other family: `ade-bench-asana001` (asana),
`ade-bench-quickbooks002` (quickbooks), `ade-bench-f1001` (f1 — the exact task the h0009
convention-bleed broke), `ade-bench-ana-eng001` (ana-eng), and `ade-bench-airbnb001` (airbnb
passer / sentinel). **No intercom canary is possible:** intercom has no passing `@baseline`
task (`intercom001/002/003` all fail), so that family cannot supply a passer — G8 should not
expect one.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0012-validation-independent-recompute.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Validation` (the single independent-recompute rule), leaves
Exploration/Implementation/Finalization and the dependency/package guardrails untouched, and
does not reference hidden `AUTO_*`/`solution__*`/verifier tests or weaken the leak-guard.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on the 4 targets + `airbnb001` sentinel, the variant must not regress the
sentinel and should flip at least one of the 4 value-divergence failures to a pass before
promotion to full.

## Smoke result

Run-dir `runs/ade-bench-h0012-validation-independent-recompute/9efca9a9001b7262` — `stratified_pass_at_1 = 0.7778` (7/9). Strict audit clean (`clean: 9, tainted: 0, coverage_missing: 0`). Per-task vs `@baseline` (`622bdedac572b479`):

| Task | Role | @baseline | smoke | Result |
|------|------|-----------|-------|--------|
| f1006 | TARGET | 0.0 | 1.0 | **FLIP → PASS** |
| airbnb007 | TARGET | 0.0 | 1.0 | **FLIP → PASS** |
| ana-eng006 | TARGET | 0.0 | 0.0 | held FAIL (inert) |
| airbnb009 | TARGET | 0.0 | 0.0 | held FAIL (inert) |
| airbnb001 | canary | 1.0 | 1.0 | held PASS |
| ana-eng001 | canary | 1.0 | 1.0 | held PASS |
| asana001 | canary | 1.0 | 1.0 | held PASS |
| f1001 | canary | 1.0 | 1.0 | held PASS |
| quickbooks002 | canary | 1.0 | 1.0 | held PASS |

Two real flips, zero canary regressions, clean audit. Smoke gate met (flips ≥1 target, sentinel airbnb001 held).

## Run result

**Full run-dir** `runs/ade-bench-h0012-validation-independent-recompute/3d8294de42b726e1` —
`stratified_pass_at_1 = 0.5625` (27/48). **@baseline** `622bdedac572b479` = 0.6458 (31/48).
**NET −4.** Strict audit on the full run-dir is clean (`clean: 48, tainted: 0,
coverage_missing: 0`) → AC-2 satisfied.

**Paired delta (AC-3).** `rk runs diff` TypeErrors on these run-dirs (`query_id: null`, the
known ade-bench data-shape limitation), so the delta was computed directly from
`per_trial_outcomes.json` paired by task slug (48/48 slugs matched, no orphans), with a
10,000-iteration paired bootstrap:

- point delta = **−0.0833** (variant 0.5625 − baseline 0.6458)
- paired 95% CI = **[−0.2083, +0.0208]** — straddles 0 and tilts negative
- discordant: **2 gains, 6 regressions, net −4**

The CI **does not clear the promotion tripwire** (it must *exclude* a regression; here it
includes one and most of the mass is ≤ 0) and the absolute score 0.5625 is **below** @baseline
0.6458. **Both promotion conditions fail.**

### Full per-task ledger (BOTH directions)

| Task | @baseline | variant | Δ | family | mechanism |
|------|-----------|---------|---|--------|-----------|
| airbnb007 | 0 | 1 | **+GAIN** | airbnb | reconcile fired on raw NPS/review-count + per-model grain row-counts → drove the value fix (executed-and-helped; held from smoke) |
| asana002 | 0 | 1 | **+GAIN** | asana | reconcile fired (model-rows vs source-rows vs distinct-IDs, "0 mismatches") → flipped `AUTO_asana__task_equality Got 2`→PASS. Known causal-flip task (h0009 also flipped it); reconcile reached the artifact (executed-and-helped, partly task-volatile) |
| ana-eng003 | 1 | 0 | **−REGR** | ana-eng | broke a passer: variant rewrote `dim_customer` to **5 columns + an enforced contract** (dropped 13 cols baseline kept); `AUTO_dim_customer_equality` ERROR ("less columns than expected") |
| f1003-hard | 1 | 0 | **−REGR** | f1 | broke a passer: answer-selection task — variant committed **6 answers** (baseline 3); `count_answers Got 1` (one over-included wrong answer) |
| f1005 | 1 | 0 | **−REGR** | f1 | broke a passer: first applied the CORRECT `sum→max` (= baseline), then a **2nd patch reverted `max`→`row_number() … standings_rank=1`** (last-race-by-date) → `AUTO_constructor_points_equality Got 2` |
| f1005-medium | 1 | 0 | **−REGR** | f1 | broke a passer: same model, went straight to `standings_rank=1` last-race path instead of baseline's `max(points)` → `Got 2` |
| f1006-hard | 1 | 0 | **−REGR** | f1 | broke a passer: same `sum→standings_rank=1` last-race rewrite of constructor_points + driver_points → `Got 2` |
| quickbooks003 | 1 | 0 | **−REGR** | quickbooks | broke a passer: "remove department" task — variant `{% if var %}`-gated the department code + left `models/quickbooks.yml` un-patched (baseline deleted the code and patched the yml) → 3 equality tests ERROR. Solver-path divergence, weakest reconcile linkage |

Note: **f1006 itself stayed FAIL (0→0) at full** — the celebrated smoke `sum→max` flip did NOT
hold at full scale (variance), while the same rule broke 4 of f1006's siblings.

## Behavioral analysis

> **NOTE — the section below (subsections a/b/c) is the SMOKE-run analysis written at the smoke
> stage.** The FULL-run behavioral analysis (the load-bearing damaged-passer read) is in
> **§ FULL-RUN behavioral analysis** further down.

### (a) Distance-to-pass on the 2 held targets (verifier `Got N`, smoke vs @baseline)

- **ana-eng006 — INERT.** Baseline & smoke verifier outputs are byte-equivalent in shape: `AUTO_fact_inventory_equality` **Got 204** (both), plus `AUTO_dim_products_equality` and `AUTO_obt_product_inventory_equality` ERROR (compile/column-count, the "has less columns than expected" shape) in both; `pass=4 fail=3` in both. `Got N` unchanged (204 → 204) ⇒ the rule is inert on this cell. (Note: the entity body's per-task characterization said `AUTO_dim_products_equality Got 5`; the actual @baseline shape is a 204-row `fact_inventory` value mismatch + two column-count compile errors. The distance metric — unchanged 204 — is what's load-bearing.)
- **airbnb009 — INERT.** `mom_agg_review_date_range` **Got 1** in both baseline and smoke; `fail=1` both. Unchanged ⇒ inert on this cell.

### (b) Committed-SQL read — the independent-recompute reconcile FIRED and reached the committed SQL on the flips

**f1006 (flipped-because-reached-SQL):** the worker ran the h0012 reconcile *before* committing, used the disagreement to root-cause, then committed the fix.
- Committed model patch (apply_patch, `…/ade-bench-f1006__LERUBYG/agent/sessions/…019e9ca2….jsonl` line 164): `sum(cs.points) → max(cs.points)` in `constructor_points.sql` and `sum(ds.points) → max(ds.points)` in `driver_points.sql` — exactly the h0012-predicted "summed all cumulative season rows instead of final standing" bug, fixed at season grain.
- Independent reconcile that drove it (same session, line 145 output): a `dbt show --inline` query reconciling the model figure against TWO structurally-different derivations — `max(points)` from `*_standings` AND `sum(points)` from a *different source table* `stg_f1_dataset__results`/`constructor_results`. Output exposed the inflation (Max Verstappen 2023: model **6,453** vs independent **575/530**), plus a grain-implied row-count reconcile (`actual_rows=3190 == expected_rows=3190`). This is the rule's exact demand (independent path + row-count reconcile), not chatter — the reconcile query is in the committed artifact and preceded the `max()` patch.

**airbnb007 (corroborating flip):** subagent report (`…/ade-bench-airbnb007__k9sVo4M/agent/codex.txt` line 26) records "Raw-source listing NPS reconciliation: 14243 listings compared, **0 NPS mismatches, 0 review-count mismatches**" and "raw daily 28-day reconciliation for 2021-10-22: model nps_28d=45, reviews_28d=7399; **raw matched exactly**" + per-model grain row-count reconciles — the independent-raw-source reconcile fired across all six committed models.

### (c) Why ana-eng006 still failed — blind-to-oracle wall (the rule fired but couldn't see the oracle)

The ana-eng006 worker **did** run the independent reconcile (report at `…/ade-bench-ana-eng006__YaYamSQ/agent/codex.txt` line 23): raw `inventory_transactions` joined directly to raw `products` vs `obt_product_inventory` → **0 product-level mismatches**; quantity total **6615** matched across source/`fact_inventory`/`obt`; grain row-counts all 102. The reconcile reported clean agreement — yet the verifier shows `AUTO_fact_inventory_equality` **Got 204** value mismatches + two column-count compile errors. The worker's independent derivation was self-consistent on the dimensions it chose (counts, quantity totals, product-name joins) but **orthogonal to the oracle's expected output** (specific column set + per-row values it has no visibility into). Independent-from-raw redundancy beats *self-anchored* error, but it cannot recover an unknown column/value contract — the same blind-to-oracle wall noted for the verify-the-target family. Hence inert here, not closer.

## FULL-RUN behavioral analysis

Cells read on the FULL run (`3d8294de42b726e1`) vs @baseline (`622bdedac572b479`), committed
`apply_patch` artifacts (not chatter), from `…/agent/sessions/**/*.jsonl`.

### The load-bearing question — did the reconcile DAMAGE passers? YES, and via a mechanism the dispatch hypothesis under-specified.

The dispatch's predicted harm was "solver computes a WRONG independent derivation, sees it
disagree with its already-correct model, and 'fixes' the correct model to match the wrong
number." The artifacts show a **more insidious variant**: the rule pushed the solver **off a
simple correct path onto an over-engineered "structurally different" path that is subtly wrong,
then the model's *own* reconcile agreed with it (correlated, not independent).**

**The f1 constructor_points cluster (4 of 6 regressions) — the smoking gun.**
- @baseline solved f1005 / f1005-medium / f1006-hard with **one** patch: `sum(points) →
  max(points)` grouped by season. `max` over cumulative standings = the final standing.
  CORRECT → all PASSED (confirmed: baseline patches show `sum→max` only).
- The variant, driven by the h0012 "reconcile by a structurally different path" rule,
  **abandoned `max`** for a `row_number() OVER (… ORDER BY race_date DESC, round_number DESC,
  race_id DESC) … WHERE standings_rank = 1` path (pick the points of the *chronologically last
  race* of the season). For f1005 this happened as a **second patch that explicitly reverted
  the correct `max`** it had just written (session `…019e9e76…` line 118 = `sum→max`, line 174
  = `max → cs.points + standings_rank=1`).
- "last race by date" ≠ "max cumulative points" on 2 rows per dataset (`Got 2`): ordering
  ties / a season whose final-date row is not the points-max. The result is a wrong table.
- **The reconcile then "confirmed" the wrong model** (f1006-hard session `…019e9e92…` lines
  151–152): the solver reconciled `constructor_points` against a `latest_constructor` CTE built
  with the **same** `standings_rank=1` logic → `cp_mismatch_latest = 0`, Verstappen 575, etc.
  This is **correlated redundancy, not independent** — the check reused the model's own new
  derivation, so it could not see the defect. The solver even *observed* a real source
  discrepancy ("2023 exposes sprint points present in standings but not in race results",
  line 109) and resolved it by trusting standings — entrenching the wrong grain.

This is the exact false-green wall in the memory note (`verification-without-oracle-real-world`):
a second derivation that *looks* independent but is correlated with the first cannot catch the
error, and worse, the rule's demand to "treat any disagreement as a defect and fix" **converted
a correct simple model into a wrong elaborate one.** The rule's false-positive cost is realized.

**ana-eng003 (regression) — "declare your grain" over-formalization.** Baseline built
`dim_customer` with all 18 source columns (PASS). Variant emitted a 5-column model **plus a new
`schema.yml` with `contract: enforced: true`** and a 5-column contract (and `email_address
data_type: integer`, itself wrong). `AUTO_dim_customer_equality` ERROR ("less columns than
expected"). The row-count/grain-reconcile framing nudged toward formalizing a narrow contract
instead of reproducing the full table — damage to a passer.

**f1003-hard (regression) — over-inclusion bias.** Not a numeric task at all (answer-selection:
which questions are answerable). Baseline committed exactly 3 correct answers; variant committed
6 (added `most_podiums`, `most_pole_positions`, `most_races`) → `count_answers Got 1` (one wrong
over-inclusion). The generative rule perturbs even non-numeric tasks; "treat disagreement as a
defect to fix" biases toward action/inclusion.

**quickbooks003 (regression) — solver-path divergence (weakest reconcile link).** "Remove the
department feature" task. Baseline deleted the department CTEs/joins/columns and patched
`models/quickbooks.yml`; variant `{% if var('using_department') %}`-gated the code and **left
`quickbooks.yml` un-patched** → 3 equality ERRORs. Most attributable to path variance + extra
validation overhead consuming turns, not a direct wrong-derivation; counts against the
generative rule's churn but is the least clean causal attribution of the six.

### The 2 gains are executed-and-helped (reconcile reached the artifact)
- **airbnb007** (held from smoke): raw-source NPS / review-count reconcile (14243 listings, 0
  mismatches) + per-model grain row-counts fired across all committed models → value fix → PASS.
- **asana002** (new at full, not in smoke set): reconcile compared model-rows vs source-rows vs
  distinct-IDs ("0 mismatches") and the task flipped `AUTO_asana__task_equality Got 2`→PASS.
  Known causal-flip task (h0009 flipped it via a different lever) → partly task-volatile, but
  the reconcile reached the artifact here.

### Smoke vs full — what smoke could NOT see
Smoke went 7/9 with TWO flips (f1006, airbnb007) and ZERO canary regressions, so it read as a
clean GO. The full run reverses that:
1. **f1006's smoke flip did not hold** (0→0 at full) — it was within-task variance, not a stable
   win. Smoke over-credited a volatile flip.
2. **The f1 damage was invisible to smoke.** Smoke's only f1 canary was `f1001`, a stable passer
   the rule never perturbs. The rule's harm lands on f1 tasks that require the `max`-vs-standings
   judgement (f1005, f1005-medium, f1006-hard, f1003-hard) — **none of which smoke sampled.** A
   single passer-canary per family cannot detect a rule that breaks a *different* member of that
   family. This is the multi-canary-per-family gap (G8 needs depth, not just one passer per
   family) flagged at propose ("watch f1001 at scale") but f1001 was the wrong sentinel — it was
   never going to move.
3. ana-eng003 / quickbooks003 regressions were on canary-family members smoke didn't run
   (smoke's ana-eng canary was ana-eng001, qb canary was quickbooks002 — both untouched).

## Verdict

**REJECTED.** Both promotion conditions fail: absolute `stratified_pass_at_1 = 0.5625 <
@baseline 0.6458`, and the paired delta is **−0.0833** with a 95% CI of **[−0.2083, +0.0208]**
that includes a regression (does not clear the tripwire). Net **−4** on a clean strict audit
(2 gains, 6 regressions). 4 of the 6 regressions are damage to f1 passers; the 2 gains are real
but cannot offset the harm.

**Transferable learning — the generative-reconcile false-positive cost is real, and worse than
predicted.** A "reconcile against an independent derivation" rule applied *generatively* (on
every task, ungated) is net-harmful because:
1. **A "structurally different path" is not a guarantee of a *better* path.** The rule pushed the
   solver off a simple correct derivation (`max(points)`) onto an elaborate "independent" one
   (`last-race-by-date standings_rank=1`) that is subtly wrong. The instruction implicitly
   assumes the second path is more trustworthy; it is merely *different*, and difference can be
   wrong. For f1005 the solver even reverted its own correct fix to obey the rule.
2. **The "independent" check became correlated.** Once the solver rebuilt the model on the new
   path, it reconciled the model against the *same* new logic → 0 mismatches → false-green. This
   is precisely the correlated-error wall (`verification-without-oracle-real-world`): only
   genuinely independent redundancy beats no-oracle; a reconcile the solver constructs *after*
   committing to a derivation shares that derivation's blind spot.
3. **Generative scope perturbs even non-numeric/structural tasks** (f1003-hard over-inclusion;
   ana-eng003 contract over-formalization; quickbooks003 path churn), where the rule has no
   purchase and only adds an action/inclusion bias and turn overhead.

**Prevention (if any future variant is attempted — not recommended):**
- **Scope/gate the rule** to numeric-aggregate tasks where the solver is *changing* a figure,
  and forbid replacing a simple correct aggregate with a more elaborate "independent" derivation
  — reconcile should *check* the existing path, never *become* the new path.
- **Require the reconcile to be genuinely independent of the model's chosen logic** (e.g. a
  coarser source-level total computed before the model is touched), and never reconcile a model
  against a CTE built with the same window/grain — that is self-anchoring in disguise.
- **Multi-canary-per-family smoke (depth, not breadth).** One passer-canary per family is blind
  to a rule that breaks a *different* family member. The f1 damage needed ≥2–3 f1 canaries
  spanning the `max`/standings judgement (f1005-class), not just the inert f1001. Update G8 to
  require multiple canaries per affected family, chosen to be *perturbable*, not just stable.
- **Distrust single-task smoke flips** — f1006's smoke flip was variance and reverted at full;
  weight a flip by whether it reaches the committed artifact AND is stable, not by smoke pass/fail.

**Next move: escalate to the captain; do NOT reflexively refile.** The independent-invariant
direction is now twice-burned — the *self-anchored* family was dead (h0006/h0007/h0008,
solver-blind-to-oracle), and h0012 shows that even a *genuinely-different-path* reconcile,
applied generatively, is net-harmful because the second path is not guaranteed correct and
re-correlates with the model post-fix. The lever family "make the solver check its own numbers
without an oracle" is exhausted as a *generative* rule; any survivor would have to be narrowly
scoped, gated to figure-changes, and forbidden from replacing correct simple paths — a much
smaller bet the captain should weigh against other directions, not an automatic refile.

(IN-STAGE Validation rule, not a workflow-structural change → WORKFLOW-REFINE.md step skipped
per dispatch; the learning lives here and in the entity. The in-stage-rule learning also belongs
in the instruction-lever taxonomy note: generative reconcile = net-negative; scope-and-gate or
drop.)

## Gatekeeper review

**Recommendation: APPROVE** — no FAILs; single Validation-stage idea, leak-guard intact, spec
scope clean, frozen files preserve kind/runtime, fidelity holds (independent-signal family, not
the dead self-verification family), G7 ships a worked-example SQL skeleton (PASS, not
abstract-structural WARN), the generative G8 rule carries a verified cross-family
`@baseline`-passer canary panel, and G9 is N/A (a single Validation recompute rule, not a
multi-candidate/selector protocol).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-05). Reviewed 2026-06-06.

Fork parent resolved: `source:` names `codex-ade-dbt-minimal`; `@baseline` resolves to run
`622bdedac572b479` whose `solver_workflow` is `codex-ade-dbt-minimal` — `source:` and the
registry agree, so the parent is `solver_workflows/codex-ade-dbt-minimal` (resolution
pre-satisfied; `rk` not run).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is one pure-addition hunk `76a77,96`; parent stage headers at L34 Exploration / L50 Implementation / L64 Validation / L77 Finalization, so the insertion (after L76, before L77) sits entirely within `## Stage: Validation`. One idea: independent-recompute reconcile. No other `## Stage:` touched; no dependency/leak-guard prose edited. |
| G2 leak-guard intact | PASS | grep over the added lines: leak tokens (`solution__\|AUTO_\|check_option_\|verifier\|equality test\|has less columns\|expected output seed`) NONE FOUND; external-fetch (`curl\|wget\|git clone\|git ls-remote\|http\|fetch\|download\|oracle\|published solution`) NONE FOUND. Diff is a pure addition (`76a77,96`), so all leak-guard/dependency prose is byte-identical to parent. |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0012-…yaml` shows only `2c2 experiment:` and `11c11 solver_workflow:`. `agent.kind: spacedock_solver` (L4) + `runtime: codex` (L5) preserved; `trials: 1` (L24) unchanged. |
| G4 smoke tasks-only | PASS | `diff …yaml …smoke.yaml` = `23a24,38` adding only a `tasks:` block (+ comments); all 9 IDs `ade-bench-` prefixed; includes all 4 named targets (ana-eng006/airbnb007/airbnb009/f1006). airbnb001 is a stable `@baseline`-pass regression sentinel in the set → no WARN. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1715B) and `…smoke.frozen.yaml` (1923B) exist; each carries L4 `kind: spacedock_solver`, L5 `runtime: codex`; smoke frozen also lists all 9 `ade-bench-` tasks. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim — Validation stage, reconcile a key figure + row count against an INDEPENDENT raw-source derivation by a structurally different path. Explicitly bans self-anchored re-runs ("Do **not** 'validate' by re-running your own model or comparing to the pre-existing code") → independent-signal family, NOT the dead h0006/h0007/h0008 self-verification family. No scope creep. |
| G7 actionability/inert-risk | PASS | Instruction ships a worked-example SQL skeleton (literal `select sum(amount) … from {{ ref }}` vs `{{ source }}`, plus `count(*)` vs `count(distinct entity_id)` grain reconcile) — copyable, not abstract-structural prose. Classify: worked-example. Low inert-risk. |
| G8 regression-canary coverage | PASS | Instruction is GENERATIVE (fires on every numeric task, no precondition gate). Smoke panel carries one `@baseline`-passer canary per non-target family: asana001 (asana), quickbooks002 (quickbooks), f1001 (f1), ana-eng001 (ana-eng), airbnb001 (airbnb) — canary @baseline-pass status treated as verified per prior review. intercom has no `@baseline` passer (intercom001/002/003 all fail), so the absence of an intercom canary is structurally correct, not a gap. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — it is a single Validation recompute rule applied within one solver session, with no "run N candidates and select one" mechanism. Per the guideline, N/A (PASS). |

**For the captain:** Clean APPROVE — advance to `smoke`. G9 (new this guideline version) is N/A: there is no candidate-generation/selection mechanism, so neither the fake-independence axis applies. The advisory G7 flag is satisfied (worked-example skeleton, not abstract prose), mitigating the talks-but-doesn't-do inert-risk. G8 is the load-bearing check: the rule is generative and the cross-family canary panel is present, one per non-target family, with intercom correctly absent. Watch f1001 at full scale — it is the exact task the h0009 convention-bleed regressed.

## Stage Report: propose

- [x] DONE: Fork the @baseline solver (`codex-ade-dbt-minimal`) and edit ONLY `## Stage: Validation`.
  `cp -r` → `solver_workflows/h0012-validation-independent-recompute/`; README diff vs parent = single addition `76a77,96` inside Validation only; leak-guard / dependency / other-stage prose untouched.
- [x] DONE: Inserted the independent-recompute rule VERBATIM with a leak-safe worked-example SQL skeleton; no hidden-test references.
  Leak check on the insertion: none of `solution__` / `AUTO_` / `check_option_` / `verifier` / `equality test` / `has less columns` / `expected output seed` present.
- [x] DONE: Sync hypothesis claim (G6) — Falsifiable-claim now states the rule ships with a concrete worked-example recompute skeleton, not abstract prose alone.
  Same single idea/stage (Validation); clause added to the existing claim paragraph.
- [x] DONE: FULL spec `specs/h0012-validation-independent-recompute.yaml` differs from baseline ONLY in `experiment:` + `solver_workflow:`.
  Two-field diff confirmed (see evidence below); `kind: spacedock_solver` + `runtime: codex` preserved.
- [x] DONE: SMOKE spec adds ONLY `benchmark.tasks` — generative rule → G8 cross-family regression panel (4 targets + 5 canaries = 9).
  Targets ana-eng006/airbnb007/airbnb009/f1006 + canaries asana001/quickbooks002/f1001/ana-eng001/airbnb001; intercom has no @baseline passer (documented above), so no intercom canary.
- [x] DONE: Freeze both specs; both `.frozen.yaml` exist and retain `kind: spacedock_solver` + `runtime: codex`.
  `specs/h0012-validation-independent-recompute.frozen.yaml` and `…smoke.frozen.yaml` written; smoke frozen carries all 9 `ade-bench-` tasks.
- [x] DONE: Frontmatter `status: hypothesis` → `propose`; stage report appended.

### Evidence

`diff specs/baseline.yaml specs/h0012-validation-independent-recompute.yaml` (exactly two fields):

```diff
2c2
< experiment: ade-bench-baseline # variants: ade-bench-h0001-<slug>
---
> experiment: ade-bench-h0012-validation-independent-recompute # variants: ade-bench-h0001-<slug>
11c11
<   solver_workflow: ./solver_workflows/codex-ade-dbt-minimal # variants repoint to ./solver_workflows/h<NNNN>-<slug>
---
>   solver_workflow: ./solver_workflows/h0012-validation-independent-recompute # variants repoint to ./solver_workflows/h<NNNN>-<slug>
```

`diff solver_workflows/codex-ade-dbt-minimal/README.md solver_workflows/h0012-validation-independent-recompute/README.md` (single Validation-stage block):

```diff
76a77,96
> When validating a numeric result, reconcile at least one key figure against an
> **independent** derivation computed straight from the raw source tables by a
> structurally different path (a different join order/grain, or a coarser source-level
> count), and reconcile the model's row count against the count implied by its declared
> grain on the raw source. Treat any disagreement as a real defect to root-cause and fix.
> Do **not** "validate" by re-running your own model or comparing to the pre-existing
> code — a check that reuses your own derivation shares its blind spot.
>
> Worked example — recompute one figure a different way, require agreement:
> ```sql
> -- (a) the figure your model produces:
> select sum(amount) as total from {{ ref('my_model') }};
> -- (b) the SAME figure derived INDEPENDENTLY from raw source by a different path/grain:
> select sum(amount) as total from {{ source('raw', 'transactions') }};
> -- if (a) != (b), root-cause and fix the model; do not explain the gap away.
> -- Row-count reconcile: model rows must equal the count implied by the declared grain:
> select count(*) from {{ ref('my_model') }};                          -- model
> select count(distinct entity_id) from {{ source('raw','entity') }};  -- grain-implied
> ```
>
```

### Summary

Forked the @baseline solver and added one `## Stage: Validation` rule: reconcile a key figure
and the row count against an independent raw-source derivation by a structurally different
path, never against a self-anchored re-run, shipped with a leak-safe worked-example SQL
skeleton. Full spec differs from baseline only in `experiment:` + `solver_workflow:`; the rule
is generative, so the smoke spec carries a G8 cross-family regression panel (asana001 /
quickbooks002 / f1001 / ana-eng001 / airbnb001) alongside the 4 targets — intercom supplies no
canary because it has no @baseline passer. Both specs frozen with `spacedock_solver` / `codex`
preserved. Gatekeeper not run (dispatched separately).

## Stage Report: smoke

- DONE: Smoke result: per-task flip/distance table smoke-vs-@baseline — confirm the 2 flips (f1006, airbnb007 -> PASS), the 5 canaries held PASS (zero regressions), and the strict audit is clean (tainted 0, captured>0).
  7/9 = 0.7778 (run-dir `9efca9a9001b7262`); f1006 0.0→1.0 and airbnb007 0.0→1.0 flip; canaries airbnb001/ana-eng001/asana001/f1001/quickbooks002 all 1.0→1.0; strict audit `clean:9 tainted:0 coverage_missing:0` (re-run independently). Smoke gate met. Table in ## Smoke result.
- DONE: Behavioral analysis: committed-SQL read proving the independent-recompute reconcile actually FIRED and reached the committed SQL on >=1 flip (verify the artifact, not the chatter), plus the Got-N distance (inert vs closer) and why-still-failing for >=1 held target (ana-eng006 / airbnb009).
  f1006 = flipped-because-reached-SQL: committed apply_patch `sum→max` (session line 164) preceded by the independent reconcile query (line 145) exposing model 6,453 vs independent 575/530 + row-count reconcile 3190==3190. airbnb007 corroborates (raw NPS reconcile, 0 mismatches). Distance: ana-eng006 Got 204→204 INERT, airbnb009 Got 1→1 INERT. Why ana-eng006 fails: reconcile fired (0 raw mismatches, qty 6615 matched) but blind-to-oracle — orthogonal to the hidden AUTO_*_equality column/value contract (204 mismatch + column-count compile errors).
- SKIPPED: WORKFLOW-REFINE.md update
  Per dispatch: h0012 is an IN-STAGE Validation rule (single README addition inside `## Stage: Validation`), not a structural workflow change (no new stage/protocol) — WORKFLOW-REFINE.md step explicitly skipped.

### Summary

Smoke is a clean go for promotion to full: 7/9 (0.7778 > @baseline 0.6458 even on this stacked panel), two artifact-verified flips, zero canary regressions, clean strict audit. The independent-recompute reconcile is load-bearing and reached the committed SQL on both flips — f1006 most cleanly (reconcile against `*_results` sums by a different source path exposed the cumulative-sum inflation, driving the committed `sum→max` patch). The two held targets are INERT (Got N unchanged), and ana-eng006 shows the rule's ceiling: it fires correctly but cannot beat the blind-to-oracle wall when the worker's self-consistent independent derivation is orthogonal to the hidden oracle's column/value contract. Recommend advancing to full; watch f1001 at scale (h0009 convention-bleed regressed it before).

## Stage Report: analyze

- DONE: Run result: absolute score 0.5625 vs @baseline 0.6458 + paired delta, AND the FULL per-task ledger BOTH directions (2 gains, 6 regressions, each with mechanism).
  0.5625 (27/48) vs 0.6458 (31/48); NET −4. `rk runs diff` TypeError'd (query_id null) → paired delta from per_trial_outcomes.json by slug + 10k bootstrap: Δ=−0.0833, 95% CI [−0.2083, +0.0208]. Strict audit on full run-dir clean (48 clean, 0 tainted). Gains: airbnb007, asana002. Regr: ana-eng003, f1003-hard, f1005, f1005-medium, f1006-hard, quickbooks003. Full ledger table in ## Run result.
- DONE: Behavioral analysis: verify the committed artifact on gains AND >=2 regressions — did the reconcile DAMAGE passers? Plus smoke-vs-full.
  YES, damaged passers. f1 cluster (4/6): baseline solved with one correct `sum→max` patch; variant rule pushed it to `row_number()…standings_rank=1` (last-race-by-date) — subtly wrong (`Got 2`); f1005 even REVERTED its own correct `max`. The "independent" reconcile re-correlated (model checked against a CTE with the same standings_rank logic → 0 mismatches false-green). ana-eng003: 5-col model + enforced contract (dropped 13 cols). f1003-hard: 6 answers vs baseline's 3 (over-inclusion). Smoke-vs-full: f1006 smoke flip REVERTED at full (variance); f1 damage invisible because the only f1 canary (f1001) was an inert passer that never moves. Detail in ## FULL-RUN behavioral analysis.
- DONE: Verdict: REJECTED with transferable learning + prevention + next-move.
  REJECTED (both promotion gates fail: 0.5625 < 0.6458, CI includes regression). Learning: generative reconcile's false-positive cost — a "structurally different path" is not guaranteed correct, and the reconcile re-correlates with the model post-fix (correlated-error wall). Prevention: scope/gate to figure-changes, forbid replacing simple-correct paths, require genuine independence, multi-perturbable-canary-per-family smoke, distrust single-task flips. Next move: escalate to captain, do NOT reflexively refile (the no-oracle self-check family is exhausted as a generative rule). Detail in ## Verdict.
- SKIPPED: WORKFLOW-REFINE.md update
  Per dispatch: h0012 is an IN-STAGE Validation rule, not a structural workflow change → learning recorded in ## Verdict + instruction-lever taxonomy instead.

### Summary

REJECTED. The generative independent-recompute Validation rule scored 0.5625 (27/48) vs @baseline 0.6458 (31/48), NET −4 on a clean strict audit (paired Δ=−0.0833, CI [−0.2083,+0.0208] — fails the tripwire). The load-bearing finding: the rule DAMAGED 4 f1 passers by pushing the solver off a simple correct `max(points)` aggregate onto an over-engineered "last-race standings" path that is subtly wrong, then "validated" it with a reconcile correlated to the new path (false-green) — the correlated-error wall, realized as net harm. Two real gains (airbnb007, asana002) cannot offset six regressions. Smoke missed all of this: f1006's flip was variance (reverted at full) and the single f1 canary (f1001) was inert. Recommend escalating to the captain; the no-oracle self-check lever family is exhausted as a generative rule.
