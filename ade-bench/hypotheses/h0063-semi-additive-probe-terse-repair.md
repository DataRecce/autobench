---
id: h0063
title: Domain-blind monotonicity-probe trigger with h0044's TERSE max()-at-grain repair wording (verbosity-vs-domain-name isolation)
status: smoke
kind: hypothesis
source: h0062 smoke-rejection deep-dive — h0062 coupled TWO changes (removed the F1 domain name AND added a verbose probe block + forbidden-branch enumeration) and regressed f1006-hard + f1005-medium onto the forbidden row_number/QUALIFY latest-row branch. This isolates the two changes — keep the domain-blind probe trigger, restore h0044's terse repair wording.
started: 2026-06-17
completed:
verdict:
score:
worktree:
---

## Hypothesis

**REV2 (current — gate-hardening; supersedes the rev1 verbosity claim, which was
FALSIFIED).** The rev1 smoke (terse domain-blind, NO-GO 15/21) settled the
verbosity-vs-domain-name question and surfaced the real mechanism — see
`## Smoke result` / `## Behavioral analysis` / `## Failure Review` (committed 6d80eac).
Findings carried forward: (a) **verbosity is NOT the cause** — domain-named+terse
(@baseline h0061) PASSED, domain-blind+verbose (h0062) and domain-blind+terse (h0063
rev1) BOTH committed the constructor-only `Got 2` miss; (b) the de-overfit was blocked
not by the missing domain name per se but by a **brittle STRICT-monotonicity probe +
escape clause** that fires on the **2 real constructor-standings decreases** (post-race
penalties) and drops `constructor_points` to a latest-row branch.

**rev2 claim.** The de-overfit is recoverable by making the probe **tolerant of rare
exceptions** while staying **domain-blind**: a measure that trends non-decreasing APART
FROM a few isolated drops (rare penalties / corrections / restatements — a handful of
rows relative to the sequence length) is STILL a running cumulative total ⇒ `max()` at
grain; a handful of decreases does NOT make it additive and does NOT justify a latest-row
select; reserve `sum()` only for a measure that rises and falls SYSTEMATICALLY (frequent
decreases — a genuine per-period delta). Prediction: `constructor_points` stops drifting
on the 2 penalty decreases, so f1006 / f1006-hard / f1005 / f1005-medium hold `max()` on
BOTH scored models across draws; the additive-SUM canaries stay byte-intact (frequent
decreases still ⇒ `sum()`). **This is a genuinely general dimensional-modeling refinement**
— running totals (standings, account balances, cumulative ledgers) legitimately carry
occasional corrections — NOT an F1-specific hack; the rule names no domain.

---

*rev1 claim (FALSIFIED — verbosity was a red herring; retained for the record):*

**Claim.** The latest-row drift that sank h0062 (f1006-hard + f1005-medium both
committed `row_number`/`QUALIFY` latest-row instead of `max()` at grain) was caused by
the **added verbosity** — the long monotonicity-probe SQL block and the expanded
forbidden-branch *enumeration* — and **not** by removing the F1 domain name. So a rule
that keeps h0062's domain-blind **monotonicity-probe TRIGGER** but restores h0044's
**terse repair wording** (one sentence: probe-fired ⇒ `replace sum(measure) with
max(measure) at the existing grain`, with the forbidden alternatives stated as briefly as
h0044 did, and no inline probe-SQL block) will **reproduce h0044's f1006 / f1006-hard
flips cell-identically** (committed `max()` at grain) while **not regressing** the
same-family sentinels or the additive-SUM canaries.

**Why this is the right isolation.** h0062 changed two things at once:
1. **Trigger:** F1 domain name → domain-blind monotonicity probe. (The de-overfit goal.)
2. **Verbosity:** a 6-line inline probe-SQL block + a longer prose paragraph that
   *enumerates* `latest-row / rank / row_number / QUALIFY / order-by-final-period` as
   things-not-to-do.

h0062's verdict isolated the FAILURE to behavior on the **hard variants** drifting onto
the named-forbidden branch, while the easy targets (f1006, f1005) still committed `max()`
and the additive-SUM canaries held byte-intact (the gate did **not** over-fire). The
transferable lesson recorded there: *naming the forbidden alternatives at length raises
their salience and hands the solver a reasoning path into them; h0044's brevity +
concrete anchor was load-bearing.* This hypothesis tests that lesson directly by holding
the trigger constant (domain-blind probe) and reverting ONLY the verbosity to h0044's
terse form. If h0063 PASSES f1006-hard + f1005-medium, the verbosity was the culprit and
the de-overfit is salvageable. If h0063 STILL regresses them, removing the domain name
itself is what breaks the construct — and the Category-C pin is confirmed un-de-overfittable.

**The single README change.** In `solver_workflows/h0063-.../README.md`, replace the
current `CUMULATIVE-SNAPSHOT TOTALS — max() AT ENTITY GRAIN (gated)` block with a terse
SEMI-ADDITIVE rule that keeps the domain-blind trigger but matches h0044's length:

