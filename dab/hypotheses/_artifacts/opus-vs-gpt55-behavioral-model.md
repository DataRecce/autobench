---
title: Two minds, opposite biases — a behavioral model of Opus-4.8 vs gpt-5.5 on DataAgentBench
date: 2026-06-17
status: synthesis — observational studies + one controlled intervention (dab0009)
draws_on:
  - opus-vs-gpt5.5-failure-modes.md         # win-side study (Opus FAIL → gpt-5.5 PASS, 6 queries)
  - opus-vs-gpt55-failure-behavior.md        # failure-side study (6 queries, raw transcripts)
  - dab0007 (gpt-5.5 @xhigh full run, 0.6002) · dab0008 (gpt-5.5 @high, deferred) · codex-dab-baseline (gpt-5.5 @high, 0.5836) · opus-4-8-baseline (@baseline, 0.6536)
  - dab0009 anti-abstention lever — the controlled intervention that validates the central thesis
runs:
  opus_xhigh:  runs/opus-4-8-baseline/e14e49869e6412de            # stratified 0.6536
  gpt55_high:  runs/codex-dab-baseline/186cd2bbb7a5d0d0           # stratified 0.5836
  gpt55_xhigh: runs/dab0007-gpt55-baseline-xhigh/9b0a658e2274cb22 # stratified 0.6002
---

# Two minds, opposite biases

## Central thesis

On DataAgentBench, **Opus-4.8 and gpt-5.5 have opposite, almost symmetric failure biases**, and most
of the per-query difference between them is explained by that one axis:

> **Opus over-commits — it grinds to a computed answer and never abstains, sometimes talking itself
> into a defensible-but-wrong branch. gpt-5.5 (especially at high reasoning effort) under-explores —
> it abstains (`"UNABLE TO DETERMINE"`) after one obstacle, even when the data is reachable.**

This is not a capability gap. In nearly every divergent query both models reach the data and compute
the same intermediate facts; they part ways at the **last decision** — *commit vs. quit*. The bias is
a property of model temperament, not of analytical horsepower, and it is **causally demonstrable**:
forbidding gpt-5.5 from abstaining (dab0009) flipped exactly the queries it had been losing by
abstention, and made it behave the way Opus already does by default.

## 1. The aggregate picture

| run | tier | stratified Pass@1 |
|---|---|---|
| opus-4-8-baseline (`@baseline`) | xhigh | **0.6536** |
| gpt-5.5 (codex-dab-baseline) | high | 0.5836 |
| gpt-5.5 (dab0007) | xhigh | 0.6002 |

Head-to-head, gpt-5.5 @xhigh vs Opus @xhigh (54 queries): **31 both pass, 13 both fail, 10 differ** —
4 gpt-5.5 wins, 6 Opus wins. The 10 divergences are where the behavioral difference lives.

**gpt-5.5 wins (Opus FAIL → gpt PASS):** `GITHUB_REPOS-q4`, `crmarenapro-q3`, `googlelocal-q2`,
`yelp-q6` — all *last-mile alignment*: literal output contract + intended-reading ambiguity
resolution (detail in `opus-vs-gpt5.5-failure-modes.md`).

**Opus wins (Opus PASS → gpt FAIL):** `GITHUB_REPOS-q3`, `PANCANCER_ATLAS-q3`, `crmarenapro-q13`,
`googlelocal-q3`, `googlelocal-q4`, `stockmarket-q3` — **dominated by gpt-5.5 abstaining** on cells
Opus simply computed.

## 2. The two signatures, from raw transcripts

| | **Opus-4.8** | **gpt-5.5 (xhigh)** |
|---|---|---|
| Data access under friction | reaches every source (incl. live DB) unprompted | gives up after one path miss |
| When unsure | **commits a value** — never abstains | **abstains** — `"UNABLE TO DETERMINE"` |
| Characteristic error | single-hypothesis lock-in / over-commit | premature abstention on a *reachable* source |
| Self-verification | re-derives via the same reading → correlated false-green | same |

