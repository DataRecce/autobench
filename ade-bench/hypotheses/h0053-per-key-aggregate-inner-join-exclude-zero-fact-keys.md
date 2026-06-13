---
id: h0053
title: Per-key metric aggregate — when the task does NOT ask for completeness, build the aggregate FROM the fact via INNER JOIN; do not LEFT JOIN the full dimension and emit zero-fact keys with NULL metrics
status: smoke
kind: hypothesis
source: Captain request 2026-06-13 from _proposal/leverable-flipped-tasks-research-2026-06-13.md (CARD 1, airbnb005). Method artifact-confirmed both directions (h0043 PASS = inner-join/14,243 rows; h0052 FAIL = left-join keep-all/17,499 rows incl 3,256 NULL-NPS). Forks the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133).
started: 2026-06-13T00:00:00Z
completed:
verdict:
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
