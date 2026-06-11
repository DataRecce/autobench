---
title: Exploration — before editing a missing-rows coverage repair, record a PROTECT-LIST of the model's load-bearing aggregate/join/GROUP BY lines and treat them as off-limits, so the implementation edit cannot silently rewrite the forks the spine repair leaves free
status: hypothesis
kind: hypothesis
source: concept-airbnb009-reproducible-fix (ideate 2026-06-11), operationalizing "remove ALL the free degrees of freedom at once" at the EXPLORATION stage (commit-the-protected-lines before the edit). Distinct stage + mechanism from h0046 (Implementation skeleton) / h0047 (Implementation negative constraint) / h0019 / h0042. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
id: h0048
started: 2026-06-11T00:00:00Z
---

## Hypothesis

The airbnb009 failure pattern is that the solver decides DURING implementation to "improve" lines
the coverage repair should leave alone — it rewrites `COUNT(*)`→`COUNT(review_cte.REVIEW_DATE)`
and/or restructures with a cross-join, both of which the oracle rejects. h0019/h0042/h0046/h0047
all act at the Implementation edit. This hypothesis acts one stage earlier: it makes the solver
**commit, during Exploration, to a protect-list of the model's load-bearing lines** before it
forms the edit, so by the time it implements, the aggregate and join lines are already declared
off-limits and the "tidy-up" impulse has no opening.

**Falsifiable claim (the single README change — Exploration stage only):** adding one Exploration
rule that, when the task is a missing-rows / coverage repair on an existing model, requires the
solver to (a) locate the single narrowing predicate that causes the missing rows, and (b) write
down a PROTECT-LIST of the model's existing aggregate expressions (`COUNT`/`SUM`/`AVG`/window),
join clauses, and `GROUP BY` — the lines that define the metric's meaning — and carry the rule
forward that the coverage repair changes ONLY the narrowing predicate and leaves every
protect-listed line byte-intact. Naming the load-bearing lines BEFORE the edit pins all three
forks at the planning step (the predicate to drop is identified; the aggregate and joins are
pre-committed as untouchable), so the implementation has no free fork left to flip.

The bet that differs from h0046/h0047: the over-edit is a planning-time decision, so the
intervention that suppresses it most reliably is a planning-time **commitment** (write the
protect-list before editing), not an implementation-time skeleton or constraint. This sits in the
Exploration stage, which the @baseline README already asks to "record suspected task type,
affected files/models, baseline errors" — this rule extends that recording to a protect-list. The
risk this tests: whether an Exploration-stage protect-list survives into the Implementation edit
or is forgotten once the solver starts writing SQL (the cross-stage-memory question).

**The single proposed README text (Exploration stage, generic, no target-specifics):**

```text
If a baseline probe shows a model is MISSING ROWS because a complete dimension (a date
dimension, key dimension, or reference list) is narrowed by a membership/filter predicate,
record TWO things before editing: (1) the single narrowing predicate to delete, and (2) a
PROTECT-LIST naming the model's existing aggregate expressions (COUNT/SUM/AVG/window
functions), join clauses, and GROUP BY — these define the metric's meaning and must stay
BYTE-INTACT through a coverage repair. Carry forward that the repair changes ONLY the
narrowing predicate; every protect-listed line is off-limits. A coverage repair that also
rewrites an aggregate or adds a cross join is changing the metric, not repairing coverage.
```

## Acceptance criteria

**AC-1 — Exactly the README change; specs differ only in `experiment:` + `solver_workflow:`.**
`diff specs/baseline.yaml specs/h0048-….yaml` shows only `experiment:` + `solver_workflow:`;
the README diff vs `codex-ade-dbt-minimal/README.md` touches only `## Stage: Exploration` (the
single protect-list rule), leaves Implementation/Validation/Finalization and the
dependency/leak-guard prose byte-identical, references no hidden `AUTO_*`/`solution__*`/
`check_*`/`verifier`/`Got N`/`equality test`/oracle count and no `dim_dates`/`sentiment`/`mom_agg`
target token, and no `curl`/`wget`/`git clone`/web fetch. `agent.kind: spacedock_solver`,
`runtime: codex`, `trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit** (`tainted: 0`,
`coverage_missing: 0`, `captured > 0`) on the same run-dir.

**AC-3 — Decisive read = the committed artifact on all three forks.** For each airbnb009 run,
read the committed `mom_agg_reviews.sql` from the `apply_patch` payload and confirm: (#1)
narrowing predicate gone, (#2) aggregate byte-intact `COUNT(*)` (NOT a column-count), (#3) no
new cross-join / joins + GROUP BY intact. A flip is credited only when all three hold AND the
verifier passes. Where the worker session captures Exploration notes, ALSO check whether a
protect-list was actually recorded (mechanism-fired evidence) vs the rule being acknowledged and
skipped — this distinguishes "protect-list held the forks" from "incidental clean edit."

**AC-4 — Reproducibility judged against the ~17% base rate.** Same protocol as h0046 AC-4: smoke
runs airbnb009 as ≥3 seed-perturbed focused repeats; GO requires every repeat to land all three
forks (AC-3) + verifier pass + clean audit. Full verdict provisional pending the 48-task run; a
full FAIL whose committed artifact nonetheless shows all three forks intact is the honest
"mechanism works but `trials: 1` cannot bank it" signal.

**AC-5 — No regression-canary loss** (same panel + rule as h0046).

**Smoke gate:** `ade-bench-airbnb009` + G8 canary panel (`airbnb001`, `asana001`, `ana-eng001`,
`f1007`, `quickbooks002`) + ≥3 focused airbnb009 repeats. GO requires the three-fork artifact read
on every repeat and zero canary regression.

## Target dataset

Primary target: `ade-bench-airbnb009`. Generative (fires on any missing-rows coverage repair on an
existing model), so the smoke carries the cross-family canary panel above (one `@baseline` passer
per non-target family; no intercom passer exists). Same structural G8 limit as h0019/h0042 —
accept the residual full-scale blind spot.

## Why this is a distinct mechanism class

- vs **h0046/h0047** (Implementation stage): both act at the edit. This acts at Exploration — a
  pre-edit COMMITMENT (protect-list) rather than an edit-time skeleton or constraint. It tests
  whether pinning the forks at the planning step (before the solver starts writing SQL) is more
  durable than pinning them at the edit, since the over-edit is itself a planning decision.
- vs **h0019/h0042**: both pinned a single fork at Implementation. The protect-list names ALL the
  load-bearing lines at once (aggregate + joins + GROUP BY), so no single fork is left free.
- The cross-stage-memory risk (does an Exploration note survive into the Implementation edit?) is
  the specific failure mode this hypothesis exposes — a useful negative result if it goes inert.

## Honest tension with the standing decisions

- **`trials: 1`** (MEMORY `ade-bench-single-trial-judge-by-artifact`): a ~17% cell can only have
  its per-draw probability raised. If the protect-list reliably survives into the edit and pins
  all three forks, the per-draw probability could clear ~50% — that is what the ≥3-repeat smoke +
  artifact read must show, full verdict provisional. Un-promotable by construction if the
  protect-list is recorded but not honoured at edit time.
- **The concluded flip-portfolio wall** (MEMORY `ade-bench-oracle-program-concluded`): filed as a
  NEW mechanism class (Exploration-stage pre-edit protect-list), not a single-fork variant nor an
  Implementation-stage re-walk. If smoke shows the committed SQL breaks any fork — or the
  protect-list is recorded then ignored — REJECTED, CAPPED one-shot, no iteration.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change.
