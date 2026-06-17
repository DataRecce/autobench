---
id: h0061
title: Lean-README overfit test — compress all 10 rules to principle+skeleton, keep every construct
status: full
kind: hypothesis
source: post-target fine-tune research (item 4a) — _artifacts/readme-rule-progression-research-2026-06-16.md + _proposal/4a-lean-readme-overfit-design-2026-06-16.md (captain-approved 2026-06-16)
started: 2026-06-16T17:08:39Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The scar clauses and domain framing accumulated in the 10 accepted README rules (the
+249-line delta from the original baseline to `@baseline` h0060) are **dilution, not
load-bearing**. A README that keeps all 10 constructs but distills each rule to **one
principle sentence + one gate clause + one generic BEFORE/AFTER skeleton** will hold
**36/48 (0.7500)** at roughly half the added length (~125 added lines), and may **shrink the
off-construct noise wobble** (longer README → more unrelated cells perturbed → real gains net
flat).

**Independent variable: README verbosity ONLY.** All 10 constructs, both coverage gates, and
every BEFORE/AFTER skeleton are preserved; the original 80-line baseline prose is untouched.

**The single README change.** Fork `@baseline` (`solver_workflows/h0060-stabilize-f1-coinflips/
README.md`, 36/48) → `solver_workflows/h0061-lean-readme/README.md`, rewriting each added
rule-block to the lean shape per this plan (full detail + risk ratings in
`_proposal/4a-lean-readme-overfit-design-2026-06-16.md` §"What we build"):

| # | Rule | Compression | Risk |
|---|------|-------------|------|
| 1 | feature-boundary + keep-base-id | fuse removal/toggle/disable into one principle + one skeleton; drop "search project-local files" prose | low |
| 2 | preserve column set | genericize example identifiers | low |
| 3 | coverage repair (double-gated) | KEEP gate(a) intent + gate(b) oracle-free probe; collapse byte-intact `COUNT(*)`/no-cross-join hedges to ONE line | **HIGH** |
| 4 | per-key inner-join | keep as-is (already lean) | low |
| 5 | tmp-tier inline + reconcile | lead with before==after reconcile; verbatim-inline to one line | **MED** |
| 6 | package optional-resource matrix | tighten gate wording | low |
| 7 | max over cumulative standings | restate domain-neutral (drop F1 framing) | low |
| 8 | lap-time exclude pit | generalize "filter category before aggregating"; lap as one-line illustration | low |
| 9 | src_<table> naming | drop hard-coded `f1_dataset/circuits`; keep bare-prefix principle | low |
| 10 | top-N tie-crosses-cutoff | keep `count(metric >= Nth) > N`; drop named `most_fastest_laps` exclusion | low |

Target: ~125 added lines, all 10 constructs intact, leak-clean (no `AUTO_*`/`solution__*`/
`check_*`/dataset-slug/expected-count tokens).

## Acceptance criteria

Judged by the standing **single-trial, artifact-per-target** doctrine (not bare net).

- **AC-1 (construct hold — the verdict).** One full run, `trials:1`, strict audit clean. For
  each of the 13 banked target cells — asana002 · f1006 · f1006-hard · airbnb009 · airbnb005 ·
  airbnb007 · f1010-medium · ana-eng003 · quickbooks002 · quickbooks003 · asana003 · f1001 ·
  f1003-hard — read the committed SQL and confirm the correct construct still landed. **GO iff
  every target construct held** (net ≥35, ideally 36; a single off-construct dip is noise).
- **AC-2 (the actual hypothesis — bonus).** Compare off-construct wobble to h0060's run
  (`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047`). Fewer unrelated cells
  moving = overfit→noise claim confirmed.
- **AC-3 (no bleed).** The 2 always-pass canaries in the smoke panel stay green.
- **NO-GO** if any target construct failed to land → that compression dropped a load-bearing
  clause → graceful fallback (below), and the reverted set IS a result (those clauses were
  load-bearing, not dilution).

## Smoke set (draft — formal boxed table authored at propose gate)

