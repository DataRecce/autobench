---
title: Build-and-verify discipline — eliminate the dominant build-error failure class
status: concept
kind: concept
source: captain hunch from h0000-baseline analyze (build-error = 27/39 failures, 69%)
started:
completed:
verdict:
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
