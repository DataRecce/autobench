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

## Stage Report: full (h0043 noise-floor self-check, Phase 1 launch)

- DONE: Create TWO self-check specs by copying the h0043 FULL spec, solver_workflow UNCHANGED, change only experiment + distinct seed
  specs/h0043-selfcheck-r1.yaml (seed 42), specs/h0043-selfcheck-r2.yaml (seed 43); both keep solver_workflow ./solver_workflows/h0043-package-update-optional-resource-matrix and FULL 48 (no benchmark.tasks), trials 1
- DONE: Freeze both (rk freeze --allow-missing)
  wrote specs/h0043-selfcheck-r1.frozen.yaml and specs/h0043-selfcheck-r2.frozen.yaml
- DONE: export RAZORBACK_SPACEDOCK_PLUGIN_DIR; launch BOTH detached (2 concurrent)
  handle runs/.rk-handles/h0043-selfcheck-r1-20260613-070416 (pid 2142784); handle runs/.rk-handles/h0043-selfcheck-r2-20260613-070433 (pid 2143067)
- DONE: Return BOTH handle paths + confirm distinct run-dir hashes (NOT 7390e6adf44ba5ea)
  r1 -> c0ea198fe426cefe; r2 -> 4902035b7ce881d6; both distinct from each other and from the 7390e6adf44ba5ea reference -> CAS-buster succeeded
- DONE: Commit the new specs path-scoped
  see commit below

### Summary
Phase-1 launch-only methodology run to measure the trials:1 noise floor: re-ran the @baseline h0043 README (solver UNCHANGED) as two fresh independent full draws, busting the content-addressed run-dir cache via distinct experiment names + distinct seeds (42/43). Both landed fresh, distinct hashes (c0ea198fe426cefe, 4902035b7ce881d6), neither colliding with the existing 7390e6adf44ba5ea reference, confirming each is a genuinely-fresh draw. Both runs launched detached and are in flight; FO owns the wait and will compare both vs the h0043 reference (32/48). No hypothesis entity created; no frontmatter touched.
