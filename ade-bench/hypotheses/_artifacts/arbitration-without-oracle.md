# Arbitration Without an Oracle

This note is for future ideation and propose-stage review. Use it when a hypothesis
adds a second path, a reviewer, a reconciliation check, or a candidate selector.

The problem is not "write a better prompt." The problem is:

> How do we decide what to trust when the solver cannot see the hidden answer key,
> self-checks can false-green, and two independent-looking paths may disagree?

The answer from real-world verification work is two-step:

1. Create an independent path that does not share the solver's original error.
2. Define an arbitration rule for disagreements before running the experiment.

The second step is load-bearing. A second path detects uncertainty; it does not
automatically identify the correct answer.

## The Abstract Problem

ade-bench gives the solver a local workspace and hides the grading oracle. The solver
can build a plausible artifact, validate it against its own framing, and still fail
the hidden tests. This is a self-anchored false-green.

Opening a second path helps only if it is genuinely independent:

- A raw-source recompute can catch a value error.
- A declared schema comparison can catch missing columns.
- A parent-key count can catch dropped grain rows.
- A second implementation can expose disagreement.

But if path A and path B produce different answers, we still need to decide what to
do. Without an arbitration rule, the system just moves the guess from "solver picks
an answer" to "reviewer picks an answer."

That is not progress.

## Real-World Pattern

Mature fields handle this by separating "independent evidence" from "arbitration."
The arbitrator is usually not a smarter person. It is a pre-declared evidence rule.

| Field | Disagreement | Arbitrator |
|---|---|---|
| Accounting | Ledger and bank records disagree. | Bank statements, invoices, receipts, payment records. If they do not tie out, record an unreconciled item. |
| Science | Two labs get different results. | Pre-registered protocol, sample design, instrument calibration, statistical method, and replication. If unresolved, the claim remains unsettled. |
| Medicine | Two tests disagree. | Gold-standard test when one exists, such as biopsy, PCR, or imaging. Without enough evidence, keep a differential diagnosis. |
| Law | Witnesses conflict. | Evidence hierarchy: documents, physical evidence, timeline, cross-examination, and burden of proof. If the proof standard is not met, do not convict. |
| Journalism / intelligence | Two sources report different claims. | Source independence, documentary evidence, chain of custody, and disconfirming evidence. If not confirmed, mark as unverified. |
| Compiler testing | Two implementations produce different outputs. | Language spec, reduced test case, reference interpreter, or a third implementation. Disagreement first means "at least one is wrong," not "we know which one." |
| Safety engineering | Sensors or operators disagree. | Redundant sensors, calibration checks, voting rules, and fault states. If the sensors cannot be reconciled, enter a safe/fault mode. |

The common rule:

> Do not choose the answer that sounds better. Choose only when higher-authority,
> reproducible evidence invalidates one side. Otherwise abstain.

## What Arbitration Is

Arbitration is a decision rule over evidence.

It should produce one of three decisions:

- `SELECT_A` / `SELECT_B`: one candidate satisfies the higher-authority evidence and
  the other violates it.
- `REJECT_BOTH`: both candidates violate a hard local rule.
- `ABSTAIN`: visible evidence cannot distinguish the candidates.

`ABSTAIN` is a valid and important result. It prevents the workflow from pretending
that hidden-oracle facts are locally knowable.

## Evidence Hierarchy for ade-bench

Use this hierarchy when designing an arbitrator:

1. Explicit task instruction.
2. Declared local contract: `schema.yml`, model description, column list, declared tests.
3. Raw source data and conservation relations.
4. Project-local tests and dbt constraints.
5. Same-project sibling model patterns.
6. Installed package artifacts, only when the task/project clearly uses that package shape.
7. Candidate transcript, plan, or self-written contract.

The bottom layer can explain behavior, but it should not decide correctness by itself.

Candidate reasoning is debug evidence, not an arbitrator.

## Ade-Bench Arbitration Patterns

### Width / Missing Columns

Independent path:

- Extract declared columns from `schema.yml` and the task instruction.
- Extract produced columns from the candidate model.
- Compute `declared - produced`.

Arbitration:

- Select the candidate with an empty declared-column deficit.
- Reject candidates missing declared columns.
- Abstain if the expected columns are not declared locally and only the hidden oracle
  distinguishes the width.

### Grain / Missing Rows

Independent path:

- Identify the local parent relation that defines the key set.
- Compute `COUNT(DISTINCT key)` on the parent.
- Compare it to the candidate output `COUNT(*)`.

Arbitration:

- Select the candidate that ties out to the parent key count and preserves required
  keys.
- Reject candidates with fewer rows than the parent count when no explicit filter
  justifies the drop.
- Abstain when the hidden solution encodes an intermediate-model convention that the
  task, schema, and local code do not specify.
