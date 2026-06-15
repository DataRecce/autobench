# DAB Autoresearch Pipeline — Design

**Date:** 2026-06-15
**Status:** Approved design — pre-implementation
**Author:** autoresearch operator (Kent)

## 1. Goal & shape

Adapt ADE-bench's autoresearch skeleton (`autobench/ade-bench/hypotheses/`) to drive
DataAgentBench (DAB) experiments through `rk run`.

Research question: **can forking the codex solver's workflow README move codex/gpt-5.5
past the Opus-4.8 incumbent on DAB's stratified Pass@1?**

Operating constraints:

- **Single run per experiment** (`trials: 1`). We judge flips by committed-artifact
  behavioral reads, not multi-trial CIs — carries over the ade-bench "single-trial,
  judge by artifact" standing decision.
- The operator drives `rk` and the spacedock workflow; the codex solver
  (`agent.kind: spacedock_solver`, `runtime: codex`) is spawned by razorback inside
  Harbor. The operator does not solve tasks.

## 2. Repo layout — `autobench/dab/`

```
dab/
├── docs/specs/                    # this design doc lives here
├── hypotheses/                    # NEW — the loop, mirrors ade-bench/hypotheses/
│   ├── README.md                  # workflow spec (frontmatter stages + stage docs)
│   ├── _gatekeeper/
│   │   └── propose-review-guideline.md   # DAB-adapted G-rules
│   ├── _artifacts/
│   │   ├── baseline.yaml          # @baseline pointer + per-dataset incumbent scores
│   │   ├── dataset-gap-ranking.md # 12-dataset stratified-Pass@1 gap ranking
│   │   ├── WORKFLOW-REFINE.md      # structural-refinement ledger
│   │   └── self-learning.md       # cumulative verdict takeaways
│   ├── _proposal/                 # pre-entity concepts / strategy memos
│   ├── _archive/                  # terminal entities (PASSED / REJECTED)
│   ├── concept-<slug>.md          # research directions (fan out to hypotheses)
│   └── dab0001-<slug>.md …        # hypothesis entities
├── specs/                         # existing — + per-hypothesis variant specs
│   ├── codex-dab-agnews.yaml      # existing example spec
│   ├── dab0001-<slug>.yaml        # variant full spec
│   ├── dab0001-<slug>.smoke.yaml  # variant smoke spec
│   └── *.frozen.yaml              # frozen pairs
├── solver_workflows/
│   ├── spacedock-readme-baseline/ # the @baseline solver README (codex)
│   └── dab0001-<slug>/            # forked variant READMEs (the single lever)
├── drivers/                       # NEW — ported rk-run-detached.sh + matrix.sh
└── runs/                          # rk run-dirs + .rk-handles/
```

## 3. Naming convention

To avoid collision with ade-bench's `h00NN` namespace, all numbered DAB entities use the
`dab` prefix:

| Thing | Pattern | Example |
|-------|---------|---------|
| Hypothesis entity file | `hypotheses/dab00NN-<slug>.md` | `hypotheses/dab0001-verify-reconcile.md` |
| Frontmatter id | `dab00NN` | `id: dab0001` |
| Variant solver dir | `solver_workflows/dab00NN-<slug>/` | `solver_workflows/dab0001-verify-reconcile/` |
| Variant full spec | `specs/dab00NN-<slug>.yaml` | `specs/dab0001-verify-reconcile.yaml` |
| Variant smoke spec | `specs/dab00NN-<slug>.smoke.yaml` | `specs/dab0001-verify-reconcile.smoke.yaml` |
| rk experiment name | `dab00NN-<slug>` | `experiment: dab0001-verify-reconcile` |
| Run-dir | `runs/dab00NN-<slug>/<job_hash>/` | `runs/dab0001-verify-reconcile/<hash>/` |

Concepts stay `concept-<slug>.md` (no number); the `dab` prefix is only for numbered
hypothesis/decision entities.

## 4. Entity & stage model — hybrid

ADE-bench's flat stage graph **plus** DAB dataset-gap targeting as a concept-selection input:

```
concept    → ideate → expanded [TERMINAL]
hypothesis → propose(🚦gate) → smoke(🚦gate) → full → analyze → conclude [TERMINAL]
                          ↘ hypothesis [revise] | conclude [REJECT clean]
```

- **Two human gates:** `propose` (leak-guard + gatekeeper + smoke-set table) and `smoke`
  (GO/NO-GO + behavioral deep-dive).
- **Dataset-targeting layer:** `_artifacts/dataset-gap-ranking.md` keeps the 12-dataset
  stratified-Pass@1 gap ranking derived from the Opus incumbent. Concepts/ideate use it to
  choose which dataset + queries a hypothesis targets. This is a lightweight *selection
  input*, not a full DAB lead→question tier.
