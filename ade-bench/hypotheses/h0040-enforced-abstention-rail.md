---
id: h0040
title: Enforced abstention rail (Track Z) — a NEW pre-commit triage stage with a fixed three-clause trigger that mechanically emits ABSTAIN and REVERTS edits made only to satisfy an undecidable load-bearing claim, recording triage.json
status: smoke
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

## Run result

## Behavioral analysis

## Verdict

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
