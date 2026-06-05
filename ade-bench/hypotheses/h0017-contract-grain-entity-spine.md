---
id: h0017
title: Output Contract — a NEW stage that, before any SQL is written, records each model's grain key-set from the NAMED local relation the existing code/instruction treats as the FROM driver, and copies THAT spine (entity FROM, children LEFT JOINed) — leaving any downstream coalesce/default where it already lives
status: propose
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type 1a - Grain - entity spine (missing parent rows)); realizes the new Output Contract stage. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed:
verdict:
score:
worktree:
---
## Hypothesis

Six tasks fail with the same entity-spine grain bug: the solver builds an aggregate keyed on
only the entities that have a matching child row, dropping the parent rows with zero children.

- `intercom001` (`AUTO_intercom__threads_equality`, `Got 7`), `intercom002`, `intercom003` —
  "create a model that aggregates the conversation parts by conversation_id …". The baseline
  builds the aggregate off the child (conversation parts), so conversations with no parts
  drop out of the grain.
- `asana004` (`AUTO_int_asana__project_user_agg_equality`, `Got 3`), `asana005`,
  `asana005-hard` — "refactor `asana__project`: move the `agg_project_users` and
  `count_project_users` CTE calculations into a new `int_asana__project_user_agg`". The
  baseline lifts the two child-grain CTEs verbatim (one row per project that HAS a user, 13
  rows) instead of the full 16-project spine the downstream model joins onto.

The dead-prose ledger says this diagnosis is correct but the prior interventions could not move
the committed SQL. h0010 stated the fix as **prose** in Implementation ("build FROM the entity,
LEFT JOIN children") and was wholly inert (0/4 — `Got 3`/`Got 7` unchanged; `asana004`
byte-identical to baseline). h0016 restated it as a **generic before/after SQL skeleton** in
Implementation; it reached the committed SQL only on `intercom001` (`Got 7 -> 5`) and flipped
0/4 because a generic placeholder skeleton installs the SHAPE but not the task-specific correct
spine SOURCE. Both fired AT Implementation time and asked the solver to restructure SQL in the
moment of writing it.

**Falsifiable claim (the single README change — a NEW `## Stage: Output Contract` between
Exploration and Implementation):** adding one stage that, on author/restructure tasks only,
makes the solver FIRST write down each model's grain key-set sourced from a **named local
relation** — the relation the existing code or instruction treats as the FROM driver — and
then reproduce THAT spine (entity `from`, children `left join`ed) in the model it authors,
with two guards (same-thing-same-shape; do-not-narrow), will flip the reachable intercom
grain-spine failures and let Implementation become a fill-in measured against the written
contract, raising `stratified_pass_at_1` above the `@baseline` 0.6458.

Why this escapes the README-prose ceiling that sank h0010/h0016, on the reachable subset: it
is anchored to a **concrete, copyable, same-domain local artifact**, the one mechanism class
that ever landed (asana002, h0009). For `intercom001/002/003` that artifact is verified
present in all three task workspaces: `models/intermediate/int_intercom__conversation_part_aggregates.sql`
already aggregates the SAME child (conversation parts) by the SAME entity (conversation) with
the correct entity spine — `from latest_conversation left join latest_conversation_part …
group by conversation_id` — and it is already the `from` driver of
`intercom__conversation_metrics.sql`. All three instructions ask for exactly that aggregation,
so the stage names a real copy template (the solver copies the spine + join direction, then
renames to the instruction's columns — `count_total_parts` -> `total_conversation_parts`,
etc.). The lever moves the control point EARLIER (write the contract before any SQL) and frames
the fix as copy-the-named-analog-spine, not the inert "restructure your query".

