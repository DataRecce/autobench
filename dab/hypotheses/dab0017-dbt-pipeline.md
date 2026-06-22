---
id: dab0017
title: Mandatory dbt-pipeline solver — build+validate dbt models per dataset, answer by querying the mart
status: conclude
kind: hypothesis
source: CL "staged unified data solver" concept; design doc dab/docs/specs/2026-06-21-dbt-pipeline-solver-design.md + handoff dab/docs/plans/2026-06-21-dbt-pipeline-implementation-handoff.md. Distinct from the output-contract/anti-abstention families — this is a METHODOLOGY lever (force every dataset through a built+validated dbt pipeline; answer stage = pure query over the mart).
started: 2026-06-21T09:30:00Z
score: 0.5
completed: 2026-06-22T03:57:37Z
verdict: rejected
---

## Hypothesis

Does forcing **every** dataset through a built + validated **dbt** pipeline — so the answer
stage becomes a pure "query the dbt models" step — move codex/gpt-5.5's stratified Pass@1 above
the Opus incumbent **without regressing currently-passing queries**? Single lever = the solver
README (dbt is baked into the image, held constant). Fork `spacedock-readme-baseline` →
`dab0017-dbt-pipeline`: `model` builds generic `stg_* → int_*/mart_*` + dbt tests (loop until
green); `analyze` queries the green mart only; `verify` unchanged + rejects per-question models.

Full design + rationale: `_artifacts/dab0017-dbt-pipeline/` (run-notes.md, feasibility.md,
canaries.md, smoke.md). Each gate was antagonist-reviewed (per captain instruction).

## Acceptance criteria (falsifiable)

- **Smoke GO** iff ≥1 currently-failing target query flips to PASS **by committed generic
  dbt-model artifact** (behavioral read) AND **zero** Opus ∩ `@codex-batch-baseline` passers (36
  canaries) regress anywhere in the smoke set.
- **Full PASS** iff (a) stratified Pass@1 over 12 beats Opus 0.654 on a clean strict audit AND
  (b) zero of the 36 canaries regress (per-query table). Net-positive that trades incumbent
  passers = FAIL.
- **Overhead falsifier:** broad regression across many datasets ⇒ mandatory-dbt falsified →
  fall back to gating (design §3/§7). A single regression blocks the run.

## Environment work (prerequisite, not the lever)

- **dbt baked into `dab-agent:latest`** (`dbt-core dbt-duckdb`, `--ignore-installed` for the
  debian-managed dep overlay). Digest `sha256:224133f0…`.
- **DuckDB sqlite/postgres scanner extensions preinstalled** into exedev's default extension home
  so `ATTACH (TYPE SQLITE|POSTGRES)` autoloads OFFLINE (run container blocks egress to
  extensions.duckdb.org). Captain Option-A decision after Gate 0 falsified design §5-item-2.
- **verify_batch per-query try/except** — razorback **PR #19**: one query's validator crash
  (e.g. `.lower()` on a list answer) no longer aborts the whole dataset's grading.
- **Connection-host fix (captain Option A):** the baseline README hardcoded `localhost` for
  postgres/mongo, but the spacedock workspace runs them at `dab-postgres`/`dab-mongo`. Forked
  anchor README → `spacedock-readme-baseline-hostfix` (host + password + pymongo-for-mongo);
  variant README uses correct hosts + a pymongo→dbt-seed bridge for mongo-only data (yelp/agnews).
  Held constant on both sides → only dbt differs.

## Target queries

Targets (codex-batch fails): crmarenapro q2,q3,q7,q8; GITHUB_REPOS q1,q2 (+ headroom PATENTS,
agnews, DEPS_DEV, PANCANCER). Canaries = 36 Opus ∩ `@codex-batch-baseline` passers (canaries.md).

## Anchor (Gate 1.5)

`@codex-batch-baseline` = `runs/codex-dab-batch-baseline/bf113446fdd94373` (host-fixed, no dbt):
**stratified Pass@1 0.6966 over all 12, 0 errored, audit clean** — already beats Opus 0.654.
codex-batch regresses vs Opus only on crmarenapro q7 (dbt-independent); gains GITHUB_REPOS q4,
stockmarket q4, yelp q6. Antagonist (antagonist-gate15): ANCHOR VALID; 36-canary set trustworthy.

