---
id: spd0018
title: No invented attribute filter — restrict dim/fact row sets by inventoried join keys only, never by payload columns
status: propose
kind: hypothesis
source: "day-queue-2026-06-26 follow-up; per-task offline diagnosis of the spd0016 tickit002 variance near-miss; forks champion @baseline spd0013; discovery smoke-only"
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

Per-task offline diagnosis of `tickit002` (the spd0016 1/2 variance near-miss) found the pass↔fail
driver is a **deterministic SQL-shape choice with an oracle-free correct answer**, NOT irreducible
variance. The FAIL run added an INVENTED `WHERE venue_seats IS NOT NULL` filter on a non-key, non-graded,
instruction-unmentioned attribute, dropping 300 valid rows from `dim_events` (8659→8359) and failing the
row-count containment. The PASS run had no such filter and reproduced gold exactly (both `dim_events`
8659 and `fct_listings` 177417, symdiff 0, verified offline). A second divergence (joining the full user
table instead of `int_sellers_extracted_from_users`) is ALREADY covered by the champion's role-dimension
clause — the gap is the invented attribute filter.

**Single README change (one knob):** fork the champion `spd0013-lean-lag-period-over-period` and add ONE
narrow prohibition clause to its grain guidance:

> **Do not invent a row filter on a non-key attribute.** When building a dimension/fact by joining
> staging models, restrict the row set ONLY by the inventoried join keys (the FK inner-joins that define
> the declared grain). Never add a `WHERE <attribute> IS NOT NULL` — or any value predicate — on a
> descriptive/payload column the instruction does not name. A NULL or zero in a descriptive attribute is
> a VALID row; dropping it under-emits and fails the row-count gate. Filter rows on join keys, never on
> payload columns.

Oracle-free (the key-vs-attribute distinction is visible in the model SQL / schema, no gold values);
gated (fires when building a dim/fact by joining staging). NO other change; leak guard byte-identical.

Primary target: `tickit002` (flip + RELIABILITY test — must pass BOTH small and large smoke = 2/2 draws,
vs the 1/2 under spd0016). Bonus discovery: `provider001`, `superstore001` (other never-pass dim/fact
marts that may carry the same invented-filter or under-emit shape).

## Pre-smoke Decision-Fork Probe

**Reachability PROVEN offline (per-task reconstruction, local source only):** the PASS-run committed SQL
reproduces both graded gold tables EXACTLY (dim_events 8659 / fct_listings 177417, symdiff 0). The sole
flip driver is the invented `IS NOT NULL` attribute filter (under-emit) — a deterministic shape choice
with an oracle-free correct answer (keys define the row set; payload columns do not). The fork is purely
behavioral: does the prohibition clause suppress the stochastic "add a defensive `IS NOT NULL`" choice so
tickit002 passes RELIABLY (2/2) instead of 1/2. Discriminator: committed `dim_events` has no invented
attribute filter and the row set matches gold.

## Acceptance criteria

**AC-1 — Exactly the README change; full spec differs only in `experiment:` + `solver_workflow:`.**
Forks `spd0013`, adds ONLY the no-invented-attribute-filter clause. Leak guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — RELIABILITY: tickit002 must pass in BOTH the small and large smoke (2/2)** to count as a durable
flip (vs the spd0016 1/2 coin-flip). NO hard-canary regression (the clause is a prohibition — must not
suppress a LEGITIMATE key filter and break a passer). NO full-run, NO promote (smoke-only discovery).

## Smoke Plan

Two-step, smoke-only, no full — tickit002 in BOTH for a 2-draw reliability check:

- **Small smoke** (~8 cells): `tickit002`, `provider001`, `superstore001` + core canaries
  `apple_store001`, `google_play001`, `mrr001`, `quickbooks002`, `activity001`.
- **Large smoke** (~14 cells): `tickit002`, `provider001`, `superstore001`, `tpch001` + full hard-canary
  panel (activity001, app_reporting001, app_reporting002, apple_store001, google_play001, google_play002,
  mrr001, quickbooks002) + `tickit001` (sibling passer — must not break).

## Gatekeeper review

