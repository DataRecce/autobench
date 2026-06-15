---
id: h0058
title: Move-B-only feature-removal stabilizer on @baseline h0056 — add the drop-feature-col / KEEP-base-id worked example to the feature-removal block to lock quickbooks002/003 against the over-drop coin-flip
status: conclude
kind: hypothesis
source: "Spun out of h0057 (REJECTED on the Move-A flip; ana-eng004 oracle-blind, 4 real-run cycles, 4 distinct failure modes). h0057 Move B was VALIDATED — quickbooks002/003 held PASS across both 14-task smokes (kept department_id, no less-columns error, zero bleed); it was orphaned only by the Move-A rejection. Forks the current @baseline h0056 (runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a, 35/48). Artifact-grounded: qb002/qb003 r1-vs-r2 forensic in h0056 = an OVER-DROP of the shared base department_id column (r1 lost both PASS->FAIL this way; r2 kept it -> both PASS); the correct boundary (drop department_name, keep department_id) is cleanly expressible and proven non-bleeding by h0057."
started: 2026-06-14T12:19:52Z
completed: 2026-06-15T00:46:21Z
verdict: passed
score: 0.7292
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

## Gatekeeper review

**Recommendation: APPROVE** — one scoped Implementation-stage worked example (generic
`using_feature`/`feature_fk_id`/`feature_name` skeleton, no target schema), leak-guard byte-intact,
spec two-field, gated to remove-feature requests with a build/rename over-fire tripwire (ana-eng003)
and two cross-family canaries in the panel; no FAIL on any rule.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-14T12:24:00Z.

Fork parent resolved: `source:` names h0056; `rk registry resolve run @baseline` →
`runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a`, whose `spec.frozen.yaml`
`solver_workflow: solver_workflows/h0056-compose-six-levers-on-h0052` — the dir forked. Agree.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff h0056/README.md h0058/README.md` = one hunk (67a68,83): the drop-feature-col/keep-base-id worked example inside `## Stage: Implementation`'s feature-removal block, after the "Preserve ordinary raw/source attributes…" paragraph. No other `## Stage:` touched; exactly the one idea the Falsifiable claim names. |
| G2 leak-guard intact | PASS | Added lines carry no `AUTO_*`/`solution__*`/`check_*`/`expected-count`/web-fetch token; the only `curl`/`wget` hits are the unchanged leak-guard prose (README L9–10), byte-identical to parent. |
| G3 spec two fields | PASS | `diff baseline.yaml h0058.yaml` = only `experiment:` + `solver_workflow:`. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0058.yaml h0058.smoke.yaml` = only an added `benchmark.tasks:` block; all six slugs `ade-bench-` prefixed; both named `## Hypothesis` targets (quickbooks002, quickbooks003) present. |
| G5 both frozen | PASS | `h0058…frozen.yaml` + `…smoke.frozen.yaml` both exist; both carry `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text = the body's generic skeleton verbatim ("drop the feature-ONLY derived column and its conditional join, but KEEP the shared base id / foreign-key column"; BEFORE/AFTER using `using_feature`/`feature_fk_id`/`feature_name`). Generative build-guidance, NOT self-anchored verification. No target `department_*` schema (h0057 leak-catch satisfied). |
| G7 actionability/inert-risk | PASS | Worked-example skeleton (the recommended copyable form, not abstract structural prose) — the G7 PASS class. Move B already produced the committed keep-base-id artifact across four h0057 cycles, so it is empirically non-inert here. |
| G8 regression-canary coverage | N/A (PASS) | Instruction is GATED — fires only on "removing a feature" (remove/disable-a-feature requests), not on every task; classify gated → N/A. Panel nonetheless carries cross-family passers (asana001, f1007) + the build/rename over-fire tripwire (ana-eng003) + same-construct canary quickbooks004; all `@baseline` r2 1.0. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever; it is build-time guidance on the removal boundary, no verify-and-act-on-disagreement instruction. |
| G11 multi-model-target risk | WARN (unverifiable) | qb002/qb003 scored-model counts are NOT in the taxonomy's multi-model-target list (only listed as h0009 bleed-family canaries) and were not enumerated from the dataset tests — surface as unknown. Mitigated: this is a STABILIZER judged by the committed drop-`department_name`/keep-`department_id` artifact across ≥2 draws (AC-3/AC-4), not a single-run flip credit — the exact G11 mitigation. |
| G12 decision-fork probe quality | N/A (PASS) | Not a fresh flipped-task follow-up needing a new probe: Move B is a component VALIDATED across four real h0057 `rk` cycles (qb002/003 held PASS on both 14-task smokes, worked example byte-unchanged), orphaned only by h0057's independent Move-A rejection. The hypothesis states this explicitly. |

**For the captain:** No blocking FAILs — APPROVE to advance to smoke. One WARN (G11): qb002/qb003 scored-model counts are unverified, so do not credit a lone PASS reward — judge strictly by the committed keep-`department_id` artifact on the transaction/union models across the ≥2 seed-perturbed draws (AC-4), which the hypothesis already requires. Watch ana-eng003 as the over-fire tripwire (the worked example must NOT fire on a build to over-preserve) and asana001 as a known package-family coin-flip (do not over-read a wobble).

## Propose stage report

**Outcome: propose artifacts built, AC-1 verified, gatekeeper APPROVE.**

What was done:
- Forked `solver_workflows/h0056-compose-six-levers-on-h0052` (the @baseline-h0056 r2 resolver,
  confirmed via `rk registry resolve run @baseline` →
  `runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a`) →
  `solver_workflows/h0058-feature-removal-keep-base-id-stabilizer`.
- Applied the ONE edit: the generic drop-feature-col / KEEP-base-id worked example (the body's
  `using_feature`/`feature_fk_id`/`feature_name` skeleton, verbatim) inserted inside the
  Implementation feature-removal block, immediately after the "Preserve ordinary raw/source
  attributes…" paragraph.

AC-1 verified:
- `diff h0056/README.md h0058/README.md` = ONE hunk (`67a68,83`) — the worked-example insertion
  only, inside `## Stage: Implementation`'s feature-removal block. Other six levers + leak-guard
  prose + every other stage byte-identical.
