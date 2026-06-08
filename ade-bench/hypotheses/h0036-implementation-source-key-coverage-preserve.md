---
id: h0036
title: Implementation — when a model must carry one row per raw-source key, a type change / dedup / join must NOT silently drop source rows; preserve full source-key coverage (never narrow a key to a type that drops non-conforming values), with a RAW-SOURCE coverage anti-join as the local acceptance signal
status: propose
kind: hypothesis
source: oracle-problem-systematic-program.md target-hunt (2026-06-08 LOW/Track-Z re-triage). SUPERSEDES the doomed h0021 (dedup tie-break that does not exist). The one new sharp-test-passing arbitrator the hunt produced. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-08T00:00:00Z
completed:
verdict:
score:
worktree:
---
## Hypothesis

`ana-eng007` (and its sibling `ana-eng007-medium`) is a **source-key COVERAGE** bug, NOT the
dedup tie-break the prior triage assumed. Ground truth, read from the @baseline run-dir
`622bdedac572b479` (`ade-bench-ana-eng007__zN8zRnV`) and the task dataset:

- The task's `environment/setup.sh` casts `products.id` to a string AND inserts **5 new product
  rows whose ids are `md5(id)`** of products 65/66/72/77/80 (non-numeric string ids). The hidden
  `solution__dim_products` seed therefore has **45 rows, 45 distinct product_ids, zero
  duplicates** — and the 5 differing rows the oracle reports are exactly those 5 hashed-id
  products.
- The oracle fails `AUTO_dim_products_equality` with **`Got 5`** (5/10 sub-checks; everything
  else passes). dbt_utils equality is a symmetric set-difference: 5 **missing** rows yields
  `Got 5`, whereas 5 *wrong-valued* rows would yield `Got 10` (5 each way). The odd,
  one-directional `Got 5` proves the solver's `dim_products` is **missing** the 5 hashed-id
  source rows — a coverage drop, not a value error.
- **Why the @baseline solver dropped them:** it mishandled the string-id type change — it cast
  `p.id` to `VARCHAR` in `dim_products` (a no-op, already string) while the 5 non-numeric md5
  ids were dropped somewhere in the lineage (an upstream narrowing cast / join that does not
  match non-numeric ids). Its agent summary claims a **"row preservation check passed 5/5
  models"** — a textbook **correlated false-green**: it reconciled row counts against its OWN
  intermediate output, never against the raw augmented `products` source, so it could not see
  that 5 raw-source ids never arrived.

**The independent arbitrator (passes THE SHARP TEST).** The correct `dim_products` must carry
**one row per distinct id in the raw `products` source** (a coverage/conservation relation the
answer MUST obey regardless of construction). The local, independent acceptance signal is a
**raw-source coverage anti-join**: `COUNT(DISTINCT id)` read from the **raw source** equals
`dim_products` row count, AND every distinct raw-source id appears in `dim_products` (anti-join
returns empty). This recomputes coverage from the raw source by a different route than the
model's own CTEs — the **f1007-hard mechanism, the loop's one proven independent catch** — and
is the opposite of the solver's self-anchored "preservation 5/5" check.

**The lever (single Implementation rule, construction-side edit-shape + a raw-source signal).**
Add one Implementation rule: when a model is meant to carry **one row per raw-source key** (a
dimension / per-entity table), a type change, dedup, or join MUST NOT silently drop source rows.
Specifically: never cast a key to a **narrower** type that discards non-conforming values (e.g.
casting an id column to integer when the source now holds non-numeric string ids drops those
rows); preserve every distinct source key through to the output. The acceptance signal is
structural and read against the **raw source**: every distinct raw-source key appears in the
output (a coverage anti-join over the raw source returns empty) — checked against the raw
source, NOT against the model's own intermediate and NOT against any expected count.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation rule that (a) frames a per-source-key model so that a type change/dedup/join
preserves full source-key coverage, (b) forbids narrowing a key's type in a way that drops
non-conforming values, and (c) uses a RAW-SOURCE coverage anti-join (distinct source keys all
present in the output) as the local acceptance signal — will flip `ana-eng007`
(`ade-bench-ana-eng007`), and plausibly `ana-eng007-medium`, from FAIL to PASS by recovering the
dropped source rows, raising `stratified_pass_at_1` above the `@baseline` 0.6458.

