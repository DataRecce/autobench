---
title: What each model is good at, and can they learn from each other — Opus-4.8 vs gpt-5.5 on DataAgentBench
date: 2026-06-17
status: research synthesis — grounded in a 6-draw-vs-6-draw per-cell band + raw-transcript reads of every clean divergent cell
supersedes_framing_in: opus-vs-gpt55-behavioral-model.md  (the "Opus commits / gpt abstains" model is a special case of the two-axis model below)
data:
  opus_xhigh:  5 runs ~/dataagentbench/_runs/spacedock-opus-4-8-xhigh-hint/run-00{3..7} + @baseline (e14e49869e6412de)  = 6 draws/cell
  gpt55_xhigh: dab0007 (9b0a658e) + 5 CAIS spacedock-codex-5.5-xhigh-hint  = 6 draws/cell  (band: _artifacts/baseline-variance-6draw.md)
  gpt55_high:  dab0008 (035dd36e) — 1 draw, tier control
  transcripts: gpt per-query steps/main/agent/codex.txt; Opus per-dataset claude-output.jsonl
---

# TL;DR

Judged the way we should judge (each model's **6-draw band**, not one lucky draw), **Opus-4.8 and
gpt-5.5 are statistically tied on DataAgentBench** — mean per-cell pass **0.6975 (Opus) vs 0.7037
(gpt-5.5)**. The famous 0.6536-vs-0.6002 single-draw headline was mostly noise. Of 54 cells, **34 both
solve, 11 both fail (the hard/oracle-blind wall), and only ~7 genuinely diverge.** Those 7 are a
**temperament trade, not a capability gap** — and the trade is *symmetric*: each model wins the cells
that play to its bias and loses the cells where the same bias backfires.

The divergence runs on **two axes**, and each model is *literal* on one axis and *elaborative* on the
other:

| axis | Opus-4.8 | gpt-5.5 | who wins which cell |
|---|---|---|---|
| **Output** | terse / literal — emits exactly the contract | elaborative — decorates the answer | Opus wins when "no extra" matters (stockmarket-q3); gpt wins when "must be complete" matters (yelp-q6) |
| **Analysis** | elaborative — over-reasons into a "sensible" reading | literal — faithful to the data/schema semantics | gpt wins when the literal semantics is the gold (GITHUB_REPOS-q4); Opus wins by persisting on hard joins (crmarenapro-q10) |

So: **gpt should learn Opus's output discipline and persistence; Opus should learn gpt's analytic
literalism and list-completeness.** But the two output biases are in *tension* — the fix for one cell is
the bug for another — so the import has to be **shape-aware**, not a blunt "be terse / be thorough."

---

# 1. The aggregate picture is a TIE (the single-draw headline was noise)

Per-cell pass rate over 6 no-lever xhigh draws each:

| | Opus-4.8 | gpt-5.5 |
|---|---|---|
| mean per-cell pass (6-draw) | **0.6975** | **0.7037** |
| single-draw headline (1 run) | 0.6536 | 0.6002 |

The single-draw gap put Opus ahead by ~5 points; the multi-trial band erases it (gpt nominally ahead by
<1 point — inside noise). **Conclusion: there is no meaningful overall capability gap on DAB at xhigh.**
What looked like "Opus is better" was variance plus a few cells each model owns.

Cell census (6-draw band, both models):
- **34 both-solid** (both ≥5/6) — shared competence, no signal.
- **11 both-hard** (both ≤1/6): DEPS_DEV_V1-q1, GITHUB_REPOS-q1/q2, PANCANCER_ATLAS-q1, PATENTS-q1/q2/q3,
  agnews-q2/q3, crmarenapro-q2, crmarenapro-q8 — the oracle-blind / genuinely-hard wall. **Neither model's
  strength touches these**; both fail them the same way (self-anchored false-green, see
  `opus-vs-gpt55-behavioral-model.md §4`).
- **~7 genuinely divergent** — the subject of this study.

The divergent cells:

| cell | Opus | gpt-5.5 | owner |
|---|---|---|---|
| stockmarket-q3 | **5/6** | 0/6 | Opus (exclusive) |
| crmarenapro-q10 | **6/6** | 4/6 | Opus |
| crmarenapro-q13 | **6/6** | 4/6 | Opus |
| GITHUB_REPOS-q4 | 0/6 | **6/6** | gpt (exclusive) |
| agnews-q4 | 1/6 | **4/6** | gpt |
| yelp-q6 | 1/6 | **4/6** | gpt |
| googlelocal-q2 | 0/6 | 2/6 | gpt (weak) |

---

# 2. The evidence — four divergent cells, read from the raw logs

## 2a. stockmarket-q3 — Opus 5/6, gpt 0/6 — *Opus's output literalism wins*

The gold answer is a **ranking**: `company_name → average-2008-trading-volume` for financially-troubled
NASDAQ companies. **Both models computed the same 15 companies and the same numbers.** They diverged only
at the final string:

- **gpt-5.5 (FAIL, every draw)** injected the company *description* into each row:
  > `"Apex Global Brands Inc. specializes in creating and marketing a diverse portfolio of fashion and
  > lifestyle brands…: 23781.42; BIO-key International, Inc. specializes in advanced biometric solutions…:
  > 10988.14; …"`

  The verifier's normalized-string match rejected it — the narrative is not in the gold.
- **Opus (PASS)** emitted exactly: `"Frontier Communications Corporation: 254397.63; Correvio Pharma Corp.:
  145247.83; …"` — names + numbers, nothing else.

**This is not abstention and not a compute gap. It is gpt over-elaborating the output.** Opus's literal
"answer only the question, no commentary" instinct is the whole win.

## 2b. GITHUB_REPOS-q4 — gpt 6/6, Opus 0/6 — *gpt's analytic literalism wins*

Question: top-5 repos whose **main language is not Python**, by commit count.

- **gpt-5.5 (PASS)** wrote a clean `JOIN main_language ml … WHERE ml.main_language <> 'Python'`. The INNER
  JOIN *correctly* drops `torvalds/linux` (it has **no parsed-language row** → ineligible), promoting
  `tensorflow/tensorflow` into slot 5. gpt followed the literal schema semantics.
- **Opus (FAIL)** reasoned its way *out* of the correct filter:
  > "`torvalds/linux` has no `languages` row, but its main language is therefore certainly not Python …
  > excluding it on a metadata-absence technicality would be **unreasonable**."

  Opus *explicitly knew* tensorflow/tensorflow was the literal 5th pick and over-rode it on a "that seems
  unreasonable" judgment — and committed the wrong set.

**This is Opus's over-reasoning signature: it elaborates the analytic interpretation past the literal data
semantics. gpt's faithfulness to "what the JOIN actually means" is the win.**

## 2c. yelp-q6 — gpt 4/6, Opus 1/6 — *Opus's output literalism BACKFIRES*

Question: highest-avg-rating business (≥5 reviews, H1-2016) **and its category(ies)**. The gold category
field is a **list**: `Restaurants, Breakfast & Brunch, American (New), Cafes`.

- **gpt-5.5 (PASS)** emitted the full list: `"Coffee House Too Cafe; Restaurants, Breakfast & Brunch,
  American (New), Cafes"`.
- **Opus (FAIL 4/5 runs)** emitted only the first element: `"Coffee House Too Cafe, Restaurants"` →
  verifier: *"Missing category: breakfast & brunch."* (One run, 007, did emit the full list and passed —
  so it's a non-deterministic truncation, not inability.)

**Same Opus terseness that won 2a loses here:** when the answer is multi-valued, "minimal output" drops
list elements. gpt's elaborative output bias makes it complete by default.

## 2d. crmarenapro-q10 / q13 — Opus 6/6, gpt 4/6 — *Opus's persistence wins on hard joins*

Both ask for a specific Salesforce **agent ID** behind a subtle multi-table window query (q10: lowest avg
handle time among agents with >1 case; q13: top sales over a 5-month window via Opportunity→Contract→Order).

- **Opus (PASS 6/6)** grinds the join to a single committed ID every time.
- **gpt-5.5 (FAIL draws)** fails two ways:
  - **abstains** — q10: *"each belongs to a different sole assignment agent; the `having count(*) > 1`
    ranking result is empty"* → returns `UNABLE TO DETERMINE` (a join-cardinality slip, then it quits
    instead of revisiting the grouping).
  - **mis-disambiguates** — q13: computes a clean revenue total but for a **neighbor** agent
    (`005Wt000003NEa3IAG` @ 46919.15 instead of the gold `…NIXCIA4`).

**Here Opus's "never quit, always commit" persistence is the asset; gpt's abstention license + literalism
let it stop at the first dead-end.** (This is the one axis the old behavioral model captured.)

---

# 3. The two-axis model

The four cells resolve into **two independent biases**, and each model sits on the *opposite* end of each:

```
                 LITERAL  <─────────────>  ELABORATIVE
 OUTPUT axis     Opus (terse)              gpt (decorates)
 ANALYSIS axis   gpt (schema-faithful)     Opus (over-reasons / persists)
```

- **Opus** = *output-literal, analysis-elaborative.* Wins stockmarket-q3 (terse output) and crmarenapro
  q10/q13 (grinds the analysis to a committed answer). Loses GITHUB_REPOS-q4 (reasons past the literal
  schema) and yelp-q6 (terseness drops a list element).
- **gpt-5.5** = *output-elaborative, analysis-literal.* Wins GITHUB_REPOS-q4 (faithful JOIN semantics) and
  yelp-q6 (complete list). Loses stockmarket-q3 (decorates the output) and crmarenapro q10/q13 (literalism
  + abstention license → quits on a hard join).

The earlier "Opus over-commits / gpt abstains" model is the **Analysis axis** alone. The new piece is the
**Output axis**, which is *opposite in sign* — and it explains the cells the abstention model couldn't
(stockmarket-q3, yelp-q6 are output failures, not commit/quit failures).

---

# 4. Can gpt learn Opus's good, and Opus learn gpt's good?

Yes in principle, and the targets are concrete — but the two output biases are in **tension**, so this is
a shape-aware transplant, not a global dial.

### What gpt-5.5 should import from Opus
1. **Output discipline (high value, we can lever this).** "Answer the question literally — names/numbers
   only, no descriptions or narrative." This directly fixes stockmarket-q3 and the whole gpt
   over-elaboration failure class. **This is exactly concept `dab0001` (output-contract lever)** —
   stockmarket-q3 is now its single strongest evidence cell (both models compute the same answer; only the
   shape differs).
2. **Persistence on hard joins (high value, but RISKY to lever).** "Don't abstain on a reachable join;
   commit a best computed ID." This is the anti-abstention family (dab0009/dab0010) — which we **rejected**:
   it perturbed stable cells and the apparent gains were single-draw phantoms. So importing Opus's
   persistence is real in theory but has so far cost more than it bought.

### What Opus should import from gpt-5.5
*(We don't operate Opus in this loop — gpt-5.5 is the solver — so this is diagnostic, not a lever we'll
build. Recorded for benchmark interpretation and any future Opus-solver work.)*
3. **Analytic literalism.** "Respect the literal data/schema semantics — an INNER JOIN excludes
   no-metadata rows; don't override it because the result 'seems unreasonable.'" Fixes GITHUB_REPOS-q4.
4. **List completeness.** "When the answer is multi-valued, emit the full list, not the first element."
   Fixes yelp-q6.

### The catch: the output fixes fight each other
- Telling gpt "**be terse**" (to win stockmarket-q3) risks making it drop list elements like Opus does on
  yelp-q6.
- Telling Opus "**be complete**" risks it adding narrative like gpt does on stockmarket-q3.

So an output-contract lever **must branch on answer shape** — *scalar / ranking → terse names+numbers; list
→ full enumeration* — rather than a single "be concise" or "be thorough" rule. A blunt version trades one
cell for another and nets ~zero. This is the design constraint dab0001 has to respect to actually bank
stockmarket-q3 without regressing yelp-q6 (which gpt already passes 4/6).

---

# 5. Implications for the loop

- **The headline reframes:** gpt-5.5 ≈ Opus on DAB (tied on the 6-draw band). There is no broad capability
  deficit to close — only ~7 temperament-driven cells, split roughly evenly. Chasing "beat Opus" by levering
  gpt is a few-cell game, not a regime change.
- **dab0001 (output-contract) is the cleanest live bet** and stockmarket-q3 is its proof case — but it must
  be **shape-aware** (§4 catch) or it will give back yelp-q6. Recommend: a verify-stage rule that re-shapes
  the answer to the gold's implied shape (scalar / delimited ranking with names+numbers only / full list),
  with worked foreign-domain examples for *both* the terse and the list case.
- **Persistence (anti-abstention) stays closed.** It's a genuine Opus strength gpt lacks (crmarenapro
  q10/q13), but every attempt to import it destabilized the protected 6/6 band. Don't reopen without a
  mechanism that's gated to abstention-only cells.
- **The both-hard 11 are untouched by cross-learning.** Neither model's strength helps there; they need an
  oracle/independent-check mechanism, not a temperament transplant.

# Caveats
- The 5 CAIS gpt draws may use a slightly older baseline README than the current `spacedock-readme-baseline`;
  the 6/6 and 0/6 cells are robust regardless, the mid-band cells (4/6) carry ±1-draw uncertainty.
- "Opus never abstains / always terse" is "in the transcripts examined" — strongly but not exhaustively
  supported; yelp-q6 run-007 shows Opus's truncation is non-deterministic, not absolute.
- gpt-5.5 @high (dab0008) was a single tier-control draw; the two-axis model is built on the xhigh bands.
- Cross-learning feasibility for traits 3–4 (Opus side) is diagnostic only — we operate gpt-5.5, not Opus.
