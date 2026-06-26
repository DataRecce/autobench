---
id: spd0011
title: Classifier contract checkpoint — make router advice enforceable without a broad stage rewrite
status: smoke
kind: hypothesis
source: "post-hypothesis stabilization plan; forks current registry baseline spd0008; follows spd0006/spd0008/spd0009 evidence that rules are often detected but not obeyed"
started: 2026-06-26
completed:
verdict:
score: 0.8
worktree:
---

## Hypothesis

The current registry baseline is the `spd0008-over-emit-collapse` solver workflow. It inherits the
`spd0007b-value-def-no-idcast` classifier/router stage and adds G2 over-emit rules, but it still does
not force implementation compliance. The solver can correctly identify a rule family and still
produce a noncompliant artifact because the implementation stage has many competing generic rules and
validation mostly accepts a clean `dbt build`.

**Single README change:** add a narrow contract checkpoint between exploration and SQL edits, and
make validation check that contract. This is a micro-hypothesis, not a broad stage rewrite:

1. `Classify` produces a provisional router result and names evidence still needed.
2. `Exploration` gathers only the local evidence needed to finalize the contract.
3. A new `Implementation Contract` checkpoint is written before SQL edits.
4. `Implementation` must follow that contract or mark it blocked.
5. `Validation` must verify the contract signature, not just table existence and build success.

This remains README-only. No harness, verifier, runtime, model, fixture, or multi-worker routing
changes are included. Moving all existing implementation tips to other stages is explicitly out of
scope for this first smoke.

## Rationale

Prior hypotheses surfaced a consistent compliance failure mode:

- `spd0006` showed that classifier/router advice can fire without producing a reliable task flip.
- `spd0008` showed the over-emit rule was directionally right, but `airbnb001` failed because the
  latest-window filter was left behind `is_incremental()`, so `--full-refresh` emitted full history.
- `spd0009` showed G1 could drive from a spine/dimension without pinning enough row-shape and
  second-blocker detail to pass; however, those G1 cells are not clean first-smoke flip targets.

The expected gain is not a new semantic rule. The expected gain is that already-known rules become
hard enough for the worker to execute and validate.

## Proposed README Mechanics

### Classify output

For every target table, the worker must write:

- target table name
- selected router branch: `R1` through `R6`
- candidate Axis rule: `G1`, `G2`, `G3`, or none
- oracle-free evidence for why the rule fires
- canary/regression risk
- evidence still needed before implementation

### Exploration for contract

Exploration must resolve:

- model naming convention
- materialization defaults
- declared model set
- sibling model patterns
- source table existence
- source row counts, key distributions, and date bounds
- incremental/full-refresh behavior when relevant
- package or missing-source blockers

### Implementation contract

Before editing SQL, the worker must write:

- `selected_rule`
- `target_tables`
- `primary_grain_driver`
- `input_relations`
- `implementation_skeleton`
- `forbidden_patterns`
- `expected_row_shape`
- `validation_signature`
- `contract_blocked_condition`

The contract must be based only on local workspace evidence. `expected_row_shape` and
`validation_signature` must be derived from a named rule template plus local evidence, not invented
freely by the worker.

For this first smoke, the allowed contract template inventory is only:

- `G2_LATEST_WINDOW_FULL_REFRESH`: for targets whose target or sibling model has latest-window logic
  tied to `is_incremental()`. The contract must name the sibling/target model, source date column,
  max-date anchor, window length, expected single-window grain, and the forbidden pattern: leaving the
  required window filter only inside an `is_incremental()` branch.
- `G2_REPORT_RAW_GROUPING_HOLD`: for report-grain targets already passing under the current champion.
  The contract must name the raw grouping column, primary anchor relation, lookup relation if any,
  and the forbidden pattern: regrouping on a canonicalized lookup value instead of preserving the raw
  key.

Any other named template is out of scope for the first smoke.

### Implementation-tip relocation

The long-term proposal restructures existing implementation-stage tips so they no longer compete
with the classifier output. That relocation is **future work**, not part of this first smoke lever.
This hypothesis should only add the contract checkpoint and contract-aware validation. The first
smoke must not move these tips.

Future strategy-selection tips:

- `PER-KEY METRIC AGGREGATE`
- `COVERAGE / COMPLETENESS`
- `BUILD / RENAME — PRESERVE THE COLUMN SET`
- `TMP/INTERMEDIATE-TIER REMOVAL`
- `FEATURE-BOUNDARY REMOVE / TOGGLE / DISABLE`
- `PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX`

