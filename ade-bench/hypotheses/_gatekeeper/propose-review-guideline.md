---
title: Propose-stage gatekeeper review guideline
applies-to-stage: propose
maintained-by: the captain, on demand, by asking an agent to update it (NOT auto-updated by the workflow; the gatekeeper reads this file fresh on every run)
last-updated: 2026-06-07
---

# Propose-stage gatekeeper review guideline

This file is the **rule set** a gatekeeper subagent applies during the `propose` stage. It
encodes the checks a human performs at the leak-guard gate, so the gatekeeper can produce an
**advisory recommendation** for the captain. The gatekeeper does **not** pass or block the
gate — the captain always makes the final decision. To tune the bar, the captain asks an
agent to update this file on demand; it is not changed automatically during a run, and the
captain need not hand-edit it. The gatekeeper has no memory of past versions and re-reads it
fresh each run, so any agent-applied update takes effect on the next review.

## What the gatekeeper reviews

The "resolver" of a hypothesis = the forked solver workflow (`solver_workflows/h<NNNN>-<slug>/`),
its `README.md` change, and the paired specs.

**First, resolve the fork parent** (G1/G6 depend on diffing against the right one): read the
hypothesis's `source:` field, which states the solver it forked from, and cross-check the
reigning champion via `uv run --project ../razorback rk registry resolve run @baseline` plus
that `@baseline` run's `solver_workflow`. Use the resulting directory as `<parent-solver>`
(the seed is `solver_workflows/codex-ade-dbt-minimal`, but a promoted hypothesis may have
moved `@baseline`). If `source:` and the registry disagree, or neither resolves, do NOT guess
— mark the parent-dependent rules (G1, G6) FAIL "could not resolve fork parent" and flag it
for the captain.

The gatekeeper then inspects, for the hypothesis under review:

1. The hypothesis body — its `## Hypothesis` "Falsifiable claim" (the single change it
   promised) and its named target datasets.
2. The forked solver README vs `<parent-solver>`:
   `diff <parent-solver>/README.md solver_workflows/h<NNNN>-<slug>/README.md`.
3. The FULL spec vs baseline: `diff specs/baseline.yaml specs/h<NNNN>-<slug>.yaml`.
4. The smoke spec vs the full spec: `diff specs/h<NNNN>-<slug>.yaml specs/h<NNNN>-<slug>.smoke.yaml`.
5. The frozen artifacts: `specs/h<NNNN>-<slug>.frozen.yaml` and `…smoke.frozen.yaml`.

The gatekeeper must NOT run `rk run`, modify any file other than appending its review block to
the hypothesis file, or fetch anything external.

## Rules

Each rule has a verdict: **PASS** (clean), **WARN** (passes but worth a human glance), or
**FAIL** (a human would reject as written).

**Unevaluable = FAIL.** If an artifact a rule needs is missing or unreadable (the forked
solver dir, a spec, a frozen file, or the resolved parent), that rule is **FAIL** with
evidence naming what was missing — never a silent PASS, and never "skip." A WARN never, on its
own, moves the recommendation off APPROVE.

### G1 — Single idea, single stage
The README diff vs the parent solver touches **exactly one** `## Stage:` section and adds
**exactly the one idea** the hypothesis's Falsifiable claim names. No other stage, and no
unrelated guardrail prose, is modified.
- **FAIL if:** the README diff is **empty** (no change was actually made to the resolver);
  more than one `## Stage:` section changed; more than one distinct idea added; the change
  edits dependency/package/leak-guard prose instead of (or in addition to) the intended stage.
- **Evidence to cite:** the diff hunks and which stage header they fall under.

### G2 — Leak-guard intact
The no-external-reference prose (no `curl`/`wget`/`git clone`/`git ls-remote`/package-source
download/web lookup/published-solution search) and the dependency/package guardrails are
unchanged and not weakened. The change introduces **no reference to hidden grading
artifacts**: `AUTO_*`, `solution__*`, `check_option_*`, `tests/AUTO_*`, "verifier",
"equality test", "expected output seed", or any instruction to run/inspect/drive-to-zero the
hidden checks.
- **FAIL if:** any leak-guard sentence is removed or softened; any hidden-test token appears
  in the added text; the change tells the solver to fetch, clone, or look up anything external.
