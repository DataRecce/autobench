---
id: h0015
title: Implementation — on repair/fix-it tasks, create the package-implied models that are missing by copying the installed package's definition
status: smoke
kind: hypothesis
source: forked from the h0009 smoke deep-dive — quickbooks001 is a separate gap from the grain-spine cluster: it is a passive "the project is broken, fix it" task where the solver fixes the one visible compile error, sees the build go green, and STOPS — even though dbt_packages/quickbooks_source literally contains the 3 missing staging models the grader wants (stg_quickbooks__estimate/refund_receipt/sales_receipt). Plays to the one proven mechanism (h0009 asana002: copying a concrete local package artifact LANDS; h0010 showed prose-described structural rewrites do NOT). Forks the then-current @baseline (re-fork at propose; @baseline 622bdedac572b479 unless h0009 promotes first).
started: 2026-06-05T08:58:01Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`quickbooks001` is a "the project is erroring out, fix it" task. The solver fixes the one
visible compile error (a missing `quickbooks__general_ledger` ref), the project then builds
green, and it **declares done** — but the grader expects 3 staging models
(`stg_quickbooks__{estimate,refund_receipt,sales_receipt}`) that were never created. Both
`@baseline` and h0009 failed all 6 of those checks (existence + equality) identically. The
key fact: those 3 models are **present in the installed `quickbooks_source` package** under
`dbt_packages/` — the answer is local and copyable, not something to invent. The solver
never looked because a passive "fix-it" framing gave it no trigger to build anything once
the project compiled.

This plays directly to the mechanism that WORKS: h0009's only flip (asana002) came from the
solver **copying a concrete local package artifact** (a column-type contract); h0010 proved
the solver will NOT implement a structurally-described rewrite from prose. Copying a
package-defined model is the former, not the latter.