> **SEMI-ADDITIVE / SNAPSHOT MEASURE — max() AT ENTITY GRAIN (gated).** When repairing
> entity/period totals that are too high and the model sums a numeric measure across a
> sequence within each entity, first check whether the measure is non-decreasing within
> each entity ordered by its sequence key (a running cumulative snapshot, not a per-period
> delta); if so, replace `sum(measure)` with `max(measure)` at the existing entity/period
> grain in every affected model. Do NOT switch to latest-row, rank, row_number, QUALIFY,
> order-by-final-period, or results-recomputation unless local evidence proves
> `max(measure)` wrong. If the measure rises and falls (a genuine per-period delta), keep
> `sum`.

This is **one block, ~7 lines** — the same length envelope as h0044's original — with the
domain-blind monotonicity condition stated inline as a clause ("non-decreasing within each
entity ordered by its sequence key") rather than expanded into a separate 6-line probe-SQL
block. The forbidden-branch list is kept *exactly as terse as h0044's* (the original
already named those branches in one sentence — h0062's regression came from the SURROUNDING
added bulk, not that list, so this isolation keeps the list at h0044 length and removes the
bulk). The repair = `max()` at the existing grain, unchanged from h0044.

**Critical design constraint.** Hold the TRIGGER constant vs h0062 (domain-blind
monotonicity, no F1 name) and revert ONLY the VERBOSITY to h0044's terse form. This is a
clean single-variable isolation: h0062 = domain-blind + verbose; h0063 = domain-blind +
terse; h0044/@baseline = domain-named + terse. Comparing h0063 vs h0062 attributes the
drift to verbosity; comparing h0063 vs @baseline attributes any residual to the domain name.

**Target datasets.**
- Flip-preservation targets: `ade-bench-f1006`, `ade-bench-f1006-hard` (must stay PASS,
  committed SQL = `max()` at grain, cell-identical to @baseline). f1006-hard is the cell
  that DRIFTED under h0062 — the primary test of this isolation.
- Same-family sentinels: `ade-bench-f1005`, `ade-bench-f1005-medium` (cumulative fixes; the
  probe must still resolve to `max()` — f1005-medium also drifted under h0062), `ade-bench-f1001`
  (f1 build; gate must NOT fire — a known build coin-flip, watch as variance).
- Additive-SUM canaries (the FALSE branch must leave legitimate sums byte-intact):
  `ade-bench-airbnb005` (rolling-28d daily-count SUM per listing/date), `ade-bench-airbnb001`
  (monthly review COUNT). Both held byte-intact under h0062 — re-run to confirm the terse
  wording still does not over-fire.

## Pre-smoke Decision-Fork Probe

