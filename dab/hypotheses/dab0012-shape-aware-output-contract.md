---
id: dab0012
title: stockmarket-q3 - shape-aware output contract (scalar/ranking -> terse names+numbers; list -> full enumeration)
status: propose
kind: hypothesis
source: dab0001 ideate (retargeted to stockmarket-q3); _artifacts/model-strengths-cross-learning.md §2a + §4
started: 2026-06-18T08:50:00Z
score: 0.9
---

## Hypothesis

gpt-5.5 fails `stockmarket-q3` 0/6 NOT on a compute gap but on output SHAPE: it computes the exact
same 15 financially-troubled NASDAQ companies and the same 2008 average-volume numbers Opus does
(Opus passes 5/6), then **decorates each ranking row with the company's description** ("Apex Global
Brands Inc. specializes in creating and marketing…: 23781.42; …"). The verifier's normalized-string
match rejects the narrative. Opus emits `name: number; name: number` and passes. This is the
cleanest output-shape signal in the target set: the answer is already correct, only the shape is
wrong (`_artifacts/model-strengths-cross-learning.md` §2a, raw-log audited).

The fix is **shape-aware** because the two output biases are in TENSION. A blunt "be terse / answer
only the question" rule fixes stockmarket-q3 but BREAKS `yelp-q6`, where the gold answer is a
multi-element category LIST and Opus's terseness drops elements (Opus 1/6; gpt passes 4/6 by
emitting the full list). So the rule MUST branch on answer SHAPE.

**The README change** (fork `spacedock-readme-baseline` -> `dab0012-shape-aware-output-contract`),
ONE idea, in the `## Rules` section. The existing line `Answer ONLY the question — no commentary
or counter-examples` has proven insufficient (gpt still injects descriptions), so REPLACE it with a
shape-branched contract:

> **Match the answer's shape to the question, then write nothing extra.**
> - **Scalar or ranking answer** (a single value, or a `name: number; name: number; …` ordered
>   list): emit ONLY the entity names and their numeric values. Do NOT append a description,
>   definition, explanation, or any narrative about an entity — the row is `name: number`, never
>   `name (what it does): number`.
> - **List answer** (the question asks for the categories / tags / set / "and its X" of an entity):
>   emit the COMPLETE enumeration of every element, comma-separated. Do NOT collapse a multi-element
>   list to its first element.
>
> Worked example (foreign domain): for "rank the 3 longest rivers by length," write
> `Nile: 6650; Amazon: 6400; Yangtze: 6300` — not `Nile (a river in Africa flowing north): 6650; …`.
> For "name the busiest airport and the airline alliances operating there," write
> `Hartsfield-Jackson; Star Alliance, Oneworld, SkyTeam` — emit all three alliances, not just the first.

The foreign-domain worked examples (rivers / airports) avoid leaking the target schema into the
README and avoid contaminating any decision sim (per the leak-catch rule in
`ade-bench-sim-validates-tendency-not-real-run`).

## Targets

- **PRIMARY flip — stockmarket-q3** (gpt 0/6, Opus 5/6): must flip to PASS. Acceptance = the scalar/
  ranking branch suppresses the description injection so the ranking string matches gold; verified
  by committed artifact (the emitted answer string for q3 is `name: number; …`, no descriptions).
- **LOAD-BEARING regression canary — yelp-q6** (gpt 4/6, VARIABLE list-answer cell): MUST NOT regress
  below its 4/6 band. This is the cell a terse-only rule would break; the list branch exists to
  protect it. A drop here falsifies the shape-awareness of the rule.
- **Stable format-sensitive canaries to hold** — bookreview-q1 (6/6), stockmarket-q1/q2/q5 (6/6),
  yelp-q1/q2/q3/q5 (6/6): no regression (the rule must not perturb already-passing format-sensitive
  ranking/list cells).

## Acceptance criteria (falsifiable)

