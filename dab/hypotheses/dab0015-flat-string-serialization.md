---
id: dab0015
title: googlelocal-q2 - pin flat-string serialization (no JSON) for list answers
status: full
kind: hypothesis
source: dab0001 output-contract concept, re-targeted — the DECORATION sub-problem (stockmarket-q3) is dead via README (dab0012 REJECTED, _artifacts/readme-cannot-suppress-output-shape.md); this tests the distinct SERIALIZATION-FORMAT sub-problem, which is a deliberated structural choice rather than an un-perceived reflex
started: 2026-06-18T11:40:00Z
score: 0.5
---

## Hypothesis

The dab0012 boundary proved that README cannot suppress a **reflex** — gpt adds content (entity
descriptions) it does not perceive as wrong. But `googlelocal-q2` is a different failure class: the model
computes the **correct** businesses (Elite Massage 5.0, Angel-A 4.33…) yet serializes them as a **JSON
list-of-dicts** when the verifier wants a flat `name - rating; …` string (gpt ~2/6; log-audited in the
dab0001 concept). Choosing JSON-vs-flat-string is a **deliberated representation choice**, not an
un-perceived reflex — and "format the output as a flat string, not JSON" is the kind of instruction models
follow far more reliably than "withhold helpful content." So the README-inert boundary may NOT transfer to
serialization-format, and the cell is a 2/6 **coin-flip** (a choice it already sometimes gets right), not a
0/6 wall — we are *stabilizing* a choice, the cheaper bet.

**The README change** (fork `spacedock-readme-baseline` → `dab0015-flat-string-serialization`), ONE idea, in
the answer-format section:

> **Write the answer to `answers.json` as a plain flat string — never JSON.** Do not emit arrays, objects,
> key names, or brackets (`[ ] { }`) or quoted field labels. If the answer is a list of items, write them
> as a flat delimited string in the order and field-form the question implies (e.g. `Item A - 4.5; Item B -
> 4.3`), not as a list of dicts.
>
> *(consequence-framing, stated truthfully):* `answers.json` is read by an automated string-matcher, not a
> human — it looks for your answer in the expected flat text form. A JSON / structured / bracketed answer
> will not match and scores zero, even when the values inside it are correct.
>
> Worked example (foreign domain): for "list the top 2 cafes and their ratings," write
> `Blue Bottle - 4.6; Stumptown - 4.4` — NOT `[{"name":"Blue Bottle","rating":4.6}, …]`.

Foreign-domain example only (no target schema leaked). The consequence-framing attaches the format to
**correctness** (matcher fails on structure), not to style ("no commentary") — the framing the dead cycles
lacked.

## Acceptance criteria (falsifiable)

- **GO** iff `googlelocal-q2` flips/stabilizes to PASS **by committed artifact** (the committed answer is a
  flat `name - rating; …` string, not JSON) AND no canary drops — judged per-cell vs
  `_artifacts/baseline-variance-6draw.md`, never single-draw. Because the cell is a 2/6 coin-flip, "GO"
  means the committed artifact shows the flat-string form was adopted *and* the cell passes; a single
  unexplained pass is not enough.
- **NO-GO / falsified** if the committed `googlelocal-q2` answer is still JSON (the serialization rule is
  inert like the decoration rules → the WHOLE output-contract concept is dead, not just decoration) OR any
  perturbable list-answer canary drops (the flat-string rule mis-fires on a cell that needs a different
  shape → the rule is not safe).
- **Boundary value:** either outcome closes the question. GO = the reflex-vs-deliberated distinction is real
  and output-contract survives on serialization; NO-GO = README is inert for output-shape of *any* class,
  and the dab0001 concept is fully, honestly dead.

## Target queries

Primary: `googlelocal-q2` (gpt ~2/6). Generative lever (fires on every list answer) → smoke needs the G8
regression panel: ≥2 PERTURBABLE list-answer canaries (passers whose answer is a list the rule fires on —
e.g. `yelp-q6` 4/6) + ≥1 cross-dataset sentinel from a perfect-score dataset (e.g. `music_brainz_20k-q1`
6/6). Avoid Mongo/Postgres-backed cells if those backends are flaky at launch.

## Smoke set (propose stage)

