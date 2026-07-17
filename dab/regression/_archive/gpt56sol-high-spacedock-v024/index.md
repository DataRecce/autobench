---
id:
title: gpt-5.6-sol @ high — spacedock v0.24 (model release)
status: done
source: backfill (dab/runs/codex-dab-d22-g56sol-h2..h6)
started: 2026-07-16
completed: 2026-07-17T03:33:54Z
verdict: PASSED
score:
worktree:
issue:
pr:
trigger: model-release
model: gpt-5.6-sol
effort: high
spacedock-version: v0.24
draws:
    - codex-dab-d22-g56sol-h2
    - codex-dab-d22-g56sol-h3
    - codex-dab-d22-g56sol-h4
    - codex-dab-d22-g56sol-h5
    - codex-dab-d22-g56sol-h6
pass-at-1: 0.7218
pass-at-1-sd: 0.0409
tokens-total: 124012875
mean-session-sec: 941
artifact-url: https://claude.ai/code/artifact/eb40262c-da0b-4b80-bcf0-b565e7a5dfed
archived: 2026-07-17T03:33:54Z
---

Backfill of the gpt-5.6-sol model-release regression: spacedock harness + dab0022
semi-structured-rules README @ high, on spacedock plugin v0.24. The clean 5-draw set is
h2–h6; the earlier h1 draw ran on plugin v0.22 and is excluded to keep the harness
version uniform. No benchmark runs are launched for this entity — analysis verifies the
recorded numbers against the run dirs (including recovering the per-draw pass@1 values,
which are not yet in this file), then publishes.

## Acceptance criteria

**AC-1 — Five clean (or disclosed-substitution) full draws exist under `dab/runs/`.**
Verified by: `dab/runs/codex-dab-d22-g56sol-h{2..6}/` present with results.

**AC-2 — pass@1, tokens, and timing in frontmatter match the extractor output.**
Verified by: re-running `extract_benchmark_data.py` over h2–h6 reproduces
`strat 0.7218, sd 0.0409, min 0.6788, max 0.7797, tokTotal 124012875, meanSec 941`
(the 5.6-sol scorecard page's `sd-h` row), and the per-draw table below is filled.

**AC-3 — The run's row is live on the regression Artifacts page at the recorded URL.**
Verified by: `artifact-url` set; row visible with matching numbers and caveats.

## Draws

| draw | experiment | stratified pass@1 | notes |
|------|-----------|-------------------|-------|
| 1 | codex-dab-d22-g56sol-h2 | 0.7108 | |
| 2 | codex-dab-d22-g56sol-h3 | 0.7797 | max |
| 3 | codex-dab-d22-g56sol-h4 | 0.7589 | |
| 4 | codex-dab-d22-g56sol-h5 | 0.6808 | |
| 5 | codex-dab-d22-g56sol-h6 | 0.6788 | min |

Mean 0.7218 · sd 0.0409 · min 0.6788 · max 0.7797 (per-draw recomputed from run dirs, reproduces the scorecard aggregate)

## Caveats (travel with this row on the page)

- h1 (v0.22 plugin) excluded; this row is plugin **v0.24** throughout.
- Token total is ~2× the bare harnesses at the same model/effort — a known
  spacedock-harness-specific blow-up on gpt-5.6-sol, not a model property.
- Delta vs the v0.22 gpt-5.5 baseline row confounds model AND harness version
  (~+0.04 plugin effect); flag this wherever the two rows are compared.

## Taint audit

_(analysis stage fills this in)_

## Publication

_(published stage fills this in)_
