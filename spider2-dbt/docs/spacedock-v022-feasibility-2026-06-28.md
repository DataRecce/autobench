# spacedock v0.22.0 solver-env feasibility — 2026-06-28

**Verdict: FEASIBLE. Zero pipeline changes needed. razorback↔spacedock contract drift is benign.**

## Why this run
Bumped the `spacedock` solver-plugin submodule v0.12.1-4 → **v0.22.0** (commit `64515d2`).
razorback (pinned at PR#26, no newer version exists) hardcodes a **v0.12-era dispatch
vocabulary** in its solver prompt (`spacedock_solver.py`): `spawn_agent(..., fork_context=false)`
plus worker-identity fields `role_asset_kind`/`role_asset_name`. Three of those were **dropped in
v0.22**:

| razorback hardcodes | v0.12 | v0.22 |
|---|---|---|
| `spawn_agent` / `wait_agent` | ✅ | ✅ survives |
| `dispatch_agent_id` / `worker_key` | ✅ | ✅ survives |
| `fork_context` | ✅ | ❌ dropped |
| `role_asset_kind` / `role_asset_name` | ✅ | ❌ dropped |

Neither submodule is ours to ad-hoc edit, and no razorback version targets v0.22 — so the only
honest test was empirical.

## Spec
`specs/spacedock-v022-feasibility.smoke.yaml` — **champion solver (spd0013) UNCHANGED** so the only
variable is the v0.22 plugin; 1 rock-solid cell (`mrr001`, 3/3 in the variance map → a failure would
unambiguously mean dispatch broke, not task variance); trials=1; gpt-5.5 / xhigh.
Run dir: `runs/spacedock-v022-feasibility/f7c456329ceb5b85`.

## Result — PASS, clean dispatch lifecycle
- **reward 1.0**, `exception_info: null`. Agent exec ~7 min.
- `subagent-trace-manifest.json`: `prompt_mode: spacedock-codex-first-officer`, **1 dispatch captured**
  (`subagent_type: spacedock:ensign`, spawn_index 0); 2 rollout sessions = the FO+1-worker pattern
  razorback prescribes ("Dispatch one worker").
- Parent codex log item sequence (clean lifecycle, **0 non-hook-trust errors**):
  - item_8/item_12: FO read the **v0.22** `codex-first-officer-runtime.md` + `fo-dispatch-core.md`.
  - **item_15 `collab_tool_call` tool=`spawn_agent`** → dispatched the ensign worker (received worker
    thread `019f0ecc…`). **No `fork_context` argument error** — codex's collab spawn doesn't require it.
  - **item_17 tool=`wait`** (v0.22 uses `wait`, not `wait_agent`) → **item_19 tool=`close_agent`** =
    terminal teardown. Full spawn→wait→close lifecycle.
  - The 2 `error` items are both `--dangerously-bypass-hook-trust` warnings (benign).

## Conclusion
The dropped fields are non-load-bearing for the single-worker dispatch razorback asks for: the worker
resolves from `dispatch_agent_id: spacedock:ensign`, and `fork_context` is a Codex spawn nicety the
collab tool doesn't require. **v0.22 stands; no pipeline / razorback changes required.**

This mrr001 PASS is the **first data point of the v0.22 re-baseline** (the prior @baseline spd0013 27/60
+ variance map were measured under v0.12 and are non-comparable). A full champion re-baseline board under
v0.22 remains a separate captain go (codex credit window resets Jul 2).
