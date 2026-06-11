# h0042 forensic postmortem — "passed smoke 3/3, failed at full"

**Status:** evidence-backed standalone report (verifies the archived entity against raw run-dir
artifacts). Author: dispatched ensign, 2026-06-11. Every "why" below cites a raw log path; every
fork classification comes from the committed `apply_patch` payload, never transcript narration.

---

## Executive summary (the answer to "why did smoke pass but full fail")

h0042 added one solver-README rule — *coverage repairs must preserve the existing aggregate metric
(`COUNT`/`SUM`/`AVG`)* — to pin the single free line that made `airbnb009` non-reproducible. Its one
focused smoke (panel + two repeats) was **3/3 PASS**, and the committed SQL proves the rule fired:
all three kept `COUNT(*)` and edited only the date spine. At full it scored **27/48 (0.5625), net −4
vs the 31/48 baseline**, and `airbnb009` **stayed FAIL** — because the full draw's committed SQL
reverted to the **exact h0019 wrong fork** (`COUNT(*)` → `COUNT(review_cte.REVIEW_DATE)` plus a
`sentiments_cte` CROSS-JOIN restructure), identical to what `@baseline` itself committed. The smoke
could not predict this because `airbnb009` is a **low-base-rate bimodal cell — it passes only 2/12
(~17%) across every full run on disk** — and a focused 3/3 was a favorable-tail streak, not the base
rate. The pin **reduces but does not eliminate** the fork variance; at `trials: 1` the single scored
draw landed on the modal FAIL branch. The other 4 of the 5 regressions are ordinary single-trial
variance on non-coverage tasks where the rule never fires (paired-delta CI touches 0, p=0.22). Net:
no clean lever-caused harm, no new movement — REJECTED, `@baseline` unchanged.

---

## 1. What h0042 was

**The lever (one paragraph).** A single Implementation-stage policy block added to a fork of the
`@baseline` solver README (verbatim B-variant text, archived entity lines 36–43): *"When the task is
about missing rows, date-spine coverage, row coverage, or join coverage, treat the fix as a coverage
repair first. Do not change metric definitions such as COUNT, SUM, AVG, window expressions, or
business-rule filters unless the task instruction, schema, visible project tests, or sibling model
evidence explicitly says that metric definition is wrong. If local validation passes after the
coverage repair, preserve the existing metric semantics."* It is a generative, abstract
abstain-prose tie-breaker — it does not name `airbnb009` and supplies no worked-example SQL skeleton
(the G7 inert-risk the gatekeeper flagged, archived entity line 134).

**The target.** `ade-bench-airbnb009`. Its scored model is `mom_agg_reviews`, whose `dates_cte`
narrows the date spine to days that already have a direct review. The known repair restores the full
spine; the known *trap* is that, after restoring the spine, the solver is free to also "clean up" the
aggregate from `COUNT(*)` to `COUNT(review_cte.REVIEW_DATE)`. h0042's claim: pin that aggregate line
so the repair becomes reproducible. The decisive artifact for every run is the committed hunk to
`models/agg/mom_agg_reviews.sql`.

---

## 2. Why the full run failed (committed-artifact reason)

**`airbnb009` at full = FAIL, reward 0.** Verifier: `mom_agg_review_date_range` —
> `Got 1 result, configured to fail if != 0`
>
> — `runs/ade-bench-h0042-coverage-repair-preserve-metric-semantics/1948ab42a6a5d9b7/ade-bench-airbnb009__uo2JG9E/verifier/test-stdout.txt:45,52`
> (reward.txt = `0`). The model itself built fine (`1 of 1 OK created sql incremental model
> main.mom_agg_reviews`, same file line 17) — this is a **semantic mismatch, not a build error**.

**The committed fork** (the only `apply_patch` to `mom_agg_reviews.sql` this cell;
`…/ade-bench-airbnb009__uo2JG9E/agent/sessions/2026/06/10/rollout-2026-06-10T18-25-45-019eb2c8-828b-7a93-b890-b0a89d22bed3.jsonl:139`):

