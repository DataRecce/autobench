---
id: h0057
title: Two-move composition on @baseline h0056 — (A) generalize the build/rename preserve-columns gate to multi-upstream OBT/join models so ana-eng004 flips; (B) sharpen the feature-boundary removal rule with a worked example (drop the feature-only column, KEEP the shared base id) to lock quickbooks002/003 against the over-drop coin-flip
status: hypothesis
kind: hypothesis
source: Captain request 2026-06-14 from the h0056 two-draw analysis (r1=32/r2=35; the r1 shortfall = f1001+qb002+qb003 coin-flips). Forks the current @baseline h0056 (runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a, 35/48). Both moves artifact-grounded — Move A: ana-eng004 forensic = same dropped-column construct as the banked ana-eng003 (build OBT from fact⋈dim, solution = all 22 cols, hist 0/23). Move B: qb002/qb003 r1-vs-r2 forensic = OVER-DROP of the base department_id column; correct boundary (drop department_name, keep department_id) is cleanly expressible.
started: 2026-06-14T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

@baseline h0056 sits at 35/48 on its r2 draw, but the two-draw analysis shows 35 is a *lucky*
draw: r1 drew 32, and the gap is three un-locked coin-flip cells (f1001, quickbooks002,
quickbooks003) that happened to land PASS in r2. This hypothesis makes two precondition-gated
edits to the h0056 README — one to FLIP a stable-FAIL cell (+1 → 36), one to STABILIZE the two
biggest regression risks so the 36 survives a re-draw.

### Move A (flip) — generalize the build/rename preserve-columns gate to multi-upstream models

`ana-eng004` builds `obt_product_inventory` ("add product details to every inventory item") by
joining `fact_inventory` ⋈ `dim_products`; the solution is effectively `SELECT *` (22 columns).
The solver prunes to a "relevant" subset → "has less columns than solution__obt_product_inventory".
This is the **identical dropped-existing-columns construct** that the banked h0055 lever fixed on
ana-eng003 (hist: ana-eng004 0/23 — never passed). The h0055 rule does NOT fire today because its
precondition says "from **a single upstream model**" — ana-eng004 builds from a **join of two**.
Move A widens that precondition to cover one-or-more upstream models (an OBT/wide-table join of a
fact and a dimension), so the existing preserve-columns rule fires. This is the same
generalization pattern h0053 showed (airbnb005 → airbnb007).

### Move B (stabilize) — sharpen the feature-boundary removal rule with a worked example

`quickbooks002`/`quickbooks003` remove the `using_department` feature. The correct edit drops the
feature-only derived column `department_name` but KEEPS the shared base column `department_id`
(other logic uses it; the solution retains it). In h0056 r1 the solver OVER-DROPPED — it scrubbed
`department_id` too → "has less columns than solution" → both regressed; in r2 it kept it → both
passed. A pure coin-flip on the removal boundary, and it was the cause of r1's shortfall. The
existing h0045 rule already says "preserve ordinary raw/source attributes…" in **prose but carries
no worked example**. Move B adds a before→after skeleton to the h0045 block making the boundary
concrete: drop the feature-only derived column, KEEP the shared base id/foreign-key column.

**Falsifiable claim (two scoped README edits — Implementation stage only):**
- (A) generalizing the preserve-columns precondition to multi-upstream OBT/join builds will make
  the committed `obt_product_inventory.sql` carry the full column set, flipping `ana-eng004`
  FAIL→PASS;
- (B) adding the drop-feature-col-keep-base-id worked example to the feature-boundary rule will
  keep `quickbooks002`/`quickbooks003` PASS on their narrow feature-removal edit (department_id
  retained), reducing their PASS→FAIL coin-flip rate;
- with NO interference: ana-eng003 still flips (h0055 base case), airbnb005/airbnb007 still flip
  (h0053), airbnb009/f1006/f1006-hard/f1010-medium still hold, and the two collision dual-pairs
  (h0050↔h0053, h0045↔h0055) still hold their correct sides.

