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
    - from: smoke
      to: conclude
      label: smoke cleanly falsifies the hypothesis; reject without a full run
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

The ensign authors the variant, then a gatekeeper subagent pre-reviews it and records an
advisory recommendation in the hypothesis file. **You make the final gate decision, informed
by that recommendation.**

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
     is spec-side only. **If the instruction is generative** (fires on every task, not gated
     on a precondition that limits it to the targets), `benchmark.tasks` MUST also carry a
     **regression panel** — ≥1 currently-passing `@baseline` task from each family OTHER than
     the targets (airbnb / ana-eng / asana / f1 / intercom / quickbooks) — as canaries (see
     the `smoke` stage; enforced by gatekeeper G8).
  4. Freeze both:
     `uv run --project ../razorback rk freeze --allow-missing specs/h<NNNN>-<slug>.yaml` and
     `uv run --project ../razorback rk freeze --allow-missing specs/h<NNNN>-<slug>.smoke.yaml`.
  5. **Run the gatekeeper.** Dispatch a review subagent that applies
     `_gatekeeper/propose-review-guideline.md` to the variant artifacts (the forked solver
     README diff vs its parent, the two spec diffs, the frozen files, and the hypothesis body)
     and writes a `## Gatekeeper review` block into the hypothesis file: a per-rule
     PASS/WARN/FAIL table plus an overall **APPROVE / REVISE / REJECT** recommendation with a
     one-line rationale. The gatekeeper is advisory — it does not pass or block the gate.
- **Gatekeeper (advisory pre-review):** its recommendation is input to your decision, not a
  substitute for it. A rule the gatekeeper marks FAIL is a likely reject; tune the bar by
  asking an agent to update `_gatekeeper/propose-review-guideline.md` on demand (it is not
  auto-updated; the gatekeeper re-reads it fresh each run).
- **Gate — you reject if:** the README leaks ground truth (its no-external-reference /
  leak-guard prose is removed or weakened); the FULL spec differs from baseline in anything other than
  `experiment:` + `solver_workflow:` (the smoke spec additionally adds `benchmark.tasks`);
  `agent.kind` ≠ `spacedock_solver` or `runtime` ≠ `codex`.
- **Good:** exactly one README idea changed; leak-guard intact; `diff` of the two specs
  shows only the two allowed fields; gatekeeper recommendation recorded.
- **Bad:** multiple knobs changed; leak-guard relaxed; advancing past a gatekeeper REJECT
  without recording why.

### `smoke`  *(🚦 go/no-go gate)*

A focused pre-flight on the hypothesis's **target datasets** via the smoke spec
(its `benchmark.tasks`). **You review before committing the full run.** *(Budget caps
deferred — this is a worthiness gate.)*

- **Inputs:** the frozen smoke spec `specs/h<NNNN>-<slug>.smoke.frozen.yaml`.
- **Smoke-set composition.** Targets + a stable-pass sentinel. **If the instruction is
  generative** (fires on every task, not gated on a precondition), the smoke set MUST also
  include a **regression panel** — ≥1 currently-passing `@baseline` task from each family
  OTHER than the targets (airbnb / ana-eng / asana / f1 / intercom / quickbooks) — as canaries.
  A generative change can regress *anywhere it fires*, and a targets-only smoke is structurally
  blind to that: h0009 looked like a GO on its 7-task targeted smoke, then lost **−3** at full
  scale on f1/quickbooks passers the smoke never ran. **A canary dropping FAIL is a NO-GO
  regardless of how many targets flipped.**
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
- **Post-run deep-dive (REQUIRED every smoke — whether GO or NO-GO).** Do not stop at the
  score. For each target task, compare the smoke cell against the same task in `@baseline`
  (`rk registry resolve run @baseline`):
  1. **Verdict delta** — did it flip FAIL→PASS, or not? Did the sentinel hold?
  2. **Distance-to-pass** — the dbt `Got N` mismatch count in `verifier/test-stdout.txt`,
     smoke vs `@baseline`. **Unchanged `Got N` ⇒ the lever was inert on that cell** — a cheap
     check to run before reading any transcript.
  3. **Behavioral why** — for at least one flipped (if any) and one still-failing target,
     read the cell transcripts (`agent/codex.txt` + the ensign `agent/sessions/<…>.jsonl`)
     and extract the **final committed artifact** (the model SQL the solver actually wrote).
     Classify each result: *flipped because the change reached the committed SQL* /
     *inert — change only discussed, not implemented* / *closer but still failing* /
     *instruction inapplicable (no analog / never triggered)*. Acknowledging an instruction
     in reasoning is NOT evidence — verify the artifact.
  Write the full per-task detail (a flip/distance/why table + the behavioral read) into
  `## Smoke result` and `## Behavioral analysis`.
- **Report to the captain in plain language.** The entity gets the full detail; the captain
  gets a SIMPLE-WORDS on-screen summary at the gate — what flipped, did we get closer, and
  (if NO-GO) why the hypothesis didn't work — not the raw tables. Lead with the go/no-go and
  the one-line reason.
