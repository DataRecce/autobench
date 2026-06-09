---
id: h0040
title: Enforced abstention rail (Track Z) — a NEW pre-commit triage stage with a fixed three-clause trigger that mechanically emits ABSTAIN and REVERTS edits made only to satisfy an undecidable load-bearing claim, recording triage.json
status: conclude
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §4 M2 (captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 4. The Track Z / h00Z enforcement primitive h0031 named as missing. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-09T12:19:47Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

**Falsifiable claim (the single README change — a NEW `## Stage:` for the pre-commit triage gate,
between Validation and Finalization; placement is an open §8-Q2 design choice for propose/captain):**
a mechanical abstention precondition — for each load-bearing claim the edit rests on, a fixed
three-clause trigger (instruction names it? existing `schema.yml` contract names it? raw
`SELECT FROM {{ source(...) }}` conservation/coverage probe — count + key-level anti-join, read from
the IMMUTABLE source — decides it?) that, if all three are NO, **mechanically emits ABSTAIN and reverts
every edit made only to satisfy that claim**, leaving those files byte-identical to task start, and
records `triage.json` — will, against the current minimal `@baseline`, abstain correctly on the 16
oracle-blocked failures (byte-identical to baseline → no-op) **without reverting any correct edit
(no passer regresses)**. This is **net-protection**, expected to flip **{0}** by construction (it never
asserts an answer; it withholds a change).

**The single solver-README change.** Add exactly one `## Stage:` header (the pre-commit triage gate).
For each load-bearing claim, a fixed three-clause tree: (1) does an explicit task-instruction sentence
name the deciding quantity? (2) does an *existing* `schema.yml` contract name it? (3) does a raw
`SELECT FROM {{ source(...) }}` conservation/coverage probe — **count + key-level anti-join, read from
the IMMUTABLE source, never a re-derived CTE** (the E0/h0032 caveat) — DECIDE it? If all three are NO,
the gate **mechanically emits ABSTAIN and reverts every edit made only to satisfy that claim**, leaving
those files byte-identical to task start. `triage.json` records the decision + the failing clause as
artifact proof the gate fired. This is single-path (no candidate generation), so it sidesteps the
G9-exhausted arbitration family entirely. **Open §8-Q2 design choice to resolve at propose/captain:** a
NEW `## Stage:` between Validation and Finalization (this entity's default framing) vs a `gate-change`
on the existing Finalization stage — either keeps the single-`## Stage:` G1-clean budget.

**Independent non-oracle signal.** In-/app only: the raw, IMMUTABLE `{{ source(...) }}` relation read
directly (count + key-level anti-join), the task instruction, and the existing `schema.yml`. Clause-3
MUST read the immutable raw source, NEVER a solver-rebuilt intermediate (the E0/h0032 + h0030 caveat) —
a re-derived CTE re-correlates with the model error and the anti-join comes back empty (the textbook
correlated-error false-green). No hidden `AUTO_*` / `solution__*` / `check_option_*` / `tests/AUTO_*` is
named or read.

**Leading indicator (distance, `Got N`).** On the 16 oracle-blocked failures `Got N` should be
**UNCHANGED** (the gate correctly abstains → files byte-identical to baseline → no-op). The
captain-carve-out abstention set (asana004/005/005-hard, ana-eng004, f1002, ana-eng007/-medium) is
already at 0, so abstaining costs nothing. The decisive read is `triage.json` recording ABSTAIN +
failing clause on those cells, AND every passer staying byte-identical to baseline (no wrong revert).

**Kill-path / predicted failure mode.** Two live risks: (1) **G7-high** — an "enforced REVERT" expressed
as README prose sits at the *same model-discretionary altitude* that produced h0031's
`abstained_claims: []` (the arbitrator promoted a tier-3 "defensible local guess" instead of abstaining);
there is no mechanical harness compelling the revert, so the central unproven claim is whether the prose
actually compels it. (2) **Inverted false-green (G10-live)** — the danger is a *wrong revert*: if
clause-3's anti-join reads a solver-rebuilt intermediate (not raw source) it re-correlates (the h0030
hazard in reverse) and could revert a *correct* edit, regressing a passer. Smoke MUST falsify this with
≥2 *perturbable* canaries per construct family. If the gate emits no ABSTAIN on the oracle-only cells
(`abstained_claims: []` like h0031 — the enforcement prose is inert), OR it reverts a correct edit and
regresses a passer (inverted false-green), the rail is REJECTED.

**Dead family it must avoid (proposal §6 map) + how it differs.** It is single-path (one build, no
candidate generation), so it sidesteps the **D4 candidate-generation/arbitration** family entirely
(no N self-scored candidates → escapes G9). It is the enforcement primitive h0031 explicitly named as
the missing piece, NOT a third route. The inverted-false-green danger is the **D7 coverage/value**
hazard in reverse (a wrong revert), which is exactly what the perturbable-canary smoke must falsify.
It must NOT re-derive its probe through a rebuilt CTE (that is the dead **D2 grain-reconcile**
re-correlation; clause-3 reads the immutable raw source only).

**Target datasets.** Net-protection / infrastructure across all 48 — there is no flippable target by
construction. Honest framing: standalone against the current minimal baseline (which does not bleed),
its protective value is unobservable — the harm it guards came from the rejected flip-seeking levers
(h0012, h0017), not from `@baseline`. **M2's real home is bolted onto a future flip-seeking generative
lever, where it would guard a live regression surface.** For smoke, the reads are (a) `triage.json`
records ABSTAIN + failing clause on the oracle-only cells (e.g. `ade-bench-asana004`,
`ade-bench-intercom001`) and (b) zero passer regresses (no wrong revert) across a cross-family canary
panel with ≥2 perturbable canaries per construct family.

**Honest expectation.** **{0}** flips by construction. Carries the live G10 inverted-false-green risk
(a wrong revert) → needs E0-style instrument validation (the clause-3 probe must clear the E0/h0032
two-sided FIRE-on-injected / SILENT-on-known-good discrimination on a fixture that SHARES the target's
upstream filter, per the h0030 refinement) + ≥2 perturbable canaries per construct family. Build and
bank the spec now; the captain decides whether to also run it standalone as a bleed-freeness check.
This is a `trials: 1`, judge-by-artifact entity; it faces its own propose + smoke gate.

**Scope.** Workflow-stage / prompt lever only; benchmark FIXED; no expanded solver access; leak-guard
intact (the stage references only the immutable raw `source()`, the task instruction, and the existing
`schema.yml`, and names no hidden `AUTO_*` / `solution__*` / `check_*` / verifier test, no
`equality test` / `has less columns` / `expected output seed`, no `Got N` or row count, and no
`curl`/`wget`/`git clone`/web/published-solution fetch). The change touches exactly one `## Stage:`
(or one gate-change on Finalization) and leaves the leak-guard prose + the other stages byte-identical.
The full spec differs from `@baseline` only in `experiment:` + `solver_workflow:`; the smoke spec
additionally adds `benchmark.tasks` (the oracle-only ABSTAIN-read cells + a cross-family canary panel
with ≥2 perturbable canaries per construct family — required because a wrong revert is a generative
regression surface).

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0040-enforced-abstention-rail.yaml` shows only
`experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md` adds exactly
one `## Stage:` header (or one gate-change on Finalization), leaves the leak-guard prose (lines ~1–32)
and the other stages byte-identical, and names no hidden `AUTO_*`/`solution__*`/`check_*`/verifier test.
`agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (computed from
`per_trial_outcomes.json`, slug-paired, 10k bootstrap) plus the absolute `stratified_pass_at_1` vs
`@baseline` 0.6458.**
The smoke deep-dive MUST read the committed `triage.json` (the dispatched-ensign `apply_patch` payload)
and confirm: (a) on the oracle-only cells it records ABSTAIN + the failing clause AND those files are
byte-identical to task start (the enforced revert actually fired — NOT h0031's `abstained_claims: []`);
and (b) NO passer regresses (no wrong revert / inverted false-green), verified on ≥2 perturbable
canaries per construct family. Unchanged `Got N` on the oracle-only failures is the SUCCESS condition.
An empty `abstained_claims` on the oracle-only cells (enforcement inert) OR a regressed passer (wrong
revert) = REJECTED.

## Gatekeeper review

**Recommendation: APPROVE** — exactly one new `## Stage:` (a pre-commit enforced-abstention triage gate)
inserted between Validation and Finalization; leak-guard prose (lines 1–32) + the four existing stages
byte-identical; full spec differs only in `experiment:` + `solver_workflow:`; smoke spec adds only
`benchmark.tasks` (13 cells: a 5-cell Panel-A ABSTAIN-fires set + an 8-cell Panel-B wrong-revert panel with
≥2 perturbable canaries on each construct-sharing family); both frozen. No FAILs. Two WARNs (G7 enforcement-
inert-risk; G10 residual wrong-revert risk) are the hypothesis's own named kill-paths and are the decisive
smoke reads, not blockers. Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-08).
Reviewed 2026-06-09T12:30Z.

