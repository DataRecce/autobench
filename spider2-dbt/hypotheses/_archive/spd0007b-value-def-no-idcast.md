---
id: spd0007b
title: Value-def MINUS the oracle-blind id-cast clause (COUNT-by-name keeper + preserve-source-dtype)
status: conclude
kind: hypothesis
source: spd0007 conclude follow-up — id-cast clause rejected as oracle-blind (broke tpch002/maturity001); isolate the durable value-def signal
started: 2026-06-25
completed: 2026-06-26T00:26:50Z
verdict: PASSED
score: 0.85
worktree:
archived: 2026-06-26T00:26:50Z
---

## Hypothesis

spd0007 (router + value-def) concluded validated-not-promoted: the value-def family split into a
**durable keeper** (COUNT(*)-vs-COUNT(DISTINCT) by column NAME — retail001 attributable, held every
draw) and an **oracle-blind destabilizer** (the Identifier-dtype cast — "schema.yml 'unique
identifier' + numeric source → cast VARCHAR" GUESSES gold dtype, broke tpch002 `p_partkey`
deterministically + is a latent trap on maturity001). spd0007b removes the destabilizer and tests
whether the value-def family nets positive once it's gone.

**The single change vs the (banked, unpromoted) spd0007 solver:** delete the Identifier-dtype CAST
clause and replace it with a **"preserve source dtype — DO NOT GUESS"** rule (carry an id column at
its source type; never re-type it to "match gold"). Everything else is unchanged: the router
(R1–R5, R6-narrowed, R1-precedence guard) + the deterministic value-def clauses (COUNT-by-name,
percentage-convert, NULL-vs-0, money-round-derived-not-raw, per-table sign, key-embedded grain).

**Targets:** retail001 (COUNT keeper — must still flip), recharge001 (percentage), f1002
(NULL-vs-0), asset001 (key-grain), twilio001 (sign). **Recovery targets:** tpch002 + maturity001
(the id-cast victims — removing the cast should let them PASS).

## Pre-smoke Decision-Fork Probe

Offline + prior-run evidence (no new probe needed): retail001's COUNT(*) flip is artifact-attributable
and held across spd0007 v1 + v2 + smoke. The id-cast clause was proven to break tpch002 (`p_partkey`
numeric→VARCHAR vs numeric gold) deterministically and to be a latent trap on maturity001 (gold ids
BIGINT); the preserve-dtype rule removes exactly that failure mode, so tpch002/maturity001 should no
longer be lever-destabilized. The remaining clauses are deterministic and name/discriminator-gated
(no oracle guess). **Watch:** these targets/canaries are flaky per the flake ledger — a single draw
won't decide; promotion requires the ≥3-draw hold-rate (below).

## Acceptance criteria

**AC-1** — only the README changes; full spec diff = `experiment:` + `solver_workflow:` only.
**AC-2** — every score paired with a clean strict audit.
**AC-3** — verdict from a **≥3-draw full-board HOLD-RATE** vs @baseline (single draws swing ±3 here:
the 4 prior full draws were 19/21/20/16). Promote only if the value-def keepers durably net-positive
with NO durable canary regression — judged by per-cell hold-rate + committed-artifact attribution,
not a single draw.

## Autonomy authorization (captain, 2026-06-25)

Captain authorized: **auto-approve the propose gate → smoke; if smoke is GO, auto-approve → full.**
Smoke GO = retail001 flips by committed artifact + the id-cast victims (tpch002/maturity001) hold +
canaries hold + audit clean. HALT for captain on NO-GO or infra failure. After the full run, do the
analyze and HALT — the promote decision + the ≥3-draw hold-rate stay the captain's.

## Gatekeeper review

**Recommendation: APPROVE** — purely-subtractive variant: the oracle-blind id-cast clause is
replaced by an oracle-free "preserve source dtype, DO NOT GUESS" rule (the only spd0007→spd0007b
diff); router + value-def superset is additive over @baseline, leak-guard byte-intact, specs scope
clean, both frozen.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-25.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

