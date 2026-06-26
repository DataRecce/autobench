---
id: spd0014
title: Declared-target closure — build every declared target/support model as a base table with exact convention naming
status: propose
kind: hypothesis
source: "day-queue-2026-06-26 Queue 1; forks champion @baseline spd0013-lean-lag-period-over-period; discovery smoke-only (no full)"
started: 2026-06-26
completed:
verdict:
score:
worktree:
---

## Hypothesis

Several never-pass tasks build *plausible* tables and pass `dbt build`, but the hidden comparison
still fails because one **declared** target or support model is missing, or the convention-correct
name is wrong — the worker stops at "the final report table exists" and never closes the full
declared model set.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add
ONE narrow clause to its existing router / Implementation guidance — a **declared-target-closure**
rule:

> Before finishing, enumerate every model the project DECLARES — every model named in `schema.yml`
> and every model referenced by the compiled manifest / `dbt ls` (including support and intermediate
> models the targets depend on). Build EACH declared model that the task asks to materialize as a
> BASE TABLE under the project's exact existing naming convention (match sibling prefixes/suffixes —
> `dim_`/`fct_`/`obt_`/`<pkg>__<entity>_<suffix>`). Do not stop when the final report table exists and
> `dbt build` is green: a task can declare several target/support models and the grader compares a
> specific one whose convention-correct name or base-table materialization you have not yet produced.
> Do NOT broadly rewrite existing passing models — only ADD/correct the missing declared targets.

