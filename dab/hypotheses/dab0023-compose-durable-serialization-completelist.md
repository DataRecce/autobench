---
id: dab0023
title: Compose the 2 durable banked levers — flat-string serialization + complete-list/flat-record — into the seed README as pre-verified levers
status: propose
kind: hypothesis
source: "dab0022 PASSED-validated follow-up (captain-directed). dab0022 validated 2 durable, confound-free flips across draws — googlelocal-q2 (flat-string serialization, reconfirming dab0015) and PATENTS-q1 (complete-list + flat simple-record) — but did NOT promote because the single-lever board lift was variance-swamped. This files the composition play: bank both pre-verified mechanisms into the seed README at once (the ade-bench h0049 gated-levers-compose pattern), scoped so they fire only where validated and do not perturb ranking/single-winner cells."
started: 2026-06-23T06:38:33Z
completed:
verdict:
score: 0.5
worktree:
---

## Hypothesis

**Falsifiable claim.** Adding **two pre-verified, scoped banked levers** — (1) a flat-string
serialization rule and (2) a complete-list / flat-record rule — to the seed solver README (fork the
current `@codex-batch-baseline` solver, `solver_workflows/spacedock-readme-baseline-hostfix`) banks the
durable dab0022/dab0015 flips (googlelocal-q2, PATENTS-q1, and any other flat-string / complete-list-shaped
cell) **without regressing the board**, because both mechanisms are already committed-artifact-validated
and are scoped to fire only where they are safe (not on ranking / single-winner cells). This is a
**banking/composition play, NOT a new mechanism** — the h0049 gated-levers-compose pattern
([[ade-bench-gated-levers-compose]]): precondition-gated levers on disjoint construct families compose
additively, the gate IS the isolation.

**The single README change** — add ONE `### Answer serialization & list rules` section with exactly these
two scoped rules (change nothing else; leak-guard prose byte-intact):

```
### Answer serialization & list rules

- Serialize each answer as a flat string of exact database values, not a JSON object/array or nested structure. For a single value, emit the value; for multiple values, emit them as a flat delimited string (e.g. `A; B; C` or `name | code | year`). Do not wrap the answer in JSON, markdown, or quotes-as-data. (Applies to the answer FORMAT only — it does not change which rows you select.)
- For a question that asks for a complete list / every qualifying row ("list all", "which X" with no top-k, "for each"), emit EVERY qualifying row as a flat-delimited record; do not truncate to top-k. This rule fires ONLY on open complete-list questions — for a single-winner question ("which one has the most", "the highest") or an explicit fixed top-k, answer with exactly that one / that k and do NOT broaden the row set or the cohort.
```

**Why these two and why scoped this way:**
- **Flat-string serialization** is the one mechanism validated TWICE: dab0015 (googlelocal-q2 flipped
  across 3 draws — adopted artifact) and dab0022 (googlelocal-q2 4/5 over 5 draws, PATENTS-q1's anchor
  failure was a JSON-list serialization crash the flat-record form fixed). Serialization-FORMAT is
  README-steerable ([[dab-flat-string-serialization-works]]); the DECORATION reflex is not — so the rule
  pins format only, explicitly NOT row selection.
- **Complete-list / flat-record**, SCOPED off single-winner and fixed-top-k questions, is the dab0022
  cycle-2 + cycle-3 scoping lesson made permanent: the un-scoped complete-list/all-associated rule
  regressed stockmarket-q3 (cycle-2, a name+number cell) and is implicated in the yelp-q4/q7 ranking
  wobble; scoping it to open complete-list questions only is what kept the durable PATENTS-q1 flip while
  removing the ranking blast radius.

**Target queries (durable, pre-verified):** googlelocal-q2 (flat-string), PATENTS-q1 (complete-list +
flat-record), plus any other flat-string / open-complete-list-shaped cell the scoped rules safely reach.
**Explicit non-targets (must NOT regress):** ranking / single-winner / fixed-top-k cells — stockmarket
q3/q4, yelp q4/q7, and the crmarenapro/PATENTS variable band (the rules are scoped to NOT fire there).

**Lever class — GENERATIVE but SCOPED.** Both rules fire by question-shape, so propose MUST carry a G8
regression panel: the durable target cells (googlelocal, PATENTS) PLUS the perturbable ranking canaries
the scope is designed to protect (stockmarket, yelp) to PROVE the scope holds — a ranking-cell regression
here means the scope failed, which is the whole falsification point.

