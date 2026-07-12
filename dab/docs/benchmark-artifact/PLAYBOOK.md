# DAB Benchmark Artifact — Rendering Playbook

How to build/refresh the DAB benchmark **Claude artifact** result page. Follow this
when a new experiment set (e.g. **gpt-5.6-sol**) finishes so the new page uses the
exact same analysis logic and visual system as the current one.

- **Live artifact (gpt-5.5):** https://claude.ai/code/artifact/15111ba9-4ff2-4857-8705-53ad5727b6bd
- **Template:** [`dab-benchmark-template.html`](./dab-benchmark-template.html) — the current page, self-contained.
- **Extractor:** [`extract_benchmark_data.py`](./extract_benchmark_data.py) — reads run dirs → emits the page's data objects.

> Golden rule: **the page is data-in, template-out.** You almost never edit chart
> code. You regenerate three JS data objects, paste them in, adjust a few prose
> anchors, and republish. Everything else (layout, palette, charts) stays fixed.

---

## 0. What the page reports (the analysis logic)

Six configs = **3 harnesses × 2 reasoning-effort tiers**, one model, scored on DAB.
Keep this framing for the new model — just swap gpt-5.5 → gpt-5.6-sol.

The page answers, in this order, and every section is driven by the data objects:

| Section | Chart | What it shows | Data |
|---|---|---|---|
| Stat tiles | — | top config, effort-flips-ranking, most token-efficient, xhigh token premium | derived from CONFIGS |
| Stratified pass@1 | grouped bars + ±1σ whiskers + reference lines | headline score per config | `strat`, `sd`, `min`, `max` |
| The finding | slope chart | effort × README are **substitute levers** (xhigh helps bare harnesses, inverts on the rich one) | `strat` by family |
| Score vs token cost | scatter | efficiency frontier (up-and-left = better) | `strat` vs `tokTotal` |
| Execution time | grouped bars + 1800s wall | mean session wall-clock; the slow config | `meanSec` |
| Session-time distribution | box + strip (60 dots/config) | full timing shape + timeout pile-up | `DURATIONS` |
| Per-dataset pass rate | heatmap | where configs win/lose | `DATASETS` |
| Full results | table | every number | CONFIGS |

**Metric = stratified pass@1** only (each dataset weighted equally). We deliberately
**do not** show micro pass@1. We **do not** show cost/USD.

---

## 1. Prerequisites: the run set

Each config is a **CAIS-style 5-run merge** living at `dab/runs/<config-name>/` with:

- `summary.json` at the config root — the merged scores + per-dataset (used for ALL configs).
- Per-run data whose layout depends on the **harness flavor** (auto-detected):
  - `direct` (bare harness): `run-*/result.json` (token stats, non-null) + `run-*/<dataset>__*/result.json` (timing).
  - `spacedock_old`: `run-*/datasets/*/codex-output.jsonl` with `token_count` events.
  - `spacedock_new`: `run-*/datasets/*/attempts/attempt-*/codex-output.jsonl` + `codex-meta.json` + `codex-stderr.log`.
  - `harbor` (gpt-5.6-sol era, e.g. `runs/g56sol-merged/<config>/`): harbor trial dirs
    `run-*/<dataset>__*/steps/main/agent/` with `codex.txt` (exec stdout, **FO-thread-only**)
    plus `sessions/**/rollout-*.jsonl` — one rollout **per thread** (FO w/o `parent_thread_id`
    + ensign w/ `parent_thread_id`), each carrying cumulative `token_count` events.
    `result.json` `stats` is **null** in this layout, so the main extractor's `tokens_direct`
    can't help. Recover tokens with **[`rollout_tokens.py`](./rollout_tokens.py)** — it sums the
    last `total_token_usage` across every rollout (FO+ensign, no double-count), following symlinks
    so it works on both the per-draw dirs and the CAIS merge dir. Verified: reproduces the
    hand-checked direct-minimal number (44,276,047) to the token. Paste its `tokTotal:`/`tokOut:`
    output straight into CONFIGS. (Earlier codex builds logged only the FO thread → tokens showed
    `—`; the newer build logs both, so the real FO+ensign cost is now recoverable — spacedock
    dab0022 gpt-5.6-sol/high = 124.0M over the 5-run sweep, 2.80× the bare harnesses.)

Expected shape (per config): **5 runs × 12 datasets = 60 sessions**, **54 queries/run**,
**270 query-trials**. Confirm the new runs match before trusting anything.

Name the new configs consistently so the extractor guesses ids/effort correctly, e.g.
`codex-dab-spacedock-high`, `...-xhigh`, `codex-dab-direct-minimal-{high,xhigh}`,
`codex-dab-direct-structured-{high,xhigh}` (any `-high`/`-xhigh` suffix works).

---

## 2. Extract the data