```diff
 dates_cte AS (
-	WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE::DATE FROM review_cte)
+	WHERE DATE_ACTUAL BETWEEN (SELECT MIN(REVIEW_DATE::DATE) FROM {{ref('fct_reviews')}})
+						  AND (SELECT MAX(REVIEW_DATE::DATE) FROM {{ref('fct_reviews')}})
 ),
+sentiments_cte AS ( SELECT DISTINCT REVIEW_SENTIMENT FROM {{ref('fct_reviews')}} ),
+date_sentiments_cte AS ( SELECT dates_cte.DATE_ACTUAL, sentiments_cte.REVIEW_SENTIMENT
+	FROM dates_cte CROSS JOIN sentiments_cte ),
 final_cte AS ( SELECT
-	COUNT(*) AS REVIEW_TOTALS ,
+	COUNT(review_cte.REVIEW_DATE) AS REVIEW_TOTALS ,
-	review_cte.REVIEW_SENTIMENT , dates_cte.DATE_ACTUAL AS AGGREGATION_DATE FROM dates_cte
+	date_sentiments_cte.REVIEW_SENTIMENT , date_sentiments_cte.DATE_ACTUAL AS AGGREGATION_DATE
+	FROM date_sentiments_cte
 	LEFT JOIN review_cte ON …
```

Three things happened at once: (a) the **date-spine repair landed** (`IN(DISTINCT)` →
`BETWEEN MIN..MAX`); (b) the aggregate was **rewritten to `COUNT(review_cte.REVIEW_DATE)`** — the
exact line the lever forbade; (c) a `sentiments_cte` + `date_sentiments_cte` **CROSS-JOIN
restructure** was added. So the rule did NOT suppress the wrong fork in this context.

**This is the baseline's own fork.** `@baseline`'s `airbnb009` cell committed the same wrong
aggregate (`…/ade-bench-baseline/622bdedac572b479/ade-bench-airbnb009__zaFEXfL/agent/sessions/2026/06/02/rollout-…147`):
`-COUNT(*)` → `+COUNT(review_cte.REVIEW_DATE)` plus a `sentiments_cte` CROSS JOIN — and the same
verifier failure `Got 1 result, configured to fail if != 0`
(`…/zaFEXfL/verifier/test-stdout.txt:52`, reward `0`). h0042 at full reproduced the baseline
behavior; the lever changed nothing on the scored draw.

No other task "failed *because of a fork the lever flipped*" — the other regressions are non-coverage
tasks (§4); `airbnb009` is the only cell whose failure is the lever's own subject matter.

---

## 3. Why smoke passed repeatedly but full failed — THE CENTRAL QUESTION

### Every `airbnb009` cell reconstructed from the committed SQL

