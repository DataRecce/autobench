---
id: dab0007
title: gpt-5.5 xhigh baseline anchor (concurrency 4)
status: conclude
kind: hypothesis
source: captain request 2026-06-16 — establish the codex/gpt-5.5 reference at xhigh reasoning
started: 2026-06-16T21:24:17Z
completed: 2026-06-17T02:37:27Z
verdict: rejected
score:
worktree:
---

## Hypothesis

This is a **baseline anchor**, not a solver-README lever. It re-runs the codex/gpt-5.5 solver on
the **unchanged seed baseline README** (`../solver_workflows/spacedock-readme-baseline`) across all
12 datasets / 54 queries, to establish a clean gpt-5.5 reference point at the **xhigh** reasoning
tier — matching the Opus incumbent's `xhigh` setting (the Opus `@baseline` was run as
`spacedock-opus-4-8-xhigh-hint`).

It differs from the prior anchor (`specs/dab-anchor-codex.yaml`, gpt-5.5 @ high) in exactly two
knobs:

- `agent.reasoning_effort: high → xhigh`
- `concurrency.trials: 2 → 4` (throughput only; `trials: 1` unchanged — single run per cell)

The solver README, model (gpt-5.5), runtime (codex), dataset set, hints, and `data_root` are all
held fixed. No README change ⇒ no leak-guard / smoke needed; this follows the README's
**anchor / first-run skips smoke** path (direct full run).

There is no FAIL→PASS flip claim — the deliverable is the run-dir + its clean-audited stratified
Pass@1, read against the current Opus `@baseline` (~0.65 / 0.6536) and the prior gpt-5.5 @ high
anchor (`codex-dab-baseline`).

## Acceptance criteria

**AC-1 — The full spec differs from `specs/dab-anchor-codex.yaml` only in `experiment:`,
`agent.reasoning_effort` (xhigh), and `concurrency.trials` (4).**
Verified by: `diff specs/dab-anchor-codex.yaml specs/dab0007-gpt55-baseline-xhigh.yaml`.

**AC-2 — The recorded stratified Pass@1 is paired with a clean strict audit on the same run-dir.**
Verified by: `rk score <run-dir>` cites `rk audit <run-dir> --policy strict`.

**AC-3 — All 12 datasets / 54 query-cells ran** (no silent dataset/query drop).
Verified by: `rk run --explain` on the frozen spec shows the full cell list before launch; the
scored run-dir reports 54 cells.

## Run plan (anchor — for the full-stage ensign)

1. `cp specs/dab-anchor-codex.yaml specs/dab0007-gpt55-baseline-xhigh.yaml`; set
   `experiment: dab0007-gpt55-baseline-xhigh`, `agent.reasoning_effort: xhigh`,
   `concurrency.trials: 4`. Leave `solver_workflow: ./solver_workflows/spacedock-readme-baseline`
   (baseline README — this is an anchor, NOT a forked variant).
2. `uv run --project ../razorback rk freeze --allow-missing specs/dab0007-gpt55-baseline-xhigh.yaml`.
3. `uv run --project ../razorback rk run specs/dab0007-gpt55-baseline-xhigh.frozen.yaml --explain`
   ($0, foreground) — confirm all 12 datasets / 54 cells survive.
4. Launch DETACHED (never foreground): `drivers/rk-run-detached.sh dab0007-full
   specs/dab0007-gpt55-baseline-xhigh.frozen.yaml run`. Return the handle path
   (`runs/.rk-handles/dab0007-full-<ts>/`) immediately; do NOT wait for the run.

## Run result

**Run-dir:** `runs/dab0007-gpt55-baseline-xhigh/9b0a658e2274cb22` (gpt-5.5, `reasoning_effort=xhigh`,
12 datasets / 54 query-cells, `trials:1`, concurrency 4).

