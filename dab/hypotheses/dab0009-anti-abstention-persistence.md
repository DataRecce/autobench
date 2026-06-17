---
id: dab0009
title: Anti-abstention + environment-persistence (forbid premature "UNABLE TO DETERMINE")
status: smoke
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

Smoke trimmed to TARGETS-ONLY (4 cells × 3 draws = 12 trials) per captain 2026-06-17; the generative-lever G8 regression panel (canaries/sentinels) is DEFERRED to the mandatory full-run gate. This smoke answers consistency-of-flip only, not board-safety.

## Smoke result

**Plain words for the captain:** The "don't quit early / try the live DB" lever WORKS — in 11 of 12
draws the solver did exactly what we asked (opened `db_config.yaml`, connected to the live
`dab-postgres`/`dab-mongo` host, and committed a real computed answer instead of bailing with "UNABLE TO
DETERMINE"). The one exception was an **infrastructure flake**, not the lever failing. But making the
solver commit a value is NOT the same as making it commit the RIGHT value: only **googlelocal-q3** flips
to PASS reliably (3/3). The other three targets are now *hard analytics problems*, not abstention
problems — the solver computes an answer every time, it's just the wrong one. **agnews-q4 is a genuine
near-tie** (5 regions within ~7 articles of each other; truth Africa came 3rd). crmarenapro-q2/q8 are
1/3 reasoning coin-flips. So Lever A is a REAL behavioral flip on the abstention axis, but it only
converts to a reward flip on 1 of 4 targets. My read: **NO-GO as a 4-target consistency flip; bank
googlelocal-q3 as the one reproducible win and the "lever reaches the artifact" proof.** Full detail
below.

**Per-target draws-passed (run-dir `runs/dab0009-anti-abstention-persistence/7de475a5c2a25626`, gpt-5.5
@xhigh, trials:3, 4 target cells = 12 trials; mean reward 0.417):**

| Target | dab0009 draws-passed | Baseline (dab0007 xhigh) | Behavioral verdict |
|--------|----------------------|--------------------------|--------------------|
| googlelocal-q3 | **3/3** | 0/1 (FAIL) | FLIPPED-REAL ×3 |
| crmarenapro-q2 | 1/3 | 0/1 (FAIL) | 1 FLIPPED-REAL, 2 COMMITTED-WRONG |
| crmarenapro-q8 | 1/3 | 0/1 (FAIL) | 1 FLIPPED-REAL, 1 COMMITTED-WRONG, 1 INFRA-INERT |
| agnews-q4 | 0/3 | 0/1 (FAIL) | 3× COMMITTED-WRONG (near-tie) |

**Distance-to-pass (DAB `validate.py` substring/ID match; concrete mismatch on a representative fail):**

- **agnews-q4** — validator: `gt = "Africa"`; checks `gt.lower() in llm_output.lower()`. Representative
  fail (`__WtYRrrx`): solver committed `South America`; its own committed ranking was
  `South America 379, North America 376, Africa 372, Europe 366, Asia 358` — Africa was **3rd, 7 articles
  off the top** across 5 near-equal buckets (~370 each). Other two draws committed `North America`. The
  miss is a near-tie classification, not a connection/abstention miss.
- **crmarenapro-q2** — validator expects exact KB id `ka0Wt000000Eq0MIAS`. Both fails (`__CitYh7a`,
  `__GHdUZ66`) committed `ka0Wt000000Ens5IAC` — a *different, plausible* knowledge article (wrong
  policy-conflict pick, one article off). Pass draw `__Tb3gqvo` committed the correct id.
- **crmarenapro-q8** — validator expects agent id `005Wt000003NIliIAG`. `__hVnigZB` committed
  `005Wt000003NBcAIAW` (wrong agent, the transfer-count ranking landed on a neighbor). `__MgEeVou`
  committed `UNABLE TO DETERMINE` → "No agent ID found" — but only after live Postgres DNS broke
  mid-trial (infra; see Failure Review). Pass draw `__WEYaD5e` committed the correct agent.

**Clean-audit attestation:** all 12 trials clean. `result.json` `n_errored_trials: 0`,
`exception_stats: {}`; `summary.json` `n_trials_errored: 0` and every cell `error_reason: null`; no cell
`result.json` carries `exception_info`. Strict audit = all 12 clean (AC-2 satisfied for the recorded
scores). NOTE: this smoke was trimmed TARGETS-ONLY per captain 2026-06-17 — the G8 canary/sentinel panel
(stockindex-q1, crmarenapro-q1/q3, googlelocal-q1) did **not** run here; board-safety is deferred to the
full-run gate (AC-3's no-canary-regress clause is unmet-because-undeferred, not failed).

## Behavioral analysis

**Headline: Lever A REACHES the committed artifact in 11/12 draws.** The env-persistence behavior is
present in every non-infra draw: solvers read `db_config.yaml` (after finding `connections.yaml` absent),
connected to the live `dab-mongo:27017` (agnews) or `dab-postgres:5432` (crmarenapro) host, and wrote a
COMPUTED value. Only ONE draw across all 12 ended in `"UNABLE TO DETERMINE"`, and that one had a genuine
DNS outage. So the abstention failure mode the lever targets is essentially eliminated — but reward only
follows on one target.

**Per target × draw:**

- **googlelocal-q3 — 3/3 FLIPPED-REAL (confirmed real persistence-driven flip).** All three draws
  (`__9ffmEqV`, `__nwkWkUs`, `__ymSKQa5`) reward 1.0, validator stdout empty (clean pass). Baseline
  dab0007 was 0/1. This is the one target where "stop quitting early + reach the live source" both fires
  AND converts to PASS, reproducibly. The legitimate bank.

- **agnews-q4 — 0/3, all COMMITTED-WRONG (lever fired, task is a near-tie), NOT inert.** Every draw
  read `db_config.yaml`, instantiated `MongoClient('mongodb://dab-mongo:27017/')`, joined ~6696 2015
  metadata rows to the Mongo articles, ran a text classifier to infer the AG-News "World" category
  (no stored category field — it must be *inferred*), then counted regions. Committed values: North
  America / South America / North America. `__WtYRrrx`'s own ranking shows the 5 regions inside a
  7-article band — a genuine near-tie where the correct bucket (Africa) was 3rd. This matches the
  dispatch caveat: agnews-q4 is a HARDER classification problem, not pure abstention; even gpt-5.5@high's
  prior pass was partly luck on the tie. **Lever A is NOT inert here — it fired in all 3; the task is
  simply a coin-toss-grade classification.**

- **crmarenapro-q2 — 1/3 (1 FLIPPED-REAL + 2 COMMITTED-WRONG).** All 3 connected to `dab-postgres` via
  psycopg2 and committed a `ka0...` knowledge-article id; none abstained. The split is pure analytic
  reasoning: pass `__Tb3gqvo` picked the correct conflicting article (`...Eq0MIAS`); the 2 fails both
  picked `...Ens5IAC` — a sibling policy article. What differs between pass and fails is *which* KB
  article the solver judged the quote to violate (a hard policy-compliance call), not whether it reached
  the data. Lever fired in all 3.

- **crmarenapro-q8 — 1/3 (1 FLIPPED-REAL + 1 COMMITTED-WRONG + 1 INFRA-INERT).** Pass `__WEYaD5e`
  connected to Postgres, computed transfer counts, committed the correct agent `005...NIliIAG`.
  `__hVnigZB` connected fine but committed `005...NBcAIAW` — wrong agent (the fewest-transfer ranking
  landed on a neighbor; analytic miss). `__MgEeVou` is the lone abstention: it probed `dab-postgres:5432`
  (initially "open"), then live DNS collapsed mid-trial with repeated
  `gaierror Temporary failure in name resolution` / `could not translate host name "dab-postgres"`; it
  retried 5×, tried 4 alternate hostnames, inspected `/etc/hosts` and `resolv.conf`, and only THEN wrote
  `UNABLE TO DETERMINE`. That is the lever working *correctly* — it exhausted every named route — against
  an unreachable source. Infra flake, not premature abstention.

**Answer to the dispatch's core question:** Lever A is **NOT inert** — it reaches the committed artifact
and eliminates premature abstention (1 abstention in 12, and that one was infra-forced after full route
exhaustion). The agnews-q4 0/3 is COMMITTED-WRONG on a near-tie, not abstention. The crmarenapro-q2/q8
1/3 splits are analytic-reasoning coin-flips between plausible ids, not connection/abstention misses.
googlelocal-q3 3/3 is a real persistence-driven flip.

## Failure Review

Non-flipping targets: agnews-q4 (0/3), crmarenapro-q2 (2/3 fail), crmarenapro-q8 (2/3 fail).

**Classification:**
- agnews-q4 ×3 → **correct-artifact-still-fail / variance** (near-tie). Lever fired, computed value
  committed, wrong region by ~7 articles across 5 near-equal buckets; an inferred-category classifier
  whose tiny variations reshuffle near-identical counts. Not fixable by an abstention/persistence lever.
- crmarenapro-q2 ×2, crmarenapro-q8 (`__hVnigZB`) → **wrong-branch / correct-artifact-still-fail**
  (analytic reasoning). Reached live Postgres, committed an id, picked a plausible-but-wrong neighbor.
  Not an abstention failure.
- crmarenapro-q8 (`__MgEeVou`) → **infrastructure** (live Postgres DNS outage mid-trial; abstention was
  the correct response after the lever exhausted all named routes + retries).

**Five failure-review questions:**
1. *Did the lever reach the committed artifact?* YES — 11/12 draws show env-persistence (db_config.yaml +
   live-host connect) and a computed value; the 1 abstention was infra-forced after full route
   exhaustion. The lever is not inert.
2. *Is the failure the lever's fault or the task's?* The task's. Three targets became near-tie /
   plausible-neighbor analytic problems once abstention was removed; one draw was infra.
3. *Reproducible or variance?* googlelocal-q3 flip is reproducible (3/3). The crmarenapro splits are
   variance between plausible answers (1/3 each). agnews-q4 is reproducibly wrong (0/3, near-tie).
4. *Would more lever text help?* No worked-example abstention skeleton would help — the solver already
   doesn't abstain. The residual misses are classification/reasoning accuracy, outside Lever A's scope.
   (The G7 inert-risk WARN did not materialize: the lever fires, it doesn't just talk.)
5. *Infra contamination of the score?* One draw (q8 `__MgEeVou`) lost to a live-Postgres DNS flake; had
   it resolved, q8 would plausibly be 2/3. The recorded score is honest but slightly infra-suppressed on
   q8.

**Next step — recommendation: FILE the bank + STOP the 4-target flip.** Recommend NO-GO on dab0009 as a
4-target consistency flip (only googlelocal-q3 meets AC-3's reproducible-flip bar; agnews-q4 and the
crmarenapro splits are task-hard / variance, not lever-addressable). Bank two durable knowledge results:
(a) **googlelocal-q3 is a real persistence-driven FLIP** (3/3, artifact-confirmed); (b) **Lever A
demonstrably reaches the committed artifact and eliminates premature abstention** (11/12; the abstention
diagnosis in `_artifacts/opus-vs-gpt55-failure-behavior.md` is the right lens, but the downstream miss is
analytic accuracy / near-tie, not quitting early). Do NOT add a worked-example skeleton (the inert-risk
WARN didn't fire). Optional probe before closing: re-run agnews-q4 / crmarenapro-q2/q8 once with the
Postgres-DNS infra confirmed healthy, to separate the q8 infra flake from true reward variance — captain's
call. This is a captain gate; FO presents, ensign does not advance the stage.

## Follow-up Routing

## Verdict

## Stage Report: smoke

- DONE: rk run --explain on specs/dab0009-anti-abstention-persistence.smoke.frozen.yaml re-confirms exactly the 4 target cells (agnews-q4, crmarenapro-q2, crmarenapro-q8, googlelocal-q3) with trials:3 (12 trials).
  `--explain` reported `Tasks: 4`, `Concurrency: 4`, model gpt-5.5, reasoning_effort xhigh. Frozen spec `trials: 3` + `concurrency.trials: 4` (12 trials). Surviving set after exclude_tasks: agnews-q4 (q1/2/3 excluded), crmarenapro-q2+q8 (all other q's excluded), googlelocal-q3 (q1/2/4 excluded) — exactly the 4 hypothesis targets.
- DONE: Detached smoke launched via drivers/rk-run-detached.sh dab0009-smoke specs/dab0009-anti-abstention-persistence.smoke.frozen.yaml run; the handle path is returned. You do NOT wait — launch, capture handle, return.
  Handle: `runs/.rk-handles/dab0009-smoke-20260617-031753/` (pid 1349665 confirmed alive; `done` absent = in flight). runs/ is gitignored — nothing to commit. Targets-only smoke (12 trials @ xhigh, concurrency 4); FO owns the wait + dispatches the post-run audit/score/deep-dive on completion.

### Summary

Smoke launch only. Re-confirmed the frozen smoke spec via `--explain` (4 target cells × trials:3 = 12 trials, xhigh, concurrency 4) and launched the detached run. Handle: `runs/.rk-handles/dab0009-smoke-20260617-031753/`. Did NOT run audit/score/deep-dive — the run is long and detached; the first officer owns the wait and dispatches the deep-dive on completion. No repo changes (runs/ gitignored), so no commit.

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

## Stage Report: smoke (deep-dive)

- DONE: ## Smoke result written: per-target draws-passed table (googlelocal-q3 3/3, crmarenapro-q2 1/3, crmarenapro-q8 1/3, agnews-q4 0/3; baseline xhigh = 0/1 each) + distance-to-pass per target + clean-audit attestation (strict audit = all 12 trials clean).
  Table + validator-mismatch per target written; clean audit from result.json (n_errored_trials:0, exception_stats:{}) + summary.json (every error_reason:null). Targets-only smoke; canary panel deferred to full-run gate noted.
- DONE: ## Behavioral analysis written: per target × per draw classified (FLIPPED-REAL / INERT / COMMITTED-WRONG / CLOSER) from codex transcript + validator output; answered "did Lever A reach the artifact or is it inert?".
  Lever REACHES the artifact in 11/12 draws (db_config.yaml + live dab-mongo/dab-postgres connect, computed value). googlelocal-q3 3/3 FLIPPED-REAL confirmed. agnews-q4 0/3 = COMMITTED-WRONG near-tie (own ranking SAm379/NAm376/Africa372 — 5 buckets in 7 articles), NOT inert. crmarenapro-q2/q8 1/3 = analytic coin-flip between plausible ids. Only abstention (q8 __MgEeVou) was infra-forced (live Postgres DNS gaierror mid-trial after 5 retries + 4 alt-hosts).
- DONE: Go/no-go recommendation with artifact evidence + ## Failure Review for non-flipping targets (classified; 5 questions answered; next step). Plain-words captain summary at top of ## Smoke result.
  Recommend NO-GO as a 4-target consistency flip; BANK googlelocal-q3 (real 3/3 persistence flip) + the "lever reaches artifact / abstention eliminated 11/12" knowledge result. Failures classified correct-artifact-still-fail (agnews near-tie), wrong-branch (crmarenapro analytic), infrastructure (q8 DNS). Did NOT advance stage (captain gate).

### Summary

Smoke deep-dive on dab0009 (Lever A: anti-abstention + env-persistence), run-dir 7de475a5c2a25626 (xhigh, 12 trials, all clean). The lever WORKS on the abstention axis — 11/12 draws committed a computed value via the live dab-mongo/dab-postgres host instead of "UNABLE TO DETERMINE"; the single abstention was a forced infra DNS outage after the solver exhausted every route. But reward only follows on googlelocal-q3 (3/3 real flip). agnews-q4 0/3 is a genuine near-tie classification (committed-wrong, not inert); crmarenapro-q2/q8 are 1/3 analytic coin-flips between plausible ids. Recommend NO-GO on the 4-target flip, BANK googlelocal-q3 + the artifact-reaching/abstention-eliminated finding. Captain gate — did not advance the stage.

### Feedback Cycles

**Cycle 1 — smoke NO-GO as a 4-target flip → REVISE scope (captain C, 2026-06-17).**

Smoke (3-draw, targets-only) result: googlelocal-q3 **3/3**, crmarenapro-q2 1/3, crmarenapro-q8 1/3,
agnews-q4 0/3 (run-dir `7de475a5c2a25626`, strict-clean).

**Lever A is validated and the README change is UNCHANGED.** Artifact read: in 11/12 draws the solver did
exactly what the README asks — opened `db_config.yaml`, connected to the live `dab-postgres:5432` /
`dab-mongo:27017` host, and committed a computed value instead of abstaining. The 1 abstention was a
genuine Postgres-DNS outage (q8 `__MgEeVou`: `gaierror`, 5 retries, 4 alt hostnames, `/etc/hosts`
checked → correctly abstained against a dead source). The G7 inert-risk WARN did NOT materialize.

**Root-cause reframe (the finding):** premature abstention was a *symptom*, not the root cause, for 3 of
the 4 smoke targets. Removing it exposed the real problem — they are **hard-analytic coin-flips**, not
abstention failures:
- agnews-q4 — near-tie inferred-category classification (committed ranking put truth `Africa` 3rd inside
  a 7-article band); reproducibly wrong, never abstaining.
- crmarenapro-q2/q8 — neighbor-ID coin-flips (committed `…Ens5` vs truth `…Eq0M`), reached over live PG.

**Scope revision:**
- **DROP** agnews-q4, crmarenapro-q2, crmarenapro-q8 from Lever A's scope — they were mis-classified;
  they need different levers (near-tie disambiguation; ID-precision) → parked as future candidate
  hypotheses, NOT filed now.
- **REFRAME** Lever A as a *board-wide anti-abstention* lever. **Confirmed win:** googlelocal-q3 (3/3,
  artifact-real). **Candidate (untested) abstention cells:** PANCANCER-q3, googlelocal-q4 — both abstained
  (`"UNABLE TO DETERMINE"`) in the dab0007 xhigh baseline, so they are Lever A's natural subclass.

**New fork to test:** do the *true* abstention cells (PANCANCER-q3, googlelocal-q4) also flip
consistently under Lever A, the way googlelocal-q3 did — or are they analytic-hard too once un-abstained?
**Probing:** no subagent probe needed — the README is validated; this is a target-set re-scope, testable
directly by a (re-)smoke on the corrected abstention set, then the full run (with the G8 panel) for net.

**q8 DNS re-run:** already artifact-confirmed as infrastructure (not variance); a re-run is low-value.

## Stage Report: smoke (cycle 2)

- DONE: Cycle-2 smoke spec built — `specs/dab0009-anti-abstention-persistence.smoke2.yaml` copied from the full spec `specs/dab0009-anti-abstention-persistence.yaml` (README + full spec UNCHANGED — Lever A validated). Adds `benchmark.tasks: [googlelocal, PANCANCER_ATLAS]` + `benchmark.exclude_tasks: [googlelocal-q1, googlelocal-q2, PANCANCER_ATLAS-q1, PANCANCER_ATLAS-q2]` so the surviving per-query set is EXACTLY {googlelocal-q3, googlelocal-q4, PANCANCER_ATLAS-q3}; `trials: 3`. Frozen.
  Query inventory from data root: googlelocal has q1-q4, PANCANCER_ATLAS has q1-q3 → excluding q1/q2 of each leaves q3,q4 (googlelocal) + q3 (PANCANCER_ATLAS) = 3 cells. `rk run --explain` reported `Tasks: 3`, `Concurrency: 4`, model gpt-5.5, reasoning_effort xhigh; solver_workflow_content_hash `ac278fa6...` (identical to cycle-1 README). Sample task = PANCANCER_ATLAS-q3. trials:3 = 9 trials.
- DONE: Detached smoke launched via `drivers/rk-run-detached.sh dab0009-smoke2 specs/dab0009-anti-abstention-persistence.smoke2.frozen.yaml run`; handle path returned.
  Handle: `runs/.rk-handles/dab0009-smoke2-20260617-043428/` (pid 1516500 confirmed alive; `done` absent = in flight). runs/ is gitignored. Spec + frozen spec committed path-scoped (cd2fbf3); razorback submodule pointer left untouched. Did NOT run audit/score/deep-dive — FO owns the wait.

### Summary

Cycle-2 smoke launch only. Re-scoped to the TRUE abstention subclass (the 3 cells that abstained "UNABLE TO DETERMINE" at the dab0007 xhigh baseline): googlelocal-q3 (re-confirm; was 3/3), googlelocal-q4 (untested), PANCANCER_ATLAS-q3 (untested). README/full spec unchanged. Frozen + `--explain` confirms exactly 3 cells × trials:3 = 9 trials @ xhigh, concurrency 4. Detached run launched, handle `runs/.rk-handles/dab0009-smoke2-20260617-043428/`. Did NOT wait — FO owns the wait and dispatches the post-run audit/score/deep-dive.
