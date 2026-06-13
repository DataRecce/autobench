# Run-queue state — 2026-06-13

## RUNNING — h0056 six-lever composition, TWO concurrent full draws (captain: skip smoke)
Merged h0053 (per-key inner-join) + h0054 (lap-time exclude-pit) + h0055 (preserve-columns) onto
@baseline h0052's three (h0044 max-points + h0045 feature-boundary + h0050 scoped coverage) = ONE
six-lever README. AC-1 clean (3 added hunks only), gatekeeper APPROVE. Skipped smoke on the strength
of a **six-way mutual-non-interference decision-fork simulation: 48/48 desired-branch, 0 collisions**
(all 8 tasks 6/6; both dual-pairs airbnb009 [h0050↔h0053] and qb002/003 [h0045↔h0055] held their
correct sides). Writeup: _artifacts/h0056-decision-fork-simulation.md.
- **r1** seed 42 → handle runs/.rk-handles/h0056-full-r1-20260613-181358/ (pid 2714347), sealed_hash 22e998fa95bb0a313ed600aea936ce7f
- **r2** seed 43 → handle runs/.rk-handles/h0056-full-r2-20260613-181403/ (pid 2714516), sealed_hash 0eb370abee3244354ba6f53dd6437e98
FO owns the sentinel scan (runs/.rk-handles/*/done; ntfy on done). When BOTH land rc=0: audit
--policy strict + score each, paired delta vs @baseline (h0052), judge by committed-artifact
(AC-3/4/5) + expectation, not single-draw net. Promote if the two draws clear h0052's ~30 expectation.
h0053/h0054/h0055 stay at `smoke` (GO) as merged building blocks — conclude alongside h0056.

## @baseline = h0052 (PROMOTED 2026-06-13)

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
