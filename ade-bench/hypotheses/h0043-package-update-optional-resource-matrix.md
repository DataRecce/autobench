---
id: h0043
title: Package-update optional-resource matrix -- when an installed package update exposes vars that disable resources, diagnose the var matrix first and gate only the affected dependency chain
status: hypothesis
kind: hypothesis
source: Captain request 2026-06-10 after asana002 decision-fork analysis; follows h0033 green-but-inert cast result and the Round 1 + Round 2 flipped-task choice map. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-10T07:17:29Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`asana002` is no longer treated as a type-cast target. h0033 showed the target can
flip, but the prescribed `::type` cast never appeared in committed SQL. The actual
green artifact was a structural package-migration repair: Fivetran's Asana package
made tag/task-tag resources optional, while downstream project models still
unconditionally referenced the tag chain. The successful repair gated the affected
models, refs, joins, and tag outputs with existing package vars such as
`asana__using_tags` and `asana__using_task_tags`.

**Falsifiable claim (the single solver-README change -- Implementation diagnostic
policy only):** adding a package-update optional-resource matrix rule will make the
solver reliably choose the `asana002` structural repair path: first inspect package
vars and optional-resource behavior, then repair the affected dependency graph with
the same existing vars. The rule should prevent the solver from starting with
model casts, raw seed/source edits, `dbt_project.yml` seed column types, or broad
package-convention copying when the visible failure is a disabled-resource
dependency.

**The single proposed README text (B variant):**

```text
When a task says an installed dbt package was updated, first classify package vars
and optional-resource behavior before editing. If a downstream model
unconditionally refs a package resource that can be disabled by an existing
package var, prefer a package-migration compatibility diagnostic: run or consider
a small disabled-var compile matrix and then repair the dependency graph with the
same existing vars. Do not start from casts, raw seed edits, or broad package
copying unless the optional-resource matrix is clean and another visible error
remains.
```

For `asana002`, the intended diagnostic is the tag/task-tag var matrix. The
intended repair family is:

- gate the relevant tag/task-tag intermediate models with existing package vars;
- conditionally include tag CTEs, refs, joins, and final columns in
  `asana__task`;
- preserve default behavior when tags/task-tags are enabled;
- emit stable `null` / `0` placeholders only where a final model must keep its
  shape when the optional resource is disabled;
- do not cast model columns, alter raw seeds/sources, change seed `column_types`,
  or apply broad package conventions outside the affected chain.

**Why this differs from h0033.** h0033 tried to force a mechanical model-layer
cast. The run passed, but the artifact proved the cast rule was inert: zero
`::<type>` casts appeared, and the actual fix was optional tag gating. h0043
therefore changes the decision policy from "find a representation mismatch" to
"first test package var optionality on package-update tasks." The artifact proof
required at smoke is the opposite of h0033: a successful run must contain the
optional-resource gating patch and must not contain a cast/seed-column-type fix.

**Pre-smoke subagent decision-fork evidence (proxy, not a score result).** We ran
fresh subagents with `fork_context=false`, no tools, no repo inspection, no hidden
verifier output, and only visible task context. The decision fork was:
package-migration optional tag gating vs model SQL cast vs raw seed/column-type
edit vs broad package copy.

Calibration with the disabled-resource compile error included:

| Variant | Rule | Optional-resource gating | Cast / seed / broad-copy |
|---|---|---:|---:|
| A | Weak baseline-style "smallest task-relevant change" | 2/2 | 0/2 |
| B | Package-update optional-resource rule | 2/2 | 0/2 |
| C | Strong matrix + no-cast guard | 2/2 | 0/2 |

Pre-diagnostic probe without the compile error, only task text + tag vars +
unconditional tag refs:

| Variant | Diagnostic path selected | Optional-resource gating | Cast / seed / broad-copy |
|---|---|---:|---:|
| A | `vars_disabled_compile_matrix` | 2/2 | 0/2 |
| B | `vars_disabled_compile_matrix` | 2/2 | 0/2 |
| C | `vars_disabled_compile_matrix` | 2/2 | 0/2 |

