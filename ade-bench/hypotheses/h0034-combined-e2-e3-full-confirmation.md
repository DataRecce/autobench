---
id: h0034
title: Combined confirmation -- E2 anti-cross-join (airbnb009) + E3 rolling-window calendar-RANGE-copy (airbnb007) in ONE variant; full 48-task confirmation + promote
status: propose
kind: hypothesis
source: _proposal/oracle-problem-systematic-program.md (E2+E3 batch-full, captain 2026-06-07); confirms h0019 (airbnb009 smoke-GO) + h0018 (airbnb007 smoke-GO) at full scale in ONE run (run-economy + interaction check); promote @baseline if the paired delta clears.
started: 2026-06-07T16:22:23Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

*(Seeded by the FO; the propose stage builds the combined variant + FULL spec.)*

E2/h0019 (anti-cross-join, airbnb009) and E3/h0018 (rolling-window expressed as a calendar-date RANGE
copied from the project's own passing sibling, airbnb007) BOTH flipped their targets at smoke,
artifact-proven (the committed SQL carried the prescribed shape), with zero canary regression. Both
are independent single-rule **Implementation-stage** additions with copyable worked examples. This
combined variant carries BOTH rules and runs the **full 48-task confirmation in one run** (cheaper
than two separate fulls; also checks the two rules do not interact to harm passers) before promotion.

**Falsifiable claim:** the combined variant holds BOTH flips (airbnb007 + airbnb009 PASS) at full
48-task scale with zero NET regression; the paired `rk runs diff` delta vs `@baseline` clears the
tripwire (CI excludes a regression) on a clean strict audit; and `stratified_pass_at_1 > 0.6458`.
**Promote `@baseline`** on success. Falsified if either flip reverts at full (variance), if the two
rules interact to regress passers, or if the net delta does not clear.

This combined run **skips smoke** (both levers were already smoke-GO'd individually): `propose -> full`.

## Acceptance criteria

**AC-1 -- Combined variant README = baseline + EXACTLY the two Implementation rules.** The forked
README adds the h0019 anti-cross-join rule AND the h0018 rolling-window calendar-RANGE-copy rule
(both lifted VERBATIM from their smoke-GO forks `solver_workflows/h0019-*` and
`solver_workflows/h0018-*`), and nothing else; leak-guard + other stages byte-identical to
`codex-ade-dbt-minimal`. The FULL spec differs from `specs/baseline.yaml` only in `experiment:` +
`solver_workflow:` and carries NO `benchmark.tasks` selector (all 48). `kind: spacedock_solver`,
`runtime: codex`, `trials: 1` preserved.

**AC-2 -- Clean strict audit on the full run** (`tainted: 0`, `captured > 0` every cell).

**AC-3 -- Verdict by the paired `rk runs diff @baseline <run>` delta (CI, adjusted p) + absolute
`stratified_pass_at_1` vs 0.6458.** Promote only if the delta clears the tripwire AND both target
flips (airbnb007, airbnb009) hold artifact-proven AND no passer regressed.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