- **Abstain (or treat the count as non-arbitrating) when the parent key set is itself
  filter-correlated with the candidate (h0030).** If both the parent and the child
  inherit the same upstream `active`/effective-date filter, `COUNT(DISTINCT parent_key)`
  collapses to the same scoped key set as the candidate and the count + anti-join agree
  even though the grain is wrong. The parent-key count only arbitrates when the parent's
  population is unambiguous and filter-free; "which population is canonical" (h0030's
  intercom 2-vs-5 split) is an oracle-only fact, not a locally-arbitrable one. See
  `verification-without-oracle.md` → correlated-error-through-a-shared-upstream-filter.

### Value Divergence

Independent path:

- Recompute the target metric from raw source by a structurally different route.
- Compare the candidate value to that recompute.

Arbitration:

- Select the candidate that reconciles to the raw-source recompute.
- Reject candidates that validate only against their own model output.
- Abstain when no conservation relation or raw-source recompute is locally derivable.

### Answer-Style Tasks

Independent path:

- For each option, run a local query or file read that can support or refute the option.
- Prefer disconfirming checks for included options.

Arbitration:

- Include an option only when it survives a specific local check and no stronger
  disconfirming evidence is found.
- Exclude unsupported options by default.
- Abstain or mark unresolved if the local workspace cannot distinguish the option.

Do not score an answer candidate only by completeness of its own table. h0026 showed
that a complete table can still be a self-anchored false-green.

### Candidate Selectors

Independent path:

- Run multiple candidates in isolated workspaces or force candidate divergence.
- Score final artifacts, not solver chatter.
- Use external checks: schema diff, raw-source reconcile, invariant checks, no-harm
  diff filters.

Arbitration:

- Select only if the scorer uses evidence outside the candidate's own reasoning.
- Reject candidates with unrelated rewrites or hard local failures.
- Abstain if all candidates share the same unverified premise.

Majority vote is not enough. If every candidate shares one misconception, majority
vote just amplifies the common-mode error.

## Required Fields for Future Hypotheses

Any hypothesis that introduces a second path, reviewer, reconciliation check, or
selector should answer these before propose:

1. What is the first path?
2. What is the independent second path?
3. What error is the second path independent from?
4. What higher-authority evidence arbitrates a disagreement?
5. What are the `SELECT`, `REJECT_BOTH`, and `ABSTAIN` conditions?
6. What run artifact proves arbitration actually happened?
7. What kind of hidden-oracle fact would force abstention?

If a hypothesis cannot answer item 4, it may still be useful as a diagnostic probe,
but it should not be sold as a pass-rate improvement mechanism.

## Example Arbitration Artifact

For every selector or reconciliation hypothesis, save a machine-readable artifact like:

```json
{
  "decision": "SELECT_CANDIDATE_2",
  "reason": "candidate_2 satisfies the raw parent row-count invariant; candidate_1 drops 7 parent keys",
  "evidence_authority": "raw_source_count_distinct_parent_key",
  "hard_failures": {
    "candidate_1": ["row_count_mismatch"],
    "candidate_2": []
  },
  "abstained_checks": []
}
```

If no visible tie-breaker exists:

```json
{
  "decision": "ABSTAIN",
  "reason": "both candidates satisfy visible contracts; the expected intermediate grain is an oracle-only convention",
  "evidence_authority": null,
  "hard_failures": {},
  "abstained_checks": ["oracle_only_intermediate_grain"]
}
```

## Anti-Patterns

Reject or downgrade hypotheses that rely on these:

- "Ask another agent which candidate is more reasonable."
- "Score the candidate by its own checklist."
- "Use majority vote without proving candidate independence."
- "Confirm that the plan sounds like the question."
- "Trust transcript claims without checking final artifacts."
- "Pick a side even when the visible workspace cannot distinguish the answers."

These are correlated checks. They recreate the same self-anchored false-green.

## Implication for the 75 Percent Goal

The path to 75 percent pass rate should prioritize tasks whose failures have visible
arbitrators:

- Raw-source reconciliation.
- Declared schema or instruction contracts.
- Parent-key or date-spine invariants.
- Local project tests or constraints.
- Disconfirming option-level checks.

Tasks whose deciding fact lives only in `solution/` or hidden tests should be marked
as low-control candidates. They may still be measured, but they should not be central
to the planned +5 pass-rate portfolio.

## Related Local Artifacts

- `verification-without-oracle.md`: the broader real-world toolkit for independent
  checks.
- `WORKFLOW-REFINE.md`: current learnings from Output Contract, Plan Reviewer, and
  selector experiments.
- `bug-type-taxonomy.md`: which ade-bench bug classes are locally arbitrable.
- `_gatekeeper/propose-review-guideline.md`: propose-stage rules that should reject
  self-anchored selectors and inert README-prose hypotheses.
