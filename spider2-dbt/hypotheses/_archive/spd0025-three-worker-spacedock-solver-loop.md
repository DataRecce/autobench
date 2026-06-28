---
id: spd0025
title: Spacedock-native three-worker solver loop — Plan / Implement / Validate with FO-routed repair
status: conclude
kind: hypothesis
source: "captain architecture follow-up after spd0024: the right harness should be Spacedock-native, not an external Razorback harness. Current benchmark solver uses Spacedock, but appears to dispatch one ensign that runs Classify/Exploration/Implementation/Validation internally. Test whether a real FO-controlled three-worker loop can run inside one benchmark task."
started: 2026-06-28
completed: 2026-06-28
verdict: REJECTED
score:
worktree:
archived: 2026-06-28T05:42:32Z
---

## Hypothesis

The current Spider2-DBT solver workflow is Spacedock-powered, but the per-task execution is still
effectively a **single solving worker** reading the solver README and performing every stage itself:
Classify, Exploration, Implementation, Validation, and Finalization. That leaves the core validation
risk in place: the implementation worker can still be the same actor that judges whether its own dbt
artifact satisfies the structural contract.

**Falsifiable claim:** a Spacedock-native, FO-controlled **three-worker loop** can remove the
player/referee coupling without adding an external Razorback harness:

1. **Plan worker**: classify the task, inspect local evidence, and write a machine-readable plan:
   target tables, source relations, structural invariants, expected source-derived checks, and
   implementation instructions.
2. **Implement worker**: fresh worker that receives only the plan and local task workspace, writes the
   dbt models, builds them, and reports changed files plus built artifacts. It does not make the final
   pass/fail judgment.
3. **Validate worker**: fresh worker that receives the plan and built artifact, not the implement
   worker's self-assessment. It independently opens DuckDB/source tables, runs the structural checks,
   and returns a PASS/FAIL report with exact failed invariants and repair hints.

The FO owns the loop:

- if Validate PASSes, finish the benchmark task;
- if Validate FAILs, route only the validation report back to Implement for one bounded repair cycle;
- after at most two repair attempts, finalize with the best artifact and an explicit failure report.

This hypothesis does **not** require an external verifier or hidden-gold access. The structural checks are
derived from local source data, schema YAML, source manifests, and the plan. It is a harness architecture
probe: can the existing `spacedock_solver` path actually run independent stage workers in one Harbor task?

## Pre-smoke Decision-Fork Probe

Before proposing a score-bearing solver README variant, prove the execution model is feasible.

Open questions:

- Can the benchmark's `spacedock_solver` agent invoke the FO in a way that dispatches multiple fresh
  subagents inside a single Spider2 task?
- Can the Plan worker write an artifact that the Implement and Validate workers can both read inside the
  task workspace?
- Can the Validate worker inspect built DuckDB/source tables without relying on the Implement worker's
  prose report?
- Can FO route a validation failure back to the Implement worker and wait for the repaired completion
  within the benchmark timeout?

If any of these are false, the correct follow-up is not another README rule. It is a runtime/scaffold
change to make multi-worker solver execution possible.

## Proposed Three-Worker Contract

### Plan Worker Output

The Plan worker writes `spacedock_plan.json` in the task workspace with:

- `target_tables`: table name, expected grain, and why each target is in scope;
- `source_relations`: source/ref relations needed for each target;
- `structural_checks`: check id, target table, source-derived expected SQL, observed SQL, fail condition,
  and repair hint;
- `implementation_instructions`: concise instructions for the Implement worker;
- `forbidden_patterns`: explicit behaviors to avoid;
- `validation_scope`: what Validate must check.

For `provider001`, the structural checks should include:

- `specialty_mapping` row count equals runtime `count(*)` over `source('nppes','nucc_taxonomy')`;
- `provider` row count equals runtime `count(*)` over `source('nppes','npi')`;
- both checks are source-derived, not gold-derived, and the plan must not bake literal counts.

### Implement Worker Contract

The Implement worker receives `spacedock_plan.json`, writes/repairs dbt models, runs the cheapest build
that materializes the targets, and writes `spacedock_implement_report.json` with:

- changed files;
- build commands and exit codes;
- built target table names;
- any blocked condition.

The Implement worker must not mark the task correct. It can only report what it built.

### Validate Worker Contract

The Validate worker receives `spacedock_plan.json` and the built artifact. It writes
`spacedock_validation_report.json` with:

- `verdict`: PASS or FAIL;
- one result per structural check;
- expected value computed at validation time;
- observed value from the built artifact;
- failed invariant and repair hint when FAIL;
- whether target tables exist as base tables.

The Validate worker should not rely on the Implement worker's prose conclusions. It may read the changed
files and built DuckDB, but the authoritative judgment comes from the plan's checks plus local source data.

## Acceptance Criteria

**AC-1 — Feasibility first.** The first experiment may be a smoke-only feasibility probe on `provider001`.
It must demonstrate that Plan, Implement, and Validate were executed by separate fresh workers or clearly
prove the current runtime cannot do that.

**AC-2 — No player/referee coupling.** The final PASS/FAIL judgment must come from the Validate worker's
fresh-context report, not from the Implement worker's self-assessment.

**AC-3 — Bounded repair loop.** On validation failure, FO routes the structured validation report back to
Implement and performs at most two repair attempts. Retry behavior must be visible in the transcript or
artifact reports.

**AC-4 — Oracle safety.** Structural checks are source-derived or schema-derived only. No hidden gold,
verifier output, expected tables, public fetches, or hardcoded gold counts.

**AC-5 — Target outcome.** For `provider001`, success is `provider001 >= 2/3` under the three-worker loop
while canaries hold. If multi-worker execution is infeasible, mark the hypothesis as a runtime-feasibility
blocker rather than scoring it as a solver failure.

## Smoke Plan

Start with the smallest feasibility smoke:

- target: `provider001`
- canaries: `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`
- trials: `1` for the first feasibility probe; only move to `trials: 3` after the transcript proves the
  three-worker loop actually ran.

Expected first result categories:

- **FEASIBLE + provider pass**: architecture is promising; run a `trials: 3` provider smoke.
- **FEASIBLE + provider fail with validation report**: architecture works; improve the provider plan/checks.
- **INFEASIBLE**: current `spacedock_solver` path cannot dispatch Plan/Implement/Validate as independent
  workers inside one task; file a runtime/scaffold follow-up before more README experiments.

## Follow-up If Successful

If `provider001` passes reliably and canaries hold, generalize the three-worker loop to a small catalog:

- `provider001`
- `xero001`
- `movie_recomm001`
- `tickit002`
- `nba001`

Do not run a full board until the three-worker loop is proven feasible and at least two catalog targets
show artifact-attributable improvement in smoke.

## Gatekeeper review