## Pre-smoke Decision-Fork Probe

**Skipped — pre-verified banked mechanisms, no new fork to probe.** Both levers are already validated by
committed artifact from prior runs, so there is no novel mechanism whose decision-tendency a probe would
de-risk:
- **Flat-string serialization**: dab0015 CONCLUDED validated (googlelocal-q2 adopted-artifact across 3
  draws); dab0022 reconfirmed it (googlelocal-q2 4/5 over 5 draws, committed-artifact read in
  `runs/dab0022-patents-semistructured-rules/*` — "All names and scores matched", the flat form fixed the
  JSON-vs-flat output gap). See [[dab-flat-string-serialization-works]] and
  [[dab-semistructured-rules-first-real-go]].
- **Complete-list + flat-record (scoped)**: dab0022 cycle-3 proved the scoped form banks PATENTS-q1 (4/5)
  while the cycle-2→cycle-3 scoping fix removed the stockmarket-q3 / yelp ranking regression
  (committed-artifact-confirmed in the dab0022 entity ## Behavioral analysis).
The open question is COMPOSITION + SCOPE-HOLD on the full board (do the two banked cells hold together and
does the scope keep the ranking cells safe), which the smoke + a multi-draw read answer directly — a
decision-fork sim would add nothing over the existing artifact evidence. (If smoke surfaces a specific
committed-artifact fork on a still-moving cell, a probe becomes meaningful for a `smoke → hypothesis`
revision.)

## Acceptance criteria (falsifiable)

**AC-0 — Anchor is the current `@codex-batch-baseline`** (codex/gpt-5.5, high; `rk registry resolve run
@codex-batch-baseline`). Model AND effort held constant → the README is the sole variable (confound-free,
the dab0022-cycle-3 regime). Propose confirms the resolved anchor.

**AC-1 — Exactly the README change; full spec differs from the anchor only in `experiment:` +
`solver_workflow:`** (effort stays `high` to match the anchor — NO xhigh). Verified by `diff`. Leak-guard
prose byte-intact; the added section is the two scoped rules only.

**AC-2 — Every recorded score paired with a clean strict audit** (`rk audit --policy strict`:
`0 coverage_missing`, `0 tainted`; exclude both dab-postgres dual-signatures before any verdict).

**AC-3 — Verdict by committed-artifact + multi-draw hold-rate, NOT a single-draw headline.** Per the
dab0022 calibration lesson (a generative lever's single full draw carries ±0.07; a confound-free executed
cell can still be variable-band), the durable cells must be judged by their ≥2/3 (or ≥3/5) hold-rate
across draws, not one draw's board delta.

**GO** iff the durable banked cells (googlelocal-q2 + PATENTS-q1) **hold across draws** (≥2/3) AND
**zero ranking/single-winner canary regression** (the scope holds — stockmarket q3/q4, yelp q4/q7 not
dragged below anchor by the complete-list rule) AND the board median ≥ anchor. **NO-GO / REJECTED** if the
composed cells don't hold, if the scope leaks (a ranking cell regresses by the complete-list rule, by
committed artifact), or if the board median sits within the ±0.07 noise of the anchor with no durable
attributable gain (the dab0022 outcome — validated-but-not-promotable, in which case CONCLUDE-validated
without moving the seed). **PROMOTE** (move `@codex-batch-baseline` → this README) only on GO with the
durable cells held across a multi-draw confirm — this is the composition's whole point: bank pre-verified
flips into the seed so they STICK.

## Gatekeeper review