These are classification or contract decisions that belong in a later relocation hypothesis.

Future calculation recipes that can remain in `Implementation`:

- `EXCLUDE-A-CATEGORY AVERAGE`
- `CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN`
- `TOP-N TIE-CROSSES-CUTOFF`

Future proof requirements:

- row-count and row-shape checks
- grain uniqueness checks
- before/after reconciliation
- full-refresh survival checks
- all target tables exist as base tables
- forbidden patterns were avoided

`TMP/INTERMEDIATE-TIER REMOVAL` is the clearest example: the implementation may inline a model, but
the important proof is before/after reconciliation. That belongs in a future contract signature and
validation relocation hypothesis.

### Implementation constraint

Implementation must follow the contract. If the contract proves infeasible, the worker must mark
`contract_blocked` with local evidence or return to exploration to fill a missing evidence field. It
may not silently switch to a different selected rule.

### Validation constraint

Validation must check the rule-specific signature:

- target tables exist as base tables;
- target names match convention;
- row shape matches the named rule template plus local evidence captured in the contract;
- grain keys are unique where expected;
- forbidden patterns were avoided;
- every contract target is checked;
- a clean `dbt build` alone is not enough.

## Smoke Plan

Run a targeted smoke only. Do not launch full unless the smoke shows a net improvement against the
current registry baseline.

Targets:

- `airbnb001` — primary flip target; known G2 worker-noncompliance where the latest-window filter
  must survive `--full-refresh`.
- `apple_store001` — known report-grain/raw-key success; should hold if the contract preserves the
  useful part of `spd0008`. Because it already passes in the current registry baseline, it is a hold
  target, not a flip target.

Do not count `salesforce001` or `jira001` as first-smoke success targets. They can be diagnostic cells
later, but prior evidence shows second blockers beyond classifier compliance.

Hard gate canaries, all current-registry-baseline passers that must hold:

- `activity001`
- `app_reporting001`
- `google_play001`
- `google_play002`
- `quickbooks003`

Telemetry-only cells may be reported but do not decide go/no-go because they have known variance or
are not current-registry-baseline passers:

- `mrr001`
- `mrr002`
- `retail001`
- `recharge002`
- `f1003`

## Acceptance Criteria

**AC-1 — README-only.** The variant differs from the champion solver only in the README. The no-fetch
leak guard remains intact. The smoke spec differs only by experiment, solver workflow, and narrowed
tasks.

**AC-2 — Contract artifact evidence.** For each target, the agent transcript must show an
implementation contract written before SQL edits or before final implementation decisions.

**AC-3 — Smoke score.** `airbnb001` must flip versus the current registry baseline by committed
artifact. Every hard gate canary listed in the smoke plan must hold. Telemetry-only cells are
reported separately and never reclassified after the result to rescue or reject the smoke.

**AC-4 — Compliance attribution.** At least one target outcome must show that validation checked a
rule-specific signature derived from a named rule template plus local evidence, not only `dbt build`.

**AC-5 — No premature full.** If `airbnb001` does not flip, or if any stable-passer canary regresses,
conclude `validated-not-promoted` or revise narrowly. Do not full-run.

## Expected Outcome

Expected realistic yield is `+1` if the contract mechanism improves compliance on a known near-miss.
The first-smoke win condition is `airbnb001`; `apple_store001` is a hold target.

If the mechanism produces better logs but no target flips, bank the contract idea for the later
autonomous stabilization loop but do not promote it into the champion solver.

## Follow-up If Successful

If the smoke is positive, create a narrowed `spd0011b` or promote to expanded smoke with:

- `airbnb001`
- `apple_store001`
- one or two additional worker-noncompliance tasks from the outcome ledger
- the same regression canaries

Full run should remain a promotion test, not discovery.

## Gatekeeper review

