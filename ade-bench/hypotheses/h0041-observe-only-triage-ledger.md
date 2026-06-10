---
id: h0041
title: Observe-only triage ledger — the h0040 three-clause trigger in OBSERVE-ONLY mode, writing triage.json {claim, clause_results, would_abstain} on all 48, never reverting; de-risks h0040 before it is trusted to revert
status: conclude
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §4 M3 (captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 5. Observe-only de-risk of h0040 (the M2 enforced abstention rail). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-08T14:29:36Z
completed: 2026-06-10
verdict: CONCLUDE (recommended; captain decides) — observe-only instrument succeeded on its own terms: contract held (tainted:0, both net-0 flips are solver variance not a gate-strip leak), routing scales to 48/48, 0/48 would_abstain. @baseline NOT promoted (net 0, {0}-flip by construction). h0040 (the rail this de-risks) already REJECTED-inert → map is retrospective de-risk knowledge; no follow-up filed.
score: 0.6458 (31/48, full run fe1505abeeddabff; = @baseline 31/48, net 0; strict audit clean, 0 errored)
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

**Verdict: GO → full.** One-line reason: the observe-only stage fired and durably emitted a
triage record on all 8 cells (the h0039 routing fix WORKED), `Got N` is byte-unchanged on every
passer (zero contamination), and the survivor airbnb009 is NOT flagged `would_abstain` — all three
inverted success conditions met.

Run dir: `runs/ade-bench-h0041-observe-only-triage-ledger/45c2ba6667a47a60`
(frozen spec `specs/h0041-observe-only-triage-ledger.smoke.frozen.yaml`,
README hash `sha256:812509727c4459ad98a237e49e3f3da9adf5bd0dc47d4147e8fbf4759b4738bf`).

**AC-2 — clean strict audit paired with the score (same run-dir):**
`rk audit --policy strict` → `summary: {clean: 8, coverage_missing: 0, tainted: 0}` (8/8 cells
`taint_status: clean`). `captured = 1` (>0) on all 8 `subagent-trace-manifest.json`.
`rk score` → `stratified_pass_at_1 = 0.625` (5/8), `n_errored = 0`, verdict `above` the 0.1875 anchor.

**Verdict split (the clean expected outcome — zero score impact by construction):**
5 reward=1.0 (the @baseline passers held) / 3 reward=0.0 (the @baseline failers held). No flips, no
regressions — exactly as predicted for an observe-only instrument.

**Inverted read (a) — `Got N` byte-unchanged on all 5 passers (contamination tripwire):** PASS.
Final verifier tallies (smoke vs @baseline `622bdedac572b479`) are byte-identical on every passer,
and the 3 failers held identical distances:

| Task | Reward | @baseline final tally | Smoke final tally | Got N |
|------|--------|------------------------|-------------------|-------|
| airbnb001 | 1.0 | 12/5/10 PASS, ERR=0 | 12/5/10 PASS, ERR=0 | unchanged |
| ana-eng001 | 1.0 | PASS=1, ERR=0 | PASS=1, ERR=0 | unchanged |
| asana001 | 1.0 | 38/1/2 PASS, ERR=0 | 38/1/2 PASS, ERR=0 | unchanged |
| f1007 | 1.0 | 3/3/6 PASS, ERR=0 | 3/3/6 PASS, ERR=0 | unchanged |
| quickbooks002 | 1.0 | 100/3/8 PASS, ERR=0 | 100/3/8 PASS, ERR=0 | unchanged |
| airbnb009 | 0.0 | Got 1, ERR=1 | Got 1, ERR=1 | unchanged |
| intercom001 | 0.0 | Got 7, ERR=1 | Got 7, ERR=1 | unchanged |
| ana-eng007 | 0.0 | Got 5, ERR=1 | Got 5, ERR=1 | unchanged |

The observe-only gate-strip held: the stage reverted/altered nothing. NO contamination.

**Inverted read (b) — triage record present & non-empty in the SESSION TRANSCRIPT on all 8 cells
(inertness kill — the make-or-break test of the h0039 routing fix):** PASS. The record was written
to `/tmp/triage.json` (torn-down container scratch, NOT in the run-dir — the h0039 trap) and the
authoritative copy survives as the `sed`/`cat`/`tee` stdout in each cell's
`agent/sessions/2026/06/08/*.jsonl`. A filled, non-empty record was recovered for **all 8** cells —
the routing fix decisively beat h0039's inert/absent record.

**Inverted read (c) — survivor airbnb009 NOT flagged `would_abstain`:** PASS. airbnb009's record has
all three clauses `supports_*` (decidable from instruction + schema.yml + raw-source probe);
`would_abstain` is false (the enforced rail would NOT suppress the one real fix).

**Full `would_abstain` distribution across the panel — 0 of 8 flagged `would_abstain: true`:**

| Task | Reward | Record schema | clauses (instr/schema/raw) | would_abstain |
|------|--------|----------------|-----------------------------|---------------|
| airbnb001 | 1.0 | bool, no `would_abstain` key | T / T / F | false (2 true) |
| ana-eng001 | 1.0 | `three_clause_check` + `classification:no-op` | T / F / F | false (instr) |
| asana001 | 1.0 | spec schema (explicit) | F / T / F | **false** |
| f1007 | 1.0 | narrative `status` (`supports`) | supports×3 | false |
| quickbooks002 | 1.0 | spec schema (explicit) | T / T / F | **false** |
| airbnb009 | 0.0 | narrative `status` (`supports_*`) | supports×3 | false |
| intercom001 | 0.0 | spec schema (explicit) | T / T / F | **false** |
| ana-eng007 | 0.0 | spec schema (explicit) | T / T / F | **false** |

`grep '"would_abstain": true'` over every cell transcript returns EMPTY. No revert/hold-back behavior:
all 8 cells ran Implementation normally (4–9 `apply_patch` calls each); the only "revert/abstain"
grep hits are the README guardrail prose echoed in the dispatch prompt, not solver action.

## Run result

**Headline (M3 deliverable — the clean full run): `stratified_pass_at_1 = 0.6458` = EXACTLY @baseline
(31 PASS / 17 FAIL = 31/48), net 0 vs @baseline 0.6458 — the by-construction observe-only outcome.**
Run dir: `runs/ade-bench-h0041-observe-only-triage-ledger/fe1505abeeddabff` (frozen spec
`specs/h0041-observe-only-triage-ledger.frozen.yaml`, all 48 tasks, `trials: 1`). 48 cells completed,
`n_errored = 0`, verdict `above` the 0.1875 anchor. Finished cleanly (rk emitted `result.json` +
harbor view/upload hints; no traceback, no freeze-lock error).

**AC-2 — clean strict audit paired with the score (SAME run-dir):** `rk audit
runs/ade-bench-h0041-observe-only-triage-ledger/fe1505abeeddabff --policy strict` →
`summary: {clean: 48, coverage_missing: 0, tainted: 0}` — all 48 trials `taint_status: clean`, zero
non-clean. `captured = 1` (>0) on all 48 `subagent-trace-manifest.json` (48/48 manifests present). The
score is trustworthy.

**Methodology consistency (no smoke→full drift):** the full run's solver README
`solver_workflow_content_hash` = `sha256:812509727c4459ad98a237e49e3f3da9adf5bd0dc47d4147e8fbf4759b4738bf`
(in `fe1505abeeddabff/config.json` + `lock.json`) is BYTE-IDENTICAL to the smoke run
`45c2ba6667a47a60`'s recorded hash and to the hash in both frozen specs. The full spec differs from the
smoke spec ONLY in `benchmark.tasks` (null/all-48 vs the 8-cell panel) — same solver README, same
`sealed_hash afb12203d4f920b450622fa7d40f5e0e`. No methodology drift.

**Net 0 — but NOT a byte-identical cell-level hold (the honest caveat for analyze).** The aggregate is
exactly @baseline (31/48), but slug-paired per-cell outcomes show TWO offsetting single-cell flips, not
zero movement:

| Cell | @baseline | h0041 full | Direction |
|------|-----------|------------|-----------|
| `ade-bench-airbnb009` | 0.0 (FAIL) | 1.0 (PASS) | FLIP UP |
| `ade-bench-f1006-hard` | 1.0 (PASS) | 0.0 (FAIL) | REGRESSION |

NET (up − down) = **0**; the other 46 cells held their @baseline verdict. Attribution (pending the
analyze-stage per-cell `Got N` deep-dive): **airbnb009 is the documented stochastic-variance survivor**
— its FAIL→PASS flip is the same non-reproducible single-trial flip recorded across h0019 and the
oracle-program conclusion (it has flipped up in some `trials:1` runs and did NOT bank), and `f1006-hard`
is the offsetting borderline cell going the other way. This reads as single-trial run-to-run variance on
two borderline cells, NOT observe-only contamination — but it means the AC-3 "`Got N` UNCHANGED on every
cell" success condition is met at the AGGREGATE level (net 0, audit clean) yet is NOT byte-identical on
these two cells. Whether the movement is pure solver nondeterminism on borderline cells or a faint
gate-strip leak is precisely what the analyze-stage per-cell `Got N` / committed-SQL diff will adjudicate
(reserved for the next stage per the dispatch). The full `would_abstain` distribution across all 48 +
the contamination deep-dive are the analyze deliverable; this stage records only the clean-run
accounting.

---

### ANALYZE STAGE (interpretation; `rk runs diff` not used — it TypeErrors on ade-bench run-dirs, so the paired delta was computed from `per_trial_outcomes.json`, slug-paired, 10k bootstrap)

**Paired delta vs @baseline (slug-paired, 10k bootstrap).** 48/48 slugs paired. Mean per-cell delta
(full − baseline) = **+0.000000**; 10k-bootstrap 95% CI = **[−0.0625, +0.0625]** (straddles 0 — the two
offsetting single-cell flips). 46/48 cells held their @baseline verdict. Aggregate 31/48 = 31/48.

**THE DECISIVE CONTAMINATION ADJUDICATION — both flips are pure single-trial solver-reasoning VARIANCE,
NOT a gate-strip leak. The observe-only contract held on all 48.** For each flipped cell I read the
COMMITTED model SQL from the `apply_patch` `payload.input` in the session transcript (not chatter) in
both runs:

| Cell | @baseline committed SQL | h0041-full committed SQL | Verdict |
|------|--------------------------|---------------------------|---------|
| `ade-bench-airbnb009` (FAIL→PASS) | LARGE over-engineered rewrite of `models/agg/mom_agg_reviews.sql`: added `bounds_cte`, a `sentiments_cte` CROSS JOIN, restructured the LEFT JOIN + NULLIF guard — **FAILED** (Got 1). | ONE minimal surgical patch to the same file: `WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE FROM review_cte)` → `WHERE DATE_ACTUAL BETWEEN (MIN(REVIEW_DATE)) AND (MAX(REVIEW_DATE))` — the correct "row for every day in range" fix — **PASSED**. | Different solver SQL strategies, both the solver's OWN reasoning. The triage record (claim + `would_abstain:false`) contains NO SQL and did not author the patch. **Variance.** |
| `ade-bench-f1006-hard` (PASS→FAIL) | ONE correct patch: `sum(points)` → `max(points)` on `constructor_points.sql` + `driver_points.sql` — **PASSED**. | The SAME first patch (`sum`→`max`), THEN a SECOND patch that over-refined it: added `row_number()` season-standing-rank windowing + `WHERE season_standing_rank = 1`, dropped the `GROUP BY` — **FAILED**. | The full solver second-guessed and broke its OWN correct fix with an extra edit. The triage record carries NO SQL. **Variance (the solver did MORE editing).** |

On NEITHER cell did the observe-only triage record influence committed SQL — the record is claim +
clause booleans + (sometimes) `would_abstain`, never SQL, and the model files edited are the task's own
model SQL. The contamination tripwire HELD: strict audit `tainted: 0` on all 48, no triage→SQL coupling
on either flip, and 46/48 cells byte-held their @baseline verdict. airbnb009 is the documented stochastic
survivor (flips up non-reproducibly at `trials:1` per the oracle-program conclusion); f1006-hard is the
offsetting variance cell. **This is the success condition for an observe-only instrument** (the gate-strip
did not leak), with the honest precision that "net 0" is aggregate-level, not byte-identical on these two
single-trial-variance cells.

**THE M3 DELIVERABLE — the ALL-48 `would_abstain` distribution (recovered per-cell from the SESSION
TRANSCRIPT, not `test -f` the run-dir).** Routing held: **48/48 cells durably emitted a triage record**
(the `/tmp/triage.json` write + `cat`/`printf`/`tee`/`*** Add File` to the session transcript survived on
every cell — the h0039 routing fix scales to all 48; 4th-scale confirmation of the smoke result).

- **`would_abstain` = TRUE: 0 of 48** (literal key where present, else derived from the clause results
  per the h0040 rule "≥1 clause supports decidability ⇒ would_abstain false"). No cell would have
  abstained.
- **@baseline PASSERS flagged `would_abstain`: NONE** ⇒ on the full 48 a future enforced rail (h0040)
  would have predicted **ZERO false-reverts** — it would not have suppressed any of the 31 passers. This
  is the green-light precondition the M3 instrument was built to map.
- **The survivor `ade-bench-airbnb009` is NOT flagged `would_abstain`** (clauses `instruction=T`,
  `schema_yml=F`, `raw_source_probe=T` ⇒ decidable) ⇒ the enforced rail would NOT have suppressed the one
  real fix. ✔
- **Schema-drift caveat confirmed at full scale (sharp h0040-hardening requirement).** The literal
  `would_abstain` key is present on only **38/48** cells; **10/48** emitted a record with a DRIFTED schema
  (renamed keys `*_clause`; clauses nested as `{verdict, evidence}` or `{evaluated, supports_claim}`
  objects; or a narrative `load_bearing_claim` + `fixed_three_clause_check` list) and NO literal
  `would_abstain` field. The abstain decision is recoverable in every case (≥1 clause supports ⇒
  decidable), but an enforced consumer that *parses* a literal `would_abstain` would mis-read 10/48 and
  MUST NOT default-to-abstain on absence — it must DERIVE abstain from the clause results. (Retrospective:
  h0040 already concluded REJECTED-inert, so this is de-risk knowledge, not a live requirement — see the
  next-move note.)
- **Round-1 mis-discrimination wall still visible.** Unlike the smoke panel (where `raw_source_probe` was
  inert on 8/8), at full scale `raw_source_probe` DID fire as a deciding clause on ~26/48 cells — but it
  never independently OVER-abstained, and on the cells where it was the *only* true clause
  (e.g. f1003-hard, f1005-medium, ana-eng007-medium) it agreed with decidability rather than flagging
  abstain. So the trigger leaned conservative (never abstained on this fixed 48) — consistent with the
  h0030/h0036 finding that the tier-3 raw-source/coverage probe under-fires rather than cleanly detecting
  oracle-only intent. The map confirms LOW over-abstention risk but does NOT certify the trigger as a
  clean oracle-only detector.

**The 5 required questions.** (1) **Net + per-task ledger both directions:** net 0; +1
airbnb009 (FAIL→PASS), −1 f1006-hard (PASS→FAIL); other 46 held. (2) **Smoke-vs-full:** smoke (8 cells)
had 0/8 would_abstain, 8/8 emitted, Got-N unchanged; full (48) reproduces — 0/48 would_abstain, 48/48
emitted, audit clean — AND extends the smoke schema-drift caveat (8/8 drifted at smoke → 10/48 lack the
literal key at full) and the raw_source_probe finding (inert on the smoke 8 → fires on ~26/48 but never
over-abstains). No smoke→full README drift (content-hash byte-identical). (3) **Already-correct-and-broken
(the regression):** f1006-hard — baseline's `sum`→`max` was already correct and the full solver BROKE it
with a second over-refinement patch (`row_number()` ranking); not a triage effect, a solver-reasoning
regression. (4) **Was the change executed? (verify the committed artifact):** YES on all 48 — every cell
durably emitted a triage record to the session transcript (48/48), and the build proceeded with the
solver's own model edits committed (the observe-only stage altered NO committed SQL on any cell, verified
on the two flips). (5) **Prevention + next move:** see `## Verdict`.

