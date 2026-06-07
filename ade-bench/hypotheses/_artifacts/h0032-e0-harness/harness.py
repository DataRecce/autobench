#!/usr/bin/env python3
"""
E0 / h0032 -- Instrument-validation harness.

For each candidate INDEPENDENT "second-path" SQL check that a downstream solver
hypothesis wants to rely on, prove it is *two-sided discriminating* on a
controlled fixture:

    fires-on-injected = TRUE  AND  fires-on-known-good = FALSE

A check that cannot fire on a known injected error is INERT (h0010/h0016 prose
signature). A check that fires on a known-good is CORRELATED / self-anchored
(h0008/h0012 signature). Either failure KILLS the check for its downstream
experiment.

The fixture is the real ade-bench f1 DuckDB (raw source tables + the canonical,
currently-PASSING @baseline model outputs ship side-by-side in the same file).
We treat the canonical model table as the KNOWN-GOOD, and build an INJECTED copy
by mutating it the way a realistic solver bug would (drop a parent key via an
added filter; cast a column to a wrong dtype; remove a required slice/model).

Every check recomputes from the RAW SOURCE table (native column names), never
from the model's own CTE / rename layer and never from the hidden `solution__*`
oracle seed -- that is the independence requirement (AC-2).

Output: a machine-readable 2x2 per check (result_2x2.json) + a printed table.
"""
import duckdb, json, shutil, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC_DB = HERE / "dbs" / "f1.duckdb"
SCRATCH = HERE / "dbs" / "f1.scratch.duckdb"
OUT = HERE / "result_2x2.json"

# fresh writable copy of the canonical fixture
shutil.copy(SRC_DB, SCRATCH)
con = duckdb.connect(str(SCRATCH))

results = []

def record(check_id, gates, model, good_fires, inj_fires, good_detail, inj_detail,
           independence, independence_note):
    cleared = (inj_fires is True) and (good_fires is False)
    results.append({
        "check_id": check_id,
        "gates_downstream": gates,
        "fixture_model": model,
        "fires_on_known_good": good_fires,      # want FALSE
        "fires_on_injected": inj_fires,         # want TRUE
        "known_good_detail": good_detail,
        "injected_detail": inj_detail,
        "two_sided_discriminating": cleared,
        "verdict": "CLEARED" if cleared else "KILLED",
        "kill_reason": (
            None if cleared else
            ("silent-on-injected => INERT" if inj_fires is not True else
             "fires-on-known-good => CORRELATED/self-anchored")
        ),
        "independence": independence,           # "independent" | "correlated" | "unavailable"
        "independence_note": independence_note,
    })

# ---------------------------------------------------------------------------
# CHECK 1 (PRIORITY -- gates E1/h0030):
#   RAW-PARENT ROW-COUNT RECONCILE
#   relation: output COUNT(*) == raw-parent COUNT(DISTINCT grain_key)
#   read raw `results`/`races` with NATIVE columns -- never the model CTE.
# ---------------------------------------------------------------------------
def reconcile_finishes_by_driver(model_tbl):
    out_n = con.execute(f"select count(*) from {model_tbl}").fetchone()[0]
    raw_n = con.execute('''
        select count(distinct r."driverId")
        from main.results r
        join main.drivers d on d."driverId" = r."driverId"
    ''').fetchone()[0]
    fired = (out_n != raw_n)
    return fired, {"output_count": out_n, "raw_parent_distinct": raw_n, "delta": out_n - raw_n}

# known-good == the canonical model table that ships in the fixture
con.execute("create or replace table good_finishes as select * from main.finishes_by_driver")
good_fires, good_d = reconcile_finishes_by_driver("good_finishes")

# injected error: a realistic solver bug -- an added WHERE that silently drops a
# parent-key cohort (here: drop every driver whose surname starts with 'H', i.e.
# Hamilton/Hill/Hakkinen/... -> grain shortfall). Build it the way a solver model
# would: from the staging layer + an extra filter, NOT by editing the raw source.
con.execute('''
  create or replace table inj_finishes as
  select fb.* from main.finishes_by_driver fb
  join main.drivers d on d."driverId" = fb.driver_id
  where d.surname not like 'H%'
''')
inj_fires, inj_d = reconcile_finishes_by_driver("inj_finishes")
record(
    "raw_parent_rowcount_reconcile", "E1/h0030", "finishes_by_driver",
    good_fires, inj_fires, good_d, inj_d,
    "independent",
    "Reconciles output COUNT(*) against COUNT(DISTINCT results.driverId) read "
    "from the RAW results+drivers tables (native cols); never reads the model's "
    "own CTE nor the solution__ oracle seed. Must-hold grain relation."
)

