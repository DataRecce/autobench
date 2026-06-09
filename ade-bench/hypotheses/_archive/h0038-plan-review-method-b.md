---
id: h0038
title: Plan Review — a NEW pre-Implementation stage running the never-run Method B (independent re-derivation + a generic leak-clean grain invariant; REJECT only on a locally-visible code-contradicts-contract bug, else PROCEED_UNDETERMINED and build as baseline)
status: conclude
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §3 E-PRMB (rank 2, captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 2. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-09T03:00:10Z
completed: 2026-06-09T06:34:35Z
verdict: REJECTED
score:
worktree: 
archived: 2026-06-09T06:34:35Z
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

**Go/no-go: NO-GO (cleanly falsified → conclude/REJECTED).** Method B FALSE-REJECTED the very
abstention cell it was designed to abstain on (`asana004` → `verdict:REJECT`, not the predicted
`PROCEED_UNDETERMINED`), confirming the oracle-problem wall: the stage cannot distinguish a
locally-decidable contradiction from an oracle-only grain convention, so its REJECTs are guesses.
The reasoning probe runs and routes durably, but it does not discriminate.

**Run:** `runs/ade-bench-h0038-plan-review-method-b/ee924fbc9d3b0b20` (smoke, 8 cells, ~1h15m).
**Audit (strict):** `clean: 8, tainted: 0, coverage_missing: 0` — fully clean. **Score:**
`stratified_pass_at_1 = 0.75` (6/8), `stratified_n_completed = 8`, `n_errored = 0`,
verdict `above` the 0.1875 paper constant. **Captured:** all 8 cells have substantive
transcripts (`codex.txt` 60–83 KB, `sessions/*.jsonl` 268–664 KB) → `captured > 0` on every cell.

**`plan_review.json` recovered on 7/8** (routing fix HELD where it fired — durable in the session
transcript via the h0041 `/tmp/plan_review.json` + `cat`-to-stdout pattern; recovered from the
`apply_patch`/`printf` `arguments` + `cat` stdout in `agent/sessions/*.jsonl` / `agent/codex.txt`).
**ana-eng001 emitted NO concrete record** — only the README template (`<the re-derived…>`,
`<REJECT | PROCEED_UNDETERMINED>`) appears; 0 concrete `intended_grain` lines vs 3–4 on every
other cell. This is the h0041-flagged schema/execution-drift mode (gpt-5.5 sometimes skips the
free-form emit). Verdict distribution among the 7 that emitted: **4 PROCEED_UNDETERMINED /
3 REJECT** (+1 missing record on ana-eng001).

| Cell | @base | h0038 | Got N (base→h0038) | plan_review verdict | Read |
|------|-------|-------|--------------------|---------------------|------|
| asana004 (abstention target) | ❌ FAIL | ❌ FAIL | **3 → 6** | **REJECT** (`from project_user`) | ❌ **FALSE-REJECT** — predicted PROCEED_UNDETERMINED; the grain is oracle-only (taxonomy Track Z) yet the stage emitted a REJECT it could not locally ground; build got *worse* (3→6, variance). |
| intercom001 (abstention target) | ❌ FAIL | ❌ FAIL | 7 → 7 (unchanged) | PROCEED_UNDETERMINED | ⚠️ correct verdict, **wrong reason** — abstained because "no existing intercom__threads SQL" (a creation task), NOT the predicted `_fivetran_active` re-correlation. Abstains by accident of empty-SQL, not by seeing the contradiction. |
| asana001 (perturbable canary) | ✅ PASS | ✅ PASS | unchanged (PASS=2/2, ERROR=0) | **REJECT** | ⚠️ REJECT on a PASSER — but record-only held: committed SQL unchanged, passed cleanly. Inert reasoning, no damage. |
| asana003 (perturbable canary) | ✅ PASS | ✅ PASS | unchanged | PROCEED_UNDETERMINED | ✅ held PASS, abstained. |
| f1007 (canary) | ✅ PASS | ✅ PASS | unchanged (PASS=6/6, ERROR=0) | **REJECT** | ⚠️ REJECT on a PASSER — record-only held: committed SQL unchanged, passed cleanly. Inert reasoning, no damage. |
| airbnb001 (canary) | ✅ PASS | ✅ PASS | unchanged | PROCEED_UNDETERMINED | ✅ held PASS, abstained. |
| ana-eng001 (canary) | ✅ PASS | ✅ PASS | unchanged | **(no concrete record)** | ⚠️ held PASS, but the stage emitted no recoverable plan_review.json — record-emit skipped (schema drift). |
| quickbooks002 (canary) | ✅ PASS | ✅ PASS | unchanged | PROCEED_UNDETERMINED | ✅ held PASS, abstained. |

**Per-checklist:**
- (a) ABSTENTION (decisive): **FAILED.** asana004 emitted **REJECT**, not the required
  `PROCEED_UNDETERMINED`. intercom001 emitted `PROCEED_UNDETERMINED` but for the wrong (empty-SQL
  creation-task) reason, not the `_fivetran_active` re-correlation. The stage does not see why
  the contradiction is non-locally-decidable; it abstained on intercom001 only because there was
  no SQL to review at all.
- (b) NO FALSE-REJECT on passers: **PASS on rewards, but the verdict probe REJECTed 2 of 6
  passers** (asana001, f1007). Those held PASS — the "record-only / build EXACTLY as baseline"
  rule HELD (committed SQL byte-equivalent, ERROR=0, Got N unchanged). So no passer reward
  regressed (G8 panel clean), but the verdict layer itself emitted false-positives it simply
  could not act on. The single REAL build delta is asana004 (a non-passer): Got 3→6, variance on
  a CREATE task neither version can ground locally.
- (c) `plan_review.json` present & non-empty on all 8: **7/8** — the routing fix held where the
  stage fired (durable, recoverable from the transcript), but **ana-eng001 emitted no concrete
  record** (template-only; the h0041 schema/execution-drift mode). So the record-emit is not
  reliably universal under gpt-5.5 — a second confirmation of the h0041 free-form-drift finding.

## Run result

## Behavioral analysis

**The first LIVE Method B run characterizes the stage as a non-discriminating reasoning probe.**
The infrastructure worked end-to-end: the stage fired on all 8 cells, emitted a substantive
`plan_review.json` on every one, and the `/tmp` + stdout routing recovered cleanly (the
h0041 fix held a second time — confirming it as the reusable observe-only write-path). But the
*content* falsifies the value claim.

**1. The REJECT verdict is a guess, not a locally-grounded contradiction (the oracle wall).**
The hypothesis predicted {0} flips and *abstention* on the oracle-blocked failures. Instead the
stage REJECTed 3 of the 7 cells that emitted a record (asana004, asana001, f1007) — including
asana004, the exact cell the dispatch said MUST abstain.
asana004's REJECT cited `contradicting_line: from project_user` with `reason` "derives project_id
from a child relation." That is the **right-sounding grain story**, but it is *not locally
decidable*: whether the canonical grain is `project` or `project_user` is fixed by the hidden
expected output (taxonomy Track Z, "oracle-only `int_` convention"). The stage pattern-matched
the invariant's "never grain from a pre-filtered child" template onto a FROM clause and fired —
exactly the false-reject the hypothesis's own kill-path warned about, and exactly the
solver-blind-to-oracle / correlated-error wall. Method A (reverse-inference) provably
false-rejects; this run shows Method B *also* false-rejects when the invariant is applied as a
pattern rather than a locally-verified anti-join. The Got 3→6 worsening on asana004 is build
variance (a CREATE task neither version can ground), not a benefit of the REJECT.

**2. The "abstain" that did fire was an accident of empty SQL, not contradiction-blindness.**
intercom001 correctly emitted `PROCEED_UNDETERMINED`, but its `reason` is "no existing
intercom__threads SQL is present" — it abstained because there was nothing to review, not because
it saw the `_fivetran_active` re-correlation that makes the grain non-decidable. So the one
"correct" abstention on a target does not demonstrate the discrimination the stage claims; it
demonstrates the stage is silent when handed an empty input.

**3. Record-only HELD — the G10 design distinction is the one thing that protected the panel.**
Two passers (asana001, f1007) drew a REJECT verdict yet held PASS with byte-unchanged committed
SQL and ERROR=0. This confirms the "record, not a gate or build mandate" framing prevented the
h0012 false-green / damage-the-passer failure: a REJECT that *acted* would have rewritten f1007's
correct `sum` path or asana001's join. So the stage is *safe* (no passer reward regressed, G8
panel clean) but *useless* for flips (its only non-trivial signal — REJECT — is a guess it
correctly refuses to act on). Safe-but-non-discriminating = no live lever.

