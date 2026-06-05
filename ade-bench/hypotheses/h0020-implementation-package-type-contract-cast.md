---
id: h0020
title: Implementation — adopt the installed package staging model's column TYPE for a same-named, same-layer output column by a mechanical in-place cast (precondition-gated, no add/drop/rename)
status: smoke
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type Type / contract mismatch (values right, column type/representation differs) — oracle 'Got N that disappears with a ::type cast'; target ade-bench-asana002 (asana__task due_at)); in-stage lever (Implementation). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed:
verdict:
score:
worktree:
---
## Hypothesis

The re-audit and the bug-type taxonomy agree that `asana002` is a **type / contract
mismatch**: the values are right but one column's declared type diverges from what the
installed package fixes, and the fix is a `::type` cast — the oracle signature is
`AUTO_asana__task_equality` failing `Got 2`, which disappears with a `due_at::timestamp`
cast. This is the loop's **one** confirmed FAIL→PASS flip from a README lever (h0009,
`asana002`), and the ledger's landed-mechanism analysis is unambiguous about *why* it
landed: a concrete copyable **local** artifact existed for the exact model being authored
(the installed `fivetran/asana_source` staging model under `dbt_packages/`), the required
edit was a **mechanical in-place substitution** (a type cast), not a structural rewrite,
and the solver was actively authoring the matching model so the precondition genuinely
held. The same ledger is equally clear about why h0009 was REJECTED: it stated the rule as
**ungated** Exploration prose ("reproduce the package's conventions exactly"), so the
generative instruction fired on the non-package majority and bled — `f1001` (a non-Fivetran
f1 project with NO package) got renamed to Fivetran `src_<dataset>__<entity>` style
(6/6→2/6) and `quickbooks003` got its intermediate/final columns trimmed to the narrower
package **staging** contract (14/14→11/14). Net at full scale: −1/48, REJECTED.

This hypothesis is the **scoped refinement of h0009 that the h0009 conclude block recorded
as unfiled** (archive lines ~290-323): keep the `asana002` type-cast win while suppressing
the convention bleed, by gating the rule with the three guardrails the conclude block
names — an **applicability gate** (act only when an installed `dbt_packages/` package model
is actually in the selected-from relation), a **same-layer match** (a staging type → the
staging-fed model; never impose a staging contract on an intermediate/final model), and
**do-no-harm** (types only, of an EXISTING same-named column; no add/drop/rename; the
project's own structure wins on conflict). It is narrowed further from h0009 in two ways:
(1) it touches **types only**, not the package's filters/dedup/column-set/grain/naming —
exactly the f1001/quickbooks003 bleed vectors; (2) it is an in-place cast on an existing
column, the mechanical-substitution edit shape that landed, not a structural directive.

Verified locally on the target workspace: `models/asana__task.sql` does
`select task.*` from `{{ var('task') }}`, and `dbt_project.yml` resolves
`task: "{{ ref('stg_asana__task') }}"` — `stg_asana__task` is **not** a local model
(no file under `models/`), so it is the installed `asana_source` staging model; `packages.yml`
pins `fivetran/asana_source [">=0.8.0","<0.9.0"]`, and `models/asana.yml` declares columns by
name/description but carries **no types**. So the `due_at` type contract is genuinely
readable only from the installed package's staging model / its column macro — a
leak-guard-allowed local signal — and the fix is a copyable in-place cast.

**Falsifiable claim (the single README change — Implementation stage only):** the seed
solver's Implementation prose says "follow local naming, materialization, source, ref,
macro, and schema patterns" but never tells the solver that a same-named column it sources
from an installed package staging model inherits that package model's **type**, so the
solver leaves `due_at` with the divergent type that `task.*` carries. Adding one
Implementation instruction — *when an output column you author/repair is the SAME-named
column sourced from an installed `dbt_packages/` staging model in the SAME layer, adopt the
package model's type for it by a matching in-place `::<type>` cast (or the project's
existing `+column_types`), values unchanged; do this only for an existing divergent-type
column the package also exposes — no add/drop/rename, no imposing package types/names where
no such package feeds the column or onto an intermediate/final model not sourced from it* —
will apply the `due_at::timestamp` cast and flip `asana002`, raising
`stratified_pass_at_1` above the `@baseline` 0.6458 **without** the h0009 f1001/quickbooks003
bleed.

