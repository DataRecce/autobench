# Workflow Refinement Log

A living ledger of **findings and learnings about refining workflow _structure_** —
adding/removing/reordering/replacing stages, or adding new protocols. When a hypothesis (or a
captain decision) changes the *shape* of a workflow rather than tweaking a rule inside an
existing stage, record what we learned here so we don't relearn it or repeat a dead end.

There are two workflow layers in this project, and both belong here:

- **Solver workflow** — the codex solver's process (`solver_workflows/<variant>/README.md`):
  its stages (Exploration → Implementation → Validation → Finalization) and the protocols it
  runs. Most `h<NNNN>` hypotheses that "refine the workflow" mutate *this*.
- **Autoresearch loop** — the spacedock meta-loop the first officer drives:
  `concept → ideate → propose → smoke → full → analyze → conclude`. Refinements to *its* stage
  graph or gate rules go here too.

## What belongs here (and what doesn't)

**Record here** — structural refinements:
- a NEW stage (e.g. the proposed *Output Contract* derivation stage)
- a NEW protocol / protocol-family (e.g. candidate-*selector* protocols)
- reordering, splitting, merging, or replacing stages
- changing a stage's gate semantics or its required outputs/canary rules

**Do NOT record here** — these live elsewhere:
- in-stage *rule* tweaks (a better instruction inside an existing stage) → the entity file +
  the `ade-bench-instruction-lever-taxonomy` memory note
- one-off task bugfixes / dataset/image issues → MEMORY notes
- routine run results with no structural lesson

## How to add an entry

Append under **Ledger** using this shape. Keep the *learning* line sharp — it's the payload.

```
### {short title} ({status} {date})
- **Layer:** solver workflow | autoresearch loop
- **Refinement type:** new stage | new protocol | reorder | replace | gate-rule
- **What was tried / decided:** …
- **Finding:** what actually happened (backed by the committed artifact / run, not chatter)
- **Learning:** the reusable rule for the next structural attempt
- **Bears on:** sibling/related hypotheses this should steer
- **Evidence:** entity file (or _archive/…), run dir, MEMORY cross-refs
```

**Process note.** The actual stage graph is *protected scaffolding* — the solver
`README.md` and the autoresearch `README.md` frontmatter are not edited casually. This log
captures the *finding/decision*; applying a structural change goes through `spacedock:refit`
or a dispatched worker, never a direct first-officer edit.

---

## Ledger

### Candidate-selector protocols: self-anchored scoring is a false-green (h0026 REJECTED, 2026-06-05)
- **Status (family, updated 2026-06-11):** **rejected-as-written** for the whole
  `concept-candidate-selector-contract-scorer` fan-out. h0026 falsified it by run; h0031
  confirmed the wall survives genuine candidate diversity + external-criterion arbitration;
  **h0024 (static-contract-scorer-selector) REJECTED 2026-06-11 as a captain strategic
  sibling-kill** (no run — its static build/shape/type rubric is the same self-anchored
  scorer, would fail propose gate G9 judgment-independence); **h0025
  (output-contract-satisfaction-selector) REJECTED 2026-06-11 as a captain strategic
  sibling-kill** (no run — each candidate writes its OWN local contract and is scored on
  artifact-vs-own-contract satisfaction; a uniformly-held wrong answer scores perfect against
  its own contract, so no candidate diversity + no independent IN-decision falsifier => fails
  propose gate G9 judgment-independence — same wall as h0026/h0031); **h0027
  (do-no-harm-selector) REJECTED 2026-06-11 as a captain strategic sibling-kill** (no run —
  its do-no-harm diff filter that rejects candidates with unrelated rewrites is useful HYGIENE,
  but the SELECTION among survivors still scores by best local-contract satisfaction, so it
  changes WHICH candidate wins yet cannot break a uniformly-held plausible-wrong answer; no
  candidate diversity + no independent IN-decision falsifier => fails G9 judgment-independence).
  All four scorer-style siblings (h0024/h0025/h0026/h0027) are now terminal. The still-open
  adversarial re-fire **h0028** intentionally attempts the G9 independence axes
  (forced-divergence + cross-examination) and is kept queued; do NOT file another self-anchored
  selector variant. Family CLOSED.
- **Layer:** solver workflow
- **Refinement type:** new protocol (an *Answer Decision Table Selector* — run N≥3 candidates,
  each emitting a per-option decision table, then pick by local-check completeness + mechanical
  transcription; gated to answer-style tasks).
- **What was tried:** fork the @baseline solver with one added selector protocol block; smoke on
  target `f1011` + two gate-off canaries (`f1007`, `asana001`).
- **Finding:** the target did **not** flip (reward 0.0). The pre-flagged *inert* risk did NOT
  materialize — the solver genuinely ran the protocol (saved candidate decision table C1 with all
  six columns, real `dbt show` local probes, a mechanical selection). It failed because it is a
  **self-anchored false-green**: all three candidates shared the *same* plausible-but-wrong
  reading of one option (committed `ABDE`; ground truth `ADE`, so the hidden `check_option_b`
  test fails), and the scorer grades each candidate against its *own* local checks
  ("support 6/6, contradictions 0"). A uniformly-held wrong answer self-scores perfect and wins;
  there is no independent oracle to break toward the correct answer. Both gate-off canaries held
  PASS with zero selector markers, so the *applicability gating* design itself is sound.
- **Learning:** a candidate-selector is worthless without (a) candidate **diversity** — force
  candidates to *disagree* on borderline options — and (b) an **independent** falsifier for an
  IN decision, not self-scored completeness. Local-check completeness alone re-creates the
  self-anchored trap. This is the recurring "solver is blind to the oracle" wall: self-anchored
  checks give false greens.
- **Bears on:** the three live siblings from the same `concept-candidate-selector-contract-scorer`
  fan-out — **h0024** (static-contract-scorer-selector), **h0025** (output-contract-satisfaction-
  selector), **h0027** (do-no-harm-selector). Each must show *how its selection criterion escapes
  self-anchoring* (independent falsifier / forced candidate divergence) before it earns a full
  run — otherwise it likely repeats h0026.
