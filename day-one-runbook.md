# Day-One Runbook — standing up the autoresearch loop on a new benchmark

A reusable, benchmark-agnostic checklist for the **first day** on any new benchmark
(the next one being DAB; the lessons are distilled from the 2-week ade-bench program —
see `ade-bench/hypotheses/_proposal/retrospective-2026-06-15-program.md`).

## The one rule

**Day one buys interpretability, not score.** Do not try to improve the solver on day
one. Spend the entire day making the *benchmark* and the *measurement* trustworthy, so
that on day two a flat score means "the lever didn't work" — not "we have no idea why
nothing moved." Almost all of ade-bench's wasted motion came from running levers before
this was true: a flat net score read as "README is dead" for a week while real gains were
being silently cancelled by unmeasured noise.

The day-one **deliverable is a one-page Benchmark Profile** (template in §7), not a lever.

---

## 1. Stand up the loop and run the cold-start baseline

- Instantiate the scaffold: spacedock workflow, registry, entity dir, `@baseline` binding.
  - **Gotcha (multi-benchmark):** export the per-benchmark registry before any `rk run`
    or you clobber another benchmark's `@baseline`
    (`export RAZORBACK_REGISTRY=<bench>/razorback-registry.yaml`;
    `export RAZORBACK_SPACEDOCK_PLUGIN_DIR=…`). See `AGENTS.md` → Run prerequisites.
  - `rk run` is 30 min–hours; launch detached (nohup + log + pidfile) and poll across turns.
- Run the **unmodified** solver on the full task set. This is the anchor every future
  variant forks and diffs against.
- Record the absolute score and bind `@baseline`. Always `rk registry resolve run @baseline`
  for the live value; never quote a number from notes as current.

## 2. Read the artifacts, not just the score — group failures by mode

- Open the committed output of **every** failure. Classify each into a failure mode, e.g.:
  build/compile error · output value mismatch (near-miss) · missing/extra rows (coverage) ·
  schema/width mismatch · answer-selection · timeout/infra.
- Produce a per-group tally + a distance-to-pass for near-misses (`checks_passed /
  expected`). This grouping is worth more than the headline number — in ade-bench it
  immediately revealed "27 build-errors vs 12 near-misses," which set the whole agenda.

## 3. Measure the noise floor BEFORE attributing anything to a lever ⭐

This is the step ade-bench did too late and paid for the entire program.

- Re-run the **identical baseline 2–3 times** (or with `trials>1` if the harness allows).
- **Count how many tasks flip pass↔fail between identical runs.** That number is the noise
  floor (ade-bench: ~3–4 of 48 at `trials:1`; 10k bootstrap CI ±4).
- This number governs **every** promotion decision for the rest of the program. Until you
  know it, you cannot distinguish a real +3 from luck, and you will misread a flat net as
  "nothing works."
- Write it into the Benchmark Profile as the **minimum detectable effect**: a lever must
  beat the noise floor (or be judged by committed artifact, §6) to count.

## 4. If you can't run multiple trials, fix that on day one — don't work around it