Fork parent resolved: `source:` says `solver_workflows/codex-ade-dbt-minimal`; `@baseline`
(run `622bdedac572b479`) config `agent.kwargs.solver_workflow = solver_workflows/codex-ade-dbt-minimal` —
agree. G1/G6 diffed against `codex-ade-dbt-minimal`.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff codex-ade-dbt-minimal/README.md → fork` is purely additive (`76a77,176`, 100 lines): one new `## Stage: Pre-commit abstention triage (enforced)`; stage count 4→5; no other stage or guardrail prose touched. |
| G2 leak-guard intact | PASS | Leak-guard prose (lines 1–32) byte-identical (verified `diff` of lines 1–32 = empty). Forbidden-token grep over the 100 added lines (`AUTO_`/`solution__`/`check_*`/`tests/AUTO`/verifier/`equality test`/`expected output seed`/`Got N`/`row count`/`has less columns`/`curl`/`wget`/`git clone`/`git ls-remote`/web) returns CLEAN. The two `git checkout`/`git stash` mentions are LOCAL workspace reverts (the enforcement mechanism), not external fetches — not a leak-guard violation. |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0040-….yaml` shows ONLY `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff` full→smoke adds only the `benchmark.tasks:` block (+ comments); all 13 slugs `ade-bench-` prefixed; the two ABSTAIN-fires targets the `## Hypothesis` names (asana004, intercom001) plus the carve-out cells (ana-eng004, f1002, ana-eng007) are all present. |
| G5 both frozen | PASS | `…frozen.yaml` (1699B) + `…smoke.frozen.yaml` (2008B) both exist; both carry `kind: spacedock_solver` + `runtime: codex` + `trials: 1`; smoke frozen carries all 13 tasks. |
| G6 resolver fidelity | PASS | Inserted text is the enforced form of the h0040/h0041 three-clause trigger (instruction / existing `schema.yml` / raw `{{ source() }}` count + key-level anti-join read from the IMMUTABLE source). It is independent (clause-3 reconciles against the raw source), NOT self-anchored, and NOT a build-to-a-contract mandate — it only REVERTS edits the AND-of-NOTs flags. Matches the Falsifiable claim (a NEW `## Stage:` between Validation and Finalization, mechanical revert on undecidable claims, PINNED `triage.json`). No scope creep. |
| G7 actionability/inert-risk | WARN | The enforcement is expressed as README prose at the same model-discretionary altitude that produced h0031's `abstained_claims:[]` (abstention PERMITTED but not fired) — there is no harness compelling the revert. MITIGATIONS in the prose: (1) abstain is DERIVED mechanically (`abstain = NOT instr AND NOT schema AND NOT raw_probe`), not a free-form field (the h0041/h0038 schema-drift fix — pin hard, never default-to-abstain on a missing clause); (2) the revert is a concrete mechanical op (`git checkout`/re-apply original bytes) with a worked anti-join skeleton, not abstract restructure prose; (3) durable `/tmp/triage.json` + `cat`-to-stdout routing (h0041-validated 8/8, h0038 7/8). Residual inert-risk is the NAMED kill-path: does the prose actually COMPEL the revert (`abstain=true` + byte-identical files on Panel A) or go inert like h0031. Predictive only; does not block. |
| G8 regression-canary coverage | PASS | The stage is GENERATIVE (the triage runs on every task). Smoke Panel B carries ≥1 `@baseline` passer per non-target family — airbnb001 / f1007+f1001 / quickbooks002 — AND the required ≥2 PERTURBABLE canaries on each construct-sharing family the targets touch: ana-eng = ana-eng002 + ana-eng002-medium (both grade `AUTO_obt_product_inventory`, the ana-eng004 target model); asana = asana003 (grades `AUTO_int_asana__project_user`, the asana004 target intermediate) + asana001 (asana entity-grain passer). f1 carries 2 (f1007 + f1001, the non-package convention-bleed tripwire). intercom has zero `@baseline` passers (all 3 fail) so no intercom canary is possible — it appears only as a Panel-A target. Satisfies the h0012 "break a different family member" guard. |
| G9 selector independence | N/A | Single-path: one build, no candidate generation, no N-candidate selector protocol. The stage triages ONE committed build against three fixed clauses — it sidesteps the G9-exhausted arbitration family (h0026/h0031) entirely. |
| G10 self-correcting false-positive | WARN | This IS an act-on-decision lever (it REVERTS) — the rule applies. Against the three FAIL axes it is SAFE: **(a) scope** — the revert is GATED to `abstain==true` (all three clauses false), not run on every edit; a passer whose edit ANY clause supports is never touched. **(b) independence source** — clause-3 reads the IMMUTABLE raw `{{ source(...) }}` with a key-level anti-join, hard-forbidding a re-derived CTE / rebuilt relation (the h0030/E0 `correlated_error_trap` hazard that would re-correlate and wrong-revert). **(c) check-don't-replace** — the action is a REVERT to byte-identical task-start, NOT replacement with a "structurally different" path (the conservative removal, not h0012's substitute-a-guess). No FAIL axis triggers → not REJECT/REVISE. The WARN: h0041 found clause-3 (the only INDEPENDENT clause) decided NOTHING on 8/8, so `abstain` rests on the non-independent instruction/schema clauses, AND a wrong revert on a re-correlated false read or an over-fired AND-of-NOTs would regress a passer (the inverted false-green, G10-live). This is the DECISIVE Panel-B smoke read: ANY regressed passer = NO-GO. |
| G11 multi-model-target risk | N/A | h0040 credits NO flip by construction (expected {0}; it withholds a change, never asserts an answer). G11 governs crediting a single-model lever with a target FLIP; with zero flips claimed, the multi-model variance trap cannot apply. (For the record, the Panel-A targets are single-model: asana004→`AUTO_int_asana__project_user_agg_equality`, intercom001→`AUTO_intercom__threads_equality`, ana-eng004→`AUTO_obt_product_inventory_equality`, f1002→`AUTO_most_podiums_equality`, ana-eng007→`AUTO_dim_products_equality`.) |

