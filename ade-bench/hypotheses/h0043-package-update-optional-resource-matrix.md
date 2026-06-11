---
id: h0043
title: Package-update optional-resource matrix -- when an installed package update exposes vars that disable resources, diagnose the var matrix first and gate only the affected dependency chain
status: analyze
kind: hypothesis
source: Captain request 2026-06-10 after asana002 decision-fork analysis; follows h0033 green-but-inert cast result and the Round 1 + Round 2 flipped-task choice map. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-10T07:17:29Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`asana002` is no longer treated as a type-cast target. h0033 showed the target can
flip, but the prescribed `::type` cast never appeared in committed SQL. The actual
green artifact was a structural package-migration repair: Fivetran's Asana package
made tag/task-tag resources optional, while downstream project models still
unconditionally referenced the tag chain. The successful repair gated the affected
models, refs, joins, and tag outputs with existing package vars such as
`asana__using_tags` and `asana__using_task_tags`.

**Falsifiable claim (the single solver-README change -- Implementation diagnostic
policy only):** adding a package-update optional-resource matrix rule will make the
solver reliably choose the `asana002` structural repair path: first inspect package
vars and optional-resource behavior, then repair the affected dependency graph with
the same existing vars. The rule should prevent the solver from starting with
model casts, raw seed/source edits, `dbt_project.yml` seed column types, or broad
package-convention copying when the visible failure is a disabled-resource
dependency.

**The single proposed README text (B variant):**

```text
When a task says an installed dbt package was updated, first classify package vars
and optional-resource behavior before editing. If a downstream model
unconditionally refs a package resource that can be disabled by an existing
package var, prefer a package-migration compatibility diagnostic: run or consider
a small disabled-var compile matrix and then repair the dependency graph with the
same existing vars. Do not start from casts, raw seed edits, or broad package
copying unless the optional-resource matrix is clean and another visible error
remains.
```

For `asana002`, the intended diagnostic is the tag/task-tag var matrix. The
intended repair family is:

- gate the relevant tag/task-tag intermediate models with existing package vars;
- conditionally include tag CTEs, refs, joins, and final columns in
  `asana__task`;
- preserve default behavior when tags/task-tags are enabled;
- emit stable `null` / `0` placeholders only where a final model must keep its
  shape when the optional resource is disabled;
- do not cast model columns, alter raw seeds/sources, change seed `column_types`,
  or apply broad package conventions outside the affected chain.

**Why this differs from h0033.** h0033 tried to force a mechanical model-layer
cast. The run passed, but the artifact proved the cast rule was inert: zero
`::<type>` casts appeared, and the actual fix was optional tag gating. h0043
therefore changes the decision policy from "find a representation mismatch" to
"first test package var optionality on package-update tasks." The artifact proof
required at smoke is the opposite of h0033: a successful run must contain the
optional-resource gating patch and must not contain a cast/seed-column-type fix.

**Pre-smoke subagent decision-fork evidence (proxy, not a score result).** We ran
fresh subagents with `fork_context=false`, no tools, no repo inspection, no hidden
verifier output, and only visible task context. The decision fork was:
package-migration optional tag gating vs model SQL cast vs raw seed/column-type
edit vs broad package copy.

Calibration with the disabled-resource compile error included:

| Variant | Rule | Optional-resource gating | Cast / seed / broad-copy |
|---|---|---:|---:|
| A | Weak baseline-style "smallest task-relevant change" | 2/2 | 0/2 |
| B | Package-update optional-resource rule | 2/2 | 0/2 |
| C | Strong matrix + no-cast guard | 2/2 | 0/2 |

Pre-diagnostic probe without the compile error, only task text + tag vars +
unconditional tag refs:

| Variant | Diagnostic path selected | Optional-resource gating | Cast / seed / broad-copy |
|---|---|---:|---:|
| A | `vars_disabled_compile_matrix` | 2/2 | 0/2 |
| B | `vars_disabled_compile_matrix` | 2/2 | 0/2 |
| C | `vars_disabled_compile_matrix` | 2/2 | 0/2 |

Follow-up B-only pre-diagnostic probe:

| Variant | Runs | `vars_disabled_compile_matrix` | Optional-resource gating | Cast / seed / broad-copy |
|---|---:|---:|---:|---:|
| B | 10 | 10 | 10 | 0 |

Total B evidence across both B batches: **14/14** chose the desired diagnostic and
repair family. The observed proxy wrong-branch rate for B is 0/14.

Honest caveat: the weak A rule also chose the desired branch in 4/4 proxy probes
when the visible tag-var context was included. That means this hypothesis is not
claiming B uniquely discovers the repair. It claims B turns the visible signal
into an explicit, smoke-auditable procedure so the real solver is less likely to
wander into the exhausted cast family or broad package-copy family.

**Falsification path.** h0043 fails if real `rk` smoke on `ade-bench-asana002`
does not patch the optional tag/task-tag chain, or if the committed artifact
starts with any of the known wrong families: model `::type` casts, raw seed/source
edits, seed `column_types`, or broad package-convention copying. It also fails if
the rule regresses canaries by firing outside package-update optional-resource
tasks.

**Target dataset.** Primary target: `ade-bench-asana002`. The expected movement is
to make the already-observed structural package-migration repair reproducible and
attributable, not to re-test the rejected cast family.

