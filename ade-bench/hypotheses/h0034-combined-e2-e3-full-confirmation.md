---
id: h0034
title: Combined confirmation -- E2 anti-cross-join (airbnb009) + E3 rolling-window calendar-RANGE-copy (airbnb007) in ONE variant; full 48-task confirmation + promote
status: analyze
kind: hypothesis
source: _proposal/oracle-problem-systematic-program.md (E2+E3 batch-full, captain 2026-06-07); confirms h0019 (airbnb009 smoke-GO) + h0018 (airbnb007 smoke-GO) at full scale in ONE run (run-economy + interaction check); promote @baseline if the paired delta clears.
started: 2026-06-07T16:22:23Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

*(Seeded by the FO; the propose stage builds the combined variant + FULL spec.)*

E2/h0019 (anti-cross-join, airbnb009) and E3/h0018 (rolling-window expressed as a calendar-date RANGE
copied from the project's own passing sibling, airbnb007) BOTH flipped their targets at smoke,
artifact-proven (the committed SQL carried the prescribed shape), with zero canary regression. Both
are independent single-rule **Implementation-stage** additions with copyable worked examples. This
combined variant carries BOTH rules and runs the **full 48-task confirmation in one run** (cheaper
than two separate fulls; also checks the two rules do not interact to harm passers) before promotion.

**Falsifiable claim:** the combined variant holds BOTH flips (airbnb007 + airbnb009 PASS) at full
48-task scale with zero NET regression; the paired `rk runs diff` delta vs `@baseline` clears the
tripwire (CI excludes a regression) on a clean strict audit; and `stratified_pass_at_1 > 0.6458`.
**Promote `@baseline`** on success. Falsified if either flip reverts at full (variance), if the two
rules interact to regress passers, or if the net delta does not clear.

This combined run **skips smoke** (both levers were already smoke-GO'd individually): `propose -> full`.

## Acceptance criteria

**AC-1 -- Combined variant README = baseline + EXACTLY the two Implementation rules.** The forked
README adds the h0019 anti-cross-join rule AND the h0018 rolling-window calendar-RANGE-copy rule
(both lifted VERBATIM from their smoke-GO forks `solver_workflows/h0019-*` and
`solver_workflows/h0018-*`), and nothing else; leak-guard + other stages byte-identical to
`codex-ade-dbt-minimal`. The FULL spec differs from `specs/baseline.yaml` only in `experiment:` +
`solver_workflow:` and carries NO `benchmark.tasks` selector (all 48). `kind: spacedock_solver`,
`runtime: codex`, `trials: 1` preserved.

**AC-2 -- Clean strict audit on the full run** (`tainted: 0`, `captured > 0` every cell).

**AC-3 -- Verdict by the paired `rk runs diff @baseline <run>` delta (CI, adjusted p) + absolute
`stratified_pass_at_1` vs 0.6458.** Promote only if the delta clears the tripwire AND both target
flips (airbnb007, airbnb009) hold artifact-proven AND no passer regressed.

## Gatekeeper review

**Recommendation: APPROVE** — confirmation/promote variant: two PREVIOUSLY-SMOKE-GO'd
Implementation rules (h0019 anti-cross-join + h0018 rolling-window calendar-RANGE) lifted
VERBATIM into ONE in-stage fork; leak-guard byte-identical; full spec two-field; clean combination.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T16:30:00Z.

Fork parent resolved: `source:` names `codex-ade-dbt-minimal` (seed); `rk registry resolve run
@baseline` → `runs/ade-bench-baseline/622bdedac572b479`, whose `solver_workflow` =
`solver_workflows/codex-ade-dbt-minimal` (content hash `133891fa…`). Both agree → `<parent-solver>`
= `codex-ade-dbt-minimal`, the dir forked and diffed against.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Diff vs parent adds only inside `## Stage: Implementation` (no `## Stage:` header in the diff; 4 stage headers in both parent and fork). **Confirmation variant:** intentionally carries TWO rules, but BOTH are previously-smoke-GO'd, BOTH live in the SAME Implementation stage, combined for run-economy + interaction check (per captain). Gate question = clean combination + leak-guard, not single-idea. |
| G2 leak-guard intact | PASS | Header/leak-guard lines 1–49 byte-identical to parent; grep over the 86 added lines finds none of AUTO_/solution__/check_option_/verifier/equality test/expected output seed/Got N/curl/wget/git clone/git ls-remote. |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0034-…yaml` shows only `experiment:` + `solver_workflow:`. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. NO `benchmark.tasks` (all 48). |
| G4 smoke tasks-only | N/A | No smoke spec — this run skips smoke (propose→full); both levers were smoke-GO'd individually (h0019 airbnb009, h0018 airbnb007). |
| G5 both frozen | PASS | `specs/h0034-…frozen.yaml` exists, carries `kind: spacedock_solver` + `runtime: codex`. No smoke frozen by design (skips smoke). |
| G6 resolver fidelity | PASS | Combined added-set is set-equal to (h0019 added 43 lines) ∪ (h0018 added 43 lines) = 86 lines, VERBATIM. Both rules are gated/generative-constructive derivations (how to build the SQL) with worked examples — neither is self-anchored "check your own work." Matches the claim (carry BOTH flips). |
| G7 actionability/inert-risk | PASS | Both rules carry a worked-example SQL skeleton (BEFORE/AFTER cross-join; WRONG/RIGHT rows-frame vs calendar-RANGE) — the copyable few-shot form, not abstract structural prose. Already smoke-proven to reach the committed artifact. |
| G8 regression-canary coverage | N/A | Both rules are GATED on narrow preconditions (h0019: completeness-repair carrying a secondary grouping column; h0018: a rolling "over last N days" window-suffixed column), not blanket-generative. Also a FULL 48-task run — all 48 ARE the panel; no smoke subset to under-cover. |
| G9 selector independence | N/A | No multi-candidate / selector protocol — two single-shot Implementation derivations. |
| G10 self-correcting false-positive | N/A | Neither rule is a verify-and-fix-on-disagreement lever; both are constructive Implementation derivations (build the SQL this shape), not reconcile-and-replace against a re-derived check. |

**For the captain:** No FAILs. This is a confirmation/promote variant, not a new idea — the two
rules read as independent, non-overlapping paragraphs (disjoint preconditions:
completeness-repair vs rolling-window column), both lifted byte-for-byte from their smoke-GO'd
forks. Decide: advance to the FULL 48-task run (skips smoke). The full run itself is the
interaction check (do the two rules harm any passer when both are live).

## Smoke result

## Run result

**IN PROGRESS** (launched 2026-06-07T16:32Z) — FULL 48-task confirmation run.

- **Spec:** `specs/h0034-combined-e2-e3-full-confirmation.frozen.yaml` (all 48 tasks, no selector; `kind: spacedock_solver`, `runtime: codex`, `trials: 1`).
- **Run dir:** `runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303/`
- **PID:** `2522572` (detached `nohup`; log `/tmp/rk-h0034-full.log`, pid `/tmp/rk-h0034-full.log.pid`).
- **Launch cmd:** `RAZORBACK_SPACEDOCK_PLUGIN_DIR=$(git rev-parse --show-toplevel)/spacedock; nohup uv run --project ../razorback rk run specs/h0034-combined-e2-e3-full-confirmation.frozen.yaml --runs-dir runs > /tmp/rk-h0034-full.log 2>&1 &`
- **Confirmed started:** run dir + `result.json`/`job.log`/`config.json` present; first cell `ade-bench-airbnb001__Dmadk6o` image built (`ade-bench-airbnb001__dmadk6o-main:latest`, in use) and agent bootstrap underway in `job.log` (NVM/node 22 + `@openai/codex@latest` install). `--explain` resolved the combined solver README cleanly beforehand.
- **ETA:** ~7 h (48 tasks × ~9 min, serial n_concurrent_trials=1).
- **Next (FO):** adopt the completed run for strict audit (`tainted: 0`, `captured > 0`) + `rk score --format json` + paired `rk runs diff @baseline <run>` (CI/adjusted p) + absolute `stratified_pass_at_1` vs 0.6458; verify both target flips (airbnb007, airbnb009) hold artifact-proven and no passer regressed; promote `@baseline` on success.

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: Combined variant fork = codex-ade-dbt-minimal + EXACTLY the two Implementation rules lifted VERBATIM
  `solver_workflows/h0034-combined-e2-e3-full-confirmation/README.md`; combined added-set is set-equal to (h0019 added 43 lines) ∪ (h0018 added 43 lines) = 86 lines; both rules inside `## Stage: Implementation` (h0019 anti-cross-join + worked example before "Run basic confirmation", h0018 rolling-window calendar-RANGE + worked example after it); header/leak-guard lines 1–49, Exploration, Validation, Finalization all byte-identical to parent; no AUTO_*/solution__*/Got N tokens.
- DONE: FULL spec specs/h0034-…yaml differs from baseline.yaml ONLY in experiment: + solver_workflow:, NO benchmark.tasks (all 48); frozen via rk freeze --allow-missing
  `diff specs/baseline.yaml specs/h0034-…yaml` = the two fields only; `kind: spacedock_solver`/`runtime: codex`/`trials: 1` preserved; `specs/h0034-…frozen.yaml` written (`tasks: null` = all 48). No smoke spec (run skips smoke).
- DONE: Gatekeeper ran; ## Gatekeeper review block written (per-rule PASS/WARN/FAIL + overall)
  APPROVE, no FAILs; G1 = two PREVIOUSLY-SMOKE-GO'd rules combined for confirmation, G2 leak-guard byte-identical, G3 spec two-field; G4/G8/G9/G10 N/A (no smoke / gated rules / no selector / not self-correcting). Fork parent resolved to `codex-ade-dbt-minimal` (source + @baseline registry agree).

### Summary

Built the combined confirmation variant (h0034) by forking `codex-ade-dbt-minimal` and lifting the two already-smoke-GO'd Implementation rules VERBATIM into one fork: h0019's anti-cross-join rule (airbnb009) and h0018's rolling-window calendar-RANGE-copy rule (airbnb007), each with its worked-example skeleton, both inside `## Stage: Implementation` with disjoint preconditions (completeness-repair vs rolling-window column) so they read as two independent, non-interacting rules. Set-diff confirms the combined additions = union of the two source forks' additions, byte-for-byte; everything outside Implementation is byte-identical to the parent. Built and froze ONLY the FULL 48-task spec (two-field delta vs baseline, no task selector, no smoke spec — this run goes propose→full since both levers were smoke-GO'd individually). Gatekeeper recommendation: APPROVE (no FAILs). Propose STOPS at the gate — no `rk run` launched; the FULL run is the next stage.

## Stage Report: full

- DONE: The FULL 48-task run is LAUNCHED DETACHED on specs/h0034-combined-e2-e3-full-confirmation.frozen.yaml: nohup, stdout/err -> /tmp/rk-h0034-full.log, PID -> /tmp/rk-h0034-full.log.pid; confirm it actually started (run dir + first cell/image-build underway). Record run-dir + PID in ## Run result (mark 'in progress').
  Run dir `runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303/`, PID `2522572` (alive). First cell `ade-bench-airbnb001__Dmadk6o` image built (`ade-bench-airbnb001__dmadk6o-main:latest`, in use); `job.log` shows agent bootstrap (NVM/node 22 + `@openai/codex@latest`). `--explain` resolved the combined README cleanly. `## Run result` marked IN PROGRESS.
- DONE: Report the run-dir path + PID + that the run is in progress, then STOP. Do NOT poll/hold for the ~7-hour duration -- the FO adopts the completed run for audit + score + analyze.
  Launch-only assignment honored: no audit/score launched (run not done); no second run launched; stopping after this commit + completion signal.

### Summary

Launched the FULL 48-task confirmation run for the combined E2+E3 variant detached via `nohup` after a clean `--explain` sanity check. The run is in progress: run dir `runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303/`, PID `2522572` (alive), log `/tmp/rk-h0034-full.log`. First cell (airbnb001) image is built and the codex agent bootstrap is underway in `job.log`. Per the assignment I did NOT poll/hold for the ~7 h duration and did NOT run audit/score — the FO adopts the completed run for the strict audit + score + paired `rk runs diff` + promote decision.
