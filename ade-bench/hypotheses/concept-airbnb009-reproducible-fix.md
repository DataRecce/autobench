---
title: Make airbnb009 reliably PASS — pin ALL THREE load-bearing implementation forks at once (full dim_dates calendar spine, keep COUNT(*), no cross-join) instead of one fork at a time
status: ideate
kind: concept
source: captain request 2026-06-11 after h0042 REJECTED; grounded in the airbnb009 failed-attempt evidence h0019/h0041/h0042.
id: concept-airbnb009-reproducible-fix
started: 2026-06-11T02:37:14Z
---

## Direction

airbnb009 is the one task where the correct fix is fully artifact-proven yet has **never been
made reproducible at `trials: 1`**. h0019 flipped it at smoke and banked it once (the old
@baseline promote), but the standalone full did not reproduce; h0041 (observe-only) saw it flip
up then offset down as pure variance; h0042 pinned `COUNT(*)` and got a clean 3/3 focused smoke,
then at full reverted to the exact wrong fork. The pattern across all three is the same: **the
solver reaches the right model and the right neighbourhood, but a low-base-rate combination of
implementation choices decides the hidden result, and pinning one choice at a time just displaces
the variance to the choices left free.** This concept is the direction to break that — a mechanism
that removes ALL the free degrees of freedom at once.

**(a) airbnb009 needs THREE load-bearing implementation forks RIGHT AT ONCE.** The committed
`models/agg/mom_agg_reviews.sql` only passes the hidden `mom_agg_review_date_range` check when all
three of these land together:

1. **Date-spine coverage** — drop the narrowing predicate `WHERE DATE_ACTUAL IN (SELECT DISTINCT
   REVIEW_DATE …)` so every calendar day is present. (Both the smoke-pass full-`dim_dates` form
   and a self-bounded `BETWEEN MIN..MAX(review_date)` span pass *within the test window*, because
   the test's own `WHERE` windows the calendar — the span is not the discriminator, as the h0019
   three-run forensics proved. What matters is the narrowing filter is gone.)
2. **Keep `COUNT(*)`** as the aggregate — do NOT "tidy up" to `COUNT(review_cte.REVIEW_DATE)`. The
   oracle uses `COUNT(*)`; the column-count rewrite makes the 722 zero-review days carry
   `REVIEW_TOTALS=0` instead of the oracle's `1`, so `sum(REVIEW_TOTALS)` misses `12196400`.
3. **No cross-join** of sentiments onto every day — let sentiments emerge from the existing
   `LEFT JOIN` + `GROUP BY`. A `(days × sentiments)` cross-join over-produces rows and breaks the
   windowed `count(*) = 12278`.

Miss any one of the three and the verifier returns `Got 1` → reward 0. The h0019 wrong fork and
the h0042 full both got #1 right and broke #2 (and #2 dragged in a #3 restructure).

