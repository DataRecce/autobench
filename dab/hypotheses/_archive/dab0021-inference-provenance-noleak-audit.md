---
id: dab0021
title: agnews-q4 - inference-provenance no-leak rule (committed category must trace to a logged content-score table)
status: smoke
kind: hypothesis
source: dab0006 ideate (integrity-safe stripped-label inference); the explicit no-leak half of the concept; forks spacedock-readme-baseline @baseline
started: 2026-06-22T10:47:00Z
score: 0.3
verdict: REJECTED
---

## Hypothesis

The concept pairs the inference lever with a HARD integrity boundary because the codex-5.5
spacedock run group is known to contain cheating on other queries — any label-stripped inference
lever is only trustworthy if we can prove the committed category was *inferred from content*, not
lifted from an oracle/hint. This hypothesis isolates that integrity half as a single change: a
**provenance rule** requiring the committed answer to a label-stripped category query to TRACE to a
content-derived score table the solver itself logged, with a `verify`-stage audit that the trace
contains no oracle/hint read.

Falsifiable claim: **a rule requiring (a) every label-stripped category answer to be backed by a
logged per-class content-score table in `_artifacts/reasoning.md`, and (b) a `verify`-stage check
that the analyze trace shows the category was computed from `title`/`description` and contains no
read of `ground_truth.csv` / `db_description_withhint.txt` / any `*_withhint` / oracle file, keeps
the inference leak-free without degrading correctness.** This is an *independent audit* (it reads
the produced trace and the score table — artifacts that exist before the audit runs), NOT a
self-anchored "re-run your own query and trust it" check, so it sidesteps the dead self-verification
family. Falsified if the audit fires on a legitimately-inferred answer (false-positive: it cannot
distinguish content-derived from leaked) or is inert (the solver logs the table but the audit never
changes a verdict).

**The README change** (fork `spacedock-readme-baseline` -> `dab0021-inference-provenance-noleak-audit`),
ONE idea, split across the two stages it naturally spans BUT one idea (provenance): a clause in
`analyze` mandating the logged score table, and the matching audit sentence in the EXISTING
`verify` "External-oracle audit" paragraph (extending it, not adding a new stage):

> *(analyze, gated)* When a category/label answer is **inferred from text** (the category is not a
> column), you MUST log in `_artifacts/reasoning.md` the per-class content-score table the argmax
> came from — the score formula and the per-group counts. An inferred-category answer with no such
> table is not admissible.
>
> *(verify, appended to External-oracle audit)* Additionally, for any answer derived from an
> inferred category, confirm `_artifacts/reasoning.md` contains the content-score table backing it
> AND the analyze trace shows the category came from `title`/`description` scoring — NOT from any
> read of `ground_truth.csv`, `*_withhint`, `expected_*`, `answer_key`, or `gold`. If the backing
> table is absent or the trace shows an oracle/hint read, REJECT with the offending event index.

## Targets

- **PRIMARY (integrity-anchor) — agnews-q4** (and the agnews label-stripped class q2/q3): the
  answer must remain at least as correct as @baseline AND now carry a verifiable content-provenance
  trail. Acceptance = committed answer is backed by a logged content-score table; the verify audit
  PASSES on a genuinely-inferred answer (no false-reject) and would REJECT a planted oracle-read
  (tested by reading the existing baseline trace, which has no oracle read → must PASS).
- **Canaries to hold**: bookreview-q1, stockindex-q3, music_brainz_20k-q1 — the provenance clause
  is gated to inferred-category answers, so non-inferred queries are untouched and must not regress.

## Acceptance criteria (falsifiable)

- **GO** iff agnews-q4 (and agnews siblings) hold/flip with a logged content-score table present
  AND the verify audit PASSES the legitimately-inferred answer (no false-reject) AND no canary
  regresses — i.e. the integrity boundary is enforceable without correctness cost.
