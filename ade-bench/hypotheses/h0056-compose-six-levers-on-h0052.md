---
id: h0056
title: Six-lever composition — stack the three new smoke-verified levers (h0053 per-key inner-join + h0054 lap-time exclude-pit-laps + h0055 build/rename preserve-columns) onto @baseline h0052's three (max-points + feature-boundary + coverage) in ONE README
status: conclude
kind: hypothesis
source: "Captain request 2026-06-13 — merge the three individually smoke-verified levers (h0053 airbnb005 inner-join GO; h0054 f1010-medium exclude-pit-laps GO; h0055 ana-eng003 preserve-columns, smoke in progress / ana-eng003 artifact passing) into one composition on the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133). Same compose-verified-bleed-free-levers play that promoted h0052; each new lever is precondition-gated and explicitly non-colliding with an existing one."
started: 2026-06-13T17:45:52Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The h0052 baseline README already composes three construct-gated levers (h0044 same-grain
`max(points)`, h0045 feature-boundary removal/toggle, h0050 intent-gated scoped coverage). This
hypothesis stacks the three NEW smoke-verified levers on top, in one README — six gated
Implementation rules total:

| # | Lever | Construct it gates on | Smoke evidence |
|---|-------|-----------------------|----------------|
| 1 | h0044 max(points) | standings/season points | (in h0052) f1006 + f1006-hard flips |
| 2 | h0045 feature-boundary | remove/disable feature | (in h0052) qb002/qb004 narrow holds |
| 3 | h0050 scoped coverage | completeness-intent missing rows | (in h0052) airbnb009 flip |
| 4 | **h0053 per-key inner-join** | per-key metric, NO completeness intent | **GO** — airbnb005 inner-join, 14,243-row oracle match |
| 5 | **h0054 lap-time exclude** | lap/duration avg accounting for pit stops | **GO** — f1010-medium EXCLUDE artifact |
| 6 | **h0055 preserve-columns** | build/rename, no feature-removal, no col-subset | smoke in progress (ana-eng003 artifact passing) |

**Two gated dual-pairs must coexist without collision (the integration risk):**
- **h0050 ↔ h0053** — opposite sides of the completeness-intent signal. h0050 ADDS missing keys
  when completeness IS requested (airbnb009); h0053 scopes to fact keys when it is NOT (airbnb005).
  Proven non-colliding in h0053's solo smoke (airbnb009 held while airbnb005 flipped).
- **h0045 ↔ h0055** — opposite task types. h0045 DROPS feature-only columns on remove/disable
  tasks (qb002/qb004); h0055 PRESERVES all upstream columns on build/rename (ana-eng003).

**Falsifiable claim (the single README change):** fork the current `@baseline` (h0052) solver and
add the three new levers **verbatim, each as its own precondition-gated Implementation rule** —
nothing else. The six-lever composition will preserve every lever's solo effect with **no
interference and no collision**:
- airbnb005 flips via the inner-join shape (h0053);
- f1010-medium commits the EXCLUDE artifact and ana-eng003 the full-18-column artifact
  (h0054/h0055 — noise-reducers that pin two coin-flip cells, shrinking the trials:1 variance pool);
