---
id: spd0022
title: Focused C1-only contract — does narrowing the contract to one template recover reliability across the C1 family?
status: conclude
kind: hypothesis
source: "spd0021 trials=3 found the BROAD 7-template gated contract does not compose (1/13 leads reliable: asana001 2/3); spd0011 showed a FOCUSED single-template contract works (airbnb 2/2). This isolates: a contract with ONLY the C1 entity-completeness template, on the C1 family, trials=3. Forks champion spd0013."
started: 2026-06-28
completed: 2026-06-28
verdict: REJECTED
score:
worktree:
archived: 2026-06-28T12:00:25Z
---

## Hypothesis

spd0021 (broad 7-template gated contract) trials=3 = only **asana001 landed (2/3)**; the other 12 leads
0–1/3. spd0011 showed a **focused single-template** contract makes its rule reliably obeyed (airbnb 2/2).
**Claim:** narrowing the contract to ONLY the **C1 entity/reference-completeness** template recovers
reliability across the C1 family (asana001's siblings provider001/intercom001/netflix001/hive001 were 0/3
under the broad contract, possibly because the worker's attention was split across 7 templates).

**Single change:** fork champion `spd0013`, add a gated Implementation Contract stage with ONLY the C1
template (entity/reference-completeness: drive FROM the base/dimension relation, LEFT-attach metrics/
crosswalk, keep EVERY base-set row, never INNER-from-aggregate, preserve fan-out, never filter on a
NULL/unknown key; signature = built row count = full base-set). No C2–C7. Oracle-free; leak guard intact.

C1 family targets (all never-pass): `asana001`, `intercom001`, `netflix001`, `hive001`, `provider001`.

## Pre-smoke Decision-Fork Probe

Reachability of each C1 cell is PROVEN offline (residual catalog 2026-06-27). asana001 already landed 2/3
under the broad contract. The OPEN question is purely reliability-under-focus: does a single-template
contract make the C1 siblings land ≥2/3 (vs 0/3 broad)? trials=3 measures it directly.

## Acceptance criteria

**AC-1 — README-only; forks spd0013; adds ONLY the C1 gated contract template.** Leak guard byte-identical.
**AC-2 — clean strict audit per draw.**
**AC-3 — HOLD-RATE (trials=3): a C1 cell is "reliably fixed" at ≥2/3.** Promote only on captain sign-off,
multi-draw. Canaries hold.

## Smoke Plan

trials=3 panel (~13 cells): C1 family (asana001, intercom001, netflix001, hive001, provider001) + canaries
(apple_store001, google_play001, google_play002, mrr001, quickbooks002, activity001, tickit001). No full
board unless ≥2 C1 cells hold ≥2/3.

## Gatekeeper review

**Recommendation: APPROVE** — pure-additive C1-only gated contract stage; single idea matching the claim, leak-guard byte-identical, specs differ only in experiment/solver_workflow plus the declared trials=3 + 12-task panel, both frozen, gated lever with 7 passing canaries.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-24). Reviewed 2026-06-28T00:00:00Z.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS | Fork parent resolved: `@baseline` → `runs/spd0013-lean-lag-period-over-period/7f3278d0d61d2577`, solver_workflow spd0013 (matches `source:`). README diff vs spd0013 is pure-additive (`266a267,289`, no deletions): one new `## Stage: Implementation Contract (GATED)` containing ONLY the C1 entity/reference-completeness template. No edits to leak-guard/output-contract prose. |
| G2 leak-guard (hidden gold) | PASS | Grep hits for `gold`/`curl`/`wget`/`git clone`/`git ls-remote` all fall in the parent's PRESERVED no-fetch + anti-leak prose; the added lines contain only leak-PROTECTIVE phrasings ("never from gold values", "no gold values, counts, or dtypes are baked"). No gold table/columns named, no read-gold/fetch instruction added; no-fetch sentences byte-identical to parent. |
| G3 spec two fields | WARN→PASS | full-baseline vs panel: substantive agent-field deltas are `experiment:`, `agent.solver_workflow:`, the DECLARED `trials: 1→3`, and the 12-task `benchmark.tasks` allowlist. `agent.kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`, `reasoning_effort: xhigh` all preserved. trials=3 is the deliberate declared hold-rate variable → PASS with WARN-note, not FAIL. |
| G4 smoke narrows tasks only | PASS | No separate smoke spec by design; the panel spec IS the trials=3 probe. `--explain` (frozen) → Tasks: 12. Allowlist includes all 5 named C1 targets (asana001, intercom001, netflix001, hive001, provider001) + 7 canaries. |
| G5 both frozen | PASS | Single panel frozen file required by design: `specs/spd0022-focused-c1-contract.panel-t3.frozen.yaml` exists, carries `kind: spacedock_solver`, `runtime: codex`, `trials: 3`, content_hash sha256:48e5e43c (distinct from baseline 9660d413 and spd0021 6a000219). |
| G6 resolver fidelity | PASS | Inserted text = the C1 template verbatim from spd0021 (diff vs spd0021 confirms spd0022 = spd0021 minus C2-C7, C1 bullet byte-identical). Gate is an oracle-free workspace/shape signal; fix is a METHOD; validation signature = built row count = full base-set (structural, not self-anchored to gold). Matches the claim, no scope creep. |
| G7 actionability/inert-risk | PASS | Concrete mechanical instruction with a literal validation signature ("built row count = the full base-set / fanned-out join") and named anti-patterns (INNER-from-aggregate, filter-NULL-key). Not abstract prose; carries a structural existence/count check. |
| G8 regression-canary coverage | PASS (N/A-generative) | Lever is GATED (fires only on entity/reference/dimension/crosswalk targets; "a task that does not match the C1 shape never enters the contract path"). Panel keeps 7 currently-PASSING @baseline canaries (all 1.0: apple_store001, google_play001, google_play002, mrr001, quickbooks002, activity001, tickit001); apple_store001 is a completeness-adjacent perturbable canary. All 5 targets confirmed 0.0 (never-pass) at @baseline. |
| G9 selector independence | N/A (PASS) | No multi-candidate/selector protocol declared. |
| G10 self-correcting false-positive | PASS | Lever is self-correcting (implement→VALIDATE→obey) but (a) GATED to C1 shapes, (b) validates a STRUCTURAL invariant (built row count = full base-set), not a re-derivation against gold, and (c) the C1 fix is a build METHOD, not a mandate to replace a correct model. Structural-signature class = safe. |

