---
id: h0040
title: Enforced abstention rail (Track Z) — a NEW pre-commit triage stage with a fixed three-clause trigger that mechanically emits ABSTAIN and REVERTS edits made only to satisfy an undecidable load-bearing claim, recording triage.json
status: hypothesis
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §4 M2 (captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 4. The Track Z / h00Z enforcement primitive h0031 named as missing. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started:
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

## Smoke result

## Run result

## Behavioral analysis

## Verdict
