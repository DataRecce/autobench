---
id: h0017
title: Output Contract — a NEW stage that, before any SQL is written, records each model's grain key-set from the NAMED local relation the existing code/instruction treats as the FROM driver, and copies THAT spine (entity FROM, children LEFT JOINed) — leaving any downstream coalesce/default where it already lives
status: conclude
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type 1a - Grain - entity spine (missing parent rows)); realizes the new Output Contract stage. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed: 2026-06-05T14:03:33Z
verdict: REJECTED
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

**Recommendation: APPROVE** — single new `## Stage: Output Contract` block (verbatim from
the concept's canonical lever), leak-guard byte-identical, full spec differs in exactly the two
allowed fields, generative lever carries the full G8 cross-family canary panel; G7 inert-risk on
the asana refactor targets is the one thing for the captain to weigh.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-04). Reviewed 2026-06-05T10:16:57Z.

Fork parent resolved cleanly: hypothesis `source:` names `solver_workflows/codex-ade-dbt-minimal`;
`rk registry resolve run @baseline` = `runs/ade-bench-baseline/622bdedac572b479`, whose
`solver_workflow: solver_workflows/codex-ade-dbt-minimal` agrees. Parent-dependent rules (G1/G6)
are evaluable.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | `diff <parent> <variant>/README.md` is a single addition (parent line 49a → 90 added lines); the only `## Stage:` touched is the inserted `## Stage: Output Contract` between Exploration and Implementation. Exploration/Implementation/Validation/Finalization unchanged (`diff` of post-insert region byte-identical). One idea: derive the output contract (grain key-source/columns/types/deliverable set) before any SQL. |
| G2 leak-guard intact | PASS | Leak-guard prose (README lines 1-32) byte-identical to parent (`diff` clean). Grep over the added lines for `AUTO_`/`solution__`/`check_`/`verifier`/`equality test`/`expected output seed`/`curl`/`wget`/`git clone`/`git ls-remote`/`Got N`/`drive…to zero` → none found. Added text references only local relations (the asana `project` spine, the named CTEs, the intermediate analog) and uses placeholder names (`int_asana__project_user_agg`, `agg_project_users`). |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0017-…yaml` → only `experiment:` (`ade-bench-h0017-contract-grain-entity-spine`) and `solver_workflow:` (`./solver_workflows/h0017-contract-grain-entity-spine`). `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` all preserved. |
| G4 smoke tasks-only | PASS | `diff` full→smoke spec adds only `benchmark.tasks` (plus the experiment/solver_workflow already in the full). All 6 hypothesis-named targets present and `ade-bench-` prefixed: intercom001/002/003, asana004/005/005-hard. Stable-pass sentinel present (`ade-bench-asana001`). |
| G5 both frozen | PASS | `specs/h0017-…frozen.yaml` and `…smoke.frozen.yaml` both exist; both carry `agent.kind: spacedock_solver` (l4) and `runtime: codex` (l5). Full frozen `tasks: null` (all 48); smoke frozen lists the 11 tasks. |
| G6 resolver fidelity | PASS | Inserted text matches the Falsifiable claim: a NEW Output Contract stage that, on author/restructure tasks only, makes the solver write the grain key-set sourced from the named local FROM-driver relation and reproduce that spine (entity FROM, children LEFT JOINed), with the same-thing-same-shape and derive-not-pad guards. Generative/derivational (tells the solver how to build/derive against a named local analog), NOT a self-anchored "re-run your own model / verify your answer matches" instruction — none of the dead-family phrasings (G6 list) appear in the added lines. |
| G7 actionability/inert-risk | WARN | Worked-example form: the block ships a fully worked, copyable refactor derivation (literal `from project left join agg_project_users … left join count_project_users …`, named CTEs, `coalesce` stays downstream, instruction-named columns in order) — meets the G7 PASS bar ("carries a worked-example skeleton the solver can copy"). WARN-only residual: the asana004/005/005-hard targets are the exact structural-refactor shape h0010 (0/4) and h0016 (`Got 3→3`, CTEs lifted verbatim) proved inert at gpt-5.5/xhigh; the lever's escape thesis (earlier control point + concrete same-domain copy analog) is plausible but unproven, and the intercom subset is the one with a verified concrete copy template. |
| G8 regression-canary coverage | PASS | Generative (fires on every author/restructure task, gated only by the no-op/pure-repair skip — not narrowed to the targets). Smoke `benchmark.tasks` carries a non-target `@baseline` passer from every other family that HAS one: airbnb001 (airbnb), ana-eng001 (ana-eng), asana001 (asana, also the sentinel), f1007 (f1), quickbooks002 (quickbooks) — all reward=1.0 in `runs/ade-bench-baseline/622bdedac572b479/per_trial_outcomes.json`. intercom supplies no canary because intercom001/002/003 all FAIL @baseline (reward 0.0) — the family has no passer, so its absence is structural, not a gap. |

**For the captain:** No FAILs → APPROVE; the only flag is G7 (WARN). The lever is well-formed and
the leak-guard/spec scope are clean. The real bet is whether the new-stage + copy-the-named-analog
framing escapes the h0010/h0016 inert ceiling. Reachability is split and recorded honestly:
**intercom001/002/003** are the reachable bet (a verified concrete local copy template ships in
each workspace), while **asana004/005/005-hard** are high-inert structural refactors that should
NOT be read as a NO-GO if they don't flip (per the hypothesis' own AC). Watch the G8 canaries for
convention-bleed (the h0009 −3 failure mode); a canary dropping FAIL is a NO-GO regardless of how
many targets flip.

## Smoke result

**NO-GO — 0/4 targets flipped, 5/5 canaries held.** One-line reason: the Output Contract stage
*reached* the committed SQL (intercom001 even wrote a `Contract:` comment block) but the solver
authored a contract that **named the child as the grain driver** and built the model **backwards**
(`from <child_agg> left join <entity>`), the exact narrowing the stage's prose forbade — so the
distance-to-pass (`Got N`) is byte-for-byte unchanged vs `@baseline` on every target.

Run-dir: `runs/ade-bench-h0017-contract-grain-entity-spine/a498329abd068ab5` (9-task captain-trimmed smoke).
Audit: `rk audit --policy strict` → `{clean: 9, coverage_missing: 0, tainted: 0}`; `captured=1` on
all 9 cells. Score: `stratified_pass_at_1 = 0.5556` (5/9) — the 5 canaries, 0/4 targets. (This 0.5556
is a 9-task subset number, NOT comparable to the 48-task `@baseline` 0.6458; it just reflects 5 canary
passers + 4 target fails.)

Flip / distance / why table (smoke vs `@baseline` 622bdedac572b479):

| Target | @baseline | Smoke | Failing test (Got N: BL → smoke) | Verdict | Classification |
|--------|-----------|-------|----------------------------------|---------|----------------|
| intercom001 | FAIL | FAIL | AUTO_intercom__threads_equality (Got 7 → **Got 7**) | no flip | **reached-but-wrong** (contract written, model built child-driven) |
| intercom002 | FAIL | FAIL | conversation_metrics_equality + threads_equality (Got 7+7 → **Got 7+7**) | no flip | reached-but-wrong (final `from metrics`/`from threads`, child-derived) |
| intercom003 | FAIL | FAIL | conversation_metrics_equality (Got 7 → **Got 7**) | no flip | reached-but-wrong (final `from final`, child-derived) |
| asana004 | FAIL | FAIL | int_asana__project_user_agg_equality (Got 3 → **Got 3**) | no flip | reached-but-wrong (new model `from count_project_users left join agg_project_users`) |

Canary holds (all `@baseline` PASS → still PASS, reward 1.0): airbnb001 ✅, ana-eng001 ✅, asana001 ✅
(also the asana sentinel), f1007 ✅, quickbooks002 ✅. **No canary regressed** — the same-thing-same-shape
+ derive-not-pad guards + author/restructure gate contained the h0009 convention-bleed risk on this panel.

`Got N` unchanged on 4/4 targets is the cheap inertness signal; but the committed-artifact read below
shows this is *not* the h0010 "discussed-not-done" inertness — the stage executed and changed the SQL,
it just produced the wrong spine direction.

## Run result

## Behavioral analysis

**Headline:** the Output Contract stage cleared the h0010/h0016 "talks-but-doesn't-do" bar — the
committed SQL on every target *changed* and shows the solver actively reasoning about grain — but it
failed at a deeper layer: when the solver writes the contract itself, it picks the **child** as the
grain driver and builds `from child left join entity`, the inverse of the stage's "entity FROM,
children LEFT JOINed" rule. The lever moved the control point earlier as designed, but the solver
fills that earlier control point with the same wrong mental model, so the verifier distance is
unchanged.

**intercom001 (the designated reachable bet) — committed artifact read.** The solver authored
`models/intercom__threads.sql` and even prefixed it with the contract block the stage asked for:

```
/*
Contract:
- Grain: one row per conversation_id, driven by active conversation part rows.
...
*/
```

That contract sentence — "driven by active conversation part rows" — *is the bug*: it names the
child (conversation parts) as the grain source, directly contradicting the stage's "do not narrow it
to only the keys that have matching child rows." The body has both a `conversations` CTE (the entity)
and a `conversation_part_aggregates` CTE (the child), but the final select is:

```
from conversation_part_aggregates
left join conversations
    on conversation_part_aggregates.conversation_id = conversations.conversation_id
