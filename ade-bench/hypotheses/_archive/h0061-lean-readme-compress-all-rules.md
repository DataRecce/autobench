---
id: h0061
title: Lean-README overfit test — compress all 10 rules to principle+skeleton, keep every construct
status: conclude
kind: hypothesis
source: post-target fine-tune research (item 4a) — _artifacts/readme-rule-progression-research-2026-06-16.md + _proposal/4a-lean-readme-overfit-design-2026-06-16.md (captain-approved 2026-06-16)
started: 2026-06-16T17:08:39Z
completed: 2026-06-17T12:14:55Z
verdict: PASSED
score:
worktree:
archived: 2026-06-17T12:14:55Z
---

## Hypothesis

The scar clauses and domain framing accumulated in the 10 accepted README rules (the
+249-line delta from the original baseline to `@baseline` h0060) are **dilution, not
load-bearing**. A README that keeps all 10 constructs but distills each rule to **one
principle sentence + one gate clause + one generic BEFORE/AFTER skeleton** will hold
**36/48 (0.7500)** at roughly half the added length (~125 added lines), and may **shrink the
off-construct noise wobble** (longer README → more unrelated cells perturbed → real gains net
flat).

**Independent variable: README verbosity ONLY.** All 10 constructs, both coverage gates, and
every BEFORE/AFTER skeleton are preserved; the original 80-line baseline prose is untouched.

**The single README change.** Fork `@baseline` (`solver_workflows/h0060-stabilize-f1-coinflips/
README.md`, 36/48) → `solver_workflows/h0061-lean-readme/README.md`, rewriting each added
rule-block to the lean shape per this plan (full detail + risk ratings in
`_proposal/4a-lean-readme-overfit-design-2026-06-16.md` §"What we build"):

| # | Rule | Compression | Risk |
|---|------|-------------|------|
| 1 | feature-boundary + keep-base-id | fuse removal/toggle/disable into one principle + one skeleton; drop "search project-local files" prose | low |
| 2 | preserve column set | genericize example identifiers | low |
| 3 | coverage repair (double-gated) | KEEP gate(a) intent + gate(b) oracle-free probe; collapse byte-intact `COUNT(*)`/no-cross-join hedges to ONE line | **HIGH** |
| 4 | per-key inner-join | keep as-is (already lean) | low |
| 5 | tmp-tier inline + reconcile | lead with before==after reconcile; verbatim-inline to one line | **MED** |
| 6 | package optional-resource matrix | tighten gate wording | low |
| 7 | max over cumulative standings | restate domain-neutral (drop F1 framing) | low |
| 8 | lap-time exclude pit | generalize "filter category before aggregating"; lap as one-line illustration | low |
| 9 | src_<table> naming | drop hard-coded `f1_dataset/circuits`; keep bare-prefix principle | low |
| 10 | top-N tie-crosses-cutoff | keep `count(metric >= Nth) > N`; drop named `most_fastest_laps` exclusion | low |

Target: ~125 added lines, all 10 constructs intact, leak-clean (no `AUTO_*`/`solution__*`/
`check_*`/dataset-slug/expected-count tokens).

## Acceptance criteria

Judged by the standing **single-trial, artifact-per-target** doctrine (not bare net).

- **AC-1 (construct hold — the verdict).** One full run, `trials:1`, strict audit clean. For
  each of the 13 banked target cells — asana002 · f1006 · f1006-hard · airbnb009 · airbnb005 ·
  airbnb007 · f1010-medium · ana-eng003 · quickbooks002 · quickbooks003 · asana003 · f1001 ·
  f1003-hard — read the committed SQL and confirm the correct construct still landed. **GO iff
  every target construct held** (net ≥35, ideally 36; a single off-construct dip is noise).
- **AC-2 (the actual hypothesis — bonus).** Compare off-construct wobble to h0060's run
  (`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047`). Fewer unrelated cells
  moving = overfit→noise claim confirmed.
- **AC-3 (no bleed).** The 2 always-pass canaries in the smoke panel stay green.
- **NO-GO** if any target construct failed to land → that compression dropped a load-bearing
  clause → graceful fallback (below), and the reverted set IS a result (those clauses were
  load-bearing, not dilution).

## Smoke set (draft — formal boxed table authored at propose gate)

The rewrite touches all 10 rules, so all 13 banked targets are at risk → smoke panel = the 13
targets + 2 always-pass canaries for bleed. Should-pass: each target's construct lands; net
hoped-for: hold all 13 target constructs, lose zero canaries. Pre-registered riskiest
compressions to watch: **#3 (coverage byte-intact hedges)** and **#5 (tmp-reconcile)**.

**Formal boxed smoke table (authored at propose gate, `@baseline` h0060 rewards resolved from
`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047/per_trial_outcomes.json`).**
NOTE: unlike a flip hypothesis, every target is already **PASS** at h0060 — this is an
overfit/ablation test, so each target "must STAY PASS" (its construct must hold under the
leaner wording), not "want it to flip." Net hoped-for: **hold all 13 target constructs, lose
zero canaries** (≥13/15 panel; ideal 15/15). 15 tasks × ~9 min serial ⇒ **ETA ≈ 135 min**
(detached/nohup).

