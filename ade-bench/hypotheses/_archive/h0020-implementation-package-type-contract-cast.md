---
id: h0020
title: Implementation — adopt the installed package staging model's column TYPE for a same-named, same-layer output column by a mechanical in-place cast (precondition-gated, no add/drop/rename)
status: conclude
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type Type / contract mismatch (values right, column type/representation differs) — oracle 'Got N that disappears with a ::type cast'; target ade-bench-asana002 (asana__task due_at)); in-stage lever (Implementation). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed: 2026-06-05T13:28:58Z
verdict: REJECTED
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

**Verdict: NO-GO.** Target did not flip AND a load-bearing canary regressed.

- Run-dir (real): `/home/kent/.local/share/razorback/runs/ade-bench-h0020-implementation-package-type-contract-cast/1ec768e85f5d4579`
  Methodology aside: the `--runs-dir runs` flag did not take; results landed under the default
  `~/.local/share/razorback/runs/...`, not `ade-bench/runs/`. Data is valid; audit/score were run against the real dir.
- Strict audit: **clean** — `tainted: 0, clean: 3, coverage_missing: 0`; subagent-trace-manifest `captured: 1` on all 3 trials (>0). Score trusted.
- Score: `stratified_pass_at_1 = 0.3333` (1/3), Wilson CI [0.061, 0.792], verdict "above" the 0.1875 paper constant — but that constant is irrelevant; the gate is vs @baseline per-task.

| Task | Role | @baseline | smoke | Distance | Flip? |
|------|------|-----------|-------|----------|-------|
| asana002 | 🎯 target | FAIL (Got 2) | FAIL (Got 2) | **unchanged 2→2** | ❌ NO FLIP |
| f1001 | applicability-gate canary | PASS 6/6 | PASS 6/6 | held | ✅ HELD |
| quickbooks003 | same-layer-guard canary | PASS 14/14 | **FAIL 11/14** | 3 models "less columns than solution" | ❌ **REGRESSION** |

Artifact checks (verify the artifact, not the chatter):
- **asana002 cast did NOT land on the model.** The only `apply_patch Update File` was `dbt_project.yml`
  (seed `+column_types` id string→bigint). The `due_at`/`due_on`/`start_on` casts the solver applied were
  inside an `exec_command` python that `ALTER`ed the raw `asana.duckdb` seed tables — the SAME wrong layer the
  @baseline hit. `models/asana__task.sql` was read (5×) but never patched. No `due_at::timestamp` / `+column_types`
  edit on `due_at` in `asana__task`. Outcome (a): the lever was inert for the target; `AUTO_asana__task_equality` still `Got 2`.
- **quickbooks003 regression is NOT the h0020 cast lever firing.** The 24 `::timestamp` tokens are pre-existing
  model code read during exploration, not edits. The regression is a task-level under-edit: the `using_department`-removal
  task was done by unwrapping the `{% if var('using_department', True) %}` guards (keeping `departments` CTE +
  `department_name` + joins) and dropping `using_department: true` from `dbt_project.yml`. @baseline (PASS) did a
  SECOND patch that fully DELETED the departments CTE / `department_name` / joins; the variant stopped after the unwrap,
  so the three models' column set diverged from `solution__*` → `default__test_equality` raised "X has less columns than
  solution__X" compile errors on `int_quickbooks__expenses_union`, `int_quickbooks__sales_union`, `quickbooks__ap_ar_enhanced`.
- **f1001 held.** 6/6 PASS. It created the project's OWN local `models/staging/f1_dataset/src_*.sql` + `stg_f1_dataset__*`
  models; no `fivetran` token, no `src_<dataset>__<entity>` double-underscore Fivetran rename. The applicability gate
  effectively held (no installed `dbt_packages/` staging model feeds f1001, so the lever did not fire / cause harm).

## Run result

Not run. Smoke gate is NO-GO; per assignment this stage ends at the go/no-go gate (no promote, no full).

## Behavioral analysis

The smoke falsifies the hypothesis on both arms.

1. **The cast lever is inert on the target (the same way the prior dead-prose family was inert).** The hypothesis
   bet that anchoring to a concrete local artifact (the installed `asana_source` staging model) + prescribing a
   mechanical in-place `::timestamp` cast would escape the dead-prose ceiling. It did not. The solver never edited
   `models/asana__task.sql`; it re-attacked the raw `asana.duckdb` / seed `+column_types` layer — exactly the
   @baseline behavior. So h0009's asana002 flip did NOT come from a `due_at::timestamp` cast on the model (the AC-2
   "verify the artifact" check the conclude block demanded): the @baseline-style raw-data path leaves `Got 2`, and the
   h0009 flip mechanism was something else (a raw-data shape change that happened to clear the mismatch), not the cast
   this README rule prescribes. The lever's premise — "tell the solver to cast the same-named package-sourced column
   in the model" — is mis-targeted: the solver does not author the cast at the model layer for this task.

