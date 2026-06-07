---
id: h0031
title: Dual Output Contract Arbitration -- generate two independent contracts, then select/abstain by visible evidence before implementation
status: smoke
kind: hypothesis
source: captain synthesis after _artifacts/arbitration-without-oracle.md and WORKFLOW-REFINE findings: Output Contract is useful as an observability surface (h0017) but not sufficient for correctness; h0026 proved self-anchored candidate scoring fails without independent judgment. This hypothesis tests the next protocol-family step: two independent contract routes plus an evidence-hierarchy arbitrator that can SELECT, REJECT_BOTH, or ABSTAIN before any SQL is authored.
started: 2026-06-07T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The Output Contract stage gave useful visibility into the solver's mental model: h0017 showed the
contract can reach the committed artifact and reveal the exact wrong assumption (child-driven grain).
But h0017 and h0023 also showed that a single contract author is not enough. The contract can be
wrong, under-scoped, or unsafe, and then Implementation builds to the wrong contract. h0026 showed
the same wall in selector form: multiple candidates are worthless if selection is anchored to each
candidate's own checks.

This hypothesis tests a resolver protocol that separates three jobs:

1. **Evidence snapshot** -- collect visible, local evidence without deciding the answer.
2. **Independent contract generation** -- two isolated routes write Output Contracts from the same
   evidence snapshot, without seeing each other's contract.
3. **Evidence arbitration** -- a separate arbitrator compares contract claims against a pre-declared
   evidence hierarchy and either selects a contract, merges non-conflicting claims, rejects both, or
   abstains when the visible workspace cannot distinguish them.

The key claim is not "two contracts will magically find the oracle." The key claim is that two
contracts expose disagreement, and an evidence-based arbitrator prevents the workflow from selecting
a plausible but unsupported contract. If visible evidence cannot decide, the correct result is
`ABSTAIN`, not a forced choice.

**Falsifiable claim:** for each smoke task, run two independent Output Contract routes (`A` and
`B`) before any SQL change. Each route must produce a contract with deliverables, grain/key source,
declared columns, local types, metric logic, assumptions, and evidence references. Then run an
arbitrator that compares the two contracts claim-by-claim using this hierarchy:

1. explicit task instruction;
2. `schema.yml` / declared local contract;
3. raw source data and conservation relations;
4. project-local tests / dbt constraints;
5. same-project sibling model patterns;
6. installed package artifacts only when the task/project clearly uses that package shape;
7. candidate transcript / plan / self-written contract (debug only, never a tie-breaker).

The arbitrator writes `arbitration.json` with one of:

- `SELECT_A` / `SELECT_B` -- one contract is supported by higher-authority visible evidence and the
  other violates it;
- `MERGE_NON_CONFLICTING` -- contracts disagree only on separable claims and each selected claim has
  visible support;
- `REJECT_BOTH` -- both contracts violate hard local evidence;
- `ABSTAIN` -- the visible workspace cannot decide the disagreement.

Implementation may proceed only from the selected or merged contract. If the arbitrator abstains on a
load-bearing claim, the run must record the unresolved claim and avoid presenting the final answer as
locally verified.

The hypothesis passes smoke if the protocol both (a) proves real independence/arbitration artifacts
exist and (b) flips or strictly improves at least one locally arbitrable target without regressing any
canary. It is falsified if the two routes converge on the same unsupported premise, if the arbitrator
chooses by narrative plausibility or transcript claims, if `arbitration.json` is missing, if it forces
a choice on an oracle-only disagreement, or if selected-contract implementation regresses canaries.

## Protocol-family declaration

This is a **protocol-family change**, not a solver-README-only hypothesis. It changes the resolver
workflow shape by adding two contract-generation routes and a pre-Implementation arbitrator. Results
must be labeled as "dual-output-contract arbitration" and kept separate from README-only
independent-variable runs.

This hypothesis should not be sold as "better instructions." The test is whether the resolver creates
auditable independent contracts and applies visible-evidence arbitration before Implementation.

## Target datasets

The first smoke should cover three locally arbitrable disagreement types, not the full benchmark:

- `ade-bench-ana-eng004` -- width/missing-columns representative. Contracts should name the expected
  column set; arbitration should use declared schema/instruction evidence and abstain if the expected
  width is oracle-only.
- `ade-bench-intercom001` -- grain/missing-parent-rows representative with a cleaner local parent
  signal than the underdetermined asana intermediate convention. Contracts should name the parent/key
  source; arbitration should use raw parent `COUNT(DISTINCT key)` and local sibling patterns.
- `ade-bench-f1011` -- answer-style representative. Contracts should produce option-level local
  checks; arbitration should prefer disconfirming evidence for included options and reject
  self-anchored completeness scoring.

Because this protocol can affect broad task behavior, the smoke carries a regression panel of
currently-passing `@baseline` canaries:

- `ade-bench-airbnb001`
- `ade-bench-ana-eng001`
- `ade-bench-asana001`
- `ade-bench-f1007`
- `ade-bench-quickbooks002`
- `ade-bench-f1001` as the non-package convention-bleed tripwire

No intercom canary is possible if the current `@baseline` still has zero passing intercom tasks.

