---
id: h0053
title: Per-key metric aggregate — when the task does NOT ask for completeness, build the aggregate FROM the fact via INNER JOIN; do not LEFT JOIN the full dimension and emit zero-fact keys with NULL metrics
status: conclude
kind: hypothesis
source: Captain request 2026-06-13 from _proposal/leverable-flipped-tasks-research-2026-06-13.md (CARD 1, airbnb005). Method artifact-confirmed both directions (h0043 PASS = inner-join/14,243 rows; h0052 FAIL = left-join keep-all/17,499 rows incl 3,256 NULL-NPS). Forks the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133).
started: 2026-06-13T00:00:00Z
completed: 2026-06-14T01:01:38Z
verdict: passed
score:
worktree:
---

## Hypothesis

`airbnb005` builds the per-listing NPS/review aggregate `listing_agg_nps_reviews`. It flips
on a single join-shape choice that the local files do not disambiguate:

- **A (oracle-correct):** derive the aggregate FROM the reviews fact and INNER JOIN the
  listing's metadata, so only listings that actually have reviews appear. The h0043 passing
  run committed exactly this — 14,243 rows, `null_nps_rows = 0`.
- **B (the failure):** LEFT JOIN the full listing dimension and keep every listing, emitting
  ~3,256 zero-review listings with NULL NPS. The h0052 failing run committed this — 17,499
  rows → 2 mismatches on `listing_agg_nps_reviews_equality_with_tolerance`. The solver
  self-validates "0 mismatches" against its own derivation (self-anchored false-green), so it
  cannot catch the divergence itself.

This is the **dual** of the coverage-repair lever already in the README (h0050): that lever
ADDS missing keys *only when the task explicitly asks for completeness*. This lever does the
opposite — *when the task does NOT ask for per-key completeness*, it scopes the aggregate to
keys present in the fact and forbids the NULL-metric zero-fact rows. The two are gated on
opposite sides of the same completeness-intent signal, so they compose without conflict.

**Falsifiable claim (the single README change — Implementation stage only):** adding a
precondition-gated worked-example skeleton — "for a per-key metric aggregate where the task
does NOT request every-key completeness, build FROM the fact via INNER JOIN; do not LEFT JOIN
the full dimension and emit zero-fact keys with NULL metrics" — will make the committed
`listing_agg_nps_reviews.sql` use the inner-join shape, flipping `airbnb005` FAIL→PASS, without
regressing the canary panel (in particular `airbnb009`, where completeness IS requested and the
coverage lever must still keep all days).

**The single proposed README skeleton (generic identifiers, Implementation stage):**

```text
PER-KEY METRIC AGGREGATE (gated). When a task asks to BUILD or create a per-key metric
aggregate (e.g. an NPS / review / rating rollup keyed by listing/customer/entity) and the
instruction does NOT request row/key COMPLETENESS (no "a row for every <key>", "include all
<keys>", "rows are missing"), scope the output to keys that actually have fact rows: build the
aggregate FROM the fact and INNER JOIN the key's metadata. Do NOT LEFT JOIN the full key
dimension and emit keys with zero fact rows carrying NULL metrics.

(If the instruction DOES request completeness, this rule does not apply — follow the
coverage-repair rule above instead.)

BEFORE (keeps zero-fact keys as NULL-metric rows — AVOID when completeness is not asked):
    select dim.key, agg.metric
    from {{ ref('key_dimension') }} dim
    left join fact_agg agg using (key)        -- emits NULL-metric rows for zero-fact keys

AFTER (scope to keys present in the fact):
    select dim.key, agg.metric
    from fact_agg agg                          -- driven by the fact
    inner join {{ ref('key_dimension') }} dim using (key)   -- zero-fact keys excluded
```

## Acceptance criteria

**AC-1 — Exactly one README change; specs differ only in `experiment:` + `solver_workflow:`.**
README diff vs the h0052 solver README adds exactly one Implementation-stage gated block (the
per-key-aggregate inner-join rule), inserted after the coverage-repair block and before "Run
basic confirmation…"; Exploration/Validation/Finalization and the leak-guard + the other four
levers byte-identical. No `AUTO_*`/`solution__*`/`check_*`/`equality test`/`nps`/`listing_agg`/
expected-row-count token; no `curl`/`wget`/`git clone`. `agent.kind: spacedock_solver`,
`runtime: codex`, `trials: 1` preserved.

