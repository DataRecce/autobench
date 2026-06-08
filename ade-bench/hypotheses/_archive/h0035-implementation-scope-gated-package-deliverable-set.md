---
id: h0035
title: Implementation — when the project's OWN ref-graph names staging models that are absent but provided as templates by an already-installed package, materialize exactly those referenced-but-absent models (scope-gated to the referenced set); never treat an installed package as a source or add a model the project does not reference
status: conclude
kind: hypothesis
source: oracle-problem-systematic-program.md E5 (deliverable / ref-graph completion, scope-gated, MEASURED not counted); successor to archived h0015 (inert) / h0013 (inert) / h0009 (-3) / h0023 (f1001 convention-bleed NO-GO). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-08T00:00:00Z
completed: 2026-06-08T00:00:00Z
verdict: REJECTED
score: MEASURED-not-counted; @baseline unchanged 31/48
worktree:
---
## Hypothesis

`quickbooks001` is the **incomplete-deliverable** bug. The @baseline solver ships a project
that is missing three staging models — `stg_quickbooks__estimate`,
`stg_quickbooks__refund_receipt`, `stg_quickbooks__sales_receipt` — and the hidden oracle
fails it `Got 1` on **six** tests (read straight from the @baseline run-dir `622bdedac572b479`,
`ade-bench-quickbooks001__5Y3hiLq/verifier/test-stdout.txt`): each of the three models fails
BOTH its `_existence` and its `_equality` check (`actual_test_total=12, actual_pass=6,
actual_fail=6`, reward 0). The three absent models are real `fivetran/quickbooks` package
staging templates — the verifier's own build materializes all three OK — yet the solver did not
produce them.

**The decisive ground-truth fact (what the solver can see LOCALLY, and why this is reachable).**
The deciding fact lives in the project's **own ref-graph**, not in the hidden oracle: the
project's downstream models (`int_quickbooks__refund_receipt_transactions`,
`int_quickbooks__sales_receipt_transactions`, and the `*_double_entry` siblings, all visible in
the @baseline build manifest) and/or its schema declarations reference staging models named
`stg_quickbooks__{estimate,refund_receipt,sales_receipt}` that **do not exist in `models/`**,
while `packages.yml` / `dbt_packages/` already installs the `fivetran/quickbooks` package that
ships templates with **exactly those names**. The missing-model set is therefore *named by the
project itself* — a purely structural, content-independent fact derivable from the local
`ref()` graph + the installed package, with no access to the hidden `AUTO_*` tests.

**The lever (single Implementation rule, SCOPE-GATED).** Add one Implementation-stage rule:
when the project's own models or schema declarations **reference** a staging model that is
**absent** from `models/`, AND an already-installed dbt package (declared in `packages.yml` /
present in `dbt_packages/`) provides a template of that exact name, materialize exactly those
**referenced-but-absent** models from the package's templates, following the project's existing
staging naming/materialization conventions. The completion set is the set-difference
`(referenced staging models) − (existing staging models)`, resolved from the local ref-graph —
nothing else.

**The SCOPE-GATE is the load-bearing, net-new part (the h0023 fix).** The clause fires ONLY on
models the project ALREADY references but that are absent. It MUST NOT: add any model the
project does not reference; treat an installed package as a new *source*; invent `src_*` /
source declarations; or "complete" a package's full model set on a project that does not use it.
A project whose ref-graph names no missing package model gets **zero** new models. This is the
exact discipline whose absence sank h0023 — its unscoped deliverable-set clause fired on f1001
(an f1 project that references no missing package model), inventing `src_*` usage and crashing
f1001 from 6/6 to 2/6 (`stg_models_use_src_models Got 11`) — the same convention-bleed that
cost h0009 −3.

**What is and is NOT locally derivable (stated plainly).** The missing-model *names* and the
fact they exist as installed-package templates are fully locally derivable (the ref-graph + the
installed package). The models' *correct contents* are NOT independently derivable beyond the
package template — so this rule steers DELIVERABLE COMPLETENESS (build the named, referenced,
absent models), not value correctness. It is therefore expected to clear the three `_existence`
legs deterministically (the model exists and builds) and to clear the `_equality` legs only to
the extent the package template's standard staging transform matches the expected output — which
for a vanilla `fivetran/quickbooks` staging model is the canonical construction. This rule does
**not** validate against any hidden count or expected seed; the acceptance signal it can observe
locally is structural — the previously-dangling `ref()`s now resolve and the named models build.

**Falsifiable claim (the single README change — Implementation stage only):** adding one
Implementation rule that (a) computes the referenced-but-absent staging-model set from the
project's own ref-graph, (b) materializes exactly that set from an already-installed package's
templates following local conventions, and (c) is hard-scoped to the referenced-but-absent set
(never add an unreferenced model, never treat a package as a source, never invent `src_*`) —
will flip `quickbooks001` (`ade-bench-quickbooks001`) toward PASS by building the three named
staging models, with **zero regression** on the convention-bleed canaries (`ade-bench-f1001`,
`ade-bench-quickbooks003`, `ade-bench-quickbooks002`).

