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

# Run DataAgentBench (DAB) through razorback — autoresearch workflow

This workflow tunes the **solver-workflow README** (`../solver_workflows/<variant>/README.md`)
to push codex/gpt-5.5 past the **Opus-4.8 incumbent (~0.65 / 0.6536 stratified Pass@1, resolve
`@baseline`)** on DAB. razorback runs and scores each variant; this workflow ideates, gates,
and analyzes.

The single lever per hypothesis is the codex solver's README (the three-stage
model → analyze → verify methodology). The variant solver is held FIXED at **codex/gpt-5.5,
`runtime: codex`**; we are NOT swapping models per hypothesis — only the README changes.

Two entity kinds share this directory:

- a **concept** (`concept-<slug>.md`, flat) is a research direction; `ideate` fans it
  out into many hypotheses — *breadth*;
- a **hypothesis** (`dab<NNNN>-<slug>.md`, flat; folder form `dab<NNNN>-<slug>/index.md`
  allowed when evidence accumulates) is one testable README change, run end-to-end;
  `conclude` may file one failure-driven follow-up — *depth*.

Both birth mechanisms are prompt-driven: the acting ensign writes the new entity file.

## Repo conventions (full detail in the repo-root `AGENTS.md`)

- Run `rk` from `dab/`: `uv run --project ../razorback rk <args>`.
- Always pass `--runs-dir runs`; prefer `rk run --explain` before a full run.
- Before any `rk run`, export `RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"`.
- **Before any `rk registry` / `rk runs diff` / `rk baseline promote`, export the DAB-local
  registry: `export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml`.**
  The razorback registry is a single GLOBAL YAML keyed only by `(kind, name)` with no project
  scoping, and the **live ade-bench loop owns the global `@baseline`** — a bare
  `rk registry … @baseline` would resolve/overwrite ade-bench's. The DAB-local registry file
  keeps DAB's `@baseline` separate. `rk run` itself does not touch the registry, so the export
  is only needed for the registry/diff/promote calls.
- **`rk run … --runs-dir` is long-running (30 min–8 hr+ for a full 54-cell run) and far exceeds
  the Bash-tool timeout — never run it in the foreground.** Launch it through `drivers/rk-run-detached.sh <key> <spec>
  [run|matrix]`, which `nohup`s the run, writes a handle under `runs/.rk-handles/<key>-<ts>/`
  (`pid` · `log` · atomic `done` sentinel with `rc`/`end`/`rundir`), and fires an **ntfy** push
  on completion. The **ensign launches and returns the handle immediately — it never waits**;
  the **FO owns the wait by scanning `runs/.rk-handles/*/` at the top of every turn** (4-state
  model + harbor-output crash check + backstop — full contract in the repo-root `AGENTS.md`
  → *Detached runs*). No live poller / no `Monitor`. The fast `--explain` / `rk audit` / `rk score`
  calls stay foreground, after the sentinel lands. `drivers/matrix.sh` launches the same way
  (`matrix` mode). See the `smoke`/`full` stages for the exact call.
- **Auto-wakeup at ETA (run the DAB FO under `/loop`).** The every-turn handle scan only fires
  when there *is* a turn — so when the captain is away, the FO must wake *itself* at the run's
  ETA instead of stalling. Immediately after launching a detached `smoke`/`full` run:
  1. Record the ETA in seconds (`eta_s` = surviving query-cells × ~per-query minutes; the same
     estimate you put in the propose smoke-set table / full-run brief).
  2. `ScheduleWakeup(delaySeconds = min(eta_s, 3600), reason = "DAB <key>: check detached run",
     prompt = <the /loop first-officer continuation>)`. Wakeups clamp to ≤1 h, so a multi-hour
     run wakes at most hourly and re-checks — that is intended (cheap sentinel poll, catches
     early finishes too).
  3. On every wake, scan `runs/.rk-handles/<key>-*/done`:
     - **present, `rc=0`** → run finished: go foreground for `rk audit` / `rk score` + the deep-dive.
     - **present, `rc≠0`** → failed: read `log`, open the `## Failure Review`.
     - **absent** → still running: re-`ScheduleWakeup` (`min(remaining_to_eta, 3600)` while before
       ETA, else ~600 s), post a one-line "still running, next check in N min", and end the turn.
  4. Stop rescheduling once `done` is consumed, or hit the ~9 h backstop → escalate to the captain.
  This *complements* the ntfy push and the every-turn scan; it makes the wait autonomous. It needs
  a wake-capable context — drive the DAB FO under `/loop` (dynamic, self-paced) so `ScheduleWakeup`
  fires; outside `/loop` the FO falls back to ntfy + the next operator turn.