Both signatures are quoted from transcripts:

- **Opus over-commits (with the right answer on screen).** On `stockmarket-q4` Opus printed *both* the
  correct margin ranking and the wrong count ranking, wrote "[margin] documented here but **not**
  adopted," and committed the wrong one. On `crmarenapro-q2` it found *a* policy violation and stopped,
  never checking the cost axis the gold rewards. Opus never wrote `"UNABLE TO DETERMINE"` in any cell
  examined.
- **gpt-5.5 abstains (avoidably).** On `crmarenapro-q2` xhigh never opened the alternate manifest
  `db_config.yaml` and made zero Postgres attempts before abstaining; on `agnews-q4` it never
  instantiated a `MongoClient` against the live service the config declared. The `high` run did both
  and passed — the capability was present; xhigh chose not to use it.

## 3. The reasoning-effort paradox

Counter-intuitively, **more reasoning made gpt-5.5 worse on the contested queries.** Every query in the
"flipped" pool that gpt-5.5 passed at `high` and failed at `xhigh` regressed *because of* the extra
deliberation, via two mechanisms seen in the transcripts:

- **Over-rationalizing the literal reading.** `stockmarket-q4`: `high` used the *tie* produced by the
  count metric as evidence that count was the wrong reading and chose margin (correct). `xhigh` demoted
  margin to a tiebreaker and committed to count — it *reasoned its way into Opus's exact mistake*.
- **Over-caution about the environment.** `agnews-q4`, `crmarenapro-q2`: `high` improvised data access;
  `xhigh` treated a file-glob miss as proof of absence and abstained. The extra budget was spent
  building a more careful case for *not* doing the pragmatic thing that won at `high`.

Implication: for this benchmark, the reasoning-tier knob is **not** monotonic for gpt-5.5. (A clean
high-vs-xhigh control, dab0008, is queued to quantify this.)

## 4. The shared failure mode (both models): self-anchored false-green

On genuinely hard queries the two models fail *identically* — often the **byte-identical wrong answer**
— and each ratifies it with a **verification step that re-implements the same interpretation**, so the
check is correlated with the error and cannot catch it:

- `PATENTS-q1`: both emit the same 89-CPC-code list (same EMA construction); each re-derives it and
  self-certifies PASS.
- `PANCANCER_ATLAS-q1`: all three runs group by the histology *name* (3 groups) when gold wants the
  ICD-O *code* (5 groups); both saw the code column and ignored it.
- `GITHUB_REPOS-q1`: gold ≈ 1/3 (0.33); both answer ~0.11–0.14 and neither runs a magnitude-plausibility
  check.

This is the oracle-blind wall (`[[verification-without-oracle-real-world]]`): only an *independent*
re-derivation or an external magnitude anchor breaks it. Extra xhigh reasoning does not.

## 5. The controlled intervention: dab0009 proves the abstention thesis is causal

The behavioral model predicts: *if gpt-5.5's losses are abstention, not capability, then a README rule
that forbids premature abstention should flip exactly the abstention-driven cells — and the committed
artifact should then show gpt-5.5 doing what Opus does (persist + compute).* dab0009 tested this.

**Lever:** three edits to the solver README — abstention demoted to a last resort; an explicit
"environment-persistence" routine (try `db_config.yaml` and the live `dab-postgres`/`dab-mongo` hosts
named in `db_description.txt` before concluding a source is missing); leak-guard preserved.

**Result (3-draw smokes at xhigh, the tier that abstains most):**

| cell | baseline (xhigh) | under Lever A | artifact |
|---|---|---|---|
| googlelocal-q3 | 0/1 (abstained) | **3/3** | persisted to live host, committed a value |
| PANCANCER_ATLAS-q3 | 0/1 (abstained) | **3/3** | computed the chi-square (305.12…) it had refused |
| googlelocal-q4 | 0/1 (abstained) | **2/3** | 2 real flips + 1 infra outage (not a wrong answer) |

