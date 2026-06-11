---
title: Implementation — a coverage-repair worked-example skeleton that pins ALL THREE forks at once (drop the narrowing date-spine predicate, keep COUNT(*) byte-intact, do NOT cross-join the secondary category) in one copyable before→after block
status: hypothesis
kind: hypothesis
source: concept-airbnb009-reproducible-fix (ideate 2026-06-11), grounded in the airbnb009 failed-attempt forensics h0019 (pinned forks #1+#3, left #2 free) / h0042 (pinned #2, left #1+#3 free). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
id: h0046
started: 2026-06-11T00:00:00Z
---

## Hypothesis

`airbnb009` is the date/calendar-spine completeness repair whose correct fix is fully
artifact-proven yet has never reproduced at `trials: 1`. The committed
`models/agg/mom_agg_reviews.sql` passes the hidden `mom_agg_review_date_range` check only when
**three implementation forks all land in the SAME draw**:

1. **Drop the narrowing predicate** `WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE …)` from
   the date CTE so every calendar day is present (the spine half).
2. **Keep `COUNT(*)`** as the aggregate — do NOT "tidy up" to `COUNT(review_cte.REVIEW_DATE)`.
   The forensics proved this is THE discriminator: the column-count rewrite makes the 722
   zero-review days carry `REVIEW_TOTALS=0` instead of the oracle's `1`, breaking the windowed
   `sum(REVIEW_TOTALS)`.
3. **No cross-join** of the secondary category (sentiments) onto every day — let categories
   emerge from the existing `LEFT JOIN` + `GROUP BY`. A `(days × categories)` cross-join
   over-produces rows and breaks the windowed `count(*)`.

The decisive lesson from h0019 and h0042: **pinning one fork at a time cannot bank this target.**
h0019 shipped an anti-cross-join skeleton (forks #1+#3) but left the aggregate line free → at
full the solver "improved" `COUNT(*)`→`COUNT(review_cte.REVIEW_DATE)` and failed. h0042 pinned
`COUNT(*)` via abstract abstain-prose (fork #2) but left the spine/restructure free → at full the
solver rebuilt with a cross-join AND flipped the count back. Each pin narrows the space but leaves
enough free choices that the joint probability of all three at once stays a coin-flip.

**Falsifiable claim (the single README change — Implementation stage only):** replacing the free
degrees of freedom with **one copyable before→after SQL worked-example skeleton that pins all
three forks simultaneously** — drop the one narrowing membership predicate, KEEP the aggregate
expression byte-intact (do not rewrite `COUNT(*)`/`COUNT(col)`/any aggregate while doing a
coverage repair), and KEEP the existing `LEFT JOIN`/`GROUP BY` byte-intact (add no new
cross-join CTE) — will make the committed `mom_agg_reviews.sql` land all three forks in a single
draw, flipping `airbnb009` FAIL→PASS reproducibly, without regressing the canary panel.

This is the h0030/h0019 finding extended: a *copyable skeleton* is the only form that has reliably
REACHED the committed SQL (prose-only h0010/h0016 went inert). h0019's skeleton showed exactly ONE
fork (the anti-cross-join). This hypothesis's net-new bet is that **a skeleton showing all three
forks in one block holds all three under a single draw** — the open question the concept names.

**The single proposed README skeleton (generic identifiers, no target-specifics):**

```text
A coverage repair (missing rows / missing days / a narrowed spine) is a SUBTRACTIVE,
in-place edit. Make exactly these edits and NOTHING ELSE: (1) delete the one narrowing
membership predicate that filters the complete dimension down to keys that already
appear in the fact; (2) leave the aggregate expression BYTE-INTACT — do not rewrite a
COUNT(*) into COUNT(col), or change any SUM/AVG/window, while repairing coverage; (3)
leave the existing join and GROUP BY BYTE-INTACT — do not add a cross join of a
secondary category against the dimension. Let categories emerge per key through the
join the model already has.

BEFORE (the bug + the two over-eager rewrites to AVOID):
    with day_set as (
        select date_col from {{ ref('dimension') }}
        where date_col in (select distinct fact_date from {{ ref('fact_detail') }})  -- the narrowing predicate
    ),
    cats as (select distinct category_col from {{ ref('fact_detail') }}),       -- DO NOT add this
    grid as (select * from day_set cross join cats)                             -- DO NOT add this
    select count(fact.fact_date) as totals                                      -- DO NOT rewrite the aggregate
    from grid left join {{ ref('fact_detail') }} fact on ... group by ...

AFTER (drop the predicate, keep COUNT(*) byte-intact, no cross join):
    with day_set as (
        select date_col from {{ ref('dimension') }}                            -- narrowing predicate DELETED
    )
    select count(*) as totals                                                  -- aggregate UNCHANGED
    from day_set left join {{ ref('fact_detail') }} fact on ... group by ...   -- existing join + group by UNCHANGED
```

## Acceptance criteria

**AC-1 — Exactly the README change; specs differ only in `experiment:` + `solver_workflow:`.**
`diff specs/baseline.yaml specs/h0046-….yaml` shows only `experiment:` + `solver_workflow:`;
the README diff vs `codex-ade-dbt-minimal/README.md` touches only `## Stage: Implementation`
(the single all-three-fork skeleton, inserted after the "...schema patterns." paragraph and
before "Run basic confirmation..."), leaves Exploration/Validation/Finalization and the
dependency/leak-guard prose byte-identical, and references no hidden `AUTO_*`/`solution__*`/
`check_*`/`verifier`/`Got N`/`equality test`/oracle count, no `dim_dates`/`sentiment`/`4508`/
`12278`/`mom_agg` target-specific token, and no `curl`/`wget`/`git clone`/web fetch.
`agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean (`tainted: 0`,
`coverage_missing: 0`), `captured > 0`.

**AC-3 — The decisive read is the committed artifact on ALL THREE forks, not transcript chatter.**
For every `airbnb009` run, read the committed `models/agg/mom_agg_reviews.sql` from the
dispatched-ensign `apply_patch` payload and classify EACH fork independently:
(#1) narrowing predicate gone? (#2) aggregate expression still `COUNT(*)` byte-intact (NOT
`COUNT(review_cte.REVIEW_DATE)` / any column-count)? (#3) no new cross-join CTE; existing
`LEFT JOIN`/`GROUP BY` intact? A flip is credited only when all three are simultaneously
satisfied AND the verifier passes. Transcript claims do not count.

**AC-4 — Reproducibility, judged honestly against the ~17% base rate (the h0042 trap).**
airbnb009 passes only ~2/12 (~17%) across the full run-dirs on disk. Per the standing
single-trial decision, a clean focused-smoke streak is NOT a flip predictor. So smoke must run
airbnb009 as **≥3 independent focused repeats** (fresh context / seed-perturbed to bust the
content-addressed run-dir cache, per the h0042 run-mechanics note), and GO requires **all
repeats land all three forks (AC-3) + verifier pass + clean audit**. State up front that even a
perfect three-fork pin only raises the per-draw probability — the full verdict is provisional
pending the 48-task run, and a single full FAIL where the committed artifact shows all three
forks landed is the honest signal that the mechanism works but `trials: 1` cannot bank it.

**AC-5 — No regression-canary loss.** All `@baseline` passers in the smoke panel must stay PASS.
Any canary regression is a NO-GO unless artifact analysis proves it is unrelated single-trial
variance and the captain explicitly accepts the risk.

**Smoke gate:** target `ade-bench-airbnb009` + the G8 canary panel (`ade-bench-airbnb001`,
`ade-bench-asana001`, `ade-bench-ana-eng001`, `ade-bench-f1007`, `ade-bench-quickbooks002`) +
the ≥3 focused airbnb009 repeats. GO requires the three-fork artifact read on every repeat and
zero canary regression before full.

## Target dataset

Primary target: `ade-bench-airbnb009` — the one task where all three forks and the intended
mechanism are artifact-proven. The rule is **generative** (it fires on any coverage repair), so
per gatekeeper G8 the smoke carries a cross-family regression-canary panel — one `@baseline`
passer per non-target family (`airbnb001`, `asana001`, `ana-eng001`, `f1007`, `quickbooks002`;
no intercom passer exists). Same structural G8 limit as h0019/h0042: only one airbnb non-target
passer and no second coverage-repair passer to recruit as a perturbable canary — accept the
residual full-scale blind spot.

## Honest tension with the standing decisions

- **`trials: 1` / no best-of-N** (MEMORY `ade-bench-single-trial-judge-by-artifact`). A ~17% cell
  is hard to bank in one draw; a three-fork skeleton can only RAISE the per-draw probability, not
  make it deterministic. If the committed artifact lands all three forks but the single scored
  draw still falls on a residual free choice the skeleton does not pin, this is un-promotable by
  construction — exactly as h0019/h0042 were. The judge-by-artifact rule (AC-3) is how we tell
  "mechanism works but unbankable" apart from "mechanism inert."
- **The concluded flip-portfolio wall** (MEMORY `ade-bench-oracle-program-concluded`). airbnb009 is
  the last open flip target; the box is closed at the lever level. This is filed as a genuinely
  NEW mechanism class (pin-all-three-forks-in-one-skeleton), distinct from h0019 (one-fork
  skeleton) and h0042 (one-fork abstain-prose). If smoke shows the committed SQL still breaks any
  one fork, it joins the wall and is REJECTED with no iteration (CAPPED one-shot).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change.