**Recommendation: APPROVE** — clean two-bullet scoped composition lever; single stage section added under `## Answers`, leak-guard byte-intact, specs differ only in `experiment:`/`solver_workflow:`, both frozen, and the smoke set carries the perturbable ranking canaries (stockmarket q3/q4, yelp q4/q7) that prove the scope holds.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-23.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff = one hunk (94–98): adds exactly one `### Answer serialization & list rules` subsection under the `## Answers` stage; no other stage/section touched; two bullets = the one composition idea the claim names. |
| G2 leak-guard intact | PASS | Only `ground_truth` hit is pre-existing leak-guard at L75 (outside the added hunk); leak-guard prose L81–87 byte-identical to parent; no `db_description_withhint`/`curl`/`wget`/`git clone` in added lines; added text pins answer FORMAT only, names no oracle/hint file. |
| G3 spec two fields | PASS | `diff` anchor vs full = only `experiment:` + `solver_workflow:` (plus ABOUTME comments); `agent.kind: spacedock_solver`, `runtime: codex`, top-level `trials: 1` preserved (`concurrency.trials:2` is not the G3 `trials`). |
| G4 smoke tasks+exclude | PASS | Smoke diff = narrows `benchmark.tasks` to the 4 needed datasets + adds `exclude_tasks` dropping the other 8 (dataset names, not per-query ids — correct for the plugin selector); `--explain` resolves exactly googlelocal/PATENTS/stockmarket/yelp; both named targets (googlelocal-q2, PATENTS-q1) survive. |
| G5 both frozen | PASS | Both `…frozen.yaml` and `…smoke.frozen.yaml` exist (Jun 23 06:42); each carries `kind: spacedock_solver` + `runtime: codex` (L4–5). |
| G6 resolver fidelity | PASS | Inserted text matches the claim verbatim (bullet 1 = flat-string serialization, format-only; bullet 2 = scoped complete-list off single-winner/fixed-top-k); generative-but-scoped, no self-anchored "verify your own answer" phrasing; no scope creep. |
| G7 actionability/inert-risk | WARN | Bullet 1 is a concrete mechanical serialization edit (flat-string, worked tokens `A; B; C`) — lands reliably. Bullet 2 is a question-shape-gated list-completeness rule (abstract-structural with cue phrases but no worked-example skeleton); inert-risk on the complete-list arm — consider a worked few-shot if PATENTS-q1 doesn't fire in smoke. |
| G8 regression-canary coverage | PASS | Generative-but-scoped (both rules fire by question-shape). Smoke keeps perturbable non-target `@baseline`-PASS canaries from datasets OTHER than the targets: stockmarket q3/q4 (ranking, anchor PASS) and yelp q4/q7 (ranking/complete-list, anchor PASS) — ≥2 perturbable canaries on the ranking construct the complete-list rule could perturb; a regression there is the designed scope-leak tripwire. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — two output-format/list-shape rules, single session. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever — no verify-and-act-on-disagreement instruction. |

**For the captain:** No FAILs — clear to advance to smoke. One thing to watch: the G7 WARN on bullet 2 (complete-list rule is shape-gated abstract prose with no worked skeleton, so it may "talk but not do" on PATENTS-q1) — if smoke shows PATENTS-q1 not flipping, a worked few-shot is the in-place fix. The G8 panel is well-formed: stockmarket q3/q4 + yelp q4/q7 are exactly the perturbable ranking canaries that must stay PASS to prove the scope holds.