**AC-2 — Every score paired with a clean strict audit.** Each `rk score` cites
`rk audit --policy strict` on the same run-dir (`tainted: 0`, `coverage_missing: 0`,
`captured > 0`).

**AC-3 — The decisive read is the committed artifact.** Read the committed
`listing_agg_nps_reviews.sql` from the dispatched-ensign `apply_patch`. Classify: does the
metric aggregate drive from the fact with an INNER JOIN to the listing dimension (no NULL-NPS
zero-review rows)? A flip is credited only when the inner-join shape lands AND the verifier
passes. Transcript chatter does not count.

**AC-4 — No regression-canary loss, incl. the inverse-construct hold.** All `@baseline`
passers in the smoke panel stay PASS. CRITICAL: `airbnb009` (completeness IS requested) must
hold PASS on its byte-identical all-three-fork coverage edit — proving the new inner-join rule
did not conflict with the coverage lever's keep-all-days case. Any canary regression is a
NO-GO unless artifact-proven unrelated single-trial variance and the captain accepts the risk.

**AC-5 — Reproducibility judged against the base rate.** airbnb005 is ~89% at @baseline (a
near-stable passer that drops ~1-in-9). Smoke runs airbnb005 as ≥2 seed-perturbed repeats; GO
requires the inner-join artifact + verifier pass + clean audit on every repeat, with the honest
note that the marginal score value is low (high base rate) and the real win is closing the
join-shape construct.

## Target dataset

Primary target: `ade-bench-airbnb005`.

Smoke panel (target + canaries):
- `ade-bench-airbnb005` — 🎯 target.
- `ade-bench-airbnb009` — ✅ MUST-HOLD inverse-construct canary (completeness requested; the
  coverage lever must still keep all days — proves no conflict).
- `ade-bench-airbnb008` — ✅ same-family perturbable canary (the cell h0046 bled onto; proves
  the new aggregate rule does not re-introduce same-family collateral).
- `ade-bench-airbnb001` — ✅ same-family canary.
- `ade-bench-asana001`, `ade-bench-f1007`, `ade-bench-quickbooks002` — ✅ cross-family canaries.

GO requires the inner-join artifact read on airbnb005 (≥2 repeats) + every canary PASS on a
clean audit, with airbnb009 explicitly holding.

## Honest tension with the standing decisions

- **`trials: 1` / no best-of-N.** airbnb005 is ~89% already; a join-shape lever can only RAISE
  the per-draw probability of the inner-join shape, not make it deterministic, and the marginal
  aggregate score is small. Judge by committed artifact (AC-3), not the single reward.
- **Bleed risk (MODERATE).** A left-join keep-all is *correct* when completeness is requested —
  that case belongs to the coverage lever (h0050) and is gated out here by the completeness-intent
  test. The airbnb009 MUST-HOLD canary is the tripwire for any gate conflict.

Method/README change only. Forks @baseline h0052 (`solver_workflows/h0052-compose-maxpoints-featureguard-scoped-coverage`, runtime codex); no dataset, harness, or runtime change.

## Gatekeeper review

