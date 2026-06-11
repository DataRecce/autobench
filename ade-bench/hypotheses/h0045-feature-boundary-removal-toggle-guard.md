---
id: h0045
title: Feature-boundary removal/toggle guard -- keep remove/disable feature requests at the project-local feature boundary, not broad domain rewrites
status: full
kind: hypothesis
source: Captain request 2026-06-10 after generalized quickbooks002/quickbooks004 decision-fork probe. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-10T16:40:51Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Some flipped passers are not failing because the model cannot edit SQL. They are
failing because a local feature-boundary task leaves two defensible branches:

1. Keep the change at the feature boundary: remove or gate only the config,
   project-local refs, joins, CTEs, select outputs, and docs whose only purpose
   is the removed/disabled feature.
2. Treat the instruction as permission for a broad cleanup: unwrap guards so the
   feature remains active, leave null placeholders, delete unrelated base
   attributes, or rewrite a wide domain model that was not asked for.

**Falsifiable claim (the single solver-README change -- Implementation policy
only):** adding a general feature-boundary removal/toggle guard will increase
the chance that the real solver takes branch 1 on feature-removal and
feature-disable tasks, while staying inert on unrelated tasks. The expected win
is stabilization: both named targets are `@baseline` passers that have flipped
under broader workflow changes, so a successful smoke should keep them PASS with
artifact-proven narrow feature-boundary edits and no broad refactor.

**The single proposed README text:**

```text
When a task asks to remove, disable, or add a switch for a project-local feature,
keep the edit at the feature boundary. Do not turn a feature-boundary request
into a broad domain rewrite.

For removal requests, remove the config/variable and project-local logic whose
only purpose is that feature: feature-specific refs, CTEs, joins, select-list
outputs, and schema docs. Do not simply unwrap old conditional guards so the
feature stays active. Do not leave placeholder outputs whose only purpose was
the removed feature. Do not edit installed packages or dependency code unless
the task explicitly asks. Preserve ordinary raw/source attributes that are part
of the base entity or transaction and do not depend on the removed feature.

For toggle or disable requests, add the requested flag/default and guard only
the derived outputs and docs controlled by that feature. Preserve the enabled
path's existing formulas and behavior. Adjust unions, column alignment,
grouping, or downstream projections only as needed because disabled outputs
changed shape. Do not recompute unrelated formulas, signs, grains, joins, or
relationship semantics unless the task explicitly asks.

Before finalizing, search project-local files for remaining references to the
removed or disabled feature. Verify the default/disabled path has the intended
refs and outputs absent, and when an enabled path exists, verify it still
compiles or preserves the prior output shape.
```

This README wording is intentionally generic. It does not name QuickBooks, any
dataset slug, any concrete variable, any concrete column, or a task-specific
answer.

## Pre-smoke Decision-Fork Probe

Method: use the local subagent decision-fork probe pattern from
`_artifacts/subagent-decision-fork-probe-method.md`: fresh subagents, no tools,
`fork_context=false`, solver-visible task/model context only, no previous
pass/fail outcome, no solution/verifier facts, and a classifier over the branch
chosen in the proposed patch plan. These counts are proxy evidence for branch
tendency, not real `rk` pass-rate estimates.

Fork being tested:

- Removal case: complete project-local feature delete vs guard-unwrapping,
  dependency/package edit, or placeholder/null-output preservation.
- Toggle case: narrow feature-derived output hiding vs broad domain refactor.

Prompt context included:

- Task instruction text.
- Relevant project vars/config.
- Project-local models and docs containing the feature references.
- Enough surrounding model shape to classify whether the proposed plan is
  feature-boundary scoped or a broad rewrite.

Weak-control calibration before the generalized rule:

| Case | Control A rule | Desired branch | Undesired branch | Other |
|---|---|---:|---:|---:|
| Feature removal | Baseline-style smallest local repair | 0/3 | 3/3 | 0/3 |
| Feature toggle | Baseline-style smallest local repair | 3/3 | 0/3 | 0/3 |

Task-specific B calibration before the captain rejected dataset-specific README
wording:

| Case | Runs | Desired branch | Undesired branch | Other |
|---|---:|---:|---:|---:|
| Feature removal | 13 | 13 | 0 | 0 |
| Feature toggle | 13 | 13 | 0 | 0 |

Final generalized B wording, exactly matching the README text above:

| Case | Runs | Desired branch | Undesired branch | Other |
|---|---:|---:|---:|---:|
| Feature removal | 10 | 10 | 0 | 0 |
| Feature toggle | 10 | 10 | 0 | 0 |
| Combined | 20 | 20 | 0 | 0 |

Expected committed-artifact signature:

1. Removal targets remove the config/variable and project-local feature-only
   refs, CTEs, joins, select outputs, and docs.
2. Removal targets do not edit installed dependencies and do not keep the removed
   feature alive by unwrapping old guards or adding placeholder outputs.
3. Toggle targets add the requested flag/default and hide only derived outputs
   controlled by that feature.
4. Toggle targets preserve the enabled path's existing formulas and avoid broad
   domain/model rewrites.
5. Unrelated canaries do not show convention bleed or task-irrelevant edits.

Interpretation: the generalized B rule has strong proxy support on the local
decision fork (20/20 desired across the two feature-boundary cases). It does not
prove pass rate. Smoke must validate committed artifacts and canaries.

## Target Datasets

Primary stabilization targets:

- `ade-bench-quickbooks002`
- `ade-bench-quickbooks004`

Regression canaries:

- `ade-bench-quickbooks003` -- same-package/same-layer quickbooks canary.
- `ade-bench-f1001` -- convention-bleed canary.
- `ade-bench-airbnb001`
- `ade-bench-ana-eng001`
- `ade-bench-asana001`

All seven smoke tasks are `@baseline` passers in
`runs/ade-bench-baseline/622bdedac572b479/per_trial_outcomes.json`.

## Proposed Smoke Design

Use a focused seven-task smoke panel:

1. `ade-bench-quickbooks002`
2. `ade-bench-quickbooks004`
3. `ade-bench-quickbooks003`
4. `ade-bench-f1001`
5. `ade-bench-airbnb001`
6. `ade-bench-ana-eng001`
7. `ade-bench-asana001`

GO criteria:

1. Strict audit clean, captured traces present, and all seven tasks PASS.
2. The two targets show the expected feature-boundary artifact shape.
3. Same-family quickbooks canary and cross-family canaries do not regress.
4. No committed patch uses a task-specific hard-coded dataset workaround.

NO-GO criteria:

1. Either target regresses.
2. Any canary regresses.
3. A target passes but the committed artifact is a broad domain rewrite rather
   than the feature-boundary edit.
4. The solver README change appears inert: the task behavior is unchanged from a
   known bad branch despite the rule being applicable.

## Acceptance Criteria

**AC-1 -- Exactly one README policy change; specs differ only in allowed fields.**
README diff vs `solver_workflows/codex-ade-dbt-minimal/README.md` must be one
Implementation-stage policy block. Full spec diff vs `specs/baseline.yaml` must
show only `experiment:` and `solver_workflow:`. Smoke spec adds only
`benchmark.tasks`.

**AC-2 -- Leak guard remains intact.** The no-external-reference and dependency
guardrail prose remains byte-identical to the parent solver README. The inserted
README text contains no hidden-test, solution, verifier, public-fetch, or
dataset-specific tokens.

**AC-3 -- Decision-policy evidence is artifact based.** Judge target success
from committed files, not transcript narration: feature-only refs/outputs/docs
removed or gated, no dependency edits, no broad refactor, and no unrelated model
semantics rewritten.

**AC-4 -- h0045 is promoted only if passers stay pass.** This is a stabilization
hypothesis. Both primary targets and every canary must remain PASS in smoke.

**AC-5 -- Proxy counts are not pass-rate claims.** The subagent probe supports
running the smoke. It cannot replace strict audit, score, and artifact review.

## Gatekeeper review