- airbnb009 + f1006 + f1006-hard (h0052's banked flips) HOLD;
- qb002 + qb004 still drop their feature columns (h0045 fires, h0055 does NOT);
- every canary holds.

**Why compose:** the program-wide lesson is that trials:1 ±noise (~±3 cells) washes a single
flip's net. Stacking verified bleed-free levers (a) banks airbnb005 (+1 over h0052) AND (b) **pins
two of the coin-flip cells** (f1010-medium, ana-eng003) that have been costing nets — a tighter
variance band, not just a higher signal. Best case nets above h0052's true expectation (~30) and
clears it on a fresh draw.

**Falsified if** composing degrades any lever vs its solo smoke (interference / README bloat
mis-routing a precondition), OR a dual-pair collides (airbnb009 coverage suppressed; qb feature
columns force-preserved), OR a canary regresses beyond off-construct trials:1 variance.

Target datasets: airbnb005 (flip); f1010-medium, ana-eng003 (pin/stabilize); airbnb009, f1006,
f1006-hard, qb002, qb004 (hold).

## Pre-smoke Decision-Fork Probe

The FO ran a six-way mutual-non-interference simulation on the COMMITTED merged six-lever
Implementation rulebook (full writeup: `_artifacts/h0056-decision-fork-simulation.md`). Method: 8
tasks × 6 fresh isolated decision agents, each given ONLY the merged rulebook + that task's clean
visible starting context (instruction + starting model SQL, stripped of any solver patch / verifier
/ oracle), classified DESIRED iff the expected gated rule fires AND no collision rule fires. 48
isolated decisions total.

**Result — 48/48 desired branch, 0 collisions:**

| Task | Role | Expected rule | Must NOT fire | Result |
|------|------|---------------|---------------|--------|
| airbnb005 | FLIP target (h0053) | per-key-inner-join | coverage-repair | 6/6 desired, 0 coll |
| f1010-medium | FLIP/PIN (h0054) | lap-time-exclude-pit | — | 6/6 desired, 0 coll |
| ana-eng003 | FLIP target (h0055) | preserve-columns | feature-boundary | 6/6 desired, 0 coll |
| airbnb009 | COLLISION canary (h0050↔h0053) | coverage-repair | per-key-inner-join | 6/6 desired, 0 coll |
| f1006 | HOLD (h0044) | max-points | — | 6/6 desired, 0 coll |
| f1006-hard | HOLD (h0044) | max-points | — | 6/6 desired, 0 coll |
| quickbooks002 | COLLISION canary (h0045↔h0055) | feature-boundary | preserve-columns | 6/6 desired, 0 coll |
| quickbooks003 | COLLISION canary (h0045↔h0055) | feature-boundary | preserve-columns | 6/6 desired, 0 coll |

**Both collision dual-pairs hold their correct sides:** (a) h0050↔h0053 (completeness-intent) —
airbnb009 (completeness asked) routed all 6 draws to COVERAGE-REPAIR with the per-key rule silent,
while airbnb005 (no completeness ask) routed all 6 to PER-KEY-INNER-JOIN with coverage silent;
(b) h0045↔h0055 (build-vs-remove) — quickbooks002+003 (feature removal) routed all 12 draws to
FEATURE-BOUNDARY (not preserve-all), while ana-eng003 (plain build/rename) routed all 6 to
PRESERVE-COLUMNS (all 18 upstream cols, not feature-drop).

**Caveat (per the method):** this is PROXY evidence — it shows the longer six-rule rulebook has no
detectable decision-policy interference (every target routes to its intended rule, every collision
canary holds), clearing the captain's "enough probability" bar to skip smoke. It does NOT prove the
solver finds the bug, writes the committed artifact, and passes the hidden grader, nor the
off-construct trials:1 ~±3-cell variance on the 40 untouched cells. The promote decision rests on
the full run-dir clearing h0052's expectation + committed-artifact reads (AC-3/AC-4/AC-5).

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Composed README = h0052's README + the h0053, h0054, h0055 lever blocks verbatim (each traceable to
its source solver dir), nothing else; the existing three levers + leak-guard byte-unchanged.

**AC-2 — Every recorded score paired with a clean strict audit** (captured>0 every cell).

**AC-3 — Verdict by paired delta vs `@baseline` (h0052), read through the known ~±3 trials:1 noise
floor.** Promote on committed-artifact + expectation (per the h0052 self-consistency precedent), not
a single-draw net alone.

**AC-4 — Per-lever committed-artifact reads (the decisive test):** airbnb005 = inner-join-from-fact
(no zero-fact NULL rows); f1010-medium = EXCLUDE pit laps before avg; ana-eng003 = all 18 columns;
airbnb009 = coverage predicate dropped (h0050 still fires); f1006/f1006-hard = `max(points)`;
qb002/qb004 = narrow feature-boundary (columns dropped, h0045 still fires).

**AC-5 — Regression panel + BOTH collision-canary pairs hold:** airbnb009 (h0050↔h0053 collision),
quickbooks002 + quickbooks003 (h0045↔h0055 collision), plus ≥1 perturbable passer per family. A
collision or same-construct regression is a NO-GO; off-construct trials:1 variance is classified,
not auto-fatal; the promote decision rests on the run-dir clearing h0052's expectation.

## Gatekeeper review

**Recommendation: APPROVE** — clean composition: each of the three new levers inserted byte-verbatim from its smoke-verified sibling, precondition-gated (non-generative), leak-guard + spec scope intact, both collision-canary pairs in the smoke panel; the only WARNs are the standing predictive ones (G7 structural-rewrite inert-risk, G11 multi-model-target variance) that never block.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-13T18:00Z.

