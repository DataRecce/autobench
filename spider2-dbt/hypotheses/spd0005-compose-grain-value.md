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
