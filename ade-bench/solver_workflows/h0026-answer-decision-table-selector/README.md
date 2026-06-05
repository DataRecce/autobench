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

## Protocol: Answer Decision Table Selector (answer-style tasks only)

This workflow uses a multi-candidate answer protocol that is **gated to
answer-style tasks** — tasks whose deliverable is a committed answer string
choosing among a fixed set of listed options (for example "which of the
following IDs / categories / segments qualify"), where the instruction lists
the candidate options and the answer is the subset that satisfies a stated
condition. A task is answer-style only when the instruction itself enumerates
the options and asks you to commit the qualifying subset as the answer.

For any task that is NOT answer-style — repairs, model creation,
refactor/config, no-op, or any task whose graded artifact is dbt model SQL
rather than a committed answer subset — ignore this protocol entirely and solve
exactly as the per-stage instructions below describe. Do not add candidate
generation, decision tables, or selection behavior to non-answer tasks; their
solve path and committed artifact must be byte-for-byte what they would be
without this protocol.

When the task IS answer-style, run the two-phase candidate-and-select protocol:

1. **Generate N >= 3 independent candidate answers.** For each candidate,
   re-derive the answer from scratch from the local workspace — do not copy a
   prior candidate's reasoning. Each candidate must produce, before committing
   its answer, a **per-option decision table** with exactly one row per option
   the instruction lists, and these columns:
   - option label (verbatim from the instruction);
   - the local file/relation inspected for this option (a model, source,
     staging relation, seed, or compiled artifact);
   - the exact local check run or read (the dbt/SQL query or row read, with its
     observed result);
   - the IN / OUT decision for the option;
   - a one-line reason tied directly to that local check;
   - the candidate's final answer string, mechanically transcribed from the
     ordered IN rows.
2. **Select one candidate with a local, mechanical scorer.** Score every
   candidate using only the task instruction, the local model SQL, local
   source/staging/seed data, installed packages under `dbt_packages/`, and the
   candidate's own committed artifacts. Prefer the candidate whose table is most
   complete and most mechanically supported, by these tie-broken criteria:
   - **completeness** — every listed option has a row; no option is omitted;
   - **local support** — every IN decision cites a concrete local check whose
     observed result supports IN; an IN row with no supporting local evidence
     disqualifies the candidate;
   - **no contradiction** — no row's decision contradicts the local evidence in
     its own reason cell or in another candidate's check of the same option;
   - **exact transcription** — the committed answer string is exactly the
     ordered IN rows of the chosen table, with no option added, dropped, or
     reordered relative to the table.
   Reject a candidate that answers from narrative plausibility, omits a listed
   option, marks an option IN without local support, or commits a string that
   does not match its own table — even if its dbt project builds green.
3. **Commit only the selected candidate's answer** as the graded artifact, and
   save the chosen decision table and the rejected candidates' tables as stage
   notes (under `/razorback-freeze` if present) for resume/debug context. The
   selection uses no hidden verifier output, no public answer, no web lookup,
   and no LLM-as-oracle judgement of correctness — only the local checks above.

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
