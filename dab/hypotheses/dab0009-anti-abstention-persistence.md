---
id: dab0009
title: Anti-abstention + environment-persistence (forbid premature "UNABLE TO DETERMINE")
status: hypothesis
kind: hypothesis
source: failure-behavior study (_artifacts/opus-vs-gpt55-failure-behavior.md) Lever A; dab0007 reject -> flipped-task pivot
started:
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

## Smoke result

## Run result

## Behavioral analysis

## Failure Review

## Follow-up Routing

## Verdict
