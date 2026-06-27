---
id: spd0015
title: Report value-semantics contract — grain-aware COUNT, raw-grain preservation, independent value-recheck (not order/top-N)
status: propose
kind: hypothesis
source: "day-queue-2026-06-26 Queue 2; forks champion @baseline spd0013-lean-lag-period-over-period; discovery smoke-only (no full)"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Several never-pass tasks produce the expected named report tables and pass `dbt build`, but the graded
**values** are off — wrong distinctness (`COUNT(*)` vs `COUNT(DISTINCT)`), a collapsed/regrouped grain,
sign, rolling/period semantics, or row-set scope — and the worker's self-validation only checks row
ORDER / top-N, which hides the value mismatch (self-anchored false-green, the recurring spider2-dbt wall).

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow **report value-semantics contract** clause to its existing G3 COLUMN-VALUE CONTRACT guidance:

> For a report/aggregate target, pin three things from LOCAL evidence before trusting `dbt build`:
> (1) **grain-aware distinctness** — choose `COUNT(*)` vs `COUNT(DISTINCT key)` from BOTH the metric
> name AND the local source grain: if one source row already IS the countable entity use `COUNT(*)`;
> if multiple source rows map to one entity (a fan-out join or a repeated key) use `COUNT(DISTINCT)`;
> (2) **raw-grain preservation** — group at the report grain the task names; do NOT pre-aggregate or
> re-group onto a canonicalized/lookup value that collapses rows the gold keeps separate;
> (3) **independent value-recheck** — before declaring done, recompute at least one report metric a
> SECOND, independent way (e.g. a direct `COUNT`/`SUM` over the source filtered to the report scope)
> and confirm it equals the built table's value. A clean `dbt build` and correct row ORDER / top-N are
> NOT sufficient — order-only checks hide value mismatches.

Derived from the metric name + local source grain (oracle-free, no gold values/counts baked); leak-safe.
NO other change; no-fetch leak guard byte-identical to spd0013.

Primary targets (all never-pass at champion = 0): `flicks001`, `movie_recomm001`, `nba001`,
`playbook002`, `twilio001`, `xero001`, `xero_new002`, `quickbooks001`.

## Pre-smoke Decision-Fork Probe

**Discovery hypothesis — reachability per the 2026-06-25 resolution survey** (these were
REACHABLE_VERIFIED/PROBABLE; "most artifacts already build clean base tables" per the day-queue, so the
gap is value semantics, not existence). No per-task offline reconstruction for this breadth sweep; the
smoke tests **steerability** of the report value-semantics contract. Fork per target: worker emits the
named report table with values off on distinctness/grain/sign/scope, self-validated by order/top-N
(champion control = FAIL) vs worker pins grain-aware distinctness + raw grain + independent value-recheck
(proposed). Artifact discriminator: the graded report value matches gold under column-containment.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
Forks `spd0013`, adds ONLY the report value-semantics clause. Leak guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — Discovery smoke useful iff ≥2 primary targets become new ever-pass with NO hard-canary
regression.** 1 flip = bank, no full. 0 flips = conclude/reject unless artifact gives a concrete second
blocker. NO full-run, NO promote.

## Smoke Plan

Two-step, smoke-only, no full:

- **Small smoke** (~8 cells): primary subset `flicks001`, `nba001`, `twilio001`, `xero001` + core
  canaries `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`.
- **Large smoke** (~16 cells): all 8 primary targets + full hard-canary panel (activity001,
  app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001,
  quickbooks002).

## Gatekeeper review

