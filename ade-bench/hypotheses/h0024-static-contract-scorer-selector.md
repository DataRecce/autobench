---
id: h0024
title: Static Contract Scorer Selector -- run multiple baseline candidates and choose by local build/artifact contract score
status: conclude
kind: hypothesis
source: concept-candidate-selector-contract-scorer fan-out; tests the static scorer selector design, not a new failure-pattern README rule. Forks the current @baseline solver protocol only as a declared protocol-family variant.
started: 2026-06-05T09:42:10Z
completed:
verdict:
score:
worktree:
---

## Hypothesis

The current pass@1 protocol commits the artifact from one candidate solve. Pass@k evidence
means that, for some tasks, another candidate in the same family of attempts may already
contain the right artifact. This hypothesis tests whether a deterministic local scorer can
choose a better committed artifact without using the hidden oracle.

**Falsifiable claim:** for each smoke task, run `N >= 3` independent candidates with the
current `@baseline` solver README unchanged, then choose the final committed artifact with a
static Contract Scorer that uses only local workspace evidence. The scorer does not ask a
candidate to write a new contract. It scores the final files directly:

- build health: `dbt compile`, targeted `dbt run`, targeted `dbt test`, or selected
  `dbt build` succeeds for the touched scope;
- artifact shape: required refs/models exist, schema-declared columns are present, and
  instruction-named deliverables are present;
- grain and key sanity: uniqueness/null/row-count checks reconcile against local sources or
  declared grain where that grain is locally derivable;
- type preservation: same-named columns keep local upstream/package types or apply an
  explicit local cast in the committed SQL;
- cleanup and no-harm: generated scratch is not committed, and unrelated package files,
  profiles, namespaces, dependencies, seeds, and unrelated models are not rewritten.

The claim passes smoke only if the selected candidate beats the single-candidate baseline on
at least one target where a local static contract can distinguish candidates, while preserving
all pass canaries. It is falsified if all selected artifacts are identical-or-worse than the
first candidate, if the scorer prefers locally invalid artifacts, or if the scorer needs hidden
verifier output to decide.

## Protocol-family declaration

This is a **protocol-family change**, not a standard solver-README-only hypothesis. It changes
candidate generation and selection: the runner must create multiple isolated candidate solves
for the same task, score each candidate's committed files locally, and commit only the
highest-scoring candidate. Results must be labeled separately from README-only experiments.
At propose, any spec/harness change must be declared as protocol-family metadata; do not claim
the independent variable is only the solver README.

## Target datasets

Smoke targets should exercise local, static artifact checks where hidden-oracle access is not
needed to reject a bad candidate:

- `ade-bench-asana002` -- package/type contract candidate where the local installed package
  type signal is concrete.
- `ade-bench-quickbooks001` -- missing local deliverable models can be detected through the
  `ref()` graph and installed package templates.
- `ade-bench-ana-eng006` -- build/shape/type checks can reject candidates that leave an
  obvious raw string/date mismatch or missing deliverables, even if width remains capped by
  oracle-only columns.
- `ade-bench-f1006` -- value-divergence reachability probe; included to test whether the
  static scorer is blind on locally underdetermined tasks.

Add currently-passing cross-family canaries at smoke because the protocol can select among
broader edits. Include at least `ade-bench-airbnb001`, `ade-bench-asana001`,
`ade-bench-f1007`, and `ade-bench-quickbooks002`; include `ade-bench-f1001` as the
non-package convention-bleed sentinel.

## Acceptance criteria

**AC-1 -- Candidate generation is real and isolated.** For every smoke cell, the run artifact
records `N >= 3` candidate workspaces/attempts with the same baseline solver README, same
model/runtime settings, and no shared mutable task state except the initial workspace copy.

**AC-2 -- Selection is leak-safe and auditable.** The scorer report is saved with the run
artifact and lists, per candidate, the local commands/checks used, the score components, and
the selected candidate. The report contains no hidden `AUTO_*`, `solution__*`,
`check_option_*`, verifier-output, public-fetch, web-search, or LLM-as-oracle references.
`rk audit --policy strict` stays clean on the selected run.

**AC-3 -- Static scoring beats first-candidate pass@1 on smoke.** On the target set, the
selected artifact should flip at least one target or strictly reduce the local distance-to-pass
without regressing any canary. A target with unchanged artifacts and unchanged `Got N` is
evidence that the selector was inert or blind for that cell.

**AC-4 -- The deep-dive verifies artifacts, not chatter.** Smoke analysis must compare the
selected committed SQL/files against the losing candidates and the first candidate, and explain
why the local scorer chose it. Candidate reasoning is not evidence unless the final artifact
satisfies the scored local contract.

## Gatekeeper review

## Smoke result

## Run result

## Behavioral analysis

