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

### Correlated error through a *shared upstream filter* (new sub-case, h0030, 2026-06-07)

A "raw-source independent probe" — the strongest shape we have, the f1007-hard move — can **still
re-correlate** if it inherits the model's upstream **FILTER / population scope**. h0030 added
exactly such a probe for grain-drop: reconcile the model's `COUNT(*)` against `COUNT(DISTINCT key)`
on the raw parent **plus** a completeness anti-join (every raw-parent key must appear). It was a
plain SELECT on `{{ source() }}`, route-independent and generation-independent — and it still
false-greened on all three intercom targets (`Got 7` byte-unchanged, distance 7). The reason: the
intercom models apply a `_fivetran_active` filter that collapses **both** the parent
(`conversation_history`) **and** the child (`conversation_part`) to the **same 5 keys**, so the
raw-source `COUNT(DISTINCT key)` agreed with the model and the anti-join was empty. The probe read
the *right relation by the right route* but over the *wrong (filtered) population*, so it shared the
model's grain error and confirmed it.

**The refinement:** independence must hold for the **POPULATION / FILTER, not just the relation or
the route.** A probe that re-applies (or silently inherits) the same `WHERE`/`active`/effective-date
filter the model uses is not independent of the grain error, even when it reads the immutable source
table by a different SQL path. Add this to the sharp test below: a check is independent only if its
*key set* is computed without the model's scoping predicate. When the deciding fact is "which
population is canonical" (h0030: 2 distinct ids in history vs 5 active parts), no
same-filter raw-source probe can settle it — that fact is oracle-only. Compounding this, a
**check-don't-replace** escape (the G10 case-(ii) "if legitimately scoped, leave it" softening,
added to avoid h0012's mandate-replace damage) becomes the hole the solver walks through: it is free
to bless the short table as "legitimately scoped." The mechanical-number ingredient that won
asana002 (`::timestamp`) worked because the target was a **value to match**; here the target was
**which population is canonical**, which a filter-correlated reconcile cannot recover. (Cross-ref:
`arbitration-without-oracle.md` → *Grain / Missing Rows* — its `ABSTAIN`-when-the-parent-count-is-a-
filtered-convention clause is the same wall; a parent-key count only arbitrates when the parent's
population is itself unambiguous and filter-free.)

## The sharp test for any proposed check

> **Is this check _independent_ of the thing it checks, or _correlated_ with it?**
> - Reads the solver's own plan / framing / output, or re-runs the solver's own logic → **correlated** → it will false-green. Reject.
> - Recomputes the truth from the **raw source** by a *different route*, or checks a relation the answer must obey regardless of method → **independent** → it can catch.
> - **Independence must also hold for the POPULATION / FILTER, not just the relation/route (h0030).** A raw-source probe that re-applies (or silently inherits) the model's `WHERE`/`active`/effective-date scoping predicate computes its key set over the *same filtered population* and re-correlates — it will false-green even though it reads the immutable source table. The probe's key set must be derived without the model's scoping filter; if "which population is canonical" is itself the deciding fact, no same-filter probe can settle it (oracle-only).

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
| #1a entity grain | intercom: ~~local parent ✓~~ → **parent is filter-correlated (h0030)** · asana004: oracle-only convention | ❌ revised down — construct/reconcile family REJECTED & oracle-blocked (h0030) |
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
- **E0/h0032 harness method refinement (h0030 finding).** E0's controlled 2×2
  (`_artifacts/h0032-e0-harness/result_2x2.json`) CLEARED the count+anti-join reconcile two-sided
  on its injected-error fixtures — but those fixtures were **CLEAN**: they lacked a *shared upstream
  filter* between parent and child, so the injected drop showed up cleanly. The real intercom
  targets have a `_fivetran_active` filter on **both** parent and child that collapses them to the
  same key set, which the synthetic fixtures did not model — so E0 validated the probe in a regime
  the actual failure does not inhabit, and predicted GO where the live run went inert. **A future E0
  fixture for any grain/completeness probe MUST share the target's upstream filter (apply the same
  `active`/effective-date predicate to both parent and child) so the harness exercises the
  filter-correlation false-green, not just a clean drop.** Without that, the harness's two-sided
  clearance is over-optimistic for filter-scoped models.

## Evidence / provenance

Session 2026-06-06 (real-data Plan Reviewer simulation on h0017 + this real-world-analogy
synthesis). Cross-refs: `WORKFLOW-REFINE.md` (Plan Reviewer + Output Contract entries),
`bug-type-taxonomy.md` (reach map source), `concept-resolve-uncovered-false-greens.md`
(f1007-hard independent-check finding). MEMORY: `ade-bench-solver-blind-to-oracle`,
`ade-bench-validation-self-anchored-false-green`, `ade-bench-instruction-lever-taxonomy`.
Literature anchors: Knight & Leveson 1986 (N-version common-mode failure); Heuer,
*Psychology of Intelligence Analysis* (ACH); metamorphic testing (Chen et al.); double-entry
bookkeeping (Pacioli).
