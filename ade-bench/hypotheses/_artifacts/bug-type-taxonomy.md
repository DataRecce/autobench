# Bug-Type Taxonomy — what's broken, and what we've tried

The standing list of **bug types** we use to classify ade-bench `@baseline` failures, and the
hypotheses that have attacked each one. This is the "what have we tried" board — **keep it
updated** as hypotheses conclude and new failure clusters are found.

**Umbrella fact:** all 17 `@baseline` failures (31/48 pass, run `622bdedac572b479`) are
**false-greens** — the solver's own check reports clean while the hidden oracle finds the answer
wrong. Source re-audit: `concept-resolve-uncovered-false-greens.md`. Glossary of failure-type
terms: `term-table.md`.

> **How to read failure signatures:** `Got N` = distance-to-pass on a row mismatch; an
> *unchanged* `Got N` vs `@baseline` means the lever was **inert** on that cell. "less columns"
> = compile-time width error. "false-green" = right shape, wrong values, solver's self-check passed.

## The board

| # | Bug type | What goes wrong (plain) | Failure signature | Tasks | Hypotheses tried | Status |
|---|---|---|---|---|---|---|
| 1 | **Grain / wrong spine** (wrong rows) | built off the child table & grouped up → parents with no children dropped | row mismatch, `Got N` | asana004, asana005, intercom001, intercom003, intercom002 | h0010 (prose) → h0016 (worked-example) | **REJECTED** 0/4 (h0016 reached SQL on intercom001 `Got 7→5`, no flip) |
| 2 | **Width / missing columns** | hand-picked a column subset instead of the full output contract | compile ERROR "has less columns than solution" | ana-eng004, f1002, ana-eng007-medium | h0011 (worked-example) | **REJECTED** 0/3 |
| 3 | **Value divergence** (shape right, numbers wrong) | right rows & columns, wrong values; only an *independent* recompute catches it | value mismatch (false-green) | ana-eng006, ana-eng007, airbnb007, asana005-hard, f1006, airbnb009 | h0012 (independent recompute, Validation) | propose |
| 4 | **Incomplete deliverable set** | compiles green so solver stops; graded models never built | missing model / multiple checks fail | quickbooks001, ana-eng007-medium | h0013 (enumerate deliverables, Exploration) | propose |
| 5 | **Missing package-implied models** (repair tasks) | fix-it task: fixes the visible error, stops; installed package already has the missing models | missing `stg_*` models the grader wants | quickbooks001 | h0015 (copy installed package, Implementation) | hypothesis |
| 6 | **Analytical-answer guess** | answer-style deliverable includes an option on plausibility, unverified | wrong answer set, `check_option_*` fails | f1011 | h0014 (per-claim evidence, Implementation) | hypothesis |
| 7 | **Package/convention fidelity** | wrong column type / local convention vs the installed package | type-contract / convention mismatch | asana002 (the loop's one partial win) | h0009 (package fidelity) | **REJECTED** (+1 smoke / −1 full) |

## Per-type detail & lessons

- **#1 Grain** — most-studied type; the prose (h0010) vs worked-example (h0016) head-to-head lives
  here. Lesson: a copyable example *reaches* the committed SQL where prose is wholly inert — but
  "reaches" ≠ "passes" (0/4). `intercom002` is a grain sibling, never run as a smoke target.
- **#2 Width** — distinct from grain: right rows, *too few columns*; catches at compile, not on
  values. Worked-example was inert (0/3).
- **#3 Value divergence** — the **heavyweight cluster (6 tasks)** and the only family mapping to
  the one *proven* mechanism (compare an independent number, as the f1007-hard catch did). Highest-
  value open type. Note: *self-anchored* checks are dead (h0006/07/08) — the recompute must be
  genuinely independent of the solver's own output.
- **#4 & #5 overlap on `quickbooks001`** — same task, two angles: h0013 = "enumerate all
  deliverables up front"; h0015 = "copy the missing models straight from the installed package"
  (plays to the proven copy-a-local-artifact lever, #7's asana002 win).
- **#6 Analytical guess** — lone tail, one task (f1011: emitted "ABDE", correct "ABE").
- **#7 Package/convention** — the loop's **only win so far** (asana002, a `due_at::timestamp` type
  match landed at smoke) — but it regressed at full scale (convention-bleed cost f1/quickbooks).

## Overlaps to keep straight

- `ana-eng007-medium` shows **both** width (#2) and incomplete-deliverable (#4) — a task can carry
  more than one bug.
- `quickbooks001` sits under both #4 and #5 by design.

## Meta-pattern (the recurring lesson)

README-prose/worked-example levers have largely hit a **ceiling** at gpt-5.5 / `reasoning_effort:
xhigh`: a verbatim copyable skeleton changes the committed SQL yet still flips zero targets,
because the residual gap is task-specific correctness the README can't supply without leaking.
Scoreboard: h0008 0/7 · h0009 +1/−1 · h0010 0/4 · h0011 0/3 · h0016 0/4. Open non-prose
directions: capability lever (stronger model/effort), multi-sample-and-select (attack run-to-run
variance), independent-invariant verification (#3's lever, done right).

---

## Maintenance — keep this current

Update this file whenever:
- **A hypothesis concludes** → change its row's Status (e.g. `propose` → `REJECTED 0/N` or
  `PROMOTED`), and add the key one-line lesson to Per-type detail.
- **A new failure cluster is found** → add a new bug-type row (next #), with tasks + failure
  signature; link the concept/hypothesis that surfaced it.
- **A task is re-classified** or shown to carry a second bug → update Tasks + the Overlaps section.
- **The scoreboard / meta-pattern shifts** → update the Meta-pattern paragraph.

Keep it grounded: pull tasks, `AUTO_*`/`check_*` test names, and `Got N` from the actual
hypothesis files (`hypotheses/h00*.md`, `_archive/`) — never invent them. The
`explain-hypotheses` skill reads this file as its taxonomy source.