The dispatch suggested `yelp-q6` (4/6) as the perturbable list canary, but its ground truth is a
**single comma-separated row** (`Coffee House Too Cafe, Restaurants, …`) — a one-item answer, not the
multi-row `name - value` list shape this lever most directly fires on. I substituted two **cleaner
multi-row list-answer canaries** whose GT is exactly the target's shape, so the G8 panel is genuinely
*perturbable*:

- `googlelocal-q4` (5/6, GT = `name,count` rows) — same dataset + shape as the target; the strongest
  "does the rule mis-fire on a list that already passes?" tripwire.
- `yelp-q7` (5/6, GT = list of category rows) — cross-dataset (Mongo+DuckDB-backed) perturbable list
  canary, so a list-shape regression on a *different* backend is also caught.

Plus the scalar sentinel `music_brainz_20k-q1` (6/6, GT = `1059.46`) from a perfect-score dataset: the
rule explicitly leaves single scalars unchanged, so this proves the lever does not perturb non-list
answers.

| Task | @baseline (Opus-4.8) | gpt-5.5 6-draw band | Should pass in smoke? | Role / why we picked it |
|------|----------------------|---------------------|-----------------------|-------------------------|
| `googlelocal-q2` | ❌ FAIL (0.0) | 2/6 (coin-flip) | 🎯 want it to flip to PASS | Target — gpt computes the right businesses but serializes as JSON list-of-dicts; the rule pins flat `name - rating` so the matcher's name+nearby-number search hits. |
| `googlelocal-q4` | ✅ PASS (1.0) | 5/6 | ✅ must stay PASS | Perturbable list canary (same dataset + `name,value` shape) — regression tripwire if the flat-string rule mis-fires on a list that already passes. |
| `yelp-q7` | ✅ PASS (1.0) | 5/6 | ✅ must stay PASS | Perturbable list canary (cross-dataset, Mongo+DuckDB) — catches a list-shape regression on a different backend. |
| `music_brainz_20k-q1` | ✅ PASS (1.0) | 6/6 | ✅ must stay PASS | Scalar sentinel (perfect-score dataset) — the rule leaves scalars unchanged; proves no over-fire on non-list answers. |

Net hoped-for: flip `googlelocal-q2` to PASS (by committed flat-string artifact), lose zero canaries/sentinel.
Surviving set confirmed via `rk run …smoke.frozen.yaml --explain` → `Tasks: 4` (14 materialized − 10
`exclude_tasks` = the 4 above). **Backends healthy at launch:** `dab-postgres` (`pg_isready` →
*accepting connections*; googlelocal review/business) and `dab-mongo` (`ping` → ok; yelp businessinfo)
both UP — the cycle-1 `Connection refused` risk does not apply at this launch. ETA ~4 query-cells.

## Verifier-integrity note (consequence-framing)

`googlelocal-q2`'s `validate.py` does `llm_output.find(name)` (substring search for each exact business
name) then scans the **10 characters after the name** for a `\d+\.\d+` score. So a JSON answer like
`[{"name":"Elite Massage","rating":5.0}]` finds the name but the next 10 chars are `","rating"` — no
bare decimal in the window → score-mismatch → 0, even though `5.0` is present elsewhere. A flat
`Elite Massage - 5.0` puts the score right after the name → matches. The README's consequence-framing is
therefore **truthful and NOT overstated**: it says the matcher "searches your text for each expected
name and a nearby numeric value" and that brackets/keys between name and value break that match — it does
**not** claim a strict char-exact compare.

## Gatekeeper review

