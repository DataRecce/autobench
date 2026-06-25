---
id: spd0005
title: Compose conditioned-grain (spd0004) + value-level semantics (spd0003) — the grain-fixed-but-value-failing cells
status: smoke
kind: hypothesis
source: spd0004 conclude (validated-not-promoted) — grain-fixed cells (jira/salesforce/pendo) still fail on value-level residuals; grain alone nets only variance-band +2
started: 2026-06-25T01:02:44Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

spd0004 validated the conditioned-grain lever as construct-steering but it nets only a variance-band
+2 standalone, because the cells whose GRAIN it fixes (jira001 grain 2→3=gold, salesforce001 55→91=gold,
pendo001 spine) then fail on **value-level** residuals — which is spd0003's family. Claim: **composing**
spd0004's grain classifier with spd0003's value-level discipline (column-completeness / value
re-derivation / count-grain) flips the grain-fixed-value-failing cells that neither lever flips alone,
for a durable lift past the single-draw noise band.

Plan: gate-compose both lever families in one README (disjoint construct families → additive per the
ade gated-compose lesson), smoke on the grain-fixed-but-value-failing set (jira001, salesforce001,
pendo001, xero001) + marketo001 (hold the grain win) + f1001/mrr001 canaries, and require a **≥3-draw
hold-rate** before any promote (single full draw is not promotable — the spd0004 lesson).

## Acceptance criteria

- **AC-1** — Flips ≥2 grain-fixed-but-value-failing cells (jira001/salesforce001/pendo001/xero001)
  FAIL→PASS, attributable to the value-level discipline ON TOP of the correct grain (smoke evidence:
  the cell already had the right row set under spd0004; now its values match).
- **AC-2** — Holds spd0004's grain win marketo001 and spd0004's value-flips retail001/quickbooks003
  (no regression from adding the value layer).
- **AC-3** — Zero regression on canaries f1001/mrr001; tpch001 grain stays SCOPE-TO-ACTIVE.
- **AC-4** — Independent variable: README = spd0004 grain classifier (§4) + the new value-level §7;
  leak-guard intact; the re-derivation rule is oracle-FREE (no gold access).
- **Promotion bar (deferred to full):** a ≥3-draw hold-rate, NOT a single +N draw (the spd0004 lesson).

## Smoke set (propose → smoke gate)

Spec `specs/spd0005-compose-grain-value.smoke.frozen.yaml` (harbor-local, gpt-5.5/xhigh, trials 1, conc 4).

| task | @baseline | spd0004 | role |
|---|---|---|---|
| jira001 | ❌ | ❌ (grain fixed, value residual) | 🎯 should-flip via value layer |
| salesforce001 | ❌ | ❌ (spine right, value residual) | 🎯 should-flip via value layer |
| pendo001 | ❌ | ❌ (spine, value residual) | 🎯 should-flip via value layer |
| xero001 | ❌ | ❌ (over-shoot/key) | 🎯 should-flip (FK-id + spine) |
| retail001 | ❌ | ✅ (count-grain) | 🛡️ hold (value lever must keep it) |
| quickbooks003 | ❌ | ✅ | 🛡️ hold |
| marketo001 | ❌ | ✅ (grain) | 🛡️ hold grain win |
| tpch001 | ❌ | ❌ | 🛡️ scope canary (value-def hard core) |
| f1001 | ✅ | ❌(c) / ✅(smoke) | 🛡️ regression canary |
| mrr001 | ✅ | ✅ | 🛡️ regression canary |

GO read: ≥2 should-flip via the value layer AND holds (marketo/retail/quickbooks003) AND canaries hold.

## Stage Report (propose)

- **Spec** authored + frozen + `rk run --explain` clean (10 cells; the §7 value-level prose present).
- **Leak-guard**: README = spd0004 grain classifier + new value-level §7; no-external-reference prose
  intact; the INDEPENDENT RE-DERIVATION rule is explicitly oracle-FREE (reconcile two of the agent's
  OWN derivations, no gold). `diff @baseline` = grain §4 + value §7 only.
- **Smoke table**: above. Auto-approved propose → smoke (captain directive: auto-approve until smoke go).

### Feedback Cycles

**Cycle 2 (auto-revise toward smoke go).** Smoke c1: jira001 FLIP (value layer worked on the designed
target) + held marketo/quickbooks003/retail001, BUT regressed BOTH stable canaries f1001 AND mrr001 —
the generic value-§7 over-fired, making the solver rework already-correct models and break them
(mrr001 rock-stable across all prior runs). Fix: added an APPLY-MINIMALLY guard ("if a target already
builds clean and matches the instruction, LEAVE IT — re-engineering a correct model is a regression
risk") and scoped INDEPENDENT RE-DERIVATION to the PRIMARY metric only ("if the two agree, stop"). Re-smoke c2.

## Stage Report (smoke — cycles 1 & 2: VARIANCE-DOMINATED, no clean GO)

Both single-draw smokes vs @baseline (run dirs `…spd0005-smoke/66b144ed`, `…-c2/e0cf153d`):

| cell | role | c1 | c2 | cross-draw |
|---|---|---|---|---|
| marketo001 | hold-g | PASS | PASS | ✅ STABLE pass (grain, spd0004 carryover) |
| quickbooks003 | hold-v | PASS | PASS | ✅ STABLE pass |
| salesforce001 | flip | fail | **PASS** | ⚠️ FLICKER |
| jira001 | flip | **PASS** | fail | ⚠️ FLICKER |
| retail001 | hold-v | PASS | fail | ⚠️ FLICKER |
| mrr001 | regr-canary | fail | PASS | ⚠️ FLICKER (c2 guard recovered it) |
| f1001 | regr-canary | fail | fail | ❌ CONSISTENT regression |
| pendo001/xero001/tpch001 | flip/scope | fail | fail | consistent fail |

c1: 4 flips, 2 canary-regr. c2: 3 flips, 1 canary-regr. **The two draws disagree on 4 of 10 cells**
(salesforce, jira, retail, mrr001 all flip PASS↔fail between identical-README draws).

**Verdict: NO clean smoke GO — the composition's signal is single-draw VARIANCE-DOMINATED.** Durable
cross-draw signal = marketo001 + quickbooks003 stable-pass (already in spd0004's reach), f1001 a
CONSISTENT regression the composition introduces, and the designed value-flips (jira/salesforce)
merely FLICKER — no stable new flip attributable to the value layer. This reconfirms the standing
lesson (spd0004; DAB dab0016/dab0017): grain+value README levers add ±variance, and a single draw —
or even two — cannot establish a GO. A trustworthy decision needs a per-cell ≥3-draw HOLD-RATE.

Bounded stop reached (smoke-go decision = NO clean GO). Recommend: 3-draw hold-rate confirm on the
flicker cells, OR conclude spd0005 validated-not-promoted (value layer = generative destabilizer,
confirming spd0003's low-ceiling prediction). Holding for captain — not auto-advancing to full.
