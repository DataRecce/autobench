---
id: h0057
title: Two-move composition on @baseline h0056 — (A) generalize the build/rename preserve-columns gate to multi-upstream OBT/join models so ana-eng004 flips; (B) sharpen the feature-boundary removal rule with a worked example (drop the feature-only column, KEEP the shared base id) to lock quickbooks002/003 against the over-drop coin-flip
status: smoke
kind: hypothesis
source: "Captain request 2026-06-14 from the h0056 two-draw analysis (r1=32/r2=35; the r1 shortfall = f1001+qb002+qb003 coin-flips). Forks the current @baseline h0056 (runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a, 35/48). Both moves artifact-grounded — Move A: ana-eng004 forensic = same dropped-column construct as the banked ana-eng003 (build OBT from fact-join-dim, solution = all 22 cols, hist 0/23). Move B: qb002/qb003 r1-vs-r2 forensic = OVER-DROP of the base department_id column; correct boundary (drop department_name, keep department_id) is cleanly expressible."
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

## Gatekeeper review

**Recommendation: APPROVE** — clean two-move scoped edit confined to `## Stage: Implementation`; both integrity rules (G2/G3/G6) PASS, leak-guard byte-identical, full preserve-columns skeleton present, strong canary panel with the qb002/qb003 bleed tripwire in place. Only advisory WARNs (G8/G11) remain.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-14T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff = two hunks only: Move-B insert at parent L67→child L68-83 and Move-A replace at parent L81-97→child L97-113. Both fall strictly inside `## Stage: Implementation`. No other stage, no leak-guard/dependency prose touched. Per AC-1 note, the two scoped edits judged as ONE coherent two-move change. |
| G2 leak-guard intact | PASS | Leak-guard region (README L1-33) IDENTICAL to parent. Forbidden-oracle grep (`AUTO_`/`solution__`/`check_`/`obt_product_inventory`/`department_id`/`department_name`/expected-count): NONE. `curl`/`wget`/`git clone` only at L9-10 = the unchanged PROHIBITION prose. Not-feature-removal guard sentence KEPT INTACT at child L104. |
| G3 spec two fields | PASS | `diff baseline.yaml h0057.yaml` = exactly `experiment:` (L2) and `solver_workflow:` (L11). `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | Smoke diff = only an added `benchmark.tasks:` block (14 tasks, all `ade-bench-` prefixed). Both targets present: ana-eng004 + quickbooks002/003. Regression sentinels present. Nothing else differs. |
| G5 both frozen | PASS | Both frozen files exist; both carry `kind: spacedock_solver`, `runtime: codex`, `trials: 1`. |
| G6 resolver fidelity | PASS | Fork parent = h0056 (`source:` and registry agree). Move A widens "single upstream"→"ONE OR MORE … OBT JOIN … PRESERVE every column from ALL", BEFORE/AFTER `select f.*, p.*`. Move B adds drop-feature-col/keep-base-id worked example. Both generative-authoring/build guidance — NOT self-anchored; no dead-family phrasings; no scope creep. |
| G7 actionability/inert-risk | PASS | Move A carries a copyable BEFORE/AFTER SQL skeleton (the PASS few-shot form); Move B is itself a BEFORE/AFTER worked example. Generalizes a *banked* preserve-columns lever (h0055 flipped ana-eng003), inheriting a demonstrated-actionable mechanism. |
| G8 regression-canary coverage | WARN | Generative (build/rename incl. join, fires broadly). Panel has cross-family canaries asana001, f1007 + same-construct perturbable canaries ana-eng003, airbnb005, and the Move-A BLEED TRIPWIRE qb002/qb003. WARN: no intercom canary, and only one airbnb perturbable canary (005) for the join-build construct — a different airbnb build passer could regress unseen. Not FAIL: ≥1 non-target passer from each touchable family present. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol. |
| G10 self-correcting false-positive | N/A | Neither move is a check/reconcile/validate-and-fix lever; both are generative authoring guidance. |
| G11 multi-model-target risk | WARN (unverifiable) | Taxonomy + dataset verifier sets not statically readable; ana-eng004/qb002/qb003 scored-model counts unconfirmed. If any target is multi-model, treat a single-run flip on the unaddressed model as variance and judge by the committed artifact on every scored model (airbnb007/h0034 lesson). |
| G12 decision-fork probe quality | N/A | Not a flipped-task follow-up; two-draw forensic on a promoted baseline, grounded in committed-artifact forensics, no subagent-count overclaim. |

**For the captain:** APPROVE — clean scoped two-move modify-in-place edit, both hunks inside Implementation, leak-guard byte-identical, integrity rules all PASS, Move-A bleed tripwire (qb002/qb003 must still DROP department_name / KEEP department_id) seated in the smoke panel. Two advisory WARNs at smoke: (G8) widened preserve-columns is more generative — confirm at full no non-target airbnb/f1 build passer regresses (only airbnb005 covers the join-build construct; no intercom canary); (G11) ana-eng004/qb002/qb003 scored-model counts unverified — if multi-model, credit by committed artifact on every scored model. Per AC-5 judge over ≥2 draws against ~33.5; read Move-B stabilization by the keep-department_id artifact, not a single reward.

## Stage Report: propose

- DONE: Move A + Move B applied to the forked @baseline h0056 README per the EXACT edit text in the hypothesis body
  Forked `solver_workflows/h0057-aneng-obt-preserve-columns-and-feature-drop-keep-base-id/`; Move A replaced the BUILD/RENAME preserve-columns precondition + BEFORE/AFTER skeleton with the multi-upstream/OBT-join version (kept the not-feature-removal guard intact); Move B inserted the drop-feature-col-keep-base-id worked example after the "Preserve ordinary raw/source attributes…" paragraph.
- DONE: AC-1 verified — `diff h0056/README.md h0057/README.md` = exactly the two scoped edits, both inside `## Stage: Implementation`
  Diff shows only the Move-A precondition+skeleton replacement and the Move-B worked-example insertion; the other five levers + leak-guard prose + all other stages byte-identical; oracle-token grep (AUTO_*/solution__*/check_*/obt_product_inventory/department_id/department_name/expected-count) returned 0; curl/wget hits are the unchanged leak-guard prohibition prose.
