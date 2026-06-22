---
title: Re-score of codex-dab-batch-baseline against latest DAB ground-truth + verifier
date: 2026-06-22
method: offline replay (no solver re-run); production verify_batch.py over answers recovered from rollout transcripts
tool: dab/tools/rescore_batch_baseline.py  (raw output: dab/tools/rescore-result.json)
non_destructive: true  (original run-dirs untouched)
---

# Question
Re-calculate the `codex-dab-batch-baseline` runs using the **latest** DAB ground truth and
verifier, without re-running the solver.

# What "latest" is
- Data submodule `~/dataagentbench/data` is at upstream HEAD `8e0eeecbe` (`ucbepic/DataAgentBench`);
  `git fetch` shows nothing newer. Only local mod is one `usaspending` bson — not a benchmark dataset.
- Diffing the validators baked into the June-21 run-dirs against the current data root: **only 4
  validators changed** — `googlelocal-q3` (accept hyphenated day-range), `PATENTS-q1/q2/q3`
  (ground-truth regeneration). The other 8 datasets' validators are byte-identical → their rewards
  cannot move.
- The verifier **runner** also advanced: the current plugin `verify_batch.py` wraps each per-query
  validator in try/except (razorback PR #19). The old runner baked in the run-dirs had no guard.

# Method
DAB validators are pure functions of the answer string (ground truth embedded as Python literals;
substring / levenshtein / number-proximity matching — no DB). So each cell can be re-scored offline by
replaying the **production** `verify_batch.py` over the solver's committed `answers.json`.

The run-dirs do **not** persist `answers.json` — only the rollout transcript + verifier outputs. So
committed answers are recovered from the rollout `.jsonl`. **Integrity gate:** recovered answers must
reproduce the *stored* `reward_per_query.json` against the *original* (run-dir-baked) validators before
any latest-verifier number is trusted. Only the 4 changed-validator cells need recovery; the 8
unchanged datasets carry forward by construction.

# Result

| Draw | run-dir | Registered? | Original | Re-scored (latest GT+verifier) |
|------|---------|-------------|----------|-------------------------------|
| draw2 | `bf113446fdd94373` | **@codex-batch-baseline** | 0.69658 (12 ds) | **0.69658 — no change** |
| draw1 | `342778d74e96f477` | no | 0.69627 (11 ds; PATENTS crash-dropped) | **0.63825** (PATENTS now included @ 0/3) |

- **Latest ground truth flips nothing.** googlelocal (both draws) and PATENTS-draw2 cross-check
  exactly AND score identically under the regenerated validators. Zero reward changes on any
  recoverable cell. (googlelocal-q3 stays pass; PATENTS-draw2 stays 0/0/0.)
- **The registered baseline (`@codex-batch-baseline` = draw2) is unchanged: 0.6966 → 0.6966.**

# The one real effect — a verifier crash, not a ground-truth change
draw1 PATENTS answered q1 as a JSON **list**. The old `validate_q1` ran `.lower()` on it
(`AttributeError: 'list' object has no attribute 'lower'`); the old runner had no per-query guard, so
the exception aborted the entire PATENTS dataset → no reward → PATENTS **silently dropped** from
draw1's stratum set (11 datasets instead of 12). draw1's 0.6963 is therefore an inflated 11-dataset
mean.

Under the latest runner the exception is caught (q1 → 0, "validator error") and PATENTS is included.
The latest `validate_q1` *still* raises on a list (confirmed) → q1 is a **definite 0**; q2/q3 are
**projected 0** (draw1 answered them as lists too, and draw2's correctly-string-formatted PATENTS still
scored 0/0/0). With PATENTS at 0/3, draw1's equal-weight stratified mean is **0.63825** (0.69627 ×
11/12).

# Caveat / limitation
draw1 PATENTS's exact q2/q3 values are **not recoverable offline**: that cell computed `answers.json`
from a DuckDB query at runtime and never echoed the full file (only debug fragments — key counts
93/35/3, endpoints `A23J`…`Y04S`). q1=0 is certain (list → guarded error); q2/q3=0 is inferred, not
byte-verified. To make draw1 PATENTS byte-exact one would either re-run that single cell, or
re-execute the agent's saved SQL (full query is in the transcript) against the PATENTS sqlite +
postgres `patent_CPCDefinition` DBs.

# Bottom line
Re-scoring `codex-dab-batch-baseline` against the latest DAB ground truth + verifier is a **no-op for
the registered baseline** (draw2, 0.6966). The latest ground-truth fixes change zero committed cells.
The only material difference is in the non-registered draw1, where the latest verifier's crash-guard
un-hides a PATENTS dataset the old verifier had silently dropped — revealing that draw1's 0.6963 was
inflated and its honest value is ~0.638.
