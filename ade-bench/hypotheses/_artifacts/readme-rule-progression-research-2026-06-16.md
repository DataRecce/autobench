# README-Rule Progression & Overfit Research (2026-06-16)

Post-target fine-tune research on the **10 accepted README rules** that took the solver
README from the original baseline (31/48) to the live `@baseline` h0060 (**36/48 = 0.7500
— the 75% target, met**). Sources: the full original→h0060 README diff
(`solver_workflows/codex-ade-dbt-minimal/README.md` → `…/h0060-stabilize-f1-coinflips/README.md`),
the entity files, `round1-round2-flipped-task-choice-map.md` (per-task volatility), and
the program retrospective (`_proposal/retrospective-2026-06-15-program.md`).

Covers the three analysis action items: (1) progression chart — which rule de-flaked which
case; (2) overfit review + simplification per rule; (3) data-modeling vs dbt classification.
Items 4 (pipeline tuning) and 5 (context freezing) are scoped at the end.

---

## 1. Progression chart — which rule de-flaked which case

"De-flaked" = converted a **volatile / coin-flipping** cell (passes some `trials:1` draws,
fails others) into a reliable pass by pinning the locally-correct branch. A task's
**pass-rate across gpt-5.5 run-dirs is the flakiness gauge** — lower = flakier = more value
from pinning. The headline number does NOT rise monotonically per step (the ±3-cell noise
floor masks single gains); construct coverage does. The number moves on *compositions* and
on the final *stabilizers*.

| # | Hyp | Rule added (short) | Target case(s) de-flaked | Pre-rule pass-rate (flakiness) | Baseline after |
|---|-----|--------------------|--------------------------|-------------------------------|----------------|
| — | base | *(incumbent README, 80 lines)* | — | — | **31/48** |
| 1 | h0043 | package optional-resource var-matrix | asana002 | 64% | **32/48** ← first genuine +1 |
| 2 | h0052 | + max(points) · feature-boundary · scoped-coverage | f1006 (52%), f1006-hard (53%), airbnb009 (69%); qb002/004 held | 52–69% | 32/48 (3-lever compose, promoted on 2-draw consistency) |
| 3 | h0056 | + per-key inner-join · lap-exclude-pit · preserve-columns | airbnb005 (89%), airbnb007, f1010-medium (73%), ana-eng003 (94%) | 73–94% | **35/48** ← first +3 |
| 4 | h0058 | + keep-base-id (stabilizer) | quickbooks002 (94%), quickbooks003 (77%) | 77–94% | 35/48 (hold-rate 2/4 → 4/4) |
| 5 | h0059 | + tmp-tier inline + reconcile | asana003 (70%) | 70% | 35/48 (banks asana003 — last bankable flipped-FAIL) |
| 6 | h0060 | + src_<table> naming · top-N tie-crosses-cutoff | f1001 (82%), f1003-hard (87%) | 82–87% | **36/48 = 0.7500** ← 75% target met, 0 regressions |

**Reading the chart.** The flakiest cells (f1006 52%, f1006-hard 53%, airbnb007 24%) were
worth the most to pin; the high-pass-rate cells (ana-eng003 94%, qb002 94%) were *already
mostly passing* and the rule mainly removes the occasional coin-flip loss — i.e. several
later rules are **stabilizers** (raise hold-rate) more than **flips** (move the median). The
two that actually moved the headline were the compositions (h0056: +3) and the final
stabilizer pair (h0060: +1 to 36). The remaining 12 fails are all oracle-blind / never-passed
(ana-eng004/006/007/007-medium, asana004/005/005-hard, f1002, intercom001/002/003,
quickbooks001) — no README rule reaches them (retrospective §5).

---

## 2. Overfit review + simplification (per rule)

Each rule rated for **overfit risk** — does it encode a *general construct* or a *scar from
one task's specific failure*? Battle-damage clauses ("do NOT rewrite COUNT(*) into
COUNT(col)") are the overfit signal: they fix one observed mis-step rather than state a
principle.