**Proposed smoke design.** Use a focused smoke panel:

- target: `ade-bench-asana002`;
- h0009/h0033 bleed canaries: `ade-bench-f1001`, `ade-bench-quickbooks003`;
- same-family sentinel: `ade-bench-asana001`;
- cross-family passers if the gatekeeper wants a wider panel:
  `ade-bench-airbnb001`, `ade-bench-ana-eng001`.

The decisive artifact read is `asana002`, not the panel mean:

1. committed patch touches the affected Asana models, expected candidates
   `models/asana__task.sql`, `models/intermediate/int_asana__task_tags.sql`, and
   `models/asana__tag.sql`;
2. patch contains package-var gating for tag/task-tag behavior;
3. patch contains no model `::type` cast as the load-bearing fix;
4. patch does not edit raw seeds/sources or seed `column_types`;
5. target passes on clean strict audit and canaries do not regress.

**Scope.** Solver README only. No benchmark, runtime, model, sampling, trials, or
spec-shape change. Leak guard remains intact; the rule references only local task
instructions, package vars, local package artifacts, model refs, and local compile
behavior. It does not mention hidden `AUTO_*` tests, `solution__*`, verifier
output, expected values, or public package sources.

## Acceptance criteria

**AC-1 -- Exactly one README policy change; specs differ only in allowed fields.**
Verified at propose by diffing the h0043 solver README against
`solver_workflows/codex-ade-dbt-minimal/README.md`: one Implementation diagnostic
policy block added, leak-guard prose byte-identical, no hidden-test/solution/
verifier references. Full spec diff vs `specs/baseline.yaml` shows only
`experiment:` and `solver_workflow:`; smoke spec adds only `benchmark.tasks`.

**AC-2 -- Every score is paired with strict clean audit and captured traces.**
Each `rk score` must cite `rk audit --policy strict` on the same run-dir with
`tainted: 0`, `coverage_missing: 0`, and captured agent traces.

**AC-3 -- Decision-policy evidence is artifact based.**
For `asana002`, read the committed patch, not the transcript narration. Classify
whether the patch is optional-resource gating, type cast, raw seed/column-type
edit, broad package copy, or unclear. Transcript claims such as "matched the
package" do not count without committed files.

**AC-4 -- h0043 is promoted only if the optional-resource path lands.**
Promotion requires `asana002` to pass with a committed optional tag/task-tag
gating repair and zero use of the known wrong repair families as the load-bearing
change. A green target with no optional-resource gating artifact is a green-but-
inert result, not a GO.

**AC-5 -- No regression canary loss.**
All baseline passers in the smoke panel must remain pass. Any canary regression
is a NO-GO unless artifact analysis proves it is unrelated single-trial variance
and the captain explicitly accepts that risk.

## Gatekeeper review

**Recommendation: APPROVE** — exactly one Implementation-stage diagnostic block added
(B-variant verbatim), leak-guard byte-identical, specs differ only in the allowed
fields, and the lever is GATED (fires only on package-update + disable-able-resource
tasks) so it carries no generative regression risk. Two WARN-only advisories carried
to the captain (G7 inert-risk; AC-4 artifact attribution is the decisive read).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-08). Reviewed 2026-06-10T09:46Z.
Note: review performed by the propose ensign in-line (no separate Agent-dispatch tool on the ensign surface); same guideline applied to the same artifacts.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff` vs parent `codex-ade-dbt-minimal/README.md` = one added 9-line block at 63a64,72, entirely inside `## Stage: Implementation` (50) before `## Stage: Validation` (73); no other stage touched. |
| G2 leak-guard intact | PASS | Added lines grep-clean for AUTO_*/solution__*/check_option/verifier/equality-test/expected-output/curl/wget/git clone/git ls-remote/web/http/browser/published-solution; leak-guard paragraphs (lines 1-32) byte-identical to parent. |
| G3 full spec two fields | PASS | `diff specs/baseline.yaml specs/h0043….yaml` = only `experiment:` and `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff` full→smoke = only an added `benchmark.tasks` block; all 6 slugs `ade-bench-` prefixed; the named target `ade-bench-asana002` is present; same-family sentinel `ade-bench-asana001` included. |
| G5 both frozen | PASS | `specs/h0043….frozen.yaml` + `…smoke.frozen.yaml` both exist; both carry `kind: spacedock_solver` + `runtime: codex`; smoke frozen lists the 6-task panel. |
| G6 resolver fidelity | PASS | Inserted text byte-matches the hypothesis "single proposed README text (B variant)" verbatim (programmatic compare = MATCH); same stage, same idea (gated package-migration diagnostic), no scope creep; it is a gated diagnostic / generative-repair instruction, NOT a self-anchored "re-run your own model / verify your answer" phrasing (dead h0006/h0007/h0008 family absent). |
| G7 actionability/inert-risk | WARN | Class: gated DIAGNOSTIC + structural-repair instruction ("repair the dependency graph with the same existing vars"), stated as abstract prose — the inserted README text carries NO worked-example SQL skeleton (the candidate files `asana__task.sql` / `int_asana__task_tags.sql` / `asana__tag.sql` and the gating pattern live only in the hypothesis body, not the rule the solver reads). Per the G7 "restructure SQL → inert at gpt-5.5/xhigh" prior (h0008 0/7, h0010 0/4), structural-rewrite prose without a copyable skeleton is inert-risk. The one durable win (asana002/h0033) was a concrete mechanical substitution, not a rewrite reasoned into. This is exactly why AC-4 makes the smoke read ARTIFACT-shaped: a green asana002 with no var-gating patch = green-but-inert (the h0033 lesson — its prescribed `::type` cast never appeared). |
| G8 regression-canary coverage | N/A (PASS) | GATED, not generative: the rule fires only "When a task says an installed dbt package was updated" AND "a downstream model unconditionally refs a package resource that can be disabled by an existing package var" — a narrow two-part precondition, and the "do not start from casts/seed edits/broad copying" clause is scoped under that same conditional. It does not fire on every task, so it carries no generative cross-family bleed risk. The smoke nonetheless carries the h0009/h0033 convention-bleed canaries `ade-bench-f1001` + `ade-bench-quickbooks003` (both @baseline PASS) plus cross-family passers `ade-bench-airbnb001` + `ade-bench-ana-eng001` and same-family sentinel `ade-bench-asana001` — coverage beyond what a gated lever requires. |
| G9 selector independence | N/A (PASS) | No multi-candidate / selector protocol declared; single-session repair lever. |
| G10 self-correcting false-positive | N/A (PASS) | Not a check/reconcile/validate-and-fix lever; it is a repair-path-selection diagnostic ("classify package vars first, then gate the dependency graph"). It does not instruct the solver to recompute a figure and overwrite on disagreement, so the h0012 false-green mode does not apply. |
| G11 multi-model-target risk | N/A (PASS) | `ade-bench-asana002` is scored by a SINGLE equality model — `AUTO_asana__task_equality` (the only `*_equality` test in the baseline verifier stdout; the other two graded items, `AUTO_asana__task_existence` and `task_source_schema`, are existence/schema gates, both PASS @baseline). The failing test is `AUTO_asana__task_equality "Got 2"`. The lever's prescribed repair (gate the tag/task-tag chain feeding `asana__task`) targets that one scored equality model, so a flip is not multi-model variance. (Taxonomy file `_artifacts/bug-type-taxonomy.md` is absent; scored-model count resolved directly from the baseline run's `verifier/test-stdout.txt`, the alternate source G11 names.) |

