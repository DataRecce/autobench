---
id: spd0001
title: Establish @baseline — full run of the spider2-dbt-baseline output-contract solver
status: analyze
kind: hypothesis
source: commission seed (loop-anchor; no scored full board exists yet)
started: 2026-06-24
completed:
verdict:
score: 1.0
worktree:
---

## Hypothesis

This is the **loop anchor**, not a lever test. There is no scored full board for spider2-dbt yet —
only two 6-task smokes (`docs/smoke6-2026-06-24.md` 0/6 on the ade README; `docs/smoke6-output-contract-2026-06-24.md`
2/6 on the output-contract README). The output-contract solver `solver_workflows/spider2-dbt-baseline`
is the right seed README, but its pass rate over the full 61 duckdb-runnable tasks is unknown.

**Claim:** running `spider2-dbt-baseline` (codex/gpt-5.5, `reasoning_effort: xhigh`, `trials: 1`,
`concurrency.trials: 4`) over the full 61-task board produces a clean, scored run that we can promote
to `@baseline` — the champion every future hypothesis diffs against. No README change is made; the
spec is `specs/full-baseline.frozen.yaml` as-is.

This entity follows the **anchor exception**: `propose → full`, skipping `smoke` (the README is the
seed, there is nothing to pre-flight). It exists so the FO's first action on the loop is unambiguous.

Target tasks: all 61 (the full board).

## Pre-smoke Decision-Fork Probe

N/A — no lever, no fork. This is the baseline-establishing run.

## Acceptance criteria

**AC-1 — Clean strict audit, no `coverage_missing`, no taint.**
Verified by: `rk audit <run-dir> --policy strict` reports 0 coverage_missing, 0 tainted. Any
build-time preflight failure or packager crash HALTS + escalates (packaging health, see README →
*Packaging / preflight health*) — it is not a result.

**AC-2 — A real scored pass rate is recorded and promoted to `@baseline`.**
Verified by: `rk score <run-dir>` emits `stratified_pass_at_1` (= flat pass rate over the scored
tasks); then
`export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml` →
`rk baseline promote <run-dir>` → `rk registry add run baseline <run-dir>` binds `@baseline`.

**AC-3 — The per-task ledger is captured** so future hypotheses can pick currently-FAIL targets and
currently-PASS canaries.
Verified by: `_artifacts/task-gap-ranking.md` is re-derived from this run's `per_trial_outcomes.json`
(which tasks pass, which fail, the failure class for the fails).

## Gatekeeper review

(Anchor run — gatekeeper N/A; no README diff, no smoke spec. The FO still confirms the full spec is
unmodified vs `specs/full-baseline.frozen.yaml` and `agent.kind: spacedock_solver` / `runtime: codex`.)

## Smoke result

N/A — anchor skips smoke (`propose → full`).

## Run result

**Run under analysis:** `runs/spider2-dbt-full-baseline/13fb630e2cae3eb8` — rc=0, 61/61 trials,
0 errored.

**Score (AC-2 measurement):** `rk score` → `stratified_pass_at_1 = 0.3114754…` = **19 PASS / 61** ;
Wilson CI [0.209, 0.436]. Single `default` stratum (flat pass rate). No prior `@baseline` exists —
this run *establishes* it; promotion is deferred to the captain at conclude.

**Strict audit (AC-1):** `rk audit --policy strict` → `{"clean": 61, "coverage_missing": 0,
"tainted": 0}`. **Clean attestation: 0 coverage_missing / 0 tainted.** No build-time preflight failure
or packager crash errored a cell.