- The independent variable is ONLY the solver README. A variant full spec differs from
  `specs/dab-anchor-codex.yaml` only in `experiment:` + `solver_workflow:`. `trials: 1` always
  (`concurrency.trials: 2` for throughput — two query-cells in parallel; DAB's per-query task
  dirs don't share a git HEAD, so the ade-bench concurrency-1 lock race does not apply here).

## File Naming

- Concepts: `concept-<slug>.md` (lowercase, hyphens; no number).
- Hypotheses: `dab<NNNN>-<slug>.md`, next available `dab<NNNN>` (scan existing `dab*-*.md` and
  `_archive/`, then increment — `status --next-id` is n/a under slug style). **Set `id: dab<NNNN>`**
  (the short prefix, e.g. `id: dab0001`) in frontmatter — recommended, mirroring ade-bench's
  `h<NNNN>` — so the entity resolves by its short id (`spacedock status --resolve dab0001`). The
  slug stays the identity (the status ID column renders the full `dab<NNNN>-<slug>`); the
  descriptive name also lives in `title`. The `dab` prefix avoids collision with ade-bench's
  `h00NN` namespace.

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Hypotheses set the short `dab<NNNN>` prefix (e.g. `dab0001`) — recommended, resolvable via `status --resolve`. Concepts use `concept-<slug>`. Slug stays the identity. |
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

- **Inputs:** a research lead, a prior verdict's follow-ups, a captain hunch, or the
  `_artifacts/dataset-gap-ranking.md` table (which datasets/queries have the most headroom
  vs the Opus incumbent).
- **Outputs:** a `concept-<slug>.md` body stating the direction and why it might raise
  the stratified Pass@1.
- **Good:** a concrete, testable direction tied to an observed failure mode on a low-scoring
  dataset.
- **Bad:** vague "make it better"; a direction with no hypothesis to derive from it.

### `ideate`

An ensign reads the concept + the current `@baseline` solver README + prior learnings +
the dataset-gap ranking, and **writes several `dab<NNNN>-<slug>.md` hypothesis entities**
(status `hypothesis`), each naming the specific solver-README change it will make and its
target dataset/queries. Then the concept advances to `expanded`.

- **Inputs:** the concept body; `../solver_workflows/spacedock-readme-baseline/README.md` (or
  the current `@baseline` solver); `_artifacts/dataset-gap-ranking.md`; the latest analyze
  findings.
- **Outputs:** 2–5 new hypothesis entities, each with a falsifiable claim + acceptance
  criteria; the concept marked `expanded`.
- **Good:** each hypothesis changes ONE idea, is falsifiable, and names its target
  datasets/queries.
- **Bad:** one mega-hypothesis; hypotheses that restate the concept without a concrete
  README change.

### `expanded`  *(terminal — concept path)*

The concept has been turned into hypotheses; archived.

### `hypothesis`  *(initial — hypothesis path)*

A fully-formed, queued hypothesis. Auto-advances to `propose`.

- **Inputs:** an `ideate` fan-out or a `conclude` follow-up.
- **Outputs:** the body's `## Hypothesis` (the claim + the single README change + named target
  queries) and `## Acceptance criteria` (the verdict, e.g. "the paired `rk runs diff` delta vs
  `@baseline` clears the tripwire on `stratified_pass_at_1`").
- **Flipped-task follow-up requirement.** If the hypothesis comes from a smoke/full rejection
  on a flipped or high-variance query, include `## Pre-smoke Decision-Fork Probe` before propose.
  It must name the local fork being tested, the exact prompt context used, the control A
  result, the proposed B/C result, the exact README wording tested, the artifact signature
  expected in a real run, and the caveat that this is proxy evidence only. If no probe was
  run, state why (for example: infrastructure fix, no local fork, or oracle-blocked).
- **Good:** falsifiable; names the target queries for smoke.
- **Bad:** success criteria invented after seeing results.

### `propose`  *(🚦 leak-guard gate)*

The ensign authors the variant, then a gatekeeper subagent pre-reviews it and records an
advisory recommendation in the hypothesis file. **You make the final gate decision, informed
by that recommendation.**

- **Inputs:** the hypothesis claim.
- **Outputs:**
  1. `cp -r ../solver_workflows/spacedock-readme-baseline ../solver_workflows/dab<NNNN>-<slug>`
     (fork the current `@baseline` solver dir — `spacedock-readme-baseline` is the seed
     baseline), then edit its `README.md` — the one variable.
  2. `cp specs/dab-anchor-codex.yaml specs/dab<NNNN>-<slug>.yaml`, set `experiment:` to
     `dab<NNNN>-<slug>` and `solver_workflow:` to `./solver_workflows/dab<NNNN>-<slug>`. This
     is the FULL spec — all 12 datasets, no query subset.
  3. Make the smoke spec: `cp specs/dab<NNNN>-<slug>.yaml specs/dab<NNNN>-<slug>.smoke.yaml`
     and add a `benchmark.tasks:` block (the dataset names whose queries the smoke needs) plus
     a `benchmark.exclude_tasks:` block (the `{dataset}-q{n}` ids to drop so only the targets +
     canaries survive). The plugin selector takes **dataset names only**; per-query subsetting
     is `exclude_tasks` (design §8). **If the instruction is generative** (fires on every query,
     not gated on a precondition that limits it to the targets), the surviving smoke set MUST
     also carry a **regression panel** — ≥1 currently-passing `@baseline` query from a dataset
     OTHER than the targets', plus **≥2 _perturbable_ canaries** (passers the lever can actually
     fire on) from the dataset whose query shape the lever most likely perturbs (enforced by
     gatekeeper G8). The three perfect-score datasets (bookreview / music_brainz_20k /
     stockindex; see `_artifacts/dataset-gap-ranking.md`) are the natural canary pool.
  4. Freeze both:
     `uv run --project ../razorback rk freeze --allow-missing specs/dab<NNNN>-<slug>.yaml` and
     `uv run --project ../razorback rk freeze --allow-missing specs/dab<NNNN>-<slug>.smoke.yaml`.
  5. **Verify the smoke selection** (design §8 caveat — no test covers `exclude_tasks` + plugin):
     `uv run --project ../razorback rk run specs/dab<NNNN>-<slug>.smoke.frozen.yaml --explain`
     and confirm the surviving per-query task list is exactly targets + canaries (no extra,
     none missing). This is $0 and foreground.
  6. **Run the gatekeeper.** Dispatch a review subagent that applies
     `_gatekeeper/propose-review-guideline.md` to the variant artifacts (the forked solver
     README diff vs its parent, the two spec diffs, the frozen files, and the hypothesis body)
     and writes a `## Gatekeeper review` block into the hypothesis file: a per-rule
     PASS/WARN/FAIL table plus an overall **APPROVE / REVISE / REJECT** recommendation with a
     one-line rationale. The gatekeeper is advisory — it does not pass or block the gate.
