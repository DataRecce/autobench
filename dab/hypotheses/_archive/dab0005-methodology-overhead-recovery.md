---
title: crmarenapro-q2/q8 - Recover capability the three-step methodology suppresses on direct queries (structural lever)
status: concept
kind: concept
source: CAIS cross-experiment scan — minimal/direct workspaces solve crmarenapro-q8 (5/5) but spacedock suppresses it (codex 0/5)
id: dab0005
score: 0.4
completed: 2026-06-21T03:47:05Z
verdict: rejected
archived: 2026-06-21T03:47:05Z
---

## Direction

A **workflow-structural** lever: trim or gate the `model → analyze → verify` overhead for queries
where the heavyweight three-step methodology demonstrably *hurts* relative to a direct/minimal
workspace. The same model solves some queries in a minimal harness but fails them under the
spacedock README — evidence the methodology itself, not the model, is the bottleneck. This is a
WORKFLOW-REFINE candidate (it changes stage structure, not just prose), so it must record its
structural finding in `_artifacts/WORKFLOW-REFINE.md`.

## Evidence

`crmarenapro-q8`: `minimal-codex-5.5` 3/5 and `structured/direct-opus-4-6` up to 5/5 solve it, but
`spacedock-codex-5.5` is 0/5 and `spacedock-opus-4-8` (`@baseline`) is 0/5 — the spacedock surface
specifically regresses it.

## Candidate hypotheses (ideate fans into 2–5)

- A README rule that lets the solver short-circuit to a direct single-query path when the task is a
  single-fact lookup (gated, with a worked example), skipping redundant context-building.
- A "verify without re-deriving" rule that stops the verify stage from second-guessing a correct
  direct answer into a wrong one.
- A scoping rule that bounds context-building so it doesn't crowd out the actual computation.

## Target queries

Primary: `crmarenapro-q8`. Watch for regressions on currently-passing spacedock queries (any
canary) — methodology changes are blast-radius-wide; smoke must carry strong cross-family canaries.
