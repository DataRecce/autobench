---
id: spd0013
title: Lean inline LAG-over-own-output period-over-period rule (NO contract scaffold) — isolate the airbnb001 flip from the heavy contract checkpoint
status: smoke
kind: hypothesis
source: "forks the CURRENT champion @baseline = spd0008-over-emit-collapse (spd0012 NOT promoted); adds ONLY a lean inline derivation-METHOD clause to spd0008's existing G3 COLUMN-VALUE CONTRACT guidance — the LAG/LEAD-over-own-output period-over-period rule — and DROPS the entire spd0011/spd0012 contract checkpoint scaffold (no Classify-output block, no Exploration-for-contract block, no Implementation Contract stage, no contract-aware Validation signature). Isolation test of spd0012's durable airbnb001 flip."
started:
completed:
verdict:
score:
worktree:
---

## Hypothesis

spd0012 (REJECTED / validated-not-promoted, full 24/60 = `@baseline`) produced ONE durable,
artifact-attributable flip: `airbnb001` 0→1, held across two draws (smoke + full), via a
LAG-over-own-output derivation-METHOD constraint that NULLs the `mom_agg_reviews.MOM` column by
construction (one window row per group ⇒ `LAG` has no prior row ⇒ NULL = gold). But that flip rode on
a **heavyweight contract checkpoint** (a Classify-output block, an Exploration-for-contract evidence
list, a full Implementation Contract stage with a named-template inventory, and a contract-aware
Validation signature). The whole-solver netted **+0** and the contract prose is suspected of a
**diffuse cost on a borderline passer** (`quickbooks003` was 0/3 across all three contract-stage draws
with `selected_rule: none` every time — no template ever touched it).

**Falsifiable claim (one knob):** the LAG-over-own-output method constraint is sufficient to flip
`airbnb001` as a **lean inline rule in the existing per-column value-def guidance**, WITHOUT any of
the contract scaffold. Fork the CURRENT champion `spd0008-over-emit-collapse` and add ONLY one clause
to its existing G3 COLUMN-VALUE CONTRACT section:

> A period-over-period derived column (MoM / YoY / delta / growth-%) must be computed as a window
> function (`LAG`/`LEAD`) over the built model's OWN output rows — partition by the group key, order
> by the window-anchor date — never against a separately re-materialized prior-period window queried
> from the source. This is a derivation METHOD, not a value (read it off the window definition; never
> bake a literal value, count, or NULL flag). When the build emits exactly one window row per group,
> the `LAG`/`LEAD` has no prior row and the column is NULL by construction. The local sibling
> `models/agg/wow_agg_reviews.sql` already follows this exact method — mirror its shape.

This is a single inline rule placed in spd0008's existing G3 list (between the existing per-column
clauses). It is gated (fires only on a period-over-period derived column), oracle-free (names a method,
not a value), and leak-safe (the only file pointer is the in-workspace sibling `wow_agg_reviews.sql`;
no gold values, counts, dtypes, or NULL flags baked). **NO Classify-output block, NO
Exploration-for-contract block, NO Implementation Contract stage, NO contract-aware Validation
signature** — that scaffold is precisely what this hypothesis isolates OUT. README-only; no harness,
verifier, runtime, model, fixture, or routing change; no-fetch leak guard byte-identical to spd0008.

Target query: `airbnb001` (flip). Key canary: `quickbooks003` (must HOLD WITHOUT the contract prose —
its recovery would be evidence the prose, not a template, was the diffuse cost). `apple_store001` is a
hold target.

## The fork this resolves

Two outcomes, both informative:

- **(a) The lean rule flips `airbnb001` AND `quickbooks003` holds** → the contract scaffold was
  unnecessary overhead; the inline method-constraint captures the durable flip at a fraction of the
  prose cost → **promote the lean rule** (a genuine +1 candidate over a fixture-corrected champion if
  the airbnb flip lands clean).
- **(b) The lean rule does NOT flip `airbnb001`** → the contract checkpoint (forcing the worker to
  write and then obey an explicit plan) WAS load-bearing for compliance — reconfirming spd0011's
  detected-but-not-obeyed finding — and the airbnb flip is reachable only with the heavy scaffold. A
  real tradeoff for the captain (a costly vehicle for a single durable cell).