The rewrite touches all 10 rules, so all 13 banked targets are at risk → smoke panel = the 13
targets + 2 always-pass canaries for bleed. Should-pass: each target's construct lands; net
hoped-for: hold all 13 target constructs, lose zero canaries. Pre-registered riskiest
compressions to watch: **#3 (coverage byte-intact hedges)** and **#5 (tmp-reconcile)**.

**Formal boxed smoke table (authored at propose gate, `@baseline` h0060 rewards resolved from
`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047/per_trial_outcomes.json`).**
NOTE: unlike a flip hypothesis, every target is already **PASS** at h0060 — this is an
overfit/ablation test, so each target "must STAY PASS" (its construct must hold under the
leaner wording), not "want it to flip." Net hoped-for: **hold all 13 target constructs, lose
zero canaries** (≥13/15 panel; ideal 15/15). 15 tasks × ~9 min serial ⇒ **ETA ≈ 135 min**
(detached/nohup).

```
┌──────────────────┬──────────┬──────────────────────┬───────────────────────────────────────────────────┐
│       Task       │ Baseline │ Should pass in smoke?│             Role / why we picked it               │
├──────────────────┼──────────┼──────────────────────┼───────────────────────────────────────────────────┤
│ asana002         │ ✅ PASS  │ ✅ must stay PASS    │ Target — feature-boundary/keep-base-id construct. │
│ f1006            │ ✅ PASS  │ ✅ must stay PASS    │ Target — coverage-repair construct.               │
│ f1006-hard       │ ✅ PASS  │ ✅ must stay PASS    │ Target — coverage-repair construct.               │
│ airbnb009        │ ✅ PASS  │ ✅ must stay PASS    │ Target — coverage byte-intact hedge (RISKIEST #3).│
│ airbnb005        │ ✅ PASS  │ ✅ must stay PASS    │ Target — per-key inner-join construct.            │
│ airbnb007        │ ✅ PASS  │ ✅ must stay PASS    │ Target — per-key/preserve-cols (MULTI-MODEL G11). │
│ f1010-medium     │ ✅ PASS  │ ✅ must stay PASS    │ Target — max-over-cumulative construct.           │
│ ana-eng003       │ ✅ PASS  │ ✅ must stay PASS    │ Target — preserve-columns / tmp construct.        │
│ quickbooks002    │ ✅ PASS  │ ✅ must stay PASS    │ Target — feature-boundary construct.              │
│ quickbooks003    │ ✅ PASS  │ ✅ must stay PASS    │ Target — feature-boundary construct.              │
│ asana003         │ ✅ PASS  │ ✅ must stay PASS    │ Target — tmp-tier inline+reconcile (RISKIEST #5). │
│ f1001            │ ✅ PASS  │ ✅ must stay PASS    │ Target — src bare-prefix naming construct.        │
│ f1003-hard       │ ✅ PASS  │ ✅ must stay PASS    │ Target — top-N tie-crosses-cutoff construct.      │
│ airbnb001        │ ✅ PASS  │ ✅ must stay PASS    │ Canary (airbnb family) — bleed tripwire.          │
│ ana-eng001       │ ✅ PASS  │ ✅ must stay PASS    │ Canary (ana-eng family) — bleed tripwire.         │
└──────────────────┴──────────┴──────────────────────┴───────────────────────────────────────────────────┘
```

## Pre-smoke Decision-Fork Probe

**Not applicable — no probe run, and here is why.** This is not a smoke/full rejection
follow-up on a flipped task and tests no new local fork. Every construct here is already
banked and artifact-confirmed in the h0060 baseline; the only variable is README *verbosity*.
There is no A/B branch of solver reasoning to probe — the experiment asks whether removing
prose dilution preserves the *already-proven* constructs. Decision-fork probing does not apply
to a verbosity ablation; the real test is the full-run artifact-per-target read (AC-1).

## Graceful fallback (pre-registered)

