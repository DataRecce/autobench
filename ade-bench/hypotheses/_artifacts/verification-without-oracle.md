# Verification Without an Oracle — real-world techniques, mapped to ade-bench

A standing reference for designing **review / verification** stages in the solver workflow.
The core ade-bench wall — `ade-bench-solver-blind-to-oracle` — is a special case of a problem
that accounting, science, intelligence analysis, compilers, and ML have all worked on for
decades: **how do you check something when you don't know the right answer?** This file records
what those fields learned, the one test that separates a working check from a false-green, and
which ade-bench bug types each technique can and cannot reach.

Use this when filing any hypothesis that adds a *checking* control point (Plan Reviewer,
reconciliation, independent invariant, candidate selector). It tells you up front whether the
idea can possibly work and what shape it must take.

## The names this problem goes by

- **The oracle problem** (software testing) — testing a program when you have no trusted source
  of correct outputs. This is *our* problem verbatim: the solver is blind to the hidden oracle.
- **Verification without ground truth** (ML / statistics).
- **Assurance / audit without a reference** (accounting, safety engineering).

## The one universal lesson

**The only thing that ever beats "no oracle" is _independent redundancy_: compute the same
truth a second time by a path that does NOT share the first path's error, then require the two
to agree.** Every working technique below is a variation on this. Double-entry bookkeeping,
replication in science, two-source journalism, differential testing, N-version programming —
all the same idea.

**The universal failure mode is its mirror: _correlated error / common-mode failure_** — the
"second path" secretly shares the first path's mistake, so both are wrong the same way and the
check passes anyway. N-version programming failed in practice because independent teams made the
*same* bugs (Knight & Leveson, 1986). Intelligence fails when two "independent" sources both
trace to one origin. ML self-consistency fails when all samples share a misconception.

**This correlated-error failure IS the ade-bench false-green.** "Self-anchored false-green"
(`ade-bench-validation-self-anchored-false-green`), the h0026 candidate-selector, and the
reverse-inference Plan Reviewer (2026-06-06) are all the same defect: a check correlated with
the thing it checks.

## The sharp test for any proposed check

> **Is this check _independent_ of the thing it checks, or _correlated_ with it?**
> - Reads the solver's own plan / framing / output, or re-runs the solver's own logic → **correlated** → it will false-green. Reject.
> - Recomputes the truth from the **raw source** by a *different route*, or checks a relation the answer must obey regardless of method → **independent** → it can catch.

Apply this before writing the hypothesis. Reverse-inference failed it (it reasoned from the
contract's own framing). h0026's selector failed it (scored each candidate by its *own* local
checks). f1007-hard — the loop's **only** real catch — passed it (an independent number from the
raw source).

## Techniques, mapped to ade-bench

| Real-world technique (field) | Core idea | ade-bench form | Reaches bug type | Transfer |
|---|---|---|---|---|
| **Double-entry / reconciliation** (accounting) | record the truth twice; the books must *tie out* | recompute each metric from the **raw source** a second way; assert totals reconcile (`SUM(model)=SUM(source)`) | **value divergence #3**, grain | ⭐ highest — generalizes f1007-hard, our only catch |
| **Metamorphic / invariant testing** (the oracle problem) | check *relations* the answer must obey, not the answer itself | grain invariant `COUNT(*)=COUNT(DISTINCT parent_key)`; completeness "every source key survives" | grain #1a/#1b | ⭐ high — independent + leak-free |
| **Differential / dissimilar redundancy** (compilers, N-version) | two *dissimilar* implementations; **disagreement = bug** | build the model two ways (entity-spine vs child) or use the 2nd model (gpt-5.4-mini); flag disagreement | broad | high — use *disagreement*, NOT majority vote (vote re-creates correlated error) |
| **Analysis of Competing Hypotheses** (Heuer / CIA) | enumerate readings, seek **dis**confirming evidence | reviewer lists grain readings (13 vs 16), surfaces the divergence instead of confirming one | underdetermined #1a, #7 | medium — *flags* ambiguity even when it can't resolve it |
| **Blinding / pre-registration** (science) | commit method *before* seeing what makes it pass | already ~done: Output Contract commits grain before SQL | (process) | mostly imported |

## What this changes about strategy

