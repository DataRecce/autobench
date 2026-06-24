---
id: dab0020
title: agnews-q4 - argmax margin-gate requiring two independent content signals to agree before committing
status: propose
kind: hypothesis
source: dab0006 ideate (integrity-safe stripped-label inference); forks spacedock-readme-baseline @baseline
started: 2026-06-22T10:46:00Z
score: 0.3
---

## Hypothesis

The @baseline failure on `agnews-q4` is a **thin-margin instability**, not an effort gap. The
@codex-batch-baseline trace commits **North America** (ground truth **Africa**) on a top ranking
bunched across the five regions within ~3% over ~6700 World articles — the leaders sit within a
single-digit-article margin of each other. At that margin a single noisy
content classifier's argmax is a coin-flip; the baseline even narrates "a close margin can be
overturned by boundary cases" and then commits anyway. The lever attacks the *decision under thin
margin*: when the leading group's lead is inside the noise band, the single-signal argmax must NOT
be trusted as-is.

Falsifiable claim: **a rule that, for a label-stripped category-inference ranking, computes TWO
independent content signals (a keyword-lexicon classifier AND a separate term-frequency / weighted
scorer) and requires them to AGREE on the winner before committing — widening the evidence (raise
the per-article assignment confidence threshold, drop no-signal articles) until they do — flips
`agnews-q4`.** The two signals are independent in *construction* (different scoring methods over
the same content), so agreement is a genuine cross-check, not one mind photocopied. If the two
signals agree on the wrong region, the content simply does not separate the regions and the
hypothesis is falsified (the margin is irreducibly within noise → README cannot fix it).

**The README change** (fork `spacedock-readme-baseline` -> `dab0020-argmax-margin-gate-dual-signal`),
ONE idea, in the `analyze` stage as a new precondition-gated checklist item:

> **Thin-margin category-inference gate.** *Trigger:* a ranking/argmax question over a category
> you had to **infer from text** (the category is not a column) AND the leading group's count is
> within 5% of the runner-up. When this triggers, do NOT commit the single-classifier argmax.
> Compute a SECOND, independently-constructed content signal — e.g. signal A = fixed-keyword hit
> count, signal B = TF-weighted category similarity — and:
> 1. If A and B agree on the top group, commit it.
> 2. If they disagree, the per-article assignments are noise-dominated: drop articles with no
>    strong category signal (raise the assignment threshold), recompute both signals, and re-test.
> 3. If they still disagree after the strongest defensible threshold, the data does not separate
>    the groups at this margin — report `"UNABLE TO DETERMINE"` rather than guessing a coin-flip.
> Record both signals' per-group tables in `_artifacts/reasoning.md`.

This is a check-and-widen rule, NOT a self-anchored "re-run your own query and trust it" — the two
signals are separately *constructed* methods (G6/G10 independence-by-different-method).

## Targets

- **PRIMARY flip — agnews-q4**: flip to PASS. Acceptance = committed region is the one BOTH signals
  agree on (shown in `_artifacts/reasoning.md` as two distinct per-region tables), OR a defensible
  `"UNABLE TO DETERMINE"` if they cannot agree (knowledge gain: proves the margin is irreducible).
- **Canaries to hold**: bookreview-q1, stockindex-q3, music_brainz_20k-q1 (gate must not fire —
  none are label-stripped category questions, so the 5% margin clause never triggers).

## Acceptance criteria (falsifiable)

- **GO** iff agnews-q4 flips to PASS by committed artifact with two distinct content-signal tables
  shown AND no canary regresses.
- **NO-GO / falsified** if the two signals agree on the WRONG region (content does not separate the
  groups — closes the dual-signal sub-family for this query) OR the rule degenerates to
  `"UNABLE TO DETERMINE"` while a deterministic classifier (dab0019) would have flipped it (the
  margin gate is over-cautious — favors dab0019) OR a canary regresses (gate mis-scoped → REVISE).
- **Relationship to dab0019:** dab0019 makes the single classifier deterministic; dab0020 adds a
  cross-signal agreement gate. If dab0019 flips alone, dab0020's second signal is redundant; if
  dab0019 lands on a wrong-but-stable region and dab0020's agreement test catches it, the
  cross-check is load-bearing. Either way the comparison sharpens the inference contract.

## Leak-guard (integrity, G2)

