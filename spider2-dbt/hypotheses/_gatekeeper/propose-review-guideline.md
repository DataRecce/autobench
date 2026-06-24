---
title: Propose-stage gatekeeper review guideline (spider2-dbt)
applies-to-stage: propose
gate-mode: AUTO-APPROVE — the gatekeeper recommendation drives the gate automatically (APPROVE ⇒ auto-advance to smoke); only a FAIL / REVISE / REJECT HALTs for the captain
maintained-by: the captain, on demand, by asking an agent to update it (NOT auto-updated by the workflow; the gatekeeper reads this file fresh on every run)
last-updated: 2026-06-24
---

# Propose-stage gatekeeper review guideline (spider2-dbt)

This file is the **rule set** a gatekeeper subagent applies during the `propose` stage. It encodes the
checks a human would perform at the leak-guard gate so the gatekeeper can produce a recommendation.

**This workflow runs the propose gate AUTO-APPROVE** (README → *Autonomous run policy → propose
auto-gate*). The gatekeeper is therefore not merely advisory decoration — its recommendation, together
with the FO's reject-checks, **drives the gate automatically**: an **APPROVE** with clean reject-checks
auto-advances to `smoke` without waiting for the captain; any **FAIL / REVISE / REJECT** (or a failed
FO reject-check) **HALTs and surfaces to the captain**. The gatekeeper has no memory of past versions
and re-reads this file fresh each run, so an agent-applied update takes effect on the next review.

## What the gatekeeper reviews

The "resolver" of a hypothesis = the forked solver workflow (`solver_workflows/spd<NNNN>-<slug>/`), its
`README.md` change, and the paired specs.

**First, resolve the fork parent** (G1 depends on diffing against the right one): read the hypothesis's
`source:` field, which states the solver it forked from, and cross-check the reigning champion via
`export RAZORBACK_REGISTRY=/home/kent/autobench/spider2-dbt/razorback-registry.yaml` then
`uv run --project ../razorback rk registry resolve run @baseline` plus that `@baseline` run's
`agent.solver_workflow`. Use the resulting directory as `<parent-solver>` (the seed is
`solver_workflows/spider2-dbt-baseline`, but a promoted hypothesis may have moved `@baseline`). If
`source:` and the registry disagree, or neither resolves, do NOT guess — mark the parent-dependent
rules (G1) FAIL "could not resolve fork parent" and flag it for the captain.

The gatekeeper then inspects:

1. The hypothesis body — its `## Hypothesis` falsifiable claim (the single change) and its named target
   tasks.
2. The forked solver README vs `<parent-solver>`:
   `diff <parent-solver>/README.md solver_workflows/spd<NNNN>-<slug>/README.md`.
3. The FULL spec vs the anchor: `diff specs/full-baseline.yaml specs/spd<NNNN>-<slug>.yaml`.
4. The smoke spec vs the full spec: `diff specs/spd<NNNN>-<slug>.yaml specs/spd<NNNN>-<slug>.smoke.yaml`.
5. The frozen artifacts: `specs/spd<NNNN>-<slug>.frozen.yaml` and `…smoke.frozen.yaml`.

The gatekeeper must NOT run `rk run`, modify any file other than appending its review block to the
hypothesis file, or fetch anything external.

## Rules

Each rule has a verdict: **PASS** (clean), **WARN** (passes but worth a human glance), or **FAIL** (a
human would reject as written). **Unevaluable = FAIL** — if an artifact a rule needs is missing or
unreadable, that rule is FAIL with evidence naming what was missing, never a silent PASS. A WARN never,
on its own, moves the recommendation off APPROVE.

### G1 — Single idea, single change
The README diff vs the parent solver adds **exactly the one idea** the hypothesis's falsifiable claim
names, in the relevant section — no unrelated guardrail or output-contract prose modified.
- **FAIL if:** the README diff is **empty** (no change actually made); more than one distinct idea
  added; the change edits leak-guard / no-fetch prose instead of (or in addition to) the intended idea.