**MEASURED, not portfolio-counted (per the program).** `quickbooks001` is the **highest
convention-bleed-risk task in the benchmark** — h0009 (−3), h0013 (inert), h0015 (inert), and
h0023 (f1001 6/6→2/6) all bled or died here across 4 attempts, 0 flips. E5 runs LAST among
flip-seekers precisely because of this. Its flip is **measured for distance/learning, not
counted toward the net**; the binding success criterion is **zero bleed** on the canary panel.
A flip with bleed is a NET FAILURE; a no-flip with zero bleed is an honest negative that retires
this family; a clean flip with zero bleed is a counted-only-on-retrospect upside.

**Why this escapes the prior ceiling (and where it sits relative to it).** h0013 (Exploration
"enumerate the complete deliverable set") and h0015 (Implementation "repair package model
coverage") were INERT — the 3 model names never appeared in the committed project (0× build).
This rule is shaped to land where they didn't: it pins the trigger to a concrete local artifact
(the project's own dangling `ref()`s to package-template names) and prescribes a concrete
mechanical action (materialize exactly the set-difference from the installed templates), the
copyable-action shape that has landed (asana002 cast, h0019 anti-cross-join) where restructure-
prose went inert. h0023 was NOT inert — it FIRED, but unscoped, and bled f1001. So the net-new
contribution over the entire prior family is the **scope-gate**: fire on the referenced-but-
absent set and *only* that set. Honest caveat: whether prose can make the solver actually
materialize package templates (vs h0013/h0015's 0× inertness) is unproven; if smoke shows the
three model names still absent from the committed project, this joins the inert ceiling and is
REJECTED with no iteration (CAPPED one-shot per the program).

**Distinct from prior entities.** Distinct from h0023 (a post-answer Output-Contract deliverable
clause, unscoped → f1001 bleed): this is an in-stage Implementation rule hard-scoped to the
project's own ref-graph set-difference, the explicit anti-bleed gate h0023 lacked. Distinct from
h0013/h0015 (inert enumerate/repair prose with no concrete trigger or action): this names a
concrete local trigger (dangling ref to a package-template name) and a concrete action
(materialize the set-difference). Distinct from h0009 (Exploration "package fidelity", −3
convention-bleed): this never asks the solver to mirror a package wholesale — only the
referenced-but-absent models.

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact: the added text references only local artifacts (the
project's own `ref()` graph, its `models/` directory, its `packages.yml` / `dbt_packages/`
installed package templates, its schema declarations) and names no hidden
`AUTO_*`/`solution__*`/`check_*`/verifier/`_existence`/`_equality` test, no `equality test`/`has
less columns`/`expected output seed`, no `Got N` or hidden row count, and no
`curl`/`wget`/`git clone`/web/published-solution fetch. The change touches exactly one
`## Stage: Implementation` block (inserted after the "...schema patterns." paragraph and before
"Run basic confirmation...") and leaves the leak-guard prose, Exploration, Validation, and
Finalization byte-identical. The spec differs from `@baseline` only in `experiment:` +
`solver_workflow:` (smoke may add only `benchmark.tasks`).

Target dataset (smoke, `ade-bench-` prefixed): the incomplete-deliverable failure —
`ade-bench-quickbooks001`. This rule is **generative** (it fires on any project with a
referenced-but-absent package-template model), so per gatekeeper G8 the smoke set carries a
convention-bleed canary panel of currently-passing @baseline tasks (verified `reward=1` in
`622bdedac572b479`), weighted toward the perturbable bleed surface this lever can actually fire
near:
- `ade-bench-f1001` — **the load-bearing convention-bleed sentinel** (the exact task h0023/h0009
  regressed; an f1 project with NO missing package model → the rule must stay silent on it).
- `ade-bench-quickbooks003` — perturbable same-family canary (a quickbooks project with the
  `fivetran/quickbooks` package installed that PASSES @baseline → the rule must not over-build it).
- `ade-bench-quickbooks002` — same-family passer / stable sentinel.
- `ade-bench-asana001`, `ade-bench-ana-eng001`, `ade-bench-airbnb001` — cross-family passers.

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0035-...yaml` shows only `experiment:` +
`solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md` touches only
`## Stage: Implementation` (the single scope-gated ref-graph deliverable-completion rule),
leaves Exploration/Validation/Finalization and the leak-guard prose byte-identical, and does not
reference hidden `AUTO_*`/`solution__*`/`_existence`/`_equality`/verifier tests or weaken the
leak-guard. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict is MEASURED-not-counted; the binding criterion is ZERO bleed.**
Verified by: the smoke deep-dive reads the committed project (the dispatched-ensign
`apply_patch`/file payload) and confirms whether the three model names
(`stg_quickbooks__{estimate,refund_receipt,sales_receipt}`) actually appear and build
(distance vs @baseline `Got 1`×6), AND confirms the canaries f1001/quickbooks003/quickbooks002
did NOT regress (no invented `src_*`, no over-built models). Promotion logic: a `quickbooks001`
flip is recorded as MEASURED upside (not counted toward the +5 net); **any** canary regression
(especially f1001 → the h0023/h0009 bleed signature) is an automatic NO-GO regardless of the
target flip. The flip is artifact-proven (model names present in the committed project), not
transcript chatter (the h0013/h0015 inertness lesson).

**Smoke gate:** on the target `ade-bench-quickbooks001` + the canary panel (`ade-bench-f1001`,
`ade-bench-quickbooks003`, `ade-bench-quickbooks002`, `ade-bench-asana001`,
`ade-bench-ana-eng001`, `ade-bench-airbnb001`), the variant must **not regress any canary**
(f1001 zero-bleed is mandatory) and should build the three named staging models — verified by
the committed-project artifact read (the three model files present and resolving the previously-
dangling refs), not by transcript chatter — before any promotion. CAPPED one-shot: if the
committed project still lacks the three model names, the rule joins the h0013/h0015 inert ceiling
and is REJECTED with no iteration.

## Gatekeeper review

**Recommendation: APPROVE** — one Implementation-stage hunk; leak-guard byte-identical with no
hidden-test tokens; full spec differs only in `experiment:`+`solver_workflow:`; both frozen;
scope-gate matches the claim; the only WARNs are inherent (G7 build-rule inert-risk, G8 intercom
has zero @baseline passers so no valid canary exists).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-07). Reviewed 2026-06-08T00:00:00Z.
Fork parent (resolved): `@baseline` = `runs/ade-bench-baseline/622bdedac572b479`, solver_workflow `solver_workflows/codex-ade-dbt-minimal` (matches `source:`).

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs parent is one addition hunk `55a56,90`, entirely inside `## Stage: Implementation`; one idea (scope-gated ref-graph deliverable completion); lines 1-49 + Validation/Finalization byte-identical. |
| G2 leak-guard intact | PASS | Forbidden-token grep over added block (AUTO_/solution__/_existence/_equality/check_/verifier/equality test/has less columns/expected output seed/Got N/curl/wget/git clone/git ls-remote) returns nothing; leak-guard prose (lines 9-32) byte-identical; trigger is the project's own dangling `ref()` + installed package, not hidden tests. |
| G3 spec two fields | PASS | `diff specs/baseline.yaml specs/h0035-…yaml` = lines 2 (experiment) + 11 (solver_workflow) only; `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff` full→smoke = only added `benchmark.tasks` (7 IDs, all `ade-bench-` prefixed); target `ade-bench-quickbooks001` present. |
| G5 both frozen | PASS | `…frozen.yaml` + `…smoke.frozen.yaml` both written; both carry `kind: spacedock_solver` (L4) + `runtime: codex` (L5); smoke frozen lists all 7 tasks; trials:1. |
| G6 resolver fidelity | PASS | Inserted text = exactly the claim: Implementation-stage, materialize the ref-graph set-difference from installed templates, hard scope-gate (never add unreferenced model / never treat package as source / never invent `src_*`/`source()`). Generative-but-scoped + derives names from the ref-graph generically (no hardcoded names) — not self-anchored verification. |
| G7 actionability/inert-risk | WARN | Carries a copyable shape (`stg_x__foo` skeleton) + a concrete mechanical procedure (set-difference then materialize-from-template), the asana002/h0019 form. But it still asks the solver to CREATE model files (closer to creation than a one-token cast); h0013/h0015 went inert on exactly this surface. Inert-risk is real and is the hypothesis's own honest caveat — the smoke artifact read (three model files present) is the inertness check. |
| G8 regression-canary coverage | PASS (with forced-gap WARN) | Generative (fires on any project with a referenced-but-absent installed-package staging template). Panel canaries: airbnb001, ana-eng001, asana001, f1001, quickbooks002/003 — all `@baseline` reward=1. Construct-sharing family (quickbooks) carries 2 perturbable canaries (003 + 002, both install `dbt_packages/quickbooks` so the lever can fire near them) plus f1001 as the zero-bleed sentinel (dbt_utils-only → lever must stay silent; the exact h0023/h0009 bleed surface). WARN: the **intercom** family has NO `@baseline` passer (intercom001/002/003 all reward=0), so no valid intercom canary exists — the gap is structurally forced, not a panel error. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol; single in-stage build rule. |
| G10 self-correcting false-positive | N/A | Construct-side BUILD rule (materialize referenced-but-absent models), not a check/reconcile/validate-and-fix lever; nothing is re-derived and "validated" against itself. Confirmed N/A per assignment. |

**For the captain:** APPROVE-class. The two WARNs are inherent, not fixable in place: G7 flags the build-rule inert-risk (the hypothesis already gates promotion on an artifact read, not chatter) and G8 flags the forced intercom gap (zero intercom passers exist to canary). The binding criterion is ZERO bleed — f1001 (scope-gate silence) is the load-bearing sentinel and quickbooks003/002 are the perturbable over-build canaries. A quickbooks001 flip is MEASURED upside, not counted toward the net.

## Stage Report: propose

- DONE: Fork the solver and insert ONE Implementation rule
  `solver_workflows/h0035-implementation-scope-gated-package-deliverable-set/` forked from `codex-ade-dbt-minimal`; README diff is one addition hunk `55a56,90` inside `## Stage: Implementation`, after the "...schema patterns." sentence and before "Run basic confirmation"; Exploration/Validation/Finalization + leak-guard prose byte-identical.
- DONE: Leak-guard self-check over the entire added block
  Forbidden-token grep (AUTO_/solution__/_existence/_equality/check_/verifier/equality test/has less columns/expected output seed/Got N/curl/wget/git clone/git ls-remote) returns nothing; references only local artifacts (own `ref()` graph, `models/`, `dbt_project.yml` vars, `*.yml` schema, `int_*` bodies, `packages.yml`/`dbt_packages/`); no hardcoded target names — set derived generically from the ref-graph (skeleton uses `stg_x__foo`).
- DONE: Verify the lever is sound against ground truth before freezing
  From `622bdedac572b479/ade-bench-quickbooks001__5Y3hiLq`: (a) `dbt_project.yml` `vars:` + project `int_quickbooks__{refund_receipt,sales_receipt}_{transactions,double_entry}` models (`/app/models/...`) reference `{{ ref('stg_quickbooks__{estimate,refund_receipt,sales_receipt}') }}` while those files are absent from the project's own `models/` (templates live only under `dbt_packages/quickbooks_source/models/`); `fivetran/quickbooks` declared + `dbt_packages/quickbooks` present → locally-visible dangling-ref signal. (b) f1001's `packages.yml` declares ONLY `dbt-labs/dbt_utils` (no `stg_*` templates), so NO dangling ref maps to an installed-package template → scope-gate keeps the rule SILENT on f1001 (the h0023/h0009 bleed surface). Verifier confirms the 6 fails = 3 models × (_existence+_equality), `Got 1` each.
- DONE: Full spec = baseline + exactly two fields
  `diff specs/baseline.yaml specs/h0035-…yaml` = line 2 `experiment: ade-bench-h0035-…` + line 11 `solver_workflow: ./solver_workflows/h0035-…` only; `kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved.
- DONE: Smoke spec adds only benchmark.tasks (7 tasks)
  `diff` full→smoke = only the added `benchmark.tasks` block: quickbooks001 (TARGET), f1001 (SENTINEL), quickbooks003 + quickbooks002 (perturbable same-family canaries, both install `dbt_packages/quickbooks`), asana001, ana-eng001, airbnb001. trials not raised.
- DONE: Freeze BOTH specs
  `rk freeze --allow-missing` (with `RAZORBACK_SPACEDOCK_PLUGIN_DIR` exported) wrote `…frozen.yaml` + `…smoke.frozen.yaml`; both carry `kind: spacedock_solver`, `runtime: codex`, `trials: 1`; smoke frozen lists all 7 tasks (L31-37).
- DONE: Run the gatekeeper subagent and write the review block
  `## Gatekeeper review` appended: G1-G6 PASS, G7 WARN (build-rule inert-risk), G8 PASS with forced-intercom-gap WARN (no intercom @baseline passer exists), G9 N/A (not a selector), G10 N/A (construct-side build rule, not a check/reconcile lever — confirmed); overall **APPROVE**.
- DONE: STOP at the gate
  No `rk run` launched (propose is a gate stage). Stage report appended; ready for captain gate decision.

### Summary

Authored the h0035 variant: a single scope-gated Implementation rule that materializes exactly the project's referenced-but-absent staging models (the ref-graph set-difference) from already-installed package templates, hard-gated against adding unreferenced models / treating a package as a source / inventing `src_*`. Ground truth verified both directions before freezing — quickbooks001's own `dbt_project.yml` vars + `int_quickbooks__*` models dangle-ref the three absent staging names (the locally-visible trigger), and f1001 installs only `dbt_utils` (no staging templates → scope-gate stays silent, closing the h0023/h0009 bleed surface). Both specs frozen (2-field full diff, 7-task smoke); gatekeeper APPROVE with two inherent WARNs (G7 build-rule inert-risk, G8 forced intercom gap). Stopped at the gate.

## Smoke result

**Verdict: NO-GO — INERT on target, ZERO bleed on canaries. Joins the h0013/h0015 inert ceiling → REJECTED, no iteration (CAPPED one-shot).**

Run dir: `runs/ade-bench-h0035-implementation-scope-gated-package-deliverable-set/efa1b651f71941b4` (single-trial, `trials:1`). Frozen `solver_workflow_content_hash: sha256:94ce42ec58a3b29b84cd254d5c0400edecbedec24c2b7287daeba6586a22318c`. Pre-flight `--explain` confirmed the 7-task plan, concurrency 1, `kind: spacedock_solver` / `runtime: codex` / `model: gpt-5.5` / `reasoning_effort: xhigh`.

**Clean-audit attestation (AC-2).** `rk audit … --policy strict` → `summary: {clean: 7, coverage_missing: 0, tainted: 0}`; every cell `subagent-trace-manifest.json` `captured=1` (>0). `rk score …` → `stratified_pass_at_1 = 0.8571` (6/7), `n_errored: 0`, `wilson_ci [0.487, 0.974]`, verdict `above` the 0.1875 paper constant. The score is trusted because the audit is clean.

| Task | Role | @baseline | h0035 smoke | Distance (Got N) | Rule fired? | Verdict |
|------|------|-----------|-------------|------------------|-------------|---------|
| `ade-bench-quickbooks001` | TARGET | 0 (`pass6/fail6`, `Got 1`×6) | **0** (`pass6/fail6`, `Got 1`×6) | **UNCHANGED** — 3 staging models' `_existence`+`_equality` all still FAIL | mentioned, but **0 model files built** | **INERT** |
| `ade-bench-f1001` | SENTINEL (h0023/h0009 bleed surface) | 1 (`pass6/fail0`, `src_*`×14) | **1** (`pass6/fail0`, `src_*`×14, identical set) | held | **0 mentions** (scope-gate silent) | **HOLD — zero bleed** |
| `ade-bench-quickbooks003` | perturbable same-family | 1 | **1** | held | 0 mentions, 0 new files | HOLD |
| `ade-bench-quickbooks002` | same-family passer | 1 | **1** | held | 0 mentions, 0 new files | HOLD |
| `ade-bench-asana001` | cross-family | 1 | **1** | held | 2 mentions, **0 new files** (read, did not over-build) | HOLD |
| `ade-bench-ana-eng001` | cross-family | 1 | **1** | held | 0 mentions, 0 new files | HOLD |
| `ade-bench-airbnb001` | cross-family | 1 | **1** | held | 0 mentions, 0 new files | HOLD |

**Binding criterion (ZERO bleed): PASSED.** All 6 canaries held reward=1; f1001 — the load-bearing sentinel — held at the artifact level (its 14 `src_*` files are byte-for-set identical to @baseline `622bdedac572b479`'s f1001, i.e. f1001's OWN legitimate solution, NOT the h0035 rule; `referenced-but-absent` mentioned 0× in that cell). No invented `src_*`, no over-built models anywhere the lever could fire. The exact h0023 bleed signature (`stg_models_use_src_models Got 11`) did NOT recur — that test PASSES here.

**MEASURED target (not counted toward +5 net): NO FLIP.** quickbooks001 stayed reward=0 at zero distance from @baseline — the lever was inert on the one task it was built to flip.

**This lever is an IN-STAGE Implementation rule tweak, NOT a structural/protocol workflow change** (no new/removed/reordered stage, no `## Protocol-family declaration`; the rule is a single hunk inside the existing `## Stage: Implementation` block). Per the smoke stage-def's workflow-refinement clause and the entity's own framing, the `_artifacts/WORKFLOW-REFINE.md` step does NOT apply and was intentionally not performed.

## Behavioral analysis

**Decisive committed-artifact read for quickbooks001 (the inert-vs-landed test — h0013/h0015 went 0× here).**
The README rule landed verbatim in the dispatched-ensign prompt ("Referenced-but-absent staging model rule: only if the project's own ref graph names a staging model that does not exist under `models/` …"). The ensign DID engage with it — `dbt_packages/quickbooks` is referenced 99× and `referenced-but-absent` 2× in its session (`…019ea4a6….jsonl`) — so this was NOT a pure read-failure like h0013/h0015. **But the three target staging-model names never appear as a file the solver created.** Across both the first-officer session and the ensign session, the ONLY `apply_patch … *** Add File:` op under `models/` is `models/quickbooks__general_ledger.sql` (file ops total = 1). The names `stg_quickbooks__{estimate,refund_receipt,sales_receipt}` appear ONLY inside `dbt build` STDOUT — that is the installed `quickbooks_source` package materializing its own `…_tmp` templates inside `dbt_packages/`, not project models the solver wrote. The verifier confirms the consequence: `actual_test_total=12, actual_pass=6, actual_fail=6`, all six target legs FAIL `Got 1` — **bit-identical distance to @baseline.** No flip, zero distance moved → INERT.

**Why inert (the load-bearing finding).** The solver diagnosed the task's surface failure as a *different* missing model — the project's schema declares `quickbooks__general_ledger` with no model file — created exactly that one file, and got a fully GREEN local build (`dbt build … PASS=172 WARN=0 ERROR=0`). Because the downstream `int_quickbooks__*` refs resolve against the package's own `stg_quickbooks__*` namespace at build time, the project compiles and builds CLEAN even with the three project-level staging models absent. The solver therefore saw NO local compile/build error pointing at the three models, hit its "smallest task-relevant change → green build → done" stopping condition, and never reached the set-difference the rule describes. The rule's premise — that the dangling refs are a *locally visible* trigger — does not hold against this solver's stopping behavior: the dangle is masked by the package namespace, so the only locally-observable signal (a red build) is satisfied by the one-file general_ledger fix. The honest pre-registered caveat (whether prose can make the solver materialize package templates vs h0013/h0015 inertness) resolves NEGATIVE: the rule was read and reasoned about, but did not convert to the artifact.

**f1001 zero-bleed confirmation (the h0023/h0009 sentinel).** f1001's `packages.yml` installs only `dbt-labs/dbt_utils` — no staging templates — so no dangling ref maps to an installed-package template, and the scope-gate kept the rule silent: `referenced-but-absent` mentioned 0× in the f1001 cell. The 14 `src_*` files the solver added (`models/staging/f1_dataset/src_*.sql`) are f1001's OWN expected repair (the task is "make `stg_models_use_src_models` pass") and are the identical set @baseline produces; that test PASSES (`6/6`), the exact opposite of the h0023 crash (`Got 11`, 6/6→2/6). Scope-gate verified working as designed. Cross-checked the same way on quickbooks002/003 (rule silent, 0 new files) and asana001 (rule read 2×, but 0 new files — read-without-over-build); none regressed.

**Conclusion.** The scope-gate is sound and the binding criterion (zero bleed) is met — this lever does NOT have the h0023 over-fire problem. But on the construct side it is INERT on the only target it was built to flip, for the same structural reason that sank h0013/h0015: a build-rule asking the solver to CREATE staging models from package templates does not convert to committed artifacts when the project already builds green via the package namespace. Per the entity's CAPPED one-shot clause and the smoke gate, this REJECTS with no iteration and retires the package-deliverable-completion family (h0009 −3 / h0013 inert / h0015 inert / h0023 f1001-bleed / h0035 inert — 5 attempts, 0 flips).

## Verdict

**REJECTED — smoke NO-GO, CAPPED one-shot (no iteration).** Smoke run dir
`runs/ade-bench-h0035-implementation-scope-gated-package-deliverable-set/efa1b651f71941b4`. The
falsifiable claim required the scope-gated ref-graph deliverable-completion rule to flip
`quickbooks001` by materializing the three referenced-but-absent staging models. It is **falsified
on the "inert" disjunct**: the lever did NOT convert to artifacts on the one target it could flip.

**Mechanism (precise).** The solver wrote exactly **ONE** new model
(`models/quickbooks__general_ledger.sql`) — the project's `schema.yml` declares
`quickbooks__general_ledger` with no model file, that produced a red local signal, the solver fixed
exactly it, and the local build went fully GREEN (`dbt build … PASS=172 WARN=0 ERROR=0`). The three
needed staging models (`stg_quickbooks__estimate` / `_refund_receipt` / `_sales_receipt`) **never
appeared as project files** — across both sessions the only `apply_patch *** Add File:` under
`models/` is `quickbooks__general_ledger.sql` (file ops total = 1); the three names appear ONLY in
`dbt build` STDOUT, where the installed `quickbooks_source` package materializes its own `…_tmp`
templates inside `dbt_packages/`. `quickbooks001` therefore held at the **same distance as
@baseline** (`actual_test_total=12, actual_pass=6, actual_fail=6`, all six legs `Got 1` — bit-
identical). **Distinct from h0013/h0015 TOTAL inertness:** here the rule was READ and REASONED about
(`dbt_packages/quickbooks` referenced 99×, `referenced-but-absent` 2× in the ensign session) — it
did NOT convert to artifacts because the project already built fully GREEN via the installed
package's own namespace, so the dangling-ref trigger the rule depends on was **MASKED**, and the
solver stopped at "smallest fix → green build → done" before reaching the set-difference. h0013/h0015
were pure read-failures (0× appearance, 0× engagement); h0035 is a new, sharper inertness mode — the
trigger is masked by a clean build, the *green-via-package-namespace* mode.

**POSITIVE finding — ZERO bleed (the binding criterion, PASSED).** All 6 canaries held reward=1.
`f1001` held 1.0 at the artifact level — its 14 `src_*` models are byte-for-set identical to
@baseline `622bdedac572b479`'s f1001, i.e. **f1001's OWN normal fix, NOT our rule firing**
(`referenced-but-absent` mentioned 0× in that cell because f1001 installs only `dbt-labs/dbt_utils`,
no staging templates → scope-gate stayed silent). The h0023 crash signature
(`stg_models_use_src_models Got 11`) did **NOT** recur — that test PASSES here (6/6), the exact
opposite of the h0023 over-fire (6/6→2/6). quickbooks003/002 (rule silent, 0 new files) and asana001
(rule read 2×, 0 new files — read-without-over-build) also held. The **scope-gate DESIGN is validated
as bleed-free**: the net-new contribution over the prior family (fire on the project's own
referenced-but-absent set and *only* that set) worked exactly as designed — even though the lever was
inert, it did not over-fire. Strict audit clean (`tainted: 0`, `captured > 0` on all 7 cells);
focused smoke score **6/7** (only the target failed). `@baseline` unchanged at 31/48.

**MEASURED-not-counted → @baseline unchanged.** Per the program, `quickbooks001` is MEASURED for
distance/learning, not counted toward the net. A REJECTED target flip therefore does **NOT** lower
`@baseline` — it stays **31/48**. The experiment's real result is the ZERO-bleed proof (scope-gate
works) plus the family-exhaustion knowledge gain.

**Family retirement (explicit).** The **package / incomplete-deliverable-completion family is now
EXHAUSTED**: h0009 (−3 convention-bleed) / h0013 (inert) / h0015 (inert) / h0023 (f1001 bleed) /
h0035 (inert) = **5 attempts, 0 flips**. Transferable rule: (a) a build-rule that asks the solver to
materialize installed-package templates does **not** land when the project already compiles/builds
green through the package namespace — the dangling-ref signal the rule depends on is **masked** by
the clean build; and (b) a **scope-gate keyed to the project's own ref-graph set-difference is a
VALIDATED bleed-free design** even when the lever itself is inert (it fixed the h0023 over-fire). The
next-direction decision (this family is dead; where to spend next) is a captain strategy call — no
follow-up is auto-filed (the conclude "do not reflexively file when the family is exhausted" rule).

**This lever is an IN-STAGE Implementation rule tweak, NOT a structural/protocol workflow change**
(no new/removed/reordered stage, no `## Protocol-family declaration`; the rule is a single hunk inside
the existing `## Stage: Implementation` block). The `_artifacts/WORKFLOW-REFINE.md` finalization step
therefore does NOT apply and was intentionally not performed.

## Stage Report: smoke

- DONE: Pre-flight `--explain` confirms the 7-task plan + frozen solver_workflow hash
  `RAZORBACK_SPACEDOCK_PLUGIN_DIR` exported; `--explain` showed Tasks=7, Concurrency=1, `kind: spacedock_solver`/`runtime: codex`/`model: gpt-5.5`/`reasoning_effort: xhigh`, frozen `solver_workflow_content_hash sha256:94ce42ec…22318c`.
- DONE: Launch the smoke run DETACHED (trials:1)
  `nohup uv run … rk run …smoke.frozen.yaml --runs-dir runs > /tmp/rk-h0035-smoke.log` PID 2741734; spec confirmed `trials:1`/`concurrency.trials:1`; not raised.
- DONE: POLL IN-TURN across this turn (no Monitor-then-yield)
  Polled `kill -0 $(cat $LOG.pid)` + docker ps + per-cell reward.txt in-turn until PID exited (~63 min, 7 cells sequential).
- DONE: After PID exits, strict audit + score
  `rk audit --policy strict` → `{clean:7, coverage_missing:0, tainted:0}`, every cell `captured=1`; `rk score` → `stratified_pass_at_1 0.8571` (6/7), `n_errored:0`. Both recorded in `## Smoke result`.
- DONE: DECISIVE artifact read for quickbooks001 (inert-vs-landed)
  Committed project has ONE `*** Add File:` under `models/` = `quickbooks__general_ledger.sql`; the three `stg_quickbooks__{estimate,refund_receipt,sales_receipt}` names never appear as solver-written files (only in package-internal `dbt build` STDOUT). Distance UNCHANGED vs @baseline (`pass6/fail6`, `Got 1`×6) → INERT.
- DONE: BINDING criterion — ZERO bleed vs @baseline (`622bdedac572b479`)
  All 6 canaries held reward=1. f1001 held 1.0 at the artifact level — its 14 `src_*` files are identical to @baseline's (f1001's own solution, NOT the rule; `referenced-but-absent` 0×); the h0023 `stg_models_use_src_models Got 11` signature did NOT recur (PASS, 6/6). quickbooks003/002/asana001/ana-eng001/airbnb001 also held (no over-build).
