---
id: h0010
title: Implementation — build one-row-per-entity models FROM the entity table as the spine, LEFT JOIN aggregated children (don't group the child table upward)
status: smoke
kind: hypothesis
source: forked from the h0009 smoke deep-dive (run 13ecf093adb674c2). 4 of the 5 non-flips (asana004, asana005, intercom001, intercom003) share ONE root cause — the solver builds an aggregate FROM the child/event table and GROUPs upward, silently dropping parent entities that have no children (wrong grain spine). h0009 showed copying a package's surface conventions (a filter) doesn't fix this; and h0008 showed checking grain at Finalization is inert. This moves the grain idea to a generative Implementation construction rule. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal; @baseline 622bdedac572b479, 31/48 = 0.6458 — h0008/h0009 promoted nothing).
started: 2026-06-04T12:14:43Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The h0009 smoke deep-dive found that **4 of its 5 non-flips share one root cause**: the
solver builds a "one row per `<entity>`" model by selecting **from the child/event table
and `GROUP BY`-ing upward**, which silently drops every parent entity that has no child
rows — changing the grain. Concretely:

- `asana004`, `asana005` (`AUTO_int_asana__project_user_agg_equality`, `Got 3`): aggregate
  off `project_user` (13 projects that have users) instead of the `project` table (16),
  dropping the 3 zero-user projects.
- `intercom001`, `intercom003` (`AUTO_intercom__threads_equality` /
  `…conversation_metrics_equality`, `Got 7`): build FROM `conversation_part_history` and
  group, yielding the 5 conversations that have parts, instead of building FROM the active
  `conversation_history` spine LEFT JOIN parts — which is the canonical solution structure
  (`from latest_conversation left join latest_conversation_part`) and includes the 2 active
  conversations that have zero parts.

This is the **same** "no source rows silently dropped" property h0008 tried to assert as a
**Finalization check** — which was behaviorally inert (the solver rubber-stamped its own
wrong output). The difference here: state it as a **generative Implementation construction
rule** that changes *how the SQL is written in the first place*, not a check applied after.
It also differs from h0009: h0009 ("copy the installed package") can't fix these because
`int_asana__project_user_agg` is bespoke (no package analog) and the intercom *transform*
package isn't installed — so the rule must be generative, not copy-from-package.

**Falsifiable claim (the single README change — Implementation stage only):** the seed
solver's Implementation prose says "make the smallest task-relevant change following local
patterns" but gives no rule for choosing the grain spine of an aggregate/entity model.
Adding one Implementation instruction — *when building or changing a model whose grain is
"one row per `<entity>`" (including tasks phrased "aggregate `<child>` by `<entity>`"),
select FROM the `<entity>`'s own table as the spine and LEFT JOIN the aggregated `<child>`
rows onto it, so every entity appears (with `0`/`NULL` aggregates where it has no children);
do NOT make the child/event table the spine and `GROUP BY` upward, which drops entities
with no child rows and changes the grain. If the source applies an active-record filter
(`_fivetran_active`), apply it to BOTH the entity spine and the child before joining* —
will flip the grain-spine failures (asana004/005, intercom001/003) to passes by producing
the correct base-table structure, raising `stratified_pass_at_1` above the `@baseline`
0.6458.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex, gpt-5.5); no dataset, harness, or
solver-runtime change. Leak-guard intact (the rule uses only the local project's source
tables and stated grain — no public fetch, no oracle, no reference to hidden `AUTO_*`
tests). One idea, one stage (Implementation).

Target datasets (smoke, all `ade-bench-` prefixed): the 4 shared-root-cause grain-spine
failures — `ade-bench-asana004`, `ade-bench-asana005`, `ade-bench-intercom001`,
`ade-bench-intercom003` — plus a stable-`@baseline`-pass regression sentinel
`ade-bench-asana001`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0010-implementation-grain-spine-from-entity.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Implementation` (the single grain-spine rule), leaves
Exploration/Validation/Finalization and the dependency/package guardrails untouched, and
does not reference hidden `AUTO_*`/verifier tests or weaken the leak-guard prose.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on the 4 targets + `asana001` sentinel, the variant must not regress the
sentinel and should flip at least one of the 4 grain-spine failures to a pass before
promotion to full.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: The forked solver README's ONLY change vs codex-ade-dbt-minimal/README.md is the single Implementation-stage grain-spine construction rule, placed in ## Stage: Implementation ONLY; Exploration/Validation/Finalization + dependency guardrails untouched; leak-guard intact; no AUTO_*/verifier reference; no re-derive/check-against-expected.
  `diff` shows a single 8-line paragraph inserted after the Implementation prose (README diff in gate evidence below); generative rule phrased "select FROM … LEFT JOIN", not a verification step.
- DONE: FULL spec specs/h0010-implementation-grain-spine-from-entity.yaml diffs specs/baseline.yaml in ONLY experiment: + solver_workflow:; smoke spec adds ONLY benchmark.tasks: [asana004, asana005, intercom001, intercom003, asana001]; agent.kind=spacedock_solver and runtime=codex preserved.
  FULL diff = 2 fields (gate evidence); smoke diff = benchmark.tasks only; frozen full spec lines 4-5 show kind: spacedock_solver / runtime: codex.
- DONE: Both specs frozen with rk freeze --allow-missing (full + smoke); two-field FULL spec diff and README diff pasted in gate evidence.
  Wrote specs/h0010-implementation-grain-spine-from-entity.frozen.yaml and .smoke.frozen.yaml.

### Summary

Forked the current @baseline solver (codex-ade-dbt-minimal, 622bdedac572b479) to
solver_workflows/h0010-implementation-grain-spine-from-entity and added exactly one
Implementation-stage rule: build "one row per `<entity>`" models FROM the entity table as
the spine and LEFT JOIN aggregated children, never grouping the child/event table upward
(apply any `_fivetran_active` filter to both sides). The rule is generative (how to write
the SQL), references no hidden AUTO_*/verifier tests, and does not instruct re-deriving or
checking against expected output. Full spec differs from baseline only in `experiment:` +
`solver_workflow:`; smoke spec adds only the 4 grain-spine targets + asana001 sentinel.
Both specs frozen. Did NOT run `rk run` (that is the smoke stage).

### Gate evidence

FULL spec diff vs baseline (specs/baseline.yaml -> specs/h0010-implementation-grain-spine-from-entity.yaml):

```diff
2c2
< experiment: ade-bench-baseline # variants: ade-bench-h0001-<slug>
---
> experiment: ade-bench-h0010-implementation-grain-spine-from-entity # variants: ade-bench-h0001-<slug>
11c11
<   solver_workflow: ./solver_workflows/codex-ade-dbt-minimal # variants repoint to ./solver_workflows/h<NNNN>-<slug>
---
>   solver_workflow: ./solver_workflows/h0010-implementation-grain-spine-from-entity # variants repoint to ./solver_workflows/h<NNNN>-<slug>
```

README diff vs codex-ade-dbt-minimal/README.md (inserted into ## Stage: Implementation):

```diff
55a56,64
> When building or changing a model whose grain is "one row per `<entity>`"
> (including tasks phrased "aggregate `<child>` by `<entity>`"), select FROM the
> `<entity>`'s own table as the spine and LEFT JOIN the aggregated `<child>` rows
> onto it, so every entity appears (with `0`/`NULL` aggregates where it has no
> children); do NOT make the child/event table the spine and `GROUP BY` upward,
> which drops entities with no child rows and changes the grain. If the source
> applies an active-record filter (`_fivetran_active`), apply it to BOTH the
> entity spine and the child before joining.
>
```