| # | Rule | Overfit risk | Why / what to simplify |
|---|------|--------------|------------------------|
| 1 | feature-boundary removal + keep-base-id | **MED** | Sound principle (drop feature-only outputs, keep shared FKs), but ~40 lines of hedging prose (removal vs toggle vs disable paths). The keep-base-id clause is a qb002/003 scar. **Simplify:** collapse the three sub-paragraphs to one principle + the one BEFORE/AFTER skeleton; drop the redundant "search project-local files" prose. |
| 2 | build/rename preserve column set | **LOW** | Clean general principle. Example uses `customer_*` names (mild ana-eng003 anchor). **Simplify:** genericize column names; the explicit cross-ref to the feature-removal carve-out is good (keep). |
| 3 | coverage repair, double-gated | **HIGH** | The longest block (~58 lines) and the most scarred. Core principle (complete the spine only when completeness is asked) is general, but "keep COUNT(*) byte-intact / do not add a cross join of a secondary category" are **airbnb009-specific battle damage**. It is really 3 fused rules. **Simplify:** keep gate(a) intent + gate(b) oracle-free probe (both transferable); demote the byte-intact aggregate/cross-join clauses to a one-line "make the minimal subtractive edit; do not rewrite aggregates or add joins while repairing coverage." |
| 4 | per-key metric inner-join from fact | **LOW** | Best-formed rule on the board. General data-modeling principle (don't emit zero-fact keys as NULL-metric rows), generic identifiers, tight skeleton. Model for the others. No change. |
| 5 | tmp-tier removal inline + reconcile | **MED** | dbt-mechanics (ref→source) wrapped around a transferable gold nugget: the **before==after reconciliation** (oracle-free double-entry). Verbose. **Simplify:** lead with the reconcile principle; the "verbatim inline" instruction is the dbt-specific half and can be one line. |
| 6 | package optional-resource var-matrix | **MED** | Prose-only, no skeleton (historically flagged G7 inert-risk). Specific to the "installed package updated + optional resource disabled" shape (Fivetran). **Simplify/strengthen:** add a minimal disabled-var compile-matrix skeleton, or accept it as narrow and gate it tightly. |
| 7 | max(points) over cumulative standings | **MED** | Principle (cumulative snapshots → max, not sum / not latest-row) is general; framing ("points/standings/race") is F1-flavored. Prose-only. **Simplify:** restate as "for cumulative-snapshot totals, aggregate with max() at the entity grain; do not switch to latest-row/rank/window unless local evidence proves max wrong" — domain-neutral. |
| 8 | lap-time average exclude pit stops | **MED** | Principle (exclude anomalous rows before averaging, don't keep-and-adjust) is general; "pit stops / lap times" is very F1-specific. **Simplify:** generalize to "when an average must exclude a category of rows, filter them out before aggregating; do not retain them and subtract an adjustment," with the lap example as illustration. |
| 9 | src_<table> bare-prefix naming | **HIGHEST** | By construction a **single-task compliance restatement** — the rule itself says "This restates the task's own instruction." Example hard-codes `f1_dataset/circuits`. Pure stabilizer for f1001. **Simplify/flag:** lowest transfer value; keep only because it's cheap and gated to "tasks that ask for `src_` models," but it is the clearest overfit and the first candidate to drop if README length ever costs off-construct cells. |
| 10 | top-N tie-crosses-cutoff | **LOW-MED** | Genuinely general analytical concept (a top-N w/o tiebreaker is nondeterministic only when a tie spans the cutoff). The `count(metric >= Nth) > N` test is clean and locally computable. The "exclude the prompt's worked example (most_fastest_laps)" clause is f1003-hard-specific. **Simplify:** drop the named-example exclusion into a generic "exclude any model the prompt already classifies." |

**Cross-cutting overfit findings:**
- **Battle-damage clauses are the overfit tell.** Rules 3 (byte-intact COUNT/cross-join) and
  9 (one-task restatement) carry the most scar tissue; rules 4 and 10 carry the least.
- **Verbosity ≠ safety.** The longest rules (1, 3) are the most overfit, not the most robust;
  the tightest (4) is the most general. Length is a liability — it both dilutes attention and
  perturbs off-construct cells (the noise-floor mechanism behind flat nets).
- **The transferable cores are extractable.** Under the scar tissue, rules 3/5/7/8/10 each
  contain a one-sentence domain-neutral principle. A simplified README could likely hold the
  same 36/48 at ~half the added length — a testable hypothesis (see §4).

---

## 3. Classification — data-modeling vs dbt

Splits the rules by whether they encode a **transferable data-modeling / analytics
principle** (would help on any SQL benchmark) or a **dbt/Fivetran tooling mechanic** (specific
to this stack).

### Data-modeling / analytics (transferable — 6 rules)
- **#2 preserve column set** — don't silently narrow a projection on a build/rename.
- **#3 coverage / spine completeness** (core) — complete the key/date spine when completeness
  is asked; minimal subtractive edit.
- **#4 per-key inner-join from fact** — don't emit zero-fact keys as NULL-metric rows.
- **#7 max over cumulative snapshots** — cumulative totals aggregate with max, not sum/latest-row.
- **#8 exclude-before-average** — filter anomalous rows out before aggregating, don't keep-and-adjust.
- **#10 top-N tie-crosses-cutoff** — a limit-N without tiebreaker is nondeterministic only at a
  boundary-spanning tie.

### dbt / Fivetran tooling mechanics (stack-specific — 3 rules)
- **#5 tmp-tier ref→source rewire** (the inline-verbatim half; the reconcile half is general).
- **#6 package optional-resource var-matrix** — Fivetran package-migration + dbt var gating.
- **#9 src_<table> naming convention** — dbt staging-layer naming.

### Mixed (1 rule)
- **#1 feature-boundary removal** — the *concept* (remove feature-only outputs, keep base FKs)
  is data-modeling; the *expression* (unwrap `{% if var('using_feature') %}` Jinja guards) is
  dbt-specific.

**Takeaway:** **6.5 of 10 rules are transferable data-modeling principles** that should carry
to any SQL/analytics benchmark (DAB included); the ~3.5 dbt-specific ones (#5 inline, #6, #9,
half of #1) are ade-bench-stack scaffolding and should NOT be ported verbatim — they'd be
re-derived per benchmark from that stack's conventions. This directly informs the new-benchmark
runbook: **seed a new benchmark's README with the 6 modeling principles; re-derive the tooling
rules from the new stack.**

---

## 4. Item 4 — "test ADB pipeline tuning" (scoping, not yet run)

Two readings; both are real and cheap to test once defined:
- **(a) README-simplification test** — the §2 finding that the transferable cores are
  extractable predicts a **shorter README holds 36/48** while perturbing fewer off-construct
  cells. Concrete test: build a simplified README (drop scar clauses in rules 1/3/9, genericize
  7/8/10), run full, confirm ≥36/48 and check whether the noise-floor wobble shrinks. This is
  the highest-value tuning experiment and directly de-risks overfit.
- **(b) solver-param tuning** — the solver config holds knobs held constant all program:
  `reasoning_effort: xhigh`, `max_turns: 200`, `temperature: 0.0`, `override_timeout_sec: 2400`.
  A small sweep (effort, max_turns) on the volatile tail could test whether the noise floor is
  reducible by config rather than by README. Pairs naturally with item 5.

**Recommendation:** run (a) first — it's the post-fine-tune deflake/overfit test the §2 analysis
sets up, and it needs no harness change. Define ADB-tuning's exact target before spending runs.

## 5. Item 5 — "implement context freezing" (existing state + path)

A stub already exists: `specs/context-freexe-test.yaml` (experiment `context-freeze-test`,
`temperature:0.0`, `seed:42`, single-cell on airbnb009). Its own note records the core problem:
the **content-addressed run-dir caches identical inputs**, so a re-run with identical context
"collapsed the first re-run" (returned the cached result instead of a fresh sample) — the
`seed:42` is a "CAS-buster" to force a genuinely-independent draw.

This is the **variance-wall** work in disguise: context freezing aims to make the solver context
deterministic/reproducible so repeated draws are stable — which is exactly what's needed to
*bank* gains against the ±3-cell noise floor and to trust a tightened CI instead of
artifact-forensics (retrospective §3.3 measurement wall; runbook §3/§4). Open questions to
resolve before "implementing":
1. **What is frozen?** The prompt/README + tool transcript + model seed, or also the dbt
   workspace state? Determinism requires pinning everything the solver reads.
2. **CAS interaction** — the content-addressed cache must distinguish "intentional re-run for
   variance measurement" from "cache hit." The seed-buster is a workaround; a first-class
   "force-fresh" flag would be cleaner.
3. **Goal** — reproducibility for *measurement* (run the same cell N times, get a stable
   pass-rate → real multi-trial) vs reproducibility for *determinism* (temp=0 making one draw
   canonical). These need different designs.

**Recommendation:** treat item 5 as the measurement-wall fix the program never landed (the
freeze-repo concurrency race blocked `trials>1`). Scope it as: "make N independent same-context
draws of one cell produce a stable pass-rate," which unblocks both honest banking and item 4(b).

---

## 6. Bottom line

- The 10 rules took the README from 31→**36/48 (75%, target met)**; the headline moved on the
  two compositions (h0056 +3) and the final stabilizer pair (h0060 +1), with the rest raising
  per-cell hold-rate against the noise floor.
- **6.5/10 rules are transferable data-modeling principles**; ~3.5 are dbt-stack scaffolding —
  port the former to new benchmarks, re-derive the latter.
- **Overfit is concentrated in the scar clauses** (rules 3 and 9 worst; 4 and 10 cleanest). A
  simplified README is predicted to hold 36/48 at roughly half the added length — the natural
  item-4(a) test.
- Items 4 and 5 are the **measurement/robustness** frontier: simplify-and-retest the README,
  and implement context freezing to finally beat the variance wall the flip program fought all
  along.

**Cross-refs:** `_proposal/retrospective-2026-06-15-program.md`,
`round1-round2-flipped-task-choice-map.md`, `leverable-flipped-tasks-research-2026-06-13.md`,
`/home/kent/autobench/day-one-runbook.md`; READMEs `solver_workflows/codex-ade-dbt-minimal/`
and `solver_workflows/h0060-stabilize-f1-coinflips/`; live `@baseline`
`runs/ade-bench-h0060-stabilize-f1-coinflips/861d18e790c72047` (36/48 = 0.7500).
</content>