**Recommendation: APPROVE** -- exactly one Implementation-stage policy block,
leak-guard/dependency guardrails unchanged, full spec differs only in the two
allowed fields, smoke spec adds only the seven-task `benchmark.tasks` panel, and
both specs are frozen. WARN: G7 actionability/inert-risk, because the rule is
feature-boundary prose rather than a literal before/after SQL token
substitution; the smoke must be judged by committed artifacts, not transcript
narration.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10).
Reviewed 2026-06-10T16:46:12Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs parent is one hunk inside `## Stage: Implementation`, adding only the feature-boundary removal/toggle guard. |
| G2 leak-guard intact | PASS | Parent no-external-reference and dependency/package guardrail prose unchanged. Added README block contains no dataset slug, concrete variable/column name, hidden-test token, solution/verifier instruction, or public-fetch instruction. |
| G3 spec two fields | PASS | `diff baseline.yaml h0045...yaml` changes only `experiment:` and `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, and `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | Full-to-smoke diff adds only `benchmark.tasks` with seven `ade-bench-` slugs, including both named targets and stable pass-regression canaries. |
| G5 both frozen | PASS | `h0045-feature-boundary-removal-toggle-guard.frozen.yaml` and `.smoke.frozen.yaml` exist; both preserve `kind: spacedock_solver` and `runtime: codex`; frozen smoke lists all seven tasks. |
| G6 resolver fidelity | PASS | Inserted README text matches the falsifiable claim: keep remove/disable feature requests at the project-local feature boundary and reject broad domain rewrites. No scope creep outside Implementation. |
| G7 actionability/inert-risk | WARN | The rule is concrete about artifact families (config/variable, refs, CTEs, joins, select outputs, docs) but still prose, not a literal SQL skeleton. Subagent probe reduces but does not remove inert-risk. |
| G8 regression-canary coverage | N/A (PASS) | Gated instruction: fires only when the task asks to remove, disable, or add a switch for a project-local feature. Smoke still carries same-family quickbooks003 plus f1001/airbnb001/ana-eng001/asana001 canaries. |
| G9 selector independence | N/A (PASS) | Not a selector protocol. |
| G10 self-correcting false-positive | N/A (PASS) | Not a reconcile/check-and-replace lever. |
| G11 multi-model-target risk | N/A (PASS) | Targets have broad quickbooks scored surfaces, but the lever is not single-model: it instructs a project-local reference/output/doc scan for the feature boundary. Artifact review must still inspect all target-side edits. |
| G12 decision-fork probe quality | PASS | The hypothesis includes `## Pre-smoke Decision-Fork Probe`, the tested fork, prompt context, weak control A, final generalized B counts, exact README wording, artifact signature, and proxy-only caveat. |

**For the captain:** APPROVE for smoke. Decisive read is artifact-level:
quickbooks002/004 must remain PASS through scoped feature-boundary edits, not a
broad rewrite; any canary regression or green-by-unrelated-refactor is NO-GO.

## Stage Report: propose

- DONE: Forked `solver_workflows/codex-ade-dbt-minimal` to
  `solver_workflows/h0045-feature-boundary-removal-toggle-guard` and added
  exactly one Implementation-stage feature-boundary removal/toggle guard. The
  solver README does not name QuickBooks, concrete variables, concrete columns,
  or dataset slugs.
- DONE: Created full and smoke specs. Full diff vs `baseline.yaml` changes only
  `experiment:` and `solver_workflow:`. Smoke diff adds only
  `benchmark.tasks` = quickbooks002 / quickbooks004 / quickbooks003 / f1001 /
  airbnb001 / ana-eng001 / asana001. All seven are `@baseline` passers.
- DONE: Froze both specs with `rk freeze --allow-missing`. Frozen smoke preserves
  `spacedock_solver`, `codex`, solver README content hash
  `sha256:376cee68489e6b3eb1307c7f14e3c3279e9d23b703fd531382afccd5796570e0`,
  and all seven smoke tasks.
- DONE: Ran `rk run --explain` on the frozen smoke spec. It resolves to 7 tasks,
  concurrency 1, runtime `codex`, model `gpt-5.5`, and the sample composed
  prompt includes the h0045 feature-boundary guard.

## Smoke result (cycle 1 — BLOCKED by infrastructure failure, no experiment evidence)

Smoke launch on `specs/h0045-feature-boundary-removal-toggle-guard.smoke.frozen.yaml`
(7-task panel) crashed at orchestrator startup (`rc=1`, ~6s) BEFORE any cell of
this launch executed. No score, no audit, no behavioral read — this is an
`infrastructure-failure`, not experiment evidence.