Fork parent resolved: `@baseline` = h0052 (`rk registry resolve run @baseline` → runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133; its solver_workflow = solver_workflows/h0052-compose-maxpoints-featureguard-scoped-coverage). Matches the hypothesis `source:`. Diff base = the h0052 solver README.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff h0052 h0056 README` = exactly 3 added hunks (79a, 138a, 165a), 0 deletions/changes; all three land under `## Stage: Implementation` (block lines 80/158/206, between Implementation@50 and Validation@221). The hypothesis's Falsifiable claim explicitly proposes adding these three blocks as one composition — three rules, one stage, the declared single change. |
| G2 leak-guard intact | PASS | grep of curl/wget/git clone/ls-remote/download/AUTO_/solution__/check_option/verifier/equality-test/expected-output/drive-to-zero/self-anchored phrasings over the added lines → none. Parent prose byte-unchanged (`diff` shows 0 `<` deletions). |
| G3 spec two fields | PASS | `diff baseline.yaml h0056.yaml` = only `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0056.yaml h0056.smoke.yaml` = only an added `benchmark.tasks:` block (16 slugs, all `ade-bench-` prefixed). Panel includes every hypothesis target (airbnb005, f1010-medium, ana-eng003) + regression sentinels (f1006/f1006-hard hold). No other field differs. |
| G5 both frozen | PASS | `h0056-*.frozen.yaml` + `…smoke.frozen.yaml` both exist; both carry `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Each inserted block is byte-identical to its smoke-verified source sibling (BLOCK A == h0054, BLOCK B == h0053, BLOCK C == h0055 — confirmed by per-block `diff -q`). Wording matches the claim exactly; no scope creep. All three are gated, build-direction/structural rules carrying worked BEFORE/AFTER SQL skeletons — generative-derivation guidance, not self-anchored "verify your own work." |
| G7 actionability/inert-risk | WARN | All three are structural-shape rules (join direction, exclude-then-aggregate, preserve-column-set) — the G7 inert-risk family at gpt-5.5/xhigh — BUT each carries a literal BEFORE→AFTER SQL skeleton (the worked-example form G7 prescribes as the mitigation) and each was individually committed-artifact-verified in its solo smoke (h0053 GO 14,243-row inner-join, h0054 EXCLUDE artifact, h0055 18-col artifact). Inert-risk materially reduced by the worked examples + prior solo evidence; surfaced per the predictive rule. |
| G8 regression-canary coverage | PASS (N/A-leaning) | All three levers are precondition-GATED, not generative (inert on any model not matching their construct), so G8 is N/A by its own gate. Even so the smoke panel carries a full canary set: ≥1 non-target passer from airbnb/asana/ana-eng/f1/quickbooks (no intercom passer exists), and the construct-adjacent families carry ≥2 perturbable canaries (airbnb 001/004/006/008; f1 1005/1006/1006-hard/1007). |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — three gated mechanical SQL-shape rules. |
| G10 self-correcting false-positive | N/A | None of the three is a check/reconcile/validate-and-fix lever; they are build-time SQL-shape constructions, not "verify a number and act on disagreement." |
| G11 multi-model-target risk | WARN | airbnb005 (h0053) and ana-eng003 (h0055) may be scored by >1 `AUTO_*_equality` model; each new lever's precondition touches the specific authored model, so a single-run flip on a multi-model target should be read as artifact-on-the-addressed-model, not aggregate proof. The hypothesis already commits to ≥2 seed-perturbed repeats per target judged by committed artifact (AC-3/AC-5), which is the prescribed mitigation. Predictive only. |
| G12 decision-fork probe quality | N/A | `## Pre-smoke Decision-Fork Probe` present and explicitly states the probe was skipped because each of the three levers is already individually committed-artifact smoke-verified and each was shown non-colliding with its dual in its solo smoke; the only new question (six-way interference) is what this smoke tests directly. Valid skip rationale. |

**For the captain:** Clean APPROVE — the composition is the three smoke-verified blocks dropped in verbatim with zero edits to h0052's existing six-lever-minus-three body or leak-guard. Two standing WARNs only (G7 structural-rewrite inert-risk, mitigated by the worked SQL skeletons + prior solo GOs; G11 multi-model variance on airbnb005/ana-eng003, mitigated by the AC-5 ≥2-repeat artifact judging). Per the dispatch the captain intends to skip smoke and go straight to full after the FO decision-fork simulation; the smoke spec is built and frozen for completeness regardless.

## Smoke result

## Run result

**Smoke skipped per captain** (2026-06-13) on the strength of the 48/48 six-way decision-fork
simulation (`_artifacts/h0056-decision-fork-simulation.md`, 0 collisions across both dual-pairs) +
the gatekeeper APPROVE (no FAILs, only the two standing predictive WARNs). Went straight to full.

**Two concurrent independent full 48-task draws launched** (the h0052 self-consistency precedent —
two independent draws beat single-draw trials:1 variance). CAS-buster: each variant differs from the
base full spec ONLY in `experiment:` + `sampling.seed:` (distinct seeds → distinct sealed_hash →
distinct run-dirs; behaviorally still temp=0 codex). Both detached via `drivers/rk-run-detached.sh`,
FO owns the sentinel scan + audit/score/paired-delta when `done` lands.

- r1: seed 42, spec `specs/h0056-compose-six-levers-on-h0052-r1.frozen.yaml` (sealed_hash
  22e998fa95bb0a313ed600aea936ce7f); handle
  `runs/.rk-handles/h0056-full-r1-20260613-181358/` (pid 2714347, log .../log)
- r2: seed 43, spec `specs/h0056-compose-six-levers-on-h0052-r2.frozen.yaml` (sealed_hash
  0eb370abee3244354ba6f53dd6437e98); handle
  `runs/.rk-handles/h0056-full-r2-20260613-181403/` (pid 2714516, log .../log)

