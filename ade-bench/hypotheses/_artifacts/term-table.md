# Term Table — how to read the operator's reports

A plain-words key for the ade-bench autoresearch loop. Keep reports skimmable:
**read the headline verdict and the recommendation first; everything between them is
evidence you can scroll past unless you want the detail.**

## How to read a gate / result report

1. **Headline verdict** — the one-line answer (e.g. `NO-GO`, `REJECTED`, `GO`, `PROMOTE`).
2. **Recommendation** — what the operator suggests doing, at the bottom.
3. (Optional) the table + "why" in the middle — the evidence behind the verdict.

If you're busy, lines 1 and 2 are enough to decide.

## Glossary

| Term | Plain meaning |
|------|---------------|
| **Task** | One problem the AI solver tries to solve (one dbt project to fix/build). |
| **Solver** | The AI (codex) that attempts the task. It **cannot see the answer key** — grading tests are hidden from it. |
| **@baseline** | Our current best score to beat: **31 of 48 tasks pass** (run `622bdedac572b479`). |
| **Hypothesis (hNNNN)** | One idea we test — always exactly **one change** to the solver's instructions, and falsifiable. |
| **Target** | A *broken* task we are **trying to fix** (want it to go FAIL → PASS). |
| **Sentinel** | A *passing* task near the targets we watch to be sure our change didn't break it. |
| **Canary** | A *passing* task in a **far-away area** — an early warning that our change broke something unrelated. |
| **Flip** | A task changing PASS↔FAIL. FAIL→PASS = good; PASS→FAIL = bad. |
| **Regression** | A task that used to pass now fails. Always bad. |
| **Smoke** | A quick, cheap test on ~9 hand-picked tasks before committing to the big run. |
| **Full run** | The big test on all 48 tasks. |
| **GO / NO-GO** | Did the quick smoke test look good enough to continue to the full run? |
| **Inert** | Our change did **nothing** — the AI ignored it; the committed code didn't change. |
| **"Got N"** | How far off the answer was (the dbt error count). Smaller = closer to correct. Same number vs baseline = our change had no effect. |
| **Convention bleed** | Our change helped the target but **accidentally broke** other tasks where it shouldn't have fired. |
| **Self-anchored / false-green** | The solver checks its work against *its own* (possibly wrong) understanding and declares success — a green that isn't really correct. |
| **Independent invariant** | A check against a number computed **separately from the solver's own output** (e.g. straight from raw source data) — the only kind of self-check that has ever caught a real bug. |
| **Consensus / self-vote** | Solver makes N attempts and commits the answer **most of them agree on** — a way to beat run-to-run noise *without* seeing the answer key. |
| **pass@1 / pass@k** | pass@1 = solved on the single committed attempt (our metric). pass@k = solved if *any* of k attempts passes (a different, headroom metric). |

## Failure modes (why a hypothesis gets rejected)

| Mode | What it means |
|------|---------------|
| **Inert** | The instruction never changed the committed SQL. The AI read it and ignored it. (e.g. h0010) |
| **Premise-falsified** | The AI *did* follow the instruction, but the task still fails because the needed info isn't available locally (it's in the hidden answer key). (e.g. h0011) |
| **Convention bleed** | The change helped the target but broke unrelated passing tasks. (e.g. h0009) |
| **Reaches-but-doesn't-pass** | The change got the AI to write better code (closer) but not correct enough to pass. (e.g. h0016) |

## The scoreboard so far (all rejected — README-prose ceiling)

| Hyp | The idea, in one line | Result |
|-----|------------------------|--------|
| h0008 | Tell the solver to double-check its own work afterward | 0/7 — inert (self-anchored) |
| h0009 | Tell it to copy the installed package's conventions | +1 smoke / −1 full — convention bleed |
| h0010 | **Describe** the grain-spine fix in prose | 0/4 — inert (never reached the SQL) |
| h0011 | Tell it to emit the full column set + show an example | 0/3 — premise-falsified |
| h0016 | **Show** the grain-spine fix as copyable example code | 0/4 — reached the SQL, still didn't pass |

**Lesson:** editing instructions to make the AI *restructure* SQL has hit a ceiling. The next
bets are non-prose: consensus/self-vote (beat the noise), a stronger model / more thinking, or
genuinely independent self-checks.
