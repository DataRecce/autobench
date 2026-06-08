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

## Stage: Triage ledger (observe-only — records a decision, changes nothing)

This stage is **observe-only**. It produces one machine-readable record and changes
**no project SQL, config, seed, schema, or files** under the dbt project. It is **not a
gate**, it **selects nothing**, and it carries **no "build to satisfy" mandate**: after
writing the record you build EXACTLY as you would without this stage. The record exists only
so a later reader can see, in machine-readable form, which load-bearing claim your edit will
rest on and whether the local workspace could decide it. It never constrains, reverts,
selects, or revises what you commit.

Always run this stage, on every task. First, in one sentence, state the single
**load-bearing claim** the task's correct output most depends on (the one quantity, grain,
mapping, column, or filter that, if read wrong, makes the output wrong). Then run this fixed
three-clause check on that claim, recording each clause's result as `true` (the claim is
decidable from that source) or `false`:

1. **instruction** — Does an explicit sentence in the task instruction name the deciding
   quantity for that claim (a stated grain, a named column/metric, an enumerated set, a
   threshold)? `true` if a sentence names it; otherwise `false`.
2. **schema_yml** — Does an **existing** `schema.yml` in the project (one already present at
   task start, not one you would add) name it — e.g. a declared column, a documented grain, or
   a declared test on the deciding key? `true` if present; otherwise `false`.
3. **raw_source_probe** — Reading **only the immutable raw `{{ source(...) }}` relation
   directly** (never a re-derived CTE or a model you rebuilt), can a conservation/coverage probe
   decide it? Run, read-only, a row **count** on the raw source and a **key-level anti-join**
   between the raw source key set and the relation the claim governs (e.g.
   `dbt show --inline "select count(*) from {{ source('<src>','<tbl>') }}"` and an
   `select count(*) from (<raw source keys> except <claim relation keys>)` style anti-join). The
   probe **decides** the claim only when the raw count and the anti-join are conclusive on their
   own (e.g. the anti-join is empty so coverage is total, or the raw count fixes the expected
   grain). `true` if the raw-source probe decides it; otherwise `false`. Read the immutable
   source only — a re-derived intermediate re-correlates with any model error and gives a false
   `true`.

Then set `would_abstain` to `true` if **all three** clause results are `false` (no local source
could decide the claim — it is oracle-only), and `false` otherwise. Emit exactly this record and
**nothing else** from this stage:

```json
{
  "claim": "<the single load-bearing claim, one sentence>",
  "clause_results": {
    "instruction": <true|false>,
    "schema_yml": <true|false>,
    "raw_source_probe": <true|false>
  },
  "would_abstain": <true|false>
}
```

Routing — make the write **unconditional** and **durable**, and do NOT depend on
`/razorback-freeze` having any particular layout. Write the JSON to the fixed scratch path
`/tmp/triage.json` (always, with no precondition), and then **print the file's contents to
standard output** so the full record is captured in your session transcript — for example:

```
apply_patch  # create /tmp/triage.json with the JSON above
cat /tmp/triage.json
```

`/tmp/triage.json` is a scratch file outside the dbt project; it is **not** the graded
artifact and is not part of the final project source state that is scored. The authoritative
copy is the one printed to stdout (it survives in the session record even though the container
scratch is discarded). This stage
**records only** — it does **not** decide which SQL you write, you must **not** revert,
rewrite, re-select, or hold back any committed model to make it agree with `would_abstain`, and
the build proceeds EXACTLY as it otherwise would. Then continue to Implementation unchanged.

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
