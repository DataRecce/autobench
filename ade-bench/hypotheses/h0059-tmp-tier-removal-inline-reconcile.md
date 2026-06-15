---
id: h0059
title: Tmp/intermediate-tier removal — behavior-preserving INLINE + before/after RECONCILE rule, to flip asana003 (the last bankable flipped FAIL) 35→36
status: conclude
kind: hypothesis
source: "Captain request 2026-06-15. asana003 is the ONLY remaining flipped FAIL at @baseline h0058 (35/48) — every other FAIL is never-passed (0/N research bets) or oracle-blocked. asana003 = behavior-preserving refactor (delete tmp tier, point stg at source); pass-vs-fail forensic = CONSERVATIVE inline (pass) vs BROAD re-derive (fail → cascade + cast('None' as date) crash). A pre-smoke single-cell PROBE (runs/ade-bench-probe-asana003-tmp-inline-reconcile/674cac4f64b68f82) PASSED 17/17 with the rule artifact-confirmed FIRED (inlined exact tmp SELECT + ran the before/after reconciliation: 22/22 pre → 11/11 post, columns/row counts matched). Forks the current @baseline h0058 (runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r2/eba9295fda32c05e, 35/48)."
started: 2026-06-15T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`asana003` is the **last bankable flipped FAIL** on the board. At @baseline h0058 (35/48) the 13
FAILs are: asana003 (flipped, 15/26 hist — has passing artifacts) + 12 never-passed (0/N) research
bets (ana-eng004/006/007/-medium, asana004/005/005-hard, f1002, intercom001/002/003, quickbooks001).
So asana003 is the only cell where we have a proven-correct target to copy, and the only realistic
single flip to reach **36/48**.

The task: *"Fivetran is updating their Asana package, remove all models in the tmp folder and have
the stg_asana__[name].sql models reference the source tables directly."* This is a
**behavior-preserving refactor** — delete the tmp tier, rewire each `stg_asana__*` to read `source()`
directly, with **output unchanged**. The verifier checks equality on `asana__task/project/tag` +
six `int_asana__*` models, plus `check_model_sources` (each stg model must have 0 refs / ≥1 source).

The pass-vs-fail fork (forensic):
- **PASS** = CONSERVATIVE inline: copy the deleted tmp model's exact SELECT (columns/casts/aliases)
  into the stg model, swap only `ref(tmp)`→`source()`. Output stays byte-identical → all equality
  tests pass.
- **FAIL** = BROAD re-derive: re-select fresh against the source → drops/renames/re-casts columns →
  cascade equality failures + the `cast('None' as date)` crash (empty `asana__task` → downstream
  `run_query('min(created_at)')` returns None). asana003's ~58% rate is the solver coin-flipping
  between these two.

**Why this is pin-able (unlike the ana-eng004 oracle-blind miss):** a behavior-preserving refactor
has a **locally-computable correct answer** — whatever the project produced BEFORE the refactor. So
the rule can carry its own **oracle-free reconciliation** (capture before, confirm after == before),
the double-entry pattern. This is the cleanest, most transferable lever form yet — it does not encode
asana003's answer; it makes the solver verify behavior-preservation against the local before-state.

**Falsifiable claim (one scoped README edit — Implementation stage only):** adding a gated
worked-example rule — "a tmp-tier-removal refactor is a behavior-preserving rewire: inline the deleted
tmp model's EXACT select, swap only `ref`→`source`, and RECONCILE before==after columns/types/row
counts; a clean `dbt run` is not sufficient proof" — will make the committed `stg_asana__*` models
inline (not re-derive) and reconcile, flipping `asana003` FAIL→PASS **reproducibly across ≥3
seed-perturbed draws**, with no canary regression.

