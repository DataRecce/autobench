# Bug-Type Taxonomy — what's broken, and what we've tried

The standing list of **bug types** we use to classify ade-bench `@baseline` failures, and the
hypotheses that have attacked each one. This is the "what have we tried" board — **keep it
updated** as hypotheses conclude and new failure clusters are found.

**Umbrella fact:** all 17 `@baseline` failures (31/48 pass, run `622bdedac572b479`) are
**false-greens** — the solver's own check reports clean (`actual_pass=10/10`) while the hidden
oracle re-runs the `AUTO_*` / `check_*` tests against `solution__*` seeds and finds the answer
wrong. Glossary: `term-table.md`.

> **Provenance:** the per-task rows below are read directly from each failing cell's hidden-oracle
> output (`runs/ade-bench-baseline/622bdedac572b479/ade-bench-<task>__*/verifier/test-stdout.txt`,
> the section after the solver's false-green self-check). These signatures are ground truth and
> supersede the coarser clustering in `concept-resolve-uncovered-false-greens.md` (see Corrections).

## Authoritative per-task ground truth (all 17 failures)

| Task | Failing oracle test | Signature | Bug type |
|---|---|---|---|
| asana004 | `AUTO_int_asana__project_user_agg_equality` | `Got 3` | grain (entity spine) |
| asana005 | `AUTO_int_asana__project_user_agg_equality` | `Got 3` | grain (entity spine) |
| asana005-hard | `AUTO_int_asana__project_user_agg_equality` | `Got 3` | grain (entity spine) |
| intercom001 | `AUTO_intercom__threads_equality` | `Got 7` | grain (entity spine) |
| intercom002 | `AUTO_intercom__threads_equality` + `…conversation_metrics_equality` | `Got 7` ×2 | grain (entity spine) |
| intercom003 | `AUTO_intercom__conversation_metrics_equality` | `Got 7` | grain (entity spine) |
| airbnb009 | `mom_agg_review_date_range` | `Got 1` — "a row for every day; some days missing" | grain (date/calendar spine) |
| ana-eng004 | `AUTO_obt_product_inventory_equality` | "has less columns" | width |
| f1002 | `AUTO_most_podiums_equality` | "has less columns" | width |
| ana-eng006 | `AUTO_dim_products` + `AUTO_obt_product_inventory` (width) **and** `AUTO_fact_inventory_equality` `Got 204` | mixed | width ×2 **+** value divergence |
| ana-eng007 | `AUTO_dim_products_equality` | `Got 5` | value divergence |
| ana-eng007-medium | `AUTO_dim_products_equality` | `Got 5` | value divergence |
| f1006 | `AUTO_constructor_points_equality` | `Got 2` | value divergence |
| airbnb007 | `daily_agg_nps_reviews_equality_with_tolerance` | `Got 4` | tolerance-band divergence |
| asana002 | `AUTO_asana__task_equality` | `Got 2` (fixed by `::timestamp` cast) | type/contract mismatch |
| quickbooks001 | 3× `stg_quickbooks__*` **existence + equality** | `Got 1` ×6 (models absent) | incomplete deliverable / missing models |
| f1011 | `check_option_b` | `Got 1` | analytical-answer guess |

## The board (bug types → hypotheses)

| # | Bug type | What goes wrong (plain) | Oracle signature | Tasks | Hypotheses | Status |
|---|---|---|---|---|---|---|
| 1 | **Grain / missing rows** — wrong or incomplete spine | built off the child/wrong table so parent (or date) rows with no children silently drop | small `Got N` on an `*_agg`/entity/date model | **1a entity:** asana004, asana005, asana005-hard, intercom001, intercom002, intercom003 · **1b date-spine:** airbnb009 | h0010 (prose) → h0016 (worked-example) for 1a; **1b uncovered** | **REJECTED** 0/4 (1a); 1b not yet attacked |
| 2 | **Width / missing columns** | hand-picked a column subset, not the full output contract | "has less columns than `solution__`" | ana-eng004, f1002, ana-eng006 (2 models) | h0011 (worked-example) | **REJECTED** 0/3 |
| 3 | **Value divergence** — shape right, numbers wrong | right rows & columns, wrong values; only an *independent* recompute catches it | `Got N` on a computed metric | ana-eng007, ana-eng007-medium, f1006, ana-eng006 (`fact_inventory`) | h0012 (independent recompute) | propose |
| 3★ | **↳ Large-magnitude / join fan-out** *(candidate sub-type)* | a join multiplies rows (double-count) → big row delta, not a subtle value error | very large `Got N` (e.g. `Got 204`) vs grain's 3–7 | ana-eng006 (`fact_inventory`) | — (SQL-unconfirmed; verify before filing) | open |
| 4 | **Tolerance-band divergence** *(NEW)* | numbers are close but fall outside the test's allowed tolerance (rounding / float / method) | test named `*_equality_with_tolerance`, `Got N` | airbnb007 | **uncovered** | open |
| 5 | **Type / contract mismatch** | values "right" but column type/representation differs (e.g. text vs `timestamp`) | `Got N`, fixed by a `::type` cast | asana002 | h0009 (package fidelity) — the loop's **one win** | +1 smoke / −1 full |
| 6 | **Incomplete deliverable / missing models** | compiles green so solver stops; graded models never built | `*_existence` tests fail (models absent) | quickbooks001 (also ana-eng007-medium per re-audit; see Corrections) | h0013 (enumerate), h0015 (copy package) | propose / hypothesis |
| 7 | **Analytical-answer guess** | answer-style deliverable includes an option on plausibility, unverified | `check_option_*` fails | f1011 | h0014 (per-claim evidence) | hypothesis |

## Read the bug type straight from the oracle output

The hidden-oracle test name + reason tells you the type without reading SQL:

- `*_existence` fails → **missing model** (#6).
- "has less columns than `solution__`" → **width** (#2).
- `*_equality_with_tolerance` `Got N` → **tolerance-band** (#4).
- `mom_agg` / `*_date_range` / "rows missing for some days" → **date-spine grain** (#1b).
- small `Got N` (3–7) on an `*_agg`/entity model → **entity grain** (#1a).
- moderate `Got N` on a computed metric → **value divergence** (#3); **very large `Got N`** → suspect **fan-out** (#3★).
- `Got N` that disappears with a `::type` cast → **type/contract** (#5).
- `check_option_*` → **analytical guess** (#7).

## Corrections from the ground-truth audit (important for the captain)

The original `concept-resolve-uncovered-false-greens.md` clustering was coarser and partly wrong;
the @baseline oracle output corrects it:

- **asana005-hard is GRAIN, not value divergence.** Same test and magnitude as asana004/005
  (`AUTO_int_asana__project_user_agg_equality`, `Got 3`) — it belongs in h0010/h0016's family
  (it just wasn't in their smoke set).
- **airbnb009 is date-spine GRAIN, not value divergence.** The task literally says "there should
  be a row for every day; some days are missing" — a missing-rows/wrong-spine bug on the calendar,
  conceptually the same as #1a but on a date spine. Fix shape = build from a complete date spine
  and LEFT JOIN.
- **airbnb007 is tolerance-band (#4), its own type** — the test is `*_with_tolerance`.
- **ana-eng006 is MIXED** — two width errors (dim_products, obt_product_inventory) **plus** a real
  value divergence (`fact_inventory`, `Got 204`). It is not a pure value-divergence task.
- **ana-eng007-medium failed on `Got 5` (value divergence) at @baseline**, not "less columns" as
  h0011's premise recorded — so h0011 partly aimed its width worked-example at a non-width task,
  which helps explain its 0/3.
- **Net effect on h0012:** its "6 value-divergence tasks" (ana-eng006, ana-eng007, airbnb007,
  asana005-hard, f1006, airbnb009) really resolve to **~3 true value-divergence** (ana-eng007,
  ana-eng007-medium, f1006) + ana-eng006's `fact_inventory` + **1 tolerance** + **1 date-spine
  grain** + **1 entity grain**. The independent-recompute lever should be re-scoped to the genuine
  value-divergence/fan-out tasks before spending budget.

## Per-type lessons

- **#1 Grain** — most-studied; prose (h0010) vs worked-example (h0016) head-to-head. Lesson: a
  copyable example *reaches* the committed SQL where prose is inert, but "reaches" ≠ "passes"
  (0/4). New: **1b date-spine** (airbnb009) is an untried, well-scoped variant — the fix is a
  known shape (complete calendar spine + LEFT JOIN).
- **#3 / #3★** — `fact_inventory`'s `Got 204` is an order of magnitude above the grain failures'
  3–7; that pattern usually means a join fanned out (double-count), a different mechanism from a
  subtle value error. Confirm in the committed SQL before treating fan-out as its own type.
- **#4 Tolerance** — distinct because the answer is *nearly* right; the lever is about
  rounding/precision/method alignment, not structure.
- **#5 Type/contract** — the loop's **only win** (asana002, `due_at::timestamp`) — a mechanical
  cast that *landed*; but it regressed at full scale (convention-bleed cost f1/quickbooks).
- **#6 Missing models** — the `*_existence` failures are the unambiguous tell; quickbooks001's
  3 `stg_*` models exist in the installed package (h0015's copy-the-package angle).

## Meta-pattern (the recurring lesson)

README-prose / worked-example levers have largely hit a **ceiling** at gpt-5.5 / `reasoning_effort:
xhigh`: a verbatim copyable skeleton changes the committed SQL yet still flips zero targets,
because the residual gap is task-specific correctness the README can't supply without leaking.
Scoreboard: h0008 0/7 · h0009 +1/−1 · h0010 0/4 · h0011 0/3 · h0016 0/4. Open non-prose
directions: capability lever (stronger model/effort), multi-sample-and-select (attack run-to-run
variance), independent-invariant verification (#3's lever, re-scoped per the Corrections).

---

## Maintenance — keep this current

Update this file whenever:
- **A hypothesis concludes** → change its row's Status (e.g. `propose` → `REJECTED 0/N` /
  `PROMOTED`) and add the one-line lesson to Per-type lessons.
- **A new failure cluster / sub-type is found** → add a row (next # or a `★` sub-type), with
  tasks + oracle signature; link the concept/hypothesis that surfaced it.
- **A task is re-classified** (as happened in Corrections) → fix the per-task table + the board +
  note it under Corrections.
- **The scoreboard / meta-pattern shifts** → update the Meta-pattern paragraph.

Ground every row in the actual oracle output
(`…/ade-bench-<task>__*/verifier/test-stdout.txt`, the post-self-check section) — never invent
task slugs, `AUTO_*` names, or `Got N`. The `explain-hypotheses` skill reads this file as its
taxonomy source.
