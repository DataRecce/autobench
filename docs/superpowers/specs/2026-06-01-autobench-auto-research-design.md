# autobench — Auto-Research Repo Design

**Date:** 2026-06-01
**Status:** Approved design (pre-implementation)
**Author:** Kent Huang (with Claude Code, brainstorming session)

## 1. Purpose

`autobench` is an **auto-research repository**. Its job is to drive a closed research
loop that fine-tunes the README of a [spacedock](https://github.com/spacedock-dev/spacedock)
workflow — the **independent variable** — to maximize the score of an AI-agent
benchmark, run by [razorback](https://github.com/spacedock-dev/razorback).

The loop is: **goal/concept → ideate hypothesis → smoke test → full run → analyze
outcome → propose the next hypothesis → (repeat) → complete.**

- **razorback** executes the benchmark from a frozen spec (YAML). The research loop
  only maintains the spec and the solver README; razorback owns execution, auditing,
  and scoring.
- **spacedock** orchestrates the research loop itself: each hypothesis is an entity
  that flows through stages dispatched by the `first-officer`, with work done by
  `ensign` agents.
- **First target benchmark:** `ade-bench` (autonomous data-engineering / dbt repair).
- **Solver runtime (held constant):** `codex` (`gpt-5.5`).

### Key insight that shaped this design

razorback already ships the exact loop. Its template
`razorback/src/razorback/templates/experiment-workflow/README.md` says: *"Copy this
template into a research repo to drive a single hypothesis from `pending` through
`conclude`."* **autobench is that research repo.** (We adapt that single-hypothesis
template into a continuous loop and rename its `pending` stage to `hypothesis`; see
§4.) razorback also provides:

- `agent.kind: spacedock_solver` with a `solver_workflow:` path field, and
  `solver_workflow_content_hash` sealed by `rk freeze` — i.e. "tune a workflow README,
  re-run the benchmark" is a first-class, reproducible operation.
- ade-bench as a Harbor plugin (`dbt-labs/ade-bench@…`).
- A codex ade/dbt-repair solver baseline at
  `razorback/examples/solver_workflows/codex-ade-dbt-repair/README.md`.

The design therefore **assembles the paved path**; it does not invent new mechanics.

## 2. Decisions (this session)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Organization approach | **A — razorback-native experiment repo** | Uses spacedock as the meta-orchestrator (as requested); each README variant is frozen + content-hashed = fully reproducible. (B confounds reproducibility; C abandons the spacedock loop.) |
| Autonomy | **Semi-autonomous, two human gates** | Gate at `propose` (leak-guard review of the README) and at `smoke → full` (money go/no-go). Everything else auto. Matches razorback's intent while running unattended between gates. |
| Solver runtime | **codex** (`gpt-5.5`) | Fork razorback's ade-specific `codex-ade-dbt-repair` baseline. One runtime held constant → the README is the only variable. |
| Workflow location | **`docs/ade-bench/`** | spacedock's `commission` default. (Discovery is frontmatter-based, so any path works; chose the spacedock idiom.) |
| Ideation / loop closure | **Two birth paths, prompt-driven** | A `concept` fans out via `ideate` into many `hypothesis` entities (breadth); each `conclude` files one failure-driven follow-up `hypothesis` (depth). Ensigns write the entity files — no spacedock mod. |

## 3. Repo structure

```
autobench/
├── README.md                       # what autobench is + how to run the loop
├── CLAUDE.md                       # thin Claude-Code preface → defers to AGENTS.md
├── AGENTS.md                       # canonical operator guide (Codex + source of truth)
├── recce.yml                       # pre-existing; unrelated, left as-is
├── .gitmodules
├── razorback/                      # submodule — benchmark runner (rk)        [existing, read-only]
├── spacedock/                      # submodule — workflow framework            [existing, read-only]
│
├── docs/
│   ├── ade-bench/                  # ← the spacedock auto-research workflow
│   │   ├── README.md               #   experiment-workflow def (commissioned-by: spacedock@…)
│   │   ├── concept-<slug>.md        #   CONCEPT entity (flat .md): a research direction to ideate from
│   │   ├── 0001-<slug>/            #   HYPOTHESIS entity (folder): one testable README variant
│   │   │   ├── index.md            #     task definition: hypothesis, AC, smoke/full notes, analyze, conclude
│   │   │   ├── solver_workflow/
│   │   │   │   └── README.md        #     ← THE independent variable: this variant's solver README
│   │   │   ├── spec.frozen.yaml     #     rk-frozen spec; seals solver_workflow_content_hash
│   │   │   └── runs/                #     durable evidence: audit.json, score.json, events.jsonl
│   │   ├── 0002-<slug>/ …
│   │   ├── _archive/               #   concluded/expanded entities (status viewer moves them here)
│   │   └── _debriefs/              #   session records (spacedock debrief)
│   └── superpowers/specs/          #   design docs (this file)
│
├── solver_workflows/
│   └── ade-bench/
│       ├── baseline/README.md       # genesis: fork of razorback codex-ade-dbt-repair (immutable)
│       └── CHAMPION.md              # pointer: current best hypothesis id + score + path
│
├── specs/
│   └── ade-bench/
│       ├── smoke.yaml               # unfrozen template: spacedock_solver + codex, n_tasks small
│       └── full.yaml                # unfrozen template: full ade-bench dataset
│
├── runs/                            # rk run output root (gitignored — large)
│
└── scripts/
    └── new-hypothesis.sh            # thin helper: scaffold a hypothesis folder by forking CHAMPION
```

### Conventions

- **`docs/ade-bench/` is a spacedock workflow directory.** Its `README.md` is the
  workflow definition (carries `commissioned-by: spacedock@…`, which is how
  `status --discover` recognizes it). It holds **two entity kinds**, both defined by a
  markdown file: **concepts** are flat files `concept-<slug>.md`; **hypotheses** are
  folders `NNNN-<slug>/` whose `index.md` is the task definition (spacedock folder
  form). Adding a second benchmark later = a sibling `docs/<benchmark>/`.
- **The independent variable is `docs/ade-bench/<hyp>/solver_workflow/README.md`** —
  frozen and content-hashed per hypothesis, so every experiment is reproducible.
- **`solver_workflows/ade-bench/baseline/`** is the immutable genesis README (the
  razorback fork); **`CHAMPION.md`** records the reigning best. Hypothesis `0001`
  forks from `baseline/`; later hypotheses fork from the champion.
- **`specs/ade-bench/{smoke,full}.yaml`** are unfrozen templates. The `propose` stage
  copies one, points `solver_workflow:` at the hypothesis's `solver_workflow/`, and
  freezes it into `spec.frozen.yaml`.
- **`runs/` is gitignored.** Durable evidence (`audit.json`, `score.json`,
  `events.jsonl`) is copied into each hypothesis's `runs/` so the folder is
  self-contained.

## 4. The research loop

The loop is a spacedock experiment workflow (`docs/ade-bench/README.md`), forked from
`razorback/src/razorback/templates/experiment-workflow/README.md` and re-gated to the
"auto except money + leak" autonomy choice. **First-officer** orchestrates; **ensigns**
execute each stage; razorback's `rk` does the benchmark work.

The workflow has **two entity kinds on two paths**, sharing one stage graph and one
directory:

- a **concept** (flat `concept-<slug>.md`) fans out into many hypotheses — *breadth*;
- a **hypothesis** (folder `NNNN-<slug>/`) is tested end-to-end and, at `conclude`,
  may spawn one failure-driven follow-up hypothesis — *depth*.

Both birth mechanisms are **prompt-driven**: the acting ensign writes the new entity
file(s). No spacedock mod is required, matching razorback's mod-free template.

### Concept path (divergent — breadth)

| Stage | Gate? | What happens |
|-------|-------|--------------|
| `concept` *(initial)* | — auto | A research direction is filed (by you or the first-officer): a plain-English theme + rationale (e.g. "give the solver a structured dbt-repair triage checklist"). This is the "provide goal or concept" entry point. Auto-advances. |
| `ideate` | — auto | An ensign reads the concept + current `CHAMPION.md` + prior learnings, **generates multiple candidate hypotheses, and writes each as a new `hypothesis`-stage entity** (folder, forked from the champion README). Then the concept advances to `expanded`. |
| `expanded` *(terminal)* | — auto | The concept has been turned into hypotheses; archived. |

There is **no gate on `ideate`** — every generated hypothesis is gated individually at
its own `propose` step, so spend stays controlled without a breadth gate.

### Hypothesis path (the test pipeline — depth)

| Stage | Gate? | What happens |
|-------|-------|--------------|
| `hypothesis` *(initial)* | — auto | A fully-formed, queued hypothesis: title, plain-English claim, `## Acceptance criteria` naming the verdict (e.g. "beats CHAMPION's `stratified_pass_at_1` on full ade-bench"). Born from an `ideate` fan-out or a `conclude` follow-up. Auto-advances. |
| `propose` | 🚦 **leak-guard** | Ensign writes/edits this variant's `solver_workflow/README.md` and the frozen spec. **Human reviews at the gate:** README leaks no ground truth; spec has `max_budget_usd` + `paper_baseline`; `agent.kind: spacedock_solver`, `runtime: codex`. |
| `smoke` | 🚦 **money go/no-go** | `rk run --explain` (free) → budget check → per-cell `rk run` → `rk audit --policy strict` → `rk score` on `n_tasks` small. **Human reviews at the gate** before committing real spend to the full run. |
| `full` | — auto | Same sandwich over the full ade-bench dataset, with `--max-budget-usd-running` as the hard backstop. Auto-advances on success. |
| `analyze` | — auto | `rk score` rolls up `stratified_pass_at_1` vs `paper_baseline`; verdict (`above` / `inside_ci` / `below`) written into `index.md`. |
| `conclude` *(terminal)* | — auto | Verdict recorded. If this variant beats CHAMPION (and audit passed) → promote (update `CHAMPION.md`). Then, **based on this run's failure pattern, file one follow-up `hypothesis` entity** (forking the possibly-new champion). Archived. |

> **Gate mechanics note:** in spacedock, a stage's `gate: true` fires at the boundary
> *leaving* that stage. So `gate: true` on `propose` is the `propose → smoke` review
> (the README), and `gate: true` on `smoke` is the `smoke → full` review (the money
> go/no-go). All other stages are `gate: false`. Net: exactly two human gate types,
> both on the hypothesis path.

### Entity lifecycle

One hypothesis = one folder/entity. Its `index.md` accumulates evidence as it flows:
claim → smoke result → full result → analyze verdict → conclude paragraph. The frozen
spec + `solver_workflow/README.md` make it a permanent, reproducible record of that
variant. A concept is a lightweight flat file that records the direction and links to
the hypotheses it spawned.

### Loop closure (the two engines)

- **Breadth:** a `concept` → `ideate` produces several hypotheses at once — exploring
  distinct directions in parallel.
- **Depth:** each `conclude` → files one follow-up `hypothesis`, taking the failure
  modes surfaced in `analyze` and proposing the next README change.

Together these keep the loop self-sustaining. First-officer keeps dispatching while
dispatchable entities exist; when the backlog empties, you file a new `concept`.

### Termination ("complete")

A single hypothesis self-terminates at `conclude`; a concept self-terminates at
`expanded`. The *campaign* is open-ended and **the human** ends it — when the score
plateaus, hits a target, or the budget is spent. Because the auto stages move work
forward but `propose`/`smoke` are gated, the human naturally stays in the loop (sees
every new README, approves every full-run spend) without babysitting mechanical steps.

### Concurrency

Kept low (1–2). Full runs cost money and serialize on the money gate. Note that an
`ideate` fan-out can queue many hypotheses at once — they progress as gates clear, not
all simultaneously.

## 5. The spec ↔ solver-workflow contract

Three artifacts per hypothesis, bound together by `rk freeze`.

### 5.1 Unfrozen spec templates

`specs/ade-bench/{smoke,full}.yaml`, modeled on
`razorback/examples/specs/codex-ade-bench-smoke.yaml`. The `propose` stage copies one,
points it at the hypothesis's README, and freezes it:

```yaml
version: 1
experiment: ade-bench-<id>-smoke
agent:
  kind: spacedock_solver
  runtime: codex                       # runtime choice, held constant
  model: gpt-5.5
  sampling: { temperature: 0.0, top_p: null, seed: 1 }
  reasoning_effort: high
  solver_workflow: ./solver_workflow    # relative to the hypothesis folder = the variant
  max_turns: 200
  tools_allowed: []
  tools_denied: []                      # leak-guard surface (block oracle tools here)
benchmark:
  kind: harbor
  dataset: dbt-labs/ade-bench@sha256:<pinned-digest>   # pin a digest for reproducibility
  n_tasks: 1                            # SMOKE only; full.yaml omits this
trials: 1
concurrency: { trials: 1 }
observers:
  - { kind: jsonl, path: events.jsonl }
  - { kind: stdout }
experiment_meta:
  max_budget_usd: 5.00                  # hard cap; full.yaml sets a higher ceiling
  paper_baseline: { name: stratified_pass_at_1, value: <ade-bench baseline> }
```

`full.yaml` is identical except it omits `n_tasks` (full dataset) and sets a higher
`max_budget_usd`.

### 5.2 `rk freeze` seals the pair

Freezing in the hypothesis folder computes `solver_workflow_content_hash` over the
README and writes `spec.frozen.yaml`. From that point the README variant and spec are
an immutable, reproducible unit — the heart of "the README is the independent
variable."

### 5.3 The `rk` sandwich

Run by smoke and full ensigns, per cell:

```bash
rk run --explain <frozen>                    # free pre-flight: catches spec/translator errors at $0
rk runs cost <run-root>                       # budget pre-check vs max_budget_usd
rk run <frozen> --task-id <t> --out <cell>    # the live burn (codex solver in Harbor/docker)
rk audit --policy strict <cell>               # fail if forbidden oracle calls in the event log
rk score <cell>                               # stratified_pass_at_1 vs paper_baseline
```

`runs/audit.json` + `runs/score.json` are copied into the hypothesis folder as durable
evidence. (Canonical sandwich reference:
`razorback/examples/drivers/dab-paper-matrix.sh`.)

### 5.4 Leak-guard (the `propose` gate's reason to exist)

The README variant must state *"the workspace data is the only authoritative source"*
and forbid external oracles:

- HuggingFace `datasets` (`load_dataset`, `hf://…`)
- public CSV/JSON downloads (kaggle, GitHub, vendor mirrors)
- web-search engines / search APIs
- LLM-as-oracle calls
- cached prior answers from earlier runs or any artifact outside the workspace

The codex baseline already forbids network access and external datasets; tuning must
never relax this. Canonical leak-guard prose source:
`razorback/packages/razorback-plugin-dab/src/razorback_plugin_dab/generate/workspace_readme.py`.

### 5.5 Response variable & scoring

`score.json → stratified_pass_at_1`, compared to `paper_baseline`
(`against_constant.stratified.verdict`: `above` / `inside_ci` / `below`). That single
number is what each hypothesis moves. `rk score` auto-pulls `paper_baseline` from the
frozen spec — do not pass `--against-constant` on the CLI.

### 5.6 Known caveat (record in every analyze report)

`rk audit --policy strict` on `spacedock_solver` runs does **not** yet walk the
solver's subagent JSONL (`agent/sessions/projects/*/*.jsonl`), so the audit verdict is
structurally incomplete for our runs. Surface this caveat in each analyze report rather
than treat the audit as airtight.

## 6. CLAUDE.md & AGENTS.md

### Three agent layers (these files target only the first)

| Layer | Who | Reads |
|-------|-----|-------|
| **Repo operator** | Claude Code *or* Codex CLI driving the loop | **CLAUDE.md / AGENTS.md** |
| **Orchestrator** | spacedock first-officer + ensigns (spawned by the operator) | `docs/ade-bench/README.md` |
| **Agent-under-test** | the codex solver (spawned by razorback/Harbor) | `…/<hyp>/solver_workflow/README.md` (the variable) |

### File strategy: one canonical body, no drift

- **`AGENTS.md`** = full operating guide (Codex reads it; also the source of truth,
  consistent with razorback's and spacedock's own `AGENTS.md`).
- **`CLAUDE.md`** = short Claude-Code preface that defers to `AGENTS.md`.

### `AGENTS.md` (canonical) — sections

1. **What autobench is** — auto-research repo: tune a spacedock solver-workflow README
   to push a benchmark score up; razorback runs the benchmark, spacedock orchestrates
   the loop. First target: ade-bench, codex runtime.
2. **Submodules** — `razorback/` (run benchmarks via `uv run rk …`; never edit),
   `spacedock/` (workflow framework + first-officer/ensign skills; never edit). Both
   read-only deps; update via `git submodule update`.
3. **Repo map** — `docs/ade-bench/`, `solver_workflows/ade-bench/{baseline,CHAMPION.md}`,
   `specs/ade-bench/`, `runs/` (gitignored).
4. **Running the loop** — seed a `concept` (the goal), then start
   `spacedock:first-officer` on `docs/ade-bench/`; the two paths (concept → `ideate`
   fan-out; hypothesis → `propose` → `smoke` → `full` → `analyze` → `conclude`); the
   two human gates (`propose` = leak-guard, `smoke → full` = money).
5. **🔒 The independent-variable rule** — *only* the solver README changes between
   hypotheses. Runtime (codex), model (gpt-5.5), sampling, spec shape, and `n_tasks`
   policy are held constant. Touching anything else confounds the result and must be
   declared as a separate hypothesis.
6. **🔒 Leak-guard discipline** — workspace data is the only authoritative source;
   forbidden-oracle list (§5.4); never relax the baseline's network/external-data ban;
   use `tools_denied`.
7. **🔒 Budget discipline** — `rk run --explain` ($0) first; smoke before full, always;
   `rk runs cost` pre-check; `--max-budget-usd-running` backstop; never exceed
   `max_budget_usd` — stop and report near the cap.
8. **🔒 Reproducibility discipline** — always `rk freeze`; pin the ade-bench dataset
   digest; frozen spec + README hash are immutable once smoke starts; copy
   `audit.json`/`score.json` into the hypothesis folder.
9. **The sandwich** — `rk run → rk audit --policy strict → rk score` per cell; record
   the spacedock_solver audit-coverage caveat (§5.6) in every analyze report.
10. **Champion promotion** — at `conclude`, a variant that beats `CHAMPION.md` (and
    passes audit) becomes the new champion; the next hypothesis forks from it.
11. **Conventions** — folder-form entities, ID style, commit discipline.

### `CLAUDE.md` (thin preface)

- **"Read `AGENTS.md` first — it is the operating guide; everything in it applies."**
- Claude-Code specifics: use the `spacedock:first-officer` skill to run/resume the
  loop; use superpowers `brainstorming` when standing up a *new* benchmark campaign;
  you are the **operator**, not the solver (the codex solver is spawned by razorback).

The four 🔒 sections are the load-bearing guardrails — what keep the auto-loop from
producing junk science or burning the budget.

## 7. Out of scope / future

- **Multi-benchmark.** Structure is namespaced (`docs/<benchmark>/`,
  `solver_workflows/<benchmark>/`, `specs/<benchmark>/`) so a second benchmark is a
  copy of the ade-bench setup. Not built now.
- **A/B-ing the runtime** (codex vs claude). Deliberately excluded — would confound the
  README as the sole independent variable.
- **Campaign-level auto-stop** (e.g. plateau detection that ends the campaign without a
  human). The human ends the campaign; per-hypothesis termination is automatic.

## 8. Values to fill in at implementation

- **ade-bench dataset digest** to pin in the spec templates. Reference example:
  `razorback/examples/specs/ade-bench-harbor-dataset-codex.yaml` (carries a
  `dbt-labs/ade-bench@sha256:…` ref).
- **`paper_baseline.value`** for ade-bench's `stratified_pass_at_1`.
- **`max_budget_usd`** caps for smoke and full.

## 9. Reusable assets (from the submodules)

| Asset | Path |
|-------|------|
| Experiment-workflow template (fork for `docs/ade-bench/README.md`) | `razorback/src/razorback/templates/experiment-workflow/README.md` |
| Codex ade/dbt-repair solver baseline (fork for `solver_workflows/ade-bench/baseline/`) | `razorback/examples/solver_workflows/codex-ade-dbt-repair/README.md` |
| Codex ade-bench smoke spec (model for `specs/ade-bench/smoke.yaml`) | `razorback/examples/specs/codex-ade-bench-smoke.yaml` |
| ade-bench Harbor dataset ref (digest to pin) | `razorback/examples/specs/ade-bench-harbor-dataset-codex.yaml` |
| Canonical sandwich driver | `razorback/examples/drivers/dab-paper-matrix.sh` |
| Leak-guard prose source | `razorback/packages/razorback-plugin-dab/src/razorback_plugin_dab/generate/workspace_readme.py` |
| Workflow orchestration | `spacedock/skills/first-officer/`, `spacedock/skills/commission/bin/status` |