### Smoke set (boxed) — `@codex-batch-baseline` rewards resolved (anchor `dab/runs/codex-dab-batch-baseline/bf113446fdd94373`, stratified 0.6965)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ Task         │ Baseline (anchor) │ Should-pass │ Role                                          │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ googlelocal  │ q2 ❌ FAIL        │ 🎯 q2 flip→PASS │ TARGET — flat-string serialization (durable) │
│ PATENTS      │ q1 ❌ FAIL        │ 🎯 q1 flip→PASS │ TARGET — complete-list + flat-record (durable)│
│ stockmarket  │ q3 ✅ q4 ✅       │ ✅ stay PASS    │ CANARY — ranking; scope-hold tripwire         │
│ yelp         │ q4 ✅ q7 ✅       │ ✅ stay PASS    │ CANARY — ranking/complete-list; scope tripwire│
└──────────────────────────────────────────────────────────────────────────────────────────────┘
Net want: +2 targets flip to PASS (googlelocal-q2, PATENTS-q1), 0 canary regressions (the scope holds).
A ranking-canary drop (stockmarket q3/q4 or yelp q4/q7 below anchor) = scope LEAKED = the falsification point.
ETA: 4 datasets in batch mode, concurrency.trials:2 → ~20–40 min wallclock.
Anchor full-board context: googlelocal q1/q3/q4 PASS q2 FAIL; PATENTS q1/q2/q3 all FAIL; stockmarket q1–q5 all PASS; yelp q1–q7 all PASS.
```

## Smoke result

### Smoke run (launched — detached)

- **Handle:** `runs/.rk-handles/dab0023-smoke-20260623-073517` (from `dab/`)
- **PID:** 2719479 (worker alive at launch; `ps` confirmed)
- **Spec:** `specs/dab0023-compose-durable-serialization-completelist.smoke.frozen.yaml`
- **Selection (`--explain`):** 4 datasets — googlelocal + PATENTS (targets), stockmarket + yelp (ranking canaries); model gpt-5.5, `reasoning_effort: high`.
- **Log:** `runs/.rk-handles/dab0023-smoke-20260623-073517/log`; **done sentinel:** `…/done` (absent until finished; then rc/end/rundir).
- **ETA:** ~21 query-cells at high → ~45–50 min wallclock (extrapolated from dab0022 cycle-1 smoke ~44 min for 19 cells). The FO owns the wait + auto-wakeup; not polling.

### Smoke outcome — phase 2 (audit + score + flip/scope table)

**Run:** `runs/dab0023-compose-durable-serialization-completelist/496bc7774f468ff7` (rc=0, ~29 min).
**Audit (AC-2):** `rk audit --policy strict` = **clean 4 / coverage_missing 0 / tainted 0** — no dab-postgres dual-signature, all 4 datasets present. Scores attestable.
**Score:** stratified Pass@1 over the 4 smoke datasets = **0.9143** (n_completed 4, n_errored 0) vs anchor on the same 4-subset **0.6875** → +0.227 on the subset. (Single high draw — not a board number; the full 12-dataset draw is what the gate-to-promote would read.)

**Flip / scope table (by committed artifact vs `@codex-batch-baseline` `bf113446fdd94373`):**

| Cell | Role | Anchor | Variant | Verdict | Attribution (committed artifact) |
|------|------|--------|---------|---------|----------------------------------|
| googlelocal-q2 | 🎯 TARGET (flat-string) | 0.0 FAIL | **1.0 PASS** | **BANKED** | "All names and scores matched successfully" — the flat-string serialization reached the answer. |
| PATENTS-q1 | 🎯 TARGET (complete-list+flat-record) | 0.0 FAIL | **1.0 PASS** | **BANKED** | "All CPC codes present in LLM output" — complete-list+flat-record fired; full CPC set emitted, not truncated. |
| PATENTS-q2 | (bonus, same dataset) | 0.0 FAIL | **1.0 PASS** | bonus flip | "All fuzzy names matched, CPC/year found near each name." |
| PATENTS-q3 | (bonus, same dataset) | 0.0 FAIL | **1.0 PASS** | bonus flip | "All assignee-title pairs matched." PATENTS swept 0/3 → 3/3. |
| stockmarket-q3 | ✅ CANARY (complete-list "for each") | 1.0 PASS | **0.0 FAIL** | **REGRESSED** | NOT row-broadening, NOT format: variant emitted the company **DESCRIPTION blurb** as the name field ("Apex Global Brands Inc. specializes in creating and marketing…: 23781.42; …") where the anchor emitted the clean **NAME** ("Apex Global Brands Inc.: 23781.42; …"). Same rows, same numbers, same `name: num; …` flat shape — wrong COLUMN. Verifier: "No number found near name" (the 200-char blurb pushed the number out of the name's match window). |
| stockmarket-q4 | ✅ CANARY (top-5 single-winner) | 1.0 PASS | 1.0 PASS | HELD | scope held on the explicit top-k cell. |
| yelp-q4 | ✅ CANARY (category avg-star) | 1.0 PASS | **0.0 FAIL** | **REGRESSED (variance)** | NOT a scope leak: variant "Restaurants \| **3.6648**" vs anchor "Restaurants, **3.6407**" — same category, **different computed average** (3.66 vs 3.64); 3.66 rounds past the verifier's tolerance for expected 3.63 while 3.64 matched. The `,`→` \| ` delimiter is the flat-string format and the verifier accepts both; the cause is the underlying number (temp=0 aggregate-grain variance on a borderline-rounding cell — yelp-q4 is confirmed variable-band from dab0022). |
| yelp-q7 | ✅ CANARY (complete-list categories) | 1.0 PASS | 1.0 PASS | HELD | "All categories are present" — complete-list fired correctly on a genuine list cell. |

**Headline:** Both durable targets BANKED by artifact (PATENTS swept 0/3→3/3, googlelocal-q2 flipped). BUT **two canaries regressed** — stockmarket-q3 (a real complete-list-rule interaction: wrong column, see Failure Review) and yelp-q4 (temp=0 variable-band, not the rule).

## Run result

## Behavioral analysis

**The two targets banked, and the composition was additive on the target side.** Both
pre-verified mechanisms fired by artifact in one README: flat-string serialization banked
googlelocal-q2, and complete-list+flat-record banked PATENTS — not just q1 (the named target)
but the whole PATENTS dataset (q1/q2/q3, 0/3→3/3). PATENTS-q1's prior anchor failure was the
JSON-list serialization crash dab0022 identified; the flat-record form fixed it, and the
complete-list rule kept the full CPC set un-truncated. This reconfirms
[[dab-flat-string-serialization-works]] and the dab0022 semi-structured-rules result, and shows
the two levers compose without cancelling on the cells they target (the h0049
[[ade-bench-gated-levers-compose]] pattern held on the target side).

**But the scope did NOT fully hold — one real interaction, one variance.** The whole
falsification point of a GENERATIVE-but-SCOPED lever is whether the scope keeps the ranking /
complete-list canaries safe. Two regressed; attribution by committed artifact splits them:

- **stockmarket-q3 = a REAL complete-list-rule interaction (scope-relevant).** q3 is a genuine
  open complete-list "for each" question ("List all company names … and for each, report its
  average daily trading volume"), so the complete-list rule *correctly* fired — it did NOT
  broaden the row set (anchor and variant have the same companies and the same numbers in the
  same flat `key: number; …` shape). The regression is a **column-selection** error: under the
  added rules the solver emitted the company **description blurb** as the record key instead of
  the **name**. The verifier matches the name then looks for a number in its neighborhood; a
  200-char description between name and number pushed the number out of the match window →
  "No number found near name". This is the rule's blast radius even when scoped correctly: the
  flat-record instruction says emit "EVERY qualifying row as a flat-delimited record" but does
  not pin WHICH column is the identity field, so on a name+number "for each" cell the solver can
  pick the wrong identity column. **The scope (single-winner vs complete-list) was right; the
  rule under-specifies the record's key column.**

- **yelp-q4 = temp=0 variable-band, NOT a scope leak.** Same category ("Restaurants"), correct
  flat-string shape, but a different computed average (3.6648 vs anchor 3.6407) that rounds past
  the verifier's tolerance for the expected 3.63. The `,`→`|` delimiter is exactly the
  flat-string rule's prescribed form and the verifier accepts both; the cause is the underlying
  aggregate number, which yelp-q4 is confirmed to wobble on at temp=0
  ([[dab-opus-vs-gpt55-behavioral-model]] variable-band; dab0022 flagged yelp-q4/q7 as variable).
  This drop attributes to draw variance, not the rules.

**Calibration note (single high draw).** This is ONE high draw; per [[dab-mandatory-dbt-rejected]]
and AC-3, a generative lever's single draw carries ±0.07 and the +0.227 subset lift is not a
board number. The target banks are artifact-attributable (durable, pre-verified, and here
re-fired), but the canary picture must be read by mechanism, not the headline: stockmarket-q3 is
a real rule effect that would recur; yelp-q4 is variance that may not.

## Failure Review

**Scope-leak finding — stockmarket-q3 (complete-list rule, key-column under-specification).**

- **What broke:** a currently-passing complete-list canary (stockmarket-q3, anchor 1.0) regressed
  to 0.0 under the added rules.
- **Root cause (by artifact):** the complete-list / flat-record bullet tells the solver to emit
  "EVERY qualifying row as a flat-delimited record" but does not say the record's leading field
  must be the entity **identity** column (name/title), not a free-text description. On a
  name+number "for each" cell the solver chose the description column as the key; the verifier's
  name→nearby-number match then failed. The complete-list rule's *scope* (it should fire on this
  open-list cell, and it did) was correct — the defect is the rule's *record shape* leaving the
  key column unpinned.
- **Not the other lever:** flat-string serialization is innocent (both anchor and variant use the
  same flat `key: number; …` form). Row selection is innocent (same rows, same numbers).
- **Fixable in place (REVISE-class):** tighten the complete-list bullet to pin the record key —
  e.g. "emit each row as `<entity name/identifier>: <value>` (or `name | value`); use the
  entity's NAME/TITLE as the leading field, never a description/blurb column." This keeps the
  single idea (it is still the complete-list/flat-record rule) and removes the stockmarket-q3
  blast radius, mirroring the dab0022 cycle-2→cycle-3 scoping-fix pattern that removed a ranking
  regression without dropping the durable flip.
- **yelp-q4 is NOT in this review** — attributed to temp=0 variable-band, not the rule (no scope
  fix would address it; a multi-draw read would show it wobbling at the anchor too).

## Follow-up Routing

**REVISE in place → re-smoke (idea unchanged).** Tighten the complete-list/flat-record bullet to
pin the record's leading field to the entity NAME/TITLE (never a description/blurb column), then
re-freeze and re-smoke the same 4-dataset panel. This is a one-line scope-tightening on the
existing bullet — the single composition idea is preserved (mirrors dab0022 cycle-2→cycle-3). If
the revise re-smoke holds stockmarket-q3 while keeping both target banks, advance to a full
multi-draw confirm (≥2/3 hold on the targets, zero scope-leak) before any PROMOTE.

## Verdict

**Gate read: REVISE (not GO, not REJECT).** One high draw: both durable targets BANKED by
committed artifact (googlelocal-q2 flipped; PATENTS swept 0/3→3/3), subset stratified +0.227 over
anchor — the composition works on the target side. But the scope did NOT fully hold: **one real
scope interaction** (stockmarket-q3, a complete-list canary, regressed because the flat-record
rule leaves the record's key column unpinned and the solver emitted the description blurb instead
of the name — verified by artifact) plus **one variance drop** (yelp-q4, temp=0 variable-band, not
the rule). GO required zero scope-leak regression; stockmarket-q3 is a genuine rule-caused
regression, so the gate cannot be GO. It is REVISE rather than REJECT because the fix is a
one-line tightening of the existing bullet (pin the key column to name/title) that keeps the
single idea — exactly the dab0022 scoping-fix shape — not a dead-family wall. **Recommended next:
REVISE the complete-list bullet, re-freeze, re-smoke the 4-panel; advance to full only if
stockmarket-q3 holds with both targets still banked.** Caveat: single high draw — yelp-q4's drop
is variance and the +0.227 is not a board number (AC-3).

## Stage Report: propose

- DONE: Fork the BATCH anchor solver `solver_workflows/spacedock-readme-baseline-hostfix` to `solver_workflows/dab0023-compose-durable-serialization-completelist` and add ONLY the `### Answer serialization & list rules` section verbatim; change nothing else, leak-guard prose byte-intact.
  `diff` = single hunk (94a94,98) adding the one subsection + two scoped bullets verbatim from the entity; leak-guard L81–87 byte-identical; no forbidden tokens in added lines.
