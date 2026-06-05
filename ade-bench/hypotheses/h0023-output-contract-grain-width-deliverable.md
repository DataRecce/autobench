---
id: h0023
title: Output Contract (new stage) — write each model's grain key-source, ordered column set, per-column types, and complete deliverable set from named local files BEFORE writing SQL (folds in the re-classified ana-eng006 — type-cast, not fan-out)
status: propose
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug types 2 width + 3star re-classified-as-type/width + 6 deliverable-set); realizes the new Output Contract stage; merged carrier of two convergent finalize candidates (width + 3star). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The width cluster the dispatch targets (`ana-eng004`, `f1002`; oracle ERRORs of the
shape "`<model>` has less columns than `solution__<model>`") shares a root finding with
the grain, type, and incomplete-deliverable clusters that the @baseline solver fails: the
seed solver **never writes down what the model it is about to author must look like**
before writing its SQL. Implementation prose says only "make the smallest task-relevant
change following local patterns" — there is no control point at which the solver commits a
concrete grain key-source, an ordered column set, per-column types, and a deliverable list,
derived by reading named local files, *before* it starts writing the query. So it emits the
minimum it reasons it needs and stops at compile-green.

**Falsifiable claim (the single README change — a NEW `## Stage: Output Contract` inserted
between Exploration and Implementation):** adding one stage that requires the solver, for
every model it must author or restructure, to *write the contract down before writing any
model SQL* — (1) the grain and the SOURCE of its full key set (the relation the existing
code or instruction treats as the driver; for a CTE extraction, the un-narrowed key set the
CTEs produced before the downstream model re-keyed/`coalesce`d them), (2) the full ordered
column set (from a declaring `schema.yml` `columns:` list, else from the upstream relations'
`SELECT` lists plus the same-kind sibling's convention, plus instruction-named columns),
(3) per-column types (taken from the relation each column is sourced from — the upstream
relation or the installed `dbt_packages/` staging model — with the matching cast applied in
place, never from a yml description), and (4) the complete deliverable model set (resolve the
`ref()` graph; a `ref()` to a non-existent model is a deliverable; an installed-package model
the project `ref()`s is the template) — then build to satisfy that written contract and treat
it as the Implementation acceptance gate — will move the locally-derivable shape/width/type/
deliverable failures and raise `stratified_pass_at_1` above the `@baseline` 0.6458.

**The candidate `3star` "join fan-out / double-count" sub-type is FALSIFIED for its only
target and folds into THIS hypothesis.** That type was filed under the label *"Join fan-out /
double-count (large-magnitude)"* with the single target `ana-eng006` (`AUTO_fact_inventory_equality`,
`Got 204` ≈ 2× the 102-row solution). A direct read of the `@baseline` oracle output kills
the label: in the baseline cell
`runs/ade-bench-baseline/622bdedac572b479/ade-bench-ana-eng006__vsSQPnr/verifier/test-stdout.txt`,
`check_row_count` **PASSES** and `AUTO_fact_inventory_existence` **PASSES** — so
`fact_inventory` was built with exactly the right **102 rows** and there is **no row
duplication / no fan-out at all**. The committed baseline `fact_inventory.sql` already dedups
with `ROW_NUMBER() OVER (PARTITION BY inventory_id …) WHERE row_number = 1`. The `Got 204` is a
**value/type-representation symmetric difference** (102 model rows + 102 solution rows, all
mismatching), driven by one column: the committed model passes `transaction_created_date`
through as a raw `MM/DD/YYYY HH:MM:SS` **string** (no `CAST`/`STRPTIME`) where the correct
answer is a `DATE`. Separately, `dim_products` and `obt_product_inventory` fail with width
("has less columns") errors. So `ana-eng006` is **not** a fan-out — it exercises this stage's
**TYPES clause** (the raw date string → `DATE` cast: exactly the asana002 mechanism, the one
in-place mechanical cast copied from a concrete local relation that has ever landed in this
loop) **plus its COLUMN-SET clause** (the `dim_products`/`obt_product_inventory` width gaps). A
fan-out-prevention construction rule would be inert by premise here (`check_row_count` already
passes; nothing multiplies rows), repeating the h0008 mis-targeting the ledger calls out. So
the candidate 3★ sub-type drops as a standalone, and `ana-eng006` is carried under THIS
hypothesis's TYPES + COLUMN-SET clauses — honest that the exact `STRPTIME` format and the two
width gaps are not locally pinned (no `schema.yml` declares
`fact_inventory`/`dim_products`/`obt_product_inventory`; the missing columns live only in the
hidden solution seed), so the stage's purchase on `ana-eng006` is the locally-derivable
in-place date cast, not a full flip.