**For the captain:** APPROVE-class — no integrity FAIL. This is the highest-regression-risk R2 hypothesis because it is the ONLY lever that ACTS (it reverts edits). Two decisive smoke reads, both the hypothesis's own named kill-paths: (1) **G7 enforcement-fires** — on Panel A (asana004 / intercom001 + the carve-outs) `triage.json` must record `abstain=true` + the failing clause AND the edited files must be byte-identical to task start (proof the REVERT fired, NOT h0031's inert `abstained_claims:[]`, NOT a pattern-matched REJECT like h0038's asana004 false-reject); (2) **G10 wrong-revert** — ZERO passer on Panel B may regress (the ≥2 perturbable ana-eng/asana doublets are the load-bearing tripwires; a wrong revert on a re-correlated read or an over-fired AND-of-NOTs is the inverted false-green). HONEST FRAMING (already in the entity): {0} flips by construction; standalone against the current minimal `@baseline` (which does NOT bleed) its protective value is UNOBSERVABLE — its real home is bolted onto a future flip-seeking generative lever. So this smoke is a BLEED-FREENESS + enforcement-fires check, and the captain decides whether to run it standalone or bank the spec for that future pairing.

## Smoke result

**Focused score (attested clean).** Run `runs/ade-bench-h0040-enforced-abstention-rail/41c556510ff753a7`,
13 cells, `trials: 1`. `rk audit --policy strict` = **clean (tainted 0/13, all `taint_status: clean`)**;
`captured > 0` on all 13 (`subagent-trace-manifest.json` = 1 each) — verified BEFORE the score is trusted.
`rk score`: **`stratified_pass_at_1 = 0.6154` (8/13)**, `n_completed=13`, `n_errored=0`, verdict `above` the
0.1875 paper baseline. This equals the by-construction expectation exactly: the 8 Panel-B passers all stay
1.0, the 5 Panel-A oracle-only failers all stay 0.0 → **net flips vs @baseline = 0**. (`@baseline`
`622bdedac572b479`: Panel A all 0.0, Panel B all 1.0; slug-paired delta is 0 on every cell, so no
bootstrap is needed.)