Fork parent: `@baseline` resolves to `runs/spider2-dbt-full-baseline/13fb630e2cae3eb8` →
solver_workflow `spider2-dbt-baseline` (the seed). The hypothesis `source:` forks the banked-but-
unpromoted spd0007 solver; spd0007b is reviewed as additive-vs-seed (G1/G2) AND as a one-clause
subtraction-vs-spd0007 (the documented single change). Both diffs confirmed.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | vs seed: one additive block (README 82a83,196 = router R1–R6 + Axis-2 G3 value-def). vs spd0007: a SINGLE hunk (167,170c167,170) swaps the cast clause for the preserve-dtype rule — no other line moved. Leak-guard prose untouched. |
| G2 leak-guard (hidden gold) | PASS | no-fetch sentence (README:11–12 `curl`/`wget`/`git clone`/`git ls-remote`/web) byte-identical seed↔spd0007b. All `gold` hits are pre-existing baseline prose ("hidden gold", "Gold table names…NOT given") + router guard rails ("Never read or guess gold values", "diverges from gold"); zero gold values/dtypes/columns/counts embedded. No `expected_`/`answer_key`/`ground_truth`. The new id rule explicitly tells the solver NOT to guess gold dtype. |
| G3 spec two fields | PASS | `diff full-baseline.yaml spd0007b-…yaml` = `experiment:` + `agent.solver_workflow:` (+ ABOUTME comment) only. kind=spacedock_solver, runtime=codex, model=gpt-5.5, reasoning_effort=xhigh, trials=1 all preserved (full spec lines 6/7/8/18/86). |
| G4 smoke narrows tasks only | PASS | smoke diff = experiment + `benchmark.tasks` (+ABOUTME) only; no `exclude_tasks`. Surviving 7: retail001/recharge001/f1002 (targets) + tpch002/maturity001 (id-cast victims) + activity001/quickbooks002 (canaries). All 3 hypothesis-named smoke targets present. |
| G5 both frozen | PASS | `…frozen.yaml` (3202B) + `…smoke.frozen.yaml` (1713B) both exist; both carry `kind: spacedock_solver` + `runtime: codex` (frozen lines 4/5). |
| G6 resolver fidelity | PASS | Inserted text "Identifier dtype — DO NOT GUESS. Carry an identifier column through at its SOURCE dtype unchanged… never re-type an id column" matches the claim verbatim (delete the cast, add preserve-dtype). Independent/generative-derive rules, not self-anchored validation. No scope creep. |
| G7 actionability/inert-risk | PASS | The replacement is a concrete mechanical negative-instruction (a do-not-edit on a named column class, gated by source dtype) — strictly easier to obey than the deleted cast; remaining value-def clauses are name/dtype-gated mechanical edits. |
| G8 regression-canary coverage | PASS | Value-def clauses are per-column NAME/dtype-gated (not generative) and R1-precedence-guarded off pre-existing models; still, the smoke keeps non-target passing canaries activity001 + quickbooks002 AND the two PASS id-cast victims tpch002/maturity001 as perturbable regression sentinels — coverage on the most-at-risk (id/dtype) family. |
| G9 selector independence | N/A | No multi-candidate / selector protocol declared. |
| G10 self-correcting false-positive | N/A | No validate-and-fix / reconcile lever; the change is a build-time dtype-preservation rule, not a check-and-replace. |

**For the captain:** AUTO-APPROVED to smoke. This is the cleanest possible variant — a single-hunk
subtraction of the clause already concluded harmful (id-cast broke tpch002/maturity001 by guessing
gold dtype), replaced by an oracle-free preserve-dtype rule; no FAILs, no WARNs. Smoke watch: the
two recovery targets tpch002 + maturity001 must now HOLD (they are the proof the cast removal is
clean), retail001 must still flip by committed artifact, canaries hold. Per AC-3 the promote
decision needs the ≥3-draw hold-rate, which remains yours after the full run.

## Smoke result

## Smoke result

Run `runs/spider2-dbt-spd0007b-smoke/a80088ac0af1a9de` (rc=0, audit strict CLEAN). **7/7 PASS —
strongest smoke of the program. GO.**
- 3 TARGET FLIPS (FAIL→PASS), all deterministic value-def clauses: retail001 (COUNT-by-name),
  recharge001 (percentage-convert), f1002 (NULL-vs-0).
