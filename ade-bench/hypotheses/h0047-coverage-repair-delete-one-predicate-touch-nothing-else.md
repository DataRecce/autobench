---
title: Implementation — frame a missing-rows coverage repair as a STRICTLY subtractive single-predicate deletion ("the only edit is to delete the one narrowing filter; touch nothing else — not the aggregate, not the joins"), removing every free fork instead of steering each
status: hypothesis
kind: hypothesis
source: concept-airbnb009-reproducible-fix (ideate 2026-06-11), candidate mechanism (d.2) "remove the free degrees of freedom rather than steer each". Distinct from h0046 (worked-example skeleton) and from h0019/h0042 (one-fork pins). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
id: h0047
started: 2026-06-11T00:00:00Z
---

## Hypothesis

airbnb009's recurring failure on the `mom_agg_review_date_range` check is **over-editing**, not
under-reaching. The @baseline solver already finds the bug location and removes the narrowing
date-spine predicate unprompted; it then loses by ALSO doing one of two over-eager cleanups the
oracle rejects: rewriting `COUNT(*)`→`COUNT(review_cte.REVIEW_DATE)` (the proven discriminator —
zeros the 722 no-review days) and/or rebuilding the model with a `(days × sentiments)` cross-join.
Both h0019 and h0042 tried to STEER the freed forks (anti-cross-join skeleton; preserve-the-metric
prose) and both lost when the solver exercised a fork the rule left open.

**Falsifiable claim (the single README change — Implementation stage only):** instead of steering
each fork, **remove the invitation to touch them at all** by reframing a coverage repair as a
strictly subtractive, single-predicate deletion. The rule states: when a model is missing rows
because a complete dimension is narrowed by a membership/filter predicate, the ONLY edit is to
**delete that one predicate**; you MUST NOT touch the aggregate expression, the joins, the
`GROUP BY`, or the model structure in the same edit. If you believe a further change is needed,
that is a SEPARATE task — for THIS repair, the minimal diff is a single deleted line. This
collapses the three forks to one decision (delete-the-line) by forbidding the over-edits that
constitute forks #2 and #3, rather than enumerating the right shape for each.

The bet that differs from h0046: a "change exactly one line, nothing else" **negative
constraint** is honoured more reliably than a "here is the correct three-fork shape to copy"
**positive skeleton**, because the recurring failure is over-eager cleanup and the cleanest way to
suppress cleanup is to deny that any edit beyond the deletion is in scope. The risk this tests
(stated by the concept): whether the solver honours "delete one line, touch nothing else" or
still over-edits — the open empirical question on this cell.

**The single proposed README text (generic, no target-specifics):**

```text
When a model is missing rows because a complete dimension (a date/calendar dimension,
a key dimension, a reference list) is narrowed by a membership or filter predicate that
restricts it to keys already present in a fact table, the coverage repair is STRICTLY
SUBTRACTIVE: the only edit is to DELETE that one narrowing predicate. In the same edit,
do NOT touch the aggregate expression (do not rewrite COUNT(*)/COUNT(col)/SUM/AVG or any
window), do NOT add or restructure joins (no cross join of a secondary category against
the dimension), and do NOT change the GROUP BY. The correct fix is a single deleted line;
the existing join and GROUP BY already let categories emerge per key. If you think a
further change is warranted, treat it as a separate concern and do not bundle it into this
coverage repair — for this repair the diff must be exactly the one deletion.
```

## Acceptance criteria

**AC-1 — Exactly the README change; specs differ only in `experiment:` + `solver_workflow:`.**
`diff specs/baseline.yaml specs/h0047-….yaml` shows only `experiment:` + `solver_workflow:`;
the README diff vs `codex-ade-dbt-minimal/README.md` touches only `## Stage: Implementation`
(the single subtractive-deletion rule, inserted after "...schema patterns."), leaves the other
stages and the dependency/leak-guard prose byte-identical, references no hidden `AUTO_*`/
`solution__*`/`check_*`/`verifier`/`Got N`/`equality test`/oracle count and no
`dim_dates`/`sentiment`/`mom_agg`/numeric-oracle token, and no `curl`/`wget`/`git clone`/web
fetch. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit** (`tainted: 0`,
`coverage_missing: 0`, `captured > 0`) on the same run-dir.

