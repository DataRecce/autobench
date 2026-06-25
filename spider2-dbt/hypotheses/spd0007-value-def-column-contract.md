---
id: spd0007
title: Axis-2 G3 — per-column-name VALUE_DEF contract (id-cast / COUNT(*) vs DISTINCT / %-convert / NULL-vs-0 / 2dp-round / key-grain)
status: hypothesis
kind: hypothesis
source: resolution-survey-2026-06-25 ranked-backlog #2; stacks on spd0006's promoted solver
started: 2026-06-25
completed:
verdict:
score: 0.8
worktree:
---

## Hypothesis

A cluster of failures is "right table + right grain, wrong column value/type/sign/null/round."
The prior value-lever (spd0005) was REJECTED because it was a **generative** discipline applied
table-wide. The fix is the opposite: **per-column-name rules, each gated on the exact column
name or a source dtype/discriminator** — the lowest-bleed lever when scoped to a named column.

**The single README change:** add **Axis-2 rule G3** to the classifier (one cohesive
value-contract block), each clause gated on an oracle-free per-column signal:

- identifier column described "the unique identifier" in `schema.yml` while the raw source is
  numeric → CAST to VARCHAR *[divvy001, intercom001 admin_id]*
- count column named `total_*` → `COUNT(*)`; `num_*` → `COUNT(DISTINCT)` (disambiguate by NAME)
  *[retail001]*
- source column carrying `VALUE` + `VALUE_TYPE='percentage'` → convert against the parent base,
  don't pass raw *[recharge001]*
- metric over a high-NULL-fraction field → NULL-preserving `count_if`, while categorical bucket
  tallies `coalesce`-to-0 *[f1002]*
- `ROUND(money, 2)` only where gold is clean — never table-wide (tpch001 keeps raw `return_total`)
- group by the timestamp grain the KEY embeds, even when the prompt says "daily" *[asset001]*

**Target tasks (REACHABLE_VERIFIED):** f1002, divvy001, recharge001, retail001, tpch001,
twilio001, asset001.

## Pre-smoke Decision-Fork Probe

Offline-verified (survey wf_32b5a457-a96): each target reconstructed from source with the named
rule applied passed the real `duckdb_match.py`. E.g. retail001 `total_invoices = COUNT(*)`
(354321) matched gold vs the baseline's `COUNT(DISTINCT)` (16646); twilio001 sign convention per
overview table matched. Reachability proven; smoke tests whether the solver applies the
**named-column** rule. **Watch:** a blanket "round all money / cast all ids / count(*) not
distinct" is net-negative — every clause MUST stay keyed to the column name.

## Acceptance criteria

**AC-1** — only the README changes; full spec diff = `experiment:` + `solver_workflow:` only.
**AC-2** — every score paired with a clean strict audit.
**AC-3** — verdict from paired `rk runs diff` vs `@baseline` (the spd0006 champion), attributed
by the committed SQL showing the named-column rule fired; GO requires ≥1 target flip by artifact
+ 0 regression, especially the dual `num_*`/`total_*` family.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