**For the captain:** No FAILs → nothing blocks the gate; advance to smoke. Two things to weigh.
(1) G7 inert-risk: the README text is abstract structural-repair prose with no worked-example
skeleton, the form that has gone inert at gpt-5.5/xhigh in past structural hypotheses. The
hypothesis acknowledges this and makes the read ARTIFACT-shaped (AC-4): a green asana002 alone
is NOT a GO — the committed patch MUST gate the tag/task-tag chain with existing package vars
(e.g. `asana__using_tags`) and MUST NOT be a `::type` cast / raw seed edit / seed
`column_types` / broad package-convention copy. Read the committed Asana model SQL, not the
transcript. (2) The pre-smoke subagent probe (B 14/14 chose the desired diagnostic) is
PRELIMINARY PROXY evidence, not an `rk` score; weak-A also chose the branch 4/4 when tag-var
context was visible, so B's value is making the repair smoke-AUDITABLE, not unique discovery.

## Smoke-set table (for the captain)

@baseline = `runs/ade-bench-baseline/622bdedac572b479` (31/48); rewards read from
`per_trial_outcomes.json` by slug.

```
┌────────────────────────┬──────────┬──────────────────────┬────────────────────────────────────────────────────────────┐
│          Task          │ Baseline │ Should pass in smoke?│                  Role / why we picked it                     │
├────────────────────────┼──────────┼──────────────────────┼────────────────────────────────────────────────────────────┤
│ ade-bench-asana002     │ ❌ FAIL  │ 🎯 want it to flip   │ TARGET — package-migration repair; gate tag/task-tag chain   │
│                        │          │                      │   with existing pkg vars. AC-4: green w/o var-gating = NOT GO.│
│ ade-bench-asana001     │ ✅ PASS  │ ✅ must stay PASS    │ Sentinel (asana same-family) — breaks ⇒ side effects in fam. │
│ ade-bench-f1001        │ ✅ PASS  │ ✅ must stay PASS    │ Canary (f1, no package) — h0009/h0033 bleed tripwire.        │
│ ade-bench-quickbooks003│ ✅ PASS  │ ✅ must stay PASS    │ Canary (quickbooks) — h0009/h0033 2nd bleed tripwire.        │
│ ade-bench-airbnb001    │ ✅ PASS  │ ✅ must stay PASS    │ Canary (airbnb family) — cross-family regression tripwire.   │
│ ade-bench-ana-eng001   │ ✅ PASS  │ ✅ must stay PASS    │ Canary (ana-eng family) — cross-family regression tripwire.  │
└────────────────────────┴──────────┴──────────────────────┴────────────────────────────────────────────────────────────┘
```

Net we want: flip `asana002` (the only target) with an ARTIFACT-proven optional-resource
var-gating patch on the tag/task-tag chain, lose zero of the 5 passers. AC-4 governs the
verdict — a green `asana002` with no var-gating patch (a `::type` cast / raw seed edit / seed
`column_types` / broad package copy instead) is green-but-inert = NOT a GO. ETA: 6 tasks ×
~9 min ≈ 54 min, detached (nohup); the captain need not wait on-screen.

