# autobench Auto-Research Repo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the `autobench/ade-bench/` auto-research repo — a razorback-scaffolded research project whose `hypotheses/` directory is a spacedock experiment workflow that tunes a codex solver README to beat the 9/48 ade-bench baseline.

**Architecture:** `rk research new` scaffolds the canonical layout (`specs/`, `solver_workflows/`, `hypotheses/`, `drivers/matrix.sh`, `razorback-research.toml`); we overwrite the conservative defaults with the spec's exact config, fork the codex ade-dbt-repair solver as the baseline, upgrade `hypotheses/README.md` into a spacedock experiment workflow (`concept→ideate→expanded` breadth + `hypothesis→propose→smoke→full→analyze→conclude` depth, two human gates), write root `AGENTS.md`/`CLAUDE.md`/`README.md`, then run the baseline full run to establish the `@baseline` anchor.

**Tech Stack:** razorback (`rk` CLI, run via `uv` from the `razorback/` submodule), spacedock (workflow framework + first-officer/ensign agents, `status` CLI), Harbor + Docker (benchmark execution), codex runtime (`gpt-5.5`) as the agent-under-test.

**Design spec:** `docs/superpowers/specs/2026-06-01-autobench-auto-research-design.md`

**Branch:** `setup-autobench-auto-research` (already checked out).

---

## Conventions used in every task

