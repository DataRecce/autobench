---
id: h0039
title: Observe-only debug lens — a NEW observe-only stage that ALWAYS writes a machine-readable reasoning record then builds EXACTLY as baseline; success = Got N UNCHANGED on all 48 (any movement = gate-strip failed = contamination = NO-GO)
status: propose
kind: hypothesis
source: _proposal/round-2-workflow-stage-program.md §4 M1 (captain-approved 2026-06-08); concept-round-2-workflow-stage-program.md item 3. The un-built WORKFLOW-REFINE Opening #2 (_artifacts/WORKFLOW-REFINE.md observe-only-lens lines). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
started: 2026-06-08T12:23:23Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

**Falsifiable claim (the single README change — a NEW observe-only `## Stage:` inserted between
Exploration and Implementation):** adding an observe-only stage that ALWAYS writes a machine-readable
reasoning record — a `Contract:` / `divergence` block to the sanctioned non-graded notes location
(`/razorback-freeze/<child>/…`, baseline README lines 30–32) — and then builds EXACTLY as baseline
(no build-to-satisfy mandate, no gate) will produce a guaranteed 48-task corpus of the solver's
at-build-time mental model **while leaving `Got N` UNCHANGED on all 48**. This is a **method
instrument**, expected to flip **{0}** tasks by construction; `Got N` UNCHANGED on all 48 is the
SUCCESS condition, and ANY movement = the gate-strip failed = the record leaked into the build =
contamination = NO-GO.

**The single solver-README change.** Add exactly one observe-only `## Stage:` header between the
existing `## Stage: Exploration` and `## Stage: Implementation` (or, if cleaner, an observe-only
sub-step inside Exploration). The stage mandates writing a machine-readable reasoning record
(`Contract:` block / `plan_review.json` / `divergence.md`) to the sanctioned non-graded notes location
via on-disk apply_patch — and then explicitly states the build proceeds EXACTLY as baseline: the record
changes no committed SQL, carries no build-to-satisfy mandate, and gates nothing. This is the exact
variant the WORKFLOW-REFINE observe-only-lens note proposed and never built.

