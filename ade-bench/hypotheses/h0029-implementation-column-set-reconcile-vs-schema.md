---
id: h0029
title: Implementation — reconcile the output column set against the DECLARED set (schema.yml + instruction) as a mechanical set-difference, never against your own judgment of which columns matter
status: propose
kind: hypothesis
source: verification-without-oracle synthesis (_artifacts/verification-without-oracle.md) — width (#2) is a bug class whose deciding fact lives in a DECLARED local artifact (schema.yml / instruction), so it is reachable by an INDEPENDENT check (accounting "footing/cross-footing": the declared set must equal the produced set). Prior width attempts h0011 (worked-example "include the full column set", REJECTED 0/3) and h0023 (Output-Contract deliverable/columns, NO-GO — f1001 convention-bleed) used construct-prose, not a reconciliation against the declared contract. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-06T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Width failures ("has less columns than `solution__<model>`") happen because the solver
hand-picks a column **subset** it judges relevant, and its own check confirms that subset is
internally consistent — a self-anchored false-green. The deciding fact (which columns the model
must have) is NOT oracle-only: for these tasks it is **declared locally**, in the model's
`schema.yml` entry and/or the task instruction's explicit column list. (airbnb007 flipped under
h0017 precisely because "create the models described in schema.yml" makes schema.yml the
contract.) So width is reachable by an **independent reconciliation** — the same move an
accountant makes when the ledger total must tie out to the sum of its parts: the produced
column set must equal the declared column set, and any difference is a defect, not a judgment
call.

This is the **independent-vs-correlated** distinction from `verification-without-oracle.md`:
h0011 told the solver to "include the full column set" (a construct-prose instruction it could
acknowledge and skip — inert at gpt-5.5/xhigh). This hypothesis instead makes the solver compute
a **mechanical set-difference against a declared external artifact** and fail loud on a nonempty
difference. The anchor (schema.yml / instruction) is external to the solver's own
column-selection reasoning, so it does not share its blind spot.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation instruction — *when you author a model that has a DECLARED column list — its entry
in `schema.yml` lists columns, or the task instruction names the columns it must expose —
reconcile your output against that declared list. READ the declared column names from
`schema.yml`/the instruction (do not re-derive or infer them from your own output), and compute
the set-difference `declared − produced`. For every declared column missing from your output, ADD
it, deriving its value from the appropriate source/analog relation — the declaration is the
contract, not your judgment. This reconcile is **ADDITIVE ONLY**: add genuinely-missing declared
columns; never DROP, RENAME, or rewrite a column you already produce, and never add a column that
is not in the declared list. If a model has no declared column list, this rule does not apply — do
not invent a contract* — shipped with a concrete worked-example skeleton (read the declared
columns; list produced columns; diff; add only the missing declared ones) — will catch the width
false-greens (ana-eng004, f1002, and the width legs of ana-eng006) and let the solver fix them,
raising `stratified_pass_at_1` above the `@baseline` 0.6458.

**G10 compliance (self-correcting-lever gating, from the h0012 −4 lesson).** This is a
reconcile-and-fix lever, so it must survive G10's three axes: **(a) scope** — it is **gated** to
models that carry a declared column list (no declared set → no-op), not run on every model; and
on a task that already produces the full declared set the diff is empty, so the rule **cannot
perturb a width-passer**. **(b) independence source** — it reconciles against the DECLARED
`schema.yml`/instruction set, a **separately-sourced external artifact that is read, never
re-derived** from the solver's own output (so it cannot re-correlate into a false-green the way
h0012's self-built CTE did). **(c) check-don't-replace** — it is **additive only**: it adds
genuinely-missing declared columns and is explicitly forbidden from dropping, renaming, or
rewriting any column already produced, so it cannot push a simple-correct model onto a wrong
"structurally different" path.

This is NOT h0011 re-filed: h0011 was a construct-prose "include all columns" worked-example;
this is an **independent set-difference reconciliation against a declared artifact**, the
verification-without-oracle "footing" import. It is NOT h0023's deliverable-set clause (that
inferred MODELS from installed packages and convention-bled on f1001); this reconciles only the
COLUMN set of a model the solver is already authoring, anchored to that model's own schema.yml
entry — no model-set inference, no package walking.

Method/README change only. Forks `solver_workflows/codex-ade-dbt-minimal` (runtime codex); no
dataset, harness, or solver-runtime change. Leak-guard intact (schema.yml + instruction are
shipped local artifacts; no public fetch, no oracle, no reference to hidden
`AUTO_*`/`solution__*`/`has less columns` verifier text).

## Target datasets

Primary smoke targets (the width cluster, all `ade-bench-` prefixed):

- `ade-bench-ana-eng004` — `AUTO_obt_product_inventory_equality` "has less columns".
- `ade-bench-f1002` — `AUTO_most_podiums_equality` "has less columns".
- `ade-bench-ana-eng006` — width legs (`AUTO_dim_products`, `AUTO_obt_product_inventory`).

