---
title: Value-level analytic semantics for the hard core (correct table name, wrong columns/values)
status: concept
kind: concept
id: spd0003
source: commission seed (smoke6-output-contract deep-dive, residual-failure bucket #2)
started:
completed:
verdict:
---

## Direction

After the naming + materialization levers (spd0002), the residual spider2-dbt failures cluster into a
single hard core: **the solver builds the correctly-named target table but the columns / grain /
values are wrong.** Smoke#2 showed this on jira001 (`jira__project_enhanced` built, value mismatch),
tpch001 (`client_purchase_status`, value mismatch), and xero_new001 (all three `xero__*` reports built,
value mismatch). These are the genuine analytic difficulty of a text-to-dbt benchmark — exact
multi-table transformation semantics under column-containment grading — and the smoke docs flagged
them as "no cheap README lever."

This concept asks: **is any slice of the value-level failure README-addressable?** Candidate forks to
`ideate` into one-change hypotheses (each falsifiable, each naming target tasks):

- **Grain discipline** — a rule forcing the solver to state and verify the output grain (one row per
  what?) before writing the model, addressing rows-too-coarse / too-fine mismatches.
- **Column-completeness** — a rule to enumerate every column the instruction implies and check each
  appears, addressing missing-column (containment) failures distinct from wrong-value failures.
- **Multi-table join semantics** — a rule about preserving cardinality across joins (the ade-bench
  per-key inner-join / grain-spine family lessons may transfer).
- **Self-validation against the instruction, not the build** — the recurring self-anchored false-green:
  the agent reports "0 mismatches" against its own interpretation. A rule that forces an independent
  re-derivation of at least one target value may catch this — but beware the oracle problem (no gold is
  visible), so this is a *redundancy* check, not a correctness check.

Expected ceiling is low — this is hard benchmark difficulty, not a wiring gap. A useful early move
before investing heavily is to **size the hard core**: how many of the 61 tasks are "right name, wrong
values" vs other classes, from the spd0001 anchor's per-task ledger (`_artifacts/task-gap-ranking.md`).
That number bounds the headroom these levers could ever reach.

`ideate` should produce 2–4 hypotheses from the forks above, ordered by how much of the hard core each
could plausibly move (per the task-gap ranking), and each scoped so its smoke set names a concrete
currently-FAIL target plus perturbable passing canaries.
