# Example Use Case: Academic Researcher Adapting the Template

## Persona

Dr. Maya Chen is a computational social science researcher. She studies how
students use AI tutoring systems when reading scientific papers. She is not
building Spacedock itself; she wants a repeatable research workflow that helps
her team turn research ideas into controlled experiments, run small pilots, run
full studies, and preserve the reasoning behind every accept/reject decision.

Maya's team has three recurring problems:

- research ideas are discussed in meetings but not turned into falsifiable
  hypotheses;
- pilot studies and full studies sometimes drift in methodology;
- results live in notebooks and chat threads, so later students cannot tell why
  a hypothesis was accepted, rejected, or revised.

She chooses the public **General Science Experiment Research Workflow** template
because it already encodes the shape she wants. Concepts and hypotheses are two
linked tracks:

```text
concept -> ideate -> expanded
                    |
                    +-> writes new hypothesis files

hypothesis -> propose -> pilot -> full -> analyze -> conclude
```

## Research Goal

Maya wants to test whether an AI tutor produces better learning outcomes when it
uses paper-specific retrieval rather than a generic course-note retrieval index.

Her first study question:

> Does paper-specific retrieval improve students' ability to answer conceptual
> questions about assigned scientific papers without increasing unsupported AI
> claims?

## Step 1: Maya Commissions a Workflow From the Public Template

The workflow gallery publishes these raw URLs:

```text
README: <PUBLIC_RAW_README_URL>
EXECUTOR: <PUBLIC_RAW_EXECUTOR_URL>
GATEKEEPER: <PUBLIC_RAW_GATEKEEPER_URL>
SELF_LEARNING: <PUBLIC_RAW_SELF_LEARNING_URL>
WORKFLOW_REFINE: <PUBLIC_RAW_WORKFLOW_REFINE_URL>
EXAMPLE_USE_CASE: <PUBLIC_RAW_EXAMPLE_USE_CASE_URL>
```

The maintainer replaces those placeholders with the actual public raw URLs before
publishing the gallery entry.

Maya opens Spacedock commission in her project repository and gives this prompt:

```text
Commission a workflow from these public template files for my academic research
project on AI tutoring with paper-specific retrieval:

README: <PUBLIC_RAW_README_URL>
EXECUTOR: <PUBLIC_RAW_EXECUTOR_URL>
GATEKEEPER: <PUBLIC_RAW_GATEKEEPER_URL>
SELF_LEARNING: <PUBLIC_RAW_SELF_LEARNING_URL>
WORKFLOW_REFINE: <PUBLIC_RAW_WORKFLOW_REFINE_URL>
EXAMPLE_USE_CASE: <PUBLIC_RAW_EXAMPLE_USE_CASE_URL>

Adapt it to my project. Each entity should be a research concept or hypothesis.
Keep the two-track shape: concepts go `concept -> ideate -> expanded`, and
ideate writes hypothesis files that go `hypothesis -> propose -> pilot -> full
-> analyze -> conclude`. Preserve the one-independent-variable rule, protocol
review, pilot gate, artifact-level attribution, durable learning logs, and the
project-specific executor contract. Put the generated workflow in docs/research.
```

Spacedock generates and adapts:

```text
docs/research/
  README.md
  EXECUTOR.md                         # project-specific pilot/full executor contract
  _gatekeeper/propose-review-guideline.md
  _artifacts/self-learning.md
  _artifacts/WORKFLOW-REFINE.md
  ethics-and-data.md                  # project-specific human-subjects/data handling notes
```

`docs/research/EXECUTOR.md` is not just a copy of the gallery file. It records
Maya's concrete command shape, required output schema, audit fields, and
detached-run convention.

Maya reviews `docs/research/README.md` and tightens the project-specific parts:

- the study population is undergraduate students in her course;
- the primary outcome is rubric-scored conceptual-answer quality;
- the secondary outcomes are unsupported AI claims, student completion time, and
  subjective helpfulness;
