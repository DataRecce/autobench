# Post-h0056 Move Discovery — how we derived Move A & Move B (the road to 36/48)

Date: 2026-06-14
Author: operator
Purpose: record the *reasoning chain* that turned the h0056 two-draw full-run evidence into the
two moves of h0057 (Move A = flip ana-eng004; Move B = stabilize quickbooks002/003). This is a
methodology document — the goal is a repeatable "after a full run, how do we pick the next move"
procedure, not just h0057-specific notes.

Inputs: h0056 promote analysis (`hypotheses/_archive/h0056-compose-six-levers-on-h0052.md`),
the flip-map (`_artifacts/round1-round2-flipped-task-choice-map.md`), and the leverable-task
research (`_proposal/leverable-flipped-tasks-research-2026-06-13.md`).
Output: `hypotheses/h0057-aneng-obt-preserve-columns-and-feature-drop-keep-base-id.md`.

> **OUTCOME UPDATE (2026-06-15) — Move A FAILED, Move B PROMOTED. Read §8 before reusing this
> procedure.** Move A never flipped ana-eng004 (h0057 REJECTED after 4 real-run revise cycles —
> the pre-diagnosis below was WRONG). Move B was validated and shipped alone as h0058
> (`runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r2/eba9295fda32c05e`, PROMOTED;
> two-draw mean 34/48, @baseline now 35/48). Goal 36 still open. The §5 selection logic mostly
> held — but step 3 (static-forensic flip-target pick) has a sharp failure mode documented in §8.

## 0. Situation after h0056

h0056 (six-lever composition) promoted to `@baseline` on its **r2** draw =
`runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a` = **35/48**.
Goal: **36/48**. So we need exactly **+1 net** — one new flip that does not get cancelled by a
regression. Two sub-goals fall out of that: (A) find a flippable FAIL cell, and (B) make sure we
don't lose a current passer in the same draw.

## 1. Method: analyze BOTH draws, not just the promoted one

h0056 was run as two independent seed-perturbed draws (the h0052 self-consistency precedent):
**r1 (seed 42) = 32/48, r2 (seed 43) = 35/48.** The promoted number is r2's 35, but the *pair*
is the real evidence. Paired by slug from each `per_trial_outcomes.json` (not `rk runs diff` —
it TypeErrors on `query_id: null`).

**Decisive decomposition — the 3-cell r1↔r2 gap:**

| Cell | base h0052 | r1 | r2 | Locked by a lever? |
|------|-----------|----|----|--------------------|
| f1001 | PASS | **FAIL** | PASS | no — deep src-registration build variance |
| quickbooks002 | PASS | **FAIL** | PASS | no — h0045 feature-removal coin-flip |
| quickbooks003 | PASS | **FAIL** | PASS | no — same |

**Finding 1 — "35 is a lucky draw, not a stable floor."** The entire r1→r2 improvement is three
un-locked coin-flip cells landing PASS in r2. The composition's true expectation is ~33.5; r2's 35
sits on top of those three (plus f1011, an oracle coin-flip). A fresh draw of the same README would
likely land ~34. **Implication:** a flip alone, on a lucky-35 baseline, is fragile — we want a move
that *also* converts some of those coin-flips into stable passers. That is what splits the problem
into Move A (flip) + Move B (stabilize).

## 2. Classify the whole board: stable-FAIL vs fragile-PASS

Computed each task's outcome across base/r1/r2 plus its historical pass rate over all gpt-5.5
run-dirs on disk. Two lists matter.

**Stable-FAIL (FAIL in BOTH r1 and r2) — the flip-target candidates:**

| Cell | hist | read |
|------|------|------|
| ana-eng004 / 006 / 007 / 007-medium | **0/N (never passed)** | build/rename family — h0055 siblings |
| asana004 / 005 / 005-hard | 0/N | unknown construct |
| f1002 | 0/23 | f1 grain/aggregate |
| quickbooks001 | 0/25 | likely feature-removal/large-build variance |
| intercom001 / 002 / 003 | 0/N | **oracle-blocked** (no passer ever) — do NOT file |
| asana003 | 15/24 (63%) | volatile passer that happened to fail both draws (bad luck) |