**Pre-smoke PROBE evidence (artifact-confirmed RULE FIRED, not a lucky draw):** a single-cell probe
(`runs/ade-bench-probe-asana003-tmp-inline-reconcile/674cac4f64b68f82`) PASSED 17/17, strict-clean.
Committed artifact: inlined the tmp SELECT into all 11 stg models (`ref`→`source` swap only); the
worker ran the reconciliation (`dbt run` 22/22 pre-refactor → 11/11 post; "all 11 row counts and
column names/types matched baseline"). The PASS corroborates byte-identical output independently (the
downstream equality cascade that crashes in FAIL runs all passed). This smoke confirms reproducibility.

**The proposed README edit (generic identifiers, Implementation stage):** the
TMP/INTERMEDIATE-TIER REMOVAL — BEHAVIOR-PRESERVING INLINE block (inline exact tmp SELECT, swap only
the FROM, before==after reconcile, with a BEFORE/AFTER skeleton). Generic identifiers only
(`stg_entity`/`source('pkg','entity')`) — no asana/stg_asana/tmp/department target token.

## Acceptance criteria

**AC-1 — One scoped README edit; spec differs only in `experiment:` + `solver_workflow:` (+ `seed`
on the draw variants).** README diff vs the h0058 solver adds exactly one Implementation-stage gated
block; the other seven levers + leak-guard + remaining stages byte-identical. No
`AUTO_*`/`solution__*`/`check_*`/`asana`/`stg_asana`/`tmp`/`created_at`/expected-count token; no
web-fetch token.

**AC-2 — Every score paired with a clean strict audit** (`tainted: 0`, `coverage_missing: 0`,
`captured > 0`).

**AC-3 — Decisive committed-artifact read (the rule must FIRE, not pass by luck).** For every
asana003 draw, read the committed `stg_asana__*` models from the ensign `apply_patch`: they must
INLINE the deleted tmp model's exact SELECT (swap only `ref`→`source`), NOT re-derive; and the
worker's reasoning must show the before/after reconciliation actually ran (pre-refactor build +
column/row-count compare), not just a final `dbt run`. A PASS whose artifact shows a fresh re-derive
(or no reconcile) is a LUCKY DRAW, not a credited flip.

**AC-4 — Reproducibility judged against the ~58% base rate (the coin-flip test).** Run asana003 as
**≥3 seed-perturbed draws** (probe + r1 panel + r2 + r3 = 4 total). GO requires the inline+reconcile
artifact (AC-3) + verifier PASS + clean audit on **every** draw. A fire-but-fail or a skip-reconcile
draw means the rate is not fully pinned → reassess, do not promote.

**AC-5 — No canary regression; no over-fire.** The r1 panel carries qb002/qb003 (Move-B
feature-removal holds), ana-eng003 (build/preserve base case — the new rule must NOT over-fire on a
non-tmp build), asana001 (package-family coin-flip canary), f1007 (cross-family stable). Any canary
regression is a NO-GO unless artifact-proven unrelated variance.

## Target dataset + draws

- 🎯 `ade-bench-asana003` — the flip target, run ×3 seed-perturbed:
  - **r1** (seed 42): panel = asana003 + qb002 + qb003 + ana-eng003 + asana001 + f1007 (flip + canaries)
  - **r2** (seed 43): asana003-only
  - **r3** (seed 44): asana003-only
- Plus the pre-smoke probe (seed null, PASSED) = a 4th independent asana003 draw.

GO requires asana003 PASS with the inline+reconcile artifact on all draws + every r1 canary holding.

## Honest tension with the standing decisions

- **`trials: 1` / coin-flip cell.** asana003 is ~58%; a single PASS is not proof. The ≥3-seed-draw
  design + the committed-artifact AC-3 (rule must fire) is how we tell "rule pins the rate" from
  "lucky draw." The reconcile teeth give a deterministic-ish mechanism, but reproducibility is the test.
- **Cleanest lever / not overfit.** The reconcile step is oracle-free (verifies against the local
  before-state) and the rule is a general refactor principle — would help any tmp-tier-removal task.
  It encodes no asana003 answer. This is the high-transfer double-entry/reconciliation pattern.
- **Bleed risk: LOW.** Gated to "delete tmp tier + point stg at source" refactors; ana-eng003 is the
  over-fire tripwire (a plain build/rename must not trigger the reconcile-inline rule).