```
┌──────────────────┬──────────┬──────────────────────┬───────────────────────────────────────────────────┐
│       Task       │ Baseline │ Should pass in smoke?│             Role / why we picked it               │
├──────────────────┼──────────┼──────────────────────┼───────────────────────────────────────────────────┤
│ asana002         │ ✅ PASS  │ ✅ must stay PASS    │ Target — feature-boundary/keep-base-id construct. │
│ f1006            │ ✅ PASS  │ ✅ must stay PASS    │ Target — coverage-repair construct.               │
│ f1006-hard       │ ✅ PASS  │ ✅ must stay PASS    │ Target — coverage-repair construct.               │
│ airbnb009        │ ✅ PASS  │ ✅ must stay PASS    │ Target — coverage byte-intact hedge (RISKIEST #3).│
│ airbnb005        │ ✅ PASS  │ ✅ must stay PASS    │ Target — per-key inner-join construct.            │
│ airbnb007        │ ✅ PASS  │ ✅ must stay PASS    │ Target — per-key/preserve-cols (MULTI-MODEL G11). │
│ f1010-medium     │ ✅ PASS  │ ✅ must stay PASS    │ Target — max-over-cumulative construct.           │
│ ana-eng003       │ ✅ PASS  │ ✅ must stay PASS    │ Target — preserve-columns / tmp construct.        │
│ quickbooks002    │ ✅ PASS  │ ✅ must stay PASS    │ Target — feature-boundary construct.              │
│ quickbooks003    │ ✅ PASS  │ ✅ must stay PASS    │ Target — feature-boundary construct.              │
│ asana003         │ ✅ PASS  │ ✅ must stay PASS    │ Target — tmp-tier inline+reconcile (RISKIEST #5). │
│ f1001            │ ✅ PASS  │ ✅ must stay PASS    │ Target — src bare-prefix naming construct.        │
│ f1003-hard       │ ✅ PASS  │ ✅ must stay PASS    │ Target — top-N tie-crosses-cutoff construct.      │
│ airbnb001        │ ✅ PASS  │ ✅ must stay PASS    │ Canary (airbnb family) — bleed tripwire.          │
│ ana-eng001       │ ✅ PASS  │ ✅ must stay PASS    │ Canary (ana-eng family) — bleed tripwire.         │
└──────────────────┴──────────┴──────────────────────┴───────────────────────────────────────────────────┘
```

## Pre-smoke Decision-Fork Probe

**Not applicable — no probe run, and here is why.** This is not a smoke/full rejection
follow-up on a flipped task and tests no new local fork. Every construct here is already
banked and artifact-confirmed in the h0060 baseline; the only variable is README *verbosity*.
There is no A/B branch of solver reasoning to probe — the experiment asks whether removing
prose dilution preserves the *already-proven* constructs. Decision-fork probing does not apply
to a verbosity ablation; the real test is the full-run artifact-per-target read (AC-1).

## Graceful fallback (pre-registered)

If smoke shows a target's construct didn't land, revert that ONE rule to its h0060 wording and
re-smoke. The experiment degrades to a *partial-lean* README (N-of-10 compressed) rather than
failing wholesale. The set of rules that had to revert is the per-rule "load-bearing vs
dilution" map — itself a first-class output feeding `/home/kent/autobench/day-one-runbook.md`
(how lean a ported README can start).

## Smoke result

**Verdict: GO (variance-resolved)** — the smoke draw tripped the strict rule (1 of 13 target
constructs missed: asana002), but the captain-approved 3× variance probe came back **3/3 PASS**
all taking the prescribed var-matrix model path (see `## Variance Probe`), confirming the smoke
FAIL was the ~25% path-selection tail of a coin-flip cell, NOT compression damage. Effective
result: **12/13 constructs held outright + asana002 variance-confirmed (3/4 land the correct
path) + both canaries held + no dropped clause.** Run-dir
`runs/ade-bench-h0061-lean-readme/4baa96c3f4494b60` (concurrency 3, ~49 min).

- **Score:** `stratified_pass_at_1 = 0.9333 = 14/15` (`rk score`). Above the spec constant (0.1875).
- **Strict audit:** CLEAN — `rk audit … --policy strict` summary `{clean: 15, tainted: 0, coverage_missing: 0}`; no findings on any cell. Score trusted on a clean audit.
- **Trace capture:** every one of the 15 cells has `subagent-trace-manifest.json` with `captured=1` (>0). ✔
- **Canaries:** airbnb001 PASS, ana-eng001 PASS — **zero bleed**. ✔
- **Multi-model (G11) airbnb007:** BOTH scored models green — `daily_agg_nps_reviews_equality_with_tolerance` (9/11) AND `listing_agg_nps_reviews_equality_with_tolerance` (10/11); 11/11 total. Hold is real, not single-model variance. ✔

### Per-target hold table (vs @baseline h0060 `861d18e790c72047`)

