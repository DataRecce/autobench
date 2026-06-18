---
id: dab0012
title: stockmarket-q3 - shape-aware output contract (scalar/ranking -> terse names+numbers; list -> full enumeration)
status: smoke
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

**Cycle-2 mechanism (the current fork).** Cycle 1 proved a `## Rules` PROSE shape-contract is
behaviorally INERT at gpt-5.5/xhigh — the solver committed the byte-identical description-decorated
answer (`## Feedback Cycles` → Cycle 1). So the suppression must be a CONCRETE step the solver
EXECUTES, not a generation-time preference it can acknowledge and skip. ONE idea:

1. **Revert `## Rules` to baseline.** Restore the original `Answer ONLY the question — no commentary
   or counter-examples` line so `## Rules` is byte-identical to `spacedock-readme-baseline` — the
   cycle-1 prose block is removed entirely.
2. **The sole change vs baseline lives in `### verify`** — a concrete post-process the solver RUNS
   before writing `answers.json` (phrased as an executable step, not a behavioral rule):

   > **Answer-shape normalization (run before emitting `answers.json`).** If the answer is a ranking
   > or a `name: value` list, normalize each row to `<entity name>: <numeric value>` ONLY: remove any
   > parenthetical, description, sector, or explanatory phrase attached to a name (e.g. turn
   > `Acme Corp (a software vendor): 12.3` into `Acme Corp: 12.3`). Then confirm the final answer
   > string contains NO `(` and no descriptive clause before a value — every row is the name, then
   > `: `, then the number. Re-serialize the answer if any row was changed.
   >
   > Worked example (foreign domain): turn `Nile (a river in Africa): 6650; Amazon (in South
   > America): 6400` into `Nile: 6650; Amazon: 6400`.

The bet: gpt ignores an abstract "don't decorate" rule but EXECUTES a concrete transform-and-check
framed as a verify-stage action. The foreign-domain rivers example avoids leaking the target schema
into the README (leak-catch rule, `ade-bench-sim-validates-tendency-not-real-run`); leak-guard prose
is untouched.

This cycle DROPS the list-branch / yelp-q6 dimension of the original hypothesis: the verify-stage
strip is a ranking-row de-decoration ONLY (it never removes list elements), and yelp's Mongo backend
was down last run, so yelp-q6 is no longer in the smoke set.

## Targets (cycle 2)

- **PRIMARY flip — stockmarket-q3** (gpt 0/6, Opus 5/6): must flip to PASS. Acceptance = the
  verify-stage strip removes the per-row description so the committed ranking string is
  `name: number; …` and matches gold; verified by committed artifact (no `(` / no descriptive clause
  before a value). Backend was UP last run — the target ran fine, just kept the decoration — so this
  is a clean test of whether the mechanical strip executes where the prose rule did not.
- **PERTURBABLE ranking canaries (same live backend) — stockmarket-q1, stockmarket-q2** (both 6/6
  ranking answers): MUST hold. These are passers the strip rule can actually FIRE on (they emit
  `name: number` rankings), so they prove the transform does not corrupt an already-correct ranking
  string. A drop here = the strip is destructive (over-stripping a name or a value).
- **Cross-dataset sentinel — music_brainz_20k-q1** (6/6, held PASS last run, backend up): MUST hold.
  The non-target regression tripwire (perfect-score dataset, different backend).

## Acceptance criteria (falsifiable)

- **GO** iff stockmarket-q3 flips to PASS by committed artifact (the emitted ranking string has the
  descriptions stripped — `name: number; …`, no `(`) AND both perturbable ranking canaries
  (stockmarket-q1, stockmarket-q2) hold at 6/6 AND the cross-dataset sentinel music_brainz_20k-q1
  holds — judged per-cell against the 6-draw band in `_artifacts/baseline-variance-6draw.md`, never
  on a single draw (standing captain rule: single-trial, judge by committed artifact + bleed-free
  canaries).
