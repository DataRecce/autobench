---
id: h0038
title: Plan Review — a NEW pre-Implementation stage running the never-run Method B (independent re-derivation + a generic leak-clean grain invariant; REJECT only on a locally-visible code-contradicts-contract bug, else PROCEED_UNDETERMINED and build as baseline)
status: propose
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §3 E-PRMB (rank 2, captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 2. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-09T03:00:10Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

**Falsifiable claim (the single README change — a NEW `## Stage: Plan Review` inserted between
Exploration and Implementation):** making Round-1's *simulated-only* Method B runnable as a live,
self-imposed fresh-derivation pass — RE-DERIVE the intended grain/keys from local artifacts against a
generic leak-clean invariant, COMPARE that re-derivation to what the existing code does, and emit
`verdict:REJECT` **only** on a locally-visible code-contradicts-contract bug (else `PROCEED_UNDETERMINED`
and build EXACTLY as baseline) — will run as a true live experiment that abstains (`Got N` UNCHANGED)
on the 16 oracle-blocked failures while committing a standing `plan_review.json` reasoning probe, and
will NOT regress any passer. **No known failure is a clean code-contradicts-contract case, so the
honest expected flip count on the known 17 is {0}**; the live target is infrastructure / a
regression-prevention rail across all 48.

**The single solver-README change.** Add exactly one `## Stage: Plan Review` header between the
existing `## Stage: Exploration` and `## Stage: Implementation`. The stage mandates, before any SQL
edit: (1) from the task instruction + the *existing* model SQL + a stated generic grain invariant
("a model's grain entity comes from its canonical source relation, never from a pre-filtered child; a
completeness/repair output must keep every key the consumer relies on"), RE-DERIVE the intended
grain/keys independently, writing the derivation to `plan_review.json` via apply_patch (a committed
artifact, not chatter); (2) COMPARE that re-derivation against what the existing code actually does;
(3) emit `verdict:REJECT` **only** when the existing code provably contradicts the re-derivation in a
way visible from local relations (e.g. it grains on a child the downstream consumer does not restore,
dropping keys end-to-end), with `reason` + `contradicting_line`; (4) if the re-derivation cannot be
pinned from local artifacts (the oracle-only case), emit `verdict:PROCEED_UNDETERMINED` and build
EXACTLY as baseline — **NEVER** reverse-inference (Method A, provably false-rejects). This is Method B:
test code against an *independent re-derivation + external invariant*, not internal
question-reconstruction.

**Independent non-oracle signal.** In-/app only: the *existing* model SQL the solver starts with, the
task instruction, and local relation row/key counts, re-derived in a deliberately separate pass against
a generic leak-clean invariant. Genuinely independent of the solver's build intent **for the
code-contradicts-contract class**; NOT independent of the oracle for the grain-convention class — which
is exactly why the stage must `PROCEED_UNDETERMINED` there. No hidden `AUTO_*` / `solution__*` /
`check_option_*` / `tests/AUTO_*` is named or read.

**Leading indicator (distance, `Got N`).** On the 16 oracle-blocked failures `Got N` should be
**UNCHANGED** (the stage abstains there) — this is the honest expected result, not an inertness failure.
The decisive smoke read is the committed `plan_review.json` on asana004 / intercom001 recording
`PROCEED_UNDETERMINED` and naming the downstream `coalesce` spine-restore — proof the stage correctly
sees the contradiction is not locally decidable. Any `Got N` shrink would have to come from a
solver-introduced contradiction the stage caught (a regression-prevention win, not a known-failure flip).

**Kill-path / predicted failure mode.** On the 16 oracle-blocked failures the stage abstains and
`Got N` is unchanged → reads as inert-but-correct. It never hits a REJECT-and-fix on the known 17
because no failure is the locally-visible code-contradicts-contract class: asana004/005 grain is erased
downstream by `LEFT JOIN…coalesce` so the contradiction is invisible locally; intercom re-correlates
through `_fivetran_active`; width needs oracle-only DROPs. Method B already VERIFIED asana004 in the
Round-1 simulation = **no false-reject, but also no catch** (the discriminating fact — the intermediate
carries the full 16-project spine — lives only in `solution/` + hidden tests). If the stage emits a
REJECT-and-rewrite on a passer (a false-reject regression), or fails to commit `plan_review.json`, it
is REJECTED.

**Dead family it must avoid (proposal §6 map) + how it differs.** Resembles **D1 grain-construct** and
**D4 candidate-generation / arbitration**. It differs precisely: (a) it is NOT a candidate generator /
selector — ONE build path is reviewed once against an external invariant, never N self-scored
candidates (so it escapes the G9-exhausted arbitration family); (b) it is NOT reverse-inference
(Method A, provably false-rejects); (c) unlike h0017 it does NOT MANDATE building-to-a-contract — it
only REJECTs a locally-visible contradiction and otherwise abstains, so it cannot invert the join
direction the way h0017 did.

**Target datasets.** Infrastructure / method PLUS a regression-prevention rail across all 48 — **none
of the 17 known failures is a clean code-contradicts-contract case** (proposal §5 + the 2026-06-08
re-triage). So the live target is (a) catch the class IF the solver *itself* introduces such a
contradiction mid-build (a rail on all 48), and (b) deliver `plan_review.json` as a standing reasoning
probe. The honest expectation is therefore stated against infrastructure/all-48, not a named flippable
failure; for smoke, the abstention reads are taken on `ade-bench-asana004` and `ade-bench-intercom001`
(both must record `PROCEED_UNDETERMINED`, naming the downstream restore).

**Honest expectation.** **{0}** flips on the known 17 (the flip-target class is empty among them). Value:
the **first live run of Method B** plus a standing `plan_review.json` reasoning probe. This is a
`trials: 1`, judge-by-artifact entity; it faces its own propose + smoke gate, and the captain decides
whether it ever runs.

**Scope.** Workflow-stage / prompt lever only; benchmark FIXED; no expanded solver access; leak-guard
intact (the stage references only the task instruction, the existing model SQL, local relation
row/key counts, and a generic invariant — it names no hidden `AUTO_*` / `solution__*` / `check_*` /
verifier test, no `equality test` / `has less columns` / `expected output seed`, no `Got N` or row
count, and no `curl`/`wget`/`git clone`/web/published-solution fetch). The change touches exactly one
new `## Stage:` header and leaves the leak-guard prose + the four existing stages byte-identical. The
full spec differs from `@baseline` only in `experiment:` + `solver_workflow:`; the smoke spec
additionally adds `benchmark.tasks`. The stage is single-path (one build reviewed once, not a
generative candidate generator) — note this for the G8/G9 read at propose.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0038-plan-review-method-b.yaml` shows only
`experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md` adds exactly
one `## Stage: Plan Review` header between Exploration and Implementation, leaves the leak-guard prose
(lines ~1–32) and the four existing stages byte-identical, and names no hidden
`AUTO_*`/`solution__*`/`check_*`/verifier test. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (computed from
`per_trial_outcomes.json`, slug-paired, 10k bootstrap) plus the absolute `stratified_pass_at_1` vs
`@baseline` 0.6458.**
The smoke deep-dive MUST read the committed `plan_review.json` (the dispatched-ensign `apply_patch`
payload) and confirm: on `ade-bench-asana004` / `ade-bench-intercom001` it records
`PROCEED_UNDETERMINED` naming the downstream `coalesce` spine-restore (proof the contradiction is
correctly seen as not locally decidable); and on no passer does it emit a REJECT-and-rewrite
(false-reject regression). Unchanged `Got N` on the oracle-blocked failures is the SUCCESS condition
here, not inertness-failure. A REJECT-and-rewrite that regresses a passer, or a missing
`plan_review.json`, is INERT/false-rejecting → REJECTED.

## Gatekeeper review

**Recommendation: APPROVE** — single new stage, leak-guard byte-identical, spec scope clean,
generative-but-record-only with a full G8 family panel + 2 perturbable asana canaries; G10/G9
N/A because the stage selects nothing and acts on nothing (it records a verdict and builds
exactly as baseline). Only WARNs are G7 (REJECT-class flips are the inert grain-rewrite family
by design — the hypothesis honestly expects {0}) and a fidelity note.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-08). Reviewed 2026-06-09T03:10Z.
Fork parent resolved: `source:` = `solver_workflows/codex-ade-dbt-minimal`; `rk registry resolve run @baseline` = `runs/ade-bench-baseline/622bdedac572b479`, whose `solver_workflow` = `solver_workflows/codex-ade-dbt-minimal` — agree.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff codex-ade-dbt-minimal/README.md h0038/README.md` is a pure addition `49a50,127`; exactly one new `## Stage: Plan Review` between Exploration and Implementation; stage count 4→5; no `<` (delete/change) hunks. |
| G2 leak-guard intact | PASS | Lines 1–32 byte-identical to parent (`diff` of `sed -n '1,32p'` empty). grep over added block 50–127: no `AUTO_*`/`solution__*`/`check_option`/`tests/AUTO`/`verifier`/`equality test`/`expected output seed`; no `Got N`/row-count leak; no `curl`/`wget`/`git clone`/`git ls-remote`. |
| G3 spec two fields | PASS | `diff baseline.yaml h0038…yaml` = only `experiment:` (line 2) + `solver_workflow:` (line 11). `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0038…yaml h0038…smoke.yaml` = only an added `benchmark.tasks:` block (+ rationale comments). All 8 slugs `ade-bench-`-prefixed. Both hypothesis-named abstention targets present (`ade-bench-asana004`, `ade-bench-intercom001`). |
| G5 both frozen | PASS | `h0038-plan-review-method-b.frozen.yaml` (1691 B) + `…smoke.frozen.yaml` (1878 B) both exist; both carry `kind: spacedock_solver` + `runtime: codex`; smoke frozen lists all 8 tasks. |
| G6 resolver fidelity | PASS | Inserted text = Method B verbatim: states the generic invariant, RE-DERIVE→COMPARE→DECIDE, `verdict:"REJECT"` only on a locally-visible code-contradicts-contract bug (with `reason`+`contradicting_line`), else `verdict:"PROCEED_UNDETERMINED"` and build EXACTLY as baseline. Explicitly forbids reverse-inference (Method A) and forbids building-to-a-contract ("never invents a contract for the code to be built to"). Independent-signal, NOT self-anchored "re-run your own model / compare to the existing code" (it derives fresh from instruction+invariant, not from the code's own output). Matches the claim; no scope creep. |
| G7 actionability/inert-risk | WARN | The stage is **record-only**: on `PROCEED_UNDETERMINED` it builds byte-for-byte as baseline (no restructure mandate). Its only behavioral lever is the REJECT-class catch (grain off a pre-filtered child) — and the **1a grain-construct/reconcile family is EXHAUSTED 4-REJ** (taxonomy: h0010/h0016/h0017/h0030), so a REJECT-and-then-fix would be the known-inert structural-rewrite family. The hypothesis already states the honest expectation as **{0} flips on the known 17** and value = first live Method B + standing `plan_review.json` probe + regression rail. Inert-on-flips is the *predicted, accepted* outcome here, not a defect. WARN, does not block. |
| G8 regression-canary coverage | PASS | Generative (fires on every task). Smoke panel carries a non-target `@baseline` passer from **every family that has one**: airbnb001 / ana-eng001 / asana001 / f1007 / quickbooks002 (intercom has no `@baseline` passer → intercom001 doubles as its family read + abstention target). For the grain-construct family the invariant most likely perturbs (asana), **≥2 perturbable canaries**: asana001 + asana003 (both `@baseline` PASS). All canary rewards re-resolved from `@baseline` `per_trial_outcomes.json`. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol. Hypothesis + README state single-path: one build reviewed once against an external invariant; "it does **not** generate or score multiple candidate answers, and it selects nothing." No N-candidate substrate, no per-candidate scoring. |
| G10 self-correcting false-positive | N/A | Not a self-correcting / fix-on-disagreement lever. It records a verdict and acts on nothing: "you must **not** revert, rewrite, re-select, invert a join, or hold back any committed model merely to make it agree with this verdict… the build proceeds EXACTLY as it otherwise would." No reconcile-and-replace, no figure-fix path → the h0012 false-green mechanism cannot fire. (This is the load-bearing difference vs the dead self-correcting family.) |
| G11 multi-model-target risk | N/A | The two abstention targets are each scored by a **single** model (taxonomy: asana004 → `AUTO_int_asana__project_user_agg_equality`; intercom001 → `AUTO_intercom__threads_equality`). They are **abstention reads** (must record `PROCEED_UNDETERMINED`), not flip-credit targets, so the single-run-variance concern does not apply. The stage is not single-model-scoped anyway (it reviews whatever the task touches). |

**For the captain:** This is a clean APPROVE. Both substantive WARN-class facts are *features*, not defects: (1) the stage is designed to abstain on all 16 oracle-blocked failures (G7 — REJECT-class flips are the known-inert grain family; honest expectation is {0} flips), and (2) it acts on nothing it records (G10 N/A — no self-correcting false-green path). The decisive smoke read is the **committed `plan_review.json` content**, not the pass-rate: confirm asana004 + intercom001 record `verdict:PROCEED_UNDETERMINED` naming the downstream `coalesce` spine-restore / `_fivetran_active` re-correlation, and that **no passer is REJECT-and-rewritten** (any Got-N movement on the 6 canaries = false-reject = NO-GO). Note the durable routing is the h0041-VALIDATED `/tmp/plan_review.json` + `cat`-to-stdout (NOT the dead `/razorback-freeze` single-child precondition that made sibling h0039 INERT).

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: README change = EXACTLY ONE new `## Stage: Plan Review` inserted between Exploration and Implementation implementing Method B (re-derive grain/keys from instruction+existing SQL+stated invariant → compare → `verdict:REJECT` only on locally-visible code-contradicts-contract bug with `reason`+`contradicting_line`, else `verdict:PROCEED_UNDETERMINED` and build EXACTLY as baseline; never reverse-inference). Leak-guard prose (lines 1–32) + four existing stages byte-identical; AC-1 satisfied.
  `diff codex-ade-dbt-minimal/README.md h0038/README.md` = pure addition `49a50,127`; stage count 4→5; grep over added block: no `AUTO_*`/`solution__*`/`check_*`/verifier/`Got N`/row-count/curl/wget/git-clone.
- DONE: DURABLE ARTIFACT ROUTING — h0041-VALIDATED fix used verbatim: write `plan_review.json` UNCONDITIONALLY to `/tmp/plan_review.json` and `cat` it to stdout (durable in the worker session transcript). Did NOT route through `/razorback-freeze` single-child precondition (the dead path that made sibling h0039 INERT).
  README added block lines 116–127: "Write the JSON to the fixed scratch path `/tmp/plan_review.json` (always, with no precondition), and then print the file's contents to standard output… `apply_patch` … `cat /tmp/plan_review.json`."
- DONE: Smoke spec `benchmark.tasks` = 2 abstention reads (asana004 + intercom001, both must record PROCEED_UNDETERMINED naming the downstream coalesce/_fivetran_active restore) + false-reject regression panel (1 passer per family: airbnb001/ana-eng001/asana001/f1007/quickbooks002) + 2nd perturbable asana canary asana003 (G8 ≥2). Gatekeeper run, per-rule table + APPROVE recorded in `## Gatekeeper review`. G9 N/A (single-path); G8 applies (generative) and PASSES.
  `diff h0038…yaml h0038…smoke.yaml` = only added `benchmark.tasks` block (8 tasks) + rationale comments. Baseline rewards re-resolved from `622bdedac572b479/per_trial_outcomes.json`.

### Summary

Authored h0038 (first LIVE run of Method B) by forking the registry-confirmed `@baseline` solver `codex-ade-dbt-minimal` into `solver_workflows/h0038-plan-review-method-b/` and inserting exactly one new `## Stage: Plan Review` between Exploration and Implementation. The stage is generative-but-record-only: it re-derives the intended grain/keys independently against a stated generic leak-clean invariant, emits `REJECT` only on a locally-visible code-contradicts-contract bug, else `PROCEED_UNDETERMINED`, and builds EXACTLY as baseline — it selects nothing (G9 N/A) and acts on nothing it records (G10 N/A, so the h0012 false-green path cannot fire). Artifact routing uses the h0041-VALIDATED unconditional `/tmp/plan_review.json` + `cat`-to-stdout (avoiding the dead `/razorback-freeze` precondition that made sibling h0039 inert). Full spec differs from baseline only in `experiment:` + `solver_workflow:`; smoke adds only the 8-task `benchmark.tasks` panel; both specs frozen with `kind/runtime/trials` preserved. Gatekeeper recommendation = **APPROVE** (no FAILs; WARNs only on G7 inert-on-flips-by-design and a fidelity note — both expected: the hypothesis honestly predicts {0} flips, value = first live Method B + standing `plan_review.json` reasoning probe + regression rail across all 48).

### Smoke-set table (captain gate)

```
┌──────────────────┬──────────┬──────────────────────┬──────────────────────────────────────────────────────────┐
│       Task       │ Baseline │ Should pass in smoke?│                  Role / why we picked it                   │
├──────────────────┼──────────┼──────────────────────┼──────────────────────────────────────────────────────────┤
│ asana004         │ ❌ FAIL  │ ❌ stays FAIL        │ Abstention read — MUST record PROCEED_UNDETERMINED naming  │
│                  │          │                      │ the downstream LEFT JOIN..coalesce spine-restore.          │
│ intercom001      │ ❌ FAIL  │ ❌ stays FAIL        │ Abstention read — MUST record PROCEED_UNDETERMINED naming  │
│                  │          │                      │ the _fivetran_active re-correlation (intercom family read).│
│ asana001         │ ✅ PASS  │ ✅ must stay PASS    │ Perturbable asana canary #1 (grain-construct family the    │
│                  │          │                      │ invariant fires on) — no REJECT-and-rewrite.               │
│ asana003         │ ✅ PASS  │ ✅ must stay PASS    │ Perturbable asana canary #2 (G8 ≥2) — no REJECT-and-rewrite│
│ airbnb001        │ ✅ PASS  │ ✅ must stay PASS    │ Canary (airbnb family) — false-reject tripwire.            │
│ ana-eng001       │ ✅ PASS  │ ✅ must stay PASS    │ Canary (ana-eng family) — false-reject tripwire.           │
│ f1007            │ ✅ PASS  │ ✅ must stay PASS    │ Canary (f1 family) — false-reject tripwire.                │
│ quickbooks002    │ ✅ PASS  │ ✅ must stay PASS    │ Canary (quickbooks family) — false-reject tripwire.        │
└──────────────────┴──────────┴──────────────────────┴──────────────────────────────────────────────────────────┘
```

Net hoped-for: **{0} flips** (honest expectation — no known failure is a clean code-contradicts-contract case); the SUCCESS condition is the *committed `plan_review.json`* on asana004 + intercom001 recording `PROCEED_UNDETERMINED` (correct abstention) AND zero false-rejects on the 6 passers (Got N byte-unchanged on every canary). Unchanged Got N on the abstention reads is the win, not inertness-failure. ETA: 8 tasks × ~9 min/task ≈ **~72 min** (serial, `n_concurrent_trials=1`), detached via nohup.
