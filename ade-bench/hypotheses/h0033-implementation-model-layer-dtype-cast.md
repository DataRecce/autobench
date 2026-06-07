---
id: h0033
title: E4 -- Implementation; apply a mechanical in-place ::type cast in the MODEL .sql (never the raw seed) when a column's representation mismatches a sibling/instruction contract -- recover asana002 without convention-bleed
status: propose
kind: hypothesis
source: _proposal/oracle-problem-systematic-program.md (E4); successor to archived h0020 (REJECTED -- cast the raw seed, wrong layer) and h0009 (asana002 win but convention-bled -3); E0/h0032 found NO declared data_type/contract entries in the project, so the cast keys off the observed type mismatch vs a sibling/instruction, not a declared contract. captain go-ahead 2026-06-07.
started: 2026-06-07T15:17:49Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

*(Seeded by the FO from the proposal E4; the propose stage builds the variant + worked example.)*

`asana002` is a type/contract mismatch (oracle `AUTO_asana__task_equality`, `Got 2`): the committed
`asana__task` model emits a column (e.g. `due_at`) whose representation/type differs from what the
hidden oracle expects; a `::timestamp` cast fixes it -- Mini-confirmed solvable and the h0009 win.
The prior attempts each failed on HOW: **h0009** landed the cast but **convention-bled** (-3 on
f1/quickbooks by over-applying the package convention); **h0020** precondition-gated the cast but
applied it to the **raw SEED** (the wrong layer). E0/h0032 found the project has **no declared
`data_type:`/`contract:` entries**, so the cast cannot key off a declared contract -- it keys off the
**observed type mismatch** vs a sibling model / the task instruction.

**Lever (single Implementation-stage rule + a copyable worked example):** when a model column's
type/representation mismatches what a sibling model or the task instruction implies, apply a
mechanical **in-place `::<type>` cast IN THE MODEL `.sql`** (e.g. `due_at::timestamp`) --
additive/in-place ONLY: no add/drop/rename of columns, and **NEVER edit the raw seed or source**
(the h0020 failure). Precondition-gated to an observed mismatch on a specific column; do **not**
broadly re-type every column (the h0009 convention-bleed).

**Falsifiable claim:** the model-layer in-place cast rule flips `asana002` (`Got 2 -> 0`) with ZERO
convention-bleed regression, raising `stratified_pass_at_1` above `@baseline` 0.6458. Falsified if
inert (committed `asana__task.sql` unchanged / still wrong type), if it edits the seed (h0020
failure mode), or if any perturbable canary regresses (h0009 failure mode).

## Target datasets

Target (smoke): `ade-bench-asana002`. This rule is generative (fires on any model with a column
type mismatch), so per G8 the smoke carries >=2 **perturbable** canaries from the families the cast
could over-apply to (the h0009 convention-bleed families): `ade-bench-f1001`,
`ade-bench-quickbooks003`; plus cross-family canaries `ade-bench-airbnb001`, `ade-bench-ana-eng001`,
`ade-bench-asana001` (the asana same-family sentinel). All confirmed `@baseline` passers.

## Acceptance criteria

**AC-1 -- Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
One `## Stage: Implementation` rule; leak-guard + other stages byte-identical; no hidden-test tokens.

**AC-2 -- The cast is applied to the MODEL `.sql` (artifact-verified from the committed apply_patch),
NOT the raw seed (the h0020 failure mode); clean strict audit (`tainted:0`, `captured>0`).**

**AC-3 -- Verdict via the paired diff vs `@baseline`: `asana002` flips AND zero convention-bleed
regression on the perturbable canaries (`f1001`/`quickbooks003`).**

## Gatekeeper review

**Recommendation: APPROVE** — one Implementation-stage in-place `::type` cast rule keyed off an
OBSERVED sibling/instruction mismatch (not a declared contract — none exists per E0/h0032); leak-guard
byte-identical; spec differs only in the two allowed fields; smoke carries ≥2 PERTURBABLE bleed canaries
in BOTH h0009 convention-bleed families (f1001 + quickbooks003) plus a worked example that pins the cast
to the MODEL `.sql` and explicitly forbids the h0020 seed/`+column_types` layer.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T15:24:00Z.

