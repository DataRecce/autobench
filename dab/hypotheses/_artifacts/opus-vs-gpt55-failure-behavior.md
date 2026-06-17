---
title: How Opus-4.8 and gpt-5.5 fail differently (and identically) on DAB — a raw-transcript behavioral study
date: 2026-06-17
scope: behavioral comparison of the two models WHEN THEY ANSWER WRONG, from raw agent transcripts
method: 6 parallel analysts, one per query, each diffing the Opus run-003 wrong-transcript against the gpt-5.5
  xhigh (dab0007) and high (codex-dab-baseline) wrong-transcripts on the SAME query
queries: PATENTS-q1, PANCANCER_ATLAS-q1, GITHUB_REPOS-q1 (both models always wrong);
  agnews-q4, stockmarket-q4, crmarenapro-q2 (flip-targets — gpt-5.5 PASSED at high, FAILED at xhigh)
sources:
  opus: ~/dataagentbench/_runs/spacedock-opus-4-8-xhigh-hint/run-003/datasets/<DS>/attempts/attempt-001/ (claude-output.jsonl, answers.json, validation.json)
  gpt55_xhigh: dab/runs/dab0007-gpt55-baseline-xhigh/9b0a658e2274cb22/<DS>-q<n>__*/ (codex rollout jsonl + verifier)
  gpt55_high: dab/runs/codex-dab-baseline/186cd2bbb7a5d0d0/<DS>-q<n>__*/
related: opus-vs-gpt5.5-failure-modes.md (the earlier WIN-side study); dab0007 ## Behavioral analysis
---

# How the two models fail on DAB — behavioral study from raw logs

## Executive summary

Reading the raw transcripts of both models on six failed queries, the failures fall into **two
regimes**, and which regime you are in depends entirely on whether the query is *genuinely hard*
or *contested* (ambiguous / environment-frictioned):

1. **On genuinely-hard queries (PATENTS-q1, PANCANCER-q1, GITHUB-q1), the two models fail
   IDENTICALLY** — frequently committing the *byte-identical wrong answer* via the *same*
   misinterpretation, each ratified by a *correlated* self-check. There is essentially no
   behavioral contrast: both grind to a confident, self-certified wrong answer. Extra xhigh
   reasoning changes nothing.

2. **On contested queries (agnews-q4, stockmarket-q4, crmarenapro-q2), the two models fail in
   OPPOSITE ways**: **Opus over-explores and over-commits** (reaches all the data, then confidently
   picks the wrong branch — sometimes with the correct answer literally on screen); **gpt-5.5 at
   xhigh under-explores and abstains** (`"UNABLE TO DETERMINE"`) — usually on an *avoidable*
   blocker it could have worked around.

The single most actionable finding: **for the contested queries, more reasoning effort made
gpt-5.5 worse.** Every one of agnews-q4 / stockmarket-q4 / crmarenapro-q2 was a PASS at `high`
and a FAIL at `xhigh`, and the transcripts show *why* — see §3.

## 1. The universal failure mechanism: self-anchored false-green (both models)

This is the dominant mechanism and it is **model-independent**. On every shared-fail query, each
model built an "independent verification" step that **re-implemented the same interpretation it was
trying to check**, got agreement, and declared PASSED on a wrong answer. Neither model ever ran a
*magnitude-plausibility* check against the answer it produced.

- **GITHUB-q1**: gold = 0.3333 (1/3). Opus committed 0.1125 (18/160), gpt-5.5 0.138 (21/152) — both
  treated the question as "fraction of README *content rows*" over a denominator of 100–160, never
  asking whether ~0.11 was plausibly the intended ~1/3. Opus even ran a dedicated `verify` stage
  that *re-derived and ratified* its own wrong number.
- **PANCANCER-q1**: gold groups by the `icd_o_3_histology` **code** (5 strata); all three runs
  (Opus, gpt@high, gpt@xhigh) grouped by the free-text `histological_type` **name** (3 strata).
  Both models *saw* the code column and ignored it; gpt-5.5's one matching value (2.7136) proves the
  arithmetic was right — only the grouping dimension was wrong. Each "verified" the wrong dimension.
- **PATENTS-q1**: both models produced the **same 89-code answer** via the same EMA-series
  construction (no zero-filled annual series); each ran a second EMA re-implementation that matched
  (same reading → correlated) and self-certified PASSED.

Take-away: the verification both models perform is *correlated with the error*, so it cannot catch
it. This is the same oracle-blind wall documented for ade-bench (`[[verification-without-oracle-real-world]]`):
only a check built on an *independent* derivation (or an external magnitude anchor) breaks it.

