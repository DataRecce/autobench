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

## Run result

## Behavioral analysis

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
