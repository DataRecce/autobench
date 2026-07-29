#!/usr/bin/env python3
# ABOUTME: Validate a Spider2 submission bundle against the official instance list and the
# ABOUTME: format constraints upstream evaluate.py actually enforces — before uploading it.
"""Check a submission bundle the way ``evaluation_suite/evaluate.py`` will read it.

Checks (each prints PASS/FAIL with the offending items):

1. ``results_metadata.jsonl`` exists at the bundle root and is the ONLY ``*.jsonl``
   there. Upstream asserts exactly this:
   ``assert len(result_jsonl_files) == 1 and result_jsonl_files[0] == "results_metadata.jsonl"``.
2. Every line is a JSON object carrying exactly the three documented keys
   ``instance_id`` / ``answer_type`` / ``answer_or_path`` — no extras, none missing.
3. ``answer_type`` is ``"file"`` for every entry. Every spider2-dbt instance is
   ``duckdb_match``-scored, and upstream's ``"answer"`` branch calls
   ``max(temp_scores)`` over a list only populated for string/number matches — so
   ``"answer"`` on a duckdb instance raises and takes the whole run down.
4. Each ``answer_or_path`` resolves to an existing file at
   ``<bundle>/<instance_id>/<answer_or_path>``, and stays inside that folder
   (no absolute paths, no ``..`` traversal).
5. Instance-id set vs the official list from ``examples/spider2-dbt.jsonl``:
   no unknown ids, no duplicates, and the missing ones are reported explicitly.
   ``danish_democracy_data001`` is called out by name — it ships a gold dir but is
   NOT one of the official instances, so it must never appear in a submission.
6. Every submitted DuckDB opens and is readable (catches a truncated or
   half-written capture that would otherwise just score 0 with no explanation).

Exit code is 0 only when every check passes AND the submitted set equals the
official set (unless ``--expect`` lowers the bar deliberately).

Usage
-----
    python tools/validate_submission_bundle.py --bundle /path/to/bundle \\
        --spider2-root /home/kent/Spider2/spider2-dbt
    python tools/validate_submission_bundle.py --bundle ... --expect 64
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_KEYS = {"instance_id", "answer_type", "answer_or_path"}
OFF_LIST_GOLD = "danish_democracy_data001"


def _official_ids(spider2_root: Path) -> list[str]:
    path = spider2_root / "examples" / "spider2-dbt.jsonl"
    return [
        json.loads(line)["instance_id"]
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--spider2-root", type=Path, default=Path("/home/kent/Spider2/spider2-dbt"))
    ap.add_argument(
        "--expect",
        type=int,
        default=None,
        help="Expected entry count. Default: the official instance count (68).",
    )
    args = ap.parse_args()

    bundle: Path = args.bundle
    failures: list[str] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
        if not ok:
            failures.append(name)

    if not bundle.is_dir():
        print(f"bundle not found: {bundle}", file=sys.stderr)
        return 1

    official = _official_ids(args.spider2_root)
    expect = args.expect if args.expect is not None else len(official)

    # 1 — the metadata file, and only it
    jsonls = sorted(p.name for p in bundle.iterdir() if p.is_file() and p.name.endswith(".jsonl"))
    check(
        "1. exactly one root *.jsonl, named results_metadata.jsonl",
        jsonls == ["results_metadata.jsonl"],
        f"found {jsonls}",
    )
    meta = bundle / "results_metadata.jsonl"
    if not meta.is_file():
        print("\ncannot continue without results_metadata.jsonl", file=sys.stderr)
        return 1

    entries: list[dict] = []
    bad_lines: list[str] = []
    for n, line in enumerate(meta.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            bad_lines.append(f"line {n}: {exc}")
            continue
        if not isinstance(obj, dict):
            bad_lines.append(f"line {n}: not a JSON object")
            continue
        entries.append(obj)
    check("2a. every line parses as a JSON object", not bad_lines, "; ".join(bad_lines))

    # 2 — exact key set
    keyed_wrong = [
        f"{e.get('instance_id', '?')}: {sorted(set(e) ^ REQUIRED_KEYS)}"
        for e in entries
        if set(e) != REQUIRED_KEYS
    ]
    check("2b. every entry has exactly the 3 required keys", not keyed_wrong, "; ".join(keyed_wrong))

    # 3 — answer_type
    wrong_type = [
        f"{e.get('instance_id')}={e.get('answer_type')!r}"
        for e in entries
        if e.get("answer_type") != "file"
    ]
    check('3. answer_type == "file" everywhere', not wrong_type, "; ".join(wrong_type))

    # 4 — paths resolve, and stay inside the instance folder
    missing_paths: list[str] = []
    escaping: list[str] = []
    for e in entries:
        instance, rel = str(e.get("instance_id")), str(e.get("answer_or_path"))
        inst_dir = (bundle / instance).resolve()
        target = (inst_dir / rel).resolve()
        if Path(rel).is_absolute() or not str(target).startswith(str(inst_dir)):
            escaping.append(f"{instance}: {rel}")
            continue
        if not target.is_file():
            missing_paths.append(f"{instance}/{rel}")
    check("4a. every answer_or_path is a relative path inside its instance folder", not escaping, "; ".join(escaping))
    check("4b. every referenced artifact exists", not missing_paths, "; ".join(missing_paths))

    # 5 — instance-id set vs official
    ids = [str(e.get("instance_id")) for e in entries]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    unknown = sorted(set(ids) - set(official))
    missing = sorted(set(official) - set(ids))
    check("5a. no duplicate instance_ids", not dupes, ", ".join(dupes))
    check("5b. no ids outside the official list", not unknown, ", ".join(unknown))
    check(f"5c. {OFF_LIST_GOLD} absent (has gold, not official)", OFF_LIST_GOLD not in set(ids))
    check(
        f"5d. entry count == {expect}",
        len(entries) == expect,
        f"got {len(entries)}" + (f"; missing: {', '.join(missing)}" if missing else ""),
    )

    # 6 — every submitted DuckDB opens
    unreadable: list[str] = []
    try:
        import duckdb
    except ImportError:
        print("[SKIP] 6. DuckDB readability — duckdb not importable")
    else:
        for e in entries:
            instance, rel = str(e.get("instance_id")), str(e.get("answer_or_path"))
            target = bundle / instance / rel
            if not target.is_file():
                continue
            try:
                con = duckdb.connect(str(target), read_only=True)
                con.execute("select count(*) from information_schema.tables").fetchone()
                con.close()
            except Exception as exc:  # noqa: BLE001
                unreadable.append(f"{instance}: {type(exc).__name__}: {exc}")
        check("6. every submitted DuckDB opens and is queryable", not unreadable, "; ".join(unreadable))

    print("\n==== VALIDATION SUMMARY ====")
    print(f"bundle  : {bundle}")
    print(f"entries : {len(entries)} (official set: {len(official)}, expected: {expect})")
    if missing:
        print(f"missing : {len(missing)} — {', '.join(missing)}")
    print(f"failures: {len(failures)}" + (f" — {', '.join(failures)}" if failures else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
