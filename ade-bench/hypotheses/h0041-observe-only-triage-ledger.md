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

## Smoke result

## Run result

## Behavioral analysis

## Verdict