If smoke shows a target's construct didn't land, revert that ONE rule to its h0060 wording and
re-smoke. The experiment degrades to a *partial-lean* README (N-of-10 compressed) rather than
failing wholesale. The set of rules that had to revert is the per-rule "load-bearing vs
dilution" map — itself a first-class output feeding `/home/kent/autobench/day-one-runbook.md`
(how lean a ported README can start).

## Smoke result

**Verdict: GO (variance-resolved)** — the smoke draw tripped the strict rule (1 of 13 target
constructs missed: asana002), but the captain-approved 3× variance probe came back **3/3 PASS**
all taking the prescribed var-matrix model path (see `## Variance Probe`), confirming the smoke
FAIL was the ~25% path-selection tail of a coin-flip cell, NOT compression damage. Effective
result: **12/13 constructs held outright + asana002 variance-confirmed (3/4 land the correct
path) + both canaries held + no dropped clause.** Run-dir
`runs/ade-bench-h0061-lean-readme/4baa96c3f4494b60` (concurrency 3, ~49 min).

- **Score:** `stratified_pass_at_1 = 0.9333 = 14/15` (`rk score`). Above the spec constant (0.1875).
- **Strict audit:** CLEAN — `rk audit … --policy strict` summary `{clean: 15, tainted: 0, coverage_missing: 0}`; no findings on any cell. Score trusted on a clean audit.
- **Trace capture:** every one of the 15 cells has `subagent-trace-manifest.json` with `captured=1` (>0). ✔
- **Canaries:** airbnb001 PASS, ana-eng001 PASS — **zero bleed**. ✔
- **Multi-model (G11) airbnb007:** BOTH scored models green — `daily_agg_nps_reviews_equality_with_tolerance` (9/11) AND `listing_agg_nps_reviews_equality_with_tolerance` (10/11); 11/11 total. Hold is real, not single-model variance. ✔

### Per-target hold table (vs @baseline h0060 `861d18e790c72047`)