**(b) It is reachable but a coin-flip at `trials: 1`.** Across the full run-dirs on disk airbnb009
passes only **~2/12 (~17%)** of the time. It is genuinely solvable by the current solver with the
current README — it banks when the gpt-5.5 draw happens to get all three forks right — but the
modal single-trial draw fails. So this is NOT an oracle-blocked task (the correct fix is locally
authorable, no hidden count needed for forks #2/#3); it is a **low-base-rate, multi-fork
reproducibility** problem.

**(c) WHY prior mechanisms failed: each PINNED ONE FORK and left the others free, so variance just
displaced.** h0019 pinned the date-spine repair / anti-cross-join shape (forks #1 + #3) but left
the aggregate line (#2) free → at full the solver "improved" `COUNT(*)`→`COUNT(review_date)` and
failed. h0042 pinned `COUNT(*)` (#2) but left the spine/restructure choice free → at full the
solver rebuilt the model with a cross-join and ALSO flipped the count back to the wrong fork. The
structural lesson: **pinning one line at a time cannot bank a multi-fork low-base-rate target** —
each fix narrows the space but leaves enough free choices that the joint probability of landing all
three at once stays a coin-flip. A clean N/N focused smoke on a ~17%-pass cell is a favorable-tail
streak, not a guarantee (the h0042 trap; MEMORY `ade-bench-single-trial-judge-by-artifact`).

**(d) Candidate NEW mechanisms to explore at ideate** (plain-English directions, NOT pre-written
hypotheses — ideate fans these out and gatekeeps each):

- **A complete copyable BEFORE/AFTER skeleton that pins ALL THREE forks simultaneously.** Where
  h0019 shipped a generic anti-cross-join skeleton (one fork) and h0042 shipped abstract
  abstain-prose (one fork), a single worked-example block that shows the exact minimal edit —
  drop the narrowing predicate, keep `COUNT(*)` byte-intact, and the existing `LEFT JOIN`/`GROUP
  BY` byte-intact (no new cross-join CTE) — gives the solver one path to copy rather than three
  independent decisions to re-derive. The h0030/h0019 finding is that a *copyable skeleton* is the
  only form that has reliably REACHED the committed SQL; the open question is whether a skeleton
  that pins three lines at once can hold all three under a single draw.
- **A mechanism that removes the free degrees of freedom rather than steering each.** E.g. frame
  the task as a strictly subtractive single-predicate deletion ("the ONLY edit is to delete the
  one narrowing `WHERE` line; touch nothing else — not the aggregate, not the joins"), so the
  solver has no invitation to rewrite the count or restructure the joins at all. The risk to test:
  whether a "change exactly one line, nothing else" framing is honoured or whether the solver
  still over-edits (the recurring failure on this cell is over-eager cleanup, not under-reaching).

**Honest tension with the standing decisions.** This direction collides with two hard constraints,
and ideate must confront them, not paper over them:

- **`trials: 1` / no best-of-N** (MEMORY `ade-bench-single-trial-judge-by-artifact`). A ~17% cell
  is, by construction, hard to bank in one draw — even a perfect three-fork pin only raises the
  per-draw probability, it cannot make a single trial deterministic. If the mechanism cannot push
  the single-draw pass probability decisively above ~50%, the flip remains **un-promotable by
  construction** under `trials: 1`, exactly as h0019 and h0042 were. Any hypothesis derived here
  must state up front how it would be judged banked under one trial (committed-artifact proof of
  all three forks on the scored draw + a clean canary panel), and accept that a streaky smoke is
  not evidence.
- **The concluded flip-portfolio wall** (MEMORY `ade-bench-oracle-program-concluded`). airbnb009 is
  the last open flip target and the program already concluded that the box is closed at the lever
  level; 75% needs a benchmark-design change, not a lever. So a candidate mechanism here is worth
  ideating ONLY if it is a genuinely new *mechanism class* (pin-all-forks-at-once / remove-DOF),
  not another single-fork prose or skeleton variant that re-walks the same wall. If ideate cannot
  name a mechanism that plausibly clears the single-draw probability bar, the honest outcome is to
  leave this concept as documented direction and not fan it into doomed variants — escalate to the
  captain as a strategy call instead.

The deliverable of a future ideate pass is one or more falsifiable `h<NNNN>` hypotheses, each ONE
solver-README change forking the current `@baseline`, each naming airbnb009 as the artifact-proven
target, each stating the three-fork acceptance condition (committed SQL: narrowing predicate gone,
`COUNT(*)` intact, no cross-join) and a cross-family regression canary panel (the rule is
generative — the h0042/h0019 G8 gap means the smoke verdict is provisional pending full).

## Stage Report: ideate

- DONE: Write 2-5 hypothesis entities (h<NNNN>-<slug>.md, status: hypothesis), each a SINGLE
  falsifiable solver-README change with named target datasets (airbnb009 + perturbable canaries)
  and acceptance criteria.
  Wrote 3 hypotheses: `h0046-coverage-repair-all-three-forks-worked-skeleton.md`,
  `h0047-coverage-repair-delete-one-predicate-touch-nothing-else.md`,
  `h0048-exploration-protect-list-load-bearing-lines-before-coverage-edit.md`. Each = one
  README change forking `@baseline` (codex-ade-dbt-minimal), names `ade-bench-airbnb009` as the
  artifact-proven target + the G8 cross-family canary panel (airbnb001/asana001/ana-eng001/
  f1007/quickbooks002; no intercom passer exists), and carries AC-1..AC-5 incl. the three-fork
  committed-artifact read (AC-3) and the ~17%-base-rate >=3-repeat reproducibility gate (AC-4).
- DONE: Each hypothesis must operationalize the concept's core bet: pin ALL THREE load-bearing
  forks at once (full date-spine coverage / keep COUNT(*) / no cross-join), not one fork at a
  time — the one-at-a-time approach already failed (h0019/h0041/h0042).
  All three pin every fork simultaneously, via THREE DISTINCT mechanism classes (head-to-head):
  h0046 = Implementation positive worked-example skeleton showing all three forks in one copyable
  before->after block; h0047 = Implementation NEGATIVE remove-the-DOF constraint ("delete the one
  narrowing predicate; touch nothing else — not the aggregate, not the joins"); h0048 =
  Exploration pre-edit PROTECT-LIST that commits the aggregate/join/GROUP BY lines as off-limits
  before the edit. Each entity has a "Why this is a distinct mechanism class" section contrasting
  it against h0019 (forks #1+#3, left #2 free), h0042 (fork #2, left #1+#3 free), and its siblings,
  so none re-walks the concluded single-fork wall.

### Summary

Fanned the concept into 3 falsifiable single-README-change hypotheses (h0046/h0047/h0048), each
operationalizing the pin-all-three-forks-at-once bet through a different mechanism class — a
positive three-fork skeleton (h0046, Implementation), a negative do-nothing-else single-predicate
constraint (h0047, Implementation), and a pre-edit protect-list of load-bearing lines (h0048,
Exploration). Every entity names airbnb009 as the artifact-proven target, carries the G8
cross-family canary panel, judges the flip by the committed-artifact three-fork read (not
transcript chatter), and confronts both standing constraints head-on: the `trials: 1` ~17%-base-
rate un-promotable-by-construction risk (AC-4: >=3 seed-perturbed focused repeats, full verdict
provisional) and the concluded flip-portfolio wall (each filed as a genuinely new mechanism class,
CAPPED one-shot if a fork breaks at smoke). Concept ready to advance to `expanded` (FO performs the
frontmatter transition).
