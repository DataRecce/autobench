# Gate 0 — dbt batch feasibility probe (crmarenapro)

**Run:** `runs/dab-gate0-probe/6678c771ca6b237b` (rc=0, 2026-06-21)
**Spec:** `specs/dab-gate0-probe.smoke.frozen.yaml` — crmarenapro, `query_mode: batch` +
`workspace_variant: spacedock`, codex/gpt-5.5 reasoning_effort=high.
**Image:** dab-agent `sha256:4ee4387c…` (Step 0).

> **REVISED after Gate-0 antagonist review (antagonist-gate0).** This first probe proved the
> *plumbing* but NOT the *method*. Corrections below; verdict downgraded to **PASS (plumbing
> only) — re-probe required on the extension-fixed image before Gate 1.**

## RE-PROBE (fixed image + hardened README) — Gate 0 PASS on the real criteria

**Run:** `runs/dab-gate0-probe/1e1f3a87afc9d073` (rc=0). Image `sha256:224133f0…` (extensions
baked); probe README hardened to mandate native ATTACH + GENERIC entity-grain marts.

| design-faithful criterion | re-probe result |
| --- | --- |
| native `ATTACH` of sqlite/duckdb/postgres OFFLINE (design §4/§5-item2) | ✅ ATTACH ×17 via `profiles.yml`/`attach:`, extensions autoloaded (`INSTALL` no-op ×71), **no seed export** |
| one generic pipeline built once, all 13 answered | ✅ |
| GENERIC entity-grain models, NOT per-question (design §9) | ✅ models are `stg_*` per source table + `int_quote_lines`/`int_lead_discussions`/… + `mart_cases`/`mart_opportunities`/`mart_orders`/`mart_contacts`/`mart_quotes`. **No `mart_qN` files; no answer-ID literals in model SQL** (verified: the ID literals in the trace are question-GIVEN inputs, analyze-stage `where product_id='…'` filters against the generic `mart_cases`, or exploration output — none baked into models) |
| question-specific filtering in `analyze` SELECT, not models | ✅ |
| `verify_batch` + per-query rewards | ✅ |

**Score:** 7/13 (q1,q3,q4,q5,q7,q10,q11). LOWER than probe-1's overfit 11/13 — this is the
**honest** generic-pipeline number on a single draw (probe-1's 11/13 was inflated by
explore-then-fit + hardcoded marts). Feasibility is about the runtime/method working, NOT the
score; the real score comparison is Gate 1.5/2 vs `@codex-batch-baseline`. The README that
produced this is the basis for the Gate-1 variant README.

**Independent re-probe antagonist (antagonist-gate0-reprobe): RE-PROBE PASS.** Reconstructed
all 44 model bodies from the apply_patch payloads and verified: native offline ATTACH (44/44
models across sqlite+duckdb+postgres), zero `mart_qN` files, zero hardcoded answer literals in
model SQL (the only model `where` constants are structural schema metadata like
`field_name in ('owner','ownerid')`; all answer IDs appear only in analyze SELECTs), exact-ID
PASSes (no false-greens), `dbt test` 18/18 green, clean leak-guard. No blockers before Gate 1.
Two non-blocking carry-forwards: (1) single-trial low-cardinality categorical PASSes (q1/q3/q4)
have intrinsic false-green exposure — judge by derivation, prefer multi-draw if a target cell;
(2) first `dbt run` needed a `read_only: true` attach retry → **folded into the variant README
skeleton** (each attach entry now `read_only: true`) to save a build cycle.

## STOP-condition check (handoff §3) — MET (plumbing)

## STOP-condition check (handoff §3) — MET (plumbing)

| requirement | result |
| --- | --- |
| one dbt build serves all queries | ✅ agent built one persistent `_artifacts/dbt/scratch.duckdb`, served all 13 ("using one dbt build that serves all queries, preserving the dbt scratch") |
| answers all queries into one answers.json | ✅ q1..q13 all graded |
| `verify_batch` runs, per-query rewards appear | ✅ `reward_per_query.json` has q1..q13 each with reward+reason |
| dbt scratch survives `model → analyze` | ✅ analyze queried the already-built scratch (no per-query rebuild) |