**What is and is NOT locally derivable (stated plainly).** That `dim_products` must cover every
raw-source product id, and that 5 ids are missing, is fully locally derivable (count distinct
ids in the raw `products` source vs the output; the md5 rows are deterministic copies of known
source rows). The exact *expected row count* lives only in the hidden seed and is NOT used by
this rule — the rule steers the EDIT SHAPE (preserve coverage; don't narrow the key type) and
its acceptance signal is the raw-source coverage anti-join, a relation the answer must obey, not
a target number. This is the f1007-hard independent-number shape, not the dead self-anchored
verify family (h0006/h0007/h0008/h0012), which read the solver's own logic.

**Why this escapes the dead-prose ceiling (and where it sits).** This is shaped like the one
in-stage rule that LANDED (h0019 anti-cross-join): a concrete edit-shape constraint with a
local STRUCTURAL acceptance signal, anchored to a concrete defect the @baseline transcript
exhibits (the dropped md5 rows), not an abstract restructure. The independent signal is the
f1007-hard raw-source recompute — the only mechanism that has ever caught a real error in this
loop. Honest caveat: whether construction prose makes gpt-5.5/xhigh actually preserve the
non-numeric ids is unproven and sits under the README-prose inertness ceiling; if smoke shows
`dim_products` still missing the hashed rows (coverage anti-join non-empty / `Got 5` unchanged),
the rule joins the ceiling and is REJECTED. `ana-eng007-medium` is a softer bet — its instruction
is a vague "the project is broken, fix it," and the @baseline solver there fixed an unrelated
break and never reached this issue; a flip on the medium variant is upside, not the core claim.

**Distinct from h0021 (DOOMED — being retired).** h0021 assumed a dedup tie-break and prescribed
`ORDER BY CAST(product_id AS INTEGER)` — but there are **zero** duplicate ids (no tie-break
exists), and casting to integer would **crash/NULL the 5 non-numeric md5 ids**, actively
breaking the very rows that must be preserved. h0036 is the opposite: it forbids narrowing the
key type and frames the bug as coverage, the correct mechanism the re-triage established.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset/harness/runtime change.
Leak-guard intact: the added text references only local artifacts (the model's own raw source
table, its key column, the output rows) and names no hidden `AUTO_*`/`solution__*`/`check_*`/
verifier/`_equality`/`_existence` test, no `equality test`/`has less columns`/`expected output
seed`, no `Got N` or hidden count, no specific hashed id values as a hardcoded list, and no
`curl`/`wget`/`git clone`/web fetch. The change touches exactly one `## Stage: Implementation`
block (inserted after the "...source, ref, macro, and schema patterns." sentence, before "Run
basic confirmation...") and leaves the leak-guard prose, Exploration, Validation, and
Finalization byte-identical. The spec differs from `@baseline` only in `experiment:` +
`solver_workflow:` (smoke may add only `benchmark.tasks`).

Target dataset (smoke, `ade-bench-` prefixed): the coverage-drop failures —
`ade-bench-ana-eng007` (primary) and `ade-bench-ana-eng007-medium` (sibling/upside). This rule
is **generative** (it fires on any per-source-key model carrying a type change), so per
gatekeeper G8 the smoke set carries a regression-canary panel of currently-passing @baseline
tasks (verified `reward=1` in `622bdedac572b479`), with **≥2 perturbable same-family canaries**
the lever can actually fire on:
- `ade-bench-ana-eng001`, `ade-bench-ana-eng002`, `ade-bench-ana-eng003` — perturbable ana-eng
  passers that build dimensions/per-entity models the coverage rule WILL fire on.
- `ade-bench-f1001` — non-package convention-bleed sentinel (must hold).
- `ade-bench-asana001`, `ade-bench-quickbooks002`, `ade-bench-airbnb001` — cross-family canaries.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0036-...yaml` shows only `experiment:` +
`solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md` touches only
`## Stage: Implementation` (the single coverage-preservation rule), leaves
Exploration/Validation/Finalization and the leak-guard prose byte-identical, and references no
hidden tests or weakens the leak-guard. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the artifact read + paired delta.** The smoke deep-dive reads the
committed `dim_products` (the dispatched-solver `apply_patch`/file payload, NOT transcript
chatter) and confirms whether the 5 previously-missing hashed-id source rows now APPEAR
(coverage recovered; `Got 5 → 0`), and that no canary regresses — especially that the rule did
not over-preserve rows on a model that legitimately filters (f1001 + the ana-eng canaries hold).
"row preservation passed" narration is NOT evidence (that was the @baseline's false-green); the
proof is the committed model carrying all distinct raw-source keys. Promote only if the paired
delta clears the tripwire on a clean audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on `ade-bench-ana-eng007` + `ade-bench-ana-eng007-medium` + the canary panel
(`ade-bench-ana-eng001`, `ade-bench-ana-eng002`, `ade-bench-ana-eng003`, `ade-bench-f1001`,
`ade-bench-asana001`, `ade-bench-quickbooks002`, `ade-bench-airbnb001`), the variant must not
regress any canary and should flip `ana-eng007` (the committed `dim_products` carries all
distinct raw-source ids) — verified by the artifact read, not chatter — before promotion to
full. CAPPED one-shot: if `dim_products` still drops the hashed rows, the rule joins the inert
ceiling and is REJECTED with no iteration.

## Gatekeeper review

**Recommendation: APPROVE** — single additive Implementation hunk, leak-guard byte-identical
with no hidden tokens or hardcoded hashed ids, full spec differs in exactly the two allowed
fields, smoke adds only `benchmark.tasks` carrying both targets + a regression panel with 3
perturbable ana-eng canaries, and the acceptance signal reconciles against the RAW SOURCE (not
the solver's own output), so it is independent rather than self-anchored.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-08T02:05:00Z.
Fork parent resolved: `solver_workflows/codex-ade-dbt-minimal` (hypothesis `source:` and `@baseline` run `622bdedac572b479` agree).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff` vs parent is one additive block `55a56,100`, entirely inside `## Stage: Implementation` (after "...source, ref, macro, and schema patterns.", before "Run basic confirmation..."); no other stage or guardrail line changed; one idea (source-key coverage preservation). |
| G2 leak-guard intact | PASS | No deletions in the diff, so the no-fetch/dependency/leak-guard paragraphs are byte-identical; token scan over added lines 56-100 returns 0 for AUTO_ / solution__ / _equality / _existence / check_ / verifier / "equality test" / "has less columns" / "expected output seed" / "Got " / curl / wget / git clone / git ls-remote; no md5 literal or hashed-id list (grep for md5/65/66/72/77/80/32-hex = none). |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0036-...yaml` = only line 2 `experiment:` and line 11 `solver_workflow:`; `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff` full vs smoke = only `23a24,33` adding `benchmark.tasks` (9 entries); all `ade-bench-` prefixed; both named targets (ana-eng007, ana-eng007-medium) present. |
| G5 both frozen | PASS | `…frozen.yaml` and `…smoke.frozen.yaml` both written; both carry `kind: spacedock_solver` + `runtime: codex` + `trials: 1`; smoke frozen lists all 9 tasks. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: Implementation stage, frames a per-source-key model to preserve full source-key coverage, forbids narrowing a key's type that drops non-conforming values, uses a RAW-SOURCE coverage anti-join as the local signal. Generative + independent (reconciles vs raw source by a different route), not the dead self-anchored "re-run/compare-to-own-output" family. |
| G7 actionability/inert-risk | PASS | Construction edit-shape rule carrying a copyable BEFORE/AFTER + anti-join SQL skeleton (the asana002/h0019 form), not abstract restructure prose. Honest residual inert-risk noted in body: README-prose inertness ceiling at gpt-5.5/xhigh is unproven for this case — flagged for the smoke artifact read. |
| G8 regression-canary coverage | PASS | Generative (fires on any per-source-key model with a type change). Panel covers each non-target family with a `@baseline` passer: f1 (f1001), asana (asana001), quickbooks (quickbooks002), airbnb (airbnb001); and the targets' own family carries 3 perturbable passers (ana-eng001/002/003) the coverage rule WILL fire on (≥2 satisfied). All 7 verified reward=1 in `622bdedac572b479`. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol; single solver session, single edit-shape rule. |
| G10 self-correcting false-positive | PASS | Not a fix-on-disagreement / replace lever: it is an edit-shape constraint (don't narrow the key) plus a local acceptance signal. The signal is **separately-sourced** — it reads the RAW SOURCE table + key column via an anti-join, NOT a CTE the model re-derives (axis b satisfied), and the rule explicitly does NOT mandate adding rows or replacing a legitimate business-rule filter (axis c — "check shape, don't over-preserve"). |

**For the captain:** Clean APPROVE — no FAILs. The one thing to weigh is the body's own honest caveat (G7): whether construction prose makes gpt-5.5/xhigh actually carry the non-numeric md5 ids is unproven and sits under the README-prose inertness ceiling. The smoke decision must read the committed `dim_products` artifact (does the coverage anti-join over raw `products` return empty / `Got 5 → 0`), not the solver's "row preservation passed" narration — that exact narration was the @baseline's self-anchored false-green (it reconciled only fact/obt row counts against its own intermediates, never dim_products vs raw products). Single-trial run; capped one-shot per the smoke gate.

## Stage Report: propose

- DONE: Fork the solver + insert ONE Implementation rule (after "...source, ref, macro, and schema patterns." before "Run basic confirmation...")
  `solver_workflows/h0036-implementation-source-key-coverage-preserve/README.md`; diff vs parent = one additive block `55a56,100`, all inside `## Stage: Implementation`; Exploration/Validation/Finalization + leak-guard (lines ~1-32) byte-identical (no deletions in diff).
- DONE: Leak-guard self-check over the added block
  Token scan of lines 56-100 = 0 hits for AUTO_/solution__/_equality/_existence/check_/verifier/"equality test"/"has less columns"/"expected output seed"/"Got "/curl/wget/git clone/git ls-remote; no md5 or hashed-id literals; acceptance signal phrased generically as a coverage anti-join over the RAW SOURCE by the key column (reads source, not solver output, not an expected number).
- DONE: Verify against ground truth before freezing
  @baseline run-dir `622bdedac572b479/ade-bench-ana-eng007__zN8zRnV`: (a) `AUTO_dim_products_equality` FAIL 5 / `Got 5 results` — one-directional (5 MISSING, coverage not value error); (b) `setup.sh` casts `products.id`→varchar and inserts `md5(id)` rows for `id::int 60..80` (the 5 non-numeric hashed source ids); (c) solver's "Row preservation check passed: fact_sales/obt_sales_overview 58, fact_inventory/obt_product_inventory 102" reconciled only its OWN intermediates, never dim_products vs raw products — the self-anchored false-green. COVERAGE framing confirmed (supersedes h0021 dedup); rule does NOT over-preserve (explicit "does not force ADD rows; a legitimate filter is fine").
- DONE: Full spec — set experiment + solver_workflow ONLY; preserve kind/runtime/trials:1
  `specs/h0036-...yaml`; `diff specs/baseline.yaml` = exactly lines 2 (`experiment:`) + 11 (`solver_workflow:`); `kind: spacedock_solver`, `runtime: codex`, `trials: 1` intact; trials NOT raised.
- DONE: Smoke spec — add ONLY benchmark.tasks with the 9 tasks
  `specs/h0036-...smoke.yaml`; diff vs full = only `23a24,33` (`benchmark.tasks`, 9 entries, all `ade-bench-` prefixed): ana-eng007 (TARGET), ana-eng007-medium (sibling), ana-eng001/002/003 (perturbable canaries), f1001 (sentinel), asana001/quickbooks002/airbnb001 (cross-family). trials NOT raised.
- DONE: Freeze BOTH specs (RAZORBACK_SPACEDOCK_PLUGIN_DIR exported)
  `…frozen.yaml` + `…smoke.frozen.yaml` written; both carry `kind: spacedock_solver`/`runtime: codex`/`trials: 1`; smoke frozen lists all 9 tasks.
- DONE: Run the gatekeeper subagent + write `## Gatekeeper review` block
  G1-G10 table appended; overall APPROVE (no FAILs; G9 N/A). Special attention: G8 = 3 perturbable ana-eng canaries present (ana-eng001/002/003) ✓; G2 = leak-guard byte-identical, no hidden tokens, no hashed-id literals ✓; G1 = one Implementation hunk only ✓; G10 = acceptance signal reads RAW SOURCE (separately-sourced anti-join), not self-anchored, judged PASS.
- DONE: STOP at the gate — no rk run launched
  No `rk run` invoked; only `rk freeze` (2x) + read-only `rk registry resolve`. Baseline rewards resolved for the smoke-set table (targets FAIL; all 7 canaries PASS; overall 31/48=0.6458).

### Summary

Authored the h0036 variant: a single additive Implementation rule (source-key COVERAGE preservation — never narrow a key to a type that drops non-conforming values; reconcile via a RAW-SOURCE coverage anti-join) plus a copyable BEFORE/AFTER skeleton, mirroring the LANDED h0019 shape. Ground truth confirmed from the @baseline run-dir: ana-eng007 fails `Got 5` = 5 MISSING md5-hashed source rows (one-directional coverage drop), and the @baseline solver's "row preservation 5/5" was a self-anchored false-green that never compared dim_products to the raw products source. Both specs frozen (full diff = 2 fields; smoke adds only the 9-task panel with 3 perturbable ana-eng canaries); gatekeeper recommends APPROVE with no FAILs. Stopped at the gate — no run launched.