- DONE: Build full + smoke specs in BATCH mode by forking `specs/codex-dab-batch-baseline.yaml`; keep `reasoning_effort: high`; full spec differs ONLY in experiment: + solver_workflow:.
  `diff codex-dab-batch-baseline.yaml dab0023-...yaml` = only `experiment:` + `solver_workflow:` (+ ABOUTME comments); effort `high`, `agent.kind: spacedock_solver`/`runtime: codex`/`trials: 1` preserved.
- DONE: Freeze both specs.
  `…frozen.yaml` + `…smoke.frozen.yaml` written (rk freeze --allow-missing); both carry kind: spacedock_solver + runtime: codex.
- DONE: `rk run --explain` to confirm the smoke selection = durable targets (googlelocal, PATENTS) PLUS the G8 ranking-canary panel (stockmarket, yelp).
  `--explain` → Tasks: 4; materialized task dirs = PATENTS, googlelocal, stockmarket, yelp; canaries stockmarket q3/q4 + yelp q4/q7 are anchor-PASS and carried (batch mode runs every query in each dataset).
- DONE: Run the gatekeeper subagent; record per-rule PASS/WARN/FAIL table + APPROVE/REVISE/REJECT; prepare the smoke-set boxed table with @codex-batch-baseline rewards resolved.
  Gatekeeper = APPROVE (no FAILs; one G7 WARN on bullet 2 inert-risk, advisory only); table + boxed smoke table written to `## Gatekeeper review`.

