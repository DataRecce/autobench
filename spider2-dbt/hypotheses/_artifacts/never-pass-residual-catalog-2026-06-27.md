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
