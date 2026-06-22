---
id: dab0022
title: Semi-structured data rules — parser-first / all-associated / full-list discipline to flip the 3 newly-resolvable PATENTS queries
status: smoke
kind: hypothesis
source: Captain-directed. Upstream updated the ground truth + verifier for ALL 3 PATENTS queries — PATENTS is no longer an unresolvable dataset (it scored 0/3 in dab0018-full3 against the old/broken oracle). This files the first hypothesis to attack the now-scorable PATENTS cells with an explicit semi-structured-data-handling README section.
started: 2026-06-22T10:37:17Z
completed:
verdict:
score: 0.5
worktree:
---

## Hypothesis

Adding a single coherent **`### Semi-structured data rules`** section to the solver README —
a parser-first / exact-identifier / all-associated-values / full-list / explicit-graph-traversal /
pre-finalize-verification-table discipline — flips the 3 newly-resolvable **PATENTS** queries
(PATENTS-q1, PATENTS-q2, PATENTS-q3) from FAIL to PASS without regressing the rest of the board.

**The single README change** (fork `solver_workflows/spacedock-readme-baseline-hostfix` — the
`@codex-batch-baseline` solver — and add this one section verbatim; change nothing else):

```
### Semi-structured data rules

- If key facts live inside free-text or JSON-like fields, first write a parser/profiler for those fields before answering. Report parse coverage and sample failures.
- When an entity identifier appears in multiple textual forms, use exact field values by default. Merge variants only if the schema or data gives an explicit shared key.
- For hierarchy-coded dimensions, verify the meaning of each level from the dimension table before filtering or grouping. Do not infer level from code length alone unless confirmed.
- If a question says “associated with”, “classified by”, or otherwise does not say “primary”, use all associated values, not only a primary/default entry.
- For time-series metrics, build the full time axis before computing rolling or exponential metrics. Fill missing periods with zero unless the question or schema says otherwise.
- For “best year”, “peak”, or ranking over a derived metric, show the neighborhood around the winner and preserve ties unless the question asks for one winner.
- For complete-list questions, emit every qualifying row. Do not truncate to top-k unless the question explicitly asks for top-k.
- For graph questions involving citations, references, dependencies, parent/child, or links: identify source nodes, traverse edges explicitly, then apply exclusions after traversal.
- Before finalizing, write a small verification table: input cohort count, parsed-row count, joined-row count, distinct output entities, and final output count.
- Format final answers as simple records with exact database values for names/titles/codes; avoid nested commentary.
```

**Target queries:** PATENTS-q1, PATENTS-q2, PATENTS-q3 (all 3 in the dataset).

**Lever class — GENERATIVE (NOT gated).** Every rule above fires on every query that matches its
shape (parsers, identifiers, hierarchy codes, time-series, ranking/peak, complete-list, graph
traversal, the verification table, final formatting), not just on PATENTS. Per the DAB calibration
lessons (dab0017/dab0016: a generative fires-everywhere lever adds ±0.07 board variance and its
smoke is NOT predictive of the full board), this lever can regress *anywhere it fires* — so propose
MUST build a regression panel (gatekeeper G8): ≥1 currently-passing query from a non-PATENTS
dataset + ≥2 *perturbable* canaries from the dataset whose query shape these rules most likely
perturb (ranking / complete-list / free-text-parse shapes — e.g. stockmarket, googlelocal, yelp).

## Pre-smoke Decision-Fork Probe

**Skipped — oracle-newly-unblocked, no local fork.** PATENTS was previously *unresolvable* (the
ground truth/verifier was broken, so the 0/3 at the anchor is an artifact of the old oracle, not a
diagnosed solver failure). There is no prior committed-artifact fork to probe because no PATENTS
result was ever scorable. The smoke run itself is the first real read on these queries against the
new oracle; a decision-fork probe would have nothing valid to fork against. (If smoke surfaces a
specific committed-artifact fork on a still-failing PATENTS query, a probe becomes meaningful for
any `smoke → hypothesis` revision.)