**Recommendation: APPROVE** — pure-addition of exactly the one gated report value-semantics clause to the existing G3 COLUMN-VALUE CONTRACT section; leak-guard byte-intact, frozen specs preserve kind/runtime/model/trials, both smoke panels narrow only `benchmark.tasks` and carry all currently-passing hard canaries, and the independent-value-recheck is anchored to a raw source (not the solver's own build).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-27.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | `diff spd0013→spd0015 README` = single append-only hunk `231a232,253`; one "REPORT VALUE-SEMANTICS CONTRACT" clause added inside the existing Axis-2 G3 COLUMN-VALUE CONTRACT section (right after COUNT-by-NAME). No deletions, no relocation, no other section touched. |
| G2 leak-guard (hidden gold) | PASS | No-fetch para (README lines 11-16) byte-identical to parent. Added lines have no `curl/wget/git clone/git ls-remote/expected_/answer_key/ground_truth`; the lone `gold` hit ("collapses rows the gold keeps separate") is generic conceptual prose mirroring the parent's PRESERVE-THE-RAW-GROUPING-KEY rule — does not name the hidden gold table or enumerate gold columns. No instruction to read any `*gold*`/expected file. |
| G3 spec two fields | PASS | Frozen full diff (`full-baseline.frozen.yaml` vs `spd0015…frozen.yaml`) changes only `experiment:` and `agent.solver_workflow:`(+its content_hash) plus frozen-provenance metadata (sealed_hash/harness_git_sha/solver_workflow_hash). `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh`, `trials: 1` all preserved (grep-confirmed identical). |
| G4 smoke narrows tasks only | PASS | Both smoke frozen diffs vs full change ONLY the `benchmark.tasks:` list; no `exclude_tasks`, no other field. `--explain` on smoke-large frozen = `Tasks: 16`, smoke-small = `Tasks: 8`. Large panel (the canary panel) = all 8 hypothesis targets + 8 hard canaries; small = 4 targets + 4 canaries. Union covers every named target; every canary is a currently-PASSING @baseline task (reward 1.0). |
| G5 both frozen | PASS | `spd0015…frozen.yaml`, `.smoke-small.frozen.yaml`, `.smoke-large.frozen.yaml` all present; each carries `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the `## Hypothesis` claim's 3 parts verbatim (grain-aware distinctness / raw-grain preservation / independent value-recheck); no added scope. Part (3)'s recheck is anchored to an INDEPENDENT source — "a direct `COUNT`/`SUM` over the source filtered to the report scope" — not self-anchored to the solver's own build; explicitly rejects the order-only false-green. |
| G7 actionability/inert-risk | WARN | Mostly mechanical (a named second-recomputation step over the source, a concrete COUNT*/COUNT(DISTINCT) rule), but parts (1)-(2) lean on abstract analytic judgment ("group at the report grain the task names", "how many source rows map to one entity") with no worked-example skeleton — at gpt-5.5/xhigh that altitude carries inert-risk (discussed-but-not-applied). WARN-only, does not move the recommendation. |
| G8 regression-canary coverage | N/A | Gated, not generative — fires only when "the target is a report/aggregate (`*_report`/`*_rollup`/overview or any named metric table)". The precondition is the isolation mechanism. (The large smoke carries 8 perturbable currently-passing canaries incl. report-grain families apple_store001/google_play001/app_reporting.) |
| G9 selector independence | N/A | No multi-candidate / selector protocol declared. |
| G10 self-correcting false-positive | PASS | Part (3) is a validate-and-act lever. (a) Scope: gated to report/aggregate targets. (b) Independence: reconciles against a separately-sourced signal (direct COUNT/SUM over the raw source filtered to report scope), NOT a re-run of the solver's own derivation. (c) Check-don't-replace: "confirm it equals" / "a value that disagrees… is still wrong" triggers investigation; no mandate to replace a model with a structurally-different one. |

**For the captain:** Auto-approved to smoke. Pure additive single-clause gated lever on the champion spd0013 (@baseline 27/60); both frozen smoke panels validated via `--explain` (large=16: 8 never-pass targets all 0.0 + 8 passing hard canaries all 1.0; small=8). One WARN only (G7): parts (1)-(2) of the clause are abstract analytic prose without a worked skeleton, so the smoke is also a test of whether report value-semantics is steerable at all at gpt-5.5/xhigh or behaviorally inert — watch the smoke artifacts for "discussed but committed model unchanged."

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the champion (cp -r solver_workflows/spd0013-lean-lag-period-over-period solver_workflows/spd0015-report-value-semantics)
  Forked; README started byte-identical to spd0013.
- DONE: Edit ONLY README.md to add the ONE report value-semantics contract clause in the existing G3 COLUMN-VALUE CONTRACT section
  Single append-only hunk after the COUNT-by-NAME clause; 3 parts (grain-aware distinctness extending COUNT-by-NAME with local source grain; raw-grain preservation cross-referencing the G2 PRESERVE-THE-RAW-GROUPING-KEY rule; independent value-recheck via a direct COUNT/SUM over the source).
- DONE: Keep the no-external-reference / leak-guard prose byte-intact; embed NO gold values/counts/dtypes/task-table-names
  No-fetch para byte-identical; added lines carry no gold table names/columns/dtypes; only generic conceptual prose.
- DONE: Do NOT relocate or delete any existing spd0013 guidance — only ADD the one clause
  `diff` = `231a232,253`, pure addition, zero deletions, zero relocations.
- DONE: Create full spec; set experiment + solver_workflow; drop stale baseline content-hash
  specs/spd0015-report-value-semantics.yaml; frozen content_hash recomputed to d337de0c (≠ baseline 9660d413).
- DONE: Create SMALL smoke spec (8 tasks)
  specs/spd0015-report-value-semantics.smoke-small.yaml; --explain = Tasks: 8.
- DONE: Create LARGE smoke spec (16 tasks)
  specs/spd0015-report-value-semantics.smoke-large.yaml; --explain = Tasks: 16.
- DONE: Freeze ALL THREE with rk freeze --allow-missing
  All three .frozen.yaml written; content_hash populated only after freezing from the spider2-dbt repo root (relative solver_workflow resolves to cwd; freezing from ade-bench left it null — re-froze correctly).
- DONE: Verify smoke selections via --explain (8 / 16)
  smoke-small.frozen = Tasks: 8; smoke-large.frozen = Tasks: 16.
- DONE: Confirm full-spec frozen diff = only experiment + solver_workflow (+ auto hashes); kind/runtime preserved; README diff = only added clause
  Frozen diff = experiment, solver_workflow(+content_hash), sealed_hash, harness_git_sha, solver_workflow_hash (all auto); kind: spacedock_solver / runtime: codex preserved.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block
  Recommendation APPROVE (no FAILs; one WARN on G7 actionability/inert-risk); block appended above.
- DONE: Do NOT launch any rk run beyond --explain. Commit. Stop; FO auto-advances to smoke.
  Only --explain run; committing now.

### Summary

Forked champion spd0013 into spd0015 and added ONE precondition-gated "REPORT VALUE-SEMANTICS CONTRACT" clause to the existing G3 COLUMN-VALUE CONTRACT section: grain-aware distinctness (extends COUNT-by-NAME with local source grain), raw-grain preservation (cross-references the G2 raw-grouping-key rule), and an independent value-recheck (recompute a metric a second way over the source — not order/top-N self-anchoring). Built and froze all three specs (full + small-8 + large-16); the full-spec frozen diff is exactly experiment + solver_workflow + auto hashes with kind/runtime preserved, and the README diff is a pure 22-line addition with leak-guard byte-intact. Gatekeeper recommends APPROVE with one G7 WARN (parts 1-2 lean abstract without a worked skeleton → the smoke also tests whether report value-semantics is steerable at all at gpt-5.5/xhigh). NOTE: freeze must be run from the spider2-dbt repo root or the relative solver_workflow path leaves solver_workflow_content_hash null.
