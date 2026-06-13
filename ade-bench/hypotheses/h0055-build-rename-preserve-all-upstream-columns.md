---
id: h0055
title: Build/rename a model — when the task does not enumerate a restricted column set, PRESERVE every upstream column; apply only the named renames/keys, do not narrow to a "relevant" subset
status: propose
kind: hypothesis
source: Captain request 2026-06-13 from _proposal/leverable-flipped-tasks-research-2026-06-13.md (CARD 3, ana-eng003). Method artifact-confirmed 2026-06-13 (h0043 PASS = all 18 stg_customer columns; h0012 FAIL = only 5 columns → AUTO_dim_customer_equality "has less columns than solution"). Forks the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133).
started: 2026-06-13T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`ana-eng003` builds `dim_customer` from `stg_customer` ("rename id→customer_id, make it the
primary key"). It flips on how wide the select is:

- **A (oracle-correct):** carry ALL 18 upstream columns through and apply only the named
  rename/key. The h0043 passing run committed this.
- **B (the failure):** narrow the select to the 5 columns the model judged "relevant"
  (id/company/names/email), dropping the other 13 (job_title, phones, address, city, state,
  zip, country, web_page, notes, attachments) → compile-time `AUTO_dim_customer_equality` "has
  less columns than `solution__dim_customer`". The task never restricted columns; the solver
  over-narrowed. Classification: DROPPED-EXISTING (the columns exist upstream).

**Important contrast — this is the INVERSE of the feature-boundary removal lever (h0045).**
The feature-boundary rule DELETES the columns whose only purpose is a removed feature; this
rule PRESERVES all ordinary upstream columns on a build/rename. The two must be gated so they
do not collide: this rule fires only on BUILD/CREATE/RENAME tasks that do NOT remove/disable a
feature and do NOT enumerate a column subset; the feature-boundary rule fires only on
remove/disable/toggle tasks. The smoke panel carries quickbooks002/003 (feature-removal) as
MUST-HOLD canaries to prove no collision.

**Falsifiable claim (the single README change — Implementation stage only):** adding a
precondition-gated worked-example skeleton — "when building/renaming a model from an upstream
model and the task does not enumerate a restricted column set, preserve every upstream column;
apply only the named renames/keys" — will make the committed `dim_customer.sql` carry the full
column set, flipping `ana-eng003` FAIL→PASS, without regressing the canary panel (especially the
feature-removal canaries, where columns SHOULD be dropped).

**The single proposed README skeleton (generic identifiers, Implementation stage):**

```text
BUILD / RENAME — PRESERVE THE COLUMN SET (gated). When a task asks to BUILD, CREATE, or RENAME
a model from a single upstream model, and it does NOT (a) remove/disable a feature or (b)
enumerate a restricted set of columns to keep, then PRESERVE every column from the upstream
model. Apply only the renames, keys, or casts the task names; carry all other columns through
unchanged. Do not prune the select to the columns you judge "relevant" — a downstream contract
may expect the full set.

(If the task removes/disables a feature, follow the feature-boundary rule above instead — there
you DO drop the feature-only columns.)

BEFORE (narrows to a judged-relevant subset — AVOID on a plain build/rename):
    select id as customer_id, company, last_name, first_name, email
    from {{ ref('upstream') }}

AFTER (preserve all upstream columns; apply only the named rename/key):
    select id as customer_id, company, last_name, first_name, email,
           /* …every remaining upstream column, unchanged… */
    from {{ ref('upstream') }}
```

## Acceptance criteria

**AC-1 — Exactly one README change; specs differ only in `experiment:` + `solver_workflow:`.**
README diff vs the h0052 solver README adds exactly one Implementation-stage gated block (the
build/rename preserve-columns rule); the other four levers, leak-guard, and remaining stages
byte-identical. No `AUTO_*`/`solution__*`/`check_*`/`dim_customer`/`stg_customer`/column-name/
expected-count token; no web-fetch token. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved.

**AC-2 — Every score paired with a clean strict audit** (`tainted: 0`, `coverage_missing: 0`,
`captured > 0`).

**AC-3 — The decisive read is the committed artifact.** Read the committed `dim_customer.sql`
from the ensign `apply_patch`. Classify: does the select carry ALL upstream columns (apply only
the rename/key), or does it narrow to a subset? A flip is credited only when the full column
set lands AND the verifier passes.

**AC-4 — No regression-canary loss, incl. the inverse-construct hold.** All `@baseline` passers
in the smoke panel stay PASS. CRITICAL: the feature-removal canaries `quickbooks002` /
`quickbooks003` must hold PASS on their narrow feature-boundary edits — proving the
preserve-columns rule did not over-fire and prevent the legitimate column DROP. Any canary
regression is a NO-GO unless artifact-proven unrelated variance and the captain accepts the risk.

**AC-5 — Reproducibility judged against the base rate.** ana-eng003 is ~94% at @baseline (a
near-stable passer, low headroom). Smoke runs it as ≥2 seed-perturbed repeats; GO requires the
full-column-set artifact + verifier pass + clean audit on every repeat. The marginal aggregate
value is low; the real win is closing the over-narrowing construct and proving the gate is
collision-free with the feature-boundary lever.

## Target dataset

Primary target: `ade-bench-ana-eng003`.

Smoke panel (target + canaries):
- `ade-bench-ana-eng003` — 🎯 target.
- `ade-bench-quickbooks002` — ✅ MUST-HOLD inverse-construct canary (feature removal — columns
  SHOULD be dropped; proves the preserve-columns rule does not over-fire).
- `ade-bench-quickbooks003` — ✅ MUST-HOLD inverse-construct canary (same feature-removal family).
- `ade-bench-ana-eng001` — ✅ same-family canary.
- `ade-bench-airbnb001`, `ade-bench-asana001`, `ade-bench-f1007` — ✅ cross-family canaries.

GO requires the full-column-set artifact read on ana-eng003 (≥2 repeats) + every canary PASS on
a clean audit, with the quickbooks feature-removal canaries explicitly holding.

## Honest tension with the standing decisions

- **Bleed risk: MODERATE-HIGH.** "Preserve all columns" is the most generative of the three
  card-1/2/3 levers — it could over-fire on a task that legitimately projects a subset, or
  collide with the feature-boundary DROP rule. The gate (build/rename AND not-feature-removal
  AND no-enumerated-subset) plus the quickbooks002/003 MUST-HOLD canaries are the safeguards;
  any over-fire shows up there before full.
- **`trials: 1`.** ana-eng003 is ~94% already; low marginal score. Judge by artifact (AC-3) and
  by the collision-free canary result, not the single reward.

Method/README change only. Forks @baseline h0052 (`solver_workflows/h0052-compose-maxpoints-featureguard-scoped-coverage`, runtime codex); no dataset, harness, or runtime change.
