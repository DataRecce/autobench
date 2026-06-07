---
id: h0033
title: E4 -- Implementation; apply a mechanical in-place ::type cast in the MODEL .sql (never the raw seed) when a column's representation mismatches a sibling/instruction contract -- recover asana002 without convention-bleed
status: conclude
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

**Run dir:** `runs/ade-bench-h0033-implementation-model-layer-dtype-cast/33cf2891e1f5e6b6` (job `33cf2891e1f5e6b6`).
**Strict audit:** `summary {clean:6, tainted:0, coverage_missing:0}` — CLEAN. `captured=1` in every cell (all 6 `subagent-trace-manifest.json`).
**Score (focused):** `stratified_pass_at_1 = 1.0`, `n_pass = 6/6`, `n_errored = 0`. Above the `pass_rate` constant.

| Task | Role | @baseline | Smoke | Flip | Got N (base→smoke) | Cast in committed model? | Verdict |
|------|------|-----------|-------|------|--------------------|--------------------------|---------|
| asana002 | TARGET | FAIL (0.0) | PASS (1.0) | FAIL→PASS | Got 2 → 0 (cleared) | **NO — `{% if %}` rewrite, ZERO `::type` cast** | flip REAL but **lever INERT** |
| f1001 | perturbable bleed canary (h0009) | PASS | PASS (1.0) | held | 6/6 → 6/6 | no cast (no bleed) | HELD ✅ |
| quickbooks003 | perturbable bleed canary (h0009) | PASS | PASS (1.0) | held | 14/14 → 14/14 | no cast (no bleed) | HELD ✅ |
| airbnb001 | cross-family sentinel | PASS | PASS (1.0) | held | 10/10 → 10/10 | 0 files touched | HELD ✅ |
| ana-eng001 | cross-family sentinel | PASS | PASS (1.0) | held | 1/1 → 1/1 | 0 files touched | HELD ✅ |
| asana001 | asana same-family sentinel | PASS | PASS (1.0) | held | 2/2 → 2/2 | no cast (no bleed) | HELD ✅ |

**Decisive read (AC-2/AC-3):** the target flipped and zero canaries regressed, but the **lever did not cause the flip**. The committed `models/asana__task.sql` (apply_patch, worker session `019ea2b4…jsonl`) gained a Jinja `{% set using_task_tags = … %}` + `{% if using_task_tags %}` conditional-inclusion rewrite that gates the `task_tags` CTE/columns/join (plus matching `config(enabled=…)` on `int_asana__task_tags.sql` / `asana__tag.sql`) — the genuine fix for the instruction "Fivetran updated their Asana package; modify our data to match." The patch contains **NO `::<type>` cast** (the only `cast(...)` calls are `cast(null as {{ dbt.type_string() }})` placeholders for the disabled-tags branch). Files touched = model `.sql` only; the **raw seed and `+column_types` are untouched** (so NOT the h0020 wrong-layer mode — but moot, since the cast rule never fired at all). This satisfies the CAPPED inert-detector NO-GO: `Got 2` cleared via a solver-native structural fix, not via the prescribed mechanical `::type` cast.

## Run result

(smoke only — no full run; gated to `conclude`/REJECTED per the inert read below)

## Behavioral analysis

**Lever exercised?** No — not in the form it prescribes. The h0033 rule says "apply a mechanical in-place `::<type>` cast IN THE MODEL `.sql` when a column's representation mismatches a sibling/instruction." Across the whole 6-task smoke, **zero `::<type>` cast tokens** appear in any committed apply_patch (scanned `::timestamp|date|varchar|int|bigint|numeric|float|double|bool|text|decimal` in every worker session). The target was not a representation/type mismatch the cast could fix — it was a **structural package-migration** (tags became optional in the new Fivetran package), and the solver correctly fixed it with feature-flag gating, exactly the edit shape it lands on the baseline workflow.