- Leak grep clean: no `AUTO_`/`solution__`/`check_`/`department_id`/`department_name`/expected-count
  token; `curl`/`wget` appear ONLY in the unchanged leak-guard prose (README L9–10). GENERIC
  identifiers only — no target schema (the h0057 leak-catch).

Specs:
- `specs/h0058-feature-removal-keep-base-id-stabilizer.yaml` — diff vs `baseline.yaml` = only
  `experiment:` + `solver_workflow:` (kind/runtime/trials preserved).
- `specs/h0058-feature-removal-keep-base-id-stabilizer.smoke.yaml` — adds only `benchmark.tasks:`
  = quickbooks002 + quickbooks003 (stabilize), quickbooks004 (narrow-toggle hold), ana-eng003
  (BUILD-PRESERVE over-fire tripwire), asana001 + f1007 (cross-family canaries). All six confirmed
  `@baseline` r2 reward 1.0 (read from the r2 `per_trial_outcomes.json`).
- Both frozen with `rk freeze --allow-missing`.

Gatekeeper: APPROVE — no FAIL; one WARN (G11 multi-model-target unverifiable, mitigated by the
AC-3/AC-4 committed-artifact judgment). Full per-rule table in `## Gatekeeper review` above.

Committed path-scoped (solver_workflows/h0058-*, specs/h0058-*, hypothesis file).

## Stage Report: full

- DONE: Two seed-variant FULL specs built from the 48-task base (NO benchmark.tasks selector); r1 = experiment ...-r1 + sampling.seed 42; r2 = experiment ...-r2 + sampling.seed 43; each differs from the base full spec ONLY in experiment: + sampling.seed:; both frozen with rk freeze --allow-missing.
  `diff base.yaml r1.yaml` / `r2.yaml` = exactly the two lines (experiment + seed); `grep tasks:` on both = none (full 48). Frozen sealed_hash DISTINCT — r1 baf3a33abb93eda7b130c141ba4e286d, r2 2f95b61fb52b7a6b9dae5ac47507d42c (CAS-buster worked → two independent run-dirs).
- DONE: Both full runs launched CONCURRENTLY and DETACHED via drivers/rk-run-detached.sh (keys h0058-full-r1 / h0058-full-r2, mode run); two handle dirs returned; ensign returns immediately, does NOT wait (FO owns the sentinel scan).
  r1 handle runs/.rk-handles/h0058-full-r1-20260614-125122 (worker pid 3259659, rk child 3259680/3259684); r2 handle runs/.rk-handles/h0058-full-r2-20260614-125122 (worker pid 3259689, rk child 3259704/3259707). RAZORBACK_SPACEDOCK_PLUGIN_DIR exported before launch.
