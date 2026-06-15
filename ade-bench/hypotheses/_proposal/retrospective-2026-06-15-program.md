# Program Retrospective — ade-bench autoresearch loop, the full 2 weeks (2026-06-15)

> Traces the whole loop from the first entity (`h0000`, 2026-06-01) to the live tail
> (`h0060`, 2026-06-15). Companion to the three round retrospectives
> (`retrospective-2026-06-07.md`, `-08.md`, `-10-round-2.md`). Written for the captain's
> end-of-program ask: *why did we conclude README was dead, why did we move to adding
> stages, and what should a future multi-benchmark workflow do differently.*

---

## 0. The headline, corrected

The working memory of this program is "65% → 73%, target 75%." That is true on the
**post-fix** baseline, but it hides the single biggest move of the two weeks and changes
how the rest should be read:

- **`h0000` cold-start baseline = 9/48 = 0.1875.** The raw codex solver README.
- **`h0005` baseline = 31/48 = 0.6458 ("65%").** This jump of **+22 tasks did NOT come
  from a README lever.** It came from fixing a *benchmark infrastructure bug* — the task
  images shipped the wrong DuckDB dataset via a BuildKit COPY mtime-collision
  (MEMORY: `ade-bench-wrong-duckdb-in-images`). The four README build-gate levers filed
  to attack the "27 build-errors" failure mode (`h0001`–`h0004`) were **all REJECTED** —
  they were chasing errors that the dataset bug, not the solver, was causing.
- The entire rest of the program — every lever, every stage, two full rounds — was the
  fight to move **31 → 36 (65% → 75%)**, and it ended at **35/48 = 0.7292 (73%)**.

**So the first lesson is structural, not about prompting at all:** the largest, cheapest
gain in the whole program was an infrastructure correctness fix discovered by auditing the
benchmark, not by improving the solver. Hold that thought for §4.

---

## 1. The arc in one screen

| Phase | Dates | Entities | What we tried | Net | Conclusion reached |
|---|---|---|---|---|---|
| **0. Setup + bug-fix** | Jun 1–3 | h0000–h0005 | raw baseline; build-gate README levers; **dataset-bug fix** | 9→**31** | build-errors were a benchmark bug, not a solver gap |
| **1. Oracle-flip program** | Jun 5–8 | h0006–h0036 | instruction/README levers: grain, cast, reconcile, candidate-selectors, arbitration, coverage | **+0** | **"README/instruction levers can't move it"** — the oracle wall |
| **2. Workflow-stage program (Round 2)** | Jun 8–10 | h0037–h0041 | **add NEW stages**: reference-mining, plan-review, observe-lens, abstention-rail, triage-ledger | **+0** | **"adding stages is also dead"** — the self-grading wall |
| **3. Worked-example flips (back to README)** | Jun 11–15 | h0042–h0060 | task-specific copyable before→after skeletons, precondition-gated, composed | 31→**35** | the leverable subset is real but small; flip program now exhausted |

Two weeks, 60 hypotheses, net **+4 tasks** of *lever* gain (on top of the +22 bug-fix gain).

---

## 1.5 The lens that explains the whole sequence: two kinds of "flip"

For most of the two weeks the score read as "nothing is working," yet real flips were
happening underneath the entire time. The contradiction dissolves once you separate two
things that both get called "a flipped task" — and failing to separate them is *the* reason
Phase 1 looked dead, Phase 2 felt necessary, and Phase 3 finally banked gains.

1. **Volatility flips (mostly random).** A task that PASSES in some `trials:1` runs and FAILS
   in others *purely because the solver sampled a different locally-plausible choice that
   draw* — no lever involved. At `trials:1` over 48 tasks, gpt-5.5 produces **~3–4 of these
   per run**, in random places (the noise floor; 10k bootstrap CI ±4).
2. **Lever-caused flips (not random).** A task that goes FAIL→PASS because a worked example
   changed the committed SQL in a reproducible, artifact-attributable way.

These look identical at the score level and opposite at the artifact level. Across the
*whole* program, **exactly one** flip was provably lever-caused as it happened — and that was
a lever *bleeding* where it shouldn't (`airbnb008`, h0046, gated out by h0050). Every other
flip seen in the early runs was the random kind.

**Why this made Phase 1 read as dead.** Things flipped constantly; the *net* stayed at 31
because a real construct gain of +3 minus ~3 random off-construct losses = a tie. h0051 and
h0052 both produced an artifact-real **+3 and still netted to a tie** against the lucky-32
baseline (`round1-round2-flipped-task-choice-map.md` §8). So the score-level evidence honestly
said "README does nothing" — and that read was *correct for what we could measure*. The real
flips were happening; they were only visible by reading the committed SQL, never the score.