**Headline:** stratified Pass@1 = **0.6002** (54/54 completed, **0 errored**) — **below** the Opus-4.8
`@baseline` incumbent **0.6536** (`runs/opus-4-8-baseline/e14e49869e6412de`). Paired delta
(stratified) = **−0.053**; per-cell unstratified delta = −0.037 (Opus 37/54 → xhigh 35/54), 95%
paired bootstrap CI **[−0.148, +0.074]** (10k resamples, straddles zero). McNemar discordants:
6 regressions vs 4 gains. This is a within-noise wobble, *under* the incumbent — **not** a promote
candidate. `rk runs diff` not used (known query_id=null crash on these dirs); delta computed from
per-cell `verifier_result.rewards.reward`.

**AC-2 clean-audit attestation:** `rk audit <run-dir> --policy strict` = **53/54 clean, 1 tainted**
(`PATENTS-q3__hg7rEct`, category `forbidden_lookup`: the codex agent ran `docker ps …` at session
jsonl lines 226/236 probing for the DB container). That cell scored **0.0 regardless** and the probe
returned nothing useful → benign behavioral note, **no score inflation**.

### 3-way per-dataset table (pass-rate = n_pass / n_completed)

| Dataset | Opus@base (xhigh) | gpt5.5 @high | gpt5.5 @xhigh (this) |
|---|---|---|---|
| DEPS_DEV_V1 | 1/2 = 0.500 | 0/2 = 0.000 | 1/2 = 0.500 |
| GITHUB_REPOS | 1/4 = 0.250 | 1/4 = 0.250 | 1/4 = 0.250 |
| PANCANCER_ATLAS | 2/3 = 0.667 | 0/3 = 0.000 | 1/3 = 0.333 |
| PATENTS | 0/3 = 0.000 | 0/3 = 0.000 | 0/3 = 0.000 |
| agnews | 1/4 = 0.250 | 2/4 = 0.500 | 1/4 = 0.250 |
| bookreview | 3/3 = 1.000 | 2/2 = 1.000¹ | 3/3 = 1.000 |
| crmarenapro | 10/13 = 0.769 | 11/13 = 0.846 | 10/13 = 0.769 |
| googlelocal | 3/4 = 0.750 | 3/4 = 0.750 | 2/4 = 0.500 |
| music_brainz_20k | 3/3 = 1.000 | 3/3 = 1.000 | 3/3 = 1.000 |
| stockindex | 3/3 = 1.000 | 3/3 = 1.000 | 3/3 = 1.000 |
| stockmarket | 4/5 = 0.800 | 4/5 = 0.800 | 3/5 = 0.600 |
| yelp | 6/7 = 0.857 | 6/7 = 0.857 | 7/7 = 1.000 |
| **stratified Pass@1** | **0.6536** | **0.5836** (53 cells, 1 err) | **0.6002** (54 cells, 0 err) |

¹ @high `bookreview` scored n=2 (one cell errored — `n_errored=1`), so its stratified total is over
53 completed cells, not 54. Account for this when reading "high vs xhigh": xhigh is +0.017 over @high
stratified, but part of that is xhigh having a clean 54/54 vs @high's 53/54.

### Full per-query ledger — EVERY cell whose verdict differs from Opus `@baseline` (both directions)

Reward 1.0 = PASS, 0.0 = FAIL. Distance-to-pass = the DAB validator's `test-stdout.txt` line.

**GAINS (Opus FAIL → xhigh PASS) — 4 cells:**

| Cell | Opus | xhigh | Distance-to-pass (now passing) / committed artifact |
|---|---|---|---|
| GITHUB_REPOS-q4 | 0.0 | 1.0 | validator clean; committed top-5 repos `apple/swift, twbs/bootstrap, Microsoft/vscode, facebook/react, tensorflow/tensorflow` matched. |
| crmarenapro-q3 | 0.0 | 1.0 | validator clean; committed `Negotiation` matched expected stage. |
| googlelocal-q2 | 0.0 | 1.0 | validator clean; committed name+rating list matched. |
| yelp-q6 | 0.0 | 1.0 | validator clean; committed `Coffee House Too Cafe` + category string matched (yelp 7/7 — the one cell Opus & @high both missed). |

