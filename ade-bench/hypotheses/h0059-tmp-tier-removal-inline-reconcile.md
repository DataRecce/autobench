---
id: h0059
title: Tmp/intermediate-tier removal — behavior-preserving INLINE + before/after RECONCILE rule, to flip asana003 (the last bankable flipped FAIL) 35→36
status: full
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