**For the captain:** AUTO-APPROVED to smoke — no FAILs. This is spd0021's C1 template carved out as a focused single-template gated contract, forking champion spd0013; the README change is strictly pure-additive and leak-clean. WARN to note: by design this probe uses a SINGLE trials=3 panel spec (no separate smoke file) — trials=3 is the declared hold-rate variable, so the standard trials=1 invariant is intentionally relaxed here. The 12-task panel = 5 never-pass C1 targets + 7 passing canaries; promotion still requires ≥2 C1 cells holding ≥2/3 plus your multi-draw sign-off.

## Smoke result

## Verdict

## Stage Report: propose

- DONE: Fork the champion (cp -r spd0013 → spd0022-focused-c1-contract)
  solver_workflows/spd0022-focused-c1-contract/README.md created from spd0013.
- DONE: Edit ONLY the README to add a gated Implementation Contract stage with ONLY the C1 template
  Added `## Stage: Implementation Contract (GATED)` (gate prose from the assignment + C1 bullet byte-identical to spd0021's broadened C1); NO C2-C7.
- DONE: Keep no-external-reference / leak-guard prose byte-intact; NO gold values/counts baked
  diff vs spd0013 = `266a267,289` (pure-additive, zero deletions); added text only says "never from gold values".
- DONE: Do NOT relocate or delete any existing spd0013 guidance; only ADD the gated C1-only contract stage
  diff vs spd0013 shows additions only; G1 PASS.
- DONE: Create a trials=3 panel spec specs/spd0022-focused-c1-contract.panel-t3.yaml (12 tasks, drop stale baseline hash)
  experiment spd0022-focused-c1-contract, solver_workflow ./solver_workflows/spd0022-focused-c1-contract, trials: 3, 12-task positive allowlist; no stale content_hash carried.
- DONE: Freeze from repo root; verify content_hash non-null + differs from baseline 9660d413 AND spd0021 6a000219; trials: 3; --explain Tasks: 12
  frozen content_hash sha256:48e5e43c... (≠ 9660d413, ≠ 6a000219); trials: 3; `rk run --explain` → Tasks: 12.
- DONE: README diff vs spd0013 = ONLY the gated C1-only stage; diff vs spd0021 = spd0021 MINUS C2-C7
  vs spd0013: only the added stage; vs spd0021: C2-C7 removed + focused C1 gate intro, C1 bullet byte-identical.
- DONE: Run the gatekeeper review subagent; write the ## Gatekeeper review block
  Gatekeeper recommendation APPROVE (no FAILs); block written above.
- DONE: Do NOT launch any rk run beyond $0 --explain. Commit. Stop; the FO owns the run launch.
  Only `rk freeze` + `rk run --explain` ($0) executed; committing now.

### Summary
Forked champion spd0013 into spd0022-focused-c1-contract with a single pure-additive change: a gated
Implementation Contract stage carrying ONLY the C1 entity/reference-completeness template (spd0021's C1
bullet byte-identical, C2-C7 dropped). Built and froze the trials=3 / 12-task panel spec
(content_hash 48e5e43c, distinct from baseline and spd0021; --explain Tasks: 12). Gatekeeper auto-approved
(no FAILs; lone WARN is the by-design single trials=3 panel as the declared hold-rate variable). No rk run
launched beyond $0 --explain — the FO owns the run launch.


## Run result + Verdict (full-board trials=3)

**asana001 promotion FAILS — validated-not-promoted. @baseline stays spd0013 27/60.** Full-board trials=3
`runs/spd0022-focused-c1-contract-full-t3/6686fe7f84c0be75`. asana001's 3 draws ran CLEAN (no error) =
genuine **[0.0, 0.0, 0.0]** — the panel 2/3 did NOT reproduce at full-board scale, so the one durable lead
does not hold board-wide. Nothing to promote.

**Run also partially CONTAMINATED by a codex account usage-limit** (out of credits, resets Jul 2nd):
audit = 160 clean / 20 coverage_missing / 0 tainted; 24 q-z tasks had ≥1 usage-limit errored draw (logged
as 0). The board SCORE is therefore invalid, but asana001's own verdict is valid (its draws were clean).
Net: the focused-C1 lever produced no promotable gain; combined with spd0011/13/21, the contract mechanism
banks ZERO durable board-wide flips. @baseline unchanged.

## Clean merged board (post usage-limit recovery, 2026-06-28)

After the codex usage-limit contaminated 24 q-z tasks, the run was completed via a credit-conscious top-up
(`spd0022-focused-c1-topup2`, trials=1, 24/24 clean after a `docker network prune` fixed an address-pool
exhaustion). Merging the original run's surviving clean draws + the top-up draw per task (59 tasks at 3
clean draws, synthea001 at 2):
- **stratified pass@1 = 0.4333 ≈ 26/60**; **majority-pass (>½ draws) = 27/60**; ever-pass = 31/60.
- = the champion spd0013 (27/60) within variance → focused-C1 is BOARD-NEUTRAL, zero durable gain.
- asana001 NOT in the majority-pass set (clean 0/3) — promotion target did not land. @baseline stays spd0013 27/60.
INFRA LESSON: two "running out" failure modes hit this session — (1) codex account usage-limit (out of
credits, resets Jul 2; contaminated 24 tasks across spd0022+spd0025-full), (2) docker address-pool
exhaustion from accumulated orphaned networks (fixed by `docker network prune`). Always prune networks
between runs; never run parallel full boards (accelerates the credit burn + contaminates both).
