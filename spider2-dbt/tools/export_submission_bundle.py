#!/usr/bin/env python3
# ABOUTME: Turn a razorback spider2-dbt run-dir into an upstream Spider2 submission bundle:
# ABOUTME: results_metadata.jsonl + <instance_id>/predicted.duckdb, per evaluation_suite/README.md.
"""Export a razorback run-dir as a Spider2 leaderboard submission bundle.

Bundle layout (``evaluation_suite/README.md``)::

    <bundle>/
      results_metadata.jsonl        # one JSON object per instance
      <instance_id>/predicted.duckdb
      ...

``results_metadata.jsonl`` entries carry exactly the three documented keys::

    {"instance_id": ..., "answer_type": "file", "answer_or_path": "predicted.duckdb"}

Every spider2-dbt instance is scored by ``duckdb_match`` (all 68 lines of
``evaluation_suite/gold/spider2_eval.jsonl`` use it), so ``answer_type`` is always
``"file"``. That matters: upstream's ``evaluate.py`` handles ``answer_type ==
"answer"`` by building ``temp_scores`` only for ``string_match`` / ``number_match``
and then calling ``max(temp_scores)`` — for a ``duckdb_match`` instance the list
stays empty and ``max([])`` raises, crashing the whole evaluation. ``"file"`` is
the only correct value here.

Source artifact
---------------
The per-instance file comes from ``<cell>/verifier/predicted.duckdb``, which only
exists if the view's ``tests/test.sh`` was patched by
``tools/add_predicted_db_capture.py`` BEFORE the run. Vanilla razorback keeps no
copy of the agent's DuckDB, so a run made without that patch cannot be exported —
this tool reports each such instance as ``MISSING_ARTIFACT`` rather than emitting a
bundle with dangling paths.

Instance identity comes from each cell's ``config.json`` -> ``task.path`` (the
materialized view dir), NOT from the trial directory name: harbor truncates long
trial names (``spider2-dbt-analytics_engineerin__irCLDMC``), so parsing the
directory would silently mangle instance ids.

Usage
-----
    python tools/export_submission_bundle.py \\
        --run-dir runs/<experiment>/<hash> --out /path/to/bundle
    # optional: emit an EMPTY placeholder DuckDB for instances that never ran, so
    # the leaderboard's denominator stays the full official set instead of
    # silently shrinking to what we managed to submit.
    python tools/export_submission_bundle.py ... --placeholder-for gitcoin001
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

VIEW_PREFIX = "spider2-dbt-"
ARTIFACT_NAME = "predicted.duckdb"


def _instance_id(cell: Path) -> str | None:
    """Instance id for a trial cell, from config.json -> task.path (truncation-proof)."""
    config = cell / "config.json"
    if not config.is_file():
        return None
    try:
        task_path = json.loads(config.read_text())["task"]["path"]
    except Exception:
        return None
    name = Path(task_path).name
    return name[len(VIEW_PREFIX):] if name.startswith(VIEW_PREFIX) else name


def _reward(cell: Path) -> float | None:
    reward_json = cell / "verifier" / "reward.json"
    if not reward_json.is_file():
        return None
    try:
        return float(json.loads(reward_json.read_text())["reward"])
    except Exception:
        return None


def _empty_duckdb(path: Path) -> None:
    """Create a valid, EMPTY DuckDB file (no tables).

    Used only for ``--placeholder-for``. ``duckdb_match`` fetches each
    ``condition_tabs`` table from the result DB inside a try/except and returns 0
    on failure, so an empty DB scores 0 — it can never accidentally match. It
    exists purely so the instance still appears in the submission and the
    leaderboard's denominator is not reduced by our omission.
    """
    import duckdb

    con = duckdb.connect(str(path))
    con.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True, help="runs/<experiment>/<hash>")
    ap.add_argument("--out", type=Path, required=True, help="Bundle dir to create.")
    ap.add_argument(
        "--placeholder-for",
        type=str,
        default="",
        help="Comma-separated instance_ids to include with an EMPTY result DuckDB "
        "(instances that could not be run). Scores 0; keeps the denominator honest.",
    )
    ap.add_argument(
        "--copy-mode",
        choices=("copy", "hardlink"),
        default="hardlink",
        help="hardlink (default, instant, same filesystem) or copy the DuckDB files.",
    )
    args = ap.parse_args()

    run_dir: Path = args.run_dir
    if not run_dir.is_dir():
        print(f"run-dir not found: {run_dir}", file=sys.stderr)
        return 1

    cells = sorted(p for p in run_dir.iterdir() if p.is_dir() and (p / "config.json").is_file())
    if not cells:
        print(f"no trial cells under {run_dir}", file=sys.stderr)
        return 1

    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    entries: list[dict] = []
    rows: list[tuple[str, str, str]] = []  # (instance, status, detail)
    seen: set[str] = set()

    for cell in cells:
        instance = _instance_id(cell)
        if instance is None:
            rows.append((cell.name, "FAIL", "cannot resolve instance_id from config.json"))
            continue
        if instance in seen:
            rows.append((instance, "FAIL", f"duplicate cell {cell.name} (trials>1 is unsupported)"))
            continue
        seen.add(instance)

        artifact = cell / "verifier" / ARTIFACT_NAME
        reward = _reward(cell)
        reward_text = "n/a" if reward is None else f"{reward:g}"
        if not artifact.is_file():
            rows.append(
                (instance, "MISSING_ARTIFACT", f"no verifier/{ARTIFACT_NAME} (reward {reward_text})")
            )
            continue

        dest_dir = out / instance
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / ARTIFACT_NAME
        if dest.exists():
            dest.unlink()
        if args.copy_mode == "hardlink":
            try:
                dest.hardlink_to(artifact)
            except OSError:
                shutil.copy2(artifact, dest)
        else:
            shutil.copy2(artifact, dest)
        entries.append(
            {"instance_id": instance, "answer_type": "file", "answer_or_path": ARTIFACT_NAME}
        )
        rows.append((instance, "ok", f"reward {reward_text}, {dest.stat().st_size} bytes"))

    for instance in [t.strip() for t in args.placeholder_for.split(",") if t.strip()]:
        if instance in seen:
            rows.append((instance, "FAIL", "--placeholder-for names an instance that DID run"))
            continue
        dest_dir = out / instance
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / ARTIFACT_NAME
        if dest.exists():
            dest.unlink()
        _empty_duckdb(dest)
        entries.append(
            {"instance_id": instance, "answer_type": "file", "answer_or_path": ARTIFACT_NAME}
        )
        rows.append((instance, "placeholder", "EMPTY result DuckDB — scores 0 by construction"))

    entries.sort(key=lambda e: e["instance_id"])
    (out / "results_metadata.jsonl").write_text(
        "".join(json.dumps(e) + "\n" for e in entries)
    )

    print(f"{'instance':<36} {'status':<18} detail")
    for instance, status, detail in sorted(rows):
        print(f"{instance:<36} {status:<18} {detail}")
    ok = sum(1 for _, s, _ in rows if s == "ok")
    ph = sum(1 for _, s, _ in rows if s == "placeholder")
    bad = [(i, s, d) for i, s, d in rows if s not in ("ok", "placeholder")]
    print("\n==== EXPORT SUMMARY ====")
    print(f"bundle              : {out}")
    print(f"results_metadata.jsonl entries: {len(entries)}  (exported {ok}, placeholder {ph})")
    print(f"not exported        : {len(bad)}")
    for instance, status, detail in bad:
        print(f"   - {instance}: {status} — {detail}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
