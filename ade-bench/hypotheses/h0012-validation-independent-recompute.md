---
id: h0012
title: Validation — reconcile one key figure (and row count) against an INDEPENDENT derivation from raw source, never against your own re-run
status: hypothesis
kind: hypothesis
source: concept-resolve-uncovered-false-greens fan-out; evidence re-audit of @baseline (622bdedac572b479, 31/48). The heavyweight cluster — 6 value-divergence false-greens (ana-eng006, ana-eng007, airbnb007, asana005-hard, f1006, airbnb009). This is the ONLY proven lever (the f1007-hard catch worked solely because it compared an independent number). The dead part is *self-anchored* checks, not the Validation stage itself (per docs/baseline-validation-self-anchored-false-green.md §4). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-04T13:40:51Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The baseline false-green finding established that the only self-check that ever caught a real
bug (`f1007-hard`) worked **solely because it compared against an independent number** — the
raw `results` table counted a structurally different way (3,373 vs the season-table sum
3,372). Every other check was self-anchored and confirmed the solver's own wrong derivation.
The re-audit confirms the largest uncovered cluster is exactly this shape:

- `ana-eng006`, `ana-eng007` (`AUTO_dim_products_equality`, `Got 5`): 5 row-level **value**
  mismatches; the solver only ran `dbt run`/spot-checks, never recomputed the values.
- `airbnb007` (`daily_agg_nps_reviews_equality_with_tolerance`, `Got 4`): 4 value mismatches;
  validated NPS ranges and row counts (shape), not values.
- `asana005-hard` (`AUTO_int_asana__project_user_agg_equality`, `Got 3`): refactor diverges;
  the self-check (`mismatch_count=0`) compared the refactor to its **own** re-derivation.
- `f1006` (`AUTO_constructor_points_equality`, `Got 2`): summed **all** cumulative season
  rows instead of the final standing (11–22× overstated); the solver even *observed* the
  discrepancy, then "validated" by re-running its own build without an independent recompute.
- `airbnb009` (`mom_agg_review_date_range`, `Got 1`): a continuous-spine fix over-produced
  rows (13,524 vs the expected 12,278) — an independent **row-count** recompute from source
  grain would have caught it.

The seed solver's Validation prose says "do additional correctness checks beyond it builds"
and "match the source-data expectation," but the solver operationalizes this by re-running its
own model or comparing to the pre-existing code — which shares the bug's blind spot.

**Falsifiable claim (the single README change — Validation stage only):** adding one
Validation instruction — *when validating a numeric result, reconcile at least one key figure
against an INDEPENDENT derivation computed straight from the raw source tables by a
structurally different path (a different join order/grain, or a coarser source-level count),
and reconcile the model's row count against the count implied by its declared grain on the
raw source; treat any disagreement as a real defect to root-cause and fix; do NOT "validate"
by re-running your own model or comparing to the pre-existing code, because a check that
reuses your own derivation shares its blind spot* — will catch the value-divergence and
wrong-row-count failures (ana-eng006/007, airbnb007, asana005-hard, f1006, airbnb009) and let
the solver fix them, raising `stratified_pass_at_1` above the `@baseline` 0.6458.

This is the report's surviving direction #1 (independent invariant) stated as a generic
Validation rule — NOT the dead self-verification family (h0006/h0007/h0008), which compared
against the solver's own re-derivation. The distinguishing instruction is the explicit ban on
self-anchored re-runs and the demand for a structurally different derivation path. One idea,
one stage (Validation).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact (raw local source tables only — no public fetch, no
oracle, no reference to hidden `AUTO_*`/`solution__*` tests).

Target datasets (smoke, all `ade-bench-` prefixed): a representative spread of the cluster —
`ade-bench-ana-eng006`, `ade-bench-airbnb007`, `ade-bench-f1006`, `ade-bench-airbnb009` —
plus a stable-`@baseline`-pass regression sentinel `ade-bench-airbnb001`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0012-validation-independent-recompute.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Validation` (the single independent-recompute rule), leaves
Exploration/Implementation/Finalization and the dependency/package guardrails untouched, and
does not reference hidden `AUTO_*`/`solution__*`/verifier tests or weaken the leak-guard.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on the 4 targets + `airbnb001` sentinel, the variant must not regress the
sentinel and should flip at least one of the 4 value-divergence failures to a pass before
promotion to full.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