**asana002 (target, flipped — non-causal):** committed `models/asana__task.sql` rewrite is `{% if using_task_tags %}`-gated CTE/columns/join + `cast(null as …)` placeholders; `int_asana__task_tags.sql` and `asana__tag.sql` get `config(enabled=…)`. No `::type` cast; seed/`+column_types` untouched. `AUTO_asana__task_equality` PASS (was FAIL 2). @baseline asana002 wrote **no patch at all** and FAILed — so the flip is real, but driven by the solver finally writing the correct structural fix, not by the cast rule.

**Bleed families (the decisive h0009 check):** f1001 worker made the normal f1 src_/stg_ build-out (28 files), quickbooks003 touched `dbt_project.yml` (a `using_department: true` var flip, NOT `+column_types`) + 3 models, asana001 touched `asana__project.sql`. **None contained a `::type` cast** → the convention-bleed h0009 failure mode did NOT recur. airbnb001/ana-eng001 sentinels: 0 files touched (lever never fired). All five HELD at 1.0.

**Classification:** asana002 = *flipped, but the change that reached the committed SQL was NOT the lever* (inert lever, solver-native structural fix). Canaries = *instruction inapplicable / never triggered* (no observed type mismatch to cast). The single advisory WATCH from the G7 gatekeeper note ("will the cast reach the model `.sql` and not the seed") resolves as: the cast reached **neither** — it was never written, because the target is not actually a `::type`-castable mismatch. Same wall as the earlier inert attempts: the loop's solver does not produce a bare representation cast here because the real bug isn't a representation mismatch.

**Variance caution honored:** the GO bar required an artifact-proven model-layer cast + Got 2 cleared + zero bleed. Got 2 cleared and zero bleed both hold, but the artifact proof FAILS — no cast in the committed model — so per the assignment ("bank a GO only on artifact-proven model-layer cast") this is NOT a GO regardless of the green score.

## Verdict

**NO-GO → conclude (REJECTED).** Falsifiable claim required the model-layer in-place `::type` cast to flip asana002. The hypothesis is **falsified on the "inert" disjunct**: asana002 flipped FAIL→PASS and zero canaries regressed, but the committed `models/asana__task.sql` gained a `{% if using_task_tags %}` conditional-inclusion rewrite with **ZERO `::<type>` casts** — the lever never fired. The flip is a solver-native structural fix (Fivetran made tags optional), not the prescribed cast; the cast rule added nothing causal. The seed-untouched / no-`+column_types` check passes (not the h0020 mode), and the h0009 convention-bleed did NOT recur (no cast bled into f1001/quickbooks003/asana001), but those are moot given the lever is inert on its own named target. Route: `conclude` (REJECTED). The recurring lesson holds — the loop's solver does not emit a bare representation `::type` cast when the actual bug is structural, so a "mechanical cast" Implementation rule has no surface to act on here.

## Stage Report: propose

- DONE: Forked solver README adds ONE Implementation-stage rule (observed-mismatch in-place `::type` cast IN THE MODEL `.sql`; additive/in-place only, no add/drop/rename, NEVER the raw seed; precondition-gated to a specific observed column, not broad re-typing; carries a copyable BEFORE→AFTER worked example)
  `diff codex-ade-dbt-minimal/README.md h0033.../README.md` = one additive hunk `63a64,108` under `## Stage: Implementation`; lines 1-49 byte-identical to parent; Exploration/Validation/Finalization + leak-guard untouched; grep of added lines for `AUTO_*`/`solution__*`/`verifier`/`Got N`/`drive-to-zero` → none.
- DONE: Specs — FULL (specs/h0033-...yaml) differs from baseline.yaml ONLY in `experiment:` + `solver_workflow:`; smoke adds ONLY benchmark.tasks (asana002 target + perturbable bleed canaries f1001 + quickbooks003 + sentinels airbnb001/ana-eng001/asana001); both frozen via `rk freeze --allow-missing`; kind=spacedock_solver/runtime=codex/trials=1 preserved
  Full diff = the two allowed fields only; smoke diff = only the added `benchmark.tasks:` block (6 `ade-bench-` slugs). `h0033...frozen.yaml` (1725B) + `h0033...smoke.frozen.yaml` (1863B) both carry kind/runtime; smoke frozen lists all 6 slugs, full frozen `tasks: null`. Baseline rewards resolved from `622bdedac572b479/per_trial_outcomes.json`: asana002=FAIL(0.0), f1001/quickbooks003/airbnb001/ana-eng001/asana001 all PASS(1.0).
