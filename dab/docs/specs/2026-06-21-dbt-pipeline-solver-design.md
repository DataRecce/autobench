# DAB dbt-Pipeline Solver — Design

**Date:** 2026-06-21
**Status:** Approved design — pre-implementation
**Authors:** autoresearch operator (Kent), concept from CL
**Related:** `dab/docs/specs/2026-06-15-dab-autoresearch-design.md` (the loop this plugs into)

## 1. Goal & shape

Solve DAB queries by **forcing the solver to build a dbt data pipeline first, then query
the answer out of the built models** — instead of answering with ad-hoc DuckDB SQL. The
aim is a _reusable, ADE-mergeable_ solver methodology, not a per-question tune.

Research question: **does relocating DAB's normalize → resolve → aggregate logic from
inline CTEs into validated dbt staging/intermediate models (gated on dirty-data schemas)
move codex/gpt-5.5's stratified Pass@1 above the Opus incumbent?**

This is a **single-lever change**: the solver README only. DAB grades `answers.json`
exclusively (`verify.py` → `validate.py` → reward), so the dbt pipeline is _instrumental
scaffolding_ the README prescribes — it never appears in the graded artifact. That keeps
the change inside the independent-variable rule.

**dbt is baked into the `dab-agent` image** (we build that image), installed once and held
**constant across the baseline and every variant run**. So dbt-in-image is part of the
fixed environment, not a per-hypothesis change — the solver README remains the only thing
that _varies between_ compared runs, and the IV rule holds. (Runtime `pip install` is
explicitly _not_ used; it would make the environment vary with the README.)

## 2. Why this can work — the ADE/DAB shared spine

ADE-bench (dbt repair/build, the deliverable _is_ the model) and DAB (query answering)
share one spine: **build + validate dbt staging/intermediate models that normalize and
reconcile dirty source data.** They diverge only at the deliverable.

|         | shared spine (build + validate dbt models)      | deliverable           | grader sees       |
| ------- | ----------------------------------------------- | --------------------- | ----------------- |
| **ADE** | `stg_*` normalize → `int_*` resolve → dbt tests | the model itself      | model correctness |
| **DAB** | same                                            | a query over the mart | `answers.json`    |

The current DAB baseline README already does normalize → entity-resolve → aggregate, but
as inline CTEs. This method relocates each step into an inspectable, testable model:

- **Step 1 — build models:** `stg_*` models do the normalize (lowercase / whitespace
  collapse / `regexp_extract` year / etc.) — today's "Step 1 — Normalize first."
- **Step 2 — answer / find where it's broken:** `int_*` models do entity resolution
  (OR-across-dirty-fields) — today's "Step 2." Generic **dbt tests** (`unique` on the
  declared grain, `not_null` on join keys, a parent/child rowcount-reconcile test) live on
  the **resolved** models and assert the _post-resolution_ invariant. A red test means the
  resolution model is still wrong (one logical entity fragmented, grain not yet collapsed) —
  i.e. _your build_ is broken. This is the ADE-style debug step, reused for free: the agent
  fixes the resolution model and re-runs until tests pass. A red test is **never** reported
  as the answer.
- **Final — answer:** `analyze` queries the mart → `answers.json` — today's "Step 3."

## 3. Scope decision — gated, not mandatory

**Decision (captain, 2026-06-21): gated dbt.** Build the dbt pipeline **only when
`db_description.txt` warns of duplicate rows / different sources / independently dirty
entity-name fields** — the _same trigger the baseline README already uses_ to switch on
the normalize→resolve sequence. Clean schemas skip dbt entirely and stay on plain DuckDB
SQL.

Rejected alternatives:

- **Mandatory dbt for every query** — uniform and the cleanest ADE merge, but burns
  budget/context on plumbing for trivial 1-query datasets and adds a build failure surface
  to queries that don't need it. This is exactly the `dab0005-methodology-overhead-recovery`
  failure mode. Rejected.
