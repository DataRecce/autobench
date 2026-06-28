---
id: spd0024
title: Harness prototype — target-provided structural retry on provider001 (does handing the worker the source-derived target make it converge?)
status: conclude
kind: hypothesis
source: "spd0023 follow-up: the retry loop FIRED but couldn't converge because the worker can't reliably DERIVE the correct target structure. This prototype HANDS the worker the source-derived target (a deterministic count-check over the full reference SOURCE) + loop-until-pass, on provider001 only. In-scope README approximation of the agent-scaffold harness (razorback is read-only). Forks champion spd0013."
started: 2026-06-28
completed: 2026-06-28
verdict: REJECTED
score:
worktree:
archived: 2026-06-28T05:26:02Z
---

## Hypothesis

spd0023 proved the retry loop fires + rebuilds but can't converge multi-source cells because the worker
can't reliably derive WHAT the correct structure should be. **Prototype test:** if we HAND the worker the
exact target — a deterministic structural check computed from the SOURCE (not gold) — does provider001
converge? This isolates "target-derivation is the wall" from "executing the fix is the wall."

**One knob:** fork champion `spd0013` and add a provider001-gated self-check + loop that names the EXACT
source-derived target:

> After building `specialty_mapping` and `provider`, run these source-derived structural checks (compute
> EXPECTED from the SOURCE at runtime — never a literal number, never gold):
> - `specialty_mapping`: EXPECTED rows = `count(*)` of the FULL taxonomy reference source; if the built
>   count is lower you dropped unmatched reference rows → rebuild with a LEFT join keeping every reference
>   row (NULL crosswalk where unmatched).
> - `provider`: EXPECTED rows = `count(*)` of ALL NPIs in the source; if lower you filtered valid rows
>   (e.g. NULL entity type) → rebuild keeping all NPIs.
> Re-run the checks after each rebuild; finalize only when BOTH built counts equal their source-derived
> EXPECTED. Repeat up to 3×.

Oracle-free: EXPECTED is a `count(*)` over the named SOURCE reference/entity table, computed at runtime; no
gold value, count, or table is read. Gated to the provider001 shape (a reference/crosswalk + full-NPI
target). NO other change; leak guard byte-identical to spd0013.

## Pre-smoke Decision-Fork Probe

Reachability proven offline (catalog: provider001 = full nucc 874 + all NPIs 85196, both LEFT-join). The
fork: spd0023 let the worker derive the target (0/3); this HANDS it the source-derived target. If
provider001 now converges ≥2/3, target-derivation was the wall → build the general harness. If it still
fails, the wall is executing-the-fix itself → stop. Discriminator: built specialty_mapping/provider row
counts reach their source-derived EXPECTED across draws.

## Acceptance criteria

**AC-1 — README-only; forks spd0013; adds ONLY the provider001-gated target-check+loop. NO hardcoded counts,
NO gold read** (oracle-safety: EXPECTED is a runtime source `count(*)`). Leak guard byte-identical.
**AC-2 — clean strict audit.**
**AC-3 — trials=3: provider001 ≥2/3 = concept proven (build general harness); 0/3 = wall is deeper, stop.**
Canaries hold. NO promote w/o captain sign-off.

## Smoke Plan

trials=3, ~5 cells: provider001 (target) + canaries apple_store001, google_play001, mrr001, quickbooks002.

## Gatekeeper review