- **Gate presentation to the captain (REQUIRED — every propose gate).** Don't just brief
  *what* the hypothesis verifies; also lay out the smoke set as a table so the captain can
  sanity-check coverage before approving. Resolve each query's `@baseline` reward first
  (`export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml`, then
  `rk registry resolve run @baseline`, then read the resolved run's `per_trial_outcomes.json`),
  and present a **boxed table** with these columns — `Task` (`{dataset}-q{n}`) / `Baseline` /
  `Should pass in smoke?` / `Role / why we picked it` — using the glyphs `❌ FAIL`, `✅ PASS`,
  `🎯 want it to flip to PASS`, `✅ must stay PASS`:

  ```
  ┌───────────────┬──────────┬─────────────────────┬─────────────────────────────────────────────┐
  │     Task      │ Baseline │ Should pass in smoke?│             Role / why we picked it          │
  ├───────────────┼──────────┼─────────────────────┼─────────────────────────────────────────────┤
  │ <ds>-q<n>     │ ❌ FAIL  │ 🎯 want it to flip  │ Target — the failure this lever should flip. │
  │ <ds>-q<n>     │ ✅ PASS  │ ✅ must stay PASS   │ Sentinel — known passer; breaks ⇒ side effs. │
  │ <ds>-q<n>     │ ✅ PASS  │ ✅ must stay PASS   │ Canary (<other ds>) — regression tripwire.   │
  └───────────────┴──────────┴─────────────────────┴─────────────────────────────────────────────┘
  ```

  One row per surviving smoke task. State the net you're hoping for (e.g. "flip ≥1 of N targets,
  lose zero sentinels/canaries"). The run is detached (nohup), so the captain needn't wait
  on-screen; give an ETA based on the number of surviving query-cells. Lead with this table +
  a plain-words brief of the lever; keep the full spec/diff detail in the hypothesis file. For a
  generative lever, the table makes the G8 panel auditable at a glance — a missing canary
  dataset is a REVISE before smoke, not a surprise at full.
- **Gatekeeper (advisory pre-review):** its recommendation is input to your decision, not a
  substitute for it. A rule the gatekeeper marks FAIL is a likely reject; tune the bar by
  asking an agent to update `_gatekeeper/propose-review-guideline.md` on demand (it is not
  auto-updated; the gatekeeper re-reads it fresh each run). For flipped-task follow-ups, the
  gatekeeper also reviews the `## Pre-smoke Decision-Fork Probe` block for proxy quality: no
  hidden-result leakage, solver-visible context only, exact README wording, a control variant,
  and no pass-rate claim from subagent counts.
- **Gate — you reject if:** the README leaks ground truth (its no-external-reference /
  leak-guard prose is removed or weakened, OR it reads `ground_truth.csv` / pastes
  `data/<ds>/db_description_withhint.txt` content into the README); the FULL spec differs from
  the anchor in anything other than `experiment:` + `solver_workflow:` (the smoke spec
  additionally adds `benchmark.tasks` + `benchmark.exclude_tasks`); `agent.kind` ≠
  `spacedock_solver` or `runtime` ≠ `codex`.
- **Good:** exactly one README idea changed; leak-guard intact; `diff` of the two specs
  shows only the two allowed fields; gatekeeper recommendation recorded; the smoke-set table
  (task / baseline-passed / should-pass / role) presented to the captain with baseline rewards
  resolved; the surviving smoke set confirmed via `--explain`.
- **Bad:** multiple knobs changed; leak-guard relaxed; advancing past a gatekeeper REJECT
  without recording why; asking for approval without showing the smoke-set table.

### `smoke`  *(🚦 go/no-go gate)*

A focused pre-flight on the hypothesis's **target queries** via the smoke spec
(its `benchmark.tasks` + `benchmark.exclude_tasks`). **You review before committing the full
run.** *(Budget caps deferred — this is a worthiness gate.)*

- **Inputs:** the frozen smoke spec `specs/dab<NNNN>-<slug>.smoke.frozen.yaml`.
- **Smoke-set composition.** Targets + a stable-pass sentinel. **If the instruction is
  generative** (fires on every query, not gated on a precondition), the surviving smoke set MUST
  also include a **regression panel** — ≥1 currently-passing `@baseline` query from a dataset
  OTHER than the targets'. A generative change can regress *anywhere it fires*, and a
  targets-only smoke is structurally blind to that. Because the metric is stratified Pass@1
  (per-dataset means averaged), a regression on a passer in a non-target dataset lowers the
  stratified score even while the target flips. **A canary dropping FAIL is a NO-GO regardless
  of how many targets flipped.**
  - **One canary per dataset is necessary but NOT sufficient — carry ≥2 _perturbable_ canaries
    for the dataset whose query shape the lever most likely perturbs.** A *perturbable* canary is
    a passer the lever can actually FIRE on; a stable passer the lever never touches proves
    nothing. A generative rule can break a *different* query of a dataset than your single canary.
  - **A lone flip may be variance — don't bank a GO on it.** gpt-5.5 @ xhigh is not
    deterministic. A GO should rest on flips you can prove reached the committed artifact (the
    deep-dive below) plus held *perturbable* canaries — not a single unexplained flip.
- **Outputs (from `dab/`):**
  ```bash
  uv run --project ../razorback rk run specs/dab<NNNN>-<slug>.smoke.frozen.yaml --explain   # $0, fast, foreground
  # rk run is long (30 min–8 hr+) >> Bash-tool timeout — launch DETACHED via the audited launcher (nohup)
  # (ensign launches, returns the handle, exits; FO scans runs/.rk-handles/*/ every turn):
  drivers/rk-run-detached.sh dab<NNNN>-smoke specs/dab<NNNN>-<slug>.smoke.frozen.yaml run
  #   -> handle: runs/.rk-handles/dab<NNNN>-smoke-<ts>/  (pid · log · done = rc/end/rundir) + ntfy on done
  # THEN ScheduleWakeup(min(eta_s,3600)) to auto-check the sentinel at the ETA — see Repo conventions
  #   → "Auto-wakeup at ETA". eta_s ≈ surviving query-cells × ~per-query minutes.
  # When `done` appears with rc=0 (or harbor output confirms — see AGENTS "Detached runs"), THEN:
  uv run --project ../razorback rk audit <run-dir> --policy strict
  uv run --project ../razorback rk score <run-dir>
  ```
  Capture the focused score + clean-audit attestation in `## Smoke result`.
- **Post-run deep-dive (REQUIRED every smoke — whether GO or NO-GO).** Do not stop at the
  score. For each target query, compare the smoke cell against the same query in `@baseline`
  (`export RAZORBACK_REGISTRY=…`, then `rk registry resolve run @baseline`):
  1. **Verdict delta** — did it flip FAIL→PASS, or not? Did the sentinel hold?
  2. **Distance-to-pass** — the DAB per-query result, smoke vs `@baseline`: read the cell's
     `validation.json` / `reward_per_query.json` (and the validator stdout) for the
     mismatch the validator reported. **Unchanged validator result ⇒ the lever was inert on
     that cell** — a cheap check to run before reading any transcript.
  3. **Behavioral why** — for at least one flipped (if any) and one still-failing target,
     read the cell transcripts (the codex `agent/` transcript + the ensign session jsonl)
     and extract the **final committed artifact** (the model SQL/answer the solver actually
     wrote). Classify each result: *flipped because the change reached the committed answer* /
     *inert — change only discussed, not implemented* / *closer but still failing* /
     *instruction inapplicable (no analog / never triggered)*. Acknowledging an instruction
     in reasoning is NOT evidence — verify the artifact.
  Write the full per-query detail (a flip/distance/why table + the behavioral read) into
  `## Smoke result` and `## Behavioral analysis`.
- **Failure review loop (REQUIRED for every NO-GO, canary regression, or revise).** Before
  routing `smoke → hypothesis` or `smoke → conclude`, append a `## Failure Review` block to the
  entity. Classify the failure as exactly one primary type:
  `infrastructure-failure` / `diagnosis-miss` / `wrong-branch` / `incomplete-artifact` /
  `correct-artifact-still-fail` / `canary-bleed` / `variance-unclear`.
  Then answer:
  1. What was the original hypothesized fork?
  2. What fork did the committed artifact actually reveal?
  3. Did the README rule fire, and where is the artifact evidence?
  4. What new fork or failure mechanism should be tested next?
  5. Is the next step `stop`, `probe`, `file`, or `escalate`?
  Infrastructure failures are not experiment evidence; recover or relaunch before drawing
  behavioral conclusions.
- **Workflow-refinement evaluation (AUTOMATIC — do this without being asked).** If the
  hypothesis's lever is a change to the **solver workflow's structure** — a new stage, a
  removed / reordered / replaced stage, or a new protocol / protocol-family (tell-tales: a
  `## Protocol-family declaration` section, or a `## Hypothesis` framed around "a NEW stage" or
  reordering stages, as opposed to a rule tweak *inside* an existing stage; the hypothesis's own
  framing is authoritative) — then the deep-dive is NOT done at the per-query flip. You MUST also
  evaluate the **workflow change itself**:
  1. **Was the stage/protocol exercised?** Across the *whole* smoke set (not just the target),
     did the new/changed stage actually fire and produce its declared artifact? Where was it
     inert or inapplicable?
  2. **Effect of the structural change** — independent of whether the target flipped: did it
     change the committed artifacts / solver behavior — help, harm, or nothing? A target that
     did NOT flip can still be a real workflow finding.
  3. **Record it in the workflow-refinement log.** Append/refresh an entry in
     `_artifacts/WORKFLOW-REFINE.md` (layer / refinement type / finding / **learning** /
     bears-on / evidence). Mandatory and automatic — part of the smoke commit; do not wait for
     the captain.
  The go/no-go you then report covers BOTH axes: the query-level result *and* the workflow-level
  learning.
- **Report to the captain in plain language.** The entity gets the full detail; the captain
  gets a SIMPLE-WORDS on-screen summary at the gate — what flipped, did we get closer, and
  (if NO-GO) why the hypothesis didn't work — not the raw tables. Lead with the go/no-go and
  the one-line reason.
- **Gate:** worthwhile (the change moved the targeted queries, or at least did not regress
  them) → `full`; flawed but revisable → back to `hypothesis`; cleanly falsified (e.g. 0
  flips, lever inert) → `conclude` (REJECTED), recording the deep-dive as the evidence.
  A `smoke → hypothesis` revision requires a `## Failure Review` block with a newly defined
  fork and a decision about whether subagent probing is needed before another smoke.
- **Good:** smoke exercises the changed behavior; audit clean before the score is trusted;
  every NO-GO carries a behavioral *why* backed by the committed artifact.
- **Bad:** advancing on a smoke that never exercised the change; scoring without a clean
  audit; reporting a NO-GO as just a number with no artifact-level reason; burying the
  captain in raw detail instead of a plain-language read.

> **Anchor / first run skips `smoke`** (`propose → full`): the codex anchor on the baseline
> README (all 12 datasets) is a direct full run that validates the loop end-to-end against the
> Opus incumbent; subsequent hypotheses go through `smoke`.

### `full`

The full run on the FULL frozen spec (`dab<NNNN>-<slug>.frozen.yaml`, all 12 datasets / 54
queries, no query subset).

- **Outputs (from `dab/`):**
  ```bash
  # rk run is long (30 min–8 hr+) >> Bash-tool timeout — launch DETACHED via the audited launcher (nohup)
  # (ensign launches, returns the handle, exits; FO scans runs/.rk-handles/*/ every turn):
  drivers/rk-run-detached.sh dab<NNNN>-full specs/dab<NNNN>-<slug>.frozen.yaml run   # all 12 datasets
  #   -> handle: runs/.rk-handles/dab<NNNN>-full-<ts>/  (pid · log · done = rc/end/rundir) + ntfy on done
  # THEN ScheduleWakeup(min(eta_s,3600)) to auto-check the sentinel at the ETA — see Repo conventions
  #   → "Auto-wakeup at ETA". eta_s ≈ 54 query-cells × ~per-query minutes for a full run.
  # When `done` appears with rc=0 (or harbor output confirms — see AGENTS "Detached runs"), THEN:
  uv run --project ../razorback rk audit <run-dir> --policy strict
  uv run --project ../razorback rk score <run-dir> --format json
  ```
  (Or run the full per-cell pipeline detached:
  `drivers/rk-run-detached.sh dab<NNNN>-full specs/dab<NNNN>-<slug>.frozen.yaml matrix` —
  `matrix.sh` chains run + audit + score + ledger internally, equally long, same handle/ntfy.)
  Record the run-dir path + headline in `## Run result`.
- **Good:** the full spec uses the SAME solver README as the smoke spec (only the query
  set differs); audit clean before the score is recorded.
- **Bad:** methodology drift between smoke and full.

### `analyze`

Interpret the full run against `@baseline` — quantitatively and behaviorally.

- **Quantitative (from `dab/`):**
  ```bash
  export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
  uv run --project ../razorback rk runs diff "$(uv run --project ../razorback rk registry resolve run @baseline)" <variant-run-dir>
  uv run --project ../razorback rk score <variant-run-dir> --format json   # absolute stratified Pass@1 vs the Opus incumbent ~0.65 (0.6536)
  ```
  Paste the paired delta (CIs, adjusted p) + absolute score into `## Run result`.
- **The codex-vs-Opus confound (DAB-specific, design §7) — call it out explicitly.** The
  `@baseline` is the Opus-4.8 incumbent; every variant runs codex/gpt-5.5. The headline
  `rk runs diff` delta therefore carries BOTH the README lever AND the model swap — they are
  entangled, and the raw number cannot attribute the gain to the README change alone. The
  behavioral / committed-artifact read below is the only thing that can: for each
  verdict-changed query, you MUST attribute **whether the README change itself moved the
  committed answer** (the wording reached the SQL/answer the solver wrote), versus a flip that
  the model swap would have produced regardless of the README. A delta with no artifact-level
  attribution is not evidence the lever worked.
- **Behavioral (per query whose verdict changed vs `@baseline`, plus a sample of persistent
  failures) — read the cell `runs/<experiment>/<hash>/<dataset>-q<n>__<short>/`:**
  - `result.json` + the per-query reward (`reward_per_query.json` / `validation.json`) →
    binary verdict.
  - the DAB validator output → **distance to pass**: what the validator compared, which check
    failed, the concrete mismatch (rows/values off).
  - the codex `agent/` transcript → the **main agent** plan, tool calls, ensign dispatches,
    validation evidence.
  - the ensign session jsonl → the **sub-agent** transcripts.
  Write a `## Behavioral analysis` block answering, per query: (1) **method adherence** —
  did the agent + ensigns actually execute the README's prescribed method? (2) why it
  works; (3) why it fails (and the per-query distance-to-pass from the validator).
- **Required questions every analyze report MUST answer** (in `## Run result` /
  `## Behavioral analysis` — so the captain reads them, not extracts them):
  1. **Net + full per-query ledger** — absolute stratified Pass@1 vs `@baseline` and paired
     delta + CI; AND *every* query that changed verdict in *both* directions (FAIL→PASS gains
     **and** PASS→FAIL regressions), each with its mechanism. Never report only the gains.
  2. **Smoke vs full** — if smoke was a GO, why did the full verdict differ? Name exactly what
     the smoke set could not see (e.g. regressions on datasets it didn't sample).
  3. **Already-correct-and-broken** — for each regression, was the query *passing* at
     `@baseline`? Call out damage to working answers explicitly; distinguish "failed to help"
     from "broke a passer."
  4. **Was the change executed? (the confound attribution)** — for representative gains and
     regressions, did the *committed artifact* actually change because of the README wording?
     Classify: executed-and-helped / executed-and-hurt / inert (discussed-not-done) /
     premise-falsified (followed but target not local) / model-swap-attributable (would flip
     regardless of the README). Verify the artifact, not the chatter.
  5. **Prevention + next move** — concrete and actionable: how to keep the gains without the
     harm (scoping guardrails), how to catch it earlier (smoke canaries / G8), and the
     recommended next step (do NOT reflexively file if the lever family is exhausted —
     escalate to the captain).
  6. **Smoke-vs-full fork drift** — if a smoke GO later fails or regresses at full, identify
     whether the smoke result was artifact-real or single-trial variance; name the fork that
     changed at full; state whether the smoke panel missed a dataset, the README rule drifted
     into a different implementation branch, or the failure is unrelated variance. This answer
     feeds the `## Failure Review` / follow-up routing loop.
- **Report to the captain in plain language.** Keep the full detail (tables, CIs, SQL) in the
  entity; give the captain a SIMPLE-WORDS on-screen summary — net result, what flipped each
  way, why, the confound caveat, and the recommendation. Lead with the headline; never make the
  captain read raw tables to learn the verdict.
- **Good:** verdict cites the diff CI + adjusted p; behavioral findings name specific
  failure mechanisms AND attribute the README lever vs the model swap; all required questions
  answered; regressions named as damage to passers; captain gets a plain-words summary.
- **Bad:** reading a within-CI wobble as a win; a score with no behavioral read; crediting a
  flip to the README without artifact-level attribution (the confound); reporting only the
  gains and omitting the regressions; a report the captain must interrogate to learn the flips,
  the prevention, or the next move.

### `conclude`  *(terminal — hypothesis path)*

- **Promote if** the variant's stratified Pass@1 clears the Opus incumbent and the paired delta
  clears the tripwire (CI excludes a regression) on a clean audit:
  ```bash
  export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml
  uv run --project ../razorback rk baseline promote <variant-run-dir>
  uv run --project ../razorback rk registry add run baseline <variant-run-dir>
  ```
  (updates `@baseline` in the DAB-local `razorback-registry.yaml`). Then update
  `_artifacts/baseline.yaml` and re-derive `_artifacts/dataset-gap-ranking.md` from the new
  champion's `summary.json`.
- **Record the learnings in the entity file — not only in operator memory.** The entity is
  the portable, cross-machine experiment record. Write the distilled lessons into
  `## Behavioral analysis` and `## Verdict`: the failure mechanism, whether the change
  reached the committed artifact (and whether the gain was lever-attributable or model-swap),
  the distance-to-pass deltas, and any transferable rule (what kind of lever lands vs is
  inert). Append a one-line entry to `_artifacts/self-learning.md`. Memory is a convenience
  mirror; the entity body is the source of truth a teammate on another machine will read.
- **Finalize the workflow-refinement finding (AUTOMATIC for any workflow-structural
  hypothesis).** If this hypothesis changed the workflow's structure (new / removed / reordered /
  replaced stage, or a new protocol — the same test as the smoke *Workflow-refinement
  evaluation* step), its entry in `_artifacts/WORKFLOW-REFINE.md` MUST reach a final state before
  archive: set the entry's status to the verdict (adopted into the workflow / rejected as written
  / open with a named next step), and make sure its **learning** line is sharp and its
  **bears-on** line lists the sibling hypotheses it should steer. Do this whether `conclude` was
  reached from `smoke` (REJECTED) or after a full `analyze` — and without being told.