- the pilot sample is 8 students and 2 assigned papers;
- the full sample is 60 students and 8 assigned papers.

She also writes `docs/research/ethics-and-data.md` with the IRB protocol id,
consent requirements, de-identification rules, data-retention policy, and the
location of private data. The workflow directory records references and hashes;
it does not commit private student data.

## Step 2: Maya Seeds a Research Concept

Maya creates the first entity:

```markdown
---
title: Paper-specific retrieval for AI tutoring
status: concept
kind: concept
source: lab planning meeting
started:
completed:
verdict:
score: 0.9
worktree:
---

## Direction

Test whether an AI tutor that retrieves from the assigned paper itself helps
students answer conceptual questions better than a tutor that retrieves only
from generic course notes.

The study should preserve the same model, interface, question set, scoring
rubric, and student recruitment criteria. The first hypotheses should isolate
retrieval source as the independent variable.
```

The concept lets the first officer fan out several candidate hypotheses without
Maya manually writing every study variant. After ideation, the concept itself
lands in `expanded`; the generated hypotheses start their own lifecycle at
`hypothesis`.

## Step 3: Spacedock Fans Out Hypotheses

During `ideate`, an ensign reads the concept and prior project notes, then writes
candidate hypotheses such as:

```text
exp0002-paper-specific-retrieval.md
exp0003-paper-plus-course-hybrid-retrieval.md
exp0004-retrieval-citation-visible-vs-hidden.md
```

Maya chooses to advance `exp0002-paper-specific-retrieval.md` first because it is
the cleanest one-variable test.

The hypothesis entity says:

```markdown
---
title: Paper-specific retrieval vs course-note retrieval
status: hypothesis
kind: hypothesis
source: exp0001-paper-specific-retrieval-for-ai-tutoring
started:
completed:
verdict:
score: 0.95
worktree:
---

## Hypothesis

An AI tutor using retrieval from the assigned paper improves student conceptual
answer quality compared with an AI tutor using retrieval from generic course
notes.

## Independent variable

Retrieval corpus changes from generic course notes to the assigned paper.

## Held constant

Same model, tutor UI, system prompt except retrieval-source wording, student
population, assigned questions, scoring rubric, evaluator instructions, runtime,
and analysis script.

## Target outcomes

Primary: rubric-scored conceptual answer quality.

Secondary: unsupported AI claims, completion time, and student helpfulness
rating.

## Acceptance criteria

Advance from pilot to full if all conditions hold:

- audit status is `clean`;
- artifacts show the tutor actually used the paper-specific retrieval index;
- no safety, consent, or data-handling issue is found;
- rubric-scored conceptual answer quality improves by at least 5 percentage
  points over control on the pilot sample;
- unsupported AI claims do not increase (`delta <= 0`);
- median completion time increases by no more than 10 percent.

For the full study, report the effect estimate with confidence intervals and
include an inter-rater agreement check for the rubric-scored answers.
```

## Step 4: Maya Adapts the Executor

The generated workflow tells Maya that Spacedock needs one command for both
pilot and full:

```bash
./scripts/run-experiment exp0002-paper-specific-retrieval --tier pilot \
  --out runs/exp0002-paper-specific-retrieval/pilot

./scripts/run-experiment exp0002-paper-specific-retrieval --tier full \
  --out runs/exp0002-paper-specific-retrieval/full
```

Maya implements `scripts/run-experiment` as a thin wrapper around her existing
study scripts:

```text
scripts/run-experiment
scripts/build_retrieval_index.py
scripts/run_tutor_sessions.py
scripts/score_student_answers.py
scripts/audit_study_run.py
```

For `--tier pilot`, the executor:

- selects 8 students and 2 papers from the predeclared pilot sample;
- builds the paper-specific retrieval index and the course-note control index;
- runs the tutor sessions;
- scores student answers with the locked rubric;
- writes `results.json`, `audit.json`, logs, and answer artifacts.

