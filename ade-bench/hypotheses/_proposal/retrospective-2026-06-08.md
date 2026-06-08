# Retrospective Addendum — Post-Program Work (2026-06-08)

**Scope.** A companion to `retrospective-2026-06-07.md` (the oracle-problem end-of-program
retrospective covering E0–E4 + the combined full). After that retrospective the captain continued
the loop: ran **E5** (h0035, the last filed flip-seeker), then chose to **hunt a new target** —
a forensic re-triage of the 9 LOW/Track-Z failures — which produced and ran **E6** (h0036). This
addendum records that post-program work and the (negative) result, and closes out two open items
the prior retrospective left for "next session" (§5.2 re-triage, §5.3 source a 6th target).

**Headline:** `@baseline` is still **31/48 = 0.6458**. E5 and E6 both REJECTED. The visible-arbitrator
flip portfolio is now **fully exhausted** — airbnb009 (E2/h0019) remains the single genuine fix, and
the captain will bank it with a one-off h0019 full-promote run at a later time (→ 32/48). No 6th
target exists at the current solver visibility.

---

## 1. Honest accounting — two more clean negatives, no score movement

| Exp | Hypothesis | Target(s) | Outcome | Net |
|-----|-----------|-----------|---------|-----|
| E5 | h0035 | quickbooks001 | **REJECTED** — scope-gated ref-graph deliverable; INERT (green-via-package-namespace); ZERO bleed | 0 (MEASURED-not-counted) |
| hunt | — | re-triage of 9 LOW/Track-Z | 1 candidate found (ana-eng007); 8 confirmed oracle-only; 4 queued hypotheses disproved | 0 |
| E6 | h0036 | ana-eng007 (+medium) | **REJECTED** — coverage lever LANDED, recovered the dropped rows, but unmasked an oracle-only VALUE bug (`Got 5 → Got 10`) | 0 |

Nothing promoted. `@baseline` unchanged. The one bankable +1 (airbnb009) is **deferred by captain
decision** — the E2/h0019 anti-cross-join lever already solves it (smoke-GO + held at full,
artifact-proven both times); banking it is a one-off single-trial full-promote run the captain will
execute later, not a new experiment.

---

## 2. New methodological findings

### 2.1 Green-via-package-namespace inertness (E5/h0035)
A build-rule that asks the solver to materialize models from an installed package's templates goes
**inert when the project already builds fully GREEN through the package's own namespace.** For
quickbooks001 the three absent `stg_quickbooks__*` staging models are resolved downstream against the
installed `fivetran/quickbooks` namespace, so the project compiles clean (`PASS=172, ERROR=0`) without
them — there is no red trigger pointing at the missing models, and the solver stops at "smallest fix →
green → done." This is a sharper inertness mode than h0013/h0015's total read-failure: the rule was
read and reasoned about but never converted to artifacts because **a clean build masks the deficiency.**

