---
id: h0021
title: Implementation — when a fix re-types a key, keep the dedup/ranking window deterministic under the original type via an in-place cast in the ORDER BY
status: propose
kind: hypothesis
source: innovate-bugtype-fixes workflow (bug type Value divergence (shape right, numbers wrong) — type-dependent dedup/ranking ORDER BY ordering sub-bug (ana-eng007 dim_products). f1006 residual excluded (not locally derivable). ana-eng007-medium demoted to sentinel per the critique (h0013 1->3 regression risk under its vague 'fix everything' instruction).); in-stage lever (Implementation). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-05T00:00:00Z
completed:
verdict:
score:
worktree:
---
## Hypothesis

The value-divergence cluster has one sub-bug whose fix is a literal, copyable in-place SQL
edit in the model's OWN file — the type-dependent dedup-ordering bug in `ana-eng007`
(`dim_products`). The model deduplicates with
`row_number() OVER(PARTITION BY product_id ORDER BY product_id) ... WHERE row_number = 1`
(`environment/project/models/warehouse/dim_products.sql`, lines 22-24), and `product_id` is
`p.id` (line 3). The task instruction is *"The id field in the 'products' table is now a
string. This has broken several models. Update them so that they work with product ids that
are strings."* The `@baseline` solver re-typed the id to a string and confirmed the row
count + column type, but left the `order by product_id` sorting **lexicographically** —
so for products that share an id, `'10' < '2'` selects a DIFFERENT surviving row than the
original numeric order did, and the dedup keeps the wrong row. Shape (row count, columns,
types) all look right; the **values** of the surviving duplicate-id rows are wrong. This is
exactly the value-divergence signature: shape right, numbers wrong.

The signal is **local and concrete**: the unstable `ORDER BY` is visible in the model the
solver is editing, and the natural fix is to keep the ordering deterministic under the
original numeric type — `order by cast(product_id as integer)`. That is a one-token in-place
substitution inside an expression already in the file, the **asana002-class mechanical edit**
(the only edit shape that has ever landed a FAIL→PASS on this benchmark, per the landed-mechanism
ledger: a column-type cast copied from a concrete local artifact). It is NOT a structural
rewrite (which table to build FROM, join direction, grain) — the class of ask that was
behaviorally inert in h0010 (prose, 0/4) and only-installs-the-shape in h0016 (worked-example,
0/4). It points at an expression already present and asks for a substitution, not a new query
shape.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation paragraph — *when a fix changes a column's data type, also fix every place that
column drives a sort order, and in particular any `row_number()` / `rank()` / `qualify` / dedup
window that keeps one surviving row per key via an `order by` on that column; an `order by` on
a now-string key sorts lexicographically and can keep a different surviving row, silently
changing values while the row count and type still look right; where the surviving row must
not depend on the new representation, keep the original ordering by casting the key back to its
prior numeric type inside the `order by` only (a one-token in-place edit, e.g.
`order by cast(<key> as integer)`), leaving columns, grain, and the rest of the SQL exactly as
the project defines them; this is an in-place substitution in the existing window, not a
restructure, and applies only where such a window already exists* — will let the solver fix the
type-dependent dedup-ordering divergence in `ana-eng007` (`dim_products`), flipping it to a
pass and raising `stratified_pass_at_1` above the `@baseline` 0.6458, while the
within-family sentinel `ana-eng007-medium` and the cross-family canary panel do not regress.

**Why it escapes the dead-prose ceiling.** The ceiling levers (h0010 prose, h0011 full-column,
h0016 worked-example skeleton) all asked the solver to **restructure** SQL — choose a different
spine, a different join, a wider derived column set — and were acknowledged-but-not-executed or
installed-the-shape-but-not-the-correct-content (0/4, 0/3, 0/4). This rule asks for none of
that: it points at a single `order by` expression **already in the committed file** and asks
for a one-token cast. That is the same edit shape as the only target that ever flipped
(asana002 under h0009: a `::timestamp` cast copied from a local artifact). It MUST change the
committed SQL (Implementation stage, build-time construction), not add a post-hoc
self-anchored Validation check — the dead family (h0006/h0007/h0008) where the solver
reconciles against its own wrong computation. Residual inert-risk is real, not zero: the
signal map marks this PARTIAL — the hazard is fully visible but the exact correct surviving
rows are not self-verifiable (`warehouse/schema.yml` does not declare `dim_products`, so there
is no local `unique`/`not_null` test on `product_id`), and the `@baseline` solver actively SAW
the id was a string and chose not to touch the `ORDER BY`; the prose must overcome that active
prior choice. The smoke read will check the committed `dim_products.sql` (did the cast land?)
and the `Got N` distance, not the transcript.