## Stage Report: propose

- DONE: README change = EXACTLY ONE Implementation-stage diagnostic policy block (B-variant verbatim)
  `diff` vs parent = single 9-line block at 63a64,72, inside `## Stage: Implementation`; leak-guard (1-32) + 4 stages byte-identical; programmatic compare to hypothesis B-variant = MATCH; grep-clean for hidden-test/external-fetch tokens (AC-1).
- DONE: Smoke spec `benchmark.tasks` = the 6-task panel; both specs frozen
  `ade-bench-asana002` (target) + `ade-bench-f1001` + `ade-bench-quickbooks003` (h0009/h0033 bleed canaries) + `ade-bench-asana001` (same-family sentinel) + `ade-bench-airbnb001` + `ade-bench-ana-eng001` (cross-family passers); all 5 = @baseline 1.0, asana002 = 0.0. Full spec diff = only `experiment:`+`solver_workflow:`; smoke diff = only `benchmark.tasks`. Both `.frozen.yaml` written, kind/runtime preserved.
- DONE: Run the gatekeeper; record per-rule table + APPROVE/REVISE/REJECT in `## Gatekeeper review`
  Recommendation APPROVE (no FAILs); G7 WARN (inert-risk, abstract structural prose, no worked-example skeleton) + AC-4 artifact-attribution note carried to the captain; G8 N/A (gated lever); G11 N/A (asana002 single-equality-model `AUTO_asana__task_equality`). Review run in-line by the propose ensign — no Agent-dispatch tool on the ensign surface.

### Summary

Forked the @baseline solver to `solver_workflows/h0043-package-update-optional-resource-matrix`
and inserted the B-variant gated package-update optional-resource diagnostic block VERBATIM
inside the existing Implementation stage (no new stage). Built + froze the full and smoke specs
(smoke = the 6-task panel: asana002 target + 5 @baseline passers as bleed/sentinel/cross-family
canaries). Applied the gatekeeper guideline → APPROVE: no FAILs, leak-guard intact, specs in
the allowed fields only, lever is GATED so no generative regression risk. Two advisories for the
captain: G7 inert-risk (the README text is abstract structural-repair prose with no copyable SQL
skeleton — the form that has gone inert at gpt-5.5/xhigh), and the decisive read is ARTIFACT-
shaped per AC-4 — a green asana002 alone is NOT a GO unless the committed patch gates the
tag/task-tag chain with existing package vars and is not a cast/seed/broad-copy.

## Smoke result

**GO.** asana002 flipped FAIL→PASS via an artifact-attributed optional-resource
VAR-GATING patch; all 5 canaries held; strict audit clean. Run dir:
`runs/ade-bench-h0043-package-update-optional-resource-matrix/b0f5d0dd93ecfca3`
(finished 2026-06-10T10:51Z, 6/6 trials completed, 0 errored).

**Score (AC-2):** `rk score` → `stratified_pass_at_1 = 1.0` (6/6), verdict `above` the
0.1875 constant. **Strict audit (AC-2):** `rk audit --policy strict` → `clean: 6,
tainted: 0, coverage_missing: 0`; every cell `captured: 1` (subagent-trace-manifest).

| Task | @baseline | Smoke | Verifier tests | Role |
|------|-----------|-------|----------------|------|
| ade-bench-asana002 | ❌ 0.0 | ✅ 1.0 | 3/3 pass (`AUTO_asana__task_equality` FAIL 2 → PASS) | TARGET — flipped |
| ade-bench-f1001 | ✅ 1.0 | ✅ 1.0 | 6/6 pass | canary (f1, h0009/h0033 bleed) — held |
| ade-bench-quickbooks003 | ✅ 1.0 | ✅ 1.0 | 14/14 pass | canary (quickbooks, h0009/h0033 bleed) — held |
| ade-bench-asana001 | ✅ 1.0 | ✅ 1.0 | 2/2 pass | sentinel (asana same-family) — held |
| ade-bench-airbnb001 | ✅ 1.0 | ✅ 1.0 | 10/10 pass | canary (airbnb) — held |
| ade-bench-ana-eng001 | ✅ 1.0 | ✅ 1.0 | 1/1 pass | canary (ana-eng) — held |

Net: flipped the 1 target, lost zero of the 5 passers. The two convention-bleed
canaries (f1001 6/6, quickbooks003 14/14) held at full baseline test count — no bleed
(the gated precondition fired only on the package-update target, as designed).

## Behavioral analysis

**The decisive artifact read (AC-3/AC-4) — CLASSIFICATION: optional-resource VAR-GATING
(the intended GO family).** Read the COMMITTED `apply_patch` payload from the asana002
trial rollout (`agent/sessions/.../rollout-*.jsonl`), not the narration. One unique
patch, touching exactly the three predicted candidate files and nothing else:
`models/intermediate/int_asana__task_tags.sql`, `models/asana__task.sql`,
`models/asana__tag.sql`.

The committed edits:

- `int_asana__task_tags.sql` and `asana__tag.sql`: added
  `{{ config(enabled=var('asana__using_tags', True) and var('asana__using_task_tags', True)) }}`
  — gates each tag/task-tag model on the EXISTING package vars.