**Recommendation: APPROVE** — structural three-worker FO-loop restructure is the intended single idea; leak-guard byte-intact, provider001 checks are source-derived (`count(*)` over `source('nppes',…)`, no baked literals, no gold/tests reads), specs preserve `spacedock_solver`/`codex`/`trials:1` with the 5 named tasks.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-28.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | README restructured into one idea — a Spacedock-native FO three-worker loop (Plan/Implement/Validate + bounded repair). Per the captain context flag this multi-section restructure IS the single intended structural change, not additive clauses. The domain rules (router, G2/G3, gated patterns) are carried forward unchanged, now folded into the Plan worker's contract rather than executed by one worker. |
| G2 leak-guard (hidden gold) | PASS | No-fetch + preserve-deps paragraphs (lines 3-23) **byte-identical** to champion spd0013. Every `gold`/`expected` hit is guard-context ("NEVER gold, tests, expected"; "compares … against a hidden gold"). No gold table name/columns enumerated; no instruction to read a gold/tests/expected file. No hardcoded counts (874/85196/460/82339 → NONE). |
| G3 spec two fields | PASS | No full spec exists by design — feasibility-only smoke mirroring spd0023/spd0024 (AC-1). Smoke spec preserves `agent.kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1`; `experiment:` set to the slug. (Full-spec two-field diff is N/A until a scoring full run is filed.) |
| G4 smoke narrows tasks only | PASS | Smoke `benchmark.tasks` = exactly the 5 declared: provider001 (target) + apple_store001, google_play001, mrr001, quickbooks002 (canaries). Includes the sole target the `## Hypothesis` names (provider001). |
| G5 both frozen | PASS | `…smoke.yaml` + `…smoke.frozen.yaml` both present; frozen carries `kind: spacedock_solver` + `runtime: codex` + `solver_workflow_content_hash: sha256:9d7f9fc0…` (differs from baseline 9660d413, confirming a real fork). |
| G6 resolver fidelity | PASS | Inserted text matches the falsifiable claim: a fresh Validate worker, given only the plan + built artifact (NOT the Implement worker's self-assessment), recomputes every `expected` from local source data — independent structural check, the opposite of the self-anchored disease. provider001 checks are SOURCE-DERIVED `count(*)` over `source('nppes',…)`. |
| G7 actionability/inert-risk | PASS | Mechanical: workers write named JSON artifacts with literal field schemas; `expected_sql`/`observed_sql` are runnable queries; `repair_attempt` counter makes the loop transcript-visible. Inert-risk is the live feasibility question; the README hard-codes the honest-INFEASIBLE fallback so a disguised single-worker run is named invalid. |
| G8 regression-canary coverage | PASS | Generative (loop fires on every task). Smoke keeps 4 non-target canaries from families other than provider's NPPES family — apple_store001 (report-grain), google_play001, mrr001 (R1/value-contract), quickbooks002 — ≥2 perturbable passers in the most-at-risk families. |
| G9 selector independence | N/A (PASS) | Not a multi-candidate selector. Sequential single-pass-per-stage pipeline with bounded repair; Implement/Validate split provides genuine context-isolation, not photocopy candidates. |
| G10 self-correcting false-positive | PASS | Validate-and-route-repair family. Repair routes back to a fresh Implement worker (no silent value rewrite); independence source is a structural invariant + a separately-sourced `count(*)` over `source(…)` recomputed at validation time; bounded to two cycles. Provider checks are row-count/existence (spd0002 SAFE class). |

**For the captain:** Auto-approved to smoke. The multi-section README rewrite is the intended single structural change (three-worker FO loop), correctly not failed under G1 for "more than one knob." Integrity rails clean: leak-guard byte-identical to spd0013, provider001 checks source-derived with no baked counts/gold reads, specs preserve `spacedock_solver`/`codex`/`trials:1` over exactly the 5 named tasks. No full spec by design (feasibility-only); a scoring full run should re-trigger G3 before promotion. Watch the smoke transcript for the load-bearing signal — whether the `spacedock_solver` path genuinely dispatched three fresh sub-workers, or honestly reported INFEASIBLE (both valid; a disguised single-worker run is not).

## Smoke result

## Verdict

## Stage Report: propose

- DONE: Fork the champion (cp spd0013 -> spd0025)
  solver_workflows/spd0025-three-worker-spacedock-solver-loop/README.md created from spd0013.
- DONE: RESTRUCTURE README into a Spacedock-native THREE-WORKER FO LOOP
  Added "YOU ARE THE FIRST OFFICER" + "The FO loop" + "Worker isolation contract" + "THE THREE WORKER ARTIFACTS" sections; the solver now dispatches Plan/Implement/Validate sub-workers, not runs stages itself.
- DONE: README instructs FO to dispatch THREE FRESH sub-workers in sequence
  Plan writes spacedock_plan.json; Implement (fresh, plan-only) writes spacedock_implement_report.json and MUST NOT judge pass/fail; Validate (fresh, plan+artifact, NOT implement self-assessment) writes spacedock_validation_report.json with PASS/FAIL; FO loops, ≤2 bounded repairs routing ONLY the validation report.
- DONE: Preserve champion domain guidance by FOLDING it into the Plan worker
  Router R1-R6, G2 over-emit, G3 column-value contract, gated analytic patterns, LAG period-over-period all carried verbatim under "PLAN WORKER — DOMAIN GUIDANCE TO FOLD INTO THE PLAN".
- DONE: provider001 structural_checks SOURCE-DERIVED + oracle-safe
  specialty_mapping rowcount == count(*) over source('nppes','nucc_taxonomy'); provider rowcount == count(*) over source('nppes','npi'); no literal counts; expected_sql run at validation time.
- DONE: Keep no-external-reference / leak-guard prose byte-intact
  Lines 3-23 (intro + no-fetch + preserve-deps) diff byte-identical to spd0013; no gold values/counts/dtypes.
- DONE: Create FEASIBILITY smoke spec (trials:1, 5 tasks)
  specs/spd0025-three-worker-spacedock-solver-loop.smoke.yaml: experiment+solver_workflow set, trials:1, tasks = provider001 + apple_store001 + google_play001 + mrr001 + quickbooks002; no stale baseline content-hash.
- DONE: Freeze from repo root; content_hash non-null + differs from baseline 9660d413; --explain Tasks: 5
  Frozen content_hash sha256:9d7f9fc0... (!= 9660d413), trials:1; `rk run ... --explain` reports `Tasks: 5`.
- DONE: Confirm agent.kind: spacedock_solver + runtime: codex preserved; full-spec NOT required
  Frozen spec lines 4-5: kind: spacedock_solver / runtime: codex; feasibility smoke only (like spd0023).
- DONE: grep README — no hardcoded gold counts (874/85196/460/82339), no gold/tests/expected reads
  Count grep: NONE; gold-read grep: only inherited guard-prose references, no file reads.
- DONE: Run gatekeeper review subagent; write ## Gatekeeper review block
  Recommendation APPROVE (all 10 rules PASS/NA); flagged as captain-authored architecture probe.
- DONE: Do NOT launch any rk run beyond $0 --explain; commit
  Only `--explain` (foreground, $0) was run; committed before signaling.

### Summary

Restructured the spd0013 champion into a Spacedock-native three-worker FO loop (Plan -> Implement -> Validate with FO-routed bounded repair, ≤2 cycles), folding all spd0013 domain knowledge into the Plan worker's plan/checks/forbidden-patterns rather than losing it. provider001 gets two source-derived oracle-safe row-count checks (count(*) over source('nppes',...)). Leak-guard prose is byte-intact; no gold counts or gold/tests/expected reads. Feasibility smoke spec frozen (trials:1, 5 tasks, content_hash 9d7f9fc0 differs from baseline 9660d413, --explain shows Tasks: 5). Gatekeeper APPROVE. FO owns the smoke launch.


## Smoke result + Verdict

**INFEASIBLE via README — RUNTIME-FEASIBILITY BLOCKER (AC-5), not a solver failure.** Feasibility smoke
`runs/spd0025-three-worker-spacedock-solver-loop/09dace6e4c75b2e1` (trials=1, 5 cells, strict audit CLEAN
5/0/0). provider001 = 0.0; canaries 4/4 hold.

**The three-worker loop did NOT materialize.** provider001's cell has only **2 worker session transcripts**
(one labeled "IMPLEMENT worker" + one FO) — IDENTICAL to a normal single-ensign cell (apple_store001 also
2 sessions). The 26 `spawn_agent` / 73 `spacedock_plan.json` / 54 `implement_report` / 52
`validation_report` string hits are README echo + the FO writing the plan/validation artifacts in its OWN
context. So the runtime collapsed the FO-routed Plan→Implement→Validate loop into the usual **FO + 1
worker**: Plan and Validate ran inside the FO context → the player/referee coupling was NOT removed (AC-2
fails); 3 separate fresh workers were NOT demonstrated (AC-1 fails).

**Verdict (per AC-5):** the `spacedock_solver` codex path cannot, from the README alone, dispatch
independent Plan/Implement/Validate workers inside one Harbor task. The correct follow-up is NOT another
README rule — it is a **runtime/scaffold change** to make multi-worker solver execution real (a
captain/engineering decision). Combined with spd0024 (even target+check+retry can't get the worker to
reliably EXECUTE a multi-table fix), the picture is: README levers are exhausted; the remaining gap needs
runtime engineering AND still faces the execution-variance wall on multi-table cells. @baseline unchanged.
