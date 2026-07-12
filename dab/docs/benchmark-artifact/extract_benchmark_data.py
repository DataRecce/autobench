#!/usr/bin/env python3
"""
Extract the data objects that drive the DAB benchmark Claude artifact page.

Usage:
    python3 extract_benchmark_data.py <runs_dir> <config_dir> [<config_dir> ...]

Each <config_dir> is a run directory under <runs_dir> (e.g. codex-dab-spacedock-high).
The script auto-detects the harness/log flavor and emits a single JSON blob with:
    - CONFIGS   : one row per config (score, stdev, min/max, tokens, meanSec, timeouts)
    - PER_DATASET: {dataset: {n_queries, {config_id: mean_passed}}}
    - DURATIONS : {config_id: [raw per-session wall-clock seconds]}

Paste the three pieces into dab-benchmark-template.html (see PLAYBOOK.md).

Config ids are derived from the dir name; override with the --id flag pairs
(e.g. --id codex-dab-spacedock-high=sd-h). Short/family/effort are guessed from
the name and should be sanity-checked in the template.

READ PLAYBOOK.md before trusting the output — the timing/token scopes differ by
flavor and several fields are legitimately null (see the caveats section).
"""
import json, glob, os, re, sys, datetime as dt, statistics as st

# ------------------------------------------------------------------ helpers
def _parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", ""))

def _quantile(a, p):
    s = sorted(a); i = (len(s) - 1) * p; lo = int(i); hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (i - lo)

# ------------------------------------------------------------------ detection
_HARBOR_TRIAL_GLOB = os.path.join("*", "*__*", "steps", "main", "agent")

def detect_flavor(cfg_path):
    """Return one of: 'direct', 'spacedock_old', 'spacedock_new', 'harbor'."""
    if glob.glob(os.path.join(cfg_path, "run-*", "result.json")):
        # direct harness: per-run result.json carries stats.n_*_tokens.
        # Require a non-null value — harbor spacedock jobs have the key with null
        # (subscription runs don't meter) and must fall through to 'harbor'.
        for f in glob.glob(os.path.join(cfg_path, "run-*", "result.json")):
            d = json.load(open(f))
            if d.get("stats", {}).get("n_input_tokens") is not None:
                return "direct"
    # spacedock: per-dataset codex sessions
    if glob.glob(os.path.join(cfg_path, "run-*", "datasets", "*", "codex-output.jsonl")):
        # old flavor has token_count events with total_token_usage
        f = glob.glob(os.path.join(cfg_path, "run-*", "datasets", "*", "codex-output.jsonl"))[0]
        if "total_token_usage" in open(f).read():
            return "spacedock_old"
    if glob.glob(os.path.join(cfg_path, "run-*", "datasets", "*", "attempts", "attempt-*", "codex-output.jsonl")):
        return "spacedock_new"
    if glob.glob(os.path.join(cfg_path, "run-*", "datasets", "*", "codex-output.jsonl")):
        return "spacedock_old"
    # harbor trial layout (gpt-5.6-sol era): <run>/<dataset>__<id>/steps/main/agent/
    # with codex.txt (exec stdout, FO-thread-only) + sessions/ (ALL thread rollouts).
    # Same layout for direct and spacedock configs; tokens come from sessions/.
    if glob.glob(os.path.join(cfg_path, _HARBOR_TRIAL_GLOB, "codex.txt")):
        return "harbor"
    raise SystemExit(f"cannot detect flavor for {cfg_path}")

# ------------------------------------------------------------------ scores
def scores(cfg_path):
    """Scores/stdev/min/max + per-dataset, from the CAIS 5-run merge summary.json."""
    d = json.load(open(os.path.join(cfg_path, "summary.json")))
    s = d["stratified_pass_at_1"]
    per_ds = {name: {"n": v["n_queries"], "mean_passed": v["mean_passed"]}
              for name, v in d.get("per_dataset", {}).items()}
    return {
        "strat": round(s["mean"], 4), "sd": round(s["stdev"], 4),
        "min": round(s["min"], 4), "max": round(s["max"], 4),
        "n_runs": d.get("n_runs"),
    }, per_ds

# ------------------------------------------------------------------ tokens
def tokens_direct(cfg_path):
    tin = tout = 0
    for f in glob.glob(os.path.join(cfg_path, "run-*", "result.json")):
        s = json.load(open(f)).get("stats", {})
        ti, to = s.get("n_input_tokens"), s.get("n_output_tokens")
        if ti is None or to is None:
            # subscription/spacedock_solver rk runs don't meter tokens → show "—"
            return {"tokTotal": None, "tokOut": None}
        tin += ti; tout += to
    return {"tokTotal": tin + tout, "tokOut": tout} if tin else {"tokTotal": None, "tokOut": None}

def tokens_spacedock_old(cfg_path):
    tin = tout = 0; n = 0
    for f in glob.glob(os.path.join(cfg_path, "run-*", "datasets", "*", "codex-output.jsonl")):
        last = None
        for line in open(f):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            p = d.get("payload", {})
            if isinstance(p, dict) and p.get("type") == "token_count":
                last = p["info"]["total_token_usage"]
        if last:
            tin += last["input_tokens"]; tout += last["output_tokens"]; n += 1
    return {"tokTotal": tin + tout, "tokOut": tout} if n else {"tokTotal": None, "tokOut": None}