**Finding 2 — the stable-FAIL set is almost all "never-passed" (0/N), not coin-flips.** These need
a *real* new lever, not luck. The only cluster adjacent to a banked win is **ana-eng build/rename**
(direct h0055 siblings). intercom is oracle-blocked (excluded). asana003 is a frequent passer that
fell twice by variance, not a target.

**Fragile-PASS in r2 (the regression risk) — passers that are NOT lever-locked:**

| Cell | hist | lockable? |
|------|------|-----------|
| quickbooks002 / 003 | 93% / 74% (fell in r1) | **YES** — feature-removal over-drop boundary |
| f1001 | 81% (fell in r1) | no — deep src-registration build issue |
| f1011 | 33% | no — oracle multiple-choice coin-flip |
| asana002 | 72% | no — package/staging variance |

(airbnb005/007, f1006/-hard, airbnb009, ana-eng003, f1010-medium read as low-hist but are
**lever-locked** post-h0053/44/50/55 — their old history predates the lever; they are stable now.)

**Finding 3 — only qb002/qb003 are both a top regression risk AND lockable.** f1011/asana002 are
unlockable (oracle/variance); f1001 is a deep build issue. So the regression-reduction move has
exactly one clean target family.

## 3. Move A — pick the flip target (forensic-confirmed)

From Finding 2, the ana-eng build/rename cluster is the only stable-FAIL cluster adjacent to a
banked lever (h0055 preserve-columns). Ran a committed-artifact forensic on ana-eng004 and
ana-eng006:

- **ana-eng004 → SAME construct as the banked ana-eng003.** It builds `obt_product_inventory`
  ("add product details to every inventory item") by joining `fact_inventory` ⋈ `dim_products`;
  the solution is effectively `SELECT *` (22 columns). The solver prunes to a "relevant" subset →
  "has less columns than solution__obt_product_inventory". **Dropped-existing-columns — exactly what
  h0055 fixed on ana-eng003.** ✅ flip target.
- **ana-eng006 → NOT clean.** Three distinct failure modes (a missing *derived* column
  `supplier_company` via a supplier join; a dedup/uniqueness failure on `fact_inventory`; a
  cascading OBT). A preserve-columns rule fixes none of them. ❌ excluded.

