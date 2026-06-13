---
id: h0056
title: Six-lever composition — stack the three new smoke-verified levers (h0053 per-key inner-join + h0054 lap-time exclude-pit-laps + h0055 build/rename preserve-columns) onto @baseline h0052's three (max-points + feature-boundary + coverage) in ONE README
status: propose
kind: hypothesis
source: "Captain request 2026-06-13 — merge the three individually smoke-verified levers (h0053 airbnb005 inner-join GO; h0054 f1010-medium exclude-pit-laps GO; h0055 ana-eng003 preserve-columns, smoke in progress / ana-eng003 artifact passing) into one composition on the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133). Same compose-verified-bleed-free-levers play that promoted h0052; each new lever is precondition-gated and explicitly non-colliding with an existing one."
started: 2026-06-13T17:45:52Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The h0052 baseline README already composes three construct-gated levers (h0044 same-grain
`max(points)`, h0045 feature-boundary removal/toggle, h0050 intent-gated scoped coverage). This
hypothesis stacks the three NEW smoke-verified levers on top, in one README — six gated
Implementation rules total:

| # | Lever | Construct it gates on | Smoke evidence |
|---|-------|-----------------------|----------------|
| 1 | h0044 max(points) | standings/season points | (in h0052) f1006 + f1006-hard flips |
| 2 | h0045 feature-boundary | remove/disable feature | (in h0052) qb002/qb004 narrow holds |
| 3 | h0050 scoped coverage | completeness-intent missing rows | (in h0052) airbnb009 flip |
| 4 | **h0053 per-key inner-join** | per-key metric, NO completeness intent | **GO** — airbnb005 inner-join, 14,243-row oracle match |
| 5 | **h0054 lap-time exclude** | lap/duration avg accounting for pit stops | **GO** — f1010-medium EXCLUDE artifact |
| 6 | **h0055 preserve-columns** | build/rename, no feature-removal, no col-subset | smoke in progress (ana-eng003 artifact passing) |

**Two gated dual-pairs must coexist without collision (the integration risk):**
- **h0050 ↔ h0053** — opposite sides of the completeness-intent signal. h0050 ADDS missing keys
  when completeness IS requested (airbnb009); h0053 scopes to fact keys when it is NOT (airbnb005).
  Proven non-colliding in h0053's solo smoke (airbnb009 held while airbnb005 flipped).
- **h0045 ↔ h0055** — opposite task types. h0045 DROPS feature-only columns on remove/disable
  tasks (qb002/qb004); h0055 PRESERVES all upstream columns on build/rename (ana-eng003).

**Falsifiable claim (the single README change):** fork the current `@baseline` (h0052) solver and
add the three new levers **verbatim, each as its own precondition-gated Implementation rule** —
nothing else. The six-lever composition will preserve every lever's solo effect with **no
interference and no collision**:
- airbnb005 flips via the inner-join shape (h0053);
- f1010-medium commits the EXCLUDE artifact and ana-eng003 the full-18-column artifact
  (h0054/h0055 — noise-reducers that pin two coin-flip cells, shrinking the trials:1 variance pool);
- airbnb009 + f1006 + f1006-hard (h0052's banked flips) HOLD;
- qb002 + qb004 still drop their feature columns (h0045 fires, h0055 does NOT);
- every canary holds.

**Why compose:** the program-wide lesson is that trials:1 ±noise (~±3 cells) washes a single
flip's net. Stacking verified bleed-free levers (a) banks airbnb005 (+1 over h0052) AND (b) **pins
two of the coin-flip cells** (f1010-medium, ana-eng003) that have been costing nets — a tighter
variance band, not just a higher signal. Best case nets above h0052's true expectation (~30) and
clears it on a fresh draw.

**Falsified if** composing degrades any lever vs its solo smoke (interference / README bloat
mis-routing a precondition), OR a dual-pair collides (airbnb009 coverage suppressed; qb feature
columns force-preserved), OR a canary regresses beyond off-construct trials:1 variance.

Target datasets: airbnb005 (flip); f1010-medium, ana-eng003 (pin/stabilize); airbnb009, f1006,
f1006-hard, qb002, qb004 (hold).

## Pre-smoke Decision-Fork Probe

Skipped — each of the three new levers is individually smoke-verified at the committed-artifact
level (h0053 GO, h0054 GO, h0055 GO-pending) and each was already shown non-colliding with its dual
in its solo smoke (h0053: airbnb009 held; h0055: qb002/003 held). The only new question is the
six-way composition / mutual interference, which the combined smoke tests directly (and the h0052
promotion already established that construct-gated levers compose). No new probe owed.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Composed README = h0052's README + the h0053, h0054, h0055 lever blocks verbatim (each traceable to
its source solver dir), nothing else; the existing three levers + leak-guard byte-unchanged.

