# Run-queue state — 2026-06-12 (bare mode; @baseline = h0043, 32/48)

Live FO tracking for the airbnb009/composition program. Bare mode (team aged out mid-run);
all dispatches are fresh bare ensigns; FO owns the detached-run wait by scanning
`runs/.rk-handles/*/`.

## Running now
- **h0050-full** — handle `h0050-full-20260612-092750` (isolated airbnb009 +1 confirmation). On done rc=0 → audit/score → analyze → conclude.
- **h0052-smoke** — handles `h0052-smoke-20260612-122107` (+ airbnb009-r2/r3). The 3-lever A/B (h0044+h0045+h0050). On all done rc=0 → Phase 2 audit/artifact + A/B-vs-h0051 read → smoke gate.

## Approved, queued to launch (staggered — launch when a slot frees, keep ≤2 concurrent)
- **h0051-full** — APPROVED to full by captain (smoke was a clean GO: +3 artifact-proven flips
  f1006/f1006-hard/airbnb009, airbnb008 byte-intact, 0 regressions). **The lead +3 → 35/48 promote
  candidate.** Currently at status `smoke` (GO); advance to `full` and launch
  `drivers/rk-run-detached.sh h0051-full specs/h0051-compose-maxpoints-and-scoped-coverage.frozen.yaml run`
  the moment h0050-full OR h0052-smoke frees a slot.

## Held
- **h0047 / h0048** — hypothesis (airbnb009 alternative mechanisms; held).
- **h0028** — hypothesis (selector adversarial re-fire; held).

## On each full/analyze completion
Promote only if the run-dir net clears h0043 (32/48). The standing finding: trials:1 variance
(~±4) can wash a small net — judge by committed artifact + held targets, and bank a flip when the
run-dir actually scores >32/48. h0051's +3 margin is the best insurance yet.