## Acceptance criteria

**AC-1 -- Real contract independence.** For every target cell, route A and route B must be generated
in isolated sessions/workspaces or under forced-divergence stances. Route B must not read route A's
contract. The run artifact records both contracts and the isolation method.

**AC-2 -- Contracts are evidence-bearing, not narrative.** Each contract claim cites a visible local
evidence source: task instruction, schema, source query, local test, sibling model, or qualified
package artifact. Claims with no visible support must be marked as assumptions, not facts.

**AC-3 -- Arbitration is evidence-based and machine-readable.** The run saves `arbitration.json`
containing the decision, selected/rejected/unresolved claims, evidence authority for each selected
claim, and every abstention. Candidate transcript quality is never a tie-breaker.

**AC-4 -- Abstention is honored.** If the arbitrator marks a load-bearing claim `ABSTAIN`, the
workflow must not pretend the selected artifact is locally verified. An abstained target can still be
useful diagnostic evidence, but it does not count as a controllable +1 candidate.

**AC-5 -- Implementation follows the arbitrated contract.** The final SQL/files must satisfy the
selected or merged contract. If final artifacts diverge from the selected contract, the hypothesis is
NO-GO even if dbt builds.

**AC-6 -- Every recorded score is paired with a clean strict audit.** `rk audit --policy strict`
must report `tainted: 0`, and each cell must have captured solver artifacts.

**Smoke gate:** require all three protocol artifacts (`contract_a`, `contract_b`,
`arbitration.json`) on every target. The smoke is GO only if at least one target flips or strictly
improves by artifact-level distance, zero canaries regress, and the improvement is attributable to an
arbitrated claim rather than transcript plausibility. A canary dropping FAIL is NO-GO regardless of
target movement.

## Gatekeeper review