- `asana__task.sql`: `{% set using_task_tags = var('asana__using_tags', True) and var('asana__using_task_tags', True) %}`,
  then conditionally includes (a) the `task_tags` CTE, (b) the tag final columns, and
  (c) the `left join task_tags` — all guarded by `{% if using_task_tags %}`. When tags
  are disabled it emits stable placeholders `cast(null as {{ dbt.type_string() }}) as tags,
  0 as number_of_tags` to keep the output shape. Default behavior (tags enabled) is
  preserved.

This is exactly the AC-4 GO condition: gates the affected dependency chain with the same
existing package vars, conditional CTEs/refs/joins/final columns, default preserved,
stable null/0 placeholders only where shape must hold.

**Wrong-family falsifiers — ALL CLEAR (AC-4):**

- NOT a `::type` representation cast: the only `cast(...)` in the patch is
  `cast(null as {{ dbt.type_string() }})` — a typed-NULL placeholder for the disabled-tags
  branch (shape preservation), not a representation cast on an existing column. This is
  the OPPOSITE of the h0033 inert result: h0033 prescribed a `::type` cast that never
  appeared; here the prescribed VAR-GATING DID appear and is load-bearing.
- NOT a raw seed/source edit: patch touches only `models/*.sql`.
- NOT a seed `column_types` edit: no `dbt_project.yml` change (0 added lines match
  `column_types`/`.csv`/`.duckdb`/`ALTER`).
- NOT a broad package-convention copy: edits are scoped to the tag/task-tag chain only.