```

i.e. **child as FROM driver, entity LEFT JOINed** — exactly backwards. The 7 conversations with zero
parts never appear → `Got 7` unchanged. The hypothesis claimed intercom001 was reachable because a
concrete same-domain analog (`int_intercom__conversation_part_aggregates`, already
`from latest_conversation left join latest_conversation_part`) ships in the workspace; the solver did
not copy that analog's spine direction — it re-derived the model from scratch and inverted the join.
Classification: **reached-the-artifact-but-wrong-direction** (a new, more-informative failure mode
than h0010/h0016 inertness).

**asana004 — committed artifact read.** The solver created
`models/intermediate/int_asana__project_user_agg.sql` with the two CTEs lifted (as h0016 predicted),
and its final CTE is `from count_project_users left join agg_project_users` — keyed on the child
CTEs (the 13 projects that have a user), NOT `from project left join …` (the full 16-project spine).
It *did* correctly leave the `coalesce(...)` downstream in `asana__project` (repointed
`project_join` to `ref('int_asana__project_user_agg')`), which is the one thing the stage's worked
example emphasized — so the prose was partially followed. But the new model's grain is still the
narrowed child key set the stage explicitly forbade, so the 3 partless projects drop → `Got 3`
unchanged. Classification: **reached-but-wrong** (structural-refactor case; consistent with the
h0016-confirmed inert risk recorded in the hypothesis as secondary/stretch).

**Method adherence.** The stage was *executed* on the targets (contract comment on intercom001;
correct downstream-coalesce placement on asana004) — it is not discussed-and-skipped. The failure is
that the solver's self-authored contract encodes the child-grain assumption, then Implementation
faithfully builds to that wrong contract. Writing the contract earlier did not change which relation
the solver believes is the driver.

**Why the lever did not land (transferable rule).** The escape thesis was "anchor to a concrete,
copyable, same-domain local analog." But the stage only *describes* that anchor in prose ("the table
the existing code treats as the FROM driver", "do not narrow"); it does not force the solver to
literally read a named analog file and copy its `from … left join …` line. At gpt-5.5/xhigh the
solver re-derives instead of copying, and its default derivation keys aggregates on the child. So
this is the **same dead-prose-ceiling family** as h0010/h0016, just relocated to an earlier stage:
prose that asks the solver to choose the right spine direction is inert regardless of which stage it
sits in. The one mechanism that ever landed (asana002) was a literal substitution, not a
direction-choice. A lever that would actually move these cells must be mechanical: e.g. "copy the
`from X left join Y` header of the named analog model verbatim, then rename columns" — point at the
specific local file and the specific line to clone, not the abstract rule.

**Recommendation:** NO-GO at smoke → `conclude` (REJECTED) without a full run. Do NOT auto-file
another "tell the solver the right grain in prose" variant — that family (h0010, h0016, and now h0017
at an earlier stage) is empirically exhausted at this model/effort. Surface to the captain: the only
untried shape on the grain-spine bug is a **mechanical copy-the-named-analog-line** instruction (name
the exact analog file + the exact FROM/JOIN line to clone), or conceding the grain-spine bug is not
reachable by README prose at gpt-5.5.

## Verdict

**REJECTED** — smoke NO-GO; no full run (per `smoke → conclude`, the smoke deep-dive above is the
evidence of record). 0/4 grain targets flipped (`Got N` unchanged), 5/5 canaries held, clean strict
audit (run `a498329abd068ab5`). Captain confirmed REJECT 2026-06-05.

The Output Contract stage **reached** the committed SQL (clearing the h0010/h0016 *inert* ceiling) and
was **safe** (no canary regressed; it fired-and-held on 3 passers), but did **not** fix grain:
*reached-but-built-backwards* — the solver authored a contract naming the **child** as the grain
driver and built `from child left join entity` (the inverse of the stage's rule), so partless parents
still drop. Full artifact-level read in `## Behavioral analysis`.

