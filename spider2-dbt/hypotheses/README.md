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
      label: README + spec pass the leak-guard gate (auto-approve)
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

# Run spider2-dbt through razorback — autoresearch workflow

This workflow tunes the **solver-workflow README** (`../solver_workflows/<variant>/README.md`)
to push the **codex/gpt-5.5 solver's pass rate** on **spider2-dbt** — a hard text-to-dbt
benchmark that grades, per task, an **exact-named output table built into the project's DuckDB**
against a hidden gold (column-containment match, row order ignored). razorback runs and scores each
variant; this workflow ideates, gates, and analyzes.

The single lever per hypothesis is the codex solver's README. The variant solver is held FIXED at
**codex/gpt-5.5, `runtime: codex`, `reasoning_effort: xhigh`, `trials: 1`** — we are NOT swapping
models per hypothesis, only the README changes.

> **No model-swap confound (unlike DAB/ade-bench).** spider2-dbt's `@baseline` is *itself* a
> codex/gpt-5.5 run (the seed `spider2-dbt-baseline` output-contract solver — see *Champion*). Both
> the baseline and every variant run the identical model/runtime/sampling; the **solver README is
> the only variable.** So a paired `rk runs diff` delta is directly attributable to the README change
> — there is no entangled model swap to subtract. You STILL verify each verdict change by the
> committed artifact (did the README wording reach the model the solver actually built?), but you do
> not have to net out a model effect the way DAB does.

Two entity kinds share this directory:

- a **concept** (`spd<NNNN>-<slug>.md`, `kind: concept`) is a research direction; `ideate` fans it
  out into many hypotheses — *breadth*;
- a **hypothesis** (`spd<NNNN>-<slug>.md`, flat; folder form `spd<NNNN>-<slug>/index.md` allowed when
  evidence accumulates) is one testable README change, run end-to-end; `conclude` may file one
  failure-driven follow-up — *depth*.

Both birth mechanisms are prompt-driven: the acting ensign writes the new entity file.

## Repo conventions (full detail in the repo-root `AGENTS.md`)

- Run `rk` from `spider2-dbt/`: `uv run --project ../razorback rk <args>`.
- Always pass `--runs-dir runs`; prefer `rk run --explain` before a full run.
- Before any `rk run`, export `RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"`.
- **Before any `rk registry` / `rk runs diff` / `rk baseline promote`, export the spider2-dbt-local
  registry: `export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml`.**
  The razorback registry is a single GLOBAL YAML keyed only by `(kind, name)` with no project
  scoping, and the **live ade-bench loop owns the global `@baseline`** — a bare
  `rk registry … @baseline` would resolve/overwrite ade-bench's (and DAB keeps its own local file for
  the same reason). The spider2-dbt-local registry file keeps this benchmark's `@baseline` separate.
  `rk run` itself does not touch the registry, so the export is only needed for the
  registry/diff/promote calls.
- **The tasks are materialized LOCALLY, not downloaded.** `benchmark.kind: harbor-local`,
  `tasks_root: /home/kent/autobench/spider2-dbt/_views`. The `spider2-dbt@1.0` harbor download is
  PKG-40-blocked, so `tools/package_spider2_dbt_views.py` builds leak-clean per-task views (source
  DuckDB + hidden gold) from the local `/home/kent/Spider2/spider2-dbt` checkout. `_views/` is
  gitignored — regenerate with the packager, never source it. The packager is the benchmark's main
  infra-fragility surface (see *Packaging / preflight health* below).
- **`rk run … --runs-dir` is long-running (30 min–8 hr+ for a full 61-task run) and far exceeds the
  Bash-tool timeout — never run it in the foreground.** Launch it through
  `drivers/rk-run-detached.sh <key> <spec> [run|matrix]`, which `nohup`s the run, writes a handle
  under `runs/.rk-handles/<key>-<ts>/` (`pid` · `log` · atomic `done` sentinel with
  `rc`/`end`/`rundir`), and fires an **ntfy** push on completion (topic in `.ntfy-topic`). The
  **ensign launches and returns the handle immediately — it never waits**; the **FO owns the wait by
  scanning `runs/.rk-handles/*/` at the top of every turn** (4-state model + harbor-output crash
  check + backstop — full contract in the repo-root `AGENTS.md` → *Detached runs*). No live poller /
  no `Monitor`. The fast `--explain` / `rk audit` / `rk score` calls stay foreground, after the
  sentinel lands. See the `smoke`/`full` stages for the exact call.
- **Auto-wakeup at ETA (run the FO under `/loop`).** The every-turn handle scan only fires when there
  *is* a turn — so when the captain is away, the FO must wake *itself* at the run's ETA instead of
  stalling. Immediately after launching a detached `smoke`/`full` run:
  1. Record the ETA in seconds (`eta_s` = surviving task-cells × ~per-task minutes; a smoke task runs
     ~6 min, the full 61-task run is multi-hour).
  2. `ScheduleWakeup(delaySeconds = min(eta_s, 3600), reason = "spider2-dbt <key>: check detached run",
     prompt = <the /loop first-officer continuation>)`. Wakeups clamp to ≤1 h, so a multi-hour run
     wakes at most hourly and re-checks — intended (cheap sentinel poll, catches early finishes too).
  3. On every wake, scan `runs/.rk-handles/<key>-*/done`: present `rc=0` → foreground audit/score +
     deep-dive; present `rc≠0` → read `log`, open `## Failure Review`; absent → re-`ScheduleWakeup`
     (`min(remaining_to_eta, 3600)` before ETA, else ~600 s), post a one-line "still running", end the
     turn.
  4. Stop rescheduling once `done` is consumed, or hit the ~9 h backstop → escalate to the captain.
  Needs a wake-capable context — drive the FO under `/loop` (dynamic, self-paced); outside `/loop` the
  FO falls back to ntfy + the next operator turn.