## Behavioral analysis

**FULL RUN (all 48 cells) — `fe1505abeeddabff`.** The observe-only triage stage was exercised on every
one of the 48 cells, and the build proceeded exactly as baseline: 48/48 cells durably emitted a triage
record to the session transcript (the `/tmp/triage.json` write + stdout `cat`/`printf`/`tee`/`*** Add
File` routing held at full scale — the h0039 routing fix is now confirmed at 48-cell scale, not just the
8-cell smoke), and the committed model SQL on every cell is the solver's OWN work — the stage altered no
committed SQL anywhere. Net 0 vs @baseline (31/48), strict audit `tainted:0`, `captured>0` on all 48. The
two single-cell flips (airbnb009 up, f1006-hard down) were adjudicated in `## Run result`: both are
single-trial solver-reasoning variance (different SQL strategies / an extra over-refinement patch), NOT a
gate-strip leak — the contamination tripwire held. The all-48 `would_abstain` map: **0/48 would_abstain**,
no @baseline passer flagged (⇒ a future enforced rail would predict zero false-reverts on this fixed 48),
the survivor airbnb009 decidable. Two sharp caveats carried from smoke and now confirmed at scale:
(1) **schema drift** — only 38/48 cells emit a literal `would_abstain` key; 10/48 use a drifted/nested/
narrative shape, so an enforced consumer MUST derive abstain from the clause results, never parse the
field and default-to-abstain on absence; (2) the trigger **never over-abstained** but leaned on the
non-independent instruction/schema clauses and under-fired the independent raw-source probe as a *sole*
decider — it maps as conservative (won't suppress), not as a certified clean oracle-only detector
(the h0030/h0036 mis-discrimination wall persists). NB: h0040, the enforced rail this M3 de-risks, has
already concluded REJECTED-inert, so this 48-cell map is retrospective de-risk knowledge.

---

**SMOKE RUN (8-cell panel) — `45c2ba6667a47a60` (retained below for the smoke→full comparison).**

**The stage was exercised on every cell, and the build proceeded exactly as baseline.** Each of the
8 cells (a) stated a load-bearing claim, (b) ran a three-clause-style check, (c) wrote a record to
`/tmp/triage.json`, (d) printed it to stdout (durable in the session transcript), and (e) continued
to Implementation and committed model edits unchanged (`apply_patch` 4–9× per cell). The verdict and
`Got N` held byte-for-byte vs @baseline on all 8, so the observe-only contract was honored — the
record was emitted and acted-on-nothing.

**Decisive contrast with h0039 (the routing fix worked).** h0039 went inert: its record routed
through the dead `/razorback-freeze` "exactly one child" precondition and nothing durable was
emitted, so it could not even be tested. h0041's unconditional write-to-`/tmp` + print-to-stdout put
a filled, non-empty record into the durable session transcript on 8/8 cells. This is the first
positive demonstration in this loop that an observe-only stage can durably emit a substantive record
without contaminating the build. The `/tmp` scratch is correctly absent from the run-dir (so a naive
`test -f` in the run-dir would falsely read inert — the h0039 trap); the stdout capture is what makes
it durable, and that is the verified home.

**Schema drift — the substantive caveat for h0040.** The solver did NOT adhere to the spec's fixed
record shape. Three distinct shapes appeared: (i) the exact spec schema with boolean `clause_results`
+ explicit `would_abstain` (asana001, quickbooks002, intercom001, ana-eng007); (ii) a boolean
variant with renamed keys / extra fields and NO `would_abstain` key (airbnb001 `instruction/schema_yml/
raw_source_probe` bare booleans; ana-eng001 `three_clause_check` + `classification:"no-op"`);
(iii) a narrative `status`+`evidence` shape with no boolean and no `would_abstain` at all (airbnb009
`supports_*`, f1007 `supports` + `classification`/`minimum_fix`). The semantic decision is recoverable
in every case (at least one clause supports ⇒ decidable ⇒ would_abstain false), and the distribution
read is robust to the drift — but a downstream enforced rail (h0040) that *parses* `would_abstain` as
a literal field would mis-parse 4 of 8 cells (the field is absent), and on those it must NOT silently
default to "abstain." This is a concrete spec-hardening requirement for h0040: either pin the schema
hard (refuse to proceed without a literal boolean) or make the enforced rail derive abstain from the
clause results, not from a possibly-absent `would_abstain` key.

**`would_abstain` distribution interpreted for h0040 revert-mode risk.** 0/8 flagged `would_abstain:
true`. The most important read: **no passer was flagged would_abstain** ⇒ on this panel h0040 would
have predicted ZERO false-reverts (it would not have suppressed any of the 5 real passers). And the
survivor airbnb009 was found decidable ⇒ h0040 would not have suppressed the one real fix. BUT the
Round-1 mis-discrimination wall is still visible in the clause pattern: `raw_source_probe` came back
NOT-deciding (false / not the deciding clause) on 8/8 cells — the tier-3 raw-source/coverage probe is
the weakest clause and never independently decided a claim here; every "decidable" verdict rested on
the instruction or schema.yml clause (the self-anchored / instruction-echo sources). So this panel does
NOT certify the trigger as a clean oracle-only detector; it confirms the trigger leans on the
non-independent clauses, exactly the h0030 false-negative / h0036 coverage-masks-value failure mode.
The ledger is a useful MAP (the trigger would not over-abstain on this panel) but not a certification.

**Distance-to-pass on the 3 still-failing cells (unchanged from @baseline, as required):** airbnb009
`Got 1` (mom_agg_review_date_range), intercom001 `Got 7` (AUTO_intercom__threads_equality), ana-eng007
`Got 5` (AUTO_dim_products_equality). These are the @baseline distances byte-for-byte — the observe-only
stage moved nothing, confirming inertness-on-the-artifact (the desired property for THIS instrument).

## Verdict

**Recommended verdict: CONCLUDE — instrument SUCCEEDED on its own terms (captain decides).** The
observe-only triage ledger delivered exactly what M3 was built for and confirmed it at full 48-cell scale:

- **The observe-only contract held (the contamination tripwire passed).** Net 0 vs @baseline (31/48),
  strict audit `tainted:0`, `captured>0` on all 48, and on BOTH single-cell flips the committed model SQL
  is the solver's OWN reasoning with zero triage→SQL coupling (airbnb009: minimal `IN`→`BETWEEN` fix vs
  baseline's broken over-rewrite; f1006-hard: an extra over-refinement patch the solver added to its own
  correct `sum`→`max`). Both flips are single-trial solver-reasoning VARIANCE, not a gate-strip leak.
  46/48 cells byte-held @baseline. (Honest precision: "net 0" is aggregate-level, not byte-identical on
  those two stochastic cells — airbnb009 is the documented non-reproducible survivor.)
