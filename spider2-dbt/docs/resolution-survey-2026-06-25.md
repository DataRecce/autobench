# spider2-dbt Failed-Task Strategy: Reachability, Families, Classifier, Backlog, 70% Verdict

## 1. Reachability Ledger (offline-verified, 41 surveyed tasks)

Every survey ran the real `duckdb_match.py` comparator against gold from a source-only reconstruction. Reachability is reported by PROOF strength, not optimism.

| Class | N | Tasks |
|---|---|---|
| REACHABLE_VERIFIED | 32 | airbnb001, airport001, apple_store001, asset001, divvy001, f1002, f1003, flicks001, hive001, intercom001, jira001, marketo001, netflix001, playbook002, provider001, quickbooks003, recharge001, recharge002, reddit001, retail001, salesforce001, shopify_holistic_reporting001, social_media001, superstore001, synthea001, tickit002, tpch001, twilio001, xero001, xero_new001, xero_new002, zuora001 |
| REACHABLE_PROBABLE | 2 | movie_recomm001 (fuzzy match unverified), quickbooks001 (running_balance window order unverified) |
| VERIFIER_FALSE_NEGATIVE | 2 | chinook001 (gold db unbuilt), sap001 (GL source tables omitted from image) |
| NOT_REACHABLE_ORACLE | 5 | analytics_engineering001, asana001, atp_tour001, scd001, pendo001 |

**HARD reachable ceiling = 19 + 32 + 2 + 2 = 55 / 61 (90%).**

The 6 dead tasks: 4 true oracle/tie-break gaps (undocumented exclusion, hash-order string_agg, name-resolution, unstable row_number tie-break) + 2 frozen-clock nondeterministic (atp_tour001 age, pendo001 spine) that only a benchmark date-pin could rescue.

## 2. Strategy Families (grouped by shared fix + oracle-free router)

Five solver-actionable families + one harness family. Reachable counts only count tasks where the fix is the decisive flip.

1. **SPINE_COMPLETENESS (12)** — under-emit because the solver drove from fact activity instead of the calendar-spine/full-dimension. Fix: drive from spine, left-join facts, carry balances forward, keep NULL. *Highest fanout, highest canary risk (inverse of the default rule).*
2. **OVER_EMIT_COLLAPSE (7)** — over-emit by full-refreshing incrementals, unioning sub-grains, joining the full user table, or using the wrong filter column. Fix: collapse to the canonical slice (incremental window / verbatim int_ union / role dimension / sibling-mirror).
3. **AUTHOR_MISSING_MODEL (4)** — target absent from `models/` though documented in schema.yml or named in the contract. Fix: enumerate every contract table; author from the declared recipe.
4. **BUILD_AS_IS / BEHAVIOR_PRESERVING (3)** — solver edited/rewrote existing models that already encode gold. Fix: `dbt build` unmodified; never 'fix' buggy-looking math; carry int_ balance columns through.
5. **VALUE_DEF (7)** — correct grain, wrong column value/type/sign/null/round. Fix: per-column-name contract (id→VARCHAR, COUNT(*) vs DISTINCT by name, %-conversion, NULL-vs-0, 2dp money round). *Lowest bleed when scoped to a named column.*
6. **VERIFIER/FIXTURE (2)** — harness repair (build gold, ship source). Not a solver lever.

## 3. Classifier Stage (the core deliverable)

A router prepended to the solver README, running on oracle-free signals only (instruction text, target names, `models/`+schema.yml tree, dbt_project.yml vars, source information_schema). Two axes:

- **Axis 1 — Materialization gate** (per condition_tab): existing `.sql` stem → BUILD_AS_IS; documented-but-unbuilt → AUTHOR from recipe; declared source-id missing → FIXTURE-DEFECT flag; lone missing final model with int_ intermediates → verbatim UNION; ALWAYS enumerate every contract table.
- **Axis 2 — Grain/Value policy** (per authored target): G1 spine-completeness (name+spine-model gate), G2 over-emit-collapse (incremental/role-dim/sibling gates), G3 value-def (per-column-name gates), G4 build-as-is guard (existing computed model).

**Isolation principle:** every Axis-2 rule is gated on a disjoint name/schema/file signal, so they compose additively without interference (gated-levers-compose prior). The default grain rule is replaced by G1 *only when G1's precondition fires* — protecting the 19 passers. No rule reads or hard-codes a gold-derived value; offsets/dates/tie-breaks are steered via "copy the nearest sibling", never a literal (avoids gold-leak).

