# Leverable Flipped-Task Research — candidate hypotheses

Date: 2026-06-13
Author: operator (forensic reads on committed artifacts across run-dirs on disk)
Purpose: a review-then-build document. For each flipped task that is plausibly fixable
by a solver-README lever, this records the failure construct, the artifact evidence, the
oracle-correct convention, and a concrete proposed lever method. We review this, then
spin up hypotheses from the cards below.

Companion: `_artifacts/round1-round2-flipped-task-choice-map.md` (the full 19-task
volatility map + pass rates). Lever-form rules: `_artifacts/bug-type-taxonomy.md` and the
instruction-lever taxonomy memory.

## Scope

19 tasks flip across the gpt-5.5 `trials:1` run-dirs. Of those:
- **8 are already covered by an active README lever** (inherited into h0052): airbnb009,
  f1006, f1006-hard, f1005, f1005-medium (h0044 max-points); quickbooks002, quickbooks004
  (h0045 feature-boundary); asana002 (h0043 package var-gating, attribution-boundary case).
- **4 are NOT README-addressable** — f1011, f1003, f1003-hard (oracle-only answer-selection,
  `count_answers`/`check_option_*`, no local signal — the solver-blind-to-oracle wall) and
  airbnb008 (already fixed; its only flip was the h0046 lever bleed, gated by h0050).
- **7 are leverable** — the subject of this document.

## The banking caveat (read first)

Every card below proposes a *construct fix*, and each is expected to flip its target on
the artifact. But at `trials:1` the board carries ~19 volatile cells, and any single full
run loses ~3–4 of them to off-construct noise regardless of the lever. h0051 and h0052 both
produced an artifact-real **+3** and still netted to a tie. So: these levers are worth
building to **close the construct knowledge gap and raise the construct score**, but the
*aggregate* pass rate will keep being masked until a measurement change (multi-trial on the
volatile tail) is accepted. File these for correctness, not to chase the headline number.

## Shared lever form (applies to every card)

The only delivery form proven to reach the committed SQL is a **copyable before→after
worked-example skeleton** with generic identifiers (h0046/h0050; prose-only h0010/h0016 went
inert). Every lever below should be:
1. A single Implementation-stage worked-example skeleton, generic identifiers only.
2. **Precondition-gated** so it fires only on its construct (the h0050 lesson — an ungated
   generative skeleton bled onto airbnb008). State the firing condition explicitly.
3. Leak-clean: no `AUTO_*`/`solution__*`/`check_*`/dataset slug/expected-count tokens.
4. Carried into smoke with **≥1 perturbable same-construct canary** (the G8 blind spot that
   sank h0046 — a non-firing canary is not enough).

---

## CARD 1 — airbnb005 (pass rate 16/18, 89%) — CONFIRMED method

- **Construct:** per-listing NPS/review aggregate; handling of zero-review listings.
- **Failure (artifact):** failing run LEFT-JOINs the full listing dimension and keeps all
  listings, emitting ~3,256 zero-review groups with NULL NPS (17,499 rows) → fails
  `listing_agg_nps_reviews_equality_with_tolerance` (Got 2). The solver self-validates
  "0 mismatches" against its own derivation — self-anchored false-green, can't self-catch.
- **Oracle-correct (confirmed):** EXCLUDE zero-review listings via an INNER JOIN to the
  reviews aggregation → 14,243 rows, no NULLs. Passing run (h0043) committed exactly this.
- **Proposed lever (worked-example skeleton):**
  > A per-key review aggregate should be built FROM the reviews fact and INNER JOIN the
  > key's metadata. Do NOT LEFT JOIN the full dimension and emit keys with zero fact rows
  > carrying NULL metrics.
  > BEFORE:  `from dim_key left join reviews_agg using(key)`  -- emits NULL-metric zero-fact rows
  > AFTER:   `from reviews_agg inner join dim_key using(key)`  -- zero-fact keys excluded
- **Gate:** fires on per-key review/NPS aggregates that LEFT JOIN a dimension. **Bleed risk:
  MODERATE** (join-type convention is somewhat generative). Canary: a second airbnb aggregate
  passer that legitimately keeps all keys, to prove the gate doesn't over-fire.
- **Confidence: HIGH.** Method artifact-confirmed both directions.
- **Headroom:** low (already 89%) — marginal score value, but a clean, knowable fix.

## CARD 2 — f1010-medium (11/15, 73%) — method known, VERIFY convention

- **Construct:** `analysis__lap_times` by track/year, accounting for pit stops.
- **Failure mode (from flip-map history; NOT yet re-read on a fresh artifact):** keep
  pit-stop laps and subtract pit-stop duration vs the oracle's exclude-them-before-averaging.
- **Oracle-correct (per flip-map):** EXCLUDE pit-stop laps before averaging.
- **Proposed lever (worked-example skeleton):**
  > When averaging lap times with pit stops, FILTER OUT pit-stop laps before the aggregate.
  > Do not retain pit-stop laps and subtract pit-stop duration.
  > BEFORE:  `avg(lap_time - pit_stop_duration)` over all laps
  > AFTER:   `avg(lap_time)` where `is_pit_lap = false`