## Acceptance criteria (falsifiable)

**AC-0 — Anchor reflects the NEW PATENTS oracle (must verify at propose, BEFORE trusting any
delta).** The `@codex-batch-baseline` PATENTS cells were originally scored against the OLD/broken
verifier (0/3). Commit `94a87c2` rescored the anchor against the latest ground-truth + verifier —
propose MUST confirm the resolved `@baseline` (`export RAZORBACK_REGISTRY=…; rk registry resolve
run @baseline`) is the rescored run and read its PATENTS per-query baseline from the NEW oracle.
If the anchor still carries old-oracle PATENTS scores, the comparison is invalid and the run must
re-baseline first.

**AC-1 — README change + one captain-directed effort change; full spec differs from the anchor in
THREE fields.** Verified by `diff specs/codex-dab-batch-baseline.yaml
specs/dab0022-patents-semistructured-rules.yaml`. The solver README diff vs its parent
(`spacedock-readme-baseline-hostfix`) adds ONLY the `### Semi-structured data rules` section;
leak-guard prose byte-intact.

> **CAPTAIN DIRECTIVE (2026-06-22) — third spec delta authorized.** The captain directed this run to
> use `agent.reasoning_effort: xhigh` (the batch anchor uses `high`). So the dab0022 full spec
> intentionally differs from `specs/codex-dab-batch-baseline.yaml` in **three** fields —
> `experiment:`, `solver_workflow:`, AND `agent.reasoning_effort:` (high→xhigh) — confirmed by the
> diff above (only those three lines change; `kind: spacedock_solver` + `runtime: codex` preserved).
> This is a **captain-authorized intentional change, NOT a leak/spec fault** — the standard "only two
> fields" reject-check is overridden for this entity by explicit directive.
>
> **METHODOLOGICAL CONFOUND (must carry to the verdict).** Because effort ALSO changed, the README is
> no longer the *only* variable vs the `high` anchor. A PATENTS flip therefore **cannot be cleanly
> attributed to the README alone** against the registered `@codex-batch-baseline` (which is `high`) —
> the flip could be the README, the xhigh effort, or their interaction. Clean attribution requires an
> **xhigh baseline** (same solver-README-minus-the-section at xhigh) to isolate the README; without
> it, AC-3's "README genuinely isolated" claim is weakened to "README + effort jointly isolated vs a
> high anchor." Flag this at smoke→full and again at the verdict.
>
> **PRIOR-LEARNING CAVEAT — the xhigh-hurts-gpt5.5 paradox.** Per the DAB behavioral model
> (`[[dab-opus-vs-gpt55-behavioral-model]]`), `xhigh` has historically *HURT* gpt-5.5 on DAB (more
> reasoning → more abstention / over-elaboration, not more accuracy). So xhigh is a double-edged
> directive: it may help PATENTS' heavy multi-join graph/EMA reasoning, but it may also *depress the
> regression-panel canaries* independent of the README. A canary drop at smoke must be read against
> this — it may be an effort side-effect, not a generative-README side-effect.

**AC-2 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict` on
the same run-dir; `0 coverage_missing`, `0 tainted`).

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`, with the codex-vs-Opus
confound attributed via the committed-artifact read** (does the README rule reach the committed
answer on each flipped PATENTS query, vs a flip the model swap would produce regardless). Note the
anchor `@codex-batch-baseline` is the SAME codex/gpt-5.5 model, so on PATENTS the model is held
constant and the README is genuinely isolated. **AMENDED per the AC-1 captain directive:** the model
is held constant but `reasoning_effort` is NOT (anchor `high` vs this run `xhigh`), so the README is
isolated *jointly with effort*, not alone — see the AC-1 confound note. Treat a PATENTS flip as
"README+xhigh vs high-anchor" until an xhigh-minus-section baseline disambiguates.