def tokens_spacedock_new(cfg_path):
    """New codex log emits usage only on turn.completed. In the FO+ensign setup the
    ensign thread is NOT logged, and timed-out sessions emit no usage at all, so any
    total here is a severe FO-only undercount. Return null and let the template show n/a."""
    return {"tokTotal": None, "tokOut": None}

def _rollout_last_usage(path):
    """Last cumulative total_token_usage in a codex rollout jsonl (= thread total)."""
    last = None
    with open(path, errors="ignore") as fh:
        for line in fh:
            if '"token_count"' not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            p = d.get("payload", {})
            if isinstance(p, dict) and p.get("type") == "token_count" and p.get("info"):
                last = p["info"].get("total_token_usage") or last
    return last

def tokens_harbor(cfg_path):
    """Harbor layout: codex.txt (stdout) is FO-thread-only, but sessions/ holds one
    rollout PER THREAD (FO + ensign for spacedock; single thread for direct), each
    with cumulative token_count events. Sum the last usage of every rollout.
    Trials whose sessions are incomplete (turn.failed / crash) are counted in
    tokMissingTrials — the total is a slight undercount when that is > 0."""
    tin = tout = 0
    n_rollouts = 0
    incomplete = 0
    for agent_dir in glob.glob(os.path.join(cfg_path, _HARBOR_TRIAL_GLOB)):
        for f in glob.glob(os.path.join(agent_dir, "sessions", "**", "*.jsonl"), recursive=True):
            u = _rollout_last_usage(f)
            if u:
                tin += u["input_tokens"]; tout += u["output_tokens"]; n_rollouts += 1
        # a session that never reached turn.completed (turn.failed / timeout / crash)
        # may be missing whole subagent rollouts → the sum is a floor, flag it
        stdout_log = os.path.join(agent_dir, "codex.txt")
        if os.path.isfile(stdout_log) and '"turn.completed"' not in open(stdout_log, errors="ignore").read():
            incomplete += 1
    if not n_rollouts:
        return {"tokTotal": None, "tokOut": None}
    out = {"tokTotal": tin + tout, "tokOut": tout}
    if incomplete:
        out["tokIncompleteTrials"] = incomplete
    return out

# ------------------------------------------------------------------ durations
def durations_direct(cfg_path):
    out = []
    for f in glob.glob(os.path.join(cfg_path, "run-*", "*__*", "result.json")):
        d = json.load(open(f)); s, e = d.get("started_at"), d.get("finished_at")
        if s and e:
            out.append(round((_parse_ts(e) - _parse_ts(s)).total_seconds()))
    return sorted(out)

def durations_spacedock_old(cfg_path):
    out = []
    for f in glob.glob(os.path.join(cfg_path, "run-*", "datasets", "*", "codex-output.jsonl")):
        vals = [int(x) for x in re.findall(r'"duration_ms":(\d+)', open(f).read())]
        if vals:
            out.append(round(max(vals) / 1000))
    return sorted(out)

def durations_spacedock_new(cfg_path):
    out = []
    for f in glob.glob(os.path.join(cfg_path, "run-*", "datasets", "*", "attempts", "attempt-*", "codex-meta.json")):
        v = json.load(open(f)).get("duration_s")
        if v is not None:
            out.append(v)
    return sorted(out)

def durations_harbor(cfg_path):
    """Trial wall-clock from the harbor trial result.json (started_at → finished_at).
    Scope = env setup + agent + verify, same as the 'direct' flavor."""
    out = []
    for agent_dir in glob.glob(os.path.join(cfg_path, _HARBOR_TRIAL_GLOB)):
        trial_dir = os.path.dirname(os.path.dirname(os.path.dirname(agent_dir)))
        rj = os.path.join(trial_dir, "result.json")
        if not os.path.isfile(rj):
            continue
        d = json.load(open(rj)); s, e = d.get("started_at"), d.get("finished_at")
        if s and e:
            out.append(round((_parse_ts(e) - _parse_ts(s)).total_seconds()))
    return sorted(out)

# ------------------------------------------------------------------ timeouts
def timeouts_spacedock_new(cfg_path, cap=1800):
    stderrs = glob.glob(os.path.join(cfg_path, "run-*", "datasets", "*", "attempts", "attempt-*", "codex-stderr.log"))
    n_to = sum(1 for f in stderrs if "timed out" in open(f, errors="ignore").read())
    return {"timeouts": n_to, "sessions": len(stderrs), "censored": n_to > 0} if n_to else {}

