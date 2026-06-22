# dab0017 dbt-pipeline — run notes

Design: `dab/docs/specs/2026-06-21-dbt-pipeline-solver-design.md`
Handoff: `dab/docs/plans/2026-06-21-dbt-pipeline-implementation-handoff.md`

## Step 0 — dbt baked into dab-agent image (DONE, 2026-06-21)

- Edit: `dataagentbench/benchmark/Dockerfile.agent` pip layer now installs
  `dbt-core dbt-duckdb` alongside the four DB drivers. Added `--ignore-installed`
  to the pip line because dbt-core's transitive deps (zipp, typing_extensions)
  require upgrading debian-managed packages that lack a RECORD file and pip
  cannot uninstall — `--ignore-installed` overlays fresh copies (standard
  externally-managed-base workaround). No `dbt-postgres` (DAB reaches PG/Mongo
  via DuckDB ATTACH).
- Built from pinned base `EXEUNTU_DIGEST=sha256:3b4a7e6d616929d0c07fe827711d444ca8d1ebd2f0ce54788d697b9f125a2e82`
  (= setup.sh:36), only the dbt pip layer changed.
- **Image digest (SUPERSEDED — pre extension layer):**
  `sha256:4ee4387cf496f569bd0cafa1d91026facd3ea1329228f1ba5f2990f85e8f421f`
- **Extension-preinstall layer added (captain chose Option A, 2026-06-21).** The run
  container blocks egress to extensions.duckdb.org, so DuckDB's sqlite/postgres scanner
  extensions (download-on-demand) made `ATTACH (TYPE SQLITE|POSTGRES)` fail offline (Gate 0
  finding). Fix: a build-time `RUN HOME=/home/exedev python -c "...INSTALL sqlite; INSTALL
  postgres"` + chown, baking them into exedev's default extension home so `ATTACH` AUTOLOADS
  them offline with **no profile config and no explicit LOAD**. Verified offline (`--network
  none`): `ATTACH sqlite ok: [(99,)]`; offline `INSTALL` is a no-op when present (so a dbt
  profile `extensions: [sqlite, postgres]` also works offline). No mongo scanner (design §5
  item 3). Baseline drivers + dbt-duckdb still import.
- **Image digest (CURRENT, provenance only — not enforced, design §7):**
  `sha256:224133f07cabc85c7dd8672e57d1ab9a46e5098960c5d1668918ba33df5e4742`
- **Artifact-capture note:** the run container workspace is NOT persisted to the run-dir
  (`steps/main/artifacts/` is empty; only `reward*.json` survive). The "committed dbt-model
  artifact" the design/handoff require for judging flips is recovered from the agent
  transcript (`steps/main/agent/codex.txt` + `agent/sessions/.../rollout-*.jsonl` apply_patch
  bodies). Judge dbt models by reading those, not a persisted file tree.
- STOP-gate verification (all PASS):
  - `dbt --version` → Core 1.11.11, duckdb plugin 1.10.1
  - `import dbt.adapters.duckdb` → OK
  - `import duckdb, psycopg2, pymongo, yaml, dotenv` → OK (duckdb 1.5.4) —
    the dep overlay did NOT break the baseline non-dbt path.

## Gate 1.5 — anchor measurement (in progress)

- **First batch-baseline run** `runs/codex-dab-batch-baseline/342778d74e96f477` (concurrency 4):
  INCONCLUSIVE. strat_pass@1 0.696 was over **11** datasets — PATENTS **errored** (dropped
  from denominator), yelp 0/7 (mongo). With PATENTS=0 over 12 it's 0.638. Audit blind-spot:
  reported `clean:12 tainted:0` despite the dropped dataset.
  - **PATENTS root cause:** agent returned q1 as a LIST; `validate_q1.py` does `.lower()` →
    AttributeError; `verify_batch.py` had no per-query try/except → whole dataset crashed
    (RewardFileNotFoundError). NOT a postgres issue (healthcheck passed, agent completed).
  - **yelp root cause:** mongo "connection refused" (×2) → 18× UNABLE TO DETERMINE. Resource
    contention at concurrency 4 (4 full pg+mongo+agent stacks on a 15GB box); restart fixes
    are present in compose.py but recovery lagged under load.