**One non-signal packaging fault found by artifact read (not by the audit):** chinook001 fails because
its GOLD `chinook.duckdb` ships only the raw source tables (album, artist, customer, …) and never the
`dim_customer`/`fct_invoice`/`obt_invoice` tables the eval spec's `condition_tabs` demand. The
verifier's *gold-side* fetch raises `Catalog Error: Table dim_customer does not exist` → `eval-spec/
compare error` → reward 0. No agent output can pass this cell (the agent in fact built all three
tables as BASE TABLEs). Classified **packaging-fault (non-signal)** and excluded from content
interpretation; the *content-signal* board is effectively 19/60.

### Full 61-task ledger (PASS/FAIL + failure bucket)

**19 PASS (sentinels):** activity001, app_reporting001, app_reporting002, f1001, google_play001,
google_play002, greenhouse001, hubspot001, lever001, maturity001, mrr001, mrr002, playbook001,
qualtrics001, quickbooks002, tickit001, tpch002, workday001, workday002.

**42 FAIL, bucketed:**

| Bucket | Count | Tasks |
|---|---|---|
| wrong-columns-or-grain | 38 | airbnb001, airport001, apple_store001, asana001, asset001, atp_tour001, divvy001, f1002, f1003, flicks001, hive001, jira001, marketo001, nba001, netflix001, pendo001, playbook002, provider001, quickbooks001, quickbooks003, recharge001, recharge002, reddit001, retail001, salesforce001, sap001, scd001, shopify_holistic_rep, social_media001, superstore001, synthea001, tickit002, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001 |
| wrong-table-name | 3 | movie_recomm001 (built `original_programs`, gold wants `user_watched_movies`); intercom001 (built only `intercom__admin_metrics` of 2 required); analytics_engineerin (built only `obt_customer_reporting` of 2 required) |
| ephemeral-not-materialized | 0 | — (output-contract README lands BASE-TABLE materialization board-wide) |
| correct-artifact-still-fail | 0 | — |
| packaging-fault (non-signal) | 1 | chinook001 (gold DB lacks the required dim/fct/obt tables) |

Method: each fail's gold `condition_tabs` were read from its `tests/spider2_eval.jsonl`; the built-table
state was confirmed against each cell's solver session jsonl (the agent's final
`information_schema.tables` probe — BASE TABLE vs VIEW vs absent), not the agent's self-reported
"0 mismatches". The plain-`mismatch` verifier string is ambiguous (a missing predicted table and a
wrong-values table both produce it, because `duckdb_match` wraps the predicted fetch in try/except),
so the artifact read is what separates the buckets.

## Behavioral analysis

**The captain's question — WHY does the agent get answers wrong:** on 38 of 42 fails the agent builds
the *correctly-named* gold table(s), materialized as a BASE TABLE, with plausible columns, and
self-validates green — but the **analytic content diverges from the unstated gold semantics**. This is
the oracle-blind wall: the agent has no gold to check against, picks a defensible interpretation of an
under-specified instruction, and its own self-validation is correlated with its own choice (the
recurring self-anchored false-green). The output-contract README already solved the *shape* problem
(correct names + BASE-TABLE materialization, 0 ephemeral fails); the residual is *value* correctness.

**Method adherence:** high. Every sampled cell ran the prescribed flow — read the dbt project, added/
edited the target model, `dbt build`, then a Python `information_schema` + row/grain self-probe. The
agents reliably land the output contract. They do NOT reliably land the gold values.

Representative evidence (built artifact + gold, per bucket):

- **jira001** (grain) — agent built `jira__project_enhanced` as BASE TABLE, **row_count 2**; gold
  `jira__project_enhanced` has **3 rows**. Correct name/materialization, wrong grain — the agent's
  project-eligibility/join produced fewer rows than gold. Distance: small (off by one project row).
- **tpch001** (values) — built `client_purchase_status` BASE TABLE, 76,777 rows, plausible derived
  columns (lifetime_value, return_pct, customer_status='red'); a value mismatch on at least one
  column-vector under column-containment. Self-probe green.
- **xero001 / retail001** (values/grain) — built `xero__balance_sheet_report` (345 rows) and
  `report_customer_invoices` (10 rows, one per country) as BASE TABLEs with sensible schemas; values
  diverge from gold's financial-aggregation conventions. Both self-validated "looks correct."
- **chinook001** (packaging, non-signal) — agent built `dim_customer`/`fct_invoice`/`obt_invoice` as
  BASE TABLEs; failure is entirely gold-side (gold DB lacks those tables). NOT a content failure.

**The 3 wrong-table-name fails are a distinct, more tractable mechanism:**

- **intercom001** and **analytics_engineerin** are **multi-table-target misses** — the gold requires
  TWO output tables (`intercom__company_metrics` + `intercom__admin_metrics`; `fact_purchase_order` +
  `obt_customer_reporting`) but the agent built only ONE and reported "COMPLETE." The agent stopped at
  the first deliverable named in the instruction and never produced the second. The missing table's
  predicted fetch raises → plain mismatch.
- **movie_recomm001** built `original_programs` (9,675 rows, keyed by program_id) — a table matching
  the instruction's surface wording ("original programs … categorize by genre and renewal status") —
  but the gold table is `user_watched_movies`. A name/scope misidentification.

**Why the passers pass:** the 19 sentinels are cells where the instruction's deliverable is
unambiguous enough that the agent's single defensible interpretation coincides with gold (e.g. the
seed dbt package already ships the gold model logic, or the metric is fully specified).

**Distance-to-pass is generally not visible** beyond "mismatch": the verifier emits only
`spider2-dbt verify: mismatch` for 41 of 42 fails (chinook001 is the lone detailed error). Under
column-containment a single diverging gold column-vector fails the whole table, so a cell can be
"one column off" or "entirely wrong" and report identically. Future value-level levers cannot read a
fine-grained distance from the verifier — they must reason from the built table vs gold directly.

## Failure Review

Not an unexpected result — this is the anchor, there is no prior expectation to violate. Two findings
worth carrying forward:

1. **The smoke mis-classified chinook001.** The 6-task smoke called it `ephemeral-not-materialized`
   (CTE never a base table). The full-board artifact read overturns that: the agent builds all three
   tables as BASE TABLEs; the gold DB is the defect. Lesson: on the smoke, the missing-table signal was
   read as a *predicted-side* ephemeral failure when it was a *gold-side* packaging fault — the two are
   indistinguishable from the plain `mismatch`/catalog-error string without reading both the built table
   AND the gold DB. The ephemeral bucket is empty on the full board.

2. **The verifier's `mismatch` string is non-diagnostic** for 41/42 fails. `duckdb_match` wraps the
   predicted-table fetch in try/except → False, so missing-table and wrong-values collapse to the same
   output. Bucketing required artifact-level reads of each cell's solver session jsonl. Any future
   analyze must do the same; do not infer the bucket from the verifier string alone.

## Follow-up Routing

- **task-gap-ranking re-derived** from this run's `per_trial_outcomes.json` →
  `_artifacts/task-gap-ranking.md` (AC-3 satisfied). The bucket counts bound the lever families.
- **spd0002 (materialization lever) has NO live target** — 0 ephemeral fails. Do not file it; the
  output-contract seed README already solved materialization board-wide.
- **Highest-confidence next lever = completeness / multi-table-target** (build EVERY deliverable the
  instruction enumerates): targets intercom001 + analytics_engineerin (both built 1 of 2 required
  tables), possibly movie_recomm001. Small, artifact-checkable, off the oracle-blind wall.
- **Value-level semantic forks** address the 38-cell grain/values bucket but face the oracle-blind wall
  (ade-bench/DAB priors: generative "pin the semantics" rules are usually inert on the real ambiguity).
  Pick cells where the instruction under-specifies a *nameable* convention; expect a low hit-rate.
- Promotion of this run to `@baseline` is the captain's decision at conclude (AC-2 binding step).

## Verdict

## Stage Report: analyze

- DONE: Record the absolute pass rate with a clean strict-audit attestation in `## Run result`
  19/61 = 0.3115 via `rk score`; `rk audit --policy strict` = 61 clean / 0 coverage_missing / 0 tainted; 0 cells errored.
