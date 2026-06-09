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

### Reference Mining: a generative copy-the-analog stage REACHES the committed SQL and the own-sibling-first gate is artifact-proven anti-bleed — but {0} flips on the width oracle (h0037 smoke GO-as-reach-finding, 2026-06-09)
- **Status:** **smoke GO → full** (reach finding, NOT a flip) — new-stage structural lever; the
  E-RMS systematization of the h0019 lone-survivor engine. @baseline UNCHANGED at 31/48 on this
  panel (0 flips, 0 regressions); advanced because the mechanism is artifact-proven to reach the
  committed SQL AND no passer regressed. Forked the @baseline solver `codex-ade-dbt-minimal`.
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
- **Learning:** (1) **A generative copy-the-analog stage CAN reach the committed SQL** (clears the
  h0010/h0016 inert-prose bar) when it carries a worked-example skeleton and cites a named local
  analog — reach-systematization of the h0019 survivor engine is achieved. (2) **Own-siblings-FIRST /
  package-only-as-fallback is the correct anti-bleed gate** — artifact-proven on f1001 (fired,
  found-no-sibling, cited own convention, held 6/6), unlike h0023's deliverable-set clause which bled
  packages. Re-use this gate shape for any future copy/template lever. (3) **Copying a CONSTRUCTION
  ANALOG does not beat the width oracle** — on a width target the deciding column set is oracle-only,
  and the closest sibling encodes a DIFFERENT (wider) convention, so a faithful analog copy is
  efficacy-zero exactly where it reaches. The D6 width family stays dead; copying shape ≠ the hidden
  DROP/ADD. (4) **An author-gated generative stage is invisible to same-model REPAIRS** — pick
  AUTHORING canaries to test regression risk.
- **Bears on:** the D6 width family (h0011/h0023/h0029 — confirms copying a construction analog does
  NOT supply the oracle-only column set; do not re-file width-flip levers); the h0017/h0023 Output
  Contract family (the own-sibling-first COPY gate is the safe version of the deliverable-set clause
  that bled f1001 — this is the gate to carry forward, not the deliverable-set clause); the
  `solver-blind-to-oracle` / `verification-without-oracle` family (the width oracle is the same wall);
  any future generative copy/template/convention lever (use own-siblings-first + worked-example +
  /tmp+stdout routing; pick authoring canaries); the standing observe-only write-path (3rd validation).
- **Evidence:** entity `hypotheses/h0037-reference-mining-stage.md` (`## Smoke result`,
  `## Behavioral analysis`); run `runs/ade-bench-h0037-reference-mining-stage/6671b5e449bd0975` (audit
  clean 10/10 tainted:0, captured=1; score 0.70; ana-eng004 committed `obt_product_inventory.sql` +
  filled `reference_mining.json` recovered from `agent/sessions/2026/06/09/*.jsonl`; f1001 6/6 PASS +
  its no-own-sibling record); baseline `runs/ade-bench-baseline/622bdedac572b479` (ana-eng004 "has
  less columns" byte-identical; f1001 6/6; intercom001/003 Got 7). MEMORY
  `ade-bench-solver-blind-to-oracle`, `verification-without-oracle-real-world`,
  `ade-bench-single-trial-judge-by-artifact`, `ade-bench-instruction-lever-taxonomy`.


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