**Recommendation: APPROVE** — clean single-stage gated worked-example dual of the h0050 coverage lever; specs scope-correct, both frozen, leak-clean; only WARN-only predictive flags (G7 restructure-inert residual, G11 airbnb005 scored-model count unverifiable from static artifacts).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-13T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is a pure addition `138a139,158` — one block "PER-KEY METRIC AGGREGATE (gated)"; `awk` shows the enclosing header is `## Stage: Implementation`; both READMEs have 4 `## Stage:` headers (unchanged count); no other stage or guardrail prose touched. Inserted after coverage-repair, before "Run basic confirmation". |
| G2 leak-guard intact | PASS | Diff is addition-only, so all leak-guard/dependency paragraphs are byte-identical to the parent. Grep of added lines 139-158 for `AUTO_`/`solution__`/`check_option`/`verifier`/`equality test`/`expected output`/`listing_agg`/`nps_reviews`/`Got N`/`14243`/`17499`/`3256`/`curl`/`wget`/`git clone`/`drive…to zero`/`re-run your own` → no match. Only hit is the generic word "NPS" in "an NPS / review / rating rollup" (an illustrative construct word, not the hidden model name `listing_agg_nps_reviews` nor any count/AUTO token). |
| G3 spec two fields | PASS | `diff specs/baseline.yaml …h0053.yaml` shows exactly two changed lines: `experiment:` (line 2) and `solver_workflow:` (line 11). `agent.kind: spacedock_solver` + `runtime: codex` preserved (frozen grep), `trials: 1` preserved. No third field. |
| G4 smoke tasks-only | PASS | `diff …h0053.yaml …smoke.yaml` adds only a `benchmark.tasks:` block (`23a24,37`); nothing else differs. All 12 slugs carry the `ade-bench-` prefix. Includes the named target `ade-bench-airbnb005` and both named MUST-HOLDs `airbnb009`/`airbnb008`; the body Target panel named airbnb001/asana001/f1007/quickbooks002 but the smoke is a richer superset (adds airbnb004/006, asana002, ana-eng001, f1006/f1006-hard) — the change is still exercised. Regression sentinels present (no WARN). |
| G5 both frozen | PASS | `ls` confirms both `…frozen.yaml` (1753 B) and `…smoke.frozen.yaml` (2033 B) exist. Grep: both carry `kind: spacedock_solver` (line 4) + `runtime: codex` (line 5) + `trials: 1`. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim verbatim in intent: Implementation stage, gated on "BUILD a per-key metric aggregate AND completeness NOT requested", "build FROM the fact via INNER JOIN; do not LEFT JOIN the full dimension and emit zero-fact keys with NULL metrics", with a before→after SQL skeleton. It is generative-form *construct guidance* (how to build), NOT self-anchored verification — no "re-run your own model"/"compare to previous output"/"drive to zero" phrasing. It explicitly defers to the coverage rule when completeness IS requested. No scope creep. |
| G7 actionability/inert-risk | WARN | Instruction class = **worked-example skeleton** (carries literal `from fact_agg agg inner join {{ ref('key_dimension') }} dim using (key)` before→after) → per G7 the worked-example form is a **PASS-class** delivery. BUT the underlying ask is a join-direction restructure (LEFT JOIN dim → INNER JOIN from fact), which is the residual-inert-risk territory at gpt-5.5/xhigh even with a skeleton ("talks but doesn't do" risk). Surfaced predictively for the captain; never blocks. |
| G8 regression-canary coverage | N/A | Lever is **GATED** on a two-part precondition (build-a-per-key-aggregate AND completeness-not-requested) and explicitly defers to the coverage rule otherwise → not generative, so G8 is N/A. Note: the smoke panel STILL carries a full regression panel anyway — airbnb009 collision canary + same-family 001/004/006/008 + h0052 banked flips f1006/f1006-hard + cross-family asana002/ana-eng001/quickbooks002/f1007 (intercom omitted with rationale: no @baseline passer in that family). |
| G9 selector independence | N/A | No multi-candidate / selector protocol declared — single generative-form build rule. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever; it prescribes a build shape, it does not instruct the solver to verify a number and act on disagreement. (The body notes the *failure* mode is self-anchored false-green, but the lever itself does not add a reconcile.) |
| G11 multi-model-target risk | WARN | Target airbnb005 builds `listing_agg_nps_reviews`. Taxonomy `bug-type-taxonomy.md:43,217` enumerates the multi-model pair (`daily_agg_nps_reviews` + `listing_agg_nps_reviews`) ONLY for **airbnb007**; for airbnb005, both the taxonomy and research CARD 1 (`leverable-flipped-tasks-research-2026-06-13.md:52-71`) name a SINGLE scored model `listing_agg_nps_reviews_equality_with_tolerance` (Got 2). The lever's precondition (per-key listing aggregate, no rolling window) matches `listing_agg` but NOT a daily rolling-window model. I cannot run `rk` to read airbnb005's verifier test set, and the airbnb NPS family is the same family that ships the daily+listing dual — so whether airbnb005 is ALSO scored by a second `daily_agg`-style model is **unverifiable from the static artifacts**. Per G11 "WARN (unverifiable): surface as unknown rather than assume single-model." If airbnb005 turns out scored by ≥2 models, a single-run flip is variance on the unaddressed model — judge by the committed artifact on EVERY scored model from the run's `verifier/test-stdout.txt`, not the aggregate verdict. AC-5's ≥2 seed-perturbed repeats + AC-3 artifact read partly mitigate. |
| G12 decision-fork probe quality | N/A | Flipped-task follow-up (forked from h0052 FAIL on airbnb005), but the method is **oracle-confirmed by prior committed artifacts both directions** — h0043 PASS = inner-join/14,243 rows/0 NULL, h0052 FAIL = left-join/17,499 rows incl ~3,256 NULL (per `source:` + CARD 1) — rather than tested via a fresh subagent decision-fork probe. No `## Pre-smoke Decision-Fork Probe` block; the artifact-confirmation stands in for it. Treated as N/A (probe stood in for by prior-run artifacts), not FAIL. |