No access to `ground_truth.csv` / `expected_*` / `answer_key` / `gold` / `db_description_withhint.txt`;
no external fetch/clone/lookup; existing no-external-reference prose byte-identical. Both signals are
computed from in-workspace `title`/`description` content only. **Inference proof at smoke:** the
committed `_artifacts/reasoning.md` carries TWO independently-constructed per-region tables; the
`verify` external-oracle audit finds no oracle/hint/HF read in the analyze trace.

## Smoke set

| Task | Baseline | Should-pass after lever | Role |
|---|---|---|---|
| agnews-q4 | ❌ FAIL | 🎯 PASS (both signals agree) or defensible UNABLE | primary flip |
| agnews-q3 | ❌ FAIL (business-articles/year, also inferred category) | hold/observe | secondary observe |
| bookreview-q1 | ✅ PASS | ✅ PASS (gate must NOT fire) | gate-scope canary |
| stockindex-q3 | ✅ PASS | ✅ PASS (gate must NOT fire) | gate-scope canary |

Net target: +1 (agnews-q4) with zero canary regression; ETA ~1 dataset smoke.

## Gatekeeper review

**Recommendation: APPROVE** — clean single-stage gated lever; integrity rules (G2/G3/G6) all PASS; one G10 WARN on second-signal independence (both signals re-derive from the same title/description text).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-24T03:03:42Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs parent `spacedock-readme-baseline-hostfix` adds ONE block (207a208-229) in the `analyze` stage only — the "Thin-margin category-inference gate" checklist item; no other stage, no leak-guard prose touched. |
| G2 leak-guard intact | PASS | grep over added `>` lines for `ground_truth`/`db_description_withhint`/`curl`/`wget`/`git clone`/`expected_*`/`answer_key`/`gold`/`huggingface`/`hf://` = NONE FOUND. Rules + "Use only the workspace data" block byte-identical to parent (diff empty). Both signals computed from in-workspace title/description only. |
| G3 spec two fields | PASS | Diffed vs the TRUE fork parent `specs/codex-dab-batch-baseline.yaml` (batch lineage), not dab-anchor-codex. Only substantive changes: `experiment:` (→dab0020-...) and `solver_workflow:` (→./solver_workflows/dab0020-...); ABOUTME comments cosmetic. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` all preserved. |
| G4 smoke tasks+exclude | PASS | Smoke diff adds ONLY `benchmark.tasks` (agnews, bookreview, stockindex — dataset names) + `benchmark.exclude_tasks` (6 q-ids). Nothing else differs (ABOUTME cosmetic). Surviving set = agnews-q3, agnews-q4, bookreview-q1, stockindex-q3 — the named PRIMARY target **agnews-q4 survives**. (rk --explain not run per gatekeeper constraints; surviving set derived from exclude_tasks.) |
| G5 both frozen | PASS | Both `…frozen.yaml` and `…smoke.frozen.yaml` exist (1871/1823 bytes); each carries `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim verbatim-in-spirit: same `analyze` stage, dual independent content signals (keyword-hit + TF-weighted) must AGREE before commit, widen-threshold-then-UNABLE-TO-DETERMINE fallback. Generative/independent in form (constructs two scoring methods), not self-anchored "re-run your own query and trust it"; no scope creep beyond the gate. |
| G7 actionability/inert-risk | WARN | Instruction class = abstract-structural (asks the solver to construct two scoring methods — "fixed-keyword hit count", "TF-weighted category similarity" — and a thresholding/widen loop) WITHOUT a worked-example skeleton or copyable SQL/Python. Inert-risk at gpt-5.5: solver may narrate the gate but commit the single-classifier argmax anyway. Suggest a worked-example skeleton for both signal computations. |
| G8 regression-canary coverage | N/A (PASS) | Lever is PRECONDITION-GATED (fires only when category was text-inferred AND top margin within 5%), NOT generative — does not fire on every query. Canary regression structurally bounded to gates that mis-fire; smoke still carries 2 non-target passers (bookreview-q1, stockindex-q3) as gate-scope canaries. |
| G9 selector independence | N/A (PASS) | Not a multi-candidate run-N-and-select protocol — it does not spawn N candidate sessions and pick one. It computes two scoring signals within the single analyze session and gates the commit on their agreement. Selector-independence axes do not apply. |
| G10 self-correcting false-positive | WARN | Self-correcting (check second signal, act on disagreement). (a) Scope: gated to the 5%-margin + text-inferred precondition — does NOT fire on already-clean/clear-margin queries (good). (c) Check-don't-replace: fallback is widen-threshold → UNABLE TO DETERMINE, not a mandate to swap in a "structurally different" query (good). (b) Independence source: BOTH signals read the SAME title/description content, scored by two methods — separately *constructed* but re-derived from the same source, not a separately-sourced raw signal. Different-method-same-content agreement can re-correlate (both wrong the same way when the content genuinely doesn't separate the regions), giving a false-green. The hypothesis acknowledges this as its own falsification condition ("if the two signals agree on the WRONG region … the margin is irreducible"), so the design fails SAFE rather than committing a confident wrong answer. WARN, not FAIL: gated (axis a) + check-don't-replace (axis c) both clear; only axis-(b) independence is correlated-re-derivation rather than separately-sourced. |

