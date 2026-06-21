# DAB dbt-Pipeline Solver — Design

**Date:** 2026-06-21
**Status:** Approved design — pre-implementation
**Authors:** autoresearch operator (Kent), concept from CL
**Related:** `dab/docs/specs/2026-06-15-dab-autoresearch-design.md` (the loop this plugs into)

## 1. Goal & shape

Solve DAB queries by **forcing the solver to build a dbt data pipeline first, then query
the answer out of the built models** — instead of answering with ad-hoc DuckDB SQL. The
aim is a *reusable, ADE-mergeable* solver methodology, not a per-question tune.

Research question: **does relocating DAB's normalize → resolve → aggregate logic from
inline CTEs into validated dbt staging/intermediate models (gated on dirty-data schemas)
move codex/gpt-5.5's stratified Pass@1 above the Opus incumbent?**

This is a **single-lever change**: the solver README only. DAB grades `answers.json`
exclusively (`verify.py` → `validate.py` → reward), so the dbt pipeline is *instrumental
scaffolding* the README prescribes — it never appears in the graded artifact. That keeps
the change inside the independent-variable rule.

**dbt is baked into the `dab-agent` image** (we build that image), installed once and held
**constant across the baseline and every variant run**. So dbt-in-image is part of the
fixed environment, not a per-hypothesis change — the solver README remains the only thing
that *varies between* compared runs, and the IV rule holds. (Runtime `pip install` is
explicitly *not* used; it would make the environment vary with the README.)

## 2. Why this can work — the ADE/DAB shared spine

ADE-bench (dbt repair/build, the deliverable *is* the model) and DAB (query answering)
share one spine: **build + validate dbt staging/intermediate models that normalize and
reconcile dirty source data.** They diverge only at the deliverable.

| | shared spine (build + validate dbt models) | deliverable | grader sees |
|---|---|---|---|
| **ADE** | `stg_*` normalize → `int_*` resolve → dbt tests | the model itself | model correctness |
| **DAB** | same | a query over the mart | `answers.json` |

The current DAB baseline README already does normalize → entity-resolve → aggregate, but
as inline CTEs. This method relocates each step into an inspectable, testable model:

- **Step 1 — build models:** `stg_*` models do the normalize (lowercase / whitespace
  collapse / `regexp_extract` year / etc.) — today's "Step 1 — Normalize first."
- **Step 2 — answer / find where it's broken:** `int_*` models do entity resolution
  (OR-across-dirty-fields) — today's "Step 2." Generic **dbt tests** (`unique` on the
  declared grain, `not_null` on join keys, a parent/child rowcount-reconcile test) live on
  the **resolved** models and assert the *post-resolution* invariant. A red test means the
  resolution model is still wrong (one logical entity fragmented, grain not yet collapsed) —
  i.e. *your build* is broken. This is the ADE-style debug step, reused for free: the agent
  fixes the resolution model and re-runs until tests pass. A red test is **never** reported
  as the answer.
- **Final — answer:** `analyze` queries the mart → `answers.json` — today's "Step 3."

## 3. Scope decision — gated, not mandatory

**Decision (captain, 2026-06-21): gated dbt.** Build the dbt pipeline **only when
`db_description.txt` warns of duplicate rows / different sources / independently dirty
entity-name fields** — the *same trigger the baseline README already uses* to switch on
the normalize→resolve sequence. Clean schemas skip dbt entirely and stay on plain DuckDB
SQL.

Rejected alternatives:
- **Mandatory dbt for every query** — uniform and the cleanest ADE merge, but burns
  budget/context on plumbing for trivial 1-query datasets and adds a build failure surface
  to queries that don't need it. This is exactly the `dab0005-methodology-overhead-recovery`
  failure mode. Rejected.
- **Probe-only** — that's not a solver method, it's Gate 0 below (a prerequisite, kept).

No new heuristic is introduced: the dbt on/off switch *is* the existing dirty-schema gate.

## 4. Architecture — README stage model

Fork `solver_workflows/spacedock-readme-baseline` → `dab00NN-dbt-gated-pipeline`. Same
`model → analyze → verify → done` stage frontmatter. The README body changes:

```
stage: model
  read db_description.txt + connections.yaml          # dbt is preinstalled in the image
  IF schema warns (duplicate / different-source / dirty entity fields):
     scaffold a minimal dbt project in _artifacts/dbt/
       profiles.yml -> duckdb, ATTACH the workspace SQLite/PG/DuckDB sources
       stg_*  models : normalize string keys (lower, regexp ws-collapse, year extract)
       int_*  models : resolve entities (OR across dirty normalized fields)
       schema.yml    : tests on RESOLVED models -> unique(grain), not_null(keys),
                       rowcount reconcile
     LOOP: dbt run ; dbt test ; if red -> fix the resolution model ; repeat
           until green (or, if grain is irreducibly ambiguous, stop and record
           the unresolved invariant in reasoning.md)
     # the model stage does NOT hand off to analyze with a red test
  ELSE:
     skip dbt; produce context.md from plain DuckDB exploration (baseline behavior)
  output: _artifacts/context.md  (+ green _artifacts/dbt/ when built)

stage: analyze
  IF dbt pipeline was built: query the (green) int_*/mart models -> answers.json
  ELSE: plain DuckDB SQL -> answers.json  (baseline behavior)
  if model stage recorded an unresolved invariant for a query -> "UNABLE TO DETERMINE"
  output: answers.json, _artifacts/reasoning.md

stage: verify  (feedback-to: analyze)
  re-derive each answer from the green mart; read the passing dbt tests as evidence
  the grain/keys are sound; REJECT if an answer doesn't reconcile or a query was
  silently answered over a model whose invariant was never made green
  external-oracle audit unchanged (leak-guard)
  output: PASSED / REJECTED stage report
```

