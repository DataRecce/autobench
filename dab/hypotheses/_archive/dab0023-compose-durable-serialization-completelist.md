---
id: dab0023
title: Compose the 2 durable banked levers — flat-string serialization + complete-list/flat-record — into the seed README as pre-verified levers
status: conclude
kind: hypothesis
source: "dab0022 PASSED-validated follow-up (captain-directed). dab0022 validated 2 durable, confound-free flips across draws — googlelocal-q2 (flat-string serialization, reconfirming dab0015) and PATENTS-q1 (complete-list + flat simple-record) — but did NOT promote because the single-lever board lift was variance-swamped. This files the composition play: bank both pre-verified mechanisms into the seed README at once (the ade-bench h0049 gated-levers-compose pattern), scoped so they fire only where validated and do not perturb ranking/single-winner cells."
started: 2026-06-23T06:38:33Z
completed: 2026-06-23T10:23:10Z
verdict: rejected
score: 0.5
worktree:
archived: 2026-06-23T10:23:10Z
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

### Smoke run cycle-2 (launched — detached)

Re-smoke after the cycle-2 scope fix (bullet 2 lead-field pinned to entity NAME/TITLE; gatekeeper cycle-2 APPROVE). Launched DETACHED and VERIFIED alive (the cycle-1 launch had silently no-op'd, so liveness was confirmed this time).

- **Handle:** `runs/.rk-handles/dab0023-smoke2-20260623-082848` (from `dab/`)
- **PID:** 2772504 — **VERIFIED alive** (`ps -p 2772504` → STAT `S`, the `__worker` running the run; `done` sentinel ABSENT = still running).
- **Spec:** `specs/dab0023-compose-durable-serialization-completelist.smoke.frozen.yaml` (solver_workflow_content_hash `sha256:df29203c…` = cycle-2 README).
- **Selection (`--explain`):** 4 datasets — googlelocal + PATENTS (targets), stockmarket + yelp (ranking canaries); model gpt-5.5, `reasoning_effort: high` (Tasks: 4, confirmed pre-launch).
- **Log:** `runs/.rk-handles/dab0023-smoke2-20260623-082848/log`; **done sentinel:** `…/done` (absent until finished; then rc/end/rundir).
- **ETA:** ~30 min wallclock (cycle-1 4-panel ran ~29 min). The FO owns the wait + auto-wakeup; not polling.
- **Cell to watch:** stockmarket-q3 must now HOLD PASS (the cycle-1 leak); both target banks (googlelocal-q2, PATENTS-q1) must stay flipped; yelp-q4's cycle-1 drop was temp=0 variance.

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

**STOP — no follow-up.** (The cycle-1 routing below proposed an in-place REVISE; it was executed
as cycle-2 and the prescribed lead-field fix proved README-inert by committed-artifact
byte-comparison — see `## Verdict (cycle 2)` and `## Failure Review (cycle 2)`.) The complete-list
arm's key-column behavior is a dead end (README cannot steer which COLUMN the solver picks as the
record key), and the only durable half (flat-string serialization) is already banked in dab0022 —
so there is no new hypothesis to file and no third revise (pinning the column harder in prose is
the same dead channel). `@codex-batch-baseline` + seed README UNCHANGED; the dab0022 5-draw 0.7433
leaderboard submission stands, unaffected. Not a structural workflow change → no WORKFLOW-REFINE
edit.

_Cycle-1 routing (superseded — recorded for history):_ **REVISE in place → re-smoke (idea
unchanged).** Tighten the complete-list/flat-record bullet to pin the record's leading field to
the entity NAME/TITLE (never a description/blurb column), then re-freeze and re-smoke the same
4-dataset panel. This is a one-line scope-tightening on the existing bullet — the single
composition idea is preserved (mirrors dab0022 cycle-2→cycle-3). If the revise re-smoke holds
stockmarket-q3 while keeping both target banks, advance to a full multi-draw confirm (≥2/3 hold on
the targets, zero scope-leak) before any PROMOTE.