**Headline:** 11/13 = 0.846 (PASS q1,q3,q4,q5,q6,q8,q9,q10,q11,q12,q13; FAIL q2,q7).
**NOT a reach signal — withdrawn.** The antagonist showed the agent EXPLORED answers with
ad-hoc duckdb queries first, then wrote per-question `mart_qN` SQL to reproduce them. q3
passed via a hardcoded keyword→stage map, q8 via a date window tuned in exploration. With
single-trial + codex≠Opus + per-question overfit, 11/13 is not portable methodology evidence.
q2/q7 failed on **logic, not connectivity** (postgres WAS reachable via psycopg2; full-table
exports, rowcounts matched): q2 picked the wrong article id; `mart_q7` literally returned
`select 'None'`. (My earlier "q2/q7 are postgres-ATTACH failures" guess was WRONG.)

## Antagonist-surfaced BLOCKERS for the method (must shape the Gate-1 README)

- **§9 violation — per-question hardcoded marts.** The agent wrote one `mart_qN` per query with
  answer literals baked in (transcript phrases, article titles, `select 'None'`). Design §9
  forbids per-question models; the reusable-pipeline thesis is untested. → The variant README
  MUST forbid per-question models + hardcoded answer literals, require GENERIC entity-grain
  marts, and put question-specific filtering in the `analyze` SELECT, not in models.
- **explore-then-fit inverts the two-phase shape.** Answers were derived in `model`-stage
  ad-hoc SQL, then marts authored to match — the opposite of "build generic models, then query."
- **LLM-judge in `verify_batch`** (q7 reason: "LLM output indicates no policy violation") — a
  non-deterministic grading path. Material for any pass-rate claim; was absent from this doc.
- **No persisted artifacts** — judge dbt models from the transcript (see run-notes).
- **Single-process stage "boundary"** — model→analyze ran in one ensign session, so scratch
  survival is trivial here. In production stages share one container workdir, so a persistent
  `scratch.duckdb` file survives regardless (design open-Q3 resolved: use a file, not in-memory).

## CRITICAL finding — design §5 Gate 0 item 2 ("ATTACH works") is FALSIFIED offline

The run container blocks egress to `extensions.duckdb.org`. DuckDB ships the
`sqlite_scanner` / `postgres_scanner` as **download-on-demand** extensions, so
`INSTALL sqlite/postgres` and therefore `ATTACH ... (TYPE SQLITE|POSTGRES)` **fail
offline**. Verified directly in the image with `--network none`:
`IO Error: Failed to download extension "sqlite_scanner" at .../v1.5.4/linux_amd64/...`.

The probe agent discovered this at runtime and **fell back to exporting the sqlite/
postgres/duckdb sources into dbt seeds**, then normalizing with `stg_*` models — still a
valid one-build dbt pipeline, which is how it reached 11/13. So the *method* works even
without ATTACH, but NOT the way design §4 prescribes (`profiles.yml → ATTACH the sources`).

### Fix is feasible and clean (verified)
Preinstalling the two scanners into the image at **build time** (egress available) and
loading them via a fixed `extension_directory` makes `LOAD`+`ATTACH` work **offline**:
```
LOAD ok offline
ATTACH sqlite ok: [(42,)]
```
(extensions land at `<extdir>/v1.5.4/linux_amd64/{sqlite,postgres}_scanner.duckdb_extension`).

### Decision needed (escalated to captain — handoff says don't improvise on design disagreement)
- **Option A — preinstall extensions in image** (design-faithful: dbt `ATTACH`s natively
  offline; removes the seed-export agent burden as a confound). One more image layer.
- **Option B — README guides the seed-export fallback** (what the probe did; 11/13 but
  q7/q2 — likely the postgres-backed queries — failed; adds agent work that itself risks
  overhead regressions, muddying the @codex-batch-baseline overhead measurement).
- **Option C — accept emergent behavior, document only.**

Recommendation: **A** — matches the "dbt baked into image" philosophy and the existing
`dab-agent-image-duckdb-extension-preinstall` backlog entity; keeps the README the single
lever and the IV clean.