- **Derive new hypotheses from the deep-dive findings.** Turn the smoke/analyze behavioral
  read into concrete next bets (each ONE README change, falsifiable, with named target
  queries). **But do not reflexively file when the evidence says the lever family is
  exhausted** — if a meta-pattern has emerged (e.g. several hypotheses of the same kind all
  inert), surface the candidate directions to the captain as a strategy decision instead of
  auto-filing another doomed variant. First write `## Follow-up Routing` with one of:
  `stop` (oracle-blocked/exhausted/no visible fork), `probe` (new fork exists but wording is
  untested), `file` (subagent probe or artifact evidence supports a new hypothesis), or
  `escalate` (multiple viable directions need captain strategy). When you do file, it is ONE
  follow-up `dab<NNNN>-<slug>.md` (status `hypothesis`) forking the current `@baseline`.
- **Verdict + archive.** Set `verdict: PASSED` (promoted / ran cleanly to a real result) or
  `REJECTED` (cleanly falsified, e.g. NO-GO at smoke); archive.

> **Reached `conclude` from `smoke`?** A cleanly-falsified hypothesis routes
> `smoke → conclude` (REJECTED) without a `full` run — the smoke deep-dive is the evidence
> of record. `full`/`analyze` only run when smoke is a GO.

## Champion (`@baseline`)