## Stage Report: feasibility (Gate 0)

- DONE: re-probe on the extension-fixed image (`runs/dab-gate0-probe/1e1f3a87afc9d073`) — one
  generic dbt pipeline (44 models, sqlite+duckdb+postgres ATTACHed offline) served all 13
  crmarenapro queries; verify_batch produced per-query rewards; scratch.duckdb persisted
  model→analyze. Generic-mart discipline held (no per-question models, no hardcoded answer
  literals). 7/13 (honest generic-pipeline number; probe-1's 11/13 was explore-then-fit overfit).
  Antagonist (antagonist-gate0-reprobe): RE-PROBE PASS, no blockers before Gate 1.

## Smoke result (Gate 2): NO-GO

Run-dir `runs/dab0017-dbt-pipeline/01e0442e6da23d51` (smoke: crmarenapro, GITHUB_REPOS +
bookreview, music_brainz_20k, stockindex, stockmarket).

| dataset | anchor | variant | Δ |
|---|---|---|---|
| crmarenapro | 9/13 | 8/13 | −1 (flip q3↑; regress q12,q13↓) |
| GITHUB_REPOS | 2/4 | 2/4 | 0 (q1,q2 not flipped) |
| stockmarket | 5/5 | 4/5 | −1 (regress q3) |
| bookreview / music_brainz_20k / stockindex | 3/3 | 3/3 | 0 ✓ |

**1 flip, 3 canary regressions → NO-GO** (zero-regression bar violated). Antagonist
(antagonist-gate2): NO-GO CONFIRMED, but the regressions are **dbt-orthogonal** — crmarenapro
q12/q13 are interpretation divergences on ambiguous ranking wording (the marts held the correct
data; analyze stage chose created-date / opportunity-owner), stockmarket q3 is a decoration
false-RED (correct numbers, broke the verifier's name-near-number proximity check). The flip
(crmarenapro q3) is real + generic (mart_opportunities ⨝ mart_activity_touchpoints surfaced
negotiation evidence the anchor missed). Generic-mart discipline held; no false-greens.

**Cross-learning:** the regression fixes fall into KNOWN dead README families — q12/q13 =
dab0016 analytic-semantics pinning (inert + destabilizing); stockmarket q3 = dab0012/dab0015
decoration (README-inert). temp=0 ⇒ near-deterministic, multi-trial unlikely to rescue. So
mandatory-dbt is **validated as a capability but not promotable** as a single-lever change, and
the gap is not README-recoverable.

## Stage Report: smoke (re-smoke, tuned README) — NO-GO (strict bar), near break-even

Run-dir `runs/dab0017-dbt-pipeline/1fec1a9f66e7d7f2` (8 datasets incl. yelp+agnews mongo).
Tuned README: mongo host `dab-mongo:27017` made redundant/inline (×3), dab0015 flat-string
serialization, ADE-h0061-inspired grain re-aggregation + completeness discipline (analyze +
verify). Smoke net: **32 vs anchor 33 = −1** (vs the prior dbt smoke which collapsed yelp to 0).

- DONE: targeted fixes LANDED — yelp **0→5** (mongo host reached, 21 `dab-mongo` hits, 0 refused),
  GITHUB q4 **0→1** (flat-string), music_brainz q1 **0→1** (grain re-aggregate), stockmarket q3
  fixed. 3 HARD crmarenapro targets flipped (q2, q3, q7).
- FAILED (3 canary regressions vs anchor → strict NO-GO):
  - crmarenapro q12 — `…NJgAIAW` vs `…NDEBIA4`: the **dab0016 date-anchor ambiguity**
    (created-vs-signed date); deterministic at temp=0, **README-inert dead family**.
  - yelp q4 — value `3.63` not found: residual analyze computation miss (mongo now reached).
  - yelp q7 — missing category `Breakfast & Brunch`: residual list-completeness miss.
- Also lost (variance, not canaries): crmarenapro q8 (1→0), agnews q2 (1→0) — both were
  single-trial flips in the prior run, not stable.

Verdict: **NO-GO on the strict zero-regression bar (3 canary regressions).** The tuning worked
(near break-even, +5 yelp recovery, 3 target flips), but one regression (crmarenapro q12) is an
unfixable dab0016 dead-family wall, so the zero-regression bar can't be cleared via the README.

## Score estimate — tuned full-2, recorded BEFORE the run (calibration)

Predicted on the tuned re-smoke (8 datasets observed) + stable history for the 4 not smoked.
**Recorded 2026-06-22 to check against the actual full-2 and diagnose any gap.**

| dataset | basis | est. pass@1 |
|---|---|---|
| crmarenapro | tuned smoke 11/13 | 0.846 |
| yelp | tuned smoke 5/7 (mongo fixed) | 0.714 |
| stockmarket | tuned smoke 4/5 | 0.800 |
| GITHUB_REPOS | tuned smoke 2/4 | 0.500 |
| agnews | tuned smoke 1/4 | 0.250 |
| bookreview / music_brainz_20k / stockindex | tuned smoke 3/3 | 1.000 ea |
| googlelocal | not smoked; 3/4 + possible q3 completeness recovery | 0.75–1.0 |
| PANCANCER_ATLAS | not smoked; stable | 0.667 |
| DEPS_DEV_V1 | not smoked; stable | 0.500 |
| PATENTS | not smoked; 0/3 everywhere | 0.000 |

**Central estimate: ≈ 0.67 ; range ~0.67–0.72.** Coin-flip cells driving the range:
googlelocal q3 (completeness fix recovers? +0.02), agnews q2 (variance +0.02), crmarenapro q8
(variance +0.006). Predicted standing: **beats Opus 0.654**, roughly **ties anchor 0.697**
(central just under), **+0.10–0.15 over the untuned dbt full (0.565)**. Predicted gate: still
**NO-GO** — canary regressions persist (crmarenapro q12 dab0016 wall; yelp q4/q7), so it fails
the zero-regression bar even if it tops Opus on aggregate. *(Estimator: dab0017 operator.)*

## Run result (full-2, TUNED) + estimate calibration

Run-dir `runs/dab0017-dbt-pipeline/0d7c317983011f71` (all 12, matrix). Clean audit (12/12, 0
errored). **Actual stratified Pass@1 = 0.6027** — vs my recorded estimate **≈0.67** → **estimate
was 0.067 too HIGH**. Standing: **BELOW Opus 0.654**, below anchor 0.697, only +0.038 over the
untuned full (0.565). **My "beats Opus" prediction was WRONG.**

| dataset | estimate | actual | gap | why |
|---|---|---|---|---|
| yelp | 5/7 (0.714) | **6/7** | +0.14 | mongo fix even more solid than smoke |
| crmarenapro | 11/13 (0.846) | **9/13** | −0.15 | smoke draw was favorable; full reverted q2/q9 (q12 recovered) |
| stockmarket | 4/5 (0.800) | **3/5** | −0.20 | smoke q3 fix did NOT hold on the full draw |
| googlelocal | 0.75–1.0 | **2/4** | −0.25 | UNSMOKED; q4 regressed (number-near-name), completeness fix didn't recover q3 |
| PANCANCER_ATLAS | 2/3 (0.667) | **1/3** | −0.33 | UNSMOKED; q3 regressed (305.12 not computed) |
| others | — | matched | 0 | GITHUB 2/4, agnews 1/4, bookreview/music_brainz/stockindex 3/3, DEPS 1/2, PATENTS 0/3 |

**Calibration finding — the smoke is NOT predictive of the full for a GENERATIVE lever.** The
grain/completeness/ranking discipline fires on *every* cell, so it re-rolls interpretation on
every cell. Between smoke and full (SAME README, temp=0) ≥8 cells flipped BOTH directions:
crmarenapro q2 1→0, q9 1→0, q12 0→1, q13 1→0; stockmarket q3 1→0; yelp q4 0→1, q6 1→0, q7 0→1.
My estimate erred by (a) trusting smoke per-cell scores as stable (crmarenapro/stockmarket drew
high in smoke, low in full) and (b) assuming the 4 unsmoked datasets were inert when the
generative rules regressed PANCANCER q3 + googlelocal q4. **This RECONFIRMS dab0016: a
generative analyze rule destabilizes the board rather than reliably helping.** A lever whose
single-draw score swings ~±0.07 on the same README is not a stable improvement — that variance
is itself a NO-GO, independent of the aggregate.

Canary regressions (5): crmarenapro q9, crmarenapro q13, stockmarket q3, googlelocal q4,
PANCANCER_ATLAS q3 → strict NO-GO. Flips held: crmarenapro q3, q7 (real dbt-method, generic).

## Run result (full-1, UNTUNED dbt — superseded by full-2)

Run-dir `runs/dab0017-dbt-pipeline/d4ddf0514cd77cd1` (all 12, matrix). **Clean audit: 12 clean,
0 errored, 0 tainted.** **Variant stratified Pass@1 = 0.565** vs anchor `@codex-batch-baseline`
0.6966 vs Opus 0.654 → **below both → FAIL on aggregate.**

| dataset | anchor | variant | Δ | character |
|---|---|---|---|---|
| **crmarenapro** | 9/13 | **11/13** | **+2** | flipped HARD targets q2,q3,q8 (Opus+codex both fail) — dbt entity-resolution WIN |
| agnews | 1/4 | 2/4 | +1 | flipped q2 |
| googlelocal | 3/4 | 3/4 | 0 | q2 flip / q3 regress (swap) |
| bookreview / stockindex / PANCANCER / DEPS_DEV / PATENTS | = | = | 0 | held |
| GITHUB_REPOS | 2/4 | 1/4 | −1 | regress |
| music_brainz_20k | 3/3 | 2/3 | −1 | regress q1 |
| stockmarket | 5/5 | 3/5 | −2 | regress |
| **yelp** | 7/7 | **0/7** | **−7** | **COLLAPSE** — mongo bridge failed |

**Flips (anchor fail → variant pass):** crmarenapro q2,q3,q8; agnews q2; googlelocal q2 (5).
**Canary regressions:** crmarenapro q13, googlelocal q3, music_brainz_20k q1, stockmarket q3,
yelp q1,q2,q3,q4,q5,q7 (10) → **FAIL on non-regression.**

**yelp collapse mechanism:** the variant agent used `MongoClient` but **never connected to
`dab-mongo`** (0 hits; 4× "connection refused", 3× ServerSelectionTimeout → 50× UNABLE TO
DETERMINE). The anchor aced yelp 7/7 because its README put `MongoClient("mongodb://dab-mongo:27017")`
prominently in DB-access; the variant buried the pymongo→dbt-seed bridge in the model stage and
the agent fell back to a refused localhost connection. The dbt indirection made mongo access
LESS reliable — a variant-README defect compounded by the mongo-has-no-dbt-adapter awkwardness.

## FINAL Conclusion (after tuned full-2)

**Verdict: REJECTED — confirmed across BOTH the untuned (0.565) and tuned (0.6027) full runs.**
The tuned dbt+quality variant does **NOT** beat Opus (0.654) on the honest full board, does not
reach the anchor (0.697), and fails the strict zero-regression bar (5 canary regressions). The
mongo-host + flat-string fixes worked (yelp 0→6/7, GITHUB q4); the dbt method genuinely flips 2
hard crmarenapro targets (q2/q3/q7 generic, artifact-confirmed). But:
- **The generative grain/completeness/ranking discipline destabilizes the board, it does not
  reliably help** — reconfirming dab0016. ≥8 cells flipped both directions between smoke and
  full on the SAME README at temp=0; two unsmoked datasets (PANCANCER q3, googlelocal q4)
  regressed under it. A lever that swings ~±0.07 per draw is not a promotable improvement.
- **The smoke over-predicted the full** (32/33 ≈ break-even → 0.603) — for a fires-everywhere
  lever the smoke subset is not representative; judge the full board, not the smoke.
- **dbt-advantage still unproven as a net win.** crmarenapro flips are real but small; they're
  swamped by board-wide variance + residual analyze misses + the tuning's added confound.

Promotable direction remains, at best, **GATED dbt on dirty-relational datasets ONLY** (where the
crmarenapro entity flips live) — but that is an untested next hypothesis, not validated here.
Seed README + design UNCHANGED. dab0017 CONCLUDED REJECTED. Follow-up: **dab0018** (classifier-gated dbt).

### WHY only crmarenapro benefits (structural — the key insight)

dbt's value = materializing correct **derived intermediate entities from multi-source joins** once
in the `int_`/`mart_` layer. That pays off only when a dataset meets BOTH conditions — and
crmarenapro is the ONLY one of 12 that does:
1. **Richly multi-source:** crmarenapro = **6 source DBs** (3 sqlite + 2 duckdb + 1 postgres);
   **every other dataset = exactly 2.** (Verified from each `db_config.yaml`.)
2. **Failures are derivation-shaped** (blocked on a missing multi-hop join), not format/compute:
   q3 needs opportunities ⨝ activity voice-call transcripts to *derive* "Negotiation" (raw
   `stage_name` says "Discovery"); q8 = case-history ⨝ agents transfer count; q2/q7 = case ⨝
   knowledge-base. The direct-SQL anchor reconstructs these ad-hoc per query and misses them; the
   materialized `int_` model gets them (q3 held across BOTH dbt runs).

The other 11 get nothing because they are either **no-headroom** (anchor already 3/3–7/7:
bookreview, music_brainz, stockindex, stockmarket, yelp → dbt can only tie/regress) or
**headroom but not derivation-shaped** (googlelocal q2 serialization, GITHUB q1/q2 parse, PATENTS
hard, DEPS_DEV/PANCANCER single-source compute, agnews mongo text-classification → a mart can't
unlock them, only adds a layer to mis-aggregate). So the design's spine thesis is sound but DAB's
mix gives it ~one place to pay off → even gated, the ceiling is ~+2 cells (~+0.03), unstable.

### (historical) Conclusion (full-1, UNTUNED)

**Verdict: REJECTED — mandatory-dbt FALSIFIED, and the dbt-advantage thesis UNPROVEN (confounded).**
Corrected after the acceptance antagonist (antagonist-accept) refuted my first-pass attribution
with artifact evidence; I accept the correction.

- **Mandatory-dbt FAILS (confirmed both legs).** Variant stratified Pass@1 **0.565 < Opus 0.654
  < anchor 0.697**; **10 canary regressions**. Clean audit (12/12, 0 errored). The unified
  "every dataset through dbt" decision is falsified by broad regression (design §3/§7 trigger).
- **The crmarenapro "win" is NOT attributable to dbt entity-resolution.** The flips (q2,q3,q8)
  are real passes but show **no mechanism delta vs the no-dbt anchor**: the variant's dirty-key
  handling is a `norm_id` = `lower(regexp_replace(trim,'^#+',''))` `#`-strip, and the **anchor
  did the byte-identical `strip().lstrip('#')` in plain Python**. The README's flagship
  OR-cluster `resolved_entity_id` mechanism **never fired** in any crmarenapro model. The flips
  are single-trial interpretation variance on hard CRM-semantics queries (±noise band), and came
  WITH a crmarenapro regression (q13 — variant returned the wrong agent AND an uncleaned `#`),
  which contradicts a "dbt resolves dirty keys better" story. **The design's core spine is NOT
  validated by this run.**
- **The two biggest losses are FIXABLE WRAPPER DEFECTS, not intrinsic dbt costs (confounds):**
  1. **yelp 7→0** — the FO two-phase re-summarization **dropped the `dab-mongo` host** from the
     variant's dispatch prompt (db_config.yaml gives no host; it lived only in prose). The agent
     tried only `localhost` → refused → abstained 7×. The anchor carried the host inline → 7/7.
     Proven fixable: **agnews (also mongo) DID reach dab-mongo and flipped q2.** Not a dbt-mongo
     limitation.
  2. **GITHUB_REPOS q4** — variant produced the IDENTICAL 5 repos as the anchor but serialized
     them as a JSON **list** → verifier `'list'.lower()` reject → false-RED (the dab0015
     serialization-format family). Substantively correct.
- **Genuine (small) dbt-overhead losses:** music_brainz q1, stockmarket q3/q4, googlelocal q3,
  crmarenapro q13 — real compute/interpretation divergences from routing through the generic
  mart (the abstraction layer adds places for the analyze SELECT to diverge). Supports the
  mart-overhead hypothesis, but small.
- **GATED-dbt is an untested NEXT hypothesis, NOT a validated direction.** The "dbt wins on
  dirty-relational, loses on mongo/clean" story is only half-supported and partly wrong: the
  crmarenapro edge is unproven (no mechanism delta vs anchor) and the motivating regressions are
  dominated by fixable wrapper bugs, not a clean dirty/clean split. To test gated-dbt fairly you
  must FIRST fix (a) the FO mongo-host drop and (b) the string-serialization contract, THEN re-run
  to see whether crmarenapro's dbt edge is reproducible AND attributable once confounds are removed.
- **Seed README + design UNCHANGED.** Mandatory-dbt not promoted. Knowledge banked (see memory):
  mandatory-dbt falsified; dbt-advantage unproven (confounded by wrapper bugs); the FO
  re-summarization can silently drop load-bearing connection details; generic-mart discipline
  held cleanly (no per-question models / no answer literals across the board).

## Verdict

**REJECTED** (frontmatter already set; this distills the closure for a teammate reading the body).
dab0017 = MANDATORY dbt-pipeline solver — force every dataset through a built+validated `stg→int→mart`
pipeline, answer = query the mart.

**Failure mechanism.** Mandatory-dbt FALSIFIED across BOTH legs: untuned full **0.565** and tuned
full (mongo-host-fix + flat-string + grain/completeness discipline) **0.6027** — both **< Opus
0.654 < anchor `@codex-batch-baseline` 0.697**. Untuned had **10 canary regressions**, tuned had 5.
dbt pays off on only 1 of 12 datasets (crmarenapro, the sole ≥3-source set with derivation-shaped
failures) while its build overhead + the generative grain/ranking discipline taxes + destabilizes
the other 11 (≥8 cells flipped both directions smoke↔full on the SAME README at temp=0; 2 unsmoked
datasets — PANCANCER q3, googlelocal q4 — regressed). A lever that swings ~±0.07 per draw is not a
promotable improvement.

**Did the change reach the committed artifact? The crmarenapro "win" was UNPROVEN here (confounded).**
The dab0017 crmarenapro flips (q2/q3/q8) were real PASSES but showed **no mechanism delta vs the
no-dbt anchor** — the variant's dirty-key handling was a `norm_id = lower(regexp_replace(trim,'^#+',''))`
`#`-strip and the anchor did the byte-identical `strip().lstrip('#')` in plain Python; the README's
flagship `resolved_entity_id` OR-cluster NEVER FIRED in any crmarenapro model, and the flips came
WITH a q13 regression (wrong agent + uncleaned `#`), contradicting the "dbt resolves dirty keys"
story. (This no-mechanism-delta gap is exactly what dab0018's gated revision later CURED — see below.)

**Two biggest losses were FIXABLE WRAPPER bugs, not dbt:** yelp 7→0 = the FO two-phase
re-summarization dropped the `dab-mongo` host → localhost refused (proved fixable, retest 0→6/7);
GITHUB q4 = JSON-list serialization false-RED. These confounds inflated the apparent dbt cost.

**Transferable rules (banked knowledge):**
- **Mandatory (fires-everywhere) dbt is dead for DAB** — the overhead/variance tax dominates DAB's
  2-source-heavy mix.
- **Calibration lesson:** a generative fires-everywhere lever's SMOKE is NOT predictive of the full
  board (the smoke over-predicted: 32/33 ≈ break-even → full 0.603); judge the full board, and
  expect ±0.07 single-draw variance from such a lever (reconfirms dab0016).
- **Reusable infra KEPT:** dbt + sqlite/postgres scanners baked into the `dab-agent` image; the
  host-fix fork (localhost→dab-postgres/dab-mongo); `verify_batch` per-query try/except (razorback
  **PR #19**, merged); `@codex-batch-baseline` registered (0.697 > Opus 0.654, the new anchor).
- **Follow-up [[dab-gated-dbt-self-cancelling]] (dab0018)** isolated and CONFIRMED the closure:
  gating dbt to ≥3-source datasets (only crmarenapro) with a zero-leak source-count classifier
  removed the board-wide tax AND cured the no-mechanism-delta gap (q3/q7 proven to reach the
  committed int_ answer, not a #-strip) — yet STILL landed REJECTED (full3 0.6927 < 0.6966) because
  the crmarenapro advantage is too small (~+0.013) and self-taxes a stable cell (q9). **dbt family
  CLOSED for DAB** with full-board evidence from both hypotheses.
- Seed README + design UNCHANGED.