## Verdict (cycle 1)

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

## Gatekeeper review (cycle 2 — supersedes cycle 1)

**Recommendation: APPROVE** — cycle-2 re-review (SUPERSEDES the cycle-1 APPROVE): the one-line scope fix is in place — bullet 2 now pins each record's leading field to the entity NAME/TITLE ("never a description/summary/blurb column"), directly addressing the cycle-1 stockmarket-q3 scope leak. Single stage section added, leak-guard byte-intact, full spec differs only in `experiment:`/`solver_workflow:` (effort stays `high`), both re-frozen (Jun 23 08:20), and the smoke panel keeps the perturbable ranking canaries that prove the scope holds.
Guideline: `_gatekeeper/propose-review-guideline.md` (last-updated 2026-06-15). Reviewed 2026-06-23.

| Rule | Verdict | Evidence |
|------|---------|----------|
| G1 single idea/stage | PASS | README diff vs parent `spacedock-readme-baseline-hostfix` = one hunk `93a94,98`: adds exactly one `### Answer serialization & list rules` subsection (two bullets = the one composition idea the claim names); no other stage/section touched, no leak-guard prose edited. |
| G2 leak-guard intact | PASS | Leak-guard lines byte-identical parent↔variant (L81–87 `diff` rc=0); the only `ground_truth`/`db_description_withhint`-adjacent hits are the pre-existing *forbidding* prose, not in the added block; added lines (L94–98) contain none of `ground_truth`/`db_description_withhint`/`curl`/`wget`/`git clone`/`huggingface`/`hf://` and pin answer FORMAT/record-shape only, naming no oracle/hint file. |
| G3 spec two fields | PASS | `diff codex-dab-batch-baseline.yaml dab0023-…yaml` = only `experiment:` + `solver_workflow:` (plus ABOUTME comment text); `agent.kind: spacedock_solver`, `runtime: codex`, top-level `trials: 1`, `reasoning_effort: high` all preserved (`concurrency.trials: 2` is the parallelism knob, not the G3 trials). |
| G4 smoke tasks+exclude | PASS | Smoke diff = adds `benchmark.tasks` (4 dataset names: googlelocal/PATENTS/stockmarket/yelp) + `exclude_tasks` (the other 8 dataset names) — dataset names, not per-query ids, correct for the plugin selector; nothing else differs. `--explain` → Tasks: 4 (exactly these); both named targets googlelocal-q2 + PATENTS-q1 survive. |
| G5 both frozen | PASS | Both `…frozen.yaml` (1895 B) and `…smoke.frozen.yaml` (1890 B) exist (Jun 23 08:20, re-frozen post-fix); each carries `kind: spacedock_solver` + `runtime: codex`. |
| G6 resolver fidelity | PASS | Inserted text matches the claim: bullet 1 = flat-string serialization, format-only ("does not change which rows you select"); bullet 2 = scoped complete-list off single-winner/fixed-top-k AND now carries the cycle-2 key-column pin ("Use the entity's NAME/TITLE as each record's leading field … never a description/summary/blurb column"). Generative-but-scoped, no self-anchored phrasing; the fix stays within the single idea (still the complete-list/flat-record rule), no scope creep. |
| G7 actionability/inert-risk | PASS | Bullet 1 = concrete mechanical serialization edit (worked tokens `A; B; C` / `name \| code \| year`). The cycle-2 fix UPGRADES bullet 2 from abstract prose toward mechanical: it now carries worked record-shape skeletons (`name: value`, `name \| value`) plus the named identity-column constraint — the cycle-1 G7 WARN is RESOLVED (the worked-example form the prior note asked for is now present). |
| G8 regression-canary coverage | PASS | Generative-but-scoped (both rules fire by question-shape). Smoke keeps non-target `@baseline`-PASS perturbable canaries from datasets OTHER than the targets: stockmarket q3/q4 + yelp q4/q7 (all anchor-PASS) — ≥2 perturbable canaries on the ranking/complete-list construct the rule could perturb; stockmarket-q3 specifically is the cycle-1 leak this revise must now hold. |
| G9 selector independence | N/A | Not a multi-candidate/selector protocol — two output-format/record-shape rules, single session. |
| G10 self-correcting false-positive | N/A | Not a check/reconcile/validate-and-fix lever — no verify-and-act-on-disagreement instruction. |