- 2 id-cast VICTIMS RECOVERED + held: tpch002, maturity001 — direct proof the oracle-blind cast
  removal fixed them.
- canaries activity001 + quickbooks002 held.
Caveat: single draw; recharge001/f1002 flips + the holds need the ≥3-draw hold-rate (these cells
are flaky per the ledger). Auto-advanced to full per captain authorization.


## Run result

## Run result — full (STRONG, decision-ready)

Run `runs/spider2-dbt-spd0007b-full/b0ebdde3817a52ab` (rc=0, audit strict CLEAN — 61 clean, 0
tainted, 0 errored). **24/61 = 0.3934 vs @baseline 19/61 = 0.3115 — net +5**, the best draw of the
program and ABOVE the prior noise band (4 earlier full draws were 19/21/20/16). One regression
(f1001 = known variance coin-flip). The previously-destabilized cells (tpch002, maturity001,
greenhouse001) ALL HELD — removing the oracle-blind id-cast worked.

| cell | Δ | attribution |
|---|---|---|
| retail001 | +PASS | **ATTRIBUTABLE — COUNT-by-name** (durable: 3 draws) |
| recharge001 | +PASS | **ATTRIBUTABLE — percentage-convert** (`case value_type='percentage' → base*value/100`; durable: smoke+full) |
| asset001 | +PASS | **ATTRIBUTABLE — key-embedded-grain** (grain ticker+date→tt_key minute-level, 77→3430/3185=gold; single draw) |
| f1002 | +PASS | variance (flip = `count(distinct)→count(*)`, a count-grain coin-flip the NULL-vs-0 clause doesn't govern) |
| f1003 | +PASS | router (sibling-mirror; flaky 2/5 full) |
| quickbooks003 | +PASS | variance (variable cell) |
| f1001 | −FAIL | variance (known coin-flip) |

**DURABLE attributable value-def signal ≈ +3** (retail001 + recharge001 + asset001 — three distinct
deterministic clauses, each artifact-confirmed) with **0 attributable regressions** (f1001 is
variance). f1002/f1003/quickbooks003 are variable bonus. This is the value-def family WORKING once
the oracle-blind id-cast destabilizer is removed — a clean inversion of spd0007's −3.

## Verdict

**PASSED — PROMOTED to @baseline (captain decision 2026-06-26).** spd0007b full 24/61 = 0.3934 is the new champion (was 19/61 = 0.3115, +5). Registered in the spider2-dbt-local `razorback-registry.yaml` (`@baseline` → `runs/spider2-dbt-spd0007b-full/b0ebdde3817a52ab`); the global ade-bench `@baseline` is untouched. The new CHAMPION SOLVER = `solver_workflows/spd0007b-value-def-no-idcast` (router R1-R5 + R6-narrowed + R1-precedence guard + value-def: COUNT-by-name, percentage, NULL-vs-0, money-round-derived, sign, key-grain, preserve-id-dtype). Future hypotheses (spd0008 grain) fork from THIS solver. Durable attributable gains banked: retail001 (COUNT), recharge001 (percentage), asset001 (key-grain). Promoted on a single +5 draw above the noise band (captain accepted promote-now over the hold-rate); the variable-bonus cells (f1002/f1003/quickbooks003) may regress on future draws — tracked in the flake ledger.

---
ORIGINAL VERDICT (pre-promotion):

**Strong promote candidate — pending the ≥3-draw hold-rate (this is draw 1).** Net +5 sits above
the ±3 noise band and the core gains are attributable to three distinct deterministic clauses, so
this is real signal, not a lucky draw. But per AC-3 (single full draws here swing ±3) the durable
number should be confirmed: f1002/f1003/quickbooks003 are variable and could regress on another
draw, while retail001/recharge001/asset001 should hold. **RECOMMENDATION (captain decision):** run
2 more full draws (draws 2–3); if the median holds ≥22–23 with retail001/recharge001/asset001
consistent and only variance-class regressions, PROMOTE spd0007b to @baseline. (24 is strong enough
that promote-now is defensible, but the hold-rate is the disciplined path given the variance wall.)
`@baseline` stays 19/61 until the hold-rate.


## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
