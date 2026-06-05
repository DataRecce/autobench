---
id: h0014
title: Implementation — for analysis/answer deliverables, back each component of the answer with its own direct query (include/exclude only on confirmation)
status: propose
kind: hypothesis
source: concept-resolve-uncovered-false-greens fan-out; evidence re-audit of @baseline (622bdedac572b479, 31/48). Lone tail — f1011: the analysis answer model emitted "ABDE" but the correct answer was "ABE"; option D was included on plausibility, never verified, and check_option_b failed (1/6). Isolated task type (answer-style deliverable). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-04T13:40:51Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The re-audit found `f1011` is a distinct, isolated failure type: the deliverable is an
**analysis answer** model (`analysis__answer`, value `ABDE`) graded per-option by
`check_option_*` tests. The solver included option **D** ("caution flags affect lap times")
on the strength of reading model logic and gathering supportive "evidence," but never ran a
direct query confirming D against the data; the correct answer was `ABE`, and
`check_option_b` failed (1 of 6 checks). Its shape check ("row_count=1, column_count=1,
value ABDE") was a false-green because shape says nothing about which letters are right.

The seed solver has no rule for how to construct an answer-style deliverable, so it assembles
the answer from plausibility and narrative evidence rather than a decisive per-option query.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation instruction — *for analysis/answer-style deliverables (e.g. selecting which
statements are true, or a single derived conclusion), back each component of the answer with
its own explicit query against the data: include an option only if a direct query confirms
it, and exclude it if the query refutes it; do not include or drop an option based on reading
model logic or plausibility alone* — will flip `f1011` by forcing a confirming/refuting query
per option (which would have dropped D), raising `stratified_pass_at_1` above the `@baseline`
0.6458.

This is the independent-evidence idea (surviving direction #1) applied to a categorical answer
rather than a numeric reconcile — distinct from h0012 (numeric/row-count recompute). It is
generative (how to build the answer), not a self-anchored re-derivation: each option is tested
against the raw data, not against the solver's prior reasoning. One idea, one stage
(Implementation). NOTE: this targets a single failure, so its expected full-run delta is
small; it is filed for completeness of the cluster, not as a high-leverage bet.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact (local data only — no public fetch, no oracle, no
reference to hidden `AUTO_*`/`check_option_*`/verifier tests).

Target datasets (smoke, all `ade-bench-` prefixed): the analysis-answer failure —
`ade-bench-f1011` — plus stable-`@baseline`-pass regression sentinels `ade-bench-f1007`,
`ade-bench-f1004` (f-series passes that exercise the same solver path without being
answer-style).

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0014-implementation-per-claim-evidence.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Implementation` (the single per-claim-evidence rule), leaves
Exploration/Validation/Finalization and the dependency/package guardrails untouched, and does
not reference hidden `AUTO_*`/`check_option_*`/`solution__*`/verifier tests or weaken the
leak-guard. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on `f1011` + the 2 f-series sentinels, the variant must not regress the
sentinels and should flip `f1011` to a pass before promotion to full.

## Gatekeeper review

**Recommendation: APPROVE** — single Implementation-stage idea, leak-guard byte-identical, full spec differs only in the two allowed fields, idea is generative-but-GATED to answer-style deliverables so no cross-family canary panel is required (G8 N/A).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-04). Reviewed 2026-06-05T09:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff` is one hunk `63a64,81` falling inside `## Stage: Implementation`; 0 `## Stage:` headers in the diff; one idea (per-option confirming/refuting query for answer-style deliverables). |
| G2 leak-guard intact | PASS | Added lines grep clean for `AUTO_`/`solution__`/`check_option`/`verifier`/`equality test`/`expected output seed`/`curl`/`wget`/`git clone`/`ls-remote` (NONE FOUND); README lines 1-48 (leak-guard + dependency/package guardrails) byte-identical to parent. |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0014-...yaml` = only `experiment:` (line 2) + `solver_workflow:` (line 11); `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff` full→smoke adds only `benchmark.tasks` (`ade-bench-f1011`, `ade-bench-f1007`, `ade-bench-f1004`); all `ade-bench-`-prefixed; includes the named target f1011; sentinels f1007+f1004 present (no WARN). |
| G5 both frozen | PASS | `specs/h0014-...frozen.yaml` and `...smoke.frozen.yaml` both exist; frozen full carries `kind: spacedock_solver` (l4) + `runtime: codex` (l5). |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim verbatim in spirit: Implementation stage, "back each component of the answer with its own explicit query… include only if a direct query confirms it, exclude if it refutes it; do not include/drop on plausibility alone." Generative/independent (query the raw data per option), not self-anchored re-run of own output. |
| G7 actionability/inert-risk | PASS | Carries a worked-example SQL skeleton (one confirming/refuting query per option, decide by result, assemble from confirmed-only) the solver can copy rather than re-derive — the worked-example form G7 prefers, not abstract structural prose. |
| G8 regression-canary coverage | N/A | Instruction is GATED: it fires ONLY on analysis/answer-style deliverables (multi-option pick or single derived conclusion), not on every dbt task. Not generative → no cross-family canary panel required; targets+sentinels sufficient. |

**For the captain:** Single GATED answer-style lever targeting the lone f1011 tail (baseline 0/6, included unverified option D). No FAILs; G8 N/A by gating. Expected full-run delta is small by design (one failure) — file/run for cluster completeness, not as a high-leverage bet. Smoke is a 3-task set (~27 min ETA).

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: README diff touches ONLY `## Stage: Implementation` (adds the single per-claim-evidence rule for analysis/answer-style deliverables); leak-guard intact; Exploration/Validation/Finalization + guardrails untouched; no hidden-test references.
  `diff` = one hunk `63a64,81` inside Implementation; 0 `## Stage:` headers in diff; leak-guard lines 1-48 byte-identical; forbidden-token grep on added lines = NONE.
- DONE: Both specs frozen; FULL spec differs from baseline ONLY in `experiment:` + `solver_workflow:`; smoke adds ONLY `benchmark.tasks` = [f1011 target, f1007 + f1004 sentinels]; GATED (answer-style only) = not generative, so no G8 canary panel required (recorded in gatekeeper block).
  `diff specs/baseline.yaml ...h0014.yaml` = 2 fields; smoke diff = benchmark.tasks only; both `.frozen.yaml` written with kind/runtime preserved.
- DONE: Gatekeeper review block written: per-rule PASS/WARN/FAIL table + overall APPROVE + one-line rationale; G8 N/A "not generative, targets+sentinels sufficient".
  8/8 rules scored, no FAILs; recommendation APPROVE.

### Summary

Forked `@baseline` solver (codex-ade-dbt-minimal) into `h0014-implementation-per-claim-evidence`,
adding one Implementation-stage rule: for analysis/answer-style deliverables, back each answer
component with its own confirming/refuting query and include only options a direct query confirms.
Single README change is the only independent variable; full spec differs only in `experiment:` +
`solver_workflow:`; smoke spec adds f1011 (target, baseline 0.0) + f1007/f1004 (sentinels, baseline
1.0). Both specs frozen. Lever is GATED to answer-style tasks (not generative) so no cross-family
canary panel is required. Gatekeeper review applied per guideline: APPROVE, no FAILs, G8 N/A. Smoke
NOT run per assignment.
