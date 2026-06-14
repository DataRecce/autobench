---
id: h0058
title: Move-B-only feature-removal stabilizer on @baseline h0056 — add the drop-feature-col / KEEP-base-id worked example to the feature-removal block to lock quickbooks002/003 against the over-drop coin-flip
status: hypothesis
kind: hypothesis
source: "Spun out of h0057 (REJECTED on the Move-A flip; ana-eng004 oracle-blind, 4 real-run cycles, 4 distinct failure modes). h0057 Move B was VALIDATED — quickbooks002/003 held PASS across both 14-task smokes (kept department_id, no less-columns error, zero bleed); it was orphaned only by the Move-A rejection. Forks the current @baseline h0056 (runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a, 35/48). Artifact-grounded: qb002/qb003 r1-vs-r2 forensic in h0056 = an OVER-DROP of the shared base department_id column (r1 lost both PASS->FAIL this way; r2 kept it -> both PASS); the correct boundary (drop department_name, keep department_id) is cleanly expressible and proven non-bleeding by h0057."
started:
completed:
verdict:
score:
worktree:
---

## Hypothesis

@baseline h0056's r1 draw (32) fell short of its r2 draw (35) on three un-locked coin-flip cells;
two of them are `quickbooks002`/`quickbooks003`. Both tasks remove the `using_department` feature.
The correct edit drops the feature-ONLY derived column `department_name` (and its conditional join)
but KEEPS the shared base column `department_id` that the rest of the project still references and
the solution retains. In h0056 r1 the solver OVER-DROPPED — it scrubbed `department_id` too →
"has less columns than solution" → both regressed PASS→FAIL; in r2 it kept it → both passed. A pure
coin-flip on the removal boundary, and it was the dominant cause of r1's shortfall.

The h0056 feature-removal block (the banked h0045 lever) already says "preserve ordinary
raw/source attributes that are part of the model" in **prose, but carries no worked example**. This
hypothesis makes ONE scoped README change: add a before→after skeleton to that block making the
boundary concrete — when removing/disabling a feature, DROP the feature-only derived column and its
conditional join, but KEEP the shared base id / foreign-key column the rest of the project uses.

This is the exact Move B from h0057, which was VALIDATED there: quickbooks002/quickbooks003 held
PASS across BOTH 14-task smokes (the worked example was byte-unchanged through all four h0057
cycles), keeping the department base id each time with the "less columns" error absent and zero
bleed to the other levers or canaries. h0057 was rejected only on its independent Move-A flip
(ana-eng004 oracle-blind); Move B is orphaned by that rejection and carried here on its own.

**This is a STABILIZER, not a flip.** It does not add a new pass on a stable-FAIL cell. qb002/qb003
are PASS@baseline coin-flips that regress when the solver over-drops the base id; the worked example
lowers that PASS→FAIL rate so the baseline's good draws become more reproducible.

**Falsifiable claim (one scoped README edit — Implementation stage only):**
With the drop-feature-col-keep-base-id worked example added to the h0056 feature-removal block,
quickbooks002/quickbooks003 commit the drop-`department_name`-keep-`department_id` artifact and hold
PASS more reproducibly across independent draws, with NO interference to the other six h0056 levers
and NO canary regression — in particular the worked example must NOT over-fire on a BUILD/RENAME
task (no column over-preservation; quickbooks004's narrow toggle and the build-direction passers
hold).

**The proposed README edit (generic identifiers, Implementation stage):**