```bash
cd dab/docs/benchmark-artifact
python3 extract_benchmark_data.py ../../runs \
  codex-dab-spacedock-high  codex-dab-spacedock-xhigh \
  codex-dab-direct-minimal-high  codex-dab-direct-minimal-xhigh \
  codex-dab-direct-structured-high  codex-dab-direct-structured-xhigh \
  --js > /tmp/new-data.js
```

For merged run sets living under a sub-directory (e.g. the gpt-5.6-sol CAIS merge),
point at that directory instead:

```bash
python3 extract_benchmark_data.py ../../runs/g56sol-merged \
  codex-dab-spacedock-high codex-dab-direct-minimal-high codex-dab-direct-structured-high \
  --js > /tmp/new-data.js
```

`--js` emits three paste-ready literals: `CONFIGS`, `DATASETS` (+ `COL_ORDER`),
`DURATIONS`. Without `--js` you get raw JSON for inspection.

**Sanity checks before pasting:**
- `DURATIONS` arrays are all length 60 (or whatever `runs × datasets` should be).
- `DATASETS` has the right dataset count (**12** for the current benchmark — not 13).
- Any `tokTotal:null` / `meanSec` cap is expected only where a flavor truly can't
  report it (see caveats). Investigate unexpected nulls.
- `strat`/`sd` match the config-root `summary.json`.

---

## 3. Update the template

Open `dab-benchmark-template.html` and replace the three data objects (search for
`const CONFIGS`, `const DATASETS` / `const COL_ORDER`, `const DURATIONS`).

Then do the **manual touch-ups** the extractor can't infer:

1. **`fam` labels** — the extractor emits `fam:"spacedock"`; restore the version
   suffix used on the page, e.g. `spacedock v0.26` (ask the captain what version the
   new spacedock runs are). Update every place the version string appears (see step 4).
2. **`note:` fields** — add for any lever-carrying / caveated config, e.g.
   `note:'+dab0022 lever'`. The extractor cannot know these.
3. **Model chips + copy** — replace `gpt-5.5` → `gpt-5.6-sol` in:
   - the `<title>`, the eyebrow, the `chip` row (`model gpt-5.5`),
   - the Artifact `description` when publishing.
4. **Reference lines** — `const REF = { anchor:0.6966, opus:0.6536 }`. These are the
   codex batch anchor and Opus-4.8 incumbent. Re-confirm they're still the right
   baselines for the new model; update the numbers AND their legend/label text if so.
   If a baseline is irrelevant for gpt-5.6-sol, drop that reference line.
5. **Headline prose** — the four stat tiles, the "finding" callout, and every
   `foot-note`/`footer` paragraph quote specific numbers ("0.763", "+48–59%",
   "0.743 → 0.685", "21 of 60", "~2.4×", "25.0m"). Re-derive these from the new data
   and rewrite. **Re-run the interpretation, don't copy the story** — the substitute-
   levers finding, the inversion, and the timeout story may change under a new model.
   Compute the new story beats yourself:
   - best config = max `strat`;
   - "effort flips ranking" = for how many families is xhigh > high;
   - "most token-efficient" = max `strat / tokTotal`;
   - "xhigh token premium" = per-family `(tokTotal_xhigh/tokTotal_high − 1)`;
   - timeout/censoring lines = from `timeouts`/`censored`.

Preview locally by opening the HTML in a browser; toggle OS light/dark; hover charts.

---

## 4. Publish

Use the Claude Code **Artifact** tool.

- **New page** (new model, fresh URL): publish `dab-benchmark-template.html` (or a
  copy renamed e.g. `dab-benchmark-5.6-sol.html`) with a descriptive `description`
  and `favicon: "📊"`. It mints a new URL — share that with the team.
- **Update the existing page in place** (keep the same URL): pass the existing
  artifact `url`. From a fresh conversation you MUST pass `url` or it mints a new one.
- Keep the **same favicon** (`📊`) across redeploys of the same artifact.

Decide with the captain: usually a **new model = new artifact** (so gpt-5.5 stays
comparable side-by-side), while tweaks to an existing model's page update in place.

---

## 5. Data-source reference (where each number comes from)

| Field | direct | spacedock_old | spacedock_new | harbor |
|---|---|---|---|---|
| `strat`,`sd`,`min`,`max`, per-dataset | config `summary.json` | same | same | same |
| `tokTotal`,`tokOut` | sum `run-*/result.json` `stats.n_*_tokens` | last `token_count.total_token_usage` per session, summed | **null** (see caveat) | last `token_count.total_token_usage` of **every** `sessions/**/*.jsonl` rollout (FO + ensign), summed |
| `meanSec` / `DURATIONS` | per-trial `result.json` `started_at→finished_at` | `task_complete.duration_ms` (max/session) | `codex-meta.json` `duration_s` | per-trial `result.json` `started_at→finished_at` |
| `timeouts`,`censored` | n/a | n/a | count `codex-stderr.log` "timed out" | `codex.txt` missing `turn.completed` + "timed out" |
| `failedSessions` | n/a | n/a | n/a | `codex.txt` missing `turn.completed`, other error (e.g. model-at-capacity `turn.failed`) |

