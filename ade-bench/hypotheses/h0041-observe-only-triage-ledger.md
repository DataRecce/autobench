---
id: h0041
title: Observe-only triage ledger — the h0040 three-clause trigger in OBSERVE-ONLY mode, writing triage.json {claim, clause_results, would_abstain} on all 48, never reverting; de-risks h0040 before it is trusted to revert
status: propose
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §4 M3 (captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 5. Observe-only de-risk of h0040 (the M2 enforced abstention rail). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-08T14:29:36Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

**Falsifiable claim (the single README change — a NEW observe-only `## Stage:` running the h0040
three-clause trigger in OBSERVE-ONLY mode):** adding a stage that runs the same fixed three-clause
trigger as the enforced abstention rail (h0040) but in pure observe-only mode — writes
`triage.json {claim, clause_results, would_abstain}` on all 48 and **never reverts or alters anything**;
the build proceeds EXACTLY as baseline — will produce the `would_abstain` distribution across the 48
known verdicts **at guaranteed zero score impact** (`Got N` UNCHANGED on all 48), and the survivor
**airbnb009 must NOT be flagged `would_abstain`** (proof the future enforced rail would not suppress the
one real fix). This is a **method instrument** de-risking h0040; expected flips **{0}** by construction.

**The single solver-README change.** Add exactly one observe-only `## Stage:` header running the h0040
three-clause trigger (instruction names the deciding quantity? existing `schema.yml` names it? raw
`SELECT FROM {{ source(...) }}` conservation/coverage probe — count + key-level anti-join from the
IMMUTABLE source — decides it?) but emitting ONLY `triage.json {claim, clause_results, would_abstain}`.
It reverts nothing, alters no committed SQL, and gates nothing; the build proceeds exactly as baseline.
Guaranteed zero score impact.

**Independent non-oracle signal.** Identical to h0040's clause-3 source: the raw, IMMUTABLE
`{{ source(...) }}` relation read directly (count + key-level anti-join), the task instruction, and the
existing `schema.yml`. But here the trigger only RECORDS its decision — it never acts on it. No hidden
`AUTO_*` / `solution__*` / `check_option_*` / `tests/AUTO_*` is named or read.

**Leading indicator (distance, `Got N`).** `Got N` **UNCHANGED on all 48** is the SUCCESS condition
(the observe-only contamination tripwire) — the stage reverts nothing and changes no SQL, so any `Got N`
movement means the observe-only gate-strip leaked = contamination = NO-GO. The discovery read is the
`would_abstain` distribution: a passer flagged `would_abstain` is a *predicted h0040 false-revert* (the
regression surface the enforced rail would expose); the survivor **airbnb009 must NOT be flagged** (proof
the enforced rail would not suppress the one real fix). This `would_abstain` map is the green-light
precondition before h0040 is ever allowed to revert in a real run.

**Kill-path / predicted failure mode.** The trigger is the same tier-3 raw-source/coverage mechanism
Round 1 proved mis-discriminates: by h0030 the probe comes back empty on genuinely-oracle-only intercom
(false-negative); by h0036 the coverage probe fires on ana-eng007 whose coverage is fixable but value is
oracle-only. So the ledger is a *map of where the trigger mis-fires* — useful for sharpening h0040 — but
it does NOT certify the trigger as a clean oracle-only detector; it is a low-cost instrument, not a
discovery. The kill is two-sided: (i) any `Got N` movement on a sampled passer = the observe-only
gate-strip leaked = contamination = NO-GO; (ii) an absent/empty `triage.json` on the sampled cells
(`test -f` fails) = the trigger went inert and delivers no ledger = REJECTED. A `would_abstain` flag on
the survivor airbnb009 is NOT a kill of THIS instrument (the ledger correctly recording it would be a
finding) — but it is a red flag against ever promoting h0040 to revert mode.

**Dead family it must avoid (proposal §6 map) + how it differs.** Like h0039, it must not become **D9
new-stage/arbitration-architecture** by sneaking any revert or build-to-satisfy behavior in — it is
strictly observe-only (writes `triage.json`, alters nothing). It re-uses the **D2 grain-reconcile** /
**D7 coverage** trigger mechanism that Round 1 proved mis-discriminates, but it does so deliberately and
only to RECORD where it mis-fires (a map, not a detector) — it never acts on the trigger, so it cannot
inherit D2's correlated-error false-green into a build decision or D7's coverage-masks-value regression.
The only contamination path is a gate-strip leak, which the `Got N`-unchanged tripwire catches.

**Target datasets.** Method instrument targeting **infrastructure / all 48** — there is no flippable
target by construction. The deliverable is the `would_abstain` distribution across the 48 known
verdicts. The decisive smoke reads are (a) `triage.json` present and non-empty on the sampled cells via
`test -f`, (b) `Got N` UNCHANGED on a sampled cross-family passer panel (the contamination tripwire),
and (c) the survivor `ade-bench-airbnb009` NOT flagged `would_abstain`.

**Honest expectation.** **{0}** flips — guaranteed zero score impact. Value: the `would_abstain` map
that de-risks h0040 before it is ever trusted to revert (a passer flagged `would_abstain` = a predicted
false-revert; airbnb009 must NOT be flagged). Honest caveat: the trigger is the same mechanism Round 1
proved mis-discriminates (h0030 false-negative on intercom, h0036 fires on ana-eng007 whose value is
oracle-only), so the ledger maps where the trigger mis-fires — useful for sharpening h0040, but it does
not certify the trigger as a clean oracle-only detector. This is a `trials: 1`, judge-by-artifact
entity; it faces its own propose + smoke gate, and the captain decides whether it ever runs.

**Scope.** Workflow-stage / prompt lever only; benchmark FIXED; no expanded solver access; leak-guard
intact (the stage references only the immutable raw `source()`, the task instruction, and the existing
`schema.yml`, and names no hidden `AUTO_*` / `solution__*` / `check_*` / verifier test, no
`equality test` / `has less columns` / `expected output seed`, no `Got N` or row count, and no
`curl`/`wget`/`git clone`/web/published-solution fetch). The change touches exactly one new observe-only
`## Stage:` header and leaves the leak-guard prose + the four existing stages byte-identical. The full
spec differs from `@baseline` only in `experiment:` + `solver_workflow:`; the smoke spec additionally
adds `benchmark.tasks` (a cross-family sentinel/canary panel + the survivor `ade-bench-airbnb009` for
the `would_abstain` non-flag read).

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0041-observe-only-triage-ledger.yaml` shows only
`experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md` adds exactly
one observe-only `## Stage:` header that writes `triage.json` and reverts/alters NOTHING, leaves the
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
`triage.json` is present and non-empty on the sampled cells via `test -f` (the trigger did not go inert),
(b) `Got N` is byte-unchanged on every sampled passer (the observe-only gate-strip held; no
contamination), and (c) the survivor `ade-bench-airbnb009` is NOT flagged `would_abstain` (the future
enforced rail would not suppress the one real fix). ANY `Got N` movement = contamination = NO-GO; an
absent/empty `triage.json` = inert = REJECTED.

## Gatekeeper review

**Recommendation: APPROVE** — exactly one new observe-only `## Stage:` added; leak-guard +
the four existing stages byte-identical; full spec differs only in `experiment:` +
`solver_workflow:`; smoke spec adds only `benchmark.tasks`; both frozen; routing fixes the
h0039 dead-precondition failure (unconditional write + `cat` to the durable session transcript).
No FAILs. The single WARN (G7) is the by-design inertness watch-item the entity already names.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-08). Reviewed 2026-06-08T14:36Z.