- Each hypothesis = ONE README change, named target queries, falsifiable claim.

Hypothesis body sections (same order as ade-bench):
`## Hypothesis` · `## Pre-smoke Decision-Fork Probe` (flipped-task follow-ups only) ·
`## Acceptance criteria` · `## Gatekeeper review` · `## Smoke result` · `## Run result` ·
`## Behavioral analysis` · `## Failure Review` · `## Follow-up Routing` · `## Verdict`.

## 5. Solver & spec model — codex variants, README-fork lever

- Variant solver is held FIXED = **codex/gpt-5.5, `runtime: codex`** (reuse the existing
  `codex-dab-*` spec config).
- The single lever per hypothesis = fork `solver_workflows/spacedock-readme-baseline` →
  `solver_workflows/dab00NN-<slug>/`, edit its README (the three-stage
  model → analyze → verify methodology).
- Per hypothesis, two specs:
  - **Full spec** (`specs/dab00NN-<slug>.yaml`): differs from baseline ONLY in
    `experiment: dab00NN-<slug>` + `solver_workflow: ./solver_workflows/dab00NN-<slug>`.
  - **Smoke spec** (`specs/dab00NN-<slug>.smoke.yaml`): the full spec plus
    `benchmark.tasks: [<target query ids> + <canary query ids>]`.
- Both frozen via `rk freeze --allow-missing`. `trials: 1` (one trial per query),
  `concurrency.trials: 2` (two query-cells run in parallel for throughput). Note: the
  ade-bench `concurrency.trials: 1` constraint was a frozen-git-repo HEAD-lock race specific
  to that solver_workflow; DAB's per-query task materialization doesn't share that repo, so
  concurrency 2 is safe here.

## 6. Baseline — convert/shim the Opus run-dir

The chosen baseline `/home/kent/dataagentbench/_runs/spacedock-opus-4-8-xhigh-hint` predates
`rk` and lacks `per_trial_outcomes.json` / frozen spec / provenance, so `rk runs diff` and
`rk baseline promote` cannot consume it as-is.

- Write an adapter that reads the legacy run-dir and emits rk-format `manifest.json` +
  `summary.json` + `per_trial_outcomes.json` (one trial per query, each with
  `dataset` / `query_id` / `reward`), placed in an rk run-dir under `dab/runs/`.
- Register it as `@baseline`. **The razorback registry is a single global YAML
  (`~/.config/razorback/registry.yaml`) keyed only by `(kind, name)` — no project scoping —
  and the live ade-bench loop owns the global `@baseline`.** DAB therefore uses a project-local
  registry: `export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml` before
  any `rk registry` / `rk runs diff` / `rk baseline promote`. The committed `razorback-research.toml`
  is a documentary seed (the store reads YAML, not the toml); the live binding lives in the
  gitignored `razorback-registry.yaml`.
- **Acceptance:** `rk runs diff <baseline> <variant>` and `rk score <baseline>` run without
  error and report a stratified Pass@1 matching the legacy `summary.json`
  (~0.68 stratified).

## 7. Comparison & promotion — single reference (Opus incumbent)

- Every codex variant is diffed directly against the Opus `@baseline` via `rk runs diff`.
  A README change "works" if the codex full run beats the Opus incumbent on stratified
  Pass@1.
- **Accepted confound (documented):** the model swap (codex vs Opus) and the README lever
  are entangled — the raw delta contains both. The `analyze` stage MUST call this out and
  lean on the **behavioral / committed-artifact read** to attribute whether the *README
  change itself* moved the committed artifact, since the headline delta also carries the
  model difference. We are accepting this trade for simplicity; there is no codex anchor.
- **Promote** (`rk baseline promote <run-dir>` + `rk registry add run baseline`) when a
  variant's stratified Pass@1 clears the Opus incumbent on a clean `rk audit`.

## 8. Smoke targeting — dataset-select + per-query exclude

Verified in razorback code (`translate.py:312-317`, plugin path): the DAB plugin's
`benchmark.tasks` selector accepts **dataset names only** (passed to the plugin as
`--datasets`), but razorback applies `benchmark.exclude_tasks` **spec-side** as a verbatim
filter on the materialized per-query task directory names *after* the plugin runs. DAB task
dir names are `{dataset}-q{query_id}` (e.g. `agnews-q1`), set in
`razorback-plugin-dab/.../generate/prepare.py:158`.

So query-level smoke targeting is achieved with a **select-then-exclude** pattern in the
smoke spec:

```yaml
benchmark:
  kind: harbor
  dataset: dab@1.0
  plugin: dab
  plugin_args: { hints: true, data_root: /home/kent/dataagentbench/data }
  tasks: [agnews, googlelocal]        # whole datasets get materialized
  exclude_tasks: [agnews-q2, agnews-q4, googlelocal-q1, googlelocal-q3]  # drop unwanted queries
```

- **Target queries** = the queries the hypothesis claims to fix (kept).
- **Canary queries** = currently-passing queries from other datasets/families, kept as
  regression tripwires.
- Everything else in the selected datasets is dropped via `exclude_tasks`.
- **Caveat:** no existing test covers `exclude_tasks` + plugin together, so the propose stage
  MUST verify the resolved task list with `rk run <smoke-spec> --explain` before launching.
- **Smoke-set table (REQUIRED at every propose gate)** reuses ade-bench's boxed format:
  `Task` (`{dataset}-q{n}`) / `Baseline (Opus) reward` / `want-flip 🎯 or hold ✅` / `role`.
  Baseline rewards resolved from the converted `per_trial_outcomes.json`.

## 9. Gatekeeper — adapted G-rules

Carried over from ade-bench:

- single-idea / single-stage README diff
- leak-guard intact (no `curl`/`wget`/`git clone`/web fetch; no hidden oracle tokens)
- full spec differs from baseline in exactly two fields (`experiment` + `solver_workflow`)
- both specs frozen, `agent.kind: spacedock_solver` / `runtime: codex` preserved
- canary coverage on generative levers
- resolver fidelity (inserted README text matches the claim)

DAB-specific replacements for ade-specific rules:

- replace dbt test-count / `AUTO_*` token checks with **DAB validator + `ground_truth.csv`
  leakage guard** and a **`data/{ds}/db_description_withhint.txt` not leaked into README**
  check
- canary coverage expressed in DAB's **stratified-by-dataset** terms (canary queries drawn
  from non-target datasets)

Advisory only; the captain decides and records any override.

## 10. Detached runs & metric

- Port `drivers/rk-run-detached.sh` + handle polling (`runs/.rk-handles/`) from ade-bench.
  DAB runs are long (30 min–hours); launch detached, FO owns the wait by scanning
  `.rk-handles/*/` each turn (carries over the "rk run must be detached" discipline).
- **Auto-wakeup at ETA:** because the every-turn scan only fires on a turn, after launching a
  detached run the FO records the ETA and `ScheduleWakeup(min(eta_s, 3600))` with a first-officer
  continuation, re-checking the `done` sentinel on each wake (reschedule while running, ≤1 h
  granularity, ~9 h backstop → escalate). Makes the wait autonomous when the captain is away;
  requires driving the DAB FO under `/loop`. Full protocol in `hypotheses/README.md`
  → Repo conventions → "Auto-wakeup at ETA".
- **Metric = stratified Pass@1:** per-query pass@1 → per-dataset arithmetic mean →
  arithmetic mean of the 12 per-dataset scores (equal dataset weight, NOT micro-average).
  `rk score` already emits `stratified_pass_at_1`.

## 11. Build order

1. **Baseline shim** — adapter converts the legacy Opus run-dir to rk format; register as
   `@baseline`; verify `rk runs diff` + `rk score`.
2. **Spec pair + selector verification** — build one variant spec pair (`dab0001-*` full +
   smoke); validate the smoke spec's `tasks` + `exclude_tasks` resolves to exactly the
   intended per-query set with `rk run <smoke-spec> --explain` (dry, ~0 cost).
3. **Drivers** — port `rk-run-detached.sh` + `matrix.sh` into `dab/drivers/`.
4. **Workflow scaffolding** — author `hypotheses/README.md` (frontmatter stages + stage
   docs), `_gatekeeper/propose-review-guideline.md`, and `_artifacts/`
   (`baseline.yaml`, `dataset-gap-ranking.md` built from the converted baseline,
   `WORKFLOW-REFINE.md`, `self-learning.md`).
5. **Anchor run** — first codex full run on the baseline README (smoke-skipping anchor, like
   ade-bench's 9/48 anchor) to sanity-check the loop end-to-end; then open hypotheses.

## Open implementation risks

- **Per-query `tasks` selector** (§8) may not be supported by the DAB plugin — verified in
  build step 2 before authoring smoke specs.
- **Baseline shim fidelity** (§6) — the legacy `summary.json` aggregates at dataset level;
  the adapter must correctly explode per-query outcomes so the stratified score round-trips.
- **Model-swap confound** (§7) is accepted, not solved — analyze-stage discipline is the
  only mitigation.