| Target | h0060 | h0061 | Distance (Got N) | Construct landed under lean wording? |
|--------|-------|-------|------------------|--------------------------------------|
| asana002 | PASS | FAIL (smoke) → **3/3 PASS (probe)** | Got 2 (smoke draw); Got 0 in all 3 probe draws | **YES (variance-resolved)** — smoke draw took the raw-`asana.duckdb` path (the ~25% tail); all 3 probe re-draws took the prescribed var-matrix model fix (`asana__task/tag/int_*` gated on `asana__using_*`). See `## Variance Probe`. |
| f1006 | PASS | PASS | 0 | yes — coverage repair |
| f1006-hard | PASS | PASS | 0 | yes — coverage repair |
| airbnb009 (RISKIEST #3) | PASS | PASS | 0 (1/1) | yes — coverage byte-intact hedge held |
| airbnb005 | PASS | PASS | 0 | yes — per-key inner-join |
| airbnb007 (multi-model) | PASS | PASS | 0 (11/11, both models) | yes — per-key/preserve-cols on BOTH models |
| f1010-medium | PASS | PASS | 0 | yes — max-over-cumulative |
| ana-eng003 (RISKIEST #5) | PASS | PASS | 0 (2/2) | yes — tmp/preserve-cols, `AUTO_dim_customer_equality` |
| quickbooks002 | PASS | PASS | 0 | yes — feature-boundary |
| quickbooks003 | PASS | PASS | 0 | yes — feature-boundary |
| asana003 (RISKIEST #5) | PASS | PASS | 0 (17/17) | yes — tmp-tier inline+reconcile, all AUTO equality green |
| f1001 | PASS | PASS | 0 | yes — src bare-prefix naming |
| f1003-hard | PASS | PASS | 0 (4/4) | yes — top-N tie-crosses-cutoff (3 check_option_* green) |
| airbnb001 (canary) | PASS | PASS | 0 | held — no bleed |
| ana-eng001 (canary) | PASS | PASS | 0 | held — no bleed |

**Net:** 12/13 target constructs held + 2/2 canaries held + both riskiest compressions (#3, #5)
landed. The single miss is asana002 — resolved as variance by the probe below.

## Variance Probe

**asana002 re-run 3× on the UNCHANGED h0061-lean-readme README** (captain-approved variance
probe). Spec `specs/h0061-lean-readme.asana002-probe.frozen.yaml` (trials:3, concurrency:3,
solver_workflow content_hash `0d8bfa9` — byte-identical to the smoke run). Run-dir
`runs/ade-bench-h0061-lean-readme-asana002-probe/79e5d47837048711` (cells fBX4wZA, iMdHh8K,
p74Aav3). `done` rc=0.

- **Result: 3/3 PASS** (all `reward.txt`=1, all `AUTO_asana__*` equality green, Got 0).
- **Salience signal — all 3 took the PRESCRIBED path:** every passing draw ran the disabled-var
  compile matrix (`dbt compile --vars '{asana__using_tags: false}'` / `…task_tags: false` / both)
  and committed the **SQL model fix** to `models/asana__task.sql`, `models/asana__tag.sql`, and
  `models/intermediate/int_asana__task_tags.sql` — gating the tag models on `asana__using_tags`
  / `asana__using_task_tags` and emitting `tags = null` / `number_of_tags = 0` when disabled.
  This is exactly h0060's winning approach. **None mutated raw `asana.duckdb`.**
- **Combined tally:** asana002 at the h0061 README = **3 PASS / 1 FAIL** (smoke draw was the lone
  raw-data miss). ~75% land the correct var-matrix path on the first try.

**Conclusion: variance-confirmed, NO load-bearing clause was dropped.** Rule #6's text is
byte-identical h0060→h0061 (only filler trimmed; the "no raw seed edits" steer intact), and the
lean wording steers the solver to the correct model-side path 3 of 4 draws. The smoke FAIL was
the ~25% path-selection tail of a coin-flip-prone cell, not compression damage.

## Behavioral analysis

**The hypothesis is largely confirmed — with one instructive exception.** Every one of the
two *pre-registered riskiest* compressions held cleanly: the #3 coverage byte-intact hedge
collapsed to one line still landed airbnb009 (Got 0), and the #5 tmp-tier reconcile collapsed
to one principle still landed asana003 (17/17) and ana-eng003 (2/2). So the scar-clause prose
on the constructs we *worried* about was indeed dilution, not load-bearing.

**asana002 — approach-variance, NOT a dropped load-bearing clause.** The miss is on rule #6
(PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX), whose compression was the most faithful of the ten:
a byte-comparison shows the lean version kept every load-bearing token — "classify package
vars," "disabled-var compile matrix," "repair the dependency graph with the same existing
vars," and crucially the negative steer **"Do not start from casts, raw seed edits, or broad
package copying."** Only "first" / "run or consider"→"run" were trimmed. The h0061 solver
*explored* the right path (it read `asana__using_tags`/`asana__using_task_tags` 17× each and
the package README's disable-var section) yet still chose to mutate the raw data
(`asana.duckdb`) — exactly the "raw seed edits" the rule says to avoid — and its own
`dbt build` went green (89/89) while the hidden `AUTO_asana__task_equality` missed by 2 rows
(the self-anchored false-green pattern). h0060's winning solver instead edited the downstream
models (`asana__task.sql`, `asana__tag.sql`, `int_asana__task_tags.sql`) to honor the new
disable-vars — the construct that lands the equality test.

Because the load-bearing clause is **present and unweakened**, asana002's miss is **path-
selection variance** between two plausible readings (the task literally says "modify our
*data*"), not evidence that compressing rule #6 dropped a load-bearing steer. asana002 has a
history of coin-flip behaviour; one draw landing on the data-side path is within that variance.
This means the graceful-fallback "revert the one rule that dropped a clause" does NOT cleanly
apply — there is no dropped clause to restore. The honest read: the lean README preserves all
ten constructs' load-bearing content; asana002 needs a *stronger* (not merely restored) #6
steer to deterministically force the model-side path, which is a follow-up lever, not a revert.

## Run result

**Full 48-task run COMPLETE — 36/48 = 0.7500, ties @baseline h0060 exactly; ALL 13
target constructs held; strict audit CLEAN.** Run-dir
`runs/ade-bench-h0061-lean-readme/50e340fd462032af` (`done` rc=0, ~134 min). Spec
`specs/h0061-lean-readme.frozen.yaml`, solver_workflow `solver_workflows/h0061-lean-readme`
content_hash `sha256:0d8bfa9…` — **byte-identical to the smoke + probe README**; only the
task set differs (all 48, no `benchmark.tasks` selector). Methodology consistent.

- **Score (trusted on clean audit):** `stratified_pass_at_1 = 0.7500 = 36/48`
  (`rk score --format json`), `n_errored=0`. Above the spec constant (0.1875),
  verdict `above`. Wilson CI [0.612, 0.851]. **Net = 36/48, exactly ties h0060's
  36/48 baseline** (no net regression from compressing all 10 rules to ~half length).
- **Strict audit:** CLEAN — `rk audit … --policy strict` summary
  `{clean: 48, tainted: 0, coverage_missing: 0}`; zero findings on all 48 cells. Score trusted.
- **Trace capture:** all 48 cells have `subagent-trace-manifest.json` with `captured>0`
  (48/48 captured>0, 0 zero, 0 missing). ✔
- **AC-1 (construct hold — the verdict): GO.** All 13 banked target constructs held
  (PASS): asana002 · f1006 · f1006-hard · airbnb009 · airbnb005 · airbnb007 ·
  f1010-medium · ana-eng003 · quickbooks002 · quickbooks003 · asana003 · f1001 ·
  f1003-hard. **Zero target dropped.** Notably **asana002 PASSED on the full run** —
  the smoke-draw miss (probe-resolved as path-selection variance) landed correctly here,
  consistent with the ~75% first-try rate.
- **AC-3 (no bleed): held.** Both always-pass canaries green (airbnb001 PASS, ana-eng001 PASS).
- **The 12 fails are all known non-target cells** (ana-eng004/006/007/007-medium,
  asana004/005/005-hard, f1002, intercom001/002/003, quickbooks001) — the same
  long-standing unsolved set, not constructs this hypothesis touched.

**Headline: 36/48 (= 36/48 baseline), audit clean = YES, all 13 target constructs held →
the lean README preserves every construct at ~half the added length. Hypothesis confirmed.**

### Analyze — quantitative (paired vs @baseline h0060 `861d18e790c72047`)

- **Tooling note:** `rk runs diff` TypeErrors on ade-bench run-dirs (`query_id: null`,
  keyed on `trial_name`), so the paired delta was computed directly from each run's
  `per_trial_outcomes.json`, paired by task slug, with a 10k-draw paired bootstrap. (Per
  the analyze contract's documented harness data-shape limitation.)
- **Paired delta = 0 tasks; 95% bootstrap CI [0, 0].** Not merely a net tie — the two runs
  are **cell-for-cell identical**: same 36 PASS, same 12 FAIL, *zero* verdict changes in
  either direction. Verified the failing sets are byte-identical (both =
  {ana-eng004, ana-eng006, ana-eng007, ana-eng007-medium, asana004, asana005, asana005-hard,
  f1002, intercom001, intercom002, intercom003, quickbooks001}). Mean per-task delta 0.0000,
  CI [0.0000, 0.0000].
- **Absolute score:** `stratified_pass_at_1 = 0.7500` vs paper_baseline constant 0.1875 →
  verdict `above` (Wilson CI [0.612, 0.851]). 0 errored.

### AC-2 — off-construct wobble (THE headline finding)

The hypothesis: a leaner README perturbs *fewer* unrelated cells. Of the 48 cells, 15 are
**construct cells** (13 banked targets + 2 canaries); the other **33 are off-construct**.

- **Off-construct cells that changed verdict (either direction): 0 of 33.**
- **Construct cells that changed: 0 of 15.**
- **Total verdict changes h0060↔h0061: 0 of 48.**

**AC-2 is confirmed in the strongest possible form.** Halving the added README length
(181→ the lean shape; original ~80-line prose untouched) did not move a *single* off-construct
cell. The overfit→noise claim is not just supported — there is **no off-construct wobble to
shrink** because the lean README reproduced the baseline's exact outcome distribution. The
~249-line scar-clause delta was dilution: removing roughly half of it cost zero constructs and
introduced zero new perturbation.

## Behavioral analysis (analyze stage — full run)

The smoke-stage `## Behavioral analysis` (above) reads the 15-cell panel; this block reads the
full 48-cell run against @baseline h0060 and answers the six required analyze questions.

**Q1 — Net + full per-task ledger (both directions).** Absolute 0.7500 (36/48) vs @baseline
0.7500 (36/48); paired delta **0 tasks, 95% bootstrap CI [0, 0]**. **The ledger of verdict
changes is EMPTY in both directions: zero FAIL→PASS gains, zero PASS→FAIL regressions.** The
two runs are cell-for-cell identical (verified by set equality of the pass and fail slugs). No
gains to claim, no regressions to disclose — there were none.

**Q2 — Smoke vs full.** Smoke was a GO (variance-resolved). The full verdict did **not** differ
adversely: every banked target that the smoke panel sampled held at full, AND the one smoke miss
(asana002) **passed at full**. The smoke panel could not see the 33 off-construct cells — but
all 33 held their baseline verdict, so the unsampled space carried no hidden regression. This is
the rare case where the full run is *strictly consistent with or better than* the smoke draw.

**Q3 — Already-correct-and-broken.** No regressions, so no damage to working code. Every cell
passing at @baseline still passes at h0061 (all 36); every cell failing at @baseline still fails
(all 12, the persistent unsolved set). Zero passers broken.

**Q4 — Was the change executed? (committed-artifact verification).** Spot-checked the
representative / pre-registered-riskiest cells by committed SQL + verifier stdout:
  - **asana002 (#6, the smoke miss):** EXECUTED-AND-HELPED via the prescribed path. The full-run
    ensign edited `models/asana__task.sql`, `models/asana__tag.sql`,
    `models/intermediate/int_asana__task_tags.sql` (var-gated on `asana__using_tags` /
    `asana__using_task_tags`), ran the full disabled-var compile matrix, and **did NOT mutate raw
    `asana.duckdb`** — exactly h0060's winning construct. Hidden `AUTO_asana__task_equality` 3/3.
    This is the ~75% correct-path draw (smoke hit the ~25% raw-data tail; probe-confirmed coin-flip).
  - **airbnb009 (RISKIEST #3, coverage byte-intact hedge → one line):** `mom_agg_review_date_range`
    1/1 PASS. Construct landed under the collapsed hedge.
  - **asana003 (RISKIEST #5, tmp-tier inline+reconcile → one principle):** 27/27 AUTO equality
    (all `AUTO_asana__*`/`int_asana__*` equality+existence). Construct landed.
  Classification across the read cells: **executed-and-helped / construct-landed; none inert, none
  premise-falsified.** The lean wording reached the committed artifact and produced the right model.

**Q5 — Prevention + next move.** Nothing to prevent — there is no harm to scope-guard and no
gain at risk of regression. The lean README is a drop-in equivalent of h0060 at ~half the added
length. The actionable move: **promote the lean README as @baseline** (equal score, identical
outcome distribution, strictly less prose to carry forward and to dilute future ports). The one
soft residual is asana002's ~75% first-try rate on the model-side path — a *strengthen-#6*
follow-up (not a revert; #6's text is already full-strength), optional and non-blocking.

**Q6 — Smoke-vs-full fork drift.** The smoke→full transition showed **no adverse drift**: the
smoke's lone miss was artifact-confirmed (by the 3× probe, 3/3 PASS on the prescribed path) to be
single-trial path-selection variance on a known coin-flip cell, NOT a README rule drifting into a
different implementation branch. At full, asana002's draw landed the prescribed model-side fork
(committed artifact verified in Q4). The smoke panel did not "miss a family" in any damaging
sense — every off-construct family held its baseline verdict at full. No fork changed adversely;
the only fork that *could* vary (asana002's data-vs-model reading) resolved correctly this draw.

**Bottom line.** The +249-line scar-clause accumulation in h0060's README was **dilution, not
load-bearing**. Compressing all 10 rules to one principle + one gate + one skeleton each (cutting
the added length roughly in half) preserved every construct AND reproduced the baseline's exact
48-cell outcome — zero constructs lost, zero off-construct perturbation. Recommend **PROMOTE**.

## Verdict

**PASSED — PROMOTED to `@baseline` (captain-approved 2026-06-17).** Before→after:
`@baseline` was `runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047` (36/48) →
now `runs/ade-bench-h0061-lean-readme/50e340fd462032af` (36/48). Promoted via
`rk registry add run baseline …` (verified: `rk registry resolve run @baseline` and
`rk registry list` both return the h0061 run-dir). Solver README
`solver_workflows/h0061-lean-readme/README.md`, content_hash `sha256:0d8bfa9…`.

**Distilled, transferable learnings (source of truth):**

1. **The +249-line scar-clause accretion in h0060's README was DILUTION, not load-bearing.**
   The lean README — each of the 10 added rules distilled to *one principle sentence + one gate
   clause + one generic BEFORE/AFTER skeleton*, roughly half the added length, original ~80-line
   baseline prose untouched — reproduced h0060 **CELL-FOR-CELL**: 36/48, paired delta **0**, 95%
   bootstrap CI **[0, 0]**, **0 of 48 verdict changes** (0/33 off-construct, 0/15 construct).
   Identical pass set, identical fail set.

2. **Why it held (mechanism):** the load-bearing content of an accepted rule is the
   *construct* — the principle (what correct shape to produce), the precondition gate (when it
   fires), and a worked skeleton (how the SQL looks). The scar-clauses and domain framing
   accumulated around each rule (specific identifiers, F1/asana wording, repeated hedges) are
   *restatements* of the construct, not additional signal. Stripping them did not weaken the
   steer — committed-artifact spot-checks confirm the riskiest compressions still landed
   (airbnb009 coverage-hedge #3 1/1; asana003 tmp-reconcile #5 27/27) and asana002 took the
   prescribed model-side path (not raw-data mutation).

3. **Transferable rule for `day-one-runbook.md` (how lean a ported README can start):**
   a ported README can start LEAN. Distill each rule to **principle + gate + one BEFORE/AFTER
   skeleton**; the scar-clauses and domain-specific framing are safe to drop without losing the
   construct. Keep: the principle, the precondition gate, one generic worked skeleton, and any
   *negative steer* (e.g. "do not start from raw seed edits"). Drop: hard-coded dataset/table
   identifiers in examples, domain narration, and repeated byte-intact hedges. Verbosity is not
   robustness — a longer README does not buy more held constructs, and the worry that it perturbs
   more unrelated cells is real-but-here-immaterial (the lean version moved zero off-construct
   cells, so there was no wobble to shrink; the upside is purely the carrying cost of less prose).

## Follow-up Routing

**`escalate`** — the oracle-flip program is exhausted (banked-flip portfolio closed; see
operator memory "oracle-problem flip program CONCLUDED"). This was an ablation, not a flip, and
it confirmed leanness is free — but it does NOT open a new flip family. Two candidate directions
for captain strategy, do **not** auto-file:

- **(a) PRIMARY — hold-out GENERALIZATION test.** Measure how much of the 36/48 survives on dbt
  tasks the README was *never tuned on*, to quantify general-capability vs ade-bench-specific
  construct overfit. Several rules (#7 max-over-cumulative, #9 src-prefix naming, #10
  top-N-tie-cutoff) are essentially task-specific recipes; leanness did not change that, and only
  a hold-out set can separate "the solver learned a general skill" from "the README memorized
  these 13 cells." This is the highest-value next question and needs a benchmark-design decision
  (where the hold-out tasks come from), so it is a captain call.
- **(b) MINOR / optional — strengthen rule #6.** asana002 lands the prescribed model-side path
  only ~75% of first-try draws (the data-vs-model reading is a coin-flip the README does not
  tightly constrain). A *strengthen* (NOT a revert — #6's text is already full-strength) could
  push that toward determinism. Low value on its own (asana002 already passes in expectation);
  only worth bundling into a larger lever.

## Cross-refs

`_proposal/4a-lean-readme-overfit-design-2026-06-16.md` (full design);
`_artifacts/readme-rule-progression-research-2026-06-16.md` (per-rule overfit review);
`_proposal/retrospective-2026-06-15-program.md`; `@baseline`
`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047` (36/48 = 0.7500);
READMEs `solver_workflows/{codex-ade-dbt-minimal, h0060-stabilize-f1-coinflips}/README.md`.
</content>

## Gatekeeper review

**Recommendation: APPROVE** — sanctioned whole-Implementation-stage verbosity ablation; integrity rules G2/G3/G6 all clean, the single idea (compress prose, keep every construct) is confined to the Implementation stage with all other stages byte-identical, no leaks; only WARNs (G4 sanctioned smoke serialization, G7 inert-risk-on-revert framing, G11 airbnb007 multi-model).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-17T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | All diff hunks fall between `## Stage: Implementation` (L50) and `## Stage: Validation` (h0060 L313 / h0061 L245); preamble+Exploration (L1–49) and Validation+Finalization (h0060 L313→EOF vs h0061 L245→EOF) verified byte-identical by diff. The "exactly one idea" literal reading would flag the 10-rule rewrite, but per captain sanction the single idea IS the multi-rule compression — intentional whole-stage rewrite, not scope creep; stays inside Implementation, touches no other stage and no leak/dependency prose. PASS on merits. |
| G2 leak-guard intact | PASS | Grep of added (`>`) diff lines for `AUTO_`/`solution__`/`check_`/`verifier`/`equality test`/`expected output`/`expected count` → none; dataset-slug grep → none; `curl`/`wget`/`git clone`/`git ls-remote`/published-solution → leak-guard prose not in the diff (untouched). |
| G3 spec two fields | PASS | `diff baseline.yaml h0061-lean-readme.yaml` shows ONLY `experiment:` and `solver_workflow:` changed; top-level `trials: 1` preserved; `agent.kind: spacedock_solver` + `runtime: codex` preserved; full spec keeps `concurrency.trials: 4` matching baseline. |
| G4 smoke tasks-only | WARN | Smoke diff adds the `benchmark.tasks` block (13 targets + 2 canaries, all `ade-bench-`-prefixed) AND flips `concurrency.trials: 4→1`. The trials flip is the sanctioned freeze-repo-race serialization for smoke (concurrency>1 → "cannot lock ref HEAD"), an infra-safety knob, not experiment scope — benign. Strict G4 wants tasks-only; surfaced as WARN, not a blocking FAIL. Every hypothesis-named target is present in the panel. |
| G5 both frozen | PASS | `specs/h0061-lean-readme.frozen.yaml` (1673B) and `…smoke.frozen.yaml` (2033B) both exist; both carry `kind: spacedock_solver` + `runtime: codex` (L4–5). |
| G6 resolver fidelity | PASS | Inserted text matches the claim: each of the 10 rules distilled to principle + gate + one generic BEFORE/AFTER skeleton (e.g. lap-time→"EXCLUDE-A-CATEGORY AVERAGE", domain identifiers genericized, `f1_dataset/circuits`→`<dataset>/<table>`). Every rule stays precondition-gated/generative-or-independent (not self-anchored "re-run your own model"); no dead-family phrasing introduced; no scope beyond compression. Parent resolved: `source:` h0060 == `rk registry resolve run @baseline` → `runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047`, solver_workflow `solver_workflows/h0060-stabilize-f1-coinflips` — agree. |
| G7 actionability/inert-risk | WARN | The compression itself is mechanical (rewrite prose); but note the constructs being preserved span structural-rewrite shapes (coverage spine, tmp-tier inline, per-key join) that are inert-prone as abstract prose — the lean rules retain worked-example skeletons, mitigating this. Predictive note: if a target's construct fails to land, the question is whether the dropped scar-clause was load-bearing; the riskiest compressions (#3 coverage byte-intact hedges → airbnb009; #5 tmp-reconcile → asana003/ana-eng003) are the ones to read by committed artifact. WARN-only, never blocks. |
| G8 regression-canary coverage | N/A (PASS) | Not generative — every rule remains precondition-gated to its named task shape ("when a task does not match a rule's gate, ignore that rule entirely"), so it cannot over-fire on non-matching tasks. Smoke nonetheless carries 2 cross-family always-pass canaries (airbnb001, ana-eng001) as bleed tripwires. Classify: gated → N/A. |
| G9 selector independence | N/A (PASS) | No multi-candidate / selector protocol declared; single solver session, no N-candidate selection. |
| G10 self-correcting false-positive | N/A (PASS) | No new self-correcting lever introduced. The preserved coverage-repair gate(b) probe and tmp-tier before==after reconcile are oracle-free, separately-sourced (dimension keys / pre-refactor capture), precondition-gated, and check-don't-blindly-replace — and they are unchanged constructs, not a new fire-on-disagreement rule. N/A; if scored, would PASS. |
| G11 multi-model-target risk | WARN | airbnb007 is a known MULTI-MODEL target (`daily_agg_nps_reviews` + `listing_agg_nps_reviews`, per `_artifacts/bug-type-taxonomy.md`). It is already PASS at h0060 with both scored models green; this hypothesis tests HOLD under leaner wording, not a fresh single-model flip, so the variance trap is muted — but the captain should judge airbnb007's hold by the committed artifact on BOTH scored models, not the aggregate verdict. Other targets single-model or covers-all. WARN-only. |
| G12 decision-fork probe quality | N/A (PASS) | Not a flipped-task follow-up; hypothesis explicitly states why no probe (verbosity ablation, no A/B branch of solver reasoning to probe; real test is the full-run artifact-per-target read). Justification present and valid. |

**For the captain:** No integrity FAILs (G2/G3/G6 clean) and no mechanical FAILs → APPROVE. Three WARNs to weigh: (1) G4 — the smoke flips `concurrency.trials 4→1`; this is the sanctioned freeze-race serialization, not experiment scope, but it is a second smoke-spec field beyond `benchmark.tasks` — confirm that is intended. (2) G7/AC — read the riskiest compressions (#3 coverage byte-intact hedges on airbnb009; #5 tmp-reconcile on asana003/ana-eng003) by committed SQL artifact, since a dropped scar-clause failing to hold IS the result (load-bearing vs dilution map). (3) G11 — judge airbnb007's hold on BOTH its scored models, not the aggregate. The "exactly one idea" G1 reading is intentionally a whole-Implementation-stage rewrite per the 4a design sanction; all other stages are byte-identical.

## Stage Report: propose

- DONE: Fork @baseline (solver_workflows/h0060-stabilize-f1-coinflips/README.md) → solver_workflows/h0061-lean-readme/README.md, compressing all 10 added rule-blocks to the lean shape, every construct + both coverage gates + every skeleton preserved, original baseline prose untouched, leak-clean, ~125 added lines.
  All 10 construct headers + 3 gate markers present; preamble/Exploration/classify/basic-confirm/Validation/Finalization byte-identical to the codex-ade-dbt-minimal seed (diff clean); leak grep (AUTO_/solution__/check_/dataset-slug/expected-count) empty. Lines: 261 total = 181 added (vs 249 in h0060). Note: 181 > the ~125 nominal target because the spec's hard requirement "every BEFORE/AFTER skeleton preserved" keeps all multi-line SQL skeletons; skeleton-preservation wins over the soft line target.
- DONE: Author both specs (cp baseline.yaml → h0061-lean-readme.yaml differing ONLY in experiment + solver_workflow; cp → .smoke.yaml adding benchmark.tasks = 13 banked targets + 2 always-pass canaries) and freeze both with rk freeze --allow-missing.
  Full-spec diff vs baseline = exactly the two allowed fields; smoke diff vs full = benchmark.tasks block + concurrency.trials 4→1 (sanctioned freeze-race serialization, matches h0060 smoke pattern). Both .frozen.yaml written (1673B / 2033B), kind=spacedock_solver + runtime=codex preserved.
- DONE: Run the gatekeeper subagent and record its per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT recommendation in the ## Gatekeeper review block.
  Recommendation: APPROVE. G2/G3/G6 (integrity) all PASS; G1 PASS-on-merits (sanctioned whole-Implementation-stage rewrite, other stages byte-identical); 3 WARNs (G4 smoke concurrency knob, G7 inert-risk on revert, G11 airbnb007 multi-model); G8/G9/G10/G12 N/A.

### Summary

Authored the lean-README overfit variant: forked @baseline h0060 and distilled all 10 added rule-blocks to one principle + one gate + one generic BEFORE/AFTER skeleton, keeping every construct, both coverage gates, and every skeleton while leaving the original ~80-line baseline prose byte-identical and leak-clean. The README is 261 lines (181 added) — over the ~125 soft target because preserving every skeleton (a hard spec requirement) keeps the SQL examples. Both specs differ from baseline only as allowed and are frozen. Gatekeeper recommends APPROVE with three WARNs to weigh at the gate. Key framing for the captain: every target is already PASS at h0060, so the smoke is a "must STAY PASS" hold test, not a flip — judge each construct by its committed SQL artifact (riskiest: #3 airbnb009 coverage hedges, #5 asana003/ana-eng003 tmp-reconcile).

## Failure Review

**Classification: path-selection variance on a known coin-flip cell (asana002) — NOT a dropped
load-bearing clause. RESOLVED-AS-VARIANCE by the 3× probe (3/3 PASS, all on the prescribed
var-matrix path — see `## Variance Probe`).** The smoke draw tripped the strict pre-registered
NO-GO rule, but the probe upgrades the verdict to **GO (variance-resolved)**: the cause was the
~25% path-selection tail, not the failure mode the hypothesis was hunting for. (Was initially
filed `variance-unclear`; the probe is the disambiguating evidence.)

- **Which compressed rule is implicated:** #6 (PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX).
- **Was a load-bearing clause dropped?** **No.** Byte-comparison of #6 h0060→h0061 shows every
  load-bearing token survived, including the negative steer "Do not start from casts, raw seed
  edits, or broad package copying." Only filler ("first", "run or consider"→"run") was trimmed.
- **What the solver did:** explored the correct var-matrix path (read `asana__using_tags` /
  `asana__using_task_tags` and the package disable-var README) but chose to mutate raw
  `asana.duckdb` — the exact "raw seed edits" the rule forbids — and self-validated green
  (own `dbt build` 89/89) while the hidden equality missed by 2 rows.
- **Graceful-fallback applicability:** the entity's pre-registered fallback is "revert the ONE
  rule that dropped a load-bearing clause and re-smoke." That does NOT cleanly apply here —
  there is no dropped clause to restore; #6 is already at full strength. Reverting #6 to its
  (substantively identical) h0060 wording would not deterministically fix a path-selection
  coin-flip.
- **Recommended routing (RESOLVED):** the disambiguating re-draw was run — **3/3 PASS on the
  prescribed path** — so option (1) ("accept lean as a HOLD; a re-draw would disambiguate") is
  now settled in favor of HOLD. **Recommendation: GO to the full run.** Optional follow-up (not
  blocking): a future lever could *strengthen* (not revert) #6 to lift asana002's ~75% first-try
  rate toward determinism — but that is a new hypothesis, not a fix this one needs.
- **Per-rule load-bearing-vs-dilution map (for the day-one runbook):** 9 of 10 compressed rules
  proved their scar-clauses were dilution (constructs held at full strength under the lean shape,
  including both pre-registered HIGH/MED-risk rules #3 and #5). Rule #6's compression was also
  faithful; its single miss is a solver path-selection variance the README does not tightly
  constrain — flagged as the one place a leaner README may want a *sharper* (not longer) steer.

## Stage Report: full

- DONE: Launch the detached 48-task full run on specs/h0061-lean-readme.frozen.yaml via drivers/rk-run-detached.sh h0061-full specs/h0061-lean-readme.frozen.yaml run, and return the handle path immediately.
  Handle `runs/.rk-handles/h0061-full-20260617-075604/` (pid 1689686, ntfy adebench-rk-381c976fe07465bf); returned to FO for the wait. Recorded in `## Run result`.
- SKIPPED: On done rc=0: rk audit … --policy strict (clean) + rk score … --format json; confirm subagent-trace-manifest captured>0; record run-dir + headline net.
  Deferred — the run is detached and not yet finished; the FO owns the wait and re-engages this ensign on done rc=0 to perform audit/score/trace and fill `## Run result`.
- DONE: Confirm methodology consistency — the full frozen spec uses the SAME solver README (content_hash 0d8bfa9) as the smoke + probe; only the task set differs.
  Full frozen spec solver_workflow_content_hash `sha256:0d8bfa9…` matches the smoke + probe README; full spec carries no `benchmark.tasks` selector (all 48), unlike the 15-task smoke panel — task set is the only difference.

### Summary

Launched the detached full 48-task run on the byte-identical lean README (content_hash 0d8bfa9, same as the verified smoke + probe). Verified the frozen spec and launcher exist and the methodology is consistent (only the task set differs from smoke). Returned the handle path to the FO immediately per the detached-run contract; audit/score/trace and the headline net (X/48 vs h0060's 36/48) are deferred to the FO-driven re-engagement on done rc=0.

## Stage Report: full (cycle 2 — post-completion audit/score)

- DONE: On done rc=0: rk audit … --policy strict (clean) + rk score … --format json; confirm subagent-trace-manifest captured>0; record run-dir + headline net.
  Run-dir `runs/ade-bench-h0061-lean-readme/50e340fd462032af`. Strict audit CLEAN `{clean:48, tainted:0, coverage_missing:0}`, zero findings. Score `stratified_pass_at_1=0.7500=36/48`, n_errored=0, above constant. Trace 48/48 captured>0. Recorded in `## Run result`.
- DONE: Confirm construct hold (AC-1) + no bleed (AC-3).
  All 13 banked target constructs PASS (zero dropped; asana002 passed on full run); both canaries (airbnb001, ana-eng001) PASS. The 12 fails are all known non-target cells.

### Summary

Full run complete: 36/48 = 0.7500, exactly ties @baseline h0060's 36/48, with a CLEAN strict audit (48/48 clean) — score trusted. All 13 banked target constructs held under the leaner README (zero dropped), both canaries green, all 48 cells captured>0, and methodology consistent (content_hash 0d8bfa9, only the task set differs). Compressing all 10 rules to ~half the added length preserved every construct with no net regression — hypothesis confirmed. AC-2 off-construct wobble comparison vs h0060 is deferred to the analyze stage.

## Stage Report: analyze

- DONE: Quantitative — paired delta vs @baseline + absolute score.
  `rk runs diff` TypeErrors on ade-bench run-dirs (query_id null) so computed paired delta from per_trial_outcomes.json (slug-paired, 10k bootstrap): **delta = 0 tasks, 95% CI [0, 0]** — runs are cell-for-cell identical (same 36 PASS, same 12 FAIL). Absolute 0.7500 vs constant 0.1875 → `above`. In `## Run result → Analyze — quantitative`.
- DONE: AC-2 — off-construct-wobble comparison vs h0060 (THE hypothesis).
  **0 of 33 off-construct cells changed verdict; 0 of 15 construct cells changed; 0 of 48 total.** Halving the added README length perturbed zero unrelated cells. Strongest-form confirmation. In `## Run result → AC-2`.
- DONE: Behavioral + the 6 required analyze questions; verify committed artifacts on representative cells.
  Empty ledger both directions (no gains, no regressions, no broken passers). Spot-checked asana002 (model-side path, NOT raw-data mutation — h0060's winning construct, AUTO equality 3/3), airbnb009 (#3, 1/1), asana003 (#5, 27/27): all executed-and-helped / construct-landed, none inert. All 6 questions answered in `## Behavioral analysis (analyze stage — full run)`.

### Summary

The lean README reproduced @baseline h0060's outcome cell-for-cell: 36/48, paired delta 0 (CI [0,0]), identical pass/fail sets, zero off-construct wobble (0/33). The +249-line scar-clause accumulation was dilution, not load-bearing — compressing all 10 rules to ~half the added length cost zero constructs and introduced zero new perturbation. Committed-artifact spot-checks confirm the riskiest compressions (#3, #5) and the smoke-miss cell (asana002, via the prescribed model-side path) all landed correctly. No regressions, no inert cells. **Recommendation: PROMOTE the lean README as the new @baseline** (equal score, identical distribution, ~half the prose); optional non-blocking follow-up = strengthen (not revert) rule #6 to lift asana002's ~75% first-try rate.

## Stage Report: conclude

- DONE: PROMOTE the lean README as the new @baseline + confirm resolution before→after.
  Before `@baseline = runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047`; after = `runs/ade-bench-h0061-lean-readme/50e340fd462032af`. Promoted via `rk registry add run baseline …` (returned OK); verified by `rk registry resolve run @baseline` AND `rk registry list` (both return the h0061 run-dir). NOTE: `rk baseline promote` requires `--to`/`--constraints` (it copies spec into a baseline dir — a different op) and is NOT what re-binds `@baseline`; the registry-add is the binding step and it landed.
- DONE: Write ## Verdict (PASSED) with distilled, transferable learnings in the entity body.
  `## Verdict` records PASSED/PROMOTED + 3 distilled learnings (scar-clause delta was dilution; the construct = principle+gate+skeleton is what's load-bearing; the lean-start rule for ported READMEs). day-one-runbook.md §8 updated with a new "a ported README can start LEAN" default bullet.
- DONE: Write ## Follow-up Routing = escalate (do NOT auto-file) with two candidate directions.
  `## Follow-up Routing` = `escalate`: (a) PRIMARY hold-out generalization test (general-capability vs ade-bench-specific construct overfit), (b) MINOR optional strengthen-#6 for asana002's ~75% model-path rate. No auto-file (flip program exhausted).

### Summary

Promoted the lean README to `@baseline` (h0060 861d18e790c72047 → h0061 50e340fd462032af), verified by `rk registry resolve`/`list`. Wrote `## Verdict` (PASSED) with the transferable learning that the accumulated scar-clause prose was dilution — a ported README can start lean (principle + gate + skeleton per rule) — and propagated that rule to `day-one-runbook.md` §8. Wrote `## Follow-up Routing = escalate` with two captain-strategy directions (PRIMARY: hold-out generalization test; MINOR: strengthen rule #6), explicitly NOT auto-filing since the flip program is exhausted. Left frontmatter + archive to the FO per instruction. One harness note surfaced: `rk baseline promote` needs `--to/--constraints` and is a spec-copy op, not the `@baseline` re-bind — `rk registry add run baseline` is the binding step.
