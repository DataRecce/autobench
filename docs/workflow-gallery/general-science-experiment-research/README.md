---
commissioned-by: spacedock@0.12.1
entity-type: experiment
entity-label: experiment
entity-label-plural: experiments
id-style: slug
state: $inline
stages:
  defaults:
    worktree: false
    concurrency: 1
  states:
    - name: concept
      initial: true
    - name: ideate
    - name: expanded
      terminal: true
    - name: hypothesis
      initial: true
    - name: propose
      gate: true
    - name: pilot
      parked: true
      gate: true
    - name: full
      parked: true
    - name: analyze
    - name: conclude
      terminal: true
  transitions:
    - from: concept
      to: ideate
      label: turn a research direction into candidate experiments
    - from: ideate
      to: expanded
      label: the concept has been expanded into hypotheses
    - from: hypothesis
      to: propose
      label: prepare the protocol and evidence plan
    - from: propose
      to: pilot
      label: protocol passes review and can run a pilot
    - from: pilot
      to: full
      label: pilot justifies the full experiment
    - from: pilot
      to: hypothesis
      label: pilot found a revisable flaw
    - from: pilot
      to: conclude
      label: pilot falsified the hypothesis
    - from: full
      to: analyze
      label: full experiment complete; interpret evidence
    - from: analyze
      to: conclude
      label: verdict and follow-up routing recorded
---

# General Science Experiment Research Workflow

This Spacedock workflow runs an iterative science research loop. It turns broad
research directions into falsifiable hypotheses, reviews each proposed protocol,
runs a small pilot before committing to the full experiment, analyzes both
quantitative results and behavioral evidence, and records portable learnings for
the next cycle.

The workflow was extracted from a production auto-research loop and generalized
for scientific experiments. Replace the adapter-specific commands in this README
with your lab's execution commands, dataset loaders, instrument scripts,
simulator, evaluation runner, or analysis notebooks.

## Core Discipline

- **One independent variable per hypothesis.** Change one protocol element at a
  time: treatment, prompt, model, reagent, parameter, dataset slice, measurement
  method, or analysis rule. If two things change, file two hypotheses or declare
  a compound hypothesis explicitly.
- **Fixed controls.** Hold controls, sampling plan, model/runtime, instrument
  setup, inclusion criteria, randomization, and scoring method constant unless
  the hypothesis is specifically about one of them.
- **Pilot before full.** A focused pilot checks whether the intervention fires,
  whether safety and validity checks pass, and whether the full run is worth the
  cost.
- **Clean audit before score.** Do not trust a result until provenance,
  coverage, and exclusion checks are clean.
- **Evidence over chatter.** Credit an effect only when the intervention reached
  the committed artifact or measured system, not merely when an agent or
  researcher said it did.
- **Learning is an artifact.** The experiment entity is the source of truth.
  Record the verdict, mechanisms, caveats, and follow-up routing there. Durable
  cross-experiment lessons go in `_artifacts/self-learning.md`; changes to the
  workflow itself go in `_artifacts/WORKFLOW-REFINE.md`.

## Roles

| Role | Responsibility |
|------|----------------|
| Captain | Owns research strategy and approves gates. |
| First officer | Runs the Spacedock workflow, dispatches workers, advances state, and owns waits. |
| Ensign | Performs scoped work: ideation, protocol authoring, pilot execution, analysis, and artifact reads. |
| Gatekeeper | Reviews proposed protocols against `_gatekeeper/propose-review-guideline.md`. |
| Executor | The lab runner, simulator, evaluator, agent, or external process that performs the experiment. |

## Entities

Two entity kinds share this workflow directory:

- **Concept** (`exp<NNNN>-<slug>.md`, `kind: concept`) is a research direction.
  It follows `concept -> ideate -> expanded`.
- **Hypothesis** (`exp<NNNN>-<slug>.md`, `kind: hypothesis`) is one testable
  protocol change. It follows:

```text
hypothesis -> propose -> pilot -> full -> analyze -> conclude
                         |
                         +-> hypothesis  (revisable flaw)
                         +-> conclude    (cleanly falsified)
```

Both birth mechanisms are prompt-driven: the acting worker writes the new entity
file.

This workflow uses `id-style: slug`, so the filename slug is the Spacedock
identity. The `exp<NNNN>` prefix is part of the slug, not a separate generated
frontmatter id. Keep `kind: concept` or `kind: hypothesis` in frontmatter so the
first officer knows which path the entity follows.

## File Naming