## Run result

| cell | role | base | now | Δ | triage abstain / reverted_files | read |
|------|------|------|-----|---|---------------------------------|------|
| asana004 | A | 0.0 | 0.0 | 0 | 4 claims, **all abstain=false**, reverted [] (instr=true on all) | inert |
| intercom001 | A | 0.0 | 0.0 | 0 | 6 claims, **all abstain=false**, reverted [] (instr=true; raw=true 4/6) | inert |
| ana-eng004 | A | 0.0 | 0.0 | 0 | 3 claims, **all abstain=false**, reverted [] (instr=true; raw=true 2/3) | inert |
| f1002 | A | 0.0 | 0.0 | 0 | 5 claims, **all abstain=false**, reverted [] (instr=true AND schema=true) | inert |
| ana-eng007 | A | 0.0 | 0.0 | 0 | 4 claims, **all abstain=false**, reverted [] (1 claim raw=true alone) | inert |
| ana-eng002 | B | 1.0 | 1.0 | 0 | `{"claims":[]}` ("pure syntax fix"), no revert | HELD |
| ana-eng002-medium | B | 1.0 | 1.0 | 0 | reverted [] | HELD |
| asana003 | B | 1.0 | 1.0 | 0 | reverted [] | HELD |
| asana001 | B | 1.0 | 1.0 | 0 | reverted [] | HELD |
| airbnb001 | B | 1.0 | 1.0 | 0 | reverted [] | HELD |
| f1007 | B | 1.0 | 1.0 | 0 | reverted [] | HELD |
| f1001 | B | 1.0 | 1.0 | 0 | reverted [] | HELD |
| quickbooks002 | B | 1.0 | 1.0 | 0 | reverted [] | HELD |