**Finding 4 — the precondition gap (the actual mechanism of Move A).** The h0055 rule does not fire
on ana-eng004 *today* because its precondition says "build/rename from **a single upstream model**"
— ana-eng004 builds from a **join of two** upstreams. The rule is correct; it just doesn't match a
join build. **Move A = widen that one precondition** ("single upstream" → "one or more upstream,
including a fact⋈dim OBT join") so the existing, already-banked preserve-columns rule fires. This is
the same generalization pattern already observed: h0053 (built for airbnb005) generalized to airbnb007
on its own. Move A is the deliberate version of that.

## 4. Move B — pick the regression-reduction target (forensic-confirmed)

From Finding 3, qb002/qb003 are the only lockable top regression risk. Ran an r1(FAIL)-vs-r2(PASS)
committed-artifact diff:

- **The over-drop mechanism.** The task removes the `using_department` feature. The correct edit
  drops the feature-ONLY derived column `department_name` (+ its conditional join) but KEEPS the
  shared base column `department_id` (the solution retains it; other logic uses it). In **r1** the
  solver scrubbed `department_id` too → "has less columns than solution" → both FAILED. In **r2** it
  kept `department_id` → both PASSED. A pure coin-flip on *how far to extend the removal*.
- **Lockability — YES, cleanly expressible.** The boundary "drop the feature-only derived column,
  KEEP the shared base id/fk" is a general, task-agnostic rule. The existing h0045 block already
  states this **in prose** ("Preserve ordinary raw/source attributes…") but carries **no worked
  example**. **Move B = add a before→after skeleton** to the h0045 block making the boundary concrete.

**Finding 5 — Move B is double-duty.** qb002/qb003 are not just a generic regression risk — they
were the *specific cause of r1's shortfall*. Locking them would have made r1 = 34. So Move B both
reduces regression and raises the floor toward a stable 35+, on top of which Move A's +1 reaches a
*robust* 36 rather than a lucky one.

## 5. The selection logic, distilled (reusable after any full run)

1. **Run two draws; decompose the gap.** The cheap draw exposes which "passes" are coin-flips. Never
   reason from the lucky draw alone.
2. **Split the goal into flip + stabilize.** +1 net = (one new flip) − (zero new regressions). On a
   lucky baseline, protecting existing passers is as valuable as adding one.
3. **Flip target = a stable-FAIL cell whose construct is adjacent to a banked lever.** Prefer
   "never-passed (0/N) + same construct as something we already fixed" over a high-headroom cell with
   an unknown construct. Confirm with a committed-artifact forensic before committing. (ana-eng004 ✅;
   ana-eng006 ❌ — same family, different failure modes.)
   ⚠️ **CORRECTION (see §8):** a static "less columns / same error string" forensic is NOT enough to
   call a cell a clean sibling. ana-eng004 looked identical to ana-eng003 but its real fork was one
   layer deeper (a duplicate-join-key retention quirk) — invisible until a real run. Before betting a
   flip target, run ONE real probe draw and read the *exact* committed-vs-solution column/row diff,
   not just the error class.
4. **Regression target = a fragile passer that is BOTH a top risk AND lockable.** Skip the
   unlockable ones (oracle MC like f1011; deep build variance like f1001; package noise like
   asana002). Pick the one with a cleanly expressible correct boundary (qb002/qb003 ✅).
5. **Prefer the minimal edit.** Move A widens one precondition on an existing rule; Move B adds a
   worked example to an existing rule. Neither is a brand-new lever — the cheapest, lowest-bleed form.
6. **Validity check against overfitting:** weight *sibling generalization* (does the rule flip an
   unseen same-construct task?) over raw origin-task flips. Move A literally tests this — it bets the
   ana-eng003 rule generalizes to ana-eng004.

## 6. Honest caveats carried into h0057

- **f1011 is unlockable and props up r2's 35.** It is an oracle multiple-choice coin-flip (~33%
  hist); it will likely wobble on any re-draw. The durable margin must come from Move A's flip +
  Move B's stabilization, NOT from f1011. h0057's GO basis is two-draw expectation + committed
  artifacts, never a single net.
- **Move A bleed risk: LOW-MODERATE.** Widening "single upstream" → "join" is more generative; the
  not-feature-removal guard plus the qb002/qb003 MUST-HOLD canaries are the tripwire (the
  h0045↔h0055 collision pair must still route feature-removal to DROP, not PRESERVE).
- **Move B adds no pass** — it lowers the qb002/qb003 PASS→FAIL rate. Judge it by the committed
  keep-department_id artifact across the two draws, not a single reward.
- **Overfitting honesty:** both moves are general principles (preserve-all-columns;
  drop-feature-keep-base-id), no oracle leak. They sit on the clean end of the general-principle ↔
  edge-case-encoding spectrum (cf. h0054 pit-stop-exclude, the closest-to-the-line lever). See the
  cheating/overfitting discussion captured against h0057.

## 7. Evidence trail

- Two-draw outcomes: `…h0056-…-r1/deff5d8a9c10c92f`, `…h0056-…-r2/2c544ee929c0c02a`; base
  `…h0052-…/dcb1a62ef4066133`. Strict-clean, 48/48 captured, 0 errored.
- Move A forensic: ana-eng004 = dropped-existing-columns (solution `SELECT *`, 22 cols),
  ana-eng006 = mixed (missing-derived + dedup + cascade).