**Recommendation: APPROVE** — single gated source-derived structural retry-loop appended to the spd0013 champion README; EXPECTED row counts are runtime `count(*)` over two confirmed solver-visible sources (`nppes.nucc_taxonomy`, `nppes.npi`), no count literal (874/85196/460/82339 or any) and no gold/tests/expected read on any added line; leak-guard byte-identical; smoke-only prototype deviations are captain-sanctioned.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-28.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | Pure append at `377a378` (31 lines, zero `<` deletions); one idea = a provider001-shape-gated "source-derived structural target check + rebuild loop"; no leak-guard/output-contract prose edited. |
| G2 leak-guard (hidden gold) | PASS | Added lines name only sources `{{ source('nppes','nucc_taxonomy') }}` / `{{ source('nppes','npi') }}`; the strings `gold/tests/expected` occur ONLY in NEGATIVE clauses ("NEVER a value read from gold/tests/expected", "never reads any gold, tests, expected, or verifier table"); no `curl/wget/git clone/ls-remote/http`; no-fetch paragraph (README lines 11–13) byte-identical to parent. |
| G3 spec two fields | PASS (prototype-noted) | No full spec exists (smoke-only prototype). Vs champion SMOKE spec, only ABOUTME comments, `experiment`, `agent.solver_workflow`, `benchmark.tasks` (5-task allowlist), and `trials` differ. `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh` preserved. `trials: 3` is the DELIBERATE 3-draw convergence design (not a violation). |
| G4 smoke narrows tasks only | PASS | Smoke `tasks` = provider001 (target, named in `## Hypothesis`) + 4 canaries; no `exclude_tasks` block. Acts as its own full spec; the only non-`benchmark.tasks` deltas are the intentional prototype fields noted in G3. Target task present. |
| G5 both frozen | PASS (prototype-noted) | `…smoke.frozen.yaml` present, carries `kind: spacedock_solver` + `runtime: codex` + `solver_workflow_content_hash`. Non-smoke `.frozen.yaml` absent by design (no full spec in this smoke-only prototype) — not a missing-artifact FAIL. |
| G6 resolver fidelity | PASS | Inserted text matches the `## Hypothesis` blockquote claim in substance: per-model EXPECTED = `count(*)` over the named SOURCE, computed AT RUNTIME, "NEVER a literal number, NEVER gold", gated to the reference-crosswalk + full-entity shape, rebuild-LEFT-join, loop ≤3×. CRITICAL CHECK PASSES: EXPECTED is a structural row-count derived from a separately-sourced signal (the source roster `count(*)`), not the solver's own re-derivation; sources confirmed real & solver-visible in `_sources.yml` (nppes.npi, nppes.nucc_taxonomy), NOT gold. No self-anchored "verify your answer matches" phrasing. |
| G7 actionability/inert-risk | PASS | Concrete & mechanical: literal SQL count checks (`select count(*) from {{ source(...) }}`), a named rebuild action (LEFT join keeping every reference/NPI row), and a bounded loop with a finalize condition — not abstract "get the grain right" prose. |
| G8 regression-canary coverage | N/A (PASS) | Lever is GATED — fires ONLY on the `specialty_mapping`+`provider` reference-crosswalk/full-roster shape (nppes sources). The 4 canaries (apple_store001, google_play001, mrr001, quickbooks002 — all 1.0 at @baseline) are non-target families with no such shape, so the gate is structurally disjoint and the lever cannot fire on them; they serve as gate-leak detectors. provider001 confirmed 0.0 at @baseline (correct target). |
| G9 selector independence | N/A (PASS) | Not a multi-candidate/selector protocol — single build + structural retry, no N-candidate generation or selection. |
| G10 self-correcting false-positive | PASS | Self-correcting (validate-and-rebuild) lever. (a) Scope: gated to the provider001 shape, does not fire on already-correct canaries. (b) Independence: checks a STRUCTURAL row-count invariant against a SEPARATELY-SOURCED signal — `count(*)` over the raw source roster, NOT a re-run of the solver's own derivation; oracle-free (no gold/expected/count literal). (c) Check-don't-replace direction is one-way and structurally motivated (rebuild ONLY when built count < source count → restore dropped rows via LEFT join), not "replace with a structurally different model"; finalize-with-best fallback after 3 caps the loop. |

**For the captain:** Auto-approved to smoke. CRITICAL CHECK CONFIRMED — EXPECTED row counts are computed at runtime via `count(*)` over solver-visible SOURCE tables (`nppes.nucc_taxonomy`, `nppes.npi`, both declared in provider001's `_sources.yml`, neither gold); no forbidden literal (874/85196/460/82339 or any multi-digit number) and no gold/tests/expected/verifier read appears on any added line (those tokens occur only in the lever's own negative leak-guard clauses). Two captain-sanctioned prototype deviations noted, did NOT FAIL: (1) smoke-only — no full spec/full-frozen exists, so G3/G4/G5 were verified directly against the spd0013 champion SMOKE spec; (2) `trials: 3` is the deliberate 3-draw convergence design. Smoke set = provider001 (target, 0.0 @baseline) + 4 non-target passing canaries (all 1.0 @baseline) acting as gate-leak sentinels; the lever is gated to the reference-crosswalk shape and disjoint from those families.

## Smoke result

## Verdict

## Stage Report: propose

- DONE: inspect _views/spider2-dbt-provider001 to identify exact source table names
  `models/_sources.yml` declares source `nppes` (schema `main`) with tables `npi`, `nucc_taxonomy`, `medicare_specialty_crosswalk`; confirmed via duckdb: `nucc_taxonomy`=874 (FULL taxonomy ref), `npi`=85196 (ALL NPIs). Only SOURCE tables read, not gold.
- DONE: Fork the champion (cp -r spd0013 → spd0024)
  `solver_workflows/spd0024-target-provided-retry-provider001/README.md` created.