The discriminator is the committed `mom_agg_reviews.MOM` artifact: NULL across all 3 rows ⇒ the lean
inline rule reached the artifact (outcome a); a real MoM% ⇒ the worker reverted to its prior-window
re-materialization reflex without the contract forcing function (outcome b).

## Pre-smoke Decision-Fork Probe

**Reachability is already proven offline (reuse spd0012's reconstruction) — the NEW fork is purely
behavioral (does a LEAN inline rule, with no contract forcing-function, steer the worker the same way
the contract scaffold did?).**

- **The fork.** `airbnb001`'s build yields a single-window `mom_agg_reviews` (3 rows, one
  AGGREGATION_DATE, REVIEW_TOTALS/REVIEW_SENTIMENT gold-exact under spd0008's existing G2 latest-window
  rule). The SOLE graded residual is the `MOM` column (verifier grades cols `[0,1,3]`). Either a real
  MoM% (worker's reflex) or NULL (gold). Which, and is the lean inline rule enough to reach it?

- **Control result (spd0008 champion, no contract, no LAG rule).** The worker computes MoM by
  separately re-materializing a prior 30-day window from `fct_reviews` (a `previous_window` CTE) and
  dividing → real percentages `≈ {−17.99, −20.25, −9.92}` ≠ gold NULL → reward 0.0. This is the
  starting state spd0013 forks from (`airbnb001` fails at spd0008).

- **Gold (reconstructed offline from `_views/spider2-dbt-airbnb001/tests/airbnb.duckdb`, spd0012).**
  `mom_agg_reviews` = 3 rows, all AGGREGATION_DATE 2021-10-22, REVIEW_SENTIMENT {negative, neutral,
  positive}, **`MOM` (DOUBLE) = NULL for all 3 rows.** Comparator = column-containment,
  `math.isclose(abs_tol=1e-2)`, `NA==NA`; the gold `{NULL,NULL,NULL}` MOM is not contained in the
  worker's real-percentage vector → mismatch, reward 0.0.

- **Proposed-rule result (verified offline by spd0012, byte-for-byte == gold).** Applying
  `LAG(REVIEW_TOTALS) OVER (PARTITION BY REVIEW_SENTIMENT ORDER BY AGGREGATION_DATE)` over the exact
  3-row single-window output yields `MOM = NULL` for all three sentiments — identical to gold. The
  derivation-method constraint mechanically produces gold MOM without any oracle read.

- **Why the proxy justifies smoke — and what is NEW.** The residual is SINGULAR (one column),
  REACHABLE (the LAG method reproduces gold offline), and README-ADDRESSABLE + oracle-free (names a
  method, not a value). spd0012 ALREADY proved the contract-scaffold version of this rule reaches the
  artifact (airbnb001 flipped, durable two-draw). The OPEN, UNTESTED question spd0013 isolates: does
  the SAME method-constraint, delivered as a **lean inline G3 clause with no contract forcing-function**,
  steer the worker off its prior-window reflex — or was the explicit write-the-plan-then-obey-it
  contract checkpoint load-bearing for that compliance? That is exactly the behavioral fork the smoke
  tests. (Plus: does `quickbooks003` recover once the heavy contract prose is gone?)

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
The variant forks `spd0008-over-emit-collapse` and adds ONLY the one lean inline G3 period-over-period
clause. NO contract-checkpoint blocks of any kind. No-fetch leak guard byte-identical; no baked gold.
Verified by: `diff specs/full-baseline.frozen.yaml specs/spd0013-*.yaml` and
`diff solver_workflows/spd0008-over-emit-collapse/README.md solver_workflows/spd0013-*/README.md`
(must show exactly the one added clause and ZERO contract-scaffold lines).

**AC-2 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict`,
rc=0, 0 coverage_missing, 0 tainted) on the same run-dir.

**AC-3 — Verdict justified by the committed-artifact read.** `airbnb001` flips iff the committed
`mom_agg_reviews.MOM` column is NULL for all 3 rows (the lean inline LAG rule reached the artifact).
If it does NOT NULL the column (worker still re-materializes a prior window), the contract checkpoint
was load-bearing for compliance — outcome (b). `quickbooks003` must HOLD (its recovery is positive
evidence the contract prose, not a template, carried the diffuse cost). Hard-gate canaries hold.

## Smoke Plan

Targeted smoke (mirror the spd0012 panel so the scaffold-removal effect is observable):

- `airbnb001` — primary flip target (MoM = lean inline LAG-over-own-output → NULL by construction).
- `apple_store001` — hold target (raw-key success spd0008 already passes; must hold).

Hard-gate canaries (champion passers that must hold):
`activity001`, `app_reporting001`, `google_play001`, `google_play002`, `quickbooks003` (the cell that
was 0/3 under the contract stage — must RECOVER to 1.0 now that the contract prose is gone; recovery
is positive evidence the prose carried a diffuse cost).

Telemetry-only (reported, not go/no-go): `mrr001`, `mrr002`, `retail001` (known flake), `recharge002`,
`f1003`.

## Expected Outcome

Realistic yield: outcome (a) — the lean inline rule flips `airbnb001` (the method is the same one that
worked under the scaffold; the question is whether the forcing-function was needed) and
`quickbooks003` recovers (the contract prose was its diffuse cost). If `airbnb001` does NOT flip under
the lean rule, that is the informative negative: outcome (b), the contract checkpoint was load-bearing
for compliance — a real tradeoff to surface to the captain, not another wording tweak. Either way the
result sharpens the cost/benefit of the contract vehicle relative to a one-line inline rule.

## Gatekeeper review

**Recommendation: APPROVE** — exactly one lean inline G3 LAG-over-own-output clause added on the spd0008 champion, zero contract-scaffold lines, leak-guard intact, specs scoped correctly, both frozen with kind/runtime preserved, smoke = 12 tasks (both targets + all 5 hard-gate canaries).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-26.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | README diff vs spd0008 (`@baseline`, matches `source:`) adds exactly ONE contiguous block: the period-over-period LAG/LEAD-over-own-output clause appended to the existing G3 COLUMN-VALUE CONTRACT list (after line 249). Clause absent from parent. ZERO contract-scaffold lines: no "Implementation Contract"/"Classify output"/"selected_rule"/"validation_signature" added (grep count 0). No other section touched. |
| G2 leak-guard (hidden gold) | PASS | Added text names a derivation METHOD only; explicitly "never bake a literal value, count, or NULL flag." Leak grep over added lines: no `expected_`/`answer_key`/`ground_truth`/`curl`/`wget`/`git clone`, no baked values (834/2745/4370/17499/MoM %). One `gold` token = generic phrase "diverges from a single-window gold" (no table/column named) — benign. Only file pointer is the in-workspace sibling `models/agg/wow_agg_reviews.sql` (a project file, not a gold/answer file). No-fetch paragraph byte-identical to spd0008. |
| G3 spec two fields | PASS | Full frozen vs `full-baseline.frozen.yaml` differs only in `experiment:` + `agent.solver_workflow:` plus four auto-recomputed hashes (`solver_workflow_content_hash`, `sealed_hash`, `harness_git_sha`, `solver_workflow_hash`). `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1` all preserved. |
| G4 smoke narrows tasks only | PASS | Smoke frozen vs full frozen differs ONLY in `benchmark.tasks` + freeze-recomputed hashes; no `exclude_tasks`. `--explain` → Tasks: 12 (airbnb001 sample). Set = airbnb001, apple_store001, activity001, app_reporting001, google_play001, google_play002, quickbooks003, mrr001, mrr002, retail001, recharge002, f1003 — includes flip target airbnb001 + hold target apple_store001 + all 5 hard-gate canaries. |
| G5 both frozen | PASS | Both frozen files exist (dated Jun 26). Both carry `kind: spacedock_solver` (line 4) and `runtime: codex` (line 5). |
| G6 resolver fidelity | PASS | Inserted clause matches the falsifiable claim verbatim (LAG/LEAD over own output, partition by group key, order by anchor date, NULL-by-construction on single window, mirror `wow_agg_reviews.sql`). Generative-style derivation-method guidance — tells HOW to derive, NOT a self-anchored check. No scope creep. |
| G7 actionability/inert-risk | PASS | Mechanical + worked-example: names a concrete window-function method (`LAG/LEAD OVER (PARTITION BY … ORDER BY …)`) and points to a concrete in-workspace sibling (`wow_agg_reviews.sql`) to mirror. spd0012 already proved the method reaches the airbnb001 artifact; the open question is whether the lean delivery lands as reliably — the behavioral test, not inert-risk. |
| G8 regression-canary coverage | N/A (PASS) | Gated clause — fires only on a period-over-period derived column (MoM/YoY/delta/growth-%), not every task. Smoke nonetheless carries 5 hard-gate `@baseline` canaries (activity001, app_reporting001, google_play001, google_play002, quickbooks003), with quickbooks003 doubling as the diffuse-cost recovery probe. |
| G9 selector independence | N/A (PASS) | Not a multi-candidate/selector protocol. |
| G10 self-correcting false-positive | N/A (PASS) | Not a validate-and-fix lever — generative derivation-method constraint, no check-and-rewrite mandate. |

**For the captain:** Auto-approved to smoke — no FAILs, no WARNs. This is the clean isolation test of spd0012's lone durable flip: it strips the entire contract-checkpoint scaffold and keeps ONLY the lean inline LAG-over-own-output G3 clause on the spd0008 champion. Two informative outcomes (lean rule flips airbnb001 + quickbooks003 recovers ⇒ scaffold was overhead; or airbnb001 holds at 0 ⇒ contract forcing-function was load-bearing). The single "gold" word in the added clause is the generic "single-window gold" phrase carried from parent wording, not a leak. Verdict hinges on the committed `mom_agg_reviews.MOM` artifact (NULL × 3 rows = reached) per AC-3.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Verify the already-forked solver README is the correct one-knob change (diff vs spd0008 = exactly one added G3 clause, ZERO contract-scaffold lines)
  `diff spd0008 spd0013 README` = single hunk `249a250,262` (the period-over-period LAG-over-own-output clause); grep `Implementation Contract|Classify output|selected_rule|validation_signature` = 0 hits; LAG/wow_agg_reviews present at lines 250-261.
- DONE: Confirm leak-guard no-fetch prose byte-identical to spd0008 and no baked gold
  No-fetch line 11 identical in both (not in diff); baked-gold scan (834/2745/4370/17499/MoM %) = 0 hits.
- DONE: Create full spec (cp full-baseline.frozen.yaml, set experiment + solver_workflow only)
  `specs/spd0013-lean-lag-period-over-period.yaml`; dropped the stale baseline `solver_workflow_content_hash` so freeze recomputes it.
- DONE: Create smoke spec (positive allowlist of the 12, no exclude_tasks)
  `specs/spd0013-lean-lag-period-over-period.smoke.yaml` — 12 tasks: airbnb001, apple_store001, activity001, app_reporting001, google_play001, google_play002, quickbooks003, mrr001, mrr002, retail001, recharge002, f1003.
- DONE: Freeze BOTH specs
  `rk freeze --allow-missing` produced `.frozen.yaml` + `.smoke.frozen.yaml`.
- DONE: Verify smoke selection --explain shows Tasks: 12
  `rk run ...smoke.frozen.yaml --explain` → `- Tasks: 12`, sample task airbnb001.
- DONE: Confirm full-spec frozen diff vs full-baseline.frozen.yaml = only experiment + solver_workflow (+ auto hashes); kind/runtime preserved
  Diff = experiment, solver_workflow, + 4 auto-recomputed hashes (solver_workflow_content_hash, sealed_hash, harness_git_sha, solver_workflow_hash); `kind: spacedock_solver` / `runtime: codex` not in diff (preserved).
- DONE: Run gatekeeper review subagent and write the Gatekeeper review block
  Subagent applied `_gatekeeper/propose-review-guideline.md` → APPROVE, all 10 rules PASS/N/A, no FAIL/WARN; block appended to `## Gatekeeper review`.
- DONE: No rk run beyond --explain; commit; stop at propose gate
  Only `rk freeze` and `rk run --explain` invoked. Committed; halting at gate.

### Summary

Verified the pre-forked spd0013 README is the clean one-knob isolation of spd0012's durable airbnb001 flip — exactly one inline G3 LAG-over-own-output period-over-period clause on the spd0008 champion, with the entire contract-checkpoint scaffold removed (grep = 0). Built and froze the full spec (cp from full-baseline.frozen, two-field edit) and the 12-task smoke spec (positive allowlist, --explain = Tasks: 12); the full frozen diff is only experiment + solver_workflow + auto hashes. Gatekeeper recommends APPROVE with no FAILs and no WARNs, so the propose auto-gate's gatekeeper condition is clean.
