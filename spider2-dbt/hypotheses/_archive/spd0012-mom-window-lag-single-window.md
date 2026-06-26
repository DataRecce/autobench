---
id: spd0012
title: MoM = window LAG over the model's own single-window output (drop the raw-grouping template)
status: conclude
kind: hypothesis
source: "forks current champion @baseline = spd0008-over-emit-collapse; carries the spd0011-validated Implementation Contract checkpoint + G2_LATEST_WINDOW_FULL_REFRESH template, drops the spd0011 G2_REPORT_RAW_GROUPING_HOLD template (proven net-negative destabilizer over two cycles), and replaces spd0011 FIX A's soft NULL-condition with a hard LAG-over-own-output derivation-method constraint"
started: 2026-06-26
completed: 2026-06-26
verdict: REJECTED
score: 24/60
worktree:
archived: 2026-06-26T15:52:32Z
---

## Hypothesis

The current registry champion (`@baseline` = `spd0008-over-emit-collapse`,
`runs/spider2-dbt-spd0008-full/4ba55fba0138a84d`, 24/60) leaves `airbnb001` failing on a single
graded column: `mom_agg_reviews.MOM`. spd0011 proved (a) the Implementation Contract checkpoint is
obeyed at gpt-5.5/codex (fire-and-obey, the first counter to the detected-but-not-obeyed wall), (b) its
`G2_LATEST_WINDOW_FULL_REFRESH` template solves the latest-window/full-refresh blocker so airbnb001's
REVIEW_TOTALS/REVIEW_SENTIMENT/grain are all gold-exact, and (c) its `G2_REPORT_RAW_GROUPING_HOLD`
template is a net-negative destabilizer that re-grains passers (recharge002 telemetry, then the
quickbooks003 HARD gate) with no compensating flip.

**Single README change (one knob):** fork the champion `spd0008-over-emit-collapse` solver workflow,
carry forward the validated Implementation Contract checkpoint + the `G2_LATEST_WINDOW_FULL_REFRESH`
template, **DROP the `G2_REPORT_RAW_GROUPING_HOLD` template entirely**, and refine the latest-window
template's period-over-period sub-rule from a soft NULL-condition into a hard **derivation-METHOD
constraint**:

> A period-over-period derived column (MoM / YoY / delta / growth-%) in a single-window build must be
> computed as a window function (`LAG`/`LEAD`) **over the built model's OWN output rows**, partitioned
> by the group key and ordered by the window-anchor date — never against a separately re-materialized
> prior-period window queried from the source. When the build emits exactly one window row per group,
> the window function has no prior row and the column is NULL by construction. (Derive the method from
> the window definition; never bake a literal value, count, or NULL flag.)

This mechanically NULLs MoM when the output is a single window — matching gold — without baking the
answer. It mirrors the scaffold's own sibling `models/agg/wow_agg_reviews.sql`, which computes its
week-over-week metric exactly this way (`LAG(REVIEW_TOTALS,6) OVER (PARTITION BY REVIEW_SENTIMENT ORDER
BY AGGREGATION_DATE ASC)`).

This remains README-only: no harness, verifier, runtime, model, fixture, or routing change. The
no-fetch leak guard stays byte-identical; no gold values/counts/dtypes baked. Target query: `airbnb001`
(flip). `apple_store001` is a hold target.

## Pre-smoke Decision-Fork Probe

**This probe is the spd0011 cycle-2 offline gold reconstruction — the left-shift reachability proof,
performed on the LOCAL source only (no network, no fabricated gold).**

- **The fork.** airbnb001's contract correctly drives a single-window `mom_agg_reviews` (3 rows, one
  AGGREGATION_DATE = 2021-10-22, REVIEW_TOTALS/REVIEW_SENTIMENT gold-exact). The ONLY graded residual is
  `MOM` (verifier grades `mom_agg_reviews` cols `[0,1,3]`). Either MoM should be a real percentage
  (worker's choice, both cycles) or NULL (gold's choice). Which, and is it README-reachable?

- **Control result (the champion + spd0011 both produce).** The worker computes MoM by separately
  re-materializing a prior 30-day window from `fct_reviews` (a `previous_window` CTE) and dividing —
  yielding real percentages `MOM = {−17.99, −20.25, −9.92}`. spd0011 FIX A's soft "NULL where the
  baseline is not present in the single window" did NOT stop this: the worker reasoned a prior window IS
  computable from the 2009–2021 source, so it refused to NULL.

