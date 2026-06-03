# Finding: baseline Validation/Finalization self-checks are false-green

**Status:** 📌 FINDING 2026-06-03 (no code change — guidance for hypothesis selection).
**Source:** full trace audit of the `@baseline` run
`runs/ade-bench-baseline/622bdedac572b479` (31/48 = 0.6458), all 48 tasks.
**Question asked:** *Do the Validation or Finalization stages detect an incorrect number and
successfully make the answer correct?*

> **One-line answer:** Almost never. Across 48 tasks the self-check caught a *new* wrong
> number and fixed it exactly **once** (`f1007-hard`), and only because it used an
> **independent** number. All **17/17 failures were false-greens** — the check reported
> clean while the hidden oracle found the answer wrong.

---

## 1. Headline numbers

| Outcome | Count | Meaning |
|---|---|---|
| Caught a NEW wrong number *during validation* and fixed → pass | **1 / 48** | `f1007-hard` only |
| Failures where validation reported clean but answer was wrong (false-green) | **17 / 17** | every failure |
| Passes where a wrong number was found-and-fixed **during diagnosis** (not a validation catch) | ~7 | f1004, f1005, f1005-medium, f1006-hard, f1007, f1007-medium, ana-eng003, ana-eng005 |
| Passes where validation fired but found nothing (confirmation only) | ~11 | answer was already correct |
| Passes with no numeric validation at all (build/compile/grep only, or no-op) | ~6 | airbnb003, ana-eng001, ana-eng002(-medium), asana003, quickbooks002/003 |

## 2. The one real catch — and why it worked

`f1007-hard` is the existence proof of a *working* check:

> Post-build validation found "total podiums across season tables = **3,372** while the raw
> standalone `results` count = **3,373**" → root-caused to `position` vs `position_order` →
> fixed 4 season models → re-validated → **PASS**.

It worked **only because it compared against an independent number**: the raw `results`
table, aggregated a *different way* than the season tables. That is a genuinely independent
invariant — exactly the lever a self-anchored check lacks.

## 3. Why the 17 failures all slipped through

Every failing check was **correlated with the solver's own (wrong) understanding**. Four
flavors:

| Mode | Tasks | What the check did |
|---|---|---|
| Compared to its **own re-derivation / the old code** | asana004, asana005, asana005-hard, intercom001/002/003, f1006 | "new model == old logic, 0 diff" — but the old logic was already wrong |
| Checked **counts/shape, not values** | ana-eng006 (102 rows, 0 dup ✓ → oracle "Got 204"), ana-eng007, airbnb007 | row/distinct/null clean while *values* wrong |
| Checked the **wrong / out-of-scope model** | quickbooks001 (validated `general_ledger`; graded models were 3 `stg_` it never built), ana-eng007-medium, f1002 (column shape) | green on a model the oracle doesn't grade |
| **Guessed a value, then confirmed the guess** | asana002 (`is_liked=false`), airbnb009 (fixed 722 missing days but broke a date-range invariant) | self-fulfilling |

The mechanism is general: a self-anchored post-answer check shares the bug's blind spot, so
it **confirms** correct answers well but **cannot catch** wrong ones. This is the
baseline-wide confirmation of why h0008 (Finalization source-invariant prose) was inert.
Root constraint: the solver is blind to the oracle (no `solution__*` seeds or `AUTO_*`
tests ship to `/app`), so any check it writes is necessarily self-referential unless it
reaches for a genuinely independent local signal.

## 4. Guidance for hypothesis selection

- **Do NOT file detect-and-fix / self-verification hypotheses on the Validation or
  Finalization stages.** That family is exhausted: h0006, h0007 (REJECTED) and h0008
  (NO-GO at smoke) all died here, and this audit shows why across the whole baseline.
- **Two live directions only:**
  1. **Independent checks** — reconcile to the *raw source grain* or a different source
     path, the way `f1007-hard` did. (If such a check lives in Validation, that is fine —
     the dead part is *self-anchored* checks, not the stage itself.)
  2. **Upstream / generative fixes** — correct the mental model at **Exploration** before
     the wrong model is built. This is `h0009-exploration-package-fidelity`'s bet.
- **Shape ≠ value.** ~2/7 of the misses h0008 targeted (ana-eng006, f1002) are
  wrong-value / right-shape; no shape invariant (rows/grain/columns) can catch those even
  in principle. Confirm a miss is actually a *shape* miss before targeting it with a
  shape-based hypothesis.

## 5. Related

- `hypotheses/_archive/h0008-finalization-source-derived-invariants.md` — the
  Finalization-stage version of this finding (with per-task trace citations).
- Memory: `ade-bench-validation-self-anchored-false-green`, `ade-bench-solver-blind-to-oracle`,
  `ade-bench-auto-equality-tests-hidden`.