- DONE: Full spec differs from baseline.yaml ONLY in `experiment:` + `solver_workflow:`; smoke spec adds the `## Target dataset` panel; both frozen
  `diff baseline.yaml h0057.yaml` = exactly 2 lines; smoke adds a 14-task `benchmark.tasks` block (ana-eng004 flip; qb002/003 stabilize+collision; ana-eng003 must-hold; ana-eng006/007/007-medium watch; airbnb005/009 + f1010-medium/f1006/quickbooks004 holds; asana001/f1007 canaries). Both frozen via `rk freeze --allow-missing`.
- DONE: Gatekeeper run; `## Gatekeeper review` block written with per-rule PASS/WARN/FAIL table + overall recommendation
  Recommendation APPROVE; G1/G6 judged the two scoped edits as one coherent two-move MODIFY-existing-blocks change; G8 confirmed the smoke panel + Move-A bleed tripwire (qb002/qb003); no FAILs, two advisory WARNs (G8 canary breadth, G11 unverifiable scored-model counts).

### Summary
Forked @baseline h0056 to h0057 and applied the two scoped in-place README edits (Move A: widen preserve-columns precondition to multi-upstream/OBT joins; Move B: add the drop-feature-col-keep-base-id worked example to the feature-removal block), both inside `## Stage: Implementation`. AC-1 verified: README diff = exactly those two edits, everything else byte-identical, no leaked oracle tokens; full spec differs only in the two allowed fields; smoke spec carries the 14-task target+canary panel; both specs frozen. Gatekeeper recommends APPROVE with two advisory WARNs (G8 canary breadth for the join-build construct / no intercom canary; G11 unverifiable scored-model counts for the three targets).

## Smoke result

**Headline: NO-GO.** Zero flips (ana-eng004 MISSED) and one regression (asana001 PASS@baseline → FAIL).
Move B held (qb002/qb003 both PASS). 9/14 PASS (stratified pass@1 = 0.643). Run complete rc=0,
14 cells, audit clean (14/14 `clean`, 0 findings), `captured = 1` on every cell.