**Target reachability is split, and recorded honestly.** PRIMARY (reachable, concrete
copyable analog): `intercom001/002/003`. SECONDARY/stretch (high inert-risk): `asana004/005/005-hard`
are REFACTOR tasks ("move these two CTEs") that h0016 proved inert on (`Got 3 -> 3`, CTEs
lifted verbatim). For these the correct extracted model needs a full 16-row `from project left
join agg/count` spine with `number_of_users_involved` left raw downstream, which is a
structural rewrite the literal instruction does not demand. The stage gives the asana case a
single mechanical rule (the refactor worked example: the new model must `select from <entity>`
and `left join` the two aggregate CTEs; do NOT move the `coalesce`; do NOT narrow to the
child-CTE output) but the verdict must NOT be judged a failure if these structurally-inert
refactors do not flip — they are carried for coverage, and the deep-dive reads the committed
`apply_patch` SQL + `Got N` distance, not the transcript.

The oracle signature is locally derivable on the reachable subset (the intercom analog ships
the correct entity-spine; the asana spine and the downstream `coalesce` are both readable in
`asana__project.sql`), but the solver cannot self-verify the exact answer (no `tests/`, no
solution seeds in `/app`) — so this targets exactly the locally-derivable shape bug and stays
out of the value-divergence zones.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact: the inserted stage references only local relations
the solver already has (the intercom intermediate analog, the asana `project` spine, the CTEs
the downstream model joins onto), uses generic placeholder names in its worked examples
(`model_x`, `agg_a`, `count_b`, `<entity>`, `<conversation>`), and contains no
`AUTO_*`/`solution__*`/`check_*`/verifier tokens, no "equality test"/"has less columns"/
"expected output seed", no `Got N` magnitudes, and no external fetch (`curl`/`wget`/`git
clone`/`git ls-remote`/web). The leak-guard prose (README lines 1-32) is byte-identical to
parent; the spec differs from baseline only in `experiment:` + `solver_workflow:` (smoke may
add only `benchmark.tasks`).

This is **generative** (it fires on every author/restructure task, gated by the
no-op/pure-repair skip), so per gatekeeper G8 the smoke set carries a cross-family
regression-canary panel — one currently-passing `@baseline` task from each other family:
`ade-bench-airbnb001`, `ade-bench-ana-eng001`, `ade-bench-asana001`, `ade-bench-f1007`,
`ade-bench-quickbooks002` (all verified reward=1.0 in
`runs/ade-bench-baseline/622bdedac572b479/per_trial_outcomes.json`). **No intercom canary is
possible:** `intercom001/002/003` all FAIL at `@baseline` (reward 0.0), so that family supplies
no passer — G8 should not expect one. The convention-bleed risk that lost h0009 -3 at full
scale is contained by the two guards (same-thing-same-shape; project-structure-wins-on-conflict)
and the author/restructure applicability gate.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h<NNNN>-contract-grain-entity-spine.yaml` shows
only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
is a single addition inserting the new `## Stage: Output Contract` block between
`## Stage: Exploration` and `## Stage: Implementation`, leaves Exploration / Implementation /
Validation / Finalization and the dependency/package guardrails untouched, keeps the leak-guard
prose (README lines 1-32) byte-identical, and references no hidden `AUTO_*`/`solution__*`/
verifier tests. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`. The deep-dive must read the COMMITTED SQL (the
dispatched-ensign `apply_patch` payload / final model SQL) and the `Got N` distance-to-pass,
not the transcript chatter — h0010/h0016 confirmed solvers discuss "spine/grain/left join"
while the committed SQL is unchanged.

**Smoke gate:** on the 6 targets + 5 cross-family canaries — primary reachable targets
`intercom001/002/003`; secondary/stretch (high-inert refactors) `asana004/005/005-hard`;
canaries `airbnb001` / `ana-eng001` / `asana001` / `f1007` / `quickbooks002` (intercom supplies
no canary, structurally) — the variant must not regress any canary and should flip at least one
of the three intercom targets to a pass before promotion to full. Asana not flipping is NOT a
NO-GO by itself (recorded as the h0016-confirmed structural-refactor inert case); a canary
dropping FAIL is a NO-GO regardless of target movement.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
