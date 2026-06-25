---
id: spd0007b
title: Value-def MINUS the oracle-blind id-cast clause (COUNT-by-name keeper + preserve-source-dtype)
status: hypothesis
kind: hypothesis
source: spd0007 conclude follow-up — id-cast clause rejected as oracle-blind (broke tpch002/maturity001); isolate the durable value-def signal
started: 2026-06-25
completed:
verdict:
score: 0.85
worktree:
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

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
