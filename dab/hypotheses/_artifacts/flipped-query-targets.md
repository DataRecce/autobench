---
title: Flipped-query targets for the DAB autoresearch loop
date: 2026-06-15
source_run_group: ~/dataagentbench/_runs/spacedock-opus-4-8-xhigh-hint/run-003..run-007
adapted_from: ~/dataagentbench/docs/research/_artifacts/fable5-target-selection-from-spacedock-opus-4-8.md
baseline: "@baseline = converted Opus-4.8 incumbent (= run-003 specifically), stratified 0.6536"
variant_solver: codex/gpt-5.5 (forks the solver-workflow README)
metric: stratified pass@1, 12-dataset DAB average (per-query weight = 100 / (12 * n_queries_in_dataset))
related:
  - dataset-gap-ranking.md
  - baseline.yaml
  - ../../docs/specs/2026-06-15-dab-autoresearch-design.md (§7 confound, §8 smoke select-then-exclude)
raw_logs: ~/dataagentbench/_runs (this run group) ; ~/CAIS-paper-experiments (prior experiments)
---

# Flipped-query targets for the DAB autoresearch loop

## Strategy (how this differs from the Fable-5 source doc)

The source artifact (`fable5-target-selection-*.md`) chased the **0/5 fair-miss** queries —
high stratified weight, but unsolved in every Opus run and therefore high-risk. This document
takes the **opposite** selection for the DAB autoresearch loop, per the captain's directive:

- **Target the *flipped* queries** — ones Opus-4.8 xhigh passed in **some but not all** of its 5
  runs (pass rate strictly between 0/5 and 5/5). A flip proves the task is *solvable* (no
  answerability wall) and that the correct approach exists; the loop's job is to make it
  *reliable*.
- **Don't touch the 5/5 saturated queries** — no headroom to overcome.
- **Don't touch the 0/5 never-resolved queries** — *unless a prior experiment proves they are
  solvable.* Opus-4.8 0/5 alone is not a wall verdict. The cross-experiment scan of
  `~/CAIS-paper-experiments` (see "Cross-experiment rescue" below) rescues three of the source
  doc's former high-priority picks — `GITHUB q4`, `googlelocal q2`, `crmarenapro q8` were resolved
  by codex-5.5 and/or other configs — and confirms only `PANCANCER q1` as a true wall (0/58).

## The bankability filter (loop-specific)

The loop's `@baseline` is a **single run** — the converted Opus incumbent, which is
`run-003` of the 5. `rk runs diff` banks a query only as a **FAIL→PASS vs run-003**. So a flipped
query is only *bankable* if **run-003 itself failed it**. Flipped queries that run-003 happened to
*pass* are not bankable (no FAIL→PASS to show) and are instead at **regression risk** — they make
excellent smoke **canaries**.

Two filters → two buckets:

| Filter | Meaning | Use |
|---|---|---|
| flipped (1/5–4/5) **AND** run-003 = FAIL | solvable, has headroom, bankable vs `@baseline` | **PRIMARY TARGETS** |
| flipped (1/5–4/5) **AND** run-003 = PASS | solvable but already-passing in `@baseline`, unstable | **CANARIES** (regression tripwires) |

(run-003 per-query rewards verified from `dab/runs/opus-4-8-baseline/e14e49869e6412de/per_trial_outcomes.json`.)

## Primary targets — overcome these

Every target **fails in run-003 (`@baseline`)**, so each is a clean bankable FAIL→PASS. They come
from two sources: **rescued** (codex-5.5 proven to solve it elsewhere — see "Cross-experiment
rescue"; log-audited legitimate, no cheating) and **flipped** (Opus passed it 1/5–4/5 in the run
group → solvable, has headroom):

