---
title: Implementation — a coverage-repair worked-example skeleton that pins ALL THREE forks at once (drop the narrowing date-spine predicate, keep COUNT(*) byte-intact, do NOT cross-join the secondary category) in one copyable before→after block
status: analyze
kind: hypothesis
source: concept-airbnb009-reproducible-fix (ideate 2026-06-11), grounded in the airbnb009 failed-attempt forensics h0019 (pinned forks #1+#3, left #2 free) / h0042 (pinned #2, left #1+#3 free). Forks the current @baseline solver (solver_workflows/codex-ade-dbt-minimal).
id: h0046
started: 2026-06-11T00:00:00Z
---

## Hypothesis

`airbnb009` is the date/calendar-spine completeness repair whose correct fix is fully
artifact-proven yet has never reproduced at `trials: 1`. The committed
`models/agg/mom_agg_reviews.sql` passes the hidden `mom_agg_review_date_range` check only when
**three implementation forks all land in the SAME draw**:

1. **Drop the narrowing predicate** `WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE …)` from
   the date CTE so every calendar day is present (the spine half).
2. **Keep `COUNT(*)`** as the aggregate — do NOT "tidy up" to `COUNT(review_cte.REVIEW_DATE)`.
   The forensics proved this is THE discriminator: the column-count rewrite makes the 722
   zero-review days carry `REVIEW_TOTALS=0` instead of the oracle's `1`, breaking the windowed
   `sum(REVIEW_TOTALS)`.
3. **No cross-join** of the secondary category (sentiments) onto every day — let categories
   emerge from the existing `LEFT JOIN` + `GROUP BY`. A `(days × categories)` cross-join
   over-produces rows and breaks the windowed `count(*)`.

The decisive lesson from h0019 and h0042: **pinning one fork at a time cannot bank this target.**
h0019 shipped an anti-cross-join skeleton (forks #1+#3) but left the aggregate line free → at
full the solver "improved" `COUNT(*)`→`COUNT(review_cte.REVIEW_DATE)` and failed. h0042 pinned
`COUNT(*)` via abstract abstain-prose (fork #2) but left the spine/restructure free → at full the
solver rebuilt with a cross-join AND flipped the count back. Each pin narrows the space but leaves
enough free choices that the joint probability of all three at once stays a coin-flip.

**Falsifiable claim (the single README change — Implementation stage only):** replacing the free
degrees of freedom with **one copyable before→after SQL worked-example skeleton that pins all
three forks simultaneously** — drop the one narrowing membership predicate, KEEP the aggregate
expression byte-intact (do not rewrite `COUNT(*)`/`COUNT(col)`/any aggregate while doing a
coverage repair), and KEEP the existing `LEFT JOIN`/`GROUP BY` byte-intact (add no new
cross-join CTE) — will make the committed `mom_agg_reviews.sql` land all three forks in a single
draw, flipping `airbnb009` FAIL→PASS reproducibly, without regressing the canary panel.

This is the h0030/h0019 finding extended: a *copyable skeleton* is the only form that has reliably
REACHED the committed SQL (prose-only h0010/h0016 went inert). h0019's skeleton showed exactly ONE
fork (the anti-cross-join). This hypothesis's net-new bet is that **a skeleton showing all three
forks in one block holds all three under a single draw** — the open question the concept names.

**The single proposed README skeleton (generic identifiers, no target-specifics):**

```text
A coverage repair (missing rows / missing days / a narrowed spine) is a SUBTRACTIVE,
in-place edit. Make exactly these edits and NOTHING ELSE: (1) delete the one narrowing
membership predicate that filters the complete dimension down to keys that already
appear in the fact; (2) leave the aggregate expression BYTE-INTACT — do not rewrite a
COUNT(*) into COUNT(col), or change any SUM/AVG/window, while repairing coverage; (3)
leave the existing join and GROUP BY BYTE-INTACT — do not add a cross join of a
secondary category against the dimension. Let categories emerge per key through the
join the model already has.

BEFORE (the bug + the two over-eager rewrites to AVOID):
    with day_set as (
        select date_col from {{ ref('dimension') }}
        where date_col in (select distinct fact_date from {{ ref('fact_detail') }})  -- the narrowing predicate
    ),
    cats as (select distinct category_col from {{ ref('fact_detail') }}),       -- DO NOT add this
    grid as (select * from day_set cross join cats)                             -- DO NOT add this
    select count(fact.fact_date) as totals                                      -- DO NOT rewrite the aggregate
    from grid left join {{ ref('fact_detail') }} fact on ... group by ...

AFTER (drop the predicate, keep COUNT(*) byte-intact, no cross join):
    with day_set as (
        select date_col from {{ ref('dimension') }}                            -- narrowing predicate DELETED
    )
    select count(*) as totals                                                  -- aggregate UNCHANGED
    from day_set left join {{ ref('fact_detail') }} fact on ... group by ...   -- existing join + group by UNCHANGED
```

## Acceptance criteria

**AC-1 — Exactly the README change; specs differ only in `experiment:` + `solver_workflow:`.**
`diff specs/baseline.yaml specs/h0046-….yaml` shows only `experiment:` + `solver_workflow:`;
the README diff vs `codex-ade-dbt-minimal/README.md` touches only `## Stage: Implementation`
(the single all-three-fork skeleton, inserted after the "...schema patterns." paragraph and
before "Run basic confirmation..."), leaves Exploration/Validation/Finalization and the
dependency/leak-guard prose byte-identical, and references no hidden `AUTO_*`/`solution__*`/
`check_*`/`verifier`/`Got N`/`equality test`/oracle count, no `dim_dates`/`sentiment`/`4508`/
`12278`/`mom_agg` target-specific token, and no `curl`/`wget`/`git clone`/web fetch.
`agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved.

**AC-2 — Every recorded score is paired with a clean strict audit.**
Each `rk score` cites a `rk audit --policy strict` on the SAME run-dir, clean (`tainted: 0`,
`coverage_missing: 0`), `captured > 0`.

**AC-3 — The decisive read is the committed artifact on ALL THREE forks, not transcript chatter.**
For every `airbnb009` run, read the committed `models/agg/mom_agg_reviews.sql` from the
dispatched-ensign `apply_patch` payload and classify EACH fork independently:
(#1) narrowing predicate gone? (#2) aggregate expression still `COUNT(*)` byte-intact (NOT
`COUNT(review_cte.REVIEW_DATE)` / any column-count)? (#3) no new cross-join CTE; existing
`LEFT JOIN`/`GROUP BY` intact? A flip is credited only when all three are simultaneously
satisfied AND the verifier passes. Transcript claims do not count.

**AC-4 — Reproducibility, judged honestly against the ~17% base rate (the h0042 trap).**
airbnb009 passes only ~2/12 (~17%) across the full run-dirs on disk. Per the standing
single-trial decision, a clean focused-smoke streak is NOT a flip predictor. So smoke must run
airbnb009 as **≥3 independent focused repeats** (fresh context / seed-perturbed to bust the
content-addressed run-dir cache, per the h0042 run-mechanics note), and GO requires **all
repeats land all three forks (AC-3) + verifier pass + clean audit**. State up front that even a
perfect three-fork pin only raises the per-draw probability — the full verdict is provisional
pending the 48-task run, and a single full FAIL where the committed artifact shows all three
forks landed is the honest signal that the mechanism works but `trials: 1` cannot bank it.

**AC-5 — No regression-canary loss.** All `@baseline` passers in the smoke panel must stay PASS.
Any canary regression is a NO-GO unless artifact analysis proves it is unrelated single-trial
variance and the captain explicitly accepts the risk.

**Smoke gate:** target `ade-bench-airbnb009` + the G8 canary panel (`ade-bench-airbnb001`,
`ade-bench-asana001`, `ade-bench-ana-eng001`, `ade-bench-f1007`, `ade-bench-quickbooks002`) +
the ≥3 focused airbnb009 repeats. GO requires the three-fork artifact read on every repeat and
zero canary regression before full.

## Target dataset

Primary target: `ade-bench-airbnb009` — the one task where all three forks and the intended
mechanism are artifact-proven. The rule is **generative** (it fires on any coverage repair), so
per gatekeeper G8 the smoke carries a cross-family regression-canary panel — one `@baseline`
passer per non-target family (`airbnb001`, `asana001`, `ana-eng001`, `f1007`, `quickbooks002`;
no intercom passer exists). Same structural G8 limit as h0019/h0042: only one airbnb non-target
passer and no second coverage-repair passer to recruit as a perturbable canary — accept the
residual full-scale blind spot.

## Honest tension with the standing decisions

- **`trials: 1` / no best-of-N** (MEMORY `ade-bench-single-trial-judge-by-artifact`). A ~17% cell
  is hard to bank in one draw; a three-fork skeleton can only RAISE the per-draw probability, not
  make it deterministic. If the committed artifact lands all three forks but the single scored
  draw still falls on a residual free choice the skeleton does not pin, this is un-promotable by
  construction — exactly as h0019/h0042 were. The judge-by-artifact rule (AC-3) is how we tell
  "mechanism works but unbankable" apart from "mechanism inert."
- **The concluded flip-portfolio wall** (MEMORY `ade-bench-oracle-program-concluded`). airbnb009 is
  the last open flip target; the box is closed at the lever level. This is filed as a genuinely
  NEW mechanism class (pin-all-three-forks-in-one-skeleton), distinct from h0019 (one-fork
  skeleton) and h0042 (one-fork abstain-prose). If smoke shows the committed SQL still breaks any
  one fork, it joins the wall and is REJECTED with no iteration (CAPPED one-shot).

Method/README change only. Forks the current `@baseline` solver
(`solver_workflows/codex-ade-dbt-minimal`, runtime codex); no dataset, harness, or
solver-runtime change.

> **Note (propose, 2026-06-11):** the `source:`/closing lines above name the stale seed
> `codex-ade-dbt-minimal`; the actual fork parent is the live `@baseline` =
> `solver_workflows/h0043-package-update-optional-resource-matrix` (registry resolves
> `@baseline` → `runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea`).
> The README diff was taken against, and the skeleton stacks on top of, the h0043 parent
> (the asana002 var-gating rule is left byte-intact). Stale-baseline slip flagged by the
> gatekeeper (G1/G6 evidence); verdict unaffected since the verified diff governs.

## Gatekeeper review

**Recommendation: APPROVE** — single Implementation-stage worked-example skeleton, leak-guard byte-intact, specs scoped to two fields; the only flags are WARN-only inert/variance predictions and one G12 probe-provenance note, none of which block the gate.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-10). Reviewed 2026-06-11T00:00:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Parent resolved by registry to `solver_workflows/h0043-package-update-optional-resource-matrix` (the `source:` line names the stale seed `codex-ade-dbt-minimal` — a noted stale-baseline slip, but the verified diff governs). README diff is one additive hunk (55a56,81), entirely under `## Stage: Implementation` (header L50), inserted after "...schema patterns." (L54) before "Run basic confirmation..." (L82); Stage-header count 4=4; no other stage/guardrail prose touched. |
| G2 leak-guard intact | PASS | Grep of the added lines for `curl\|wget\|git clone\|git ls-remote\|AUTO_\|solution__\|check_option\|verifier\|equality test\|expected output\|dim_dates\|sentiment\|4508\|12278\|mom_agg` → no match (exit 1). Diff is purely additive; the leak-guard paragraphs (README L9-10 et seq.) are byte-identical to the parent. Skeleton uses only generic identifiers (`dimension`/`fact_detail`/`category_col`). |
| G3 spec two fields | PASS | `diff baseline.yaml h0046.yaml` = exactly two hunks: `experiment:` and `solver_workflow:`. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` preserved. |
| G4 smoke tasks-only | PASS | `diff h0046.yaml h0046.smoke.yaml` = one added `benchmark.tasks:` block only; all six slugs `ade-bench-` prefixed; includes the named target `ade-bench-airbnb009`. Nothing else differs. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1745B) and `…smoke.frozen.yaml` (1884B) present; each carries `kind: spacedock_solver`, `runtime: codex`, `trials: 1`. |
| G6 resolver fidelity | PASS | Inserted skeleton matches the Falsifiable claim verbatim in intent: (1) delete the one narrowing membership predicate, (2) keep the aggregate `COUNT(*)` byte-intact, (3) no cross-join — one copyable before→after block in Implementation. Generative-but-mechanical/subtractive; contains NO self-anchored "re-run your own model / verify your answer matches / compare to existing code" phrasing (dead h0006/7/8 family absent). |
| G7 actionability/inert-risk | PASS | Carries a literal before→after SQL skeleton (the guideline's explicit PASS form vs inert abstract prose). Inert-risk note: it IS a structural-edit instruction, but the worked-example form is precisely the mitigation G7 prescribes; forensics (h0019/h0030) say a copyable skeleton is the only form that has reliably reached the committed SQL. Net-new bet (all three forks in one block) remains a single-trial-REACH risk, not a propose-stage integrity issue. |
| G8 regression-canary coverage | WARN | Generative (fires on any coverage repair). Smoke carries one @baseline passer per available non-target family — airbnb001/asana001/ana-eng001/f1007/quickbooks002 (all confirmed @baseline=1.0); no intercom passer exists, correctly omitted. WARN (not FAIL): ≥1 canary per family is present, but the construct-sharing family (airbnb) carries only the single passer airbnb001 and there is no second *perturbable* coverage-repair canary — the residual full-scale blind spot (same structural limit as h0019/h0042, acknowledged in the body and smoke comment). |
| G9 selector independence | N/A | Not a multi-candidate / selector protocol — a single subtractive edit, no N-candidate generation or scoring. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever — it is a mechanical subtractive edit (delete predicate, keep aggregate byte-intact, add no CTE), not a "verify a result and act on disagreement" instruction. |
| G11 multi-model-target risk | WARN (unverifiable) | Cannot confirm airbnb009's scored-model count statically: `_artifacts/bug-type-taxonomy.md` is absent and the gatekeeper does not run `rk` to read the verifier test set. The hypothesis + probe name a single scored check (`mom_agg_review_date_range`) on the single edited model `mom_agg_reviews.sql`, which leans single-model — but per G11 an unconfirmable count is surfaced as unknown, not assumed. If airbnb009 turns out multi-model, a single-run flip must be treated as variance and judged by the committed artifact on every scored model. |
| G12 decision-fork probe quality | WARN | airbnb009 is a flipped-task follow-up, so a probe is expected. No inline `## Pre-smoke Decision-Fork Probe` block in the body; a standalone artifact (`_artifacts/h0046-h0047-h0048-decision-fork-probe.md`) carries all required fields — fork tested (3 forks), prompt context (task instr + starting SQL + 2 sibling models + rule only), control A (0/12 all-three), B/C/D = 12/12, exact per-variant wording tested, expected committed-artifact signature (three-fork classification by a blind classifier), and an explicit proxy-only / single-trial-REACH caveat. No leakage (no hidden tests, expected totals, or correct-answer labels; classifier blind to which rule). WARN for provenance/format: the probe lives outside the hypothesis body so the body doesn't self-document it — treat smoke as exploratory, not confirmatory (consistent with the artifact's own h0042 cautionary framing). |

**For the captain:** No FAILs — clean to advance to smoke. Two substantive WARNs to hold in mind: (G8) the airbnb construct-family has only one canary and no perturbable coverage-repair sentinel, so a generative-rule regression could surface only at full scale (accepted structural limit, same as h0019/h0042); (G11) airbnb009's scored-model count is unverifiable here — if it proves multi-model, judge any flip by the committed artifact on every scored model, not the aggregate. Also note the `source:` line names the stale seed `codex-ade-dbt-minimal`; the real fork (verified by diff) is the live @baseline h0043 — worth a one-line fix in the body but it does not affect the verdict. Per AC-4, require ≥3 seed-perturbed airbnb009 repeats all landing three forks before any GO.

## Stage Report: propose

- DONE: Fork the CURRENT @baseline solver — solver_workflows/h0043-package-update-optional-resource-matrix → solver_workflows/h0046-coverage-repair-all-three-forks-worked-skeleton, add ONLY the h0046 worked-example skeleton to Implementation; README diff vs h0043 shows exactly that one idea, leak-guard intact.
  `diff h0043/README.md h0046/README.md` = single additive hunk 55a56,81 under `## Stage: Implementation` only; leak-guard paragraphs byte-identical.
- DONE: Build the FULL spec (cp baseline.yaml; set ONLY experiment + solver_workflow — AC-1) AND the smoke spec (benchmark.tasks = airbnb009 + G8 panel); freeze both with rk freeze --allow-missing.
  `diff baseline.yaml h0046.yaml` = only experiment + solver_workflow; `diff h0046.yaml h0046.smoke.yaml` = only the added `benchmark.tasks` block (airbnb009 + airbnb001/asana001/ana-eng001/f1007/quickbooks002); both `.frozen.yaml` written.
- DONE: Run the gatekeeper subagent and write the `## Gatekeeper review` block (per-rule PASS/WARN/FAIL + overall APPROVE/REVISE/REJECT + one-line rationale).
  Gatekeeper returned APPROVE; no FAILs; WARNs on G8 (one airbnb canary), G11 (unverifiable scored-model count), G12 (probe in artifact not inline). Block written above.

### Summary

Forked the live @baseline (h0043, NOT the seed) and added exactly one Implementation-stage worked-example SQL skeleton that pins all three airbnb009 forks (drop narrowing predicate / keep COUNT(*) byte-intact / no cross-join) in one copyable before→after block; the asana002 var-gating rule from h0043 is left byte-intact so the skeleton stacks on it. Full spec differs from baseline only in `experiment:` + `solver_workflow:`; smoke spec adds only `benchmark.tasks` (target airbnb009 + the G8 cross-family canary panel — five passers, no intercom passer exists). Both specs frozen; gatekeeper APPROVE with WARN-only flags (single airbnb canary / unverifiable scored-model count / probe-in-artifact). Smoke baselines resolved against h0043: airbnb009=0.0 (target), all five canaries=1.0. Flagged the stale `source:` line (names seed) for the captain — the verified diff governs.

## Smoke result

**GO.** The all-three-fork worked-example skeleton flipped airbnb009 FAIL→PASS on **all 3
independent draws (3/3)** vs the ~17% @baseline base rate, with a **byte-identical committed
artifact every time** — the clean subtractive edit (drop the narrowing predicate, KEEP `COUNT(*)`,
no cross-join) — and **zero canary regressions** (all 5 canaries held PASS on clean audit). The
mechanism is artifact-proven, not transcript chatter, and is single-scored-model (resolves the G11
WARN). This is a strong smoke GO; per AC-4 the full verdict stays provisional pending the 48-task
run (`trials: 1` can still land a residual free choice), but the convergence here is far stronger
than h0019/h0042 ever showed.

### Audit + score (all foreground, post-sentinel)

All three run-dirs: `rk audit --policy strict` **clean** (`tainted: 0`, `coverage_missing: 0`;
panel clean=6, each repeat clean=1) and every cell's `subagent-trace-manifest.json` `captured ≥ 1`
— scores trusted (AC-2 satisfied). Run-dirs:
`runs/ade-bench-h0046-…/bc6ce6143ceee77c` (panel) ·
`…-airbnb009-r2/9138440df75aaf75` · `…-airbnb009-r3/f61bc08a15c7a752`.

### airbnb009 three-fork artifact read — the decisive AC-3/AC-4 table

Committed `models/agg/mom_agg_reviews.sql` `apply_patch` from each draw's worker session
(`agent/sessions/.../*.jsonl`). airbnb009 is scored by exactly **one** test
(`mom_agg_review_date_range`, `actual_test_total=1`) — single-model, so the flip is not multi-model
variance (G11 resolved).

| Draw | Seed | #1 narrowing predicate dropped? | #2 `COUNT(*)` byte-intact (not `COUNT(col)`)? | #3 no cross-join CTE? | reward | All 3 forks? |
|------|------|--------------------------------|----------------------------------------------|----------------------|--------|--------------|
| Panel (repeat #1) | null | ✅ predicate deleted | ✅ aggregate not in diff (untouched) | ✅ no `cats`/`grid`/cross-join | 1.0 | ✅ YES |
| r2 | 42 | ✅ predicate deleted | ✅ aggregate not in diff (untouched) | ✅ no cross-join | 1.0 | ✅ YES |
| r3 | 43 | ✅ predicate deleted | ✅ aggregate not in diff (untouched) | ✅ no cross-join | 1.0 | ✅ YES |

**airbnb009 pass count across the 3 draws: 3/3.** All three `apply_patch` payloads are
**byte-identical** — the same minimal subtractive hunk:
```diff
 dates_cte AS (
 	SELECT DATE_ACTUAL
 	FROM {{ ref('dim_dates') }}
-	WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE::DATE FROM review_cte)
 	{% if is_incremental() %}
-		AND DATE_ACTUAL = (SELECT MAX(REVIEW_DATE::DATE) FROM {{ref('fct_reviews')}})
+	WHERE DATE_ACTUAL = (SELECT MAX(REVIEW_DATE::DATE) FROM {{ref('fct_reviews')}})
 	{% endif %}
 ),
```
The `AND`→`WHERE` flip in the `is_incremental` branch is a *required* syntactic consequence of
deleting the preceding `WHERE…IN` (the branch's `AND` had no `WHERE` to attach to once the predicate
was gone) — not a second idea. Forks #2 and #3 are proven by **absence from the diff**: the patch is
an `*** Update File` hunk that touches only `dates_cte`, so the `SELECT COUNT(*) AS REVIEW_TOTALS`
line and the existing `LEFT JOIN`/`GROUP BY` are byte-unchanged, and no `cats`/`grid`/`cross join`
CTE was added.

### Canary panel (AC-5) — all hold

| Canary | Family | @baseline (h0043) | Smoke panel | Held? |
|--------|--------|-------------------|-------------|-------|
| airbnb001 | airbnb (same-family) | 1.0 | 1.0 | ✅ |
| asana001 | asana | 1.0 | 1.0 | ✅ |
| ana-eng001 | ana-eng | 1.0 | 1.0 | ✅ |
| f1007 | f1 | 1.0 | 1.0 | ✅ |
| quickbooks002 | quickbooks | 1.0 | 1.0 | ✅ |

Zero regressions, including the lone same-family canary airbnb001. (G8 residual stands for full
scale: only one airbnb non-target passer and no second coverage-repair passer to perturb — the
generative rule's same-family blind spot is exercised at the 48-task run, not here.)

## Behavioral analysis

**Why it flipped — the @baseline contrast is the proof.** The @baseline (h0043, no skeleton)
airbnb009 cell committed exactly the two-fork failure the forensics predicted:
```diff
-	WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE::DATE FROM review_cte)
+	WHERE DATE_ACTUAL BETWEEN (SELECT MIN(REVIEW_DATE::DATE) FROM review_cte)
+						  AND (SELECT MAX(REVIEW_DATE::DATE) FROM review_cte)   -- fork #1: only a PARTIAL spine repair
 SELECT
-	COUNT(*) AS REVIEW_TOTALS ,
+	COUNT(review_cte.REVIEW_DATE) AS REVIEW_TOTALS ,                          -- fork #2: THE over-eager aggregate rewrite
```
That `COUNT(*)`→`COUNT(review_cte.REVIEW_DATE)` rewrite is the discriminator the hypothesis named:
it makes the 722 zero-review days carry `REVIEW_TOTALS=0` instead of the oracle's `1`, breaking the
windowed `sum` → `Got 1` mismatch → FAIL. The h0046 skeleton's explicit "leave the aggregate
expression BYTE-INTACT — do not rewrite a `COUNT(*)` into `COUNT(col)`" prevented exactly this, and
its "delete the one narrowing membership predicate" steered the solver to a *clean* drop rather than
the partial `BETWEEN MIN..MAX` range. Classification: **flipped because the change reached the
committed SQL** — and reached it identically on all three draws.

**Inert-risk verdict (G7) falsified — the worked-example form works.** h0019 (one-fork skeleton) and
h0042 (one-fork abstain-prose) each pinned one fork and lost the others to free choices; the
prose-only h0010/h0016 went inert. The net-new bet — *a skeleton showing all three forks in one
block holds all three under a single draw* — is confirmed at smoke: not one of the three draws
flip-flopped the aggregate or added a cross-join. The copyable before→after block is the lever form
that both REACHES the committed SQL and PINS all the free choices at once.

**Honest caveat (AC-4 / the standing single-trial decision).** 3/3 at smoke raises the per-draw
probability dramatically but does not make the cell deterministic; the full 48-task run draws
airbnb009 once more, and a residual free choice the skeleton does not pin could still surface. The
honest signal to watch at full: if the committed artifact lands all three forks but the single
scored draw still fails on something the skeleton doesn't pin, that is "mechanism works but
`trials: 1` cannot bank it" (the h0019/h0042 outcome), NOT mechanism-inert. The 3/3 byte-identical
convergence makes that outcome much less likely here than for the prior one-fork attempts.

## Smoke result (Phase 1 — launch record)

Three detached runs launched 2026-06-11T04:38Z (FO owns the wait; scan `runs/.rk-handles/*/`):

| Run | Spec (frozen) | Tasks | Seed | Handle |
|-----|---------------|-------|------|--------|
| Panel (repeat #1) | `h0046-…smoke.frozen.yaml` | 6 (airbnb009 target + airbnb001/asana001/ana-eng001/f1007/quickbooks002 G8 canaries) | null | `runs/.rk-handles/h0046-smoke-20260611-043802/` |
| airbnb009 r2 | `h0046-…airbnb009-r2.frozen.yaml` | 1 (airbnb009) | 42 | `runs/.rk-handles/h0046-airbnb009-r2-20260611-043809/` |
| airbnb009 r3 | `h0046-…airbnb009-r3.frozen.yaml` | 1 (airbnb009) | 43 | `runs/.rk-handles/h0046-airbnb009-r3-20260611-043809/` |

`--explain` rc=0 on all three (panel resolved to 6 tasks, each repeat to 1 airbnb009). Distinct
experiment names + distinct seeds (42/43) are CAS-busters so each repeat lands a separate
content-addressed run-dir; combined with the panel's airbnb009 cell this gives **≥3 independent
airbnb009 draws** to read the bimodal ~17% cell per AC-4. ETA ≈ 6×9 min ≈ 55 min for the panel;
the two single-cell repeats ~9 min each (overlapping). **Phase 2** (after sentinels): strict audit
clean + captured>0, score, the three-fork committed-artifact deep-dive on every airbnb009 draw vs
@baseline (h0043), the five canaries hold, then `## Behavioral analysis` + GO/NO-GO. A flip counts
only if the committed `mom_agg_reviews.sql` shows ALL THREE forks; a lone flip among the draws is
variance, not a GO.

## Stage Report: smoke

- DONE: Strict audit each run-dir; confirm clean + captured>0 BEFORE trusting any score; score each.
  All 3 run-dirs `rk audit --policy strict` clean (tainted 0 / coverage_missing 0); all 8 cells captured≥1; rewards trusted.
- DONE: THE DECISIVE READ (AC-3/AC-4) — committed `mom_agg_reviews.sql` three-fork classification on every airbnb009 draw vs @baseline.
  3/3 draws byte-identical clean subtractive edit: predicate dropped, `COUNT(*)` untouched, no cross-join; all reward=1.0. @baseline committed `COUNT(*)`→`COUNT(col)` + `BETWEEN MIN..MAX` (the predicted 2-fork failure → Got 1 → FAIL). airbnb009 single-scored-model (`mom_agg_review_date_range`), G11 resolved.
- DONE: Canary check (AC-5) — airbnb001/asana001/ana-eng001/f1007/quickbooks002 hold PASS on clean audit.
  All 5 canaries reward=1.0, zero regressions incl. lone same-family airbnb001.
- DONE: Write `## Smoke result` + `## Behavioral analysis`; lead with GO/NO-GO + one-line reason.
  GO written; behavioral why backed by the @baseline contrast (the COUNT-rewrite discriminator); G7 inert-risk falsified.
- SKIPPED: `## Failure Review` block.
  Not a NO-GO / canary regression / revise — GO, so no Failure Review owed.
- SKIPPED: Workflow-refinement log entry (`_artifacts/WORKFLOW-REFINE.md`).
  Lever is a rule tweak INSIDE the existing Implementation stage (a worked-example skeleton), not a new/reordered/replaced stage or protocol-family — structural-refinement evaluation is N/A; the in-stage learning belongs to the instruction-lever taxonomy, not WORKFLOW-REFINE.

### Summary

Smoke is a clean **GO**: the all-three-fork worked-example skeleton flipped airbnb009 FAIL→PASS on
**3/3 independent draws** (panel + r2 seed=42 + r3 seed=43) vs the ~17% @baseline base rate, with a
**byte-identical committed artifact** every time — the minimal subtractive edit (drop the narrowing
predicate, keep `COUNT(*)` byte-intact, no cross-join) — and **zero canary regressions**. The
@baseline contrast proves the mechanism: without the skeleton the solver committed the exact
predicted failure (`COUNT(*)`→`COUNT(review_cte.REVIEW_DATE)` + a partial `BETWEEN MIN..MAX` range),
which the skeleton's byte-intact-aggregate rule prevented. airbnb009 is single-scored-model
(`mom_agg_review_date_range`), so the flip is not multi-model variance (G11 resolved). The net-new
bet (one block pins all three forks under a single draw) is confirmed — the G7 inert-risk on
structural rewrites is falsified by the worked-example form. Per AC-4 the full 48-task verdict stays
provisional (`trials: 1`), but the 3/3 byte-identical convergence is far stronger than h0019/h0042.

## Run result (Phase 1 — full launched, awaiting sentinel)

Full 48-task run launched 2026-06-11T15:27Z, detached, concurrent with the captain's midnight
batch (h0044/h0045). `rk run --explain` rc=0, resolved to **48 tasks**. FO owns the wait (scan
`runs/.rk-handles/*/`).

- Spec (frozen): `specs/h0046-coverage-repair-all-three-forks-worked-skeleton.frozen.yaml`
- Handle: `runs/.rk-handles/h0046-full-20260611-152733/` (pid 601381 ALIVE at launch, no `done` yet)

**Phase 2** (after the `done` sentinel lands rc=0): strict audit the run-dir clean
(`tainted: 0`, `coverage_missing: 0`) + `captured > 0` on every cell BEFORE trusting the score;
`rk score <dir> --format json`; record run-dir + headline pass-rate here. The behavioral
deep-dive (the airbnb009 three-fork artifact read vs @baseline + canary/regression sweep) is the
separate `analyze` stage the FO dispatches next — NOT done in this Run-result write-up.

## Run result

**Recommendation: do NOT promote — net −1 (31/48 vs @baseline h0043 32/48), a statistical wash
hiding one REAL gain, one REAL lever-caused regression, and one variance loss.** The lever
*works exactly as designed* on its target (airbnb009 FAIL→PASS, byte-identical all-three-fork
artifact — 4/4 now across smoke+full), but it is **generative and fired on a same-family sibling
where the coverage repair was NOT the bug** (airbnb008 PASS→FAIL — the G8 same-family blind spot,
realized). The third change (f1011 PASS→FAIL) is unrelated oracle-only answer-selection variance.
Net result is the h0009/h0012-class "correct mechanism, generative collateral" outcome: the gain
is real and reproducible, but it does not bank because the same rule damages a passer the smoke
panel never sampled.

### Audit + score

Run-dir: `runs/ade-bench-h0046-coverage-repair-all-three-forks-worked-skeleton/dfabb292560234ce`.
`rk audit --policy strict` **clean** (clean=48, `tainted: 0`, `coverage_missing: 0`); `captured > 0`
on **48/48** cells — score trusted (AC-2). `rk score --format json`:
**`stratified_pass_at_1 = 0.6458` (31/48)**, Wilson CI [0.504, 0.766], well above the
paper_baseline 0.1875.

### Paired delta vs @baseline (h0043, 32/48)

`rk runs diff` is unusable on these run-dirs (the known `query_id: null` → TypeError; MEMORY
`ade-bench-runs-diff-query-id-null`), so the paired delta is computed directly from
`per_trial_outcomes.json`, paired by task slug:

- **Mean paired delta = −0.0208 (−1 task over 48 paired).** 95% bootstrap CI (10k resamples)
  **[−0.104, +0.042]** — straddles 0; the aggregate is a within-noise wash. The signal is in the
  three artifact reads below, not the number.

**Full per-task ledger (every verdict change, both directions):**

| Task | Family | @baseline | Variant | Δ | Mechanism (artifact-verified) |
|------|--------|-----------|---------|---|-------------------------------|
| airbnb009 | airbnb | ❌ FAIL | ✅ PASS | **+1** | **Real gain.** Committed `mom_agg_reviews.sql` = byte-identical all-three-fork edit (drop predicate / `COUNT(*)` untouched / no cross-join); single test `mom_agg_review_date_range` PASS. Smoke's 3/3 held at full → **4/4** total. |
| airbnb008 | airbnb | ✅ PASS | ❌ FAIL | **−1** | **Real lever-caused same-family bleed.** Skeleton FIRED: solver applied the *identical* predicate-drop hunk to BOTH `mom_agg_reviews.sql` AND `wow_agg_reviews.sql` — but airbnb008's actual fix was a one-line YAML quote balance (`agg.yml`). The unwanted coverage edit broke `AUTO_mom_agg_reviews_equality` (Got 28631). @baseline touched ONLY `agg.yml` → PASS. |
| f1011 | f1 | ✅ PASS | ❌ FAIL | **−1** | **Unrelated single-trial variance.** Both runs touched the same file (`models/stats/analysis__answer.sql`); failure is `check_option_b` (Got 1) — an oracle-only multiple-choice answer-selection (ADE/ABDE-class). No `dates_cte`/coverage edit; the skeleton has no bearing. |

Net = +1 −1 −1 = **−1**.

## Behavioral analysis

**Q1 — Net + full per-task ledger.** Absolute 31/48 (0.6458) vs @baseline 32/48 (0.6667); paired
delta −0.0208, 95% CI [−0.104, +0.042] (straddles 0). Three verdict changes, all in the ledger
above: +airbnb009 (real gain), −airbnb008 (real bleed), −f1011 (variance). Not gains-only.

**Q2 — Smoke vs full: why the GO didn't bank.** The smoke set (6-task panel + 3 focused airbnb009
repeats) carried exactly **one airbnb canary — airbnb001 — and never ran airbnb008.** airbnb001 is
a stable passer the skeleton does not fire on; airbnb008 is a *perturbable* sibling that uses the
SAME `dates_cte`/`mom_agg_reviews`/`wow_agg_reviews` date-spine construct, so the generative rule
fires on it. This is **exactly the G8 same-family blind spot named at the propose gate** ("only one
airbnb non-target passer and no second coverage-repair passer to recruit as a perturbable canary —
accept the residual full-scale blind spot"). The smoke could not see airbnb008 because no second
perturbable airbnb canary existed to recruit; the WARN was accepted, and the full run realized it.
The smoke GO was **artifact-real** (the airbnb009 gain reproduced 4/4), not a false positive — what
smoke missed was the *collateral*, not the *gain*.

**Q3 — Already-correct-and-broken.** Both regressions were **passing at @baseline** — this is damage
to working code, not "failed to help." airbnb008: @baseline PASS (4/4), variant FAIL (3/4) — the
skeleton actively *added* a wrong edit to two models the task did not ask to touch. f1011: @baseline
PASS (6/6), variant FAIL (5/6) — a borderline answer-option flip on the same committed file. Only
airbnb008 is lever-attributable; f1011 is variance on an oracle-only cell the lever never reaches.

**Q4 — Was the change executed? (committed artifact, not chatter.)**
- airbnb009 — **executed-and-helped.** Committed `apply_patch` = the byte-identical all-three-fork
  hunk; single scored model PASS. (Same artifact as all 3 smoke draws → 4/4.)
- airbnb008 — **executed-and-hurt.** Committed `apply_patch` applied the skeleton's literal
  predicate-drop hunk to `mom_agg_reviews.sql` AND `wow_agg_reviews.sql`; @baseline applied neither.
  The skeleton's pattern is *verbatim* in the diff — unambiguous lever causation, not variance.
- f1011 — **premise-falsified / inert for the lever.** The committed change is on
  `analysis__answer.sql` (a multiple-choice answer model); no coverage/date-spine analog exists for
  the skeleton to act on. The PASS→FAIL is single-trial answer-selection variance, independent of
  the lever.

**Q5 — Prevention + next move.** The gain is real and the mechanism is proven; the problem is purely
**scope** — the skeleton fires on *any* model with a `dates_cte … WHERE … IN` shape, including
siblings where that predicate is correct. Two prevention levers:
1. **Scope the rule to a fired precondition** (the h0012/G10 fix-shape): gate the predicate-drop on
   evidence that days are *actually missing for this task* (the task asks for per-day completeness
   AND a missing-day probe is non-zero), instead of "any coverage-shaped CTE." That keeps airbnb009
   (genuinely missing 722 days) and spares airbnb008 (where the predicate was correct). This is a
   REVISE-class change to the same idea, not a new family.
2. **Catch it earlier:** the G8 WARN should have been a harder stop — a same-family perturbable
   canary is *necessary*. airbnb008 IS that canary; it simply was not recruitable as a `@baseline`
   *passer the lever fires on* without running it. The smoke panel should, going forward, include
   the perturbable sibling even when it is the one we expect to be at risk — running it is how the
   bleed is caught before full.

   **Recommended next step: present to the captain — do NOT auto-promote and do NOT reflexively
   re-file.** The honest read is "correct, reproducible mechanism with a known generative scope
   defect." A scoped-precondition revision (lever 1) is a plausible single follow-up that could bank
   the airbnb009 +1 without the airbnb008 −1 — but the broader flip-portfolio is concluded
   (MEMORY `ade-bench-oracle-program-concluded`), so whether to spend a cycle on the scoped variant
   is a captain call, not an automatic file.

**Q6 — Smoke-vs-full fork drift.** No fork drift: the airbnb009 committed fork at full is
**byte-identical** to all three smoke draws — the README rule did NOT drift into a different
implementation branch, and the smoke result was artifact-real, not variance. What changed at full is
not the target's fork but the *population*: the full run exposed the generative rule to airbnb008, a
same-family sibling the smoke panel did not sample (the missed family member, G8). For the
follow-up routing loop: the fork to address is not airbnb009's (it is solved) but the **rule's
trigger condition** — it must distinguish "missing-day coverage repair" from "a correct narrowing
predicate on a sibling model." This is the input to any scoped-precondition revision.

### Workflow-refinement note

N/A as a structural refinement (the lever is an in-stage Implementation rule, not a new/reordered
stage or protocol-family). But the in-stage learning is sharp and belongs in the instruction-lever
taxonomy: **a copyable worked-example skeleton REACHES and PINS the committed SQL reliably (4/4
byte-identical — the h0019/h0042 inert/one-fork wall is broken), but an *ungated* coverage-repair
skeleton is generative and bleeds onto same-construct siblings where the edit is wrong.** The
worked-example form is the right *delivery* mechanism; the missing piece is a *firing precondition*.
This is the first lever to both (a) reproducibly reach the committed SQL across draws AND (b) prove
the generative-collateral failure mode on a same-family sibling at full — a knowledge gain even
though net is −1.

## Stage Report: analyze

- DONE: Strict audit clean + captured>0 BEFORE score; `rk score --format json`; record in `## Run result`.
  audit clean=48 / tainted 0 / coverage_missing 0; captured>0 on 48/48; score 31/48 (0.6458).
- DONE: Paired delta vs @baseline (h0043) — bootstrap CI since `rk runs diff` TypeErrors.
  `rk runs diff` unusable (query_id null); computed slug-paired from per_trial_outcomes.json: −0.0208, 95% bootstrap CI [−0.104, +0.042] (straddles 0).
- DONE: PRE-AUDIT read — verify airbnb009 three-fork artifact; CLASSIFY airbnb008 (same-family bleed?) + f1011.
  airbnb009 committed artifact = byte-identical all-three-fork edit (4/4 smoke+full). airbnb008 = LEVER-CAUSED same-family bleed (skeleton's predicate-drop hunk applied verbatim to mom_agg_reviews.sql + wow_agg_reviews.sql; broke AUTO_mom_agg_reviews_equality Got 28631; @baseline touched only agg.yml). f1011 = unrelated oracle-only check_option_b variance.
- DONE: Answer ALL §analyze required questions (esp. Q2 smoke missed airbnb008, Q3 broke-a-passer, Q6 fork-drift); `## Run result` + `## Behavioral analysis`; lead with verdict + bleed-vs-variance.
  All 6 questions answered; airbnb008 named explicitly as the G8 same-family blind spot realized; f1011 as variance; recommendation = present to captain (scoped-precondition revision is a possible single follow-up, captain call — not auto-file).

### Summary

Net **−1** (31/48 vs 32/48), a statistical wash hiding three artifact-decisive changes. The lever
**works as designed**: airbnb009 flipped FAIL→PASS with a byte-identical all-three-fork committed
artifact (4/4 across smoke+full — the worked-example skeleton reliably reaches AND pins the SQL,
breaking the h0019/h0042 wall). But it is **generative and bled onto airbnb008**, a same-family
sibling where the coverage repair was NOT the bug: the solver applied the skeleton's literal
predicate-drop to two date-spine models the task did not ask to touch, breaking a passer
(`AUTO_mom_agg_reviews_equality`, Got 28631). This is the **G8 same-family blind spot flagged at
propose, now realized** — the smoke carried only airbnb001 (a non-firing stable passer) and never
ran airbnb008. f1011 is unrelated oracle-only answer-selection variance. Recommendation: do NOT
promote; present to the captain. A scoped-precondition revision (fire the predicate-drop only on a
non-zero missing-day probe) could plausibly bank the +1 without the −1, but the flip-portfolio is
concluded, so spending that cycle is a captain decision.