**Independent non-oracle signal.** None is asserted against the oracle — by design. The deliverable is
the *record itself*: a 48-task map of the solver's belief, most valuable on the ~14 fired-and-failed
cells. h0017 proved the `Contract:` block legibly states the *wrong* model in the solver's own words
(asana004 wrote "one row per project_id present in int_asana__project_user"; intercom001 wrote "driven
by active conversation part rows" = the bug verbatim). This stage captures that on all 48 instead of
only the ~7 cells h0017 fired on, and it feeds the ideate stage with a per-task map of which failures
are code-contradicts-contract (a future Method-B subject) vs self-consistent-but-oracle-only (the wall).
No hidden `AUTO_*` / `solution__*` / `check_option_*` / `tests/AUTO_*` is named or read.

**Leading indicator (distance, `Got N`).** `Got N` **UNCHANGED on all 48** is the SUCCESS condition
(the contamination tripwire). Because the stage changes no committed SQL by construction, it CANNOT
false-green and CANNOT flip; any `Got N` movement means the observe-only gate-strip failed (the record
fed the build) → NO-GO. The leading indicator is therefore inverted from a flip-seeker: flatness is the
win, movement is the failure.

**Kill-path / predicted failure mode.** The known risk is G7-high inertness in the data-quality sense —
an artifact the solver is told changes nothing has weaker production pressure than h0017's build-feeding
contract; h0031 already skipped process artifacts on easy passers. Mitigate with on-disk apply_patch +
≥1 `dbt show` key-count line per model, verified by `test -f`. The kill is two-sided: (i) if any
`Got N` moves on a sampled passer, the gate-strip failed = contamination = NO-GO; (ii) if the record is
absent/empty on the fired-and-failed cells (`test -f` fails), the lens went inert and delivers no corpus
= REJECTED. The corpus records the solver's *belief*, which is demonstrably unreliable on the failers —
but that unreliability is itself the finding (it confirms the failures are self-consistent, not
self-contradictory; wall-confirming knowledge).

**Dead family it must avoid (proposal §6 map) + how it differs.** It must not become **D9
new-stage/arbitration-architecture** (mostly INERT-or-correlated) by sneaking a build-to-satisfy
mandate in: there is NO gate and NO mandate, so it cannot false-green like h0017 (D1) or arbitrate like
h0031 (D4). It is strictly weaker than every flip-seeker by design — it is an observability instrument,
not a route, contract, or selector. The only way it touches a dead family is if the gate-strip leaks
(then it becomes a contaminated D1/D9 variant) — which the `Got N`-unchanged tripwire exists to catch.

**Target datasets.** Method instrument targeting **infrastructure / all 48** — there is no flippable
target by construction. The deliverable is the 48-task reasoning corpus; the decisive smoke reads are
(a) the committed record present and non-empty on the fired-and-failed cells (e.g. `ade-bench-asana004`,
`ade-bench-intercom001`) via `test -f`, and (b) `Got N` UNCHANGED on a sampled cross-family passer panel
(the contamination tripwire).

**Honest expectation.** **{0}** flips by construction. Value: the un-built observe-only debug-lens
corpus, built at last — a guaranteed 48-task map of the solver's at-build-time mental model. Honest
caveats: (1) G7-high inertness (mitigated by on-disk apply_patch + `test -f`); (2) the corpus records
*belief*, unreliable on the failers, but that unreliability is the finding; (3) substantial overlap
with the existing §5 triage and the archived h0017 debug run `19283fb82dbd4ffd`, so the marginal yield
is bounded. This is a `trials: 1`, judge-by-artifact entity; it faces its own propose + smoke gate, and
the captain decides whether it ever runs.

**Scope.** Workflow-stage / prompt lever only; benchmark FIXED; no expanded solver access; leak-guard
intact (the stage references only local artifacts + the sanctioned non-graded notes location, and names
no hidden `AUTO_*` / `solution__*` / `check_*` / verifier test, no `equality test` / `has less columns` /
`expected output seed`, no `Got N` or row count, and no `curl`/`wget`/`git clone`/web/published-solution
fetch). The change touches exactly one new observe-only `## Stage:` header and leaves the leak-guard
prose + Exploration/Implementation/Validation/Finalization byte-identical. The full spec differs from
`@baseline` only in `experiment:` + `solver_workflow:`; the smoke spec additionally adds
`benchmark.tasks` (a cross-family sentinel/canary panel + the fired-and-failed record-presence cells).

## Acceptance criteria

**AC-1 — Exactly the README change; spec differs only in `experiment:` + `solver_workflow:`.**
Verified by: `diff ../specs/baseline.yaml ../specs/h0039-observe-only-debug-lens.yaml` shows only
`experiment:` + `solver_workflow:`; the README diff vs `codex-ade-dbt-minimal/README.md` adds exactly
one observe-only `## Stage:` header, carries NO build-to-satisfy mandate and NO gate, leaves the
leak-guard prose (lines ~1–32) and the four existing stages byte-identical, and names no hidden
`AUTO_*`/`solution__*`/`check_*`/verifier test. `agent.kind: spacedock_solver`, `runtime: codex`,
`trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Verified by: each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean
(`tainted: 0`), `captured > 0`.

**AC-3 — Verdict justified by the paired `rk runs diff` delta vs `@baseline` (computed from
`per_trial_outcomes.json`, slug-paired, 10k bootstrap) plus the absolute `stratified_pass_at_1` vs
`@baseline` 0.6458.**
For this observe-only instrument the verdict is inverted: `Got N` UNCHANGED on the sampled panel
(no flips, no regressions) is the SUCCESS condition. The smoke deep-dive MUST confirm (a) the committed
reasoning record is present and non-empty on the fired-and-failed cells via `test -f` (the lens did not
go inert) and (b) `Got N` is byte-unchanged on every sampled passer (the gate-strip held; no
contamination). ANY `Got N` movement = contamination = NO-GO; an absent/empty record on the
fired-and-failed cells = inert = REJECTED.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

## Verdict