**Falsifiable claim (the single README change — Implementation stage only):** the seed
solver's Implementation prose classifies the task (no-op/repair/creation/…) and fixes the
smallest visible failure, but for **repair / "broken project" tasks it stops at "builds
green"** and never checks for package-implied models that should exist but don't. Adding one
Implementation instruction — *on a repair / "fix the broken project" task, "builds green" is
necessary but NOT sufficient: enumerate the staging/intermediate models the installed
package(s) under `dbt_packages/` and the project's own schema/refs imply the project should
expose, and for any that are absent, create them by reproducing the installed package's
definition for that entity (copy the package's model/macro usage; do not hand-roll). Do not
finalize a repair task while a package-implied model the project is meant to expose is
missing* — will create the 3 missing quickbooks staging models and flip `quickbooks001`,
raising `stratified_pass_at_1` above `@baseline`.

Method/README change only; forks the then-current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal` unless h0009 promotes first), runtime codex,
gpt-5.5. Leak-guard intact: the source is the **local** `dbt_packages/` tree and the
project's own schema/refs — no public fetch, no `git clone`, no oracle, no reference to the
hidden `AUTO_*` tests. One idea, one stage (Implementation, repair-task handling).

Target datasets (smoke, all `ade-bench-` prefixed): `ade-bench-quickbooks001` (the 3
missing-model target) + `ade-bench-ana-eng007-medium` (another "the project is broken, fix
it" task) + a stable-`@baseline`-pass regression sentinel `ade-bench-quickbooks004`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0015-implementation-repair-package-model-coverage.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs the `@baseline` solver
touches only `## Stage: Implementation` (the single repair-coverage instruction), leaves the
other stages + dependency/package guardrails untouched, and does not reference hidden
`AUTO_*`/verifier tests or weaken the leak-guard. `agent.kind: spacedock_solver`,
`runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean,
`captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
plus the absolute `stratified_pass_at_1` vs `@baseline`.**

**Smoke gate:** must not regress the `quickbooks004` sentinel and should flip
`quickbooks001` (and/or `ana-eng007-medium`) to a pass; the post-smoke deep-dive must
confirm the solver actually CREATED the missing models from the package (artifact check),
not merely discussed coverage.

## Gatekeeper review

**Recommendation: APPROVE** — single Implementation-stage repair-coverage rule; leak-guard byte-intact; specs differ in only the two allowed fields; the copy-the-package-definition action is the one proven landing mechanism (h0009 asana002), and the generative-class copy action is covered by a cross-family G8 panel.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-04). Reviewed 2026-06-05T09:30:00Z. Fork parent resolved: `@baseline` = `runs/ade-bench-baseline/622bdedac572b479` → `solver_workflows/codex-ade-dbt-minimal` (matches `source:`).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is one hunk at line 64, falling under `## Stage: Implementation` (before `## Stage: Validation`); adds exactly the repair-task package-model-coverage rule, no other stage touched. |
| G2 leak-guard intact | PASS | grep of added lines for `AUTO_/solution__/check_option/verifier/equality test/expected output/curl/wget/git clone/ls-remote/download/web` → none; no-fetch + dependency-preservation paragraphs byte-identical to parent; added text scopes source to "the local task workspace (`dbt_packages/` and the project's own schema/refs)". |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0015-….yaml` shows only `experiment:` (line 2) + `solver_workflow:` (line 11); `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | smoke vs full diff = single added `benchmark.tasks:` block; all 7 slugs `ade-bench-` prefixed; both hypothesis targets (quickbooks001, ana-eng007-medium) present. |
| G5 both frozen | PASS | `…frozen.yaml` + `…smoke.frozen.yaml` both written; both carry `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text mirrors the Falsifiable claim verbatim in spirit: repair task → "builds green" necessary-not-sufficient → enumerate package-implied staging/intermediate models from `dbt_packages/` + project schema/refs → CREATE absent ones by reproducing the installed package's definition (copy, don't hand-roll) → don't finalize while a package-implied model is missing. Generative/independent (copy a concrete local artifact), NOT self-anchored re-run-your-own-output (the dead h0006/7/8 family). |
| G7 actionability/inert-risk | PASS | Mechanical-copy class: "reproduce the installed package's own definition … copy the model SQL and macro usage." This is the concrete copyable-artifact form (the lone durable win, h0009 asana002), NOT the abstract-structural rewrite that proved inert in h0010/h0016. No worked-example skeleton needed because the artifact to copy already exists locally under `dbt_packages/`. |
| G8 regression-canary coverage | PASS | Judged GENERATIVE: gated on "repair task + package-implied model missing", but "repair" classification fires broadly and the copy-package action is the exact family that bled in h0009 (f1001 + quickbooks003 PASS→FAIL at full scale). Cross-family panel added: quickbooks003 (same-package bleed victim), airbnb001, asana001, f1001 — each a `@baseline` passer from a non-target family. intercom family has ZERO `@baseline` passers (no canary possible) — documented, not a gap the panel can fill. ana-eng is a target family (ana-eng007-medium), so no separate ana-eng canary. |

**For the captain:** All eight rules PASS — advance to smoke. The one judgment call is G8: I classified the lever as generative-enough to warrant a panel (the copy-package action is h0009's convention-bleed family), so the smoke set carries quickbooks003 + airbnb001 + asana001 + f1001 as cross-family tripwires beyond the quickbooks004 sentinel. intercom is uncoverable (0 baseline passers). The smoke-gate deep-dive must verify the solver actually CREATED the 3 `stg_quickbooks__*` models from the package (artifact check), not merely discussed coverage.

## Smoke result

**Verdict: NO-GO → conclude REJECTED.** 0/2 targets flipped AND the f1001 canary
regressed (1→0). A canary dropping to FAIL is a NO-GO regardless of target flips; here
both targets were also inert, so there is nothing to weigh against the regression.

- Run-dir: `runs/ade-bench-h0015-implementation-repair-package-model-coverage/36c1bcd6bbe217fd`
- **Clean-audit attestation (AC-2):** `rk audit … --policy strict` →
  `summary: {clean: 7, coverage_missing: 0, tainted: 0}`; all 7 trials `taint_status: clean`;
  every cell `subagent-trace-manifest` captured = 1 (>0). Score trusted.
- `rk score` → `stratified_pass_at_1 = 0.5714` (4/7), n_completed 7, n_errored 0.
  vs `@baseline` 622bdedac572b479 on the SAME 7 slugs = 5/7 (0.7143) → **−1 net (one
  canary lost, zero targets gained)**.

| Task | Role | base→smoke | dbt distance (Got N) base→smoke | Why |
|------|------|-----------|--------------------------------|-----|
| quickbooks001 | TARGET | 0→0 ❌ | 6 FAIL → 6 FAIL (3 stg ×{exist,equal}, all `Got 1`) — IDENTICAL | **Rule INERT.** Solver fixed the one visible compile error (`quickbooks__general_ledger.sql`), built green (`PASS=172`), declared done — exactly the baseline failure mode. Never created the 3 `stg_quickbooks__*` models. |
| ana-eng007-medium | TARGET | 0→0 ❌ | 1 FAIL → 1 FAIL (`AUTO_dim_products_equality Got 5`) — IDENTICAL | **Rule inapplicable.** `dim_products` already EXISTS; failure is a 5-row value gap, not a missing package model. Solver fixed 2 unrelated models, built green, stopped. |
| f1001 | CANARY | 1→0 ❌ **REGRESSION** | 6/6 PASS → 5/6 (`src_models_are_correct Got 14`) | **CONVENTION-BLEED.** Rule made solver invent 14 spurious `src_*.sql` "source" models + rewrite all 13 `stg_f1_dataset__*` to ref them. The project's own guard `src_models_are_correct` catches exactly those 14 wrong rows. |
| quickbooks003 | CANARY | 1→1 ✅ | — | Held (same-package bleed victim from h0009 — held here). |
| quickbooks004 | SENTINEL | 1→1 ✅ | — | Held. |
| airbnb001 | CANARY | 1→1 ✅ | — | Held. |
| asana001 | CANARY | 1→1 ✅ | — | Held. |

**Load-bearing artifact check (smoke-gate requirement):** the smoke-gate demanded confirmation
the solver actually CREATED the 3 `stg_quickbooks__{estimate,refund_receipt,sales_receipt}`
models, not merely discussed them. CONFIRMED NEGATIVE — they were not created. The
quickbooks001 verifier is byte-identical to baseline (the 3 `*_existence` tests still return
`Got 1 result`, the missing-model sentinel), and the FO's final report lists exactly one
changed file (`models/quickbooks__general_ledger.sql`) with no staging models added. The
package-copy rule did not fire on its primary target.

## Run result

Not run. Smoke is NO-GO (canary regression); do not promote to full.

## Behavioral analysis

The hypothesis was the concrete counterpart to h0013's failed abstract prose: bet that the
ONE proven landing mechanism (h0009 asana002 — copy a concrete local package artifact) would
carry quickbooks001 by telling the solver, on a repair task, to copy the 3 package-defined
staging models out of `dbt_packages/`. Smoke falsified it on two independent fronts:

1. **Inert on the primary target (the bet's whole point).** On quickbooks001 the solver
   behaved IDENTICALLY to baseline: classified the task, fixed the single visible compile
   error (the missing `quickbooks__general_ledger` ref), saw `dbt build PASS=172`, and
   declared done. The new Implementation instruction — "builds green is necessary but NOT
   sufficient … enumerate package-implied models … create any that are absent by copying the
   `dbt_packages/` definition" — produced ZERO behavioral change: no `stg_quickbooks__*`
   model was created, the same 6 tests fail with the same `Got 1`. The "copy a concrete local
   artifact" framing did NOT transfer from h0009's single-column-contract copy (asana002) to
   a multi-model staging-layer reconstruction. The instruction reads as a generic
   "be thorough" exhortation the solver discounts once the build is green — the same
   passive-repair stop-at-green failure h0009's deep-dive originally flagged.

2. **Convention-bleed regression on a non-target family (the gatekeeper G8 risk, realized).**
   The exact failure the G8 row predicted happened: on f1001 — a non-Fivetran f1 task whose
   project does NOT use a `src_` source-view layer — the solver mis-applied the
   "enumerate package-implied staging/source models the project is meant to expose" rule. It
   invented 14 new `src_*.sql` view models and rewrote all 13 `stg_f1_dataset__*` models to
   select from them, hallucinating the dbt-package src-layer idiom onto a project that never
   had it. The project's own shipped guard `src_models_are_correct` flips to `Got 14 results`
   — it is literally counting the 14 spurious models. f1001 was the same victim that broke at
   h0009 full scale; the lever reproduced that bleed at smoke scale on a 7-task panel. This is
   the generative downside materializing: the rule is gated on "repair task + package-implied
   model missing," but "repair" fires broadly and the model the rule decides is "missing"
   is, on f1, a model the project deliberately does not expose.

3. **Structurally inapplicable on the secondary target.** ana-eng007-medium's lone failure is
   a 5-row value mismatch in an EXISTING model (`dim_products`); there is no absent
   package-implied model for the rule to create, so it was a no-op (distance identical to
   baseline). This target was never a fit for a missing-model lever.

Net: the rule is simultaneously too weak where it was supposed to land (inert on
quickbooks001, the bet) and too strong where it must not fire (fabricates a source layer on
f1001). Both are classic h0010/h0009 signatures — prose-described structural reconstruction
does not land, and a broadly-firing "expose more models" instruction bleeds the dominant
package convention onto families that don't use it. The README-prose ceiling holds: a single
Implementation paragraph cannot make the solver reconstruct a multi-model staging layer it
otherwise stops short of, and the same paragraph actively damages projects outside the
package's convention.

## Verdict

**REJECTED at smoke (NO-GO).** f1001 canary regressed 1→0 via h0009-style convention-bleed
(14 hallucinated `src_*` models) — a NO-GO on its own — and BOTH targets were inert
(quickbooks001 byte-identical to baseline, the 3 `stg_quickbooks__*` models never created;
ana-eng007-medium structurally inapplicable). Net −1 on the 7-task panel (5/7 → 4/7).
Routing: **conclude REJECTED**. Do not promote to full.

## Stage Report: propose

- DONE: README diff touches ONLY `## Stage: Implementation` (adds the single repair-task rule; leak-guard intact; source = LOCAL dbt_packages/ + project schema only; other stages + guardrails untouched; no hidden AUTO_*/solution__*/verifier refs)
  `diff codex-ade-dbt-minimal/README.md h0015-…/README.md` = one added hunk at line 64 under Implementation; forbidden-token grep over added lines returned none.