2. **The same-layer guard never got a chance to work, and a sibling failure mode bit instead.** quickbooks003 did not
   regress because the lever imposed a package staging contract (the h0009 mechanism the guard was written to stop) —
   the lever did not fire on quickbooks003 at all. It regressed because the variant under-performed the *unrelated*
   `using_department`-removal task relative to @baseline (unwrap-only vs full-delete). This is run-to-run solver
   variance on a hard multi-model edit, not a lever bleed. But the smoke gate is outcome-based: a load-bearing canary
   dropped FAIL, which is a NO-GO regardless of attribution. The bleed-suppression claim is therefore *untested* (the
   lever was inert everywhere), and the canary that was supposed to prove the guard instead regressed for an orthogonal
   reason — leaving zero evidence the guard adds value and direct evidence the variant does not reliably hold the line.

Net: 0/1 target flip + 1/2 load-bearing canaries regressed. The lever did not reach the model layer on the target
(inert, dead-prose-family behavior) and bought no demonstrable bleed protection. This is the README-prose ceiling
reasserting itself on a cast just as it did on the restructure family (h0010/h0011/h0013/h0016).

## Verdict

**REJECTED — cleanly falsified at smoke (NO-GO); no full run. Score: 1/3 (`stratified_pass_at_1 = 0.3333`).**

The hypothesis routed `smoke → conclude` without a full run: the smoke deep-dive is the evidence of record. Real
run-dir: `/home/kent/.local/share/razorback/runs/ade-bench-h0020-implementation-package-type-contract-cast/1ec768e85f5d4579`.
Strict audit clean (`tainted: 0, clean: 3, coverage_missing: 0`, subagent-trace-manifest `captured: 1` on all 3);
`stratified_pass_at_1 = 0.3333`. *Methodology aside:* the `--runs-dir runs` flag did not take — results landed in the
default razorback runs dir, not `ade-bench/runs/`; data is valid and audit/score were run against the real dir.

**Mechanism (from the smoke deep-dive):**

- **asana002 — INERT (NO FLIP, Got 2→2).** The prescribed in-place `due_at::timestamp` cast NEVER landed on
  `models/asana__task.sql` (read 5×, never patched). The solver instead edited `dbt_project.yml` `+column_types`
  and ran an `exec_command` python that `ALTER`ed the raw `asana.duckdb` seed tables — its wrong-layer habit, the
  same layer @baseline hit. `AUTO_asana__task_equality` still `Got 2`. The most concrete, most-favorable in-place-cast
  prose was inert at the model layer.
- **f1001 — HELD (PASS 6/6).** The applicability gate effectively worked: f1001 built its OWN local
  `models/staging/f1_dataset/src_*.sql` + `stg_f1_dataset__*` models with no `fivetran` token and no
  `src_<dataset>__<entity>` Fivetran rename. No installed `dbt_packages/` staging model feeds f1001, so the lever did
  not fire and caused no harm — the h0009 convention-bleed victim was protected.
- **quickbooks003 — REGRESSED 14→11, but NOT from this lever.** The 24 `::timestamp` tokens were pre-existing model
  code read during exploration, not edits. The regression is orthogonal under-edit/variance on the unrelated
  `using_department`-removal task: the variant only unwrapped the `{% if var('using_department', True) %}` guards
  (keeping the `departments` CTE + `department_name` + joins) where @baseline did a SECOND patch fully DELETING the CTE,
  so 3 models (`int_quickbooks__expenses_union`, `int_quickbooks__sales_union`, `quickbooks__ap_ar_enhanced`) tripped
  "less columns than solution". The same-layer guard never got a chance to act; the bleed-suppression claim is
  therefore left untested while the canary still dropped (the smoke gate is outcome-based → NO-GO regardless of cause).

Net: 0/1 target flip + 1/2 load-bearing canaries regressed. The README-prose ceiling reasserts itself on a cast
exactly as it did on the restructure family (h0010/h0011/h0013/h0016).

**Transferable findings (for the ledger):**

1. **The README-prose ceiling holds even at the most-favorable case.** Even the NARROWEST, most-concrete
   in-place-cast prose — anchored to a concrete local artifact (the installed `asana_source` staging model) and
   prescribing a single-column mechanical `::timestamp` cast, the exact edit shape the loop calls its "one landed
   mechanism" — was INERT. The solver kept its raw-table `ALTER` / seed `+column_types` habit and never edited the
   model SQL. Anchoring + mechanical-substitution framing did NOT pull the edit to the model layer. The "tell the
   solver how to build it in prose" approach is exhausted for cast-shaped edits too, not just restructures.

2. **The asana002 "one win" is now IN DOUBT.** h0020's evidence — the solver's natural path leaves Got 2 even when
   explicitly told to cast the model column — strongly suggests h0009's asana002 FAIL→PASS flip did NOT come from a
   model-SQL `::timestamp` cast on `asana__task.sql`. It may have been run-to-run variance or a different edit
   (a raw-data shape change that happened to clear the mismatch). **FLAG:** the "a mechanical in-place edit is the one
   thing that lands" thesis — which h0023's type leg and other downstream bets lean on — needs the h0009 asana002
   artifact (its committed `apply_patch` payload / run-dir) RE-READ before it is trusted. If h0009's flip was not a
   model-SQL cast, the loop currently has ZERO confirmed README-lever flips.