## 4. Ranked Backlog (LEFT-SHIFT noted; reachability already proven ⇒ smoke tests COMPLIANCE)

1. **MATERIALIZATION gate** — +4 to +8, reachability verified, smoke = does the router pick build-vs-author and kill the "create new model" reflex. Smoke: zuora001 + 1 authoring canary.
2. **VALUE_DEF column rules** — +3 to +6, all verified, smoke = solver applies the named-column rule. Smoke: retail001 + num_invoices canary.
3. **OVER_EMIT_COLLAPSE** — +4 to +6, all verified, smoke = collapse compliance. Smoke: tickit002 + full-population canary.
4. **SPINE_COMPLETENESS** — +6 to +10 OR net-negative; the binding experiment, smoke = gate isolation. Smoke: salesforce001 + marketo001, two per-key passer canaries, require 0 regressions.
5. **FIXTURE/VERIFIER repair** — +2 deterministic, harness-only, no solver smoke; idempotent gold-build guard.

## 5. Calibrated 70% Verdict

**Attainable but a stretch.** Ceiling 55 (90%) leaves ample headroom over 43, so the constraint is NOT reachability. Every reachable task has a verified oracle-free router signal, so it is NOT raw steerability either.

**Binding constraint = compliance-under-a-gate-seam + variance.** The SPINE family (largest, +12 reachable) is the literal inverse of the grain rule the 19 passers depend on; its dominant risk is canary regression on a leaky gate. And "reached the answer offline" proves gold is attainable, not that the temp=0 production solver complies (sim-validates-tendency scar).

**Realistic band: 38–48 / 61.** Floor 38 (~62%) = the two low-risk families + 2 fixture repairs. Center 43 (70%) = + a clean OVER_EMIT_COLLAPSE. Ceiling 48 (~79%) = + SPINE landing cleanly. Hitting 43 requires ~24 of the 36 reachable/probable/fixture tasks to actually flip (~66% conversion) — that conversion rate, not the ceiling, is the wall. Budget for 38–43 likely; treat 43 as the optimistic-but-real target contingent on the gated spine rules not regressing the baseline 19.


---

## 6. Classifier Stage — full routing rules

```
CLASSIFIER-STAGE DESIGN — a router prepended to the top of the solver README. It runs BEFORE any modeling on oracle-free inputs only: the instruction text, the eval condition_tabs / target table names, the models/ + schema.yml tree, dbt_project.yml vars, and the SOURCE information_schema (column names, dtypes, COUNT vs COUNT DISTINCT on join keys). No gold values are ever read.

Two axes, evaluated in order. AXIS 1 (MATERIALIZATION) decides WHAT to build; AXIS 2 (GRAIN/VALUE POLICY) decides HOW.

=== AXIS 1: MATERIALIZATION GATE (run first, per target table in condition_tabs) ===
For each table T in the eval contract:
  R1. If models/**/T.sql EXISTS  -> BUILD_AS_IS: `dbt deps && dbt build`, do NOT create or edit model SQL. Repair a model ONLY if dbt build fails; never to 'improve' a passing build. [zuora001]
  R2. Else if schema.yml documents a model named T (refs + column descriptions) but no T.sql -> AUTHOR T from its declared recipe, mirroring the nearest same-role sibling's conventions (surrogate-key offset+ROW_NUMBER, {{ref('dim_*')}} FK joins, dtypes). Do NOT invent a differently-named table. [superstore001, movie_recomm001]
  R3. Else if T depends (via dbt_project.yml vars or an int_ ref) on a SOURCE identifier that is ABSENT from the source DB information_schema -> FLAG FIXTURE DEFECT, abort, report ungradeable. Do NOT fabricate source rows. [sap001]
  R4. Else -> AUTHOR T as a new model.
  R5. ALWAYS enumerate EVERY table in condition_tabs, not just the prose-named one. [intercom001, analytics_engineering001]
  R6. If int_*__T_* intermediates exist and T is the lone missing sibling in an otherwise-complete dir -> AUTHOR T as a verbatim UNION ALL / FULL OUTER JOIN of those intermediates; do NOT re-derive from raw. [synthea001, shopify_holistic_reporting001]

=== AXIS 2: GRAIN / VALUE POLICY (run per authored target) ===
  G1 (SPINE_COMPLETENESS): IF target name matches /_daily_|_rollup|_balance_sheet|_snapshot|_overview/ AND a date-spine model ships, OR instruction has completeness verbs ('each/every/map X to Y/balance on a monthly basis') over a named dimension whose rowcount == target grain, OR target matches *_enhanced/*_metrics/*__<entity> with a same-named source dimension -> DRIVE FROM THE SPINE/DIMENSION (left-join facts; carry cumulative balances forward across zero-activity periods; leave metrics NULL not 0). [salesforce001, xero_new001, jira001, provider001, playbook002]
  G2 (OVER_EMIT_COLLAPSE): IF target maps to a materialized='incremental' model with an is_incremental() filter -> emit ONLY the latest window. IF target fact carries seller_*/buyer_* AND an int_<role>_extracted_from_users ships -> inner-join through the role dimension. IF a *_by_<entity> stat has an opposite-entity sibling -> copy the sibling's filter verbatim, swap only the entity. [airbnb001, tickit002, f1003]
  G3 (VALUE_DEF, per compared column): cast identifier cols to VARCHAR when source numeric + 'unique identifier' description; COUNT(*) vs COUNT(DISTINCT) by column NAME (total_* vs num_*); convert VALUE+VALUE_TYPE='percentage' against the parent base; NULL-preserve count_if for feature-absent metrics vs coalesce-0 for categorical tallies; ROUND money to 2dp where gold is clean; group by the timestamp the KEY embeds even if the prompt says 'daily'. [retail001, divvy001, recharge001, f1002, asset001]
  G4 (BUILD_AS_IS guard): when a target is a thin reshape over an existing computed model, reproduce that model's math verbatim — do NOT 'fix' a buggy-looking formula; if an int_*balances column already exists, project it through, don't recompute. [airport001, quickbooks003]

=== ISOLATION (the gate IS the mechanism) ===
Every Axis-2 rule is precondition-gated on a NAME/SCHEMA/FILE signal that is DISJOINT across families, so they compose additively without interference (per the gated-levers-compose prior). The standing default README grain rule ('drive from fact activity, do not pad zero rows; inner-join dimensions') is REPLACED by G1's spine rule ONLY when G1's precondition fires; on everything else it stays as-is to protect the 19 passers. This is the single highest-risk seam: G1 is the literal inverse of the default rule, so its gate must be tight. No rule reads or hard-codes a gold-derived value (offsets, dates, tie-break seeds) — those are steered via 'copy the nearest sibling', never a literal.
```