# ---------------------------------------------------------------------------
# CHECK 1b (corroborating, same instrument, second model -- gates E1/h0030):
#   driver_wins_by_season grain = distinct (driverId, year) with position=1
# ---------------------------------------------------------------------------
def reconcile_wins_by_season(model_tbl):
    out_n = con.execute(f"select count(*) from {model_tbl}").fetchone()[0]
    raw_n = con.execute('''
        select count(*) from (
          select distinct r."driverId", ra."year"
          from main.results r
          join main.races ra on r."raceId" = ra."raceId"
          where r."position" = 1)
    ''').fetchone()[0]
    fired = (out_n != raw_n)
    return fired, {"output_count": out_n, "raw_parent_distinct": raw_n, "delta": out_n - raw_n}

con.execute("create or replace table good_wins as select * from main.driver_wins_by_season")
gw_fires, gw_d = reconcile_wins_by_season("good_wins")
# injected: drop one season's worth of winning rows (remove year 2008) -> a
# "missing calendar slice" parent-key drop.
con.execute('''
  create or replace table inj_wins as
  select w.* from main.driver_wins_by_season w
  where w.season <> 2008
''')
iw_fires, iw_d = reconcile_wins_by_season("inj_wins")
record(
    "raw_parent_rowcount_reconcile__wins", "E1/h0030", "driver_wins_by_season",
    gw_fires, iw_fires, gw_d, iw_d,
    "independent",
    "Second model on the same instrument: distinct (driverId, year)|position=1 "
    "from RAW results+races. Injected drop = a whole season slice."
)

# ---------------------------------------------------------------------------
# CHECK 2 (gates E4): information_schema dtype assertion.
#   The entity asks for dtype-vs-DECLARED-CONTRACT. Finding: NO dbt project in
#   the ade-bench corpus declares `data_type:` or `contract: enforced` -- the
#   "declared contract" does not exist as an independent artifact (verified by
#   grep across shared/projects/dbt). So we validate the only INDEPENDENT dtype
#   relation available: model column dtype == RAW SOURCE column dtype for a
#   pass-through key column (driver_id should stay the raw driverId integer type).
# ---------------------------------------------------------------------------
def dtype_of(tbl, col):
    rows = con.execute(f"describe {tbl}").fetchall()
    for r in rows:
        if r[0] == col:
            return r[1]
    return None

raw_driverid_type = dtype_of("main.results", "driverId")   # raw source dtype (oracle)
def dtype_check_finishes(model_tbl):
    mt = dtype_of(model_tbl, "driver_id")
    # normalise duckdb integer family for the structural comparison
    fired = (str(mt).upper() != str(raw_driverid_type).upper())
    return fired, {"model_driver_id_type": mt, "raw_driverId_type": raw_driverid_type}

good_dt_fires, good_dt = dtype_check_finishes("good_finishes")
# injected: cast the key column to VARCHAR (a classic wrong-dtype solver bug)
con.execute('''
  create or replace table inj_finishes_dtype as
  select cast(driver_id as varchar) as driver_id,
         * exclude (driver_id)
  from main.finishes_by_driver
''')
inj_dt_fires, inj_dt = dtype_check_finishes("inj_finishes_dtype")
record(
    "info_schema_dtype_vs_raw_source", "E4", "finishes_by_driver.driver_id",
    good_dt_fires, inj_dt_fires, good_dt, inj_dt,
    "independent",
    "Compares model column dtype to the RAW source column dtype via "
    "information_schema/describe. NOTE: the entity's 'declared contract' variant "
    "is UNAVAILABLE -- no data_type:/contract: enforced anywhere in the corpus; "
    "deriving an 'expected' dtype from the model SQL would be CORRELATED. Only the "
    "raw-source-as-oracle variant is independent, and that is what is validated here."
)

# ---------------------------------------------------------------------------
# CHECK 3 (gates E5): ref-graph / _existence completeness.
#   Independent relation: every parent key present in the RAW SOURCE must appear
#   in the output (no silently dropped key). Recompute the required key-set from
#   RAW results+drivers, NOT from solution__ (oracle) nor the model CTE.
# ---------------------------------------------------------------------------
def completeness_check(model_tbl):
    # raw required key-set: every driverId that has a result and exists in drivers
    missing = con.execute(f'''
        select count(*) from (
          select distinct r."driverId" as k
          from main.results r
          join main.drivers d on d."driverId" = r."driverId"
        ) raw
        left join (select distinct driver_id as k from {model_tbl}) m
          on raw.k = m.k
        where m.k is null
    ''').fetchone()[0]
    fired = (missing > 0)
    return fired, {"raw_keys_missing_from_output": missing}

