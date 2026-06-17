---
id: dab0009
title: Anti-abstention + environment-persistence (forbid premature "UNABLE TO DETERMINE")
status: propose
kind: hypothesis
source: failure-behavior study (_artifacts/opus-vs-gpt55-failure-behavior.md) Lever A; dab0007 reject -> flipped-task pivot
started: 2026-06-17T02:53:14Z
completed:
verdict:
score: 0.9
worktree:
---

## Hypothesis

**Claim:** gpt-5.5 @xhigh loses several *flipped* tasks by **prematurely abstaining** — it writes
`"UNABLE TO DETERMINE"` after one connection-path miss instead of exhausting the named access routes
and committing a best-effort computed value. A single solver-README change that (1) forbids premature
abstention and (2) requires exhausting every named connection path before concluding a source is
absent will make these flipped tasks flip to PASS **consistently** at xhigh.

**The single README change** (fork `spacedock-readme-baseline` → `dab0009-anti-abstention-persistence`):
- **`## Rules`, line ~72** — replace `If the data doesn't support an answer, say "UNABLE TO DETERMINE"`
  with a rule that abstention is a **last resort only after exhausting all access routes**, and that a
  best-effort computed value is preferred over abstaining when the data is reachable.
- **leak-guard line ~83** — keep the leak-guard intact (still return `UNABLE TO DETERMINE` only if
  *genuinely* unanswerable from the workspace), but qualify "unanswerable" as "after every connection
  path has been tried."
- **`## Database Access` (lines ~43-66)** — add **environment-persistence** guidance: if
  `connections.yaml` is absent or a source is not visible as files, try the alternate manifests
  (`db_config.yaml`) and the **live service hosts** named in `db_description.txt` (e.g. a `dab-postgres`
  / `dab-mongo` host) via the appropriate driver before concluding the source is missing.

This is ONE idea: *don't quit early*. It does not touch the analyze/verify methodology or the answer
format. The leak-guard (no external data) is preserved verbatim.

**Target queries (flipped — PASS in gpt-5.5@high, FAIL at the xhigh reference dab0007):**
`agnews-q4`, `crmarenapro-q2`, `crmarenapro-q8`, `googlelocal-q3`. Behavioral evidence per target is in
`_artifacts/opus-vs-gpt55-failure-behavior.md` (§2/§3) and `opus-vs-gpt5.5-failure-modes.md`.

## Pre-smoke Decision-Fork Probe

- **Fork tested:** abstain vs. persist-and-commit, on a source that *appears* missing but is reachable.
- **Prompt context (solver-visible):** `db_description.txt` (names the live store), the absent
  `connections.yaml` / dump folder, the present `db_config.yaml`.
- **Control (A) result — baseline README:** at xhigh the solver hit one path miss, the README's line-72
  sanction kicked in, and it committed `"UNABLE TO DETERMINE"` → FAIL. Verified in the dab0007 cell
  transcripts (crmarenapro-q2: never opened `db_config.yaml`, 0 psycopg2 attempts; agnews-q4: never
  instantiated a `MongoClient`).
- **Proposed-rule (B) result — strongest available proxy:** **gpt-5.5 @high already exhibits the target
  behavior** on these exact cells — it read `db_config.yaml`, connected to the Postgres/live-Mongo host,
  and committed a computed value → PASS (codex-dab-baseline transcripts). Same model, same tier family;
  the capability is proven present. The lever's job is to make xhigh *reliably* do what high already does.
- **Exact README wording tested:** the line-72 / line-83 / Database-Access edits above.
- **Expected artifact signature in a real run:** the committed answer for each target is a **computed
  value** (a name/number/ranking), and the transcript shows ≥1 attempt against the alternate manifest or
  live host — NOT `"UNABLE TO DETERMINE"`.
- **Why this justifies smoke (not just a number):** the proxy is *real same-model artifact evidence*
  (high already does it), not a subagent sim, so the false-GO risk (sim ≠ production) does not apply.
- **Caveat:** proxy is the @high run, a different tier; the smoke at xhigh is the real test of whether
  the README rule alone (without the lower tier) reproduces the behavior.

## Acceptance criteria

**AC-1 — Exactly the README changes; full spec differs from `specs/dab0007-gpt55-baseline-xhigh.yaml`
only in `experiment:` + `solver_workflow:`.** Verified by `diff`.

**AC-2 — Every recorded score paired with a clean strict audit.**

**AC-3 — Consistency, not a single flip.** Across the **3 smoke draws**, the flipped targets pass
*reproducibly* (report draws-passed per target; the bar is a clear improvement over the xhigh reference's
0/1, judged with the committed-artifact read — abstention→computed-value — not the bare reward), AND
no sentinel/canary regresses in any draw. A lone 1/3 flip with no artifact change is NOT a GO.