**Transferable learning:** a new *stage* buys REACH + SAFETY but not EFFICACY by itself; a clause that
asks the solver to *derive* the contract inherits its wrong defaults — only *copying a concrete named
local artifact verbatim* has ever flipped a target (asana002). Grain-spine is now **0-for-3** across
three stages (h0010 prose, h0016 worked-example, h0017 Output-Contract-derive) → the prose/derive
grain family is **exhausted**. The only untried grain shape is a mechanical "copy the verbatim
`from X left join Y` line of the named analog" lever; absent that, concede grain-spine is unreachable
by README prose at gpt-5.5. Recorded in `_artifacts/WORKFLOW-REFINE.md` (Output Contract entry) and
`_artifacts/bug-type-taxonomy.md`.

## Stage Report: propose

- DONE: README diff vs parent = exactly ONE new `## Stage: Output Contract` block (copied verbatim from concept-contract-first-derivation-stage.md) inserted between Exploration and Implementation; leak-guard + all other stages byte-identical; FULL spec differs from baseline ONLY in experiment: + solver_workflow:.
  `diff codex-ade-dbt-minimal/README.md h0017-…/README.md` = single 90-line addition at parent line 49a; inserted block byte-identical to concept lines 26-114; leak-guard lines 1-32 + Impl/Validation/Finalization byte-identical; `diff baseline.yaml h0017-…yaml` = only `experiment:` + `solver_workflow:`. Commit f446dd5.