**Recommendation: APPROVE** — purely-additive contract checkpoint forked from champion spd0008; specs in scope, leak-guard byte-identical, the validation_signature is an independent structural check (not self-anchored), and the gated 2-template inventory carries the full 5-canary hard-gate panel.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-26T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Diff vs champion spd0008 is 3 pure-add hunks (`90a91-103`, `269a283-349`, `383a464-477`): a Classify-output block, a new "Implementation Contract" stage + Exploration-resolve block, and a Validation contract-signature block. All serve the ONE idea — make router advice enforceable via a contract checkpoint. No deletions/changes (no `d`/`c` hunks); leak-guard untouched. |
| G2 leak-guard intact | PASS | Lines 1-30 (the no-fetch guard) byte-identical to parent (`diff` EXIT 0). Grep of added lines: every "gold" hit is PROTECTIVE ("never from gold", "DERIVED from the named template + local Exploration facts… never a baked gold count", "never on gold values, expected counts, or external lookup"); no `curl`/`wget`/`git clone`/`git ls-remote`/`http`, no `ground_truth`/`answer_key` read, no `db_description_withhint` paste. `expected_row_shape`/`validation_signature` are explicitly worker-derived from a named template + local evidence, not baked. |
| G3 spec two fields | PASS | `diff full-baseline.yaml spd0011-classifier-contract.yaml` shows only `experiment:` and `solver_workflow:` changed. Frozen diff adds only auto-derived freeze provenance (solver_workflow_content_hash, sealed_hash, harness_git_sha, solver_workflow_hash) — not authored edits. `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved (frozen line 91). |
| G4 smoke tasks+exclude | PASS | `harbor-local` smoke uses a positive `benchmark.tasks:` allowlist (no `exclude_tasks` — correct, that field errors `extra_forbidden` here). Exactly 12 dataset names, matching `--explain`'s `Tasks: 12`: targets airbnb001 (flip) + apple_store001 (hold), hard-gate canaries activity001/app_reporting001/google_play001/google_play002/quickbooks003, telemetry mrr001/mrr002/retail001/recharge002/f1003. All hypothesis-named targets present. No other field differs. |
| G5 both frozen | PASS | Both `spd0011-classifier-contract.frozen.yaml` and `…smoke.frozen.yaml` exist (3176B / 1865B). Both carry `kind: spacedock_solver` + `runtime: codex` (lines 4-5). |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: Classify-output fields, Exploration-for-contract, a pre-SQL "Implementation Contract" checkpoint with the 9 named fields + 2-template inventory (G2_LATEST_WINDOW_FULL_REFRESH, G2_REPORT_RAW_GROUPING_HOLD), and a Validation signature check. Generative/independent in spirit — it tells the worker how to DERIVE and structurally verify an artifact, not "re-run your own query / confirm your answer matches." No scope creep; existing tips explicitly NOT relocated (relocation flagged as future work, and the diff confirms tips at L365-438 are intact). |
| G7 actionability/inert-risk | WARN | The contract is a structured worked-form (9 named fields + 2 concrete forbidden-pattern templates with literal anti-patterns — e.g. "window filter only inside an `is_incremental()` branch"), which lands better than abstract prose. BUT the core lever is a process instruction ("write a contract before editing SQL, then follow it") — a discipline gate the solver can acknowledge-and-skip. Inert-risk: prior spider2-dbt evidence (spd0006/spd0009) is that rules are "detected but not obeyed"; a checkpoint that is itself prose has the same exposure. The smoke's AC-2 (transcript must SHOW the contract written before edits) is the right inert-detector — flag for the captain to judge by artifact, not log presence. |
| G8 regression-canary coverage | PASS | Lever is PRECONDITION-GATED, not fires-everywhere: the 2 templates fire only on targets whose model/sibling has the named structure; non-matching targets get `selected_rule: none` and use existing guidance unchanged (README L300-302). The new contract/validation STAGES are generative (every target writes a contract), so the regression risk is real but bounded — and the smoke carries the 5 hard-gate non-target canaries (activity001/app_reporting001/google_play001/google_play002/quickbooks003), all current-@baseline passers, plus apple_store001 as a perturbable raw-grouping hold. ≥2 perturbable canaries on the targets' construct (apple_store001 + the G2_REPORT_RAW_GROUPING_HOLD-shaped passers) present. |
| G9 selector independence | N/A | No multi-candidate / N-of-K selector protocol. The contract is a single per-target plan, not a field of competing candidates scored against each other. |
| G10 self-correcting false-positive | PASS | The Validation signature is a CHECK-and-fix-or-block lever, so G10 applies. (a) Scope: gated — checks the rule-specific signature only for targets that adopted a template; `none` targets fall through to existing validation. (b) Independence: the signature is an INDEPENDENT STRUCTURAL check of the BUILT ARTIFACT (table exists as base table, name convention, single-window row shape, raw-key preservation, grain uniqueness, forbidden-pattern absence) authored from the template BEFORE the SQL exists — it is not re-running the solver's own derivation/query, so it is not self-anchored. (c) Check-don't-replace: on failure it says "fix it or mark `contract_blocked` with local evidence" — investigate/block, not "swap to a structurally different query." No re-derived-double-entry false-green. |

**For the captain:** No FAILs → APPROVE; advance to `smoke`. One WARN to weigh (G7): the lever is fundamentally a process/discipline checkpoint, and spider2-dbt's recurring failure mode is "rule detected but not obeyed" — so judge the smoke strictly by AC-2/AC-4 committed-artifact evidence (was a contract actually written pre-edit AND did Validation run a template-derived signature beyond `dbt build`), not by whether the transcript merely mentions the contract. The airbnb001 flip is the single win condition; treat apple_store001 + the 5 hard-gate canaries as the must-hold panel.

## Stage Report: propose

- DONE: Fork the champion solver: cp -r solver_workflows/spd0008-over-emit-collapse solver_workflows/spd0011-classifier-contract
  Forked; pre-edit diff -r was identical.
- DONE: Edit ONLY solver_workflows/spd0011-classifier-contract/README.md to add the narrow Implementation Contract checkpoint + contract-aware validation per the hypothesis Proposed README Mechanics (one knob)
  3 purely-additive hunks (90a91-103 Classify output, 269a283-349 Exploration-resolve + new Implementation Contract stage, 383a464-477 Validation signature); no deletions.
- DONE: Keep the no-external-reference / leak-guard prose byte-intact; embed no gold values, dtypes, counts, or row numbers
  Lines 1-30 byte-identical to parent; all added "gold" mentions are protective; expected_row_shape/validation_signature explicitly worker-derived from template + local evidence.
- DONE: Do NOT relocate or delete any existing implementation-stage tips (relocation is explicit future work, out of scope for this smoke)
  All 6 tips intact in the Implementation stage; diff shows zero d/c hunks.
- DONE: Create full spec: cp specs/full-baseline.frozen.yaml ... then set experiment + solver_workflow (no other field changes)
  Built from full-baseline.yaml (editable source); experiment: spd0011-classifier-contract, solver_workflow: ./solver_workflows/spd0011-classifier-contract.
- DONE: Create smoke spec ... so ONLY these survive: airbnb001, apple_store001, activity001, app_reporting001, google_play001, google_play002, quickbooks003 (+ telemetry mrr001, mrr002, retail001, recharge002, f1003)
  Positive benchmark.tasks allowlist of exactly 12 dataset names (harbor-local rejects exclude_tasks as extra_forbidden, so positive allowlist is the proven pattern).
- DONE: Freeze both
  Wrote spd0011-classifier-contract.frozen.yaml and .smoke.frozen.yaml.
- DONE: Verify smoke selection via --explain
  rk run ... --explain reports Tasks: 12, solver_workflow resolves to solver_workflows/spd0011-classifier-contract.
- DONE: Confirm full-spec diff vs full-baseline.frozen.yaml shows ONLY experiment: + solver_workflow: changed
  Only authored changes are experiment + solver_workflow; remaining diffs (solver_workflow_content_hash, solver_workflow_hash, sealed_hash, harness_git_sha) are auto-derived freeze provenance.
- DONE: Run the gatekeeper review subagent and write a ## Gatekeeper review block
  Appended; overall APPROVE (no FAILs; one G7 WARN = process-checkpoint inert-risk).

### Summary

Forked champion spd0008-over-emit-collapse into spd0011-classifier-contract and made the single one-knob README change: added per-target Classify output fields, an Exploration-for-contract evidence-resolution list, a new pre-SQL Implementation Contract checkpoint (9 named fields + a 2-template inventory: G2_LATEST_WINDOW_FULL_REFRESH and G2_REPORT_RAW_GROUPING_HOLD), and a contract-signature Validation check. The diff is purely additive; existing implementation tips and the no-fetch leak-guard are untouched, no gold baked in. Full spec diffs only experiment + solver_workflow; smoke is a 12-task positive allowlist (--explain confirms Tasks: 12). Gatekeeper recommends APPROVE with one G7 WARN (judge the smoke by AC-2/AC-4 committed-artifact evidence, not transcript mentions). Stopped at the propose gate; no rk run launched beyond $0 --explain.