**triage.json route.** The record is written by the spawned **ensign sub-agent** and `cat`-ed to stdout,
landing in `<cell>/agent/sessions/**/rollout-*.jsonl` (the orchestrator `codex.txt` carries the prose
summary). Reads taken from the transcript, NOT `test -f` the run-dir (the `/tmp` scratch is torn down — the
h0039 trap). All `reverted_files` non-empty matches across the panel were the prompt-template echo
(`"reverted_files":["..."]`); the real records are empty on every cell.

## Behavioral analysis

**(A) G7 enforcement — INERT on all 5 Panel-A oracle-only cells (the named kill-path fired).** Every
Panel-A cell emitted a *fully populated, well-formed* `triage.json` (3-6 explicit claims, `abstain` derived),
but the derived `abstain` came out **`false` on every single claim → zero `reverted_files`**. So the revert
**never fired** on the cells where it was supposed to. This is NOT h0031's empty `abstained_claims:[]`
(permission-not-fired); it is a fully-instantiated AND-of-NOTs that evaluates to NO-abstain because the
solver **self-credits the trigger clauses**: clause-1 (instruction) reads `true` wherever the task names a
column/grain/target at the surface (asana004 4/4; f1002 5/5 instr=true and schema=true via the existing
`__stats.yml`), and clause-3 (raw_source_probe) reads `true` claiming the raw probe "decides" the claim
(intercom001 4/6, ana-eng004 2/3, ana-eng007 one claim on raw alone). These cells are oracle-blocked on
**aggregation semantics / value mapping**, not on whether a column is *named* — and clause-1 conflates
surface naming with "names the deciding quantity," so abstain ≈ never.

**(B) G10 wrong-revert — PASS (decisive safety read).** All 8 Panel-B passers held reward 1.0 with zero
real reverts; **zero passer regressed**, including the 4 perturbable canaries (ana-eng002 + ana-eng002-medium
on `AUTO_obt_product_inventory`; asana003 on the asana004 target intermediate `AUTO_int_asana__project_user`;
plus the f1007/f1001 convention-bleed tripwires). The `abstain==true`-gated revert scoping held trivially:
nothing was ever reverted, so the inverted-false-green could not arise.

**Schema drift (4th routing test after h0041/h0038/h0037).** The durable stdout/session-transcript ROUTING
worked on all 13 (the h0041 fix holds), but the PINNED record SHAPE did NOT hold uniformly: asana004 used the
pinned nested `clause_results:{...}` + `reverted_files`; intercom001 FLATTENED to
`{formula, claims:[{name, instruction, schema_yml, raw_source_probe, abstain}]}` (no `reverted_files`); 
ana-eng002 emitted `{"claims":[]}`. A pinned shape in prose is not reliably honored by gpt-5.5@xhigh even with
an explicit "derived, not free-form" instruction — downstream readers must be schema-tolerant.

## Verdict

**REJECTED-inert — knowledge gain. Terminal; no follow-up filed.** The decisive G7 read fails: the enforced
revert **NEVER FIRED**. On all 5 oracle-only Panel-A cells (asana004, intercom001, ana-eng004, f1002,
ana-eng007) `abstain=false` on every claim → zero `reverted_files`, reward unchanged at 0.0 — the gate is
inert on exactly the cells it was designed for. The cause is precise: the solver **self-credits clause-1
(instruction-names-it)** as `true` wherever the task surface-names a column/grain/target (asana004 4/4;
f1002 5/5 instr + schema via `__stats.yml`) and **self-credits clause-3 (raw-probe-decided-it)** as `true`
(intercom001 4/6, ana-eng004 2/3, ana-eng007 1 claim on raw alone), so the mechanical `abstain = NOT instr
AND NOT schema AND NOT raw` is never all-true. This is **NOT h0031's empty `abstained_claims:[]`**
(permission-not-fired) — it is a fully-instantiated AND-of-NOTs that evaluates to NO-abstain because the
clause EVALUATION is itself model-discretionary and self-credited. **It is h0031's discretionary wall in a
NEW place:** not permitted-vs-enforced, but the trigger booleans the enforcement derives from are themselves
discretionary self-reads, so deriving `abstain` mechanically buys nothing when its inputs are not
independent.