**The discovery that turned this around (2026-06-13).** The leverable flips were not found by
running more experiments hoping flips appear. They were found by a deliberate **forensic pass**
(`leverable-flipped-tasks-research-2026-06-13.md`) that uses the randomness itself as the
search filter:

1. **Volatility = the candidate filter.** Collect every task that flipped *at least once*
   across all run-dirs on disk — the 19-task "sensitivity set." A task that flip-flops is, by
   definition, one where the solver sits on a knife's edge between two locally-plausible
   repairs. Tasks that *never* flip (always FAIL) are oracle-blind or need a structural fix —
   not leverable.
2. **Read the committed artifacts, both directions.** For each volatile task, open the SQL
   from a passing run *and* a failing run and name the exact fork — `COUNT(*)` vs
   `COUNT(review_date)`, `max(points)` vs latest-row, exclude-pit-laps vs subtract-duration,
   preserve-all-columns vs drop-some.
3. **Classify by oracle-locality.** Is the correct branch *derivable from the visible files*
   (a convention the workspace under-specifies but pins) or *oracle-only* (no local signal —
   the answer-selection tasks f1011/f1003)? Only the locally-derivable forks are leverable.
4. **Pin the right branch** with a precondition-gated worked example, converting a coin-flip
   cell into a reliable pass.

**So: random, or did we do something right?** Both — and the honest part is that the
*failed* stage round (Phase 2) is what made the flip-hunt possible. The
*which-task-flips-this-draw* is random, but the **set of flippable tasks is a stable
sensitivity set**, and the **leverable subset within it is fixed by oracle-locality** — found
by reading committed SQL, not by luck. Phase 2 netted zero flips and did not find the targets,
yet it earned the two things the hunt depended on:

- **It validated the delivery vehicle.** h0037 (reference-mining stage) proved a worked-example
  copy *reaches the committed SQL, bleed-free, at 48-task scale*. Every Phase-3 flip rides on
  that exact mechanism — Round 2 proved the gun fires before we found the targets.
- **It forced the artifact-judgment discipline.** Rounds 1–2 hammered in "judge by the
  committed artifact, not the net score" and "separate lever-caused from variance flips."
  Without that discipline the forensic read (step 2) is impossible — you'd be fooled by the
  noise floor every time, exactly as the score-level read was.

**When we knew flips mattered.** The near-miss tasks were named as "cheapest points" on day one
(h0000). What took two weeks was learning that *flipping ≠ ability* and that the leverable
subset is defined by oracle-locality, not closeness. The choice-map was first built **2026-06-10**
(end of Round 2, 12 tasks), extended to 19 on **2026-06-13**, alongside the forensic
leverable-research — so the explicit "hunt the volatile cells, read their artifacts, pin the
locally-derivable forks" strategy crystallized **right after Round 2 closed**, not before.

One caveat that still stands: pinning the leverable forks never removed the ~3-cell noise floor,
which is why the late hypotheses shifted from *flipping* new tasks to *stabilizing* the volatile
ones (h0058/h0060) — aiming for a robust 36/48 rather than a lucky one.

---

## 2. Why we concluded "README is a dead end" (end of Phase 1)

Phase 1 was the **oracle-problem systematic program** (`_proposal/oracle-problem-systematic-program.md`).
We ran every shape of in-README / in-prompt lever against the 17 false-green / near-miss
failures:

- **Grain construct** (entity-spine, prose, worked example, contract) — `h0010/h0016/h0017`
- **Grain reconcile** (raw-source count + anti-join) — `h0030`
- **Cast / type-contract** (seed-layer, model-layer) — `h0020/h0033`
- **Candidate-generation + arbitration** (selectors, dual-contract) — `h0026/h0031`
- **Coverage repair** — `h0035/h0036`

**Every one netted +0.** Three distinct failure signatures kept recurring, and together
they named the wall:

1. **Inert prose** — restructuring instructions "talk but don't do." The rule was read and
   reasoned about but never reached the committed SQL (`h0010`, `h0016`).