**REGRESSIONS (Opus PASS → xhigh FAIL) — 6 cells (all genuine; `exception_info` empty on all):**

| Cell | Opus | xhigh | Validator distance-to-pass | Committed artifact (what xhigh wrote) |
|---|---|---|---|---|
| PANCANCER_ATLAS-q3 | 1.0 | 0.0 | `No value in LLM output matches 305.12, 305.1, or 305` | `"UNABLE TO DETERMINE"` — abandoned the chi-square computation. |
| GITHUB_REPOS-q3 | 1.0 | 0.0 | `Number 1077 not found in LLM output` | committed `0` — count query produced an empty/zero result (filter logic wrong). |
| googlelocal-q3 | 1.0 | 0.0 | `Missing business name: TACOS LA CABANA` | `"UNABLE TO DETERMINE"` — abandoned the open-after-6PM top-5 query. |
| googlelocal-q4 | 1.0 | 0.0 | `Missing business name: Encino Dermatology & Laser` | `"UNABLE TO DETERMINE"` — abandoned the 2019 high-rating-count query. |
| stockmarket-q3 | 1.0 | 0.0 | `No number found near name: Apex Global Brands Inc` | name buried in self-generated marketing prose (`"Apex Global Brands Inc. specializes in creating and marketing… : 23781.42…"`) → validator's name→number proximity regex can't bind the number to the bare name. |
| crmarenapro-q13 | 1.0 | 0.0 | `Found agent IDs ['005Wt000003NEa3IAG'], but expected '005Wt000003NIXCIA4'` | committed `#005Wt000003NEa3IAG` — wrong agent **and** the leading `#` corruption (per the hint) not stripped. |

Note the per-dataset table can mask cell-level churn: GITHUB_REPOS (1/4 both) is a SWAP (Opus passed q3,
xhigh passed q4); crmarenapro (10/13 both) is a SWAP (Opus passed q13, xhigh passed q3). Net dataset
rate identical but different cells. The dispatch's KEY-DATA hint listed PANCANCER-q1, googlelocal-q3/q4,
stockmarket-q3/q4 as regressions; the authoritative per-cell diff vs the *Opus* run-dir is the ledger
above — PANCANCER **q3** (not q1) regressed, GITHUB_REPOS-q3 regressed, crmarenapro-q13 regressed; and
stockmarket has only **one** Opus→xhigh regression (q3), not two (q4 was already FAIL at Opus, so q4 is
not a verdict change vs `@baseline`).

## Behavioral analysis

**Framing (CRITICAL — the confound is fully resolved here).** dab0007 is an **anchor baseline with NO
solver-README lever**: it runs the *unchanged* seed baseline README. So the entire delta vs Opus is
attributable to exactly two knobs — the **model swap (Opus-4.8 → gpt-5.5)** and the **reasoning-effort
tier (the prior gpt-5.5 anchor was @high; this is @xhigh)**. There is **no README wording** that could
have moved any committed answer. Every verdict change below is therefore classified
**model-swap-attributable** by construction; the artifact reads below explain the *mechanism* of each
flip, not a lever attribution.

**Method adherence.** All 54 cells executed the README's prescribed orchestration: the codex
first-officer dispatched a `spacedock:ensign` worker that ran the dataset stage sequence and wrote
`/workspace/answers.json` (confirmed in the session jsonls). The pipeline is healthy — 0 errored, the
postgres/mongo infra fixes held (no Healthcheck/permission failures this run). The recurring *behavioral*
weakness is self-grading: on the give-up cells the ensign's verify stage reported `Verdict: PASSED`
while the committed answer was `"UNABLE TO DETERMINE"` (e.g. PANCANCER-q3) — the same self-anchored
false-green pattern the ade-bench side documented.

