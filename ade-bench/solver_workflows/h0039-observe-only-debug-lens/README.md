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

## Stage: Observe (debug lens — observe-only, changes nothing)

This stage is **observe-only**. It produces a written reasoning record and changes
**no project SQL, config, or files** under the dbt project. It is **not a gate** and
carries **no "build to satisfy" mandate**: after writing the record you build EXACTLY as
you would without this stage. The record exists only so a later reader can see, in
machine-readable form, what mental model you held at build time; it never constrains,
selects, or revises what you commit.

Always run this stage. For each model the task asks you to author, restructure, or repair,
write down your at-build-time understanding — your `Contract:` / `divergence` notes:

1. **Grain** — what one row is, and which key set you believe must be present.
2. **Columns** — the full set you intend to emit, in order.
3. **Types** — the type you intend for each column.
4. **Divergence** — anything you are unsure about, any place your plan might depart from
   what the task seems to want, and the source you read to decide it.

Write the record to the sanctioned non-graded notes location, not into the dbt project:
if `/razorback-freeze` exists and has exactly one child directory, write
`plan_review.json` there (alongside the `exploration.md` / `implementation.md` /
`validation.md` notes). Use **on-disk `apply_patch`** to create the file — do not merely
discuss the record in your reasoning; the artifact must exist on disk. Use a structure such
as:

```json
{
  "models": [
    {
      "name": "<model>",
      "grain": "<one row per …>",
      "key_count_observed": <N>,
      "columns": ["…"],
      "types": {"…": "…"},
      "divergence": "<what you are unsure of, or 'none'>"
    }
  ]
}
```

To populate `key_count_observed`, run **at least one `dbt show` key-count probe per model**
you record (e.g. `dbt show --inline "select count(distinct <key>) from {{ ref('<model>') }}"`,
or against the upstream relation when the model is not yet built) and copy the number into
the record. These probes are read-only observations; they change nothing you commit.

This record is for resume/debug context only. It is **not the graded artifact**, it does
**not** decide which SQL you write, and you must **not** rewrite, re-select, or hold back any
committed model to make it agree with the record. Then proceed to Implementation exactly as
you otherwise would.

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
