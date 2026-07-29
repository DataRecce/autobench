---
title: Expand the board to the official 68 instances and produce a leaderboard-format submission (@baseline README + gpt-5.6-sol xhigh)
status: propose
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
| 1 | `activity001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
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
| 27 | `inzight001` | Y | not yet | not yet | not yet | pending | view built 2026-07-29; never run |
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
| 52 | `shopify001` | Y | not yet | not yet | not yet | pending | view built 2026-07-29; never run |
| 53 | `shopify002` | Y | not yet | not yet | not yet | pending | view built 2026-07-29; never run |
| 54 | `shopify_holistic_reporting001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 55 | `social_media001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 56 | `superstore001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
| 57 | `synthea001` | Y | Y | Y | Y | 0 | spd0042 run-dir |
| 58 | `tickit001` | Y | Y | Y | Y | 1 | spd0042 run-dir |
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

Roll-up: **60** proven executable end-to-end in spd0042 · **1** (`chinook001`) proven executable across
9 historical run-dirs, structurally unscoreable locally · **3** newly packaged, execution pending ·
**3** blocked on the razorback no-gold path · **1** (`gitcoin001`) not runnable at all.

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

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

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