**AC-4 — Leak-guard intact.** The forked README still forbids external data / ground-truth lookup; the
only relaxation is *premature* abstention, not the no-external-reference rule.

## Gatekeeper review

**Recommendation: APPROVE** — no FAILs; clean generative lever with a correctly-stratified canary panel (stockindex cross-dataset + crmarenapro-q3 perturbable same-dataset). One G7 WARN (env-persistence is partly abstract-structural prose, though anchored by concrete `ATTACH ... (TYPE POSTGRES/MONGO)` tokens) carried to the captain.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-17T03:10:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is non-empty and adds one idea — "don't quit early." Two hunks (`## Database Access` env-persistence block at 67a68; `## Rules` line-72 abstention rule at 72c86) plus the consequential leak-guard re-phrasing at 83c101. All three serve the single anti-abstention/persistence claim; no analyze/verify methodology or answer-format section touched. |
| G2 leak-guard intact | PASS | grep of added (`^>`) lines for `ground_truth`/`db_description_withhint`/`curl`/`wget`/`git clone`/`datasets.load_dataset`/`huggingface`/`hf:`/`web search` = none. The 83c101 edit only qualifies "unanswerable" as "after every named connection path has been tried" — it does not remove or soften the no-external-data rule; the only relaxation is *premature* abstention. Added text references `db_description.txt` (visible workspace file), not the withheld `db_description_withhint.txt`. |
| G3 spec two fields | PASS | `diff dab0007-gpt55-baseline-xhigh.yaml dab0009…yaml` = only `experiment:` + `solver_workflow:` changed. `agent.kind: spacedock_solver`, `runtime: codex`, `reasoning_effort: xhigh`, `trials: 1`, `concurrency.trials: 4` all preserved (dab0007 is the correct AC-1 parent). NOTE: diffing vs `dab-anchor-codex.yaml` additionally shows reasoning_effort high->xhigh and trials 2->1 — those are inherited from the dab0007 xhigh reference, NOT introduced here; not a G3 fail. |
| G4 smoke tasks+exclude | PASS | `diff full -> smoke` adds only `benchmark.tasks` (dataset names: agnews, crmarenapro, googlelocal, stockindex) + `benchmark.exclude_tasks` (q-ids), plus the deliberate smoke-only trials 1->3 deviation (see captain note). `tasks` uses dataset names (not per-query ids). Surviving 8-query set per ensign `rk --explain` (`Tasks: 8`) includes all 4 hypothesis targets (agnews-q4, crmarenapro-q2/q8, googlelocal-q3) + sentinels crmarenapro-q1 & googlelocal-q1. Regression sentinels present, so no WARN. |
| G5 both frozen | PASS | `ls` confirms both `dab0009…frozen.yaml` and `dab0009…smoke.frozen.yaml` exist; both carry `kind: spacedock_solver` + `runtime: codex` (lines 4-5 of each). |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: line-72 becomes "Abstention … is a LAST RESORT, used only AFTER you have exhausted every named connection path … commit a best-effort COMPUTED value rather than abstaining"; Database-Access block adds the alternate-manifest + live-host persistence guidance. Generative/independent, NOT self-anchored — no "re-run your own query"/"verify your answer matches" phrasing. No scope creep beyond the claimed idea. |
| G7 actionability/inert-risk | WARN | The abstention rule is a concrete behavioral directive (commit a computed value, don't abstain on one path miss) and the env-persistence block names mechanical tokens (`db_config.yaml`, `ATTACH ... (TYPE POSTGRES)`, `LOAD mongo` / `ATTACH 'mongodb://<host>:27017/dbname' ... (TYPE MONGO)`) — those land. But "exhaust every named connection path before concluding a source is missing" is partly abstract-structural prose with no worked-example skeleton; at gpt-5.5/xhigh this risks "talks but doesn't do." Inert-risk: solver may discuss persistence but still abstain. (WARN-only; never blocks.) |
| G8 regression-canary coverage | PASS | Instruction is GENERATIVE (abstention rule + env-persistence fire on every query, not gated to targets) -> G8 applies. Smoke set keeps `@baseline` passers from a non-target dataset: stockindex-q1=1.0 (cross-dataset canary, one of the three perfect-score datasets). Same-dataset perturbable canary crmarenapro-q3=1.0 survives — a crmarenapro passer the anti-abstention lever could push to over-commit, so it can actually FIRE. Sentinels crmarenapro-q1=1.0 + googlelocal-q1=1.0 also survive. Panel has ≥1 non-target passer + ≥1 perturbable canary on the shared-construct dataset. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — single anti-abstention behavioral lever, one solver session per query. No N-candidate generation or scored selection. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever. README text never instructs "verify a result and replace on disagreement"; it tells the solver to keep trying access routes and commit a computed value, with no second-derivation reconcile step. Confirmed from the inserted README prose. |

**For the captain:** Clean APPROVE — integrity rules (G2/G3/G6) all PASS, generative lever carries the right stratified canary panel (stockindex-q1 cross-dataset + crmarenapro-q3 perturbable same-dataset). AUDITABLE DEVIATION: the smoke spec deliberately raises `trials: 1 -> 3` (full stays trials:1) — this is the intended 3-draw consistency measure of AC-3, not a G3/G4 violation; concurrency.trials stays 4. One thing to watch: the G7 inert-risk WARN — "exhaust every connection path" is partly abstract prose; if the smoke shows the solver discussing persistence but still abstaining, consider adding a worked-example connect-then-compute skeleton before promoting.

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict

## Stage Report: propose

- DONE: README forked + edited = EXACTLY Lever A and nothing else
  `solver_workflows/dab0009-anti-abstention-persistence/README.md`; `diff` vs parent `spacedock-readme-baseline` shows only 3 hunks — (a) `## Rules` line-72 abstention rule rewritten (UNABLE TO DETERMINE = last resort after exhausting every connection path; best-effort COMPUTED value preferred when reachable); (b) `## Database Access` env-persistence block (db_config.yaml + live hosts in db_description.txt via the right driver before concluding a source is missing); (c) leak-guard qualified "after every connection path" but no-external-data forbidden list preserved verbatim (AC-4). analyze/verify methodology + answer format untouched.
- DONE: Full spec `specs/dab0009-anti-abstention-persistence.yaml` differs from dab0007 only in experiment + solver_workflow (AC-1)
  `diff specs/dab0007-gpt55-baseline-xhigh.yaml specs/dab0009-anti-abstention-persistence.yaml` = 2 fields; trials:1, concurrency.trials:4, xhigh, all 12 tasks preserved.
- DONE: Smoke spec adds benchmark.tasks + benchmark.exclude_tasks + trials:3
  4 datasets (agnews/crmarenapro/googlelocal/stockindex) + 16 exclude ids → surviving 8 = targets agnews-q4/crmarenapro-q2/crmarenapro-q8/googlelocal-q3 + sentinels crmarenapro-q1/googlelocal-q1 + canaries stockindex-q1 (cross-dataset) / crmarenapro-q3 (perturbable). trials:1→3 (3-draw consistency, smoke-only); concurrency.trials:4 (schema cap is 4, dispatch's "e.g. 6" not allowed). Both frozen; `rk run …smoke.frozen.yaml --explain` reported `Tasks: 8`.
- DONE: Gatekeeper subagent run; per-rule table + APPROVE/REVISE/REJECT written into `## Gatekeeper review`
  Recommendation APPROVE (no FAILs; one G7 WARN inert-risk). Trials:3 deviation audited in the review. Baseline rewards resolved from dab0007 per_trial_outcomes.json for the FO smoke-set table.

### Baseline (dab0007 xhigh) rewards for the propose-gate smoke table

| Task | Baseline | Should-pass | Role |
|------|----------|-------------|------|
| agnews-q4 | 0.0 | ✅ | TARGET (flip) |
| crmarenapro-q2 | 0.0 | ✅ | TARGET (flip) |
| crmarenapro-q8 | 0.0 | ✅ | TARGET (flip) |
| googlelocal-q3 | 0.0 | ✅ | TARGET (flip) |
| crmarenapro-q1 | 1.0 | ✅ | sentinel (stay PASS) |
| googlelocal-q1 | 1.0 | ✅ | sentinel (stay PASS) |
| stockindex-q1 | 1.0 | ✅ | cross-dataset canary (G8) |
| crmarenapro-q3 | 1.0 | ✅ | perturbable canary |

Net target: 4 FAIL→PASS, 4 passers hold. 8 tasks × 3 draws = 24 trials @ xhigh, concurrency 4.

### Summary

Authored dab0009 (Lever A: anti-abstention + environment-persistence) entirely as a one-idea solver-README fork. The README forbids premature `"UNABLE TO DETERMINE"` (last resort only, computed value preferred) and adds environment-persistence (try db_config.yaml + the live hosts in db_description.txt before declaring a source missing); leak-guard preserved verbatim. Full spec is a clean 2-field fork of dab0007; smoke spec selects exactly the 4 flip targets + a 4-query sentinel/canary panel at trials:3. Both frozen, --explain confirms `Tasks: 8`. Gatekeeper = APPROVE with one G7 inert-risk WARN (env-persistence is partly abstract prose; watch for talks-but-doesn't-do in smoke). No rk run launched — awaits captain's propose-gate GO.
