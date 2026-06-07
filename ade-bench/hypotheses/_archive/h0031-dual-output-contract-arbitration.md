---
id: h0031
title: Dual Output Contract Arbitration -- generate two independent contracts, then select/abstain by visible evidence before implementation
status: conclude
kind: hypothesis
source: captain synthesis after _artifacts/arbitration-without-oracle.md and WORKFLOW-REFINE findings: Output Contract is useful as an observability surface (h0017) but not sufficient for correctness; h0026 proved self-anchored candidate scoring fails without independent judgment. This hypothesis tests the next protocol-family step: two independent contract routes plus an evidence-hierarchy arbitrator that can SELECT, REJECT_BOTH, or ABSTAIN before any SQL is authored.
started: 2026-06-07T00:00:00Z
completed: 2026-06-07T05:22:55Z
verdict: REJECTED
score:
worktree: 
archived: 2026-06-07T05:22:56Z
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

**NO-GO (cleanly falsified). Recommend conclude REJECTED.** Smoke run
`runs/ade-bench-h0031-dual-output-contract-arbitration/0de9870ae2220bca` (gpt-5.5@xhigh, trials:1).

- **Audit (AC-6):** `rk audit --policy strict` → `tainted: 0, clean: 11, coverage_missing: 0`;
  every cell `subagent-trace-manifest.json` has `captured: 1`. Score trusted.
- **Score:** `rk score` → 8/11 pass (pass@1 = 0.727), 0 errored. Above the 0.1875 constant.
- **Paired vs `@baseline` (`622bdedac572b479`), per-cell reward:**

| slug | role | baseline | h0031 | delta | distance-to-pass (h0031 vs baseline) |
|------|------|---------|-------|-------|---------------------------------------|
| ana-eng004 | TARGET (width) | 0.0 | 0.0 | — | identical: "has less columns than solution", 1-pass/1-fail both |
| intercom001 | TARGET (grain) | 0.0 | 0.0 | — | identical: "Got 7 results", 1-pass/1-fail both |
| f1011 | TARGET (answer-style) | 0.0 | 0.0 | — | identical: committed **ABDE**, fails `check_option_b` both |
| airbnb001 | canary | 1.0 | 1.0 | held | protocol not exercised (no arbitration.json) |
| ana-eng001 | canary | 1.0 | 1.0 | held | protocol not exercised |
| asana001 | canary | 1.0 | 1.0 | held | protocol not exercised |
| f1007 | canary | 1.0 | 1.0 | held | protocol not exercised |
| quickbooks002 | canary | 1.0 | 1.0 | held | protocol not exercised |
| f1001 | canary (f1 doublet) | 1.0 | 1.0 | held | arbitration.json written; still pass |
| ana-eng002 | canary (perturbable doublet) | 1.0 | 1.0 | held | protocol not exercised |
| asana003 | canary (perturbable doublet) | 1.0 | 1.0 | held | protocol not exercised |

- **Target flips:** 0. **Canary regressions:** 0 (incl. perturbable doublets ana-eng002 / asana003 → no h0012-class drop).
- **Gate routing:** 0 flips + lever changed no distance-to-pass on any target + the one path it
  controlled (f1011) reproduced the baseline's byte-identical wrong answer → **cleanly falsified →
  conclude (REJECTED)**.

## Run result

(skipped — smoke falsified; no full run.)

## Behavioral analysis

**The protocol is real, independent, and evidence-bearing — and still cannot beat the
blind-to-oracle wall.** This is the rare case where the lever did *exactly* what the spec asked and
the spec's own falsifier fired.

**AC-1 / G9 (route-B divergence) — PASSED on all 3 targets.** Route B genuinely diverged from A on
real claims, not a photocopy: intercom001's B drove `conversation_created_at` from
`conversation_history` and carried an explicit `attempt_to_defeat_route_a` block; ana-eng004's B
swapped the product source `dim_products` → raw `northwind.products`
(`supplier_company`→`supplier_ids`); f1011's B proposed a CEF reading the arbitrator rejected.