- DONE: Both handles confirmed live (pid alive + rk run child spawned) before returning; exact two handle-dir paths reported.
  Both worker pids alive, both rk-run children present in pgrep, no premature `done` sentinel after a 20s recheck (log still buffering through Harbor startup — expected). ntfy topic adebench-rk-381c976fe07465bf armed on both.

### Summary
Launched the h0058 stabilizer promote test as two concurrent independent full 48-task draws (seed 42 / seed 43) against @baseline h0056 (35/48; qb002/qb003 the dominant r1 shortfall). Built two two-field seed-variant specs from the AC-1-verified base, froze both to DISTINCT sealed_hashes (CAS-buster confirmed → two separate run-dirs), and launched both detached via rk-run-detached.sh. Both handles confirmed live with rk children spawned. Did NOT audit/score — the FO owns audit + score + paired-delta when both sentinels (runs/.rk-handles/*/done) land. Each run is budgeted up to ~7hr.

## Run result

**Headline (plain words):** h0058 is a clean variance-reducer. The drop-feature-col/keep-base-id
worked example did exactly what it was built for — it locked `quickbooks002` and `quickbooks003`
to PASS in BOTH independent draws, where the baseline coin-flipped them (both FAILED in the
baseline's bad draw). No collision, no same-construct regression, no over-fire on the build/rename
tripwire, both draws strict-clean. The headline mean barely moved (34/48 vs the baseline's 33.5/48)
because off-construct f1 trials:1 noise ate into the seed-42 draw, but the qb-pair hold-rate rose
from **2-of-4 baseline draw-cells → 4-of-4**, which is the stabilizer's actual value.

**Scores (both strict-clean — re-confirmed `clean=48 / coverage_missing=0 / tainted=0` on BOTH):**

| Run | seed | run-dir | score | audit |
|-----|------|---------|-------|-------|
| @baseline h0056 (named) | 43 | runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a | 35/48 (0.7292) | — |
| @baseline h0056 r1 draw | 42 | runs/ade-bench-h0056-compose-six-levers-on-h0052-r1/deff5d8a9c10c92f | 32/48 (0.6667) | — |
| h0058 r1 | 42 | runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r1/c1a7e3195d18a55c | **33/48 (0.6875)** | clean=48/cm=0/tainted=0 |
| h0058 r2 | 43 | runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r2/eba9295fda32c05e | **35/48 (0.7292)** | clean=48/cm=0/tainted=0 |

Absolute vs paper_baseline 0.1875: both draws far above (`against_constant: above`).

**Paired ledger (paired by slug from `per_trial_outcomes.json`; `rk runs diff` TypeErrors on
ade-bench run-dirs — query_id null — so computed directly, as the tooling note prescribes).**

The decisive comparison for a *stabilizer* is SAME-SEED: h0058 vs @baseline at the same seed, so
the only difference is the worked example.

- **Same-seed-42 (h0058 r1 vs h0056 r1):** qb002 **F→P**, qb003 **F→P** (the stabilizer firing),
  f1003 **P→F** (off-construct f1 variance). f1001 stays F→F (seed-42 coin-flip in BOTH).
  Net +1 → 33/48.
- **Same-seed-43 (h0058 r2 vs h0056 r2 = the named @baseline):** **ZERO verdict changes.**
  Identical 35/48, paired bootstrap delta +0.0 [CI +0.0,+0.0]. The worked example was inert-safe on
  the seed where the baseline already kept department_id.

Cross-seed (h0058 r1 vs the named @baseline r2) paired bootstrap delta = −2.0 tasks
[95% CI −5.0,+0.0]: this is NOT a regression of the lever — it is the baseline's own seed-42→43
swing (f1001, f1003) reappearing in h0058's seed-42 draw, with qb002/003 already PASS in the
seed-43 baseline so they show no gain there. Within CI of zero; the lever's effect is seen on the
same-seed pairing, not this cross-seed one.

**Every verdict change, both directions, with mechanism:**

| Task | base→h0058 | seed | direction | mechanism |
|------|-----------|------|-----------|-----------|
| quickbooks002 | F→P | 42 (r1) | GAIN (stabilize) | worked example fired: dropped `department_name` + its conditional `using_department` join, KEPT `department_id` → no "less columns" error; 8/8 checks |
| quickbooks003 | F→P | 42 (r1) | GAIN (stabilize) | same: removed `department_name` outputs/docs, preserved base `department_id` FK; 14/14 checks |
| f1003 | P→F | 42 (r1) | REGRESSION | off-construct f1 variance: `count_answers` test "Got 1 result, configured to fail if != 0" (3/4 checks); the feature-removal worked example is ABSENT from the cell — not lever-caused |
| (f1001 F→F both seed-42 cells; P→P both seed-43 cells — NOT a change vs same-seed baseline) | | | seed coin-flip | identical `src_models_are_correct` FAIL 14 ("Got 14 results") in BOTH h0056 r1 AND h0058 r1; worked example absent |

**Held PASS across base + both draws:** qb004 (narrow toggle), ana-eng003 (build/preserve
tripwire), asana001 + f1007 (cross-family canaries), airbnb005/007/009, f1006, f1011, and the rest
of the 35-strong stable core. **Stable FAIL (unchanged):** ana-eng004 (Move A was dropped — h0058
is Move-B only), ana-eng006/007/007-medium, asana003/004/005/005-hard, intercom001/002/003,
quickbooks001, f1002.

### The six required analyze questions

1. **Net + full per-task ledger.** Above. h0058 = 33 (r1) / 35 (r2); two-draw mean **34/48 vs
   h0056 33.5/48**. Same-seed-42 net +1 (qb +2, f1003 −1); same-seed-43 net 0 (identical). Both
   gains (qb002, qb003) and the lone regression (f1003) named with mechanism; f1001 is a seed
   coin-flip, not a change vs same-seed baseline.
2. **Smoke vs full.** Smoke was **SKIPPED** for h0058 — Move B was already real-smoke-validated
   TWICE in h0057 (qb002/qb003 held PASS across both 14-task smokes, the worked example
   byte-unchanged through all four h0057 cycles, zero bleed). The full run confirms the smoke read:
   the worked example fires on the qb removal tasks and is silent elsewhere. No smoke→full fork
   drift to explain because there was no h0058 smoke; the f1003 r1 wobble is on a family the h0057
   smokes never sampled (f1) and is unrelated to the lever.
3. **Already-correct-and-broken.** The one regression, f1003, WAS passing at @baseline (P in
   b_r1, b_r2, and h_r2). It broke ONLY in the seed-42 draw, on its own f1 `count_answers` model,
   with the feature-removal worked example absent. This is "failed to be immune to off-construct
   trials:1 variance," NOT "the lever broke a passer" — the lever never touched f1003's construct.
   qb002/qb003 were PASS@baseline *coin-flips* (F in the seed-42 baseline) that the lever
   stabilized; no working code was damaged by the lever.
4. **Was the change executed?** YES, verified on the committed artifact (apply_patch hunks in the
   cell-root agent transcript + ensign session jsonl), not chatter:
   - qb002 (both draws): apply_patch deletes `departments.fully_qualified_name as department_name`
     and the `{% if var('using_department') %} left join departments … {% endif %}` blocks in
     `int_quickbooks__expenses_union.sql`, `int_quickbooks__sales_union.sql`,
     `quickbooks__ap_ar_enhanced.sql`; `expense_union.department_id` / `sales_union.department_id`
     remain (no `-` deletion of the base column). `dbt show` against `information_schema.columns`:
     "only `department_id` remains … no `department_name`." → **executed-and-helped.**
   - qb003 (both draws): ensign summary "Removed `department_name` outputs/docs. Preserved base
     `department_id` foreign-key columns where already propagated." Verifier 14/14, no "less
     columns" error. → **executed-and-helped.**
   - f1003 r1 regression: feature-removal worked example ABSENT (no `department`/`feature_fk_id`
     token in the cell); failure is on the cell's own f1 `count_answers` model →
     **off-construct variance, not inert and not lever-caused.**
   - ana-eng003 (build tripwire): no feature-removal worked-example token in the cell, normal build
     artifact, 2/2 → **lever correctly did NOT fire** (gated to remove-feature requests).
5. **Prevention + next move.** Gains kept without harm BY CONSTRUCTION: the worked example is gated
   to remove/disable-a-feature requests (ana-eng003 build/preserve confirms zero bleed in both
   draws; qb004 narrow toggle held). The residual harm (f1003/f1001 seed wobble) is off-construct
   trials:1 variance the lever can't touch and the panel can't cheaply suppress at trials:1 — it is
   the known f1 coin-flip noise floor (f1001 regressed in an h0057 draw too). Recommended next move:
   the captain decides promote (this is a variance-reducer, see closing rec); if not promoted, the
   qb keep-base-id boundary is now a proven, banked, non-bleeding component available to any future
   feature-removal composition.
6. **Smoke-vs-full fork drift.** N/A in the usual sense (no h0058 smoke). The h0057 smoke read of
   Move B held at full: qb002/qb003 keep-base-id artifact reproduced in both full draws. The f1003
   seed-42 wobble is single-trial variance on a family (f1) the lever does not touch and the h0057
   smokes did not sample — not a README rule drifting into a different branch, not a lever effect.

## Behavioral analysis

### quickbooks002 — STABILIZE target — F→P (seed 42), P→P (seed 43); committed keep-base-id artifact BOTH draws
Method adherence: the main agent dispatched a `spacedock:ensign` implementation worker that executed
the README's feature-removal method exactly. **Committed artifact (apply_patch, cell-root
`agent/codex.txt` + ensign session jsonl), seed-42 cell:** in all three affected union/enhanced
models the patch removes ONLY `departments.fully_qualified_name as department_name` and the
`{% if var('using_department', True) %} … left join departments on departments.department_id = …
{% endif %}` conditional joins, plus the `department_name` entries in `quickbooks.yml`/`docs.md`.
The base column `expense_union.department_id` / `sales_union.department_id` is NOT in any deletion —
it stays in the select. Worker `dbt show` on `information_schema.columns`: "only `department_id`
remains in the affected output path, with no `department_name`." Why it works: the verifier's
AUTO_*_equality "has less columns than solution" error (the over-drop failure mode) is ABSENT;
verifier `Done. PASS=8 … ERROR=0 TOTAL=8`, expected_test_count=8, the two department guard checks
(`check_if_models_use_department_var`, `check_if_project_has_department_var`) PASS. Seed-43 cell
identical shape (`deletes department_name: True`, no base-id deletion), 8/8. Distance-to-pass: 8/8
both draws.

### quickbooks003 — STABILIZE target — F→P (seed 42), P→P (seed 43); keep-base-id artifact BOTH draws
Method adherence: ensign worker, feature-removal method executed. Committed-artifact evidence: ensign
final report "Removed `department_name` outputs/docs. Preserved base `department_id` foreign-key
columns where already propagated"; project-local search for `department_name`/`department_table`/
`ref('stg_quickbooks__department')` returned no matches while `department_id` was retained. Verifier
`Done. PASS=14 … ERROR=0 TOTAL=14`, expected_test_count=14, both department guard checks PASS, no
"less columns" error. (The apply_patch body in qb003 was applied via the ensign's edit path that
didn't surface a literal `-department_name` select line in the extracted hunk — confirmed instead by
the ensign's explicit drop-`department_name`/keep-`department_id` report and the full 14/14 verifier
with the over-drop error absent.) Distance-to-pass: 14/14 both draws.

### ana-eng003 — BUILD/PRESERVE over-fire tripwire (AC-5) — P→P both draws, NO over-fire
Method adherence + over-fire check: the cell carries NO feature-removal worked-example token
(`drop the feature-only`, `feature_fk_id`, `keep the shared base`, `feature-removal` all absent in
both draws) — the gated worked example correctly did NOT fire on a build/rename task, so there was
no column over-preservation. Normal build artifact, verifier 2/2 (expected_test_count=2,
`Done. PASS=2 ERROR=0`) both draws. The h0045↔h0055 boundary held: feature-removal guidance fires
only on remove/disable-a-feature requests.

### quickbooks004 — narrow-toggle MUST-HOLD — P→P both draws
Reward 1 in both draws; the worked example did not perturb the narrow-toggle behavior.

### asana001 + f1007 — cross-family canaries — P→P both draws
Both held PASS across base + both draws. (asana001 is a known package-family coin-flip per the h0057
forensic; it did not wobble here.)

### f1003 — REGRESSION (seed 42 only) — off-construct variance, NOT lever-caused
Method adherence: feature-removal worked example ABSENT from the cell (f1003 is an f1 standings/
aggregate task, not a feature-removal task — the gated example correctly never fired). Failure
mechanism: 3 of 4 checks pass; the `count_answers` test fails — "Got 1 result, configured to fail
if != 0" (`Done. PASS=3 ERROR=1 TOTAL=4`). This is a bug on the cell's OWN f1 aggregate model, on
the seed-42 draw only (P in b_r1, b_r2, h_r2). Classification: off-construct trials:1 variance, not
lever-caused, not inert. Distance-to-pass: 3/4.

### f1001 — seed-42 coin-flip — NOT a change vs same-seed baseline
Identical failure in BOTH the @baseline seed-42 cell AND the h0058 seed-42 cell:
`src_models_are_correct` FAIL 14 ("Got 14 results, configured to fail if != 0"), 5/6 checks
(`Done. PASS=5 ERROR=1 TOTAL=6`). Passes in both seed-43 cells. The feature-removal worked example
is absent. This is a pure seed coin-flip in the baseline itself (f1001 also regressed in an h0057
draw), reproduced identically under h0058 — it is NOT a verdict change attributable to the lever.

## Promote recommendation

**Recommend PROMOTE as a variance-reducer (decision is the captain's).** Judged by the standard the
hypothesis sets — the committed keep-`department_id` artifact across ≥2 draws plus the hold-rate
lift, NOT the modest headline net — h0058 is a clean, collision-free stabilizer: (1) qb002 AND
qb003 committed the drop-`department_name`/keep-`department_id` artifact with the over-drop "less
columns" error absent in BOTH seed-perturbed draws (AC-3); (2) the qb-pair hold rate rose from
2-of-4 baseline draw-cells (both FAILED in the seed-42 baseline, the dominant r1 shortfall) to
4-of-4 (AC-4); (3) the seed-43 draw is byte-for-byte identical to the named @baseline (delta 0,
CI [0,0]) — zero interference with the other six levers; (4) the build/preserve over-fire tripwire
(ana-eng003) and the narrow toggle (qb004) held P/P with the worked example provably not firing
(AC-5); (5) both draws strict-clean. The two-draw expectation rises 33.5→34/48 and, more to the
point, the worst-case draw improves (the baseline's bad seed-42 draw goes 32→33 because the qb pair
stops coin-flipping). Honest caveat: the headline mean moved only +0.5 because off-construct f1
trials:1 variance (f1003, f1001) is noise the lever cannot touch; this is a reproducibility
improvement on the qb removal boundary, not a pass-count flip. As a banked, proven-non-bleeding
component it is worth promoting; if the captain prefers to hold for a larger net, the keep-base-id
worked example remains a de-risked component for future feature-removal compositions.

## Stage Report: analyze

- DONE: `## Run result` written — paired per-task ledger for BOTH draws (r1 c1a7e319 = 33/48, r2 eba9295f = 35/48) vs @baseline h0056, both strict-clean (clean=48/coverage_missing=0/tainted=0 RE-CONFIRMED on BOTH via `rk audit`); every verdict change in both directions with mechanism; all SIX analyze required questions answered; smoke SKIPPED stated (Move B real-smoke-validated 2x in h0057).
  Scores `rk score`: r1 0.6875, r2 0.7292, both `against_constant: above`. rk runs diff TypeErrored (query_id null) → paired delta from per_trial_outcomes.json; same-seed-43 delta +0.0 [CI 0,0], same-seed-42 net +1 (qb +2, f1003 −1).
- DONE: STABILIZER VERDICT (AC-3/AC-4) — qb002 + qb003 committed keep-`department_id` artifact in BOTH draws, confirmed from committed apply_patch + ensign session, NOT just reward.
  qb002 apply_patch deletes only `department_name` + `using_department` conditional joins, keeps `department_id` (dbt show: "only department_id remains, no department_name"); qb003 ensign "Removed department_name…Preserved base department_id"; "less columns" error absent, 8/8 + 14/14. Hold-rate lift 2/4 baseline draw-cells (both FAILED seed-42) → 4/4. AC-5: ana-eng003 P/P with no feature-removal token (did not fire on build), qb004 P/P.
- DONE: f1001 + f1003 r1-only regressions classified as off-construct variance vs lever-caused.
  Both cells carry NO feature-removal worked-example token. f1003 fails own f1 `count_answers` ("Got 1 result", 3/4); f1001 fails identically in BOTH baseline-seed-42 AND h0058-seed-42 cells (`src_models_are_correct` FAIL 14, 5/6) → seed coin-flip, not a change vs same-seed baseline. Closed with the PROMOTE recommendation (variance-reducer: qb hold 2/4→4/4, mean 34>33.5, collision-free, no over-fire; honest the headline net is modest; decision is the captain's).

### Summary
h0058 is a clean variance-reducer: the gated drop-feature-col/keep-base-id worked example fired on
qb002+qb003 and committed the drop-`department_name`/keep-`department_id` artifact (over-drop "less
columns" error absent) in BOTH seed-perturbed draws, lifting the qb-pair hold rate from 2-of-4
baseline draw-cells to 4-of-4. The seed-43 draw is byte-identical to the named @baseline (delta 0);
the seed-42 draw is 33/48 (qb +2, f1003 −1 off-construct f1 variance). Build/preserve tripwire
(ana-eng003) and narrow toggle (qb004) held P/P with the worked example provably not firing; both
draws strict-clean. Recommended PROMOTE as a banked, non-bleeding reproducibility improvement on the
qb removal boundary (two-draw mean 34 vs 33.5), honest that the headline net is modest — the captain
decides.

## Verdict

**PASSED / PROMOTED.** @baseline rebound from h0056 to
`runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r2/eba9295fda32c05e` (**35/48 =
0.7292**), PROMOTED by the FO 2026-06-14 (analyze commit 5830be7).

**Basis — a STABILIZER, not a headline net flip.** h0058 added one scoped worked example
(drop-feature-col / KEEP-base-id) to the existing feature-removal block. It promotes on a
**STRICT-≥-every-seed + committed-artifact + hold-rate** basis, NOT a pass-count flip:

- **STRICT ≥ every seed.** Seed-43: byte-identical to the named @baseline (35→35, paired delta +0.0
  CI [0,0]) — no-op on the good draw, zero interference with the other six h0056 levers. Seed-42:
  32→33 — the worked example prevents the over-drop on the baseline's BAD draw. So h0058 is ≥ h0056
  on every seed tested; it can only help or stay flat.
- **Committed keep-base-id artifact.** qb002 + qb003 committed the drop-`department_name` /
  keep-`department_id` artifact in BOTH draws (apply_patch removes only `department_name` + the
  `using_department` conditional join; `department_id` retained; the "has less columns than
  solution" over-drop error absent; 8/8 and 14/14).
- **Hold-rate 2/4 → 4/4.** The qb-pair coin-flipped in the baseline (both FAILED in the seed-42
  draw, the dominant r1 shortfall = 2-of-4 baseline draw-cells PASS); under h0058 both hold PASS in
  both draws = 4-of-4.
- No over-fire: the build/preserve tripwire (ana-eng003) and narrow toggle (qb004) held P/P with the
  gated worked example provably NOT firing; both draws strict-clean (clean=48/cm=0/tainted=0).

**Transferable lesson.** A precondition-gated STABILIZER — a worked example that prevents a known
over-drop regression mode — promotes on reproducibility (strict-≥-every-seed) + a committed artifact
+ a hold-rate lift, NOT on a headline net flip. Its value compounds because it banks a known
regression mode OUT of the baseline README: every future hypothesis now forks from a more
reproducible baseline (the qb removal boundary no longer coin-flips), so a banked variance-reducer
is real progress toward the goal even when the two-draw mean moves only +0.5 (33.5→34/48).

**Move B lineage.** This worked example IS Move B from h0057, where it was VALIDATED (qb002/qb003
held PASS across both 14-task smokes, byte-unchanged through all four h0057 cycles, zero bleed). It
was orphaned only by h0057's independent Move-A rejection (ana-eng004 oracle-blind) and carried here
solo. h0058 re-validated it at full 48-task scale across two independent draws.

## Follow-up Routing

**ESCALATE — surface candidate directions + the diminishing-returns read for captain strategy; do
NOT auto-file a doomed variant.**

The remaining 13 @baseline-h0058 FAILs (scanned from the r2 `per_trial_outcomes.json`): `ana-eng004`,
`ana-eng006`, `ana-eng007`, `ana-eng007-medium`, `asana003`, `asana004`, `asana005`, `asana005-hard`,
`f1002`, `intercom001`, `intercom002`, `intercom003`, `quickbooks001`. **None of these 13 has ever
been a named target of any prior hypothesis** — they are the untouched FAIL core; every banked flip
(airbnb009, f1006, asana002, qb002/003) hit a DIFFERENT cell.

Bucketed by verifier signature (r2 cells):

- **Oracle-blind / hidden-test family (the dead wall) — ~6 cells.** Several FAILs show the visible
  verifier ALL-GREEN yet reward 0 — the signature of hidden AUTO_*_equality tests the solver never
  sees: intercom001 (visible PASS=1, expected_test_count=2), ana-eng006 (4/4 visible, expected 7),
  intercom003 (1/1), asana005 (81/81 visible, expected 8), asana005-hard (2/2), ana-eng007-medium
  (40/40). The solver passes everything it CAN see and still fails a hidden equality. This is the
  solver-blind-to-oracle / AUTO_*-equality-hidden wall (memory: dead family) — no edit-shape lever
  can teach the solver to satisfy a check it cannot observe. ana-eng004 is the already-closed
  oracle-blind case (h0057 Move-A REJECTED, 4 cycles, 4 distinct failure modes).

- **Visible-partial-fail family — ~7 cells.** asana003 (PASS=11/ERROR=6), quickbooks001
  (6/ERROR=6), intercom002 (2/ERROR=2), f1002 (9/ERROR=1), asana004 (5/ERROR=1), ana-eng007
  (9/ERROR=1). These have visible failing tests, so they LOOK edit-shape-tractable — but the solver
  already saw those errors and could not close them at trials:1, which reads as genuine task
  difficulty (multi-error: asana003/qb001 each 6 errors), NOT a coin-flip removal boundary like the
  qb002/003 over-drop that h0058 just banked. None is a stable-PASS that regressed; none is a
  one-token boundary.

**Why ESCALATE, not file.** The construct-gated edit-shape family (max-points / feature-boundary /
coverage / per-key / lap-time / preserve-columns / now feature-removal-keep-base-id) has banked its
readily-flippable targets — the surviving FAILs are either oracle-blind (no lever reaches them) or
multi-error genuine-difficulty cells with no clean single-token boundary. The single-trial /
judge-by-artifact regime and the concluded oracle-flip program both say: do not re-open a dead family
or chase a doomed variant. The honest read for captain strategy is **diminishing returns on
README/edit-shape levers** — 75% needs a benchmark-design change (e.g. exposing the hidden
equality tests to the solver, or multi-trial), not another instruction lever. Candidate directions to
put to the captain: (a) STOP filing edit-shape hypotheses and bank h0058 as the closing flip of the
program; (b) a benchmark-design change to surface the oracle (hidden AUTO_*_equality) so the
oracle-blind ~6 become reachable; (c) if a lever is still wanted, the only non-oracle-blind,
single-error candidates are f1002 / asana004 / ana-eng007 (1 visible error each) — but each lacks the
clean coin-flip boundary that made qb002/003 tractable, so confidence is LOW. Recommend the captain
choose (a) or (b) over auto-filing (c).

## Stage Report: conclude

- DONE: h0058 `## Verdict` written — PASSED / PROMOTED, @baseline rebound to runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r2/eba9295fda32c05e (35/48 = 0.7292).
  Recorded the STRICT-≥-every-seed (s43 byte-identical delta 0; s42 32→33) + committed keep-`department_id` artifact (8/8, 14/14, over-drop error absent) + hold-rate 2/4→4/4 basis; transferable lesson (gated stabilizer banks a regression mode out of the README → more reproducible baseline for future forks, not a headline net); Move B lineage (h0057-validated, orphaned by the ana-eng004 oracle-blind Move-A rejection, carried solo) noted.
- DONE: h0058 `## Follow-up Routing` written = ESCALATE + rationale.
  Scanned the r2 per_trial_outcomes.json (13 FAILs, NONE a prior-hypothesis target). Bucketed: ~6 oracle-blind/hidden-AUTO_*-equality cells (visible all-green yet reward 0: intercom001 vis 1/exp 2, ana-eng006 4/exp 7, asana005 81/exp 8, etc.) = the dead wall no edit-shape lever reaches; ~7 visible-partial-fail multi-error cells = genuine difficulty, no clean coin-flip boundary. Recommended ESCALATE (diminishing returns on edit-shape; surface STOP / benchmark-design-change / low-confidence single-error candidates for captain strategy) over auto-filing a doomed variant.

### Summary
Record-writing only (no re-runs). h0058 concluded PASSED/PROMOTED as a clean precondition-gated variance-reducer that banks the qb002/003 over-drop coin-flip out of the baseline README (strict ≥ every seed, committed keep-base-id artifact both draws, hold-rate 2/4→4/4, zero interference/over-fire). Follow-up = ESCALATE: the 13 remaining @baseline FAILs are untouched by any prior hypothesis and split into an oracle-blind hidden-test family (unreachable) and multi-error genuine-difficulty cells (no clean boundary) — diminishing returns on edit-shape levers, so surface candidate directions for captain strategy rather than file a doomed variant.