### Summary
Forked the @codex-batch-baseline solver and added exactly one `### Answer serialization & list rules` section with the two pre-verified scoped levers (flat-string serialization + scoped complete-list/flat-record) verbatim; full spec differs from the anchor only in `experiment:` + `solver_workflow:` with `reasoning_effort: high` held (AC-1 confound-free). Both specs frozen; `--explain` confirms the smoke set is exactly the 2 durable targets (googlelocal-q2 ❌, PATENTS-q1 ❌ at anchor) plus the G8 ranking-canary panel (stockmarket q3/q4 ✅, yelp q4/q7 ✅ at anchor) so a scope leak is detectable. Gatekeeper recommends APPROVE with a single advisory G7 WARN (the complete-list bullet is shape-gated abstract prose without a worked skeleton — inert-risk on PATENTS-q1; fixable in place if smoke shows it not firing). All FO reject-condition checks are clean → auto-gate conditions met.

## Stage Report: smoke

- DONE: Launch the dab0023 detached smoke (high) and record the handle/pid/ETA.
  Launched via `drivers/rk-run-detached.sh dab0023-smoke …smoke.frozen.yaml run`; handle `runs/.rk-handles/dab0023-smoke-20260623-073517`, pid 2719479 (alive, `ps` confirmed); `--explain` re-confirmed 4 datasets + effort high. Section written to `## Smoke result → Smoke run (launched — detached)`. Not polling — FO owns the wait.