| Priority | Query | Source | run-003 | Weight (pts) | Bankable lift | Nature / lever |
|---|---|---|---:|---:|---:|---|
| 1 | `GITHUB_REPOS-q4` | rescued (codex 5/5) | FAIL | 2.08 | +2.08 | Top-5 non-Python repos by commits. **codex-5.5 nails it 5/5 on our exact spacedock surface** (log-verified genuine SQL, excluded NULL-language `torvalds/linux`). Likely flips via the anchor with **no lever** (model-capability). |
| 2 | `googlelocal-q2` | rescued (codex-capable) | FAIL | 2.08 | +2.08 | Massage businesses avg-rating ≥4.0. **codex computes the correct businesses every run**; 4/5 fail only on output shape (JSON-dicts vs `name - rating` string) → **output-contract lever**. |
| 3 | `stockmarket-q4` | flipped 3/5 | FAIL | 1.67 | +1.67 | Top-5 NYSE non-ETF "up>down days 2017" — ordering/tie/filter variance. Opus gets it >half the time. |
| 4 | `yelp-q6` | flipped 1/5 | FAIL | 1.19 | +1.19 | Highest-avg-rating business + category, ≥5 reviews, H1-2016 window — flaky category/rating join; latest Opus run passed (trending up). |
| 5 | `agnews-q4` | flipped 1/5 | FAIL | 2.08 | +2.08 | "2015 region with most World-category articles" — argmax behind noisy category inference. High weight but **integrity-sensitive** (AG-News labels stripped); treat as a stretch. |
| 6 | `crmarenapro-q3` | flipped 3/5 | FAIL | 0.64 | +0.64 | 5-way stage-label correctness classification for one opportunity — flaky label choice; small weight. |

**Max bankable lift if all six flip vs `@baseline`: +9.74 stratified points** (0.6536 → ~0.751).
`GITHUB_REPOS-q4` and `googlelocal-q2` lead: highest weight (2.08) **and** the strongest evidence
codex can do them (5/5 / correct-but-misformatted on our surface). `crmarenapro-q8` (+0.64,
README-suppressed, see rescue section) is a secondary target → ~+10.4 pts if included.

## Cross-experiment rescue — queries Opus-4.8 never solved but others did

Opus-4.8 xhigh went 0/5 on `PANCANCER q1`, `googlelocal q2`, `GITHUB q4`, `crmarenapro q8`, so
the flip/fail analysis above (which only sees the Opus-4.8 run group) parked them as "never
resolved." Scanning `~/CAIS-paper-experiments` (passes/runs across all prior models + workspace
variants) **overturns that for three of the four** — they are *not* walls, and two are solvable by
codex-5.5 itself, making them strong bankable targets vs the Opus `@baseline`:

| Query | wt | `@baseline` (opus-4-8 run-003) | **codex-5.5 spacedock** (closest to our loop) | codex-5.5 minimal | best Opus prior | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `GITHUB_REPOS-q4` | 2.08 | FAIL | **5/5** | 5/5 | 5/5 (4-6/4-7, structured) | **Top target — model-capability flip.** Codex nails it on our exact surface; the anchor likely banks +2.08 with no lever. |
| `googlelocal-q2` | 2.08 | FAIL | 1/5 | **5/5** | 0/5 (no Opus ever) | **Output-format lever target.** Log-verified: codex computes the *correct* businesses in all 5 spacedock runs; 4/5 fail only on output shape (JSON-dicts vs the expected `name - rating` string). Lever = answer/output contract. +2.08. |
| `crmarenapro-q8` | 0.64 | FAIL | 0/5 | 3/5 | 5/5 (spacedock-opus-4-6) | **README-lever target.** Solvable in spacedock (opus-4-6 5/5) but codex-5.5 + opus-4-8 regressed → recoverable; low weight. +0.64. |
| `PANCANCER_ATLAS-q1` | 2.78 | FAIL | 0/5 | 0/5 | **0/58 everywhere** | **Confirmed wall.** No model/config ever passed it — stays excluded. |

Two flip mechanisms to exploit:
- **Model-capability flips** — codex-5.5 already passes on the spacedock surface (`GITHUB_REPOS-q4`
  5/5) where opus-4-8 fails. The codex anchor banks these vs the Opus `@baseline` *without a lever*
  (the design §7 model-swap confound here is the *point*, not a nuisance). Verify on the anchor run.
- **README-suppressed flips** — the task is provably solvable (codex-minimal or spacedock-opus-4-6
  passes) but our spacedock baseline README suppresses it for codex (`googlelocal-q2` 1/5,
  `crmarenapro-q8` 0/5). These are the best *lever* hypotheses: there is direct evidence a README
  change can recover a lost capability. Diff the minimal vs spacedock workspace prose for the lever
  direction.

Combined max bankable lift from this rescue set (excluding the PANCANCER wall): **+4.80 pts**
(`GITHUB q4` 2.08 + `googlelocal q2` 2.08 + `crmarenapro q8` 0.64), on top of the +5.58 from the
flipped set → the loop's bankable target pool is now ~**+10.4 stratified points**. Prioritize
`GITHUB_REPOS-q4` and `googlelocal-q2` (2.08 each, strong codex evidence).

