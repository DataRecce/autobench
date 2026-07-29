#!/usr/bin/env python3
# ABOUTME: Size the "fixture-deficient project" exposure across packaged views — models that call
# ABOUTME: macros from a dbt package that is neither vendored under dbt_packages/ nor declared.
"""Which views ask the solver to build against a package that isn't there?

Why this exists
---------------
`activity001` passed 50 of 51 lifetime runs and then scored 0.0 in spd0043's smoke. The cause was not
infrastructure: its models call `dbt_activity_schema.*` macros, that package is absent from
`dbt_packages/`, and the project ships no `packages.yml` or `dependencies.yml`. The solver's stated
blocker was factually correct. What changed was its disposition — earlier runs worked around the
deficient fixture and built the targets anyway; this run declined to and abstained.

That makes the deficiency a submission-wide risk rather than one canary: any view with the same shape
can flip the same way, depending on whether the solver decides to work around it. This tool measures how
many are exposed.

What it flags, per view
----------------------
* ``UNRESOLVED_NS``  — a model or project macro references ``<ns>.<macro>`` where ``<ns>`` is neither a
  Jinja/dbt builtin nor a directory under ``dbt_packages/``. This is the activity001 shape.
* ``DECLARED_NOT_VENDORED`` — ``packages.yml``/``dependencies.yml`` names a package with no
  corresponding ``dbt_packages/`` directory. The container is offline, so `dbt deps` cannot fetch it.
* ``VENDORED_UNDECLARED`` — a package is vendored but no manifest declares it. Benign for building
  (dbt loads by presence) but it is the condition both solvers complained about, so it is reported.

A view with no findings is not necessarily solvable, but it is not deficient in *this* way.

Usage
-----
    python tools/check_missing_declared_packages.py --views _views
    python tools/check_missing_declared_packages.py --views _views --verbose
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VIEW_PREFIX = "spider2-dbt-"

# Dotted names that are Jinja/dbt context objects, NOT dbt packages. A reference to one of these is
# never a missing dependency.
BUILTIN_NAMESPACES = {
    "adapter", "api", "builtins", "config", "dbt", "dbt_version", "exceptions", "flags", "graph",
    "invocation_id", "load_result", "local_md5", "log", "model", "modules", "print", "project_name",
    "ref", "return", "run_query", "run_started_at", "schema", "selected_resources", "source",
    "statement", "store_result", "target", "this", "thread_id", "try_or_compiler_error", "var",
    "zip", "dict", "list", "set", "range", "namespace", "loop", "caller", "self",
    # Jinja macro varargs/kwargs objects — `kwargs.get(...)` is not a package call.
    "kwargs", "varargs",
}

# `{{ ns.macro(` / `{% set x = ns.macro(` — a dotted call whose head is a bare identifier.
_NS_CALL = re.compile(r"(?<![\w.])([a-z_][a-z0-9_]*)\.[a-z_][a-z0-9_]*\s*\(", re.I)
# Package entries in packages.yml / dependencies.yml.
_PKG_NAME = re.compile(r"^\s*-\s*(?:package|local|git):\s*(.+?)\s*$", re.M)

# Names bound locally in the SAME file are Jinja variables, not packages: `{% set col = ... %}`,
# `{% for col in ... %}`, `{% macro f(col, cols) %}`, `{% call ... %}`. Without this exclusion the
# scan reports `kwargs`, `col`, `re`, `node`, `fields` as missing dependencies — noise that would
# inflate the exposure count and bury the real findings.
_LOCAL_SET = re.compile(r"\{%-?\s*set\s+([a-z_][a-z0-9_]*)", re.I)
_LOCAL_FOR = re.compile(r"\{%-?\s*for\s+([a-z_][a-z0-9_,\s]*?)\s+in\s", re.I)
_LOCAL_MACRO = re.compile(r"\{%-?\s*macro\s+[a-z_][a-z0-9_]*\s*\((.*?)\)", re.I | re.S)


def _local_names(text: str) -> set[str]:
    names = {m.lower() for m in _LOCAL_SET.findall(text)}
    for group in _LOCAL_FOR.findall(text):
        names |= {p.strip().lower() for p in group.split(",") if p.strip()}
    for args in _LOCAL_MACRO.findall(text):
        for arg in args.split(","):
            name = arg.split("=")[0].strip().lower()
            if re.fullmatch(r"[a-z_][a-z0-9_]*", name):
                names.add(name)
    return names


def _referenced_namespaces(project: Path) -> dict[str, int]:
    """Package namespaces referenced from the project's OWN sql/yml (never from dbt_packages/).

    Excludes Jinja/dbt builtins and any name bound locally in the same file, so what remains is a
    call into another dbt package's macro namespace.
    """
    counts: dict[str, int] = {}
    for sub in ("models", "macros", "analyses", "snapshots", "tests"):
        root = project / sub
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_dir() or "dbt_packages" in path.parts:
                continue
            if path.suffix.lower() not in (".sql", ".yml", ".yaml"):
                continue
            text = path.read_text(errors="ignore")
            local = _local_names(text)
            # Only look inside Jinja delimiters; plain SQL `table.column(` is not a macro call.
            for chunk in re.findall(r"\{\{(.*?)\}\}|\{%(.*?)%\}", text, re.S):
                for part in chunk:
                    for ns in _NS_CALL.findall(part or ""):
                        low = ns.lower()
                        if low in BUILTIN_NAMESPACES or low in local:
                            continue
                        counts[low] = counts.get(low, 0) + 1
    return counts


def _vendored(project: Path) -> set[str]:
    pkgs = project / "dbt_packages"
    if not pkgs.is_dir():
        return set()
    return {p.name.lower() for p in pkgs.iterdir() if p.is_dir()}


def _declared(project: Path) -> tuple[set[str], list[str]]:
    """(declared package short-names, manifest files found)."""
    names: set[str] = set()
    found: list[str] = []
    for fname in ("packages.yml", "dependencies.yml"):
        path = project / fname
        if not path.is_file():
            continue
        found.append(fname)
        for raw in _PKG_NAME.findall(path.read_text(errors="ignore")):
            # `fivetran/shopify_source` -> shopify_source; `dbt_packages/dbt_utils` -> dbt_utils
            names.add(raw.strip().strip("\"'").rstrip("/").split("/")[-1].lower())
    return names, found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--views", type=Path, required=True)
    ap.add_argument("--verbose", action="store_true", help="Also print clean views.")
    args = ap.parse_args()

    views = sorted(p for p in args.views.glob(f"{VIEW_PREFIX}*") if p.is_dir())
    if not views:
        print(f"no views under {args.views}", file=sys.stderr)
        return 1

    unresolved: dict[str, list[str]] = {}
    declared_missing: dict[str, list[str]] = {}
    vendored_undeclared: list[str] = []
    clean: list[str] = []

    for view in views:
        instance = view.name[len(VIEW_PREFIX):]
        project = view / "dbt_project"
        if not project.is_dir():
            continue
        refs = _referenced_namespaces(project)
        have = _vendored(project)
        declared, manifests = _declared(project)

        missing_ns = sorted(ns for ns in refs if ns not in have)
        if missing_ns:
            unresolved[instance] = [f"{ns}(x{refs[ns]})" for ns in missing_ns]
        gap = sorted(declared - have)
        if gap:
            declared_missing[instance] = gap
        if have and not manifests:
            vendored_undeclared.append(instance)
        if not missing_ns and not gap:
            clean.append(instance)

    def block(title: str, rows: dict[str, list[str]]) -> None:
        print(f"\n### {title}: {len(rows)}")
        for inst, items in sorted(rows.items()):
            print(f"   {inst:<34} {', '.join(items)}")

    block("UNRESOLVED_NS — models call a package that is NOT vendored (the activity001 shape)", unresolved)
    block("DECLARED_NOT_VENDORED — manifest names a package with no dbt_packages/ dir", declared_missing)
    print(f"\n### VENDORED_UNDECLARED — packages present but no manifest: {len(vendored_undeclared)}")
    print("   " + (", ".join(sorted(vendored_undeclared)) if vendored_undeclared else "(none)"))
    if args.verbose:
        print(f"\n### no package deficiency: {len(clean)}")
        for inst in clean:
            print(f"   {inst}")

    print("\n==== EXPOSURE SUMMARY ====")
    print(f"views checked                : {len(views)}")
    print(f"UNRESOLVED_NS (highest risk) : {len(unresolved)} — {', '.join(sorted(unresolved)) or '(none)'}")
    print(f"DECLARED_NOT_VENDORED        : {len(declared_missing)} — {', '.join(sorted(declared_missing)) or '(none)'}")
    print(f"VENDORED_UNDECLARED          : {len(vendored_undeclared)}")
    print(f"no package deficiency        : {len(clean)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