Method/README change only. Forks @baseline h0058 (`solver_workflows/h0058-feature-removal-keep-base-id-stabilizer`, runtime codex); no dataset, harness, or runtime change.

## Smoke result

**GO.** asana003 flipped FAIL→PASS on **4/4 independent draws** (probe seed-null + r1 seed-42 +
r2 seed-43 + r3 seed-44) vs the ~58% base rate, and the **rule FIRED in every draw** (committed
artifact = inline of the exact tmp SELECT + an executed before/after reconciliation) — so the
streak is mechanism, not luck. All strict-clean, captured>0; all 5 r1 canaries held including the
over-fire tripwire. This pins asana003 → **35 → 36 candidate** on the cleanest (oracle-free
reconciliation) lever in the program.

Run-dirs: r1 `…-r1/dafb7977973a688b` (panel, 6/6) · r2 `…-r2/37a10aa3779bda63` (1/1) ·
r3 `…-r3/a7a653fa9e46c0db` (1/1) · probe `…-probe…/674cac4f64b68f82` (1/1). Strict audit on each:
`tainted 0 / coverage_missing 0`, captured>0.

### asana003 flip — the decisive AC-3/AC-4 read (rule fired = not luck)

| Draw | Seed | asana003 | Inline (not re-derive)? | Reconcile actually ran? | Verdict |
|------|------|----------|--------------------------|--------------------------|---------|
| probe | null | PASS | ✅ inlined exact tmp SELECT, ref→source | ✅ 22/22 pre → 11/11 post, cols/rows matched | RULE FIRED |
| r1 | 42 | PASS | ✅ inlined, only FROM swapped | ✅ `dbt show` metadata capture; row recon all matched (project 16, tag 17, task 1, …); `column_metadata_mismatches=0` | RULE FIRED |
| r2 | 43 | PASS | ✅ inlined; **caught+reverted an intermediate re-derive failure via the reconcile** | ✅ 22 baseline → 11 final; schemas/types/rows matched all 11 | RULE FIRED |
| r3 | 44 | PASS | ✅ inlined (`select *` bodies, FROM→source) | ✅ **row-fingerprint (SHA256) match** before vs after, all 11 | RULE FIRED |

**asana003 pass count: 4/4, rule fired 4/4.** Pure-luck probability of 4/4 on a 58% cell ≈ 11% —
but the committed-artifact reads show the inline+reconcile mechanism drove every pass, so this is
not the luck tail. R2 is the strongest single proof: the reconcile step *caught* a re-derive that
would have failed and forced the revert — the teeth working exactly as designed.

### Canary panel (r1, AC-5) — all hold, no over-fire

| Canary | Role | r1 |
|--------|------|----|
| quickbooks002 | Move-B feature-removal hold | ✅ PASS |
| quickbooks003 | Move-B feature-removal hold | ✅ PASS |
| ana-eng003 | **over-fire tripwire** (build/preserve — the new rule must NOT fire on a non-tmp build) | ✅ PASS (rule correctly silent) |
| asana001 | package-family coin-flip canary | ✅ PASS |
| f1007 | cross-family stable | ✅ PASS |

Zero regression; the tmp-tier rule did not over-fire on ana-eng003 (a plain build, no tmp tier).

**Verdict: GO → full.** The flip is artifact-real and reproducible (4/4, rule fired each time), the
lever is oracle-free (reconciles against the local before-state, encodes no answer), and canaries
hold. Per the standing two-draw promote precedent (h0052/h0056/h0058), the full verdict is provisional
pending ≥2 seed-perturbed full 48-task draws clearing @baseline h0058's expectation (~34) — but unlike
a coin-flip flip, the reconcile mechanism gives strong reason to expect asana003 reproduces at full.

## Run launch (full stage record)

Two concurrent seed-perturbed FULL 48-task draws launched detached (2026-06-15) to bank asana003 →
36/48 and check board-wide no-regression vs @baseline h0058 (35/48,
`runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r2/eba9295fda32c05e`).