- **The routing fix scales (the make-or-break vs h0039).** 48/48 cells durably emitted a substantive
  triage record to the session transcript — the unconditional `/tmp`-write + stdout-capture beat h0039's
  dead-precondition inertness at full scale.
- **The M3 map: 0/48 would_abstain, no passer flagged, survivor decidable** ⇒ a future enforced rail
  would predict ZERO false-reverts on this fixed 48.

**@baseline NOT promoted** (net 0 — nothing to bank; this was {0}-flip by construction). **No reflexive
follow-up filed.** **Prevention / next-move** (the 5th required question): the two enforced-rail
hardening requirements this instrument surfaced — (1) DERIVE abstain from the clause results, never parse
a possibly-absent literal `would_abstain` (10/48 cells lack it under schema drift); (2) the trigger
under-fires the independent raw-source probe and leans on the non-independent instruction/schema clauses
(the h0030/h0036 wall), so it maps as conservative, NOT a certified oracle-only detector — are
RETROSPECTIVE de-risk knowledge only: **h0040, the enforced abstention rail this M3 was built to
de-risk, has already concluded REJECTED-inert.** With h0040 dead, there is no live consumer to harden;
escalate the two requirements as recorded knowledge (entity + WORKFLOW-REFINE), do NOT re-open the
enforced-rail family. This closes the M3 observe-only de-risk line.

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

