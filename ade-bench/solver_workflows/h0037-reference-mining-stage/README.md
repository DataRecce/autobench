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

## Stage: Reference Mining

Run this stage whenever the task makes you author or restructure a model
(creation, refactor/config, or the model-building part of a mixed task). Skip it
for no-op tasks (change nothing) and for pure repairs whose fix is a single local
edit to an existing model (make the smallest fix and go to Implementation). When
it applies, do it BEFORE you write any model SQL — its job is to find an already-
correct local model of the same shape and reuse its construction verbatim, so you
copy a working skeleton instead of re-deriving one from scratch.

For each model you must deliver, mine a reference in three steps:

1. **Name the target's layer and grain.** State the model's directory/layer (e.g.
   `models/analytics_obt/`, `models/warehouse/`, the staging layer) and what one
   row is — the exact key column(s) the model is keyed on.

2. **Locate the closest already-passing in-project analog — own siblings FIRST.**
   Search the project's OWN models for the nearest sibling of the same kind that
   the project's dbt build already produces successfully — preferably a model in
   the SAME directory/layer with the same shape (e.g. another one-big-table model
   in `models/analytics_obt/` beside the one you are building, another fact in
   `models/warehouse/`, another staging model in the staging layer). Try the
   project's own passing siblings first and only fall back to an installed-package
   template (a model under `dbt_packages/`) of the same shape when the project has
   no same-layer sibling. The analog is local and non-graded — it encodes the
   project's authored construction convention, not the target's expected values.

3. **Record the analog and its construction.** Capture, from the analog's source,
   the four construction facts you will copy: (a) its **FROM relation** — the
   left-most `from` table it builds on; (b) its **join ladder** — each
   `left join` / `join` in order and the join key; (c) its **spine/key source** —
   which relation supplies the full key set the analog is keyed on (the table the
   others are joined ONTO); (d) its **window / group-by** — any `group by` keys or
   `over (...)` partitions. Record the analog's path and the line range you read
   it from. Emit exactly this record, unconditionally and durably: write it to the
   fixed scratch path `/tmp/reference_mining.json` (always, with no precondition on
   `/razorback-freeze` or any other directory), then PRINT the file to standard
   output so the full record is captured in your session transcript:

   ```json
   {
     "target_model": "<path of the model you are building>",
     "layer": "<the target's directory/layer>",
     "grain": "<one row per …; the key column(s)>",
     "analog": "<analog file path>:<line-range>",
     "analog_source": "own_sibling | package_template",
     "from_relation": "<the analog's left-most FROM relation>",
     "join_ladder": ["<join 1: relation on key>", "<join 2: …>"],
     "spine_key_source": "<relation that supplies the full key set>",
     "window_group_by": "<group by keys / over(...) partitions, or none>"
   }
   ```

   ```
   apply_patch  # create /tmp/reference_mining.json with the JSON above
   cat /tmp/reference_mining.json
   ```

   `/tmp/reference_mining.json` is scratch OUTSIDE the dbt project; it is not the
   graded artifact and is not part of the final project source state. The
   authoritative copy is the one printed to stdout (it survives in the session
   record even though the container scratch is discarded).

Then, in Implementation, **copy the recorded analog's construction verbatim as the
skeleton** — its FROM relation, its join ladder, its spine/key source, and its
window/group-by — and adapt ONLY the leaf columns and source relations to the
target model. Build the target on the analog's spine; do not re-invent a different
FROM, join direction, or grain when a same-layer sibling already shows the working
one. Worked example (the analog is the AFTER skeleton you copy; you change only the
leaf source and columns, not the FROM/join/spine/group-by shape):

```sql
-- Target: models/analytics_obt/<target_obt>.sql, one row per <target_key>.
-- Reference Mining record (own_sibling):
--   Analog: models/analytics_obt/<sibling_obt>.sql:1-40
--   from_relation: {{ ref('<spine_dim_or_fact>') }}
--   join_ladder: [left join {{ ref('<dim_a>') }} on <key_a>,
--                 left join {{ ref('<dim_b>') }} on <key_b>]
--   spine_key_source: {{ ref('<spine_dim_or_fact>') }}   -- supplies the full key set
--   window_group_by: none
-- Copy the analog's FROM/join/spine VERBATIM; adapt only the leaf source + columns.
select
  spine.<target_key>,
  a.<leaf_col_from_dim_a>,
  b.<leaf_col_from_dim_b>
from {{ ref('<target_spine>') }} as spine          -- same FROM shape as the analog
left join {{ ref('<target_dim_a>') }} as a on a.<key_a> = spine.<key_a>   -- same join ladder
left join {{ ref('<target_dim_b>') }} as b on b.<key_b> = spine.<key_b>
```

Two guards on what you copy:

- **Same-layer, same-shape only.** Adopt a construction only from an analog that
  is genuinely the analog for THIS model — a same-layer sibling of the same kind,
  or the installed-package model for the same staging entity. Do not import a
  FROM/join/spine from a relation that is not the analog, and where the analog and
  the project's own existing structure for this model conflict, keep the project's
  structure.
- **Copy shape, not contents.** Copy the analog's construction skeleton
  (FROM/join/spine/window), not its specific output columns or its data. The
  analog's column LADDER may be wider or narrower than the target needs; carry only
  the columns the target's own instruction and upstream relations support, and do
  not pad the target with the analog's extra columns or narrow it below what its
  own sources provide.

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