- Smoke run-dir: `runs/ade-bench-h0057-aneng-obt-preserve-columns-and-feature-drop-keep-base-id/0d63e37e05bae208` (rc=0).
- @baseline = h0056 r2: `runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a`.

| Task | @baseline (h0056 r2) | h0057 smoke | Role | Verdict | Distance / why |
|------|----------------------|-------------|------|---------|----------------|
| ana-eng004 | FAIL (0/23 hist) | **FAIL** | 🎯 Move A flip | MISSED | committed obt = 22 cols; verifier wants 23 ("less columns"). Move A FIRED + reached the SQL (full fact⋈dim join, `attachments` PRESENT) but worker collapsed the duplicate join key — kept `i.product_id`, dropped `p.product_id` → 22 not 23 |
| quickbooks002 | PASS | **PASS** | 🎯 Move B stabilize | HELD | kept department base id; no "less columns" error |
| quickbooks003 | PASS | **PASS** | 🎯 Move B stabilize | HELD | kept department base id; no "less columns" error |
| ana-eng003 | PASS | PASS | ✅ h0055 base case | HELD | widened precondition did not break it |
| airbnb005 | PASS | PASS | ✅ h0053 collision pair | HELD | — |
| airbnb009 | PASS | PASS | ✅ h0050 collision pair | HELD | — |
| f1006 | PASS | PASS | ✅ banked max(points) | HELD | — |
| f1010-medium | PASS | PASS | ✅ banked exclude-pit | HELD | — |
| f1007 | PASS | PASS | ✅ cross-family canary | HELD | — |
| quickbooks004 | PASS | PASS | ✅ banked narrow toggle | HELD | — |
| asana001 | **PASS** (stable r1+r2) | **FAIL** | ✅ cross-family canary | **REGRESSION** | committed asana__task.sql gated `tags`/`number_of_tags` behind `{% if var('asana__using_tags') and var('asana__using_task_tags') %}` → vars resolved disabled → dropped 2 cols → "less columns" |
| ana-eng006 | FAIL | FAIL | ✅ watch (not expected to flip) | held FAIL | baseline-FAIL, mixed failure modes — NOT a regression |
| ana-eng007 | FAIL | FAIL | ✅ opportunistic watch | held FAIL | baseline-FAIL — NOT a regression |
| ana-eng007-medium | FAIL | FAIL | ✅ opportunistic watch | held FAIL | baseline-FAIL — NOT a regression |

Audit/capture: `rk audit --policy strict` → all 14 `clean`, 0 findings; `captured = 1` on every cell.
ana-eng006/007/007-medium were baseline-FAIL (not regressions); the widened Move-A rule did NOT
opportunistically flip them.

## Behavioral analysis

### ana-eng004 (Move A flip target — MISSED) — incomplete-artifact / wrong-construct in the pre-diagnosis
Committed `models/analytics_obt/obt_product_inventory.sql` (from the worker-session apply_patch,
`rollout-…019ec4ef…jsonl`):
```
SELECT i.inventory_id, i.transaction_type, i.transaction_created_date, i.transaction_modified_date,
       i.product_id, i.quantity, i.purchase_order_id, i.customer_order_id, i.comments,        -- 9 from fact_inventory
       p.product_code, p.product_name, p.description, p.supplier_company, p.standard_cost,
       p.list_price, p.reorder_level, p.target_level, p.quantity_per_unit, p.discontinued,
       p.minimum_reorder_quantity, p.category, p.attachments                                  -- 13 from dim_products
FROM {{ ref('fact_inventory') }} i LEFT JOIN {{ ref('dim_products') }} p ON p.product_id = i.product_id
```
= **22 columns**; verifier wants **23**.