- **Gate:** fires on lap-time averages that account for pit stops. **Bleed risk: LOW** (narrow).
- **Confidence: MEDIUM-HIGH on method, but VERIFY FIRST** — read a failing vs passing
  `analysis__lap_times.sql` to confirm exclude-vs-subtract before filing (flip-map is the
  only current source).
- **Headroom:** moderate. Cleanest single-construct win; same shape as the proven max-points lever.

## CARD 3 — ana-eng003 (15/16, 94%) — CONFIRMED method

- **Construct:** build `dim_customer` from `stg_customer`; "rename id→customer_id, make PK".
- **Failure (artifact):** failing run selected only 5 of 18 columns from the staging model
  (dropped job_title, phones, address, city, state, zip, country, web_page, notes,
  attachments, …) → compile-time `AUTO_dim_customer_equality` "has less columns than
  solution__dim_customer". Classification: **(a) DROPPED-EXISTING** — the columns exist
  upstream; the model over-narrowed the select. The task never restricted columns.
- **Oracle-correct (confirmed):** carry ALL upstream columns through to the dimension
  (passing run selected all 18 from `stg_customer`).
- **Proposed lever (worked-example skeleton):**
  > When a build/rename task does not restrict the column set, PRESERVE every column from
  > the upstream/staging model — do not narrow the select to a subset you judge "relevant."
  > Apply only the renames/keys the task names; keep all other columns.
  > BEFORE:  `select id as customer_id, company, last_name, first_name, email from stg`
  > AFTER:   `select id as customer_id, /* …all remaining stg columns… */ from stg`
- **Gate:** fires when building/renaming a model from a single upstream model and the task
  does not enumerate a restricted column set. **Bleed risk: MODERATE-HIGH** — "preserve all
  columns" is generative; could conflict with tasks that legitimately project a subset.
  MUST carry a canary that legitimately narrows columns to prove the gate is safe.
- **Confidence: HIGH on mechanism, MEDIUM on safe gating.** This is the inverse of the
  quickbooks003/feature-boundary construct (see cross-task note) — under-include vs over-include.
- **Headroom:** low (94%).

## CARD 4 — quickbooks003 (17/22, 77%) — method = an EXISTING lever

- **Construct:** removing the `using_department` feature; `int_quickbooks__*_union` /
  `ap_ar_enhanced` models.
- **Failure (artifact):** the solver removed the `{% if var('using_department') %}` guards
  but LEFT the `departments.fully_qualified_name as department_name` column body in the
  select → orphaned column → schema mismatch vs solution. Classification: **(b) feature-guard
  removal handled wrong** — identical construct to quickbooks002.
- **Oracle-correct:** delete the ENTIRE guarded block including the column body, not just the
  `{% if %}` wrapper. This is exactly what **h0045 (feature-boundary removal/toggle guard)**
  prescribes — and h0045 is already composed into h0052.
- **Action — NOT a new lever:**
  1. Confirm h0052 (which carries h0045) stabilizes quickbooks003 (it passed in h0052; all 5
     historical failures were in runs WITHOUT h0045).
  2. Optionally SHARPEN the existing h0045 block with a worked-example skeleton showing the
     delete-whole-block edit (h0045 is currently prose, flagged G7 inert-risk):
     > BEFORE: `{% if var('using_feature') %} feature_col, {% endif %}`  -- removing the guard only
     > AFTER:  (entire line deleted)                                      -- remove guard AND column
- **Confidence: HIGH.** Same construct as an already-working lever.
- **Headroom:** moderate (77%).

## CARD 5 — f1001 (23/28, 82%) — completeness-style, leverable

- **Construct:** re-wire the F1 staging layer onto the correct `src` models / sources.
- **Failure (artifact):** some `stg_*` models left on the old/wrong source →
  `stg_models_use_src_models` (Got 11), `stg_races/stg_results_uses_correct_sources`,
  `src_models_are_correct` (compile error). Incomplete or incorrect source-rewiring.
- **Oracle-correct:** every `stg_*` references its corresponding `src` model; none left on
  the prior source.
- **Proposed lever (worked-example + completeness check):**
  > When re-wiring staging onto sources/src models, EVERY `stg_*` must reference its
  > corresponding `src` model. Before finalizing, list the staging models and verify none
  > still reference the old/raw source directly.
- **Gate:** fires on staging-source-rewiring tasks. **Bleed risk: LOW-MODERATE.**
- **Confidence: MEDIUM** — it's a completeness sweep, not a single SQL shape, so less reliable
  than a worked-example. *Re-read a fresh failing artifact to confirm whether the failures are
  "left a stg on the old source" vs a deeper src-definition error before finalizing wording.*
- **Headroom:** moderate.

## CARD 6 — asana003 (14/20, 70%) — known mechanism, brittle to pin