- **`rk` invocation** — run from the `ade-bench/` directory:
  ```bash
  uv run --project ../razorback rk <args>
  ```
  (`uv` uses the razorback submodule's environment; cwd stays `ade-bench/` so relative paths like `specs/…` and `--runs-dir runs` resolve.)
- **Before any `rk run`** (live execution only — Tasks require it explicitly), from the repo root:
  ```bash
  export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(pwd)/spacedock"
  ```
  Specs with `agent.kind: spacedock_solver` fail at agent setup without it.
- **spacedock status CLI:** `spacedock/skills/commission/bin/status` (run from repo root).
- **Never edit the `razorback/` or `spacedock/` submodules** — they are read-only dependencies.
- Commit after each task. Work stays on branch `setup-autobench-auto-research`.

---

## Task 1: Scaffold the ade-bench research repo

**Files:**
- Create (via `rk research new`): `ade-bench/README.md`, `ade-bench/razorback-research.toml`, `ade-bench/specs/{baseline.yaml,README.md}`, `ade-bench/solver_workflows/{baseline/README.md,README.md}`, `ade-bench/hypotheses/README.md`, `ade-bench/drivers/matrix.sh`
- Modify: `.gitignore`

- [ ] **Step 1: Run the scaffolder** (from repo root)

```bash
uv run --project razorback rk research new ade-bench \
  --from 'dbt-labs/ade-bench@sha256:2c1f9e6966d01b0a5de2235d1a0b64089c7eead42c85c3b7b61d0929405c2bd5' \
  --solver-runtime codex --target-model gpt-5.5 \
  --into ./ade-bench
```

Expected: prints `note: no benchmark-defaults entry for dbt-labs/ade-bench — scaffolded conservative defaults with a TODO marker.` then `scaffolded .../ade-bench/`. (The conservative defaults are overwritten in Tasks 2–3.)

- [ ] **Step 2: Verify the scaffold tree**

Run:
```bash
find ade-bench -type f | sort
```
Expected exactly:
```
ade-bench/README.md
ade-bench/drivers/matrix.sh
ade-bench/hypotheses/README.md
ade-bench/razorback-research.toml
ade-bench/solver_workflows/README.md
ade-bench/solver_workflows/baseline/README.md
ade-bench/specs/README.md
ade-bench/specs/baseline.yaml
```

- [ ] **Step 3: Gitignore the run outputs**

Append to `.gitignore` (currently contains `recce.yml`):

```
ade-bench/runs/
```

- [ ] **Step 4: Verify ignore + tracked files**

Run:
```bash
mkdir -p ade-bench/runs && touch ade-bench/runs/.keep
git status --porcelain ade-bench | grep -E "runs/" || echo "runs/ correctly ignored"
```
Expected: `runs/ correctly ignored` (the `runs/` path produces no output from `git status`).

- [ ] **Step 5: Commit**

```bash
git add ade-bench .gitignore
git commit -m "feat: scaffold ade-bench research repo via rk research new"
```

---

## Task 2: Fork the codex solver baseline README

The scaffolded `ade-bench/solver_workflows/baseline/README.md` is razorback's generic model/analyze/verify loop. Replace it with a fork of razorback's ade-specific `codex-ade-dbt-repair` prose, keeping an explicit leak-guard section.

**Files:**
- Modify (overwrite): `ade-bench/solver_workflows/baseline/README.md`

- [ ] **Step 1: Overwrite the baseline solver README**

Write `ade-bench/solver_workflows/baseline/README.md` with exactly:

```markdown
# ade-bench codex solver workflow (baseline)

The spacedock-solver (codex) agent reads this README per trial. Hypothesis variants
copy this directory to `../h<NNNN>-<slug>/` and edit the prose — this README is the
research's independent variable.

Work offline inside the task workspace. Inspect `instruction.md`, `task.toml`, the dbt
project files, and any local validation scripts before editing.

Repair the task-local dbt project so the requested behavior is implemented in the
project itself. Prefer the smallest clear model, macro, seed, config, or test change
that addresses the failure described by the task.

Run cheap local validation when the task provides it, such as `dbt compile`, targeted
`dbt build`/`dbt test`, or task-local shell scripts. Record only concise evidence in
your final message.

Leave the repaired project state as the graded artifact. Do not optimize for a separate
answer file, network access, package installs, or external datasets.

## Reset declaration

Between trials, razorback resets the inner-agent container, the per-trial workspace,
and any sidecar services declared in `task.toml`. Stateful learning across trials is
intentionally not supported.

## External-oracle audit (leak-guard — DO NOT REMOVE OR WEAKEN)

The workspace data is the only authoritative source. If a task is unanswerable from it,
say so rather than reaching outside. Forbidden:

- `datasets.load_dataset(...)` / `from datasets import load_dataset` / `hf://…` — HuggingFace canonical-dataset lookups.
- `huggingface_hub` / `transformers` / `evaluate` imports whose only purpose is to fetch canonical answer-key data.
- `requests.get` / `curl` / `wget` to canonical-data hosts (huggingface.co, raw.githubusercontent.com, kaggle.com, the benchmark's published dataset hub pages).
- web search (`web_search`, `web.run`) and LLM-as-oracle patterns (asking another model "what is the answer to task X?").

NOT forbidden: `pip install` of generic compute libraries (scikit-learn, pandas, numpy,
scipy, duckdb, …) that ship no canonical-data downloads.

`rk audit --policy strict` is the post-run backstop; this prose deters the paths the
runtime cannot see.
```

- [ ] **Step 2: Verify the leak-guard section is present**

Run:
```bash
grep -c "External-oracle audit" ade-bench/solver_workflows/baseline/README.md
```
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add ade-bench/solver_workflows/baseline/README.md
git commit -m "feat: fork codex ade-dbt-repair solver as the baseline (with leak-guard)"
```

---

## Task 3: Replace the baseline spec with the design's exact config

The scaffolded `specs/baseline.yaml` has conservative placeholders (`max_turns: 20`, `reasoning_effort: default`, `concurrency.trials: 4`, `paper_baseline.value: 0.0`, agent + meta budgets, a TODO comment). Replace it with the spec's §5.1 config.

**Files:**
- Modify (overwrite): `ade-bench/specs/baseline.yaml`

- [ ] **Step 1: Overwrite `ade-bench/specs/baseline.yaml`**

Write exactly:

```yaml
version: 1
experiment: ade-bench-baseline          # variants: ade-bench-h0001-<slug>
agent:
  kind: spacedock_solver
  runtime: codex
  model: gpt-5.5
  sampling:
    temperature: 0.0
    top_p: null
    seed: null
  solver_workflow: ./solver_workflows/baseline   # variants repoint to ./solver_workflows/h<NNNN>-<slug>
  spacedock_skill_version: "1.0.0"
  max_turns: 200
  override_timeout_sec: 2400
  max_timeout_sec: 2400
  reasoning_effort: xhigh                # held constant across all hypotheses
  tools_allowed: []
  tools_denied: []
benchmark:
  kind: harbor
  dataset: dbt-labs/ade-bench@sha256:2c1f9e6966d01b0a5de2235d1a0b64089c7eead42c85c3b7b61d0929405c2bd5
  # full: whole dataset (all 48). smoke: SAME frozen spec, run-time task subset.
  # baseline / first run: skip smoke, run full directly.
trials: 1                               # one trial per task — applies to BOTH smoke and full
concurrency:
  trials: 1
observers:
  - kind: jsonl
    path: events.jsonl
  - kind: stdout
experiment_meta:
  # max_budget_usd deferred — first loops run on a flat OpenAI subscription, not metered API.
  paper_baseline:
    name: stratified_pass_at_1
    value: 0.1875                        # 9/48 — initial spacedock baseline (no published paper)
provenance:
  pin_model_version: false
  pin_image_digest: false
```

- [ ] **Step 2: Verify the YAML parses and the TODO marker is gone**

Run:
```bash
python3 -c "import yaml,sys; d=yaml.safe_load(open('ade-bench/specs/baseline.yaml')); print('runtime',d['agent']['runtime']); print('reasoning',d['agent']['reasoning_effort']); print('trials',d['trials'],d['concurrency']['trials']); print('paper',d['experiment_meta']['paper_baseline']['value'])"
grep -c "TODO" ade-bench/specs/baseline.yaml
```
Expected:
```
runtime codex
reasoning xhigh
trials 1 1
paper 0.1875
0
```

- [ ] **Step 3: Commit**

```bash
git add ade-bench/specs/baseline.yaml
git commit -m "feat: set baseline spec config (codex/gpt-5.5, trials:1, paper_baseline 9/48, budgets deferred)"
```

---

## Task 4: Freeze the baseline spec and verify resolution

Freeze seals the solver-workflow content hash and resolves dynamic inputs; `--explain` confirms the spec resolves end-to-end at $0 before any live run.

**Files:**
- Create (via `rk freeze`): `ade-bench/specs/baseline.frozen.yaml`, `ade-bench/specs/provenance.yaml`

- [ ] **Step 1: Freeze the spec** (from `ade-bench/`)

```bash
cd ade-bench
uv run --project ../razorback rk freeze specs/baseline.yaml
```
Expected: writes `specs/baseline.frozen.yaml` (and `provenance.yaml`); no error.

- [ ] **Step 2: Verify the frozen spec sealed the solver-workflow hash**

Run (from `ade-bench/`):
```bash
grep -E "solver_workflow_content_hash|sealed_hash" specs/baseline.frozen.yaml
```
Expected: a `solver_workflow_content_hash: sha256:…` line (and/or `sealed_hash:`) — proves the baseline solver README was hashed into the frozen spec.

- [ ] **Step 3: Resolve-check with `--explain` ($0, no Docker, no Harbor)**

Run (from `ade-bench/`):
```bash
uv run --project ../razorback rk run specs/baseline.frozen.yaml --explain --explain-format json | python3 -c "import json,sys; d=json.load(sys.stdin); print('OK explain resolved')"
```
Expected: `OK explain resolved` (the explain plan is valid JSON; no translator error). If it errors, STOP and fix the spec before proceeding.

- [ ] **Step 4: Commit**

```bash
cd ..
git add ade-bench/specs/baseline.frozen.yaml ade-bench/specs/provenance.yaml
git commit -m "feat: freeze baseline spec; verify resolution with rk run --explain"
```

---

## Task 5: Upgrade `hypotheses/` into the spacedock experiment workflow

Replace the scaffolded notes README with a spacedock-commissioned workflow: `concept→ideate→expanded` (breadth) + `hypothesis→propose→smoke→full→analyze→conclude` (depth), gates on `propose` + `smoke`.

**Files:**
- Modify (overwrite): `ade-bench/hypotheses/README.md`

- [ ] **Step 1: Overwrite `ade-bench/hypotheses/README.md`**

Write exactly:

````markdown
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

- **Inputs:** the concept body; `../solver_workflows/baseline/README.md` (or the current
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
  1. `cp -r ../solver_workflows/baseline ../solver_workflows/h<NNNN>-<slug>` (fork the
     current `@baseline` solver dir), then edit its `README.md` — the one variable.
  2. `cp ../specs/baseline.yaml ../specs/h<NNNN>-<slug>.yaml`, set `experiment:` to
     `ade-bench-h<NNNN>-<slug>` and `solver_workflow:` to
     `./solver_workflows/h<NNNN>-<slug>`.
  3. `uv run --project ../razorback rk freeze specs/h<NNNN>-<slug>.yaml`.
- **Gate — you reject if:** the README leaks ground truth (the External-oracle audit
  section is removed/weakened); the spec differs from baseline in anything other than
  `experiment:` + `solver_workflow:`; `agent.kind` ≠ `spacedock_solver` or
  `runtime` ≠ `codex`.
- **Good:** exactly one README idea changed; leak-guard intact; `diff` of the two specs
  shows only the two allowed fields.
- **Bad:** multiple knobs changed; leak-guard relaxed.

### `smoke`  *(🚦 go/no-go gate)*

A focused pre-flight on the hypothesis's **target datasets** (run-time subset of the same
frozen spec). **You review before committing the full run.** *(Budget caps deferred —
this is a worthiness gate.)*

- **Inputs:** the frozen variant spec; the hypothesis's target dataset IDs.
- **Outputs (per target dataset, from `ade-bench/`):**
  ```bash
  uv run --project ../razorback rk run specs/h<NNNN>-<slug>.frozen.yaml --explain   # $0 first
  uv run --project ../razorback rk run specs/h<NNNN>-<slug>.frozen.yaml --runs-dir runs --task-id <dataset>
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

The full 48-task run on the same frozen spec.

- **Outputs (from `ade-bench/`):**
  ```bash
  uv run --project ../razorback rk run specs/h<NNNN>-<slug>.frozen.yaml --runs-dir runs   # all 48
  uv run --project ../razorback rk audit <run-dir> --policy strict
  uv run --project ../razorback rk score <run-dir> --format json
  ```
  (Or `bash drivers/matrix.sh --specs 'specs/h<NNNN>-<slug>.frozen.yaml'` to chain
  run + `captured>0` + audit + score + ledger.) Record the run-dir path + headline in
  `## Run result`.
- **Good:** same frozen spec smoke validated; audit clean before the score is recorded.
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
````

- [ ] **Step 2: Validate the workflow frontmatter**

Run (from repo root):
```bash
spacedock/skills/commission/bin/status --workflow-dir ade-bench/hypotheses --validate
```
Expected: `VALID`

- [ ] **Step 3: Verify discovery finds exactly this workflow**

Run (from repo root):
```bash
spacedock/skills/commission/bin/status --discover
```
Expected: output includes the absolute path to `ade-bench/hypotheses` (and no `solver_workflows` dirs — those READMEs have no `commissioned-by` frontmatter).

- [ ] **Step 4: Commit**

```bash
git add ade-bench/hypotheses/README.md
git commit -m "feat: upgrade hypotheses/ into the spacedock experiment workflow"
```

---

## Task 6: Write the repo-root `AGENTS.md`

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1: Write `AGENTS.md`**

Write exactly:

```markdown
# autobench — operator guide

autobench is an auto-research repo. It tunes a **codex spacedock solver-workflow README**
(the independent variable) to push the ade-bench `stratified_pass_at_1` above the
**9/48 (0.1875)** baseline. razorback runs and scores each variant; a spacedock workflow
(`ade-bench/hypotheses/`) ideates, gates, and analyzes. First target benchmark:
`ade-bench` (48 tasks). See `docs/superpowers/specs/2026-06-01-autobench-auto-research-design.md`.

## Submodules (read-only — never edit)

- `razorback/` — benchmark runner. Run `rk` from `ade-bench/`:
  `uv run --project ../razorback rk <args>`. (Optional shell alias:
  `alias rk='uv run --project '"$PWD"'/razorback rk'`.)
- `spacedock/` — workflow framework + `first-officer`/`ensign` skills + the `status` CLI
  at `spacedock/skills/commission/bin/status`.

## 🔒 Run prerequisites (load-bearing — before any `rk run`)

- `export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"` —
  specs with `agent.kind: spacedock_solver` fail at agent setup without it.
- `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` set; codex auth configured (the
  first loops run on a flat OpenAI personal subscription).
- Docker / Colima running (Harbor's execution environment).
- The ade-bench dataset resolves anonymously (it is public).

## Running the loop

1. Seed a concept: `ade-bench/hypotheses/concept-<slug>.md`.
2. Start the orchestrator: `spacedock:first-officer` on `ade-bench/hypotheses/`.
3. Flow: concept → `ideate` (fan-out) ; hypothesis → `propose` → `smoke` → `full` →
   `analyze` → `conclude`.
4. Two human gates: `propose` (leak-guard) and `smoke → full` (go/no-go). Always pass
   `--runs-dir runs`; prefer `rk run --explain` first.

## 🔒 The independent-variable rule

Only the solver README changes between hypotheses. Runtime (codex), model (gpt-5.5),
sampling, `reasoning_effort: xhigh`, `trials: 1` (every run, smoke and full), and spec
shape are held constant. A variant spec differs from `ade-bench/specs/baseline.yaml`
only in `experiment:` + `solver_workflow:`. Anything else is a separate, declared
hypothesis.

## 🔒 Leak-guard discipline

The workspace data is the only authoritative source. The solver README's
**External-oracle audit** section must stay intact (no HuggingFace `datasets`/`hf://`,
no canonical-data downloads, no web search, no LLM-as-oracle). `rk audit --policy strict`
is the backstop. Enforce at the `propose` gate.

## Budget discipline

`rk run --explain` ($0) first; smoke (the hypothesis's target datasets) before full.
Budget caps are **deferred** while on a flat OpenAI subscription; reinstate
`--max-budget-usd-running` / `experiment_meta.max_budget_usd` when moving to metered API.

## 🔒 Reproducibility discipline

Always `rk freeze` (seals the solver-README content hash). The dataset digest is pinned.
A frozen spec + README hash are immutable once smoke starts.

## Native primitives

- Champion = `@baseline`: `rk baseline promote <run-dir>` + `rk registry add run baseline <run-dir>`.
- Compare: `rk runs diff "$(... rk registry resolve run @baseline)" <variant-run-dir>`.
- Per-cell pipeline: `ade-bench/drivers/matrix.sh` (chains run + `captured>0` + audit + score + ledger).

## Monitoring & log analysis

Live: `<run-dir>/job.log`, `<cell>/trial.log`, main agent `<cell>/agent/codex.txt`;
sub-agent (ensign) transcripts under `<cell>/agent/sessions/<year>/…` (dispatch summary
in `<cell>/subagent-trace-manifest.json`); grader output in `<cell>/verifier/`
(`reward.txt`, `test-stdout.txt`); failures in `<cell>/exception.txt`; results in
`summary.json` / `per_trial_outcomes.json` / `result.json`. `events.jsonl` is often
**empty** for these Harbor runs — do not rely on it. The `analyze` stage reads these
per-task logs for distance-to-pass + behavioral findings.

## Safety

Never delete or rewrite existing run directories unless asked. Keep outputs under
`ade-bench/runs/` (gitignored). Do not move run outputs into tracked files.
```

- [ ] **Step 2: Commit**

```bash
git add AGENTS.md
git commit -m "docs: add repo-root AGENTS.md operator guide"
```

---

## Task 7: Write the repo-root `CLAUDE.md`

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Write `CLAUDE.md`**

Write exactly:

```markdown
# CLAUDE.md

**Read `AGENTS.md` first — it is the operating guide for this repo; everything in it
applies.**

Claude-Code specifics:

- Use the `spacedock:first-officer` skill to run or resume the autoresearch loop on
  `ade-bench/hypotheses/`.
- Use the `superpowers:brainstorming` skill when standing up a new benchmark or a new
  research concept.
- You are the **operator** of the loop, not the solver. The codex solver
  (`agent.kind: spacedock_solver`, `runtime: codex`) is spawned by razorback inside
  Harbor — you drive `rk` and the spacedock workflow, you do not solve the tasks.
- `rk` is run from `ade-bench/` as `uv run --project ../razorback rk <args>`; export
  `RAZORBACK_SPACEDOCK_PLUGIN_DIR` before any `rk run` (see AGENTS.md → Run prerequisites).
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add repo-root CLAUDE.md (defers to AGENTS.md)"
```

---

## Task 8: Write the repo-root `README.md`

**Files:**
- Modify (overwrite): `README.md` (currently just `# autobench`)

- [ ] **Step 1: Overwrite `README.md`**

Write exactly:

```markdown
# autobench

Auto-research repo for AI-agent benchmarks. It runs a spacedock workflow that fine-tunes
a **solver-workflow README** to maximize a benchmark score, with [razorback](https://github.com/spacedock-dev/razorback)
executing and scoring each variant.

First target: **ade-bench** (48 dbt-repair tasks). Baseline to beat: **9/48 (0.1875)**.

## Layout

- `ade-bench/` — the per-benchmark research repo (`rk research new` layout):
  `specs/`, `solver_workflows/`, `hypotheses/` (the spacedock workflow), `drivers/matrix.sh`,
  `razorback-research.toml`, `runs/` (gitignored).
- `razorback/`, `spacedock/` — submodules (read-only).
- `ade-bench-datasets.md` — the 48 ade-bench task names + difficulties.
- `docs/superpowers/` — design spec + implementation plan.

## Operating the loop

See `AGENTS.md` (operator guide) and `CLAUDE.md`. In short: seed a concept under
`ade-bench/hypotheses/`, run `spacedock:first-officer` on that directory, and approve at
the `propose` (leak-guard) and `smoke → full` (go/no-go) gates.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: expand repo-root README with layout + operating guide"
```

---

## Task 9: Establish the 9/48 `@baseline` (LIVE — requires Docker + codex auth)

This is the one expensive, long-running task: a full 48-task run of the baseline spec to
produce the `@baseline` anchor. It needs the run prerequisites satisfied.

**Files:**
- Create: `ade-bench/hypotheses/h0000-baseline.md`
- Modify (via `rk registry`): `ade-bench/razorback-research.toml`

- [ ] **Step 1: Verify prerequisites**

Run (from repo root):
```bash
export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(pwd)/spacedock"
docker info >/dev/null 2>&1 && echo "docker OK" || echo "START DOCKER FIRST"
echo "RAZORBACK_SPACEDOCK_PLUGIN_DIR=$RAZORBACK_SPACEDOCK_PLUGIN_DIR"
```
Expected: `docker OK` and the env var pointing at `<repo>/spacedock`. Confirm codex auth / OpenAI subscription is configured before proceeding.

- [ ] **Step 2: Seed the baseline entity (skips smoke)**

Create `ade-bench/hypotheses/h0000-baseline.md`:

```markdown
---
id: h0000
title: Baseline — codex ade-dbt-repair solver, full 48 tasks
status: full
kind: hypothesis
source: setup
started:
completed:
verdict:
score:
worktree:
---

## Hypothesis

Establish the anchor: the baseline codex solver README on all 48 ade-bench tasks. No
README change — this defines `@baseline` and the 9/48 (0.1875) reference. Skips smoke.

## Run result

## Behavioral analysis

## Verdict
```

- [ ] **Step 3: Pre-flight the run ($0)**

Run (from `ade-bench/`):
```bash
uv run --project ../razorback rk run specs/baseline.frozen.yaml --explain
```
Expected: a resolved plan with `agent.kind: spacedock_solver`, `runtime: codex`, the pinned dataset, and the sealed solver-workflow hash. If it disagrees with the spec, STOP.

- [ ] **Step 4: Run the full baseline (LONG — 48 tasks)**

Run (from `ade-bench/`):
```bash
uv run --project ../razorback rk run specs/baseline.frozen.yaml --runs-dir runs
```
Expected: a run-dir under `runs/ade-bench-baseline/<sealed-hash>/`. Capture the path:
```bash
BASELINE_RUN=$(ls -dt runs/ade-bench-baseline/*/ | head -1); echo "$BASELINE_RUN"
```

- [ ] **Step 5: Audit (strict) and score**

Run (from `ade-bench/`):
```bash
uv run --project ../razorback rk audit "$BASELINE_RUN" --policy strict
uv run --project ../razorback rk score "$BASELINE_RUN" --format json | tee "$BASELINE_RUN/score.json"
```
Expected: audit clean (`taint_status: clean`); `score.json` `stratified_pass_at_1` ≈ `0.1875` (9/48). Record the actual value (it anchors the campaign).

- [ ] **Step 6: Bind `@baseline`**

Run (from `ade-bench/`):
```bash
uv run --project ../razorback rk baseline promote "$BASELINE_RUN"
uv run --project ../razorback rk registry add run baseline "$BASELINE_RUN"
uv run --project ../razorback rk registry resolve run @baseline
```
Expected: the last command prints the baseline run-dir path; `razorback-research.toml` now has a `[[refs]]` entry binding `@baseline`.

- [ ] **Step 7: Record the headline + conclude the baseline entity**

Edit `ade-bench/hypotheses/h0000-baseline.md`: paste the `score.json` headline into
`## Run result`, a short behavioral note (which task groups passed/failed) into
`## Behavioral analysis`, set `status: conclude`, `completed:` (today), `verdict: PASSED`,
`score:` (the measured pass rate), and write `## Verdict`.

- [ ] **Step 8: Commit (specs/entity/registry; runs/ stays ignored)**

```bash
cd ..
git add ade-bench/hypotheses/h0000-baseline.md ade-bench/razorback-research.toml
git commit -m "feat: establish @baseline from the full ade-bench baseline run (9/48 anchor)"
```

---

## Done

The loop is ready: seed a `concept-<slug>.md`, run `spacedock:first-officer` on
`ade-bench/hypotheses/`, and iterate. The next hypothesis forks `@baseline`'s solver
README, smokes its target datasets, runs full, and is judged by `rk runs diff` + the
behavioral log read.