**Move A FIRED and reached the committed artifact** — the worker built the full fact⋈dim OBT, used a
`SELECT`-style carry-through (no "judged-relevant" prune), and `p.attachments` IS present (so the
dispatch's pre-diagnosis that `attachments` was dropped is WRONG for this draw). The actual miss: the
worker collapsed the **duplicate join key** — it kept `i.product_id` but dropped `p.product_id` from
dim_products. `fact_inventory` = 9 cols, `dim_products` = 14 cols (`product_id` + the 13 carried
`product_code…attachments`); the solution keeps **both** product_id columns → 9 + 14 = 23. The worker
kept 9 + 13 = 22 because de-duplicating the join key felt natural. Move A's BEFORE/AFTER skeleton
(`select f.*, p.*`) says "preserve every column from ALL upstreams" but has no teeth to force an
explicit **upstream-vs-output column AUDIT** — the worker read "preserve" as "carry the obvious union",
silently dropping the second copy of the join key. Classify: incomplete-artifact (one short, audit-miss
on the duplicate-key column).

### asana001 (the REGRESSION) — decisive bleed-vs-variance forensic
1. **h0057 committed edit (FAIL).** Worker edited 4 files: `dbt_project.yml`, `int_asana__task_tags.sql`,
   `asana__tag.sql`, **and `asana__task.sql`**. The `asana__task.sql` hunk wraps the `tags` and
   `coalesce(...number_of_tags...)` select columns AND the `left join task_tags` behind
   `{% set using_tags = var('asana__using_tags', True) and var('asana__using_task_tags', True) %}` /
   `{% if using_tags %}`. At verifier time those vars resolved to a disabled state → the 2 tags columns
   were dropped from asana__task → `"asana__task has less columns than solution__asana__task"`.
2. **h0056 r2 committed edit (PASS).** Worker edited ONLY `int_asana__task_tags.sql` and `asana__tag.sql`
   — it did **NOT touch `asana__task.sql` at all**. The fix lived entirely upstream (tags intermediate +
   tag model), so asana__task kept its `tags`/`number_of_tags` columns intact → 23 cols → PASS.
   The drop is exactly the columns h0057 additionally gated in asana__task that h0056 r2 left alone.
3. **What rule shaped the drop?** The worker's reasoning is overwhelmingly the **h0043 package-migration /
   optional-resource gating** lever (keyword counts in the reasoning text: package×82, disable×26,
   optional×17, using_tags/using_task_tags×8 each), with the explicit diagnostic: *"first classify package
   vars and optional-resource behavior. If a downstream model unconditionally refs a package resource that
   can be disabled by an existing package var, prefer a package-migration compatibility diagnostic and
   repair."* The worker validated with `--vars '{asana__using_tags: true, asana__using_task_tags: true}'`
   (compiles PASS) — a self-anchored false-green. The h0057-NEW phrasings (feature-only, shared base id,
   preserve all, PRESERVE every column, feature boundary) DO appear in the text, but **every occurrence is
   inside the README BEFORE/AFTER skeletons echoed in the prompt** — none appears in the worker's own
   reasoning shaping the asana__task gate. Move A says PRESERVE all columns (the *opposite* of what the
   worker did); Move B's worked example is a feature-removal task with a derived column + conditional join,
   and the worker did not cite it to motivate gating `tags`. The h0057 README diff left the h0043 package
   rule **byte-identical**.
4. **VERDICT: `variance-unclear`** (off-construct, asana package-migration coin-flip). The committed edit is
   pure h0043 optional-resource gating; the two NEW h0057 edits are ABSENT from the shaping. asana001 admits
   multiple column outcomes — fix tags upstream-only (h0056 r2 → PASS) vs additionally gate them in
   asana__task with a var that resolves disabled (h0057 → FAIL). This is a same-rule, different-draw outcome
   on a byte-identical package rule = variance, NOT h0057 interference. (Caveat per the dispatch: asana001
   was stably PASS in BOTH h0056 draws, so this is a noticeable wobble — but the committed-artifact + reasoning
   forensic shows no Move-A/Move-B firing, so it is not classifiable as a bleed.)

## Failure Review

Primary classification per failure:

- **ana-eng004 = incomplete-artifact.** Move A fired and reached the committed SQL (full fact⋈dim OBT,
  no relevance-prune, `attachments` present), but the worker collapsed the duplicate join key — kept
  `i.product_id`, dropped `p.product_id` → 22 cols vs the solution's 23. The pre-diagnosis (attachments
  omitted) was wrong for this draw; the real one-column miss is the second copy of the join key. Move A
  lacks teeth to force an explicit upstream-vs-output column audit.