- Pre-flight all clean: `rk run --explain` resolved 7 tasks / concurrency 1 /
  codex / gpt-5.5, composed prompt carries the h0045 guard; all 7 panel tasks
  confirmed `@baseline` 1.0 in `runs/ade-bench-baseline/622bdedac572b479`
  (parsed via `trial_name` — `benchmark_task_id`/`query_id` are null in that file).
- Launch: `drivers/rk-run-detached.sh h0045-smoke … run` → handle
  `runs/.rk-handles/h0045-smoke-20260610-170831` (pid 4018431).
- Crash: `done` → `rc=1 rundir=runs/ade-bench-h0045-feature-boundary-removal-toggle-guard/df3a3b1e3a4c2ace`.
  Traceback: `PermissionError: [Errno 13] Permission denied:
  …/df3a3b1e3a4c2ace/_job_config.yaml` at `razorback/cli/run.py:360`.

### Root cause — orphaned root-owned state from a PRIOR, non-launcher h0045 run

- The deterministic content-hash run dir `df3a3b1e3a4c2ace` already existed,
  owned by `root:root` (I run as `kent`), created **16:59-17:00** — ~9 min BEFORE
  my 17:08 dispatch. It held only partial `quickbooks002` cell attempts
  (`__ah6uCZP`, `__nACSwo7`) + `_razorback/freeze`, no `_job_config.yaml`.
- Two Harbor containers from that prior run were still **running** at diagnosis:
  `ade-bench-quickbooks002__ah6uczp-main-1` (started 16:51:38) and
  `…__nacswo7-main-1` (started 16:50:49). Their orchestrator was already dead
  (`pgrep -af "rk run"` → none), so the dispatch's "no other rk run is active"
  was true, but the run leaked root-owned containers + run-dir tree.
- There is **no other `h0045` handle** under `runs/.rk-handles/` — so the prior
  run was a direct/manual `rk run` of this same spec (not via the audited
  launcher), which crashed/was killed and orphaned its container children.
- My `kent`-owned relaunch reuses the same deterministic run-dir path and cannot
  write `_job_config.yaml` into the root-owned tree → immediate `rc=1`.

### Recovery is BLOCKED on privilege / shared-state decision

Clean recovery = (a) stop the two orphaned `quickbooks002` containers, (b) remove
the stale root-owned `df3a3b1e3a4c2ace` run dir, (c) relaunch. I cannot do (a)/(b)
as `kent`: `docker rm -f` of the two containers was DENIED by the auto-mode
classifier (force-removing shared containers of uncertain provenance), and the
run dir is `root:root`. Escalated to team-lead for a privileged cleanup or
go-ahead before relaunch. No behavioral conclusion can be drawn until the
infra failure is recovered and the smoke actually executes its 7 cells.

### Cleanup + relaunch (captain APPROVED, bounded)

- `docker rm -f` of ONLY the two orphaned containers
  `ade-bench-quickbooks002__ah6uczp-main-1` + `…__nacswo7-main-1` (names confirmed
  first via `docker ps --filter name=quickbooks002`; no other container touched).
  After: zero `ade-bench` containers remain.
- `sudo rm -rf …/df3a3b1e3a4c2ace` (only that one hash dir), then `sudo rmdir`
  the now-empty root-owned experiment parent so `rk` recreates the tree as `kent`.
  Nothing else under `runs/` touched.
- Relaunch: `drivers/rk-run-detached.sh h0045-smoke-r2 … run` → handle
  `runs/.rk-handles/h0045-smoke-r2-20260610-172101` (pid 4020017). Run dir
  `df3a3b1e3a4c2ace` recreated `kent:kent`, no instant crash (no seed perturbation
  needed — clearing the collision was sufficient). Polling for `done` across turns.

(Cycle 1 was an infra collision, not experiment evidence — the real smoke result
follows below once cycle-2 completes.)

### Cycle 2 — REAL evidence (GO)

