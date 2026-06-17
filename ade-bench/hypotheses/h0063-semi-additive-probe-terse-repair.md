---
id: h0063
title: Domain-blind monotonicity-probe trigger with h0044's TERSE max()-at-grain repair wording (verbosity-vs-domain-name isolation)
status: hypothesis
kind: hypothesis
source: h0062 smoke-rejection deep-dive — h0062 coupled TWO changes (removed the F1 domain name AND added a verbose probe block + forbidden-branch enumeration) and regressed f1006-hard + f1005-medium onto the forbidden row_number/QUALIFY latest-row branch. This isolates the two changes — keep the domain-blind probe trigger, restore h0044's terse repair wording.
started: 2026-06-17
completed:
verdict:
score:
worktree:
---

## Hypothesis

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

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