- DONE: Write `## Smoke result` (flip/distance/why table + clean-audit attestation) and `## Behavioral analysis`
  Both sections appended; flip/distance/why table + clean-audit attestation in Smoke result; committed-artifact read + f1001 zero-bleed confirmation in Behavioral analysis. WORKFLOW-REFINE.md step explicitly N/A (in-stage Implementation rule tweak, not a structural/protocol change).
- DONE: Plain-words go/no-go to the captain
  NO-GO delivered: INERT on target (3 models never built, zero distance) + ZERO bleed (f1001 + all canaries hold). CAPPED one-shot → REJECTED, no iteration.

### Summary

h0035 smoke is a clean NO-GO of the honest-negative kind. The scope-gated Implementation rule met its BINDING criterion — ZERO bleed: all 6 canaries held reward=1 and the f1001 sentinel held at the artifact level (its `src_*` build is identical to @baseline and the h0023 `Got 11` signature never recurred), so the scope-gate works and this lever does NOT have the h0023 over-fire problem. But the MEASURED target quickbooks001 did NOT flip: the committed project contains exactly one new model (`quickbooks__general_ledger.sql`) and the three target staging models never appear as solver-written files — the rule was read and reasoned about (99× `dbt_packages/quickbooks`, 2× `referenced-but-absent`) but never converted to artifacts because the project builds green via the package namespace, masking the dangling-ref trigger. Verifier distance is bit-identical to @baseline (`Got 1`×6). Inert on the only target it was built for → joins the h0013/h0015 inert ceiling → REJECTED, no iteration (CAPPED one-shot), retiring the package-deliverable-completion family (5 attempts, 0 flips). Audit clean (tainted:0, captured>0 all cells); score 6/7 trusted.

