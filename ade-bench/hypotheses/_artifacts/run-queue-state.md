# Run-queue state — 2026-06-13 (PROGRAM MILESTONE: first composition promote)

## @baseline = h0052 (PROMOTED 2026-06-13)
`runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133` (32/48 = 0.6667).
The composition README banks **airbnb009 + f1006 + f1006-hard** as verified, reproducible, bleed-free
flips: h0044 same-grain `max(points)` + h0045 feature-boundary guard + h0050 intent-gated scoped
coverage skeleton. New hypotheses fork from THIS README.

## How it was banked (the methodology win)
Single-draw net never showed the gain (h0051 31, h0052 32 vs a lucky baseline 32). The **baseline
self-consistency run** settled it: the UNCHANGED h0043 README, re-drawn at seeds 42/43, scored
**29 and 30** — regressing the same coin-flip cells (f1011, f1005, asana003, qb004) — proving the
reference 32 was a lucky high draw (true expectation ~30). The composition's draws (31, 32) beat
both baseline-fresh draws → a real ~+1.5 gain. Promote rested on **expectation + committed artifact
+ regression forensics** (all PASS→FAIL cells proven off-construct trials:1 coin-flips), not the
single-draw net. Noise floor measured: ~±3 cells/draw.

## Nothing running. Active queue (all HELD — no captain go):
- **h0047** — coverage-repair "delete one predicate, touch nothing else" (airbnb009 alt mechanism).
- **h0048** — exploration protect-list (airbnb009 alt mechanism).
- **h0028** — answer decision-table selector adversarial re-fire (candidate-selector family, G9-gated).

## Archived this arc (REJECTED unless noted)
h0024/h0025/h0027 (selector family killed) · concept-airbnb009 (→ h0046/47/48) · h0044/h0045/h0046
(net-washed, levers validated) · h0049 (composition proven, superseded by scoped) · h0050 (scoped
lever validated at full, net-washed) · h0051 (2-lever, superseded) · **h0052 (PASSED — PROMOTED)**.
Forensics + methodology in `_artifacts/`: h0042 reproducibility-gap, h0046/47/48 decision-fork probe,
WORKFLOW-REFINE composition+self-consistency entry.