Gated (fires when `schema.yml`/manifest declares multiple targets/support models), oracle-free (reads
the project's own declarations, never gold), leak-safe (no values/counts/dtypes baked). NO other
change; no-fetch leak guard byte-identical to spd0013.

Primary targets (all never-pass at champion = 0): `asana001`, `intercom001`, `netflix001`,
`pendo001`, `reddit001`, `social_media001`, `zuora001`, `xero_new001`.

## Pre-smoke Decision-Fork Probe

**Discovery hypothesis — reachability is per the 2026-06-25 resolution survey** (these targets were
mostly REACHABLE_VERIFIED/PROBABLE: declared-but-unbuilt or convention-name misses, not oracle-blind).
A per-task offline gold reconstruction is NOT run for this breadth sweep (8 targets); the smoke tests
**steerability** of the declared-target-closure rule — does naming "close the full declared set, not
just the final report" steer the worker to build the missing/mis-named declared target. The fork per
target: worker builds plausible tables + green `dbt build` (champion control = FAIL) vs worker closes
the full declared target set with convention-correct base tables (proposed). Artifact discriminator:
the graded target table exists as a convention-named base table AND the comparison passes.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
Forks `spd0013-lean-lag-period-over-period`, adds ONLY the declared-target-closure clause. Leak guard
byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — Discovery smoke is useful iff ≥2 primary targets become new ever-pass with NO hard-canary
regression** (day-queue rule). 1 flip = bank, do not full. 0 flips = conclude/reject unless artifact
gives a concrete second blocker. NO full-run, NO promote (smoke-only discovery).

## Smoke Plan

Two-step (small then large), smoke-only, no full:

- **Small smoke** (~8 cells): primary subset `asana001`, `netflix001`, `social_media001`, `zuora001`
  + core canaries `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`.
- **Large smoke** (~16 cells): all 8 primary targets + full hard-canary panel (activity001,
  app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001,
  quickbooks002).

## Gatekeeper review

**Recommendation: APPROVE** — a single gated, oracle-free declared-target-closure clause (R7) added to the router; full spec differs only in the two allowed fields; both smokes narrow only `benchmark.tasks` with a non-target hard-canary panel; all three frozen artifacts carry `kind: spacedock_solver` + `runtime: codex`. No FAILs.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-26.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | README diff adds exactly ONE idea: the `R7 — DECLARED-TARGET CLOSURE` rule in the Classify router (after R5/R6), plus the one router-sequence sentence updated to list R7's gate. No leak-guard/output-contract prose touched. |
| G2 leak-guard (hidden gold) | PASS | Grep over ADDED lines for `gold/expected_/answer_key/ground_truth/curl/wget/git clone/git ls-remote` → none. No-fetch paragraph byte-identical to parent. R7 reads only the project's OWN `schema.yml`/manifest/`dbt ls`, names a METHOD, bakes no values/counts/dtypes/gold-table-names. |
| G3 spec two fields | PASS | `diff full-baseline.yaml spd0014…yaml` shows only ABOUTME + `experiment:` + `agent.solver_workflow:`. `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1`, `concurrency.trials: 4`, `kind`/`runtime` all preserved. |
| G4 smoke narrows tasks only | PASS | Both smoke diffs change only ABOUTME + `benchmark.tasks:` (no `exclude_tasks`). LARGE (16, --explain confirmed) = all 8 named targets + 8 canaries (full target set). SMALL (8, --explain confirmed) = primary 4-subset + 4 canaries (deliberate primary-subset+canary step, not a missing-target FAIL). |
| G5 both frozen | PASS | All three frozen files exist (full + smoke-small + smoke-large); each carries `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted R7 matches the `## Hypothesis` claim: enumerate every declared model (schema.yml + manifest/`dbt ls`, incl. support/intermediate), build each as a BASE TABLE under the exact convention, don't stop at final-report+green-build, don't broadly rewrite passing models. Generative-but-gated and independent; not self-anchored "verify". |
| G7 actionability/inert-risk | PASS | Mechanical: names BASE TABLE materialization, a concrete naming pattern to match from siblings, and a concrete closure step (enumerate declared set; "all the tables exist" ≠ closed). Named existence/enumeration procedure → low inert-risk. |
| G8 regression-canary coverage | PASS | R7 is GATED (fires only when schema.yml/manifest declares MULTIPLE targets/support models) and ADD/correct-missing only. Both smokes carry a non-target passing canary panel (small: apple_store001, google_play001, mrr001, quickbooks002; large adds activity001, app_reporting001/002, google_play002) — ≥2 perturbable passers for the most-at-risk multi-model family. |
| G9 selector independence | N/A | No multi-candidate / selector protocol — single build. |
| G10 self-correcting false-positive | PASS | Structure/existence-class (declared set materialized as base tables under convention), gated to multi-target projects, ADD/correct-missing only, explicitly forbids rewriting passing models — cannot turn a right value wrong (spd0002 class). |

**For the captain:** Auto-approved to smoke. R7 is a gated, generative-but-scoped, structure-only closure rule reading the project's own declarations — leak-guard byte-identical, two-field spec diff, three frozen files clean. Discovery smoke-only (no full, no promote per AC-3): SMALL (8) = primary-4 + 4 canaries, LARGE (16) = all 8 named targets + 8-canary panel; the LARGE smoke carries the full named target set, SMALL is the intended primary-subset+canary step.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the champion: cp -r solver_workflows/spd0013-lean-lag-period-over-period solver_workflows/spd0014-declared-target-closure
  Forked; only README.md present in the new dir.
- DONE: Edit ONLY README.md to add the ONE declared-target-closure clause in the router / Implementation guidance
  Added `R7 — DECLARED-TARGET CLOSURE` to the Classify router (after R5/R6); diff = pure addition + one router-sequence sentence listing R7's gate.
- DONE: Keep the no-external-reference / leak-guard prose byte-intact; embed NO gold values/dtypes/counts/task-table-names
  Gatekeeper G2 PASS: no-fetch paragraph byte-identical; grep of added lines for gold/expected_/curl/git clone → none; R7 names a METHOD.
- DONE: Do NOT relocate or delete any existing spd0013 guidance — only ADD the one closure clause
  README diff (145a146,160) is a single insertion; no deletions; router/value-def/G2/LAG clauses untouched.
- DONE: Create full spec set experiment + solver_workflow; drop stale baseline content-hash so freeze recomputes
  specs/spd0014-declared-target-closure.yaml written from full-baseline.yaml source form; frozen recomputed solver_workflow_content_hash db64037….
- DONE: Create SMALL smoke spec (8 tasks)
  specs/spd0014-declared-target-closure.smoke-small.yaml: asana001, netflix001, social_media001, zuora001, apple_store001, google_play001, mrr001, quickbooks002.
- DONE: Create LARGE smoke spec (16 tasks)
  specs/spd0014-declared-target-closure.smoke-large.yaml: 8 primary targets + 8 hard canaries.
- DONE: Freeze ALL THREE with rk freeze --allow-missing
  All three wrote .frozen.yaml (full + smoke-small + smoke-large).
- DONE: Verify both smoke selections via --explain
  smoke-small.frozen → Tasks: 8; smoke-large.frozen → Tasks: 16.
- DONE: Confirm full-spec frozen diff shows ONLY experiment + solver_workflow (+ auto hashes); kind/runtime preserved; README diff = only the added clause
  Frozen full diff = experiment + solver_workflow(+content_hash) + sealed_hash + solver_workflow_hash + harness_git_sha (all auto); kind: spacedock_solver / runtime: codex preserved.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block
  Subagent applied G1–G10; APPROVE, no FAILs; block appended.
- DONE: Do NOT launch any rk run beyond --explain. Commit. Stop.
  Only --explain + freeze run; committing now.

### Summary

Forked spd0013 (= @baseline, 27/60) to spd0014 and added exactly ONE gated, oracle-free `R7 — DECLARED-TARGET CLOSURE` router clause: enumerate every model the project declares (schema.yml + manifest/dbt ls, incl. support/intermediate) and build each declared target the task asks to materialize as a base table under the project's exact naming convention, refusing to treat a green `dbt build` + final-report table as proof the declared set is closed; ADD/correct-missing only, no broad rewrite of passing models. Built + froze the full spec plus SMALL (8) and LARGE (16) smokes; --explain confirms 8/16; full-spec frozen diff is the two allowed fields plus auto hashes only. Gatekeeper recommends APPROVE (no FAILs). Smoke-only discovery — no full-run, no promote.