## Stage Report: conclude

- DONE: Write the ## Verdict section — REJECTED, smoke NO-GO, CAPPED one-shot
  `## Verdict` appended (before `## Stage Report: smoke`): mechanism precise — solver wrote ONE new model (`quickbooks__general_ledger.sql`), the three `stg_quickbooks__*` staging models never appeared as files; quickbooks001 held at @baseline distance (6/12 fail, `Got 1`×6); distinct from h0013/h0015 TOTAL inertness — here READ/reasoned (99×/2×) but masked by green-via-package-namespace.
- DONE: Record the POSITIVE finding — ZERO bleed
  In `## Verdict`: f1001 held 1.0 (14 `src_*` byte-identical to @baseline = f1001's own fix, rule fired 0×); h0023 `stg_models_use_src_models Got 11` did NOT recur; all 6 canaries held; scope-gate DESIGN validated bleed-free; strict audit clean (tainted:0, captured>0 all 7 cells); focused score 6/7; @baseline unchanged 31/48.
- DONE: State the family retirement explicitly — 5-for-0
  `## Verdict` records package/incomplete-deliverable-completion EXHAUSTED (h0009 −3 / h0013 inert / h0015 inert / h0023 f1001-bleed / h0035 inert) + the transferable rule (green-via-package-namespace masks the trigger; scope-gate keyed to the project's own ref-graph set-difference is a validated bleed-free design even when the lever is inert).
- DONE: Update the program doc E5 section (RESOLVED block, E1-style) + honest portfolio math
  `_proposal/oracle-problem-systematic-program.md`: added `STATUS 2026-06-08: RESOLVED — NO-GO / REJECTED (h0035)` block to E5 (one-line mechanism: green-via-package-namespace masks the dangling-ref trigger → inert; scope-gate validated bleed-free); portfolio-math E5 row updated to `{0} landed (MEASURED, REJECTED — INERT, zero bleed; family exhausted 5-for-0)`; @baseline remains 31/48.
- DONE: Update doctrine — verification-without-oracle.md + bug-type-taxonomy.md
  `verification-without-oracle.md`: new subsection "Green-via-package-namespace masks the trigger" (new named inertness mode + scope-gate as validated anti-bleed; family EXHAUSTED 5-for-0) + reach-map #6 revised down. `bug-type-taxonomy.md`: row #6 + per-task quickbooks001 row + the #6 "Read the bug type straight" note + Meta-pattern scoreboard all updated with h0035 INERT / 5-for-0 / green-via-package-namespace.
- DONE: WORKFLOW-REFINE.md finalization step does NOT apply (in-stage Implementation rule tweak)
  Stated explicitly in `## Verdict` and here: no new/removed/reordered stage and no `## Protocol-family declaration` — a single hunk inside the existing `## Stage: Implementation` block; the structural-workflow test fails, so the WORKFLOW-REFINE.md step was intentionally not performed.
- DONE: Do NOT auto-file a follow-up — family exhausted (5-for-0 meta-pattern)
  No new `h<NNNN>` entity filed; per the conclude "do not reflexively file when the family is exhausted" rule, the next-direction decision is surfaced as a captain strategy call (the FO will raise it).
- DONE: Set terminal frontmatter + archive
  Frontmatter set `verdict: REJECTED`, `completed: 2026-06-08T00:00:00Z`, `score: MEASURED-not-counted; @baseline unchanged 31/48` (status stays `conclude`); entity `git mv`'d to `hypotheses/_archive/` (entity .md only; the `solver_workflows/h0035-...` fork left in place per the h0030/h0033 archive pattern); committed.

### Summary

Concluded h0035 as a clean REJECTED of the honest-negative kind. The scope-gated Implementation rule met its BINDING criterion — ZERO bleed (all 6 canaries held reward=1, f1001 held 1.0 at the artifact level, the h0023 `Got 11` over-fire signature never recurred), so the scope-gate keyed to the project's own ref-graph set-difference is a VALIDATED bleed-free design that fixed h0023's over-fire. But the MEASURED target quickbooks001 did NOT flip: the solver wrote only `quickbooks__general_ledger.sql` and the three `stg_quickbooks__*` staging models never appeared as files — INERT for a new, sharper reason than h0013/h0015 (green-via-package-namespace: the project builds fully GREEN through the installed package's own namespace, masking the dangling-ref trigger the rule depends on). Because the experiment is MEASURED-not-counted, the REJECTED target does NOT lower @baseline (stays 31/48); the real results are the zero-bleed proof + the family-exhaustion knowledge gain. The package/incomplete-deliverable-completion family is now EXHAUSTED 5-for-0. Program doc E5 RESOLVED-block + portfolio math + both doctrine files updated; WORKFLOW-REFINE.md N/A (in-stage rule tweak); no follow-up filed (family dead → captain strategy call). Frontmatter set terminal and entity archived.
