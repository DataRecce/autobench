---
id: h0011
title: Implementation — emit the full expected output column set (from the local contract), don't drop columns the upstream/schema declares
status: propose
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

## Stage Report: propose

- [x] DONE: Forked the `@baseline` solver dir.
  `cp -r solver_workflows/codex-ade-dbt-minimal solver_workflows/h0011-implementation-full-column-set`.
- [x] DONE: Edited ONLY the `## Stage: Implementation` section of the forked README — appended the single full-column-set paragraph at the end of the stage prose (after "Do not remove `dbt_packages/` …", before `## Stage: Validation`). No other stage or guardrail touched; no hidden-test reference.
- [x] DONE: Created the FULL spec `specs/h0011-implementation-full-column-set.yaml` from `baseline.yaml`, changing only `experiment:` and `solver_workflow:`.
- [x] DONE: Created the smoke spec `specs/h0011-implementation-full-column-set.smoke.yaml` from the full spec, adding only `benchmark.tasks` (ana-eng004, f1002, ana-eng007-medium + ana-eng008 sentinel, ade-bench- prefixed).
- [x] DONE: Froze both via `rk freeze --allow-missing`. `specs/h0011-implementation-full-column-set.frozen.yaml` and `...smoke.frozen.yaml` written; both retain `kind: spacedock_solver` + `runtime: codex`. Smoke frozen carries the 4 tasks; full frozen has `tasks: null`.
- [x] DONE: Set frontmatter `status: hypothesis -> propose`.

### Evidence diffs

`diff specs/baseline.yaml specs/h0011-implementation-full-column-set.yaml`:

```diff
2c2
< experiment: ade-bench-baseline # variants: ade-bench-h0001-<slug>
---
> experiment: ade-bench-h0011-implementation-full-column-set # variants: ade-bench-h0001-<slug>
11c11
<   solver_workflow: ./solver_workflows/codex-ade-dbt-minimal # variants repoint to ./solver_workflows/h<NNNN>-<slug>
---
>   solver_workflow: ./solver_workflows/h0011-implementation-full-column-set # variants repoint to ./solver_workflows/h<NNNN>-<slug>
```

`diff solver_workflows/codex-ade-dbt-minimal/README.md solver_workflows/h0011-implementation-full-column-set/README.md`:

```diff
63a64,70
> When building or extending a model, derive its output column set from the local
> contract — the columns of the upstream/source tables it selects from, the model's
> `schema.yml` entries, and any sibling model of the same family — and emit every
> column that contract implies; never drop columns the upstream model or schema
> already declares. For "one big table"/wide models, carry through all columns from
> each joined source rather than a hand-picked subset.
>
```

### Summary

Forked the @baseline solver and added exactly one `## Stage: Implementation` rule (derive the full output column set from the local contract; carry through all joined-source columns for wide/OBT models). The full spec differs from baseline only in `experiment:` + `solver_workflow:`; the smoke spec adds only `benchmark.tasks` for the 3 missing-column targets plus the ana-eng008 sentinel. Both specs frozen cleanly with `kind: spacedock_solver` and `runtime: codex` preserved. Gatekeeper not run (dispatched separately); no `rk run` invoked.

## Gatekeeper review

**Recommendation: APPROVE** — no FAILs; the single Implementation-stage column-set rule is generative/local-signal-only with the spec scope, leak-guard, and frozen artifacts all clean; the one open concern is inert-risk (G7), advisory only.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-04). Reviewed 2026-06-04T15:50:07Z.

Fork parent resolved: hypothesis `source:` names `solver_workflows/codex-ade-dbt-minimal`; `rk registry resolve run @baseline` → `runs/ade-bench-baseline/622bdedac572b479`, whose `spec.frozen.yaml` carries `solver_workflow: solver_workflows/codex-ade-dbt-minimal`. Source and registry agree → parent = `solver_workflows/codex-ade-dbt-minimal`.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is a single hunk `63a64,70` (6 prose lines + 1 blank). Line 63 sits inside `## Stage: Implementation` (header @50, `## Stage: Validation` @71); no other stage header in the diff. One idea added (derive full output column set from local contract). |
| G2 leak-guard intact | PASS | `diff` of README lines 1–32 (leak-guard + dependency/package guardrails) byte-identical (`LEAKGUARD-IDENTICAL`). Grep of added `>` lines for `AUTO_/solution__/check_option_/verifier/equality test/expected output seed/curl/wget/git clone/git ls-remote/download/fetch/web/oracle/drive…zero/re-run/compare` returned no matches. |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0011-...yaml` shows only `experiment:` (line 2) and `solver_workflow:` (line 11). `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved in the full spec. |
| G4 smoke tasks-only | PASS | `diff full smoke` adds only `benchmark.tasks` (`23a24,28`): `ade-bench-ana-eng004`, `-f1002`, `-ana-eng007-medium`, `-ana-eng008` — all `ade-bench-` prefixed, covering all 3 hypothesis targets + sentinel. No WARN: sentinel `ana-eng008` passes `@baseline` (reward 1.0); the 3 targets are baseline failures (reward 0.0). |
| G5 both frozen | PASS | `ls` confirms both `…frozen.yaml` (1711B) and `…smoke.frozen.yaml` (1808B) exist. Both carry `kind: spacedock_solver` (@4) and `runtime: codex` (@5). Full frozen `tasks: null`; smoke frozen carries the 4 tasks. |
| G6 resolver fidelity | PASS | Inserted text ("derive its output column set from the local contract — upstream/source columns, `schema.yml`, sibling models — and emit every column that contract implies; never drop columns…; for wide/OBT models carry through all columns from each joined source") matches the Falsifiable claim verbatim in stage and idea. Generative + independent local signals; no self-anchored "re-run/compare to existing/drive to zero" dead-family phrasing. |
| G7 actionability/inert-risk | WARN | Instruction classified **abstract-structural**: it directs *which* columns to emit and to widen the SELECT/projection from the contract, stated as prose with no worked-example SQL skeleton and no named mechanical edit (cast/literal/filter). On this `@baseline`, projection/structure prose has been behaviorally inert ("talks but doesn't do"). Suggest a few-shot before→after skeleton showing the full-width SELECT to pattern-match. |

**For the captain:** No integrity FAILs — leak-guard, spec scope (two fields), and fidelity are all clean, so nothing blocks advancing to `smoke`. The one flag is G7 inert-risk: the column-set rule is abstract-structural prose without a worked example, the inert family on this baseline; consider asking the ensign to add a literal before→after SELECT skeleton before/after the smoke run, and watch whether the committed SQL actually widens the projection (not just the transcript).