1. **Prefer "reconcile the output" over "review the plan."** Plan-review can only catch
   *local-fact* bugs (the deciding fact is in the task text / `schema.yml` / existing code). The
   accountant's move — independently recompute and reconcile to the raw source — is stronger and
   reaches the largest uncovered cluster, **value divergence (#3)**, which no plan-reviewer can
   touch (the fact is the number itself). It is the generalization of f1007-hard.

2. **Fix a reviewer by making it _disconfirm_, not _confirm_.** A reverse-inference / "can I
   reconstruct a plausible question?" reviewer confirms and false-greens. An ACH-style reviewer
   that enumerates readings and hunts disconfirming evidence at least **flags** an
   underdetermined case (asana004's 13-vs-16) instead of silently passing it.

3. **Honest ceiling.** Real-world verification *raises* the catch rate; it never reaches 100%.
   Where there is genuinely **no independent path to the truth** — an arbitrary computed value
   with no conservation relation, or an **oracle-only convention** like asana004's "intermediate
   carries 16 rows" (the fact lives only in `solution/` + the hidden test) — even expert auditors
   and scientists are blind. Fraud that is *consistently* falsified across all records survives
   audit. The goal is not a magic reviewer; it is **the maximum independent redundancy the leak
   boundary allows.**

## Connection to existing doctrine

This is the real-world framing of a belief the loop already holds: "independent invariants is
the live lever" (`concept-resolve-uncovered-false-greens.md`, the f1007-hard finding). That
belief is just the dbt name for **double-entry + metamorphic testing**. The contribution of this
note is the **toolbox** (reconcile / invariant / differential / disconfirm) and the **test**
(independent vs correlated) to build them well, plus the names to find the literature.

## Reach map — which bug types a check can touch (from `bug-type-taxonomy.md`)

| Bug type | Where the deciding fact lives | Reachable by an independent check? |
|---|---|---|
| #2 width (missing columns) | `schema.yml` / instruction → **local** | ✅ best plan-review target (mechanical completeness assertion) |
| #1b date-spine | "row for every day" + data min/max → **local** | ✅ invariant: grain covers [min,max] |
| #4 rolling-window/tolerance | the project's own existing rolling model → **local** | ✅ already flipped under h0017 (airbnb007) |
| #6 incomplete deliverable | `schema.yml`/ref-graph *if enumerated* | ⚠️ partial (enumerable-only) |
| #5 type/contract | type declared / derivable downstream | ⚠️ partial (asana002 `::timestamp`) |
| #1a entity grain | intercom: local parent ✓ · **asana004: oracle-only convention** | ⚠️ split — mostly not |
| #3 value divergence | the computed **value** itself → **oracle-only** for the number, but **reconcilable from raw source** | ⭐ reconciliation is the only shot; no plan-reviewer can |
| #7 analytical guess | which options are true → needs independent **recompute** | ❌ for plan-review; needs per-claim evidence (h0014) |

## Bears on

- The **Plan Reviewer** direction (WORKFLOW-REFINE, 2026-06-06): workable but bounded to
  local-fact bugs; must *disconfirm*, not *confirm*.
- The **candidate-selector** siblings h0024/h0025/h0027: each needs an *independent* IN-decision
  falsifier (the test above), not self/internal consistency.
- The next concrete lever: an **independent-reconciliation check** on a value-divergence target
  (e.g. ana-eng007) where a raw-source recompute is locally derivable — the highest-transfer
  import here.

## Evidence / provenance

Session 2026-06-06 (real-data Plan Reviewer simulation on h0017 + this real-world-analogy
synthesis). Cross-refs: `WORKFLOW-REFINE.md` (Plan Reviewer + Output Contract entries),
`bug-type-taxonomy.md` (reach map source), `concept-resolve-uncovered-false-greens.md`
(f1007-hard independent-check finding). MEMORY: `ade-bench-solver-blind-to-oracle`,
`ade-bench-validation-self-anchored-false-green`, `ade-bench-instruction-lever-taxonomy`.
Literature anchors: Knight & Leveson 1986 (N-version common-mode failure); Heuer,
*Psychology of Intelligence Analysis* (ACH); metamorphic testing (Chen et al.); double-entry
bookkeeping (Pacioli).
