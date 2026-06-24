---
title: Propose-stage gatekeeper review guideline
applies-to-stage: propose
maintained-by: the captain, on demand, by asking an agent to update it (NOT auto-updated by the workflow; the gatekeeper reads this file fresh on every run)
last-updated: 2026-06-15
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

The "resolver" of a hypothesis = the forked solver workflow (`solver_workflows/dab<NNNN>-<slug>/`),
its `README.md` change, and the paired specs.

**First, resolve the fork parent** (G1 depends on diffing against the right one): read the
hypothesis's `source:` field, which states the solver it forked from, and cross-check the
reigning champion via `export RAZORBACK_REGISTRY=/home/kent/autobench/dab/razorback-registry.yaml`
then `uv run --project ../razorback rk registry resolve run @baseline` plus that `@baseline`
run's `solver_workflow`. Use the resulting directory as `<parent-solver>` (the seed is
`solver_workflows/spacedock-readme-baseline`, but a promoted hypothesis may have moved
`@baseline`). If `source:` and the registry disagree, or neither resolves, do NOT guess —
mark the parent-dependent rules (G1) FAIL "could not resolve fork parent" and flag it for the
captain.

The gatekeeper then inspects, for the hypothesis under review:

1. The hypothesis body — its `## Hypothesis` "Falsifiable claim" (the single change it
   promised) and its named target datasets/queries.
2. The forked solver README vs `<parent-solver>`:
   `diff <parent-solver>/README.md solver_workflows/dab<NNNN>-<slug>/README.md`.
3. The FULL spec vs the anchor: `diff specs/dab-anchor-codex.yaml specs/dab<NNNN>-<slug>.yaml`.
4. The smoke spec vs the full spec: `diff specs/dab<NNNN>-<slug>.yaml specs/dab<NNNN>-<slug>.smoke.yaml`.
5. The frozen artifacts: `specs/dab<NNNN>-<slug>.frozen.yaml` and `…smoke.frozen.yaml`.

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
The README diff vs the parent solver touches **exactly one** stage section (the
model → analyze → verify methodology) and adds **exactly the one idea** the hypothesis's
Falsifiable claim names. No other stage, and no unrelated guardrail prose, is modified.
- **FAIL if:** the README diff is **empty** (no change was actually made to the resolver);
  more than one stage section changed; more than one distinct idea added; the change edits
  leak-guard prose instead of (or in addition to) the intended stage.
- **Evidence to cite:** the diff hunks and which stage they fall under.

### G2 — Leak-guard intact (DAB)
The no-external-reference prose (no `curl`/`wget`/`git clone`/`git ls-remote`/web lookup/
published-solution search) is unchanged and not weakened. The change introduces **no access to
hidden grading artifacts and no copy of withheld description text**:
- it must NOT instruct the solver to read, open, or inspect `ground_truth.csv` (the per-query
  oracle answers), nor any `expected_*` / `answer_key` / `gold` file;
- it must NOT paste or paraphrase the content of `data/<ds>/db_description_withhint.txt` (the
  withheld-hint schema description) into the README — the README is the same for every query
  and must not smuggle dataset-specific answer hints;
- it must NOT tell the solver to fetch, clone, or look up anything external.
- **FAIL if:** any leak-guard sentence is removed or softened; the added text names or reads
  `ground_truth.csv` / any oracle answer file; the added text reproduces `db_description_withhint.txt`
  content; the change tells the solver to fetch/clone/look up anything external.
- **Evidence to cite:** grep results for the forbidden tokens (`ground_truth`, `db_description_withhint`,
  `curl`, `wget`, `git clone`) over the added lines; a note that the leak-guard paragraphs are
  byte-identical to the parent.

### G3 — Full spec differs in exactly two fields
`diff specs/dab-anchor-codex.yaml specs/dab<NNNN>-<slug>.yaml` shows **only** `experiment:` and
`solver_workflow:` changed. `agent.kind: spacedock_solver` and `runtime: codex` are preserved.
- **FAIL if:** any third field differs; `agent.kind` or `runtime` changed; `trials` ≠ 1.
- **Evidence to cite:** the two-line diff.

