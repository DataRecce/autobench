---
title: Output Contract — a new derivation stage between Exploration and Implementation that records grain key-source, ordered column set, column types, and the complete deliverable model set from named local artifacts before any SQL is written
status: expanded
kind: concept
source: innovate-bugtype-fixes workflow; captain steer to fix bug types in Exploration/Implementation or a new stage between them rather than post-answer Validation.
started: 2026-06-05T00:00:00Z
completed: 2026-06-05T00:00:00Z
verdict: PASSED
id: concept-contract-first-derivation-stage
worktree:
archived: 2026-06-11T02:47:49Z
---
## Direction

The captain's thesis: post-answer Validation is a weak place to catch ade-bench's false-greens; fix the answer BEFORE the bug is born by deriving the OUTPUT CONTRACT up front from LOCAL, non-leaking signals, then building to satisfy it. This concept proposes inserting a new solver-workflow stage, **Output Contract**, Insert as a new `## Stage: Output Contract` section BETWEEN the end of `## Stage: Exploration` (after the line "Record suspected task type, affected files/models, baseline errors, and useful data observations before making project changes.") and the start of `## Stage: Implementation` (the line "## Stage: Implementation"). In the current README file (/home/kent/autobench/ade-bench/solver_workflows/codex-ade-dbt-minimal/README.md) this is between line 48 and line 50..

**Why it escapes the prose ceiling.** The dead prose/skeleton levers (h0010, h0011, h0016) all fired AT Implementation time and asked the solver to restructure SQL in the moment of writing it — and were acknowledged-but-not-executed (the committed SQL was byte-identical or still drove the child grain). This stage moves the lever EARLIER and changes the artifact's precondition: the solver must first WRITE DOWN a concrete contract (grain key-source, ordered columns, types, model set) extracted by reading named local files, and Implementation becomes a fill-in measured against that written contract rather than a fresh derivation. That is a different control point than the inert in-line Implementation prose. It also concentrates on the ONE mechanism that ever landed (asana002): a mechanical, copyable, in-place substitution anchored to a concrete local artifact (the installed package staging model / the upstream relation / the spine the code already joins onto). The grain rule is framed not as 'restructure your query' (the inert ask) but as 'the new model must reproduce what the existing CTEs produced, un-narrowed, because the coalesce/spine already live downstream' — a copy-and-repoint edit, not a rewrite. It does NOT claim to recover signals that are only in the hidden oracle: the ground-truth map shows the asana004 spine, the airbnb009 complete-date spine, the ana-eng006 stated uniqueness, the quickbooks001 broken-ref set, and the asana002 package type are all LOCALLY derivable; for the value-divergence residuals (f1006, airbnb007) where nothing local pins the answer, the stage is silent and adds nothing. So it targets exactly the locally-derivable shape/width/deliverable/type bugs and stays out of the lever-killing zones.