| Draw | Seed | Experiment | Frozen spec | sealed_hash |
|------|------|------------|-------------|-------------|
| full-r1 | 42 | ade-bench-h0059-tmp-tier-removal-inline-reconcile-full-r1 | specs/h0059-tmp-tier-removal-inline-reconcile-full-r1.frozen.yaml | 88cdb3fb570792c9b5348538972bfd37 |
| full-r2 | 43 | ade-bench-h0059-tmp-tier-removal-inline-reconcile-full-r2 | specs/h0059-tmp-tier-removal-inline-reconcile-full-r2.frozen.yaml | 50efe7bf0eead51da71ef3565d97c015 |

Both variants differ from the 48-task base full spec
(`specs/h0059-tmp-tier-removal-inline-reconcile.yaml`) ONLY in `experiment:` + `sampling.seed:` —
no `benchmark.tasks` added (`tasks: null` in both frozen specs = full 48). Distinct sealed_hashes
(CAS-buster confirmed).

Handle dirs (FO owns the sentinel scan; ensign did NOT wait):
- full-r1: `/home/kent/autobench/ade-bench/runs/.rk-handles/h0059-full-r1-20260615-045341/`
  (supervisor pid 3737424 → uv 3737439 → rk python 3737442; log `…/log`; sentinel `…/done` absent)
- full-r2: `/home/kent/autobench/ade-bench/runs/.rk-handles/h0059-full-r2-20260615-045346/`
  (supervisor pid 3737585 → uv 3737600 → rk python 3737603; log `…/log`; sentinel `…/done` absent)

ntfy topic: adebench-rk-381c976fe07465bf. Both up to ~7hr. FO handles audit + score + paired-delta
when both sentinels land.

## Stage Report: full

- DONE: Two seed-variant FULL specs built from specs/h0059-tmp-tier-removal-inline-reconcile.yaml (the 48-task base, NO benchmark.tasks); full-r1 = experiment ...-full-r1 + seed 42; full-r2 = experiment ...-full-r2 + seed 43; each differs from the base full spec ONLY in experiment: + sampling.seed: (CAS-buster); both frozen with rk freeze --allow-missing; distinct sealed_hashes confirmed.
  diff vs base = only experiment:+seed: lines; frozen tasks: null (full 48); sealed_hash r1 88cdb3fb / r2 50efe7bf (distinct).
- DONE: Both full runs launched CONCURRENTLY and DETACHED via drivers/rk-run-detached.sh (keys h0059-full-r1 and h0059-full-r2, mode run); the two handle dirs under runs/.rk-handles/ returned with pid/log paths; ensign returns immediately and does NOT wait (the FO owns the sentinel scan).
  handles runs/.rk-handles/h0059-full-r1-20260615-045341 (pid 3737424) + h0059-full-r2-20260615-045346 (pid 3737585); did not poll completion.
- DONE: Both handles confirmed live (pid alive + rk run child spawned) before returning; the exact two handle-dir paths reported.
  supervisors ALIVE; rk python children 3737442 (r1) / 3737603 (r2) confirmed via ps tree; both done sentinels absent.

### Summary