- Concepts and hypotheses share one `exp<NNNN>` slug prefix space.
- Do not set a separate `id:` field in new entities; the slug is the id.
- Use folder form (`exp<NNNN>-<slug>/index.md`) only when evidence becomes too
  large for a single markdown file.

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Human-readable title. |
| `status` | enum | `concept`, `ideate`, `expanded`, `hypothesis`, `propose`, `pilot`, `full`, `analyze`, `conclude`. |
| `kind` | enum | `concept` or `hypothesis`. |
| `source` | string | Where the entity came from. |
| `started` / `completed` | ISO 8601 | Start and terminal dates. |
| `verdict` | enum | `PASSED`, `REJECTED`, or `INCONCLUSIVE` at terminal state. |
| `score` | number | Optional priority from 0.0 to 1.0. |
| `worktree` | string | Optional working directory if the experiment needs one. |

## Stage Guide

### `concept`

A broad research direction is filed.

- **Inputs:** prior findings, literature gaps, failed experiments, reviewer
  questions, operator hunches, or a task-gap ranking.
- **Outputs:** a concept entity with `## Direction`, expected value, and known
  constraints.
- **Good:** concrete enough to generate falsifiable hypotheses.
- **Bad:** "improve results" without a suspected mechanism.

### `ideate`

An ensign reads the concept, prior learnings, current baseline protocol, and
available evidence, then writes 2-5 hypothesis entities.

- **Outputs:** hypotheses with one independent variable, named target outcomes,
  controls, acceptance criteria, and expected artifact signatures.
- **Good:** each hypothesis can be falsified by a pilot.
- **Bad:** one large hypothesis containing several unrelated interventions.

### `hypothesis`

A queued, fully formed hypothesis.

Each hypothesis should include:

- `## Hypothesis` with the falsifiable claim and the single change.
- `## Independent variable` naming exactly what changes.
- `## Held constant` naming controls and invariants.
- `## Target outcomes` naming primary and secondary outcomes.
- `## Acceptance criteria` with pass/fail thresholds and audit requirements.
- `## Risk and validity notes` for leakage, confounds, safety, and cost.

### `propose` *(gate)*

The ensign authors the protocol package, then a gatekeeper reviews it. The
captain makes the final call unless autonomous mode is explicitly enabled for a
clean happy path.

- **Inputs:** hypothesis entity, baseline protocol, prior learnings, and any
  domain constraints.
- **Outputs:** protocol diff, pilot plan, full-run plan, frozen or versioned
  execution artifacts, and a `## Gatekeeper review` block.
- **Gate presentation:** show the intervention, control set, pilot sample, target
  outcomes, expected artifact signature, cost/ETA, and the gatekeeper
  recommendation.
- **Reject if:** the protocol changes more than the declared variable, weakens
  provenance or safety rules, leaks holdout answers, uses unauthorized external
  references, changes controls without declaration, or lacks an audit path.

### `pilot` *(gate)*

A focused pilot checks whether the intervention is real, measurable, and worth a
full run.

- **Inputs:** frozen/versioned pilot protocol.
- **Pilot composition:** include target cases, at least one stable control, and
  perturbable canaries when the change is generative or broad.
- **Required analysis:** audit/provenance, outcome delta versus baseline,
  distance-to-pass or distance-to-target, and artifact-level evidence that the
  intervention actually fired.
- **Failure review:** every no-go gets a `## Failure Review` classifying the
  primary failure as `infrastructure-failure`, `diagnosis-miss`, `wrong-branch`,
  `incomplete-artifact`, `correct-artifact-still-fail`, `canary-bleed`,
  `variance-unclear`, or `safety-validity-failure`.
- **Gate:** advance to `full` only when the pilot is clean, exercised the changed
  behavior, and did not damage controls or canaries.

### `full`

Run the full experiment using the same protocol that passed pilot, with only the
declared sample-size or coverage expansion.

- **Outputs:** run directory, raw results, audit/provenance report, and headline
  score or effect estimate.
- **Good:** pilot and full differ only in declared coverage or sample size.
- **Bad:** changing method, controls, or scoring between pilot and full.

### `analyze`

Interpret the full experiment quantitatively and mechanistically.

The report must answer:

1. What is the net result versus baseline, with uncertainty where applicable?
2. Which target outcomes improved, held, regressed, or stayed unresolved?
3. Which controls or canaries moved, and why?
4. Did the independent variable actually reach the committed artifact,
   treatment, model, instrument, or measured system?
5. What confounds remain: variance, sampling, measurement, model change,
   instrument drift, contamination, leakage, or analysis bias?
6. What should happen next: stop, probe, file a follow-up, or escalate?

