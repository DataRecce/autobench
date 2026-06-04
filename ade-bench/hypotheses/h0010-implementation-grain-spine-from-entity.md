---
id: h0010
title: Implementation — build one-row-per-entity models FROM the entity table as the spine, LEFT JOIN aggregated children (don't group the child table upward)
status: conclude
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

**Recommendation: NO-GO** (do not promote to full). The grain-spine Implementation
rule did not change the final committed SQL on the targets — instruction inert.

Run dir: `runs/ade-bench-h0010-implementation-grain-spine-from-entity/37f787e351594ca6`
(smoke spec `specs/h0010-implementation-grain-spine-from-entity.smoke.frozen.yaml`,
5 tasks, trials=1).

**Audit + score attestation.** 5/5 cells completed, 0 errored. `rk audit --policy
strict` on this run-dir: CLEAN — `{clean: 5, tainted: 0, coverage_missing: 0}`,
`captured > 0` all cells. `rk score` paired to the same run-dir:
`stratified_pass_at_1 = 0.2` (1/5). (Audit + score executed by team-lead on this
exact run-dir.)

**Per-task vs `@baseline` (622bdedac572b479):**

| Task | @baseline | h0010 | Flip? | Distance-to-pass |
|------|-----------|-------|-------|------------------|
| ade-bench-asana004   | FAIL | FAIL (0) | no | unchanged — `Got 3` |
| ade-bench-asana005   | FAIL | FAIL (0) | no | unchanged — `Got 3` |
| ade-bench-intercom001| FAIL | FAIL (0) | no | unchanged — `Got 7` |
| ade-bench-intercom003| FAIL | FAIL (0) | no | unchanged — `Got 7` |
| ade-bench-asana001 (sentinel) | PASS | PASS (1) | n/a | sentinel held, no regression |

ZERO of the 4 grain-spine targets flipped; the sentinel did not regress.

**Behavioral verdict (did the FINAL COMMITTED SQL apply the entity-spine LEFT JOIN?).**
No — on both inspected targets the solver kept the **child table as the spine**, the
exact error the rule names. asana004 `int_asana__project_user_agg.sql` is structurally
identical to @baseline: it spines off `count_project_users`/`agg_project_users` built
`from {{ ref('int_asana__project_user') }}` (the child) and `GROUP BY`-s upward, then
`select * from project_user_agg` (renamed `final`) — the `project` table is never the
FROM spine, so the 3 zero-user projects stay dropped. intercom001 `intercom__threads.sql`
does `from conversation_part_aggregates left join conversations` — the parts aggregate
(child) is still the spine and `conversation_history` (the entity) is the LEFT-JOINed
side, i.e. the join is anchored backwards from the rule; the solver did add
`where _fivetran_active` to both CTEs (a surface nod to the rule's filter clause) but
left the grain direction inverted, so the 2 zero-part active conversations stay dropped.
The rule was discussed/partially gestured at (filter applied) but the load-bearing
"FROM the entity as the spine" structure was NOT implemented — the instruction is inert
on the committed model, just as h0008's Finalization check was inert. NO-GO: this is not
a "grain wasn't the whole bug" result (the SQL never changed grain direction); it is
"rule not implemented," so the hypothesis as worded (a prose Implementation rule will
flip these) is falsified at smoke.

## Run result

## Behavioral analysis

## Verdict

**REJECTED at smoke (pre-full, NO-GO). @baseline (622bdedac572b479) UNTOUCHED — nothing
promoted.**

**Evidence.** Smoke ran the 4 grain-spine targets + asana001 sentinel: 5/5 cells
completed, 0 errored; `rk audit --policy strict` CLEAN `{clean: 5, tainted: 0}`; paired
`rk score` `stratified_pass_at_1 = 0.2` (1/5). The asana001 sentinel held (PASS, no
regression), but ALL 4 grain-spine targets stayed FAIL with UNCHANGED distance-to-pass —
asana004/005 `Got 3`, intercom001/003 `Got 7`. No target flipped.

**Mechanism (the important part — why it failed).** The rule was behaviorally **INERT**,
and not because the diagnosis was wrong: the grain spine genuinely IS the bug. It failed
because the solver did not translate the prose rule into the committed SQL. Two deep-dives
on the final committed models confirm this:
- `asana004` — final `int_asana__project_user_agg.sql` is **structurally identical to
  @baseline**: it still spines off the `agg_project_users`/`count_project_users` CTEs (both
  built `from {{ ref('int_asana__project_user') }}`, the child, GROUP BY upward) and never
  selects FROM the `project` table; @baseline's `final` CTE is merely renamed
  `project_user_agg`. The 3 zero-user projects stay dropped.
- `intercom001` — the solver DID build a `conversations` spine CTE (`from
  conversation_history where _fivetran_active`) and added `_fivetran_active` to both sides,
  but wired the join **backwards**: `from conversation_part_aggregates left join
  conversations`, so the parts aggregate (child) still drives the grain. The 2 zero-part
  active conversations stay dropped.

In short: **"talks / partially gestures (filter, a spine CTE) but doesn't do"** — the
load-bearing "FROM the entity as the spine" structure never reached the committed model,
exactly the inertness h0008's Finalization check showed.

**META-FINDING across the three hypotheses tried on this @baseline.** h0008
(check-afterward): 0/7 flips. h0009 (copy-the-installed-package): 1/6. h0010
(construct-rule): 0/4. README-prose levers at gpt-5.5 / `reasoning_effort: xhigh` largely
do NOT change the committed SQL structure on these data-correctness tasks. The single
durable win (asana002, under h0009) was a type-contract match the solver could apply
**mechanically** — not a structural rewrite it had to reason its way into. The pattern:
prose that asks the solver to restructure how it writes SQL is inert; prose that names a
concrete mechanical substitution can land.

**Next move (explicitly NOT another reflexive prose hypothesis).** Per the meta-pattern,
filing another prose-rule hypothesis would just re-confirm the inertness ceiling. The next
step is a **captain strategy decision**, not an automatic follow-up — candidate directions:
(a) a worked-example / few-shot Implementation instruction that shows the exact SQL
skeleton (`from <entity> left join (<child agg>) ... `) for the solver to pattern-match
mechanically rather than re-derive; (b) accept a solver-execution ceiling at this
model/effort and stop spending budget on prose levers; (c) a non-prose approach (e.g. a
harness/scaffold change). No follow-up hypothesis is filed here by design. Frontmatter
(status/verdict/completed) is left for the first officer.

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

## Stage Report: smoke

- DONE: Smoke run launched DETACHED (nohup + /tmp/rk-h0010-smoke.log + .pid), polled across turns; all 5 cells completed with 0 errored and captured > 0.
  Run dir runs/ade-bench-h0010-implementation-grain-spine-from-entity/37f787e351594ca6; 5/5 completed, 0 errored, strict audit captured > 0 all cells.
- DONE: rk audit <run-dir> --policy strict is CLEAN and the rk score is paired to that same run-dir; both recorded in ## Smoke result.
  Strict audit {clean: 5, tainted: 0, coverage_missing: 0}; score stratified_pass_at_1 = 0.2 (1/5) on the same run-dir (run by team-lead).
- DONE: Per-task smoke verdicts vs @baseline in ## Smoke result: which targets flipped, asana001 sentinel held, and the behavioral check (did the solver apply the entity-spine LEFT JOIN?).
  Per-task table recorded; 0/4 targets flipped, sentinel held; behavioral check confirms child stayed the spine on asana004 (identical to @baseline) and intercom001 (parts-aggregate LEFT JOIN conversations, join anchored backwards).

### Summary

Smoke ran the 4 grain-spine targets + asana001 sentinel; clean strict audit,
stratified_pass_at_1 = 0.2 (only the sentinel passed). Zero targets flipped and
distance-to-pass is unchanged vs @baseline (asana004/005 `Got 3`, intercom001/003
`Got 7`). Behavioral extraction of the final committed SQL shows the rule was NOT
implemented: asana004's `int_asana__project_user_agg` is structurally identical to
@baseline (child `int_asana__project_user` is the FROM spine, GROUP BY upward), and
intercom001's `intercom__threads` spines off the parts aggregate and LEFT JOINs
conversations (join anchored backwards), so zero-child entities stay dropped. The
solver added `_fivetran_active` to both sides on intercom (a surface nod) but never
moved the entity table to the FROM spine. Recommend NO-GO — a prose Implementation
rule is inert on the committed model, mirroring h0008's inert Finalization check.

## Stage Report: conclude

- DONE: Write ## Verdict — REJECTED at smoke (pre-full, NO-GO) with the score/audit evidence and the inert-mechanism deep-dives.
  Verdict cites 5/5 completed, 0 errored, strict audit CLEAN {clean:5,tainted:0}, score 0.2 (1/5), sentinel held, all 4 targets FAIL with unchanged Got 3 / Got 7; mechanism = rule inert (asana004 identical to @baseline; intercom001 join wired backwards). "Talks/partially-gestures but doesn't do."
- DONE: State the META-FINDING across h0008 (0/7), h0009 (1/6), h0010 (0/4) — README-prose levers at gpt-5.5/xhigh largely don't change committed SQL; asana002 win was a mechanical type-contract match. @baseline 622bdedac572b479 untouched, nothing promoted.
  Recorded in the ## Verdict META-FINDING paragraph; also reflected in memory ade-bench-instruction-lever-taxonomy.md.
- DONE: Do NOT file a follow-up hypothesis; note the next move is a captain strategy decision (worked-example/few-shot skeleton vs accepting an execution ceiling vs non-prose approach). Frontmatter left for the FO.
  Stated explicitly in the ## Verdict "Next move" paragraph; no new hypothesis filed; no promotion / registry add performed.

### Summary

h0010 is REJECTED at smoke (NO-GO); @baseline stays 622bdedac572b479, nothing promoted.
The grain diagnosis was correct but the prose Implementation rule was behaviorally inert —
the solver did not translate it into the committed SQL (asana004 byte-identical to
@baseline; intercom001 join anchored backwards). This completes a three-hypothesis
meta-pattern (h0008 0/7, h0009 1/6, h0010 0/4): README-prose levers at this model/effort
rarely restructure committed SQL, with the lone win being a mechanical type-contract match.
No follow-up hypothesis filed — the next move is a captain strategy decision. Frontmatter
left for the first officer.