Built the two seed-perturbed FULL 48-task variant specs (seeds 42/43) from the AC-1-verified base full
spec, froze both (distinct sealed_hashes 88cdb3fb / 50efe7bf), and launched both concurrently DETACHED.
Confirmed both supervisor pids alive with rk-run children spawned and done sentinels absent, then returned
without waiting. Notable: variants are pure experiment:+seed: deltas with tasks: null (true full 48, no
selector) — the FO scans runs/.rk-handles/*/ for the two sentinels, then audits + scores + paired-delta.

## Run result

**Headline (plain words):** asana003 — the lever's only target — flipped FAIL→PASS in BOTH full
draws (6/6 across smoke + full), and the committed artifact proves the inline+reconcile rule FIRED,
not luck. But the two-draw net lands at **35 / 34 (mean 34.5)**, flat-to-down vs **@baseline h0058 =
35/48**. The asana003 +1 was washed out by off-construct coin-flips (f1001, quickbooks004, f1003-hard)
on the longer-README draws — none of which the lever touched. The flip is real and reproducible; the
board-level net is inside the noise floor.

### Absolute scores + audit (AC-2)

| Run | Seed | Run-dir | Score | Strict audit (clean / cov_missing / tainted) |
|-----|------|---------|-------|----------------------------------------------|
| @baseline h0058 | 43 | runs/ade-bench-h0058-feature-removal-keep-base-id-stabilizer-r2/eba9295fda32c05e | **35/48 = 0.7292** | — |
| full-r1 | 42 | runs/ade-bench-h0059-tmp-tier-removal-inline-reconcile-full-r1/97c03e6c467742f8 | **35/48 = 0.7292** | 48 / 0 / 0 ✅ |
| full-r2 | 43 | runs/ade-bench-h0059-tmp-tier-removal-inline-reconcile-full-r2/1fcc9223b9de5194 | **34/48 = 0.7083** | 48 / 0 / 0 ✅ |

Absolute vs paper_baseline 0.1875: r1 = 3.89× paper, r2 = 3.78× paper. Both strict-clean
(`rk audit --policy strict` → clean=48, coverage_missing=0, tainted=0); asana003 cell `captured=1>0`
in both draws. `stratified_pass_at_1` == raw pass rate here.

### Paired per-task ledger (computed from per_trial_outcomes.json, paired by slug — `rk runs diff`
TypeErrors on these run-dirs, query_id null; harness data-shape limitation, not a run defect)

vs @baseline h0058 r2 (seed43), 48/48 slugs paired. Verdict CHANGES in BOTH directions:

| Task | @baseline (h0058 r2) | full-r1 (s42) | full-r2 (s43) | Direction | Mechanism |
|------|----------------------|---------------|---------------|-----------|-----------|
| **asana003** | F | **P** | **P** | **gain (BOTH draws)** | THE lever flip — inline+reconcile rule FIRED (artifact-confirmed below) |
| f1003-hard | P | **F** | P | regression (r1 only) | off-construct: `count_answers` aggregate test FAIL 1; rule did NOT fire (0 asana mentions) |
| f1001 | P | P | **F** | regression (r2 only) | off-construct: F1 standings/races/results src+stg model task; `src_models_are_correct` ERROR + 3 stg-source FAILs; rule did NOT fire |
| quickbooks004 | P | P | **F** | regression (r2 only) | off-construct: quickbooks double-entry / xr_var toggle (48 expected tests); rule did NOT fire |

All 44 other tasks: unchanged across baseline / r1 / r2. Net: r1 = 35 (asana003 +1, f1003-hard −1 →
flat), r2 = 34 (asana003 +1, f1001 −1, qb004 −1 → −1).

### The SIX required analyze questions

1. **Net + full ledger (both directions).** Above. Gains: asana003 (both draws). Regressions:
   f1003-hard (r1), f1001 (r2), quickbooks004 (r2). Net r1=35 (=baseline), r2=34 (−1 vs baseline),
   mean 34.5. Same-seed-43 apples-to-apples (r2 vs h0058 r2, both seed43): asana003 +1, f1001 −1,
   qb004 −1 → 35→34. Same-seed-42 (r1 vs h0058 seed42=33): asana003 +1, f1001 +1, f1003 +1,
   f1003-hard −1 → 33→35. The asana003 +1 is real in every framing; the ±-other tasks are the
   trials:1 noise band (~±3) and flip both ways depending on seed.
2. **Smoke vs full.** Smoke was a GO on a 6-task r1 canary panel (asana003 + qb002/qb003/ana-eng003/
   asana001/f1007) + asana003-only r2/r3 + probe. The panel deliberately sampled the lever target and
   its near-family canaries — it could NOT see f1001 (F1 standings), f1003-hard (F1 aggregate), or
   quickbooks004 (qb double-entry toggle), which are off-construct coin-flip cells unrelated to the
   tmp-tier rule. The full board surfaced their independent variance. The asana003 flip itself did
   NOT drift between smoke and full — it held 6/6.
3. **Already-correct-and-broken.** All three regressions were PASSING at @baseline (damage to working
   code, not "failed to help"). BUT: the lever did not cause the damage — see Q4. These are passers
   that flipped on their own trials:1 variance, amplified (if at all) only by the longer README
   shifting unrelated solves (README-length perturbation), not by the rule firing on them.
4. **Was the change executed? (the decisive read.)**
   - **asana003 (gain): executed-and-helped, BOTH draws.** Committed `apply_patch` inlines all 11
     `stg_asana__*` models — each changes ONLY `ref('..._tmp')`→`source('asana','..')` in the FROM
     and in `get_columns_in_relation(...)`; the `fill_staging_columns`/`get_*_columns()` macro bodies
     are untouched (= exact tmp SELECT preserved, NOT a re-derive), plus `*** Delete File:` for the
     tmp models. Reconcile genuinely ran: r1 captured baseline build (38 models/51 tests) + DuckDB
     Python row/column snapshot → post-change (27 models) → "before/after reconciliation matched for
     all eleven staging models." r2 likewise (22 baseline models → reconcile "row counts and ordered
     column/type signatures match the baseline"); r2's tmp bodies were `select * from {{var(..)}}`, so
     it faithfully kept `FROM {{var(..)}}` and used `source()` only for column introspection — a
     faithful inline, not a re-derive. Both: `asana__task` built OK, `cast('None' as date)` crash
     ABSENT, 17/17 tests + `check_model_sources` PASS.
   - **f1001 / f1003-hard / quickbooks004 (regressions): inert w.r.t. the lever.** Zero `asana`
     mentions, zero tmp-deletion / ref→source-swap action in any of the three ensign sessions — the
     tmp-tier-removal rule did NOT fire. Its precondition ("delete tmp tier + point stg at source"
     asana-package refactor) cannot match an F1 src/stg-model task, an F1 `count_answers` aggregate,
     or a quickbooks xr_var toggle. Classification: **off-construct trials:1 variance / README-length
     perturbation, NOT lever bleed.**
5. **Prevention + next move.** The flip is artifact-real but the net is washed by off-construct
   coin-flips at trials:1. Prevention of false-promote: judge this flip by construct + committed
   artifact + reproducibility (4 smoke + 2 full = 6/6, rule fired every time), the h0052/h0058
   banking precedent — NOT by single-draw net, which is dominated by ~±3 noise on flip-flop cells
   (f1001, qb004 are documented flip-floppers; f1003/f1003-hard noisy). To establish whether asana003
   lifts the *expectation* would need more seed-perturbed full draws. Recommended next step: see the
   PROMOTE recommendation — escalate to the captain; do not reflexively file a successor (the
   single-flip-on-trials:1 ceiling is structural, not a lever gap).
6. **Smoke-vs-full fork drift.** The smoke GO was artifact-real for its claim (asana003 flips via the
   rule) and that held at full — no drift on the target. What changed at full was NOT the lever's
   fork: three OFF-CONSTRUCT passers (families the smoke panel did not sample) flipped on their own
   single-trial variance. The README rule did not drift into a different implementation branch on
   asana003 (inline+reconcile both draws). The full "miss" is unrelated-variance dilution of a real
   +1, not a lever failure. No follow-up routing needed on the lever; the limit is the trials:1 noise
   floor swallowing a clean single flip.

## Behavioral analysis

### asana003 — the lever flip, artifact-confirmed in BOTH full draws (AC-3/AC-4)

| Draw | Seed | Verdict | Inline (not re-derive)? | Reconcile actually ran? | crash absent / tests |
|------|------|---------|--------------------------|--------------------------|----------------------|
| full-r1 | 42 | PASS | ✅ 11/11 stg: ONLY `ref(tmp)`→`source('asana',..)` in FROM + introspection; macro/get_*_columns() bodies untouched; tmp files deleted | ✅ baseline build (38 mdl/51 tests) + DuckDB Python row/col snapshot → post (27 mdl) → "reconciliation matched for all eleven" | ✅ `asana__task` OK, no `cast('None' as date)`; 17/17 + check_model_sources PASS |
| full-r2 | 43 | PASS | ✅ 11/11 stg: tmp bodies were `select * from {{var}}`, faithfully kept `FROM {{var}}`, `source()` for introspection only (var() returns no cols to get_columns_in_relation) | ✅ baseline 22 mdl materialized → DuckDB row+ordered col/type signature → post 27 mdl → "row counts and ordered column/type signatures match the baseline" | ✅ same — crash absent, 17/17 + check_model_sources PASS |

Cross-ref the smoke deep-dive (`_artifacts/h0059-three-run-deep-dive.md`): probe + r1/r2/r3 smoke all
showed the same inline+reconcile artifact. Combined with these two full draws = **asana003 PASS 6/6,
rule FIRED 6/6**. The reconcile teeth worked as designed (r2 smoke even caught and reverted a
re-derive live). This is mechanism, not the luck tail of a 58% cell.

### Per-regressor off-construct verdict (the load-bearing read for the promote call)

- **f1003-hard (r1 P→F).** F1 `count_answers` aggregate task; failed `count_answers` (FAIL 1). Zero
  asana/tmp activity in the ensign session. Off-construct trials:1 variance. NOT lever bleed.
  (f1003-hard noisy historically.)
- **f1001 (r2 P→F).** F1 standings task (races/results/standings + src/stg models); failed
  `src_models_are_correct` (ERROR) + `stg_models_use_src_models`/`stg_races`/`stg_results`
  uses-correct-sources (FAILs). This is its OWN src→stg construct, not the asana tmp tier; rule's
  precondition cannot match. Off-construct variance / README-length perturbation. NOT lever bleed.
  (f1001 is a documented flip-flopper — memory note.)
- **quickbooks004 (r2 P→F).** Quickbooks double-entry / multi-currency `xr_var` toggle, 48 expected
  AUTO_* tests. No asana/tmp activity. A complex multi-model coin-flip cell (qb004 documented
  flip-flopper). Off-construct variance. NOT lever bleed.
- **f1003 gain note.** Dispatch flagged an f1003 F→P; that gain is only vs h0058 *seed42* (33).
  Against @baseline (h0058 r2, seed43) f1003 was already P and stayed P in both draws — no change.
  Listed for completeness; off-construct either way (F1 aggregate, rule silent).

**AC-1/AC-5 confirmations.** README delta vs h0058 = exactly one added Implementation-stage gated
block (the TMP/INTERMEDIATE-TIER REMOVAL — BEHAVIOR-PRESERVING INLINE section, ~27 added lines,
generic `stg_entity`/`source('schema','table')` identifiers only — no asana/stg_asana/tmp/created_at/
AUTO_* token). The longer README is the only plausible cross-task perturbation vector, and it shifts
unrelated solves (README-length), it does not fire the gated rule off-target. All 5 r1 smoke canaries
held (qb002/qb003/ana-eng003 over-fire tripwire/asana001/f1007) — over-fire AC-5 clean at smoke.

### PROMOTE recommendation (artifact-grounded; decision is the captain's)

asana003 is a **verified 6/6 reproducible inline+reconcile flip** — the committed artifact proves the
rule fired (exact tmp SELECT inlined, ref→source swap only, before==after reconciliation executed) in
all four smoke draws and both full draws, with the `cast('None' as date)` crash absent and equality +
check_model_sources passing every time. The lever is the cleanest in the program: oracle-free
(reconciles against the local before-state, encodes no answer) and a general refactor principle. BUT
the two-draw full net is **35 / 34 (mean 34.5), flat-to-down vs @baseline 35** — the asana003 +1 is
swallowed by off-construct coin-flips (f1001, quickbooks004, f1003-hard), none of which the rule
touched (artifact-confirmed inert). At trials:1 a single clean flip cannot clear the ~±3 noise floor
when 3+ documented flip-flop passers wobble on the same draws.

Three options for the captain:
1. **Bank asana003 by construct + artifact + reproducibility** (the h0052/h0058 precedent), accepting
   a flat board net. Justification: the flip is mechanism-proven and the regressors are proven
   off-construct variance, so the lever's *expected* contribution is +1; the measured wash is
   noise, not lever harm. This is the strongest evidence-per-flip in the program.
2. **Run additional seed-perturbed full draws** (e.g. seeds 44/45) to test whether asana003 lifts the
   board *expectation* above 35 — i.e. whether the +1 survives averaging once the off-construct
   flip-flops cancel. Costs ~2 more 7hr runs.
3. **Conclude validated-but-net-washed:** record asana003 as a verified reproducible flip that the
   trials:1 noise floor structurally prevents from banking as a board +1, and stop (no successor —
   the single-flip ceiling is a benchmark-design limit, not a lever gap).

My artifact-grounded lean: **(1) bank by construct + artifact**, consistent with the standing
single-trial / judge-by-artifact captain decision and the h0052/h0058 banking precedent — the flip is
the most mechanism-proven in the program and the dilution is demonstrably off-construct noise. If the
captain wants a board-number guarantee rather than an artifact verdict, (2) is the clean fallback.

## Stage Report: analyze

- DONE: `## Run result` written — paired per-task ledger for BOTH draws (full-r1 seed42 97c03e6c = 35/48, full-r2 seed43 1fcc9223 = 34/48) vs @baseline h0058 (35/48), both strict-clean (clean=48/0/0); every verdict change in BOTH directions with mechanism; all SIX required questions answered. asana003 = the lever flip, F→P in BOTH draws (6/6 across smoke+full).
  Ledger computed from per_trial_outcomes.json (rk runs diff TypeErrors, query_id null); scores via rk score; audits via rk audit --policy strict (summary {clean:48,coverage_missing:0,tainted:0} each); asana003 captured=1.
- DONE: asana003 committed-artifact CONFIRMED at full (both draws) — inline+reconcile shape (exact tmp SELECT inlined, ref→source swap only, before==after reconciliation ran), NOT a broad re-derive; cast('None' as date) crash absent; equality + check_model_sources PASS.
  Read ensign apply_patch in agent/sessions/*.jsonl (custom_tool_call apply_patch) + reconcile reasoning; r1 macro bodies untouched, r2 faithfully kept FROM var() with source() introspection; cross-ref _artifacts/h0059-three-run-deep-dive.md.
- DONE: REGRESSOR classification — f1001 (P→F r2), f1003-hard (P→F r1), quickbooks004 (P→F r2), AND the f1003 gain (vs seed42 only): tmp-tier rule did NOT fire on any (0 asana mentions, no tmp-delete/ref→source action); each verdicted off-construct trials:1 variance / README-length perturbation, NOT lever bleed; PROMOTE recommendation given (bank-by-artifact lean).
  Grepped each regressor ensign session for asana/tmp/ref→source firing — all empty; classified each construct (F1 standings/aggregate, qb xr_var toggle); 3 options laid out, decision left to captain.

### Summary

Confirmed the asana003 inline+reconcile flip is artifact-real and reproducible in BOTH full draws
(6/6 with smoke, rule fired every time — exact tmp SELECT inlined, ref→source swap only, before==after
reconcile executed, crash absent, 17/17 + check_model_sources PASS). The two-draw net is 35/34 (mean
34.5), flat-to-down vs @baseline 35: the real +1 is washed by three off-construct coin-flip passers
(f1001, quickbooks004, f1003-hard) on which the tmp-tier rule provably did NOT fire — off-construct
trials:1 variance, not lever bleed. Recommendation: bank asana003 by construct + artifact +
reproducibility (h0052/h0058 precedent) accepting flat net, or run more seed draws; captain decides.