**4. Net for the program.** This is the predicted {0}-flips outcome reached by a *different and
sharper* mechanism than expected: not "abstains everywhere" but "REJECTs half the panel on
ungrounded guesses, then correctly declines to act." It re-confirms the standing wall
(`ade-bench-solver-blind-to-oracle`, `verification-without-oracle-real-world`): an independent
re-derivation against a generic invariant cannot beat the oracle, because the invariant is a
*pattern* and the deciding fact is *correlated-out* of every local relation. The honest residual
value is exactly two knowledge gains: (a) Method B is now **empirically** shown to false-reject
live (not just simulated), closing the "is the never-run Method B different?" question — it is
not; and (b) the observe-only `/tmp`+stdout routing is re-validated as the durable write-path. No
6th live lever emerges. Recommend **conclude/REJECTED** — do NOT promote to full (a full run
would only spread the same ungrounded-REJECT behavior across 48 cells; the 3-of-7 REJECT rate
(~43%) predicts ~20 ungrounded REJECTs at scale, and the only thing keeping them harmless is the
record-only rail, which delivers no upside). A secondary defect compounds it: the record-emit is
not even reliable (ana-eng001 emitted no concrete `plan_review.json` — the same free-form
schema-drift h0041 already flagged), so the "standing reasoning probe" value is itself leaky.

