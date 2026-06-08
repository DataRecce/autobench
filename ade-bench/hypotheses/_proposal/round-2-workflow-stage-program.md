# ROUND-2 PROPOSAL — Workflow-Stage Program for the ade-bench Oracle Problem (2026-06-08)

> Companion to `oracle-problem-systematic-program.md` (the Round-1 plan) and the two retrospectives
> (`retrospective-2026-06-07.md`, `retrospective-2026-06-08.md`). Same rigor, same honesty: every
> claim below is grounded in a Round-1 run, archive entity, or banked doctrine note. No false hope.

---

## 1. TL;DR + the honest frame

**`@baseline = 31/48 (0.6458)`** (run `runs/ade-bench-baseline/622bdedac572b479`). Goal is still **36/48 (75%)**. The honest ceiling inside the fixed-benchmark box is **~32/48** — 31 today, +1 once the one real fix (airbnb009 / h0019) is *banked* by a deferred captain full-promote run, which is a banking step, not an experiment. **75% is not reachable inside this box** and Round 2 will not pretend otherwise.

What Round 2 is actually for, in plain words:

1. **Bank the one sure point** (airbnb009 → 32/48) without spending an experiment slot on it.
2. **Run the genuinely-new STAGE-level bets the captain asked for** — the never-run Plan-Review *Method B* and the Reference-Mining / Analog-Copy stage — as honest experiments with pre-registered kill-paths. These are expected to yield **mostly {0 or 1} flips**; their value is structural knowledge about the solver stage graph, not pass-rate.
3. **Stand up the method / net-protecting deliverables** the program has wanted but never built: the observe-only debug-lens corpus and the *enforced* abstention rail (Track Z). These are explicitly **0-flip** instruments, valued under the knowledge-gains-are-small-successes doctrine.

The strict-scope constraints (captain decision, 2026-06-08) bind every line below:

- **Independent variable = the solver README ONLY** (`solver_workflows/codex-ade-dbt-minimal/README.md`). Full spec differs from baseline in exactly `experiment:` + `solver_workflow:` (G3); each hypothesis touches **one** `## Stage:` (G1). `trials: 1` always.
- **Decision #4 holds — the benchmark is FIXED.** No new `tests/`, no `solution__*` seeds, no truthful schema, no benchmark-design change. **No expanded solver access** — no new tools, no fetching external/published solutions, no reading the hidden oracle (`AUTO_*_equality`, `solution__*`, `check_option_*`, `tests/AUTO_*`). Leak-guard is sacred.
- **In scope:** re-processing material that ALREADY ships to `/app` — installed packages (`fivetran`/`quickbooks`), sibling models, the project's own passing models — via a workflow stage.

**The wall, restated.** All 17 failures are **self-anchored false-greens**: the solver self-checks 10/10 clean; the hidden oracle re-runs `AUTO_*_equality` / `check_*` against `solution__*` seeds and fails. The solver ships **no `tests/` and no `solution__*`** — it is blind to the oracle. Every stage shape tried in Round 1 (single contract h0017, dual-contract + arbitration h0031, selector h0026) reproduced this false-green. *Adding a route, a contract, or a selector does not manufacture an oracle.* This is the boundary Round 2 works inside, not against.

---

## 2. The one sure gain — BANK airbnb009 (E2 / h0019) → 32/48

**This is a banking step, not an experiment.** Do not file it as a new hypothesis; do not re-smoke it.

airbnb009 is the program's single genuine fix and the type specimen of the lone survivor family (Section 4): a surgical, copyable, in-place Implementation worked-example anchored to a concrete local artifact. h0019's anti-cross-join rule flipped airbnb009 FAIL→PASS **at smoke AND held at full**, artifact-proven both times: committed `models/agg/mom_agg_reviews.sql` swapped `WHERE DATE_ACTUAL IN (SELECT DISTINCT REVIEW_DATE…)` for `WHERE DATE_ACTUAL BETWEEN (MIN…) AND (MAX…)` (3,786 → 4,508 dates) and let the 3 sentiment categories emerge through the existing `LEFT JOIN` instead of cross-joining. Single-model, lever-attributable +1 (run `d8bd75a0189bda65`; file `h0019-implementation-let-categories-emerge-not-cross-join.md`, status **ACTIVE**).

It is **unpromoted only because of the variance wall.** In the combined-full run (h0034, `1880d6497bdd6303`) its clean +1 was masked inside the [−4,+4] paired-CI band by ±2 unrelated single-trial noise (asana003 build error + f1005 QUALIFY off-by-2, both rule-independent gpt-5.5 non-determinism).

**How to bank it (single-trial doctrine).** Judge by **committed-artifact proof + bleed-free canaries, NOT multi-trial CI**:

1. Run the frozen h0019 full spec once (trials:1).
2. Confirm the committed `mom_agg_reviews.sql` carries the `BETWEEN (MIN…) AND (MAX…)` edit (the prescribed token — a green score alone is not attribution, per the h0033 green-but-inert lesson).
3. Confirm the canary panel is bleed-free at the artifact level; treat any asana003 / f1005-class regression as known gpt-5.5 noise, not a do-no-harm failure (it is not lever-attributable).

Outcome: **31 → 32/48.** This is the +1 the honest ceiling already accounts for. Round 2's experiments are *on top of* this, and none is expected to add a second guaranteed point.

---

## 3. The Round-2 experiment program (kept workflow-stage experiments, ranked)

**Honest preamble.** The propose-stage gatekeeper screened every Round-2 candidate. **It returned ZERO KEEP verdicts and zero KILL-of-a-survivor verdicts — every flip-seeking candidate resolved to METHOD-ONLY.** That is the central, sober finding of the Round-2 ideation pass: *the survivors are thin to the point of being empty.* The 17-failure tractability table (Section 5 of the brief; reproduced in the dead-family map below) shows exactly **1 bankable target** (airbnb009, already in hand) and **0** of the remaining 16 with a visible local arbitrator that yields a flip.

Consequently this section is short by necessity and honest by design. Two genuinely-new STAGE-level bets are worth **running as real (single-trial) experiments** because they exercise solver-graph shapes the program has never run live and will return committed-artifact evidence either way. Everything else is method/banking (Section 4). I rank only the two run-worthy bets; I do not manufacture a longer "kept" list out of relabeled dead families.

### E-RMS (rank 1) — Reference-Mining Stage: a cited in-app analog before any model edit

- **Stage shape.** A NEW `## Stage: Reference Mining` inserted **between Exploration and Implementation** — the proven solver-graph insert point (same slot as h0017/h0031/h0032). Touches exactly one new `## Stage:` header (G1 clean).
- **Mechanism.** Before editing any target model, the solver must (a) name the target's directory/layer and grain; (b) locate the closest already-passing **in-project** sibling in the same layer (e.g. `analytics_obt/obt_sales_overview.sql` beside the failing `obt_product_inventory`), or, absent a sibling, an installed-package template of the same shape; (c) record `Analog: <file>:<line-range>` plus the analog's FROM relation, join ladder, spine/key source, window/group-by; (d) in Implementation, copy that construction verbatim as the skeleton and adapt only leaf columns/source. This **promotes the lone survivor mechanism (a verbatim BEFORE/AFTER skeleton anchored to a named local artifact) from a one-off Implementation clause into a generative pre-Implementation stage.** The cited-analog requirement is what makes it structural (reaches SQL like h0017) rather than inert prose (h0010/h0016).
- **Target task(s).** Primary: **ana-eng004** (`obt_product_inventory`, width) — has a confirmed passing same-dir sibling `obt_sales_overview.sql`. Secondary reach-only: intercom001/003 (sibling `int_intercom__*` intermediates exist). Method value: systematizes the survivor across all 48.
- **Independent non-oracle signal.** The in-/app **passing-sibling artifact** — a GREEN model the project's own dbt build already produces. Real, ships to /app, non-oracle: it encodes the project's authored column-ladder / join / grain *convention*. The signal is **convention-fidelity** (does my model's FROM/join/spine match the analog's?), not a target value.
- **Leading indicator (distance).** ana-eng004 `obt_product_inventory` "has less columns" — watch whether the copied `obt_sales_overview` ladder shrinks the gap. **Honest prediction: no movement or wrong-direction** (the sibling is *wider*, so it may ADD columns when the bug needs DROPs). intercom001 `Got 7`: expect flat. A flat `Got N` across the panel = inert / oracle-wall confirmation, the cheapest kill.
- **Kill-path / predicted failure mode.** On ana-eng004 the analog `obt_sales_overview.sql` is structurally **wider** than the target, and the target already follows the identical OBT skeleton; copying the analog's column-ladder ADDS columns while the hidden `AUTO_obt_product_inventory_equality` requires DROPs to match `solution__obt_product_inventory`. Expected flat-or-worse `Got N` — the width oracle wall (D6).
- **Dead family it must avoid + how.** Resembles **D6 width** (h0011/h0023/h0029, ORACLE-ONLY) on its primary target and **D1 grain-convention** on intercom. It differs from the dead **h0009 package-copy** by being gated to the project's OWN passing siblings first (package only as fallback) — removing the h0023 convention-bleed vector that regressed f1001 6/6→2/6; it copies *construction shape* not a deliverable set; it lives in a new pre-Implementation stage that reaches SQL. It differs from h0017 by copying an *existing correct artifact verbatim* instead of authoring a contract from scratch (which h0017 wrote backwards).
- **Expected flips.** **{0}** on the known 17 (the analog is the wrong dimension — convention, not the deciding DROP/value). The contribution is reach-systematization of the survivor engine + a possible distance read on ana-eng004.
- **Expected gatekeeper verdict.** **METHOD-ONLY.** **G7 WARN** (the generative copy-the-analog engine is the survivor — low inert-risk, reaches SQL — but the cited-analog discovery step can go inert). **G8**: generative → requires ≥2 perturbable canaries per OBT family. **No G2/G3/G6 integrity FAIL** (re-processes in-/app siblings only, no oracle/tool access). G9/G11 N/A.