## Stage Report: smoke

- DONE: Smoke run on `specs/h0041-observe-only-triage-ledger.smoke.frozen.yaml` completed; strict audit clean + captured>0; focused score + attestation recorded.
  Launched detached (nohup, PID 2932921, polled across turns); run `45c2ba6667a47a60` finished 8/8, 0 errored (1h11m). `rk audit --policy strict` → `{clean:8, coverage_missing:0, tainted:0}`; `captured=1` on all 8 `subagent-trace-manifest.json`; `rk score` → `stratified_pass_at_1=0.625` (5/8, verdict `above`). Recorded in `## Smoke result`.
- DONE: The three INVERTED reads with per-cell evidence.
  (a) `Got N` byte-unchanged vs @baseline on all 5 passers — confirmed (final verifier tallies byte-identical; the 3 failers held Got 1 / Got 7 / Got 5). No contamination. (b) triage record present & non-empty on intercom001 + ana-eng007 (and all 8) — recovered the `cat`/`sed`/`tee`-ed JSON from each cell's `agent/sessions/2026/06/08/*.jsonl`; NOT inert (the h0039 routing fix worked). (c) airbnb009 `would_abstain` = false (all 3 clauses `supports_*`, decidable). Full distribution: 0/8 flagged `would_abstain:true`.