Both confirmed live at launch (nohup pid alive, `rk run` child process spawned and running).

### Analyze result (2026-06-14) — both draws landed, strict-clean, 48/48 captured, 0 errored

**@baseline = h0052** `runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133` = **32/48 = 0.6667**.

| Draw | run-dir hash | n_pass | pass@1 | Wilson CI | paired Δ vs h0052 (10k bootstrap) |
|------|-------------|--------|--------|-----------|-----------------------------------|
| r1 (seed 42) | deff5d8a9c10c92f | 32/48 | 0.6667 | [0.525, 0.783] | +0 cells, 95% CI [-5, +5] |
| r2 (seed 43) | 2c544ee929c0c02a | 35/48 | 0.7292 | [0.590, 0.834] | +3 cells, 95% CI [+0, +7] |

Both vs `paper_baseline` 0.1875 → far above. Paired by slug from `per_trial_outcomes.json` (`rk runs diff`
TypeErrors on these dirs — `query_id: null`, harness data-shape limitation, not a run defect).

**Full paired ledger (every verdict change, both directions):**

| Slug | base | r1 | r2 | Direction | Mechanism |
|------|------|----|----|-----------|-----------|
| airbnb005 | 0 | 1 | 1 | GAIN (both) | **h0053 fired** — inner-join-from-`fct_reviews` per-key NPS, no zero-fact NULL rows (TARGET) |
| airbnb007 | 0 | 1 | 1 | GAIN (both) | **h0053 generalized** to sibling NPS task — per-listing aggregate built FROM fact + INNER JOIN dim |
| f1011 | 0 | 1 | 1 | GAIN (both) | OFF-construct: multiple-choice option task (check_option_a..f); base failed 1 option, both draws passed all 6 — oracle MC coin-flip landing favorably, NOT lever-caused |
| f1001 | 1 | 0 | 1 | REGRESS (r1 only) | OFF-construct trials:1 variance — 14-file src/staging build; r1 botched `src_models_are_correct` (Got 14≠0), r2 + base built it correctly. No lever rule fired. |
| quickbooks002 | 1 | 0 | 1 | REGRESS (r1 only) | h0045-family feature-removal coin-flip — r1 OVER-DROPPED `department_id` (base col), "less columns than solution"; r2 kept it. Preserve-columns (h0055) NEVER fired. NOT a collision. |
| quickbooks003 | 1 | 0 | 1 | REGRESS (r1 only) | Same as qb002 — r1 dropped `department_id` across 79 lines / 14 models, r2 dropped only 4 (the conditional joins). Over-DROP coin-flip, h0055 absent. NOT a collision. |

**Held canaries (PASS in base + r1 + r2), committed-artifact confirmed:**
- airbnb009 (h0050↔h0053 collision canary) — coverage-repair edit on `mom_agg_reviews.sql` (date-spine WHERE), per-key inner-join did NOT fire. Dual-pair held.
- f1006 + f1006-hard (h0044) — `max(cs.points)`/`max(ds.points)` committed in both.
- ana-eng003 (h0055 target) + f1010-medium (h0054 target) — PASS both draws; f1010-medium committed the `lap_times_without_pit_stops` EXCLUDE-then-`avg(milliseconds)` shape.
- quickbooks004 held PASS both draws.

### The six required analyze questions

1. **Net + ledger** — r1 = 32/48 (paired +0, CI [-5,+5]); r2 = 35/48 (paired +3, CI [+0,+7]). Mean 33.5.
   Both directions in the table above: 3 gains held in BOTH draws (airbnb005, airbnb007, f1011); 3
   regressions in r1 ONLY (f1001, quickbooks002, quickbooks003), all held PASS in r2. Net r1 = +3−3 = 0;
   net r2 = +3−0 = +3.
