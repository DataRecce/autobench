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

## Smoke result

## Run result

## Behavioral analysis

## Verdict