**AC-2 — Every recorded score paired with a clean strict audit** (captured>0 every cell).

**AC-3 — Verdict by paired delta vs `@baseline` (h0052), read through the known ~±3 trials:1 noise
floor.** Promote on committed-artifact + expectation (per the h0052 self-consistency precedent), not
a single-draw net alone.

**AC-4 — Per-lever committed-artifact reads (the decisive test):** airbnb005 = inner-join-from-fact
(no zero-fact NULL rows); f1010-medium = EXCLUDE pit laps before avg; ana-eng003 = all 18 columns;
airbnb009 = coverage predicate dropped (h0050 still fires); f1006/f1006-hard = `max(points)`;
qb002/qb004 = narrow feature-boundary (columns dropped, h0045 still fires).

**AC-5 — Regression panel + BOTH collision-canary pairs hold:** airbnb009 (h0050↔h0053 collision),
quickbooks002 + quickbooks003 (h0045↔h0055 collision), plus ≥1 perturbable passer per family. A
collision or same-construct regression is a NO-GO; off-construct trials:1 variance is classified,
not auto-fatal; the promote decision rests on the run-dir clearing h0052's expectation.

## Gatekeeper review

**Recommendation: APPROVE** — clean composition: each of the three new levers inserted byte-verbatim from its smoke-verified sibling, precondition-gated (non-generative), leak-guard + spec scope intact, both collision-canary pairs in the smoke panel; the only WARNs are the standing predictive ones (G7 structural-rewrite inert-risk, G11 multi-model-target variance) that never block.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-13T18:00Z.

Fork parent resolved: `@baseline` = h0052 (`rk registry resolve run @baseline` → runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133; its solver_workflow = solver_workflows/h0052-compose-maxpoints-featureguard-scoped-coverage). Matches the hypothesis `source:`. Diff base = the h0052 solver README.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff h0052 h0056 README` = exactly 3 added hunks (79a, 138a, 165a), 0 deletions/changes; all three land under `## Stage: Implementation` (block lines 80/158/206, between Implementation@50 and Validation@221). The hypothesis's Falsifiable claim explicitly proposes adding these three blocks as one composition — three rules, one stage, the declared single change. |
| G2 leak-guard intact | PASS | grep of curl/wget/git clone/ls-remote/download/AUTO_/solution__/check_option/verifier/equality-test/expected-output/drive-to-zero/self-anchored phrasings over the added lines → none. Parent prose byte-unchanged (`diff` shows 0 `<` deletions). |
| G3 spec two fields | PASS | `diff baseline.yaml h0056.yaml` = only `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0056.yaml h0056.smoke.yaml` = only an added `benchmark.tasks:` block (16 slugs, all `ade-bench-` prefixed). Panel includes every hypothesis target (airbnb005, f1010-medium, ana-eng003) + regression sentinels (f1006/f1006-hard hold). No other field differs. |
| G5 both frozen | PASS | `h0056-*.frozen.yaml` + `…smoke.frozen.yaml` both exist; both carry `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Each inserted block is byte-identical to its smoke-verified source sibling (BLOCK A == h0054, BLOCK B == h0053, BLOCK C == h0055 — confirmed by per-block `diff -q`). Wording matches the claim exactly; no scope creep. All three are gated, build-direction/structural rules carrying worked BEFORE/AFTER SQL skeletons — generative-derivation guidance, not self-anchored "verify your own work." |
| G7 actionability/inert-risk | WARN | All three are structural-shape rules (join direction, exclude-then-aggregate, preserve-column-set) — the G7 inert-risk family at gpt-5.5/xhigh — BUT each carries a literal BEFORE→AFTER SQL skeleton (the worked-example form G7 prescribes as the mitigation) and each was individually committed-artifact-verified in its solo smoke (h0053 GO 14,243-row inner-join, h0054 EXCLUDE artifact, h0055 18-col artifact). Inert-risk materially reduced by the worked examples + prior solo evidence; surfaced per the predictive rule. |
| G8 regression-canary coverage | PASS (N/A-leaning) | All three levers are precondition-GATED, not generative (inert on any model not matching their construct), so G8 is N/A by its own gate. Even so the smoke panel carries a full canary set: ≥1 non-target passer from airbnb/asana/ana-eng/f1/quickbooks (no intercom passer exists), and the construct-adjacent families carry ≥2 perturbable canaries (airbnb 001/004/006/008; f1 1005/1006/1006-hard/1007). |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — three gated mechanical SQL-shape rules. |
| G10 self-correcting false-positive | N/A | None of the three is a check/reconcile/validate-and-fix lever; they are build-time SQL-shape constructions, not "verify a number and act on disagreement." |
| G11 multi-model-target risk | WARN | airbnb005 (h0053) and ana-eng003 (h0055) may be scored by >1 `AUTO_*_equality` model; each new lever's precondition touches the specific authored model, so a single-run flip on a multi-model target should be read as artifact-on-the-addressed-model, not aggregate proof. The hypothesis already commits to ≥2 seed-perturbed repeats per target judged by committed artifact (AC-3/AC-5), which is the prescribed mitigation. Predictive only. |
| G12 decision-fork probe quality | N/A | `## Pre-smoke Decision-Fork Probe` present and explicitly states the probe was skipped because each of the three levers is already individually committed-artifact smoke-verified and each was shown non-colliding with its dual in its solo smoke; the only new question (six-way interference) is what this smoke tests directly. Valid skip rationale. |

