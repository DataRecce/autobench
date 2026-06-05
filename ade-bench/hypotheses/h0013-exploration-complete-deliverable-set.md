---
id: h0013
title: Exploration — enumerate the COMPLETE set of required deliverable models up front; a green compile is not evidence they exist
status: smoke
kind: hypothesis
source: concept-resolve-uncovered-false-greens fan-out; evidence re-audit of @baseline (622bdedac572b479, 31/48). Cluster "incomplete deliverable set / stopped at compile-green" — quickbooks001 built only quickbooks__general_ledger and never built the 3 stg_quickbooks__* staging models the oracle grades (6/12 checks failed); ana-eng007-medium also left graded models unbuilt. h0009 flagged this as a "fix-it-task completeness lever" deferred to a later hypothesis. Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-04T13:40:51Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The re-audit confirmed `quickbooks001` fails for a reason no other lever addresses: the task
is framed "the project is erroring — fix it," and the solver fixed the one visible compile
error, the full project built green (`PASS=172`), and it **stopped** — it never built the 3
`stg_quickbooks__estimate` / `…__refund_receipt` / `…__sales_receipt` staging models that the
hidden `AUTO_stg_quickbooks__*_{equality,existence}` tests actually grade (6 of 12 checks
failed on models that were never created). Its self-check validated the wrong scope
(`quickbooks__general_ledger` in isolation) and read "172 models built" — which mostly counts
pre-installed `dbt_packages/` package models — as done. `ana-eng007-medium` shows the milder
form: it validated only `fact_purchase_order` and left `dim_products` / `fact_inventory` /
`obt_product_inventory` untested and wrong.

The seed solver's Exploration prose says "inspect the task instruction … models … schema YAML"
and Implementation says "make the smallest task-relevant change," but nothing tells the solver
to enumerate the **full deliverable set** — so in a fix-it task a green compile of the existing
project reads as completion even when required models are missing entirely.

**Falsifiable claim (the single README change — Exploration stage only):** adding one
Exploration instruction — *identify the COMPLETE set of models the task requires as
deliverables before editing: read the task statement for every named or implied model, and
cross-check `schema.yml` and any installed package's staging set for models that are
declared/expected but not yet present; in "the project is erroring / fix it" tasks, a green
compile of the existing project is NOT evidence the deliverables exist — a required model may
be missing entirely; record each required deliverable and ensure every one is built* — will
flip `quickbooks001` (and help `ana-eng007-medium`) by making the solver build the full set of
graded models, raising `stratified_pass_at_1` above the `@baseline` 0.6458.

Generative/up-front (the report's surviving direction #2 — fix the understanding before the
wrong/absent model is the answer). Distinct from h0009 (reproduce a package's *conventions* in
models you author) — this is about *which* models must exist at all, including ones a green
build silently leaves missing. One idea, one stage (Exploration).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change. Leak-guard intact (task statement + local schema/package manifests
only — no public fetch, no oracle, no reference to hidden `AUTO_*`/`solution__*` tests).

Target datasets (smoke, all `ade-bench-` prefixed): the incomplete-deliverable failures —
`ade-bench-quickbooks001`, `ade-bench-ana-eng007-medium` — plus stable-`@baseline`-pass
regression sentinels `ade-bench-quickbooks002`, `ade-bench-quickbooks003`.

## Acceptance criteria