**Gains (vs Opus) — why they now pass:**
- **yelp-q6, GITHUB_REPOS-q4, crmarenapro-q3, googlelocal-q2** — the validator reports clean and the
  committed artifact matched the expected value. yelp-q6 is the genuine new win (Opus *and* @high both
  missed it → yelp goes 7/7). The other three are intra-dataset coin-flips: GITHUB_REPOS and crmarenapro
  net to the same dataset rate (a different cell passed). Mechanism: gpt-5.5 reached a correct SQL
  formulation on these where Opus did not — a model-behavior difference, not a method difference.
- **Recoveries vs the prior @high anchor (not vs Opus):** DEPS_DEV_V1 0/2→1/2 and PANCANCER_ATLAS
  0/3→1/3 (q2 recovered). The @high anchor scored these datasets 0.000 largely due to the dab-postgres
  startup/restart issue; at xhigh with the restart fix in place those cells completed and PANCANCER-q2
  passed. This is an infra-fix + tier effect, not a regression/gain vs the Opus incumbent.

**Regressions (vs Opus) — committed-artifact mechanism, all genuine (no infra error):**
1. **PANCANCER_ATLAS-q3** — *gave up.* Hard multi-step chi-square (exclude marginals ≤10, female BRCA,
   reliable mutations). gpt-5.5 committed `"UNABLE TO DETERMINE"`; validator wanted 305.12/305.1/305.
   Damage to a passer: Opus completed this computation. Mechanism = model abandoned a hard analytic chain.
2. **googlelocal-q3** and **googlelocal-q4** — *gave up.* Both committed `"UNABLE TO DETERMINE"` on the
   join+filter+top-N business queries (open-after-6PM; 2019 high-rating counts). Validator: missing the
   expected business name. Two passers broken on one dataset (googlelocal 3/4→2/4). Mechanism = model
   gave up rather than producing a wrong-but-shaped answer.
3. **stockmarket-q3** — *output-contract / verbosity failure.* The query logic looked plausible but the
   agent wrapped each company name in a long self-generated marketing description, so the validator's
   "number near the bare name" proximity match failed (`No number found near name: Apex Global Brands
   Inc`). Mechanism = gpt-5.5 verbosity broke the validator's name→value binding — a formatting break, not
   a wrong number.
4. **GITHUB_REPOS-q3** — *wrong count.* Committed `0` where the truth is `1077` (Shell + Apache-2.0
   commit-message filter). The multi-table join / language-primary filter produced an empty set.
   Mechanism = query-logic error (empty result).
5. **crmarenapro-q13** — *corruption-handling miss.* Committed `#005Wt000003NEa3IAG`: both the wrong agent
   (expected `005Wt000003NIXCIA4`) AND the leading-`#` corruption left un-stripped, despite the explicit
   "~25% of ID-like fields may include a leading #" hint. Mechanism = model did not apply the documented
   ID-normalization, picked the wrong top-sales agent.

**Required analyze questions:**
1. **Net + full ledger** — answered above: stratified 0.6002 vs `@baseline` 0.6536 (Δ −0.053, per-cell
   Δ −0.037, 95% CI [−0.148, +0.074]); 4 gains / 6 regressions enumerated both directions with mechanisms.
2. **Smoke vs full** — N/A: anchor / first-run path **skips smoke** (no README change ⇒ no leak-guard).
   There is no smoke GO to reconcile against.
3. **Already-correct-and-broken** — Yes: all 6 regressions were **passing at Opus `@baseline`** and broke
   here (PANCANCER-q3, GITHUB_REPOS-q3, googlelocal-q3, googlelocal-q4, stockmarket-q3, crmarenapro-q13).
   This is damage to working answers, not merely "failed to help." But it is **model-swap damage**, not a
   lever side-effect — there is no lever.
4. **Was the change executed? (confound attribution)** — There is **no README change to execute**; the
   confound is fully collapsed onto the model+tier swap. Every flip is **model-swap-attributable** by
   construction. Artifact-verified (not chatter): gains matched the validator value; regressions are
   `"UNABLE TO DETERMINE"` (give-ups), `0` (wrong count), verbose-prose name burial, or un-normalized `#`.