- **Evidence to cite:** grep results for the forbidden tokens over the added lines; a note
  that the leak-guard paragraphs are byte-identical to the parent.

### G3 — Full spec differs in exactly two fields
`diff specs/baseline.yaml specs/h<NNNN>-<slug>.yaml` shows **only** `experiment:` and
`solver_workflow:` changed. `agent.kind: spacedock_solver` and `runtime: codex` are preserved.
- **FAIL if:** any third field differs; `agent.kind` or `runtime` changed; `trials` ≠ 1.
- **Evidence to cite:** the two-line diff.

### G4 — Smoke spec adds only benchmark.tasks
`diff specs/h<NNNN>-<slug>.yaml specs/h<NNNN>-<slug>.smoke.yaml` shows **only** an added
`benchmark.tasks:` block (the target dataset IDs, `ade-bench-` prefixed) — or, for a general
change with no targets, only `benchmark.n_tasks: 5`. Nothing else differs.
- **FAIL if:** the smoke spec changes any field other than `benchmark.tasks`/`n_tasks`; task
  slugs are bare (missing the `ade-bench-` prefix); the `benchmark.tasks` do **not** include
  every target dataset the hypothesis's `## Hypothesis` names (the smoke must exercise the
  change, not a different dataset set).
- **WARN if:** the target tasks do not include at least one stable-`@baseline`-pass
  regression sentinel.
- **Evidence to cite:** the smoke diff and the resolved task list.

### G5 — Both specs frozen, kind/runtime preserved
`specs/h<NNNN>-<slug>.frozen.yaml` and `…smoke.frozen.yaml` both exist; both still carry
`agent.kind: spacedock_solver` and `runtime: codex`.
- **FAIL if:** either frozen file is missing, or a frozen file dropped `kind`/`runtime`.
- **Evidence to cite:** `ls` of the frozen files + the kind/runtime lines.

### G6 — Resolver fidelity (matches the plan)
The wording actually inserted into the README matches the hypothesis's Falsifiable claim:
same stage, same idea, no scope creep, and it stays **generative or independent** (it tells
the solver how to build/derive, or to reconcile against an independent local signal) rather
than a self-anchored "check your own work / re-run your own model" instruction — the family
the baseline finding proved inert.
- **Dead-family phrasings to flag** (self-anchored verification — the inert h0006/h0007/h0008
  family): "re-run your own model", "compare to the previous/old output", "compare against the
  existing code", "drive … to zero rows", "verify your answer matches", "confirm the result
  equals", "check that the output is correct" with no independent source named. Their presence
  in the inserted text is a strong FAIL signal **unless** the check reconciles against a
  genuinely independent local signal (a different source table / grain / join path).
  Self-anchored **selection** — a multi-candidate protocol scored by the candidates' own
  checks — is the same disease at the protocol level (h0026); it is reviewed under **G9**.
- **FAIL if:** the inserted text diverges from the claim; it adds scope the hypothesis did
  not promise; it is a self-verification instruction that re-runs the solver's own derivation
  or compares to the pre-existing code (the dead h0006/h0007/h0008 family).
- **WARN if:** the wording is in the right stage and spirit but materially reworded from the
  claim (the captain may want to confirm the intent survived).
- **Evidence to cite:** the inserted sentence(s) quoted against the claim.