**Why it escapes the dead-prose ceiling.** The inert/doomed family (h0010, h0011, h0013,
h0016) all asked the solver to RESTRUCTURE a query (which table to build FROM, join
direction, grain, the full column set, "build the complete set") — acknowledged-but-not-
executed, or premise-falsified because the target signal lived only in the hidden oracle.
This rule asks for none of that. It anchors to a **concrete local artifact** (the installed
`asana_source` staging model that `var('task')` already resolves to) and specifies a
**mechanical in-place substitution** (a single-column type cast) — the *exact* edit shape
that is the loop's only landed mechanism. The target signal is **locally derivable** (the
package type, not a hidden `solution__` seed), so it is not in the h0011 premise-
falsification zone. It does not add a post-hoc check, so it is not in the dead self-anchored
Validation family (h0006/h0007/h0008).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no new stage, no dataset,
harness, or solver-runtime change. Leak-guard intact (installed `dbt_packages/` package
model + the project's own `+column_types` and same-named columns only — no public fetch, no
oracle, no hidden `AUTO_*`/`solution__*` tests, no `Got N` magnitude, no
"drive-to-zero"/self-re-run phrasing; the cast leaves values unchanged so it cannot leak an
expected answer). The spec differs from baseline only in `experiment:` + `solver_workflow:`
(smoke adds only `benchmark.tasks`).

Target dataset (smoke, all `ade-bench-` prefixed): the type-mismatch failure
`ade-bench-asana002`. This rule is **generative** (it fires on every author/repair task
whose precondition holds, not on a single named target), so per gatekeeper G8 the smoke set
carries a cross-family regression-canary panel that specifically covers the populations the
h0009 targets-only smoke was structurally blind to: `ade-bench-asana001` (asana passer /
same-family sentinel), `ade-bench-f1001` (the **non-Fivetran f1** task h0009's convention
bleed broke — the load-bearing gate canary), `ade-bench-quickbooks003` (the **quickbooks
intermediate** h0009 trimmed to a staging contract — the load-bearing same-layer canary),
`ade-bench-quickbooks002` (quickbooks passer), `ade-bench-ana-eng001` (ana-eng passer), and
`ade-bench-airbnb001` (airbnb passer), plus `ade-bench-f1007` (f1 passer). **No intercom
canary is possible:** intercom has no passing `@baseline` task (`intercom001/002/003` all
fail), so that family cannot supply a passer — G8 should not expect one.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h<NNNN>-implementation-package-type-contract-cast.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Implementation` (the single package-type-cast rule appended after
the `dbt_packages/` preservation line), leaves Exploration/Validation/Finalization and the
dependency/package guardrails untouched, adds **no** new `## Stage:` block, and does not
reference hidden `AUTO_*`/`solution__*`/verifier tests or weaken the leak-guard.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on the target `asana002` + the canary panel (asana001, f1001,
quickbooks003, quickbooks002, ana-eng001, airbnb001, f1007), the variant must (1) **flip
`asana002` to a pass**, and (2) **not regress any canary** — in particular the f1001 and
quickbooks003 gate canaries that h0009 broke must hold. Per *verify the artifact, not the
chatter*: the smoke deep-dive must confirm the flip by reading the **committed
`apply_patch` payload** for a `::timestamp` / `+column_types` edit on `due_at` in
`asana__task` (the h0009 cast was inferred from the cleared mismatch, not directly
observed), and confirm the target's distance-to-pass dropped from the `@baseline`
failing state to passing — not merely that the transcript discussed package types.