Fork parent resolved: `source:` says `solver_workflows/codex-ade-dbt-minimal`; `@baseline`
(run `622bdedac572b479`) config `agent.kwargs.solver_workflow = solver_workflows/codex-ade-dbt-minimal`
— agree. G1/G6 diffed against `codex-ade-dbt-minimal`.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff` is purely additive (`49a50,117`): one new `## Stage: Triage ledger (observe-only …)`; stage count 4→5; no other stage or guardrail prose touched. |
| G2 leak-guard intact | PASS | Leak-guard prose (lines 1–32) byte-identical; forbidden-token grep over the 67 added lines (AUTO_/solution__/check_*/verifier/equality test/Got N/row count/curl/wget/git clone/web) returns CLEAN after rewording "the verifier ignores it" → "is not part of the final project source state that is scored". |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0041-….yaml` shows only `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff` full→smoke adds only the `benchmark.tasks:` block (+ comments); all 8 slugs `ade-bench-` prefixed. Observe-only has no flippable target by construction; the panel carries the discovery reads the `## Hypothesis` names (airbnb009 non-flag read + intercom001/ana-eng007 present/non-empty reads). |
| G5 both frozen | PASS | `…frozen.yaml` + `…smoke.frozen.yaml` both exist; both carry `kind: spacedock_solver` + `runtime: codex`; smoke frozen carries all 8 tasks. |
| G6 resolver fidelity | PASS | Inserted text is the h0040 three-clause trigger (instruction / existing `schema.yml` / raw `{{ source() }}` count + key-level anti-join) in OBSERVE-ONLY mode emitting only `triage.json {claim, clause_results, would_abstain}`. It is independent (reconciles against the immutable raw source), NOT self-anchored: it never re-runs/compares-to its own model and explicitly forbids reverting/rewriting/re-selecting. Matches the Falsifiable claim; no scope creep. |
| G7 actionability/inert-risk | WARN | Observe-only record-emission with an unconditional on-disk write + a `cat`-to-stdout durability step is mechanical (not abstract restructure prose). Inert-risk is the *named* kill-path: this is the sibling of h0039, which went inert because its record routed through the dead `/razorback-freeze` "exactly one child directory" precondition. **This variant fixes that** — write is unconditional and the authoritative copy is the stdout/session-transcript record (the only home reasoning has durably survived per the h0039 WORKFLOW-REFINE finding; cf. h0017 `Contract:` blocks). Residual inert-risk is only if the solver skips the stage entirely — the smoke present/non-empty read on intercom001/ana-eng007 is the kill check. |
| G8 regression-canary coverage | PASS | The stage is **generative** (fires on every task). Smoke panel carries one `@baseline` passer per family as a Got-N contamination tripwire — airbnb001 / ana-eng001 / asana001 / f1007 / quickbooks002 (intercom has no @baseline passer, so intercom001 is its representative + a fired-and-failed read). Because the stage touches NO SQL/config/files (observe-only), the *only* regression surface is a gate-strip leak, which a single Got-N tripwire per family catches; no construct-family perturbable-doublet is required (the lever cannot perturb any model). |
| G9 selector independence | N/A | No multi-candidate / selector protocol — single observe-only record, no N candidates, no selection. |
| G10 self-correcting false-positive | N/A | Not self-correcting — the stage records `would_abstain` and explicitly **acts on nothing** (no revert, no fix-on-disagreement); the build proceeds exactly as baseline. The only contamination path is a gate-strip leak (caught by the Got-N tripwires), not a self-correcting overwrite. |
| G11 multi-model-target risk | N/A | No flippable target by construction; expected flips {0}. Nothing is credited as a flip, so the multi-model variance trap does not apply. |