gc_fires, gc_d = completeness_check("good_finishes")
ic_fires, ic_d = completeness_check("inj_finishes")   # reuse the H% drop = missing keys
record(
    "ref_graph_existence_completeness", "E5", "finishes_by_driver",
    gc_fires, ic_fires, gc_d, ic_d,
    "independent",
    "Anti-join of the RAW-source required key-set against the output; fires if any "
    "raw parent key is absent. Reads raw results+drivers, never solution__ "
    "(the hidden oracle) nor the model CTE. This is the row-level dual of the count "
    "reconcile -- catches drops a count alone could mask (drop N + add N)."
)

# ---------------------------------------------------------------------------
# ADVERSARIAL probes -- not 2x2 rows; they characterise each check's blind spot
# so the independence verdict is earned, not assumed (the h0012 lesson).
# ---------------------------------------------------------------------------
adversarial = {}

# A) CORRELATED-ERROR trap for the reconcile: if the check read the SAME polluted
#    parent the output was built from (a solver-rebuilt intermediate) instead of
#    the immutable raw source, it would false-green. Proves independence is
#    load-bearing, not decorative.
con.execute('''create or replace table polluted_results as
               select * from main.results where "driverId" % 7 <> 0''')
out_corr = con.execute('''select count(distinct r."driverId") from polluted_results r
   join main.drivers d on d."driverId"=r."driverId"''').fetchone()[0]
corr_read = con.execute('''select count(distinct r."driverId") from polluted_results r
   join main.drivers d on d."driverId"=r."driverId"''').fetchone()[0]
indep_read = con.execute('''select count(distinct r."driverId") from main.results r
   join main.drivers d on d."driverId"=r."driverId"''').fetchone()[0]
adversarial["correlated_error_trap"] = {
    "polluted_output_distinct": out_corr,
    "correlated_read_matches_output": out_corr == corr_read,   # True => would FALSE-GREEN
    "independent_read_matches_output": out_corr == indep_read,  # False => correctly FIRES
    "lesson": "reconcile is sound ONLY if it reads the immutable raw source; reading a "
              "solver-rebuilt intermediate re-introduces the correlated error and false-greens.",
}

# B) COUNT blind spot vs completeness: drop-N-add-N keeps COUNT(*) equal, so the
#    count reconcile is blind, but the row-level completeness anti-join fires.
con.execute('''create or replace table out_swap as
  select driver_id from (select driver_id from main.finishes_by_driver order by driver_id limit 855)
  union all
  select 999000 + i as driver_id from range(5) t(i)''')
swap_n = con.execute("select count(*) from out_swap").fetchone()[0]
swap_missing = con.execute('''select count(*) from (
  select distinct r."driverId" k from main.results r
  join main.drivers d on d."driverId"=r."driverId") raw
  left join (select distinct driver_id k from out_swap) m on raw.k=m.k
  where m.k is null''').fetchone()[0]
adversarial["count_blind_spot"] = {
    "output_count": swap_n, "raw_distinct": indep_read,
    "count_reconcile_fires": swap_n != indep_read,        # False => count is BLIND
    "completeness_check_fires": swap_missing > 0,          # True  => existence catches it
    "lesson": "the count reconcile (E1) and the completeness anti-join (E5) are complementary: "
              "a drop-N-add-N bug is invisible to the count but caught by completeness.",
}

con.close()
SCRATCH.unlink(missing_ok=True)

OUT.write_text(json.dumps({"checks": results, "adversarial": adversarial}, indent=2))

# ---- print human table ----
print("\nE0 / h0032 instrument-validation 2x2\n" + "=" * 72)
hdr = f"{'check_id':<40}{'good':>6}{'inj':>6}  verdict"
print(hdr); print("-" * 72)
for r in results:
    print(f"{r['check_id']:<40}{str(r['fires_on_known_good']):>6}{str(r['fires_on_injected']):>6}  {r['verdict']}")
print("=" * 72)
for r in results:
    print(f"\n[{r['check_id']}] gates {r['gates_downstream']}  -> {r['verdict']}")
    print(f"   known-good (want fire=False): {r['known_good_detail']}  fired={r['fires_on_known_good']}")
    print(f"   injected   (want fire=True):  {r['injected_detail']}  fired={r['fires_on_injected']}")
    if r['kill_reason']:
        print(f"   KILL REASON: {r['kill_reason']}")
    print(f"   independence: {r['independence']}")
print("\nADVERSARIAL probes\n" + "-" * 72)
for k, v in adversarial.items():
    print(f"[{k}] {v}")
print(f"\nwrote {OUT}")
