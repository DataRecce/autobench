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

## Smoke result

## Run result

## Behavioral analysis

## Verdict