`tokTotal = input + output` (cached input is a subset of input, already in input).

---

## 6. Caveats & gotchas (hard-won — read before interpreting)

- **12 datasets, not 13.** 54 queries span 12 datasets. Don't mislabel.
- **Session vs query-trial.** spacedock (and direct) solve **batch-per-dataset**:
  one codex session = one dataset. So `sessions = runs × datasets = 60`, while the
  scoring unit is `query-trials = runs × 54 = 270`. Timeouts are counted per session.
- **`codex exec --json` stdout is FO-thread-only — never read tokens from `codex.txt`.**
  The FO spawns the ensign via codex-native `spawn_agent`; the subagent thread's events
  (including its `turn.completed.usage`) are **never emitted to stdout**. The ensign is
  ~80% of real spend, so any stdout-based sum is a ~5× undercount. This is codex CLI
  behavior, not a razorback/harbor bug.
- **spacedock_new (gpt-5.5 xhigh) token usage is not recoverable** — that layout kept
  only the stdout stream, and 21/60 sessions timed out with no usage at all. The
  extractor returns `null` and the page shows `—`. Do NOT fabricate a number.
- **harbor spacedock token usage IS recoverable** — harbor mirrors `$CODEX_HOME/sessions/`
  into each trial, one rollout jsonl **per thread** (FO `thread_source: "user"` + ensign
  `thread_source: "subagent"`). `tokens_harbor()` sums the last cumulative `token_count`
  of every rollout. Validated: on direct configs this reproduces the harness-metered
  `stats.n_*_tokens` **exactly**. `tokIncompleteTrials` counts sessions that never
  reached `turn.completed` (their sum is a floor — footnote it if > 0).
- **`failedSessions` ≠ `timeouts`.** Harbor sessions can die fast on provider errors
  (`turn.failed` "model is at capacity") — they score 0 but are NOT right-censored;
  don't hatch the timing bar for them. Only "timed out" sessions are censored.
- **Right-censored timing.** spacedock_new sessions cap at the **1800s timeout wall**.
  If any hit it, the mean is a **floor**, not the true mean — mark it (`censored`,
  "⚠ floor") and say so. In the gpt-5.5 run, 21/60 spacedock·xhigh sessions capped.
- **Timing scopes differ slightly by flavor** (direct = trial wall-clock incl.
  setup+verify; spacedock = codex agent/process time). Agent dominates, so it's
  comparable at presentation level — but footnote it, as the current page does.
- **Reference baselines drift.** `@codex-batch-baseline` (0.697) and the Opus-4.8
  incumbent (0.654) are from the gpt-5.5 era. Re-resolve before quoting for a new model.
- **A 5-draw mean wobbles ±0.03.** Don't over-narrate small `strat` gaps; lean on
  the distribution/whiskers. (See the DAB variance notes.)

---

## 7. Visual system (keep it consistent)

The template already encodes this; don't drift from it:

- **Series colors:** `high = blue #2a78d6`, `xhigh = orange #eb6834` (dark-mode
  variants in `:root`). CVD-validated pair — if you ever add a series, re-validate.
- **Status/among-chrome:** green `--good` for the "best" pill only; sequential blue
  ramp for the heatmap; `--xhigh` orange for the timeout wall + censored hatch.
- **Type:** mono-forward (`ui-monospace`) for labels/eyebrows/numbers; system-sans
  for headings/body; `tabular-nums` on all figures. No web-font CDN (CSP blocks it).
- **Theme:** light + dark both via CSS tokens; charts re-render on theme toggle.
- **Honesty:** score/token/time bars start at **0**; whiskers = **±1 stdev**;
  censored data is hatched + captioned; missing data shows `—`, never zero.

---

## 8. Quick checklist

- [ ] New runs present, 6 configs, 60 sessions each, 12 datasets, 54 queries/run.
- [ ] `extract_benchmark_data.py ... --js` run; sanity checks pass.
- [ ] Three data objects pasted into the template.
- [ ] `fam` versions + `note:` levers restored; model strings swapped to gpt-5.6-sol.
- [ ] `REF` baselines re-confirmed; legend text matches.
- [ ] All prose numbers (tiles, callout, footnotes) re-derived from new data.
- [ ] Local preview: light/dark, hover tooltips, no horizontal scroll.
- [ ] Published via Artifact (new URL for new model, or `url` to update in place).
- [ ] Link shared; template copy archived if you minted a new page.