**For the captain:** Clean APPROVE — the composition is the three smoke-verified blocks dropped in verbatim with zero edits to h0052's existing six-lever-minus-three body or leak-guard. Two standing WARNs only (G7 structural-rewrite inert-risk, mitigated by the worked SQL skeletons + prior solo GOs; G11 multi-model variance on airbnb005/ana-eng003, mitigated by the AC-5 ≥2-repeat artifact judging). Per the dispatch the captain intends to skip smoke and go straight to full after the FO decision-fork simulation; the smoke spec is built and frozen for completeness regardless.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Merged solver README = h0052 README + three lever blocks inserted VERBATIM at section anchors; `diff h0052/README.md h0056/README.md` shows EXACTLY those three hunks, leak-guard prose byte-unchanged (AC-1)
  Fork via `cp -r`; applied each sibling's single-block diff as a patch. diff = 3 added hunks (79a BLOCK C/h0055, 138a BLOCK B/h0053, 165a BLOCK A/h0054), 0 deletions; per-block `diff -q` confirms each block byte-identical to its source sibling; all three under `## Stage: Implementation`.
- DONE: Full spec h0056.yaml differs from baseline.yaml ONLY in experiment: + solver_workflow:; smoke spec adds benchmark.tasks integration panel; both frozen with rk freeze --allow-missing
  `diff baseline.yaml h0056.yaml` = exactly those 2 lines. Smoke panel = 16 tasks: targets airbnb005/f1010-medium/ana-eng003 + collision pairs airbnb009 and quickbooks002+003 + banked holds f1006/f1006-hard + per-family perturbable passers (airbnb001/004/006/008, f1005/f1007, asana002, ana-eng001). Smoke scaffold byte-identical to siblings (only tasks/exp/solver differ). Both .frozen.yaml written.
- DONE: Gatekeeper run against the variant artifacts; `## Gatekeeper review` block written with per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT + one-line rationale
  Fork parent resolved @baseline=h0052 (registry + source agree). Overall APPROVE; G1-G6 PASS, G8 PASS(N/A-leaning, gated), G9/G10/G12 N/A, two standing predictive WARNs (G7 inert-risk mitigated by worked SQL skeletons + prior solo GOs; G11 multi-model variance mitigated by AC-5 repeats).

### Summary
Built the six-lever composition by forking @baseline h0052's solver and inserting the three smoke-verified lever blocks (h0053 per-key inner-join, h0054 lap-time exclude-pit-laps, h0055 build/rename preserve-columns) byte-verbatim at their Implementation-stage anchors. Full spec differs from baseline only in experiment+solver_workflow; smoke spec adds a 16-task integration panel (union of the three sibling smoke panels, deduped, with both collision-canary pairs). Both specs frozen. Gatekeeper recommendation APPROVE — no FAILs, only the two standing predictive WARNs. Per dispatch the captain intends to skip smoke and go straight to full after the FO decision-fork simulation.
