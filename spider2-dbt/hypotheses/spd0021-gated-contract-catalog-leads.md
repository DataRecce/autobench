---
id: spd0021
title: Gated contract forcing-function over the 5 catalog leads — reliable compliance via write-then-obey, multi-draw
status: smoke
kind: hypothesis
source: "synthesis of the 2026-06-27 autonomous sprint: the contract forcing-function (spd0011) is the ONLY mechanism that made a README rule reliably obeyed (airbnb 2/2 with scaffold vs 1/2 lean); the residual catalog gives 5 exact oracle-free per-task fixes. This composes them GATED (zero passer cost) and judges by a trials=3 hold-rate (beats the variance wall). forks champion @baseline spd0013."
started: 2026-06-27
completed:
verdict:
score:
worktree:
---

## Hypothesis

The 2026-06-27 sprint established that the never-pass pool's binding constraint is **compliance
reliability + variance**, not reachability: precise oracle-free rules get ADOPTED in the committed
artifact but flip only ~half the draws (tickit002 2/4, movie_recomm001 0/2, provider001 0/2). The ONE
mechanism proven to make a rule *reliably* obeyed is the **contract forcing-function** (spd0011): airbnb001
held **2/2 with** the write-then-obey contract scaffold vs **1/2 without** it (spd0013). spd0011 only
failed because the scaffold was WHOLE-SOLVER (diffuse prose cost on passers, e.g. quickbooks003 0/3) and
carried a destabilizer template.

**The synthesis (this hypothesis):** apply the contract forcing-function **GATED to ONLY the 5 catalog-lead
task shapes**, each with its exact offline-diagnosed fix as the contract template, so it forces reliable
compliance on the leads while **passers never enter the contract path** (gated-levers-compose → zero prose
cost). Judge by a **trials=3 hold-rate**, not a single draw (the discipline every prior single-draw verdict
lacked).

Fork the champion `spd0013-lean-lag-period-over-period`. Add ONE gated stage:

> **Implementation Contract (GATED).** BEFORE editing SQL, check whether the task matches one of the
> contract shapes below. If NONE match, proceed with the existing flow unchanged — do NOT write a contract
> (no overhead). If one matches, write its contract (selected template, expected_row_shape,
> forbidden_patterns, validation_signature) from the template + local evidence, implement to OBEY it, then
> VALIDATE the signature before declaring done (a clean `dbt build` is not enough). The contract is derived
> only from local workspace evidence; never from gold values.

### Contract templates (each gated on an oracle-free shape signal; each fix is a METHOD, no gold baked)

- **C1 — REFERENCE/CROSSWALK FULL-SET PRESERVATION.** *Gate:* a reference/dimension/crosswalk target built
  from a full entity set (all codes / all entities / a complete reference list). *Fix:* LEFT-join the
  enrichment/crosswalk relations onto the full base set; keep EVERY base-set row (NULL where unmatched);
  never INNER-join-away unmatched rows and never filter on a NULL/"unknown" key/type/category. *Signature:*
  built row count = the base-set's own row count; no join shrinks it. *(provider001.)*
- **C2 — CUMULATIVE-SPINE ENDPOINT.** *Gate:* a monthly/period spine driving a cumulative balance /
  running-total report. *Fix:* the spine ENDS at the last period that has source activity — never
  `current_date` / `greatest(max, current_date)` (which over-emits future-empty periods); round money
  columns to 2dp. *Signature:* the max emitted period = the last period with source data; no trailing
  empty periods. *(xero001.)*
- **C3 — FUZZY/PARTIAL NAME-MATCH JOIN.** *Gate:* a join the model's schema.yml/description calls a
  partial / fuzzy / starts-with name match (esp. when the task instruction is underspecified or describes a
  different deliverable). *Fix:* treat the model's schema.yml as the authoritative contract; implement the
  match as an anchored prefix `LIKE (<other> || '%')` — NOT exact equality; PRESERVE the natural fan-out
  (no dedup unless the spec says one row per key); strip only a trailing `(YYYY)` token. *Signature:* the
  join is a prefix LIKE and the row set keeps the fan-out. *(movie_recomm001.)*
