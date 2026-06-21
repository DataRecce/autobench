# DAB Self-Learning Log

Append one entry per concluded hypothesis: verdict (PASSED/REJECTED), the concrete dial it
moved or ruled out, and the transferable takeaway. Keyed to committed-artifact evidence.
- dab0009 (anti-abstention) REJECTED as board lever: real flip on googlelocal-q3 (3/3) but net -0.010 vs matched ref; generative lever perturbs 6/7-stable cells it never touches (related-not-causal per 5 Opus + 5 CAIS run-history). Lean v2 (None carve-out + failure-gated db_config) sim-cleared the 2 perturbation risks -> dab0010. Diagnostic logic codified in unexpected-result-playbook.md.
- dab0010 (anti-abstention LEAN v2) REJECTED: mechanism-cleared of causation but two STABLE cells (crmarenapro-q7/q12, 6/7+) came in 1/3 — captain bar: destabilizing stable cells is unacceptable regardless of causation. Anti-abstention family concluded (v1 net-neg, v2 cleared-but-destabilizing). Lesson: a global README lever can't PROVE stable-cell safety at low trial counts; next lever must be precondition-gated + judged vs a multi-trial no-lever baseline. -> built the multi-trial baseline artifact _artifacts/baseline-variance-6draw.md (no entity needed).
- dab0008 (gpt-5.5 @HIGH tier control) REJECTED: high 0.5733 < xhigh 0.6002 < Opus 0.6536; NO tier advantage (gap within single-trial noise + 3 stable-cell single-draw misses). dab0005 premise REFUTED — crmarenapro-q2/q8 fail clean at high (0/6 never-pass); prior gpt-high 1/1 was a single-draw phantom (same trap as dab0009/dab0010). KEEP xhigh as the no-lever tier. Two highest-EV families (anti-abstention, tier) now both closed.

## dab0012 (REJECTED, 2026-06-18) — README cannot suppress output-shape at gpt-5.5
stockmarket-q3 (gpt 0/6, computes the right ranking, fails only by decorating each row with the
company description). Two mechanism-distinct README levers both INERT by committed artifact:
cycle 1 generation-time prose rule (smoke 9eee91ea), cycle 2 executable verify-stage strip
(smoke 6884375f — discussed in transcript, not applied; clean read, canaries held). Boundary:
output-shape suppression is unreachable via the solver README — it's a generation-time "be helpful"
reflex the model doesn't perceive as wrong, the README has no enforcement under it, and self-verify
is correlated with the error. Fix is verifier-side (benchmark change), not a solver lever. Pre-empts
dab0013/dab0014 (same axis). Full reason+suggestion: _artifacts/readme-cannot-suppress-output-shape.md

## dab0015 (VALIDATED, NOT PROMOTED, 2026-06-19) — flat-string serialization works (1 cell)
First gpt-5.5 lever to GO. A `## Answers` README rule pinning flat-string (not JSON) serialization,
framed as a matcher-correctness consequence. Attributable result: googlelocal-q2 ONLY — 2/6 baseline →
adopted the flat-string committed artifact and PASS across 3 consecutive draws (smoke + full-1 + full-2).
~1 cell, ~+1.4 pts stratified (within the ±3 noise floor). Zero lever-caused regression across 54 cells
(over-flatten falsifier never fired). yelp-q6 DOWNGRADED on FO artifact re-check: 4/6 baseline, one
lever-draw, full-list form is not lever-specific, no rule-citation → not counted as lever evidence.
Captain chose validated-but-NOT-promoted: a single within-noise cell doesn't warrant a seed-README edit;
rule + knowledge recorded for future composition. KEY KNOWLEDGE: output SERIALIZATION-format is
README-steerable at gpt-5.5 (deliberated choice), whereas the DECORATION reflex is NOT (dab0012 dead-family)
— reflex-vs-deliberated distinction now empirically grounded. INFRA: full-1 PG-volume concurrency collision
(fixed, PR #18) + full-2 Mongo serverSelectionTimeout; a fully-clean 54-cell board stayed elusive (different
backend dropped each run). Detail: dab0015 entity ## Conclusion (commit 9ca5a8c).

## Workflow refit (2026-06-21) — autonomous run policy (auto-gate to full-run launch)
Added `## Autonomous run policy` to the DAB workflow README + inline auto-gate notes on propose/smoke.
Encodes the guarded auto-pipeline distilled from dab0015: automate the mechanical spine + the clean
happy path through propose → smoke → the full-run LAUNCH; HALT+escalate on judgment. Default stays
captain-gated; autonomous mode is opt-in per hypothesis (drive the FO under /loop). Key guardrails:
propose auto-APPROVE = gatekeeper APPROVE + FO reject-checks; smoke→full auto-advance = strict-audit-clean
+ 0 coverage_missing + target-flipped-by-committed-artifact + canaries-held + backend-health + LOW-BASELINE
target (the yelp-q6 4/6-trap: a single pass on a multi-pass cell is not lever evidence). Never auto:
conclude/promote/seed-README-edit, strategy (lever choice/retarget/pivot/revise-vs-reject), infra code
fixes, or an UNEXPECTED result (→ unexpected-result-playbook). Infra is NEVER counted as a result.
