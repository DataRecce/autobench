# Midnight full-run batch — launch plan (captain-approved 2026-06-11)

Captain approved, on 2026-06-11, committing THREE full 48-task runs at midnight, launched
**concurrently** (prior art: h0042-full + h0043-full ran ~4 min apart on 06-10, both rc=0 — this
harbor handles concurrent fulls). Trigger = **captain pings the FO at ~00:00**; the FO then launches.
All three are at `smoke` with a recorded **GO**; the captain's midnight launch instruction IS the
smoke→full gate approval for all three. `@baseline` is currently **h0043 = 32/48**.

## The three (all smoke-GO, frozen full specs verified present)

| Hyp | Lever | Smoke GO basis | Full upside |
|-----|-------|----------------|-------------|
| h0044 | same-grain `max(points)` standings guard | f1006 flip artifact-proven; f1006-hard held; 6/6 panel | potential +1 (f1006) + stabilizes f1006-hard |
| h0045 | feature-boundary removal/toggle guard | qb002/qb004 held via narrow edits; 7/7 panel | stability/no-harm bet |
| h0046 | coverage-repair all-three-forks skeleton | airbnb009 **3/3 byte-identical** flip; canaries held | potential +1 → 33/48 (stacks on h0043) |

## Launch sequence (at midnight, per entity)

For each of h0044 / h0045 / h0046:
1. Advance frontmatter: `spacedock status --workflow-dir <wd> --set <slug> status=full` (commit `advance: <slug> entering full`).
2. Dispatch a `full`-stage ensign (reuse smoke ensign if still alive + budget ok; else fresh) to LAUNCH detached and return the handle — do NOT wait:
   ```
   export RAZORBACK_SPACEDOCK_PLUGIN_DIR="$(git rev-parse --show-toplevel)/spacedock"
   drivers/rk-run-detached.sh h0044-full specs/h0044-cumulative-standings-max-points-guard.frozen.yaml run
   drivers/rk-run-detached.sh h0045-full specs/h0045-feature-boundary-removal-toggle-guard.frozen.yaml run
   drivers/rk-run-detached.sh h0046-full specs/h0046-coverage-repair-all-three-forks-worked-skeleton.frozen.yaml run
   ```
   (`--explain` foreground first on each is fine but optional — specs already smoke-validated.)
3. FO owns the wait: scan `runs/.rk-handles/*/` each turn (ntfy fires per run). ETA ~7 hr concurrent.

## When each `done` lands (rc=0)

Re-engage that entity's ensign for `analyze`: strict audit clean + captured>0 BEFORE score;
`rk score <dir> --format json`; paired delta vs `@baseline` (h0043) — compute from
`per_trial_outcomes.json` slug-paired if `rk runs diff` TypeErrors; the §analyze required-questions
deep-dive (net + BOTH-direction ledger, smoke-vs-full, broke-a-passer, was-it-executed, prevention,
fork-drift). Then the analyze→conclude gate. Watch specifically:
- **h0046**: the single scored airbnb009 full draw (3/3 byte-identical smoke makes the trials:1
  bank-failure of h0019/h0042 less likely, but not impossible) AND the **G8 same-family blind spot**
  (only airbnb001 was canaried at smoke — full is where h0009/h0012 regressed other members).
- **h0044/h0045**: cross-family bleed at full scale (both passed targeted smokes; full is the real
  zero-bleed test — h0009/h0012 both regressed at full after clean smokes).
