# DAB dbt-Pipeline Solver — Design

**Date:** 2026-06-21
**Status:** Approved design — pre-implementation
**Authors:** autoresearch operator (Kent), concept from CL
**Related:** `dab/docs/specs/2026-06-15-dab-autoresearch-design.md` (the loop this plugs into)

## 1. Goal & shape

Solve DAB queries by **forcing the solver to build a dbt data pipeline first, then query
the answer out of the built models** — instead of answering with ad-hoc DuckDB SQL. The
aim is a _reusable, ADE-mergeable_ solver methodology, not a per-question tune.

Research question: **does forcing _every_ dataset through a built+validated dbt pipeline —
so the answer stage becomes a pure "query the dbt models" step — move codex/gpt-5.5's
stratified Pass@1 above the Opus incumbent without regressing currently-passing datasets?**

**Architecture intent (CL's "staged unified data solver").** The point is a clean two-phase
shape: **Phase 1 (model)** builds the dbt models for the dataset; **Phase 2 (analyze)** does
nothing but query those models for each answer. Making this uniform across all 12 datasets is
the goal — a reusable, non-specialized method, not a per-question tune. (An earlier draft
gated dbt to only the "dirty-data" datasets; that left two code paths and defeated the
unified-query architecture — see §3.)

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

Every dataset builds a dbt pipeline; the answer is always a query over its models. The
pipeline is always 3 layers, but each layer scales to what the schema needs:

- **Step 1 — `stg_*` (always):** one staging model per source table — type casts, light
  normalize (lowercase / whitespace collapse / `regexp_extract` year). For a clean dataset
  this is a near-passthrough; for a dirty one it carries the normalize logic.
- **Step 2 — `int_*` / mart (always):** the joins/aggregations the questions need. **When
  the schema warns of duplicate / different-source / dirty entity-name fields**, this layer
  also does entity resolution (OR-across-dirty-fields); when it doesn't, it's a plain
  join/aggregate. Generic **dbt tests** (`unique` on the declared grain, `not_null` on join
  keys, a parent/child rowcount-reconcile test) assert the model's invariant. A red test
  means _your build_ is wrong (grain not collapsed, key fragmented) — the ADE-style debug
  step, reused for free: fix the model and re-run until green. A red test is **never**
  reported as the answer.
- **Step 3 — answer (always):** `analyze` queries the mart → `answers.json`. Pure query — no
  exploration, no ad-hoc SQL outside the dbt project.

So the dbt pipeline is mandatory; the **entity-resolution work inside it is the only part
that's conditional** (on the same dirty-schema signal the baseline README already names).
That conditionality lives _inside_ a model, not as an on/off switch for the whole pipeline.

## 3. Scope decision — mandatory (all datasets through dbt)

**Decision (captain, 2026-06-21): mandatory dbt.** Every dataset builds a dbt pipeline and
every answer is a query over it. There is **no on/off gate** for the pipeline — that is the
whole point (§1): a single uniform code path, so the answer stage is purely "query the dbt
models." Only the entity-resolution work _inside_ the pipeline is conditional (§2).

**Why we reversed the earlier "gated" draft.** A prior version gated dbt on the baseline's
dirty-schema trigger. Reading the actual materialized descriptions
(`db_description_withhint.txt`, the `hints: true` baseline) showed the gate fires on
essentially **one** dataset (`music_brainz_20k`, which already passes 3/3) plus a borderline
`crmarenapro` — and **none** of the real failing targets (PATENTS, agnews, GITHUB_REPOS,
yelp) trip it. So gating would make the method a no-op exactly where the score gaps are, and
it would leave two code paths, breaking the unified-query architecture. Mandatory fixes both.

**Accepted cost — overhead is now the headline risk.** Forcing dbt onto a clean, 1-query
dataset costs budget/context and adds a build failure surface that can regress a
currently-passing dataset (`dab0005-methodology-overhead-recovery`). We accept this as the
price of a uniform architecture, and manage it three ways:

1. **Minimal, templated scaffold** — staging models are near-passthrough for clean schemas;
   the README ships a fixed dbt skeleton so the agent fills models, not boilerplate.
2. **A codex baseline** (§5 Gate 1.5) — measure overhead against codex's _own_ current
   scores, not against Opus, so a regression is attributable to dbt, not the model swap.
3. **Canaries** — currently-passing datasets in every smoke set; any drop is an overhead
   stop-signal.

**The dirty-schema signal still matters, but only inside Step 2.** The variant README reuses
the baseline trigger verbatim to decide whether the `int_*` layer adds entity resolution. It
is no longer a pipeline gate, so it can't make the method a no-op; it just selects which
models a (always-built) pipeline contains.

## 4. Architecture — README stage model

Fork `solver_workflows/spacedock-readme-baseline` → `dab00NN-dbt-pipeline`. Same
`model → analyze → verify → done` stage frontmatter. The README body changes:

```yaml
stage: model    # Phase 1 — build the pipeline (ALWAYS, every dataset)
  read db_description.txt + connections.yaml          # dbt is preinstalled in the image
  scaffold the templated dbt project in _artifacts/dbt/
    profiles.yml -> duckdb, ATTACH the workspace SQLite/PG/DuckDB sources
    stg_*  models : one per source table — cast + light normalize (passthrough if clean)
    int_*/mart    : the joins/aggregations the questions need
                    + IF schema warns (duplicate / different-source / dirty entity fields):
                        add entity resolution (OR across dirty normalized fields)
    schema.yml    : tests -> unique(grain), not_null(keys), rowcount reconcile
  LOOP: dbt run ; dbt test ; if red -> fix the model ; repeat
        until green (or, if grain is irreducibly ambiguous, stop and record
        the unresolved invariant in reasoning.md)
  # model stage does NOT hand off to analyze with a red test
  output: green _artifacts/dbt/  (+ _artifacts/context.md)

stage: analyze  # Phase 2 — pure query, no ad-hoc SQL outside the dbt project
  query the (green) int_*/mart models -> answers.json
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
- **The dirty-schema signal** (reused verbatim from the baseline trigger) only decides
  whether the `int_*` layer adds entity resolution — it is _not_ a pipeline on/off gate.
  The pipeline is always built, so the signal's fuzziness can't make the method a no-op; at
  worst it adds/omits a resolution model, which the dbt grain tests would catch.

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

Probe mechanism: a throwaway README that exercises **the actual load-bearing runtime**, not a
toy case. Run it on a **multi-query** dataset (**`crmarenapro`**, 13 queries) under
**`query_mode: batch` + `workspace_variant: spacedock`**, and require it to: build the dbt
pipeline **once**, answer **all** queries from the models into one `answers.json`, and pass
`verify_batch`. It must also confirm the dbt scratch project survives the `model → analyze`
stage boundary (§8 #3). Write the outcome to `_artifacts/feasibility.md`. Run `rk run --explain`
first. A 1-query/per-query probe is **insufficient** — it never touches batch, `verify_batch`,
or the multi-query build-once path, so it could green-light a runtime that's actually broken.

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

The Opus `@baseline` does not need rerunning: it's a converted legacy run on a separate
frozen image, and adding an unused package doesn't change anything that doesn't import it.
(The _codex_ baseline below is a separate, deliberate addition — not forced by the image.)

**Execution mode — `query_mode: batch` (load-bearing for mandatory dbt).** A DAB dataset has
many queries (crmarenapro has 13). The plugin's default `query_mode: per-query` materializes
one workspace **per query**, which would rebuild the whole dbt pipeline once per query — e.g.
13× for crmarenapro, pure waste. We run **`plugin_args.query_mode: batch`** (with
**`workspace_variant: spacedock`**): one workspace **per dataset**, all queries answered in a
single turn (`verify_batch` validates each query → per-query rewards, so stratified Pass@1 is
unchanged and comparable). This makes "build the dbt pipeline **once per dataset**, query it
for every question" actually true — it's the runtime that realizes the §1 two-phase shape. The
current `codex-dab-baseline.yaml` sets neither (→ per-query); the new specs set both explicitly.

**Gate 1 — freeze the comparison anchor: `@codex-batch-baseline`.** The mandatory-dbt shape
requires `batch` + `spacedock` `plugin_args`, which the old per-query `codex-dab-baseline` does
**not** use — so the variant is *not* a two-field diff against that old spec. Instead:

1. Author a **`codex-dab-batch-baseline.yaml`**: the current baseline README (no dbt) +
   `plugin_args.query_mode: batch` + `workspace_variant: spacedock`. Freeze it; register the
   run as **`@codex-batch-baseline`**. This is the proper apples-to-apples anchor (same model,
   same runtime grouping, no dbt).
2. Fork `solver_workflows/spacedock-readme-baseline` → `dab00NN-dbt-pipeline` and edit its
   README per §4. Create the **dbt variant spec by copying `codex-dab-batch-baseline.yaml` and
   changing only `experiment:` + `solver_workflow:`** — *that* is the clean single-lever
   (README-only) diff. `query_mode` and `workspace_variant` are identical on both sides, so
   they cancel.

`rk freeze --allow-missing` both. (The old per-query `codex-dab-baseline` is superseded as the
comparison anchor; Opus `@baseline` remains only the headline-incumbent reference, §6.)

**Gate 1.5 — measure `@codex-batch-baseline` and intersect the canary pool.** Running
`@codex-batch-baseline` over the smoke set gives codex's _own_ current per-dataset scores
(codex ≠ Opus). **Define canaries as the intersection: queries that pass in *both* Opus
incumbent *and* `@codex-batch-baseline`.** This closes the gap where a dataset Opus passes but
codex-batch already fails could be picked as a canary and let the variant lose an
incumbent-passing dataset while still "passing" the canary rule. **Separately flag** any
Opus-passing dataset that `@codex-batch-baseline` already regresses — that's a finding about
codex/batch itself (independent of dbt), to record before judging the variant.

**Gate 2 — eval.** Smoke a **mix** (mandatory dbt touches every dataset, so the smoke set must
test both reach and safety):

- **Failing targets** (can dbt flip them?): **crmarenapro** (q2/q3/q8; the one target whose
  schema also warrants entity resolution) + **GITHUB_REPOS** (multi-value parse via `int_*`).
- **Canaries** (does mandatory-dbt overhead regress a passer?): from the **Opus ∩
  `@codex-batch-baseline`** intersection (Gate 1.5) — start from **bookreview /
  music_brainz_20k / stockindex** + a near-perfect one (**stockmarket** / **googlelocal**), but
  **drop any that codex-batch doesn't also pass**.

Compare each smoke run **two ways**: vs `@codex-batch-baseline` (overhead/regression) and vs
Opus `@baseline` (headline).

**Non-regression is per-query and applies everywhere, not just to the named canaries.** The
canary _datasets_ above are just the cheapest place to watch overhead; the actual blocker is:
**no query that passes in both Opus and `@codex-batch-baseline` may regress — in any evaluated
dataset, including the failing-target datasets and the full run.** crmarenapro has 10 passing
queries; flipping q2 while breaking q1 is a fail, not a win. Every smoke/full report MUST
include an explicit **regression table over all Opus ∩ `@codex-batch-baseline` passers in the
evaluated set**, not just the chosen canaries.

GO only if a target flips **and** zero Opus ∩ codex-batch passers regress. Then full over all 12.

## 6. Eval & acceptance

- **Smoke GO/NO-GO:** at least one currently-failing target query flips to pass via the
  committed dbt-model artifact (behavioral read, not just reward), **and zero Opus ∩
  `@codex-batch-baseline` passers regress anywhere in the smoke set** (per-query, across both
  target and canary datasets — see Gate 2, not only the named canaries).
- **Full success:** **(a)** stratified Pass@1 over all 12 datasets beats the Opus incumbent on
  a clean `rk audit --policy strict`, **and (b) a hard non-regression bar — no Opus ∩
  `@codex-batch-baseline` passer regresses anywhere in the full 12**, shown by an explicit
  per-query regression table. Aggregate Pass@1 beating Opus is necessary but **not sufficient**:
  a net-positive run that silently trades away incumbent passers is a FAIL, not a win.
  Attribute by behavioral read — the model-swap confound
  (codex vs Opus, §7 of the autoresearch design) is on the _headline_ comparison; the
  _overhead_ question is answered cleanly by `@codex-batch-baseline`.
- **Reward path unchanged:** `answers.json` remains the only graded output; the dbt project
  is scaffolding.

### Incumbent per-dataset scores (Opus `@baseline`, xhigh +hints; 54 q / 12 ds; strat. P@1 = 0.654)

Source: `dab/hypotheses/_artifacts/dataset-gap-ranking.md`. Used to pick targets (headroom)
and canaries (currently passing). **Note these are _Opus_ scores — `@codex-batch-baseline`
(Gate 1.5) gives codex's own numbers; canaries are the Opus ∩ codex-batch intersection, and
the canary check compares against `@codex-batch-baseline`.**

| group | dataset | score | queries | failing |
| --- | --- | --- | --- | --- |
| 🟢 perfect (canary pool) | bookreview | 1.00 | 3/3 | — |
| 🟢 perfect (canary pool) | music_brainz_20k | 1.00 | 3/3 | — |
| 🟢 perfect (canary pool) | stockindex | 1.00 | 3/3 | — |
| 🟡 near-perfect | yelp | 0.86 | 6/7 | q6 |
| 🟡 near-perfect | stockmarket | 0.80 | 4/5 | q4 |
| 🟡 near-perfect | crmarenapro | 0.77 | 10/13 | q2, q3, q8 |
| 🟡 near-perfect | googlelocal | 0.75 | 3/4 | q2 |
| 🔴 headroom (targets) | PANCANCER_ATLAS | 0.67 | 2/3 | q1 |
| 🔴 headroom (targets) | DEPS_DEV_V1 | 0.50 | 1/2 | q1 |
| 🔴 headroom (targets) | agnews | 0.25 | 1/4 | q2, q3, q4 |
| 🔴 headroom (targets) | GITHUB_REPOS | 0.25 | 1/4 | q1, q2, q4 |
| 🔴 headroom (targets) | PATENTS | 0.00 | 0/3 | q1, q2, q3 |

## 7. Risk register

- **Overhead regression — PRIMARY risk under mandatory** (`dab0005-methodology-overhead-recovery`):
  forcing dbt onto every dataset (including clean, 1-query ones) costs budget/context and can
  regress a passer. No gate to fall back on. Mitigated by: (1) a minimal templated scaffold so
  the agent fills models not boilerplate; (2) `@codex-batch-baseline` (§5 Gate 1.5) for clean
  attribution; (3) the **per-query non-regression bar of Gate 2/§6** — _any single_ Opus ∩
  `@codex-batch-baseline` passer regressing **anywhere** in the evaluated set (not just the
  named canary datasets) is a stop-signal. The named canaries are only the cheapest smoke
  subset to watch, **not** the limit of the check. Separately, if regressions are _broad_
  across many datasets, the mandatory decision itself is falsified — fall back to gating (that
  global-falsification judgment is the only place "broadly" applies).
- **New failure surface:** a broken dbt build/test can zero a query the baseline passed —
  now on _every_ dataset, not just dirty ones. `verify` + the per-query non-regression bar
  (Gate 2/§6) catch it; the templated scaffold + green-tests-before-`analyze` contract bound it.
- **Mongo adapter gap:** resolved — only `agnews`/`yelp` touch Mongo and both ship a
  relational backend dbt-duckdb attaches natively; no Mongo-only dataset exists (Gate 0 item 3).
- **Image drift (accepted confound — captain decision 2026-06-21).** dbt is baked into the
  mutable `dab-agent:latest` tag, and `rk`'s run path does not enforce a frozen
  `image_digest` (compose materializes `image: dab-agent:latest` verbatim). We **accept**
  this rather than build digest-enforcement, on three grounds: (1) `@codex-batch-baseline` and the
  dbt variant are run back-to-back under the **same rebuilt image**, so they are digest-matched
  in practice; the only un-matched reference is the Opus `@baseline` (a separate frozen
  historical image), whose model+environment gap is already the documented confound from §7 of
  the autoresearch design; (2) we control the image and rebuild it
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
   pick whatever survives the `model → analyze` stage boundary cleanly. (Defer to Gate 0 —
   the probe answers it.)
4. ~~Gated vs. mandatory~~ — **resolved: mandatory** (§3), reversing the earlier gated draft;
   the unified-query architecture (§1) requires it.
5. **Does mandatory-dbt overhead regress currently-passing datasets?** — the central
   empirical unknown. Not answerable on paper; the Gate-2 canaries vs `@codex-batch-baseline`
   decide it. If they regress broadly, fall back to gating (§7).

## 9. Non-goals

- No per-question dbt models or question-specific tests (would break reusability and the
  IV discipline).
- The README is the only lever that **varies between** `@codex-batch-baseline` and the variant.
  `query_mode: batch` + `workspace_variant: spacedock` are set in **both** specs as
  held-constant constants (§5 Execution mode) — they change the runtime grouping, not the
  comparison. Grader, runtime, model, and sampling are otherwise unchanged.
- No ADE-bench changes; the merge is conceptual (shared spine), realized later if this wins.