**Recommendation: APPROVE** — single-idea flat-string format pin in the Answers section, integrity rules clean, generative G8 panel carries 2 perturbable list canaries + a scalar sentinel, and the consequence-framing is truthful to the substring+nearby-number matcher.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-18T14:20:00Z.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | Parent = `spacedock-readme-baseline` (README diff clean against it; matches `source:`). Diff is one hunk `89a90,107`: an 18-line block appended to the **Answers** section only — the flat-string-not-JSON pin + consequence-framing + foreign-domain worked example. No other stage (model/analyze/verify) or leak-guard prose touched. |
| G2 leak-guard intact | PASS | `grep ground_truth\|db_description_withhint\|curl\|wget\|git clone` over the README hits only line 71 (`Do NOT access validate.py or ground_truth.csv`) — the **pre-existing** leak-guard rule, byte-identical to parent, NOT in the added block. The "Use only the workspace data" / HuggingFace / no-external-lookup paragraphs are unchanged. Added block introduces no oracle-file read and no withheld-hint paste. |
| G3 spec two fields | PASS | `diff anchor vs full` = exactly two changes: `experiment: dab-anchor-codex → dab0015-flat-string-serialization` and `solver_workflow: ./...spacedock-readme-baseline → ./...dab0015-flat-string-serialization`. `agent.kind: spacedock_solver`, `runtime: codex`, `trials: 1` all preserved. |
| G4 smoke tasks+exclude | PASS | `diff full vs smoke` adds only `benchmark.tasks` (3 dataset names: googlelocal, music_brainz_20k, yelp) + `benchmark.exclude_tasks` (10 q-ids). Nothing else differs. Surviving set = 14 materialized − 10 = **4**: googlelocal-q2 (target, present), googlelocal-q4, yelp-q7, music_brainz_20k-q1 — matches the ensign's `--explain → Tasks: 4`. Target query included; regression sentinels present. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1806 B) and `…smoke.frozen.yaml` (1821 B) exist; each carries `agent.kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text = the claim verbatim (flat string, never JSON; no arrays/objects/brackets/keys; `Item A - 4.5; Item B - 4.3` form; foreign-domain Blue Bottle/Stumptown example). Generative format pin, not self-anchored "re-run/verify your own query". Consequence-framing says the matcher "searches your text for each expected name and a nearby numeric value" — truthful to validate.py's `find(name)` + `\d+\.\d+`-in-next-10-chars; does NOT overstate as strict char-exact. No scope creep. |
| G7 actionability/inert-risk | PASS | Mechanical-substitution + worked-example: a concrete serialization form (`name - value; …`) with a copyable few-shot skeleton, not abstract query-restructuring prose. Low inert-risk. |
| G8 regression-canary coverage | PASS | Generative (fires on every list answer). Surviving non-target @baseline passers (per_trial_outcomes, reward=1.0): googlelocal-q4 (same dataset + multi-row `name,value` shape — perturbable), yelp-q7 (cross-dataset Mongo+DuckDB list — perturbable), music_brainz_20k-q1 (scalar 1059.46 — sentinel, non-perturbable by design). ≥2 perturbable list canaries on the target's construct + a non-target passer → panel satisfied. Target googlelocal-q2 = 0.0 FAIL as stated. |
| G9 selector independence | N/A | No multi-candidate / selector protocol declared. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever — it's a one-shot output-format pin, no "verify result and act on disagreement". |

**For the captain:** Clean APPROVE, no FAILs and no WARNs. The G8 panel is genuinely perturbable (googlelocal-q4 is the strongest tripwire: same dataset + `name,value` list shape the lever fires on), and the matcher consequence-framing was verified truthful against validate.py. Only judgment call to keep in mind: this is the output-contract concept's serialization sub-problem after dab0012 proved the decoration sub-problem README-inert — if googlelocal-q2's committed answer is still JSON the whole concept is dead; if it flips by flat-string artifact the reflex-vs-deliberated distinction holds. Per the acceptance criteria, judge GO by committed flat-string artifact + zero canary drops, not single-draw reward.

## Stage Report: propose

- DONE: ONE knob — flat-string-not-JSON serialization rule added verbatim (flat delimited string, never arrays/objects/keys/brackets; truthful consequence-framing tied to the name+nearby-number matcher; foreign-domain cafes example) in the forked README's `## Answers` section; leak-guard intact; both spec diffs vs anchor show ONLY `experiment:` + `solver_workflow:` (smoke adds `benchmark.tasks` + `benchmark.exclude_tasks`).
  README diff = one hunk `89a90,107` (Answers section only, no stage/leak-guard touched); full-spec diff = 2 fields; smoke-spec diff = tasks+exclude only. Commit 4ee98cd.
