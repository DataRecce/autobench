---
title: Why Opus-4.8 fails where gpt-5.5 passes — last-mile failure modes on DAB
date: 2026-06-16
scope: the 6 queries that are FAIL in the Opus-4.8 @baseline (run-003) but PASS in the gpt-5.5 codex-dab-baseline
sources:
  opus_fail: ~/dataagentbench/_runs/spacedock-opus-4-8-xhigh-hint/run-003/datasets/<ds>/attempts/attempt-001/ (validation.json + workspace/_artifacts/reasoning.md)
  gpt55_pass: dab/runs/codex-dab-baseline/186cd2bbb7a5d0d0/<ds>-q<n>__*/ (verifier/test-stdout.txt + agent/sessions/*.jsonl)
method: paired transcript diff (failing Opus approach vs passing gpt-5.5 approach), per query
related: flipped-query-targets.md
---

# Why Opus-4.8 fails where gpt-5.5 passes

## Executive summary

We compared the *failing* Opus-4.8 transcript against the *passing* gpt-5.5 transcript for all six
queries that flip FAIL→PASS between the two baselines (`GITHUB_REPOS-q4`, `googlelocal-q2`,
`stockmarket-q4`, `yelp-q6`, `agnews-q4`, `crmarenapro-q3`).

**The headline: none of the six is a capability or data-access failure.** In every case Opus
reached the data and usually computed the *same* intermediate facts as gpt-5.5 — the same winner,
the same per-row numbers, even the same gold string verbatim. Opus lost in the **last mile**:
output shaping, ambiguity/tie resolution, and inference-method choice. And in several cases Opus's
*more elaborate* reasoning actively hurt it — it explicitly considered the correct branch and
talked itself out of it.

gpt-5.5's edge here is **not** "writes better SQL." It is: (1) emitting the literal, complete,
verifier-shaped answer; (2) resolving ambiguity toward the benchmark's intended reading; and
(3) using instance-direct, robustness-checked inference instead of a single population/lexicon
model.

## Per-query ledger

| Query | Opus answer (wrong) | gpt-5.5 answer (right=gold) | Root cause | Theme |
|---|---|---|---|---|
| `GITHUB_REPOS-q4` | kept `torvalds/linux` (no language row) at #1 → dropped `tensorflow` | INNER-JOIN on languages → `torvalds/linux` excluded → `tensorflow` enters top-5 | NULL/edge-case resolution (keep vs drop unclassifiable row) | Interpretation |
| `stockmarket-q4` | ranked by raw up-day **count** | ranked by **margin** (up−down) — matches gold | wrong ORDER-BY for "top 5" | Interpretation |
| `googlelocal-q2` | `Elite Massage (average rating 5.0)` + dropped `J B Oriental Inc` | `Elite Massage: 5.0; … J B Oriental Inc: 4.166…` | score pushed outside verifier's 10-char window; name-only candidate match | Output format |
| `yelp-q6` | `…, Restaurants` (singular category) | `…, Restaurants, Breakfast & Brunch, American (New), Cafes` (all 4) | truncated a multi-value answer on a singular reading | Output format |
| `agnews-q4` | `South America` (single-pass keyword argmax) | `Africa` (Naive-Bayes + consensus, threshold-stable) | noisy classifier resolved a near-tie wrong | Inference method |
| `crmarenapro-q3` | `Quote` (population modal-frequency vote over a truncated task set) | `Negotiation` (read the furthest-stage task as evidence) | correlational model washed out the decisive task | Inference method |

## Three cross-cutting themes

### Theme 1 — Output-contract literalism (`googlelocal-q2`, `yelp-q6`)
Opus computed the correct answer, then **mis-shaped it for the verifier**:
- `yelp-q6`: it read "what category" as singular and reported only `Restaurants`, *discarding* the
  full list `Restaurants, Breakfast & Brunch, American (New), Cafes` it had already extracted
  verbatim. The validator requires all four substrings → fail on the first missing one. gpt-5.5
  emitted the whole list.
- `googlelocal-q2`: Opus wrote `Elite Massage (average rating 5.0)`; the verifier only scans the
  10 characters after each name for a number, and `" (average "` has no digit → "No score found
  after name: Elite Massage." gpt-5.5 wrote `Name: score`, with the digit inside the window.

These are correct-substance, wrong-form losses. **Caveat:** they are partly *verifier brittleness*
(a 10-char window; substring-of-all-categories) — Opus's answers were arguably right to a human.
gpt-5.5 wins by being more verifier-literal, not more correct.

### Theme 2 — Ambiguity & tie resolution (`stockmarket-q4`, `GITHUB_REPOS-q4`)
When the query underdetermined the answer, Opus reasoned carefully, **explicitly named the correct
branch, and chose against it**:
- `stockmarket-q4`: Opus's own `reasoning.md` documents the margin interpretation — "rank directly
  by margin (up-dn) desc would give … MFA Financial, Argo Group, HDFC Bank, Albany International,
  DTE Energy" (exactly the gold) — then writes "**not** adopted," ranking by raw up-day count
  instead. gpt-5.5 reasoned that "more up days than down days" makes the *excess* the ranking
  quantity, and matched gold.
- `GITHUB_REPOS-q4`: Opus saw `torvalds/linux` has no language row, reasoned "no row ⇒ certainly
  not Python ⇒ keep," and called exclusion "unreasonable … a metadata-absence technicality." gpt-5.5
  inner-joined on the language table, structurally dropping the unclassifiable repo — which is how
  the gold was built.

Pattern: Opus's elaboration surfaces the right answer *and a defensible wrong one*, and it commits
to the wrong one. gpt-5.5 lands on the benchmark's intended reading with less deliberation.

### Theme 3 — Inference-method robustness (`agnews-q4`, `crmarenapro-q3`)
On tasks needing inference (classify stripped-label text; judge a CRM stage), Opus used a single
**population/lexicon statistical model** that drowned the decisive signal; gpt-5.5 used
**instance-direct, cross-checked** methods:
- `agnews-q4`: Opus ran a fixed keyword lexicon with *World as the residual default* (every
  zero-signal article → World), one-shot argmax → `South America` by a noise-floor margin (it even
  noted Africa tied for #1 in a stricter variant, then committed to the single pass). gpt-5.5 built
  a Naive-Bayes + seeded hybrid, ran several classifiers, and picked the **threshold-stable**
  region → `Africa` (gold). Both were verified leak-free.
- `crmarenapro-q3`: both read the *same 6 tasks*. Opus built a board-wide modal-frequency profile
  and **dropped the two decisive tasks** ("Hold negotiation meeting", "Prepare contract for
  approval") from its scoring set → modal vote said `Quote`. gpt-5.5 read the furthest-stage task
  as the evidence and eliminated by record presence (no signed contract ⇒ not Closed; negotiation
  tasks present ⇒ `Negotiation`).

Pattern: Opus generalizes to a population/lexicon model; gpt-5.5 reasons from the specific
instance's evidence and stress-tests the close call.

## The unifying insight

Across all six, Opus had the data and the right intermediate results — it lost on **judgment at the
final step**, and its extra reasoning was as often a liability as an asset (it argued itself into
the defensible-but-wrong branch in 4 of 6). gpt-5.5's wins are concentrated in:
1. **answer-contract literalism** (emit the complete, verifier-shaped string),
2. **intended-reading ambiguity resolution** (margin not count; drop the unclassifiable row), and
3. **instance-direct, robustness-checked inference** (consensus classifier; furthest-stage evidence).

This is a "last-mile alignment" advantage, not a raw analytical one.

## Caveats

- **Single-run comparison.** This is Opus run-003 vs one gpt-5.5 run. Opus is *flaky* on several of
  these (1/5–4/5 across its 5 runs) — so this is "how Opus fails *when* it fails," not "Opus always
  fails." The failure *modes*, not the pass rate, are the finding.
- **Two of six are verifier brittleness** (`googlelocal-q2`, `yelp-q6`): Opus's substance was
  defensible; the loss is form. Read those as "gpt-5.5 is more verifier-literal," and weigh whether
  the benchmark's verifier is over-strict.
- **Model-environment confound elsewhere** does not apply here — these six are genuine model
  differences (same workspace surface; no infra failure in any of the six, unlike PANCANCER).

## Implications for the loop

The loop's solver *is* gpt-5.5, so this primarily explains *why* the 8 model-swap gains happened —
and, by symmetry, predicts where gpt-5.5's own **regressions** come from. The same three themes
almost certainly drive gpt-5.5's 7 regressions (e.g. `googlelocal-q4`/output-format,
`stockmarket-q3`/aggregation-interpretation, `DEPS_DEV_V1-q2`/parse-coverage). The actionable
transfer: the README levers should **lock in** the three behaviors gpt-5.5 already does well here
(literal answer contract, intended-reading resolution, robustness-checked inference) so it stops
losing them on the regression queries — see `flipped-query-targets.md` (regression-recovery pivot).
