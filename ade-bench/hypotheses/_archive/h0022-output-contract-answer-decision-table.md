---
id: h0022
title: Output Contract — for an analysis/answer-style deliverable, write a per-option option->local-check->IN/OUT decision table before authoring the answer SQL, default every option OUT, and transcribe the answer string mechanically from the IN rows
status: conclude
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type Analytical-answer guess (categorical/multi-select answer with an unverified option included on plausibility)); realizes the new Output Contract stage. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed: 2026-06-08T00:00:00Z
verdict: REJECTED
score:
worktree:
---
## Hypothesis

The re-audit isolates `f1011` as a distinct, single-task failure type: the deliverable is an
**analysis answer** model (`analysis__answer`, a one-row/one-column answer string) graded
per-option. The instruction lists six statements (A–F) about a model, `analysis__lap_times`,
and asks for the letters of the true problems. The baseline self-assembled the answer from
narrative "evidence" and plausibility rather than a decisive per-option check against the
actual model SQL and source data, and the committed answer was wrong (reward 0.0, one option
flipped). Its self-attestation ("row_count=1, column_count=1, value … ; evidence supported the
letters") was a false-green: shape and a prose recap say nothing about which letters are right.

The seed solver has no rule for HOW to construct an answer-style deliverable, so it narrates
support for letters instead of forcing each option through one concrete local check before the
answer string exists.

**Falsifiable claim (the single README change — a new `## Stage: Output Contract` block,
scoped to answer-style deliverables only):** adding one stage that requires the solver, for an
analysis/answer-style model, to **write a per-option `option → local-check → IN/OUT` decision
table before authoring the answer SQL**, with the answer string transcribed mechanically from
the IN rows, will flip `f1011` and raise `stratified_pass_at_1` above the `@baseline` 0.6458.
The table carries three load-bearing mechanics: (a) **default-OUT / burden-of-proof** — an
option is IN only on a confirming local check; (b) an explicit **model-SQL reading** rule — a
value the model computes in a CTE but never emits in its final `SELECT` is a real defect (IN),
while a correctly-applied transformation is not; and (c) a **no-local-column ⇒ OUT** rule for
claims naming a phenomenon for which no column exists in any local relation, paired with the
explicit converse that a claim DECIDABLE from data the sources hold (e.g. a record-status /
completion field that exists in a staging relation while the model applies no filter on it)
is confirmed and stays IN.

**Why these mechanics, grounded in the local artifact.** The model the question is about ships
into the workspace at `environment/setup-data/analysis__lap_times.sql`. Reading it directly:
its `metrics` CTE computes both `avg_lap_time` and `avg_adjusted_lap_time`, but the **final
`SELECT` emits only `cast(round(m.avg_lap_time,0) as integer) as avg_lap_time_in_ms` — the
adjusted value the question describes is computed but never emitted** (the pit-stop-adjustment
option is a real, locally-readable defect via mechanic (b)). The model applies **no
completion/status filter on laps**, and a record-status signal IS locally present
(`stg_f1_dataset__status` exposes `statusid/status`; `stg_f1_dataset__results` carries
`status_id/status_desc`) — so the incomplete-laps option is *confirmable* from data the
sources hold and must stay IN (this is exactly why the original candidate's "source does not
hold the data ⇒ OUT" clause was deleted: applied to the status-backed option it would have
dropped a correct letter and manufactured a fresh single-task regression). By contrast, the
caution-flag option names a phenomenon for which **no column exists anywhere** in the project
(grep across all models + `setup-data` finds no caution/safety/flag column; the status table
holds only `statusid/status`), so the no-local-column ⇒ OUT rule (mechanic (a)+(c)) drops
exactly the option the solver would otherwise include on plausibility, without endangering any
confirmable option.

**Why this escapes the dead-prose ceiling.** The inert levers (h0010 0/4, h0011 0/3, h0013
0/2, h0016 0/4) all fired AT Implementation time and asked the solver to restructure or
enumerate in the moment of writing, and were acknowledged-but-not-executed — the committed
artifact was unchanged. This lever moves the control point EARLIER and changes the artifact's
precondition: the solver must first WRITE a concrete per-option decision table by reading
named local files, and Implementation becomes a transcription of the IN rows rather than a
fresh judgement. It is also scoped to answer-style deliverables, so it is a no-op on every
other task and does not license the unanchored rework that regressed h0013's second target.
It does not claim to recover any signal that lives only in the hidden oracle: every option's
verdict is decidable from the local `analysis__lap_times` SQL plus source/staging probes
(model-mechanism for the track/race-grain/pit-adjustment options, present status data for
incomplete-laps, absent column for caution-flags). Residual risk (the lever may still be
written as chatter and not reach the committed string) is real and must be checked against the
committed SQL and the per-option distance, not the transcript.

This is the burden-of-proof/decision-table refinement of the answer-style cluster; the
mutually-exclusive evidence-ledger skin was dropped as a duplicate that amplified the
regression vector against the confirmable incomplete-laps option. One idea, one stage. It is
**not** generative — it fires only when the deliverable is an answer-style model — so it is a
no-op on the cross-family canary panel by construction; the panel is carried to PROVE that
no-op, not because the rule fires everywhere. NOTE: this targets a single failure, so its
expected full-run delta is small; it is filed as the type's one on-theme bet, not a
high-leverage swing.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact: the added block references only the named model,
its SQL, and local source/staging relations — no public fetch, no oracle, no reference to
hidden `AUTO_*`/`check_option_*`/`solution__*`/verifier tests, no "equality test" / "has less
columns" / "expected output seed" tokens, and no self-anchored "drive the count to zero / re-run
your own output" phrasing. The README lines 1–32 (leak-guard + dependency guardrails) and every
other `## Stage:` block stay byte-identical; the spec differs from baseline only in
`experiment:` + `solver_workflow:` (the smoke spec additionally adds `benchmark.tasks`), with
`agent.kind: spacedock_solver` and `runtime: codex` preserved.

Target dataset (smoke, all `ade-bench-` prefixed): the analysis-answer failure —
`ade-bench-f1011`. Because a new `## Stage:` block is added (it could in principle be read on
any task even though its applicability gate makes it a no-op off answer-style deliverables),
the smoke set carries a cross-family regression panel — one currently-passing `@baseline` task
from each other family — to prove the no-op and catch any unintended bleed: `ade-bench-f1007`
(f-series, the same family as the target, exercising the solver path without being
answer-style), `ade-bench-airbnb001`, `ade-bench-ana-eng001`, `ade-bench-asana001`,
`ade-bench-quickbooks002`. **No intercom canary is possible:** intercom has no passing
`@baseline` task (intercom001/002/003 all fail), so that family cannot supply a passer — this
is structurally uncoverable, not an omission.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h<NNNN>-output-contract-answer-decision-table.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs
`codex-ade-dbt-minimal/README.md` is a single insertion of one new `## Stage: Output Contract`
block between Exploration and Implementation (one stage, one idea: the answer-style decision
table), leaves Exploration/Implementation/Validation/Finalization and the dependency/package
guardrails untouched, keeps the leak-guard prose (lines 1–32) byte-identical, and does not
reference hidden `AUTO_*`/`check_option_*`/`solution__*`/verifier tests or weaken the
leak-guard. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on `f1011` (target) + the cross-family canary panel `f1007` / `airbnb001` /
`ana-eng001` / `asana001` / `quickbooks002`, the variant must not regress any canary and should
flip `f1011` to a pass before promotion to full. The post-smoke deep-dive must confirm the flip
came from a committed per-option decision table transcribed into the answer string (read the
committed `analysis__answer` SQL and the per-option distance, not the transcript chatter), not
from an unverified re-guess.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict


## Re-triage verdict (2026-06-08) — REJECTED without running (doomed by LOW/Track-Z re-triage)

REJECTED. Same f1011 oracle-only wall as h0014, with inverted mechanics: h0022's decision-table rules
("a status-backed option stays IN" / "no-local-column => OUT") would KEEP the wrong B (status columns
exist locally) and DROP the correct D (no caution-flag column exists) — the exact opposite of the
oracle (truth ADE: B-OUT, D-IN). It manufactures a different wrong answer. f1011's local evidence is
misleading (h0031-proven); no local arbitrator exists. Retired without a run.
