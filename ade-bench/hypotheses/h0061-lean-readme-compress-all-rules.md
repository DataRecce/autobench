---
id: h0061
title: Lean-README overfit test — compress all 10 rules to principle+skeleton, keep every construct
status: hypothesis
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

## Cross-refs

`_proposal/4a-lean-readme-overfit-design-2026-06-16.md` (full design);
`_artifacts/readme-rule-progression-research-2026-06-16.md` (per-rule overfit review);
`_proposal/retrospective-2026-06-15-program.md`; `@baseline`
`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047` (36/48 = 0.7500);
READMEs `solver_workflows/{codex-ade-dbt-minimal, h0060-stabilize-f1-coinflips}/README.md`.
</content>
