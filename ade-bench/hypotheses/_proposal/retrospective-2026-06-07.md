# End-of-Program Retrospective — The Oracle-Problem Systematic Program (2026-06-07)

**Scope.** This retrospects the entire oracle-problem flip portfolio that ran this session under
`_proposal/oracle-problem-systematic-program.md`: E0 (h0032), E1 (h0030), E2 (h0019), E3 (h0018),
E4 (h0033), and the combined full confirmation (h0034). It is the captain-requested
*retrospective-now* synthesis (chosen over chasing the final 2-task gap mid-flight). The honest
headline is in §1; the methodological findings — which are the real deliverable — are in §2–§4; the
concrete path to 75% next session is in §5.

---

## 1. Honest accounting — the pass rate did NOT move

**`@baseline` is UNCHANGED at 31/48 = 0.6458.** Nothing was promoted. The entire flip portfolio
(E1–E4 + the combined full) netted **+0** against a +5 target (75% = 36/48).

| Exp | Hypothesis | Target(s) | Outcome | Net to baseline |
|-----|-----------|-----------|---------|-----------------|
| E0 | h0032 | (instrument gate) | **PASSED** — method deliverable; ships nothing to solver | 0 (enables others) |
| E1 | h0030 | intercom001/002/003 | **REJECTED** — reconcile re-correlated through shared `_fivetran_active` filter; oracle-blocked | 0 (safe-but-inert) |
| E2 | h0019 | airbnb009 | **smoke-GO, HELD at full (artifact-proven)** — the ONE genuine fix | +1, but UNPROMOTED |
| E3 | h0018 | airbnb007 | **smoke-GO, REVERTED at full + multi-model** | 0 |
| E4 | h0033 | asana002 | **REJECTED** — cast lever inert; bug is structural; green-but-inert | 0 |
| — | h0034 (combined full) | airbnb009 + airbnb007 | **REJECTED / NO-PROMOTE** — net +0, paired CI [-4,+4] | 0 |

**The one genuine fix: airbnb009 (E2/h0019).** The anti-cross-join + worked-example lever flipped
airbnb009 FAIL→PASS at smoke AND held at full, and is **artifact-proven both times** — the committed
`models/agg/mom_agg_reviews.sql` swapped the `WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE…)`
spine filter for `WHERE DATE_ACTUAL BETWEEN (MIN…) AND (MAX…)` (3,786 → 4,508 aggregation dates),
exactly the prescribed shape. This is a real, repeatable, lever-attributable +1.

**Why the real +1 was not banked.** In the combined full (h0034, run
`runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303/`, clean strict audit
`tainted:0`), airbnb009 held (+1) and an incidental `f1011` flipped (+1), but two unrelated passers
regressed — `asana003` (build error in `asana__daily_metrics`, a `cast('None' as date)` from solver
staging re-wiring) and `f1005` (constructor-points `QUALIFY` rewrite off by 2) — both **rule-independent
gpt-5.5 non-determinism**. Net = +0. `stratified_pass_at_1 = 0.6458` exactly. **The real +1 from
airbnb009 was masked by ±2 of unrelated single-trial noise.** That is the binding constraint, stated
plainly: not lever quality, but **variance**.

---

## 2. Methodological findings — the real deliverable

### 2.1 THE VARIANCE WALL (the new binding constraint)

At `trials: 1` over `n=48`, gpt-5.5@xhigh manufactures **±2 incidental flips per run** independent of
any lever. The 10k paired bootstrap over the 48 per-task deltas (h0034, seed 20260607) gives a **95% CI
on the mean delta of [-0.0833, +0.0833] = [-4, +4] tasks**. A lone real +1 (airbnb009) sits *inside*
that band and cannot be cleanly distinguished from noise on a single trial. The do-no-harm tripwire (CI
must exclude a regression) is **structurally unsatisfiable for a +1 lever at trials=1** — the CI is wider
than the signal.

This is not new caution being restated for its own sake; it is the precise reason the program ended at
+0 despite owning a genuine fix. Two prior smoke-GO/full-revert events (h0012's f1006 flip; h0018's
airbnb007 flip) were the early warnings; the combined full made it the headline.