**No follow-up filed.** Per the conclude stage's "do not reflexively file when the evidence says the lever family is
exhausted": both findings point at a meta-pattern (prose-driven model-layer edits are inert) and a foundational
audit need (re-read the h0009 asana002 artifact). These are strategy calls — surfaced here for the captain rather than
auto-filed as another doomed variant. No promote, no full run, no follow-up `h<NNNN>` created.

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

## Stage Report: smoke

- DONE: Smoke run completed on the 3-task frozen panel; `rk audit --policy strict` clean (tainted:0) + captured>0 BEFORE trusting score; focused `rk score` recorded with clean-audit attestation + run-dir
  Real run-dir `.../runs/ade-bench-h0020-...cast/1ec768e85f5d4579` (default dir; --runs-dir flag did not take — noted). Audit: clean=3/tainted=0/coverage_missing=0; subagent-trace-manifest captured=1 all 3. Score: stratified_pass_at_1=0.3333 (1/3). Per-task asana002 0, f1001 1, quickbooks003 0.
- DONE: Deep-dive vs @baseline (622bdedac572b479) — target flip check + load-bearing canary-hold check, artifact-level
  asana002: NO FLIP, Got 2→2; `due_at::timestamp` cast did NOT land on `asana__task.sql` (only `dbt_project.yml` +column_types patched; raw `asana.duckdb` altered instead) — outcome (a), lever inert at model layer. f1001: HELD 6/6 (own local src_*/stg_ naming, no Fivetran rename — gate effectively held). quickbooks003: REGRESSED 14→11 ("less columns than solution__" on 2 intermediate + 1 final) — caused by an under-edit on the unrelated using_department-removal task (unwrap-only vs @baseline full-delete), NOT the h0020 cast lever firing. Written into ## Smoke result + ## Behavioral analysis.
- DONE: Plain-language go/no-go + one-line reason + routing recommendation, led by the verdict
  NO-GO → conclude REJECTED; reason: target inert (cast never landed on model; still Got 2) + load-bearing canary regressed. In ## Verdict.

### Summary

Smoke is a clean-audited NO-GO: 0/1 target flip and 1/2 load-bearing canaries regressed. The artifact check is the load-bearing finding — the prescribed `due_at::timestamp` cast never landed on `models/asana__task.sql`; the solver re-edited the raw `asana.duckdb`/seed `+column_types` layer (the @baseline path) and stayed at `Got 2`. This both shows the cast lever is inert prose at the model layer and disproves the premise that h0009's asana002 flip came from this cast. quickbooks003 regressed for an orthogonal reason (an under-edit on the using_department task, not a lever bleed), so the bleed-suppression claim is left untested while the canary still dropped. Methodology aside: the `--runs-dir runs` flag did not take, so results landed in the default razorback runs dir; data valid, audit+score run there. Recommend conclude (REJECTED).

## Stage Report: conclude

- DONE: Write ## Verdict: REJECTED (cleanly falsified at smoke, no full run; 1/3)
  Replaced ## Verdict with full conclude verdict; mechanism (asana002 INERT cast never landed on asana__task.sql; f1001 HELD; quickbooks003 REGRESSED 14→11 from orthogonal under-edit not the lever); cites real run-dir .../1ec768e85f5d4579, clean strict audit (clean:3 tainted:0), stratified_pass_at_1=0.3333; --runs-dir methodology aside recorded.
- DONE: Record the TWO transferable findings
  (a) README-prose ceiling holds even at the most-favorable case — narrowest concrete in-place-cast prose was inert, solver kept raw-table ALTER habit, never edited model SQL. (b) asana002 "one win" now IN DOUBT — h0009's flip may not have been a model-SQL ::timestamp cast; FLAGGED that the "mechanical in-place edit lands" thesis (h0023 type leg + others) needs the h0009 asana002 artifact re-read before trusted.
- DONE: Do NOT auto-file a follow-up; defer the strategy call to the captain
  No follow-up h<NNNN> filed; both findings surfaced to the captain as a strategy/audit decision per the conclude "do not reflexively file when the family is exhausted" rule. No promote, no full run.

### Summary

Concluded h0020 as REJECTED — cleanly falsified at the smoke NO-GO gate (1/3, no full run). The Smoke result and Behavioral analysis (smoke ensign, commit 1fcfe12) were left intact; only the ## Verdict section was replaced with the full conclude verdict. Two transferable findings recorded: the README-prose ceiling holds even for the narrowest most-concrete in-place cast (the solver never edited the model SQL, keeping its raw-table ALTER habit), and h0009's asana002 "one win" is now in doubt — flagged that the "mechanical in-place edit lands" thesis needs the h0009 artifact re-read before downstream bets (h0023 type leg) trust it. No follow-up filed; strategy call deferred to the captain. FO handles verdict frontmatter + archival.
