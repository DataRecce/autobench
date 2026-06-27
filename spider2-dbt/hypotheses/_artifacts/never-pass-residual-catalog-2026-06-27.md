# Never-Pass Residual Catalog — 2026-06-27 (autonomous sprint capstone)

Per-task offline diagnosis (read-only: gold reconstructed from local source + champion spd0013 committed
artifact). Goal: for each never-pass cell, the EXACT residual + whether an oracle-free deterministic fix
exists. Verifier = per-column multiset containment, numeric tol 1e-2, AND across graded tables.

## Oracle-free DETERMINISTIC flip candidates (worth a narrow hypothesis)

| Task | Graded / gold grain | Exact residual | Oracle-free fix (general wording) | Prior-family? |
|---|---|---|---|---|
| **xero001** | `xero__balance_sheet_report` 1170 rows (account×month, cumulative balance) | champion spine runs to `current_date` (2026) → 1614 rows; gold ends at last activity month (2024-09) | "monthly spine ENDS at the last month with journal-line activity, not current_date; round net_amount to 2dp" | spine/spd0009 (clamp was tricky — undershot) |
| **movie_recomm001** | `user_watched_movies` 56596 rows (fan-out, NOT deduped) | champion used title EQUALITY + dedup-to-min-id → 9817; gold uses prefix `LIKE omdb_name\|\|'%'`, NO dedup | "when instruction underspecified, treat the model's schema.yml as authoritative; partial-title-match = prefix LIKE (not equality); preserve natural fan-out, no per-key dedup; strip only trailing (YYYY)" | NONE (novel) |
| **provider001** | `specialty_mapping` 874 + `provider` 85196 | champion INNER-joined crosswalk (460) + filtered NULL entity type (82339); gold LEFT-joins keep-all | "build from the full reference set via LEFT join; keep every row (NULL attribute where unmatched); never INNER-join-away or filter on a NULL key/type" | coverage/spd0004 (validated-not-promoted) |
| **nba001** | `season_summary` playoff-milestone cols (Monte-Carlo) | champion re-ran UNSEEDED `random()` sim (off by ~20); gold = committed snapshot parquet | "for stochastic playoff/championship milestone columns, read the committed season-summary snapshot parquet from the data catalog; never re-run an unseeded simulation" | NONE (novel) |
| flicks001 (`movie_actor_by_year` only) | 60983 rows | champion grained by actor_id + role filter (57585) | "INNER-join credits→movies over ALL roles; group by release_year+credit name; no_of_movie = COUNT(*)" | grain (partial — other table float-cusp blocked) |
| playbook002 (`cpa_and_roas` join-grain only) | 5 rows | champion INNER-joined ad_spend dropping 3 sources | "aggregate-then-join; never let a spend/dimension join filter the metric grain" | coverage (partial — model-choice oracle-blind) |

## ORACLE-BLIND / NOT pursuable (do not spend lever effort)

- **superstore001** — graded FKs are non-deterministic `ROW_NUMBER() OVER (order by null)` surrogate keys; per-row id assignment not reproducible from instruction+schema.
- **twilio001** — only residual is a per-TABLE sign convention (account spend +, number spend −); a fivetran-package convention not stated in the instruction (borderline/fragile).
- **playbook002 `cpa_and_roas` model choice** — gold uses LINEAR attribution though the `.yml` spec says 40/20/40 = a spec-vs-gold contradiction; only reading gold reveals it. Champion was correct per the documented spec.
- **flicks001 `actor_rating_by_total_movie`** — grain is oracle-free but 2 actors sit on a float-summation-order cusp just over 1e-2; no natural SQL reproduces gold's rounding. (atp_tour001/scd001/pendo001 = frozen-clock/row_number — prior survey NOT-reachable.)

## KEY CAVEAT (from spd0016/spd0018 + spd0013)

Even an EXACT, oracle-free, deterministic residual fix is **not guaranteed to flip the cell reliably** —
the worker's draw-to-draw SQL-shape variance dominates a single README clause (tickit002 = 2/4 across
draws despite a precise rule), and prohibition-style clauses can over-fire onto passers (spd0018 regressed
google_play001). POSITIVE directives ("do X this way") may steer more reliably than prohibitions
("don't do Y"). Reliability requires a 2+-draw smoke check, and a true fix likely needs the heavier
contract forcing-function (spd0013) to be obeyed consistently — which carries its own cost. So: these are
the best LEADS, not guaranteed flips.