## 7. Family detail (router signal · playbook · canary risk · smoke anchors)


### SPINE_COMPLETENESS (GRAIN_UNDER_EMIT) — reachable 12
- **tasks:** salesforce001, recharge002, xero001, xero_new001, xero_new002, jira001, marketo001, intercom001, provider001, hive001, flicks001, playbook002
- **router_signal:** ORACLE-FREE. Fires when ANY of: (a) target table name matches /_daily_|_rollup|_balance_sheet|_snapshot|_overview/ AND a date-spine model (int_*__calendar_spine / int_*date_spine) ships in models/; (b) instruction carries completeness verbs 'each/every/for all/map X to Y/balance ... on a monthly basis' over a NAMED reference/dimension source whose rowcount equals the target's expected grain; (c) target name matches the Fivetran *_enhanced / *_metrics / *__<entity> dimension convention AND a same-named source dimension table exists. ALL readable from instruction text + target table name + source schema; no gold access.
- **playbook:** Drive the row grain from the SPINE/DIMENSION side, not the fact/event side. (1) Start FROM the calendar-spine model (or the full dimension table) as the driving relation; (2) LEFT JOIN the per-period/per-key fact aggregates onto it; (3) for balance-sheet/cumulative targets, carry the running SUM forward across zero-activity periods (window SUM over partition by entity order by date_month) and add any package-standard synthetic rows (e.g. Retained Earnings = -cumulative P&L); (4) leave metric columns NULL on no-activity rows (do NOT coalesce-to-0 unless the spec says zero-fill); (5) for financial money columns ROUND(net_amount,2) so the comparator's str()-keyed float sort aligns. NEVER let an INNER JOIN or a GROUP BY over only-active rows define the period/entity grain.
- **canary_risk:** HIGH and structurally adversarial: this family is the DIRECT INVERSE of the existing solver-README grain rule ('drive from fact activity; do not pad zero-activity rows'), which the 19 current passers (per-key aggregate tasks) depend on. An ungated flip OVER-emits on genuine event/activity-grained targets. MUST be precondition-gated on the spine/dimension/completeness signal so the gate IS the isolation; fires only on _daily_/_rollup/_balance_sheet/_enhanced/_metrics targets with a spine or named-dimension source. Secondary NULL-vs-zero-fill risk: forcing coalesce-to-0 breaks salesforce001/scd001 (gold keeps NULL).
- **smoke_anchors:** salesforce001, marketo001, xero_new001