**Why we cannot just run `trials > 1` to shrink the CI.** The `freeze-repo concurrency race`
(MEMORY: `ade-bench-freeze-repo-concurrency-race`) blocks it: every task in a harbor run shares ONE
freeze git repo (`sealed_hash` computed without task identity on the harbor path), so `concurrency.trials > 1`
makes two trials `git commit` to the same repo simultaneously and one aborts with "cannot lock ref HEAD".
The current spec is pinned `trials: 1` to dodge the race. **So the variance wall is currently a
HARNESS-LIMIT wall, not a measurement-design wall** — we cannot average out the noise until the freeze
repo is made per-task/per-trial in razorback (pass `benchmark_task_id` into `compute_sealed_hash`, or
give each trial a unique `RAZORBACK_FREEZE_DIR`).

### 2.2 THE MULTI-MODEL-TARGET TRAP (why airbnb007 reverted)

airbnb007 is scored by **two** models: `daily_agg_nps_reviews` (the rolling-window model the E3 lever
addresses) AND `listing_agg_nps_reviews` (a per-listing lifetime NPS total with **no** rolling window,
which the E3 precondition never matches). In the combined full the rolling-window calendar-RANGE copy
DID reach the SQL — `daily_agg_nps_reviews` carried the 28-day `BETWEEN dateadd('day',-27,…) AND …`
RANGE and `daily_agg_nps_reviews_equality_with_tolerance` **PASSED** — yet the task scored 0 because
`listing_agg_nps_reviews_equality_with_tolerance` failed by 2 rows (`Got 2`). **The h0018 smoke-GO was
variance on the unaddressed `listing_agg` model, not a real fix of the rolling window.**

This is the **h0012/f1006 multi-model pattern**: a target whose pass/fail verdict is gated by a model
the lever does not touch. A single-model lever cannot credit a flip on a multi-model target — even when
its own mechanism lands artifact-proven. The lesson generalizes: *before crediting any single-model
lever with a target flip, enumerate ALL of the target's scored models; if the lever's precondition
matches fewer than all of them, a single-run flip is variance, not a fix.*

### 2.3 The two findings interact

The variance wall and the multi-model trap compound: airbnb007 has *both* an unaddressed second model
*and* single-trial noise, so its smoke flip was doubly untrustworthy. airbnb009 has neither problem
(single scored model, lever-attributable) — yet still couldn't be banked, because the *combined* run's
unrelated ±2 noise swamped its clean +1. The program's ceiling was therefore set by measurement, not by
the levers: we own a real fix we cannot prove at the current trial budget.

---

## 3. The dead-family map (do NOT re-file these)

Every checking/generation family aimed at the 17 false-greens has now been exhausted or oracle-blocked.
The recurring wall is the **oracle problem** (`_artifacts/verification-without-oracle.md`): the only
thing that beats no-oracle is *independent redundancy*, and the universal failure is *correlated error*.

| Family | Status | Why dead | Evidence |
|--------|--------|----------|----------|
| **Grain construct (entity spine, prose/example/contract)** | EXHAUSTED | inert at gpt-5.5/xhigh — "talks but doesn't do" (h0010 prose, h0016 example, h0017 contract) | `_archive/h0010,h0016,h0017` |
| **Grain reconcile (raw-source COUNT(DISTINCT) + anti-join)** | EXHAUSTED + ORACLE-BLOCKED | the "independent" probe **re-correlated through the shared `_fivetran_active` filter** — parent and child collapse to the same 5 keys, anti-join empty, false-green. "Which population is canonical" is oracle-only. | E1/h0030, `_archive/h0030` |
| **Cast / type-contract (seed-layer, model-layer)** | EXHAUSTED for asana002 | asana002 is a **structural package-migration** (Fivetran made tags optional), not a representation mismatch — a `::type` cast has no surface. h0009 bled / h0020 seed-layer-inert / h0033 model-layer-no-surface (green-but-inert) | E4/h0033, `_archive/h0033`, `_archive/h0020` |
| **Candidate-generation + arbitration (selector, dual-contract)** | EXHAUSTED | genuine candidate diversity + external-criterion arbitration are **table stakes, not a contribution** — both achieved (h0031 route B diverged, used raw conservation probes) and STILL reproduced baseline's byte-identical wrong answer (f1011 `ABDE`). More generation does not create an oracle. | `_archive/h0026, h0031` |