**AC-2 / AC-3 (evidence-based, machine-readable arbitration) — PASSED on the 4 cells that ran it.**
Real `arbitration.json` reached disk via `apply_patch` (verified `test -f`/`ls`) for ana-eng004
(MERGE_NON_CONFLICTING), intercom001 (SELECT_A), f1011 (SELECT_A → answer ABDE), and f1001.
Arbitration used INDEPENDENT probes, not transcript plausibility — intercom rejected route B via a
raw conservation check (`part_rows_with_history_match: 0`); ana-eng004 used a coverage probe
(dim_products misses 16 of 102 inventory rows; raw products covers all 102). **AC-5 (implementation
follows arbitrated contract) — PASSED**: committed SQL matched `selected_claims` on every target.

**AC-4 (abstention honored) — VIOLATED exactly where it was load-bearing.** Every target wrote
`abstained_claims: []` on the one claim that was genuinely oracle-only:
- ana-eng004: the exact expected column set is oracle-only (`arbitration.json` itself records
  `"No schema YAML declares obt_product_inventory"`) — yet the arbitrator committed a confident
  22-column width and failed "has less columns than solution".
- intercom001: the part_type→assignment/reopen/contact-reply metric mapping is oracle-only — the
  local sample had `assignment_rows: 0, reopen_rows: 0, comment_rows: 0`, i.e. **no visible rows to
  validate the mapping** — yet it SELECTed tier-3 "defensible local" guesses and missed by 7 rows.
- f1011: B=IN ("does not handle incomplete laps") was supported only by a self-derived local probe
  (`3,760 lap rows where max lap differs from results.laps`) that *correlates with* the wrong
  reading. Result: **the byte-identical wrong answer ABDE that the single-author baseline committed**,
  failing the same `check_option_b`.

**The falsifier in the Hypothesis fired verbatim:** "It is falsified if the two routes converge on
the same unsupported premise … if it forces a choice on an oracle-only disagreement." On every
target, the visible workspace could not decide the load-bearing claim, both routes (or the
arbitrator) converged on the locally-plausible-but-unsupported reading, and arbitration forced a
SELECT instead of ABSTAIN. Adding a second contract route + an external-evidence arbitrator
reproduces the single-author answer on exactly the tasks it was built to fix — the same wall as
`solver-blind-to-oracle`, h0026, and the verification-without-oracle synthesis, now confirmed for
the two-route generative form. The next step is not a third route; it is an **enforced abstention
gate** (a claim with no tier-1/tier-2 support and no route-deciding conservation/coverage signal
MUST be ABSTAIN, not a tier-3 default).

**Workflow-level (protocol-family eval, recorded in `_artifacts/WORKFLOW-REFINE.md`):** the new
stage was **selectively exercised — fired on only 4/11 cells** (3 targets + f1001). The 7
pure-passer canaries did NOT materialize the protocol (no `arbitration.json` written); the solver
ran the contracts only on tasks it found ambiguous. Upside: this makes the zero-regression result
genuine unchanged-baseline behavior rather than luck — the perturbable doublets were never touched.

## Verdict

**REJECTED (smoke).** Falsified by its own stated criteria. The dual-output-contract arbitration
protocol produces genuinely independent, evidence-bearing, machine-readable artifacts (AC-1/2/3/5
held) but cannot solve the oracle problem: on all three targets the load-bearing disagreement was
oracle-only, the arbitrator did not abstain (AC-4 violated), and every target reproduced baseline's
exact distance-to-pass — f1011 the byte-identical wrong answer ABDE. Zero target flips, zero canary
regressions. Transferable learning: route-divergence + external-criterion judgment are table stakes,
not a contribution; the missing piece is an *enforced* abstention on oracle-only claims.

## Next directions