### OVER_EMIT_COLLAPSE (GRAIN_OVER_EMIT) — reachable 7
- **tasks:** airbnb001, apple_store001, synthea001, shopify_holistic_reporting001, tickit002, reddit001, f1003
- **router_signal:** ORACLE-FREE, several distinct sub-signals: (a) target maps to a model config(materialized='incremental') with an is_incremental() period-restriction WHERE clause -> emit only the latest window (airbnb001); (b) target is the lone missing final model in an otherwise-complete dir that has int_*__<target>_* intermediates -> UNION ALL the intermediates verbatim, don't re-derive (synthea001, shopify..., apple_store001); (c) target fact carries role-prefixed columns (seller_*/buyer_*) AND an int_<role>_extracted_from_users dimension ships -> inner-join through the role dimension (tickit002); (d) target is a *_by_<entity> stat with an existing opposite-entity sibling model -> copy the sibling's filter verbatim, swap only the entity (f1003); (e) parallel prod_<entity> passthrough tables built 1:1 from raw_<entity> -> no inner-join prune (reddit001).
- **playbook:** Collapse to the canonical slice. Respect incremental contracts (emit only the latest window); for missing final models, UNION ALL / FULL OUTER JOIN the EXISTING int_ intermediates verbatim rather than re-aggregating raw sources; resolve role attributes through the role-specific intermediate dimension (inner join) not the raw user table; mirror an opposite-entity sibling's exact filter/aggregation column (e.g. position not position_order) when a sibling exists; for passthrough tables preserve source grain and do not inner-join-prune. The comparator's hard len(v)==len(v) gate means a single extra/missing row fails every gold column-vector — grain exactness is binary.
- **canary_risk:** MEDIUM. Sub-signals are each narrow and structurally gated (incremental config, sibling-file existence, role-dimension existence) so cross-task bleed is low. The one watch item: a blanket 'UNION existing intermediates verbatim' could regress a task whose final model legitimately FILTERS/transforms its intermediates; scope to the missing-final-model-with-existing-intermediates pattern and let row-count-from-source decide domain inclusion. reddit001 carries an intra-task tension (keep orphan comments AND drop 1 curated post) so even a scoped rule leaves a residual single-row gap there (its posts side has an undocumented 1-row drop).
- **smoke_anchors:** synthea001, tickit002, airbnb001

### BUILD_AS_IS / BEHAVIOR_PRESERVING — reachable 3
- **tasks:** zuora001, airport001, quickbooks003
- **router_signal:** ORACLE-FREE: (a) for each table in eval condition_tabs, a file models/**/<table>.sql ALREADY EXISTS (target name == existing model stem) -> BUILD-AS-IS: dbt deps + dbt build, do NOT add/edit model SQL (zuora001); (b) the requested target is a thin pivot/aggregation over an EXISTING committed model that performs a non-trivial math computation (haversine, ratio, conversion) -> reproduce that model verbatim, do NOT 'fix' math that looks buggy (airport001); (c) an int_*balances/snapshot model already exposes the requested balance column -> PROJECT-AND-FILTER it through, don't recompute a running sum (quickbooks003). All detectable from the eval spec + models/ tree + source schema.
- **playbook:** The gold answer is defined as 'what this project produces when built unmodified.' If a model whose stem equals a target table already exists: run dbt deps + dbt build only, never create or edit model SQL (repair ONLY if dbt build fails, never to 'improve' a passing build). If a needed intermediate already exists, ref() it unchanged even if its math looks wrong. If an int_ layer already exposes the requested balance/metric column, carry it through unchanged rather than re-deriving. Directly counters the README's 'create a NEW model for each result table' reflex that corrupted zuora001 (edited 5 models) and airport001 (rewrote the haversine).
- **canary_risk:** MEDIUM. 'Do not edit/add models' must be strictly gated to existing-stem matches, or it suppresses genuine authoring tasks (the majority). 'Never correct existing model logic' could block a task that genuinely ships a stubbed model expecting completion. Gate: reproduce verbatim ONLY models you merely ref() as inputs to a NEW target; you MAY complete a model the instruction explicitly tells you to finish; repair an existing model only when dbt build fails.
- **smoke_anchors:** zuora001, airport001