- DONE: Gatekeeper ran; `## Gatekeeper review` block written (per-rule PASS/WARN/FAIL incl. G7 worked-example + G8 perturbable-canary coverage on f1/quickbooks + G10 N/A) + overall APPROVE with one-line rationale
  Recommendation APPROVE; G1-G6/G8 PASS, G7 PASS with the load-bearing inert-risk watch (h0020 retyped the seed not the model — the net-new defense is the explicit model-layer/never-seed rule + worked example, decisive at smoke via the committed `apply_patch` artifact read), G9/G10 N/A. Fork parent resolved to codex-ade-dbt-minimal via `source:` + @baseline registry agreement.

### Summary

Forked the `@baseline` solver into `solver_workflows/h0033-implementation-model-layer-dtype-cast` and added one Implementation-stage rule: when an output column's stored type/representation is OBSERVED to mismatch a sibling model's same column or the task instruction, fix it with a mechanical in-place `::<type>` cast IN THE MODEL `.sql` (worked example `due_at::timestamp`), additive/in-place only and NEVER editing the raw seed/source or `dbt_project.yml` `+column_types` (the h0020 wrong-layer failure), precondition-gated to that one observed column rather than broad re-typing (the h0009 convention-bleed). Because the lever is generative, the smoke panel doubles perturbable canaries on both h0009 bleed families (f1001 + quickbooks003) and adds the asana same-family sentinel plus airbnb/ana-eng passers; intercom is uncoverable (no @baseline passer). Full spec differs from baseline only in `experiment:`+`solver_workflow:`; smoke adds only `benchmark.tasks`; both specs frozen with kind/runtime preserved. Gatekeeper recommendation: APPROVE (no FAILs); the single advisory watch is G7's inert-risk (will the cast reach the model `.sql` and not the seed) — the decisive smoke read. Smoke NOT run per assignment; propose stops at the gate.

## Stage Report: smoke

- DONE: Smoke run completed on specs/h0033-implementation-model-layer-dtype-cast.smoke.frozen.yaml with a CLEAN strict audit (rk audit --policy strict => tainted:0) and captured>0 in every cell; the focused rk score is recorded in ## Smoke result
  Run dir `runs/ade-bench-h0033-implementation-model-layer-dtype-cast/33cf2891e1f5e6b6`; audit `summary {clean:6, tainted:0, coverage_missing:0}`; captured=1 in all 6 manifests; `rk score` = stratified_pass_at_1 1.0, 6/6 pass, 0 errored.
- DONE: Per-target deep-dive on asana002 — Got 2 cleared (AUTO_asana__task_equality FAIL 2 -> PASS) BUT artifact NOT proven: committed models/asana__task.sql gained a `{% if using_task_tags %}` conditional-inclusion rewrite with ZERO `::type` cast; seed + `+column_types` UNTOUCHED (not h0020). CAPPED inert-detector => NO-GO. Zero of the 5 canaries regress; no cast bled into f1001/quickbooks003 (the h0009 bleed check) or asana001
  Worker session `019ea2b4…jsonl` apply_patch: files = model `.sql` only; only `cast(null as {{ dbt.type_string() }})` placeholders, no `::<type>`. f1001 6/6, quickbooks003 14/14, airbnb001 10/10, ana-eng001 1/1, asana001 2/2 — all HELD; cast-token scan = NONE in every worker patch.
- DONE: Plain-words go/no-go to the captain — NO-GO (conclude/REJECTED); inert lever (Got 2 cleared via solver-native feature-flag fix, not the prescribed `::type` cast)
  Verdict written in ## Verdict; one smoke, no iteration (CAPPED).

### Summary