- ade-bench never escaped single-draw judgment (the freeze-repo concurrency race blocked
  `trials>1`), and it cost a real banked point (a genuine +1 that wouldn't reproduce).
- For a new benchmark, make multi-trial work **first**: per-task/per-trial isolation
  (e.g. unique freeze dir / task-id in the sealed hash). A day here lets day-two promotion
  use a tightened CI instead of slow artifact-forensics, and removes the variance wall.
- If it genuinely can't be fixed, that's a known constraint to design around from day one —
  not a surprise to discover mid-program.

## 5. Audit the benchmark — assume failures are the HARNESS's fault until proven otherwise

The largest single ade-bench gain (+22 tasks, 9→31) was a **dataset bug fix**, not a
prompt; the levers filed against those "failures" were all rejected because the bug was
upstream. So:

- Run the strict audit (`rk audit --policy strict`); confirm it's clean.
- Verify datasets/images are correct (ade-bench shipped the **wrong DuckDB dataset** via a
  BuildKit COPY mtime collision). Check for answer/oracle **leakage** into what the solver
  sees.
- Confirm failures are **reproducible**, not infra-flaky.
- **DAB-specific audit items (all were real bugs there):**
  - Agent image is non-root → codex setup runs as root but agent runs as the image user →
    `Permission denied` exit 1. Check the main service user in the plugin compose.
  - A backing service (e.g. mongo) with **no restart policy** → one crash bricks the whole
    trial. Add `restart: on-failure` (and bound cache size).
  - Per-query verifier crashes from **missing vendored scaffold** (`common_scaffold`) →
    `RewardFileNotFoundError` / no reward. Ensure the materializer vendors it on every path.
- **Fix infrastructure bugs before filing a single solver hypothesis.** They are the
  cheapest, largest gains and they are invisible if you assume the solver is at fault.

## 6. Triage every failure by oracle-locality — this decides what's even leverable

For each failing task, ask the **sharp test** (`ade-bench/hypotheses/_artifacts/
verification-without-oracle.md`): *is the deciding fact derivable from what the solver can
see, or does it live only in the hidden oracle?*

- **Leverable** = locally derivable → eligible for a prompt-side hypothesis.
- **Oracle-blind** = answer lives only in hidden solution/tests → no prompt will ever fix
  it. Do not file levers against it; it becomes a *benchmark-design finding* instead (§8).
- ade-bench discovered this partition on day ~10; doing it day one would have skipped most
  of two dead rounds. The leverable subset is found by reading committed artifacts of the
  **volatile** tasks (those that pass in some runs, fail in others) and naming the local
  fork the solver is coin-flipping between — see the retrospective §1.5 (two kinds of flip).

---

## 7. The day-one deliverable: the Benchmark Profile (one page)

```
BENCHMARK PROFILE — <name> — <date>
- Cold-start baseline:        N/T = X.XX  (run-dir …)
- Noise floor:                ±K tasks over R re-runs  (min detectable effect)
- Multi-trial available?      yes / no (+ blocker & fix if no)
- Audit:                      strict-clean? datasets correct? leaks? infra bugs found+fixed
- Failure-mode groups:        build-error N · near-miss N · coverage N · width N · answer-sel N
- Oracle-locality partition:  leverable [tasks…]  |  oracle-blind [tasks…]
- Predicted prompt-side ceiling: ~Y/T   (leverable subset only)
- Benchmark-design findings:  what the owner must change to lift the ceiling
```

This is what makes day two productive. Levers start day two, aimed **only** at the
leverable set, judged against the **measured** noise floor.

---

## 8. Defaults for when you start levering (day two onward)

Earned the hard way in ade-bench; adopt as the starting discipline, not re-derive:

- **Worked-example skeletons, not prose principles.** Prose goes inert (read, reasoned
  about, never reaches the committed artifact). Copyable before→after examples with generic
  identifiers are the only delivery form proven to change the code.
- **A ported README can start LEAN — verbosity is not robustness.** Distill each accepted
  rule to **principle + precondition gate + one generic BEFORE/AFTER skeleton** (plus any
  *negative steer*, e.g. "do not start from raw seed edits"). The scar-clauses, domain-specific
  framing, hard-coded dataset/table identifiers, and repeated byte-intact hedges that accumulate
  around a rule are *restatements* of the construct, not added signal — safe to drop. ade-bench
  h0061 cut a tuned README's added length roughly in half (10 rules compressed) and reproduced
  the prior `@baseline` **cell-for-cell** (paired delta 0, CI [0,0], 0/48 verdict changes,
  0/33 off-construct cells moved). A longer README buys no extra held constructs; the only thing
  a leaner one saves is the carrying cost of prose — so a new benchmark's README should START at
  the lean shape, not accrete scar-clauses and later try to trim them.
- **Precondition-gate every lever** so disjoint ones compose additively in one artifact —
  the gate IS the isolation. Lets you bank many flips at once and re-verify cheaply.
- **Carry ≥1 perturbable same-construct canary** into smoke (a non-firing canary is not
  enough to prove a lever is bleed-free).
- **Judge by committed artifact + reproducibility, not single-draw net** — until the
  measurement (§3/§4) is good enough to trust a CI. A green score is not lever attribution;
  read the committed artifact to confirm the prescribed edit actually landed.
- **Never author independence in-context.** Any checker / judge / abstention rail written as
  prompt prose is graded by the same model that did the work, so it self-grades (fires when
  it shouldn't, or refuses to fire when it should). If you need an independent check, it must
  be operator-side harness code or a different model — decided at the workflow level, declined
  at the gatekeeper if proposed as prompt prose.
- **A behavior-preserving refactor carries its own oracle-free check** (before == after /
  double-entry reconciliation). This is the cleanest way past the oracle wall — the only
  lever form that supplies its own correct answer without leaking anything.
- **Maintain a living dead-family map** so you never re-run a documented wall under a new
  name; treat negative results that clear dead weight as real progress.
- **A decision-fork simulation validates tendency, not real-run compliance** — trust it to
  skip smoke only for a merge of already-solo-verified levers, never to validate a new one.

---

## 9. What success looks like at end of day one

You should be able to answer, with evidence:
1. What's the honest baseline, and is it stable (noise floor known)?
2. Are the failures the solver's fault or the harness's? (Infra bugs fixed.)
3. Which failing tasks are even *winnable* from the prompt side, and which are oracle-blind?
4. What's the realistic prompt-side ceiling, and what would the benchmark owner have to
   change to raise it?

If you can't answer these, day two is premature — you'll be levering blind, which is the
exact trap that cost ade-bench its first week.