- **Fixes applied (captain-approved):**
  - `verify_batch.py` per-query try/except — **razorback PR #19**
    (`fix/dab-verify-batch-per-query-isolation`). Scoring-neutral; import-time failures still
    crash loudly (existing test preserved). Held constant on anchor + variant.
  - Lowered `concurrency: 4 → 2` on all three specs (anchor + variant + smoke), re-frozen.
- **Re-run:** `codex-batch-baseline-v2` launched (handle `codex-batch-baseline-v2-*`) — uses
  the fixed verifier (in working tree before launch) + concurrency 2.

## CONNECTION-HOST bug + mongo-only data (captain Option A, 2026-06-21)

- **yelp 0/7 root cause:** the baseline solver README (the lever) hardcodes
  `mongodb://localhost:27017` (mongo) and `host=localhost ... password=dabench` (postgres).
  The spacedock workspace runs these in separate containers at `dab-mongo`/`dab-postgres`
  (the plugin workspace_readme says so — the two docs CONFLICT). Agent followed localhost →
  "connection refused". Harness healthcheck confirmed mongo was UP at dab-mongo with data.
  yelp's business data is **mongo-only** (no relational copy — contradicts design §5), so all
  business questions abstained → 0/7. Same bug cost crmarenapro q2/q7 (postgres) and agnews
  mongo queries. NOT a codex/infra/contention issue; concurrency change does NOT fix it.
- **Captain decision (Option A):** fix hosts in BOTH READMEs (held constant) so the only
  remaining lever is dbt-vs-no-dbt; add a pymongo→dbt-seed bridge for mongo data.
  - Anchor README **forked** → `spacedock-readme-baseline-hostfix` (localhost→dab-postgres/
    dab-mongo; postgres password dabench→postgres; mongo via **pymongo** not duckdb ATTACH
    TYPE MONGO — the mongo duckdb extension is also unavailable offline). Original shared
    `spacedock-readme-baseline` left untouched (used by archived hypotheses).
  - `codex-dab-batch-baseline.yaml` repointed to the hostfix fork. IV re-verified: anchor vs
    variant differ only in experiment + solver_workflow.
  - Variant `dab0017` README: postgres already dab-postgres (ATTACH, scanner baked); mongo
    section rewritten to pymongo→`_artifacts/dbt/seeds/<collection>.csv`→dbt source (the ONLY
    mongo→duckdb bridge; explicitly NOT the forbidden relational-source seed-export shortcut).
- **baseline-v2 STOPPED** (rc=143) before completion — it used the broken-host README; its
  cells show NonZeroAgentExitCodeError from the operator kill (no summary written). Abandoned.
  Orphan containers cleaned. Replaced by the host-fixed re-run.
- **Validating** host fix on yelp+crmarenapro (`codex-batch-baseline-hostcheck`) before the
  full anchor re-run.

### Dep-overlay residual risk (design §7) — full pin-candidate list
`--ignore-installed` overlaid fresh copies of several debian-managed packages.
Bumps that touch the **baseline (non-dbt) path** (antagonist-step0 audit):
- **PyYAML 6.0.1 → 6.0.3** (baseline uses `pyyaml`)
- **Jinja2 3.1.2 → 3.1.6**
- **click 8.1.6 → 8.4.1**
- (also zipp 1.0.0→4.1.0, typing_extensions 4.10.0→4.15.0, packaging 24.0→26.2,
  MarkupSafe 2.1.5→3.0.3)
`duckdb` stayed at **1.5.4** (dbt-duckdb declares `duckdb>=1.0.0`, no cap — NO
downgrade/pin of the baseline's query engine; the most dangerous confound did not occur).
All same-major compatible bumps; baseline drivers still import + duckdb connect/yaml
roundtrip work. **Canary set (Gate 2) is the backstop**: any unexpected canary move ⇒
suspect one of these bumps and pin it.

Note: `--ignore-installed` leaves the OLD debian copies physically on disk (shadowed);
the pip copies win by sys.path order (`/usr/local` before `/usr/lib`) — benign today,
latent provenance hazard. Acceptable for this single-image, back-to-back-run setup.
