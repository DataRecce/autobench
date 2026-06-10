# Retrospective — Round 2 Workflow-Stage Program (2026-06-10)

> Companion to `round-2-workflow-stage-program.md` (the Round-2 plan) and the Round-1
> retrospectives (`retrospective-2026-06-07.md`, `retrospective-2026-06-08.md`). Same rules:
> every claim cites a run-dir or archive entity. h0041's full run is still parked (captain
> midnight trigger); everything else in the Round-2 set is terminal, so this retrospective is
> written now — h0041 is observe-only and cannot change the score accounting below.

---

## 1. Plain words first

Round 2 ran five workflow-stage hypotheses (h0037–h0041) plus the airbnb009 banking step.
**The score did not move: `@baseline` stays 31/48 (0.6458).** Worse than the plan's floor: the
one gain the proposal called *sure* — banking airbnb009 to reach 32/48 — **failed**. The flip
did not reproduce at trials:1 (h0019 E2-alone full `8773355d65f92e1b`, net −1, airbnb009 stayed
`Got 1`), so the "honest ceiling" of 32 collapsed back to 31.

Everything else landed almost exactly where the proposal predicted: the two run-worthy
experiments and the three method instruments all produced **0 flips**, and four of the five are
REJECTED. The exception is h0041 (the observe-only triage ledger), the only smoke GO, whose
full run is parked.

The sober headline: **the proposal's predictions were right everywhere except the one place it
claimed certainty.** Every {0}-flip prediction held; the single "+1, already in hand" failed.
That inversion is itself the most important finding of Round 2 (§4.1).

What we bought with the round is knowledge, not score — and by the standing
knowledge-gains-are-small-successes doctrine that is real progress: the oracle wall is now
confirmed from every remaining structural angle (generate / review / enforce / observe), one
genuinely new wall was found (self-credited trigger clauses, §4.2), and four reusable
positive primitives were banked (§5).

---

## 2. How the experiments were designed (the design, restated honestly)

The Round-2 design was deliberately defensive, built on Round-1's conclusions:

- **The box was fixed.** Independent variable = the solver README only; one `## Stage:` per
  hypothesis; specs differ from `@baseline` only in `experiment:` + `solver_workflow:`;
  `trials: 1`; benchmark FIXED; leak-guard sacred.
- **The gatekeeper had already said no.** Every Round-2 flip-seeking candidate resolved to
  METHOD-ONLY at ideation; zero KEEP verdicts. The program knowingly ran experiments whose
  *predicted* flip count was {0}, valuing structural knowledge about the solver stage graph.
- **The portfolio had three tiers:**
  1. **Banking** (not an experiment): re-run the frozen h0019 spec, judge by committed artifact.
  2. **Two run-worthy structural bets** — h0037 Reference Mining (systematize the h0019
     lone-survivor engine into a generative pre-Implementation stage) and h0038 Plan Review
     (the never-run Method B: independent re-derivation + generic invariant, REJECT only on a
     locally-visible contradiction, else abstain).
  3. **Three instruments/rails** — h0039 observe-only debug lens (M1), h0040 enforced
     abstention rail (M2/Track Z), h0041 observe-only triage ledger (M3, de-risks M2).
- **Measurement discipline:** judge by committed-artifact proof + bleed-free canaries, never
  multi-trial CI; `Got N` as leading indicator; pre-registered kill-paths in every entity;
  perturbable canaries for generative levers; strict audit before any score is trusted.