**AC-1 — Exactly the README changes; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff specs/baseline.yaml specs/h0013-exploration-complete-deliverable-set.yaml`
shows only `experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md`
touches only `## Stage: Exploration` (the single complete-deliverable rule), leaves
Implementation/Validation/Finalization and the dependency/package guardrails untouched, and
does not reference hidden `AUTO_*`/`solution__*`/verifier tests or weaken the leak-guard.
`agent.kind: spacedock_solver`, `runtime: codex` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff @baseline <variant-run-dir>` delta
(CIs, adjusted p) plus the absolute `stratified_pass_at_1` vs `@baseline` 0.6458.**
Promote only if the paired delta clears the tripwire (CI excludes a regression) on a clean
audit AND `stratified_pass_at_1 > 0.6458`.

**Smoke gate:** on the 2 targets + the 2 quickbooks sentinels, the variant must not regress
the sentinels and should flip at least `quickbooks001` to a pass before promotion to full.

## Gatekeeper review

**Recommendation: APPROVE** — single Exploration-stage idea matching the claim; leak-guard
byte-identical; specs differ only in the two allowed fields (+ smoke adds `benchmark.tasks`);
generative lever carries an airbnb/asana/f1 canary panel (intercom has no `@baseline` passer to
supply one — structurally uncoverable, documented).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-04). Reviewed 2026-06-05T06:35:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff = one insertion (lines 47-54) under `## Stage: Exploration` only; Implementation/Validation/Finalization untouched; dependency/package guardrail prose untouched. |
| G2 leak-guard intact | PASS | Lines 1-32 (leak-guard + dependency guardrails) byte-identical to parent; grep of added lines for curl/wget/clone/ls-remote/AUTO_*/solution__*/check_option/verifier/equality/expected-output/drive-to-zero/re-run/fetch = none found. |
| G3 spec two fields | PASS | `diff baseline.yaml h0013...yaml` shows only `experiment:` + `solver_workflow:`; `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff full smoke` adds only the `benchmark.tasks` block; both targets (quickbooks001, ana-eng007-medium) present; all slugs `ade-bench-` prefixed. |
| G5 both frozen | PASS | `h0013...frozen.yaml` and `...smoke.frozen.yaml` both exist; both carry `agent.kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text reproduces the Falsifiable claim verbatim in spirit (Exploration stage, "identify the COMPLETE set … a green compile is NOT evidence … record each deliverable and ensure every one is built"); generative/up-front, NOT self-anchored — names independent local signals (task statement, `schema.yml`, installed package staging set), not "re-run your own model / compare to existing code". |
| G7 actionability/inert-risk | WARN | Instruction class: abstract coverage/enumeration prose ("enumerate the complete set", "ensure every one is built") — NOT a structural SQL rewrite (no FROM/spine/join/grain), but also not a concrete mechanical substitution or worked-example skeleton. Inert-risk per the h0008/h0010 "talks but doesn't do" pattern: the solver may acknowledge the enumeration in reasoning yet still stop at compile-green. Smoke must verify the committed artifact (were the missing stg_quickbooks__* models actually built), not the chatter. |
| G8 regression-canary coverage | PASS (captain-revised panel) | Generative (fires every task during Exploration). **Captain revised the panel at the propose gate (2026-06-05):** trimmed to ONE quickbooks sentinel (dropped quickbooks003), swapped the 001 canaries for more representative passers, and **DROPPED the airbnb family entirely** — an explicit G8 override accepting that smoke is BLIND to airbnb-family regressions (observable only at full scale). Final panel: quickbooks001 + ana-eng007-medium (targets) + quickbooks002 (sentinel) + asana003 + f1007-hard (canaries). Caveat (unchanged): the intercom family has NO `@baseline` passer (intercom001/002/003 all FAIL), so a passing intercom canary is structurally impossible; documented in the smoke spec comment, not an omission. ana-eng + quickbooks are target families (covered by targets/sentinel). |

**For the captain:** APPROVE-class. One thing to weigh before smoke: G7 inert-risk — this is the abstract-prose family that has been behaviorally inert at gpt-5.5/xhigh (h0008 0/7, h0010 0/4); the smoke deep-dive must confirm the missing `stg_quickbooks__*` models were actually *built* in the committed artifact, not just discussed. One structural gap to note: intercom cannot contribute a passing canary (zero `@baseline` passers in that family), so the generative lever's intercom blast-radius will only be observable at full scale, not smoke.

## Smoke result

## Run result

## Behavioral analysis

## Verdict

## Stage Report: propose

- DONE: README diff touches ONLY `## Stage: Exploration` (adds the single complete-deliverable rule); leak-guard intact; other stages + guardrails untouched; no hidden-test references
  Forked `solver_workflows/h0013-exploration-complete-deliverable-set`; diff vs parent = one 8-line insertion (README lines 47-54) under Exploration only; leak-guard lines 1-32 byte-identical; no AUTO_*/solution__*/verifier tokens in added text.
