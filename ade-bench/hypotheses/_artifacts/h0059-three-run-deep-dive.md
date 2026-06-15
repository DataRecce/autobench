# h0059 deep-dive — asana003 PASSED via INLINE+RECONCILE across all 3 runs + probe

**Date:** 2026-06-15 · **Scope:** read-only forensic audit of the 4 asana003 draws of
h0059 (tmp-tier-removal, inline+reconcile lever). Goal: confirm each reward-1 PASS is the
prescribed conservative-inline + before==after reconciliation artifact, NOT a lucky
re-derive.

## Task recap
The task deletes the Asana `tmp/` model tier and rewires each `stg_asana__[name].sql` to
read its source directly, OUTPUT UNCHANGED. The h0059 rule prescribes a CONSERVATIVE INLINE
(copy the deleted tmp's exact SELECT, swap only the relation, RECONCILE before==after —
double-entry). FAIL path = a BROAD re-derive (fresh select → column drops/renames/re-casts →
equality failures + a `cast('None' as date)` crash on empty `asana__task`).

## Per-run table

| Run | seed | INLINE (exact tmp select)? | RECONCILE ran? | tmp deleted | sources-only (check_model_sources) | equality PASS | `cast('None')` crash | audit |
|-----|------|---------------------------|----------------|-------------|------------------------------------|---------------|---------------------|-------|
| r1    | 42   | YES — 11/11 stg, ref(tmp)→source(), macro+get_*_columns() body unchanged | YES — explicit baseline + before==after | 11/11 | PASS | 17/17 | none | clean 6/0/0 |
| r2    | 43   | YES — 11/11 stg (started var(), refined to source()) | YES — explicit, **caught the FAIL path live** | 11/11 | PASS | 17/17 | none | clean 1/0/0 |
| r3    | 44   | YES — 11/11 stg, ref(tmp)→source(), body unchanged | YES — explicit + full-row fingerprints | 11/11 | PASS | 17/17 | none | clean 1/0/0 |
| probe | null | YES — 11/11 stg, FROM kept tmp's literal `var()`, introspection→source() | YES — explicit before==after | 11/11 | PASS | 17/17 | none | (probe not audited per scope) |

All four: reward 1.0, verifier "Verification successful!", 17/17 data tests pass including
`check_model_sources`, zero test FAIL/ERROR, zero `cast('None' as date)` crash.

## Per-run detail

**r1 (the cleanest reference).** Ensign captured the pre-refactor baseline first ("run the
existing Asana source models first so the baseline is captured", row counts logged:
project 16, project_task 2, section 13, story 3, tag 17, task 1, task_follower 1,
task_section 2, task_tag 4, team 25, user 20). Single apply_patch: 11 stg models updated
(each swaps only `from {{ ref('stg_asana__X_tmp') }}` → `from {{ source('asana','X') }}`
plus the matching `get_columns_in_relation` swap; `fill_staging_columns(... get_X_columns())`
body untouched) + 11 tmp files deleted. Post-edit: "Row-count reconciliation is clean for
all 11 staging models"; "Column reconciliation is clean … zero mismatches across column
names, order, and data types." Textbook double-entry inline.

**r2 (the strongest mechanism evidence — the FAIL path was triggered and caught).** First
apply_patch inlined the tmp's literal body using `{{ var('project') }}` for BOTH the FROM
and `get_columns_in_relation`. Post-edit build FAILED: "`fill_staging_columns` macro filled
key columns as null … `adapter.get_columns_in_relation(var('project'))` returned no columns,
so it emitted `cast(null …)` for every expected field." A second apply_patch corrected the
introspection (and FROM) to `source('asana',...)`. Then "before/after reconciliation passed
for all eleven … same column names, same DuckDB data types, same row counts." The
reconciliation/build step is precisely what detected the latent break — this is the rule's
double-entry guard working in vivo, not luck.

**r3.** Baseline build (22/22), then snapshot of "columns, types, row counts, and full-row
fingerprints" for the 11 staging outputs. Single 11-file inline patch (ref(tmp)→source()),
11 tmp deletes. "Before/after reconciliation is clean for every affected staging model";
then a full 27-model project build + a second post-full-run reconciliation. Strictest of the
four (added row fingerprints + full-graph rebuild).

**probe (seed null).** Same baseline-capture-then-inline-then-reconcile spine. Distinct
surface shape: the probe kept each tmp model's *literal* `select * from {{ var(...) }}` body
in the FROM (the most literal "copy the tmp's exact select") and pointed only
`get_columns_in_relation` at `source('asana',...)`. It explicitly probed `var()` vs
`source()` for introspection ("`get_columns_in_relation(var(...))` is not reliable from the
root inline context") and chose source() for introspection. "After-state schemas and row
counts match the baseline for all affected staging models." Passed identically (`check_model_sources`
satisfied by the source() introspection call).

## Cross-run synthesis

- **Same mechanism, all 4 draws.** Every draw (a) captured a pre-refactor baseline, (b)
  inlined the deleted tmp's exact SELECT into each of the 11 stg models swapping only the
  relation (no column drops/renames/re-casts — never a fresh re-derive), (c) deleted all 11
  tmp files, and (d) ran an explicit before==after reconciliation over columns/types/row
  counts. The reconciliation step fired in **every** draw, not just some.
- **Minor, benign surface variation in the FROM-relation expression**, all converging on a
  passing inline:
  - r1, r3: FROM → `source('asana',X)` directly (one patch).
  - r2: FROM started `var(X)` → refined to `source('asana',X)` after the build/reconcile
    caught the null-column break.
  - probe: FROM kept tmp's literal `var(X)`; only introspection → `source('asana',X)`.
  This variation is in HOW the source relation is named in the FROM, not in the SELECT shape
  (columns/casts/aliases are identical to the tmp in all four). The verifier's
  `check_model_sources` is satisfied in all cases by the `source()` introspection call, and
  equality holds because the column-filling macro body is unchanged.
- **The FAIL path is real and the guard caught it (r2).** r2 actually produced the
  null-column degenerate edit and the build+reconcile step flagged it before completion. That
  is direct evidence the double-entry reconciliation is load-bearing, not decorative.
- **No residual coin-flip risk.** No draw passed via a path other than inline+reconcile; no
  draw re-derived a fresh select; no `cast('None' as date)` crash occurred in any draw. The
  one knob that varied (var vs source in the FROM) is self-correcting under the prescribed
  reconciliation — the worst case (r2's var/var) was caught and fixed within the same run.
- **Audits clean.** r1 6/0/0, r2 1/0/0, r3 1/0/0 (clean/coverage_missing/tainted), asana003
  trial clean in every audited run.

## Verdict

asana003 is a **reproducible inline+reconcile flip** — all 3 seeded runs + the probe passed
via the prescribed conservative-inline edit (exact tmp SELECT preserved, only the relation
swapped) gated by an explicit before==after reconciliation that demonstrably catches the
FAIL path (r2). No residual coin-flip risk: every draw exercised the same double-entry
mechanism, the reconciliation fired in all four, and no draw reached PASS by a lucky
re-derive.
