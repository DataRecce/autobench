# autobench — Auto-Research Repo Design

**Date:** 2026-06-01
**Status:** Approved design (pre-implementation)
**Author:** Kent Huang (with Claude Code, brainstorming session)

## 1. Purpose

`autobench` is an **auto-research repository**. It drives a closed research loop that
fine-tunes the README of a [spacedock](https://github.com/spacedock-dev/spacedock)
solver workflow — the **independent variable** — to maximize the score of an AI-agent
benchmark run by [razorback](https://github.com/spacedock-dev/razorback).

The loop is: **goal/concept → ideate hypotheses → smoke test → full run → analyze
outcome → propose the next hypothesis → (repeat) → complete.**

- **razorback** executes the benchmark from a frozen spec (YAML), audits the run for
  leakage, and scores it. The research loop only maintains the spec and the solver
  README; razorback owns execution, auditing, and scoring.
- **spacedock** orchestrates the research loop: each hypothesis is an entity that flows
  through stages dispatched by the `first-officer`, with work done by `ensign` agents.
- **First target benchmark:** `ade-bench` (autonomous data-engineering / dbt repair),
  pinned at `dbt-labs/ade-bench@sha256:2c1f9e6966d01b0a5de2235d1a0b64089c7eead42c85c3b7b61d0929405c2bd5`
  — **48 tasks** across 6 groups (Airbnb, Analytics-Eng, Asana, F1, Intercom,
  QuickBooks), each tagged easy/medium/hard (see `ade-bench-datasets.md`).
- **Solver runtime (held constant):** `codex` (`gpt-5.5`).
- **Baseline to beat:** there is no published paper baseline. The current
  spacedock-solver run scores **9/48 = 0.1875** on `stratified_pass_at_1`; that number
  is the anchor every hypothesis tries to beat.

### Design grounding: razorback's canonical autoresearch repo

razorback ships `rk research new <slug> --from <dataset>`, which scaffolds the exact
autoresearch repo this design targets, and provides native primitives for the loop:

- `rk research new` → the canonical layout (`specs/`, `solver_workflows/`,
  `hypotheses/`, `drivers/matrix.sh`, `razorback-research.toml`).
- `rk baseline promote` + a `@baseline` entry in `razorback-research.toml` (via
  `rk registry add`) → the **champion mechanism**.
- `rk runs diff <baseline-run> <variant-run>` → **paired delta** with bootstrap CIs and
  Holm-Bonferroni-adjusted p-values.
- `drivers/matrix.sh` → per-cell `rk run → audit → score`, which **rejects cells whose
  `subagent-trace-manifest.json` has `captured == 0`** (the spacedock crew failed to
  load) and rejects tainted (leaked) cells.

`rk-monitor` (a sibling repo) is the **manual precursor**: it runs ade-bench through
razorback by hand and ran the first experiments. autobench automates that loop with a
spacedock workflow and reuses rk-monitor's proven conventions.

**The design therefore rebases onto razorback's canonical layout and layers our
additions on top:** a `concept → ideate` *breadth* front-end and first-officer
orchestration with two human gates. It assembles the paved path; it does not reinvent
baseline/diff/scoring.

## 2. Decisions (this session)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Foundation | **Rebase onto `rk research new` canonical layout + spacedock layer** | Native `@baseline` registry, `rk runs diff`, `matrix.sh`, flat `solver_workflows/`+`specs/`. We upgrade `hypotheses/` into the spacedock workflow. Least custom code; most reproducible. (Option A.) |
| Per-benchmark namespacing | **Each benchmark = a `rk research new` subdir** (`ade-bench/`) | autobench is a multi-benchmark umbrella; a 2nd benchmark is a sibling `rk research new` subdir. |
| Autonomy | **Semi-autonomous, two human gates** | Gate at `propose` (leak-guard review of the README) and at `smoke → full` (go/no-go before the full run). Everything else auto. |
| Baseline / target | **Initial spacedock run = 9/48 (0.1875)** | No published paper baseline. The first full baseline run scores 9/48; it seeds `@baseline` and `experiment_meta.paper_baseline.value: 0.1875`. Hypotheses aim to beat it. |
| Budget caps | **Deferred — flat OpenAI subscription** | First loops run on an OpenAI personal subscription, not metered API. Omit `max_budget_usd` / `--max-budget-usd-running` for now; reinstate when moving to metered spend. The `smoke → full` gate remains as a worthiness go/no-go. |
| Smoke subset | **Hypothesis's target datasets; first run skips smoke** | `rk run` has no task-selector flag — subsetting is spec-side. Smoke runs a sibling smoke spec (the full hypothesis spec + `benchmark.tasks` = the target datasets); a general change with no targets uses `benchmark.n_tasks`. The baseline/first run skips smoke and runs full directly. |
| Trials per run | **Always `trials: 1`** | Both smoke and full use `trials: 1` / `concurrency.trials: 1` — one trial per task, every run. Held constant. |
| Solver runtime | **codex** (`gpt-5.5`) | One runtime held constant → the README is the only variable. Baseline solver is razorback's `codex-ade-dbt-minimal` (the solver behind the 9/48 anchor). |
| Ideation / loop closure | **Two birth paths, prompt-driven** | A `concept` fans out via `ideate` into many `hypothesis` entities (breadth); each `conclude` files one failure-driven follow-up `hypothesis` (depth). Ensigns write the entity files — no spacedock mod. |
| Champion | **Native `@baseline` registry + `rk baseline promote`** | Replaces a custom `CHAMPION.md`. `conclude` promotes a winner and re-binds `@baseline`. |
| Comparison | **`rk runs diff @baseline <variant>` + `rk score`** | Paired delta (CIs, adjusted p) for the promotion verdict; `rk score` for the absolute `stratified_pass_at_1` vs `paper_baseline`. |
| Analyze depth | **Score diff + per-task distance-to-pass + behavioral log read** | `analyze` pairs the quantitative diff with per-task distance-to-pass (`checks_passed / expected_test_count` from `verifier/test-stdout.txt`) and a read of the main + sub-agent logs (method-adherence, why-it-works / why-it-fails). These findings — not just the binary delta — seed the next hypothesis. |
| Hypothesis entity form | **Flat `h<NNNN>-<slug>.md`** (folder form optional) | Canonical naming. The heavy artifacts live in sibling `solver_workflows/` + `specs/`, keyed by the same slug. |

## 3. Repo structure

`ade-bench/` is generated by `rk research new ade-bench --into ./ade-bench
--solver-runtime codex --target-model gpt-5.5`; we then upgrade `hypotheses/` into a
spacedock workflow and fork the codex solver baseline.

```
autobench/
├── README.md                       # what autobench is + how to run the loop
├── CLAUDE.md                       # thin Claude-Code preface → defers to AGENTS.md
├── AGENTS.md                       # canonical operator guide (Codex + source of truth)
├── ade-bench-datasets.md           # the 48 ade-bench task names + difficulties (reference)
├── recce.yml                       # pre-existing; unrelated, left as-is
├── .gitmodules
├── razorback/                      # submodule — benchmark runner (rk)        [read-only]
├── spacedock/                      # submodule — workflow framework            [read-only]
│
├── ade-bench/                      # = `rk research new ade-bench …` output
│   ├── razorback-research.toml     #   named-ref registry: @baseline (← champion), @latest
│   ├── README.md                   #   razorback's repo readme (first-run + lifecycle)
│   ├── specs/
│   │   ├── baseline.yaml            #     spacedock_solver/codex/gpt-5.5; solver_workflow: ./solver_workflows/codex-ade-dbt-minimal
│   │   ├── baseline.frozen.yaml     #     after `rk freeze`
│   │   └── h0001-<slug>.yaml         #     variant spec: repoints solver_workflow + experiment
│   ├── solver_workflows/            #   ← THE independent variable (flat, one dir per variant)
│   │   ├── codex-ade-dbt-minimal/README.md  # razorback's codex-ade-dbt-minimal — the 9/48 baseline solver
│   │   └── h0001-<slug>/README.md    #     the variant under test
│   ├── hypotheses/                  #   ← UPGRADED into the spacedock experiment workflow
│   │   ├── README.md                #     commissioned-by: spacedock@ + concept→ideate→…→conclude
│   │   ├── concept-<slug>.md         #     CONCEPT entity (flat .md): a research direction to ideate from
│   │   ├── h0001-<slug>.md           #     HYPOTHESIS entity (flat .md): notes + accumulated evidence
│   │   ├── _archive/                #     concluded/expanded entities
│   │   └── _debriefs/               #     session records
│   ├── drivers/matrix.sh            #   per-cell run+audit+score; captured>0 + taint guards; ledger.tsv
│   └── runs/                        #   razorback run outputs (gitignored)
│
└── docs/superpowers/specs/          #   design docs (this file)
```

### Conventions

- **`ade-bench/hypotheses/` is the spacedock workflow directory** — its `README.md`
  carries `commissioned-by: spacedock@…` (how `status --discover` recognizes it) and
  defines the stages. It holds two entity kinds, both defined by a markdown file:
  **concepts** (`concept-<slug>.md`) and **hypotheses** (`h<NNNN>-<slug>.md`; folder
  form `h<NNNN>-<slug>/index.md` is allowed when evidence accumulates).
- **The independent variable is `ade-bench/solver_workflows/h<NNNN>-<slug>/README.md`**
  — kept flat (canonical layout), forked from the current `@baseline`'s solver
  workflow, frozen + content-hashed per hypothesis via `rk freeze`.
- **The variant spec is `ade-bench/specs/h<NNNN>-<slug>.yaml`** — a copy of
  `baseline.yaml` with `experiment:` renamed and `solver_workflow:` repointed at the
  matching `solver_workflows/` dir.
- **Champion = the `@baseline` registry entry** in `razorback-research.toml`, promoted
  via `rk baseline promote` + `rk registry add run baseline <run-dir>`.
- **`runs/` is gitignored.** Specs and solver READMEs are tracked; run outputs are not.
- **Adding a second benchmark later** = `rk research new <other> --into ./<other>` and
  the same `hypotheses/` upgrade.

## 4. The research loop

The loop is a spacedock experiment workflow at `ade-bench/hypotheses/README.md`, built
by upgrading the `rk research new` `hypotheses/` notes README into a
spacedock-commissioned workflow. It preserves razorback's canonical stage semantics
(`propose` edits `solver_workflows/…`, writes `specs/…`, freezes; `analyze` runs
`rk runs diff`; `conclude` promotes `@baseline`) and adds the `concept → ideate`
breadth front-end and the two gates. **First-officer** orchestrates; **ensigns** run the
`rk` commands; `drivers/matrix.sh` chains the per-cell pipeline.

The workflow has **two entity kinds on two paths**, sharing one directory; both birth
mechanisms are prompt-driven (the acting ensign writes the new entity file — no mod).

### Concept path (divergent — breadth)

| Stage | Gate? | What happens |
|-------|-------|--------------|
| `concept` *(initial)* | — auto | A research direction is filed (by you or the first-officer): a plain-English theme + rationale (e.g. "give the solver a structured dbt-repair triage checklist"). The "provide goal or concept" entry point. Auto-advances. |
| `ideate` | — auto | An ensign reads the concept + the current `@baseline` solver README + prior learnings, **generates multiple candidate hypotheses, and writes each as a new `hypothesis` entity** (`h<NNNN>-<slug>.md`, each naming the solver-README change it will make). Then the concept advances to `expanded`. |
| `expanded` *(terminal)* | — auto | The concept has been turned into hypotheses; archived. |

No gate on `ideate` — every generated hypothesis is gated individually at its own
`propose`, so spend stays controlled without a breadth gate.

### Hypothesis path (the test pipeline — depth)

| Stage | Gate? | What happens |
|-------|-------|--------------|
| `hypothesis` *(initial)* | — auto | A fully-formed, queued hypothesis: title, falsifiable claim, `## Acceptance criteria` (the verdict, e.g. "the paired `rk runs diff` delta vs `@baseline` clears the tripwire on `stratified_pass_at_1`"). Born from an `ideate` fan-out or a `conclude` follow-up. Auto-advances. |
| `propose` | 🚦 **leak-guard** | Ensign forks `@baseline`'s solver dir to `solver_workflows/h<NNNN>-<slug>/`, edits its `README.md` (the one variable), copies `specs/baseline.yaml` → `specs/h<NNNN>-<slug>.yaml` (repointing `solver_workflow:` + `experiment:`), and `rk freeze`s it. **Human reviews:** README leaks no ground truth (the leak-guard prose is intact); spec is `spacedock_solver`/`codex`; budget + baseline present. |
| `smoke` | 🚦 **go/no-go** | Run the **smoke spec** (hypothesis spec + `benchmark.tasks` = its **target datasets**): `rk run --explain` (free) → `rk run <smoke-frozen> --runs-dir runs` → `captured > 0` → `rk audit --policy strict` → `rk score`. **Human reviews** the focused result before committing the full run. *(Budget caps deferred — this is a worthiness gate.)* |
| `full` | — auto | `drivers/matrix.sh` (or `rk run` with no `tasks` selector) over all 48 tasks: per-cell run → `captured > 0` → `rk audit --policy strict` → `rk score`. Auto-advances on a clean ledger. |
| `analyze` | — auto | **Quantitative:** `rk runs diff "$(rk registry resolve run @baseline)" <variant-run-dir>` (paired delta, CIs, adjusted p) + absolute `rk score` vs `paper_baseline`. **Behavioral (§5.6):** read the per-task agent logs — main `agent/codex.txt`, sub-agent `agent/sessions/…`, `subagent-trace-manifest.json`, `verifier/` — for verdict-changed and failing tasks, capturing per-task **distance to pass** (`checks_passed / expected_test_count`) and judging method-adherence and the why-it-works / why-it-fails mechanisms. Both written into the entity body; verdict line written. |
| `conclude` *(terminal)* | — auto | Verdict recorded. **If the paired delta clears the tripwire (and audit was clean) → promote:** `rk baseline promote <variant-run-dir>` + `rk registry add run baseline <variant-run-dir>`. Then, **using analyze's behavioral findings (method-adherence + failure mechanisms), file one follow-up `hypothesis` entity** (forking the new `@baseline`). Archived. |

> **Gate mechanics:** in spacedock a stage's `gate: true` fires at the boundary
> *leaving* that stage. `gate: true` on `propose` = the `propose → smoke` review (the
> README); `gate: true` on `smoke` = the `smoke → full` review (go/no-go before full).
> All other stages are `gate: false`. Net: exactly two human gate types, both on the
> hypothesis path.

> **Baseline / first run:** establishing the 9/48 anchor is a direct full run — the
> baseline entity **skips `smoke`** (`propose → full`) and, at `conclude`, binds
> `@baseline` to its run-dir. Every later hypothesis forks from `@baseline` and does
> run `smoke` on its target datasets.

### Entity lifecycle

One hypothesis = one flat `h<NNNN>-<slug>.md` whose body accumulates evidence as it
flows: claim → smoke result → full result → `rk runs diff` delta → verdict. Its frozen
spec (`specs/`) + solver README (`solver_workflows/`) make it a reproducible record. A
concept is a lightweight flat file recording the direction and the hypotheses it
spawned.

### Loop closure (the two engines)

- **Breadth:** a `concept` → `ideate` produces several hypotheses at once.
- **Depth:** each `conclude` → files one follow-up `hypothesis` from the failure modes.

First-officer keeps dispatching while dispatchable entities exist; when the backlog
empties, you file a new `concept`.

### Termination ("complete")

A hypothesis self-terminates at `conclude`; a concept at `expanded`. The *campaign* is
open-ended and **you** end it — when the score plateaus, hits a target, or the budget is
spent. Auto stages move work forward; the two gates keep you in the loop (you see every
new README and approve every full-run spend).

### Concurrency

Kept low. Full runs cost money and serialize on the money gate. An `ideate` fan-out can
queue many hypotheses; they progress as gates clear, not all at once.

## 5. The spec ↔ solver-workflow contract

### 5.1 The baseline spec (canonical shape, ade-bench/codex)

`ade-bench/specs/baseline.yaml`, derived from `rk research new` + rk-monitor's
`spacedock-harness-gpt-5.5-xhigh-full48.yaml`:

```yaml
version: 1
experiment: ade-bench-baseline          # variants: ade-bench-h0001-<slug>
agent:
  kind: spacedock_solver
  runtime: codex
  model: gpt-5.5
  sampling: { temperature: 0.0, top_p: null, seed: null }
  solver_workflow: ./solver_workflows/codex-ade-dbt-minimal   # variants fork to ./solver_workflows/h<NNNN>-<slug>
  spacedock_skill_version: "1.0.0"
  max_turns: 200
  override_timeout_sec: 2400
  max_timeout_sec: 2400
  reasoning_effort: xhigh                # held constant (rk-monitor used xhigh on full48)
  tools_allowed: []
  tools_denied: []
benchmark:
  kind: harbor
  dataset: dbt-labs/ade-bench@sha256:2c1f9e6966d01b0a5de2235d1a0b64089c7eead42c85c3b7b61d0929405c2bd5
  # full: whole dataset (all 48). smoke: a sibling spec adds `benchmark.tasks` =
  #   the hypothesis's target datasets. baseline / first run: skip smoke, run full directly.
trials: 1                               # one trial per task — applies to BOTH smoke and full
concurrency: { trials: 1 }
observers:
  - { kind: jsonl, path: events.jsonl }
  - { kind: stdout }
experiment_meta:
  # max_budget_usd deferred — first loops run on a flat OpenAI subscription, not metered API.
  paper_baseline: { name: pass_rate, value: 0.1875 }   # 9/48 — simple pass rate #pass/#total. rk score
                                                        # compares its stratified_pass_at_1 field, which
                                                        # for ade-bench's single dataset == #pass/#total.
provenance: { pin_model_version: false, pin_image_digest: false }
```

A variant spec is a copy with `experiment:` renamed and `solver_workflow:` repointed —
**nothing else changes** (the independent-variable rule, §6). Smoke and full use sibling
specs that differ only in that the smoke spec adds `benchmark.tasks` (the target
datasets) — `rk run` has no task-selector flag, so subsetting is spec-side. Both carry
`trials: 1` and the same solver README + content hash.

### 5.2 `rk freeze` seals the pair

Freezing resolves the model alias and computes `solver_workflow_content_hash` over the
variant README, writing `<spec>.frozen.yaml` + `provenance.yaml`. The README variant and
spec are then an immutable, reproducible unit.

### 5.3 The per-cell sandwich (`drivers/matrix.sh`)

For each cell the matrix driver runs:

```
rk run <frozen> --runs-dir runs [--max-budget-usd-running <budget-file>]
  → spacedock smoke gate: subagent-trace-manifest.json captured > 0   (REJECT cell if 0)
  → rk audit --policy strict → audit.json                             (REJECT cell if tainted)
  → rk score → score.json   (paper_baseline auto-pulled from experiment_meta)
  → ledger.tsv row: spec, status, run_dir, cost_usd, taint_count
```

Smoke is the same pipeline restricted to the hypothesis's target datasets (via the smoke
spec's `benchmark.tasks`); the baseline/first run skips smoke and runs full directly. The
`captured > 0` guard **resolves the earlier audit-coverage caveat**: a spacedock-solver
cell that didn't capture its subagent trace is rejected, not silently scored.

### 5.4 Leak-guard (the `propose` gate's reason to exist)

The solver README must keep its **no-external-reference / leak-guard prose** (the
`codex-ade-dbt-minimal` baseline states it inline): the workspace data is the only
authoritative source; forbidden — public fetches (`curl`/`wget`/`git clone`,
package-source downloads), HuggingFace `datasets`/`hf://`, web search, LLM-as-oracle.
(Not forbidden: `pip install` of generic compute libs that ship no canonical data.)
razorback's runtime `DISALLOWED_TOOLS` and `rk audit --policy strict` are the backstops;
the prose deters the rest. Tuning must never relax this; you enforce it at the gate.

### 5.5 Response variable & promotion verdict

- **Paired (promotion):** `rk runs diff @baseline <variant>` — the delta on
  `stratified_pass_at_1` with bootstrap CIs and Holm-Bonferroni-adjusted p-values. The
  variant promotes to `@baseline` only if the delta clears the tripwire (CI excludes a
  regression) on a clean audit.
- **Absolute (context):** `rk score`'s `stratified_pass_at_1` vs
  `experiment_meta.paper_baseline` (`against_constant.stratified.verdict`).

### 5.6 Behavioral analysis (the log read)

The score diff says *whether* a variant helped; the agent logs say *why*, and whether
the agent actually executed the hypothesis's method. In `analyze`, for every task whose
verdict changed vs `@baseline` (newly-passing and newly-failing) plus a sample of
persistent failures, read the per-task cell
`runs/<experiment>/<hash>/<task-id>__<short>/`:

| Artifact | What it tells you |
|----------|-------------------|
| `result.json` + `verifier/reward.txt` | the **binary verdict** (reward 0/1) |
| `verifier/test-stdout.txt` | **distance to pass** — `[ade-bench] expected_test_count=N` (denominator), the dbt `Done. PASS=… ERROR=… SKIP=… TOTAL=…` line, which target checks ran (`Including: <check>.sql`), which failed, and the concrete failure (e.g. `Catalog Error: … src_results does not exist`) |
| `agent/codex.txt` | the **main agent** (codex first-officer) transcript — plan, tool calls, ensign dispatches, validation evidence, tokens |
| `subagent-trace-manifest.json` | dispatch summary — `prompt_mode`, `captured`, each `dispatches[]` (`subagent_type: spacedock:ensign`, `spawn_index`) |
| `agent/sessions/<year>/…` | the **sub-agent (ensign)** transcripts — what each dispatched worker actually did |
| `trial.log` | harness-level per-task log |

**Distance to pass (partial progress).** The `reward` is binary, but
`test-stdout.txt` exposes how *close* a task got: `checks_passed / expected_test_count`
(and whether the dbt build itself errored before tests could even run). Record this
per task in the entity body. A hypothesis that moves a task from, say, 0/6 (build
errors) to 4/6 (builds, two checks fail) is **directional progress** even though the
verdict stayed `0` — a positive signal worth iterating on, and one the binary
`stratified_pass_at_1` hides. Note *which* checks fail and what each targets, so the
next hypothesis can aim at the specific gap.

Three questions, written into a `## Behavioral analysis` block in the entity body:

1. **Method adherence** — did the main agent *and its ensigns* actually execute the
   hypothesis's prescribed method (the README change), or ignore / misapply it? Compare
   the README's prescribed steps against the observed plan + tool calls + dispatches.
2. **Why it works** — on wins, the mechanism that produced the pass.
3. **Why it fails** — on losses, the failure mechanism: wrong diagnosis, method not
   followed, method followed but insufficient, or a harness/validation issue.

These behavioral findings — not just the score delta — are what `conclude` distills into
the next hypothesis, so the loop iterates on *understood* failure modes rather than
blind score-chasing.

## 6. CLAUDE.md & AGENTS.md

These files target the **repo operator** (Claude Code or Codex CLI driving the loop) —
not the spacedock first-officer (reads `hypotheses/README.md`) nor the codex solver
(reads `solver_workflows/<variant>/README.md`).

### File strategy: one canonical body, no drift

- **`AGENTS.md`** = full operating guide (Codex reads it; source of truth; consistent
  with razorback's and spacedock's own `AGENTS.md`).
- **`CLAUDE.md`** = short Claude-Code preface that defers to `AGENTS.md`.

### `AGENTS.md` (canonical) — sections (modeled on rk-monitor's proven content)

1. **What autobench is** — auto-research repo tuning a codex spacedock solver README to
   push ade-bench's `stratified_pass_at_1` up; razorback runs+scores, spacedock
   orchestrates. Per-benchmark subdir `ade-bench/`.
2. **Submodules** — `razorback/` (run `rk` from it via `uv`; an `rk` alias routing
   through the submodule + `uv run` is expected), `spacedock/` (workflow framework +
   first-officer/ensign skills). Both read-only.
3. **🔒 Run prerequisites (load-bearing)** — before any `rk run`:
   - `export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(pwd)/spacedock"` (specs with
     `agent.kind: spacedock_solver` fail at agent setup without it).
   - `ANTHROPIC_API_KEY` *or* `CLAUDE_CODE_OAUTH_TOKEN` in the env.
   - Docker / Colima running (Harbor's docker environment).
   - dataset ref resolves anonymously (ade-bench is public).
4. **Running the loop** — seed a `concept`, then start `spacedock:first-officer` on
   `ade-bench/hypotheses/`; two paths (concept→`ideate` fan-out; hypothesis→`propose`→
   `smoke`→`full`→`analyze`→`conclude`); two human gates (`propose`=leak-guard,
   `smoke→full`=money). Always pass `--runs-dir runs`; prefer `rk run --explain` first.
5. **🔒 The independent-variable rule** — *only* the solver README changes between
   hypotheses. Runtime (codex), model (gpt-5.5), sampling, `reasoning_effort`,
   `trials: 1` (one trial per task on every run, smoke and full), and spec shape are
   held constant. A variant spec differs from `baseline.yaml` only in `experiment:` +
   `solver_workflow:`. Anything else is a separate, declared hypothesis.
6. **🔒 Leak-guard discipline** — §5.4: workspace data only; forbidden-oracle list;
   never relax the baseline solver README's no-external-reference / leak-guard prose.
7. **Budget discipline** — `rk run --explain` ($0) first; smoke (the hypothesis's
   target datasets) before full. Budget caps **deferred** while running on a flat
   OpenAI subscription; reinstate `--max-budget-usd-running` / `max_budget_usd` when
   moving to metered API spend.
8. **🔒 Reproducibility discipline** — always `rk freeze`; the dataset digest is pinned;
   frozen spec + README hash are immutable once smoke starts.
9. **Native primitives** — champion = `@baseline` (`rk baseline promote` +
   `rk registry add run baseline <dir>`); compare with `rk runs diff @baseline <dir>`;
   per-cell pipeline = `drivers/matrix.sh` (chains audit + `captured>0` + taint guards).
10. **Monitoring & log analysis** — live: `<run-dir>/job.log`, `<cell>/trial.log`,
    main agent `<cell>/agent/codex.txt`; sub-agent (ensign) transcripts under
    `<cell>/agent/sessions/<year>/…` (dispatch summary in
    `<cell>/subagent-trace-manifest.json`); grader output in `<cell>/verifier/`;
    failures in `<cell>/exception.txt`; results in `summary.json` /
    `per_trial_outcomes.json` / `result.json`. `events.jsonl` is often **empty** — do
    not rely on it. `analyze` reads these per-task logs for the behavioral read (§5.6).
11. **Safety** — never delete/rewrite existing run directories unless asked; keep
    outputs under `runs/` (gitignored); don't move run outputs into tracked files.

### `CLAUDE.md` (thin preface)

- **"Read `AGENTS.md` first — it is the operating guide; everything in it applies."**
- Claude-Code specifics: use `spacedock:first-officer` to run/resume the loop; use
  superpowers `brainstorming` when standing up a new benchmark or concept; you are the
  **operator**, not the solver (the codex solver is spawned by razorback).

The four 🔒 sections plus run prerequisites are the load-bearing guardrails.

## 7. Out of scope / future

- **Multi-benchmark.** A second benchmark = `rk research new <slug> --into ./<slug>` +
  the `hypotheses/` upgrade. Not built now.
- **A/B-ing the runtime** (codex vs claude). Excluded — would confound the README as the
  sole independent variable.
- **Holdout tier — excluded for now (confirmed).** rk-monitor's workflow includes an
  out-of-sample `holdout` stage before accept; autobench's `conclude` is the single
  terminal. Revisit only if README overfitting to the 48 tasks becomes a concern.
- **Campaign-level auto-stop.** You end the campaign; per-entity termination is
  automatic.

## 8. Concrete config (resolved this session)

- **`paper_baseline.value` = `0.1875`** (9/48 — the initial spacedock-solver baseline;
  no published paper). Also the `@baseline` anchor.
- **Budget caps — deferred.** First loops run on a flat OpenAI personal subscription
  (not metered API); omit `max_budget_usd` / `--max-budget-usd-running`. Reinstate when
  moving to metered spend.
- **Smoke subset = the hypothesis's target datasets** (a sibling smoke spec with
  `benchmark.tasks`; a general change uses `benchmark.n_tasks`). `rk run` has no
  task-selector flag — subsetting is spec-side. **The baseline / first run skips smoke
  and runs full directly.**
- **`trials: 1` for every run** (smoke and full). `concurrency.trials: 1`. Held
  constant — one trial per task, always.
- **Dataset digest — pinned:**
  `dbt-labs/ade-bench@sha256:2c1f9e6966d01b0a5de2235d1a0b64089c7eead42c85c3b7b61d0929405c2bd5`.

Still to confirm at implementation:

- **`rk` invocation** — the alias/wrapper that routes `rk` through the `razorback/`
  submodule via `uv` in this repo.

## 9. Reusable assets

| Asset | Path |
|-------|------|
| Research-repo scaffolder | `rk research new ade-bench --from <dataset> --solver-runtime codex --target-model gpt-5.5 --into ./ade-bench` |
| Canonical template tree | `razorback/docs/templates/research-project/` (README, razorback-research.toml, hypotheses/README.md, specs/baseline.yaml, solver_workflows/baseline/README.md, drivers/matrix.sh) |
| Codex ade-dbt-minimal solver baseline (copied to `solver_workflows/codex-ade-dbt-minimal/`) | `razorback/examples/solver_workflows/codex-ade-dbt-minimal/README.md` |
| Native champion / compare | `rk baseline promote`, `rk registry add\|resolve`, `rk runs diff` |
| Per-cell driver | `ade-bench/drivers/matrix.sh` (modeled on `razorback/examples/drivers/dab-paper-matrix.sh`) |
| Layout/contents spec | `razorback/docs/superpowers/specs/2026-05-23-generic-harbor-benchmark-surface.md` §2.3 |
| Manual precursor (conventions, monitor TUI) | `rk-monitor/` — `CLAUDE.md`, `AGENTS.md`, `docs/ade-bench-experiment-workflow/`, `scripts/monitor.py` |
| ade-bench task catalog | `ade-bench-datasets.md` (48 tasks, 6 groups, difficulties) |
| Workflow orchestration | `spacedock/skills/first-officer/`, `spacedock/skills/commission/bin/status` |
