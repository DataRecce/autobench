#!/usr/bin/env python3
# ABOUTME: Offline re-score of codex-dab-batch-baseline against the LATEST DAB
# ABOUTME: ground-truth/verifier (data root @ upstream HEAD), without re-running the solver.
#
# Method: recover each cell's committed answers.json from the rollout transcript,
# replay the production verify_batch.py over it. Integrity gate: recovered answers
# MUST reproduce the stored reward_per_query.json against the ORIGINAL (run-dir-baked)
# validators before any "latest" number is trusted. Only the 4 changed-validator
# queries (googlelocal-q3, PATENTS-q1/q2/q3) can move; the other 8 datasets carry
# forward unchanged by construction. Non-destructive: original run-dirs untouched.

import json
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

DAB = Path("/home/kent/autobench/dab")
RUNS = DAB / "runs/codex-dab-batch-baseline"
DRAWS = ["342778d74e96f477", "bf113446fdd94373"]
DATA_ROOT = Path.home() / "dataagentbench/data"
# the LATEST production runner (per-query try/except guard, PR #19)
PLUGIN_VERIFY_BATCH = (
    Path("/home/kent/autobench/razorback/packages/razorback-plugin-dab")
    / "src/razorback_plugin_dab/verify/verify_batch.py"
)
# (dataset, query_id) whose validator changed since the original June-21 run
CHANGED = {("googlelocal", 3), ("PATENTS", 1), ("PATENTS", 2), ("PATENTS", 3)}
CHANGED_DATASETS = {ds for ds, _ in CHANGED}


def find_cell(draw: str, dataset: str) -> Path:
    hits = sorted((RUNS / draw).glob(f"{dataset}__*"))
    assert len(hits) == 1, f"expected 1 cell for {draw}/{dataset}, got {hits}"
    return hits[0]


def recover_answers(cell: Path) -> dict | None:
    """Recover the final committed answers.json from the rollout transcript.

    Collect every observable write to /workspace/answers.json — apply_patch
    Add-File bodies ('+'-prefixed lines) and shell heredoc bodies in
    exec_command arguments — plus any full JSON dump echoed in a
    function_call_output. Return the LAST candidate that parses as a dict.
    """
    rolls = sorted(cell.glob("steps/main/agent/sessions/**/*.jsonl"))
    candidates: list[dict] = []
    for r in rolls:
        for line in r.open():
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            p = o.get("payload", {})
            t = p.get("type")
            # 1) apply_patch Add File: /workspace/answers.json
            if t == "custom_tool_call" and p.get("name") == "apply_patch":
                body = _extract_apply_patch_add(p.get("input") or "")
                if body is not None:
                    d = _try_json(body)
                    if isinstance(d, dict):
                        candidates.append(d)
            # 2) shell heredoc / write in exec_command arguments
            if t == "function_call" and "answers.json" in (p.get("arguments") or ""):
                for body in _extract_heredoc_bodies(p.get("arguments") or ""):
                    d = _try_json(body)
                    if isinstance(d, dict):
                        candidates.append(d)
            # 3) full JSON dump echoed back (e.g. `python -m json.tool answers.json`)
            if t == "function_call_output":
                out = p.get("output") or ""
                d = _try_json_embedded(out)
                if isinstance(d, dict) and any(k.startswith("q") for k in d):
                    candidates.append(d)
    # prefer the last candidate that looks like an answers map (q-keys)
    qmaps = [c for c in candidates if any(k.startswith("q") for k in c)]
    if qmaps:
        return qmaps[-1]
    return candidates[-1] if candidates else None


def _extract_apply_patch_add(patch: str) -> str | None:
    lines = patch.splitlines()
    out: list[str] = []
    capturing = False
    for ln in lines:
        if ln.startswith("*** Add File: ") and ln.endswith("/workspace/answers.json"):
            capturing = True
            out = []
            continue
        if capturing and ln.startswith("*** "):
            break
        if capturing:
            out.append(ln[1:] if ln.startswith(("+", " ")) else ln)
    return "\n".join(out) if out else None


def _extract_heredoc_bodies(cmd: str) -> list[str]:
    """Pull heredoc bodies out of a shell command string. Handles `<<'EOF' ... EOF`
    and `<<EOF ... EOF` with arbitrary delimiters."""
    import re

    bodies: list[str] = []
    for m in re.finditer(r"<<-?\s*'?([A-Za-z_][A-Za-z0-9_]*)'?\s*\n(.*?)\n\1", cmd, re.S):
        bodies.append(m.group(2))
    return bodies