### E-PRMB (rank 2) — Plan Reviewer Method B: a fresh-derivation REJECT stage scoped to a code-contradicts-contract bug

- **Stage shape.** A NEW `## Stage: Plan Review` inserted **between Exploration and Implementation** (proven insert point). This makes Round-1's *simulated-only* Method B runnable as a live, self-imposed fresh-derivation pass. New-stage / new-protocol on the single `## Stage:` graph (G1 clean).
- **Mechanism.** Before any SQL edit: (1) from the task instruction + the *existing* model SQL + a stated generic grain invariant ("a model's grain entity comes from its canonical source relation, never from a pre-filtered child; a completeness/repair output must keep every key the consumer relies on"), RE-DERIVE the intended grain/keys independently, writing the derivation to `plan_review.json` via apply_patch (committed artifact, not chatter). (2) COMPARE that re-derivation against what the existing code actually does. (3) Emit `verdict:REJECT` **only** when the existing code provably contradicts the re-derivation in a way visible from local relations (e.g. it grains on a child the downstream consumer does not restore, dropping keys end-to-end), with `reason` + `contradicting_line`. (4) If the re-derivation cannot be pinned from local artifacts (the oracle-only case), emit `verdict:PROCEED_UNDETERMINED` and build EXACTLY as baseline — **never** reverse-inference (Method A, provably false-rejects). This is Method B: test code against an *independent re-derivation + external invariant*, not internal question-reconstruction.
- **Target task(s).** Infrastructure/method PLUS a regression-prevention rail. **None of the 17 known failures is a clean code-contradicts-contract case** (Section 5 + the 2026-06-08 re-triage): asana004/005 grain is erased downstream by `LEFT JOIN…coalesce` so the contradiction is invisible locally; intercom re-correlates through `_fivetran_active`; width needs oracle-only DROPs. So the live target is (a) catch the class IF the solver *itself* introduces such a contradiction mid-build (a rail on all 48), and (b) deliver `plan_review.json` as a standing reasoning probe.
- **Independent non-oracle signal.** In-/app only: the *existing* model SQL the solver starts with, the task instruction, and local relation row/key counts, re-derived in a deliberately separate pass against a generic leak-clean invariant. Genuinely independent of the solver's build intent **for the code-contradicts-contract class**; not independent of the oracle for the grain-convention class — which is exactly why it must `PROCEED_UNDETERMINED` there.
- **Leading indicator (distance).** On the 16 oracle-blocked failures `Got N` should be **UNCHANGED** (it abstains there) — the honest expected result, not inertness-failure. Decisive smoke read: committed `plan_review.json` on asana004 / intercom001 records `PROCEED_UNDETERMINED` naming the downstream `coalesce` spine-restore (proof it correctly sees the contradiction is not locally decidable). Any `Got N` shrink would have to come from a solver-introduced contradiction it caught — a regression-prevention win, not a known-failure flip.
- **Kill-path / predicted failure mode.** On the 16 oracle-blocked failures it abstains, `Got N` unchanged → reads as inert-but-correct. It never hits a REJECT-and-fix on the known 17 because no failure is the locally-visible code-contradicts-contract class. Method B already VERIFIED asana004 in the Round-1 simulation = **no false-reject, but also no catch** (the discriminating fact — the intermediate carries the full 16-project spine — lives only in `solution/` + hidden tests).
- **Dead family it must avoid + how.** Resembles **D1 grain-construct** and **D4 selector/arbitration**. Differs precisely: (a) NOT a candidate generator/selector — ONE build path reviewed once against an external invariant, never N self-scored candidates (escapes G9). (b) NOT reverse-inference (Method A, provably false-rejects). (c) Unlike h0017 it does not MANDATE building-to-a-contract; it only REJECTs a locally-visible contradiction and otherwise abstains, so it cannot invert the join direction the way h0017 did.
- **Expected flips.** **{0}** on the known 17 (the flip-target class is empty among the 17). Value: the **first live run of Method B** + a standing `plan_review.json` reasoning probe.
- **Expected gatekeeper verdict.** **METHOD-ONLY.** **G1/G2/G3 PASS**; **G6 PASS** (independent re-derivation + invariant compared to CODE, not self-anchored re-run); **G7 HIGH** inert-risk (abstains by design on all 16 oracle-blocked failures, committing only a probe); **G9 escaped** (single build path, external invariant); **G10 partially addressed** (REJECT bound to a raw `source()` anti-join, not plausibility); **G11 N/A**. Residual self-anchoring WARN (the re-derivation may inherit the solver's wrong reading — the h0026/h0031 wall) is mitigated by the raw-source binding and moot because the flip-target class is empty.

### Why no rank 3+

Every other flip-seeking shape proposed in the Round-2 ideation pass — sibling-spine handoff (E-SIB), differential-against-prior-build, enumerate-then-classify (E-ENUM), analog-diff Validation (ADVS) — is a **relabel of the lone survivor engine or a dead family**, and the gatekeeper resolved each to METHOD-ONLY against a concrete kill-path:

- **E-SIB / Differential-against-prior-build** dead-end on airbnb009 (already banked by h0019; @baseline already builds the full date spine unprompted — the load-bearing edit is the anti-cross-join, which the sibling shape does not carry) and go inert on the grain cluster (no canonical-grain sibling exists).
- **E-ENUM** is Exploration-stage enumeration *prose* on the construct side (DEAD-for-0: h0013 inert, h0009 −3) and the h0036/h0030 correlated-recompute wall on the classify side (moving the recompute earlier changes *when* the false-green is logged, not *whether* the deciding fact is oracle-only).
- **ADVS** has no live subject — the one structural-divergence shape it cites (airbnb009) is already banked at construction time, where a later Validation reconcile is strictly weaker.

Filing any of these as a flip experiment would re-spend a run on a wall the dead-family map already documents. They appear in Section 4 (method) or Section 6 (do-not-re-file), not here.

---

## 4. METHOD-ONLY / net-protecting deliverables

These are **not flip-seekers.** Each is labeled method/banking; each is expected to move **0 tasks** and that is the success condition, not a failure. They are the legitimate, valued Round-2 space per the brief (Section I) and the knowledge-gains-are-small-successes doctrine. They split into observe-only lenses (diagnose the wall) and the abstention rail (protect the net).

### M1 — Observe-only debug-lens (the un-built Round-1 Opening #2), built at last

- **Shape.** A NEW observe-only `## Stage:` between Exploration and Implementation (or an observe-only sub-step in an existing stage) that ALWAYS writes a machine-readable reasoning record — a `Contract:` / `plan_review.json` / `divergence.md` block to the sanctioned non-graded notes location (`/razorback-freeze/<child>/…`, baseline README lines 30–32) — and then **builds EXACTLY as baseline.** No build-to-satisfy mandate, no gate.
- **Why it is safe.** It changes no committed SQL by construction, so it **cannot false-green and cannot flip.** The success criterion is `Got N` **UNCHANGED on all 48** (any movement = the gate-strip failed = contamination, NO-GO). It is the exact variant WORKFLOW-REFINE lines 199–201 proposed and never built.
- **Deliverable.** A guaranteed 48-task corpus of the solver's at-build-time mental model, most valuable on the ~14 fired-and-failed cells. h0017 proved the `Contract:` block legibly states the *wrong* model in the solver's own words (asana004 wrote "one row per project_id present in int_asana__project_user"; intercom001 wrote "driven by active conversation part rows" = the bug verbatim). M1 captures that on all 48 instead of only the ~7 cells h0017 fired on, and it feeds the ideate stage with a per-task map of which failures are code-contradicts-contract (a future Method-B subject) vs self-consistent-but-oracle-only (the wall).
- **Honest caveats.** (1) **G7-high inertness in the data-quality sense** — an artifact the solver is told changes nothing has weaker production pressure than h0017's build-feeding contract; h0031 already skipped process artifacts on easy passers. Mitigate with on-disk apply_patch + ≥1 `dbt show` key-count line per model, verified by `test -f`. (2) The corpus records the solver's *belief*, which is demonstrably unreliable on the failers — but that unreliability is itself the finding (it confirms the failures are self-consistent, not self-contradictory; wall-confirming knowledge). (3) Substantial overlap with the existing Section-5 triage and the archived h0017 debug run `19283fb82dbd4ffd`, so the marginal yield is bounded.

### M2 — Enforced abstention rail (Track Z / `h00Z`), built at last — the net-protecting safety rail

- **Shape.** A mechanical abstention precondition. Two viable placements, captain's choice: a NEW `## Stage:` between Validation and Finalization (pre-commit triage gate), or a `gate-change` on the existing Finalization stage. Single `## Stage:` touched (G1 clean).
- **Mechanism.** For each load-bearing claim the edit rests on, a fixed three-clause tree: (1) does an explicit task-instruction sentence name the deciding quantity? (2) does an *existing* `schema.yml` contract name it? (3) does a raw `SELECT FROM {{ source(...) }}` conservation/coverage probe — **count + key-level anti-join, read from the IMMUTABLE source, never a re-derived CTE** (the E0/h0032 caveat) — DECIDE it? If all three are NO, the gate **mechanically emits ABSTAIN and reverts every edit made only to satisfy that claim**, leaving those files byte-identical to task start. `triage.json` records the decision + failing clause as artifact proof the gate fired.
- **Why it matters / what it fixes.** h0031 died with `abstained_claims: []` on every load-bearing oracle-only claim because abstention was *permitted, not enforced* — the arbitrator promoted a tier-3 "defensible local guess" instead of abstaining (program §5 Track Z, lines 213–222; h0031 conclude). M2 is the **enforcement primitive h0031 explicitly named as the missing piece, not a third route.** It is single-path (no candidate generation), so it sidesteps the G9-exhausted arbitration family entirely.
- **Expected flips.** **{0}** by construction (it never asserts an answer; it withholds a change). On the 16 oracle-blocked failures it correctly abstains → byte-identical to baseline → no-op. The captain-carve-out abstention set (asana004/005/005-hard, ana-eng004, f1002, ana-eng007/-medium) is already at 0, so abstaining costs nothing.
- **Honest caveats.** (1) **G7-high**: an "enforced REVERT" expressed as README prose sits at the *same model-discretionary altitude* that produced h0031's `abstained_claims: []` — there is no mechanical harness compelling the revert; this is the central unproven claim and the only real experimental question. (2) **Inverted false-green risk (G10-live)**: the danger is a *wrong revert* — if clause-3's anti-join reads a solver-rebuilt intermediate (not raw source) it re-correlates (the h0030 hazard in reverse) and could revert a *correct* edit, regressing a passer. This is what smoke must falsify, with ≥2 perturbable canaries per construct family. (3) Standalone against the current minimal baseline (which does not bleed), its protective value is unobservable — the harm it guards came from the rejected flip-seeking levers (h0012, h0017), not from @baseline. **M2's real home is bolted onto a future flip-seeking generative lever, where it would guard a live regression surface.** Build and bank the spec now; the captain decides whether to also run it standalone as a bleed-freeness check.

### M3 — Observe-only triage ledger (de-risk M2 before it is trusted to revert)

- **Shape.** The M2 three-clause trigger in OBSERVE-ONLY mode — writes `triage.json {claim, clause_results, would_abstain}` on all 48, **never reverts or alters anything**; build proceeds exactly as baseline. Guaranteed zero score impact.
- **Deliverable.** The `would_abstain` distribution across the 48 known verdicts: a passer flagged `would_abstain` is a *predicted M2 false-revert* (the regression surface M2 would expose); the survivor airbnb009 must NOT be flagged (proof M2 would not suppress the one real fix). This is the green-light precondition before M2 is ever allowed to revert in a real run.
- **Honest caveat.** The trigger is the same tier-3 raw-source/coverage mechanism Round 1 proved mis-discriminates: by h0030 the probe comes back empty on genuinely-oracle-only intercom (false-negative); by h0036 the coverage probe fires on ana-eng007 whose coverage is fixable but value is oracle-only. So the ledger is a *map of where the trigger mis-fires*, which is useful for sharpening M2, but it does not certify the trigger as a clean oracle-only detector. It is a low-cost instrument, not a discovery.

**Net-protection design notes worth banking even if never run standalone:** the *scope-gated revert-on-bleed* idea (fire only on the project's OWN referenced-but-absent / instruction-unauthorized diff signatures — the validated h0035 scope-gate that held f1001 at 1.0) is the subtractive inverse of the dead deliverable-set clause and is the correct guard to pair with any future generative lever. Record it; do not spend a smoke run on it absent a live lever to protect.

---

## 5. Honest portfolio math

| E-entry | Type | Realistic flips | Best-case flips | Gate verdict |
|---|---|---:|---:|---|
| **Bank airbnb009 (h0019)** | banking step (not an experiment) | **+1** | **+1** | already smoke-GO + held at full |
| E-RMS (Reference-Mining Stage) | run-worthy experiment | 0 | 0–1* | METHOD-ONLY (G7 WARN) |
| E-PRMB (Plan Reviewer Method B) | run-worthy experiment | 0 | 0** | METHOD-ONLY (G7 HIGH) |
| M1 (observe-only debug lens) | method / instrument | 0 | 0 | METHOD-ONLY (G7 HIGH) |
| M2 (enforced abstention rail) | net-protection rail | 0 | 0 | METHOD-ONLY (G7 HIGH, G10 live) |
| M3 (observe-only triage ledger) | method / instrument | 0 | 0 | METHOD-ONLY (G7 low) |

\* E-RMS best case is 0–1 only on a not-yet-found target meeting all four survivor conditions; on the known 17 it is 0 (the analog is the wrong dimension — convention, not the deciding DROP/value).
\*\* E-PRMB best case is 0 on the known 17 (the code-contradicts-contract class is empty among them); any non-zero would be a regression *prevented*, not a known failure flipped.

**Realistic Round-2 landing: 32/48 (0.6667)** — the banked airbnb009, plus 0 experiment flips. **Best plausible case: 32/48** as well, unless a target-hunt (out-of-scope-adjacent, see Open Questions) surfaces a genuinely-new survivor-shaped task — which Round 1 concluded the known 17 do not offer.

**Is 75% (36/48) reachable? Plainly: no, not inside this box.** It requires +4 over the banked 32, and there are **0 remaining failures with a visible local arbitrator that yields a flip** (Section 6 rollup). The four "land/reach-but-lose" tasks (ana-eng007/-medium coverage→value; intercom001/003 re-correlation) and the eight oracle-only-by-triage tasks all need the deciding fact that lives only in `solution/` + hidden tests = changing what ships = out of scope. **Round 2's honest deliverable is 32/48 + a banked method portfolio (the first live Method-B run, the 48-task debug-lens corpus, the enforced-abstention spec), not a pass-rate jump.**

---

## 6. What Round 2 will NOT re-file, and why (the dead-family map)

Do not re-spend a run on any of these. Each died in Round 1 with a cited run; relabeling does not revive it.

| # | Dead family | Status | Targets | Why dead (evidence) |
|---|---|---|---|---|
| D1 | Grain-construct (prose / worked-example / Output-Contract spine) | EXHAUSTED 3-for-0 | intercom001/002/003 (`Got 7`), asana004/005/005-hard (`Got 3`) | restructuring prose INERT at gpt-5.5/xhigh; h0017 cleared inertness but built backwards (named the child as grain driver). `_archive/{h0010,h0016,h0017}` |
| D2 | Grain-reconcile (raw-source COUNT(DISTINCT) + anti-join) | EXHAUSTED + ORACLE-BLOCKED | intercom001/002/003 | the "independent" probe re-correlated through the shared `_fivetran_active` filter → anti-join empty (textbook correlated-error false-green). Canonical population is oracle-only. `_archive/h0030` |
| D3 | Cast / type-contract | EXHAUSTED 3-for-0 | asana002 (`Got 2`) | mis-classified — asana002 is a structural package-migration, no `::type` surface; h0033 was green-but-inert (flip was solver-native, not lever-attributable). `_archive/{h0033,h0020,h0009}` |
| D4 | Candidate-generation / arbitration (selector + dual-output-contract) | EXHAUSTED (meta-pattern) | f1011, grain cluster | generation-independence + external arbitration are TABLE STAKES; h0026 all candidates shared the wrong reading (`ABDE` vs `ADE`); h0031 cleared every independence bar and STILL committed byte-identical `ABDE`. Siblings h0024/h0025/h0027/h0028 inherit (G9-exhausted). `_archive/{h0026,h0031}` |
| D5 | Incomplete-deliverable / missing-models | DEAD 5-for-0 (highest-bleed) | quickbooks001 (`Got 1`×6) | green-via-package-namespace masks the trigger (project builds GREEN `PASS=172,ERROR=0` without the 3 staging models — no red trigger to fire on); h0023 bled f1001 6/6→2/6. `_archive/{h0035,h0023,h0013,h0015}` |
| D6 | Width / missing-columns | ORACLE-ONLY (EXHAUSTED) | ana-eng004, f1002, ana-eng006 | declared column sets LIE or are absent; true set needs DROPs that live only in the hidden solution (f1002 schema.yml over-declares 6 vs 3; ana-eng004 target undeclared). h0029 retired without a run. `_archive/{h0029,h0011,h0023}` |
| D7 | Coverage / value-divergence | ORACLE-BLOCKED (sharpest negative) | ana-eng007/-medium, f1006 | h0012 generative recompute REJECTED NET −4 (pushed 4 passers off a simple-correct `sum→max`); **h0036 fired correctly, removed the hidden filter, recovered coverage — and STILL LOST `Got 5 → Got 10`** because the recovered rows were oracle-only-valued. A coverage fix can MASK an oracle-only value bug; fixing coverage doubles distance. `_archive/{h0012,h0036}` |
| D8 | Analytical-answer (per-claim / decision-table) | ORACLE-ONLY (retired w/o run) | f1011 (`check_option_b Got 1`) | local evidence PROVEN misleading (truth `ADE`; the wrong letter B is a misleading-but-locally-TRUE signal; D has no local column). h0014/h0022 retired REJECTED. `_archive/{h0014,h0022}` |
| D9 | New-stage / arbitration-architecture refinements | mostly INERT-or-correlated; one method-PASS (E0/h0032) | — | exposed the VARIANCE WALL (h0034, paired CI [−4,+4]) and the MULTI-MODEL-TARGET TRAP (G11: airbnb007 scored by 2 models). `_archive/h0034` |

**Killed Round-2 candidates (do not re-file under a new name):** the convergence-to-fixpoint STOP gate (D7, would go inert or over-revert the f1 standings family); the two-pass ref-graph completeness gate (D5, bit-identical to h0035's green-via-namespace dead end); the Finalization differential-vs-prior-build gate (D7 + the dead Finalization-invariant family h0004/h0006/h0007/h0008 + inherits h0030 re-correlation); the Finalization conservation gate (misreads its own evidence — the h0034 regressions were the solver's OWN edits, inside the diff, so the gate would not fire); the staged-escalation Implementation (composes D2 + D5 + D7, 0 flips on every named target).

---

## 7. Measurement + gate discipline

- **trials:1 always.** Captain standing decision AND pinned by the freeze-repo concurrency race ("git cannot lock ref HEAD" when `concurrency.trials>1`). Do not propose multi-trial.
- **Judge by committed-artifact proof + bleed-free canaries, NOT multi-trial CI.** A green flip is not lever attribution (h0033 green-but-inert): require the prescribed token in the committed `apply_patch`. The VARIANCE WALL ([−4,+4] paired CI, 10k bootstrap, h0034 `1880d6497bdd6303`) makes the do-no-harm tripwire structurally unsatisfiable for a +1 lever at trials:1 — which is exactly why airbnb009's real +1 was masked.
- **Distance-to-pass (`Got N`) is the LEADING indicator; flip is LAGGING.** Read `Got N` from `verifier/test-stdout.txt`. **Unchanged `Got N` ⇒ INERT** (cheapest check, before any transcript). For an observe-only lens (M1/M3), unchanged `Got N` is the *success* condition (contamination tripwire). Watch for the 2026-06-08 `Got N → Got 2N` pattern — a landed coverage fix unmasking an oracle-only value bug (E6/h0036) — as the canary for the value wall.
- **Perturbable canaries.** A generative lever (E-RMS, M2) MUST carry ≥2 *perturbable* canaries per shared-construct family (passers it will actually fire on; inert stable passers are blind — h0009 −3, h0012 −4). If none exists for a family, state the regression surface is BLIND; do not paper over.
- **Smoke is the recurring blind spot.** h0017's 9-task smoke missed all 6 full-run movers. Every generative-stage smoke must sample beyond targets + one-per-family, presented in the REQUIRED boxed table (Task / Baseline / Should-pass / Role with ❌✅🎯 glyphs + net + ETA ≈ N×9 min).
- **E0-style instrument gate where relevant.** Before any "independent second-path" check (M2 clause-3, M3 trigger) is trusted, it must clear the E0/h0032 two-sided discrimination on a controlled fixture (FIRE-on-injected, SILENT-on-known-good), and — per the h0030 refinement — **the fixture MUST share the target's upstream filter**, or it validates in a regime the real failure does not inhabit. The reconcile is sound ONLY reading the immutable raw `source()`, paired with a key-level anti-join (bare `COUNT(*)` is blind to drop-N-add-N).
- **Analysis math.** `rk runs diff` CRASHES on ade-bench run-dirs (`query_id null → TypeError`); compute the paired delta from `per_trial_outcomes.json`, slug-paired, 10k bootstrap.
- **Loop-side instrumentation (optional, zero solver risk).** A Smoke-Lens auto-probe (inert-detector + verify-the-artifact + credit-time-G11, the drafted-but-unbuilt `smoke-review-guideline.md` items, propose-guideline lines 334–354) reads only operator-side run-dir artifacts and formalizes existing manual smoke practice. It touches no solver README and ships nothing — strongest scope compliance — but it creates no flips; build only if the operator wants a repeatable smoke artifact.

---

## 8. Open questions for the captain (plain words first, technical underneath)

1. **Do we run the two experiments at all, or just bank the method?**
   *Plain:* The gatekeeper says neither new experiment is likely to flip anything; both mainly produce evidence. Do we spend two smoke runs to *prove* the Plan-Review and Reference-Mining stages behave as predicted, or do we skip straight to banking the observe-only lens and the abstention spec?
   *Technical:* E-RMS and E-PRMB are the only genuinely-new solver-graph shapes left (the captain asked for more structural experiments). Running them returns committed-artifact evidence (Method B's first live `plan_review.json`; per-task analog-existence) that the observe-only lens approximates more cheaply. The trade is run cost (~N×9 min smoke each) vs. live-shape confidence.

2. **Where does the enforced abstention rail live, and do we run it standalone?**
   *Plain:* The safety rail (Track Z) only *visibly* helps when paired with a risky lever — standalone against today's careful baseline it does nothing. Do we build and bank its spec now and bolt it onto a future lever, or also run it alone just to prove the "enforced revert" actually obeys?
   *Technical:* M2's central unproven claim is whether a README-prose "enforced REVERT" escapes the model-discretionary altitude that produced h0031's `abstained_claims: []`. A standalone smoke can only test bleed-freeness (no firing target among the 16); it cannot test protection. Captain's call on whether that is worth a run.

3. **Is the target-hunt formally closed, or do we leave one slot for it?**
   *Plain:* Round 1 concluded the 17 known failures contain no second flippable target. Finding a *new* one would require looking outside the known set — which brushes against the "don't change what ships" line. Do we declare the flip portfolio closed at airbnb009, or keep a narrow, in-scope hunt open?
   *Technical:* The survivor family needs all four conditions (value/shape-to-match, locally determinable, single-model, concrete sibling to copy). The brief says such a target was "never hunted" outside the 17. Any hunt must stay strictly in-scope (re-process /app material only) and is expected to come up empty — but it is the only path to a 33rd point inside the box.

4. **Do we accept 32/48 + a banked method portfolio as the Round-2 success definition?**
   *Plain:* Should we write the Round-2 verdict now as "banked the one real fix, mapped the wall, built the instruments — 75% is out of reach inside the rules", and treat that as a win?
   *Technical:* This is the knowledge-gains-are-small-successes doctrine applied at the program level. The honest deliverables are: 32/48; the first live Method-B run; the 48-task debug-lens corpus; the enforced-abstention spec; a complete dead-family map. None of those is a pass-rate jump, and all of them are real.

---

## Cross-refs

- **Round-1 plan:** `_proposal/oracle-problem-systematic-program.md` (Track Z §5 lines 213–222; LOW-control triage lines 116–123; arbitration-as-decision-rule line 97; abstention-not-enforced line 60).
- **Retrospectives:** `_proposal/retrospective-2026-06-07.md` (h0034 regressions = solver's own edits, lines 35–37; variance wall); `_proposal/retrospective-2026-06-08.md` (§5 airbnb009 deferred-bankable; E5 inert; E6 coverage-masks-oracle-value; @baseline 31/48).
- **Doctrine:** `_artifacts/verification-without-oracle.md` (independent-vs-correlated test, double-entry/reconciliation import); `_artifacts/bug-type-taxonomy.md` (bug-type → target map); `_artifacts/WORKFLOW-REFINE.md` (observe-only lens un-built, lines 199–201; Method B safe / Method A fails, lines 260–274; h0017 wrong-model statements, lines 127, 191–193); `_artifacts/arbitration-without-oracle.md`.
- **Gates:** `_gatekeeper/propose-review-guideline.md` (G1–G11; smoke-review "Future scope" lines 334–354).
- **Loop:** `hypotheses/README.md` (meta-loop stages 7–55; propose smoke-table format).
- **Survivor:** `hypotheses/h0019-implementation-let-categories-emerge-not-cross-join.md` (status ACTIVE; run `d8bd75a0189bda65`).
- **Key archive entities + runs:** h0017 `_archive/h0017` (smoke `a498329abd068ab5`, full `19283fb82dbd4ffd`); h0023 `_archive/h0023` (run `e018ce3babecc3dc`); h0031 `_archive/h0031` (run `0de9870ae2220bca`); h0032 `_artifacts/h0032-e0-harness/{harness.py,result_2x2.json}`; h0026 `_archive/h0026` (run `a01f97caf6d6462e`); h0030 `_archive/h0030`; h0033 `_archive/h0033` (run `33cf2891e1f5e6b6`); h0035 `_archive/h0035` (run `efa1b651f71941b4`); h0012 `_archive/h0012` (run `3d8294de42b726e1`); h0036 `_archive/h0036` (run `c51545c270b51f6d`); h0034 combined-full `1880d6497bdd6303`.
- **Baseline:** `runs/ade-bench-baseline/622bdedac572b479` (31/48 = 0.6458).
- **MEMORY notes:** baseline re-bound post-DuckDB-fix; AUTO_* equality tests hidden; solver blind to oracle; single-trial judge-by-artifact; propose-gatekeeper; propose-gate smoke table format; verification-without-oracle; knowledge-gains-are-small-successes; WORKFLOW-REFINE structural-learnings ledger.