## Recommended next bets (positive-directive, deterministic)
1. **movie_recomm001** — prefix-LIKE-no-dedup join (novel mechanism, clean directive).
2. **xero001** — spine-ends-at-last-activity-month (high-value, but confirm it beats spd0009's clamp issue).
3. **provider001** — LEFT-join-preserve-all-rows (clean, 2 cells; coverage family — may need a sharper directive than spd0004's).
4. **nba001** — read-the-snapshot-parquet (novel; compliance-risky — worker must choose the snapshot over simulating).

---

## Catalog extension (2026-06-27, batches A+B — 15 more cells diagnosed)

### Batch A (Q1 family)
| Task | Reachable? | Fix class | Fix |
|---|---|---|---|
| asana001 | YES | deterministic oracle-free | drive FROM entity dim, LEFT-JOIN metrics; keep all entities (C1 family) |
| intercom001 | YES | deterministic oracle-free | full dim row set, LEFT-attach aggregates not INNER (C1 family) |
| netflix001 | YES | deterministic oracle-free | keep all rows; emit date-parts as typed strings; clean only the named title col |
| reddit001 | PARTIAL | comments oracle-free / posts ORACLE-BLIND | left-attach + emit macro hour cols; lone-2022-row drop unreachable |
| social_media001 | YES | deterministic oracle-free | cast id to varchar before split_part; don't quote col/delim (NEW C6) |
| zuora001 | YES | VARIANCE-prone | carry account_id from invoice spine, not min() from a sibling dim |
| xero_new001 | YES | deterministic oracle-free | author all 3 models (champion authored none); balance sheet = forward-carry over full spine + equity roll-ups (C2 + C7) |

### Batch B (mixed)
| Task | Reachable? | Fix class | Fix |
|---|---|---|---|
| hive001 | YES | deterministic oracle-free | INNER JOIN cases→country-codes on geo_id=alpha_2code, keep fanout (no dedupe) (C1 family) |
| synthea001 | YES | deterministic oracle-free | author missing `cost` model = UNION ALL of int__cost_* (champion errored, never built) (NEW C7) |
| quickbooks001 | YES (fragile) | VARIANCE-prone | dbt_utils surrogate-key recipe + deterministic running_balance tiebreak |
| tpch001 | NO | ORACLE-BLIND | status thresholds + NULL bucket + return_pct scale + zero-purchase filter only in gold |
| xero_new002 | YES | deterministic oracle-free | Retained Earnings = cumulative P&L to month_end; drop FY-end pin + Current-Year-Earnings split (C2 family) |
| atp_tour001 | NO | ORACLE-BLIND frozen-clock | age = run_started_at − dob, frozen at 2024 |
| scd001 | NO (partial) | pool deterministic; tiebreak ORACLE-BLIND | corporate-only pool fixes first_user; most_active/most_orders tie irreproducible |
| pendo001 | NO | ORACLE-BLIND frozen-clock | guide date_day bound = current_date (2024-09-08) |

### Consolidated reachable-deterministic lead set (~13 cells, by template family)
- **C1 entity/reference-completeness** (LEFT-attach, keep full base-set, keep fanout, no INNER-from-aggregate): provider001, asana001, intercom001, netflix001, reddit001(comments), hive001.
- **C2 cumulative balance-sheet spine** (spine ends at last activity; Retained Earnings = cumulative P&L): xero001, xero_new001, xero_new002.
- **C3 fuzzy/partial name-match**: movie_recomm001.
- **C4 no-invented-filter dim/fact**: tickit002.
- **C5 stochastic-simulation snapshot**: nba001.
- **C6 cast-before-string-op** (NEW): social_media001.
- **C7 author-the-missing-graded-model** (NEW; esp. UNION of sibling int_ models): synthea001, xero_new001.
- Variance-prone (exclude from contract, note): zuora001, quickbooks001.
- ORACLE-BLIND / frozen-clock (dead): tpch001, atp_tour001, pendo001, scd001, superstore001, twilio001, playbook002-model, flicks001-actor_rating, reddit001-posts.