**For the captain:** No FAILs → advances to smoke. Two WARNs to weigh: (G7) the dual-signal computation is abstract prose with no worked-example skeleton — high inert-risk at gpt-5.5 (the solver may discuss the gate but commit the single argmax); consider asking the ensign to add copyable signal-A/signal-B skeletons before smoke. (G10) the two "independent" signals both re-derive from the same title/description text — not double-entry from a different source, so agreement can be correlated-wrong; this is exactly the dab0020-vs-dab0019 question the hypothesis poses, and the UNABLE-TO-DETERMINE fallback makes it fail safe. Smoke should confirm agnews-q4 either flips with two genuinely-divergent per-region tables in `_artifacts/reasoning.md` or yields a defensible UNABLE (not a coin-flip commit), and that the gate does NOT fire on bookreview-q1 / stockindex-q3.

## Stage Report: propose

- DONE: Read dab0020-argmax-margin-gate-dual-signal.md fully; verify AC-0.
  Single-knob (one analyze-stage gated checklist item), target named (agnews-q4 PRIMARY flip); entity well-formed.
- DONE: BATCH lineage fork; edit ONLY README.md to add the single lever; leak-guard byte-intact.
  cp from solver_workflows/spacedock-readme-baseline-hostfix; diff = pure addition 207a208-229 (the "Thin-margin category-inference gate" block); no forbidden tokens in added lines.
- DONE: Full spec from codex-dab-batch-baseline.yaml; experiment + solver_workflow only.
  diff vs codex-dab-batch-baseline.yaml = only experiment:, solver_workflow:, ABOUTME; query_mode:batch, workspace_variant:spacedock, reasoning_effort:high preserved.
- DONE: Smoke spec adds benchmark.tasks + exclude_tasks; gated lever → lighter canary set.
  tasks=agnews,bookreview,stockindex; exclude=agnews-q1/q2,bookreview-q2/q3,stockindex-q1/q2 → surviving scored set = agnews-q4(target)+agnews-q3(observe)+bookreview-q1+stockindex-q3 canaries. Lever is PRECONDITION-GATED (not generative), so no full G8 panel required.
- DONE: export RAZORBACK_REGISTRY + RAZORBACK_SPACEDOCK_PLUGIN_DIR; freeze both.
  wrote dab0020-...frozen.yaml + .smoke.frozen.yaml; both carry kind:spacedock_solver, runtime:codex.
- DONE: Verify smoke selection via --explain.
  Tasks: 3 (agnews, bookreview, stockindex); lever present in composed prompt (line 297). exclude_tasks survives freeze; surviving scored cells = the 4 expected.
- DONE: Run gatekeeper subagent; write ## Gatekeeper review block.
  Recommendation APPROVE (no FAILs); G7 WARN (abstract-structural, inert-risk) + G10 WARN (both signals re-derive same title/description content — correlated-wrong risk, fails safe via UNABLE-TO-DETERMINE). G8/G9 N/A (gated, not selector).
- DONE: STOP at propose gate; report to FO.
  No rk run beyond --explain launched. Findings below.

### Summary
Forked the batch baseline (spacedock-readme-baseline-hostfix) into dab0020 with ONE added analyze-stage gated checklist item — the thin-margin dual-signal argmax gate — and built/froze full + smoke specs differing only in the allowed fields. Gatekeeper APPROVE with two advisory WARNs (G7 inert-risk: no worked-example skeleton; G10: the two "independent" signals re-derive from the same title/description text, so agreement can be correlated-wrong, but the design fails safe). NOTE: the @codex-batch-baseline agnews-q4 trace committed "North America" (truth "Africa"); the hypothesis body has been corrected (it previously cited "South America" with an unverified count ranking) — the thin-margin framing is unchanged.