**This is a STRATEGY decision for the captain, not an auto-filed follow-up.** Per conclude
discipline we do NOT reflexively file the next hypothesis — and here that restraint is load-bearing,
because the blind-to-oracle wall is now a **meta-pattern**: h0026 (self-anchored selector) and h0031
(two-route arbitration) have both hit it from opposite directions. h0031 supplied the two fixes h0026
lacked — genuine candidate **divergence** (route B verifiably disagreed with A) and an **external
judgment criterion** (raw conservation/coverage probes, never transcript) — and the wall held anyway.

**What is now exhausted (do NOT file more of this):** the candidate-generation / multi-route /
arbitration family. More routes, better divergence, better external judgment cannot manufacture an
oracle. On an oracle-only disagreement the visible workspace simply does not contain the
discriminating fact, so every route converges on the same locally-plausible-but-unsupported premise.
A third contract route, a "route C", a fancier arbitrator, or a plan-reviewer on top would all
reproduce this result.

**The one candidate next lever — and it is a GENUINELY NEW one, because it changes the OBJECTIVE, not
the candidate count.** Stop chasing the oracle; change what counts as success. An **ENFORCED
abstention gate**:

> A load-bearing claim with **no tier-1/tier-2 visible support** (explicit instruction or declared
> `schema.yml`) **AND no conservation/coverage signal that actually decides between the routes** MUST
> be marked `ABSTAIN`. An abstained load-bearing claim may not be silently filled by either
> contract's tier-3 "defensible local" default.