### G7 — Actionability / inert-risk (advisory, WARN-only)
The change must be expressible as something the solver implements **mechanically**, not
abstract prose it can acknowledge and skip. Empirically on this `@baseline` (h0008
check-afterward 0/7, h0009 copy-the-package 1/6, h0010 construct-rule 0/4), README prose that
asks the solver to **restructure SQL** — which table to build FROM, join direction, grain,
spine — is behaviorally **inert** at gpt-5.5/`xhigh`: the solver discusses it but the
committed SQL is unchanged ("talks but doesn't do"). The one durable win (asana002) was a
concrete mechanical substitution (`due_at::timestamp`), not a rewrite it had to reason into.
This rule is **predictive, not an integrity check** — it never FAILs, only WARNs, so it never
blocks the gate; it flags inert-risk in the captain note (it would have flagged h0010 here,
before its smoke run).
- **WARN if:** the inserted instruction asks for a structural rewrite (FROM/spine/
  join-direction/grain restructuring; phrasings like "build one-row-per-entity", "select FROM
  X instead of Y", "make the entity the spine") stated as **abstract prose**, *without* a
  worked-example SQL skeleton or a named mechanical edit. Note the inert-risk and suggest the
  worked-example / few-shot form (show the literal before→after SQL skeleton to pattern-match,
  e.g. `from <entity> left join (<child agg>) …`).
- **PASS if:** the change is a concrete mechanical substitution (a cast, column add/rename,
  literal/default value, or filter token) **or** it carries a worked-example skeleton the
  solver can copy rather than re-derive.
- **Evidence to cite:** quote the instruction and classify it —
  mechanical-substitution / worked-example / abstract-structural.

### G8 — Regression-canary coverage (generative instructions)
A **generative** instruction — one that fires on every task, not gated on a precondition that
limits it to the targets — can regress any currently-passing task it touches. A targets-only
smoke set is structurally blind to that: h0009 passed its 7-task targeted smoke (1 flip,
sentinel held) then lost **−3** at full scale on f1/quickbooks passers the smoke never ran
("convention bleed"). So a generative change must carry a regression panel in its smoke spec.
- **N/A (PASS) if:** the instruction is gated/scoped to a narrow precondition (e.g. "only when
  a package model for this entity exists") or is a mechanical substitution on a specific
  construct — classify and mark N/A.
- **FAIL if:** the instruction is generative AND the smoke `benchmark.tasks` lists no
  currently-passing `@baseline` canary from families other than the targets. Recommend adding
  ≥1 passing canary per other family (REVISE-class — fixable in place, idea unchanged).
- **WARN if:** the panel has ≥1 canary per family but they are all **inert stable passers** the
  lever cannot fire on, OR the family most structurally similar to the targets carries only one
  canary. One canary per family is *necessary but not sufficient*: a generative rule can break a
  **different member** of a family than the single canary you picked. **h0012** passed a 9-task
  smoke (its one f1 canary, f1001, held) then lost **−4** at full when it broke four *other* f1
  passers (f1003-hard / f1005 / f1005-medium / f1006-hard) the smoke never ran. Recommend ≥2
  **perturbable** canaries (passers the lever will actually *fire* on) from each family the
  lever's mechanism is most likely to perturb — not only stable passers it skips.
- **PASS if:** generative AND the smoke spec carries the canary panel (≥1 non-target
  `@baseline` passer from each other family: airbnb / ana-eng / asana / f1 / intercom /
  quickbooks) AND, for the family(ies) sharing the targets' construct, ≥2 **perturbable** canaries.
- **Evidence to cite:** classify the instruction (generative vs gated/mechanical); if
  generative, list the smoke `benchmark.tasks` canaries, confirm each is a `@baseline` passer
  from a non-target family, and flag whether the lever can plausibly *fire* on each (perturbable
  vs inert).

### G9 — Selector independence (multi-candidate / selector protocol families)
Applies only when the hypothesis declares a **multi-candidate / selector protocol** — it runs
N candidates and selects one; mark **N/A (PASS)** otherwise. Earned from **h0026** (REJECTED at
smoke): the protocol executed faithfully — N≥3 candidates, real local probes, saved decision
tables, mechanical selection — and was still structurally unable to win, because **both
independence axes were missing, and both were visible in the propose artifacts before any run**.
The failure mode is the **fake-independence selector**: photocopy candidates judged by their own
light. Check both axes:

- **(a) Generation independence — are the N candidates real, or one mind photocopied?**
  The harness runs **one solver session per task** (`trials: 1`, single `agent`), so a
  README-only protocol that says "run N ≥ 3 candidates" is necessarily *simulated inside one
  session*: every candidate shares the same exploration, context window, and first reading, so
  they converge on the same answer (h0026: three "independent" candidates, identical wrong
  `ABDE`). To satisfy this axis the design must provide **isolation** (genuinely separate
  runs/sessions/agents — a harness/spec-level mechanism, not README prose) or **forced
  divergence** (each candidate is assigned a distinct stance on the borderline decisions, e.g.
  "candidate 2 must argue option B is OUT and try to defeat the IN evidence").
- **(b) Judgment independence — who grades the candidates?** List every scoring criterion the
  selector uses and name its **anchor**. A criterion computed from the candidate's **own**
  artifacts (completeness of its own table, "support N/N" against its own probes, answer string
  matches its own table) is **self-anchored selection**: a plausible-but-wrong candidate
  self-scores perfect and wins (h0026's scorer graded the wrong answer 6/6). Running real SQL
  against real data does **not** make a check independent — independence is about who *authors
  and interprets* the check, not whether the data is real. To satisfy this axis at least one
  load-bearing criterion must be **external to all candidates**: e.g. falsifier checks authored
  before any candidate exists, candidates cross-examining each other's IN decisions, or a
  per-IN-decision adversarial probe that a wrong IN would fail.
- **FAIL if:** the claim's mechanism depends on candidate diversity but the substrate provides a
  single session and no forced-divergence design (axis a); **or** every selection criterion is
  anchored to the candidate's own checks/artifacts (axis b).
- **WARN if:** isolation/divergence or an external criterion is claimed but cannot be verified
  from the README + specs alone.
- **Evidence to cite:** quote the candidate-generation text and classify the substrate
  (in-session vs isolated vs forced-divergence); table each scoring criterion → its anchor
  (candidate-own vs external).

### G10 — Self-correcting lever false-positive risk (check / reconcile / validate-and-fix families)
Applies only when the lever instructs the solver to **verify a result and act on disagreement**
— a check, reconcile, validation, or "fix it if your number doesn't match" instruction; mark
**N/A (PASS)** otherwise. Earned from **h0012** (REJECTED at full, **−4**): a Validation rule
"reconcile a key figure against an INDEPENDENT raw-source derivation by a structurally different
path" was *correct in theory* (it flipped airbnb007, asana002) yet lost net −4 because, applied
generatively, it **damaged passers** — it pushed four f1 `constructor_points` passers off a
simple-correct `sum→max` onto an elaborate wrong path, then "validated" against a CTE built with
that *same* wrong logic (0 mismatches → false-green). A self-correcting lever is most dangerous on
the tasks it should leave alone. Check three axes:

- **(a) Scope — generative vs figure-change-gated.** A self-correcting lever that fires on
  *every* task also fires on already-correct ones; when the model is right but the solver's
  second derivation is wrong, the rule "fixes" the right answer to the wrong number. To be safe it
  must be gated to a precondition (fire only when a numeric figure is actually being authored /
  changed / is genuinely in question), not run on every task.
- **(b) Independence source — separately-sourced vs re-derived.** The reconcile target must be a
  **separately-sourced** signal — a plain `SELECT … FROM {{ source }}` with **no model logic** —
  not an artifact the solver re-derives itself (a CTE sharing the model's window / grain / join).
  A self-built "independent" check **re-correlates** with the model after a fix and gives a
  false-green (h0012). Double-entry works only when the second entry comes from a different
  *source*, not the same hand.
- **(c) Check-don't-replace.** The instruction must trigger *investigation* of a disagreement,
  not mandate replacing a simple-correct path with a "structurally different" (and possibly wrong)
  one. "Use a different path" optimizes for *different*, not *correct*.
- **FAIL if:** the lever is self-correcting AND (a) generative with no figure-change gate, **or**
  (b) reconciles against a re-derived artifact rather than a separately-sourced raw signal,
  **or** (c) mandates replacing/re-deriving instead of investigating.
- **WARN if:** it is gated but the gate is weak or unverifiable from the README, or the
  independence source is ambiguous.
- **Evidence to cite:** classify the lever (self-correcting vs not); quote its scope gate
  (generative vs figure-change); name what the reconcile compares against (raw source vs
  re-derived CTE); quote any "different path" / "rewrite" mandate.

## Recommendation rubric

After scoring all ten rules, the gatekeeper emits one overall recommendation. **WARNs never
drive the recommendation by themselves** — surface them in the "For the captain" note (G7 is
WARN-only by design and always lands there). Only FAILs move it off APPROVE:

- **APPROVE** — no FAILs (any number of WARNs allowed). Nothing blocks the gate; the captain
  can advance to `smoke`. Carry every WARN into the captain note.
- **REVISE** — at least one FAIL, and **all** FAILs are on the mechanical rules
  (G1/G4/G5/G8/G9/G10) the ensign can fix in place without changing the idea; no FAIL on
  G2/G3/G6. Recommend the specific fix, then re-review. (G9 caveat: a G9 FAIL is REVISE-class
  only when independence can be added without changing the single idea — e.g. adding
  forced-divergence stances or an external falsifier criterion; if the self-anchored selection
  criterion *is* the idea, the variant should go back to `hypothesis` instead. G10 caveat: same
  shape — gating a self-correcting lever to figure-changes, repointing its reconcile to a raw
  source, or softening "replace" to "investigate" is REVISE-class; but if an *ungated,
  fix-on-disagreement, re-derived* check **is** the idea, send it back to `hypothesis`.)
- **REJECT** — any FAIL on **G2 (leak-guard)**, **G3 (spec scope)**, or **G6 (fidelity)** —
  the integrity rules. The variant should go back to `hypothesis`.

The recommendation is advisory. The captain may override it in either direction and should
record the reason when doing so.

## Output format (what the gatekeeper appends to the hypothesis file)

The gatekeeper appends (or replaces) a `## Gatekeeper review` block in the hypothesis file:

```markdown
## Gatekeeper review

**Recommendation: APPROVE | REVISE | REJECT** — <one-line rationale>.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated <date>). Reviewed <ISO 8601>.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS/WARN/FAIL | <diff cite> |
| G2 leak-guard intact | PASS/WARN/FAIL | <grep cite> |
| G3 spec two fields | PASS/WARN/FAIL | <diff cite> |
| G4 smoke tasks-only | PASS/WARN/FAIL | <diff cite> |
| G5 both frozen | PASS/WARN/FAIL | <ls/head cite> |
| G6 resolver fidelity | PASS/WARN/FAIL | <claim vs inserted text> |
| G7 actionability/inert-risk | PASS/WARN | <instruction class + inert-risk note> |
| G8 regression-canary coverage | PASS/FAIL/N/A | <generative? + non-target passing canaries cited> |
| G9 selector independence | PASS/WARN/FAIL/N/A | <substrate class + per-criterion anchors> |
| G10 self-correcting false-positive | PASS/WARN/FAIL/N/A | <self-correcting? scope gate + reconcile source + replace-vs-check> |

**For the captain:** <what to look at / what to decide, 1–3 lines.>
```

## Future scope (not yet built)

The h0010 rejection also produced two lessons that belong to the **smoke go/no-go gate**, not
this propose gate, so they are deliberately NOT encoded here:

- **Inert-detector:** if a failing target's distance-to-pass (the dbt `Got N` mismatch count
  in `verifier/test-stdout.txt`) is UNCHANGED vs `@baseline`, the lever did nothing to that
  cell — a cheap inertness flag before reading transcripts.
- **Verify the artifact, not the chatter:** acknowledging an instruction ≠ executing it; check
  the final committed SQL, not the solver's reasoning, before crediting a flip.

If the gatekeeper is later extended to the smoke gate, capture these in a sibling
`_gatekeeper/smoke-review-guideline.md`. They are recorded for now in the h0010 archive entry
and operator memory (`ade-bench-instruction-lever-taxonomy`).
