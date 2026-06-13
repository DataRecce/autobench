---
id: h0055
title: Build/rename a model — when the task does not enumerate a restricted column set, PRESERVE every upstream column; apply only the named renames/keys, do not narrow to a "relevant" subset
status: smoke
kind: hypothesis
source: Captain request 2026-06-13 from _proposal/leverable-flipped-tasks-research-2026-06-13.md (CARD 3, ana-eng003). Method artifact-confirmed 2026-06-13 (h0043 PASS = all 18 stg_customer columns; h0012 FAIL = only 5 columns → AUTO_dim_customer_equality "has less columns than solution"). Forks the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133).
started: 2026-06-13T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`ana-eng003` builds `dim_customer` from `stg_customer` ("rename id→customer_id, make it the
primary key"). It flips on how wide the select is:

- **A (oracle-correct):** carry ALL 18 upstream columns through and apply only the named
  rename/key. The h0043 passing run committed this.
- **B (the failure):** narrow the select to the 5 columns the model judged "relevant"
  (id/company/names/email), dropping the other 13 (job_title, phones, address, city, state,
  zip, country, web_page, notes, attachments) → compile-time `AUTO_dim_customer_equality` "has
  less columns than `solution__dim_customer`". The task never restricted columns; the solver
  over-narrowed. Classification: DROPPED-EXISTING (the columns exist upstream).

**Important contrast — this is the INVERSE of the feature-boundary removal lever (h0045).**
The feature-boundary rule DELETES the columns whose only purpose is a removed feature; this
rule PRESERVES all ordinary upstream columns on a build/rename. The two must be gated so they
do not collide: this rule fires only on BUILD/CREATE/RENAME tasks that do NOT remove/disable a
feature and do NOT enumerate a column subset; the feature-boundary rule fires only on
remove/disable/toggle tasks. The smoke panel carries quickbooks002/003 (feature-removal) as
MUST-HOLD canaries to prove no collision.

**Falsifiable claim (the single README change — Implementation stage only):** adding a
precondition-gated worked-example skeleton — "when building/renaming a model from an upstream
model and the task does not enumerate a restricted column set, preserve every upstream column;
apply only the named renames/keys" — will make the committed `dim_customer.sql` carry the full
column set, flipping `ana-eng003` FAIL→PASS, without regressing the canary panel (especially the
feature-removal canaries, where columns SHOULD be dropped).

**The single proposed README skeleton (generic identifiers, Implementation stage):**

```text
BUILD / RENAME — PRESERVE THE COLUMN SET (gated). When a task asks to BUILD, CREATE, or RENAME
a model from a single upstream model, and it does NOT (a) remove/disable a feature or (b)
enumerate a restricted set of columns to keep, then PRESERVE every column from the upstream
model. Apply only the renames, keys, or casts the task names; carry all other columns through
unchanged. Do not prune the select to the columns you judge "relevant" — a downstream contract
may expect the full set.

(If the task removes/disables a feature, follow the feature-boundary rule above instead — there
you DO drop the feature-only columns.)

BEFORE (narrows to a judged-relevant subset — AVOID on a plain build/rename):
    select id as customer_id, company, last_name, first_name, email
    from {{ ref('upstream') }}

AFTER (preserve all upstream columns; apply only the named rename/key):
    select id as customer_id, company, last_name, first_name, email,
           /* …every remaining upstream column, unchanged… */
    from {{ ref('upstream') }}
```

## Acceptance criteria

**AC-1 — Exactly one README change; specs differ only in `experiment:` + `solver_workflow:`.**
README diff vs the h0052 solver README adds exactly one Implementation-stage gated block (the
build/rename preserve-columns rule); the other four levers, leak-guard, and remaining stages
byte-identical. No `AUTO_*`/`solution__*`/`check_*`/`dim_customer`/`stg_customer`/column-name/
expected-count token; no web-fetch token. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved.

**AC-2 — Every score paired with a clean strict audit** (`tainted: 0`, `coverage_missing: 0`,
`captured > 0`).

**AC-3 — The decisive read is the committed artifact.** Read the committed `dim_customer.sql`
from the ensign `apply_patch`. Classify: does the select carry ALL upstream columns (apply only
the rename/key), or does it narrow to a subset? A flip is credited only when the full column
set lands AND the verifier passes.

**AC-4 — No regression-canary loss, incl. the inverse-construct hold.** All `@baseline` passers
in the smoke panel stay PASS. CRITICAL: the feature-removal canaries `quickbooks002` /
`quickbooks003` must hold PASS on their narrow feature-boundary edits — proving the
preserve-columns rule did not over-fire and prevent the legitimate column DROP. Any canary
regression is a NO-GO unless artifact-proven unrelated variance and the captain accepts the risk.

**AC-5 — Reproducibility judged against the base rate.** ana-eng003 is ~94% at @baseline (a
near-stable passer, low headroom). Smoke runs it as ≥2 seed-perturbed repeats; GO requires the
full-column-set artifact + verifier pass + clean audit on every repeat. The marginal aggregate
value is low; the real win is closing the over-narrowing construct and proving the gate is
collision-free with the feature-boundary lever.

## Target dataset

Primary target: `ade-bench-ana-eng003`.

Smoke panel (target + canaries):
- `ade-bench-ana-eng003` — 🎯 target.
- `ade-bench-quickbooks002` — ✅ MUST-HOLD inverse-construct canary (feature removal — columns
  SHOULD be dropped; proves the preserve-columns rule does not over-fire).
- `ade-bench-quickbooks003` — ✅ MUST-HOLD inverse-construct canary (same feature-removal family).
- `ade-bench-ana-eng001` — ✅ same-family canary.
- `ade-bench-airbnb001`, `ade-bench-asana001`, `ade-bench-f1007` — ✅ cross-family canaries.

GO requires the full-column-set artifact read on ana-eng003 (≥2 repeats) + every canary PASS on
a clean audit, with the quickbooks feature-removal canaries explicitly holding.

## Honest tension with the standing decisions

- **Bleed risk: MODERATE-HIGH.** "Preserve all columns" is the most generative of the three
  card-1/2/3 levers — it could over-fire on a task that legitimately projects a subset, or
  collide with the feature-boundary DROP rule. The gate (build/rename AND not-feature-removal
  AND no-enumerated-subset) plus the quickbooks002/003 MUST-HOLD canaries are the safeguards;
  any over-fire shows up there before full.
- **`trials: 1`.** ana-eng003 is ~94% already; low marginal score. Judge by artifact (AC-3) and
  by the collision-free canary result, not the single reward.

Method/README change only. Forks @baseline h0052 (`solver_workflows/h0052-compose-maxpoints-featureguard-scoped-coverage`, runtime codex); no dataset, harness, or runtime change.

## Propose artifacts

- Forked solver: `solver_workflows/h0055-build-rename-preserve-all-upstream-columns/`
  (parent = `solver_workflows/h0052-compose-maxpoints-featureguard-scoped-coverage`, the
  current `@baseline` = `runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133`).
- README diff vs h0052 = exactly ONE added block (lines 80-98): the gated BUILD/RENAME
  PRESERVE-THE-COLUMN-SET rule, placed immediately after the feature-boundary removal/toggle
  rules so the "follow the feature-boundary rule above instead" cross-reference resolves. The
  four other levers, leak-guard prose, and all other stages are byte-identical (AC-1 met).
- FULL spec `specs/h0055-build-rename-preserve-all-upstream-columns.yaml`: differs from
  `baseline.yaml` ONLY in `experiment:` + `solver_workflow:`. Frozen.
- Smoke spec `…smoke.yaml`: differs from FULL ONLY by the `benchmark.tasks` block (10 tasks).
  Frozen.
- No forbidden token in the README diff: no `AUTO_*`/`solution__*`/`check_*`/`dim_customer`/
  `stg_customer`/expected-count/web-fetch token. The skeleton uses the generic identifiers
  (`customer_id`/`company`/`email`/`upstream`) verbatim from the approved hypothesis-body
  skeleton.

### Baseline-reward table (@baseline = h0052 dcb1a62, per_trial_outcomes.json)

| Task | @baseline reward | Role |
|---|---|---|
| ade-bench-ana-eng003 | 1.0 PASS | TARGET — preserve-columns flip. NOTE: this baseline draw is PASS (AC-5 frames it as ~94% near-stable passer, low headroom). Judge by full-column-set ARTIFACT (AC-3), not by flipping a 0.0. |
| ade-bench-quickbooks002 | 1.0 PASS | MANDATORY inverse-construct canary (feature removal — columns SHOULD drop). Must hold. |
| ade-bench-quickbooks003 | 1.0 PASS | MANDATORY inverse-construct canary (feature-removal family). Must hold. |
| ade-bench-airbnb009 | 1.0 PASS | h0052 banked flip (coverage). Must hold. |
| ade-bench-f1006 | 1.0 PASS | h0052 banked flip (max-points). Must hold. |
| ade-bench-f1006-hard | 1.0 PASS | h0052 banked flip (max-points hard). Must hold. |
| ade-bench-ana-eng001 | 1.0 PASS | same-family canary. Must hold. |
| ade-bench-airbnb001 | 1.0 PASS | cross-family canary (airbnb). Must hold. |
| ade-bench-asana002 | 1.0 PASS | cross-family canary (asana). Must hold. |
| ade-bench-f1007 | 1.0 PASS | cross-family canary (f1). Must hold. |

KEY TENSION FOR THE CAPTAIN: ana-eng003 is PASS=1.0 in the @baseline single-trial draw (not a
hard FAIL). The hypothesis (AC-5) anticipates this — ana-eng003 is ~94% base-rate, the marginal
aggregate value is low, and the GO bar is the full-18-column ARTIFACT + clean audit on every
seed-perturbed repeat, plus the collision-free hold on quickbooks002/003. This lever banks a
CONSTRUCT closure + a gating proof, not a 0->1 pass-rate flip.

## Gatekeeper review

**Recommendation: APPROVE** — gated (non-generative) single-idea Implementation-stage rule, leak-guard/spec/fidelity all clean; only WARNs (no decision-fork probe block; ana-eng003 is a baseline PASS judged by artifact, so smoke is exploratory not a 0→1 flip).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-13.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff = one added block at L80-98, entirely inside `## Stage: Implementation`; no other stage touched; one idea (build/rename preserve-columns). |
| G2 leak-guard intact | PASS | No forbidden token in added lines (grep: NONE); leak-guard prose (`curl`/`wget`/`git clone`/`ls-remote`/published-solution) byte-unchanged from parent; no `AUTO_*`/`solution__*`/`check_*`/`dim_customer`/`stg_customer` token. |
| G3 spec two fields | PASS | `diff baseline.yaml h0055.yaml` = only `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | smoke diff = only an added `benchmark.tasks:` block (10 tasks); all `ade-bench-` prefixed; target ana-eng003 included; carries stable-passer sentinels (incl. quickbooks002/003 inverse-construct holds). |
| G5 both frozen | PASS | both `.frozen.yaml` and `.smoke.frozen.yaml` exist; each carries `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | inserted text matches the Falsifiable claim verbatim (gated build/rename preserve-columns worked-example skeleton, Implementation stage); generative-but-scoped, not self-anchored verification; correctly defers to the feature-boundary rule it is placed after. |
| G7 actionability/inert-risk | PASS | carries a literal BEFORE→AFTER SQL skeleton to copy (worked-example form), not abstract structural prose; not a build/deliverable-completion rule. |
| G8 regression-canary coverage | N/A (PASS) | lever is GATED to a narrow precondition (build/create/rename AND not-feature-removal AND no-enumerated-subset), not generative; smoke nonetheless carries non-target passers from airbnb/asana/f1/quickbooks families + the MANDATORY inverse-construct quickbooks002/003 holds. |
| G9 selector independence | N/A (PASS) | not a multi-candidate / selector protocol. |
| G10 self-correcting false-positive | N/A (PASS) | not a check/reconcile/validate-and-fix lever; it prescribes how to build the select, no "verify and act on disagreement" instruction. |
| G11 multi-model-target risk | N/A (PASS) | ana-eng003 is a single-model `dim_customer` target (`AUTO_dim_customer_equality`); not in the taxonomy's multi-model-trap list (only airbnb007 named MULTI-MODEL); lever's precondition reaches the one scored model. |
| G12 decision-fork probe quality | WARN | flipped-task-derived (source: leverable-flipped-tasks CARD 3) but no `## Pre-smoke Decision-Fork Probe` block and no explicit "probe skipped because" statement; AC-5 frames ana-eng003 as a ~94% baseline PASS judged by artifact, so the target is not a 0→1 flip chase — treat smoke as exploratory, judge by the full-column-set artifact + collision-free quickbooks holds, not the single reward. |

**For the captain:** No FAILs — APPROVE to smoke. Two things to keep in view: (1) ana-eng003 is already PASS=1.0 at @baseline, so the smoke GO bar is the full-18-column committed-artifact read (AC-3) on every seed-perturbed repeat, not an aggregate flip; (2) G12 WARN — no decision-fork probe was filed, so smoke is exploratory; the decisive evidence is the quickbooks002/003 inverse-construct HOLD (proving the gate is collision-free with the h0045 feature-boundary DROP), the real deliverable of this lever.

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver h0052 → h0055; add ONLY the build/rename preserve-columns worked-example skeleton as a new precondition-gated Implementation rule, gated as the inverse of h0045 and deferring to feature-boundary otherwise.
  `solver_workflows/h0055-build-rename-preserve-all-upstream-columns/README.md`; diff vs h0052 = exactly ONE added block (README lines 80-98), placed right after the feature-boundary rules so the "follow the feature-boundary rule above" cross-ref resolves; four other levers + leak-guard byte-identical (AC-1 met). No AUTO_/solution__/check_/dim_customer/stg_customer/count/web-fetch token.
- DONE: Build FULL spec (cp baseline.yaml; ONLY experiment + solver_workflow) AND smoke spec (target ana-eng003 + collision canaries quickbooks002/003 + h0052 banked flips airbnb009/f1006/f1006-hard + per-family canaries airbnb001/asana002/ana-eng001/f1007); resolve each @baseline reward; freeze both.
  FULL spec diff vs baseline = 2 lines (experiment + solver_workflow). Smoke diff vs FULL = benchmark.tasks block only. Both frozen (.frozen.yaml + .smoke.frozen.yaml written). Baseline (h0052 dcb1a62) rewards resolved: ALL 10 smoke tasks = 1.0 PASS — including the target ana-eng003 (see KEY TENSION).
- DONE: Run the gatekeeper, write ## Gatekeeper review. Did NOT launch any rk run.
  Gatekeeper recommendation = APPROVE (9 PASS, 1 WARN [G12 no decision-fork probe block — flipped-task-derived but framed as a near-stable passer judged by artifact], 0 FAIL). Section appended at entity line 160.

### Summary
Authored the h0055 propose variant: forked @baseline h0052 and added a single gated BUILD/RENAME PRESERVE-THE-COLUMN-SET Implementation rule (the inverse of the h0045 feature-boundary DROP rule), gated to fire only on build/create/rename tasks that neither remove a feature nor enumerate a column subset. Both specs built (FULL = 2-field diff, smoke = +benchmark.tasks only) and frozen; gatekeeper APPROVED. KEY TENSION for the captain: at the @baseline draw the flip target ana-eng003 is already PASS=1.0 (not FAIL) — consistent with AC-5's ~94% near-stable-passer framing; the GO bar is the full-18-column committed ARTIFACT + clean audit per repeat plus the collision-free hold on the quickbooks002/003 inverse canaries, NOT a 0→1 pass-rate flip. Did NOT launch rk run; FO drives smoke after the gate.
