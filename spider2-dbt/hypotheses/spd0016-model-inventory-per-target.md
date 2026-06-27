---
id: spd0016
title: Model-inventory per-target grain/PK contract — validate every dimensional target separately, not just the final report
status: smoke
kind: hypothesis
source: "day-queue-2026-06-26 Queue 4; forks champion @baseline spd0013-lean-lag-period-over-period; discovery smoke-only (no full)"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Large multi-target dimensional marts build many plausible tables and pass `dbt build`, but one
dimension/fact GRAIN, ID mapping, or support relation is subtly wrong — and the worker only validates
the final report, not each target separately.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow **per-target model-inventory** clause to its router/Implementation guidance:

> For a multi-target mart (≥2 graded/declared target tables), before editing SQL write a one-line
> inventory PER target: target name · declared grain · source grain · primary key · required support
> refs. Then implement and VALIDATE EACH target separately against its own inventory line (its grain key
> is unique, its row set matches the declared grain, its support refs resolve) — do NOT declare done on
> the final report alone. A subtly-wrong dimension/fact grain or ID mapping in a non-final target fails
> the hidden comparison even when `dbt build` is green.

Derived from the project's own declarations/sources (oracle-free, no gold baked); leak-safe. NO other
change; no-fetch leak guard byte-identical to spd0013.

Primary targets (all never-pass at champion = 0; `analytics_engineering001` dropped — not in the gradeable
60-board): `atp_tour001`, `superstore001`, `tickit002`, `tpch001`, `provider001`, `scd001`.

**Survey caveat (recorded for honest yield):** `scd001` (unstable `row_number` tiebreak) and `atp_tour001`
(frozen-clock spine) were flagged NOT-reachable by the 2026-06-25 survey — included for coverage but the
realistic reachable pool is `superstore001`, `tickit002`, `tpch001`, `provider001`.

## Pre-smoke Decision-Fork Probe

**Discovery hypothesis — reachability per the 2026-06-25 survey** (superstore001 downstream-FK gap,
tickit002 sibling-grain, tpch001 genuine-difficulty, provider001 full-dim-LEFT-join were REACHABLE/PROBABLE;
scd001/atp_tour001 NOT-reachable). No per-task offline reconstruction for this breadth sweep; the smoke
tests **steerability** of the per-target inventory+separate-validation contract. Fork per target: worker
validates only the final report and ships a subtly-wrong non-final grain (champion control = FAIL) vs
worker writes a per-target inventory and validates each separately (proposed). Discriminator: each graded
target matches gold under column-containment.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
Forks `spd0013`, adds ONLY the per-target inventory clause. Leak guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — Discovery smoke useful iff ≥2 primary targets become new ever-pass with NO hard-canary
regression.** 1 flip = bank, no full. 0 flips = conclude/reject unless artifact gives a concrete second
blocker. NO full-run, NO promote.

## Smoke Plan

Two-step, smoke-only, no full:

- **Small smoke** (~8 cells): reachable subset `superstore001`, `tickit002`, `tpch001`, `provider001`
  + core canaries `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`.
- **Large smoke** (~14 cells): all 6 primary targets + full hard-canary panel (activity001,
  app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001,
  quickbooks002).

## Gatekeeper review

**Fork parent resolved:** `@baseline` → `runs/spd0013-lean-lag-period-over-period/7f3278d0d61d2577`,
`agent.solver_workflow: solver_workflows/spd0013-lean-lag-period-over-period` — matches the hypothesis
`source:` field. No disagreement.

- **G1 — Single idea, single change:** PASS — README diff is purely additive (`291a292,305`): one hunk
  inserting the per-target model-inventory clause immediately before the Implementation-stage gated-rules
  block. No deletions, exactly one idea.
- **G2 — Leak-guard intact:** PASS — added lines contain no forbidden tokens (no
  `gold`/`expected_`/`answer_key`/`ground_truth`/`curl`/`wget`/`git clone`); the no-fetch prose
  (README lines 11-12) is byte-untouched.
- **G3 — Full spec scope:** PASS — frozen-vs-frozen diff shows ONLY `experiment:`, `solver_workflow:`,
  `solver_workflow_content_hash` (auto), `sealed_hash` (auto), `harness_git_sha` (auto checkout drift),
  provenance `solver_workflow_hash` (auto). `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`,
  `reasoning_effort: xhigh`, `trials: 1` all preserved. (Unfrozen `full-baseline.yaml` diff is
  formatting/normalization only — fork was from the canonical frozen baseline, the spd0015 pattern.)