- The independent variable is ONLY the solver README. A variant full spec differs from
  `specs/full-baseline.frozen.yaml` only in `experiment:` + `agent.solver_workflow:`. `trials: 1`
  always (`concurrency.trials: 4` for the full run, `2` for smoke — spider2-dbt tasks each get an
  isolated task-dir / DuckDB, so there is no shared-state race).

## File Naming

- Concepts and hypotheses share one `spd<NNNN>` id space. Concepts: `spd<NNNN>-<slug>.md`,
  `kind: concept`, `id: spd<NNNN>` (e.g. `spd0003-value-level-semantics.md`). The `spd<NNNN>` a
  concept consumes is not reused when `ideate` fans it into hypotheses.
- Hypotheses: `spd<NNNN>-<slug>.md`, next available `spd<NNNN>` (scan existing `spd*-*.md` and
  `_archive/`, then increment — `status --next-id` is n/a under slug style). **Set `id: spd<NNNN>`**
  (the short prefix, e.g. `id: spd0002`) in frontmatter so the entity resolves by its short id
  (`spacedock status --resolve spd0002`). The slug stays the identity (the status ID column renders
  the full `spd<NNNN>-<slug>`); the descriptive name also lives in `title`. The `spd` prefix avoids
  collision with ade-bench's `h00NN` and DAB's `dab<NNNN>` namespaces.

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Every entity (concept or hypothesis) sets the short `spd<NNNN>` prefix (e.g. `spd0001`) — resolvable via `status --resolve`. Slug stays the identity. |
| `title` | string | Human-readable name. |
| `status` | enum | concept, ideate, expanded, hypothesis, propose, smoke, full, analyze, conclude. |
| `kind` | enum | `concept` or `hypothesis` (which path this entity is on). |
| `source` | string | Where it came from (concept fan-out, prior verdict, captain hunch, smoke deep-dive). |
| `started` / `completed` | ISO 8601 | When work began / reached a terminal stage. |
| `verdict` | enum | PASSED or REJECTED — set at a terminal stage. |
| `score` | number | Priority 0.0–1.0 (optional); higher = ideate/advance sooner. See `_artifacts/task-gap-ranking.md`. |
| `worktree` | string | Empty (this workflow runs inline; the solver runs inside Harbor task containers). |

## The metric (read this before reasoning about gains/regressions)

spider2-dbt has **no per-dataset stratification**. Every task is one query under a single `default`
stratum, so `rk score`'s **`stratified_pass_at_1` is just the flat pass rate** = (tasks passing) /
(tasks scored). The full board is **61 duckdb-runnable tasks** (68 declared − 4 goldless
[airbnb002 / biketheft001 / gitcoin001 / google_ads001] − 3 postgres-backed
[inzight001 / shopify001 / shopify002]).

Consequences that differ from DAB's stratified metric:

- **A regression on ANY currently-passing task lowers the score directly** (no per-dataset mean to
  dilute it). One passer broken = −1/61 ≈ −0.016. **A canary dropping FAIL is a NO-GO regardless of
  how many targets flipped.**
- **A "canary / sentinel" is simply a currently-passing task** the lever must not break. There is no
  multi-draw band yet (`trials: 1`); judge a flip by the **committed artifact** (the built table
  reached gold), not by a single reward, and judge a regression by the **artifact damage** (the lever
  changed what the solver built on a passer). A 6-draw band may be built later into
  `_artifacts/baseline-variance.md`.
- Goldless and postgres-backed tasks are **known non-signal** — never count them as regressions; they
  are excluded from the 61 by the full spec's task list.

## Autonomous run policy (auto-approve propose gate + escalation)

This workflow runs the **propose gate AUTO-APPROVE by default** (the gatekeeper is advisory and the
gate self-advances on a clean recommendation — see below). The expensive `smoke → full` step stays
behind a hard guardrail, and `analyze → conclude` / promote are NEVER automated. Driving the FO under
`/loop` lets the auto-gate and the detached-run waits resolve without a captain turn.

Scope boundary:

| step | autonomous? |
|---|---|
| frontmatter transitions, dispatch, detached launch, sentinel wait, audit, score | YES — mechanical spine |
| `propose` gate | **AUTO-APPROVE** on the criteria below, else HALT |
| `smoke → full` | AUTO-ADVANCE on the guardrail below, else HALT |
| `full` run launch + `analyze` data-gathering | YES |
| `analyze → conclude`, promote, seed-README edit | NEVER — always escalate to the captain |
| which lever / retarget / pivot after a dead family / revise-vs-reject | NEVER — strategy is human |
| packager / infra **code** fixes (e.g. a schema-align bug) | NEVER auto — HALT + escalate |

