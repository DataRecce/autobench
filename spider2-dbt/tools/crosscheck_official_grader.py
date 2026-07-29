#!/usr/bin/env python3
# ABOUTME: AC-4 — grade with the OFFICIAL Spider2 eval_utils.duckdb_match and reconcile against
# ABOUTME: razorback's own comparator. Two modes: differential fuzz (no run needed) and bundle grading.
"""Is razorback's grader the same test as the leaderboard's?

razorback scores spider2-dbt with its own ``compare_duckdb``
(``razorback/benchmarks/spider2_dbt/duckdb_match.py``), documented as a faithful
port of Spider2's ``eval_utils.duckdb_match``. "Documented as" is not "verified
as": if the two diverge, every score this workflow has ever recorded was measured
against a grader that is not the leaderboard's. This tool checks it by running the
UPSTREAM code itself, not a re-transcription.

Importing upstream ``eval_utils`` requires ``google.cloud.bigquery``, used only by
``get_bigquery_sql_result`` — irrelevant to ``duckdb_match``. Rather than install a
cloud SDK, a stub module is injected for that one import so the graded code path is
upstream's own unmodified bytes.

Modes
-----
``--fuzz N``      Differential test on N generated table pairs. Builds a random
                  gold/pred DuckDB pair per case (integers, floats, strings, NULLs,
                  DECIMALs, dates, empty tables, column permutations, extra pred
                  columns, row shuffles, and float perturbations straddling the
                  1e-2 tolerance), grades each with BOTH comparators, and reports
                  any case where the verdicts differ. Needs no run and no bundle —
                  this is the check that can be run before committing 4 GPU-hours.

``--bundle DIR``  Grade a real submission bundle with upstream ``duckdb_match``
                  against ``evaluation_suite/gold/`` and reconcile per instance
                  against the razorback rewards in ``--run-dir``. Prints one row per
                  instance and an explicit list of disagreements.

Usage
-----
    python tools/crosscheck_official_grader.py --fuzz 400
    python tools/crosscheck_official_grader.py --bundle /path/to/bundle \\
        --run-dir runs/<experiment>/<hash>
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import types
from pathlib import Path

DEFAULT_SPIDER2_ROOT = Path("/home/kent/Spider2/spider2-dbt")


def load_official_duckdb_match(spider2_root: Path):
    """Import the UPSTREAM eval_utils and return its `duckdb_match`.

    Stubs `google.cloud.bigquery` (module-level import in eval_utils, used only by
    the BigQuery helper) so the real file imports unmodified.
    """
    if "google.cloud.bigquery" not in sys.modules:
        google = sys.modules.setdefault("google", types.ModuleType("google"))
        cloud = sys.modules.setdefault("google.cloud", types.ModuleType("google.cloud"))
        bigquery = types.ModuleType("google.cloud.bigquery")
        bigquery.Client = object  # never called on the duckdb_match path
        sys.modules["google.cloud.bigquery"] = bigquery
        google.cloud = cloud
        cloud.bigquery = bigquery
    suite = str(spider2_root / "evaluation_suite")
    if suite not in sys.path:
        sys.path.insert(0, suite)
    import eval_utils  # noqa: PLC0415 — deliberate late import of upstream code

    return eval_utils.duckdb_match


def load_razorback_compare():
    from razorback.benchmarks.spider2_dbt.duckdb_match import compare_duckdb
    from razorback.benchmarks.spider2_dbt.eval_spec import EvalSpec

    return compare_duckdb, EvalSpec


# ---------------------------------------------------------------- fuzz mode


_SQL_TYPES = ("INTEGER", "BIGINT", "DOUBLE", "VARCHAR", "DECIMAL(12,3)", "DATE", "BOOLEAN")


def _random_value(rng: random.Random, sql_type: str, *, nullable: bool):
    if nullable and rng.random() < 0.15:
        return "NULL"
    if sql_type in ("INTEGER", "BIGINT"):
        return str(rng.randint(-1000, 1000))
    if sql_type == "DOUBLE":
        return repr(round(rng.uniform(-1000, 1000), 4))
    if sql_type == "DECIMAL(12,3)":
        return repr(round(rng.uniform(-1000, 1000), 3))
    if sql_type == "VARCHAR":
        return "'" + rng.choice(["alpha", "beta", "gamma", "", "Türkiye", "o'brien".replace("'", "''")]) + "'"
    if sql_type == "DATE":
        return f"DATE '20{rng.randint(10, 24)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}'"
    if sql_type == "BOOLEAN":
        return rng.choice(("TRUE", "FALSE"))
    raise AssertionError(sql_type)


def _write_table(con, table: str, types_: list[str], rows: list[list[str]]) -> None:
    cols = ", ".join(f'"c{i}" {t}' for i, t in enumerate(types_))
    con.execute(f'CREATE TABLE "{table}" ({cols})')
    for row in rows:
        con.execute(f'INSERT INTO "{table}" VALUES ({", ".join(row)})')


def _fuzz_case(rng: random.Random, tmp: Path, index: int) -> dict:
    """Build one gold/pred DuckDB pair plus its eval parameters."""
    ntabs = rng.choice((1, 1, 2))
    tabs = [f"t{j}" for j in range(ntabs)]
    ncols = [rng.randint(1, 5) for _ in tabs]
    nrows = [rng.choice((0, 1, 3, 7)) for _ in tabs]

    gold_path = tmp / f"gold{index}.duckdb"
    pred_path = tmp / f"pred{index}.duckdb"
    for p in (gold_path, pred_path):
        p.unlink(missing_ok=True)

    import duckdb

    gcon = duckdb.connect(str(gold_path))
    pcon = duckdb.connect(str(pred_path))
    condition_cols: list[list[int]] = []
    ignore_orders: list[bool] = []
    try:
        for t, nc, nr in zip(tabs, ncols, nrows):
            types_ = [rng.choice(_SQL_TYPES) for _ in range(nc)]
            gold_rows = [[_random_value(rng, ty, nullable=True) for ty in types_] for _ in range(nr)]
            _write_table(gcon, t, types_, gold_rows)

            mode = rng.choice(
                (
                    "identical",
                    "identical",
                    "shuffled",
                    "extra_pred_col",
                    "perturb_small",
                    "perturb_large",
                    "row_dropped",
                    "missing_table",
                    "value_changed",
                )
            )
            pred_types, pred_rows = list(types_), [list(r) for r in gold_rows]
            if mode == "shuffled":
                rng.shuffle(pred_rows)
            elif mode == "extra_pred_col":
                pred_types.append("VARCHAR")
                for r in pred_rows:
                    r.append("'extra'")
            elif mode in ("perturb_small", "perturb_large") and pred_rows:
                delta = 0.001 if mode == "perturb_small" else 5.0
                for r in pred_rows:
                    for ci, ty in enumerate(pred_types):
                        if ty in ("DOUBLE", "DECIMAL(12,3)") and r[ci] != "NULL":
                            r[ci] = repr(float(r[ci]) + delta)
            elif mode == "row_dropped" and pred_rows:
                pred_rows.pop()
            elif mode == "value_changed" and pred_rows:
                r = pred_rows[rng.randrange(len(pred_rows))]
                ci = rng.randrange(len(pred_types))
                r[ci] = _random_value(rng, pred_types[ci], nullable=False)

            if mode != "missing_table":
                _write_table(pcon, t, pred_types, pred_rows)

            picked = sorted(rng.sample(range(nc), rng.randint(1, nc))) if rng.random() < 0.6 else []
            condition_cols.append(picked)
            ignore_orders.append(rng.random() < 0.5)
    finally:
        gcon.close()
        pcon.close()

    return {
        "gold": gold_path,
        "pred": pred_path,
        "condition_tabs": tabs,
        "condition_cols": condition_cols,
        "ignore_orders": ignore_orders,
    }


def run_fuzz(n: int, spider2_root: Path, seed: int) -> int:
    official = load_official_duckdb_match(spider2_root)
    compare_duckdb, EvalSpec = load_razorback_compare()
    rng = random.Random(seed)

    import tempfile

    disagreements: list[str] = []
    agree_1 = agree_0 = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for i in range(n):
            case = _fuzz_case(rng, tmp, i)
            try:
                up = int(
                    official(
                        str(case["pred"]),
                        str(case["gold"]),
                        condition_tabs=case["condition_tabs"],
                        condition_cols=case["condition_cols"],
                        ignore_orders=case["ignore_orders"],
                    )
                )
            except Exception as exc:  # upstream's gold fetch is NOT wrapped
                up = f"RAISED {type(exc).__name__}"
            spec = EvalSpec(
                gold=case["gold"].name,
                condition_tabs=case["condition_tabs"],
                condition_cols=case["condition_cols"],
                ignore_orders=case["ignore_orders"],
            )
            try:
                rb = int(
                    compare_duckdb(predicted_db=case["pred"], gold_db=case["gold"], spec=spec)
                )
            except Exception as exc:
                rb = f"RAISED {type(exc).__name__}"
            if up != rb:
                disagreements.append(
                    f"case {i}: upstream={up} razorback={rb} tabs={case['condition_tabs']} "
                    f"cols={case['condition_cols']} ignore={case['ignore_orders']}"
                )
            elif up == 1:
                agree_1 += 1
            else:
                agree_0 += 1

    print("==== DIFFERENTIAL FUZZ ====")
    print(f"cases            : {n} (seed {seed})")
    print(f"agree on MATCH   : {agree_1}")
    print(f"agree on MISMATCH: {agree_0}")
    print(f"DISAGREEMENTS    : {len(disagreements)}")
    for line in disagreements[:40]:
        print(f"   - {line}")
    if agree_1 == 0:
        print("WARNING: no case matched — the fuzz never exercised the agree-on-MATCH branch.")
        return 1
    return 1 if disagreements else 0


# -------------------------------------------------------------- bundle mode


def _run_dir_rewards(run_dir: Path) -> dict[str, float]:
    rewards: dict[str, float] = {}
    for cell in sorted(p for p in run_dir.iterdir() if p.is_dir()):
        config, reward_json = cell / "config.json", cell / "verifier" / "reward.json"
        if not (config.is_file() and reward_json.is_file()):
            continue
        try:
            name = Path(json.loads(config.read_text())["task"]["path"]).name
            instance = name.removeprefix("spider2-dbt-")
            rewards[instance] = float(json.loads(reward_json.read_text())["reward"])
        except Exception:
            continue
    return rewards


def run_bundle(bundle: Path, run_dir: Path | None, spider2_root: Path) -> int:
    official = load_official_duckdb_match(spider2_root)
    gold_root = spider2_root / "evaluation_suite" / "gold"
    specs = {
        json.loads(line)["instance_id"]: json.loads(line)
        for line in (gold_root / "spider2_eval.jsonl").read_text().splitlines()
        if line.strip()
    }
    rewards = _run_dir_rewards(run_dir) if run_dir else {}

    entries = [
        json.loads(line)
        for line in (bundle / "results_metadata.jsonl").read_text().splitlines()
        if line.strip()
    ]
    print(f"{'instance':<36} {'official':>9} {'razorback':>10}  note")
    disagree: list[str] = []
    ungradeable: list[str] = []
    for entry in sorted(entries, key=lambda e: e["instance_id"]):
        instance = entry["instance_id"]
        result = bundle / instance / entry["answer_or_path"]
        spec = specs.get(instance)
        rb = rewards.get(instance)
        rb_text = "n/a" if rb is None else f"{rb:g}"
        if spec is None:
            print(f"{instance:<36} {'-':>9} {rb_text:>10}  NO OFFICIAL EVAL LINE")
            ungradeable.append(f"{instance}: no eval line")
            continue
        params = dict(spec["evaluation"]["parameters"])
        gold_file = gold_root / instance / params.pop("gold")
        if not gold_file.is_file():
            print(f"{instance:<36} {'-':>9} {rb_text:>10}  NO LOCAL GOLD (leaderboard-only)")
            ungradeable.append(f"{instance}: no local gold")
            continue
        try:
            up = int(official(str(result), str(gold_file), **params))
        except Exception as exc:  # noqa: BLE001
            up = 0
            print(f"{instance:<36} {up:>9} {rb_text:>10}  upstream raised {type(exc).__name__}")
        else:
            note = ""
            if rb is not None and int(rb) != up:
                note = "*** DISAGREE ***"
                disagree.append(f"{instance}: official={up} razorback={rb:g}")
            print(f"{instance:<36} {up:>9} {rb_text:>10}  {note}")

    print("\n==== CROSS-CHECK SUMMARY ====")
    print(f"entries        : {len(entries)}")
    print(f"not gradeable locally: {len(ungradeable)}")
    for line in ungradeable:
        print(f"   - {line}")
    print(f"DISAGREEMENTS  : {len(disagree)}")
    for line in disagree:
        print(f"   - {line}")
    return 1 if disagree else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--spider2-root", type=Path, default=DEFAULT_SPIDER2_ROOT)
    ap.add_argument("--fuzz", type=int, default=0, help="Run N differential fuzz cases.")
    ap.add_argument("--seed", type=int, default=20260729)
    ap.add_argument("--bundle", type=Path, default=None)
    ap.add_argument("--run-dir", type=Path, default=None)
    args = ap.parse_args()

    if args.fuzz:
        return run_fuzz(args.fuzz, args.spider2_root, args.seed)
    if args.bundle:
        return run_bundle(args.bundle, args.run_dir, args.spider2_root)
    ap.error("pass --fuzz N or --bundle DIR")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