- DONE: GENERATIVE-lever smoke set carries the G8 regression panel, confirmed EXACTLY via `rk run --explain` → `Tasks: 4`: target googlelocal-q2 + 2 PERTURBABLE multi-row list canaries (googlelocal-q4 same-dataset, yelp-q7 cross-dataset) + 1 cross-dataset scalar sentinel (music_brainz_20k-q1). Backend health confirmed at launch: dab-postgres `pg_isready` → accepting connections; dab-mongo `ping` → ok.
  Substituted the dispatch's suggested yelp-q6 (single-row GT) with googlelocal-q4 + yelp-q7 (true multi-row `name,value` list GT) so the canaries are genuinely perturbable; rationale in the Smoke set block.
- DONE: gatekeeper subagent ran against the variant artifacts; per-rule PASS/WARN/FAIL table + overall recommendation written into the `## Gatekeeper review` block.
  Recommendation: APPROVE — no FAILs, no WARNs across G1–G10 (G9/G10 N/A); consequence-framing verified truthful against validate.py.

### Summary

Forked `spacedock-readme-baseline` → `dab0015-flat-string-serialization` and added one README idea in `## Answers`: write each answer value as a plain flat string, never JSON, with a truthful consequence-framing (the matcher searches text for each expected name + a nearby numeric value; brackets/keys between name and value break the match — NOT a char-exact-compare claim) and a foreign-domain worked example. Full spec = anchor + the two allowed fields; smoke survives exactly googlelocal-q2 (target) + googlelocal-q4/yelp-q7 (perturbable list canaries) + music_brainz_20k-q1 (scalar sentinel), confirmed via `--explain` (Tasks: 4) with both networked backends healthy. Gatekeeper recommends APPROVE with a clean per-rule table; this propose package is auditable and ready for the captain's smoke gate.

## Smoke result

Run-dir: `runs/dab0015-flat-string-serialization/bddf52340d225cdd` (smoke, trials:1). `rk audit --policy strict` = **CLEAN** (4 clean / 0 tainted, no findings). `rk score` = stratified_pass_at_1 **1.0**, 4/4 cells PASS.

| Task | @baseline | 6-draw band | Smoke reward | Verdict | Committed answer (recovered from codex apply_patch) |
|------|-----------|-------------|--------------|---------|------------------------------------------------------|
| `googlelocal-q2` | ❌ 0.0 | 2/6 coin-flip | ✅ **1.0** | 🎯 FLIPPED | `{"answer":"Angel-A Massage - 4.333333333333333; Aurora Massage - 4.178571428571429; Elite Massage - 5.0; J B Oriental Inc - 4.166666666666667"}` |
| `googlelocal-q4` | ✅ 1.0 | 5/6 | ✅ 1.0 | ✅ HELD | `{"answer":"Encino Dermatology & Laser: Alex Khadavi MD - 19; The Boochyard @ Local Roots - 17; Aurora Massage - 14"}` |
| `yelp-q7` | ✅ 1.0 | 5/6 | ✅ 1.0 | ✅ HELD | `{"answer": "Restaurants - 58; Food - 36; American (New) - 24; Shopping - 20; Breakfast & Brunch - 19"}` |
| `music_brainz_20k-q1` | ✅ 1.0 | 6/6 | ✅ 1.0 | ✅ HELD | `{"answer": "1059.46"}` |

Net: 4/4, target flipped, zero canary/sentinel drops.

## Behavioral analysis

**The flip is the pin being ADOPTED, not coincidental flat output.** Three independent lines of transcript evidence:

1. **Committed artifact is unambiguously flat.** googlelocal-q2's `answer` value is a `name - rating; …`
   flat delimited string — exactly the README form (`Item A - 4.5; Item B - 4.3`), with NO arrays,
   objects, key names, or brackets *inside the value*. All 4 GT businesses present with correct ratings;
   the matcher's `find(name)` + `\d+\.\d+`-within-10-chars succeeds because each rating sits right after
   its name.
2. **The model explicitly acted on the rule.** Its analyze/verify reasoning (subagent rollout
   `…14-21-07…`, lines 107/124) states the answer is "delimited as a single flat string" and its verify
   step records: *"Verified JSON has only `answer`, value is a string, **no brackets/objects inside the
   answer**."* That is the README's flat-string-not-JSON instruction being checked and satisfied, not a
   chance emission — the model named the no-brackets constraint and confirmed compliance.
