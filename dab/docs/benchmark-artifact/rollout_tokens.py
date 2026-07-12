#!/usr/bin/env python3
"""
Recover token usage from codex session ROLLOUT logs (rk-native run dirs).

Why this exists
---------------
`extract_benchmark_data.py` was built for the old CAIS merge layout
(run-*/datasets/*/attempts/attempt-*/codex-output.jsonl) and reads direct-harness
tokens from each run's result.json `stats`. The current rk/harbor run dirs use a
different layout and their result.json `stats` is null, so tokens must be recovered
from the codex rollout logs instead:

    <cfg>/<job-hash>/<DATASET>__<id>/steps/main/agent/sessions/YYYY/MM/DD/rollout-*.jsonl

Each rollout is one codex session. The last `token_count` event carries the
cumulative `total_token_usage`. We take that per rollout and SUM across all rollout
files in the config.

Multi-agent (spacedock) note
----------------------------
A spacedock_solver dataset produces TWO rollout files per dataset:
  - the first-officer thread (session_meta has NO parent_thread_id), and
  - the ensign solver thread (session_meta HAS parent_thread_id + agent_nickname).
They are independent codex sessions (no token double-count), so summing every
rollout in the config gives the true FO+ensign cost. Earlier codex builds logged
ONLY the first-officer thread — that was the "spacedock tokens unrecoverable" bug.
The newer build logs both, so summing rollouts now yields the real total.

A plain `agent.kind: codex` dataset (direct-minimal / direct-structured) produces
ONE rollout file per dataset, so the same summation Just Works.

Convention (matches the artifact page + extract_benchmark_data.tokens_direct):
    total = input_tokens + output_tokens   (input_tokens already includes cached)
    out   = output_tokens
summed over every rollout in every run of the config.

Verified: this reproduces the hand-checked direct-minimal gpt-5.6-sol page number
(44,276,047 / 551,743) to the token.

Usage
-----
    python3 rollout_tokens.py <cfg_dir> [<cfg_dir> ...]

Each <cfg_dir> is a config root that contains run directories (either rk job-hash
subdirs directly, or a CAIS merge dir whose run-* entries symlink to them — this
follows symlinks). Prints tokTotal / tokOut per config, paste-ready for the page's
CONFIGS `tokTotal:` / `tokOut:` fields.
"""
import json, os, sys


def _rollout_total(path):
    """(input_tokens, output_tokens) from the last token_count in one rollout log."""
    last = None
    with open(path, errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            p = d.get("payload", {})
            if isinstance(p, dict) and p.get("type") == "token_count":
                ttu = (p.get("info") or {}).get("total_token_usage")
                if ttu:
                    last = ttu
    if not last:
        return (0, 0)
    return (last.get("input_tokens", 0), last.get("output_tokens", 0))


def _iter_rollouts(cfg_dir):
    """Yield every rollout-*.jsonl under cfg_dir, following symlinks (merge dirs)."""
    for root, _dirs, files in os.walk(cfg_dir, followlinks=True):
        for name in files:
            if name.startswith("rollout-") and name.endswith(".jsonl"):
                yield os.path.join(root, name)


def config_tokens(cfg_dir):
    tin = tout = 0
    nfiles = 0
    for f in _iter_rollouts(cfg_dir):
        i, o = _rollout_total(f)
        tin += i
        tout += o
        nfiles += 1
    return {"tokTotal": tin + tout, "tokOut": tout, "rollouts": nfiles}


def main(argv):
    if not argv:
        print(__doc__)
        sys.exit(1)
    for cfg in argv:
        r = config_tokens(cfg)
        name = os.path.basename(os.path.normpath(cfg))
        print(f"{name}: tokTotal:{r['tokTotal']} tokOut:{r['tokOut']}  "
              f"({r['rollouts']} rollout sessions)")


if __name__ == "__main__":
    main(sys.argv[1:])
