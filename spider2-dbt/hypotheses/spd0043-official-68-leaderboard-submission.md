---
title: Expand the board to the official 68 instances and produce a leaderboard-format submission (@baseline README + gpt-5.6-sol xhigh)
status: analyze
kind: hypothesis
source: "captain-directed (2026-07-29). Prepare a spider2-dbt leaderboard submission. Requirements: (a) the full run must execute ALL official spider2-dbt instances — 68 per examples/spider2-dbt.jsonl; (b) prove razorback can execute any one of them and produce the evidence the upstream evaluation_suite requires; (c) use @baseline solver README + gpt-5.6-sol @ xhigh. Upstream ref: https://github.com/xlang-ai/Spider2/tree/main/spider2-dbt/evaluation_suite"
started: 2026-07-29T02:03:46Z
completed:
verdict:
score: 0.95
worktree:
id: spd0043
---

## Hypothesis

Not a lever hypothesis — a **coverage + deliverable** entity. The claim under test is operational:
**razorback can execute all 68 official spider2-dbt instances and emit a submission bundle that the
upstream `evaluation_suite/evaluate.py` accepts and grades.**

Falsifiable in two ways: an instance that cannot be packaged or executed, or a bundle the official
evaluator rejects or grades inconsistently with razorback's own rewards.

## Task-set audit (FO, 2026-07-29)