- **asana001 = variance-unclear.** Committed asana__task.sql gates `tags`/`number_of_tags` behind a
  package var (`asana__using_tags`/`asana__using_task_tags`) that resolved disabled → "less columns".
  Pure h0043 package-migration optional-resource gating; the two NEW h0057 edits did not fire (all
  Move-A/Move-B tokens are README prose echoed in the prompt). h0056 r2 PASSED by fixing tags upstream
  only and never touching asana__task. Byte-identical package rule → same-rule different-draw = variance.

Failure-review questions:
1. **Original hypothesized fork.** Move A: widening the preserve-columns precondition to multi-upstream
   OBT/join builds makes the committed obt_product_inventory.sql carry the full column set → ana-eng004
   FAIL→PASS. Move B: the keep-base-id worked example holds qb002/qb003.
2. **Fork the committed artifact revealed.** Move A DID change the artifact (full join, no prune) but the
   real fork is one layer deeper: an OBT that joins on a key shared by both upstreams must keep BOTH
   copies of the key column (the solution does); "preserve every column" without an explicit upstream-vs-
   output column count lets the worker silently de-dup the join key and land one short. For asana001 the
   fork is unchanged-h0043 package gating with a self-anchored `--vars true` false-green, plus the asana
   package admitting an upstream-only vs asana__task-gated repair (the coin-flip).
3. **Did the README rule fire, where is the evidence?** Move A: YES — committed obt SQL is the full
   fact⋈dim join (worker-session apply_patch). Move B: YES (held) — qb002/qb003 kept the department base
   id, no "less columns". asana001: the NEW rules did NOT fire — only the byte-identical h0043 package
   rule shaped the asana__task gate (reasoning keyword forensic).
4. **New fork to test next.** REVISE Move A with an explicit upstream-column-AUDIT step that forces a
   count: list each upstream model's FULL column set, confirm every column (INCLUDING a join key that
   exists in more than one upstream — keep both copies unless the task says otherwise) appears in the
   output, and diff against the upstream rather than trusting an existing or "natural" SELECT.
5. **Next step:** `file` — REVISE Move A (smoke → hypothesis), re-smoke. Move B needs no change. asana001
   is variance, not a bleed, so it does not block a re-smoke; but it is a live reminder that the asana
   package family is a coin-flip and should stay in the canary panel.

## Follow-up Routing

**Route: smoke → hypothesis (REVISE Move A), then re-smoke (hypothesis → propose → smoke).**

- **REVISE Move A — add an upstream-column-AUDIT step.** Before finalizing a BUILD/RENAME, the rule must
  force: *"list each upstream model's full column set and confirm every column appears in your output. An
  existing model may have pre-pruned columns — diff against the upstream and add any missing; do not trust
  the current SELECT. When two upstreams share a join-key column, KEEP BOTH copies (qualify them) unless
  the task says to collapse them — the solution's wide table retains the duplicate key."* This directly
  attacks the ana-eng004 miss (22 vs 23 = the dropped second `product_id`). The existing
  `select f.*, p.*` skeleton already implies both copies; make the audit step explicit so the worker
  counts rather than carrying the "natural" de-duplicated union.
- **Move B: no change.** It held (qb002/qb003 PASS, department base id kept). Do NOT scope it to asana001
  — asana001 was variance (off-construct package gating), not a Move-B bleed.
- **Recommendation: re-smoke after the Move-A revision** (it is artifact-grounded: Move A demonstrably
  reaches the SQL and is one column short for a nameable, fixable reason). NOT conclude — the lever is not
  inert; it is under-specified by exactly one audit step. Keep asana001 + f1007 as cross-family canaries
  and add a second asana canary if breadth allows (the package family is a known coin-flip).

## Stage Report: smoke