- DONE: Generative lever's smoke spec carries a G8 regression panel (2 targets + 2 quickbooks sentinels + ≥1 passing canary per non-target family)
  `benchmark.tasks` = quickbooks001, ana-eng007-medium (targets) + quickbooks002/003 (sentinels) + airbnb001/asana001/f1001 (passing canaries). Caveat: intercom has ZERO @baseline passers (intercom001/002/003 all FAIL) — passing intercom canary structurally impossible, documented in spec comment. Both specs frozen; FULL diff vs baseline = only experiment: + solver_workflow:; smoke adds only benchmark.tasks.
- DONE: Gatekeeper review block written (per-rule PASS/WARN/FAIL table + overall APPROVE + one-line rationale)
  Recommendation APPROVE; G1-G6 PASS, G7 WARN (abstract-prose inert-risk), G8 PASS-with-caveat (intercom uncoverable).

### Summary

Forked the @baseline solver and added one Exploration-stage rule (enumerate the COMPLETE deliverable set; a green compile is not evidence the models exist). AC-1 verified: `diff specs/baseline.yaml specs/h0013-exploration-complete-deliverable-set.yaml` shows only experiment: + solver_workflow:. The lever is generative (fires every task during Exploration) so the smoke spec carries a regression panel; the one structural gap is intercom, which has no @baseline passer to supply a canary — surfaced for the captain. Gatekeeper recommends APPROVE with a G7 inert-risk WARN (this is the abstract-prose family that was inert in h0008/h0010 — the smoke deep-dive must verify the missing stg_quickbooks__* models were actually built, not just discussed). Did not run smoke per dispatch.

## Stage Report: propose (cycle 2 — captain panel revision)

- DONE: Smoke spec `benchmark.tasks` rewritten to EXACTLY the captain's 5 (quickbooks001, ana-eng007-medium, quickbooks002, asana003, f1007-hard); comment documents 2 targets + 1 quickbooks sentinel + asana/f1 canaries, the captain's airbnb DROP (deliberate G8 override — smoke blind to airbnb regressions), and intercom uncoverable
  `specs/h0013-exploration-complete-deliverable-set.smoke.yaml` — dropped quickbooks003/airbnb001/asana001/f1001, added asana003/f1007-hard; FULL spec + FULL frozen untouched (`git status` shows only the smoke pair + provenance changed).
- DONE: Smoke re-frozen — `rk freeze --allow-missing` rewrote `.smoke.frozen.yaml`; the 5 slugs verified present (lines 31-35)
  `wrote specs/h0013-...smoke.frozen.yaml`; `grep ade-bench-` on the frozen file = quickbooks001 / ana-eng007-medium / quickbooks002 / asana003 / f1007-hard. FULL frozen left untouched.
- DONE: Entity G8 row + note updated to record the captain's panel revision (airbnb dropped by captain decision, sentinel trimmed to quickbooks002); this stage-report addendum appended
  G8 row now reads "PASS (captain-revised panel)" documenting the airbnb G8 override and the trimmed sentinel.

### Summary

Applied the captain's propose-gate panel revision to the smoke spec only. Final smoke panel = quickbooks001 + ana-eng007-medium (targets), quickbooks002 (sentinel), asana003 + f1007-hard (canaries) — quickbooks003 and the entire airbnb family dropped per explicit captain G8 override (smoke accepted as blind to airbnb-family regressions, observable only at full). Re-froze the smoke spec; the 5 slugs are present in `.smoke.frozen.yaml`. FULL spec, FULL frozen spec, and the solver README were left untouched; smoke still differs from full only in `benchmark.tasks`. Did not run smoke per dispatch.