### `propose` auto-gate (AUTO-APPROVE — the gatekeeper is auto-approve)
The propose gatekeeper is **auto-approve**: the gatekeeper subagent still runs and records its
PASS/WARN/FAIL table + recommendation into the entity, and the FO still runs the reject-checks, but on
a clean result the gate **advances to `smoke` automatically without waiting for the captain**.
Auto-APPROVE (advance to `smoke`) iff BOTH hold; otherwise HALT and present the gate:
1. the gatekeeper recommendation is **APPROVE** (a single FAIL → HALT); AND
2. the FO reject-condition checks are clean — one-knob README diff, leak-guard byte-intact, full-spec
   diff = only `experiment:` + `agent.solver_workflow:`, `agent.kind: spacedock_solver` /
   `runtime: codex`.

A gatekeeper **REVISE/REJECT** or any failed reject-check HALTS (never auto-revise a leak/spec fault).
The gate still records the smoke-set table into the entity so the captain can audit the auto-approval
after the fact.

### `smoke → full` auto-advance guardrail
The full run is the expensive, infra-fragile step, and a smoke GO can be a **false positive**
(variance or packaging) — so auto-advance only behind a HARD guardrail. Advance to `full` iff ALL
hold; else HALT:
1. **strict audit clean, `0 coverage_missing`, `0 tainted`** — no task errored, no infra taint;
2. **target flipped by the COMMITTED ARTIFACT**, not merely `reward=1.0` — the built table reached
   gold because the README change steered it there (deep-dive below);
3. **canaries held** — no currently-passing task dropped FAIL; the artifacts the lever touched on
   passers are intact;
4. **packaging / preflight health confirmed** at smoke launch — no build-time preflight failure
   (`razorback_spider2_preflight.py … exit 2`), no source-schema-align crash, no missing-view; an
   error behind a packaging fault is not a result (see *Packaging / preflight health*);
5. **the target is a LOW-BASELINE (currently-FAIL) task.** A pass on a task that already passes at
   `@baseline` is **not** evidence the lever did anything; auto-mode must NOT advance on it or count
   it.

### HALT-and-escalate triggers (surface to the captain; do not auto-advance)
- gatekeeper REVISE/REJECT, or a failed `propose` reject-check;
- smoke **NO-GO**, a **canary regression**, or a GO that fails the `smoke → full` guardrail (incl. the
  already-passing-target trap);
- **any infra anomaly**: detached run `rc≠0`, audit `coverage_missing > 0` or taint, a build-time
  **preflight failure**, a packager **source-schema-align** crash, a missing materialized view, or a
  stale job-dir lock (`FileExistsError … lock.json`). **Infra is NEVER a result** — report it, never
  count it as a regression.
- an UNEXPECTED `full`/`analyze` result — follow `_artifacts/unexpected-result-playbook.md`; do not
  verdict on the headline number.

### What stays human even in autonomous mode
Strategy and honesty: which lever to run, the retarget, the pivot after a dead family,
revise-vs-reject, the attribution downgrade of a lucky pass, and the promote/conclude verdict.
Auto-mode automates the *waiting and the clean cases* (and now the propose gate) and surfaces every
off-happy-path moment — which is where the real work of a run lives.

## Stages

### `concept`  *(initial — concept path)*

A research direction is filed (by you or the first officer): a plain-English theme + rationale.

- **Inputs:** a research lead, a prior verdict's follow-ups, a captain hunch, or the
  `_artifacts/task-gap-ranking.md` table (which tasks have the most headroom — currently-FAIL tasks
  whose failure mode looks README-addressable).
- **Outputs:** a `spd<NNNN>-<slug>.md` (`kind: concept`) body stating the direction and why it might
  raise the pass rate.
- **Good:** a concrete, testable direction tied to an observed failure mode on a currently-failing
  task (e.g. "ephemeral-materialization misses", "value-level grain/column semantics").
- **Bad:** vague "make it better"; a direction with no hypothesis to derive from it.

### `ideate`

An ensign reads the concept + the current `@baseline` solver README + prior learnings + the
task-gap ranking, and **writes several `spd<NNNN>-<slug>.md` hypothesis entities** (status
`hypothesis`), each naming the specific solver-README change it will make and its target task(s).
Then the concept advances to `expanded`.

- **Inputs:** the concept body; the current `@baseline` solver README (seed:
  `../solver_workflows/spider2-dbt-baseline/README.md`); `_artifacts/task-gap-ranking.md`; the latest
  analyze/smoke findings.
- **Outputs:** 2–5 new hypothesis entities, each with a falsifiable claim + acceptance criteria; the
  concept marked `expanded`.
- **Good:** each hypothesis changes ONE idea, is falsifiable, and names its target task(s).
- **Bad:** one mega-hypothesis; hypotheses that restate the concept without a concrete README change.

### `expanded`  *(terminal — concept path)*

The concept has been turned into hypotheses; archived.

### `hypothesis`  *(initial — hypothesis path)*

A fully-formed, queued hypothesis. Auto-advances to `propose`.