## Verdict

**REJECTED — rejected-as-written (NO-GO at smoke; knowledge gain). @baseline UNCHANGED at
31/48 (`runs/ade-bench-baseline/622bdedac572b479`); NOT promoted.**

The FIRST LIVE run of Method B FALSE-REJECTS on the oracle wall. The stage emitted
`verdict:REJECT` on its own abstention target `asana004` — the exact cell the spec said MUST
record `PROCEED_UNDETERMINED` — citing `contradicting_line: "from project_user"`. That is a
guess pattern-matched onto a FROM clause from the invariant's "never grain from a pre-filtered
child" template, NOT a locally-grounded contradiction: whether the canonical grain is `project`
or `project_user` is fixed by the hidden expected output (taxonomy Track Z, oracle-only `int_`
convention). The single "correct" abstention on a target (`intercom001` →
`PROCEED_UNDETERMINED`) was an **accident of empty SQL** ("no existing intercom__threads SQL
present" — a creation task), not the predicted `_fivetran_active` re-correlation. So Method B is
**empirically NO better than Method A** on the wall: an independent re-derivation against a
generic leak-clean invariant, applied as a *pattern*, false-rejects exactly where the deciding
fact is correlated-out of every local relation. The detector is falsified.

**The record-only rail kept it HARMLESS — the one thing that worked.** Of the 7 cells that
emitted a concrete record, 3 drew a REJECT (`asana004`, plus the PASSERS `asana001` and `f1007`),
but the "record, not a gate or build mandate" design held: both REJECTed passers kept
byte-unchanged committed SQL with ERROR=0 and held PASS. No passer reward regressed (G8 panel
clean); the single real build delta was `asana004` Got 3→6, variance on a CREATE task neither
version can ground. Strict audit clean (8/8, `tainted:0`, `coverage_missing:0`); score
`stratified_pass_at_1 = 0.75` (6/8). So the stage is **safe but non-discriminating** — its only
non-trivial signal (REJECT) is a guess it correctly refuses to act on. Safe-but-useless = no live
lever. A full run would only spread ~20 ungrounded REJECTs across 48 cells (~43% REJECT rate) with
zero upside, harmless only by the record-only rail → do NOT promote to full.

**Residual value = two knowledge gains.** (1) Method B is now *empirically* shown to false-reject
live (not just simulated), closing the standing "is the never-run Method B different from Method
A?" question — it is not; both hit `ade-bench-solver-blind-to-oracle` /
`verification-without-oracle-real-world`. (2) The h0041 `/tmp`+stdout observe-only write-path is
re-validated a second time as the durable record route (recovered on 7/8 cells). A secondary
defect compounds the negative: `ana-eng001` emitted only the README template, no concrete record —
the free-form schema drifts under gpt-5.5 (a 2nd sighting after h0041), so any ENFORCED downstream
consumer must hard-pin the schema rather than trust this emit. The WORKFLOW-REFINE.md structural
entry is finalized to its terminal state. No follow-up hypothesis is filed — the oracle-wall
finding closes the Method-B question, and h0037 (E-RMS) is the remaining queued run-worthy bet.

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

## Stage Report: smoke

- DONE: Smoke run completed (detached nohup, polled via Monitor across turns ~1h15m). Strict audit clean + captured>0 on all 8; focused score + clean-audit attestation recorded in `## Smoke result`.
  `rk audit ee924fbc9d3b0b20 --policy strict` → `clean: 8, tainted: 0, coverage_missing: 0`; `rk score` → `stratified_pass_at_1=0.75` (6/8), n_completed=8, n_errored=0; captured: all 8 cells codex.txt 60–83KB + jsonl 268–664KB.
- DONE: Decisive Method-B reads (plan_review.json recovered from session transcript on 7/8). (a) ABSTENTION FAILED — asana004 emitted REJECT (predicted PROCEED_UNDETERMINED; Got 3→6); intercom001 PROCEED_UNDETERMINED but for the wrong empty-SQL reason. (b) NO passer reward regressed (G8 clean) BUT the verdict probe REJECTed 2 passers (asana001, f1007) — record-only held, committed SQL byte-unchanged, ERROR=0. (c) plan_review.json present & non-empty on 7/8 — ana-eng001 emitted no concrete record (schema drift).
  Per-cell table in `## Smoke result`.
- DONE: Per-cell verdict distribution reported (the live-rail characterization): among the 7 cells that emitted a concrete record, **4 PROCEED_UNDETERMINED** (airbnb001, asana003, intercom001, quickbooks002) **/ 3 REJECT** (asana004, asana001, f1007); **+1 missing** (ana-eng001 — no concrete record).
  See `## Behavioral analysis`.
- DONE: Workflow-refinement evaluation + `_artifacts/WORKFLOW-REFINE.md` entry appended (new-stage structural lever; first LIVE Method B). Conclusion: Method B empirically false-rejects live (same oracle wall as Method A); routing fix re-validated; record-only rail is the sole safety.
  Entry: "Plan Review (Method B): the FIRST LIVE run … (h0038 smoke NO-GO, 2026-06-09)".

### Summary

First LIVE run of Method B. Infrastructure mostly worked: stage fired and the h0041 `/tmp`+stdout routing recovered a concrete `plan_review.json` on 7/8 cells (ana-eng001 emitted only the template — schema drift, second confirmation of the h0041 free-form-drift finding). The CONTENT falsifies the value claim: the stage emitted REJECT on the abstention target asana004 (a guess pattern-matched onto `from project_user`, not a locally-grounded contradiction — the canonical grain is oracle-only) and on 2 passers; the only "correct" abstention on a target (intercom001) was an accident of empty SQL. Audit clean (8/8, tainted:0), score 0.75 (6/8), no passer reward regressed because the record-only rail held — but the verdict layer is non-discriminating. **Go/no-go = NO-GO → conclude/REJECTED.** Method B is empirically no different from Method A on the oracle wall; do not promote to full (would spread ungrounded REJECTs across 48 cells with zero upside, kept harmless only by the record-only design).

**Verdict distribution (authoritative):** among the 7 cells with a concrete record, **4 PROCEED_UNDETERMINED** (airbnb001, asana003, intercom001, quickbooks002) **/ 3 REJECT** (asana004, asana001, f1007); **ana-eng001 emitted no concrete record**. (Recovered by reading the final emitted record per cell from the transcript — raw `verdict` token counts are noisy because the README prose itself contains "verdict:REJECT … else verdict:PROCEED_UNDETERMINED".)

## Stage Report: conclude

- DONE: Write the terminal `## Verdict`: REJECTED — knowledge gain.
  `## Verdict` states REJECTED / rejected-as-written: the first LIVE Method B FALSE-REJECTS on the oracle wall (asana004 → `verdict:REJECT` on its own abstention target, a guess pattern-matched on `from project_user`; intercom001 abstained only by accident of empty-SQL); record-only kept it HARMLESS (2 passers drew spurious REJECTs but committed SQL byte-identical, no passer regressed; audit clean 8/8, score 0.75); Method B empirically no better than Method A; @baseline UNCHANGED 31/48, NOT promoted.
- DONE: Finalize the `_artifacts/WORKFLOW-REFINE.md` h0038 entry to a FINAL state (h0038 IS a NEW-STAGE structural lever — mandatory).
  Status → **rejected-as-written** (detector falsified / record-only rail safe but useless); learning line sharpened to "an independent JOIN-shape re-derivation cannot distinguish a locally-decidable contradiction from an oracle-only grain convention → guesses REJECT on the wall"; bears-on flags the free-form record SCHEMA-DRIFT as a 2nd sighting after h0041 (any ENFORCED consumer like h0040/M2 needs a PINNED schema and must NOT trust this trigger to revert); /tmp+stdout routing re-validated noted (durable 7/8, after 8/8 at h0041).
- DONE: Confirm @baseline NOT promoted and NO new follow-up hypothesis filed.
  No `rk baseline promote` / `rk registry add run` issued — @baseline stays `runs/ade-bench-baseline/622bdedac572b479` (31/48); no new `h<NNNN>-<slug>.md` filed — the Method-B/oracle-wall finding closes the re-derive-without-oracle family and h0037 (E-RMS) is the queued remaining run-worthy bet, so no new flip-seeking lever is warranted (escalated to captain by conclude rather than reflexively filing).

### Summary

Terminal conclude for h0038 (NO-GO at smoke, captain-decided REJECTED). Wrote the `## Verdict`: REJECTED — knowledge gain. The first LIVE run of Method B FALSE-REJECTS on the oracle wall — it cannot distinguish a locally-decidable contradiction from an oracle-only grain convention, so it guessed REJECT on its own abstention target asana004 (`from project_user`) and on 2 passers, while the only "correct" abstention (intercom001) was an accident of empty SQL. The record-only rail kept it HARMLESS (no passer reward regressed; committed SQL byte-identical; audit clean 8/8; score 0.75), but the detector is useless — Method B is empirically no different from Method A on the wall. Finalized the WORKFLOW-REFINE.md new-stage entry to **rejected-as-written** with a sharpened learning line and a bears-on flag for h0040/M2 (the schema-drift is a 2nd sighting after h0041 → enforced consumers need a pinned schema). @baseline NOT promoted (stays 31/48); NO follow-up hypothesis filed (h0037/E-RMS is the queued bet; the oracle-wall finding closes the Method-B question). Pure documentation finalization — no `rk` command re-run.