Smoke ran clean (strict audit tainted:0, captured>0 all cells; rk score 6/6 = 1.0). asana002 flipped FAIL->PASS and zero canaries regressed, but the decisive artifact read shows the h0033 lever is INERT: the committed models/asana__task.sql gained a Jinja `{% if using_task_tags %}` conditional-inclusion rewrite (the genuine fix for the Fivetran "tags became optional" package migration) with ZERO `::<type>` casts. Seed/`+column_types` untouched (not the h0020 wrong-layer mode) and no cast bled into either h0009 bleed family (f1001/quickbooks003 both HELD, no cast in any committed patch) — but both are moot since the cast rule never fired on its own named target. The flip is solver-native and non-causal. Per the CAPPED inert-detector and the artifact-proof GO bar, this is a NO-GO -> conclude (REJECTED). In-stage lever, no structural workflow change => WORKFLOW-REFINE.md N/A.

## Stage Report: conclude

- DONE: Finalize the bug-type-taxonomy.md #5 (type/contract, asana002) row + per-type lesson: mark h0033 REJECTED -- the mechanical-cast lever was INERT ... asana002 is a STRUCTURAL package-migration bug, NOT a representation/type mismatch ... cast-lever family is now EXHAUSTED for asana002 (h0009 bled / h0020 seed-layer / h0033 no-surface)
  Updated `_artifacts/bug-type-taxonomy.md`: per-task ground-truth row (asana002 re-classified `type/contract` → `structural package-migration`, `{% if using_task_tags %}` fix, flips solver-native); board row #5 (struck `asana002`, added h0033 REJ, "CAST-LEVER FAMILY EXHAUSTED for asana002 — do not re-file"); per-type lesson #5 rewritten (3-rejection convergence, green-but-inert, run-dir `33cf2891e1f5e6b6`); Meta-pattern scoreboard appended `h0033 INERT`.
- DONE: Record the transferable lesson in the instruction-lever taxonomy / verification-without-oracle as appropriate: a 'mechanical cast/edit' lever is INERT when the real bug is STRUCTURAL ... attribution requires the prescribed artifact in the COMMITTED SQL, not a green flip (the E4 green-but-inert case)
  `_artifacts/verification-without-oracle.md`: new subsection "A green flip is not lever attribution — the inert lever / green-but-inert failure (h0033)" + reach-map #5 revised down (asana002 re-classified structural, cast family exhausted). Instruction-lever memory note (`~/.claude/.../ade-bench-instruction-lever-taxonomy.md`, not repo-tracked): META-FINDING scoreboard + full h0033 RESULT block + new "mechanical cast inert when bug is structural / green flip ≠ attribution" principle.
- DONE: Verdict narrative REJECTED; per conclude discipline DO NOT auto-file a cast follow-up (family exhausted for asana002)
  `## Verdict` (NO-GO → REJECTED) already written by the smoke ensign and confirmed correct; NO cast follow-up filed; the exhaustion note ("do not re-file a cast lever for asana002") is now recorded in both `_artifacts` records and the memory note.

### Summary

Finalized the cross-experiment records for h0033 (REJECTED, inert lever) without re-running analysis — the smoke ensign had already written `## Smoke result`/`## Behavioral analysis`/`## Verdict`. The sharp finding: asana002 is a STRUCTURAL package-migration bug (Fivetran made `task_tags` optional, fixed by a `{% if using_task_tags %}` conditional-inclusion rewrite), NOT a type/contract representation mismatch, so the prescribed mechanical `::type` cast had no surface to act on; the target flipped solver-native, not lever-attributable. Re-classified bug-type #5 (asana002 struck from type/contract), recorded the cast-lever family as EXHAUSTED for asana002 across h0009/h0020/h0033, and captured the transferable E4 lesson (a green flip is not lever attribution — confirm the prescribed artifact in the committed patch) in `verification-without-oracle.md` and the instruction-lever memory note. In-stage Implementation tweak, not structural → WORKFLOW-REFINE.md N/A; frontmatter (verdict/completed) + archive left to the FO.