- DONE: treat any build-time preflight failure or packager crash as a NON-SIGNAL packaging fault (name it, exclude it)
  chinook001 named as packaging-fault(non-signal) — gold DB lacks the required dim/fct/obt tables (gold-side Catalog Error), excluded from content.
- DONE: Write the full 61-task ledger in `## Run result` — every task PASS/FAIL — and bucket each FAIL into exactly one failure class; give per-bucket counts
  19 PASS listed; 42 FAIL bucketed: wrong-columns-or-grain 38 / wrong-table-name 3 / ephemeral-not-materialized 0 / correct-artifact-still-fail 0 / packaging-fault 1.
- DONE: In `## Behavioral analysis`, answer WHY the agent produces wrong answers, from committed artifact + verifier stdout + transcripts across every non-trivial bucket
  Dominant mechanism = oracle-blind value/grain divergence on a correctly-named, materialized BASE TABLE (jira001 2-vs-3 rows, tpch001, xero001, retail001 cited); distinct multi-table-target miss (intercom001/analytics_engineerin) and name miss (movie_recomm001); chinook001 gold-side.
- DONE: re-derive `_artifacts/task-gap-ranking.md` from per_trial_outcomes.json
  Rewritten with live 19/61 board, bucket counts, sentinels, and ideation order.

### Summary

Anchor full run scored 19/61 = 0.3115 on a clean strict audit (0 coverage_missing, 0 tainted, 0
errored). The output-contract README has fully solved table-name + BASE-TABLE materialization (0
ephemeral fails board-wide); the residual failures are dominated by the oracle-blind wall — 38 of 42
fails build the correctly-named gold table but produce values/grain that diverge from the unstated
gold semantics and self-validate green. Three fails are a more tractable wrong-table-name family (two
are multi-table-target misses where the agent built 1 of 2 required tables). One fail (chinook001) is a
non-signal packaging fault: the gold DB itself lacks the tables the eval spec demands. Two corrections
banked: the smoke's "ephemeral" label for chinook001 is overturned (it is a packaging fault), and the
verifier's plain `mismatch` string is non-diagnostic so bucketing required per-cell artifact reads.
No promotion performed — @baseline binding is the captain's call at conclude.