**What the stage derives** (each from a concrete local artifact, leak-safe):
- Grain (what one row is) plus the SOURCE of the full key set — derived from the relation the existing code/instruction treats as the driver (the FROM/left-most spine, the instruction-named entity, or a stated uniqueness rule), with an explicit rule not to narrow an extracted CTE's key set to only child-matched keys (the asana004/asana005/intercom grain-drop bug).
- The full required COLUMN set in order — from a declaring schema.yml/*.yml columns: list when one exists, otherwise from the upstream relations' SELECT lists plus the same-kind sibling model's convention, plus instruction-named columns verbatim (ana-eng004 OBT-sibling case, f1002 yml case).
- Column TYPES — taken from the upstream relation, or from the installed dbt_packages/ staging model for the same-named column with the matching cast applied in place (asana002 ::timestamp cast), explicitly NOT from a yml description.
- The COMPLETE deliverable model set — by resolving the local ref() graph (a ref() to a non-existent model => that model is a deliverable) and matching installed package models the local models ref by name (quickbooks001 missing stg_/int_ set).
- An applicability gate (author/refactor only; no-op and pure-repair skip the stage) and two contract guards: same-thing-same-shape (only adopt analog signals; project structure wins on conflict) and derive-not-pad (only list columns a local relation/instruction/declaring-yml supports; do not fabricate to match an over-broad yml).

**Proposed `## Stage:` block** (the exact lever, to fork into a variant solver README):

## Stage: Output Contract

Run this stage only when the task requires you to **author or restructure** one or
more models (creation, refactor/config, or the model-building part of a mixed task).
**Skip it entirely for no-op and pure-repair tasks**: on a no-op, change nothing; on a
repair, the contract is already fixed by the existing model and downstream consumers, so
go straight to Implementation and make the smallest fix. Do not invent a contract a
plain repair does not need.

When it does apply, **write the contract down before you write any model SQL.** For each
model you must deliver, derive these four things from the local workspace only and record
them (in the freeze notes if available, otherwise as a short comment block you keep next
to your work):

1. **Grain — what one row is, and which key set must be present.** Name the exact key
   column(s) and, critically, the *source of the full key set*. The full key set is the
   relation the existing code or the instruction treats as the driver — the table that is
   the `FROM` / left-most relation onto which other relations are `LEFT JOIN`ed, the table
   the instruction names as the thing being described, or the relation a stated uniqueness
   rule applies to. If the instruction says the model is unique on a key, that key is the
   grain. If you are extracting CTEs out of an existing model, the new model's key set must
   stay the key set those CTEs produced *before* the downstream model re-keyed or
   `coalesce`d them — do not narrow it to only the keys that have matching child rows.
2. **Columns — the full required set, in order.** If a `schema.yml` / `*.yml` declares
   `columns:` for this model, that ordered list is the contract; reproduce every declared
   column. If no yml declares this model, derive the column set from the relations you are
   selecting from (the upstream models' / sources' `SELECT` lists) plus the convention of
   the closest sibling model of the *same kind* (e.g. another model in the same directory
   that joins the same dims onto a fact). Use the instruction's named columns verbatim when
   it lists them.
3. **Types.** For each column, take the type from the relation it is sourced from. When you
   are matching a model to an installed package's staging model (the package is resolved in
   `dbt_packages/`), read that package model's column and adopt its type for the same-named
   column — apply the matching cast in place. A local yml description is *not* a type
   source; types come from the upstream relation or the installed package model.
4. **Deliverable set — every model that must exist.** Resolve the full `ref()` graph: if a
   local model `ref()`s a model that does not exist, that missing model is part of the
   deliverable set. If an installed package in `dbt_packages/` ships a model your local
   models `ref()` by name, that package model is the template for the one you must
   reproduce. Cross-check against any yml that declares models.

**Then build to satisfy the written contract**, and treat the contract as the acceptance
condition for the Implementation stage: a model is not done until its committed SQL emits
exactly the recorded grain key set, the recorded columns in order, and the recorded types.

Two guards on the contract itself:

- **Same-thing, same-shape only.** Only adopt a key set, column, type, or template from a
  local relation that is genuinely the analog for *this* model — the spine the code already
  joins onto, a same-layer sibling, or the installed package model for the same staging
  entity. Do not import naming, grain, or columns from a relation that is not the analog,
  and do not impose a package convention on a model that has no package analog. Where a
  local signal and the project's own existing structure conflict, keep the project's
  structure.
- **Derive, do not pad.** Only list a column you can point to in a local relation, an
  instruction, or a declaring yml for *this* model. If a yml appears to declare more
  columns than the relations you select from can produce, prefer the columns the data and
  instruction actually support; do not fabricate columns to match an over-broad
  declaration.

Worked derivation (refactor example, fully local). Instruction: *"refactor `asana__project`
into a new intermediate model … do the calculations done in the `agg_project_users` and
`count_project_users` CTEs in a new model `int_asana__project_user_agg` with columns
`project_id`, `users`, `number_of_users_involved` … then update `asana__project` to use it."*
Open the model named in the instruction (`models/asana__project.sql`) and read how those two
CTEs feed the rest of the model:

- The CTEs `agg_project_users` and `count_project_users` each `group by project_id` over
  `int_asana__project_user` — so their *own* key set is the set of `project_id`s that have a
  matching user, which is **narrower** than the full project list.
- But in the assembling CTE (`project_join`) the model does
  `from project left join agg_project_users … left join count_project_users …` and applies
  `coalesce(count_project_users.number_of_users_involved, 0)` **there**, after the join.

Contract derivation for the new `int_asana__project_user_agg`: (1) **Grain** = one row per
`project_id`; the full key set is the keys the CTE output is *consumed against*, i.e. the
CTE output as-is (do not pre-filter or re-key it) — the new model must reproduce exactly
what those CTEs produced, with no `coalesce` and no narrowing, because the `coalesce` and the
full-project spine live downstream in `asana__project` and must stay there. (2) **Columns**
= `project_id`, `users`, `number_of_users_involved` (instruction-named, in order).
(3) **Types** = inherited from `int_asana__project_user` / the existing CTE expressions.
(4) **Deliverable set** = the one new intermediate model plus the edit to `asana__project`
so it `ref()`s the new model in place of the two inline CTEs, with the existing downstream
`coalesce(...)`/spine join left intact. A secondary local check: `intermediate_asana.yml`
declares a `dbt_utils.unique_combination_of_columns` test on the upstream
`int_asana__project_user`, confirming that is the child grain you are aggregating from. With
the contract written this way, Implementation is a fill-in (lift the CTE bodies verbatim into
the new model, repoint the `ref`) rather than a re-derivation — and you do not silently move
the `coalesce`/spine into the new model, which would change its grain.

**Known risks** (and the prose scoping that contains them):
- Inertness (the h0010/h0011/h0016 ceiling): the solver may write the contract as chatter and still build the same wrong SQL. SCOPED by making the written contract the explicit acceptance condition for Implementation and by framing the grain fix as a copy-and-repoint (lift the CTE verbatim, do not move the coalesce) rather than 'restructure' — i.e. a mechanical substitution, the only edit shape that has ever landed. Residual risk remains real; verify by reading the committed SQL and the Got-N distance, not the transcript.
- Convention bleed / over-application on the non-target majority (the h0009 -3 regression: Fivetran naming forced onto non-package f1001, columns trimmed to a staging contract on quickbooks intermediates). SCOPED by the 'same-thing, same-shape only' guard (adopt a key/column/type/template only from the genuine analog; do not impose a package convention on a model with no package analog) and the explicit 'where a local signal conflicts with the project's own structure, keep the project's structure' tie-breaker.
- Misleading local declarations (f1002 most_podiums: the yml over-declares 6 cols vs the real 3-col answer). SCOPED by the 'derive, do not pad' guard: prefer the columns the upstream relations and instruction actually support over an over-broad yml declaration; do not fabricate columns to match a declaration. This will not fully fix f1002 (the true 3-col answer is not locally provable) but it stops the lever from making it worse by padding to 6.
- Harm on no-op/repair tasks (a contract step could provoke needless edits). SCOPED by the leading applicability gate: the stage runs only for author/refactor/mixed-build work; no-op changes nothing and pure-repair goes straight to the smallest fix with no contract authored.
- Generative blast radius — as a stage that fires on every authoring task, it is gatekeeper-G8-relevant and must carry cross-family regression canaries (at least one currently-passing @baseline task from each non-target family, including a non-package f1 task and a quickbooks intermediate) in any smoke set, since a targets-only smoke set was structurally blind to h0009's regressions. This is a process risk to enforce at propose-gate, not something prose alone removes.
- Value-divergence residuals (f1006 tie-break, airbnb007 invented NPS definition/tolerance) are NOT locally derivable; the stage is deliberately silent on them and must not be expected to flip them — claiming so would be the h0011 premise-falsification trap.

**Fan-out.** This concept was ideated into the following hypotheses (this workflow run):
- `h0017-contract-grain-entity-spine` (bug type 1a - Grain - entity spine (missing parent rows))
- `h0018-contract-rolling-window-calendar-range` (bug type Tolerance-band divergence (*_equality_with_tolerance) — root-caused on airbnb007 (daily_agg_nps_reviews) as a date-grain / rolling-window CONSTRUCTION error: a per-day aggregate keyed on actually-occurring review_dates with a rolling 'over last 28 days' figure, NOT a numeric-formula error)
- `h0019-implementation-let-categories-emerge-not-cross-join` (bug type 1b - Grain - date/calendar spine (missing days))
- `h0020-implementation-package-type-contract-cast` (bug type Type / contract mismatch (values right, column type/representation differs) — oracle 'Got N that disappears with a ::type cast'; target ade-bench-asana002 (asana__task due_at))
- `h0021-implementation-stable-dedup-ordering-under-type-change` (bug type Value divergence (shape right, numbers wrong) — type-dependent dedup/ranking ORDER BY ordering sub-bug (ana-eng007 dim_products). f1006 residual excluded (not locally derivable). ana-eng007-medium demoted to sentinel per the critique (h0013 1->3 regression risk under its vague 'fix everything' instruction).)
- `h0022-output-contract-answer-decision-table` (bug type Analytical-answer guess (categorical/multi-select answer with an unverified option included on plausibility))