**For the captain:** No FAILs → nothing blocks the gate; advance to smoke. Two WARN-only flags to weigh: (G7) the inner-join restructure carries the right worked-example form but still sits in residual restructure-inert territory at gpt-5.5/xhigh — verify the committed `listing_agg_nps_reviews.sql` actually adopts the INNER-JOIN-from-fact shape (AC-3), don't credit chatter. (G11) airbnb005's scored-model count cannot be confirmed static; if smoke shows a flip, re-enumerate the target's scored models from `verifier/test-stdout.txt` and confirm the inner-join artifact landed on EVERY scored model before banking — a flip with an unaddressed scored model still red is variance, not a fix (the airbnb007/h0034 lesson). Honest note already in the body: airbnb005 is ~89% so the marginal score is low; the real win is closing the join-shape construct. airbnb009 MUST-HOLD is the gate-conflict tripwire.

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver h0052 → solver_workflows/h0053-per-key-aggregate-inner-join-exclude-zero-fact-keys; add ONLY the h0053 per-key-aggregate inner-join worked-example skeleton as a new Implementation-stage gated rule that explicitly defers to the coverage rule on completeness-intent tasks.
  `diff` vs h0052 README = pure addition `138a139,158` (one block, inserted after the coverage-repair block, before "Run basic confirmation"); all four existing levers + leak-guard byte-unchanged (AC-1). Commit a0bbcaa.
- DONE: Build FULL spec (cp baseline.yaml; only experiment + solver_workflow) AND smoke spec with the flip target + collision canary + banked flips + per-family canaries; resolve each task's @baseline reward.
  Full-spec diff vs baseline = exactly experiment:+solver_workflow: (G3 PASS). Smoke adds only benchmark.tasks (G4 PASS). @baseline h0052 dcb1a62 rewards: airbnb005=0.0 FAIL (flip target), airbnb009/008/001/004/006=1.0, f1006/f1006-hard=1.0, asana002/ana-eng001/quickbooks002/f1007=1.0 (all MUST-HOLD). Both frozen (1753 B / 2033 B).
- DONE: Run the gatekeeper, write ## Gatekeeper review. Did NOT launch any rk run.
  Gatekeeper recommendation = APPROVE (no FAILs); G7 + G11 WARN-only predictive flags surfaced; review block appended above this report.