### AUTHOR_MISSING_MODEL (MATERIALIZATION gate) — reachable 4
- **tasks:** superstore001, social_media001, movie_recomm001, quickbooks001, intercom001, chinook001, sap001
- **router_signal:** ORACLE-FREE and the PRIMARY top-of-router gate: for each table in eval condition_tabs, glob models/ for a matching .sql stem AND check schema.yml for a documented-but-unbuilt model name. Three outcomes: (1) target present as .sql -> route to BUILD_AS_IS; (2) target absent but schema.yml documents it with refs/column descriptions -> AUTHOR it from the declared recipe, do NOT invent a differently-named table (movie_recomm001, superstore001); (3) target's declared SOURCE identifier (dbt_project.yml vars) resolves to a table NOT in the source DB -> FIXTURE DEFECT, flag ungradeable (sap001). Also: condition_tabs lists MULTIPLE targets but instruction names only the obvious one -> enumerate EVERY contract table (intercom001 built only 1 of 2).
- **playbook:** Enumerate every table in the eval contract and materialize each named target. For a schema.yml-documented-but-unbuilt model, build it from its declared refs + per-column descriptions, mirroring the nearest same-role sibling's conventions (surrogate-key '<offset> + ROW_NUMBER() OVER(order by null)', {{ ref('dim_*') }} FK joins, dtype/rounding). Do NOT invent a differently-named table or build only the suggestively-named one. A pre-flight gold-integrity check (condition_tabs vs gold table set; declared source-ids vs information_schema) surfaces fixture defects (chinook001/sap001) instead of silent FAIL.
- **canary_risk:** LOW for completeness (column-containment tolerates extra predicted tables/columns, so 'emit every contract table' is near-zero regression). MODERATE for the recipe sub-rules: hard-coding surrogate-key offsets (1000 vs 100 vs 10) is gold-derived and not uniformly inferable — steer via 'copy the nearest same-role sibling's convention', never a fixed literal. 'Always build every schema.yml-documented model' could waste effort on helper models; scope to the SPECIFIC graded target named in the contract.
- **smoke_anchors:** superstore001, social_media001