**Two literal width candidates were KILLed before filing; this is the type's on-theme bet.**
The critique correctly rejected both straight "mirror the sibling projection" candidates
(`output-contract-sibling-projection`, `implementation-mirror-sibling-projection`) on
proven premise falsification, not speculation. h0011 (REJECTED) already prescribed exactly
that mechanism for `ana-eng004`: its rollout shows the solver consulted the sibling
`obt_sales_overview` ~23 times, emitted 22 columns, logged a "column contract" check — and
still ERRORed "has less columns than `solution__obt_product_inventory`". I confirmed against
the shipped workspace why: the sibling `obt_sales_overview.sql` selects `p.attachments` (it
KEEPS dim_products.attachments), and the hidden 22-col answer = 13 of dim_products' 14
columns (it DROPS `attachments`) + 9 `fact_inventory` columns + one DERIVED `ipd` column
that exists in no upstream relation or sibling. The two decisive width deltas (drop
`attachments`, derive `ipd`) live only in the hidden seed — `derivable:no` — so no
sibling-mirror wording recovers them, and a re-statement of h0011 on the identical target is
doomed. For `f1002` the local `__stats.yml` over-declares `most_podiums` at 6 columns
(rank/driver_full_name/podiums/p1/p2/p3) while the true answer is 3 — following the yml
builds 6 and still mismatches, so width here is also not locally provable.

**Why this escapes the dead-prose / blind-to-oracle ceiling where h0011/h0013/h0016 did
not.** It does NOT claim to recover oracle-only signals. It is a different control point and
a different lever shape:

- It is **not** an in-line Implementation rule asking the solver to restructure SQL in the
  moment of writing it (the inert h0010/h0011/h0016 ask — acknowledged, committed SQL
  byte-identical). It moves the lever EARLIER: the solver must first WRITE DOWN a concrete
  contract extracted by reading named local files, and Implementation becomes a fill-in
  measured against that written contract.
