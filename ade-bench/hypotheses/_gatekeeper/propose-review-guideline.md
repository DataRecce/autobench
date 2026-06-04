---
title: Propose-stage gatekeeper review guideline
applies-to-stage: propose
maintained-by: human (edit freely; the gatekeeper reads this file fresh on every run)
last-updated: 2026-06-04
---

# Propose-stage gatekeeper review guideline

This file is the **rule set** a gatekeeper subagent applies during the `propose` stage. It
encodes the checks a human performs at the leak-guard gate, so the gatekeeper can produce an
**advisory recommendation** for the captain. The gatekeeper does **not** pass or block the
gate — the captain always makes the final decision. Edit this file by hand to tune the bar;
the gatekeeper has no memory of past versions and re-reads it each run.

## What the gatekeeper reviews

The "resolver" of a hypothesis = the forked solver workflow (`solver_workflows/h<NNNN>-<slug>/`),
its `README.md` change, and the paired specs. The gatekeeper inspects, for the hypothesis
under review:

1. The hypothesis body — its `## Hypothesis` "Falsifiable claim" (the single change it
   promised) and its named target datasets.
2. The forked solver README vs the parent `@baseline` solver it forked from
   (`solver_workflows/codex-ade-dbt-minimal` unless a newer `@baseline` is in force):
   `diff <parent-solver>/README.md solver_workflows/h<NNNN>-<slug>/README.md`.
3. The FULL spec vs baseline: `diff specs/baseline.yaml specs/h<NNNN>-<slug>.yaml`.
4. The smoke spec vs the full spec: `diff specs/h<NNNN>-<slug>.yaml specs/h<NNNN>-<slug>.smoke.yaml`.
5. The frozen artifacts: `specs/h<NNNN>-<slug>.frozen.yaml` and `…smoke.frozen.yaml`.

The gatekeeper must NOT run `rk run`, modify any file other than appending its review block to
the hypothesis file, or fetch anything external.

## Rules

Each rule has a verdict: **PASS** (clean), **WARN** (passes but worth a human glance), or
**FAIL** (a human would reject as written).

### G1 — Single idea, single stage
The README diff vs the parent solver touches **exactly one** `## Stage:` section and adds
**exactly the one idea** the hypothesis's Falsifiable claim names. No other stage, and no
unrelated guardrail prose, is modified.
- **FAIL if:** more than one `## Stage:` section changed; more than one distinct idea added;
  the change edits dependency/package/leak-guard prose instead of (or in addition to) the
  intended stage.
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
  slugs are bare (missing the `ade-bench-` prefix).
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
- **FAIL if:** the inserted text diverges from the claim; it adds scope the hypothesis did
  not promise; it is a self-verification instruction that re-runs the solver's own derivation
  or compares to the pre-existing code (the dead h0006/h0007/h0008 family).
- **WARN if:** the wording is in the right stage and spirit but materially reworded from the
  claim (the captain may want to confirm the intent survived).
- **Evidence to cite:** the inserted sentence(s) quoted against the claim.

## Recommendation rubric

After scoring all six rules, the gatekeeper emits one overall recommendation:

- **APPROVE** — all rules PASS (WARNs allowed). Nothing blocks the gate; the captain can
  advance to `smoke`.
- **REVISE** — no FAILs on G2/G3/G6 (the integrity rules), but one or more FAIL/WARN on the
  mechanical rules (G1/G4/G5) that the ensign can fix in place without changing the idea.
  Recommend the specific fix, then re-review.
- **REJECT** — any FAIL on **G2 (leak-guard)**, **G3 (spec scope)**, or **G6 (fidelity)**.
  These are integrity violations; the variant should go back to `hypothesis`.

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

**For the captain:** <what to look at / what to decide, 1–3 lines.>
```