### VALUE_DEF (column contract: value / type / sign / null / round) — reachable 7
- **tasks:** f1002, divvy001, recharge001, retail001, tpch001, twilio001, asset001
- **router_signal:** ORACLE-FREE, per-column name/schema tells: (a) identifier column described 'the unique identifier' in schema.yml while raw source is numeric -> CAST to VARCHAR (divvy001, intercom001 admin_id); (b) count column named total_invoices vs num_invoices disambiguates COUNT(*) vs COUNT(DISTINCT) (retail001); (c) source column carries VALUE + VALUE_TYPE='percentage' discriminator -> convert against parent base, don't pass raw (recharge001); (d) a metric over a high-NULL-fraction source field (fastest_laps over rank) -> count_if NULL-preserving, while categorical buckets coalesce-to-0 (f1002); (e) instruction 'categorize by percentage/ratio' -> bin + NULL above band + drop zero-denominator (tpch001); (f) overview-model pair with opposite sign conventions (twilio001); (g) target key embeds a minute-level timestamp (tt_key=ticker||ts) -> group by full ts not date even when prompt says 'daily' (asset001).
- **playbook:** Pin the exact column contract from schema.yml/source-dtype signals: cast identifier columns to the contract type; choose COUNT(*) vs COUNT(DISTINCT) by the column NAME; convert typed values (percentage discounts = base*VALUE/100); split NULL-vs-0 empty-group handling (NULL for feature-absent metrics, 0 for categorical tallies); ROUND money aggregates to 2dp where gold is clean (but leave raw where gold is raw — tpch001 splits both within one table); keep package spend-sign conventions per-table; group by the timestamp grain the KEY embeds, not the prompt noun. The comparator's str()-keyed sort makes float-noise a false-fail -> round the clean columns.
- **canary_risk:** MODERATE and column-specific. A blanket 'round all money to 2dp' is NET-NEGATIVE (regresses tpch001's raw return_total and any full-precision gold). A blanket 'cast all ids to VARCHAR' breaks genuine numeric-id columns (comparator uses isclose for numerics). A blanket 'count(*) not distinct' regresses the num_invoices sibling family. EVERY value-def rule must be keyed on the exact column NAME or the source dtype/discriminator, never applied table-wide. These are the lowest-bleed levers when scoped to a named column.
- **smoke_anchors:** retail001, divvy001, twilio001


## 8. Ranked backlog detail


**#1 — AUTHOR_MISSING_MODEL / BUILD_AS_IS** (gain +4 to +8 (zuora001, superstore001, social_media001, synthea001, intercom001, apple_store001 high-confidence; movie_recomm001/quickbooks001 probable))
- hypothesis: MATERIALIZATION gate (Axis-1 R1/R2/R5/R6): route by target-stem presence — BUILD_AS_IS for existing-stem targets, AUTHOR-from-schema.yml for documented-missing, enumerate every condition_tab. Lowest-risk, highest-fanout (touches the materialization root cause across ~10 reachable tasks).
- left-shift: Reachability VERIFIED for all members except movie_recomm001/quickbooks001 (PROBABLE) — smoke tests ONLY solver COMPLIANCE (does the router pick BUILD_AS_IS vs AUTHOR and stop the 'create new model' reflex), not whether gold is reachable.
- smoke plan: 1 target: zuora001 (should flip — pure build-as-is). 1 canary: any current passer that legitimately authors a NEW model (confirm the gate does not suppress authoring). Net +1, ETA short.

**#2 — VALUE_DEF** (gain +3 to +6 (divvy001, retail001, recharge001, twilio001, f1002, asset001))
- hypothesis: VALUE_DEF column-contract rules (Axis-2 G3): per-column-name routing for id-dtype cast, COUNT(*) vs DISTINCT, percentage conversion, NULL-vs-0, money rounding. Narrowest gates, lowest bleed.
- left-shift: Reachability VERIFIED for all 7 members — smoke tests ONLY whether the solver applies the named-column rule (compliance), reachability already proven by the offline comparator runs.
- smoke plan: 1 target: retail001 (total_invoices=COUNT(*) flip). 1 canary: report_year_invoices-style num_invoices task (confirm COUNT(DISTINCT) NOT broken). Net +1, watch the dual num_*/total_* family.

**#3 — OVER_EMIT_COLLAPSE** (gain +4 to +6 (airbnb001, tickit002, f1003, apple_store001 grain; reddit001 partial))
- hypothesis: OVER_EMIT_COLLAPSE (Axis-2 G2): incremental-window respect, role-dimension inner-join, sibling-mirror grain. Structurally gated sub-signals, medium fanout.
- left-shift: Reachability VERIFIED for all members — smoke tests solver COMPLIANCE with the collapse rule. reddit001 has a residual unreachable 1-row curated drop, so it is the one member that may not flip even at full compliance.
- smoke plan: 1 target: tickit002 (role-dimension inner-join, +0 rows over-emit fix). 1 canary: a fact task that intends the FULL user population (confirm no spurious prune). Net +1.

**#4 — SPINE_COMPLETENESS** (gain +6 to +10 if the gate holds; risk of NET-NEGATIVE if it bleeds onto the 19 passers' per-key aggregates)
- hypothesis: SPINE_COMPLETENESS (Axis-2 G1): drive daily/rollup/balance-sheet/enhanced/metrics targets from the calendar-spine / full dimension, left-join facts, carry balances forward, keep NULL. Highest fanout (12 tasks) but HIGHEST canary risk — direct inverse of the default grain rule.
- left-shift: Reachability VERIFIED for all 12 members — smoke tests are PURELY a steerability/compliance + canary-isolation test (does the gated spine rule fire on _daily_/_balance_sheet targets WITHOUT over-emitting on activity-grained passers). This is the binding-constraint experiment.
- smoke plan: 2 targets to stress the gate seam: salesforce001 (spine flip) + marketo001 (dimension-spine flip). 2 canaries: two current per-key-aggregate passers that MUST stay inner-join-scoped. The gate's isolation is the whole hypothesis; net must be >=+1 with 0 canary regressions before promotion.

**#5 — VERIFIER/FIXTURE** (gain +2 (chinook001, sap001) — deterministic once the fixture is repaired)
- hypothesis: FIXTURE/VERIFIER repair (harness-side, NOT a solver lever): build gold from source for chinook001; ship the 3 GL source tables for sap001; add a pre-flight gold-integrity gate (condition_tabs vs gold table set). Recovers 2 verifier false-negatives.
- left-shift: Reachability VERIFIED conditional on the fixture fix (chinook001 comparator PASSES once gold is materialized). NOT a solver compliance test — there is nothing to smoke on the solver side; it is a one-time benchmark repair + idempotent gold-build guard.
- smoke plan: No solver smoke. Repair fixtures, re-run the full baseline board, confirm chinook001/sap001 flip and 0 previously-passing golds change (idempotent build only when condition_tabs absent).


## 9. Per-task survey ledger

| task | family | reachability | conf | mechanism (short) |
|---|---|---|---|---|
| airbnb001 | GRAIN_OVER_EMIT | REACHABLE_VERIFIED | HIGH | Two-table compare. dim_listings_hosts (cols 2-8: LISTING_ID,LISTING_NAME,ROOM_TYPE,MINIMUM_NIGHTS,PRICE,HOST_ID,HOST_NAME) was already corre… |
| apple_store001 | GRAIN_OVER_EMIT | REACHABLE_VERIFIED | HIGH | The two graded final models — apple_store__source_type_report and apple_store__territory_report — are entirely MISSING from models/ (no mode… |
| f1003 | GRAIN_OVER_EMIT | REACHABLE_VERIFIED | HIGH | Task requires 4 target tables. Three already match gold exactly when built via the sibling-template definitions: driver_fastest_laps_by_seas… |
| reddit001 | GRAIN_OVER_EMIT | REACHABLE_VERIFIED | HIGH | Gold has two grain rules the baseline got wrong in opposite directions. prod_posts_ghosts gold = raw_posts_ghosts MINUS exactly one row (pos… |
| shopify_holistic_reporting001 | GRAIN_OVER_EMIT | REACHABLE_VERIFIED | HIGH | Gold target shopify_holistic_reporting__daily_customer_metrics has exactly 1 row: a Klaviyo-only row (all shopify_* metric cols and email NU… |
| synthea001 | GRAIN_OVER_EMIT | REACHABLE_VERIFIED | HIGH | Target main.cost: gold=809 rows (Drug 665 + Procedure 144, ZERO condition), compared cols [0,1,2,3,4,5,6,7,8,9,16], ignore_order=true. The d… |
| tickit002 | GRAIN_OVER_EMIT | REACHABLE_VERIFIED | HIGH | The fct_listings fact over-emits rows because the baseline resolved the seller dimension by joining listings to the FULL user/stg_tickit__us… |
| asset001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Baseline built both target tables at ticker+date grain (77 rows each), but gold is at ticker+ts (full minute-level TIMESTAMP) grain: gold ba… |
| flicks001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Two distinct errors caused both target tables to under-emit and mis-value. (1) actor_rating_by_total_movie: gold has 56,754 rows = EVERY dis… |
| hive001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Both target tables (stg_covid__cases, covid_cases) ship as .yml-only dbt models with NO .sql — the solver writes the SQL. Gold covid_cases =… |
| intercom001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Two compounding defects, both fail-closed under the AND-over-tables comparator. (1) MATERIALIZATION/missing-table: the eval compares TWO tab… |
| jira001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Gold target jira__project_enhanced is the COMPLETE project dimension: 3 rows, one per source `project` row (10001 TP, 10005 TCP, 10008 TBTP)… |
| marketo001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Gold target main.marketo__email_templates is a 79-row dimension: ALL most-recent-version (is_most_recent_version=True) email-template-histor… |
| netflix001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Target table is stg_google_sheets__originals_unioned; compared columns (condition_cols [0,1,3,4,5,8,9]) = title, Genre, Seasons, Runtime, re… |
| playbook002 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Baseline FAILs on cpa_and_roas (attribution_touches[15,16,17,18] is actually reachable/fine; the failure is cpa_and_roas[0,1,2]). Two compou… |
| provider001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Both AND-ed target tables under-emit on the same LEFT-vs-INNER spine axis. (1) specialty_mapping: gold = full NUCC taxonomy spine = 874 rows… |
| recharge002 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | The gold target `recharge__customer_daily_rollup` is a calendar-spine model: every customer crossed against the full date spine. Gold = 122 … |
| salesforce001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Gold salesforce__daily_activity has 91 rows = a CONTIGUOUS daily date spine (2024-06-05..2024-09-03, every day), of which 37 rows have all-N… |
| xero001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Gold xero__balance_sheet_report (1170 rows, 20 account_names, 60 months 2019-10..2024-09) is the dbt-xero package's standard balance-sheet m… |
| xero_new001 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | The graded contract ANDs three target tables: xero__general_ledger (gold 4033 rows), xero__balance_sheet_report (gold 1170 rows, compared co… |
| xero_new002 | GRAIN_UNDER_EMIT | REACHABLE_VERIFIED | HIGH | Gold xero__balance_sheet_report = 1170 rows spanning 60 month-ends (2019-10 .. 2024-09): one row per (calendar-spine month >= an account's f… |
| zuora001 | MATERIALIZATION | REACHABLE_VERIFIED | HIGH | This is a stock fivetran/zuora dbt-package reconstruction: the two target tables (zuora__account_overview, zuora__account_daily_overview) an… |
| airport001 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | Two-table task. Table 1 (fct_arrivals__malaysia_summary, condition_cols 0-4: airport_id,name,latitude,longitude,flight_count) was built CORR… |
| divvy001 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | The eval compares TWO target tables under AND: stg_divvy_data (condition_cols 0,1,2,3,6,7,8,9,10,11,12,13) and facts_divvy (0,1,2,3,4,5,6,7,… |
| f1002 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | Only finishes_by_constructor is wrong (the two championship tables already reproduce gold exactly, 0 set-diff). Two value-definition bugs in… |
| quickbooks003 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | Gold for both target tables (quickbooks__balance_sheet 276 rows, quickbooks__general_ledger_by_period 759 rows) is the standard fivetran/qui… |
| recharge001 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | Target recharge__charge_line_item_history is a UNION of 4 charge sub-component types (charge line, discount, shipping, tax), 2 charges = 8 r… |
| retail001 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | Gold target report_customer_invoices defines total_invoices as COUNT(*) of fct_invoices LINE-ITEM rows per country (UK=354321), with total_r… |
| social_media001 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | The task ships an incomplete Fivetran social_media_reporting dbt package: only the facebook feeder model exists; the solver must author the … |
| superstore001 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | The two target models are absent as .sql files: models/ has dim_calendar/customers/geo/products/regions/shipping + fct_returns, but NOT dim_… |
| tpch001 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | Target table `client_purchase_status` (gold 75007 rows, 7 cols compared 0-6, ignore_orders). Baseline built 76777 rows with three value-defi… |
| twilio001 | VALUE_DEF | REACHABLE_VERIFIED | HIGH | The two target models use OPPOSITE sign conventions for message spend, and the baseline applied one convention to both. Twilio stores per-me… |
| movie_recomm001 | MISSING_COLUMN | REACHABLE_PROBABLE | HIGH | The eval contract compares one table, `user_watched_movies` (5 cols user_id/rating/title/OMDB_movie_id/movielens_genres, 56596 rows, ignore_… |
| quickbooks001 | MISSING_COLUMN | REACHABLE_PROBABLE | HIGH | The baseline got the row grain right (76 rows, matching gold) but built only a bare dbt_utils.union_relations() of the 12 double_entry model… |
| analytics_engineering001 | GRAIN_OVER_EMIT | NOT_REACHABLE_ORACLE | HIGH | Eval requires TWO target tables compared by column-containment (ignore_order=true): fact_purchase_order (gold 103 rows, condition_cols [0,1,… |
| pendo001 | GRAIN_OVER_EMIT | NOT_REACHABLE_ORACLE | HIGH | Both target tables (pendo__guide_daily_metrics, pendo__page_daily_metrics) are calendar-spine skeletons in the standard Pendo dbt package: s… |
| sap001 | MISSING_COLUMN | NOT_REACHABLE_ORACLE | HIGH | The two target tables sap__0fi_gl_10 (gold 204 rows x 32 cols) and sap__0fi_gl_14 (gold 3 rows x 174 cols) derive from three SAP GL raw fact… |
| asana001 | VALUE_DEF | NOT_REACHABLE_ORACLE | HIGH | Task = author the Fivetran asana package marts asana__team + asana__user (neither model ships in models/; only the asana_source staging pack… |
| atp_tour001 | VALUE_DEF | NOT_REACHABLE_ORACLE | HIGH | Multi-table text-to-dbt build: gold compares 3 target tables (dim_player, dim_tournament, rpt_match_summary) via per-column containment (ign… |
| scd001 | VALUE_DEF | NOT_REACHABLE_ORACLE | HIGH | Two final report models (fct_jafflegaggle, rpt_corporate_accounts) must be authored from scratch (they are absent from models/; only stg_* +… |
| chinook001 | VERIFIER | NOT_REACHABLE_ORACLE | HIGH | The gold DuckDB the verifier scores against contains NO answer tables. test.sh runs verify.py --gold-db /tests/chinook.duckdb; compare_duckd… |

> nba001 (42nd failed task) was not surveyed — schema retry cap; it is the frozen-Monte-Carlo-seed VALUE_DEF oracle wall (known NOT_REACHABLE).

_Method: dynamic workflow `spider2-dbt-resolution-survey` (run wf_32b5a457-a96), one agent per failed task, each reconstructing the target from SOURCE and running the verifier's own `duckdb_match.py` against gold offline (the left-shifted reachability check). Full per-task records: `resolution-survey-2026-06-25-pertask.json`._