**The revert primitive is BLEED-FREE (the banked result).** The G10 read is clean: all **8/8 Panel-B passers
held reward 1.0 with zero wrong reverts**, including the **4 perturbable canaries** (ana-eng002 +
ana-eng002-medium on `AUTO_obt_product_inventory`; asana003 on the asana004 target intermediate
`AUTO_int_asana__project_user`; plus the f1007/f1001 convention-bleed tripwires) — zero passer regressed. The
`abstain==true`-gated revert scoping held trivially (nothing was ever reverted). **Audit clean 13/13**
(strict, `tainted 0/13`), captured>0 on all 13, `stratified_pass_at_1 = 0.6154` (8/13), net flips vs
@baseline = **0 by construction**. **@baseline is UNCHANGED at runs/ade-bench-baseline/622bdedac572b479
(31/48); NOTHING promoted.**

**Learning for M2 as an enforcement primitive:** an "enforced revert" written as README prose is structurally
inert against an oracle gap the same way the read-only checking levers are, because the AND-of-NOTs is only
as independent as its clauses — and clause-1/clause-3 are solver-self-graded. For the revert to fire
usefully, at least one clause must be evaluated by something the solver cannot talk itself out of
(independent redundancy — the standing `verification-without-oracle` requirement). **Disposition:** the
bleed-free spec is **BANKED**; do NOT re-run standalone on the minimal @baseline (its protective value is
unobservable there — the minimal baseline does not bleed, so there is nothing to guard or to wrong-revert).
M2's only real test is bolted onto a future flip-seeking generative lever that actually bleeds — there it
would either guard a live regression (value) or wrong-revert (inverted false-green); the minimal baseline can
show neither. Full structural learning + the 4th schema-drift observation recorded in
`_artifacts/WORKFLOW-REFINE.md`.

**Program-level close.** h0040 is the LAST of the Round-2 workflow-stage set (h0037–h0041); all five ran
through smoke with **0 flips**. The oracle/discretionary wall held across every R2 lens — reference-mining
(h0037), plan-review/Method-B (h0038), observe-only (h0039 routing-dead / h0041 routing-fixed), and the
enforced rail (h0040). The durable yield is method/safety knowledge: the stdout/session-transcript routing
fix (h0041, held 4× through h0040), the pinned-schema necessity (4th schema-drift sighting here), the
anti-bleed proof (h0040 G10, h0037 own-sibling gate), and this enforcement-inert finding. No 6th hypothesis
is reflexively filed — the next-direction strategy decision is escalated to the captain.

## Stage Report: propose

- DONE: README change = EXACTLY ONE new `## Stage:` (pre-commit triage gate between Validation and Finalization)
  `diff codex-ade-dbt-minimal/README.md → fork` is purely additive (`76a77,176`, 100 lines): one new
  `## Stage: Pre-commit abstention triage (enforced)` placed between Validation and Finalization (the dispatch
  default; noted for the captain). Fixed three-clause trigger (instruction / existing `schema.yml` / raw
  `SELECT FROM {{ source(...) }}` count + key-level anti-join read from the IMMUTABLE source); all-three-NO →
  mechanical ABSTAIN + revert of edits made only to satisfy that claim → byte-identical to task start; records
  `triage.json`. Leak-guard prose (lines 1–32) + the four existing stages byte-identical; forbidden-token grep
  over added lines CLEAN; names no hidden `AUTO_*`/`solution__*`/`check_*`/verifier test, no `Got N`/row count/
  equality test/has less columns, no `curl`/`wget`/`git clone`/web fetch (AC-1). `git checkout`/`git stash` are
  LOCAL reverts (the enforcement op), not external fetches.
- DONE: PINNED SCHEMA + DURABLE ROUTING (the cross-hypothesis lessons)
  `triage.json` schema PINNED HARD: `abstain` is DERIVED mechanically (`abstain = NOT instruction AND NOT
  schema_yml AND NOT raw_source_probe`), NOT read from a free-form/optional field; each clause must be set
  explicitly and a missing clause is invalid — NEVER default-to-abstain on a missing field (fixes the h0041/
  h0038 3x schema-drift). Routed UNCONDITIONALLY to `/tmp/triage.json` + `cat`-to-stdout (the h0041-validated
  8/8 durable path, h0038 7/8), NOT the dead `/razorback-freeze` single-child precondition. Clause-3 reads the
  IMMUTABLE raw `source()` only with a key-level anti-join, hard-forbidding a re-derived CTE (the E0/h0032
  `correlated_error_trap` + h0030 re-correlation → wrong-revert hazard).