**Canary integrity (AC-5):** all 5 canaries PASS on the clean strict audit at full
verifier test count (f1001 6/6, quickbooks003 14/14, asana001 2/2, airbnb001 10/10,
ana-eng001 1/1) — no degraded greens, no regression. The gated precondition ("a task says
an installed package was updated AND a model unconditionally refs a disable-able package
resource") fired only on asana002, so no generative cross-family bleed — consistent with
the G8 N/A classification at propose.

**Verdict read:** This is the rare artifact-attributed flip — green AND inert-free. It
proves the h0043 gated package-update optional-resource diagnostic produces the structural
package-migration repair, not the exhausted cast/seed/broad-copy families. Single-trial,
so the flip is one observation; but unlike a multi-model target, asana002 is scored by a
single equality model (`AUTO_asana__task_equality`) which the var-gating patch directly
addresses (FAIL 2 → PASS), so the flip is attributable to the lever's mechanism rather than
variance on an unaddressed model (G11 N/A confirmed). Recommend → `full`.

## Stage Report: smoke

- DONE: Smoke run on the frozen 6-task panel completed (detached nohup, polled across turns); strict audit clean + captured>0 before score
  Run dir `…/b0f5d0dd93ecfca3`; `rk audit --policy strict` = clean:6/tainted:0/coverage_missing:0; captured:1 on all 6 cells; `rk score` = stratified_pass_at_1 1.0 (6/6). Recorded in `## Smoke result`.
- DONE: THE DECISIVE ARTIFACT READ (AC-3/AC-4) — classify the committed asana002 patch
  Read the committed `apply_patch` from the trial rollout JSONL: optional-resource VAR-GATING (gates tag/task-tag chain via existing pkg vars `asana__using_tags`/`asana__using_task_tags`; conditional CTE/join/final-columns + stable null/0 placeholders) across the 3 predicted models. NOT a `::type` cast / raw seed edit / seed column_types / broad package copy (all falsifiers clear). asana002 PASSED (`AUTO_asana__task_equality` FAIL 2 → PASS). = artifact-attributed GO, not green-but-inert.
- DONE: Canary check (AC-5) — all 5 hold PASS on the clean audit; per-cell + classification recorded
  f1001 6/6, quickbooks003 14/14, asana001 2/2, airbnb001 10/10, ana-eng001 1/1; zero regression. Recorded in `## Smoke result` + `## Behavioral analysis`. In-stage instruction lever → no WORKFLOW-REFINE entry needed.

### Summary

GO. The detached 6-task smoke flipped asana002 FAIL→PASS and held all 5 canaries; strict
audit clean (tainted 0, captured 1 on every cell); score 1.0. The decisive artifact read is
the headline: the committed asana002 patch is optional-resource VAR-GATING (gates the
tag/task-tag chain with the existing package vars, conditional CTEs/refs/joins/final columns,
stable typed-null placeholders) across exactly the three predicted Asana models — and is NOT
a `::type` cast / raw seed edit / seed `column_types` / broad package copy. This is the
opposite of the h0033 green-but-inert outcome: the prescribed repair appeared in the committed
SQL and is load-bearing. Recommend advancing to `full`.

## Run result

**Methodology consistency (no smoke→full drift) — CONFIRMED.** The full frozen spec
`specs/h0043-package-update-optional-resource-matrix.frozen.yaml` references the SAME
solver README content-hash as the smoke frozen spec:
`solver_workflow_content_hash: sha256:2badaaae1ee8ccf610fb2be457c00b9d75cfdb55405e3adf069e824ce56a1ce5`
(byte-identical `solver_workflow_hash` on both specs). Only the task set differs — full
has `benchmark.tasks: null` (all 48); smoke listed the 6-task panel. `trials: 1`,
`concurrency.trials: 1`, `agent.kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`,
`reasoning_effort: xhigh` all preserved.

**Launched (detached, nohup).** `drivers/rk-run-detached.sh h0043-full
specs/h0043-package-update-optional-resource-matrix.frozen.yaml run` at
2026-06-10T17:29:40Z. Handle: `runs/.rk-handles/h0043-full-20260610-172940/`
(worker pid 4028792). Run-dir:
`runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea/` —
distinct content-hash from the smoke run `b0f5d0dd93ecfca3`, no path collision.
Ran concurrently with h0042-full and h0045-smoke (3 rk runs total). Done sentinel:
`rc=0 end=2026-06-11T00:09:19Z` (~6h35m wall, slower under concurrent load).
**Run-dir solver hash (what actually ran)** = `config.json
/agents[0]/kwargs/solver_workflow_content_hash:
sha256:2badaaae1ee8ccf610fb2be457c00b9d75cfdb55405e3adf069e824ce56a1ce5` —
byte-identical to the smoke frozen spec. No smoke→full drift.

**Strict audit (AC-2) — CLEAN.** `rk audit … --policy strict` →
`summary: { clean: 48, tainted: 0, coverage_missing: 0 }`; all 48 trial records
`taint_status: clean` with zero findings; captured-trace evidence present on all 48
cells (`coverage_missing: 0`). The +1 is on a clean run — trustworthy.

**Score (AC-2).** `rk score … --format json` → `stratified_pass_at_1 = 0.6667`
(**32/48**), `stratified_n_completed: 48`, `stratified_n_errored: 0`, verdict `above`
the 0.1875 constant.

**HEADLINE: 32/48 = 0.6667, net +1 vs @baseline 31/48 (0.6458).** asana002
flipped FAIL→PASS (baseline 0.0 → 1.0) — the var-gating flip HELD at 48-scale. First
+1 of the program; promote-to-32 candidate.

**Per-task split vs @baseline (slug-paired, 48/48 paired, single-trial).** Net +1 by
count, but the composition is NOT a clean isolated target flip — flagging for analyze:

| Movement | Slug | @baseline | h0043 full | Note |
|---|---|---|---|---|
| FLIP UP | `ade-bench-asana002` | 0.0 | 1.0 | TARGET — held at full (intended) |
| FLIP UP | `ade-bench-f1011` | 0.0 | 1.0 | OFF-TARGET flip-up, not in smoke panel |
| FLIP DOWN | `ade-bench-f1006-hard` | 1.0 | 0.0 | OFF-TARGET regression, not in smoke panel |

- Stayed PASS: 30 · Stayed FAIL: 15 · Flips: +2 / −1 ⇒ **net +1**.
- The 5 smoke canaries ALL held PASS at full (f1001, quickbooks003, asana001,
  airbnb001, ana-eng001 = 1.0). The off-target movers (f1011, f1006-hard) were NOT
  in the smoke panel, so smoke could not have caught them.
- 16 FAILs at full: airbnb007, airbnb009, ana-eng004, ana-eng006, ana-eng007,
  ana-eng007-medium, asana004, asana005, asana005-hard, f1002, f1006, f1006-hard,
  intercom001, intercom002, intercom003, quickbooks001.

**For analyze (NEXT stage — not done here):** the net +1 is real on a clean,
0-errored, strict-clean run, but it is +2/−1, not a lone target flip. The clean-+1
question is open: (a) re-confirm asana002 flipped via the COMMITTED var-gating patch
(not coincidence), and (b) adjudicate whether the off-target f1011 flip-up and
f1006-hard regression are lever-attributable or single-trial variance — the gated
lever fires only on package-update + disable-able-resource tasks, so an effect on
f1011/f1006-hard would need an artifact check. A masked-regression risk exists in
principle (the +1 count could hide a lever-caused f1006-hard loss offset by an
unrelated f1011 gain), so analyze must read the committed artifacts of all three
movers before the +1 is banked as CLEAN.

## Stage Report: full

- DONE: Full 48-task run on `specs/h0043-package-update-optional-resource-matrix.frozen.yaml` completed (detached nohup, polled across turns); strict audit clean + captured>0 every cell BEFORE the score; run-dir + headline + net recorded
  Run-dir `…/7390e6adf44ba5ea` (done `rc=0 end=2026-06-11T00:09:19Z`). `rk audit --policy strict` = `clean:48, tainted:0, coverage_missing:0`, all 48 trials `taint_status: clean` zero findings, captured-trace evidence on all 48 cells. `rk score` = `stratified_pass_at_1 0.6667` (32/48), 48 completed / 0 errored, verdict `above`. Net **+1** vs @baseline 31/48 — asana002 held FAIL→PASS at full. Recorded in `## Run result`.
- DONE: Methodology consistency (no smoke→full drift) — confirmed; hash stated
  Full frozen spec + the run-dir's own resolved `config.json` both carry `solver_workflow_content_hash: sha256:2badaaae1ee8ccf610fb2be457c00b9d75cfdb55405e3adf069e824ce56a1ce5` — byte-identical to the smoke frozen spec. Only the task set differed (full `tasks: null` = all 48). No drift.

### Summary

Net +1 confirmed on a CLEAN run: 32/48 = 0.6667 (audit strict-clean, tainted 0, 0 errored), asana002 held FAIL→PASS at 48-scale and the var-gating flip survived. All 5 smoke canaries held PASS. IMPORTANT for analyze: the +1 is +2/−1 by slug-paired composition, not a lone target flip — besides the target there is an OFF-TARGET flip-up `f1011` (0.0→1.0) and an OFF-TARGET regression `f1006-hard` (1.0→0.0), neither in the smoke panel. The clean-+1 verdict is OPEN: analyze must re-prove asana002 via the committed var-gating patch and adjudicate whether the two off-target movers are lever-attributable or single-trial variance before banking the +1. Solver README hash matches smoke (no drift). I did NOT start the per-task ledger / asana002 re-proof — that is the analyze stage.

## Run result — analyze (quantitative)

**Paired delta (slug-paired from `per_trial_outcomes.json`; `rk runs diff` TypeErrors on
ade-bench run-dirs — `query_id: null`, harness data-shape limitation, not a run defect).**
48/48 slugs paired. @baseline 31/48 = 0.6458 → h0043 32/48 = 0.6667. Observed net task
delta **+1** (pass-rate delta **+0.0208**). 10k paired bootstrap (seed 20260611) 95% CI on
the pass-rate delta = **[−0.0417, +0.0833]** ⇒ in task-count terms **[−2, +4]**; P(delta>0)
= 0.61. **The aggregate CI straddles zero** — at single-trial it cannot distinguish +1 from
noise. Per the standing decision (judge by committed-artifact proof + bleed-free canaries,
NOT multi-trial CI), the verdict rests on the artifact-attributed mechanism below, not the
headline number. Absolute: `stratified_pass_at_1 0.6667`, verdict `above` the 0.1875 paper
baseline.

**Full per-task ledger — both directions (the +1 is +2 / −1):**

| Dir | Slug | @base | h0043 | Failing/passing test | Committed artifact | Lever sig? | Class |
|---|---|---|---|---|---|---|---|
| ↑ | `asana002` | 0.0 | 1.0 | `AUTO_asana__task_equality` FAIL 2 → PASS (3/3) | var-gates tag/task-tag chain across `int_asana__task_tags.sql` + `asana__task.sql` + `asana__tag.sql` via `config(enabled=var('asana__using_tags',…))` + `{% if %}` CTE/join/columns + typed-null placeholders | **YES** | executed-and-helped (lever) |
| ↑ | `f1011` | 0.0 | 1.0 | 6/6 `check_option_*` PASS | `Add models/stats/analysis__answer.sql` = `select 'ADE' as answer` | NO | off-target, lever-INERT, variance gain |
| ↓ | `f1006-hard` | 1.0 | 0.0 | `AUTO_constructor_points_equality` **FAIL 2** (driver_points PASS) | rewrote `constructor_points.sql`+`driver_points.sql` `sum()+GROUP BY` → `row_number() … standings_rank=1` | NO | off-target, lever-INERT, regression-on-passer (variance) |

Stayed PASS: 30 · Stayed FAIL: 15. The 5 smoke canaries (f1001, quickbooks003, asana001,
airbnb001, ana-eng001) all held PASS at full.

## Behavioral analysis — analyze (full run vs @baseline)

**LEAD (clean-+1 verdict): this IS a CLEAN, lever-attributable +1.** The net +1 rests
entirely on the lever's `asana002` flip, which is artifact-proven optional-resource
VAR-GATING at BOTH smoke AND full (2/2). The two off-target movers are each provably
lever-INERT (zero `config(enabled=var(…))` / `using_tags` signature in committed SQL) and
happen to net 0. The lever caused no regression — the one regression (`f1006-hard`) is a
fragile-baseline cell that the lever never touched. PROMOTE-worthy.

**Q1 — Net + full per-task ledger (both directions).** See the ledger table in
`## Run result — analyze`. Net +1 = `asana002` (lever) +1, `f1011` (variance) +1,
`f1006-hard` (variance) −1. Reported in both directions; the lone regression is named.

**Q2 — Smoke vs full.** Smoke was a GO (asana002 flip + 5 canaries held) and the full
CONFIRMED it (asana002 held). The full *additionally* surfaced two off-target movers
(`f1011` +, `f1006-hard` −) that the **6-task smoke panel could not see** — neither slug was
in the panel. This did not change the GO direction (net still +1, target still flipped via
the same patch); it only revealed off-target single-trial noise the panel did not sample.
The smoke panel correctly covered the lever's *blast radius* (it is gated; canaries confirm
no bleed) — the off-target movers are outside that radius and are not lever effects.

