---
id: h0009
title: Exploration — reproduce the installed dbt package's conventions (grain, active-filter, dedup, column set) instead of hand-rolling
status: conclude
kind: hypothesis
source: forked from the h0005 @baseline (622bdedac572b479, 31/48 = 0.6458) 17-failure raw-log analysis + h0007's rejection note (surviving direction #2 — "improve the solver's up-front understanding so it does not form the wrong mental model"). Queued behind h0008; both attack the same failures from different stages (Finalization invariants vs Exploration root-cause). solver_workflows/codex-ade-dbt-minimal at fork (re-fork from whatever @baseline is when this fires).
started: 2026-06-03T14:07:16Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

A large share of the `@baseline` failures sit on **Fivetran-package** datasets
(asana, intercom, quickbooks — ~8 of 17) whose canonical answer closely mirrors the
modeling conventions of the dbt package already installed in the local `dbt_packages/`
tree. The solver fails them by **hand-rolling a plausible-but-divergent transformation**
instead of reproducing the installed package's idioms: it skips the `_fivetran_active`
active-record filter (intercom grain: 2 expected vs 5 emitted), invents a join grain that
drops base-entity rows (asana `int_asana__project_user_agg`), or misses a package-shaped
cast (asana002 `due_at::timestamp`). The package source is a **local, leak-guard-allowed**
signal the solver under-uses.

**Falsifiable claim (the single README change — Exploration stage only):** the seed
solver's Exploration prose inspects project files generically but does NOT direct the
solver to study and reproduce the conventions of any dbt package already present in
`dbt_packages/`. Adding one Exploration instruction — *when the project embeds a known dbt
package (e.g. a Fivetran `*_source`/staging package in `dbt_packages/`), read that
package's existing staging/intermediate models and reproduce their conventions exactly for
the models you build or change: the active-record / `_fivetran_active` filtering, the
dedup keys, the output column set, and the grain (one-row-per-which-entity); do not
hand-roll a simpler aggregation that diverges from the package's join anchor and filters*
— will fix the root-cause mental-model error on the Fivetran cluster, flipping a material
number of those failures to passes and raising `stratified_pass_at_1` above whatever
`@baseline` is when this fires.

Distinct from h0008 (Finalization invariants, a detect-and-fix check): this is a
generative Exploration change that prevents the wrong model from being built in the first
place. One idea, one stage.

Method/README change only. Forks the then-current `@baseline` solver; no dataset, harness,
or solver-runtime change. Leak-guard intact (the package source is local — no public
fetch, no `git clone` of the upstream package, no oracle).

Target datasets (smoke, all `ade-bench-` prefixed): the Fivetran cluster —
`ade-bench-intercom001`, `ade-bench-intercom003`, `ade-bench-asana002`,
`ade-bench-asana004`, `ade-bench-asana005`, `ade-bench-quickbooks001`, plus a
stable-pass regression sentinel `ade-bench-asana001`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0009-exploration-package-fidelity.yaml` shows
only `experiment:` + `solver_workflow:`; the README diff vs the `@baseline` solver touches
only `## Stage: Exploration` (the single package-fidelity instruction), leaves
Implementation/Validation/Finalization and the dependency/package guardrails untouched, and
does not reference hidden tests or weaken the leak-guard. `agent.kind: spacedock_solver`,
`runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean,
`captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs the then-current `@baseline`.**

**Smoke gate:** must not regress the `asana001` sentinel and should flip at least one
targeted Fivetran failure to a pass before promotion to full.

## Smoke result

Smoke spec: `specs/h0009-exploration-package-fidelity.smoke.frozen.yaml` (7 tasks).
Run dir: `runs/ade-bench-h0009-exploration-package-fidelity/13ecf093adb674c2`.