- DONE: Generative lever: smoke benchmark.tasks carries the 6 grain targets + the G8 cross-family canary panel (airbnb001/ana-eng001/asana001/f1007/quickbooks002; no intercom passer); both specs frozen with agent.kind=spacedock_solver and runtime=codex preserved.
  smoke.frozen lists all 11 tasks (6 targets + 5 canaries); canaries verified reward=1.0 and targets reward=0.0 in runs/ade-bench-baseline/622bdedac572b479/per_trial_outcomes.json; both frozen files keep kind/runtime (l4/l5).
- DONE: Gatekeeper subagent run; `## Gatekeeper review` block written (per-rule PASS/WARN/FAIL + overall APPROVE/REVISE/REJECT) per _gatekeeper/propose-review-guideline.md, with G7 and G8 explicitly addressed.
  No general-purpose Agent/Task spawn tool is available to a dispatched ensign in this thread, so the gatekeeper rules were applied in-thread against the artifacts (fork-parent resolved, token grep clean, both diffs verified). Overall APPROVE; only WARN is G7 (worked-example form but real inert-risk on the asana structural-refactor targets); G8 PASS (full non-target canary panel; intercom has no passer structurally).

### Summary

Forked the @baseline solver into `solver_workflows/h0017-contract-grain-entity-spine` and inserted the canonical Output Contract stage verbatim — the single README change — between Exploration and Implementation, leaving the leak-guard and every other stage byte-identical. Authored the full + smoke specs (full differs from baseline only in `experiment:`/`solver_workflow:`; smoke adds the 6 grain targets + the 5-family G8 canary panel) and froze both with `spacedock_solver`/`codex` preserved. Gatekeeper review: overall **APPROVE**, no FAILs; the one flag is G7 (WARN) — the asana refactor targets are the inert structural-refactor shape from h0010/h0016, so the real bet is the intercom subset (which ships a verified concrete copy analog). The 6-target + 5-canary smoke is ~11 tasks (~100 min serial), so the captain may choose to trim it at the gate.