**AC-3 — Decisive read = the committed artifact on all three forks (AC-3 of h0046, verbatim
criteria).** For each airbnb009 run, read the committed `mom_agg_reviews.sql` from the
`apply_patch` payload and confirm the diff is the single predicate deletion: (#1) narrowing
predicate deleted, (#2) aggregate byte-intact `COUNT(*)`, (#3) no cross-join / joins+GROUP BY
intact. ADDITIONALLY classify the diff SIZE — the distinctive prediction of THIS rule is a
**one-line (single-hunk, deletion-only) diff**; a multi-line restructure means the
"touch-nothing-else" constraint was not honoured even if the verifier happens to pass.

**AC-4 — Reproducibility judged against the ~17% base rate.** Same protocol as h0046 AC-4: smoke
runs airbnb009 as ≥3 seed-perturbed focused repeats; GO requires every repeat to be the
single-predicate-deletion diff (AC-3) + verifier pass + clean audit. The full verdict is
provisional pending the 48-task run; a full FAIL whose committed artifact is nonetheless the
clean one-line deletion is the honest "mechanism works, `trials: 1` cannot bank it" signal.

**AC-5 — No regression-canary loss** (same panel + rule as h0046).

**Smoke gate:** `ade-bench-airbnb009` + G8 canary panel (`airbnb001`, `asana001`, `ana-eng001`,
`f1007`, `quickbooks002`) + ≥3 focused airbnb009 repeats. GO requires the one-line-deletion
artifact read on every repeat and zero canary regression.

## Target dataset

Primary target: `ade-bench-airbnb009`. Generative (fires on any missing-rows coverage repair), so
the smoke carries the cross-family canary panel above (one `@baseline` passer per non-target
family; no intercom passer exists). Same structural G8 limit as h0019/h0042 — accept the residual
full-scale blind spot.

## Why this is a distinct mechanism class (not a re-walk of h0019/h0042/h0046)

- vs **h0019** (anti-cross-join skeleton): h0019 pinned forks #1+#3 by showing the right join
  shape; it said nothing about the aggregate, so the solver was free to rewrite `COUNT(*)`. This
  rule pins all three by forbidding ANY edit beyond the deletion — the aggregate is protected by
  the negative constraint, not by a positive shape.
- vs **h0042** (preserve-the-metric abstain-prose): h0042 pinned only fork #2 ("don't change
  COUNT/SUM/AVG") and left the spine/restructure free, so the solver rebuilt with a cross-join.
  This rule forbids the restructure too, in the same sentence.
- vs **h0046** (positive three-fork skeleton): h0046 shows the correct three-fork shape to COPY;
  this rule denies that any edit beyond the deletion is in scope (a NEGATIVE/remove-the-DOF
  framing). They are the two mechanism classes the concept names at (d) — a head-to-head: does a
  copyable correct-shape or a strict do-nothing-else constraint bank the multi-fork target?

## Honest tension with the standing decisions

- **`trials: 1`** (MEMORY `ade-bench-single-trial-judge-by-artifact`): a ~17% cell can only have
  its per-draw probability raised, not made deterministic. The recurring over-edit is the variance
  source; if the negative constraint genuinely suppresses over-editing the per-draw probability
  could clear ~50%, but that is exactly what the ≥3-repeat smoke + artifact read must demonstrate,
  with the full verdict provisional. Un-promotable by construction if the constraint is honoured
  but a residual free choice still decides the scored draw.
- **The concluded flip-portfolio wall** (MEMORY `ade-bench-oracle-program-concluded`): filed as a
  NEW mechanism class (remove-the-DOF negative framing), not another single-fork variant. If smoke
  shows the solver still over-edits (multi-line restructure / aggregate rewrite / cross-join), the
  "touch-nothing-else" framing is REJECTED as not honoured — CAPPED one-shot, no iteration.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change.