- DONE: Both specs frozen; FULL spec differs from baseline ONLY in experiment: + solver_workflow:; smoke spec adds ONLY benchmark.tasks; GENERATIVITY ASSESSMENT recorded in the G8 row with added canaries
  `diff baseline.yaml h0015-….yaml` = 2 fields; smoke diff = only `benchmark.tasks`; G8 judged generative → cross-family panel quickbooks003/airbnb001/asana001/f1001 added (intercom uncoverable: 0 baseline passers).
- DONE: Gatekeeper review block written into the hypothesis file: per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT + one-line rationale
  `## Gatekeeper review` block: 8/8 PASS, overall APPROVE; parent resolved @baseline=622bdedac572b479 → codex-ade-dbt-minimal.

### Summary

Forked the @baseline seed solver and added one Implementation-stage rule: on a repair/"fix the broken project" task, "builds green" is necessary but not sufficient — enumerate package-implied staging/intermediate models from the local `dbt_packages/` tree + project schema/refs and CREATE any absent ones by reproducing the installed package's own definition (copy, don't hand-roll). This is the CONCRETE counterpart to h0013's failed abstract prose: it plays to the one proven landing mechanism (h0009 asana002 copied a concrete local package artifact). Full spec differs from baseline in only experiment: + solver_workflow:; smoke spec adds quickbooks001 + ana-eng007-medium (targets), quickbooks004 (sentinel), and a cross-family G8 regression panel (quickbooks003/airbnb001/asana001/f1001) because the copy-package action is exactly h0009's convention-bleed family. Both specs frozen; gatekeeper review 8/8 PASS → APPROVE. Did NOT run smoke per dispatch.

