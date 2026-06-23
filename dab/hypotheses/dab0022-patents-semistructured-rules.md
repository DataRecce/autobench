---
id: dab0022
title: Semi-structured data rules — parser-first / all-associated / full-list discipline to flip the 3 newly-resolvable PATENTS queries
status: analyze
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

**AC-1 — Exactly the README change; full spec differs from the anchor in ONLY TWO fields
(`experiment:` + `solver_workflow:`).** Verified by `diff specs/codex-dab-batch-baseline.yaml
specs/dab0022-patents-semistructured-rules.yaml`. The solver README diff vs its parent
(`spacedock-readme-baseline-hostfix`) adds ONLY the `### Semi-structured data rules` section
(now with the two cycle-3 scoping fixes inside it); leak-guard prose byte-intact.

> **REVISE CYCLE 3 (2026-06-22) — effort reverted to `high`; confound REMOVED; this SUPERSEDES the
> cycle-2 xhigh directive block below.** Per captain direction after the cycle-2 smoke (which flipped
> PATENTS-q1/q2 but regressed stockmarket-q3), `agent.reasoning_effort` is reverted **xhigh → high** in
> both specs. The captain attributed the stockmarket-q3 regression to the **README rule** (the
> simple-record/free-text rule pulling a description blurb into a name+number answer), not to xhigh
> effort. Reverting to `high` restores the workflow invariant: the full spec now differs from
> `specs/codex-dab-batch-baseline.yaml` in **only two** fields (`experiment:` + `solver_workflow:`,
> confirmed by the diff above; both frozen specs carry `reasoning_effort: high`), so the **README is once
> more the sole variable vs the high anchor** — the AC-1/AC-3 methodological confound is GONE and a
> PATENTS flip or a canary drop now attributes cleanly to the README. The cycle-3 re-author also adds
> two scoping fixes inside the same one section (idea unchanged): (fix #1) the simple-record rule now
> forbids inserting free-text description/blurb fields into a name+number answer and keeps the number
> adjacent to the name (targets the stockmarket-q3 regression); (fix #2) the graph/citation rule now
> binds a code's title at the exact named hierarchy level — the subclass title for a subclass question,
> not the group-level title (targets PATENTS-q3's wrong-level title). New solver content hash
> `sha256:b2cae85c…` (was `ff279bd8…`). The cycle-2 block below is retained for audit trail only.
>
> ---
> **[SUPERSEDED — cycle-2 only] CAPTAIN DIRECTIVE (2026-06-22) — third spec delta authorized.** The captain directed this run to
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
constant and the README is genuinely isolated. **RE-AMENDED (REVISE cycle 3):** effort is reverted to
`high`, matching the anchor, so the model AND the effort are now both held constant — the README is once
more **genuinely isolated** (the cycle-2 "README+xhigh jointly" weakening is withdrawn; the confound is
removed). A PATENTS flip in the cycle-3 re-smoke is cleanly attributable to the README.

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

_Re-run (cycle 3) after the REVISE re-author: `reasoning_effort` reverted xhigh→high (confound removed, two-field diff restored) + two in-section scoping fixes (stockmarket-q3 regression, PATENTS-q3 title level). This supersedes the cycle-2 captain-override review below. The cycle-1 (two-field) and cycle-2 (three-field, captain-override) blocks are retained in git history._

**Recommendation: APPROVE** — cycle-3 re-author (xhigh→high effort revert + two in-section scoping fixes) is clean: full spec back to exactly two fields (README = sole variable, confound removed), README still addition-only / one-section / one-idea, leak-guard byte-intact, both specs re-frozen with kind/runtime/effort preserved, panel unchanged. The G7 inert-risk WARN is softened (fix #1 is now a concrete name+number / no-blurb mechanical instruction) but the section overall remains partly abstract-structural prose, so the WARN stands for the captain note.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-22T12:25:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is still a single pure addition `88a89,101` — one `### Semi-structured data rules` block. The two cycle-3 fixes are scoping clauses APPENDED inside the existing graph/citation bullet and the final-format bullet (no new bullet, no second section, no new lever) — still one idea, one stage. |
| G2 leak-guard intact | PASS | Added-line grep for `ground_truth`/`db_description_withhint`/`curl`/`wget`/`git clone` = NONE FOUND; diff is addition-only so all parent leak-guard paragraphs are byte-identical. The two new clauses name only generic schema concepts (hierarchy level / name+number), no oracle file or withheld-hint content. |
| G3 spec two fields | PASS | Full-spec diff vs `codex-dab-batch-baseline.yaml` is BACK to exactly two fields — `experiment:` + `solver_workflow:` (plus ABOUTME comments). `reasoning_effort:` reverted xhigh→high (now matches the anchor), so the cycle-2 captain-override is no longer needed — clean two-field PASS. `kind: spacedock_solver` + `runtime: codex` + `trials: 1` preserved. README is once again the sole variable vs the high anchor; the AC-1/AC-3 confound is removed. |
| G4 smoke tasks+exclude | PASS | Smoke diff adds only `benchmark.tasks:` (PATENTS/stockmarket/googlelocal/yelp — dataset names) + dataset-level `exclude_tasks:` (8 non-panel datasets); effort now matches the full spec (both high). Ensign re-confirmed Tasks: 4 via `--explain`; surviving set includes all 3 named targets (PATENTS-q1/q2/q3). |
| G5 both frozen | PASS | Both `…frozen.yaml` + `…smoke.frozen.yaml` re-frozen this cycle, each carrying `kind: spacedock_solver` + `runtime: codex` AND `reasoning_effort: high` (verified line 21 in both). |
| G6 resolver fidelity | PASS | Inserted text matches the claim, and the two new clauses match the cycle-2 Failure Review's prescribed scoping: fix #1 (stockmarket-q3) = output only exact name + adjacent number, no description/blurb fields; fix #2 (PATENTS-q3) = resolve a code's title at exactly the named hierarchy level, no finer/coarser substitution. Targeted scoping of the existing idea, not new scope — idea intact, generative authoring prose, no self-anchored verification. |
| G7 actionability/inert-risk | WARN (softened) | Fix #1 is now a CONCRETE mechanical instruction ("output only the exact name + that number kept adjacent; do NOT insert free-text description/summary fields") — more actionable than the original abstract bullet, genuinely softening the inert-risk on the formatting clause. Fix #2 is a concrete level-resolution rule (good). But the section's core bullets (parser-first, full time axis, traverse edges, all-associated) remain abstract-structural prose with no worked-example skeleton — the dab0012/dab0017 "talks but doesn't do" risk persists for those, so the WARN stands. |
| G8 regression-canary coverage | PASS | Same generative lever, same 4-dataset panel. Smoke keeps abundant non-PATENTS `@baseline` passers — stockmarket q1-q5 (5), yelp q1-q7 (7), googlelocal q1/q3/q4 (3). ≥2 perturbable canaries on each most-similar shape: stockmarket (time-series + best-year/peak rank — incl. the q3 the fix targets), yelp (free-text + complete-list), googlelocal (free-text + all-associated). Effort now high (matches anchor), so a panel drop this cycle is attributable to the README, not effort. |
| G9 selector independence | N/A | Generative authoring lever, not a multi-candidate/selector protocol. |
| G10 self-correcting false-positive | N/A | Authoring discipline, not a check/reconcile/validate-and-fix-on-disagreement lever. |

**For the captain:** No FAILs — clear to advance to smoke (cycle 3). The cycle-2 confound is resolved: effort is back to high, so the README is the sole variable vs `@codex-batch-baseline` and a clean PATENTS attribution is again possible (AC-3 isolation restored). Watch two things at smoke: (1) does fix #1 actually hold stockmarket-q3 (the cycle-2 regression) while the 2 PATENTS flips survive the effort revert — confirm both by committed artifact, since reverting xhigh→high could itself move the PATENTS cells; (2) the remaining abstract bullets (G7) are still the inert-risk surface. Still honor AC-0: confirm the anchor's PATENTS cells are scored against the NEW oracle (commit `94a87c2`).

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

> **NOTE:** the section above is the cycle-1 (xhigh) smoke that produced the REVISE. The cycle-3
> re-smoke below is the one to read for the current go/no-go (effort=high, two README fixes).

## Smoke run cycle-3 (launched — detached)

Launched the cycle-3 re-smoke after the REVISE re-author (effort reverted to `high`, two in-section
README scoping fixes). FO owns the wait via the sentinel scan; I return the handle and do not poll.

- **Handle:** `runs/.rk-handles/dab0022-smoke2-20260622-150545/`
- **PID:** 1853402 (worker alive at launch; `done` sentinel absent = running)
- **Spec:** `specs/dab0022-patents-semistructured-rules.smoke.frozen.yaml` (4 datasets, `reasoning_effort: high`)
- **Selection (re-confirmed $0 via `--explain`):** `Tasks: 4` = PATENTS + stockmarket + googlelocal + yelp;
  resolved `reasoning_effort: "high"`; **new solver hash `sha256:b2cae85c…`** (the cycle-3 README with both fixes).
- **Cells:** 19 query-cells (PATENTS 3 targets + stockmarket 5 + yelp 7 + googlelocal 4 canaries).
- **Started:** 2026-06-22T15:05:45Z. **Sentinel:** `runs/.rk-handles/dab0022-smoke2-20260622-150545/done`
  (absent until finished; `rc=0` ⇒ OK). **Log:** `…/log`. ntfy: none configured.
- **ETA:** ~**35–45 min** wall. This is `high` (not xhigh) — same effort as the cycle-1 smoke (which ran
  ~44 min) and faster than xhigh; PATENTS remains the heaviest cell (billion-row CPC EMA + citation graph).

**Phase-2 watch-items (per the cycle-3 gatekeeper, now with NO effort confound — effort=high matches the anchor):**
1. **Did fix #1 hold stockmarket-q3?** The cycle-2 regression must be back to PASS (the simple-record
   rule now forbids the description blurb). Confirm by committed artifact (name+number, no blurb).
2. **Did the 2 PATENTS flips survive the effort revert?** q1/q2 flipped at xhigh in cycle-1; the
   xhigh→high revert could itself move them — confirm by committed artifact, not just reward.
3. **Did fix #2 flip PATENTS-q3?** If the subclass-title level binding worked, q3 may now PASS (turning
   the panel toward +3/0). All attributions are clean this cycle (README is the sole variable).

## Yelp confirm probe (launched — detached)

Captain chose the disambiguation probe (my recommended option 2): a **yelp-only 3-draw** run at the
cycle-3 README + `high`, to decide whether the cycle-3 yelp-q4/q7 drops are **README-real or temp=0
variable-band noise** (they passed at the anchor AND cycle-1 — 2 prior passes — then dropped at cycle-3).
NOT an IV change: same cycle-3 solver_workflow (hash `b2cae85c…`), same effort; only the task set +
trials change.

- **Spec:** `specs/dab0022-patents-semistructured-rules.yelp3.frozen.yaml` — yelp only, `trials: 3`,
  `concurrency.trials: 1` (CRITICAL — same-dataset multi-draw collides on the shared named postgres
  volume at concurrency>1; the dab0018 crma3 lesson, so draws run **serially**).
- **`--explain` confirmed:** `Tasks: 1` (yelp), `trials: 3`, `reasoning_effort: "high"`, solver hash
  `sha256:b2cae85c…` → **21 cells** (7 yelp queries × 3 draws).
- **Handle:** `runs/.rk-handles/dab0022-yelp3-20260622-170140/`
- **PID:** 1915756 (worker alive at launch; `done` sentinel absent = running)
- **Started:** 2026-06-22T17:01:40Z. **Sentinel:** `runs/.rk-handles/dab0022-yelp3-20260622-170140/done`
  (absent until finished; `rc=0` ⇒ OK). **Log:** `…/log`. ntfy: none configured.
- **ETA:** ~**25–40 min** wall (3 serial yelp draws at concurrency.trials:1; yelp is a mid-weight 7-query
  free-text dataset — one draw is a fraction of the ~29-min full-panel cycle-3 run, ×3 serial).

**Decision rule (FO, on the `done` sentinel):** per-draw + per-query pass-count for **yelp-q4 and
yelp-q7** across the 3 clean draws vs anchor 7/7. Exclude any infra-killed draw (coverage_missing) from
the count.
- **q4/q7 STABLY drop** (fail in a clear majority of clean draws) → **README-real** → proceed to the
  option-1 scope-fix REVISE (scope the full-list/ranking rules off single-winner / fixed-top-k questions).
- **q4/q7 wobble** (pass in a majority) → **variable-band noise**, not the README → the board is
  effectively a **clean +3-PATENTS-target GO** (all targets solved, the cycle-2 regression fixed, no
  real canary loss).

### Probe RESULT — WOBBLE confirmed (cycle-3 yelp drops were NOISE, not the README)

**Run dir:** `runs/dab0022-patents-semistructured-rules/f18986d467555a33` (rc=0, ~41 min).
**Audit (AC-2): CLEAN** — `coverage_missing: 0`, `tainted: 0`; **all 3 draws clean** (none infra-killed),
so the full 3-draw read stands.

Per-draw, per-query (vs anchor yelp 7/7), by validator + committed artifact:

| Draw | q1 | q2 | q3 | **q4** | q5 | q6 | **q7** | yelp total |
|------|----|----|----|--------|----|----|--------|------------|
| EaHD9jk | ✅ | ✅ | ✅ | **✅** | ✅ | ✅ | **✅** | 7/7 |
| EvQ8oN8 | ✅ | ❌ | ✅ | **✅** | ✅ | ✅ | **✅** | 6/7 |
| FCzHEVJ | ✅ | ✅ | ✅ | **✅** | ✅ | ✅ | **✅** | 7/7 |
| **q4/q7 pass-count** | | | | **3/3** | | | **3/3** | |

- **yelp-q4: PASS 3/3** — every draw "Found: Restaurant, 3.63" (the exact GT value). The cycle-3 single
  fail (committed 3.5414) was a one-draw aggregation wobble, not a README effect.
- **yelp-q7: PASS 3/3** — every draw "All categories are present." The cycle-3 missing-Breakfast&Brunch
  was a one-draw top-5 ranking wobble.
- Incidental: **yelp-q2** dropped in 1/3 draws (EvQ8oN8) — q2 is itself a variable-band ranking cell
  ("which state has the most reviews + its avg rating"), independent of the two cells under test; it
  confirms yelp carries temp=0 variance generally, reinforcing that q4/q7's single-draw cycle-3 fail was
  noise.

**VERDICT: WOBBLE.** yelp-q4 and yelp-q7 pass in 3/3 clean draws (unanimous majority) — the cycle-3
drops were **temp=0 variable-band noise, NOT a README regression.** Per the decision rule this means the
cycle-3 board is **effectively a clean +3-PATENTS-target GO**: all 3 PATENTS targets flipped FAIL→PASS by
committed artifact (confound-free at high), the cycle-2 stockmarket-q3 regression was genuinely fixed,
and there is **no real canary loss** on the panel. No option-1 scope-fix REVISE is needed — the lever's
blast radius did not actually damage yelp.

**Caveat for the full board:** this confirms yelp's ranking cells (q2/q4/q7) sit in the temp=0 variable
band, so a single full draw will wobble some ranking cells in BOTH directions regardless of the README —
the standing DAB calibration lesson (dab0011/dab0016). The +3 PATENTS flips are the real, stable signal;
isolated single-cell ranking wobbles on the full board should be read as variance, not lever regressions,
unless they reproduce across draws.

## Smoke result

### Cycle-3 (effort=high, two README fixes) — THE CURRENT READ

**Run dir:** `runs/dab0022-patents-semistructured-rules/2c614e7b01ec1b31` (rc=0, ~29 min).
**Audit (AC-2): CLEAN** — `coverage_missing: 0`, `tainted: 0`, all 4 trials `clean`. **Panel score: 0.8661**
(4 datasets only; up from cycle-1's 0.8042). **No effort confound** — effort=high matches the anchor, so
every attribution below is cleanly README-driven.

**Headline: all 3 PATENTS targets now PASS AND the cycle-2 stockmarket-q3 regression is FIXED — but the
generative lever opened TWO NEW yelp regressions (q4, q7). GO bar (zero canary regression) still NOT met
→ REVISE again (or accept the trade as a partial win — captain's call).**

| Cell | Anchor | Cy1 (xhigh) | Cy3 (high) | Validator reason (cy3) | Classification (by committed artifact) |
|------|--------|-------------|------------|------------------------|----------------------------------------|
| **PATENTS-q1** | ❌ 0 | ✅ 1 | ✅ 1 | "All CPC codes present." | **flip held** through the effort revert — flat list of level-5 codes. README-attributable, now confound-free. |
| **PATENTS-q2** | ❌ 0 | ✅ 1 | ✅ 1 | "All fuzzy names matched, CPC/year near each." | **flip held** — level-4 records. README-attributable, confound-free. |
| **PATENTS-q3** | ❌ 0 | ❌ 0 | ✅ **1** | "All assignee-title pairs matched by at least one method." | **NEW FLIP — fix #2 worked.** The subclass-title level-binding clause bound the title at the right hierarchy level; the 3 (assignee, subclass-title) pairs now match. README-attributable. |
| **stockmarket-q3** | ✅ 1 | ❌ 0 | ✅ **1** | "All names (≤5 edits) and rounded numbers matched." | **REGRESSION FIXED — fix #1 worked.** The committed answer now pairs the exact name with its avg-volume number (no description blurb), restoring name↔number proximity. README-attributable. |
| **yelp-q4** | ✅ 1 | ✅ 1 | ❌ **0** | "Value '3.63' not found in LLM output." | **NEW REGRESSION.** Q4 = "which category has the most credit-card businesses, and its avg rating." Committed "Restaurants; average rating **3.5414**" — right category, but the avg-rating cohort/aggregation differs from GT's 3.63. A ranking-over-derived-metric cell (the variable band) the lever perturbed. |
| **yelp-q7** | ✅ 1 | ✅ 1 | ❌ **0** | "Missing category: Breakfast & Brunch" | **NEW REGRESSION.** Q7 = "top-5 categories by reviews from 2016-registered users." Committed top-5 = `Restaurants; Food; American (New); Shopping; Automotive` — GT wants **Breakfast & Brunch** in the top-5 (the worker ranked Shopping/Automotive into slots 4-5 instead). A complete-list/ranking content difference the lever's category-attribution perturbed. |
| yelp q1/q2/q3/q5/q6 | ✅ 5 | ✅ 5 | ✅ 5 | all pass | held. |
| googlelocal q1/q3/q4 | ✅ 1/1/1 | ✅ 1/1/1 | ✅ 1/1/1 | hold | held (q2 still ❌, not a target). |
| stockmarket q1/q2/q4/q5 | ✅ 4 | ✅ 4 | ✅ 4 | hold | held. |

**Cell net on the panel: +3 PATENTS flips + stockmarket-q3 restored − 2 NEW yelp regressions.** The
targets are fully solved (3/3 PATENTS, cleanly attributed, confound-free) and the cycle-2 fix worked,
but the lever traded them for 2 fresh yelp drops — so the strict GO bar (≥1 PATENTS flip AND **zero**
canary regression) is still not met.

**Single-draw variance caveat (flagged per the checklist):** yelp-q4 and yelp-q7 are both
**ranking/aggregation-over-derived-metric** cells (largest-category-and-its-average; top-5-by-reviews) —
exactly the temp=0 *variable band* that wobbles on cohort/tie-break/metric choice (cf. dab0016
stockmarket-q4, the dab0011 variance band). They held at the anchor (high) AND at cycle-1 (xhigh) — two
prior passes — then dropped here, which points to a real README-induced ranking shift rather than pure
noise; but a single high draw cannot fully exclude temp=0 variable-band wobble on these two cells. A
1-draw repeat (or a 3-draw band read) on yelp alone would disambiguate README-effect vs variance.

### Cycle-1 (xhigh) — superseded by cycle-3; produced the REVISE

**Run dir:** `runs/dab0022-patents-semistructured-rules/e5cb461ef07e9322` (rc=0, ~44 min).
**Audit (AC-2): CLEAN** — `rk audit --policy strict` → `coverage_missing: 0`, `tainted: 0`; all 4
dataset trials `taint_status: clean`, zero findings. **Score (focused, 4 datasets): 0.8042 stratified**
(not comparable to the 12-dataset board; this is the smoke panel only).

**Headline: 2 PATENTS targets flipped FAIL→PASS by committed artifact; 1 canary regressed
(stockmarket-q3). Not a clean GO — there IS a canary regression. → flawed-but-revisable.**

Per-query vs `@codex-batch-baseline` (anchor scores from its `summary.json`):

| Cell | Anchor | Smoke | Δ | Validator reason (smoke) | Classification (by committed artifact) |
|------|--------|-------|---|--------------------------|----------------------------------------|
| **PATENTS-q1** | ❌ 0 | ✅ 1 | **+1 FLIP** | "All CPC codes present in LLM output." | **flipped — change reached the committed answer.** Worker parsed all 277813 publication rows (parser-first rule), computed the level-5 EMA full-year-axis, and emitted a **flat newline-separated list of 72 codes** (complete-list + simple-record rules). The rescore doc noted the anchor's PATENTS-q1 failed by emitting a JSON **list** that crashed `.lower()`; the README's "simple records, avoid nested commentary" produced an accepted flat string. README-attributable. |
| **PATENTS-q2** | ❌ 0 | ✅ 1 | **+1 FLIP** | "All fuzzy names matched, and CPC/year found near each name." | **flipped — change reached the committed answer.** Flat `TITLE | CODE | YEAR` records for Germany H2-2019 level-4 EMA (hierarchy-level + EMA-full-axis + complete-list + simple-record rules all fired). README-attributable. |
| **PATENTS-q3** | ❌ 0 | ❌ 0 | 0 | "No match for: CRYSTAL IS INC + …; SCHOWALTER LEO J + …; BLOOM ENERGY CORP + …" | **closer-but-failing (NOT inert).** Worker traversed the citation graph correctly (167 UNIV CALIFORNIA pubs → 1,255,417 citation edges → 3 citing assignees, exclusion applied after traversal — exactly the graph-traversal rule) and committed 3 (assignee, subclass-title) pairs. But the resolved **CPC subclass titles are wrong** (committed the cited patent's primary level-5 group title, not the ground-truth subclass title). Self-graded PASSED = a self-anchored false-green on q3. The README reached the method but the title-resolution semantics are off. |
| stockmarket-q3 | ✅ 1 | ❌ 0 | **−1 REGRESSION** | "No number found near name: Apex Global Brands Inc" | **canary regression — README side-effect, effort-confounded.** Q3 = "list all NASDAQ financially-troubled companies with 2008 volume; for each report its avg daily volume." Worker emitted a complete list (cohort 25 → 15 rows) but attached the company's **full free-text description blurb** ("Apex Global Brands Inc. specializes in creating and marketing a diverse portfolio of fashion and lifestyle brands…") to the name, pushing the required volume number out of the validator's name↔number proximity window. This is the **simple-record + free-text/parser rules misfiring on a name+number complete-list shape** — exactly the perturbable shape the panel was chosen to catch (cf. dab0016 stockmarket-q3). **AC-1 confound:** the verbose-blurb output is ALSO the xhigh-over-elaboration signature, so README-rule vs xhigh-effort are entangled and point the same way (verbose output). Counts against the run regardless of cause. |
| yelp q1–q7 | ✅ 7/7 | ✅ 7/7 | 0 | all pass | Held — no perturbation (free-text + complete-list canaries stable). |
| googlelocal q1/q3/q4 | ✅ 1/1/1 | ✅ 1/1/1 | 0 | hold | Held (q2 still ❌, not a target). |

**Cell net on the panel: +2 (PATENTS q1,q2) − 1 (stockmarket-q3) = +1 cell**, but the GO bar is
"≥1 PATENTS flip AND **zero** canary regression" — the stockmarket-q3 drop fails the zero-regression
clause.

## Full run (launched — detached)

Smoke is a GO (clean +3-PATENTS-target; cycle-3 yelp drops confirmed temp=0 variance by the 3-draw
probe). Captain pre-authorized full. Launched the detached full run on the cycle-3 frozen spec; FO owns
the wait via the sentinel scan.

- **Handle:** `runs/.rk-handles/dab0022-full-20260622-174918/`
- **PID:** 1973989 (worker alive at launch; `done` sentinel absent = running)
- **Spec:** `specs/dab0022-patents-semistructured-rules.frozen.yaml` (12 datasets, `reasoning_effort: high`)
- **Selection (re-confirmed $0 via `--explain`):** `Tasks: 12`, `reasoning_effort: "high"`, solver hash
  **`sha256:b2cae85c…`** (the cycle-3 fixed README — both scoping fixes). All 12 datasets → 54 query-cells.
- **Started:** 2026-06-22T17:49:18Z. **Sentinel:** `runs/.rk-handles/dab0022-full-20260622-174918/done`
  (absent until finished; `rc=0` ⇒ OK). **Log:** `…/log`. ntfy: none configured.
- **ETA:** ~**75–90 min** wall (54 cells, high, concurrency.trials:2 — dab0018 full3 at the same shape
  ran ~81 min). PATENTS is the heaviest cell (billion-row CPC EMA + citation-graph join).

**Phase-2 read (FO, on the `done` sentinel) — AC-2/AC-3:** `rk audit --policy strict` (0 coverage_missing
/ 0 tainted — exclude both PG-degradation signatures before any verdict, per the dab postgres dual-signature
lesson), `rk score`, then `rk runs diff` vs `@codex-batch-baseline` (the high anchor — README is the SOLE
variable, confound-free). Confirm the **3 PATENTS flips** hold by committed artifact and read the full
board for generative side-effects. **CALIBRATION (carry from the smoke):** this is a generative
fires-everywhere lever and a single full draw — yelp/stockmarket/googlelocal ranking cells (q2/q4/q7-type)
are confirmed variable-band, so judge by **attributed per-query mechanism**, not the headline delta;
isolated single-cell ranking wobbles are variance unless they reproduce, while the +3 PATENTS flips are the
real signal. Many unsmoked ranking/complete-list cells (agnews, bookreview, music_brainz, crmarenapro,
DEPS_DEV, GITHUB, PANCANCER) will also see this lever fire.

## Run result

**Run dir:** `runs/dab0022-patents-semistructured-rules/d0a6f64260336fff` (rc=0, ~77 min).

**Audit (AC-2): CLEAN — run is VALID, not inconclusive.** `rk audit --policy strict` →
`coverage_missing: 0`, `tainted: 0`; **all 12 datasets present and clean** (54/54 cells scored:
agnews 4, bookreview 3, crmarenapro 13, DEPS_DEV_V1 2, GITHUB_REPOS 4, googlelocal 4, music_brainz 3,
PANCANCER 3, PATENTS 3, stockindex 3, stockmarket 5, yelp 7). **No dab-postgres/Mongo degradation
signature** — grep of every `reward_per_query.json` for "could not translate host name / connection
refused / serverSelectionTimeout / unhealthy / timed out" = NONE; no whole-dataset drop, no mid-run
host-abstain. Both PG-dual-signature checks pass, so the board verdict is trustworthy.

**Headline (AC-3): stratified Pass@1 = 0.7675** vs anchor `@codex-batch-baseline` 0.6966 →
**paired delta +0.0709** (README is the SOLE variable vs the high anchor — confound-free). Also clears
the Opus incumbent `@baseline` 0.6536 by +0.114. (`rk runs diff` not needed — computed the per-query
ledger slug-paired from each run's `summary.json`.)

**PATENTS target verdicts (the hypothesis's claim): q1 ✅ PASS, q2 ✅ PASS, q3 ❌ FAIL.**
- PATENTS-q1 0→1 HELD ("All CPC codes present").
- PATENTS-q2 0→1 HELD ("All fuzzy names matched, CPC/year near each").
- **PATENTS-q3 did NOT hold** — it PASSED in the cycle-3 smoke (1/1/1) but FAILS on the full draw
  ("No match for: BLOOM ENERGY CORP + PROCESSES OR MEANS…"). So **2 of 3 PATENTS targets flipped on the
  full board**, not 3 — q3 is a single-draw movement (smoke-PASS → full-FAIL) on the citation-graph cell;
  whether it's variance or a fragile flip is an analyze-stage question.

**Full paired ledger vs anchor (5 flips, 2 regressions):**

| Direction | Cells | Validator note |
|-----------|-------|----------------|
| FLIP (FAIL→PASS) | **PATENTS-q1, PATENTS-q2** (targets) | the hypothesis's 2 held target flips |
| FLIP (FAIL→PASS) | crmarenapro-q2, crmarenapro-q7, googlelocal-q2 | incidental off-target flips (q2/q7 "Found expected agent ID"; googlelocal-q2 was the long-standing non-target failer) |
| REGRESSION (PASS→FAIL) | crmarenapro-q13 | "Found agent IDs ['005…NEa3'] but expected '005…NIXC'" (wrong agent id) |
| REGRESSION (PASS→FAIL) | yelp-q4 | "Value '3.63' not found" — the confirmed variable-band cell (3/3 in the probe; wobbled here) |

**Net cells: +5 flips − 2 regressions = +3 on the board → +0.0709 stratified.** Per the smoke
calibration, the 2 regressions land on confirmed/likely variable-band cells (yelp-q4 proven variable by
the 3-draw probe; crmarenapro-q13 was 1/3 in the dab0018 probe per the determinism note) — but
attribution (lever-real vs temp=0 variance) is the analyze stage's job; this section records the facts
only.

## 3-draw confirm run (launched — detached)

Captain approved a 3-draw full CONFIRM before any promote — to separate the analyze stage's ~+3
README-attributable cells from the variable-band cells that landed favorably on the single full draw
(per the generative-lever ±0.07 calibration rule). NOT an IV change: same cycle-3 solver README (hash
`b2cae85c…`), effort high, all 12 datasets; only `trials` (1→3) and `concurrency.trials` (2→4, a
THROUGHPUT knob) change.

- **Spec:** `specs/dab0022-patents-semistructured-rules.confirm3.frozen.yaml` — `trials: 3`,
  `concurrency.trials: 4`, all 12 datasets.
- **`--explain` confirmed:** `Tasks: 12`, `reasoning_effort: "high"`, solver hash `sha256:b2cae85c…`
  → **162 cells** (12 datasets × 3 draws).
- **Handle:** `runs/.rk-handles/dab0022-confirm3-20260623-001040/`
- **PID:** 2145114 (worker alive at launch; `done` sentinel absent = running)
- **Started:** 2026-06-23T00:10:40Z. **Sentinel:** `runs/.rk-handles/dab0022-confirm3-20260623-001040/done`
  (absent until finished; `rc=0` ⇒ OK). **Log:** `…/log`. ntfy: none configured.
- **ETA:** ~**2–2.5 h** wall (162 cells; the single 54-cell draw at concurrency:2 ran ~77 min — 3× the
  cells at 2× the slots ≈ 1.5× wall, but PATENTS/crmarenapro serialize on the shared postgres volume so
  real parallelism is capped above that).

> **INFRA CAVEAT (record before the audit).** At `concurrency.trials: 4`, two draws of the SAME dataset
> can run concurrently and collide on the shared **named postgres volume** — the dab0018 crma3 signature:
> `volume … already exists but was created for project …` → that draw is **infra-killed with
> coverage_missing**. That is INFRA, **not a result**: on the phase-2 audit, EXCLUDE any such infra-killed
> draw from the per-query counts and **re-run it at `trials: 1`**. A clean read needs ≥2 clean draws per
> dataset.

**Decision rule (FO, on the `done` sentinel):** per the analyze recommendation — **PROMOTE** iff the 3
README-attributable cells (PATENTS-q1, PATENTS-q2, googlelocal-q2) hold **≥2/3 across CLEAN draws** AND
the board **median stratified ≥ anchor 0.6966**; else **CONCLUDE validated-but-NOT-promoted** (bank the
lever family, seed README unchanged). Judge by those attributed cells + the median, not a single draw's
headline.

### Confirm RESULT — decision rule NOT met → CONCLUDE validated-but-NOT-promoted

**Run dir:** `runs/dab0022-patents-semistructured-rules/e8ec7dd1bde26916` (rc=0, ~2h13m).
**Audit (AC-2): CLEAN — all 36 trials (12 datasets × 3 draws) clean**, `coverage_missing: 0`,
`tainted: 0`. No infra-kill: the infra-signature grep hits were the benign `serverSelectionTimeoutMS=5000`
parameter inside the routine Mongo healthcheck command (every Mongo trial has it), NOT failures — all
suspect trials scored normally. **Clean-draw map: 3/3 for every dataset** (no exclusions, no trials:1
re-run needed).

**Per-draw board stratified Pass@1:** draw0 **0.7985**, draw1 **0.7058**, draw2 **0.6675** →
**MEDIAN 0.7058** vs anchor 0.6966 (**+0.009**). The ~0.13 draw spread (0.6675–0.7985) IS the
generative-lever ±0.07 variance the calibration rule warned about — the single full draw's 0.7675 was a
high-ish draw, not the center.

**The 3 README-attributable cells across the 3 clean draws:**

| Cell | draw0 | draw1 | draw2 | hold-rate | ≥2/3? |
|------|-------|-------|-------|-----------|-------|
| **PATENTS-q1** | ✅ | ❌ | ✅ | **2/3** | ✅ holds |
| **PATENTS-q2** | ✅ | ❌ | ❌ | **1/3** | ❌ **FAILS** |
| **googlelocal-q2** | ✅ | ✅ | ❌ | **2/3** | ✅ holds |

**DECISION RULE NOT MET.** It required **all 3** attributed cells ≥2/3 AND median ≥ anchor. The median
clears (0.7058 ≥ 0.6966, barely), but **PATENTS-q2 holds only 1/3** — so the rule fails. Critically, the
3-draw confirm REVEALS that PATENTS-q2 is itself variable-band, not a durable flip: its 3 draws fail on
different content each time (draw1 "Code/year not found near OPTICS"; draw2 "Name fuzzy match failed for
BAKING; EDIBLE DOUGHS") — the level-4 EMA ranking computes a different CPC set per draw, exactly like
q3. So of the 3 PATENTS targets, **only q1 is durable (2/3); q2 and q3 are both variable-band.** The
single-draw analyze read (which counted q1+q2 as stable) over-credited q2 — this is precisely the
single-draw-inflation the confirm was ordered to catch.

**Durable, confound-free README signal = 2 cells (PATENTS-q1 ≥2/3, googlelocal-q2 ≥2/3).** That is real
and valuable, but it is +2 cells ≈ +0.03 stratified, and the board median sits only +0.009 above the
anchor — well inside the noise floor. The variable-band cells (PATENTS-q2/q3, crmarenapro-q2/q7/q13,
yelp-q4) wobble enough to move the board ±0.07 draw-to-draw, swamping the +2-cell signal.

**RECOMMENDATION: CONCLUDE validated-but-NOT-promoted** (mirrors dab0015). Bank the semi-structured-data
lever as a validated-actionable family with **2 durable confound-free flips** (PATENTS-q1 complete-list/
flat-record; googlelocal-q2 flat-serialization — reconfirming [[dab-flat-string-serialization-works]]),
but do NOT move `@codex-batch-baseline` — the board median is within the ±0.07 noise floor and the
headline gain is variance-dominated. Seed README unchanged. The lever's PATENTS-q1 + googlelocal-q2
mechanism is bankable for future composition.

## 5th draw (leaderboard) (launched — detached)

Captain wants a 5th draw to aggregate **5 draws of the cycle-3 README at high** for a DAB leaderboard
submission: `d0a6f64260336fff` (first full, 1 draw) + `e8ec7dd1bde26916` (confirm, 3 draws) + this draw5
(1 draw) = 5 total. NOT an IV change (same cycle-3 solver hash `b2cae85c`, effort high, 12 datasets);
this is a draw-count addition, not a hypothesis change — the CONCLUDE recommendation above stands
independent of the leaderboard aggregate.

- **Spec:** `specs/dab0022-patents-semistructured-rules.draw5.frozen.yaml` — `experiment:
  dab0022-patents-semistructured-rules-draw5` (DISTINCT label → fresh run dir; the identical frozen spec
  would collide on the deterministic run-dir hash), `trials: 1`, `concurrency.trials: 4` (safe at
  trials:1 — one instance per dataset, no same-dataset postgres-volume race).
- **`--explain` confirmed:** `Tasks: 12`, `trials 1`, `reasoning_effort: "high"`, solver hash
  `sha256:b2cae85c…` (IV unchanged), **fresh run dir
  `runs/dab0022-patents-semistructured-rules-draw5/f74c12b94f2f5172`** (distinct from d0a6f64260336fff).
- **Handle:** `runs/.rk-handles/dab0022-draw5-20260623-023350/`
- **PID:** 2520874 (worker alive at launch; `done` sentinel absent = running)
- **Started:** 2026-06-23T02:33:50Z. **Sentinel:** `runs/.rk-handles/dab0022-draw5-20260623-023350/done`
  (absent until finished; `rc=0` ⇒ OK). **Log:** `…/log`. ntfy: none configured.
- **ETA:** ~**45–60 min** wall (54 cells, trials:1, concurrency:4 — faster than the first full's ~77 min
  at concurrency:2). PATENTS the heaviest cell.

**On done (FO):** `rk audit --policy strict` (exclude any infra signature), then aggregate all 5 draws
(1 + 3 + 1) for the leaderboard submission. The 5 run dirs: `d0a6f64260336fff`, `e8ec7dd1bde26916`
(3 draws within), `f74c12b94f2f5172`.

## Leaderboard submission

**5th draw audit (AC-2): CLEAN** — `runs/dab0022-patents-semistructured-rules-draw5/f74c12b94f2f5172`,
`coverage_missing: 0`, `tainted: 0`, 12/12 datasets clean, no infra signature. Single-draw stratified
0.7771. All 5 draws are an apples-to-apples set: SAME cycle-3 solver hash `b2cae85c` at `reasoning_effort
high`, all 12 datasets.

**The 5 draws (1 + 3 + 1):**

| Draw | run dir | per-draw stratified |
|------|---------|---------------------|
| 1 (first full) | `d0a6f64260336fff` | 0.7675 |
| 2 (confirm d0) | `e8ec7dd1bde26916` | 0.7985 |
| 3 (confirm d1) | `e8ec7dd1bde26916` | 0.7058 |
| 4 (confirm d2) | `e8ec7dd1bde26916` | 0.6675 |
| 5 (draw5) | `f74c12b94f2f5172` | 0.7771 |

**Per-draw board spread:** min 0.6675 · **median 0.7675** · max 0.7985 · **mean 0.7433**
(vs anchor `@codex-batch-baseline` 0.6966, Opus incumbent 0.6536).

**AGGREGATE stratified Pass@1 over 5 draws (per-query 5-draw mean → per-dataset mean → mean of 12) =
`0.7433`** (= the per-draw mean, as expected). Per-dataset 5-draw table:

| Dataset | 5-draw mean | per-query Pass@1 (over 5 draws) |
|---------|-------------|----------------------------------|
| DEPS_DEV_V1 | 0.500 | q1 0.0 · q2 1.0 |
| GITHUB_REPOS | 0.500 | q1 0.0 · q2 0.0 · q3 1.0 · q4 1.0 |
| PANCANCER_ATLAS | 0.667 | q1 0.0 · q2 1.0 · q3 1.0 |
| PATENTS | 0.533 | **q1 0.8 · q2 0.6 · q3 0.2** |
| agnews | 0.450 | q1 1.0 · q2 0.0 · q3 0.0 · q4 0.8 |
| bookreview | 0.867 | q1 1.0 · q2 0.8 · q3 0.8 |
| crmarenapro | 0.738 | q1 1.0 · q2 0.6 · q3 0.0 · q4 1.0 · q5 1.0 · q6 0.8 · q7 1.0 · q8 0.2 · q9 0.6 · q10 1.0 · q11 1.0 · q12 0.8 · q13 0.6 |
| googlelocal | 0.950 | q1 1.0 · q2 0.8 · q3 1.0 · q4 1.0 |
| music_brainz_20k | 1.000 | q1 1.0 · q2 1.0 · q3 1.0 |
| stockindex | 1.000 | q1 1.0 · q2 1.0 · q3 1.0 |
| stockmarket | 0.800 | q1 1.0 · q2 1.0 · q3 0.4 · q4 0.6 · q5 1.0 |
| yelp | 0.914 | q1 1.0 · q2 1.0 · q3 1.0 · q4 0.6 · q5 0.8 · q6 1.0 · q7 1.0 |

**Target cells over 5 draws (corroborates the confirm):** PATENTS-q1 **4/5** (0.8), q2 **3/5** (0.6),
q3 **1/5** (0.2). googlelocal-q2 **4/5** (0.8). So PATENTS-q1 + googlelocal-q2 are durable (4/5);
PATENTS-q2 is marginal (3/5, just over half — consistent with variable-band, not a clean flip); q3 is
clearly variable (1/5). This 5-draw read REINFORCES the CONCLUDE-not-promoted verdict: the aggregate
0.7433 sits +0.047 over the anchor but the per-draw spread (0.6675–0.7985) straddles it, and only 2 cells
hold durably.

**SUBMISSION-MECHANISM QUESTION (for the captain).** The DAB leaderboard is the **upstream `benchctl`
publish flow** (`~/dataagentbench/README.md` §"Leaderboard (publishing results)"): pressing **`p`** on a
finished run in `benchctl` copies that run's `summary.md` → `results/<experiment>__<run-NNN>.md` and
appends a row to `results/LEADERBOARD.md` (date, agent, model, **aggregate score**, cost, duration);
`results/` is committed. **Key caveat:** this publishes ONE run's aggregate, not a multi-run mean — the
upstream leaderboard has no native 5-draw aggregation. So:
- The **0.7433 5-draw aggregate is OUR (more honest) statistic** — to submit it we'd publish a curated row
  noting "mean of 5 draws (0.6675–0.7985)", not a single benchctl press.
- If the captain wants a **single-run** leaderboard row via benchctl's `p`, pick the **median draw
  (0.7675, run d0a6f64260336fff)** as the representative — NOT the max (0.7985), which would
  cherry-pick the top of the variance band.
- These run dirs live under `dab/runs/` (gitignored, not `~/dataagentbench/_runs/`), so a benchctl
  publish would need the runs visible to benchctl, OR we hand-author the `results/LEADERBOARD.md` row +
  `summary.md` copy. **Captain should direct: (a) submit the 5-draw mean as a curated row, or (b) publish
  the median single run via benchctl — and confirm where benchctl reads runs from for this harness.**

### SUBMITTED — curated 5-draw-mean row (captain chose option a); local commit, NOT pushed

Captain chose the curated 5-draw-mean submission. Authored it in the `~/dataagentbench` repo to match
the existing LEADERBOARD.md schema exactly (`Date | Experiment | Run | Agent | Model | Score | Cost |
Duration | Summary`). **Committed locally only — NOT pushed; awaiting captain go-ahead for the push.**

- **`~/dataagentbench` local commit:** `cbff2b41` (branch `main`, ahead of origin by 1, not pushed).
- **LEADERBOARD.md row (newest-first, above the existing Opus-4-7 row):**
  `| 2026-06-23 | dab0022-patents-semistructured-rules | 5-draw mean | codex spacedock-solver |
  gpt-5.5 (effort high) | 204/270 (76%) — 5-draw mean, stratified 0.7433 (spread 0.6675–0.7985) |
  n/a (flat sub) | ~259m (5 draws) | [link](./dab0022-patents-semistructured-rules__5draw-mean.md) |`
- **Supporting summary artifact:** `~/dataagentbench/results/dab0022-patents-semistructured-rules__5draw-mean.md`
  — headlines the 5-draw mean (stratified 0.7433), uses the MEDIAN draw `d0a6f64260336fff` (42/54) as the
  representative per-dataset table, explicitly annotated that the published score is the 5-draw mean so the
  artifact and row are consistent.
- **Score form:** matched the existing row's `N/M (P%)` convention with the 5-draw raw-cell micro-average
  **204/270 (76%)**, and put the stratified 5-draw mean (0.7433) + spread inline in the Run/Score cells so
  it's not misread as a single run. **Cost = n/a** (codex flat OpenAI subscription — `cost_usd` is null in
  every run's summary.json; honest rather than invented). **Duration = ~259m (4h19m)** = draw1 76m47s +
  3-draw confirm 133m09s + draw5 49m05s, summed from the handle `done` sentinels (no duration field in
  summary.json).
- **Runs-visibility:** hand-authored (not a benchctl `p` publish), so the runs did NOT need to be in
  `~/dataagentbench/_runs/` — wrote `results/` directly.

**Next: captain go-ahead to push `~/dataagentbench` `cbff2b41` to origin** (DataRecce/dataagentbench).
Per the dispatch I stopped at the local commit and did not push / open a PR.

### FORMAL submission package — `dab/leaderboard_submissions/` (captain's chosen mechanism)

Captain directed the formal DAB leaderboard submission package, assembled as a NEW tracked folder
`dab/leaderboard_submissions/` (NOT under gitignored `runs/`). Two deliverables, each replicating an
existing DAB reference format; same draw→run-index mapping across both (run "0"/run-001=d0a6f64,
"1"/"2"/"3"=run-002/003/004=e8ec7dd trials 0/1/2, "4"/run-005=f74c12b).

- **Deliverable 1 — `codex-gpt-5.5_results.json`** (ref: `data/leaderboard_submissions/<model>_results.json`):
  flat list of `{dataset, query, run, answer}`, run/query as strings, answer = solver's committed answer
  recovered from each worker session. **267 entries** (target 270 — see the gap below). 2 cells had
  list-valued committed answers (bookreview run "3" q2/q3), preserved via `json.dumps`.
- **Deliverable 2 — `raw_logs/`** (ref: `~/spacedock-experiment-opus-4-8-hint/`): 12 dataset dirs ×
  run-001..run-005 = **60 run dirs**, each with `answers.json` + `codex-output.jsonl` (the codex worker
  transcript) + `codex-output.fo.jsonl` (the first-officer session) + `taint.json` + `taint.md`; plus 12
  per-dataset `summary.json`. taint all clean (matches the `rk audit` clean board). 314 files, ~31M.
- **Deviations from the references** (documented in `leaderboard_submissions/README.md`): transcript named
  `codex-output.jsonl` (ours is codex/gpt-5.5, not Claude's `claude-output.jsonl`); `summary.json`
  cost/token fields are `null` (codex flat subscription — not tracked).
- **KNOWN GAP — `PATENTS` run-005 (run index "4") q1/q2/q3 OMITTED (the 3 missing of 270).** That draw
  computed answers in a runtime `solve_dataset.py` (live-DB) and only READ `answers.json` back for
  contract checks (truncated), so the verbatim committed answer is NOT recoverable from the transcript;
  per the no-fabrication rule it is omitted (its `raw_logs/PATENTS/run-005/answers.json` carries a
  `_recovery_status: FAILED` marker, not a fabricated answer). The cell scored q1✅ q2✅ q3❌. To make it
  byte-exact, re-run that single PATENTS cell at trials:1 — **captain's call** whether the 3-cell gap
  warrants it before submission.
- **Validation:** Deliverable 1 — 267 entries, every (dataset,query,run) unique, no nulls, strings ✓.
  Deliverable 2 — 60 run dirs × 4–5 files + 12 summary.json ✓. Cross-check — Deliverable-1 run "0"
  answers byte-match `raw_logs/<ds>/run-001/answers.json` (spot-checked crmarenapro/yelp/bookreview, 0
  mismatches). Committed in the dab repo (NOT pushed).

### PATENTS draw5 re-run (launched — detached) — to fill the 267→270 gap

Captain approved re-running the one PATENTS draw5 cell to close the 3-entry gap (PATENTS run "4"
q1/q2/q3) for a byte-exact 270/270. PATENTS-only, trials:1, same cycle-3 README (the IV), fresh run dir.

- **Spec:** `specs/dab0022-patents-semistructured-rules.patents-r5.frozen.yaml` — `experiment:
  dab0022-patents-semistructured-rules-patents-r5` (DISTINCT → fresh run dir), PATENTS only, `trials: 1`,
  `concurrency.trials: 1`.
- **`--explain` confirmed:** `Tasks: 1` (PATENTS, 3 cells q1/q2/q3), `reasoning_effort: "high"`, solver
  hash `sha256:b2cae85c…` (IV unchanged), fresh run dir
  `runs/dab0022-patents-semistructured-rules-patents-r5/7e0f83df055ce078`.
- **Handle:** `runs/.rk-handles/dab0022-patents-r5-20260623-035538/` · **PID:** 2656592 (alive, `done` absent).
- **Started:** 2026-06-23T03:55:38Z. **Sentinel:** `…/done` (rc=0 ⇒ OK). ntfy: none.
- **ETA:** ~12–20 min (PATENTS is the heaviest dataset — billion-row CPC EMA + citation-graph join — but
  only 3 cells, trials:1).

**Phase-2 (FO, on done):** audit the cell; **CONFIRM the on-disk answers.json carries the FULL verbatim
q1/q2/q3 strings (not truncated)** — this is the whole point of the re-run; if it's still truncated/
computed-not-persisted, FLAG (a re-run alone won't fix it, we'd need a different recovery). Then PATCH
`codex-gpt-5.5_results.json` run "4" PATENTS q1/q2/q3 (267→270) and replace
`raw_logs/PATENTS/run-005/` with this fresh cell's transcript + answers.json + taint (drop the
`_recovery_status:FAILED` marker). Note in the README that draw5-PATENTS is a FRESH independent draw (the
original verbatim answers were unrecoverable) — honest disclosure. This is a fresh draw substituting for
the original run-005 PATENTS cell; the other 11 datasets' run-005 cells stay from f74c12b.

**PATCHED — 270/270 (re-run RECOVERY SUCCEEDED).** Run `7e0f83df055ce078` audit-CLEAN
(coverage_missing 0, tainted 0, clean). The fresh PATENTS cell scored q1✅ q2✅ q3❌ (same as the
original) AND **echoed the full verbatim answers object** in an intermediate worker print — q1 (430
chars, the 72-code list), q2 (1393, title|code|year records), q3 (255, the BLOOM ENERGY CORP / CRYSTAL
IS / SCHOWALTER pairs) — lengths matching the worker's own self-report {q1:430, q2:1393, q3:255}, so the
recovery is byte-exact, not truncated. Patched:
- `codex-gpt-5.5_results.json`: added PATENTS run "4" q1/q2/q3 → **270 entries**, re-validated (unique
  (dataset,query,run), no nulls, all strings).
- `raw_logs/PATENTS/run-005/`: replaced with the fresh cell's `answers.json` (full), `codex-output.jsonl`
  (worker) + `codex-output.fo.jsonl` (FO), `taint.json`/`taint.md` (clean); the `_recovery_status:FAILED`
  marker is gone.
- `raw_logs/PATENTS/summary.json`: run-005 stays passed=2/3 (the score was always known from the original
  reward_per_query; only the answer TEXT was missing), so the per-dataset/aggregate numbers are unchanged.
- `leaderboard_submissions/README.md`: updated note 4 to disclose run-005-PATENTS is a fresh independent
  draw (same score, full answers).

The original draw5 PATENTS cell (f74c12b) had only truncated read-backs — its verbatim answer remains
unrecoverable, which is WHY the substitution; the harness-not-persisting-answers.json is the root cause
(durable source = transcript only). The re-run worked because this draw happened to echo the full object
before writing.

## Behavioral analysis

### FULL-RUN analysis (the verdict basis) — the 6 required questions

Run `d0a6f64260336fff`, audit-clean, stratified **0.7675 vs anchor 0.6966 = +0.0709**, confound-free
(codex-vs-codex, README the sole variable). Every verdict-changed cell confirmed by committed
`answers.json` recovered from the worker session jsonl.

**Q1 — Net + full per-query ledger, both directions, with mechanism.** Net **+3 cells** (+5 flips,
−2 regressions):

| Cell | Δ | anchor→full | Mechanism (by committed artifact) | Class |
|------|---|-------------|-----------------------------------|-------|
| PATENTS-q1 | +1 | 0→1 | flat newline-list of 72 level-5 codes, built on parser-first profiling (273,364 rows parsed) + complete-list + simple-record rules | **executed-and-helped (README)** |
| PATENTS-q2 | +1 | 0→1 | flat `TITLE \| CODE \| YEAR` records, level-4 EMA, same rule stack | **executed-and-helped (README)** |
| googlelocal-q2 | +1 | 0→1 | "All names and scores matched" — the dab0015-known cell that computes correct businesses every run and fails ONLY on JSON-vs-flat output format; the simple-record/flat rules fixed the serialization | **executed-and-helped (README)** — corroborates [[dab-flat-string-serialization-works]] |
| crmarenapro-q2 | +1 | 0→1 | "Found expected agent ID ka0Wt…Eq0M" — a CRM agent-id lookup; no semi-structured rule has an obvious mechanism here | **variable-band variance** (dab0018 band) |
| crmarenapro-q7 | +1 | 0→1 | "Found expected agent ID ka0Wt…EoD3" — same | **variable-band variance** (dab0018 band) |
| crmarenapro-q13 | −1 | 1→0 | committed agent id 005Wt…NEa3 vs expected 005Wt…NIXC — wrong id, no README mechanism; known regression-prone CRM cell ([[dab-mandatory-dbt-rejected]], 1/3 in dab0018) | **variable-band variance** |
| yelp-q4 | −1 | 1→0 | committed "Restaurants, **3.6523**" (rounds to 3.65) vs GT 3.63 — same category, a near-miss average; PROVEN 3/3 PASS in the dab0022 yelp probe | **variable-band variance** (proven) |

**Only 3 of the 5 flips are README-attributable (the 2 PATENTS targets + googlelocal-q2); the 2
crmarenapro flips and BOTH regressions are variable-band variance.** Net README-attributable = **+3
real cells** (PATENTS-q1, PATENTS-q2, googlelocal-q2); the variance cells roughly wash (+2 crma flips −2
regressions = 0).

**Q2 — Smoke→full: why did PATENTS-q3 drop, what could smoke not see?** q3 PASSED the cycle-3 smoke
(committed the correct subclass `titleFull` strings, e.g. BLOOM ENERGY CORP → "PROCESSES OR MEANS, e.g.
BATTERIES, FOR THE DIRECT CONVERSION OF CHEMICAL ENERGY…") but FAILED the full draw (committed
**coarse/wrong-level** titles — BLOOM ENERGY CORP → "ELECTRIC ELEMENTS", CRYSTAL IS → "ELECTRIC
ELEMENTS", plus a shifted assignee set incl. CALIFORNIA INST OF TECHN). So fix #2's level-binding rule
LANDED in the smoke draw but the worker re-derived the title at a coarser hierarchy level on the full
draw. This is a **smoke→full fork drift on the citation-graph cell, in the variable band**: q3 is a
multi-join, level-sensitive, large-cohort (169 source pubs × 1.25M citation edges) query whose path
choice (which CPC level to read titleFull from) is not pinned by the README strongly enough to survive
temp=0 re-derivation. Smoke (single draw) cannot see this — a cell that's variable across draws will show
its PASS face in one draw and its FAIL face in another. **q3 is NOT a stable flip; treat it as variance
that happened to pass at smoke.** (The hypothesis-claim count is therefore 2/3 PATENTS targets stably
flipped, not 3/3.)

**Q3 — Already-correct-and-broken?** Yes for both regressions: crmarenapro-q13 (anchor 1) and yelp-q4
(anchor 1) were PASSING at the anchor and the variant "broke" them — but by committed artifact neither is
a README mechanism failure: q13 is a wrong CRM agent-id (no semi-structured rule touches it) and yelp-q4
is a 3.65-vs-3.63 rounding near-miss on a cell PROVEN 3/3 in the probe. Both are the variable band
giving back cells it gives elsewhere, not the lever damaging correct answers (contrast the cycle-2
stockmarket-q3 regression, which WAS a real README over-formatting bug and was fixed).

**Q4 — Was the change executed (confound attribution)?** Model held constant (codex/gpt-5.5 both sides),
effort held constant (high both sides) — so attribution is **README-vs-variance, not model-swap and not
effort**. The README was demonstrably executed: the worker's verification table shows parser-first
profiling (273,364/277,813 rows parsed), full-axis EMA, explicit citation traversal, and flat
simple-record output — the exact rule stack. The 3 README-attributable flips reach the committed answer
through that stack. The variance cells are README-independent (no matching mechanism + known band
membership).

**Q5 — Prevention + next move.** The +0.0709 headline OVERSTATES the durable lever effect: ~+3 of the
net cells are real (README) and ~0 net comes from variance cells that happened to land favorably this
draw (2 crma flips − 2 regressions). On a different seed the variance cells could net negative and drag
the headline toward the anchor. **Prevention:** judge by the 3 attributed cells, not the 0.7675 — and
confirm with a multi-draw before promoting (the dab0017 lesson: a generative lever's single full draw
carries ±0.07 variance). **Next move:** a 3-draw full (or at least a 3-draw on the moving datasets
PATENTS/crmarenapro/yelp/googlelocal) to separate the stable +3 from the variable band.

**Q6 — Smoke-vs-full fork drift.** One real instance: PATENTS-q3 (smoke PASS → full FAIL, diagnosed
above as variable-band level-binding drift). The smoke also under-counted variance generally — it saw 0
crmarenapro cells (crma not in the 4-dataset panel), so the q2/q7 flips and q13 regression were entirely
invisible to smoke. This is the standing calibration lesson: a generative fires-everywhere lever's smoke
panel is NOT a faithful predictor of the full board (dab0016/dab0017) — confirmed yet again here.

### Cycle-3 (the current read)

**Both targeted fixes landed, confound-free — this is strong evidence the lever is mechanically
steerable, not inert.** With effort=high (matching the anchor) the README is the sole variable, so the
cycle-3 movements attribute cleanly:
- **Fix #2 flipped PATENTS-q3** (0→1): the new "resolve a code's title at exactly the named hierarchy
  level" clause moved the worker off the level-5 group title onto the correct subclass title; all 3
  assignee-title pairs now match. The lever solved all 3 PATENTS targets.
- **Fix #1 restored stockmarket-q3** (the cycle-2 regression, back to 1): the "output only name+number,
  no description blurb" clause removed the free-text blurb that had broken the validator's name↔number
  proximity. The targeted scoping worked exactly as designed.
- **The 2 PATENTS flips survived the xhigh→high revert** — they were not an xhigh artifact; they are the
  README. This retroactively resolves the cycle-1 AC-1 confound in the README's favor for q1/q2.

**But the generative lever opened 2 NEW yelp regressions — the same fires-everywhere cost, now
confound-free.** yelp-q4 ("largest credit-card category + its average rating") and yelp-q7 ("top-5
categories by reviews from 2016 users") both dropped. These are **ranking/aggregation-over-derived-metric**
cells — the temp=0 *variable band*. The committed artifacts show content shifts, not format faults:
q4 committed the right category (Restaurants) with avg 3.5414 vs GT 3.63 (a cohort/aggregation
difference); q7 committed `Restaurants/Food/American (New)/Shopping/Automotive` vs GT wanting
Breakfast & Brunch in the top-5 (a ranking/attribution difference). The README's complete-list /
all-associated / "show the neighborhood, preserve ties" rules plausibly nudged the category cohort and
the tie/rank cut — which is *generative behavior on a ranking shape*, the dab0016 lesson restated: a
fires-everywhere lever perturbs the variable band in both directions.

**Net behavioral picture:** the lever now does exactly what it was designed to do on its targets
(3/3 PATENTS + the regression fix, all by artifact) AND it destabilizes a different pair of perturbable
ranking cells — a textbook generative trade. The two faults are no longer "is it inert" (clearly not) but
"can its blast radius be contained to the targets." See Failure Review for whether the yelp drops are
README-real or variable-band noise and the next-fork options.

### Cycle-1 (xhigh) — superseded; retained below

**The lever is NOT inert — it lands mechanically (refutes the G7 worry).** The cycle-2 gatekeeper's
top concern was G7: a fires-everywhere prose lever with no worked example might be discussed-and-skipped
("talks but doesn't do", the dab0012/dab0017 wall). The smoke artifacts refute that here: the worker
demonstrably *executed* the rules — parser-first (parsed all 277,813 publication rows + reported
coverage), full-year EMA axis, explicit citation-graph traversal (1.25M edges, exclusion-after-traversal),
a pre-finalize verification table (cohort/parsed/joined/distinct/output counts per query), and
flat simple-record output. The PATENTS prose rules reach the committed answer. This is a meaningfully
different outcome from the inert README families — the semi-structured discipline is **actionable** at
gpt-5.5/xhigh on these query shapes.

**Why q1/q2 flipped:** PATENTS-q1's anchor failure (per the rescore doc) was a *serialization* fault —
a JSON list that crashed the validator. The README's "format final answers as simple records … avoid
nested commentary" + "complete-list: emit every qualifying row" converted the output to a flat
newline-list the validator accepts, and the parser-first + hierarchy-level + EMA-full-axis rules got the
*content* right (all 72 level-5 codes present). q2 is the same story at level-4 with title/code/year
records. These are real, README-attributable flips — and they echo the one validated DAB lever to date
([[dab-flat-string-serialization-works]]): serialization-format IS solver-README-steerable.

**Why q3 didn't flip (closer-but-failing, not inert):** the graph traversal was correct (right citing
assignees: CRYSTAL IS INC, SCHOWALTER LEO J, BLOOM ENERGY CORP) but the worker resolved the **wrong CPC
subclass titles** — it reported the cited patent's primary level-5 *group* title where the ground truth
wants the *subclass* title. The README's "verify the meaning of each level from the dimension table"
rule fired but the worker mapped the wrong hierarchy level for the title. It then self-graded q3 PASSED
— a self-anchored false-green (the verify stage re-derived from the same wrong mapping), the recurring
no-independent-oracle wall ([[verification-without-oracle-real-world]]). One mechanical level-fix away
from a flip, not a dead end.

**Why stockmarket-q3 regressed (the generative cost, effort-confounded):** the simple-record + free-text
rules, applied to a name+number complete-list question, caused the worker to attach the company's full
free-text *description blurb* to the entity name, pushing the required avg-daily-volume number out of
the validator's name↔number proximity window. This is the predicted generative side-effect on a
perturbable shape (the G8 panel did its job — the canary fired). Per AC-1 it is **entangled with the
xhigh effort confound**: a verbose description blurb is exactly the xhigh-over-elaboration signature
([[dab-opus-vs-gpt55-behavioral-model]]), so "README simple-record rule misfired" and "xhigh
over-elaborated" point the same direction and cannot be cleanly separated on this single high-vs-xhigh
draw. Either way it is a real regression on a previously-stable passer.

**Calibration note (carries to full):** this confirms the dab0016/dab0017 lesson that a generative
fires-everywhere lever's behavior is bidirectional — it flipped 2 target cells AND regressed 1 stable
canary on the SAME run. The full 12-dataset board has many more unsmoked perturbable name+number /
complete-list / free-text cells (agnews, bookreview, music_brainz, crmarenapro, DEPS_DEV, GITHUB) that
this lever will also fire on; the smoke's +1 cell net is NOT a safe predictor of the full board.

## Failure Review

### Cycle-3 (the current verdict basis)

**Primary classification: GENERATIVE SIDE-EFFECT REGRESSION (confound-free) — the targeted fixes worked
but the lever's blast radius moved to two NEW ranking cells.** Cycle-3 is a clean win on everything it
aimed at — all 3 PATENTS targets PASS (q3 flipped via fix #2), the cycle-2 stockmarket-q3 regression is
fixed (fix #1), and the q1/q2 flips survived the effort revert so they are genuinely the README. The
fault is that the same fires-everywhere rules destabilized **yelp-q4 and yelp-q7** (both previously
stable passers at anchor-high AND cycle-1-xhigh). With effort=high there is no confound: these drops are
README-attributable ranking/aggregation shifts on the variable band, not effort.

**Why the GO bar is still not met:** GO = ≥1 PATENTS flip AND **zero** canary regression. First clause is
now overwhelmingly satisfied (3/3 PATENTS by artifact); the second fails (2 yelp regressions). So this is
not a clean GO — but it is a markedly better board than cycle-2 (targets fully solved, prior regression
fixed, only the blast-radius problem remains).

**Open question — README-real vs variable-band noise (single draw):** yelp-q4/q7 are
ranking-over-derived-metric cells in the temp=0 variable band. Two prior passes (anchor + cycle-1) then a
drop leans toward a real README-induced ranking shift, but one high draw can't fully exclude variance. A
cheap 1–3-draw yelp-only repeat would settle it before any heavier decision.

**Next-fork options (captain's call — this is genuinely on the GO/REVISE boundary):**
1. **REVISE again (tighten the blast radius):** the complete-list / all-associated / "show the
   neighborhood, preserve ties" rules are what plausibly moved the yelp rankings. Scope them so they do
   NOT alter the cohort or tie/rank cut on a single-winner "which category" or fixed top-k question
   (q4 is single-winner; q7 is top-5) — apply the full-list discipline only when the question asks for an
   open complete list, not a fixed-k ranking. This is a REVISE-class in-section edit, idea intact, and it
   directly targets both yelp drops.
2. **Disambiguate first (cheapest):** a yelp-only 1-draw repeat (or 3-draw band) at high to confirm
   whether q4/q7 are README-real or variable-band wobble. If they hold on a repeat, the regression was
   noise and the board is effectively a clean +3-target GO; if they drop again, do option 1.
3. **Accept the trade to full (captain may judge the +3-target win worth 2 ranking-cell drops):** but the
   calibration note below warns the full 12-dataset board has many more unsmoked ranking/complete-list
   cells this lever will fire on — the panel's net is NOT a safe full-board predictor (dab0016/dab0017).

**Recommendation: REVISE (option 1), optionally preceded by the option-2 yelp repeat to confirm the
drops are real before spending the edit.** Do not advance to full as-is: a fires-everywhere lever that
regressed 2 of 7 yelp cells on the smoke panel will likely regress more on the unsmoked ranking-heavy
datasets, and the stratified metric punishes that.

### Cycle-1 (xhigh) — superseded; retained below

**Primary classification: GENERATIVE SIDE-EFFECT REGRESSION on a perturbable canary (not inert, not
leak, not infra).** The lever works on its targets (2/3 PATENTS flipped by artifact) but its
fires-everywhere nature regressed a previously-stable passer (stockmarket-q3) via the simple-record +
free-text rules over-formatting a name+number answer — exactly the failure mode the G8 panel was built
to surface. Secondary: PATENTS-q3 is a closer-but-failing self-anchored false-green (wrong CPC hierarchy
level for the subclass title).

**Why the GO bar is not met:** GO requires ≥1 PATENTS flip AND **zero** canary regression. The first
clause is satisfied (q1, q2 by committed artifact); the second is not (stockmarket-q3 1→0). So this is
not a clean GO.

**Confound caveat (AC-1):** the run is xhigh vs the high anchor. The 2 PATENTS flips are README+xhigh
*jointly*, and the stockmarket-q3 regression is README-rule *or* xhigh-over-elaboration (entangled,
same direction). Neither the flip nor the regression is cleanly attributable to the README alone without
an xhigh-minus-section baseline.

**Next-fork decision — REVISE (back to `hypothesis`), do not conclude and do not advance to full as-is.**
Two independent, mechanically-fixable faults, both addressable without abandoning the idea:
1. **Scope the simple-record/free-text rules to suppress the regression.** The "simple records / exact
   database values for names" rule should explicitly forbid pulling free-text *description* fields into a
   name+number answer (emit the name token only, then the number). This is the one rule that caused the
   canary drop; tightening it is a REVISE-class in-place edit, idea unchanged.
2. **Fix PATENTS-q3's hierarchy-level resolution** — the "verify the meaning of each level from the
   dimension table" rule needs to bind the *subclass* title (not the level-5 group title) for citation
   questions; a worked-example or a sharper level-binding instruction would likely flip q3 too (turning
   the panel from +2/−1 into a potential +3/0).

**Decoupling recommendation for the captain (re the confound):** before or alongside the REVISE, run an
**xhigh-minus-section baseline** (the anchor README at xhigh) on this same 4-dataset panel. If
stockmarket-q3 *also* regresses at xhigh-without-the-section, the drop is effort, not the README, and
the rule-scoping fix in (1) is unnecessary; if it holds at xhigh-without-section, the regression is the
README and (1) is required. This single $0-cheap-to-launch control disentangles AC-1's confound and tells
us whether the 2 PATENTS flips are the README or the effort.

## Follow-up Routing

**Verdict recommendation: PROMOTE-CANDIDATE, but NOT-yet on a single draw — confirm with a 3-draw full
first.** This is the strongest DAB result to date and the first genuinely lever-attributable multi-cell
gain, but a single full draw's +0.0709 is not yet trustworthy enough to promote outright.

**Why it's a real result (the case FOR):**
- **3 cells are README-attributable by committed artifact, confound-free** (codex-vs-codex, high-vs-high):
  PATENTS-q1, PATENTS-q2 (the targets), and googlelocal-q2 (the dab0015-known serialization cell). The
  README rule stack (parser-first / complete-list / flat simple-record / level-binding) demonstrably
  reached each committed answer.
- This **validates the semi-structured-data lever family** as actionable at gpt-5.5/high — refuting the
  G7 "abstract prose goes inert" worry (dab0012/dab0017). It also independently **reconfirms
  [[dab-flat-string-serialization-works]]** (googlelocal-q2 via flat serialization), composing two
  validated mechanisms in one README.

**Why NOT to promote on this draw (the case for one more confirm):**
- The **+0.0709 headline overstates the durable effect.** Decompose: ~+3 real (README) cells + a
  net-~0 from variable-band cells that happened to land favorably (crmarenapro-q2/q7 flipped, but
  crmarenapro-q13 + yelp-q4 regressed — all four are variance, not mechanism). On another seed the
  variance cells could net negative, dragging the headline toward the anchor. The **honest durable lever
  estimate is ~+3 cells ≈ +0.04 stratified**, not +0.0709.
- **PATENTS-q3 did NOT stably flip** — it was a smoke→full fork-drift (variable-band level-binding), so
  the hypothesis claim is 2/3 targets, not 3/3.
- The standing DAB calibration rule ([[dab-mandatory-dbt-rejected]], [[dab-determinism-lever-family-dead]]):
  **a generative fires-everywhere lever's single full draw carries ±0.07 variance — judge by attributed
  per-query mechanism, never a single-draw headline.** Promoting on one draw would repeat the exact error
  those notes warn against.

**Recommended next move (cheap, decisive):** a **3-draw full** at `concurrency.trials: 1` (or, to save
budget, a 3-draw on just the moving datasets PATENTS + crmarenapro + yelp + googlelocal + the 3 stable
anchors). Decision rule: if PATENTS-q1/q2 + googlelocal-q2 hold ≥2/3 AND the board median stays ≥ anchor,
**PROMOTE** (set `@codex-batch-baseline` → this README; it becomes the new codex anchor with a genuine
+3-cell mechanism). If the 3 attributed cells wobble or the variance cells net the board back to ~anchor,
**CONCLUDE validated-but-NOT-promoted** (bank the semi-structured lever as a proven-actionable family for
future composition, like dab0015 — seed README unchanged).

**Do NOT REVISE** — there is no mechanism bug to fix (the cycle-2 stockmarket-q3 regression was the only
real README bug, and it's fixed; the current regressions are variance). The only open question is
durability, which a confirm draw answers, not a re-author.

**This is the captain's call** — I write the recommendation; the FO presents it. I did not edit the seed
README, promote, or conclude.

## Verdict

_Pending captain decision at the analyze gate. **UPDATED after the 3-draw confirm — Ensign
recommendation: CONCLUDE validated-but-NOT-promoted.** The confirm decision rule was NOT met:
PATENTS-q2 held only 1/3 across clean draws (revealed as variable-band, not a durable flip), so the
"all 3 attributed cells ≥2/3" clause fails; board median 0.7058 clears the anchor 0.6966 by only +0.009
(inside the ±0.07 noise floor). Durable confound-free signal = 2 cells (PATENTS-q1 2/3 + googlelocal-q2
2/3) ≈ +0.03, variance-swamped. Bank the semi-structured-data lever as a validated-actionable family
(2 durable flips, reconfirms [[dab-flat-string-serialization-works]]); do NOT move @codex-batch-baseline;
seed README unchanged. This is the captain's call — recommendation only; I did not promote/conclude/edit
the registry or seed._

_(Prior single-draw analyze recommendation was PROMOTE-CANDIDATE-pending-confirm; the confirm correctly
caught that the single draw over-credited PATENTS-q2 — the system worked as designed.)_

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

## Stage Report: smoke (phase 2 — audit + score + deep-dive)

- DONE: Audit (AC-2) — `rk audit --policy strict` on `runs/dab0022-patents-semistructured-rules/e5cb461ef07e9322`; record clean/coverage_missing/tainted; then `rk score` in `## Smoke result`.
  CLEAN: `coverage_missing: 0`, `tainted: 0`, all 4 trials clean. Score 0.8042 (4-dataset panel only). Recorded in `## Smoke result`.
- DONE: Per-target deep-dive (PATENTS q1/q2/q3) — verdict vs `@codex-batch-baseline`, validator distance-to-pass, committed artifact, classify each; write `## Smoke result` table + `## Behavioral analysis`.
  q1 +1 FLIP (flat-list serialization + complete-list reached the answer), q2 +1 FLIP (level-4 records), q3 still 0 (closer-but-failing: correct graph traversal, wrong CPC subclass title level; self-anchored false-green). All verified against the committed answers recovered from the worker session jsonl, not just the reward.
- DONE: Canary read + gate verdict — check all 15 canaries for drops; attribute README vs xhigh per AC-1; give go/no-go; on regression append `## Failure Review`; lead with plain-words go/no-go.
  1 regression: stockmarket-q3 1→0 (simple-record/free-text rule pulled a description blurb into a name+number answer; entangled with xhigh over-elaboration per AC-1). yelp 7/7 + googlelocal q1/q3/q4 held. Verdict NO-GO-as-is → REVISE to `hypothesis`; `## Failure Review` appended with primary classification + the rule-scoping + q3 level-fix forks + an xhigh-minus-section decoupling control.

### Summary

Audit clean (AC-2 PASS). The lever is genuinely actionable at gpt-5.5/xhigh — it flipped PATENTS-q1 and q2 FAIL→PASS by committed artifact (refuting the G7 inert-risk worry), with PATENTS-q3 closer-but-failing on a wrong CPC-hierarchy-level title (self-anchored false-green). But its generative nature regressed a stable canary, stockmarket-q3 (the simple-record + free-text rules over-formatted a name+number answer with a description blurb), so the zero-regression GO clause is not met → REVISE back to `hypothesis`. Both faults are mechanically fixable (scope the simple-record rule to exclude free-text description fields; bind the subclass title at the right level for q3). AC-1 confound stands: flips are README+xhigh jointly and the regression is README-rule-or-xhigh (same direction) — recommend an xhigh-minus-section baseline on this panel to disentangle before the REVISE re-smoke.

## Stage Report: propose (cycle 3 — REVISE re-author: two README fixes + effort→high)

- DONE: README fix #1 (stockmarket-q3 regression) — scope the simple-record/all-associated rule so it does NOT pull free-text description fields into a name+number answer; keep the number adjacent to the name; rest of section byte-intact.
  Appended a clause to the "Format final answers as simple records…" bullet: for "for each X report its Y" questions, output only the exact name + that number kept adjacent; do not insert free-text description/summary fields. README diff stays addition-only (`88a89,101`), leak-guard byte-intact.
- DONE: README fix #2 (PATENTS-q3) — bind the CPC subclass title at the correct hierarchy level from the dimension table (q3 reported the level-5 group title, not the subclass).
  Appended a clause to the graph/citation bullet: when the question asks for a code's title at a named hierarchy level (e.g. subclass title), resolve the title at exactly that level — do not substitute a finer/coarser level's title.
- DONE: Effort → high in BOTH specs; re-freeze both; confirm `high` in both frozen; update AC-1 (now 2 fields, sole variable, confound removed, supersedes xhigh addendum); re-run the gatekeeper (cycle-3); re-confirm smoke selection via `--explain`; record the captain's REVISE rationale.
  Both specs reverted xhigh→high, re-frozen; `grep reasoning_effort …frozen …smoke.frozen` = `high` in both. Full-spec diff vs anchor = exactly 2 fields (`experiment:` + `solver_workflow:`). New solver hash `sha256:b2cae85c…` (was `ff279bd8…`). `--explain` → `Tasks: 4`, `reasoning_effort: "high"`. AC-1/AC-3 updated (cycle-2 xhigh block marked SUPERSEDED; confound removed; README genuinely isolated again). Cycle-3 gatekeeper (Reviewed 2026-06-22T12:25:00Z) recommends **APPROVE**, G3 clean two-field PASS (no override), G7 WARN softened; block in `## Gatekeeper review`. Captain's REVISE rationale (regression = README, effort→high for clean isolation) recorded in AC-1.

### Summary

REVISE cycle 3 re-author: kept the one idea (semi-structured data rules), applied two in-section scoping fixes — fix #1 forbids pulling free-text description blurbs into name+number answers (targets the stockmarket-q3 regression), fix #2 binds a code's title at the exact named hierarchy level (targets PATENTS-q3's wrong-level title) — and reverted `reasoning_effort` xhigh→high in both specs. The effort revert restores the workflow invariant: the full spec differs from the anchor in only two fields (`experiment:` + `solver_workflow:`), the README is once again the sole variable, and the AC-1/AC-3 confound is removed (clean README attribution restored). Both specs re-frozen at `high`, new solver hash, smoke selection unchanged (4 datasets), gatekeeper cycle-3 APPROVE (no FAILs; G7 WARN softened by fix #1's concrete instruction but standing for the remaining abstract bullets). Ready for the cycle-3 smoke re-launch.

## Stage Report: smoke (cycle 3 — launch, detached)

- DONE: Re-confirm selection ($0) via `--explain` = 4 datasets (PATENTS + stockmarket + yelp + googlelocal), reasoning_effort "high"; launch DETACHED via `drivers/rk-run-detached.sh dab0022-smoke2 …smoke.frozen.yaml run`; record handle + pid + concrete ETA.
  `--explain` → `Tasks: 4`, `reasoning_effort: "high"`, solver hash `sha256:b2cae85c…` (cycle-3 README). Launched: handle `runs/.rk-handles/dab0022-smoke2-20260622-150545/`, pid 1853402 (alive, `done` absent), started 2026-06-22T15:05:45Z. ETA ~35–45 min (high; cycle-1 ran ~44 min). Recorded in `## Smoke run cycle-3 (launched — detached)`. Did NOT poll/wait — handle returned to the FO immediately.

### Summary

Re-confirmed the cycle-3 smoke selection at $0 (4 datasets, effort high, new solver hash b2cae85c) and launched the re-smoke detached via the standard driver. Worker pid 1853402 alive, `done` sentinel absent; handle recorded for the FO's sentinel scan. Returned the handle immediately per the launch-phase contract; phase 2 (audit/score/deep-dive) runs when the FO re-engages on the sentinel. This cycle has NO effort confound (high matches the anchor), so all phase-2 attributions are clean — the three watch-items: fix #1 holds stockmarket-q3, the 2 PATENTS flips survive the effort revert, and possibly fix #2 flips PATENTS-q3.

## Stage Report: smoke (cycle 3 — phase 2: audit + score + deep-dive)

- DONE: Audit (AC-2) — `rk audit --policy strict` on `runs/dab0022-patents-semistructured-rules/2c614e7b01ec1b31`; record clean/coverage_missing/tainted; then `rk score` → cycle-3 `## Smoke result`.
  CLEAN: `coverage_missing: 0`, `tainted: 0`, all 4 trials clean. Panel score 0.8661 (up from cycle-1 0.8042). Recorded in `## Smoke result` → "Cycle-3" subsection.
- DONE: Per-target + canary deep-dive vs `@codex-batch-baseline`, all by committed artifact — (a) fix #1 restored stockmarket-q3? (b) PATENTS q1/q2 flips survived xhigh→high? (c) fix #2 flipped PATENTS-q3? + all 15 canaries for new drops.
  (a) YES stockmarket-q3 1 (name+number, no blurb). (b) YES q1/q2 held. (c) YES PATENTS-q3 flipped 0→1 (subclass-title level bound). NEW: yelp-q4 1→0 (avg 3.5414 vs GT 3.63) + yelp-q7 1→0 (top-5 missing Breakfast & Brunch) — both ranking/aggregation content shifts, verified against committed answers. Cycle-3 `## Smoke result` table + `## Behavioral analysis`.
- DONE: Gate verdict (plain words), single-draw variance flagged; on regression append `## Failure Review`.
  Verdict: NO-GO-as-is → REVISE (option 1: scope full-list/ranking rules off fixed-k questions), optionally preceded by a cheap yelp-only repeat to confirm the q4/q7 drops are README-real vs variable-band noise. `## Failure Review` cycle-3 subsection appended with the boundary-case framing and 3 next-fork options. Flagged yelp-q4/q7 as variable-band ranking cells (single high draw can't fully exclude temp=0 wobble; 2 prior passes lean toward README-real).

### Summary

Cycle-3 audit CLEAN. The two targeted README fixes both worked, confound-free (effort=high): all 3 PATENTS targets now PASS (fix #2 flipped q3), the cycle-2 stockmarket-q3 regression is fixed (fix #1), and the q1/q2 flips survived the effort revert so they are genuinely the README. But the fires-everywhere lever opened 2 NEW yelp regressions (q4, q7 — ranking/aggregation variable-band cells), so the strict zero-regression GO clause is still unmet → REVISE (tighten the full-list/ranking rules to not perturb fixed-k questions), optionally after a cheap yelp repeat to confirm the drops are real. This is on the GO/REVISE boundary — targets fully solved, only blast-radius containment remains; do not advance to full as-is (the unsmoked ranking-heavy datasets would likely regress further).

## Stage Report: smoke (cycle 3 — yelp confirm probe launch, detached)

- DONE: Build a yelp-only 3-draw probe spec — fork the cycle-3 frozen spec to yelp-only, `trials: 3`, `concurrency.trials: 1`, SAME variant solver_workflow + effort high; freeze; `--explain` to confirm yelp only / trials=3 → 21 cells / effort high / solver hash b2cae85c.
  Built `specs/dab0022-patents-semistructured-rules.yelp3.yaml` + frozen; `--explain` → `Tasks: 1` (yelp), `trials: 3`, `concurrency.trials: 1`, `reasoning_effort: "high"`, solver hash `sha256:b2cae85c…` (= cycle-3 hash, no IV change). 21 cells (7×3).
- DONE: Launch detached via `drivers/rk-run-detached.sh dab0022-yelp3 …yelp3.frozen.yaml run`; record handle + pid + ETA; return immediately, do NOT poll.
  Launched: handle `runs/.rk-handles/dab0022-yelp3-20260622-170140/`, pid 1915756 (alive, `done` absent), started 2026-06-22T17:01:40Z. ETA ~25–40 min (3 serial draws, high). Recorded in `## Yelp confirm probe (launched — detached)` with the decision rule. Did NOT poll/wait — handle returned to the FO.

### Summary

Built and launched the captain-chosen yelp-only 3-draw confirm probe (same cycle-3 README + effort high, only task set + trials changed) to settle whether the cycle-3 yelp-q4/q7 drops are README-real or temp=0 variable-band noise. trials:3 / concurrency.trials:1 (serial — avoids the postgres-volume collision per the dab0018 crma3 lesson). `--explain` confirmed yelp-only, 21 cells, effort high, the cycle-3 solver hash. Worker pid 1915756 alive, handle recorded; returned immediately per the launch-phase contract. Decision rule recorded: q4/q7 stable-drop ⇒ README-real ⇒ option-1 scope-fix REVISE; q4/q7 wobble ⇒ noise ⇒ effectively a clean +3-target GO. FO owns the wait via the sentinel scan.

## Stage Report: smoke (cycle 3 — yelp confirm probe analysis)

- DONE: Audit (AC-2) — `rk audit --policy strict` on `runs/dab0022-patents-semistructured-rules/f18986d467555a33`; record clean/coverage_missing/tainted; exclude any infra-killed draw; confirm ≥2 clean draws.
  CLEAN: `coverage_missing: 0`, `tainted: 0`; ALL 3 draws clean (none excluded) → full 3-draw read.
- DONE: q4/q7 per-draw read across the clean draws (+ full yelp 7-query totals per draw); pass-count vs anchor 7/7; verify by committed artifact where a flip is in question.
  yelp-q4 **3/3 PASS** ("Found: Restaurant, 3.63" each draw), yelp-q7 **3/3 PASS** ("All categories present" each draw). Per-draw totals 7/7, 6/7, 7/7 (the 1 drop was yelp-q2, a different variable-band cell). Per-draw table in `## Yelp confirm probe` → "Probe RESULT".
- DONE: Verdict per the decision rule + plain-words summary; lead with the case + counts.
  **WOBBLE** (q4=3/3, q7=3/3 pass — unanimous) → the cycle-3 yelp drops were temp=0 variable-band NOISE, not README. Board is effectively a **clean +3-PATENTS-target GO**; no option-1 REVISE needed. Recorded in `## Yelp confirm probe` → "VERDICT".

### Summary

The yelp-only 3-draw probe is unambiguous: all 3 draws clean (AC-2), and yelp-q4 + yelp-q7 BOTH pass 3/3 (q4 hits the exact GT 3.63 every draw; q7 has all categories every draw). The cycle-3 single-draw yelp drops were temp=0 variable-band noise, NOT a README regression — confirmed by the decision rule's wobble branch. So the dab0022 cycle-3 smoke is effectively a CLEAN +3-PATENTS-target GO: all 3 targets flipped FAIL→PASS by committed artifact (confound-free at high), the cycle-2 stockmarket-q3 regression genuinely fixed, no real canary loss. Recommendation to the FO: advance smoke→full (the captain pre-authorized this on a confirmed wobble). Carry the calibration caveat that yelp's ranking cells (q2/q4/q7) are variable-band, so isolated single-cell ranking wobbles on the full board are variance, not lever regressions, unless they reproduce.

## Stage Report: full (launch — detached)

- DONE: Re-confirm $0 selection via `--explain` = all 12 datasets / 54 cells, reasoning_effort "high", solver hash = the cycle-3 hash `sha256:b2cae85c…`; launch DETACHED via `drivers/rk-run-detached.sh dab0022-full …frozen.yaml run`; record handle + pid + ETA.
  `--explain` → `Tasks: 12`, `reasoning_effort: "high"`, solver hash `sha256:b2cae85c…` (cycle-3 fixed README). Launched: handle `runs/.rk-handles/dab0022-full-20260622-174918/`, pid 1973989 (alive, `done` absent), started 2026-06-22T17:49:18Z. ETA ~75–90 min (54 cells, high, concurrency.trials:2; dab0018 full3 same shape ~81 min). Recorded in `## Full run (launched — detached)`. Did NOT poll/wait — handle returned to the FO immediately.

### Summary

Re-confirmed the full-board selection at $0 (12 datasets / 54 cells, effort high, cycle-3 solver hash b2cae85c) and launched the detached full run via the standard driver. Worker pid 1973989 alive, `done` sentinel absent; handle recorded for the FO's sentinel scan. Returned the handle immediately per the launch-phase contract; phase 2 (audit/score/diff/per-cell read) runs when the FO re-engages on the sentinel. README is the SOLE variable vs the high anchor (confound-free). Calibration carried: judge by attributed per-query mechanism, not the headline delta — the +3 PATENTS flips are the real signal; variable-band ranking wobbles are variance unless they reproduce.

## Stage Report: full (phase 2 — audit + score + diff)

- DONE: Audit (AC-2), gate the verdict — `rk audit --policy strict` on `…/d0a6f64260336fff`; exclude BOTH dab-postgres degradation signatures; all 12 datasets present + healthy.
  CLEAN: `coverage_missing: 0`, `tainted: 0`; all 12 datasets clean, 54/54 cells scored; grep for host-name/refused/serverSelectionTimeout/unhealthy across every reward_per_query = NONE. Run is VALID, NOT inconclusive. Recorded in `## Run result`.
- DONE: Score + diff (audit clean) — `rk score --format json` (vs Opus ~0.6536) and paired delta vs `@codex-batch-baseline`; record run-dir + stratified + delta + PATENTS q1/q2/q3 in `## Run result`.
  Stratified 0.7675 vs anchor 0.6966 = **+0.0709** (clears Opus 0.6536 by +0.114). Paired ledger computed slug-paired from summary.json (rk runs diff not needed): 5 flips (PATENTS-q1/q2 targets + crmarenapro-q2/q7 + googlelocal-q2), 2 regressions (crmarenapro-q13, yelp-q4). PATENTS verdict q1 ✅ / q2 ✅ / **q3 ❌** (q3 PASSED in cycle-3 smoke but did NOT hold on the full draw). Recorded in `## Run result`.

### Summary

Full run audit-clean (AC-2): all 12 datasets present and healthy, no PG/Mongo degradation signature, so the board is trustworthy — proceed to analyze. Headline 0.7675 stratified, +0.0709 vs the high codex anchor (confound-free, README sole variable) and +0.114 over the Opus incumbent. 2 of the 3 PATENTS targets flipped and HELD (q1, q2); PATENTS-q3 PASSED in the cycle-3 smoke but did NOT hold on the full draw (single-draw movement on the citation-graph cell). Off-target: +crmarenapro-q2/q7 +googlelocal-q2 flipped, −crmarenapro-q13 −yelp-q4 regressed (both on confirmed/likely variable-band cells). Net +3 cells. Facts only — the lever-real-vs-variance attribution for q3 and the 4 off-target cells is the analyze stage's job; did NOT do the behavioral deep-dive per the dispatch.

## Stage Report: analyze

- DONE: Confirm + attribute every verdict-changed cell by committed artifact, both directions; verify the 2 PATENTS target flips reached the committed answer via the semi-structured rules; diagnose PATENTS-q3 smoke→full separately; check the 2 regressions against variable-band evidence.
  All 7 cells classified from recovered committed `answers.json`: README-attributable = PATENTS-q1, PATENTS-q2, googlelocal-q2 (3 cells); variable-band variance = crmarenapro-q2/q7 (flips), crmarenapro-q13 + yelp-q4 (regressions). PATENTS-q3 = smoke→full fork drift (smoke committed correct subclass titleFull; full committed coarse "ELECTRIC ELEMENTS" wrong-level titles + shifted assignees) → variable-band, NOT a stable flip. yelp-q4 = "Restaurants, 3.6523" near-miss vs GT 3.63 (proven 3/3 in the probe).
- DONE: Answer all 6 required analyze questions in `## Behavioral analysis` (FULL-RUN subsection).
  Q1 ledger+mechanism, Q2 q3 smoke→full drift, Q3 already-correct-and-broken (both regressions were anchor-PASS but variance not mechanism), Q4 executed+confound (model AND effort held constant → README-vs-variance), Q5 prevention+next (durable ≈ +3 cells ≈ +0.04, confirm with 3-draw), Q6 fork drift (q3 + crma invisible to smoke).
- DONE: `## Follow-up Routing` + verdict recommendation + plain-words captain summary; honest about single-draw trustworthiness.
  Recommendation: PROMOTE-CANDIDATE but NOT-yet on one draw → run a 3-draw confirm; promote iff the 3 attributed cells hold ≥2/3 and board median ≥ anchor, else CONCLUDE-validated-not-promoted. Do NOT REVISE (no mechanism bug). Did NOT edit seed README / promote / conclude — captain's call.

### Summary

Airtight per-cell attribution by committed artifact: of the +5/−2 ledger, exactly **3 flips are
README-attributable and confound-free** (PATENTS-q1, PATENTS-q2, googlelocal-q2 — the rule stack reached
each committed answer, model+effort held constant), while the 2 crmarenapro flips and BOTH regressions
are variable-band variance (no matching mechanism + known band membership; yelp-q4 proven 3/3 in the
probe). PATENTS-q3 was a smoke→full fork drift (correct subclass title at smoke, coarse wrong-level title
at full), so 2/3 targets stably flipped, not 3/3. The +0.0709 headline overstates the durable lever
effect (~+3 cells ≈ +0.04 after removing the variance cells that happened to land favorably). This is the
strongest, first genuinely lever-attributable DAB result — recommend PROMOTE-CANDIDATE pending a 3-draw
confirm, NOT a single-draw promote (per the generative-lever ±0.07 calibration rule). Captain's call; I
wrote the recommendation only.

## Stage Report: analyze (3-draw confirm launch — detached)

- DONE: Build the 3-draw confirm spec — fork the cycle-3 frozen spec, `trials: 3`, `concurrency.trials: 4` (throughput knob, NOT IV), SAME solver_workflow + effort + all 12 datasets; freeze; `--explain` to confirm 12×3=162 cells / effort high / solver hash b2cae85c.
  Built `specs/dab0022-patents-semistructured-rules.confirm3.{yaml,frozen.yaml}`; `--explain` → `Tasks: 12`, `trials: 3`, `concurrency.trials: 4`, `reasoning_effort: "high"`, solver hash `sha256:b2cae85c…` → 162 cells.
- DONE: Launch detached via `drivers/rk-run-detached.sh dab0022-confirm3 …confirm3.frozen.yaml run`; record handle + pid + ETA + the infra caveat; return immediately, do NOT poll.
  Launched: handle `runs/.rk-handles/dab0022-confirm3-20260623-001040/`, pid 2145114 (alive, `done` absent), started 2026-06-23T00:10:40Z. ETA ~2–2.5 h. Recorded in `## 3-draw confirm run (launched — detached)` with the postgres-volume infra caveat + the PROMOTE/CONCLUDE decision rule. Did NOT poll/wait — handle returned to the FO.

### Summary

Built and launched the captain-approved 3-draw full confirm (concurrency.trials:4 for throughput — not an IV; same cycle-3 README, effort high, 12 datasets, 162 cells) to verify the single-draw +0.0709 before any promote. Worker pid 2145114 alive, handle recorded; returned immediately per the launch-phase contract. Recorded the concurrency:4 postgres-volume collision caveat (exclude any infra-killed draw, re-run at trials:1) and the decision rule: PROMOTE iff PATENTS-q1/q2 + googlelocal-q2 hold ≥2/3 across clean draws AND board median ≥ anchor 0.6966, else CONCLUDE validated-but-not-promoted. FO owns the wait via the sentinel scan.

## Stage Report: analyze (3-draw confirm analysis)

- DONE: Audit (AC-2) + infra exclusion — `rk audit --policy strict` on `…/e8ec7dd1bde26916`; exclude same-dataset postgres-volume collisions + PG/Mongo abstains; per-dataset clean-draw count; flag any dataset <2 clean.
  CLEAN: all 36 trials clean, `coverage_missing: 0`, `tainted: 0`. Infra-signature grep hits = benign Mongo healthcheck `serverSelectionTimeoutMS=5000` params (all suspect trials scored normally), NOT kills. Clean-draw map: 3/3 for every dataset — no exclusions, no trials:1 re-run needed.
- DONE: Per-cell + board read across clean draws — hold-rate for PATENTS-q1/q2 + googlelocal-q2; per-draw board stratified + median vs anchor 0.6966.
  Per-draw board: 0.7985 / 0.7058 / 0.6675 → MEDIAN 0.7058 (anchor +0.009). Hold-rates: PATENTS-q1 2/3 ✅, PATENTS-q2 **1/3 ❌** (revealed variable-band — fails on different content each draw), googlelocal-q2 2/3 ✅. Recorded in `## 3-draw confirm run` → "Confirm RESULT".
- DONE: DECISION + recommendation; did NOT promote/conclude/edit registry or seed.
  Decision rule NOT met (PATENTS-q2 <2/3). Recommendation: **CONCLUDE validated-but-NOT-promoted** — bank 2 durable confound-free flips (PATENTS-q1 + googlelocal-q2), do NOT move `@codex-batch-baseline`, seed unchanged. Recorded in `## 3-draw confirm run` + `## Verdict`.

### Summary

The 3-draw confirm is decisive and audit-clean (36/36 trials clean, 3/3 per dataset). It does NOT meet the promote rule: PATENTS-q2 held only 1/3 (the confirm revealed it as variable-band, not the durable flip the single draw suggested — the level-4 EMA ranking computes a different CPC set per draw), and the board median 0.7058 clears the anchor by only +0.009 (inside the ±0.07 noise floor). Durable confound-free README signal = 2 cells (PATENTS-q1 + googlelocal-q2) ≈ +0.03, variance-swamped. Recommendation: CONCLUDE validated-but-NOT-promoted — bank the semi-structured lever family (2 durable flips, reconfirms flat-string serialization) without moving the anchor. The confirm worked exactly as designed: it caught the single-draw inflation of PATENTS-q2. Captain's call; recommendation only.

## Stage Report: analyze (5th draw — leaderboard launch, detached)

- DONE: Build the 5th-draw spec with a fresh run dir — fork the cycle-3 frozen spec, DISTINCT `experiment: …-draw5`, `trials: 1`, `concurrency.trials: 4`, SAME solver_workflow (IV) + effort + 12 datasets; freeze; `--explain` to confirm 54 cells / trials 1 / effort high / solver hash b2cae85c / a NEW run-dir.
  Built `specs/dab0022-patents-semistructured-rules.draw5.{yaml,frozen.yaml}`; `--explain` → `Tasks: 12`, trials 1, effort high, solver hash `b2cae85c…`, fresh run dir `runs/dab0022-patents-semistructured-rules-draw5/f74c12b94f2f5172` (distinct from d0a6f64260336fff). ✓
- DONE: Launch detached via `drivers/rk-run-detached.sh dab0022-draw5 …draw5.frozen.yaml run`; record handle + pid + ETA; return immediately, do NOT poll.
  Launched: handle `runs/.rk-handles/dab0022-draw5-20260623-023350/`, pid 2520874 (alive, `done` absent), started 2026-06-23T02:33:50Z. ETA ~45–60 min. Recorded in `## 5th draw (leaderboard) (launched — detached)`. Did NOT poll/wait — handle returned to the FO.

### Summary

Built and launched the 5th full draw for the DAB leaderboard aggregate (5 draws total of the cycle-3 README at high: 1 first-full + 3 confirm + this). Used a distinct experiment label (…-draw5) so it gets a fresh run dir f74c12b94f2f5172 (the identical frozen spec would collide on the deterministic run-dir hash); IV unchanged (same solver hash b2cae85c). trials:1/concurrency:4 is race-safe. Worker pid 2520874 alive; handle returned immediately per the launch-phase contract. This is a draw-count addition for the leaderboard, NOT a hypothesis change — the CONCLUDE validated-but-NOT-promoted recommendation stands. FO owns the wait; on done, audit then aggregate the 5 draws.

## Stage Report: analyze (5-draw leaderboard aggregate)

- DONE: Audit the 5th draw (AC-2) — `rk audit --policy strict` on `…-draw5/f74c12b94f2f5172`; confirm clean, all 12 datasets; exclude any infra signature.
  CLEAN: `coverage_missing: 0`, `tainted: 0`, 12/12 datasets clean, no infra signature. Single-draw 0.7771. No exclusion.
- DONE: Aggregate all 5 clean draws (1 + 3 + 1) — per-query 5-draw Pass@1, aggregate stratified + per-draw spread, confirm same solver hash b2cae85c at high; leaderboard table per-dataset + overall.
  All 5 cells×draws verified (every cell exactly 5 draws). Aggregate stratified **0.7433**; per-draw spread min 0.6675 / median 0.7675 / max 0.7985 / mean 0.7433. Target cells over 5: PATENTS-q1 4/5, q2 3/5, q3 1/5, googlelocal-q2 4/5. Full per-dataset/per-query table in `## Leaderboard submission`.
- DONE: Report + surface the submission-mechanism question; do NOT promote/edit seed.
  DAB leaderboard = upstream benchctl `p` publish (one run's summary.md → results/ + LEADERBOARD.md row, aggregate score; no native multi-run mean). Surfaced 2 options for the captain (submit the 5-draw mean as a curated row, or publish the median single run d0a6f64=0.7675 via benchctl) + the runs-location caveat. CONCLUDE-not-promoted stands; seed/@baseline untouched.

### Summary

5th draw audit-clean; all 5 draws aggregate apples-to-apples (same cycle-3 hash b2cae85c at high, 12 datasets). Aggregate stratified Pass@1 over 5 draws = 0.7433 (vs anchor 0.6966, Opus 0.6536), per-draw spread 0.6675–0.7985 (median 0.7675). The 5-draw read reinforces CONCLUDE-not-promoted: PATENTS-q1 (4/5) + googlelocal-q2 (4/5) are durable, PATENTS-q2 marginal (3/5), q3 variable (1/5); the +0.047 aggregate sits inside a per-draw spread that straddles the anchor. Surfaced the leaderboard submission mechanism (upstream benchctl publish, one-run aggregate — no native 5-draw mean) and recommended the median single run (0.7675) if a single benchctl row is wanted, else a curated 5-draw-mean row; flagged that these run dirs are under dab/runs/ (gitignored) so benchctl's run source needs confirming. Did not promote or edit the seed — that's the captain's call.

## Stage Report: analyze (leaderboard row — curated 5-draw-mean, local only)

- DONE: Read the leaderboard format first — `~/dataagentbench/README.md` §Leaderboard + existing LEADERBOARD.md rows + a sample summary; match the column schema + summary-file convention exactly.
  Schema: `Date | Experiment | Run | Agent | Model | Score | Cost | Duration | Summary`; Score form `N/M (P%)`; summary artifact `# Run Summary` with aggregate + per-dataset table.
- DONE: Author the curated row + supporting summary — aggregate 0.7433 (5-draw mean) with explicit spread note; cost+duration from the run dirs; median draw d0a6f64 as the representative annotated artifact.
  LEADERBOARD.md row added (newest-first); summary `results/dab0022-patents-semistructured-rules__5draw-mean.md` created. Score 204/270 (76%) raw-cell micro-avg + inline "5-draw mean, stratified 0.7433 (spread 0.6675–0.7985)". Cost n/a (flat sub; cost_usd null). Duration ~259m summed from handle sentinels. Median-draw per-dataset table (42/54), annotated that the published score is the 5-draw mean.
- DONE: Resolve runs-visibility + commit locally; do NOT push.
  Hand-authored (not benchctl `p`), so no `_runs/` dependency. Committed `~/dataagentbench` `cbff2b41` (main, ahead of origin 1, NOT pushed). STOPPED at local commit per dispatch.
- DONE: Record the submission in the entity `## Leaderboard submission`.
  Recorded the commit sha, exact row text, artifact path, cost/duration derivation, and the push-pending note.

### Summary

Authored the captain-chosen curated 5-draw-mean leaderboard row in `~/dataagentbench`, matching the existing LEADERBOARD.md schema exactly: row `2026-06-23 | dab0022-patents-semistructured-rules | 5-draw mean | codex spacedock-solver | gpt-5.5 (effort high) | 204/270 (76%) — 5-draw mean, stratified 0.7433 (spread 0.6675–0.7985) | n/a (flat sub) | ~259m (5 draws)` + supporting summary artifact (median draw d0a6f64 as the representative table, annotated that the score is the 5-draw mean so artifact and row stay consistent). Cost is honestly n/a (codex flat subscription, cost_usd null in every summary.json); duration ~259m summed from the 3 run handles. Committed LOCALLY only — `~/dataagentbench` `cbff2b41`, ahead of origin by 1, NOT pushed; stopped per dispatch for captain go-ahead before any push to DataRecce/dataagentbench. CONCLUDE-not-promoted verdict unchanged; @baseline and seed README untouched.

## Stage Report: analyze (formal leaderboard submission package)

- DONE: Study both references in full — answers-JSON ref `data/leaderboard_submissions/claude-opus-4-6_results.json` (270 flat objects {dataset,query,run,answer}; run/query strings) + raw-logs ref `~/spacedock-experiment-opus-4-8-hint/` (per-dataset → run-001..005 → answers.json/claude-output.jsonl/taint.json/taint.md + per-dataset summary.json).
  Schemas confirmed and replicated; draw→run-index mapping fixed (run-001=d0a6f64, 002/003/004=e8ec7dd trials 0/1/2, 005=f74c12b).
- DONE: Deliverable 1 — `dab/leaderboard_submissions/codex-gpt-5.5_results.json`, committed answers recovered per worker session, integrity-gated against reward_per_query.
  267/270 entries (3 omitted = PATENTS run-005 q1/q2/q3, unrecoverable runtime-computed answers — NOT fabricated). Validated: unique (dataset,query,run), no nulls, strings.
- DONE: Deliverable 2 — `dab/leaderboard_submissions/raw_logs/` tree replicating the reference exactly.
  12 datasets × run-001..005 = 60 run dirs (answers.json + codex-output.jsonl + codex-output.fo.jsonl + taint.json + taint.md) + 12 summary.json; 314 files, ~31M. taint clean throughout (matches rk audit). codex transcript naming + null cost/token fields documented in README.md.
- DONE: Commit the new tree (NOT under gitignored runs/), do NOT push; report paths/counts/validation/deviations/commit sha; record in entity.
  Committed in the dab repo (sha in the commit log); NOT pushed anywhere. Recorded in `## Leaderboard submission` → "FORMAL submission package".

### Summary

Assembled the formal DAB leaderboard submission package under the new tracked folder `dab/leaderboard_submissions/`, replicating both DAB reference formats. Deliverable 1 (`codex-gpt-5.5_results.json`) = 267 of 270 `{dataset,query,run,answer}` entries (the 3 missing are PATENTS run-005 q1/q2/q3, genuinely unrecoverable — the draw computed answers in a runtime script that was only read back truncated; omitted not fabricated, flagged in the README + entity with a re-run option for the captain). Deliverable 2 (`raw_logs/`) = the full 12×5 tree (60 run dirs, codex transcript + answers + taint per cell, 12 summary.json), taint clean throughout. Deviations (codex-output.jsonl naming, null cost/token for the flat subscription) documented. A subagent did the 60-cell extraction against an exact recipe I verified; I checked the on-disk result (counts, file sets, the FAILED marker) before committing. Committed in the dab repo, NOT pushed. The earlier hand-authored ~/dataagentbench LEADERBOARD.md row (cbff2b41, local) is left as-is per the dispatch; this formal package is the captain's chosen mechanism.

## Stage Report: analyze (PATENTS draw5 re-run launch — detached)

- DONE: Build a PATENTS-only trials:1 spec with a fresh run dir — fork the cycle-3 frozen spec, PATENTS only, trials:1, DISTINCT experiment …-patents-r5, SAME solver_workflow (IV) + effort high; freeze; `--explain` to confirm PATENTS only / 3 cells / effort high / solver hash b2cae85c / fresh run-dir.
  Built `specs/dab0022-patents-semistructured-rules.patents-r5.{yaml,frozen.yaml}`; `--explain` → `Tasks: 1` (PATENTS), trials 1, effort high, solver hash `b2cae85c…`, fresh run dir `runs/dab0022-patents-semistructured-rules-patents-r5/7e0f83df055ce078`. Recorded the phase-2 reminder to confirm answers.json is full (not truncated).
- DONE: Launch detached via `drivers/rk-run-detached.sh dab0022-patents-r5 …patents-r5.frozen.yaml run`; record handle + pid + ETA; return immediately, do NOT poll.
  Launched: handle `runs/.rk-handles/dab0022-patents-r5-20260623-035538/`, pid 2656592 (alive, `done` absent), started 2026-06-23T03:55:38Z. ETA ~12–20 min. Recorded in `## Leaderboard submission` → "PATENTS draw5 re-run". Did NOT poll/wait — handle returned to the FO.

### Summary

Built and launched the captain-approved PATENTS-only re-run (trials:1, fresh run dir, same cycle-3 README at high) to fill the 3-entry leaderboard gap with byte-exact recoverable answers. Worker pid 2656592 alive; handle returned immediately per the launch-phase contract. Phase 2 (on done): confirm the cell's on-disk answers.json carries the FULL verbatim q1/q2/q3 (the whole point — flag if still truncated), then patch codex-gpt-5.5_results.json run "4" PATENTS (267→270) and replace raw_logs/PATENTS/run-005/ with this fresh cell, with honest README disclosure that draw5-PATENTS is a fresh independent draw. FO owns the wait.

## Stage Report: analyze (PATENTS re-run phase 2 — recover + patch to 270)

- DONE: Audit the fresh cell — `rk audit --policy strict` on `…-patents-r5/7e0f83df055ce078`.
  CLEAN: coverage_missing 0, tainted 0, clean. Scored q1✅ q2✅ q3❌.
- DONE: RECOVERY CHECK (decisive) — determine whether the FULL verbatim q1/q2/q3 are recoverable.
  RECOVERABLE: a worker `function_call_output` echoed the complete answers object verbatim (q1 430 / q2 1393 / q3 255 chars; lengths matched the worker's self-report → byte-exact, not truncated). The harness still does NOT persist answers.json out of the container; this draw succeeded because it printed the full object before writing (the original f74c12b draw printed only lengths).
- DONE: Patch to 270 — update results JSON run "4" PATENTS; replace raw_logs/PATENTS/run-005/; re-validate; update README; commit.
  `codex-gpt-5.5_results.json` → 270 entries (validated: unique, no nulls, strings). `raw_logs/PATENTS/run-005/` = fresh answers.json + worker/FO transcripts + clean taint (FAILED marker dropped). summary.json unchanged (score was always known, 2/3). README note 4 rewritten as fresh-independent-draw disclosure. Committed.

### Summary

PATCHED to 270/270. The fresh PATENTS re-run (audit-clean) echoed the full verbatim q1/q2/q3 (byte-exact, lengths matched its self-report), so the gap is closed without fabrication. Patched `codex-gpt-5.5_results.json` (267→270, re-validated) and replaced `raw_logs/PATENTS/run-005/` with the fresh cell (FAILED marker gone); the README discloses run-005-PATENTS is a fresh independent draw (same score q1✅q2✅q3❌, so summary.json/aggregate unchanged). Root cause of the original gap: the harness does not persist per-cell answers.json out of the container, so recovery depends on whether a draw echoes the full object in its transcript — a known fragility, not luck-per-se, worth a harness fix if byte-exact recovery is needed routinely. The dab-repo package is now a complete 270/270 submission, committed, NOT pushed.