| Cell | Run (kind) | Spine predicate | Aggregate (committed) | CROSS JOIN | Reward | Got N | Committed-SQL apply_patch path |
|---|---|---|---|---|---|---|---|
| `NH3nEkU` | `797604a420d08244` (smoke panel) | `IN(DISTINCT)` → `BETWEEN MIN..MAX` | `COUNT(*)` (line **not in hunk** = kept) | none | **1.0 PASS** | — | `…/797604…/ade-bench-airbnb009__NH3nEkU/agent/sessions/…/rollout-2026-06-10T08-45-56-…jsonl:125` |
| `ERR5VmQ` | `0a456f136f374439` (focused #1) | `IN(DISTINCT)` → `BETWEEN MIN..MAX` (bounds-CTE) | `COUNT(*)` (**not in hunk** = kept) | bounds-CTE only (not sentiment) | **1.0 PASS** | — | `…/0a45…/ade-bench-airbnb009__ERR5VmQ/agent/sessions/…/rollout-2026-06-10T09-32-18-…jsonl:151` |
| `dvgEBNs` | `a267ccc4c36ec50c` (focused #2, seed 42) | `IN(DISTINCT)` → `BETWEEN MIN..MAX` | `COUNT(*)` (**not in hunk** = kept) | none | **1.0 PASS** | — | `…/a267…/ade-bench-airbnb009__dvgEBNs/agent/sessions/…/rollout-2026-06-10T09-47-05-…jsonl:157` |
| `uo2JG9E` | `1948ab42a6a5d9b7` (FULL) | `IN(DISTINCT)` → `BETWEEN MIN..MAX` | **`COUNT(review_cte.REVIEW_DATE)`** (line **rewritten**) | sentiments + date_sentiments | **0.0 FAIL** | 1 | `…/1948…/ade-bench-airbnb009__uo2JG9E/agent/sessions/…/rollout-2026-06-10T18-25-45-…jsonl:139` |

The three smoke cells are **artifact-real**: in each, the `COUNT(*) AS REVIEW_TOTALS` line never
appears in any diff hunk — it is preserved by construction, and only the `dates_cte` (and in ERR5VmQ a
bounds-CTE) is edited. The 3/3 was genuine. The full draw is the bimodal cell's other branch.

### The mechanism: a low-base-rate, lever-unpinned-in-practice fork

The pass/fail is a pure function of one line — *which aggregate the solver commits, conditional on the
spine repair landing* — and the lever did not deterministically pin it. The cross-run evidence proves
the variance is intrinsic to the cell, not to h0042:

**`airbnb009` passes 2/12 (~17%) across every full (≥40-cell) run on disk** (independently enumerated
by reward.txt over all run-dirs):

| Run-dir (full) | airbnb009 reward | committed aggregate | committed spine |
|---|---|---|---|
| `ade-bench-baseline/622bdedac572b479` | 0 | `COUNT(review_cte.REVIEW_DATE)` | BETWEEN |
| `ade-bench-baseline-gpt-5.4-mini/5295…` | 0 | — | — |
| `…codex-gpt54mini-xhigh/c5ac…` | 0 | — | — |
| `h0009…/1026…` | 0 | — | — |
| `h0012…/3d82…` | 0 | — | — |
| `h0017…/1928…` | 0 | — | — |
| `h0019…/8773…` | 0 | **`COUNT(review_cte.REVIEW_DATE)`**, BETWEEN, no cross-join (Got 1, `…/8773…/…airbnb009…/verifier/test-stdout.txt:52`) | BETWEEN |
| **`h0034…/1880…`** | **1** | **`COUNT(*)` kept** (line not in hunk), BETWEEN, no cross-join | BETWEEN |
| `h0037…/5d70…` | 0 | — | — |
| **`h0041…/fe15…`** | **1** | **`COUNT(*)` kept** (line not in hunk), BETWEEN, no cross-join | BETWEEN |
| `h0042…/1948…` (this run) | 0 | `COUNT(review_cte.REVIEW_DATE)` + cross-join | BETWEEN |
| `h0043…/7390…` | 0 | — | — |

**The two passing full runs (h0034, h0041) both kept `COUNT(*)` with a spine-only edit; the two
artifact-classified fails (h0019, h0042) both rewrote to `COUNT(review_cte.REVIEW_DATE)`.** The
divide is exactly the aggregate line. A focused 3/3 single-cell smoke is **3 draws from a ~17%-pass
process that happened to cluster on the good branch** — it over-sampled the favorable tail and was
therefore necessary-but-not-sufficient. At `trials: 1` the one scored full draw fell on the modal
FAIL branch. The pin demonstrably *reduces* the wrong-fork rate (3/3 + 2 other full passes vs the
modal fail) but does not *eliminate* it — abstract abstain-prose can be acknowledged-and-skipped (the
G7 inert risk). This is the standing single-trial reality: "pinned the fork in N fresh contexts" ≠
"the single scored trial lands there."

---

## 4. Net + per-task ledger at full (both directions)

**Absolute:** h0042 = **27/48 (`stratified_pass_at_1` 0.5625** via `rk score`; independently, 27 of
48 `reward.txt` == 1). **Strict audit clean BEFORE the score was trusted:** `rk audit … --policy
strict` → `summary {clean: 48, coverage_missing: 0, tainted: 0}`, 0 findings. **Baseline
622bdedac572b479 = 31/48** (31 of 48 reward.txt == 1, independently counted). **Paired delta = −4**
(slug-paired over the identical 48-task set). The archived entity reports a 10k-bootstrap 95% CI of
**[−9, 0] tasks (touches 0), sign-test p = 0.219** — i.e. not statistically distinguishable from
zero. NOTE: this is the comparison against the **31/48 baseline in force at h0042's time**; the
current `@baseline` is now 32/48 (h0043), which h0042 leaves untouched.

| Task | @baseline | h0042 full | Δ | Committed-artifact mechanism (raw cite) | Cross-run P/F | Class |
|---|---|---|---|---|---|---|
| **airbnb009** (target) | 0 F | 0 F | 0 | aggregate rewritten to `COUNT(review_cte.REVIEW_DATE)` + sentiments CROSS-JOIN; `Got 1` (`…uo2JG9E/verifier/test-stdout.txt:52`; patch jsonl:139) | P 2/12 (~17%) | target did not flip — bimodal, pin reduces ≠ eliminates |
| airbnb005 | 1 P | 0 F | −1 | `*_nps_reviews_equality_with_tolerance` FAIL 4 / FAIL 2 (`…airbnb005__TfLibsk/verifier/test-stdout.txt:90,92`); from-scratch NPS rolling-window authoring | P 10/12 (F 2/12) | rare drop; from-scratch value/window divergence, NOT a coverage-repair the rule fires on |
| asana003 | 1 P | 0 F | −1 | `ERROR creating sql table … asana__daily_metrics` + 6/17 equality FAILs (project 16, tag 17, task 1, project_task_metrics 17, project_user 13, task_tags 1) (`…asana003__mssQ5T4/verifier/test-stdout.txt:79,214–242`); package-staging migration | P 8/12 (F 4/12) | single-trial VARIANCE (rule doesn't fire) |
| f1005-medium | 1 P | 0 F | −1 | `AUTO_constructor_points_equality` FAIL 2 (driver_points PASS) (`…f1005-medium__mQjVVPB/verifier/test-stdout.txt:58,62`); value divergence | P 8/12 (F 4/12) | single-trial VARIANCE |
| f1006-hard | 1 P | 0 F | −1 | `AUTO_constructor_points_equality` FAIL 2 (driver_points PASS) (`…f1006-hard__ZttduZy/verifier/test-stdout.txt:58,62`); value divergence | F 8/12 (chronic — also dropped h0037/h0041/h0043) | single-trial VARIANCE |
| quickbooks003 | 1 P | 0 F | −1 | **Compilation Error** — `int_quickbooks__expenses_union` / `…sales_union` / `quickbooks__ap_ar_enhanced` "has less columns than solution__…" (`…quickbooks003__Q9tARwd/verifier/test-stdout.txt:354,355,362,370`); under-inclusion / broken edit on a package-config task | P 6/12 / F 6/12 (coin-flip) | single-trial VARIANCE (compile-broken, not coverage) |
| asana002 (gain) | 0 F | 1 P | +1 | conditional-inclusion package-migration fix; `AUTO_asana__task_equality` PASS (`…asana002__bs2LnhU/verifier/test-stdout.txt:224`) | P 6/12 / F 6/12 (coin-flip) | incidental VARIANCE gain, NOT the lever's target |

**Arithmetic:** +1 (asana002) − 5 (regressions) = −4; airbnb009 contributes 0.

**Broke-a-passer vs failed-to-help:** all 5 regressions were @baseline 1.0 passers → this is damage
to working rows, not "failed to help." BUT 4/5 (asana003, f1005-medium, f1006-hard, quickbooks003)
are non-coverage tasks where the rule's premise never holds (package-migration / value-divergence /
compile-broken), each failing in 4–8 of the other 12 full runs — so they are **executed-but-the-rule-
is-inert-there**, independent variance, not lever-caused harm. **airbnb005 is the lone anomaly**
(drops only 2/12) and is a from-scratch NPS-authoring task with many free knobs, still not a clean
"rule preserved a metric that should have changed." **There is no cell where the lever flipped a
metric it should not have.** The target (airbnb009) "failed to help": rule present, did not fire on
the scored draw.

---

## 5. New learnings (transferable rules)

1. **A focused single-cell reproducibility smoke — even 3/3 — is not a flip predictor for a
   low-base-rate target at `trials: 1`.** Three draws from a ~17%-pass bimodal process can cluster on
   the favorable tail and read 3/3 while the modal outcome is FAIL. Before promoting such a flip,
   *measure the cross-run base rate* (the 2/12 table existed on disk the whole time) — a smoke that
   over-samples one branch is necessary-not-sufficient evidence.

2. **An abstract abstain-prose lever pins a fork probabilistically, not deterministically.** h0042
   moved airbnb009 from "modal-fail" toward "more often pass" (3/3 smoke + 2/12 full passes are real),
   but a rule with no worked-example skeleton can be acknowledged-and-skipped on any given draw (the
   G7 inert mode). Classify by the committed SQL, never the transcript: the full cell's transcript
   may have acknowledged the rule, yet the committed aggregate was the forbidden one.

3. **A generative rule's smoke verdict is provisional pending full.** A 6-task panel structurally
   cannot see the 41 unsampled tasks; 4 of the 5 regressions here were coin-flip cells on unsampled
   tasks that churn run-to-run. For generative levers, treat smoke GO as conditional and expect a
   variance-band of ±several tasks at full.

4. **Oracle-blindness restated:** the solver could not tell `COUNT(*)` from `COUNT(review_date)` was
   the *correct* metric — both pass local validation — so the only thing standing between them was an
   external rule, and an abstract one does not bind. (The oracle, used for analysis only, also uses
   `COUNT(*)` with a MIN..MAX spine, so `COUNT(*)` is correct and the h0019/full fork is wrong.)

**The airbnb009 saga across h0019 / h0041 / h0042** (all artifact-classified above): h0019 first
*found* the spine repair but left the aggregate free and committed the wrong `COUNT(review_date)` fork
(FAIL, `…8773…/…/verifier/test-stdout.txt:52`). h0034 and h0041 are the only two full runs that ever
passed it — both by keeping `COUNT(*)` with a spine-only edit (incidental, not because either lever
targeted the fork). h0042 explicitly targeted the fork, reproduced 3/3 in smoke, but on its single
full draw landed on the same wrong fork as h0019 and baseline. Across all four artifact-read full
runs the rule is exact: **kept `COUNT(*)` ⇒ PASS, rewrote to `COUNT(review_date)` ⇒ FAIL.** The cell
is a coin-flip on that one line and no instruction lever filed so far made the favorable side reliable
at `trials: 1`.

---

## 6. Methodology implication

**Why our smoke methodology structurally could not predict the full outcome.** The smoke design was a
focused panel (`airbnb009` + 5 cross-family canaries) plus two focused `airbnb009` repeats, with a GO
bar of ≥2/3 committed-`COUNT(*)`+pass. Two structural blind spots made it un-predictive:

- **It measured the wrong quantity.** A 3-draw focused repeat estimates "can the rule ever produce the
  good branch," not "what fraction of scored draws land there." For a bimodal ~17%-pass cell, the
  former can be 3/3 while the latter is low — and only the latter governs a `trials: 1` full score.
  The methodology had no step that compared the smoke draws to the cell's known cross-run base rate
  (which was already on disk: 2/12).

- **A 6-task panel cannot surface unsampled-task variance.** 4 of the 5 full regressions were
  coin-flip cells on tasks the smoke never ran (the G8 gap). The panel's 5 canaries themselves held
  PASS at full — the regressions were entirely on unsampled cells — so the canary panel gave a true
  "no canary lost" signal that was nonetheless uninformative about the net.

**What would have caught it.** (a) Reading the cross-run base-rate table for the target *before*
promoting (2/12 was a red flag that 3/3 was a tail streak); (b) for a low-base-rate flip target,
either requiring multi-trial CI on the target — which the standing `trials: 1` decision forbids,
making such flips un-promotable by construction — or labeling the smoke GO explicitly provisional and
expecting a single full draw to regress to the ~17% base rate; (c) treating any generative rule's
smoke as a lower bound on full variance, not a point prediction. The transferable lesson is durably
recorded in MEMORY (`ade-bench-single-trial-judge-by-artifact`, the focused-reproducibility-smoke-trap
paragraph) and the verdict re-confirms the concluded flip-portfolio / single-trial-variance wall
(`ade-bench-oracle-program-concluded`).

---

### Attestation

- Score: `rk score …/1948ab42a6a5d9b7 --format json` → `stratified_pass_at_1 = 0.5625`; independent
  reward count 27/48 pass. Baseline `622bdedac572b479` independent reward count 31/48 pass.
- Audit: `rk audit …/1948ab42a6a5d9b7 --policy strict` → `summary {clean: 48, coverage_missing: 0,
  tainted: 0}`, 0 findings.
- Every fork classification above is from the committed `apply_patch` payload in the cell's
  `agent/sessions/**/*.jsonl`, not transcript narration (AC-3). The COUNT line being *absent from a
  diff hunk* is the proof that `COUNT(*)` was preserved by construction.
- This report verifies and upholds the archived entity's `### Decisive: THE REPRODUCIBILITY GAP` and
  `### Per-task ledger` conclusions; no prior claim failed to hold up against the raw logs.
