---
id: dab0022
title: Semi-structured data rules — parser-first / all-associated / full-list discipline to flip the 3 newly-resolvable PATENTS queries
status: hypothesis
kind: hypothesis
source: Captain-directed. Upstream updated the ground truth + verifier for ALL 3 PATENTS queries — PATENTS is no longer an unresolvable dataset (it scored 0/3 in dab0018-full3 against the old/broken oracle). This files the first hypothesis to attack the now-scorable PATENTS cells with an explicit semi-structured-data-handling README section.
started:
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

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