def timeouts_harbor(cfg_path):
    """Classify sessions that never reached turn.completed.
    - "timed out"  → timeouts (right-censored timing, like spacedock_new)
    - anything else (e.g. turn.failed "model is at capacity") → failedSessions:
      fast failures scored 0, NOT censored — do not hatch/floor the timing for them."""
    n_to = n_fail = n_sessions = 0
    for f in glob.glob(os.path.join(cfg_path, _HARBOR_TRIAL_GLOB, "codex.txt")):
        n_sessions += 1
        txt = open(f, errors="ignore").read()
        if '"turn.completed"' in txt:
            continue
        if "timed out" in txt:
            n_to += 1
        else:
            n_fail += 1
    out = {}
    if n_to:
        out.update({"timeouts": n_to, "censored": True})
    if n_fail:
        out["failedSessions"] = n_fail
    if out:
        out["sessions"] = n_sessions
    return out

# ------------------------------------------------------------------ per-config
def build_config(cfg_path, cfg_id, short, family, effort):
    flavor = detect_flavor(cfg_path)
    sc, per_ds = scores(cfg_path)
    tok = {"direct": tokens_direct, "spacedock_old": tokens_spacedock_old,
           "spacedock_new": tokens_spacedock_new, "harbor": tokens_harbor}[flavor](cfg_path)
    durs = {"direct": durations_direct, "spacedock_old": durations_spacedock_old,
            "spacedock_new": durations_spacedock_new, "harbor": durations_harbor}[flavor](cfg_path)
    row = {"id": cfg_id, "fam": family, "short": short, "effort": effort, "flavor": flavor,
           **sc, **tok, "meanSec": round(st.mean(durs)) if durs else None}
    if flavor == "spacedock_new":
        row.update(timeouts_spacedock_new(cfg_path))
    elif flavor == "harbor":
        row.update(timeouts_harbor(cfg_path))
    return row, per_ds, durs

# ------------------------------------------------------------------ name guessing
def guess_meta(name):
    effort = "xhigh" if name.endswith("xhigh") else ("high" if name.endswith("high") else "?")
    base = re.sub(r"-(x?high)$", "", name).replace("codex-dab-", "")
    short = {"spacedock": "spacedock", "direct-minimal": "direct-min",
             "direct-structured": "direct-str"}.get(base, base)
    family = {"spacedock": "spacedock", "direct-minimal": "direct-minimal",
              "direct-structured": "direct-structured"}.get(base, base)
    # short id prefix: known families mapped explicitly, else initials
    prefix = {"spacedock": "sd", "direct-minimal": "dm",
              "direct-structured": "ds"}.get(base, "".join(w[0] for w in base.split("-")))
    sid = prefix + "-" + ("x" if effort == "xhigh" else "h")
    return sid, short, family, effort

# ------------------------------------------------------------------ main
def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    runs_dir, cfg_names = args[0], args[1:]

    CONFIGS = []
    PER_DATASET = {}
    DURATIONS = {}
    for name in cfg_names:
        cfg_path = os.path.join(runs_dir, name)
        sid, short, family, effort = guess_meta(name)
        row, per_ds, durs = build_config(cfg_path, sid, short, family, effort)
        CONFIGS.append(row)
        DURATIONS[sid] = durs
        for ds, v in per_ds.items():
            PER_DATASET.setdefault(ds, {"n": v["n"], "vals": {}})
            PER_DATASET[ds]["vals"][sid] = v["mean_passed"]

    if "--js" in argv:
        emit_js(CONFIGS, PER_DATASET, DURATIONS)
    else:
        print(json.dumps({"CONFIGS": CONFIGS, "PER_DATASET": PER_DATASET, "DURATIONS": DURATIONS}, indent=2))

def emit_js(CONFIGS, PER_DATASET, DURATIONS):
    """Print paste-ready JS literals matching dab-benchmark-template.html's data objects."""
    def jsval(v):
        return "null" if v is None else json.dumps(v)
    # CONFIGS
    print("// ---- paste into template: const CONFIGS = [...] ----")
    print("const CONFIGS = [")
    keys = ["id", "fam", "short", "effort", "strat", "sd", "min", "max",
            "tokTotal", "tokOut", "tokIncompleteTrials", "meanSec",
            "censored", "timeouts", "failedSessions", "sessions"]
    for c in CONFIGS:
        parts = [f"{k}:{jsval(c[k])}" for k in keys if k in c and c.get(k) is not None or k in ("tokTotal", "tokOut")]
        print("  { " + ", ".join(parts) + " },  // TODO add note: for lever-carrying configs")
    print("];\n")
    # DATASETS (sorted by n_queries desc, matching the template)
    print("// ---- paste into template: const DATASETS = [...] ----")
    print("const DATASETS = [")
    for name, v in sorted(PER_DATASET.items(), key=lambda kv: -kv[1]["n"]):
        vals = json.dumps(v["vals"]).replace('"', "'")
        print(f"  ['{name}',{v['n']}, {vals}],")
    print("];")
    ids = [c["id"] for c in CONFIGS]
    print(f"const COL_ORDER = {json.dumps(ids)};\n".replace('"', "'"))
    # DURATIONS
    print("// ---- paste into template: const DURATIONS = {...} ----")
    print("const DURATIONS = {")
    for cid, arr in DURATIONS.items():
        print(f"  '{cid}':{json.dumps(arr)},")
    print("};")

if __name__ == "__main__":
    main(sys.argv[1:])