- DONE: Workflow-refinement evaluation (new-stage structural lever); `_artifacts/WORKFLOW-REFINE.md` entry appended as part of the smoke commit.
  Routing fix WORKED (8/8 durable records vs h0039's zero); committed behavior byte-unchanged (Got N held); `would_abstain` map implies LOW over-abstention risk for h0040 (no passer flagged, survivor decidable) but with a sharp caveat — the independent `raw_source_probe` clause never decided on 8/8 cells, so decidability rests on the non-independent instruction/schema clauses. New entry: "Observe-only triage ledger: the stdout/session-transcript routing FIX works …".

### Summary

Smoke is a clean GO → full. The decisive result: the h0039 routing fix WORKED — an observe-only stage durably emitted a filled, non-empty triage record on all 8 cells (recovered from the session transcript, the `/tmp` scratch being correctly torn-down/absent from the run-dir), with ZERO build contamination (Got N byte-unchanged on every passer and failer; strict audit tainted:0; score 0.625 = the baseline 5/8 split). The `would_abstain` deliverable: 0/8 flagged abstain, the survivor airbnb009 found decidable — so on this panel h0040 would predict zero false-reverts. Two caveats for h0040: (1) the record schema DRIFTED into 3 incompatible shapes (4 of 8 cells lack a literal `would_abstain` field) so an enforced consumer must derive abstain from the clause results, not parse the field; (2) the only independent clause (raw_source_probe) decided nothing on 8/8 — the trigger's "decidable" verdicts lean on the non-independent instruction/schema clauses, inheriting the Round-1 mis-discrimination wall.

## Stage Report: full

- DONE: Full 48-task run on `specs/h0041-observe-only-triage-ledger.frozen.yaml` completed; strict audit clean + captured>0 on every cell; score recorded.
  Launched DETACHED (nohup, PID 3630703, polled across turns via a persistent Monitor — never foregrounded). Run `fe1505abeeddabff` finished all 48 cells, `n_errored = 0`. `rk audit --policy strict` → `{clean: 48, coverage_missing: 0, tainted: 0}` (48/48 `taint_status: clean`, zero non-clean); `captured = 1` on all 48 `subagent-trace-manifest.json`. `rk score --format json` → `stratified_pass_at_1 = 0.6458` (31/48), verdict `above` the 0.1875 anchor. Recorded in `## Run result`.
- DONE: Headline + net vs @baseline recorded. 31 PASS / 17 FAIL = 0.6458 = EXACTLY @baseline (31/48), **net 0** — the by-construction observe-only outcome. Honest caveat surfaced: the net-0 aggregate hides TWO offsetting single-cell flips (airbnb009 FAIL→PASS, the documented stochastic survivor; f1006-hard PASS→FAIL, the offset) — single-trial variance on two borderline cells, NOT byte-identical at the cell level. The per-cell `Got N` / committed-SQL contamination adjudication is reserved for the analyze stage.
- DONE: Methodology consistency (no smoke→full drift) confirmed. Full run solver README `solver_workflow_content_hash = sha256:812509727c4459ad98a237e49e3f3da9adf5bd0dc47d4147e8fbf4759b4738bf` (in `fe1505abeeddabff` config.json + lock.json) is byte-identical to the smoke run `45c2ba6667a47a60`'s recorded hash and to both frozen specs; the full spec differs from smoke only in `benchmark.tasks` (all 48 vs the 8-cell panel); `sealed_hash afb12203d4f920b450622fa7d40f5e0e` matches.

### Summary

The M3 clean full run is banked: run dir `runs/ade-bench-h0041-observe-only-triage-ledger/fe1505abeeddabff`, `stratified_pass_at_1 = 0.6458` = exactly @baseline 31/48, net 0, strict audit `{clean:48, tainted:0}`, captured>0 on all 48, 0 errored, no smoke→full README drift (content-hash byte-identical to smoke). The expected observe-only result. ONE honest caveat for the analyze stage: net 0 is at the aggregate level, not byte-identical at the cell level — two offsetting flips (airbnb009 up, the known stochastic survivor; f1006-hard down) net to zero. That reads as single-trial variance on two borderline cells rather than a gate-strip leak, but the per-cell `Got N` / committed-SQL deep-dive (the analyze deliverable, reserved per the dispatch) is what adjudicates variance-vs-contamination. The full `would_abstain` distribution across all 48 is likewise the analyze deliverable, not done here.

## Stage Report: analyze

- DONE: THE CONTAMINATION ADJUDICATION — both net-0 flips are single-trial solver-reasoning VARIANCE, not a gate-strip leak.
  Read the committed model SQL from the `apply_patch` `payload.input` in the session transcript for both flipped cells in both runs. airbnb009 (FAIL→PASS): full committed a minimal `WHERE … IN (DISTINCT)` → `WHERE … BETWEEN MIN AND MAX` fix to `mom_agg_reviews.sql` (correct); baseline committed a large over-engineered rewrite (bounds_cte + sentiments CROSS JOIN + NULLIF) that broke. f1006-hard (PASS→FAIL): baseline committed ONE correct `sum`→`max` patch; full committed that SAME patch PLUS a second over-refinement (`row_number()` season-rank + `WHERE rank=1`, GROUP BY dropped) that broke its own fix. Triage record carries NO SQL on either; zero triage→SQL coupling; 46/48 cells byte-held @baseline; strict audit tainted:0. The observe-only contract held on all 48. (`rk runs diff` not used — TypeErrors on ade-bench dirs; paired delta from per_trial_outcomes.json, slug-paired, 10k bootstrap: mean +0.0, 95% CI [−0.0625, +0.0625].)
- DONE: THE M3 DELIVERABLE — the all-48 would_abstain map (recovered per-cell from the session transcript, not test -f the run-dir).
  48/48 cells durably emitted a triage record (the /tmp+stdout routing scales — 4th-scale confirmation of smoke). would_abstain TRUE: 0/48. No @baseline passer flagged ⇒ a future enforced rail would predict ZERO false-reverts on this fixed 48. Survivor airbnb009 NOT flagged (instruction=T, raw_source_probe=T ⇒ decidable). Schema-drift confirmed at scale: literal `would_abstain` key on only 38/48; 10/48 use drifted/nested/narrative shapes (an enforced consumer MUST derive abstain from clauses, never parse the field + default-to-abstain). raw_source_probe fired on ~26/48 (vs inert on the smoke 8) but never over-abstained — conservative map, NOT a certified oracle-only detector (h0030/h0036 wall persists).
- DONE: The 5 required questions answered in `## Run result`; verdict + prevention/next-move in `## Verdict`; WORKFLOW-REFINE updated.
  Recommended CONCLUDE (captain decides): instrument succeeded on its own terms (contract held, routing scales, 0/48 would_abstain). @baseline NOT promoted (net 0, {0}-flip by construction). No reflexive follow-up. The two enforced-rail hardening requirements are RETROSPECTIVE de-risk knowledge only — h0040 (the rail this de-risks) already concluded REJECTED-inert; do not re-open the enforced-rail family.

### Summary

Analyze closes the M3 observe-only de-risk line. The decisive adjudication: net 0 vs @baseline is TWO offsetting single-cell flips (airbnb009 up, f1006-hard down), and reading the committed SQL on both proves they are pure single-trial solver-reasoning variance — the observe-only stage altered NO committed SQL on any cell, the contamination tripwire held (tainted:0, 46/48 byte-held). The M3 deliverable: 48/48 cells durably emitted a triage record (routing scales), 0/48 would_abstain, no passer flagged, survivor decidable ⇒ a future enforced rail would predict zero false-reverts on this fixed 48. Two confirmed-at-scale caveats (schema drift on 10/48 → derive abstain from clauses; raw-source probe under-fires → conservative map not a clean detector) are retrospective de-risk knowledge since h0040 is already REJECTED-inert. Recommended verdict CONCLUDE; @baseline NOT promoted; no follow-up filed.
