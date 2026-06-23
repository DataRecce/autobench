# DAB leaderboard submission — dab0022 semi-structured-data-rules (codex / gpt-5.5)

Formal DataAgentBench leaderboard submission package for the autobench `dab0022-patents-semistructured-rules`
result. **5 full draws** of one solver README (the cycle-3 `### Semi-structured data rules` section;
solver content hash `sha256:b2cae85c…`) over all 12 datasets / 54 queries.

- **Agent:** codex spacedock-solver (batch mode — one agent session per dataset per run)
- **Model:** gpt-5.5, `reasoning_effort: high`, `temperature: 0.0`
- **Aggregate (5-draw mean):** stratified Pass@1 = 0.7433 (per-draw spread 0.6675–0.7985; median 0.7675);
  raw-cell micro-average 204/270.

## Contents

- `codex-gpt-5.5_results.json` — **Deliverable 1**: flat list of 270 `{dataset, query, run, answer}`
  objects (54 queries × 5 runs), matching the reference
  `data/leaderboard_submissions/<model>_results.json` schema (`run` and `query` are strings; `query` is
  the per-dataset query number). `answer` is the solver's committed answer for that query in that draw.
- `raw_logs/` — **Deliverable 2**: per-dataset directories (12) → `run-001`..`run-005` subdirs, each with
  the codex agent transcript, the cell `answers.json`, and the `rk audit` taint files; plus a per-dataset
  `summary.json`. Matches the reference `~/spacedock-experiment-opus-4-8-hint/` tree.

## Draw → run-index mapping (consistent across both deliverables)

| run index (results.json) | run dir (raw_logs) | source run | notes |
|--------------------------|--------------------|------------|-------|
| `"0"` | `run-001` | `runs/dab0022-patents-semistructured-rules/d0a6f64260336fff` | first full draw (trials:1) |
| `"1"` | `run-002` | `runs/dab0022-patents-semistructured-rules/e8ec7dd1bde26916` (trial 0) | 3-draw confirm, internal trial 0 |
| `"2"` | `run-003` | `runs/dab0022-patents-semistructured-rules/e8ec7dd1bde26916` (trial 1) | 3-draw confirm, internal trial 1 |
| `"3"` | `run-004` | `runs/dab0022-patents-semistructured-rules/e8ec7dd1bde26916` (trial 2) | 3-draw confirm, internal trial 2 |
| `"4"` | `run-005` | `runs/dab0022-patents-semistructured-rules-draw5/f74c12b94f2f5172` | 5th full draw (trials:1) |

## Deviations from the reference formats (read me)

1. **Transcript filename: `codex-output.jsonl`, not `claude-output.jsonl`.** Our solver is codex
   (gpt-5.5), not Claude. The per-run file SET is otherwise identical to the reference
   (`answers.json`, the agent transcript, `taint.json`, `taint.md`). The transcript is the codex
   **worker** session jsonl (batch mode dispatches one worker per dataset-run; the first-officer session
   that dispatches it is included as `codex-output.fo.jsonl` for completeness where present).
2. **`summary.json` cost/token fields:** codex ran on a flat OpenAI subscription, so per-run
   `cost_usd` and token counts are not tracked by the harness — these fields are `null` (the reference's
   Claude runs had metered token/cost stats). `passed`/`total`/`score`/`taint_status`/`duration_s`
   are populated.
3. **`answers.json` recovery:** the run-dirs do not persist `answers.json` (only the rollout transcript +
   verifier outputs), so each cell's `answers.json` is recovered from the worker transcript's final write
   to `/workspace/answers.json`. Integrity is gated by matching the recovered key set to the stored
   `reward_per_query.json`. 59 of 60 cells recovered cleanly on the first pass; the 60th (PATENTS run-005)
   was filled by a fresh re-run — see note 4. **All 270 entries are now present.**
4. **`PATENTS` run-005 (run index `"4"`) is a FRESH INDEPENDENT DRAW — honest disclosure.** The ORIGINAL
   draw-5 PATENTS cell (`runs/dab0022-patents-semistructured-rules-draw5/f74c12b94f2f5172`) computed its
   answers inside a runtime `solve_dataset.py` (live-DB query) that `json.dump`'d to `answers.json`, and
   the worker only READ the file back for contract checks (truncated prefixes) — so its verbatim committed
   answer was NOT recoverable from the transcript (the harness does not persist the per-cell `answers.json`
   out of the container; the only durable source is the transcript). Rather than fabricate, a **fresh
   PATENTS-only re-run** was launched at the same cycle-3 README + high (run dir
   `runs/dab0022-patents-semistructured-rules-patents-r5/7e0f83df055ce078`); that draw echoed the full
   answers object verbatim (q1 430 / q2 1393 / q3 255 chars — lengths matched its own self-report), so its
   q1/q2/q3 now populate run "4" in `codex-gpt-5.5_results.json` and `raw_logs/PATENTS/run-005/`. **This
   means the PATENTS run-005 cell is a different draw than the other 11 datasets' run-005 cells (which are
   from f74c12b)** — a deliberate, disclosed substitution to achieve a byte-exact 270/270 without
   fabrication. The fresh cell scored the same as the original (q1✅ q2✅ q3❌, 2/3), so the per-dataset
   `summary.json` and aggregate are unchanged.
