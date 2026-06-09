# Codex ADE dbt Minimal Workflow

Work in the task workspace as delivered by the benchmark harness. Do not clear
proxy environment variables or treat public-network access as a source-code fix.
The benchmark instruction is appended below these workflow instructions. The
graded artifact is the final dbt project source state; do not create an answer
file unless the task explicitly asks for one.

Do not fetch public reference material while solving. This includes `curl`,
`wget`, `git clone`, `git ls-remote`, package-source downloads, browser or web
lookup of upstream projects, and searches for published solutions. Use only the
local task workspace: installed packages, `dbt_packages/`, package manifests,
compiled artifacts, logs, macros, models, seeds, profiles, and project data.

Preserve existing dbt dependencies, package files, profiles, seeds, and macros
unless the task explicitly requires changing them. Hidden verifier tests may
depend on the existing project structure and package namespaces.

It is acceptable to run `dbt deps` for setup and validation when `packages.yml`
or `package-lock.yml` declares dependencies and `dbt_packages/` is absent.
Preserve any `dbt_packages/` directory already present at task start; the
verifier may reuse image-installed dependencies without registry access. Treat
`target/` and `logs/` as generated scratch state. Do not rewrite `packages.yml`,
`package-lock.yml`, package namespaces, profiles, or dependency macros unless the
task explicitly requires that change. In particular, never replace `dbt_utils`
or another declared package with a partial local shim; hidden verifier tests may
call package macros such as `dbt_utils.test_equality` even when visible models
only use one helper macro.

If `/razorback-freeze` exists and has exactly one child directory, write concise
stage notes there as `exploration.md`, `implementation.md`, and `validation.md`.
These notes are for resume/debug context; they are not the graded artifact.

## Stage: Exploration

Before editing, inspect the task instruction, project guidance files,
`dbt_project.yml`, `profiles.yml`, `packages.yml`, `package-lock.yml`, models,
macros, seeds, schema YAML, and existing logs.

Run cheap baseline probes when useful, such as `dbt compile --profiles-dir .`,
targeted `dbt run`, targeted `dbt test`, or log inspection. If a baseline probe
fails because declared packages are missing, run `dbt deps` before interpreting
the project as broken. For data-correctness tasks, sample relevant source tables
and current model outputs: row counts, nulls, duplicates, key distributions, and
representative rows.

Record suspected task type, affected files/models, baseline errors, and useful
data observations before making project changes.

## Stage: Plan Review (independent re-derivation — rejects only a locally-visible contradiction, else proceeds unchanged)

Before any SQL edit, do one **independent re-derivation** pass. The goal is to decide whether
the model SQL you start with provably contradicts the task's intent in a way you can see from
**local relations alone** — and if so, to record that contradiction — while otherwise leaving
the build EXACTLY as it would have been. This stage is **single-path**: it reviews the one
build path once against an external invariant; it does **not** generate or score multiple
candidate answers, and it **selects nothing**.

State, verbatim, this generic leak-clean grain invariant and use it as your external yardstick:

> A model's grain entity comes from its canonical source relation, never from a pre-filtered
> child; a completeness/repair output must keep every key the consumer relies on.

Then run the re-derivation in three steps:

1. **RE-DERIVE (independently).** From only (a) the task instruction, (b) the **existing** model
   SQL already in the project, and (c) the generic invariant above, derive in a deliberately
   separate pass what the intended **grain entity and key set** should be — which source
   relation the grain entity must come from, and which keys the downstream consumer relies on.
   Derive this fresh from the instruction and the invariant; do **not** reverse-infer the
   intended grain by reading it back off the existing code or its current output — reverse-
   inference just re-states whatever the code already does and cannot catch a bug.
2. **COMPARE.** Compare that independent re-derivation to what the existing code **actually
   does** (which source relation it grains from; which keys survive end-to-end). Confirm the
   contradiction, if any, using only **local relations** you can read directly — the raw
   `{{ source(...) }}` relations, row/key counts, and key-level anti-joins between the source
   key set and the relation the grain governs.