- Move B forensic: qb002/qb003 r1 = OVER-DROP of base `department_id` ("less columns than
  solution"); r2 = kept it. Correct boundary cleanly expressible; h0045 has the prose, lacks the
  example.
- Historical pass rates: flip-map `_artifacts/round1-round2-flipped-task-choice-map.md`.

## 8. Postmortem (2026-06-15) — Move A failed, Move B promoted: what we got wrong and what held

**Result:** h0057 (Move A + Move B) was REJECTED — Move A never flipped ana-eng004 across 4 real-run
revise cycles. Move B was validated (qb002/qb003 held every smoke) and shipped alone as **h0058
(PROMOTED)**: r1=33, r2=35, two-draw mean **34/48** (up from h0056's 33.5); @baseline now
`runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r2/eba9295fda32c05e` = 35/48. **Goal 36
remains open** — the stabilizer banked, the flip did not.

### What we got wrong — the Move-A pre-diagnosis

§3 classified ana-eng004 as "the identical dropped-columns construct as the banked ana-eng003." That
was wrong, and only a real run revealed it:
- Move A **fired and reached the committed SQL** — the worker built the full `fact ⋈ dim` OBT, no
  relevance-prune, `attachments` present. Mechanically the rule worked.
- ana-eng004 still landed **22 columns vs the solution's 23.** The real fork: both upstreams share the
  join key `product_id`, and **the solution keeps BOTH copies** (`i.product_id` AND `p.product_id`).
  The worker did the natural thing — de-duplicated the join key — landing one column short.
- "Preserve every column" prose has no teeth to force keeping a *redundant duplicate* join-key column,
  and 4 cycles of adding teeth (column audits, explicit counts) all failed. Keeping a redundant
  duplicate column is an oracle quirk, not a derivable principle → ana-eng004 is **oracle-blind**, not
  a clean sibling. (h0058 source note: "ana-eng004 oracle-blind, 4 real-run cycles, 4 distinct
  failure modes.")

### What held — the method mostly worked

- **Move B was exactly right** — qb002/qb003 held PASS across every smoke and the promote; the
  keep-base-id worked example is collision-free and raised the two-draw expectation 33.5→34. The
  "stabilize a lockable fragile passer" half of the procedure delivered.
- **The sibling-generalization validity check (step 6) did its job.** ana-eng004 NOT generalizing from
  ana-eng003 is the signal that (a) the preserve-columns rule is a genuine principle (it didn't overfit
  / falsely fire to "pass" ana-eng004), and (b) ana-eng004 needed something non-general — which we then
  correctly declined to encode (the captain cut Move A rather than keep adding edge-case teeth).
- **Splitting flip + stabilize was correct** — because the two were separable, the validated half
  (Move B) shipped immediately instead of being sunk with the failed flip.

### Procedure corrections (fold into §5 for next time)

1. **Step 3 needs a real-run probe, not a static forensic.** "Same error class (less columns)" ≠ "same
   fork." Before committing a flip target, run ONE probe draw and diff the *exact* committed output vs
   the solution (column-by-column / row-by-row), not just the error string. ana-eng004's true miss
   (duplicate-join-key retention) was invisible to the static read.
2. **Add an "oracle-blind" exit.** If the correct output requires a quirk the solver cannot derive
   locally (here: emit a redundant duplicate column), STOP — do not add increasingly specific teeth.
   That drift is exactly the edge-case-encoding line; the captain's 4-cycle cutoff is the right
   instinct, and it should be a named stop rule, not a judgment call.
3. **Separable moves are a feature.** Keep flip and stabilize as independently-shippable edits so a
   validated stabilizer is never orphaned by a failed flip (h0058 is the proof).

### Where this leaves the road to 36

ana-eng004 is reclassified **oracle-blind** (move it out of the "clean flip target" set, alongside
intercom and f1011). The flip target for 36 must be re-picked from the remaining stable-FAIL set using
the **corrected step 3** (real-run probe first). Candidates not yet probed this way: ana-eng007 /
007-medium (still build/rename family but unverified at the column-diff level), f1002 (f1
grain/aggregate), asana004/005 (unread). None should be called "clean" until a probe draw shows a
locally-derivable fork.
