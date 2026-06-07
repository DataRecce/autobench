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

When you author a model that has a DECLARED column list — its entry in
`schema.yml` lists columns, or the task instruction explicitly names the columns
it must expose — reconcile your output against that declared list as a mechanical
set-difference, not against your own judgment of which columns matter. READ the
declared column names from `schema.yml`/the instruction (do not re-derive or
infer them from your own output), list the columns your model actually produces,
and compute `declared − produced`. For every declared column missing from your
output, ADD it, deriving its value from the appropriate source/analog relation —
the declaration is the contract, not your judgment. This reconcile is ADDITIVE
ONLY: add genuinely-missing declared columns; never DROP, RENAME, or rewrite a
column you already produce, and never add a column that is not in the declared
list. If a model has no declared column list, this rule does not apply — do not
invent a contract.

Worked example — reconcile produced against declared, add only the missing:
```text
# 1. READ the declared columns from schema.yml (or the instruction), verbatim:
#    declared = {product_id, product_name, category, on_hand_qty, unit_cost}
# 2. LIST the columns your model currently produces:
#    produced = {product_id, product_name, on_hand_qty}
# 3. DIFF — declared minus produced:
#    missing  = {category, unit_cost}
# 4. ADD only the missing declared columns, sourced from the right relation;
#    leave the already-produced columns exactly as they are.
```
```sql
-- BEFORE: produced is a subset of the declared contract
select product_id, product_name, on_hand_qty
from {{ ref('upstream') }}

-- AFTER: the two missing declared columns added (category, unit_cost);
--   nothing existing dropped, renamed, or rewritten; no undeclared column added
select product_id, product_name, on_hand_qty,
       category, unit_cost          -- the {declared − produced} difference
from {{ ref('upstream') }}
```

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