**For the captain:** This cycle-2 review SUPERSEDES the cycle-1 APPROVE. The cycle-1 smoke surfaced the stockmarket-q3 scope leak (the flat-record rule left the record's identity column unpinned, so the solver emitted the company description blurb as the leading field). The cycle-2 one-line fix is confirmed present in bullet 2 — it now pins the leading field to the entity NAME/TITLE and explicitly forbids a description/summary/blurb column (the dab0022 cycle-2→cycle-3 scoping-fix shape, the in-place fix the cycle-1 verdict prescribed). No FAILs; the prior G7 WARN is now RESOLVED (bullet 2 carries worked `name: value` skeletons). Clear to re-smoke the same 4-panel — the cell to watch is stockmarket-q3 (must now HOLD PASS) alongside the two target banks (googlelocal-q2, PATENTS-q1); yelp-q4's cycle-1 drop was temp=0 variable-band, not the rule.

## Stage Report: propose (cycle 2)

- DONE: ONE-LINE SCOPE FIX — tighten the complete-list/flat-record bullet so the leading record-key field is pinned to the entity NAME/TITLE, never a free-text description/summary column; flat-string bullet + everything else byte-intact; leak-guard byte-intact; section stays ONE idea.
  README diff vs parent = single hunk `93a94,98` (unchanged shape); bullet 2 gains one sentence ("Use the entity's NAME/TITLE as each record's leading field (e.g. `name: value` or `name | value`), never a description/summary/blurb column."); bullet 1 byte-identical; leak-guard L81–87 byte-identical (`diff` rc=0); no forbidden tokens in L94–98.
- DONE: Re-freeze BOTH specs; confirm full spec differs from anchor ONLY in `experiment:` + `solver_workflow:` (effort stays high); re-run `rk run --explain` on smoke frozen to confirm the 4-dataset selection unchanged.
  `rk freeze --allow-missing` re-wrote both `…frozen.yaml` (08:20); new solver_workflow_content_hash `sha256:df29203c…`. Full source-spec diff vs `codex-dab-batch-baseline.yaml` = only `experiment:` + `solver_workflow:` (+ ABOUTME); `reasoning_effort: high`, `spacedock_solver`/`codex`/`trials:1` intact. `--explain` on smoke frozen → `Tasks: 4` = googlelocal + PATENTS (targets) + stockmarket + yelp (ranking canaries); other 8 excluded.
- DONE: Re-run the gatekeeper subagent; record the cycle-2 per-rule table + APPROVE/REVISE/REJECT; note cycle-2 supersedes cycle-1 and the complete-list bullet now pins the lead field.
  Gatekeeper cycle-2 = APPROVE, zero FAILs; cycle-1 G7 WARN now RESOLVED (worked `name: value` skeletons present). Recorded in `## Gatekeeper review (cycle 2 — supersedes cycle 1)`.

### Summary
Applied the captain-approved cycle-2 one-line scope fix: bullet 2 of the `### Answer serialization & list rules` section now pins each complete-list record's leading field to the entity NAME/TITLE (never a description/summary/blurb column) — the dab0022 cycle-2→cycle-3 scoping-fix shape that addresses the cycle-1 stockmarket-q3 leak (solver had emitted the company description blurb as the key, pushing the required number out of the validator's name-number match window). Bullet 1 and the leak-guard prose stay byte-intact; the section remains one idea. Both specs re-frozen; the full spec still differs from the anchor only in `experiment:` + `solver_workflow:` with `reasoning_effort: high` held; `--explain` re-confirms the unchanged 4-dataset smoke panel. The cycle-2 gatekeeper recommends APPROVE with zero FAILs and the prior G7 inert-risk WARN now resolved.

