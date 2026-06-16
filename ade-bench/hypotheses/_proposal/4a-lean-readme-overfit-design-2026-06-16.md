# Design — Item 4a: lean-README overfit test (next hypothesis, ~h0061)

Date: 2026-06-16 · Status: design approved (captain ok 2026-06-16), pre-propose
Source: post-target fine-tune research (`_artifacts/readme-rule-progression-research-2026-06-16.md`)

## Hypothesis

The scar clauses and domain framing accumulated in the 10 accepted README rules are
**dilution, not load-bearing**. A README that keeps all 10 constructs but distills each to
**one principle sentence + one gate clause + one generic BEFORE/AFTER skeleton** will hold
**36/48 (0.7500)** at roughly half the added length (~125 added lines vs the current 249),
and may **shrink the off-construct noise wobble** (the overfit→noise mechanism: a longer
README perturbs more unrelated cells, which is what keeps real gains netting flat).

Independent variable: README verbosity ONLY. All 10 constructs, both gates, and every
BEFORE/AFTER skeleton are preserved. The original 80-line baseline prose is left untouched
(it is not the variable).

## What we build

Fork the live `@baseline` README (`solver_workflows/h0060-stabilize-f1-coinflips/README.md`,
36/48) into `solver_workflows/h0061-lean-readme/README.md`. Rewrite each added rule-block to
the fixed lean shape. Per-rule compression plan:

| # | Rule | Compression action | Risk |
|---|------|---------------------|------|
| 1 | feature-boundary + keep-base-id | Fuse the removal/toggle/disable triple-paragraph into one principle + keep the one skeleton; drop the "search project-local files" prose. | low |
| 2 | preserve column set | Keep; genericize `customer_*` example identifiers. | low |
| 3 | coverage repair (double-gated) | KEEP gate(a) intent + gate(b) oracle-free probe (both transferable). Collapse the byte-intact `COUNT(*)`/no-cross-join hedges to ONE line: "make the minimal subtractive edit; do not rewrite aggregates or add joins while repairing coverage." | **HIGH** — riskiest; the hedges may be load-bearing for airbnb009. |
| 4 | per-key inner-join | Keep as-is (already the model lean rule). | low |
| 5 | tmp-tier inline + reconcile | Lead with the before==after reconcile principle; reduce the verbatim-inline instruction to one line. | **MED** — verify reconcile clause survives. |
| 6 | package optional-resource matrix | Keep (prose-only, already short); tighten gate wording. | low |
| 7 | max over cumulative standings | Restate domain-neutral: "cumulative-snapshot totals aggregate with `max()` at entity grain; don't switch to latest-row/rank/window unless local evidence proves max wrong." | low |
| 8 | lap-time exclude pit | Generalize: "when an average must exclude a row category, filter before aggregating; don't keep-and-subtract." Lap example as one-line illustration. | low |
| 9 | src_<table> naming | Drop hard-coded `f1_dataset/circuits`; keep the bare-prefix principle + generic skeleton. | low |
| 10 | top-N tie-crosses-cutoff | Keep the `count(metric >= Nth) > N` test; drop the named `most_fastest_laps` exclusion → generic "exclude any model the prompt already classifies." | low |

Target: ~125 added lines, all 10 constructs intact, leak-clean (no `AUTO_*`/`solution__*`/
`check_*`/dataset-slug/expected-count tokens).

## How we judge — artifact-per-target (the standing single-trial doctrine)

One full run, `trials:1`, strict audit clean. Then for each of the **13 banked target cells**
read the committed SQL and confirm the correct construct still landed:

> asana002 · f1006 · f1006-hard · airbnb009 · airbnb005 · airbnb007 · f1010-medium ·
> ana-eng003 · quickbooks002 · quickbooks003 · asana003 · f1001 · f1003-hard

- **GO** if every target construct held (net ≥35, ideally 36). A single off-construct dip is
  noise, not a regression (judge by construct-touch, not the bare number).
- **Bonus signal** (the actual hypothesis): compare the off-construct wobble to h0060's run —
  if fewer unrelated cells move, the overfit→noise claim is confirmed.
- **NO-GO** if any target construct failed to land → the compression dropped a load-bearing
  clause (see fallback).

## Smoke first (propose-gate)

Because the rewrite touches all 10 rules, all 13 targets are at risk, so the smoke panel =
the 13 banked targets + 2 always-pass canaries for bleed detection. Should-pass = each
target's construct lands; canaries must stay green. (Formal boxed smoke table per
`hypotheses/README.md` propose-stage format to be filled at the propose gate.)

## Kill / graceful fallback

Pre-registered riskiest compressions: **#3 (coverage byte-intact hedges)** and **#5
(tmp-reconcile)**. If smoke shows a target's construct didn't land, revert that ONE rule to
its h0060 wording and re-smoke. The experiment therefore degrades to a *partial-lean* README
(N-of-10 rules compressed) rather than failing wholesale — and the set of rules that had to
revert IS the result: those clauses were load-bearing, not dilution.

## Output / value

- **If GO:** a leaner `@baseline` at the same 36/48; the overfit hypothesis proven; and a
  per-rule "load-bearing vs dilution" map.
- **Feeds the day-one runbook:** how lean a *ported* README can start on a new benchmark
  (the 6.5 transferable data-modeling rules in their distilled form).
- **De-risks future composition:** a shorter baseline perturbs fewer off-construct cells, so
  subsequent hypotheses fork from a quieter, more reproducible baseline.

## Out of scope

- Dropping any construct (captain decision: compress-only, keep all 10).
- Item 5 context-freezing / multi-draw measurement (postponed).
- Solver-param tuning (item 4b) — separate experiment.

## Cross-refs

`_artifacts/readme-rule-progression-research-2026-06-16.md` (the per-rule overfit review);
`_proposal/retrospective-2026-06-15-program.md`; live `@baseline`
`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047` (36/48 = 0.7500);
READMEs `solver_workflows/{codex-ade-dbt-minimal, h0060-stabilize-f1-coinflips}/README.md`;
`/home/kent/autobench/day-one-runbook.md`.
</content>