- **Inputs:** an `ideate` fan-out or a `conclude` follow-up.
- **Outputs:** the body's `## Hypothesis` (the claim + the single README change + named target tasks)
  and `## Acceptance criteria` (the verdict, e.g. "the paired delta vs `@baseline` clears the
  tripwire on the pass rate, attributed by the committed artifact").
- **Flipped-task follow-up requirement.** If the hypothesis comes from a smoke/full rejection on a
  flipped or high-variance task, include `## Pre-smoke Decision-Fork Probe` before propose. It must
  name the local fork being tested, the exact prompt context used, the control A result, the proposed
  B/C result, the exact README wording tested, the artifact signature expected in a real run, and the
  caveat that this is proxy evidence only. If no probe was run, state why (infra fix, no local fork,
  oracle-blocked).
- **Good:** falsifiable; names the target tasks for smoke.
- **Bad:** success criteria invented after seeing results.

### `propose`  *(🚦 leak-guard gate — AUTO-APPROVE)*

The ensign authors the variant, then a gatekeeper subagent pre-reviews it and records an advisory
recommendation in the hypothesis file. **The gate auto-approves on a clean gatekeeper APPROVE + clean
reject-checks** (see *Autonomous run policy → propose auto-gate*); any FAIL / REVISE / REJECT / failed
check HALTS for the captain.

- **Inputs:** the hypothesis claim.
- **Outputs:**
  1. `cp -r ../solver_workflows/spider2-dbt-baseline ../solver_workflows/spd<NNNN>-<slug>` (fork the
     current `@baseline` solver dir — `spider2-dbt-baseline` is the seed baseline), then edit its
     `README.md` — the one variable.
  2. `cp specs/full-baseline.yaml specs/spd<NNNN>-<slug>.yaml`, set `experiment:` to
     `spider2-dbt-spd<NNNN>-<slug>` and `agent.solver_workflow:` to
     `./solver_workflows/spd<NNNN>-<slug>`. This is the FULL spec — all 61 tasks, no subset.
  3. Make the smoke spec: `cp specs/spd<NNNN>-<slug>.yaml specs/spd<NNNN>-<slug>.smoke.yaml` and
     replace `benchmark.tasks:` with the smoke subset — the targets + sentinels/canaries (the
     `spider2-dbt-<task>` ids). spider2-dbt tasks are one-query each, so the smoke set is just a
     **subset of the `tasks:` list** — there is no `exclude_tasks` machinery. **If the instruction is
     generative** (fires on every task, not gated on a precondition that limits it to the targets),
     the smoke set MUST also carry a **regression panel**: ≥2 currently-PASSING tasks the lever can
     actually fire on (perturbable sentinels), drawn from a task family OTHER than the targets'. The
     standing 6-task smoke set (tpch001 / activity001 / xero_new001 / chinook001 / jira001 / f1001)
     already pairs two passers (activity001, f1001) with four currently-failing targets — extend it
     when a lever's blast radius points elsewhere.
  4. Freeze both:
     `uv run --project ../razorback rk freeze --allow-missing specs/spd<NNNN>-<slug>.yaml` and
     `uv run --project ../razorback rk freeze --allow-missing specs/spd<NNNN>-<slug>.smoke.yaml`.
  5. **Verify the smoke selection:**
     `uv run --project ../razorback rk run specs/spd<NNNN>-<slug>.smoke.frozen.yaml --explain` and
     confirm the surviving task list is exactly targets + sentinels (no extra, none missing). $0,
     foreground.
  6. **Run the gatekeeper.** Dispatch a review subagent that applies
     `_gatekeeper/propose-review-guideline.md` to the variant artifacts (the forked solver README
     diff vs its parent, the two spec diffs, the frozen files, and the hypothesis body) and writes a
     `## Gatekeeper review` block into the hypothesis file: a per-rule PASS/WARN/FAIL table plus an
     overall **APPROVE / REVISE / REJECT** recommendation with a one-line rationale. Advisory — it
     informs the auto-gate, it is not the gate.
- **Gate record (REQUIRED — every propose gate, even on auto-approve).** Record the smoke set as a
  table so the captain can audit coverage after the auto-approval. Resolve each task's `@baseline`
  reward first (`export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml`,
  then `rk registry resolve run @baseline`, then read the resolved run's `per_trial_outcomes.json`),
  and write a **boxed table** with columns — `Task` (`spider2-dbt-<task>`) / `Baseline` / `Should pass
  in smoke?` / `Role / why we picked it` — using the glyphs `❌ FAIL`, `✅ PASS`,
  `🎯 want it to flip to PASS`, `✅ must stay PASS`:

  ```
  ┌───────────────────────┬──────────┬─────────────────────┬─────────────────────────────────────────────┐
  │         Task          │ Baseline │ Should pass in smoke?│             Role / why we picked it          │
  ├───────────────────────┼──────────┼─────────────────────┼─────────────────────────────────────────────┤
  │ spider2-dbt-<task>    │ ❌ FAIL  │ 🎯 want it to flip  │ Target — the failure this lever should flip. │
  │ spider2-dbt-<task>    │ ✅ PASS  │ ✅ must stay PASS   │ Sentinel — known passer; breaks ⇒ side effs. │
  │ spider2-dbt-<task>    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (other family) — regression tripwire. │
  └───────────────────────┴──────────┴─────────────────────┴─────────────────────────────────────────────┘
  ```

  One row per surviving smoke task. State the net you're hoping for (e.g. "flip ≥1 of N targets, lose
  zero sentinels/canaries"). The run is detached (nohup); give an ETA based on the number of surviving
  task-cells (~6 min/task). Lead with this table + a plain-words brief of the lever; keep the full
  spec/diff detail in the hypothesis file. For a generative lever, the table makes the regression
  panel auditable at a glance.
- **Gatekeeper (advisory pre-review):** its recommendation drives the auto-gate. A rule it marks FAIL
  HALTS for the captain; tune the bar by asking an agent to update
  `_gatekeeper/propose-review-guideline.md` on demand (it is not auto-updated; the gatekeeper re-reads
  it fresh each run). For flipped-task follow-ups, the gatekeeper also reviews the
  `## Pre-smoke Decision-Fork Probe` block for proxy quality: no hidden-gold leakage, solver-visible
  context only, exact README wording, a control variant, and no pass-rate claim from subagent counts.
- **Gate — HALT (do not auto-approve) if:** the README leaks ground truth (its no-external-reference /
  leak-guard prose is removed or weakened, OR it reads/pastes any hidden gold — the gold table name,
  its columns, or `*_gold*` contents — into the README); the FULL spec differs from the anchor in
  anything other than `experiment:` + `agent.solver_workflow:` (the smoke spec additionally narrows
  `benchmark.tasks`); `agent.kind` ≠ `spacedock_solver` or `runtime` ≠ `codex`.
- **Good:** exactly one README idea changed; leak-guard intact; `diff` of the two specs shows only the
  allowed fields; gatekeeper recommendation recorded; the smoke-set table presented with baseline
  rewards resolved; the surviving smoke set confirmed via `--explain`.
- **Bad:** multiple knobs changed; leak-guard relaxed; auto-approving past a gatekeeper FAIL; recording
  no smoke-set table.
- **Autonomous mode:** AUTO-APPROVE iff the gatekeeper recommends APPROVE *and* the reject-checks are
  clean (see *Autonomous run policy*); any FAIL / REVISE / REJECT / failed check HALTS for the captain.

### `smoke`  *(🚦 go/no-go gate)*

A focused pre-flight on the hypothesis's **target tasks** via the smoke spec (its narrowed
`benchmark.tasks`). **You review before committing the full run.** *(Budget caps deferred — this is a
worthiness gate.)*

- **Inputs:** the frozen smoke spec `specs/spd<NNNN>-<slug>.smoke.frozen.yaml`.
- **Smoke-set composition.** Targets + ≥1 stable-pass sentinel. **If the instruction is generative**
  (fires on every task, not gated on a precondition), the smoke set MUST also include a **regression
  panel** — ≥2 currently-PASSING tasks the lever can actually fire on, from a family OTHER than the
  targets'. A generative change can regress *anywhere it fires*, and a targets-only smoke is
  structurally blind to that. Because the metric is a flat pass rate, a regression on any passer lowers
  the score even while the target flips. **A canary dropping FAIL is a NO-GO regardless of how many
  targets flipped.** A lone flip may be variance (`trials: 1`, gpt-5.5 is not deterministic) — bank a
  GO on a flip you can prove reached the committed artifact (the deep-dive below) plus held canaries,
  not on a single unexplained flip.
- **Outputs (from `spider2-dbt/`):**
  ```bash
  uv run --project ../razorback rk run specs/spd<NNNN>-<slug>.smoke.frozen.yaml --explain   # $0, fast, foreground
  # rk run is long (30 min–8 hr+) >> Bash-tool timeout — launch DETACHED via the audited launcher (nohup)
  # (ensign launches, returns the handle, exits; FO scans runs/.rk-handles/*/ every turn):
  drivers/rk-run-detached.sh spd<NNNN>-smoke specs/spd<NNNN>-<slug>.smoke.frozen.yaml run
  #   -> handle: runs/.rk-handles/spd<NNNN>-smoke-<ts>/  (pid · log · done = rc/end/rundir) + ntfy on done
  # THEN ScheduleWakeup(min(eta_s,3600)) to auto-check the sentinel at the ETA — see Repo conventions.
  # When `done` appears with rc=0 (or harbor output confirms — see AGENTS "Detached runs"), THEN:
  uv run --project ../razorback rk audit <run-dir> --policy strict
  uv run --project ../razorback rk score <run-dir>
  ```
  Capture the focused score + clean-audit attestation in `## Smoke result`.
- **Post-run deep-dive (REQUIRED every smoke — whether GO or NO-GO).** Do not stop at the score. For
  each target task, compare the smoke cell against the same task in `@baseline`
  (`export RAZORBACK_REGISTRY=…`, then `rk registry resolve run @baseline`):
  1. **Verdict delta** — did it flip FAIL→PASS, or not? Did the sentinel hold?
  2. **Distance-to-pass** — read the cell's `validation.json` / `reward.json` (and the
     spider2-dbt verifier stdout: which gold table was missing, or which columns/values mismatched).
     **Unchanged verifier result ⇒ the lever was inert on that cell** — a cheap check before reading
     any transcript.
  3. **Behavioral why** — for at least one flipped (if any) and one still-failing target, read the
     cell transcripts (the codex `agent/` transcript + the ensign session jsonl) and extract the
     **final committed artifact** (the dbt model SQL + the built table the solver actually
     materialized). Classify each: *flipped because the change reached the committed model* / *inert —
     change only discussed, not implemented* / *closer but still failing (right table name, wrong
     columns/grain/values)* / *instruction inapplicable*. Acknowledging an instruction in reasoning is
     NOT evidence — verify the artifact (the built table in the output DuckDB).
  Write the full per-task detail (a flip/distance/why table + the behavioral read) into
  `## Smoke result` and `## Behavioral analysis`.
