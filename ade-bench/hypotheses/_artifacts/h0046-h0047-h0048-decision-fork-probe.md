# Decision-Fork Probe — h0046 / h0047 / h0048 (airbnb009 three-fork repair)

Date: 2026-06-11
Method: `_artifacts/subagent-decision-fork-probe-method.md` (subagent decision-fork probe).
Orchestrated as a 96-agent workflow: 12 fresh solver draws × 4 README variants (48 draws),
each committed `mom_agg_reviews.sql` then classified by an **independent, blind** classifier
(does not see which rule produced the SQL) on the three forks. No oracle leakage: subagents
saw only the task instruction, the starting `mom_agg_reviews.sql`, the two sibling models,
and the rule variant — no hidden tests, no expected totals, no "correct answer".

## The fork being measured

airbnb009 passes the hidden `mom_agg_review_date_range` check only when **all three forks land
in the same draw** (proven by the h0042 deep-dive,
`_artifacts/h0042-smoke-vs-full-reproducibility-gap.md`):
1. **spine** — drop the `dates_cte` narrowing predicate `WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE … FROM review_cte)` so the full calendar is present;
2. **aggregate** — keep `COUNT(*)` (NOT `COUNT(review_cte.REVIEW_DATE)` — the column rewrite zeros the 722 no-review days → the discriminator);
3. **shape** — add NO `(days × sentiments)` cross-join; let sentiments emerge from the existing `LEFT JOIN` + `GROUP BY`.

The "preferred branch" measured by the classifier = **all three correct**.

## Result

| Variant | Runs | spine dropped | kept `COUNT(*)` | no cross-join | **all-three (smoke-pass proxy)** |
|---|---:|---:|---:|---:|---:|
| A — control (no coverage rule) | 12 | 12/12 | **0/12** | 9/12 | **0/12 = 0%** |
| B — h0046 worked-example skeleton | 12 | 12/12 | 12/12 | 12/12 | **12/12 = 100%** |
| C — h0047 negative "delete one line, touch nothing else" | 12 | 12/12 | 12/12 | 12/12 | **12/12 = 100%** |
| D — h0048 Exploration protect-list | 12 | 12/12 | 12/12 | 12/12 | **12/12 = 100%** |

### Control failure mode (the key validation)

Every control draw (12/12) **found and dropped the narrowing spine predicate** — the solver
always locates the bug. But **0/12 kept `COUNT(*)`**: every single unguided draw "tidied up"
the aggregate to `COUNT(review_cte.REVIEW_DATE)` / `COUNT(review_cte.REVIEW_SENTIMENT)`, and
**3/12 also added a `(day × sentiment)` cross-join** (`sentiments_cte … CROSS JOIN`). This
reproduces the exact h0019/h0042 full-run failure mode in the proxy: the failure is **over-eager
cleanup of the aggregate**, fork #2, not an inability to find the bug. The discriminator the
baseline gets wrong 100% of the time is precisely the one all three rules target.

## Interpretation (two layers)

**Proxy result.** All three rules fully suppress both over-edits at the decision-policy level:
0/12 → 12/12 on the aggregate, and no cross-joins. The lift over control is maximal and clean,
and far stronger than h0042's abstract abstain-prose (which the same kind of proxy showed only
moved a 2/2 wrong-rate, and which then failed at full). The probe **validates the three-fork
premise** and shows each wording materially changes the local decision policy on this fork.

**Required real validation.** This is a decision-policy proxy, NOT a pass rate. The proxy CANNOT
measure the one thing that actually killed h0042: **single-trial REACH in the real multi-stage
codex solver** — whether the rule reaches the *committed* artifact on the *one scored draw*.
h0042 is the cautionary precedent: a strong proxy + a 3/3 focused smoke, then a full FAIL because
the single scored full draw landed on the modal wrong branch (airbnb009 is intrinsically bimodal,
~17% pass across 12 historical full runs). The smallest real validation per variant: a focused
`rk` smoke on airbnb009 + the canary panel, **judged by the committed `mom_agg_reviews.sql` on
all three forks**, and — given the cell's bimodality — **≥3 seed-perturbed focused repeats** before
trusting a GO (h0042 AC-4).

### Confidence + which to smoke first

- 12/12 with 0 failures → Rule-of-three 95% CI lower bound ≈ **74%** (not literal certainty).
- The proxy **cannot discriminate** the three (all 100%). Structural reasoning breaks the tie:
  - **h0048 (Exploration protect-list)** carries the LEAST-informative 100%: its own stated risk
    is cross-stage memory (does an Exploration-stage protect-list survive into the Implementation
    edit?). A single-prompt proxy hands the rule to the same context that writes the SQL, so it
    **structurally cannot test that forgetting risk** — its proxy score is inflated relative to its
    real risk.
  - **h0047 (negative constraint)** is prose; prose can be acknowledged-then-skipped at full (the
    G7 inert risk that bit h0042's abstain-prose). Strong proxy, but prose-reach is the open risk.
  - **h0046 (copyable skeleton)** has the strongest independent reason to REACH the committed
    artifact: the forensics record that a *copyable skeleton* is the only form that has reliably
    reached the committed SQL (prose-only levers h0010/h0016 went inert). Its proxy 100% and its
    reach argument point the same way.
- **Recommendation:** if smoking one, **h0046 first**. The proxy de-risks the *decision-policy*
  axis for all three; it does NOT de-risk the *single-trial-reach* axis, which only `rk` smoke
  (with seed-perturbed repeats + committed-artifact classification) can settle.

## Caveats (from the method)

- Estimates local decision tendency, not pass rate.
- Proxy subagents are reasoning LLMs given a clean focused prompt with the rule salient — not the
  multi-stage codex solver; they may over- or under-state branch probability if the real solver's
  context differs.
- Repeated subagents are not a substitute for `trials > 1`.
- A positive probe lowers the cost of deciding what to smoke; it does not skip audit, scoring, or
  committed-artifact inspection in the real run.