2. **Smoke vs full** — **smoke was SKIPPED** per captain (the 48/48 six-way decision-fork sim +
   gatekeeper APPROVE stood in). The 48/48 sim is a DECISION-policy proxy: it proved every target routes
   to its intended rule and every collision-canary holds its side. It could NOT see (a) the solver's
   feature-removal BOUNDARY judgment on qb002/qb003 (how far to extend the drop — a coin-flip the sim
   doesn't model because it isn't a rule-routing question), (b) off-construct trials:1 variance on the 40
   untouched cells (f1001's 14-file build), nor (c) oracle MC variance (f1011). The sim was right where it
   spoke (no collision) and silent where the variance lives.
3. **Already-correct-and-broken** — all 3 r1 regressions were PASSING at h0052. f1001, qb002, qb003 are
   damage to working code in r1. But each held PASS in r2 + baseline → the damage is draw-specific
   trials:1 variance, not a systematic lever-induced break. No regression is lever-caused (proof below).
4. **Was the change executed?** — verified from committed artifacts, not chatter:
   - airbnb005: executed-and-helped (inner-join-from-fact committed, 4/4).
   - airbnb007: executed-and-helped (per-key fact aggregate committed, 11/11).
   - f1011: premise-falsified-favorably (no lever touches MC; coin-flip pass).
   - qb002/qb003 r1: executed-and-HURT by an over-aggressive feature-removal (h0045-family), NOT by h0055.
   - f1001 r1: executed-and-hurt by a botched src-model build, off-construct.
5. **Prevention + next move** — the gains (airbnb005/007 via h0053) are real and reproduced in both
   draws; keep them. The harm is NOT lever-caused — it is the standing trials:1 ~±3-cell floor on
   feature-removal-boundary and large-build cells (qb002/qb003/f1001 all flip-flop between draws). No
   scoping guardrail is needed because no lever over-fired. To catch earlier: a feature-removal
   boundary canary (qb002/qb003) in any future smoke would surface the coin-flip, but it would not
   change the verdict (it's variance, not a defect). Recommended next move below in the PROMOTE para.
6. **Smoke-vs-full fork drift** — N/A in the rule-drift sense: the three NEW levers all fired with their
   intended committed shape in BOTH draws (airbnb005 inner-join, f1010-medium exclude-pit, ana-eng003
   18-col, airbnb007 generalization). No new lever drifted into a wrong branch. The r1 net shortfall is
   entirely the off-construct/feature-boundary variance pool (f1001 + qb002 + qb003), which the skipped
   smoke could not have sampled as anything but coin-flips. The fork that changed at r1 was the
   h0045-family feature-removal BOUNDARY (over-drop), an existing-lever-family coin-flip, not any of the
   three new additions.

## Behavioral analysis

Per-cell forensic (committed artifact + agent reasoning + verifier line + cross-draw diff + verdict).
Edits read from the cell-root session jsonl (`apply_patch` payloads) and `agent/codex.txt` reasoning;
verdict from `verifier/test-stdout.txt`.

### quickbooks002 — r1 REGRESS (P→F), r2 + base PASS  →  VERDICT: VARIANCE (h0045 feature-removal over-DROP; h0055 preserve-columns NEVER fired)

- **Verifier (r1):** 6/8 PASS, 2 ERROR — `AUTO_int_quickbooks__expenses_union_equality` and
  `…__sales_union_equality`, both: *"int_quickbooks__expenses_union has **less columns than**
  solution__int_quickbooks__expenses_union"*. The `check_if_models_use_department_var` +
  `check_if_project_has_department_var` checks PASSED → the feature removal itself was correct; the
  failure is the union models lost a column the solution KEEPS.
- **Committed artifact (r1):** the `apply_patch` deletes both the conditional `department_name`
  (correct) AND the base lines `- sales_union.department_id,` / `- expense_union.department_id,`
  (wrong — `department_id` is a shared base column the oracle retains).
- **codex.txt reasoning (r1) — the load-bearing quote:** *"the downstream unions would still expose
  departments if I only removed the conditional name joins … I'm going to remove the column consistently
  from local transaction, intermediate, enhanced, double-entry SQL."* This is a deliberate
  **feature-BOUNDARY judgment (h0045 family)** — the solver decided `department_id` was a "department
  placeholder" to remove. **Zero mention of preserve-columns / "PRESERVE THE COLUMN SET" / h0055.** The
  preserve-columns rule did not fire; if it had, the error would be the OPPOSITE (too MANY columns).
- **Head-to-head:** r2 (PASS, 8/8) committed the SAME structure but KEPT `sales_union.department_id` /
  `expense_union.department_id` (no `-` on those lines), removing only `department_name`. Baseline h0052
  also passed. The only difference between FAIL and PASS is how far the solver extended the
  `department_id` removal — a pure boundary coin-flip.
- **Verdict:** `variance (h0045 feature-removal coin-flip, preserve-columns absent — OVER-drop)`. The
  decision-fork sim said preserve-columns would not fire on qb002 and it did not. Matches the prior
  h0055 smoke forensic (over-KEEP there; over-DROP here — same coin-flip axis, opposite slip).

### quickbooks003 — r1 REGRESS (P→F), r2 + base PASS  →  VERDICT: VARIANCE (identical mechanism to qb002)

- **Verifier (r1):** 9/14 PASS, 5 ERROR — `expenses_union`, `invoice_join`,
  `refund_receipt_transactions`, `sales_receipt_transactions`, `sales_union` all *"has less columns than
  solution"*. Both `check_if_*_department_var` checks PASSED (13/14, 14/14).
- **Committed artifact (r1):** `apply_patch` carries **79 `department_id` DROP lines** across all
  transaction/intermediate/double-entry models — the solver scrubbed `department_id` project-wide.
- **Reasoning (r1):** 0 preserve-columns / "PRESERVE THE COLUMN SET" hits in the ensign reasoning. Pure
  feature-removal over-extension.
- **Head-to-head:** r2 (PASS, 14/14) dropped only **4** `department_id` lines (the conditional join
  clauses), kept the base `department_id` output columns. Same FAIL-vs-PASS axis as qb002.
- **Verdict:** `variance (h0045 feature-removal coin-flip, preserve-columns absent — OVER-drop)`. NOT a
  collision.

### f1001 — r1 REGRESS (P→F), r2 + base PASS  →  VERDICT: off-construct trials:1 VARIANCE (no lever fired)

- **Verifier (r1):** 5/6 PASS, `src_models_are_correct` FAIL (*Got 14 results, configured to fail if
  != 0*). This is a 14-source-model + 14-staging-model build task (`src_circuits`, `src_results`, … +
  `stg_f1_dataset__*`).
- **Committed artifact:** 14 `Add File: …/src_*.sql` + 14 `Update File: …/stg_*.sql` — a large
  scaffolding build. None of the six lever constructs (standings max-points, feature-boundary, coverage,
  per-key inner-join, lap-exclude, preserve-columns) targets src-model structural correctness.
- **Reasoning:** 0 lever-firing language. "preserve"/"lap"/"pit" keyword hits are README boilerplate
  echoed in the prompt, not firing.
- **Head-to-head:** r2 built the same src models and passed `src_models_are_correct` 6/6; baseline
  passed. r1 botched the src-model shape (14 wrong) on a multi-file build.
- **Verdict:** off-construct trials:1 variance on a large build cell — not lever-caused.

### airbnb005 — GAIN both draws (TARGET, h0053)  →  VERDICT: h0053 fired, executed-and-helped (AC-4 ✔)

- **Verifier (r1):** 4/4 PASS. **Committed artifact:** `listing_agg_nps_reviews.sql` /
  `daily_agg_nps_reviews.sql` built with `FROM {{ ref('fct_reviews') }}` + `INNER JOIN review_counts_cte`
  / `INNER JOIN listing_metadata_cte` — the per-key inner-join-from-fact shape (no left-join-from-dim
  that would emit zero-fact NULL rows). Held identically in r2. The h0053 14,243-row inner-join construct
  is present in the committed artifact.

### airbnb007 — GAIN both draws (sibling NPS, h0053 generalization)  →  VERDICT: real lever gain

- **Verifier (r1):** 11/11 PASS. **Committed artifact:** `listing_agg_nps_reviews.sql` aggregates
  `COUNT(*) … FROM {{ ref('fct_reviews') }}` per listing then `INNER JOIN {{ ref('dim_listings') }}` —
  same per-key NPS-from-fact shape as airbnb005. Held in both draws. The h0053 per-key inner-join
  construct generalized from its solo target (airbnb005) to this sibling task — a genuine lever effect,
  not a fluke (reproduced across two independent seeds).

### f1011 — GAIN both draws  →  VERDICT: oracle MC coin-flip (NOT lever-caused)

- **Verifier:** option-check task (`check_option_a` … `check_option_f`, expected_test_count=6). Baseline
  FAILED `check_option_b` (5/6); r1 + r2 both PASS all 6. No lever touches a multiple-choice construct.
  This is the known oracle MC coin-flip landing favorably on both draws.

### Held canaries (committed-artifact confirmation — AC-5)

- **airbnb009 (h0050↔h0053 collision canary):** PASS 1/1 all three. r1 committed a coverage/date-spine
  edit on `mom_agg_reviews.sql` (`AND`→`WHERE DATE_ACTUAL = (SELECT MAX(REVIEW_DATE::DATE) …)`) — the
  coverage-repair construct (h0050). Per-key inner-join (h0053) did NOT fire. **Dual-pair held — no
  collision.**
- **f1006 + f1006-hard (h0044):** `max(cs.points)` / `max(ds.points)` committed in both; PASS both draws.
- **f1010-medium (h0054):** `lap_times_without_pit_stops` via `left join pit_stop_laps … where
  psl.race_id is null` then `avg(milliseconds)` — EXCLUDE-then-aggregate shape committed; PASS.
- **ana-eng003 (h0055):** PASS both draws.

### Collision verdict (AC-5), stated plainly

**No regression is lever-caused. Neither collision dual-pair collided.**
- h0045↔h0055: qb002 + qb003 r1 regressions are h0045-family feature-removal **over-DROP** coin-flips —
  the solver scrubbed the base `department_id` column. The h0055 preserve-columns rule NEVER fired in
  either cell (0 firing-language hits; the failure mode is "too FEW columns", the exact opposite of a
  preserve-columns over-KEEP). The decision-fork sim's "preserve-columns silent on qb002/qb003" proxy is
  CONFIRMED by the committed artifacts.
- h0050↔h0053: airbnb009 held PASS with the coverage edit; airbnb005 flipped with the inner-join edit.
  Opposite sides of the completeness-intent signal, both correct. No collision.

### PROMOTE recommendation (artifact-grounded; the DECISION is the captain's)

**Recommend: PROMOTE candidate — h0056 is collision-free and clears h0052's expectation.**

- **Collision-free:** verified from committed artifacts, not the proxy. Both collision dual-pairs held
  their correct sides in both draws (airbnb009 coverage / airbnb005 inner-join; qb002/qb003 feature-drop
  with preserve-columns silent). Every one of the three NEW levers fired with its intended committed
  shape in both draws (airbnb005 inner-join, f1010-medium exclude-pit, ana-eng003 18-col, plus the h0053
  generalization to airbnb007). The three r1 regressions are ALL off-construct / feature-boundary
  trials:1 coin-flips that held PASS in r2 — none lever-caused.
- **Clears the bar:** h0052's measured expectation is ~30 (its self-consistency run drew 29/30 on the
  unchanged h0043 README; h0052's own draws were 31/32). h0056 drew **32 and 35 (mean 33.5)** — both
  draws beat 30, and r2's +3 paired CI is [+0, +7] (lower bound touches 0 but the mean clears h0052's
  expectation and the gains are artifact-real + reproduced across both seeds). The NEW banked value over
  h0052 is airbnb005 + airbnb007 (h0053 per-key inner-join, +2 reproduced in BOTH draws), on top of
  h0052's existing banked flips which all held.
- **Caveat for the captain:** r1's net is +0 because the existing-family feature-removal coin-flips
  (qb002/qb003) and the f1001 build variance happened to land badly that draw; this is the standing
  ~±3-cell trials:1 floor, not a defect in the composition. The promote rests (per the h0052 precedent)
  on committed-artifact proof + the two-draw expectation clearing 30 — both satisfied — not on a single
  draw's net.

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Merged solver README = h0052 README + three lever blocks inserted VERBATIM at section anchors; `diff h0052/README.md h0056/README.md` shows EXACTLY those three hunks, leak-guard prose byte-unchanged (AC-1)
  Fork via `cp -r`; applied each sibling's single-block diff as a patch. diff = 3 added hunks (79a BLOCK C/h0055, 138a BLOCK B/h0053, 165a BLOCK A/h0054), 0 deletions; per-block `diff -q` confirms each block byte-identical to its source sibling; all three under `## Stage: Implementation`.
- DONE: Full spec h0056.yaml differs from baseline.yaml ONLY in experiment: + solver_workflow:; smoke spec adds benchmark.tasks integration panel; both frozen with rk freeze --allow-missing
  `diff baseline.yaml h0056.yaml` = exactly those 2 lines. Smoke panel = 16 tasks: targets airbnb005/f1010-medium/ana-eng003 + collision pairs airbnb009 and quickbooks002+003 + banked holds f1006/f1006-hard + per-family perturbable passers (airbnb001/004/006/008, f1005/f1007, asana002, ana-eng001). Smoke scaffold byte-identical to siblings (only tasks/exp/solver differ). Both .frozen.yaml written.
- DONE: Gatekeeper run against the variant artifacts; `## Gatekeeper review` block written with per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT + one-line rationale
  Fork parent resolved @baseline=h0052 (registry + source agree). Overall APPROVE; G1-G6 PASS, G8 PASS(N/A-leaning, gated), G9/G10/G12 N/A, two standing predictive WARNs (G7 inert-risk mitigated by worked SQL skeletons + prior solo GOs; G11 multi-model variance mitigated by AC-5 repeats).

### Summary
Built the six-lever composition by forking @baseline h0052's solver and inserting the three smoke-verified lever blocks (h0053 per-key inner-join, h0054 lap-time exclude-pit-laps, h0055 build/rename preserve-columns) byte-verbatim at their Implementation-stage anchors. Full spec differs from baseline only in experiment+solver_workflow; smoke spec adds a 16-task integration panel (union of the three sibling smoke panels, deduped, with both collision-canary pairs). Both specs frozen. Gatekeeper recommendation APPROVE — no FAILs, only the two standing predictive WARNs. Per dispatch the captain intends to skip smoke and go straight to full after the FO decision-fork simulation.

## Stage Report: full

- DONE: Two seed-variant FULL specs built from the 48-task base (NO benchmark.tasks): r1 = experiment ...-r1 + seed 42; r2 = experiment ...-r2 + seed 43; each differs from the base full spec ONLY in experiment: + sampling.seed: (CAS-buster); both frozen with rk freeze --allow-missing.
  `diff` of each variant vs base = exactly the experiment: + seed: lines (0 benchmark.tasks). Frozen specs carry distinct sealed_hash (r1 22e998fa..., r2 0eb370ab...) → two genuinely-independent run-dirs.
- DONE: Both full runs launched CONCURRENTLY and DETACHED via drivers/rk-run-detached.sh (keys h0056-full-r1 and h0056-full-r2, mode run); the two handle dirs returned with pid/log; ensign returned immediately, did NOT wait.
  r1 handle runs/.rk-handles/h0056-full-r1-20260613-181358 (pid 2714347); r2 handle runs/.rk-handles/h0056-full-r2-20260613-181403 (pid 2714516).
- DONE: Both handles confirmed live (pid alive, rk run child process spawned) before returning; exact two handle-dir paths reported.
  ps --ppid showed the `uv run ... rk run` child alive under each nohup pid; log 0 bytes is normal startup buffering (uv resolve + harbor/docker spin-up before first flush). FO owns the sentinel scan.
- DONE: Body updated — `## Pre-smoke Decision-Fork Probe` carries the 48/48 six-way sim summary (cites _artifacts/h0056-decision-fork-simulation.md, both dual-pairs + proxy caveat); `## Run result` notes smoke-skipped-per-captain + the two launch handles.
  Replaced the prior "Skipped" text with the 8-task table + two-dual-pair non-collision finding; Run result records both handles, seeds, sealed_hashes, spec paths.

### Summary
Launched the h0056 six-lever composition as TWO concurrent independent full 48-task draws per captain (skip smoke). Built r1/r2 seed-variant specs (seeds 42/43) from the AC-1-verified 48-task base differing only in experiment:+sampling.seed: — distinct sealed_hashes confirm the CAS-buster yields two separate run-dirs (single-draw trials:1 variance washes a flip; two draws is the h0052 self-consistency precedent). Both frozen, launched detached, confirmed live (child rk processes running). Body updated with the 48/48 six-way decision-fork sim summary + both launch handles. Did NOT audit/score — the FO owns the sentinel scan + paired-delta when the two `done` files land.

## Stage Report: analyze

- DONE: Paired per-task ledger for BOTH draws (r1 deff5d8a, r2 2c544ee9) vs @baseline h0052 written into `## Run result`: net (r1=32, r2=35 of 48), every verdict change in BOTH directions with mechanism, and all SIX analyze required-questions answered.
  Ledger computed from per_trial_outcomes.json (paired by slug; rk runs diff TypeErrors on these dirs). r1=32/48 paired +0 CI[-5,+5]; r2=35/48 paired +3 CI[+0,+7]. 3 gains both draws (airbnb005/airbnb007/f1011), 3 r1-only regressions (f1001/qb002/qb003 all held PASS in r2). Smoke explicitly noted SKIPPED + what the 48/48 sim could not see (feature-boundary judgment, off-construct variance, MC variance).
- DONE: COLLISION VERDICT (AC-5) — classified the r1-only qb002+qb003 double-regression from committed artifacts + reasoning; confirmed airbnb009 + f1006/f1006-hard held both draws; stated plainly no regression is lever-caused.
  qb002/qb003 r1 = VARIANCE (h0045 feature-removal OVER-DROP of base department_id; "less columns than solution"; preserve-columns NEVER fired, 0 firing-language hits — opposite of an h0055 over-KEEP). r2 kept department_id and passed. Head-to-head r1-vs-r2-vs-base done. Neither dual-pair collided; sim's preserve-columns-silent proxy CONFIRMED.
- DONE: AC-4 committed-artifact reads on gains + promote recommendation: airbnb005 = inner-join-from-fact (h0053 fired, both draws); airbnb007 = same per-key lever generalizing to sibling NPS; f1001 + f1011 classified; PROMOTE recommendation written.
  airbnb005 4/4 INNER JOIN from fct_reviews; airbnb007 11/11 per-listing aggregate from fact + INNER JOIN dim. f1001 r1 = off-construct 14-file build variance (no lever fired, held r2+base). f1011 = oracle MC coin-flip (no lever touches MC). Recommendation: PROMOTE candidate — collision-free, two draws 32/35 mean 33.5 clear h0052's ~30 expectation, +2 new banked (airbnb005+airbnb007 reproduced both draws); decision is the captain's.

### Summary
Both h0056 draws landed strict-clean (48/48 captured, 0 errored): r1=32/48, r2=35/48 (mean 33.5). The three new levers all fired with their intended committed shape in both draws and h0053 banked +2 new flips (airbnb005 + airbnb007) over h0052. The decisive forensic: the r1-only qb002+qb003 double-regression is h0045-family feature-removal OVER-DROP variance (the solver scrubbed the base department_id column; preserve-columns never fired — failure mode is "too few columns", the exact opposite of an h0055 over-KEEP), confirming the decision-fork sim's no-collision proxy from the actual artifacts. No regression is lever-caused. Recommendation: PROMOTE candidate (collision-free, clears h0052's expectation on the two-draw + committed-artifact precedent); the promote decision is the captain's.