- Its load-bearing flips are the **locally-derivable** legs, not width or the exact
  `ana-eng006` deltas. `asana004` grain is derivable from the named `asana__project.sql`: the
  `project` spine drives the join and the `coalesce(...,0)` lives downstream in `project_join`
  (I verified both in the shipped workspace model and the instruction's named 3 columns), so
  the contract's grain rule — *reproduce the un-narrowed CTE output; do not move the
  coalesce/spine into the new model* — is a copy-and-repoint edit, the only edit shape that has
  ever landed (asana002). `quickbooks001` deliverable set is `derivable:yes`: local int models
  `ref()` the three missing `stg_quickbooks__*` models and the installed
  `dbt_packages/quickbooks_source` ships them as templates. The type leg concentrates on the
  one mechanism that flipped a target (asana002 `::timestamp` cast copied from the installed
  package model), which is also the live lever on `ana-eng006`'s `transaction_created_date`.
- For `ana-eng004` width, the stage at least makes the solver DERIVE the contract correctly
  (22 locally-supported columns) rather than hand-rolling a narrow projection — but the
  hypothesis is honest that the two oracle-only deltas keep it from flipping, so it is
  carried as the width representative / do-no-harm case, not the flip claim. The **derive,
  do-not-pad** guard exists precisely so the stage does not make `f1002` worse by padding to
  the yml's 6 over-declared columns.

Distinct from h0013 (Exploration enumeration prose — abstract, inert, NO-GO) and h0016
(Implementation grain skeleton — installed the shape, never the correct spine source): this
writes a concrete per-model contract as the *precondition* for SQL and frames the grain fix
as copy-and-repoint, not "restructure your query." Distinct from h0012 (post-answer
Validation recompute — a check, not construction). One idea, one stage (the new Output
Contract stage).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact: the stage references only local workspace
artifacts (the project's own `schema.yml`/`*.yml`, `sources.yml`, seeds, same-directory
siblings, upstream relations the model selects from, `dbt_packages/` staging models, the
broken `ref()` graph, the task instruction) — no public fetch (no
`curl`/`wget`/`git clone`/`git ls-remote`/web), no reference to hidden
`AUTO_*`/`solution__*`/`check_*`/verifier tests or the phrases
"equality test"/"has less columns"/"expected output seed", and it does not weaken the
dependency/package guardrails. The README lines 1-32 stay byte-identical; the spec differs
from baseline only in `experiment:` + `solver_workflow:` (smoke adds only `benchmark.tasks`).

This rule is **generative** (it fires on every authoring/refactor task), so per gatekeeper
G8 the smoke set carries a cross-family regression-canary panel — one currently-passing
`@baseline` task per non-target family: `ade-bench-airbnb001`, `ade-bench-ana-eng001`,
`ade-bench-asana001`, `ade-bench-f1007`, `ade-bench-quickbooks002` — plus
`ade-bench-f1001` as the non-package convention-bleed sentinel (the exact task the h0009
ungated package-fidelity rule regressed). **No intercom canary is possible:** intercom has no
passing `@baseline` task (`intercom001/002/003` all fail), so that family cannot supply a
passer — G8 should not expect one. Targets (smoke, all `ade-bench-` prefixed): the
locally-derivable flip candidates `ade-bench-asana004` (grain — the load-bearing
copy-and-repoint flip) and `ade-bench-quickbooks001` (deliverable set, `derivable:yes`), plus
`ade-bench-ana-eng004` (width/type-2 representative whose contract is locally derivable even
though its two oracle-only deltas cap a full flip) and the re-classified `ade-bench-ana-eng006`
(TYPES + COLUMN-SET — the in-place date cast is the live lever; the width gaps are not
locally derivable). The load-bearing flips are the locally-derivable legs (asana004 grain,
quickbooks001 deliverables); the width and the exact `ana-eng006` deltas sit at the
blind-to-oracle ceiling and are not flip claims.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h00NN-contract-output-grain-width-deliverable.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs
`codex-ade-dbt-minimal/README.md` is a single contiguous insertion of one new
`## Stage: Output Contract` block between Exploration (end, current line 48) and
Implementation (current line 50), leaves Exploration/Implementation/Validation/Finalization
and the dependency/package guardrails (lines 1-32) byte-identical, and does not reference
hidden `AUTO_*`/`solution__*`/`check_*`/verifier tests, the phrases
"equality test"/"has less columns"/"expected output seed", or any external fetch, and does
not weaken the leak-guard. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`. Because the stage is generative, the full-run diff
(not the targets-only smoke) is the binding evidence for regression — the h0009
convention-bleed losses were structurally invisible to a targets-only smoke set. The smoke
deep-dive must VERIFY THE ARTIFACT, NOT THE CHATTER: read the committed SQL and use unchanged
distance-to-pass (`Got N` vs `@baseline`) as the cheap inert-detector before any transcript
read (a written contract that is mere chatter while the committed SQL is unchanged is the
h0010/h0013/h0016 inert signature and is a NO-GO) — for `asana004` confirm the new
`int_asana__project_user_agg` reproduces the un-narrowed CTE key set (no `coalesce`, no spine
moved into it) and `asana__project` repoints its `ref`; for `quickbooks001` confirm the three
`stg_quickbooks__{estimate,refund_receipt,sales_receipt}` models were actually BUILT (not
merely discussed); for `ana-eng004` confirm the projection was derived to the full
locally-supported width and the lever did not regress it; for `ana-eng006` confirm the
committed `fact_inventory.sql` now applies the in-place `DATE` cast on
`transaction_created_date` (do not expect the `dim_products`/`obt_product_inventory` width
gaps to clear — they are not locally derivable).

**Smoke gate:** on the 4 targets (`ade-bench-asana004`, `ade-bench-quickbooks001`,
`ade-bench-ana-eng004`, `ade-bench-ana-eng006`) + the cross-family canary panel
(`ade-bench-airbnb001`, `ade-bench-ana-eng001`, `ade-bench-asana001`, `ade-bench-f1007`,
`ade-bench-quickbooks002`, `ade-bench-f1001`), the variant must not regress any canary
(especially the non-package `f1001` convention-bleed sentinel) and should flip at least one of
`asana004`/`quickbooks001` (the locally-derivable legs) to a pass before promotion to full. A
0/4 with `ana-eng004` and `ana-eng006` unchanged-short would confirm the width/exact-delta
legs are at the blind-to-oracle ceiling; an `f1001` regression would confirm convention bleed
and is a NO-GO regardless of target flips.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
