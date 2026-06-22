---
id: dab0018
title: Classifier-gated dbt — route multi-source-derivation datasets to dbt, all others to the direct method
status: propose
kind: hypothesis
source: dab0017 REJECTED follow-up. Mandatory-dbt failed (0.565 untuned / 0.603 tuned, both < Opus 0.654) because dbt's derived-intermediate-entity value pays off on only ONE of 12 datasets (crmarenapro, 6 sources, derivation-blocked failures) while its overhead+variance taxes the 2-source datasets. This gates dbt to where it has signal so the non-dbt path stays byte-identical to the anchor.
started: 2026-06-22T04:25:01Z
score: 0.5
completed:
verdict:
---

## Hypothesis

A per-dataset **classifier (oracle-free precondition gate)** at the top of the `model` stage
routes each dataset to one of two methods, in a SINGLE forked README:
- **dbt-pipeline path** (dab0017's tuned method: `stg→int→mart` + tests, ATTACH/pymongo, generic
  marts, answer = query the mart) — used when the gate FIRES;
- **direct path** (the current `spacedock-readme-baseline-hostfix` method verbatim: DuckDB
  ATTACH + pymongo, direct analytical SQL) — used when the gate does NOT fire.

**The gate IS the isolation mechanism** (ade-bench gated-levers-compose pattern, h0049). Because
non-firing datasets run the direct method *verbatim*, they are byte-identical to
`@codex-batch-baseline` → **zero regression by construction** on the 11 two-source datasets. The
only delta vs the anchor is on the firing dataset(s) — collapsing the whole experiment to: "does
gated dbt bank crmarenapro's q2/q3/q7/q8 unlock without the board-wide overhead/variance tax?"

### Gate signal (oracle-free, computable from `db_config.yaml` + `db_description.txt`)

**FIRE dbt iff the dataset has ≥3 source databases.** (crmarenapro = 6; all 11 others = 2 —
verified across every db_config.yaml, dab0017.) Rationale: dbt's value is materializing derived
intermediate entities from MULTI-SOURCE joins; ≥3 sources is the structural marker of
cross-source-derivation work, and it cleanly isolates crmarenapro. **Do NOT** gate on the
dirty-schema trigger — it over-fires on 2-source music_brainz (dab0017 §why-only-crmarenapro).
(Open question for propose: is a pure source-count gate too crmarenapro-specific / overfit? An
alternative is `≥3 sources AND db_description warns of cross-source dirty entity fields`.)

## Acceptance criteria (falsifiable)

- **GO** iff stratified Pass@1 over 12 **beats `@codex-batch-baseline` 0.6966** AND **zero** of the
  36 Opus∩codex-batch canaries regress — judged per-query. Since the gate routes all 2-source
  datasets to the verbatim direct method, any regression there is a GATE-LEAK bug (the branch
  fired wrong), not a method effect.
- **The crmarenapro gain must be STABLE** — dab0017 showed it as variance-fragile (untuned 11/13,
  tuned 9/13). Multi-trial crmarenapro (≥3 draws) to confirm the q2/q3/q7/q8 unlock holds; a
  single-draw +2 is not sufficient (the dab0017 calibration lesson: generative paths add ±0.07
  variance).
- **NO-GO / REJECTED** if (a) the gate mis-fires (a 2-source dataset routed to dbt, or crmarenapro
  routed to direct), or (b) crmarenapro's dbt advantage does not hold across draws, or (c) the
  realized lift is within the ±noise band.

## Honest ceiling (from dab0017 structural analysis)

Only crmarenapro fires the gate, so the **best case is ~+2 cells over the anchor (~+0.03
stratified)** — and dab0017 showed even that is variance-fragile. This hypothesis is worth running
ONLY to (1) cleanly isolate whether the dbt derivation advantage on crmarenapro is real+stable
once the overhead/variance tax on other datasets is removed, and (2) validate the gated-composition
mechanism for DAB. If crmarenapro's unlock proves stable under the gate, it is a small but clean,
attributable, promotable win — the first on DAB. If not, the dbt family is fully closed for DAB.

## Target / canaries

- **Target (gate fires):** crmarenapro — bank q2/q3/q7/q8 (q3 held across both dab0017 dbt runs).
- **Canaries (gate must NOT fire → verbatim direct method):** all 11 two-source datasets; the 36
  Opus∩codex-batch passers must stay byte-identical to the anchor. Any drop = gate-leak bug.
- **Anchor:** `@codex-batch-baseline` (`runs/codex-dab-batch-baseline/bf113446fdd94373`, 0.6966).

## Reusable infra (already built in dab0017 — no rebuild needed)

dab-agent image with dbt + sqlite/postgres scanners baked in (digest `sha256:224133f0…`);
`verify_batch` per-query try/except (razorback PR #19, merged); `spacedock-readme-baseline-hostfix`
(the verbatim direct path); the tuned dab0017 README (the dbt path); `@codex-batch-baseline`
registered. The fork for this entity = a single README that branches on the source-count gate.