3. **The rule is shape-aware, not blanket-flatten.** The scalar sentinel
   `music_brainz_20k-q1` committed `1059.46` unchanged (rule leaves single scalars alone), and the two
   multi-row list canaries committed correct flat `name - value` lists — googlelocal-q4 kept the `:`
   that is part of a business *name* ("Encino Dermatology & Laser: Alex Khadavi MD"), so no
   over-flattening / structure-loss. No mis-fire on a cell that needed different shape.

**Why it worked where dab0012 (decoration) failed:** dab0012 tried to suppress an un-perceived *reflex*
(entity descriptions the model doesn't see as wrong) and was README-inert. Serialization-format is a
*deliberated* representation choice — "write a flat string, not JSON" is an instruction gpt-5.5 follows
and self-verifies. The reflex-vs-deliberated distinction is real: **output-contract survives on
serialization-format even though it is dead on decoration.**

**Verdict: candidate GO — committed flat-string artifact confirms the pin was adopted AND all four cells
pass with zero canary drops.** googlelocal-q2 is a 2/6 coin-flip, so per the acceptance criteria the
single 1.0 alone would be variance-suspect; but the artifact + the model's explicit no-brackets
verification raise this above luck. The standing single-trial / judge-by-artifact captain rule
(`ade-bench-single-trial-judge-by-artifact`) is satisfied here: the artifact proves mechanism adoption.
A 1× confirmation draw on googlelocal-q2 would further harden the flip against the coin-flip prior, but
the GO does not depend on it — the artifact is the proof.

## Run result

Run-dir: `runs/dab0015-flat-string-serialization/605aada30f9b8580` (full, all-12, trials:1, ~3h).

- `rk audit --policy strict`: **41 clean / 0 tainted / 13 coverage_missing**. The 13 coverage_missing are the ENTIRE `crmarenapro` dataset (q1–q13) — `subagent-trace-manifest.json` absent because the trial environment never started: `result.json.exception_info` = `RuntimeError: Docker compose command failed … container …-dab-postgres-1 is unhealthy`. No agent ran on any crmarenapro cell.
- `rk score`: stratified Pass@1 = **0.4355** over the 11 datasets that produced results (crmarenapro dropped entirely; 20/54 cells reward=1.0).
- **This headline is INFRA-CORRUPTED and must NOT be read as a board score.** See below.

## Behavioral analysis

**Headline verdict: the full run is INCONCLUSIVE for board-wide regression — a sustained mid-run Postgres outage corrupted the board. The flat-string lever itself is clean: it flipped its target, helped a second cell, and was NOT the cause of any stable-cell failure.**

Walked the unexpected-result-playbook (`_artifacts/unexpected-result-playbook.md`):

### Step 1 — paired diff (matched reference = gpt-5.5 6-draw band, NOT Opus @baseline)
Against Opus @baseline the diff is −17 cells, but that entangles the model swap + the infra outage and is not the right reference. Against the matched gpt-5.5 6-draw band, the cells that fell below band split cleanly into infra vs non-mechanism:

### Step 2-3 — separate infra from behavior (artifact + exception, every moved cell)

**INFRA (excluded from behavioral verdict) — a ~70-min Postgres degradation, 17:08–18:21:**
- All 13 `crmarenapro` (Postgres-backed): compose `dab-postgres unhealthy` → environment never came up → errored, no trace. Includes 9 rock-stable (6/6) cells (q1,q4,q5,q6,q7,q9,q11,q12 + q13). **INFRA, not lever.**
- `bookreview-q3` (6/6 stable): committed `UNABLE TO DETERMINE`; log shows `dab-postgres did not resolve` / `could not translate host name`. **INFRA.**
- `googlelocal-q4` (5/6, a SMOKE-PASS canary): committed `UNABLE TO DETERMINE`; log shows `dab-postgres DNS failure` / `Connection refused` / `could not translate host name`. **INFRA** — the exact cell that PASSED in smoke when PG was up; its full FAIL is the outage, not the rule mis-firing.
- `PANCANCER_ATLAS-q3`, `PATENTS-q3`, `agnews-q2/q3`: PG host-resolution errors in-log (PATENTS/agnews are 0/6 never-pass regardless).

**NOT mechanism-caused (format rule fired correctly; failure is wrong VALUE, not wrong SHAPE):**
- `music_brainz_20k-q1` (6/6): committed flat scalar `601.44` vs GT `1059.46`. The rule leaves scalars unchanged and DID — the answer is correctly shaped, the *number* is wrong. Analytical/sampling variance, not format. (Passed identically-formatted in smoke.)
- `music_brainz_20k-q3` (6/6): committed flat `Groovey by Rich Matteson - 5417.34 USD` — correct flat shape, WRONG song. Analytical variance.
- `GITHUB_REPOS-q4` (6/6): committed flat `torvalds/linux, apple/swift, …` — correct flat shape, missed `tensorflow/tensorflow`. Analytical variance.

**Decisive point for the NO-GO condition:** the falsification trigger was "the flat-string rule over-flattened a list that needed structure." That did NOT happen on any cell. Every cell where the rule fired committed a correctly-formed flat string; the only failures are infra abstains and wrong-value analytical misses on historically-noisy-at-single-trial cells. **No format mis-fire anywhere on the board.**

### Step 4-5 — causation at the honest ceiling
The 3 non-infra stable failures (music_brainz_20k-q1/q3, GITHUB_REPOS-q4) are at most RELATED (single-trial global-prompt perturbation re-rolls the dice, the dab0009 lesson) — but their committed artifacts prove the *format mechanism* is innocent. At single-trial this is not proven causal in either direction; the matched-band read is the ceiling.

### The two GAINS — both mechanism-attributed (artifact + reasoning)
- **`googlelocal-q2`** (target, 2/6 coin-flip): **HELD PASS** at full. Committed the identical flat `Angel-A Massage - 4.333…; Aurora Massage - 4.178…; Elite Massage - 5.0; J B Oriental Inc - 4.166…`; reasoning references "flat delimited"/"flat string". The pin is now adopted across TWO independent draws (smoke + full) — that materially hardens the flip above the 2/6 prior: **pin-adopted-real, not variance.**
- **`yelp-q6`** (4/6): flipped to PASS. Committed flat `Coffee House Too Cafe - Restaurants, Breakfast & Brunch, American (New), Cafes` (single-row list flattened with ` - ` between name and categories), reasoning references the flat-string rule. Mechanism-attributed gain — notably the very cell the dispatch first proposed as a canary.

### Codex-vs-Opus confound
@baseline is Opus; this run is gpt-5.5 + the README rule. Every verdict-changed cell was attributed by committed artifact above: the 2 gains are README-rule-executed-and-helped; the stable failures are infra (PG outage) or wrong-value (model/sampling), never the format rule. A delta with no artifact attribution was not counted.

### Recommendation
**RE-RUN, do not promote or reject on this draw.** The lever's own evidence is positive and clean (target held across two draws with adopted-artifact, a second mechanism-attributed gain, zero format mis-fires), but a ~70-min Postgres degradation erased an entire dataset (crmarenapro, 13 cells) and forced infra abstains on multiple PG-backed passers — so the board-wide regression question this full run exists to answer is unanswerable from it. Re-run the full spec once PG/Mongo health is confirmed stable for the run duration; judge promotion on the clean board.

## Failure Review

- **What happened:** full run scored a headline 0.4355 with many stable cells failing, but `rk audit` shows it is infra-corrupted: 13/54 cells (all of crmarenapro) errored with `container dab-postgres … is unhealthy` and several PG-backed passers (bookreview-q3, googlelocal-q4, PANCANCER-q3) abstained with `could not translate host name` across a ~17:08–18:21 window. This is the recurring `dab-postgres` DNS/health flake compounding a whole-dataset compose failure — NOT the flat-string lever.
- **Lever status:** clean on its own evidence — googlelocal-q2 held PASS (adopted flat artifact, 2 draws); yelp-q6 flipped (mechanism-attributed); no over-flatten / format mis-fire on any cell. The NO-GO falsification condition did not trigger.
- **Next step:** RE-RUN the full spec (`specs/dab0015-flat-string-serialization.frozen.yaml`) after confirming `dab-postgres` + `dab-mongo` are healthy AND verifying the per-trial PG container health check is stable (see memory `dab-mongo-segfault-no-restart-bricks-trial` / `dab-agent-image-nonroot-codex-perm` for the restart-policy fix lineage). Judge promotion on the clean board, against the gpt-5.5 matched band.