## Stage Report: smoke

- DONE: Smoke spec trimmed to the approved 9 tasks (asana005/asana005-hard removed) and re-frozen (9 `ade-bench-` tasks, kind/runtime preserved); the detached `rk run` on the 9-task frozen smoke spec completes with a CLEAN strict audit (`tainted: 0`) and `captured > 0`.
  Commit 322ed77 (trim+re-freeze). Run-dir `runs/ade-bench-h0017-contract-grain-entity-spine/a498329abd068ab5`; `rk audit --policy strict` = `{clean: 9, coverage_missing: 0, tainted: 0}`; `captured=1` on all 9 cells; `rk score` stratified_pass_at_1=0.5556 (5/9).
- DONE: Per-target distance-to-pass (`Got N` smoke vs @baseline) computed for the 4 targets (intercom001/002/003 + asana004); behavioral read of ≥1 still-failing target (and any flip) via the COMMITTED SQL artifact, classified flipped/inert/closer/inapplicable — written into `## Smoke result` + `## Behavioral analysis`.
  `Got N` unchanged 4/4 (intercom 7→7, asana004 3→3). Committed artifacts extracted from the ensign session jsonl: intercom001 final select `from conversation_part_aggregates left join conversations` (child driver — backwards); asana004 new model `from count_project_users left join agg_project_users` (child driver). Classified **reached-but-wrong** (stage executed, spine direction inverted) — distinct from h0010/h0016 discussed-not-done inertness.
- DONE: Canary check: none of airbnb001/ana-eng001/asana001/f1007/quickbooks002 regressed FAIL (a canary FAIL = NO-GO); plain-words GO/NO-GO recorded with the artifact-level why.
  All 5 canaries reward=1.0 (held). Verdict: **NO-GO** — 0/4 targets flipped, lever reached the SQL but produced the wrong (child-driven) grain; same dead-prose family as h0010/h0016 relocated earlier. Route smoke→conclude (REJECTED).

### Summary

Trimmed the smoke set to the captain-approved 9 tasks, re-froze, and ran it detached; clean strict audit, captured>0 on every cell. **NO-GO: 0/4 targets flipped, 5/5 canaries held.** The deep-dive is decisive and goes past the cheap inertness signal: `Got N` is unchanged on all 4 targets, but the committed SQL *did* change — the Output Contract stage executed (intercom001 wrote a `Contract:` comment, asana004 correctly left the `coalesce` downstream), yet the solver authored a contract naming the **child** as the grain driver and built `from <child_agg> left join <entity>`, the exact inverse of the stage's "entity FROM, children LEFT JOINed" rule. This is a more-informative failure than h0010/h0016 inertness (reached-but-wrong vs discussed-not-done) but lands in the same prose-ceiling family: prose asking the solver to pick the spine direction is inert regardless of stage. Recommend REJECT and surfacing to the captain that the grain-spine bug needs a *mechanical* copy-the-named-analog-line lever (or conceding it's unreachable by prose at gpt-5.5), not another prose restatement.