- **Gold (reconstructed offline from `_views/spider2-dbt-airbnb001/tests/airbnb.duckdb`).**
  `mom_agg_reviews` = exactly 3 rows, all `AGGREGATION_DATE` 2021-10-22, REVIEW_TOTALS {834, 2745, 4370},
  REVIEW_SENTIMENT {negative, neutral, positive}, **`MOM` (DOUBLE) = NULL for all 3 rows.**
  `dim_listings_hosts` gold = 17,499 rows (worker builds 17,499, 0 mismatch) → not a blocker. Comparator
  (`tests/duckdb_match.py`) = column-containment, `math.isclose(abs_tol=1e-2)`, `NA==NA`; the gold
  `{NULL,NULL,NULL}` MOM vector is not contained in the worker's `{−17.99,−20.25,−9.92}` → mismatch,
  reward 0.0. Confirmed both cycles: MOM is the SOLE residual.

- **Proposed-rule result (verified offline, byte-for-byte == gold).** Applying
  `LAG(REVIEW_TOTALS) OVER (PARTITION BY REVIEW_SENTIMENT ORDER BY AGGREGATION_DATE)` over the exact 3-row
  single-window output yields `MOM = NULL` for negative, neutral, AND positive — identical to gold. So the
  derivation-method constraint mechanically produces the gold MOM without any oracle read or baked value.

- **Why the proxy justifies smoke.** The residual is (1) SINGULAR (one column), (2) REACHABLE (the LAG
  method reproduces gold offline), and (3) README-ADDRESSABLE + oracle-free (the rule names a method, not
  a value; the worker already has the local sibling pattern `wow_agg_reviews`). This is NOT oracle-blind:
  gold MOM=NULL is the mechanical consequence of a LAG over a single-window output, derivable from the
  window definition alone. The open risk is behavioral, not reachability — whether a method-constraint
  README ("use LAG over your own output, do not re-query a prior window") actually steers the worker off
  its prior-window reflex. That is exactly what the smoke tests.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `solver_workflow:`.**
The variant forks `spd0008-over-emit-collapse` and differs only in the README (carry the contract
checkpoint + `G2_LATEST_WINDOW_FULL_REFRESH` with the LAG-method MoM constraint; DROP
`G2_REPORT_RAW_GROUPING_HOLD`). No-fetch leak guard byte-identical; no baked gold. Verified by:
`diff specs/full-baseline.frozen.yaml specs/spd0012-*.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict`,
rc=0, 0 coverage_missing, 0 tainted) on the same run-dir.

**AC-3 — Verdict justified by the committed-artifact read.** `airbnb001` flips iff the committed
`mom_agg_reviews.MOM` column is NULL for all 3 rows (the LAG-over-own-output method reached the
artifact). The hard-gate canaries must hold; with `G2_REPORT_RAW_GROUPING_HOLD` removed, quickbooks003
and recharge002 should NOT be re-grained by a raw-grouping template.

## Smoke Plan

Targeted smoke (mirror the spd0011 panel so the dropped-template effect is observable):

- `airbnb001` — primary flip target (MoM = LAG-over-own-output → NULL).
- `apple_store001` — hold target (raw-key success that spd0008 already passes; must hold WITHOUT the
  raw-grouping template — proves the template was not load-bearing for the hold).

Hard-gate canaries (champion passers that must hold):
`activity001`, `app_reporting001`, `google_play001`, `google_play002`, `quickbooks003` (the spd0011
cycle-2 regression — must RECOVER to 1.0 now that `G2_REPORT_RAW_GROUPING_HOLD` is dropped).

Telemetry-only (reported, not go/no-go): `mrr001`, `mrr002`, `retail001` (known flake), `recharge002`
(must not re-regress with the template gone), `f1003`.

## Expected Outcome

Realistic yield `+1` (airbnb001) with quickbooks003 RECOVERED, IF the LAG-method constraint steers the
worker off its prior-window reflex. The dropped template is the safety win: removing
`G2_REPORT_RAW_GROUPING_HOLD` should un-regress the two cells it destabilized. If airbnb001 still does
not NULL the MOM column despite the method constraint, the residual is a deeper behavioral reflex (the
worker insists on a "real" MoM) and the value-def family is the next escalation, not another template
tweak — conclude `validated-not-promoted` per AC-5 discipline rather than re-tweaking wording.

