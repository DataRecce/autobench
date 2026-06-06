---
id: h0029
title: Implementation — reconcile the output column set against the DECLARED set (schema.yml + instruction) as a mechanical set-difference, never against your own judgment of which columns matter
status: hypothesis
kind: hypothesis
source: verification-without-oracle synthesis (_artifacts/verification-without-oracle.md) — width (#2) is a bug class whose deciding fact lives in a DECLARED local artifact (schema.yml / instruction), so it is reachable by an INDEPENDENT check (accounting "footing/cross-footing": the declared set must equal the produced set). Prior width attempts h0011 (worked-example "include the full column set", REJECTED 0/3) and h0023 (Output-Contract deliverable/columns, NO-GO — f1001 convention-bleed) used construct-prose, not a reconciliation against the declared contract. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-06T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

Width failures ("has less columns than `solution__<model>`") happen because the solver
hand-picks a column **subset** it judges relevant, and its own check confirms that subset is
internally consistent — a self-anchored false-green. The deciding fact (which columns the model
must have) is NOT oracle-only: for these tasks it is **declared locally**, in the model's
`schema.yml` entry and/or the task instruction's explicit column list. (airbnb007 flipped under
h0017 precisely because "create the models described in schema.yml" makes schema.yml the
contract.) So width is reachable by an **independent reconciliation** — the same move an
accountant makes when the ledger total must tie out to the sum of its parts: the produced
column set must equal the declared column set, and any difference is a defect, not a judgment
call.

This is the **independent-vs-correlated** distinction from `verification-without-oracle.md`:
h0011 told the solver to "include the full column set" (a construct-prose instruction it could
acknowledge and skip — inert at gpt-5.5/xhigh). This hypothesis instead makes the solver compute
a **mechanical set-difference against a declared external artifact** and fail loud on a nonempty
difference. The anchor (schema.yml / instruction) is external to the solver's own
column-selection reasoning, so it does not share its blind spot.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation instruction — *for each model you author, build the column contract from the
DECLARED set: the columns listed for this model in `schema.yml` (if present) and any columns
named explicitly in the task instruction. Compute the set-difference `declared − produced`; it
must be empty. For every declared column missing from your output, ADD it, deriving its value
from the appropriate source/analog relation (do not drop it because you judge it irrelevant — the
declaration is the contract, not your judgment). Do NOT treat your own chosen subset as
complete* — shipped with a concrete worked-example skeleton (enumerate declared columns; list
produced columns; diff; add the missing ones) — will catch the width false-greens (ana-eng004,
f1002, and the width legs of ana-eng006) and let the solver fix them, raising
`stratified_pass_at_1` above the `@baseline` 0.6458.

This is NOT h0011 re-filed: h0011 was a construct-prose "include all columns" worked-example;
this is an **independent set-difference reconciliation against a declared artifact**, the
verification-without-oracle "footing" import. It is NOT h0023's deliverable-set clause (that
inferred MODELS from installed packages and convention-bled on f1001); this reconciles only the
COLUMN set of a model the solver is already authoring, anchored to that model's own schema.yml
entry — no model-set inference, no package walking.

Method/README change only. Forks `solver_workflows/codex-ade-dbt-minimal` (runtime codex); no
dataset, harness, or solver-runtime change. Leak-guard intact (schema.yml + instruction are
shipped local artifacts; no public fetch, no oracle, no reference to hidden
`AUTO_*`/`solution__*`/`has less columns` verifier text).

## Target datasets

Primary smoke targets (the width cluster, all `ade-bench-` prefixed):

- `ade-bench-ana-eng004` — `AUTO_obt_product_inventory_equality` "has less columns".
- `ade-bench-f1002` — `AUTO_most_podiums_equality` "has less columns".
- `ade-bench-ana-eng006` — width legs (`AUTO_dim_products`, `AUTO_obt_product_inventory`).

This rule fires whenever a model is authored (semi-generative; gated in effect to models that
carry a declared schema.yml/instruction column list, but to be safe treat as generative per G8).
Cross-family regression-canary panel (one `@baseline` passer per non-target family):
`ade-bench-asana001`, `ade-bench-quickbooks002`, `ade-bench-f1001` (the h0009/h0023
convention-bleed tripwire), `ade-bench-airbnb001`. No intercom canary exists (`intercom001/002/003`
all fail @baseline).

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
The README diff vs `codex-ade-dbt-minimal/README.md` touches only `## Stage: Implementation`
(the single column-set reconciliation rule), leaves the other stages and the
dependency/package/leak-guard prose untouched, and references no hidden
`AUTO_*`/`solution__*`/"has less columns" verifier tokens. `agent.kind: spacedock_solver`,
`runtime: codex` preserved.

**AC-2 — G6 independence.** The inserted text reconciles against the DECLARED schema.yml /
instruction set (external), not the solver's own re-run or judgment — not the dead
self-verification family. G7: ships a worked-example set-difference skeleton, not abstract prose.

**AC-3 — Every recorded score is paired with a clean strict audit** (`rk audit --policy strict`,
`tainted: 0`, `captured > 0`).

**Smoke gate:** flip ≥1 of the width targets (the `has less columns` ERROR clears) with **zero**
canary regressions (a canary dropping FAIL is NO-GO regardless of target movement, per the h0009
−3 lesson). Inert-detector: if a target's compile-time column error is unchanged, the rule was
inert.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Gatekeeper review

## Stage Report: propose