### Summary
Forked @baseline h0052 into the h0053 solver and added exactly one Implementation-stage gated block — the per-key-aggregate INNER-JOIN-from-fact worked-example skeleton — which is the explicit DUAL of the h0050 coverage lever (fires only when completeness is NOT requested; defers to the coverage rule when it IS). Full spec differs from baseline only in experiment:+solver_workflow:; smoke adds only a benchmark.tasks panel (target airbnb005 @baseline 0.0 FAIL + the airbnb009 collision MUST-HOLD canary + h0052 banked flips f1006/f1006-hard + same-family 001/004/006/008 + cross-family asana002/ana-eng001/quickbooks002/f1007). Both specs frozen; gatekeeper APPROVEs with two WARN-only flags — G7 (verify the committed listing_agg_nps_reviews.sql actually adopts the inner-join shape, AC-3, not chatter) and G11 (airbnb005's scored-model count is unverifiable static; re-enumerate from verifier/test-stdout.txt if it flips). No rk run launched, per dispatch.

## Smoke result

**Verdict: GO.** Run-dir `runs/ade-bench-h0053-per-key-aggregate-inner-join-exclude-zero-fact-keys/bc3d76e716365ef1` (rc=0). Strict audit clean (`tainted: 0`, `coverage_missing: 0`, `clean: 12`); `captured=1` every cell. `rk score` = **12/12 PASS, pass_at_1 = 1.0** (above the 0.1875 constant).

| Task | Role | @baseline (h0052) | Smoke | Scored tests | Read |
|------|------|-------------------|-------|--------------|------|
| airbnb005 | 🎯 target | 0.0 FAIL | **1.0 PASS** | 4/4 (2 models: listing_agg + daily_agg equality+existence) | **FLIP — inner-join-from-fact artifact landed** |
| airbnb009 | ✅ collision MUST-HOLD | 1.0 | 1.0 PASS | 1/1 mom_agg_review_date_range | **coverage lever still fired — narrowing predicate dropped** |
| airbnb008 | ✅ same-family | 1.0 | 1.0 PASS | 4/4 | hold |
| airbnb001 | ✅ same-family | 1.0 | 1.0 PASS | 10/10 | hold |
| airbnb004 | ✅ same-family | 1.0 | 1.0 PASS | 2/2 | hold |
| airbnb006 | ✅ same-family | 1.0 | 1.0 PASS | 7/7 | hold |
| f1006 | ✅ h0052 banked flip | 1.0 | 1.0 PASS | 4/4 | hold |
| f1006-hard | ✅ h0052 banked flip | 1.0 | 1.0 PASS | 4/4 | hold |
| asana002 | ✅ cross-family | 1.0 | 1.0 PASS | 3/3 | hold |
| ana-eng001 | ✅ cross-family | 1.0 | 1.0 PASS | 1/1 | hold |
| f1007 | ✅ cross-family | 1.0 | 1.0 PASS | 6/6 | hold |
| quickbooks002 | ✅ cross-family | 1.0 | 1.0 PASS | 8/8 | hold |

Net: **+1 target flip (airbnb005), zero canary loss, collision canary holds.**

## Behavioral analysis

**DECISIVE READ (a) — airbnb005 (AC-3, the GO target).** The committed `models/agg/listing_agg_nps_reviews.sql` (apply_patch in the dispatched solver Ensign session `rollout-2026-06-13T14-57-55-...jsonl`) is the INNER-JOIN-from-fact shape, verbatim core:

```
FROM review_cte                          -- review_cte = {{ref('fct_reviews')}}
INNER JOIN listing_cte                   -- listing_cte = {{ref('dim_listings')}}
	ON review_cte.LISTING_ID = listing_cte.LISTING_ID
GROUP BY review_cte.LISTING_ID, listing_cte.LISTING_NAME, listing_cte.ROOM_TYPE
```

Driven FROM the reviews fact, INNER JOIN to listing metadata — only listings with reviews appear. There is NO `LEFT JOIN {{ref('dim_listings')}}` keep-all, NO zero-fact NULL-NPS rows. This is shape A (oracle-correct), the dual of h0052's failing left-join-keep-all (17,499 rows incl ~3,256 NULL-NPS). The verifier seed `solution__listing_agg_nps_reviews` loaded **14,243 rows** — matching the h0043 inner-join oracle exactly. The lever reached the committed artifact; this is not transcript chatter.

**G11 RESOLVED (scored-model count).** airbnb005 is scored by FOUR tests across TWO models — `listing_agg_nps_reviews_equality_with_tolerance`, `daily_agg_nps_reviews_equality_with_tolerance`, and both `AUTO_*_existence` — all PASS (PASS=4 ERROR=0 FAIL=0). The second model `daily_agg_nps_reviews.sql` was also committed (rolling-28d window via a self-join on `daily_counts`; its internal LEFT JOIN is the rolling-window self-join, not a keep-all-listings dimension join — correct in form, and its equality test PASSED). The flip is NOT variance on an unaddressed model: the inner-join artifact + correct daily model landed on EVERY scored model. The G11 WARN is closed.

**DECISIVE READ (b) — airbnb009 (THE COLLISION CHECK, AC-4).** The committed `models/agg/mom_agg_reviews.sql` apply_patch DROPS the narrowing date predicate — it removes `WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE::DATE FROM review_cte)` so `dates_cte` keeps every calendar day from `dim_dates` (incremental branch retained). This is exactly the h0050 coverage-repair / keep-all-days lever firing on a completeness-requested task. The h0053 inner-join rule did NOT mis-fire here and did NOT suppress completeness. Scored test `mom_agg_review_date_range` PASS. **Both gates coexist: h0053 fires on no-completeness airbnb005 (inner-join-from-fact), h0050 fires on completeness airbnb009 (keep-all-days). No collision.** This is the precondition-gated-dual composing additively, as hypothesized.

**Canaries + banked flips.** All ten non-target/non-collision cells PASS on full test sets (actual_fail=0 each): same-family airbnb001/004/006/008, h0052 banked flips f1006/f1006-hard, cross-family asana002/ana-eng001/f1007/quickbooks002. Zero regression; the new aggregate rule introduced no same-family collateral (the cell h0046 bled onto, airbnb008, holds 4/4).

**Honest notes.**
- **AC-5 (≥2 seed-perturbed airbnb005 repeats) NOT satisfied as specified.** The smoke panel ran airbnb005 once (12 cells = 12 distinct tasks, one trial each), not as ≥2 repeats. The GO rests on the committed-artifact proof (AC-3) — inner-join shape landed, 14,243-row oracle match, 4/4 scored tests PASS, clean audit — per the standing single-trial / judge-by-artifact captain decision, NOT on a multi-repeat reproducibility number. airbnb005 is ~89% at @baseline so the marginal score is low; the real, durable win is closing the join-shape construct with an artifact-confirmed correct shape.
- **Workflow-refinement log: N/A.** This lever is an in-stage rule tweak (a new gated Implementation-stage worked-example block), NOT a structural workflow change (no new/removed/reordered stage, no new protocol-family). Per the smoke stage's structural-change tell-tales it does not require a `_artifacts/WORKFLOW-REFINE.md` entry; the in-stage rule lands in the instruction-lever taxonomy via the gated-levers-compose note (h0049/h0050 family).

## GO/NO-GO

**GO.** airbnb005 flips FAIL→PASS via the committed INNER-JOIN-from-fact `listing_agg_nps_reviews.sql` (artifact-confirmed, 14,243-row oracle match, 4/4 scored tests on BOTH scored models — G11 closed); the airbnb009 collision canary holds PASS with the h0050 coverage lever STILL firing (narrowing predicate dropped, keep-all-days) — proving the new inner-join rule did not conflict with or suppress completeness; zero canary loss across all ten regression/banked cells (12/12 PASS, clean strict audit). The two gates compose additively on opposite sides of the completeness-intent signal exactly as hypothesized. Route smoke → full.

## Verdict

**PASSED — smoke-validated (GO) lever, MERGED into the h0056 six-lever composition which PROMOTED to
@baseline.**

This lever did not run its own full; per captain it was composed with h0054 + h0055 onto @baseline
h0052 in the single six-lever README of **h0056**, which PROMOTED (35/48 = 0.7292, the first six-lever
baseline; @baseline rebound to
`runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a`).

**Banked solo effect (now live verbatim in the @baseline README):** the per-key inner-join-from-fact
rule — build the per-key aggregate FROM the fact table and `INNER JOIN` the dimension (no
left-join-from-dim that emits zero-fact NULL rows). Solo smoke flipped **airbnb005** (committed
INNER-JOIN-from-`fct_reviews` `listing_agg_nps_reviews.sql`, 14,243-row oracle match, 4/4 scored). In
h0056 this lever fired with the SAME committed shape in BOTH full draws AND **generalized** to the
sibling NPS task **airbnb007** (per-listing aggregate from `fct_reviews` + `INNER JOIN dim_listings`,
11/11) — a +2 reproduced flip over h0052, the strongest banked gain of the composition.

**Collision-free, confirmed from the h0056 committed artifacts:** the h0050↔h0053 dual-pair (opposite
sides of the completeness-intent signal) held in both draws — airbnb009 routed to coverage-repair with
the inner-join silent, airbnb005 routed to inner-join with coverage silent. Cited evidence: the h0056
promotion + the 48/48 six-way decision-fork simulation (`_artifacts/h0056-decision-fork-simulation.md`,
this lever scored 6/6 desired on its airbnb005 target, 0 collisions).