- **Failure review loop (REQUIRED for every NO-GO, canary regression, or revise).** Before routing
  `smoke → hypothesis` or `smoke → conclude`, append a `## Failure Review` block. Classify the failure
  as exactly one primary type: `infrastructure-failure` / `diagnosis-miss` / `wrong-table-name` /
  `ephemeral-not-materialized` / `wrong-columns-or-grain` / `correct-artifact-still-fail` /
  `canary-bleed` / `variance-unclear`. Then answer:
  1. What was the original hypothesized fork?
  2. What fork did the committed artifact actually reveal?
  3. Did the README rule fire, and where is the artifact evidence?
  4. What new fork or failure mechanism should be tested next?
  5. Is the next step `stop`, `probe`, `file`, or `escalate`?
  Infrastructure / packaging failures are not experiment evidence; recover or relaunch before drawing
  behavioral conclusions.
- **Workflow-refinement evaluation (AUTOMATIC — do this without being asked).** If the hypothesis's
  lever is a change to the solver workflow's **structure** — a new stage, a removed/reordered/replaced
  stage, or a new protocol/protocol-family (tell-tale: a `## Protocol-family declaration` section, or
  a `## Hypothesis` framed around "a NEW stage" rather than a rule tweak *inside* an existing stage) —
  then the deep-dive is NOT done at the per-task flip. Also evaluate the workflow change itself:
  1. **Was the stage/protocol exercised?** Across the whole smoke set, did the new/changed stage fire
     and produce its declared artifact? Where was it inert?
  2. **Effect of the structural change** — independent of whether the target flipped: did it change the
     committed models / solver behavior — help, harm, or nothing?
  3. **Record it** — append/refresh an entry in `_artifacts/WORKFLOW-REFINE.md` (layer / refinement
     type / finding / **learning** / bears-on / evidence). Mandatory and automatic — part of the smoke
     commit.
  The go/no-go then covers BOTH axes: the task-level result *and* the workflow-level learning.