In 8 of 9 draws the model exhibited the full persistence signature (opened `db_config.yaml`, connected
to the live host, committed a computed value, **zero** abstentions). **This is causal evidence**: the
only change was "don't quit early," and the abstention-driven failures converted to correct computed
answers — i.e. gpt-5.5 was made to behave like Opus on exactly the axis where they differ.

**A crucial null result** also fell out: the *first* dab0009 smoke targeted four cells we *assumed*
were abstention failures (`agnews-q4`, `crmarenapro-q2/q8`, `googlelocal-q3`). Only `googlelocal-q3`
flipped consistently. Reading the artifacts showed the other three were **not** abstention failures —
they are hard-analytic coin-flips (a near-tie classification; neighbor-ID confusion) that merely
*manifested* as abstention at xhigh. So abstention is a **symptom** that can mask two distinct
underlying states: (a) genuine give-up on a reachable, computable answer (Lever A fixes this), and
(b) a hard analytic problem the model can't reliably solve (Lever A exposes but cannot fix). The taxonomy
matters: only (a) is "abstention-driven."

## 6. Why the difference exists (hypothesis)

Both models read the *same* baseline instruction ("if the data doesn't support an answer, say UNABLE TO
DETERMINE"), yet behave oppositely:

- **Opus carries a strong "always produce an answer" prior** and effectively ignores the abstention
  license; it treats quitting as failure and grinds. Cost: it over-commits, including to wrong branches.
- **gpt-5.5 is more literal / instruction-faithful**, and follows the abstention license — more so at
  `xhigh`, where extra deliberation amplifies caution ("the source seems missing → the rule permits
  abstaining → abstain"). Cost: it quits on reachable data.

So the abstention behavior is partly **induced by the prompt** (the baseline README sanctioned it) and
partly **temperament** (gpt-5.5 is the more faithful rule-follower). This is why a prompt change moves
gpt-5.5 so cleanly: we are removing a license its temperament was inclined to take.

## 7. Implications

**For the loop (solver = gpt-5.5):**
- Anti-abstention (dab0009 Lever A) is the first validated DAB lever — it imports Opus's persistence
  without (yet) importing Opus's over-commitment. Carry it to a full run with a regression panel.
- Separate the two states abstention masks: pursue the *analytic-hard* coin-flips (agnews near-tie,
  crmarenapro ID-precision, stockmarket tie-disambiguation) with **different** levers; do not file them
  as anti-abstention work.
- Treat the reasoning tier as a real variable, not a "more is better" dial (§3); dab0008 will settle it.

**For benchmark interpretation:**
- A model-swap delta on DAB entangles capability with *temperament*. The headline 0.6536 vs 0.6002 is
  not "Opus computes better" — it is substantially "Opus refuses to quit and gpt-5.5 was told it could."
- Both models share the self-anchored-verification blind spot (§4); a DAB result is only as trustworthy
  as an *independent* check, which neither model performs by default.

**For the symmetry:** the two biases suggest a combined target — a solver that *persists and commits
like Opus* but *resolves ambiguity and shapes output like gpt-5.5* (gpt-5.5's 4 wins in §1). The levers
are additive on disjoint query families; the open risk is that pushing gpt-5.5 toward commitment
eventually imports Opus's over-commit failures — to be watched at the regression panel.

## Caveats

- Single-trial per cell on the full runs; the dab0009 smokes are 3-draw (consistency-checked).
- The Opus `@baseline` is one converted median run; Opus's behavior varies run-to-run, so "Opus never
  abstains" is "in the transcripts examined," strongly but not exhaustively supported.
- A recurring infrastructure flake (`dab-postgres` DNS dropping mid-trial) produces *involuntary*
  abstentions that are not behavioral — distinguish them from genuine give-up (the dab0009 deep-dives do).
