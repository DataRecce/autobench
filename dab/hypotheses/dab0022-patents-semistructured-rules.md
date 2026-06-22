---
id: dab0022
title: Semi-structured data rules — parser-first / all-associated / full-list discipline to flip the 3 newly-resolvable PATENTS queries
status: propose
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

**AC-1 — Exactly the README change; full spec differs from the anchor only in `experiment:` +
`solver_workflow:`.** Verified by `diff specs/codex-dab-batch-baseline.yaml
specs/dab0022-patents-semistructured-rules.yaml`. The solver README diff vs its parent
(`spacedock-readme-baseline-hostfix`) adds ONLY the `### Semi-structured data rules` section;
leak-guard prose byte-intact.

**AC-2 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict` on
the same run-dir; `0 coverage_missing`, `0 tainted`).

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`, with the codex-vs-Opus
confound attributed via the committed-artifact read** (does the README rule reach the committed
answer on each flipped PATENTS query, vs a flip the model swap would produce regardless). Note the
anchor `@codex-batch-baseline` is the SAME codex/gpt-5.5 model, so on PATENTS the model is held
constant and the README is genuinely isolated.

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

**Recommendation: APPROVE** — clean two-field spec fork, leak-guard byte-intact, single generative `### Semi-structured data rules` section matching the claim, both specs frozen with kind/runtime preserved, and an abundant perturbable canary panel (stockmarket 5 / yelp 7 / googlelocal 3 passers, ≥2 perturbable on each most-similar shape). One G7 inert-risk WARN (the rules are largely abstract-structural prose) for the captain note.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-22T11:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is a single pure addition `88a89,101` — one `### Semi-structured data rules` block in the analyze/methodology section; no other stage touched, no leak-guard prose edited. |
| G2 leak-guard intact | PASS | Added-line grep for `ground_truth`/`db_description_withhint`/`curl`/`wget`/`git clone` = NONE FOUND; diff is addition-only so all parent leak-guard paragraphs are byte-identical. |
| G3 spec two fields | PASS | `diff` vs `codex-dab-batch-baseline.yaml` shows only `experiment:` and `solver_workflow:` changed (plus the ABOUTME comment header, not a field); `agent.kind: spacedock_solver` + `runtime: codex` preserved; `trials: 1`. |
| G4 smoke tasks+exclude | PASS | Smoke diff adds only `benchmark.tasks:` (PATENTS/stockmarket/googlelocal/yelp — dataset names, not per-query ids) + `exclude_tasks:` (8 non-panel datasets); nothing else differs. Surviving set per ensign `--explain` includes all 3 named targets (PATENTS-q1/q2/q3). |
| G5 both frozen | PASS | Both `…frozen.yaml` and `…smoke.frozen.yaml` exist (1867 / 1862 bytes); each carries `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text is verbatim the 10-bullet block quoted in the Falsifiable claim; same stage, same idea, no scope creep; fully generative authoring prose (parser-first / all-associated / full-list / graph-traversal / verification-table) — no self-anchored "re-run/verify your own answer" phrasing. |
| G7 actionability/inert-risk | WARN | Most bullets are abstract-structural prose ("build the full time axis", "traverse edges explicitly", "use all associated values", "emit every qualifying row") with NO worked-example skeleton — exactly the "talks but doesn't do" shape that went inert in dab0012/dab0017 at gpt-5.5/xhigh. The verification-table bullet is the most concrete; the rest carry real inert-risk. |
| G8 regression-canary coverage | PASS | Generative lever (fires on every shape-matching query). Smoke keeps abundant non-PATENTS `@baseline` passers — stockmarket q1-q5 (5), yelp q1-q7 (7), googlelocal q1/q3/q4 (3). ≥2 perturbable canaries on each most-similar shape: stockmarket (time-series + best-year/peak rank), yelp (free-text + complete-list), googlelocal (free-text + all-associated). |
| G9 selector independence | N/A | Generative authoring lever, not a multi-candidate/selector protocol. |
| G10 self-correcting false-positive | N/A | Authoring discipline, not a check/reconcile/validate-and-fix-on-disagreement lever (the verification table is a pre-finalize sanity scratchpad, not a fix-on-disagreement rule). |

**For the captain:** No FAILs — clear to advance to smoke. Two things to weigh: (1) G7 inert-risk — this is a fires-everywhere prose lever with no worked example, the same form that went inert at gpt-5.5 in dab0012/dab0017; smoke is the real test of whether it lands on PATENTS rather than being discussed-and-skipped. (2) AC-0 is already verified PASS above — the codex `@codex-batch-baseline` fork parent's PATENTS cells were rescored against the NEW oracle (commit `94a87c2`) at 0/0/0 on content, so the delta will be valid.

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