- DONE: `rk run --explain` sanity-checked on specs/h0057-...smoke.frozen.yaml (confirms the 14-task panel + solver resolve) before the real launch.
  Explain exit 0: Tasks=14, Concurrency=1, Solver workflow=solver_workflows/h0057-aneng-obt-preserve-columns-and-feature-drop-keep-base-id, README found=True (RAZORBACK_SPACEDOCK_PLUGIN_DIR=/home/kent/autobench/spacedock).
- DONE: Smoke run launched DETACHED via drivers/rk-run-detached.sh (key h0057-smoke, the smoke.frozen.yaml spec, mode run); handle dir returned with pid + log; ensign returns immediately, FO owns the sentinel scan.
  Handle: /home/kent/autobench/ade-bench/runs/.rk-handles/h0057-smoke-20260614-065900/ ; pid 3151900 ; log runs/.rk-handles/h0057-smoke-20260614-065900/log ; ntfy adebench-rk-381c976fe07465bf.
- DONE: Handle confirmed live (pid alive + rk run child process spawned) before returning; the exact handle-dir absolute path reported.
  Process tree alive: 3151900 (worker) → 3151915 (uv rk run) → 3151918 (rk python) → 3152038 (harbor run); `done` sentinel absent (run in flight).

### Summary
Ran the foreground `--explain` sanity check (exit 0; 14-task panel, concurrency 1, h0057 solver_workflow + README all resolve), then launched the smoke run detached via drivers/rk-run-detached.sh under key h0057-smoke. Confirmed the handle live — full process tree from worker pid 3151900 down to harbor run 3152038, `done` sentinel absent. Returned immediately without waiting; the FO owns the sentinel scan and the ~2 hr run is in flight.

## Stage Report: smoke (cycle 2 — post-run analysis)

- DONE: `## Smoke result` written: full 14-task panel vs @baseline (h0056 r2) with per-target flip/distance/why; headline NO-GO (zero flips — ana-eng004 missed; one regression — asana001). Move B held (qb002/qb003 PASS). ana-eng006/007/007-medium stayed FAIL (baseline-FAIL, not regressions). Audit clean (14/14), captured=1 every cell.
  Run-dir 0d63e37e05bae208, rc=0; `rk audit --policy strict` → all clean / 0 findings; `rk score` → stratified pass@1 0.643 (9/14); per-cell reward.txt + subagent-trace-manifest captured read.
- DONE: asana001 BLEED-vs-VARIANCE verdict from committed artifacts = `variance-unclear`.
  h0057 asana__task.sql gates `tags`/`number_of_tags` behind `var('asana__using_tags')`/`var('asana__using_task_tags')` (resolved disabled → less columns); h0056 r2 PASSED by editing ONLY the tags intermediate + tag model, never touching asana__task. Reasoning is pure h0043 package-migration gating (package×82); all Move-A/Move-B tokens are README prose echoed in the prompt, none shaped the drop. Byte-identical package rule → same-rule different-draw = variance.
- DONE: `## Failure Review` block written — ana-eng004 = incomplete-artifact (Move A fired + reached SQL, full fact⋈dim join with attachments present, but collapsed the duplicate join key → kept i.product_id, dropped p.product_id → 22<23); asana001 = variance-unclear; all five failure-review questions answered; follow-up routing recommends REVISE Move A with an upstream-column-AUDIT step (count every upstream column, keep BOTH copies of a shared join key), Move B unchanged, re-smoke.

### Summary
NO-GO: zero flips and one regression on a clean audit (14/14 clean, captured>0 every cell). ana-eng004 missed by exactly one column — Move A fired and reached the committed OBT (full fact⋈dim join, attachments PRESENT, contradicting the dispatch's attachments pre-diagnosis), but the worker collapsed the duplicate join key (kept i.product_id, dropped p.product_id → 22 vs the solution's 23). asana001's regression is `variance-unclear`: the committed asana__task.sql gated the tags columns behind a package var that resolved disabled (pure h0043 package-migration gating), the byte-identical package rule fired differently than h0056 r2 (which fixed tags upstream-only and never touched asana__task), and neither Move A nor Move B shaped the drop (all their tokens are README prose). Routing: REVISE Move A with an explicit upstream-column-AUDIT step (keep both copies of a shared join key), Move B unchanged, re-smoke.
