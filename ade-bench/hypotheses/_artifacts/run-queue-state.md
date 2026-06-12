# Run-queue state — 2026-06-12 (bare mode; @baseline = h0043, 32/48)

Live FO tracking for the airbnb009/composition program. Bare mode (team aged out mid-run);
all dispatches are fresh bare ensigns; FO owns the detached-run wait by scanning
`runs/.rk-handles/*/`.

## Running now (2 concurrent)
- **h0050-full** — handle `h0050-full-20260612-092750` (isolated airbnb009 +1 confirmation).
- **h0051-full** — handle `h0051-full-20260612-144814` — the **lead +3 promote bet** (smoke GO: f1006/f1006-hard/airbnb009 flip, airbnb008 byte-intact, 0 regressions).

## Approved, queued to launch (staggered — launch when a slot frees, keep <=2 concurrent)
- **h0052-full** — APPROVED to full (smoke GO; A/B proved h0045's guard is FREE — h0052 == h0051 artifact-for-artifact). Serves as the **2nd independent full draw of the +3 composition** (variance hedge). Currently at status `smoke` (GO); advance to `full` and launch `drivers/rk-run-detached.sh h0052-full specs/h0052-compose-maxpoints-featureguard-scoped-coverage.frozen.yaml run` the moment h0050-full OR h0051-full frees a slot.

## Held
- **h0047 / h0048** — hypothesis (airbnb009 alternative mechanisms; held).
- **h0028** — hypothesis (selector adversarial re-fire; held).

## On each full/analyze completion
Promote only if the run-dir net clears h0043 (32/48). The standing finding: trials:1 variance
(~±4) can wash a small net — judge by committed artifact + held targets, and bank a flip when the
run-dir actually scores >32/48. PROMOTE if EITHER h0051-full OR h0052-full nets >32/48 with the +3 flips artifact-real and no lever-caused regression. Two independent draws of the same +3 composition hedge the +/-4 variance.
