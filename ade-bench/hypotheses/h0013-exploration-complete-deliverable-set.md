---
id: h0013
title: Exploration — enumerate the COMPLETE set of required deliverable models up front; a green compile is not evidence they exist
status: hypothesis
kind: hypothesis
source: concept-resolve-uncovered-false-greens fan-out; evidence re-audit of @baseline (622bdedac572b479, 31/48). Cluster "incomplete deliverable set / stopped at compile-green" — quickbooks001 built only quickbooks__general_ledger and never built the 3 stg_quickbooks__* staging models the oracle grades (6/12 checks failed); ana-eng007-medium also left graded models unbuilt. h0009 flagged this as a "fix-it-task completeness lever" deferred to a later hypothesis. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-04T13:40:51Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The re-audit confirmed `quickbooks001` fails for a reason no other lever addresses: the task
is framed "the project is erroring — fix it," and the solver fixed the one visible compile
error, the full project built green (`PASS=172`), and it **stopped** — it never built the 3
`stg_quickbooks__estimate` / `…__refund_receipt` / `…__sales_receipt` staging models that the
hidden `AUTO_stg_quickbooks__*_{equality,existence}` tests actually grade (6 of 12 checks
failed on models that were never created). Its self-check validated the wrong scope
(`quickbooks__general_ledger` in isolation) and read "172 models built" — which mostly counts
pre-installed `dbt_packages/` package models — as done. `ana-eng007-medium` shows the milder
form: it validated only `fact_purchase_order` and left `dim_products` / `fact_inventory` /
`obt_product_inventory` untested and wrong.

The seed solver's Exploration prose says "inspect the task instruction … models … schema YAML"
and Implementation says "make the smallest task-relevant change," but nothing tells the solver
to enumerate the **full deliverable set** — so in a fix-it task a green compile of the existing
project reads as completion even when required models are missing entirely.

**Falsifiable claim (the single README change — Exploration stage only):** adding one
Exploration instruction — *identify the COMPLETE set of models the task requires as
deliverables before editing: read the task statement for every named or implied model, and
cross-check `schema.yml` and any installed package's staging set for models that are
declared/expected but not yet present; in "the project is erroring / fix it" tasks, a green
compile of the existing project is NOT evidence the deliverables exist — a required model may
be missing entirely; record each required deliverable and ensure every one is built* — will
flip `quickbooks001` (and help `ana-eng007-medium`) by making the solver build the full set of
graded models, raising `stratified_pass_at_1` above the `@baseline` 0.6458.

Generative/up-front (the report's surviving direction #2 — fix the understanding before the
wrong/absent model is the answer). Distinct from h0009 (reproduce a package's *conventions* in
models you author) — this is about *which* models must exist at all, including ones a green
build silently leaves missing. One idea, one stage (Exploration).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact (task statement + local schema/package manifests
only — no public fetch, no oracle, no reference to hidden `AUTO_*`/`solution__*` tests).

Target datasets (smoke, all `ade-bench-` prefixed): the incomplete-deliverable failures —
`ade-bench-quickbooks001`, `ade-bench-ana-eng007-medium` — plus stable-`@baseline`-pass
regression sentinels `ade-bench-quickbooks002`, `ade-bench-quickbooks003`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0013-exploration-complete-deliverable-set.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Exploration` (the single complete-deliverable rule), leaves
Implementation/Validation/Finalization and the dependency/package guardrails untouched, and
does not reference hidden `AUTO_*`/`solution__*`/verifier tests or weaken the leak-guard.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on the 2 targets + the 2 quickbooks sentinels, the variant must not regress
the sentinels and should flip at least `quickbooks001` to a pass before promotion to full.

## Smoke result

## Run result

## Behavioral analysis

## Verdict
