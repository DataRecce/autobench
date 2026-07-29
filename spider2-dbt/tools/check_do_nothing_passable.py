#!/usr/bin/env python3
# ABOUTME: AC-6 floor check — grade each packaged view's UNBUILT source DuckDB against its own gold.
# ABOUTME: A view that already scores 1.0 with zero agent work is do-nothing-passable (a free point).
"""What does this board score if the agent does nothing?

Some spider2-dbt instances ship a source DuckDB that already satisfies their
``condition_tabs`` — the answer tables are present and gold-matching before any dbt
model is built. Those cells score 1.0 for an agent that touches nothing, and can
actively PENALISE an agent that rebuilds them. That is the board's floor, and a
submission's honest headline needs it stated.

The check is exactly the verifier's own comparison with the *pristine* source DB
substituted for the agent's built one:

    compare_duckdb(predicted_db=<view>/dbt_project/<db>.duckdb,
                   gold_db=<view>/tests/<gold>.duckdb,
                   spec=<view>/tests/spider2_eval.jsonl)

so a `PASSES_UNBUILT` verdict is a statement about razorback's real scoring path,
not a proxy for it.

Usage
-----
    python tools/check_do_nothing_passable.py --views _views
    python tools/check_do_nothing_passable.py --views _views --tasks inzight001,shopify001
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

VIEW_PREFIX = "spider2-dbt-"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--views", type=Path, required=True)
    ap.add_argument("--tasks", type=str, default=None, help="Comma-separated instance_ids.")
    args = ap.parse_args()

    from razorback.benchmarks.spider2_dbt.duckdb_match import compare_duckdb
    from razorback.benchmarks.spider2_dbt.eval_spec import load_eval_spec

    views = sorted(p for p in args.views.glob(f"{VIEW_PREFIX}*") if p.is_dir())
    if args.tasks:
        want = {t.strip() for t in args.tasks.split(",") if t.strip()}
        views = [v for v in views if v.name[len(VIEW_PREFIX):] in want]
    if not views:
        print(f"no matching views under {args.views}", file=sys.stderr)
        return 1

    passes: list[str] = []
    rows: list[tuple[str, str]] = []
    for view in views:
        instance = view.name[len(VIEW_PREFIX):]
        spec_path = view / "tests" / "spider2_eval.jsonl"
        if not spec_path.is_file():
            rows.append((instance, "NO_EVAL_SPEC"))
            continue
        spec = load_eval_spec(spec_path)
        gold = view / "tests" / (spec.gold or "")
        source_candidates = sorted((view / "dbt_project").glob("*.duckdb"))
        if not gold.is_file() or not source_candidates:
            rows.append((instance, "NO_GOLD" if not gold.is_file() else "NO_SOURCE_DB"))
            continue
        try:
            hit = compare_duckdb(
                predicted_db=source_candidates[0], gold_db=gold, spec=spec
            )
        except Exception as exc:  # noqa: BLE001
            rows.append((instance, f"ERROR {type(exc).__name__}: {exc}"))
            continue
        if hit:
            passes.append(instance)
            rows.append((instance, "PASSES_UNBUILT  <-- free point / penalises work"))
        else:
            rows.append((instance, "needs work"))

    for instance, verdict in rows:
        print(f"{instance:<36} {verdict}")
    print("\n==== DO-NOTHING FLOOR ====")
    print(f"views checked        : {len(rows)}")
    print(f"pass with zero work  : {len(passes)} — {', '.join(passes) if passes else '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