**Recommendation: APPROVE** — generative protocol-family change; full spec differs in exactly the two allowed fields, leak-guard byte-identical, one new stage added, and the smoke panel carries the G8/G10 perturbable-canary doubling (f1, ana-eng, asana each have 2 perturbable canaries). No FAILs. Two WARNs (G7 inert-risk, G9 forced-divergence unverifiable from artifacts alone) are advisory and do not block.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07. Fork parent resolved: `solver_workflows/codex-ade-dbt-minimal` (source: field implies the seed; `@baseline`=runs/ade-bench-baseline/622bdedac572b479 config names `codex-ade-dbt-minimal` — agree).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs parent adds exactly ONE `## Stage:` (Dual Output Contract Arbitration) between Exploration and Implementation; the other three stage bodies are byte-identical (only line offsets shift). |
| G2 leak-guard intact | PASS | Lines 1–48 (preamble + leak-guard + Exploration) byte-identical to parent; no forbidden token (`AUTO_`/`solution__`/`check_option_`/"expected output seed") in added text — the 3 "verifier" hits are all in the unchanged baseline package-guard prose (lines 16/22/26). |
| G3 spec two fields | PASS | `diff baseline.yaml h0031…yaml` = only `experiment:` + `solver_workflow:`; `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0031…yaml h0031…smoke.yaml` = only an added `benchmark.tasks:` block; all 3 targets (ana-eng004, intercom001, f1011) present and `ade-bench-` prefixed; no bare slugs; 11 real task IDs. |
| G5 both frozen | PASS | `…frozen.yaml` (1715B) and `…smoke.frozen.yaml` (1969B) both written by `rk freeze`; both carry `kind: spacedock_solver` + `runtime: codex`; smoke frozen has 11 tasks. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: shared evidence snapshot → two independent contracts (A + forced-divergence B that must not read A) → evidence-hierarchy arbitrator writing `arbitration.json` with exactly one of SELECT_A/SELECT_B/MERGE_NON_CONFLICTING/REJECT_BOTH/ABSTAIN before any SQL. Generative/independent, not the dead self-anchored "re-run your own model" family; abstention honored. |
| G7 actionability/inert-risk | WARN | Abstract-structural: it asks the solver to *produce process artifacts* (two contracts + `arbitration.json`) and run a multi-phase protocol inside one session. It carries worked `arbitration.json` skeletons (good), but the core is a process to execute, not a one-line mechanical substitution — inert-risk that the solver narrates the protocol without materially changing committed SQL (the h0010/h0017/h0023 "talks but doesn't do" wall). Predictive only; does not block. |
| G8 regression-canary coverage | PASS | Generative (fires on every author/restructure + answer-style task). Panel: airbnb001 / ana-eng001 / asana001 / f1007 / quickbooks002 / f1001 = ≥1 `@baseline` passer per non-target family (intercom has zero passers → N/A, covered by the asana grain doublet). Perturbable doubling on construct-sharing families: f1 = f1007 + f1001 (both author `AUTO_stg_f1_dataset__results`); ana-eng = ana-eng001 + ana-eng002 (ana-eng002 grades the SAME `AUTO_obt_product_inventory` model as target ana-eng004); asana = asana001 + asana003 (asana003 grades the SAME `AUTO_int_asana__project_user` intermediate as the entity-grain target family). Satisfies the h0012 "break a different family member" guard. |
| G9 selector independence | WARN | Multi-candidate/selector family (two contract routes + arbitrator). Axis (a) generation independence: substrate is one solver session per task (`trials: 1`), so route B is simulated in-session — the README supplies the allowed mitigation (**forced-divergence** stance: B must take the opposite plausible reading and try to defeat A's claims), but whether B genuinely diverges cannot be verified from README + specs alone. Axis (b) judgment independence: the arbitrator scores against an **external evidence hierarchy** (instruction > schema > raw source/conservation > local tests > sibling > package) and **explicitly forbids candidate self-scoring / transcript plausibility as a tie-breaker** — a real external criterion, not h0026's self-anchored scorer. Both axes are addressed in prose; WARN (not FAIL) because the divergence/external-criterion is claimed but not harness-enforced. |
| G10 self-correcting false-positive | PASS | Not the ungated "fix-your-own-number-on-disagreement / re-derive" lever h0012 was. (a) It acts on disagreement *before* Implementation, not as a generative post-hoc self-correction of an already-correct answer. (b) Its reconcile authorities are separately-sourced (raw parent `COUNT(DISTINCT key)`, declared `schema.yml`, instruction) — not a CTE re-deriving the model's own logic. (c) `ABSTAIN`/`REJECT_BOTH` are first-class outcomes and the guards forbid replacing a project's existing structure / padding columns / marking an option IN without support — it investigates, it does not mandate "use a different path." The generative scope is the only watch-item and is already carried under G7/G9. |

**For the captain:** No integrity FAIL — safe to advance to `smoke`. Watch two things at smoke: (1) **G7 inert-risk** — confirm the protocol actually reaches the committed artifact (real `contract_a`/`contract_b`/`arbitration.json` per target, not just transcript narration); a target with identical distance-to-pass vs `@baseline` means the lever did nothing there. (2) **G9 forced-divergence in-session** — the single-session substrate is the same wall h0026 hit; the smoke gate (entity AC-1) must verify route B genuinely disagreed with route A on real claims, otherwise the two "independent" contracts are one mind photocopied and arbitration is theatre. The perturbable doublets (ana-eng002, asana003) are the load-bearing regression tripwires — a drop there, not just on the single per-family canary, is the h0012-class NO-GO.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: The forked solver README implements the dual-output-contract arbitration protocol
  `solver_workflows/h0031-dual-output-contract-arbitration/README.md` — one new `## Stage: Dual Output Contract Arbitration` between Exploration and Implementation: Phase 1 shared evidence snapshot, Phase 2 two independent contracts (B = forced-divergence, must not read A), Phase 3 evidence-hierarchy arbitrator writing `arbitration.json` with one of SELECT_A/SELECT_B/MERGE_NON_CONFLICTING/REJECT_BOTH/ABSTAIN; implement-only-the-arbitrated-contract + abstain-not-verified; leak-guard/Exploration/Impl/Valid/Final byte-identical to parent (lines 1–48 verified identical).
- DONE: Smoke spec carries the entity smoke set + perturbable regression panel
  `specs/h0031-dual-output-contract-arbitration.smoke.yaml` — 11 tasks: 3 targets (ana-eng004, intercom001, f1011) + 6 cross-family canaries (airbnb001/ana-eng001/asana001/f1007/quickbooks002/f1001) + G8/G10 perturbable doubling (ana-eng002 same `obt_product_inventory` as target; asana003 same `int_asana__project_user` intermediate). Full spec differs from baseline ONLY in `experiment:` + `solver_workflow:` (diff verified); smoke differs from full ONLY by the `benchmark.tasks` block; both frozen via `rk freeze --allow-missing`; `kind=spacedock_solver`/`runtime=codex`/`trials=1` preserved.
- DONE: Gatekeeper ran against the variant artifacts and a review block is in the entity body
  Per-rule PASS/WARN/FAIL table written under `## Gatekeeper review` (G1–G10, incl. generative G8/G10); overall **APPROVE** (no FAIL; WARNs on G7 inert-risk + G9 in-session forced-divergence). Run inline (no Agent-dispatch tool available to this ensign); fork parent resolved to `codex-ade-dbt-minimal` (source: + @baseline config agree).

### Summary

Authored the h0031 dual-output-contract arbitration variant: forked the seed solver and added a single new Output-Contract-style stage that generates TWO independent contracts (A, plus a forced-divergence B that cannot read A) from a shared evidence snapshot, then arbitrates claim-by-claim against a fixed evidence hierarchy into a machine-readable `arbitration.json` (SELECT_A/SELECT_B/MERGE_NON_CONFLICTING/REJECT_BOTH/ABSTAIN) before any SQL is authored. Because the protocol is generative, the smoke panel was strengthened beyond the entity's base set to 11 tasks so each construct-sharing family (f1/ana-eng/asana) carries ≥2 perturbable canaries (the h0012 "break a different family member" guard). Gatekeeper recommends APPROVE; the load-bearing smoke watch-items are real per-target arbitration artifacts (G7) and genuine route-B divergence in the single-session substrate (G9, the h0026 wall). Propose stops at the gate — no `rk run` launched.

