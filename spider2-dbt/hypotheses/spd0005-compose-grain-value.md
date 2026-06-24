---
id: spd0005
title: Compose conditioned-grain (spd0004) + value-level semantics (spd0003) — the grain-fixed-but-value-failing cells
status: hypothesis
kind: hypothesis
source: spd0004 conclude (validated-not-promoted) — grain-fixed cells (jira/salesforce/pendo) still fail on value-level residuals; grain alone nets only variance-band +2
started:
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