- **Report to the captain in plain language.** The entity gets the full detail; the captain gets a
  SIMPLE-WORDS on-screen summary at the gate — what flipped, did we get closer, and (if NO-GO) why —
  not the raw tables. Lead with the go/no-go and the one-line reason.
- **Gate:** worthwhile (the change moved the targeted tasks, or at least did not regress them) →
  `full`; flawed but revisable → back to `hypothesis`; cleanly falsified (0 flips, lever inert) →
  `conclude` (REJECTED), recording the deep-dive as the evidence. A `smoke → hypothesis` revision
  requires a `## Failure Review` block with a newly defined fork and a decision about whether subagent
  probing is needed before another smoke.
- **Good:** smoke exercises the changed behavior; audit clean before the score is trusted; every NO-GO
  carries a behavioral *why* backed by the committed artifact.
- **Bad:** advancing on a smoke that never exercised the change; scoring without a clean audit;
  reporting a NO-GO as just a number; burying the captain in raw detail.
- **Autonomous mode:** auto-advance `smoke → full` only behind the hard guardrail in *Autonomous run
  policy* (audit clean + `0 coverage_missing`, target flipped by committed artifact, canaries held,
  packaging healthy, **currently-FAIL target**); a NO-GO, canary regression, infra anomaly, or
  low-confidence GO HALTS for the captain.

> **Anchor / first run skips `smoke`** (`propose → full`): the first full run on the seed
> `spider2-dbt-baseline` README (all 61 tasks) is a direct full run that **establishes `@baseline`**
> and validates the loop end-to-end; subsequent hypotheses go through `smoke`.

### `full`

The full run on the FULL frozen spec (`spd<NNNN>-<slug>.frozen.yaml`, all 61 duckdb-runnable tasks, no
subset).

- **Outputs (from `spider2-dbt/`):**
  ```bash
  # rk run is long (multi-hour for 61 tasks) >> Bash-tool timeout — launch DETACHED via the launcher (nohup):
  drivers/rk-run-detached.sh spd<NNNN>-full specs/spd<NNNN>-<slug>.frozen.yaml run   # all 61 tasks
  #   -> handle: runs/.rk-handles/spd<NNNN>-full-<ts>/  (pid · log · done = rc/end/rundir) + ntfy on done
  # THEN ScheduleWakeup(min(eta_s,3600)) to auto-check the sentinel at the ETA.
  # When `done` appears with rc=0 (or harbor output confirms), THEN:
  uv run --project ../razorback rk audit <run-dir> --policy strict
  uv run --project ../razorback rk score <run-dir> --format json
  ```
  (Or run the full per-cell pipeline detached with `matrix` mode if `drivers/matrix.sh` is present.)
  Record the run-dir path + headline in `## Run result`.
- **Good:** the full spec uses the SAME solver README as the smoke spec (only the task set differs);
  audit clean before the score is recorded.
- **Bad:** methodology drift between smoke and full.

### `analyze`

Interpret the full run against `@baseline` — quantitatively and behaviorally.