- **Construct:** remove all Asana `tmp` models; make `stg_asana__*` reference sources directly.
- **Failure (artifact):** a broad `var()` rewrite + tmp deletion leaves `asana__task` empty
  → downstream `asana__daily_metrics`'s Jinja `run_query('min(created_at)')` returns None →
  compiled `cast('None' as date)` parse error → all 6 equality tests cascade-fail.
- **Oracle-correct:** repoint conservatively, preserving the tmp layer's column/type/row
  behavior so downstream models still build with non-empty inputs.
- **Proposed lever (restraint + build-verify):**
  > When removing tmp/intermediate models and repointing staging to sources, PRESERVE the
  > column/type/row behavior of the layer you remove. After the edit, verify downstream models
  > still build and that no model feeding a `run_query()` returns an empty result.
- **Gate:** fires on tmp-removal / staging-repoint tasks. **Bleed risk: LOW-MODERATE.**
- **Confidence: LOW-MEDIUM** — the failure is a build-path interaction (empty input → None-date),
  hard to express as a clean before→after skeleton. May not bank.
- **Headroom:** moderate.

## CARD 7 — airbnb007 (4/17, 24%) — method known, historically RESISTANT (moonshot)

- **Construct:** create the Airbnb models in `schema.yml`, incl. rolling NPS/review aggregates.
  TWO failure axes at once.
- **Failure modes:** (a) 28-day rolling window done with `ROWS BETWEEN 27 PRECEDING` (fails on
  sparse dates) instead of a calendar date range; (b) the task is scored by TWO models
  (`daily_agg_nps_reviews` AND `listing_agg_nps_reviews`) — a fix to one passes smoke but
  fails full.
- **Oracle-correct:** calendar-date-range 28-day window; fix BOTH scored models.
- **Proposed lever (worked-example, two-part):**
  > A rolling N-day window over sparse dates must range over a CALENDAR date spine, not
  > `ROWS BETWEEN n PRECEDING`. Also: this task scores BOTH the daily and the listing
  > aggregate — apply the fix to both.
  > (skeleton: a calendar date_spine join + `sum(...) over (order by date range between ...)`)
- **Gate:** fires on rolling-window-over-dates aggregates. **Bleed risk: MODERATE.**
- **Confidence: LOW on banking** — this exact family (grain/width/window) beat h0010, h0016,
  and h0019. Method is known; odds are poor.
- **Headroom:** largest (24%), but historically the hardest cell on the board.

---

## Cross-task observations

1. **Column-set is a TWO-WAY construct.** ana-eng003 fails by UNDER-including (dropped
   existing upstream columns); quickbooks003 fails by OVER-including (orphaned feature-guard
   column). A single "preserve columns" rule helps one and hurts the other — do NOT merge them
   into one lever. ana-eng003 → "carry all upstream columns"; quickbooks003 → "delete the whole
   guarded block" (= h0045). Keep them as distinct, oppositely-gated rules.

2. **Three of the leverable methods reduce to a known winning form:** airbnb005 (join-type
   convention), f1010-medium (filter-then-aggregate convention), ana-eng003 (column
   preservation) are all "pin the correct local convention" — the same shape that made the
   max-points lever (h0044) work. These are the strongest candidates.

3. **The answer-selection family (f1011/f1003/f1003-hard) is the hard wall** and is excluded
   here. If banking the score ever matters more than construct coverage, the move for those is
   multi-trial scoring, not a lever.

## Recommended filing order (for the hypotheses we build from this)

| # | Task | Confidence | New lever? | Verify before filing? |
|---|------|-----------|-----------|----------------------|
| 1 | airbnb005 | HIGH | yes (gated inner-join) | no — confirmed |
| 2 | f1010-medium | MED-HIGH | yes (gated exclude-laps) | YES — re-read a failing artifact |
| 3 | ana-eng003 | HIGH mech / MED gate | yes (gated preserve-columns) | no — confirmed; design the gate carefully |
| 4 | quickbooks003 | HIGH | NO — confirm h0052/h0045 covers; optionally sharpen | confirm h0052 result |
| 5 | f1001 | MED | yes (completeness) | YES — confirm failure is "stg on old source" |
| 6 | asana003 | LOW-MED | yes (restraint+build-verify) | — brittle, lower priority |
| 7 | airbnb007 | LOW (resistant) | yes (calendar-window+dual-model) | — moonshot, file last |

**Composition note:** per h0049/h0052, disjoint precondition-gated levers compose additively
in one README without interference. Once 2–3 of cards 1–3 pass solo smoke, compose them onto
@baseline (as h0052 did) rather than promoting singly. Watch the ana-eng003 gate especially —
its "preserve all columns" rule is the most generative and needs the strongest canary.

## Open verification items (do before filing the affected card)

- [ ] f1010-medium: read a failing + passing `analysis__lap_times.sql` to confirm
      exclude-vs-subtract (Card 2 relies on flip-map history, not a fresh artifact).
- [ ] f1001: confirm the failing mechanism is "stg left on old source" vs a deeper
      src-definition error (Card 5 wording depends on it).
- [ ] quickbooks003: confirm h0052 (with h0045) actually stabilizes it before deciding
      whether any new work is needed (Card 4).
