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

## Stage: Dual Output Contract Arbitration

Run this stage only when the task requires you to **author or restructure** one or
more models, or to commit an **answer-style** deliverable (a chosen subset of the
options the instruction enumerates). **Skip it entirely for no-op and pure-repair
tasks**: on a no-op, change nothing; on a repair, the contract is already fixed by
the existing model and downstream consumers, so go straight to Implementation and
make the smallest fix. Do not invent a contract a plain repair does not need.

When it applies, do not write any model SQL or commit any answer until you have run
all three phases below and recorded `arbitration.json`. The point of this stage is
that **two independent contracts expose disagreement, and a separate evidence-based
arbitrator — not narrative plausibility — decides what gets built.**

### Phase 1 — Shared evidence snapshot (decide nothing)

From the local workspace only, collect the visible evidence both routes will read,
**without choosing the answer**. Record, in the freeze notes if available (otherwise
a short comment block you keep next to your work):

- the exact task instruction text relevant to the deliverable;
- any `schema.yml` / `*.yml` that declares the target model(s): its `columns:` list
  (in order), declared types/tests, and described grain;
- the upstream relations the deliverable selects from, and the closest same-kind
  sibling model;
- for grain: the local parent/driver relation and its `COUNT(DISTINCT <key>)`;
- for width: the declared column set vs the columns the upstream relations can
  produce;
- for answer-style: per option, the local file/relation that could support or
  refute it, and a disconfirming check for each option;
- any installed package model under `dbt_packages/` that is the template for a model
  you must reproduce — only when the project clearly uses that package shape.
Do not record the snapshot as a decision; it is shared raw input for both routes.

### Phase 2 — Two independent contracts (B must not read A)

Produce **two** Output Contracts, route **A** and route **B**, each from the shared
snapshot, and keep them isolated so route B cannot anchor on route A:

- Author route A's full contract first and save it as `contract_a` (in the freeze
  notes if available, else a labelled comment block).
- Author route B as a **forced-divergence** stance: for every claim where the
  evidence is not unambiguous, route B must take the *opposite plausible reading*
  from route A and try to defeat A's claim with local evidence — argue the other
  grain source, the other column set, or, for answer-style, that each borderline
  option route A marked IN is actually OUT (and vice-versa). Do not copy route A's
  reasoning; re-derive every claim from the snapshot. Save it as `contract_b`.

Each contract must state, for every deliverable: **grain** (what one row is and the
source of the full key set), **declared columns** (full ordered set), **local
types** (sourced from the upstream relation or the installed package model, never
from a yml description alone), **metric logic**, **assumptions**, and an **evidence
reference for each claim**. A claim with no visible local support must be written
down as an *assumption*, not a fact. For answer-style tasks each route emits a
per-option IN/OUT table with the local check it relied on.

### Phase 3 — Evidence arbitration (independent of both routes)

Compare the two contracts **claim by claim** against this fixed evidence hierarchy,
highest authority first:

1. explicit task instruction;
2. `schema.yml` / declared local contract (columns, types, declared tests);
3. raw source data and conservation relations (e.g. parent `COUNT(DISTINCT key)`,
   row-count ties, sum/total conservation);
4. project-local tests / dbt constraints;
5. same-project sibling model patterns;
6. installed package artifacts, only when the task/project clearly uses that package
   shape;
7. candidate transcript / plan / self-written contract — **debug only, never a
   tie-breaker.**

The arbitrator decides on evidence authority, **not** on which contract reads better,
which route is more thorough, or which transcript is more convincing. Candidate
self-scoring (a contract's own completeness, its own "support N/N" count, its own
claimed checks) is **never** the deciding criterion — a plausible contract can
self-score perfect and still be wrong. For each contested claim, the higher-authority
visible source decides; if the only thing separating the two contracts is a fact that
lives in the hidden grading set (not derivable from layers 1–6), that claim is
`ABSTAIN`, not a forced pick.

Write `arbitration.json` (in the freeze notes if available, else next to your work)
with exactly one top-level `decision`:

- `SELECT_A` / `SELECT_B` — one contract is supported by higher-authority visible
  evidence and the other violates it;
- `MERGE_NON_CONFLICTING` — the contracts disagree only on separable claims and each
  selected claim has its own visible support;
- `REJECT_BOTH` — both contracts violate a hard local evidence rule;
- `ABSTAIN` — the visible workspace cannot decide the load-bearing disagreement.

`arbitration.json` must also record, per claim: the selected reading, the evidence
authority layer (1–7) that decided it, the rejected reading, and every abstained
claim. Example shape:

```json
{
  "decision": "SELECT_B",
  "reason": "route B ties out to parent COUNT(DISTINCT key)=14; route A drops 7 keys",
  "selected_claims": [
    {"claim": "grain", "reading": "one row per parent key, full key set",
     "evidence_authority": "3_raw_source_count_distinct_parent_key",
     "rejected_reading": "one row per child-matched key"}
  ],
  "abstained_claims": [],
  "hard_failures": {"contract_a": ["row_count_mismatch"], "contract_b": []}
}
```

If no visible layer separates the routes on a load-bearing claim:

```json
{
  "decision": "ABSTAIN",
  "reason": "both contracts satisfy layers 1-6; the deciding width/grain is oracle-only",
  "selected_claims": [],
  "abstained_claims": ["expected_intermediate_grain_oracle_only"],
  "hard_failures": {}
}
```

### Then implement only the arbitrated contract

Implementation proceeds **only** from the selected (or merged) contract, and that
contract is the acceptance condition: a deliverable is not done until its committed
SQL/answer emits exactly the arbitrated grain key set, the arbitrated columns in
order, the arbitrated types, and (for answer-style) exactly the arbitrated IN rows.
If the arbitrator returned `ABSTAIN` or `REJECT_BOTH` on a load-bearing claim, build
the most defensible artifact the visible evidence supports but **do not present the
final answer as locally verified** — record the unresolved claim in the freeze notes.
An abstained target is still useful diagnostic evidence; it is not a verified pass.

Two guards on the contracts themselves:

- **Same-thing, same-shape only.** Only adopt a key set, column, type, or template
  from a local relation that is genuinely the analog for *this* deliverable — the
  spine the code already joins onto, a same-layer sibling, or the installed package
  model for the same staging entity. Where a local signal and the project's own
  existing structure conflict, keep the project's structure.
- **Derive, do not pad.** Only list a column, key, or IN option you can point to in a
  local relation, an instruction, or a declaring yml. Do not fabricate columns to
  match an over-broad declaration, and do not mark an answer option IN without a local
  check whose observed result supports IN.

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