- **GO** iff stockmarket-q3 flips to PASS by committed artifact AND yelp-q6 holds at/above its 4/6
  band AND no ROCK-STABLE (6/6) canary drops — judged per-cell against the 6-draw band in
  `_artifacts/baseline-variance-6draw.md`, never on a single draw (standing captain rule:
  single-trial, judge by committed artifact + bleed-free canaries).
- **NO-GO / falsified** if stockmarket-q3 stays FAIL (the description injection is not the cause, or
  the rule does not suppress it), OR if yelp-q6 drops below its band (the rule is effectively
  terse-only and the list branch failed to protect the list answer).

## Smoke set

| Task | Baseline (6-draw) | Should-pass after lever | Role |
|---|---|---|---|
| stockmarket-q3 | 0/6 | PASS (flip) | 🎯 primary flip |
| yelp-q6 | 4/6 (variable) | hold ≥4/6 | ❌ load-bearing perturbable list canary |
| bookreview-q1 | 6/6 | PASS | ✅ stable format-string canary |
| music_brainz_20k-q1 | 6/6 | PASS | ✅ cross-dataset regression sentinel (perfect-score dataset, not a target's) |

The 4th cell is `music_brainz_20k-q1` (not stockmarket-q1) to satisfy gatekeeper G8: a generative
shape contract fires on every query, so the regression panel needs ≥1 passer from a dataset OTHER
than the targets' (stockmarket/yelp). music_brainz_20k is a perfect-score dataset and is not a
target's dataset, so it is the cross-dataset tripwire. Surviving smoke set confirmed exactly 4 via
`rk run specs/dab0012-shape-aware-output-contract.smoke.frozen.yaml --explain` (`Tasks: 4`).

## Gatekeeper review

**Recommendation: APPROVE** — single-idea shape-aware output contract in `## Rules`, integrity rules (G2/G3/G6) all clean, generative-canary coverage present; one WARN that the load-bearing perturbable canary (yelp-q6) is the only genuinely fireable list-branch cell.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-18T09:40:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is one hunk: line 75 (`Answer ONLY the question…`) → shape-branched contract. Sits under `## Rules` (68) before `## Answers` (85). One stage, one idea (shape-aware output contract). |
| G2 leak-guard intact | PASS | Forbidden-token grep over README: only hit is pre-existing protective line 71 (`Do NOT access validate.py or ground_truth.csv`), byte-identical to parent. Added lines (rivers/airports worked examples) name no oracle file, paste no `db_description_withhint`, fetch nothing (no curl/wget/clone). |
| G3 spec two fields | PASS | `diff anchor vs dab0012` = only `experiment:` + `solver_workflow:`. `agent.kind: spacedock_solver` + `runtime: codex` preserved; top-level `trials: 1` (the `trials: 2` is under `concurrency:`, unchanged from anchor). |
| G4 smoke tasks+exclude | PASS | Smoke diff = only reduced `tasks:` (dataset names: bookreview/music_brainz_20k/stockmarket/yelp) + added `exclude_tasks:` (per-query ids). `tasks` uses dataset names, not query ids. --explain surviving set = stockmarket-q3 (target), yelp-q6, bookreview-q1, music_brainz_20k-q1 — includes the named target; stable sentinels present. |
| G5 both frozen | PASS | Both `.frozen.yaml` and `.smoke.frozen.yaml` exist; both carry `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim cell-for-cell: scalar/ranking → terse `name: number`; list → complete enumeration. Generative/format-directive, not self-anchored verification ("re-run your own query"/"verify your answer matches" absent). |
| G7 actionability/inert-risk | PASS | Worked-example form: carries copyable skeletons (`Nile: 6650; Amazon: 6400; …`, `Hartsfield-Jackson; Star Alliance, Oneworld, SkyTeam`) — mechanical, not abstract-structural. Inert-risk note: the prior `Answer ONLY the question` line was already behaviorally inert here (gpt still injected descriptions); the worked examples are the bet that concrete suppression lands where the abstract rule didn't. |
| G8 regression-canary coverage | PASS | Generative (fires on every answer's shape, not precondition-gated). Surviving non-target `@baseline` passers: yelp-q6 (4/6 VARIABLE list canary — perturbable, the cell a terse-only rule breaks), bookreview-q1 (6/6 format), music_brainz_20k-q1 (6/6 cross-dataset sentinel from a perfect-score dataset). ≥1 non-target passer ✅. WARN: the genuinely perturbable list-branch canary is a single cell (yelp-q6); bookreview-q1/music_brainz_20k-q1 are stable format sentinels the lever may not fire on. Coverage condition met; surfaced for the captain. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol. |
| G10 self-correcting false-positive | N/A | Formatting contract, not a check/reconcile/validate-and-fix lever (no "verify a result and act on disagreement"). |

**For the captain:** No FAILs — clean to advance to `smoke`. Two things to watch: (1) the load-bearing list branch is exercised by only ONE perturbable canary (yelp-q6, the 4/6 variable cell); a hold there is the whole shape-awareness claim, so judge it per-cell against the 6-draw band, not a single draw. (2) G7 inert-risk: the replaced `Answer ONLY the question` line was already inert at gpt-5.5/xhigh, so the flip rides entirely on whether the concrete `name (what it does): number` worked-example actually suppresses the description injection — confirm via the committed stockmarket-q3 answer-string artifact.

## Stage Report: propose

- DONE: The forked solver README changes EXACTLY ONE idea — REPLACE the existing `Answer ONLY the question` line with the shape-branched contract (scalar/ranking → names+numbers only, no descriptions; list → full enumeration), leak-guard prose intact, foreign-domain worked examples (rivers/airports, NOT the target schema); and both spec diffs vs specs/dab-anchor-codex.yaml show ONLY experiment: + solver_workflow: (smoke additionally adds benchmark.tasks + benchmark.exclude_tasks).
  `diff spacedock-readme-baseline vs dab0012 README` = one hunk (line 75 → shape contract); full-spec diff = exactly experiment:+solver_workflow:; smoke diff adds only tasks (4 dataset names) + exclude_tasks (14 per-query ids).
- DONE: This lever is GENERATIVE, so the smoke set carries the G8 regression panel and is confirmed EXACTLY via `rk run --explain`: target stockmarket-q3 + the list canary yelp-q6 + a format canary bookreview-q1 + ≥1 passer from a perfect-score dataset OTHER than stockmarket/yelp/bookreview (music_brainz_20k-q1) — surviving set is exactly targets + canaries, no extra, none missing.
  `rk run …smoke.frozen.yaml --explain` reported `Tasks: 4`; exclude_tasks is the exact complement of {stockmarket-q3, yelp-q6, bookreview-q1, music_brainz_20k-q1} within those 4 datasets.
- DONE: The gatekeeper subagent ran against the variant artifacts and its per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT recommendation is written into the dab0012 hypothesis file.
  `## Gatekeeper review` block above: APPROVE, no FAILs (G1–G7 PASS, G8 PASS-with-WARN, G9/G10 N/A).

### Summary

Forked `spacedock-readme-baseline` → `dab0012-shape-aware-output-contract` and replaced the single
proven-inert `Answer ONLY the question` rule with a shape-branched output contract (scalar/ranking →
terse `name: number`; list → complete enumeration), keeping leak-guard prose byte-identical and using
foreign-domain rivers/airports worked examples to avoid leaking the target schema. Built the full +
smoke specs (smoke restricted to 4 datasets, exclude_tasks down to the target + 3 canaries), froze
both, and confirmed `Tasks: 4` via `--explain`. The 4th canary is music_brainz_20k-q1 (a perfect-score,
non-target dataset) rather than stockmarket-q1 to satisfy G8's cross-dataset regression requirement.
Gatekeeper recommends APPROVE with two advisory WARNs (single perturbable list canary yelp-q6; G7
inert-risk on the replaced line — flip rides on the worked-example suppressing the description injection).

## Smoke result

**Verdict: NO-GO.** Run-dir `runs/dab0012-shape-aware-output-contract/9eee91ea2489003e` (15m wall).
Strict audit CLEAN (4/4 trials clean, 0 tainted, 0 coverage-missing). Stratified Pass@1 = **0.25**
(1 of 4 cells pass).

| Cell | 6-draw band | Smoke | Verdict-delta | Validator message | Cause |
|---|---|---|---|---|---|
| stockmarket-q3 (target) | 0/6 | **0 / FAIL** | no flip | `No number found near name: Apex Global Brands Inc` | **lever INERT** — committed answer byte-identical to baseline failure mode |
| yelp-q6 (list canary) | 4/6 | **0 / FAIL** | dropped | `Missing name: Coffee House Too Cafe` | **INFRASTRUCTURE** — Mongo business source unreachable → abstained `UNABLE TO DETERMINE` |
| bookreview-q1 (sentinel) | 6/6 | **0 / FAIL** | dropped | `Ground truth '2020' not found in LLM output` | **INFRASTRUCTURE** — Postgres `Connection refused` (localhost:5432) → abstained `UNABLE TO DETERMINE` |
| music_brainz_20k-q1 (sentinel) | 6/6 | **1 / PASS** | held | — | held |

The headline 1/4 split is NOT three shape-rule regressions: only the **target** result is valid
experiment evidence. Both canary "drops" are backend-connectivity failures (Mongo for yelp-q6,
Postgres for bookreview-q1 — known DAB infra fragility, see memory `dab-mongo-segfault-no-restart`
and the Postgres-attach path), so they are NOT canary-bleed and carry no signal about the contract.
The cross-dataset sentinel that DID have a working backend (music_brainz_20k-q1) held cleanly.

## Behavioral analysis

**Target stockmarket-q3 — lever fully INERT (the decisive finding).** The committed answer string
(extracted from the codex transcript's "Exact final answer string" block,
`stockmarket-q3__RGp9845/.../rollout-…09-48-59….jsonl`) is **byte-for-byte the baseline failure
mode** — every ranking row still carries the full company description:

> `Apex Global Brands Inc. specializes in creating and marketing a diverse portfolio of fashion and
> lifestyle brands, connecting consumers with trendy and innovative products worldwide.: 23781.42…;
> BIO-key International, Inc. specializes in advanced biometric solutions…: 10988.14; …`

The solver computed the correct 15 companies and the correct 2008 average volumes (verified in its
own reasoning) — exactly as the hypothesis predicted — but the shape-branched `name: number` contract
**did not reach the committed answer**: the description injection is fully present. The validator's
`No number found near name: Apex Global Brands Inc` fires precisely because the description text sits
between the name and the number, defeating the name→number proximity match. This is the **G7
inert-risk materializing exactly as the gatekeeper flagged**: the replaced `Answer ONLY the question`
line was already inert at gpt-5.5, and the concrete `name (what it does): number` worked-example did
NOT change the behavior either. The flip rode entirely on suppression that never happened.

**Canary drops — infrastructure, not regression.** yelp-q6 committed `UNABLE TO DETERMINE` with the
explicit transcript reason *"The configured Mongo business source was absent/unreachable, so exact
business name and category field values could not be determined"* (it had already computed
`businessref_9`, avg 4.375 — the right entity, just couldn't name it). bookreview-q1 committed
`UNABLE TO DETERMINE` after `connection to server at "localhost" (::1), port 5432 failed: Connection
refused` against `bookreview_db`. Neither abstention is something the output-shape contract can cause
(the contract governs answer formatting, not the decision to abstain when a backend is down).

**Net:** the hypothesis is cleanly falsified on its own target — the description-injection fork is
real but the README-prose contract is **behaviorally inert** at gpt-5.5/xhigh, the same wall the
prior `Answer ONLY the question` line hit. A README formatting rule (even with a worked example) does
not suppress the injection.

## Failure Review

**Primary type: `incomplete-artifact`** (target). The lever's prose reached the solver's context but
NOT its committed answer — the artifact is unchanged from baseline. (Secondary: two canaries lost to
`infrastructure-failure` — Mongo + Postgres backends unreachable — which is NOT experiment evidence
and does not count as canary-bleed.)

1. **Original hypothesized fork.** gpt-5.5 fails stockmarket-q3 purely on output SHAPE — it decorates
   each ranking row with the company description; a shape-branched `name: number` contract (terse for
   scalar/ranking, full enumeration for lists) would suppress the injection and flip it, while the
   list branch protects yelp-q6.
2. **What the committed artifact actually revealed.** The diagnosis of the fork was CORRECT (the
   committed answer is the description-decorated ranking, computed values right) — but the *fix* was
   wrong: the README contract is **inert**. The solver did not strip the descriptions; the answer is
   identical to the baseline FAIL. A formatting instruction in `## Rules` does not change gpt-5.5's
   committed output here, with or without a worked example.
3. **Did the README rule fire?** No — no artifact evidence of firing. The committed string is
   byte-identical to the baseline description-injected answer. This is the same inert-prose wall the
   replaced `Answer ONLY the question` line hit (and the gatekeeper's G7 WARN predicted).
4. **New fork / mechanism to test next.** The injection must be removed by a MECHANICAL step the
   solver executes, not prose it can acknowledge and skip. Candidates: (a) a verify-stage post-process
   that re-writes `answers.json` by regex-stripping any text between an entity name and its `:` number
   in a ranking answer (a concrete transform, not a directive); (b) a worked SKELETON the solver copies
   that builds the answer string in SQL as `name || ': ' || CAST(value AS VARCHAR)` (string assembled
   from columns, leaving no slot for a description). Both move from "tell it to be terse" (inert) to
   "give it the exact construction" (mechanical). Note the broader pattern: README-prose output
   contracts are inert at gpt-5.5/xhigh — this is a transferable knowledge gain.
5. **Next step: `file`.** File the inert-prose finding as a knowledge gain and route a follow-up that
   makes the suppression MECHANICAL (option b — SQL string assembly skeleton — is the cleaner bet;
   it cannot leave a description slot). Also: the two infra failures mean the smoke under-covered —
   any re-smoke should confirm the Mongo (yelp) and Postgres (bookreview) backends are healthy before
   trusting canary verdicts, OR swap to canaries on backends that were up (music_brainz held).

## Feedback Cycles

### Cycle 1 — 2026-06-18 — smoke NO-GO (prose-inert) → revise to verify-stage mechanical strip
- **Result:** smoke run `9eee91ea2489003e`, audit clean. stockmarket-q3 did NOT flip — committed answer
  byte-identical to baseline ("…specializes in…: 23781.42"). The shape-aware README **prose** rule was
  behaviorally INERT at gpt-5.5/xhigh (the gatekeeper G7 risk materialized; same wall as the old
  `Answer ONLY the question` line). yelp-q6 / bookreview-q1 FAILs were INFRASTRUCTURE (Mongo / Postgres
  `Connection refused` → abstained), NOT canary-bleed; music_brainz_20k-q1 held PASS.
- **New fork (cycle 2):** suppression must be MECHANICAL, not a generation-time rule. Replace the prose
  shape-contract with a **verify-stage post-process the solver EXECUTES**: each ranking / `name: value`
  row forced to `<name>: <number>`, any parenthetical/descriptive clause stripped and re-serialized,
  with a final regex check before emitting answers.json. Tests: *gpt executes a concrete transform even
  when it ignores an abstract rule.*
- **Captain decision:** revise (not reject) — exhaust mechanism-distinct forks before concluding.