> **When the result is UNEXPECTED** (a smoke GO that didn't translate, a flip that didn't reproduce, an
> unexpected regression, a score below `@baseline`), follow the fixed diagnostic ladder in
> `_artifacts/unexpected-result-playbook.md` before routing. Do not promote/reject/revise on the
> headline number alone.

- **Quantitative (from `spider2-dbt/`):**
  ```bash
  export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml
  uv run --project ../razorback rk score <variant-run-dir> --format json   # absolute pass rate vs @baseline
  # rk runs diff CRASHES on these run-dirs (query_id is null — single "default" stratum, same as
  # ade-bench/DAB): TypeError on the null query_id. So compute the PAIRED delta from
  # per_trial_outcomes.json instead — slug-pair each task's reward (variant vs @baseline) and
  # bootstrap (10k) the paired difference. (See memory: rk-runs-diff-query-id-null.)
  ```
  Paste the absolute pass rate + the paired delta (bootstrap CI) into `## Run result`.
- **Attribution (no model-swap confound — but still verify the artifact).** Because `@baseline` and the
  variant are the SAME codex/gpt-5.5 solver, the paired delta is directly attributable to the README —
  there is no model effect to net out. BUT a delta is only *lever* evidence if the README wording
  actually reached the committed model: for each verdict-changed task, read the committed artifact (the
  dbt model SQL + the built table) and confirm the README rule is *why* it changed. A delta with no
  artifact-level read is not evidence the lever worked (it could be `trials: 1` variance).
- **Behavioral (per task whose verdict changed vs `@baseline`, plus a sample of persistent failures)
  — read the cell `runs/<experiment>/<hash>/spider2-dbt-<task>__<short>/`:**
  - `result.json` + the per-task reward (`reward.json` / `validation.json`) → binary verdict.
  - the spider2-dbt verifier output → **distance to pass**: missing gold table name, or which
    columns/values mismatched (column-containment), or grain off.
  - the codex `agent/` transcript → the main agent plan, dbt model edits, `dbt build`, self-validation.
  - the ensign session jsonl → the sub-agent transcripts.
  Write a `## Behavioral analysis` block answering, per task: (1) **method adherence** — did the agent
  execute the README's prescribed method? (2) why it works; (3) why it fails (the per-task distance to
  pass from the verifier).