(Source: `~/CAIS-paper-experiments/{spacedock,minimal,structured,direct-*}-{opus-4-6,opus-4-7,codex-5.5}-*`,
legacy `run-*/datasets/<ds>/attempts/attempt-*/validation.json`. The `spacedock-codex-5.5-xhigh-hint`
column is the closest analog to our loop's codex/gpt-5.5 + spacedock + hints surface.)

**Cheating check (codex-5.5 spacedock).** Because the codex-5.5 spacedock run group is known to
contain some cheating elsewhere, the `GITHUB_REPOS-q4` and `googlelocal-q2` passes were log-audited
(`codex-output.jsonl` + workspace `_artifacts/reasoning.md`): both are **legitimate** — genuine,
edge-case-aware DuckDB SQL; no `ground_truth`/`solution` file is present in the agent workspace
(harbor keeps it verifier-side), no command read one, and the agent's `rg` searches explicitly
`-g '!ground_truth.csv' -g '!validate.py'`. Caveat: worker sub-thread keystrokes aren't in the
orchestrator transcript, but with no answer file in-workspace there is nothing to leak. The
"cheating behavior" in this run group is in *other* queries, not these two.

## Canaries — keep these passing (do NOT target)

Flipped but **passing in run-003**, so they are the queries most likely to silently regress when a
codex variant changes the solver README. Use them as smoke canaries (must-stay-PASS):

| Query | 5-run rate | run-003 | Weight (pts) | Why a good canary |
|---|---:|---:|---:|---|
| `bookreview-q1` | 4/5 | PASS | 2.78 | Decade-with-highest-avg-rating (≥10 distinct rated books) — highest weight; one Opus run already missed it, so genuinely fragile. |
| `stockmarket-q3` | 4/5 | PASS | 1.67 | NASDAQ financially-troubled companies' 2008 avg volume — multi-condition filter, one miss. |
| `crmarenapro-q12` | 4/5 | PASS | 0.64 | Quickest avg open→close turnaround, Apr-2023, sales-cycle policy — one miss. |

For a stable (non-fragile) canary, also draw from the 5/5 datasets `music_brainz_20k` and
`stockindex` — see `dataset-gap-ranking.md`.

## Excluded — won't touch (per directive)

**5/5 saturated — no headroom:** `music_brainz_20k` q1–q3, `stockindex` q1–q3, and every query not
listed in the flip/fail tables (those passed 5/5 in the run group).

**0/5 in Opus-4.8 — but split by the cross-experiment scan (above):**
- **Rescued → now targets** (resolved elsewhere; see "Cross-experiment rescue"): `GITHUB_REPOS-q4`,
  `googlelocal-q2`, `crmarenapro-q8`.
- **Confirmed walls / still excluded** (0/58 everywhere, or known GT/answerability defects per the
  source doc): `PANCANCER_ATLAS-q1` (0/58), `DEPS_DEV_V1-q1` (95-way tie), `GITHUB_REPOS-q1/q2`
  (GT defects), `PATENTS-q1/q2/q3` (missing rows / hidden EMA convention), `agnews-q2/q3` (stripped
  labels), `crmarenapro-q2` (contested GT). These stay parked until an answerability artifact
  overturns them.

## Target prompts (primary)

`GITHUB_REPOS-q4`:
> List the repository names for the top five GitHub repositories whose main language is not
> Python, ordered by the highest number of commits.

`googlelocal-q2`:
> Which massage therapy businesses have an average rating of at least 4.0, and what are their
> respective average ratings?

`stockmarket-q4`:
> What are the names (not symbol) of the top 5 non-ETF stocks listed on the New York Stock
> Exchange (NYSE) that had more up days than down days in 2017? (Up days: closing price > opening
> price; Down days: closing price < opening price)

`yelp-q6`:
> Which business received the highest average rating between January 1, 2016 and June 30, 2016,
> and what category does it belong to? Consider only businesses with at least 5 reviews.

`agnews-q4`:
> In 2015, which region published the largest number of articles in the World category?

`crmarenapro-q3`:
> Is the stage name accurately representing the tasks for this opportunity? If it is not, what
> should the appropriate stage name be? Return only the correct stage label among
> ('Qualification', 'Discovery', 'Quote', 'Negotiation', 'Closed'). Opportunity Id: 006Wt000007BGGjIAO

## Concept ideation order (where to start)

The six concept entities (`dab0001`–`dab0006`) should be ideated **one at a time** in this order.
Lead with the concept whose lever is highest-confidence and cleanly attributable, then widen.

| Order | Concept | Rationale |
|---|---|---|
| 1 | `dab0001` answer-output-contract | **Start here.** Log-verified: codex computes `googlelocal-q2` correctly every run, fails 4/5 *only* on output format — so a README format rule is the entire mechanism. Cleanest attributable flip (no model-swap confound, §7), 2.08 pts, and the safest first trip through propose→smoke→full→analyze→conclude. |
| 2 | `dab0003` aggregation-filter-precision | Concrete per-query semantic rules (counts / thresholds / date windows / NULLs); testable and attributable. |
| 3 | `dab0002` deterministic-ordering-tiebreak | Broad (3 flipped targets) but variance-based — a 1/5–3/5 flip is harder to prove in a single run; do it once the pipeline is trusted. |
| 4 | `dab0005` methodology-overhead-recovery | **Structural** (changes stage flow): wide blast radius, must log to `WORKFLOW-REFINE.md` and carry strong cross-family canaries. Defer until the loop is proven. |
| 5 | `dab0006` integrity-safe-stripped-label-inference | Hardest: `agnews-q4` at 1/5, integrity-sensitive, smoke must artifact-verify the answer was inferred not leaked. |
| — | `dab0004` multisource-join-grain | **Hold — harvest, don't ideate.** Its headline target `GITHUB-q4` flips via the *anchor* (codex already 5/5), so a README lever here risks being **inert**. Bank GITHUB-q4 from the anchor run; only ideate this concept if the anchor shows a join-grain query that still fails. |

**Run the codex anchor (`dab-anchor-codex`) before committing smoke/full budget to the
variance concepts (`dab0002`/`dab0003`).** The anchor establishes codex's per-query baseline —
which targets it already passes (no lever needed) vs still fails (lever needed) — and banks the
free model-capability flips (`GITHUB-q4`). Ideation itself is cheap (no run cost), so `dab0001`
can be ideated now in parallel; the anchor only gates the *expensive* runs.

## How to target one in the loop

Each primary target becomes one `dab00NN-<slug>` hypothesis whose single lever is a README edit
(design §5). Smoke targets the one query plus canaries via dataset-select + per-query exclude
(design §8). Example for `stockmarket-q4` (keep q4 + a fragile canary + a stable canary):

```yaml
benchmark:
  kind: harbor
  dataset: dab@1.0
  plugin: dab
  plugin_args: { hints: true, data_root: /home/kent/dataagentbench/data }
  tasks: [stockmarket, music_brainz_20k]            # whole datasets materialize
  exclude_tasks:                                    # drop everything except q4 + one stable canary
    - stockmarket-q1
    - stockmarket-q2
    - stockmarket-q3        # NOTE: this is a canary too — keep it instead if testing for regressions
    - stockmarket-q5
    - music_brainz_20k-q2
    - music_brainz_20k-q3   # keep music_brainz_20k-q1 as a stable must-stay-PASS canary
```

Smoke-set table (propose gate): `stockmarket-q4` 🎯 want-flip (run-003 FAIL) · `stockmarket-q3`
✅ must-stay-PASS (fragile canary) · `music_brainz_20k-q1` ✅ must-stay-PASS (stable canary).

## Confound caveat (design §7)

`@baseline` is Opus; variants are codex/gpt-5.5. A bankable FAIL→PASS therefore mixes the
**model swap** with the **README lever**. The codex anchor run (spec `dab-anchor-codex`, not yet
executed) establishes codex's own per-query baseline; until then, attribute any flip with the
committed-artifact read (did the README change move the answer, or did codex already solve it?),
not the headline delta alone.

## Source / raw logs

- Run group + per-query truth: `~/dataagentbench/_runs/spacedock-opus-4-8-xhigh-hint/run-003..007`.
- Prior experiments: `~/CAIS-paper-experiments`.
- Per-query weights: `100 / (12 * n_queries)` → agnews 2.08, bookreview 2.78, crmarenapro 0.64,
  stockmarket 1.67, yelp 1.19.