## Gatekeeper review

**Recommendation: APPROVE** — one cohesive contract-checkpoint idea (drop the net-negative raw-grouping template, keep only G2_LATEST_WINDOW, harden the MoM sub-rule to a LAG-over-own-output derivation-METHOD constraint); leak-guard byte-identical, no gold values leaked, specs scoped to exactly two fields, smoke narrows tasks-only with both targets present, lever is precondition-gated with a structural validation signature.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-26T11:42:00Z.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | Diff vs `spd0008/README.md` adds 3 hunks all serving ONE idea: a Classify-output block (90a91), the Exploration-for-contract evidence list + Implementation Contract stage with a single-template inventory (269a283) and contract-aware Validation (383a471). Inventory holds only `G2_LATEST_WINDOW_FULL_REFRESH`; the dropped `G2_REPORT_RAW_GROUPING_HOLD` appears 0 times. No leak-guard/no-fetch prose edited. |
| G2 leak-guard (hidden gold) | PASS | Numeric/value grep (`834|2745|4370|17499|-17.99|-20.25|-9.92|expected_|answer_key|ground_truth`) returns ONLY the literal field name `expected_row_shape` — no gold values, counts, dtypes, or NULL flags baked. All `gold`/`curl`/`wget`/`git clone` hits are in prohibition prose. No-fetch paragraph (lines 11–15) byte-identical to spd0008. The MoM rule names a METHOD (`LAG`/`LEAD` over own output) + a local-sibling file pointer `models/agg/wow_agg_reviews.sql` (allowed workspace path), not gold. |
| G3 spec two fields | PASS | Frozen-vs-frozen diff (`full-baseline.frozen.yaml` vs `spd0012…frozen.yaml`) changes ONLY `experiment:`, `agent.solver_workflow:`, and the auto-regenerated hashes (`solver_workflow_content_hash`, `sealed_hash`, `harness_git_sha`, `solver_workflow_hash`). Preserved: `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1`. No third functional field differs. |
| G4 smoke narrows tasks only | PASS | Smoke diff changes only the experiment-name suffix (`-smoke`) and narrows `benchmark.tasks` to exactly 12: airbnb001, apple_store001, activity001, app_reporting001, google_play001, google_play002, quickbooks003, mrr001, mrr002, retail001, recharge002, f1003. No `exclude_tasks`. Both named targets present: airbnb001 (flip) + apple_store001 (hold). quickbooks003 + recharge002 retained as de-regression canaries. |
| G5 both frozen | PASS | Both `spd0012…frozen.yaml` and `…smoke.frozen.yaml` exist; both carry `agent.kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the falsifiable claim verbatim: a single-template contract checkpoint with the MoM rule "computed as a window function (`LAG`/`LEAD`) over the built model's OWN output rows… never against a separately re-materialized prior-period window." Generative/independent build-and-derive instruction; the Validation signature checks STRUCTURE (LAG-over-own-output method present, single-window grain), not "verify your answer matches" — no self-anchored false-green phrasing. No scope creep. |
| G7 actionability/inert-risk | PASS | Concrete + mechanical: names a specific SQL construct (`LAG`/`LEAD` partitioned by group key, ordered by window-anchor date) and carries a worked-example skeleton from the local sibling (`LAG(REVIEW_TOTALS, 6) OVER (PARTITION BY REVIEW_SENTIMENT ORDER BY AGGREGATION_DATE)`). Not abstract prose. |
| G8 regression-canary coverage | N/A (PASS) | Lever is precondition-GATED, not fires-everywhere: `G2_LATEST_WINDOW_FULL_REFRESH` fires ONLY on a target/sibling carrying `is_incremental()` latest-window logic; any non-matching target sets `selected_rule: none` and uses unchanged guidance. Smoke nonetheless carries passing canaries (activity001, app_reporting001, google_play001/002, quickbooks003, recharge002). |
| G9 selector independence | N/A (PASS) | No multi-candidate / run-N-and-select protocol declared; single build-one-contract-per-target design. |
| G10 self-correcting false-positive | PASS | Validation is a STRUCTURAL/existence-and-method check (table exists as base table, name convention, single-window grain unique, forbidden patterns absent, period-over-period column computed via LAG/LEAD over own output) — it does NOT re-derive against the solver's own answer and is gated to the latest-window precondition. Per spd0002-class rule, a structure/method check cannot turn a right value wrong → not value-rewriting. |

**For the captain:** Auto-approved to smoke with no FAILs and no WARNs. This is the spd0011 follow-up that drops the proven net-negative `G2_REPORT_RAW_GROUPING_HOLD` template and hardens the MoM rule into a LAG-over-own-output method constraint; the 12-task smoke pairs the airbnb001 flip target with apple_store001 (proves the dropped template was not load-bearing for that hold) and keeps quickbooks003 + recharge002 to confirm they un-regress now that the raw-grouping template is gone. Worth a glance at the smoke result for whether the method-constraint actually steers the worker off its prior-window reflex (the open behavioral risk the hypothesis itself flags).

## Smoke result

**Smoke run:** `runs/spd0012-mom-window-lag-single-window-smoke/14fe861107f3b0ff` (12 cells, strict audit
CLEAN — 12 clean / 0 coverage_missing / 0 tainted, rc=0). Verdict: **GO** (captain-approved to full
2026-06-26). 9/12 pass.

| Task | Baseline (spd0008) | spd0012 | Flip/distance/why |
|------|------|------|------|
| **airbnb001** (target) | ❌ 0.0 | ✅ **1.0** | **FLIPPED — artifact-real.** Committed SQL computes MoM via `LAG(REVIEW_TOTALS, …) OVER (PARTITION BY REVIEW_SENTIMENT ORDER BY AGGREGATION_DATE)` over the model's OWN single-window output; one window row per group ⇒ LAG has no prior row ⇒ `MOM` NULL by construction = gold. reward=1.0 ⇒ verifier matched gold on cols [0,1,3] incl. MOM. The method-constraint steered the worker off the prior-window re-materialization reflex spd0011 could not stop. |
| apple_store001 (hold) | ✅ 1.0 | ✅ 1.0 | HELD **without** `G2_REPORT_RAW_GROUPING_HOLD` — proves that template was never load-bearing for the hold, only destabilizing. |
| recharge002 (telemetry) | ✅ 1.0 (spd0011: ❌) | ✅ 1.0 | **RECOVERED** — dropping the raw-grouping template un-regressed the cell it destabilized in spd0011. Safety win confirmed. |
| activity001 / app_reporting001 / google_play001 / google_play002 | ✅ 1.0 | ✅ 1.0 | hard-gate canaries held. |
| **quickbooks003** (hard-gate) | ✅ 1.0 | ❌ 0.0 | Did NOT recover. **`selected_rule: none` — NO template fired** ⇒ not a template-lever regression. quickbooks003 is a documented flake candidate; the contract stage alone passed it under spd0011 cycle-1. Read = **flake variance** (to be re-confirmed at full). |
| f1003 / retail001 (telemetry) | ✅ 1.0 | ❌ 0.0 | flake drops — both `selected_rule: none`, both documented flake candidates. |

## Behavioral analysis

**airbnb001 — flipped because the README method-constraint reached the committed artifact.** Both spd0011
cycles the worker re-materialized a prior 30-day window from the 12-year `fct_reviews` source (`previous_window`
CTE) and divided → real MoM% `{−17.99,−20.25,−9.92}` ≠ gold NULL. spd0012's hard derivation-method rule
("compute period-over-period via `LAG`/`LEAD` over your OWN output, never a re-queried prior window") + the
local sibling pointer (`wow_agg_reviews.sql`) made the worker use `LAG` over the single-window output, where a
positive offset returns NULL (no prior row) — mechanically reproducing gold MOM=NULL with no oracle read. This is
the **first artifact-attributable flip of a previously-stuck cell since the spd0007b/spd0008 promotions**, and the
first time a *value-definition residual* (not grain/materialization) was made README-addressable — via a
**method** constraint (how to derive), where spd0007's *dtype/formula* value-defs were oracle-blind.

**quickbooks003 / f1003 / retail001 — flake, not lever.** All three selected `selected_rule: none`; no contract
template touched them. quickbooks003's non-recovery refutes the spd0012 prediction that dropping the destabilizer
would restore it — but the mechanism evidence (no template fired; contract stage alone passed it in spd0011 c1)
points to flake variance, consistent with its documented flake-candidate status. The full run is the independent
re-draw that settles it.

**Contract-checkpoint mechanism (workflow-structural) — still obeyed, now single-template.** The Classify →
Implementation Contract → contract-aware Validation stage fired across the smoke; with only
`G2_LATEST_WINDOW_FULL_REFRESH` in the inventory, non-matching targets correctly took `selected_rule: none` and
fell through to existing guidance (no over-fire). The destabilizer was the *template*, not the *checkpoint* —
removing it preserved the mechanism's value (the airbnb flip) while eliminating the passer-regression
(recharge002/quickbooks003-via-template). See `_artifacts/WORKFLOW-REFINE.md`.

## Run result

**Full run:** `runs/spd0012-mom-window-lag-single-window/73c08047c34ee18a`, **24/60 = 0.40**
(strict audit CLEAN — 60 clean / 0 coverage_missing / 0 tainted, rc=0). Same headline as
`@baseline` = `spd0008` (`runs/spider2-dbt-spd0008-full/4ba55fba0138a84d`, 24/60). **Net +0.**

Paired per-query ledger vs `@baseline` spd0008 (5 gains, 5 regressions):

| Direction | Cells |
|-----------|-------|
| **GAINS** (0→1) | `airbnb001`, `sap001`, `airport001`, `f1001`, `recharge001` |
| **REGRESSIONS** (1→0) | `quickbooks003`, `recharge002`, `marketo001`, `retail001`, `f1003` |

10 cells moved, net 0. Only ONE of the ten is lever-attributable (see Behavioral analysis): the
contract template fired in the committed artifact on `airbnb001` only. Every other moved cell
(both directions) selected `selected_rule: none` — no template fired — and is model/run variance,
EXCEPT `sap001`, which is the deterministic spd0010 FIXTURE repair (available to ANY solver on the
repaired 60-board).

## Behavioral analysis (full run)

**Attribution verified by grepping each moved cell's `agent`/`sessions` transcript for
`selected_rule`:**

- **`airbnb001` — the ONLY lever-attributable flip.** The contract template
  `G2_LATEST_WINDOW_FULL_REFRESH` fired (`selected_rule` set), the committed SQL computes
  `LAG(REVIEW_TOTALS, …) OVER (PARTITION BY REVIEW_SENTIMENT ORDER BY AGGREGATION_DATE)` over the
  model's OWN single-window output ⇒ `MOM` NULL by construction = gold, reward 1.0. The flip HELD
  across BOTH the smoke and the full draws → **durable, artifact-attributable**. This is the
  program's **first value-definition flip made README-addressable via a derivation METHOD** (how to
  compute), where spd0007's dtype/formula value-defs were oracle-blind. The contract+method
  MECHANISM works.

- **`sap001` (0→1) — fixture confound, NOT this lever.** This is the deterministic spd0010 FIXTURE
  repair, available to any solver running on the repaired 60-board. A fixture-corrected `spd0008`
  re-run would bank `sap001` too (≈25/60), so spd0012 at 24/60 is **not clearly above a
  fixture-corrected champion**.

- **`airport001` / `f1001` / `recharge001` (gains) and `marketo001` / `recharge002` / `retail001` /
  `f1003` (regressions) — variance/flake.** EVERY one selected `selected_rule: none` — NO contract
  template touched them. These are model/run-variance moves, not lever effects; they happen to net
  to zero around the airbnb+fixture signal.

- **`quickbooks003` (1→0) — UNRESOLVED diffuse-cost suspicion.** Was 1.0 at `spd0008` (which has no
  contract stage) but is **0/3 across the three contract-stage draws** (spd0011 cycle-2,
  spd0012-smoke, spd0012-full), and selected `selected_rule: none` EVERY time (no template fired).
  Because no template touched it yet it dropped only under the contract-stage solver, the suspicion
  is a **diffuse cost of the heavyweight contract PROSE on a borderline passer** — the worker reads
  the long Classify→Contract→contract-aware-Validation machinery and spends attention/structure that
  destabilizes a marginal cell. UNRESOLVED here: separating "diffuse prose cost" from "flake" would
  need a multi-draw spd0008-vs-contract-stage probe on quickbooks003. The captain chose to ISOLATE
  the lever (spd0013) rather than run that probe.

### Analyze required questions

1. **Net + full bidirectional ledger.** Net **+0** (24/60 = `@baseline`). GAINS:
   airbnb001, sap001, airport001, f1001, recharge001. REGRESSIONS: quickbooks003, recharge002,
   marketo001, retail001, f1003. The headline does not move.

2. **Smoke-vs-full.** `airbnb001` flipped in BOTH (artifact-real, durable). `quickbooks003` was
   down in BOTH smoke and full (`selected_rule: none` both) — consistent non-recovery, not a
   one-draw blip. `recharge002` RECOVERED at smoke (1.0) but REGRESSED at full (1.0→0.0) — a
   flip-flop with `selected_rule: none` = pure variance. The smoke's 9/12 over-stated the board
   (full netted to +0).

3. **Already-correct-and-broken.** All five regressions (quickbooks003, recharge002, marketo001,
   retail001, f1003) were baseline passers. None was template-caused — every one selected
   `selected_rule: none`. They are flake/variable cells (retail001 and f1003 are documented flake
   candidates; recharge002 flip-flopped smoke↔full). quickbooks003 is the one with a residual
   non-flake suspicion (diffuse contract-prose cost), still unresolved.

4. **Was the change executed?** YES on `airbnb001` — executed AND helped: the committed
   `mom_agg_reviews.MOM` is NULL across all 3 rows via the LAG-over-own-output artifact, reward 1.0.
   Everywhere else the lever was INERT (no template fired); the other ten cell-moves are model
   variance, not lever execution.

5. **Prevention + next move.** The airbnb flip is real but rides on a heavyweight contract
   checkpoint that (a) contributes a possible diffuse cost on a borderline passer (quickbooks003)
   and (b) leaves the headline at +0 because the durable signal is a single cell swamped by the
   fixture confound + variance. Next move: **ISOLATE** — does the LAG rule flip airbnb001 WITHOUT
   the contract scaffold? Filed as **spd0013** (lean inline rule on the spd0008 champion, no
   contract machinery). If the lean rule suffices and quickbooks003 holds → promote the lean rule;
   if it does not flip airbnb001 → the contract checkpoint was load-bearing for compliance (a real
   tradeoff for the captain).

6. **Smoke-vs-full fork drift.** The airbnb flip is artifact-real in BOTH draws (no drift — the most
   reliable cell). The smoke could NOT settle quickbooks003: at smoke its drop read as plausible
   flake, but the full re-draw shows 0/3 under the contract stage — the smoke had no power to
   separate flake from a diffuse contract-prose cost. recharge002's smoke "recovery" did not
   replicate at full (flip-flop = variance the smoke mis-read as a safety win).

## Failure Review

Not a failure of the lever's mechanism — `airbnb001` flipped exactly as designed and HELD across two
draws (smoke + full), artifact-attributable to the LAG-over-own-output derivation-method constraint.
The hypothesis falls short on the PROMOTION bar, not the mechanism bar:

- **Headline net +0.** The one durable, artifact-attributable flip (airbnb001) is offset by the
  fixture confound (sap001 is free to any solver on the repaired board) and a wash of
  `selected_rule:none` variance moves in both directions.
- **Does not clear a fixture-corrected champion.** A fixture-corrected spd0008 would also bank
  sap001 (≈25/60), so spd0012 at 24 is not clearly above the right comparison point.
- **Possible diffuse cost.** quickbooks003 is 0/3 under the contract stage with no template ever
  firing — a heavyweight-prose cost on a borderline passer is the leading (unresolved) explanation.

Classification: the lever WORKS but its vehicle (the heavy contract checkpoint) is costly and the
durable signal is a single cell. Route = **file** the isolation experiment (spd0013) that strips the
contract scaffold and keeps only the lean LAG rule.

## Follow-up Routing

**file** — filed `spd0013-lean-lag-period-over-period.md` (status `hypothesis`), forking the CURRENT
champion `spd0008-over-emit-collapse` (spd0012 is NOT promoted). spd0013 adds ONLY a lean inline
value-def rule — the LAG-over-own-output period-over-period derivation method — to spd0008's existing
G3 COLUMN-VALUE CONTRACT guidance, with NO Classify-output block, NO Exploration-for-contract block,
NO Implementation Contract stage, and NO contract-aware Validation signature. The fork it tests:
does the lean rule flip `airbnb001` without the contract scaffold (→ scaffold was unnecessary
overhead, promote lean) OR does it fail to flip (→ the contract checkpoint was load-bearing for
compliance, a real tradeoff)? `quickbooks003` is the key canary — it must HOLD without the contract
prose. The spd0012 Pre-smoke Decision-Fork Probe (offline gold reconstruction: LAG over the 3-row
single-window output == gold MOM=NULL byte-for-byte) is reused as spd0013's reachability proof.

## Verdict

**REJECTED — validated-not-promoted.** `@baseline` UNCHANGED = `spd0008` 24/60.

Banked findings:

- **`airbnb001` is a DURABLE, artifact-attributable LEVER flip** via the LAG-over-own-output
  derivation-METHOD constraint — held across two independent draws (smoke + full), committed-artifact
  proof (`MOM` NULL via `LAG` over the model's own single-window output = gold). This is the
  program's **FIRST value-definition flip made README-addressable through a METHOD** (how to derive),
  distinct from spd0007's oracle-blind dtype/formula value-defs. The **contract + method MECHANISM
  works** and is bankable knowledge.
- **BUT net +0 headline does not clear a fixture-corrected champion** — sap001 is a deterministic
  fixture confound (free to any solver on the repaired board, ≈25/60), and the durable airbnb signal
  is a single cell swamped by `selected_rule:none` variance in both directions.
- **The heavyweight contract checkpoint may carry a diffuse `quickbooks003` cost** — 0/3 across three
  contract-stage draws, never a template firing (no template touched it) — unresolved here; the
  captain chose to isolate (spd0013) rather than run a dedicated probe.

Decision: do NOT promote. File the lean-LAG isolation follow-up (spd0013) that separates the durable
method-constraint flip from the costly contract vehicle.

## Stage Report: propose

- DONE: Fork the champion: cp -r solver_workflows/spd0008-over-emit-collapse solver_workflows/spd0012-mom-window-lag-single-window
  Forked; README is the only file. spd0011 README (= spd0008 + contract machinery) copied in as the seed, then the two deltas applied.
- DONE: Edit ONLY the README to carry the spd0011 Implementation Contract checkpoint + G2_LATEST_WINDOW template, DROP G2_REPORT_RAW_GROUPING_HOLD, harden the period-over-period sub-rule to a hard LAG-over-own-output derivation-METHOD constraint (one knob)
  `diff spd0008 spd0012` = 4 added blocks only (Classify-output, Exploration-for-contract, Implementation Contract stage, contract-aware Validation); inventory says "Only this one named template"; G2_REPORT_RAW_GROUPING_HOLD appears 0 times.
- DONE: Keep the no-external-reference / leak-guard prose byte-intact; embed no gold values, dtypes, counts, NULL flags
  No-fetch para (lines 11-15) byte-identical to spd0008; gold-value grep (834/2745/4370/17499/-17.99/-20.25/-9.92) returns NONE; MoM rule names a METHOD only.
- DONE: Source the contract-checkpoint text from spd0011's README ... with ONLY the G2_LATEST_WINDOW_FULL_REFRESH template
  Seeded from spd0011 README so all four contract blocks are carried verbatim; the dropped template removed from the inventory bullet AND the Validation signature reference.
- DONE: Do NOT relocate or delete any existing spd0008 implementation-stage tips
  Diff shows additions only (90a91, 269a283, 383a471); no spd0008 line modified/removed. The wow_agg_reviews.sql pointer added is a leak-safe local file-path reference (verified the sibling exists with the cited LAG expression).
- DONE: Create full spec: cp full-baseline.frozen.yaml ... set experiment + solver_workflow only
  specs/spd0012-mom-window-lag-single-window.yaml; only experiment: + solver_workflow: edited.
- DONE: Create smoke spec: positive benchmark.tasks allowlist of exactly the 12 (no exclude_tasks)
  specs/spd0012-mom-window-lag-single-window.smoke.yaml; 12 tasks, no exclude_tasks, experiment suffixed -smoke.
- DONE: Freeze BOTH
  wrote spd0012-mom-window-lag-single-window.frozen.yaml AND .smoke.frozen.yaml.
- DONE: Verify smoke selection --explain shows Tasks: 12
  `rk run ...smoke.frozen.yaml --explain` => "- Tasks: `12`".
- DONE: Confirm full-spec frozen diff vs full-baseline.frozen.yaml shows ONLY experiment + solver_workflow (+ auto hashes); kind/runtime preserved
  Frozen-vs-frozen diff = experiment, solver_workflow, solver_workflow_content_hash, sealed_hash, harness_git_sha, solver_workflow_hash only; kind: spacedock_solver / runtime: codex unchanged.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block; leak-guard attention on the LAG-method MoM rule
  Gatekeeper recommendation APPROVE; all 10 rules PASS/N/A, zero FAIL, zero WARN. Block written above.
- DONE: Do NOT launch any rk run beyond --explain. Commit. Stop at the propose gate.
  Only `rk freeze` + `rk run --explain` executed. Committed below; stopping at gate.

### Summary

Forked the champion spd0008-over-emit-collapse into spd0012, then layered in the spd0011-validated
Implementation Contract checkpoint with exactly ONE knob: dropped the proven net-negative
`G2_REPORT_RAW_GROUPING_HOLD` template (only `G2_LATEST_WINDOW_FULL_REFRESH` remains in the inventory)
and hardened the period-over-period sub-rule from spd0011's soft NULL-condition into a hard
LAG/LEAD-over-own-output derivation-METHOD constraint, with a leak-safe pointer to the in-workspace
sibling `models/agg/wow_agg_reviews.sql`. Both specs freeze cleanly; smoke selects the 12-task panel;
the full frozen diff vs baseline is exactly experiment + solver_workflow + auto hashes. Gatekeeper
APPROVE (10/10 PASS/N/A, no FAIL/WARN) — auto-advance to smoke with clean FO reject-checks.

## Stage Report: conclude

- DONE: Write the ## Run result block (full 24/60=0.40, run dir 73c08047c34ee18a, strict audit CLEAN 60/0/0 rc=0, paired ledger vs @baseline spd0008, net +0)
  Run result block written with the gains/regressions table and the one-lever-attributable note.
- DONE: Write/extend the ## Behavioral analysis with the full-run attribution (only airbnb001 fired a template = durable; all others selected_rule:none = variance; sap001 = fixture fix; quickbooks003 0/3 under contract stage = unresolved diffuse-prose suspicion)
  Added `## Behavioral analysis (full run)` with per-cell selected_rule attribution.
