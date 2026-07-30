#!/usr/bin/env python3
# ABOUTME: Patch packaged spider2-dbt task views so the verifier ALSO persists the agent's
# ABOUTME: built /app/<db>.duckdb to /logs/verifier/predicted.duckdb — the artifact a
# ABOUTME: leaderboard submission bundle is made of. Reward semantics are untouched.
"""Make the predicted DuckDB survive the run.

Why this is needed
------------------
A razorback run-dir carries NO copy of the DuckDB the agent built. The emitted
``tests/test.sh`` runs the verifier INSIDE the task container against
``/app/<db>.duckdb`` and only ``/logs/verifier/reward.json`` reaches the host;
the container is then torn down (``docker compose down --volumes``) and the
predicted database is gone. So a submission bundle cannot be reconstructed from
any completed run, however clean.

Harbor bind-mounts the container's logs dir to the host trial dir (see
``harbor/environments/docker/docker.py`` -> ``prepare_logs_for_host``, which
chowns the *bind-mounted* logs directory back to the host user). That is why
``<cell>/verifier/reward.json`` appears on the host: it is the same file the
verifier wrote to ``/logs/verifier/reward.json``. Anything else written there
lands on the host too, at full size, with no copy step and no size cap.

What this does
--------------
Rewrites each view's ``tests/test.sh`` to copy ``/app/<db>.duckdb`` to
``/logs/verifier/predicted.duckdb`` BEFORE invoking the verifier, keeping the
verifier invocation byte-identical. Effects:

* the reward is computed from exactly the same file as before -> no grading change;
* the copy happens before ``verify.py``, so an unreadable/absent predicted DB
  still reaches the verifier's own "predicted DB not found" path (reward 0);
* the ``cp`` is best-effort (``|| true``): a failed copy must never turn a
  passing cell into an error. A missing ``predicted.duckdb`` is then a bundle-time
  gap the exporter reports, not a corrupted score.

``tests/`` is uploaded to the container only at verify time and is NOT part of the
Docker build context (``environment/``), so patching it changes nothing the agent
sees and does not invalidate any image layer. Idempotent: guarded by a marker.

Usage
-----
    python tools/add_predicted_db_capture.py --views _views            # patch all
    python tools/add_predicted_db_capture.py --views _views --check    # report only
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MARKER = "# razorback-spider2: persist the predicted DuckDB for submission export"

_CAPTURE_TEMPLATE = """{marker}
cp {predicted_db} /logs/verifier/predicted.duckdb || true
"""

# `--predicted-db <path>` as emitted by razorback's _TEST_SH_TEMPLATE (shlex-quoted).
_PREDICTED_RE = re.compile(r"^\s*--predicted-db\s+(\S+)\s*\\?\s*$", re.M)


def _predicted_db_arg(text: str) -> str | None:
    """The `--predicted-db` value already in this test.sh.

    Reusing the emitted argument means we never re-resolve the DuckDB stem: the
    captured file is by construction the exact one the verifier scores.
    """
    hits = _PREDICTED_RE.findall(text)
    return hits[0] if len(hits) == 1 else None


def patch_view(view: Path, *, check: bool) -> tuple[str, str]:
    """Return (status, detail) for one view dir. Status is one of
    ok / already / skip / FAIL."""
    test_sh = view / "tests" / "test.sh"
    if not test_sh.is_file():
        return "skip", "no tests/test.sh"
    text = test_sh.read_text()
    if MARKER in text:
        return "already", "marker present"
    if "NO_LOCAL_GOLD" in text:
        # razorback's record-only verifier (no local gold) already captures the
        # predicted DuckDB to the same path and scores a deterministic 0.0. There is
        # no `--predicted-db` argument to key off and nothing to add.
        return "skip", "record-only view — already captures predicted.duckdb"
    predicted = _predicted_db_arg(text)
    if predicted is None:
        return "FAIL", "could not find exactly one --predicted-db argument"
    if "python /tests/verify.py" not in text:
        return "FAIL", "test.sh does not invoke /tests/verify.py"

    block = _CAPTURE_TEMPLATE.format(marker=MARKER, predicted_db=predicted)
    # Insert immediately before the verifier invocation, after `mkdir -p /logs/verifier`
    # so the destination directory already exists.
    anchor = "python /tests/verify.py"
    patched = text.replace(anchor, block + anchor, 1)
    if check:
        return "ok", f"would capture {predicted}"
    if test_sh.is_symlink():  # never write through a link-mode reflection
        test_sh.unlink()
        test_sh.write_text(patched)
    else:
        test_sh.write_text(patched)
    test_sh.chmod(0o755)
    return "ok", f"captures {predicted}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--views", type=Path, required=True, help="Root holding spider2-dbt-* views.")
    ap.add_argument("--check", action="store_true", help="Report what would change; write nothing.")
    args = ap.parse_args()

    views = sorted(p for p in args.views.glob("spider2-dbt-*") if p.is_dir())
    if not views:
        print(f"no spider2-dbt-* views under {args.views}", file=sys.stderr)
        return 1

    counts: dict[str, int] = {}
    failures: list[tuple[str, str]] = []
    for view in views:
        status, detail = patch_view(view, check=args.check)
        counts[status] = counts.get(status, 0) + 1
        if status == "FAIL":
            failures.append((view.name, detail))
            print(f"[FAIL] {view.name}: {detail}", file=sys.stderr)

    print(f"\n==== {'CHECK' if args.check else 'PATCH'} SUMMARY ====")
    print(f"views       : {len(views)}")
    for status in ("ok", "already", "skip", "FAIL"):
        if status in counts:
            print(f"{status:<12}: {counts[status]}")
    for name, detail in failures:
        print(f"   - {name}: {detail}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