**For the captain:** APPROVE-class. The decisive de-risk vs h0039 is the routing fix — `triage.json` is written unconditionally and `cat`-ed to stdout so it lands durably in the worker session transcript (`agent/sessions/*.jsonl`), the one location that survived even the notes-free @baseline run; it does NOT depend on the dead `/razorback-freeze` single-child precondition. Smoke success is INVERTED: (a) Got N byte-unchanged on all 5 passer tripwires (contamination kill), (b) `triage.json` record present & non-empty on intercom001/ana-eng007 (inertness kill), (c) airbnb009 NOT flagged `would_abstain` (the survivor must be found decidable). The single WARN (G7 inert-risk) is the hypothesis's own named kill-path, already mitigated by the routing change and checked at smoke.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: DURABLE ARTIFACT ROUTING (the make-or-break h0039 fix)
  The new stage writes `triage.json` to a fixed `/tmp/triage.json` **unconditionally** (no
  single-child `if`) and then `cat`s it to stdout so the full record lands durably in the worker
  session transcript (`agent/sessions/*.jsonl`) — the only home reasoning survived in this harness
  (h0017 `Contract:` blocks; cf. h0039 WORKFLOW-REFINE). Confirmed host-side `_razorback/freeze` is
  empty in @baseline `622bdedac572b479`, so the `/razorback-freeze` precondition is structurally
  dead; the stage explicitly does NOT depend on it.
- DONE: README change is EXACTLY ONE new observe-only `## Stage:`
  `diff codex-ade-dbt-minimal/README.md → fork` is purely additive (`49a50,117`, 68 lines): one new
  `## Stage: Triage ledger (observe-only …)` running the h0040 three-clause trigger (instruction /
  existing `schema.yml` / raw `{{ source() }}` count + key-level anti-join) emitting only
  `triage.json {claim, clause_results, would_abstain}`; reverts/alters/gates nothing. Leak-guard
  prose (lines 1–32) + the four existing stages (Exploration/Implementation/Validation/Finalization)
  byte-identical; forbidden-token grep over added lines CLEAN (reworded the one "verifier" hit).
- DONE: Smoke spec `benchmark.tasks` is a CONTAMINATION panel + discovery reads
  8 tasks: 5 cross-family @baseline passers as Got-N tripwires (airbnb001/ana-eng001/asana001/f1007/
  quickbooks002), the survivor ade-bench-airbnb009 (would_abstain NON-flag read), and the
  fired-and-failed cells ade-bench-intercom001 + ade-bench-ana-eng007 (triage.json present/non-empty).
  G4 diff = only `benchmark.tasks`; all slugs `ade-bench-` prefixed; both specs frozen.
- DONE: Run the gatekeeper; record per-rule table + recommendation
  `## Gatekeeper review` written: APPROVE, no FAILs, one by-design WARN (G7 inert-risk, mitigated by
  the routing fix); G9/G10/G11 N/A (observe-only, no candidates, no flippable target).

### Summary

Forked `codex-ade-dbt-minimal` → `h0041-observe-only-triage-ledger` and added exactly one
observe-only `## Stage: Triage ledger` running the h0040 three-clause trigger but emitting only
`triage.json` and acting on nothing — build proceeds exactly as baseline. The decisive change vs the
just-rejected sibling h0039 is the routing: the write is unconditional and the authoritative copy is
`cat`-ed to stdout so it survives in the durable session transcript, not the dead `/razorback-freeze`
single-child precondition (verified empty in the @baseline run-dir). Full spec differs from baseline
only in `experiment:` + `solver_workflow:`; smoke spec adds only the 8-task panel; both frozen with
`kind: spacedock_solver` / `runtime: codex` / `trials: 1` preserved. Gatekeeper: APPROVE. Smoke
success is INVERTED — Got N unchanged on the 5 passers (contamination kill), triage.json present on
the two failers (inertness kill), airbnb009 NOT flagged would_abstain (survivor decidable).