### Summary
Re-confirmed the smoke selection (4 datasets: googlelocal/PATENTS targets + stockmarket/yelp ranking canaries, gpt-5.5/high) then launched the run DETACHED. Handle `runs/.rk-handles/dab0023-smoke-20260623-073517`, pid 2719479 verified alive; `done` sentinel absent (running). Returning the handle to the FO immediately per the detached-run contract.

### Stage Report: smoke (phase 2 — audit + score + deep-dive)

- DONE: Audit (AC-2) — `rk audit --policy strict`.
  clean 4 / coverage_missing 0 / tainted 0; no dab-postgres dual-signature; scores attestable.
- DONE: Score — `rk score`.
  Stratified Pass@1 = 0.9143 over the 4 smoke datasets (n_completed 4, n_errored 0); anchor 4-subset 0.6875 → +0.227 (single high draw, not a board number).
- DONE: Deep-dive (a) did the 2 durable targets bank?
  BOTH banked by committed artifact: googlelocal-q2 0→1 ("All names and scores matched"); PATENTS-q1 0→1 ("All CPC codes present") + bonus PATENTS q2/q3 also flipped (dataset 0/3→3/3). Recoverability: answers extracted verbatim from the codex rollout transcripts (escaped form), not truncated prefixes.
- DONE: Deep-dive (b) did the scope hold?
  PARTIAL — two canaries regressed. stockmarket-q3 (complete-list "for each") = REAL rule interaction by artifact: solver emitted the description blurb as the record key instead of the name (anchor used names; same rows/numbers/flat-shape) → wrong column, not row-broadening. yelp-q4 = temp=0 variable-band (3.6648 vs anchor 3.6407 avg, rounds past tolerance) — NOT the rule. stockmarket-q4 + yelp-q7 HELD.
- DONE: `## Smoke result` flip/scope table + `## Behavioral analysis` + `## Failure Review` written.
  Full attribution tables and root-cause for the stockmarket-q3 scope interaction recorded.
- DONE: Gate verdict (plain words).
  REVISE: both targets banked, but stockmarket-q3 is a real complete-list-rule regression (key column unpinned) → tighten the bullet to pin the leading field to name/title, re-freeze, re-smoke; advance to full only if it holds. REJECT not warranted (one-line in-place fix, single idea preserved); GO not warranted (scope-leak by artifact). yelp-q4 flagged as variance.

### Summary
Smoke ran clean (rc=0, strict audit 4/0/0). Both pre-verified targets BANKED by committed artifact — googlelocal-q2 flipped and PATENTS swept 0/3→3/3 — confirming the two levers compose additively on the cells they target (h0049 pattern). The scope did not fully hold: stockmarket-q3 (a genuine complete-list canary) regressed because the flat-record rule leaves the record's identity column unpinned and the solver emitted the description blurb instead of the name (artifact-verified; not row-broadening, not format), while yelp-q4 dropped on temp=0 variable-band variance unrelated to the rule. Verdict REVISE: pin the complete-list bullet's key column to name/title (one-line, single-idea-preserving, dab0022 cycle-2→cycle-3 shape), re-smoke the 4-panel, advance to full only if stockmarket-q3 holds with both targets still banked.