Scope classification (G10(a)): **gated** to models that carry a declared column list — but most
dbt models ship a `schema.yml` entry, so for G8 canary purposes treat it as broad and carry a
full regression panel, **doubling the families that share the targets' construct**. The targets
span **ana-eng** (ana-eng004, ana-eng006) and **f1** (f1002), so those two families each need ≥2
**perturbable** canaries (passers whose models carry declared column lists the reconcile can
actually fire on), per G8:

- **ana-eng (shared construct, ≥2 perturbable):** `ade-bench-ana-eng001`, `ade-bench-ana-eng003`.
- **f1 (shared construct, ≥2 perturbable):** `ade-bench-f1001` (the h0009/h0023 convention-bleed
  tripwire), `ade-bench-f1004`.
- **One `@baseline` passer per other family:** `ade-bench-airbnb001`, `ade-bench-asana001`,
  `ade-bench-quickbooks002`. No intercom canary exists (`intercom001/002/003` all fail @baseline).

(All eight canaries are confirmed `@baseline` passers from the 31/48 outcomes.)

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
The README diff vs `codex-ade-dbt-minimal/README.md` touches only `## Stage: Implementation`
(the single column-set reconciliation rule), leaves the other stages and the
dependency/package/leak-guard prose untouched, and references no hidden
`AUTO_*`/`solution__*`/"has less columns" verifier tokens. `agent.kind: spacedock_solver`,
`runtime: codex` preserved.

**AC-2 — G6 independence + G10 self-correcting-lever gating + G7 actionability.** The inserted
text reconciles against the DECLARED schema.yml / instruction set (external), not the solver's own
re-run or judgment — not the dead self-verification family (G6). It satisfies **G10** on all three
axes: **(a)** gated to declared-list models (no declared set → no-op; full declared set already
produced → no-op, so width-passers are untouched); **(b)** the reconcile target is the
separately-sourced declared list, READ not re-derived (no re-correlation false-green); **(c)**
additive only — adds missing declared columns, never drops/renames/rewrites an existing column or
adds an undeclared one. **G7:** ships a worked-example set-difference skeleton, not abstract prose.

**AC-3 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict`,
`tainted: 0`, `captured > 0`).

**Smoke gate:** flip ≥1 of the width targets (the `has less columns` ERROR clears) with **zero**
canary regressions across the full panel — and specifically zero regressions on the **≥2
perturbable canaries per shared-construct family** (ana-eng001/003, f1001/f1004), since a
generative reconcile can break a *different* family member than a single canary (the h0012 −4
lesson, G8). A canary dropping FAIL is NO-GO regardless of target movement (h0009 −3 lesson).
Inert-detector: if a target's compile-time column error is unchanged, the rule was inert. Variance
caution: a lone target flip with no artifact-proof (the added column visible in the committed SQL)
may be noise — bank a GO on artifact-proven flips, not a single reward change.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Gatekeeper review

**Recommendation: APPROVE** — clean additive G10-gated column-set reconcile against an external declared artifact (schema.yml/instruction), one idea in one stage, leak-guard byte-identical, two-field spec, full regression panel with perturbable doubling on both construct-sharing families; no FAILs.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Fork parent resolved: `@baseline` = `runs/ade-bench-baseline/622bdedac572b479`, its `solver_workflow` = `solver_workflows/codex-ade-dbt-minimal` — matches the hypothesis `source:`. README diff vs parent = pure addition `63a64,100` (no existing line modified); all added lines (64–100) fall inside `## Stage: Implementation` (50–100, before `## Stage: Validation` at 101); single idea = the declared−produced column-set reconcile. |
| G2 leak-guard intact | PASS | README lines 1–33 (header + no-external-reference prose at 9–11: `curl`/`wget`/`git clone`/`git ls-remote`/package-source/published-solutions) are byte-identical parent↔fork (`diff` empty). Forbidden-token grep over added lines 64–100 (`AUTO_`/`solution__`/`check_option`/`has less columns`/`verifier`/`equality test`/`expected output seed`/`curl`/`wget`/`clone`) = NONE. |
| G3 spec two fields | PASS | `diff baseline.yaml h0029.yaml` = exactly two hunks: `experiment:` (line 2) and `solver_workflow:` (line 11). `agent.kind: spacedock_solver`, `runtime: codex` preserved; `trials: 1` unchanged in both spec and concurrency. |
| G4 smoke tasks-only | PASS | `diff h0029.yaml h0029.smoke.yaml` = single added `benchmark.tasks:` block (`23a24,38`); all 10 slugs `ade-bench-` prefixed; includes every named target (ana-eng004, f1002, ana-eng006) + 7 canaries. WARN-condition (no stable passer sentinel) does NOT trigger: 7 of the 10 are confirmed `@baseline` passers. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1741 B) and `…smoke.frozen.yaml` (1971 B) exist; each carries `kind: spacedock_solver` (line 4) + `runtime: codex` (line 5); smoke frozen carries all 10 task slugs (lines 31–40). |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: same stage (Implementation), same idea (mechanical `declared − produced` set-diff). It is **independent**, not self-anchored: it READs declared column names from `schema.yml`/the instruction ("do not re-derive or infer them from your own output") — an external anchor, not the dead h0006/h0007/h0008 self-verification family. No dead-family phrasings present. |
| G7 actionability/inert-risk | PASS | Carries a worked-example skeleton (4-step text recipe + BEFORE→AFTER SQL the solver can copy: `select … , category, unit_cost  -- the {declared − produced} difference`), not abstract structural prose. Class: worked-example mechanical column-add — the G7-favored form, not a FROM/spine/grain rewrite. |
| G8 regression-canary coverage | PASS | Generative (fires on every model carrying a declared column list — not precondition-gated to the targets). Smoke panel verified against `622bdedac572b479` per_trial_outcomes (31/48): ≥1 non-target `@baseline` passer per other family — airbnb001=1.0, asana001=1.0, quickbooks002=1.0; intercom legitimately absent (intercom001/002/003 all 0.0 @baseline, no passer to draw). Construct-sharing families doubled with ≥2 perturbable passers each: ana-eng001=1.0 & ana-eng003=1.0; f1001=1.0 & f1004=1.0. Targets confirmed FAIL: ana-eng004/f1002/ana-eng006 all 0.0. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — single generative Implementation rule. |
| G10 self-correcting false-positive | PASS | Self-correcting (reconcile-and-fix), so in scope; all three axes pass. (a) Scope: gated — no declared column list → no-op; a model already producing the full declared set has an empty diff → cannot perturb a width-passer. (b) Independence source: reconciles against the DECLARED `schema.yml`/instruction set, a separately-sourced external artifact READ verbatim, not a re-derived CTE — no re-correlation false-green (the h0012 failure mode). (c) Check-don't-replace: explicitly ADDITIVE ONLY — "never DROP, RENAME, or rewrite a column you already produce, and never add a column that is not in the declared list" — cannot push a simple-correct path onto a wrong "structurally different" one. |

