# Flipping More Tasks Under the Blind-to-Oracle Wall: A Genuine-Independent-Redundancy Program

**TL;DR.** Our solver builds a dbt artifact, self-checks it clean, and ships it wrong: it never sees the hidden grading oracle, and all 17 baseline failures are these "self-anchored false-greens." Every prior lever stalled because it manufactured a *second opinion* that secretly shared the first one's mistake — the correlated-error wall (h0012 regressed NET −4 by damaging passers; h0031 reproduced baseline's exact wrong answers). The reframe: stop generating smarter judges and instead recompute the truth by a path that *cannot* share the error — a raw-source key-count, a complete-calendar relation, the project's own passing sibling, the `information_schema` contract, the package ref-graph — aimed **only** at tasks whose failure has a visible local arbitrator. The method is a five-step pipeline gated by a mandatory two-sided instrument check (E0): a check must demonstrably fire on an injected error and stay silent on a known-good before we trust it on a real task. The honest portfolio is **+3 to +6 flips against a +5 target**, and it reaches 75% *only if* the intercom grain reconcile breaks an inertness wall that has held three times — that is the real bet, not a comfortable buffer. We are explicitly **NOT** building another candidate-generator, arbitration agent, or third route (that family is exhausted), and we are NOT chasing the oracle-only tasks (we route them to an *enforced* abstention rail whose only job is to keep them at net-zero, not to flip them).

---

## Decisions locked (captain, 2026-06-07)

The four debate questions in §7 are resolved:

1. **E1 (intercom grain fix) — run first, capped.** It leads the program as the make-or-break bet, but on a tight leash: one smoke; if distance-to-pass doesn't move, we do NOT iterate — we move on. If no real perturbable canary exists, we proceed on E0's synthetic injected-error fixtures (the canary situation is reported before the full run).
2. **If we land at +3 (34/48) — run and reassess.** No speculative sixth-task hunt up front; we look for more only after E1/E2/E3 results are in.
3. **Abstention — enforce on the oracle-only tail EXCEPT the two Mini-proven-solvable tasks (f1006, f1011), which stay free to attempt.** They are already failing, so a wrong guess costs nothing, and a weaker model already flipped them — a free upside shot. Everything else oracle-only is hard-forced to ABSTAIN. (Caveat: h0031 showed f1011's local evidence is misleading, so any flip there is luck, not method — it is not portfolio-counted.)
4. **Benchmark is fixed — the five out-of-reach tasks (ana-eng004, f1002, f1006, asana004, f1011) are out of scope** for this pass-rate push. (f1006/f1011 still get a free attempt per #3, but are not portfolio-counted.)
5. **(2026-06-07, post-E1) Accept 34/48 as the landing; execute the ENTIRE plan, then retrospect — do NOT chase the 2-task gap mid-flight.** E1's NO-GO fixes the realistic ceiling at +3 → 34/48 (0.7083), 2 short of 75%. Decision: do **not** open target-sourcing in parallel. Run the full filed portfolio — E2 (h0019, full-run confirm) / E3 (h0018, airbnb007) / E4 (asana002 cast) / E5 (h0015-successor, measured) + Track Z as the safety rail — to completion as filed. **Then run an end-of-program RETROSPECTIVE** that figures out how to close the final 2-task gap to 75%: re-triage the 9 LOW/Track-Z tasks by the E1 **value/shape-to-match vs population-canonical tractability rule**, promote E5 to *counted* if it flips bleed-safe, and source a 6th/7th visible-arbitrator target. The banked **method** (the E0 instrument-gate, the tractability rule, the dead-family map) is treated as a first-class deliverable alongside the pass-rate number — small successes compounding toward the goal, not just flips.

   > **STATUS 2026-06-08 — the LOW/Track-Z target hunt is EXHAUSTED.** The re-triage produced exactly
   > ONE new visible-arbitrator candidate (`ana-eng007` coverage, carried by **h0036**); the other
   > eight LOW/Track-Z tasks were confirmed informationally blocked (four queued hypotheses
   > h0021/h0029/h0014/h0022 retired as doomed-by-re-triage). **h0036 REJECTED at smoke**
   > (`runs/.../c51545c270b51f6d`): the coverage rule LANDED — the solver found and removed a hidden
   > `WHERE supplier_ids NOT LIKE '%;%'` filter in `stg_products.sql`, `dim_products` grew 40→45, and
   > the RAW-SOURCE coverage anti-join went EMPTY — but the recovered rows need oracle-only VALUES, so
   > distance got WORSE (`Got 5 → Got 10`) and two downstream OBT models broke; neither target flipped.
   > **New named pattern: a coverage drop can MASK an oracle-only value bug — fixing coverage surfaces
   > the masked rows as wrong-valued and the distance doubles (`Got N → Got 2N`).** ana-eng007 /
   > ana-eng007-medium are therefore ORACLE-BLOCKED on the value half. **No new flip target found; the
   > hunt is exhausted, @baseline remains 31/48.** The only remaining bankable flip is **airbnb009**
   > (E2 anti-cross-join `Got 1`); surfacing that as a captain strategy call. Doctrine corrected in
   > `_artifacts/bug-type-taxonomy.md` + `_artifacts/verification-without-oracle.md`.

---

## 1. The problem we face

The solver (`codex/gpt-5.5@xhigh`) receives a local dbt workspace but **no `tests/` and no `solution__*` seeds**. It can build a plausible artifact, validate it against its own framing, and stop — while the hidden oracle re-runs `AUTO_*_equality` / `check_*` tests against `solution__*` seeds and finds the answer wrong. Every one of the 17 baseline failures has this exact shape: **the solver self-checks clean and is wrong anyway.**

This is the textbook *oracle problem* — verifying correctness with no trusted reference (Barr, Harman, McMinn, Shahbaz & Yoo 2015, *The Oracle Problem in Software Testing*, IEEE TSE 41(5):507–525). Internally we call each instance a **self-anchored false-green** (`_artifacts/verification-without-oracle.md`).

- **@baseline** = 31/48 (0.6458), run `runs/ade-bench-baseline/622bdedac572b479`.
- **Goal** = 36/48 (0.75) → **+5 net flips**.
- **The 17 failures** sort into seven bug types (`_artifacts/bug-type-taxonomy.md`): entity-grain, date-spine, width, value-divergence, tolerance-band, type/contract, incomplete-deliverable, analytical-guess.

A second oracle (gpt-5.4-mini, 28/48, run `c5acd9b29faeb087`) flips **asana002, f1006, f1011** — hard proof those three are *solvable* (a workflow/correctness gap, not benchmark-impossible), even though a weaker model gets them.

---

## 2. Why prior attempts stalled

Two rejections are the spine of this reframe. They prove that *generating* a second opinion is exhausted — not that independent redundancy fails.

### 2.1 h0012 — generative reconcile, REJECTED at full, NET −4
Run `3d8294de42b726e1` (0.5625 vs 0.6458). The "independent" recompute **collapsed into correlated error and damaged passers**: it pushed four `f1 constructor_points` models off a simple-correct `sum→max` path onto a "structurally different" wrong path, then false-green-validated against a CTE that *shared the model's own logic*. Two gains (airbnb007, asana002) could not offset six regressions. The single unperturbed canary (f1001) was blind to the −4 because the lever never fired on it. (`_artifacts/bug-type-taxonomy.md` line 73; `_archive/h0012`.) **Lesson, encoded as gatekeeper G10 + the G8 perturbable-canary rule:** a self-correcting lever that *always fires* and *replaces* will realize correlated error as **regression**.

### 2.2 h0031 — dual-output-contract arbitration, NO-GO, 0 flips / 0 distance moved
This is the decisive negative. Route B *genuinely diverged* (drove from `conversation_history`, swapped to raw `northwind.products`, carried `attempt_to_defeat_route_a`); the arbitrator used independent raw conservation/coverage probes — it cleared the generation-independence wall (G9/AC-1). **And it still reproduced baseline's EXACT wrong answers** (f1011 byte-identical `ABDE`), for two reasons:
1. **It targeted oracle-only tasks.** ana-eng004 / intercom001 / f1011 are exactly the ones the doctrine flags **low-control** — the deciding fact lives only in `solution/` or hidden tests. No amount of generation manufactures redundancy a task does not contain.
2. **Two contracts in one solver session over shared priors is a correlated substrate.** A second contract inherits the first path's blind spot.

On the load-bearing oracle-only claim, h0031 logged `abstained_claims: []` — abstention was *permitted but not enforced* (AC-4 violated), so the arbitrator picked a tier-3 default *and was confidently wrong*. (`_archive/h0031`.)

### 2.3 The reframe
We stalled because **(a) we aimed at oracle-only targets** and **(b) we used correlated (in-session) substrates.** Generation-independence is **table stakes, not a contribution.** The lever must be **genuine independent redundancy — a recompute from RAW SOURCE or a structural relation the answer MUST obey — aimed exclusively at VISIBLE-ARBITRATOR tasks.** The loop's only real catch (f1007-hard) was exactly this: an independent number recomputed from raw source. The only structural flip (airbnb007 under h0017's contract leg) was a differential against the project's *own* pre-existing rolling-window model. Both pass the sharp test below. Everything that re-read the solver's logic (h0006/7/8, h0012, h0026, h0031) failed it.

---

## 3. The systematic method

A repeatable five-step pipeline. The hinge is step (c): the independence proof and the correlated-error guard.

### THE ONE LAW (lead with it)
`_artifacts/verification-without-oracle.md`: **the only thing that beats no-oracle is independent redundancy** — recompute the truth by a path that does NOT share the first path's error, then require agreement. The universal failure is its mirror, **correlated / common-mode error**: the "second path" secretly shares the first's mistake, both wrong the same way, the check passes vacuously.

This is not folklore. It is the empirically documented killer of:
- **N-version programming** — Knight & Leveson 1986 (IEEE TSE SE-12(1):96–109): 27 independently-built versions failed *together* on hard inputs more than independence predicts.
- **Weak supervision with unmodeled latent correlation** — Ratner, De Sa, Wu, Selsam & Ré 2016 (*Data Programming*, NeurIPS / arXiv:1605.07723); Ratner et al. 2020 (*Snorkel*, VLDBJ 29:709–730).
- **Unlabeled accuracy estimation** — Jaffe, Nadler & Kluger 2015 (AISTATS, PMLR v38:407–415).
- **Multi-agent debate among homogeneous agents** — Wynn, Satija & Hadfield 2025 (*Talk Isn't Always Cheap*, arXiv:2509.05396): same-base-model agents drift to a wrong consensus via sycophancy/conformity.

> **THE SHARP TEST** (`_artifacts/arbitration-without-oracle.md`): Does the check read the solver's own plan/output or re-run its own logic → **correlated → it will false-green → reject.** Does it recompute the truth from the **raw source by a different route**, or check a relation the answer must obey regardless of method → **independent → it can catch.**

### (a) TRIAGE by arbitrability — see §4.

### (b) MATCH method → bug-type (the verified toolbox)
Each method recomputes by a path the solver's SQL did not consume the same way: partial/derived oracles (Barr 2015); metamorphic relations (Chen et al. 2018, *Metamorphic Testing: A Review*, ACM CSUR 51(1) art. 4); property-based (Claessen & Hughes 2000, *QuickCheck*, ICFP); differential (McKeeman 1998, *Differential Testing for Software*, DTJ 10(1):100–107); constraint/denial-constraint as oracle (Chu, Ilyas & Papotti 2013, PVLDB 6(13)); grounded reference / retrieval (Lewis et al. 2020, *RAG*, NeurIPS); execution-feedback verification (Ni et al. 2023, *LEVER*, ICML / arXiv:2302.08468); invariant detection (Ernst et al. 2007, *Daikon*, SciCompProg 69).

### (c) CONSTRUCT a genuinely independent path + STATE the proof and the guard
Every second-path hypothesis MUST answer the 7 required questions (`_artifacts/verification-without-oracle.md` §6); the load-bearing ones are **#3 (what error is the second path independent from)** and **#4 (what higher-authority evidence arbitrates a disagreement)**. Two mandatory attachments:

- **INDEPENDENCE PROOF (the sharp test, operationalized = E0).** State the raw source / structural relation the path reads. Then *prove* the path is live and discriminating with a two-sided instrument check: it must **FIRE on an injected/known error** AND stay **SILENT on a known-good**. A path that cannot demonstrably fire is inert (the h0010/h0016 prose signature); a path that fires on a known-good is correlated (the h0008/h0012 signature).
- **CORRELATED-ERROR GUARD (the h0012 lesson = gatekeeper G10 + G8).** Three mandatory clauses for any generative/self-correcting lever:
  1. **Figure-CHANGE-gated** — fire *only* when the independent relation already disagrees (a shortfall/mismatch), never always-on (G10-a).
  2. **CHECK-don't-replace, never replace a simple-correct path** — a disagreement triggers *investigation*, not an automatic rewrite; the h0012 `sum→max` regression is precisely the forbidden move (G10-c).
  3. **≥2 PERTURBABLE canaries per family** — passers the lever will *actually fire on*. One unperturbed canary (f1001) was blind to h0012's −4 (G8). **Caveat surfaced in triage (see §4 / §6):** a perturbable canary must be a passer the gated relation *can* fire on; if a family has no such passer in the benchmark, the canary requirement is unsatisfiable and that family's regression risk is **unmeasurable at smoke** — a caveat we must state, not paper over.

### (d) ARBITRATE / ABSTAIN with a machine-readable artifact
Arbitration is a *decision rule over evidence*, not a smarter agent. It emits exactly one of `SELECT_A / SELECT_B / REJECT_BOTH / ABSTAIN` to an `arbitration.json` so we can audit that arbitration *actually happened*. **ABSTAIN must be MECHANIZED and ENFORCED, not "MUST abstain" prose** — h0031 died because abstention was optional and produced `abstained_claims: []`. The trigger is a concrete checkable precondition (see Track Z, §5). Evidence authority is the 7-tier hierarchy: instruction > declared contract > raw source/conservation > local tests > sibling patterns > package artifacts > transcript (never).

### (e) MEASURE distance-to-pass as the LEADING indicator, flip as the LAGGING one
`Got N` is the oracle's row/option distance from correct (intercom `Got 7`, asana `Got 3`, airbnb009 `Got 1`, f1011 `check_option_b Got 1`). **Distance-shrink on a target is the leading indicator** that the independent path is reaching the right construction *before* a full flip; a flip (FAIL→PASS) is the lagging confirmation. h0016 *reached* `Got 7→5` on intercom001 without passing — a partial signal the inert prose levers (h0010, `Got 7→7`) never produced. We track distance every smoke (§6).

---

## 4. Arbitrability triage of the 17 failures

Sorted by whether a **clean, self-contained independent arbitrator exists in the LOCAL workspace** (grounded in `runs/.../verifier/test-stdout.txt` + `_artifacts/bug-type-taxonomy.md`).

| Control | Tasks | The named independent check | Note |
|---|---|---|---|
| **HIGH** | intercom001/002/003 (`Got 7`) | raw-parent `output COUNT(*) == COUNT(DISTINCT parent_key)` from raw seed | one shared cause; bimodal {0,3} (see §5/E1) |
| **HIGH** | airbnb009 (`Got 1`) | continuous-day relation; **but residual is the cross-join, not the spine** (h0019) | spine already half-fixed unprompted |
| **HIGH** | airbnb007 (`Got 4`) | differential vs project's OWN passing sibling `mom_agg_reviews.sql` | the loop's one structural flip |
| **HIGH** | asana002 (`Got 2`) | `information_schema` dtype vs declared contract; `::timestamp` cast | mini-flip-confirmed solvable |
| **MED** | quickbooks001 (`Got 1`×6) | ref-graph / installed `fivetran/quickbooks` package; models named by `_existence` tests | highest convention-bleed risk; {0,1} |
| **MED→Z** | ana-eng006 `fact_inventory` (`Got 204`) | `MM/DD/YYYY→DATE` cast leg recoverable; but cell is "width ×2 **+** value" | partial fix won't flip the cell |
| **LOW (Track Z)** | **asana005, asana005-hard** (`Got 3`) | same `AUTO_int_asana__project_user_agg` test — **the `int_` oracle-only convention** | taxonomy line 71: "intercom/airbnb009 are the cleaner test"; **NOT flip buffer** |
| **LOW (Track Z)** | asana004 (`Got 3`) | oracle-only `int_` convention | "partly underdetermined" |
| **LOW (Track Z)** | ana-eng004, f1002 (width) | NO truthful local declaration (f1002 schema.yml over-declares 6 vs true 3) | oracle-only / misleading |
| **LOW (Track Z)** | ana-eng007, ana-eng007-medium (`Got 5`) | subtle dedup tie-break | weak local signal |
| **LOW (Track Z)** | f1006 (`Got 2`) | not locally derivable | mini-flips but no local arbitrator |
| **LOW (Track Z)** | f1011 (`check_option_b Got 1`) | local evidence proven MISLEADING by h0031 | the `ABDE` confidently-wrong trap |

**Rule:** HIGH + the best MED (quickbooks001) form the flip portfolio. LOW tasks are **informationally blocked, not selection-blocked** — they go to the abstention rail (Track Z). Adding more generation/arbitration there is exhausted (h0026 + h0031 meta-pattern). **Note the correction the critique forced:** asana005/005-hard sit on the *same oracle-only `int_` convention* the program flags LOW, so they are **NOT** E1 flip buffer; they are Track Z.

---

## 5. The experiment program

Sequenced HIGH-control first. **E0 gates everything on a per-check basis** (each E0 check gates only its own downstream experiment). The regression-guard is baked into every generative entry. **Track Z** runs the abstention rail in parallel as a safety rail.

---

### E0 — Instrument-validation control (MANDATORY GATE)
- **What we test:** does each candidate independent check **FIRE on an injected error AND stay SILENT on a known-good** — i.e. is it discriminating and not self-anchored — *before* we trust it on real tasks?
- **The independent path & method:** take 2–3 KNOWN-GOOD passing models; inject a known error into a copy (drop a parent key → grain shortfall; cast a column to the wrong dtype; remove a calendar day). Run the candidate dbt checks (raw-parent `COUNT(DISTINCT key)` reconcile, `information_schema` dtype assertion, complete-calendar left-join) against both.
- **What evidence we want:** per check, a 2×2: fires-on-injected = TRUE, fires-on-known-good = FALSE.
- **Pass-kill:** PASS = all candidate checks are two-sided discriminating. **KILL (per check):** silent on injected error → inert (do not deploy); fires on known-good → correlated/over-broad (reject). A check that fails either side does not advance to its E-experiment, **and only that experiment is blocked** — others proceed.
- **Sequence rationale:** the literal operationalization of the sharp test and the antidote to the entire false-green family (h0008's "independent" reconcile was never instrument-validated; it self-anchored). No real-task experiment runs a check E0 hasn't cleared.
- **Future hypothesis stub:** `h00E0` instrument-control harness — prerequisite for h0030/h0029/h0021. Expected direct contribution to +5: **0** (it makes every flip below trustworthy).

---

### E1 — Grain-entity raw-parent row-count reconcile *(highest control, biggest cluster — and the program's make-or-break bet)*

> **STATUS 2026-06-07: RESOLVED — NO-GO / REJECTED (h0030).** The reconcile fired and *reached the committed SQL* (count + anti-join present) but **re-correlated through the shared `_fivetran_active` filter** — parent and child collapse to the same 5 keys, so the anti-join came back empty and the probe false-greened; the solver saw the 2-vs-5 split and took the legitimate-scope escape. The deciding fact ("which population is canonical") is oracle-only. **4th grain rejection (h0010/h0016/h0017/h0030); family exhausted/oracle-blocked.** Zero canary regression (safe-but-inert). New transferable lesson recorded: *an independent raw-source probe can still re-correlate if it inherits the model's upstream filter/population* (`_artifacts/verification-without-oracle.md`). **The realistic portfolio ceiling is now the actual ceiling: +3 → 34/48.**
- **What we test:** does a raw-parent independent row-count reconcile drive the solver to the correct entity spine and shrink `Got 7` toward 0 — and, critically, does bolting a *mechanical number* onto a structural rewrite break the **inertness wall** that has held this family 0-for-3?
- **The independent path & method:** build FROM the raw parent spine; assert `output COUNT(*) == COUNT(DISTINCT parent_key)` reading the **raw seed** (`conversation_contact_history_data` / `contact_company_history_data`), NOT the model's CTE. This passes the sharp test cleanly (it is the f1007-hard mechanism). A shortfall is a SIGNAL TO INVESTIGATE (check-don't-replace; figure-gated). G10 guard already encoded in filed h0030.
- **What evidence we want:** distance shrink `Got 7 → 0` on intercom001/002/003 (leading); E0-proven the reconcile fires on an injected dropped-key and is silent on the passing sibling; zero canary regression.
- **Pass-kill:** PASS = ≥1 intercom flips at smoke with distance moving on the others, zero regression. **PRIMARY PREDICTED KILL-PATH = inert REACH (`Got 7→7`, committed SQL unchanged)** — the h0010 signature this family hit three times (h0010 prose, h0016 example, h0017 contract); gatekeeper G7 predicts structural-rewrite prose is inert at gpt-5.5/xhigh ("talks but doesn't do"). The leading indicator to demand at smoke is distance **below 5** (h0016 already reached `Got 7→5`); anything ≥5 is the same wall. Secondary KILL = any canary regresses.
- **Sequence rationale:** highest control, largest cluster, one shared cause, direct heir to the loop's one proven catch. **Honest framing: this is a bimodal {0, 3} bet, not a +3 expectation** — if the mechanical-number-bolted-to-rewrite breaks inertness, ~3 flips; if it stays inert (the family's 3-for-3 prior), 0. Its result tells us whether mechanical raw-source reconciliation transfers to *construction* at all, which unlocks E2/E3.
- **Future hypothesis stub:** **h0030** (filed, `h0030-implementation-grain-rowcount-reconcile-vs-parent.md`). Targets: intercom001/002/003 only. **asana005/005-hard are NOT here — they are Track Z** (`int_` oracle-only convention, taxonomy line 71). Expected contribution: **{0 or 3}**.

---

### E2 — Date-spine: anti-cross-join clause (target the ACTUAL residual, not the spine)
- **What we test:** does the **anti-cross-join clause** close airbnb009's single-row over-production residual — *not* a completeness invariant, because the spine is already there?
- **The independent path & method:** ground truth read from the @baseline cell — the solver **already removed the narrowing filter and drove from the full min/max date spine unprompted** (`expected_days=4508`, `missing_mom_days=0`), yet still failed because it then **cross-joined all three sentiments onto every day**, over-producing rows. The single net-new load-bearing lever is the anti-cross-join clause: let categories emerge through the existing `LEFT JOIN`, never multiply every category against every key. The completeness reconcile (h0030's calendar leg) is likely **inert here** because the spine is already complete. The oracle is a singular `mom_agg_review_date_range` test, `Got 1` (one offending row), consistent with over-production, not a missing day.
- **What evidence we want:** `Got 1 → 0` via the cross-join fix; zero date/grain canary regression. (E0's completeness check is *measured* on airbnb009 but expected silent — confirming the residual is the join shape.)
- **Pass-kill:** PASS = airbnb009 flips. **KILL** = inert or a canary regresses.
- **Sequence rationale:** runs right after E1, reuses the E0 discipline; but its mechanism is **h0019's anti-cross-join, distinct from h0030's missing-spine** — the critique caught us conflating the two. We pick the one mechanism that addresses the *actual* residual.
- **Future hypothesis stub:** **h0019** (filed, `h0019-implementation-let-categories-emerge-not-cross-join.md`). Expected contribution: **+1**.

---

### E3 — Rolling-window differential vs the project's own passing sibling
- **What we test:** does copying a pre-existing *passing* sibling's rolling-window construction (vs nudging precision) flip the tolerance-band failure?
- **The independent path & method:** differential against the project's OWN passing sibling `mom_agg_reviews.sql` (`BETWEEN date−29 AND date`); copy it, changing only the interval (28-day calendar RANGE, never `rows between N preceding`). The sibling's PASS is the independent reference — an artifact the solver didn't author (McKeeman differential).
- **What evidence we want:** `Got 4 → 0`; the sibling diff is genuinely different-route; zero canary regression.
- **Pass-kill:** PASS = airbnb007 flips. **KILL** = inert or regresses.
- **Sequence rationale:** airbnb007 is the **only** structural flip the loop has produced (h0017 contract leg) — empirically the most likely repeatable win, but a *single* task, so it sits after the E1/E2 cluster; its mechanism (differential vs own artifact) validates independently.
- **Future hypothesis stub:** **h0018** (filed, `h0018-contract-rolling-window-calendar-range.md`). Expected contribution: **+1** (repeat of a demonstrated flip).

---

### E4 — Mechanical type-contract cast (surgical, figure-gated, MODEL layer)
- **What we test:** does a mechanically-prescribed in-place cast at the MODEL layer — with an explicit "patch the `.sql`, not the seed" rule — land the asana002-class fix the loop's one prior win demonstrated?
- **The independent path & method:** `information_schema` dtype vs declared contract; mechanical in-place `::timestamp` cast on `asana__task.sql` (NOT the raw seed — h0020 failed because the solver `ALTER`ed the seed, the wrong layer). Precondition-gated to the dtype mismatch; additive/in-place only, no add/drop/rename.
- **What evidence we want:** `Got 2 → 0` on asana002; the cast is applied to the model `.sql` (artifact check, not the seed); zero convention-bleed regression (the h0009 −3 failure mode → ≥2 perturbable non-package canaries held, e.g. f1001/quickbooks003).
- **Pass-kill:** PASS = asana002 flips, zero bleed. **KILL** = solver casts the seed again (h0020 signature) OR convention-bleed regresses a canary.
- **Sequence rationale:** mini-confirmed solvable and the loop's one landed mechanism — but h0020 cast doubt on the layer and h0009 showed convention-bleed risk, so it needs the strict layer-targeting + perturbable-canary discipline established by E0–E3.
- **Future hypothesis stub:** **h0021** (filed, stable dedup ordering) + **h0020-successor** (`::timestamp` cast). **ana-eng006 is NOT counted here** — it is "width ×2 + value," and a partial cast-leg fix will not flip the cell; the cast leg is *measured* for distance only, the flip is not claimed. Expected contribution: **+1**.

---

### E5 — Deliverable / ref-graph completion (scope-gated, MEASURED not counted)

> **STATUS 2026-06-08: RESOLVED — NO-GO / REJECTED (h0035).** The scope-gated ref-graph
> deliverable-completion rule was **INERT** on `quickbooks001` (the only target it could flip): the
> solver wrote ONE new model (`quickbooks__general_ledger.sql`, the schema-declared red signal) and
> the three needed `stg_quickbooks__*` staging models never appeared as project files — `green-via-
> package-namespace masks the dangling-ref trigger → inert` (the project builds fully GREEN through the
> installed package's own namespace, so the solver hit "smallest fix → green → done" before reaching
> the set-difference; a new, sharper inertness mode than h0013/h0015's total read-failure). Distance
> bit-identical to @baseline (`Got 1`×6). **The scope-gate is VALIDATED bleed-free** — ZERO bleed on
> all 6 canaries; f1001 held 1.0 at the artifact level (its 14 `src_*` are @baseline-identical, the
> rule fired 0×) and the h0023 `stg_models_use_src_models Got 11` signature did NOT recur — so the
> net-new contribution (fire only on the project's own referenced-but-absent set) fixed the h0023
> over-fire even though the lever itself was inert. **5th package/incomplete-deliverable rejection
> (h0009 −3 / h0013 inert / h0015 inert / h0023 f1001-bleed / h0035 inert); family EXHAUSTED, 5-for-0,
> oracle/inertness-blocked.** MEASURED-not-counted: a REJECTED target flip does NOT lower @baseline —
> it remains **31/48**. Transferable lesson recorded in `_artifacts/verification-without-oracle.md` +
> `_artifacts/bug-type-taxonomy.md`. No follow-up filed (family dead; next direction is a captain
> strategy call).
- **What we test:** does ref-graph/package resolution, scoped to explicit `_existence` failures, build the 3 missing models without convention-bleed?
- **The independent path & method:** resolve the `ref()` graph + installed `fivetran/quickbooks` package; the 3 absent `stg_quickbooks__{estimate,refund_receipt,sales_receipt}` models exist as package templates and are named exactly by the failing `_existence` tests (ref-graph independence passes the sharp test — it is independent of content). **Scope-gate the deliverable-set clause to tasks with an explicit missing-model `_existence` signal** (h0023 lesson: an unscoped clause regressed f1001 6/6→2/6 by treating any installed package as a source).
- **What evidence we want:** the 3 model names appear and build (h0013/h0015 inertness was 0× appearance); `_existence` flips; zero f1001-style invented-`src_*` regression (≥2 perturbable canaries).
- **Pass-kill:** PASS = all 3 `_existence` flip (and ≥1 `_equality`). **KILL** = inert (models never built, the h0013/h0015 signature) OR convention-bleed regresses f1001/quickbooks003.
- **Sequence rationale:** this is the **highest-bleed-risk task in the benchmark** — h0009 (−3), h0013 (inert), h0015 (inert), h0023 (f1001 6/6→2/6) **all bled or died here** (4 attempts, 0 flips). It runs LAST among flip-seekers, only after E0–E4 have proven the perturbable-canary guard catches bleed.
- **Future hypothesis stub:** `h0015-successor` (scope-gated deliverable-set). Expected contribution: **{0 or 1} — MEASURED, not counted toward the net.**

---

### Track Z — ENFORCED abstention rail (LOW-control; success = zero-regression + honest non-answer)
- **What we test:** can we *mechanically enforce* abstention on oracle-only claims so the lever neither flips (impossible) nor regresses (the real risk) — converting h0031's silent `abstained_claims: []` into a mandatory non-answer?
- **The independent path & method — the MECHANICAL TRIGGER (the critique's MF-3 fix):** abstention is not a "MUST abstain" instruction (that is the exact prose altitude that produced `[]`). It is a concrete, checkable precondition written to `arbitration.json`:
  > **IF** no tier-1 instruction names the load-bearing fact (e.g. the column set / grain convention) **AND** no tier-2 schema declaration names it truthfully **AND** no raw-source conservation/coverage probe contradicts either candidate **THEN** emit `ABSTAIN` and leave the @baseline answer untouched — do NOT author a confident value.
  Grounded in selective prediction (Chow 1970, IEEE TIT 16(1); Geifman & El-Yaniv 2017, NeurIPS / arXiv:1705.08500) and risk control under no labels (Angelopoulos et al. 2022, *Conformal Risk Control*, arXiv:2208.02814, ICLR 2024).
- **What evidence we want:** **zero regression** on all LOW-control tasks; `arbitration.json` records `ABSTAIN` on each oracle-only claim (the artifact proof abstention fired); NO byte-identical-wrong-answer-with-false-confidence (the f1011 `ABDE` h0031 signature). **Track Z is generative-adjacent** (it touches arbitration on every LOW task) → it needs its **own ≥2 perturbable canaries** to prove it doesn't regress passers.
- **Pass-kill:** PASS = zero regression + every oracle-only claim recorded as ABSTAIN. **KILL** = any regression, OR a non-answer dressed as a confident wrong answer (Phillips et al. 2026, *Entropy Alone is Insufficient for Safe Selective Prediction in LLMs*, arXiv:2603.21172 — the confidently-wrong regime).
- **Sequence rationale:** runs in parallel as a SAFETY rail, not a flip-seeker; its whole purpose is to keep LOW-control tasks from contributing *negative* net while the flip experiments harvest HIGH-control wins.
- **Captain carve-out (2026-06-07):** enforced abstention applies to **asana004 / asana005 / asana005-hard / ana-eng004 / f1002 / ana-eng007 / ana-eng007-medium**. **f1006 and f1011 are EXEMPT — they stay free to attempt** (already-failing + Mini-proven-solvable → free upside), are NOT portfolio-counted, and any flip there is treated as luck (h0031 proved f1011's local evidence misleading), not method.
- **Future hypothesis stub:** `h00Z-abstention-gate` (enforced-abstention harness; successor to h0031's `abstained_claims` failure). Expected contribution: **0 flips, protects the net.**

---

### Honest portfolio math (the critique's MF-1 fix — there is NO +7, NO 2-flip buffer)

| Experiment | Target(s) | Expected flips |
|---|---|---|
| E0 | (instrument gate) | 0 (enables all below) |
| **E1** | intercom001/002/003 | **{0 or 3}** — bimodal cluster bet, ONE shared mechanism |
| E2 | airbnb009 | +1 (clean, anti-cross-join) |
| E3 | airbnb007 | +1 (demonstrated flip) |
| E4 | asana002 | +1 (mini-confirmed) |
| E5 | quickbooks001 | **{0} landed (MEASURED, REJECTED/h0035 — INERT, zero bleed; family exhausted 5-for-0)** |
| Track Z | the 9 LOW-control tasks | 0 — protects the net |

- **Realistic mode if E1 stays inert:** E2+E3+E4 = **+3 → 34/48, short of 75%.**
- **Best case:** E1(3)+E2+E3+E4 = **+6 → 37/48**, with E5 a possible 7th.
- **The plain statement for the captain: this program reaches 75% ONLY IF the intercom grain reconcile breaks the inertness wall that has held three times.** Everything else is +1-or-0 singletons. That is the bet.

---

## 6. Measurement & regression guards

### 6.1 Distance-to-pass methodology
- **Primary metric:** the oracle's `Got N` per target, read from `runs/.../ade-bench-<task>__*/verifier/test-stdout.txt`.
- **Leading indicator = distance shrink** before a flip. A construct that reaches committed SQL but doesn't pass (h0016 `Got 7→5`) is iterable signal; a construct that leaves distance flat (`Got 7→7`, h0010) is **inert** and dies. For E1 specifically the threshold is **distance < 5** (anything ≥5 is the same wall h0016 hit).
- **Lagging indicator = flip** (FAIL→PASS) confirmed at full.
- **Paired delta** computed from `per_trial_outcomes.json`, slug-paired + 10k bootstrap (the `rk runs diff` crash workaround per local memory), to separate true flips from variance — h0012's f1006 smoke-flip was variance and reverted at full.

### 6.2 Perturbable-canary smoke (the G8 law — and the unsatisfiability caveat)
Every smoke spec MUST carry, per family its targets share a construct with, **≥2 PERTURBABLE canaries** — currently-passing @baseline models the lever will *actually fire on*, not inert stable passers. One canary is necessary but NOT sufficient (h0012's single f1001 held while the lever broke four *other* f1 members → −4). The smoke set is presented in the REQUIRED boxed Task/Baseline/Should-pass/Role table (per `hypotheses/README.md` propose stage) with ❌✅🎯 glyphs, net, and ETA.
- **The SF-3 caveat (must be stated, not assumed):** h0030's reconcile is gated to "models whose grain is *meant* to be complete over a parent key set" — so it does **not** fire on the f1 `constructor_points` simple-aggregate passers that h0012 broke. The canaries that matter for E1 are **grain-completeness passers the lever WILL fire on.** Before smoke, we must **verify such a perturbable canary exists in @baseline**; if none does, the G8 requirement is *unsatisfiable for this family* and E1's regression surface is **blind at smoke** — that is a stated caveat, not a hidden assumption. (E0's injected-error fixtures partially substitute, but they are synthetic, not @baseline passers.)

### 6.3 The h0012 guard (gatekeeper preconditions, all REVISE-class-fixable in place)
- **G10:** self-correcting levers MUST be (a) figure-change-gated, (b) reconcile against a RAW/declared external source (not the solver's own CTE), (c) check-don't-replace. Generative + always-on + replaces = automatic FAIL (the h0012 shape).
- **G9:** selector/arbitration families need candidate DIVERSITY + an independent IN-decision falsifier; a uniformly-held plausible-wrong reading self-scores perfect (h0026). **This is why the program contains NO new candidate-generation/arbitration experiment — that family is EXHAUSTED (h0026 + h0031 meta-pattern).**
- **G8:** ≥2 perturbable canaries per shared family (§6.2).
- **G7:** structural-rewrite prose is predicted inert at gpt-5.5/xhigh — the explicit reason E1's primary kill-path is inert-REACH.

### 6.4 When to RETIRE a family
- **Inert twice** at distance (committed SQL unchanged, `Got N` flat across two phrasings) → retire (construct-prose grain already retired: h0010/h0016/h0017).
- **Regresses at full despite a clean smoke** → retire the *always-on/replace* variant; only a figure-gated check-don't-replace successor may re-file (h0012 → h0021/h0029/h0030).
- **Reproduces baseline's exact wrong answer with `abstained_claims: []`** on an oracle-only target → retire generation/arbitration on that target; the residual gap is **informational, not a selection weakness** (h0031). Move to Track Z.
- **Oracle-only by triage** → never enters the flip portfolio; lives in Track Z with success = zero-regression.

---

## 7. Open questions for the captain to debate

*(Plain-word question first; the technical detail is kept underneath each.)*

1. **We're betting almost everything on one risky fix.** The biggest group of failures is the "intercom" tasks, and our main fix for them is all-or-nothing — it flips 3 at once or flips none — and three previous tries at this same group moved nothing. *Are we OK leaning the whole plan on this one shaky fix, or do we want a backup approach to that group lined up first?*
   - *Technical:* this is the E1 bimodal {0, 3} bet. If the mechanical-number-bolted-to-rewrite still goes inert (the family's 3-for-3 prior — h0010/h0016/h0017 — and G7's "structural-rewrite prose is inert at gpt-5.5/xhigh" prediction), we land at +3 → 34/48. The program's risk is concentrated in E1.

2. **We might not have a safe way to test that fix.** Before trusting a fix, we want an already-passing task that the fix actually touches, so we can confirm it doesn't quietly break things. We're not sure such a task exists for the intercom fix. *If there's no real "safe test subject," is it OK to test using only made-up injected examples, or do we insist on a real one first?*
   - *Technical:* does a *perturbable* grain-completeness canary exist in @baseline (§6.2)? If not, E1's regression surface is blind at smoke and we ship E1 on E0's synthetic injected-error fixtures alone. Is that acceptable, or is a real perturbable canary a hard prerequisite?

3. **Even if the rest works, we land one short.** If everything except the risky intercom fix succeeds, we get +3 → 34 of 48 — just under the 75% goal. *Do we go find one more winnable task now, or run the plan as-is and see where we land?*
   - *Technical:* the honest ceiling without E1 is +3. Do we source a sixth visible-arbitrator candidate now (e.g. re-checking whether any LOW-control task has a *truthful* local declaration we mis-triaged), or run the program and reassess after the first results?

4. **For the impossible tasks: force "I don't know," or let it guess?** A handful of tasks can't be solved with what the solver can see. We can force it to say "I don't know" instead of guessing — that guarantees we don't break anything there, but also kills any lucky win. *Do we hard-force "I don't know," or leave it free to take a guess on a few of them?*
   - *Technical:* how hard do we enforce Track Z's mechanical abstention trigger? Enforcing `ABSTAIN` guarantees net-zero on the oracle-only tail but forecloses any lucky flip. Given h0031's confidently-wrong `ABDE` reproduction, the safe default is enforce — but is there a LOW-control task we'd rather leave the solver free to attempt?

5. **Five tasks are simply out of reach.** For five failures, the right answer isn't anywhere in what the solver is allowed to look at — no method can find it; only changing what information the solver receives would. *Do we treat that as a separate, later project, or just accept those five are off the table?*
   - *Technical:* five of the 17 (ana-eng004, f1002, f1006, asana004, f1011) have no recoverable local arbitrator. Reaching them requires changing what ships to the solver (a benchmark-design question), not a better lever. Separate workstream, or out of scope?

---

**Bottom line.** The path to 75% is not a smarter judge or a third route — those hit the correlated-error wall every time (h0012 regression, h0031 reproduction). It is **mechanical independent redundancy** — recompute from the raw parent key-count, fix the cross-join, copy the project's own passing sibling, assert the `information_schema` contract, resolve the package ref-graph — aimed only at the **HIGH-control visible-arbitrator tasks**, each instrument-validated by E0, each guarded against the h0012 regression by figure-gating + check-don't-replace + ≥2 perturbable canaries, with an **enforced, mechanically-triggered** abstention rail keeping the oracle-only tail at net-zero. The honest yield is **+3 to +6**, and **75% rides on the intercom grain reconcile breaking a three-time inertness wall.** That is the bet, stated plainly.

---

**Citations — internal:** `hypotheses/_artifacts/{verification-without-oracle.md, arbitration-without-oracle.md, bug-type-taxonomy.md, WORKFLOW-REFINE.md, term-table.md}`; `hypotheses/_archive/h00{08,09,10,12,16,17,20,23,26,31}*.md`; filed `hypotheses/h00{18,19,21,29,30}*.md`; `hypotheses/_gatekeeper/propose-review-guideline.md` (G7/G8/G9/G10); baseline cells `runs/ade-bench-baseline/622bdedac572b479/ade-bench-<task>__*/verifier/test-stdout.txt`.

**Citations — public:** Barr et al. 2015 (TSE 41(5)); Chen et al. 2018 (CSUR 51(1)); Knight & Leveson 1986 (TSE SE-12(1)); McKeeman 1998 (DTJ 10(1)); Claessen & Hughes 2000 (ICFP); Ratner et al. 2016 (NeurIPS / 1605.07723), 2020 (VLDBJ 29); Jaffe, Nadler & Kluger 2015 (AISTATS); Ernst et al. 2007 (SciCompProg 69); Chu, Ilyas & Papotti 2013 (PVLDB 6(13)); Lewis et al. 2020 (RAG, NeurIPS); Ni et al. 2023 (LEVER, ICML / 2302.08468); Chow 1970 (IEEE TIT 16(1)); Geifman & El-Yaniv 2017 (NeurIPS / 1705.08500); Angelopoulos et al. 2022 (Conformal Risk Control / 2208.02814, ICLR 2024); Wynn, Satija & Hadfield 2025 (2509.05396); Phillips et al. 2026 (2603.21172).