Run dir `runs/ade-bench-h0045-feature-boundary-removal-toggle-guard/df3a3b1e3a4c2ace`
(deterministic hash put it back at the same path after the orphan was cleared;
this tree is `kent`-owned and complete). `done` rc=0, end 2026-06-10T18:25:53Z.

- **Strict audit clean:** `rk audit --policy strict` → `summary: {clean: 7,
  tainted: 0, coverage_missing: 0}`, every cell `findings: []`.
- **Score:** `rk score` → `stratified_pass_at_1: 1.0`, `n_completed: 7`,
  `n_errored: 0`. Against-constant verdict `above` (baseline 0.1875).
- **Trace capture:** `captured = 1` on all 7 cells (subagent-trace-manifest).

**Verdict: GO → full.** 7/7 PASS (all `@baseline` 1.0 passers held), strict
audit clean, and BOTH targets passed via genuinely NARROW feature-boundary
committed edits (not a broad rewrite, not green-by-unrelated-refactor).

| Task | Role | Baseline | Smoke | Verifier tests | Artifact classification |
|---|---|---|---|---|---|
| quickbooks002 | target (removal) | 1.0 | PASS | 8/8 | NARROW feature-boundary |
| quickbooks004 | target (toggle)  | 1.0 | PASS | 48/48 | NARROW feature-boundary |
| quickbooks003 | same-family canary | 1.0 | PASS | 14/14 | n/a (rule not applicable) |
| f1001 | convention-bleed canary | 1.0 | PASS | 6/6 | n/a (no bleed) |
| airbnb001 | cross-family canary | 1.0 | PASS | 10/10 | n/a (no bleed) |
| ana-eng001 | cross-family canary | 1.0 | PASS | 1/1 | n/a (no bleed; 0-file no-op) |
| asana001 | cross-family canary | 1.0 | PASS | 2/2 | n/a (no bleed) |

## Behavioral analysis

Committed artifacts read from each cell's ENSIGN `apply_patch` payloads
(`agent/sessions/.../rollout-*.jsonl`) — NOT the first-officer narration in
`agent/codex.txt`. Both targets are decided by what reached the committed SQL.

**quickbooks002 — removal — NARROW FEATURE-BOUNDARY (GO).** Instruction: remove
the `using_department` variable and all project-local refs, NOT the Fivetran
source package. Committed patch touched 6 project-local files (`dbt_project.yml`,
`quickbooks__ap_ar_enhanced.sql`, `int_quickbooks__sales_union.sql`,
`int_quickbooks__expenses_union.sql`, `quickbooks.yml`, `docs.md`); **zero**
dependency / `dbt_packages` / Fivetran edits. The signature matches the README
guard exactly:
- Removed the `using_department: true` var from `dbt_project.yml`.
- **Deleted** the feature-only `{% if var('using_department') %} departments as
  (...) {% endif %}` CTEs, the `department_name` select outputs, and the
  `left join departments …` joins — deleted the whole guarded block *including
  the body*, did NOT unwrap the guard to keep the feature alive.
- **Preserved the base raw attribute** `department_id` (it is part of the base
  entity and does not depend on the removed feature) — removed only the derived
  `department_name`. No null/placeholder outputs.
- Removed the `department_name` schema docs in `quickbooks.yml` + the
  "department level detail" prose in `docs.md`.
- Verifier: 8/8 hidden tests PASS → genuine pass, not green-by-refactor.

**quickbooks004 — toggle/disable — NARROW FEATURE-BOUNDARY (GO).** Instruction:
add a `using_exchange_rate` var defaulting false and use it to hide the
converted-amount / converted-payment (exchange-rate) columns. Committed patch
added `using_exchange_rate: false` to `dbt_project.yml` and gated ~30
project-local models (all `transaction_lines/*`, `double_entry_transactions/*`,
the intermediate joins/unions, `ap_ar_enhanced`, `expenses_sales_enhanced`,
`quickbooks.yml`); **zero** dependency edits. This wide footprint is the
*expected* feature-boundary shape (the exchange-rate columns are wired through
every transaction/double-entry/union model — it matches the `@baseline` PASS
footprint), NOT a broad domain rewrite:
- Gated ONLY the exchange-rate-derived columns (`converted_amount`,
  `total_converted_amount`, `total_current_converted_payment`,
  `estimate_total_converted_amount`) behind `{% if var('using_exchange_rate',
  false) %}`.