**For the captain:** No FAILs and no WARNs — clean APPROVE; advance to `smoke`. The G10 safety story is strong on paper (gated + external-read anchor + additive-only), but it rests on the *generative* assumption that the smoke panel is dense enough; the panel is correctly built (verified passers, perturbable doubling on both ana-eng and f1). The one residual to watch at the smoke gate is the standing inert-risk for this `@baseline` — even a clean worked-example column-add can be "talked but not done" — so bank a GO only on artifact-proven flips (the added declared columns visible in committed SQL), per the hypothesis's own variance caution.

## Stage Report: propose

- DONE: Forked solver README adds EXACTLY the G10-gated additive column-set reconcile as ONE Implementation-stage instruction (with the worked-example skeleton); leak-guard/dependency prose byte-identical to the codex-ade-dbt-minimal parent.
  `diff codex-ade-dbt-minimal/README.md h0029-.../README.md` = pure addition `63a64,100` (no existing line modified), entirely inside `## Stage: Implementation`; forbidden-token grep (`AUTO_`/`solution__`/`has less columns`/`verifier`/`curl`…) hits only the parent's pre-existing leak-guard lines (9/10/16/22/26), zero in added lines 64–100.
- DONE: Full spec specs/h0029-...yaml differs from specs/baseline.yaml ONLY in experiment + solver_workflow; smoke spec adds benchmark.tasks with the 10 named tasks (targets ade-bench-ana-eng004/f1002/ana-eng006 + canaries ade-bench-ana-eng001/ana-eng003/f1001/f1004/airbnb001/asana001/quickbooks002).
  `diff baseline.yaml h0029.yaml` = 2 hunks (lines 2, 11) only; `diff h0029.yaml h0029.smoke.yaml` = single added `benchmark.tasks` block `23a24,38`, all 10 slugs `ade-bench-` prefixed.
- DONE: Both specs frozen via rk freeze --allow-missing; agent.kind=spacedock_solver and runtime=codex preserved in both.
  `rk freeze` wrote both `.frozen.yaml`; grep confirms `kind: spacedock_solver` + `runtime: codex` (lines 4/5) in both frozen files, full carries the new experiment/solver_workflow, smoke carries all 10 task slugs (lines 31–40).
- SKIPPED: Run the gatekeeper (Output 5).
  Per dispatch: the FO dispatches an INDEPENDENT gatekeeper review after this build completes, so the review stays independent of the builder. Outputs 1–4 only, per instruction.

### Summary

Forked the @baseline seed (codex-ade-dbt-minimal) into h0029 and inserted one Implementation-stage instruction: a mechanical `declared − produced` column-set reconcile against the DECLARED schema.yml/instruction list (READ not re-derived), gated to models that carry a declared column list, ADDITIVE-only (add missing declared columns; never drop/rename/rewrite an existing column or add an undeclared one), shipped with a worked-example set-difference skeleton. The leak-guard / no-external-reference / dependency prose is byte-identical to the parent — the diff is a pure 37-line addition inside `## Stage: Implementation`. Full spec differs from baseline only in experiment + solver_workflow; smoke spec adds a 10-task benchmark.tasks panel (3 width targets + G8/G10 perturbable doubling on the ana-eng and f1 construct-sharing families + one passer per other family). Both specs frozen, kind/runtime preserved. Did Outputs 1–4 only; the independent gatekeeper (Output 5) is the FO's to dispatch.