**Recommendation: APPROVE** — a single gated prohibition clause (one new Axis-2 G2 bullet) forked cleanly off the @baseline champion spd0013; leak guard byte-identical, specs differ only in identity fields, gated scope makes G8/G10 N/A, and the regression panel is well-stocked with perturbable + sibling canaries.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-27.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | README diff vs parent `spd0013-lean-lag-period-over-period` = `183a184,189`: exactly ONE added 6-line bullet "Do not invent a row filter on a non-key attribute" in the Axis-2 G2 over-emit section. Zero deletions, no leak-guard/output-contract prose touched. Single idea matching the falsifiable claim. |
| G2 leak-guard (hidden gold) | PASS | Grep over added (`^>`) lines for `gold/expected_/answer_key/curl/wget/git clone/git ls-remote/ground_truth/venue_seats/8659/177417/8359` = no match (exit 1). `tickit002` token count in README = 1 (the pre-existing `*[tickit002.]*` sibling tag from spd0013, unchanged). No-fetch paragraph region byte-identical to parent (diff exit 0). |
| G3 spec two fields | PASS | Frozen-vs-frozen (the dispatch built the full spec from `full-baseline.frozen.yaml`) shows only `experiment:`, `agent.solver_workflow:`, two auto content-hashes (`solver_workflow_content_hash`/`solver_workflow_hash`), recomputed `sealed_hash`, and `harness_git_sha` (environment provenance, not spec content). `kind: spacedock_solver` / `runtime: codex` / `model: gpt-5.5` / `reasoning_effort: xhigh` / top-level `trials: 1` / `concurrency.trials: 4` all preserved. The raw `full-baseline.yaml` diff is noisier (max_budget_usd, append_system_prompt, provenance block, list-indent reflow) but that is unfrozen-anchor serialization expansion, not spec-content change. |
| G4 smoke narrows tasks only | PASS | Both smoke diffs touch only `benchmark.tasks`; no `exclude_tasks` block. Small (8 tasks per `--explain`): tickit002, provider001, superstore001 + canaries apple_store001, google_play001, mrr001, quickbooks002, activity001. Large (13): adds tpch001, app_reporting001/002, google_play002, tickit001. Both include the named primary target `tickit002`; bonus targets provider001/superstore001 present in both. |
| G5 both frozen | PASS | `.frozen.yaml`, `.smoke-small.frozen.yaml`, `.smoke-large.frozen.yaml` all exist (3194/1772/1919 bytes, dated Jun 27). All three carry `kind: spacedock_solver` and `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text is verbatim the claim's clause and stays generative-in-form-but-gated ("When building a dimension/fact by joining staging models, restrict the row set ONLY by the inventoried join keys"). It tells the solver how to scope a row set against an oracle-free structural signal (keys vs payload columns visible in SQL/schema) — not a self-anchored "verify your answer matches gold" check. No scope creep beyond the one prohibition. |
| G7 actionability/inert-risk | WARN | The clause is a concrete mechanical prohibition (a named anti-pattern: "Never add a `WHERE <attribute> IS NOT NULL` … on a descriptive/payload column") which lands better than abstract prose, but it carries NO worked-example skeleton and is phrased as a prohibition (avoid X) rather than a positive edit. Mild inert-risk: at gpt-5.5/xhigh a "don't do X" rule can be acknowledged-but-not-applied. The 2/2 reliability AC is the right test for this. (WARN only; does not move the recommendation.) |
| G8 regression-canary coverage | N/A (PASS) | Gated, not generative: fires ONLY when "building a dimension/fact by joining staging models" — not every task. A prohibition scoped to a structural precondition → N/A per the gate clause. (Panel is nonetheless well-stocked: small smoke keeps 5 non-target passers, large adds 4 more incl. sibling passer tickit001 — covers the regression-by-over-suppression risk the captain flagged.) |
| G9 selector independence | N/A (PASS) | No multi-candidate / selector protocol declared; single gated clause. |
| G10 self-correcting false-positive | N/A (PASS) | Not a validate-and-fix / reconcile lever. It is a build-time scoping prohibition on how to write the join, not a "check the result and replace on disagreement" instruction — it never re-derives or rewrites a committed value against a second derivation. No false-green-flip surface. |

**For the captain:** Auto-approved to smoke. This is a clean one-bullet gated fork off the @baseline champion spd0013 (verified: `@baseline` resolves to `runs/spd0013-lean-lag-period-over-period/7f3278d0d61d2577`, matching `source:`). The only flag is the G7 WARN — a prohibition-style clause with no worked example carries some inert-risk; the AC-3 requirement that tickit002 pass BOTH smokes (2/2, vs the spd0016 1/2 coin-flip) is the right durability check. Note the prohibition's real downside is suppressing a LEGITIMATE key filter and breaking a passer — the large-smoke panel (sibling passer tickit001 + 8 hard canaries) is the relevant regression watch; audit those if any flip.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the champion: cp -r solver_workflows/spd0013-lean-lag-period-over-period solver_workflows/spd0018-no-invented-attribute-filter
  Forked; new dir contains README.md only (champion is README-only).
- DONE: Edit ONLY README.md to add the ONE no-invented-attribute-filter clause in the existing grain guidance
  Added one 6-line bullet in the Axis-2 G2 over-emit section (after the role-dimension bullet); README diff = `183a184,189`, zero deletions.
- DONE: Keep no-external-reference / leak-guard prose byte-intact; NO gold values/counts/dtypes/task-table-names baked
  grep for venue_seats/8659/177417/8359/dim_events/fct_listings = none; only token is the pre-existing `*[tickit002.]*` sibling tag (count 1, unchanged vs spd0013).
- DONE: Do NOT relocate or delete any existing spd0013 guidance — only ADD the one clause
  diff confirms pure addition, no moved/deleted lines.
- DONE: Create full spec, set experiment + solver_workflow, drop stale baseline content-hash, freeze from repo root
  specs/spd0018-no-invented-attribute-filter.yaml built from full-baseline.frozen.yaml; experiment+solver_workflow set, stale sealed_hash + solver_workflow_hash dropped; frozen from /home/kent/autobench/spider2-dbt.
- DONE: Create SMALL smoke spec (exactly 8 tasks)
  tickit002, provider001, superstore001, apple_store001, google_play001, mrr001, quickbooks002, activity001.
- DONE: Create LARGE smoke spec (exactly 13 tasks)
  tickit002, provider001, superstore001, tpch001, activity001, app_reporting001, app_reporting002, apple_store001, google_play001, google_play002, mrr001, quickbooks002, tickit001.
- DONE: Freeze ALL THREE from the repo root; verify content_hash non-null + differs from baseline 9660d413
  All three frozen (--allow-missing, mirrors spd0016); solver_workflow_content_hash = d2178732… (non-null, ≠ 9660d413).
- DONE: Verify smoke selections via --explain (8 / 13)
  smoke-small --explain → Tasks: 8; smoke-large --explain → Tasks: 13.
- DONE: Confirm full frozen diff vs full-baseline.frozen.yaml = only experiment + solver_workflow (+ auto hashes); kind/runtime preserved
  diff = experiment, solver_workflow, 2 content-hashes, recomputed sealed_hash, harness_git_sha (env provenance); kind: spacedock_solver / runtime: codex preserved.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block
  Subagent recommendation APPROVE (G1-G6 PASS, G7 WARN inert-risk only, G8/G9/G10 N/A); block appended above.
- DONE: Do NOT launch any rk run beyond --explain. Commit. Stop.
  Only --explain run; committing now; FO auto-advances to smoke.

### Summary

Forked the @baseline champion spd0013 and added exactly ONE gated prohibition clause ("Do not invent a row filter on a non-key attribute") to the Axis-2 G2 over-emit section — the per-task fix for the spd0016 tickit002 1/2 variance near-miss (the FAIL run invented an IS-NOT-NULL filter on a non-key payload column, under-emitting valid rows). The clause names the key-vs-payload distinction in general terms; no gold values, counts, or task table names baked. Built and froze all three specs (full + small/large smoke) from the repo root; smoke selections confirmed at 8 and 13 tasks, content hash d2178732… differs from baseline. Gatekeeper: APPROVE (sole flag a G7 WARN on prohibition-style inert-risk, which the 2/2 reliability AC is designed to test).