## Stage Report: smoke (cycle-2 launch)

- DONE: Launch the dab0023 cycle-2 re-smoke (high) DETACHED and VERIFY the handle (the cycle-1 launch silently no-op'd).
  `--explain` re-confirmed Tasks: 4 (googlelocal/PATENTS targets + stockmarket/yelp canaries, gpt-5.5/high, content-hash df29203c) then launched via `drivers/rk-run-detached.sh dab0023-smoke2 …smoke.frozen.yaml run`. Handle `runs/.rk-handles/dab0023-smoke2-20260623-082848`, pid 2772504 VERIFIED alive (`ps` → STAT `S`, `__worker` running; `done` sentinel ABSENT). Recorded in `## Smoke result → Smoke run cycle-2 (launched — detached)`. ETA ~30 min. Not polling — FO owns the wait.

### Summary
Re-confirmed the 4-dataset smoke selection (high) then launched the cycle-2 re-smoke DETACHED. Unlike the cycle-1 launch (which silently no-op'd), this one was VERIFIED: handle dir `runs/.rk-handles/dab0023-smoke2-20260623-082848` exists, worker pid 2772504 confirmed alive via `ps`, `done` sentinel absent (running). Returning the handle to the FO immediately per the detached-run contract — the FO owns the wait + auto-wakeup.

## Smoke result (cycle 2 — phase 2: audit + score + scope-fix verification)

**Run:** `runs/dab0023-compose-durable-serialization-completelist/2df5f0e5c3907715` (rc=0, ~30 min; done sentinel end 08:58).
**Audit (AC-2):** `rk audit --policy strict` = **clean 4 / coverage_missing 0 / tainted 0** — no dab-postgres dual-signature, all 4 datasets present. Scores attestable.
**Score:** stratified Pass@1 over the 4 smoke datasets = **0.8042** (n_completed 4, n_errored 0) vs cycle-1 **0.9143** and the anchor 4-subset baseline. Single high draw — NOT a board number.

**Cycle-2 flip/scope table (by committed artifact vs anchor `bf113446fdd94373`; per-query = anchor / cycle-1 / cycle-2):**

| Cell | Role | Anchor | C1 | C2 | C2 verdict | Attribution (committed artifact) |
|------|------|--------|----|----|-----------|----------------------------------|
| googlelocal-q2 | 🎯 TARGET (flat-string) | FAIL | PASS | **FAIL** | **format FIRED, row-selection miss (variance).** Committed `"Elite Massage \| 5.0; Angel-A Massage \| 4.333…; Aurora Massage \| 4.178…"` — correct flat `name \| value` shape (flat-string lever worked) but wrong row set: expected "J B Oriental Inc" absent. Confirmed variable-band (dab0022: 4/5 over 5 draws); this draw is the natural ~1/5 miss, NOT a serialization failure. |
| PATENTS-q1 | 🎯 TARGET (complete-list+flat-record) | FAIL | PASS | **PASS** | **STILL BANKED.** "All CPC codes present in LLM output" — complete-list+flat-record fired, full CPC set emitted un-truncated. The named target holds across both draws. |
| PATENTS-q2 | (bonus) | FAIL | PASS | **PASS** | "All fuzzy names matched, CPC/year found near each name." Holds. |
| PATENTS-q3 | (bonus) | FAIL | PASS | **FAIL** | **name-lead FIRED, CPC-subclass-selection miss (variance).** Committed answer leads with the NAME (`BLOOM ENERGY CORP \| …`, `CRYSTAL IS INC \| SEMICONDUCTOR DEVICES NOT COVERED BY CLASS H10`) — name-lead + flat-record both correct. Failed because the verifier expected CRYSTAL IS INC paired with a different/longer CPC subclass title ("SINGLE-CRYSTAL GROWTH; …"); the solver chose the wrong CPC subclass. Analytic join-semantics variance, NOT format/row-count. |
| stockmarket-q3 | ✅ CANARY (complete-list "for each") | PASS | FAIL | **FAIL** | **SCOPE FIX WAS INERT (still regressed).** Committed q3 STILL leads each record with the description BLURB: `"Apex Global Brands Inc. specializes in creating and marketing…: 23781.42; BIO-key International, Inc. specializes in…: 10988.14; …"` — byte-pattern identical to cycle-1. The lead-field pin ("use NAME/TITLE, never a description/blurb") did NOT change the committed output. Verifier "No number found near name" (the blurb pushes the number out of the name's match window). |
| stockmarket-q4 | ✅ CANARY (top-5) | PASS | PASS | **PASS** | HELD. |
| yelp-q4 | ✅ CANARY (category avg-star) | PASS | FAIL | **PASS** | **RECOVERED** — confirming the cycle-1 drop was temp=0 variable-band variance, not the rule (as attributed). |
| yelp-q7 | ✅ CANARY (complete-list categories) | PASS | PASS | **PASS** | HELD. |

**Headline:** The named target PATENTS-q1 STILL banks; the other target googlelocal-q2 missed on row-selection variance (format fired). The scope fix was **INERT on its own target cell** — stockmarket-q3 still emits the blurb-led answer, byte-identical to cycle-1. yelp-q4 recovered (confirming cycle-1's variance call).

## Behavioral analysis (cycle 2)

**The lead-field scope fix did NOT change behavior on stockmarket-q3 — it was inert.** This is the gate-deciding finding. The cycle-2 README adds a concrete, worked instruction to bullet 2: "Use the entity's NAME/TITLE as each record's leading field (e.g. `name: value` or `name | value`), never a description/summary/blurb column." By committed artifact the solver's q3 answer is *byte-pattern identical to cycle-1* — it still leads each record with the full company description blurb. The solver did not adopt the rule on this cell. This is the **"talks but doesn't do"** inert-risk the cycle-1 G7 WARN flagged (and which the cycle-2 gatekeeper believed resolved by the worked skeleton): a README prose instruction about WHICH COLUMN to use as the record key is **not reliably actionable** at gpt-5.5/high — the solver had already built its q3 result keyed on the description column during exploration and the README rule did not redirect that choice. The dab0012/[[dab-readme-cannot-suppress-output-shape]] family wall recurs: README prose can pin FORMAT (flat-string fired everywhere) but cannot reliably steer WHICH FIELD the solver treats as identity.

**The two non-banking targets are FORMAT-fired / CONTENT-variance, not lever failures.** googlelocal-q2 and PATENTS-q3 both committed correctly-shaped flat / name-led answers (the levers fired) but missed on analytic content — googlelocal-q2 on row selection (3 massage businesses vs the expected set incl. "J B Oriental Inc"; confirmed variable-band 4/5), PATENTS-q3 on CPC-subclass choice (wrong subclass title for CRYSTAL IS INC). These are the oracle-blind variable band, not the rules. PATENTS-q1 (the named target) held both draws.

**Calibration note (single high draw).** Per AC-3 and [[dab-mandatory-dbt-rejected]], a generative lever's single draw carries ±0.07; the cycle-2↔cycle-1 swings (googlelocal-q2 PASS→FAIL, PATENTS-q3 PASS→FAIL, yelp-q4 FAIL→PASS) are exactly that draw variance on the oracle-blind band. The durable signal across BOTH draws: PATENTS-q1 banks; flat-string format fires; stockmarket-q3 regresses with the SAME blurb-led mechanism (the fix is inert).

## Failure Review (cycle 2)

**The cycle-2 scope fix is INERT on stockmarket-q3 — the regression persists by the same mechanism.**

- **What broke:** the stockmarket-q3 canary (anchor PASS) regressed to 0.0 again, IDENTICALLY to cycle-1 — committed answer leads each record with the description blurb, not the name.
- **Root cause (by artifact):** the cycle-2 README instruction pinning the leading field to NAME/TITLE was NOT adopted by the solver on this cell. The committed q3 string is byte-pattern identical to cycle-1's blurb-led output. The fix changed the README but not the behavior — a README prose instruction about which column is the record identity is not reliably actionable at gpt-5.5/high (the "talks but doesn't do" inert-risk; same wall as [[dab-readme-cannot-suppress-output-shape]] / dab0012 for output-shape steering).
- **Not row-selection, not flat-string:** rows and numbers are the same as the anchor; the flat `key: number; …` shape is correct. The single defect is the identity COLUMN, and the README could not move it.
- **Why a third in-place revise is NOT indicated:** cycle-1 attributed this to an unpinned key column and prescribed the lead-field pin; cycle-2 added exactly that pin and it was inert by artifact. The same one-line-prose family has now failed to move this cell once it was tried. Pinning the column harder in prose is the same dead channel (README-cannot-steer-which-field). This crosses from "fixable scoping nuance" into the dab0012 README-output-shape dead-family boundary for the complete-list arm's key-column behavior.

## Verdict (cycle 2)

**Gate read: NO-GO for promote; the composition is VALIDATED-BUT-NOT-PROMOTABLE (the dab0022 outcome), and the complete-list arm's key-column behavior is REJECTED as README-inert.** One high draw, clean audit (4/0/0). The decisive reads:
1. **The scope fix was INERT** — stockmarket-q3 still regressed by the identical blurb-led mechanism (committed answer byte-pattern identical to cycle-1). GO required stockmarket-q3 to HOLD PASS; it did not, and the prescribed in-place fix did not move it. This is not a new leak — it is the *same* leak surviving the fix, which reclassifies it from REVISE-able to README-inert ([[dab-readme-cannot-suppress-output-shape]] family).
2. **The flat-string serialization lever is real and durable** — it fired (correct flat shape) on every target; PATENTS-q1 (named target) banked across BOTH draws. This reconfirms [[dab-flat-string-serialization-works]].
3. **The two non-banks (googlelocal-q2, PATENTS-q3) are oracle-blind content variance, not lever failures** — both committed correctly-formatted answers and missed on analytic content; the format/shape levers fired.

**Recommendation:** Do NOT advance to full (the scope fix is inert → a full board would carry the stockmarket-q3-style key-column regression on every complete-list "for each" name+number cell, with no in-prose remedy). CONCLUDE the hypothesis **validated-but-not-promoted**: bank the knowledge — (a) flat-string serialization durably fires (already in [[dab-flat-string-serialization-works]]); (b) the complete-list/flat-record arm's KEY-COLUMN choice is README-inert (the lead-field prose fix did not move stockmarket-q3 by artifact), a new boundary for [[dab-readme-cannot-suppress-output-shape]]. Leave `@codex-batch-baseline` UNCHANGED. **NOT a third in-place revise** — the one-line key-column pin was the prescribed fix and it was inert; pinning harder in prose is the same dead channel. Caveat: single high draw — the per-cell variance (googlelocal-q2, PATENTS-q3) is draw noise, but the stockmarket-q3 inert-fix finding is by committed-artifact byte-comparison, not a variance call.

## Stage Report: smoke (cycle-2 phase 2 — audit + score + scope-fix verification)

- DONE: Audit (AC-2) — `rk audit --policy strict` on `2df5f0e5c3907715`.
  clean 4 / coverage_missing 0 / tainted 0; no dab-postgres dual-signature; scores attestable. Run-dir confirmed = the smoke2 done sentinel (rc=0, end 08:58).
- DONE: Score — `rk score`.
  Stratified Pass@1 = 0.8042 over the 4 smoke datasets (n_completed 4, n_errored 0); cycle-1 was 0.9143. Single high draw, not a board number.
- DONE: Deep-dive (a) do the 2 targets still bank?
  PATENTS-q1 (named target) STILL banks by artifact ("All CPC codes present"). googlelocal-q2 did NOT bank this draw — but by committed artifact the flat-string format fired (`name | value`); the miss is row-selection variance (variable-band 4/5 in dab0022), not the lever.
- DONE: Deep-dive (b) DID THE SCOPE FIX WORK? (stockmarket-q3).
  NO — INERT by committed artifact. The cycle-2 q3 answer is byte-pattern identical to cycle-1: it STILL leads each record with the description blurb ("Apex Global Brands Inc. specializes in…: 23781.42; …"), not the name. The lead-field pin did not change behavior. stockmarket-q4 + yelp-q7 HELD; yelp-q4 RECOVERED (confirming cycle-1's variance attribution).
- DONE: Cycle-2 flip/scope table + `## Behavioral analysis (cycle 2)` + `## Failure Review (cycle 2)` written.
  Full per-cell attribution (anchor/C1/C2) recorded; stockmarket-q3 inert-fix established by byte-comparison; PATENTS-q3 non-bank attributed to CPC-subclass-selection variance.
- DONE: Gate verdict (plain words).
  NO-GO for promote; the prescribed scope fix was INERT (stockmarket-q3 unchanged by artifact) → reclassify the complete-list key-column behavior as README-inert ([[dab-readme-cannot-suppress-output-shape]] family), NOT a third revise. Flat-string lever durable (PATENTS-q1 banks both draws). CONCLUDE validated-but-not-promoted; leave `@codex-batch-baseline` unchanged.

### Summary
Cycle-2 re-smoke ran clean (rc=0, strict audit 4/0/0), stratified 0.8042 over the 4-panel. The gate-deciding finding: the lead-field scope fix was **INERT** — stockmarket-q3's committed answer is byte-pattern identical to cycle-1 (still leads with the description blurb), so the prescribed fix did not change behavior. PATENTS-q1 (named target) banked across both draws and the flat-string format fired on every target, confirming the durable flat-string lever; the two non-banks (googlelocal-q2, PATENTS-q3) committed correctly-shaped answers and missed on oracle-blind analytic content (row-selection / CPC-subclass variance), not lever failure; yelp-q4 recovered (cycle-1 variance confirmed). Verdict NO-GO-for-promote: the complete-list arm's key-column choice is README-inert (a new boundary for the dab0012 README-output-shape dead family), NOT a third in-place revise. Recommend CONCLUDE validated-but-not-promoted, `@codex-batch-baseline` unchanged. Caveat: single high draw; per-cell content swings are draw variance, but the inert-fix finding is by committed-artifact byte-comparison.

## Verdict

**REJECTED** (captain-concluded 2026-06-23; record-keeping only — `@codex-batch-baseline` + seed
README UNCHANGED, the FO sets the frontmatter verdict/status and archives).

**The composition hypothesis is FALSIFIED.** It did NOT bank both durable cells without regression:
across two confound-free high draws (codex-vs-codex, high-vs-high) the named target PATENTS-q1
banked but googlelocal-q2 did not hold, and a ranking/complete-list canary (stockmarket-q3)
regressed both times. The h0049 "gated levers compose additively, the gate is the isolation"
pattern did NOT carry here, because the distinctive new arm could not be gated into safety.

**Why — the distinctive new arm (complete-list KEY-COLUMN pinning) is README-INERT by
committed-artifact byte-comparison.** The cycle-2 lead-field fix ("use the entity's NAME/TITLE as
each record's leading field, never a description/blurb column") left stockmarket-q3's committed
answer *byte-identical to cycle-1* — still blurb-led ("Apex Global Brands Inc. specializes in
…: 23781.42; …"), failed both draws. The README changed; the behavior did not. A README prose
instruction about WHICH COLUMN is the record identity is not reliably actionable at gpt-5.5/high
("talks but doesn't do"). Notably, the *same* name-lead fix that *appeared* to work in dab0022
cycle-3 was a favorable single draw — dab0023's 2-draw byte-comparison shows it is
weakly/un-steerable, i.e. draw-dependent rather than a real flip.

**What IS real (but already banked, not a new win):** the FORMAT half — flat-string serialization
— IS README-steerable and durable. It fired on every target this run and PATENTS-q1 banked across
BOTH draws, reconfirming [[dab-flat-string-serialization-works]] a third time (after dab0015 +
dab0022). That is a reconfirmation already captured by the dab0022 leaderboard submission, not a
new promotable result. The two non-banking targets (googlelocal-q2 row-selection, PATENTS-q3
CPC-subclass) committed correctly-shaped answers and missed on oracle-blind analytic content —
draw variance, not lever failure.

**KEY NEW KNOWLEDGE — a sharper boundary on the dab0012 README-output-shape dead family
([[dab-readme-cannot-suppress-output-shape]]):** the README can steer answer **FORMAT**
(flat-string: durable) but NOT **which COLUMN** the solver picks as the record key (the complete-list
key-column choice is README-inert / draw-dependent, proven here by 2-draw byte-comparison). The
flat-string FORMAT lever and the key-COLUMN selection are on opposite sides of this line.

**Disposition:** `@codex-batch-baseline` and the seed README UNCHANGED. No follow-up (the
complete-list arm is a dead end; flat-string is already banked in dab0022). The dab0022 5-draw
0.7433 leaderboard submission stands as the deliverable, unaffected. Caveat: single high draw per
cycle — the per-cell content swings (googlelocal-q2, PATENTS-q3) are draw noise, but the
stockmarket-q3 inert-fix finding is by committed-artifact byte-comparison across two draws, not a
variance call.

## Stage Report: conclude

- DONE: Write dab0023 `## Verdict` = REJECTED (distill the falsification + key new knowledge).
  Canonical `## Verdict` = **REJECTED** written: composition FALSIFIED (didn't bank both durable cells without regression); the complete-list KEY-COLUMN arm is README-inert by 2-draw byte-comparison (cycle-2 lead-field fix left stockmarket-q3 byte-identical to cycle-1); flat-string FORMAT half durable but already banked in dab0022 (reconfirms 3rd time); key new knowledge = sharper dab0012 boundary (README steers FORMAT not which COLUMN is the record key). Cycle-1 verdict relabelled `## Verdict (cycle 1)` to preserve history.
- DONE: Append a one-line dab0023 entry to `_artifacts/self-learning.md`.
  Appended: REJECTED; complete-list key-column README-inert = new dab0012-family boundary; flat-string reconfirmed durable; no seed change.
- DONE: Set `## Follow-up Routing` = stop.
  Updated to **STOP — no follow-up** (arm is a dead end, flat-string already banked); cycle-1 REVISE routing kept inline as superseded-for-history. Not a structural change → no WORKFLOW-REFINE edit (noted).

### Summary
Concluded dab0023 as REJECTED (record-keeping only — `@codex-batch-baseline` + seed README UNCHANGED; FO owns frontmatter verdict/status + archive). Canonical `## Verdict` distills the falsification: the composition did not bank both durable cells without regression, and the distinctive complete-list KEY-COLUMN arm is README-inert by committed-artifact byte-comparison across two draws (the prescribed lead-field fix left stockmarket-q3 byte-identical to cycle-1). The flat-string FORMAT half is durable but already banked in dab0022, so it is a reconfirmation, not a new promotable win. Key new knowledge banked to self-learning: a sharper dab0012-family boundary — the README can steer answer FORMAT (flat-string) but not which COLUMN the solver treats as the record key. Follow-up Routing = stop (dead end, no new hypothesis); no WORKFLOW-REFINE edit (not structural). The dab0022 5-draw 0.7433 leaderboard submission stands unaffected.