> **SUPERSEDED in part** by `## Propose findings` below. The set counts (68 official / 65 gold /
> 61 views / 60 in spec) all reproduce. Two conclusions do NOT: "All 8 have project sources … so
> none is fundamentally blocked" is **false** (gitcoin001 ships no source DuckDB anywhere upstream),
> and the gradeable count is **63, not 64** (chinook001's gold ships no answer tables). Kept as the
> FO's record; read the corrected audit below.

| Set | Source | Count |
|---|---|---|
| Official instance list | `Spider2/spider2-dbt/examples/spider2-dbt.jsonl` | **68** (all `type: DBT`) |
| Local gold dirs | `Spider2/spider2-dbt/evaluation_suite/gold/` | 65 |
| Our packaged task views | `spider2-dbt/_views/spider2-dbt-*` | 61 |
| Our current run spec | `specs/spd0042-*.frozen.yaml` | 60 |

Note: the upstream README says "69 examples"; the machine-readable list says 68. **68 is authoritative.**
`danish_democracy_data001` has a gold dir but is NOT in the official 68 — it must NOT be submitted.

### The 8 official instances we do not currently run

Group A — **gold present locally, fully self-gradable** (packaging is the only gap):

| Instance | Gold | View | Note |
|---|---|---|---|
| chinook001 | Y | Y | view exists but EXCLUDED from the board per spd0010 as "upstream-goldless". Gold DOES exist at `evaluation_suite/gold/chinook001`. **Re-examine that exclusion — it may be stale or may have a different real cause.** |
| inzight001 | Y | N | never packaged |
| shopify001 | Y | N | never packaged |
| shopify002 | Y | N | never packaged |

Group B — **no gold in the local eval suite** (runnable, not locally gradable):

| Instance | Gold | Source dir | Note |
|---|---|---|---|
| airbnb002 | N | Y | official, `type: DBT` |
| biketheft001 | N | Y | official, `type: DBT` |
| gitcoin001 | N | Y | official, `type: DBT` |
| google_ads001 | N | Y | official, `type: DBT` |

All 8 have project sources under `Spider2/spider2-dbt/examples/`, so none is fundamentally blocked.
Group B is expected for a leaderboard: the submission carries answers and the leaderboard grades them
server-side. **All 68 get submitted.** Submitting only the 64 self-gradable would cap the score at 64/68.

## Propose findings (ensign, 2026-07-29)

Everything below was derived locally and re-verified; where it disagrees with the FO brief, this
section is the one to trust (the FO dispatch instructed exactly that).

### 1. Corrected task-set audit — the official 68 split five ways, not two

| Class | Count | Instances |
|---|---|---|
| Runnable **and** locally gradeable | **63** | the 60 on the spd0042 board + `inzight001`, `shopify001`, `shopify002` |
| Runnable, NOT locally gradeable — gold ships **no answer tables** | 1 | `chinook001` |
| Runnable, NOT locally gradeable — **no gold dir upstream** | 3 | `airbnb002`, `biketheft001`, `google_ads001` |
| **NOT runnable** — no source data anywhere upstream | 1 | `gitcoin001` |
| **Official total** | **68** | |

Provenance of the gap, from the upstream archives themselves (`Spider2/spider2-dbt/*.zip`, the inputs
`setup.py` extracts):

```
DBT_start_db.zip : 68 source .duckdb — the official 68 MINUS gitcoin001 PLUS danish_democracy_data001
dbt_gold.zip     : 65 gold   .duckdb — the official 68 MINUS airbnb002/biketheft001/gitcoin001/google_ads001
                                        PLUS danish_democracy_data001
```

So the 4 missing golds and the 1 missing source are **upstream gaps, not a broken local checkout** —
re-running `setup.py` cannot recover any of them. `danish_democracy_data001` ships both a source and a
gold but is absent from `examples/spider2-dbt.jsonl` and from `gold/spider2_eval.jsonl`, so upstream's
own evaluator would never grade it. Confirms: it must not be submitted.

The upstream README's "69 examples" matches neither the instance list (68) nor the gold set (65) nor
the source set (68). The machine-readable `examples/spider2-dbt.jsonl` is authoritative, as the FO said.

Also confirmed: all **68** official instances have an eval line in `gold/spider2_eval.jsonl`, and all
68 use `func: duckdb_match` with `gold` + `condition_tabs` + `condition_cols` + `ignore_orders`
populated. No instance is `table_match`, `number_match`, or `string_match`. That fixes
`answer_type: "file"` for every bundle entry (see finding 5).

**Gold-integrity gate over all 68** (open each gold DuckDB, assert every `condition_tabs` table exists
— the check spd0010 recommended and deferred):

```
chinook001      MISSING_CONDITION_TABS   ['dim_customer', 'fct_invoice', 'obt_invoice']
airbnb002       NO_GOLD_DIR
biketheft001    NO_GOLD_DIR
google_ads001   NO_GOLD_DIR
gitcoin001      NO_GOLD_DIR
OK: 63/68
```

### 2. chinook001 — the exclusion is STILL VALID, not stale

The FO's premise was that `evaluation_suite/gold/chinook001` now existing means spd0010's
"upstream-goldless" exclusion went stale. It did not: **the directory existing is not the same as the
answers existing.** spd0010's actual finding reproduces exactly — the gold DuckDB is present and
readable, and all three of its `condition_tabs` (`dim_customer`, `fct_invoice`, `obt_invoice`) are
absent from it. The gold side of the compare can never yield a match.

Independent corroboration from run history: chinook001 has executed in **9** run-dirs across this
workflow (`runs/*/*/spider2-dbt-chinook001__*`) and scored **reward 0.0 in 9 of 9**, with
`agent_execution` and `verifier` both present and `exception_info: None` in the most recent. It is not
an erroring cell — it runs clean and is structurally unscoreable locally.

**Decision (evidence-based): RUN it and SUBMIT it; exclude it from the local gradeable denominator.**
The leaderboard holds the real gold, so an answer for chinook001 may well score there; dropping it from
the submission would cap the achievable score at 67/68 for no gain. This is the same treatment the 3
no-gold instances get. Its view already exists and needs no repair.

### 3. BLOCKER — the predicted DuckDB does not survive a run, so no bundle can be exported

This is the finding that governs the whole entity. `tests/test.sh` runs the verifier **inside** the task
container against `/app/<db>.duckdb`; only `/logs/verifier/reward.json` reaches the host, and harbor then
tears the container down with `down --volumes`. A completed run-dir therefore contains **no copy of the
answer**. Verified on the real 60-cell spd0042 run-dir:

```
$ python tools/export_submission_bundle.py --run-dir runs/spd0042-rebaseline-gpt56sol-xhigh/1984b76c702a0dfa --out …
results_metadata.jsonl entries: 0  (exported 0, placeholder 0)
not exported        : 60      # every cell: MISSING_ARTIFACT — no verifier/predicted.duckdb
```

`tools/capture_predicted_db.sh` (from an earlier cycle) works only by `docker cp`-polling a **live**
container, so it cannot recover a past run and would need 68 concurrent pollers for a future one.

**Fix, built and proven: `tools/add_predicted_db_capture.py`.** Harbor bind-mounts the container logs dir
to the host trial dir (`harbor/environments/docker/docker.py::prepare_logs_for_host` chowns the
*bind-mounted* logs dir back to the host user) — which is exactly why `reward.json` appears on the host.
So one line in `test.sh` persists the answer at full size with no copy step and no size cap:

```
# razorback-spider2: persist the predicted DuckDB for submission export
cp /app/inzight.duckdb /logs/verifier/predicted.duckdb || true
```

Applied to all 64 views, idempotent (`already: 64` on re-run). Reward-neutrality proven **by execution**,
not by inspection — a path-rewritten copy of the real `test.sh` was run against a real gold/pred pair
before and after patching:

| control | predicted DB fed in | reward before patch | reward after patch | captured? |
|---|---|---|---|---|
| positive | inzight001 gold | `{"reward": 1.0}` | `{"reward": 1.0}` — `cmp` IDENTICAL | yes, `cmp`-identical to source |
| negative | inzight001 unbuilt source | — | `{"reward": 0.0}` | yes |

The diff against the unpatched `test.sh` is exactly the two lines above; the `verify.py` invocation is
byte-identical, the `cp` is best-effort (`|| true`) so a failed copy can never turn a passing cell into
an error, and `tests/` is uploaded only at verify time and is not in the Docker build context — the
agent sees nothing different and no image layer is invalidated.

**Cost to plan for:** gold DuckDBs average 37 MB and top out at 334 MB (2.4 GB for 65). A 64-cell
predicted-DB capture is the same order — call it 3–8 GB. `/` currently has **46 GB free (82% used)**.
Fine, but not ignorable.

### 4. BLOCKER (fixed) — 3 official instances were unpackageable because razorback reads a *vendored* dbt profile

`inzight001`, `shopify001`, `shopify002` all failed to materialize:

```
Spider2WorkspacePreflightError: {"reason": "target output not duckdb", "target": "postgres", "type": "postgres"}
```

Cause: `preflight.resolve_spider2_db_name` → `_read_profiles_db_path` walks
`workspace.rglob("profiles.yml")` **without excluding `dbt_packages/`**, and `sorted()` puts
`dbt_packages/…` (d) ahead of the project's own `profiles.yml` (p). Those three instances are the only
ones in the 68 that vendor a package shipping its own CI profile —
`dbt_packages/dbt_date/integration_tests/ci/profiles.yml`, which declares `target: postgres`. The
resolver hits that first and fails closed. Each project's own `profiles.yml` is plain
`type: duckdb`.

Fixed **in `tools/` only**, matching the surface spd0010 established ("confined to the packager; the
comparator/scorer is NEVER edited"): `_prune_vendored_profiles` deletes `profiles.yml` files vendored
inside `dbt_packages/` from the staged copy. dbt only ever reads `$DBT_PROFILES_DIR/profiles.yml`
(`/app`), never a package's, so this cannot change any build or any grade. Same class as the existing
`_align_source_schemas_to_main` / `_vendor_dbt_utils` repairs. Result:

```
   [prune-profiles] dbt_packages/dbt_date/integration_tests/ci/profiles.yml
   [prune-profiles] dbt_packages/dbt_expectations/integration_tests/ci/profiles.yml
[ok]   inzight001 -> spider2-dbt-inzight001
[ok]   shopify001 -> spider2-dbt-shopify001
[ok]   shopify002 -> spider2-dbt-shopify002
packaged OK : 3   skipped : 0   failed : 0
```

Views: 61 → **64**. No `gold` path segment survives in any agent-facing view (checked).

The underlying razorback bug is still there and will bite any future instance that vendors a package
profile; the one-line upstream fix is to skip `dbt_packages` in that `rglob`, exactly as the packager's
own `_align_source_schemas_to_main` already does. Not applied here — razorback code is a HALT-and-escalate
surface per the workflow's autonomous-mode table. No GitHub issue opened (dispatch boundary).

### 5. Submission tooling — built, and each piece exercised

All four live in `tools/` and were run, not just written.

| Tool | What it does | Proof it works |
|---|---|---|
| `add_predicted_db_capture.py` | patches each view's `test.sh` to persist `/app/<db>.duckdb` → `/logs/verifier/predicted.duckdb`; reuses the `--predicted-db` argument already emitted so the captured file is by construction the one scored | 64/64 patched; re-run reports `already: 64`; 2-line diff; positive+negative reward controls above |
| `export_submission_bundle.py` | run-dir → `results_metadata.jsonl` + `<instance_id>/predicted.duckdb`; instance identity from `config.json` → `task.path`, **not** the trial dir name | correctly emitted `analytics_engineering001` whose trial dir is truncated to `spider2-dbt-analytics_engineerin__…`; happy path + `MISSING_ARTIFACT` + `--placeholder-for` all exercised on a synthetic run-dir and on the real spd0042 one |
| `validate_submission_bundle.py` | 10 checks: single root `*.jsonl`, exact 3-key entries, `answer_type == "file"`, paths exist and stay inside the instance folder, no dupes, no off-list ids, `danish_democracy_data001` absent, entry count, every DuckDB opens | **mutation-tested** — 6 deliberate defects injected (wrong `answer_type`, extra key, `../` traversal, danish entry, dangling path, stray `.jsonl`) and **every one of the 9 substantive checks fired**; not a tautology |
| `crosscheck_official_grader.py` | AC-4: imports the **real upstream** `eval_utils.duckdb_match` and grades against razorback's comparator — `--fuzz N` differential mode (no run needed) or `--bundle` reconciliation | see finding 6 |

Two format traps upstream's `evaluate.py` sets, both encoded in the validator:

1. `answer_type` **must** be `"file"`. The `"answer"` branch only fills `temp_scores` for
   `string_match`/`number_match` and then calls `max(temp_scores)` — on a `duckdb_match` instance the
   list stays empty, `max([])` raises, and (because the surrounding `except:` is
   `import pdb; pdb.set_trace()`) the whole evaluation drops into an interactive debugger.
2. The result dir must hold **exactly one** `*.jsonl`, named `results_metadata.jsonl` — upstream
   `assert`s it.

And one scoring subtlety worth the captain's attention: upstream's denominator is
`len(common_instance_ids)` = *gold ∩ submitted*. **Omitting an instance shrinks the denominator rather
than costing a point**, so a 64-entry bundle would report a pass rate over 64, not 68 — flattering and
wrong. Hence `--placeholder-for`: emit an EMPTY result DuckDB for an instance we could not run so it
still appears, scores 0 (`duckdb_match` fetches each `condition_tabs` table in a try/except → 0 on a
missing table), and keeps the denominator honest. Off by default; the captain decides.

### 6. AC-4 — razorback's grader vs the official one: the port holds under differential test

The FO framed this as "not obviously the same test". It is closer than that: razorback's
`benchmarks/spider2_dbt/duckdb_match.py` is a **deliberate line-by-line port** of Spider2's
`eval_utils.duckdb_match` / `compare_pandas_table` — same 1e-2 `math.isclose` tolerance, same
column-**containment** semantics (every gold column-vector must match *some* pred column-vector, extra
pred columns tolerated), same `ignore_order` sort key, same AND across `condition_tabs`, same
"predicted-table fetch raises ⇒ mismatch". It consumes the same per-instance `condition_cols` /
`ignore_orders` from the same eval line. So the two graders are *intended* to be identical; the open
question was porting fidelity, and that is testable.

**Differential fuzz** (`--fuzz`): generate random gold/pred DuckDB pairs — INTEGER/BIGINT/DOUBLE/
VARCHAR/DECIMAL/DATE/BOOLEAN columns, NULLs, empty tables, 1–2 tables, random `condition_cols` subsets,
random `ignore_orders`, and mutations spanning identical / row-shuffled / extra-pred-column /
float-perturbed-by-0.001 (inside tolerance) / perturbed-by-5.0 (outside) / row-dropped / table-missing /
single-value-changed — then grade each pair with **upstream's own imported function** and with
razorback's, and diff the verdicts. Upstream needs `google.cloud.bigquery` only for an unrelated
helper, so that one import is stubbed and the graded bytes are upstream's unmodified.

**Result — 1500 cases, 0 disagreements:**

```
$ python tools/crosscheck_official_grader.py --fuzz 1500 --seed 43
==== DIFFERENTIAL FUZZ ====
cases            : 1500 (seed 43)
agree on MATCH   : 919
agree on MISMATCH: 581
DISAGREEMENTS    : 0
```

Both verdict branches are heavily exercised (919 / 581), so this is not a vacuous all-mismatch pass; a
40-case run at the default seed 20260729 independently gave 22 / 18 / 0. **The port is faithful on
everything the fuzz can reach.** This is the cheap half of AC-4 and it needed no board; `--bundle` mode
does the real per-instance reconciliation against the same upstream function once a board exists.

Three places the two graders *could* still part company, none of which the fuzz can see, all worth
naming:

- **Table-name quoting.** Upstream interpolates `SELECT * FROM {table_name}` unquoted; razorback quotes
  the identifier. DuckDB is case-insensitive for quoted identifiers too, so this only matters for a
  table name that is a reserved word or contains special characters — where upstream would *raise* (gold
  side is not wrapped in try/except, so `evaluate.py` catches it and scores 0) while razorback succeeds.
  None of the 68 instances' `condition_tabs` need quoting today, so it is latent, not live.
- **pandas `fetchdf()` vs native `fetchall()`.** Upstream's dtype coercions (int+NULL → float64/NaN,
  DECIMAL → float64, DATE → `Timestamp`) are applied identically to gold and pred, and razorback
  normalizes `Decimal` → `float` for the same reason, so representation differences cancel. The one
  asymmetry — numpy `int64` is not a Python `int`, so upstream compares integer columns with `!=` while
  razorback routes them through `math.isclose(abs_tol=1e-2)` — is behaviourally identical for integers
  (two distinct ints differ by ≥ 1 ≫ 0.01).
- **Row order without `ignore_orders`.** Where an instance sets `ignore_orders: false`, *both* graders
  compare in unordered `SELECT *` fetch order, so both are equally exposed to DuckDB returning rows in a
  different order. That is a property of the benchmark, not a divergence — but it is a real flake source
  for any such instance.

### 7. AC-1 — two-way diff, spec vs the official 68

```
official (examples/spider2-dbt.jsonl) : 68
frozen spec benchmark.tasks           : 64

OFFICIAL \ SPEC  (in the official 68, absent from the spec):
  - airbnb002        # no gold upstream -> materializer fails closed
  - biketheft001     # no gold upstream -> materializer fails closed
  - gitcoin001       # NO SOURCE DATA upstream -> not runnable at all
  - google_ads001    # no gold upstream -> materializer fails closed

SPEC \ OFFICIAL  (in the spec, not in the official 68):
  (empty)

danish_democracy_data001 in spec: False  (MUST be False)
```

**AC-1 as written is NOT met, and cannot be met today.** One direction is clean — no extras, no
`danish_democracy_data001`. The other carries 4 documented, cause-attributed absences. Per the dispatch's
own instruction for chinook001 ("the spec carries 67 gradeable + a documented exclusion rather than a
silent 68 that errors one cell"), a spec naming views that do not exist would be a booby trap, so the
frozen spec carries **64** and the gap is recorded rather than papered over.

The 3 no-gold instances are recoverable with a razorback change (finding 9). `gitcoin001` is not
recoverable at all: no data exists to run it against.

### 8. AC-5 — configuration held and recorded

| Knob | Value | Where verified |
|---|---|---|
| `solver_workflow` | `solver_workflows/spd0038-compose-6-stabilizers` — **unforked, unedited** | frozen spec line 11 |
| `solver_workflow_content_hash` | `sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f` | frozen spec — **exact match** to the @baseline hash in the dispatch |
| `agent.kind` / `runtime` | `spacedock_solver` / `codex` | frozen spec lines 4–5 |
| `model` | `gpt-5.6-sol` | frozen spec line 6 |
| `reasoning_effort` | `xhigh` | frozen spec line 21 |
| `trials` / `concurrency.trials` | `1` / `4` | frozen spec lines 95, 97 |
| `sealed_hash` | `65b01e4bb11ff1c723b6d2908235ad1d` — **identical to spd0042's frozen spec** | agent block is byte-equivalent to spd0042's |
| `image_digest` | `sha256:224133f07cabc85c7dd8672e57d1ab9a46e5098960c5d1668918ba33df5e4742` | same as spd0042 |
| `agent_cli_hash` | `sha256:134063e133f0b4244fa3b251acf973d4fe4b4aeeacbdc135211bf480f59f1477` | same as spd0042's frozen |
| spacedock plugin | commit `ca136f83a`, `git describe` = **`v0.27.0-pre0`** | the dispatch called this "v0.26.0" — the commit matches, the tag does not; recording the commit as authoritative |

Whole-spec diff against spd0042's frozen spec with the task lists stripped:

```
2c2
< experiment: spd0042-rebaseline-gpt56sol-xhigh
---
> experiment: spd0043-official-board-64
48c48
<   harness_git_sha: db6c2e68223a21982c269f9f1f5723c784ea50d0
---
>   harness_git_sha: 62519ca9ca88bb026fdeff3f7b28771ce077d66b
```

`experiment:` is the allowed field; `harness_git_sha` is a recorded provenance fact that moves with repo
HEAD, not a knob. `solver_workflow` is *identical* in both — the standing reject-check "the full spec
differs from the anchor only in `experiment:` + `solver_workflow:`" is satisfied more strictly than
required, with `benchmark.tasks` and `model:` changing by captain-set design (the dispatch waived that
clause).

Selection confirmed foreground and free:

```
$ rk run specs/spd0043-official-board-64.frozen.yaml --runs-dir runs --explain
- Experiment: `spd0043-official-board-64`
- Tasks: `64`        - Concurrency: `4`
- Spec kind: `spacedock_solver`   - Runtime: `codex`   - Model: `gpt-5.6-sol`
```

The empty job dir `runs/spd0043-official-board-64/4455c87a5710a2cd` that `--explain` left behind was
removed, so it cannot become a stale-lock trap.

### 9. Decisions the captain owns before `full`

1. **Launch the 64 now, or wait for 67?** Recovering `airbnb002` / `biketheft001` / `google_ads001`
   needs a razorback change: `_ensure_verifier_assets` deliberately **raises** when the eval spec names
   a gold DB that is not on disk ("refusing to emit a verifier that would score against a missing
   gold — fail-closed"). The clean shape is an explicit opt-in *record-only* mode: when the eval line
   exists but the gold file does not, emit a `test.sh` that captures `/app/<db>.duckdb` and writes
   `{"reward": 0.0}` plus a `NO_LOCAL_GOLD` marker, instead of raising. Default behaviour unchanged.
   That is razorback code — HALT-and-escalate, not an ensign call. I did **not** fabricate a stand-in
   gold to get past the guard; a fake file in a gold slot is exactly what spd0010 refused to do.
2. **`gitcoin001` in the bundle or not?** It cannot be run. Including it via `--placeholder-for` keeps
   upstream's denominator at 68; omitting it shrinks the denominator and inflates the reported rate.
   Recommend including it, with the emptiness disclosed.
3. **Every view's `tests/test.sh` changed.** Precisely: 3 views were newly materialized and the other
   61 had `test.sh` patched **in place** (nothing was re-materialized). Reward-neutrality is proven
   two ways — the execution controls above, and the gatekeeper's independent reconstruction of all 64
   unpatched bodies, each byte-identical to razorback's own `_TEST_SH_TEMPLATE` with that cell's own
   `--predicted-db`. The disclosure that matters: the cells that produced spd0042's 33/60 are no longer
   byte-identical under `tests/`.
4. **Wall clock and disk.** ~64 cells at concurrency 4; spd0042 took 3h16m for 60, so ~3.5h, plus the
   predicted-DB capture (3–8 GB against 46 GB free).

### 10. AC-2 evidence scaffold — per-instance execution table (all 68, pre-filled)

`view built` / `container up` / `solver ran` / `verifier ran` / `reward`. Rows marked `pending` are the
three newly-packaged instances that have never been run — the `smoke` stage's job is exactly to turn
those into `Y`. Rows marked `BLOCKED` carry their cause.

| # | instance | view built | container up | solver ran | verifier ran | reward | evidence |
|---|---|---|---|---|---|---|---|
| 1 | `activity001` | Y | Y | Y | Y | 0 (smoke) · 1/3 post-patch · 51/53 lifetime | spd0043 smoke + canary arm A — COIN-FLIP cell on a deficient fixture |
| 2 | `airbnb001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 3 | `airbnb002` | N | BLOCKED | BLOCKED | BLOCKED | N.A. (no local gold) | materializer fails closed: no gold DB |
| 4 | `airport001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 5 | `analytics_engineering001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 6 | `app_reporting001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 7 | `app_reporting002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 8 | `apple_store001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 9 | `asana001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 10 | `asset001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 11 | `atp_tour001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 12 | `biketheft001` | N | BLOCKED | BLOCKED | BLOCKED | N.A. (no local gold) | materializer fails closed: no gold DB |
| 13 | `chinook001` | Y | Y | Y | Y | 0 (9/9 historical) | 9 prior run-dirs, all reward 0 |
| 14 | `divvy001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 15 | `f1001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 16 | `f1002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 17 | `f1003` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 18 | `flicks001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 19 | `gitcoin001` | N | BLOCKED | BLOCKED | BLOCKED | N.A. (no source data) | no source DuckDB upstream |
| 20 | `google_ads001` | N | BLOCKED | BLOCKED | BLOCKED | N.A. (no local gold) | materializer fails closed: no gold DB |
| 21 | `google_play001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 22 | `google_play002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 23 | `greenhouse001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 24 | `hive001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 25 | `hubspot001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 26 | `intercom001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 27 | `inzight001` | Y | Y | Y | Y | 0 | spd0043 smoke — FIRST execution ever, clean, legitimate miss |
| 28 | `jira001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 29 | `lever001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 30 | `marketo001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 31 | `maturity001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 32 | `movie_recomm001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 33 | `mrr001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 34 | `mrr002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 35 | `nba001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 36 | `netflix001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 37 | `pendo001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 38 | `playbook001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 39 | `playbook002` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 40 | `provider001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 41 | `qualtrics001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 42 | `quickbooks001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 43 | `quickbooks002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 44 | `quickbooks003` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 45 | `recharge001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 46 | `recharge002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 47 | `reddit001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 48 | `retail001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 49 | `salesforce001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 50 | `sap001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 51 | `scd001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 52 | `shopify001` | Y | Y | Y | Y | 0 | spd0043 smoke — FIRST execution ever, clean, legitimate miss |
| 53 | `shopify002` | Y | Y | Y | Y | **1** | spd0043 smoke — FIRST execution ever, **PASSED** |
| 54 | `shopify_holistic_reporting001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 55 | `social_media001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 56 | `superstore001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 57 | `synthea001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 58 | `tickit001` | Y | Y | Y | Y | 1 | spd0042 + spd0043 smoke — canary HELD (23/26 lifetime) |
| 59 | `tickit002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 60 | `tpch001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 61 | `tpch002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 62 | `twilio001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 63 | `workday001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 64 | `workday002` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 65 | `xero001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 66 | `xero_new001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 67 | `xero_new002` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 68 | `zuora001` | Y | Y | Y | Y | 0 | spd0042 run-dir |

Roll-up after smoke: **63** proven executable end-to-end (60 from spd0042 + the 3 newly packaged, all
three now confirmed at smoke) · **1** (`chinook001`) proven executable across 9 historical run-dirs,
structurally unscoreable locally · **3** blocked on the razorback no-gold path (captain-approved
`record-only` mode, separate dispatch) · **1** (`gitcoin001`) not runnable at all, submitted as a
disclosed placeholder. **No row is unaccounted for**, which is AC-2's bar.

### 11. AC-6 — the do-nothing floor

The known contamination was recorded as two instances: `divvy001` and `retail001` pass with **zero**
agent work — their packaged source DuckDB already satisfies their `condition_tabs`, so attempting the
task can only lose the point. `tools/check_do_nothing_passable.py` measures this for every packaged view
by feeding the verifier's own `compare_duckdb` the **unbuilt** source DB in place of the agent's built
one, so the verdict is a statement about the real scoring path, not a proxy for it.

**Swept across all 64 views, it is 8 instances, not 2:**

```
pass with zero work : 8 — divvy001, f1003, mrr001, playbook001, quickbooks003,
                          retail001, salesforce001, superstore001
```

The board's do-nothing floor is therefore **8/64 = 0.125**, and the contamination is 4× larger than the
record said. None of the three newly-added instances is do-nothing-passable (independently confirmed:
their `condition_tabs` are absent from their packaged source DBs), so this is not an artifact of the
expansion.

**The part that is worth acting on:** cross-referencing those 8 against spd0042's actual per-cell rewards,
the solver **lost 2 of the 8 free points** —

| instance | do-nothing verdict | spd0042 reward |
|---|---|---|
| divvy001, f1003, mrr001, playbook001, retail001, superstore001 | passes unbuilt | 1.0 (held) |
| **quickbooks003** | passes unbuilt | **0.0 — destroyed a free point** |
| **salesforce001** | passes unbuilt | **0.0 — destroyed a free point** |

So spd0042's 33/60 had ~2 points of pure self-inflicted loss in it: 35/60 (0.583) was available for
*less* work, not more. That is a lever-shaped finding for a later entity (a "leave an already-satisfied
target alone" precondition), and it belongs in the submission's own disclosure: the honest floor of any
score this board produces is 8 free cells, of which we have historically kept 6.

## Upstream submission format (from `evaluation_suite/README.md`)

```
<submission-folder>/
├── results_metadata.jsonl
├── <instance_id>/
│   └── result.csv   or   <name>.db / .duckdb
└── ...
```

`results_metadata.jsonl`, one JSON object per instance:
`{"instance_id": ..., "answer_type": "answer"|"file", "answer_or_path": ...}`

Graded by `python evaluate.py --result_dir <folder> --gold_dir gold`. Match functions:
`number_match`, `string_match`, `table_match`, `duckdb_match`. spider2-dbt instances are DuckDB
projects — the sampled gold (`gold/divvy001/divvy.duckdb`) is a duckdb file, so these are
`duckdb_match` / `table_match`, i.e. `answer_type: "file"`.

## Configuration (captain-set)

| Knob | Value |
|---|---|
| solver_workflow | `@baseline` = `solver_workflows/spd0038-compose-6-stabilizers`, UNCHANGED (hash `sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f`) |
| model | `gpt-5.6-sol` |
| reasoning_effort | `xhigh` |
| benchmark.tasks | all 68 official instances |
| trials | 1 |

Same configuration as spd0042 (which scored 33/60 on the 60-task board), expanded to 68 tasks.

## Acceptance criteria

**AC-1 — All 68 official instances are in the frozen spec.** A diff of the frozen spec's
`benchmark.tasks` against the 68 `instance_id`s in `examples/spider2-dbt.jsonl` is EMPTY in both
directions, and `danish_democracy_data001` is absent.
Verified by: the diff command + its output pasted into the entity.

**AC-2 — Every one of the 68 is proven EXECUTABLE by razorback, individually.** Presence in a spec is
not execution. For each instance: the view materializes, the container comes up, and the solver runs
to a result. For the 64 with local gold the verifier must also return a reward. For the 4 Group-B
instances, execution + production of an answer artifact is the bar, and the missing local gold is
recorded as expected rather than as a failure.
Verified by: a per-instance execution table (instance / view built / container up / solver ran /
verifier ran / reward-or-N.A.) covering all 68, with no row unaccounted for.

**AC-3 — The submission bundle conforms to the documented format.** `results_metadata.jsonl` has
exactly 68 entries with the three required keys, every referenced artifact path exists relative to
its instance folder, and no extra instances are present.
Verified by: a validator run over the bundle whose output is pasted in.

**AC-4 — Independent cross-check with the OFFICIAL evaluator.** `evaluation_suite/evaluate.py` is run
against our bundle for the 64 locally-gradable instances, and its per-instance verdicts are reconciled
against razorback's own per-cell rewards. Every disagreement is named instance-by-instance with a cause.
This is the check that can actually falsify our whole grading pipeline — a silent divergence here means
every score this workflow has recorded was measured against a grader that differs from the leaderboard's.

**AC-5 — Configuration held and recorded.** Solver README byte-identical to `@baseline` (hash match),
`model: gpt-5.6-sol`, `reasoning_effort: xhigh`; spacedock plugin commit and `codex --version` /
`agent_cli_hash` captured at launch.

**AC-6 — Known contamination disclosed.** The do-nothing-passable finding (divvy001, retail001 pass
with zero work and penalise attempting) is restated, and the 8 newly-added instances are checked for
the same property so the submission's own floor is known.

## Known risks

- **chinook001's exclusion may be load-bearing.** spd0010 excluded it as goldless; gold now appears to
  exist. If the real cause was a broken/unbuildable fixture, re-including it could error the cell.
  Diagnose before assuming stale.
- **Group B produces unverifiable answers.** We cannot know locally whether those 4 are right.
- **Grader divergence (AC-4) is the highest-value unknown.** razorback grades an exact-named output
  table vs gold; the official suite uses `duckdb_match`/`table_match` with per-instance
  `condition_cols` / `ignore_order` parameters. These are not obviously the same test.
- **Wall clock** ~68 cells at concurrency 4, ~3.5-4h based on spd0042's 3h16m for 60.
- **Auth**: spd0042 attempt 1 lost 41 cells to a codex `refresh_token_reused` race. Re-check auth
  immediately before launch and watch for the first errored cell.

## Pre-smoke Decision-Fork Probe

N/A as a lever probe. The riskiest mechanism is instead exercised FIRST per the probe discipline:
packaging + single-instance execution of the 8 new instances (the `smoke` stage) is the smallest run
that would invalidate this entity if it broke, and it precedes the 4-hour board.

## Gatekeeper review

**Recommendation: APPROVE** — no FAILs on any applicable rule; the entity is a coverage/deliverable
entity, the solver is provably unforked and byte-identical to `@baseline`, the frozen spec differs from
the spd0042 anchor only in `experiment:` + the captain-waived `benchmark.tasks` + the
provenance-tracking `harness_git_sha`, the comparator/scorer is untouched, no gold reaches the agent, and
every falsifiable number in the body reproduced against the filesystem and run history.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-07-29.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).
Transcribed verbatim by the propose ensign (the gatekeeper was run read-only so it could not race the
ensign's own edits to this file).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | **N/A (verified-as-empty)** | No fork exists by design; an empty README diff is the *requirement* here, so the "empty diff ⇒ FAIL" clause is inapplicable. Verified instead: `agent.solver_workflow: solver_workflows/spd0038-compose-6-stabilizers` (frozen spec L11), dir holds exactly one file (`README.md`, 34738 B), `git status --porcelain -- spider2-dbt/solver_workflows` is **empty** (last touching commit `d95880e`, the spd0038 ideate). Recomputed razorback's `_dir_content_hash` (`spec/freeze.py:64`) over that dir: `sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f` — **exact match** to the spec's `solver_workflow_content_hash`, to `provenance.solver_workflow_hash`, and to the `@baseline` run's recorded hash (`runs/spd0038-compose-6-stabilizers-full/fb10902ab7d9ffa7/config.json:81`). `rk registry resolve run @baseline` → that same run-dir, whose `spec.frozen.yaml:11` names the same dir. Parent resolution agrees with `source:`. |
| G2 leak-guard (hidden gold) | **PASS** | (a) README unforked and hash-identical, so no added prose exists to leak gold or soften no-fetch text. (b) 3 new views: `find _views/spider2-dbt-{inzight001,shopify001,shopify002} -path '*gold*'` → **zero hits** (razorback's `gold/`-dir prune, `harbor_view.py:287-296`). (c) Gold ships as `tests/<db>.duckdb` (`cmp` → byte-identical to `evaluation_suite/gold/<inst>/<db>.duckdb` for all 3), and `tests/` is uploaded **only at verify time** (`harbor/verifier/verifier.py:133-138`; `harbor/models/task/paths.py:23`), i.e. after the agent phase. `environment/` build context copies only `dbt_project/` + the preflight script — **no `COPY tests`**. (d) The agent-facing DB is provably the *unbuilt* source: `_views/…/dbt_project/<db>.duckdb` is `cmp`-identical to `examples/<inst>/<db>.duckdb`, and none of the graded `condition_tabs` exist in it (`inzight001` needs `mrt_capacity_tariff`; `shopify001` needs `shopify__products`,`shopify__daily_shop`; `shopify002` needs `shopify__discounts` — all absent) ⇒ no gold leak **and** none of the 3 is do-nothing-passable. (e) The only `gold`-token hits in agent-facing trees are vendored dbt-package CI fixtures, pre-existing upstream content with no spider2 answer data. |
| G3 spec two fields | **PASS** | Full frozen-vs-anchor diff yields exactly three kinds of hunk: `experiment:` (allowed), `benchmark.tasks` (+4, captain-waived), `provenance.harness_git_sha: db6c2e68… → 62519ca9…` — and `62519ca9…` **is** `git -C /home/kent/autobench rev-parse HEAD`, a recorded provenance fact, not a knob. Task delta is pure addition: `spd0043 \ spd0042 = {chinook001, inzight001, shopify001, shopify002}`, `spd0042 \ spd0043 = {}`. Knobs re-verified by YAML parse: `kind spacedock_solver`, `runtime codex`, `model gpt-5.6-sol` (**unchanged** from the anchor), `reasoning_effort xhigh`, `trials 1`, `concurrency.trials 4`, `benchmark.kind harbor-local`, `tasks_root` unchanged. `sealed_hash 65b01e4b…`, `image_digest sha256:224133f0…`, `agent_cli_hash sha256:134063e1…` all **identical** to the anchor (absent from the diff entirely). 64 tasks, 64 unique, all 64 view dirs exist, `danish_democracy_data001` absent. |
| G4 smoke narrows tasks only | **N/A** | No smoke spec by design — `smoke` here means executing the 3 newly-packaged instances, not a targets+canaries subset. `ls specs/spd0043*` shows only the full + frozen pair. No `exclude_tasks` anywhere. |
| G5 both frozen | **PASS (the "both" half N/A)** | Only one spec exists by design. `specs/spd0043-official-board-64.frozen.yaml` present (3288 B) carrying `kind: spacedock_solver` (L4) + `runtime: codex` (L5). Freeze is clean: pre-freeze→frozen adds only the ABOUTME strip, path normalisation, `solver_workflow_content_hash`, `sealed_hash`, and the 5 pinned provenance fields — no knob moved. `--explain`'s empty job dir was genuinely removed (`runs/spd0043-official-board-64/` does not exist), so no stale-lock trap. |
| G6 resolver fidelity | **PASS** | No inserted text to diverge; the substituted check is whether the artifacts match the stated operational claim and whether the body overclaims. They match, and it does not — see X4. |
| G7 actionability/inert-risk | **N/A** | Advisory rule about instruction wording; no instruction changed. |
| G8 regression-canary coverage | **N/A** | Lever mechanics; no instruction, generative or gated, exists. (The nearest analogue — the `test.sh` patch firing on all 64 views — is audited in X3 and is reward-neutral by construction.) |
| G9 selector independence | **N/A** | No multi-candidate/selector protocol declared. |
| G10 self-correcting false-positive | **N/A** | No validate-and-fix lever declared. |

### Supplementary integrity rows (the real risk surface for this entity)

| Check | Verdict | Evidence |
|------|---------|----------|
| **X1 — comparator/scorer untouched** | **PASS** | `git -C razorback status --porcelain` → `M uv.lock` only; `git diff --stat` → `uv.lock | 4 ----`. `git status --porcelain -- src/razorback/benchmarks/spider2_dbt/` is **empty**; last commits touching `duckdb_match.py`/`eval_spec.py`/`verify.py` are `f35a13b`/`6c76cbe`/`0ce7d51`, all pre-dating this cycle (mtime 2026-06-19). The 5 new `tools/` scripts import the comparator **read-only** and write nothing outside a bundle `--out` dir or a `tempfile.TemporaryDirectory()`. The one packager edit (`_prune_vendored_profiles`, +32/-0) stays inside `tools/`. |
| **X2 — `_prune_vendored_profiles` blast radius** | **PASS** | Deletes `profiles.yml` only under the staged copy's `dbt_packages/`. Independently confirmed only 3 instances are affected: `find _views -path '*dbt_packages*' -name profiles.yml` → **0 hits**, while all **64/64** views still have their own `dbt_project/profiles.yml` and all 64 declare `duckdb`. `view_manifest.json` mtimes show only **3** views re-materialized on 2026-07-29 (61 still 2026-06-24). dbt reads only `$DBT_PROFILES_DIR=/app/profiles.yml`, never a package's, so this cannot change a build or a grade. |
| **X3 — `test.sh` patch reward-neutrality** | **PASS (with a WARN note)** | Reconstructed the unpatched body for **all 64** views by deleting exactly the marker line and the following `cp`, and compared against razorback's `_TEST_SH_TEMPLATE` (`harbor_view.py:58-66`) rendered with each view's own `--predicted-db`/`--gold-db`: **64/64 byte-identical**, one marker and one `cp` per file, and in every case the `cp` source is *the same path* as `--predicted-db`. Nothing there can change a reward: the source is read-only, the destination does not collide with `--reward-out`, and `\|\| true` neutralises `set -eu`. Nothing there can leak gold: `test.sh` runs only in the verify phase after the agent is gone, and the captured file is the *agent's own build*. Gold DBs in `tests/` untouched (mtime 2026-06-22 across all 64). **WARN:** the copy lands on the host bind-mount — 4 concurrent cells at up to 334 MB each against 46 GB free is bounded but not free; a verify-time ENOSPC would surface as a failed `reward.json` write, not a silent mis-score. |
| **X4 — honesty of the record** | **PASS** | Every falsifiable number reproduced. (i) `AC-1 NOT met` is stated plainly, twice, and the frozen spec carries 64 rather than a booby-trapped 68 — independent two-way diff gives `OFFICIAL \ SPEC = {airbnb002, biketheft001, gitcoin001, google_ads001}`, `SPEC \ OFFICIAL = {}`, danish absent: **identical** to finding 7. (ii) Blocked-cause spot-checks hold: `examples/gitcoin001/` contains **no `.duckdb` at all** ⇒ "no source data" true; `airbnb002`/`biketheft001`/`google_ads001` each have a source `.duckdb` but **no** `evaluation_suite/gold/<inst>/` dir ⇒ "no upstream gold" true. (iii) chinook001: gold DB exists and opens, holds the 11 raw Chinook tables, and **all three** `condition_tabs` are absent ⇒ exclusion valid not stale; "9 of 9 run-dirs, reward 0.0" reproduces exactly. (iv) The 68-row AC-2 table has 68 unique ids **set-equal to the official 68**, and its reward column reproduces spd0042's `per_trial_outcomes.json` **cell-for-cell with zero mismatches** (33 ones + 27 zeros = 60, sum 33.0). (v) All 68 eval lines are `func: duckdb_match` — confirmed. (vi) Disk/size claims exact: `46G` avail / 82% used; 65 golds, 2.43 GB, avg 37 MB, max 334 MB. (vii) Re-ran the AC-4 differential fuzz independently (`--fuzz 40`, default seed): **22 MATCH / 18 MISMATCH / 0 DISAGREEMENTS** — the entity's number, reproduced. **Three precision nits, none an overclaim:** the 1500-case fuzz was cited via a dangling forward reference; the reward-neutrality table shows no *pre-patch* measurement for the negative control (the 64/64 byte-identity check covers it more strongly); and captain-decision #3's "re-materialising 64 views" was looser than reality (3 re-materialized, 61 patched in place). `score: 0.95` in the front-matter is the entity-quality field, not a benchmark result. |

**For the captain:** Auto-approved to `smoke`, whose only job is to execute `inzight001`/`shopify001`/
`shopify002` for the first time — the ~3.5 h 64-cell board and your two open decisions (launch 64 now vs
wait for a razorback record-only mode to recover the 3 no-gold instances; `--placeholder-for gitcoin001`)
are still yours before `full`. Two things to hold when the board lands: `chinook001` is now *on* the board
and is a guaranteed 0, so `rk`'s headline reads as N/64 while the honest local denominator is 63; and the
61 pre-existing views' `tests/test.sh` were patched in place, so spd0042's cells are no longer
`tests/`-byte-identical (reward-neutral — all 64 unpatched bodies verified byte-identical to razorback's
own template, every `cp` source equal to that cell's `--predicted-db`). Watch verify-time disk.

**Ensign follow-up on the three nits (all fixed before this block was written):** the dangling fuzz
reference now carries the completed 1500-case result (919 MATCH / 581 MISMATCH / **0 disagreements**);
captain-decision #3 now states the 3-re-materialized / 61-patched-in-place split; and the
reward-neutrality claim now cites the gatekeeper's 64/64 byte-identity reconstruction alongside the
execution controls.

## Smoke result

Run: `runs/spd0043-official-board-64-smoke/c5b797acd42d2e6b` (handle
`runs/.rk-handles/spd0043-smoke-20260729-061045`, rc=0, 06:10:45 → 06:43:01 = **32 min**).
Strict audit **CLEAN** — `0` findings, `taint_status: clean` on every cell, `stratified_n_errored: 0`,
`stratified_n_completed: 5`, `stratified_pass_at_1: 0.4` (2/5).

**Verdict: NO-GO on the canary, GO on everything the smoke was built to prove.** The canary drop is
real and is NOT the capture patch — root cause below is a solver-side classification flip, evidenced by
the solver's own transcript against the passing run's transcript.

| Cell | Role | Reward | Historical | Captured predicted DB | Read |
|---|---|---|---|---|---|
| `inzight001` | 🎯 target, first execution ever | 0.0 | — | 2.9 MB | executed clean; legitimate miss (bar was execution) |
| `shopify001` | 🎯 target, first execution ever | 0.0 | — | 22.6 MB | executed clean; legitimate miss |
| `shopify002` | 🎯 target, first execution ever | **1.0** | — | 19.7 MB | **PASSED on first execution** — a genuinely new board point |
| `tickit001` | ✅ canary | 1.0 | 23/26 | 67.6 MB | HELD; also proves capture at real scale |
| `activity001` | ✅ canary | **0.0** | **50/51** | 9.2 MB | **DROPPED** — see the failure review |

Two of the three newly-packaged official instances execute and miss; one passes outright. All three are
now proven executable end-to-end, which was the stage's first question.

### AC-3 mechanism proof — the capture works in production

The propose finding was 0/60 exportable. On this run: **5/5**.

```
$ python tools/export_submission_bundle.py --run-dir <smoke-run-dir> --out <bundle>
activity001   ok  reward 0, 9187328 bytes      shopify002  ok  reward 1, 19673088 bytes
inzight001    ok  reward 0, 2895872 bytes      tickit001   ok  reward 1, 67645440 bytes
shopify001    ok  reward 0, 22556672 bytes
results_metadata.jsonl entries: 5  (exported 5, placeholder 0)   not exported: 0
```

Bundle shape is exactly the documented layout — `results_metadata.jsonl` at the root plus one
`<instance_id>/predicted.duckdb` per cell — and every entry carries only the three required keys:

```json
{"instance_id": "shopify002", "answer_type": "file", "answer_or_path": "predicted.duckdb"}
```

Validator: **10/10 PASS** (`--expect 5`), including `answer_type == "file"` everywhere, every referenced
path existing inside its own instance folder, no off-list ids, `danish_democracy_data001` absent, and
every submitted DuckDB opening and querying cleanly.

Measured capture sizes (grounding the 67-cell projection in measurement rather than the earlier
estimate): 2.9 / 9.2 / 19.7 / 22.6 / 67.6 MB — mean **24.4 MB**, and `tickit001` at 67.6 MB is 2× the
gold-file mean, so a 67-cell board projects to roughly **1.6 GB**, comfortably inside the 46 GB free.
The earlier 3–8 GB estimate was pessimistic.

### AC-4 on live data — the two graders agree cell-for-cell

First time the official grader and razorback's have seen a real solver artifact rather than synthetic pairs:

```
instance                              official  razorback  note
activity001                                  0          0
inzight001                                   0          0
shopify001                                   0          0
shopify002                                   1          1
tickit001                                    1          1
DISAGREEMENTS  : 0        not gradeable locally: 0
```

This is stronger than the fuzz because the artifacts are real and heterogeneous: a 172,456-row × 20-col
`fct_sales` (tickit001), a 3-row × 42-col `shopify__discounts` (shopify002), and three genuine misses —
one of which (`activity001`) is a *missing-table* miss, exercising the branch where the predicted-table
fetch raises and both graders must return 0 rather than crash. Combined with the 1500-case fuzz, AC-4 is
satisfied on both synthetic and live evidence.

Operational note for the 67-cell cross-check: upstream's grader is **slow** on wide/tall tables — it does
`fetchdf().transpose().values.tolist()` and then Python-sorts every gold column-vector against every pred
column-vector, so tickit001 alone burned ~4 min of CPU at 610 MB RSS. Budget ~10-15 min for a 67-cell
reconciliation, and do not run it inside a 120 s foreground call.

## Run result

**COMPLETE — launched 2026-07-30 05:06:33, finished 09:03:48 (+0800). 3 h 57 m 15 s. 67/67 completed,
`n_errored_trials: 0`, zero `exception.txt`, all 67 `verifier/predicted.duckdb` captured.
`stratified_pass_at_1 = 0.47761194` = 32/67 on an UNCENSORED denominator (`stratified_n_errored: 0`).
Per-cell wall clock 493–1581 s, so the 3 h 57 m is the healthy signature, not a fast-fail.**

Headline, and the honest denominators — see `## Behavioral analysis` for why the raw rate is NOT
comparable to spd0042's 33/60:

| denominator | rate | what it means |
|---|---|---|
| **32/67 = 0.4776** | raw board, razorback's grader | every executed cell, including 4 that cannot be scored locally |
| **33/67 = 0.4925** | raw board, **the OFFICIAL grader** | AC-4 found razorback under-scores mrr002 — see AC-4 below. **This is the number to quote for a leaderboard claim.** |
| **32/63 = 0.5079** | locally gradeable (razorback) | drops chinook001 + the 3 record-only cells (structural zeros) |
| **33/61 = 0.5410** | locally gradeable (official) | the 61 cells upstream's grader can actually resolve gold for |
| **30/61 = 0.4918** | minus do-nothing-passable | razorback's grader, also dropping divvy001 + retail001 (K1: both reward inaction; both passed here) |
| **33/68 = 0.4853** | as SUBMITTED (floor) | upstream's denominator + upstream's grader; gitcoin001 an empty placeholder |
| **up to 37/68 = 0.5441** | as submitted (ceiling) | if the leaderboard's real gold credits all 4 no-gold answers |
| 32/65 = 0.4923 | minus the 1 infra abort | google_play002 did no work (below) |

`rk audit --policy strict`: **66 clean / 0 tainted / 1 coverage_missing**, and the single coverage_missing
cell is `google_play002` (`spacedock_dispatch_events_absent`, `captured: 0`) — the same cell that turns
out to be an infra abort. For contrast, spd0042 carried 5 `coverage_missing`. No leak findings anywhere.

| | |
|---|---|
| handle | `runs/.rk-handles/spd0043-full-20260730-050626/` |
| job dir | `runs/spd0043-official-board-67/4de20bed438d4d51` |
| PID | `881538` (worker; `pid` file is authoritative) |
| spec | `specs/spd0043-official-board-67.frozen.yaml` — **67** tasks, concurrency 4, trials 1 |
| ntfy | `adebench-rk-381c976fe07465bf` |
| ETA | **~3.5–4 h** → ~08:40–09:10 +0800. spd0042 ran 60 cells in 3h16m at the same concurrency; 67 cells scales to ~3.65 h, plus predicted-DuckDB capture I/O. |

Launch-time liveness confirmed (not just "rc=0 and a handle"): at T+3.5 min the worker PID was alive, the
job dir held `lock.json` + 4 cell dirs, 4 solver containers were `Up`, and `job.log` showed the composed
solver prompt reaching the agent. `spider2-dbt-airbnb002__tDnaLZG` — one of the three new record-only
cells — is in that first batch of four and its container came up, so the new packaging path is exercised
in production from the first minute.

**Failure signature to check before ANY score** (spd0042 attempt 1 lost 41/60 cells to an invisible
`refresh_token_reused` race): read `n_trials_errored` in `result.json` first. `stratified_pass_at_1`
censors errored cells out of its denominator, so a high-looking rate on a censored board is not a score.
A finish materially under ~3 h is a FAILURE signature, not speed.

### AC-5 — configuration captured AT LAUNCH

| Knob | Value at launch | How captured |
|---|---|---|
| spacedock plugin — `git describe --tags` | `v0.27.0-pre0` | `git -C spacedock describe --tags` |
| spacedock plugin — commit | `ca136f83a579fd44c223321ae7f8fe7785c685f7` | `git -C spacedock rev-parse HEAD` |
| spacedock plugin — worktree | **clean** (`status --short` empty), detached HEAD (no branch) | `git -C spacedock status --short` |
| **razorback — branch** | `spd0043-record-only-no-local-gold` | `git -C razorback branch --show-current` |
| **razorback — commit** | `027bb95` ("prune empty gold/ dirs on the record-only path too"), atop `26a0696` ("opt-in record-only verifier for instances with NO local gold"), branched from `9232cbb` | `git -C razorback log --oneline` |
| razorback — worktree | one stray uncommitted `M uv.lock` (4 deleted lines), deliberately NOT committed and NOT pushed; no effect on the grading path | `git -C razorback status --short` |
| `codex --version` | `codex-cli 0.145.0` | — |
| `codex login status` | `Logged in using ChatGPT` — **re-checked at the launch instant**, in the same command as the launch | — |
| docker | server `29.5.2`, zero running containers pre-launch (no stale cell) | `docker info` / `docker ps` |
| disk free | **43 GB** on `/` (242 G, 83% used) before launch; measured record-only captures ran 2.9–67.6 MB, so 67 cells is comfortably inside budget | `df -h` |
| in-flight runs | none — every prior `.rk-handles/*/` carries a terminal `done` sentinel | handle sweep |

**Why razorback's SHA is recorded here and nowhere else.** The frozen spec pins the solver README, the
image digest, the agent CLI hash and `harness_git_sha` (the *autobench* repo), but nothing in it records
which razorback revision graded the board. For this board razorback is a genuine independent variable —
it carries the record-only verifier that makes 3 of the 67 cells exist at all — so the branch and commit
belong in the provenance record explicitly.

`harness_git_sha` frozen into the spec is `ccda85a73a2cb0d5d8ca0e3e3a92113962054020` (the recovery
commit). Repo HEAD then advanced by one commit — the spec-pair commit `6bbed4d` — which is expected:
`harness_git_sha` records HEAD at freeze time, and the spec cannot contain the hash of the commit that
adds it.

### AC-1 — two-way diff at 67 tasks (re-freeze)

```
official (examples/spider2-dbt.jsonl) : 68  (unique 68)
frozen spec benchmark.tasks           : 67  (unique 67)

OFFICIAL \ SPEC  (in the official 68, absent from the spec):
  - gitcoin001

SPEC \ OFFICIAL  (in the spec, not in the official 68):
  (empty)

danish_democracy_data001 in spec: False  (MUST be False)
chinook001 in spec:   True
airbnb002 in spec:    True
biketheft001 in spec: True
google_ads001 in spec: True
```

`gitcoin001` is now the **only** `OFFICIAL \ SPEC` entry — it ships in the bundle as a disclosed
`--placeholder-for` entry (no source DuckDB exists upstream), which holds the reported denominator at
upstream's 68 instead of quietly shrinking it. The three former no-gold absences are in. The spec's 67
task slugs match the 67 materialized views under `_views/` exactly — set difference empty in both
directions, so no cell can error on a missing view.

Configuration held against the anchor — whole-spec diff vs `spd0042-rebaseline-gpt56sol-xhigh.frozen.yaml`
with both task lists stripped:

```
2c2
< experiment: spd0042-rebaseline-gpt56sol-xhigh
---
> experiment: spd0043-official-board-67
48c48
<   harness_git_sha: db6c2e68223a21982c269f9f1f5723c784ea50d0
---
>   harness_git_sha: ccda85a73a2cb0d5d8ca0e3e3a92113962054020
```

Nothing else moved: `solver_workflow: solver_workflows/spd0038-compose-6-stabilizers` with
`solver_workflow_content_hash: sha256:607dec2920bce80739fe7fe40ab9627074ef29cff74e364c913fba485184011f`
(the @baseline README, byte-identical), `sealed_hash: 65b01e4bb11ff1c723b6d2908235ad1d` (identical to
spd0042), `model: gpt-5.6-sol`, `reasoning_effort: xhigh`, `trials: 1`, `concurrency.trials: 4`,
`max_turns: 200`, `override_timeout_sec: 2400.0`.

Selection confirmed foreground and free before launch:

```
$ rk run specs/spd0043-official-board-67.frozen.yaml --runs-dir runs --explain
- Experiment: `spd0043-official-board-67`
- Job name:   `4de20bed438d4d51`
- Tasks: `67`        - Concurrency: `4`
- Spec kind: `spacedock_solver`   - Runtime: `codex`   - Model: `gpt-5.6-sol`
```

The empty job-dir tree `runs/spd0043-official-board-67/` that `--explain` left behind was removed before
launch, so no stale `lock.json` could sit on the path. The real run then re-created the *same* job name
`4de20bed438d4d51` (it is the frozen spec's content hash) — which is why deleting it mattered rather than
being cosmetic.

## Submission bundle — THE DELIVERABLE

```
/home/kent/autobench/spider2-dbt/runs/_submissions/spd0043-official-68/
```

**68 entries. 4.35 GiB logical.** Layout is exactly upstream's: `results_metadata.jsonl` at the root plus
one `<instance_id>/predicted.duckdb` per entry.

```
$ python3 tools/export_submission_bundle.py \
    --run-dir runs/spd0043-official-board-67/4de20bed438d4d51 \
    --out runs/_submissions/spd0043-official-68 --placeholder-for gitcoin001
==== EXPORT SUMMARY ====
results_metadata.jsonl entries: 68  (exported 67, placeholder 1)
not exported        : 0
```

```
$ python3 tools/validate_submission_bundle.py --bundle runs/_submissions/spd0043-official-68 \
    --spider2-root /home/kent/Spider2/spider2-dbt
[PASS] 1. exactly one root *.jsonl, named results_metadata.jsonl — found ['results_metadata.jsonl']
[PASS] 2a. every line parses as a JSON object
[PASS] 2b. every entry has exactly the 3 required keys
[PASS] 3. answer_type == "file" everywhere
[PASS] 4a. every answer_or_path is a relative path inside its instance folder
[PASS] 4b. every referenced artifact exists
[PASS] 5a. no duplicate instance_ids
[PASS] 5b. no ids outside the official list
[PASS] 5c. danish_democracy_data001 absent (has gold, not official)
[PASS] 5d. entry count == 68 — got 68
[PASS] 6. every submitted DuckDB opens and is queryable
==== VALIDATION SUMMARY ====
entries : 68 (official set: 68, expected: 68)   failures: 0     [exit 0]
```

**Disk, plainly.** The 68 DuckDBs total **4.35 GiB** (mean 65.5 MB, median 18.8 MB) but the bundle
consumed **~0 additional bytes**: the exporter's default `--copy-mode hardlink` links each file to the
run-dir capture on the same filesystem (verified: `stat` shows link count 2 on `tickit001`, 1 on the
freshly-created `gitcoin001` placeholder). Free space was 39 GB before and after. Two consequences the
captain should know: deleting the run-dir will NOT damage the bundle (`rm` only unlinks), and
`tar`/`zip`/`rsync` of the bundle will materialize the full 4.35 GiB.

The size distribution blew well past the smoke-stage projection. Smoke measured 2.9–67.6 MB and projected
~1.6 GB for 67 cells; the real spread is **1.8 MB (mrr002) to 1530 MB (biketheft001)**, with airbnb002 at
526 MB and airbnb001 at 429 MB — three cells carry 2.4 GiB of the 4.35. Two of those three are the new
record-only instances, which had never been captured before. The projection was not wrong about the
typical cell; it was wrong because the tail is two orders of magnitude wide.

### The four cells that score 0 locally but carry a real answer

This is a stated **upside**, not a ceiling. Each of these has its required answer tables populated in the
submitted DuckDB; the local 0.0 is an absence of gold on our side, not a wrong answer:

| instance | why 0.0 locally | answer actually submitted |
|---|---|---|
| chinook001 | its gold DB exists but contains **none** of `dim_customer` / `fct_invoice` / `obt_invoice` | all three present: 60 / 412 / 412 rows |
| airbnb002 | no gold DuckDB upstream (record-only) | `src_hosts` 14,111 rows; `wow_agg_reviews` 3 rows |
| biketheft001 | no gold DuckDB upstream (record-only) | `fact_theft_reports` 59,380 rows |
| google_ads001 | no gold DuckDB upstream (record-only) | `google_ads__campaign_report` 16 rows; `google_ads__keyword_report` 15 rows |
| gitcoin001 | no source data upstream — never ran | **nothing** — empty DB by construction, can only score 0 |

The leaderboard holds the true gold for the first four, so the submitted score sits in
**[32/68 = 0.4706, 36/68 = 0.5294]**. gitcoin001 is a permanent 0 and is disclosed as such.

## Behavioral analysis

### 1. Net, and the full per-cell ledger in both directions

`stratified_pass_at_1` **0.4776** (32/67, Wilson CI [0.3625, 0.5951], `n_errored 0`) against
`@baseline = runs/spd0038-compose-6-stabilizers-full/fb10902ab7d9ffa7`. The paired instrument is the
comparison that carries information, and the right partner is **spd0042** — the byte-identical
configuration (same README hash, same model, same effort), not `@baseline` (a different model on a
plugin/CLI environment that no longer exists).

Raw paired read on the 60 shared cells: **33 → 31, net −2**, 8 discordant (3 gains, 5 regressions).

**Corrected paired read.** One cell on each board had a solver that never ran at all (below), so those
cells measure infrastructure, not the configuration. Excluding both:

**58 work-doing shared cells: 32 → 31, net −1.** 3 gains, 4 regressions, 7 discordant,
**McNemar exact two-sided p = 1.0000**.

**And once the one known grader defect is corrected on the side where it is measurable, net = 0.** mrr002
is a razorback false-negative (AC-4); the official grader scores it 1, so it is concordant with spd0042,
not a regression. That leaves **32 → 32, net 0, 3 gains / 3 regressions, 6 discordant, p = 1.0000**.
Stated with its own asymmetry: I can re-grade spd0043 with the official grader because this is the first
board with captures, and I cannot do the same for spd0042, so the correction is applied to one side only
and mildly favours spd0043. The conclusion does not move either way — −1 and 0 are the same null.

| direction | cell | prior pass-rate (this program, excl. this board) | mechanism |
|---|---|---|---|
| GAIN | intercom001 | **0/26** | **first pass ever recorded** — see §4 |
| GAIN | airport001 | 2/14 (14%) | churn on an unstable cell |
| GAIN | quickbooks003 | 21/34 (62%) | churn on a coin-flip cell |
| REGR | google_play001 | 48/52 (92%) | union-completeness miss — built 10 of 32 / 10 of 20 required rows |
| ~~REGR~~ | mrr002 | 20/21 (95%) | **NOT A REGRESSION — razorback grader defect.** The official grader scores it **1**. See AC-4. |
| REGR | superstore001 | 1/22 (5%) | reversion to its own norm; spd0042 was its only prior pass |
| REGR | tickit002 | 4/24 (17%) | reversion to its own norm |
| (excluded) | google_play002 | 30/31 (97%) | **INFRA — no worker ran**, 2 m 32 s |
| (excluded) | scd001 | — | spd0042's own no-work abort |

Against the K2 yardstick (15.8% same-config per-cell churn ⇒ ~9.2 expected discordant on 58 cells,
binomial 95% range ≈ 4–15), **7 observed discordant is textbook churn** and a net of −1 with p = 1.0000 is
as null as this instrument can report.

**Say the consequence plainly: this board does NOT show a regression from the `test.sh` capture patch or
from the razorback record-only change.** Both landed between the two boards, so a careless reader will
blame them — and the data does not support that. Three independent reasons: the net is −1 on a
p = 1.0000 instrument; the capture patch is reward-neutral by construction (below); and the record-only
path only touches the 3 cells that have no gold, none of which existed on spd0042.

The reward-neutrality argument, stated precisely from the emitted `test.sh` rather than from memory — the
`cp` runs **before** `verify.py`, not after:

```sh
mkdir -p /logs/verifier
cp /app/mrr.duckdb /logs/verifier/predicted.duckdb || true      # <-- the patch
python /tests/verify.py --predicted-db /app/mrr.duckdb --gold-db /tests/mrr.duckdb \
  --eval-spec /tests/spider2_eval.jsonl --reward-out /logs/verifier/reward.json
```

It is still neutral, but for two different reasons than ordering: it only **reads** `/app/<db>.duckdb` and
writes to a different path, so the graded artifact is untouched; and `|| true` under `set -eu` means a
failed copy cannot abort the script before the verifier runs. The one residual coupling worth naming
honestly: the copy consumes disk, so on a full filesystem it could starve `verify.py`. That did not happen
here (85% used / 39 GB free at the end, and all 67 verifiers produced a reward), but it is the mechanism to
check first if a future board shows unexplained verifier failures.

### 2. Was the change executed? (confound attribution)

There was no README lever this cycle — the solver README is byte-identical to `@baseline`
(`sha256:607dec29…`), and spd0042 already carried the model swap. So for every moved cell the honest
classification is **neither executed-and-helped nor executed-and-hurt but same-configuration variance**:
the only differences between the two boards are the task set, the reward-neutral capture patch, and the
draw. Attributing any of these 7 flips to a lever would be inventing a cause. The one durable
artifact-level finding is intercom001's reachability (§4).

### 3. The regressions, judged as damage — and one that is not a regression at all

Two of the four regressions (superstore001 1/22, tickit002 4/24) are **not damage to working answers**:
those cells are chronic failures whose spd0042 pass was the outlier. Calling them regressions inverts the
base rate.

Two are real breakage of high-reliability passers, and both have a concrete mechanism read off the
committed artifact:

- **google_play001** (prior 48/52). Column sets are exactly right; row counts are not.
  `google_play__device_report` has 10 rows against gold's 20, and PRED's rows are a strict **subset** of
  gold's — same dates, same devices, half the rows. `google_play__country_report` has 10 rows against 32,
  spanning 10 dates / 9 countries against gold's 22 / 27, and the two sets barely overlap (PRED is all
  2017-12, gold starts 2017-02). The fixture ships the per-country and per-device facts split across
  several ~10-row source tables (`stats_installs_country` 10, `stats_ratings_country` 12,
  `stats_store_performance_country` 10 — and 10+12+10 = **32**, gold's exact row count; 10+10 = **20** for
  device). The solver built each report from a **single** source table instead of combining all of them.
  Distance to pass: 22 missing country rows and 10 missing device rows, zero schema error. This is the
  program's familiar completeness failure family, not a new one.
- **mrr002** (prior 20/21) is **not a solver failure at all.** Its answer is correct — the official grader
  scores it 1 and razorback scores it 0. AC-4 below has the root cause. *(My first pass on this cell
  reported "243/410 rows differ on `change_category`". That was an artifact of my own `astype(str)`
  comparison, not the cell: the real difference is a DATE-vs-TIMESTAMP column type on three other columns.
  Corrected here because it changes the verdict, not just the wording.)*

**Was each regression passing at `@baseline`?** google_play001 yes (92% lifetime). superstore001 and
tickit002 no — `@baseline` (spd0038) failed both. mrr002 is not a regression.

Statistically, **1** real break among the 18 cells with ≥85% prior reliability against **0.84 expected** is
exactly ordinary. This is worth spelling out because the raw list of 5 regressions *looked* alarming — it
appeared to contain three ≥90%-reliability cells. One turned out to be an infra abort, one a grader
false-negative, and only google_play001 is a genuine break of a reliable passer. Three of the five
"regressions" were not regressions.

### 4. intercom001 — a genuine first pass, but NOT the model swap

Checked the way activity001 was checked: reward across every run-dir in the program, excluding the
auth-poisoned spd0042 attempt 1.

**intercom001 = 0/26 before this board, 1/27 lifetime. This is the first pass ever recorded on that
cell.** spd0039 classified it as a single-mechanism *never-pass* and used it to conclude the group was
`NEEDS-PHASE2-readme-exhausted`. That label is now falsified: the cell is **reachable**.

What the artifact shows changed. The failing spd0042 draw's transcript mentions `median` once and
references only the two target tables. The passing draw names the specific output columns
(`median_time_to_first_response_time_minutes`, `median_time_to_last_close_minutes`,
`median_conversations_reopened`, `median_conversation_assignments`) and works through the shipped
intermediate chain — `intercom__conversation_metrics`, `intercom__using_team`, `intercom__contact_enhanced`,
`intercom__company_enhanced`, `intercom__conversation_enhanced` — rather than computing the metrics from
raw sources. Mechanism: **discovering and reusing the existing model chain**.

**The claim the dispatch offered does not survive.** "The model swap reaching a cell the README program
could not" requires the swap to be the discriminator, and it is not: gpt-5.6-sol has now seen intercom001
three times (spd0042 attempt 1, spd0042 attempt 2, this board) and scored 0, 0, 1. Same model, same
README, same effort. The durable finding is narrower and still worth banking: **intercom001 is reachable
at roughly 1-in-27 under this configuration, so "never-pass" was a sampling artifact of the label, not a
property of the cell.** One draw does not make it a target; it makes it a candidate.

### 5. The infra abort — 1 cell, and how it nearly corrupted the read

`google_play002` scored 0.0 without attempting the task. Its `agent/codex.txt` ends:

> Blocked by the `spacedock:first-officer` mandatory version gate: `spacedock` is not on `PATH`, and
> `SPACEDOCK_BIN` is not executable/set. […] No worker ran, no files changed, and no validation was
> performed.

2 m 32 s wall clock against a 493–1581 s range for every other cell, `subagent-trace-manifest.json` with
`captured: 0` and `dispatches: []`, and it is the run's only `coverage_missing` in `rk audit --policy
strict`. Three independent signals agreeing.

**A caution for the next reader of this repo, because I nearly got this wrong.** The string
`spacedock: command not found` appears in **61 of 67** cell logs — the solver probes for the bare binary,
the probe fails, and it then proceeds normally via `SPACEDOCK_BIN` / the plugin dir. Grepping for that
string as an abort signature would have condemned 61 healthy cells including most of the passes. The
discriminating signature is the conjunction: **`captured == 0` in the trace manifest AND `No worker ran`
in the log AND a wall clock far below the cell-time floor.** By that test there is exactly one abort on
this board, and one (`scd001`) on spd0042.

### 6. Smoke vs full

No fork drift to explain: smoke was not a lever GO, it was a mechanism proof (AC-3 capture works, AC-4
graders agree on 5 live cells), and both held at full — 67/67 captures, and the AC-4 result below. The one
thing smoke could not see was the size tail (§ Submission bundle): a 5-cell panel that happened to sample
2.9–67.6 MB gave a 1.6 GB projection for a board whose real total is 4.35 GiB, because it never sampled a
`biketheft001`-class cell. A capture-volume smoke should sample the *largest* source DB, not a
convenience panel.

### 7. Prevention and next move

- **The launcher-gate abort is the one thing worth fixing, and it is cheap.** It has now silently eaten a
  cell on two consecutive boards (scd001, then google_play002 — a 97% passer). It is invisible in the
  headline because it scores 0.0 like an honest miss. Two guards, both mechanical: fail the trial (so
  `n_errored` catches it) rather than writing reward 0.0, or add a post-run check that flags any cell with
  `captured == 0` before a score is quoted. `rk audit --policy strict` already catches it as
  `coverage_missing` — the gap is that nobody is required to read the audit before the score.
- **Fix the DATE/TIMESTAMP defect in `duckdb_match._normalize` — this is the highest-value follow-up on
  the board.** It is a few lines in the same function that already normalizes `Decimal → float`, it is
  proven against a live case, and until it lands every score this program produces is a lower bound that
  under-counts date-grained cells specifically. Two things to do alongside it: extend the differential fuzz
  to generate `DATE`-vs-`TIMESTAMP` column pairs (the 1500-case fuzz missed this because it never varied
  the temporal type *across* the pair), and re-check whether any historically-stuck date-grained cell was
  ever a false negative. Do NOT bundle this with a lever experiment — it moves the measuring instrument.
- **Do not chase google_play001 with a README lever.** It is a single-draw movement on a cell this
  configuration passes ~92% of the time; the expected value of a lever aimed at it is noise. Its
  multi-source union requirement is, however, well-specified enough to be worth a *canary* if a future
  lever touches completeness.
- **Recommendation on promotion: recommend, do not promote — the captain's call.** This board is not
  comparable to `@baseline` (26/60, different model and a plugin/CLI environment that no longer exists),
  and against its true partner spd0042 it is a null result (net −1 on razorback's grader, net 0 once the
  known grader defect is corrected; p = 1.0000 either way). What it *is*: the
  broadest clean board on record (67 cells, 0 errored, 0 tainted) and the first complete, validated
  68-entry submission bundle. If the goal is a leaderboard number, ship it. If the goal is a moved
  `@baseline`, this board does not supply the evidence, and pooling spd0042 + spd0043 (2 draws of the same
  configuration, 63–65 passes over 118 work-doing cells) is the cheaper path to a defensible mean than a
  third draw.
- **Follow-ups already owned elsewhere, unchanged:** the `dbt_activity_schema` fixture vendoring (3-cell
  exposure, disclosed and accepted) and gitcoin001's missing source data. Neither belongs inside a
  submission run.

### 8. AC-4 CLOSED on the real submission artifact — and it found a divergence

Ran the **UPSTREAM** `evaluation_suite/eval_utils.duckdb_match` (upstream's own unmodified bytes, with only
`google.cloud.bigquery` stubbed for an unrelated module-level import) over the actual submitted bundle,
and reconciled cell-by-cell against razorback's recorded rewards.

```
==== CROSS-CHECK SUMMARY ====
entries              : 68
upstream-graded      : 61      official PASS 33 / FAIL 28
not gradeable locally: 7
   - airbnb002, biketheft001, google_ads001, gitcoin001   (no local gold at all)
   - social_media001, xero_new001, xero_new002            (gold filename mismatch — see below)
DISAGREEMENTS  : 1
   - mrr002: official=1 razorback=0
```

**The 1500-case fuzz and the 5-cell live panel were both 0-disagreement. At 61-cell scale, one divergence
appeared — and it goes in the direction that matters: razorback FAILS an answer the leaderboard PASSES.**

#### Root cause: razorback's port loses pandas' DATE/TIMESTAMP unification

Reproduced outside the container, on byte-identical gold (`sha256 2f57f2d2…` for both the upstream gold and
the view's copy), so this is the comparator and nothing else:

```
razorback compare_duckdb(bundle mrr002, upstream gold) -> False
upstream  duckdb_match (bundle mrr002, upstream gold) -> 1
```

Instrumenting razorback's own `_fetch_columns` + `_vectors_match` names the exact failure — three gold
column-vectors find no partner in the predicted table:

```
*** gold col 0 'date_month':         gold types {date}  pred types {datetime}   410/410 element diffs
*** gold col 4 'first_active_month':  gold types {date}  pred types {datetime}   410/410 element diffs
*** gold col 5 'last_active_month':   gold types {date}  pred types {datetime}   410/410 element diffs
      first diff: datetime.date(2018, 1, 1)  vs  datetime.datetime(2018, 1, 1, 0, 0)
```

Gold stores those columns as DuckDB `DATE`; the solver's table stores them as `TIMESTAMP`. The two paths
then diverge:

- **Upstream** reads via `fetchdf()`. pandas coerces `DATE` *and* `TIMESTAMP` to the same `datetime64`
  dtype, so the values compare equal → match → 1.
- **razorback** reads via `fetchall()` (deliberately — no pandas in the verifier image, per the module's
  own ABOUTME). `fetchall()` preserves the distinction: `datetime.date` for `DATE`,
  `datetime.datetime` for `TIMESTAMP`. `_vectors_match` reaches its `elif a != b` branch and
  `date(2018,1,1) != datetime(2018,1,1,0,0)` in Python → no match → 0.

`duckdb_match.py` already anticipates exactly this class of bug for one type: `_normalize()` coerces
`Decimal → float` precisely because "Decimal is `numbers.Number` yet NOT `numbers.Real`, so it would skip
the tolerance branch and a within-1e-2 DECIMAL match would wrongly score 0." The date case is the same
mistake with a different type, and the fix belongs in the same function — normalize `datetime.date` to
`datetime.datetime` at midnight (or both to a common ordinal) so the pandas-equivalent unification is
restored. **I did not make that change**: it is razorback grading-path code, and altering the grader while
a submission bundle is on the table is precisely the wrong moment. Recommended as a follow-up.

**Blast radius on this board: exactly 1 cell.** Scanned all 61 gradeable cells for a `DATE`↔`TIMESTAMP`
type mismatch on any graded column — only `mrr002.mrr` has one. That agrees with the crosscheck finding
exactly one disagreement, from two independent directions (schema scan and differential grading).

**Why this matters beyond one cell.** DuckDB's `date_trunc('month', …)` returns `TIMESTAMP`, which is the
natural way to build exactly the monthly-rollup tables this benchmark is full of. So the defect is not
exotic — it is one plausible SQL choice away on any date-grained task, and it silently converts a correct
answer into a 0. Every score this program has recorded is therefore a **lower bound** on the leaderboard's
grader, with the bias concentrated in date-grained aggregation cells rather than spread evenly. mrr002's
20/21 lifetime says the solver usually emits `DATE` and only tripped the defect on this draw — which is
also why 20 prior draws never exposed it.

#### Second AC-4 finding: upstream cannot resolve its own gold for 3 instances

`social_media001`, `xero_new001`, `xero_new002` are reported "not gradeable" not because gold is missing
but because **upstream's eval line names a filename its own gold directory does not contain**:

| instance | eval line says | actually on disk | razorback's view grades against |
|---|---|---|---|
| social_media001 | `social_media_reporting__rollup_report.duckdb` | `social_media.duckdb` | `social_media.duckdb` |
| xero_new001 | `xero.duckdb` | `xero_new.duckdb` | `xero_new.duckdb` |
| xero_new002 | `xero.duckdb` | `xero_new.duckdb` | `xero_new.duckdb` |

razorback's packager reconciles the name to the one `.duckdb` actually present and rewrites the view's
eval line; upstream's `evaluate.py` joins the raw eval-line name and would find nothing. It does not crash
— `duckdb_match` is wrapped in a bare `try/except: score = 0` — so those three would score **0** under the
grader as shipped. **The two graders are running different tests on these 3 cells.** All three scored 0
locally anyway, so no verdict differs today; the exposure is latent — if a future draw gets one right,
razorback would say 1 and upstream-as-shipped would say 0. (The public leaderboard presumably holds a
corrected gold set; that is an assumption, not something this evidence establishes.)

`chinook001` is the third shape of the same theme: its gold file exists but contains none of its three
required answer tables, so upstream raises `CatalogException` and its `try/except` scores 0. Both graders
say 0, so it is recorded as an agreement — but it is an agreement on "unscoreable", not on "wrong".

**AC-4 verdict: the comparator port is faithful in its column-containment semantics — the structure,
the 1e-2 tolerance, the extra-pred-column tolerance and the missing-table fail-closed all hold across 61
live cells — with ONE identified defect (DATE/TIMESTAMP unification) and one gold-resolution divergence
that is upstream's own data bug rather than a comparator difference.** That is a pass with two named,
bounded exceptions, not a clean pass, and the honest headline is that we grade ourselves slightly *harder*
than the leaderboard does.

Operational note, for whoever runs this next: the reconciliation took **~17 minutes of single-core CPU**
(09:10:0x → 09:27:07 UTC) at
~1.1 GB RSS on 61 cells. Upstream's comparator is `O(gold_cols × pred_cols)` vector comparisons with a
Python `sorted()` per comparison, so cost scales with table area, not cell count. Do not run it in a
foreground call.

### 9. Full per-cell ledger, all 68 official instances

`spd0043` = this board, `spd0042` = the byte-identical prior configuration, `prior pass-rate` = every
recorded draw in this program excluding this board and excluding spd0042's auth-poisoned attempt 1,
`MB` = submitted capture size. `—` = the cell did not run in that board.

| instance | spd0043 | spd0042 | prior pass-rate | move | MB | note |
|---|---|---|---|---|---|---|
| activity001 | 1 | 1 | 50/52 | = | 9.8 |  |
| airbnb001 | 1 | 1 | 17/32 | = | 428.5 |  |
| airbnb002 | 0 | — | 0/1 | new | 526.3 | record-only, no local gold |
| airport001 | 1 | 0 | 2/14 | **GAIN** | 4.5 |  |
| analytics_engineering001 | 0 | 0 | 0/15 | = | 23.3 |  |
| app_reporting001 | 1 | 1 | 41/41 | = | 21.0 |  |
| app_reporting002 | 1 | 1 | 25/25 | = | 18.8 |  |
| apple_store001 | 1 | 1 | 46/54 | = | 20.5 |  |
| asana001 | 1 | 1 | 5/24 | = | 16.8 |  |
| asset001 | 1 | 1 | 11/24 | = | 131.0 |  |
| atp_tour001 | 0 | 0 | 0/16 | = | 87.8 |  |
| biketheft001 | 0 | — | 0/1 | new | 1530.3 | record-only, no local gold |
| chinook001 | 0 | — | 0/9 | new | 6.5 | gold ships none of its 3 answer tables |
| divvy001 | 1 | 1 | 4/25 | = | 91.8 |  |
| f1001 | 1 | 1 | 19/37 | = | 11.8 |  |
| f1002 | 1 | 1 | 5/15 | = | 11.3 |  |
| f1003 | 1 | 1 | 15/20 | = | 11.3 |  |
| flicks001 | 0 | 0 | 0/18 | = | 16.5 |  |
| gitcoin001 | — | — | — |  | 0.0 | PLACEHOLDER — no source data upstream; empty DB, cannot score |
| google_ads001 | 0 | — | 0/1 | new | 13.8 | record-only, no local gold |
| google_play001 | 0 | 1 | 48/52 | **REGR** | 15.0 |  |
| google_play002 | 0 | 1 | 30/31 | **REGR** | 12.0 | INFRA — launcher-gate abort, no worker ran (2m32s) |
| greenhouse001 | 1 | 1 | 18/20 | = | 21.3 |  |
| hive001 | 0 | 0 | 0/23 | = | 2.3 |  |
| hubspot001 | 1 | 1 | 16/19 | = | 40.8 |  |
| intercom001 | 1 | 0 | 0/26 | **GAIN** | 24.5 |  |
| inzight001 | 0 | — | 0/1 | new | 2.3 |  |
| jira001 | 1 | 1 | 3/25 | = | 7.5 |  |
| lever001 | 1 | 1 | 13/14 | = | 15.5 |  |
| marketo001 | 1 | 1 | 22/27 | = | 18.8 |  |
| maturity001 | 1 | 1 | 14/15 | = | 6.5 |  |
| movie_recomm001 | 0 | 0 | 0/27 | = | 47.0 |  |
| mrr001 | 1 | 1 | 71/81 | = | 2.5 |  |
| mrr002 | 0 | 1 | 20/21 | ~~REGR~~ | 1.8 | **official grader says 1** — razorback DATE/TIMESTAMP defect, AC-4 §8 |
| nba001 | 0 | 0 | 0/24 | = | 116.8 |  |
| netflix001 | 0 | 0 | 0/25 | = | 5.0 |  |
| pendo001 | 0 | 0 | 0/22 | = | 35.8 |  |
| playbook001 | 1 | 1 | 14/14 | = | 1.8 |  |
| playbook002 | 0 | 0 | 0/16 | = | 2.0 |  |
| provider001 | 0 | 0 | 0/33 | = | 30.8 |  |
| qualtrics001 | 1 | 1 | 14/14 | = | 13.8 |  |
| quickbooks001 | 0 | 0 | 0/15 | = | 48.8 |  |
| quickbooks002 | 1 | 1 | 53/54 | = | 47.5 |  |
| quickbooks003 | 1 | 0 | 21/34 | **GAIN** | 52.3 |  |
| recharge001 | 0 | 0 | 9/20 | = | 12.5 |  |
| recharge002 | 1 | 1 | 4/22 | = | 14.5 |  |
| reddit001 | 0 | 0 | 0/16 | = | 236.3 |  |
| retail001 | 1 | 1 | 20/30 | = | 26.3 |  |
| salesforce001 | 0 | 0 | 3/25 | = | 17.8 |  |
| sap001 | 1 | 1 | 14/22 | = | 39.5 |  |
| scd001 | 0 | 0 | 0/16 | = | 14.3 |  |
| shopify001 | 0 | — | 0/1 | new | 20.0 |  |
| shopify002 | 1 | — | 1/1 | new | 20.8 |  |
| shopify_holistic_reporting001 | 0 | 0 | 0/15 | = | 14.8 |  |
| social_media001 | 0 | 0 | 0/24 | = | 33.3 | upstream gold filename mismatch — official grader cannot resolve gold (AC-4 §8) |
| superstore001 | 0 | 1 | 1/22 | **REGR** | 6.8 |  |
| synthea001 | 0 | 0 | 0/22 | = | 27.8 |  |
| tickit001 | 1 | 1 | 24/24 | = | 64.8 |  |
| tickit002 | 0 | 1 | 4/24 | **REGR** | 55.3 |  |
| tpch001 | 0 | 0 | 0/28 | = | 108.5 |  |
| tpch002 | 1 | 1 | 16/17 | = | 83.0 |  |
| twilio001 | 0 | 0 | 0/17 | = | 8.8 |  |
| workday001 | 1 | 1 | 15/16 | = | 27.5 |  |
| workday002 | 1 | 1 | 16/16 | = | 27.5 |  |
| xero001 | 0 | 0 | 0/33 | = | 8.0 |  |
| xero_new001 | 0 | 0 | 0/26 | = | 12.3 | upstream gold filename mismatch — official grader cannot resolve gold (AC-4 §8) |
| xero_new002 | 0 | 0 | 0/21 | = | 8.3 | upstream gold filename mismatch — official grader cannot resolve gold (AC-4 §8) |
| zuora001 | 0 | 0 | 0/18 | = | 13.8 |  |

**What the `0/N` column says about the ceiling.** **28 of the 68 instances have never passed** in this
program, this board included — and **22 of those 28 have ≥15 recorded attempts** (xero001 0/33,
provider001 0/33, tpch001 0/28, movie_recomm001 0/27, xero_new001 0/26, netflix001 0/25, nba001 0/24,
social_media001 0/24, hive001 0/23 …). That is a third of the official board at a lifetime zero across
every README the program has tried and two models. The remaining 6 never-passers are low-attempt cells,
mostly the ones added this cycle.

The gap between 32/67 and a materially higher number is not in the cells that wobble — the wobble is
worth ±2 and this stage just spent its effort proving that. It is in that 22-cell block, and nothing in
the README channel has moved it. Any plan to raise the leaderboard number should start by asking what
those 22 have in common, not by tuning around the discordant pairs.

## Failure Review

**Primary type: `wrong-branch`** (solver-side classification flip). Explicitly NOT
`infrastructure-failure` and NOT `variance-unclear`.

**The FO's framing, and where it was wrong.** The FO correctly refused to let this be written off as
churn: `activity001` is **50/51 lifetime** and the single failure is this run, so the 15.8% board-average
churn figure does not cover it. But the accompanying premise — "the only thing that changed between
spd0042's 1.0 and this 0.0 is the `test.sh` capture patch" — is **false**, and that was my miss at
propose. The **spacedock plugin also moved**: spd0042's own spec header pins it at `601c3f53`; this run
ran `ca136f83a`. Those are **68 commits** apart, including orchestration-contract changes ("Verifier
carve-out", "Fan-out clause orders dedupe before verify", "Host-neutral contract core"). I recorded the
plugin commit at propose and flagged that its tag disagreed with the dispatch, but I never diffed it
against spd0042's — exactly the omission the standing plugin-version lesson warns about.

**The capture patch is exonerated, on four independent lines of evidence:**

1. **Ordering** (the FO asked for this explicitly). The rendered `test.sh` is
   `mkdir -p /logs/verifier` → marker comment → `cp /app/activity.duckdb /logs/verifier/predicted.duckdb || true`
   → the verify invocation. So the `cp` runs **BEFORE** `verify.py`, and the verify invocation is
   byte-identical to razorback's own template. No name collision: the DB stem is `activity`, the capture
   destination is `predicted.duckdb`, the reward file is `reward.json`.
2. **Nothing reads that directory.** `verify.py`, `duckdb_match.py`, and `eval_spec.py` contain no
   `glob` / `listdir` / `scandir` / `iterdir` / `walk`, and no reference to `/logs` at all. Mechanism 1
   is ruled out by code, not by assertion.
3. **The view is otherwise untouched.** Exactly **1 of 489** files in the activity001 view has an mtime
   after 2026-07-01, and it is `tests/test.sh`. The fixture that produced 50 passes is byte-identical.
4. **The verdict reproduces offline on the captured bytes.**
   `compare_duckdb(captured predicted.duckdb, gold)` = `False`, matching the container's
   `{"reward": 0.0}`. The capture is faithful and the comparator is doing in-container what it does
   offline. Mechanism 3 (size/timing) dies here too — the 9.2 MB capture is the smallest of the five and
   the two 1.0 cells captured 19.7 MB and 67.6 MB successfully.

**What actually happened — the solver abstained on a task it can do.** Same fixture, same README hash,
same model, opposite branch:

| | spd0042 (**1.0**, 11 min) | spd0043 smoke (**0.0**, 8 min) |
|---|---|---|
| classification | **R2** — "declared in YAML but missing SQL" | **R3** — "fixture defect" |
| action | **authored** `dataset__aggregate_after_1.sql` + `dataset__aggregate_all_ever_1.sql` | **"Changed files: none"** |
| dbt | `dbt compile` passed; `dbt build` passed all 8 models/tests | `dbt compile` failed; "neither target table exists in `main`" |
| the same blocker | noted it — "`dbt_activity_schema` macros are absent … did not fabricate a package shim" — **and built the targets anyway** | treated it as authorization to do nothing |

Confirmed against the databases: the predicted DB holds **exactly the same 29 tables as the pristine
source** — the solver built *nothing*. Gold holds 48, including the two graded targets, which the source
never ships (so this is a failure-to-create, not a destroyed passer). The 8-minute runtime, shortest of
the five, is the abstain signature.

So the R3 "don't fabricate" rule fired as a **total abstain** on a task whose declared targets are
authorable — and the passing run proves they are authorable, while citing the identical missing-macro
condition. That is a real and actionable defect in the R2/R3 gate, not noise.

**Is it the plugin or the model?** RESOLVED — see the discriminator section below. It is neither the
patch nor the plugin: the plugin never moved (reflog-verified), and arm A passed WITH the patch present.
It is a solver disposition flip on a fixture-deficient cell. Three consecutive failures on a 98% cell is ~1e-5 by chance, so something real
changed; the plugin's 68-commit advance is the leading candidate because it governs the
first-officer→ensign dispatch that produced the abstain, but gpt-5.6-sol branch nondeterminism at
`temperature: 0.0` cannot be excluded from two draws.

**Answers to the five required questions.**
1. *Original hypothesized fork:* none — this is a coverage entity, and the canary was expected to hold.
2. *Fork the committed artifact revealed:* R2-authoring versus R3-abstain on an unbuildable-as-shipped
   project. The artifact is unambiguous: zero new tables.
3. *Did the rule fire, and where is the evidence?* Yes — the ensign names R3 explicitly and reports
   "Changed files: none"; the DB table-set comparison corroborates it independently of the transcript.
4. *What to test next:* tighten the R3 gate so "package macros absent" alone does not authorize a total
   abstain when the declared targets are authorable from source (the R2 path the passing run took). That
   is a solver-README lever for a separate entity, and it is worth filing — `activity001` is the most
   stable cell on the board and it just lost to this.
5. *Next step:* `escalate`. The patch question is answered; the plugin-versus-model attribution and the
   R3-gate lever are captain-level strategy calls, and the 67-cell board should not launch until the
   attribution is settled.


### Canary discriminator — the patch is CLEARED empirically, and activity001 is not a reliable canary

**Arm A (patch PRESENT, `trials: 2`), `runs/spd0043-activity001-canary-patched/892e186069ab1984`:**

| trial | reward | tables built |
|---|---|---|
| `__VvpuPBm` | 0.0 | none (29 = pristine source) |
| `__4FfvfWB` | **1.0** | **`dataset__aggregate_after_1`, `dataset__aggregate_all_ever_1`** (31 vs 29) |

**Arm A is the falsifier and it fired.** A cell that passes *with the capture patch present*, building exactly
the two graded targets, cannot be a cell the patch breaks. The FO asked that the patch not be cleared "by
argument" — this clears it by experiment: patched-and-passing is a direct observation, not an inference.

**Arm B (patch reverted) was therefore NOT run, deliberately.** Arm B is the control for the hypothesis
"the patch breaks the cell", and that hypothesis is already dead. Its only remaining value would be
estimating the unpatched pass rate, which is not a board decision and would cost another ~20 min of
solver time on a cell we now know is stochastic. Recorded as a deliberate skip, not an omission — say the
word and it is one command.

**What activity001 actually is:** a **coin-flip cell on a deficient fixture**, not the 98% sentinel its
record suggested. Post-patch draws: smoke 0.0, arm A 0.0, arm A 1.0 → **1/3**, against 50/51 lifetime
before. *(Updated at `analyze`: the 67-cell board added a 4th post-patch draw, **1.0** — so post-patch
stands at 2/4. Still a coin flip, still retired as a canary, and the patch stays cleared: three of the
four post-patch draws now show the cell passing or capable of passing with the patch present.)* The same fixture, README hash, model, and plugin produce both branches, so the variable is the
solver's *disposition*: R2 (author the missing SQL and build) versus R3 (declare a fixture defect and
abstain). Both readings are defensible, which is exactly why it flips.

**Correction to my own earlier report:** I told the FO the spacedock plugin had moved 68 commits between
spd0042 and this run, and that this was the confound. That was wrong. `git -C spacedock reflog` shows the
repin to `ca136f83a` landed 2026-07-27 12:36:32Z — *before* spd0042 attempt 1 (12:39Z), attempt 2
(07-28 00:27Z), and this smoke (07-29 06:10Z). All three ran on the same plugin. The `601c3f53` in this
entity's Configuration table is the as-filed value that spd0042's own launch-time capture retired. The
plugin is exonerated as a between-run variable; the disposition flip stands on its own.

### The real risk this exposes — and its size

The FO's reframing is the durable finding: `activity001`'s stated blocker is **factually true**. Verified
directly — its models call `dbt_activity_schema.*` **101 times**, `dbt_packages/` holds only `dbt_utils`,
and there is no `packages.yml` or `dependencies.yml` at all. The macros were *always* absent; the view is
unchanged but for `test.sh`; so its long streak depended on the solver choosing to build around a
deficient fixture. That is a submission-wide risk, not one canary.

`tools/check_missing_declared_packages.py` sizes it across all 64 views (static scan, no DB, no model):

| class | count | instances |
|---|---|---|
| **UNRESOLVED_NS** — models call a package that is not vendored (the activity001 shape) | **9** | activity001, hubspot001, jira001, retail001, scd001, shopify001, shopify002, shopify_holistic_reporting001, zuora001 |
| DECLARED_NOT_VENDORED — manifest names a package with no `dbt_packages/` dir (container is offline, `dbt deps` cannot fetch) | 7 | chinook001, inzight001, netflix001, retail001, scd001, shopify_holistic_reporting001, zuora001 |
| VENDORED_UNDECLARED — package present, no manifest (benign for building; the condition both solvers complained about) | 9 | activity001, apple_store001, f1003, qualtrics001, recharge002, salesforce001, workday001, workday002, xero001 |
| no package deficiency | 52 | — |

Cross-referencing the 9 against real outcomes turns a scary count into a small one:

| instance | spd0042 | lifetime | exposure |
|---|---|---|---|
| `activity001` | 1.0 | 51/53 | **at risk** — already demonstrated flipping |
| `hubspot001` | 1.0 | 16/20 | **at risk** — a passer on a deficient fixture |
| `jira001` | 1.0 | 3/26 | **at risk**, but a low-rate cell that happened to pass |
| `retail001` | 1.0 | 21/31 | **protected** — do-nothing-passable, so an abstaining solver still scores 1.0 |
| `scd001` / `shopify_holistic_reporting001` / `zuora001` | 0.0 | 0/17, 0/16, 0/19 | no exposure — chronic zeros, the deficiency is already fatal there |
| `shopify001` / `shopify002` | — | new | one passed, one failed in this smoke |

**Board exposure is 3 cells** (activity001, hubspot001, jira001), not 9 and not 64 — `retail001` is
insulated by being do-nothing-passable, and the three chronic zeros have nothing left to lose. On a 67-cell
board that is a worst case of about **-3 cells (~4.5 points)** from this mechanism, concentrated in cells
whose fixtures are objectively deficient.

The precision matters here: the unfiltered scan reported 17 instances, but `kwargs`, `col`, `re`, `node`,
`fields` and friends are Jinja locals and varargs, not packages. The tool excludes builtins plus any name
bound by `{% set %}` / `{% for %}` / a macro parameter in the same file, which is what takes it from 17 to
9. An inflated exposure number would have been worse than none.

**Recommended, for the captain:** the honest fix is not a solver-README nudge, it is the packaging layer —
the same surface spd0010 established. `dbt_activity_schema` is a real public package; vendoring it (as
`_vendor_dbt_utils` already does for `dbt_utils`) would remove the ambiguity that makes activity001 a coin
flip, and would do it without asking the solver to fabricate anything. That is a separate entity: it
changes the fixture, so it must not ride along inside a submission run.

## Follow-up Routing

`escalate` — two decisions are the captain's, and one follow-up entity should be filed.

**Escalate (captain):**
1. **Launch the 67-cell board now, or vendor `dbt_activity_schema` first?** Board exposure to the
   abstain mechanism is **3 cells** (activity001, hubspot001, jira001) — a worst case of ~-3 cells / ~4.5
   points. Launching now is defensible provided the disclosure below rides with the result; fixing the
   fixture first is cleaner but changes the fixture, so it cannot ride inside a submission run.
2. **`activity001` is retired as a canary.** It is a coin flip on a deficient fixture (1/3 post-patch),
   not the 98% sentinel its record implied. Future smokes should use `tickit001` (23/26, held here) plus a
   passer from the 52 views with no package deficiency.

**File (one follow-up entity, NOT in this one):** vendor `dbt_activity_schema` into the activity001 view
through `tools/`, exactly as `_vendor_dbt_utils` already vendors `dbt_utils` — a packaging-layer fixture
repair on spd0010's established surface, which removes the R2/R3 ambiguity without asking the solver to
fabricate anything. Verify it is idempotent and changes no other cell, and re-measure activity001's rate.

**Stop:** the capture-patch investigation. Cleared by experiment (arm A passed with the patch present),
not by argument.

**Disclosure that must ride with any submission from this board** (AC-6 plus this stage's finding):
8 of 64 cells are do-nothing-passable (floor 0.125) and 2 of those were destroyed by the solver in
spd0042; 9 cells sit on package-deficient fixtures, of which 3 are passers that can abstain-flip; and
`chinook001` is a structural 0 locally while still being submitted.

## Verdict

## Stage Report: propose

- FAILED: Package the 8 missing official instances as harbor-local task views (chinook001 already has a view; inzight001, shopify001, shopify002, airbnb002, biketheft001, gitcoin001, google_ads001 need building) using the same packaging path that produced the existing 61 views from /home/kent/Spider2/spider2-dbt/examples/. Then author + freeze the submission spec with benchmark.tasks = exactly the 68 official instance_ids from examples/spider2-dbt.jsonl, solver_workflow pointing at the UNCHANGED @baseline solver_workflows/spd0038-compose-6-stabilizers, model gpt-5.6-sol, reasoning_effort xhigh, trials 1, concurrency.trials 4. Paste the AC-1 two-way diff (spec vs official 68) showing it EMPTY and danish_democracy_data001 absent.
  3 of 7 packaged (inzight001/shopify001/shopify002, after fixing a vendored-postgres-profile packaging bug — finding 4); spec carries **64**, not 68; AC-1 diff is EMPTY in the SPEC\OFFICIAL direction with danish absent, but OFFICIAL\SPEC holds 4 cause-attributed absences (`airbnb002`/`biketheft001`/`google_ads001` have no upstream gold and razorback's materializer fails closed; `gitcoin001` has no upstream source data at all, so it cannot be run by anyone). Config held exactly: solver hash `sha256:607dec29…` = @baseline, gpt-5.6-sol, xhigh, trials 1, concurrency 4 — findings 7 and 8.
- DONE: DIAGNOSE chinook001 before including it — spd0010 excluded it from the board as "upstream-goldless" but evaluation_suite/gold/chinook001 exists. Determine the REAL cause from spd0010's record and from the fixture itself, then decide include-or-exclude on evidence and record the reasoning. If it must stay excluded, the spec carries 67 gradeable + a documented exclusion rather than a silent 68 that errors one cell. Do not assume the old exclusion is stale and do not assume it is still valid.
  Exclusion is STILL VALID: the gold DuckDB opens fine but all three `condition_tabs` are absent from it, so the gold side can never match; corroborated by 9/9 historical run-dirs at reward 0.0 with clean `agent_execution` + `verifier`. Decision: INCLUDE in the run and the bundle (the leaderboard holds real gold), EXCLUDE from the local gradeable denominator (63, not 64) — finding 2.
- DONE: Build the AC-2 evidence scaffold and the submission-bundle exporter, but do NOT run the full board: (a) a per-instance execution table covering all 68 with columns instance / view built / container up / solver ran / verifier ran / reward-or-N.A., pre-filled for what you can establish at propose; (b) an exporter that turns a razorback run-dir into the upstream bundle layout (results_metadata.jsonl with instance_id/answer_type/answer_or_path + per-instance artifact files) per evaluation_suite/README.md, plus a validator that checks 68 entries and that every referenced path exists. Then run the gatekeeper per _gatekeeper/propose-review-guideline.md and record its block.
  68-row table in finding 10 (gatekeeper independently reproduced its reward column cell-for-cell against spd0042's `per_trial_outcomes.json`); `tools/export_submission_bundle.py` + `tools/validate_submission_bundle.py` built and exercised; gatekeeper run read-only and its APPROVE block transcribed verbatim. No run launched.

### Falsifiability of each check I am citing

- `tools/validate_submission_bundle.py` — mutation-tested: 6 deliberate defects injected into a good bundle (wrong `answer_type`, extra key, `../` traversal, `danish_democracy_data001` entry, dangling path, stray root `.jsonl`) and **all 9 substantive checks fired**. What would make it fail: any of those defects reaching a real bundle. A bare "10 PASS" without the mutation run would hide a tautology.
- `tools/crosscheck_official_grader.py --fuzz 1500` — 919 MATCH / 581 MISMATCH / **0 disagreements** against the *imported upstream* `eval_utils.duckdb_match`. What would make it fail: any porting divergence reachable by the generated cases (tolerance boundary, `ignore_order` sort key, column containment, extra pred columns, missing table). Both verdict branches are exercised, so an all-mismatch vacuous pass is excluded.
- `add_predicted_db_capture.py` reward-neutrality — proven by *executing* a path-rewritten copy of the real `test.sh` before and after patching: positive control (gold as predicted) `{"reward": 1.0}` both times, `cmp`-identical; negative control (unbuilt source) `{"reward": 0.0}`. What would make it fail: any edit that moved `--predicted-db`, `--gold-db`, or `--reward-out`.
- Gold-integrity gate + do-nothing sweep — both run through the verifier's own `compare_duckdb`, not a re-implementation, so a divergence between them and the real scorer is impossible by construction.

### Summary

Packaged 3 of the 7 missing instances (61 → 64 views) after diagnosing and fixing a packaging bug —
razorback's DuckDB resolver reads `profiles.yml` files vendored inside `dbt_packages/`, and the three
`dbt_date`-vendoring instances were failing closed on that package's `target: postgres` CI fixture; the
repair is confined to `tools/`, as spd0010 established. Froze a 64-task spec byte-equivalent to spd0042's
config (identical `sealed_hash`, @baseline solver hash unchanged) and confirmed selection with
`--explain`. **AC-1 cannot be met: 4 official instances are blocked by upstream data gaps**, one
(`gitcoin001`) permanently — proven from `DBT_start_db.zip`/`dbt_gold.zip` themselves, so no re-`setup.py`
recovers them. chinook001's old exclusion is still valid (goldless *answers*, not a missing dir), and it
is now on the board as a submit-only guaranteed-0.

Two findings dominate. **(1) The predicted DuckDB never survives a run** — the verifier runs in-container
and only `reward.json` escapes, so no bundle was exportable from any past or future run; verified against
the real 60-cell spd0042 run-dir (60/60 `MISSING_ARTIFACT`). Fixed via harbor's logs bind-mount with a
proven reward-neutral one-line `test.sh` patch. **(2) AC-4 came out well:** razorback's comparator is a
real port of upstream's `duckdb_match`, and 1500 differential fuzz cases against the imported upstream
function found **0 disagreements** — the recorded scores were not measured against a different grader.
Three latent divergences are named anyway (identifier quoting, pandas-vs-native dtypes, unordered fetch).

One unrequested finding worth the captain's attention: the do-nothing floor is **8 instances, not the 2
on record**, and spd0042's solver **destroyed 2 of those free points** (`quickbooks003`, `salesforce001`)
— 35/60 was available for less work than 33/60 took.

## Stage Report: smoke

- DONE: Execute the 3 newly-packaged instances (inzight001, shopify001, shopify002) for the first time at trials=1, PLUS 2 canaries that PASSED in spd0042 — the test.sh patch touched all 64 views and its reward-neutrality has only ever been shown by synthetic controls, never on a live run, so a passing cell still passing is the check that can actually fail. Fill the AC-2 execution table rows for all 5: view built / container up / solver ran / verifier ran / reward. Report rewards honestly — for the 3 new instances the bar is EXECUTION, not passing, so a 0.0 is a legitimate result; for the 2 canaries a drop to 0.0 IS a failure and must halt.
  All 5 executed; strict audit CLEAN, 0 errored, 0 tainted. shopify002 **PASSED 1.0 on first execution**, inzight001/shopify001 0.0 (legitimate misses). tickit001 canary HELD 1.0; **activity001 canary DROPPED to 0.0 → halted and investigated rather than reported as noise**. AC-2 rows filled for all 5 (lines 398/424/449/450/455).
- DONE: Prove the predicted-DuckDB capture works on a REAL run, which has never been exercised: confirm verifier/predicted.duckdb lands on the host for each smoke cell, then run tools/export_submission_bundle.py over the smoke run-dir and show a results_metadata.jsonl whose entries have the three required keys and whose referenced artifact paths all exist relative to their instance folders. This is the AC-3 mechanism proof — the propose finding showed 0/60 exportable before the fix, so this is the check that the fix actually holds in production.
  Capture landed on **5/5** cells (2.9–67.6 MB); export emitted a 5-entry `results_metadata.jsonl` in the documented layout; validator **10/10 PASS** including the 3-required-keys and path-existence checks. Was 0/60 before the fix.
- DONE: Run the per-instance half of AC-4 on live data: grade the exported smoke cells with the OFFICIAL evaluation_suite grader (tools/crosscheck_official_grader.py --bundle, or evaluate.py directly) and reconcile its verdict against razorback's own reward for each cell. Any disagreement is named cell-by-cell with a cause.
  **5/5 agreement, 0 disagreements** — over a 172k×20 table, a 3×42 table, and a missing-table miss (the branch where the predicted fetch raises). No disagreement to name.
- DONE: *(FO mid-stage ask)* state the rendered order of `cp` vs `verify.py`, and size the fixture-deficiency exposure.
  Order: `mkdir` → marker → `cp` → `verify.py`, i.e. the `cp` runs BEFORE verify, invocation byte-identical. Exposure: `tools/check_missing_declared_packages.py` → 9 package-deficient views, of which **3 are at-risk passers**; 52 clean.
- SKIPPED: Canary discriminator arm B (patch REVERTED).
  Arm A passed 1.0 **with the patch present**, which falsifies the deterministic-patch hypothesis outright; arm B is the control for a dead hypothesis and would cost ~20 min of solver time for no board decision. Deliberate skip, recorded — one command to run if the captain wants the unpatched rate.

### Falsifiability of the claims above

- *"the patch is reward-neutral"* — would be falsified by a patched cell that cannot pass. Arm A trial `__4FfvfWB` passed **1.0 with the patch present** and built both graded targets, so the claim survives its strongest test. Supporting: `cp` before `verify.py`, verify invocation byte-identical, no `glob`/`listdir`/`walk`/`/logs` in any of the three verifier files, 1 of 489 view files changed, and `compare_duckdb(captured bytes, gold) = False` reproducing the container verdict.
- *"AC-4 graders agree"* — would be falsified by any cell where official ≠ razorback. 5/5 live + 1500/1500 fuzz, both branches exercised.
- *"exposure is 3 cells"* — would be falsified by a package-deficient view that is a passer and not in {activity001, hubspot001, jira001}. Derived by intersecting the 9 UNRESOLVED_NS views with spd0042 rewards; `retail001` is excluded on the independent ground that it is do-nothing-passable, so abstaining still scores it 1.0.

### Summary

**NO-GO on the canary, GO on everything the stage set out to prove.** All three newly-packaged official
instances now execute end-to-end and **shopify002 passed on its first execution ever**; the submission
pipeline works end-to-end on real solver artifacts (capture 5/5, export 5 entries, validator 10/10) where
it produced nothing at all before; and AC-4 now holds on live data as well as synthetic (5/5, 0
disagreements).

The canary drop was real and I did not write it off. It is **not** the capture patch — cleared by
experiment, since arm A passed with the patch present — and **not** the plugin, which never moved
(reflog-verified; my earlier 68-commit claim to the FO was wrong and is corrected in the entity). It is a
solver **disposition flip** on a fixture whose deficiency is objectively real: `activity001`'s models call
`dbt_activity_schema` 101 times against a package that is absent and undeclared. Earlier runs built around
it; this one invoked the R3 fixture-defect rule and abstained with "Changed files: none". So its 50/51
streak was masking a bad fixture, and it is a coin flip (1/3 post-patch), not a sentinel — it is retired
as a canary.

Sizing the resulting submission-wide risk was the useful part: 9 of 64 views are package-deficient, but
only **3 are at-risk passers** (activity001, hubspot001, jira001) — `retail001` is insulated by being
do-nothing-passable and three others are chronic zeros. Worst case ~-3 cells on a 67-cell board. The
honest fix is a packaging-layer vendoring of `dbt_activity_schema`, filed as a separate entity because it
changes the fixture and must not ride inside a submission run.

## Stage Report: full

This dispatch replaced a stalled `full`-stage worker. Phases 1 (razorback record-only mode) and 2 (3-cell
validation) were **inherited and verified, not re-done**; phase 3 (re-freeze, launch, provenance) is mine.

- DONE: RECOVER the stalled worker's uncommitted work product first: review and commit
  spider2-dbt/tools/add_predicted_db_capture.py, spider2-dbt/tools/package_spider2_dbt_views.py, and
  specs/spd0043-recordonly-validate.{yaml,frozen.yaml}, plus the razorback submodule pointer for branch
  spd0043-record-only-no-local-gold
  Commit `ccda85a`, path-scoped. Reviewed each diff before committing: `--allow-missing-gold` is a
  genuine opt-in (`gold_db` becomes `Path | None`; both the source-restore and the `shutil.copy2` into the
  gold slot are guarded, so **nothing is fabricated** where gold would be), and the capture script's new
  branch only *skips* views that already capture. Deliberately NOT swept in: razorback's stray `M uv.lock`,
  the `spacedock` gitlink drift, and `specs/spd0013-rebaseline-v022.*` (another entity's untracked files).
  razorback was not pushed and no PR was opened.
- DONE (inherited-and-verified) PHASE 1: the opt-in default-unchanged test exists and passes
  `uv run pytest tests/unit/test_spider2_dbt_harbor_view.py -q` → **18 passed**. The load-bearing one is
  `test_missing_gold_db_still_raises_when_record_only_not_requested`: it asserts a gold-less task still
  raises `FileNotFoundError` mentioning `fail-closed` when the opt-in is absent. It fails if record-only
  ever becomes the default — i.e. it is exactly the spd0010 fail-closed guarantee, held. Companions:
  `test_record_only_is_inert_when_gold_is_present` fails if enabling the flag degrades a gradeable task to
  unscored (the "zero the whole board while looking successful" regression), and
  `test_missing_eval_spec_raises_even_with_record_only` fails if the opt-in is widened to swallow a missing
  `spider2_eval.jsonl` (the answer contract).
- DONE (inherited-and-verified) PHASE 2: the 3-cell hard gate
  `runs/spd0043-recordonly-validate/6bcbfc00072d2a60/result.json` read directly: `n_total_trials 3`,
  `n_completed_trials 3`, **`n_errored_trials 0`**, all three rewards `0.0`; and three
  `*/verifier/predicted.duckdb` files present on the host (airbnb002, biketheft001, google_ads001). That is
  the designed behaviour, so the HARD STOP did not fire.
- DONE: Re-freeze the submission spec to 67 tasks — the existing 64 plus airbnb002, biketheft001,
  google_ads001. Paste the AC-1 two-way diff: gitcoin001 must be the ONLY remaining OFFICIAL\SPEC entry and
  danish_democracy_data001 must still be absent. Confirm the selection with `rk run --explain` ($0) and
  remove the empty job dir it leaves
  `specs/spd0043-official-board-67.{yaml,frozen.yaml}`, commit `6bbed4d`. AC-1 diff pasted in
  `## Run result`: `OFFICIAL \ SPEC = {gitcoin001}` only, `SPEC \ OFFICIAL` empty,
  `danish_democracy_data001` False. `--explain` reported `Tasks: 67`; its empty job-dir tree was removed
  (the real run re-created the same job name `4de20bed438d4d51`, so that removal was load-bearing, not
  cosmetic) and no stale `lock.json` was on the path.
- DONE: Launch the 67-cell board DETACHED via drivers/rk-run-detached.sh and report handle path, job dir,
  PID and ETA without blocking
  Handle `runs/.rk-handles/spd0043-full-20260730-050626/`, job dir
  `runs/spd0043-official-board-67/4de20bed438d4d51`, PID `881538`, ETA ~3.5–4 h (~08:40–09:10 +0800).
  Liveness verified at T+3.5 min rather than trusting rc=0: worker PID alive, `lock.json` + 4 cell dirs
  written, 4 solver containers `Up`, composed prompt visible in `job.log` — and `airbnb002` (a record-only
  cell) is in the first batch, so the new path is exercised from minute one.
- DONE: Capture AC-5 at launch into '## Run result': spacedock plugin describe/rev-parse/status --short,
  codex --version, codex login status, AND the razorback branch + commit SHA
  All eight captured in the AC-5 table. Plugin `v0.27.0-pre0` / `ca136f83a` / clean+detached (unmoved);
  razorback `spd0043-record-only-no-local-gold` @ `027bb95`; `codex-cli 0.145.0`; `codex login status` =
  `Logged in using ChatGPT`, re-checked **in the same shell command as the launch** per the spd0042
  attempt-1 `refresh_token_reused` lesson. Also recorded: docker 29.5.2, zero pre-launch containers, 43 GB
  free, and no other in-flight handle.
- SKIPPED: run audit/score
  Explicitly out of scope — the board will still be in flight for hours. The next stage must read
  `n_trials_errored` before any score, because `stratified_pass_at_1` censors errored cells out of its
  denominator.

### Summary

Recovered the dead worker's work product into two path-scoped commits (`ccda85a` recovery, `6bbed4d` the
67-task spec pair), independently verified both inherited phases rather than taking them on report — the
fail-closed default test passes and the 3-cell gate really is 3/3 with 0 errored and three captured
predicted DBs — then re-froze to 67, confirmed AC-1 is now a single documented absence (`gitcoin001`,
shipping as a disclosed placeholder), and launched the board detached. The one thing worth the next
reader's attention: razorback is running on an unpushed feature branch that nothing in the frozen spec
records, which is why its branch and SHA are now written into AC-5 explicitly — the board is not
reproducible from the spec alone.

## Stage Report: analyze

- DONE: Export the FULL submission bundle — this is the deliverable. All 67 executed instances PLUS
  gitcoin001 as a disclosed placeholder = 68 entries in results_metadata.jsonl … Run the validator and
  paste its output. State the bundle's on-disk size and path plainly
  `/home/kent/autobench/spider2-dbt/runs/_submissions/spd0043-official-68/` — 68 entries (67 exported + 1
  placeholder, 0 not exported), 4.35 GiB logical / ~0 incremental (hardlinked). Validator output pasted in
  `## Submission bundle`: 11/11 PASS, exit 0. What would make each check fail is documented at its source
  and the suite was mutation-tested at `propose`; the two that could plausibly have fired here are 4b
  (a dangling artifact path — would fire if any capture had not landed) and 5d (entry count ≠ 68 — would
  fire if the placeholder or any cell were dropped). Both passed against 68 real files.
- DONE: Close AC-4 on the real submission artifact: run the OFFICIAL evaluation_suite grader over the
  bundle for the 63 locally-gradeable instances and reconcile its verdict cell-by-cell against razorback's
  own rewards. Name EVERY disagreement with a cause.
  **`## Behavioral analysis` §8. 61 cells graded (not 63 — see below), 33 official PASS, and exactly ONE
  disagreement: mrr002, official=1 razorback=0.** Root cause identified and reproduced outside the
  container on byte-identical gold: razorback's `fetchall()`-based port preserves `datetime.date` vs
  `datetime.datetime` where upstream's `fetchdf()` coerces both to `datetime64`, so a gold `DATE` column
  against a predicted `TIMESTAMP` column fails `_vectors_match`'s `a != b` branch. The defect is the exact
  analogue of the `Decimal → float` case `_normalize()` already handles. Blast radius bounded at 1 cell by
  two independent methods (differential grading, and a schema scan of all 61 gradeable cells for
  DATE↔TIMESTAMP mismatches). Second finding: the count is 61, not 63, because upstream's own eval line
  names a gold filename absent from its own gold dir for social_media001 / xero_new001 / xero_new002 —
  razorback name-reconciles, upstream-as-shipped scores 0, so the two graders run different tests on those
  3. Razorback NOT modified (grading-path code, and mid-submission is the wrong moment); filed as the
  top-priority follow-up instead.
- DONE: Report the honest denominators and the paired read … Then the paired comparison against spd0042 on
  the 60 shared cells … judged against the 15.8% same-config churn yardstick. Separately: verify whether
  intercom001 is a genuine first pass
  All six denominators tabulated in `## Run result`, now split by grader (razorback 32/67 vs **official
  33/67**, submitted range [33/68, 37/68]). Paired read in §1: the FO's raw figures reproduced exactly
  (33→31, net −2, 3 gains / 5 regressions), then corrected twice — excluding the one no-work cell on each
  board gives 32→31 net −1, and correcting mrr002's grader false-negative gives **32→32, net 0, McNemar
  exact two-sided p = 1.0000** against a K2 expectation of ~9.2 discordant. **intercom001 confirmed 0/26
  before this board — the first pass ever recorded**, which falsifies spd0039's never-pass label; but the
  dispatch's "model swap reached it" framing does NOT survive, because gpt-5.6-sol has scored 0, 0, 1 on
  that cell under the identical configuration (§4).
- DONE: (stage def) `rk score` + `rk audit --policy strict`
  `stratified_pass_at_1 0.47761194`, `stratified_n_errored 0`, Wilson CI [0.3625, 0.5951]. Audit: 66 clean
  / 0 tainted / **1 coverage_missing = google_play002**, which independently corroborated the infra abort.
- DONE: (stage def) behavioral read per moved cell, with confound attribution
  §2–§5. Attribution is `same-configuration variance` for every moved cell — there was no README lever this
  cycle (hash `sha256:607dec29…` verified identical across spd0038/spd0042/spd0043) and spd0042 already
  carried the model swap, so crediting any flip to a lever would be inventing a cause. Mechanisms read off
  committed artifacts: google_play001 built each report from ONE source table where gold unions three
  (10+12+10 = gold's exact 32 rows); intercom001 reused the shipped `intercom__*` model chain.
- SKIPPED: `rk runs diff @baseline` as the headline instrument
  `@baseline` resolves to `spd0038-compose-6-stabilizers-full` — gpt-5.5 on a plugin/CLI environment that
  no longer exists, and a 60-cell task set. Its absolute score is reported for context but the paired
  instrument is spd0042 (byte-identical configuration), which is the comparison that carries information.
  Stated rather than silently substituted.
- SKIPPED: promotion / registry change
  Out of scope by dispatch (`Do NOT modify razorback-registry.yaml`); recommendation recorded in §7.

### Summary

Exported and validated the deliverable — a complete 68-entry submission bundle, 11/11 validator checks,
4.35 GiB — then spent the analysis effort on the three things that change what the numbers mean. First,
**AC-4 found a real grader divergence**: razorback fails mrr002 where the official grader passes it,
because its no-pandas port preserves a `DATE`/`TIMESTAMP` distinction pandas erases; the board is
**33/67 by the leaderboard's own grader**, and every score this program has recorded is a lower bound
biased against date-grained cells. Second, **one cell (google_play002) scored 0.0 without running at all** —
a spacedock version-gate abort, caught by the conjunction of `captured: 0`, `No worker ran`, a 2 m 32 s wall
clock, and the run's only `coverage_missing`; three of the five apparent regressions were therefore not
regressions, and the corrected paired read against spd0042 is **net 0, p = 1.0000**, which means this board
does NOT show a regression from the capture patch or the record-only change. Third, **intercom001 passed
for the first time in 27 recorded draws**, falsifying spd0039's never-pass label — though not, as suggested,
via the model swap, since the same configuration had already failed it twice. The durable structural fact
is the one the ledger exposes: 28 of 68 instances have never passed, 22 of them with ≥15 attempts, and that
block — not the churn — is where the score is stuck.