- DONE: Smoke spec `benchmark.tasks` — TWO required reads (ABSTAIN-fires + G10 wrong-revert panel)
  13 cells. Panel A (oracle-only @baseline FAILERS, want abstain=true + byte-identical revert):
  asana004 (the cell h0038 false-rejected), intercom001, ana-eng004, f1002, ana-eng007. Panel B (G10
  wrong-revert, want ZERO passer regress): ≥2 PERTURBABLE per construct-sharing family — ana-eng002 +
  ana-eng002-medium (both grade `AUTO_obt_product_inventory`, the ana-eng004 target model), asana003 (grades
  `AUTO_int_asana__project_user`, the asana004 target intermediate) + asana001; plus ≥1 passer per other
  family — airbnb001, f1007 + f1001 (f1 convention-bleed tripwire), quickbooks002. intercom has zero
  `@baseline` passers so no intercom canary is possible (it appears only as a Panel-A target). Full spec
  differs from baseline ONLY in `experiment:` + `solver_workflow:` (diff verified); smoke differs from full
  ONLY by the `benchmark.tasks` block; both frozen via `rk freeze --allow-missing`; `kind`/`runtime`/`trials:1`
  preserved. Gatekeeper ran (inline): per-rule table + APPROVE recorded in `## Gatekeeper review`.

### Summary

Forked `codex-ade-dbt-minimal` → `h0040-enforced-abstention-rail` and added exactly one new `## Stage:
Pre-commit abstention triage (enforced)` between Validation and Finalization — the enforcement primitive
h0031 named as missing (h0031 died with `abstained_claims:[]` because abstention was PERMITTED, not
ENFORCED). The decisive design choices absorb the sibling findings: abstain is DERIVED from the three boolean
clauses by a hard AND-of-NOTs rule (never a free-form field, never default-to-abstain on a missing clause —
the h0041/h0038 schema-drift fix); the revert is a concrete mechanical op gated to `abstain==true` only (so a
passer whose edit any clause supports is never touched — the G10 wrong-revert defense); clause-3 reads the
IMMUTABLE raw `source()` with a key-level anti-join, hard-forbidding a re-derived CTE (the h0030/E0 re-
correlation hazard); routing reuses the h0041-validated unconditional `/tmp` + stdout path. Gatekeeper:
APPROVE, no FAILs; two by-design WARNs (G7 enforcement-inert-risk like h0031, G10 residual wrong-revert) are
the two decisive smoke reads, NOT blockers. HONEST FRAMING: {0} flips by construction; standalone against the
non-bleeding minimal `@baseline` its protective value is unobservable — its real home is bolted onto a future
flip-seeking generative lever. So this smoke is a BLEED-FREENESS + enforcement-fires check. Propose stops at
the gate; no `rk run` launched.

## Stage Report: smoke

- DONE: Smoke run on `specs/h0040-enforced-abstention-rail.smoke.frozen.yaml` completed (launched DETACHED via nohup, polled across turns). Strict audit clean + captured>0 on every cell BEFORE the score; focused score + clean-audit attestation in `## Smoke result`.
  Run `runs/.../41c556510ff753a7`, 13/13 cells, `trials:1`. `rk audit --policy strict` clean (tainted 0/13, all `taint_status: clean`); `captured>0` on all 13. `rk score`: `stratified_pass_at_1 = 0.6154` (8/13), `n_errored=0`, verdict `above` 0.1875. Net flips vs @baseline = 0 (slug-paired Δ = 0 every cell).
- DONE: The TWO decisive reads — (A) G7 enforcement-fires (read triage.json from the session transcript, not test -f the run-dir) and (B) G10 no-wrong-revert.
  (A) **INERT, not fired** — on all 5 Panel-A oracle-only cells (asana004, intercom001, ana-eng004, f1002, ana-eng007) triage.json is well-formed and populated but `abstain=false` on EVERY claim → ZERO `reverted_files`, reward stays 0.0. NOT h0031's empty `abstained_claims:[]`; the AND-of-NOTs evaluates to NO-abstain because clause-1 (instruction) and clause-3 (raw_source_probe) are self-credited `true`. (B) **NO WRONG REVERT** — all 8 Panel-B passers held reward 1.0, zero real reverts, zero regression (incl. the 4 perturbable canaries). triage.json read from `agent/sessions/**/rollout-*.jsonl` (cat-to-stdout route; the run-dir `/tmp` scratch is torn down — h0039 trap avoided).
- DONE: Workflow-refinement evaluation (new-stage structural lever) + `_artifacts/WORKFLOW-REFINE.md` entry.
  Did NOT fire on the oracle cells (G7 inert, like h0031 via a different route); did NOT wrong-revert any passer (G10 clean). Pinned-schema + derived-abstain held the ROUTING (4th test after h0041/h0038/h0037) but the record SHAPE drifted (asana004 pinned-nested / intercom001 flattened / ana-eng002 empty-claims). Ledger entry appended: "Enforced abstention rail (Track Z / M2): the REVERT never fires …" — M2 is provably bleed-free but unobservable standalone; its only real test is bolted onto a future flip-seeking generative lever that bleeds. Don't re-run standalone on the minimal baseline.

