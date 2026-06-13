---
id: h0053
title: Per-key metric aggregate — when the task does NOT ask for completeness, build the aggregate FROM the fact via INNER JOIN; do not LEFT JOIN the full dimension and emit zero-fact keys with NULL metrics
status: hypothesis
kind: hypothesis
source: Captain request 2026-06-13 from _proposal/leverable-flipped-tasks-research-2026-06-13.md (CARD 1, airbnb005). Method artifact-confirmed both directions (h0043 PASS = inner-join/14,243 rows; h0052 FAIL = left-join keep-all/17,499 rows incl 3,256 NULL-NPS). Forks the current @baseline h0052 (runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133).
started: 2026-06-13T00:00:00Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

`airbnb005` builds the per-listing NPS/review aggregate `listing_agg_nps_reviews`. It flips
on a single join-shape choice that the local files do not disambiguate:

- **A (oracle-correct):** derive the aggregate FROM the reviews fact and INNER JOIN the
  listing's metadata, so only listings that actually have reviews appear. The h0043 passing
  run committed exactly this — 14,243 rows, `null_nps_rows = 0`.
- **B (the failure):** LEFT JOIN the full listing dimension and keep every listing, emitting
  ~3,256 zero-review listings with NULL NPS. The h0052 failing run committed this — 17,499
  rows → 2 mismatches on `listing_agg_nps_reviews_equality_with_tolerance`. The solver
  self-validates "0 mismatches" against its own derivation (self-anchored false-green), so it
  cannot catch the divergence itself.

This is the **dual** of the coverage-repair lever already in the README (h0050): that lever
ADDS missing keys *only when the task explicitly asks for completeness*. This lever does the
opposite — *when the task does NOT ask for per-key completeness*, it scopes the aggregate to
keys present in the fact and forbids the NULL-metric zero-fact rows. The two are gated on
opposite sides of the same completeness-intent signal, so they compose without conflict.

**Falsifiable claim (the single README change — Implementation stage only):** adding a
precondition-gated worked-example skeleton — "for a per-key metric aggregate where the task
does NOT request every-key completeness, build FROM the fact via INNER JOIN; do not LEFT JOIN
the full dimension and emit zero-fact keys with NULL metrics" — will make the committed
`listing_agg_nps_reviews.sql` use the inner-join shape, flipping `airbnb005` FAIL→PASS, without
regressing the canary panel (in particular `airbnb009`, where completeness IS requested and the
coverage lever must still keep all days).

**The single proposed README skeleton (generic identifiers, Implementation stage):**

```text
PER-KEY METRIC AGGREGATE (gated). When a task asks to BUILD or create a per-key metric
aggregate (e.g. an NPS / review / rating rollup keyed by listing/customer/entity) and the
instruction does NOT request row/key COMPLETENESS (no "a row for every <key>", "include all
<keys>", "rows are missing"), scope the output to keys that actually have fact rows: build the
aggregate FROM the fact and INNER JOIN the key's metadata. Do NOT LEFT JOIN the full key
dimension and emit keys with zero fact rows carrying NULL metrics.

(If the instruction DOES request completeness, this rule does not apply — follow the
coverage-repair rule above instead.)

BEFORE (keeps zero-fact keys as NULL-metric rows — AVOID when completeness is not asked):
    select dim.key, agg.metric
    from {{ ref('key_dimension') }} dim
    left join fact_agg agg using (key)        -- emits NULL-metric rows for zero-fact keys

AFTER (scope to keys present in the fact):
    select dim.key, agg.metric
    from fact_agg agg                          -- driven by the fact
    inner join {{ ref('key_dimension') }} dim using (key)   -- zero-fact keys excluded
```

## Acceptance criteria

**AC-1 — Exactly one README change; specs differ only in `experiment:` + `solver_workflow:`.**
README diff vs the h0052 solver README adds exactly one Implementation-stage gated block (the
per-key-aggregate inner-join rule), inserted after the coverage-repair block and before "Run
basic confirmation…"; Exploration/Validation/Finalization and the leak-guard + the other four
levers byte-identical. No `AUTO_*`/`solution__*`/`check_*`/`equality test`/`nps`/`listing_agg`/
expected-row-count token; no `curl`/`wget`/`git clone`. `agent.kind: spacedock_solver`,
`runtime: codex`, `trials: 1` preserved.

**AC-2 — Every score paired with a clean strict audit.** Each `rk score` cites
`rk audit --policy strict` on the same run-dir (`tainted: 0`, `coverage_missing: 0`,
`captured > 0`).

**AC-3 — The decisive read is the committed artifact.** Read the committed
`listing_agg_nps_reviews.sql` from the dispatched-ensign `apply_patch`. Classify: does the
metric aggregate drive from the fact with an INNER JOIN to the listing dimension (no NULL-NPS
zero-review rows)? A flip is credited only when the inner-join shape lands AND the verifier
passes. Transcript chatter does not count.

**AC-4 — No regression-canary loss, incl. the inverse-construct hold.** All `@baseline`
passers in the smoke panel stay PASS. CRITICAL: `airbnb009` (completeness IS requested) must
hold PASS on its byte-identical all-three-fork coverage edit — proving the new inner-join rule
did not conflict with the coverage lever's keep-all-days case. Any canary regression is a
NO-GO unless artifact-proven unrelated single-trial variance and the captain accepts the risk.

**AC-5 — Reproducibility judged against the base rate.** airbnb005 is ~89% at @baseline (a
near-stable passer that drops ~1-in-9). Smoke runs airbnb005 as ≥2 seed-perturbed repeats; GO
requires the inner-join artifact + verifier pass + clean audit on every repeat, with the honest
note that the marginal score value is low (high base rate) and the real win is closing the
join-shape construct.

## Target dataset

Primary target: `ade-bench-airbnb005`.

Smoke panel (target + canaries):
- `ade-bench-airbnb005` — 🎯 target.
- `ade-bench-airbnb009` — ✅ MUST-HOLD inverse-construct canary (completeness requested; the
  coverage lever must still keep all days — proves no conflict).
- `ade-bench-airbnb008` — ✅ same-family perturbable canary (the cell h0046 bled onto; proves
  the new aggregate rule does not re-introduce same-family collateral).
- `ade-bench-airbnb001` — ✅ same-family canary.
- `ade-bench-asana001`, `ade-bench-f1007`, `ade-bench-quickbooks002` — ✅ cross-family canaries.

GO requires the inner-join artifact read on airbnb005 (≥2 repeats) + every canary PASS on a
clean audit, with airbnb009 explicitly holding.

## Honest tension with the standing decisions

- **`trials: 1` / no best-of-N.** airbnb005 is ~89% already; a join-shape lever can only RAISE
  the per-draw probability of the inner-join shape, not make it deterministic, and the marginal
  aggregate score is small. Judge by committed artifact (AC-3), not the single reward.
- **Bleed risk (MODERATE).** A left-join keep-all is *correct* when completeness is requested —
  that case belongs to the coverage lever (h0050) and is gated out here by the completeness-intent
  test. The airbnb009 MUST-HOLD canary is the tripwire for any gate conflict.

Method/README change only. Forks @baseline h0052 (`solver_workflows/h0052-compose-maxpoints-featureguard-scoped-coverage`, runtime codex); no dataset, harness, or runtime change.
