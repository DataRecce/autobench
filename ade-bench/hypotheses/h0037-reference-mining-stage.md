---
id: h0037
title: Reference Mining — a NEW pre-Implementation stage that cites the closest already-passing in-project analog and copies its FROM/join/spine/window construction verbatim before any model edit
status: propose
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §3 E-RMS (rank 1, captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 1. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-09T07:01:21Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

**Falsifiable claim (the single README change — a NEW `## Stage: Reference Mining` inserted
between Exploration and Implementation):** systematizing the lone-survivor mechanism — a verbatim
BEFORE/AFTER skeleton anchored to a named local artifact (h0019, the one genuine fix) — from a
one-off Implementation clause into a generative pre-Implementation stage will produce a committed,
cited in-project analog (`Analog: <file>:<line-range>`) whose FROM/join/spine/window construction is
copied verbatim as the Implementation skeleton, and will flip **ana-eng004** (`ade-bench-ana-eng004`,
`obt_product_inventory`, width) from FAIL to PASS, raising `stratified_pass_at_1` above the
`@baseline` 0.6458.

**The single solver-README change.** Add exactly one `## Stage: Reference Mining` header between the
existing `## Stage: Exploration` and `## Stage: Implementation`. The stage requires the solver, before
editing any target model, to: (a) name the target's directory/layer and grain; (b) locate the closest
already-passing **in-project** sibling in the same layer (e.g. `analytics_obt/obt_sales_overview.sql`
beside the failing `obt_product_inventory`), or — absent a sibling — an installed-package template of
the same shape; (c) record `Analog: <file>:<line-range>` plus the analog's FROM relation, join ladder,
spine/key source, and window/group-by to the sanctioned non-graded notes location; (d) in
Implementation, copy that construction verbatim as the skeleton and adapt only leaf columns/source.
The **cited-analog requirement** is what makes the stage structural (it reaches SQL the way h0017 did)
rather than inert prose (h0010/h0016). The project's OWN passing siblings are tried FIRST; an installed
package is a fallback only — this is the deliberate gate that removes the h0023 convention-bleed vector.

**Independent non-oracle signal.** The in-/app **passing-sibling artifact** — a GREEN model the
project's own dbt build already produces. It is real, ships to `/app`, and is non-oracle: it encodes
the project's authored column-ladder / join / grain *convention*. The signal is **convention-fidelity**
(does my model's FROM/join/spine match the analog's?), NOT a target value. No hidden
`AUTO_*_equality` / `solution__*` / `check_option_*` / `tests/AUTO_*` is named or read.

**Leading indicator (distance, `Got N`).** ana-eng004's `obt_product_inventory` fails the width check
("has less columns"); watch whether the copied `obt_sales_overview` ladder shrinks the gap.
**Honest prediction: no movement or wrong-direction** — the sibling `obt_sales_overview` is *wider*
than the target and the target already follows the identical OBT skeleton, so copying the analog's
column-ladder ADDS columns where the hidden `AUTO_obt_product_inventory_equality` requires DROPs to
match `solution__obt_product_inventory`. Secondary reach-only intercom001 (`Got 7`) / intercom003: expect
flat. A flat `Got N` across the panel is inertness / oracle-wall confirmation — the cheapest kill.

**Kill-path / predicted failure mode.** On ana-eng004 the analog is structurally wider than the target
and the target already follows the OBT skeleton; copying the analog's column-ladder ADDS columns while
the width oracle requires DROPs that live only in `solution__obt_product_inventory`. Expected
flat-or-worse `Got N` — the width oracle wall (dead family D6). If the committed `obt_product_inventory.sql`
does not carry the cited analog's construction (the analog-discovery step went inert), or `Got N` is
flat across the panel, the stage joins the prose ceiling and is REJECTED.

**Dead family it must avoid (proposal §6 map) + how it differs.** Resembles **D6 width**
(h0011/h0023/h0029, ORACLE-ONLY) on its primary target and **D1 grain-convention** on intercom. It is
NOT the dead **h0009 package-copy** because it is gated to the project's OWN passing siblings first
(package only as fallback), removing the h0023 convention-bleed vector that regressed f1001 6/6→2/6; it
copies *construction shape*, not a deliverable set; it lives in a new pre-Implementation stage that
reaches SQL. It differs from h0017 by copying an *existing correct artifact verbatim* instead of
authoring a contract from scratch (which h0017 wrote backwards, naming the child as grain driver).

**Target datasets.** Primary: `ade-bench-ana-eng004` (`obt_product_inventory`, width — has a confirmed
passing same-dir sibling `obt_sales_overview.sql`). Secondary reach-only: `ade-bench-intercom001` /
`ade-bench-intercom003` (sibling `int_intercom__*` intermediates exist). The method/reach value is
systematizing the survivor engine across all 48.

**Honest expectation.** **{0}** flips on the known 17 (the analog is the wrong dimension — convention,
not the deciding DROP/value). The contribution is reach-systematization of the survivor engine plus a
possible distance read on ana-eng004. This is a `trials: 1`, judge-by-artifact entity; it faces its own
propose + smoke gate, and the captain decides whether it ever runs.

**Scope.** Workflow-stage / prompt lever only; benchmark FIXED; no expanded solver access; leak-guard
intact (the stage references only local artifacts — sibling models, installed-package templates, the
target's own grain — and names no hidden `AUTO_*` / `solution__*` / `check_*` / verifier test, no
`equality test` / `has less columns` / `expected output seed`, no `Got N` or row count, and no
`curl`/`wget`/`git clone`/web/published-solution fetch). The change touches exactly one new `## Stage:`
header and leaves the leak-guard prose + Exploration/Implementation/Validation/Finalization
byte-identical. The full spec differs from `@baseline` only in `experiment:` + `solver_workflow:`; the
smoke spec additionally adds `benchmark.tasks`. Because the stage is **generative** (it fires on every
model edit, not gated to the target), per gatekeeper G8 the smoke set MUST carry a cross-family
regression-canary panel plus ≥2 *perturbable* canaries for the OBT/width construct family.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0037-reference-mining-stage.yaml` shows only
`experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md` adds exactly
one `## Stage: Reference Mining` header between Exploration and Implementation, leaves the leak-guard
prose (lines ~1–32) and the four existing stages byte-identical, and names no hidden
`AUTO_*`/`solution__*`/`check_*`/verifier test. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (computed from
`per_trial_outcomes.json`, slug-paired, 10k bootstrap — `rk runs diff` crashes on ade-bench run-dirs)
plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
The smoke deep-dive MUST read the committed `obt_product_inventory.sql` (the dispatched-ensign
`apply_patch` payload) and confirm the cited analog's construction REACHED the SQL — the FROM/join/
spine/window ladder copied from the named `Analog:`, not transcript chatter — plus the `Got N` distance
vs `@baseline`. A green score alone is NOT attribution (the h0033 green-but-inert lesson). If the
committed SQL does not carry the analog construction, or `Got N` is flat across the panel, the stage is
INERT/ceiling-bound → REJECTED.

## Gatekeeper review

**Recommendation: APPROVE** — exactly one new `## Stage: Reference Mining` between
Exploration and Implementation; leak-guard byte-identical; both specs differ only in the
sanctioned fields; generative lever carries a full G8 panel (target + 3 perturbable OBT/wide
canaries + one passer per other family). No FAIL. Two WARN-only inert-risk notes (G7 structural
copy at xhigh; the kill-path width-oracle prediction).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-08). Reviewed 2026-06-09T07:10Z.
Fork parent: `solver_workflows/codex-ade-dbt-minimal` (= `@baseline` run
`runs/ade-bench-baseline/622bdedac572b479`, 31/48; `source:` and registry agree).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs parent = one hunk `49a50,154`, all additions, zero deletions; the only new `## Stage:` header is `## Stage: Reference Mining`, inserted between Exploration and Implementation; no other stage touched. |
| G2 leak-guard intact | PASS | `sed -n '1,49p'` of fork == parent byte-for-byte (leak-guard + Exploration unchanged); grep over added lines 50-154 finds no `AUTO_*`/`solution__*`/`check_*`/`tests/AUTO`/`verifier`/`equality test`/`has less columns`/`Got N`/`row count`/`curl`/`wget`/`git clone`/`hf://`/web-fetch token (all hits are in the unchanged parent prose). |
| G3 spec two fields | PASS | `diff baseline.yaml h0037….yaml` = only `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1`, `reasoning_effort: xhigh` preserved. |
| G4 smoke tasks-only | PASS | `diff full smoke` adds only the `benchmark.tasks` block (+ comments); every target the `## Hypothesis` names is present (`ade-bench-ana-eng004`, plus reach `ade-bench-intercom001`/`003`); all slugs `ade-bench-`-prefixed; ≥1 stable-pass sentinel present. |
| G5 both frozen | PASS | `…frozen.yaml` and `…smoke.frozen.yaml` both written; both carry `kind: spacedock_solver` (l.4) + `runtime: codex` (l.5) + `trials: 1`; smoke frozen lists all 10 panel tasks. |
| G6 resolver fidelity | PASS | Inserted text = the claim verbatim: a pre-Implementation stage that (a) names layer+grain, (b) finds the closest already-passing **in-project** sibling (own siblings FIRST, package fallback), (c) records `Analog: <file>:<line-range>` + FROM/join/spine/window, (d) copies that construction verbatim in Implementation. NOT self-anchored (h0006/7/8 family): it reconciles against an INDEPENDENT local signal — a GREEN sibling the project already builds — not the solver's own re-run/old output. No scope creep. |
| G7 actionability/inert-risk | WARN | Structural-copy lever (FROM/spine/join reuse) — the family the baseline proved behaviorally inert at gpt-5.5/`xhigh` (h0010 0/4, h0016, h0008 0/7: "talks but doesn't do"). MITIGATED by a worked-example SQL skeleton (the analog is the AFTER skeleton the solver copies, h0019-form) rather than abstract prose, which is the form the rule says to prefer. Residual inert-risk: the hypothesis itself predicts {0} flips on the width oracle. Inert-risk noted for the captain; never blocks. |
| G8 regression-canary coverage | PASS | Generative (fires on every model-authoring task, not gated to the target). Smoke panel: target `ana-eng004` (FAIL) + **3 perturbable OBT/wide canaries** — `ana-eng002` & `ana-eng002-medium` (scored on the **SAME** model `AUTO_obt_product_inventory_equality` the target is, so the stage fires on the identical OBT construct) and `ana-eng005` (`fact_inventory`, wide warehouse model) — + **one `@baseline` passer per other family**: `airbnb001`, `asana001`, `f1001` (the passer h0023's convention-bleed broke 6/6→2/6), `quickbooks002`. ≥2 perturbable canaries on the targets' construct family satisfied; one canary per other family satisfied. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — single solver session authors one model per task; no N-candidate scoring. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever — it copies a construction skeleton BEFORE the edit; it does not verify a result and act on disagreement, names no figure to reconcile, and mandates no re-derivation against a self-built CTE. |
| G11 multi-model-target risk | N/A | Primary target `ade-bench-ana-eng004` is scored by a single model (`AUTO_obt_product_inventory_equality` + `_existence`, both on `obt_product_inventory`) — confirmed from its `verifier/test-stdout.txt`. The lever fires on whatever model the task builds, so it reaches that one scored model. Single-model target ⇒ no unaddressed-second-model variance trap. |

**For the captain:** No integrity FAIL — clean to advance to `smoke`. The two WARNs are
predictive, not blocking: **(G7)** this is a structural FROM/spine/join-copy lever, the exact
family that has been behaviorally inert at gpt-5.5/`xhigh` (talks-but-doesn't-do); the worked-example
skeleton is the recommended mitigation but the hypothesis honestly predicts {0} flips because the
sibling `obt_sales_overview` is WIDER than the target and the width oracle requires DROPs that live
only in the hidden solution. The decisive smoke read is **attribution, not the green score**: read
the committed `obt_product_inventory.sql` and confirm the cited `Analog:` construction actually
reached the SQL (recoverable from `/tmp/reference_mining.json` echoed to stdout). **(regression
risk — highest of the R2 set)** this is the only R2 lever that both fires generatively AND copies
construction INTO committed SQL on every model, so it can break a passer by copying a wrong/wider
analog — `ana-eng002` / `ana-eng002-medium` are the decisive canaries (same OBT model as the
target); a single canary dropping FAIL is a NO-GO regardless of any target flip.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: README change = EXACTLY ONE new `## Stage: Reference Mining` inserted between Exploration and Implementation
  `diff codex-ade-dbt-minimal/README.md h0037…/README.md` = single hunk `49a50,154`, all additions; (a) names target layer+grain, (b) own-siblings-FIRST / package-fallback gate, (c) records `Analog: <file>:<line-range>` + FROM/join/spine/window, (d) Implementation copies it verbatim. Leak-guard + four existing stages byte-identical (lines 1-49 == parent); grep over added lines finds no hidden `AUTO_*`/`solution__*`/`check_*`/verifier/`has less columns`/equality/`Got N`/row-count/`curl`/`wget`/`git clone`/web token.
- DONE: DURABLE ARTIFACT ROUTING — the h0041-VALIDATED fix is MANDATORY
  Stage records the `Analog:` citation + construction UNCONDITIONALLY to `/tmp/reference_mining.json` and `cat`s it to stdout (h0041 form); does NOT route through the dead `/razorback-freeze` single-child precondition. JSON schema carries `analog`, `from_relation`, `join_ladder`, `spine_key_source`, `window_group_by` so the smoke read can recover the cited analog from the transcript and verify it reached the committed SQL.
- DONE: Smoke spec `benchmark.tasks` — generative stage panel per G8
  10 tasks: target `ade-bench-ana-eng004` + 3 perturbable OBT/wide canaries (`ana-eng002`, `ana-eng002-medium` — both scored on the SAME model `obt_product_inventory` as the target; `ana-eng005` = wide `fact_inventory`) + one passer per other family (`airbnb001`/`asana001`/`f1001`/`quickbooks002`) + reach-only `intercom001`/`intercom003`. Gatekeeper run; per-rule table + APPROVE recorded in `## Gatekeeper review`.

### Summary

Forked the `@baseline` solver into `solver_workflows/h0037-reference-mining-stage` and added exactly one
`## Stage: Reference Mining` between Exploration and Implementation that systematizes the h0019
lone-survivor engine: cite the closest already-passing IN-PROJECT sibling (own siblings first, package
fallback) as `Analog: <file>:<line-range>`, record its FROM/join/spine/window, and copy that construction
verbatim in Implementation. Artifact routing uses the h0041-validated unconditional `/tmp` + cat-to-stdout
form (NOT the dead `/razorback-freeze` precondition) so the smoke read can attribute the analog to the
committed SQL. Specs differ from baseline only in `experiment:`+`solver_workflow:` (full) and the added
`benchmark.tasks` (smoke); both frozen with kind/runtime/trials preserved. Gatekeeper recommendation:
**APPROVE** (no FAIL; two WARN-only inert/regression-risk notes). NOT YET RUN — this is the propose gate;
the captain decides whether it advances to smoke.

### Smoke-set presentation (for the captain — baseline rewards from `622bdedac572b479/per_trial_outcomes.json`)

```
┌───────────────────────────┬──────────┬──────────────────────┬─────────────────────────────────────────────────────┐
│           Task            │ Baseline │ Should pass in smoke?│                Role / why we picked it                │
├───────────────────────────┼──────────┼──────────────────────┼─────────────────────────────────────────────────────┤
│ ade-bench-ana-eng004      │ ❌ FAIL  │ 🎯 want it to flip   │ Target — obt_product_inventory width flip attempt.    │
│ ade-bench-ana-eng002      │ ✅ PASS  │ ✅ must stay PASS    │ Perturbable OBT canary — SAME model as the target.    │
│ ade-bench-ana-eng002-med..│ ✅ PASS  │ ✅ must stay PASS    │ Perturbable OBT canary — SAME model as the target.    │
│ ade-bench-ana-eng005      │ ✅ PASS  │ ✅ must stay PASS    │ Perturbable OBT/wide canary — fact_inventory.         │
│ ade-bench-intercom001     │ ❌ FAIL  │ (reach-only read)    │ Secondary reach read — distance signal, not credited. │
│ ade-bench-intercom003     │ ❌ FAIL  │ (reach-only read)    │ Secondary reach read — distance signal, not credited. │
│ ade-bench-airbnb001       │ ✅ PASS  │ ✅ must stay PASS    │ Canary (airbnb family) — cross-family tripwire.       │
│ ade-bench-asana001        │ ✅ PASS  │ ✅ must stay PASS    │ Canary (asana family) — cross-family tripwire.        │
│ ade-bench-f1001           │ ✅ PASS  │ ✅ must stay PASS    │ Canary (f1 family) — h0023 bled this 6/6->2/6.        │
│ ade-bench-quickbooks002   │ ✅ PASS  │ ✅ must stay PASS    │ Canary (quickbooks family) — cross-family tripwire.   │
└───────────────────────────┴──────────┴──────────────────────┴─────────────────────────────────────────────────────┘
```

Net hoped-for: flip the 1 target (ana-eng004) while losing **zero** canaries/sentinels — honest prediction
is **{0} flips** (width-oracle wall), so the real win is the attribution read + distance, and a single
canary dropping FAIL is a NO-GO. ETA ≈ 10 tasks × ~9 min ≈ **90 min** (serial, `n_concurrent_trials=1`,
detached/nohup — no need to wait on-screen).
