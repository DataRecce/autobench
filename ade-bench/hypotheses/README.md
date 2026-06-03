---
commissioned-by: spacedock@0.12.1
entity-type: hypothesis
entity-label: hypothesis
entity-label-plural: hypotheses
id-style: slug
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
    - name: smoke
      gate: true
    - name: full
    - name: analyze
    - name: conclude
      terminal: true
  transitions:
    - from: concept
      to: ideate
      label: fan a concept out into candidate hypotheses
    - from: ideate
      to: expanded
      label: the concept has been turned into hypotheses
    - from: hypothesis
      to: propose
      label: begin authoring the variant README + spec
    - from: propose
      to: smoke
      label: README + spec pass the leak-guard gate
    - from: smoke
      to: full
      label: smoke worthwhile; commit to the full run
    - from: smoke
      to: hypothesis
      label: smoke surfaces a flawed change; revise
    - from: full
      to: analyze
      label: full run complete; interpret evidence
    - from: analyze
      to: conclude
      label: verdict written; promote or discard
---

# Run ade-bench through razorback — autoresearch workflow

This workflow tunes the **solver-workflow README** (`../solver_workflows/<variant>/README.md`)
to push ade-bench's `stratified_pass_at_1` above the **9/48 (0.1875)** baseline. razorback
runs and scores each variant; this workflow ideates, gates, and analyzes.

Two entity kinds share this directory:

- a **concept** (`concept-<slug>.md`, flat) is a research direction; `ideate` fans it
  out into many hypotheses — *breadth*;
- a **hypothesis** (`h<NNNN>-<slug>.md`, flat; folder form `h<NNNN>-<slug>/index.md`
  allowed when evidence accumulates) is one testable README change, run end-to-end;
  `conclude` may file one failure-driven follow-up — *depth*.

Both birth mechanisms are prompt-driven: the acting ensign writes the new entity file.

## Repo conventions (full detail in the repo-root `AGENTS.md`)

- Run `rk` from `ade-bench/`: `uv run --project ../razorback rk <args>`.
- Always pass `--runs-dir runs`; prefer `rk run --explain` before a full run.
- Before any `rk run`, export `RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"`.
- **`rk run … --runs-dir` is long-running (30 min–5 hr) and exceeds the Bash-tool timeout —
  never run it in the foreground.** Launch it detached with `nohup`, redirect stdout+stderr
  to a tmp log file, and record the PID to a tmp file, so the FO or ensign can trace liveness
  (`kill -0 $(cat <pidfile>)`) and progress (`tail -f <log>`) across turns without blocking.
  The fast `--explain` / `rk audit` / `rk score` calls stay in the foreground. `drivers/matrix.sh`
  invokes `rk run` internally — background it the same way. See the `smoke`/`full` stages for
  the exact pattern.
- The independent variable is ONLY the solver README. A variant spec differs from
  `specs/baseline.yaml` only in `experiment:` + `solver_workflow:`. `trials: 1` always.

## File Naming

- Concepts: `concept-<slug>.md` (lowercase, hyphens).
- Hypotheses: `h<NNNN>-<slug>.md`, next available `hNNNN`; the descriptive name lives in
  `title`. With `id-style: slug` the slug is the identity; if `id` is set it must match.

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Optional under `id-style: slug`; when set, matches the slug. |
| `title` | string | Human-readable name. |
| `status` | enum | concept, ideate, expanded, hypothesis, propose, smoke, full, analyze, conclude. |
| `kind` | enum | `concept` or `hypothesis` (which path this entity is on). |
| `source` | string | Where it came from (concept fan-out, prior verdict, captain hunch). |
| `started` / `completed` | ISO 8601 | When work began / reached a terminal stage. |
| `verdict` | enum | PASSED or REJECTED — set at a terminal stage. |
| `score` | number | Priority 0.0–1.0 (optional). |
| `worktree` | string | Empty (this workflow runs inline). |

## Stages

### `concept`  *(initial — concept path)*

A research direction is filed (by you or the first officer): a plain-English theme +
rationale.

- **Inputs:** a research lead, a prior verdict's follow-ups, or a captain hunch.
- **Outputs:** a `concept-<slug>.md` body stating the direction and why it might raise
  the score.
- **Good:** a concrete, testable direction tied to an observed failure mode.
- **Bad:** vague "make it better"; a direction with no hypothesis to derive from it.

### `ideate`

An ensign reads the concept + the current `@baseline` solver README + prior learnings
and **writes several `h<NNNN>-<slug>.md` hypothesis entities** (status `hypothesis`),
each naming the specific solver-README change it will make. Then the concept advances to
`expanded`.

- **Inputs:** the concept body; `../solver_workflows/codex-ade-dbt-minimal/README.md` (or the current
  `@baseline` solver); the latest analyze findings.
