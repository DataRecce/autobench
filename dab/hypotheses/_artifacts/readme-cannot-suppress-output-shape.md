---
title: Why the solver README cannot fix output-shape failures at gpt-5.5/xhigh — and what would
date: 2026-06-18
status: boundary finding — two mechanism-distinct README levers (dab0012 cycle 1 + cycle 2) both inert, clean reads
evidence:
  - dab0012 cycle 1 (prose rule)   smoke 9eee91ea2489003e — stockmarket-q3 committed answer byte-identical, still decorated
  - dab0012 cycle 2 (verify-step)  smoke 6884375f9d7aff15 — same; transform discussed in transcript, NOT applied; canaries all held (clean read, no infra confound)
bears_on: dab0013 (anti-decoration prose), dab0014 (list prose) — same axis, pre-empted dead; the dab0001 output-contract family is closed for the gpt-5.5 solver
---

# The failure we tried to fix

`stockmarket-q3`: gpt-5.5 computes the **exact correct** ranking (the same 15 troubled-NASDAQ companies
and 2008 average volumes Opus computes) and then **decorates every row with the company's description**
— `"Apex Global Brands Inc. specializes in creating and marketing…: 23781.42; …"`. The DAB verifier does
a normalized-string match and rejects the narrative. The computation is right; only the output *shape* is
wrong. This is the cleanest "lever should fix it" signal in the target set (gpt 0/6, Opus 5/6).

# What we tried (two mechanism-distinct README levers, both inert)

| cycle | mechanism | result | committed `stockmarket-q3` answer |
|---|---|---|---|
| 1 | **generation-time prose rule** — "emit `name: number` only, never `name (description): number`" in `## Rules`, shape-branched, foreign-domain examples | NO-GO | byte-identical to baseline — still fully decorated |
| 2 | **executable verify-stage transform** — "before writing `answers.json`, strip the parenthetical/description off each ranking row, re-serialize, regex-confirm no `(` before a value" in `### verify` | NO-GO | byte-identical again; transcript shows the strip was *discussed* (`normaliz`, `parenthetical`) but **not applied** to the file |

Cycle 2 was a clean read — all backends up, every cell completed, and the three canaries (`stockmarket-q1`,
`stockmarket-q2`, `music_brainz_20k-q1`) all held PASS, so the strip didn't over-fire either. The lever
simply did nothing to the committed answer.

# Why the README can't fix this (root cause)

The README only has leverage over what the solver **deliberates and chooses**. This failure is none of
those things:

1. **It's a generation-time reflex, not a decision.** The decoration is emitted while the model serializes
   its final answer — a "be helpful / be informative" reflex, downstream of the planning context where a
   README instruction has purchase. The model can carry the rule in its reasoning and still not bind its
   own serialization step. We saw exactly this in cycle 2: it *talked about* normalizing, then wrote all 35
   decorated rows anyway.
2. **A stable temperament prior overrides a contextual instruction.** gpt-5.5 is *output-elaborative* by
   disposition (the cross-learning study, `model-strengths-cross-learning.md` §2a/§4). That bias is a trait,
   not a wording gap — so no phrasing of "don't elaborate" closes it, the same way Opus's "always produce an
   answer" prior ignores the abstention license it's given.
3. **Self-verification is correlated with the error (oracle-blind wall).** The verify step is run by the
   *same* model that injected the descriptions. It re-reads its answer, sees nothing wrong (it thinks the
   descriptions are a *feature*), and doesn't strip. An instruction asking the model to check its own output
   cannot catch an error the model does not perceive as an error — this is the same self-anchored false-green
   wall as `[[verification-without-oracle-real-world]]`.
4. **The README is solver-discretionary — there is no enforcement.** Nothing sits between the solver's
   answer and the verifier. Both framings (rule, executable step) rely on the solver's discretion to comply,
   and the solver's discretion is precisely what is biased. A directive with no gate under it has a ceiling
   of "the wording is present" — which is not behavior.

Net: output-shape suppression at gpt-5.5/xhigh is **not reachable through the solver README at all** —
neither an abstract rule nor a concrete executable step changes the committed answer string. The
description-injection *diagnosis* is correct and robust; the *fix-via-README* is dead. We did not run a
third fork (a SQL `name || ': ' || value` skeleton) because it has the same root vulnerability — it is still
a README directive the model can compute around and re-decorate at answer time — so the boundary predicts it
inert too.

# Suggested way forward

A fix would have to come from **outside the solver's discretion**. The only two places that could live are
both unavailable to this loop:

1. **The benchmark's verifier (DAB ground-truth scorer) — OFF-LIMITS, never.** One *could* make the scorer
   strip descriptions before the string compare, but changing the benchmark scorer is **tampering**: it
   re-baselines every model, invalidates every reference number (`@baseline`, the 6-draw band, the CAIS
   runs), and inflates the score without the model improving. Standing captain rule: **we do not change the
   benchmark verifier.** Not a path.
2. **A non-model post-process step in the solver workflow.** A deterministic regex normalizer run on
   `answers.json` before submission (code, not a README instruction the model executes) would suppress the
   decoration — but the spacedock solver is README-only (`agent.kind: spacedock_solver`, the model does
   everything), so this is a workflow-structure change that redefines what "the solver" is, and it isn't the
   kind of lever this loop runs. Effectively out of scope.

Note the in-scope analog was already exhausted: the solver's own **`### verify` stage** (which *is* part of
the editable README) was cycle 2 — an executable strip the model is told to run — and it was inert (the
model discussed it and didn't apply it). So the editable-by-us channel (both `## Rules` and `### verify`) is
done, and the only mechanically-effective channels are forbidden (benchmark scorer) or out-of-scope
(non-model workflow code).

**Therefore: output-shape is a genuine DEAD FAMILY for this loop.** Close the `dab0001` output-contract
concept — including the still-queued **dab0013** (anti-decoration prose) and **dab0014** (list prose), which
sit on the same axis and are pre-empted dead by this boundary — and spend the loop on cells where the gap is
something the solver actually **deliberates** (analysis / interpretation / persistence), not its
serialization reflex.

**Bottom line for the captain:** we can't make gpt-5.5 stop decorating its answers by editing the README —
the decoration is a built-in "be helpful" reflex it doesn't perceive as wrong, and the README has no
enforcement under it. The only mechanically-effective fix lives in the benchmark scorer, which we will not
touch. So this cell is unwinnable within the loop's rules: output-shape is closed — pivot to analysis-side
cells.
