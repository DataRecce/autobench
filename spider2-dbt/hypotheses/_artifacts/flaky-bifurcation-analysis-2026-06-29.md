# Flaky-band bifurcation analysis — 2026-06-29 (concept spd0030)

Per-cell diff of PASSING vs FAILING champion(-ish) draws (transcripts; SQL/verifier-diff not preserved, so
read from the solver's own committed model SQL + validation in agent rollouts). A passing draw = verified
correct answer → the variance source is the choice that differs. **9 analyzed, 7 pinnable, 2 dropped.**

## Pinnable — NEW rule (champion README lacks it; highest GO odds)
- **quickbooks003** → spd0031. FAIL rebuilds upstream `int_*`/`stg_*` (gl 759→990, bs 276→360); PASS builds
  ONLY the missing leaf via narrow `--select <leaf>` (no `+`) on the shipped intermediates. Directive: when
  the target leaf's upstream deps already exist as populated tables, build only the leaf; never rebuild/edit
  a pre-existing upstream model or its casts (even to dodge an unrelated upstream error). Canary: quickbooks002.
- **sap001** → spd0032. FAIL passes an unpivoted-long intermediate straight through (408 rows, 2× grain);
  PASS re-aggregates to the dimensional grain (GROUP BY + SUM, 204). Directive: when the source is a long/
  unpivoted intermediate (one row per measure bucket) but the target grain is one row per key, re-aggregate
  (GROUP BY non-measure cols + SUM measures, round to scale); INNER only on grain-defining table, LEFT for
  enrichment. Canary: marketo001. (Caveat: ~50% flake also has an infra build-fail path a README can't fix.)
- **divvy001** → spd0033. FAIL makes a failing staging not_null test green by adding `WHERE ... is not null`
  (drops 1 row, 426886≠426887); PASS downgrades the test to `severity: warn`, preserving raw grain.
  Directive: when a no-filter staging/passthrough model's column test fails on raw rows, make the test
  non-blocking (warn) — never add a WHERE that drops rows. Canary: f1001.
- **asset001** → spd0034. FAIL rounds the per-unit price early (→ amplified by shares) OR leaves the final
  value full-precision (comparator string-sort artifact); PASS keeps intermediates full-precision and rounds
  ONLY the final product to 2dp. Directive: round only the final derived product-of-(aggregated-price ×
  magnitude) column to 2dp; never round a per-unit price before multiplying. Canary: recharge001.

## Pinnable — SHARPEN an existing-but-under-obeyed rule (harder; rule present, compliance ~70-80%)
- **greenhouse001** → spd0035. FAIL string-casts BIGINT id columns (`cast(... as type_string())`) → grader's
  type-sensitive compare rejects string-vs-int; PASS passes ids native. Champion has "never re-type an id"
  but it's under-obeyed → sharpen with the explicit `type_string()`/varchar prohibition on upstream ids.
  Canary: hubspot001.
- **airbnb001** → spd0036. FAIL computes the rolling window over ALL dates (11k rows); PASS anchors to the
  single MAX source date (3 rows). Champion has the window rule but it's under-obeyed → sharpen + add a
  row-count self-check (rows == distinct group values, not source dates). Canary: mrr001.
- **apple_store001** → spd0037. FAIL re-groups on the canonicalized lookup name (collapses raw-spelling
  duplicate rows); PASS keeps the RAW territory as the grouping key. Champion has the preserve-raw-key
  sub-note but it's under-obeyed → sharpen. Canary: google_play001.

## Dropped — NOT intrinsically champion-flaky (no fix needed)
- **lever001**: its only fail was a spd0022 harness tool-call parse crash (no SQL authored); champion builds
  the shipped model deterministically. NOT pinnable (infra/transient).
- **workday001**: its only fail was spd0022's C1 lever mis-selecting the base relation; champion (no C1)
  anchors correctly and passes. Lever-induced, not intrinsic.

## Smoke design (all hypotheses)
Target cell at **trials=3** (measure the consistency hold-rate — single-draw is the optimism trap) + 1–2
rock-solid canaries. GO = target 3/3 + canaries hold. NO-GO = revise the directive and re-smoke until no
method works, then drop. Up to 2 smokes concurrent.