**Failure contract (one rule).** dbt tests are a **hard gate on the resolved models**, not
a diagnostic the answer rides on. Green before `analyze`, or the affected query is
`UNABLE TO DETERMINE`. The intra-stage `model` loop owns the fix; `verify → analyze`
feedback owns answer-level rejections. There is no path where `answers.json` is built on a
model with a red test.

### Components & boundaries

- **dbt project** lives under `_artifacts/dbt/` (workspace-local, never touches source
  DBs — DuckDB attaches read-only; intermediate results are dbt models in a scratch
  duckdb file). Self-contained: deletable without affecting the answer once `answers.json`
  is written.
- **Generic tests only.** `unique` / `not_null` / a rowcount-reconcile test expressed
  against the *declared grain*, not against any specific question. Keeps it reusable and
  non-tuned.
- **The gate predicate** is the single coupling point to the rest of the README, and it is
  reused verbatim from baseline — no new branching logic.

## 5. Preparation sequence (the gates)

**Gate 0 — feasibility probe (BLOCKER, ~$0, do before authoring Gate 1).**
Nothing about dbt exists in the DAB environment today (no dbt in the plugin, the workspace,
the baseline README; agent image is `dab-agent:latest`). Before the real hypothesis is
worth authoring, prove:
1. `dbt` + `dbt-duckdb` runs in the solver container. **Decision: baked into the
   `dab-agent` image** (we build it), held constant across baseline + variants (see §1).
   The probe just confirms `dbt --version` resolves and a trivial model builds — no runtime
   install, no pip-network dependency.
2. dbt-duckdb can ATTACH the workspace SQLite / PostgreSQL / DuckDB sources.
3. **Mongo** — the adapter risk. dbt-duckdb has no native Mongo; it only works through
   DuckDB's mongo extension *inside* a model. Either prove that path or restrict the method
   to non-Mongo datasets. Determine which target datasets are Mongo (`compose.py` builds
   `dab-mongo`) **before** fixing the smoke set.

Probe mechanism: a throwaway README that runs the install/attach/`dbt run`/`dbt test` on a
single dirty-data query and writes the outcome to `_artifacts/feasibility.md`. Run
`rk run --explain` first, then a 1-query smoke.

**Gate 1 — author the gated README lever** (only if Gate 0 = GO). Fork + edit per §4,
create full + smoke specs differing from baseline only in `experiment:` + `solver_workflow:`,
`rk freeze --allow-missing`.

**Gate 2 — eval.** Smoke on dirty/multi-source targets that clear the Mongo check —
candidates **agnews (0.25), GITHUB_REPOS (0.25), crmarenapro, yelp** — plus canaries
**bookreview / music_brainz_20k / stockindex** (currently 3/3, guard against overhead
regression). Then full; `rk runs diff` vs Opus `@baseline`.

## 6. Eval & acceptance

- **Smoke GO/NO-GO:** at least one currently-failing target query flips to pass via the
  committed dbt-model artifact (behavioral read, not just reward), and **no canary
  regresses**.
- **Full success:** stratified Pass@1 over the target datasets beats the Opus incumbent on
  a clean `rk audit --policy strict`, attributed by behavioral read (the model-swap
  confound from §7 of the autoresearch design still applies — lean on the committed-artifact
  read to attribute the lever).
- **Reward path unchanged:** `answers.json` remains the only graded output; the dbt project
  is scaffolding.

## 7. Risk register

- **Overhead regression** (`dab0005-methodology-overhead-recovery`): dbt plumbing costs
  budget/context. Mitigated by gating (clean schemas skip dbt) and by the canary set.
- **New failure surface:** a broken dbt build/test can zero a query the baseline passed.
  `verify` + canaries catch this; the gate keeps it off simple queries.
- **Mongo adapter gap:** handled at Gate 0 (prove or exclude).
- **Image drift:** dbt is baked into `dab-agent`; the image must be rebuilt and the SAME
  image used for baseline and variants, or the comparison reintroduces an environment
  confound. Pin/record the image digest at freeze time.
- **Leak-guard:** unaffected — dbt reads only workspace DBs; the external-oracle audit in
  `verify` is unchanged.

## 8. Open questions (resolve at Gate 0 / propose)

1. ~~Runtime install vs. baked image~~ — **resolved: baked into `dab-agent`, constant
   across runs** (§1). Remaining: pin the image digest at freeze so baseline/variant share it.
2. Which target datasets are Mongo — fixes the smoke set.
3. Scratch materialization: separate duckdb file under `_artifacts/dbt/` vs. in-memory —
   pick whatever survives the `model → analyze` stage boundary cleanly.

## 9. Non-goals

- No per-question dbt models or question-specific tests (would break reusability and the
  IV discipline).
- No change to the grader, specs shape, runtime, model, or sampling — README only.
- No ADE-bench changes; the merge is conceptual (shared spine), realized later if this wins.
