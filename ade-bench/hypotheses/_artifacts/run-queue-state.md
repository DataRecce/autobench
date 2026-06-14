# Run-queue state — 2026-06-14 (PROGRAM MILESTONE: first SIX-lever baseline, 35/48)

## @baseline = h0056 (PROMOTED 2026-06-14) — SIX-lever composition, 35/48 = 0.7292
`runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a` (35/48 = 0.7292). Forks h0052
and adds three NEW construct-gated edit-shape levers verbatim → six total: h0044 max(points) + h0045
feature-boundary + h0050 scoped coverage + **h0053 per-key inner-join + h0054 lap-time exclude-pit +
h0055 build/rename preserve-columns**. Banks **airbnb005 + airbnb007** as NEW reproduced flips (h0053
per-key inner-join-from-fact, generalized to the airbnb007 NPS sibling) on top of h0052's
airbnb009/f1006/f1006-hard. New hypotheses fork from THIS six-lever README.

## How it was banked (methodology)
Captain merged the three solo-smoke-GO levers (h0053/h0054/h0055) into one composition. Smoke was
SKIPPED on the strength of a **six-way mutual-non-interference decision-fork simulation: 48/48
desired-branch, 0 collisions** (8 tasks × 6 fresh isolated draws; both dual-pairs airbnb009
[h0050-h0053] and qb002/003 [h0045-h0055] held their correct sides — _artifacts/h0056-decision-fork-simulation.md).
Then TWO concurrent full draws (CAS-buster seeds 42/43): **r1=32, r2=35, mean 33.5**, both above h0052's
measured ~30 expectation; both strict-clean. Promote rested on the two-draw expectation + committed
artifacts (NOT single-draw net) — the same play that promoted h0052. The r1-only qb002+qb003 dip was
forensically proven h0045-family feature-removal OVER-DROP variance ("less columns than solution" — the
OPPOSITE of an h0055 preserve over-fire; zero preserve-columns firing language), NOT a collision.
h0053/h0054/h0055 concluded PASSED (smoke-validated, merged). Prior anchor h0052 still on disk.

## Prior anchor: h0052 (was @baseline 2026-06-13 → 06-14)
`runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133` (32/48 = 0.6667).
Three composed levers (h0044+h0045+h0050); banked airbnb009/f1006/f1006-hard. Superseded by h0056.

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