- **Probe-only** — that's not a solver method, it's Gate 0 below (a prerequisite, kept).

**Gate text — reused verbatim from baseline.** The variant README MUST copy the baseline
trigger character-for-character (from `solver_workflows/spacedock-readme-baseline/README.md`):

> **Trigger:** if `db_description.txt` warns about `duplicate` rows, `different sources`, or
> independently dirty entity-name fields (e.g. title/artist/album, or name/description) on
> any table you intend to join, group, or rank over, you MUST run the following three steps
> **in order** before issuing the analytical query.

This is *not* a new heuristic, and we deliberately do **not** make the gate executable or
keyword-deterministic — that would be a second lever on top of "relocate logic into dbt
models" and would confound attribution (a win could be the dbt method *or* a sharper gate),
breaking the single-IV rule. Gate precision is its own future hypothesis, if it ever matters.

**Why the gate's fuzziness doesn't bias the result.** Baseline and variant fire on the
*same* trigger text, so any gate ambiguity (including schemas that need normalization but
don't use those exact words) is **held constant and cancels in `rk runs diff`**. The only
thing that varies post-gate is inline CTEs vs. dbt models. Fixing the gate's recall is not
this method's job.

**One new wrinkle:** a false-positive gate fire costs *more* under dbt (scaffolding
overhead) than under baseline (a few extra CTEs). Mitigation already exists — the canary set
(§5 Gate 2) catches overhead regressions on currently-passing clean datasets.

## 4. Architecture — README stage model

Fork `solver_workflows/spacedock-readme-baseline` → `dab00NN-dbt-gated-pipeline`. Same
`model → analyze → verify → done` stage frontmatter. The README body changes:

```yaml
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
  against the _declared grain_, not against any specific question. Keeps it reusable and
  non-tuned.
- **The gate predicate** is the single coupling point to the rest of the README. It reuses
  the baseline trigger **verbatim** (quoted in §3) — no new branching logic, and held
  constant across baseline + variant so its fuzziness cancels in the diff.

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
3. **Mongo — resolved, effectively moot.** dbt-duckdb has no native Mongo adapter, but it
   doesn't need one: every dataset materializes **all** its `dataset.toml` backends (same
   data, different engines), and only **2 of 12** touch Mongo — `agnews` (also `sqlite`) and
   `yelp` (also `duckdb`). Both ship a relational backend dbt-duckdb attaches natively, so
   the dbt pipeline always sources from the relational side and never touches Mongo. No
   Mongo-only dataset exists. The Gate-0 probe only needs to confirm SQLite/PostgreSQL/DuckDB
   attach (item 2); Mongo is not on the critical path.

Probe mechanism: a throwaway README that runs the attach/`dbt run`/`dbt test` on a
single dirty-data query and writes the outcome to `_artifacts/feasibility.md`. Run
`rk run --explain` first, then a 1-query smoke.

**Agent image — concrete build (execute at implementation).** The `dab-agent:latest`
Dockerfile is **not** in this repo; it lives in the sibling `dataagentbench` repo (PKG-24
to vendor it into razorback is still backlog):

- Dockerfile: `dataagentbench/benchmark/Dockerfile.agent` (exeuntu base + one pip layer)
- Build orchestration: `dataagentbench/benchmark/setup.sh:147-152`
- Image-name constant: `razorback-plugin-dab/.../generate/compose.py:14` (`DEFAULT_AGENT_IMAGE`)

1. **Add dbt to the pip layer** in `Dockerfile.agent` — append `dbt-core dbt-duckdb` to the
   existing `pip install --break-system-packages` line (alongside
   `duckdb psycopg2-binary pymongo pyyaml python-dotenv`). Only `dbt-duckdb` — DAB reaches
   SQLite/PG/Mongo *through* DuckDB `ATTACH`, so no `dbt-postgres` is needed.
2. **Rebuild** (self-contained — the Dockerfile `COPY`s nothing; reuse the pinned base digest
   from `setup.sh:36` so only the dbt layer changes):

   ```bash
   cd <path-to>/dataagentbench
   EXEUNTU_DIGEST="sha256:3b4a7e6d616929d0c07fe827711d444ca8d1ebd2f0ce54788d697b9f125a2e82"
   docker pull "ghcr.io/boldsoftware/exeuntu@${EXEUNTU_DIGEST}"
   docker build --build-arg EXEUNTU_DIGEST="${EXEUNTU_DIGEST}" \
     -f benchmark/Dockerfile.agent -t dab-agent:latest .
   ```
3. **Record the digest for provenance** (not enforcement): note
   `docker inspect --format '{{.Id}}' dab-agent:latest` alongside the run. See §7 "Image
   drift (accepted)" for why we do not gate on it.

No re-baseline needed: an unused package doesn't change the non-dbt path's behavior, and
`@baseline` is the converted Opus run (a separate, frozen historical image) — so installing
dbt is environment-neutral for everything except the new dbt variant.

**Gate 1 — author the gated README lever** (only if Gate 0 = GO). Fork + edit per §4,
create full + smoke specs differing from baseline only in `experiment:` + `solver_workflow:`,
`rk freeze --allow-missing`.

**Gate 2 — eval.** Smoke on dirty/multi-source targets — candidates **agnews (0.25),
GITHUB_REPOS (0.25), crmarenapro, yelp** (agnews/yelp source from their relational backend,
not Mongo — see Gate 0 item 3) — plus canaries
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
- **Mongo adapter gap:** resolved — only `agnews`/`yelp` touch Mongo and both ship a
  relational backend dbt-duckdb attaches natively; no Mongo-only dataset exists (Gate 0 item 3).
- **Image drift (accepted confound — captain decision 2026-06-21).** dbt is baked into the
  mutable `dab-agent:latest` tag, and `rk`'s run path does not enforce a frozen
  `image_digest` (compose materializes `image: dab-agent:latest` verbatim). We **accept**
  this rather than build digest-enforcement, on three grounds: (1) the comparison reference
  is the Opus `@baseline`, a separate frozen historical image — there is no codex baseline
  run to keep digest-matched, so the relevant model+environment gap is already the documented
  confound from §7 of the autoresearch design; (2) we control the image and rebuild it
  deterministically from the pinned exeuntu digest, so drift is operator-introduced, not
  ambient; (3) installed-but-unused packages are treated as behavior-neutral on the non-dbt
  path. **Residual risk:** dbt-core's transitive deps (jinja2, pyyaml, click, …) could bump
  a package the baseline path *does* use (`pyyaml` is already in the image). Mitigation: the
  canary set (§5 Gate 2) catches any regression on currently-passing clean datasets; if a
  canary moves unexpectedly, suspect a dependency bump and pin it. The digest is recorded for
  provenance only.
- **Leak-guard:** unaffected — dbt reads only workspace DBs; the external-oracle audit in
  `verify` is unchanged.

## 8. Open questions (resolve at Gate 0 / propose)

1. ~~Runtime install vs. baked image~~ — **resolved: baked into `dab-agent`, constant
   across runs** (§1); digest recorded for provenance, not enforced (§7 accepted confound).
2. ~~Which target datasets are Mongo~~ — **resolved:** only `agnews`/`yelp`, both with a
   relational backend; method sources from the relational side (Gate 0 item 3).
3. Scratch materialization: separate duckdb file under `_artifacts/dbt/` vs. in-memory —
   pick whatever survives the `model → analyze` stage boundary cleanly. **(Defer to Gate 0 —
   the only genuinely empirical unknown left; the probe answers it.)**

## 9. Non-goals

- No per-question dbt models or question-specific tests (would break reusability and the
  IV discipline).
- No change to the grader, specs shape, runtime, model, or sampling — README only.
- No ADE-bench changes; the merge is conceptual (shared spine), realized later if this wins.