**Audit + score attestation (same run-dir):**
- `rk audit … --policy strict`: CLEAN — `{clean: 7, tainted: 0, coverage_missing: 0}`; `captured = 1` on all 7 cells (subagent-trace-manifest.json confirms the `spacedock:ensign` dispatch was captured per cell).
- `rk run`: 7/7 completed, 0 errored.
- `rk score`: `stratified_pass_at_1 = 0.2857` (2/7).

**Per-task verdict vs `@baseline` (622bdedac572b479):**

| task | @baseline | h0009 smoke | delta |
|------|-----------|-------------|-------|
| ade-bench-asana001 (sentinel) | PASS (1) | PASS (1) | held — no regression |
| ade-bench-asana002 | FAIL (0) | **PASS (1)** | **FAIL→PASS flip** |
| ade-bench-asana004 | FAIL (0) | FAIL (0) | — |
| ade-bench-asana005 | FAIL (0) | FAIL (0) | — |
| ade-bench-intercom001 | FAIL (0) | FAIL (0) | — |
| ade-bench-intercom003 | FAIL (0) | FAIL (0) | — |
| ade-bench-quickbooks001 | FAIL (0) | FAIL (0) | — |

1 of 6 Fivetran targets flipped FAIL→PASS (asana002); the `asana001` sentinel held PASS (no regression). Smoke `stratified_pass_at_1` 0.2857 is a 7-task subset metric, NOT comparable to the 48-task @baseline 0.6458 — the go/no-go signal here is the per-task flip + sentinel, not the aggregate.

**Behavioral read (was the Exploration change exercised?):** Yes — the package-fidelity instruction is verbatim in the resolved solver prompt (job.log lines 380-385), so it reached every cell.
- **asana002 (the FLIP) — instruction exercised AND load-bearing.** The ensign's own stage report says it "corrected source column types to match installed `asana_source` macros" and ran a "Package column-contract check: `remaining_mismatches = 0`" — i.e. it read the installed Fivetran `asana_source` package and reproduced its column contract/types rather than hand-rolling. Verifier passed all 3 hidden tests including `AUTO_asana002…_equality`.
- **intercom001 (still FAIL) — instruction engaged but the divergence persists.** The solver DID apply active-record reasoning (its report: `thread_rows=5, matching active_part_conversations=5`), but the hidden `AUTO_intercom__threads_equality` test still returns 7 row-level mismatches. So it picked an active-record grain of 5 conversations, which diverges from the canonical answer the verifier expects — the package-read nudge moved it toward active-record thinking but not to the exact package grain/aggregation. Residual failure mode = grain/value divergence, not a "never looked at the package" gap.

**Gate recommendation: GO → full.** Clean strict audit, ≥1 targeted flip (asana002), sentinel held, and the flip is causally attributable to the Exploration change (package-contract match drove the asana002 fix). The residual intercom/quickbooks failures are value-level grain divergences that a full 48-task run is worth measuring against @baseline to see net effect.

## Run result

**Full run.** `runs/ade-bench-h0009-exploration-package-fidelity/1026ae344528e6eb`
(48/48 completed, 0 errored). `@baseline` = `runs/ade-bench-baseline/622bdedac572b479`
(31/48 = 0.6458).

**Audit + score (same run-dir).** `rk audit … --policy strict`: CLEAN —
`{clean: 48, tainted: 0, coverage_missing: 0}` (verified by team-lead). `rk score`:
`stratified_pass_at_1 = 0.625` (30/48), Wilson CI [0.4836, 0.7478]; `against_constant`
verdict `above` the 0.1875 floor.

**Paired delta vs `@baseline`.** The CLI `rk runs diff` cannot run on these two run-dirs
— ade-bench outcomes carry `query_id: null` (tasks key on `trial_name`, not `query_id`),
so `diff/pairing.py:22` raises `TypeError: int() argument … not 'NoneType'`. This is a
harness data-shape limitation, not a run defect (the strict audit on the same run-dir is
clean). I computed the paired delta directly from `per_trial_outcomes.json`, pairing by
task slug (suffix-stripped), with a 10k paired bootstrap (seed 0) matching `compute_diff`:

| metric | value |
|--------|-------|
| paired n | 48 (full overlap, no unmatched tasks either side) |
| baseline pass@1 | 0.6458 (31/48) |
| h0009 pass@1 | **0.6250 (30/48)** |
| **delta (h0009 − baseline)** | **−0.0208 (NET −1 task)** |
| paired bootstrap 95% CI on delta | **[−0.1042, +0.0625]** (straddles 0) |
| McNemar exact two-sided p (5 discordant: 2 gain / 3 regress) | **1.0000** |

FAIL→PASS gains (2): `asana002`, `f1011`. PASS→FAIL regressions (3): `f1001`,
`f1006-hard`, `quickbooks003`. **NET −1 / below baseline.** The delta is negative, its CI
straddles zero, and p=1.0 — h0009 does **NOT** clear the promotion tripwire (CI does not
exclude a regression; absolute score 0.625 < @baseline 0.6458). The change is statistically
indistinguishable from noise in aggregate while costing one net task.

## Behavioral analysis

Captain-requested deep-dive on the smoke run (`13ecf093adb674c2`), comparing each cell's
agent/ensign transcript + distance-to-pass against the same task in `@baseline`
(`622bdedac572b479`). Distance-to-pass (`Got N` mismatch count) is **identical** in both
runs for all 5 non-flips; only `asana002` moved.

**The flip (`asana002`) is causal, high confidence.** Both runs peeked at `dbt_packages/`,
but only h0009 acted on the package's full contract. Baseline added the 3 missing columns
(`_fivetran_synced`, `liked`, `num_likes`) but left existing column **types** unfixed →
2-row equality miss. h0009, following "reproduce the package's conventions exactly,
including the output column set," went deeper and corrected source column **types** to
match the installed `asana_source` macros (the ground-truth fix is `due_at::timestamp`) →
3/3 PASS. Baseline omitted exactly what the package defines and what the solution requires;
h0009 copied it. Not run-to-run noise. *(Caveat: the specific `due_at` column is inferred
from h0009's "matched the column contract, remaining_mismatches=0" note + the solution; the
mechanism is solid.)*

**Zero narrowing on the 5 non-flips — three distinct reasons:**

1. **No package model to copy (`asana004`, `asana005` — `Got 3`, unchanged).** The target
   `int_asana__project_user_agg` is a NEW bespoke model with no analog in `asana_source`,
   so "copy the package" had nothing to point at. Both runs hand-rolled the identical bug:
   aggregate off `project_user` (13 projects with users) instead of the `project` table
   (16), dropping the 3 zero-user projects.
2. **Copied the filter, not the grain (`intercom001`, `intercom003` — `Got 7`, unchanged).**
   The instruction *did* fire — h0009 applied `where coalesce(_fivetran_active, true)` from
   the package's staging convention. But the real bug is the **spine/join direction**: the
   canonical `intercom__threads` builds `from latest_conversation (conversation_history,
   active) LEFT JOIN latest_conversation_part` — one row per active conversation, incl. the
   2 with zero parts. h0009 (like baseline) built FROM the parts table and grouped upward →
   the 5 conversations that have parts, missing the 2 zero-part rows. It copied the easy
   surface convention and skipped the hard structural one. NB: the intercom **transform**
   package (which encodes this spine) is NOT installed — only `intercom_source` (staging) —
   so "copy the package model" cannot supply the fix here; a generative grain rule must.
3. **Never triggered (`quickbooks001` — 6 fails, unchanged).** The `quickbooks_source`
   package literally contains the 3 missing staging models, but the task is framed
   "the project is erroring — fix it." h0009 fixed the one visible compile error, the
   project built green, and it stopped — it noted the package exists but never opened
   `dbt_packages/quickbooks_source/models/`. The instruction is scoped to "models you build
   or change," so a passive fix-it task never activated it.