- **Gate:** worthwhile (the change moved the targeted tasks, or at least did not regress
  them) → `full`; flawed but revisable → back to `hypothesis`; cleanly falsified (e.g. 0
  flips, lever inert) → `conclude` (REJECTED), recording the deep-dive as the evidence.
- **Good:** smoke exercises the changed behavior; audit clean before the score is trusted;
  every NO-GO carries a behavioral *why* backed by the committed artifact.
- **Bad:** advancing on a smoke that never exercised the change; scoring without a clean
  audit; reporting a NO-GO as just a number with no artifact-level reason; burying the
  captain in raw detail instead of a plain-language read.

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
- **Required questions every analyze report MUST answer** (in `## Run result` /
  `## Behavioral analysis` — so the captain reads them, not extracts them):
  1. **Net + full per-task ledger** — absolute score vs `@baseline` and paired delta + CI;
     AND *every* task that changed verdict in *both* directions (FAIL→PASS gains **and**
     PASS→FAIL regressions), each with its mechanism. Never report only the gains.
  2. **Smoke vs full** — if smoke was a GO, why did the full verdict differ? Name exactly what
     the smoke set could not see (e.g. regressions on families it didn't sample).
  3. **Already-correct-and-broken** — for each regression, was the task *passing* at
     `@baseline`? Call out damage to working code explicitly; distinguish "failed to help"
     from "broke a passer."
  4. **Was the change executed?** — for representative gains and regressions, did the
     *committed artifact* actually change? Classify: executed-and-helped / executed-and-hurt /
     inert (discussed-not-done) / premise-falsified (followed but target not local). Verify
     the artifact, not the chatter.
  5. **Prevention + next move** — concrete and actionable: how to keep the gains without the
     harm (scoping guardrails), how to catch it earlier (smoke canaries / G8), and the
     recommended next step (do NOT reflexively file if the lever family is exhausted —
     escalate to the captain).
- **Report to the captain in plain language.** Keep the full detail (tables, CIs, SQL) in the
  entity; give the captain a SIMPLE-WORDS on-screen summary — net result, what flipped each
  way, why, and the recommendation. Lead with the headline; never make the captain read raw
  tables to learn the verdict.
- **Tooling note:** `rk runs diff` can raise `TypeError` on ade-bench run-dirs (outcomes carry
  `query_id: null`, keyed on `trial_name`). If so, compute the paired delta directly from
  `per_trial_outcomes.json` (pair by task slug) and say you did — it is a harness data-shape
  limitation, not a run defect.
- **Good:** verdict cites the diff CI + adjusted p; behavioral findings name specific
  failure mechanisms; all five required questions answered; regressions named as damage to
  passers; captain gets a plain-words summary.
- **Bad:** reading a within-CI wobble as a win; a score with no behavioral read; reporting
  only the gains and omitting the regressions; a report the captain must interrogate to learn
  the flips, the prevention, or the next move.

### `conclude`  *(terminal — hypothesis path)*

- **Promote if** the paired delta clears the tripwire (CI excludes a regression) on a
  clean audit:
  ```bash
  uv run --project ../razorback rk baseline promote <variant-run-dir>
  uv run --project ../razorback rk registry add run baseline <variant-run-dir>
  ```
  (updates `@baseline` in `razorback-research.toml`).
- **Record the learnings in the entity file — not only in operator memory.** The entity is
  the portable, cross-machine experiment record. Write the distilled lessons into
  `## Behavioral analysis` and `## Verdict`: the failure mechanism, whether the change
  reached the committed artifact, the distance-to-pass deltas, and any transferable rule
  (what kind of lever lands vs is inert). Memory is a convenience mirror; the entity body is
  the source of truth a teammate on another machine will read.
- **Derive new hypotheses from the deep-dive findings.** Turn the smoke/analyze behavioral
  read into concrete next bets (each ONE README change, falsifiable, with named target
  datasets). **But do not reflexively file when the evidence says the lever family is
  exhausted** — if a meta-pattern has emerged (e.g. several hypotheses of the same kind all
  inert), surface the candidate directions to the captain as a strategy decision instead of
  auto-filing another doomed variant. When you do file, it is ONE follow-up
  `h<NNNN>-<slug>.md` (status `hypothesis`) forking the current `@baseline`.
- **Verdict + archive.** Set `verdict: PASSED` (promoted / ran cleanly to a real result) or
  `REJECTED` (cleanly falsified, e.g. NO-GO at smoke); archive.

> **Reached `conclude` from `smoke`?** A cleanly-falsified hypothesis routes
> `smoke → conclude` (REJECTED) without a `full` run — the smoke deep-dive is the evidence
> of record. `full`/`analyze` only run when smoke is a GO.

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

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
```

## Commit Discipline

Commit at every stage transition and entity-body update; variant specs + solver READMEs
are tracked, `runs/` stays gitignored.
