---
id: spd0020
title: Preserve-all-rows LEFT join for reference/dimension tables — never INNER-join-away or filter NULL keys
status: propose
kind: hypothesis
source: "never-pass-residual-catalog-2026-06-27 (provider001 diagnosis); forks champion @baseline spd0013; discovery smoke-only; FINAL sprint hypothesis"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Offline diagnosis of `provider001` (catalog 2026-06-27) found a DETERMINISTIC, oracle-free residual on
BOTH graded tables: the champion INNER-joined / filtered rows that gold keeps. `specialty_mapping` gold =
874 (all taxonomy codes, NULL specialty where the Medicare crosswalk is unmatched) but champion kept only
460 matched; `provider` gold = 85196 (all NPIs) but champion filtered to entity_type ∈ {1,2}, dropping the
2857 NULL-entity-type NPIs → 82339. Both tables reproduce gold EXACTLY with a LEFT join that preserves all
reference rows.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow clause to its grain/coverage guidance:

> When a target is a reference/dimension/crosswalk table built from a full entity set (e.g. "all
> taxonomy codes", "all providers/NPIs", a complete code list), preserve EVERY row of that base set:
> LEFT-join the enrichment/crosswalk relations onto it and leave the enriched columns NULL when
> unmatched. Never INNER-join away unmatched rows, and never filter rows out on a NULL or "unknown"
> key/type/category value — a NULL attribute is a VALID row. Only the base-set's own existence defines
> the row count; joins must not shrink it.

Oracle-free (the "full set" intent + the FK-vs-attribute distinction are in the instruction/schema; no
gold values baked); gated (fires on a reference/dimension/crosswalk target built from a full base set).
NO other change; leak guard byte-identical to spd0013.

Primary target: `provider001` (flip + RELIABILITY test — in BOTH smokes for 2 draws; 2 attributable graded
tables).

## Pre-smoke Decision-Fork Probe

**Reachability PROVEN offline (catalog 2026-06-27, local source only):** both graded gold tables
(`specialty_mapping` 874, `provider` 85196) are reproduced EXACTLY by a LEFT-join-preserve-all-rows build;
the champion's INNER-join/NULL-filter gives 460/82339. Deterministic, oracle-free. The fork is behavioral:
does the preserve-all-rows directive steer the worker off its INNER-join/filter reflex. Discriminator: the
committed `specialty_mapping`/`provider` keep the full base-set row count (LEFT join, NULL where unmatched).

This is the COVERAGE family (spd0004 explored a blanket version, validated-not-promoted on variance) — but
this clause is SHARPER (a specific reference/full-set-preservation directive), and the residual here is a
clean, complete, two-table oracle-free fix (unlike tickit002/movie_recomm001 which had finer sub-residuals).

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.** Leak
guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — RELIABILITY: provider001 must pass in BOTH small and large smoke (2/2)** to count as a durable
flip; NO hard-canary regression (the clause must not suppress a LEGITIMATE inner-join filter and break a
passer — the coverage-family regression risk). NO full-run, NO promote (smoke-only discovery).

## Smoke Plan

Two-step, smoke-only, no full — provider001 in BOTH for a 2-draw reliability check:

- **Small smoke** (~7 cells): `provider001` + core canaries `apple_store001`, `google_play001`, `mrr001`,
  `quickbooks002`, `activity001`, `app_reporting001`.
- **Large smoke** (~11 cells): `provider001`, `superstore001` (other multi-table mart) + full hard-canary
  panel (activity001, app_reporting001, app_reporting002, apple_store001, google_play001, google_play002,
  mrr001, quickbooks002) + `mrr002` (perturbable coverage-shape canary).

## Gatekeeper review

Resolver = forked solver `solver_workflows/spd0020-preserve-all-rows-left-join` (parent: champion
`spd0013-lean-lag-period-over-period`, @baseline run `7f3278d0d61d2577`, 27/60). Subagent review:

- **G1 — Single idea, single change:** PASS — README diff vs parent is a single additive hunk
  (`342a343,353`), no deletions: the one "REFERENCE/DIMENSION/CROSSWALK FULL-SET PRESERVATION (gated)"
  clause, inserted right after the COVERAGE / COMPLETENESS gated rule in the grain/coverage guidance.
  No leak-guard / output-contract prose touched. One distinct idea.
- **G2 — Leak-guard intact:** PASS — grep over the 11 added lines for `gold|expected_|answer_key|curl|
  wget|git clone|git ls-remote|ground_truth` and for diagnosis values (`specialty_mapping`, `874`,
  `85196`, `82339`, NPI) returns NONE; only generic examples ("all taxonomy codes", "all providers").
  No-fetch paragraph byte-identical to parent.
- **G3 — Full spec differs in exactly two fields:** PASS — `experiment:` + `agent.solver_workflow:`
  changed; the content-hash line is the expected frozen-vs-unfrozen artifact (frozen full spec carries
  the new forked-solver hash `d37f2cee…`). `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`,
  `reasoning_effort: xhigh`, `trials: 1` preserved.
- **G4 — Smoke spec narrows only `benchmark.tasks`:** PASS (both smokes) — each diff vs full = only the
  task list; no `exclude_tasks`. SMALL=7, LARGE=11; target `provider001` in BOTH (2-draw reliability).
- **G5 — Both specs frozen, kind/runtime preserved:** PASS — all three frozen files exist; each carries
  `kind: spacedock_solver` + `runtime: codex` and the forked-solver content hash.
- **G6 — Resolver fidelity:** PASS — inserted text matches the hypothesis blockquote near-verbatim;
  generative-build guidance (join shape), not self-anchored validation. Adds an in-spirit contrast vs
  the per-key-aggregate rule (disambiguation, not new scope).
- **G7 — Actionability / inert-risk (WARN-only):** WARN — concrete join-shape directive but carries no
  BEFORE/AFTER SQL skeleton (unlike the adjacent PER-KEY / EXCLUDE-A-CATEGORY gated rules). Inert-risk:
  solver acknowledges "preserve all rows" yet still emits its INNER-join / entity_type-filter reflex.
  Advisory only; does not move the recommendation.
- **G8 — Regression-canary coverage:** PASS — lever is GATED (reference/dimension/crosswalk full-set
  targets only), not generative. Both smokes carry a strong non-target passing-canary panel from
  @baseline `7f3278d0d61d2577`; `mrr002` is the declared perturbable coverage-shape canary, apple_store001/
  app_reporting report-grain passers also perturbable. (`superstore001` is a baseline FAIL → second
  target/probe, not a canary.)
- **G9 — Selector independence:** N/A (PASS) — no multi-candidate / selector protocol declared.
- **G10 — Self-correcting lever false-positive risk:** N/A (PASS) — build/derivation instruction, not a
  validate-and-act-on-disagreement check; no value-rewriting machinery.

**Overall recommendation: APPROVE** — No FAILs (one advisory G7 WARN). README diff is the exact single
additive gated clause, leak-guard byte-identical, no gold baked; full spec differs only in `experiment:`/
`solver_workflow:` (+ auto hashes); all three frozen files preserve kind/runtime; both smokes narrow only
`benchmark.tasks` with `provider001` in both for the 2-draw reliability check + a rich canary panel.
**Captain watch (G7):** confirm in smoke artifacts that the full base-set row count is preserved (the
preserve-all directive actually landed, not acknowledged-then-skipped against the INNER-join reflex).

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the champion: cp -r solver_workflows/spd0013-lean-lag-period-over-period solver_workflows/spd0020-preserve-all-rows-left-join
  Forked; only README.md present in the new dir.
- DONE: Edit ONLY .../spd0020.../README.md to add the ONE preserve-all-rows clause (grain/coverage guidance)
  Added "REFERENCE/DIMENSION/CROSSWALK FULL-SET PRESERVATION (gated)" right after COVERAGE / COMPLETENESS; diff = single additive hunk 342a343,353, no deletions.
- DONE: Keep no-external-reference / leak-guard prose byte-intact; NO gold values/counts/dtypes/task-table-names baked
  grep for 874/85196/460/82339/specialty_mapping/provider/NPI/entity_type over added lines = NONE; no-fetch paragraph byte-identical.
- DONE: Do NOT relocate or delete any existing spd0013 guidance -- only ADD the one clause
  diff is purely additive (one hunk, 11 lines), zero deletions/moves.
- DONE: Create full spec; set experiment + solver_workflow (drop stale baseline content-hash); RUN rk freeze FROM REPO ROOT
  experiment: spd0020-preserve-all-rows-left-join, solver_workflow: ./solver_workflows/spd0020-preserve-all-rows-left-join, stale content-hash dropped; frozen content_hash d37f2cee (≠ baseline 9660d413).
- DONE: Create SMALL smoke spec (positive allowlist of exactly 7)
  specs/spd0020-preserve-all-rows-left-join.smoke-small.yaml: provider001, apple_store001, google_play001, mrr001, quickbooks002, activity001, app_reporting001.
- DONE: Create LARGE smoke spec (positive allowlist of exactly 11)
  specs/spd0020-preserve-all-rows-left-join.smoke-large.yaml: provider001, superstore001, activity001, app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001, mrr002, quickbooks002.
- DONE: Freeze ALL THREE from repo root; verify content_hash non-null + differs from baseline 9660d413
  All three frozen (--allow-missing, matching spd0013's model_resolved_version:null); content_hash d37f2cee non-null, ≠ 9660d413.
- DONE: Verify smoke selections: small --explain shows Tasks: 7; large --explain shows Tasks: 11
  rk run --explain: SMALL Tasks: 7, LARGE Tasks: 11.
- DONE: Confirm full-spec frozen diff vs full-baseline.frozen.yaml = ONLY experiment + solver_workflow (+ auto hashes); kind/runtime preserved; README diff = ONLY added clause
  Diff = experiment, solver_workflow(+content_hash), and auto provenance (sealed_hash, harness_git_sha, solver_workflow_hash); kind: spacedock_solver / runtime: codex preserved; README diff = single additive clause.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block
  Gatekeeper: APPROVE (no FAILs; one advisory G7 WARN — no BEFORE/AFTER skeleton). Block written.
- DONE: Do NOT launch any rk run beyond --explain. Commit. Stop; FO auto-advances to smoke.
  Only `rk freeze` and `rk run --explain` invoked; committing now.

### Summary

Forked champion spd0013 into spd0020 and added exactly ONE gated clause to the grain/coverage guidance:
preserve EVERY row of a reference/dimension/crosswalk target built from a full entity set (LEFT-join
enrichment, NULL when unmatched; never INNER-join-away; never filter on a NULL/"unknown" key/type/category
value). One knob; leak-guard byte-intact; no gold baked. Built + froze the full spec plus two smoke specs
(SMALL=7, LARGE=11) with provider001 in BOTH for a 2-draw reliability test. Gatekeeper APPROVE with one
advisory WARN (G7: no worked SQL skeleton → watch that the preserve-all directive lands, not just gets
acknowledged). No rk run beyond --explain.
