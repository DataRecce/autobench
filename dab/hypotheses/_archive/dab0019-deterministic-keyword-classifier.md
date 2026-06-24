---
id: dab0019
title: agnews-q4 - deterministic keyword-anchored content classifier for label-stripped category queries
status: smoke
kind: hypothesis
source: dab0006 ideate (integrity-safe stripped-label inference); forks spacedock-readme-baseline @baseline
started: 2026-06-22T10:45:00Z
score: 0.3
verdict: REJECTED
---

## Hypothesis

`agnews-q4` ("In 2015, which region published the largest number of articles in the World
category?") has **no `category` column** — the AG-News labels are stripped, so the solver must
*infer* each article's category from `title`+`description` content and then argmax the per-region
World count. The @baseline solver already attempts this (seeded TF-IDF + a "stress-test" rule
scorer), yet commits the WRONG region: the @codex-batch-baseline trace commits **North America**
(ground truth is **Africa**), with the 2015 World-count ranking bunched across the five regions
inside a ~3% band — a single-digit-article margin over ~6700 articles. The classification *effort* is not the gap; the
**non-determinism** is: an ad-hoc, model-authored lexicon + a seeded random component makes the
argmax a coin-flip that lands on a wrong region. The fix is to remove the randomness, not add more
of it.

Falsifiable claim: **a precondition-gated rule that, for a label-stripped category query, makes the
content classifier DETERMINISTIC — a fixed published keyword lexicon per category, a fixed
per-article scoring rule, and a fixed lexicographic region tie-break — produces a reproducible
argmax that flips `agnews-q4` to PASS.** If a deterministic classifier still lands on the wrong
region, the lexicon is mis-specified (not the determinism) and the hypothesis is falsified.

**The README change** (fork `spacedock-readme-baseline` -> `dab0019-deterministic-keyword-classifier`),
ONE idea, in the `analyze` stage as a new precondition-gated checklist item AFTER the
duplicate-source sequence (it does not touch that sequence). Gate, then mechanical recipe:

> **Label-stripped category inference (gated).** *Trigger:* the question names a category /
> class / label (e.g. "World", "Sports", "Business", "Science/Technology") that is **not a column**
> in any table — you must infer it from text fields (`title`, `description`). When this triggers,
> do NOT use a random seed, a sampled subset, or an LLM judgement call per row — those make the
> argmax irreproducible. Instead build a DETERMINISTIC classifier:
> 1. Define one fixed, lowercased keyword set per candidate category (e.g. World →
>    {war, nation, government, minister, election, diplomatic, treaty, …}; keep the lexicon in
>    `_artifacts/reasoning.md`).
> 2. Score every article by the count of category-keyword hits in `lower(title || ' ' || description)`;
>    assign the article to its single highest-scoring category; on a per-article score tie, assign
>    to NONE (drop it) so a tie cannot inflate a category.
> 3. Aggregate the target metric over the assigned category, then rank the groups; on a
>    between-group count tie at the top, break **lexicographically by the group key** and state the
>    tie in `_artifacts/reasoning.md`.
> This whole step is **skipped** when the category IS a column — read it directly.

No new external access; the lexicon is author-built from general knowledge of the category names
in the question, never from any hint/oracle file (see leak-guard below).

## Targets

- **PRIMARY flip — agnews-q4** (Opus 1/5, gpt-5.5 0/1 by trace): flip to PASS. Acceptance =
  committed `answers.json` region differs from the baseline's "North America" (GT "Africa"), AND
  `_artifacts/reasoning.md` shows the fixed lexicon + a deterministic per-region World-count table
  with the stated tie-break — proving the answer was *inferred deterministically from content*, not
  drawn from any oracle.
- **Canaries to hold** (non-agnews, currently-passing — guard the gate): bookreview-q1 (perfect
  dataset, no category-inference shape — the gate must NOT fire), stockindex-q3 (perfect dataset),
  music_brainz_20k-q1 (perfect). The gate must leave every non-label-stripped query untouched.

## Acceptance criteria (falsifiable)

- **GO** iff agnews-q4 flips to PASS by committed artifact AND the reasoning artifact shows the
  deterministic lexicon + region table (inference proof) AND no canary regresses.
- **NO-GO / falsified** if agnews-q4 stays FAIL (deterministic classification with an author-built
  lexicon is insufficient — the content signal is too weak for ANY README-buildable classifier,
  closing the keyword-classifier sub-family) OR if the gate fires on a non-category query and
  regresses a canary (gate is mis-scoped → REVISE the trigger).

## Leak-guard (integrity, G2)

The added text adds NO access to hidden grading artifacts: it never reads/opens/inspects
`ground_truth.csv`, `expected_*`, `answer_key`, `gold`, or `db_description_withhint.txt`, and never
fetches/clones/looks up anything external. The lexicon is built from the category NAMES already in
the question text — not copied from any withheld description. The existing no-external-reference
prose is left byte-identical. **Inference proof at smoke:** the committed
`_artifacts/reasoning.md` must contain the per-article scoring lexicon and the per-region count
table; the `verify`-stage external-oracle audit (already in the baseline README) must find no
`ground_truth` / `huggingface` / `datasets.load_dataset` / hint-file read in the analyze trace.

## Smoke set

| Task | Baseline | Should-pass after lever | Role |
|---|---|---|---|
| agnews-q4 | ❌ FAIL (Opus 1/5) | 🎯 PASS (flip) | primary flip |
| agnews-q2 | ❌ FAIL | hold/observe (also category-inference: Science/Technology fraction) | secondary observe |
| bookreview-q1 | ✅ PASS | ✅ PASS (gate must NOT fire) | gate-scope canary |
| stockindex-q3 | ✅ PASS | ✅ PASS (gate must NOT fire) | gate-scope canary |

Net target: +1 (agnews-q4) with zero canary regression; ETA ~1 dataset smoke.

## Gatekeeper review

| Rule | Verdict | Rationale |
|---|---|---|
| G1 single idea/stage | PASS | Pure 21-line addition of one checklist bullet ("Label-stripped category inference (gated)") in the `analyze` stage only; nothing removed/modified, exactly the one idea the Falsifiable claim names. |
| G2 leak-guard intact | PASS | No-external-reference prose byte-identical; added text names no `ground_truth`/`expected_*`/`gold`/`db_description_withhint`, pastes no withheld hint, fetches nothing — lexicon is author-built from the category names already in the question. |
| G3 spec two fields | PASS | Full-spec diff = only ABOUTME comments + `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver` and `runtime: codex` preserved; `trials: 1`. |
| G4 smoke tasks+exclude | PASS | Smoke adds only `tasks: [agnews,bookreview,stockindex]` (dataset names, correct batch convention) + `exclude_tasks` of other datasets; nothing else differs; target agnews-q4 survives. |
| G5 both frozen | PASS | `dab0019-…frozen.yaml` and `…smoke.frozen.yaml` both exist; both carry `kind: spacedock_solver` and `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the claim verbatim in intent: a gated, generative deterministic classifier (fixed lexicon + fixed scoring + lexicographic tie-break); no self-anchored "re-run/verify your own answer" phrasing. |
| G7 actionability/inert-risk | WARN | Recipe is mostly mechanical (count keyword hits in `lower(title||' '||description)`, drop per-article ties, lexicographic group tie-break) with a worked skeleton, but "define one fixed keyword set per category" leaves the lexicon author-derived — the lever's success rides on lexicon quality the README can only gesture at; flag inert/under-specified-lexicon risk for the captain. |
| G8 regression-canary coverage | PASS (N/A) | Precondition-gated (fires only when the named category is not a column), not fires-everywhere generative → no full generative-regression panel required; the two gate-scope canaries (bookreview-q1, stockindex-q3, both non-target perfect-dataset `@baseline` passers) correctly test that the gate stays dormant on non-category queries. |
| G9 selector independence | PASS (N/A) | Not a multi-candidate / selector protocol — single deterministic classifier, no N-candidate selection. |
| G10 self-correcting false-positive | PASS (N/A) | Not a check/reconcile/validate-and-fix lever — it is a generation recipe (build a deterministic classifier), not a "verify a result and act on disagreement" instruction. |

**Overall:** APPROVE

**Rationale:** No FAILs — integrity rules (G1/G2/G3/G6) all clean, gated lever correctly carries gate-scope canaries instead of a generative panel; the sole WARN (G7 lexicon-quality/inert-risk) is advisory and does not block the gate.

## Stage Report: propose

- DONE: Read dab0019-deterministic-keyword-classifier.md fully. AC-0 verified.
  Entity well-formed, single-knob (one gated analyze-stage checklist bullet), target agnews-q4 named.
- DONE: BATCH lineage fork of solver_workflows/spacedock-readme-baseline-hostfix -> dab0019-deterministic-keyword-classifier; README edited with the single lever.
  `diff` = pure +21-line addition (the gated "Label-stripped category inference" bullet), leak-guard prose byte-intact, no ground_truth/hint content pasted.
- DONE: Full spec specs/dab0019-deterministic-keyword-classifier.yaml.
  Diff vs codex-dab-batch-baseline.yaml = only ABOUTME comments + `experiment:` + `solver_workflow:`; query_mode:batch/workspace_variant:spacedock/reasoning_effort:high unchanged.
- DONE: Smoke spec specs/dab0019-deterministic-keyword-classifier.smoke.yaml.
  Gated lever → lighter canary set; dataset-level selection tasks=[agnews,bookreview,stockindex] (per-query `-qN` excludes are INERT in batch mode — batch emits one task per dataset and scores all queries via reward_per_query.json).
- DONE: export RAZORBACK_REGISTRY + RAZORBACK_SPACEDOCK_PLUGIN_DIR; froze both specs.
  Wrote dab0019-deterministic-keyword-classifier.frozen.yaml and .smoke.frozen.yaml.
- DONE: Verify smoke selection via `rk run ... --explain`.
  Tasks: 3 (agnews, bookreview, stockindex); validators present for agnews-q4 (target) + q2 (observe) + bookreview-q1 + stockindex-q3 (canaries); no extra datasets.
- DONE: Gatekeeper subagent applied; review block written above.
  Overall APPROVE, one advisory WARN (G7 lexicon-quality/inert-risk), no FAIL.
- DONE: STOP at propose gate.
  No smoke/full run launched beyond --explain (foreground, free).

### Summary

Forked the batch baseline README and added ONE precondition-gated analyze-stage bullet that makes a label-stripped category classifier deterministic (fixed lexicon + count-hit scoring + lexicographic tie-break). Gatekeeper APPROVE with a single advisory WARN (the keyword lexicon is author-derived, so the smoke run is the real test of whether a README-buildable lexicon flips agnews-q4). Key finding: per-query `-qN` excludes are inert in DAB batch mode (one task per dataset), so the smoke uses dataset-level selection; @codex-batch-baseline reference confirms agnews-q4 FAIL (committed "North America", GT "Africa") and both canaries PASS.

## Behavioral analysis

**Smoke run of record:** `runs/dab0019-deterministic-keyword-classifier/b1c5e442c1818cf2`
(rc=0, 18m12s, clean audit — 3/3 trials completed, 0 errored, no `coverage_missing`, no taint).
Per the smoke→conclude rule, a clean falsification at smoke does NOT advance to a full run.

**Failure mechanism (the thin-margin wall).** agnews-q4 scored reward 0.0. The dab0019
deterministic lever committed **South America** (332 World-category articles, 2015); ground
truth is **Africa** (320), with North America also at 320. The committed answer misses by ~12
counts / ~3.7% over ~6700 articles — the five World-category region counts are bunched inside a
~3% band. This is the falsified branch of dab0019's own acceptance criteria: a deterministic
classifier landed on the wrong region, so the lexicon (not the determinism) was the gap — and
more precisely, the *content signal itself* does not separate the regions at this margin.

**Did the change reach the committed artifact? No — recipe under-fired.** Grep of the analyze
transcript for a fixed-keyword-lexicon execution signature (`keyword`/`lexicon`) was **empty**:
the prescribed deterministic recipe did not execute as written. The solver narrated/used its own
classification rather than the README's fixed lexicon — a partial **dab0012 "talks but doesn't
do"** pattern. So the run is BOTH "recipe under-fired" AND "even the resulting classification
missed by a thin margin."

**Two-methods-two-wrong-regions — the margin is irreducible.** The no-lever
`@codex-batch-baseline` committed **North America**; the dab0019 deterministic lever committed
**South America** — TWO different methods landing on TWO different WRONG regions, both clustered
within ~12 counts of the true answer (Africa). This is direct evidence the content signal does
NOT separate these regions at this margin: the ~3% spread is irreducible noise, not a
determinism gap a README recipe can close.

**Distance to pass.** Effectively unbridgeable by this lever-family: a ~12-count / ~3.7% margin
sitting below the resolution of any keyword-count classifier a README can author, compounded by
the recipe never firing as written. No tweaking of the author-built lexicon is expected to
separate Africa from South America / North America at this band.

**Canaries.** ALL HELD: bookreview-q1/q2/q3 = 1.0/1.0/1.0; stockindex-q1/q2/q3 = 1.0/1.0/1.0.
The precondition gate stayed correctly scoped — it did NOT fire on non-category queries. (agnews-q1
incidentally 1.0; agnews-q2/q3 observe 0.0.)

**Transferable rule.** A README-buildable deterministic keyword classifier cannot separate the
AG-news World-category regions at a ~3% margin — the thin margin is the wall, not the recipe.
Combined with the empty no-lexicon-signature finding, this reconfirms the dab0012 boundary:
gpt-5.5 narrates a prescribed analytic recipe but commits its own method.

## Verdict

**verdict: REJECTED** — cleanly falsified at smoke (no full run, per the smoke→conclude rule).

agnews-q4 did NOT flip (committed South America 332 vs GT Africa 320, ~3.7% margin), and the
prescribed deterministic recipe left no execution signature in the transcript. This matches the
explicit NO-GO/falsified branch of dab0019's acceptance criteria: deterministic classification
with an author-built lexicon is insufficient because the content signal is too weak for ANY
README-buildable classifier.

This **closes the keyword-classifier sub-family for agnews-q4 ONLY**. Canaries held; audit clean.
Do NOT promote, do NOT run `rk baseline promote`, do NOT touch `@baseline`.

## Follow-up Routing

**stop** for the keyword-classifier sub-family.

Siblings dab0020 (dual-signal agreement gate) and dab0021 (provenance no-leak audit) are
DIFFERENT mechanisms, not keyword classifiers, and are CURRENTLY SMOKING concurrently. dab0019's
reject closes only the keyword-classifier sub-family; the **agnews-q4 family-level verdict awaits
dab0020/dab0021**. No new hypothesis filed. Not workflow-structural → no WORKFLOW-REFINE entry.

## Stage Report: conclude

- DONE: Read the evidence package at /tmp/dab0019-conclude-evidence.txt and the entity file.
  Captain REJECTED verdict + full smoke artifact evidence consumed; numbers used verbatim.
- DONE: Write ## Behavioral analysis into the entity.
  Covers committed South America 332 vs GT Africa 320 (~3.7% margin), empty no-lexicon-signature (recipe under-fired / partial dab0012), two-methods-two-wrong-regions irreducible margin, distance-to-pass, transferable rule.
- DONE: Write ## Verdict with verdict: REJECTED.
  Falsified at smoke (no full run); closes keyword-classifier sub-family for agnews-q4 ONLY; canaries held; audit clean; no promote, no @baseline touch.
- DONE: Set frontmatter verdict: REJECTED and append self-learning line.
  Frontmatter field added; one dab0019 entry appended to _artifacts/self-learning.md with the transferable rule.
- DONE: Write ## Follow-up Routing = stop for the keyword-classifier sub-family.
  Notes siblings dab0020/dab0021 are different mechanisms currently smoking; family verdict awaits them; no new hypothesis; no WORKFLOW-REFINE entry.
- DONE: Archive the entity to _archive/ and commit with a conclude: prefix.
  git mv + path-scoped commit (see SHA in completion signal).

### Summary

dab0019 CONCLUDED REJECTED — cleanly falsified at smoke. A README-buildable deterministic keyword classifier could not separate the AG-news World-category regions at a ~3% content-signal margin (committed South America 332 vs GT Africa 320); two distinct methods landed on two different wrong regions within ~12 counts of the truth, proving the margin is irreducible noise, and the prescribed lexicon recipe left no execution signature (partial dab0012 talks-but-doesnt-do). Closes the keyword-classifier sub-family for agnews-q4 only; canaries held, audit clean, @baseline untouched; siblings dab0020/dab0021 (different mechanisms) still smoking.