Why this is different from everything tried (h0017 / h0023 / h0026 / h0031): every prior lever tried
to make the workflow *get the answer right* by adding generation or judgment. This lever accepts that
on the unbreakable class the answer is *not locally recoverable* and changes the workflow's objective
to **calibrated refusal** — it turns a confident wrong (a guaranteed −0 that also pollutes any
downstream selection) into an honest "cannot decide locally." Its falsifier is sharp and cheap to
smoke: on the three h0031 targets the enforced gate MUST flip every load-bearing SELECT-on-oracle-only
to ABSTAIN (the arbitration.json on all three already self-records the oracle-only condition, e.g.
ana-eng004's `"No schema YAML declares obt_product_inventory"`), and it must NOT abstain on the
locally-decided canaries.

**Open risk the captain should weigh before approving:** this lever raises abstention, not pass-rate.
It is only worth pursuing if the benchmark / downstream consumer rewards calibrated abstention over a
confident wrong guess. If the scoring is strictly pass/fail with no credit (or penalty relief) for
abstaining, an enforced abstention gate will look like a pure score loss on the very targets it
"handles" — so the strategic question for the captain is **whether the objective itself (maximize
flips) is the right objective, or whether honest abstention on the oracle-only class is the more
valuable behavior to reward.** That objective question, not another candidate-generation hypothesis,
is the live fork.

## Stage Report: propose

- DONE: The forked solver README implements the dual-output-contract arbitration protocol
  `solver_workflows/h0031-dual-output-contract-arbitration/README.md` — one new `## Stage: Dual Output Contract Arbitration` between Exploration and Implementation: Phase 1 shared evidence snapshot, Phase 2 two independent contracts (B = forced-divergence, must not read A), Phase 3 evidence-hierarchy arbitrator writing `arbitration.json` with one of SELECT_A/SELECT_B/MERGE_NON_CONFLICTING/REJECT_BOTH/ABSTAIN; implement-only-the-arbitrated-contract + abstain-not-verified; leak-guard/Exploration/Impl/Valid/Final byte-identical to parent (lines 1–48 verified identical).
- DONE: Smoke spec carries the entity smoke set + perturbable regression panel
  `specs/h0031-dual-output-contract-arbitration.smoke.yaml` — 11 tasks: 3 targets (ana-eng004, intercom001, f1011) + 6 cross-family canaries (airbnb001/ana-eng001/asana001/f1007/quickbooks002/f1001) + G8/G10 perturbable doubling (ana-eng002 same `obt_product_inventory` as target; asana003 same `int_asana__project_user` intermediate). Full spec differs from baseline ONLY in `experiment:` + `solver_workflow:` (diff verified); smoke differs from full ONLY by the `benchmark.tasks` block; both frozen via `rk freeze --allow-missing`; `kind=spacedock_solver`/`runtime=codex`/`trials=1` preserved.
- DONE: Gatekeeper ran against the variant artifacts and a review block is in the entity body
  Per-rule PASS/WARN/FAIL table written under `## Gatekeeper review` (G1–G10, incl. generative G8/G10); overall **APPROVE** (no FAIL; WARNs on G7 inert-risk + G9 in-session forced-divergence). Run inline (no Agent-dispatch tool available to this ensign); fork parent resolved to `codex-ade-dbt-minimal` (source: + @baseline config agree).

### Summary

Authored the h0031 dual-output-contract arbitration variant: forked the seed solver and added a single new Output-Contract-style stage that generates TWO independent contracts (A, plus a forced-divergence B that cannot read A) from a shared evidence snapshot, then arbitrates claim-by-claim against a fixed evidence hierarchy into a machine-readable `arbitration.json` (SELECT_A/SELECT_B/MERGE_NON_CONFLICTING/REJECT_BOTH/ABSTAIN) before any SQL is authored. Because the protocol is generative, the smoke panel was strengthened beyond the entity's base set to 11 tasks so each construct-sharing family (f1/ana-eng/asana) carries ≥2 perturbable canaries (the h0012 "break a different family member" guard). Gatekeeper recommends APPROVE; the load-bearing smoke watch-items are real per-target arbitration artifacts (G7) and genuine route-B divergence in the single-session substrate (G9, the h0026 wall). Propose stops at the gate — no `rk run` launched.


## Stage Report: smoke

- DONE: Smoke run completed on specs/h0031-dual-output-contract-arbitration.smoke.frozen.yaml with a CLEAN strict audit and captured > 0 in every cell; focused rk score recorded in ## Smoke result (AC-6)
  Run `0de9870ae2220bca`, 11/11 trials, 0 errored; `rk audit --policy strict` → tainted:0, clean:11, coverage_missing:0; every `subagent-trace-manifest.json` captured:1; `rk score` → 8/11 pass (pass@1=0.727).
- DONE: Per-target protocol+behavioral deep-dive for ALL three targets (ana-eng004, intercom001, f1011): real contract_a+contract_b+arbitration.json reached the committed artifact, route B genuinely diverged, classified flip/distance-to-pass vs @baseline; zero of 8 canaries regressed
  All 3 targets wrote a real `arbitration.json` to disk (apply_patch, verified `test -f`/`ls`); route B verifiably diverged (intercom B had an explicit `attempt_to_defeat_route_a`; ana-eng004 B swapped product source; f1011 B proposed CEF); arbitration used independent conservation/coverage probes (AC-1/2/3/5 held). All 3 land at the IDENTICAL distance-to-pass as @baseline — f1011 committed the byte-identical wrong answer ABDE failing the same check_option_b. 0 flips, 0 canary regressions (ana-eng002/asana003 doublets both 1.0). AC-4 violated: every target abstained_claims:[] on the load-bearing oracle-only claim.
- DONE: Protocol-family change => AUTOMATIC workflow-refinement evaluation done and recorded in _artifacts/WORKFLOW-REFINE.md; go/no-go covers BOTH task-level and workflow-level
  WORKFLOW-REFINE.md entry appended: the new arbitration stage was selectively exercised (fired on only 4/11 cells — the 3 targets + f1001; the 7 pure-passer canaries did NOT materialize the protocol), so the zero-regression result is genuine unchanged-baseline behavior; transferable learning = route-divergence + external-criterion judgment are table stakes, the missing piece is an ENFORCED abstention on oracle-only claims.

### Summary

NO-GO / cleanly falsified — recommend conclude REJECTED. The dual-output-contract arbitration protocol did exactly what the spec asked (genuinely independent route B, machine-readable evidence-based `arbitration.json` reaching the committed SQL on every target) yet moved zero targets and changed zero distances-to-pass vs @baseline; f1011 reproduced the baseline's byte-identical wrong answer ABDE. The hypothesis's own falsifier fired verbatim: on every target the load-bearing disagreement was oracle-only, both routes converged on the locally-plausible-but-unsupported reading, and the arbitrator forced a SELECT instead of ABSTAIN (AC-4 violated). Zero canary regressions (incl. perturbable doublets) — genuine, because the protocol was only exercised on the 4 ambiguous cells and never touched the 7 easy passers. Same blind-to-oracle wall as h0026 / solver-blind-to-oracle, confirmed for the two-route generative form.


## Stage Report: conclude

- DONE: The _artifacts/WORKFLOW-REFINE.md entry for h0031 is FINALIZED to a terminal state per that file's template
  Header set to `(h0031, REJECTED — rejected-as-written, 2026-06-07)` + a new `**Status:**` line = `rejected-as-written` (protocol-family change tested + cleanly falsified at smoke, no full run). `Learning` line rewritten to lead with "genuinely-independent route B + external-criterion arbitration are TABLE STAKES, not a contribution" (they reproduced baseline's exact wrong answers) and name the missing piece (ENFORCED abstention gate). `Bears on` line now explicitly names the steered siblings: h0026 (self-anchored selector), h0017/h0023 (single-contract), and the solver-blind-to-oracle / verification-without-oracle family (now a meta-pattern).
- DONE: The entity's distilled learnings are portable and complete in ## Verdict / ## Behavioral analysis
  Audited the four required points already present (no re-run): failure mechanism (AC-4 violated on oracle-only claims, routes converge on locally-plausible-but-unsupported reading); change DID reach the committed artifact (real `arbitration.json` via apply_patch, AC-1/2/3/5 held — not inert); identical distance-to-pass deltas (Smoke-result table + f1011 byte-identical ABDE); transferable rule (divergence + external judgment are table stakes; enforced abstention is the missing piece). Complete — no additions needed to those two sections.
- DONE: Per conclude discipline, DO NOT reflexively file a follow-up — surface the candidate next lever as a STRATEGY decision for the captain
  Added `## Next directions` to the entity: NO new hypothesis filed. Surfaces the ENFORCED abstention gate as the one candidate next lever, explicitly flagged as a GENUINELY NEW lever (it changes the OBJECTIVE — calibrated refusal — not the candidate count, which is the exhausted family). Names the open risk (it raises abstention not pass-rate; only worth it if the consumer rewards calibrated abstention) and frames the live fork as an objective question for the captain. Did NOT set verdict frontmatter and did NOT archive (FO performs terminal frontmatter + archive).

### Summary

Finalized the cross-experiment records and the strategy fork for the cleanly-falsified h0031. No re-run and no run-dir reads — the smoke deep-dive is the evidence of record. The WORKFLOW-REFINE.md h0031 entry is now terminal (`rejected-as-written`) with a sharp table-stakes learning line and a bears-on line naming h0026 / h0017 / h0023 / the blind-to-oracle family. The entity's Verdict + Behavioral analysis already carried all four required portable learnings (verified, not re-derived). Per the exhausted-family discipline I filed NO follow-up; instead a new `## Next directions` section surfaces the ENFORCED abstention gate to the captain as a strategy decision, explicitly distinguishing it (a genuinely new OBJECTIVE-changing lever) from the now-exhausted candidate-generation/arbitration family, and flagging the open question of whether the benchmark rewards calibrated abstention over a confident wrong. Verdict frontmatter + archive deliberately left to the FO.