- **Outputs:** 2–5 new hypothesis entities, each with a falsifiable claim + acceptance
  criteria; the concept marked `expanded`.
- **Good:** each hypothesis changes ONE idea, is falsifiable, and names its target
  datasets.
- **Bad:** one mega-hypothesis; hypotheses that restate the concept without a concrete
  README change.

### `expanded`  *(terminal — concept path)*

The concept has been turned into hypotheses; archived.

### `hypothesis`  *(initial — hypothesis path)*

A fully-formed, queued hypothesis. Auto-advances to `propose`.

- **Inputs:** an `ideate` fan-out or a `conclude` follow-up.
- **Outputs:** the body's `## Hypothesis` (the claim + the single README change) and
  `## Acceptance criteria` (the verdict, e.g. "the paired `rk runs diff` delta vs
  `@baseline` clears the tripwire on `stratified_pass_at_1`").
- **Good:** falsifiable; names the target datasets for smoke.
- **Bad:** success criteria invented after seeing results.

### `propose`  *(🚦 leak-guard gate)*

The ensign authors the variant. **You review at the gate.**

- **Inputs:** the hypothesis claim.
- **Outputs:**
  1. `cp -r ../solver_workflows/codex-ade-dbt-minimal ../solver_workflows/h<NNNN>-<slug>` (fork
     the current `@baseline` solver dir — `codex-ade-dbt-minimal` is the seed baseline), then
     edit its `README.md` — the one variable.
  2. `cp ../specs/baseline.yaml ../specs/h<NNNN>-<slug>.yaml`, set `experiment:` to
     `ade-bench-h<NNNN>-<slug>` and `solver_workflow:` to
     `./solver_workflows/h<NNNN>-<slug>`. This is the FULL spec — no task selector.
  3. Make the smoke spec: `cp ../specs/h<NNNN>-<slug>.yaml ../specs/h<NNNN>-<slug>.smoke.yaml`
     and add `benchmark.tasks: [<target dataset IDs>]` (a general change with no targets
     uses `benchmark.n_tasks: 5` instead). `rk run` has NO task-selector flag — subsetting
     is spec-side only.
  4. Freeze both:
     `uv run --project ../razorback rk freeze --allow-missing specs/h<NNNN>-<slug>.yaml` and
     `uv run --project ../razorback rk freeze --allow-missing specs/h<NNNN>-<slug>.smoke.yaml`.
- **Gate — you reject if:** the README leaks ground truth (its no-external-reference /
  leak-guard prose is removed or weakened); the FULL spec differs from baseline in anything other than
  `experiment:` + `solver_workflow:` (the smoke spec additionally adds `benchmark.tasks`);
  `agent.kind` ≠ `spacedock_solver` or `runtime` ≠ `codex`.
- **Good:** exactly one README idea changed; leak-guard intact; `diff` of the two specs
  shows only the two allowed fields.
- **Bad:** multiple knobs changed; leak-guard relaxed.

### `smoke`  *(🚦 go/no-go gate)*

A focused pre-flight on the hypothesis's **target datasets** via the smoke spec
(its `benchmark.tasks`). **You review before committing the full run.** *(Budget caps
deferred — this is a worthiness gate.)*

- **Inputs:** the frozen smoke spec `specs/h<NNNN>-<slug>.smoke.frozen.yaml`.
- **Outputs (from `ade-bench/`):**
  ```bash
  uv run --project ../razorback rk run specs/h<NNNN>-<slug>.smoke.frozen.yaml --explain   # $0, fast, foreground
  # rk run is long (30 min–5 hr) > Bash-tool timeout — launch detached, log to tmp, record PID:
  LOG=/tmp/rk-h<NNNN>-smoke.log
  nohup uv run --project ../razorback rk run specs/h<NNNN>-<slug>.smoke.frozen.yaml --runs-dir runs > "$LOG" 2>&1 &
  echo $! > "$LOG.pid"   # trace: kill -0 $(cat "$LOG.pid") => alive ; tail -f "$LOG" => progress
  # Poll until the PID exits (across turns — do NOT block a single Bash call on it), THEN:
  uv run --project ../razorback rk audit <run-dir> --policy strict
  uv run --project ../razorback rk score <run-dir>
  ```
  Confirm `<run-dir>/<cell>/subagent-trace-manifest.json` has `captured > 0`. Capture the
  focused score + clean-audit attestation in `## Smoke result`.
- **Gate:** worthwhile (the change moved the targeted tasks, or at least did not regress
  them) → `full`; flawed → back to `hypothesis`.
- **Good:** smoke exercises the changed behavior; audit clean before the score is trusted.
- **Bad:** advancing on a smoke that never exercised the change; scoring without a clean
  audit.

> **Baseline / first run skips `smoke`** (`propose → full`): the 9/48 anchor is a direct
> full run, then `conclude` binds `@baseline`.

### `full`

The full 48-task run on the FULL frozen spec (`h<NNNN>-<slug>.frozen.yaml`, no task selector).

- **Outputs (from `ade-bench/`):**
  ```bash
  # rk run is long (30 min–5 hr) > Bash-tool timeout — launch detached, log to tmp, record PID:
  LOG=/tmp/rk-h<NNNN>-full.log
  nohup uv run --project ../razorback rk run specs/h<NNNN>-<slug>.frozen.yaml --runs-dir runs > "$LOG" 2>&1 &   # all 48
  echo $! > "$LOG.pid"   # trace: kill -0 $(cat "$LOG.pid") => alive ; tail -f "$LOG" => progress
  # Poll until the PID exits (across turns — do NOT block a single Bash call on it), THEN:
  uv run --project ../razorback rk audit <run-dir> --policy strict
  uv run --project ../razorback rk score <run-dir> --format json
  ```
  (Or background `bash drivers/matrix.sh --specs 'specs/h<NNNN>-<slug>.frozen.yaml'` the same
  nohup+PID way — it invokes `rk run` internally and is equally long — to chain
  run + `captured>0` + audit + score + ledger.) Record the run-dir path + headline in
  `## Run result`.
- **Good:** the full spec uses the SAME solver README as the smoke spec (only the task
  set differs); audit clean before the score is recorded.
- **Bad:** methodology drift between smoke and full.

### `analyze`

Interpret the full run against `@baseline` — quantitatively and behaviorally.

- **Quantitative (from `ade-bench/`):**
  ```bash
  uv run --project ../razorback rk runs diff "$(uv run --project ../razorback rk registry resolve run @baseline)" <variant-run-dir>
  uv run --project ../razorback rk score <variant-run-dir> --format json   # absolute vs paper_baseline 0.1875
  ```
  Paste the paired delta (CIs, adjusted p) + absolute score into `## Run result`.
- **Behavioral (§5.6 of the spec) — per task whose verdict changed vs `@baseline`,
  plus a sample of persistent failures, read the cell
  `runs/<experiment>/<hash>/<task>__<short>/`:**
  - `result.json` + `verifier/reward.txt` → binary verdict.
  - `verifier/test-stdout.txt` → **distance to pass**: `[ade-bench] expected_test_count=N`,
    the dbt `Done. PASS=… ERROR=… SKIP=… TOTAL=…` line, which target checks ran
    (`Including: <check>.sql`), which failed, and the concrete failure.
  - `agent/codex.txt` → the **main agent** transcript (plan, tool calls, ensign
    dispatches, validation evidence).
  - `subagent-trace-manifest.json` → dispatch summary (`captured`, `subagent_type:
    spacedock:ensign`).
  - `agent/sessions/<year>/…` → the **sub-agent (ensign)** transcripts.
  Write a `## Behavioral analysis` block answering, per task: (1) **method adherence** —
  did the agent + ensigns actually execute the README's prescribed method? (2) why it
  works; (3) why it fails (and the per-task distance-to-pass `checks_passed /
  expected_test_count`).
- **Good:** verdict cites the diff CI + adjusted p; behavioral findings name specific
  failure mechanisms.
- **Bad:** reading a within-CI wobble as a win; a score with no behavioral read.

### `conclude`  *(terminal — hypothesis path)*

- **Promote if** the paired delta clears the tripwire (CI excludes a regression) on a
  clean audit:
  ```bash
  uv run --project ../razorback rk baseline promote <variant-run-dir>
  uv run --project ../razorback rk registry add run baseline <variant-run-dir>
  ```
  (updates `@baseline` in `razorback-research.toml`).
- **Then** file ONE follow-up `h<NNNN>-<slug>.md` (status `hypothesis`) using analyze's
  behavioral findings (method-adherence + failure mechanisms), forking the new
  `@baseline`. Set `verdict: PASSED` (ran cleanly) or `REJECTED` (failed to reach analyze
  cleanly); archive.

## Champion (`@baseline`)

The reigning champion is the `@baseline` run-dir in `razorback-research.toml`. New
hypotheses fork from its solver README; `analyze` diffs against its run-dir.

## Templates

Concept (`concept-<slug>.md`):
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

<the theme and why it might raise the score>
```

Hypothesis (`h<NNNN>-<slug>.md`):
```yaml
---
id: h<NNNN>
title: <one-line change>
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

The falsifiable claim and the single solver-README change it makes. Target datasets: <ids>.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h<NNNN>-<slug>.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`.**

## Smoke result

## Run result

## Behavioral analysis

## Verdict
```

## Commit Discipline

Commit at every stage transition and entity-body update; variant specs + solver READMEs
are tracked, `runs/` stays gitignored.