**GO** iff ≥1 of the 3 PATENTS queries flips FAIL→PASS by committed-artifact evidence AND zero
canary/sentinel regression on the regression panel (stratified Pass@1 not dragged below
`@baseline` by a generative side-effect). **NO-GO / REJECTED** if the rules are inert on PATENTS
(discussed-not-done), if PATENTS flips are model-swap-attributable rather than README-driven, or if
the generative lever regresses other datasets enough to net flat/negative.

## AC-0 verification — anchor reflects the NEW PATENTS oracle (PASS)

Resolved at propose (`export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml`):

- `@baseline` → `runs/opus-4-8-baseline/e14e49869e6412de` (Opus-4.8 incumbent, 0.6536) — the *headline*
  champion, but NOT the comparison anchor for this PATENTS lever.
- `@codex-batch-baseline` → `runs/codex-dab-batch-baseline/bf113446fdd94373` (draw2, codex/gpt-5.5,
  stratified 0.6966) — **the fork parent and the isolated-comparison anchor** (same codex model held
  constant on PATENTS, so the README is the only moving variable — AC-3).

**Rescore commit `94a87c2` confirms the anchor PATENTS cells ARE the new-oracle scores** (read from
`dab/tools/rescore-result.json` + `dab/docs/rescore-codex-batch-baseline-latest-gt-2026-06-22.md`):
the registered draw2 anchor recovers its committed `answers.json`, cross-checks against the stored
`reward_per_query.json`, and scores under the **production `verify_batch.py` + latest ground truth**:

| query | anchor reward (NEW oracle) | failure mode (per rescore doc) |
|-------|----------------------------|--------------------------------|
| PATENTS-q1 | **0.0** | wrong CPC set / level-5 best-year=2022 selection |
| PATENTS-q2 | **0.0** | wrong code-year (Germany H2-2019 EMA, level-4) |
| PATENTS-q3 | **0.0** | wrong assignee↔CPC-subclass-title (UNIV CALIFORNIA citation graph) |

