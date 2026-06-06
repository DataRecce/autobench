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