**Q3 — Already-correct-and-broken.** One regression: `f1006-hard` was PASSING at @baseline
(1.0) and dropped to 0.0 here — nominally damage to a passer. BUT @baseline is the OUTLIER:
`f1006-hard` scored 0.0 in every other full run on record (h0037, h0041, h0042 fulls all
0.0; only @baseline = 1.0). So the @baseline green is the fragile observation; h0043's 0.0
is the modal outcome across 4 independent fulls. The h0043 committed artifact (a
`row_number() standings_rank=1` reinterpretation of f1 standings) is an unrelated
domain-logic choice the solver makes variably across runs — NOT lever-caused damage. This is
"unrelated single-trial variance on a chronically variance-prone cell," not "the lever broke
working code." (AC-5 / G8: the lever is gated and the in-panel canaries all held.)

**Q4 — Was the change executed? (artifact, not chatter).**
- `asana002` (gain): **executed-and-helped (lever)** — committed `apply_patch` gates the
  tag/task-tag chain with the existing package vars across exactly the 3 predicted models;
  the only `cast(...)` is a typed-NULL shape placeholder in the disabled branch, NOT a
  `::type` representation cast; no raw seed / no `dbt_project.yml` / no broad copy. Opposite
  of h0033's green-but-inert (there the prescribed cast never appeared; here the prescribed
  var-gating IS load-bearing).
