---
title: Build-and-verify discipline — eliminate the dominant build-error failure class
status: expanded
kind: concept
source: captain hunch from h0000-baseline analyze (build-error = 27/39 failures, 69%)
started: 2026-06-01T17:06:27Z
completed: 2026-06-01T17:14:03Z
verdict: PASSED
id: concept-build-and-verify
---

## Direction

**Theme.** Make the solver build-and-verify the full dbt graph — and resolve every
build error — *before* it declares a task done. The `h0000-baseline` analyze found the
dominant failure class is build-errors: **27 of 39 failures (69%)** never compile. dbt
raises `Runtime Error … Catalog Error: Table with name <X> does not exist` from unbuilt
or misnamed upstream relations, so **zero target tests even run** and the task scores a
hard 0. Exemplars: intercom001 (`stg_intercom__conversation_part_history`), ana-eng002
(`fact_inventory`), f1005 (`stg_f1_dataset__constructor_standings`), asana003
(`project_data`). This class wipes out intercom (3/3), most of f1 (13/16), and most of
ana-eng (7/10).

**Why it might raise the score.** The current `@baseline` solver README
(`codex-ade-dbt-minimal`) only *suggests* a build check — **Stage: Implementation** says
"Use the cheapest command that proves the edited area compiles or builds … Fix
build/compile errors caused by your change before moving on." That guidance is permissive
and scoped to "the edited area," so it does not force a clean *full-graph* build and the
solver ships graphs with dangling upstreams. A stronger, mandatory build-and-verify
discipline should convert many 0/N build-errors into at-least-runnable trials. Even a
partial conversion is valuable: it redistributes opaque hard-zeros into a readable
build-error → near-miss → pass spectrum that directs the next hypothesis.

**Candidate mechanisms for `ideate` to fan out** (the independent variable is ONLY the
solver README; each derived hypothesis changes ONE idea):

1. **Strengthen the existing Validation stage** — add an explicit build-and-verify
   instruction to **Stage: Validation**: run a full `dbt build` (or `dbt run` over the
   whole graph), treat any `Catalog Error: … does not exist` as unfinished work, and
   forbid finalizing until the graph builds with zero errors.
2. **Insert a dedicated build-gate stage** between **Stage: Implementation** and
   **Stage: Validation** — a "Build Gate" that must reach a zero-error full-graph build;
   on a build failure it routes *back to Implementation* (build the missing /
   correctly-named upstream) and re-gates. A bounded retry loop, not an open one.
3. Other framings `ideate` may surface — e.g. an explicit "resolve every dangling
   `ref()`/source before done" checklist; a compile-then-full-build ordering; or a
   pre-finalize full-graph build assertion folded into **Stage: Finalization**.

**Target datasets for eventual smoke** (build-error exemplars spanning groups):
`intercom001`, `f1005`, `ana-eng002`, `asana003`. Each hypothesis should also name a
near-miss control (e.g. `quickbooks003`) to watch the change does not regress
already-building tasks.

**Guardrails.** Each derived hypothesis keeps the solver README's no-external-reference /
leak-guard prose intact and changes exactly one idea; its variant spec differs from
`specs/baseline.yaml` only in `experiment:` + `solver_workflow:`.

## Stage Report: ideate

- DONE: Each hypothesis is ONE concrete, falsifiable solver-README change naming the specific Stage it edits and its target datasets — not a restatement of the concept.
  Four entities, each a single named-stage README edit with a falsifiable reject condition: h0001 (Stage: Validation — mandatory zero-error full build), h0002 (new Stage: Build Gate between Implementation and Validation, bounded build-fail→Implementation loop), h0003 (Stage: Implementation — ref()/source() resolution checklist), h0004 (Stage: Finalization — pre-finalize full-build assertion).
- DONE: The fan-out spans distinct mechanisms — the captain's two plus at least one alternative framing — not three variants of one idea.
  h0001 = captain mechanism 1 (strengthen Validation); h0002 = captain mechanism 2 (dedicated Build Gate stage with reject-back-to-Implementation); h0003 + h0004 are two distinct alternative framings (static ref/source resolution in Implementation; single terminal pre-finalize assertion in Finalization) that attack the same class without a mid-pipeline run-gate.
- DONE: Each hypothesis names concrete smoke target datasets from the baseline build-error set plus a near-miss control to watch for regression.
  All four name intercom001, f1005, ana-eng002, asana003 as smoke targets and quickbooks003 (baseline 12/14) as the non-regression control; reject conditions explicitly include quickbooks003 regression.

### Summary

Filed four hypothesis entities (h0001–h0004), each `status: hypothesis`, `kind: hypothesis`, `source: concept-build-and-verify fan-out`, following the README Hypothesis template (## Hypothesis = single named-stage README change + targets; ## Acceptance criteria AC-1/2/3). The independent variable in every entity is ONLY the solver README — no variant README or spec was authored here (that is propose). The fan-out covers both captain-mandated mechanisms (h0001 strengthen Validation; h0002 dedicated Build Gate stage with bounded build-fail→Implementation routing) plus two discovered alternative framings (h0003 static ref()/source() resolution checklist in Implementation, which uniquely catches naming mismatches like asana003's `project_data` without a build run; h0004 pre-finalize full-build assertion in Finalization, testing whether one terminal gate suffices). Each keeps the leak-guard / no-external-reference prose intact, changes exactly one idea, and is falsifiable against the build-error count on the four smoke targets with quickbooks003 as the regression control. Concept frontmatter status left unchanged for the first officer to advance concept → expanded.
