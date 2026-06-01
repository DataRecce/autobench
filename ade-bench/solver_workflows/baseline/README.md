# ade-bench codex solver workflow (baseline)

The spacedock-solver (codex) agent reads this README per trial. Hypothesis variants
copy this directory to `../h<NNNN>-<slug>/` and edit the prose — this README is the
research's independent variable.

Work offline inside the task workspace. Inspect `instruction.md`, `task.toml`, the dbt
project files, and any local validation scripts before editing.

Repair the task-local dbt project so the requested behavior is implemented in the
project itself. Prefer the smallest clear model, macro, seed, config, or test change
that addresses the failure described by the task.

Run cheap local validation when the task provides it, such as `dbt compile`, targeted
`dbt build`/`dbt test`, or task-local shell scripts. Record only concise evidence in
your final message.

Leave the repaired project state as the graded artifact. Do not optimize for a separate
answer file, network access, package installs, or external datasets.

## Reset declaration

Between trials, razorback resets the inner-agent container, the per-trial workspace,
and any sidecar services declared in `task.toml`. Stateful learning across trials is
intentionally not supported.

## External-oracle audit (leak-guard — DO NOT REMOVE OR WEAKEN)

The workspace data is the only authoritative source. If a task is unanswerable from it,
say so rather than reaching outside. Forbidden:

- `datasets.load_dataset(...)` / `from datasets import load_dataset` / `hf://…` — HuggingFace canonical-dataset lookups.
- `huggingface_hub` / `transformers` / `evaluate` imports whose only purpose is to fetch canonical answer-key data.
- `requests.get` / `curl` / `wget` to canonical-data hosts (huggingface.co, raw.githubusercontent.com, kaggle.com, the benchmark's published dataset hub pages).
- web search (`web_search`, `web.run`) and LLM-as-oracle patterns (asking another model "what is the answer to task X?").

NOT forbidden: `pip install` of generic compute libraries (scikit-learn, pandas, numpy,
scipy, duckdb, …) that ship no canonical-data downloads.

`rk audit --policy strict` is the post-run backstop; this prose deters the paths the
runtime cannot see.
