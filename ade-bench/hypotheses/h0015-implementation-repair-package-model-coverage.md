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

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: README diff touches ONLY `## Stage: Implementation` (adds the single repair-task rule; leak-guard intact; source = LOCAL dbt_packages/ + project schema only; other stages + guardrails untouched; no hidden AUTO_*/solution__*/verifier refs)
  `diff codex-ade-dbt-minimal/README.md h0015-…/README.md` = one added hunk at line 64 under Implementation; forbidden-token grep over added lines returned none.
- DONE: Both specs frozen; FULL spec differs from baseline ONLY in experiment: + solver_workflow:; smoke spec adds ONLY benchmark.tasks; GENERATIVITY ASSESSMENT recorded in the G8 row with added canaries
  `diff baseline.yaml h0015-….yaml` = 2 fields; smoke diff = only `benchmark.tasks`; G8 judged generative → cross-family panel quickbooks003/airbnb001/asana001/f1001 added (intercom uncoverable: 0 baseline passers).
- DONE: Gatekeeper review block written into the hypothesis file: per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT + one-line rationale
  `## Gatekeeper review` block: 8/8 PASS, overall APPROVE; parent resolved @baseline=622bdedac572b479 → codex-ade-dbt-minimal.

### Summary

Forked the @baseline seed solver and added one Implementation-stage rule: on a repair/"fix the broken project" task, "builds green" is necessary but not sufficient — enumerate package-implied staging/intermediate models from the local `dbt_packages/` tree + project schema/refs and CREATE any absent ones by reproducing the installed package's own definition (copy, don't hand-roll). This is the CONCRETE counterpart to h0013's failed abstract prose: it plays to the one proven landing mechanism (h0009 asana002 copied a concrete local package artifact). Full spec differs from baseline in only experiment: + solver_workflow:; smoke spec adds quickbooks001 + ana-eng007-medium (targets), quickbooks004 (sentinel), and a cross-family G8 regression panel (quickbooks003/airbnb001/asana001/f1001) because the copy-package action is exactly h0009's convention-bleed family. Both specs frozen; gatekeeper review 8/8 PASS → APPROVE. Did NOT run smoke per dispatch.