3. **DECIDE — emit a verdict.** Emit `verdict: "REJECT"` **only** when the existing code
   provably contradicts the re-derivation in a way **visible from local relations** — for
   example it grains the model on a **pre-filtered child** relation and the downstream consumer
   never restores the dropped keys, so the keys are lost end-to-end and a local anti-join shows
   the gap. Record a one-sentence `reason` and the `contradicting_line` (the specific line of
   the existing SQL that contradicts the re-derivation). **Otherwise** — including the common
   case where the intended grain **cannot be pinned from local relations** because the
   discriminating fact lives downstream (e.g. a child's missing keys are restored later by a
   `LEFT JOIN … coalesce(...)` spine, or a relation is re-correlated through a status/active
   flag, or the difference would only show after an operation the local relations don't carry)
   — emit `verdict: "PROCEED_UNDETERMINED"`. When you cannot decide the contradiction from
   local relations, you MUST emit `PROCEED_UNDETERMINED`; do not guess REJECT.

The verdict is a **record, not a gate or a build mandate.** On `PROCEED_UNDETERMINED` you build
EXACTLY as you would have without this stage — same smallest task-relevant change, same FROM,
same join direction, same grain. This stage adds **no** "build to satisfy the verdict" rule:
even on `REJECT` it only records the contradiction; you still make the smallest task-relevant
change in Implementation as usual, now informed by the recorded reason. You must **not** revert,
rewrite, re-select, invert a join, or hold back any committed model merely to make it agree with
this verdict. The verdict never invents a contract for the code to be built to.

Emit exactly this record and **nothing else** from this stage:

```json
{
  "intended_grain": "<the re-derived grain entity + key set, one phrase>",
  "code_does": "<what the existing SQL actually grains on / which keys survive, one phrase>",
  "verdict": "<REJECT | PROCEED_UNDETERMINED>",
  "reason": "<one sentence; for PROCEED_UNDETERMINED, name the downstream restore/flag that makes the contradiction not locally decidable>",
  "contradicting_line": "<the existing-SQL line that contradicts the re-derivation, or null when PROCEED_UNDETERMINED>"
}
```

Routing — make the write **unconditional** and **durable**, and do NOT depend on
`/razorback-freeze` having any particular layout. Write the JSON to the fixed scratch path
`/tmp/plan_review.json` (always, with no precondition), and then **print the file's contents to
standard output** so the full record is captured in your session transcript — for example:

```
apply_patch  # create /tmp/plan_review.json with the JSON above
cat /tmp/plan_review.json
```

`/tmp/plan_review.json` is a scratch file outside the dbt project; it is **not** the graded
artifact and is not part of the final project source state that is scored. The authoritative
copy is the one printed to stdout (it survives in the session record even though the container
scratch is discarded). This stage **records only** — it does **not** decide which SQL you write,
and the build proceeds EXACTLY as it otherwise would. Then continue to Implementation unchanged.

## Stage: Implementation

Classify the task locally as no-op, repair, creation, refactor/config, or mixed.
Make the smallest task-relevant dbt project change, following local naming,
materialization, source, ref, macro, and schema patterns.

Run basic confirmation as part of implementation. Use the cheapest command that
proves the edited area compiles or builds: `dbt compile`, targeted `dbt run`,
targeted `dbt test`, or selected `dbt build`. Fix build/compile errors caused by
your change before moving on. Build outputs can remain scratch state during
validation, but remove `target/` and `logs/` before finalizing unless the task
explicitly requires them. Do not remove `dbt_packages/` when it existed at task
start.

## Stage: Validation

Do additional correctness checks beyond "it builds".

For repairs, confirm the original failure mode is gone and the affected output
matches the source-data expectation. For refactors/config changes, check row
counts, schemas, and value-level behavior for affected and downstream models.
For new models or analysis tasks, check required columns, grain, uniqueness,
null behavior, row counts, and representative rows against source data. For
no-op tasks, confirm no project change was needed and leave files untouched.

Run broader dbt validation when practical for the task scope.

## Stage: Finalization

Leave only intended project changes. Remove scratch files unless the dbt project
requires them. Finish with changed files and concise validation evidence.
