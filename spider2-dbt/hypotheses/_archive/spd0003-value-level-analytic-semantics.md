---
title: Value-level analytic semantics for the hard core (correct table name, wrong columns/values)
status: expanded
kind: concept
id: spd0003
source: commission seed (smoke6-output-contract deep-dive, residual-failure bucket #2)
started: 2026-06-25T06:51:28Z
completed: 2026-06-25T06:51:28Z
verdict: exhausted
archived: 2026-06-25T06:51:28Z
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

## Ideate Stage Report — concept EXHAUSTED (fans to 0 new README hypotheses)

Dispatched ideate. All four candidate forks are already covered by concluded hypotheses, and the
concept's question ("is any value-level slice README-addressable?") is answered **NO**:

| spd0003 fork | tested by | outcome |
|---|---|---|
| Grain discipline | **spd0004** (conditioned-grain) | validated-not-promoted — construct real but variance-swamped; +2 single-draw |
| Multi-table join / cardinality | spd0004 (PRESERVE-COVERAGE/SCOPE classifier) | same — folded into grain |
| Column-completeness (+FK, count-grain, definition-from-project) | **spd0005** §7 | REJECTED — 0 durable flips |
| Self-validation / independent re-derivation | spd0005 §7 | REJECTED — flickered, destabilized 2 canaries |

spd0005's 3-draw hold-rate is decisive: the value-level fixes **flicker (≤1/3)** — variance-dominated,
not durable — and the broad value discipline **regresses stable canaries** (f1001, mrr001). A narrower
single-fork value lever faces the same variance wall (the designed flips already flickered when the
rule was present) and the same oracle ceiling (no gold visible). **Fan-out = 0 viable solver-README
hypotheses.** The concept is exhausted as a README-lever direction.

**Redirect (non-README, higher expected value than any value-level prose lever):**
1. **Verifier false-negative audit** — divvy001's committed SQL reproduced gold with 0 set-difference
   yet scored a binary "mismatch". If a fraction of the "value-def" fails are measurement artifacts,
   the value-level "difficulty" is partly a verifier problem, not a solver one. Capture predicted DBs
   + diff vs gold across the value-def cells; fix/flag the comparator. (Not a hypothesis — infra/audit.)
2. **Grain multi-draw promotion** — spd0004's grain classifier is the one construct-validated lever; a
   ≥3-draw full-board could establish whether its +2 is durable enough to promote `@baseline`.

Marking the concept **expanded** (terminal). @baseline stays 19/61.