## 2. The two models' opposite signatures on contested queries

| | **Opus-4.8** | **gpt-5.5 (xhigh)** |
|---|---|---|
| Data access under friction | reaches every source (incl. the gold evidence) | gives up after one naming-convention miss |
| When unsure | **commits a value** (never abstains) | **abstains** — `"UNABLE TO DETERMINE"` |
| Characteristic error | single-hypothesis lock-in / over-commit | premature abstention on an avoidable blocker |
| Example | crmarenapro-q2: found *a* bundle violation, stopped, never checked the cost axis the gold rewards | crmarenapro-q2: never read `db_config.yaml`, never tried the Postgres host the schema named → abstained |

- **Opus over-commits.** On stockmarket-q4 it printed the correct margin-ranking *and the wrong
  count-ranking side by side*, then wrote "[margin] is documented here but **not** adopted," and
  committed the wrong one. On crmarenapro-q2 it locked onto the first plausible violation it found
  and never tested the cost axis. On agnews-q4 it noted "margin is thin … within classifier noise"
  and committed its classifier's wrong leader anyway.
- **gpt-5.5-xhigh abstains — avoidably.** On agnews-q4 the Mongo dump folder was absent as files;
  xhigh concluded the source was unavailable and wrote `UNABLE TO DETERMINE` — but never instantiated
  a `MongoClient` against the live service the config declared (which the `high` run *did*). On
  crmarenapro-q2 it searched only for file-DBs and `connections.yaml`, never opened the alternate
  `db_config.yaml`, and abstained — though the schema doc plainly named a Postgres store.

## 3. The crux: more reasoning effort made gpt-5.5 WORSE on the contested queries

All three flip-targets were **PASS at `high`, FAIL at `xhigh`**. The transcripts show two distinct
mechanisms by which extra deliberation backfired:

- **Over-rationalizing the literal reading (stockmarket-q4).** `high` treated the *tie* produced by
  the count-metric as evidence that count was the wrong reading, and chose margin (→ gold). `xhigh`
  demoted margin to a mere tiebreaker and committed to count — *talking itself into Opus's exact
  misinterpretation*. More reasoning manufactured a more elaborate defense of the wrong branch.
- **Over-caution about the environment (agnews-q4, crmarenapro-q2).** `high` improvised data access
  (fell back to the live Mongo service / read the alternate `db_config.yaml`). `xhigh` treated a
  file-glob miss as proof of absence and abstained. More deliberation made it *more literal and
  conservative* about source availability, so it quit where `high` had improvised.

In both mechanisms, the extra xhigh budget was spent building a more careful case for *not* doing
the pragmatic thing that won at `high`.

## 4. Implications for the loop (our solver is gpt-5.5)

The behavioral split says exactly where the README levers should push gpt-5.5 — toward Opus's
strengths (persistence, always-commit) without importing Opus's weakness (over-commit to a wrong
branch):

1. **Anti-abstention + environment persistence (highest yield).** "Never answer
   `UNABLE TO DETERMINE`. If a data source appears missing, exhaust every connection path named in
   `db_description` / `db_config.yaml` / the live service hosts before concluding absence; then
   commit a best-effort computed value." Targets the avoidable abstentions: **agnews-q4,
   crmarenapro-q2, crmarenapro-q8** (and PANCANCER-q3, googlelocal-q3/q4 from dab0007). This is
   literally the behavior gpt-5.5 *already shows at `high`* — the lever is to make it reliable at xhigh.
2. **Tie/degenerate-result as a disambiguation signal (interpretation discipline).** "If one reading
   of an ambiguous ranking/grouping produces a tie or a degenerate result and another is clean,
   prefer the clean reading." This is exactly what won stockmarket-q4 at `high`. Pushes against the
   xhigh over-rationalization.
3. **Independent verification + magnitude check (the hard, universal one).** "Re-derive the answer
   via a *different* method/interpretation, and sanity-check its magnitude against an a-priori
   expectation." This is the only thing that breaks the §1 self-anchored false-green — but it is the
   oracle-blind wall, and ade-bench's program showed it is the hardest to land. Lower confidence.

Caveat: single-trial per cell. The §2/§3 abstention and interpretation behaviors are **robust** (the
model literally wrote the abstention string / the interpretation rationale — not noise). The §1
convergent-wrong-answer findings are byte-identical across independent runs, so also robust. The
weakest claim is any specific lever's *flip rate* — that needs a smoke run judged by committed
artifact, per the workflow.