ADD a worked example inside the existing feature-removal block (after the "Preserve ordinary
raw/source attributes…" paragraph):

```text
(worked example for "remove the config/variable … Preserve ordinary raw/source attributes …")
When removing a feature, drop the feature-ONLY derived column and its conditional join, but KEEP
the shared base id / foreign-key column that the rest of the project uses.

BEFORE (using_feature enabled):
    select t.entity_id,
           t.feature_fk_id,                         -- BASE column from the source/transaction
           {% if var('using_feature', True) %}
           dim.feature_label as feature_name,       -- FEATURE-ONLY derived column
           {% endif %}
    from t {% if var('using_feature', True) %} left join dim on dim.id = t.feature_fk_id {% endif %}

AFTER (remove the feature — keep the base fk, drop only the feature-only column + its join):
    select t.entity_id,
           t.feature_fk_id                          -- KEEP: shared base column (solution retains it)
    from t                                          -- DROPPED: the conditional join + feature_name
```

## Acceptance criteria

**AC-1 — Exactly one scoped README edit; spec differs only in `experiment:` + `solver_workflow:`.**
README diff vs the h0056 solver README = the single worked-example insertion inside the existing
feature-removal block. No NEW stage or rule; the other six levers, the leak-guard prose, and every
other stage byte-identical. No `AUTO_*`/`solution__*`/`check_*`/`department_id`/`department_name`/
expected-count token; no web-fetch token. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved. The worked example uses GENERIC identifiers (the foreign-domain
`using_feature`/`feature_fk_id`/`feature_name` skeleton) — it must NOT embed the target's own
schema (the h0057 leak-catch: a target's columns in the README is a double leak — README overfit +
sim contamination).

**AC-2 — Every score paired with a clean strict audit** (`tainted: 0`, `coverage_missing: 0`,
`captured > 0`).

**AC-3 — Decisive per-cell committed-artifact reads (not chatter).**
quickbooks002 + quickbooks003: the committed transaction/union models DROP `department_name` (and
its conditional join) but KEEP `department_id`; the "has less columns than solution" error is
absent. Regression holds, committed-shape confirmed: quickbooks004 (narrow toggle held), ana-eng003
(build PRESERVE held — the feature-removal worked example must not bleed into a build), and a
cross-family canary.

**AC-4 — Judged on a TWO-DRAW expectation + committed artifact (not a single flip).** This is a
variance-reducer: GO if quickbooks002/quickbooks003 hold their keep-`department_id` artifact across
≥2 independent seed-perturbed draws with no collision and no regression, raising the qb002/qb003
hold rate vs the h0056 r1-vs-r2 coin-flip. A single PASS reward is NOT the proof — the committed
keep-base-id artifact across draws is.

**AC-5 — Canaries incl. quickbooks004 + a cross-family hold; the worked example must NOT over-fire
on a build/rename.** No column over-preservation: a BUILD/RENAME task (e.g. ana-eng003, the
preserve-columns base case) must still behave exactly as @baseline — the feature-removal worked
example fires only on a remove/disable-a-feature task, not on a build. A collision (the rule firing
on a build to over-preserve) or any same-construct regression is a NO-GO.

## Target dataset

- `ade-bench-quickbooks002`, `ade-bench-quickbooks003` — 🎯 STABILIZE targets (PASS@baseline
  coin-flips; must DROP `department_name`, KEEP `department_id`). Judged by the committed
  keep-base-id artifact + a two-draw expectation, NOT a single flip.
- `ade-bench-quickbooks004` — ✅ MUST-HOLD (banked narrow toggle; the worked example must not
  perturb it).
- `ade-bench-ana-eng003` — ✅ MUST-HOLD build/rename PRESERVE base case (the h0045↔h0055 boundary:
  the feature-removal worked example must NOT fire on a build to over-preserve columns).
- A cross-family canary (e.g. `ade-bench-asana001` / `ade-bench-f1007`) — ✅ HOLD (note asana001 is
  a known package-family coin-flip per the h0057 forensic; watch, do not over-read a wobble).

GO requires quickbooks002/quickbooks003 holding their keep-`department_id` committed artifact across
≥2 draws with no collision/regression and a clean strict audit — i.e. a more reproducible baseline,
proven by the two-draw expectation, not a headline +1.

## Honest tension with the standing decisions

- **Pure stabilizer, not a flip.** Its value is a more reproducible baseline (lowering the
  qb002/qb003 over-drop PASS→FAIL rate), not a net pass-add. Judge it by the committed keep-base-id
  artifact across two draws, per the single-trial / judge-by-artifact standing decision — closing a
  coin-flip is a small success worth banking.
- **One edit modifies an existing block (adds a worked example).** It is one coherent additive
  sharpening inside Implementation, not a from-scratch lever; the gatekeeper G1/G6 read it as one
  scoped edit.
- **Bleed risk: LOW.** The worked example is gated to remove/disable-a-feature requests and was
  proven non-bleeding across four h0057 cycles (qb004 + ana-eng003 + the build passers all held).
  The build-direction MUST-HOLD (ana-eng003) is the tripwire against over-preservation.
- **Foreign-domain worked example (h0057 leak-catch).** The skeleton uses generic
  `using_feature`/`feature_fk_id`/`feature_name` identifiers, never the target's `department_*`
  columns — a target's own schema in the README is a double leak.

Method/README change only. Forks @baseline h0056
(`solver_workflows/h0056-compose-six-levers-on-h0052`, runtime codex); no dataset, harness, or
runtime change.