- DONE: Edit ONLY README.md to add ONE gated stage with actual source names
  Added "SOURCE-DERIVED STRUCTURAL TARGET CHECK + REBUILD LOOP" block; EXPECTED = `count(*)` over `{{ source('nppes','nucc_taxonomy') }}` (specialty_mapping) and `{{ source('nppes','npi') }}` (provider); LEFT-join rebuild keeping all reference rows / all NPIs; ≤3 cycles.
- DONE: ORACLE-SAFETY — EXPECTED is runtime count(*) over SOURCE, no hardcoded count, no gold/tests/expected ref
  grep of added lines: zero of 874/85196/460/82339/558; "gold/tests/expected" appear only in NEGATIVE leak-guard clauses. Gatekeeper independently confirmed.
- DONE: Keep no-external-reference / leak-guard prose byte-intact
  `diff` of README lines 12–16 (no-fetch paragraph) = byte-identical to spd0013.
- DONE: Do NOT relocate/delete existing spd0013 guidance; only ADD the one gated stage
  `diff` = single hunk `377a378,408` (pure append, zero deletions).
- DONE: Create trials=3 spec with 5-task allowlist; drop stale baseline content-hash
  `specs/spd0024-target-provided-retry-provider001.smoke.yaml`: experiment + solver_workflow set, trials:3, tasks = provider001/apple_store001/google_play001/mrr001/quickbooks002. Unfrozen spec carries no content-hash.
- DONE: Freeze from REPO ROOT; verify content_hash non-null + differs from 9660d413; trials:3; --explain Tasks: 5
  Frozen `solver_workflow_content_hash: sha256:bc73b82c…` (differs from baseline 9660d413); trials:3; `rk run --explain` → `Tasks: 5`, $0.
- DONE: README diff vs spd0013 = ONLY added gated stage; grep CONFIRMS no hardcoded gold counts / no gold-file refs
  Verified above (pure append, no forbidden literals, no gold/tests/expected reads).
- DONE: Run gatekeeper review subagent (harness-prototype, captain-approved); write review block; verify EXPECTED source-runtime-derived
  Gatekeeper APPROVE — all G1–G10 PASS/N/A; explicitly confirmed EXPECTED is runtime `count(*)` over source, not a baked number. Block written above.
- DONE: Do NOT launch any rk run beyond $0 --explain; commit; stop
  Only `--explain` ($0) run; committing now; FO owns the run launch.

### Summary

Forked the spd0013 champion solver into spd0024 and added exactly one gated stage: a provider001-shape source-derived structural retry loop that computes EXPECTED row counts at runtime via `count(*)` over the SOURCE tables `nppes.nucc_taxonomy` (full taxonomy reference) and `nppes.npi` (all NPIs), then LEFT-join-rebuilds any model that dropped rows (≤3 cycles). Oracle-safety verified by grep and by the gatekeeper: no hardcoded counts, no gold/tests/expected reads, leak-guard byte-intact. Smoke spec (trials=3, 5 tasks) frozen with a content-hash distinct from baseline 9660d413; `--explain` confirms Tasks: 5. Gatekeeper recommendation APPROVE.


## Smoke result + Verdict

**REJECTED — target-provision does NOT converge provider001 (0/3); the wall is EXECUTING the fix, not deriving/checking it.**
trials=3 `runs/spd0024-target-provided-retry-provider001/ceb6d07620748157` (5 cells, strict audit CLEAN 15/0/0).
provider001 0/3; canaries hold (quickbooks002 2/3 = variance).

**Artifact-proven:** the worker RAN the provided source-count checks (count over nppes.nucc_taxonomy 18×,
nppes.npi 8×), SAW the gaps (logged nucc 874 / crosswalk 558 / its built ~460 / npi 85196 vs 82339), and
REBUILT 3×. Still 0/3. So target-provision + forced check + retry all occurred and it still didn't converge.

**The wall, located precisely:** NOT target-derivation (spd0023), NOT check-discipline (checks ran) — it is
reliably EXECUTING the multi-table fix. provider001's residual is row-set-reproducible (catalog: LEFT-join →
gold exactly), so this isn't a value-oracle problem; the worker simply can't reliably write the correct
LEFT-join (join key / no dedup / keep-all) across rebuilds — the SQL execution is the varying part.

**Implication for the harness path:** an external harness forces the check + hands the target, but still
relies on the LLM worker to write the correct rebuild SQL — exactly the varying part. So multi-table
provider001-class cells will NOT converge via any LLM-worker harness. Only asana001-class cells (where the
worker's natural single-table build IS the fix) land reliably. Bears on spd0025 (the three-worker loop's
Validate worker is also oracle-blind / the Implement worker has the same execution variance).