def _try_json(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None


def _try_json_embedded(s: str):
    # find the first '{' ... last '}' and try to parse
    i, j = s.find("{"), s.rfind("}")
    if i == -1 or j == -1 or j <= i:
        return None
    return _try_json(s[i : j + 1])


def run_verify_batch(tests_dir: Path, answers: dict, runner: Path | None = None) -> dict | None:
    """Run verify_batch.py over `answers`; return per-query reward map, or None
    if the runner crashed without producing output (mirrors the original
    crash-drop behavior). `runner` overrides which verify_batch.py is used
    (default: the one inside tests_dir)."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        ans = td / "answers.json"
        ans.write_text(json.dumps(answers))
        reward_out = td / "reward.json"
        pq_out = td / "reward_per_query.json"
        vb = runner if runner is not None else (tests_dir / "verify_batch.py")
        subprocess.run(
            [
                sys.executable, str(vb),
                "--tests-dir", str(tests_dir),
                "--answers", str(ans),
                "--reward-out", str(reward_out),
                "--per-query-out", str(pq_out),
            ],
            cwd=str(tests_dir), capture_output=True, text=True,
        )
        if not pq_out.exists():
            return None
        return json.loads(pq_out.read_text())


def latest_tests_dir(orig_tests: Path, dataset: str, stage: Path) -> Path:
    """Copy the original tests dir and overlay the LATEST data-root validators
    for the changed queries of `dataset`. Faithful to prepare's non-bookreview
    copy path (direct shutil.copy2 of data-root validate.py)."""
    dst = stage / dataset
    shutil.copytree(orig_tests, dst)
    # latest runner (per-query guard)
    shutil.copy2(PLUGIN_VERIFY_BATCH, dst / "verify_batch.py")
    # latest validators for the changed queries
    for ds, qid in CHANGED:
        if ds != dataset:
            continue
        src = DATA_ROOT / f"query_{dataset}" / f"query{qid}" / "validate.py"
        shutil.copy2(src, dst / f"validate_q{qid}.py")
    return dst


def main() -> int:
    report = {"draws": {}, "changed_queries": sorted(f"{d}-q{q}" for d, q in CHANGED)}
    all_ok = True
    with tempfile.TemporaryDirectory() as stage_root:
        for draw in DRAWS:
            dreport = {}
            for dataset in sorted(CHANGED_DATASETS):
                cell = find_cell(draw, dataset)
                pq_path = cell / "steps/main/verifier/reward_per_query.json"
                stored = json.loads(pq_path.read_text()) if pq_path.exists() else None
                answers = recover_answers(cell)
                orig_tests = DAB / f"runs/codex-dab-batch-baseline/{draw}/tasks/{dataset}/tests"
                entry = {"recovered": answers is not None, "stored_existed": stored is not None}
                if answers is None:
                    entry["error"] = "could not recover answers.json from rollout"
                    all_ok = False
                    dreport[dataset] = entry
                    continue
                # integrity cross-check: recovered answers + ORIGINAL tests (old
                # runner + old validators) must reproduce the stored result.
                xcheck = run_verify_batch(orig_tests, answers)
                if stored is None:
                    # original produced NO reward (crash-drop). Faithful recovery
                    # must reproduce the crash → xcheck is None too.
                    xc_ok = xcheck is None
                    entry["xcheck_reproduces_crash_drop"] = xc_ok
                else:
                    xc_ok = (xcheck is not None) and (
                        {k: xcheck.get(k, {}).get("reward") for k in stored}
                        == {k: stored[k].get("reward") for k in stored}
                    )
                    entry["xcheck_reproduces_stored"] = xc_ok
                    if not xc_ok:
                        entry["xcheck_detail"] = {
                            "stored": {k: stored[k]["reward"] for k in stored},
                            "replayed_orig": None if xcheck is None
                            else {k: xcheck.get(k, {}).get("reward") for k in stored},
                        }
                if not xc_ok:
                    all_ok = False
                # latest replay: latest runner + latest validators
                stage = Path(stage_root) / draw
                stage.mkdir(parents=True, exist_ok=True)
                ltests = latest_tests_dir(orig_tests, dataset, stage)
                latest = run_verify_batch(ltests, answers, runner=ltests / "verify_batch.py")
                if latest is None:
                    entry["latest_error"] = "latest verify_batch produced no output"
                    all_ok = False
                    dreport[dataset] = entry
                    continue
                old_map = stored or {}
                flips = {}
                for k in sorted(set(old_map) | set(latest)):
                    old = old_map.get(k, {}).get("reward")
                    new = latest.get(k, {}).get("reward")
                    if old != new:
                        flips[k] = {
                            "old": old, "new": new,
                            "old_reason": old_map.get(k, {}).get("reason"),
                            "new_reason": latest.get(k, {}).get("reason"),
                        }
                entry["flips"] = flips
                entry["latest_per_query"] = {k: latest[k]["reward"] for k in sorted(latest)}
                dreport[dataset] = entry
            report["draws"][draw] = dreport
    report["integrity_all_ok"] = all_ok
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 2


if __name__ == "__main__":
    sys.exit(main())