The reigning champion is the `@baseline` run-dir in the DAB-local `razorback-registry.yaml`
(resolve it after `export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml`).
The seed champion is the converted Opus-4.8 incumbent (~0.65 / 0.6536 stratified Pass@1). New hypotheses
fork from its solver README (`spacedock-readme-baseline` until a codex variant is promoted);
`analyze` diffs against its run-dir.

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

<the theme and why it might raise the stratified Pass@1>
```

Hypothesis (`dab<NNNN>-<slug>.md`):
```yaml
---
id: dab<NNNN>
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

The falsifiable claim and the single solver-README change it makes. Target queries: <ids>.

## Pre-smoke Decision-Fork Probe

Required for flipped-task follow-ups unless explicitly skipped. State the fork, prompt context,
control result, proposed-rule result, exact README wording tested, expected artifact signature,
and why the proxy does or does not justify smoke.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/dab-anchor-codex.yaml specs/dab<NNNN>-<slug>.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`, with the
codex-vs-Opus confound attributed via the committed-artifact read.**

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

Required for every smoke/full rejection or revise route. Classify the failure and define the
next fork or routing decision: stop / probe / file / escalate.

## Follow-up Routing

## Verdict
```

## Commit Discipline

Commit at every stage transition and entity-body update; variant specs + solver READMEs
are tracked, `runs/` and the live `razorback-registry.yaml` stay gitignored.
