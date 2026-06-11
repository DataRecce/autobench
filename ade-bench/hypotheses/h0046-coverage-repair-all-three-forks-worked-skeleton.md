---
title: Implementation — a coverage-repair worked-example skeleton that pins ALL THREE forks at once (drop the narrowing date-spine predicate, keep COUNT(*) byte-intact, do NOT cross-join the secondary category) in one copyable before→after block
status: smoke
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

## Smoke result (Phase 1 — launched, awaiting sentinels)

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