- **Evidence:** the diff hunks and which section they fall under.

### G2 — Leak-guard intact (spider2-dbt: hidden gold)
spider2-dbt grades against a **hidden gold table** — the gold table name, its exact columns, and any
`*gold*` artifact are NOT given to the solver. The change must NOT leak any of that, and must NOT
weaken the no-external-fetch prose:
- it must NOT name the hidden gold table(s) or enumerate gold columns in the README (the README is the
  same for every task and must not smuggle task-specific answer hints);
- it must NOT instruct the solver to read, open, or inspect any `*gold*` / `expected_*` / `answer_key`
  file, or the verifier's comparison data;
- it must NOT tell the solver to fetch / `curl` / `wget` / `git clone` / `git ls-remote` / web-look-up
  upstream projects or published solutions.
- **FAIL if:** any no-fetch sentence is removed or softened; the added text names the gold table /
  columns or reads any gold/expected file; the added text tells the solver to fetch/clone/look up
  anything external.
- **Evidence:** grep over the added lines for forbidden tokens (`gold`, `expected_`, `answer_key`,
  `curl`, `wget`, `git clone`, `ground_truth`); a note that the no-fetch paragraphs are byte-identical
  to the parent.

### G3 — Full spec differs in exactly two fields
`diff specs/full-baseline.yaml specs/spd<NNNN>-<slug>.yaml` shows **only** `experiment:` and
`agent.solver_workflow:` changed. `agent.kind: spacedock_solver`, `runtime: codex`, `model: gpt-5.5`,
`reasoning_effort: xhigh`, and `trials: 1` are preserved.
- **FAIL if:** any third field differs; `agent.kind` / `runtime` / `model` changed; `trials` ≠ 1.
- **Evidence:** the two-line diff.

### G4 — Smoke spec narrows only `benchmark.tasks`
`diff specs/spd<NNNN>-<slug>.yaml specs/spd<NNNN>-<slug>.smoke.yaml` shows **only** the
`benchmark.tasks:` list narrowed to the smoke subset (targets + sentinels/canaries). spider2-dbt tasks
are one-query each, so smoke selection is a **subset of the `tasks:` list** — there is NO
`exclude_tasks` machinery here (that is a DAB construct).
- **FAIL if:** the smoke spec changes any field other than `benchmark.tasks`; it introduces an
  `exclude_tasks` block; the narrowed `tasks` list does **not** include every target task the
  hypothesis's `## Hypothesis` names.
- **WARN if:** the surviving set has no currently-PASSING sentinel.
- **Evidence:** the smoke diff and the `--explain`-confirmed surviving task list.

### G5 — Both specs frozen, kind/runtime preserved
`specs/spd<NNNN>-<slug>.frozen.yaml` and `…smoke.frozen.yaml` both exist; both still carry
`agent.kind: spacedock_solver` and `runtime: codex`.
- **FAIL if:** either frozen file is missing, or a frozen file dropped `kind`/`runtime`.
- **Evidence:** `ls` of the frozen files + the kind/runtime lines.

### G6 — Resolver fidelity (matches the plan)
The wording actually inserted into the README matches the hypothesis's falsifiable claim: same idea, no
scope creep, and it stays **generative or independent** (it tells the solver how to build/derive/
materialize a model, or how to validate against an independent local signal) rather than a
self-anchored "check your own work" instruction.
- **Dead-family phrasings to flag** (self-anchored validation): "verify your answer matches", "confirm
  the result equals", "check the output is correct" with no independent source named. spider2-dbt's
  recurring false-green is the agent reporting "0 mismatches" against its own interpretation — a check
  anchored only to the solver's own build is that disease.
- **FAIL if:** the inserted text diverges from the claim; it adds unpromised scope; it is a
  self-validation instruction anchored only to the solver's own build with no independent source.
