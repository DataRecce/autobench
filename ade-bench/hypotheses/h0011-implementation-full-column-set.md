---
id: h0011
title: Implementation — emit the full expected output column set (from the local contract), don't drop columns the upstream/schema declares
status: hypothesis
kind: hypothesis
source: concept-resolve-uncovered-false-greens fan-out; evidence re-audit of @baseline (622bdedac572b479, 31/48). Cluster "missing output columns" — 3 failures (ana-eng004, f1002, ana-eng007-medium) where AUTO_*_equality ERRORs "has less columns than solution__<model>". Distinct from the report's named modes (not value-divergence, not grain). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-04T13:40:51Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The evidence re-audit found **3 of the 12 uncovered `@baseline` failures share one root
cause**: the solver builds or extends a model with **fewer output columns than the
deliverable requires**, so the hidden `AUTO_<model>_equality` test fails at compile with
"has less columns than `solution__<model>`" — not a value mismatch, a *width* mismatch.

- `ana-eng004` (`AUTO_obt_product_inventory_equality` ERROR "less columns"): built the OBT
  with a hand-picked subset of columns instead of carrying every column from the joined
  sources.
- `f1002` (`AUTO_most_podiums_equality` ERROR "less columns"): the new `most_podiums` model
  omitted columns present in the expected output; the solver "checked" only its own
  `schema.yml`, which was already too narrow.
- `ana-eng007-medium` (`AUTO_dim_products_equality` + `AUTO_obt_product_inventory_equality`
  both ERROR "less columns"): same width gap on two models.

The seed solver's Implementation prose says "make the smallest task-relevant change following
local patterns" but gives no rule for choosing a model's **output column set**, so the solver
emits the minimum it reasons it needs.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation instruction — *when building or extending a model, derive its output column
set from the local contract (the columns of the upstream/source tables it selects from, the
model's `schema.yml` entries, and any sibling model of the same family) and emit every column
that contract implies; never drop columns the upstream model or schema already declares; for
"one big table"/wide models, carry through all columns from each joined source rather than a
hand-picked subset* — will flip the missing-column failures (ana-eng004, f1002,
ana-eng007-medium) to passes by producing the full expected schema width, raising
`stratified_pass_at_1` above the `@baseline` 0.6458.

Generative (how to write the model), uses only local signals (sources, schema YAML, sibling
models). Distinct from h0009 (copy installed package conventions) and h0010 (grain spine):
those govern rows/grain, this governs the column set. One idea, one stage (Implementation).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact (local contract only — no public fetch, no oracle,
no reference to hidden `AUTO_*`/`solution__*` tests).

Target datasets (smoke, all `ade-bench-` prefixed): the 3 missing-column failures —
`ade-bench-ana-eng004`, `ade-bench-f1002`, `ade-bench-ana-eng007-medium` — plus a
stable-`@baseline`-pass regression sentinel `ade-bench-ana-eng008`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0011-implementation-full-column-set.yaml` shows
only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Implementation` (the single column-set rule), leaves
Exploration/Validation/Finalization and the dependency/package guardrails untouched, and does
not reference hidden `AUTO_*`/`solution__*`/verifier tests or weaken the leak-guard.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on the 3 targets + `ana-eng008` sentinel, the variant must not regress the
sentinel and should flip at least one of the 3 missing-column failures to a pass before
promotion to full.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