- **G4 — Smoke narrows only tasks:** PASS — both smoke specs change ONLY `benchmark.tasks`; no
  `exclude_tasks`. Small=8, Large=14; all 6 primary targets present in the LARGE smoke; all 8 canaries
  are currently-PASSING sentinels.
- **G5 — Frozen, kind/runtime preserved:** PASS — all three frozen files exist; each carries
  `kind: spacedock_solver` + `runtime: codex`.
- **G6 — Resolver fidelity:** PASS — inserted text matches the claim 1:1 (one-line inventory per target +
  validate each separately on PK-unique / row-set-vs-declared-grain / support-refs-resolve; "do NOT
  declare done on the FINAL report alone"). Validation is independent/structural, NOT self-anchored.
- **G7 — Actionability (WARN-only):** PASS — concrete mechanical instruction (literal delimited inventory
  line + three nameable assertions), low inert-risk.
- **G8 — Regression-canary coverage:** N/A (PASS) — the clause is GATED to multi-target marts (≥2
  declared/graded targets), not generative; FAIL bar does not apply. 8 passing non-target canaries carried
  regardless.
- **G9 — Selector independence:** N/A — no multi-candidate / selector protocol.
- **G10 — Self-correcting false-positive risk:** PASS — gated (not generative), checks are STRUCTURAL
  invariants from the project's own declarations (not a re-derivation against the solver's own answer),
  and it triggers investigation ("do NOT declare done") rather than mandating a replace. Safe class.

**Overall: APPROVE** — purely additive, leak-safe, correctly frozen and scoped; the one new clause is
gated, structurally-anchored, and faithful to the claim, with no FAIL on any rule.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the champion: cp -r solver_workflows/spd0013-lean-lag-period-over-period solver_workflows/spd0016-model-inventory-per-target
  Forked; pre-edit README sha matched champion (b44236af).
- DONE: Edit ONLY README.md to add the ONE per-target model-inventory clause (router/Implementation guidance)
  Added 14-line gated clause at the head of the Implementation-stage gated-rules block; diff `291a292,305`, 0 deletions.
- DONE: Keep no-external-reference / leak-guard prose byte-intact; NO gold values/counts/dtypes/task-table-names baked
  Leak-guard lines 12-23 byte-identical to spd0013; no forbidden tokens in added lines.
- DONE: Do NOT relocate or delete any existing spd0013 guidance -- only ADD the one clause
  diff is purely additive (single insertion hunk, no deletions).
- DONE: Create full spec from full-baseline.frozen.yaml; set experiment + solver_workflow; drop stale baseline content-hash; rk freeze FROM REPO ROOT
  Froze from /home/kent/autobench/spider2-dbt with --allow-missing (model_resolved_version null, spd0015 pattern).
- DONE: Create SMALL smoke spec (8 tasks)
  --explain -> Tasks: 8 (superstore001, tickit002, tpch001, provider001, apple_store001, google_play001, mrr001, quickbooks002).
- DONE: Create LARGE smoke spec (14 tasks)
  --explain -> Tasks: 14 (6 primaries + 8 hard canaries).
- DONE: Freeze ALL THREE from repo root; verify solver_workflow_content_hash non-null and differs from baseline 9660d413
  All three = sha256:b899b831... (non-null, differs from 9660d413).
- DONE: Verify smoke selections via --explain (8 / 14)
  Confirmed above.
- DONE: Confirm full-spec frozen diff vs baseline = ONLY experiment + solver_workflow (+ auto hashes); kind/runtime preserved; README diff = ONLY added clause
  Frozen-vs-frozen diff = experiment/solver_workflow/content_hash/sealed_hash/solver_workflow_hash/harness_git_sha (all auto); spacedock_solver+codex preserved.
- DONE: Run gatekeeper review subagent; write the ## Gatekeeper review block
  Gatekeeper returned APPROVE, all G1-G10 PASS/N/A, no FAILs; block appended.
- DONE: Do NOT launch any rk run beyond --explain. Commit. Stop; FO auto-advances to smoke.
  Only --explain + freeze run; committing now.

### Summary

Forked champion spd0013 into spd0016 and added ONE gated per-target model-inventory clause to the
Implementation stage (write a one-line inventory per target, then validate each target SEPARATELY on
PK-uniqueness / row-set-vs-declared-grain / support-refs-resolve, not just the final report). README diff
is purely additive (14 lines, 0 deletions), leak-guard byte-intact, no gold baked. Built + froze full +
small(8) + large(14) specs from the repo root; content hash b899b831 (non-null, differs from baseline
9660d413). Gatekeeper APPROVE with no FAILs. Per the propose auto-gate, this auto-advances to smoke.