- **Preserved the enabled-path formulas verbatim** — the
  `* coalesce(exchange_rate, 1)` expressions and the credit/sign `case`
  logic are wrapped, not rewritten.
- Structural changes are exactly the README-allowed "adjust column alignment /
  grouping only as needed because disabled outputs changed shape": moved the
  trailing comma so `total_amount` is the last column when converted columns are
  off, and conditionally switched `dbt_utils.group_by(11)→(9)` /
  `group_by(17)→(15)` to match the reduced non-aggregated column count.
- Did NOT recompute unrelated formulas, signs, grains, joins, or the
  `using_estimate` guard.
- Verifier: 48/48 hidden tests PASS.

**Canaries (5/5 hold, no convention bleed).** quickbooks003 (same family),
f1001 (broad-footprint convention-bleed canary), airbnb001, ana-eng001 (a
correctly-identified 0-file no-op), asana001 — all PASS with 0 failing verifier
tests. The feature-boundary guard is gated on remove/disable-feature tasks and
did not mis-fire: no spurious `using_*` gating leaked into the canaries, and
each canary's committed footprint reflects its own task scope, not the rule.

**Net:** 0 regressions, both targets stabilized via artifact-proven narrow
feature-boundary edits. As a stabilization lever on the minimal @baseline its
standalone protective value is limited (the targets already pass) — this smoke
confirms (a) no harm and (b) the feature-boundary artifact discipline holds; the
real protective value is when combined with a flip-seeking lever at full scale.
(In-stage instruction lever — no `_artifacts/WORKFLOW-REFINE.md` entry needed.)

## Stage Report: smoke

- DONE: Smoke run on `specs/h0045-feature-boundary-removal-toggle-guard.smoke.frozen.yaml`
  (7-task panel) completed, launched DETACHED via `drivers/rk-run-detached.sh`, PID
  file, polled across turns. Cycle 1 died at startup on a root-owned run-dir
  collision (infra-failure, recovered via captain-approved bounded cleanup);
  cycle 2 is the real evidence — run dir `df3a3b1e3a4c2ace`, `done` rc=0.
  Strict audit `--policy strict` clean (`tainted: 0`, `coverage_missing: 0`),
  `captured: 1` on all 7 cells, score `stratified_pass_at_1: 1.0`. Attestation
  in `## Smoke result` → `### Cycle 2`.
- DONE: THE DECISIVE ARTIFACT READ (AC-3/AC-4). All 7 tasks HELD PASS. Read the
  committed `apply_patch` payloads (ensign rollout, not narration) for both
  targets: quickbooks002 = NARROW feature-boundary removal (var + dept CTEs/joins/
  outputs/docs deleted; base `department_id` preserved; no dependency edits; no
  guard-unwrap; no placeholders; 8/8 tests). quickbooks004 = NARROW feature-
  boundary toggle (added `using_exchange_rate: false`; gated only converted-amount
  columns; enabled-path formulas preserved; group_by/comma adjusted only for
  shape; no dependency edits; no broad rewrite; 48/48 tests). Classification +
  evidence in `## Behavioral analysis`.
- DONE: Canary check (AC-5). quickbooks003 + f1001 + airbnb001 + ana-eng001 +
  asana001 all hold PASS, 0 failing verifier tests, no convention bleed (guard
  did not mis-fire on non-feature-removal tasks). Per-cell results in
  `## Smoke result`. (In-stage instruction lever → no WORKFLOW-REFINE entry.)

### Summary

GO → full. 7/7 PASS, strict audit clean, both targets stabilized via
artifact-proven NARROW feature-boundary edits (not green-by-broad-rewrite): qb002
removed only project-local department logic preserving `department_id`; qb004
gated only the exchange-rate columns preserving enabled-path formulas. The
~30-file qb004 footprint is the expected feature-boundary shape (matches the
@baseline PASS footprint), not a broad rewrite. Notable: a prior non-launcher
run of this exact spec orphaned root-owned containers + a run dir that blocked
the first launch; recovered with a bounded, captain-approved cleanup.
