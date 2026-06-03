---
id: h0007
title: Validation — reconstruct expected output from visible source data and self-validate before finalizing
status: hypothesis
kind: hypothesis
source: forked from h0006's falsification — the target tests/AUTO_*_equality.sql checks are HIDDEN verifier tests injected only at grading time (absent from the solver's /app/tests), so h0006's "run the visible target singular tests and drive them to zero rows" had nothing to run (0/8 flips, clean audit, +1 regression). Forks the post-DuckDB-fix @baseline (622bdedac572b479, 31/48 = 0.6458); solver_workflows/codex-ade-dbt-minimal unchanged (h0006 did not promote).
started:
completed:
verdict:
score:
worktree:
---

## Hypothesis

h0006 falsified the assumption that the grading checks are runnable by the solver: the
target `tests/AUTO_*_equality.sql` singular checks are **hidden verifier tests injected
only at grading time** and never exist in `/app/tests`. So any method that tells the
solver to *run* those checks is inert (h0006: 0/8 flips on a clean audit, `captured=1`,
+1 regression).

But the remaining dominant failure class is still **target equality-test misses** on tasks
that build green — and on the highest-leverage cluster tasks the *expected* output is fully
determined by the **visible** inputs: the task spec dictates the exact grain/columns and
the source data + existing CTE logic dictate the values. Example (asana004): "move the
`agg_project_users` and `count_project_users` CTE calculations into a new
`int_asana__project_user_agg` model with columns `project_id`, `users`,
`number_of_users_involved`." The failing `AUTO_int_asana__project_user_agg_equality` is a
3-row logic mismatch the solver could have caught itself — by reconstructing what the
output *should* be from the visible source and comparing — without ever seeing the hidden
test.

**Falsifiable claim (the single README change):** the seed solver's Validation stage
checks generic data-quality properties ("row counts, nulls, uniqueness, representative
rows") but does not **independently reconstruct the expected result** for the changed
model from the visible source data + the task spec's stated grain/columns/aggregation, and
**diff its model output against that reconstruction**. Adding one Validation/Finalization
instruction — *for each model the task requires you to create or change, derive the
expected output independently from the visible source tables and the task's stated
grain/columns/aggregation (e.g. an ad-hoc `SELECT`/CTE built straight from sources, or a
hand-computed expectation on a sampled key), then diff your model's output against that
reconstruction; reconcile every discrepancy (row count, key set, and per-column values on
shared keys) before finalizing* — will catch the subtle aggregation/grain mismatches that
currently fail the hidden `_equality` checks, converting a material number of equality
misses into passes and raising `stratified_pass_at_1` above the `@baseline` 0.6458.

This is a method/README change only. It forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex, gpt-5.5) with no dataset,
harness, or solver-runtime change. The change must NOT reference the hidden `AUTO_*`
tests, and the no-external-reference / leak-guard prose stays intact (the reconstruction
is built only from the local workspace source data — no public fetch, no oracle).

## Acceptance criteria

**AC-1 — Spec diff is a single, localized Validation/Finalization change.**
Verified by: the diff vs `@baseline`'s `solver_workflows/codex-ade-dbt-minimal/README.md`
touches only the `## Stage: Validation` (and, if needed, `## Stage: Finalization`)
section, adding the "reconstruct expected output from visible source + task spec and diff
against it" instruction. No reference to the hidden `AUTO_*`/verifier tests. No change to
Exploration/Implementation or to the dependency/package guardrails. FULL spec differs from
baseline only in `experiment:` + `solver_workflow:`.

**AC-2 — Smoke gate.** On the smoke subset (the shared-logic cluster targets below), the
variant must not regress any `@baseline` pass and should flip at least one equality miss
to a pass before promotion to full.

**AC-3 — Promotion gate (full run).** Paired `rk runs diff @baseline <variant-run-dir>` on
a clean `rk audit --policy strict`: the adjusted-p / CI clears the tripwire (CI excludes a
regression) AND `stratified_pass_at_1 > 0.6458`. Every recorded score is paired with a
clean strict audit on the same run-dir.

## Target datasets

Highest-leverage shared-logic clusters from the h0005/h0006 equality-miss analysis — tasks
that build green and fail a single (or few) `_equality` check whose expected value is
reconstructable from visible sources:

- **asana `int_asana__project_user_agg` cluster** (one shared aggregation; a correct
  reconstruction could flip several at once):
  - `asana004` 5/6 — `AUTO_int_asana__project_user_agg_equality` (3-row miss)
  - `asana005` 7/8 and `asana005-hard` 7/8 — same check (3-row miss)
- **intercom threads / conversation-metrics cluster:**
  - `intercom001` 1/2 — `AUTO_intercom__threads_equality` (7-row miss)
  - `intercom003` 1/2 — `AUTO_intercom__conversation_metrics_equality`
- **other off-by-one reconstructable misses (smoke breadth):**
  - `asana002` 2/3 — `AUTO_asana__task_equality`
  - `f1006` 3/4 — `AUTO_constructor_points_equality`
  - `ana-eng007` 9/10 — `AUTO_dim_products_equality`

Proposed smoke set (shared-logic-first): the asana cluster (`asana004`, `asana005`,
`asana005-hard`) + intercom (`intercom001`, `intercom003`) + `asana002` + `f1006`. Remember
benchmark.tasks must use the **`ade-bench-` prefixed** ids (e.g. `ade-bench-asana004`) —
the bare slug is rejected by `rk run`.

## Run result

## Behavioral analysis

## Verdict