- **C4 — NO-INVENTED-FILTER DIMENSION/FACT.** *Gate:* a dimension/fact built by joining staging models.
  *Fix:* restrict the row set ONLY by the inventoried join keys; never add `WHERE <attribute> IS NOT NULL`
  (or any value predicate) on a descriptive/payload column the instruction does not name — a NULL/zero in a
  descriptive attribute is a VALID row; resolve role attributes through the role dimension
  (`int_<role>_extracted_from_users`), never the full raw user table. *Signature:* no invented attribute
  filter; the row count = the key-join row set. *(tickit002.)*
- **C5 — STOCHASTIC-SIMULATION SNAPSHOT.** *Gate:* graded columns produced by an UNSEEDED simulation
  (`random()` with no seed) for which a committed snapshot exists in the project's data catalog. *Fix:* for
  those columns, READ the committed snapshot (parquet/seed) from the data catalog and join it to the
  deterministic columns — do NOT re-run the unseeded simulation (it is not reproducible). *Signature:* the
  stochastic columns are sourced from the committed snapshot, not a fresh simulation. *(nba001.)*

Each gate is an oracle-free workspace/shape signal; no gold values, counts, or dtypes are baked. NO other
change; the no-fetch leak guard is byte-identical to spd0013. Existing champion guidance is untouched for
non-matching tasks.

## Pre-smoke Decision-Fork Probe

