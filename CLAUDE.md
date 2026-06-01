# CLAUDE.md

**Read `AGENTS.md` first — it is the operating guide for this repo; everything in it
applies.**

Claude-Code specifics:

- Use the `spacedock:first-officer` skill to run or resume the autoresearch loop on
  `ade-bench/hypotheses/`.
- Use the `superpowers:brainstorming` skill when standing up a new benchmark or a new
  research concept.
- You are the **operator** of the loop, not the solver. The codex solver
  (`agent.kind: spacedock_solver`, `runtime: codex`) is spawned by razorback inside
  Harbor — you drive `rk` and the spacedock workflow, you do not solve the tasks.
- `rk` is run from `ade-bench/` as `uv run --project ../razorback rk <args>`; export
  `RAZORBACK_SPACEDOCK_PLUGIN_DIR` before any `rk run` (see AGENTS.md → Run prerequisites).