**Cross-cutting discovery (drives h0010):** 4 of the 5 non-flips (`asana004`, `asana005`,
`intercom001`, `intercom003`) are the **same root cause** — *built from the child/event
table and grouped upward, silently dropping parent entities with no children* (the wrong
grain spine). A single generative Implementation rule ("build one-row-per-entity models
FROM the entity table as the spine, LEFT JOIN aggregated children") targets all four. This
is the h0008 grain idea moved from an inert *Finalization check* to a generative
*construction rule* — filed as **h0010**. `quickbooks001` is a separate coverage/discovery
gap (a fix-it-task completeness lever), noted for a later hypothesis.

**Verdict on h0009 as written:** the package-fidelity lever is **real but narrow** — it
flips a failure only when the failing model has a direct package analog AND the solver is
actively authoring it (`asana002` hit both; the others each missed one). Net effect on the
full 48 is expected to be small. The higher-leverage finding is h0010 (grain spine, 4
candidate flips from one rule).

### Full-run deep-dive (1026ae344528e6eb vs @baseline)

The smoke read predicted "narrow gain, small net." The full run is **worse than that — NET
−1**: 2 gains, 3 regressions. The decisive new evidence is the **3 regressions, all on
non-target tasks** that the smoke set could not see. The same instruction that helped on the
one task with a clean package analog (`asana002`) caused **convention bleed** on three tasks
where "match the package" was the wrong move.

**The 3 regressions — each a distinct over-modification driven by the instruction:**

1. **`f1001` (1→0): renamed source models to a package-style grain the hidden tests reject.**
   Baseline built `src_circuits`, `src_constructor_results`, … — the exact names the hidden
   structural tests check (`src_models_are_correct`, `stg_models_use_src_models`,
   `stg_races_uses_correct_sources`); 6/6 PASS. h0009 renamed them to
   `src_f1_dataset__circuits`, `src_f1_dataset__constructor_results`, … — a **Fivetran
   `src_<dataset>__<entity>` naming convention**. f1 is **not** a Fivetran package; there is
   no package to reproduce. The rename broke `src_models_are_correct` (compile error:
   `'dict object' has no attribute 'model.f1.src_circuits'`) plus the two
   `stg_*_uses_correct_sources` ref-checks → 4/6 fail. Pure convention bleed: the instruction
   ("reproduce the package's … grain / column set / naming") was applied to a project with no
   package, manufacturing a divergence from a previously-correct, test-shaped naming.

2. **`quickbooks003` (1→0): trimmed columns to match the package staging contract, dropping
   columns the solution requires.** Baseline 14/14 PASS. h0009 11/14 — the 3 failures are
   equality compile-errors: `int_quickbooks__expenses_union`, `int_quickbooks__sales_union`,
   and `quickbooks__ap_ar_enhanced` each "**has less columns than** solution__…". The
   instruction told the solver to "reproduce the package's … output column set"; here the
   installed `quickbooks_source` package defines the *staging* contract, and the solver
   shaped its *intermediate/final* models to that narrower staging column set rather than the
   wider set the task's solution defines. The package fidelity pull actively *removed*
   columns that baseline had kept. This is the mirror image of the asana002 win — there,
   copying the package contract added the right columns; here, copying it dropped the right
   columns.

3. **`f1006-hard` (1→0): value-level divergence, weakly attributable.** Baseline 4/4 PASS;
   h0009 fails `AUTO_constructor_points_equality` with `Got 2` (2 rows differ), the other 3
   pass. No package analog on f1 (formula1, not Fivetran), so the mechanism is not
   package-contract bleed; this is a 2-row value drift on a "-hard" task. Best read as
   run-to-run instability rather than a clean causal effect of the instruction — but it lands
   on the regression side of the ledger regardless, and a method change whose *net* sign is
   negative cannot lean on "one of the three regressions might be noise."

**The 2 gains:**

- **`asana002` (0→1): causal, package-fidelity win (same as smoke).** The ensign read the
  installed `asana_source` Fivetran package and corrected source column **types** to match
  its macros (`remaining_mismatches = 0`); 3/3 hidden tests PASS incl.
  `AUTO_asana002…_equality`. This is the one task where a package analog existed AND the
  solver was authoring the matching model — the lever working as designed.
- **`f1011` (0→1): incidental, NOT attributable to the instruction.** f1011 is a formula1
  task with no Fivetran package present, so the package-fidelity instruction had nothing to
  act on. The 6 option-check tests now pass where baseline failed. Most parsimoniously
  run-to-run variation, not a package-fidelity effect — symmetric to the `f1006-hard` noise
  on the loss side.

**Smoke-set blind spot (the load-bearing finding).** The smoke set was the targeted Fivetran
cluster + an asana sentinel: `intercom001, intercom003, asana002, asana004, asana005,
quickbooks001, asana001`. **None of the 3 regressed tasks (`f1001`, `f1006-hard`,
`quickbooks003`) were in it.** Two of them are f1 tasks — exactly the population the smoke
set excluded by design. So the smoke gate was structurally incapable of catching the
dominant failure mode (convention bleed onto non-package projects), and the GO→full
recommendation was sound on the evidence it had but blind to the collateral. A
targets-only smoke set systematically under-samples the regressions a *generative*
instruction can cause everywhere it fires.

## Verdict

**REJECTED — do NOT promote. `@baseline` stays `622bdedac572b479` (31/48 = 0.6458).**

Package-fidelity as a single Exploration instruction is **NET-NEGATIVE at full scale**:
30/48 (0.625) vs @baseline 31/48 (0.6458), delta **−0.0208**, paired bootstrap 95% CI
**[−0.1042, +0.0625]** (straddles 0), McNemar exact p **1.0000**. The change does not clear
the promotion tripwire (CI does not exclude a regression; absolute score below baseline) on
a clean strict audit ({clean:48, tainted:0}).

The hypothesis is **falsified as written**. The mechanism is real but **double-edged**: the
exact instruction that lets the solver copy a package's column contract when a clean analog
exists (`asana002`, the one causal win) also drives it to copy package conventions where
they don't belong — manufacturing regressions via **convention bleed**:
- `f1001`: applied Fivetran `src_<dataset>__<entity>` naming to a non-Fivetran f1 project,
  breaking the hidden structural tests that expect plain `src_<entity>` names (6/6 → 2/6).
- `quickbooks003`: shaped intermediate/final models to the package's narrower *staging*
  column set, dropping columns the solution requires ("has less columns than solution__…",
  14/14 → 11/14).
- `f1006-hard`: 2-row value drift, weakly attributable / likely noise — but on the loss side.

The narrow gain (one task with a clean package analog the solver was authoring) does **not**
outweigh the collateral. A generative Exploration instruction fires on *every* task, so its
blast radius includes the non-package majority where "reproduce the package" is actively
harmful — and the targets-only smoke set could not see this (none of the 3 regressions were
in it; two are f1 tasks the smoke set excluded by design). The higher-leverage,
non-conflated direction surfaced here is **h0010** (grain-spine construction rule — build
one-row-per-entity models FROM the entity table, LEFT JOIN children), which targets the
shared root cause of the still-failing Fivetran cluster without the package-convention bleed.

**Findings for the captain to decide (NOT auto-filed):**

1. **Candidate REFINEMENT of this lever.** The asana002-type win and the f1001/quickbooks003
   regressions come from the *same* instruction firing too broadly. A scoped version —
   "reproduce the package's conventions ONLY when a real package analog exists in
   `dbt_packages/` for the specific model you are authoring; otherwise leave naming/grain/
   columns as the project already defines them" — could in principle keep the local
   type-contract win while suppressing the convention bleed onto non-package projects (f1) and
   onto models with no package analog. Unverified; would need its own hypothesis + a
   broad-regression smoke set. Note the prior on README-prose levers is weak (see the
   instruction-lever taxonomy: most do not change committed SQL), so a scoped re-try should be
   weighed against the captain's standing "stop reflexive prose hypotheses" guidance.
2. **WORKFLOW lesson — smoke design for GENERATIVE instructions.** This smoke set (6 targets +
   1 sentinel, all Fivetran) was *structurally* incapable of catching the dominant failure
   mode, because a generative Exploration/Implementation instruction fires on every task and
   can regress tasks far from the targeted cluster. The f1/quickbooks regressions were invisible
   to it by construction. Lesson: for any lever that changes how the solver *builds* models
   (not just a detect-and-fix check on a known target), the smoke set must include a **broad
   regression sample across task families**, not just the targeted failures plus one
   stable-pass sentinel. The single-sentinel design is adequate only for narrowly-scoped
   checks whose blast radius is provably the target set.

## Stage Report: propose

- DONE: The forked solver README's ONLY change vs codex-ade-dbt-minimal/README.md is the single Exploration-stage package-fidelity instruction; leak-guard / no-external-reference prose intact; NO reference to hidden AUTO_*/verifier tests.
  `diff` shows a single 7-line addition at line 49 inside `## Stage: Exploration`; the no-external-reference paragraph (curl/wget/git clone/package-source) and dbt_packages preservation prose are untouched; the new text says "do not hand-roll a simpler aggregation" and "read that package's existing models" — local-only, no test/verifier mention.
- DONE: FULL spec specs/h0009-exploration-package-fidelity.yaml diffs specs/baseline.yaml in ONLY experiment: + solver_workflow:; the smoke spec adds ONLY benchmark.tasks: [intercom001, intercom003, asana002, asana004, asana005, quickbooks001, asana001]; agent.kind=spacedock_solver and runtime=codex preserved.
  See Gate evidence FULL spec diff (two lines). Smoke diff vs full adds only the 7-task `tasks:` block. Frozen smoke spec lines 4-5 confirm `kind: spacedock_solver` / `runtime: codex`.
- DONE: Both specs frozen with rk freeze --allow-missing (full + smoke); paste the two-field FULL spec diff and the README diff into a ### Gate evidence block.
  Wrote specs/h0009-exploration-package-fidelity.frozen.yaml and specs/h0009-exploration-package-fidelity.smoke.frozen.yaml; evidence below.

### Gate evidence

FULL spec diff (`diff specs/baseline.yaml specs/h0009-exploration-package-fidelity.yaml` — exactly two fields):

```
2c2
< experiment: ade-bench-baseline # variants: ade-bench-h0001-<slug>
---
> experiment: ade-bench-h0009-exploration-package-fidelity # variants: ade-bench-h0001-<slug>
11c11
<   solver_workflow: ./solver_workflows/codex-ade-dbt-minimal # variants repoint to ./solver_workflows/h<NNNN>-<slug>
---
>   solver_workflow: ./solver_workflows/h0009-exploration-package-fidelity # variants repoint to ./solver_workflows/h<NNNN>-<slug>
```

README diff (`diff solver_workflows/codex-ade-dbt-minimal/README.md solver_workflows/h0009-exploration-package-fidelity/README.md` — single Exploration-stage addition):

```
49a50,56
> When the project embeds a known dbt package (e.g. a Fivetran `*_source`/staging
> package in `dbt_packages/`), read that package's existing staging/intermediate
> models and reproduce their conventions exactly for the models you build or
> change: the active-record / `_fivetran_active` filtering, the dedup keys, the
> output column set, and the grain (one-row-per-which-entity); do not hand-roll a
> simpler aggregation that diverges from the package's join anchor and filters.
> 
```

Smoke spec diff vs FULL (`diff specs/h0009-exploration-package-fidelity.yaml specs/h0009-exploration-package-fidelity.smoke.yaml` — adds only benchmark.tasks):

```
23a24,31
>   tasks: # Fivetran package-fidelity cluster + asana001 stable-pass regression sentinel; ade-bench- prefixed (bare slugs rejected by rk run)
>     - ade-bench-intercom001
>     - ade-bench-intercom003
>     - ade-bench-asana002
>     - ade-bench-asana004
>     - ade-bench-asana005
>     - ade-bench-quickbooks001
>     - ade-bench-asana001
```

Frozen artifacts: `specs/h0009-exploration-package-fidelity.frozen.yaml` (full), `specs/h0009-exploration-package-fidelity.smoke.frozen.yaml` (smoke). Both preserve `agent.kind: spacedock_solver`, `runtime: codex`. `provenance.yaml` was regenerated by `rk freeze` (shared file; harness_git_sha bumped vs baseline.frozen — a freeze-time artifact, not a spec change).

### Summary

Forked the current @baseline solver (codex-ade-dbt-minimal, 622bdedac572b479) into solver_workflows/h0009-exploration-package-fidelity and added exactly one Exploration-stage instruction: when a known dbt package is present in dbt_packages/, read its staging/intermediate models and reproduce their conventions (active-record/_fivetran_active filtering, dedup keys, output column set, grain) rather than hand-rolling a divergent aggregation. Leak-guard prose (no public fetch/clone) is intact and the change references only the local package source — no hidden-test/verifier mention. FULL spec differs from baseline in only experiment: + solver_workflow:; the smoke spec adds only the 7-task Fivetran cluster + asana001 sentinel; both specs frozen.

## Stage Report: smoke

- DONE: Smoke run launched DETACHED (nohup + /tmp/rk-h0009-smoke.log + .pid), polled across turns; all 7 cells completed with 0 errored and `captured > 0` on the cells.
  PID 849145 → log /tmp/rk-h0009-smoke.log; run dir runs/ade-bench-h0009-exploration-package-fidelity/13ecf093adb674c2; 7/7 completed, 0 errored; captured=1 on all 7 cells (subagent-trace-manifest.json).
- DONE: `rk audit <run-dir> --policy strict` is CLEAN and the `rk score` is paired to that same run-dir; both recorded in `## Smoke result`.
  Strict audit CLEAN {clean: 7, tainted: 0, coverage_missing: 0}; score stratified_pass_at_1 = 0.2857 (2/7) on the same run-dir 13ecf093adb674c2.
- DONE: Per-task smoke verdicts vs `@baseline`: name which of the 6 Fivetran targets flipped FAIL→PASS, confirm the `asana001` sentinel did not regress (go/no-go signal), and note whether the transcript shows the solver actually used dbt_packages/ conventions.
  asana002 flipped FAIL→PASS (only Fivetran flip); asana001 sentinel held PASS (no regression); asana002 transcript shows the ensign matched the installed `asana_source` package column contract (remaining_mismatches=0) — the Exploration change was exercised and load-bearing. intercom001 still FAIL: engaged active-record grain (5) but hidden equality test found 7 mismatches → residual value-level divergence.

### Summary

Smoke ran cleanly on all 7 targets (strict audit clean, 0 errored). One Fivetran target (asana002) flipped FAIL→PASS and the sentinel (asana001) held, giving a GO signal. The flip is causally tied to the Exploration change: the asana002 worker read the installed Fivetran `asana_source` package and reproduced its column contract rather than hand-rolling. Still-failing cells (intercom001, quickbooks001) show the instruction was reached but residual grain/value divergence remains — worth a full run to measure net effect vs @baseline. Gate recommendation: GO → full.

## Stage Report: analyze

- DONE: Paste the paired `rk runs diff @baseline <h0009-full-run>` delta (CIs, adjusted p) + absolute stratified_pass_at_1 (0.625, 30/48) vs @baseline (0.6458, 31/48) into ## Run result; state plainly it is NET -1 / below baseline / does NOT clear the promotion tripwire. Audit verified CLEAN.
  `rk runs diff` CLI crashes on ade-bench (query_id:null → TypeError in pairing.py:22); computed paired delta directly from per_trial_outcomes.json (slug-paired, 10k bootstrap seed 0): delta -0.0208, 95% CI [-0.1042, +0.0625] (straddles 0), McNemar p=1.0; 30/48 vs 31/48 = NET -1, below baseline, does NOT clear tripwire. Strict audit CLEAN {clean:48, tainted:0} (team-lead).
- DONE: Behavioral deep-dive — the 3 REGRESSIONS. For each PASS->FAIL read h0009 vs @baseline verifier/test-stdout + explain WHY package-fidelity broke a passing task. Confirm the 2 gains; note the smoke-set blind spot.
  f1001: convention bleed — renamed sources to Fivetran `src_<dataset>__<entity>` on a non-Fivetran f1 project, broke hidden structural tests (6/6→2/6). quickbooks003: trimmed cols to package staging contract ("has less columns than solution__", 14/14→11/14). f1006-hard: 2-row value drift, likely noise. Gains: asana002 (causal type-contract match, 3/3) + f1011 (incidental, no package present). All 3 regressions absent from the 7-task smoke set (2 are f1 tasks the smoke set excluded) → smoke structurally blind.
- DONE: Write verdict-bearing learnings into the entity (## Behavioral analysis / ## Verdict): package-fidelity is NET-NEGATIVE at full scale; recommend conclude REJECTED, do NOT promote (@baseline stays 622bdedac572b479).
  Wrote Full-run deep-dive subsection + Verdict (REJECTED, NET-NEGATIVE, convention-bleed mechanism, h0010 as the non-conflated successor). @baseline stays 622bdedac572b479.

### Summary

h0009 full run (1026ae344528e6eb, clean strict audit) scores 0.625 (30/48) vs @baseline 0.6458 (31/48): NET -1, paired delta -0.0208, CI [-0.1042, +0.0625] straddling zero, McNemar p=1.0 — does NOT clear the promotion tripwire. The decisive finding is the 3 regressions, all on tasks the targeted smoke set could not see: the generative package-fidelity instruction caused convention bleed (f1001 Fivetran-style source renaming on a non-Fivetran project; quickbooks003 column-trimming to the package staging contract) while delivering only one causal gain (asana002). Verdict: REJECTED, do NOT promote; @baseline stays 622bdedac572b479. h0010 (grain-spine construction rule) is the non-conflated successor.

## Stage Report: conclude

- DONE: Confirm NO promotion was performed (no rk baseline promote / rk registry add); @baseline stays 622bdedac572b479.
  `rk registry resolve run @baseline` → `runs/ade-bench-baseline/622bdedac572b479` (unchanged); only read-only `rk score`/`rk audit`/`resolve` were ever run on h0009.
- DONE: Record (for the captain, not auto-filed) the two findings worth acting on — (a) candidate REFINEMENT: scope package-fidelity to fire only when a real package analog exists for the model being authored; (b) WORKFLOW lesson: generative-instruction smoke sets must include a broad regression sample, not just targets + 1 sentinel.
  Both written into ## Verdict under "Findings for the captain to decide (NOT auto-filed)" (the portable record). No follow-up hypothesis file created.
- DONE: Append ## Stage Report: conclude; leave frontmatter (status/verdict/completed) for the first officer; commit before sending Done.
  This report; frontmatter untouched; commit below.

### Summary

h0009 concluded REJECTED — package-fidelity as a single generative Exploration instruction is NET-NEGATIVE at full scale (30/48 vs @baseline 31/48; delta -0.0208, CI [-0.1042,+0.0625], McNemar p=1.0). No promotion performed; @baseline stays 622bdedac572b479. The one causal gain (asana002 type-contract match) is outweighed by convention-bleed regressions on non-package tasks (f1001, quickbooks003) that the targets-only smoke set was structurally blind to. Two captain-decision findings recorded in ## Verdict: a scoped-lever refinement candidate and a smoke-design lesson for generative instructions. Frontmatter left for the first officer.
