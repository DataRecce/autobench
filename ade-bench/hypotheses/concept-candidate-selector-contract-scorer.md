---
title: Candidate Selector / Contract Scorer -- run multiple candidate solves, then choose the committed answer by leak-safe local contract satisfaction rather than hidden oracle access
status: concept
kind: concept
source: captain strategy after Pass@k headroom evidence; Output Contract stage exists but still needs a way to choose among multiple plausible committed artifacts.
started: 2026-06-05T09:34:45Z
completed:
verdict:
score:
worktree:
id: concept-candidate-selector-contract-scorer
---

## Direction

The captain's thesis: if Pass@k shows that at least one attempt can solve a task, the next
missing mechanism is not another README rule. It is **selection**. The benchmark score is
pass@1, but the solver may produce several candidate solutions where only one is correct. We
need a leak-safe selector that chooses the best candidate using only local workspace evidence,
never the hidden verifier.

This is a declared protocol change, not a standard README-only hypothesis. It changes the
single-candidate solve loop into a two-phase solve:

1. Generate N candidate solutions for the same task.
2. Score each candidate with a local Contract Scorer.
3. Commit the highest-scoring candidate.
4. Run the normal hidden benchmark only after selection, for measurement.

The selector must not inspect hidden `AUTO_*`, `solution__*`, verifier output, public
solutions, web results, or any external reference. It can only inspect each candidate's
committed files, local dbt artifacts, source data, installed packages, schema YAML, package
models, and the task instruction.

## Why This Is Different

The recent Output Contract hypotheses try to make one solver attempt derive the right
contract before writing SQL. That may still fail in two ways:

- the solver writes the contract as chatter but commits SQL that does not satisfy it;
- two attempts derive different plausible contracts, and only one is right.

Candidate Selector / Contract Scorer moves the control point after candidate generation but
before final commit. It does not ask the same attempt to self-attest. It compares committed
artifacts across attempts using the same local scoring rubric.

This directly targets the repeated loop finding: **verify the artifact, not the transcript**.

## Contract Scorer

For each candidate, score only local, leak-safe evidence:

- **Build health:** `dbt compile`, targeted `dbt run`, targeted `dbt test`, or selected
  `dbt build` succeeds for the relevant scope.
- **Output Contract satisfaction:** committed SQL matches the recorded grain, columns, types,
  and deliverable set.
- **Artifact match:** the contract is reflected in final files, not only in notes or
  transcript claims.
- **Grain checks:** row count and key-set checks reconcile against source or declared grain.
- **Type checks:** package/source column types are preserved or cast in place when required.
- **Deliverable checks:** required refs/models exist; missing refs are resolved.
- **Package checks:** installed package templates are copied only when same-entity/same-layer
  applies.
- **Answer checks:** answer-style tasks include a per-option local-check IN/OUT table, and the
  answer string is mechanically transcribed.
- **Do-no-harm checks:** unrelated files, package namespaces, dependencies, and profiles are
  not rewritten.

The scorer should prefer a candidate that satisfies more concrete local checks. It should
reject candidates with obvious contract violations even when their transcript sounds
confident.

## Acceptance Criteria

A first hypothesis from this concept should prove:

- N candidate attempts are produced for each smoke task.
- The selector chooses one candidate without hidden oracle access.
- The chosen candidate's scorer report is saved with the run artifact.
- On smoke, selected pass@1 is better than single-attempt baseline for the same task set.
- `rk audit --policy strict` stays clean.

## Suggested First Smoke

Use tasks where Pass@k or second-oracle evidence says a pass is reachable:

- `ade-bench-asana002`
- `ade-bench-f1011`
- `ade-bench-f1006`

Add stable passing canaries from other families. The point is not broad coverage yet. The
point is to test whether local selection can recover known reachable wins without oracle
access.

## Known Risks

- The scorer may prefer a well-validated wrong candidate if the local contract is incomplete.
- Multiple attempts increase cost and runtime.
- This is not compatible with the current README-only independent-variable rule, so results
  must be labeled as a new protocol family.
- If Pass@k headroom exists but the local scorer cannot identify the passing candidate, the
  next problem is scorer quality, not candidate generation.

## Fan-out Ideas

This concept should ideate into hypotheses that each test one selector design, not one
failure-pattern fix:

1. **Static Contract Scorer:** run N candidates, score with build health + artifact contract
   checks only.
2. **Output-Contract-Aware Selector:** require each candidate to write an Output Contract,
   then select the artifact that best satisfies it.
3. **Answer-Task Selector:** for answer-style tasks, select by per-option local-check table
   completeness and answer-string transcription.
4. **Do-No-Harm Selector:** select among candidates by rejecting any that rewrite unrelated
   files, dependencies, packages, profiles, or namespaces.