For `--tier full`, the same executor:

- selects the full predeclared sample of 60 students and 8 papers;
- uses the same index-building, session-running, scoring, and audit code;
- writes the same artifact structure under a different run directory.

The pilot and full tiers differ only in sample coverage. The treatment,
controls, scoring, consent rules, and analysis method stay fixed.

## Step 5: The Proposal Gate Catches Protocol Problems

At `propose`, Spacedock prepares the protocol package and runs the gatekeeper
checklist.

The gatekeeper checks:

- only the retrieval corpus changes;
- the pilot includes target cases and controls;
- student consent and privacy constraints are documented;
- the scoring rubric is fixed before results are seen;
- the executor records provenance and audit files;
- no holdout answers or post-hoc exclusion rules leak into the protocol;
- `docs/research/ethics-and-data.md` names the IRB/consent and privacy rules,
  while private student records remain outside the workflow directory.

Maya reviews the gate summary. If the gatekeeper finds that the pilot lacks a
course-note control group, the workflow stays at `propose` or routes back to
`hypothesis` until the design is fixed. If the protocol is clean, Maya approves
the pilot.

## Step 6: Pilot Run

The first officer dispatches the `pilot` stage, whose worker invokes:

```bash
./scripts/run-experiment exp0002-paper-specific-retrieval --tier pilot \
  --out runs/exp0002-paper-specific-retrieval/pilot
```

The executor writes:

```text
runs/exp0002-paper-specific-retrieval/pilot/
  meta.json
  protocol.md
  results.json
  audit.json
  logs/
  artifacts/
```

The pilot result shows:

- conceptual answer quality improves by 7 percentage points;
- unsupported AI claims stay flat;
- completion time increases by 4 percent, inside the budget;
- audit is clean;
- artifacts confirm the tutor actually used the paper-specific retrieval index.

Maya approves `pilot -> full`.

## Step 7: Full Run

The first officer dispatches the `full` stage, whose worker invokes the same
executor with `--tier full`:

```bash
./scripts/run-experiment exp0002-paper-specific-retrieval --tier full \
  --out runs/exp0002-paper-specific-retrieval/full
```

Because the full run may take several hours, Maya can use the detached launcher
pattern from `EXECUTOR.md`. The first officer watches for the `done` sentinel,
then reads `audit.json` and `results.json`.

## Step 8: Analyze and Conclude

At `analyze`, Spacedock compares full results with the baseline condition and
requires the report to answer:

- Did conceptual-answer quality improve?
- Did unsupported claims increase?
- Did any control or canary regress?
- Did the independent variable actually reach the measured system?
- Are there remaining confounds such as student imbalance, paper difficulty, or
  evaluator drift?

At `conclude`, Maya records one of three outcomes:

- `PASSED`: paper-specific retrieval should be adopted for the next study phase;
- `REJECTED`: the intervention failed or caused unacceptable regressions;
- `INCONCLUSIVE`: the result was underpowered, noisy, or confounded.

The entity becomes the durable experiment record. A one-line lesson is added to
`_artifacts/self-learning.md`, for example:

```markdown
- **exp0002 - PASSED.** Paper-specific retrieval improved conceptual answer
  quality without increasing unsupported claims; future studies should test
  whether showing citations to students improves trust calibration.
```

## What This Example Shows

The public workflow template gives Maya the research operating system:

- concept fan-out;
- one-variable hypotheses;
- protocol review;
- pilot gate;
- full execution;
- audit and artifact attribution;
- durable conclusions.

Maya supplies the domain-specific executor and scientific judgment:

- sample definitions;
- consent and privacy constraints;
- tutor session runner;
- scoring rubric;
- analysis scripts;
- interpretation of the research result.

That division is the intended use of the public template: Spacedock manages the
research workflow, while the user's project provides the experiment executor.