### G4 — Smoke spec adds only tasks + exclude_tasks
`diff specs/dab<NNNN>-<slug>.yaml specs/dab<NNNN>-<slug>.smoke.yaml` shows **only** an added
`benchmark.tasks:` block (the dataset names whose queries the smoke needs) and a
`benchmark.exclude_tasks:` block (the `{dataset}-q{n}` ids to drop). Nothing else differs.
The surviving per-query set (targets + canaries) is what the propose stage verified with
`rk run <smoke-spec> --explain`.
- **FAIL if:** the smoke spec changes any field other than `benchmark.tasks` / `benchmark.exclude_tasks`;
  `tasks` lists per-query ids instead of dataset names (the plugin selector takes dataset names
  only — query-level filtering happens via `exclude_tasks`); the surviving query set does **not**
  include every target query the hypothesis's `## Hypothesis` names.
- **WARN if:** the surviving set has no stable-`@baseline`-pass regression sentinel.
- **Evidence to cite:** the smoke diff and the `--explain`-confirmed surviving task list.

### G5 — Both specs frozen, kind/runtime preserved
`specs/dab<NNNN>-<slug>.frozen.yaml` and `…smoke.frozen.yaml` both exist; both still carry
`agent.kind: spacedock_solver` and `runtime: codex`.
- **FAIL if:** either frozen file is missing, or a frozen file dropped `kind`/`runtime`.
- **Evidence to cite:** `ls` of the frozen files + the kind/runtime lines.

### G6 — Resolver fidelity (matches the plan)
The wording actually inserted into the README matches the hypothesis's Falsifiable claim:
same stage, same idea, no scope creep, and it stays **generative or independent** (it tells
the solver how to build/derive a query, or to reconcile against an independent local signal)
rather than a self-anchored "check your own work / re-run your own query" instruction.
- **Dead-family phrasings to flag** (self-anchored verification): "re-run your own query",
  "compare to the previous/old result", "verify your answer matches", "confirm the result
  equals", "check that the output is correct" with no independent source named. Their presence
  in the inserted text is a strong FAIL signal **unless** the check reconciles against a
  genuinely independent local signal (a different source table / grain / join path).
  Self-anchored **selection** — a multi-candidate protocol scored by the candidates' own
  checks — is the same disease at the protocol level; it is reviewed under **G9**.
- **FAIL if:** the inserted text diverges from the claim; it adds scope the hypothesis did
  not promise; it is a self-verification instruction that re-runs the solver's own derivation
  or compares to the pre-existing answer.
- **WARN if:** the wording is in the right stage and spirit but materially reworded from the
  claim (the captain may want to confirm the intent survived).
- **Evidence to cite:** the inserted sentence(s) quoted against the claim.

### G7 — Actionability / inert-risk (advisory, WARN-only)
The change must be expressible as something the solver implements **mechanically**, not
abstract prose it can acknowledge and skip. README prose that asks the solver to **restructure
a query** in the abstract — which table to read FROM, join direction, grain, the shape of the
answer — tends to be behaviorally **inert** at gpt-5.5/`xhigh`: the solver discusses it but the
committed SQL/answer is unchanged ("talks but doesn't do"). A concrete mechanical instruction
(a specific cast, a column to add/rename, a literal filter token, a worked-example skeleton to
copy) lands more reliably. This rule is **predictive, not an integrity check** — it never
FAILs, only WARNs, so it never blocks the gate; it flags inert-risk in the captain note.
- **WARN if:** the inserted instruction asks for a structural rewrite stated as **abstract
  prose**, *without* a worked-example skeleton or a named mechanical edit. Note the inert-risk
  and suggest the worked-example / few-shot form.
- **PASS if:** the change is a concrete mechanical substitution (a cast, column add/rename,
  literal/default value, filter token) **or** it carries a worked-example skeleton the solver
  can copy rather than re-derive.