**Why `ana-eng007-medium` is a sentinel, not a flip target.** It shares the `dim_products`
bug but its instruction is the vague *"The project is broken. Fix it."* — a broad-scope task.
h0013 evidence is direct: a broader/generative instruction REGRESSED `ana-eng007-medium` from
1 fail to 3 (it broke `obt_product_inventory` and `obt_sales_overview` and worsened
`dim_products` 5→10). On that fragile task the dedup fix is reachable only via wide edits that
break the two OBT models. So the focused `ana-eng007` (where the ORDER BY hazard is squarely
in scope) is the sole flip target; `ana-eng007-medium` rides along only as a within-family
sentinel that **must not regress**.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact (the inserted text references only the model's OWN
existing `order by` / `row_number()` window — no public fetch, no oracle, no reference to
hidden `AUTO_*`/`solution__*` tests, no `Got N` magnitude). The full spec differs from baseline
only in `experiment:` + `solver_workflow:` (smoke may add only `benchmark.tasks`).

This rule is **generative** (it is evaluated on every task) but is a **no-op unless a
type-changed key drives an existing dedup/ranking `order by`** in the model being edited, so
its effective blast radius is narrow. Per gatekeeper G8 the smoke set carries a cross-family
regression-canary panel — one currently-passing `@baseline` task from each non-target family:
`ade-bench-ana-eng001` (ana-eng), `ade-bench-asana001` (asana), `ade-bench-quickbooks002`
(quickbooks), `ade-bench-f1007` (f1 — a non-package task, to catch convention-bleed), and
`ade-bench-airbnb001` (airbnb). **No intercom canary is possible:** intercom has no passing
`@baseline` task (`intercom001/002/003` all fail), so that family cannot supply a passer — G8
should not expect one.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h<NNNN>-implementation-stable-dedup-ordering-under-type-change.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Implementation` (the single in-place ORDER-BY-cast paragraph, inserted
after the `...schema patterns.` line and before `Run basic confirmation...`), leaves
Exploration/Validation/Finalization and the dependency/package guardrails (lines ~1-32)
byte-identical, and does not reference hidden `AUTO_*`/`solution__*`/verifier tests or weaken
the leak-guard. `agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0` (confirm `<run-dir>/<cell>/subagent-trace-manifest.json`).

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`. (Compute the paired delta from
`per_trial_outcomes.json` slug-paired + 10k bootstrap, since `rk runs diff` crashes on
ade-bench run-dirs with `query_id: null`.)

**Smoke gate:** on the target `ade-bench-ana-eng007` + the within-family sentinel
`ade-bench-ana-eng007-medium` + the cross-family canary panel (`ana-eng001`, `asana001`,
`quickbooks002`, `f1007`, `airbnb001`), the variant must flip `ana-eng007` FAIL→PASS and must
NOT regress the sentinel or any canary. A canary dropping FAIL is a NO-GO regardless of the
target flip. Before reading any transcript, confirm the committed `dim_products.sql` carries
the in-place `order by cast(...)` edit and check the `Got N` distance vs `@baseline` — an
unchanged committed `ORDER BY` means the lever was inert.

## Gatekeeper review

**Recommendation: APPROVE** — clean integrity rules (G1/G2/G3/G6 PASS), a concrete one-token in-place cast (G7 PASS), and a present-but-thin G8 panel (two WARNs, no FAIL): the construct-sharing family ana-eng carries only one canary and the whole panel is inert stable passers the lever cannot fire on.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-07T04:54:54Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff is a pure addition `55a56,68` (one paragraph) falling under `## Stage: Implementation` (header at L50; inserted L56-67, after `…schema patterns.` L54, before `Run basic confirmation…` L69). Exactly one stage, exactly one idea (in-place ORDER-BY cast); no other stage or guardrail prose touched. |
| G2 leak-guard intact | PASS | Lines 1-32 (leak-guard + dependency/package prose) byte-identical to parent (`diff` empty). Grep of inserted L56-67 for curl/wget/git-clone/ls-remote/AUTO_*/solution__*/check_option/verifier/equality-test/expected-output/`Got N`/http/download/fetch = NONE. Inserted text references only the model's OWN existing `order by`/`row_number()` window. |
| G3 spec two fields | PASS | `diff baseline.yaml h0021.yaml` shows only L2 `experiment:` and L11 `solver_workflow:`. `agent.kind: spacedock_solver` (L4), `runtime: codex` (L5), `trials: 1` (L24) all preserved/unchanged. |
| G4 smoke tasks-only | PASS | `diff h0021.yaml h0021.smoke.yaml` = only an added `benchmark.tasks:` block. All 7 slugs `ade-bench-` prefixed. Includes the target `ana-eng007` plus a stable-@baseline-pass regression sentinel (5 passing canaries) — no WARN. |
| G5 both frozen | PASS | Both `…frozen.yaml` and `…smoke.frozen.yaml` present (1759 / 1931 bytes). Each carries `kind: spacedock_solver` (L4) + `runtime: codex` (L5) + repointed `solver_workflow` (L11). |
| G6 resolver fidelity | PASS | Fork parent resolves cleanly: `source:` = codex-ade-dbt-minimal; `@baseline` = run 622bdedac572b479 → solver_workflow codex-ade-dbt-minimal (agree). Inserted text matches the Falsifiable claim (Implementation stage; cast the re-typed key back inside an existing `order by` only). Generative-construction lever, not self-anchored verification — no dead-family ("re-run your own", "drive to zero", "verify matches") phrasing. |
| G7 actionability/inert-risk | PASS | Mechanical substitution: a concrete one-token cast `order by cast(<key> as integer)` inside an expression already in the file (asana002-class). NOT a FROM/spine/join/grain restructure — none of the h0010 abstract-structural inert-risk phrasings. Residual inert-risk (the @baseline solver actively saw the string id and chose not to touch the ORDER BY) is real and self-flagged in the body; the worked literal mitigates it. |
| G8 regression-canary coverage | WARN | Generative but no-op unless a type-changed key drives an existing dedup/ranking `order by` (narrow blast radius). Panel verified against run 622bdedac572b479: ana-eng001/asana001/quickbooks002/f1007/airbnb001 all reward=1.0 PASS — one passer per available non-target family (intercom001/002/003 all FAIL, so no intercom passer is possible — correctly excused). FAIL clause does NOT trigger (coverage present). Two WARN conditions DO: (1) the construct-sharing target family **ana-eng carries only ONE canary** (ana-eng001) though 6 ana-eng passers exist (001/002/002-medium/003/005/008) — a generative rule can break a different ana-eng member than the one picked (h0012 broke 4 other f1 passers its single canary never covered); (2) all 5 canaries are **inert stable passers** the lever cannot fire on (none re-types a key into a dedup `order by`). WARN, not FAIL. |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol; single in-place cast inside one solver session. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever; it is a build-time construction guard that changes the committed SQL, not a verify-and-act-on-disagreement rule. |