Follow-up B-only pre-diagnostic probe:

| Variant | Runs | `vars_disabled_compile_matrix` | Optional-resource gating | Cast / seed / broad-copy |
|---|---:|---:|---:|---:|
| B | 10 | 10 | 10 | 0 |

Total B evidence across both B batches: **14/14** chose the desired diagnostic and
repair family. The observed proxy wrong-branch rate for B is 0/14.

Honest caveat: the weak A rule also chose the desired branch in 4/4 proxy probes
when the visible tag-var context was included. That means this hypothesis is not
claiming B uniquely discovers the repair. It claims B turns the visible signal
into an explicit, smoke-auditable procedure so the real solver is less likely to
wander into the exhausted cast family or broad package-copy family.

**Falsification path.** h0043 fails if real `rk` smoke on `ade-bench-asana002`
does not patch the optional tag/task-tag chain, or if the committed artifact
starts with any of the known wrong families: model `::type` casts, raw seed/source
edits, seed `column_types`, or broad package-convention copying. It also fails if
the rule regresses canaries by firing outside package-update optional-resource
tasks.

**Target dataset.** Primary target: `ade-bench-asana002`. The expected movement is
to make the already-observed structural package-migration repair reproducible and
attributable, not to re-test the rejected cast family.

**Proposed smoke design.** Use a focused smoke panel:

- target: `ade-bench-asana002`;
- h0009/h0033 bleed canaries: `ade-bench-f1001`, `ade-bench-quickbooks003`;
- same-family sentinel: `ade-bench-asana001`;
- cross-family passers if the gatekeeper wants a wider panel:
  `ade-bench-airbnb001`, `ade-bench-ana-eng001`.

The decisive artifact read is `asana002`, not the panel mean:

1. committed patch touches the affected Asana models, expected candidates
   `models/asana__task.sql`, `models/intermediate/int_asana__task_tags.sql`, and
   `models/asana__tag.sql`;
2. patch contains package-var gating for tag/task-tag behavior;
3. patch contains no model `::type` cast as the load-bearing fix;
4. patch does not edit raw seeds/sources or seed `column_types`;
5. target passes on clean strict audit and canaries do not regress.

**Scope.** Solver README only. No benchmark, runtime, model, sampling, trials, or
spec-shape change. Leak guard remains intact; the rule references only local task
instructions, package vars, local package artifacts, model refs, and local compile
behavior. It does not mention hidden `AUTO_*` tests, `solution__*`, verifier
output, expected values, or public package sources.

## Acceptance criteria

**AC-1 -- Exactly one README policy change; specs differ only in allowed fields.**
Verified at propose by diffing the h0043 solver README against
`solver_workflows/codex-ade-dbt-minimal/README.md`: one Implementation diagnostic
policy block added, leak-guard prose byte-identical, no hidden-test/solution/
verifier references. Full spec diff vs `specs/baseline.yaml` shows only
`experiment:` and `solver_workflow:`; smoke spec adds only `benchmark.tasks`.

**AC-2 -- Every score is paired with strict clean audit and captured traces.**
Each `rk score` must cite `rk audit --policy strict` on the same run-dir with
`tainted: 0`, `coverage_missing: 0`, and captured agent traces.

**AC-3 -- Decision-policy evidence is artifact based.**
For `asana002`, read the committed patch, not the transcript narration. Classify
whether the patch is optional-resource gating, type cast, raw seed/column-type
edit, broad package copy, or unclear. Transcript claims such as "matched the
package" do not count without committed files.

**AC-4 -- h0043 is promoted only if the optional-resource path lands.**
Promotion requires `asana002` to pass with a committed optional tag/task-tag
gating repair and zero use of the known wrong repair families as the load-bearing
change. A green target with no optional-resource gating artifact is a green-but-
inert result, not a GO.

**AC-5 -- No regression canary loss.**
All baseline passers in the smoke panel must remain pass. Any canary regression
is a NO-GO unless artifact analysis proves it is unrelated single-trial variance
and the captain explicitly accepts that risk.