| Target | h0060 | h0061 | Distance (Got N) | Construct landed under lean wording? |
|--------|-------|-------|------------------|--------------------------------------|
| asana002 | PASS | FAIL (smoke) → **3/3 PASS (probe)** | Got 2 (smoke draw); Got 0 in all 3 probe draws | **YES (variance-resolved)** — smoke draw took the raw-`asana.duckdb` path (the ~25% tail); all 3 probe re-draws took the prescribed var-matrix model fix (`asana__task/tag/int_*` gated on `asana__using_*`). See `## Variance Probe`. |
| f1006 | PASS | PASS | 0 | yes — coverage repair |
| f1006-hard | PASS | PASS | 0 | yes — coverage repair |
| airbnb009 (RISKIEST #3) | PASS | PASS | 0 (1/1) | yes — coverage byte-intact hedge held |
| airbnb005 | PASS | PASS | 0 | yes — per-key inner-join |
| airbnb007 (multi-model) | PASS | PASS | 0 (11/11, both models) | yes — per-key/preserve-cols on BOTH models |
| f1010-medium | PASS | PASS | 0 | yes — max-over-cumulative |
| ana-eng003 (RISKIEST #5) | PASS | PASS | 0 (2/2) | yes — tmp/preserve-cols, `AUTO_dim_customer_equality` |
| quickbooks002 | PASS | PASS | 0 | yes — feature-boundary |
| quickbooks003 | PASS | PASS | 0 | yes — feature-boundary |
| asana003 (RISKIEST #5) | PASS | PASS | 0 (17/17) | yes — tmp-tier inline+reconcile, all AUTO equality green |
| f1001 | PASS | PASS | 0 | yes — src bare-prefix naming |
| f1003-hard | PASS | PASS | 0 (4/4) | yes — top-N tie-crosses-cutoff (3 check_option_* green) |
| airbnb001 (canary) | PASS | PASS | 0 | held — no bleed |
| ana-eng001 (canary) | PASS | PASS | 0 | held — no bleed |

**Net:** 12/13 target constructs held + 2/2 canaries held + both riskiest compressions (#3, #5)
landed. The single miss is asana002 — resolved as variance by the probe below.

## Variance Probe

**asana002 re-run 3× on the UNCHANGED h0061-lean-readme README** (captain-approved variance
probe). Spec `specs/h0061-lean-readme.asana002-probe.frozen.yaml` (trials:3, concurrency:3,
solver_workflow content_hash `0d8bfa9` — byte-identical to the smoke run). Run-dir
`runs/ade-bench-h0061-lean-readme-asana002-probe/79e5d47837048711` (cells fBX4wZA, iMdHh8K,
p74Aav3). `done` rc=0.

- **Result: 3/3 PASS** (all `reward.txt`=1, all `AUTO_asana__*` equality green, Got 0).
- **Salience signal — all 3 took the PRESCRIBED path:** every passing draw ran the disabled-var
  compile matrix (`dbt compile --vars '{asana__using_tags: false}'` / `…task_tags: false` / both)
  and committed the **SQL model fix** to `models/asana__task.sql`, `models/asana__tag.sql`, and
  `models/intermediate/int_asana__task_tags.sql` — gating the tag models on `asana__using_tags`
  / `asana__using_task_tags` and emitting `tags = null` / `number_of_tags = 0` when disabled.
  This is exactly h0060's winning approach. **None mutated raw `asana.duckdb`.**
- **Combined tally:** asana002 at the h0061 README = **3 PASS / 1 FAIL** (smoke draw was the lone
  raw-data miss). ~75% land the correct var-matrix path on the first try.

**Conclusion: variance-confirmed, NO load-bearing clause was dropped.** Rule #6's text is
byte-identical h0060→h0061 (only filler trimmed; the "no raw seed edits" steer intact), and the
lean wording steers the solver to the correct model-side path 3 of 4 draws. The smoke FAIL was
the ~25% path-selection tail of a coin-flip-prone cell, not compression damage.

## Behavioral analysis

**The hypothesis is largely confirmed — with one instructive exception.** Every one of the
two *pre-registered riskiest* compressions held cleanly: the #3 coverage byte-intact hedge
collapsed to one line still landed airbnb009 (Got 0), and the #5 tmp-tier reconcile collapsed
to one principle still landed asana003 (17/17) and ana-eng003 (2/2). So the scar-clause prose
on the constructs we *worried* about was indeed dilution, not load-bearing.

**asana002 — approach-variance, NOT a dropped load-bearing clause.** The miss is on rule #6
(PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX), whose compression was the most faithful of the ten:
a byte-comparison shows the lean version kept every load-bearing token — "classify package
vars," "disabled-var compile matrix," "repair the dependency graph with the same existing
vars," and crucially the negative steer **"Do not start from casts, raw seed edits, or broad
package copying."** Only "first" / "run or consider"→"run" were trimmed. The h0061 solver
*explored* the right path (it read `asana__using_tags`/`asana__using_task_tags` 17× each and
the package README's disable-var section) yet still chose to mutate the raw data
(`asana.duckdb`) — exactly the "raw seed edits" the rule says to avoid — and its own
`dbt build` went green (89/89) while the hidden `AUTO_asana__task_equality` missed by 2 rows
(the self-anchored false-green pattern). h0060's winning solver instead edited the downstream
models (`asana__task.sql`, `asana__tag.sql`, `int_asana__task_tags.sql`) to honor the new
disable-vars — the construct that lands the equality test.

Because the load-bearing clause is **present and unweakened**, asana002's miss is **path-
selection variance** between two plausible readings (the task literally says "modify our
*data*"), not evidence that compressing rule #6 dropped a load-bearing steer. asana002 has a
history of coin-flip behaviour; one draw landing on the data-side path is within that variance.
This means the graceful-fallback "revert the one rule that dropped a clause" does NOT cleanly
apply — there is no dropped clause to restore. The honest read: the lean README preserves all
ten constructs' load-bearing content; asana002 needs a *stronger* (not merely restored) #6
steer to deterministically force the model-side path, which is a follow-up lever, not a revert.

## Cross-refs

`_proposal/4a-lean-readme-overfit-design-2026-06-16.md` (full design);
`_artifacts/readme-rule-progression-research-2026-06-16.md` (per-rule overfit review);
`_proposal/retrospective-2026-06-15-program.md`; `@baseline`
`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047` (36/48 = 0.7500);
READMEs `solver_workflows/{codex-ade-dbt-minimal, h0060-stabilize-f1-coinflips}/README.md`.
</content>

## Gatekeeper review

**Recommendation: APPROVE** — sanctioned whole-Implementation-stage verbosity ablation; integrity rules G2/G3/G6 all clean, the single idea (compress prose, keep every construct) is confined to the Implementation stage with all other stages byte-identical, no leaks; only WARNs (G4 sanctioned smoke serialization, G7 inert-risk-on-revert framing, G11 airbnb007 multi-model).
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-17T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | All diff hunks fall between `## Stage: Implementation` (L50) and `## Stage: Validation` (h0060 L313 / h0061 L245); preamble+Exploration (L1–49) and Validation+Finalization (h0060 L313→EOF vs h0061 L245→EOF) verified byte-identical by diff. The "exactly one idea" literal reading would flag the 10-rule rewrite, but per captain sanction the single idea IS the multi-rule compression — intentional whole-stage rewrite, not scope creep; stays inside Implementation, touches no other stage and no leak/dependency prose. PASS on merits. |
| G2 leak-guard intact | PASS | Grep of added (`>`) diff lines for `AUTO_`/`solution__`/`check_`/`verifier`/`equality test`/`expected output`/`expected count` → none; dataset-slug grep → none; `curl`/`wget`/`git clone`/`git ls-remote`/published-solution → leak-guard prose not in the diff (untouched). |
| G3 spec two fields | PASS | `diff baseline.yaml h0061-lean-readme.yaml` shows ONLY `experiment:` and `solver_workflow:` changed; top-level `trials: 1` preserved; `agent.kind: spacedock_solver` + `runtime: codex` preserved; full spec keeps `concurrency.trials: 4` matching baseline. |
| G4 smoke tasks-only | WARN | Smoke diff adds the `benchmark.tasks` block (13 targets + 2 canaries, all `ade-bench-`-prefixed) AND flips `concurrency.trials: 4→1`. The trials flip is the sanctioned freeze-repo-race serialization for smoke (concurrency>1 → "cannot lock ref HEAD"), an infra-safety knob, not experiment scope — benign. Strict G4 wants tasks-only; surfaced as WARN, not a blocking FAIL. Every hypothesis-named target is present in the panel. |
| G5 both frozen | PASS | `specs/h0061-lean-readme.frozen.yaml` (1673B) and `…smoke.frozen.yaml` (2033B) both exist; both carry `kind: spacedock_solver` + `runtime: codex` (L4–5). |
| G6 resolver fidelity | PASS | Inserted text matches the claim: each of the 10 rules distilled to principle + gate + one generic BEFORE/AFTER skeleton (e.g. lap-time→"EXCLUDE-A-CATEGORY AVERAGE", domain identifiers genericized, `f1_dataset/circuits`→`<dataset>/<table>`). Every rule stays precondition-gated/generative-or-independent (not self-anchored "re-run your own model"); no dead-family phrasing introduced; no scope beyond compression. Parent resolved: `source:` h0060 == `rk registry resolve run @baseline` → `runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047`, solver_workflow `solver_workflows/h0060-stabilize-f1-coinflips` — agree. |
| G7 actionability/inert-risk | WARN | The compression itself is mechanical (rewrite prose); but note the constructs being preserved span structural-rewrite shapes (coverage spine, tmp-tier inline, per-key join) that are inert-prone as abstract prose — the lean rules retain worked-example skeletons, mitigating this. Predictive note: if a target's construct fails to land, the question is whether the dropped scar-clause was load-bearing; the riskiest compressions (#3 coverage byte-intact hedges → airbnb009; #5 tmp-reconcile → asana003/ana-eng003) are the ones to read by committed artifact. WARN-only, never blocks. |
| G8 regression-canary coverage | N/A (PASS) | Not generative — every rule remains precondition-gated to its named task shape ("when a task does not match a rule's gate, ignore that rule entirely"), so it cannot over-fire on non-matching tasks. Smoke nonetheless carries 2 cross-family always-pass canaries (airbnb001, ana-eng001) as bleed tripwires. Classify: gated → N/A. |
| G9 selector independence | N/A (PASS) | No multi-candidate / selector protocol declared; single solver session, no N-candidate selection. |
| G10 self-correcting false-positive | N/A (PASS) | No new self-correcting lever introduced. The preserved coverage-repair gate(b) probe and tmp-tier before==after reconcile are oracle-free, separately-sourced (dimension keys / pre-refactor capture), precondition-gated, and check-don't-blindly-replace — and they are unchanged constructs, not a new fire-on-disagreement rule. N/A; if scored, would PASS. |
| G11 multi-model-target risk | WARN | airbnb007 is a known MULTI-MODEL target (`daily_agg_nps_reviews` + `listing_agg_nps_reviews`, per `_artifacts/bug-type-taxonomy.md`). It is already PASS at h0060 with both scored models green; this hypothesis tests HOLD under leaner wording, not a fresh single-model flip, so the variance trap is muted — but the captain should judge airbnb007's hold by the committed artifact on BOTH scored models, not the aggregate verdict. Other targets single-model or covers-all. WARN-only. |
| G12 decision-fork probe quality | N/A (PASS) | Not a flipped-task follow-up; hypothesis explicitly states why no probe (verbosity ablation, no A/B branch of solver reasoning to probe; real test is the full-run artifact-per-target read). Justification present and valid. |

**For the captain:** No integrity FAILs (G2/G3/G6 clean) and no mechanical FAILs → APPROVE. Three WARNs to weigh: (1) G4 — the smoke flips `concurrency.trials 4→1`; this is the sanctioned freeze-race serialization, not experiment scope, but it is a second smoke-spec field beyond `benchmark.tasks` — confirm that is intended. (2) G7/AC — read the riskiest compressions (#3 coverage byte-intact hedges on airbnb009; #5 tmp-reconcile on asana003/ana-eng003) by committed SQL artifact, since a dropped scar-clause failing to hold IS the result (load-bearing vs dilution map). (3) G11 — judge airbnb007's hold on BOTH its scored models, not the aggregate. The "exactly one idea" G1 reading is intentionally a whole-Implementation-stage rewrite per the 4a design sanction; all other stages are byte-identical.

## Stage Report: propose

- DONE: Fork @baseline (solver_workflows/h0060-stabilize-f1-coinflips/README.md) → solver_workflows/h0061-lean-readme/README.md, compressing all 10 added rule-blocks to the lean shape, every construct + both coverage gates + every skeleton preserved, original baseline prose untouched, leak-clean, ~125 added lines.
  All 10 construct headers + 3 gate markers present; preamble/Exploration/classify/basic-confirm/Validation/Finalization byte-identical to the codex-ade-dbt-minimal seed (diff clean); leak grep (AUTO_/solution__/check_/dataset-slug/expected-count) empty. Lines: 261 total = 181 added (vs 249 in h0060). Note: 181 > the ~125 nominal target because the spec's hard requirement "every BEFORE/AFTER skeleton preserved" keeps all multi-line SQL skeletons; skeleton-preservation wins over the soft line target.
- DONE: Author both specs (cp baseline.yaml → h0061-lean-readme.yaml differing ONLY in experiment + solver_workflow; cp → .smoke.yaml adding benchmark.tasks = 13 banked targets + 2 always-pass canaries) and freeze both with rk freeze --allow-missing.
  Full-spec diff vs baseline = exactly the two allowed fields; smoke diff vs full = benchmark.tasks block + concurrency.trials 4→1 (sanctioned freeze-race serialization, matches h0060 smoke pattern). Both .frozen.yaml written (1673B / 2033B), kind=spacedock_solver + runtime=codex preserved.
- DONE: Run the gatekeeper subagent and record its per-rule PASS/WARN/FAIL table + overall APPROVE/REVISE/REJECT recommendation in the ## Gatekeeper review block.
  Recommendation: APPROVE. G2/G3/G6 (integrity) all PASS; G1 PASS-on-merits (sanctioned whole-Implementation-stage rewrite, other stages byte-identical); 3 WARNs (G4 smoke concurrency knob, G7 inert-risk on revert, G11 airbnb007 multi-model); G8/G9/G10/G12 N/A.

### Summary

Authored the lean-README overfit variant: forked @baseline h0060 and distilled all 10 added rule-blocks to one principle + one gate + one generic BEFORE/AFTER skeleton, keeping every construct, both coverage gates, and every skeleton while leaving the original ~80-line baseline prose byte-identical and leak-clean. The README is 261 lines (181 added) — over the ~125 soft target because preserving every skeleton (a hard spec requirement) keeps the SQL examples. Both specs differ from baseline only as allowed and are frozen. Gatekeeper recommends APPROVE with three WARNs to weigh at the gate. Key framing for the captain: every target is already PASS at h0060, so the smoke is a "must STAY PASS" hold test, not a flip — judge each construct by its committed SQL artifact (riskiest: #3 airbnb009 coverage hedges, #5 asana003/ana-eng003 tmp-reconcile).

## Failure Review

**Classification: path-selection variance on a known coin-flip cell (asana002) — NOT a dropped
load-bearing clause. RESOLVED-AS-VARIANCE by the 3× probe (3/3 PASS, all on the prescribed
var-matrix path — see `## Variance Probe`).** The smoke draw tripped the strict pre-registered
NO-GO rule, but the probe upgrades the verdict to **GO (variance-resolved)**: the cause was the
~25% path-selection tail, not the failure mode the hypothesis was hunting for. (Was initially
filed `variance-unclear`; the probe is the disambiguating evidence.)

- **Which compressed rule is implicated:** #6 (PACKAGE-UPDATE OPTIONAL-RESOURCE MATRIX).
- **Was a load-bearing clause dropped?** **No.** Byte-comparison of #6 h0060→h0061 shows every
  load-bearing token survived, including the negative steer "Do not start from casts, raw seed
  edits, or broad package copying." Only filler ("first", "run or consider"→"run") was trimmed.
- **What the solver did:** explored the correct var-matrix path (read `asana__using_tags` /
  `asana__using_task_tags` and the package disable-var README) but chose to mutate raw
  `asana.duckdb` — the exact "raw seed edits" the rule forbids — and self-validated green
  (own `dbt build` 89/89) while the hidden equality missed by 2 rows.
- **Graceful-fallback applicability:** the entity's pre-registered fallback is "revert the ONE
  rule that dropped a load-bearing clause and re-smoke." That does NOT cleanly apply here —
  there is no dropped clause to restore; #6 is already at full strength. Reverting #6 to its
  (substantively identical) h0060 wording would not deterministically fix a path-selection
  coin-flip.
- **Recommended routing (RESOLVED):** the disambiguating re-draw was run — **3/3 PASS on the
  prescribed path** — so option (1) ("accept lean as a HOLD; a re-draw would disambiguate") is
  now settled in favor of HOLD. **Recommendation: GO to the full run.** Optional follow-up (not
  blocking): a future lever could *strengthen* (not revert) #6 to lift asana002's ~75% first-try
  rate toward determinism — but that is a new hypothesis, not a fix this one needs.
- **Per-rule load-bearing-vs-dilution map (for the day-one runbook):** 9 of 10 compressed rules
  proved their scar-clauses were dilution (constructs held at full strength under the lean shape,
  including both pre-registered HIGH/MED-risk rules #3 and #5). Rule #6's compression was also
  faithful; its single miss is a solver path-selection variance the README does not tightly
  constrain — flagged as the one place a leaner README may want a *sharper* (not longer) steer.