- **NO-GO / falsified** if the audit FALSE-REJECTS a content-inferred answer (cannot tell inference
  from leak → the boundary is not README-enforceable, an integrity-family wall) OR is fully inert
  (the table is logged but no verdict ever changes → it is decoration, not a guard) OR a canary
  regresses (gate mis-scoped → REVISE).
- **Relationship to dab0019/dab0020:** those raise inference *quality*; dab0021 makes the inference
  *auditable*. dab0021 is the lever you compose with whichever of dab0019/dab0020 wins, to keep the
  resulting answer provably leak-free — directly the concept's "raise inference quality AND keep it
  leak-free" pairing.

## Leak-guard (integrity, G2)

This hypothesis IS a leak-guard reinforcement: it STRENGTHENS the existing no-external-reference
prose and never weakens it; it adds NO read of any oracle/hint file (it *forbids* such reads and
*audits against* them). It reproduces no `db_description_withhint.txt` content. **Inference proof at
smoke:** the verify audit's PASS on the baseline-style inferred answer (with the logged score table
present, no oracle read in trace) is itself the proof the answer was inferred, not leaked; a planted
oracle-read in a probe trace must produce a REJECT.

## Smoke set

| Task | Baseline | Should-pass after lever | Role |
|---|---|---|---|
| agnews-q4 | ❌ FAIL | hold/flip WITH logged score table; verify PASSES (no false-reject) | 🎯 integrity anchor |
| agnews-q2 | ❌ FAIL | hold/observe with provenance table | secondary observe |
| bookreview-q1 | ✅ PASS | ✅ PASS (clause gated off) | gate-scope canary |
| stockindex-q3 | ✅ PASS | ✅ PASS (clause gated off) | gate-scope canary |

Net target: integrity boundary enforced at zero correctness cost (no canary regression); ETA ~1
dataset smoke. This is the "no-leak rule paired with the inference lever" the concept names.

## Gatekeeper review

**Recommendation: APPROVE** — single gated provenance idea, leak-guard strengthened (not weakened), specs/frozen clean; WARNs only (two-stage split, audit inert-risk, solver-authored provenance signal).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-24T00:00:00Z.

Parent-resolution note: `source:` says it forks `spacedock-readme-baseline @baseline`, but the apples-to-apples codex/gpt-5.5 anchor is `spacedock-readme-baseline-hostfix` (= `@codex-batch-baseline`); the fork README and both specs use it as parent. In the DAB registry `@baseline` resolves to the Opus-4-8 incumbent (known gotcha — NOT the codex anchor). Diffed against `solver_workflows/spacedock-readme-baseline-hostfix` and full-spec anchor `specs/codex-dab-batch-baseline.yaml`.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | WARN | Diff touches TWO sections — an analyze clause (mandate logged per-class score table) at 221a222 and a verify clause (provenance audit) at 241c247, appended to the EXISTING "External-oracle audit" paragraph (`specific external source.` → `…Additionally…`). Strictly two stage sections, but ONE coupled idea (provenance: log + audit), the verify edit extends existing audit prose (no new stage), no unrelated guardrail touched. Captain confirm the two-stage split is acceptable. |
| G2 leak-guard intact | PASS | grep hits are both FORBID/audit, not instruct-to-read: L75 pre-existing "Do NOT access `validate.py` or `ground_truth.csv`" (byte-identical to parent), L251 new audit clause forbidding any read of `ground_truth.csv`/`*_withhint`/`expected_*`/`answer_key`/`gold`. No curl/wget/git clone; no `db_description_withhint` content pasted. Leak-guard strengthened. |
| G3 spec two fields | PASS | diff vs `codex-dab-batch-baseline.yaml` shows only ABOUTME comments + `experiment:` (→dab0021…) + `solver_workflow:` (→./solver_workflows/dab0021…). `agent.kind: spacedock_solver` + `runtime: codex` preserved (frozen confirms); trials:1. |
| G4 smoke tasks+exclude | PASS | Smoke adds `tasks:` [agnews, bookreview, music_brainz_20k, stockindex] + `exclude_tasks:` [other 8 datasets]; nothing else differs. --explain surviving set = agnews (q4 target + q2 observe) + bookreview/music_brainz_20k/stockindex canaries; both target queries present. |
| G5 both frozen | PASS | Both `.frozen.yaml` and `.smoke.frozen.yaml` exist; both carry `kind: spacedock_solver` (L4) + `runtime: codex` (L5). |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim verbatim (analyze: log per-class content-score table; verify: confirm table present + trace shows title/description scoring + no oracle/hint read, REJECT with event index). Independent audit of pre-existing artifacts (trace + score table), explicitly NOT a self-anchored re-run; same stages/idea, no scope creep. |
| G7 actionability/inert-risk | WARN | Concrete artifact-production (log a named table to `_artifacts/reasoning.md`) + concrete check (confirm file contains table, scan trace for forbidden reads, REJECT w/ event index) — not abstract-structural. Inert-risk: README audit clauses are the known DAB "talks but doesn't do" family (dab0012); watch at smoke that the verdict actually changes, not just gets discussed. |
| G8 regression-canary coverage | N/A | Precondition-GATED (fires only when a category answer is inferred from text / not a column). Canary datasets have no inferred-category queries → gate does not fire (scope-canary test); not a fires-everywhere generative lever. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol. |
| G10 self-correcting false-positive | WARN | Verify-and-REJECT lever, but: (a) GATED to inferred-category answers (not generative — non-inferred passers untouched); (c) REJECTs/flags, does not mandate replacing a correct query. Mild (b) note: the provenance signal (logged score table) is solver-AUTHORED, so a solver that leaks AND fabricates a plausible table self-passes (correlated evidence) — the hypothesis itself names this as its false-negative falsification condition. Low passer-flip risk because gated off non-inferred queries; watch at smoke that the audit can actually distinguish inferred from leaked. |