### `conclude`

Write the verdict and archive or promote.

- **Promote/adopt if:** the full result passes acceptance criteria on a clean
  audit and the mechanism is attributable to the declared independent variable.
- **Reject if:** the pilot or full run cleanly falsifies the hypothesis, harms
  controls, fails safety/validity checks, or produces an unattributable effect.
- **Inconclusive if:** the run is clean but underpowered, noisy, or blocked by a
  confound that cannot be resolved inside the current hypothesis.
- **Always record:** verdict, evidence, caveats, mechanism, follow-up routing,
  and one-line learning in `_artifacts/self-learning.md`.
- **Workflow changes:** if the hypothesis changed this workflow's structure, also
  finalize the entry in `_artifacts/WORKFLOW-REFINE.md`.

## Long-Running Experiments

If execution can outlive an agent turn, do not wait inside a worker. Launch via a
detached runner that writes a handle directory with:

- `pid` for diagnostics,
- `log` for combined output,
- `meta` for provenance,
- `done` as the terminal sentinel containing return code, end time, and run dir.

The first officer owns waiting by scanning handle directories at the start of
each turn. Treat `done` as the source of truth; if a process is gone but no
sentinel exists, inspect the runner's own output before declaring a crash. For
autonomous operation, schedule wakeups at the ETA and reschedule until the
sentinel lands or a wall-clock backstop triggers escalation.

## Executor Adapter

Spacedock manages the workflow state; the project supplies the command that
actually runs the experiment. When adapting this template, define one executor
entry point for both `pilot` and `full`, for example:

```bash
./scripts/run-experiment <hypothesis-id> --tier pilot --out runs/<hypothesis-id>/pilot
./scripts/run-experiment <hypothesis-id> --tier full  --out runs/<hypothesis-id>/full
```

The executor should write `meta.json`, `results.json`, `audit.json`, logs, and
artifacts under the output directory. The same method must run at both tiers;
only sample size or coverage should change. See `EXECUTOR.md` for the full
contract and examples.

## Optional Observability

If your environment records local agent sessions, `agentsview` can sync and
serve them for manual inspection:

```bash
agentsview sync
agentsview serve
```

Some Codex/Spacedock environments write parent sessions as
`agent/sessions/rollout-*.jsonl` with `thread_source=user`, and dispatched
workers with `thread_source=subagent`. If your run artifacts include a
`subagent-trace-manifest.json`, a monitor can label these as
`session:first-officer` and `subagent:<type>#N`. Treat this as optional
observability, not a requirement for using the workflow.

## Templates

Concept:

```yaml
---
title: <research direction>
status: concept
kind: concept
source:
started:
completed:
verdict:
---

## Direction

<theme, rationale, constraints, and why this direction may improve the target outcome>
```

Example concept (`exp0001-retrieval-quality.md`):

```markdown
---
title: Retrieval depth and answer quality
status: concept
kind: concept
source: initial research idea
started:
completed:
verdict:
score: 0.8
worktree:
---

## Direction

Explore whether deeper retrieval improves answer correctness without increasing
unsupported claims or latency beyond the study budget.
```

Hypothesis:

```yaml
---
title: <one-line hypothesis>
status: hypothesis
kind: hypothesis
source:
started:
completed:
verdict:
score:
worktree:
---

## Hypothesis

<falsifiable claim>

## Independent variable

<the one thing that changes>

## Held constant

<controls, runtime, sampling, scoring, inclusion criteria, environment>

## Target outcomes

<primary, secondary, controls/canaries>

## Acceptance criteria

<thresholds, audit requirements, attribution requirements>

## Gatekeeper review

## Pilot result

## Run result

## Analysis

## Failure Review

## Follow-up Routing

## Verdict
```

Example hypothesis (`exp0002-retrieval-depth-20.md`):

```markdown
---
title: Retrieval depth 20 vs 5
status: hypothesis
kind: hypothesis
source: exp0001-retrieval-quality
started:
completed:
verdict:
score: 0.9
worktree:
---

## Hypothesis

Increasing retrieval depth from 5 to 20 improves answer correctness on the
evaluation set.

## Independent variable

Retrieval depth changes from 5 to 20.

## Held constant

Same model, prompts, dataset, evaluator, scoring rubric, runtime, and random
seed.

## Target outcomes

Primary: correctness. Secondary: unsupported-claim rate and latency.

## Acceptance criteria

Accept if correctness improves by at least 5 percentage points, unsupported
claims do not increase, latency remains within the predeclared budget, and the
run has a clean audit.
```