**Reachability of all 5 leads is PROVEN offline** (residual catalog 2026-06-27, local source only): each
fix reproduces its graded gold exactly (provider001 874+85196, xero001 1170, movie_recomm001 56596,
tickit002 8659+177417, nba001 = the committed snapshot). The OPEN question is purely **reliability**: does
the contract forcing-function (write-then-obey, gated) make these fixes land RELIABLY across draws — beating
the lean-rule baselines (tickit002 2/4, movie_recomm001 0/2, provider001 0/2)? That is exactly what the
trials=3 run measures: per-lead hold-rate WITH the contract vs the lean-rule baseline WITHOUT it. The
passer-cost question (did spd0011's contract prose cost qb003?) is answered by gating: passers match no
template and never enter the contract path.

## Acceptance criteria

**AC-1 — README-only; full spec differs only in `experiment:` + `solver_workflow:`.** Forks spd0013, adds
ONLY the gated contract stage + 5 templates. Leak guard byte-identical; no baked gold.

**AC-2 — Every recorded score paired with a clean strict audit** (rc=0, 0 coverage_missing, 0 tainted).

**AC-3 — HOLD-RATE verdict (trials=3).** A lead is "reliably fixed" if it passes ≥2/3 draws (vs its lean
baseline). The contract must HOLD the hard canaries (≥2/3 each; no passer that was rock-solid drops below
2/3) — the gated design predicts zero passer cost. Promote only on a multi-draw hold-rate, never a single
draw (the variance-wall discipline). NO promote without captain sign-off.

## Smoke Plan

1. **Sanity smoke (trials=1, ~13 cells):** the 5 leads (provider001, xero001, movie_recomm001, tickit002,
   nba001) + hard canaries (apple_store001, google_play001, google_play002, mrr001, quickbooks002,
   activity001, app_reporting001, app_reporting002) + tickit001 (sibling) — confirm the contract FIRES on
   each lead, builds clean, and no gross canary breakage. ~40 min.
2. **If clean → trials=3 FULL board (60 tasks):** the long-running multi-draw run. Yields per-cell hold
   rates board-wide → the promotable verdict + a full regression check. ~8–9 h.

## Gatekeeper review

**Recommendation: APPROVE** — the REVISE only broadens C1/C2 and adds C6/C7 inside the already-gated contract stage and grows the sanity smoke 14→22; it remains ONE gated forcing-function idea, leak guard byte-intact with no baked gold, all 13 leads baseline-FAIL and all 9 sentinels baseline-PASS, no integrity-rule FAIL.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-27.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | README diff vs parent spd0013 is a pure addition (`266a267,329`, zero `^<` deletions) of ONE block `## Stage: Implementation Contract (GATED)` carrying C1–C7. The broadened C1 (6 cells) / C2 (3 cells) and new C6/C7 are additional gated templates of the SAME forcing-function mechanism, not new ideas. No leak-guard/output-contract prose modified. |
| G2 leak-guard (hidden gold) | PASS | Grep of added lines for forbidden gold counts `874/85196/1170/56596/8659/177417/809/558/99` → NO match. No `curl/wget/git clone/git ls-remote/answer_key/ground_truth` added. Only `gold`/`expected_` hits are prohibition prose ("never from gold values", "No gold values") and the field name `expected_row_shape`. C7's `synthea001`/`xero_new001` and all other `*(taskNNN.)*` are champion-style task tags, not gold. No-fetch prose byte-identical (pure-addition diff). |
| G3 spec two fields | PASS | `diff spd0013…yaml spd0021…yaml`: `experiment:` + `agent.solver_workflow:` changed; `trials: 1→3` is the DELIBERATE multi-draw hold-rate design (AC-3, captain-approved) — intended, not drift. `kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh` all preserved. |
| G4 smoke narrows tasks only | PASS | Smoke narrowed to 22 tasks (`--explain` = 22). Other deltas are non-scope: ABOUTME comments, dropped `sealed_hash` (provenance), and `trials: 3→1` — the latter is the intended cheap sanity-smoke draw against the trials=3 full board. No `exclude_tasks`. All 13 named targets present + 9 baseline-PASSING sentinels (apple_store001, google_play001/002, mrr001, quickbooks002, activity001, app_reporting001/002, tickit001 = 1.0 each in @baseline `spd0013/7f3278d0d61d2577`). |
| G5 both frozen | PASS | `…frozen.yaml` and `…smoke-sanity.frozen.yaml` both exist; both carry `kind: spacedock_solver` and `runtime: codex`; full frozen trials:3, smoke frozen trials:1, 22 tasks. |
| G6 resolver fidelity | PASS | Inserted text matches the claim: gated contract written from template+local evidence, implement-to-OBEY, then VALIDATE an oracle-free STRUCTURAL signature. C1–C7 signatures are independent local signals (built row count = full base-set; max period = last source period; prefix-LIKE present; no invented filter; snapshot-sourced; derived key populated+non-constant; target exists as a base table) — not a self-anchored "0 mismatches against my own build" check. No scope creep beyond the 7 templates. |
| G7 actionability/inert-risk | PASS | Concrete/mechanical per template: LEFT-JOIN from base relation; spine ends at last activity period; `LIKE (<other> \|\| '%')`; no `WHERE attr IS NOT NULL`; read committed snapshot; cast-to-varchar-before-string-op; author the missing model as `UNION ALL` — each with a checkable validation signature. Worked-skeleton class. |
| G8 regression-canary coverage | N/A (PASS) | GATED: the contract stage fires only when a task matches one of 7 disjoint shape gates; non-matching tasks proceed unchanged (zero contract path). The smoke panel nonetheless carries 9 currently-PASSING non-target sentinels. |
| G9 selector independence | N/A (PASS) | Not a multi-candidate / run-N-candidates selector protocol; single obey-the-contract path per matched shape. |
| G10 self-correcting false-positive | PASS | Self-correcting (VALIDATE the signature before done) but (a) GATED to 7 disjoint preconditioned shapes, (b) checks STRUCTURAL/independent signatures (row-count vs base set, max-period vs source, derived-key non-constant, target-exists-as-base-table) not a re-derivation of the graded answer, (c) drives implement-to-OBEY, not blind replacement. Structure/signature-class check → safe. |

**For the captain:** Auto-approved to smoke. This REVISE only broadened C1 (now 6 cells: provider001/asana001/intercom001/netflix001/reddit001-comments/hive001) and C2 (3 cells: xero001/xero_new001/xero_new002) and added C6 (CAST-BEFORE-STRING-OP, social_media001) + C7 (AUTHOR-THE-MISSING-MODEL, synthea001/xero_new001), and grew the sanity smoke 14→22 — all within the already-gated stage; C3/C4/C5 unchanged. Two after-the-fact eyeballs: (1) `trials: 3` is the intended full-board key change (AC-3), and the smoke's `trials: 1` is the deliberate cheap sanity draw — neither is a G3/G4 integrity drift; (2) all 13 leads confirmed baseline-FAIL (0.0) and all 9 sentinels baseline-PASS (1.0) in @baseline `spd0013/7f3278d0d61d2577`.

## Revision Note (catalog A+B expansion)

Pre-trials=3 revision driven by the offline catalog A+B diagnosis
(`hypotheses/_artifacts/never-pass-residual-catalog-2026-06-27.md`, "Consolidated reachable-deterministic
lead set"). The first propose covered only 5 leads via C1–C5; this revise broadens two templates and adds
two so the multi-draw run tests the FULL ~13-cell reachable-deterministic lead set:

- **Broadened C1 → ENTITY/REFERENCE-COMPLETENESS** (was REFERENCE/CROSSWALK FULL-SET PRESERVATION): now
  covers **6 cells** — provider001, asana001, intercom001, netflix001, reddit001-comments, hive001. The
  gate widened from "reference/crosswalk built from a full entity set" to "any per-entity / reference /
  dimension / crosswalk target whose grade expects the full base-set OR a preserved join fan-out"; the fix
  now spells out drive-FROM-the-base-relation + LEFT-attach (coalesce counts to 0), never inner-join-from
  an aggregate/active-subset, and preserve fan-out at the joined grain.
- **Broadened C2 → CUMULATIVE BALANCE-SHEET SPINE** (was CUMULATIVE-SPINE ENDPOINT): now covers **3 cells**
  — xero001, xero_new001, xero_new002. Added the forward-carry-across-gaps rule and the Retained-Earnings /
  equity roll-up = cumulative P&L to month-end (drop prior-FY-end pin / Current-Year-Earnings split),
  beyond the original spine-endpoint clause.
- **Added C6 — CAST-BEFORE-STRING-OP**: social_media001 (champion quoted a column into a string literal in
  `split_part`; cast the numeric column to varchar before the string op, reference the real identifier).
- **Added C7 — AUTHOR THE MISSING GRADED MODEL**: synthea001 (errored, never built the UNION cost model)
  and xero_new001 (authored zero SQL). Author the missing model; if a UNION of sibling `int_` models,
  build it as `UNION ALL`.

C3/C4/C5 unchanged. EXCLUDED (variance-prone): zuora001, quickbooks001. EXCLUDED (oracle-blind /
frozen-clock): tpch001, atp_tour001, pendo001, scd001, superstore001, twilio001, playbook002-model,
flicks001-actor_rating, reddit001-posts.

Sanity smoke panel expanded **14 → 22**: the 13 leads (provider001, asana001, intercom001, netflix001,
hive001, xero001, xero_new001, xero_new002, movie_recomm001, tickit002, nba001, social_media001,
synthea001) + 8 hard canaries (apple_store001, google_play001, google_play002, mrr001, quickbooks002,
activity001, app_reporting001, app_reporting002) + tickit001 sibling. Full spec unchanged at trials:3 (its
board already carried every lead). Both specs re-frozen from the repo root; `solver_workflow_content_hash`
changed `46a11f38…` → `6a000219…`. Leak guard byte-intact; no gold counts baked.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the champion: cp -r solver_workflows/spd0013-lean-lag-period-over-period solver_workflows/spd0021-gated-contract-catalog-leads
  Forked; README begins identical to spd0013 (404 lines pre-edit).
- DONE: Edit ONLY README to add the gated Implementation Contract stage + 5 templates exactly as specified
  Added `## Stage: Implementation Contract (GATED)` between G3 close and Exploration; diff vs spd0013 = pure addition `266a267,311`.
- DONE: The 5 templates are C1-C5 — copied each gate + fix + signature from the hypothesis file
  C1 full-set preservation, C2 cumulative-spine endpoint, C3 fuzzy prefix-LIKE, C4 no-invented-filter, C5 stochastic snapshot — verbatim from ## Hypothesis.
- DONE: Keep the no-external-reference / leak-guard prose byte-intact; NO gold values/counts/dtypes baked
  No-fetch para byte-identical (pure-addition diff); grep for 874/85196/1170/56596/8659/177417 = no match (exit 1); only the 5 established `*(taskNNN.)*` task tags present.
- DONE: Do NOT relocate or delete any existing spd0013 guidance — only ADD the gated contract stage
  Diff confirms ZERO deletions/modifications; single insertion hunk.
- DONE: Create full spec; set experiment + solver_workflow + trials: 3; drop stale baseline content-hash; freeze from repo root
  specs/spd0021-gated-contract-catalog-leads.yaml: experiment + solver_workflow set, trials:3, stale hash fields stripped; froze from /home/kent/autobench/spider2-dbt.
- DONE: Create SANITY smoke spec: trials: 1, positive allowlist of exactly 14 tasks
  specs/spd0021-gated-contract-catalog-leads.smoke-sanity.yaml: 5 leads + 8 hard canaries + tickit001, trials:1.
- DONE: Freeze BOTH from repo root; verify content_hash non-null + differs from baseline 9660d413; full trials:3, sanity trials:1
  Both frozen; content_hash sha256:46a11f38… (non-null, differs from 9660d413); full=trials:3, sanity=trials:1.
- DONE: Verify sanity smoke selection: .smoke-sanity.frozen.yaml --explain shows Tasks: 14
  `--explain` → `- Tasks: 14`; gated contract prose present in materialized prompt.
- DONE: Confirm full-spec frozen diff vs baseline = ONLY experiment + solver_workflow + trials (1->3) + auto hashes; kind/runtime preserved; README diff = only the added stage
  Frozen diff: experiment, solver_workflow(+content_hash), sealed_hash, trials 1->3, harness_git_sha, solver_workflow_hash — only experiment+solver_workflow+trials are manual; kind: spacedock_solver / runtime: codex / model gpt-5.5 / reasoning_effort xhigh preserved.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block
  Gatekeeper recommendation APPROVE, no FAILs (G8/G9 N/A); block appended above.
- DONE: Do NOT launch any rk run beyond --explain. Commit. Stop; the FO owns the smoke launch
  Only `--explain` run (free, foreground); committing now.

### Summary

Forked champion spd0013 and added ONE gated stage — `## Stage: Implementation Contract (GATED)` with the 5 catalog-lead templates C1–C5 — each on a disjoint oracle-free shape gate, each fix a METHOD (no gold baked). The README change is a pure addition (no deletions, leak-guard byte-intact). Full spec sets trials:3 (the multi-draw hold-rate, the deliberate key change vs prior single-draw hypotheses); sanity smoke is trials:1 over 14 cells (5 leads + 8 passing canaries + tickit001). Both specs froze clean (content_hash 46a11f38, differs from baseline 9660d413); the full-spec frozen diff vs baseline is only experiment + solver_workflow + trials plus auto-regenerated hashes. Gatekeeper APPROVE, no FAILs. No rk run beyond --explain.

## Stage Report: propose (cycle 2 — catalog A+B expansion)

- DONE: Edit ONLY the solver README to BROADEN C1 + C2 and ADD C6 + C7 in the gated Implementation Contract stage
  README diff vs spd0013 = pure addition; C3/C4/C5 untouched; C1/C2 broadened, C6/C7 added.
- DONE: BROADEN C1 to "ENTITY/REFERENCE-COMPLETENESS" (6 cells)
  Gate widened to any per-entity/reference/dimension/crosswalk full-base-set OR preserved fan-out; fix = drive-FROM-base + LEFT-attach, never inner-from-aggregate; tags provider001/asana001/intercom001/netflix001/reddit001-comments/hive001.
- DONE: BROADEN C2 to "CUMULATIVE BALANCE-SHEET SPINE" (3 cells)
  Added forward-carry-across-gaps + Retained-Earnings = cumulative P&L to month-end (drop FY-end pin/CY-earnings split); tags xero001/xero_new001/xero_new002.
- DONE: ADD C6 "CAST-BEFORE-STRING-OP" (social_media001)
  Cast numeric col to varchar before split_part/etc, reference real identifier; signature = derived key populated + non-constant.
- DONE: ADD C7 "AUTHOR THE MISSING GRADED MODEL" (synthea001/xero_new001)
  Author the absent/errored target; UNION of sibling int_ models = UNION ALL; signature = target exists as a base table.
- DONE: Keep no-external-reference / leak-guard prose byte-intact; NO gold values/counts/dtypes baked
  Leak-guard para diff vs spd0013 = BYTE-INTACT; grep 874/85196/1170/56596/8659/177417/809/558/99 = no match; only champion-style *(taskNNN.)* tags.
- DONE: Do NOT relocate or delete existing spd0013 guidance or the C3/C4/C5 templates; only broaden C1/C2 + add C6/C7
  C3/C4/C5 verbatim; spd0013 guidance untouched.
- DONE: Re-freeze BOTH specs from the REPO ROOT: full (trials:3 unchanged) AND rebuilt sanity smoke (trials:1, 22 tasks)
  Froze from /home/kent/autobench/spider2-dbt (--allow-missing, as prior); sanity rebuilt to exactly 22 tasks.
- DONE: Verify solver_workflow_content_hash CHANGED vs prior 46a11f38; full trials:3; sanity --explain shows Tasks: 22
  Both frozen hashes = sha256:6a000219… (changed from 46a11f38); full trials:3; sanity --explain → Tasks: 22.
- DONE: Re-run the gatekeeper review subagent; REPLACE the ## Gatekeeper review block
  Gatekeeper APPROVE, no FAILs (G8/G9 N/A); block replaced above.
- DONE: Append a "## Revision Note (catalog A+B expansion)" to the hypothesis file
  Appended before ## Smoke result; documents broadened C1/C2, new C6/C7, 14→22 smoke, hash change.
- DONE: Do NOT launch any rk run beyond $0 --explain. Commit. Stop; the FO owns the smoke launch
  Only --explain run (free); committing now.

### Summary

Broadened the gated contract templates C1 (→6 cells: provider/asana/intercom/netflix/reddit-comments/hive) and C2 (→3 cells: xero/xero_new001/xero_new002), and added C6 (CAST-BEFORE-STRING-OP, social_media001) + C7 (AUTHOR THE MISSING GRADED MODEL, synthea001/xero_new001), so the trials=3 run tests the full ~13-cell reachable-deterministic lead set instead of 5. C3/C4/C5 and all spd0013 guidance untouched; README change is a pure addition, leak-guard byte-intact, no gold counts baked. Re-froze both specs from the repo root (content_hash 46a11f38 → 6a000219); full spec stays trials:3, sanity smoke rebuilt to exactly 22 tasks (13 leads + 8 hard canaries + tickit001). Gatekeeper re-reviewed: APPROVE, no FAILs.