*(This hypothesis forks from a SMOKE REJECTION — h0062 — so a decision-fork probe is
required. The fork under test is structural prose, not new data, so the "probe" is the
committed-artifact contrast already in hand from h0062's run plus the proposed terse wording.)*

- **Fork under test.** Under the SAME domain-blind monotonicity-probe trigger, does TERSE
  repair wording (h0063, h0044-length) keep the solver on `max()` at grain for the hard
  cumulative variants, where VERBOSE wording (h0062) drifted it onto `row_number`/`QUALIFY`?
- **Prompt context.** Solver-visible only: the f1 `*_points` model SQL (`sum(points)` with
  the too-high total) + the shipped `*_standings` seed/source rows. No hidden verifier counts.
- **Control A (verbose, FAILED — already run).** h0062 run-dir
  `runs/ade-bench-h0062-semi-additive-measure-generalize-maxpoints/63ffe07e1eefe1d6`:
  f1006-hard committed `row_number() over (… order by round desc) WHERE standings_order=1`
  and f1005-medium committed `QUALIFY ROW_NUMBER() OVER (… ORDER BY round DESC)` →
  `AUTO_constructor_points_equality` Got 2 on both (driver_points PASSED). This is the
  measured baseline for the verbose arm — a real `rk` run, not a proxy.
- **Control (domain-named, PASSED).** @baseline h0061
  `runs/ade-bench-h0061-lean-readme/50e340fd462032af`: f1006-hard committed `max(cs.points)`
  → PASS. The terse + domain-named arm.
- **Proposed B (terse + domain-blind).** Expected: f1006-hard / f1005-medium commit `max()`
  at grain (matching @baseline) iff verbosity — not the domain name — was the cause.
- **Expected artifact signature in a real run.** The committed f1006 / f1006-hard /
  f1005 / f1005-medium models use `max(<measure>)` at the existing entity/season grain —
  identical to the @baseline / h0044 artifact; `Got N` unchanged vs @baseline. The
  additive-SUM canaries keep `sum()` byte-intact.
- **Proxy caveat.** Controls A and the domain-named control are REAL `rk` runs (h0062, h0061),
  not subagent proxies — this is stronger than a typical decision-fork probe. The residual
  uncertainty is only whether the proposed terse-domain-blind wording lands `max()` on the
  hard variants; smoke on the real run settles it. This does NOT prove the production solver
  will (a) read the inline monotonicity clause, (b) pick the right sequence key, or (c)
  resist the latest-row branch under terser wording. Smoke is required.
- **Clean-room subagent simulation — INCONCLUSIVE.** A clean-room subagent sim was run on the
  proposed terse-domain-blind wording but could NOT reproduce h0062's known real-run
  `row_number`/`QUALIFY` drift: the sim arm committed `max()` 5/5 even on the VERBOSE (h0062)
  wording, i.e. it failed to reproduce the very failure this hypothesis exists to fix. A sim
  that cannot recreate the control-A failure cannot discriminate the terse arm from the verbose
  arm, so it carries no signal here. The real multi-draw smoke (trials:3, so f1006-hard /
  f1005-medium yield a 3-draw distribution) is therefore the only reliable test — exactly the
  variance-vs-causation rationale of the h0061 asana002 3x probe.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0063-semi-additive-probe-terse-repair.yaml`.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the same run-dir.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline`.**

**AC-4 — Verbosity-isolated behavior preservation (the actual test).** PASSES iff:
  1. `f1006` AND `f1006-hard` stay PASS with committed SQL `max()` at the entity/season
     grain (cell-identical to `@baseline`; `Got N` unchanged) — the terse domain-blind
     wording reproduced the flip the verbose domain-blind wording lost; AND
  2. `f1005` AND `f1005-medium` stay PASS (probe resolved to `max()`, no latest-row drift); AND
  3. zero regressions on the additive-SUM canaries (FALSE branch left `sum()` byte-intact).
  FAILS if f1006-hard or f1005-medium regresses onto the forbidden latest-row/window branch
  (⇒ removing the DOMAIN NAME, not the verbosity, is what breaks the construct — the
  Category-C pin is confirmed un-de-overfittable) or any additive-SUM canary flips PASS→FAIL.
  f1001 is watched as the known build coin-flip (variance, not a verdict-driver).

## Gatekeeper review

**Recommendation (rev2): APPROVE** — rev2 makes ONE artifact-pointed change: it hardens the FALSE-branch gate to tolerate rare isolated drops AND removes the rev1 escape clause ("unless local evidence proves max() wrong") that the rev1 smoke proved was the hazard; still one block, leak-clean, fully domain-blind, full spec keeps trials:1, smoke trials:3 is the justified multi-draw probe; gated structural repair grounded in REAL rk controls (rev1 smoke 7850ae9e + h0062 FAIL / h0061 PASS).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-17T19:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | rev2 README diff vs parent h0061 (resolved: `@baseline` = `runs/ade-bench-h0061-lean-readme/50e340fd462032af`) touches exactly ONE block, under `## Stage: Implementation` (the only stage header before the change; others are Exploration L34, Validation L252, Finalization L265): `CUMULATIVE-SNAPSHOT TOTALS` (6 lines) → `SEMI-ADDITIVE / SNAPSHOT MEASURE` (13 lines). No other `## Stage:` section, no leak-guard/dependency prose changed. One idea: domain-blind rare-exceptions-tolerant monotonicity gate + terse max()-at-grain repair. The +7 lines spell out the rare-exceptions tolerance (the intended single change), not scope creep. |
| G2 leak-guard intact | PASS | grep of the added (`^>`) lines for `AUTO_*`/`solution__`/`check_`/`tests/`/`verifier`/`equality test`/`expected` → NO matches. Same grep also clean for domain tokens `F1`/`race`/`standings`/`driver`/`constructor`/`points`/`season`/`grand prix`. No `curl`/`wget`/`clone`/external-fetch prose touched. Leak-clean. |
| G3 spec two fields | PASS | `diff baseline.yaml h0063…yaml` shows only `experiment:` and `solver_workflow:` changed. `agent.kind: spacedock_solver` (L4) + `runtime: codex` (L5) preserved. Full spec `trials: 1` (L24). |
| G4 smoke tasks-only | PASS (1 note) | smoke diff adds `benchmark.tasks:` (7 IDs, all `ade-bench-` prefixed: f1006, f1006-hard, f1005, f1005-medium, f1001, airbnb005, airbnb001 — covers every hypothesis target). NOTE per operator (a): smoke also sets `trials: 3` + `concurrency.trials: 3` — a DELIBERATE multi-draw variance probe (f1006-hard/f1005-medium → 3-draw distribution; same rationale as h0061 asana002 3x). G3/G4 trials:1 applies to the FULL spec only, which is correctly trials:1. Not auto-FAILed; smoke-only, justified, precedented. Recorded for the captain. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1715B, trials:1) and `…smoke.frozen.yaml` (1870B, trials:3) exist; both carry `kind: spacedock_solver` + `runtime: codex` (L4–5) and the rev2 `solver_workflow_content_hash: sha256:6978723f…` (re-frozen for rev2, matches the operator's stated hash). |
| G6 resolver fidelity | PASS | rev2 inserted text matches the rev2 ## Hypothesis claim on all four points: (i) rare-exceptions-tolerant gate — "trends non-decreasing APART FROM A FEW ISOLATED DROPS (rare penalties, corrections, or restatements — a handful of rows)"; (ii) max() even with a handful of drops — "A handful of decreases does NOT make it additive … max() at the grain is still the minimal correct repair (it ignores the dips)"; (iii) no latest-row — "does NOT justify selecting a single latest row"; (iv) sum() only for systematic rise-and-fall — "Reserve sum() ONLY for a measure that rises and falls SYSTEMATICALLY (frequent decreases)". DOMAIN-BLIND confirmed (grep clean; uses "measure"/"entity/period"/"sequence key", not points/race/standings). The rev1 escape clause "unless local evidence proves max() wrong" is REMOVED — the documented rev1 hazard is gone. Touches exactly one block. Generative-derivation form (replace at grain), not self-anchored. |
| G7 actionability/inert-risk | PASS | Concrete mechanical substitution: `replace sum(measure) with max(measure)` at the existing entity/period grain — a named edit, not abstract FROM/spine restructuring. The asana002-class "do, don't reason-into" form. The gate condition is stated as one inline clause (no probe-SQL block to reason around). |
| G8 regression-canary coverage | N/A (PASS) | Lever is GATED (fires only "when repairing entity/period totals that are too high and the model sums a numeric measure across a sequence" with the non-decreasing-apart-from-rare-drops condition), not generative. Smoke still carries cross-family canaries: airbnb005 + airbnb001 (additive-SUM FALSE-branch sentinels) + f1001 (f1 build; gate must not fire). The gate is the isolation mechanism; rev1 smoke confirmed both airbnb canaries 3/3 byte-intact. |
| G9 selector independence | N/A (PASS) | Not a multi-candidate / selector protocol — a single gated repair rule. |
| G10 self-correcting false-positive | N/A (PASS) | Not a check/reconcile/validate-and-fix lever — a gated structural repair (sum→max), no "verify a figure and act on disagreement" instruction. Per operator (c): rev2 REMOVED the rev1 "unless local evidence proves max() wrong" escape clause that was the rev1 false-positive hazard, so the only conditional left selects sum() vs max() by the measure's own movement pattern — a selection rule, not a self-reconcile. Confirmed N/A. |
| G11 multi-model-target risk | WARN | f1 `*_points` targets are scored by ≥2 models (`AUTO_driver_points_equality` + `AUTO_constructor_points_equality`; the rev1 smoke showed driver PASS / constructor Got 2 on every failing draw). The lever applies to all summed-measure points models (covers-all in scope), but each f1-points verdict is gated by `constructor_points`. Treat any single-draw flip as needing multi-draw confirmation; judge by the committed artifact on EVERY scored model. The trials:3 probe directly addresses this — and rev1's run already proved BOTH models PASS together on the 6 passing draws (no single-model false credit). |
| G12 decision-fork probe quality | PASS | Per operator (d): the rev2 mechanism is grounded in a REAL rk run, not a subagent proxy. The rev1 smoke (run-dir 7850ae9e524dcb7a, strict-audit clean) is the measured control — it produced the artifact (constructor Got 2 from the escape clause firing on the 2 real constructor-standings decreases) that rev2 is designed to fix. Prior controls also real: h0062 (domain-blind verbose, FAIL) / h0061 (domain-named, PASS). The clean-room subagent sim was honestly recorded INCONCLUSIVE (could not reproduce the drift) → no subagent-count→pass-rate overclaim. No hidden-correct labels / verifier output used as prompt evidence. |

**For the captain (rev2):** No FAILs → APPROVE; advance to smoke. This is the artifact-pointed rev2 the rev1 Failure Review recommended (gate-hardening + escape-clause removal), not the FO's concrete-neutral-anchor ladder. Two items to weigh: (1) G4 — smoke is INTENTIONALLY trials:3 (multi-draw variance probe); read it as a 3-draw distribution on f1006-hard/f1005-medium, not a single GO/NO-GO; full spec correctly stays trials:1. (2) G11 — credit an f1-points flip only when the committed `max()` artifact lands on BOTH `driver_points` AND `constructor_points` (the persistent miss has been constructor-only). The open risk rev2 must actually clear: rev1's behavioral analysis found the PASS/FAIL split was a probe-depth coin flip — a deeper probe surfaces the 2 constructor decreases and (under rev1) the escape clause then licensed the latest-row drift. rev2 removes that escape clause and reframes a handful of drops as still-cumulative, so the deep probe should no longer have a license to abandon max(); smoke is the test of whether the reframed gate holds when the probe finds those 2 decreases.

## Smoke result

### rev2 (CURRENT — gate-hardening) — GO-leaning, 20/21

**Verdict: GO-with-one-residual (20/21 = 0.9524).** Multi-draw smoke, run-dir
`runs/ade-bench-h0063-semi-additive-probe-terse-repair/2bba19d41a474310` (57m, rc=0,
0 errors). Strict audit CLEAN (`taint_status: clean`, findings: [] on all 21 cells); all
21 cells captured a reward; `rk score` = stratified mean 0.9524 = 20/21.

**Per-cell per-draw distribution (rev2):**

| Task | rev2 draws | rev2 rate | rev1 rate | Both models on passes? |
|------|-----------|-----------|-----------|------------------------|
| f1006              | 1,1,1 | **3/3** | 0/3 | BOTH PASS — **0/3→3/3, decisive** |
| f1006-hard         | 0,1,1 | 2/3 | 2/3 | passes BOTH PASS; 1 residual fail = constructor Got 2 |
| f1005              | 1,1,1 | **3/3** | 2/3 | BOTH PASS |
| f1005-medium       | 1,1,1 | **3/3** | 2/3 | BOTH PASS |
| f1001              | 1,1,1 | 3/3 | 3/3 | build; gate did not fire |
| airbnb005          | 1,1,1 | 3/3 | 3/3 | additive-SUM byte-intact (no over-fire) |
| airbnb001          | 1,1,1 | 3/3 | 3/3 | additive-SUM byte-intact (no over-fire) |

**The single residual** is one f1006-hard draw (`7pRy7uZ`): same signature as the rev1
drift — `constructor_points_equality` FAIL Got 2 / driver PASS. Everything else holds
`max()`. f1-points constructor-drift rate fell from rev1's ~6/12 draws to rev2's **1/12**.

---

### rev1 (FALSIFIED arm — terse domain-blind) — NO-GO, 15/21

**Verdict: NO-GO (15/21 = 0.7143).** Multi-draw smoke, run-dir
`runs/ade-bench-h0063-semi-additive-probe-terse-repair/7850ae9e524dcb7a` (58m54s, rc=0,
0 SpacedockSolverAgentError — the two earlier 21/21-errored runs were the
`RAZORBACK_SPACEDOCK_PLUGIN_DIR` env bug; ignore). Strict audit CLEAN
(`taint_status: clean`, findings: [] on all 21 cells). `rk score` = stratified mean
0.7142857 = 15/21; all 21 cells captured a reward (no residual infra).

**Per-cell per-draw distribution (3 draws each):**

| Task | Draw rewards | Pass rate | Both scored models? | Read |
|------|--------------|-----------|---------------------|------|
| f1006              | 0,0,0 | **0/3** | constructor FAIL Got 2 / driver PASS on all 3 | REGRESSED — new vs @baseline AND h0062 |
| f1006-hard         | 1,0,1 | 2/3 | pass-draws BOTH PASS; fail-draw constructor Got 2 | held 2/3 |
| f1005              | 0,1,1 | 2/3 | pass-draws BOTH PASS; fail-draw constructor Got 2 | held 2/3 |
| f1005-medium       | 1,0,1 | 2/3 | pass-draws BOTH PASS; fail-draw constructor Got 2 | held 2/3 |
| f1001              | 1,1,1 | 3/3 | build; gate did not fire | clean |
| airbnb005          | 1,1,1 | 3/3 | additive-SUM FALSE branch | byte-intact (no over-fire) |
| airbnb001          | 1,1,1 | 3/3 | additive-SUM FALSE branch | byte-intact (no over-fire) |

**The drift signature is IDENTICAL on every failing f1-points draw** (all 4 tasks): 
`AUTO_constructor_points_equality` FAIL **Got 2**, `AUTO_driver_points_equality` **PASS**.
Not a different bug per cell — one mechanism. Canaries clean: the terse-blind FALSE branch
left legitimate sums byte-intact (airbnb005/airbnb001 3/3); the gate did not over-fire on
the f1 build (f1001 3/3).

## Run result

## Behavioral analysis

### rev2 (gate-hardening) — the de-overfit is SALVAGED, domain-blind

**The wins are artifact-confirmed `max()` on BOTH models.** Spot-checked the constructor
artifacts of 4 winning draws (f1006 jGUBJFd, f1005 6cuJhJF, f1005-medium Dk6wpqQ, f1006-hard
SkLoupm): every one has `AUTO_constructor_points_equality` PASS AND `AUTO_driver_points_equality`
PASS. The rev1 hazard is gone in the common case: the rare-exceptions-tolerant gate now reads
the 2 constructor penalty decreases as "isolated drops within a running cumulative total" and
keeps `max()` at grain — `constructor_points` no longer drifts to latest-row. The decisive
signal fired: **f1006 went 0/3 → 3/3.** f1005 and f1005-medium each improved 2/3 → 3/3.

**The single residual is leftover causal drift, NOT variance — but a rare tail.** The one
f1006-hard fail (`7pRy7uZ`) committed `row_number()`-latest-standings-row for BOTH models
("keep the latest standings row per driver/constructor and season"). Driver still PASSES (its
latest row equals max because driver standings are strictly monotone), constructor FAILS Got 2
(latest-row drops the 2 penalty rows) — the identical rev1 mechanism. So the hardened gate did
not 100% suppress the latest-row reasoning path; one draw in twelve f1-points draws still talked
itself onto latest-row despite the rule's explicit "a handful of decreases does NOT justify
selecting a single latest row." This is a **probe-depth tail**, not noise: it's the same drift,
at ~1/12 vs rev1's ~6/12.

**Verdict on the de-overfit: SALVAGED (GO-with-caveat).** Gate-hardening recovered all four
f1-points targets to a domain-BLIND rule, with no over-fire (airbnb005/airbnb001/f1001 all 3/3,
sums byte-intact). This confirms the rev1 finding twice over: **verbosity was a red herring; the
real blocker was a brittle strict-monotonicity probe + escape clause, and a rare-exceptions-
tolerant probe fixes it without naming F1.** The domain name was NOT irreplaceable — it was a
*proxy* for "treat occasional decreases as corrections, not deltas," which the rev2 rule now
states directly and generally. Residual risk: the latest-row path is still reachable (~8% of
f1-points draws); a single-trial full run could land that tail on f1006-hard. My call: **GO**,
with the residual flagged for the captain — the de-overfit is genuine and general, but a
belt-and-braces rev3 (a one-line `max()` BEFORE/AFTER skeleton to crowd out the latest-row
reasoning path) could push the residual toward 0 if the captain wants it tighter before
promotion. NOT my call to run full or promote — held for the captain.

---

### rev1 (FALSIFIED arm) — root cause analysis (retained)

**Root cause — the escape clause fires on the 2 real constructor-standings decreases; the
domain name was load-bearing because it pre-committed the snapshot interpretation BEFORE the
probe could find them.** Artifact read of the solver transcripts (`agent/codex.txt`):

- **driver_points** (PASS on every draw): the solver's local probe finds driver standings are
  strictly non-decreasing (0 decreases over 34,680 rows) → monotonicity probe TRUE →
  `sum→max(points)` → correct.
- **constructor_points** (FAIL Got 2 on every failing draw): constructor standings have **2
  decreases** (post-race penalties/resets, e.g. "Force India 2018 went 59 → 18/52"). On the
  FAILING draws the solver's probe SURFACES those 2 decreases, reads the README clause "unless
  **local evidence proves `max(measure)` wrong**" as satisfied, and SWITCHES constructor to a
  **final-season-snapshot / latest-row** branch (`row_number`/`QUALIFY`/"final standings row
  per constructor-season"). The true answer is still `max()`; the off-by-2 is exactly those 2
  penalty rows the final-row branch drops. → `Got 2`.
- **The split is a probe-depth coin flip:** the PASSING draws committed `max(cs.points)` and
  simply never surfaced the 2 decreases — they probed "0 mismatches vs max(points)" and stopped.
  The FAILING draws ran a deeper investigation, found the decreases, and the escape clause gave
  them permission to abandon max(). f1006 (the plainest "figure out what's wrong" framing)
  invites the deepest investigation → 0/3 (deterministic FAIL, NOT variance); the harder
  variants fail 1/3 (coin-flip on probe depth).

**Verbosity-vs-domain-name verdict — the DOMAIN NAME is load-bearing; verbosity was NOT the
cause.** Three real `rk` arms, same constructor data:
- @baseline h0061 (domain-NAMED + terse): f1006 PASS — committed `max(cs.points)` on
  constructor EVEN THOUGH its transcript mentions latest/QUALIFY/row_number. The concrete
  anchor ("treat points as cumulative race-by-race snapshots") pre-committed the snapshot
  interpretation, so the 2 decreases never dislodged max().
- h0062 (domain-BLIND + verbose): constructor Got 2 (same miss).
- h0063 (domain-BLIND + terse): constructor Got 2 (same miss) — AND a NEW f1006 0/3 regression.

Reverting the verbosity did NOT recover the flip. Both domain-blind arms (verbose h0062 AND
terse h0063) drift constructor onto the latest-row branch by the SAME mechanism. The single
isolated variable is settled: **removing the domain name is what breaks the construct, not the
verbosity.** The h0062-recorded "verbosity raised salience" lesson was a red herring — the
real driver is that the domain-blind monotonicity probe, lacking the snapshot anchor, treats
the 2 legitimate-but-decreasing constructor rows as evidence against max(). The Category-C pin
(domain-named max()-at-grain) is confirmed **un-de-overfittable** by trigger-genericization
alone: the F1 domain name does load-bearing work that no domain-blind monotonicity test
reproduces, because the constructor data is NOT actually monotonic.

**G11 confirmed:** all 6 passing f1-points draws have BOTH `constructor_points_equality` AND
`driver_points_equality` PASS — no single-model false credit. Every failing draw fails on
constructor only. The trials:3 design correctly exposed f1006 as deterministic-FAIL (0/3), not
a one-draw fluke.

## Failure Review

**Primary failure type: escape-clause-triggered latest-row drift on non-monotonic real data
(de-overfit-by-genericization wall).** The terse domain-blind rule is behaviorally WORSE than
@baseline on the easy target (f1006 0/3 regression) and no better on the hard variants — it
inherits h0062's exact constructor-only Got-2 miss. NO-GO by AC-4: f1006 + the failing draws of
f1006-hard/f1005/f1005-medium regressed onto the forbidden branch; the de-overfit is NOT
salvageable by reverting verbosity.

**What this rules out / banks (knowledge gain):**
1. Verbosity is NOT the h0062 culprit — REJECTED as a cause by a clean single-variable run.
   Do not re-test wording length on this construct.
2. The domain name in the @baseline CUMULATIVE-SNAPSHOT rule is **load-bearing** — it pre-anchors
   the snapshot interpretation so the solver does not act on the 2 real constructor decreases.
   A domain-blind monotonicity probe cannot replace it because constructor points genuinely
   decrease (penalties), so any "non-decreasing?" gate self-defeats on constructor.
3. The escape clause "unless local evidence proves max() wrong" is the active hazard once the
   anchor is removed: a deeper probe + a real decrease = permission to drift. The PASS/FAIL
   split is probe-depth, not wording.

**Recommended next revision — and a caution against the candidate ladder.** The FO's candidate
ladder (rev2 = concrete domain-NEUTRAL anchor like "running-total / account-balance"; rev3 =
add a max() BEFORE/AFTER skeleton) addresses VERBOSITY/CONCRETENESS, but the artifacts say the
problem is **NOT** concreteness — it is that the domain-blind probe + escape clause act on the
2 legitimate constructor decreases. A neutral analogy alone will NOT stop a deep probe from
finding those decreases and firing the escape clause. The artifact-pointed fix is to **neutralize
the escape clause's interaction with small decreases**, NOT to re-decorate the trigger:

- **rev2 (artifact-pointed): keep the domain-blind trigger but HARDEN the FALSE-branch gate** —
  state that a SMALL number of within-entity decreases (a handful of rows, consistent with
  penalties/adjustments) does NOT disqualify max(): the measure is "non-decreasing apart from
  rare downward corrections" still ⇒ max() at grain. I.e. change the monotonicity test from
  strict to "monotone-with-rare-exceptions", and keep the escape clause for a measure that
  rises-and-falls *systematically* (a true per-period delta), not one with 2 penalty dips. This
  directly targets the observed mechanism (2 decreases → escape → drift) and is still
  domain-blind. Pair it with the existing terse repair.
- **rev3 (fallback): the concrete domain-NEUTRAL anchor** (running-total / cumulative-balance
  analogy + the existing terse max() repair) only if rev2's gate-hardening still leaks — but
  expect it to be insufficient alone, because it does not stop the deep probe.
- **If both leak: conclude the pin is un-de-overfittable** and route conclude-REJECTED (present
  to captain; do not auto-conclude). The domain name's load-bearing work — pre-committing the
  interpretation so a real-data decrease never reaches the escape clause — may be irreducible.

My recommendation: **rev2 = gate-hardening (monotone-with-rare-exceptions)**, because it is the
ONLY candidate that addresses the mechanism the artifacts actually show. The neutral anchor
(rev3) treats a symptom (anchoring) that the @baseline already had; the disease is the
strict-monotonicity-plus-escape-clause reacting to 2 real decreases.

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: Fork @baseline (h0061-lean-readme/README.md) → h0063 solver dir, replacing ONLY the CUMULATIVE-SNAPSHOT block with the TERSE domain-blind SEMI-ADDITIVE block.
  `diff h0061-lean-readme/README.md h0063…/README.md` = exactly one block changed (188–196); inserted text byte-matches the entity ## Hypothesis quote; domain-blind (no F1/race/standings/points), 9 lines ≈ h0044 envelope, monotonicity stated as one inline clause, no probe-SQL block, forbidden-branch list at h0044-terse, repair = max() at grain.
- DONE: Leak-clean.
  grep of added lines for AUTO_*/solution__*/check_*/dataset-slug/expected-count/verifier/equality-test → none (gatekeeper G2 PASS).
- DONE: Author FULL spec — differs from baseline ONLY in experiment: + solver_workflow:, trials stays 1.
  `diff baseline.yaml h0063…yaml` = 2 fields; kind=spacedock_solver, runtime=codex preserved; trials:1.
- DONE: Author SMOKE spec — multi-draw variance probe.
  benchmark.tasks = f1006, f1006-hard, f1005, f1005-medium, f1001, airbnb005, airbnb001; top-level trials:3 + concurrency.trials:3 (so f1006-hard/f1005-medium yield a 3-draw distribution — variance-vs-causation, h0061 asana002 3x rationale).
- DONE: Freeze both with rk freeze --allow-missing.
  `…frozen.yaml` (full, trials:1) + `…smoke.frozen.yaml` (smoke, trials:3) both written; both carry kind/runtime.
- DONE: Run the gatekeeper subagent and record its per-rule table + overall recommendation in ## Gatekeeper review.
  Recommendation APPROVE — no FAILs; 1 WARN (G11 multi-model f1 *_points: credit a flip only when max() lands on both driver_points AND constructor_points), 1 note (G4: smoke trials:3 is the deliberate probe).
- DONE: Record the clean-room subagent simulation as INCONCLUSIVE in the entity.
  Note added to ## Pre-smoke Decision-Fork Probe: sim committed max() 5/5 even on the verbose arm → could not reproduce h0062's drift → real multi-draw smoke is the only reliable test.

### Summary

Single-variable isolation built: holds h0062's domain-blind monotonicity-probe TRIGGER constant and reverts ONLY the verbosity to h0044's terse max()-at-grain wording (one inline monotonicity clause, no probe-SQL block, forbidden-branch list at h0044 length). All 7 smoke tasks PASS at @baseline (h0061), so this is a flip-PRESERVATION test: the terse domain-blind wording must not regress f1006-hard / f1005-medium onto the row_number/QUALIFY branch that h0062's verbose wording drifted them onto, while the additive-SUM canaries (airbnb005/airbnb001) stay byte-intact. Smoke is a deliberate 3-draw variance probe (trials:3) because a single draw cannot distinguish a coin-flip from causal drift. Gatekeeper APPROVE with one G11 WARN (judge f1 flips by the committed artifact on both scored points models).

## Stage Report: smoke

- DONE: Strict audit + score on the clean run-dir.
  `rk audit … --policy strict` = taint_status clean, findings:[] on all 21 cells; `rk score` = mean 0.7143 = 15/21; all 21 cells captured>0 (no residual infra). run-dir 7850ae9e524dcb7a.
- DONE: Record per-cell per-draw rewards in ## Smoke result.
  f1006 0/3, f1006-hard 2/3, f1005 2/3, f1005-medium 2/3, f1001 3/3, airbnb005 3/3, airbnb001 3/3.
- DONE: Per-target artifact deep-dive AS A DISTRIBUTION (BOTH scored models).
  Every failing f1-points draw = identical signature: constructor_points_equality FAIL Got 2 / driver_points_equality PASS. Passing draws: BOTH equality tests PASS (G11 satisfied). Read from agent/codex.txt worker messages.
- DONE: Tally drift-rate + compare to h0062 / @baseline.
  Domain-blind terse (h0063) drifts constructor onto final-row/latest-row by the SAME mechanism as domain-blind verbose (h0062); domain-NAMED terse (@baseline h0061) committed max() and PASSED. Verbosity REJECTED as cause; domain name is load-bearing.
- DONE: Confirm f1001 (variance) + airbnb005/airbnb001 (byte-intact sum).
  f1001 3/3 (gate did not fire); airbnb005/airbnb001 3/3 (FALSE branch byte-intact, no over-fire).
- DONE: Write distribution table + behavioral read to ## Smoke result + ## Behavioral analysis; append ## Failure Review (NO-GO).
  All three sections written; primary failure type = escape-clause-triggered latest-row drift on non-monotonic real constructor data (2 penalty decreases).

### Summary

NO-GO (15/21). Clean run, strict-audit clean. The key finding (the f1006 0/3 surprise): the
terse domain-blind monotonicity probe SURFACES the 2 real constructor-standings decreases
(post-race penalties), reads the README's "unless local evidence proves max() wrong" escape
clause as satisfied, and switches constructor_points to a final-row/latest-row branch → Got 2 —
the SAME constructor-only miss as h0062. The PASS/FAIL split is a probe-depth coin flip (deeper
probe finds the decreases → escape fires). @baseline's DOMAIN NAME pre-commits the snapshot
interpretation so the decreases never reach the escape clause — that is the load-bearing work no
domain-blind probe reproduces. Verbosity is decisively REJECTED as the h0062 cause. Recommended
rev2 = HARDEN the FALSE-branch gate (monotone-with-rare-exceptions ⇒ still max()), NOT the FO's
concrete-neutral-anchor ladder, which treats a symptom the @baseline already had and won't stop
the deep probe.

## Stage Report: smoke (rev2)

- DONE: Strict audit + score; confirm captured>0 all 21 cells.
  `rk audit … --policy strict` = 21/21 taint clean, findings:[]; `rk score` = mean 0.9524 = 20/21; all 21 cells captured. run-dir 2bba19d41a474310.
- DONE: Record per-cell-per-draw table in ## Smoke result (rev2).
  f1006 3/3 (was 0/3), f1006-hard 2/3, f1005 3/3 (was 2/3), f1005-medium 3/3 (was 2/3), f1001 3/3, airbnb005 3/3, airbnb001 3/3.
- DONE: Confirm WINS are max() on BOTH models (G11).
  Spot-checked 4 winning draws (f1006 jGUBJFd, f1005 6cuJhJF, f1005-medium Dk6wpqQ, f1006-hard SkLoupm): all have constructor_points_equality PASS AND driver_points_equality PASS. Hardened gate held on the 2 penalty decreases.
- DONE: Characterize the ONE residual (f1006-hard 7pRy7uZ).
  Leftover causal drift, NOT variance/unrelated: committed row_number() latest-standings-row for both models; constructor FAIL Got 2 / driver PASS — identical rev1 mechanism, now at 1/12 f1-points draws (was ~6/12). A probe-depth tail.
- DONE: Write ## Behavioral analysis (rev2) — de-overfit verdict.
  SALVAGED / GO-with-caveat: gate-hardening recovered all 4 f1-points targets to a domain-BLIND rule, no over-fire; verbosity confirmed a red herring twice; residual ~8% latest-row tail flagged; optional rev3 (max() skeleton) could tighten it.

### Summary

rev2 GO-leaning at 20/21, strict-audit clean. The gate-hardening WORKED: f1006 0/3→3/3
(decisive), f1005 + f1005-medium 2/3→3/3, all wins artifact-confirmed `max()` on BOTH scored
models — constructor_points no longer drifts to latest-row on the 2 real penalty decreases. The
single residual (one f1006-hard draw) is the SAME leftover causal drift (row_number latest-row,
constructor Got 2), not variance, but now a rare ~1/12 tail. No over-fire (canaries + build 3/3,
sums byte-intact). De-overfit SALVAGED with a domain-BLIND, genuinely general rule — verbosity
was a red herring; the real fix was a rare-exceptions-tolerant probe. Held for the captain; no
auto-full/promote. Optional rev3 (a max() BEFORE/AFTER skeleton) could push the residual toward 0.