**The single survivor family that produced a real fix:** surgical, copyable, in-place
**Implementation-stage worked-example edits** anchored to a concrete local artifact (the asana002-shape).
That is the form that landed airbnb009 (E2) and *reached* the right SQL on airbnb007 (E3) — it is the
only lever shape that has ever moved committed SQL toward correct on this `@baseline`. It works when the
target is a **value/shape to match** and **single-model**; it fails when the bug is structural with no
mechanical surface (E4), when the deciding fact is a filtered-population convention (E1), or when a
second unaddressed model gates the verdict (E3).

---

## 4. Method deliverables (banked, first-class, transferable)

These are the durable wins of the program — small successes compounding toward the goal, per the
captain's "knowledge gains are small successes" doctrine. The pass-rate number did not move; the
*method* did.

1. **E0 instrument-gate (h0032 PASSED).** A per-check, OFFLINE two-sided discrimination gate: before any
   "independent second-path" check is trusted on a real task, it must FIRE on an injected error AND stay
   SILENT on a known-good. Inert (silent-on-injected) = the h0010/h0016 prose signature; correlated
   (fires-on-known-good) = the h0008/h0012 signature. Harness + machine-readable 2×2 at
   `_artifacts/h0032-e0-harness/`. **Refinement forced by h0030:** an E0 fixture for a grain/completeness
   probe MUST share the target's upstream filter (apply the same `active`/effective-date predicate to both
   parent and child), or it validates the probe in a regime the real failure does not inhabit (E0
   over-predicted GO on h0030 because its fixtures were filter-clean).

2. **Correlated-error-via-shared-filter (E1/h0030).** A raw-source independent probe — the strongest shape
   we have — can still re-correlate if it inherits the model's upstream FILTER/population, not just the
   relation/route. Independence must hold for the **population**, not only the relation. Encoded into the
   sharp test in `_artifacts/verification-without-oracle.md` and the Grain arbitration clause in
   `_artifacts/arbitration-without-oracle.md`.

3. **Green-but-inert / attribution (E4/h0033).** A green flip is NOT lever attribution. A mechanical-edit
   lever can be inert yet the target flips green, because the solver fixes the bug structurally without
   emitting the prescribed token. Attribution requires the **prescribed artifact in the COMMITTED SQL**,
   not a green score. The cheap inert-detector (`Got N` unchanged) catches *nothing-happened*; the
   artifact read catches *something-happened-but-not-the-lever*.