## Stage Report: smoke

- DONE: Smoke run completed on the 7-task frozen spec; strict audit clean (tainted:0) + subagent-trace-manifest captured>0 BEFORE trusting score; focused `rk score` recorded with clean-audit attestation and run-dir
  `rk audit --policy strict` → `summary {clean:7, coverage_missing:0, tainted:0}`, all 7 trials clean, each cell manifest captured=1; `rk score` → stratified_pass_at_1=0.5714 (4/7); run-dir 36c1bcd6bbe217fd. Written into ## Smoke result.
- DONE: Deep-dive on BOTH targets (verdict delta + distance-to-pass vs @baseline) AND the load-bearing artifact check for quickbooks001 (3 stg models created?); all 5 guards confirmed with special attention to quickbooks003 + f1001
  quickbooks001 0→0 INERT (6→6 FAIL, `Got 1`; 3 `stg_quickbooks__*` NOT created — FO changed only `quickbooks__general_ledger.sql`); ana-eng007-medium 0→0 inert (1→1 FAIL `Got 5`, dim_products already exists); **f1001 1→0 REGRESSION** (convention-bleed: 14 invented `src_*` models, `src_models_are_correct Got 14`); quickbooks003/quickbooks004/airbnb001/asana001 all held PASS. Written into ## Smoke result + ## Behavioral analysis.
- DONE: Plain-language go/no-go with one-line reason + gate routing recommendation, led by verdict not tables
  NO-GO — f1001 canary regressed via h0009 convention-bleed AND both targets inert (net −1); route to conclude REJECTED. In ## Verdict.

### Summary

Smoke is a clean NO-GO. The strict audit was clean (7/7, tainted:0, manifests captured) so the score is trusted: 4/7 vs @baseline's 5/7 on the same slugs = −1 net. The package-copy rule was INERT on its primary target — quickbooks001 is byte-identical to baseline (the solver fixed the one visible compile error, built green at PASS=172, and stopped; the 3 `stg_quickbooks__{estimate,refund_receipt,sales_receipt}` models were never created, so the `*_existence` tests still return `Got 1`). The same rule REGRESSED the f1001 canary by reproducing the exact h0009 convention-bleed: it hallucinated 14 `src_*` source-view models + rewrote all 13 `stg_f1_dataset__*` to ref them on a project that uses no src layer, tripping the project's own `src_models_are_correct` guard (`Got 14`). ana-eng007-medium was structurally inapplicable (failure is a 5-row value gap in an existing model). A canary regression is a NO-GO on its own; with both targets inert there is no offsetting flip. Recommend conclude REJECTED — the README-prose ceiling holds (one Implementation paragraph cannot make the solver reconstruct a missing multi-model staging layer, and it actively damages non-package-convention families).
