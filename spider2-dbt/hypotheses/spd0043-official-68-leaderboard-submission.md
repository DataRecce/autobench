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

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