2. **Correlated-error false-green** — an "independent" check re-correlated through a shared
   upstream filter/population and confirmed the wrong answer (`h0030` shared `_fivetran_active`;
   `h0031` reproduced baseline's byte-identical wrong `ABDE`). More generation/checking does
   not manufacture an oracle.
3. **Oracle-only deciding fact** — even when a lever *landed* (the f1007-hard shape, `h0036`
   recovered the dropped rows correctly), the recovered quantity needed a value that lives
   only in the hidden seed/solution. Fixing the visible symptom made the score *worse*
   (`Got 5 → Got 10`).

**The conclusion (retro 06-07 / 06-08): the binding constraint is the *oracle problem*.**
The deciding facts (width column-sets, grain conventions, value semantics, date-range
counts) live only in `solution__*` + the hidden tests. The solver is *blind to the oracle*
(no tests, no solution seeds ship to `/app`). No README instruction can supply a fact that
is not in what the solver can see. The only thing that beats no-oracle is *independent
redundancy*, and the universal failure mode is *correlated error*
(`_artifacts/verification-without-oracle.md`).

That is the precise, defensible reason "README is dead" was declared — **not** "we got
bored of prose," but "we proved that every in-context lever shape either goes inert or
re-correlates, and the remaining facts are genuinely not visible to the solver."

---

## 3. Why we moved to "adding new stages" — and why that also died

### 3.1 The reasoning behind the pivot to stages

The Phase-1 diagnosis pointed at a specific gap: a single in-context prose instruction
cannot create the *independent second path* that the oracle problem demands. The natural
structural escalation was: **if prose can't create independence, give it its own STAGE.**
Round 2 (`round-2-workflow-stage-program.md`) attacked the wall from the four remaining
structural angles:

- **Generate** — `h0037` reference-mining stage (systematize the one survivor lever, the
  worked-example copy, into a generative pre-Implementation stage).
- **Review** — `h0038` plan-review stage (independent re-derivation + generic invariant,
  the never-run "Method B").
- **Enforce** — `h0040` abstention rail (revert any edit the solver can't independently
  ground).
- **Observe** — `h0039`/`h0041` debug-lens + triage-ledger (map which facts are decidable).

This was a *deliberate, gatekeeper-acknowledged* bet: the gatekeeper had already scored
every Round-2 candidate METHOD-ONLY ({0} predicted flips), and we ran them anyway to buy
structural knowledge about the solver's stage graph.

### 3.2 Why stages died — the self-grading wall

Round 2 netted **+0**, and worse, the one "sure" banking point (airbnb009) failed to
reproduce. The new wall it exposed is the deepest finding of the program:

**Any mechanism authored as solver-README prose — a new stage, a REJECT verdict, an
abstention trigger — is evaluated by the same model, in the same context, that produced the
work being judged. Independence cannot be authored in the same context.** It fails in both
directions:

- `h0038` plan-review **false-rejected** its own designated abstention target (the invariant
  pattern-matched a clause it couldn't locally ground).
- `h0040` abstention rail **never fired** — the solver *self-credits* the trigger clauses
  (the AND-of-NOTs all read `true` because the inputs are discretionary self-reads).
- `h0039` was fully inert (routed through a dead `/razorback-freeze` precondition).

A new *stage* is not more independent than a new *sentence* when the same model executes
both. That is why "adding stages" was concluded dead: it was the same self-grading wall in
a bigger box.

### 3.3 The third wall, named here for completeness

Underneath both rounds sat a **measurement wall**: at `trials:1` with gpt-5.5/xhigh the
run-to-run noise is **±3–4 tasks** (10k paired bootstrap CI [-4,+4]). A lone real +1 sits
*inside* the noise. We couldn't average it out because the **freeze-repo concurrency race**
(MEMORY: `ade-bench-freeze-repo-concurrency-race`) forbids `trials > 1`. So even a genuine
fix (airbnb009) could not be *banked* on a single draw.

The three walls interlock and define the box exactly:
- To beat the **oracle wall** you need an independent check → blocked by the **self-grading wall**.
- To bank small real wins instead, you need repeatability → blocked by the **variance wall**.
- Full pinning of an edit ≡ leaking the per-task answer → out of scope.

---

## 4. Why going BACK to README finally worked (Phase 3, +4)

This is the part that looks paradoxical — we declared README dead, then banked every real
flip via README edits. The resolution: **Phase 3 was not "README again." It changed the
target class, the lever shape, and the promotion rule simultaneously.** The medium was the
same; the method was not. (How the target tasks were *found* — the forensic flip-hunt over
the volatility set — is §1.5; this section is what we did with them once found.)

| Dimension | Phases 1–2 (dead) | Phase 3 (banked +4) |
|---|---|---|
| **Target** | the hardest failures, many **oracle-only** | only tasks whose correct branch is **locally derivable** (a convention under-specified in the workspace but determinable) |
| **Lever shape** | general **prose principles** | copyable **before→after worked-example skeletons** with generic identifiers |
| **Composition** | one lever at a time, ungated | **precondition-gated** levers, disjoint constructs, composed additively in one README (the gate IS the isolation) |
| **Promotion** | single-draw **net delta** (buried in ±4 noise) | **committed-artifact + reproducibility + two-draw self-consistency** |

The six levers composed into the 35/48 baseline (`h0056`), all worked-examples on
locally-derivable conventions:

1. `max(points)` cumulative-standings guard → **f1006, f1006-hard** (`h0044`)
2. feature-boundary removal guard → **quickbooks002/004** held (`h0045`)
3. scoped coverage repair, gated on a fired missing-day probe → **airbnb009** (`h0050`)
4. per-key inner-join-from-fact → **airbnb005 (+ airbnb007)** (`h0053`)
5. lap-time exclude-pit-stop-laps → **f1010-medium** (`h0054`)
6. build/rename preserve-all-upstream-columns → **ana-eng003** (`h0055`)

Then two stabilizers on top: `h0058` keep-base-id (locks the qb002/003 over-drop
coin-flip), `h0059` tmp-tier-removal inline+reconcile (banks **asana003**, the *last*
bankable flipped-FAIL).

**The deep reason it worked:** the oracle wall was never "README can't help." It was
"you can't supply a fact the solver can't locally derive." Phase 3 found the *subset* of
failures where the correct answer **is** locally derivable, and delivered it in the **one
shape that reaches committed code** (a worked example), gated so it fires only on its own
construct, and judged it by **whether the prescribed edit actually landed in the committed
SQL reproducibly** — not by a net delta the noise floor would have eaten.

The single cleanest idea — and the most transferable — is `h0059`'s **behavior-preserving
refactor + double-entry reconciliation**: a refactor has a locally-computable correct
answer (the *before-state*), so the lever can carry its own oracle-free check (before ==
after). That is the way *past* the oracle-blind wall without leaking anything.

---

## 5. Why it stopped at 35/48 (73%), not 36/48 (75%)

- **The flip program is exhausted.** asana003 (`h0059`) was the last failing task with a
  locally-derivable fix. Every remaining FAIL is either never-passed research-bet,
  oracle-blocked (no passer can exist), or **oracle-blind** — needs an oracle-only exact
  output the solver has no local signal for. `ana-eng004` was reclassified into this set
  (`h0057`): a de-leaked honest *simulation* scored it 10/10, yet the real run failed 4/4,
  because production normalizes the cryptic alias the answer requires. The sim↔real gap is
  unbridgeable for oracle-only-exact-schema targets.
- **The noise floor masks new +1s.** A longer README perturbs ~3 off-construct passers, so
  even a real flip nets flat. `h0060` (live) responds by *stabilizing* the f1001 / f1003-hard
  coin-flips instead of flipping new tasks — aiming for a *robust* 36, not a lucky one.
- **The honest ceiling finding (S4, still standing):** past ~73%, moving the number is a
  **benchmark-design** question (ship truthful `schema.yml`, ship a subset of `tests/`, or
  score against declared-not-hidden expectations), not a smarter prompt.

---

## 6. What to shift for a benchmark-agnostic workflow (the forward-looking ask)

The two weeks produced a reusable *method*, not just a number. If we want this loop to take
on DAB and future benchmarks efficiently, these are the shifts — ordered by how much wasted
motion they would have saved here.

### 6.1 Front-load a benchmark-correctness audit (would have saved Phase 0 confusion)
The biggest gain (9→31) was a dataset-bug fix; the four levers chasing that failure mode
were wasted because the bug was upstream. **New stage-zero before any lever runs:** audit
the benchmark itself for leaks, wrong-dataset/image bugs, lying contracts, and false-green
self-checks. The DAB project has already hit the same class repeatedly
(MEMORY: non-root image perm fail, mongo SIGSEGV no-restart, missing `common_scaffold`).
Make "is the failure the solver's or the harness's?" the *first* question, with a standard
guard-script + strict audit, not a thing discovered mid-program.

### 6.2 Triage every target by oracle-locality FIRST (would have saved most of Phases 1–2)
Before filing any prompt-side hypothesis, classify each failing task with the **sharp test**
(`_artifacts/verification-without-oracle.md`): *is the deciding fact locally derivable, or
oracle-only?* Only locally-derivable tasks are leverable from the prompt side. Phases 1–2
spent ~35 hypotheses discovering this one task at a time. A locality triage up front would
have pointed straight at the Phase-3 leverable subset and skipped the dead families. **This
is the single highest-value transferable artifact** — port the sharp test and the
dead-family map shape to every new benchmark.

### 6.3 Default the lever shape to worked-example skeletons, not prose
Confirmed across the whole program: **copyable before→after skeletons reach committed code;
prose principles go inert.** Make worked-example the default lever form in the workflow's
propose stage; treat any prose-only lever as suspect-inert until proven otherwise.

### 6.4 Make levers precondition-gated and composable by default
Disjoint gated levers compose additively — the gate is the isolation, so you can bank many
flips in one artifact and re-verify cheaply (`h0049/h0056`). Bake gating into the lever
template so composition is the default, not a late discovery.

### 6.5 Fix measurement before fighting it
The variance wall cost a real +1 (airbnb009) and forced an awkward
judge-by-artifact doctrine. For a new benchmark: **fix the multi-trial blocker first**
(per-task/per-trial freeze repo — pass `benchmark_task_id` into `compute_sealed_hash`, or a
unique `RAZORBACK_FREEZE_DIR` per trial). Then promotion can use a tightened CI instead of
artifact-forensics. Until then, carry forward the working doctrine: **judge flips by
committed-artifact + reproducibility, not single-draw net.**

### 6.6 Never author independence in-context — design it as harness code
The self-grading wall is permanent for any prompt-authored check. If a benchmark genuinely
needs an independent verifier/abstention/judge, it must be **operator-side harness code or a
different model/context**, decided at the workflow level — not a README clause. Make this a
hard gatekeeper rule so such proposals are declined without spending a run.

### 6.7 Treat benchmark-design feedback as a first-class deliverable
The honest path to 75% here was a benchmark-design recommendation, not a lever. A mature
multi-benchmark workflow should emit, per benchmark, *"here is the prompt-side ceiling and
here is what the benchmark owner must change to lift it"* as a standing output — turning the
oracle/self-grading walls from dead-ends into actionable benchmark-design findings.

### 6.8 Keep the reusable infrastructure (it is already benchmark-agnostic)
The spacedock first-officer loop, the propose-gate gatekeeper, the decision-fork simulation
(with its known sim↔real caveat), the smoke→full discipline, entity files with run-dir
citations, and the dead-family map / WORKFLOW-REFINE ledger are all benchmark-independent and
should be the scaffold for DAB and beyond. The one caveat to carry: **a decision-fork sim
validates *tendency*, not real-run compliance** — trust it to skip smoke only for a merge of
already-solo-verified levers, never to validate a new one (`h0057`).

---

## 7. Bottom line for the captain (plain words)

We spent two weeks and moved the score from 65% to 73%, against a 75% goal. The honest
story has three beats. **First**, the easy half of the climb (the cold-start 19% up to 65%)
was really a *benchmark bug fix*, not clever prompting — which is the first lesson: audit
the benchmark before you tune the solver. **Second**, we then spent a week proving that
ordinary README instructions, and even brand-new workflow stages, *cannot* move the number,
because the answers the solver needs aren't in what it's allowed to see (the oracle wall),
and any check we write is graded by the same model that did the work (the self-grading
wall). Declaring those dead was correct and evidence-backed, not impatience. **Third**, we
went back to the README but changed the *method*: only attack tasks whose right answer is
actually derivable from what the solver sees, deliver the fix as a copy-paste worked
example, gate each one so they stack, and judge success by whether the code actually changed
— not by a noisy score. That banked the four real flips to 73%, and we stopped at 73%
because the remaining tasks genuinely can't be solved without changing what the benchmark
shows the solver. For the next benchmark: do the locality triage and the bug-audit *first*,
default to worked-example gated levers, fix the multi-trial measurement, and ship the
"what the benchmark owner must change" finding as a real deliverable.

---

**Cross-refs:** `retrospective-2026-06-07.md`, `-08.md`, `-10-round-2.md`;
`oracle-problem-systematic-program.md`, `round-2-workflow-stage-program.md`,
`leverable-flipped-tasks-research-2026-06-13.md`, `h0056-postrun-move-discovery-2026-06-14.md`;
`_artifacts/{verification-without-oracle.md, WORKFLOW-REFINE.md, round1-round2-flipped-task-choice-map.md, h0059-three-run-deep-dive.md}`;
baseline run `runs/ade-bench-baseline/622bdedac572b479` (31/48);
current `@baseline` `runs/ade-bench-h0059-tmp-tier-removal-inline-reconcile-full-r1/97c03e6c467742f8` (35/48 = 0.7292).
</content>
</invoke>