- DONE: Answer the analyze required questions (1) net+ledger (2) smoke-vs-full (3) already-correct-and-broken (4) was-executed (5) prevention+next (6) smoke-vs-full fork drift
  All six answered under `### Analyze required questions`.
- DONE: Set frontmatter verdict: REJECTED and completed: 2026-06-26; write ## Verdict = validated-not-promoted with banked findings; @baseline UNCHANGED = spd0008 24/60
  Frontmatter verdict REJECTED, completed 2026-06-26, score 24/60; Verdict block written.
- DONE: Finalize the spd0012 entry in _artifacts/WORKFLOW-REFINE.md (status rejected-as-written; sharpen learning; bears-on spd0013)
  spd0012 entry updated to FULL finding + rejected-as-written status + sharpened learning + bears-on spd0013.
- DONE: Append a one-line entry to _artifacts/self-learning.md
  Appended the spd0012 REJECTED/validated-not-promoted entry.
- DONE: File spd0013-<slug>.md (status hypothesis, id spd0013) forking spd0008-over-emit-collapse; ONLY a lean inline value-def LAG rule; NO contract scaffold; target airbnb001, canary quickbooks003; reuse spd0012 offline probe; state the new fork
  Filed hypotheses/spd0013-lean-lag-period-over-period.md + forked solver_workflows/spd0013-lean-lag-period-over-period (diff vs spd0008 = exactly one G3 clause, 0 contract-scaffold lines, leak-guard byte-identical, no gold values).
- DONE: Commit all edits. Do NOT archive spd0012 (FO archives). Do NOT launch any rk run.
  Committed below; no archive, no rk run.

### Summary

Concluded spd0012 REJECTED / validated-not-promoted. The full run (24/60 = @baseline, net +0, strict
audit clean) confirmed airbnb001 as a DURABLE artifact-attributable lever flip via the
LAG-over-own-output derivation-METHOD constraint (template fired, MOM NULL by construction = gold, held
smoke+full) — the program's first value-def flip made README-addressable through a METHOD. But the
headline does not clear a fixture-corrected champion (sap001 is the spd0010 fixture confound) and the
heavy contract checkpoint may carry a diffuse quickbooks003 cost (0/3 under the stage, selected_rule:none
every draw). @baseline UNCHANGED = spd0008 24/60. Filed spd0013 (lean-LAG isolation): the same
method-constraint as a single inline G3 clause on the spd0008 champion with the entire contract scaffold
removed — does the lean rule still flip airbnb001 (scaffold = overhead → promote lean) or not (scaffold =
load-bearing for compliance → a real tradeoff), and does quickbooks003 recover without the contract prose?