No run was performed. This is a captain strategic kill on the basis of the sibling
evidence, not a falsification by run. The mechanism that sinks h0024 is the one already
demonstrated by **h0026** (and confirmed a second time by **h0031**): a selector that
scores `N >= 3` candidates by each candidate's **own** local-check completeness cannot
catch a **uniformly-held plausible-wrong** answer. When every candidate shares the same
locally-defensible-but-wrong reading (h0026: committed `ABDE` vs ground truth `ADE`,
failing the hidden `check_option_b`), each candidate self-scores perfect against its own
checks ("support 6/6, contradictions 0") and the highest scorer is still wrong. This is
the **self-anchored false-green** — the same wall as `solver-blind-to-oracle`.

h0024's static Contract Scorer (build health / artifact shape / grain / type / no-harm,
all scored on the candidate's *own* committed files) is exactly this design with a
different rubric. On a locally-underdetermined task — the very class the selector is
meant to fix — all candidates pass the same local contract and the scorer has no
**independent** signal to break toward the oracle's answer. The static-contract rubric
does not add candidate **diversity** (it does not force candidates to disagree on
borderline decisions) nor an **independent IN-decision falsifier**; it re-creates the
self-anchored trap with build/shape checks instead of decision-table checks. h0031
further showed that even *genuine* route divergence plus an *external-criterion*
arbitrator still reproduces the byte-identical wrong answer on oracle-only claims — so
adding diversity and an external scorer (the two things h0024 lacks) is *table stakes*,
not a fix. h0024 as written would land short of even that bar.

At propose, h0024 would now also fail gatekeeper rule **G9 (selector independence)** on
the judgment axis: its selection criterion is anchored solely to the candidate's own
checks with no external falsifier. The candidate-selector family from
`concept-candidate-selector-contract-scorer` is exhausted.

## Verdict

**REJECTED: sibling-killed by h0026** — a selector that scores `N >= 3` candidates by
their OWN local-check completeness cannot catch a uniformly-held plausible-wrong answer
(self-anchored false-green, the same wall as `solver-blind-to-oracle`). No run was
performed; this is a captain strategic kill on the sibling evidence, not a falsification
by run. Confirmed twice in the family: h0026 (decision-table selector, target did not
flip, all three candidates self-scored a uniformly-held `ABDE`) and h0031 (dual-contract
arbitration — genuine route divergence + external-criterion arbitrator still reproduced
byte-identical `ABDE` on the oracle-only claim). h0024's static Contract Scorer is the
same self-anchored design with a build/shape/type rubric; it adds neither candidate
diversity nor an independent IN-decision falsifier, so it would repeat the family wall.
Would fail propose gate G9 (judgment-independence axis) as written.

## Follow-up Routing

**stop** — the candidate-selector family is exhausted (oracle-blocked, no visible fork).
This verdict bears on the two remaining live siblings from the same
`concept-candidate-selector-contract-scorer` fan-out: **h0025** (output-contract-
satisfaction-selector) and **h0027** (do-no-harm-selector). Both share h0024's
self-anchored-scoring design and the same wall; neither should earn a run without first
showing how its selection criterion escapes self-anchoring (an independent IN-decision
falsifier or forced candidate divergence), and per h0031 even that is now table stakes,
not a contribution. Do not file another candidate-selector variant.

## Stage Report: conclude

- DONE: Write ## Verdict = REJECTED: sibling-killed by h0026 -- a selector that scores N>=3 candidates by their OWN local-check completeness cannot catch a uniformly-held plausible-wrong answer (self-anchored false-green, same wall as solver-blind-to-oracle). No run performed; this is a captain strategic kill, not a falsification by run.
  `## Verdict` + `## Behavioral analysis` written into the entity body; verdict states the self-anchored mechanism, cites h0026 + h0031 confirmation, and the G9 propose-gate fail.
- DONE: Write ## Follow-up Routing = stop: candidate-selector family exhausted; this verdict bears on siblings h0025/h0027.
  `## Follow-up Routing` = stop; names h0025/h0027 and the independence bar (G9) they must clear before any run.
- DONE: Finalize the workflow-refinement finding (AUTOMATIC for any workflow-structural hypothesis).
  Updated the existing family entry "Candidate-selector protocols: self-anchored scoring is a false-green" in `_artifacts/WORKFLOW-REFINE.md` with a 2026-06-11 family status line (rejected-as-written, family CLOSED, h0024 sibling-kill recorded); no duplicate entry created since the structural finding is the shared family wall already documented.

### Summary

h0024 is REJECTED as a captain strategic sibling-kill with no run. Its static Contract
Scorer is the same self-anchored-scoring design that h0026 falsified by run and h0031
confirmed survives even genuine candidate diversity + external arbitration; scoring N>=3
candidates by their own local checks cannot break a uniformly-held plausible-wrong answer
toward the oracle. Routing is `stop` — the `concept-candidate-selector-contract-scorer`
family is exhausted and CLOSED; the verdict steers the remaining siblings h0025/h0027,
which are now gated by propose rule G9. Frontmatter status/verdict/archived transitions
and the move to `_archive/` are left to the first officer's advance step.