**For the captain:** No FAILs → advance to smoke. Three things to weigh: (1) G1 — the lever edits two sections (analyze + verify) but as one coupled provenance idea, the verify half merely extends the existing external-oracle audit paragraph; confirm you accept the two-stage split rather than requiring a single-stage variant. (2) G7/G10 — both flag the same risk in different language: an audit clause may be inert ("talks but doesn't do") and its evidence is solver-authored, so verify at smoke that the verify verdict actually changes AND that it could distinguish a content-inferred answer from a planted oracle-read (the hypothesis's own GO/NO-GO test). (3) Parent resolves to `@codex-batch-baseline` (hostfix), not the Opus `@baseline` the `source:` line cites.

## Stage Report: propose

- DONE: Read dab0021 fully; verified AC-0 (entity well-formed, single provenance idea, target agnews-q4 named).
  ## Hypothesis names one lever (provenance: analyze-log + verify-audit); PRIMARY target agnews-q4.
- DONE: BATCH lineage fork.
  `cp -r solver_workflows/spacedock-readme-baseline-hostfix solver_workflows/dab0021-inference-provenance-noleak-audit`; README diff = two added blocks only (analyze provenance clause + verify audit extension); leak-guard byte-intact; no oracle/hint content pasted.
- DONE: Full spec.
  `specs/dab0021-inference-provenance-noleak-audit.yaml`; diff vs codex-dab-batch-baseline.yaml = ABOUTME + `experiment:` + `solver_workflow:` only; query_mode:batch, workspace_variant:spacedock, reasoning_effort:high preserved.
- DONE: Smoke spec.
  `…smoke.yaml` adds `tasks:` [agnews, bookreview, music_brainz_20k, stockindex] + `exclude_tasks:` [other 8]. Lever is PRECONDITION-GATED (inferred-category only) → lighter scope-canary set; canaries carry no inferred-category query so gate cannot fire on them.
- DONE: Export registry + plugin dir; freeze both.
  Wrote `…frozen.yaml` and `…smoke.frozen.yaml`; both carry kind:spacedock_solver + runtime:codex.
- DONE: Verify smoke selection via --explain.
  `rk run …smoke.frozen.yaml --explain` → Tasks: 4; materialized dirs = agnews, bookreview, music_brainz_20k, stockindex (target agnews-q4 + agnews-q2 observe + 3 canaries; none extra/missing).
- DONE: Run gatekeeper subagent; write ## Gatekeeper review block.
  Appended above: APPROVE, no FAILs; WARNs on G1 (two-stage split, one idea), G7 (audit inert-risk), G10 (solver-authored provenance evidence); G8/G9 N/A.
- DONE: STOP at propose gate.
  No rk run beyond --explain; reporting to FO.

### Summary
Forked the batch-baseline solver (spacedock-readme-baseline-hostfix = @codex-batch-baseline) into dab0021 and added the single gated provenance lever as two coupled blocks: an analyze clause mandating a logged per-class content-score table for any text-inferred category answer, and an extension of the EXISTING verify "External-oracle audit" paragraph that confirms the table is present and the analyze trace shows title/description scoring with no oracle/hint read (REJECT with event index otherwise). Full-spec diff is exactly the 2 allowed fields + ABOUTME; smoke surviving set is agnews (q4 target FAIL + q2 observe FAIL) + bookreview/music_brainz_20k/stockindex canaries (all PASS at @codex-batch-baseline). Gatekeeper recommends APPROVE (no FAILs; three WARNs, none blocking). Auto-gate condition met: gatekeeper APPROVE + clean reject-checks (one-knob README, leak-guard byte-intact, spec diff = only experiment+solver_workflow, kind/runtime preserved).

## Behavioral analysis

**Smoke run of record:** `runs/dab0021-inference-provenance-noleak-audit/bad5276942f5f7a9` (rc=0).
Clean audit: 3/3 trials, 0 errored, no `coverage_missing`/taint; smoke stratified 0.639.

**PRIMARY TARGET agnews-q4 — NO FLIP.** reward 0.0: the solver committed **"South America"** vs
GROUND TRUTH **"Africa"** — the same wrong region as the dab0019 deterministic classifier. This is
expected: the provenance no-leak audit is an INTEGRITY guard, not a classifier. It audits *where*
the answer came from; it does not change *which* region wins the argmax. So the lever could not move
agnews-q4 off the irreducible-margin wall that dab0019/dab0020 already mapped (the World-category
regions do not separate at the ~3% content-signal margin).

**DECISIVE CANARY REGRESSION — stockindex-q3 dropped.** reward 0.0: *"Neither candidate ranking
matched: Missing name: NSEI."* stockindex-q3 is a **6/6 STABLE SENTINEL** in
`_artifacts/baseline-variance-6draw.md` (stockindex-q1/q2/q3 all 6/6) and PASSED in BOTH the dab0019
and dab0020 smokes earlier the same day. It dropped ONLY under dab0021 — a REAL, lever-attributable
canary regression, not variance. Mechanism: the verify-stage external-oracle/provenance-audit prose
extension OVER-FIRED on a non-target ranking query, making the solver over-conservative — it
abstained/truncated the ranking and dropped NSEI. The clause was *supposed* to be gated to
inferred-category answers; on a ranking query it should have stayed dormant. It did not.

**Other cells held / clean:** music_brainz_20k-q1/q2/q3 = 1.0 (held); stockindex-q1/q2 = 1.0 (held);
agnews-q1 = 1.0; agnews-q2/q3 = 0.0 (RED, as at baseline). bookreview was DROPPED from this smoke
for concurrent-launch infra-safety (its shared postgres named volume would have collided with the
dab0020 smoke running concurrently) — documented in the smoke spec ABOUTME; music_brainz_20k +
stockindex carried the canary panel.

## Verdict

**verdict: REJECTED** — falsified at smoke (no full run; smoke→conclude rule for a cleanly-falsified
hypothesis). Two NO-GO conditions hit at once:

1. **No flip** — agnews-q4 committed South America vs GT Africa (provenance audit cannot create
   separating signal; it is an integrity guard, not a classifier).
2. **Canary regression** — stockindex-q3, a 6/6 stable sentinel, dropped via lever-attributable
   over-fire of the verify/audit prose on a non-target ranking query (the precondition gate did NOT
   hold the clause to inferred-category answers).

**dab0021 is the WORST of the three agnews-q4 mechanisms:** dab0019 (no flip, no regression),
dab0020 (no flip, but informative — the committed UNABLE proved the margin irreducible), dab0021
(no flip AND regressed a stable sentinel). Do NOT promote; @baseline / @codex-batch-baseline and the
seed README are UNCHANGED.

**TRANSFERABLE RULE:** a verify-stage integrity/audit clause has off-target regression cost even when
nominally precondition-gated — an audit that demands content-provenance can make the solver
over-conservative on unrelated ranking/completeness queries (drop a required entity, truncate a
ranking). README verify/audit prose is NOT reliably scopeable: it bleeds onto non-target queries.
Reconfirms the dab0012/dab0023 boundary that README prose (esp. verify/audit clauses) is not
gate-tight and carries off-target cost. Do not add audit prose without a hard scope test that proves
the gate stays dormant on the canary panel.

## Follow-up Routing

**stop.** This is the 3rd of 3 distinct agnews-q4 README-inference mechanisms; NONE reached Africa:
dab0019 (deterministic keyword classifier → South America), dab0020 (dual-signal require-agreement
gate → UNABLE, proving the margin irreducible), dab0021 (provenance no-leak audit → South America +
sentinel regression). Three mechanism-distinct attempts, all blocked by the same irreducible ~3%
content-signal margin (proven, not guessed, by dab0020's safe-abstain). The agnews-q4 README-inference
lever family is EXHAUSTED on tested evidence. No new hypothesis filed. NOT workflow-structural →
no WORKFLOW-REFINE entry.

## Stage Report: conclude

- DONE: Read /tmp/dab0021-conclude-evidence.txt and dab0021-inference-provenance-noleak-audit.md.
  Captain verdict REJECTED + full smoke evidence (run bad5276942f5f7a9) consumed; no numbers invented.
- DONE: Write ## Behavioral analysis: no flip (South America vs GT Africa) + DECISIVE canary regression (stockindex-q3, 6/6 sentinel, lever-attributable verify/audit over-fire), other canaries held, clean audit.
  Section appended above with the evidence-file numbers verbatim.
- DONE: Write ## Verdict = REJECTED (falsified + canary-regression at smoke, no full run); worst of three; transferable rule (verify/audit prose not gate-tight, off-target cost). No promote / no @baseline touch.
  ## Verdict section appended; @baseline / @codex-batch-baseline / seed README untouched.
- DONE: Set frontmatter verdict: REJECTED. Append ONE line to _artifacts/self-learning.md for dab0021.
  Frontmatter `verdict: REJECTED` set; one-line dab0021 entry appended to self-learning.md.
- DONE: Write ## Follow-up Routing = stop with family context (3 mechanisms, none reached Africa, family exhausted). No new hypothesis. No WORKFLOW-REFINE entry.
  ## Follow-up Routing = stop; family exhausted on tested evidence.
- DONE: Archive (git mv to _archive/) and commit with conclude: prefix.
  See commit; entity moved to _archive/dab0021-inference-provenance-noleak-audit.md.

### Summary
dab0021 REJECTED at smoke (falsified + canary regression, no full run). The provenance no-leak audit did not flip agnews-q4 (South America vs GT Africa — an integrity guard cannot create separating signal) AND it regressed stockindex-q3, a 6/6 stable sentinel, via lever-attributable over-fire of the verify/audit prose on a non-target ranking query — the worst of the three agnews-q4 mechanisms. Transferable rule: verify/audit README prose is not gate-tight and carries off-target regression cost. Family verdict: 3 distinct mechanisms (dab0019/0020/0021), none reached Africa, agnews-q4 README-inference family EXHAUSTED; routing = stop, no follow-up.
