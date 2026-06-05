---
name: explain-hypotheses
description: >-
  Explain one ade-bench autoresearch hypothesis, or compare several, in plain words
  backed by structured comparison tables. Use this whenever the captain asks "what's
  different between h00XX and h00YY", "explain this hypothesis", "what bug does h00ZZ
  target", "show the remaining tasks/bugs", or any request to summarize, contrast, or
  lay out hypotheses, their target tasks, failure types, or results — even if they
  don't say the word "table". Always reach for this skill for hypothesis explanation
  so the format stays consistent across the whole loop.
---

# Explaining hypotheses

The captain reads **plain words first, detail in tables**. A hypothesis is only useful to
explain if the listener walks away knowing three things: *what bug it attacks*, *which tasks
that bug shows up on*, and *what happened (or what's predicted) when we tried to fix it*. This
skill is the house style for delivering exactly that, consistently, every time.

This complements the operator-memory rule "report plain words, detail in file" — say it
simply, then put the structure in tables the captain can scan.

## The core idea: organize by BUG, not by hypothesis

The single most important move: **group the explanation around the underlying bug (failure
family), not around the hypothesis number.** Hypotheses come and go; the bugs are the stable
spine. Two hypotheses that attack the same bug (e.g. h0010 prose vs h0016 worked-example) only
differ in *how they deliver the fix* — make that the headline, not a wall of per-hypothesis prose.

So the reasoning order is always:

1. **Name the bug(s)** in one plain sentence each — what goes wrong, in human terms.
2. **List the tasks** that bug appears on, in a per-task table.
3. **Map hypothesis → lever → result** in a cross-reference table when more than one hypothesis
   is in play.

## Step 1 — Plain-words lead

Open with 2–4 sentences of plain language before any table. State the shared bug, then the
axis of difference. Example opener for "what's different between h0010 and h0016":

> Both attack the **exact same bug** (grain — the model is built off the child table so parents
> with no children get dropped). They differ only in **how they deliver the fix**: h0010
> *described* it in prose; h0016 *showed* a copyable SQL skeleton. The example reached the
> committed SQL where the prose didn't — but neither made anything pass.

Keep distinctions sharp and parallel ("prose vs worked-example", "rows vs columns"). If two
hypotheses target *different* bugs, say so up front — that is the headline difference.

## Step 2 — Per-task table (one per bug family)

For each bug family, write one plain-sentence description, then this table. Use these exact
columns so tables are comparable across sessions:

| Task | Failing hidden test | Failure type | What goes wrong |
|---|---|---|---|
| asana004 | `AUTO_int_asana__project_user_agg_equality` | row mismatch, `Got 3` | aggregates off `project_user` (13 w/ users) not `project` (16) — drops 3 zero-user projects |

Column rules:
- **Task** — the `ade-bench-` slug, but you may drop the prefix for readability (`asana004`).
- **Failing hidden test** — the `AUTO_*_equality` (or `check_*`) test that catches it. If unknown, say so rather than inventing one.
- **Failure type** — use the shared vocabulary below, plus the distance-to-pass marker when known.
- **What goes wrong** — one concrete clause: the actual mistake in the committed SQL/output.

When showing a smoke/regression result rather than a diagnosis, swap to result columns:
`Task | Role | base reward | result reward | base Got-N | result Got-N | moved? | classification`
(roles: 🎯 target, ✅ sentinel/canary). Mark flips, holds, and regressions explicitly — a
canary dropping FAIL is a NO-GO regardless of target movement.

## Step 3 — Cross-reference table (when comparing 2+ hypotheses)

Tie it together so the captain sees the whole board at a glance:

| Bug kind | Hypothesis | Lever family | Status / Result |
|---|---|---|---|
| grain — wrong rows | h0010 → h0016 | prose → worked-example | REJECTED (0/4; example reached SQL 7→5, no flip) |
| width — missing columns | h0011 | worked-example | REJECTED (0/3) |
| value divergence | h0012 | independent recompute | propose |

Put the same-bug hypotheses on one row with an arrow (`h0010 → h0016`) when the point is the
delivery contrast; give different-bug hypotheses their own rows.

## Shared failure-type vocabulary

Use these names so every table speaks the same language (canonical glossary:
`ade-bench/hypotheses/_artifacts/term-table.md`):

- **row mismatch (`Got N`)** — right columns, wrong number of rows. The `Got N` is the
  distance-to-pass; **unchanged `Got N` vs @baseline = the lever was inert on that cell** (cheap
  inert-detector — check this before reading transcripts).
- **width / "less columns"** — compile-time ERROR "has less columns than `solution__<model>`";
  right rows, too few columns.
- **value divergence (false-green)** — right shape, wrong values; the solver's own check passes
  while the hidden oracle fails. Only an *independent* recompute catches it.
- **incomplete deliverable set** — project compiles green but graded models were never built.
- **analytical-answer guess** — an answer-style deliverable includes an option on plausibility
  without a per-claim query.

## Two distinctions to keep straight

- **Diagnosis vs intervention.** A REJECTED hypothesis can still have a *correct* diagnosis — it
  was the *fix* (usually prose) that was inert. Say "the bug is real; the prose fix didn't land",
  not "the theory was wrong". This is a recurring, important nuance.
- **Reaches vs passes.** "The fix reached the committed SQL" (changed the artifact) is not the
  same as "the task passed". h0016 reached SQL on intercom001 (`Got 7→5`) yet still flipped 0/4.

## Worked example — the canonical three-way ("what's different between h0010, h0011, h0016")

This is the reference output. h0010 and h0016 share a bug; h0011 attacks a different one.

**Plain words:** h0010 and h0016 both attack the **grain** bug (wrong rows) — h0010 described
the fix, h0016 showed a copyable example. h0011 attacks a **different** bug, **width** (missing
columns). All three were rejected; together they show README/prose tuning has hit a ceiling.

Then the grain per-task table, the width per-task table, then:

| Bug kind | Hypothesis | Lever family | Result |
|---|---|---|---|
| grain — wrong rows | h0010 | prose rule | 0/4, inert (never reached SQL) |
| grain — wrong rows | h0016 | worked-example | 0/4, reached SQL on 1 task (7→5) |
| width — missing columns | h0011 | worked-example | 0/3, no flips |

Close with the takeaway in plain words (here: "show-don't-tell beats prose for *execution*, but
even the best example can't supply task-specific correctness without leaking — hence the ceiling").

## Where to find the inputs

- Active hypotheses: `ade-bench/hypotheses/h00*.md`. Archived/concluded: `.../hypotheses/_archive/`.
- Read the frontmatter (`id`, `title`, `status`, `verdict`, `source`) + the `## Hypothesis`,
  `## Smoke result`, and `## Verdict` sections — that's where tasks, failing tests, `Got N`, and
  results live.
- **Bug-type taxonomy / "what we've tried" board (start here):**
  `ade-bench/hypotheses/_artifacts/bug-type-taxonomy.md` — the standing list of bug types, their
  tasks, and the hypotheses attacking each. Read it first to ground any comparison; keep it
  updated when a hypothesis concludes or a new cluster is found.
- The original failure-cluster re-audit across all baseline failures:
  `ade-bench/hypotheses/concept-resolve-uncovered-false-greens.md`.
- Term glossary: `ade-bench/hypotheses/_artifacts/term-table.md`.
- Smoke-table glyph/format convention: `ade-bench/hypotheses/README.md` (propose stage).

Read the actual files before tabulating — never invent task slugs, `AUTO_*` test names, or
`Got N` values. If a value isn't in the source, write "unknown" rather than guessing.