- **Evidence to cite:** quote the instruction and classify it —
  mechanical-substitution / worked-example / abstract-structural.

### G8 — Regression-canary coverage (generative instructions, DAB stratified terms)
A **generative** instruction — one that fires on every query, not gated on a precondition that
limits it to the targets — can regress any currently-passing query it touches. A targets-only
smoke set is structurally blind to that. The metric is **stratified Pass@1** (per-query →
per-dataset mean → mean of 12 datasets), so a regression on a currently-passing query in a
non-target dataset *lowers that dataset's mean and the stratified score* even while the target
flips. A generative change must therefore carry a regression panel in its smoke spec.
- **N/A (PASS) if:** the instruction is gated/scoped to a narrow precondition or is a mechanical
  substitution on a specific construct — classify and mark N/A.
- **FAIL if:** the instruction is generative AND the smoke set (after `tasks` + `exclude_tasks`)
  keeps no currently-passing `@baseline` canary query from a dataset OTHER than the targets'
  dataset(s). Recommend keeping ≥1 passing canary from a non-target dataset (REVISE-class —
  fixable in place, idea unchanged). The three perfect-score datasets
  (bookreview / music_brainz_20k / stockindex; see `_artifacts/dataset-gap-ranking.md`) are the
  natural canary pool.
- **WARN if:** the panel has ≥1 canary but they are all **inert stable passers** the lever
  cannot fire on, OR the dataset most structurally similar to the targets carries only one
  canary. A *perturbable* canary is a passer the lever can actually FIRE on; a stable passer the
  lever never touches proves nothing. Recommend ≥2 perturbable canaries from the dataset whose
  query shape the lever's mechanism most likely perturbs.
- **PASS if:** generative AND the smoke set keeps a canary panel (≥1 non-target `@baseline`
  passer query) AND, for the construct the targets share, ≥2 **perturbable** canaries.
- **Evidence to cite:** classify the instruction (generative vs gated/mechanical); if
  generative, list the surviving non-target `@baseline`-passer queries (from
  `per_trial_outcomes.json`), and flag whether the lever can plausibly *fire* on each
  (perturbable vs inert).

### G9 — Selector independence (multi-candidate / selector protocol families)
Applies only when the hypothesis declares a **multi-candidate / selector protocol** — it runs
N candidates and selects one; mark **N/A (PASS)** otherwise. The failure mode is the
**fake-independence selector**: photocopy candidates judged by their own light. Check both axes:

- **(a) Generation independence — are the N candidates real, or one mind photocopied?**
  The harness runs **one solver session per query** (`trials: 1`, single `agent`), so a
  README-only protocol that says "run N ≥ 3 candidates" is necessarily *simulated inside one
  session*: every candidate shares the same exploration, context window, and first reading, so
  they converge on the same answer. To satisfy this axis the design must provide **isolation**
  (genuinely separate runs/sessions/agents — a harness/spec-level mechanism, not README prose)
  or **forced divergence** (each candidate assigned a distinct stance on the borderline
  decisions).
- **(b) Judgment independence — who grades the candidates?** List every scoring criterion the
  selector uses and name its **anchor**. A criterion computed from the candidate's **own**
  artifacts (completeness of its own result, "support N/N" against its own probes, answer
  string matches its own table) is **self-anchored selection**: a plausible-but-wrong candidate
  self-scores perfect and wins. Running real SQL against real data does **not** make a check
  independent — independence is about who *authors and interprets* the check, not whether the
  data is real. To satisfy this axis at least one load-bearing criterion must be **external to
  all candidates**: falsifier checks authored before any candidate exists, candidates
  cross-examining each other's decisions, or a per-decision adversarial probe a wrong answer
  would fail.
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
**N/A (PASS)** otherwise. A self-correcting lever is most dangerous on the queries it should
leave alone: when the model's answer is already right but the solver's second derivation is
wrong, the rule "fixes" the right answer to the wrong one, then the DAB validator scores it 0
and the per-query `reward_per_query.json` flips a passer to FAIL. Check three axes:

- **(a) Scope — generative vs change-gated.** A self-correcting lever that fires on *every*
  query also fires on already-correct ones. To be safe it must be gated to a precondition (fire
  only when a figure/answer is genuinely in question), not run on every query.
- **(b) Independence source — separately-sourced vs re-derived.** The reconcile target must be a
  **separately-sourced** signal — a plain read from a different source table with **no shared
  query logic** — not an artifact the solver re-derives itself (a CTE sharing the same window /
  grain / join). A self-built "independent" check **re-correlates** with the answer after a fix
  and gives a false-green: the DAB validator and the solver's own reconcile both pass while the
  answer is wrong. Double-entry works only when the second entry comes from a different *source*,
  not the same hand.
- **(c) Check-don't-replace.** The instruction must trigger *investigation* of a disagreement,
  not mandate replacing a simple-correct query with a "structurally different" (and possibly
  wrong) one. "Use a different path" optimizes for *different*, not *correct*.
- **FAIL if:** the lever is self-correcting AND (a) generative with no change gate, **or**
  (b) reconciles against a re-derived artifact rather than a separately-sourced raw signal,
  **or** (c) mandates replacing/re-deriving instead of investigating.
- **WARN if:** it is gated but the gate is weak or unverifiable from the README, or the
  independence source is ambiguous.
- **Evidence to cite:** classify the lever (self-correcting vs not); quote its scope gate
  (generative vs change-gated); name what the reconcile compares against (raw source vs
  re-derived); quote any "different path" / "rewrite" mandate. Note that the DAB validator
  writes `reward_per_query.json` — a false-green here is invisible to the validator, so the
  independence source is what protects the passer.

## Recommendation rubric

After scoring all ten rules, the gatekeeper emits one overall recommendation. **WARNs never
drive the recommendation by themselves** — surface them in the "For the captain" note (G7 is
WARN-only by design and always lands there). Only FAILs move it off APPROVE:

- **APPROVE** — no FAILs (any number of WARNs allowed). Nothing blocks the gate; the captain
  can advance to `smoke`. Carry every WARN into the captain note.
- **REVISE** — at least one FAIL, and **all** FAILs are on the mechanical rules
  (G1/G4/G5/G8/G9/G10) the ensign can fix in place without changing the idea; no FAIL on
  G2/G3/G6. Recommend the specific fix, then re-review. (G9 caveat: a G9 FAIL is REVISE-class
  only when independence can be added without changing the single idea; if the self-anchored
  selection criterion *is* the idea, the variant goes back to `hypothesis`. G10 caveat: same
  shape — gating a self-correcting lever, repointing its reconcile to a raw source, or softening
  "replace" to "investigate" is REVISE-class; but if an *ungated, fix-on-disagreement,
  re-derived* check **is** the idea, send it back to `hypothesis`.)
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
| G2 leak-guard intact | PASS/WARN/FAIL | <grep cite: ground_truth/db_description_withhint/curl> |
| G3 spec two fields | PASS/WARN/FAIL | <diff cite> |
| G4 smoke tasks+exclude | PASS/WARN/FAIL | <diff + --explain surviving set> |
| G5 both frozen | PASS/WARN/FAIL | <ls/head cite> |
| G6 resolver fidelity | PASS/WARN/FAIL | <claim vs inserted text> |
| G7 actionability/inert-risk | PASS/WARN | <instruction class + inert-risk note> |
| G8 regression-canary coverage | PASS/FAIL/N/A | <generative? + non-target passer canaries cited> |
| G9 selector independence | PASS/WARN/FAIL/N/A | <substrate class + per-criterion anchors> |
| G10 self-correcting false-positive | PASS/WARN/FAIL/N/A | <self-correcting? scope gate + reconcile source + replace-vs-check> |

**For the captain:** <what to look at / what to decide, 1–3 lines.>
```