**The two proposed README edits (generic identifiers, Implementation stage):**

Move A — EDIT the existing "BUILD / RENAME — PRESERVE THE COLUMN SET" block's precondition:

```text
... When a task asks to BUILD, CREATE, or RENAME a model from ONE OR MORE upstream models
— including a wide/one-big-table (OBT) build that JOINS a fact to one or more dimensions —
and it does NOT (a) remove/disable a feature or (b) enumerate a restricted set of columns to
keep, then PRESERVE every column from ALL the joined upstream models. Apply only the renames,
keys, casts, or the join itself the task names; carry all other upstream columns through
unchanged. Do not prune the select to the columns you judge "relevant" — a downstream contract
(and OBT consumers) may expect the full set.

BEFORE (OBT build that prunes to a judged-relevant subset — AVOID):
    select f.inventory_id, p.product_name, f.quantity
    from {{ ref('fact_table') }} f left join {{ ref('dim_table') }} p using (key)

AFTER (preserve all columns from BOTH upstreams; apply only the join the task asks for):
    select f.*, p.*            -- or every column of f and p listed explicitly, unchanged
    from {{ ref('fact_table') }} f left join {{ ref('dim_table') }} p using (key)
```

Move B — ADD a worked example to the existing feature-boundary removal block:

```text
(worked example for "remove the config/variable … Preserve ordinary raw/source attributes …")
When removing a feature, drop the feature-ONLY derived column and its conditional join, but KEEP
the shared base id / foreign-key column that the rest of the project uses.

BEFORE (using_feature enabled):
    select t.entity_id,
           t.feature_fk_id,                         -- BASE column from the source/transaction
           {% if var('using_feature', True) %}
           dim.feature_label as feature_name,       -- FEATURE-ONLY derived column
           {% endif %}
    from t {% if var('using_feature', True) %} left join dim on dim.id = t.feature_fk_id {% endif %}

AFTER (remove the feature — keep the base fk, drop only the feature-only column + its join):
    select t.entity_id,
           t.feature_fk_id                          -- KEEP: shared base column (solution retains it)
    from t                                          -- DROPPED: the conditional join + feature_name
```

## Acceptance criteria

**AC-1 — Exactly two scoped README edits; spec differs only in `experiment:` + `solver_workflow:`.**
README diff vs the h0056 solver README = (A) the preserve-columns block's precondition+skeleton
widened to multi-upstream OBT/join, and (B) a worked example added inside the existing
feature-boundary removal block. No NEW stage/rule beyond these two; the other five levers,
leak-guard, and the remaining stages byte-identical. No `AUTO_*`/`solution__*`/`check_*`/
`obt_product_inventory`/`department_id`/`department_name`/expected-count token; no web-fetch
token. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved.
(NOTE for the gatekeeper: unlike h0052/h0056 this is NOT "add N verbatim blocks" — it MODIFIES
two existing blocks. G1/G6 must judge the two scoped edits, both inside `## Stage: Implementation`,
as one coherent two-move change.)

**AC-2 — Every score paired with a clean strict audit** (`tainted: 0`, `coverage_missing: 0`,
`captured > 0`).

**AC-3 — Decisive per-cell committed-artifact reads (not chatter):**
- ana-eng004 (Move A flip): committed `obt_product_inventory.sql` carries the full upstream column
  set from the fact⋈dim join (no pruned subset) AND the verifier passes.
- quickbooks002 + quickbooks003 (Move B stabilize): committed unions/transactions DROP
  `department_name` (+ its conditional join) but KEEP `department_id`; "less columns" error absent.
- Regression holds, committed-shape confirmed: ana-eng003 (all upstream cols), airbnb005/airbnb007
  (inner-join-from-fact), airbnb009 (coverage predicate dropped), f1006/f1006-hard (`max(points)`),
  f1010-medium (exclude-pit), quickbooks004 (narrow toggle).