5. **Prevention + next move** — see Verdict. The give-up + verbose-prose failure modes are the two
   highest-yield README-lever targets if the loop wants to *improve* gpt-5.5: (a) a "never commit UNABLE
   TO DETERMINE — commit your best computed value" instruction, and (b) an output-contract rule to emit
   bare `name: value` pairs with no prose. The corruption-normalization miss (crmarenapro-q13) is a third.
6. **Smoke-vs-full fork drift** — N/A (no smoke stage for an anchor).

## Verdict

**ANALYZE-ONLY — no promote, no registry write** (per dispatch and per workflow: this is an anchor, and
0.6002 < incumbent 0.6536). gpt-5.5 @xhigh on the unchanged baseline README scores **0.6002 stratified,
clean 54/54 (0 errored), strict audit 53/54 clean** (1 benign `forbidden_lookup` taint on a 0.0 cell).
That is **−0.053 below** the Opus-4.8 `@baseline` (0.6536), within the paired-bootstrap noise floor
(CI [−0.148, +0.074] crosses zero) but on the **wrong side** of the incumbent, with **6 regressions vs
4 gains** — a net loss driven by the model swap, not a lever.

**Confound note:** because there is no README lever, the −0.053 is 100% attributable to the model swap
(Opus-4.8 → gpt-5.5) plus the reasoning tier. The behavioral signature of the loss is consistent:
gpt-5.5 **gives up** on hard analytic queries (`"UNABLE TO DETERMINE"` on PANCANCER-q3, googlelocal-q3/q4)
and **over-narrates** its output (stockmarket-q3 verbose prose broke the validator's name→value match),
where Opus committed a computed value in the validator-readable shape.

**Recommended next move (captain decides — do NOT auto-file):** Opus-4.8 @xhigh **remains the better
anchor** and should stay the `@baseline`. gpt-5.5 @xhigh is a *worse* base model on DAB and is **not** a
promote candidate. The reasoning-tier bump high→xhigh did **not** lift gpt-5.5 above the incumbent
(0.5836→0.6002 is mostly the clean 54/54 + the postgres-restart recovery, not a real reasoning gain). If
the loop wants to pursue gpt-5.5, the productive path is **solver-README levers targeting its two
characteristic failure modes** — (1) forbid `"UNABLE TO DETERMINE"`/force a best-effort committed value,
(2) bare `name: value` output contract — smoked on the give-up + verbose cells. Otherwise, treat this as a
banked knowledge gain (gpt-5.5 underperforms Opus on DAB; the gap is give-ups + verbosity, not infra) and
move on.

## Stage Report: full

- DONE: Spec prepared + frozen; `diff specs/dab-anchor-codex.yaml specs/dab0007-gpt55-baseline-xhigh.yaml` shows ONLY experiment=dab0007-gpt55-baseline-xhigh, agent.reasoning_effort=xhigh, concurrency.trials=4 (AC-1).
  Diff = exactly 3 hunks (lines 3/8/38); solver_workflow stays `solver_workflows/spacedock-readme-baseline`; all 12 tasks intact in frozen spec.
- DONE: rk run --explain confirms all 12 datasets / 54 query-cells survive before launch (AC-3).
  `rk run ...frozen.yaml --explain` reports `- Tasks: 54`; sample task `DEPS_DEV_V1-q1`; awk count of `benchmark.tasks` = 12 datasets.
- DONE: Detached full run launched via drivers/rk-run-detached.sh; handle path returned.
  `drivers/rk-run-detached.sh dab0007-full specs/dab0007-gpt55-baseline-xhigh.frozen.yaml run` → handle `runs/.rk-handles/dab0007-full-20260616-181559` (pid 801782, alive; `done` sentinel absent = in progress). Did NOT wait — FO owns the wait.

### Summary

Anchor spec built by copying `dab-anchor-codex.yaml` and changing exactly three knobs (experiment, reasoning_effort high→xhigh, concurrency.trials 2→4); baseline README, model gpt-5.5, codex runtime, 12 tasks, hints, and data_root all held fixed — no README change, so no smoke/gatekeeper (anchor path). Frozen and --explain confirmed 12 datasets / 54 cells. Launched detached at handle `runs/.rk-handles/dab0007-full-20260616-181559`; specs committed (cb6e82b), runs/ gitignored. Run is long (30 min–8 hr+); first officer owns the wait via the handle's `done` sentinel.

## Stage Report: analyze

- DONE: Write ## Run result — stratified 0.6002 (54/54, 0 errored), 3-way per-dataset table (Opus 0.6536 / @high 0.5836 / @xhigh 0.6002), full both-direction per-query ledger with validator distance-to-pass.
  Score from `rk score <run-dir> --format json` = 0.6002136; per-cell rewards from each `result.json` verifier_result; 4 gains + 6 regressions enumerated.
- DONE: Cite clean-audit attestation (AC-2): strict audit 53/54 clean, 1 tainted (PATENTS-q3 forbidden_lookup, benign).
  `rk audit <run-dir> --policy strict` summary parsed: 54 trials, 53 clean, 1 tainted (PATENTS-q3 docker-ps probe, lines 226/236, scored 0.0).
- DONE: Write ## Behavioral analysis — read transcripts/validator for each verdict-changed cell, classified each; gains (yelp 7/7 + DEPS/PANCANCER-q2 recoveries vs @high) and 6 genuine regressions (mechanism per cell).
  Committed artifacts read from session jsonls: PANCANCER-q3/googlelocal-q3/q4 = "UNABLE TO DETERMINE"; GITHUB-q3 = `0`; stockmarket-q3 = name buried in prose; crmarenapro-q13 = wrong agent + un-stripped `#`.
- DONE: Answer the analyze required questions + plain-words captain summary + framing (all delta = MODEL SWAP, no README lever) + PATENTS-q3 benign note + next move.
  All 6 required questions answered inline in ## Behavioral analysis; ## Verdict carries the plain-words recommendation (keep Opus as @baseline; do NOT promote).

### Summary

Analyzed the completed gpt-5.5 @xhigh anchor: stratified 0.6002, clean 54/54 (0 errored), strict audit 53/54 clean (1 benign forbidden_lookup taint on a 0.0 cell) — **−0.053 BELOW** the Opus-4.8 @baseline 0.6536, within bootstrap noise (CI [−0.148,+0.074]) but on the wrong side, with 6 regressions vs 4 gains. Because this is an anchor with NO README lever, 100% of the delta is the model swap + tier: the loss signature is gpt-5.5 GIVING UP on hard analytic queries ("UNABLE TO DETERMINE") and OVER-NARRATING output (breaking the validator's name→value match), where Opus committed a validator-readable value. Verdict = analyze-only, no promote/registry write; recommend Opus-4.8 @xhigh stays @baseline.

## Follow-up Routing

**Captain verdict (2026-06-17): REJECTED.** gpt-5.5 @xhigh (0.6002) is below the Opus-4.8 incumbent
(0.6536); not a promote candidate. `@baseline` stays the Opus-4.8 run. dab0007 is retained as the
**gpt-5.5 @xhigh reference run** for the loop (the solver tier the hypotheses smoke against).

**Routing = `escalate → pivot`.** Do NOT auto-file a follow-up anchor. The productive direction (captain-
directed) is **solver-README levers targeting the FLIPPED tasks** — queries gpt-5.5 has demonstrably
passed in some run but fails at the xhigh reference (agnews-q4, stockmarket-q4, crmarenapro-q2/q8,
googlelocal-q3). The two highest-yield levers from `_artifacts/opus-vs-gpt55-failure-behavior.md`:
(A) anti-abstention + environment-persistence (forbid `UNABLE TO DETERMINE`; exhaust every named
connection path before concluding a source is absent), and (B) tie/degenerate-result as a
disambiguation signal. These are pursued as new hypotheses, smoke-verified for *consistency* on the
flipped tasks. Sibling tier-control dab0008 deferred to a midnight run.
