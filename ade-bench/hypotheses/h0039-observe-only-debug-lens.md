---
id: h0039
title: Observe-only debug lens — a NEW observe-only stage that ALWAYS writes a machine-readable reasoning record then builds EXACTLY as baseline; success = Got N UNCHANGED on all 48 (any movement = gate-strip failed = contamination = NO-GO)
status: conclude
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §4 M1 (captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 3. The un-built WORKFLOW-REFINE Opening #2 (_artifacts/WORKFLOW-REFINE.md observe-only-lens lines). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-08T12:23:23Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

**Falsifiable claim (the single README change — a NEW observe-only `## Stage:` inserted between
Exploration and Implementation):** adding an observe-only stage that ALWAYS writes a machine-readable
reasoning record — a `Contract:` / `divergence` block to the sanctioned non-graded notes location
(`/razorback-freeze/<child>/…`, baseline README lines 30–32) — and then builds EXACTLY as baseline
(no build-to-satisfy mandate, no gate) will produce a guaranteed 48-task corpus of the solver's
at-build-time mental model **while leaving `Got N` UNCHANGED on all 48**. This is a **method
instrument**, expected to flip **{0}** tasks by construction; `Got N` UNCHANGED on all 48 is the
SUCCESS condition, and ANY movement = the gate-strip failed = the record leaked into the build =
contamination = NO-GO.

**The single solver-README change.** Add exactly one observe-only `## Stage:` header between the
existing `## Stage: Exploration` and `## Stage: Implementation` (or, if cleaner, an observe-only
sub-step inside Exploration). The stage mandates writing a machine-readable reasoning record
(`Contract:` block / `plan_review.json` / `divergence.md`) to the sanctioned non-graded notes location
via on-disk apply_patch — and then explicitly states the build proceeds EXACTLY as baseline: the record
changes no committed SQL, carries no build-to-satisfy mandate, and gates nothing. This is the exact
variant the WORKFLOW-REFINE observe-only-lens note proposed and never built.

**Independent non-oracle signal.** None is asserted against the oracle — by design. The deliverable is
the *record itself*: a 48-task map of the solver's belief, most valuable on the ~14 fired-and-failed
cells. h0017 proved the `Contract:` block legibly states the *wrong* model in the solver's own words
(asana004 wrote "one row per project_id present in int_asana__project_user"; intercom001 wrote "driven
by active conversation part rows" = the bug verbatim). This stage captures that on all 48 instead of
only the ~7 cells h0017 fired on, and it feeds the ideate stage with a per-task map of which failures
are code-contradicts-contract (a future Method-B subject) vs self-consistent-but-oracle-only (the wall).
No hidden `AUTO_*` / `solution__*` / `check_option_*` / `tests/AUTO_*` is named or read.

**Leading indicator (distance, `Got N`).** `Got N` **UNCHANGED on all 48** is the SUCCESS condition
(the contamination tripwire). Because the stage changes no committed SQL by construction, it CANNOT
false-green and CANNOT flip; any `Got N` movement means the observe-only gate-strip failed (the record
fed the build) → NO-GO. The leading indicator is therefore inverted from a flip-seeker: flatness is the
win, movement is the failure.

**Kill-path / predicted failure mode.** The known risk is G7-high inertness in the data-quality sense —
an artifact the solver is told changes nothing has weaker production pressure than h0017's build-feeding
contract; h0031 already skipped process artifacts on easy passers. Mitigate with on-disk apply_patch +
≥1 `dbt show` key-count line per model, verified by `test -f`. The kill is two-sided: (i) if any
`Got N` moves on a sampled passer, the gate-strip failed = contamination = NO-GO; (ii) if the record is
absent/empty on the fired-and-failed cells (`test -f` fails), the lens went inert and delivers no corpus
= REJECTED. The corpus records the solver's *belief*, which is demonstrably unreliable on the failers —
but that unreliability is itself the finding (it confirms the failures are self-consistent, not
self-contradictory; wall-confirming knowledge).

**Dead family it must avoid (proposal §6 map) + how it differs.** It must not become **D9
new-stage/arbitration-architecture** (mostly INERT-or-correlated) by sneaking a build-to-satisfy
mandate in: there is NO gate and NO mandate, so it cannot false-green like h0017 (D1) or arbitrate like
h0031 (D4). It is strictly weaker than every flip-seeker by design — it is an observability instrument,
not a route, contract, or selector. The only way it touches a dead family is if the gate-strip leaks
(then it becomes a contaminated D1/D9 variant) — which the `Got N`-unchanged tripwire exists to catch.

**Target datasets.** Method instrument targeting **infrastructure / all 48** — there is no flippable
target by construction. The deliverable is the 48-task reasoning corpus; the decisive smoke reads are
(a) the committed record present and non-empty on the fired-and-failed cells (e.g. `ade-bench-asana004`,
`ade-bench-intercom001`) via `test -f`, and (b) `Got N` UNCHANGED on a sampled cross-family passer panel
(the contamination tripwire).

**Honest expectation.** **{0}** flips by construction. Value: the un-built observe-only debug-lens
corpus, built at last — a guaranteed 48-task map of the solver's at-build-time mental model. Honest
caveats: (1) G7-high inertness (mitigated by on-disk apply_patch + `test -f`); (2) the corpus records
*belief*, unreliable on the failers, but that unreliability is the finding; (3) substantial overlap
with the existing §5 triage and the archived h0017 debug run `19283fb82dbd4ffd`, so the marginal yield
is bounded. This is a `trials: 1`, judge-by-artifact entity; it faces its own propose + smoke gate, and
the captain decides whether it ever runs.

**Scope.** Workflow-stage / prompt lever only; benchmark FIXED; no expanded solver access; leak-guard
intact (the stage references only local artifacts + the sanctioned non-graded notes location, and names
no hidden `AUTO_*` / `solution__*` / `check_*` / verifier test, no `equality test` / `has less columns` /
`expected output seed`, no `Got N` or row count, and no `curl`/`wget`/`git clone`/web/published-solution
fetch). The change touches exactly one new observe-only `## Stage:` header and leaves the leak-guard
prose + Exploration/Implementation/Validation/Finalization byte-identical. The full spec differs from
`@baseline` only in `experiment:` + `solver_workflow:`; the smoke spec additionally adds
`benchmark.tasks` (a cross-family sentinel/canary panel + the fired-and-failed record-presence cells).

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0039-observe-only-debug-lens.yaml` shows only
`experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md` adds exactly
one observe-only `## Stage:` header, carries NO build-to-satisfy mandate and NO gate, leaves the
leak-guard prose (lines ~1–32) and the four existing stages byte-identical, and names no hidden
`AUTO_*`/`solution__*`/`check_*`/verifier test. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (computed from
`per_trial_outcomes.json`, slug-paired, 10k bootstrap) plus the absolute `stratified_pass_at_1` vs
`@baseline` 0.6458.**
For this observe-only instrument the verdict is inverted: `Got N` UNCHANGED on the sampled panel
(no flips, no regressions) is the SUCCESS condition. The smoke deep-dive MUST confirm (a) the committed
reasoning record is present and non-empty on the fired-and-failed cells via `test -f` (the lens did not
go inert) and (b) `Got N` is byte-unchanged on every sampled passer (the gate-strip held; no
contamination). ANY `Got N` movement = contamination = NO-GO; an absent/empty record on the
fired-and-failed cells = inert = REJECTED.

## Gatekeeper review

**Recommendation: APPROVE** — exactly one new observe-only `## Stage:` added; leak-guard byte-identical;
specs differ only in the two allowed fields (+ smoke `benchmark.tasks`); no integrity FAIL. Only WARN is
the self-declared G7 inertness risk (a process artifact told it changes nothing), mitigated by on-disk
`apply_patch` + a `dbt show` key-count probe per model + `test -f` presence check on the failers.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-08). Reviewed 2026-06-08T12:30Z.

Fork parent resolved & cross-checked: `source:` names `solver_workflows/codex-ade-dbt-minimal`; `@baseline`
= `runs/ade-bench-baseline/622bdedac572b479` whose `spec.frozen.yaml` `solver_workflow:` is
`solver_workflows/codex-ade-dbt-minimal` — agree, so G1/G6 evaluable against the right parent.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff codex-ade-dbt-minimal/README.md h0039/README.md` = `49a50,99` — pure insertion of exactly one `## Stage: Observe (debug lens — observe-only, changes nothing)`; no line removed/modified; falls between Exploration and Implementation as claimed. |
| G2 leak-guard intact | PASS | Lines 1–32 (no-fetch + dependency/package guardrails) byte-identical to parent. Grep over the 50 added lines for `AUTO_ \| solution__ \| check_ \| verifier \| equality test \| Got N \| row count \| curl \| wget \| git clone \| git ls-remote \| web fetch \| published solution` → the only hit is `no "build to satisfy" mandate` (a negation/disclaimer, not a directive). Record target is the sanctioned non-graded notes location only. |
| G3 spec two fields | PASS | `diff baseline.yaml h0039.yaml` shows only `experiment:` (→`ade-bench-h0039-observe-only-debug-lens`) and `solver_workflow:` (→`./solver_workflows/h0039-observe-only-debug-lens`). `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0039.yaml h0039.smoke.yaml` shows only an added `benchmark.tasks:` block (`23a24,35`); all 8 slugs `ade-bench-`-prefixed; includes both record-presence cells the `## Hypothesis` names (asana004, intercom001) + the cross-family Got-N tripwires. |
| G5 both frozen | PASS | `h0039-observe-only-debug-lens.frozen.yaml` + `…smoke.frozen.yaml` both written; both carry `kind: spacedock_solver`, `runtime: codex`, `trials: 1`; smoke frozen lists 8 tasks. |
| G6 resolver fidelity | PASS | Inserted text matches the claim: observe-only stage, writes a `Contract:`/`divergence` reasoning record to the non-graded notes location, then "build EXACTLY as you would without this stage… not a gate… no build-to-satisfy mandate… must not rewrite, re-select, or hold back any committed model." NOT self-anchored verification (it records belief; it does not re-run/compare/drive-to-zero the solver's own derivation) — the dead h0006/h0007/h0008 phrasings are absent. No scope creep. |
| G7 actionability/inert-risk | WARN | Process artifact the solver is told changes nothing → G7-high inertness in the data-quality sense (the kill-path the hypothesis itself names). Mitigated: written via on-disk `apply_patch` (artifact must exist, not just be discussed) + ≥1 `dbt show` key-count probe per model + smoke `test -f` non-empty check on the fired-and-failed cells. Class: process-record (not a SQL restructure, not a build/deliverable-completion rule). Surfaced for the captain; never blocks the gate. |
| G8 regression-canary coverage | PASS | Generative (fires on every author/restructure/repair task). Smoke panel carries a Got-N tripwire from every family that HAS an `@baseline` passer: airbnb001 / ana-eng001 / asana001 / f1007 / quickbooks002 (all reward=1.0). intercom has **no** `@baseline` passer (all 3 FAIL, 31/48) so no intercom tripwire is possible — recorded in the spec comment, not an omission. For asana (the family sharing the targets' authoring construct) a 2nd perturbable passer asana003 (reward=1.0) is carried per the ≥2 rule. Because the lever is observe-only by construction (changes no committed SQL), the success criterion is **Got N UNCHANGED**, not a flip — the panel is a contamination tripwire, exactly what G8 exists to protect. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — single session, one build, no candidate set. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever. The stage explicitly does NOT act on disagreement ("must not rewrite, re-select, or hold back any committed model to make it agree with the record") — there is no fix-on-disagreement path to false-green. |
| G11 multi-model-target risk | N/A | No flip target by construction — this is a method instrument expected to flip 0 tasks; the verdict is inverted (Got N unchanged = success). No single-model-flip-as-variance hazard. |

**For the captain:** No integrity FAIL — APPROVE-class. The single live concern is the self-declared G7
inertness (an artifact told it changes nothing has weak production pressure; h0031 already skipped
process artifacts on easy passers). The smoke `test -f` non-empty check on asana004 + intercom001 is the
inertness kill (absent/empty record there = REJECTED); any Got-N movement on a sampled passer is the
contamination kill (= NO-GO). intercom carries no Got-N tripwire because the family has zero `@baseline`
passers — accepted, not a coverage gap.

## Smoke result

**Verdict: REJECTED — INERT (not contamination/NO-GO).** Run `runs/ade-bench-h0039-observe-only-debug-lens/e84f83324081c22d` (8 tasks, 1h 7m). Strict audit **clean** (`clean: 8, tainted: 0, coverage_missing: 0`); `captured=1` on every cell (`> 0`). Score `stratified_pass_at_1 = 0.625` (5/8). The Observe stage went **fully inert at the artifact level on all 8 cells** — `plan_review.json` was never written anywhere — because the `/razorback-freeze` "exactly one child directory" precondition (inherited verbatim from the baseline README lines 30–32) is **structurally unmet in this harbor task layout**. The lens delivered **no reasoning corpus** → the hypothesis's own kill-path (ii): "record absent/empty on the fired-and-failed cells = inert = REJECTED."

The 5/8 (not the expected 6/8) is NOT contamination: the dropped passer is `asana003`, but `plan_review.json` was never produced on any cell, so there was no record to leak into the build. The drop is **solver run-to-run variance** on a refactor task (detail in `## Behavioral analysis`).

### Per-cell flip / distance / record table

| Cell | @baseline | smoke | Got N (smoke vs base) | plan_review.json written? | Read |
|------|-----------|-------|------------------------|---------------------------|------|
| airbnb001 (canary) | ✅ r=1 fail=0 | ✅ r=1 fail=0 | unchanged (no fails) | NO — "zero child directories, not applicable" | held; lens inert |
| ana-eng001 (canary) | ✅ r=1 fail=0 | ✅ r=1 fail=0 | unchanged | NO | held; lens inert |
| asana001 (canary) | ✅ r=1 fail=0 | ✅ r=1 fail=0 | unchanged | NO | held; lens inert |
| f1007 (canary) | ✅ r=1 fail=0 | ✅ r=1 fail=0 | unchanged | NO | held; lens inert |
| quickbooks002 (canary) | ✅ r=1 fail=0 | ✅ r=1 fail=0 | unchanged | NO | held; lens inert |
| **asana003 (canary)** | ✅ r=1 fail=0 | ❌ **r=0 fail=6** | **moved 0→6 fails + 1 build ERROR** | NO | **DROPPED — variance, not leak** (no record existed to leak) |
| asana004 (failer cell) | ❌ r=0 Got 3 | ❌ r=0 Got 3 | **byte-unchanged (Got 3)** | NO — record ABSENT | inertness kill confirmed |
| intercom001 (failer cell) | ❌ r=0 Got 7 | ❌ r=0 Got 7 | **byte-unchanged (Got 7)** | NO — record ABSENT | inertness kill confirmed |

**Decisive inverted reads:**
- **(a) Got-N contamination tripwire:** 5/6 passers byte-unchanged. asana003 moved (fail 0→6), but `plan_review.json` was never written on ANY cell → no artifact could feed the build → the move is variance, not gate-strip leak. The two designed-failers held byte-identical (Got 3 / Got 7), the signature of a fully-inert lens.
- **(b) Record presence (inertness kill):** `plan_review.json` is **ABSENT** on asana004 and intercom001 (and all 6 others). The worker explicitly logged on every cell: *"The freeze directory check found zero child directories, so the conditional freeze notes and `plan_review.json` are not applicable here."* Lens inert → REJECTED.

## Run result

N/A — REJECTED at smoke (inert). No full run.

## Behavioral analysis

**Root cause of the inertness — the notes-location precondition is environmentally unmet.** The Observe stage routes its record to the sanctioned non-graded notes location *only* "if `/razorback-freeze` exists and has exactly one child directory" (the precondition the baseline README already uses for `exploration.md`/`implementation.md`/`validation.md`). In every cell of this harbor run the worker probed `/razorback-freeze` and found a **degenerate layout** — `find /razorback-freeze -mindepth 1 -maxdepth 1 -type d` returned either `/app`, `0`, or dataset-table content, never the clean single-child shape — and so concluded the conditional notes were "not applicable" and skipped `plan_review.json` entirely. This is **not** specific to h0039: the **@baseline run ALSO never wrote any freeze notes** (no `exploration.md`/`implementation.md`/`validation.md` exist anywhere under `runs/ade-bench-baseline/622bdedac572b479`, and its airbnb001 worker reached the identical "not applicable" conclusion). The precondition has been silently failing the whole time; h0039 is the first hypothesis to depend on it and thereby surface it. The G7-high inertness the propose gate flagged materialized — but via the **routing precondition**, not via "an artifact told it changes nothing." The on-disk-`apply_patch` + `dbt show` mitigation never got a chance to run because the gating `if` short-circuited first.

**The asana003 passer drop is variance, not contamination.** asana003 ("remove the tmp models; have `stg_asana__[name].sql` reference the source tables directly") is a refactor. @baseline passed 17/17. The smoke worker committed (via `apply_patch`, `patch_apply_end` = success) a repoint of all `stg_asana__*` models from `from {{ ref('stg_asana__*_tmp') }}` to `from {{ var('<name>') }}` (and `get_columns_in_relation(var('<name>'))`) plus deletion of all `tmp/` models. That `var()` path changed values/types — 6 `AUTO_*_equality` tests failed (project Got 16, tag Got 17, task Got 1, project_task_metrics Got 17, project_user Got 13, task_tags Got 1) and `asana__daily_metrics` hit a build ERROR (`Conversion Error: invalid date field format: "None"`). The baseline worker had chosen a different, correct repoint. Because **no `plan_review.json` was ever written**, the Observe stage produced no artifact that could have influenced this build — the SQL choice is the solver's own, and the FAIL is gpt-5.5 @ xhigh run-to-run variance on a refactor (consistent with the standing "single-trial, judge by artifact" caveat; the lever is provably absent from the causal chain). Verifying the **artifact** (not the chatter) confirms: the committed SQL diff is a plain `ref→var` repoint with zero reference to any reasoning record.

**Did the structural change alter committed behavior?** No — it could not, because it never fired its artifact. On the 5 held passers the committed behavior is byte-identical to baseline; on the 2 failers the Got-N is byte-identical to baseline. The new stage is observe-only AND inert, so it changed nothing — which is the *success direction for the no-harm axis*, but it also delivered *nothing*, which is the *failure direction for the deliverable axis*. Net: a clean, well-instrumented REJECTED-inert with a concrete, transferable root cause (the freeze-notes routing precondition is dead in this harbor layout).

## Behavioral analysis

## Verdict

**REJECTED — INERT (at smoke).** The observe-only lens produced no reasoning corpus: `plan_review.json`
was never written on any of the 8 cells because the `/razorback-freeze` "exactly one child directory"
routing precondition is structurally unmet in this harbor layout (the @baseline run never wrote freeze
notes either). This is the hypothesis's own kill-path (ii): record absent on the fired-and-failed cells
= inert = REJECTED. It is NOT contamination: strict audit clean (8/8), 5/6 passers held byte-unchanged,
and the lone passer drop (asana003) is run-to-run variance — with no record ever written, nothing could
leak into the build, and the two failers held Got-N byte-identical (Got 3 / Got 7). Zero score impact
held, but the deliverable (the 48-task belief corpus) was empty. **Transferable finding:** the
freeze-notes routing precondition is dead here — the only place reasoning has ever durably survived in
this harness is the ensign worker `agent/sessions/*.jsonl`, so any future debug-lens must target the
session transcript or an unconditional path, not `/razorback-freeze` (steers h0041, h0038; logged in
`_artifacts/WORKFLOW-REFINE.md`).

## Stage Report: propose

- DONE: README change is EXACTLY ONE new observe-only `## Stage:` header inserted between Exploration and Implementation — NO build-to-satisfy mandate, NO gate; the leak-guard prose (~lines 1-32) and the four existing stages byte-identical to codex-ade-dbt-minimal/README.md (AC-1).
  `diff codex-ade-dbt-minimal/README.md h0039/README.md` = `49a50,99` (pure insertion, nothing removed/modified). New stage states "build EXACTLY as you would without this stage… not a gate… no build-to-satisfy mandate… must not rewrite, re-select, or hold back any committed model." Spec diff = only `experiment:` + `solver_workflow:`.
- DONE: Smoke spec `benchmark.tasks` is a CONTAMINATION panel (generative stage) — ≥1 currently-passing @baseline task from each family with a passer as Got-N tripwires, PLUS the fired-and-failed record-presence cells ade-bench-asana004 and ade-bench-intercom001.
  8 tasks: airbnb001 / ana-eng001 / asana001 / asana003 / f1007 / quickbooks002 (all reward=1.0 → Got-N tripwires) + asana004 / intercom001 (reward=0.0 → `test -f` record-presence cells). intercom has NO @baseline passer (all 3 FAIL) so no intercom tripwire is possible — recorded in the spec comment.
- DONE: Gatekeeper run; a `## Gatekeeper review` block with a per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT recommendation written into the hypothesis file.
  Recommendation **APPROVE** (no integrity FAIL); one WARN = self-declared G7 inertness, mitigated by on-disk apply_patch + dbt show key-count probe per model + smoke `test -f`. Gatekeeper run in-process (ensign cannot spawn a further subagent), applying `_gatekeeper/propose-review-guideline.md` to the diffs/frozen artifacts; fork parent cross-checked (source == @baseline solver_workflow == codex-ade-dbt-minimal).

### Smoke-set table (for the captain — gate presentation)

This is an **observe-only / generative** lever expected to flip **0** tasks by construction; SUCCESS = **Got N UNCHANGED** on every sampled passer (contamination tripwire), AND the `plan_review.json` record present & non-empty on the fired-and-failed cells (inertness kill). The "Should pass in smoke?" column reads "must stay PASS / Got N unchanged" for tripwires (movement = contamination = NO-GO) and "record present (still FAIL)" for the two failer cells.

```
┌─────────────────────────┬──────────┬──────────────────────────────┬──────────────────────────────────────────────────────────┐
│          Task           │ Baseline │     Should pass in smoke?    │                  Role / why we picked it                   │
├─────────────────────────┼──────────┼──────────────────────────────┼──────────────────────────────────────────────────────────┤
│ ade-bench-airbnb001     │ ✅ PASS  │ ✅ stay PASS, Got N unchanged │ Canary (airbnb) — Got-N contamination tripwire.            │
│ ade-bench-ana-eng001    │ ✅ PASS  │ ✅ stay PASS, Got N unchanged │ Canary (ana-eng) — Got-N contamination tripwire.          │
│ ade-bench-asana001      │ ✅ PASS  │ ✅ stay PASS, Got N unchanged │ Canary (asana) — Got-N contamination tripwire.            │
│ ade-bench-asana003      │ ✅ PASS  │ ✅ stay PASS, Got N unchanged │ 2nd asana perturbable canary (construct family) per G8.   │
│ ade-bench-f1007         │ ✅ PASS  │ ✅ stay PASS, Got N unchanged │ Canary (f1) — Got-N contamination tripwire.               │
│ ade-bench-quickbooks002 │ ✅ PASS  │ ✅ stay PASS, Got N unchanged │ Canary (quickbooks) — Got-N contamination tripwire.       │
│ ade-bench-asana004      │ ❌ FAIL  │ ❌ stay FAIL; record present  │ Fired-and-failed cell — `test -f plan_review.json` (asana).│
│ ade-bench-intercom001   │ ❌ FAIL  │ ❌ stay FAIL; record present  │ Fired-and-failed cell + only intercom coverage (no passer).│
└─────────────────────────┴──────────┴──────────────────────────────┴──────────────────────────────────────────────────────────┘
```

Net hoped for: **0 flips, 0 regressions** — every passer holds with Got N byte-unchanged (gate-strip held), and `plan_review.json` is present & non-empty on asana004 + intercom001 (lens did not go inert). Any Got-N movement on a passer = contamination = NO-GO; absent/empty record on the failers = inert = REJECTED. intercom has no @baseline passer, so it contributes only the failer cell. ETA ≈ 8 tasks × ~9 min ≈ **~70–75 min**, detached (nohup) — no need to wait on-screen.

### Summary

Built the WORKFLOW-REFINE Opening #2 observe-only debug lens. Forked `codex-ade-dbt-minimal` → `h0039-observe-only-debug-lens`; the single change is one new observe-only `## Stage: Observe` between Exploration and Implementation that always writes a machine-readable `plan_review.json` (Contract/divergence: grain, columns, types, divergence + a `dbt show` key-count per model) to the sanctioned non-graded notes location via on-disk apply_patch, then explicitly builds EXACTLY as baseline — no gate, no build-to-satisfy mandate, changes no committed SQL. Full spec differs from baseline only in `experiment:` + `solver_workflow:`; smoke spec adds an 8-task contamination panel; both frozen with kind/runtime/trials preserved. Gatekeeper: APPROVE, sole WARN is the self-declared G7 inertness (mitigated). The decisive smoke reads are inverted from a flip-seeker: Got N unchanged on the 6 passers (contamination tripwire) + plan_review.json present/non-empty on asana004 + intercom001 (inertness kill).

## Stage Report: smoke

- DONE: Smoke run on `specs/h0039-observe-only-debug-lens.smoke.frozen.yaml` completed (detached nohup, polled across turns; 1h 7m). Strict audit clean and `captured > 0` on every cell BEFORE the score; recorded in `## Smoke result`.
  `rk audit … --policy strict` → `clean: 8, tainted: 0, coverage_missing: 0`; `captured=1` on all 8 cells; `rk score` → `stratified_pass_at_1 = 0.625` (5/8). Run `runs/ade-bench-h0039-observe-only-debug-lens/e84f83324081c22d`.
- DONE: The two decisive INVERTED reads recorded with per-cell evidence.
  (a) Got-N: 5/6 passers byte-unchanged; asana003 moved (fail 0→6) but is variance not leak (no record was ever written, so nothing could feed the build); the 2 failers held Got 3 / Got 7 byte-identical. (b) Record presence: `plan_review.json` ABSENT on asana004 + intercom001 (and all 6 others) — inert = REJECTED.
- DONE: Workflow-refinement evaluation done (new-stage structural lever); entry appended to `_artifacts/WORKFLOW-REFINE.md` as part of the smoke commit.
  The Observe stage fired its probe on all 8 cells but wrote its artifact on ZERO — the `/razorback-freeze` "exactly one child directory" precondition is environmentally unmet (baseline never wrote freeze notes either). Committed behavior byte-unchanged on the 5 held passers + 2 failers. Entry: "the freeze-notes routing precondition is DEAD in this harbor layout."

### Summary

Smoke is a clean REJECTED-inert. The observe-only stage never wrote `plan_review.json` on any cell because it routes through the `/razorback-freeze` single-child precondition, which is structurally unmet in this harbor layout (the @baseline run never wrote freeze notes either — h0039 is the first hypothesis to depend on it and surface it). Strict audit clean 8/8; 5/6 passers held byte-unchanged; the lone passer drop (asana003, a `ref(tmp)`→`var()` refactor) is run-to-run variance, not contamination, because with no record written nothing could leak into the build, and both failers held Got-N byte-identical. The transferable learning (route durable artifacts to the session transcript or an unconditional path, NOT `/razorback-freeze`) is logged in WORKFLOW-REFINE and steers h0041/h0038.