- **NO-GO / falsified** if stockmarket-q3 stays FAIL — either the verify-stage strip is ALSO inert
  (the solver acknowledges but does not run the transform, same wall as cycle 1's prose rule), OR it
  runs but the string still mismatches gold. **Destructive-strip NO-GO** if a perturbable ranking
  canary (stockmarket-q1/q2) drops — the transform corrupted an already-correct answer.

## Smoke set (cycle 2)

| Task | Baseline (6-draw) | Should-pass after lever | Role |
|---|---|---|---|
| stockmarket-q3 | 0/6 | PASS (flip) | 🎯 primary flip |
| stockmarket-q1 | 6/6 | hold 6/6 | ✅ perturbable ranking canary (same live backend) |
| stockmarket-q2 | 6/6 | hold 6/6 | ✅ 2nd perturbable ranking canary (G8, same live backend) |
| music_brainz_20k-q1 | 6/6 | hold | ✅ cross-dataset sentinel (perfect-score dataset, held last run) |

Cycle-2 smoke DROPS yelp-q6 and bookreview-q1 (cycle 1 lost both to backend `Connection refused` —
Mongo / Postgres — not to the lever). The new canaries are two 6/6 stockmarket RANKINGS on the SAME
live backend as the target: they are *perturbable* (the strip rule fires on them) and prove it does
not corrupt a correct ranking, satisfying G8's ≥2-perturbable-canary requirement on the construct the
lever most perturbs. music_brainz_20k-q1 (held PASS last run, backend up) is the cross-dataset
tripwire. Surviving smoke set confirmed exactly 4 via
`rk run specs/dab0012-shape-aware-output-contract.smoke.frozen.yaml --explain` (`Tasks: 4`).

## Gatekeeper review

**Recommendation: APPROVE (cycle 2)** — the mechanism moved from inert generation-time prose to a concrete verify-stage transform-and-check; `## Rules` is reverted byte-for-byte to baseline and the SOLE change is one hunk in `### verify`; integrity rules (G2/G3/G6) clean; the strip is a string-formatting normalization (deletes descriptive text, never recomputes a value), so the G10 false-positive risk is low; generative-canary coverage now has TWO perturbable same-backend ranking canaries (the cycle-1 single-canary WARN is resolved).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-18T10:35:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs parent is ONE hunk (238a239–259) entirely inside `### verify` (218) before `## Entity File` (260). `## Rules` block (68–84) is byte-identical to parent (`diff` of the Rules region → RULES_IDENTICAL): the cycle-1 prose contract was fully removed. One stage (`verify`), one idea (executable answer-shape normalization). |
| G2 leak-guard intact | PASS | Forbidden-token grep over the dab0012 README: the only hit is pre-existing protective line 71 (`Do NOT access validate.py or ground_truth.csv`), present byte-identical in the parent. Added lines name no oracle/`answer_key`/`gold` file, paste no `db_description_withhint`, fetch nothing (no curl/wget/clone/ls-remote); the worked example is a FOREIGN domain (rivers: `Nile: 6650; Amazon: 6400`), not the target schema. |
| G3 spec two fields | PASS | `diff dab-anchor-codex.yaml vs dab0012.yaml` = ONLY `experiment:` + `solver_workflow:`. `agent.kind: spacedock_solver` + `runtime: codex` preserved; top-level `trials: 1` (the `trials: 2` is under `concurrency:`, unchanged from anchor). No third field differs. |
| G4 smoke tasks+exclude | PASS | Smoke diff vs full = ONLY a reduced `benchmark.tasks:` (dataset NAMES: `music_brainz_20k`, `stockmarket`) + an added `benchmark.exclude_tasks:` (per-query ids `music_brainz_20k-q2/q3`, `stockmarket-q4/q5`). `tasks` uses dataset names, not query ids. Surviving per-query set (frozen smoke, `--explain` reported `Tasks: 4`) = stockmarket-q3 (target), stockmarket-q1, stockmarket-q2, music_brainz_20k-q1 — includes the named target; cross-dataset sentinel present. |
| G5 both frozen | PASS | Both `dab0012-…frozen.yaml` and `…smoke.frozen.yaml` exist (1810/1744 B, Jun 18 10:28); both carry `agent.kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the cycle-2 Falsifiable claim exactly: a verify-stage executable transform that keeps only `<name>: <number>` per ranking / `name: value` row, strips parenthetical/descriptive clauses, re-writes `answers.json` if changed, then regex-confirms no `(` before a value — scoped to ranking/`name:value` answers, scalars/plain lists left unchanged. No scope creep. Generative + executable, NOT self-anchored verification ("re-run your own query"/"verify your answer matches" absent). |
| G7 actionability/inert-risk | PASS | Concrete mechanical transform with a copyable foreign-domain skeleton (`Nile (a river in Africa): 6650 → Nile: 6650`) plus a definite regex post-check (no `(` before a value) — this is exactly the worked-example/named-mechanical-edit form the rule prefers, and the deliberate fix for cycle 1's inert abstract prose. Inert-risk note: cycle 1 proved a generation-time `## Rules` directive is inert at gpt-5.5/xhigh; the bet here is that a verify-stage transform-and-check the solver EXECUTES lands where the rule did not — plausible but the inert wall is the residual risk to watch in the artifact. |
| G8 regression-canary coverage | PASS | Generative (the strip fires on every ranking / `name:value` answer, not precondition-gated). Surviving non-target/non-flip `@baseline` passers: stockmarket-q1 (6/6 ranking) + stockmarket-q2 (6/6 ranking) — TWO PERTURBABLE canaries on the exact construct the lever most perturbs (same live backend, the strip genuinely fires on them), satisfying the ≥2-perturbable requirement; plus music_brainz_20k-q1 (6/6, different backend) as the cross-dataset tripwire. The cycle-1 single-canary WARN is resolved. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — single solver session, no N-candidate generation or selection. |
| G10 self-correcting false-positive | PASS | The lever does act on a check (strip + regex-confirm + re-serialize), so G10 is in scope, but it is a STRING-FORMATTING NORMALIZATION, not a recompute-and-replace: it deletes descriptive text BETWEEN an already-correct name and its already-correct number — the entity names and numeric values are untouched and never re-derived from data. There is no second derivation that could swap a correct value for a wrong one (axis b N/A — nothing is re-sourced), and "fix the offending row" means re-strip the SAME row, not replace the query with a different path (axis c clean). Residual risk is purely destructive over-stripping a name/number, which is precisely what the two perturbable ranking canaries (q1/q2) guard. Generative on shape (axis a) but the action cannot manufacture a wrong VALUE, so the passer-flip risk G10 protects against does not apply. PASS. |

**For the captain:** No FAILs — clean to advance to `smoke`. The cycle-2 design directly addresses both cycle-1 weaknesses: (1) mechanism moved from proven-inert generation prose to an executable verify-stage transform, and (2) canary coverage upgraded to two PERTURBABLE same-backend ranking passers (stockmarket-q1/q2) on the construct the strip fires on, plus a cross-dataset sentinel — and it drops the infra-fragile yelp/bookreview cells that confounded cycle 1. Two things to watch: (a) the central bet is whether a verify-stage transform escapes the same inert wall the prose hit — confirm via the committed stockmarket-q3 answer string (descriptions stripped, no `(`); (b) judge the q1/q2 holds per-cell against the 6-draw band, since the only real regression vector is destructive over-stripping of an already-correct ranking row.

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

## Stage Report: propose (cycle 2)

- DONE: ONE knob — reverted the cycle-1 shape-aware prose block in `## Rules` back to the baseline `Answer ONLY the question — no commentary or counter-examples` line, and put the SOLE change vs baseline in `### verify` as a concrete executable answer-shape normalization (strip parenthetical/descriptive clause from each `name: value` ranking row, re-write answers.json, regex-confirm no `(` before a value). Foreign-domain rivers worked example.
  `diff spacedock-readme-baseline vs dab0012 README` = ONE hunk (238a239–259) entirely inside `### verify`; `## Rules` is byte-identical to baseline.
- DONE: both spec diffs vs anchor show only the allowed fields (smoke adds tasks+exclude_tasks); both re-frozen with kind=spacedock_solver / runtime=codex.
  Full diff = experiment:+solver_workflow: only; smoke diff adds tasks (stockmarket, music_brainz_20k) + exclude_tasks (4 ids).
- DONE: smoke surviving set confirmed EXACTLY 4 via `--explain` (`Tasks: 4`) = stockmarket-q3 (target) + stockmarket-q1 + stockmarket-q2 (two perturbable ranking canaries, same live backend) + music_brainz_20k-q1 (cross-dataset sentinel). Dodges the Mongo/Postgres cells that died on infra in cycle 1.
  exclude_tasks is the exact complement of {q3,q1,q2 + mb-q1} within the 2 datasets.
- DONE: gatekeeper re-run (cycle 2); per-rule table + APPROVE recorded in `## Gatekeeper review` (replaced the cycle-1 block).
  APPROVE, no FAILs, no WARNs (cycle-1 single-canary WARN resolved; G10 PASS — string-format normalization, not a recompute).

### Summary

Cycle-2 REVISE: cycle 1 proved a `## Rules` prose output-contract is behaviorally inert at gpt-5.5/xhigh
(byte-identical decorated answer). Re-authored as a MECHANICAL change — `## Rules` reverted to baseline,
sole change is a verify-stage transform-and-check the solver EXECUTES (strip descriptions from ranking
rows + regex-confirm). Smoke set re-picked to dodge the Mongo/Postgres infra failures: target
stockmarket-q3 + two perturbable 6/6 stockmarket rankings (same live backend) + music_brainz_20k-q1
cross-dataset sentinel; `Tasks: 4` confirmed. Gatekeeper APPROVE, no FAILs/WARNs.