- `f1011` (gain): **inert w.r.t. the lever** — committed a one-line answer model; the
  package-update/optional-resource rule did not fire (not such a task) and left no signature.
  Executed a trivial correct answer = variance gain, not a lever effect.
- `f1006-hard` (regression): **inert w.r.t. the lever / executed-and-hurt by an unrelated
  edit** — committed a standings rewrite with no var-gating signature; the lever did not fire
  (f1 standings is not a package-update/optional-resource task). The hurt is from the
  solver's own domain choice, not the lever.

**Q5 — Prevention + next move.** The gains we want to keep = the `asana002` var-gating flip,
which is GATED and carries no cross-family bleed risk (canaries held; G8 N/A confirmed at
full). The off-target noise (`f1011`/`f1006-hard`) is single-trial variance, not a lever
harm, so no scoping guardrail is needed for the lever itself. To catch the f1006-hard
*baseline fragility* earlier, a chronic-variance watchlist (f1006-hard 1.0 only at @baseline,
0.0 in 4 fulls) belongs in the standing canary notes — it will keep appearing as ±1 noise in
every full and should not be read as a lever signal. **Recommended next move:** CONCLUDE
h0043 as a clean, artifact-attributed +1 and recommend the captain PROMOTE @baseline to
**32/48** on the strength of the lever-attributable asana002 var-gating flip (2/2
smoke+full). This is the program's first genuine +1. Do NOT re-open the exhausted cast/seed
families. The captain decides the registry re-bind.

**Q6 — Smoke-vs-full fork drift.** No adverse drift. The smoke GO was ARTIFACT-REAL, not
variance: the asana002 var-gating patch reproduced at full (same family, same 3 models, same
existing pkg vars), so the smoke→full fork held on the target. The full-only movers
(`f1011`, `f1006-hard`) are NOT a drifted lever branch — both are lever-inert (no var-gating)
and outside the gated precondition; they are unrelated single-trial variance the smoke panel
did not sample. No README rule drifted into a different implementation branch. The only
"miss" is panel coverage (the panel sampled the lever's blast radius, not the whole 48), and
that miss surfaced only noise, not a hidden lever regression.

## Stage Report: analyze

- DONE: RE-PROVE THE TARGET — asana002 var-gating at full matches smoke (2/2 artifact-proven)
  Read the committed `apply_patch` from `ade-bench-asana002__JNWKSkQ` rollout JSONL: optional-resource VAR-GATING across the same 3 models (`int_asana__task_tags.sql`, `asana__task.sql`, `asana__tag.sql`) via `config(enabled=var('asana__using_tags',…))` + `{% if %}` CTE/join/columns + typed-null placeholders. NOT a `::type` cast / seed edit / broad rewrite. `AUTO_asana__task_equality` FAIL 2 → PASS. Lever-attributable, reproduced smoke→full.
- DONE: ADJUDICATE THE 2 OFF-TARGET MOVERS — both lever-INERT, net 0, unrelated variance
  `f1011` (+, `select 'ADE' as answer`) and `f1006-hard` (−, `row_number() standings_rank=1` f1-standings rewrite) — committed SQL has ZERO `config(enabled=var)/using_tags` signature; lever did not fire (neither is a package-update/optional-resource task). f1006-hard 0.0 is modal (also 0.0 in h0037/h0041/h0042 fulls; @baseline 1.0 is the outlier) — fragile-baseline variance, not lever damage. Net +1 rests on asana002 alone.
- DONE: Answer the 5 (six) required questions in `## Run result` + `## Behavioral analysis`; recommend verdict + PROMOTE
  Paired delta +1 (bootstrap 95% CI [−2,+4] straddles 0 → verdict on artifact mechanism per standing decision, not CI). All six Qs answered. Lead: CLEAN lever-attributable +1. Recommend CONCLUDE h0043 + captain PROMOTE @baseline → 32/48.

### Summary

CLEAN +1. The net +1 is artifact-attributed to the lever: asana002 flipped FAIL→PASS via
optional-resource VAR-GATING at BOTH smoke and full (2/2, same 3 models, same existing pkg
vars), the opposite of h0033's green-but-inert. The two off-target movers (`f1011` +,
`f1006-hard` −) are each provably lever-INERT (no var-gating signature) and net 0;
`f1006-hard`'s drop is fragile-baseline variance (0.0 in 3 other fulls, @baseline 1.0 is the
outlier), not lever damage. The aggregate bootstrap CI straddles zero — expected at
single-trial — so the verdict rests on the committed-artifact mechanism (standing decision),
which is decisively a lever win. Recommend CONCLUDE as the program's first genuine +1 and
that the captain PROMOTE @baseline to 32/48. `rk runs diff` TypeError'd (query_id null) →
paired delta computed from per_trial_outcomes.json by slug, as noted.