- **WARN if:** the wording is in the right spirit but materially reworded from the claim.
- **Evidence:** the inserted sentence(s) quoted against the claim.

### G7 — Actionability / inert-risk (advisory, WARN-only)
The change must be something the solver implements **mechanically**, not abstract prose it can
acknowledge and skip. At gpt-5.5/`xhigh`, abstract structural prose ("get the grain right", "use the
correct columns") tends to be behaviorally **inert** — the solver discusses it but the committed model
is unchanged. A concrete mechanical instruction (a specific `{{ config(materialized='table') }}`
override, a named directory to avoid, a literal validation step like "assert each target table name
exists in the built DuckDB", a worked-example model skeleton) lands more reliably. Predictive, not an
integrity check — never FAILs, only WARNs.
- **WARN if:** the instruction asks for an abstract analytic rewrite without a worked-example skeleton
  or a named mechanical edit. Note the inert-risk and suggest the concrete form.
- **PASS if:** the change is a concrete mechanical instruction (a config override, a named dir,
  a literal existence check) or carries a worked-example skeleton.
- **Evidence:** quote the instruction and classify — mechanical / worked-example / abstract.

### G8 — Regression-canary coverage (generative instructions, flat-pass-rate terms)
A **generative** instruction — one that fires on every task, not gated to the targets — can regress any
currently-passing task it touches. The metric is a **flat pass rate**, so a regression on a passer
*directly* lowers the score (−1/61 ≈ −0.016) even while the target flips; a targets-only smoke is blind
to that. A generative change must carry a regression panel in its smoke spec.
- **N/A (PASS) if:** the instruction is gated/scoped to a narrow precondition (fires only on tasks
  matching a condition) — classify and mark N/A.
- **FAIL if:** generative AND the smoke set keeps no currently-PASSING `@baseline` task from a family
  OTHER than the targets'. Recommend keeping ≥1 passing canary from a non-target family (REVISE-class).
- **WARN if:** the panel has ≥1 canary but they are all **inert stable passers** the lever cannot fire
  on, OR fewer than 2 perturbable canaries cover the family the lever most likely perturbs. A
  *perturbable* canary is a passer the lever can actually FIRE on.
- **PASS if:** generative AND the smoke set keeps a non-target passing canary AND ≥2 perturbable
  canaries for the most-at-risk family.
- **Evidence:** classify the instruction (generative vs gated); if generative, list the surviving
  non-target `@baseline`-passer tasks (from `per_trial_outcomes.json`) and flag perturbable vs inert.

### G9 — Selector independence (multi-candidate / selector protocol families)
Applies only when the hypothesis declares a **multi-candidate / selector protocol** (run N candidate
models, select one); mark **N/A (PASS)** otherwise. The harness runs **one solver session per task**
(`trials: 1`), so a README-only "run N candidates" protocol is simulated inside one session — every
candidate shares the same context and converges. The failure mode is the **fake-independence
selector**: photocopy candidates judged by their own light.
- **FAIL if:** the mechanism depends on candidate diversity but the substrate provides a single session
  and no forced-divergence design; **or** every selection criterion is anchored to the candidate's own
  build (self-anchored selection — a wrong candidate self-scores perfect and wins).
- **WARN if:** isolation/divergence or an external criterion is claimed but unverifiable from
  README + specs alone.
- **Evidence:** quote the candidate-generation text and classify the substrate; table each scoring
  criterion → its anchor (candidate-own vs external).

### G10 — Self-correcting lever false-positive risk (check / validate-and-fix families)
Applies only when the lever instructs the solver to **validate a result and act on disagreement** — a
check, reconcile, or "fix it if it doesn't match" instruction; mark **N/A (PASS)** otherwise. The danger
is a task the solver already builds correctly: if the solver's second derivation is wrong, the rule
"fixes" the right table to a wrong one and the verifier flips a passer to FAIL.
- **(a) Scope** — a self-correcting lever that fires on every task also fires on already-correct ones;
  to be safe it should be gated to a precondition.
- **(b) Independence source** — a validation must check a **structural** invariant (the target table
  exists as a base table; the declared grain holds; required columns are present) or reconcile against
  a **separately-sourced** signal, NOT re-run the solver's own derivation (which re-correlates with the
  answer and gives a false-green). A pure existence/structure check (the spd0002 class) is SAFE — it
  cannot turn a right value wrong.
- **(c) Check-don't-replace** — the instruction must trigger *investigation* of a disagreement, not
  mandate replacing a correct model with a "structurally different" (possibly wrong) one.
- **FAIL if:** the lever is self-correcting AND (a) generative with no gate AND it can rewrite values,
  **or** (b) reconciles against a re-derived artifact rather than a structural invariant / raw source,
  **or** (c) mandates replacing/re-deriving instead of investigating. *(A structure/existence-only check
  is PASS — it is not value-rewriting.)*
- **WARN if:** gated but the gate is weak/unverifiable, or the independence source is ambiguous.
- **Evidence:** classify the lever; quote its scope gate; name what the validation checks (structural
  existence / raw source vs re-derived); quote any "replace / rewrite" mandate.

## Recommendation rubric

After scoring all ten rules, the gatekeeper emits one overall recommendation. **WARNs never drive the
recommendation by themselves** (G7 is WARN-only by design); only FAILs move it off APPROVE.

- **APPROVE** — no FAILs (any number of WARNs allowed). With clean FO reject-checks this **auto-advances
  to `smoke`** (auto-approve gate). Carry every WARN into the captain note for after-the-fact audit.
- **REVISE** — at least one FAIL, and **all** FAILs are on mechanical rules (G1/G4/G5/G8/G9/G10) the
  ensign can fix in place without changing the idea; no FAIL on G2/G3/G6. HALTs; recommend the specific
  fix, then re-review. (G9/G10 caveat: if the self-anchored selection or the ungated value-rewriting
  check *is* the idea, the variant goes back to `hypothesis`, not REVISE.)
- **REJECT** — any FAIL on **G2 (leak-guard)**, **G3 (spec scope)**, or **G6 (fidelity)** — the
  integrity rules. HALTs; the variant goes back to `hypothesis`.

Because the gate is auto-approve, an APPROVE means the workflow advances without a captain turn — so the
gatekeeper must be **conservative**: when a rule is genuinely unevaluable or borderline, prefer FAIL
(HALT) over a silent PASS. The captain audits APPROVEs after the fact via the recorded smoke-set table.

## Output format (what the gatekeeper appends to the hypothesis file)

```markdown
## Gatekeeper review

**Recommendation: APPROVE | REVISE | REJECT** — <one-line rationale>.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated <date>). Reviewed <ISO 8601>.
Gate mode: AUTO-APPROVE (APPROVE + clean reject-checks ⇒ auto-advance to smoke).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea | PASS/WARN/FAIL | <diff cite> |
| G2 leak-guard (hidden gold) | PASS/WARN/FAIL | <grep cite: gold/expected_/curl/git clone> |
| G3 spec two fields | PASS/WARN/FAIL | <diff cite> |
| G4 smoke narrows tasks only | PASS/WARN/FAIL | <diff + --explain surviving set> |
| G5 both frozen | PASS/WARN/FAIL | <ls/head cite> |
| G6 resolver fidelity | PASS/WARN/FAIL | <claim vs inserted text> |
| G7 actionability/inert-risk | PASS/WARN | <instruction class + inert-risk note> |
| G8 regression-canary coverage | PASS/FAIL/N/A | <generative? + non-target passer canaries cited> |
| G9 selector independence | PASS/WARN/FAIL/N/A | <substrate class + per-criterion anchors> |
| G10 self-correcting false-positive | PASS/WARN/FAIL/N/A | <self-correcting? scope gate + check target> |

**For the captain:** <what to look at / what was auto-approved, 1–3 lines.>
```