**The positive half:** E5's **scope-gate** (fire ONLY on the project's own referenced-but-absent set;
never treat an installed package as a source, never invent `src_*`) is a **validated bleed-free design.**
It fixed h0023's over-fire — f1001 held 1.0 and the `stg_models_use_src_models Got 11` crash signature
never recurred. The design works; the lever was just inert. (Encoded in `bug-type-taxonomy.md` #6.)

### 2.2 Coverage-masks-oracle-value — a LANDED lever that still loses (E6/h0036) — the key finding
This is the most instructive negative of the whole program. Unlike every prior dead lever, **E6 was
NOT inert.** Primed by the source-key coverage rule, the solver found and removed the hidden filter
`WHERE supplier_ids NOT LIKE '%;%'` in `stg_products.sql` that was dropping the 5 md5-hashed product
rows; `dim_products` grew 40 → 45 and the raw-source coverage anti-join went empty
(`raw_distinct=45 | rows=45 | distinct=45`). The construction-edit-shape lever + raw-source signal —
the f1007-hard shape, the loop's one proven independent catch — **fired correctly on its own terms.**

And it still lost. **Recovering coverage unmasked an oracle-only VALUE bug.** The 5 recovered rows
came back with wrong attribute values (the correct values live only in the hidden seed; no local
relation recomputes them), so the equality distance got *worse*: `Got 5 → Got 10`, and two downstream
OBT models broke. New named pattern: **a coverage drop can MASK an oracle-only value bug — fixing the
coverage surfaces the masked rows as wrong-valued and distance doubles (`Got N → Got 2N`).**

The generalization sharpens the oracle wall: *a genuine independent check helps only if the quantity
it recovers/verifies is itself locally determinable.* A raw-source coverage anti-join is genuinely
independent — but coverage-alone is insufficient when the masked rows also need oracle-only values.
This also corrects the optimistic mid-hunt read (the `Got 5` one-directional diff did indicate missing
rows, but "missing rows" was a symptom of an upstream filter hiding rows whose *values* were wrong).

### 2.3 The re-triage closes §5.2/§5.3 — there is no mis-triaged 6th target
A forensic re-triage of all 9 LOW/Track-Z failures against primary evidence (verifier output +
solver transcripts + task datasets + the sharp test) confirmed they are **informationally blocked,
not selection-blocked**:
- **asana004/005/005-hard** (`int_asana__project_user_agg` `Got 3`): oracle-only. The intermediate's
  true grain (full 16-project spine vs the literal-CTE 13) is **erased downstream** by
  `asana__project`'s `LEFT JOIN … coalesce(…,0)` — invisible to every local check; any "completeness"
  arbitrator would have to *assume* the answer.
- **ana-eng004 / f1002** (width, "less columns"): oracle-only. f1002's `schema.yml` **lies**
  (declares 6 columns, truth is 3); ana-eng004's target model isn't declared at all. The true sets
  require column **DROPs** that live only in the hidden solution.
- **ana-eng007 / -medium**: looked locally-arbitrable (coverage) → ran as E6 → oracle-blocked (§2.2).
- **f1006**: oracle-only (2 residual rows not locally pinnable; mini-solvable ≠ locally-arbitrable).
- **f1011**: oracle-only (h0031-proven misleading local signal).

**Two doctrine factual errors corrected** in the process: f1011's truth is **"ADE"** (not "ABE") — the
wrong letter is **B**, and D is correctly included; ana-eng007 is **coverage-then-oracle-blocked**, not
a value-divergence dedup tie-break. The re-triage also **disproved four filed-but-unrun hypotheses**
(retired REJECTED, no run spent): h0021 (dedup that doesn't exist; would crash on the md5 ids), h0029
(reconciles against the lying schema → reinforces the bug), h0014 + h0022 (built on the wrong f1011
truth / inverted mechanics).

---

## 3. Dead-family map — final state (updated from §3 of 2026-06-07)

| Family | Status | Why dead |
|--------|--------|----------|
| Grain construct (prose/example/contract) | EXHAUSTED | inert at gpt-5.5/xhigh (h0010/h0016/h0017) |
| Grain reconcile (raw-source count + anti-join) | EXHAUSTED + ORACLE-BLOCKED | re-correlates through the shared filter (E1/h0030) |
| Cast / type-contract | EXHAUSTED | asana002 is structural, no cast surface (E4/h0033) |
| Candidate-generation + arbitration (selector, dual-contract) | EXHAUSTED | generation/arbitration is table stakes, not an oracle (h0026/h0031); **the queued selector family h0024/h0025/h0027/h0028 inherits this verdict — retire as G9-exhausted** |
| **Incomplete-deliverable / missing-models** | **DEAD, 5-for-0** | green-via-package-namespace inertness (h0009 −3 / h0013 inert / h0015 inert / h0023 f1001-bleed / h0035 inert) |
| **Width (#2)** | **ORACLE-ONLY** | declared column sets lie or are absent; true set needs DROPs from the hidden solution (h0029 retired) |
| **Coverage / value-divergence (ana-eng007)** | **ORACLE-BLOCKED** | coverage is locally fixable but masks oracle-only values (E6/h0036; h0021 retired) |
| Analytical-answer (f1011) | ORACLE-ONLY | misleading local signal, h0031-proven (h0014/h0022 retired) |

**The single survivor family** is unchanged from 2026-06-07: surgical, copyable, in-place
**Implementation-stage worked-example edits** anchored to a concrete local artifact — the shape that
landed airbnb009 (E2). It works only when the target is a **value/shape to match**, **single-model**,
with the deciding quantity **locally determinable**. E6 confirmed the boundary: even when this shape
*lands*, an oracle-only quantity underneath kills the flip.

---

## 4. Method deliverables banked this session

1. **Coverage-masks-oracle-value (`Got N → Got 2N`)** — a landed lever can still lose when fixing the
   visible symptom unmasks an oracle-only quantity. (§2.2; `verification-without-oracle.md`,
   `bug-type-taxonomy.md`.)
2. **Green-via-package-namespace inertness** — a clean build can mask a deliverable deficiency, so a
   build-rule has no trigger to fire on. (§2.1; `bug-type-taxonomy.md` #6.)
3. **Scope-gate = a validated bleed-free design** — fire only on the project's own referenced-but-absent
   set; it fixed h0023's over-fire even while the lever was inert. (§2.1.)
4. **Three distinct failure modes, separated** — INERT (lever never fired: h0035), LANDED-but-lost
   (lever fired correctly, target oracle-blocked underneath: h0036), and the dead self-anchored family
   (correlated false-green). Only the first is about the lever; the second is about the task.
5. **A reusable re-triage audit** — challenge each "oracle-only" verdict against primary evidence + the
   sharp test; it disproved 4 queued hypotheses and 2 doctrine errors in one pass. Negative results that
   *clear dead weight* are real progress (the "knowledge gains are small successes" doctrine).

---

## 5. Final state and the one remaining move

- **`@baseline` = 31/48.** One bankable +1: **airbnb009 (E2/h0019)** — proven, artifact-verified,
  bleed-free, single-model, lever-attributable. **Deferred by captain decision**: the captain will run
  a one-off single-trial h0019 full-promote run at a later time → **32/48**. This is a banking/measurement
  step, not a new experiment (the lever already solves the task).
- **The flip portfolio is exhausted.** Every other failure of the 17 is oracle-blocked — confirmed by
  the §2.3 re-triage. There is no 6th visible-arbitrator target.
- **Honest ceiling:** 31/48 now; 32/48 once airbnb009 is banked. **Reaching 36/48 (75%) requires
  changing what ships to the solver** (truthful declarations / tests / solution visibility) — a
  benchmark-design change, out of scope per decision #4. No prompt/README lever closes the remaining gap.
- **Open housekeeping:** the selector family h0024/h0025/h0027/h0028 should be retired as G9-exhausted
  (same wall as h0026/h0031); not yet done — a one-pass cleanup when convenient.
- **The standing measurement note** (from 2026-06-07 §2.1, still true): at `trials:1` the run-to-run CI
  is ±4 tasks. The captain's directive to NOT run multi-trial smoke/full stands — we judge flips by
  **artifact-proof + bleed-free canaries**, not the noisy aggregate. airbnb009's banking run should be
  judged the same way (flip artifact-proven + no real canary regression), accepting incidental
  single-trial wobble as noise.

---

## 6. Bottom line for the captain (plain words)

We went looking for one more winnable task and confirmed there isn't one the solver can actually reach.
The best candidate (ana-eng007) taught us the sharpest lesson of the program: our fix made the code do
exactly the right structural thing — it recovered the rows that were being dropped — but those rows
needed values that only the hidden answer key holds, so the result got *worse*, not better. The other
fifteen failures are all that shape: the answer simply isn't in what the solver is allowed to see. We
also cleared the dead weight — retired five doomed ideas without spending runs on them and fixed two
mistakes in our own notes. The one real win we own, airbnb009, is yours to bank with a single full run
whenever you have time → 32 of 48. Past that, moving the number is a benchmark-design question (change
what the solver is shown), not a smarter prompt. The program's durable output is the *method* — which
ideas work, which are dead, and why — not the pass-rate, which stands at 31 (32 once you bank airbnb009).

---

**Cross-refs:** `_proposal/retrospective-2026-06-07.md` (the main retrospective);
`_proposal/oracle-problem-systematic-program.md` (the plan, E5 + decision #5 updated);
`_archive/h0035` (E5), `_archive/h0036` (E6), `_archive/{h0021,h0029,h0014,h0022}` (re-triage retirements);
`_artifacts/{verification-without-oracle.md, bug-type-taxonomy.md, arbitration-without-oracle.md}` (doctrine, corrected 2026-06-08);
`h0019-implementation-let-categories-emerge-not-cross-join.md` (the deferred-banking fix);
run dirs `runs/ade-bench-baseline/622bdedac572b479` (@baseline 31/48),
`runs/ade-bench-h0035-implementation-scope-gated-package-deliverable-set/efa1b651f71941b4` (E5 smoke),
`runs/ade-bench-h0036-implementation-source-key-coverage-preserve/c51545c270b51f6d` (E6 smoke).