**AC-4 — No collision; no same-construct regression.** Both dual-pairs hold their correct sides:
h0050↔h0053 (airbnb009 coverage vs airbnb005 inner-join), h0045↔h0055 (feature-removal DROP vs
build PRESERVE). CRITICAL Move-A safety: the widened preserve-columns precondition must NOT fire on
a feature-removal task (qb002/qb003 must still DROP the feature column) — the widening adds "join"
to the build-direction gate, it does not touch the "not-feature-removal" guard. A collision or a
same-construct regression is a NO-GO.

**AC-5 — Judged on a two-draw expectation + committed artifacts (the h0052/h0056 precedent), read
through the ~±3-cell trials:1 noise floor.** Run ≥2 independent seed-perturbed full draws. GO basis:
ana-eng004 flips on the committed full-column artifact in ≥1 draw with no collision, qb002/qb003
hold their keep-department_id artifact, and the two-draw mean clears h0056's expectation (~33.5).
HONEST: f1011 (oracle MC, ~33%) props up r2's 35 and is NOT lockable — it is expected to wobble;
the durable margin must come from the Move-A flip + the Move-B stabilization, not from f1011.

## Target dataset

- `ade-bench-ana-eng004` — 🎯 Move A flip target (hist 0/23, stable-FAIL; same construct as banked
  ana-eng003).
- `ade-bench-quickbooks002`, `ade-bench-quickbooks003` — 🎯 Move B stabilize targets + h0045↔h0055
  collision canaries (must DROP department_name, KEEP department_id).
- `ade-bench-ana-eng003` — ✅ MUST-HOLD (h0055 base case; the widened precondition must not break it).
- `ade-bench-ana-eng006`, `ade-bench-ana-eng007`, `ade-bench-ana-eng007-medium` — ✅ opportunistic
  generalization watch (the widened rule MAY flip ana-eng007/-medium; ana-eng006 has mixed
  failure modes — missing derived col + dedup — so it is NOT expected to flip, only to not regress).
- `ade-bench-airbnb005`, `ade-bench-airbnb009` — ✅ h0053/h0050 collision-pair holds.
- `ade-bench-f1010-medium`, `ade-bench-f1006`, `ade-bench-quickbooks004` — ✅ banked-lever holds.
- `ade-bench-asana001`, `ade-bench-f1007` — ✅ cross-family canaries.

GO requires the ana-eng004 full-column flip artifact (≥1 of ≥2 draws) + qb002/qb003 holding their
keep-department_id artifact + ana-eng003 still flipping + every collision pair holding, on a clean
audit, with the two-draw mean clearing ~33.5.

## Honest tension with the standing decisions

- **Two edits modify existing blocks (not pure additive compose).** Move A widens a precondition;
  Move B adds a worked example inside an existing block. Both are inside Implementation and are one
  coherent "tighten what's already there" change — but the gatekeeper G1/G6 must read it as scoped
  edits, not a from-scratch lever (see AC-1 note).
- **Move A bleed risk: LOW-MODERATE.** Widening "single upstream" → "one or more / join" is more
  generative; the not-feature-removal guard + the qb002/qb003 MUST-HOLD canaries are the tripwire.
- **Move B is a stabilizer, not a flip.** It does not add a pass; it lowers the qb002/qb003 PASS→FAIL
  rate. Its value is a more reproducible baseline, judged across the two draws, not a single net.
- **`trials: 1`.** ana-eng004 is 0/23 (a genuine flip, not a coin-flip), so a single clean draw with
  the full-column artifact is strong; qb002/qb003 are coin-flips, so judge their stabilization by the
  committed keep-department_id artifact, not one reward.

Method/README change only. Forks @baseline h0056 (`solver_workflows/h0056-compose-six-levers-on-h0052`, runtime codex); no dataset, harness, or runtime change.