**For the captain:** No FAILs → nothing blocks advancing to `smoke`. Two G8 WARNs to weigh: the panel proves the lever does not break the broad families, but it is structurally blind to a within-ana-eng regression (only ana-eng001 carries the family, and it is inert) — exactly the h0012 "broke a different family member" hole. Consider adding ≥2 *perturbable* ana-eng passers (ideally any that involve a sort/dedup the cast could perturb) before or alongside smoke. G7 inert-risk is the live question: the @baseline solver saw the string id and deliberately left the ORDER BY; the prose must overcome that prior choice — confirm at the smoke gate by reading the committed `dim_products.sql` for the landed `order by cast(...)` and the `Got N` distance, not the transcript.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: Forked solver README adds EXACTLY the in-place ORDER-BY-cast paragraph as ONE Implementation-stage idea; leak-guard / dependency prose byte-identical to parent.
  `diff codex-ade-dbt-minimal/README.md h0021-.../README.md` = pure addition at `55a56,68` (one paragraph inside `## Stage: Implementation`, after `...schema patterns.`, before `Run basic confirmation...`); lines 1-32 (leak-guard/dependency) untouched.
- DONE: Full spec differs from baseline ONLY in experiment + solver_workflow; smoke spec adds benchmark.tasks with the 7 tasks named in the body.
  `diff baseline.yaml h0021-...yaml` = only lines 2 + 11; smoke adds the same two + a `tasks:` block (ana-eng007, ana-eng007-medium, ana-eng001, asana001, quickbooks002, f1007, airbnb001).
- DONE: Both specs frozen via `rk freeze --allow-missing`; agent.kind=spacedock_solver and runtime=codex preserved in both.
  Wrote h0021-...frozen.yaml + h0021-...smoke.frozen.yaml; grep confirms `kind: spacedock_solver` + `runtime: codex` + repointed solver_workflow in both frozen files.
- SKIPPED: Gatekeeper (Output 5).
  Per dispatch — the FO dispatches an INDEPENDENT gatekeeper review after completion; the ensign does not self-run it.

### Summary
Forked `codex-ade-dbt-minimal` -> `solver_workflows/h0021-implementation-stable-dedup-ordering-under-type-change` and inserted a single surgical Implementation-stage paragraph: when a fix re-types a key, keep an existing dedup/ranking `order by` deterministic under the key's ORIGINAL type via an in-place `cast(<key> as integer)` inside that same window — referencing only the model's own existing `row_number()`/`order by`, no new derivation. Full + smoke specs created and frozen (only experiment+solver_workflow differ from baseline; smoke adds 7-task selector). @baseline rewards resolved from run 622bdedac572b479: target ana-eng007 FAIL (0.0), within-family sentinel ana-eng007-medium also FAIL (0.0 — it shares the dim_products bug but under a vague broad-scope instruction; "must not regress" = must not drop below its current 5-fail state, NOT a flip target), all 5 cross-family canaries PASS (1.0). Generative-but-narrow lever (no-op unless a type-changed key drives an existing dedup `order by`), so G8 canary panel is carried; G10 does not apply (this is a construction guard, not a check/reconcile/validate-and-fix lever). Did Outputs 1-4 only; gatekeeper deferred to the FO's independent dispatch.
