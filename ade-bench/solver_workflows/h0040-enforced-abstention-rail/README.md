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

## Stage: Validation

Do additional correctness checks beyond "it builds".

For repairs, confirm the original failure mode is gone and the affected output
matches the source-data expectation. For refactors/config changes, check row
counts, schemas, and value-level behavior for affected and downstream models.
For new models or analysis tasks, check required columns, grain, uniqueness,
null behavior, row counts, and representative rows against source data. For
no-op tasks, confirm no project change was needed and leave files untouched.

Run broader dbt validation when practical for the task scope.

## Stage: Pre-commit abstention triage (enforced)

This stage runs **after Validation and before Finalization**, on every task. It is a
**mechanical gate**, not advice: for each load-bearing claim your edit rests on, you run a
**fixed three-clause trigger**, and **the abstain decision is computed from the three booleans
by an AND-of-NOTs rule — never by your judgment of whether the claim "feels" decidable or the
edit "looks" contradictory.** When the rule says abstain, you **must mechanically revert** the
edits that exist only to satisfy that claim, so those files end up **byte-identical to their
task-start state**. You do not get to overrule the booleans, and you do not get to abstain on a
hunch — the only input to the decision is the three explicit clause results.

**Step 1 — name the load-bearing claims.** List each **load-bearing claim** your committed edit
rests on: a quantity, grain, key set, column set, value mapping, threshold, or filter that, if
read wrong, makes the output wrong. For a no-op task with no edit, the list is empty and this
stage is a no-op.

**Step 2 — run the fixed three-clause trigger on each claim.** For each claim record three
booleans. **Set each one explicitly to `true` or `false`; there is no "unknown" and no default —
a clause you did not evaluate is not allowed.** A claim counts as decided if any clause is `true`.

1. **instruction** — Does an explicit sentence in the task instruction name the deciding quantity
   for that claim (a stated grain, a named column/metric, an enumerated set, a threshold)? `true`
   if a sentence names it; otherwise `false`.
2. **schema_yml** — Does an **existing** `schema.yml` already present at task start (not one you
   would add) name it — a declared column, a documented grain, or a declared test on the deciding
   key? `true` if present; otherwise `false`.
3. **raw_source_probe** — Reading **only the immutable raw `{{ source(...) }}` relation directly**
   — never a model you rebuilt, never a re-derived CTE, never your own output — can a
   conservation/coverage probe **decide** the claim on its own? Run two read-only probes against
   the raw source: a row **count** on the raw source, and a **key-level anti-join** between the
   raw-source key set and the relation the claim governs, e.g.

   ```
   dbt show --inline "select count(*) from {{ source('<src>','<tbl>') }}"
   dbt show --inline "select count(*) from (
       select <key> from {{ source('<src>','<tbl>') }}
       except
       select <key> from <claim_relation>
   )"
   ```

   The probe **decides** the claim only when the raw count or anti-join is conclusive on its own
   (the anti-join is empty so coverage over the raw key set is total, or the raw count fixes the
   expected grain). `true` if the raw-source probe decides it; otherwise `false`. **Read the
   immutable source only.** A re-derived intermediate re-correlates with any model error and gives
   a false `true` — and acting on a false `true` would let a wrong edit survive, while reverting on
   a re-correlated false read would destroy a *correct* edit. The anti-join's left side must be the
   raw `{{ source(...) }}` key set, never a relation you built.

**Step 3 — compute `abstain` mechanically.** `abstain` for a claim is **`true` if and only if all
three clause results are `false`** (`abstain = NOT instruction AND NOT schema_yml AND NOT
raw_source_probe`). Compute it from the booleans; do not write it by hand and do not infer it.
If any clause result is missing, the record is invalid — re-evaluate that clause and set it
explicitly; **never treat a missing clause as `false` and never default the claim to abstain.**

**Step 4 — enforce.** For each claim with `abstain == true` (oracle-only — no local source can
decide it), **mechanically revert every edit you made ONLY to satisfy that claim**, restoring those
files to byte-identical task-start state (`git checkout -- <file>` / `git stash` the
claim-specific hunks, or re-apply the original bytes), and record `reverted_files` for that claim.
Revert **only** the hunks whose sole purpose was that undecidable claim — edits that are also
required by a *separately decided* claim (one with a `true` clause) stay. **A claim with `abstain
== false` is never reverted** — at least one local source decided it, so the edit stands. This is
the whole safety contract: you revert on the mechanical AND-of-NOTs and nothing else, so a passer
whose edit any clause supports cannot be reverted.

**Step 5 — record `triage.json` (PINNED schema) and route it durably.** Emit exactly this record
and nothing else from this stage. The shape is fixed; `abstain` is derived, not free-form:

```json
{
  "claims": [
    {
      "claim": "<the single load-bearing claim, one sentence>",
      "clause_results": {
        "instruction": <true|false>,
        "schema_yml": <true|false>,
        "raw_source_probe": <true|false>
      },
      "abstain": <true|false>,
      "reverted_files": [ "<path>", "..." ]
    }
  ]
}
```

Write the record to the fixed scratch path `/tmp/triage.json` **unconditionally** (no
precondition, no dependence on `/razorback-freeze` having any particular layout), then **print the
file's contents to standard output** so the full record is captured in your session transcript:

```
apply_patch  # create /tmp/triage.json with the JSON above
cat /tmp/triage.json
```

`/tmp/triage.json` is scratch outside the dbt project; it is not the graded artifact. The
authoritative copy is the one printed to stdout — it survives in the session record even though
the container scratch is discarded. Then continue to Finalization. The graded project state after
this stage = your committed edits **minus exactly the reverts the AND-of-NOTs rule fired**; a claim
that any clause decided keeps its edit untouched.

## Stage: Finalization

Leave only intended project changes. Remove scratch files unless the dbt project
requires them. Finish with changed files and concise validation evidence.