Fork parent resolved: `source:` names `solver_workflows/codex-ade-dbt-minimal`; `rk registry resolve run
@baseline` → `runs/ade-bench-baseline/622bdedac572b479` whose `solver_workflow` is
`./solver_workflows/codex-ade-dbt-minimal`. Agree → parent = `codex-ade-dbt-minimal`.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff = one additive hunk `63a64,108`, falling entirely under `## Stage: Implementation` (inserted after the `dbt_packages/` preservation line, before `## Stage: Validation`); one idea (observed-mismatch in-place `::type` cast in the model SQL). No other `## Stage:` touched. |
| G2 leak-guard intact | PASS | Lines 1-49 byte-identical to parent (`diff` of 1-49 → empty). Grep of the ADDED lines 64-108 for `AUTO_*`/`solution__*`/`check_option`/`verifier`/`equality test`/`expected output`/`drive-to-zero`/`Got N`/`curl`/`wget`/`git clone`/`ls-remote`/self-re-run → NONE. A cast changes representation only, not values → cannot leak an expected answer. |
| G3 spec two fields | PASS | `diff baseline.yaml h0033...yaml` = only `experiment:` (→ ade-bench-h0033-...) and `solver_workflow:` (→ ./solver_workflows/h0033-...). `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0033...yaml h0033...smoke.yaml` = only an added `benchmark.tasks:` block. All 6 slugs `ade-bench-` prefixed; includes the named target `ade-bench-asana002`. Carries the asana same-family sentinel (asana001). |
| G5 both frozen | PASS | `h0033...frozen.yaml` (1725B) and `h0033...smoke.frozen.yaml` (1863B) both exist; both carry `kind: spacedock_solver` + `runtime: codex`. Smoke frozen lists all 6 slugs; full frozen `tasks: null`. |
| G6 resolver fidelity | PASS | Inserted text = the Falsifiable claim in spirit: same stage (Implementation), same idea (mechanical in-place `::<type>` cast on ONE observed-mismatch column, in the model `.sql`, never the seed, no add/drop/rename). It tells the solver how to BUILD/derive (generative), keyed to an independent local signal (a sibling model's type / the instruction), NOT a self-anchored "re-run your own model / compare to the old output" — none of the dead h0006/7/8 phrasings present. No scope creep beyond the claim. |
| G7 actionability/inert-risk | PASS | Concrete mechanical SUBSTITUTION (a single-column `::<type>` cast — the loop's one durable edit shape, `due_at::timestamp`), NOT a structural FROM/spine/join/grain rewrite, AND it carries a copyable BEFORE→AFTER SQL worked example the solver can pattern-match. **Inert-risk note for the captain:** h0020 (the prior gated cast) was REJECTED because the cast NEVER reached `asana__task.sql` — the solver kept its raw-seed `ALTER`/`+column_types` habit; this variant's net-new lever is the explicit "EDIT THE MODEL `.sql`, NEVER the seed/`+column_types`" constraint + the worked example. Whether that pulls the edit to the model layer is exactly what smoke must prove (artifact read: did the committed `apply_patch` touch `models/asana__task.sql`, not the seed). |
| G8 regression-canary coverage | PASS | GENERATIVE (the cast can fire on any model column observed to mismatch a sibling/instruction type) → panel required. Smoke carries ≥2 PERTURBABLE canaries in EACH family the cast could over-apply to — the two h0009 convention-bleed families: f1 (f1001, NO-package, the 6/6→2/6 victim) and quickbooks (quickbooks003, intermediate, the 14/14→11/14 victim) — plus one passer from each other coverable family (airbnb001, ana-eng001) and the asana same-family sentinel (asana001). All five are confirmed `@baseline` PASS (`622bdedac572b479/per_trial_outcomes.json`). Intercom is uncoverable (intercom001/002/003 all FAIL @baseline — no passer). |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — a single mechanical cast, one solver session. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever — it does not verify a number and act on disagreement; it is a one-shot representation cast gated to a precondition (an OBSERVED column type/representation mismatch vs a sibling/instruction). The precondition gating ("ONLY a specific column you have OBSERVED to mismatch… do NOT broadly re-type") is the h0009 convention-bleed guard, and the panel's 2-perturbable-canary doubling on f1+quickbooks measures it directly at smoke. |

**For the captain:** No FAILs. G7 carries the load-bearing WATCH (advisory, not a block): the prior gated cast (h0020) was inert because the solver retyped the raw seed instead of the model — this variant's only net-new defense is the explicit "edit the model `.sql`, never the seed/`+column_types`" rule plus the copyable worked example. The decisive smoke read is therefore the ARTIFACT: did the committed `apply_patch` add `::timestamp` to `models/asana__task.sql` (and `asana002` clear `Got 2`), with the seed untouched and zero bleed on f1001/quickbooks003. Both bleed families carry 2 perturbable canaries so the h0009 convention-bleed surface is auditable at smoke; intercom is the only uncoverable family (no @baseline passer). Clear to advance to `smoke`.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: Forked solver README adds ONE Implementation-stage rule (observed-mismatch in-place `::type` cast IN THE MODEL `.sql`; additive/in-place only, no add/drop/rename, NEVER the raw seed; precondition-gated to a specific observed column, not broad re-typing; carries a copyable BEFORE→AFTER worked example)
  `diff codex-ade-dbt-minimal/README.md h0033.../README.md` = one additive hunk `63a64,108` under `## Stage: Implementation`; lines 1-49 byte-identical to parent; Exploration/Validation/Finalization + leak-guard untouched; grep of added lines for `AUTO_*`/`solution__*`/`verifier`/`Got N`/`drive-to-zero` → none.
- DONE: Specs — FULL (specs/h0033-...yaml) differs from baseline.yaml ONLY in `experiment:` + `solver_workflow:`; smoke adds ONLY benchmark.tasks (asana002 target + perturbable bleed canaries f1001 + quickbooks003 + sentinels airbnb001/ana-eng001/asana001); both frozen via `rk freeze --allow-missing`; kind=spacedock_solver/runtime=codex/trials=1 preserved
  Full diff = the two allowed fields only; smoke diff = only the added `benchmark.tasks:` block (6 `ade-bench-` slugs). `h0033...frozen.yaml` (1725B) + `h0033...smoke.frozen.yaml` (1863B) both carry kind/runtime; smoke frozen lists all 6 slugs, full frozen `tasks: null`. Baseline rewards resolved from `622bdedac572b479/per_trial_outcomes.json`: asana002=FAIL(0.0), f1001/quickbooks003/airbnb001/ana-eng001/asana001 all PASS(1.0).
- DONE: Gatekeeper ran; `## Gatekeeper review` block written (per-rule PASS/WARN/FAIL incl. G7 worked-example + G8 perturbable-canary coverage on f1/quickbooks + G10 N/A) + overall APPROVE with one-line rationale
  Recommendation APPROVE; G1-G6/G8 PASS, G7 PASS with the load-bearing inert-risk watch (h0020 retyped the seed not the model — the net-new defense is the explicit model-layer/never-seed rule + worked example, decisive at smoke via the committed `apply_patch` artifact read), G9/G10 N/A. Fork parent resolved to codex-ade-dbt-minimal via `source:` + @baseline registry agreement.

### Summary

Forked the `@baseline` solver into `solver_workflows/h0033-implementation-model-layer-dtype-cast` and added one Implementation-stage rule: when an output column's stored type/representation is OBSERVED to mismatch a sibling model's same column or the task instruction, fix it with a mechanical in-place `::<type>` cast IN THE MODEL `.sql` (worked example `due_at::timestamp`), additive/in-place only and NEVER editing the raw seed/source or `dbt_project.yml` `+column_types` (the h0020 wrong-layer failure), precondition-gated to that one observed column rather than broad re-typing (the h0009 convention-bleed). Because the lever is generative, the smoke panel doubles perturbable canaries on both h0009 bleed families (f1001 + quickbooks003) and adds the asana same-family sentinel plus airbnb/ana-eng passers; intercom is uncoverable (no @baseline passer). Full spec differs from baseline only in `experiment:`+`solver_workflow:`; smoke adds only `benchmark.tasks`; both specs frozen with kind/runtime preserved. Gatekeeper recommendation: APPROVE (no FAILs); the single advisory watch is G7's inert-risk (will the cast reach the model `.sql` and not the seed) — the decisive smoke read. Smoke NOT run per assignment; propose stops at the gate.