- **Required questions every analyze report MUST answer** (in `## Run result` / `## Behavioral
  analysis`):
  1. **Net + full per-task ledger** — absolute pass rate vs `@baseline` and paired delta + CI; AND
     *every* task that changed verdict in *both* directions (FAIL→PASS gains **and** PASS→FAIL
     regressions), each with its mechanism. Never report only the gains.
  2. **Smoke vs full** — if smoke was a GO, why did the full verdict differ? Name exactly what the smoke
     set could not see (e.g. regressions on tasks/families it didn't sample).
  3. **Already-correct-and-broken** — for each regression, was the task *passing* at `@baseline`? Call
     out damage to working answers explicitly; distinguish "failed to help" from "broke a passer."
  4. **Was the change executed?** — for representative gains and regressions, did the *committed
     artifact* (the built table) actually change because of the README wording? Classify:
     executed-and-helped / executed-and-hurt / inert (discussed-not-done) / premise-falsified (followed
     but target not local) / variance (single-trial flip not reproducible by artifact). Verify the
     artifact, not the chatter.
  5. **Prevention + next move** — concrete and actionable: how to keep the gains without the harm
     (scoping guardrails), how to catch it earlier (smoke canaries), and the recommended next step (do
     NOT reflexively file if the lever family is exhausted — escalate).
  6. **Smoke-vs-full fork drift** — if a smoke GO later fails/regresses at full, identify whether the
     smoke result was artifact-real or single-trial variance; name the fork that changed at full; state
     whether the smoke panel missed a family, the rule drifted into a different branch, or the failure
     is unrelated variance. Feeds the `## Failure Review` / follow-up routing.
- **Report to the captain in plain language.** Full detail (tables, CIs, SQL) in the entity; a
  SIMPLE-WORDS on-screen summary — net result, what flipped each way, why, and the recommendation. Lead
  with the headline; never make the captain read raw tables to learn the verdict.
- **Good:** verdict cites the paired delta + CI; behavioral findings name specific failure mechanisms
  AND confirm the README lever reached the committed artifact; all required questions answered;
  regressions named as damage to passers; captain gets a plain-words summary.
- **Bad:** reading a within-CI wobble as a win; a score with no behavioral read; crediting a flip to the
  README without artifact-level confirmation; reporting only the gains; a report the captain must
  interrogate.

### `conclude`  *(terminal — hypothesis path)*

- **Promote if** the variant's pass rate clears `@baseline` and the paired delta clears the tripwire
  (bootstrap CI excludes a regression) on a clean audit:
  ```bash
  export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml
  uv run --project ../razorback rk baseline promote <variant-run-dir>
  uv run --project ../razorback rk registry add run baseline <variant-run-dir>
  ```
  (updates `@baseline` in the spider2-dbt-local `razorback-registry.yaml`). Then update
  `_artifacts/baseline.yaml` and re-derive `_artifacts/task-gap-ranking.md` from the new champion's
  `summary.json`.
- **Record the learnings in the entity file — not only in operator memory.** The entity is the
  portable, cross-machine experiment record. Write the distilled lessons into `## Behavioral analysis`
  and `## Verdict`: the failure mechanism, whether the change reached the committed artifact, the
  distance-to-pass deltas, and any transferable rule (what kind of lever lands vs is inert). Append a
  one-line entry to `_artifacts/self-learning.md`. Memory is a convenience mirror; the entity body is
  the source of truth.
- **Finalize the workflow-refinement finding (AUTOMATIC for any workflow-structural hypothesis).** If
  this hypothesis changed the solver workflow's structure, its entry in `_artifacts/WORKFLOW-REFINE.md`
  MUST reach a final state before archive: set its status to the verdict (adopted / rejected-as-written
  / open-with-next-step), sharpen its **learning** line, and list the sibling hypotheses it steers in
  **bears-on**. Do this whether `conclude` was reached from `smoke` (REJECTED) or after a full
  `analyze`.
- **Derive new hypotheses from the deep-dive findings.** Turn the smoke/analyze behavioral read into
  concrete next bets (each ONE README change, falsifiable, with named target tasks). **But do not
  reflexively file when the evidence says the lever family is exhausted** — if a meta-pattern has
  emerged (several hypotheses of the same kind all inert), surface the candidate directions to the
  captain as a strategy decision. First write `## Follow-up Routing` with one of: `stop`
  (oracle-blocked / exhausted / no visible fork), `probe` (new fork exists but wording untested), `file`
  (probe or artifact evidence supports a new hypothesis), or `escalate` (multiple viable directions
  need captain strategy). When you file, it is ONE follow-up `spd<NNNN>-<slug>.md` (status `hypothesis`)
  forking the current `@baseline`.
- **Verdict + archive.** Set `verdict: PASSED` (promoted / ran cleanly to a real result) or `REJECTED`
  (cleanly falsified, e.g. NO-GO at smoke); archive into `_archive/`.

> **Reached `conclude` from `smoke`?** A cleanly-falsified hypothesis routes `smoke → conclude`
> (REJECTED) without a `full` run — the smoke deep-dive is the evidence of record. `full`/`analyze`
> only run when smoke is a GO.

## Champion (`@baseline`)

The reigning champion is the `@baseline` run-dir in the spider2-dbt-local `razorback-registry.yaml`
(resolve it after `export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml`).
The **seed champion is the first scored full run of the `spider2-dbt-baseline` output-contract solver**
under codex/gpt-5.5 — established by the anchor hypothesis (`propose → full`, skipping smoke). Until
that anchor run is promoted, new hypotheses fork from the `spider2-dbt-baseline` solver README;
`analyze` diffs against the `@baseline` run-dir. Because `@baseline` is itself a codex/gpt-5.5 run,
there is **no model-swap confound** — the README is the only variable.

## Packaging / preflight health (the infra-fragility surface)

spider2-dbt has **no PG/Mongo backends** (unlike DAB) — every task is a self-contained DuckDB built
from local views. The fragility lives in `tools/package_spider2_dbt_views.py` and the per-task
build-time preflight. **A packaging/preflight fault is NEVER a result** — recover before drawing any
behavioral conclusion. Known classes (from the smoke standups, `docs/smoke6*.md`):

- **build-time preflight failure** (`razorback_spider2_preflight.py --db-name <x>` exit 2): the source
  DuckDB's required source tables didn't validate — usually a db-name / source-schema mismatch. The
  packager's `_align_source_schemas_to_main()` fixes the f1001-class case (a `sources:` source whose
  default-name schema is absent while `main` holds the tables → set `schema: main`). If a NEW task hits
  this, HALT + escalate (packager code fix, never auto).
- **ephemeral-not-materialized**: correct model names built but placed under an `ephemeral`-configured
  dir (e.g. `models/intermediate/`) → compiled to CTEs, never tables → invisible to the verifier. This
  is a SOLVER-README–addressable failure (the spd0002-class lever), not a packaging bug.
- **goldless / postgres-backed tasks**: excluded from the 61 — never count as regressions.

## Templates

Concept (`spd<NNNN>-<slug>.md`):
```yaml
---
title: <research direction>
status: concept
kind: concept
id: spd<NNNN>
source:
started:
completed:
verdict:
---

## Direction

<the theme and why it might raise the pass rate>
```

Hypothesis (`spd<NNNN>-<slug>.md`):
```yaml
---
id: spd<NNNN>
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

The falsifiable claim and the single solver-README change it makes. Target tasks: <ids>.

## Pre-smoke Decision-Fork Probe

Required for flipped-task follow-ups unless explicitly skipped. State the fork, prompt context, control
result, proposed-rule result, exact README wording tested, expected artifact signature, and why the
proxy does or does not justify smoke.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs only in `experiment:` + `agent.solver_workflow:`.**
Verified by: `diff specs/full-baseline.yaml specs/spd<NNNN>-<slug>.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired delta vs `@baseline` (computed from `per_trial_outcomes.json`,
bootstrap CI), with each verdict change confirmed at the committed artifact (the built table).**

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

Required for every smoke/full rejection or revise route. Classify the failure and define the next fork
or routing decision: stop / probe / file / escalate.

## Follow-up Routing

## Verdict
```

## Commit Discipline

Commit at every stage transition and entity-body update; variant specs + solver READMEs are tracked,
`runs/`, `_views/`, and the live `razorback-registry.yaml` stay gitignored.