### Summary

M2 / Track Z enforced abstention rail smoke is a clean **REJECTED-inert**. The decisive G7 read fails the
way the kill-path named: the enforced revert never fired on any of the 5 oracle-only Panel-A cells — each
produced a fully-instantiated `triage.json`, but the AND-of-NOTs computed `abstain=false` on every claim
(clause-1 instruction and clause-3 raw-source-probe self-credited `true`), so zero `reverted_files`. This is
the h0031 wall reached through self-graded trigger clauses rather than an empty abstention list. The G10
safety read is clean — all 8 Panel-B passers held 1.0 with zero wrong reverts (incl. 4 perturbable canaries),
strict-audit clean, captured>0 on all 13, net flips 0 by construction (`stratified_pass_at_1 0.6154`). So M2
is provably bleed-free but its protective value is unobservable on the non-bleeding minimal @baseline — its
real home is bolted onto a future flip-seeking generative lever. Bank the spec; do not re-run standalone.
Routing reused from h0041 worked on all 13; the pinned record shape drifted (4th schema-drift instance).

## Stage Report: conclude

- DONE: Write the terminal `## Verdict`: REJECTED-inert — knowledge gain.
  States plainly the enforced revert NEVER FIRED — `abstain=false` on all 5 oracle-only cells because the
  solver self-credits clause-1 (instruction-names-it) and clause-3 (raw-probe-decided-it) as true, so the
  AND-of-NOTs is never all-true; h0031's discretionary wall in a NEW place (clause EVALUATION is itself
  model-discretionary + self-credited, not permitted-vs-enforced). Revert primitive BLEED-FREE (G10 clean:
  8/8 passers held, 0 wrong reverts incl. 4 perturbable canaries). Audit clean 13/13, score 0.6154 (net 0).
  @baseline UNCHANGED 31/48 (NOT promoted). Bleed-free spec BANKED for a future flip-seeking pairing.
- DONE: Finalize the `_artifacts/WORKFLOW-REFINE.md` h0040 entry to a FINAL state (h0040 IS a NEW-STAGE structural lever — mandatory).
  Added the leading `**Status:** rejected-as-written` line (enforcement inert via self-credited clauses;
  revert primitive bleed-free + bankable). Sharpened the Learning line (an enforced-abstain trigger as
  README prose cannot compel abstention because the clause evaluation is model-discretionary and the solver
  self-credits a clause true → same discretionary wall as h0031, NEW mechanism). Bears-on now records: the
  bleed-free revert primitive is reusable for a future flip-seeking-lever pairing; 4th schema-drift sighting
  → pinned-schema necessity reconfirmed; routing held a 4th time; the program-level close.
- DONE: Confirm @baseline NOT promoted (registry untouched) + NO new follow-up hypothesis filed + record the PROGRAM-LEVEL close.
  @baseline run-dir `runs/ade-bench-baseline/622bdedac572b479` (31/48) intact; baseline specs untouched (my
  only diffs are this entity file + WORKFLOW-REFINE.md). Highest active hypothesis is h0041 — no h0042
  exists. Program-level close recorded in both the `## Verdict` and the ledger Bears-on: h0040 is the LAST
  of the R2 workflow-stage set (h0037–h0041); all five smoked with 0 flips; the oracle/discretionary wall
  held across reference-mining / plan-review-Method-B / observe-only / enforced-rail; durable yield is
  method/safety knowledge (routing fix, schema-drift, anti-bleed proof, enforcement-inert finding). No 6th
  filed; next-direction decision escalated to the captain.

### Summary

Terminal conclude for h0040 (captain-decided REJECTED). Wrote the terminal `## Verdict` (REJECTED-inert —
knowledge gain): the enforced revert never fired because the AND-of-NOTs trigger booleans are themselves
model-discretionary and self-credited true (clause-1 instruction + clause-3 raw-probe) — h0031's
discretionary wall via a new mechanism — while the revert primitive is provably bleed-free (G10 clean, 8/8
passers incl. 4 perturbable canaries) and is BANKED for a future flip-seeking pairing. @baseline unchanged at
31/48; nothing promoted; no follow-up filed. Finalized the mandatory WORKFLOW-REFINE.md new-stage entry to a
FINAL `rejected-as-written` state with sharpened Learning + Bears-on (4th schema-drift / pinned-schema
reconfirmed; routing held 4×; program-level close). h0040 is the last of the R2 set h0037–h0041 — all five
0-flip; the next-direction strategy decision is escalated to the captain. Pure documentation finalization; no
`rk` command re-run; the FO sets verdict frontmatter + archives after this report.