## Gatekeeper review

**Recommendation: APPROVE** — single Implementation-stage package-type-cast rule; leak-guard byte-identical; spec differs only in the two allowed fields; smoke carries the full G8 canary panel including h0009's load-bearing bleed canaries.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-04). Reviewed 2026-06-05T11:40:00Z.

Fork parent resolved: `source:` names `solver_workflows/codex-ade-dbt-minimal`; `rk registry resolve run @baseline` → `runs/ade-bench-baseline/622bdedac572b479` whose `solver_workflow` is `./solver_workflows/codex-ade-dbt-minimal`. Agree → parent = `codex-ade-dbt-minimal`.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff = one hunk, lines 64-73, falls entirely under `## Stage: Implementation` (inserted after the `dbt_packages/` preservation line, before `## Stage: Validation`); one idea (adopt package staging model's type via in-place `::<type>` cast). No other `## Stage:` touched. |
| G2 leak-guard intact | PASS | Lines 1-49 byte-identical to parent (no-external-reference + dependency/package guardrails unchanged). Grep of added lines for `AUTO_*`/`solution__*`/`check_option`/`verifier`/`equality test`/`expected output`/`drive-to-zero`/`curl`/`wget`/`git clone`/`ls-remote` → NONE. Cast leaves values unchanged → cannot leak an expected answer. |
| G3 spec two fields | PASS | `diff baseline.yaml h0020...yaml` = only `experiment:` (→ ade-bench-h0020-...) and `solver_workflow:` (→ ./solver_workflows/h0020-...). `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0020...yaml h0020...smoke.yaml` = only an added `benchmark.tasks:` block. After the captain's propose-gate trim, all 3 slugs `ade-bench-` prefixed (asana002, f1001, quickbooks003); includes the hypothesis's named target `ade-bench-asana002`. |
| G5 both frozen | PASS | `h0020...frozen.yaml` (1733B) and `h0020...smoke.frozen.yaml` (1919B) both exist; both carry `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text = the Falsifiable claim verbatim in spirit: same stage (Implementation), same idea (same-named, same-layer, package-staging-sourced column → in-place `::<type>` cast, values unchanged, no add/drop/rename, no imposing where no package feed / on non-sourced intermediate/final). Generative-derive (tells solver how to build), reconciles against an independent local signal (the installed `dbt_packages/` staging model's declared type) — NOT self-anchored re-run/compare-to-own-output. No dead-family phrasing present. No scope creep beyond the claim. |
| G7 actionability/inert-risk | PASS | Mechanical substitution — a single-column in-place `::<type>` cast / `+column_types`, the exact edit shape of the loop's only durable win (asana002 `due_at::timestamp`). Not a structural FROM/spine/join/grain rewrite, so not in the inert "talks-but-doesn't-do" family. No worked-example skeleton needed for a cast. |
| G8 regression-canary coverage | PASS | Instruction is GENERATIVE but precondition-gated (fires only when a same-named column is sourced from an installed `dbt_packages/` staging model in the same layer). **Captain trimmed the panel at the propose gate** to the target + the 2 LOAD-BEARING h0009-bleed canaries: panel is now asana002 (🎯 target, baseline FAIL 0.0) + f1001 (f1, NO package — h0009 convention-bleed victim / applicability-gate test, baseline PASS 1.0) + quickbooks003 (quickbooks intermediate — h0009 same-layer trim victim / same-layer-guard test, baseline PASS 1.0). The other family passers (asana001, quickbooks002, ana-eng001, airbnb001, f1007) were dropped per the captain's call — the trim concentrates the smoke on the two specific failure modes this lever's gates exist to prevent. **Intercom remains uncoverable** (intercom001/002/003 all FAIL @baseline). Baseline rewards resolved from `622bdedac572b479/per_trial_outcomes.json`. |

**For the captain:** No FAILs, no WARNs. The two load-bearing canaries that broke h0009 at full scale (f1001 = applicability-gate test, quickbooks003 = same-layer test) are both present in the smoke panel, so the bleed-suppression claim is directly testable at smoke. The only family without a canary is intercom, which structurally cannot supply one (no baseline passer). Clear to advance to `smoke`.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: README diff touches ONLY `## Stage: Implementation` (adds the single precondition-gated in-place package-type-cast rule; no add/drop/rename; gated to same-named, same-layer, package-staging-sourced columns)
  `diff codex-ade-dbt-minimal/README.md h0020.../README.md` = one hunk (lines 64-73) under Implementation; lines 1-49 byte-identical; no `AUTO_*`/`solution__*`/verifier tokens in added text.
- DONE: Both specs frozen; FULL spec differs from baseline ONLY in experiment: + solver_workflow:; smoke adds ONLY benchmark.tasks; G8 panel + judgment recorded in gatekeeper block
  Full diff = 2 fields; smoke diff = only `benchmark.tasks:` (8 `ade-bench-` slugs: asana002 target + asana001/f1001/quickbooks003/quickbooks002/ana-eng001/airbnb001/f1007 canaries, all `@baseline` passers); intercom has no passer so no canary (recorded). Both `.frozen.yaml` exist with kind/runtime preserved.
- DONE: Gatekeeper review block written: per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT + one-line rationale
  Recommendation APPROVE (G1-G8 all PASS, no WARN); fork parent resolved to codex-ade-dbt-minimal via source: + @baseline registry.

### Summary

Forked the current `@baseline` solver into `solver_workflows/h0020-implementation-package-type-contract-cast`, adding one Implementation-stage rule: adopt an installed `dbt_packages/` staging model's column TYPE for a same-named, same-layer output column via an in-place `::<type>` cast (values unchanged; no add/drop/rename; gated so it never fires where no package feeds the column or on a non-sourced intermediate/final model). This is the scoped refinement of h0009's asana002 win, gated to kill the f1001/quickbooks003 convention bleed. Full spec differs from baseline only in `experiment:`+`solver_workflow:`; smoke adds only the `benchmark.tasks` panel (target asana002 + the two load-bearing h0009 bleed canaries f1001/quickbooks003 + passers; all canaries are confirmed `@baseline` passers). Both specs frozen with kind/runtime preserved. Gatekeeper recommendation: APPROVE (all eight rules PASS, no WARN). Smoke not run, per instruction.

## Stage Report: propose (cycle 2 — captain panel trim)

- DONE: smoke `benchmark.tasks` trimmed at the captain's propose-gate call to EXACTLY 3 slugs
  `ade-bench-asana002` (target) + `ade-bench-f1001` (applicability-gate canary) + `ade-bench-quickbooks003` (same-layer canary); asana001/quickbooks002/ana-eng001/airbnb001/f1007 dropped per captain; comment updated, intercom-uncoverable note retained.
- DONE: smoke spec re-frozen; FULL spec + FULL frozen untouched
  `rk freeze --allow-missing` rewrote `...smoke.frozen.yaml`; `grep ade-bench-` confirms the 3 slugs; full `.yaml`/`.frozen.yaml` not modified.
- DONE: Gatekeeper review G8 (and G4) rows updated to record the trim; addendum appended
  G8 now reads the 3-task panel (asana002 + f1001 + quickbooks003); G4 corrected from "8 slugs" to "3 slugs".

### Summary

Per the captain's revision at the propose gate, the smoke panel was trimmed from 8 tasks to 3: target `asana002` plus only the two load-bearing h0009-bleed canaries (`f1001` = applicability-gate test, `quickbooks003` = same-layer-guard test). The smoke spec was re-frozen; the FULL spec and its frozen file were left untouched. The Gatekeeper G8/G4 rows now reflect the trimmed panel. Smoke still not run.