The latest ground-truth regeneration **flips zero recoverable cells** (0.6966 → 0.6966); PATENTS=0/3
is a genuine **content** failure under the valid new verifier, NOT a verifier-crash artifact. (The
"broken oracle" effect was only on the *non-registered* draw1, where the old runner's missing
per-query try/except crash-dropped PATENTS entirely and inflated it to an 11-dataset 0.6963; razorback
PR #19's crash-guard un-hid it at 0/3 → honest 0.638. The registered draw2 anchor was never affected.)

**Verdict: AC-0 PASS — the comparison is valid.** The anchor carries new-oracle PATENTS scores (0/0/0);
no re-baseline needed. dab0022 attacks 3 genuinely-failing content cells with the model held constant.

## Gatekeeper review

_Re-run (cycle 2) after the CAPTAIN DIRECTIVE set `reasoning_effort: xhigh` and both specs were re-frozen. This supersedes the cycle-1 two-field review; the diff now legitimately shows three fields and G3 is ruled PASS under captain-override._

**Recommendation: APPROVE** — no FAILs: clean fork with the README addition matching the claim, leak-guard byte-intact, both specs frozen with kind/runtime preserved, abundant perturbable canary panel. The full spec now differs in THREE fields (`experiment:`, `solver_workflow:`, `reasoning_effort:` high→xhigh); per the recorded CAPTAIN DIRECTIVE in AC-1 the effort delta is authorized, so G3 does NOT fail on the third field — but it introduces a methodological confound and the xhigh-hurts-gpt5.5 prior caveat, both carried to the captain note. G7 inert-risk WARN stands.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-22T11:42:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is a single pure addition `88a89,101` — one `### Semi-structured data rules` block in the analyze/methodology section; no other stage touched, no leak-guard prose edited. (README unchanged since first review.) |
| G2 leak-guard intact | PASS | Added-line grep for `ground_truth`/`db_description_withhint`/`curl`/`wget`/`git clone` = NONE FOUND; diff is addition-only so all parent leak-guard paragraphs are byte-identical. |
| G3 spec fields | PASS (captain-override) | Full-spec diff vs `codex-dab-batch-baseline.yaml` now changes THREE fields: `experiment:`, `solver_workflow:`, AND `reasoning_effort:` (high→xhigh), plus the ABOUTME comment. The guideline's "exactly two fields / FAIL on any third" is OVERRIDDEN for this entity by the recorded CAPTAIN DIRECTIVE (2026-06-22) in AC-1 authorizing the effort delta as an intentional third change. `kind: spacedock_solver` + `runtime: codex` + `trials: 1` all preserved. Two caveats this introduces are flagged for the captain (see note). |
| G4 smoke tasks+exclude | PASS | Smoke diff adds only `benchmark.tasks:` (PATENTS/stockmarket/googlelocal/yelp — dataset names, not per-query ids) + dataset-level `exclude_tasks:` (8 non-panel datasets); no field other than tasks/exclude_tasks differs (effort already matches the full spec — both xhigh). Surviving set per ensign `--explain` includes all 3 named targets (PATENTS-q1/q2/q3). |
| G5 both frozen | PASS | Both `…frozen.yaml` + `…smoke.frozen.yaml` exist; each re-frozen carrying `kind: spacedock_solver` + `runtime: codex` AND `reasoning_effort: xhigh` (verified line 21 in both). |
| G6 resolver fidelity | PASS | Inserted text is verbatim the 10-bullet block in the Falsifiable claim; same stage, same idea, generative authoring prose, no self-anchored "verify your own answer" phrasing. (Fidelity is about the README change; the effort delta is a spec field, ruled under G3.) |
| G7 actionability/inert-risk | WARN | Most bullets are abstract-structural prose ("build the full time axis", "traverse edges explicitly", "use all associated values", "emit every qualifying row") with NO worked-example skeleton — the "talks but doesn't do" shape that went inert in dab0012/dab0017 at gpt-5.5/xhigh. The pre-finalize verification-table bullet is the most concrete; the rest carry real inert-risk. |
| G8 regression-canary coverage | PASS | Generative lever (fires on every shape-matching query). Smoke keeps abundant non-PATENTS `@baseline` passers — stockmarket q1-q5 (5), yelp q1-q7 (7), googlelocal q1/q3/q4 (3). ≥2 perturbable canaries on each most-similar shape: stockmarket (time-series + best-year/peak rank), yelp (free-text + complete-list), googlelocal (free-text + all-associated). Caveat for interpretation moved to captain note (effort confound). |
| G9 selector independence | N/A | Generative authoring lever, not a multi-candidate/selector protocol. |
| G10 self-correcting false-positive | N/A | Authoring discipline, not a check/reconcile/validate-and-fix-on-disagreement lever (the verification table is a pre-finalize scratchpad, not a fix-on-disagreement rule). |

**For the captain:** No FAILs — clear to advance to smoke, but the captain-authorized xhigh delta carries two consequences to track to the verdict. (1) METHODOLOGICAL CONFOUND: the README is no longer the only variable vs the registered `high` anchor `@codex-batch-baseline`, so a PATENTS flip cannot be cleanly attributed to the README alone (README, xhigh effort, or their interaction) — clean isolation would need an xhigh-minus-section baseline; AC-3's "README genuinely isolated" weakens to "README + effort jointly isolated vs a high anchor." (2) PRIOR-LEARNING CAVEAT: per the xhigh-hurts-gpt5.5 behavioral model, xhigh has historically HURT gpt-5.5 on DAB (more abstention / over-elaboration), so a regression-panel canary drop at smoke may be an effort side-effect rather than a generative-README side-effect — do not attribute a non-PATENTS drop to the README without controlling for effort. Also still honor AC-0: confirmed PASS above (anchor PATENTS rescored against the NEW oracle, commit `94a87c2`, 0/0/0 on content). G7 inert-risk (fires-everywhere prose, no worked example) remains the main pre-smoke risk on the lever itself.

## Propose-gate smoke set

Smoke spec `specs/dab0022-patents-semistructured-rules.smoke.frozen.yaml`; selection confirmed via
`rk run --explain` (`Tasks: 4`, run-dir `runs/dab0022-patents-semistructured-rules/e4ca5116daac04da`,
solver hash `sha256:ff279bd8…dadd53`). Baseline rewards = `@codex-batch-baseline` (the fork parent,
codex/gpt-5.5 held constant — the valid PATENTS anchor), read from its `summary.json`. **19 query-cells**
(PATENTS 3 + stockmarket 5 + yelp 7 + googlelocal 4). This is a GENERATIVE lever — the table makes the
G8 panel auditable: every non-PATENTS row is a perturbable passer the lever can actually fire on.

```
┌───────────────────┬──────────┬─────────────────────┬──────────────────────────────────────────────────────┐
│       Task        │ Baseline │ Should pass in smoke?│             Role / why we picked it                    │
├───────────────────┼──────────┼─────────────────────┼──────────────────────────────────────────────────────┤
│ PATENTS-q1        │ ❌ FAIL  │ 🎯 want it to flip  │ Target — CPC level-5 EMA best-year=2022 (hierarchy +   │
│                   │          │                     │ time-series + peak rules).                             │
│ PATENTS-q2        │ ❌ FAIL  │ 🎯 want it to flip  │ Target — Germany H2-2019 level-4 EMA (hierarchy +      │
│                   │          │                     │ time-series + parser rules).                           │
│ PATENTS-q3        │ ❌ FAIL  │ 🎯 want it to flip  │ Target — UNIV CALIFORNIA citation graph → CPC subclass │
│                   │          │                     │ titles (graph-traversal + all-associated + exact-id).  │
│ stockmarket-q1    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (stockmarket) — perturbable: time-series shape. │
│ stockmarket-q2    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (stockmarket) — perturbable: time-series shape. │
│ stockmarket-q3    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (stockmarket) — perturbable: ranking/peak.      │
│ stockmarket-q4    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (stockmarket) — perturbable: ranking metric     │
│                   │          │                     │ (the cell dab0016 saw flip on metric choice).          │
│ stockmarket-q5    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (stockmarket) — perturbable: time-series/rank.  │
│ yelp-q1           │ ✅ PASS  │ ✅ must stay PASS   │ Canary (yelp) — perturbable: free-text + complete-list.│
│ yelp-q2           │ ✅ PASS  │ ✅ must stay PASS   │ Canary (yelp) — perturbable: free-text parse.          │
│ yelp-q3           │ ✅ PASS  │ ✅ must stay PASS   │ Canary (yelp) — perturbable: free-text parse.          │
│ yelp-q4           │ ✅ PASS  │ ✅ must stay PASS   │ Canary (yelp) — perturbable: complete-list / ranking.  │
│ yelp-q5           │ ✅ PASS  │ ✅ must stay PASS   │ Canary (yelp) — perturbable: complete-list / ranking.  │
│ yelp-q6           │ ✅ PASS  │ ✅ must stay PASS   │ Canary (yelp) — perturbable: free-text + all-associated│
│ yelp-q7           │ ✅ PASS  │ ✅ must stay PASS   │ Canary (yelp) — perturbable: complete-list.            │
│ googlelocal-q1    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (googlelocal) — perturbable: free-text parse.   │
│ googlelocal-q2    │ ❌ FAIL  │ — (already fails)   │ Non-target failer — watch only; no flip credit claimed.│
│ googlelocal-q3    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (googlelocal) — perturbable: all-associated.    │
│ googlelocal-q4    │ ✅ PASS  │ ✅ must stay PASS   │ Canary (googlelocal) — perturbable: complete-list.     │
└───────────────────┴──────────┴─────────────────────┴──────────────────────────────────────────────────────┘
```

**Net hoped for:** flip ≥1 of the 3 PATENTS targets FAIL→PASS by committed-artifact evidence, lose
**zero** of the 15 passer canaries (stockmarket 5 + yelp 7 + googlelocal q1/q3/q4). googlelocal-q2 is
already FAIL and not a target — watched but no credit. Run is detached (nohup); no need to wait
on-screen. **ETA** ~ 4 batch-dataset cells at concurrency.trials:2 ≈ 30–60 min wall (PATENTS is the
heaviest — billion-row CPC EMA over postgres `patent_CPCDefinition` + sqlite publication DB).

> **TWO CAPTAIN-DIRECTIVE CAVEATS carried into this smoke read** (`reasoning_effort: xhigh`, anchor=`high`):
> 1. **Effort confound on the targets.** A PATENTS flip here is "README + xhigh vs the high anchor," NOT
>    the README in isolation — it could be the rules, the xhigh effort, or their interaction. Treat any
>    GO as needing an xhigh-minus-section baseline before clean README attribution (AC-1 / AC-3).
> 2. **Effort confound on the canaries (xhigh-hurts-gpt5.5).** A canary drop in the panel may be an
>    xhigh effort side-effect (more abstention / over-elaboration), NOT a generative-README side-effect.
>    Do not read a non-PATENTS regression as a README G8 failure without controlling for effort — though
>    for the GO/NO-GO bar a drop still counts against the run regardless of which cause it is.

## Smoke run (launched — detached)

Launched the detached smoke run on the frozen smoke spec. The FO owns the wait (sentinel scan); I
return the handle and do not poll.

- **Handle:** `runs/.rk-handles/dab0022-smoke-20260622-105518/`
- **PID:** 1755090 (worker alive at launch; `done` sentinel absent = still running)
- **Spec:** `specs/dab0022-patents-semistructured-rules.smoke.frozen.yaml` (4 datasets, `reasoning_effort: xhigh`)
- **Selection (re-confirmed $0 via `--explain`):** `Tasks: 4` = PATENTS + stockmarket + googlelocal + yelp;
  resolved `harbor_agent_kwargs.reasoning_effort: "xhigh"`; solver hash `sha256:ff279bd8…dadd53`.
- **Cells:** 19 query-cells (PATENTS 3 targets + stockmarket 5 + yelp 7 + googlelocal 4 canaries).
- **Started:** 2026-06-22T10:55:18Z. **Sentinel:** `runs/.rk-handles/dab0022-smoke-20260622-105518/done`
  (absent until finished; `rc=0` ⇒ OK). **Log:** `…/log`. ntfy: none configured.
- **ETA:** ~19 cells at `concurrency.trials:2`, xhigh (slower than high) — expect notably longer than a
  `high` smoke; rough order ~1–2 h wall, PATENTS the heaviest (billion-row CPC EMA + citation-graph join).

**Next (FO, phase 2 on the `done` sentinel):** `rk audit --policy strict` (AC-2: 0 coverage_missing /
0 tainted), `rk score`, then the per-cell deep-dive — read PATENTS committed `answers.json` per query
for FAIL→PASS by-artifact, and check the 15 canaries for any drop (remember the xhigh effort confound:
a canary drop may be effort, not the README — AC-1 caveats).

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork the BATCH anchor solver to `solver_workflows/dab0022-patents-semistructured-rules` and add ONLY the `### Semi-structured data rules` section (verbatim); leak-guard prose byte-intact.
  `diff` vs `spacedock-readme-baseline-hostfix/README.md` = pure addition `88a89,101`; forbidden-token grep on added lines (ground_truth/db_description_withhint/curl/wget/git clone) = none.
- DONE: Build full + smoke specs in BATCH mode by forking `specs/codex-dab-batch-baseline.yaml`; freeze both.
  Full diff (sans ABOUTME comments) = only `experiment:` + `solver_workflow:`; `dab0022-patents-semistructured-rules.frozen.yaml` + `…smoke.frozen.yaml` written via `rk freeze --allow-missing`.
- DONE: Verify via `rk run --explain` that the smoke selection = PATENTS (all 3 queries) PLUS the generative regression panel.
  `--explain` → `Tasks: 4` = PATENTS + stockmarket + googlelocal + yelp; surviving cells = PATENTS q1-q3 (targets) + 15 perturbable non-PATENTS passers (≥2 on each of ranking / complete-list / free-text-parse shapes).
- DONE: Verify AC-0 — the anchor reflects the NEW PATENTS oracle.
  `@codex-batch-baseline` = `bf113446fdd94373`; rescore commit `94a87c2` (rescore-result.json) scores its committed PATENTS answers at q1/q2/q3 = 0/0/0 on CONTENT under production verify_batch.py + latest GT — valid new-oracle scores, no re-baseline needed. Recorded in `## AC-0 verification`.
- DONE: Run the gatekeeper subagent; record its table + APPROVE/REVISE/REJECT block.
  Recommendation **APPROVE** (no FAILs; one G7 inert-risk WARN); G9/G10 N/A (generative authoring lever). Block in `## Gatekeeper review`.
- DONE: Prepare the smoke-set boxed table with `@codex-batch-baseline` rewards resolved; G8 panel auditable.
  19-cell boxed table in `## Propose-gate smoke set` (3 targets ❌ + 15 must-stay ✅ canaries + googlelocal-q2 already-FAIL watch); net = flip ≥1 PATENTS, lose 0 canaries.

### Summary

dab0022 is a single generative `### Semi-structured data rules` README section forked onto the codex `@codex-batch-baseline` anchor to flip the 3 now-scorable PATENTS content failures (q1/q2/q3 = 0/0/0). AC-0 verified PASS: the anchor's PATENTS cells were rescored against the NEW oracle (commit 94a87c2) and genuinely fail on content — the comparison is valid and the model is held constant (codex-vs-codex). Gatekeeper recommends APPROVE with one G7 inert-risk WARN (fires-everywhere prose with no worked example, the dab0012/dab0017 "talks but doesn't do" shape) — smoke is the real test. The smoke panel keeps 15 perturbable passer canaries across stockmarket/yelp/googlelocal (the exact ranking/complete-list/free-text-parse shapes these rules most likely perturb), so any generative side-effect is visible at smoke. Auto-gate criteria are met (gatekeeper APPROVE + reject-checks clean), but presenting the gate to the captain given the G7 inert-risk WARN.

## Stage Report: propose (cycle 2 — captain directive: reasoning_effort xhigh)

- DONE: Set `agent.reasoning_effort: xhigh` in BOTH `specs/dab0022-patents-semistructured-rules.yaml` and `…smoke.yaml`, then re-freeze both.
  All 4 spec files (full+smoke, source+frozen) now carry `reasoning_effort: xhigh`; both frozen re-written; `kind: spacedock_solver` + `runtime: codex` + `trials: 1` preserved.
- DONE: Update AC-1 to record the xhigh delta as a captain-directed intentional change (third allowed spec delta), NOT a leak/spec fault.
  AC-1 now carries a "CAPTAIN DIRECTIVE (2026-06-22)" addendum + a METHODOLOGICAL CONFOUND note + the xhigh-hurts-gpt5.5 PRIOR-LEARNING caveat; AC-3 amended that the README is isolated jointly-with-effort, not alone.
- DONE: Re-run the gatekeeper; G3 evidence notes the effort delta is captain-authorized (G3 PASS, not FAIL), with the methodological confound + xhigh-hurts-gpt5.5 paradox explicitly flagged.
  Cycle-2 gatekeeper (Reviewed 2026-06-22T11:42:00Z) recommends **APPROVE**, G3 PASS (captain-override) on the verified three-field diff; both caveats in the "For the captain" note. Block supersedes cycle-1 in `## Gatekeeper review`.
- DONE: Carry both caveats into the smoke-set presentation.
  Two-caveat block added under "Net hoped for" in `## Propose-gate smoke set`.

### Summary

Per captain directive, dab0022 now runs at `reasoning_effort: xhigh` (anchor is `high`), making the full spec intentionally differ from `codex-dab-batch-baseline.yaml` in THREE fields (experiment / solver_workflow / reasoning_effort). AC-1 records this as captain-authorized (not a spec fault) and the cycle-2 gatekeeper rules G3 PASS under that override while flagging two consequences carried to the verdict: (1) the README is no longer the only variable vs the high anchor, so a PATENTS flip is README+xhigh jointly, not isolated — clean attribution needs an xhigh-minus-section baseline; (2) the xhigh-hurts-gpt5.5 paradox means a canary drop at smoke may be an effort side-effect rather than a README side-effect. Recommendation stays APPROVE, no FAILs; G7 inert-risk WARN remains the main lever risk.

## Stage Report: propose (cycle 3 — re-verify xhigh landed)

- DONE: Confirm `reasoning_effort: xhigh` is present in BOTH frozen specs and lands in the resolved run kwargs.
  Team-lead reported the frozen specs still read `high`; re-checked and they do NOT — on-disk + committed HEAD (373ae82, branch main, no other worktrees, clean tree) both `*.frozen.yaml` read `reasoning_effort: xhigh` (line 21). The cycle-2 commit already carried the change; the `high` read was stale (pre-373ae82 / different shell). No re-edit or re-freeze was needed — re-applying would have been a no-op.
- DONE: Confirm via `rk run --explain` ($0) that the resolved run uses xhigh and the smoke selection is unchanged.
  `--explain` on `…smoke.frozen.yaml` resolves `harbor_agent_kwargs.reasoning_effort: "xhigh"` (the authoritative runtime value Harbor executes), `Tasks: 4` = PATENTS + stockmarket + googlelocal + yelp (unchanged), solver hash `sha256:ff279bd8…dadd53` unchanged. Full-spec diff vs anchor = exactly 3 fields (experiment / reasoning_effort high→xhigh / solver_workflow).

### Summary

Re-verification only: the xhigh change had already landed in cycle-2 commit 373ae82 (both source + both frozen specs, committed HEAD on main, clean tree) — the team-lead's `high` report was a stale read. Confirmed authoritatively via `rk run --explain`, whose resolved `harbor_agent_kwargs.reasoning_effort` is `xhigh` and whose smoke selection (Tasks: 4, PATENTS + canary panel) and solver hash are unchanged. AC-1 / Gatekeeper-G3 / smoke-set caveats from cycle 2 stand. No spec edits or commits were needed for the effort field; this report documents the re-check.

## Stage Report: smoke

- DONE: Re-confirm selection ($0) via `rk run --explain` = 4 datasets (PATENTS + stockmarket + yelp + googlelocal); launch DETACHED via `drivers/rk-run-detached.sh dab0022-smoke …smoke.frozen.yaml run`; record handle + pid + ETA.
  `--explain` → `Tasks: 4`, resolved `reasoning_effort: "xhigh"`, solver hash `sha256:ff279bd8…dadd53`. Launched: handle `runs/.rk-handles/dab0022-smoke-20260622-105518/`, pid 1755090 (alive, `done` absent), started 2026-06-22T10:55:18Z. Recorded in `## Smoke run (launched — detached)`. Did NOT poll/wait — handle returned to the FO immediately.

### Summary

Re-confirmed the smoke selection at $0 (4 datasets, xhigh resolved in the run kwargs) and launched the detached smoke run on the frozen smoke spec via the standard detached driver. Worker is alive (pid 1755090), the `done` sentinel is absent (still running), and the handle is recorded for the FO's sentinel scan. Per the launch-phase contract I returned the handle immediately and did not wait — phase 2 (audit/score/per-cell deep-dive) runs when the FO re-engages on the `done` sentinel. ETA is longer than a `high` smoke because xhigh is slower; PATENTS is the heaviest cell.