4. **Worked-example-decisive (E2/E3 confirmation).** A copyable BEFORE/AFTER SQL skeleton anchored to a
   local sibling artifact is the ONE lever shape that reaches the committed SQL where restructuring prose
   goes inert. Confirmed three times now (asana002 under h0009, airbnb009 under h0019, the airbnb007
   window-copy under h0018 — the last *reached* the SQL even though the task didn't flip). This is the
   live construction-side lever family; everything prose-only is dead.

5. **The multi-model-target trap (E3 + this retrospective).** New, banked into the taxonomy and
   WORKFLOW-REFINE: enumerate a target's scored models before crediting a single-model lever.

---

## 5. Recommended next moves — how to actually close toward 75%

The program proved the ceiling is **measurement**, not lever quality, for at least one real +1. The
fastest honest gains are about *banking what we already have* and *removing the variance blocker*, not
inventing new levers.

### 5.1 Bank airbnb009 under noise (highest-value, lowest-risk)
airbnb009/E2 is a real, artifact-proven, single-model, lever-attributable +1 that the combined run could
not bank only because of unrelated noise. Two paths to bank it:
- **(preferred) Fix the freeze-repo race** so `trials > 1` is safe — make the freeze repo per-task/per-trial
  in razorback (`benchmark_task_id` into `compute_sealed_hash`, or unique `RAZORBACK_FREEZE_DIR` per trial).
  Then a multi-trial paired run shrinks the CI below ±1 and the +1 separates from noise. This unblocks the
  entire program, not just airbnb009.
- **(stopgap) A multi-trial paired re-confirm of E2 ALONE** (h0019, no E3) — run airbnb009 + canaries at
  several trials (sequentially if the race is unfixed) and take the paired delta. Isolating E2 from E3's
  unrelated regressions and averaging trials is the cheapest way to demonstrate the +1 without touching
  razorback. Do NOT auto-promote on a single trial.

### 5.2 Re-triage the LOW / Track-Z tasks by the E1 tractability rule
Apply the E1 **value/shape-to-match vs population-canonical** distinction to the 9 LOW/Track-Z tasks:
a task is only winnable by an independent check if its deciding fact is a value/shape to match, not a
filtered-population convention or an oracle-only `int_` convention. Most of Track Z fails this test
(asana004/005/005-hard `int_` convention; ana-eng004/f1002 over-declared/misleading schema; f1011
locally-misleading). Confirm none was mis-triaged as oracle-only when a *truthful* local declaration
exists — that is the only place a 6th visible-arbitrator target could hide.

### 5.3 Source a 6th/7th visible-arbitrator target
The filed flip portfolio is exhausted at one real fix (airbnb009). To reach 75% we need 4 more clean +1s,
and the dead-family map says they will NOT come from grain/cast/arbitration. Source new targets only where
the deciding fact is a **value/shape to match** with a **single scored model** and a **local arbitrator** —
the airbnb009/asana002 profile. The width cluster (#2: ana-eng004, f1002) and the value-divergence cluster
(#3: ana-eng007/ana-eng007-medium) are the next candidates *if* a truthful local declaration is found;
h0029 (column-set reconcile vs schema.yml) is filed for #2 but must clear the multi-model-target check and
E0 first.

### 5.4 Add a MULTI-MODEL-TARGET check to the smoke/gatekeeper discipline
New gate rule (G8-adjacent): before a single-model lever is credited with a target flip, **enumerate the
target's scored models from the verifier test set**; if the lever's precondition matches fewer than all of
them, treat a single-run flip as variance — require a repeat or a wider lever, and do not credit the flip.
This would have caught airbnb007's false smoke-GO at propose. Pair it with the standing variance caution
(a lone flip with no artifact proof, or a flip on a multi-model target, may be noise).

---

## 6. Bottom line for the captain (plain words)

We ran the whole plan. The score did not move — it is still 31 of 48. That is the finding, not a failure
to report: we now know **the thing stopping us is measurement noise, not bad ideas.** We have one genuinely
good fix (airbnb009) that we can see working in the committed code, but at one trial per task the run-to-run
noise is bigger than a single fix, so a real +1 gets cancelled out by two unrelated lucky/unlucky flips
elsewhere. The cheapest next win is **not a new idea — it is making the harness able to run each task more
than once** (fix the freeze-repo race), then re-confirming airbnb009 alone. We also mapped out which whole
families of ideas are dead ends (grain rewrites, type casts, second-opinion judges), so we stop spending
runs on them. And we learned a new trap — some tasks are graded on two models at once, so a fix to one of
them can look like a win at smoke and vanish at full. Promote nothing now; the combined run did not clear.

---

**Cross-refs:** `_proposal/oracle-problem-systematic-program.md` (the plan);
`h0034-combined-e2-e3-full-confirmation.md`, `h0019-implementation-let-categories-emerge-not-cross-join.md`,
`h0018-contract-rolling-window-calendar-range.md` (active entities);
`_archive/h0030, h0031, h0032, h0033` (E1/arbitration/E0/E4);
`_artifacts/{verification-without-oracle.md, arbitration-without-oracle.md, bug-type-taxonomy.md, WORKFLOW-REFINE.md, term-table.md}`;
MEMORY: `ade-bench-freeze-repo-concurrency-race` (the variance-wall blocker),
`verification-without-oracle-real-world`, `ade-bench-solver-blind-to-oracle`,
`ade-bench-validation-self-anchored-false-green`, `ade-bench-instruction-lever-taxonomy`.
Run dirs: `runs/ade-bench-baseline/622bdedac572b479` (@baseline 31/48);
`runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303` (combined full, NET +0);
`runs/ade-bench-h0019-implementation-let-categories-emerge-not-cross-join/d8bd75a0189bda65` (E2 smoke-GO);
`runs/ade-bench-h0018-contract-rolling-window-calendar-range/72b3c0a6d7ac9f05` (E3 smoke-GO).