- **Encoded (2026-06-05, captain direction):** this learning is now a **propose-gate rule — G9
  "Selector independence"** in `_gatekeeper/propose-review-guideline.md`: any multi-candidate /
  selector protocol is screened BEFORE smoke on two axes — (a) *generation independence* (the
  single-session harness cannot supply N independent candidates; require isolation or forced
  divergence) and (b) *judgment independence* (no selection criterion may be anchored solely to
  the candidate's own checks; require an external falsifier). h0026 would have FAILed both axes
  at propose — the "fake-independence selector" is now caught without spending a smoke run.
- **Evidence:** `_archive/h0026-answer-decision-table-selector.md` (`## Smoke result`,
  `## Behavioral analysis`, `## Verdict`); run `a01f97caf6d6462e`. MEMORY:
  `ade-bench-validation-self-anchored-false-green`, `ade-bench-solver-blind-to-oracle`.

### Output Contract: a new derivation stage before any SQL (h0017 + h0023 both NO-GO, 2026-06-05)
- **Layer:** solver workflow
- **Refinement type:** new stage — a derivation stage *between Exploration and Implementation*
  that records each model's grain key-source, ordered column set, per-column types, and the
  complete deliverable set from **named local artifacts** before any SQL is written.
- **What was tried:** concept `concept-contract-first-derivation-stage`, realized by
  **h0017** (grain entity spine — NO-GO), **h0023** (grain/width/deliverable — NO-GO), and
  **h0022** (answer decision table — not yet dispatched).

- **Finding (h0023 smoke, ADDED — run `e018ce3babecc3dc`, 9 tasks = 3 targets + 6 canaries incl
  f1001 convention-bleed sentinel):** automatic NO-GO: **f1001 canary REGRESSED** (was PASS 6/6
  @baseline; smoke 2/6 — `stg_models_use_src_models Got 11`, `stg_races_uses_correct_sources Got 1`,
  `stg_results_uses_correct_sources Got 1`). All 3 targets inert (Got N unchanged:
  quickbooks001 Got 1, ana-eng006 Got 204, ana-eng004 FAIL). The **deliverable-set clause** caused
  the f1 solver to create package-style staging models on a task (f1001) that does not use them —
  convention-bleed from the clause's "resolve ref() graph + create missing models" pattern applied
  too broadly. The *same-thing-same-shape* guard was insufficient to contain it. The copy-shaped
  thesis is inconclusive — neither quickbooks001 (copy missing stg_ models) nor ana-eng006 (DATE
  cast) executed; f1001's regression was the only behavioral signal.
- **Finding (h0017 smoke; 9 tasks = 4 grain targets + 5 cross-family canaries; clean audit
  `tainted:0`, `captured=1`/cell; run `a498329abd068ab5`).** Judge the new stage on three axes:
  - **REACH — it works (the headline).** The stage is NOT inert: it fired on **7/9** cells and
    changed the committed SQL (solver wrote explicit `/* Contract: … */` blocks). This clears the
    bar that sank h0010 (prose) and h0016 (worked-example), both of which were *inert* — committed
    SQL never changed. A structural stage reaches the artifact where in-line prose did not.
  - **SAFETY — no regressions, even when it fires.** 5/5 canaries held PASS; on 3 of them
    (asana001, f1007, quickbooks002) the stage **fired and they still passed** — safe when it
    *engages*, not just safe by skipping. The *same-thing-same-shape* + *derive-not-pad* guards +
    the author/restructure gate contained the h0009 convention-bleed (−3 at full). The stage is
    carry-forward-safe infrastructure.
  - **EFFICACY — 0/4 grain targets, and the *reason* is the payload.** `Got N` byte-for-byte
    unchanged (intercom001/002/003 `Got 7`, asana004 `Got 3`). This is NOT h0010/h0016 inertness —
    it is **reached-but-built-backwards**: the solver wrote the contract *wrong*, naming the
    **child** as the grain driver and building `from child left join entity` (inverse of the
    stage's "entity FROM, children LEFT JOINed" rule). intercom001's own contract comment said
    *"driven by active conversation part rows"* — naming the child IS the bug. It did not copy the
    correct spine from the same-domain analog (`int_intercom__conversation_part_aggregates`) that
    shipped in the workspace; it re-derived and inverted.
- **Learning (updated after h0023):** **a new stage buys REACH but not SAFETY OR EFFICACY by
  default — clause-by-clause analysis is mandatory before shipping.**
  - *h0017 (grain clause):* reach ✓, safety ✓ (5/5 canaries held), efficacy ✗ — the grain clause
    is DERIVE-shaped; the solver inverts the join direction. Fix: make it COPY (copy the verbatim
    `from X left join Y` line of the named analog, cite source file+line).
  - *h0023 (deliverable-set clause):* reach unclear, safety ✗ (**f1001 REGRESSED** — convention-
    bleed), efficacy ✗ — the deliverable-set clause fires too broadly: it treats any installed
    package as a source for missing models, even on projects (f1: F1 stats) that don't use
    package-style staging models. The *same-thing-same-shape* guard did not prevent it. Fix: the
    deliverable-set clause must be **strictly scoped** — only trigger when the task instruction
    explicitly names a missing model or a `*_existence` test fails; never infer "this project should
    have staging models" from the presence of an installed package alone.
  - *Columns/types clauses:* **untested** — f1001's regression contaminated the run before these
    could be distinguished. Their safety and efficacy are genuinely unknown.
  - **The COPY-vs-DERIVE thesis is inconclusive** (h0023 failed before the copy-shaped legs could
    execute). Still the best hypothesis for *why* the grain clause fails; still untested.
  - **Do NOT ship the current Output Contract stage as-is to any future hypothesis.** The
    deliverable-set clause is a regression risk. The grain clause is inert. Strip or scope both
    before re-using the stage.
- **Bears on:** **h0022** (answer decision table — copy-shaped per-option checks; not yet
  dispatched; its clause is orthogonal to deliverable-set, so it is not contaminated by h0023's
  finding and is still worth running); the grain follow-up (0-for-3 exhausted, captain to decide);
  any future Output-Contract-family hypothesis must scope the deliverable-set clause before filing.
- **Evidence:** `_archive/h0017-contract-grain-entity-spine.md` (commit `41054bb`); run
  `runs/ade-bench-h0017-contract-grain-entity-spine/a498329abd068ab5`; `_archive/h0023-output-
  contract-grain-width-deliverable.md` (commits `764bfaa`, `a93412a`); run
  `runs/ade-bench-h0023-output-contract-grain-width-deliverable/e018ce3babecc3dc`. MEMORY:
  `ade-bench-instruction-lever-taxonomy`.

### Output Contract full-48 debug run — agent-plan analysis (h0017, 2026-06-06)
- **Layer:** solver workflow
- **Refinement type:** new stage — *observability/debug* use. A full 48-task run of the already-
  REJECTED h0017 variant (captain-requested; NOT for verification), to read the solver's committed
  `Contract:` blocks as a window into its (often wrong) mental model. Run `19283fb82dbd4ffd`, clean
  strict audit (`tainted:0`, 48/48, 0 errored). Two background readers extracted committed artifacts
  for every changed-verdict task.
- **Finding — score:** 29/48 (0.6042) vs `@baseline` 31/48 (0.6458), **net −2**. GAINS (FAIL→PASS):
  airbnb007, f1006. REGRESSIONS (PASS→FAIL): f1003, f1006-hard, f1010-medium, quickbooks003. 0/6
  grain targets flipped (consistent with the smoke). **The 9-task smoke was blind to ALL 6
  changed-verdict tasks** — none were in the smoke set; the smoke's "0 flips / 5 canaries held"
  saw neither the 2 gains nor the 4 regressions. (The h0009 coverage lesson, made concrete.)
- **Finding — causation (committed-artifact reads, not chatter):**
  - **NOT convention-bleed.** The author/restructure gate worked: it correctly SKIPPED the pure-repair
    tasks (f1006-hard, quickbooks003). No task over-built deliverables or bled a package pattern.
  - **Real stage-caused effects are small:** +airbnb007 (real — the solver wrote "review-date grain +
    calendar-range 28-day lookback" into the contract first, then built to it; the **grain-key-source
    clause** drove the flip) and at most −f1010-medium (premature contract-pinning locked the wrong
    reading of the ambiguous "account for pit stops" spec — *subtract* vs *exclude* pit laps; oracle
    wanted exclude, per a dual `_exclude_pit_stops` seed).
  - **The other 4 flips are orthogonal to the stage:** f1006 (coincidental sibling-convention
    `sum→max` on a *repair* task the stage didn't fire on), f1003 (analytical criterion-drift
    over-inclusion: 6 rows vs 3), f1006-hard (over-engineered repair off baseline's minimal `sum→max`
    path), quickbooks003 (keep-vs-drop "remove all references" misread; baseline was *rescued* by a
    compile failure h0017 never hit).
  - **Common root across the regressions = false-green self-validation** (each worker validated its
    output against its *own* derived expectation, never the oracle) — the recurring wall, not a new
    stage harm.
  - **Caveat:** 1 trial/arm; gpt-5.5 @ xhigh is not bit-deterministic. Part of the ±delta is
    run-to-run variance. Net read: **the stage is ~score-neutral within noise**, not a −2 harm.
- **The `Contract:` block IS a usable reasoning probe (the debug payload):** on a failing task it
  states the wrong mental model in the solver's own words.
  - `asana004` (FAIL): `-- Grain: one row per project_id present in int_asana__project_user` — grains
    on the CHILD intermediate (only projects that have a user) → drops the 3 user-less projects
    (`Got 3`). The bug is legible *in the contract itself*.
  - `airbnb005` (PASS): `/* Contract: one row per reviewed listing_id ... columns ... types ... */` —
    clean grain/columns/types → correct SQL.
- **Learning:**
  - The Output Contract stage is **REACH-positive, ~score-neutral, and observability-positive** — its
    `Contract:` blocks are a genuine "show-your-reasoning" instrument, most valuable on the 14
    fired-and-failed tasks. For a CLEAN standing debug lens, an **observe-only variant** (always write
    the contract block, then build *exactly as baseline* — drop the "build to satisfy" mandate and the
    gate) would give the reasoning window on all 48 at *guaranteed* zero score impact.
  - **airbnb007's real flip validates the rolling-window-as-calendar-range mechanism** → empirically
    motivates **h0018**.
  - **Smoke coverage:** a generative lever's smoke must sample beyond targets+one-per-family — here
    all 6 movers were unsampled. Reinforces the G8 / smoke-set composition rule.
  - **`agent/codex.txt` is the first-officer layer, NOT the solver's contract** — the `Contract:`
    blocks + stage text live in the ensign worker `agent/sessions/*.jsonl`. A grep for "Output
    Contract" on `codex.txt` returning 0 does NOT mean the stage wasn't delivered (it is in the frozen
    solver README, inlined for every task). Read the worker session, not the FO transcript.
- **Bears on:** **h0018** (now empirically motivated by airbnb007); **h0022** (untested, orthogonal to
  the deliverable-set risk); a possible *observe-only* debug-lens variant; the **false-green
  self-validation** wall (the dominant regression root, MEMORY `ade-bench-validation-self-anchored-false-green`).
- **Evidence:** run `runs/ade-bench-h0017-contract-grain-entity-spine/19283fb82dbd4ffd` (per-cell
  `agent/sessions/*.jsonl` = committed Contract blocks + SQL; `verifier/test-stdout.txt` = oracle);
  two reader analyses (this session, 2026-06-06). MEMORY: `ade-bench-instruction-lever-taxonomy`,
  `ade-bench-validation-self-anchored-false-green`.

### Plan Reviewer: a pre-Implementation stage that verifies the Output Contract (simulated on real h0017 data — architecture sound, reverse-inference criterion FAILS, 2026-06-06)
- **Layer:** solver workflow
- **Refinement type:** new stage + new protocol — a *Plan Reviewer* stage **between Output Contract
  and Implementation**: spawn a **fresh-session** subagent to verify the Contract *before* any SQL is
  written, and on failure REJECT with feedback so the author re-derives the contract (a reject-loop).
  The captain's proposed verification criterion was **reverse inference**: from the contract alone,
  reconstruct the task question; if it reconstructs, the contract is "verified."
- **What was tried:** simulated the stage with **4 fresh-session subagents** on real h0017 contracts —
  two methods × {known failer `asana004`, known passer `airbnb005`}. Method **A = reverse-inference**
  (question + contract only); Method **B = independent re-derivation** (question + contract + the
  *existing* `asana__project.sql` the solver starts with + a generic grain invariant: "grain entity
  from the canonical source, never a pre-filtered child"). No oracle/solution/test files given to any
  reviewer (leak-clean — same constraint as the real stage).
- **Finding (verdicts vs ground truth):**
  - **A1 reverse-infer / asana004 (FAIL):** REJECT — but **for the wrong reason** and it **missed the
    actual bug.** It reconstructed the agent's *wrong* 13-row grain happily; it rejected only because it
    flagged the **correct** `users = user_name‖role` column as an "unverifiable invention." A noisy
    false-reject on a correct detail; the grain defect went unnamed. Its reject feedback would not fix
    the grain.
  - **A2 reverse-infer / airbnb005 (PASS):** VERIFIED (high) — correct accept.
  - **B1 re-derive+invariant / asana004 (FAIL):** **VERIFIED** (high) — it *saw* the invariant and
    reasoned around it correctly: the intermediate *may* stay at 13 rows because `asana__project`'s
    surviving `left join … coalesce(…,0)` restores the spine downstream. Internally valid; still wrong
    vs the oracle.
  - **B2 re-derive+invariant / airbnb005 (PASS):** VERIFIED (high) — correct accept, **no false
    alarm** (the invariant did not over-trigger on a clean contract).
- **Ground truth (operator-side, confirmed):** oracle seed `INSERT 16`; agent built **13**; equality
  test `Got 3` (the 3 user-less projects). The oracle's `int_asana__project_user_agg.sql` wraps the
  aggregates in `from project p left join agg left join count` — it pushed the **16-project spine
  INSIDE the new intermediate**. The agent kept the intermediate at the raw CTE grain (13) and left the
  spine in `asana__project`. **Both refactors yield a correct `asana__project`; the oracle grades the
  *intermediate* and picked 16 by convention.** The task question never says which.
- **Learning:**
  - **The stage *architecture* is sound and SAFE** — a fresh-session plan review before Implementation
    with a reject-loop is reasonable, and checking the *plan* beats checking only the *result*.
    Independent re-derivation (B) was safe on both cells (no false-reject), unlike reverse-inference
    (A1's bogus reject).
  - **The reverse-inference *criterion* provably does not work.** It tests **internal consistency**
    (can I reconstruct a plausible question?), and a plausible-wrong plan is internally consistent *by
    construction* — that is what makes it plausible. On the real failer it both *missed* the grain bug
    and *false-rejected a correct column*. Reverse-inference relocates the false-green to the plan
    stage; it does not break it. **Do not adopt reverse-inference as the verifier.**
  - **`asana004` is the *unbreakable* class even for the strong criterion.** It is **underdetermined**:
    two valid refactors exist, both produce a correct final model, the question is silent, and the
    discriminating fact (intermediate carries the full entity spine) lives **only in `solution/` + the
    hidden test** — in *neither the question nor the existing code*. No leak-clean reviewer can pick the
    oracle's convention. This is the **solver-blind-to-oracle wall** in its purest form.
  - **Where a Plan Reviewer WOULD earn flips:** the class where **the existing code contradicts the
    contract** (e.g. a contract that grains on a filtered child *when the consumer does NOT restore the
    spine*). Method B catches those; method A does not. asana004 simply is not that class.
  - **Same wall as the candidate-selector finding (h0026):** verification by *self/internal* consistency
    can't catch a uniformly-held plausible-wrong plan; you need an **independent** signal, and for the
    grain family no non-leaking independent signal exists. The only remaining non-leaking shot is on the
    *author* side, not the reviewer: a **prescriptive** contract clause ("when extracting an aggregate
    into a named `<entity>_agg` intermediate, the intermediate MUST carry the full entity key set from
    the canonical source") — h0017's grain-key-source clause, sharpened. Empirically a long shot (the
    mild version flipped airbnb007, not asana004).
- **Bears on:** the Output-Contract family (a Plan Reviewer is the natural "verify the contract" add-on
  — but only with method B, and only for code-contradicts-contract bugs); the candidate-selector
  siblings **h0024/h0025/h0027** (same requirement: an *independent* IN-decision falsifier, not
  self/internal consistency); the grain follow-up (reaffirms 0-for-N exhausted — the discriminating
  fact is oracle-only; concede unless the sharpened prescriptive-author clause is tried).
- **Real-world framing:** this is "the oracle problem" — see `verification-without-oracle.md` for how
  accounting/science/intelligence/compilers solve verification-without-ground-truth, the
  *independent-vs-correlated* test every check must pass, and why **reconcile-to-raw (double-entry)**
  beats plan-review for the value-divergence cluster.
- **Evidence:** this session's 4-subagent simulation (2026-06-06); run
  `runs/ade-bench-h0017-contract-grain-entity-spine/19283fb82dbd4ffd/ade-bench-asana004__z4s6LiP/verifier/test-stdout.txt`
  (`Got 3`, seed `INSERT 16`); oracle
  `datasets/ade-bench-asana004/solution/solutions/int_asana__project_user_agg.sql` (spine inside the
  intermediate) + `instruction.md` (silent on grain). MEMORY: `ade-bench-solver-blind-to-oracle`,
  `ade-bench-validation-self-anchored-false-green`, `ade-bench-instruction-lever-taxonomy`.

### Autoresearch loop: keep the `smoke` gate; judge it by learning-rate, not flip-rate (captain decision, 2026-06-05)
- **Layer:** autoresearch loop
- **Refinement type:** gate-rule — the `propose → smoke → full` go/no-go gate.
- **Decision:** keep `smoke` as the gate for every new idea. It is a cheap triage + *learning*
  lane (~30 min for a gated lever; roughly 1/10th the cost of a full 48-task run) that kills
  inert levers and catches regressions before we commit a full run. The metric for the stage is
  not flip-rate — it's whether smokes produce sharp *whys* that seed the next hypothesis.
- **Earned rules:**
  - *Generative (ungated) levers MUST carry a cross-family canary panel.* Earned from **h0009**,
    which looked like a GO on a targets-only smoke and then lost **−3** at full scale on
    f1/quickbooks passers the smoke never ran. **A canary dropping FAIL is a NO-GO regardless of
    how many targets flipped.**
  - *Gated levers can trim the panel* to a couple of cross-family tripwires (~3 tasks total),
    since the lever can't fire on non-target families (e.g. h0026, h0020).
  - *Baseline / first run skips `smoke`* (`propose → full`) — the anchor is a direct full run.
- **Bears on:** every hypothesis dispatch; the smoke-set composition rule in the autoresearch
  `README.md`.
- **Evidence:** autoresearch `README.md` (`### smoke` stage definition); MEMORY
  `ade-bench-instruction-lever-taxonomy`; this session's smoke-stage discussion.

### Gate-rule + smoke-set refit — encode the h0012 self-correcting-lever lesson (G10, G8-perturbable, variance-caution) (captain decision, 2026-06-07)
- **Layer:** autoresearch loop
- **Refinement type:** gate-rule (propose gatekeeper) + smoke-set composition rule.
- **What was decided:** after **h0012** (reconcile-to-raw) passed a clean 9-task smoke then lost
  **−4** at full, encode three protections so the same failure is caught *before* a full run:
  1. **New gatekeeper rule G10 — "Self-correcting lever false-positive risk"** (propose gate),
     parallel to G9-for-selectors. Applies to any check / reconcile / validate-and-fix lever.
     Three axes: (a) scope — generative vs figure-change-gated; (b) independence source —
     separately-sourced raw `SELECT FROM source` vs a re-derived CTE that re-correlates;
     (c) check-don't-replace — investigate disagreement, never mandate replacing a simple-correct
     path. FAIL → REVISE (gate it) unless the *ungated, fix-on-disagreement, re-derived* check IS
     the idea (→ back to `hypothesis`). Rubric + output-format table updated to ten rules.
  2. **G8 strengthened** — one canary per family is *necessary but not sufficient*; for the
     family(ies) sharing the targets' construct, require ≥2 **perturbable** canaries (passers the
     lever can actually fire on). A stable passer the lever skips proves nothing.
  3. **Smoke-set composition (README) + propose smoke-set guidance** mirror the perturbable-canary
     rule, and add a **variance caution**: a lone flip with no artifact-proof may be variance
     (h0012's f1006 flipped at smoke, reverted at full) — a GO rests on artifact-proven flips +
     held perturbable canaries.
- **Finding (what motivated it):** h0012's generative reconcile damaged 4 f1 passers — it pushed
  them off a simple-correct `sum→max` onto a wrong "structurally different" path and false-green-
  validated against a CTE sharing the model's own logic (correlated-error). The 9-task smoke
  (single f1 canary f1001, a stable passer the rule never perturbed) was structurally blind to it.
- **Learning:** the gate now screens the *whole self-correcting family* — not just h0012 but the
  drafted reconcile pair h0029/h0030 — for the generative-false-positive / re-correlation /
  replace-the-path failure mode at propose, and the smoke can no longer be fooled by a single
  unperturbed-canary panel or a variance flip.
- **Bears on:** **h0029** (column-set reconcile) and **h0030** (grain row-count reconcile) — both
  will now trip G10 unless gated to figure-changes + repointed to a raw-source signal + softened
  to check-don't-replace before dispatch; every future check/reconcile/validation lever; the
  smoke-set composition for any generative lever.
- **Evidence:** `_gatekeeper/propose-review-guideline.md` (G10 added; G8 + rubric + output-format
  updated; `last-updated: 2026-06-07`); autoresearch `README.md` (`### smoke` Smoke-set
  composition + `### propose` smoke-set guidance); `_archive/h0012-validation-independent-recompute.md`
  (run `3d8294de42b726e1`); MEMORY `verification-without-oracle-real-world`,
  `ade-bench-instruction-lever-taxonomy`.

### Dual Output Contract Arbitration — new pre-Implementation stage: two independent contracts + evidence-hierarchy arbitrator (h0031, REJECTED — rejected-as-written, 2026-06-07)
- **Status:** **rejected-as-written** — protocol-family change tested and **cleanly falsified at smoke** (no full run; the hypothesis's own falsifier fired verbatim). Terminal.
- **Layer:** solver workflow (`solver_workflows/h0031-dual-output-contract-arbitration/README.md`).
- **Refinement type:** NEW stage / NEW protocol-family — one `## Stage: Dual Output Contract
  Arbitration` inserted between Exploration and Implementation: Phase 1 shared evidence snapshot,
  Phase 2 two independent contracts (B = forced-divergence, must not read A), Phase 3 an
  evidence-hierarchy arbitrator writing machine-readable `arbitration.json`
  (SELECT_A / SELECT_B / MERGE_NON_CONFLICTING / REJECT_BOTH / ABSTAIN) before any SQL.
- **Finding (smoke, run `0de9870ae2220bca`, 8/11 pass, clean strict audit tainted:0, captured:1
  all 11):** the stage is **NOT inert and NOT theatre — it materialized real, independent,
  evidence-bearing artifacts** on every target, yet **moved zero targets and zero distances-to-pass
  vs `@baseline`**. Two sub-findings:
  1. **Protocol fidelity is real (refutes the G7 inert-risk watch-item, on the targets).** All 3
     targets wrote a genuine `arbitration.json` to disk via `apply_patch` (verified `test -f` +
     `ls`), and the committed SQL matched the arbitrated `selected_claims` (AC-5 held). **Route B
     genuinely diverged from A on real claims (the G9/AC-1 single-session wall was cleared on the
     targets):** intercom001's B drove conversation_created_at from `conversation_history` with an
     explicit `attempt_to_defeat_route_a` block; ana-eng004's B swapped the product source from
     `dim_products`→raw `northwind.products` (supplier_company→supplier_ids); f1011's B proposed a
     CEF option reading the arbitrator rejected. Arbitration used INDEPENDENT probes, not transcript
     plausibility — intercom rejected B via a raw conservation check (`part_rows_with_history_match:
     0`, a history join would not conserve parent rows); ana-eng004 used a coverage probe
     (`dim_products misses 16 of 102 inventory rows; raw products covers all 102`).
  2. **The protocol does NOT beat the blind-to-oracle wall — it hits it in arbitration form.** All
     three targets land at the *identical* distance-to-pass as baseline: ana-eng004 "has less
     columns than solution" (exact width is oracle-only — `arbitration.json` itself records
     `target_schema_yaml: "No schema YAML declares obt_product_inventory"` — yet
     `abstained_claims: []`); intercom001 "Got 7 results" (the part_type→assignment/reopen/contact
     metric mapping is oracle-only — local data had `assignment_rows:0, reopen_rows:0, comment_rows:0`,
     i.e. NO visible rows to validate the mapping — yet selected at tier-3, not abstained); f1011
     committed **ABDE**, the *byte-identical wrong answer* baseline committed, failing the same
     `check_option_b` — B=IN was supported by a self-derived local probe that correlates with the
     wrong reading (the h0026 self-anchored-scorer / correlated-error false-green, now with a
     two-route apparatus on top). **AC-4 (abstention honored) was violated exactly where it mattered:
     every target had `abstained_claims: []` on the one load-bearing claim that was genuinely
     oracle-only.** When the workspace cannot decide, two independent contracts still converge on the
     same locally-plausible-but-unsupported premise, and the arbitrator picks it instead of abstaining.
- **What the stage did to committed artifacts independent of target movement / whole-set coverage:**
  the new stage was **selectively exercised — fired on only 4 of 11 cells** (the 3 targets + f1001),
  each of which wrote a real `arbitration.json`. The **7 pure-passer canaries**
  (airbnb001 / ana-eng001 / asana001 / f1007 / quickbooks002 + the perturbable doublets
  **ana-eng002 / asana003**) **did NOT materialize the protocol at all** — no `arbitration.json`
  written; the `selected_claims`/decision-enum string hits there are README-skeleton echo, not
  produced artifacts. So the README's "across the WHOLE smoke set" framing is false in practice: the
  solver ran the protocol only on tasks it found ambiguous and skipped it on tasks it found easy.
  Upside: because the 7 easy canaries were untouched, **zero canaries regressed** (all 8 panel
  members 1.0, full pass-count match) is genuine unchanged-baseline behavior, not luck — the h0012
  perturbable-doublet tripwire (ana-eng002 / asana003) did not fire because the lever never reached
  those constructs.
- **Learning:** **genuinely-independent route B + external-criterion arbitration are TABLE STAKES,
  not a contribution** — they were both achieved (route B diverged on every target; the arbitrator
  scored on raw conservation/coverage probes, never transcript plausibility) and they STILL
  reproduced baseline's exact wrong answers (f1011 → byte-identical ABDE). Adding a second
  independent contract route + an evidence-hierarchy arbitrator does NOT create an oracle. On an
  oracle-only disagreement (exact column width, exact part_type→metric mapping, single-option
  inclusion) the only correct move is `ABSTAIN`, and an arbitrator that *can* abstain still won't if
  it is permitted to promote a tier-3 "defensible local" guess to a SELECT. The missing piece is an
  **ENFORCED abstention gate** (not a third route): a load-bearing claim with no tier-1/tier-2
  visible support (instruction or schema) AND no route-deciding conservation/coverage signal MUST be
  marked `ABSTAIN`, and an abstained load-bearing claim must not be silently filled by either
  contract's tier-3 default. Until abstention is *enforced* rather than *permitted*, dual-contract
  arbitration reproduces the single-author answer on exactly the tasks it was built to fix. Same wall
  as `solver-blind-to-oracle` / h0026 / the `verification-without-oracle` synthesis — confirmed a
  third time, now for the two-route generative form, so **more candidate generation is exhausted**;
  the live lever is changing the OBJECTIVE (abstain) rather than chasing the oracle.
- **Bears on:** **h0026** (self-anchored-selector — h0031 confirms its wall survives genuine
  candidate diversity + external judgment: the two-route apparatus is h0026 with the divergence and
  external-criterion fixes applied, and it still false-greens via correlated-error on the
  oracle-only claim); **h0017 / h0023** (single-contract Output-Contract stage — a SECOND independent
  contract does not rescue the single-author failure mode; the wall is the oracle, not author count);
  the **solver-blind-to-oracle / verification-without-oracle** family (h0026 + h0031 now make the
  blind-to-oracle wall a META-PATTERN — do NOT reflexively file more candidate-generation/arbitration
  levers); and every future multi-route / arbitration / selector protocol (h0024 / h0025 / h0027 and
  any successor of h0031): generation-independence + external-criterion judgment are table stakes, not
  the contribution; the contribution must be an *enforced* abstention on oracle-only claims. Confirms
  G9 (selector independence) and G10 (self-correcting false-positive) as the right gate axes, and
  shows the in-session forced-divergence substrate CAN diverge (a partial answer to the G9 WARN)
  without solving the underlying oracle problem.
- **Evidence:** run `runs/ade-bench-h0031-dual-output-contract-arbitration/0de9870ae2220bca`
  (clean strict audit; `per_trial_outcomes.json`); committed `arbitration.json` for ana-eng004
  (MERGE_NON_CONFLICTING) / intercom001 (SELECT_A) / f1011 (SELECT_A, answer ABDE) extracted from
  `agent/sessions/*.jsonl`; baseline `runs/ade-bench-baseline/622bdedac572b479` (f1011 baseline
  answer = ABDE, same `check_option_b` fail; ana-eng004 + intercom001 same distance-to-pass);
  MEMORY `ade-bench-solver-blind-to-oracle`, `verification-without-oracle-real-world`,
  `ade-bench-validation-self-anchored-false-green` (h0026).

### Combined-full confirmation methodology + the single-trial-variance-masking wall (h0034, E2+E3 combined full, 2026-06-07)
- **Layer:** autoresearch loop
- **Refinement type:** gate-rule / methodology — a **combined-full confirmation** variant (carry ≥2
  previously-smoke-GO'd in-stage rules in ONE fork, skip smoke, run `propose → full` once) for run-economy
  + an interaction check; and a finding about what a single-trial full run can and cannot bank.
- **What was tried:** h0034 forked `codex-ade-dbt-minimal` and lifted the two smoke-GO'd Implementation
  rules VERBATIM into one fork — E2/h0019 anti-cross-join (airbnb009) + E3/h0018 rolling-window calendar-
  RANGE copy (airbnb007) — then ran the FULL 48-task confirmation once (`trials: 1`) to confirm both flips
  at scale and promote `@baseline` if the paired delta cleared. Run
  `runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303`, clean strict audit (`tainted:0`).
- **Finding — NET +0, NO-PROMOTE (the headline):** `stratified_pass_at_1 = 0.6458` = `@baseline` exactly.
  GAINS: airbnb009 (E2, HELD, artifact-proven `mom_agg_reviews.sql` BETWEEN-spine) + f1011 (incidental
  variance). REGRESSIONS: asana003 (build error `asana__daily_metrics` `cast('None' as date)` from solver
  staging re-wiring) + f1005 (constructor-points `QUALIFY` rewrite off-by-2). **Both regressions are
  rule-independent gpt-5.5 non-determinism** — neither E2 nor E3 touches asana staging or F1 constructor
  points. 10k paired bootstrap (seed 20260607) over the 48 per-task deltas → **95% CI on mean delta
  [-0.0833,+0.0833] = [-4,+4] tasks**, straddles 0.
- **Finding — the combined-full methodology itself worked as a confirmation vehicle.** The two rules did
  NOT interact to harm passers (the regressions were unrelated to both); the fork construction was clean
  (combined added-set = union of the two source forks' additions, byte-for-byte; leak-guard byte-identical);
  the strict audit was clean. Running both in one full is a legitimate run-economy + interaction-check move.
  **But it cannot bank a lone +1.**
- **Learning — THE SINGLE-TRIAL-VARIANCE-MASKING WALL (the binding constraint now).** At `trials:1` over
  n=48, gpt-5.5@xhigh manufactures ±2 incidental flips/run independent of any lever; the paired CI is ±4
  tasks — **wider than a single-lever +1 signal**. So the do-no-harm tripwire (CI must exclude a regression)
  is **structurally unsatisfiable for a +1 lever at trials=1**. airbnb009 is a real, artifact-proven,
  lever-attributable +1 — and it could NOT be banked because two unrelated noise flips cancelled it.
  **The binding constraint is now measurement VARIANCE, not lever quality.** And we cannot just run
  `trials>1` to shrink the CI: the **freeze-repo concurrency race** (MEMORY
  `ade-bench-freeze-repo-concurrency-race`) pins the spec to `trials:1` (shared freeze git repo → "cannot
  lock ref HEAD" when two trials commit at once). **So the variance wall is currently a HARNESS-LIMIT wall**
  — to close it, make the freeze repo per-task/per-trial in razorback (pass `benchmark_task_id` into
  `compute_sealed_hash`, or unique `RAZORBACK_FREEZE_DIR` per trial), which unblocks multi-trial paired
  confirmation for the whole program.
- **Learning — the MULTI-MODEL-TARGET TRAP (E3/airbnb007).** A single-model lever cannot credit a flip on a
  target scored by ≥2 models when it addresses only one. airbnb007 is scored by `daily_agg_nps_reviews`
  (rolling-window, the E3 target) AND `listing_agg_nps_reviews` (per-listing lifetime NPS, no window). At
  full the calendar-RANGE copy reached `daily_agg` and that test PASSED — yet the task scored 0 because
  `listing_agg` failed by 2 rows (a model E3 never matches). The h0018 smoke-GO was variance on the
  unaddressed model, not a fix (the h0012/f1006 pattern). **Add a smoke/gatekeeper check: enumerate a
  target's scored models before crediting a single-model lever; precondition-match < all models ⇒ treat a
  single-run flip as variance.** Full detail in `bug-type-taxonomy.md` → "The multi-model-target trap".
- **Bears on:** every promote decision (do not promote a lone +1 on a single trial); the E2-only re-confirm
  path (`_proposal/retrospective-2026-06-07.md` §5.1); any future combined-full confirmation (clean vehicle,
  but cannot bank sub-CI signal); razorback freeze-repo fix as the program-unblocking move; the propose
  gatekeeper (add the multi-model-target check).
- **Evidence:** `h0034-combined-e2-e3-full-confirmation.md` (`## Run result`, `## Behavioral analysis`,
  `## Verdict`); run `runs/ade-bench-h0034-combined-e2-e3-full-confirmation/1880d6497bdd6303`; baseline
  `runs/ade-bench-baseline/622bdedac572b479`; `_proposal/retrospective-2026-06-07.md`; MEMORY
  `ade-bench-freeze-repo-concurrency-race`, `verification-without-oracle-real-world`,
  `ade-bench-instruction-lever-taxonomy`.

---

## h0032 (E0) — instrument-validation GATE before any second-path check is trusted (new protocol)

- **Decision (structural):** introduce a per-check **instrument-validation gate** — before a downstream
  hypothesis (E1/h0030, E4, E5) is trusted to use an "independent second-path" check, the check must be
  proven **two-sided discriminating** on a controlled fixture: FIRES on a known injected error AND stays
  SILENT on a known-good. Inert (silent-on-injected) = the h0010/h0016 prose signature; correlated
  (fires-on-known-good, or false-greens on a correlated read) = the h0008/h0012 signature. Runs OFFLINE
  (no `rk run`, no solver README) against the real fixture DuckDB; ships nothing to the solver, so the
  propose leak-guard does not apply — the gate is the INDEPENDENCE sharp test instead.
- **Result:** E1/h0030 raw-parent row-count reconcile **CLEARED** (2 f1 models); E5 ref-graph/_existence
  completeness **CLEARED**; E4 dtype-vs-**declared-contract** **KILLED — the artifact does not exist**
  (zero `data_type:`/`contract:` across all of `shared/projects/dbt/`), but a dtype-vs-**raw-source**
  substitute **CLEARED narrowly** (pass-through key/identity cols only; derived aggregates have no raw
  oracle). Harness + machine-readable 2x2: `_artifacts/h0032-e0-harness/{harness.py,result_2x2.json}`.
- **Two load-bearing caveats (proved by adversarial probes, fold into E1's design):**
  1. The reconcile is sound ONLY if it reads the **immutable raw source** (`{{ source() }}`/loaded
     tables). Reading a solver-rebuilt intermediate re-introduces the correlated error and false-greens
     (probe A: correlated read 737==737 passes; true-raw read 737≠860 fires). This is the h0012 wall
     restated for the reconcile.
  2. A bare `COUNT(*)` reconcile is BLIND to drop-N-add-N (probe B: 860==860, silent); the E5 key-level
     anti-join catches it. **E1 should pair the count with the completeness anti-join**, not ship the
     count alone — they are complementary, not redundant.
- **Bears on:** **E1/h0030** (proceed, but bind the raw read to `source()` and pair count+completeness);
  **E4** (re-spec to dtype-vs-raw-source; drop the declared-contract framing — no contract exists; scope
  it to pass-through columns); **E5** (proceed). General: every future "independent check" hypothesis
  should pass an E0-style two-sided + independence gate (incl. an adversarial correlated-read probe)
  BEFORE a 48-task run — this is the operational form of the `verification-without-oracle` independent-
  vs-correlated test. Confirms the gate axes G9 (independence) and G10 (self-correcting false-positive).
- **Evidence:** `_artifacts/h0032-e0-harness/result_2x2.json` (`checks[]` all CLEARED on the 2x2 +
  `adversarial{}` correlated_error_trap / count_blind_spot); fixture = f1 DuckDB from the ade-bench
  `databases` GitHub release (raw source + canonical @baseline outputs ship together);
  baseline `runs/ade-bench-baseline/622bdedac572b479` (f1001 passing, model outputs canonical).

### Gate-rule refit — encode the multi-model-target trap (G11) + green-via-package-namespace inertness (G7) (captain decision, 2026-06-08)
- **Layer:** autoresearch loop
- **Refinement type:** gate-rule (propose gatekeeper).
- **What was decided:** after the two end-of-program retrospectives
  (`_proposal/retrospective-2026-06-07.md` §5.4 + `…-06-08.md`), fold two post-G10 findings into
  the propose gatekeeper so they screen before any future flip hypothesis spends a run:
  1. **New rule G11 — "Multi-model-target variance risk"** (advisory, WARN-only, parallel to G7).
     A single-model lever cannot credit a flip on a target scored by ≥2 models when its precondition
     matches fewer than all of them; a single-run flip there is variance on the unaddressed model.
     Earned from **h0034/E3** (airbnb007: calendar-RANGE copy passed `daily_agg_nps_reviews` but the
     task scored 0 on `listing_agg_nps_reviews`, which the lever never touches). The rule tells the
     gatekeeper to enumerate the target's scored models statically (taxonomy list + dataset tests, no
     `rk`). Recommended in BOTH retrospectives but never previously encoded.
  2. **G7 strengthened** — added the second inertness mode **green-via-package-namespace** (E5/h0035):
     a build / deliverable-completion rule goes inert when the project already builds GREEN through the
     package's own namespace, so there is no red trigger to fire on. Marked the **incomplete-deliverable
     / missing-models family DEAD 5-for-0** (h0009/h0013/h0015/h0023/h0035) so any new build-rule is
     pre-flagged.
  3. **Future-scope note** — recorded the *credit-time* form of G11 (confirm the artifact landed on
     every scored model from the run's `verifier/test-stdout.txt`) as a smoke-gate item for the
     not-yet-built `smoke-review-guideline.md`, alongside the inert-detector + verify-the-artifact items.
- **Finding (what motivated it):** the oracle-problem flip program CONCLUDED at net +0 — `@baseline`
  still 31/48 (32 once airbnb009 is banked). The README/prompt lever space is exhausted; G11 + the G7
  update are "bank the lesson so it is not relearned," and only unlock new flips if the program reopens
  with a benchmark-design change (out of scope per program decision #4).
- **Learning:** the propose gate now predicts the multi-model-target variance trap and the
  green-via-package inertness mode at filing time — the two post-G10 failure modes that cost runs
  (h0034, h0035) without being caught.
- **Bears on:** any future flip hypothesis aimed at a multi-model target (airbnb007 and siblings) or
  any build/deliverable-completion rule; the deferred airbnb009 banking run (single-model, single
  scored model → G11 N/A, judge by artifact); a future `smoke-review-guideline.md`.
- **Evidence:** `_gatekeeper/propose-review-guideline.md` (G11 added; G7 + rubric + output-format
  updated; `last-updated: 2026-06-08`); `_proposal/retrospective-2026-06-07.md` (§5.4) +
  `_proposal/retrospective-2026-06-08.md` (§2.1–2.2); `_archive/{h0034,h0035}`; MEMORY
  `ade-bench-oracle-program-concluded`, `ade-bench-instruction-lever-taxonomy`,
  `ade-bench-single-trial-judge-by-artifact`.

### Observe-only debug lens: the freeze-notes routing precondition is DEAD in this harbor layout (h0039 REJECTED-inert, 2026-06-08)
- **Status:** **rejected-as-written** — new-stage structural lever tested and cleanly falsified at smoke
  (no full run); rejected via INERT, not contamination. The stage never wrote its `plan_review.json`
  artifact because the `/razorback-freeze` "exactly one child directory" routing precondition is
  structurally unmet in this harbor layout (the @baseline run never wrote freeze notes either). Terminal.
- **Layer:** solver workflow
- **Refinement type:** new stage — an observe-only `## Stage: Observe` between Exploration and
  Implementation that ALWAYS writes a machine-readable `plan_review.json` (grain/columns/types/
  divergence + a `dbt show` key-count per model) to the sanctioned non-graded notes location, then
  builds EXACTLY as baseline (no gate, no build-to-satisfy mandate). This is the WORKFLOW-REFINE
  *Opening #2 observe-only-lens*, finally built and run.
- **What was tried:** fork @baseline (`codex-ade-dbt-minimal`), add exactly one observe-only stage;
  8-task contamination smoke (6 cross-family Got-N tripwires + the fired-and-failed cells asana004 /
  intercom001). Success was INVERTED: Got N unchanged on passers (gate-strip held) + record present on
  the failers (lens not inert).
- **Finding:** the Observe stage went **fully inert at the artifact level on all 8 cells** —
  `plan_review.json` was never written anywhere. The stage routes its record to the notes location
  *only* "if `/razorback-freeze` exists and has exactly one child directory" (the precondition the
  baseline README already uses for `exploration.md`/`implementation.md`/`validation.md`). In every
  cell the worker probed `/razorback-freeze`, found a **degenerate layout** (`find … -type d` returns
  `/app` / `0` / dataset content, never a clean single child), logged *"zero child directories … not
  applicable,"* and skipped the record. Crucially the **@baseline run ALSO never wrote any freeze
  notes** — the precondition has been silently failing all along; h0039 is the first hypothesis to
  depend on it and thereby surface it. Strict audit clean (8/8). The lone passer drop (asana003,
  17/17 → 11/17, a `ref(tmp)`→`var()` refactor that broke 6 equality tests) is **variance, not
  contamination**: with no record ever written, nothing could leak into the build; the failers held
  Got-N byte-identical (Got 3 / Got 7), the signature of a fully-inert lens.
- **Learning:** **the `/razorback-freeze` "exactly one child directory" notes precondition is dead in
  this harbor task layout — do not route any required artifact through it.** Any future
  observe/record/debug-lens stage that must produce a durable artifact has to (a) write to a location
  that does NOT depend on that precondition (e.g. a fixed in-`/app` scratch path the verifier ignores,
  or an unconditional notes file), and (b) be checked by mirroring the artifact OUT of the container
  into the run-dir, because the committed dbt project state (and any in-container notes) is torn down
  and never lands under `runs/<…>/<cell>/`. The G7-high inertness the propose gate flagged
  materialized — but via the routing precondition short-circuiting, NOT via "an artifact told it
  changes nothing"; the on-disk-`apply_patch` + `dbt show` mitigation never executed. Confirms the
  WORKFLOW-REFINE Opening #2 hope ("guaranteed zero score impact, reasoning window on all 48") is
  unreachable as specified: zero score impact held, but the corpus was empty.
- **Bears on:** h0041 (observe-only triage ledger — SAME routing dependency; must fix the notes
  location before it can deliver a corpus); h0038 (plan-review Method-B — depends on a written
  contract existing); the archived h0017 Output Contract finding (its `Contract:` blocks lived in the
  ensign worker `sessions/*.jsonl`, NOT a notes file — that is the only place reasoning has ever
  durably survived in this harness, so a debug lens should target the session transcript, not
  `/razorback-freeze`).
- **Next step (captain decision, 2026-06-08):** NO separate follow-up hypothesis is filed for the
  write-path fix. Routing durable debug-lens artifacts to an unconditional path (or the worker session
  transcript) instead of `/razorback-freeze` folds into **h0041's propose** — h0041 (observe-only triage
  ledger) carries the identical routing dependency and is the natural home to land the fix once and for
  all. This entry is the structural record of *why* the fix is needed; h0041 is where it gets built.
- **Evidence:** entity `hypotheses/h0039-observe-only-debug-lens.md`; run
  `runs/ade-bench-h0039-observe-only-debug-lens/e84f83324081c22d` (audit clean 8/8; score 0.625;
  asana003 `patch_apply_end` shows the `ref→var` repoint; airbnb001 worker session logs the
  "zero child directories … not applicable" decision verbatim); baseline
  `runs/ade-bench-baseline/622bdedac572b479` (no freeze notes written — precondition unmet at baseline
  too). MEMORY `ade-bench-single-trial-judge-by-artifact`, `ade-bench-instruction-lever-taxonomy`.

### Observe-only triage ledger: the stdout/session-transcript routing FIX works — an observe-only stage CAN durably emit a substantive record with zero build contamination (h0041 smoke GO, 2026-06-08)
- **Status:** **smoke GO → full** — new-stage structural lever; the h0039 routing fix is VALIDATED. First
  positive demonstration in this loop that an observe-only stage durably emits a substantive record
  without contaminating the build. (Expected flips {0} by construction — this is a method instrument, not
  a flip-seeker; the deliverable is the `would_abstain` map that de-risks h0040.)
- **Layer:** solver workflow (`solver_workflows/h0041-observe-only-triage-ledger/README.md`).
- **Refinement type:** new stage — exactly one observe-only `## Stage: Triage ledger` running the h0040
  three-clause trigger (instruction / existing `schema.yml` / raw `{{ source() }}` count + key-level
  anti-join) but emitting ONLY `triage.json {claim, clause_results, would_abstain}` to a FIXED `/tmp`
  scratch path UNCONDITIONALLY and then `cat`-ing it to stdout. Reverts/alters/gates nothing; build
  proceeds exactly as baseline.
- **What was tried:** fork @baseline (`codex-ade-dbt-minimal`), add exactly one observe-only stage with
  the **h0039-fix routing** (unconditional write to `/tmp/triage.json` + print-to-stdout so the record
  lands in the durable session transcript, NOT through the dead `/razorback-freeze` precondition). 8-task
  contamination smoke (5 cross-family Got-N tripwires airbnb001/ana-eng001/asana001/f1007/quickbooks002 +
  the survivor airbnb009 + the fired-and-failed cells intercom001/ana-eng007). Run
  `runs/ade-bench-h0041-observe-only-triage-ledger/45c2ba6667a47a60`, clean strict audit (`tainted:0`,
  8/8, captured=1 all 8), score 0.625 (5/8 = the baseline split, zero score impact).
- **Finding — THE ROUTING FIX WORKED (the make-or-break vs h0039).** Where h0039 wrote NOTHING (its
  `plan_review.json` routed through the dead `/razorback-freeze` "exactly one child" precondition), h0041
  produced a **filled, non-empty triage record on 8/8 cells**, recovered from the `sed`/`cat`/`tee` stdout
  in each cell's `agent/sessions/2026/06/08/*.jsonl`. The `/tmp/triage.json` scratch is correctly ABSENT
  from the run-dir (torn down) — a naive `test -f` in the run-dir would falsely read inert (the h0039
  trap); the stdout/session-transcript capture is the verified durable home (matches the h0017 finding
  that reasoning only survives in the worker `sessions/*.jsonl`). `Got N` was byte-unchanged on all 5
  passers and all 3 failers vs @baseline — the observe-only gate-strip held, ZERO contamination. No
  `would_abstain: true` anywhere; all 8 cells ran Implementation normally (4–9 `apply_patch` each); the
  only "revert/abstain" grep hits are the README guardrail prose echoed in the dispatch prompt, not action.
- **Finding — SCHEMA DRIFT (the substantive caveat for h0040).** The solver did NOT adhere to the spec's
  fixed record shape. THREE shapes appeared across 8 cells: (i) exact spec schema with boolean
  `clause_results` + explicit `would_abstain` (asana001/quickbooks002/intercom001/ana-eng007 — all
  `would_abstain:false`); (ii) boolean variant with renamed keys / no `would_abstain` key (airbnb001 bare
  booleans T/T/F; ana-eng001 `three_clause_check` + `classification:"no-op"` T/F/F); (iii) narrative
  `status`+`evidence` shape, NO boolean, NO `would_abstain` (airbnb009 `supports_*`, f1007 `supports` +
  `classification`/`minimum_fix`). The semantic decision (≥1 clause supports ⇒ decidable ⇒ no-abstain) is
  recoverable in every case and the distribution read is robust to the drift, but a downstream enforced
  rail (h0040) that PARSES `would_abstain` as a literal field would mis-parse 4 of 8 cells (field absent)
  and must NOT default those to "abstain."
- **Finding — `would_abstain` DISTRIBUTION = 0/8 flagged true.** Every cell found its load-bearing claim
  decidable. Most important: NO passer flagged ⇒ h0040 would have predicted ZERO false-reverts on this
  panel (would not suppress any of the 5 real passers), and the survivor airbnb009 was found decidable ⇒
  h0040 would not suppress the one real fix. BUT `raw_source_probe` came back NOT-deciding on 8/8 cells —
  the tier-3 raw-source/coverage probe (the only independent clause) never independently decided a claim;
  every "decidable" verdict rested on the instruction or schema.yml clause (the self-anchored / instruction-
  echo sources). So this panel does NOT certify the trigger as a clean oracle-only detector — it confirms
  the trigger leans on the non-independent clauses, exactly the Round-1 h0030 false-negative / h0036
  coverage-masks-value mode. The ledger is a useful MAP (no over-abstention on this panel), not a
  certification.
- **Learning:** (1) **An observe-only stage CAN durably emit a substantive record with zero build
  contamination** — route the record via an UNCONDITIONAL write + print-to-stdout (the session transcript),
  NEVER via `/razorback-freeze`. This is the reusable write-path for any future debug-lens / observe-only
  stage (closes the h0039 Opening-#2 gap). (2) **A free-form record schema drifts under gpt-5.5** — three
  incompatible shapes emerged from one fixed spec; an enforced consumer must derive its decision from the
  clause results, not from a possibly-absent literal field, OR hard-pin the schema and refuse to proceed
  without the literal boolean. (3) **For h0040 revert-mode: the over-abstention risk is LOW on this panel
  (0/8 flagged, survivor decidable), but the trigger's "decidable" verdicts rest on the non-independent
  clauses** — the independent raw-source probe never decided, so h0040 inherits the Round-1
  mis-discrimination wall and would be deciding reverts on instruction/schema echo, not on an independent
  oracle-only signal. Green-light precondition for h0040 = MET (no false-reverts predicted here) but with
  a sharp caveat (the abstain decision is not resting on the independent clause).
- **Bears on:** **h0040** (the M2 enforced abstention rail — this de-risk says the over-abstention risk is
  low on this panel, but flags two must-fixes: hard-pin/derive the `would_abstain` schema, and recognize
  that the trigger's decidability rests on non-independent clauses so an enforced revert inherits the
  Round-1 wall); **h0039** (this is its named routing fix, now VALIDATED — the `/razorback-freeze`
  dependency was the whole problem, and stdout/session-transcript routing solves it); any future
  observe-only / debug-lens stage (use the unconditional-write + print-to-stdout pattern); the
  solver-blind-to-oracle / verification-without-oracle family (the raw-source probe never independently
  deciding is the same wall, now visible in the clause-level data).
- **Evidence:** entity `hypotheses/h0041-observe-only-triage-ledger.md` (`## Smoke result`,
  `## Behavioral analysis`); run `runs/ade-bench-h0041-observe-only-triage-ledger/45c2ba6667a47a60` (audit
  clean 8/8 tainted:0, captured=1; score 0.625; the 8 triage records recovered from
  `agent/sessions/2026/06/08/*.jsonl`); baseline `runs/ade-bench-baseline/622bdedac572b479` (5 passers /
  3 failers, byte-identical Got N). MEMORY `ade-bench-solver-blind-to-oracle`,
  `verification-without-oracle-real-world`, `ade-bench-single-trial-judge-by-artifact`,
  `ade-bench-instruction-lever-taxonomy`.

### Observe-only triage ledger CONFIRMED at full 48-cell scale: routing scales, 0/48 would_abstain, both net-0 flips are solver variance — the contract held (h0041 full + analyze CONCLUDE, 2026-06-10)
- **Status:** **PASSED-as-instrument (terminal; captain decision 2026-06-10)** — the observe-only mechanism
  was validated END-TO-END at 48-cell scale; the M3 observe-only de-risk line is CLOSED. PASSED here = "ran
  cleanly to a real result" (validated mechanism + the all-48 `would_abstain` map), NOT a @baseline
  promotion. Everything the smoke found reproduces at 48-cell scale; nothing new breaks. @baseline NOT
  promoted (net 0, {0}-flip by construction; registry verified unchanged at `622bdedac572b479`); no
  follow-up filed (`stop`).
- **Layer:** solver workflow (`solver_workflows/h0041-observe-only-triage-ledger/README.md`), same frozen
  skeleton as smoke (content-hash `sha256:812509727c…b4738bf` byte-identical — no smoke→full drift).
- **Run:** `runs/ade-bench-h0041-observe-only-triage-ledger/fe1505abeeddabff`, all 48 tasks, `trials:1`;
  strict audit `{clean:48, tainted:0}`, `captured=1` on all 48; score `stratified_pass_at_1 = 0.6458`
  (31/48) = exactly @baseline, `n_errored=0`.
- **Finding — ROUTING SCALES (4th-scale confirmation of the make-or-break h0039 fix).** 48/48 cells
  durably emitted a triage record to the session transcript (the unconditional `/tmp/triage.json` write +
  stdout `cat`/`printf`/`tee`/`*** Add File`). Not one cell went inert. The 8-cell smoke proof generalizes.
- **Finding — THE CONTAMINATION CONTRACT HELD; net 0 is TWO offsetting flips = solver VARIANCE, not a
  gate-strip leak.** Net 0 vs @baseline decomposes into +1 airbnb009 (FAIL→PASS) and −1 f1006-hard
  (PASS→FAIL); 46/48 byte-held. Reading the committed `apply_patch` SQL on both flips proves variance, not
  contamination: airbnb009 full committed a minimal `IN(DISTINCT)`→`BETWEEN MIN/MAX` fix (correct) where
  baseline over-rewrote and broke it; f1006-hard full committed baseline's correct `sum`→`max` PLUS a
  second over-refinement (`row_number()` season-rank) that broke its own fix. Triage record carries NO SQL
  on either; zero triage→SQL coupling. The observe-only gate-strip did not leak. (`rk runs diff` TypeErrors
  on ade-bench dirs → paired delta from per_trial_outcomes.json, slug-paired, 10k bootstrap: mean +0.0,
  95% CI [−0.0625, +0.0625].) Honest precision: "net 0" is aggregate-level, NOT byte-identical on those
  two single-trial-variance cells (airbnb009 is the documented non-reproducible survivor).
- **Finding — THE M3 MAP: 0/48 would_abstain, no passer flagged, survivor decidable.** A future enforced
  rail would predict ZERO false-reverts on this fixed 48. Schema-drift confirmed at scale: literal
  `would_abstain` key on only 38/48; 10/48 use drifted/nested (`{verdict,evidence}`,
  `{evaluated,supports_claim}`) / narrative (`load_bearing_claim`+`fixed_three_clause_check`) shapes — an
  enforced consumer MUST DERIVE abstain from the clause results, never parse the field + default-to-abstain.
  raw_source_probe fired on ~26/48 (vs inert on the smoke 8) but never OVER-abstained and never independently
  decided a cell the instruction/schema clauses didn't — conservative map, NOT a certified clean oracle-only
  detector (the h0030/h0036 mis-discrimination wall persists at the clause level).
- **Learning (the durable positive — a PROVEN, REUSABLE primitive):** the **durable observe-only
  write-path — an unconditional `/tmp/<record>.json` write + a `cat`-to-stdout step that lands the record
  in the worker session transcript** — is a PROVEN positive primitive that SCALED to 48/48 cells with zero
  build contamination. This is the structural primitive any future observe / record / debug-lens stage
  should REUSE; it is explicitly NOT the dead `/razorback-freeze` "exactly one child" precondition (verified
  empty in the @baseline run-dir) that made the sibling h0039 go inert. The h0039→h0041 arc is the canonical
  worked example: route durable records through stdout/session-transcript, never through `/razorback-freeze`.
  Secondary learnings: (a) an observe-only instrument's success metric is "the contract held"
  (`tainted:0`, no record→artifact coupling, aggregate net 0) — judge the committed ARTIFACT (the
  `apply_patch` SQL), not the aggregate alone, because single-trial variance still moves a couple of
  borderline cells at the CELL level (airbnb009 up / f1006-hard down here, both solver-own SQL). (b) The two
  enforced-rail hardening requirements (derive abstain from the clause booleans; the trigger leans on
  non-independent clauses) are RETROSPECTIVE de-risk knowledge — **h0040, the enforced abstention rail this
  M3 was built to de-risk, already concluded REJECTED-inert**, so there is no live consumer to harden; do
  NOT re-open the enforced-rail / arbitration-architecture family (D9).
- **Bears on:** **any future observe / record / debug-lens stage** — REUSE the proven unconditional-write +
  cat-to-stdout write-path (the durable positive primitive). **Any future ENFORCED consumer of a
  `would_abstain`-style record** — the map's two caveats steer it directly: (1) DERIVE abstain from the
  clause booleans, never parse the literal `would_abstain` field + default-to-abstain on absence (10/48
  schema-drifted, no literal key); (2) the trigger is a CONSERVATIVE map not a certified oracle-only
  detector (raw_source_probe under-fires as a *sole* decider — the h0030/h0036 wall), so an enforced rail
  built on it would lean on the non-independent instruction/schema clauses. **h0040** (REJECTED-inert — this
  map is now retrospective; the green-light precondition it was to feed has no live consumer; D9 stays
  closed). **h0039** (its routing fix, validated at smoke, now confirmed at scale). The solver-blind-to-oracle
  / verification-without-oracle family (raw-source probe under-firing as a *sole* decider is the same wall in
  the clause-level data). Closes the M3 observe-only de-risk line of the Round-2 workflow-stage program.
- **Evidence:** entity `hypotheses/h0041-observe-only-triage-ledger.md` (`## Run result` ANALYZE section,
  `## Behavioral analysis` FULL RUN lead, `## Verdict`); run
  `runs/ade-bench-h0041-observe-only-triage-ledger/fe1505abeeddabff` (audit clean 48/48 tainted:0,
  captured=1; score 0.6458; 48 triage records + the two flips' committed `apply_patch` SQL recovered from
  `agent/sessions/2026/06/10/*.jsonl`); baseline `runs/ade-bench-baseline/622bdedac572b479`. MEMORY
  `ade-bench-oracle-program-concluded` (airbnb009 stochastic survivor), `ade-bench-single-trial-judge-by-artifact`,
  `verification-without-oracle-real-world`.

### Plan Review (Method B): the FIRST LIVE run of independent re-derivation — Method B ALSO false-rejects; the REJECT verdict is a guess, not a locally-grounded contradiction (h0038 smoke NO-GO, 2026-06-09)
- **Status:** **rejected-as-written** (smoke NO-GO → conclude/REJECTED; terminal) — new-stage
  structural lever (a pre-Implementation `## Stage: Plan Review` between Exploration and
  Implementation, generative-but-record-only). The DETECTOR is falsified — Method B FALSE-REJECTS
  live (the first live run of the never-run, Round-1-only-simulated criterion); the RECORD-ONLY
  RAIL is SAFE (no passer regressed) but the verdict layer is USELESS (its only signal, REJECT, is
  an ungrounded guess). @baseline UNCHANGED at 31/48, NOT promoted. Forked the @baseline solver
  `codex-ade-dbt-minimal`.
- **Idea:** from (task instruction + the EXISTING model SQL + a stated generic leak-clean grain
  invariant — "a model's grain entity comes from its canonical source relation, never from a
  pre-filtered child; a completeness/repair output must keep every key the consumer relies on") RE-DERIVE
  the intended grain/keys INDEPENDENTLY, COMPARE to what the code does, emit `verdict:REJECT` ONLY on a
  LOCALLY-VISIBLE code-contradicts-contract bug (with `reason` + `contradicting_line`), else
  `PROCEED_UNDETERMINED` and build EXACTLY as baseline. NEVER reverse-inference (Method A). Single-path
  (one build reviewed once against an external invariant; selects nothing) — distinct from the
  G9-exhausted candidate-arbitration family.
- **Routing:** REUSED the h0041-VALIDATED unconditional `/tmp/plan_review.json` + `cat`-to-stdout
  write-path (NOT the dead `/razorback-freeze` single-child precondition that made h0039 inert). **It
  held a second time** — `plan_review.json` recovered on 8/8 cells from `agent/sessions/*.jsonl` +
  `agent/codex.txt`. This re-confirms the observe-only write-path as the standing pattern for any
  record-emitting stage.
- **Finding — verdict distribution (of the 7 cells that emitted a concrete record) 4 PROCEED_UNDETERMINED
  / 3 REJECT, +1 missing record (ana-eng001 emitted template-only — h0041 schema drift); Method B
  FALSE-REJECTS LIVE.**
  The decisive result: asana004 — the cell the proposal said MUST abstain (`PROCEED_UNDETERMINED`,
  oracle-only grain per Track Z) — instead emitted **REJECT** with `contradicting_line: "from
  project_user"`. The stage pattern-matched the invariant's "never grain from a pre-filtered child"
  template onto a FROM clause and fired, but it could NOT locally verify the contradiction (whether the
  canonical grain is `project` vs `project_user` is fixed by hidden expected output). The REJECT is a
  **guess shaped like a contradiction**, not a locally-grounded one. asana001 + f1007 (PASSERS) also
  drew REJECT verdicts. So Method B does NOT escape the Method-A false-reject failure — applied as a
  generic *pattern* against a generic *invariant*, it false-rejects exactly where the deciding fact is
  correlated-out of every local relation. The one "correct" abstention on a target (intercom001) was an
  **accident of empty SQL** ("no existing intercom__threads SQL present" — a creation task), not the
  predicted `_fivetran_active`-re-correlation discrimination.
- **Finding — record-only HELD and is the ONLY thing that kept the panel safe (G10 distinction
  earned its keep).** The two REJECTed passers held PASS with byte-unchanged committed SQL and
  ERROR=0; the "record, not a gate or build mandate" rule prevented the h0012 damage-the-passer
  false-green. Net: G8 panel clean (no passer reward regressed; the single real build delta is
  asana004 Got 3→6, variance on a non-passer CREATE task). So the stage is SAFE but
  NON-DISCRIMINATING — its only non-trivial signal (REJECT) is a guess it correctly refuses to act
  on. Safe-but-useless = no live lever.
- **Finding — the record-emit is not even reliable (a second h0041-drift confirmation).** ana-eng001
  emitted NO concrete `plan_review.json` — only the README template (`<the re-derived…>`,
  `<REJECT | PROCEED_UNDETERMINED>`) survives in its transcript (0 concrete `intended_grain` lines vs
  3–4 on every other cell). So the free-form record schema drifts under gpt-5.5 and a cell can skip
  the emit entirely; the "standing reasoning probe" value is itself leaky (7/8 here), reinforcing the
  h0041 rule that an enforced consumer must hard-pin the schema / refuse to proceed without the literal
  field rather than trust a free-form emit.
- **Learning:** (1) **An independent JOIN-shape re-derivation cannot distinguish a
  locally-decidable contradiction from an oracle-only grain convention — so on the wall it GUESSES
  REJECT.** Method B is empirically NO different from Method A: a generic leak-clean invariant
  ("never grain from a pre-filtered child") applied as a *pattern* fires on a plausible-but-correct
  FROM clause (`asana004` → `from project_user`) because the canonical-grain fact (`project` vs
  `project_user`) lives ONLY in the hidden expected output, not in any local relation. There is no
  locally-visible signal that separates "code contradicts the contract" from "the convention is
  oracle-only," so the re-derivation defaults to REJECT exactly where it should abstain. This closes
  the standing "is the never-run Method B worth running?" question: NO — the re-derivation cannot
  beat the oracle (same wall as `solver-blind-to-oracle` / `verification-without-oracle-real-world`;
  the invariant is a pattern, the deciding fact is the correlated-out residual). (2) **An
  emit-a-verdict stage is only as safe as its record-only rail** — at a ~3-of-7 (~43%) REJECT rate,
  a full run would spread ~20 ungrounded REJECTs across 48 cells; the record-only design is the sole
  reason that is harmless, and it delivers zero upside. (3) The `/tmp`+stdout routing is
  twice-validated as a durable write-path (durable 7/8 here, after the durable 8/8 at h0041 — re-use
  it for any future record-emitting stage), BUT the free-form record schema drifts under gpt-5.5
  (1/8 cells, ana-eng001, emitted template-only and skipped the concrete emit) — a SECOND SIGHTING
  after h0041, so any enforced consumer must hard-pin / derive its decision from the schema rather
  than trust a free-form emit.
- **Bears on:** the verify/re-derive-without-oracle family (Method B now empirically dead alongside
  Method A — do NOT file further "re-derive the grain and compare" levers, single-path or otherwise);
  **h0040 / M2 (the enforced abstention rail)** — the free-form record SCHEMA-DRIFT is now a 2ND
  SIGHTING after h0041 (ana-eng001 emitted only the README template, no concrete record), so any
  ENFORCED consumer that PARSES this trigger must hard-PIN the record schema (refuse to proceed
  without the literal field) and must NOT trust this free-form emit to drive a revert — an
  enforced revert on a possibly-absent / pattern-matched verdict would both inherit the
  guesses-REJECT wall above AND mis-parse the drifted cells; h0017 (Output Contract, which DID
  build-to-a-contract and inverted joins — this confirms the safer record-only framing avoids that
  damage but at the cost of any flip); any future verdict/REJECT-emitting stage (must keep the
  record-only rail; a fix-on-REJECT variant would damage passers). The candidate-arbitration family
  (G9) remains separately exhausted (h0026).
- **Evidence:** entity `hypotheses/h0038-plan-review-method-b.md` (`## Smoke result`,
  `## Behavioral analysis`); run `runs/ade-bench-h0038-plan-review-method-b/ee924fbc9d3b0b20` (audit
  strict clean 8/8 tainted:0 coverage_missing:0, captured>0 all 8; score
  `stratified_pass_at_1=0.75` 6/8; 7/8 concrete plan_review records recovered, distribution 4
  PROCEED_UNDETERMINED / 3 REJECT, ana-eng001 emitted template-only); baseline
  `runs/ade-bench-baseline/622bdedac572b479` (asana004 Got 3,
  intercom001 Got 7; 6 panel passers held). MEMORY `ade-bench-solver-blind-to-oracle`,
  `verification-without-oracle-real-world`, `ade-bench-oracle-program-concluded`,
  `ade-bench-single-trial-judge-by-artifact`, `ade-bench-instruction-lever-taxonomy`.

### Reference Mining: a generative copy-the-analog stage REACHES committed SQL and the own-sibling-first gate is artifact-proven anti-bleed AT SCALE — but {0} flips on the width oracle (h0037 REJECTED — rejected-as-written / not-promotable, 2026-06-10)
- **Status:** **rejected-as-written / not-promotable** (CAPTAIN, conclude 2026-06-10) — new-stage
  structural lever; the E-RMS systematization of the h0019 lone-survivor engine. Full 48-run scored
  **0.625 (30/48), net −1 vs @baseline 0.6458 (31/48)**, **0 flips on the known wall**; @baseline
  UNCHANGED at `runs/ade-bench-baseline/622bdedac572b479` (31/48), registry NOT touched, no follow-up
  filed. NOT promoted because there is no flip and the −1 is unrelated single-trial variance (not a
  lever regression). **REJECTED-as-written, but this is the ONLY R2 structural lever with a clean
  POSITIVE mechanism result — the reach + anti-bleed-at-scale primitive is the bankable value, not a
  score.** Forked the @baseline solver `codex-ade-dbt-minimal`.
- **Layer:** solver workflow (`solver_workflows/h0037-reference-mining-stage/README.md`).
- **Refinement type:** NEW stage — exactly one `## Stage: Reference Mining` between Exploration and
  Implementation (generative on model-authoring tasks, gated-skip on repairs/no-ops). It (a) names
  the target's layer+grain, (b) finds the closest already-passing IN-PROJECT sibling (own siblings
  FIRST, installed-package template ONLY as fallback — the deliberate anti-h0023-bleed gate), (c)
  records `Analog: <file>:<line-range>` + FROM/join/spine/window to an UNCONDITIONAL
  `/tmp/reference_mining.json` + `cat`-to-stdout (the h0041-validated routing, NOT the dead
  `/razorback-freeze` precondition), (d) copies that construction VERBATIM as the Implementation
  skeleton, adapting only leaf columns/source. Carries a worked-example SQL skeleton (h0019 form) to
  clear the G7 abstract-prose inertness bar.
- **What was tried:** 10-task G8 panel: target ana-eng004 (obt_product_inventory width) + 3 intended
  OBT/wide canaries (ana-eng002 / ana-eng002-medium / ana-eng005) + one passer per other family
  (airbnb001 / asana001 / f1001 / quickbooks002) + reach reads intercom001/003. Run
  `runs/ade-bench-h0037-reference-mining-stage/6671b5e449bd0975`, clean strict audit (`tainted:0`,
  10/10, captured=1 all 10), score 0.70 (7/10 = the baseline split).
- **Finding — REACH (the headline; clears the h0010/h0016 + h0033 bars).** On ana-eng004 the stage
  fired fully and CONCRETELY: it wrote a filled record (`analog: obt_sales_overview.sql:1-78`,
  `own_sibling`, `from_relation/spine_key_source: fact_sales`, grain = one row per inventory_id) and
  the analog's construction SHAPE (OBT fact-spine + LEFT JOIN dim, single `source` CTE, `SELECT *`)
  REACHED the committed `obt_product_inventory.sql` — with the spine correctly adapted to the target's
  own `fact_inventory` (not a verbatim `fact_sales` copy) and one analog column convention adopted
  (`p.attachments`). NOT inert-prose (committed SQL carries the cited construction) and NOT
  green-but-inert (attribution proven on the artifact, not the score). The h0019 lone-survivor engine
  generalizes into a generative stage that reaches the artifact.
- **Finding — EFFICACY {0} (the D6 width oracle wall, exactly as predicted).** ana-eng004 still fails
  `AUTO_obt_product_inventory_equality` "has less columns than solution__obt_product_inventory" —
  **byte-identical to @baseline**. The sibling `obt_sales_overview` is WIDER (≈60 cols / 3-fact-join)
  than the target, the target already followed the analog's fact-spine skeleton, so copying the
  analog's shape adds nothing decision-relevant and copying its column ladder only widens — while the
  width oracle's exact column set lives ONLY in the hidden `solution__*`. The deciding DROP/ADD is
  oracle-only; no leak-clean analog encodes it. Same `solver-blind-to-oracle` ceiling as D6
  (h0011/h0023/h0029). intercom001/003 reach flat at `Got 7`.
- **Finding — SAFETY (the own-sibling-first gate is ARTIFACT-PROVEN anti-bleed; the decisive workflow
  result).** f1001 — the passer h0023's deliverable-set clause broke 6/6→2/6 via convention-bleed —
  **FIRED the stage here (creation/mixed `src_*` task) and held 6/6 PASS**, including the exact three
  tests h0023 bled. Its record shows it correctly found `closest_own_same_layer_sibling: "none found …
  no existing src_* models"` and did NOT fall to a package template — it cited the project's OWN
  `source('f1_dataset',…)` convention. So the own-siblings-FIRST / package-only-as-fallback gate
  removes the h0023 convention-bleed vector: the stage fired and held, it did not hold by skipping.
  The Output-Contract deliverable-set clause that caused the h0023 bleed is absent here by design.
- **Finding — the intended OBT perturbable canaries were REPAIRS (smoke-panel caveat for next time).**
  ana-eng002 / ana-eng002-medium are scored on the SAME `obt_product_inventory` model as the target,
  but their instructions are "fix the syntax error" / "fix the error" — pure repairs, so the
  author/restructure gate correctly SKIPPED them (no record written) and they could NOT exercise the
  generative copy. ana-eng005 is a dedup repair (also skipped). The only cells that genuinely fired
  the generative copy were ana-eng004 (target) and f1001 (creation); **f1001 is the load-bearing
  regression-safety datum, not the OBT doublet.** Lesson for G8 panel design: verify a "perturbable"
  canary is an AUTHORING task (creation/restructure), not a same-model REPAIR — a repair on the
  target's model is invisible to an author-gated generative stage.
- **Finding — routing held a 3rd time; schema drifted a 3rd time.** `/tmp`+stdout routing recovered
  the record on both firing cells (after h0041 8/8, h0038 7/8) — the standing observe-only write-path.
  But the free-form record SCHEMA DRIFTED again (3rd sighting): ana-eng004 used the spec keys, f1001
  used `records[]`/`task_classification`/`construction_skeleton`. Semantic content recoverable both
  ways; any enforced consumer must derive its decision from content, not a literal field.
- **Learning (FINAL — after the full 48-run + analyze):** **Reference-mining is the one R2 structural
  positive: it REACHES committed SQL AND the own-sibling-first gate is anti-bleed AT SCALE — a reusable
  positive structural primitive — but a structural shape-copy cannot supply the oracle-only
  width/value/semantic deciding fact, so it flips nothing on the known wall.** Four reusable facts:
  (1) **A generative copy-the-analog stage CAN reach the committed SQL** (clears the h0010/h0016
  inert-prose bar AND the h0033 green-but-inert bar) when it carries a worked-example skeleton + cites
  a named local analog — reach-systematization of the h0019 survivor engine, confirmed at full (RM
  fired on ~21/48 authoring cells). (2) **Own-siblings-FIRST / package-only-as-fallback is the correct
  anti-bleed gate, and it is SAFE AT SCALE** — across all 48, NO held passer was broken by a
  wrong/wider analog (the smoke→full h0012 convention-bleed-at-scale fear is FALSIFIED by committed
  artifact): f1001 fired, found no own sibling, cited its own `source()` convention, held 6/6
  (vs h0023's deliverable-set clause which bled f1001 6/6→2/6 via a package); intercom001 took the
  package-fallback path and still held its baseline FAIL. **This is the gate shape to carry forward for
  any future copy/template lever.** (3) **Copying a CONSTRUCTION ANALOG cannot supply the oracle-only
  deciding fact** — on a width target the deciding column set lives only in the hidden `solution__*`,
  and the closest sibling encodes a DIFFERENT (wider) convention, so a faithful analog copy is
  efficacy-zero exactly where it reaches; AND a structural construction-copy is **INERT on
  task-semantic dimensions it does not encode** (pit-stop handling, max-vs-latest — the f1010-medium /
  f1006-hard full-run drops). Copy-the-shape fixes shape/grain/join/spine, not the deciding business
  rule or the oracle DROP/ADD. The D6 width family stays dead. (4) **An author-gated generative stage
  is invisible to same-model REPAIRS** — pick AUTHORING (creation/restructure) canaries, not same-model
  repairs, to test regression risk. **Net structural verdict: the own-sibling-first reach primitive is
  REUSABLE, but only when PAIRED with a semantic/value lever — alone it reaches but cannot decide.**
- **Bears on:** **the own-sibling-first anti-bleed REACH primitive is the one structural POSITIVE of
  the R2 set — reusable when PAIRED with a semantic/value lever** (alone it reaches committed SQL but
  cannot decide the oracle-only fact). Carry this gate shape forward, not as a standalone flip lever.
  Sharp **contrast: h0023** bled f1001 6/6→2/6 via its deliverable-set package-copy clause; h0037's
  own-siblings-FIRST / package-only-as-fallback gate is the SAFE version of the same idea, artifact-
  proven anti-bleed across all 48 — when a future Output-Contract or copy/template lever needs a "find
  the analog" step, use h0037's gate, never h0023's deliverable-set clause. Also bears on: the D6 width
  family (h0011/h0023/h0029 — confirms copying a construction analog does NOT supply the oracle-only
  column set; do not re-file width-flip levers); the `solver-blind-to-oracle` /
  `verification-without-oracle` family (the width oracle is the same wall); any future generative
  copy/template/convention lever (use own-siblings-first + worked-example + /tmp+stdout routing; pick
  AUTHORING canaries, not same-model repairs); the standing observe-only write-path (3rd validation).
- **Evidence:** entity `hypotheses/h0037-reference-mining-stage.md` (`## Smoke result`,
  `## Behavioral analysis`); run `runs/ade-bench-h0037-reference-mining-stage/6671b5e449bd0975` (audit
  clean 10/10 tainted:0, captured=1; score 0.70; ana-eng004 committed `obt_product_inventory.sql` +
  filled `reference_mining.json` recovered from `agent/sessions/2026/06/09/*.jsonl`; f1001 6/6 PASS +
  its no-own-sibling record); baseline `runs/ade-bench-baseline/622bdedac572b479` (ana-eng004 "has
  less columns" byte-identical; f1001 6/6; intercom001/003 Got 7). MEMORY
  `ade-bench-solver-blind-to-oracle`, `verification-without-oracle-real-world`,
  `ade-bench-single-trial-judge-by-artifact`, `ade-bench-instruction-lever-taxonomy`.

- **FULL-RUN ADDENDUM (analyze, 2026-06-09→10; run `…/5d707b3cdf7901b3`, all 48):** scored **0.625
  (30/48), net −1 vs `@baseline` 0.6458** = **+1 / −2** (paired bootstrap obs −1, 95% CI [−5,+2],
  straddles 0). Strict audit clean (`tainted:0`, 48/48 captured a verifier outcome). **The −1 is
  unrelated single-trial solver-reasoning variance, NOT a lever regression — the smoke→full h0012 fear
  (gate insufficient at scale) is FALSIFIED by committed-artifact forensics:**
  - `f1006-hard` DROP — REPAIR; RM correctly did NOT fire (no `Analog:`). Solver chose `row_number()/
    latest` vs baseline's correct `max(points)`; lost 2 edge-case rows (`Got 2`). Analog never engaged.
  - `f1010-medium` DROP — CREATION; RM FIRED citing `constructor_points` (a points-SUM) which has ZERO
    pit-stop logic → **inert on the failing dimension**. Solver over-engineered "subtract pit-stop
    duration" vs baseline's correct "exclude pit-stop laps" (`Got 1092`). NOT a wrong/wider-analog bleed.
  - `asana002` GAIN — incidental config-task flip (RM did not fire; known causal-flip task).
  - **Whole-48 reach scan:** RM fired on ~21/48 authoring cells, correctly skipped repairs/no-ops/config,
    and **NO held passer was broken by a wrong/wider analog copy** — the own-sibling-first gate is **safe
    at scale** (confirms smoke). `intercom001` exercised the package-fallback path (cited a
    `dbt_packages/dbt_utils/integration_tests/…` template, no own sibling) and held its baseline FAIL.
  - Target `ana-eng004` held FAIL at the **byte-identical** width wall ("has less columns…", a
    `dbt_utils.equality` Compilation Error), cited analog `obt_sales_overview.sql:1-78` reaching the
    committed SQL — **reach finding holds at full**.
  - **New reusable boundary:** a structural construction-copy analog is **INERT on task-semantic
    dimensions it does not encode** (pit-stop handling, max-vs-latest) — "copy the construction shape"
    fixes shape/grain/join, not the deciding business rule. **Recommended conclude: `@baseline` NOT
    promoted (net −1, no flip); bank the knowledge gains.** Evidence: run `…/5d707b3cdf7901b3` per-cell
    `verifier/test-stdout.txt` + `agent/sessions/**/*.jsonl` apply_patch payloads; baseline
    `…/622bdedac572b479` (f1006-hard `max(points)`; f1010-medium exclude-pit-laps).


### Enforced abstention rail (Track Z / M2): the REVERT never fires — clause-1/clause-3 self-credit collapses the AND-of-NOTs, so the gate is inert on every oracle-only cell (h0040 smoke REJECTED-inert, 2026-06-09)
- **Status:** **rejected-as-written** — new-stage structural lever (the 5th `## Stage:`, a pre-commit
  enforced-abstention triage gate, the ONLY R2 lever that ACTS) tested and cleanly falsified at smoke
  (no full run). Terminal. REJECTED-inert: the enforcement is inert on every oracle-only cell (the named
  G7 kill-path fired) while the revert primitive is provably **bleed-free** (G10 clean) and therefore
  **bankable** for a future flip-seeking-lever pairing. @baseline UNCHANGED at 31/48
  (`runs/ade-bench-baseline/622bdedac572b479`); NOTHING promoted; no follow-up filed.
- **Layer:** solver workflow
- **Refinement type:** new stage (a 5th `## Stage: Pre-commit abstention triage (enforced)` between
  Validation and Finalization — the ONLY R2 lever that ACTS: it mechanically reverts edits when a fixed
  three-clause trigger (instruction / existing `schema.yml` / raw `{{ source() }}` count + key-level
  anti-join) is all-NO, with `abstain` DERIVED by AND-of-NOTs and `triage.json` routed to `/tmp` +
  `cat`-to-stdout). The enforcement primitive h0031 named as missing.
- **What was tried:** fork @baseline (`codex-ade-dbt-minimal`) + one new enforced-revert stage; smoke on
  13 cells — Panel A (5 oracle-only @baseline failers: asana004, intercom001, ana-eng004, f1002,
  ana-eng007) where the revert SHOULD fire, + Panel B (8 passers incl. perturbable doublets ana-eng002 /
  ana-eng002-medium and asana003/asana001, f1 convention-bleed tripwire f1007/f1001) where it must NOT.
- **Finding (two decisive reads, from the SESSION TRANSCRIPT — triage.json is written by the spawned
  ensign sub-agent and `cat`-ed to stdout, landing in `agent/sessions/**/rollout-*.jsonl`, NOT the
  run-dir; the orchestrator `codex.txt` carries the prose summary):**
  **(A) G7 enforcement INERT on all 5 Panel-A cells.** Every Panel-A cell produced a well-formed,
  populated `triage.json` (3-6 explicit claims, derived `abstain`), but **`abstain=false` on every claim
  → ZERO `reverted_files` everywhere.** Reward stayed 0.0 (== baseline) on all 5 — the gate never fired
  where it was supposed to. Mechanism: the solver self-credits **clause-1 (instruction)** as `true`
  because the task instruction names the columns/grain/target at the surface (asana004: 4/4 instr=true;
  f1002: 5/5 instr=true AND schema=true via `__stats.yml`), and/or **clause-3 (raw_source_probe)** as
  `true` claiming the raw probe "decides" the claim (intercom001 4/6, ana-eng004 2/3, ana-eng007 1 claim
  on raw alone) — so the AND-of-NOTs never reaches abstain. This is NOT h0031's empty
  `abstained_claims:[]` (permission-not-fired); it is a **fully-instantiated trigger that evaluates to
  NO-abstain** because the cells are oracle-blocked on *aggregation semantics / value mapping*, not on
  whether a column is named — and clause-1 reads surface naming as "deciding the quantity."
  **(B) G10 PASS — zero wrong revert.** All 8 Panel-B passers held reward 1.0 with zero real
  `reverted_files`; zero passer regressed. The gate-to-`abstain==true` scoping held: nothing was ever
  reverted, so the inverted-false-green could not arise. (ana-eng002 even classified its task a "pure
  syntax fix" → `{"claims":[]}`.) Strict audit clean (tainted 0/13), captured>0 on all 13,
  `stratified_pass_at_1=0.6154` (8/13), net flips vs @baseline = **0** (by construction).
  **Schema drift returned (4th routing test after h0041/h0038/h0037):** the PINNED nested schema did NOT
  hold uniformly — asana004 used the pinned `clause_results:{...}` + `reverted_files`; intercom001
  FLATTENED to `{formula, claims:[{name, instruction, schema_yml, raw_source_probe, abstain}]}` (no
  `reverted_files`, added `formula`/`name`); ana-eng002 emitted `{"claims":[]}`. The durable stdout/
  session-transcript ROUTING worked on all 13 (the h0041 fix holds); it is the record SHAPE that drifts.
- **Learning:** an "enforced-abstain trigger as README prose cannot compel abstention because the clause
  evaluation is itself model-discretionary and the solver self-credits a clause true** — so the enforced
  revert is **structurally inert against an oracle gap the same way the read-only levers are.** This is the
  **same discretionary wall as h0031, reached through a NEW mechanism:** h0031 died at
  *permission-not-fired* (`abstained_claims:[]`); h0040 dies at *the clause booleans the enforcement derives
  from are themselves discretionary self-reads* — the two non-independent clauses (clause-1 instruction,
  clause-2 schema) are read generously (surface column-naming counts as "names the deciding quantity") and
  the one independent clause (clause-3 raw-source probe) is self-credited as "decides it," so abstain≈never.
  The h0031 wall is NOT beaten by *deriving* abstain from booleans when the booleans are discretionary.
  **For the AND-of-NOTs to fire, at least one clause must be evaluated by something the solver cannot talk
  itself out of** — the same independent-redundancy requirement as every checking lever
  ([[verification-without-oracle-real-world]]). On the safety side this is the *good* failure: the revert
  PRIMITIVE is PROVABLY bleed-free (0 wrong reverts across 8 passers incl. 4 perturbable canaries; G10
  clean) — but its protective value is **unobservable** standalone (the minimal @baseline does not bleed,
  nothing to revert), exactly the entity's honest framing. **M2's only real test is bolted onto a future
  flip-seeking generative lever that actually bleeds** — there it would either guard a live regression
  (value) or wrong-revert (inverted false-green); the minimal baseline can show neither. Banking the spec
  is correct; running it again standalone is not.
- **Bears on:** the R2 enforcement-primitive question — do NOT file another standalone enforced-revert on
  the minimal baseline (it cannot fire usefully and cannot show protective value). **The bleed-free revert
  primitive is REUSABLE for a future flip-seeking-lever pairing** (pair M2 with a bleeding generative lever,
  or first make clause evaluation non-self-graded); same wall as h0031 (abstention permitted-not-fired) and
  the whole blind-to-oracle family. **4th schema-drift sighting → pinned-schema necessity reconfirmed:** a
  PINNED record shape in prose is NOT reliably honored by gpt-5.5@xhigh even with an explicit "derived, not
  free-form" instruction (after h0041 / h0038 / h0037), so an enforced consumer must derive its decision
  from clause content, not a literal field — readers must be schema-tolerant. **Routing held a 4th time:**
  the h0041 stdout/session-transcript write-path delivered the record on all 13 cells; it is the standing
  durable write-path. **Program-level close:** h0040 is the LAST of the R2 workflow-stage set
  (h0037–h0041); all five ran through smoke with 0 flips — the oracle/discretionary wall held across
  reference-mining (h0037), plan-review/Method-B (h0038), observe-only (h0039/h0041), and the enforced rail
  (h0040). The durable yield is method/safety knowledge (routing fix, schema-drift, anti-bleed proof,
  enforcement-inert finding), not a pass-rate flip. The next-direction strategy decision is escalated to the
  captain; no 6th hypothesis is reflexively filed.
- **Evidence:** entity `hypotheses/h0040-enforced-abstention-rail.md`; run
  `runs/ade-bench-h0040-enforced-abstention-rail/41c556510ff753a7` (strict audit clean, 8/13);
  @baseline `runs/ade-bench-baseline/622bdedac572b479` (Panel A all 0.0, Panel B all 1.0). MEMORY:
  `ade-bench-solver-blind-to-oracle`, `verification-without-oracle-real-world`,
  `ade-bench-oracle-problem-concluded`, `workflow-synth-slug-mismatch-skips-files`,
  `ade-bench-single-trial-judge-by-artifact`. Sibling routing tests: h0041 (8/8 durable), h0038 (7/8),
  h0037, h0039 (the /tmp + stdout route this entity reused).

### Detached-run launch + completion-notify protocol: sentinel-scanned-every-turn + ntfy push, NOT a live poller (captain decision, 2026-06-09)
- **Layer:** autoresearch loop
- **Refinement type:** new protocol (how the FO/ensign launch a long `rk run` and learn it finished)
- **What was decided:** every `rk run`/`matrix.sh` launches through a single audited launcher
  `drivers/rk-run-detached.sh <key> <spec> [run|matrix]`. It `nohup`s the run (mandatory — plain
  `run_in_background` is reaped at turn-end; nohup survives the 7 hr+ duration), writes a handle
  `runs/.rk-handles/<key>-<ts>/` (`pid` · `log` · atomic `done` sentinel = `rc`/`end`/`rundir`), and
  fires an **ntfy** push on completion. The **ensign launches and returns the handle immediately — it
  never waits** (subagents are synchronous); the **FO owns the wait by scanning `runs/.rk-handles/*/`
  at the top of EVERY turn** (4-state read; on no-`done` + pid-dead, check harbor `result.json`/
  `summary.json` before crying crash; ~9 h wall-clock backstop). Replaces the old "nohup + tmp log +
  poll across turns" pattern and consolidates 3 inline copies (README smoke + full + matrix.sh).
- **Finding:** smoke-tested the launcher end-to-end (cmd mode): `rc` captured correctly (0 / 7), atomic
  same-fs sentinel written, the crash branch (worker SIGKILLed pre-sentinel) detected as no-`done` +
  pid-dead, and **ntfy delivery confirmed server-side** (both OK + FAIL messages landed). Real-plumbing
  proof, not an unprovable lifetime claim.
- **Learning:** for untrackable detached work, the wake mechanism is an *accelerator, never the
  correctness guarantee*. A live poller (`Monitor`) was REJECTED in design: its multi-hour lifetime is
  asserted-from-docs, not observed — the same claim class that already failed for background Bash — and
  a short Step-0 test cannot distinguish "survives the session" from "survives 90 s", so a green probe
  would be a **self-anchored false-green** (the project's recurring wall: cf. `validation-self-anchored-
  false-green`, the oracle-problem program). Invert it: the **sentinel + scan-every-turn is the floor**;
  the **nohup wrapper's own ntfy push is the autonomous notification** (survives anything, no agent
  awake needed) — strictly more robust than the poller, and it sidesteps the arming race, FO
  context-bloat, and the false-green entirely. General rule for any "notify me when the detached thing
  finishes": let the detached thing emit its OWN push; make the agent's check idempotent + every-turn.
- **Bears on:** every `smoke`/`full` run going forward; any future FO-autonomy work (the
  scan-every-turn rule is the re-attach/recovery hook). Hardened by an adversarial design review
  (general-purpose subagent) that surfaced the cross-fs `mv` non-atomicity, harbor-output-as-authority,
  and `rc`-capture-ordering fixes now baked into the launcher.
- **Evidence:** `ade-bench/drivers/rk-run-detached.sh`; contract in repo-root `AGENTS.md` → *Detached
  runs*; call sites `hypotheses/README.md` `smoke`/`full` + Repo conventions; MEMORY
  `rk-run-detached-nohup` (rewritten). Smoke test: handles under `runs/.rk-handles/` (cleaned); ntfy
  topic `ade-bench/.ntfy-topic` (gitignored).

### Orthogonal construct-gated levers COMPOSE in one README — no interference (h0049 GO, 2026-06-11)
- **Layer:** solver workflow
- **Refinement type:** new protocol — *multi-lever composition*: stack N already-smoke-verified,
  precondition-gated Implementation rules VERBATIM in a single README (each its own gated paragraph,
  no integration prose) and test whether each lever keeps its solo effect or stacking interferes.
- **Finding (h0049 smoke, run `aa64c927c4f793bd` panel + `98f921121acc361b` repeats; clean strict
  audit, captured>0 every cell):** ONE README composing three orthogonal construct-gated levers
  (h0044 same-grain max(points) / h0045 feature-boundary toggle / h0046 coverage-repair skeleton)
  stacked on @baseline h0043 **preserved every lever's solo effect by committed artifact**: airbnb009
  flipped FAIL→PASS **3/3** (three-fork signature — drop narrowing predicate, COUNT(*) byte-intact,
  no cross-join); f1006 + f1006-hard flipped via `sum(points)→max(points)` (no latest-row/QUALIFY);
  qb002 held; all 7 canaries held (incl. the perturbable same-construct ones the levers can fire on:
  f1005/f1005-medium, airbnb001/008, qb003). The one regression (qb004 0.0) was NOT interference:
  the two non-firing levers (h0044/h0046) appeared **0 times** in qb004's reasoning, and the failing
  artifact (`{% if %}` Jinja wrapped around a column entry in schema `quickbooks.yml` → YAML parse
  error, 0/48 tests ran) is h0045's OWN known-bimodal coin-flip — in h0045's solo smoke the solver
  made the same broken edit then REVERTED it (PASS); combined it didn't revert (FAIL). Same idea both
  times; difference is single-trial self-correction, not a stacked-lever effect.
- **Learning:** **precondition-gated levers that target DISJOINT construct families compose
  additively in one README — no cross-talk, no README-bloat precondition mis-fire.** The gate is the
  isolation mechanism: a lever's rule is inert text on any task whose construct it doesn't match, so
  N disjoint gated levers behave as N independent solo runs. This is the OPPOSITE of a generative
  (ungated) lever, which bleeds across families (h0009 −3, h0012 −4). Composition is therefore a cheap
  way to bank multiple verified flips at once WITHOUT re-paying per-lever full-run cost — but the
  per-lever solo verification must come FIRST (you compose verified levers, you don't discover them by
  stacking). Corollary trap surfaced: a self-correcting solver behavior (try-broken-then-revert) makes
  a hold target a coin-flip — judge holds by whether the lever's CONSTRUCT is even touched, not by a
  single reward. (Also a latent solver trap: guarding a column by wrapping its schema-`.yml` entry in
  `{% if %}` is invalid dbt — gate it in the model SQL select-list instead; the solver's offline
  jinja/DuckDB-parser probe misses it because it never runs dbt's schema parser.)
- **Bears on:** any future "bank several verified levers together" move (compose, don't re-run each at
  full); the propose-gate canary doctrine (G8 — gated levers need same-construct perturbable canaries,
  but cross-lever interference is NOT a new failure mode for DISJOINT gates); the hold-target judging
  rule (construct-touch, not reward, for coin-flip cells).
- **Evidence:** `hypotheses/h0049-combined-three-lever-single-readme.md` (`## Smoke result` /
  `## Behavioral analysis` / `## Failure Review`); runs
  `runs/ade-bench-h0049-combined-three-lever-single-readme/{aa64c927c4f793bd,98f921121acc361b}`;
  source levers h0044/h0045/h0046; MEMORY cross-ref `ade-bench-instruction-lever-taxonomy`.

### trials:1 single-run variance (~±4 tasks) dominates the per-lever +1 signal — judge by artifact + held targets, bank only artifact-reproducible flips with gated bleed (h0044/h0045/h0046 midnight-batch CONCLUDE, 2026-06-12)
- **Layer:** autoresearch loop
- **Refinement type:** gate-rule / methodology — how to JUDGE a lever's full-run result
  (promote criterion + what counts as a flip) under the standing trials:1 decision.
- **What happened:** all three midnight-batch levers ran full 48-task and ALL netted negative
  vs `@baseline` h0043 (32/48), all REJECTED no-promote, all on CLEAN strict audits:
  **h0044** (cumulative-standings max-points guard) 31/48 net −1 — both targets f1006 + f1006-hard
  flipped FAIL→PASS on artifact-proven same-grain `max(points)`, but asana002/f1011/quickbooks002
  regressed as off-construct variance (lever provably inert there); **h0045** (feature-boundary
  no-harm guard) 28/48 net −4 with **ZERO gains by design** — both targets held, all four
  regressions (asana002/f1005/f1010-medium/f1011) off-construct, gate held (no `using_*` bleed);
  **h0046** (coverage-repair all-three-fork skeleton) 31/48 net −1 — airbnb009 flipped 4/4
  byte-identical (broke the h0019/h0042 wall) but bled onto same-family airbnb008 (real generative
  scope defect, not variance), f1011 variance.
- **Finding:** a **provable no-harm guard (h0045) still scored −4.** A lever that flips nothing by
  construction moved the aggregate four tasks purely on off-construct coin-flips — the cleanest
  possible demonstration that trials:1 single-run noise (~±4 tasks) is WIDER than any single-lever
  +1 signal. The same borderline cells (asana002 — h0043's own +1 coin-flip; f1011 — the oracle-only
  ADE/ABDE answer cell) wobbled across h0044, h0045, AND h0046, confirming the variance read is
  batch-wide, not lever-specific. This is the single-trial-variance-masking wall (h0034) realized
  three more times.
- **Learning:** **judge a lever by its committed artifact + held targets, NOT by the single
  aggregate score** — the aggregate is below the noise floor at trials:1. A flip banks ONLY when
  the gain is (a) artifact-reproducible across draws AND (b) same-family bleed is gated. h0044's
  gains were artifact-real but the family is exhausted (stop); h0045 is a verified no-harm
  discipline with no standalone value (stop, compose-only); h0046's gain was artifact-real (4/4
  byte-identical) but ungated → it bled, so the bankable form is the GATED follow-up **h0050**
  (intent + fired-probe double-gate, smoke-GO: airbnb009 3/3 AND airbnb008 byte-intact). The
  discriminator between "stop" and "file" at conclude is exactly whether the negative net is pure
  off-construct variance (stop — nothing to fix) or hides a real lever-caused same-family bleed
  that a precondition can gate (file the scoped variant).
- **Bears on:** every full-run promote/conclude decision under trials:1 (do not read a negative
  aggregate as lever harm without the per-cell artifact read); the no-harm-guard composition path
  (h0045 → compose under a future flip lever, cf. h0049 additive composition); the gated-skeleton
  banking path (h0046 → h0050); any future batch of construct-gated levers (expect ~±4 aggregate
  noise — size the smoke + judge by artifact, not net).
- **Evidence:** `hypotheses/h0044-cumulative-standings-max-points-guard.md`,
  `hypotheses/h0045-feature-boundary-removal-toggle-guard.md`,
  `hypotheses/h0046-coverage-repair-all-three-forks-worked-skeleton.md` (each `## Run result` /
  `## Behavioral analysis` / `## Verdict` / `## Follow-up Routing`); runs
  `runs/ade-bench-h0044-cumulative-standings-max-points-guard/645f1f4dbca44ee0`,
  `runs/ade-bench-h0045-feature-boundary-removal-toggle-guard/9cd7b6635a124c12`,
  `runs/ade-bench-h0046-coverage-repair-all-three-forks-worked-skeleton/dfabb292560234ce`;
  `@baseline` h0043 `runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea`;
  follow-up `hypotheses/h0050-*` (smoke-GO); MEMORY `ade-bench-single-trial-judge-by-artifact`,
  `ade-bench-oracle-program-concluded`, `ade-bench-instruction-lever-taxonomy`,
  `ade-bench-gated-levers-compose`.

### A/B-isolation proves a no-harm guard is FREE under three-lever composition (h0052 smoke-GO → PROMOTED at conclude, 2026-06-12 / -13)
- **Layer:** solver workflow
- **Refinement type:** new protocol (composition method — A/B-paired smoke to isolate one lever's marginal contribution)
- **What was tried / decided:** the SCOPED, bleed-free re-do of h0049 — fork @baseline (h0043) and stack three precondition-gated Implementation rules verbatim (h0044 same-grain max(points), h0045 feature-boundary guard, h0050 intent+probe double-gated coverage), but run it as an **A/B against h0051** (= h0044 + h0050 only). The h0052−h0051 README diff is EXACTLY the h0045 block, so the paired smoke isolates h0045's marginal contribution.
- **Finding:** decisive. All 13 shared panel cells have IDENTICAL verdict AND identical committed artifact across h0051 and h0052 (f1006/f1006-hard = max() on both scored models; airbnb009 = dates_cte predicate removal; airbnb008 = agg.yml, mom_agg byte-intact; qb002/qb004 = narrow using_department removal). The only structural delta is h0052's added qb003 canary (PASS). Adding h0045 changed zero cells, zero verdicts, zero artifacts. The double-gate held under composition: h0050 fired on airbnb009 (3/3 byte-consistent) and correctly did NOT fire on airbnb008.
- **Learning:** when composing a verified **no-harm** guard onto a verified **flip** lever, build the smoke as an A/B pair (composition-minus-the-guard vs composition-with-it) on a shared panel — the per-cell artifact diff isolates the guard's marginal contribution cleanly and turns "is the third guard free or bloat?" into a falsifiable per-cell check, not an aggregate-noise argument. A guard whose construct family is already-passing (qb002/004/003) will be inert-but-safe: its prose neither tightens nor loosens an already-correct narrow edit, so the artifacts stay byte-equivalent to the no-guard arm. This is the bankable composition recipe: gate IS the isolation (cf. ade-bench-gated-levers-compose), A/B IS the proof of freeness.
- **Bears on:** h0049 (additive composition, this is its scoped re-do), h0051 (the A/B partner — its full result is the baseline for h0052's marginal-contribution read at scale), any future stack that adds a no-harm guard onto a flip lever; the single-trial judge-by-artifact discipline.
- **Evidence:** `hypotheses/h0052-compose-maxpoints-featureguard-scoped-coverage.md` (`## Smoke result` / `## Behavioral analysis`); runs `runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/f65c803f8713c00b` (panel 14/14), `…-airbnb009-r2/1462fa6db3e876c8`, `…-airbnb009-r3/1e0351c7ba0144f5`; A/B partner `runs/ade-bench-h0051-compose-maxpoints-and-scoped-coverage/372f512fc7007ed8` (panel 13/13); `@baseline` h0043 `runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea`; MEMORY `ade-bench-gated-levers-compose`, `ade-bench-single-trial-judge-by-artifact`.

### Composition + self-consistency promote — bank several verified levers in ONE README, prove the gain by a baseline self-consistency re-run, not a single-draw net (h0052 PROMOTED, 2026-06-13)
- **Layer:** autoresearch loop
- **Refinement type:** gate-rule / methodology — the `analyze → conclude` promote decision for a composed multi-lever README under the standing trials:1 regime. FIRST composition promote of the program.
- **What was tried / decided:** h0052 (3 construct-gated levers: h0044 max(points) + h0045 feature-boundary guard + h0050 intent-gated scoped coverage, forked from @baseline h0043) reached conclude as a tie-by-net (32/48 == the reference @baseline-32; its 2-lever partner h0051 drew 31/48). Rather than reading the tie as no-promote, PROMOTE on **two-draw self-consistency**: re-run the @baseline README against ITSELF and compare draw distributions, not single nets.
- **Finding:** the reference @baseline 32 was a LUCKY HIGH DRAW. The h0043 README re-run against itself scored **29 and 30** (true expectation ~30), while the composition drew **31 and 32** across its two independent full draws (h0051 + h0052). Both composition draws beat both baseline-fresh draws — a real ~+1.5-cell expectation gain that the single lucky-32 reference masked. The composition's +3 construct flips (f1006 + f1006-hard max(points) on both scored models; airbnb009 dates_cte removal) landed at the committed-artifact level in BOTH draws; regression forensics confirmed every PASS→FAIL cell is an off-construct trials:1 coin-flip with zero lever causation and zero gate mis-fire. h0052 promoted to @baseline (`dcb1a62ef4066133`); h0051 REJECTED-superseded (its +3 banked via the promoted superset).
- **Learning:** to clear the trials:1 ~±3-cell noise floor WITHOUT raising trials (which the standing single-trial captain decision declines), (1) **bank several pre-verified, bleed-free, construct-gated levers in ONE README** so the construct signal is +3 not +1 — the gate is the isolation, disjoint constructs compose additively (cf. h0049); and (2) **PROVE the expectation gain by a baseline self-consistency re-run** — re-run the incumbent README against itself for 2+ draws and compare the draw DISTRIBUTION (does every composition draw beat every baseline-fresh draw?), because a single reference net can be a lucky high draw that no real lever can beat. Promote on expectation + committed artifact + bleed-free forensics, NOT a single-draw net. This is the recipe that finally banks verified construct flips the single-trial floor was swallowing (h0034/h0044/h0046/h0051 all lost real signal to it).
- **Bears on:** the single-trial-variance-masking wall (h0034) and the trials:1 judge-by-artifact discipline (h0044/h0045/h0046) — this is the methodology that gets a verified +signal PROMOTED despite that wall; h0049 (additive composition, the substrate); h0051 (the A/B partner, superseded); any future promote of a composed/multi-lever README under trials:1; the standing single-trial captain decision (no freeze-repo/trials>1 fix needed — self-consistency substitutes for the CI).
- **Evidence:** `hypotheses/h0052-compose-maxpoints-featureguard-scoped-coverage.md` (`## Run result` / `## Behavioral analysis` / `## Regression Forensics` / `## Verdict (conclude — TERMINAL)`); `hypotheses/h0051-compose-maxpoints-and-scoped-coverage.md` (`## Verdict (conclude — TERMINAL)`, REJECTED-superseded); promoted run `runs/ade-bench-h0052-compose-maxpoints-featureguard-scoped-coverage/dcb1a62ef4066133` (32/48, now @baseline); 2nd draw `runs/ade-bench-h0051-compose-maxpoints-and-scoped-coverage/48aa50e556d16a80` (31/48); baseline self-consistency draws (29/30, h0043 re-run); prior @baseline h0043 `runs/ade-bench-h0043-package-update-optional-resource-matrix/7390e6adf44ba5ea`; MEMORY `ade-bench-gated-levers-compose`, `ade-bench-single-trial-judge-by-artifact`, `ade-bench-oracle-program-concluded`.

### Decision-fork simulation as a smoke SUBSTITUTE for a merge of already-solo-verified levers (h0056 PROMOTED, 2026-06-14)
- **Layer:** autoresearch loop
- **Refinement type:** new protocol — replace the `smoke` go/no-go gate with a multi-agent decision-fork SIMULATION when the hypothesis is a pure MERGE of levers each already solo-smoke-verified.
- **What was tried / decided:** Captain merged three solo-smoke-GO construct-gated levers (h0053 per-key inner-join + h0054 lap-time exclude-pit + h0055 build/rename preserve-columns) onto @baseline h0052's three (h0044+h0045+h0050) → ONE six-lever README (h0056). The ONLY new risk a merge introduces is **six-way mutual interference / precondition mis-routing** (a rule firing on the wrong task, or a dual-pair colliding) — which a fresh smoke would sample only at one trial:1 draw per task. Instead, ran a **decision-fork simulation** (per `_artifacts/subagent-decision-fork-probe-method.md`, scaled to a fan-out): 8 tasks (3 flip targets + both collision-canary dual-pairs + max-points holds) × **6 fresh, context-isolated decision agents** each given ONLY the committed merged rulebook + that task's clean visible context, classified in code by which gated rule fires. Captain pre-authorized: if the sim verifies, SKIP smoke → straight to full, 2 concurrent draws.
- **Finding:** **48/48 desired-branch, 0 collisions.** Every flip target routed to its intended rule; both dual-pairs held their correct sides (airbnb009 stayed coverage-repair, per-key silent [h0050↔h0053]; qb002/003 stayed feature-boundary, preserve-columns silent [h0045↔h0055]). The two concurrent full draws then landed r1=32 / r2=35 (mean 33.5, both above h0052's ~30 expectation), strict-clean, collision-free — PROMOTED to @baseline (first six-lever baseline, 35/48=0.7292). The full run vindicated the sim: the only regression cluster (r1 qb002+qb003) was forensically the h0045 feature-removal OVER-DROP coin-flip ("less columns than solution" = opposite of a preserve over-fire), exactly the "preserve-columns stays silent on qb" the sim predicted.
- **Learning:** when a hypothesis is a MERGE of levers that were EACH already solo-smoke-verified and shown non-colliding with their dual, the residual risk is mutual interference, not single-lever efficacy — and that is a **decision-POLICY** question a fan-out of fresh isolated decision agents answers far more densely (8×6=48 independent reads of precondition-routing) than a one-draw-per-task smoke. The substitution is valid ONLY under that precondition (each lever solo-verified); it does NOT replace smoke for a NEW untested lever (the sim estimates decision tendency, not pass rate — it cannot prove the solver finds the bug, writes the artifact, and passes the hidden grader). Keep the full run as the promote evidence; the sim only earns the right to skip smoke. Build the sim against the COMMITTED merged rulebook (not a hand-assembled one) and feed each decision agent ONLY (rulebook + clean per-task context) with no repo access, to avoid leakage. Watch the cell-path glob: run cells nest `runs/<exp>/<hash>/<cell>` (3 levels) — a 2-level glob silently drops tasks (2/8 failed extraction on the first pass).
- **Bears on:** the composition+self-consistency promote recipe (the prior entry — this extends it: sim-substitutes-smoke for the merge step, self-consistency-style two-draw expectation for the promote); `_artifacts/subagent-decision-fork-probe-method.md` (this is its first fan-out-scaled, collision-detection use); the single-trial judge-by-artifact discipline; any future merge of pre-verified construct-gated levers; ade-bench-gated-levers-compose (the gate IS the isolation, now shown to hold at SIX levers).
- **Evidence:** `hypotheses/_archive/h0056-compose-six-levers-on-h0052.md` (`## Pre-smoke Decision-Fork Probe` / `## Run result` / `## Behavioral analysis` / `## Verdict`); `_artifacts/h0056-decision-fork-simulation.md` (the 48/48 writeup); promoted run `runs/ade-bench-h0056-compose-six-levers-on-h0052-r2/2c544ee929c0c02a` (35/48, now @baseline); 2nd draw `…-r1/deff5d8a9c10c92f` (32/48); merged building blocks `hypotheses/_archive/h0053-*`, `h0054-*`, `h0055-*` (all PASSED, merged); prior anchor h0052 `dcb1a62ef4066133`.