Design quality verdict: **the experimental method was sound and is not what failed.** Every
hypothesis had a falsifiable claim, a pre-registered kill-path, and the kill-path is what
actually fired in 4 of 5 cases. The smoke panels caught what they were designed to catch; the
attribution reads (artifact, not score) correctly separated variance from lever effects three
times (h0037's −1, h0039's asana003 drop, h0038's asana004 worsening).

---

## 3. What happened — per-experiment results

| Entity | Type | Predicted | Actual | Verdict | Run(s) |
|---|---|---|---|---|---|
| **Bank airbnb009 (h0019)** | banking step | **+1 sure** | **flip NOT reproduced; net −1 (noise)** | real-but-UNPROMOTABLE | full `8773355d65f92e1b` |
| **h0037 Reference Mining** | experiment (E-RMS) | {0} flips, wall holds | 0 flips on the wall; full net −1 = variance, not regression; reach + safety proven | REJECTED (richest positive mechanism finding) | smoke `6671b5e449bd0975`, full `5d707b3cdf7901b3` |
| **h0038 Plan Review / Method B** | experiment (E-PRMB) | {0} flips, abstains correctly | **FALSE-REJECTED its own abstention target**; harmless only via the record-only rail | REJECTED (NO-GO at smoke) | smoke `ee924fbc9d3b0b20` |
| **h0039 Observe lens (M1)** | instrument | 0 flips, 48-task corpus | **fully inert** — `/razorback-freeze` routing precondition is dead; no corpus | REJECTED-inert | smoke `e84f83324081c22d` |
| **h0040 Enforced rail (M2)** | rail | 0 flips, enforce-or-inert question | **revert NEVER fired** — solver self-credits the trigger clauses; bleed-free (G10 clean 8/8) | REJECTED-inert (spec banked) | smoke `41c556510ff753a7` |
| **h0041 Triage ledger (M3)** | instrument | 0 flips, would_abstain map | smoke GO: routing fix worked 8/8, zero contamination, 0/8 would_abstain, airbnb009 decidable | smoke GO; **full parked** | smoke `45c2ba6667a47a60` |

Per-experiment detail (one paragraph each; full forensics live in the entity files):

**Banking airbnb009 — the failure that matters.** The lever itself FIRED in all three runs ever
taken (smoke `d8bd75a0…`, combined `1880d649…`, standalone full `8773355d…`): the identical
one-file anti-cross-join edit landed every time. What differed in the failing run was **one
line the rule does not pin** — `COUNT(*)` vs `COUNT(review_cte.REVIEW_DATE)` in the aggregate —
and that free choice alone flipped the hidden date-range test. So "artifact-proven + held once
at full" is still not bankable when the edit retains an unpinned degree of freedom whose
correct setting is oracle-only. The fix is real; the measurement regime cannot bank it.

**h0037 Reference Mining — the one clean positive mechanism result.** The stage reached
committed SQL (cited `Analog: obt_sales_overview.sql:1-78`, construction landed in
`obt_product_inventory.sql`; fired on ~21/48 authoring cells), clearing the h0010/h0016
inert-prose bar and the h0033 green-but-inert bar. The own-sibling-first gate is artifact-proven
bleed-free at scale (f1001 held 6/6 incl. the three tests h0023 bled; no passer broken by a
wrong/wider analog across all 48). Efficacy was {0} exactly as predicted: ana-eng004 held FAIL
byte-identical at the D6 width wall. The full-run net −1 (+asana002 / −f1006-hard −f1010-medium)
is forensically attributed to single-trial solver-reasoning variance on ambiguous repairs
(max-vs-latest; subtract-vs-exclude), not to the lever. New transferable boundary: **structural
construction-copy is inert on task-semantic dimensions it does not encode.**

**h0038 Method B — a sharper negative than predicted.** Predicted: abstain everywhere
(`PROCEED_UNDETERMINED`), {0} flips. Actual: it REJECTed 3 of 7 cells that emitted a record,
including asana004 — the exact cell the spec said MUST abstain — by pattern-matching the
"never grain from a pre-filtered child" invariant onto a FROM clause it could not locally
ground. The only "correct" abstention (intercom001) was an accident of empty SQL (creation
task). Conclusion banked: **Method B is empirically no better than Method A** — an independent
re-derivation against a generic invariant, applied as a pattern, false-rejects exactly where
the deciding fact is correlated-out of every local relation. The record-only rail is the sole
reason it was harmless.

**h0039 → h0041 — one instrument, two attempts, one infrastructure discovery.** h0039 routed
its record through the baseline README's `/razorback-freeze` "exactly one child directory"
precondition and went fully inert — and surfaced that the precondition has been silently dead
the whole time (even `@baseline` never wrote freeze notes). h0041 rebuilt it with unconditional
`/tmp` write + `cat`-to-stdout and the record durably landed on 8/8 cells with zero
contamination. That routing fix then held in h0038 (7/8), h0037 (all firing cells), and h0040
(13/13) — **the one piece of Round-2 infrastructure that is now validated 4×.**

**h0040 Enforced rail — h0031's wall found in a NEW place.** The revert never fired on any of
the 5 oracle-only Panel-A cells: every `triage.json` was well-formed and fully populated, but
`abstain = NOT instr AND NOT schema AND NOT raw_probe` evaluated false on every claim because
the solver **self-credits the clauses** (instruction "names" the quantity wherever the task
surface-names a column; the raw probe "decides" claims it cannot decide). This is not h0031's
empty `abstained_claims:[]` (permission-not-fired); it is mechanically-derived enforcement
whose *inputs* are discretionary self-reads. The G10 safety read was clean — 8/8 passers held,
zero wrong reverts — so the bleed-free revert primitive is banked for a future pairing.

---

## 4. Are we closer? And why it doesn't work

**On score: no.** 31/48 before, 31/48 after, and the credible ceiling *dropped* from 32 to 31
because the one bankable point proved unbankable. 75% (36/48) required +4 beyond that ceiling
and was already declared unreachable inside the box; Round 2 confirmed it from the remaining
untested angles.

**On knowledge: yes, materially.** Round 1 ended with one wall (the oracle problem) and several
open questions: is Method B different? can an observe lens be built? can abstention be
enforced? can the survivor engine generalize? Round 2 closed all four, each with a clean
artifact-grounded answer. The program now has a *complete* negative map of the
solver-README-stage design space, plus three structural insights that interlock:

### 4.1 The variance wall extends to banking (the new, painful one)

At trials:1 with gpt-5.5/xhigh, a +1 lever cannot be banked even when it demonstrably fires,
**unless the prescribed edit pins every load-bearing degree of freedom.** h0019 pinned the
predicate (the BETWEEN bound) but left the aggregate line free; the solver's coin-flip on the
free line decides the hidden test. The proposal treated "fired + held once" as sufficient for
banking; it is not. Corollary: in this regime the bankability bar is *determinism of the
committed artifact*, not attribution of it.

### 4.2 The self-grading wall (generalizes h0031 + h0040 + h0038)

Any mechanism expressed as solver-README prose — REJECT verdicts, abstention triggers,
enforcement rails — is evaluated by the same model in the same context that produced the work
being judged. Round 2 shows this fails in BOTH directions on the same wall: h0038's clauses
fire when they shouldn't (false-reject: the invariant pattern-matches), h0040's clauses refuse
to fire when they should (self-credit: the trigger booleans read true). **Independence cannot
be authored in the same context.** Mechanizing the *derivation* (h0040's AND-of-NOTs) buys
nothing when the inputs are self-graded; pinning the *schema* buys nothing when gpt-5.5 drifts
the record shape (4 sightings across h0041/h0038/h0037/h0040). This is the deepest transferable
lesson of the round and the program-level reason the entire "checking lever" family is closed.

### 4.3 The oracle wall held every remaining angle (now exhaustively)

The deciding facts (width column-sets, grain conventions, value semantics, pit-stop rules,
date-range counts) live only in `solution__*` + hidden tests. Round 2 attacked it via
generation (copy a passing analog — wrong dimension: convention, not the deciding value),
review (re-derive independently — false-rejects), enforcement (revert undecidable edits —
self-neutralizes), and observation (map decidability — the only independent clause decided
nothing on 8/8). Combined with Round 1's contracts, selectors, arbitration, reconciles, and
recomputes, **every structural shape available inside the README box has now been run or
provably reduced to a dead family.** The wall is not under-explored; it is closed.

Why the three interlock: to beat the oracle wall (4.3) you need an independent check — blocked
by self-grading (4.2). To bank small real wins instead, you need repeatability — blocked by the
variance/pinning wall (4.1). And full pinning of an edit is equivalent to leaking the per-task
answer, which is out of scope. That triangle is the box, fully mapped.

---

## 5. What was banked (the positive ledger)

1. **Durable observe-only write-path** — unconditional `/tmp/<record>.json` + `cat`-to-stdout
   into the session transcript. Validated 4× (h0041 8/8, h0038 7/8, h0037, h0040 13/13).
   The `/razorback-freeze` notes precondition is confirmed dead; never route through it.
2. **Own-sibling-first reach primitive (h0037)** — a generative analog-copy stage that reaches
   committed SQL without bleeding (h0023's vector closed, proven at all-48 scale). Reusable iff
   ever paired with a lever that supplies the *semantic* deciding fact.
3. **Record-only rail** — the design distinction that kept h0038's ungrounded REJECTs and
   h0040's triage harmless. Any future judging/observing stage must stay record-only unless its
   trigger inputs are independently evaluated.
4. **Bleed-free revert primitive (h0040 spec)** — banked for a hypothetical future pairing with
   a lever that actually bleeds; do not re-run standalone on the non-bleeding minimal baseline.
5. **Boundary statements** (negative knowledge, citable): Method B ≡ Method A on the wall;
   structural construction-copy is inert on un-encoded task semantics; prose-pinned schemas
   drift under gpt-5.5 (consumers must derive, not parse); enforcement prose self-neutralizes
   via self-credited clauses.

---

## 6. Suggestions (operator's insight — for the captain to decide)

**S1 — Declare Round 2 closed and stop filing README-stage hypotheses.** The design space is
exhaustively mapped (§4.3). A Round 3 inside the same box would re-run documented walls under
new names — exactly what the dead-family map exists to prevent. The Round-2 success definition
from §8-Q4 of the proposal should be adopted *minus the banked point*: 31/48 + a complete wall
map + the method portfolio.

**S2 — Decide h0041's parked full run on its real remaining value, which has shrunk.** Its
stated purpose (de-risk h0040 before trusting it to revert) is moot — h0040 is already
rejected-inert. The residual value is a 48-task decidability/clause corpus at zero score risk.
That is worth one cheap run **only if** the captain wants the corpus to inform a future
*benchmark-design* proposal (it would document, per task, which deciding facts are locally
absent — strong evidence for §S4). Otherwise cancel it; do not run it out of momentum.

**S3 — If airbnb009 still matters, settle it with sequential single-trial repeats, not CI.**
The trials:1 doctrine exists because of budget and the freeze-repo concurrency race
(`concurrency.trials>1` breaks; standing decision: don't fix it). But nothing forbids **N
sequential 1-task, 1-trial runs of the frozen h0019 spec on airbnb009 alone** (~9 min each).
Three repeats give a 0–3 reproduction count for under 30 minutes total — enough to either bank
the point under a captain-amended rule ("bank at ≥2/3 on the target cell") or close it
permanently. This respects the spirit of single-trial economy while fixing its one
demonstrated blind spot: a real fix left unbankable by a coin-flip (§4.1). Alternative if no
repeat is wanted: amend the h0019 rule to pin the aggregate line (`COUNT(*)`, never a
column-count) — the one unpinned degree of freedom is known and one line; a single re-run then
tests a fully-pinned edit. Either path is cheaper than the value of the only real +1 the
program ever found.

**S4 — Re-scope or re-state the goal: 75% requires changing what ships, and the program is now
the proof.** The honest deliverable the loop is uniquely positioned to write is a
**benchmark-design recommendation**, grounded in 41 hypotheses of evidence: ade-bench tasks are
unsolvable past ~65% by *any* prompt-side lever because (a) deciding facts are oracle-only,
(b) declared contracts lie or are absent (f1002 over-declares 6 vs 3; ana-eng004 undeclared),
and (c) self-checks structurally false-green. Concrete fixes only the benchmark owner can make:
ship truthful `schema.yml` contracts, ship the `tests/` the oracle runs (or a subset), or score
against declared-not-hidden expectations. If the 75% goal stands, this document — not another
lever — is the path to it.

**S5 — If any future checking/enforcement lever is ever considered, require structural
independence up front.** The §4.2 wall implies a hard gate: a trigger clause counts as
independent only if it is evaluated *outside the solver's context* (different session, different
model, or operator-side harness code), not by prose instruction. Inside the current scope
(benchmark fixed, solver access fixed) that is impossible by construction — which is itself the
clean one-line reason to decline such proposals at the gatekeeper without spending a run.

**S6 — Carry the two repeat-offender measurement lessons into any future loop config:**
(a) schema drift is structural — any machine-readable solver record must be consumed by
derivation over content, never by parsing a pinned field; (b) smoke panels cannot exercise
generative levers on repair tasks (h0037's "perturbable OBT canaries" were repairs the
author-gate correctly skipped) — panel selection must check the *task type* fires the lever,
not just the family/model overlap.

---

## 7. Cross-refs

- Round-2 plan: `_proposal/round-2-workflow-stage-program.md`.
- Entities: `h0037` (active file, REJECTED, awaiting archive), `_archive/h0038`,
  `_archive/h0039`, `_archive/h0040`, `h0041` (smoke GO, full parked),
  `_archive/h0019` (banking failure, E2-alone `8773355d65f92e1b`).
- Runs: h0037 smoke `6671b5e449bd0975` / full `5d707b3cdf7901b3`; h0038 `ee924fbc9d3b0b20`;
  h0039 `e84f83324081c22d`; h0040 `41c556510ff753a7`; h0041 `45c2ba6667a47a60`;
  `@baseline` `runs/ade-bench-baseline/622bdedac572b479` (31/48).
- Ledgers: `_artifacts/WORKFLOW-REFINE.md` (all five structural entries finalized);
  `_artifacts/verification-without-oracle.md`; `_gatekeeper/propose-review-guideline.md`.
